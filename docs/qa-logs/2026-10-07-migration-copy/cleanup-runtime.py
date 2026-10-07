#!/usr/bin/env python3
"""Retire only completed #502 owner runtime payloads, preserving compact evidence."""
import datetime, hashlib, json, os, pathlib, stat, subprocess
out = pathlib.Path(__file__).resolve().parent
receipt = out / 'cleanup.json'
assert not receipt.exists(), 'cleanup receipt already exists'
pids = json.loads((out / 'process-exits.json').read_text())['pid_list'] + [4077114]
check = subprocess.run(['ps', '-p', ','.join(map(str, pids)), '-o', 'pid=,stat=,comm='], capture_output=True, text=True)
assert check.returncode == 1 and not check.stdout.strip(), 'a recorded owner process remains'
assert not pathlib.Path('/workspace/tmp/pixelelated-m7-migration-copy-vm04/vm.pid').exists()
paths = [
 '/tmp/pixelelated-m7-migration-copy02/GuiMenu.cpp.o',
 '/tmp/pixelelated-m7-migration-copy03/emulationstation',
 '/workspace/tmp/pixelelated-m7-migration-copy-vm04/emulationstation',
 '/workspace/tmp/pixelelated-m7-migration-copy-vm04/vm.qcow2',
 '/workspace/tmp/pixelelated-m7-migration-copy-vm04/vm.ovmf-vars.fd',
 '/workspace/tmp/pixelelated-m7-migration-copy-vm04/qa-key',
 '/workspace/tmp/pixelelated-m7-migration-copy-vm04/qa-key.pub',
]
rows = []
for name in paths:
 p = pathlib.Path(name)
 s = p.lstat()
 assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and s.st_uid == os.getuid(), name
 row = dict(path=name, bytes=s.st_size, allocated_bytes=s.st_blocks*512)
 if not p.name.startswith('qa-key'):
  h=hashlib.sha256()
  with p.open('rb') as f:
   while block := f.read(1024*1024): h.update(block)
  row['sha256']=h.hexdigest()
 else: row['identity']='ephemeral QA key; contents and fingerprint not retained'
 rows.append(row)
for row in rows:
 pathlib.Path(row['path']).unlink()
 row['absent_after']=not pathlib.Path(row['path']).exists()
assert all(row['absent_after'] for row in rows)
result=dict(result='PASS', at=datetime.datetime.now(datetime.timezone.utc).isoformat(), process_check=dict(pids=pids, exit_code=check.returncode, stdout=check.stdout), files=rows, reclaimed_allocated_bytes=sum(r['allocated_bytes'] for r in rows))
receipt.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(dict(result='PASS', removed=len(rows), reclaimed_allocated_bytes=result['reclaimed_allocated_bytes'], receipt=str(receipt))))

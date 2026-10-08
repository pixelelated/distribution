#!/usr/bin/env python3
"""Finite synthetic write/refusal/systemd controls, followed by a power-cut checkpoint."""
import fcntl,hashlib,json,os,pathlib,shutil,signal,stat,subprocess,time
P=pathlib.Path;Q=P('/storage/qa519');F=Q/'followup';F.mkdir(mode=0o700)
assert 'ee014909137e03706e0b3020b8396be589aaa705' in P('/etc/os-release').read_text()
assert 'GENERIC_X64' in P('/etc/os-release').read_text()
assert (Q/'final.json').is_file() and json.loads((Q/'final.json').read_text())['passed']
S=P('/storage/.config/system/configs/system.cfg');C=P('/storage/.config/cloud_sync.conf')
def run(a,ok=(0,)):
 p=subprocess.run(a,text=True,capture_output=True,timeout=60)
 if p.returncode not in ok:raise RuntimeError((a,p.returncode,p.stdout,p.stderr))
 return p
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(name,x):
 results.append({'name':name,'pass':True,'detail':x});(F/'results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS '+name,flush=True)
def cfgstate():return {str(p):{'sha256':digest(p),'mode':stat.S_IMODE(p.stat().st_mode)} for p in [S,S.with_name(S.name+'.backup'),C,C.with_name(C.name+'.bak')]}
results=[];baseline=cfgstate()
run(['systemctl','mask','emustation.service','essway.service']);run(['systemctl','stop','emustation.service','essway.service'])
assert run(['pgrep','emulationstatio'],ok=(0,1)).returncode==1

# The actual writer must fail before replacing either live or fallback bytes.
tmp=S.with_name(S.name+'.tmp');assert not tmp.exists();tmp.mkdir()
p=run(['bash','-c','. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 1 cloudsaves.gameexit 1'],ok=(1,))
assert cfgstate()==baseline;tmp.rmdir();record('installed-settings-writer-refuses-unwritable-temp',{'rc':p.returncode,'all_original_hashes_and_modes_equal':True})
tmp=S.with_name(S.name+'.backup.tmp');assert not tmp.exists();tmp.mkdir()
p=run(['/usr/bin/chksysconfig','backup'],ok=(1,));assert cfgstate()==baseline;tmp.rmdir()
record('installed-last-good-writer-refuses-unwritable-temp',{'rc':p.returncode,'all_original_hashes_and_modes_equal':True})

# Root cannot be made unwritable with chmod. Exhaustion is represented by a
# small private tmpfs filled to capacity, so this is a real kernel ENOSPC.
small=F/'full';small.mkdir();run(['mount','-t','tmpfs','-o','size=64k,mode=700','tmpfs',str(small)])
try:
 (small/'target').write_bytes(b'complete-original\n')
 try:
  with (small/'fill').open('wb') as f:
   while True:f.write(b'x'*4096);f.flush()
 except OSError as e:assert e.errno==28
 try:
  with (small/'target.new').open('xb') as f:f.write(b'new-value\n');f.flush();os.fsync(f.fileno())
  os.replace(small/'target.new',small/'target')
 except OSError as e:assert e.errno==28
 else:raise AssertionError('ENOSPC did not refuse')
 assert (small/'target').read_bytes()==b'complete-original\n'
 record('atomic-publication-real-ENOSPC-preserves-original',True)
finally:run(['umount',str(small)])

# Genuine systemd KillMode=process lifecycle with an explicitly synthetic
# worker. It is not a fake ES runtime and is not claimed to be one.
worker=F/'worker.sh';worker.write_text('#!/bin/bash\nexec 9>/var/run/cloud_sync.lock\nflock -n 9 || exit 75\necho $$ > /storage/qa519/followup/worker.pid\nexec sleep 120\n');worker.chmod(0o700)
parent=F/'parent.sh';parent.write_text('#!/bin/bash\nsetsid /storage/qa519/followup/worker.sh >/storage/qa519/followup/worker.log 2>&1 &\nwhile :; do sleep 1; done\n');parent.chmod(0o700)
unit=P('/run/systemd/system/qa519-detached.service');unit.write_text('[Unit]\nDescription=QA519 synthetic detached worker\n[Service]\nExecStart=/storage/qa519/followup/parent.sh\nKillMode=process\nTimeoutStopSec=3\nRestart=always\nRestartSec=2\n')
run(['systemctl','daemon-reload']);run(['systemctl','start','qa519-detached.service'])
for _ in range(50):
 if (F/'worker.pid').exists():break
 time.sleep(.1)
pid=int((F/'worker.pid').read_text());identity=P('/proc',str(pid),'stat').read_text()
run(['systemctl','stop','qa519-detached.service'])
assert P('/proc',str(pid)).exists()
with open('/var/run/cloud_sync.lock','a') as lock:
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:pass
 else:raise AssertionError('detached worker lease not held')
assert cfgstate()==baseline
record('actual-systemd-process-killmode-leaves-detectable-lease-owner',{'worker_pid':pid,'proc_identity':identity,'unit':unit.read_text(),'config_unchanged':True})
os.kill(pid,signal.SIGTERM)
for _ in range(50):
 try:
  state=P('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()[0]
  if state=='Z':break
 except FileNotFoundError:break
 time.sleep(.1)
else:raise AssertionError('owned synthetic worker did not stop')
with open('/var/run/cloud_sync.lock','a') as lock:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
unit.unlink();run(['systemctl','daemon-reload']);run(['systemctl','reset-failed','qa519-detached.service'],ok=(0,1))

# Exercise the installed fallback consumer without permitting a remote write:
# temporarily empty only this invented alias file; load_config precedes the
# missing-remote refusal. The real consumer restores the aligned .bak.
rc=P('/storage/.config/rclone/rclone.conf');creds=rc.read_bytes();config=C.read_bytes()
try:
 rc.write_bytes(b'');C.write_bytes(b'SAVES_REMOTE="unfinished')
 p=run(['/usr/bin/cloud_backup','--yes','--saves-only'],ok=(1,))
 (F/'fallback-consumer.log').write_text(p.stdout+p.stderr)
 assert C.read_bytes()==config and cfgstate()==baseline
 record('installed-cloud-fallback-restores-aligned-guards-before-no-remote-refusal',{'rc':p.returncode,'no_remote_configured_during_control':True,'all_config_hashes_and_modes_equal':True})
finally:rc.write_bytes(creds)
assert rc.read_bytes()==creds
assert run(['/usr/bin/cloud_migrate_layout','--needs-step'],ok=(1,)).returncode==1
assert cfgstate()==baseline
run(['sync'])
(F/'power-checkpoint.json').write_text(json.dumps({'boot_id':P('/proc/sys/kernel/random/boot_id').read_text().strip(),'configs':baseline,'rclone_sha256':digest(rc),'save_sha256':digest(P('/storage/roms/savefiles/qa519.srm')),'recovery_sha256':digest(P('/storage/.cache/cloud_sync/replaced/qa519.srm')),'units':{u:run(['systemctl','show',u,'-p','ActiveState','-p','UnitFileState']).stdout for u in ['emustation.service','essway.service']},'scope':'deliberate power cut after fully guarded state and persistent masks; not every low-level filesystem timing'},indent=2)+'\n')
run(['sync']);record('durable-masked-recovery-checkpoint-ready',True)

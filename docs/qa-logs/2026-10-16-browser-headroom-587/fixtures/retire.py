from pathlib import Path
import json,os,stat,subprocess,hashlib,shutil,time
R=Path('/workspace/tmp/pix-m7-headroom-vm-20261016-02');E=Path('/workspace/tmp/pix-m7-headroom-evidence-20261016-01');run=Path((R/'run.path').read_text().strip())
consumed=json.loads((run/'admission-consumed.json').read_text());assert consumed['state']=='consumed' and consumed['id']=='5c8eeab34ebb4b30ae07af99fc0c7aa6'
assert hashlib.sha256((E/'acceptance.json').read_bytes()).hexdigest()==consumed['evidence_sha256']
exits=json.loads((E/'host-exits.json').read_text());assert all(x==0 for x in exits['original_channels'].values())
for row in exits['qemu_identities']+exits['command_identities']:
 p=Path('/proc',str(row['pid']),'stat')
 if p.exists():assert int(p.read_text().rsplit(')',1)[1].split()[19])!=row['start_ticks']
assert {p.name for p in (R/'vm').iterdir()}=={'disk.qcow2','OVMF.fd'}
records=[]
for name in ['disk.qcow2','OVMF.fd']:
 p=R/'vm'/name;s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1
 f=subprocess.run(['fuser',str(p)],capture_output=True,text=True,timeout=10);assert f.returncode==1 and not f.stdout.strip() and not f.stderr.strip()
 identity={'path':str(p),'inode':s.st_ino,'device':s.st_dev,'size':s.st_size,'allocated_bytes':s.st_blocks*512,'mtime_ns':s.st_mtime_ns}
 assert p.lstat()==s;p.unlink();assert not p.exists();records.append(identity)
shutil.copy2(run/'admission-consumed.json',E/'admission-consumed.json')
(E/'retirement.json').write_text(json.dumps({'status':'RETIRED_OWNED_DISK_AND_FIRMWARE','epoch':time.time(),'files':records,'allocated_bytes_recovered':sum(x['allocated_bytes'] for x in records)},indent=2)+'\n')
print('Retired',sum(x['allocated_bytes'] for x in records),'allocated bytes; compact evidence retained')

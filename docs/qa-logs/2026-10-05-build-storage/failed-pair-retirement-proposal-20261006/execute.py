"""Prepared fixed action; execute only after explicit owner approval of this two-file proposal."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,stat,subprocess
parser=argparse.ArgumentParser();parser.add_argument('--approved-plan-sha',required=True);args=parser.parse_args()
owner=Path('/workspace/tmp/pixelelated-m7-qa-disk-retirement-preflight-01');proposal=owner/'proposal.json';digest=hashlib.sha256(proposal.read_bytes()).hexdigest();assert args.approved_plan_sha==digest
p=json.loads(proposal.read_text());v=json.loads((owner/'owner-verification.json').read_text());assert set(v['channels'].values())=={'0'}
summary=json.loads((owner/'summary.json').read_text());assert all(summary[k]==0 for k in ['discovery_errors','qemu_errors','backing_matches','container_matches'])
assert (datetime.now(timezone.utc)-datetime.fromisoformat(p['utc'])).total_seconds()<900,'Refresh read-only dependency scan after15minutes'
publication=json.loads(Path('/workspace/tmp/pixelelated-m7-p4-source16-publication-01/publication.json').read_text());assert publication['remote_refs_verified']
base=Path('/workspace/tmp/pixelelated-m7-p4-no-join-negative-01/pair');allowed={base/'vm-a.qcow2',base/'vm-b.qcow2'};assert {Path(t['path']) for t in p['targets']}==allowed
assert not (owner/'execution.json').exists()
for entry in Path('/proc').glob('[0-9]*/cmdline'):
 try:a=[x.decode(errors='replace') for x in entry.read_bytes().split(b'\0') if x]
 except OSError:continue
 assert not (a and Path(a[0]).name.startswith('qemu-system-')),str(entry)
# Every precondition is checked before either unlink. Exact file identities only.
for t in p['targets']:
 f=Path(t['path']);s=f.lstat();assert stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1
 assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)==(t['device'],t['inode'],t['size'],t['mtime_ns'])
 with f.open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==t['sha256']
info=os.statvfs('/workspace');before=info.f_bavail*info.f_frsize;assert before+p['reclaim_bytes']>p['required_bytes']
removed=[]
try:
 for t in p['targets']:
  f=Path(t['path']);s=f.lstat();assert (s.st_dev,s.st_ino)==(t['device'],t['inode']);f.unlink();removed.append(t['path'])
finally:
 info=os.statvfs('/workspace');after=info.f_bavail*info.f_frsize
 receipt={'utc':datetime.now(timezone.utc).isoformat(),'approved_plan_sha256':digest,'removed':removed,'all_targets_absent':all(not f.exists() for f in allowed),'before_available_bytes':before,'after_available_bytes':after,'observed_available_increase':after-before,'scope':'Only two owner-approved failed01 QA disks; all evidence, successful02, source images and all build/candidate/source stores retained.'}
 (owner/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
assert receipt['all_targets_absent'] and after>p['required_bytes']

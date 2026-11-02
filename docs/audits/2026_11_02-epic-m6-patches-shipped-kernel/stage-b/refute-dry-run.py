#!/usr/bin/env python3
"""Reproduce the v2 dry-run disagreement without touching product source."""
from pathlib import Path
import subprocess,shutil,time,datetime,hashlib,json
R=Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688')
T=Path('/workspace/tmp/m6-t41'); A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/stage-b'
root=T/'src/refute-H700-same-input'; assert not root.exists();shutil.copytree(T/'src/pristine-H700',root)
order=(A/'order-H700.txt').read_text().replace(chr(92)+'u002d','-').splitlines()
def treehash():
 h=hashlib.sha256()
 for p in sorted(root.rglob('*')):
  if p.is_file():h.update(str(p.relative_to(root)).encode()+b'\0'+p.read_bytes()+b'\0')
 return h.hexdigest()
records=[]
def apply(i,dry):
 path=order[i-1];data=subprocess.check_output(['git','show','02aab33bd9842610b0d466c9c186454dc14373ee:'+path],cwd=R)
 args=['patch','-p1','-N','--batch','--directory',str(root)]+(['--dry-run'] if dry else [])
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();tic=time.monotonic();before=treehash();proc=subprocess.run(args,input=data,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);after=treehash()
 name=f'logs/same-input-H700-{i:03d}.{"dry" if dry else "apply"}.out';(A/name).write_bytes(proc.stdout)
 rec={'path':path,'patch_sha256':hashlib.sha256(data).hexdigest(),'command':args,'start':start,'elapsed_seconds':round(time.monotonic()-tic,3),'rc':proc.returncode,'before_tree_sha256':before,'after_tree_sha256':after,'output':name}
 records.append(rec);print(i,'dry' if dry else 'apply','rc',proc.returncode,flush=True);return rec
for i in range(1,11):assert apply(i,False)['rc']==0
trial=apply(11,True); actual=apply(11,False)
assert trial['rc']==1 and actual['rc']==0
assert trial['before_tree_sha256']==trial['after_tree_sha256']==actual['before_tree_sha256']
assert trial['patch_sha256']==actual['patch_sha256']
(A/'same-input-refutation.json').write_text(json.dumps(records,indent=2)+'\n')
print('PROVEN: identical source tree and patch bytes; dry-run rc=1; normal scratch apply rc=0')

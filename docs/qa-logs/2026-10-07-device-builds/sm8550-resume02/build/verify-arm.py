"""Read-only verification of accepted ARM payload and original build stamps."""
from pathlib import Path
import hashlib,json,os
p=Path('/workspace/tmp/pixelelated-m7-sm8550-build-02/artifacts/arm-output-manifest.json')
expected='41b6eaa2906661b6fbea165161e958edc42846feeff11cf03c2c935b01fb1ade'
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
j=json.loads(p.read_text());assert j['result']=='PASS'
root=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01/build.pixelelated-SM8550.arm')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024**2),b''):h.update(block)
 return h.hexdigest()
for name,value in j['files'].items():
 p=root/'image/system'/name;assert p.is_file() and not p.is_symlink() and sha(p)==value,name
for name,value in j['symlinks'].items():
 p=root/'image/system'/name;assert p.is_symlink() and os.readlink(p)==value,name
for name,value in j['stamps'].items():assert sha(root/name)==value,name
assert not any('/fex-emu/' in name for name in j['stamps'])
print('PASS original ARM manifest: %d files, %d symlinks, %d stamps; %s'%(len(j['files']),len(j['symlinks']),len(j['stamps']),expected),flush=True)

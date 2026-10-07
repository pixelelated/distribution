"""Preserve the enumerated interrupted scopes without deleting any payload."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01')
owner=Path('/workspace/tmp/pixelelated-m7-h700-arm-01')
root=tree/'build.pixelelated-H700.arm'
assert json.loads((owner/'owner-verification.json').read_text())['result']=='FAILED'
assert json.loads(Path('/workspace/tmp/pixelelated-m7-spirv-host-control-01/owner-verification.json').read_text())['result']=='PASS'
for p in [owner,Path('/workspace/tmp/pixelelated-m7-spirv-host-control-01')]:
    for pid in json.loads((p/'owner-verification.json').read_text())['pids_absent']:
        assert not Path('/proc',str(pid)).exists()
subprocess.run(['python3','-I',str(owner/'verify-source.py')],cwd=tree,check=True)
assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True).strip()
pres=json.loads((owner/'failure-preservation.json').read_text())
assert hashlib.file_digest(Path(pres['archive']).open('rb'),'sha256').hexdigest()==pres['archive_sha256']
expected={'gcc','glib','lxml','spirv-tools'}
found=set();scope=[]
for d in sorted((root/'build').iterdir()):
    pkg=d/'.rocknix-package'
    if not pkg.is_file():continue
    name=re.search(r'INFO_PKG_NAME="([^"]+)"',pkg.read_text())[1]
    contexts=[p for p in d.iterdir() if p.is_dir() and p.name.startswith('.') and ('linux-gnu' in p.name)]
    stamps=list((root/'.stamps'/name).glob('build_*'))
    compiled=False
    if not stamps:
        for base,dirs,files in os.walk(d):
            if any(f.endswith(('.o','.a')) for f in files):compiled=True;break
    if not stamps and (contexts or compiled):
        found.add(name);scope.append(d)
assert found==expected,(found,expected)
for name in expected|{'llvm'}:
    s=root/'.stamps'/name
    assert s.is_dir() and not list(s.glob('build_*'))
    scope.append(s)
unpack=root/'.unpack/llvm';assert unpack.is_dir();scope.append(unpack)
preserved=owner/'interrupted-scopes';preserved.mkdir()
plan=[]
for p in scope:
    dest=preserved/p.relative_to(root)
    assert not dest.exists()
    st=p.stat();plan.append({'source':str(p),'destination':str(dest),'device':st.st_dev,'inode':st.st_ino})
(owner/'recovery-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
for row in plan:
    source=Path(row['source']);dest=Path(row['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
    source.rename(dest)
    assert not source.exists() and dest.stat().st_dev==row['device'] and dest.stat().st_ino==row['inode']
(owner/'recovery.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','preserved_by_rename':plan,'deleted_payloads':0,'enumerated_unstamped_scopes':sorted(found),'incomplete_unpack':'llvm'},indent=2)+'\n')
subprocess.run(['git','-C',str(tree),'merge','--ff-only','next'],check=True)
print('PASS preserved all interrupted scopes and advanced stopped checkout to committed repair',flush=True)

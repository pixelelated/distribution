import subprocess,os,json,tempfile,hashlib
from pathlib import Path
root=Path('/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346')
clone=Path('/workspace/tmp/m6-coordinator/t42-brief-proof-50os455x/clone')
helper=root/'docs/qa-logs/2026-11-02-m6-resume/t42-brief-inputs.py'
out=Path(tempfile.mkdtemp(prefix='t42-v2-guards-'))
base='b6332dbc13f5929f05ec5ba23c44285c5ee56b38'
def git(*a,data=None,env=None):
 return subprocess.check_output(['git','-C',str(clone),*a],input=data,env=env)
records=[]
for label,path in [('selector','tools/renovation-inventory'),('referent','projects/ROCKNIX/packages/apps/mangohud/patches/SM8750/0002-SM8750-Battery.patch')]:
 env=dict(os.environ,GIT_INDEX_FILE=str(out/(label+'.index')))
 git('read-tree',base,env=env)
 original=git('show',base+':'+path)
 blob=git('hash-object','-w','--stdin',data=original+b'\n# deliberate brief-guard fixture\n').decode().strip()
 mode=git('ls-tree',base,'--',path).decode().split()[0]
 git('update-index','--add','--cacheinfo',mode+','+blob+','+path,env=env)
 tree=git('write-tree',env=env).decode().strip()
 commit=git('-c','user.name=T42 proof fixture','-c','user.email=proof@example.invalid','commit-tree',tree,'-p',base,data=('T42 '+label+' guard fixture\n').encode()).decode().strip()
 r=subprocess.run(['python3',str(helper),'--repo',str(clone),'--ref',commit,'--out',str(out/label)],capture_output=True)
 (out/(label+'.out')).write_bytes(r.stdout+r.stderr)
 expected=b'selector/input bytes drift' if label=='selector' else b'referent bytes drift'
 assert r.returncode!=0 and expected in r.stderr,(label,r.returncode,r.stderr[-500:])
 records.append({'case':label,'commit':commit,'rc':r.returncode,'expected_failure':expected.decode(),'output_sha256':hashlib.sha256(r.stdout+r.stderr).hexdigest()})
r=subprocess.run(['python3',str(helper),'--repo',str(root),'--ref','HEAD','--out',str(out/'positive')],capture_output=True)
(out/'positive.out').write_bytes(r.stdout+r.stderr)
assert r.returncode==0,r.stderr
records.append({'case':'positive','rc':r.returncode,'summary':json.loads(r.stdout),'output_sha256':hashlib.sha256(r.stdout+r.stderr).hexdigest()})
(out/'results.json').write_text(json.dumps(records,indent=2)+'\n')
print(out)
print(json.dumps([{'case':r['case'],'rc':r['rc']} for r in records]))

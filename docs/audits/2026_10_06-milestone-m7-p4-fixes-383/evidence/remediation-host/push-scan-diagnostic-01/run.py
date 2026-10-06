from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent;root=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');assert Path.cwd()==root
(owner/'run.path').write_text(str(root/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');rc=1
try:
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h
 rev='cc058c962c629b460432ee7d96edba8b3c52970f..e98339387135678f7ec82a8f90bde9643d2e4cd0'
 cmds=[('names',['git','diff','--name-only','--no-renames','--diff-filter=AM',rev,'--','.',':!*.po',':!*.pot']),('patch',['git','log','-p','--src-prefix=a/','--dst-prefix=b/','--no-renames','--diff-merges=first-parent','--format=commit %h',rev,'--not','--remotes=origin','--','.',':!*.po',':!*.pot']),('messages',['git','log','--format=commit %h%n%B',rev,'--not','--remotes=origin'])]
 rows=[]
 for name,args in cmds:
  with (owner/(name+'.data')).open('wb') as output,(owner/'artifacts'/(name+'.stderr')).open('wb') as error:r=subprocess.run(args,stdout=output,stderr=error)
  row=dict(stage=name,rc=r.returncode,bytes=(owner/(name+'.data')).stat().st_size);rows.append(row);print(json.dumps(row),flush=True);assert r.returncode==0
 with (owner/'lines.data').open('wb') as output,(owner/'artifacts/lines.stderr').open('wb') as error:
  with (owner/'patch.data').open('rb') as source:r=subprocess.run(['bash','-c','. .githooks/guard-lib; guard_load pre-push || exit; guard_added_lines'],stdin=source,stdout=output,stderr=error)
 row=dict(stage='guard_added_lines',rc=r.returncode,bytes=(owner/'lines.data').stat().st_size);rows.append(row);print(json.dumps(row),flush=True)
 (owner/'artifacts/results.json').write_text(json.dumps(rows,indent=2)+'\n');assert r.returncode==0
 for f in ['names.data','patch.data','messages.data','lines.data']:(owner/f).unlink()
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

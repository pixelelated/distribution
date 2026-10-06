from pathlib import Path
import datetime,hashlib,json,os,subprocess
b=Path('/tmp/pixelelated-approved-cleanup-20261006');o=Path(__file__).parent;r=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement03')
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a],text=True).strip()
f=json.loads(Path('/tmp/pixelelated-approved-cleanup-03/completion.json').read_text());assert f['job_rc']==1
assert not Path('/proc',Path('/tmp/pixelelated-approved-cleanup-03/removal.pid').read_text().strip()).exists()
report=json.loads((b/'root-watch.jsonl').read_text().splitlines()[-1]);age=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(report['utc'])).total_seconds()
assert 0<=age<15 and report['effective_uid']==0 and not report['matches'] and not report['unreadable']
assert tree.exists() and not tree.is_symlink() and 'worktree '+str(tree)+'\n' not in git(r,'worktree','list','--porcelain')+'\n'
row=next(x for x in json.loads((r/'docs/qa-logs/2026-10-05-build-storage/custody-followup-20261006/tree-custody.json').read_text()) if x['tree']==str(tree))
assert git(r,'rev-parse',row['branch'])==row['head']
(o/'root-before.json').write_text(json.dumps(report,indent=2)+'\n')
subprocess.run([str(r/'tools/fork-worktree'),'repair',str(tree),row['head']],cwd=r,check=True)
subprocess.run(['git','-C',str(tree),'switch',row['branch']],check=True)
patch=r/'docs/qa-logs/2026-10-05-build-storage/custody-followup-20261006/m7-pixelelated-replacement03.patch'
assert hashlib.sha256(patch.read_bytes()).hexdigest()==row['tracked_diff_sha256']
subprocess.run(['git','-C',str(tree),'apply',str(patch)],check=True)
assert git(tree,'rev-parse','HEAD')==row['head'] and git(tree,'branch','--show-current')==row['branch']
assert hashlib.sha256(subprocess.check_output(['git','-C',str(tree),'diff','--binary'])).hexdigest()==row['tracked_diff_sha256']
assert subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True)==row['tracked_status']
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tree':str(tree),'head':row['head'],'branch':row['branch'],'tracked_diff_sha256':row['tracked_diff_sha256'],'registered':True,'purpose':'Restore metadata for the already-approved removal; removed build intermediates are not reconstructed','prior_failure_preserved':True}
(o/'repair-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

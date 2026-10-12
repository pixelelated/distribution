"""Exact first #493 Oct12 batch. Checks by default; deletion only with --apply."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib.util,json,os,subprocess,sys,fcntl
O=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('guards',O/'guards.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
PLAN=Path('/workspace/tmp/pixelelated-m7-retention-20261012-plan04/plan.json')
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
def custody(plan):
 for r in g.read(plan['source_inputs']['path']):
  if 'sha256' in r:g.same(r,True)
  else:
   g.require(git(r['path'],'rev-parse','HEAD')==r['git_head'],'source git changed')
   g.require(git(r['path'],'submodule','status','--recursive').splitlines()==r['submodules'],'source submodules changed')
   if r.get('extra_source'):
    e=r['extra_source'];g.require(git(e['path'],'rev-parse','HEAD')==e['head'] and not git(e['path'],'status','--porcelain'),'extra source changed')
 for r in plan['worktrees']:
  for key in ['source_inventory','records']:g.same(r[key],True)
  for f in g.read(r['records']['path']):g.require(g.sha(f['object'])==f['sha256'],'preserved object differs')
def validate(plan,owner):
 for r in plan['files']+plan['protected_firmware']:g.same(r,True)
 g.same(plan['retained_records'],True)
 for r in g.read(plan['retained_records']['path']):g.same(r,True)
 for r in plan['extractions']:
  g.require(g.sha(r['manifest'])==r['manifest_sha256'],'extraction manifest changed');g.check_tree(r['path'],g.read(r['manifest']))
 for r in plan['worktrees']:
  g.require(g.identity(r['path'])==r['root_identity'],'worktree root changed')
  g.require(git(r['path'],'rev-parse','HEAD')==r['head'],'worktree HEAD changed')
  g.require(git(r['path'],'branch','--show-current')==r['branch'],'worktree branch changed')
  diff=subprocess.check_output(['git','-C',r['path'],'diff','--binary','HEAD'])
  g.require(hashlib.sha256(diff).hexdigest()==r['tracked_diff_sha256'],'tracked diff changed')
  g.require(not git(r['path'],'ls-files','--others','--exclude-standard'),'unpreserved untracked worktree files')
 custody(plan)
 references=g.read(O/'classified-references.json');g.require(references['result']=='PASS','unclassified external dependencies')
 for r in references['links']:
  p=Path(r['source']);g.require(p.is_symlink() and os.readlink(p)==r['link'] and str(p.resolve())==r['target'],'external link changed')
  g.require(r['classification']=='COMPLETED_HISTORICAL_CONSUMER','live dependency')
  for pid in r['exited_pids']:g.require(not Path('/proc',str(pid)).exists(),'former consumer PID now present; reclassify')
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--apply',action='store_true');args=a.parse_args()
 lock=(O/'execution.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 g.require(not (O/'result.json').exists(),'owner already used; never replay')
 for p,h in g.read(O/'seal.json').items():g.require(g.sha(p)==h,'sealed input changed: '+p)
 plan=g.read(PLAN);targets=[r['path'] for kind in ['files','extractions','worktrees'] for r in plan[kind]]
 g.require(len(targets)==64 and len(set(targets))==64,'unexpected exact target count')
 for hold in plan['protected_firmware']:
  g.require(not any(g.within(hold['path'],t) for t in targets),'protected firmware selected')
 for r in plan['files']:
  g.require(r['identity']['links']==1,'unclassified payload hardlink')
  if 'chain' in r:g.require(not any(z.get('backing-filename') for z in r['chain']),'unclassified backing dependency')
 validate(plan,O)
 g.live_check(targets,O,'preflight')
 if not args.apply:
  print('PASS exact plan, preservation, root coverage and live dependencies; verify-only, no deletion',flush=True);return
 g.require(os.environ.get('RASTERATOPS_BUILD_RUN'),'watched owner required for apply')
 (O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
 before=g.available();journal=(O/'removed.jsonl').open('x')
 def done(kind,path):
  journal.write(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'kind':kind,'path':path})+'\n');journal.flush();os.fsync(journal.fileno());print('Removed',kind,path,flush=True)
 # No overlays/backing pairs in this batch; all selected disks are independent.
 for r in plan['files']:
  g.same(r);p=Path(r['path']);fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   s=os.stat(p.name,dir_fd=fd,follow_symlinks=False);g.require((s.st_dev,s.st_ino)==(r['identity']['device'],r['identity']['inode']),'payload replaced');os.unlink(p.name,dir_fd=fd)
  finally:os.close(fd)
  done('file',str(p))
 for r in plan['extractions']:
  g.live_check([r['path']],O,'extraction-'+Path(r['path']).parent.name);g.remove_tree(r['path'],g.read(r['manifest']));done('extraction',r['path'])
 for r in plan['worktrees']:
  g.live_check([r['path']],O,'tree-'+Path(r['path']).name)
  subprocess.run([str(g.REPO/'tools/fork-worktree'),'remove',r['path'],'--force'],check=True,cwd=g.REPO,stdin=subprocess.DEVNULL)
  done('worktree',r['path'])
 for t in targets:g.require(not os.path.lexists(t),'removed target remains')
 registered=git(g.REPO,'worktree','list','--porcelain');g.require(all('worktree '+r['path']+'\n' not in registered+'\n' for r in plan['worktrees']),'worktree remains registered')
 for r in plan['protected_firmware']+g.read(plan['retained_records']['path']):g.same(r,True)
 custody(plan)
 result={'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','targets_removed':len(targets),'available_before':before,'available_after':g.available(),'recovered_bytes':g.available()-before,'plan_sha256':g.sha(PLAN),'deletion_performed':True}
 g.write(O/'result.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
 rc=1
 try:main();rc=0
 finally:
  if os.environ.get('RASTERATOPS_BUILD_RUN'):
   (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
 sys.exit(rc)

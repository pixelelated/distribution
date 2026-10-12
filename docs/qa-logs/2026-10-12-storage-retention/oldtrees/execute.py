"""Exact #493 17-tree retirement. --verify never deletes; --apply needs fresh root proof."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,fcntl,hashlib,importlib.util,json,os,stat,subprocess,sys
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('guards',P/'guards.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
def ident(p):
 s=Path(p).lstat();return dict(device=s.st_dev,inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=s.st_mode,uid=s.st_uid,links=s.st_nlink)
def require(c,m):g.require(c,m)
def same_input(r,hashed=False):
 p=Path(r['path']);require(not p.is_symlink() and str(p.resolve())==str(p),'redirected independent input '+str(p));require(ident(p)==r['identity'],'input identity changed '+str(p))
 if hashed:require(g.sha(p)==r['sha256'] and ident(p)==r['identity'],'input hash changed '+str(p))
def frozen_tree(r):
 p=Path(r['path']);require(not p.is_symlink() and str(p.resolve())==str(p),'redirected worktree')
 require(ident(p)==r['root_identity'],'worktree identity changed '+str(p));require(git(p,'rev-parse','HEAD')==r['head'] and git(p,'branch','--show-current')==r['branch'],'worktree Git identity changed')
 diff=subprocess.check_output(['git','-C',str(p),'diff','--binary','HEAD']);require(hashlib.sha256(diff).hexdigest()==r['tracked_patch_sha256'],'tracked work changed')
 require(git(p,'ls-files','--others','--exclude-standard').splitlines()==r['untracked_preserved'],'unreviewed untracked work')
def source_git(r):
 p=Path(r['path']);require(not p.is_symlink() and str(p.resolve())==str(p),'redirected source cache');require(git(p,'rev-parse','HEAD')==r['head'],'source cache HEAD changed')
 if 'unmapped_gitlinks' in r:
  require(p.name=='daedalusx64-sa-f17e9ed86f3806fadeb69abd29c9526ab2d4bd1b','unclassified unmapped submodule')
  require([x for x in git(p,'ls-tree','-r','HEAD').splitlines() if x.startswith('160000 ')]==['160000 commit 175079bacd37fa2bde746163814846feb9b4bb13\tSaveStates'],'unmapped gitlink changed')
  require(not (p/'.gitmodules').exists() and (p/'SaveStates').is_dir() and not (p/'SaveStates').is_symlink() and not list((p/'SaveStates').iterdir()),'unmapped gitlink gained payload')
 else:require(git(p,'submodule','status','--recursive').splitlines()==r['submodules'],'source submodule changed')
def custody(plan,originals):
 count=0
 for r in g.read(plan['source_manifest']):
  if r['kind']=='file':same_input(r,True)
  else:source_git(r)
  count+=1
 print('PASS',count,'independent source inputs',flush=True)
 objects={}
 for t in plan['worktrees']:
  for key in ['records','special_inputs']:
   for r in g.read(t[key]):
    if originals:same_input(r)
    objects[r['object']]=r['sha256']
    if originals:require(Path(r['path']).stat().st_ino!=Path(r['object']).stat().st_ino,'custody shares original inode')
 for p,h in objects.items():require(g.sha(p)==h,'preserved object differs '+p)
 print('PASS',len(objects),'independent preserved objects',flush=True)
def dependencies(plan,before):
 refs=g.read(plan['dependencies']);require(refs['result']=='PASS_CLASSIFIED','unclassified dependencies')
 for owner,r in refs['owners'].items():
  for p,h in r['evidence'].items():require(g.sha(p)==h,'historical terminal evidence changed')
  require(all(not Path('/proc',str(p)).exists() for p in r['exited_pids']),'historical PID present; reclassify')
 for r in refs['links']:
  p=Path(r['source']);kind=r['classification']
  if kind=='CONSUMER_ALREADY_REMOVED_FIRST_BATCH':require(not os.path.lexists(p),'removed consumer reappeared')
  elif kind=='COMPLETED_HISTORICAL_CONSUMER':
   require(os.path.lexists(p)==r['exists'],'historical link presence changed')
   if r['exists']:require(p.is_symlink() and os.readlink(p)==r['link'],'historical reference changed')
  elif kind=='CURRENT_CACHE_CONTAINER_BIND':
   require(p.is_symlink() and os.readlink(p)==r['link'],'current cache link changed')
   target=Path(r['retained_host_target'])
   if r['identity'] is None:require(not target.exists(),'previously missing target changed')
   else:
    s=target.stat();actual=dict(device=s.st_dev,inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=s.st_mode);require(actual==r['identity'],'retained bind target changed')
  else:raise RuntimeError('unknown dependency disposition')
 print('PASS',len(refs['links']),'classified dependency leads',flush=True)
def manifests():
 for p,h in g.read(P/'manifest-seal.json').items():require(g.sha(p)==h,'sealed manifest changed '+p)
 for p,h in g.read(P/'code-seal.json').items():require(g.sha(p)==h,'sealed executor changed '+p)
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--owner',type=Path,required=True);mode=a.add_mutually_exclusive_group(required=True);mode.add_argument('--verify',action='store_true');mode.add_argument('--apply',action='store_true');args=a.parse_args();o=args.owner.resolve(strict=True)
 lock=(P/'execution.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 require(not (o/'result.json').exists(),'owner already used');require(os.environ.get('RASTERATOPS_BUILD_RUN'),'watched owner required')
 (o/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');manifests();plan=g.read(P/'plan.json');targets=[r['path'] for r in plan['worktrees']]
 require(len(targets)==len(set(targets))==17,'scope changed');require(plan['source_gaps']==[],'source gaps')
 for t in targets:
  require(t.startswith('/workspace/repos/rocknix.worktrees/'),'outside worktree namespace')
  require(not any(g.within(t,p) or g.within(p,t) for p in plan['protected_roots']),'protected root selected')
  require(not any(g.within(p['path'],t) for p in plan['protected_firmware']),'protected firmware selected')
 for r in plan['worktrees']:frozen_tree(r)
 for r in plan['protected_firmware']:g.same(r,True)
 custody(plan,True);dependencies(plan,True)
 if not args.apply:
  g.write(o/'result.json',{'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS_PREPARATION_ONLY_REQUIRES_FRESH_ROOT_DEPENDENCIES','trees':17,'gross_bytes':plan['gross_allocated_bytes'],'deletion_performed':False});print('PASS preparation only; privileged process proof still required',flush=True);return
 g.live_check(targets,o,'apply-preflight');before=g.available();journal=(o/'removed.jsonl').open('x')
 for r in plan['worktrees']:
  frozen_tree(r);g.live_check([r['path']],o,'tree-'+Path(r['path']).name)
  subprocess.run([str(g.REPO/'tools/fork-worktree'),'remove',r['path'],'--force'],check=True,cwd=g.REPO,stdin=subprocess.DEVNULL)
  require(not os.path.lexists(r['path']),'removed target remains')
  journal.write(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'path':r['path'],'head':r['head'],'branch_preserved':r['branch']})+'\n');journal.flush();os.fsync(journal.fileno());print('REMOVED',r['path'],flush=True)
 registered=git(g.REPO,'worktree','list','--porcelain')
 for r in plan['worktrees']:
  require('worktree '+r['path']+'\n' not in registered+'\n','worktree still registered');require(git(g.REPO,'rev-parse',r['branch'])==r['head'],'source branch not preserved')
 for p in plan['protected_roots']:require(Path(p).is_dir(),'protected root missing')
 for r in plan['protected_firmware']:g.same(r,True)
 custody(plan,False);dependencies(plan,False);manifests();after=g.available()
 g.write(o/'result.json',{'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','trees_removed':17,'available_before':before,'available_after':after,'recovered_bytes':after-before,'gross_planned_bytes':plan['gross_allocated_bytes'],'source_branches_preserved':True,'custody_and_current_caches_verified_after':True,'deletion_performed':True});print('PASS removal and retained inputs; recovered bytes',after-before,flush=True)
if __name__=='__main__':
 rc=1
 try:main();rc=0
 finally:
  if '--owner' in sys.argv:
   o=Path(sys.argv[sys.argv.index('--owner')+1]);(o/'inner.rc').write_text(str(rc)+'\n');(o/'outer.rc').write_text(str(rc)+'\n')
 sys.exit(rc)

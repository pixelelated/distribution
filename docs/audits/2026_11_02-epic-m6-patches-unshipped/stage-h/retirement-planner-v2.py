#!/usr/bin/env python3
"""Retire only named T43 projections after committed custody and fresh checks."""
import datetime,hashlib,json,os,pathlib,stat,sys
R=pathlib.Path(__file__).resolve().parents[1];BASE=pathlib.Path('/workspace/tmp/m6-t43')
FLAGS=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads((R/p).read_text())
def canonical(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':')).encode())
def meta(s):return {'dev':s.st_dev,'ino':s.st_ino,'mode':stat.S_IMODE(s.st_mode),'uid':s.st_uid,'gid':s.st_gid,'size':s.st_size,'mtime_ns':s.st_mtime_ns,'ctime_ns':s.st_ctime_ns,'kind':'dir' if stat.S_ISDIR(s.st_mode) else 'file'}
def basefd():
 fd=os.open('/',FLAGS)
 try:
  for part in BASE.parts[1:]:
   nxt=os.open(part,FLAGS,dir_fd=fd);os.close(fd);fd=nxt
  return fd
 except:os.close(fd);raise
def permitted(root,allowed):
 p=pathlib.Path(root)
 assert p.parent==BASE and str(p) in allowed,'unknown or unconfined path'
 assert p.name not in {'stage-d-publication','eh-publication'} and 'cache' not in p.name and 'receipt' not in p.name,'cache/receipt path protected'
import importlib.util
_spec=importlib.util.spec_from_file_location('own_scope',R/'tools/retirement-owner-scope.py');OWN=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(OWN)
def completed(name):
 x=load(name);assert 'finished' in x and isinstance(x.get('exit'),int),'missing own producer receipt'
 children=[]
 if name=='stage-f/retirement-controls-v2-run.json':
  proof=load('stage-f/retirement-controls-v2.json');children=proof['known_children']
  assert children and all(c['joined'] and c['exit']==0 and c['finished'] for c in children),'unaccounted F control child'
 return {'receipt':name,'sha256':sha((R/name).read_bytes()),'argv':x['argv'],'cwd':x['cwd'],'started':x.get('started'),'finished':x['finished'],'exit':x['exit'],'termination':'returned','pid_recorded':False,'accounted_known_children':children,'child_accounting':'synchronous source/control implementation; no persistent child or handoff'}
def producer_for(evidence):
 if 'partial-failure-control-v2' in evidence:return 'stage-b/partial-control-v2-run.json'
 if 'partial-failure-control.json' in evidence:return 'stage-b/partial-control-run.json'
 if 'application-overlay/' in evidence:return 'stage-b/application-overlay-run.json'
 return 'stage-b/application-run.json'
def owner_evidence(root,value):
 return OWN.assess(root,completed(value['producer']),[OWN.observer()])
def inspect(root,expected,allowed,prior=None,owner_uid=None,device=None,keep=False,live=None):
 permitted(root,allowed)
 assert not [x for x in (live or []) if x['root']==root],'live owner reference'
 bfd=basefd();fd=None
 try:
  fd=os.open(pathlib.Path(root).name,FLAGS,dir_fd=bfd);rs=os.fstat(fd);dev=os.fstat(bfd).st_dev if device is None else device;uid=os.getuid() if owner_uid is None else owner_uid
  assert rs.st_dev==dev,'mount crossing'
  nodes={};snapshot={};dirs=set()
  def walk(cur,rel):
   ds=os.fstat(cur);assert ds.st_dev==dev,'mount crossing';assert ds.st_uid==uid,'owner mismatch';nodes[rel or '.']=meta(ds)
   for name in sorted(os.listdir(cur)):
    s=os.stat(name,dir_fd=cur,follow_symlinks=False);p=name if not rel else rel+'/'+name
    assert s.st_dev==dev,'mount crossing';assert s.st_uid==uid,'owner mismatch'
    if stat.S_ISDIR(s.st_mode):
     dirs.add(p);child=os.open(name,FLAGS,dir_fd=cur)
     try:assert (os.fstat(child).st_dev,os.fstat(child).st_ino)==(s.st_dev,s.st_ino),'identity changed while opening';walk(child,p)
     finally:os.close(child)
    else:
     assert stat.S_ISREG(s.st_mode),'symlink or special-file substitution'
     f=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=cur)
     try:
      before=os.fstat(f);assert meta(before)==meta(s),'identity changed while opening'
      h=hashlib.sha256();size=0
      while True:
       b=os.read(f,1024*1024)
       if not b:break
       size+=len(b);h.update(b)
      assert meta(os.fstat(f))==meta(before),'content changed while reading'
     finally:os.close(f)
     nodes[p]=meta(s);snapshot[p]={'type':'file','mode':oct(stat.S_IMODE(s.st_mode)),'sha256':h.hexdigest(),'bytes':size}
   assert meta(os.fstat(cur))==nodes[rel or '.'],'directory changed while reading'
  walk(fd,'')
  expected_dirs={str(parent) for name in expected for parent in pathlib.PurePosixPath(name).parents if str(parent)!='.'}
  assert dirs==expected_dirs,'unexpected or missing directory'
  assert snapshot==expected,'content snapshot mismatch'
  if prior is not None:assert nodes==prior,'fresh identity/metadata changed'
  result={'nodes':nodes,'content_snapshot_sha256':canonical(snapshot),'files':len(snapshot),'bytes':sum(x['bytes'] for x in snapshot.values())}
  if keep:result['_fd']=fd;result['_basefd']=bfd;fd=bfd=None
  return result
 finally:
  if fd is not None:os.close(fd)
  if bfd is not None:os.close(bfd)
def erase(root,inspection,empty_only=False):
 fd=inspection['_fd'];bfd=inspection['_basefd'];nodes=inspection['nodes']
 try:
  s=os.stat(pathlib.Path(root).name,dir_fd=bfd,follow_symlinks=False);assert meta(s)==nodes['.'],'root identity changed before deletion'
  if empty_only:
   assert os.listdir(fd)==[],'empty-prefix gained content'
  else:
   def walk(cur,rel):
    expected_names={p[len(rel)+1:] if rel else p for p in nodes if p!='.' and str(pathlib.PurePosixPath(p).parent)==(rel or '.')}
    assert set(os.listdir(cur))==expected_names,'directory membership changed before deletion'
    for name in sorted(expected_names):
     key=name if not rel else rel+'/'+name;s=os.stat(name,dir_fd=cur,follow_symlinks=False);assert meta(s)==nodes[key],'entry changed before deletion'
     if stat.S_ISDIR(s.st_mode):
      child=os.open(name,FLAGS,dir_fd=cur)
      try:
       assert (os.fstat(child).st_dev,os.fstat(child).st_ino)==(s.st_dev,s.st_ino),'directory identity changed'
       walk(child,key)
      finally:os.close(child)
      fresh=os.stat(name,dir_fd=cur,follow_symlinks=False);assert (fresh.st_dev,fresh.st_ino)==(s.st_dev,s.st_ino),'directory substituted'
      os.rmdir(name,dir_fd=cur)
     else:assert stat.S_ISREG(s.st_mode),'symlink substitution';os.unlink(name,dir_fd=cur)
   walk(fd,'')
  s=os.stat(pathlib.Path(root).name,dir_fd=bfd,follow_symlinks=False);assert (s.st_dev,s.st_ino)==(nodes['.']['dev'],nodes['.']['ino']),'root substituted'
  os.rmdir(pathlib.Path(root).name,dir_fd=bfd)
 finally:os.close(fd);os.close(bfd)
def expected_roots():
 out={}
 for root,v in load('stage-d/custody.json')['owned_receipt_bound_roots'].items():
  x=load(v['evidence']);expected=None
  if v['role']=='needed source members':expected=x['input_snapshot']
  elif v['role'] in ('normal candidate','successful prefix'):
   found=[z['candidate_snapshot'] for z in x.get('rows',[]) if z.get('candidate_root')==root]
   if found:expected=found[-1]
   elif x.get('final_prefix_root')==root:expected=x['final_prefix_snapshot']
  elif v['role']=='constructed guard fixture':
   expected={'prefix/'+p:t for p,t in x['prefix_after'].items()}
   if 'failed_candidate' in x:expected.update({'candidate/'+p:t for p,t in x['failed_candidate'].items()})
  assert expected is not None,root
  out[root]={'expected':expected,'evidence':v['evidence'],'custody_class':'D producer-bound path','producer':producer_for(v['evidence'])}
 for x in load('stage-d/prefix-custody.json')['records']:
  assert x['path'] not in out;x=dict(x)
  out[x['path']]={'expected':x['observed_snapshot'],'evidence':'stage-d/prefix-custody.json','custody_class':x['evidence_class'],'producer':producer_for(x['matches_recorded_input'])}
 for x in load('stage-d/empty-prefix-observation.json')['records']:
  out[x['path']]={'expected':{},'evidence':'stage-d/empty-prefix-observation.json','custody_class':'fresh current-state authorization only; no historical ownership recovery','empty_only':True,'producer':'stage-b/application-overlay-run.json'}
 for file,producer in [('retirement-control-custody.json','retirement-controls-run.json'),('retirement-control-custody-v2.json','retirement-controls-v2-run.json')]:
  extra=R/'stage-f'/file
  if extra.exists():
   x=json.loads(extra.read_text());out[x['root']]={'expected':x['final_snapshot'],'evidence':'stage-f/'+file,'custody_class':'new F control creation/current-content receipt','producer':'stage-f/'+producer}
 return out
def caches():
 out={}
 for p in load('stage-d/custody.json')['archive_hashes_after']:
  s=pathlib.Path(p).lstat();assert stat.S_ISREG(s.st_mode);out[p]=meta(s)
 return out
def producer_completion():
 names=['stage-b/application-run.json','stage-b/application-overlay-run.json','stage-b/partial-control-v2-run.json']
 out={}
 for name in names:
  x=load(name);assert x['exit']==0;out[name]={'exit':x['exit'],'finished':x.get('finished'),'sha256':sha((R/name).read_bytes())}
 return out
def plan():
 roots=expected_roots();result={'at':now(),'uid':os.getuid(),'authority':'#690 comments6590563116/6590591845/6590887584','producer_completion':producer_completion(),'process_scope':OWN.LIMIT,'global_no_reference_assertion':False,'cache_metadata_before':caches(),'roots':{},'preserved':['/workspace/cache/rocknix-sources','/workspace/tmp/m6-t43/stage-d-publication','/workspace/tmp/m6-t43/eh-publication']}
 for root,v in roots.items():
  try:
   owners=owner_evidence(root,v);x=inspect(root,v['expected'],roots)
   result['roots'][root]={**{k:z for k,z in v.items() if k!='expected'},**x,'owner_evidence':owners,'status':'eligible'}
  except (AssertionError,OSError) as e:result['roots'][root]={'status':'retained','reason':str(e),'evidence':v['evidence'],'producer':v['producer']}
 (R/'stage-h/retirement-plan.json').write_text(json.dumps(result,indent=2)+'\\n')
 print('H own-lane plan:',sum(x['status']=='eligible' for x in result['roots'].values()),'eligible;',sum(x['status']=='retained' for x in result['roots'].values()),'retained; no deletion; no global process assertion')
def retire():
 import subprocess
 path='docs/audits/2026_11_02-epic-m6-patches-unshipped/stage-h/retirement-plan.json'
 b=pathlib.Path(path).read_bytes();assert subprocess.check_output(['git','show','HEAD:'+path])==b,'cleanup plan must be committed'
 planned=json.loads(b);roots=expected_roots();results={'at':now(),'committed_plan_sha256':sha(b),'committed_at':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'process_scope':OWN.LIMIT,'global_no_reference_assertion':False,'roots':{}}
 for root,v in planned['roots'].items():
  if v['status']!='eligible':results['roots'][root]=v;continue
  try:
   owners=owner_evidence(root,roots[root]);x=inspect(root,roots[root]['expected'],roots,prior=v['nodes'],keep=True)
   erase(root,x,empty_only=v.get('empty_only',False))
   results['roots'][root]={'status':'retired','method':'nonrecursive rmdir' if v.get('empty_only') else 'fd-relative regular-file unlink and empty-directory rmdir','custody_class':v['custody_class'],'owner_evidence':owners,'files':v['files'],'bytes':v['bytes'],'finished':now()}
  except (AssertionError,OSError) as e:results['roots'][root]={'status':'retained-or-partial','reason':str(e),'custody_class':v['custody_class']}
  (R/'stage-h/retirement-result.json').write_text(json.dumps(results,indent=2)+'\n')
 results['cache_metadata_after']=caches();results['cache_metadata_equal']=results['cache_metadata_after']==planned['cache_metadata_before'];results['cache_evidence']='Fresh metadata comparison only. D retains21 historical before/after content-hash pairs; no new cache content hash and no cache mutation.'
 results['finished']=now();(R/'stage-h/retirement-result.json').write_text(json.dumps(results,indent=2)+'\n')
 print('H retirement:',sum(x['status']=='retired' for x in results['roots'].values()),'retired;',sum(x['status']!='retired' for x in results['roots'].values()),'retained/partial; cache metadata equal:',results['cache_metadata_equal'])
if __name__=='__main__':
 assert set(os.sched_getaffinity(0))<=set(range(8,24))
 (R/'stage-h').mkdir(exist_ok=True)
 if sys.argv[1]=='plan':plan()
 elif sys.argv[1]=='retire':retire()
 else:raise AssertionError('explicit plan/retire mode required')

"""D230 H-only retirement of receipt-bound T42 scratch. No caches or other lanes."""
import pathlib,subprocess,json,hashlib,datetime,os,re,shutil,tempfile,stat
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');REL='docs/audits/2026_11_02-epic-m6-patches-shipped';A=R/REL;H=A/'stage-h';S=pathlib.Path('/workspace/tmp/m6-t42');T=pathlib.Path('/tmp/m6-t42-inputs.8whm3634');D='d37670de318eb428604e4442f95defe10eade173';events=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(name,argv):
 q=subprocess.run(argv,cwd=R,capture_output=True);(H/(name+'.stdout')).write_bytes(q.stdout);(H/(name+'.stderr')).write_bytes(q.stderr);events.append({'name':name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'cwd':str(R),'rc':q.returncode,'stdout_sha256':sha(q.stdout),'stderr_sha256':sha(q.stderr)});dump(H/'cleanup-commands.json',events);return q

def no_owner(q):
 assert q.returncode in (0,1) and not q.stderr,'open-owner census incomplete'
 assert q.returncode==1 and not q.stdout,'live owner holds scratch'
def valid(p):
 assert p==T or p.parent==S,'outside exact owned scratch roots'
 assert p.is_dir() and not p.is_symlink() and p.resolve()==p,'scratch root is not a real confined directory'
 assert not os.path.ismount(p),'scratch root is a mount'
 assert p.stat().st_uid==os.getuid(),'scratch root owner differs'

def main():
 assert shutil.rmtree.avoids_symlink_attacks,'rmtree cannot confine symlinks'
 H.mkdir(exist_ok=True);assert not (H/'cleanup-result.json').exists(),'refuse repeated cleanup'
 assert S.is_dir() and not S.is_symlink() and T.is_dir() and not T.is_symlink()
 # The new F reader and its manifest must themselves be committed before retirement.
 p=A/'stage-f/accepted-manifest.json';q=run('committed-manifest',['git','show','HEAD:'+REL+'/stage-f/accepted-manifest.json']);assert q.returncode==0 and q.stdout==p.read_bytes()
 manifest=json.loads(p.read_text());assert manifest['accepted_D']==D
 for n in manifest['entries']:
  p=R/n['path'];b=os.readlink(p).encode() if p.is_symlink() else p.read_bytes();assert sha(b)==n['sha256'],'needed durable receipt changed'
 q=run('accepted-receipt-diff',['git','diff','--exit-code',D,'--',*[REL+'/'+x for x in ['stage-a','stage-b','stage-c','stage-d']]]);assert q.returncode==0
 # Map exact top-level roots back to durable, already accepted receipts.
 owned={};cache=set()
 for p in (A/'stage-b/application').glob('G*.json'):
  r=json.loads(p.read_text());candidate=S/r['group']
  if candidate.exists():assert r.get('archive_receipt') and any('normal' in n for n in r['rows']);owned[candidate]={'kind':'package-plan target projection','receipt':str(p.relative_to(A))}
 for p in (A/'stage-b/application').glob('archive-*.json'):
  r=json.loads(p.read_text());owned[pathlib.Path(r['base'])]={'kind':'safe cached-member projection','receipt':str(p.relative_to(A))};cache.add(r['path'])
 inherited=[]
 for p in (A/'stage-b/inherited-source').glob('*.json'):
  r=json.loads(p.read_text())
  if not isinstance(r,dict):continue
  if r.get('archive'):cache.add(r['archive'])
  if r.get('scratch') and pathlib.Path(r['scratch']).exists():inherited.append({'path':r['scratch'],'receipt':str(p.relative_to(A))})
 actual_inherited={str(p) for p in (S/'inherited-source').iterdir()};assert actual_inherited=={x['path'] for x in inherited},'unowned inherited scratch entry'
 owned[S/'inherited-source']={'kind':'inherited raw-source projections','children':inherited}
 fixtures={'runner-fixture':'stage-b/application/partial-failure-control.json','nested-patch':'stage-b/nested-patch/receipt.json','path-guard-fixture':'stage-c/protected-path-controls.json'}
 for name,receipt in fixtures.items():assert (A/receipt).is_file();owned[S/name]={'kind':'accepted synthetic proof fixture','receipt':receipt}
 assert set(S.iterdir())==set(owned),'unowned scratch root; stop before deletion'
 # Small text export is bound exactly to copied Stage A outputs; no glob over other /tmp lanes.
 tmpfiles=[]
 for p in sorted(T.rglob('*')):
  assert not p.is_symlink()
  if p.is_file():
   local=p.relative_to(T);target=A/'stage-a'/local;assert target.is_file() and p.read_bytes()==target.read_bytes(),'ephemeral input export lacks committed equivalent';tmpfiles.append({'path':str(p),'receipt':str(target.relative_to(A)),'sha256':sha(p.read_bytes())})
 owned[T]={'kind':'ephemeral small-text Stage A export','files':tmpfiles}
 # New cleanup guards fail on an outside path and a deliberately live text fixture.
 try:valid(pathlib.Path('/workspace/cache/rocknix-sources'))
 except AssertionError as e:assert str(e)=='outside exact owned scratch roots';outside=str(e)
 else:raise AssertionError('outside-path control passed')
 baseline=run('owner-census-baseline',['lsof','-nP','-Fpcn','+D',str(S)])
 excludes=sorted(set(re.findall(r"can't stat\(\) .*? file system (.+)",baseline.stderr.decode())))
 assert all(x.startswith(('/var/lib/docker/','/run/docker/','/run/snapd/ns')) for x in excludes),'unrecognized inaccessible filesystem'
 base=['lsof','-nP','-Fpcn']+sum((['-e',x] for x in excludes),[])
 fixture=pathlib.Path(tempfile.mkdtemp(prefix='m6-t42-cleanup-control-',dir='/tmp'));control=fixture/'open.txt';control.write_text('synthetic live-owner control\n')
 with control.open('rb') as handle:
  live=run('owner-control-live',base+['+D',str(fixture)])
  try:no_owner(live)
  except AssertionError as e:assert str(e)=='live owner holds scratch';live_error=str(e)
  else:raise AssertionError('live-owner control passed')
 closed=run('owner-control-closed',base+['+D',str(fixture)]);no_owner(closed);control.unlink();fixture.rmdir()
 dump(H/'cleanup-controls.json',{'outside_path':{'rejected':True,'assertion':outside},'live_owner':{'rejected':True,'assertion':live_error,'fixture':str(fixture)},'closed_owner':'actual lsof rc1, empty stdout/stderr; no open handle','excluded_filesystems':excludes,'exclusion_reason':'Inaccessible Docker/snap mount paths are outside both exact T42 scratch roots; baseline warning retained. No process arguments or file contents read by census.'})
 roots=[]
 for p,origin in sorted(owned.items(),key=lambda x:str(x[0])):
  valid(p);dev=p.stat().st_dev;files=links=bytes_=0
  for child in p.rglob('*'):
   st=child.lstat()
   if child.is_symlink():links+=1
   elif child.is_file():assert st.st_dev==dev;files+=1;bytes_+=st.st_size
   elif child.is_dir():assert st.st_dev==dev and not os.path.ismount(child),'mounted child in cleanup root'
   else:raise AssertionError('unsupported special file in scratch')
  roots.append({'path':str(p),'origin':origin,'files':files,'symlinks':links,'logical_file_bytes':bytes_,'device':dev,'inode':p.stat().st_ino})
 cache_before={p:{'inode':pathlib.Path(p).stat().st_ino,'bytes':pathlib.Path(p).stat().st_size,'mtime_ns':pathlib.Path(p).stat().st_mtime_ns} for p in sorted(cache)}
 dump(H/'cleanup-manifest.json',{'accepted_D':D,'needed_receipts_committed_at':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'accepted_manifest_sha256':sha((A/'stage-f/accepted-manifest.json').read_bytes()),'roots':roots,'cache_preserved_metadata':cache_before,'scope':'Only these exact receipt-bound roots; no cache, worktree, external final-publication directory or another lane path is a deletion target.'})
 for name,p in [('owned-source',S),('owned-text-export',T)]:no_owner(run('pre-delete-'+name,base+['+D',str(p)]))
 # Check inode/owner again immediately before each confined deletion. No broad rm/glob.
 removed=[]
 for root in roots:
  p=pathlib.Path(root['path']);valid(p);assert p.stat().st_ino==root['inode'] and p.stat().st_dev==root['device'];shutil.rmtree(p);assert not p.exists();removed.append(str(p))
 assert not list(S.iterdir()) and not T.exists()
 cache_after={p:{'inode':pathlib.Path(p).stat().st_ino,'bytes':pathlib.Path(p).stat().st_size,'mtime_ns':pathlib.Path(p).stat().st_mtime_ns} for p in sorted(cache)};assert cache_before==cache_after,'cache metadata changed'
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'removed_roots':removed,'root_count':len(removed),'logical_file_bytes_retired':sum(r['logical_file_bytes'] for r in roots),'retained_empty_root':str(S),'cache_archive_count_untouched':len(cache),'no_live_owner':'two immediate pre-delete bounded lsof checks rc1 with empty stdout/stderr after explicit unrelated-mount exclusions; live-owner negative control rejects','producer_replays':0,'source_extractions':0,'source_applications':0,'remaining_runtime_held':False,'external_publication_receipts':'separate lane-owned directory outside /workspace/tmp/m6-t42; final handback supplies exact path/hash'};dump(H/'cleanup-result.json',result)
 print('PASS H cleanup:',len(removed),'exact owned roots;',result['logical_file_bytes_retired'],'logical bytes;',len(cache),'cache archives preserved')
if __name__=='__main__':main()

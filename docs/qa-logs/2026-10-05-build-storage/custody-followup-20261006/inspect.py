from pathlib import Path
import os,json,subprocess,hashlib,datetime,time
out=Path(__file__).parent; trees=[Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n) for n in ['03','05','06','07','08']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,j):(out/n).write_text(json.dumps(j,indent=2)+'\n')
def call(args):return subprocess.check_output(args,text=True)
rows=[]
leads=json.loads(Path('/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-05-build-storage/custody-leads/receipt.json').read_text())
for tree in trees:
 head=call(['git','-C',str(tree),'rev-parse','HEAD']).strip();branch=call(['git','-C',str(tree),'branch','--show-current']).strip();status=call(['git','-C',str(tree),'status','--porcelain']);diff=subprocess.check_output(['git','-C',str(tree),'diff','--binary']);(out/(tree.name+'.patch')).write_bytes(diff)
 lead=next(r for r in leads['records'] if r['tree']==str(tree));assert head==lead['head']
 bundles=[]
 for b in lead['bundles']:
  p=Path(b['bundle']);raw=(p/'manifest.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==p.name
  j=json.loads(raw);assert j['inputs']['distribution_commit']==head
  bundles.append({'path':str(p),'manifest_sha256':p.name,'files':j['files'],'scope':'manifest digest verified now; payload reverified in retained custody-leads receipt'})
 symlinks=[]
 for p in tree.iterdir():
  if p.is_symlink():symlinks.append({'path':str(p),'target':os.readlink(p)})
 rows.append({'tree':str(tree),'head':head,'branch':branch,'tracked_status':status,'tracked_diff_sha256':hashlib.sha256(diff).hexdigest(),'diff_file':tree.name+'.patch','retained_bundles':bundles,'top_level_symlinks':symlinks,'deletion_authorized':False})
 print('Recorded source/branch/tracked diff/candidate custody',tree.name,flush=True)
save('tree-custody.json',rows)
# Inspect existing QA/archive locations. Build package directories are explicitly
# excluded: this is a QA-disk inventory, not a claim about arbitrary hidden files.
roots=[Path('/workspace/tmp'),Path('/workspace/artifacts'),Path('/workspace/repos/rocknix.worktrees')]
disks=[];errors=[];pruned=[];count=0;last=time.monotonic()
for root in roots:
 for base,dirs,files in os.walk(root,followlinks=False,onerror=lambda e:errors.append(str(e))):
  keep=[]
  for d in dirs:
   p=Path(base)/d
   if d in ['.git','node_modules','__pycache__'] or d.startswith('build.'):
    pruned.append(str(p))
   else:keep.append(d)
  dirs[:]=keep
  for n in files:
   if n.endswith('.qcow2'):disks.append(Path(base)/n)
  count+=1
  if time.monotonic()-last>10:print('QA disk discovery directories',count,'disks',len(disks),flush=True);last=time.monotonic()
save('discovery-scope.json',{'roots':list(map(str,roots)),'pruned':pruned,'directories':count,'disks':list(map(str,disks)),'errors':errors,'limitation':'Excluded package build roots, git metadata and node_modules; no whole-host arbitrary-file absence claim'})
chains=[]
for i,p in enumerate(disks):
 r=subprocess.run(['qemu-img','info','--force-share','--backing-chain','--output=json',str(p)],capture_output=True,text=True,timeout=30)
 row={'path':str(p),'rc':r.returncode}
 if r.returncode:row['error']=r.stderr.strip()
 else:
  j=json.loads(r.stdout);row['chain']=j
  row['references_proposed_tree']=any(any(str(v).startswith(str(t)+'/') for t in trees) for x in j for k,v in x.items() if k in ['filename','full-backing-filename','backing-filename'])
 chains.append(row)
 if i%20==0:print('Backing chains inspected',i+1,'of',len(disks),flush=True)
save('backing-chains.json',chains)
# Only record matches; do not dump process arguments or environments.
process_matches=[];proc_errors=[]
for p in Path('/proc').glob('[0-9]*'):
 try:
  candidates=[('cwd',os.readlink(p/'cwd'))]+[('argument',os.fsdecode(x)) for x in (p/'cmdline').read_bytes().split(b'\0') if x]
  for fd in (p/'fd').iterdir():
   try:candidates.append(('fd',os.readlink(fd)))
   except (FileNotFoundError,ProcessLookupError):pass
  hits=[{'kind':k,'tree':str(t)} for k,v in candidates for t in trees if v.startswith(str(t)+'/') or v==str(t)]
  if hits:process_matches.append({'pid':int(p.name),'matches':hits})
 except (FileNotFoundError,ProcessLookupError):continue
 except PermissionError:proc_errors.append({'pid':int(p.name),'error':'permission denied; process references unverified'})
containers=[]
for cid in call(['docker','ps','-q']).split():
 d=json.loads(call(['docker','inspect',cid]))[0];hits=[{'source':m['Source'],'destination':m['Destination']} for m in d['Mounts'] if any(m['Source'].startswith(str(t)) for t in trees)]
 if hits:containers.append({'id':d['Id'],'matching_mounts':hits})
save('live-dependencies.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'matches':process_matches,'unreadable_processes':proc_errors,'container_matches':containers})
save('summary.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trees':len(rows),'qa_disks':len(disks),'backing_errors':sum(x['rc']!=0 for x in chains),'proposed_tree_backing_references':sum(x.get('references_proposed_tree',False) for x in chains),'process_matches':len(process_matches),'unreadable_processes':len(proc_errors),'container_matches':len(containers),'scope_complete':False,'removal_ready':False,'deletion_performed':False,'remaining':'Full excluded-root dependency review, required source/licence/debug and failed-log preservation with hash receipts, net recovery and exact removal commands'})
print('PASS bounded custody inspection complete; preservation/removal plan remains incomplete',flush=True)

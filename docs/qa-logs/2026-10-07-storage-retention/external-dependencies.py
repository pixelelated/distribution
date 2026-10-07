from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for p,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
 prefixes=('/workspace/tmp/','/workspace/artifacts/rocknix-images/')
 roots=[Path('/workspace/repos'),Path('/workspace/cache'),Path('/workspace/artifacts'),Path('/home/max/Development')]
 links=[];references=[];errors=[];directories=0;manifests=0;tick=time.monotonic()
 def strings(v,key=()):
  if isinstance(v,str):yield key,v
  elif isinstance(v,list):
   for i,x in enumerate(v):yield from strings(x,key+(i,))
  elif isinstance(v,dict):
   for k,x in v.items():
    yield key+('<key>',),k
    yield from strings(x,key+(k,))
 for root in roots:
  if not root.exists():continue
  pending=[root]
  while pending:
   p=pending.pop();directories+=1
   try:
    with os.scandir(p) as entries:
     for e in entries:
      try:
       if e.is_symlink():
        # Absolute resolved destinations matter, including relative symlinks.
        target=os.path.realpath(e.path)
        if target.startswith(prefixes):links.append({'source':e.path,'target':target})
       elif e.is_dir(follow_symlinks=False):pending.append(Path(e.path))
       elif e.is_file(follow_symlinks=False) and e.name.endswith('.json') and e.path.startswith('/workspace/artifacts/'):
        data=json.loads(Path(e.path).read_text());manifests+=1
        for key,value in strings(data):
         if value.startswith(prefixes):references.append({'manifest':e.path,'key':key,'value':value})
      except (OSError,ValueError,RuntimeError) as error:errors.append({'path':e.path,'error':str(error)})
   except OSError as error:errors.append({'path':str(p),'error':str(error)})
   if time.monotonic()-tick>10:print(f'Scanned {directories} directories, {manifests} artifact manifests, {len(links)} external symlinks, {len(errors)} errors',flush=True);tick=time.monotonic()
 mounts=[]
 for cid in subprocess.check_output(['docker','ps','-aq'],text=True).split():
  d=json.loads(subprocess.check_output(['docker','inspect',cid],text=True))[0]
  for m in d['Mounts']:
   if m['Source'].startswith('/workspace/') or m['Source']=='/workspace':mounts.append({'container':cid,'running':d['State']['Running'],'source':m['Source']})
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'directories':directories,'artifact_manifests':manifests,'external_symlinks':links,'artifact_path_references':references,'container_mounts':mounts,'errors':errors,'scope':'Read-only external reference discovery for runtime payload review. Classify provenance versus live dependencies; no deletion eligibility claimed.'}
 f=owner/'artifacts/result.json';f.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'directories':directories,'external_symlinks':len(links),'artifact_references':len(references),'errors':len(errors),'report_sha256':hashlib.sha256(f.read_bytes()).hexdigest()}),flush=True)
 assert not errors,errors[:5]
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

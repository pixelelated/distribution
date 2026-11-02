"""Source-only patch stack proof. No recipe evaluation, fetch, build or runtime."""
import pathlib,subprocess,json,hashlib,datetime,time,re,tarfile,shutil,posixpath,os,collections
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';B=A/'stage-b';O=B/'application';S=pathlib.Path('/workspace/tmp/m6-t42');SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
ENV={**os.environ,'LC_ALL':'C','LANG':'C'}
def sha(b):return hashlib.sha256(b).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(p,o):p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def blob(p):return subprocess.check_output(['git','-C',str(R),'show',SEED+':'+p])
def snapshot(d):
 rows=[]
 for p in sorted(d.rglob('*')):
  assert not p.is_symlink()
  if p.is_file():rows.append({'path':str(p.relative_to(d)),'sha256':fsha(p),'mode':oct(p.stat().st_mode&0o777)})
 return {'files':rows,'sha256':sha(json.dumps(rows,sort_keys=True).encode())}
def command(argv,cwd,data,out):
 started=now();tick=time.monotonic();p=subprocess.run(argv,cwd=cwd,input=data,capture_output=True,env=ENV,timeout=90)
 out.with_suffix('.stdout').write_bytes(p.stdout);out.with_suffix('.stderr').write_bytes(p.stderr)
 return dict(argv=argv,cwd=str(cwd),utc=started,elapsed_s=time.monotonic()-tick,locale='C',rc=p.returncode,stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr),stdout=str(out.with_suffix('.stdout').relative_to(A)),stderr=str(out.with_suffix('.stderr').relative_to(A)))
def safe_rel(p):
 q=pathlib.PurePosixPath(p)
 if q.is_absolute() or '..' in q.parts:raise ValueError('unsafe member/path '+p)
 return str(q)
def touched(data):
 out=set()
 for l in data.decode().splitlines():
  if l.startswith(('--- ','+++ ','*** ')):
   raw=l[4:].split()[0]
   if raw=='/dev/null' or raw[0].isdigit():continue
   safe_rel(raw)
   if '/' not in raw:raise ValueError('patch -p1 target lacks leading component '+raw)
   out.add(safe_rel(raw.split('/',1)[1]))
 if not out:raise ValueError('no parsed patch targets; needs contextual review')
 return out
def trial(prefix,data,outdir,idx):
 before=snapshot(prefix);diag=outdir/('diagnostic-'+str(idx));candidate=outdir/('candidate-'+str(idx));shutil.copytree(prefix,diag);shutil.copytree(prefix,candidate)
 # Full normal execution, including all hunks after a partial failure.
 d=command(['patch','--dry-run','-p1','-N','--batch'],diag,data,O/(outdir.name+'-'+str(idx)+'-diagnostic'))
 n=command(['patch','-p1','-N','--batch'],candidate,data,O/(outdir.name+'-'+str(idx)+'-normal'))
 after=snapshot(candidate);promoted=n['rc']==0
 if promoted:
  old=outdir/('prefix-before-'+str(idx));prefix.rename(old);candidate.rename(prefix)
 assert snapshot(prefix)['sha256']==(after['sha256'] if promoted else before['sha256'])
 txt=(A/n['stdout']).read_text()+(A/n['stderr']).read_text()
 status='fails' if not promoted else 'fuzz' if re.search(r'with fuzz',txt) else 'offset' if re.search(r'offset [+-]?\d+ lines?',txt) else 'applies'
 return dict(before=before,after=after,promoted=promoted,diagnostic=d,normal=n,status=status,patch_sha256=sha(data))
O.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
assert not (S/'runner-fixture').exists(),'refuse replay/overwrite prior run'
fixture=S/'runner-fixture';fixture.mkdir();prefix=fixture/'prefix';prefix.mkdir();(prefix/'one').write_text('old\n');(prefix/'two').write_text('present\n')
bad=b'--- a/one\n+++ b/one\n@@ -1 +1 @@\n-old\n+new\n--- a/two\n+++ b/two\n@@ -1 +1 @@\n-missing\n+changed\n'
probe=trial(prefix,bad,fixture,1)
assert probe['normal']['rc']!=0 and not probe['promoted'] and probe['after']['sha256']!=probe['before']['sha256'] and (prefix/'one').read_text()=='old\n'
probe['successor']={'status':'blocked','invoked':False,'reason':'failed predecessor is not promoted'}
dump(O/'partial-failure-control.json',probe);print('PASS partial-failure: candidate changed, prefix preserved, successor blocked',flush=True)
version=subprocess.check_output(['patch','--version'],env=ENV).decode().splitlines()[0]
groups=json.loads((B/'selection.json').read_text());outputs=[];archive_cache={};bases={}
for g in groups:
 rec={'group':g['id'],'recipe':g['recipe'],'plan':g['plan'],'utc':now(),'tool':version,'locale':'C','census':{'scope':'source-only; no build/guest/device/cloud/fetch/config sourcing','process_names':subprocess.check_output(['ps','-eo','pid,comm'],env=ENV).decode().splitlines()},'rows':[]}
 reasons=list(g['open_reasons']);inputs=g['metadata']['inputs'];body='\n'.join(blob(p).decode() for p in inputs)
 if re.search(r'^\s*(?:pre_unpack)\s*\(\)|^\s*PKG_(?:SOURCE_DIR|TAR_STRIP_COMPONENTS)\s*=',body,re.M):reasons.append('nondefault extraction/pre_unpack requires explicit root proof')
 name=g['metadata']['values'].get('PKG_NAME'); vals=g['metadata']['values']
 if not reasons:
  try:
   archive=pathlib.Path(g['archives'][0]);side=pathlib.Path(str(archive)+'.sha256')
   if not side.is_file():raise ValueError('archive checksum sidecar missing: '+str(side))
   if not tarfile.is_tarfile(archive):raise ValueError('non-tar extraction backend not proved')
   if str(archive) not in archive_cache:
    digest=fsha(archive);sidebytes=side.read_bytes();assert digest==vals['PKG_SHA256'],'archive bytes differ from recipe SHA256';assert sidebytes.decode().strip().split()[0]==digest,'archive sidecar differs from bytes'
    with tarfile.open(archive) as tar:
     members=tar.getmembers();names=[];roots=set();byname={}
     for m in members:
      clean=safe_rel(m.name);parts=pathlib.PurePosixPath(clean).parts
      if not parts:continue
      roots.add(parts[0]);names.append(dict(name=m.name,type=m.type.decode(errors='replace'),link=m.linkname,size=m.size))
      if m.issym() or m.islnk():
       target=posixpath.normpath(posixpath.join(posixpath.dirname(clean),m.linkname)) if m.issym() else posixpath.normpath(m.linkname)
       if m.linkname.startswith('/') or target.startswith('../') or target.split('/')[0]!=parts[0]:raise ValueError('escaping archive link '+m.name)
      if len(parts)>1:
       rel='/'.join(parts[1:])
       if rel in byname and not m.isdir():raise ValueError('duplicate archive member '+rel)
       byname[rel]=m
     if len(roots)!=1:raise ValueError('archive has no unique strip-one root')
     # Only target union needed by this package's selected stacks, plus explicit inherited context.
     needs=set()
     for peer in groups:
      if peer['recipe']==g['recipe']:
       for item in peer['stack']:needs|=touched(blob(item['referent']))
     for inher in json.loads((B/'inherited-inputs.json').read_text()):
      if inher['recipe']==g['recipe']:
       try:needs|=touched(inher['patch_text'].encode())
       except ValueError:pass
     base=S/('archive-'+digest[:16]);base.mkdir(exist_ok=False);extracted=[];missing=[]
     for rel in sorted(needs):
      m=byname.get(rel)
      if m is None:missing.append(rel);continue
      if not m.isfile():raise ValueError('needed member not regular '+rel)
      data=tar.extractfile(m).read();dest=base/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);dest.chmod(0o644|(m.mode&0o111));extracted.append({'path':rel,'member':m.name,'sha256':sha(data),'bytes':len(data)})
     arc=dict(path=str(archive),sha256=digest,recipe_sha256=vals['PKG_SHA256'],sidecar_sha256=sha(sidebytes),member_manifest_sha256=sha(json.dumps(names,sort_keys=True).encode()),member_count=len(members),root=next(iter(roots)),extracted=extracted,missing=missing,base=str(base),source_tree=snapshot(base))
     archive_cache[str(archive)]=arc;dump(O/('archive-'+digest[:16]+'.json'),arc)
   arc=archive_cache[str(archive)];rec['archive_receipt']='stage-b/application/archive-'+arc['sha256'][:16]+'.json';rec['archive_sha256']=arc['sha256']
   # The build copies recipe sources before patches. A touched overlay member needs explicit proof.
   targets=set()
   for item in g['stack']:targets|=touched(blob(item['referent']))
   overlays=[]
   for inp in inputs:
    src=inp.rsplit('/',1)[0]+'/sources/'
    for rel in targets:
     probe=subprocess.run(['git','cat-file','-e',SEED+':'+src+rel],cwd=R,capture_output=True)
     if probe.returncode==0:overlays.append(src+rel)
   if overlays:raise ValueError('touched pre-patch source overlay needs composed input proof: '+', '.join(overlays))
   gd=S/g['id'];gd.mkdir();prefix=gd/'prefix';shutil.copytree(arc['base'],prefix);blocked=False
   for order,item in enumerate(g['stack'],1):
    literal=blob(item['referent']);r=dict(order=order,path=item['path'],referent=item['referent'],literal_sha256=sha(literal),device=g['device'],target_cpu='unused: no @TARGET_CPU@ token' if b'@TARGET_CPU@' not in literal else 'unknown',backend='patch')
    if blocked:r.update(status='blocked',reason='preceding candidate not promoted',invoked=False)
    elif re.search(rb'^GIT binary patch$|^rename from|^rename to',literal,re.M):r.update(status='open-item',reason='context git-apply backend not admitted by ordinary runner',invoked=False);blocked=True
    elif b'@TARGET_CPU@' in literal:r.update(status='open-item',reason='TARGET_CPU static value not established',invoked=False);blocked=True
    else:
     data=literal.replace(b'@DEVICE@',g['device'].encode());r['rendered_sha256']=sha(data);r.update(trial(prefix,data,gd,order));r['invoked']=True
     if not r['promoted']:blocked=True
    rec['rows'].append(r)
  except (ValueError,AssertionError,tarfile.TarError,UnicodeError) as e:reasons.append(str(e))
 rec['open_reasons']=reasons
 if reasons and not rec['rows']:rec['rows']=[dict(path=p,status='open-item',reason='; '.join(reasons),invoked=False) for p in g['native']]
 dump(O/(g['id']+'.json'),rec);outputs.append({'group':g['id'],'receipt':'stage-b/application/'+g['id']+'.json','open_reasons':reasons,'statuses':dict(collections.Counter(x['status'] for x in rec['rows']))})
 print(g['id'],g['plan'],name,dict(collections.Counter(x['status'] for x in rec['rows'])),flush=True)
dump(O/'index.json',outputs);print('COMPLETE',len(outputs),dict(collections.Counter(s for x in outputs for s,count in x['statuses'].items() for _ in range(count))),flush=True)

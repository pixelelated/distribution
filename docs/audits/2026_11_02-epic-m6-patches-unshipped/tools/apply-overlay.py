#!/usr/bin/env python3
"""Bounded immutable-source application: exact hash, member projection, rc0 promotion."""
import collections,datetime,hashlib,json,os,pathlib,posixpath,re,shutil,subprocess,sys,tarfile,tempfile
R=pathlib.Path(__file__).resolve().parents[1];B=json.loads((R/'stage-a/bindings.json').read_text());S=B['source'];OUT=R/'stage-b/application-overlay';OUT.mkdir(exist_ok=True);SCR=pathlib.Path('/workspace/tmp/m6-t43');SCR.mkdir(exist_ok=True);assert set(os.sched_getaffinity(0))<=set(range(8,24))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def git(p):return subprocess.check_output(['git','show',S+':'+p])
def safe(p):
 q=pathlib.PurePosixPath(p);assert p and not q.is_absolute() and '..' not in q.parts and '\x00' not in p, 'unsafe relative path '+p
 return str(q)
def snapshot(d):
 result={}
 for p in sorted(d.rglob('*')):
  rel=str(p.relative_to(d))
  if p.is_symlink():
   target=os.readlink(p);resolved=posixpath.normpath(posixpath.join(posixpath.dirname(rel),target));safe(resolved);assert not target.startswith('/'),'absolute output symlink';result[rel]={'type':'link','target':target,'sha256':sha(target.encode())}
  elif p.is_file():result[rel]={'type':'file','mode':oct(p.stat().st_mode&0o777),'sha256':filehash(p),'bytes':p.stat().st_size}
 return result
def digest(s):return sha(json.dumps(s,sort_keys=True).encode())
def patchcall(candidate,data,stem):
 start=now();argv=['patch','-d',str(candidate),'-p1'];proc=subprocess.run(argv,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={'PATH':'/usr/bin:/bin','LC_ALL':'C','HOME':str(SCR)},timeout=60)
 (OUT/(stem+'.stdout')).write_bytes(proc.stdout);(OUT/(stem+'.stderr')).write_bytes(proc.stderr)
 return {'argv':argv,'start':start,'end':now(),'exit':proc.returncode,'stdout_sha256':sha(proc.stdout),'stderr_sha256':sha(proc.stderr),'output':proc.stdout.decode(errors='replace'),'error':proc.stderr.decode(errors='replace')}
def advance(state,data,stem):
 if state['blocked']:
  return {'status':'blocked','reason':state['blocked'],'normal_called':False}
 prefix=state['prefix'];candidate=pathlib.Path(tempfile.mkdtemp(prefix=stem+'-candidate-',dir=SCR));shutil.copytree(prefix,candidate,dirs_exist_ok=True);before=snapshot(prefix);r=patchcall(candidate,data,stem)
 # Preserve the actual command result before any post-call assertion can fail.
 save(OUT/(stem+'-call.json'),r)
 after=snapshot(candidate);row={'normal_called':True,'normal':r,'input_digest':digest(before),'output_digest':digest(after),'candidate_snapshot':after,'candidate_root':str(candidate)}
 if r['exit']==0:
  row['status']='fuzz' if 'fuzz' in r['output'] else ('offset' if 'offset' in r['output'] else 'applies');row['promoted']=True;state['prefix']=candidate
 else:
  row['status']='fails';row['promoted']=False;row['prefix_unchanged']=snapshot(prefix)==before;state['blocked']='normal failure at '+stem;assert row['prefix_unchanged']
 return row

def control():
 f=OUT/'fixtures';f.mkdir(exist_ok=True)
 before=b'one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\n';bad=b'--- a/a.txt\n+++ b/a.txt\n@@ -1 +1 @@\n-one\n+ONE\n@@ -7,2 +7,2 @@\n-not-seven\n+SEVEN\n eight\n';after=b'--- a/a.txt\n+++ b/a.txt\n@@ -1 +1 @@\n-ONE\n+SUCCESSOR\n'
 for n,b in [('input.txt',before),('partial.patch',bad),('successor.patch',after)]: (f/n).write_bytes(b)
 d=pathlib.Path(tempfile.mkdtemp(prefix='partial-control-',dir=SCR));prefix=d/'prefix';prefix.mkdir();(prefix/'a.txt').write_bytes(before);initial=snapshot(prefix);state={'prefix':prefix,'blocked':None};r=advance(state,bad,'partial-failure-v2');successor=advance(state,after,'partial-successor-v2')
 assert r['normal']['exit']!=0 and r['candidate_snapshot']!=initial and snapshot(prefix)==initial and state['prefix']==prefix and not r['promoted'] and not successor['normal_called']
 save(OUT/'partial-failure-control-v2.json',{'class':'constructed mechanism fixture using actual advance function','input_sha256':{p.name:filehash(p) for p in f.iterdir()},'receipt':r,'prefix_before':initial,'prefix_after':snapshot(prefix),'successor':successor,'projection_root':str(d),'exit':0})
 unsafe=[]
 for path in ['/etc/passwd','../escape','a/../../escape']:
  try:safe(path)
  except AssertionError as e:unsafe.append({'input':path,'refusal':str(e)})
 assert len(unsafe)==3;save(OUT/'path-safety-controls.json',unsafe)
 print('PASS partial-failure: candidate changed, prefix retained, successor calls 0',flush=True)
if '--control' in sys.argv:control();sys.exit(0)
assert (R/'stage-b/application/partial-failure-control-v2.json').exists(),'control required first'
plans=json.loads((R/'stage-b/plans-overlay.json').read_text());patchcache={};archive_hashes={};projection_cache={};summary=[]
version=subprocess.check_output(['patch','--version']).decode();save(OUT/'environment.json',{'version':version,'patch_binary_sha256':filehash('/usr/bin/patch'),'locale':'C','start':now(),'affinity':sorted(os.sched_getaffinity(0)),'producer_sha256':filehash(__file__),'plan_sha256':filehash(R/'stage-b/plans-overlay.json')})
def patchmeta(path,plan):
 if path not in patchcache:
  mode=subprocess.check_output(['git','ls-tree',S,'--',path]).decode().split()[0];literal=git(path);referent=path
  if mode=='120000':referent=safe(posixpath.normpath(posixpath.join(posixpath.dirname(path),literal.decode())));data=git(referent)
  else:data=literal
  patchcache[path]=(literal,data,referent,mode)
 literal,data,referent,mode=patchcache[path];render=data.replace(b'@TARGET_CPU@',plan['target_cpu'].encode()).replace(b'@DEVICE@',plan['device'].encode());targets=[]
 for l in render.decode(errors='replace').splitlines():
  if l.startswith(('--- ','+++ ')):
   raw=l[4:].split('\t')[0].split(' ')[0]
   if raw=='/dev/null':continue
   assert not raw.startswith('/') and '/' in raw,'unsupported target '+raw
   targets.append(safe(raw.split('/',1)[1]))
 assert targets,'no supported unified targets'
 binary=bool(re.search(br'^GIT binary patch$|^rename from|^rename to',data,re.M))
 return {'path':path,'referent':referent,'mode':mode,'literal_sha256':sha(literal),'content_sha256':sha(data),'rendered_sha256':sha(render),'targets':sorted(set(targets)),'backend':'git apply' if binary else 'patch','rendered':render}
for plan in plans:
 gid=plan['id'];report={'id':gid,'census':plan,'started':now(),'rows':[],'input_snapshot':{},'limits':plan['preimage_limits'].copy()};save(OUT/(gid+'-census.json'),report)
 if not plan['native_paths']:
  report['limits']+=['configuration-only plan: no patch application claim'];report['status']='config-source-only';save(OUT/(gid+'.json'),report);summary.append({'id':gid,'status':report['status'],'limits':report['limits']});continue
 if not plan['cache_candidates']:report['limits']+=['exact source archive absent from inspected package cache directory']
 qualified=[]
 for c in plan['cache_candidates']:
  if c not in archive_hashes:archive_hashes[c]=filehash(c)
  if archive_hashes[c]==plan['expected_sha256']:qualified.append(c)
 if plan['cache_candidates'] and not qualified:report['limits']+=['available candidate SHA256 does not match exact recipe input']
 report['cache_observations']=[{'path':c,'sha256':archive_hashes[c],'expected':plan['expected_sha256']} for c in plan['cache_candidates']]
 if len(qualified)>1:report['limits']+=['ambiguous multiple matching source archives']
 if report['limits']:
  report['status']='open-item';save(OUT/(gid+'.json'),report);summary.append({'id':gid,'status':'open-item','limits':report['limits']});continue
 archive=qualified[0];report['archive']={'path':archive,'sha256':archive_hashes[archive],'recipe_url':plan['url']};metas=[]
 try:
  metas=[patchmeta(p,plan) for p in plan['stack']];needed=sorted({t for m in metas for t in m['targets']});report['stack']=[{k:v for k,v in m.items() if k!='rendered'} for m in metas];report['stack_sha256']=sha(json.dumps(report['stack'],sort_keys=True).encode())
  key=(archive,tuple(needed))
  if key not in projection_cache:
   source=pathlib.Path(tempfile.mkdtemp(prefix='source-members-',dir=SCR));seen=set();found=set();roots=set();headers=[]
   with tarfile.open(archive,'r|*') as tar:
    for m in tar:
     name=safe(m.name);roots.add(name.split('/')[0]);assert len(roots)==1,'multiple archive roots'
     assert name not in seen,'duplicate archive member '+name;seen.add(name);headers.append([name,m.type.decode(errors='replace'),m.size,m.linkname])
     if m.issym() or m.islnk():
      target=posixpath.normpath(posixpath.join(posixpath.dirname(name),m.linkname)) if m.issym() else m.linkname;safe(target);assert target.split('/')[0]==name.split('/')[0],'escaping archive link'
     rel=name.split('/',1)[1] if '/' in name else ''
     if rel in needed:
      assert m.isfile(),'needed archive member is not regular '+rel
      dest=source/safe(rel);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(tar.extractfile(m).read());dest.chmod(m.mode&0o777);found.add(rel)
   projection_cache[key]=(source,{'archive_header_count':len(headers),'archive_header_sha256':sha(json.dumps(headers).encode()),'projected_members':snapshot(source),'absent_targets':sorted(set(needed)-found),'projection_root':str(source)})
  source,projection=projection_cache[key];report['projection']=projection;report['overlay_evidence']=[]
  # scripts/unpack:103-105 copies package sources/ before post_unpack/pre_patch.
  for item in plan['source_overlays']:
   data=git(item['path']);entry={**item,'sha256':sha(data),'projected':item['relative'] in needed};report['overlay_evidence'].append(entry)
   if entry['projected']:
    assert item['mode'] in ['100644','100755'],'needed overlay link requires separate qualification'
    dest=source/safe(item['relative']);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);dest.chmod(0o755 if item['mode']=='100755' else 0o644)
  report['input_snapshot']=snapshot(source);prefix=pathlib.Path(tempfile.mkdtemp(prefix=gid+'-prefix-',dir=SCR));shutil.copytree(source,prefix,dirs_exist_ok=True);state={'prefix':prefix,'blocked':None}
  for i,m in enumerate(metas):
   row={k:v for k,v in m.items() if k!='rendered'};row.update(index=i+1,native=m['path'] in plan['native_paths'])
   if state['blocked']:row.update(advance(state,m['rendered'],gid+'-'+str(i+1).zfill(3)));report['rows'].append(row);continue
   if m['backend']!='patch':state['blocked']='git-apply binary/rename semantics require unsupported safe-directory qualification';row.update(status='open-item',reason=state['blocked'],normal_called=False);report['rows'].append(row);continue
   row.update(advance(state,m['rendered'],gid+'-'+str(i+1).zfill(3)));report['rows'].append(row)
   save(OUT/(gid+'-progress.json'),report)
  report['status']='partial' if state['blocked'] else 'applies';report['final_prefix_root']=str(state['prefix']);report['final_prefix_snapshot']=snapshot(state['prefix'])
 except (AssertionError,tarfile.TarError,UnicodeError) as e:
  report['status']='open-item';report['limits'].append(str(e));report['rows']=report.get('rows',[])
 report['finished']=now();save(OUT/(gid+'.json'),report);summary.append({'id':gid,'status':report['status'],'limits':report['limits'],'native_results':dict(collections.Counter(r['status'] for r in report['rows'] if r['native']))});print(gid,plan['name'],plan['consumer'],report['status'],summary[-1].get('native_results',{}),report['limits'],flush=True)
save(OUT/'summary.json',{'finished':now(),'groups':summary,'archive_hashes':archive_hashes,'normal_calls':sum(sum(bool(r.get('normal_called')) for r in json.loads((OUT/(p['id']+'.json')).read_text()).get('rows',[])) for p in plans)});print('DONE',len(summary),flush=True)

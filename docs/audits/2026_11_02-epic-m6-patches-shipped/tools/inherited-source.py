"""Exact-pin cached-source comparisons, not application claims."""
import pathlib,json,subprocess,re,hashlib,tarfile,posixpath,datetime,ast,collections
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';B=A/'stage-b';O=B/'inherited-source';S=pathlib.Path('/workspace/tmp/m6-t42/inherited-source');SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
def blob(p):return git('show',SEED+':'+p)
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def safe(p):
 q=pathlib.PurePosixPath(p)
 if q.is_absolute() or '..' in q.parts:raise ValueError('unsafe path '+p)
 return str(q)
def targets(txt):
 out=set()
 for l in txt.splitlines():
  if l.startswith(('--- ','+++ ','*** ')):
   p=l[4:].split()[0]
   if p!='/dev/null' and '/' in p and not p[0].isdigit():out.add(safe(p.split('/',1)[1]))
 return out
tree=ast.parse((A/'tools/select.py').read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='meta');exec(compile(ast.Module(body=[node],type_ignores=[]),'select.py:meta','exec'),globals())
leads=json.loads((B/'inherited-inputs.json').read_text());O.mkdir(exist_ok=True);S.mkdir(exist_ok=True);results=[]
recipes=list(dict.fromkeys(x['recipe'] for x in leads));recipes.remove('projects/ROCKNIX/devices/H700/packages/u-boot/package.mk');recipes += ['projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/package.mk','projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/package.mk']
for rp in recipes:
 m=meta(rp,'H700' if 'u-boot-DDR' in rp else 'GENERIC_X64','aarch64' if 'u-boot-DDR' in rp else 'x86_64');v=m['values'];name=v['PKG_NAME'];pin=v['PKG_VERSION'];need=set()
 for x in leads:
  if x['recipe']==rp or ('u-boot-DDR' in rp and x['index']==1):need|=targets(x['patch_text'])
 # Closely connected source facts, not an exported source checkout.
 extra={'ffmpeg':['libpostproc/postprocess.c','libpostproc/Makefile','configure'],'libsndfile':['CMakeLists.txt'],'seatd':['seatd-launch/seatd-launch.c','meson.build'],'vulkan-tools':['CMakeLists.txt'],'fluidsynth':['CMakeLists.txt'],'glibc':['Makefile','Makerules','sysdeps/arm/Makefile','elf/dl-version.c','elf/dl-tls.c'],'mkbootimg':['mkbootimg.py'],'sway':['meson.build'],'mesa':['src/gallium/targets/dri/meson.build']}
 need.update(extra.get(name,[]));record={'recipe':rp,'recipe_sha256':sha(blob(rp)),'pin':pin,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'unmodified cached-source comparison, not stack application','requested':sorted(need)}
 try:
  cache=pathlib.Path('/workspace/cache/rocknix-sources')/name;candidates=[p for p in cache.glob('*') if p.is_file() and not p.name.endswith(('.url','.sha256')) and p.name.startswith(name+'-'+pin+'.')]
  if len(candidates)!=1:raise ValueError('exact cached archive missing or ambiguous: '+name+'-'+pin)
  arc=candidates[0];datahash=hashlib.file_digest(arc.open('rb'),'sha256').hexdigest();side=pathlib.Path(str(arc)+'.sha256');assert datahash==v.get('PKG_SHA256'),'recipe SHA256 mismatch/missing';assert side.read_text().strip().split()[0]==datahash,'sidecar mismatch'
  with tarfile.open(arc) as tar:
   ms=tar.getmembers();lookup={};roots=set();dups=[]
   for member in ms:
    clean=safe(member.name);parts=pathlib.PurePosixPath(clean).parts
    if not parts:continue
    roots.add(parts[0])
    if member.issym() or member.islnk():
     dest=posixpath.normpath(posixpath.join(posixpath.dirname(clean),member.linkname)) if member.issym() else posixpath.normpath(member.linkname)
     if member.linkname.startswith('/') or dest.startswith('../') or dest.split('/')[0]!=parts[0]:raise ValueError('escaping archive link '+member.name)
    if len(parts)>1:
     rel='/'.join(parts[1:])
     if rel in lookup and not member.isdir():dups.append(rel)
     lookup[rel]=member
   assert len(roots)==1,'no unique archive root'
   if dups:raise ValueError('duplicate archive members; first '+dups[0])
   dest=S/name;dest.mkdir(exist_ok=False);found=[];missing=[]
   for p in sorted(need):
    member=lookup.get(p)
    if not member:missing.append(p);continue
    if not member.isfile():raise ValueError('needed member not regular '+p)
    data=tar.extractfile(member).read();f=dest/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data);found.append({'path':p,'member':member.name,'sha256':sha(data),'bytes':len(data)})
   record.update(archive=str(arc),archive_sha256=datahash,sidecar_sha256=sha(side.read_bytes()),member_count=len(ms),root=next(iter(roots)),member_manifest_sha256=sha('\n'.join(x.name for x in ms).encode()),files=found,missing=missing,scratch=str(dest),status='qualified raw source')
 except (ValueError,AssertionError,tarfile.TarError,FileNotFoundError) as e:record.update(status='open-item',missing_input=str(e))
 dump(O/(name+'.json'),record);results.append(record);print(name,pin,record['status'],record.get('missing_input',''),flush=True)
dump(O/'index.json',results)

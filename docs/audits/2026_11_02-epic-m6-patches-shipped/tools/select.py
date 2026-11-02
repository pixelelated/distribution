"""Conservative static source/stack model. Never evaluates shell or configuration."""
import pathlib,json,re,subprocess,hashlib,fnmatch,posixpath,datetime,collections
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';B=A/'stage-b';SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
def blob(p,ref=SEED):return git('show',ref+':'+p)
def sha(x):return hashlib.sha256(x).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
T={}
for ent in git('ls-tree','-r','-z',SEED).split(b'\0'):
 if ent:
  m,p=ent.split(b'\t',1);mode,kind,oid=m.decode().split();T[p.decode()]={'mode':mode,'oid':oid}
native=json.loads((B/'native-inputs.json').read_text());recipes=json.loads((B/'recipes.json').read_text())
def resolve(p):
 for _ in range(10):
  found=False
  for i in range(1,len(p.split('/'))+1):
   pre='/'.join(p.split('/')[:i])
   if T.get(pre,{}).get('mode')=='120000':
    p=posixpath.normpath(posixpath.join(posixpath.dirname(pre),blob(pre).decode(),*p.split('/')[i:]));found=True;break
  if not found:return p
 raise ValueError('link loop')
def selected_recipe(n):
 ps=n['recipes'];local=[p for p in ps if p.startswith('projects/ROCKNIX/packages/')]
 return local[0] if len(local)==1 else ps[0] if len(ps)==1 else None
def meta(p,device,arch,seen=()):
 assert p not in seen
 txt=blob(p).decode(); vals={};inputs=[p];ambiguity=[]
 for line in txt.splitlines():
  inc=re.match(r'^\. \$\{ROOT\}/([^\s]+/package.mk)',line)
  if inc:
   old=meta(inc[1],device,arch,seen+(p,));vals.update(old['values']);inputs+=old['inputs'];ambiguity+=old['ambiguity']
  m=re.match(r'^\s*(PKG_(?:NAME|VERSION|SHA256|URL|SOURCE_NAME|SITE))="([^"\n]*)"',line)
  if m:vals[m[1]]=m[2]
 # Explicit source-read branches, not shell execution.
 name=vals.get('PKG_NAME',pathlib.PurePosixPath(p).parent.name)
 if name=='atf' and device=='H700':vals['PKG_VERSION']='2.12.0';vals.pop('PKG_SHA256',None)
 if name=='sway' and device=='RK3588':vals['PKG_VERSION']='1.9';vals.pop('PKG_SHA256',None)
 if '$(get_pkg_version vitaquake2-lr)'==vals.get('PKG_VERSION'):vals['PKG_VERSION']='59a511555106eef7156c1f34d1ee6c47d11cc4ee'
 for _ in range(5):
  for k,v in vals.items():
   for key,val in vals.copy().items():v=v.replace('${'+key+'}',val)
   vals[k]=v
 # Unsupported branching of input fields is never silently assumed.
 vers=re.findall(r'^\s*PKG_VERSION="([^"\n]*)"',txt,re.M)
 if len(set(vers))>1 and name not in ['moonlight','atf','sway']:ambiguity.append('conditional PKG_VERSION needs static branch proof')
 extras=[];unknown=[]
 if 'PKG_PATCH_DIRS' in txt:
  if name=='gamepadtester':extras=[device,'xbox' if device.startswith('SM8') else 'legacy']
  elif name=='mangohud':unknown=['BATTERYPLUS_SUPPORT branch must be established from layered configuration'];extras=['common']+(['qualcomm'] if device.startswith('SM') else [])+[device]
  elif name=='glibc':extras=['widevine-arm'] if arch in ['arm','aarch64'] else []
  elif name=='mupen64plus-lr':extras=[device]+(['AMD64'] if device=='GENERIC_X64' else [])
  elif name=='mednafen':extras=['sdl-input'] if device=='H700' or device.startswith('SM8') else []
  elif name=='ffmpeg':extras=['libreelec','v4l2-request','v4l2-drmprime']
  elif name in ['desmume-lr','amiberry','azahar-sa','gmu']:unknown=['graphics feature branch selecting PKG_PATCH_DIRS needs static layered configuration proof']
  elif name=='SDL3':extras=[] # RK-only later pre_configure patch loop; none of five plans is RK.
  elif all(re.fullmatch(r'PKG_PATCH_DIRS\+="\s*\$\{DEVICE\}"',l.strip()) for l in txt.splitlines() if 'PKG_PATCH_DIRS' in l):extras=[device]
  else:unknown=['unrecognized patch-directory assignment needs explicit source-read branch proof']
 hooks=[]
 for inp in inputs:
  body=blob(inp).decode()
  hooks += [f'{inp}:{m.start()+1}:{m.group(1)}' for m in re.finditer(r'^\s*(unpack|post_unpack|pre_patch)\s*\(\)',body,re.M)]
 return dict(values=vals,inputs=list(dict.fromkeys(inputs)),ambiguity=ambiguity,extras=extras,stack_unknown=unknown,hooks=hooks,recipe_sha256=sha(blob(p)))
def children(d):
 actual=resolve(d);prefix=actual+'/'
 return [d+'/'+p[len(prefix):] for p in sorted(T) if p.startswith(prefix) and '/' not in p[len(prefix):] and p.endswith('.patch')]
def stack(p,m,device,arch):
 d=p.rsplit('/',1)[0];name=m['values'].get('PKG_NAME',d.split('/')[-1]);v=m['values'].get('PKG_VERSION','UNKNOWN');pa='x86' if arch=='x86_64' else arch;prj='projects/ROCKNIX';ds=[d+'/patches',d+'/patches/'+pa]
 ds += [d+'/patches/'+x for x in m['extras']]
 ds += [d+'/patches/'+v,d+'/patches/'+v+'/'+pa,prj+'/patches/'+name,prj+'/patches/'+name+'/'+pa]
 for x in m['extras']:ds += [prj+'/patches/'+name+'/'+x,prj+'/devices/'+device+'/patches/'+name+'/'+x]
 ds += [prj+'/patches/'+name+'/'+v,prj+'/devices/'+device+'/patches/'+name]
 out=[]
 for d in ds:out+=children(d)
 return out
groups={}
for n in native:
 p=selected_recipe(n)
 for plan in n['plans']:
  key=(p,plan)
  if key not in groups:
   device,arch=plan.rsplit('-',1);m=meta(p,device,arch);st=stack(p,m,device,arch);name=m['values'].get('PKG_NAME',p.split('/')[-2]);pin=m['values'].get('PKG_VERSION','UNKNOWN');cache=pathlib.Path('/workspace/cache/rocknix-sources')/name
   cand=sorted(str(x) for x in cache.glob('*') if x.is_file() and not x.name.endswith(('.sha256','.url')) and (x.name.startswith(name+'-'+pin+'.') or x.name==m['values'].get('PKG_SOURCE_NAME')))
   reasons=m['ambiguity']+m['stack_unknown']
   if m['hooks']:reasons.append('pre-patch/custom unpack input needs source transformation proof: '+', '.join(m['hooks']))
   if not re.fullmatch('[0-9a-f]{64}',m['values'].get('PKG_SHA256','')):reasons.append('recipe lacks statically proved archive SHA256; cached git directories are not archive proof')
   if len(cand)!=1:reasons.append(f'exact pin archive candidate count {len(cand)}; need {name}-{pin} archive and matching sidecar')
   if re.search(r'[$`]',pin):reasons.append('symbolic pin unresolved')
   groups[key]=dict(id='G%03d'%(len(groups)+1),recipe=p,plan=plan,device=device,arch=arch,patch_arch='x86' if arch=='x86_64' else arch,metadata=m,stack=[dict(path=q,referent=resolve(q),mode=T[resolve(q)]['mode'],oid=T[resolve(q)]['oid'],sha256=sha(blob(resolve(q)))) for q in st],archives=cand,open_reasons=reasons,native=[])
  groups[key]['native'].append(n['path'])
  if n['path'] not in [s['path'] for s in groups[key]['stack']]:groups[key]['open_reasons'].append('member '+n['path']+' not selected by conservative static stack; survey reach is not executed selection')
for g in groups.values():g['open_reasons']=list(dict.fromkeys(g['open_reasons']))
dump(B/'selection.json',list(groups.values()));print('groups',len(groups),'eligible before archive verification',sum(not g['open_reasons'] for g in groups.values()))
dump(B/'native-read-assessment.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reader='Codex / GPT-6-Astra / xhigh',ranges=[dict(first=1,last=79,assessment='Toolchain/build convention patches dominate; Python feature disabling is intentional distribution policy, not upstream supersession. woff2 and WebKit full-line reads bind historical target comments to current pins; application required.'),dict(first=80,last=161,assessment='Device policies and build fixes; FEX thunk include exclusion is full-line read. Mangohud branch and link need separate selection; context-format readline cannot be lost by unified-diff-only tooling. Archive proof must preserve headers versus attribution claims.'),dict(first=162,last=241,assessment='Emulator Makefiles require rendered DEVICE and architecture branches. Vitaquake links remain native identities while x86_64 unselected siblings stay #1071. Dolphin lifecycle requires ScopeGuard source and actual post_unpack state.'),dict(first=242,last=320,assessment='PPSSPP 007 outer diff creates a nested patch instead of editing SDL source: investigate bug. Mesa/SDL teardown readings do not prove runtime efficiency. FFmpeg series are multi-commit aggregates, not one Subject per entire file.'),dict(first=321,last=384,assessment='Network/service state paths are product policy. Systemd integration decisions stay #1104. T43 MangoHud referent stays context. atf H700 source lacks recipe checksum and cannot be admitted from filename alone.')],coverage='384 path/header/target/currency digests reviewed; recipes and exact context read where stated. Not 71,387 lines of code review. Full line read only explicitly recorded twelve fork-written patches.'))

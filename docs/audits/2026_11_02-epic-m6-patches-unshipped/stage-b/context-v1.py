#!/usr/bin/env python3
"""Static T43 recipe/selector census; no shell evaluation or inventory producer."""
import collections,datetime,hashlib,json,pathlib,re,subprocess,fnmatch
R=pathlib.Path(__file__).resolve().parents[1];B=json.loads((R/'stage-a/bindings.json').read_text());S=B['source'];U=B['upstream'];C=R/'stage-b'
def git(*a):return subprocess.check_output(['git',*a])
def show(p,ref=S):return git('show',ref+':'+p)
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(C/n).write_text(json.dumps(x,indent=2)+'\n')
rows=json.loads((C/'observations.json').read_text());recipe_meta=json.loads(show('docs/qa-logs/2026-11-02-m6-resume/t43-preparation/recipes.json'));paths=git('ls-tree','-r','--name-only',S).decode().splitlines();pathset=set(paths)
records={};plans=[];context={}
for p in ['scripts/unpack','scripts/extract','config/functions','config/options','config/arch.arm','config/arch.aarch64','config/arch.x86_64','distributions/ROCKNIX/options','projects/ROCKNIX/options']:
 b=show(p);context[p]={'sha256':sha(b),'lines':b.decode().splitlines()}
def assignments(t):return [[i,l] for i,l in enumerate(t.splitlines(),1) if re.search(r'PKG_(VERSION|SHA256|URL|SITE|NAME|PATCH_DIRS)|^(unpack|post_unpack|pre_patch)\(',l)]
def literals(t):return dict(re.findall(r'^([A-Z0-9_]+)="([^"\n]*)"',t,re.M))
for rp,rm in recipe_meta.items():
 raw=show(rp);t=raw.decode();assert sha(raw)==rm['sha256_P1'];vv=literals(t);name=vv['PKG_NAME'];directory=str(pathlib.PurePosixPath(rp).parent)
 records[rp]={'sha256':sha(raw),'owner':rm['owner_P1'],'member_count':rm['paths'],'source_lines':t.splitlines(),'assignments':assignments(t),'upstream_sha256':sha(show(rp,U)),'upstream_assignments':assignments(show(rp,U).decode())}
 for consumer in sorted({c for x in rows if x['source_recipe']==rp for c in x['buildable_by']}):
  dev,arch=consumer.rsplit('-',1);optpath=f'projects/ROCKNIX/devices/{dev}/options';opt=show(optpath).decode();context[optpath]={'sha256':sha(opt.encode()),'lines':opt.splitlines()};cpus=re.findall(r'TARGET_CPU="([^"]+)"',opt);cpu=cpus[0];v=vv.copy();extra=[];limits=[]
  if name=='linux':
   pin={'AMD64':'7.1.2','RK3326':'7.1.2','RK3399':'6.18.49','RK3566':'7.0.2','RK3576':'7.0.2','RK3588':'b8e62bed74766b6c8c423a767b35495e78b64caf','S922X':'6.18.49'}.get(dev,'7.2');m=re.search(r'PKG_VERSION="'+pin+r'"\n\s+PKG_SHA256="([^"]+)"\n\s+PKG_URL="([^"]+)"',t);assert m;v.update(PKG_VERSION=pin,PKG_SHA256=m[1],PKG_URL=m[2]);extra=['mainline',dev,'default']
   if dev.startswith('RK'):extra+=['mainline-rockchip']
   if dev in ['RK3326','AMD64','RK3566','RK3576']:extra+=['7.0']
   if dev=='RK3588':extra=[dev,'default']
  elif name=='libmali':
   extra=[dev]
   if dev in ['RK3326','RK3566','RK3576']:
    v.update(PKG_VERSION='4233031d818e97a19e8a9cdbbd5c15795ededd93',PKG_SHA256='54b8af924f582f7da7e120fbad4812a502cc7cc67f6d6ab061377cb403f3eb2d',PKG_SITE='https://github.com/JeffyCN/mirrors');extra+=['next']
   limits+=['custom unpack selects LIBNAME/MALI_FAMILY/PLATFORM and renames data; exact complete preimage not established']
  elif name=='wlroots':
   pin='0.19.3-rk' if dev in ['RK3326','RK3566','RK3576','S922X'] else ('0.17.4-rk' if dev=='RK3588' else '0.19.3');m=re.search(r'PKG_VERSION="'+re.escape(pin)+r'"\n\s+PKG_SHA256="([^"]+)"',t);assert m;v.update(PKG_VERSION=pin,PKG_SHA256=m[1],PKG_URL='https://github.com/rocknix/rockchip-wlroots/archive/refs/tags/${PKG_VERSION}.tar.gz');extra=['libmali'] if pin=='0.19.3-rk' else []
  elif name=='atf':v.update(PKG_VERSION='2.10.0',PKG_SHA256='696b8e53923aac4474532da7dd681f0bd044b329732facd65aeabea3e61adca9');extra=[dev]
  elif name=='gamepadtester':extra=[dev,'xbox' if dev in ['SM8650','SM8750','SM8550','SM8250'] else 'legacy']
  elif name=='mangohud':extra=['common']+(['qualcomm'] if dev.startswith('SM') else [])+(['batteryplus'] if dev=='S922X' else [])+[dev]
  elif name=='ffmpeg':extra=['libreelec','v4l2-request','v4l2-drmprime']+(['vf-deinterlace-v4l2m2m'] if dev.startswith('RK') and dev!='RK3588' else []);limits+=['post_unpack VERSION/RELEASE write and PKG_FFMPEG_BRANCH input not materialized; no full preimage claim']
  elif name=='azahar-sa':extra=['prefer_gles'];limits+=['Git/submodule source recipe has no archive SHA256; no exact archive input permitted by this runner']
  else:
   extra=[dev] if re.search(r'PKG_PATCH_DIRS\+?="\s*\$\{DEVICE\}"',t) else []
  if name=='ppsspp-sa':limits+=['Git/submodule source lacks archive SHA256; post_unpack generated make/ninja inputs not established']
  if name=='xemu-sa':limits+=['post_unpack edits configure using build TOOLCHAIN path; full preimage not established']
  if name=='ectool':limits+=['Git source recipe has no archive SHA256; no cached exact archive']
  if re.search(r'^(pre_patch|post_unpack|unpack)\(',t,re.M) and name not in ['libmali','ffmpeg','ppsspp-sa','xemu-sa','wlroots']:raise AssertionError(('unreviewed hook',rp))
  pin=v.get('PKG_VERSION','unknown');url=v.get('PKG_URL','unknown')
  for _ in range(6):
   url=url.replace('${PKG_VERSION/.*/}',pin.split('.')[0]);url=re.sub(r'\$\{([A-Z0-9_]+)\}|\$([A-Z0-9_]+)',lambda m:v.get(m[1] or m[2],m[0]),url)
  assert '$' not in url,(rp,url)
  parch='x86' if arch=='x86_64' else ('aarch64' if name in ['linux','mali-bifrost'] else arch)
  pkgdirs=[directory+'/patches/'+x for x in extra];prjdirs=['projects/ROCKNIX/patches/'+name+'/'+x for x in extra]+['projects/ROCKNIX/devices/'+dev+'/patches/'+name+'/'+x for x in extra]
  # scripts/unpack appends project and device explicit selectors interleaved per extra.
  prjdirs=[q for x in extra for q in ['projects/ROCKNIX/patches/'+name+'/'+x,'projects/ROCKNIX/devices/'+dev+'/patches/'+name+'/'+x]]
  dirs=[directory+'/patches',directory+'/patches/'+parch]+pkgdirs+[directory+'/patches/'+pin,directory+'/patches/'+pin+'/'+parch,'projects/ROCKNIX/patches/'+name,'projects/ROCKNIX/patches/'+name+'/'+parch]+prjdirs+['projects/ROCKNIX/patches/'+name+'/'+pin,'projects/ROCKNIX/devices/'+dev+'/patches/'+name]
  stack=[p for d in dirs for p in sorted(paths) if str(pathlib.PurePosixPath(p).parent)==d and p.endswith('.patch')]
  native=[x['path'] for x in rows if x['source_recipe']==rp and consumer in x['buildable_by'] and x['kind']!='config'];missing=sorted(set(native)-set(stack))
  if missing:limits+=['inventory rows outside static selected stack: '+', '.join(missing)]
  overlays=[p for p in paths if p.startswith(directory+'/sources/')]
  if overlays:limits+=['package sources/ overlay present; exact overlap/preimage not materialized']
  if not v.get('PKG_SHA256'):limits+=['recipe lacks archive checksum']
  cachedir=pathlib.Path('/workspace/cache/rocknix-sources')/name
  candidates=[str(p) for p in sorted(cachedir.iterdir()) if p.is_file() and not p.name.endswith(('.sha256','.url')) and pin in p.name] if cachedir.is_dir() else []
  gid=f'G{len(plans)+1:03}';plans.append({'id':gid,'recipe':rp,'recipe_sha256':sha(raw),'owner':rm['owner_P1'],'consumer':consumer,'device':dev,'arch':arch,'target_cpu':cpu,'patch_arch':parch,'LINUX':'unset in clean default source config','batteryplus':'yes' if dev=='S922X' else 'no or unset; exact yes predicate false','name':name,'pin':pin,'url':url,'expected_sha256':v.get('PKG_SHA256'),'selectors':extra,'ordered_pattern_directories':dirs,'stack':stack,'native_paths':native,'config_paths':[x['path'] for x in rows if x['source_recipe']==rp and consumer in x['buildable_by'] and x['kind']=='config'],'cache_candidates':candidates,'preimage_limits':limits,'source_only':True,'runtime':False})
write('recipes.json',records);write('source-context.json',context);write('plans.json',plans)
write('execution-census.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plans':len(plans),'recipes':len(records),'all_source_only':True,'CPU_affinity':'8-23','not_run':['config/recipe','unpack/extract scripts','build/compiler','guest','device/cloud','provider','host ledger','accepted producers'],'input_files':{'observations.json':sha((C/'observations.json').read_bytes()),'recipes-preparation':sha(show('docs/qa-logs/2026-11-02-m6-resume/t43-preparation/recipes.json'))}})
print(json.dumps({'plans':len(plans),'recipes':len(records),'missing_selection':[(p['id'],p['preimage_limits']) for p in plans if any('outside static' in x for x in p['preimage_limits'])],'cache_candidates':sum(bool(p['cache_candidates']) for p in plans)}))

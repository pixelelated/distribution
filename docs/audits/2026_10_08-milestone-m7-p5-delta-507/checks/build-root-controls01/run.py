from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys

owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
results=[]
def put(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(data)
def read(path):return path.read_text() if path.is_file() else None
def same(path,expected):
 observed=read(path)
 if observed is None:return False
 if path.suffix=='.json':
  try:return json.loads(observed)==json.loads(expected)
  except ValueError:return False
 return observed==expected
def hook(kind,version,brand,arch='aarch64',missing=False):
 label='-'.join([kind,version,brand,arch,'missing' if missing else 'present'])
 root=owner/'cases'/label;root.mkdir(parents=True)
 src=root/'source';src.mkdir();install=root/'installed';pkgdir=root/'recipe-data';pkgdir.mkdir()
 arm=root/('build.'+brand+'-H700.arm');prefix=arm/'install_pkg';desired={};links={}
 def witness(rel,data):desired[rel]=data
 if kind=='box86':
  src=arm/'build/box86-fixture';src.mkdir(parents=True)
  for rel,data in {'x86lib/witness.so':'x86 library','.arm-test/box86':'ARM box86','tests/bash':'x86 bash','.arm-test/system/box86.conf':'binfmt witness','system/box86.box86rc':'configuration witness'}.items():put(src/rel,data)
  mapping={'usr/share/box86/lib/witness.so':'x86 library','usr/bin/box86':'ARM box86','usr/bin/bash-x86':'x86 bash','etc/binfmt.d/box86.conf':'binfmt witness','usr/config/box86.box86rc':'configuration witness'}
  for rel,data in mapping.items():put(prefix/'box86-fixture'/rel,data);witness(rel,data)
  links['etc/box86.box86rc']='/storage/.config/box86.box86rc'
 elif kind in ['gpsp-lr','desmume-lr']:
  core=kind[:-3]+'_libretro.so';rel='usr/lib/libretro/'+core
  put(prefix/(kind+'-fixture')/rel,'ARM '+core);witness(rel,'ARM '+core)
 elif kind=='daedalusx64-sa':
  recipe=(owner/version/(kind+'.mk')).read_text()
  pin=next(l.split('"')[1] for l in recipe.splitlines() if l.startswith('PKG_VERSION='))
  for rel,data in {'usr/bin/DaedalusX64':'launch witness','usr/config/DaedalusX64/daedalus':'ARM daedalus'}.items():put(prefix/(kind+'-'+pin)/rel,data);witness(rel,data)
 elif kind=='lib32':
  image=arm/'image/system'
  for rel,data in {'usr/lib/libc.so.6':'ARM libc','usr/lib32/driver.so':'ARM driver','usr/bin/ldd':'ARM ldd','usr/share/vulkan/icd.d/test.json':'{"ICD":{"library_path":"/usr/lib/driver.so","library_arch":"64"}}'}.items():put(image/rel,data)
  witness('usr/lib32/libc.so.6','ARM libc');witness('usr/lib32/driver.so','ARM driver');witness('usr/bin/ldd32','ARM ldd')
  witness('usr/share/vulkan/icd.d/test.lib32.json','{"ICD":{"library_path":"/usr/lib32/driver.so","library_arch":"32"}}')
  links['usr/lib/ld-linux-armhf.so.3']='/usr/lib32/ld-linux-armhf.so.3'
 elif kind=='retroarch':
  for rel,data in {'retroarch':'native retroarch','retroarch.cfg':'default cfg','gfx/video_filters/native.so':'native video','gfx/video_filters/native.filt':'video descriptor','libretro-common/audio/dsp_filters/native.so':'native audio','libretro-common/audio/dsp_filters/native.dsp':'audio descriptor'}.items():put(src/rel,data)
  for rel,data in {'sources/H700/device.cfg':'device cfg','sounds/witness.wav':'sound','scripts/call_achievements_hooks.sh':'hook'}.items():put(pkgdir/rel,data)
  for rel,data in {'usr/bin/retroarch':'ARM retroarch','usr/share/retroarch/filters/64bit/video/arm.so':'ARM video','usr/share/retroarch/filters/64bit/audio/arm.so':'ARM audio'}.items():put(prefix/'retroarch-fixture'/rel,data)
  witness('usr/bin/retroarch','native retroarch');witness('usr/bin/retroarch32','ARM retroarch');witness('usr/share/retroarch/filters/32bit/video/arm.so','ARM video');witness('usr/share/retroarch/filters/32bit/audio/arm.so','ARM audio')
 else:raise AssertionError(kind)
 if missing:shutil.rmtree(arm)
 # A renamed build must not silently consume an older ROCKNIX sibling.
 old=root/'build.ROCKNIX-H700.arm'
 if brand!='ROCKNIX' and not missing:
  shutil.copytree(arm,old)
  for p in old.rglob('*'):
   if p.is_file():p.write_text('WRONG OLD BUILD')
 env=dict(os.environ,ROOT=str(root),DISTRO='ROCKNIX',DISTRONAME=brand,DEVICE='H700',ARCH=arch,TARGET_ARCH=arch,TARGET_NAME='arm-test',ENABLE_32BIT='true',PKG_BUILD=str(src),PKG_DIR=str(pkgdir),INSTALL=str(install))
 recipe=owner/version/(kind+'.mk')
 with (owner/'artifacts'/(label+'.log')).open('x') as out:
  completed=subprocess.run(['bash','-c','source "$1"; set -e; makeinstall_target','control',str(recipe)],cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT)
 observed=completed.returncode==0 and all(same(install/rel,data) for rel,data in desired.items()) and all((install/rel).is_symlink() and os.readlink(install/rel)==target for rel,target in links.items())
 expect=not missing and (version=='fixed' or brand=='ROCKNIX')
 assert observed==expect,(label,completed.returncode,observed,expect)
 results.append({'case':label,'command_rc':completed.returncode,'required_payload_verified':observed,'expected_payload':expect,'result':'PASS'})
 print('PASS',label,'payload='+str(observed),flush=True)

def lifecycle(version,brand,alias=False):
 label='lifecycle-'+version+'-'+brand+('-alias' if alias else '-same-device')
 root=owner/'cases'/label;root.mkdir(parents=True)
 device='H700';base='BASE' if alias else device
 script=root/'scripts/build_distro';script.parent.mkdir();shutil.copyfile(owner/version/'build_distro',script);script.chmod(0o755)
 for name in ['checkdeps','clean']:put(root/'scripts'/name,'#!/bin/bash\nexit 0\n');(root/'scripts'/name).chmod(0o755)
 put(root/'config/options','DISTRO=ROCKNIX\nDISTRONAME='+brand+'\nPROJECT=ROCKNIX\nDEVICE=H700\nDEVICE_ROOT='+base+'\nARCH=arm\nENABLE_32BIT=false\n')
 put(root/'projects/ROCKNIX/devices/H700/options','true\n')
 target=root/('build.'+brand+'-'+base+'.arm')
 for rel in ['image/old','initramfs/old','.stamps/initramfs/old']:put(target/rel,'remove this generated output')
 if alias:put(root/('build.'+brand+'-H700.arm')/'stale','remove stale child')
 for area in ['target','release']:put(root/area/(brand+'-H700.arm-old.tar'),'remove old image')
 put(root/'protected/input','keep exact input')
 if brand!='ROCKNIX':
  put(root/'build.ROCKNIX-H700.arm/image/keep','keep unrelated sibling')
  put(root/'target/ROCKNIX-H700.arm-keep.tar','keep unrelated image')
 env=dict(os.environ,ARCH='arm',RASTERATOPS_WATCH_EXEC=str(script));env.pop('DIRTY',None)
 with (owner/'artifacts'/(label+'.log')).open('x') as out:r=subprocess.run([str(script)],cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT)
 expected=version=='fixed' or brand=='ROCKNIX'
 observed=r.returncode==0 and all(not (target/rel).exists() for rel in ['image','initramfs','.stamps/initramfs']) and not list((root/'target').glob(brand+'-H700.arm-old*')) and not list((root/'release').glob(brand+'-H700.arm-old*'))
 if alias:observed=observed and (root/('build.'+brand+'-H700.arm')).is_symlink() and (root/('build.'+brand+'-H700.arm')).resolve()==target
 assert observed==expected,(label,observed,r.returncode)
 if expected:
  assert read(root/'protected/input')=='keep exact input'
  if brand!='ROCKNIX':assert read(root/'build.ROCKNIX-H700.arm/image/keep')=='keep unrelated sibling' and read(root/'target/ROCKNIX-H700.arm-keep.tar')=='keep unrelated image'
 results.append({'case':label,'command_rc':r.returncode,'generated_paths_cleaned':observed,'expected':expected,'result':'PASS'});print('PASS',label,flush=True)

rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 for kind in ['box86','lib32','gpsp-lr','desmume-lr','daedalusx64-sa','retroarch']:
  for version,brand in [('original','pixelelated'),('fixed','pixelelated'),('original','ROCKNIX'),('fixed','ROCKNIX')]:hook(kind,version,brand)
 for version in ['original','fixed']:
  for brand in ['ROCKNIX','pixelelated']:hook('box86',version,brand,'arm')
 for kind in ['box86','lib32','gpsp-lr','desmume-lr','daedalusx64-sa','retroarch']:hook(kind,'fixed','pixelelated',missing=True)
 for version in ['original','fixed']:
  for brand in ['ROCKNIX','pixelelated']:
   for alias in [False,True]:lifecycle(version,brand,alias)
 (owner/'artifacts/result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','cases':results,'scope':'actual recipe install hooks and build_distro in isolated host fixtures; original expected failures, unchanged ROCKNIX controls, renamed collision and missing-payload controls; actual device build acceptance remains separate'},indent=2)+'\n')
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)

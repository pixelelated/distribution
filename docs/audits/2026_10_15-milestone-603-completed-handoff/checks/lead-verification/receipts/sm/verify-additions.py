"""Additional device installed mappings; reuse the qualified Local/Squash reader."""
from pathlib import Path,PurePosixPath
import argparse,datetime,hashlib,importlib.machinery,importlib.util,json,os,re,stat,subprocess
p=argparse.ArgumentParser();p.add_argument('--system',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text());T=Path(j['host_worktree']);R=T/j['build_root'];root=R/'image/system'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
checker=T/'tools/pixelelated-state-check';assert sha(checker)=='65ab515ec2c0ccdf474f08128cabf1dea774846a8add3725cd05d334b2e1eba6'
loader=importlib.machinery.SourceFileLoader('device_state_reader',str(checker));spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
left=m.Local(root);right=m.Squash(a.system) if a.system else None

def link_chain(fs,path):
 pending=list(PurePosixPath(path).parts[1:]);done=[];links=[]
 while pending:
  part=pending.pop(0)
  if part in ('','.'):continue
  if part=='..':assert done;done.pop();continue
  candidate='/'+ '/'.join(done+[part]);target=fs.link(candidate)
  if target is not None:
   links.append({'path':candidate,'target':target});assert len(links)<=40
   target_path=PurePosixPath(target)
   if target_path.is_absolute():done=[];pending=list(target_path.parts[1:])+pending
   else:pending=list(target_path.parts)+pending
  else:done.append(part)
 return {'resolved':'/'+'/'.join(done),'links':links}

mapping={
 'usr/bin/cloud_oauth':'projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth',
 'usr/bin/raofflineproxy-ctl':'projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl',
 'usr/bin/runemu.sh':'projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh',
 'usr/bin/wifictl':'projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl'}
paths=['usr/bin/python3','usr/bin/gst-inspect-1.0','usr/lib/gstreamer-1.0/gst-plugin-scanner','usr/lib/gstreamer-1.0/libgstopengl.so','usr/lib/libgstcontroller-1.0.so.0','usr/lib/libgstnet-1.0.so.0','usr/lib/libgstreamer-1.0.so.0','usr/lib/libgstmpegts-1.0.so.0','usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo','usr/config/locale/en_GB/LC_MESSAGES/emulationstation2.mo']
sysrows={};special={}
# The frozen device package graph selects gst-plugins-good through Qt6/Dolphin
# on SM8550. H700 selects core/base/bad for its sign-in window, without Qt6.
assert j['device'] in ['H700','SM8550']
good_paths=['usr/lib/gstreamer-1.0/libgstadaptivedemux2.so','usr/lib/gstreamer-1.0/libgstrtpmanager.so','usr/lib/gstreamer-1.0/libgstrtsp.so','usr/lib/gstreamer-1.0/libgstudp.so']
good_packages=sorted(R.glob('install_pkg/gst-plugins-good-*'))
good_stamp=R/'.stamps/gst-plugins-good'
if j['device']=='H700':
 assert not good_packages and not good_stamp.exists() and not good_stamp.is_symlink(),'unexpected H700 gst-plugins-good selection'
 for n in good_paths:
  assert left.info('/'+n) is None,n+' unexpectedly present on H700'
  if right:assert right.info('/'+n) is None,n+' unexpectedly packaged on H700'
else:
 assert len(good_packages)==1 and good_packages[0].is_dir() and (good_stamp/'build_target').is_file()
 assert (R/'.stamps/qt6/build_target').is_file()
 paths+=good_paths
special['gstreamer_profile']={'device':j['device'],'gst_plugins_good_selected':j['device']=='SM8550','expected_absent_paths':good_paths if j['device']=='H700' else [],'package_graph':'Frozen emulators device case -> Dolphin -> Qt6 -> gst-plugins-good on SM8550; WebKit requires core/base/bad on both.'}
if j['device']=='SM8550':
 assert 'VULKAN_SUPPORT="yes"' in (T/'projects/ROCKNIX/devices/SM8550/options').read_text()
 for n in ['start_dolphin_gc.sh','start_dolphin_wii.sh','cheevos_dolphin.sh','dolphin-save-paths']:mapping['usr/bin/'+n]='projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/'+n
 mapping['usr/config/modules/Install Steam.sh']='projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh'
 paths+=['usr/bin/dolphin-emu','usr/bin/dolphin-emu-nogui','usr/bin/steam']
 sysdata=json.loads((O/'dolphin-sys-source-manifest.json').read_text());sysrows={r['installed_path']:r for r in sysdata['products']};assert len(sysrows)==6
 dolphin=R/'build'/('dolphin-sa-'+sysdata['dolphin_pin'])
 for n,row in sysrows.items():assert sha(dolphin/row['source_relative'])==row['sha256'];paths.append(n)
 cmake=dolphin/'.aarch64-rocknix-linux-gnu/CMakeCache.txt';assert 'USE_RETRO_ACHIEVEMENTS:BOOL=ON' in cmake.read_text()
 patch=T/'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch'
 with patch.open('rb') as f:proof=subprocess.run(['patch','--dry-run','--batch','--fuzz=0','--reverse','-p1'],cwd=dolphin,stdin=f,capture_output=True)
 assert proof.returncode==0,proof.stderr
 special['dolphin_patch018']={'patch_sha256':sha(patch),'reverse_dry_run_exit':proof.returncode,'stdout':proof.stdout.decode(),'stderr':proof.stderr.decode(),'actual_MainNoGUI_sha256':sha(dolphin/'Source/Core/DolphinNoGUI/MainNoGUI.cpp')}
 base=T/'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/config/SM8550'
 for folder,dirs,files in os.walk(base,followlinks=True):
  for name in files:
   f=Path(folder)/name;assert f.resolve().is_relative_to(T/'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/config')
   mapping['usr/config/dolphin-emu/'+str(f.relative_to(base))]=str(f.relative_to(T))
 # Actual current ABL recipe has one signed ELF plus four support files.
 abl=R/'install_pkg/rocknix-abl-1.2/usr/share/bootloader/rocknix_abl';ablrows={str(f.relative_to(abl)):sha(f) for f in abl.rglob('*') if f.is_file()};assert len(ablrows)==5 and 'abl_signed-SM8550.elf' in ablrows
 for n,h in ablrows.items():assert sha(root/'usr/share/bootloader/rocknix_abl'/n)==h;paths.append('usr/share/bootloader/rocknix_abl/'+n)
 abl_source=R/'build/rocknix-abl-1.2'
 assert sha(abl_source/'abl_signed-SM8550.elf')==ablrows['abl_signed-SM8550.elf']
 for name in ['README','backup_abl.sh','restore_backup_abl.sh']:
  assert sha(T/'projects/ROCKNIX/packages/tools/rocknix-abl/sources'/name)==ablrows[name]
 template=(T/'projects/ROCKNIX/packages/tools/rocknix-abl/sources/flash_abl.sh.template').read_bytes()
 assert hashlib.sha256(template.replace(b'%DEVICE%',b'SM8550')).hexdigest()==ablrows['flash_abl.sh']
 expected_path=O/'abl-expected.json';assert sha(expected_path)==j['abl_expected_sha256']
 expected=json.loads(expected_path.read_text());assert len(expected['files'])==5
 assert {Path(r['installed_path']).name:r['expected_installed_sha256'] for r in expected['files']}==ablrows
 for r in expected['files']:
  f=abl/Path(r['installed_path']).name;assert f.stat().st_size==r['expected_installed_bytes']
  expected_mode=stat.S_IMODE((T/r['source']).stat().st_mode) if r.get('source_sha256') else int(r['expected_installed_mode'],8)&0o777
  assert stat.S_IMODE(f.stat().st_mode)==expected_mode
 special['abl_1_2_source_readback']={'expected_manifest_sha256':sha(expected_path),'root_archive_readback':expected['root_archive_readback'],'archive_sha256':'64034fb076ea0bb858beaa2f29dbef635e97d29f3e3d32c13bce61bd4af4cff7','LinuxLoader_commit':'e9d37131c0c2273076468156fb0f87aa6834202b','scope':'Exact retained archive member digest and unchanged support-file source mapping; implementation source/notice custody remains a separate hold.'}
 special['abl_1_2']=ablrows
for n,src in mapping.items():
 expected=(T/src).read_bytes()
 if Path(n).name in ['start_dolphin_gc.sh','start_dolphin_wii.sh']:expected=expected.replace(b'@DOLPHIN_BACKEND@',b'wayland').replace(b'@GRENDERER@',b'Vulkan').replace(b'@EXPORTS@',b'export QT_QPA_PLATFORM=wayland')
 assert left.read('/'+n)==expected,n+' source/install mismatch'
paths+=list(mapping)
products={}
for n in sorted(set(paths)):
 path='/'+n;data=left.read(path,limit=256*1024**2);mode=stat.filemode(left.resolve(path).stat().st_mode);links=link_chain(left,path)
 if right:
  assert right.read(path,limit=256*1024**2)==data,n
  assert link_chain(right,path)==links and right.nodes[right.resolve(path)][0]==mode,n
 row={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'mode':mode,'link_chain':links};products[n]=row
 if n in sysrows:
  exp=sysrows[n];assert row['sha256']==exp['sha256'] and len(data)==exp['bytes'] and mode==exp['expected_installed_mode']
  assert links=={'resolved':'/'+exp['installed_target'],'links':[{'path':'/usr/share/dolphin-emu/sys','target':'../../config/dolphin-emu'}]}
 # The exact signed ABL release member is ELF32/EM_ARM, not a Linux userland ELF.
 if n=='usr/share/bootloader/rocknix_abl/abl_signed-SM8550.elf':
  assert j['device']=='SM8550' and len(data)==258048 and row['sha256']=='8c27a70961476b327071ada2fd9b9c55dd2dcdc913eff3d33f2576133d7e398c'
  assert data[:6]==b'\x7fELF\x01\x01' and int.from_bytes(data[18:20],'little')==40,n
  special['abl_1_2_format']={'class':'ELF32','encoding':'little-endian','e_machine':40,'header64_hex':data[:64].hex(),'scope':'Exact signed release member, not Linux userland or native boot qualification'}
 elif data[:4]==b'\x7fELF' and n!='usr/bin/steam':assert data[:6]==b'\x7fELF\x02\x01' and int.from_bytes(data[18:20],'little')==183,n
# Read ELF dependency metadata without loading or executing any target binary.
closure={}
for name in paths:
 if name.startswith(('usr/lib/gstreamer-1.0/','usr/lib/libgst','usr/bin/gst-')):
  path=left.resolve('/'+name);data=path.read_bytes()
  if data[:4]!=b'\x7fELF':continue
  text=subprocess.check_output(['readelf','-d',str(path)],text=True)
  needed=re.findall(r'\(NEEDED\).*?\[(.*?)\]',text);closure[name]=needed
  for lib in needed:
   assert '/' not in lib and any(left.info(prefix+lib) is not None for prefix in ['/usr/lib/','/lib/']),name+' missing '+lib
   if right:assert any(right.info(prefix+lib) is not None for prefix in ['/usr/lib/','/lib/']),name+' packaged dependency '+lib
special['gstreamer_DT_NEEDED']=closure
# Raw KERNEL equality is checked independently by each original firmware reader.
patch=T/'projects/ROCKNIX/packages/linux/patches/7.2/0016-drm-msm-dp-return-0-from-audio_prepare-when-cable-is-disconnected.patch'
assert sha(patch)=='81665288adedb443e7c555e11ecf40cd05d819b10c6a5761e7326a64576d3815'
assert (R/'.stamps/linux/build_target').is_file()
special['kernel']={'recipe_version':'7.2','shared_patch_sha256':sha(patch),'actual_build_stamp_sha256':sha(R/'.stamps/linux/build_target'),'scope':'Normal package clean/rebuild and canonical KERNEL assembly; no physical boot claim.'}
result={'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'device':j['device'],'source':j['distribution_commit'],'products':products,'source_mappings':mapping,'special':special,'comparison':'staged and independently extracted SYSTEM bytes/modes/link chains' if right else 'source and staged bytes; independent firmware readback still required'}
out=a.output or O/'artifacts/affected-products-staged.json';out.write_text(json.dumps(result,indent=2)+'\n');print('PASS affected '+j['device']+' installed mappings; '+str(len(products))+' products')

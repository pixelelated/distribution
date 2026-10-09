import pathlib,subprocess,json,hashlib,os,shutil,time,importlib.util,fcntl
P=pathlib.Path;Q=P('/storage/qa519-operation');O=P('/storage/.cache/pixelelated-owner-alignment-519')
S=P('/storage/.config/system/configs/system.cfg');C=P('/storage/.config/cloud_sync.conf');M=P('/storage/.config/cloud-layout-migration.json');D=P('/storage/.cache/cloud_sync/scan')
assert 'GENERIC_X64' in P('/etc/os-release').read_text();assert not P('/storage/.config/rclone/rclone.conf').exists()
def run(a,rc=0):
 p=subprocess.run(a,capture_output=True,text=True,timeout=120)
 assert p.returncode==rc,(a,p.returncode,p.stdout,p.stderr)
 return p
def shell(s):return run(['bash','-c',s])
spec=importlib.util.spec_from_file_location('i',Q/'inspect.py');I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
def replace(data,values):
 import re
 s=data.decode()
 for k,v in values.items():
  s,n=re.subn('^'+k+'=.*$',k+'="'+v+'"',s,flags=re.M);assert n==1
 return s.encode()
shell('systemctl stop essway.service emustation.service')
for p in [P('/storage/.config/rclone'),P('/storage/roms/savefiles'),P('/storage/.cache/cloud_sync/replaced')]:p.mkdir(parents=True,exist_ok=True)
P('/storage/.config/rclone/rclone.conf').write_text('[qa519]\ntype = alias\nremote = /storage/qa519-operation/cloud\n');P('/storage/.config/rclone/rclone.conf').chmod(0o600)
for p in [Q/'cloud/ROCKNIX/Saves/savefiles',Q/'cloud/ROCKNIX/Backups',Q/'cloud/ROCKNIX/Content']:p.mkdir(parents=True,exist_ok=True)
P('/storage/roms/savefiles/qa519.srm').write_bytes(b'synthetic owner progress\n');(Q/'cloud/ROCKNIX/Saves/savefiles/qa519.srm').write_bytes(b'synthetic owner progress\n');P('/storage/.cache/cloud_sync/replaced/qa519.srm').write_bytes(b'synthetic older progress\n')
shell('. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 0 cloudsaves.gameexit 0')
S.write_bytes(S.read_bytes()+b'qa519.duplicate=first\nqa519.duplicate=last\n');S.chmod(0o644);S.with_name(S.name+'.backup').chmod(0o644)
C.write_bytes(replace(C.read_bytes(),{'SAVES_REMOTE':'/ROCKNIX/Saves','SETTINGS_REMOTE':'/ROCKNIX/Backups','CONTENT_REMOTE':'/ROCKNIX/Content','LAYOUT_KEEP':'/ROCKNIX/Saves'}));C.chmod(0o644)
shell('systemctl start essway.service');time.sleep(3)
# ES cached0 and keep-guarded while preparing pending auto1 state on disk.
shell('. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 1 cloudsaves.gameexit 1; chksysconfig backup')
C.write_bytes(replace(C.read_bytes(),{'SAVES_REMOTE':'/pixelelated/Saves','SETTINGS_REMOTE':'/pixelelated/Backups','LAYOUT_KEEP':''}))
CB=C.with_name(C.name+'.bak')
if CB.exists():CB.unlink()
M.write_text('{"schema":1,"step":1,"stage":"discarded"}\n');M.chmod(0o644)
if D.exists():shutil.rmtree(D)
D.mkdir();(D/'join').write_bytes(b'');(D/'state').write_text('synthetic old scan\n')
C.with_name(C.name+'.pre-contentpath-fix').write_text('# invented historical backup\n')
base=I.collect()
plan={'schema':1,'operation_sha256':I.digest(Q/'operation.py'),'collector_sha256':I.digest(Q/'inspect.py'),'binding':base,'cloud_targets':{'SAVES_REMOTE':'/ROCKNIX/Saves','SETTINGS_REMOTE':'/ROCKNIX/Backups','LAYOUT_KEEP':'/ROCKNIX/Saves'},'intended_image_tar_sha256':'b49cca4ca0b8996fa994181508c887d9df5afe155c9502919bab7bf7e153e39d'}
def writeplan(): (Q/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
writeplan();cmd=['python3','-I','-B',str(Q/'operation.py'),'apply','--plan',str(Q/'plan.json'),'--collector',str(Q/'inspect.py')]
results=[]
def record(name):results.append(name);print('PASS '+name,flush=True)
# Busy lease must refuse before creating the operational gate/archive.
f=open('/var/run/cloud_sync.lock','a');fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
p=run(cmd,1);assert not O.exists();f.close();record('held-transfer-lease-refuses-without-device-edits')
# A boot/config hash binding is mandatory; changing only plan is sufficient.
original_boot=base['boot_id'];plan['binding']['boot_id']='wrong-boot';writeplan();p=run(cmd,1);assert not O.exists();plan['binding']['boot_id']=original_boot;writeplan();record('stale-binding-refuses-before-gate')
# Fault after live cloud publication exercises exact executor rollback. It
# deliberately leaves frontend gated; only this fixture cleanup restarts ES0.
p=run(cmd+['--synthetic-fail','cloud-live'],1);assert 'synthetic interruption' in p.stderr,p.stderr
assert (O/'maintenance.active').exists();assert run(['systemctl','is-active','essway.service'],3).stdout.strip()=='inactive'
rollback=cmd.copy();rollback[4]='rollback';p=run(rollback)
assert (O/'rollback.json').exists()
for path in [S,S.with_name(S.name+'.backup'),C,CB,M]:assert I.metadata(path)==base['files'][str(path)]
assert I.tree(D)==base['scan'];assert I.tree(P('/storage/.cache/cloud_sync/replaced'))==base['local_recovery']
assert (O/'maintenance.active').exists();record('exact-executor-interruption-and-rollback-retains-gate-and-original-modes')
# Retain the failed run and restore solely synthetic fixture's frontend.
shutil.copytree(O,Q/'failed-operation')
shell('. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 0 cloudsaves.gameexit 0')
for u in ['essway.service','emustation.service']:
 p=P('/storage/.config/system.d')/(u+'.d');(p/'90-pixelelated-owner-alignment-519.conf').unlink();p.rmdir()
shutil.rmtree(O);shell('systemctl daemon-reload; systemctl unmask essway.service emustation.service; systemctl start essway.service');time.sleep(3)
shell('. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 1 cloudsaves.gameexit 1; chksysconfig backup')
plan['binding']=I.collect();writeplan()
p=run(cmd);assert (O/'acceptance.json').exists();a=json.loads((O/'acceptance.json').read_text())
assert a['accepted'];assert a['binding']['safe_payload']==base['safe_payload'];assert a['binding']['local_recovery']==base['local_recovery'];assert not (O/'maintenance.active').exists()
record('exact-executor-success-restores-frontend-and-removes-temporary-gates')
assert S.stat().st_mode&0o777==0o644 and C.stat().st_mode&0o777==0o644
assert S.read_bytes()==S.with_name(S.name+'.backup').read_bytes();assert C.read_bytes()==CB.read_bytes()
assert b'qa519.duplicate=first\nqa519.duplicate=last\n' in S.read_bytes()
record('private-archive-live-mode-preservation-and-unrelated-duplicate-retention')
(Q/'result.json').write_text(json.dumps({'passed':True,'checks':results,'operation_sha256':I.digest(Q/'operation.py'),'collector_sha256':I.digest(Q/'inspect.py'),'scope':'same executable uses invented alias/data; no private owner binding imported'},indent=2)+'\n')

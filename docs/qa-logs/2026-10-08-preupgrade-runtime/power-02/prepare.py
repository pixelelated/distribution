import pathlib,subprocess,json,hashlib,stat
P=pathlib.Path;Q=P('/storage/qa519');N=Q/'power2';N.mkdir(mode=0o700)
assert 'ee014909137e03706e0b3020b8396be589aaa705' in P('/etc/os-release').read_text()
def run(a):return subprocess.run(a,check=True,capture_output=True,text=True,timeout=30)
run(['systemctl','mask','emustation.service','essway.service']);run(['systemctl','stop','emustation.service','essway.service'])
S=P('/storage/.config/system/configs/system.cfg');C=P('/storage/.config/cloud_sync.conf');M=P('/storage/.config/cloud-layout-migration.json');D=P('/storage/.cache/cloud_sync/scan')
# Deliberately restore unsafe automatic settings to test the replacement guard
# BEFORE any alignment phases. No personal data exists in this VM.
run(['bash','-c','. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 1 cloudsaves.gameexit 1'])
run(['/usr/bin/chksysconfig','backup'])
C.write_bytes((Q/'archive-success/2').read_bytes());C.chmod(0o600)
C.with_name(C.name+'.bak').unlink()
M.write_bytes((Q/'archive-success/4').read_bytes());M.chmod(0o600)
import shutil
shutil.copytree(Q/'archive-success/5',D)
dropins={}
for u in ['emustation.service','essway.service']:
 d=P('/storage/.config/system.d')/(u+'.d');assert not d.exists();d.mkdir(mode=0o700)
 f=d/'90-qa519-maintenance.conf';f.write_text('[Unit]\nConditionPathExists=!/storage/qa519/maintenance.active\n');f.chmod(0o600);dropins[str(f)]=hashlib.sha256(f.read_bytes()).hexdigest()
(Q/'maintenance.active').write_text('qa519 synthetic controlled alignment\n');(Q/'maintenance.active').chmod(0o600)
run(['systemctl','daemon-reload']);run(['systemctl','unmask','emustation.service','essway.service']);run(['systemctl','start','essway.service'])
states={u:run(['systemctl','show',u,'-p','ActiveState','-p','ConditionResult','-p','UnitFileState']).stdout for u in ['emustation.service','essway.service']}
assert all('ActiveState=inactive' in v for v in states.values()),states
assert 'ConditionResult=no' in states['essway.service']
files={str(p):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)} for p in [C,M,P('/storage/.config/rclone/rclone.conf'),P('/storage/roms/savefiles/qa519.srm'),P('/storage/.cache/cloud_sync/replaced/qa519.srm')]}
(N/'settings-before').write_bytes(S.read_bytes());(N/'checkpoint.json').write_text(json.dumps({'boot':P('/proc/sys/kernel/random/boot_id').read_text().strip(),'files':files,'dropins':dropins,'settings_mode':stat.S_IMODE(S.stat().st_mode),'states':states,'auto_before':'1','guard':'persistent negative ConditionPathExists + private marker; independent of masks'},indent=2)+'\n')
run(['sync']);print('PASS conditional guard blocks actual frontend with auto1; durable power checkpoint ready',flush=True)

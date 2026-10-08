#!/usr/bin/env python3
import fcntl,hashlib,json,pathlib,stat,subprocess,time
P=pathlib.Path;Q=P('/storage/qa519');O=Q/'power';O.mkdir(mode=0o700)
before=json.loads((Q/'followup/power-checkpoint.json').read_text());now=P('/proc/sys/kernel/random/boot_id').read_text().strip()
assert now!=before['boot_id']
def run(a,ok=(0,)):
 p=subprocess.run(a,text=True,capture_output=True,timeout=30)
 if p.returncode not in ok:raise RuntimeError((a,p.returncode,p.stdout,p.stderr))
 return p
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def configs():return {s:{'sha256':h(P(s)),'mode':stat.S_IMODE(P(s).stat().st_mode)} for s in before['configs']}
assert configs()==before['configs']
states={u:run(['systemctl','show',u,'-p','ActiveState','-p','UnitFileState']).stdout for u in ['emustation.service','essway.service']}
assert all('UnitFileState=masked' in v and 'ActiveState=inactive' in v for v in states.values()),states
assert run(['pgrep','emulationstatio'],ok=(0,1)).returncode==1
for file,key in [('/storage/.config/rclone/rclone.conf','rclone_sha256'),('/storage/roms/savefiles/qa519.srm','save_sha256'),('/storage/.cache/cloud_sync/replaced/qa519.srm','recovery_sha256')]:assert h(P(file))==before[key]
with open('/var/run/cloud_sync.lock','a') as lock:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert run(['/usr/bin/cloud_migrate_layout','--needs-step'],ok=(1,)).returncode==1
observed=json.loads((Q/'observers.json').read_text())
for name,row in observed.items():
 target=P('/usr/bin')/name
 assert h(target)==row['executed_original_sha256'],name
 run(['mount','--bind',str(Q/'observe'/name),str(target)])
(Q/'calls.log').write_text('')
run(['systemctl','unmask','emustation.service','essway.service']);run(['systemctl','start','essway.service'])
for _ in range(120):
 p=run(['curl','-fsS','--max-time','1','http://127.0.0.1:1234/isIdle'],ok=tuple(range(128)))
 if p.returncode==0 and json.loads(p.stdout)==[True]:break
 time.sleep(.2)
else:raise RuntimeError('ES not idle after guarded recovery')
time.sleep(3)
trace=(Q/'calls.log').read_text()
assert 'cloud_migrate_layout --needs-step' in trace
assert not any(n in trace for n in ['cloud_net_ready','cloud_backup','cloud_restore','cloud_scan']),trace
assert configs()==before['configs']
states={u:run(['systemctl','show',u,'-p','ActiveState','-p','UnitFileState']).stdout for u in ['emustation.service','essway.service']}
assert 'UnitFileState=disabled' in states['emustation.service'] and 'ActiveState=inactive' in states['emustation.service']
assert 'UnitFileState=disabled' in states['essway.service'] and 'ActiveState=active' in states['essway.service']
for file,key in [('/storage/.config/rclone/rclone.conf','rclone_sha256'),('/storage/roms/savefiles/qa519.srm','save_sha256'),('/storage/.cache/cloud_sync/replaced/qa519.srm','recovery_sha256')]:assert h(P(file))==before[key]
result={'pass':True,'before_boot':before['boot_id'],'after_boot':now,'configs':configs(),'calls':trace,'restored_original_services':states,'protected_payloads_equal':True,'old_runtime_lease_lost_and_reacquired':True,'persistent_masks_survived_power_cycle':True,'unmodified_installed_helpers_verified_after_reboot':True,'scope':'power interruption after synchronized guarded state, followed by explicit recovery; not exhaustive flash fault timings'}
(O/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS actual power interruption retains guards; explicit ES recovery has no automatic transfer or migration scan',flush=True)

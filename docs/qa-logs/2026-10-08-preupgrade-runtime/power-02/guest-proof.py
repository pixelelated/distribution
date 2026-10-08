import ast,collections,errno,fcntl,hashlib,json,os,pathlib,re,shutil,stat,subprocess,sys,time
P=pathlib.Path;Q=P('/storage/qa519');N=Q/'power2';before=json.loads((N/'checkpoint.json').read_text())
assert P('/proc/sys/kernel/random/boot_id').read_text().strip()!=before['boot']
# Reuse the exact previously executed transaction functions; do not execute
# its fixture setup or other top-level actions again.
source=(N/'transaction-source.py').read_text();tree=ast.parse(source)
fnames={'run','sh','h','state','dump','atomic','edit','services','cloud_workers','wait_idle','stop','start','protected','fail','transaction'}
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in fnames]
assert {n.name for n in functions}==fnames
exec(compile(ast.Module(body=functions,type_ignores=[]),'qualified-transaction-functions','exec'))
C=P('/storage/.config/cloud_sync.conf');S=P('/storage/.config/system/configs/system.cfg');M=P('/storage/.config/cloud-layout-migration.json');D=P('/storage/.cache/cloud_sync/scan');UNITS=['emustation.service','essway.service']
for s,x in before['files'].items():assert h(P(s))==x['sha256'] and stat.S_IMODE(P(s).stat().st_mode)==x['mode'],s
for s,x in before['dropins'].items():assert h(P(s))==x,s
assert (Q/'maintenance.active').is_file()
def assignments(data):return [l for l in data.decode().splitlines() if l and not l.startswith('#')]
a=assignments((N/'settings-before').read_bytes());b=assignments(S.read_bytes())
assert collections.Counter(a)==collections.Counter(b),'unaccounted setting addition/removal'
def effective(lines):return dict(l.split('=',1) for l in lines)
assert effective(a)==effective(b) and effective(b)['cloudsaves.startup']=='1'
assert stat.S_IMODE(S.stat().st_mode)==before['settings_mode']
states={u:run(['systemctl','show',u,'-p','ActiveState','-p','ConditionResult','-p','UnitFileState']).stdout for u in UNITS}
assert all('ActiveState=inactive' in s for s in states.values()),states
assert 'UnitFileState=disabled' in states['essway.service'] and 'ConditionResult=no' in states['essway.service'],states
assert run(['pgrep','emulationstatio'],ok=(0,1)).returncode==1
assert not cloud_workers(),cloud_workers()
print('PASS actual reboot unmasks essway but persistent condition prevents frontend/automatic startup with auto1',flush=True)
# Boot ID and byte changes invalidate the old action receipt. Create a fresh
# observed binding only after this qualified recovery; never waive drift.
paths=[S,S.with_name(S.name+'.backup'),C,C.with_name(C.name+'.bak'),M,D]
baseline={str(p):state(p) for p in paths};guarded_payload=protected()
stop();archive=transaction('power2-resume')
accepted={str(p):state(p) for p in paths}
observed=json.loads((Q/'observers.json').read_text())
for name,row in observed.items():
 target=P('/usr/bin')/name;assert h(target)==row['executed_original_sha256']
 run(['mount','--bind',str(Q/'observe'/name),str(target)])
(Q/'calls.log').write_text('')
# The marker is removed last, after exact guard readback and removal of only
# the named, hash-matched drop-ins. A failed removal keeps the gate closed.
for s,x in before['dropins'].items():
 p=P(s);assert h(p)==x;p.unlink();p.parent.rmdir()
run(['systemctl','daemon-reload']);(Q/'maintenance.active').unlink()
start();time.sleep(3)
trace=(Q/'calls.log').read_text()
assert 'cloud_migrate_layout --needs-step' in trace
assert not any(n in trace for n in ['cloud_net_ready','cloud_backup','cloud_restore','cloud_scan']),trace
assert {str(p):state(p) for p in paths}==accepted and protected()==guarded_payload
states_final=services();assert 'ActiveState=active' in states_final['essway.service'] and 'ActiveState=inactive' in states_final['emustation.service']
assert all('UnitFileState=disabled' in x for x in states_final.values())
assert all(not P(p).exists() for p in before['dropins']) and not (Q/'maintenance.active').exists()
(N/'result.json').write_text(json.dumps({'pass':True,'actual_boot_changed':True,'auto1_blocked_before_alignment':True,'boot_unmask_observed':True,'condition_result_before':states,'new_state_binding_required':True,'settings_assignment_multiset_and_effective_values_preserved_across_boot':True,'protected_equal':True,'qualified_transaction_source_sha256':hashlib.sha256(source.encode()).hexdigest(),'after':accepted,'calls':trace,'restored_original_service_states':states_final,'temporary_dropins_marker_removed':True,'scope':'power loss at durable pre-alignment guard, then explicit rebind/transaction/guarded restart; not exhaustive flash fault timings'},indent=2)+'\n')
print('PASS interrupted alignment recovered; exact transaction and ES restart preserve data and remove temporary startup gate',flush=True)

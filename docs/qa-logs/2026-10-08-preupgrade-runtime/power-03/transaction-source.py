#!/usr/bin/env python3
"""Synthetic-only installed-old-source transaction/runtime proof for #519.

Refuses anything except the exact GENERIC_X64 QA guest and its invented alias.
This is a rehearsal, not a device alignment utility.
"""
import errno, fcntl, hashlib, json, os, pathlib, re, shutil, stat, subprocess, sys, time
P=pathlib.Path
Q=P('/storage/qa519')
C=P('/storage/.config/cloud_sync.conf')
S=P('/storage/.config/system/configs/system.cfg')
M=P('/storage/.config/cloud-layout-migration.json')
D=P('/storage/.cache/cloud_sync/scan')
UNITS=['emustation.service','essway.service']
RESULTS=[]

def run(args, ok=(0,), **kw):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=90,**kw)
    if p.returncode not in ok: raise RuntimeError((args,p.returncode,p.stdout))
    return p
def sh(s,ok=(0,)): return run(['bash','-c',s],ok)
def record(name,detail):
    RESULTS.append({'name':name,'pass':True,'detail':detail})
    (Q/'results.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
    print('PASS '+name,flush=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state(p):
    if p.is_symlink():return {'symlink':os.readlink(p)}
    if not p.exists():return None
    if p.is_dir():return {'directory':True,'mode':stat.S_IMODE(p.stat().st_mode),'entries':{x.name:state(x) for x in sorted(p.iterdir())}}
    return {'sha256':h(p),'mode':stat.S_IMODE(p.stat().st_mode),'bytes':p.stat().st_size}
def dump(n,v): (Q/n).write_text(json.dumps(v,indent=2)+'\n')
def settings(a):
    run(['bash','-c','. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup "$1" cloudsaves.gameexit "$1"','qa',a])
    run(['/usr/bin/chksysconfig','backup'])
def atomic(p,b,mode=0o600):
    assert not p.is_symlink() and (not p.exists() or p.is_file()), str(p)
    t=p.with_name(p.name+'.qa519-new')
    fd=os.open(t,os.O_WRONLY|os.O_CREAT|os.O_EXCL,mode)
    try:
        with os.fdopen(fd,'wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
        os.chmod(t,mode);os.replace(t,p)
        fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
    finally:
        if t.exists():t.unlink()
def edit(data,pairs):
    text=data.decode();assert text.endswith('\n')
    for key,value in pairs.items():
        text,n=re.subn('^'+re.escape(key)+'=.*$',key+'="'+value+'"',text,flags=re.M)
        assert n==1,(key,n)
    return text.encode()
def services():
    return {u:run(['systemctl','show',u,'-p','ActiveState','-p','SubState','-p','MainPID','-p','UnitFileState','-p','KillMode','-p','Restart']).stdout for u in UNITS}
def cloud_workers():
    found=[]
    for p in P('/proc').glob('[0-9]*'):
        try:
            s=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
            if any(t in s for t in ('/usr/bin/cloud_','/storage/qa519/original/cloud_','/storage/qa519/original/rclone')):
                found.append({'pid':int(p.name),'argv':s})
        except (OSError,ProcessLookupError):pass
    return found
def wait_idle():
    for _ in range(100):
        p=run(['curl','-fsS','--max-time','2','http://127.0.0.1:1234/isIdle'],ok=tuple(range(128)))
        if p.returncode==0 and json.loads(p.stdout)==[True]:return
        time.sleep(.2)
    raise RuntimeError('actual ES did not become idle')
def stop():
    run(['systemctl','mask',*UNITS]);run(['systemctl','stop',*UNITS])
    for _ in range(100):
        if not cloud_workers():break
        time.sleep(.1)
    assert not cloud_workers(),cloud_workers()
    assert run(['pgrep','emulationstatio'],ok=(0,1)).returncode==1
def start():
    run(['systemctl','unmask',*UNITS]);run(['systemctl','start','essway.service']);wait_idle()
def protected():return {str(p):state(p) for p in (Q/'cloud',P('/storage/roms/savefiles/qa519.srm'),P('/storage/.cache/cloud_sync/replaced/qa519.srm'),P('/storage/.config/rclone/rclone.conf'))}

assert 'BUILD_ID="ee014909137e03706e0b3020b8396be589aaa705"' in P('/etc/os-release').read_text()
assert 'GENERIC_X64' in P('/etc/os-release').read_text()
assert sys.argv[1]=='--synthetic-only'
Q.mkdir(mode=0o700,exist_ok=False)
dump('initial-services.json',services())
assert 'ActiveState=active' in services()['essway.service']
assert not P('/storage/.config/rclone/rclone.conf').exists()
stop()
record('actual-frontend-stopped-and-persistently-masked',services())
assert run(['systemctl','start','essway.service'],ok=(1,)).returncode==1
record('masked-frontend-refuses-start','actual installed essway.service')

# Only synthetic content is introduced. No host or owner file is imported.
for p in (Q/'cloud/ROCKNIX/Saves/savefiles',Q/'cloud/ROCKNIX/Backups',Q/'cloud/ROCKNIX/Content',Q/'cloud/pixelelated/Saves',Q/'cloud/pixelelated/Backups',P('/storage/roms/savefiles'),P('/storage/.cache/cloud_sync/replaced'),P('/storage/.config/rclone')):p.mkdir(parents=True,exist_ok=True)
for p in (Q/'cloud/ROCKNIX/Saves/savefiles/qa519.srm',P('/storage/roms/savefiles/qa519.srm')):p.write_bytes(b'qa519 invented game progress\n')
P('/storage/.cache/cloud_sync/replaced/qa519.srm').write_bytes(b'qa519 invented recovery version\n')
rconf=P('/storage/.config/rclone/rclone.conf');rconf.write_text('[qa519]\ntype = alias\nremote = /storage/qa519/cloud\n');rconf.chmod(0o600)
original_cfg=C.read_bytes()
atomic(C,edit(original_cfg,{'SAVES_REMOTE':'/ROCKNIX/Saves','SETTINGS_REMOTE':'/ROCKNIX/Backups','CONTENT_REMOTE':'/ROCKNIX/Content','LAYOUT_KEEP':'/ROCKNIX/Saves'}))
settings('0')

# Observe real helpers; their byte-identical bodies and real rclone still run.
(Q/'original').mkdir();(Q/'observe').mkdir();observed={}
names=['cloud_net_ready','cloud_migrate_layout','cloud_scan','cloud_backup','cloud_restore','rclone']
for name in names:
    src=P('/usr/bin')/name;orig=Q/'original'/name;shutil.copy2(src,orig)
    assert h(src)==h(orig)
    wrapper=Q/'observe'/name
    wrapper.write_text('#!/bin/bash\nprintf "%s %s\\n" '+name+' "$*" >> /storage/qa519/calls.log\nexec /storage/qa519/original/'+name+' "$@"\n')
    wrapper.chmod(0o700);run(['mount','--bind',str(wrapper),str(src)])
    observed[name]={'executed_original_sha256':h(orig),'observer_sha256':h(wrapper)}
dump('observers.json',observed)
run(['/usr/bin/rclone','cat','qa519:/ROCKNIX/Saves/savefiles/qa519.srm'])
record('real-rclone-positive-observation', (Q/'calls.log').read_text())

# A synchronous ES start hook edits the disk after SystemConf has loaded1.
# Seeing cloud_net_ready proves real ES kept the cached value, not just source intent.
lease=open('/var/run/cloud_sync.lock','a');fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
settings('1')
hook=P('/storage/.config/emulationstation/scripts/start/qa519-disk-auto0.sh');hook.parent.mkdir(parents=True,exist_ok=True)
hook.write_text('#!/bin/bash\n. /etc/profile >/dev/null 2>&1\nset_settings cloudsaves.startup 0 cloudsaves.gameexit 0\nprintf "disk-now-auto0\\n" >> /storage/qa519/calls.log\n');hook.chmod(0o700)
(Q/'calls.log').write_text('')
start()
for _ in range(700):
    trace=(Q/'calls.log').read_text()
    if 'cloud_net_ready --wait 60' in trace:break
    time.sleep(.1)
assert 'disk-now-auto0' in trace and 'cloud_net_ready --wait 60' in trace,trace
assert 'cloudsaves.startup=0\n' in S.read_text()
record('actual-ES-cached1-survives-external-disk0',trace)
# Let the worker finish by its own bound; never kill a potentially active transfer.
for _ in range(750):
    if not cloud_workers():break
    time.sleep(.1)
assert not cloud_workers(),cloud_workers()
stop();hook.unlink();hook.parent.rmdir();hook.parent.parent.rmdir()
fcntl.flock(lease,fcntl.LOCK_UN);lease.close()

# Freeze the exact invented pre-alignment state, including duplicate unrelated
# assignments and a last-good copy. These bytes must survive every rollback.
settings('1');atomic(S,S.read_bytes()+b'qa519.duplicate=first\nqa519.duplicate=last\n');run(['/usr/bin/chksysconfig','backup'])
atomic(C,edit(original_cfg,{'SAVES_REMOTE':'/pixelelated/Saves','SETTINGS_REMOTE':'/pixelelated/Backups','CONTENT_REMOTE':'/ROCKNIX/Content','LAYOUT_KEEP':''}))
if C.with_name(C.name+'.bak').exists():C.with_name(C.name+'.bak').unlink()
M.write_text('{"schema":1,"step":1,"stage":"discarded"}\n');M.chmod(0o600)
if D.exists():shutil.rmtree(D) # disposable fixture only, before baseline
D.mkdir(parents=True);(D/'join').write_bytes(b'');(D/'state').write_text('qa519 synthetic stale scan\n')
paths=[S,S.with_name(S.name+'.backup'),C,C.with_name(C.name+'.bak'),M,D]
baseline={str(p):state(p) for p in paths};guarded_payload=protected()
orig=Q/'baseline';orig.mkdir(mode=0o700)
for i,p in enumerate(paths):
    if p.is_dir():shutil.copytree(p,orig/str(i))
    elif p.exists():shutil.copy2(p,orig/str(i))
dump('baseline.json',baseline)
def restore_baseline():
    for i,p in enumerate(paths):
        if p.is_symlink() or p.is_file():p.unlink()
        elif p.exists():shutil.rmtree(p)
        x=orig/str(i)
        if x.is_dir():shutil.copytree(x,p)
        elif x.exists():shutil.copy2(x,p)
    assert {str(p):state(p) for p in paths}==baseline
    assert protected()==guarded_payload
def fail(tag,requested):
    if tag==requested:raise OSError(errno.EIO,'deliberate boundary failure: '+tag)
def transaction(case,expected=None):
    archive=Q/('archive-'+case);archive.mkdir(mode=0o700)
    with open('/var/run/cloud_sync.lock','a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        assert not cloud_workers()
        for p in ('/storage/.config/.restore-in-progress','/storage/.config/.restore-reverted','/storage/.config/.cloud-journey-pending','/storage/.cache/cloud_sync/journey-tiers'):
            assert not P(p).exists(),p
        assert {str(p):state(p) for p in paths}==(expected or baseline),'state drift'
        assert all('ActiveState=inactive' in v and 'UnitFileState=masked' in v for v in services().values())
        fail('before-archive',case)
        for i,p in enumerate(paths):
            if p.is_dir():shutil.copytree(p,archive/str(i))
            elif p.exists():shutil.copy2(p,archive/str(i))
        assert {str(p):state(archive/str(i)) for i,p in enumerate(paths)}==baseline
        fail('archived',case)
        before=S.read_bytes();mode=stat.S_IMODE(S.stat().st_mode)
        # Actual installed atomic writer, never a replacement implementation.
        run(['bash','-c','. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 0 cloudsaves.gameexit 0'])
        strip=lambda b:b''.join(l for l in b.splitlines(keepends=True) if not l.startswith((b'cloudsaves.startup=',b'cloudsaves.gameexit=')))
        assert strip(before)==strip(S.read_bytes()) and stat.S_IMODE(S.stat().st_mode)==mode
        fail('settings-live',case)
        run(['/usr/bin/chksysconfig','backup']);assert state(S)==state(S.with_name(S.name+'.backup'))
        fail('settings-fallback',case)
        new=edit(C.read_bytes(),{'SAVES_REMOTE':'/ROCKNIX/Saves','SETTINGS_REMOTE':'/ROCKNIX/Backups','LAYOUT_KEEP':'/ROCKNIX/Saves'})
        atomic(C,new);fail('cloud-live',case)
        atomic(C.with_name(C.name+'.bak'),new);fail('cloud-fallback',case)
        assert run(['/usr/bin/cloud_migrate_layout','--needs-step'],ok=(0,1)).returncode==0 # existing pending record wins until archival
        os.rename(M,archive/'retired-migration');fail('migration-archived',case)
        os.rename(D,archive/'retired-scan');fail('scan-archived',case)
        assert run(['/usr/bin/cloud_migrate_layout','--needs-step'],ok=(1,)).returncode==1
        assert protected()==guarded_payload
    return archive
for phase in ['before-archive','archived','settings-live','settings-fallback','cloud-live','cloud-fallback','migration-archived','scan-archived']:
    try:transaction(phase)
    except OSError as e:assert e.errno==errno.EIO
    else:raise AssertionError('fault not injected')
    assert protected()==guarded_payload
    assert all('UnitFileState=masked' in v for v in services().values())
    dump('interrupted-'+phase+'.json',{str(p):state(p) for p in paths})
    restore_baseline();record('interruption-and-exact-rollback-'+phase,{'protected_equal':True,'config_records_and_modes_restored':True,'frontend_remained_masked':True})

# Refusal controls: active lease, recovery marker, drift, and unsafe atomic target.
held=open('/var/run/cloud_sync.lock','a');fcntl.flock(held,fcntl.LOCK_EX|fcntl.LOCK_NB)
try:transaction('lease-held')
except BlockingIOError:pass
else:raise AssertionError('lease not respected')
held.close();record('active-lease-refuses-before-change', {str(p):state(p) for p in paths}==baseline)
marker=P('/storage/.config/.restore-in-progress');marker.write_text('qa519-preserve-me\n')
try:transaction('recovery-marker')
except AssertionError as e:assert str(marker) in str(e)
else:raise AssertionError('unknown recovery accepted')
assert marker.read_text()=='qa519-preserve-me\n';marker.unlink();record('active-recovery-refuses-preserved',True)
atomic(C,C.read_bytes()+b'# intervening edit\n')
try:transaction('drift')
except AssertionError as e:assert 'state drift' in str(e)
else:raise AssertionError('drift accepted')
restore_baseline();record('configuration-drift-invalidates-plan',True)
target=Q/'must-stay';target.write_bytes(b'untouched');link=Q/'unsafe';link.symlink_to(target)
try:atomic(link,b'bad')
except AssertionError:pass
else:raise AssertionError('symlink followed')
assert target.read_bytes()==b'untouched';record('atomic-symlink-target-refuses',True)

archive=transaction('success');record('complete-reversible-transaction',{'archive':str(archive),'protected_equal':protected()==guarded_payload})
accepted={str(p):state(p) for p in paths};dump('accepted-before-restart.json',accepted)
# Damaged settings recover from the newly aligned last-good record using the
# actual installed recovery command. This deliberately runs only on synthetic data.
atomic(S,b'broken without newline');run(['/usr/bin/chksysconfig','restore'])
assert state(S)==accepted[str(S)];record('aligned-settings-fallback-recovers-auto0',True)

(Q/'calls.log').write_text('')
start()
time.sleep(3)
trace=(Q/'calls.log').read_text();dump('guarded-restart-calls.json',trace)
assert not any(n in trace for n in ['cloud_net_ready','cloud_backup','cloud_restore','cloud_scan']),trace
assert 'cloud_migrate_layout --needs-step' in trace,trace
assert {str(p):state(p) for p in paths}==accepted
assert protected()==guarded_payload and not cloud_workers()
record('actual-ES-guarded-restart-no-automatic-transfer-or-folder-scan',{'calls':trace,'services':services(),'protected_equal':True})
dump('final.json',{'checks':len(RESULTS),'passed':True,'scope':'synthetic live VM transaction and restart; injected boundary interruptions are not abrupt host power cuts','cloud_fallback_consumer_not_exercised':True,'detached_KillMode_process_control_not_exercised':True,'guest_retention':'immediate follow-up power/failure controls only; no device authority'})

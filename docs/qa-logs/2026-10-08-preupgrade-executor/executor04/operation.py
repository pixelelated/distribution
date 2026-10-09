#!/usr/bin/env python3
"""One-time #519 local owner alignment. Never runs a remote transfer.

The private plan binds this exact executable and collector. Apply refuses
state drift. Failure retains a durable frontend gate; rollback restores original
config/records under that gate, deliberately without restarting automatic sync.
This is an operational packet, not a shipped migration feature.
"""
import argparse,fcntl,hashlib,importlib.util,json,os,pathlib,re,shutil,stat,subprocess,sys,time
P=pathlib.Path
O=P('/storage/.cache/pixelelated-owner-alignment-519')
S=P('/storage/.config/system/configs/system.cfg');SB=S.with_name(S.name+'.backup')
C=P('/storage/.config/cloud_sync.conf');CB=C.with_name(C.name+'.bak')
M=P('/storage/.config/cloud-layout-migration.json');D=P('/storage/.cache/cloud_sync/scan')
UNITS=['emustation.service','essway.service']
GATE=O/'maintenance.active'
DROP={u:P('/storage/.config/system.d')/(u+'.d')/'90-pixelelated-owner-alignment-519.conf' for u in UNITS}
GATE_BYTES=b'pixelelated owner alignment #519\n'
DROP_BYTES=('[Unit]\nConditionPathExists=!'+str(GATE)+'\n').encode()
MUTABLE=[S,SB,C,CB,M,D]

def check(test,label):
    if not test:raise RuntimeError(label)
def run(args,ok=(0,),**kw):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90,**kw)
    check(p.returncode in ok,'command refused: '+args[0]+' rc='+str(p.returncode))
    return p

def fsyncdir(p):
    fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def parents_safe(p):
    for q in [p]+list(p.parents):check(not q.is_symlink(),'symlink refuses')
def atomic(p,data,mode):
    parents_safe(p);check(not p.exists() or p.is_file(),'non-file refuses')
    t=p.with_name(p.name+'.519-new')
    fd=os.open(t,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode)
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(data);f.flush();os.fchmod(f.fileno(),mode);os.fsync(f.fileno())
        os.replace(t,p);fsyncdir(p.parent)
    finally:
        if t.exists():t.unlink()
def dump(p,data):atomic(p,(json.dumps(data,indent=2)+'\n').encode(),0o600)
def strip(data,keys):
    prefixes=tuple(k.encode()+b'=' for k in keys)
    return b''.join(l for l in data.splitlines(keepends=True) if not l.startswith(prefixes))
def edit(data,values):
    text=data.decode();check(text.endswith('\n'),'missing trailing newline')
    for k,v in values.items():
        check(re.fullmatch(r'[A-Z_]+',k) and re.fullmatch(r'/[A-Za-z0-9/]+',v),'invalid fixed target')
        text,n=re.subn('^'+re.escape(k)+'=.*$',k+'="'+v+'"',text,flags=re.M)
        check(n==1,'target assignment count')
    return text.encode()
def settings0():
    before=S.read_bytes();mode=stat.S_IMODE(S.stat().st_mode)
    run(['bash','-c','. /etc/profile >/dev/null 2>&1; set_settings cloudsaves.startup 0 cloudsaves.gameexit 0'],umask=0o022)
    check(strip(before,['cloudsaves.startup','cloudsaves.gameexit'])==strip(S.read_bytes(),['cloudsaves.startup','cloudsaves.gameexit']),'unrelated setting drift')
    check(stat.S_IMODE(S.stat().st_mode)<=0o777 and stat.S_IMODE(S.stat().st_mode)==mode,'settings mode drift')
    check(I.settings()=={'automatic_sync':{'cloudsaves.startup':['0'],'cloudsaves.gameexit':['0']},'startup_game_configured':False},'automatic guard mismatch')
    run(['/usr/bin/chksysconfig','backup'],umask=0o022);check(I.metadata(S)==I.metadata(SB),'fallback differs')
def services():
    result={}
    for u in UNITS:
        raw=run(['systemctl','show',u,'-p','ActiveState','-p','SubState','-p','MainPID','-p','UnitFileState','-p','KillMode','-p','Restart','-p','FragmentPath','-p','DropInPaths','-p','Conditions']).stdout.decode()
        result[u]=dict(l.split('=',1) for l in raw.splitlines() if '=' in l)
    return result

def workers():
    found=[]
    for p in P('/proc').glob('[0-9]*'):
        try:
            if int(p.name)==os.getpid():continue
            cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ');comm=(p/'comm').read_text().strip()
            if comm=='rclone' or b'/usr/bin/cloud_' in cmd or b'/original/cloud_' in cmd:found.append(int(p.name))
        except (FileNotFoundError,ProcessLookupError):pass
    return found

def stable_snapshot(n):
    return {k:v for k,v in n.items() if k not in ['elapsed_seconds']}
def lease():
    p='/var/run/cloud_sync.lock';fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_NOFOLLOW,0o600)
    fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    check(os.fstat(fd).st_ino==os.stat(p).st_ino,'lease replaced')
    return fd

def prepare_gate():
    for p in DROP.values():
        parents_safe(p);check(not p.exists(),'gate path already occupied')
        check(not p.parent.exists(),'unexpected frontend drop-in directory')
    check(not O.exists(),'operation archive already exists');parents_safe(O)
    O.mkdir(mode=0o700);fsyncdir(O.parent)
    dump(O/'plan.json',PLAN)
    atomic(GATE,GATE_BYTES,0o600)
    for p in DROP.values():
        p.parent.mkdir(mode=0o755);fsyncdir(p.parent.parent)
        atomic(p,DROP_BYTES,0o644)
    os.sync();run(['systemctl','daemon-reload'])
    for u,v in services().items():
        check(str(DROP[u]) in v['DropInPaths'] and DROP_BYTES in run(['systemctl','cat',u]).stdout,'gate not loaded')

def quiesce():
    check(not workers(),'active cloud worker')
    run(['systemctl','mask',*UNITS]);run(['systemctl','stop',*UNITS])
    deadline=time.monotonic()+12
    while workers() and time.monotonic()<deadline:time.sleep(.2)
    check(not workers(),'detached worker remains')
    for v in services().values():check(v['ActiveState']=='inactive' and v['UnitFileState']=='masked','frontend not quiescent')
    p=run(['pgrep','emulationstatio'],ok=(0,1));check(p.returncode==1,'ES process remains')

def protected():
    # Uses the installed local-only filter, never personal remote credentials.
    n=I.collect(frontend=False)
    mutable={str(p) for p in MUTABLE}
    return {'boot_id':n['boot_id'],'files':{k:v for k,v in n['files'].items() if k not in mutable},'safe_payload':n['safe_payload'],'local_recovery':n['local_recovery'],'hooks':n['hooks'],'markers':n['markers']}
def baseline_protected():
    n=PLAN['binding'];mutable={str(p) for p in MUTABLE}
    return {'boot_id':n['boot_id'],'files':{k:v for k,v in n['files'].items() if k not in mutable},'safe_payload':n['safe_payload'],'local_recovery':n['local_recovery'],'hooks':n['hooks'],'markers':n['markers']}
def archive():
    A=O/'originals';A.mkdir(mode=0o700)
    for i,p in enumerate(MUTABLE):
        if not p.exists():continue
        dest=A/str(i)
        if p.is_dir():
            shutil.copytree(p,dest)
            for q in [dest]+list(dest.rglob('*')):q.chmod(0o700 if q.is_dir() else 0o600)
        else:
            with dest.open('xb') as f:f.write(p.read_bytes())
            dest.chmod(0o600)
        # Content is checked independently; original modes remain in the binding.
        verify_archive(i,p,dest)
    os.sync();dump(O/'archive-complete.json',{'complete':True})
def verify_archive(i,p,dest):
    if p.is_file():check(I.digest(p)==I.digest(dest),'archive mismatch')
    else:
        a=I.tree(p);b=I.tree(dest)
        check(set(a['entries'])==set(b['entries']),'archive tree mismatch')
        for k,v in a['entries'].items():
            if v['kind']=='file':check(v['sha256']==b['entries'][k]['sha256'],'archive content mismatch')
def expected_state():
    return {str(p): I.tree(p) if p==D else I.metadata(p) for p in MUTABLE}
def align():
    settings0();phase('settings')
    new=edit(C.read_bytes(),PLAN['cloud_targets'])
    cmode=PLAN['binding']['files'][str(C)]['mode']
    atomic(C,new,cmode);phase('cloud-live')
    b=PLAN['binding']['files'][str(CB)]
    atomic(CB,new,b['mode'] if b['kind']=='file' else cmode);phase('cloud-fallback')
    check(C.read_bytes()==CB.read_bytes(),'cloud fallback mismatch')
    for p,name in [(M,'retired-migration'),(D,'retired-scan')]:
        check(p.exists() and not p.is_symlink(),'missing exact stale record')
        os.rename(p,O/name);fsyncdir(p.parent);fsyncdir(O);phase(name)
    check(run(['/usr/bin/cloud_migrate_layout','--needs-step'],ok=(0,1)).returncode==1,'old migration still pending')
    check(protected()==baseline_protected(),'protected state drift')
    dump(O/'aligned.json',expected_state());os.sync()

def phase(name):
    dump(O/'phase.json',{'phase':name})
    if ARGS.synthetic_fail==name:
        check('GENERIC_X64' in P('/etc/os-release').read_text(),'fault injection restricted to VM')
        raise RuntimeError('synthetic interruption '+name)
def release_gate():
    check(GATE.read_bytes()==GATE_BYTES,'maintenance marker drift')
    for p in DROP.values():
        check(p.is_file() and not p.is_symlink() and p.read_bytes()==DROP_BYTES,'drop-in drift')
        check(list(p.parent.iterdir())==[p],'unexpected drop-in sibling')
    for p in DROP.values():p.unlink();p.parent.rmdir();fsyncdir(p.parent.parent)
    GATE.unlink();fsyncdir(O);run(['systemctl','daemon-reload'])
    run(['systemctl','unmask',*UNITS])
    for u,v in PLAN['binding']['units'].items():
        check(v['UnitFileState']=='disabled','unexpected original enable state')
        if v['ActiveState']=='active':run(['systemctl','start',u])
    deadline=time.monotonic()+30
    while time.monotonic()<deadline:
        r=run(['curl','-fsS','--max-time','2','http://127.0.0.1:1234/isIdle'],ok=tuple(range(128)))
        if r.returncode==0 and json.loads(r.stdout)==[True]:break
        time.sleep(.25)
    else:raise RuntimeError('frontend not idle after restart')
    time.sleep(3)
    check(not workers(),'unexpected worker after restart')
    check(protected()==baseline_protected(),'post-restart protected drift')
    check(expected_state()==json.loads((O/'aligned.json').read_text()),'post-restart aligned drift')
    for u,v in services().items():
        old=PLAN['binding']['units'][u]
        check(all(v[k]==old[k] for k in ['ActiveState','SubState','UnitFileState','KillMode','Restart','FragmentPath']),'frontend state not restored')
    n=I.collect();check(n['unit_overrides']==PLAN['binding']['unit_overrides'],'unit override residue')
    dump(O/'acceptance.json',{'accepted':True,'scope':'one-time local alignment; no firmware update, cloud transfer or automatic-sync reenable','image_sha256':PLAN['intended_image_tar_sha256'],'operation_sha256':I.digest(P(__file__)),'collector_sha256':I.digest(ARGS.collector),'binding':n})

def retain_gate():
    if not O.exists():return
    atomic(GATE,GATE_BYTES,0o600)
    for p in DROP.values():
        if not p.parent.exists():p.parent.mkdir(mode=0o755)
        if p.exists():check(p.read_bytes()==DROP_BYTES,'foreign drop-in refuses recovery overwrite')
        else:atomic(p,DROP_BYTES,0o644)
    os.sync();run(['systemctl','daemon-reload'])
    run(['systemctl','mask',*UNITS]);run(['systemctl','stop',*UNITS])

def rollback():
    check((O/'archive-complete.json').exists(),'no complete archive; retain gate and inspect')
    retain_gate();check(not workers(),'worker blocks rollback')
    for i,p in enumerate(MUTABLE):
        old=PLAN['binding']['scan'] if p==D else PLAN['binding']['files'][str(p)]
        kind=old['root']['kind'] if p==D else old['kind'];a=O/'originals'/str(i)
        if kind=='absent':
            if p.exists():
                check(p==CB and p.is_file() and not p.is_symlink(),'refuse unknown absent-target cleanup')
                # Preserve even the partial aligned fallback for diagnosis.
                os.rename(p,O/'rollback-created-fallback');fsyncdir(p.parent);fsyncdir(O)
        elif kind=='file':
            check(I.digest(a)==old['sha256'],'archived file drift')
            atomic(p,a.read_bytes(),old['mode'])
        elif p==D:
            if p.exists():check(I.tree(p)==old,'unexpected current scan')
            else:
                retired=O/'retired-scan';check(I.tree(retired)==old,'retired scan drift')
                os.rename(retired,p);fsyncdir(p.parent);fsyncdir(O)
        else:raise RuntimeError('unclassified restore target')
    check(protected()==baseline_protected(),'rollback protected drift')
    check(expected_state()=={str(p):(PLAN['binding']['scan'] if p==D else PLAN['binding']['files'][str(p)]) for p in MUTABLE},'rollback state mismatch')
    dump(O/'rollback.json',{'original_state_restored':True,'frontend_gate_retained':True,'automatic_sync_not_restarted':True})
    os.sync()

def main():
    global I,PLAN,ARGS
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['apply','rollback']);ap.add_argument('--plan',type=P,required=True);ap.add_argument('--collector',type=P,required=True);ap.add_argument('--synthetic-fail',choices=['settings','cloud-live','cloud-fallback','retired-migration','retired-scan']);ARGS=ap.parse_args()
    check(os.geteuid()==0,'root required');os.umask(0o077)
    PLAN=json.loads(ARGS.plan.read_text());check(PLAN['schema']==1,'plan schema')
    check(hashlib.sha256(P(__file__).read_bytes()).hexdigest()==PLAN['operation_sha256'],'operation source changed')
    check(hashlib.sha256(ARGS.collector.read_bytes()).hexdigest()==PLAN['collector_sha256'],'collector source changed')
    sp=importlib.util.spec_from_file_location('inspect519',ARGS.collector);I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    if ARGS.synthetic_fail:check('GENERIC_X64' in P('/etc/os-release').read_text(),'fault injection requires VM')
    check(PLAN['cloud_targets']=={'SAVES_REMOTE':'/ROCKNIX/Saves','SETTINGS_REMOTE':'/ROCKNIX/Backups','LAYOUT_KEEP':'/ROCKNIX/Saves'},'target contract drift')
    lock=lease()
    try:
        if ARGS.action=='rollback':
            check(json.loads((O/'plan.json').read_text())==PLAN,'archive plan differs')
            rollback();print('PASS originals restored; maintenance gate remains; no frontend restart',flush=True);return
        check(not O.exists(),'archive exists; inspect, never overwrite')
        n=I.collect();check(stable_snapshot(n)==stable_snapshot(PLAN['binding']),'fresh binding differs')
        check(n['frontend_idle']==[True] and not workers() and not n['busy_cloud_processes'],'device not quiescent')
        check(not n['settings']['startup_game_configured'],'startup game configured')
        check(all(v['kind']=='absent' for v in n['markers'].values()),'recovery marker blocks')
        check(all(v['root']['kind']=='absent' for v in n['hooks'].values()),'custom hook blocks')
        check(n['settings']['automatic_sync']=={'cloudsaves.startup':['1'],'cloudsaves.gameexit':['1']},'unexpected original automation')
        check(set(n['scan']['entries'])=={'join','state'},'scan scope drift')
        check(all(v['UnitFileState']=='disabled' and v['DropInPaths']=='' for v in n['units'].values()),'unexpected service config')
        check(n['units']['essway.service']['ActiveState']=='active' and n['units']['emustation.service']['ActiveState']=='inactive','unexpected frontend selection')
        try:
            prepare_gate();quiesce();check(protected()==baseline_protected(),'state drift after quiescence')
            check(expected_state()=={str(p):(n['scan'] if p==D else n['files'][str(p)]) for p in MUTABLE},'mutable state drift after quiescence')
            archive();align();release_gate();print('PASS exact local alignment accepted; automatic sync remains off',flush=True)
        except BaseException:
            retain_gate();raise
    finally:os.close(lock)
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('REFUSED '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)

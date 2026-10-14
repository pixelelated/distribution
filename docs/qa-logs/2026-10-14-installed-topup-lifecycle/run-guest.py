#!/usr/bin/env python3
"""One installed567 fixture command; original adapter bytes and product paths stay unchanged."""
import ctypes,hashlib,json,os,re,resource,shutil,signal,stat,subprocess,sys,tarfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from census import direct_children,signal_child
OUT=Path('/tmp/pix-output/installed567');PACKET=Path('/run/pix567-installed-packet')
BINDING=Path('/run/pix567-installed-binding.json');SCRATCH=Path('/run/pix567-installed01')
SEAL='f4af7321d227950b4b658efb20dc30fa7862998960ae8cd9da5dd65a4cb9d8c8'
report={'status':'FAIL','commands':[],'cleanup_errors':[],'forced_children':[]};mounted=False;stopped=False
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024**2),b''):h.update(block)
    return h.hexdigest()
def save(path,value):
    pending=path.with_name(path.name+'.pending');pending.write_text(json.dumps(value,indent=2)+'\n');pending.replace(path)
def bounds():
    if not SCRATCH.exists():return
    paths=list(SCRATCH.rglob('*'));assert len(paths)<=2048,'fixture output count bound'
    sizes=[]
    for p in paths:
        try:info=p.lstat()
        except FileNotFoundError:continue  # Atomic observer/stamp rename during live sampling.
        if stat.S_ISREG(info.st_mode):sizes.append(info.st_size)
    assert sum(sizes)<=64*1024**2 and all(n<=8*1024**2 for n in sizes),'fixture aggregate output bound'
def call(name,args,seconds=20,check=True,fixture=False):
    row={'name':name,'argv':[str(x) for x in args],'original_returncode':None,'timed_out':False};report['commands'].append(row);child=None
    env={'PATH':'/usr/bin:/usr/sbin:/bin:/sbin','HOME':'/storage','LANG':'C','LC_ALL':'C'}
    def limits():resource.setrlimit(resource.RLIMIT_FSIZE,(64*1024**2,64*1024**2));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    try:
        with (OUT/(name+'.stdout')).open('xb') as out,(OUT/(name+'.stderr')).open('xb') as err:
            child=subprocess.Popen(row['argv'],stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=env,start_new_session=True,preexec_fn=limits)
            try:
                deadline=time.monotonic()+seconds
                while True:
                    assert all((OUT/(name+s)).stat().st_size<=8*1024**2 for s in ['.stdout','.stderr'])
                    if fixture:bounds()
                    left=deadline-time.monotonic()
                    if left<=0:raise subprocess.TimeoutExpired(row['argv'],seconds)
                    try:row['original_returncode']=child.wait(timeout=min(1,left));break
                    except subprocess.TimeoutExpired:pass
            except BaseException as error:
                row['timed_out']=isinstance(error,subprocess.TimeoutExpired);row['interrupted']=type(error).__name__
                if child.poll() is None:
                    os.killpg(child.pid,signal.SIGTERM)
                    try:row['original_returncode']=child.wait(timeout=10)
                    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);row['original_returncode']=child.wait(timeout=2)
                else:row['original_returncode']=child.returncode
                raise
        if check:assert row['original_returncode']==0,name
        return row,(OUT/(name+'.stdout')).read_text()
    finally:save(OUT/(name+'.exit.json'),row)
def frontend():
    found=[]
    for p in Path('/proc').iterdir():
        if p.name.isascii() and p.name.isdigit():
            try:
                if os.readlink(p/'exe')=='/usr/bin/emulationstation':found.append(p)
            except (FileNotFoundError,ProcessLookupError):pass
    return found
def reap():
    deadline=time.monotonic()+5
    while True:
        while True:
            try:pid,status=os.waitpid(-1,os.WNOHANG)
            except ChildProcessError:break
            if not pid:break
            report.setdefault('reaped_children',[]).append({'pid':pid,'wait_status':status})
        children=direct_children(os.getpid())
        if not children:return
        assert time.monotonic()<deadline,'owned child cleanup deadline'
        for row in children:report['forced_children'].append(signal_child(row,os.getpid()))
        time.sleep(.02)
def archive_records():
    if not SCRATCH.exists():return
    bounds();files=[];rows=[]
    for path in sorted(SCRATCH.rglob('*')):
        name=str(path.relative_to(SCRATCH));info=path.lstat()
        if name=='key.pem':continue  # ephemeral synthetic TLS private key is never exported
        if stat.S_ISDIR(info.st_mode):continue
        assert stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode),'unexpected fixture evidence type'
        row={'path':name,'mode':stat.S_IMODE(info.st_mode)}
        if path.is_symlink():row.update(kind='symlink',target=os.readlink(path))
        else:row.update(kind='file',bytes=info.st_size,sha256=sha(path))
        rows.append(row);files.append(path)
    with tarfile.open(OUT/'fixture-originals.tar.gz','x:gz',dereference=False) as tar:
        for path,row in zip(files,rows):tar.add(path,arcname=row['path'],recursive=False)
    assert (OUT/'fixture-originals.tar.gz').stat().st_size<=80*1024**2
    with tarfile.open(OUT/'fixture-originals.tar.gz') as tar:
        members=tar.getmembers();assert [m.name for m in members]==[r['path'] for r in rows]
        for row,path,m in zip(rows,files,members):
            if row['kind']=='symlink':assert m.issym() and m.linkname==os.readlink(path)==row['target']
            else:
                raw=tar.extractfile(m).read();assert m.isfile() and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==sha(path)==row['sha256']
    save(OUT/'fixture-originals.json',rows)
def expired(*_):raise TimeoutError('outer guest work deadline or termination')
assert os.geteuid()==0 and len(sys.argv)==2 and re.fullmatch('[0-9a-f]{64}',sys.argv[1])
OUT.mkdir();resource.setrlimit(resource.RLIMIT_FSIZE,(128*1024**2,128*1024**2));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
signal.signal(signal.SIGALRM,expired);signal.signal(signal.SIGTERM,expired);signal.alarm(420)
try:
    libc=ctypes.CDLL(None,use_errno=True);libc.prctl.restype=ctypes.c_int;assert libc.prctl(36,1,0,0,0)==0
    source=HERE/'installed567';binding=HERE/'binding.json';assert sha(binding)==sys.argv[1]
    b=json.loads(binding.read_text());assert b['boot_id']==Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    assert sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo']
    assert sha(Path('/usr/bin/emulationstation'))==b['files']['/usr/bin/emulationstation']['sha256']
    assert sha(source/'SHA256SUMS')==SEAL
    for line in (source/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);assert sha(source/name)==digest
    for path in [PACKET,BINDING,SCRATCH]:assert not path.exists() and not path.is_symlink()
    # Observe the actual installed ES environment; keep only Wayland connection fields.
    deadline=time.monotonic()+60;observations=[]
    while True:
        processes=frontend();ready=False
        if len(processes)==1:
            env=dict(item.split(b'=',1) for item in (processes[0]/'environ').read_bytes().split(b'\0') if b'=' in item)
            runtime=Path(env.get(b'XDG_RUNTIME_DIR',b'').decode()).resolve();display=env.get(b'WAYLAND_DISPLAY',b'').decode()
            ready=runtime.is_absolute() and runtime.is_relative_to('/run') and bool(display) and '/' not in display and (runtime/display).is_socket()
            if ready:
                sockets=[p for p in runtime.glob('sway-ipc.*.sock') if p.is_socket()];ready=len(sockets)==1
            if ready:break
        observations.append({'seconds_remaining':round(deadline-time.monotonic(),2),'frontend_count':len(processes),'wayland_ready':ready})
        assert time.monotonic()<deadline,'actual Wayland startup timeout';time.sleep(.5)
    original_pid=int(processes[0].name);assert sha(processes[0]/'exe')==b['files']['/usr/bin/emulationstation']['sha256']
    _,text=call('sway-output',['swaymsg','-s',sockets[0],'-t','get_outputs','-r'])
    outputs=[row for row in json.loads(text) if row.get('active')];assert len(outputs)==1 and outputs[0]['current_mode']['width']==640 and outputs[0]['current_mode']['height']==480
    save(OUT/'display-binding.json',{'original_es_pid':original_pid,'xdg_runtime_dir':str(runtime),'wayland_display':display,'sway_socket':str(sockets[0]),'outputs':outputs,'startup_observations':observations})
    _,text=call('frontend-active',['systemctl','is-active','essway.service']);assert text.strip()=='active'
    call('frontend-stop',['systemctl','stop','essway.service'],30);stopped=True
    deadline=time.monotonic()+10
    while frontend():assert time.monotonic()<deadline,'old ES survived stop';time.sleep(.1)
    assert (runtime/display).is_socket() and sockets[0].is_socket()
    PACKET.mkdir();call('packet-bind',['mount','--bind',source,PACKET]);mounted=True
    call('packet-readonly',['mount','-o','remount,bind,ro',PACKET]);shutil.copy2(binding,BINDING);assert sha(BINDING)==sys.argv[1]
    argv=['/usr/bin/python3','-I','-S','-B',PACKET/'run-fixture.py','--installed-binding',BINDING,'--binding-sha256',sys.argv[1],'--output',SCRATCH,'--xdg-runtime-dir',runtime,'--wayland-display',display,'--disposable-guest']
    row,_=call('original-fixture',argv,310,check=False,fixture=True)
    assert row['original_returncode']==0 and not row['timed_out']
    original=json.loads((SCRATCH/'result.json').read_text());worker=json.loads((SCRATCH/'worker-result.json').read_text());lock=json.loads((SCRATCH/'lock-custody-result.json').read_text())
    assert original['passed'] and original['worker_exit']==0 and not original['timeout'] and original['interrupted_signal'] is None
    assert not original['stragglers_killed'] and not original['namespace_processes_remaining'] and original['parent_unchanged']
    assert worker['passed'] and worker['es_exit']==worker['listener_exit']==0 and not worker['es_forced'] and worker['output_guard_passed']
    assert worker['topup_exits']==[0] and worker['installed_observers']['all_exited'] and worker['backend']['passed'] and lock['passed'] and not lock['errors']
    assert not (SCRATCH/'key.pem').exists();report['status']='PASS'
except BaseException as error:report['error']=type(error).__name__+': '+str(error)
finally:
    signal.alarm(90)
    try:
        quiet=True
        try:reap()
        except BaseException as error:quiet=False;report['cleanup_errors'].append('descendants: '+str(error))
        if quiet:
            try:archive_records()
            except BaseException as error:report['cleanup_errors'].append('original export: '+str(error))
        if BINDING.exists():shutil.copy2(BINDING,OUT/'binding.json')
        if mounted:
            try:call('packet-unmount',['umount',PACKET],10);PACKET.rmdir()
            except BaseException as error:report['cleanup_errors'].append('packet unmount: '+str(error))
        if stopped:
            try:
                call('frontend-restart',['systemctl','start','essway.service'],30)
                deadline=time.monotonic()+20
                while True:
                    pids=frontend()
                    if len(pids)==1 and sha(pids[0]/'exe')==b['files']['/usr/bin/emulationstation']['sha256']:break
                    assert time.monotonic()<deadline,'original frontend not restored';time.sleep(.2)
                save(OUT/'frontend-restored.json',{'pid':int(pids[0].name),'installed_es_sha256':sha(pids[0]/'exe'),'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()})
            except BaseException as error:report['cleanup_errors'].append('frontend restoration: '+str(error))
        reap();report['remaining_children']=direct_children(os.getpid())
    except BaseException as error:report['cleanup_errors'].append('finalizer: '+str(error))
    finally:
        signal.alarm(0)
        if report['cleanup_errors'] or report['forced_children'] or report.get('remaining_children'):report['status']='FAIL'
        save(OUT/'outer-guest-result.json',report)
        files=[p for p in sorted(OUT.rglob('*')) if p.is_file()];assert len(files)<=128 and sum(p.stat().st_size for p in files)<=112*1024**2
        save(OUT.parent/'guest-export-manifest.json',[{'path':str(p.relative_to(OUT.parent)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files])
print(json.dumps({'status':report['status'],'originals':str(OUT)}),flush=True)
raise SystemExit(0 if report['status']=='PASS' else 1)

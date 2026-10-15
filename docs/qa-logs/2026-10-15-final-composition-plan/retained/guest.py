#!/usr/bin/python3
"""Installed default loader only. CONFIG is supplied by the bound outer owner."""
import base64,ctypes,hashlib,json,os,resource,shutil,signal,stat,subprocess,time
from pathlib import Path
ROOT=Path('/run/pix-m7-retained-loader')
assert not ROOT.exists() and not ROOT.is_symlink(),'fresh private runtime output required'
ROOT.mkdir(mode=0o700)
result={'status':'FAIL','started':time.time(),'checks':[],'cleanup_errors':[]}
selected=['/storage/.config/system/configs/system.cfg','/storage/.config/emulationstation/es_settings.cfg','/storage/.config/cloud_sync.conf','/storage/roms/gb/pixelelated-installed-state.gb','/storage/roms/gb/gamelist.xml','/storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat','/storage/.cache/cloud_sync/last-backup','/storage/.cache/cloud_sync/last-restore']
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def data(p):
    p=Path(p);assert p.is_file() and not p.is_symlink() and p.stat().st_size<=1024**2,str(p)
    before=p.stat();raw=p.read_bytes();after=p.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
    return (raw,stat.S_IMODE(before.st_mode))
def snapshot():return {n:data(n) for n in selected}
def members():
    rows={};mounts=[line.split()[4] for line in Path('/proc/self/mountinfo').read_text().splitlines()]
    for rel,want in CONFIG['members'].items():
        p=Path('/')/rel;assert p.is_file() and p.stat().st_size==want['bytes'] and digest(p)==want['sha256'] and stat.filemode(p.stat().st_mode)==want['mode'],rel
        chain=want['link_chain'];assert str(p.resolve())==chain['resolved'],rel
        for link in chain['links']:assert os.readlink(link['path'])==link['target']
        # Root filesystem is normal; a product-specific mount/overlay is not.
        assert not any(str(p)==m or str(p.resolve())==m or m.startswith('/usr/') and str(p).startswith(m+'/') for m in mounts),rel
        assert '/usr' not in mounts,'unexpected /usr overlay'
        rows[rel]={'sha256':want['sha256'],'mode':want['mode'],'resolved':str(p.resolve())}
    return rows
def persist_command(index,row):
    raw=json.dumps(row,sort_keys=True).encode()
    (ROOT/(str(index)+'.receipt.json')).write_bytes(raw+b'\n')
    print('PIX_LOADER_COMMAND='+base64.b64encode(raw).decode(),flush=True)
def command(args,seconds,env=None):
    index=len(result['checks']);row={'argv':args,'timeout_seconds':seconds,'original_returncode':None,'timed_out':False};result['checks'].append(row)
    out=ROOT/(str(index)+'.stdout');err=ROOT/(str(index)+'.stderr');child=None;recorded=False
    try:
        with out.open('xb') as o,err.open('xb') as e:
            child=subprocess.Popen(args,stdin=subprocess.DEVNULL,stdout=o,stderr=e,env=env,start_new_session=True)
            try:row['original_returncode']=child.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                row['timed_out']=True;os.killpg(child.pid,signal.SIGKILL);row['original_returncode']=child.wait(timeout=5)
        assert out.stat().st_size<=2*1024**2 and err.stat().st_size<=2*1024**2,'output limit'
        row.update(stdout=out.read_text(errors='replace'),stderr=err.read_text(errors='replace'))
        persist_command(index,row);recorded=True
        assert not row['timed_out'] and row['original_returncode']==0,'loader command failed'
        return row
    finally:
        if child and child.poll() is None:os.killpg(child.pid,signal.SIGKILL);row['original_returncode']=child.wait(timeout=5);result['cleanup_errors'].append('forced loader cleanup')
        for key,p in [('stdout',out),('stderr',err)]:
            if p.exists() and key not in row:row[key]=p.read_bytes()[:2*1024**2].decode(errors='replace')
        if not recorded:persist_command(index,row)
before=None
try:
    resource.setrlimit(resource.RLIMIT_FSIZE,(2*1024**2,2*1024**2));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    result['boot_id']=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    assert result['boot_id'] not in [b['boot_id'] for b in CONFIG['previous_boots']]
    result['cmdline']=Path('/proc/cmdline').read_text().strip();result['interfaces']=sorted(p.name for p in Path('/sys/class/net').iterdir());assert result['interfaces']==['lo']
    assert 'BUILD_ID="'+CONFIG['commit']+'"' in Path('/etc/os-release').read_text()
    state=Path('/storage/.cache/pixelelated-installed-state-'+CONFIG['retained_id'])
    for name,h in CONFIG['retained_receipts'].items():assert digest(state/name)==h,name
    result['original_retained_receipts_equal']=True
    assert not any(Path('/storage/.update').iterdir())
    before=snapshot();result['members_before']=members()
    for key in ['LD_LIBRARY_PATH','LD_PRELOAD','GST_PLUGIN_SCANNER','GST_PLUGIN_SCANNER_1_0','GST_PLUGIN_PATH','GST_PLUGIN_PATH_1_0','GST_PLUGIN_SYSTEM_PATH','GST_PLUGIN_SYSTEM_PATH_1_0','GST_REGISTRY_FORK']:assert not os.environ.get(key),'unexpected loader override: '+key
    for lib in ['libgstcontroller-1.0.so.0','libgstreamer-1.0.so.0','/usr/lib/gstreamer-1.0/libgstopengl.so']:ctypes.CDLL(lib,mode=os.RTLD_NOW)
    result['rtld_now']='PASS'
    for target in ['/usr/bin/cloud-signin-window','/usr/lib/gstreamer-1.0/gst-plugin-scanner']:
        row=command(['ldd',target],15);assert 'not found' not in row['stdout']+row['stderr'],target
    registry=ROOT/'gst-registry.bin';assert not registry.exists()
    env=dict(os.environ,GST_REGISTRY=str(registry))
    row=command(['/usr/bin/gst-inspect-1.0','opengl'],30,env)
    assert registry.is_file() and registry.stat().st_size>0 and 'Failed to load plugin' not in row['stderr'] and 'External plugin loader failed' not in row['stderr']
    result['scanner_scope']='Installed executable/default registry and ldd closure; no separate scanner child-exec trace claimed.'
    result['status']='PASS'
except BaseException as exc:result['error']=type(exc).__name__+': '+str(exc)
finally:
    try:
        registry=ROOT/'gst-registry.bin'
        if registry.is_file():
            assert not registry.is_symlink() and registry.stat().st_size<=2*1024**2
            raw=registry.read_bytes();result['registry']={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'fresh':True}
            print('PIX_LOADER_REGISTRY='+base64.b64encode(raw).decode(),flush=True)
    except BaseException as exc:result['cleanup_errors'].append('registry receipt: '+str(exc))
    try:
        if before is not None:
            result['selected_bytes_and_modes_equal']=snapshot()==before
            assert result['selected_bytes_and_modes_equal'],'selected synthetic state changed during probe'
        result['members_after']=members();assert result['members_after']==result.get('members_before'),'installed members changed'
        live=[]
        for p in Path('/proc').iterdir():
            if not p.name.isdigit():continue
            try:name=Path(os.readlink(p/'exe')).name
            except (FileNotFoundError,ProcessLookupError):continue
            if name in ['gst-inspect-1.0','gst-plugin-scanner']:live.append(int(p.name))
        result['remaining_loader_pids']=live;assert not live,'loader child remains'
        assert Path('/proc/sys/kernel/random/boot_id').read_text().strip()==result['boot_id']
    except BaseException as exc:result['cleanup_errors'].append(type(exc).__name__+': '+str(exc))
    try:shutil.rmtree(ROOT);result['private_runtime_removed']=not ROOT.exists()
    except BaseException as exc:result['cleanup_errors'].append('private runtime: '+str(exc))
    if result['cleanup_errors']:result['status']='FAIL'
    result['ended']=time.time()
    # No private settings/account values or account hashes leave the guest.
    print('PIX_RETAINED_LOADER='+base64.b64encode(json.dumps(result,sort_keys=True).encode()).decode(),flush=True)
raise SystemExit(0 if result['status']=='PASS' else 1)

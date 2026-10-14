#!/usr/bin/env python3
"""UNRUN guest transport/owner wrapper. Product execution is exclusively the sealed fixture."""
import hashlib,json,os,resource,shutil,signal,subprocess,sys,time
from pathlib import Path
OUT=Path('/tmp/pix-output/installed588');OUT.mkdir()
PACKET=Path('/run/pix588-installed-packet');INPUTS=Path('/run/pix588-installed-inputs');SCRATCH=Path('/run/pix588-installed-owner')
report={'status':'FAIL','commands':[],'cleanup_errors':[],'forced_cleanup':False};frontend=None;mounts=[]
resource.setrlimit(resource.RLIMIT_FSIZE,(4*1024**2,4*1024**2));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def call(name,args,seconds=20,check=True):
    row={'name':name,'argv':args,'timed_out':False,'original_returncode':None};report['commands'].append(row)
    with (OUT/(name+'.stdout')).open('xb') as stdout,(OUT/(name+'.stderr')).open('xb') as stderr:
        child=subprocess.Popen(args,stdout=stdout,stderr=stderr,stdin=subprocess.DEVNULL,start_new_session=True)
        try:row['original_returncode']=child.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            row['timed_out']=True;os.killpg(child.pid,signal.SIGTERM)
            try:row['original_returncode']=child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGKILL);row['original_returncode']=child.wait(timeout=2)
    if check:assert not row['timed_out'] and row['original_returncode']==0,name
    return row,(OUT/(name+'.stdout')).read_text()
def mount_ro(source,target):
    target.mkdir();call('bind-'+target.name,['mount','--bind',str(source),str(target)]);mounts.append(target)
    call('readonly-'+target.name,['mount','-o','remount,bind,ro',str(target)])
try:
    assert len(sys.argv)==2 and len(sys.argv[1])==64
    binding=Path('/tmp/pix588-binding/binding.json');assert sha(binding)==sys.argv[1]
    b=json.loads(binding.read_text());assert b['boot_id']==Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    assert set(p.name for p in Path('/sys/class/net').iterdir())=={'lo'}
    source=Path('/tmp/pix-input/installed588')
    assert sha(source/'SHA256SUMS')=='dcbee145f6f7c41da944416bcdd4cb4868be91aeaf1a7935b52d1e1db68f4301'
    for line in (source/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);assert sha(source/name)==digest
    for p in [PACKET,INPUTS,SCRATCH]:assert not p.exists()
    active=[]
    for unit in ['essway.service','emustation.service']:
        row,text=call('active-'+unit,['systemctl','is-active',unit],check=False)
        if row['original_returncode']==0 and text.strip()=='active':active.append(unit)
        else:assert not row['timed_out'] and row['original_returncode'] in (3,4),row
    assert len(active)==1;frontend=active[0]
    call('frontend-stop',['systemctl','stop',frontend],seconds=30)
    deadline=time.monotonic()+10
    while True:
        pids=[]
        for proc in Path('/proc').iterdir():
            if proc.name.isdigit():
                try:
                    if Path(os.readlink(proc/'exe')).name=='emulationstation':pids.append(int(proc.name))
                except (FileNotFoundError,PermissionError,ProcessLookupError):pass
        if not pids:break
        assert time.monotonic()<deadline,'frontend remains';time.sleep(.1)
    mount_ro(source,PACKET);mount_ro(binding.parent,INPUTS)
    SCRATCH.mkdir();call('scratch',['mount','-t','tmpfs','-o','size=64m,mode=0700','pix588-installed-owner',str(SCRATCH)]);mounts.append(SCRATCH)
    argv=['systemd-run','--unit=pix588-installed-owner.service','--wait','--pipe','--property=Type=exec','--property=RuntimeMaxSec=280','--property=TimeoutStopSec=20','--property=KillMode=control-group','--property=LimitAS=1G','--property=LimitCPU=150','--property=LimitFSIZE=4M','--property=LimitCORE=0','/usr/bin/python3','-I','-S','-B',str(PACKET/'owner.py'),'--output',str(SCRATCH/'run01'),'--binding-sha256',sys.argv[1]]
    row,_=call('original-systemd-run',argv,seconds=310,check=False)
    assert row['original_returncode']==0 and not row['timed_out'],row
    owner=json.loads((SCRATCH/'run01/owner-result.json').read_text());payload=json.loads((SCRATCH/'run01/payload/result.json').read_text())
    assert owner['status']==payload['status']=='PASS' and owner['original_child_exit']==0 and not owner['timed_out']
    assert owner['remaining_children']==[] and not owner['signals'] and not owner['cleanup_errors'] and not payload['cleanup_errors']
    report['status']='PASS'
except BaseException as error:report['error']=type(error).__name__+': '+str(error)
finally:
    # Preserve original outcomes. Any cleanup intervention prevents PASS.
    for unit in ['raofflineproxy.service','pix588-installed-owner.service']:
        try:
            _,state=call('final-state-'+unit,['systemctl','show',unit,'--property=ActiveState','--property=SubState','--property=MainPID','--property=ExecMainCode','--property=ExecMainStatus'],check=False)
            fields=dict(line.split('=',1) for line in state.splitlines() if '=' in line)
            if fields.get('ActiveState') in ('active','activating','deactivating') or fields.get('MainPID','0')!='0':
                report['forced_cleanup']=True;call('cleanup-stop-'+unit,['systemctl','stop',unit],seconds=25)
        except BaseException as error:report['cleanup_errors'].append(str(error))
    try:
        root=SCRATCH/'run01'
        if root.exists():
            children=list(root.rglob('*'));assert len(children)<=512 and not any(f.is_symlink() for f in children)
            files=[f for f in children if f.is_file()];assert sum(f.stat().st_size for f in files)<=16*1024**2
            shutil.copytree(root,OUT/'original-owner');write(OUT/'original-owner-manifest.json',[{'path':str(f.relative_to(root)),'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(files)])
        shutil.copy2('/tmp/pix588-binding/binding.json',OUT/'binding.json')
    except BaseException as error:report['cleanup_errors'].append(str(error))
    for target in reversed(mounts):
        try:call('unmount-'+target.name,['umount',str(target)],seconds=10)
        except BaseException as error:report['cleanup_errors'].append(str(error))
    if frontend:
        try:call('frontend-restart',['systemctl','start',frontend],seconds=30)
        except BaseException as error:report['cleanup_errors'].append(str(error))
    if report['cleanup_errors'] or report['forced_cleanup']:report['status']='FAIL'
    write(OUT/'outer-guest-result.json',report)
print(json.dumps({'status':report['status'],'original_results':str(OUT)}),flush=True)
raise SystemExit(0 if report['status']=='PASS' else 1)

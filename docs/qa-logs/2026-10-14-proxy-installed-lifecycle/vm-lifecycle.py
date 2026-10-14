#!/usr/bin/env python3
"""UNRUN admitted host lifecycle: original clean first boot, then installed #588 once."""
import base64,gzip,hashlib,json,os,shlex,shutil,signal,socket,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent;C=json.loads((R/'config.json').read_text());TREE=Path(C['checkout']);V=R/'vm';F=C['custody'];disk=V/'disk.qcow2'
result={'rc':1,'started':time.time(),'boots':[],'commands':[],'cleanup_errors':[]};mounted=False;sequence=0

def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def identity(pid):
    p=Path('/proc',str(pid));fields=(p/'stat').read_text().rsplit(')',1)[1].split()
    assert fields[0]!='Z'
    return {'pid':pid,'start_ticks':int(fields[19]),'cmdline':[x.decode() for x in (p/'cmdline').read_bytes().split(b'\0') if x]}
def evidence(path):return {'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path)}
def call(name,args,seconds,check=True):
    global sequence
    sequence+=1;stem=R/'records'/('%03d-%s'%(sequence,name));row={'name':name,'argv':[str(x) for x in args],'timeout_seconds':seconds,'timed_out':False,'original_returncode':None};result['commands'].append(row)
    child=None
    try:
        with Path(str(stem)+'.stdout').open('xb') as stdout,Path(str(stem)+'.stderr').open('xb') as stderr:
            child=subprocess.Popen(row['argv'],stdout=stdout,stderr=stderr,stdin=subprocess.DEVNULL,start_new_session=True)
            try:
                command_deadline=time.monotonic()+seconds
                while True:
                    for suffix in ['.stdout','.stderr']:
                        assert Path(str(stem)+suffix).stat().st_size<=8*1024**2,'live command output bound exceeded'
                    remaining=command_deadline-time.monotonic()
                    if remaining<=0:raise subprocess.TimeoutExpired(row['argv'],seconds)
                    try:row['original_returncode']=child.wait(timeout=min(1,remaining));break
                    except subprocess.TimeoutExpired:pass
            except BaseException as exc:
                row['timed_out']=isinstance(exc,subprocess.TimeoutExpired);row['interrupted']=type(exc).__name__
                if child.poll() is None:
                    os.killpg(child.pid,signal.SIGTERM)
                    try:row['original_returncode']=child.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(child.pid,signal.SIGKILL);row['original_returncode']=child.wait(timeout=2)
                else:row['original_returncode']=child.returncode
                raise
        assert Path(str(stem)+'.stdout').stat().st_size<=8*1024**2 and Path(str(stem)+'.stderr').stat().st_size<=8*1024**2,'host command output bound'
        if check:assert row['original_returncode']==0,name
        return Path(str(stem)+'.stdout').read_text()
    finally:write(Path(str(stem)+'.exit.json'),row)
def serial(name,command,seconds=30):
    # vm-serial is a transport; preserve and separately check the guest's real exit.
    marker='PIX_LIFECYCLE_'+name.upper().replace('-','_')+'_RC:'
    text=call(name,[TREE/'tools/vm-serial','--socket',V/'serial.sock','--timeout',str(seconds),'sh','( '+command+'\n ); pxrc=$?; printf "'+marker+'%s\\n" "$pxrc"'],seconds+15)
    assert text.count(marker)==1 and marker+'0' in text,name
    return text
def monitor(command):
    with socket.socket(socket.AF_UNIX) as s:
        s.settimeout(5);s.connect(str(V/'monitor.sock'));s.recv(65536);s.sendall((command+'\n').encode());data=b''
        while b'(qemu)' not in data:
            chunk=s.recv(65536);assert chunk,'monitor EOF';data+=chunk;assert len(data)<=1024**2
    text=data.decode(errors='replace')
    with (R/'monitor.log').open('a') as f:f.write(command+'\n'+text+'\n')
    assert 'Error' not in text and 'failed' not in text.lower(),text

def expired(signum,frame):raise TimeoutError('full lifecycle deadline or termination')
signal.signal(signal.SIGALRM,expired);signal.signal(signal.SIGTERM,expired);signal.alarm(C['work_seconds'])
try:
    assert Path('/proc/self/ns/pid').stat().st_ino==4026531836,'use actual admitted host namespace'
    run=Path(os.environ['RASTERATOPS_BUILD_RUN']);run=run if run.is_absolute() else TREE/run
    assert run.parent==TREE/'.build-runs'
    watcher=identity(int((run/'watcher.pid').read_text()));write(R/'records/watch-owner.json',{'run':str(run),'lifecycle':identity(os.getpid()),'watcher':watcher,'work_alarm_seconds':C['work_seconds'],'cleanup_alarm_seconds':C['cleanup_seconds'],'guest_command_watchdog_seconds':310,'guest_cleanup_grace_seconds':10})
    for path,digest in C['tools'].items():assert sha(Path(path))==digest,path
    for path,digest in C['code'].items():assert sha(R/path)==digest,path
    assert call('source-head',['git','-C',TREE,'rev-parse','HEAD'],10).strip()==C['commit']
    assert sha(R/'records/final-custody.original.json')==C['custody_sha256']
    for name in ['image','system','boot_config','source_receipt','update_report','install_report']:assert sha(Path(F[name]['path']))==F[name]['sha256'],name
    with socket.socket() as s:s.bind(('127.0.0.1',5900+C['vnc']))
    # Reuse accepted sparse inflation, conversion and minimum disk size. No kernel/boot-file mutation.
    raw=V/'disk.img';count=0
    with gzip.open(F['image']['path'],'rb') as source,raw.open('xb') as target:
        while chunk:=source.read(4*1024**2):
            count+=len(chunk);assert count<=F['image']['raw_bytes']
            if chunk.count(0)==len(chunk):target.seek(len(chunk),1)
            else:target.write(chunk)
        target.truncate()
    assert count==F['image']['raw_bytes'];call('convert',['qemu-img','convert','-f','raw','-O','qcow2',raw,disk],90);call('resize',['qemu-img','resize',disk,'16G'],30);raw.unlink()
    args=[disk,'--no-network','--headless','--daemonize','--gl','auto','--res','640x480','--vnc',str(C['vnc']),'--pidfile',V/'vm.pid','--serial',V/'serial.sock','--monitor',V/'monitor.sock','--ovmf-vars',V/'OVMF.fd']
    generated=shlex.split(call('qemu-args',[C['helper'],'qemu-args',*args],20))
    assert generated.count('-nic')==1 and generated[generated.index('-nic')+1]=='none'
    assert '-netdev' not in generated and not any('hostfwd=' in a or 'cloud_ssh_port' in a for a in generated)
    assert generated[generated.index('-m')+1]=='8192' and generated[generated.index('-smp')+1]=='4'
    write(R/'generated-640x480.json',generated);call('qemu-start',[C['helper'],'run',*args],60)
    qemu=identity(int((V/'vm.pid').read_text()));assert qemu['cmdline']==generated
    write(R/'qemu-640x480.json',qemu);result['boots'].append({'pid':qemu['pid'],'start_ticks':qemu['start_ticks'],'source_sha256':F['image']['sha256'],'profile':'640x480','no_network':True})
    call('wait-serial',[TREE/'tools/vm-serial','--socket',V/'serial.sock','wait','--up-to','240'],260)
    # The original clean helper runs BEFORE attaching fixture media or writing any fixture state.
    call('clean-first-boot',['bash',TREE/'docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh',R/'clean',V/'serial.sock'],210)
    raw_clean=(R/'clean/first-boot.serial').read_text();report,end=json.JSONDecoder().raw_decode(raw_clean[raw_clean.index('{\n'):])
    assert report['schema']==1 and report['policy']=='pixelelated-selected-state-v1' and report['mode']=='first-boot'
    assert report['status']=='pass' and report['blocked_count']==report['error_count']==0
    assert any(x.get('category')=='boot-ready' and x.get('status')=='clear' and x.get('present') is True for x in report['checks'])
    assert raw_clean.count('PIX_STATE_565_RC=')==1 and 'PIX_STATE_565_RC=0' in raw_clean
    # Preserve the exact original JSON text, not a synthetic summary.
    (R/'clean/report.json').write_text(raw_clean[raw_clean.index('{\n'):][:end]+'\n')
    script="import socket,json;from pathlib import Path;a=sorted(n for _,n in socket.if_nameindex());b=sorted(p.name for p in Path('/sys/class/net').iterdir());assert a==b==['lo'];print('PIX_BOOT_JSON='+json.dumps({'interfaces':a,'sysfs':b,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}))"
    text=serial('topology','python3 -I -S -B -c '+shlex.quote(script));boot=json.loads(next(x.split('=',1)[1] for x in text.splitlines() if x.startswith('PIX_BOOT_JSON=')))
    write(R/'records/boot.json',boot)
    assert identity(qemu['pid'])==qemu and identity(watcher['pid'])==watcher and signal.getitimer(signal.ITIMER_REAL)[0]>0
    # Record an actual cap only when readable; default allocation does not promise one.
    cgroup_raw=Path('/proc',str(qemu['pid']),'cgroup').read_text();cap=None;cap_observations=[]
    for line in cgroup_raw.splitlines():
        _,controllers,relative=line.split(':',2)
        candidates=[]
        if controllers=='':candidates=[Path('/sys/fs/cgroup')/relative.lstrip('/')/'memory.max']
        if 'memory' in controllers.split(','):candidates=[Path('/sys/fs/cgroup/memory')/relative.lstrip('/')/'memory.limit_in_bytes']
        for path in candidates:
            try:
                value=path.read_text().strip();cap_observations.append({'path':str(path),'value':value})
                if value.isdigit():cap=int(value)
            except OSError as exc:cap_observations.append({'path':str(path),'error':str(exc)})
    write(R/'records/host-cgroup.json',{'cgroup':cgroup_raw,'observations':cap_observations,'observed_local_limit_bytes':cap,'ancestor_caps_not_claimed':True})
    outer={'status':'PASS','boot_id':boot['boot_id'],'vm_ram_bytes':8589934592,'vcpus':4,'no_nic':True,'host_qemu_identity':{k:qemu[k] for k in ['pid','start_ticks']},'host_cgroup_memory_max_bytes':cap,'command_timeout_seconds':310,'cleanup_grace_seconds':10,'watchdog_running':True,'evidence':[evidence(R/x) for x in ['records/watch-owner.json','qemu-640x480.json','records/boot.json','records/host-cgroup.json','run-guest.py']]}
    write(R/'records/outer-receipt.json',outer)
    source=json.loads((R/'records/source-receipt.original.json').read_text());source.update(clean_report_sha256=sha(R/'clean/report.json'),clean_ready_report_verified=True,clean_boot_id=boot['boot_id'])
    source['evidence']+= [evidence(R/'clean/first-boot.serial'),evidence(R/'clean/report.json')];write(R/'records/source-receipt.bound.json',source)
    binding=R/'records/binding.json'
    call('bind-image',['python3','-I','-S','-B',R/'source/installed588/bind-image.py','--root',F['system']['root'],'--source-receipt',R/'records/source-receipt.bound.json','--clean-report',R/'clean/report.json','--boot-config',F['boot_config']['path'],'--image-sha256',F['image']['sha256'],'--distribution-commit',C['commit'],'--boot-id',boot['boot_id'],'--safeguards','outer-vm','--outer-receipt',R/'records/outer-receipt.json','--output',binding],30)
    # Only now create and attach read-only fixture media; no product source/native overlay.
    payload=V/'input-tree';payload.mkdir();shutil.copytree(R/'source/installed588',payload/'installed588');shutil.copy2(R/'run-guest.py',payload/'run-guest.py')
    write(R/'records/input-files.json',{str(f.relative_to(payload)):sha(f) for f in sorted(payload.rglob('*')) if f.is_file()})
    for name,label in [('input','PIXINPUT'),('output','PIXOUTPUT')]:
        path=V/(name+'.ext4')
        with path.open('xb') as stream:stream.truncate(256*1024**2)
        mk=['mkfs.ext4','-q','-F','-L',label]+(['-d',payload] if name=='input' else [])+[path]
        call('media-'+name,mk,60)
    shutil.rmtree(payload)
    for name in ['input','output']:
        monitor('drive_add 0 if=none,id=pix'+name+',format=raw,'+('readonly=on,' if name=='input' else '')+'file='+str(V/(name+'.ext4')))
        monitor('device_add usb-storage,drive=pix'+name+',id=pix'+name+'dev,serial=pix'+name)
    serial('media','for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXOUTPUT && break; sleep 1; done; mkdir /tmp/pix-input /tmp/pix-output && mount -t ext4 -o ro,noload /dev/disk/by-label/PIXINPUT /tmp/pix-input && mount -t ext4 /dev/disk/by-label/PIXOUTPUT /tmp/pix-output');mounted=True
    # Immutable boot-specific binding is small and transported only after clean proof.
    encoded=base64.b64encode(binding.read_bytes()).decode();assert len(encoded)<=512*1024
    serial('binding-init','mkdir /tmp/pix588-binding && : > /tmp/pix588-binding/binding.b64')
    for i in range(0,len(encoded),2000):serial('binding-chunk-'+str(i),'printf %s '+shlex.quote(encoded[i:i+2000])+' >> /tmp/pix588-binding/binding.b64')
    serial('binding-finish','base64 -d /tmp/pix588-binding/binding.b64 > /tmp/pix588-binding/binding.json && rm /tmp/pix588-binding/binding.b64 && printf "%s  %s\\n" '+sha(binding)+' /tmp/pix588-binding/binding.json | sha256sum -c -')
    serial('guest-code','printf "%s  %s\\n" '+C['code']['run-guest.py']+' /tmp/pix-input/run-guest.py | sha256sum -c -')
    text=serial('installed588','python3 -I -S -B /tmp/pix-input/run-guest.py '+sha(binding),seconds=450);(R/'qa-serial.txt').write_text(text)
    text=serial('unmount','sync && umount /tmp/pix-output && umount /tmp/pix-input && sync');mounted=False
    (R/'unmount-640x480.txt').write_text(text+'\nPIX_UNMOUNT_RC:0\n');result['rc']=0
except BaseException as exc:result['error']=type(exc).__name__+': '+str(exc)
finally:
    # Independent bounded finalizer; never turn an interrupted original into success.
    signal.alarm(C['cleanup_seconds'])
    try:
        if (V/'vm.pid').exists():
            try:
                text=serial('finally-flush','sync; if grep -q " /tmp/pix-output " /proc/mounts; then umount /tmp/pix-output; else true; fi; pxrc=$?; sync; exit "$pxrc"',seconds=30)
                (R/'finally-flush.txt').write_text(text+'\nPIX_FINALLY_FLUSH_RC:0\n')
            except BaseException as exc:result['cleanup_errors'].append('flush: '+str(exc))
            try:
                text=call('vm-stop',[TREE/'tools/vm-stop',V/'vm.pid',disk],35);(R/'vm-stop.log').write_text(text)
            except BaseException as exc:result['cleanup_errors'].append('stop: '+str(exc))
    finally:
        signal.alarm(0)
        if result['cleanup_errors']:result['rc']=1
        result['ended']=time.time();write(R/'vm-result.json',result)
raise SystemExit(result['rc'])

#!/usr/bin/env python3
"""UNRUN: one watched clean final boot and unchanged installed567 success case.

Host call/serial/QEMU/stop patterns derive from installed-lifecycle 615bbece.
The sealed top-up fixture is unchanged; this owner supplies custody/transport only.
"""
import ctypes,gzip,hashlib,json,os,shlex,shutil,signal,socket,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;C=json.loads((R/'config.json').read_text());TREE=Path(C['checkout']);V=R/'vm';F=C['custody'];disk=V/'disk.qcow2'
result={'rc':1,'started':time.time(),'commands':[],'boots':[],'cleanup_errors':[]};sequence=0
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
assert sha(R/'census.py')==C['code']['census.py']
sys.path.insert(0,str(R))
from census import direct_children,signal_child
def reap_transport_children():
    # The unchanged qualified pidfd helper handles adopted transport children
    # before another serial client starts. Stop the daemonized QEMU separately.
    qpid=int((V/'vm.pid').read_text()) if (V/'vm.pid').exists() else None
    deadline=time.monotonic()+5
    while True:
        while True:
            try:pid,status=os.waitpid(-1,os.WNOHANG)
            except ChildProcessError:break
            if not pid:break
            result.setdefault('reaped_host_children',[]).append({'pid':pid,'wait_status':status})
        children=[row for row in direct_children(os.getpid()) if row['pid']!=qpid]
        if not children:return
        assert time.monotonic()<deadline,'host transport child cleanup deadline'
        for row in children:result.setdefault('forced_host_child_cleanup',[]).append(signal_child(row,os.getpid()))
        time.sleep(.02)
def identity(pid):
    p=Path('/proc',str(pid));fields=(p/'stat').read_text().rsplit(')',1)[1].split();assert fields[0]!='Z'
    return {'pid':pid,'start_ticks':int(fields[19]),'cmdline':[v.decode() for v in (p/'cmdline').read_bytes().split(b'\0') if v]}
def call(name,args,seconds,check=True):
    global sequence
    sequence+=1;stem=R/'records'/('%03d-%s'%(sequence,name));row={'name':name,'argv':[str(x) for x in args],'timeout_seconds':seconds,'timed_out':False,'original_returncode':None};result['commands'].append(row);child=None
    try:
        with Path(str(stem)+'.stdout').open('xb') as stdout,Path(str(stem)+'.stderr').open('xb') as stderr:
            child=subprocess.Popen(row['argv'],stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,start_new_session=True)
            try:
                deadline=time.monotonic()+seconds
                while True:
                    assert all(Path(str(stem)+s).stat().st_size<=8*1024**2 for s in ['.stdout','.stderr']),'command output bound'
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
        assert all(Path(str(stem)+s).stat().st_size<=8*1024**2 for s in ['.stdout','.stderr'])
        if check:assert row['original_returncode']==0,name
        return Path(str(stem)+'.stdout').read_text()
    finally:write(Path(str(stem)+'.exit.json'),row)
def serial(name,command,seconds=30):
    marker='PIX_INSTALLED567_'+name.upper().replace('-','_')+'_RC:'
    assert '\n' not in command, 'single physical serial line required'
    text=call(name,[TREE/'tools/vm-serial','--socket',V/'serial.sock','--timeout',str(seconds),'sh','( '+command+' ); pxrc=$?; printf "'+marker+'%s\\n" "$pxrc"'],seconds+15)
    assert text.count(marker)==1 and marker+'0' in text,name
    return text
def monitor(command):
    with socket.socket(socket.AF_UNIX) as s:
        s.settimeout(5);s.connect(str(V/'monitor.sock'));s.recv(65536);s.sendall((command+'\n').encode());data=b''
        while b'(qemu)' not in data:
            chunk=s.recv(65536);assert chunk;data+=chunk;assert len(data)<=1024**2
    text=data.decode(errors='replace')
    with (R/'monitor.log').open('a') as f:f.write(command+'\n'+text+'\n')
    assert 'Error' not in text and 'failed' not in text.lower(),text
def expired(*_):raise TimeoutError('installed567 whole work deadline or termination')
signal.signal(signal.SIGALRM,expired);signal.signal(signal.SIGTERM,expired);signal.alarm(C['work_seconds'])
try:
    assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
    libc=ctypes.CDLL(None,use_errno=True);libc.prctl.restype=ctypes.c_int;assert libc.prctl(36,1,0,0,0)==0
    run=Path(os.environ['RASTERATOPS_BUILD_RUN']);run=run if run.is_absolute() else TREE/run;assert run.parent==TREE/'.build-runs'
    watcher=identity(int((run/'watcher.pid').read_text()));write(R/'records/watch-owner.json',{'run':str(run),'owner':identity(os.getpid()),'watcher':watcher,'work_seconds':C['work_seconds'],'cleanup_seconds':C['cleanup_seconds']})
    for path,digest in C['tools'].items():assert sha(Path(path))==digest
    for path,digest in C['code'].items():assert sha(R/path)==digest
    for path,digest in C['verification'].items():assert sha(Path(path))==digest
    assert call('source-head',['git','-C',TREE,'rev-parse','HEAD'],10).strip()==C['commit']
    assert not call('source-clean',['git','-C',TREE,'status','--porcelain'],10).strip()
    assert sha(R/'records/custody.original.json')==C['custody_sha256']
    assert sha(R/'records/source-receipt.es-bound.json')==C['source_receipt_sha256']
    for name in ['image','system','boot_config','source_receipt','update_report','install_report']:assert sha(Path(F[name]['path']))==F[name]['sha256'],name
    adapter=R/'source/installed567';assert sha(adapter/'SHA256SUMS')==C['adapter_manifest']
    for line in (adapter/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);assert sha(adapter/name)==digest
    with socket.socket() as s:s.bind(('127.0.0.1',5900+C['vnc']))
    raw=V/'disk.img';count=0
    with gzip.open(F['image']['path'],'rb') as source,raw.open('xb') as target:
        while chunk:=source.read(4*1024**2):
            count+=len(chunk);assert count<=F['image']['raw_bytes']
            if chunk.count(0)==len(chunk):target.seek(len(chunk),1)
            else:target.write(chunk)
        target.truncate()
    assert count==F['image']['raw_bytes']
    call('convert',['qemu-img','convert','-f','raw','-O','qcow2',raw,disk],120);call('resize',['qemu-img','resize',disk,'16G'],30);raw.unlink()
    args=[disk,'--no-network','--headless','--daemonize','--gl','auto','--res','640x480','--vnc',str(C['vnc']),'--pidfile',V/'vm.pid','--serial',V/'serial.sock','--monitor',V/'monitor.sock','--ovmf-vars',V/'OVMF.fd']
    generated=shlex.split(call('qemu-args',[C['helper'],'qemu-args',*args],20))
    assert generated.count('-nic')==1 and generated[generated.index('-nic')+1]=='none' and '-netdev' not in generated and not any('hostfwd=' in arg for arg in generated)
    assert generated[generated.index('-m')+1]=='8192' and generated[generated.index('-smp')+1]=='4'
    write(R/'generated-640x480.json',generated);call('qemu-start',[C['helper'],'run',*args],60)
    qemu=identity(int((V/'vm.pid').read_text()));assert qemu['cmdline']==generated;write(R/'qemu.json',qemu);result['boots'].append(qemu)
    call('wait-serial',[TREE/'tools/vm-serial','--socket',V/'serial.sock','wait','--up-to','240'],260)
    # Existing untouched clean check precedes every fixture mount, account or ROM seed.
    call('clean-first-boot',['bash',TREE/'docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh',R/'clean',V/'serial.sock'],210)
    text=(R/'clean/first-boot.serial').read_text();start=text.index('{\n');clean,end=json.JSONDecoder().raw_decode(text[start:])
    assert clean['schema']==1 and clean['policy']=='pixelelated-selected-state-v1' and clean['mode']=='first-boot' and clean['status']=='pass'
    assert clean['blocked_count']==clean['error_count']==0 and any(r.get('category')=='boot-ready' and r.get('status')=='clear' and r.get('present') is True for r in clean['checks'])
    assert text.count('PIX_STATE_565_RC=')==1 and 'PIX_STATE_565_RC=0' in text
    (R/'clean/report.json').write_text(text[start:][:end]+'\n')
    code="import json,socket;from pathlib import Path;assert sorted(n for _,n in socket.if_nameindex())==sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo'];print('PIX_BOOT='+json.dumps({'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'os_release':Path('/etc/os-release').read_text()}))"
    text=serial('boot','python3 -I -S -B -c '+shlex.quote(code));boot=json.loads(next(line.split('=',1)[1] for line in text.splitlines() if line.startswith('PIX_BOOT=')))
    assert 'BUILD_ID="'+C['commit']+'"' in boot['os_release'];write(R/'records/boot.json',boot)
    assert identity(qemu['pid'])==qemu and identity(watcher['pid'])==watcher
    binding=R/'records/binding.json'
    call('bind-image',['python3','-I','-S','-B',adapter/'bind-image.py','--root',F['system']['root'],'--distribution',TREE,'--source-receipt',R/'records/source-receipt.es-bound.json','--image-sha256',F['image']['sha256'],'--boot-id',boot['boot_id'],'--output',binding],60)
    b=json.loads(binding.read_text());assert b['build_id']==b['distribution_commit']==C['commit'] and b['pins']['emulationstation']==C['es_commit']
    payload=V/'input-tree';payload.mkdir();shutil.copytree(adapter,payload/'installed567')
    for name in ['run-guest.py','census.py']:shutil.copy2(R/name,payload/name)
    shutil.copy2(binding,payload/'binding.json')
    write(R/'records/input-files.json',{str(f.relative_to(payload)):sha(f) for f in sorted(payload.rglob('*')) if f.is_file()})
    for name,label in [('input','PIXINPUT'),('output','PIXOUTPUT')]:
        medium=V/(name+'.ext4')
        with medium.open('xb') as f:f.truncate(256*1024**2)
        call('media-'+name,['mkfs.ext4','-q','-F','-m','0','-L',label]+(['-d',payload] if name=='input' else [])+[medium],60)
    shutil.rmtree(payload)
    for name in ['input','output']:
        monitor('drive_add 0 if=none,id=pix'+name+',format=raw,'+('readonly=on,' if name=='input' else '')+'file='+str(V/(name+'.ext4')))
        monitor('device_add usb-storage,drive=pix'+name+',id=pix'+name+'dev,serial=pix'+name)
    serial('media','for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXOUTPUT && break; sleep 1; done; mkdir /tmp/pix-input /tmp/pix-output && mount -t ext4 -o ro,noload /dev/disk/by-label/PIXINPUT /tmp/pix-input && mount -t ext4 /dev/disk/by-label/PIXOUTPUT /tmp/pix-output')
    serial('guest-code','printf "%s  %s\\n" '+C['code']['run-guest.py']+' /tmp/pix-input/run-guest.py '+C['code']['census.py']+' /tmp/pix-input/census.py | sha256sum -c -')
    text=serial('installed567','python3 -I -S -B /tmp/pix-input/run-guest.py '+sha(binding),seconds=550);(R/'qa-serial.txt').write_text(text)
    text=serial('unmount','sync && umount /tmp/pix-output && umount /tmp/pix-input && sync');(R/'unmount.txt').write_text(text);result['rc']=0
except BaseException as error:result['error']=type(error).__name__+': '+str(error)
finally:
    signal.alarm(C['cleanup_seconds'])
    try:
        quiet=True
        try:reap_transport_children()
        except BaseException as error:quiet=False;result['cleanup_errors'].append('transport: '+str(error))
        if (V/'vm.pid').exists():
            if quiet:
                try:
                    text=serial('finally-flush','sync; if grep -q " /tmp/pix-output " /proc/mounts; then umount /tmp/pix-output; else true; fi; pxrc=$?; sync; exit "$pxrc"',seconds=30)
                    (R/'finally-flush.txt').write_text(text)
                except BaseException as error:result['cleanup_errors'].append('flush: '+str(error))
            try:(R/'vm-stop.log').write_text(call('vm-stop',[TREE/'tools/vm-stop',V/'vm.pid',disk],35))
            except BaseException as error:result['cleanup_errors'].append('stop: '+str(error))
        reap_transport_children();result['remaining_host_children']=direct_children(os.getpid())
        if result.get('forced_host_child_cleanup') or result['remaining_host_children']:result['cleanup_errors'].append('host child intervention or survivor')
    except BaseException as error:result['cleanup_errors'].append('finalizer: '+str(error))
    finally:
        signal.alarm(0)
        if result['cleanup_errors']:result['rc']=1
        result['ended']=time.time();write(R/'vm-result.json',result)
raise SystemExit(result['rc'])

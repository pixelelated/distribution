#!/usr/bin/env python3
"""UNRUN: one watched retained20->actual update->installed backup lifecycle.

Host call/serial/QEMU/stop patterns derive from installed-lifecycle 615bbece.
The corrected retained fixture and its four original phase clocks are unchanged.
"""
import base64,ctypes,gzip,hashlib,json,os,shlex,shutil,signal,socket,subprocess,sys,tarfile,time
from pathlib import Path
R=Path(__file__).resolve().parent;C=json.loads((R/'config.json').read_text());TREE=Path(C['checkout']);V=R/'vm';disk=V/'disk.qcow2'
result={'rc':1,'started':time.time(),'commands':[],'boots':[],'phases':[],'cleanup_errors':[]};sequence=0
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
assert sha(R/'census.py')==C['code']['census.py']
sys.path.insert(0,str(R))
from census import direct_children,signal_child
def reap_transport_children():
    # A timed-out run-phase timeout(1) may own a separate process group. The
    # unchanged qualified pidfd helper handles adopted children before another
    # serial client starts. The owned daemonized QEMU is stopped separately.
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
    marker='PIX_RETAINED_'+name.upper().replace('-','_')+'_RC:'
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
def phase(name,seconds):
    text=call('phase-'+name,['bash',R/'source/retained-corrected/run-phase.sh',TREE,R/'prepared',R/'phases'/name,V/'serial.sock',name],seconds)
    row=json.loads((R/'phases'/name/(name+'.result.json')).read_text());assert row['result']=='PASS'
    result['phases'].append({'phase':name,'result':'PASS','result_sha256':sha(R/'phases'/name/(name+'.result.json'))})
def boot_record(label):
    command="import json;from pathlib import Path;print('PIX_BOOT='+json.dumps({'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'os_release':Path('/etc/os-release').read_text(),'interfaces':sorted(p.name for p in Path('/sys/class/net').iterdir())}))"
    text=serial('boot-'+label,'python3 -I -S -B -c '+shlex.quote(command));row=json.loads(next(line.split('=',1)[1] for line in text.splitlines() if line.startswith('PIX_BOOT=')))
    assert row['interfaces']==['lo'];row['label']=label;result['boots'].append(row);write(R/'records'/('boot-'+label+'.json'),row);return row
def export_guest():
    # Only original value-free receipts; never settings, account values/hashes,
    # backup stdout/stderr or the synthetic backup archive.
    assert not result.get('guest_export_attempted');result['guest_export_attempted']=True
    names=['seed-started','seed','before','before-policy','after','after-policy','backup-child','backup']
    code="import base64,json;from pathlib import Path;root=Path("+repr('/storage/.cache/pixelelated-installed-state-'+C['id'])+");rows={}\nfor name in "+repr(names)+":\n p=root/(name+'.json')\n if p.exists():\n  assert p.is_file() and not p.is_symlink() and p.stat().st_size<=2097152\n  raw=p.read_bytes();json.loads(raw);rows[p.name]=base64.b64encode(raw).decode()\nprint('PIX_RECEIPTS='+json.dumps(rows,sort_keys=True))"
    encoded=base64.b64encode(code.encode()).decode()
    invocation='import base64;exec(compile(base64.b64decode('+repr(encoded)+'),"<retained-receipt-export>","exec"))'
    text=serial('receipt-export','python3 -I -S -B -c '+shlex.quote(invocation),seconds=40)
    rows=json.loads(next(line.split('=',1)[1] for line in text.splitlines() if line.startswith('PIX_RECEIPTS=')))
    assert set(rows)<=set(name+'.json' for name in names)
    for name,value in rows.items():
        raw=base64.b64decode(value,validate=True);assert len(raw)<=2*1024**2;(R/'guest'/name).write_bytes(raw)
    write(R/'guest-manifest.json',[{'path':name,'bytes':(R/'guest'/name).stat().st_size,'sha256':sha(R/'guest'/name)} for name in sorted(rows)])
def expired(*_):raise TimeoutError('whole retained lifecycle deadline or termination')
signal.signal(signal.SIGALRM,expired);signal.signal(signal.SIGTERM,expired);signal.alarm(C['work_seconds'])
try:
    assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
    os.environ['TMPDIR']=str(R/'reader-scratch')
    libc=ctypes.CDLL(None,use_errno=True);libc.prctl.restype=ctypes.c_int;assert libc.prctl(36,1,0,0,0)==0
    run=Path(os.environ['RASTERATOPS_BUILD_RUN']);run=run if run.is_absolute() else TREE/run;assert run.parent==TREE/'.build-runs'
    watcher=identity(int((run/'watcher.pid').read_text()));write(R/'records/watch-owner.json',{'run':str(run),'owner':identity(os.getpid()),'watcher':watcher,'work_seconds':C['work_seconds'],'cleanup_seconds':C['cleanup_seconds']})
    for path,digest in C['tools'].items():assert sha(Path(path))==digest
    for path,digest in C['code'].items():assert sha(R/path)==digest
    for path,digest in C['verification'].items():assert sha(Path(path))==digest
    assert call('source-head',['git','-C',TREE,'rev-parse','HEAD'],10).strip()==C['commit']
    for name in ['baseline','update','system']:assert sha(Path(C[name]['path']))==C[name]['sha256'],name
    archive=R/'source/correction.tar.gz';assert sha(archive)=='5e1255cbf9d22d1b2f0ff7b128be9f657d82be2d6e38870fccc284d7bc4111dd'
    correction=R/'source/correction';correction.mkdir()
    with tarfile.open(archive) as tar:
        members=tar.getmembers();assert sum(m.size for m in members)<=1024**2
        for m in members:
            name=Path(m.name);assert not name.is_absolute() and '..' not in name.parts and (m.isfile() or m.isdir())
            dest=correction/name
            if m.isdir():dest.mkdir(parents=True,exist_ok=True)
            else:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(tar.extractfile(m).read())
    assert sha(correction/'SHA256SUMS')=='bc4a76241fc24c40a61be59821c15ce5d9eb9514e4e8a34f203a5306b6431b08'
    for line in (correction/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);assert sha(correction/name)==digest
    call('materialize-correction',['python3','-I','-S','-B',correction/'materialize.py','--original',R/'source/retained-original','--output',R/'source/retained-corrected'],30)
    call('prepare-retained',['python3','-I','-B',R/'source/retained-corrected/prepare.py','--checkout',TREE,'--system',C['system']['path'],'--system-sha256',C['system']['sha256'],'--output',R/'prepared','--id',C['id']],450)
    with socket.socket() as s:s.bind(('127.0.0.1',5900+C['vnc']))
    raw=V/'disk.img';count=0
    with gzip.open(C['baseline']['path'],'rb') as source,raw.open('xb') as target:
        while chunk:=source.read(4*1024**2):
            count+=len(chunk);assert count<=16*1024**3
            if chunk.count(0)==len(chunk):target.seek(len(chunk),1)
            else:target.write(chunk)
        target.truncate()
    write(R/'records/baseline-inflation.json',{'compressed_sha256':C['baseline']['sha256'],'raw_bytes':count})
    call('convert',['qemu-img','convert','-f','raw','-O','qcow2',raw,disk],120);call('resize',['qemu-img','resize',disk,'16G'],30);raw.unlink()
    args=[disk,'--no-network','--headless','--daemonize','--gl','auto','--res','640x480','--vnc',str(C['vnc']),'--pidfile',V/'vm.pid','--serial',V/'serial.sock','--monitor',V/'monitor.sock','--ovmf-vars',V/'OVMF.fd']
    generated=shlex.split(call('qemu-args',[C['helper'],'qemu-args',*args],20))
    assert generated.count('-nic')==1 and generated[generated.index('-nic')+1]=='none' and '-netdev' not in generated and not any('hostfwd=' in arg for arg in generated)
    assert generated[generated.index('-m')+1]=='8192' and generated[generated.index('-smp')+1]=='4'
    write(R/'generated-640x480.json',generated);call('qemu-start',[C['helper'],'run',*args],60)
    qemu=identity(int((V/'vm.pid').read_text()));assert qemu['cmdline']==generated;write(R/'qemu.json',qemu)
    call('wait-baseline',[TREE/'tools/vm-serial','--socket',V/'serial.sock','wait','--up-to','240'],260)
    baseline_boot=boot_record('baseline');phase('seed',355);phase('before',235)
    medium=V/'input.ext4'
    with medium.open('xb') as f:f.truncate(C['input_media_bytes'])
    call('input-format',['mkfs.ext4','-q','-F','-m','0','-L','PIXUPDATE',medium],60)
    call('input-write',['debugfs','-w','-R','write '+C['update']['path']+' /update.tar',medium],180)
    monitor('drive_add 0 if=none,id=pixupdate,format=raw,readonly=on,file='+str(medium))
    monitor('device_add usb-storage,drive=pixupdate,id=pixupdatedev,serial=pixupdate')
    serial('mount-input','for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXUPDATE && break; sleep 1; done; mkdir /tmp/pix-retained-input && mount -t ext4 -o ro,noload /dev/disk/by-label/PIXUPDATE /tmp/pix-retained-input')
    staging="import os;from pathlib import Path;p=Path('/storage/.update');assert p.is_dir() and not any(p.iterdir());f=os.statvfs('/storage');assert f.f_bavail*f.f_frsize>="+str(C['guest_update_free_bytes'])
    serial('update-prerequisites','python3 -I -S -B -c '+shlex.quote(staging))
    destination='/storage/.update/'+Path(C['update']['path']).name
    serial('stage-update','printf "%s  %s\\n" '+C['update']['sha256']+' /tmp/pix-retained-input/update.tar | sha256sum -c - && cp /tmp/pix-retained-input/update.tar '+shlex.quote(destination)+' && printf "%s  %s\\n" '+C['update']['sha256']+' '+shlex.quote(destination)+' | sha256sum -c - && sync && umount /tmp/pix-retained-input',seconds=240)
    assert identity(qemu['pid'])==qemu
    serial('reboot-request','sync && systemctl reboot --no-block',seconds=30)
    test='[ "$(cat /proc/sys/kernel/random/boot_id)" != '+shlex.quote(baseline_boot['boot_id'])+' ] && grep -qx '+shlex.quote('BUILD_ID="'+C['commit']+'"')+' /etc/os-release && [ "$(pgrep emulationstation | wc -l)" = 1 ]'
    call('wait-updated',[TREE/'tools/vm-serial','--socket',V/'serial.sock','wait','--for',test,'--up-to','600'],620)
    updated=boot_record('candidate');assert updated['boot_id']!=baseline_boot['boot_id'] and identity(qemu['pid'])==qemu
    phase('after',235);phase('backup',475);export_guest()
    assert {p.name for p in (R/'guest').iterdir()}=={name+'.json' for name in ['seed-started','seed','before','before-policy','after','after-policy','backup-child','backup']}
    child=json.loads((R/'guest/backup-child.json').read_text());assert child=={'returncode':0,'timed_out':False}
    assert len(result['phases'])==4 and sha(Path(C['update']['path']))==C['update']['sha256'];result['rc']=0
except BaseException as error:result['error']=type(error).__name__+': '+str(error)
finally:
    signal.alarm(C['cleanup_seconds'])
    try:
        transport_quiet=True
        try:reap_transport_children()
        except BaseException as error:transport_quiet=False;result['cleanup_errors'].append('transport cleanup: '+str(error))
        if (V/'vm.pid').exists():
            if transport_quiet and not result.get('guest_export_attempted'):
                try:export_guest()
                except BaseException as error:result['cleanup_errors'].append('receipt export: '+str(error))
            if transport_quiet:
                try:serial('final-sync','sync',seconds=20)
                except BaseException as error:result['cleanup_errors'].append('sync: '+str(error))
            try:(R/'vm-stop.log').write_text(call('vm-stop',[TREE/'tools/vm-stop',V/'vm.pid',disk],35))
            except BaseException as error:result['cleanup_errors'].append('stop: '+str(error))
        reap_transport_children();result['remaining_host_children']=direct_children(os.getpid())
        if result.get('forced_host_child_cleanup') or result['remaining_host_children']:result['cleanup_errors'].append('host descendants required intervention or remain')
    except BaseException as error:result['cleanup_errors'].append('finalizer: '+str(error))
    finally:
        signal.alarm(0)
        if result['cleanup_errors']:result['rc']=1
        result['ended']=time.time();write(R/'vm-result.json',result)
raise SystemExit(result['rc'])

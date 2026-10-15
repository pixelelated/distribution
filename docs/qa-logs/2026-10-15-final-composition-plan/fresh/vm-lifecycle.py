#!/usr/bin/env python3
"""One admitted fresh no-NIC image: untouched clean-state gate, installed loader and exact stop."""
import base64,ctypes,gzip,hashlib,json,os,re,shlex,shutil,signal,socket,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;C=json.loads((R/'config.json').read_text());TREE=Path(C['checkout']);V=R/'vm';D=V/'disk.qcow2'
assert not (R/'vm-result.json').exists(),'fresh owner required'
result={'rc':1,'started':time.time(),'commands':[],'boots':[],'cleanup_errors':[]};sequence=0;next_sample=0;known={};qemu=None
def write(p,obj):
    with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert sha(R/'census.py')==C['code']['census.py']
sys.path.insert(0,str(R))
from census import direct_children,signal_child
def proc(pid):
    try:
        p=Path('/proc',str(pid));f=(p/'stat').read_text().rsplit(')',1)[1].split()
        if f[0]=='Z':return None
        return {'pid':pid,'ppid':int(f[1]),'pgid':int(f[2]),'sid':int(f[3]),'start_ticks':int(f[19]),'argv':[x.decode(errors='replace') for x in (p/'cmdline').read_bytes().split(b'\0') if x]}
    except (FileNotFoundError,ProcessLookupError):return None
def same(row):
    now=proc(row['pid']);return now if now and now['start_ticks']==row['start_ticks'] else None
def table():
    return {int(p.name):row for p in Path('/proc').iterdir() if p.name.isdigit() and (row:=proc(int(p.name)))}
def descendants(root,rows):
    found={root};previous=set()
    while found!=previous:
        previous=set(found);found.update(p for p,r in rows.items() if r['ppid'] in found)
    return found
def observe(child=None):
    global next_sample
    rows=table()
    selected=descendants(os.getpid(),rows)
    if child:selected.update(descendants(child,rows))
    selected.discard(os.getpid())
    for pid in selected:
        if pid in rows:
            row=rows[pid]
            # Daemonized QEMU is owned by vm-stop, independently of command descendants.
            if row['argv'] and Path(row['argv'][0]).name.startswith('qemu-system-') and 'if=none,id=rocknix,format=qcow2,file='+str(D) in row['argv']:continue
            known[(pid,row['start_ticks'])]=row
    files=[p for p in R.rglob('*') if not p.is_symlink() and p.is_file() and not p.is_relative_to(V)]
    total=0
    for p in files:
        try:total+=p.stat().st_size
        except FileNotFoundError:pass # temporary-file retirement is not observer failure
    assert total<=C['host_record_limit_bytes'] and len(files)<=4096,'host records/temporary output bound'
    if time.monotonic()>=next_sample:
        sample={'epoch':time.time(),'host_record_bytes':total,'host_record_files':len(files),'observed_command_processes':len(selected),'meminfo':Path('/proc/meminfo').read_text(),'memory_pressure':Path('/proc/pressure/memory').read_text(),'io_pressure':Path('/proc/pressure/io').read_text()}
        if qemu and same(qemu):sample['qemu_status']=Path('/proc',str(qemu['pid']),'status').read_text()
        with (R/'records/resources.jsonl').open('a') as f:f.write(json.dumps(sample)+'\n')
        next_sample=time.monotonic()+5
def owned_qemu(identity):
    if qemu and identity['pid']==qemu['pid'] and identity['start_ticks']==qemu['start_ticks']:return True
    row=proc(identity['pid'])
    return bool(row and row['argv'] and Path(row['argv'][0]).name.startswith('qemu-system-') and 'if=none,id=rocknix,format=qcow2,file='+str(D) in row['argv'])
def stop_children(active=None,keep_qemu=True):
    # The owner is a subreaper: detached descendants are adopted even between
    # observations. Never steal an outstanding Popen's original wait status.
    # The unchanged qualified helper signals identity-checked direct pidfds;
    # killing a parent exposes its adopted children for the next bounded census.
    deadline=time.monotonic()+13;interventions=[]
    while True:
        if active:active.poll()
        children=direct_children(os.getpid())
        for identity in children:
            if owned_qemu(identity) and (keep_qemu or proc(identity['pid'])):continue
            if active and identity['pid']==active.pid:continue
            try:pid,status=os.waitpid(identity['pid'],os.WNOHANG)
            except ChildProcessError:continue
            if pid:result.setdefault('reaped_host_children',[]).append({'pid':pid,'wait_status':status})
        children=[r for r in direct_children(os.getpid()) if not (owned_qemu(r) and (keep_qemu or proc(r['pid'])))]
        if not children:return interventions
        assert time.monotonic()<deadline,'owned host descendants survived bounded stop'
        for identity in children:
            row=proc(identity['pid'])
            if row:known[(row['pid'],row['start_ticks'])]=row
            intervention=signal_child(identity,os.getpid())
            if intervention['outcome']=='pidfd-kill':
                interventions.append(intervention)
                result.setdefault('forced_host_child_cleanup',[]).append(intervention)
        time.sleep(.02)
def call(name,args,seconds,check=True,input_path=None):
    global sequence
    sequence+=1;stem=R/'records'/('%03d-%s'%(sequence,name));row={'name':name,'argv':list(map(str,args)),'timeout_seconds':seconds,'timed_out':False,'original_returncode':None};result['commands'].append(row)
    child=None
    try:
        with Path(str(stem)+'.stdout').open('xb') as out,Path(str(stem)+'.stderr').open('xb') as err:
            data=input_path.open('rb') if input_path else subprocess.DEVNULL
            try:child=subprocess.Popen(row['argv'],stdin=data,stdout=out,stderr=err,start_new_session=True,env=dict(os.environ,TMPDIR=str(R/'host-tmp')))
            finally:
                if input_path:data.close()
            row['pid']=child.pid;deadline=time.monotonic()+seconds
            while child.poll() is None:
                observe(child.pid)
                assert Path(str(stem)+'.stdout').stat().st_size<=8*1024**2 and Path(str(stem)+'.stderr').stat().st_size<=8*1024**2,'command output bound'
                if time.monotonic()>=deadline:row['timed_out']=True;raise TimeoutError(name+' timed out')
                time.sleep(.25)
            row['original_returncode']=child.wait()
        if check:assert row['original_returncode']==0,name
        return Path(str(stem)+'.stdout').read_text()
    except BaseException as exc:
        row['error']=type(exc).__name__+': '+str(exc)
        if child:
            # Re-snapshot before stopping: transport children may use separate sessions.
            try:observe(child.pid)
            except BaseException:pass
            try:row['forced_host_cleanup']=stop_children(active=child)
            finally:row['original_returncode']=child.wait(timeout=3)
        raise
    finally:write(Path(str(stem)+'.exit.json'),row)
def serial(name,command,seconds=30):
    assert '\n' not in command and '\r' not in command,'single physical serial line required'
    marker='PIX_LOADER_'+name.upper().replace('-','_')+'_RC:'
    text=call(name,[TREE/'tools/vm-serial','--socket',V/'serial.sock','--timeout',str(seconds),'sh','( '+command+' ); pxrc=$?; printf "'+marker+'%s\\n" "$pxrc"'],seconds+15)
    matches=re.findall(re.escape(marker)+r'(-?\d+)\s*',text);assert matches==['0'],name
    return text
def monitor(command):
    with socket.socket(socket.AF_UNIX) as s:
        s.settimeout(5);s.connect(str(V/'monitor.sock'));s.recv(65536);s.sendall((command+'\n').encode());data=b''
        while b'(qemu)' not in data:
            chunk=s.recv(65536);assert chunk;data+=chunk;assert len(data)<=1024**2
    text=data.decode(errors='replace')
    with (R/'monitor.log').open('a') as f:f.write(command+'\n'+text+'\n')
    assert 'Error' not in text and 'failed' not in text.lower(),text
def export_loader(text):
    originals=[json.loads(base64.b64decode(x.split('=',1)[1],validate=True)) for x in text.splitlines() if x.startswith('PIX_LOADER_COMMAND=')]
    assert len(originals)<=3
    for i,row in enumerate(originals):write(R/'records'/('guest-command-%d.json'%i),row)
    rows=[x.split('=',1)[1] for x in text.splitlines() if x.startswith('PIX_RETAINED_LOADER=')];assert len(rows)==1
    raw=base64.b64decode(rows[0],validate=True);assert len(raw)<=8*1024**2
    record=json.loads(raw);(R/'records/guest-loader.json').write_bytes(raw+b'\n')
    registries=[x.split('=',1)[1] for x in text.splitlines() if x.startswith('PIX_LOADER_REGISTRY=')];assert len(registries)<=1
    if registries:
        registry=base64.b64decode(registries[0],validate=True);assert len(registry)<=2*1024**2
        (R/'records/gst-registry.bin').write_bytes(registry)
        assert len(registry)==record['registry']['bytes'] and hashlib.sha256(registry).hexdigest()==record['registry']['sha256']
    assert originals==record['checks'];return record
def expire(_sig,_frame):raise TimeoutError('full lifecycle deadline or termination')
signal.signal(signal.SIGALRM,expire);signal.signal(signal.SIGTERM,expire);signal.signal(signal.SIGINT,expire);signal.alarm(C['work_seconds'])
try:
    assert hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal')
    libc=ctypes.CDLL(None,use_errno=True);assert libc.prctl(36,1,0,0,0)==0,'set child subreaper'
    subreaper=ctypes.c_int();assert libc.prctl(37,ctypes.byref(subreaper),0,0,0)==0 and subreaper.value==1,'read back child subreaper'
    result['child_subreaper']=True
    assert Path('/proc/self/ns/pid').stat().st_ino==C['host_pid_namespace'],'actual host PID namespace'
    run=Path(os.environ['RASTERATOPS_BUILD_RUN']);run=run if run.is_absolute() else TREE/run
    assert run.parent==TREE/'.build-runs';admission=json.loads((run/'admission.json').read_text())
    assert admission['source']['head']==C['commit'] and admission['submission_owner']==str(R/'lifecycle-owner')
    (R/'run.path').write_text(str(run)+'\n');write(R/'records/watch-owner.json',{'run':str(run),'owner':proc(os.getpid()),'watcher':proc(int((run/'watcher.pid').read_text())),'work_seconds':C['work_seconds'],'cleanup_seconds':C['cleanup_seconds']})
    for n,h in C['tools'].items():assert sha(Path(n))==h,n
    for n,h in C['code'].items():assert sha(R/n)==h,n
    assert sha(R/'records/final-result.json')==C['verification_sha256'] and sha(R/'records/final-inputs.json')==C['inputs_sha256']
    assert call('source',['git','-C',TREE,'rev-parse','HEAD'],10).strip()==C['commit']
    image=Path(C['image']['path']);assert image.stat().st_size==C['image']['bytes'] and sha(image)==C['image']['sha256']
    raw=V/'disk.img';count=0
    with gzip.open(image,'rb') as source,raw.open('xb') as target:
        while chunk:=source.read(4*1024**2):
            count+=len(chunk);assert count<=16*1024**3
            if chunk.count(0)==len(chunk):target.seek(len(chunk),1)
            else:target.write(chunk)
        target.truncate()
    call('convert',['qemu-img','convert','-f','raw','-O','qcow2',raw,D],120)
    call('resize',['qemu-img','resize',D,'16G'],30);raw.unlink()
    with socket.socket() as s:s.bind(('127.0.0.1',5900+C['vnc']))
    args=[D,'--no-network','--headless','--daemonize','--gl','auto','--res','640x480','--vnc',str(C['vnc']),'--pidfile',V/'vm.pid','--serial',V/'serial.sock','--monitor',V/'monitor.sock','--ovmf-vars',V/'OVMF.fd']
    generated=shlex.split(call('qemu-args',[C['helper'],'qemu-args',*args],20))
    assert generated[generated.index('-m')+1]=='8192' and generated[generated.index('-smp')+1]=='4'
    assert generated.count('-nic')==1 and generated[generated.index('-nic')+1]=='none' and '-netdev' not in generated and not any('hostfwd=' in x for x in generated)
    assert '-append' not in generated and '-kernel' not in generated
    write(R/'records/qemu-generated.json',generated);call('qemu-start',[C['helper'],'run',*args],60)
    qemu=proc(int((V/'vm.pid').read_text()));assert qemu and qemu['argv']==generated
    result['boots'].append(qemu);write(R/'records/qemu-start.json',qemu)
    call('serial-ready',[TREE/'tools/vm-serial','--socket',V/'serial.sock','wait','--up-to','240'],260)
    # Original corrected clean gate runs before helper media, SSH, synthetic config or library.
    call('untouched-clean',['bash',C['clean_helper'],R/'clean',V/'serial.sock'],210)
    clean=(R/'clean/first-boot.serial').read_text();start=clean.index('{\n');report,end=json.JSONDecoder().raw_decode(clean[start:])
    assert report['schema']==1 and report['policy']=='pixelelated-selected-state-v1' and report['mode']=='first-boot' and report['status']=='pass' and report['blocked_count']==report['error_count']==0
    assert any(x.get('category')=='boot-ready' and x.get('status')=='clear' and x.get('present') is True for x in report['checks'])
    assert clean.count('PIX_STATE_565_RC=')==1 and 'PIX_STATE_565_RC=0' in clean
    (R/'clean/report.json').write_text(clean[start:][:end]+'\n')
    code="import json;from pathlib import Path;print('PIX_CLEAN_BOOT='+json.dumps({'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'os_release':Path('/etc/os-release').read_text(),'interfaces':sorted(p.name for p in Path('/sys/class/net').iterdir())}))"
    text=serial('boot','python3 -I -S -B -c '+shlex.quote(code));boot=json.loads(next(x.split('=',1)[1] for x in text.splitlines() if x.startswith('PIX_CLEAN_BOOT=')))
    assert boot['interfaces']==['lo'] and 'BUILD_ID="'+C['commit']+'"' in boot['os_release'];write(R/'records/boot.json',boot)
    payload={key:C[key] for key in ['commit','es_commit','members']}
    code='CONFIG='+repr(payload)+'\n'+(R/'guest.py').read_text()
    import zlib
    encoded=base64.b64encode(zlib.compress(code.encode(),9)).decode()
    invoke='import base64,zlib;exec(compile(zlib.decompress(base64.b64decode('+repr(encoded)+')),"<bound-fresh-loader>","exec"))'
    command='python3 -I -S -B -c '+shlex.quote(invoke)
    assert '\n' not in command and '\r' not in command
    # Record the actual guest status independently of the serial transport;
    # parse/export originals before deciding success, including ordinary failure.
    marker='PIX_LOADER_PROBE_RC:'
    text=call('installed-loader',[TREE/'tools/vm-serial','--socket',V/'serial.sock','--timeout','130','sh','( '+command+' ); pxrc=$?; printf "'+marker+'%s\\n" "$pxrc"'],150)
    guest=export_loader(text);statuses=re.findall(re.escape(marker)+r'(-?\d+)\s*',text);write(R/'records/guest-exit.json',{'reported_statuses':statuses,'transport_returncode':result['commands'][-1]['original_returncode']})
    assert statuses==['0'] and guest['status']=='PASS' and not guest['cleanup_errors'] and guest['selected_bytes_and_modes_equal'] and guest['private_runtime_removed']
    assert all(r['original_returncode']==0 and not r['timed_out'] for r in guest['checks'])
    assert len(guest['checks'])==3 and guest['rtld_now']=='PASS' and guest['boot_id']==boot['boot_id']
    result['rc']=0
except BaseException as exc:result['error']=type(exc).__name__+': '+str(exc)
finally:
    signal.alarm(C['cleanup_seconds'])
    try:
        try:observe()
        except BaseException as exc:result['cleanup_errors'].append('observer: '+str(exc))
        try:
            interventions=stop_children();result['forced_host_cleanup']=interventions
            if interventions:result['rc']=1
        except BaseException as exc:result['cleanup_errors'].append('host children: '+str(exc))
        if (V/'vm.pid').exists():
            try:serial('final-sync','sync',seconds=15)
            except BaseException as exc:result['cleanup_errors'].append('sync: '+str(exc))
            try:
                text=call('vm-stop',[TREE/'tools/vm-stop',V/'vm.pid',D],35)
                assert 'down: owned QEMU exited' in text
            except BaseException as exc:result['cleanup_errors'].append('VM stop: '+str(exc))
        try:
            stop_children(keep_qemu=bool(qemu and same(qemu)));result['remaining_host_children']=direct_children(os.getpid())
            if result['remaining_host_children']:result['cleanup_errors'].append('remaining owned host children')
        except BaseException as exc:result['cleanup_errors'].append('final child census: '+str(exc))
    finally:
        signal.alarm(0)
        survivors=[r for r in known.values() if same(r)];result['surviving_host_processes']=survivors;result['qemu_still_live']=bool(qemu and same(qemu))
        if survivors or result['qemu_still_live'] or result['cleanup_errors'] or result.get('forced_host_child_cleanup'):result['rc']=1
        result['ended']=time.time();write(R/'records/host-process-identities.json',list(known.values()));write(R/'vm-result.json',result)
raise SystemExit(result['rc'])

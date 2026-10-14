#!/usr/bin/env python3
"""One admitted default-boot guest: clean proof, unchanged installed UI smoke, exact stop."""
import ctypes,gzip,hashlib,json,os,re,shlex,signal,socket,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;C=json.loads((R/'config.json').read_text());TREE=Path(C['checkout']);V=R/'vm';D=V/'disk.qcow2'
assert not (R/'vm-result.json').exists(),'fresh owner required'
result={'rc':1,'started':time.time(),'commands':[],'boots':[],'cleanup_errors':[]};sequence=0;ssh=None;next_sample=0;known={};qemu=None
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
    # Private browser TMPDIR and exact SSH key also identify orphaned children.
    for pid,row in rows.items():
        if any(a==str(V/'qa-key') or a.startswith(str(R/'host-tmp')+'/') or a.startswith('--user-data-dir='+str(R/'host-tmp')+'/') or a.startswith(str(R/'smoke')+'/') for a in row['argv']):selected.add(pid)
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
        except FileNotFoundError:pass # browser temporary-file retirement is not observer failure
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
            # Re-snapshot before stopping: stages, Playwright and tunnel use separate sessions.
            try:observe(child.pid)
            except BaseException:pass
            try:row['forced_host_cleanup']=stop_children(active=child)
            finally:row['original_returncode']=child.wait(timeout=3)
        raise
    finally:write(Path(str(stem)+'.exit.json'),row)
def serial(name,command,seconds=30):
    assert '\n' not in command and '\r' not in command,'single physical serial line required'
    marker='PIX_UI_'+name.upper().replace('-','_')+'_RC:'
    text=call(name,[TREE/'tools/vm-serial','--socket',V/'serial.sock','--timeout',str(seconds),'sh','( '+command+' ); pxrc=$?; printf "'+marker+'%s\\n" "$pxrc"'],seconds+15)
    matches=re.findall(re.escape(marker)+r'(-?\d+)\s*',text);assert matches==['0'],name
    return text
def expire(_sig,_frame):raise TimeoutError('full lifecycle deadline or termination')
signal.signal(signal.SIGALRM,expire);signal.signal(signal.SIGTERM,expire);signal.signal(signal.SIGINT,expire);signal.alarm(C['work_seconds'])
try:
    assert hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal')
    libc=ctypes.CDLL(None,use_errno=True);assert libc.prctl(36,1,0,0,0)==0,'set child subreaper'
    subreaper=ctypes.c_int();assert libc.prctl(37,ctypes.byref(subreaper),0,0,0)==0 and subreaper.value==1,'read back child subreaper'
    result['child_subreaper']=True
    assert Path('/proc/self/ns/pid').stat().st_ino==C['host_pid_namespace'],'use original host PID namespace'
    run=Path(os.environ['RASTERATOPS_BUILD_RUN']);run=run if run.is_absolute() else TREE/run
    assert run.parent==TREE/'.build-runs';admission=json.loads((run/'admission.json').read_text())
    assert admission['source']['head']==C['commit'] and admission['submission_owner']==str(R/'lifecycle-owner')
    (R/'run.path').write_text(str(run)+'\n');write(R/'records/watch-owner.json',{'run':str(run),'owner':proc(os.getpid()),'watcher':proc(int((run/'watcher.pid').read_text())),'work_seconds':C['work_seconds'],'smoke_seconds':C['smoke_seconds'],'cleanup_seconds':C['cleanup_seconds']})
    for n,h in C['tools'].items():assert sha(Path(n))==h,n
    for n,h in C['dependencies'].items():assert sha(Path(n))==h,n
    for n,h in C['code'].items():assert sha(R/n)==h,n
    assert call('source',['git','-C',TREE,'rev-parse','HEAD'],10).strip()==C['commit']
    assert sha(R/'records/image-verification.original.json')==C['verification_sha256']
    assert sha(R/'records/image-inputs.original.json')==C['image_inputs_sha256']
    for port in [C['ssh_port'],5900+C['vnc'],18080]:
        with socket.socket() as s:s.bind(('127.0.0.1',port))
    (R/'host-tmp').mkdir(mode=0o700)
    image=Path(C['image']['path']);assert sha(image)==C['image']['sha256'] and image.stat().st_size==C['image']['bytes']
    raw=V/'disk.img';count=0
    with gzip.open(image,'rb') as src,raw.open('xb') as dst:
        while chunk:=src.read(4*1024**2):
            count+=len(chunk);assert count<=C['image']['raw_bytes']
            if chunk.count(0)==len(chunk):dst.seek(len(chunk),1)
            else:dst.write(chunk)
        dst.truncate()
    assert count==C['image']['raw_bytes']
    call('convert',['qemu-img','convert','-f','raw','-O','qcow2',raw,D],90);call('resize',['qemu-img','resize',D,'16G'],30);raw.unlink()
    args=[D,'--net','user','--headless','--daemonize','--gl','auto','--res','640x480','--ssh-port',str(C['ssh_port']),'--vnc',str(C['vnc']),'--pidfile',V/'vm.pid','--serial',V/'serial.sock','--monitor',V/'monitor.sock','--ovmf-vars',V/'OVMF.fd']
    generated=shlex.split(call('qemu-args',[C['helper'],'qemu-args',*args],20))
    assert generated[generated.index('-m')+1]=='8192' and generated[generated.index('-smp')+1]=='4'
    assert generated[generated.index('-netdev')+1]=='user,id=net0,hostfwd=tcp:127.0.0.1:'+str(C['ssh_port'])+'-:22'
    assert '-append' not in generated and '-kernel' not in generated
    write(R/'records/qemu-generated.json',generated);call('qemu-start',[C['helper'],'run',*args],60)
    qemu=proc(int((V/'vm.pid').read_text()));assert qemu and qemu['argv']==generated
    result['boots'].append(qemu);write(R/'records/qemu-start.json',qemu)
    call('serial-ready',[TREE/'tools/vm-serial','--socket',V/'serial.sock','wait','--up-to','240'],260)
    # No SSH key, helper media, synthetic config or fixture library exists before this proof.
    call('untouched-clean',['bash',TREE/'docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh',R/'clean',V/'serial.sock'],210)
    clean=(R/'clean/first-boot.serial').read_text();start=clean.index('{\n');report,end=json.JSONDecoder().raw_decode(clean[start:])
    assert report['schema']==1 and report['policy']=='pixelelated-selected-state-v1' and report['mode']=='first-boot' and report['status']=='pass' and report['blocked_count']==report['error_count']==0
    assert any(x.get('category')=='boot-ready' and x.get('status')=='clear' and x.get('present') is True for x in report['checks'])
    assert clean.count('PIX_STATE_565_RC=')==1 and 'PIX_STATE_565_RC=0' in clean
    (R/'clean/report.json').write_text(clean[start:][:end]+'\n')
    code="import json;from pathlib import Path;print('PIX_UI_BOOT='+json.dumps({'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'cmdline':Path('/proc/cmdline').read_text().strip(),'os_release':Path('/etc/os-release').read_text()}))"
    text=serial('boot','python3 -I -S -B -c '+shlex.quote(code));boot=json.loads(next(x.split('=',1)[1] for x in text.splitlines() if x.startswith('PIX_UI_BOOT=')));assert 'BUILD_ID="'+C['commit']+'"' in boot['os_release'];write(R/'records/boot.json',boot)
    # Reuse only accepted QA SSH provisioning. No old provision.py/product overlay.
    call('keygen',['ssh-keygen','-q','-t','ed25519','-N','','-f',V/'qa-key','-C','pix-installed-ui-synthetic'],20)
    public=(V/'qa-key.pub').read_text().strip();assert public.startswith('ssh-ed25519 ') and '\n' not in public
    serial('ssh-provision',"set -e; test ! -s /storage/.ssh/authorized_keys; mkdir -p /storage/.ssh /storage/.cache/services; chmod 700 /storage/.ssh; printf '%s\\n' "+shlex.quote(public)+" > /storage/.ssh/authorized_keys; chmod 600 /storage/.ssh/authorized_keys; touch /storage/.cache/services/sshd.conf; systemctl start sshd.service; systemctl is-active --quiet sshd.service")
    text=serial('ssh-host-key',"set -e; printf 'PIX_UI_HOSTKEY='; cat /storage/.cache/ssh/ssh_host_ed25519_key.pub")
    host=next(x.split('=',1)[1] for x in text.splitlines() if x.startswith('PIX_UI_HOSTKEY='));kind,key,*_=host.split();assert kind=='ssh-ed25519' and re.fullmatch('[A-Za-z0-9+/=]+',key)
    (V/'known_hosts').write_text('[127.0.0.1]:'+str(C['ssh_port'])+' '+kind+' '+key+'\n')
    ssh=['ssh','-i',str(V/'qa-key'),'-p',str(C['ssh_port']),'-o','BatchMode=yes','-o','IdentitiesOnly=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(V/'known_hosts'),'-o','ControlMaster=no','-o','ControlPath=none','root@127.0.0.1'];write(R/'ssh-command.json',ssh)
    assert call('ssh-boot',ssh+['cat /proc/sys/kernel/random/boot_id'],20).strip()==boot['boot_id']
    # Existing preparer validates all installed members, original packet and dependency hashes.
    call('prepare-smoke',['python3','-I','-B',R/'source/smoke/prepare.py','--image-verification',R/'records/image-verification.original.json','--ssh-command',R/'ssh-command.json','--monitor',V/'monitor.sock','--playwright-python',C['playwright_python'],'--chromium',C['chromium'],'--out',R/'smoke'],60)
    call('original-smoke',['python3','-B',R/'smoke/run.py'],C['smoke_seconds'])
    smoke=json.loads((R/'smoke/result.json').read_text());assert smoke['status']=='PASS' and smoke['cleanup']=='PASS' and not smoke.get('cleanup_error')
    assert smoke['boot_id']==boot['boot_id'] and all(x['original_returncode']==0 and not x['timed_out'] and not x.get('output_guard') and not x.get('observer_error') for x in smoke['stages'])
    text=call('guest-postcheck',ssh+['. /etc/profile >/dev/null 2>&1; python3 -I -S -B -'],30,input_path=R/'guest-postcheck.py')
    post=json.loads(text);assert post['status']=='PASS' and post['boot_id']==boot['boot_id'];write(R/'records/guest-postcheck.json',post)
    result['rc']=0
except BaseException as exc:result['error']=type(exc).__name__+': '+str(exc)
finally:
    signal.alarm(C['cleanup_seconds'])
    # Stop observed host cases/tunnels/browser descendants before ending their guest.
    try:
        try:observe()
        except BaseException as exc:result['cleanup_errors'].append('observer: '+str(exc))
        try:
            interventions=stop_children();result['forced_host_cleanup']=interventions
            if interventions:result['rc']=1
        except BaseException as exc:result['cleanup_errors'].append('host children: '+str(exc))
        if (V/'vm.pid').exists():
            # On a failed smoke this is best-effort readback, never restoration success.
            if ssh:
                try:call('final-sync',ssh+['sync'],12)
                except BaseException as exc:result['cleanup_errors'].append('sync: '+str(exc))
            try:call('vm-stop',[TREE/'tools/vm-stop',V/'vm.pid',D],35)
            except BaseException as exc:result['cleanup_errors'].append('VM stop: '+str(exc))
        try:
            # Reap the separately stopped QEMU and any adopted final transport.
            # A still-live QEMU remains vm-stop's responsibility, never child kill.
            stop_children(keep_qemu=bool(qemu and same(qemu)))
            result['remaining_host_children']=direct_children(os.getpid())
            if result['remaining_host_children']:result['cleanup_errors'].append('remaining owned host children')
        except BaseException as exc:result['cleanup_errors'].append('final child census: '+str(exc))
    finally:
        signal.alarm(0)
        survivors=[r for r in known.values() if same(r)]
        result['surviving_host_processes']=survivors
        result['qemu_still_live']=bool(qemu and same(qemu))
        if survivors or result['qemu_still_live'] or result['cleanup_errors'] or result.get('forced_host_child_cleanup'):result['rc']=1
        result['ended']=time.time();write(R/'records/host-process-identities.json',list(known.values()));write(R/'vm-result.json',result)
raise SystemExit(result['rc'])

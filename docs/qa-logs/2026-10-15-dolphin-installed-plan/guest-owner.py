#!/usr/bin/env python3
"""UNRUN derivative of qualified #584 owner: three installed Dolphin startup observations, then compact export."""
import ctypes,hashlib,json,os,shutil,signal,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from census import direct_children,proc_identity,signal_child
R=Path('/run/pix-installed-native');OUT=Path('/tmp/pix-output/native-owner')
def require(ok,message):
    if not ok:raise AssertionError(message)
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def main():
    require(len(sys.argv)==2,'one final verification SHA argument required')
    require(os.geteuid()==0 and sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo'],'allocated root no-NIC guest required')
    require(os.statvfs(HERE).f_flag&os.ST_RDONLY,'read-only source media required')
    binding=json.loads((HERE/'binding.json').read_text())
    for name,digest in binding['owner_files'].items():require(sha(HERE/name)==digest,'owner code changed: '+name)
    packet=HERE.parent/'packet'
    require(sha(packet/'SHA256SUMS')==binding['case_seal'],'case seal changed')
    for line in (packet/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);require(sha(packet/name)==digest,'case source changed: '+name)
    require(sha(HERE.parent/'final-image-result.json')==sys.argv[1]==binding['verification_sha256'],'final verifier changed')
    require(R.is_dir() and not any(R.iterdir()),'fresh mounted scratch required')
    mounts=[x for x in Path('/proc/self/mountinfo').read_text().splitlines() if x.split()[4]==str(R)]
    require(len(mounts)==1 and mounts[0].split(' - ')[1].split()[0]=='tmpfs' and 'noexec' not in mounts[0].split()[5].split(','),'dedicated executable tmpfs required')
    fs=os.statvfs(R);require(fs.f_blocks*fs.f_frsize<=256*1024**2 and fs.f_bavail*fs.f_frsize>=200*1024**2,'scratch must provide200-256MiB')
    OUT.mkdir(mode=0o700);started=time.monotonic();child=None;parent=os.getpid()
    report={'status':'FAIL','original_child_exit':None,'timed_out':False,'signals':[],'cleanup_errors':[],'reaped':[],
            'owner_identity':proc_identity(parent),'case_seal':binding['case_seal'],'verification_sha256':sys.argv[1],
            'limits':{'work_seconds':180,'cleanup_seconds':10,'export_seconds':20,'total_seconds':210}}
    libc=ctypes.CDLL(None,use_errno=True);libc.prctl.restype=ctypes.c_int
    def preexec():
        if libc.prctl(1,signal.SIGKILL,0,0,0)!=0 or os.getppid()!=parent:os._exit(125)
    def terminated(*_):raise TimeoutError('owner deadline or termination')
    signal.signal(signal.SIGTERM,terminated);signal.signal(signal.SIGALRM,terminated);signal.alarm(180)
    try:
        require(hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal'),'pidfd support required')
        require(libc.prctl(36,1,0,0,0)==0,'subreaper setup failed')
        argv=['/bin/bash',str(packet/'run-guest.sh'),sys.argv[1]];report['argv']=argv
        with (OUT/'case.stdout').open('xb') as stdout,(OUT/'case.stderr').open('xb') as stderr:
            child=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,start_new_session=True,preexec_fn=preexec)
            report['child_identity']=proc_identity(child.pid)
            try:report['original_child_exit']=child.wait(timeout=180)
            except subprocess.TimeoutExpired:report['timed_out']=True;raise
        require(report['original_child_exit']==0,'original case failed; no retry')
        observed=json.loads((R/'result.json').read_text())
        require(observed['status']=='PASS' and len(observed['rows'])==3,'startup proof did not pass')
        report['status']='PASS'
    except BaseException as exc:
        report['error']=type(exc).__name__+': '+str(exc)
        if isinstance(exc,(TimeoutError,subprocess.TimeoutExpired)):report['timed_out']=True
    finally:
        signal.alarm(10)
        try:
            if child is not None and child.poll() is None:
                identity=proc_identity(child.pid);require(identity is not None,'live case identity unavailable')
                report['signals'].append(signal_child(identity,parent));report['original_child_exit']=child.wait(timeout=2)
            deadline=time.monotonic()+5
            while True:
                while True:
                    try:pid,status=os.waitpid(-1,os.WNOHANG)
                    except ChildProcessError:break
                    if not pid:break
                    report['reaped'].append({'pid':pid,'wait_status':status})
                children=direct_children(parent)
                if not children:break
                require(time.monotonic()<deadline,'descendant cleanup deadline')
                for identity in children:report['signals'].append(signal_child(identity,parent))
                time.sleep(.02)
            report['remaining_children']=direct_children(parent)
        except BaseException as exc:
            report['remaining_children']=None;report['cleanup_errors'].append(str(exc))
        if report['signals'] or report['cleanup_errors'] or report['reaped'] or report.get('remaining_children')!=[]:report['status']='FAIL'
        signal.alarm(20)
        try:
            # Retain original small channels, installed-resource readbacks and the self-authored DOL.
            copied=[];total=0
            for path in sorted(R.rglob('*')):
                if not path.is_file():continue
                require(not path.is_symlink(),'unexpected scratch symlink')
                name=path.relative_to(R)
                if name.parts[:2]==('preparation','writer-files'):continue
                size=path.stat().st_size;total+=size
                require(size<=64*1024**2 and total<=192*1024**2,'compact export bound exceeded')
                dest=OUT/'case'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
                require(sha(path)==sha(dest),'copy differs')
                copied.append({'path':str(Path('case')/name),'bytes':size,'sha256':sha(dest)})
            report['copied_case_files']=copied
        except BaseException as exc:report['status']='FAIL';report['cleanup_errors'].append('export: '+str(exc))
        signal.alarm(0);report['elapsed_seconds']=time.monotonic()-started
        (OUT/'owner-result.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'status':report['status'],'original_child_exit':report['original_child_exit']}),flush=True)
    return 0 if report['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

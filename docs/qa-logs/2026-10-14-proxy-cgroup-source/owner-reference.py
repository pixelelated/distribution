#!/usr/bin/env python3
"""HELD: one native integration child; original exit and bounded pidfd cleanup."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent


def require(value,message):
    if not value:raise AssertionError(message)


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission',type=Path,required=True)
    parser.add_argument('--admission-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    root=Path('/run/pix583-native-owner');out=args.output.absolute()
    require(root.resolve(strict=True)==root and out.parent==root and not out.exists(),'fresh allocated owner output required')
    require(set(p.name for p in Path('/sys/class/net').iterdir())=={'lo'},'owner requires allocated no-NIC guest')
    require(sha(args.admission)==args.admission_sha256,'admission changed before owner launch')
    seal=json.loads((HERE.parent/'runner-seal.json').read_text())
    for name,digest in seal.items():require(sha(HERE/name)==digest,'runner source changed: '+name)
    sys.path.insert(0,str(HERE))
    from census import direct_children,proc_identity,signal_child
    out.mkdir(mode=0o700);started=time.monotonic();child=None;parent=os.getpid()
    report={'status':'FAIL','original_child_exit':None,'timed_out':False,'signals':[],
            'cleanup_errors':[],'reaped':[],'runner_sha256':seal,'owner_identity':proc_identity(parent)}
    libc=ctypes.CDLL(None,use_errno=True);libc.prctl.restype=ctypes.c_int
    def preexec():
        # No threads exist here. Prevent an orphaned native child if this owner dies.
        if libc.prctl(1,signal.SIGKILL,0,0,0)!=0 or os.getppid()!=parent:os._exit(125)
    try:
        require(hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal'),'pidfd support required')
        require(libc.prctl(36,1,0,0,0)==0,'subreaper setup failed')
        argv=[sys.executable,'-I','-S','-B',str(HERE/'run.py'),'--admission',str(args.admission),
              '--admission-sha256',args.admission_sha256,'--output',str(out/'payload')]
        report['argv']=argv
        with (out/'stdout').open('xb') as stdout,(out/'stderr').open('xb') as stderr:
            child=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                                   start_new_session=True,preexec_fn=preexec)
            report['child_identity']=proc_identity(child.pid)
            try:report['original_child_exit']=child.wait(timeout=190)
            except subprocess.TimeoutExpired:
                report['timed_out']=True
                identity=proc_identity(child.pid)
                require(identity is not None,'timed-out child identity unavailable')
                report['signals'].append(signal_child(identity,parent))
                report['original_child_exit']=child.wait(timeout=2)
        payload=json.loads((out/'payload/result.json').read_text())
        require(report['original_child_exit']==0 and payload['status']=='PASS' and not report['timed_out'],
                'original integration child failed; no retry')
        report['status']='PASS'
    except BaseException as error:
        report['error']=type(error).__name__+': '+str(error)
    finally:
        # The native child is reaped through Popen first, preserving its real exit.
        if child is not None and child.poll() is None:
            try:
                identity=proc_identity(child.pid)
                require(identity is not None,'live child identity unavailable')
                report['signals'].append(signal_child(identity,parent))
                report['original_child_exit']=child.wait(timeout=2)
            except BaseException as error:report['cleanup_errors'].append(str(error))
        deadline=time.monotonic()+3
        try:
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
                time.sleep(0.02)
            report['remaining_children']=direct_children(parent)
        except BaseException as error:
            report['remaining_children']=None;report['cleanup_errors'].append(str(error))
        if report['signals'] or report['cleanup_errors'] or report['reaped'] or report.get('remaining_children')!=[]:
            report['status']='FAIL'
        report['elapsed_seconds']=time.monotonic()-started
        try:
            report['artifacts']={str(p.relative_to(out)):{'bytes':p.stat().st_size,'sha256':sha(p)}
                                 for p in sorted(out.rglob('*')) if p.is_file()}
        except BaseException as error:
            report['status']='FAIL';report['artifact_observation_error']=str(error)
        try:(out/'owner-result.json').write_text(json.dumps(report,indent=2)+'\n')
        except BaseException as error:
            report['status']='FAIL';report['receipt_error']=str(error);print(json.dumps(report),flush=True);raise
        print(json.dumps({'status':report['status'],'owner_result':str(out/'owner-result.json')}),flush=True)
    return 0 if report['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""UNRUN fresh no-NIC VM owner. One 240s budget includes up to 5s cleanup."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from guest_support import HERE,INPUT,OUTPUT,SCRATCH,LIMIT,census,descendants,identity,read,require,same,sha,usage,verify_packet,write


def preflight(run_id):
    require(sys.version_info>=(3,11),'immutable oracle requires Python 3.11 hashlib.file_digest')
    require(os.geteuid()==0 and sys.platform=='linux' and os.uname().machine=='x86_64','disposable x86_64 Linux guest root required')
    require(HERE==INPUT/'owner','run the exact read-only public packet path')
    require(sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo'],'no-NIC guest required')
    require(INPUT.resolve()==INPUT and os.statvfs(INPUT).f_flag&os.ST_RDONLY,'read-only public input required')
    verify_packet()
    require(SCRATCH.resolve()==SCRATCH and SCRATCH.is_dir() and not list(SCRATCH.iterdir()),'fresh empty private scratch required')
    rows=[]
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        left,right=line.split(' - ',1);fields=left.split();tail=right.split()
        if fields[4]==str(SCRATCH):rows.append((fields,tail))
    require(len(rows)==1,'scratch needs its own mount')
    fields,tail=rows[0];flags=set(fields[5].split(','))
    require(tail[0]=='tmpfs' and 'rw' in flags and 'noexec' not in flags,'scratch must be executable writable tmpfs')
    fs=os.statvfs(SCRATCH)
    require(128*1024**2<=fs.f_blocks*fs.f_frsize<=LIMIT and fs.f_bavail*fs.f_frsize>=128*1024**2,'scratch must be bounded to 2GiB with 128MiB free')
    require(SCRATCH.stat().st_mode&0o777==0o700,'private scratch mode must be 0700')
    require(OUTPUT.resolve()==OUTPUT and OUTPUT.is_dir() and not os.statvfs(OUTPUT).f_flag&os.ST_RDONLY,'real writable output directory required')
    staged=Path('/tmp')/('pix574-dolphin-'+run_id)
    require(not staged.exists() and not staged.is_symlink() and not staged.with_suffix('.stage.json').exists(),'run ID already used by stager')
    return staged


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id',required=True)
    args=parser.parse_args();require(re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,47}',args.run_id),'fresh simple run ID required')
    started=time.monotonic();deadline=started+235;cleanup_deadline=started+240
    os.umask(0o077)
    staged=preflight(args.run_id)
    out=OUTPUT/('pix574-chd-owner-'+args.run_id);out.mkdir(mode=0o700)
    # Every adopted orphan remains attributable even when bounded.py starts a
    # new session. The coordinator still owns VM retirement after any hard kill.
    libc=ctypes.CDLL(None,use_errno=True)
    require(libc.prctl(36,1,0,0,0)==0,'PR_SET_CHILD_SUBREAPER failed')
    owner=identity(os.getpid());boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    write(out/'owner.json',dict(identity=owner,boot_id=boot,started_monotonic=started,
        work_deadline=deadline,total_deadline=cleanup_deadline,private_limit=LIMIT,
        packet_manifest_sha256=sha(HERE/'SHA256SUMS'),network_interfaces=['lo'],subreaper=True,
        uid=os.geteuid(),synthetic_home=str(SCRATCH/'home'),os_uid_remains_guest_root=True))
    known={};reaped=[];actions=[];child=None;error=None;interrupted=[];forced=False
    samples=(out/'samples.jsonl').open('x');last_sample=0
    def stop(signum,frame):interrupted.append(signum)
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,stop)

    def observe():
        rows=census();owned=descendants(rows,os.getpid())
        for pid,row in owned.items():
            key=(pid,row['start_ticks'])
            if key not in known:
                record=dict(row)
                try:record['argv']=Path('/proc',str(pid),'cmdline').read_bytes().decode(errors='replace').split('\0')[:-1]
                except FileNotFoundError:record['argv']=[]
                known[key]=record
        return rows,owned

    def reap():
        # Let Popen consume its own original wait status first.
        if child is not None:child.poll()
        if child is not None and child.returncode is None:return
        while True:
            try:pid,status=os.waitpid(-1,os.WNOHANG)
            except ChildProcessError:return
            if not pid:return
            matches=[v for (p,_),v in known.items() if p==pid]
            reaped.append(dict(pid=pid,wait_status=status,returncode=os.waitstatus_to_exitcode(status),identities=matches))

    def signal_owned(sig):
        nonlocal forced
        rows,owned=observe()
        live={pid:row for pid,row in owned.items() if row['state']!='Z'}
        # Signal a group only when every current member is one of our exact
        # descendants and its leader still has the observed start identity.
        groups={row['pgrp'] for row in live.values()}
        for pg in sorted(groups):
            leader=live.get(pg)
            members={pid for pid,row in rows.items() if row['pgrp']==pg}
            if leader is None or not members<=set(owned) or not same(leader):continue
            try:os.killpg(pg,sig);forced=True;actions.append(dict(group=pg,leader=leader,signal=sig))
            except ProcessLookupError:pass
        # Includes sessions whose leader already exited. Never use a command
        # name, saved PID alone, or an unrelated process-group identifier.
        for pid,row in live.items():
            if not same(row):continue
            try:os.kill(pid,sig);forced=True;actions.append(dict(identity=row,signal=sig))
            except ProcessLookupError:pass

    try:
        require(time.monotonic()<deadline,'preflight exhausted work deadline')
        argv=[sys.executable,'-I','-S','-B',str(HERE/'guest-work.py'),'--run-id',args.run_id,
              '--output',str(out),'--deadline',str(deadline)]
        with (out/'worker.stdout').open('xb') as stdout,(out/'worker.stderr').open('xb') as stderr:
            # Avoid inherited player/provider/environment state in the worker.
            child=subprocess.Popen(argv,stdout=stdout,stderr=stderr,start_new_session=True,
                env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C'},cwd=SCRATCH)
            write(out/'worker-started.json',dict(argv=argv,identity=identity(child.pid),executable_sha256=sha(sys.executable)))
            while True:
                rows,owned=observe();now=time.monotonic()
                if now-last_sample>=1:
                    disk=usage([SCRATCH,staged,out,OUTPUT/('pix574-chd-'+args.run_id)]);last_sample=now
                    samples.write(json.dumps(dict(elapsed=now-started,processes=list(owned.values()),disk=disk))+'\n');samples.flush()
                    require(max(disk['apparent'],disk['allocated'])<=LIMIT and disk['files']<=8192,'aggregate fixture file budget exceeded')
                    require(len(owned)<=64,'descendant count exceeded')
                    require(sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo'],'guest network interfaces changed')
                require(not interrupted,'owner interrupted: '+str(interrupted))
                require(now<deadline,'single 235s work deadline exhausted')
                if child.poll() is not None:
                    reap();_,remaining=observe()
                    require(not remaining,'worker exited with descendants')
                    require(child.returncode==0,'original worker failed')
                    require(read(out/'worker-result.json')['status']=='PASS','worker result absent/failing')
                    break
                time.sleep(0.1)
    except BaseException as exc:error=repr(exc)
    finally:
        # At most five seconds from work cutoff, never a per-case extension.
        # Normal success sends no signals. Failure preserves scratch and logs.
        _,remaining=observe()
        retire_limit=min(time.monotonic()+5,cleanup_deadline)
        if remaining:
            signal_owned(signal.SIGTERM)
            term_until=min(time.monotonic()+1,retire_limit-1)
            while time.monotonic()<term_until:
                reap();_,remaining=observe()
                if not remaining:break
                time.sleep(0.05)
            # Send KILL once even if a late interruption consumed the reserve.
            reap();_,remaining=observe()
            if remaining:signal_owned(signal.SIGKILL)
            while time.monotonic()<retire_limit:
                reap();_,remaining=observe()
                if not remaining:break
                signal_owned(signal.SIGKILL);time.sleep(0.05)
        reap();_,remaining=observe();samples.close()
        elapsed=time.monotonic()-started
        live_known=[v for v in known.values() if same(v)]
        cleanup=dict(status='PASS' if not remaining and not live_known else 'FAIL',
            remaining=list(remaining.values()),surviving_observed=live_known,signals=actions,
            adopted_original_waits=reaped,all_observed=list(known.values()),forced=forced)
        write(out/'cleanup.json',cleanup)
        rc=child.returncode if child is not None else None
        result=dict(status='PASS' if error is None and rc==0 and cleanup['status']=='PASS' and not forced and elapsed<=240 else 'FAIL',
            original_worker_returncode=rc,error=error,elapsed=elapsed,total_limit_seconds=240,
            cleanup=cleanup['status'],forced_cleanup=forced,sys_lookup_measured=False,
            scratch_retained=str(SCRATCH),stager_copy_retained=str(staged),output=str(out))
        write(out/'result.json',result);print(json.dumps(result),flush=True)
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())

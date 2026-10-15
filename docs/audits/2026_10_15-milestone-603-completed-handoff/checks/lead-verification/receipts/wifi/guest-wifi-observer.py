#!/usr/bin/env python3
"""UNRUN Linux/VM supervisor; record the original driver and descendant statuses.

The known-bad baseline returns 1 when children survive normal driver exit. That
failure is retained, then this supervisor cleans only its own child tree.
"""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def identity(pid):
    """A disappeared PID is benign; an unreadable existing PID is unknown, never absent."""
    directory = Path('/proc') / str(pid)
    try:
        with (directory / 'stat').open('rb') as stream:
            raw = stream.read(65537)
    except (FileNotFoundError, ProcessLookupError):
        try:
            directory.stat()
        except (FileNotFoundError, ProcessLookupError):
            return None
        raise RuntimeError('stat unavailable for a still-present proc PID ' + str(pid))
    assert len(raw) <= 65536, 'oversized proc stat'
    prefix, separator, tail = raw.rpartition(b')')
    assert separator and prefix.split(b' (', 1)[0] == str(pid).encode(), 'malformed proc stat'
    fields = tail.split()
    assert len(fields) >= 20, 'short proc stat'
    return dict(pid=pid, ppid=int(fields[1]), pgid=int(fields[2]),
                state=fields[0].decode('ascii'), start_ticks=int(fields[19]))


def census():
    rows = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isascii() or not entry.name.isdigit():
            continue
        row = identity(int(entry.name))
        if row is not None:
            rows.append(row)
    return sorted(rows, key=lambda row: row['pid'])


def children(pid):
    assert identity(pid) is not None, 'cannot observe fixture parent'
    return [row for row in census() if row['ppid'] == pid]


def tree(pid):
    assert identity(pid) is not None, 'cannot observe fixture tree root'
    rows = census()
    answer, parents, seen = [], [pid], {pid}
    while parents:
        parent = parents.pop()
        for row in rows:
            if row['ppid'] == parent:
                assert row['pid'] not in seen, 'cyclic proc ancestry'
                seen.add(row['pid']); answer.append(row); parents.append(row['pid'])
    return answer


def same(row):
    now = identity(row['pid'])
    return now is not None and now['start_ticks'] == row['start_ticks']


def signal_child(row, parent, signum=signal.SIGKILL):
    """Only direct/adopted children through identity-checked pidfds may be signaled."""
    assert row['ppid'] == parent, 'refusing a non-child signal'
    def stable(now):
        return all(now[key] == row[key] for key in ['pid', 'ppid', 'pgid', 'start_ticks'])
    now = identity(row['pid'])
    if now is None:
        return dict(identity=row, signal=signum, outcome='already-gone')
    assert stable(now), 'child identity changed before pidfd acquisition'
    try:
        fd = os.pidfd_open(row['pid'], 0)
    except ProcessLookupError:
        return dict(identity=row, signal=signum, outcome='gone-before-pidfd')
    try:
        now = identity(row['pid'])
        if now is None:
            return dict(identity=row, signal=signum, outcome='gone-after-pidfd')
        assert stable(now), 'child identity changed after pidfd acquisition'
        try:
            signal.pidfd_send_signal(fd, signum, None, 0)
        except ProcessLookupError:
            return dict(identity=row, signal=signum, outcome='gone-before-signal')
        return dict(identity=row, signal=signum, outcome='pidfd-signal')
    finally:
        os.close(fd)


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def reap(rows):
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            return
        if pid == 0:
            return
        rows.append(dict(pid=pid, wait_status=status, exit_code=os.waitstatus_to_exitcode(status)))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--binary-sha256',required=True)
    p.add_argument('--known-bad',action='store_true')
    a=p.parse_args()
    assert os.getuid()==0 and sorted(x.name for x in Path('/sys/class/net').iterdir())==['lo']
    assert a.output.parent==Path('/tmp/pix-output/audit-ui') and not a.output.exists()
    assert hashlib.sha256(Path('/usr/bin/emulationstation').read_bytes()).hexdigest()==a.binary_sha256
    assert subprocess.run(['systemctl','is-active','--quiet','essway.service'],timeout=5).returncode==3
    a.output.mkdir(mode=0o700);root=a.output
    libc=ctypes.CDLL(None,use_errno=True);assert libc.prctl(36,1,0,0,0)==0
    def interrupted(sig,frame):raise KeyboardInterrupt('observer signal '+str(sig))
    signal.signal(signal.SIGTERM,interrupted)
    deadline=time.monotonic()+180
    result={'status':'RUNNING','scope':'actual installed-path ES; explicit candidate overlay if staged',
            'binary_sha256':a.binary_sha256,'known_bad':a.known_bad,'started':time.monotonic(),
            'reaped':[],'forced_cleanup':[],'observations':[]}
    proc=None;original=2;observed=[]
    write(root/'startup-inputs.json', {name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in ['/usr/bin/emulationstation','/usr/bin/es_settings','/etc/profile','/usr/bin/wifictl']})
    def reap_backend(rows):
        for row in rows:
            try:pid,status=os.waitpid(row['pid'],os.WNOHANG)
            except ChildProcessError:continue
            if pid:result['reaped'].append({'pid':pid,'wait_status':status,'exit_code':os.waitstatus_to_exitcode(status)})
    def wait_for(path,seconds):
        limit=min(deadline,time.monotonic()+seconds)
        while not path.exists():
            assert proc.poll() is None and time.monotonic()<limit,'frontend/handshake deadline'
            time.sleep(.02)
    try:
        assert hasattr(os, "pidfd_open") and hasattr(signal, "pidfd_send_signal"), "pidfd support required"
        env=dict(os.environ,WIFI_PROOF_ROOT=str(root))
        with (root/'frontend.stdout').open('xb') as out,(root/'frontend.stderr').open('xb') as err:
            proc=subprocess.Popen(['/bin/bash','-ec','. /usr/bin/es_settings; exec /usr/bin/emulationstation --log-path /var/log --no-splash'],cwd='/storage',env=env,stdout=out,stderr=err,start_new_session=True)
            result['driver_identity']=identity(proc.pid)
            limit=time.monotonic()+40
            while True:
                assert proc.poll() is None and time.monotonic()<limit
                try:
                    if hashlib.sha256(Path(f'/proc/{proc.pid}/exe').read_bytes()).hexdigest()==a.binary_sha256:break
                except FileNotFoundError:pass
                time.sleep(.05)
            write(root/'frontend-ready.json',{'identity':identity(proc.pid),'binary_sha256':a.binary_sha256})
            wait_for(root/'backend-ready',75)
            observed=tree(proc.pid);result['observations']=observed
            ids=[int(x) for x in (root/'backend-pids').read_text().split()];assert len(ids)==2
            index={r['pid']:r for r in observed};assert all(pid in index and index[pid]['state']!='Z' for pid in ids)
            group=[index[x] for x in ids];assert group[0]['pgid']==ids[0]==group[1]['pgid']
            result['blocked_group']=group;write(root/'blocked-ready.json',{'group':group,'frontend':identity(proc.pid)})
            wait_for(root/'continue-exit',25)
            # The original 30s scan limit is never lengthened by the fixture.
            assert all(same(x) and identity(x['pid'])['state']!='Z' for x in group),'scan completed before exit request'
            calls=(root/'invocations').read_text().splitlines();assert sum(x.split()[2] in ['list','scanlist'] for x in calls)==1
            result['calls_before_exit']=calls;result['exit_requested']=time.monotonic()
            assert same(result['driver_identity'])
            result['normal_exit_signal']=signal_child(result['driver_identity'],os.getpid(),signal.SIGINT)
            limit=min(deadline,time.monotonic()+10)
            while proc.poll() is None:
                reap_backend(group)
                if 'scan_group_stopped' not in result and all(not same(x) or identity(x['pid'])['state']=='Z' for x in group):result['scan_group_stopped']=time.monotonic()
                assert time.monotonic()<limit,'whole frontend exit exceeded10s'
                time.sleep(.01)
            result['driver_original_returncode']=proc.wait(timeout=1);result['driver_exited']=time.monotonic()
            reap(result['reaped']);limit=time.monotonic()+.5
            while children(os.getpid()) and time.monotonic()<limit:reap(result['reaped']);time.sleep(.01)
            if 'scan_group_stopped' not in result and all(not same(x) for x in group):result['scan_group_stopped']=time.monotonic()
            result['survivors_after_normal_exit']=tree(os.getpid());result['owned_identities_still_present']=[x for x in observed if same(x)]
            after=(root/'invocations').read_text().splitlines();result['calls_after_exit']=after
            result['no_later_backend']=after==calls
            log=Path('/var/log/es_log.txt').read_text();assert len(log.encode())<=2*1024**2;(root/'es-log.txt').write_text(log)
            result['join_logs']={'stopping':log.count('wifi picker: stopping scan worker'),'joined':log.count('wifi picker: scan worker joined')}
            bounded=result.get('scan_group_stopped',float('inf'))-result['exit_requested']<=3
            original=0 if (result['driver_original_returncode']==0 and not result['survivors_after_normal_exit'] and not result['owned_identities_still_present'] and result['no_later_backend'] and bounded and result['join_logs']=={'stopping':1,'joined':1}) else 1
            result['status']='PASS' if original==0 else 'FAIL'
    except BaseException as error:
        result['status']='FAIL';result['error']=f'{type(error).__name__}: {error}'
    finally:
        # Publish original failure first. A failed observation/receipt cannot skip cleanup
        # or turn unknown custody into an empty census.
        result['original_observation_returncode'] = original
        result['observation_errors'] = []
        result['survivors_after_cleanup'] = None
        try:
            write(root / 'before-cleanup.json', result)
        except BaseException as error:
            result['observation_errors'].append('before receipt: ' + type(error).__name__ + ': ' + str(error))
        try:
            if proc is not None and proc.poll() is None:
                row = identity(proc.pid)
                assert row is not None and row['ppid'] == os.getpid()
                assert result.get('driver_identity') and same(result['driver_identity'])
                result['forced_cleanup'].append(signal_child(row, os.getpid()))
                try:
                    result['driver_original_returncode'] = proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    result['driver_unreaped'] = True
            limit = time.monotonic() + 3
            while time.monotonic() < limit:
                # Do not steal the Popen direct child's original wait status.
                if proc is None or proc.returncode is not None:
                    reap(result['reaped'])
                owned = children(os.getpid())
                if not owned:
                    break
                for row in owned:
                    if row['state'] != 'Z':
                        result['forced_cleanup'].append(signal_child(row, os.getpid()))
                time.sleep(.01)
            if proc is not None and proc.returncode is None:
                try:
                    result['driver_original_returncode'] = proc.wait(timeout=.1)
                except subprocess.TimeoutExpired:
                    result['driver_unreaped'] = True
            if proc is None or proc.returncode is not None:
                reap(result['reaped'])
        except BaseException as error:
            result['observation_errors'].append('cleanup: ' + type(error).__name__ + ': ' + str(error))
        try:
            result['survivors_after_cleanup'] = tree(os.getpid())
        except BaseException as error:
            result['observation_errors'].append('final census: ' + type(error).__name__ + ': ' + str(error))
        result['ended'] = time.monotonic()
        clean = (result['survivors_after_cleanup'] == [] and not result['observation_errors']
                 and not result.get('driver_unreaped') and not (original == 0 and result['forced_cleanup']))
        result['final_returncode'] = original if clean else 2
        if result['final_returncode'] != 0:
            result['status'] = 'FAIL'
        try:
            write(root / 'result.json', result)
        except BaseException as error:
            result['status'] = 'FAIL'; result['final_returncode'] = 2
            result['receipt_error'] = type(error).__name__ + ': ' + str(error)
            print(json.dumps(result), flush=True)
            raise
    return result['final_returncode']

if __name__=='__main__':raise SystemExit(main())

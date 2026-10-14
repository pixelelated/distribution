#!/usr/bin/env python3
"""UNRUN full-script VM fixture: exact shell bytes, disposable chroot, synthetic data.

Requires Linux root in an allocated disposable GENERIC_X64 VM. No listener,
Dolphin/proxy process, config from the installed image, account or external network.
"""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import sqlite3
import struct
import subprocess
import sys
import time

REVISION = Path(__file__).resolve().parents[1]
REVISION_SHA256 = '313f58513492763b08b82961b50a22b0d785bff3d2faf319b0ff14f35ad3a927'
PACKET = REVISION.parent / '2026-10-14-dolphin-proxy-routing-source'
BINDINGS_SHA256 = 'b2771499d182f434113ba3ba6d340c1442645e8aa9e65a210f957b8013fd18b4'
SCRIPT = 'projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/cheevos_dolphin.sh'
WORK_SECONDS = 60
MAX_STAGE = 24 * 1024 * 1024
MAX_SCRATCH = 32 * 1024 * 1024
PROFILE = '''# Entirely synthetic profile; do not source the guest profile.
get_setting() {
  local key value
  while IFS='=' read -r key value; do
    if [ "$key" = "$1" ]; then printf '%s\\n' "$value"; return 0; fi
  done < /fixture/settings
  return 0
}
set_setting() { printf '%s\\n' 'UNEXPECTED settings mutation' >&2; exit 96; }
'''
HEAD = '  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt uid timeout inode\n'
TABLES = {
    'ipv4': ('0100007F:1F90', '0A', 'tcp'),
    'wildcard4': ('00000000:1F90', '0A', 'tcp'),
    'mapped6': ('0000000000000000FFFF00000100007F:1F90', '0A', 'tcp6'),
    'loopback6': ('00000000000000000000000001000000:1F90', '0A', 'tcp6'),
    'wildcard6': ('00000000000000000000000000000000:1F90', '0A', 'tcp6'),
    'wrong-port': ('0100007F:1F91', '0A', 'tcp'),
    'established': ('0100007F:1F90', '01', 'tcp'),
    'other-address': ('0200007F:1F90', '0A', 'tcp'),
    'empty': None, 'missing': None, 'unreadable': None,
}
ELIGIBLE = {'ipv4', 'wildcard4', 'mapped6'}


def require(value, text):
    if not value:
        raise AssertionError(text)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def elf_dependencies(data):
    """Static ELF64 little-endian inspection; never invoke ldd or a loader."""
    require(data[:6] == b'\x7fELF\x02\x01', 'requires ELF64 little-endian guest runtime')
    require(struct.unpack_from('<H', data, 18)[0] == 62, 'requires GENERIC_X64 x86-64 binaries')
    offset = struct.unpack_from('<Q', data, 32)[0]
    size, count = struct.unpack_from('<HH', data, 54)
    require(size == 56 and count < 256, 'unsupported ELF program-header layout')
    ph = [struct.unpack_from('<IIQQQQQQ', data, offset+i*size) for i in range(count)]
    interp = [data[h[2]:h[2]+h[5]].rstrip(b'\0').decode() for h in ph if h[0] == 3]
    require(len(interp) <= 1, 'multiple ELF interpreters')
    dynamic = []
    for h in ph:
        if h[0] == 2:
            require(h[5] < 65536, 'excessive dynamic table')
            for i in range(h[2], h[2]+h[5], 16):
                tag, value = struct.unpack_from('<qQ', data, i)
                if not tag: break
                dynamic.append((tag, value))
    table = next((v for t,v in dynamic if t == 5), None)
    if table is None:
        return interp, []
    load = next(h for h in ph if h[0] == 1 and h[3] <= table < h[3]+h[5])
    start = table-load[3]+load[2]
    def string(index):
        end = data.index(b'\0', start+index, min(len(data), start+index+4096))
        return data[start+index:end].decode()
    # Exact image binaries normally use standard paths. Refuse exotic loader
    # search directives rather than claiming to have staged an equivalent tree.
    paths = [string(v) for t,v in dynamic if t in (15,29)]
    require(all(all(p in ('/lib','/lib64','/usr/lib','/usr/lib64') for p in s.split(':')) for s in paths),
            'nonstandard ELF RPATH/RUNPATH requires a separate staging review')
    return interp, [string(v) for t,v in dynamic if t == 1]


def stage_runtime(root):
    staged = {}; identities = []; total = 0
    searches = [Path(p) for p in ('/usr/lib','/lib','/lib64','/usr/lib64',
                '/lib/x86_64-linux-gnu','/usr/lib/x86_64-linux-gnu')]
    def copy(source, invocation):
        nonlocal total
        require(invocation.startswith('/') and '..' not in Path(invocation).parts, 'unsafe ELF destination')
        if invocation in staged: return
        requested = Path(source)
        resolved = requested.resolve(strict=True)
        require(resolved.is_file() and resolved.stat().st_size <= 16*1024*1024,
                'runtime source is not a regular file within16MiB')
        data = resolved.read_bytes()
        require(len(data) <= 16*1024*1024, 'one runtime file exceeds16MiB')
        interp, needed = elf_dependencies(data)
        total += len(data)
        require(total <= MAX_STAGE, 'runtime staging exceeds24MiB')
        dest = root/invocation.lstrip('/'); dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data); dest.chmod(0o755)
        require(resolved.stat().st_size == len(data) and sha(resolved.read_bytes()) == sha(data),
                'runtime source changed while copying')
        identities.append({'requested_path':str(requested), 'resolved_identity_path':str(resolved),
                           'guest_invocation_path':invocation, 'sha256':sha(data), 'bytes':len(data)})
        staged[invocation] = sha(data)
        for item in interp: copy(item, item)
        for name in needed:
            require('/' not in name, 'unexpected slash in DT_NEEDED')
            library = next((p/name for p in searches if (p/name).is_file()), None)
            require(library is not None, 'missing dependency: '+name)
            copy(library, str(library))
    for command in ('bash','cat'):
        invocation = shutil.which(command)
        require(invocation is not None, 'guest lacks '+command)
        # Preserve argv[0] basename even when cat resolves to BusyBox bytes.
        copy(invocation, '/bin/'+command)
    return identities, total


def cases():
    found = []
    for toggle in ('0','1','','unknown'):
        for hardcore in ('0','1','','unknown'):
            for host in ('','custom.example.invalid:1234'):
                found.append(dict(name=f'gates-{len(found):02}', toggle=toggle, hardcore=hardcore,
                                  host=host, table='ipv4'))
    for table in TABLES:
        for host in ('','https://custom.example.invalid'):
            found.append(dict(name=f'table-{table}-{len(found):02}', toggle='1', hardcore='0', host=host, table=table))
    for state in ('disabled','empty-enabled','missing-token'):
        for host in ('','custom.example.invalid:1234'):
            found.append(dict(name=f'early-{state}-{len(found):02}', toggle='1', hardcore='0', host=host,
                              table='ipv4', early=state))
    found.append(dict(name='encore-new-unofficial', toggle='1', hardcore='0', host='', table='ipv4', encore='1', unofficial='1', legacy='0'))
    found.append(dict(name='legacy-unofficial', toggle='0', hardcore='0', host='', table='ipv4', unofficial='', legacy='1'))
    found.append(dict(name='new-unofficial-wins', toggle='0', hardcore='0', host='', table='ipv4', unofficial='0', legacy='1'))
    return found


def configure(root, case):
    for folder in ('etc','fixture','storage/.config/dolphin-emu','var/log','proc/net'):
        (root/folder).mkdir(parents=True,exist_ok=True)
    for folder in ('storage/.config/dolphin-emu','var/log'):
        (root/folder).chmod(0o777)
    (root/'etc/profile').write_text(PROFILE); (root/'etc/profile').chmod(0o444)
    values = {
        'global.retroachievements.username':'<fixture-user>',
        'global.retroachievements.password':'<fixture-password>',
        'global.retroachievements.token':'<fixture-token>',
        'global.retroachievements':'1',
        'global.retroachievements.hardcore':case['hardcore'],
        'global.retroachievements.offlineproxy':case['toggle'],
        'global.retroachievements.customhost':case['host'],
        'global.retroachievements.encore':case.get('encore','0'),
        'global.retroachievements.unofficial':case.get('unofficial','0'),
        'global.retroachievements.testunofficial':case.get('legacy','0'),
    }
    early=case.get('early')
    if early=='disabled': values['global.retroachievements']='0'
    if early=='empty-enabled': values['global.retroachievements']=''
    if early=='missing-token': values['global.retroachievements.token']=''
    settings=root/'fixture/settings'; settings.chmod(0o644) if settings.exists() else None
    settings.write_text(''.join(k+'='+v+'\n' for k,v in values.items())); settings.chmod(0o444)
    for filename in ('tcp','tcp6'):
        p=root/'proc/net'/filename
        if p.exists(): p.unlink()
        if case['table']!='missing':
            p.write_text(HEAD);p.chmod(0 if case['table']=='unreadable' else 0o444)
    row=TABLES[case['table']]
    if row:
        addr,state,filename=row;p=root/'proc/net'/filename;p.chmod(0o644)
        p.write_text(HEAD+f'   0: {addr} 00000000:0000 {state} 00000000:00000000 00:00000000 00000000 0 0 123\n');p.chmod(0o444)
    ini=root/'storage/.config/dolphin-emu/RetroAchievements.ini'
    ini.write_text('[Achievements]\nHostUrl = 127.0.0.1:8080\nPreserveOnEarlyRefusal = yes\n');ini.chmod(0o666)
    log=root/'var/log/cheevos.log';log.write_text('synthetic prior log\n');log.chmod(0o666)
    return values,ini,log


def expected_ini(values, host):
    flag=lambda key:'True' if values[key]=='1' else 'False'
    unofficial=values['global.retroachievements.unofficial'] or values['global.retroachievements.testunofficial']
    return ('[Achievements]\nDiscordPresenceEnabled = False\nEnabled = True\n'
            f'EncoreEnabled = {flag("global.retroachievements.encore")}\n'
            f'HardcoreEnabled = {flag("global.retroachievements.hardcore")}\n'
            'ProgressEnabled = False\nSpectatorEnabled = False\n'
            f'UnofficialEnabled = {"True" if unofficial=="1" else "False"}\n'
            f'Username = {values["global.retroachievements.username"]}\n'
            f'ApiToken = {values["global.retroachievements.token"]}\nHostUrl = {host}\n').encode()


def snapshot(root, ignore=()):
    return {str(p.relative_to(root)):{'sha256':sha(p.read_bytes()),'mode':p.stat().st_mode & 0o777}
            for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)) not in ignore}


def proc_identity(pid):
    """Read PID/PPID/start ticks only. A vanished directory is the sole benign read race."""
    directory=Path('/proc')/str(pid)
    try:
        with (directory/'stat').open('rb') as stream:
            raw=stream.read(65537)
    except (FileNotFoundError, ProcessLookupError):
        try: directory.stat()
        except (FileNotFoundError, ProcessLookupError): return None
        raise RuntimeError('stat unavailable for a still-present proc PID '+str(pid))
    require(len(raw)<=65536, 'oversized proc stat for PID '+str(pid))
    # comm may contain spaces, newlines and closing parentheses. It is never
    # matched or retained; numeric fields start after its final closing paren.
    prefix,separator,tail=raw.rpartition(b')')
    require(separator and prefix.split(b' (',1)[0]==str(pid).encode(),
            'malformed proc stat PID '+str(pid))
    fields=tail.split()
    require(len(fields)>=20, 'short proc stat PID '+str(pid))
    return {'pid':pid,'ppid':int(fields[1]),'start_ticks':int(fields[19])}


def direct_children(parent):
    """Census this subreaper's direct/adopted children; errors never mean empty."""
    require(proc_identity(parent) is not None, 'cannot observe fixture owner in proc')
    found=[]
    for entry in Path('/proc').iterdir():
        if not entry.name.isascii() or not entry.name.isdigit(): continue
        identity=proc_identity(int(entry.name))
        if identity is not None and identity['ppid']==parent:
            found.append(identity)
    return sorted(found,key=lambda item:item['pid'])


def signal_child(identity,parent):
    """Only an identity-checked child pidfd may receive a signal; never numeric kill."""
    require(identity['ppid']==parent, 'refusing a non-child signal')
    current=proc_identity(identity['pid'])
    if current is None: return {'identity':identity,'outcome':'already-gone'}
    require(current==identity, 'child identity changed before pidfd acquisition')
    try: fd=os.pidfd_open(identity['pid'],0)
    except ProcessLookupError: return {'identity':identity,'outcome':'gone-before-pidfd'}
    try:
        # Refuse reuse/reparenting between the census and the acquired handle.
        current=proc_identity(identity['pid'])
        if current is None: return {'identity':identity,'outcome':'gone-after-pidfd'}
        require(current==identity, 'child identity changed after pidfd acquisition')
        try: signal.pidfd_send_signal(fd,signal.SIGKILL,None,0)
        except ProcessLookupError: return {'identity':identity,'outcome':'gone-before-signal'}
        return {'identity':identity,'outcome':'pidfd-kill'}
    finally:
        os.close(fd)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();out=args.output.absolute()
    require(os.geteuid()==0,'allocated disposable VM root required')
    require(out.parent==Path('/run') and out.name.startswith('pix584-') and not out.exists() and not out.is_symlink(),
            'fresh /run/pix584-* output required')
    revision_bytes=(REVISION/'bindings.json').read_bytes()
    require(sha(revision_bytes)==REVISION_SHA256,'revision binding changed')
    revision=json.loads(revision_bytes)
    require(sha((PACKET/'fixtures/probe.py').read_bytes())==revision['base_fixture_sha256'],'original fixture changed')
    require(sha((PACKET/'SHA256SUMS').read_bytes())==revision['base_manifest_sha256'],'original manifest changed')
    bindbytes=(PACKET/'bindings.json').read_bytes();require(sha(bindbytes)==BINDINGS_SHA256,'binding manifest changed')
    bind=json.loads(bindbytes)
    for name,expected in bind['fixture_inputs'].items(): require(sha((PACKET/name).read_bytes())==expected,name+' changed')
    require(os.statvfs('/run').f_bavail*os.statvfs('/run').f_frsize >= MAX_SCRATCH+16*1024*1024,'need48MiB free/reserve')
    resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE,(16*1024*1024,16*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU,(50,50))
    out.mkdir(mode=0o755);root=out/'root';root.mkdir(mode=0o755)
    started=time.monotonic();deadline=started+WORK_SECONDS
    report={'status':'FAIL','evidence':'full configuration script with synthetic inputs only',
            'python':sys.version,'bindings_sha256':sha(bindbytes),'cases':[],'runtime':'actual guest bash/cat, ELF dependencies copied'}
    libc=ctypes.CDLL(None,use_errno=True);libc.prctl.restype=ctypes.c_int;libc.unshare.restype=ctypes.c_int
    require(libc.prctl(36,1,0,0,0)==0,'subreaper setup failed')
    parent=os.getpid();parent_net=os.readlink('/proc/self/ns/net')
    report['parent_net_namespace']=parent_net
    def timed_out(signum,frame): raise TimeoutError('whole fixture work deadline')
    signal.signal(signal.SIGALRM,timed_out);signal.alarm(WORK_SECONDS)
    # Stable synthetic tripwires, outside every case's writable config directory.
    active=None
    report['fixture_sha256']=sha(Path(__file__).read_bytes())
    report['revision_bindings_sha256']=sha(revision_bytes)
    report['original_fixture_sha256']=revision['base_fixture_sha256']
    report['signals']=[]
    try:
        require(hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal'),
                'identity-safe cleanup requires Python/Linux pidfd support')
        report['runtime_files'],report['runtime_bytes']=stage_runtime(root)
        for folder in ('fixture','storage/.config/raofflineproxy'):
            (root/folder).mkdir(parents=True,exist_ok=True)
        db=sqlite3.connect(root/'storage/.config/raofflineproxy/proxy.sqlite3')
        try:
            db.execute('CREATE TABLE pending_awards (sentinel TEXT)')
            db.execute("INSERT INTO pending_awards VALUES ('synthetic queue must not change')")
            db.commit()
        finally:
            db.close()
        for variant in ('before','after'):
            actual=(PACKET/'source'/f'cheevos_dolphin.{variant}.sh').read_bytes()
            script=root/'fixture/actual.sh';script.write_bytes(actual);script.chmod(0o444)
            for case in cases():
                require(time.monotonic()<deadline,'deadline before next case')
                values,ini,log=configure(root,case)
                before_ini=ini.read_bytes();protected=snapshot(root,('storage/.config/dolphin-emu/RetroAchievements.ini','var/log/cheevos.log'))
                name=variant+'-'+case['name'];receipt=out/name;receipt.mkdir()
                record={'name':name,'variant':variant,'input':case,'script_sha256':sha(actual),'original_exit':None,'status':'FAIL'}
                report['cases'].append(record)
                rd,wr=os.pipe()
                def isolate():
                    require(libc.prctl(1,signal.SIGKILL,0,0,0)==0,'initial parent-death signal failed')
                    require(os.getppid()==parent,'owner exited before containment')
                    require(libc.unshare(0x40000000)==0,'private network namespace unavailable')
                    ns=os.readlink('/proc/self/ns/net');require(ns!=parent_net,'network namespace did not change')
                    os.chroot(root);os.chdir('/')
                    os.setgroups([]);os.setgid(65534);os.setuid(65534)
                    require(libc.prctl(38,1,0,0,0)==0,'no-new-privileges failed')
                    require(libc.prctl(1,signal.SIGKILL,0,0,0)==0,'post-setuid parent-death signal failed')
                    chosen=ctypes.c_int()
                    require(libc.prctl(2,ctypes.byref(chosen),0,0,0)==0 and chosen.value==signal.SIGKILL,'parent-death signal readback failed')
                    require(os.getppid()==parent,'owner exited during containment')
                    resource.setrlimit(resource.RLIMIT_CPU,(2,2))
                    resource.setrlimit(resource.RLIMIT_FSIZE,(65536,65536))
                    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
                    os.write(wr,json.dumps({'net_namespace':ns,'uid':os.getuid(),'gid':os.getgid(),'parent_death_signal':chosen.value}).encode())
                    os.close(wr)
                try:
                    with (receipt/'stdout').open('wb') as stdout,(receipt/'stderr').open('wb') as stderr:
                        active=subprocess.Popen(['/bin/bash','--noprofile','--norc','/fixture/actual.sh'],
                            stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                            env={'PATH':'/bin','HOME':'/nonexistent','LC_ALL':'C'},
                            start_new_session=True,preexec_fn=isolate,pass_fds=(wr,))
                        os.close(wr);wr=-1
                        record['containment']=json.loads(os.read(rd,4096))
                        try: record['original_exit']=active.wait(timeout=min(3,max(0.01,deadline-time.monotonic())))
                        except subprocess.TimeoutExpired:
                            record['timed_out']=True
                            for child in direct_children(parent):
                                report['signals'].append(signal_child(child,parent))
                            record['original_exit']=active.wait(timeout=2)
                            raise AssertionError(name+': per-case deadline')
                        active=None
                finally:
                    os.close(rd)
                    if wr>=0:os.close(wr)
                # Reap any unexpected descendant and retain its original wait status.
                children=[]
                while True:
                    try: pid,status=os.waitpid(-1,os.WNOHANG)
                    except ChildProcessError: break
                    if pid==0:break
                    children.append({'pid':pid,'wait_status':status})
                record['unexpected_descendants']=children
                require(not children,name+': unexpected descendant adopted')
                live=direct_children(parent)
                require(not live,name+': live descendants '+str(live))
                (receipt/'generated.ini').write_bytes(ini.read_bytes());(receipt/'log').write_bytes(log.read_bytes())
                (receipt/'settings').write_bytes((root/'fixture/settings').read_bytes())
                require(protected==snapshot(root,('storage/.config/dolphin-emu/RetroAchievements.ini','var/log/cheevos.log')),name+': protected input/queue/runtime changed')
                require((receipt/'stdout').read_bytes()==b'',name+': unexpected stdout')
                require((receipt/'stderr').read_bytes()==b'',name+': unexpected stderr')
                early=case.get('early');eligible=variant=='after' and case['toggle']=='1' and case['hardcore']=='0' and case['table'] in ELIGIBLE
                if early:
                    require(record['original_exit']==1 and ini.read_bytes()==before_ini,name+': early-refusal preservation failed')
                    expected_log=('RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station.\n' if early=='missing-token' else 'RetroAchievements are not enabled, please turn them on in Emulation Station.\n')
                else:
                    require(record['original_exit']==0,name+': original script exit '+str(record['original_exit']))
                    host='127.0.0.1:8080' if eligible else case['host']
                    require(ini.read_bytes()==expected_ini(values,host),name+': complete generated INI differs')
                    expected_log='synthetic prior log\n'
                    if variant=='after' and case['toggle']=='1' and case['hardcore']=='0' and not eligible:
                        if case['table'] in ('missing','unreadable'):
                            expected_log+='Offline RetroAchievements is on but the listener tables could not be read; keeping the configured achievements host.\n'
                        else:
                            expected_log+='Offline RetroAchievements is on but nothing is listening on 127.0.0.1:8080; keeping the configured achievements host.\n'
                require(log.read_text()==expected_log,name+': fallback diagnostic differs')
                record['status']='PASS';record['protected_files_unchanged']=len(protected)
                record['ini_sha256']=sha(ini.read_bytes())
                (receipt/'result.json').write_text(json.dumps(record,indent=2)+'\n')
        report['status']='PASS'
    except BaseException as error:
        report['error']=type(error).__name__+': '+str(error)
        raise
    finally:
        signal.alarm(0)
        report['remaining_children']=None  # unknown until observation succeeds
        report['cleanup_descendants']=[]
        report['observation_errors']=[]
        try:
            if active is not None:
                for child in direct_children(parent):
                    report['signals'].append(signal_child(child,parent))
                try:
                    exit_code=active.wait(timeout=3)
                    if report['cases'] and report['cases'][-1]['original_exit'] is None:
                        report['cases'][-1]['original_exit']=exit_code
                except subprocess.TimeoutExpired: report['cleanup_failed']=True
            # Kill/reap only our direct/adopted children within the original
            # two-second cleanup budget. Unexpected children always mean FAIL.
            cleanup_deadline=time.monotonic()+2
            while time.monotonic()<cleanup_deadline:
                owned=direct_children(parent)
                if not owned:break
                report['status']='FAIL'
                for child in owned:
                    report['signals'].append(signal_child(child,parent))
                while True:
                    try:pid,status=os.waitpid(-1,os.WNOHANG)
                    except ChildProcessError:break
                    if pid==0:break
                    report['cleanup_descendants'].append({'pid':pid,'wait_status':status})
                time.sleep(0.01)
        except BaseException as error:
            report['status']='FAIL'
            report['observation_errors'].append('cleanup: '+type(error).__name__+': '+str(error))
        # Each observation is independent of receipt publication. An error
        # cannot become an empty census or erase the original failure/exit.
        try:
            report['remaining_children']=direct_children(parent)
        except BaseException as error:
            report['status']='FAIL'
            report['observation_errors'].append('final census: '+type(error).__name__+': '+str(error))
        report['elapsed_seconds']=time.monotonic()-started
        try:
            report['retained_bytes']=sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
            if report['retained_bytes']>MAX_SCRATCH:
                report['status']='FAIL';report['scratch_limit_exceeded']=True
        except BaseException as error:
            report['status']='FAIL'
            report['observation_errors'].append('scratch census: '+type(error).__name__+': '+str(error))
        if report['remaining_children'] is None or report['remaining_children'] or report.get('cleanup_failed'):
            report['status']='FAIL'
        try:
            (out/'result.json').write_text(json.dumps(report,indent=2)+'\n')
        except BaseException as error:
            report['status']='FAIL'
            report['receipt_error']=type(error).__name__+': '+str(error)
            # Keep a fallback receipt in the coordinator's captured owner stdout
            # if the output filesystem itself cannot accept the final JSON.
            print(json.dumps(report),flush=True)
            raise
        print(json.dumps({'status':report['status'],'result':str(out/'result.json')}),flush=True)
    require(report['status']=='PASS','fixture did not pass')


if __name__=='__main__':
    main()

"""One selected sealed #1433 armed action, with frame-bound ordinary quit evidence."""
import base64
import fcntl
import hashlib
import json
import os
import re
import shlex
import socket
import sys
import time
import uuid
from pathlib import Path

from common import now, write
from readback_boundaries import check_boundaries, verify_drives
from visible_quit import VisibleQuit, check_edges, document, verify_saves
import menu_timing as T

S='/tmp/m7-1433-armed-input'
R='/tmp/m7-1433-armed-result'
FRONTEND='/tmp/qa-composed-source'
FOUT='/tmp/qa-composed-result/flow/normal-exit'
GUEST_WITNESS='/tmp/m7-owner-witness.py'
FILE_OUT='/tmp/m7-1433-owner-file-originals'
LIVE_OUT='/tmp/m7-1433-owner-live-originals'
FILE_LIMITS={'file-originals.json':8192,'local.srm':8192,'current.srm':8192,'old.srm':8192}


def validate_cpu(cpu, row):
    assert cpu['state']=='ready' and cpu['pid']==row['emulator'], 'same tracked RetroArch CPU witness required'
    assert type(cpu['start_ticks']) is int and cpu['start_ticks']==row['start_ticks']>0
    samples=cpu['samples']
    assert 1<=len(samples)<=40 and all(len(s)==2 and all(isinstance(x,int) and x>=0 for x in s) for s in samples)
    assert all(b[0]-a[0]>=1000000000 and b[1]>=a[1] for a,b in zip(samples,samples[1:]))
    deadline,ticks=samples[-1]
    assert ticks>=200 or (ticks>=30 and sum(s[1]>0 for s in samples)>=4), 'established VM CPU threshold'
    assert cpu['margin_end_ns']-deadline>=3000000000 and cpu['margin_end_ticks']>=ticks, 'three-second write margin'


LIMITS={'result.json':128*1024,'proof-inputs.json':128*1024,'unarmed-readback.serial':128*1024,
        'armed-readback.serial':128*1024,'game-ready.json':128*1024,'child-originals.jsonl':2*1024**2,
        'menu-window.json':4096,'exit-chain.json':128*1024,'observer.stderr':128*1024,'before.json':128*1024,
        'after.json':128*1024,'preservation.json':128*1024,'product-log.original':128*1024}
SETTINGS_ORIGINALS={'settings-before.original':65536,'settings-after.original':65536}
LIMITS.update(SETTINGS_ORIGINALS)


def ctx_witness(boot,attempt):
    return f'python3 -I -B {GUEST_WITNESS} cpu {boot} {attempt}'


def open_armed_console(path, cutoff):
    # Same console setup as vm-serial, with an absolute quiet/byte bound.
    end=min(cutoff,time.monotonic()+8)
    client=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    try:
        client.settimeout(max(.001,end-time.monotonic()))
        client.connect(str(path))
        client.settimeout(max(.001,end-time.monotonic()))
        client.sendall(b"\nstty -echo 2>/dev/null\n")
        drained=0
        while time.monotonic()+.3<end:
            client.settimeout(.3)
            try:
                chunk=client.recv(65536)
            except TimeoutError:
                return client
            drained+=len(chunk)
            if not chunk or drained>65536:
                break
        raise RuntimeError("armed console did not reach bounded quiet")
    except BaseException:
        client.close()
        raise


def serial_armed(ctx, qemu, owner, boot, attempt, visual, cutoff):
    tag=uuid.uuid4().hex
    begin=b'BEG'+tag.encode()
    end=b'END'+tag.encode()
    ret=b'M7RC'+tag.encode()+b':'
    prefix=b'M7_EXIT_READY='
    cpu_prefix=b'M7_EXIT_CPU='
    menu_prefix=b'M7_MENU_GUARD='
    row=cpu=menu=None
    checked=False
    cmd=f'python3 -I -B {S}/arm.py --disposable-no-nic --boot-id {boot} --attempt {attempt}'
    command=f'echo {begin.decode()}; {ctx_witness(boot,attempt)} & witness=$!; {cmd}; r=$?; wait "$witness"; printf "\\n{ret.decode()}%s\\n" "$r"; echo {end.decode()}\n'
    buf=bytearray()
    pending=b''
    began=False
    finished=False
    ready_count=0
    receipt={'argv':cmd.split(),'utc':now(),'completed_transport':False,
             'original_guest_rc':None,'accepted_ready_count':0,'original_visual_input_sent':False,
             'cutoff_host_ns':int(cutoff*T.NS)}
    with (owner/'serial.lock').open('a') as locked:
        fcntl.flock(locked,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            client=open_armed_console(owner/'vm/s.sock',cutoff)
            try:
                ctx.set('1433-armed-foreground')
                client.settimeout(max(.001,min(8,cutoff-time.monotonic())))
                client.sendall(command.encode())
                while time.monotonic()<cutoff:
                    assert qemu.poll() is None,'QEMU died during armed case'
                    client.settimeout(max(.001,min(8,cutoff-time.monotonic())))
                    try: chunk=client.recv(65536)
                    except (socket.timeout,TimeoutError): continue
                    if not chunk:break
                    buf.extend(chunk)
                    if len(buf)>T.SERIAL_CAP:raise RuntimeError('serial original exceeded its cap')
                    pending+=chunk
                    while b'\n' in pending:
                        raw,pending=pending.split(b'\n',1)
                        line=raw.strip(b'\r')
                        if line==begin:
                            assert not began
                            began=True
                        if not began:continue
                        if line.startswith(prefix):
                            ready_count+=1
                            assert ready_count==1 and len(line)<=8192
                            row=json.loads(line[len(prefix):])
                            assert row['schema']=='m7-1433-armed-ready-v1'
                            assert row['attempt']==attempt and row['boot_id']==boot
                            assert row['config_effective'] is True and row['core_mapped'] is True
                            es=row['ES']
                            assert isinstance(es['pid'],int) and es['pid']>1
                            assert isinstance(row['emulator'],int) and row['emulator']>1 and row['emulator']!=es['pid']
                            write(owner/'records/1433-ready.json',row,True)
                            receipt['accepted_ready_count']=1
                        if line.startswith(cpu_prefix):
                            assert cpu is None and len(line)<=4096, 'duplicate or oversized CPU witness'
                            cpu=json.loads(line[len(cpu_prefix):])
                            assert cpu['attempt']==attempt and cpu['boot_id']==boot, 'stale CPU witness'
                            receipt['cpu_witness']=cpu
                            write(owner/'records/1433-cpu.json',cpu,True)
                        if row is not None and cpu is not None and not checked:
                            checked=True
                            try:
                                validate_cpu(cpu,row)
                            except (AssertionError,KeyError,TypeError) as error:
                                receipt['readiness_refusal']=str(error)[:256]
                            else:
                                menu=VisibleQuit(ctx,qemu,owner,visual,row,receipt)
                        if line.startswith(menu_prefix) and menu is not None:
                            try:
                                if len(line)+2>T.GUARD_LINE:
                                    raise ValueError("menu guard original exceeded cap")
                                menu.accept(json.loads(line[len(menu_prefix):]),time.monotonic_ns())
                            except (ValueError,TypeError) as error:
                                menu.refuse(error)
                        if line.startswith(ret):
                            assert receipt['original_guest_rc'] is None and re.fullmatch(rb'[0-9]{1,3}',line[len(ret):])
                            receipt['original_guest_rc']=int(line[len(ret):])
                        if line==end:
                            finished=True
                            break
                    if finished:break
                    if (menu is not None and receipt["original_guest_rc"] is None and not pending and
                            time.monotonic()+T.SERIAL_RESERVE<cutoff):
                        menu.step()
            finally:client.close()
            receipt['completed_transport']=finished and receipt['original_guest_rc'] is not None
            if menu is not None and menu.state not in ("finished","refused"):
                menu.refuse("guest foreground ended before a qualified confirmation")
        except BaseException as error:
            receipt['error']=type(error).__name__+': '+str(error)
            raise
        finally:
            with (owner/'records/1433-armed.serial').open('xb') as file:file.write(buf)
            write(owner/'records/1433-armed.serial.json',receipt,True)
    return receipt


def archive_timeout(deadline, ordinary):
    left=deadline-time.monotonic()
    if left<5:
        raise RuntimeError("independent archive deadline exhausted")
    return min(ordinary,(left-1)/4)


def export(ctx,owner,folder,items,prefix,deadline):
    collected={}
    for name,limit in items.items():
        assert Path(name).name==name
        idx=prefix+'-export-'+name
        p=folder+'/'+name
        cmd=f'if test -f {p} && test ! -L {p}; then stat -c %s {p}; else echo ABSENT; fi'
        size=ctx.serial_ok(idx+'-size',cmd,archive_timeout(deadline,8)).strip()
        if size=='ABSENT':
            collected[name]=None
            continue
        size=int(size)
        assert 0<=size<=limit
        parts=[]
        chunk_size=192*1024
        for i in range((size+chunk_size-1)//chunk_size):
            raw=ctx.serial_ok(idx+f'-{i}',f'dd if={p} bs={chunk_size} skip={i} count=1 status=none | base64 -w0',archive_timeout(deadline,12))
            part=base64.b64decode(raw.strip(),validate=True)
            assert len(part)==min(chunk_size,size-i*chunk_size)
            parts.append(part)
        data=b''.join(parts)
        assert len(data)==size
        expected=ctx.serial_ok(idx+'-digest',f'sha256sum {p}',archive_timeout(deadline,10)).split()[0]
        assert hashlib.sha256(data).hexdigest()==expected
        dest=owner/'export'/prefix
        dest.mkdir(exist_ok=True)
        with (dest/name).open('xb') as file:
            if name in SETTINGS_ORIGINALS:
                os.fchmod(file.fileno(), 0o600)
            file.write(data)
        collected[name]={'sha256':expected,'bytes':size}
    write(owner/'records'/(prefix+'-export.json'),collected,True)
    return collected


def seed_rehearsal_markers(ctx, case):
    """Recreate the exact synthetic retained state on a fresh QA backing."""
    marker=case['marker']
    assert marker==ctx.c['source'] and re.fullmatch(r'[0-9a-f]{40}',marker)
    paths={'/storage/roms/nes/M7-normal-boot.srm':8192,
           '/storage/roms/savestates/nes/M7-normal-boot.state.auto':300000,
           '/storage/roms/savestates/nes/M7-normal-boot.state1':200000,
           '/storage/roms/savestates/nes/M7-normal-boot.state2':100000,
           '/storage/.config/m7-normal-boot-marker':64}
    assert {path:row['bytes'] for path,row in case['files'].items()}==paths
    value=repr(case['files'])
    seed=f"""
import hashlib, os
from pathlib import Path
expected={value}
assert sorted(p.name for p in Path('/sys/class/net').iterdir()) == ['lo']
data={{path:(b'M7 synthetic retained qualification\\n'*10000)[:r['bytes']] for path,r in expected.items()}}
assert all(hashlib.sha256(buf).hexdigest()==expected[path]['sha256'] for path,buf in data.items())
assert not any(Path(path).exists() or Path(path).is_symlink() for path in data)
for path,buf in data.items():
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as stream:
        stream.write(buf)
        stream.flush()
        os.fsync(stream.fileno())
"""
    body=ctx.serial_ok('seed-synthetic-rehearsal-markers',
        'set -eu; python3 -I -B -c '+shlex.quote(seed)+
        '; /bin/bash -c '+shlex.quote('. /etc/profile >/dev/null 2>&1; set_setting rehearsal.marker '+marker+
                                     '; get_setting rehearsal.marker'),25)
    assert body.strip()==marker, 'synthetic rehearsal setting readback differs'


def execute(ctx,qemu,owner,deadline,admitted):
    c=ctx.c
    assert c['selected_case']=='1433-armed-exit' and deadline-time.monotonic()>T.WORK, 'insufficient standing slot for sealed review and export'
    verify_drives(ctx,qemu,owner)
    b=ctx.serial_ok('1433-boot-and-staged-seal',f'''
set -eu
test "$(ls /sys/class/net)" = lo
test -z "$(ip -4 route show default)"
test -z "$(ls -A /storage/.update)"
test "$(cat /sys/block/vdb/serial)" = M7BOOTPREP
test "$(cat /sys/block/vdb/ro)" = 1
test ! -d /sys/block/vdc
grep -Fx 'BUILD_ID="{c['source']}"' /etc/os-release
grep -Fx 'BUILD_DIRTY="no"' /etc/os-release
test ! -e {S}
mkdir -m 700 {S}
tar -xf /dev/vdb -C {S}
cd {S}
sha256sum -c SHA256SUMS
sha256sum -c FRONTEND.SHA256SUMS
mkdir -m 700 {FRONTEND}
for f in normal_restart.py boot_support.py cgroup_runtime.py; do mv "frontend-$f" "{FRONTEND}/$f"; done
printf "M7BOOT="; cat /proc/sys/kernel/random/boot_id
''',25)
    ids=[line[len('M7BOOT='):] for line in b.splitlines() if line.startswith('M7BOOT=')]
    assert len(ids)==1 and re.fullmatch(r'[a-f0-9-]{36}',ids[0]) and ids[0]!=c['previous_boot']
    if 'rehearsal_fixture' in c:
        seed_rehearsal_markers(ctx,c['rehearsal_fixture'])
    attempt=json.loads((owner/'slot/request.json').read_text())['nonce']
    assert re.fullmatch(r'[a-f0-9]{32}',attempt)
    write(owner/'records/1433-boot-binding.json',{'boot_id':ids[0],'attempt':attempt,'admission_id':admitted['id']},True)
    visual=[sys.executable,'-I','-B',c['tools']['visual'],'--monitor',str(owner/'vm/m.sock')]
    from preflight import execute as preflight
    preflight(ctx,owner,ids[0],attempt,deadline)
    witness=(owner/'code/guest-witness.py').read_bytes()
    assert len(witness)<=16384
    encoded=base64.b64encode(witness).decode()
    digest=hashlib.sha256(witness).hexdigest()
    ctx.serial_ok('1433-passive-witness-stage',
                  f'umask 077; set -C; printf %s {encoded} | base64 -d > {GUEST_WITNESS} && '
                  f'echo "{digest}  {GUEST_WITNESS}" | sha256sum -c -',
                  12)
    arm_start=time.monotonic()
    cutoff=T.arm_cutoff(arm_start,deadline)
    write(owner/'records/1433-timing-budget.json',
          {'boot_id':ids[0],'attempt':attempt,'arm_start_host_ns':int(arm_start*T.NS),
           'arm_cutoff_host_ns':int(cutoff*T.NS),'archive_until_host_ns':int(deadline*T.NS),
           'archive_reserved_seconds':T.ARCHIVE,'outer_slot_seconds':c['slot_seconds'],
           'menu_seconds':T.MENU,'post_exit_seconds':T.POST_EXIT,'observer_seconds':T.OBSERVER},True)
    failure=None;receipt=None
    try:receipt=serial_armed(ctx,qemu,owner,ids[0],attempt,visual,cutoff)
    except BaseException as error:failure=error
    archive_start=time.monotonic()
    write(owner/'records/1433-archive-start.json',
          {'start_host_ns':int(archive_start*T.NS),'remaining_seconds':deadline-archive_start,
           'arm_complete':bool(receipt and receipt['completed_transport'])},True)
    originals=export(ctx,owner,R,LIMITS,'armed',deadline)
    _,file_original_rc=ctx.serial(
        '1433-same-boot-file-originals',
        f'python3 -I -B {GUEST_WITNESS} files {ids[0]} {attempt}',archive_timeout(deadline,20))
    file_originals=export(ctx,owner,FILE_OUT,FILE_LIMITS,'save-originals',deadline)
    export(ctx,owner,LIVE_OUT,FILE_LIMITS,'live-save-originals',deadline)
    check_boundaries(c,owner)
    if failure is not None:raise failure
    assert receipt['completed_transport'] and receipt['original_guest_rc']==0, 'armed guest original refused or incomplete'
    assert receipt['accepted_ready_count']==1 and receipt['original_visual_input_sent']
    assert all(originals.values()),'missing expected original proof files'
    outcome=json.loads((owner/'export/armed/result.json').read_bytes())
    assert outcome['status']=='GUEST_LOCAL_EXIT_EVIDENCE_COMPLETE_OWNER_RETIREMENT_DUE'
    check_edges(outcome,receipt,ids[0],attempt)
    assert file_original_rc==0 and all(file_originals.values()),'same-case files/Bash originals incomplete'
    evidence=owner/'export/armed'
    save_proof=verify_saves(document(evidence/'before.json'),document(evidence/'after.json'),
                           document(evidence/'exit-chain.json'),file_originals,owner/'export/save-originals',
                           ids[0],attempt)
    write(owner/'records/1433-save-original-joins.json',save_proof,True)
    ctx.command('1433-return-frame',visual+['shot',str(owner/'frames/1433-return.png')],archive_timeout(deadline,12))
    code=f'import sys;sys.path.insert(0,{FRONTEND!r});import normal_restart;normal_restart.exit_normal()'
    _,quit_rc=ctx.serial('1433-normal-frontend-exit',
                         'mkdir -p /tmp/qa-composed-result/flow && python3 -I -B -c '+shlex.quote(code),archive_timeout(deadline,50))
    exit_results=export(ctx,owner,FOUT,{n:128*1024 for n in ('result.json','original-post.json','normal-quit-request.json')},'frontend',deadline)
    assert quit_rc==0 and all(exit_results.values()),'normal frontend exit evidence refused'
    ready=json.loads((owner/'export/frontend/original-post.json').read_bytes())
    assert ready['exit_status']=='0' and ready['service_result']=='success' and not ready['remaining']
    check_boundaries(c,owner,'budget-after-frontend-exit')
    assert time.monotonic()<deadline,'archive deadline exhausted before final readback'

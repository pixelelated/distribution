"""Selected unarmed installed readback. One fresh boot, no game launch."""
import json
import os
import shlex
import sys
import time
from pathlib import Path
from common import write
from materialize import fingerprint

S='/tmp/pix-installed-qa'

def check_boundaries(config,owner,name='budget'):
    for field in ('backing','raw_backing'):
        row=config[field]
        assert fingerprint(Path(row['path']))==row['identity'],field+' drift'
    available=os.statvfs(owner)
    assert available.f_bavail*available.f_frsize>=config['host_floor']+64*1024**2,'host floor reserve'
    run=Path(os.environ['RASTERATOPS_BUILD_RUN'])
    if not run.is_absolute():
        run=Path(config['checkout'])/run
    chain_file=owner/'vm/disk.qcow2'
    qemu_log=owner/'records/qemu.log'
    paths=[p for d in (owner,run) for p in d.rglob('*') if p.is_file() and not p.is_symlink()]
    charged=sum(x.stat().st_blocks*512 for x in paths if x not in (chain_file,qemu_log))
    assert charged<=config['other_outputs_limit'],'other outputs allowance'
    write(owner/'records'/(name+'.json'),
          {'boot_qa_other_allocated_bytes':charged,'top_overlay_allocated_bytes':chain_file.stat().st_blocks*512,
           'qemu_log_allocated_bytes':qemu_log.stat().st_blocks*512,
           'workspace_available_bytes':available.f_bavail*available.f_frsize},True)


def verify_drives(ctx,qemu,owner):
    proc=Path('/proc')/str(qemu.pid)
    open_paths={}
    for fd in (proc/'fd').iterdir():
        try:
            target=os.readlink(fd)
            if target in (ctx.c['backing']['path'],ctx.c['raw_backing']['path'],str(owner/'vm/disk.qcow2')):
                line=next(x for x in (proc/'fdinfo'/fd.name).read_text().splitlines() if x.startswith('flags:'))
                open_paths.setdefault(target,[]).append(int(line.split()[1],8)&os.O_ACCMODE)
        except FileNotFoundError:
            continue
    for field in ('backing','raw_backing'):
        modes=open_paths.get(ctx.c[field]['path'])
        assert modes and all(mode==os.O_RDONLY for mode in modes),(field,modes)
    assert os.O_RDWR in open_paths.get(str(owner/'vm/disk.qcow2'),[])
    write(owner/'records/qemu-drive-access.json',open_paths,True)


def execute(ctx,qemu,owner,deadline,admitted):
    assert ctx.c['selected_case']=='1433-unarmed-pregame'
    assert deadline-time.monotonic()>200
    verify_drives(ctx,qemu,owner)
    tag='M7_1433_PREGAME='
    prior=shlex.quote(ctx.c['previous_boot'])
    ctx.serial_ok('verified-boot-and-fixture-transport',f'''
set -eu
test "$(ls /sys/class/net)" = lo
test "$(cat /proc/sys/kernel/random/boot_id)" != {prior}
grep -Fx 'BUILD_ID="{ctx.c['source']}"' /etc/os-release
grep -Fx 'BUILD_DIRTY="no"' /etc/os-release
test -z "$(ls -A /storage/.update)"
test "$(cat /sys/block/vdb/serial)" = M7BOOTPREP
test "$(cat /sys/block/vdb/ro)" = 1
test ! -d /sys/block/vdc
test ! -e {S}
mkdir -m 700 {S}
tar -xf /dev/vdb -C {S}
cd {S}
sha256sum -c SHA256SUMS
''',20)
    body,rc=ctx.serial('1433-pregame',f'''
set -eu
test "$(ls /sys/class/net)" = lo
pid="$(pgrep -x emulationstation)"
set -- $pid
test "$#" = 1
exec python3 -I -B {S}/guest-readback.py --package-readback {S}/packaged-readback.json --es-pid "$1" --previous-boot {prior}
''',45)
    messages=[x[len(tag):] for x in body.splitlines() if x.startswith(tag)]
    if len(messages)==1:
        observation=json.loads(messages[0])
        write(owner/'records/1433-pregame.json',observation,True)
    else:
        raise RuntimeError('expected exactly one original pre-game observation; see serial record')
    check_boundaries(ctx.c,owner)
    assert rc==0 and observation['status']=='PREGAME_INSTALLED_READBACK_ONLY','PA readback did not accept the guest'
    ctx.command('ordinary-frame',[sys.executable,'-I','-B',ctx.c['tools']['visual'],
        '--monitor',str(owner/'vm/m.sock'),'shot',str(owner/'frames/ordinary.png')],20)

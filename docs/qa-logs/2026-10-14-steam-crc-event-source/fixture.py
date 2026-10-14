#!/usr/bin/env python3
"""UNRUN complete-installer VM caller fixture. Coordinator allocation required."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import select
import shutil
import signal
import socket
import stat
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MAX_SECONDS = 90
MAX_BYTES = 64 * 1024**2
MAX_LOG_BYTES = 2 * 1024**2
MIN_FREE_BYTES = 2368 * 1024**2
CALLS = ['ensure_fex_rootfs', 'link_steam_library', 'ensure_steam_desktop_stub',
         'install_steam_runtime_arm64', 'install_steam_client_arm64', 'install_bundled_proton_files',
         'install_proton_cachyos', 'install_proton_ge', 'run_steam_first_launch']
TOOLS = ('unshare', 'mount', 'chroot', 'bash', 'sh', 'sleep', 'mkdir', 'touch', 'chmod',
         'cp', 'rm', 'ln', 'grep', 'head', 'basename', 'sed', 'strings', 'python3')


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def file_digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def sealed_source(path, binding):
    before = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'Source changed while reading')
    require(digest(raw) == binding['installer_sha256'], 'Installer identity changed; stop for new source review')
    for name, row in binding['helpers'].items():
        first, last = ("<<'" + row['marker'] + "'\n").encode(), ('\n' + row['marker'] + '\n').encode()
        require(raw.count(first) == raw.count(last) == 1, 'Ambiguous embedded helper')
        require(digest(raw.split(first, 1)[1].split(last, 1)[0]) == row['helper_sha256'], name + ' helper changed')
        shell = raw[raw.index((row['shell_start'] + '() {').encode()):raw.index((row['shell_end'] + '() {').encode())]
        require(digest(shell) == row['shell_function_sha256'], name + ' shell changed')
    return raw


def verify_packet():
    seen = set()
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = HERE / name
        require(name not in seen and not Path(name).is_absolute() and '..' not in Path(name).parts,
                'Unsafe packet entry')
        require(path.resolve(strict=True) == path and path.is_file() and not path.is_symlink(), 'Aliased packet input')
        require(file_digest(path) == expected, 'Packet hash changed: ' + name)
        seen.add(name)
    actual = set()
    for path in HERE.rglob('*'):
        require(not path.is_symlink(), 'Unexpected packet symlink')
        if path.is_file() and path != HERE / 'SHA256SUMS':
            actual.add(str(path.relative_to(HERE)))
    require(actual == seen, 'Incomplete/extra packet files')
    return json.loads((HERE / 'source.json').read_text())


def manifest(root):
    rows = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(base) / name
            info = path.lstat()
            row = {'mode': info.st_mode, 'device': info.st_dev, 'inode': info.st_ino}
            if stat.S_ISLNK(info.st_mode):
                row['link'] = os.readlink(path)
            elif stat.S_ISREG(info.st_mode):
                row.update(bytes=info.st_size, sha256=file_digest(path))
            else:
                require(stat.S_ISDIR(info.st_mode), 'Unexpected synthetic file type')
            rows[str(path.relative_to(root))] = row
    return rows


def namespaces():
    return {name: os.readlink('/proc/self/ns/' + name) for name in ('mnt', 'pid', 'net', 'ipc', 'uts')}


def allocated_bytes(path):
    # Count directory entries, symlink text, allocated blocks, and logical bytes.
    # A monitor is not a quota; use a disposable filesystem with a hard cap in VM.
    total = entries = 0
    for base, dirs, files in os.walk(path, followlinks=False):
        for name in dirs + files:
            try:
                info = (Path(base) / name).lstat()
            except FileNotFoundError:
                continue  # A fixture atomically renamed/removed its own entry.
            entries += 1
            total += max(info.st_size, info.st_blocks * 512)
            require(entries <= 100000, 'Combined fixture exceeded the entry limit')
    return total

def proc_table():
    result = {}
    for entry in Path('/proc').iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            # comm may contain spaces or parentheses; fields follow its final ')'.
            fields = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            result[int(entry.name)] = {'pid': int(entry.name), 'state': fields[0],
                                       'ppid': int(fields[1]), 'start_ticks': int(fields[19])}
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError:
            continue
    return result

def descendants():
    table = proc_table()
    owners = {os.getpid()}
    while True:
        added = {pid for pid, item in table.items() if item['ppid'] in owners} - owners
        if not added:
            break
        owners |= added
    return {pid: table[pid] for pid in owners if pid != os.getpid()}

def signal_owned(items, signum):
    current = descendants()
    for pid, item in items.items():
        now = current.get(pid)
        if now and now['start_ticks'] == item['start_ticks'] and now['state'] != 'Z':
            try:
                os.kill(pid, signum)
            except ProcessLookupError:
                pass

def reap_adopted():
    # Called only after Popen.wait/poll has consumed the suite owner status.
    # PR_SET_CHILD_SUBREAPER keeps setsid/forked FEX descendants in this owner.
    receipts = []
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            break
        if pid == 0:
            break
        receipts.append({'pid': pid, 'exit': os.waitstatus_to_exitcode(status)})
    return receipts

def quiesce(proc, terminate=False):
    before = descendants()
    live = {pid: row for pid, row in before.items() if row['state'] != 'Z'}
    intervention = terminate or bool(live)
    if intervention:
        signal_owned(before, signal.SIGTERM)
        deadline = time.monotonic() + 1
        while time.monotonic() < deadline:
            proc.poll()
            if not any(row['state'] != 'Z' for row in descendants().values()):
                break
            time.sleep(0.02)
        signal_owned(descendants(), signal.SIGKILL)
    code = proc.wait(timeout=5)
    reaped = []
    deadline = time.monotonic() + 3
    while True:
        reaped += reap_adopted()
        remaining = descendants()
        if not remaining:
            break
        require(time.monotonic() < deadline, 'Owned descendants did not become quiescent; stop allocation')
        signal_owned(remaining, signal.SIGKILL)
        time.sleep(0.02)
    return {'suite_exit': code, 'intervention': intervention,
            'descendants_at_exit': list(before.values()), 'adopted_exits': reaped,
            'quiescent': True}


def prepare_tools(jail):
    paths = {}
    for name in TOOLS:
        candidate = shutil.which(name, path='/usr/bin:/bin:/usr/sbin:/sbin')
        require(candidate is not None, 'Missing installed prerequisite: ' + name)
        path = Path(candidate).resolve(strict=True)
        require(path.is_file(), 'Invalid installed tool: ' + name)
        require(Path(candidate).is_absolute() and Path(candidate).name == name, 'Ambiguous tool invocation')
        paths[name] = {'invoke_path': candidate, 'resolved_path': str(path), 'sha256': file_digest(path)}
    roots = sorted({Path(p).resolve(strict=True) for p in ('/usr', '/bin', '/lib', '/lib64') if Path(p).exists()},
                   key=lambda p: len(p.parts))
    roots = [p for p in roots if not any(p != other and p.is_relative_to(other) for other in roots)]
    require(all(any(Path(row['resolved_path']).is_relative_to(p) for p in roots) for row in paths.values()),
            'Tool outside immutable bind roots')
    for path in roots:
        (jail / 'system' / str(path).lstrip('/')).mkdir(parents=True, exist_ok=True)
    for name, row in paths.items():
        target = jail / 'usr/bin' / name
        if not target.exists():
            target.symlink_to('/system' + row['resolved_path'])
    for name in ('bash', 'sh'):
        (jail / 'bin' / name).symlink_to('/system' + paths[name]['resolved_path'])
    # Native loader/stdlib/library bytes stay in read-only mounts; no cache copy.
    for top in ('lib', 'lib64'):
        if Path('/' + top).exists():
            (jail / top).symlink_to('/system' + str(Path('/' + top).resolve(strict=True)))
    for path in Path('/usr/lib').iterdir():
        target = jail / 'usr/lib' / path.name
        if not target.exists() and not target.is_symlink():
            resolved = path.resolve()
            if any(resolved.is_relative_to(p) for p in roots):
                target.symlink_to('/system' + str(resolved))
    return paths, [str(p) for p in roots]


def recorded_tool(paths, name):
    row = paths[name]
    invoke = Path(row['invoke_path'])
    require(invoke.is_absolute() and invoke.name == name, 'Invalid recorded applet invocation')
    resolved = invoke.resolve(strict=True)
    require(str(resolved) == row['resolved_path'] and file_digest(resolved) == row['sha256'],
            'Installed executable changed: ' + name)
    return str(invoke)  # argv[0] must retain the applet, even when its bytes are BusyBox.


def namespace_launcher(output, control):
    binding = verify_packet()
    owner = json.loads((output / 'owner.json').read_text())
    require(os.geteuid() == 0 and Path('/sys/class/dmi/id/sys_vendor').read_text().strip() == 'QEMU',
            'Namespace launcher requires allocated root QEMU guest')
    require(namespaces() == owner['namespaces'] and os.getppid() == owner['owner_pid'],
            'Launcher no longer belongs to fixture owner')
    require(proc_table()[os.getppid()]['start_ticks'] == owner['owner_start_ticks'], 'Owner identity changed')
    for name in ('unshare', 'mount', 'chroot'):
        recorded_tool(owner['tools'], name)
        require(owner['tools'][name]['sha256'] == binding['applet_revision']['namespace_tool_sha256'],
                'Namespace tool differs from inspected BusyBox 1.36.1 bytes')
    # Reference this exact process before exec/fork; no numeric parent-PID lookup
    # is possible from PID 1 after BusyBox mounts the namespace's private procfs.
    parent_fd = os.pidfd_open(os.getpid(), 0)
    os.set_inheritable(parent_fd, True)
    argv = [recorded_tool(owner['tools'], 'unshare'), '-m', '-p', '-n', '-i', '-u',
            '-f', '--mount-proc', sys.executable, '-I', '-S', '-B', str(Path(__file__).resolve()),
            '--namespace-worker', str(output), '--parent-pidfd', str(parent_fd)]
    if control:
        argv += ['--namespace-control', control]
    receipt = output / ('launcher-' + (control or 'caller') + '.json')
    receipt.write_text(json.dumps({'argv': argv, 'launcher_pid': os.getpid(),
                                   'parent_pidfd': parent_fd, 'control': control,
                                   'mechanism': 'inherited self pidfd; worker arms parent-death SIGKILL then polls'}, indent=2) + '\n')
    os.execve(argv[0], argv, {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'C', 'LC_ALL': 'C'})


def arm_parent_death(parent_fd):
    require(isinstance(parent_fd, int) and parent_fd >= 3, 'Missing inherited parent pidfd')
    require(os.readlink('/proc/self/fd/' + str(parent_fd)) == 'anon_inode:[pidfd]', 'Not a parent pidfd')
    libc = ctypes.CDLL(None, use_errno=True)
    require(libc.prctl(1, signal.SIGKILL, 0, 0, 0) == 0, 'Parent-death SIGKILL setup failed')
    chosen = ctypes.c_int()
    require(libc.prctl(2, ctypes.byref(chosen), 0, 0, 0) == 0 and chosen.value == signal.SIGKILL,
            'Parent-death SIGKILL readback failed')
    poller = select.poll()
    poller.register(parent_fd, select.POLLIN | select.POLLHUP | select.POLLERR)
    try:
        # As in util-linux --kill-child, close the parent-exited-before-prctl race.
        require(not poller.poll(0), 'Namespace parent exited before guard armed')
    finally:
        os.close(parent_fd)
    return {'signal': int(signal.SIGKILL), 'readback': chosen.value,
            'parent_pidfd_alive_after_arm': True, 'pidfd_closed': True}


def namespace_control(output, parent_fd, kind):
    owner = json.loads((output / 'owner.json').read_text())
    current = namespaces()
    require(os.getpid() == 1 and all(current[n] != owner['namespaces'][n] for n in current),
            'Cleanup control requires private namespaces and PID 1')
    require(int(Path('/proc/self/stat').read_text().split(' ', 1)[0]) == 1, 'Control procfs mismatch')
    control = output / 'supervision' / kind
    if kind == 'parent-exit-before-arm':
        poller = select.poll()
        poller.register(parent_fd, select.POLLIN | select.POLLHUP | select.POLLERR)
        (control / 'ready').write_text('kill unshare parent before arm\n')
        require(poller.poll(3000), 'Control parent was not killed within bound')
        try:
            arm_parent_death(parent_fd)
        except RuntimeError as error:
            require(str(error) == 'Namespace parent exited before guard armed', 'Wrong guard refusal: ' + str(error))
            (control / 'refusal.json').write_text(json.dumps({'expected_refusal': str(error), 'original_exit': 77}) + '\n')
            return 77
        raise RuntimeError('Dead parent was accepted')
    require(kind == 'parent-exit-after-arm', 'Unknown cleanup control')
    guard = arm_parent_death(parent_fd)
    child = os.fork()
    if child == 0:
        os.setsid()
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        (control / 'detached-child-ready').write_text(str(os.getpid()) + '\n')
        time.sleep(30)  # Must die with PID 1; this delay is never a success path.
        os._exit(93)
    deadline = time.monotonic() + 1
    while not (control / 'detached-child-ready').exists():
        require(time.monotonic() < deadline, 'Detached control child did not become ready')
        time.sleep(0.01)
    (control / 'guard.json').write_text(json.dumps(guard) + '\n')
    (control / 'ready').write_text('kill unshare parent after arm, with detached child\n')
    time.sleep(30)
    return 94


def supervision_controls(output, started):
    results = []
    for kind in ('parent-exit-after-arm', 'parent-exit-before-arm'):
        control = output / 'supervision' / kind
        control.mkdir(parents=True)
        row = {'name': kind, 'status': 'RUNNING', 'attempts': 1, 'namespace_owner_original_exit': None}
        proc = None
        try:
            argv = [sys.executable, '-I', '-S', '-B', str(Path(__file__).resolve()),
                    '--namespace-launcher', str(output), '--namespace-control', kind]
            row['argv'] = argv
            with (control / 'stdout').open('wb') as stdout, (control / 'stderr').open('wb') as stderr:
                proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                        env={'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'C', 'LC_ALL': 'C'},
                                        start_new_session=True)
                deadline = min(started + MAX_SECONDS, time.monotonic() + 3)
                while not (control / 'ready').exists():
                    require(proc.poll() is None, 'Cleanup control launcher failed')
                    require(time.monotonic() < deadline, 'Cleanup control readiness deadline')
                    require(allocated_bytes(output) <= MAX_BYTES, 'Cleanup control retained-data limit')
                    require(max((control / 'stdout').stat().st_size, (control / 'stderr').stat().st_size) <= MAX_LOG_BYTES,
                            'Cleanup control log limit')
                    time.sleep(0.01)
                require(proc.poll() is None, 'Cleanup control parent already exited')
                proc.kill()  # Intentional death of only the unshare parent; no rescue yet.
                row['namespace_owner_original_exit'] = proc.wait(timeout=2)
                deadline = min(started + MAX_SECONDS, time.monotonic() + 2)
                while any(r['state'] != 'Z' for r in descendants().values()) and time.monotonic() < deadline:
                    time.sleep(0.01)
                row['live_before_rescue'] = [r for r in descendants().values() if r['state'] != 'Z']
                require(row['namespace_owner_original_exit'] == -signal.SIGKILL, 'Wrong original parent exit')
                require(not row['live_before_rescue'], 'Parent-death guard left live descendants')
                row['supervision'] = quiesce(proc)
                require(not row['supervision']['intervention'], 'Control needed cleanup rescue')
                codes = [r['exit'] for r in row['supervision']['adopted_exits']]
                expected = -signal.SIGKILL if kind == 'parent-exit-after-arm' else 77
                require(codes and all(code == expected for code in codes), 'Wrong original control child exits: ' + repr(codes))
                if kind == 'parent-exit-before-arm':
                    require(json.loads((control / 'refusal.json').read_text())['original_exit'] == 77, 'Missing explicit race refusal')
                row['status'] = 'PASS'
        except BaseException as error:
            row['status'] = 'FAIL'
            row['error'] = repr(error)
            raise
        finally:
            if proc is not None and (proc.poll() is None or descendants()):
                row['failure_cleanup'] = quiesce(proc, terminate=True)
            if proc is not None:
                row['namespace_owner_original_exit'] = proc.returncode
            row['remaining_descendants'] = list(descendants().values())
            (control / 'result.json').write_text(json.dumps(row, indent=2) + '\n')
        results.append(row)
    return results


def require_empty_routes(raw):
    # A zero-byte proc table and a header-only table both contain zero rows.
    # Never accept a headerless route merely because it occupies one line.
    require(isinstance(raw, str), 'Route table was not text')
    if raw == '':
        return {'representation': 'empty', 'data_rows': 0}
    header = ['Iface', 'Destination', 'Gateway', 'Flags', 'RefCnt', 'Use',
              'Metric', 'Mask', 'MTU', 'Window', 'IRTT']
    lines = raw.splitlines()
    require(len(lines) == 1 and lines[0].split() == header,
            'New network namespace route table has data or unrecognized text')
    return {'representation': 'header-only', 'data_rows': 0}


def route_oracle_controls():
    cases = json.loads((HERE / 'route-cases.json').read_text())
    results = []
    for case in cases:
        try:
            observation = require_empty_routes(case['raw'])
            accepted = True
        except RuntimeError as error:
            observation = {'refusal': str(error)}
            accepted = False
        row = {'name': case['name'], 'expected_accept': case['accept'],
               'actual_accept': accepted, 'observation': observation}
        require(accepted is case['accept'], 'Route oracle control failed: ' + json.dumps(row))
        results.append(row)
    return results


def namespace_worker(output, parent_pidfd):
    owner = json.loads((output / 'owner.json').read_text())
    current = namespaces()
    require(os.getpid() == 1 and all(current[n] != owner['namespaces'][n] for n in current),
            'Refusing mounts without distinct mount/PID/network/IPC/UTS namespaces')
    require(int(Path('/proc/self/stat').read_text().split(' ', 1)[0]) == os.getpid(),
            'proc does not represent the new PID namespace')
    guard = arm_parent_death(parent_pidfd)
    jail = output / 'rootfs'
    mount = recorded_tool(owner['tools'], 'mount')
    report = {'status': 'RUNNING', 'namespaces': current, 'parent_death_guard': guard,
              'mount_commands': [], 'installer_exit': None,
              'evidence': 'complete sealed installer, synthetic profile/fetch/payload/engine boundaries'}
    def mounted(args):
        argv = [mount, '-n', *map(str, args)]  # Never write the guest's shared /etc/mtab.
        result = subprocess.run(argv, capture_output=True, timeout=5)
        report['mount_commands'].append({'argv': argv, 'original_exit': result.returncode,
                                        'stderr': result.stderr.decode()})
        require(result.returncode == 0, 'Namespace mount failed')
    try:
        mounted(['--make-rprivate', '/'])
        mounted(['--bind', jail, jail])
        for root in owner['native_roots']:
            target = jail / 'system' / root.lstrip('/')
            mounted(['--bind', root, target])
            mounted(['-o', 'remount,bind,ro,nosuid,nodev', target])
        for name in ('storage', 'qa', 'tmp'):
            mounted(['--bind', output / name, jail / name])
        mounted(['-t', 'proc', '-o', 'nosuid,nodev,noexec', 'proc', jail / 'proc'])
        mounted(['-o', 'remount,ro,nosuid,nodev,noexec', jail / 'proc'])
        require((jail / 'proc/sys/fs/binfmt_misc').is_dir(), 'Missing private binfmt mount target')
        mounted(['--bind', output / 'binfmt', jail / 'proc/sys/fs/binfmt_misc'])
        null = Path('/dev/null').lstat()
        require(stat.S_ISCHR(null.st_mode) and os.major(null.st_rdev) == 1 and os.minor(null.st_rdev) == 3,
                'Unexpected /dev/null identity')
        report['null_identity'] = {'device': null.st_dev, 'inode': null.st_ino, 'mode': null.st_mode, 'rdev': null.st_rdev}
        (jail / 'dev/null').touch()
        mounted(['--bind', '/dev/null', jail / 'dev/null'])
        mounted(['-o', 'remount,bind,ro,nosuid,nodev', jail])
        env = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'HOME': '/storage',
               'TMPDIR': '/tmp', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONNOUSERSITE': '1',
               'DEVICE_HAS_DUAL_SCREEN': 'false', 'PS4': '+ '}
        report['interpreter'] = sys.version
        report['mountinfo_before'] = Path('/proc/self/mountinfo').read_text()
        report['route_oracle_controls'] = route_oracle_controls()
        report['routes_before'] = Path('/proc/net/route').read_text()
        report['route_oracle'] = require_empty_routes(report['routes_before'])
        case = owner["case"]
        guard = output / "qa/exec-guard.py"
        chroot = recorded_tool(owner["tools"], "chroot")
        base = [sys.executable, "-I", "-S", "-B", str(guard)]
        report["exec_guard_controls"] = []
        for label, expected in (("exec-denial", 77), ("exec-allowed", 17), ("exec-many-syscalls", 19), ("exec-blocked", 1)):
            receipt = output / (label + ".json")
            control_argv = [*base, "--receipt", str(receipt), "--client", "/qa/guard-should-not-run",
                            "--seconds", "2" if label == "exec-blocked" else "10", "--", chroot, str(jail), "/usr/bin/python3",
                            "-I", "-S", "-B", "/qa/boundary.py", label]
            with (output / (label + ".stdout")).open("wb") as stdout, (output / (label + ".stderr")).open("wb") as stderr:
                control = subprocess.run(control_argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=12)
            observed = json.loads(receipt.read_text())
            require(control.returncode == expected and not observed["remaining_traced"], "Exec guard control failed")
            if label == "exec-blocked":
                require(observed["status"] == "FAIL" and observed["original_caller_exit"] is None
                        and "Exec boundary deadline" in observed.get("error", "")
                        and 2 <= observed["elapsed_seconds"] < 7 and observed["cleanup_exits"],
                        "Blocking wait was not bounded with an honest absent caller result")
                events = collect_events(output, "events-controls")
                require(any(e.get("point") == "blocked-wait" for e in events), "Deadline control never reached its idle wait")
            else:
                require(observed["original_caller_exit"] == expected and observed["status"] == "RETURNED",
                        "Exec guard changed an ordinary original exit")
            require(observed["main_loop_poll_sleeps"] == 0, "Main trace loop polled with sleeps")
            if label == "exec-many-syscalls":
                require(observed["syscall_stops"] >= 4000, "Busy syscall control did not exercise wait overhead")
            require(len(observed["denied_execs"]) == (1 if label == "exec-denial" else 0)
                    and not (output / "qa/guard-escaped").exists(), "Exec guard did not deny only its target")
            report["exec_guard_controls"].append({"case": label, "driver_exit": control.returncode,
                "original_caller_exit": observed["original_caller_exit"], "status": "PASS"})
        report["attempts"] = []
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location("case_payload", output / "qa/payload.py")
        payload = module_from_spec(spec)
        spec.loader.exec_module(payload)
        for attempt in range(1, 3 if case in payload.RETRIES | payload.RETRY_REFUSALS else 2):
            (output / "qa/attempt.json").write_text(json.dumps({"attempt": attempt}) + "\n")
            receipt = output / ("exec-" + str(attempt) + ".json")
            argv = [*base, "--receipt", str(receipt), "--client", str(payload.STEAM / "steamrtarm64/steam"),
                    "--seconds", str(owner["seconds"] - 10), "--", chroot, str(jail), "/bin/bash",
                    "--noprofile", "--norc", "-x", "/usr/config/modules/Install Steam.sh"]
            with (output / ("installer-" + str(attempt) + ".stdout")).open("wb") as stdout, (output / ("installer-" + str(attempt) + ".stderr")).open("wb") as stderr:
                proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, env=env)
                original = proc.wait()
            observation = json.loads(receipt.read_text())
            row = {"attempt": attempt, "installer_exit": observation["original_caller_exit"],
                   "trace_driver_exit": original, "trace": observation}
            report["attempts"].append(row)
            report["installer_exit"] = observation["original_caller_exit"]
            report["trace_driver_exit"] = original
            # Even guard failure has an immediate original receipt; an absent
            # caller result must not be filled with the trace driver's exit.
            (output / ("attempt-" + str(attempt) + "-result.json")).write_text(json.dumps(row, indent=2) + "\n")
            require(observation["status"] == "RETURNED" and original == observation["original_caller_exit"]
                    and not observation["remaining_traced"], "Trace boundary did not return the original caller exit")
            (output / ("attempt-" + str(attempt) + "-storage.json")).write_text(json.dumps(manifest(output / "storage"), indent=2) + "\n")
            root = output / "storage" / payload.case_root(case).relative_to("/storage")
            journal = root / ".steam-client-update/owner.jsonl"
            if journal.is_file() and not journal.is_symlink():
                require(journal.stat().st_size <= 2 * 1024**2, "Journal receipt exceeds bound")
                (output / ("attempt-" + str(attempt) + "-journal.jsonl")).write_bytes(journal.read_bytes())
            # Preserve the original failed result on disk before the deliberately
            # requested second invocation. Never replace attempt 1 with its retry.
            (output / ("attempt-" + str(attempt) + "-result.json")).write_text(json.dumps(row, indent=2) + "\n")
            if attempt == 1 and case in payload.RETRIES | payload.RETRY_REFUSALS:
                require(original == 1, "First fault did not produce the expected original caller failure")
                first_error = (output / "installer-1.stderr").read_text(errors="replace")
                events = collect_events(output, "events-attempt-1")
                if case == "proc-census-error":
                    require("Transfer quiescence is unestablished" in first_error and journal.is_file(),
                            "Census failure permitted transaction cleanup")
                    require(any(e.get("point") == "proc-stat-visibility-gap" for e in events), "Missing exact census refusal")
                    held = json.loads((output / "qa/held-state-observation.json").read_text())
                    require(held["status"] == "OBSERVED_HELD_WHILE_CHILD_LIVE"
                            and any(e["exit"] == 77 for e in observation["original_exits"]),
                            "Independent FD holder did not prove held state before releasing itself")
                elif case == "crc-failure-retry":
                    require("CRC, length" in first_error, "Failure did not reach candidate CRC validation")
                elif case == "download-failure-retry":
                    require(any(e.get("original_exit") == 23 and e.get("point") == "partial-transport" for e in events), "Missing original transfer failure")
                elif case == "validation-failure-retry":
                    require("not an ARM64 ELF" in first_error, "Failure did not reach bootstrap validation")
                elif case == "publication-failure-retry":
                    require(any(e.get("point") == "publication-rename" for e in events), "Missing exact publication failure")
                elif case == "metadata-failure-retry":
                    require(any(e.get("point") == "metadata-beta-open" for e in events), "Missing exact metadata failure")
                else:
                    require(any(e.get("kind") == "fault" and e.get("original_signal") == 9 for e in events)
                            and any(e["exit"] == -9 for e in observation["original_exits"]), "Missing original signal interruption")
                    require(journal.is_file(), "Interrupted transaction did not preserve its journal")
                if case == "committed-self-update-retry":
                    payload.put(root / "steamrtarm64/steamclient.so",
                                payload.bootstrap_elf(False, b"independent-self-update-after-commit"))
                    payload.put(root / "package/beta", "preserved-after-self-update\n")
                    (output / "self-update-control.json").write_text(json.dumps({
                        "meaning": "synthetic actor only, no actual self-update", "path": "steamrtarm64/steamclient.so",
                        "sha256": file_digest(root / "steamrtarm64/steamclient.so"),
                        "beta": "preserved-after-self-update\n"}, indent=2) + "\n")
        report["adopted_exits"] = reap_adopted()
        report["remaining_descendants"] = list(descendants().values())
        require(not report["remaining_descendants"], "Full caller left descendants; namespace will be retired")
        report["status"] = "RETURNED"
    except BaseException as error:
        report['status'] = 'FAIL'
        report['error'] = repr(error)
    finally:
        (output / 'namespace-result.json').write_text(json.dumps(report, indent=2) + '\n')
    return 0 if report['status'] == 'RETURNED' else 1


def collect_events(output, label):
    # Called only after the original trace result proves no remaining tracees,
    # or from assess after unchanged outer quiescence has succeeded.
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("event_records", HERE / "event_records.py")
    records = module_from_spec(spec)
    spec.loader.exec_module(records)
    return records.collect(output / "qa", output / (label + ".ndjson"))


def assess(output, before, payload, case):
    after = manifest(output / "storage")
    (output / "after.json").write_text(json.dumps(after, indent=2) + "\n")
    ns = json.loads((output / "namespace-result.json").read_text())
    attempts = ns["attempts"]
    events = collect_events(output, "events-collected")
    last = attempts[-1]["attempt"]
    stdout = (output / ("installer-" + str(last) + ".stdout")).read_text(errors="replace")
    stderr = (output / ("installer-" + str(last) + ".stderr")).read_text(errors="replace")
    root = output / "storage" / payload.case_root(case).relative_to("/storage")
    prefix = str(payload.case_root(case).relative_to("/storage"))
    early = case in payload.EARLY
    refused = early or case in ("metadata-conflict-after-profile", "transport-timeout", "proc-census-error")
    expected_exits = ([1, 1] if case in payload.RETRY_REFUSALS else [1, 0] if case in payload.RETRIES else [1] if refused else [0])
    require([a["installer_exit"] for a in attempts] == expected_exits, "Wrong original full-caller exit sequence")
    require(len(attempts) == (2 if case in payload.RETRIES | payload.RETRY_REFUSALS else 1), "Unexpected implicit retry")
    protected = [prefix + "/" + name for name in ("steamapps", "userdata", "depotcache", "linuxarm64",
                 "custom-root-file", "compatibilitytools.d/proton-cachyos-old-arm64", "compatibilitytools.d/GE-Protonold-aarch64")]
    protected += ["games-internal/roms/other-library", "games-internal/roms/steam/unrelated",
                  "games-external", ".steam/fixture-existing", ".local/share/fex-emu/RootFS/OtherRoot",
                  ".local/share/fex-emu/RootFS/ArchLinux.sqsh"]
    if case in payload.EXISTING:
        support_prefix = str(payload.support_root(case).relative_to("/storage"))
        protected += [prefix + "/steamrtarm64", prefix + "/package", support_prefix + "/steam", support_prefix + "/sdkarm64"]
    if case in ("fresh-profile-dot", "existing-profile-dot"):
        protected += ["custom-profile/support/preserve"]
    if case in ("fresh-profile-parent-alias", "existing-profile-parent-alias"):
        protected += ["profile", "link", "support", "elsewhere/deep", "elsewhere/support/preserve"]
    checks = {}
    for p in protected:
        old = {k: v for k, v in before.items() if k == p or k.startswith(p + "/")}
        new = {k: v for k, v in after.items() if k == p or k.startswith(p + "/")}
        checks[p] = bool(old) and old == new
    require(all(checks.values()), "Client transaction/caller changed protected synthetic data")
    # Existing FEX's deliberate atomic refresh keeps extra bytes/mode, not inode.
    extra = ".config/fex-emu/AppConfig/extra.json"
    require({k: v for k, v in before[extra].items() if k not in ("device", "inode")} ==
            {k: v for k, v in after[extra].items() if k not in ("device", "inode")}, "FEX extra changed")
    for name in (prefix,):
        require(before[name] == after[name], "Steam root identity changed")
    if case == "valid-existing-alias":
        logical = str(payload.STEAM.relative_to("/storage"))
        require(before[logical] == after[logical], "Existing allowed alias changed")
    if early:
        require(before == after and not (output / "storage/profile-ran").exists()
                and not (output / "tmp/.process-kill-data").exists(), "Pre-profile refusal performed writes")
        require(not any(e.get("command") in ("profile", "set_kill", "curl", "wget", "FEXRootFSFetcher") for e in events),
                "Early refusal reached a mutating boundary")
    elif case == "metadata-conflict-after-profile":
        only = "profile-ran"
        require({k: v for k, v in after.items() if k != only} == before and only in after, "Metadata refusal exceeded profile effects")
        require(not any(e.get("command") in ("set_kill", "curl", "wget", "FEXRootFSFetcher") for e in events),
                "Metadata refusal reached later installer operations")
    else:
        require((output / "storage/profile-ran").is_file(), "Full caller did not source profile")
    final_success = "Steam setup finished. Start Steam to continue." in stdout
    require(final_success is (not refused), "Misleading or missing terminal setup status")
    denied = [e for a in attempts for e in a["trace"]["denied_execs"]]
    require(len(denied) == (0 if refused else 1) and all(e["forced_errno"] == 13 for e in denied),
            "Native client execution was not denied at its exact syscall")
    require(all(not a["trace"]["client_executed"] and not a["trace"]["native_client_success"] for a in attempts),
            "Synthetic structure must not claim native client success")
    if not refused:
        reached = [line.lstrip("+").strip() for line in stderr.splitlines() if line.lstrip("+").strip() in CALLS]
        require(reached == CALLS, "Final complete caller missed its original component order")
        require(not (root / ".steam-client-update").exists(), "Completed client transaction left staging")
        require((output / "storage/.local/share/fex-emu/RootFS/ArchLinux/synthetic-generation").read_text() == "new-fex",
                "Preserved FEX helper did not complete")
        for path in (root / ".steam-runtime-update", root / ".proton-variant-stage",
                     output / "storage/.local/share/fex-emu/.steam-fex-update"):
            require(not path.exists(), "Existing helper did not retire its own stage")
        if case not in payload.EXISTING and case != "committed-self-update-retry":
            expected_files = payload.client_files()
            for name, data in expected_files.items():
                path = root / name
                require(not path.is_symlink() and path.read_bytes() == data, "Fresh client bytes differ: " + name)
            for row in payload.layout():
                path = root / row["canonical_name"].rstrip("/")
                if row["kind"] == "symlink":
                    require(path.is_symlink() and os.readlink(path) == row["relative_target"]
                            and path.resolve().is_file(), "Fresh stored link did not resolve inside client")
                require(not (root / row["raw_name"].rstrip("/")).exists() if "\\" in row["raw_name"] else True,
                        "Literal-backslash sibling was incorrectly published")
            require((root / "package/beta").read_bytes() == b"publicbeta\n", "Wrong fresh channel")
            support = output / "storage" / payload.support_root(case).relative_to("/storage")
            require(os.readlink(support / "steam") == str(payload.STEAM)
                    and os.readlink(support / "sdkarm64") == str(payload.STEAM / "linuxarm64"), "Wrong fresh support aliases")
        if case == "committed-self-update-retry":
            actor = json.loads((output / "self-update-control.json").read_text())
            require(file_digest(root / "steamrtarm64/steamclient.so") == actor["sha256"]
                    and (root / "package/beta").read_text() == actor["beta"], "Committed client was checked against obsolete bytes")
        if case in payload.EXISTING:
            require(not any(e.get("kind") == "archive-copy" and e.get("name") == "client.zip" for e in events),
                    "Existing client was reacquired")
    if case in ("fresh-profile-parent-alias", "existing-profile-parent-alias"):
        support = output / "storage/elsewhere/support"
        require((support / "registry.vdf").is_file() and not (output / "storage/support/registry.vdf").exists(),
                "Registry and client metadata did not use the same actual support directory")
        require(os.readlink(support / "steam") == str(payload.STEAM)
                and os.readlink(support / "sdkarm64") == str(payload.STEAM / "linuxarm64"),
                "Actual profile alias destination lacks its support links")
    if case in ("detached-transfer-child", "transport-timeout"):
        child = json.loads((output / "qa/detached-child-ready-1.json").read_text())
        require(any(e["pid"] == child["pid"] and e["exit"] == -9 for e in attempts[0]["trace"]["original_exits"])
                and not attempts[0]["trace"]["cleanup_exits"], "Detached child needed tracer rescue instead of product cleanup")
    if case == "proc-census-error":
        first = json.loads((output / "attempt-1-storage.json").read_text())
        second = json.loads((output / "attempt-2-storage.json").read_text())
        require(first == second and prefix + "/.steam-client-update/owner.jsonl" in after
                and prefix + "/steamrtarm64" not in after, "Unresolved transfer state was cleaned or installed on retry")
        require(sum(e.get("command") == "profile" for e in events) == 1
                and not any(e.get("helper") == "client" and e.get("mode") == "install"
                            and e.get("attempt") == 2 for e in events), "Held retry crossed pre-profile admission")
    if case in ("crc-failure-retry", "download-failure-retry", "metadata-failure-retry", "validation-failure-retry", "publication-failure-retry", "transport-timeout"):
        first = json.loads((output / "attempt-1-storage.json").read_text())
        require(prefix + "/steamrtarm64" not in first, "Fresh failure exposed a misleading installed directory")
        require(not any(k == prefix + "/.steam-client-update" or k.startswith(prefix + "/.steam-client-update/") for k in first),
                "Ordinary failed client stage was not safely retired")
    result = {"case": case, "original_installer_exits": expected_exits, "protected": checks,
              "complete_caller": not refused, "native_client_execution": "NOT_REACHED" if refused else "DENIED; not qualification",
              "retry_count": len(attempts) - 1, "profile_effects_rollback": False,
              "unknown_state_preserved": early, "boundary_events": events}
    (output / "caller-observation.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    global MAX_SECONDS
    require(sys.flags.optimize == 0, 'Assertions must remain enabled')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--installer', type=Path)
    parser.add_argument('--disposable-vm', action='store_true')
    parser.add_argument('--case', required=False)
    parser.add_argument('--namespace-worker', type=Path, help=argparse.SUPPRESS)
    parser.add_argument('--namespace-launcher', type=Path, help=argparse.SUPPRESS)
    parser.add_argument('--namespace-control', choices=('parent-exit-after-arm', 'parent-exit-before-arm'), help=argparse.SUPPRESS)
    parser.add_argument('--parent-pidfd', type=int, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.namespace_launcher:
        return namespace_launcher(args.namespace_launcher, args.namespace_control)
    if args.namespace_worker:
        if args.namespace_control:
            return namespace_control(args.namespace_worker, args.parent_pidfd, args.namespace_control)
        return namespace_worker(args.namespace_worker, args.parent_pidfd)
    binding = verify_packet()
    require(args.case in binding['cases'], 'Choose one independent case')
    MAX_SECONDS = 240 if args.case == 'transport-timeout' else 90
    require(args.disposable_vm and os.geteuid() == 0 and platform.machine() == 'x86_64', 'Disposable root GENERIC_X64 VM required')
    vendor = Path('/sys/class/dmi/id/sys_vendor').read_text().strip()
    require(vendor == 'QEMU', 'Refusing non-QEMU environment; no host/device execution')
    installer = (args.installer or ROOT / binding['installer_path']).resolve(strict=True)
    raw = sealed_source(installer, binding)
    scratch = Path(os.environ['TMPDIR']).resolve(strict=True)
    output = args.output
    require(output is not None and output.is_absolute() and output.parent == scratch, 'Output must be a new direct TMPDIR child')
    require(not output.exists() and not output.is_symlink() and not output.is_relative_to(ROOT)
            and not output.is_relative_to(Path('/storage')), 'Refusing reused/source/real-storage scratch')
    require(not (os.statvfs(scratch).f_flag & os.ST_NOEXEC), 'Synthetic fetcher/client scripts need executable scratch')
    free = shutil.disk_usage(scratch).free
    require(free >= MIN_FREE_BYTES, 'Need 2368 MiB free for unchanged Proton reserve plus retained evidence')
    require(not descendants(), 'Caller fixture already owns children')
    libc = ctypes.CDLL(None, use_errno=True)
    require(libc.prctl(36, 1, 0, 0, 0) == 0, 'Subreaper setup failed')
    output.mkdir(mode=0o700)
    report = {'status': 'RUNNING', 'evidence': 'whole sealed caller with synthetic boundaries; not native acceptance',
              'installer_sha256': digest(raw), 'packet_manifest_sha256': file_digest(HERE / 'SHA256SUMS'),
              'python': sys.version, 'python_executable_sha256': file_digest(Path(sys.executable).resolve()),
              'vm_vendor': vendor, 'free_bytes_before': free, 'limits': binding['limits'], 'allocated_case_invocations': 1,
              'installer_original_exit': None, 'case': args.case}
    proc = None
    started = time.monotonic()
    try:
        # Only after seals/VM/scratch guards: import the fixture's data generator.
        sys.path.insert(0, str(HERE))
        import payload
        payload.build(output, HERE, raw, args.case)
        tools, roots = prepare_tools(output / 'rootfs')
        report['tools'] = tools
        launcher = output / 'rootfs/usr/bin/python3'
        require(launcher.is_symlink() and os.readlink(launcher) == '/system' + tools['python3']['resolved_path'], 'Unexpected synthetic interpreter launcher')
        launcher.unlink()
        payload.put(launcher, '#!/bin/sh\nexec /system' + tools['python3']['resolved_path'] + ' -I -S -B /qa/python-boundary.py \"$@\"\n', 0o755)
        (output / 'qa/native-tools.json').write_text(json.dumps(tools, sort_keys=True) + '\n')
        (output / 'binfmt').mkdir()
        for name in ('x86', 'box32', 'box64'):
            (output / 'binfmt' / name).write_text('1\n')
        before = manifest(output / 'storage')
        (output / 'before.json').write_text(json.dumps(before, indent=2) + '\n')
        owner = {'namespaces': namespaces(), 'tools': tools, 'native_roots': roots,
                 'case': args.case, 'seconds': MAX_SECONDS, 'owner_pid': os.getpid(), 'owner_start_ticks': proc_table()[os.getpid()]['start_ticks']}
        (output / 'owner.json').write_text(json.dumps(owner, indent=2) + '\n')
        staged = output / 'rootfs/usr/config/modules/Install Steam.sh'
        require(staged.read_bytes() == raw, 'Staged installer changed')
        report['archives'] = {p.name: {'sha256': file_digest(p), 'bytes': p.stat().st_size}
                              for p in (output / 'qa/payloads').iterdir()}
        report['supervision_controls'] = supervision_controls(output, started)
        argv = [sys.executable, '-I', '-S', '-B', str(Path(__file__).resolve()),
                '--namespace-launcher', str(output)]
        report['owner_argv'] = argv
        with (output / 'owner.stdout').open('wb') as stdout, (output / 'owner.stderr').open('wb') as stderr:
            proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                    env={'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'C', 'LC_ALL': 'C'}, start_new_session=True)
            guard = None
            while proc.poll() is None:
                if time.monotonic() - started >= MAX_SECONDS:
                    guard = 'work deadline'
                if allocated_bytes(output) > MAX_BYTES:
                    guard = 'retained-data limit'
                if any(p.stat().st_size > MAX_LOG_BYTES for p in output.rglob('*.std*')):
                    guard = 'log limit'
                if guard:
                    break
                time.sleep(0.05)
            report['supervision'] = quiesce(proc, terminate=guard is not None)
        report['guard'] = guard
        report['namespace_owner_exit'] = proc.returncode
        require((output / 'namespace-result.json').is_file(),
                'Namespace setup did not produce installer receipt; original owner exit retained')
        ns = json.loads((output / 'namespace-result.json').read_text())
        report['installer_original_exit'] = ns['installer_exit']
        report['trace_driver_exit'] = ns.get('trace_driver_exit')
        require(not guard and proc.returncode == 0 and not report['supervision']['intervention'], 'Namespace execution/supervision failed')
        require(sealed_source(installer, binding) == raw and staged.read_bytes() == raw, 'Source changed during execution')
        report['caller'] = assess(output, before, payload, args.case)
        report['status'] = 'PASS'
    except BaseException as error:
        report['status'] = 'FAIL'
        report['error'] = repr(error)
        if proc is not None and (proc.poll() is None or descendants()):
            report['failure_cleanup'] = quiesce(proc, terminate=True)
    finally:
        report['elapsed_seconds'] = time.monotonic() - started
        report['retained_bytes'] = allocated_bytes(output)
        report['remaining_descendants'] = list(descendants().values())
        if (output / 'storage').is_dir() and not report['remaining_descendants']:
            try:
                (output / 'after.json').write_text(json.dumps(manifest(output / 'storage'), indent=2) + '\n')
            except Exception as error:
                report['after_manifest_error'] = repr(error)
                report['status'] = 'FAIL'
        (output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'status': report['status'], 'result': str(output / 'result.json')}))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())

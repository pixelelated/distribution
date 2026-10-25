"""T11 S2 (#1089): the launcher's PID-file path, its stale-socket clearing and
its two socket paths, judged with no guest.

    python3 -I -B launcher-case.py <generic-x64-vm> <unfixed|fixed> <case>

Cases (positives fail on the unfixed launcher and hold on the fixed one):
  pidfile-symlink  `qemu-args --headless --pidfile <link>`: unfixed prints the
                   link's target after -pidfile; fixed refuses, naming the path.
  socket-swap      prepare_run over a monitor socket judged stale, which a
                   live listener replaces before the clear: unfixed removes the
                   live socket; fixed refuses and leaves it.
  same-paths       `qemu-args --headless` with --monitor and --serial equal:
                   unfixed prints both; fixed refuses.
Controls (the same on both sides):
  pidfile-regular  a plain PID-file path is printed as given.
  socket-dead      a socket nobody listens on is cleared by prepare_run.
  socket-symlink   a symlink at the monitor path is refused and left.
  socket-notsock   a regular file at the monitor path is refused and left.
  socket-live      a socket a live listener holds is refused and left (after
                   the launcher's grace of a few seconds).

Every case stops before QEMU: QEMU_SYSTEM_X86_64 names a stub that refuses to
run, `qemu-args` only prints, and prepare_run is called in-process. Writes
only under $TMPDIR (a sparse 16 GiB qcow2, sockets, links). Prints one verdict
line last; exits 0 when the side's expectation is met, 1 when not, 2 when the
case cannot run.
"""
import importlib.machinery
import importlib.util
import os
import socket
import subprocess
import sys
import tempfile
import types

LAUNCHER, SIDE, CASE = sys.argv[1], sys.argv[2], sys.argv[3]
if SIDE not in ("unfixed", "fixed"):
    print(f"launcher-case: CANNOT -- side {SIDE}")
    sys.exit(2)
W = tempfile.mkdtemp(prefix="s2-launcher.", dir=os.environ["TMPDIR"])
STUB = os.path.join(W, "qemu-stub")
with open(STUB, "w") as f:
    f.write("#!/bin/sh\necho 'qemu-stub: refusing to run' >&2\nexit 97\n")
os.chmod(STUB, 0o755)
DISK = os.path.join(W, "disk.qcow2")
try:
    subprocess.run(["qemu-img", "create", "-q", "-f", "qcow2", DISK, "16G"], check=True)
except (OSError, subprocess.CalledProcessError) as e:
    print(f"launcher-case: CANNOT -- qemu-img: {e}")
    sys.exit(2)


def qemu_count():
    r = subprocess.run(["pgrep", "-x", "qemu-system-x86"], capture_output=True, text=True)
    return len(r.stdout.split())


def qemu_args(*extra):
    env = dict(os.environ, QEMU_SYSTEM_X86_64=STUB)
    cmd = [sys.executable, "-I", "-B", LAUNCHER, "qemu-args", DISK, "--headless", "--gl", "none",
           "--vnc", "47", "--ssh-port", "10947", "--mac", "52:54:00:00:00:47", *extra]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60)
    return r.returncode, r.stdout, r.stderr


def load_launcher():
    loader = importlib.machinery.SourceFileLoader("gxv_under_test", LAUNCHER)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def listener(path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(path)
    s.listen(1)
    return s


def answers(path):
    p = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    p.settimeout(1.0)
    try:
        p.connect(path)
        return True
    except OSError:
        return False
    finally:
        p.close()


def run_args(monitor):
    return types.SimpleNamespace(disk=DISK, ovmf_vars=None, ovmf_code=None, ovmf_vars_template=None,
                                 monitor=monitor, serial=os.path.join(W, "unused-serial.sock"),
                                 headless=False)


before = qemu_count()
facts, ok = "", False
if CASE == "pidfile-symlink":
    target = os.path.join(W, "elsewhere.txt")
    with open(target, "w") as f:
        f.write("not a pid file\n")
    link = os.path.join(W, "qemu.pid")
    os.symlink(target, link)
    rc, out, err = qemu_args("--pidfile", link, "--monitor", os.path.join(W, "m.sock"), "--serial", os.path.join(W, "s.sock"))
    follows = f"-pidfile {target}" in out
    refused = rc != 0 and link in err
    facts = f"rc={rc} prints-target={'yes' if follows else 'no'} refused-naming-link={'yes' if refused else 'no'}"
    ok = (rc == 0 and follows) if SIDE == "unfixed" else (refused and not follows)
    if err.strip():
        print("  | " + err.strip().splitlines()[-1])
elif CASE == "pidfile-regular":
    pid = os.path.join(W, "plain.pid")
    rc, out, err = qemu_args("--pidfile", pid, "--monitor", os.path.join(W, "m.sock"), "--serial", os.path.join(W, "s.sock"))
    facts = f"rc={rc} prints-path={'yes' if f'-pidfile {pid}' in out else 'no'}"
    ok = rc == 0 and f"-pidfile {pid}" in out
elif CASE == "same-paths":
    same = os.path.join(W, "both.sock")
    rc, out, err = qemu_args("--pidfile", os.path.join(W, "p.pid"), "--monitor", same, "--serial", same)
    both = out.count(same) >= 2
    facts = f"rc={rc} both-in-command={'yes' if both else 'no'}"
    ok = (rc == 0 and both) if SIDE == "unfixed" else (rc != 0 and not both)
    if err.strip():
        print("  | " + err.strip().splitlines()[-1])
elif CASE in ("socket-swap", "socket-dead"):
    mod = load_launcher()
    mon = os.path.join(W, "mon.sock")
    dead = listener(mon)
    dead.close()  # the file stays; nobody listens: a previous QEMU's socket
    live = []
    if CASE == "socket-swap":
        real = mod.stale_socket

        def swapping(path):
            verdict = real(path)
            if str(path) == mon and verdict:
                os.unlink(mon)
                live.append(listener(mon))  # a second launcher's live socket, bound in the window
            return verdict

        mod.stale_socket = swapping
    err = ""
    try:
        mod.prepare_run(mod.load_profile(), run_args(mon))
        raised = False
    except ValueError as e:
        raised, err = True, str(e)
    present = os.path.exists(mon)
    live_ok = answers(mon) if live else False
    facts = f"raised={'yes' if raised else 'no'} path-present={'yes' if present else 'no'} live-answers={'yes' if live_ok else 'no'}"
    if err:
        print("  | " + err)
    if CASE == "socket-swap":
        ok = (not raised and not present) if SIDE == "unfixed" else (raised and present and live_ok)
    else:
        ok = not raised and not present
    for s in live:
        s.close()
elif CASE in ("socket-symlink", "socket-notsock", "socket-live"):
    mod = load_launcher()
    mon = os.path.join(W, "mon.sock")
    held = []
    if CASE == "socket-symlink":
        target = os.path.join(W, "precious.txt")
        with open(target, "w") as f:
            f.write("keep\n")
        os.symlink(target, mon)
    elif CASE == "socket-notsock":
        with open(mon, "w") as f:
            f.write("a disk image given as --monitor\n")
    else:
        held.append(listener(mon))
    err = ""
    try:
        mod.prepare_run(mod.load_profile(), run_args(mon))
        raised = False
    except ValueError as e:
        raised, err = True, str(e)
    present = os.path.lexists(mon)
    facts = f"raised={'yes' if raised else 'no'} path-present={'yes' if present else 'no'}"
    if err:
        print("  | " + err)
    ok = raised and present
    for s in held:
        s.close()
else:
    print(f"launcher-case: CANNOT -- unknown case {CASE}")
    sys.exit(2)
after = qemu_count()
facts += f" qemu-before={before} qemu-after={after}"
if after > before:
    ok = False
print(f"launcher-case {CASE}: {SIDE}-expectation-met ({facts})" if ok else f"launcher-case {CASE}: UNEXPECTED on {SIDE} ({facts})")
sys.exit(0 if ok else 1)

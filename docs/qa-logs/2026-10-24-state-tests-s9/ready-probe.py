"""ready-probe.py -- T14 S9's harness for #1000: run a gate's own
first_boot_ready() with systemctl answered by a stand-in (one loaded
rocknix-autostart.service whose ExecStart is given, autostart.service not
found), and report which of the gate's checks refused first, by its source
line. Nothing else is stubbed: the host's boot id, uptime and mounts are read
as they are, so a gate that accepts the ExecStart refuses later, at the
/storage mounts this host lacks.
    python3 -I ready-probe.py <gate> <path> <argv joined>
"""
import subprocess, sys
from importlib.machinery import SourceFileLoader
gate = SourceFileLoader("gate", sys.argv[1]).load_module()
path, argv = sys.argv[2], sys.argv[3]
execstart = ("{ path=%s ; argv[]=%s ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; "
             "pid=0 ; code=exited ; status=0 }" % (path, argv))
def run(cmd, **kw):
    name = cmd[-1]
    if name == "autostart.service":
        out = "Id=autostart.service\nLoadState=not-found\n"
    else:
        out = "\n".join(["Id=" + name, "LoadState=loaded", "Type=oneshot", "ActiveState=active",
                         "SubState=exited", "Result=success", "ExecMainCode=1", "ExecMainStatus=0",
                         "ExecMainStartTimestampMonotonic=1", "ExecMainExitTimestampMonotonic=2",
                         "ConditionResult=yes", "ExecStart=" + execstart]) + "\n"
    return subprocess.CompletedProcess(cmd, 0, out.encode(), b"")
gate.subprocess.run = run
lines = open(sys.argv[1]).read().splitlines()
first = []
real = gate.require
def recording(ok):
    if not ok and not first:
        first.append(lines[sys._getframe(1).f_lineno - 1].strip())
    real(ok)
gate.require = recording
try:
    gate.first_boot_ready()
    print("READY")
except gate.Invalid:
    print("REFUSED AT " + first[0])

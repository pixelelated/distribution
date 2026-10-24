#!/usr/bin/env python3
"""sandbox-case.py -- T14 S2's control (#992, #999): what reaches a script
inside the real-rclone tests' sandbox, and what the connections fixture lets
run. Every input is constructed under a scratch root; no real remote, no real
rclone configuration, and the lane's own HOME is never the one tested.

  python3 -I sandbox-case.py --tools <dir holding the tools> --source-root <tree> --rclone <a copy of rclone> --scratch <dir>

<dir holding the tools> is the worktree (fixed) or an export of the stage-D
tip (unfixed); both are read, never written. Exit 0 when every case holds.
"""
import argparse, importlib.machinery, importlib.util, json, os, shutil, subprocess, sys, types
from pathlib import Path
sys.dont_write_bytecode = True
p = argparse.ArgumentParser()
p.add_argument("--tools", type=Path, required=True)
p.add_argument("--source-root", type=Path, required=True)
p.add_argument("--rclone", type=Path, required=True)
p.add_argument("--scratch", type=Path, required=True)
a = p.parse_args()
S = a.scratch.resolve()
if S.exists():
    shutil.rmtree(S)
S.mkdir(parents=True)
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("  ok    " if ok else "  FAIL  ") + name + (f"  [{detail}]" if detail and not ok else ""), flush=True)
    fails += 0 if ok else 1
def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader); m = importlib.util.module_from_spec(spec); loader.exec_module(m); return m

# The caller's environment, constructed: what a careless caller could export.
tmpdir = S / "caller-tmp"; tmpdir.mkdir()
witness = {
    "TMPDIR": str(tmpdir),                                   # a host path the sandbox does not mount
    "RCLONE_CONFIG": "/etc/t14-stand-in-absent.conf",        # a configuration path, stand-in, absent
    "RCLONE_CONFIG_QA_TYPE": "local",                        # an environment-defined remote
    "BASH_ENV": "/shim/logger",                              # a file every sandboxed bash would source
    "BASH_FUNC_t14probefn%%": "() { echo exported-function-ran; }",
}
saved = {k: os.environ.get(k) for k in witness}
os.environ.update(witness)

# Part A: a probe script run through Fixture.run, the sandbox the four share.
lay = load("t14_layout", a.tools / "rasteratops-cloud-layout-test")
args = types.SimpleNamespace(ref=None, source_root=a.source_root, rclone=str(a.rclone))
f = lay.Fixture(S / "probe", args)
lay.put(f.path / "repo/t14probe", "#!/bin/bash\n"
        "for v in RCLONE_CONFIG RCLONE_CONFIG_QA_TYPE BASH_ENV; do [ -n \"${!v+x}\" ] && echo \"ENV $v\"; done\n"
        "echo \"TMPDIRVAL ${TMPDIR-}\"\n"
        "type t14probefn >/dev/null 2>&1 && echo FUNC t14probefn\n"
        "t=$(mktemp 2>/dev/null) && echo MKTEMP-OK || echo MKTEMP-FAIL\n"
        "echo NETDEV $(($(wc -l < /proc/net/dev) - 2))\n", )
(f.path / "repo/t14probe").chmod(0o755)
r = f.run("t14probe")
out = r.stdout
leaked = [l.split()[1] for l in out.splitlines() if l.startswith("ENV ")]
inner_tmp = next((l.split(" ", 1)[1] if " " in l else "" for l in out.splitlines() if l.startswith("TMPDIRVAL")), None)
if inner_tmp == str(tmpdir): leaked.append("TMPDIR")      # the sandbox's own TMPDIR=/tmp is not the caller's
net = next((int(l.split()[1]) for l in out.splitlines() if l.startswith("NETDEV ")), None)
journal = (f.path / "ctl/journal").read_text() if (f.path / "ctl/journal").exists() else ""
print(f"  probe: leaked={leaked} func={'FUNC' in out} mktemp={'MKTEMP-OK' in out} netdev={net} journal_lines={len(journal.splitlines())}")
check("no caller variable reaches a sandboxed script (TMPDIR, RCLONE_CONFIG, RCLONE_CONFIG_QA_TYPE, BASH_ENV)", not leaked, ",".join(leaked))
check("no exported shell function reaches a sandboxed script", "FUNC t14probefn" not in out)
check("BASH_ENV is not sourced (the logger shim wrote nothing before the script)", journal == "", repr(journal[:40]))
check("mktemp works inside the sandbox with the caller's TMPDIR exported", "MKTEMP-OK" in out)
check("the sandbox has no network interface but loopback (local backends only)", net == 1, f"netdev={net}")

# Part B: the archive cases the caller's TMPDIR used to break, the whole test as T15 calls it.
o = S / "layout"
rb = subprocess.run([sys.executable, "-I", str(a.tools / "rasteratops-cloud-layout-test"), "--source-root", str(a.source_root),
                     "--rclone", str(a.rclone), "--output", str(o), "--archives-only"], capture_output=True, text=True, timeout=900)
last = (rb.stdout.strip().splitlines() or [""])[-1]
print("  layout --archives-only: rc %d | %s" % (rb.returncode, last[:90]))
check("rasteratops-cloud-layout-test --archives-only passes with the caller's TMPDIR, RCLONE_CONFIG and BASH_ENV exported", rb.returncode == 0 and "0 FAIL" in last, last[:80])

for k, v in saved.items():
    if v is None: os.environ.pop(k, None)
    else: os.environ[k] = v

# Part C: the connections fixture's guard, on a stand-in HOME.
home = S / "standin-home"; (home / ".config/rclone").mkdir(parents=True)
default_conf = home / ".config/rclone/rclone.conf"
os.environ["HOME"] = str(home); os.environ.pop("XDG_CONFIG_HOME", None); os.environ.pop("RCLONE_CONFIG", None)
sys.path.insert(0, str(a.tools / "test-fixtures"))
fx = load("t14_conn_fixture", a.tools / "test-fixtures/cloud_connections_fixture.py")
def module_with(rclone_path, sp):
    class Refused(Exception): pass
    conn = types.SimpleNamespace(Refused=Refused)
    return types.SimpleNamespace(connections=conn, subprocess=sp, RCLONE=str(rclone_path))
copied = S / "elsewhere/rclone"; copied.parent.mkdir(); shutil.copy2(a.rclone, copied)
d = S / "conn"; d.mkdir()
m = module_with(copied, subprocess); fx.configure(m, d)
stage = d / "staged.conf"; stage.write_text("")
before = default_conf.exists()
try:
    m.connections.run(["--config", str(stage), "config", "create", "t14qa", "alias", "remote", str(S / "nowhere")])
    admitted = True
except Exception as e:
    admitted = False; why = str(e)
print(f"  guard: real rclone at another path admitted={admitted}; default config written={default_conf.exists() and not before}; stage has t14qa={'t14qa' in stage.read_text()}")
check("a real rclone copied to another path is refused by the fixture", not admitted)
check("the stand-in HOME's default rclone configuration is never written", not default_conf.exists())
# the fixture's own shape still works: a script shim in the fixture's directory, real subprocess, --config kept
shim = d / "rclone"; shim.write_text('#!/bin/bash\nprintf "%s\\n" "$@" > "$(dirname "$0")/argv"\n'); shim.chmod(0o755)
m2 = module_with(shim, subprocess); fx.configure(m2, d)
try:
    m2.connections.run(["--config", str(stage), "listremotes"]); ok2 = True
except Exception:
    ok2 = False
argv = (d / "argv").read_text().split() if (d / "argv").exists() else []
check("a shim in the fixture's own directory still runs, and receives the stage's --config", ok2 and argv[:2] == ["--config", str(stage)], " ".join(argv))
# and T15's table-answered fake: the argv shape its prefixes match is unchanged
class Fake:
    def __init__(self): self.calls = []
    def run(self, args, **kw):
        self.calls.append(list(args)); return subprocess.CompletedProcess(args, 0, "", "")
fk = Fake(); m3 = module_with("/usr/bin/rclone", fk); fx.configure(m3, d)
m3.connections.run(["--config", str(stage), "listremotes"])
check("a table fake (T15's FakeSP shape) still sees [rclone, <command>...] at argv[1:]", fk.calls and fk.calls[0][1:] == ["listremotes"], str(fk.calls[:1]))
print("PASS" if fails == 0 else f"FAIL ({fails})")
sys.exit(1 if fails else 0)

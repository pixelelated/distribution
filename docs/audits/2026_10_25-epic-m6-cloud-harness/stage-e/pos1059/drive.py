#!/usr/bin/env python3
"""#1059: the verdict line and what is refused. (1) The CLI with --only
NO-SUCH-CELL against a dead port (port 1): is the unknown cell named, rc 2?
(2) prepare_device on a stub with ssh and no cloud scripts: does the failed
equipment check stop the setup? (3) the last line after one PASS and one
SKIP, and a run that checked nothing: its line and its exit (main()'s return,
evaluated from the AST). The backend state is a missing directory under
$TMPDIR on port 9080; nothing listens.
    python3 -I -B pos1059/drive.py <cloud-round-trip> unfixed|fixed"""
import ast, contextlib, io, os, subprocess, sys, types
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, scratch, verdict

tool, expect = args()
env = dict(os.environ, CLOUD_QA_STATE=os.path.join(scratch("pos1059"), "state"), CLOUD_QA_PORT="9080")
p = subprocess.run([sys.executable, tool, "--only", "NO-SUCH-CELL", "--host", "root@127.0.0.1", "--port", "1",
                    "--identity", "/nonexistent"], capture_output=True, text=True, env=env, timeout=120)
named = "NO-SUCH-CELL" in (p.stdout + p.stderr)
print(f"(1) --only NO-SUCH-CELL: rc {p.returncode}; the cell named: {named}")
crt = load(tool)
real_backend = crt.backend
crt.backend = lambda *a, **k: ""
class Dev:
    host, port = "stub", 0
    def run(self, cmd, check=True): return "ok\n" if cmd.strip() == "echo ok" else ""
    def write(self, path, data): pass
    def sha(self, path): return None
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        crt.prepare_device(Dev(), "qa-cloud", "/storage/cloud-qa", types.SimpleNamespace(real_roms=False, path_prefix=None), [])
except Exception:
    pass
went_on = "point the device at the QA bucket" in buf.getvalue()
print(f"(2) the equipment FAIL printed: {'device is missing rclone' in buf.getvalue()}; setup went on: {went_on}")
crt.backend = real_backend
os.environ["CLOUD_QA_STATE"] = env["CLOUD_QA_STATE"]
if hasattr(crt, "verdict_line"):
    crt.CHECKS.update(passed=0, failed=0); crt.SKIPPED.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        crt.check(True, "one check", ""); crt.skip("one cell could not run")
    line = crt.verdict_line(0)
    crt.CHECKS.update(passed=0, failed=0); crt.SKIPPED.clear()
    nothing = crt.verdict_line(0)
else:
    tree = ast.parse(open(tool).read())
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print"
                and "PASSED" in ast.unparse(n) and "CHECK(S) FAILED" in ast.unparse(n))
    line = eval(compile(ast.Expression(node.args[0]), tool, "eval"), {"failures": 0, "note": " (one cell could not run)"}).strip()
    nothing = line
tree = ast.parse(open(tool).read())
main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
ret = [n for n in ast.walk(main) if isinstance(n, ast.Return) and n.value is not None and "failures" in ast.unparse(n)][-1]
code = eval(compile(ast.Expression(ret.value), tool, "eval"), {"failures": 0, "line": nothing})
print(f"(3) last line: {line}")
print(f"    nothing checked: {nothing} -> exit {code}")
counts = "passed," in line and "skipped" in line and "backend" in line
observed = ("unfixed" if not named and went_on and not counts else
            "fixed" if named and p.returncode == 2 and not went_on and counts and nothing.startswith("NOTHING CHECKED") and code == 3 else "neither")
verdict("pos1059", expect, observed, f"unknown cell named {named} (rc {p.returncode}); setup went on {went_on}; counts on the line {counts}; nothing-checked exit {code}")

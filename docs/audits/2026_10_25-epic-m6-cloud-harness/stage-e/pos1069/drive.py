#!/usr/bin/env python3
"""#1069: A15's upload fixture (the dev.write(... upload ...) argument, from
the AST, evaluated in the tool's namespace) written under $TMPDIR and listed
with tar -tzf, the check cloud_backup applies before sending.
    python3 -I -B pos1069/drive.py <cloud-round-trip> unfixed|fixed"""
import ast, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, scratch, verdict

tool, expect = args()
tree = ast.parse(open(tool).read())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "fx_a15")
call = next(n for n in ast.walk(fn) if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "write"
            and "upload" in ast.unparse(n.args[0]))
data = eval(compile(ast.Expression(call.args[1]), tool, "eval"), vars(load(tool)))
out = os.path.join(scratch("pos1069"), "a15-upload.tar.gz")
open(out, "wb").write(data)
r = subprocess.run(["tar", "-tzf", out], capture_output=True, text=True)
said = (r.stdout or r.stderr).strip().splitlines()
print(f"A15's upload fixture: {ast.unparse(call.args[1])} -> {len(data)} bytes; tar -tzf rc={r.returncode}: {said[0] if said else ''}")
observed = "fixed" if r.returncode == 0 else "unfixed"
verdict("pos1069", expect, observed, f"tar -tzf rc {r.returncode}")

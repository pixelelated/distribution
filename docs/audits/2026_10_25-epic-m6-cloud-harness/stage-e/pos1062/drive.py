#!/usr/bin/env python3
"""#1062: KILL1. (1) The names fx_kill1 reads that neither it, its
parameters, module scope nor the builtins assign. (2) Its preservation
predicate over a cloud listing with one file gone (unfixed: the inline
`torn = {...}` from the AST; fixed: kill1_bad()).
    python3 -I -B pos1062/drive.py <cloud-round-trip> unfixed|fixed"""
import ast, builtins, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, verdict

tool, expect = args()
tree = ast.parse(open(tool).read())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "fx_kill1")
# module scope only: a name assigned inside another function (Link.exercise's
# and fx_kill5's own `webdav`) is not visible in fx_kill1
top = [n for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.For, ast.With, ast.If, ast.Try))]
module = {t.id for n in top for t in ast.walk(n) if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store)
          and not any(isinstance(f, (ast.FunctionDef, ast.ClassDef)) for f in ast.walk(n))} \
    | {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))} \
    | {a.asname or a.name.split(".")[0] for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names}
local = {t.id for t in ast.walk(fn) if isinstance(t, ast.Name) and isinstance(t.ctx, (ast.Store, ast.Del))} \
    | {a.arg for a in fn.args.args} \
    | {t.name for t in ast.walk(fn) if isinstance(t, (ast.FunctionDef, ast.ExceptHandler)) and getattr(t, "name", None)} \
    | {a.arg for t in ast.walk(fn) if isinstance(t, ast.Lambda) for a in t.args.args} \
    | {g.id for t in ast.walk(fn) if isinstance(t, ast.comprehension) for g in ast.walk(t.target) if isinstance(g, ast.Name)}
loads = {t.id for t in ast.walk(fn) if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Load)}
unbound = sorted(loads - local - module - set(dir(builtins)))
print("names fx_kill1 reads and nothing assigns:", unbound or "none")
states = {"saves/a.state": "absent", "saves/b.state": "v1", "saves/c.state": "v2"}
crt = load(tool)
if hasattr(crt, "kill1_bad"):
    bad = crt.kill1_bad(states)
else:
    node = next(n for n in ast.walk(fn) if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "torn")
    bad = eval(compile(ast.Expression(node.value), tool, "eval"), {"states": states})
print("one file absent from the cloud -> the predicate fails:", bad or "none")
observed = ("unfixed" if unbound == ["webdav"] and not bad else "fixed" if not unbound and "saves/a.state" in bad else "neither")
verdict("pos1062", expect, observed, f"unassigned {unbound or 'none'}; absent file {'fails' if bad else 'passes'}")

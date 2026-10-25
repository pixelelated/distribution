#!/usr/bin/env python3
"""#1063: CONTRACT's dry-run guard over a copy-arm dry run that found no
conflict (the banner still says `conflicts []`) and over one that found one
(unfixed: the `guard = ...` expression from the AST; fixed: contract_guard()).
    python3 -I -B pos1063/drive.py <cloud-round-trip> unfixed|fixed"""
import ast, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, verdict

tool, expect = args()
clean = {"rc": 0, "out": "dry-run: push ['saves/x.srm'] fetch [] conflicts [] questions []", "conflicts": []}
one = {"rc": 0, "out": "dry-run: push [] fetch [] conflicts ['saves/Contract Both.srm'] questions []", "conflicts": ["saves/Contract Both.srm"]}
crt = load(tool)
if hasattr(crt, "contract_guard"):
    g = crt.contract_guard
else:
    tree = ast.parse(open(tool).read())
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "guard"
                and "conflict" in ast.unparse(n.value))
    expr = compile(ast.Expression(node.value), tool, "eval")
    g = lambda dry: eval(expr, {"dry": dry})
fc, fo = bool(g(clean)), bool(g(one))
print(f"no conflict found: the guard {'FIRES' if fc else 'does not fire'}; one conflict: {'FIRES' if fo else 'does not fire'}")
observed = "unfixed" if fc and fo else "fixed" if (not fc and fo) else "neither"
verdict("pos1063", expect, observed, f"clean {'fires' if fc else 'quiet'}, conflict {'fires' if fo else 'quiet'}")

#!/usr/bin/env python3
"""rules-check.py -- tools/rules-check's control (T10 S9, #948): the tool's two
readers, imported and fed constructed text; nothing in the tree is read.
  python3 -I rules-check.py [rules-check]"""
import importlib.machinery, importlib.util, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../../tools/rules-check"))
loader = importlib.machinery.SourceFileLoader("rules_check", TOOL)
spec = importlib.util.spec_from_loader("rules_check", loader); mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
fails = 0
def check(name, cond):
    global fails
    print(("  ok    " if cond else "  FAIL  ") + name); fails += 0 if cond else 1
nw = getattr(mod, "names_word", None)
check("a rule's name inside a path is no mention: worktrees in ../rocknix.worktrees/", nw is not None and not nw("git worktree add ../rocknix.worktrees/x", "worktrees"))
check("a rule's name as a word is a mention", nw is not None and nw("| `worktrees` | the layout |", "worktrees") and nw("see worktrees.md", "worktrees"))
gaps = getattr(mod, "detail_in_gaps", None)
index = """## The fork's own tools

| Tool | What it answers | Detail in |
| --- | --- | --- |
| `alpha` | a | `one.md` |
| `beta`, `beta-test` | b | `one.md` |

**When a rule earns its place**
"""
rules = {"one.md": "This rule runs `tools/alpha` and `tools/beta`."}
got = gaps(index, lambda r: rules.get(r, "")) if gaps else None
check("an index row whose Detail-in rule never names the tool is reported: beta-test -> one.md (got %s)" % got, got == [("beta-test", "one.md")])
print("PASS" if fails == 0 else "FAIL"); sys.exit(1 if fails else 0)

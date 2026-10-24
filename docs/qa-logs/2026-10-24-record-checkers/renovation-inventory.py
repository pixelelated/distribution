#!/usr/bin/env python3
"""renovation-inventory.py -- tools/renovation-inventory's write and staged-path
cases (T10 S9, #957). The tool imported; its git reader run on a throwaway
repository under .qa-scratch/ holding a staged rm and a staged add (equal
counts, different sets); its main run with `build` replaced by a stub that
returns counts which disagree, over a scratch distribution whose inventory.json
is hashed before and after. The stub stands in for a full run, which needs the
container planner (tools/viewplan per device); the decision under test, write
or not, is the same code either way. Nothing in the tree is read or written.
  python3 -I renovation-inventory.py [renovation-inventory] [scratch-parent]"""
import hashlib, importlib.machinery, importlib.util, io, os, shutil, subprocess, sys, tempfile, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOOL = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tools/renovation-inventory"))
PARENT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, ".qa-scratch"))
loader = importlib.machinery.SourceFileLoader("renovation_inventory", TOOL)
spec = importlib.util.spec_from_loader("renovation_inventory", loader); mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
fails = 0
def check(name, cond):
    global fails
    print(("  ok    " if cond else "  FAIL  ") + name); fails += 0 if cond else 1
os.makedirs(PARENT, exist_ok=True)
S = tempfile.mkdtemp(prefix="renovation-inventory.", dir=PARENT)
try:
    # 1. a staged rm plus a staged add: the counts agree, the sets do not
    repo = os.path.join(S, "repo")
    G = lambda *a: subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.hooksPath=/dev/null", *a],
                                  check=True, capture_output=True)
    subprocess.run(["git", "init", "-q", "-b", "main", repo], check=True)
    for n in ("a.txt", "b.txt"):
        open(os.path.join(repo, n), "w").write(n + "\n")
    G("add", "-A"); G("commit", "-q", "-m", "base")
    G("rm", "-q", "--cached", "b.txt"); open(os.path.join(repo, "c.txt"), "w").write("c\n"); G("add", "c.txt")
    head, index = mod.tracked(repo)
    n_index = index if isinstance(index, int) else len(index)
    differs = getattr(mod, "index_differs", None)
    got = differs(head, index) if differs else None
    check("a staged rm and add leave the counts equal (%d and %d)" % (len(head), n_index), len(head) == n_index == 2)
    check("and the sets apart: index_differs names b.txt and c.txt (got %s)" % got, got == ["b.txt", "c.txt"])

    # 2. a run whose counts disagree writes nothing
    dist = os.path.join(S, "dist"); os.makedirs(os.path.join(dist, "docs/reviews")); os.makedirs(os.path.join(dist, ".githooks"))
    open(os.path.join(dist, ".githooks/secret-patterns"), "w").write("SECRET_PATTERNS='%s'\n" % ("STANDIN" + "_NEVER_" + "[0-9]{64}"))
    inv = os.path.join(dist, "docs/reviews/inventory.json")
    open(inv, "w").write('{"constructed": "the inventory before the run"}\n')
    before = hashlib.sha256(open(inv, "rb").read()).hexdigest()
    counts = {"paths": (5, 4), "es-paths": (3, 3), "patches": (0, 0), "unassigned": 0, "ambiguous": 0,
              "paths-differ": ["staged.txt"], "es-paths-differ": []}
    header = {"seconds": {"git": 0.0, "plans": 0.0}}
    mod.build = lambda args: (header, [], counts, [], [])
    argv = sys.argv
    sys.argv = ["renovation-inventory", "--distribution", dist]
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            rc = mod.main()
    except Exception as e:   # the unfixed tool writes, then may trip over the stub's thin header
        rc = "raised %s" % type(e).__name__
    finally:
        sys.argv = argv
    after = hashlib.sha256(open(inv, "rb").read()).hexdigest()
    print("        inventory.json sha256 before %s" % before)
    print("        inventory.json sha256 after  %s" % after)
    check("a run whose counts disagree exits 1 (rc %s)" % rc, rc == 1)
    check("and leaves inventory.json byte-identical", before == after)
    check("and no inventory.md is written", not os.path.exists(os.path.join(dist, "docs/reviews/inventory.md")))
finally:
    shutil.rmtree(S)
print("PASS" if fails == 0 else "FAIL"); sys.exit(1 if fails else 0)

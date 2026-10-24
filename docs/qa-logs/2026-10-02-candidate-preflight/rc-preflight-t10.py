#!/usr/bin/env python3
"""rc-preflight-t10.py -- tools/rc-preflight's acceptance and bug-trace cases
(T10 S9, #956): the tool imported, its `run` replaced by a stub tracker, its
acceptance file and register pointed at constructed files in a throwaway
directory. Nothing in the tree or on the tracker is read.
  python3 -I rc-preflight-t10.py [rc-preflight]"""
import importlib.machinery, importlib.util, io, json, os, re, sys, tempfile, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../../tools/rc-preflight"))
loader = importlib.machinery.SourceFileLoader("rc_preflight", TOOL)
spec = importlib.util.spec_from_loader("rc_preflight", loader); mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
fails = 0
def check(name, cond):
    global fails
    print(("  ok    " if cond else "  FAIL  ") + name); fails += 0 if cond else 1

tmp = tempfile.mkdtemp(prefix="rc-preflight-t10.")
reg = os.path.join(tmp, "register.md"); acc_file = os.path.join(tmp, "rc-accept.txt")
open(reg, "w").write("| ID | Date | Decision |\n| --- | --- | --- |\n| D-TEST-1 | 2026-10-24 | **the zip pin stands** |\n\n## Open decisions\n")
open(acc_file, "w").write("package zip D-TEST-1 -- a known kind\nfrob zip D-TEST-1 -- a kind the tool has no item for\nbase nowhere D-TEST-1 -- a base that is not one of the two\nbug #5 D-TEST-1 -- an accepted bug\n")
mod.REGISTER, mod.ACCEPT = reg, acc_file

def rows_of(fn, *args):
    r = mod.Report()
    with contextlib.redirect_stdout(io.StringIO()):
        out = fn(r, *args)
    return r.rows, out

# 1. the acceptance line's kind and item
ids = mod.decided_ids()
cka = getattr(mod, "check_acceptances", None)
if cka:
    rows, acc = rows_of(cka, ids)
else:
    acc, bad = mod.acceptances(ids); rows = [("NOTE", "rc-accept.txt", b) for b in bad]
f = [x for x in rows if x[0] == "FAIL" and x[1] == "rc-accept.txt"]
check("an acceptance line of an unknown kind is a named finding (FAIL rc-accept.txt ... frob)", any("frob" in x[2] for x in f))
check("a base acceptance naming neither base is a named finding", any("nowhere" in x[2] for x in f))
check("a known kind still accepts: package zip", acc.get(("package", "zip")) == "D-TEST-1")

# 2 and 3. a stub tracker
def make_run(comments, total=None):
    def run(cmd, cwd=None, timeout=600):
        if cmd[:3] == ["gh", "issue", "list"]:
            limit = int(cmd[cmd.index("--limit") + 1]); state = cmd[cmd.index("--state") + 1]
            if total is not None:
                return 0, json.dumps([{"number": 1000 + i, "title": "t", "closedAt": "2026-10-01T00:00:00Z", "stateReason": "COMPLETED"} for i in range(limit)]), ""
            return 0, json.dumps([{"number": 5, "title": "t"}] if state == "open" else []), ""
        if cmd[:2] == ["gh", "api"]:
            if cmd[-3].endswith("/comments") or (len(cmd) > 3 and cmd[3].endswith("/comments")):
                return 0, comments, ""
            return 0, "", ""
        return 1, "", "unexpected command"
    return run

def verdict(rows, item):
    return [x[0] for x in rows if x[1] == item]

hollow = "## Code trace\n\nAlready written:\n"
mod.run = make_run(hollow)
acc_bug = {("bug", "5"): "D-TEST-1"}
rows, _ = rows_of(mod.check_bugs, acc_bug)
check("an accepted bug whose trace is only a heading fails bugs (got %s)" % verdict(rows, "bugs"), verdict(rows, "bugs") == ["FAIL"])
rows, _ = rows_of(mod.check_already_written)
check("the same bug's empty Already written: line fails already written (got %s)" % verdict(rows, "already written"), verdict(rows, "already written") == ["FAIL"])

full = "## Code trace\n\n**How it was found:** a constructed case.\n\n**Already written:** nothing inherited: the old code wrote nothing.\n"
mod.run = make_run(full)
rows, _ = rows_of(mod.check_bugs, acc_bug)
check("a trace with content passes bugs (got %s)" % verdict(rows, "bugs"), verdict(rows, "bugs") == ["PASS"])
rows, _ = rows_of(mod.check_already_written)
check("and passes already written (got %s)" % verdict(rows, "already written"), verdict(rows, "already written") == ["PASS"])

inline = "**Code trace** (for the candidate). Found writing the walks; at source the focus stop.\n\nAlready written: nothing inherited -- no state.\n"
mod.run = make_run(inline)
rows, _ = rows_of(mod.check_bugs, acc_bug)
check("a trace written on its heading's own line passes bugs (got %s)" % verdict(rows, "bugs"), verdict(rows, "bugs") == ["PASS"])

mod.run = make_run(full, total=True)
rows, _ = rows_of(mod.check_bugs, {})
check("a tracker answer of exactly the limit makes bugs CANNOT (got %s)" % verdict(rows, "bugs"), verdict(rows, "bugs") == ["CANNOT"])
rows, _ = rows_of(mod.check_already_written)
check("and already written CANNOT (got %s)" % verdict(rows, "already written"), verdict(rows, "already written")[:1] == ["CANNOT"])

for p in (reg, acc_file): os.remove(p)
os.rmdir(tmp)
print("PASS" if fails == 0 else "FAIL"); sys.exit(1 if fails else 0)

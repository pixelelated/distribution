#!/usr/bin/env python3
"""run.py -- tools/ceremony-check's tracker and marker control (T10 S5, #943).
Never reads GitHub: the tracker is ../2026-10-24-box-check/gh-double, first on
PATH, serving a constructed population; the marker cases build an audit
folder in a throwaway root under .qa-scratch/.
  python3 -I run.py [ceremony-check] [scratch-parent]
Each case prints ok or FAIL; the run ends PASS (exit 0) or FAIL (1)."""
import datetime as dt, hashlib, importlib.machinery, importlib.util, json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOOL = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tools/ceremony-check"))
PARENT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, ".qa-scratch")
os.makedirs(PARENT, exist_ok=True)
S = tempfile.mkdtemp(prefix="ceremony-check-control.", dir=PARENT)
fails = 0
def check(name, cond):
    global fails
    print(("  ok    " if cond else "  FAIL  ") + name)
    fails += 0 if cond else 1

loader = importlib.machinery.SourceFileLoader("ceremony_check", TOOL)
spec = importlib.util.spec_from_loader("ceremony_check", loader); mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)

print("--- the completion marker's receipt")
root = os.path.join(S, "root"); a = os.path.join(root, "docs/audits/2026_10_01-epic-x"); os.makedirs(a)
def build(body="- [x] PL-01 resolved", exact=True):
    for n, t in (("04-analysis.md", "analysis\n"), ("05-punch-list.md", "punch\n")):
        open(os.path.join(a, n), "w").write(t)
    rb = os.path.join(a, "tracker-final-readback.json"); json.dump({"number": 9, "state": "closed", "state_reason": "completed", "body": body}, open(rb, "w"))
    tc = os.path.join(a, "tracker-completion.json"); json.dump({"result": "PASS", "exact_bodies_and_states": exact, "closed_completed": [9], "verified_utc": "2026-10-01T00:00:00+00:00"}, open(tc, "w"))
    rel = lambda p: os.path.relpath(p, root)
    ev = {rel(os.path.join(a, n)): hashlib.sha256(open(os.path.join(a, n), "rb").read()).hexdigest() for n in ("04-analysis.md", "05-punch-list.md", "tracker-final-readback.json", "tracker-completion.json")}
    m = os.path.join(a, "audit-completion.json")
    json.dump({"schema": 1, "issue": 9, "completed_at": "2026-10-01T00:00:00+00:00", "tracker_readback": rel(rb), "tracker_completion": rel(tc), "evidence": ev}, open(m, "w"))
    return m
def accepted(m):
    try:
        mod.completed_audit_marker(m, root, dt.datetime(2026, 10, 24, tzinfo=dt.timezone.utc)); return True
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return False
check("a valid receipt is accepted", accepted(build()))
check("a receipt whose exact_bodies_and_states is the string \"false\" is refused", not accepted(build(exact="false")))
check("a readback body with an unticked '* [ ]' checkbox is refused", not accepted(build(body="- [x] PL-01 resolved\n* [ ] PL-02 open")))
p = os.path.join(a, "04-analysis.md")
check("the streamed digest equals hashlib.sha256 over the bytes (the 18:18 hunk)", getattr(mod, "file_sha256", lambda _p: None)(p) == hashlib.sha256(open(p, "rb").read()).hexdigest())

print("--- the clocks reset only on a marker")
mod.ROOT = root
os.makedirs(os.path.join(root, "docs/futros"), exist_ok=True); open(os.path.join(root, "docs/futros/2099-01-01-x.md"), "w").write("x\n")
futro_rx = getattr(mod, "FUTRO_MARKER", r"\bfutro\b")
try:
    got = mod.last_marker({}, futro_rx, "futros", dt.date(2026, 10, 24))
except TypeError:
    got = mod.last_marker({}, futro_rx, "futros")
check("a futro file dated 2099 does not set the clock (got %s)" % got, got is None)
days = {dt.date(2026, 10, 20): [("10:00", "skipped the futro for #900")], dt.date(2026, 10, 21): [("11:00", "futro for #901: the five questions")]}
os.remove(os.path.join(root, "docs/futros/2099-01-01-x.md"))
try:
    got = mod.last_marker(days, futro_rx, "futros", dt.date(2026, 10, 24))
except TypeError:
    got = mod.last_marker(days, futro_rx, "futros")
check("a heading that mentions a futro is not one; a heading that is one sets the clock (got %s)" % got, got == dt.date(2026, 10, 21))
days = {dt.date(2026, 10, 20): [("10:00", "skipped the futro for #900")]}
try:
    got = mod.last_marker(days, futro_rx, "futros", dt.date(2026, 10, 24))
except TypeError:
    got = mod.last_marker(days, futro_rx, "futros")
check("only a mention: no clock (got %s)" % got, got is None)

print("--- the tracker, through the gh double")
bin_ = os.path.join(S, "bin"); os.makedirs(bin_); shutil.copy(os.path.join(HERE, "../2026-10-24-box-check/gh-double"), os.path.join(bin_, "gh")); os.chmod(os.path.join(bin_, "gh"), 0o755)
pop = [{"number": 2000 - i, "title": "issue %d" % i, "state": "CLOSED", "labels": [], "createdAt": "2026-09-01T00:00:00Z",
        "closedAt": "2026-09-01T00:00:00Z", "body": "- [x] the guest prints PASS"} for i in range(250)]
pop[230]["body"] = "- [ ] a criterion nobody ticked"
issues = os.path.join(S, "issues.json"); json.dump(pop, open(issues, "w"))
def run(**env):
    e = dict(os.environ, PATH=bin_ + os.pathsep + os.environ["PATH"], GH_DOUBLE_ISSUES=issues, **env)
    r = subprocess.run([sys.executable, TOOL], capture_output=True, text=True, env=e, cwd=ROOT, timeout=300)
    return r.stdout + r.stderr
out = run()
hy = [l for l in out.splitlines() if " hygiene " in l]
check("250 closed issues, an open checkbox at 230: hygiene names #%d (%s)" % (pop[230]["number"], (hy or ["no line"])[0].strip()[:70]), bool(hy) and "DUE" in hy[0] and "#%d" % pop[230]["number"] in hy[0])
out = run(GH_DOUBLE_TOTAL="999")
hy = [l for l in out.splitlines() if " hygiene " in l]
check("the tracker says 999 and the read returns 250: hygiene is DUE as a short read (%s)" % (hy or ["no line"])[0].strip()[:70], bool(hy) and "DUE" in hy[0] and "250 of 999" in hy[0])
out = run(GH_DOUBLE_FAIL="1")
tail = out.split("overdue.", 1)[-1] if "overdue." in out else ""
check("the tracker does not answer: the futro line is counted overdue", "futro:" in tail)
check("the tracker does not answer: the hygiene line is counted overdue", "hygiene:" in tail)

shutil.rmtree(S, ignore_errors=True)
print("PASS" if fails == 0 else "FAIL")
sys.exit(1 if fails else 0)

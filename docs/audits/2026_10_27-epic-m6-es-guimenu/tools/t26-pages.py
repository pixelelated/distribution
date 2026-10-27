#!/usr/bin/env python3
"""T26 (#673): one row per page GuiMenu.cpp builds, at the pin.

    python3 -I t26-pages.py <pin.cpp> [--table] [--dialogs]

Method, stated so the figures can be checked:
- A page is a `new GuiSettings(` construction, a class in this file deriving
  from `GuiSettings` (its body is the page's range), or the main menu
  (`GuiMenu::GuiMenu`). Its title is every `_("...")` literal in the
  construction's title argument (a ternary gives two), else the argument
  as written (`expr:`).
- A page's range is the innermost brace block holding its construction (the
  definition for a page built at a function's top level, a lambda or an if
  block for one built inside); a line belongs to the innermost page range
  holding it, so a page's columns exclude the pages built inside it; code of
  a page-building function outside every page block goes to that
  function's nearest page.
- Runs: a call to a process primitive -- `runSystemCommand(`,
  `GetShOutput(`, `GetShOutputLines(`, `executeScriptLegacy(`, `system(`,
  `popen(` -- outside a helper's body, or to a helper of this file whose
  body makes one, found transitively (a page builder that makes one is an
  opener, listed under Opens, and its own runs are on its own row). Its thread is `worker` when it
  sits in the first lambda of a `GuiLoading` or in a `std::thread`, else
  `interface` (`worker (in the helper)` when the helper's every process
  runs on a worker of its own); its bound is `timeout` when the call's text runs one,
  `timeout (in the helper)` when the helper's every process does, else
  `none`.
- Opens: `new Gui*(` / `new Cloud*(` other than `GuiMsgBox`, `GuiLoading`
  and the page's own construction, and calls to functions of this file that
  build a page.
- Dialogs: each `new GuiMsgBox(` with its button labels in order (a bare
  literal is marked untranslated; an icon argument ends the buttons); the back
  button lands on the only button, else the first named OK or NO, else the
  last (`es-core/src/guis/GuiMsgBox.cpp:116-133` at the pin).
Exits 1 when a figure drifts from the counts asserted below.
"""
import importlib.util, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t26defs", os.path.join(HERE, "t26-defs.py"))
t26defs = importlib.util.module_from_spec(spec); spec.loader.exec_module(t26defs)
EXPECT = {"pages": 60, "titles": 65, "runs": 159, "runs-interface": 131, "dialogs": 108}

path = sys.argv[1]
raw = open(path, encoding="utf-8").read()
blanked = t26defs.blank(raw)
lines_start = [0]
for m in re.finditer("\n", raw):
    lines_start.append(m.end())
import bisect
line_of = lambda off: bisect.bisect_right(lines_start, off)
defs = t26defs.definitions(path)
def_at = lambda ln: next((d for d in defs if d["start"] <= ln <= d["end"]), None)
off_of_line = lambda ln: lines_start[ln - 1]
starts_off = lambda ln: lines_start[ln - 1] if ln - 1 < len(lines_start) else len(raw)

def call_args(op):
    depth = 0; start = op + 1; args = []
    for i in range(op, len(blanked)):
        c = blanked[i]
        if c in "([{": depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                args.append((start, i)); return args, i
        elif c == "," and depth == 1:
            args.append((start, i)); start = i + 1
    raise SystemExit("unbalanced call at line %d" % line_of(op))
argtext = lambda a: re.sub(r"\s+", " ", raw[a[0]:a[1]]).strip()
lits = lambda t: re.findall(r'_\(\s*"((?:[^"\\]|\\.)*)"', t)

# brace blocks, by first-arm counting under conditionals (as t26-defs counts them)
pairs = []; stack = []; cond = []
for ln, (rl, bl) in enumerate(zip(raw.split("\n"), blanked.split("\n")), 1):
    s = rl.strip()
    if s.startswith("#"):
        d = re.match(r"#\s*(\w+)", s); d = d.group(1) if d else ""
        if d in ("if", "ifdef", "ifndef"): cond.append(True)
        elif d in ("elif", "else"):
            if cond: cond[-1] = False
        elif d == "endif" and cond: cond.pop()
        continue
    if not all(cond):
        continue
    base = off_of_line(ln)
    for i, ch in enumerate(bl):
        if ch == "{": stack.append(base + i)
        elif ch == "}" and stack: pairs.append((stack.pop(), base + i))
innermost = lambda off: min((p for p in pairs if p[0] < off < p[1]), key=lambda p: p[1] - p[0], default=None)

# --- pages --------------------------------------------------------------------------
pages = []
for m in re.finditer(r"\bnew GuiSettings\(", blanked):
    args, end = call_args(m.end() - 1)
    t = argtext(args[1]) if len(args) > 1 else ""
    blk = innermost(m.start())
    pages.append({"kind": "GuiSettings", "off": m.start(), "line": line_of(m.start()), "titles": lits(t) or ["expr: " + t[:60]],
                  "range": blk, "def": def_at(line_of(m.start()))})
for m in re.finditer(r"^(class|struct)\s+(\w+)\s*:\s*public\s+GuiSettings\b", blanked, re.M):
    body = blanked.index("{", m.end())
    blk = next(p for p in pairs if p[0] == body)
    base = re.search(r":\s*GuiSettings\(([^;{]*)\)", raw[blk[0]:blk[1]])
    t = base.group(1) if base else ""
    pages.append({"kind": "class " + m.group(2), "off": m.start(), "line": line_of(m.start()),
                  "titles": lits(t) or ["expr: " + re.sub(r"\s+", " ", t)[:60]], "range": blk, "def": None, "name": m.group(2)})
ctor = next(d for d in defs if d["name"] == "GuiMenu::GuiMenu")
pages.append({"kind": "main menu", "off": off_of_line(ctor["start"]), "line": ctor["start"], "titles": ["MAIN MENU"],
              "range": (off_of_line(ctor["start"]), off_of_line(ctor["end"] + 1) - 1), "def": ctor})
pages.sort(key=lambda p: p["off"])
def page_at(off):
    c = [p for p in pages if p["range"] and p["range"][0] <= off <= p["range"][1]]
    if c:
        return min(c, key=lambda p: p["range"][1] - p["range"][0])
    d = def_at(line_of(off))            # code of a page-building function outside its page's block
    same = [p for p in pages if p["def"] is d] if d else []
    return min(same, key=lambda p: abs(p["off"] - off)) if same else None

# --- runners: functions whose body starts a process, transitively ----------------------
PRIM = r"\b(runSystemCommand|GetShOutputLines|GetShOutput|executeScriptLegacy|system|popen)\("
def body_of(d):
    return blanked[off_of_line(d["start"]):off_of_line(d["end"] + 1) - 1]
short = lambda n: n.split("::")[-1]
builders = {short(d["name"]) for d in defs if "new GuiSettings(" in body_of(d) or "new CloudConnectionsPage(" in body_of(d)}
runners = {short(d["name"]) for d in defs if re.search(PRIM, body_of(d))}
while True:
    # through helpers only: a function that opens a page builder is an opener, not a runner
    more = {short(d["name"]) for d in defs if short(d["name"]) not in runners and
            any(re.search(r"(?<![\w:])%s\(" % re.escape(r), body_of(d)) for r in runners - builders)}
    if not more: break
    runners |= more

# worker regions: GuiLoading's first lambda and std::thread bodies
workers = []
for m in re.finditer(r"\bnew GuiLoading<", blanked):
    op = blanked.index("(", m.end()); args, _ = call_args(op)
    for a in args:
        if "[" in blanked[a[0]:a[1]] and "{" in blanked[a[0]:a[1]]:
            workers.append(a); break
for m in re.finditer(r"\bstd::thread\b\s*\(?", blanked):
    op = blanked.find("(", m.start(), m.start() + 40)
    if op > 0:
        args, _ = call_args(op); workers += args
in_worker = lambda off: any(a[0] <= off <= a[1] for a in workers)

runs = []
helpers = runners - builders - {"GuiMenu"}  # a page builder that runs a process is an opener, not a run
helper_defs = [d for d in defs if short(d["name"]) in helpers]
in_helper = lambda off: any(d["start"] <= line_of(off) <= d["end"] for d in helper_defs)
# A helper is bounded when every process it starts -- itself or through another
# helper -- runs under `timeout` (cloudSetupInfo's `timeout 10`, cloudScanStamped's 5).
def _starts(d):
    body0 = starts_off(d["start"]); body1 = starts_off(d["end"] + 1)
    prim, calls, wk = [], [], []
    for m in re.finditer(PRIM, blanked[body0:body1]):
        op = blanked.index("(", body0 + m.start()); _, e = call_args(op)
        prim.append(re.search(r"\btimeout\b", raw[body0 + m.start():e + 1]) is not None)
        wk.append(in_worker(body0 + m.start()))
    for h in helpers:
        if h == short(d["name"]): continue
        for mm in re.finditer(r"(?<![\w:])%s\(" % re.escape(h), blanked[body0:body1]):
            calls.append((h, in_worker(body0 + mm.start())))
    return prim, calls, wk
_info = {short(d["name"]): _starts(d) for d in helper_defs}
bounded_helpers = {h for h, (prim, calls, wk) in _info.items() if prim and all(prim) and not calls}
while True:
    more = {h for h, (prim, calls, wk) in _info.items() if h not in bounded_helpers and (prim or calls)
            and all(prim) and calls and all(c in bounded_helpers for c, _w in calls)}
    if not more: break
    bounded_helpers |= more
# A helper whose every process runs on a worker (its own GuiLoading or thread).
worker_helpers = {h for h, (prim, calls, wk) in _info.items() if (wk or calls) and all(wk) and all(w for _c, w in calls)}
while True:
    more = {h for h, (prim, calls, wk) in _info.items() if h not in worker_helpers and calls
            and all(wk) and all(w or c in worker_helpers for c, w in calls)}
    if not more: break
    worker_helpers |= more
names = "|".join(sorted(map(re.escape, helpers), key=len, reverse=True))
for m in re.finditer(r"(?<![\w:>.])(%s)\(|%s" % (names, PRIM), blanked):
    name = m.group(1) or m.group(2)
    d = def_at(line_of(m.start()))
    if d and short(d["name"]) == name and line_of(m.start()) == d["start"]:
        continue                       # the runner's own definition line
    if in_helper(m.start()):
        continue                       # counted at the helper's call sites
    op = blanked.index("(", m.start()); args, end = call_args(op)
    txt = raw[m.start():end + 1]
    runs.append({"off": m.start(), "line": line_of(m.start()), "name": name,
                 "thread": "worker" if in_worker(m.start()) else ("worker (in the helper)" if name in worker_helpers else "interface"),
                 "bound": "timeout" if re.search(r"\btimeout\b", txt) else ("timeout (in the helper)" if name in bounded_helpers else "none"),
                 "page": page_at(m.start())})

opens = collections.defaultdict(list)
for m in re.finditer(r"\bnew (Gui|Cloud)(\w+)\b", blanked):
    n = m.group(1) + m.group(2)
    if n in ("GuiMsgBox", "GuiLoading", "GuiSettings"): continue
    p = page_at(m.start())
    if p: opens[id(p)].append("%s %d" % (n, line_of(m.start())))
bnames = "|".join(sorted(map(re.escape, builders), key=len, reverse=True))
for m in re.finditer(r"(?<![\w:])(%s)\(" % bnames, blanked):
    d = def_at(line_of(m.start()))
    if d and line_of(m.start()) == d["start"]: continue
    p = page_at(m.start())
    if p and (not p["def"] or short(p["def"]["name"]) != m.group(1)):
        opens[id(p)].append("%s %d" % (m.group(1), line_of(m.start())))

dialogs = []
for m in re.finditer(r"\bnew GuiMsgBox\(", blanked):
    args, end = call_args(m.end() - 1); a = [argtext(x) for x in args]
    btns = []
    for i in (2, 4, 6):
        if i >= len(a) or a[i].startswith("GuiMsgBoxIcon"):
            break                      # (window, text, name1, func1, icon): no more buttons
        l = lits(a[i]); bare = re.match(r'^"((?:[^"\\]|\\.)*)"$', a[i])
        btns.append(l[0] if l else (bare.group(1) + " (untranslated)") if bare and bare.group(1) else
                    "" if a[i] in ('""', "nullptr") else "expr:" + a[i][:20])
    btns = [b for b in btns if b]
    if not btns: btns = ["OK"]          # GuiMsgBox's default single button
    up = lambda b: b.replace(" (untranslated)", "").upper()
    back = btns[0] if len(btns) == 1 else next((b for b in btns if up(b) in ("OK", "NO")), btns[-1])
    text = lits(a[1]) if len(a) > 1 else []
    dialogs.append({"off": m.start(), "line": line_of(m.start()), "buttons": btns, "back": back,
                    "text": (text[0] if text else "expr: " + (a[1][:40] if len(a) > 1 else "")), "page": page_at(m.start())})

titles = [t for p in pages for t in p["titles"]]
got = {"pages": len(pages), "titles": len(titles), "runs": len(runs),
       "runs-interface": len([r for r in runs if r["thread"] == "interface"]), "dialogs": len(dialogs)}

if "--table" in sys.argv:
    print("| Title | Built at | Function | Range | Opens | Runs (line thread bound) | Threads | Dialogs (buttons; back) |")
    print("| --- | ---: | --- | --- | --- | --- | --- | --- |")
    for p in pages:
        pr = [r for r in runs if r["page"] is p]; pd = [x for x in dialogs if x["page"] is p]
        thr = sorted(set("%s %d" % ("GuiLoading" if "GuiLoading" in raw[a[0] - 200:a[0]] else "std::thread", line_of(a[0]))
                         for a in workers if p["range"][0] <= a[0] <= p["range"][1] and page_at(a[0]) is p))
        fn = p["def"]["name"].replace("GuiMenu::", "") if p["def"] else p.get("name", "")
        print("| %s | %d | `%s` | %d-%d | %s | %s | %s | %s |" % (
            " / ".join(p["titles"]).replace("|", "\\|"), p["line"], fn, line_of(p["range"][0]), line_of(p["range"][1]),
            ", ".join(opens[id(p)]) or "-",
            "; ".join("%s %d %s %s" % (r["name"], r["line"], r["thread"], r["bound"]) for r in pr) or "-",
            ", ".join(thr) or "-",
            "; ".join("%d %s; back %s" % (x["line"], "/".join(x["buttons"]), x["back"]) for x in pd) or "-"))
if "--dialogs" in sys.argv:
    for x in dialogs:
        print("dialog %d [%s] back=%s: %s" % (x["line"], " / ".join(x["buttons"]), x["back"], x["text"][:70]))

shapes = collections.Counter(" / ".join(x["buttons"]) for x in dialogs)
print("pages %d (%s); titles %d (literal %d, computed %d)" % (got["pages"], dict(collections.Counter(p["kind"].split()[0] for p in pages)),
      got["titles"], len([t for t in titles if not t.startswith("expr:")]), len([t for t in titles if t.startswith("expr:")])))
print("unique literal titles %d" % len(set(t for t in titles if not t.startswith("expr:"))))
print("runners (this file's functions that start a process, transitively): %d, of which page builders %d and helpers %d: %s"
      % (len(runners), len(runners & builders), len(helpers), ", ".join(sorted(helpers))))
print("runs %d: interface %d, worker %d; bounded %d (in the call %d, in the helper %d); bounded helpers: %s" % (got["runs"], got["runs-interface"],
      got["runs"] - got["runs-interface"], len([r for r in runs if r["bound"] != "none"]), len([r for r in runs if r["bound"] == "timeout"]),
      len([r for r in runs if r["bound"].startswith("timeout (")]), ", ".join(sorted(bounded_helpers))))
print("interface-thread runs with no bound %d; worker helpers: %s" % (len([r for r in runs if r["thread"] == "interface" and r["bound"] == "none"]),
      ", ".join(sorted(worker_helpers))))
print("dialogs %d; back lands on:" % got["dialogs"], dict(collections.Counter(x["back"] for x in dialogs)))
print("dialog shapes:", dict(shapes.most_common()))
drift = {k: (got[k], EXPECT[k]) for k in EXPECT if got[k] != EXPECT[k]}
if drift:
    print("DRIFT (got, asserted):", drift); sys.exit(1)
print("asserted counts hold")

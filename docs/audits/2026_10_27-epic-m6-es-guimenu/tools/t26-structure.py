#!/usr/bin/env python3
"""T26 (#673): GuiMenu.cpp's structure at the pin -- the transitions, the reads,
the duplicates, the conditionals, the includes and the header.

    python3 -I t26-structure.py <pin.cpp> <GuiMenu.h> <tests dir> [--transitions] [--reads] [--dups] [--ifs]

Method, stated so the figures can be checked:
- Definitions and blanking are `t26-defs.py`'s.
- **Transitions:** every `cloudSetupPresent(` call but its definition, and
  every lambda that both ends a page (`<x>->close()` or `delete <x>;`) and
  opens one (a call to a function of this file that builds a page, or a
  `pushGui(new Gui...`), the close and the open both in that lambda and
  not in a lambda nested in it. A row gives the closed page, what holds the
  lambda (the receiver of the call it is passed to), the capture list,
  whether a `cloudSetupPresent` is its scope's last statement (a `return;`
  after it counts as last, in the innermost block), the captured names used
  after the close (`this` when a bare member of `GuiMenu` is called) -- a
  use-after-free only when the holder is the closed page or a component its
  rows were built with (blindspot 4) --
  and the harnesses under `tests/` that name the enclosing function.
- **Reads:** every `exists(` and `isRegularFile(` call, its path argument
  (an identifier resolved to its last assignment in the function, or to a
  file-scope constant), and whether it is cached: `exists(p, false)` is not;
  `exists(p)` is; `isRegularFile` takes no flag and is cached
  (`FileSystemUtil.cpp:1122-1175`).
- **Duplicates:** every `_("...")` literal that labels a row (the first
  argument of a builder), titles a page, or is a dialog's text, built in two
  or more functions, with every line; and the count of one-line literals of
  any role in two or more functions.
- **Conditionals:** every `#if`/`#ifdef`/`#ifndef` region evaluated with
  `ROCKNIX` and `DISABLE_KODI` defined and `BATOCERA`, `WIN32`, `_WIN32`,
  `_RPI_`, `_ENABLEEMUELEC` and `_ENABLE_KODI_` undefined (the image build's
  flags); a condition naming another macro is `unknown` and its lines are
  counted apart. Lines counted are non-blank, non-preprocessor lines in an
  arm the build does not compile (`--lines` prints each such line, `dead`
  or `unknown`). A region whose first arm opens and closes a different
  number of braces is listed.
- **Header:** the identifiers declared with `(` inside `class GuiMenu` in the
  header, against the `GuiMenu::` definitions.
Exits 1 when a figure drifts from the counts asserted below.
"""
import importlib.util, os, re, sys, collections, bisect

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t26defs", os.path.join(HERE, "t26-defs.py"))
t26defs = importlib.util.module_from_spec(spec); spec.loader.exec_module(t26defs)
EXPECT = {"transitions-present": 16, "transitions-other": 10, "reads": 37, "reads-uncached": 12,
          "dup-labels": 74, "lits-2plus": 165, "if-lines": 86, "dead-lines": 869, "includes": 98}

path, hdr, tests = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(path, encoding="utf-8").read(); blanked = t26defs.blank(raw)
rl = raw.split("\n"); bl = blanked.split("\n")
starts = [0] + [m.end() for m in re.finditer("\n", raw)]
line_of = lambda off: bisect.bisect_right(starts, off)
defs = t26defs.definitions(path)
def_at = lambda ln: next((d for d in defs if d["start"] <= ln <= d["end"]), None)
short = lambda n: n.split("::")[-1]
def call_args(op):
    depth = 0; s = op + 1; args = []
    for i in range(op, len(blanked)):
        c = blanked[i]
        if c in "([{": depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0: args.append((s, i)); return args, i
        elif c == "," and depth == 1: args.append((s, i)); s = i + 1
    raise SystemExit("unbalanced at %d" % line_of(op))
argtext = lambda a: re.sub(r"\s+", " ", raw[a[0]:a[1]]).strip()
lit1 = lambda t: (re.findall(r'_\(\s*"((?:[^"\\]|\\.)*)"\s*\)', t) or [None])[0]
testtext = {f: open(os.path.join(tests, f), encoding="utf-8", errors="replace").read()
            for f in sorted(os.listdir(tests)) if f.endswith(".py")}
harness = lambda name: [f for f, t in testtext.items() if re.search(r"\b%s\b" % re.escape(name), t)]

# brace pairs (first-arm counting) and lambdas
pairs = []; st = []; cond = []
for ln, (r, b) in enumerate(zip(rl, bl), 1):
    s = r.strip()
    if s.startswith("#"):
        d = re.match(r"#\s*(\w+)", s); d = d.group(1) if d else ""
        if d in ("if", "ifdef", "ifndef"): cond.append(True)
        elif d in ("elif", "else"):
            if cond: cond[-1] = False
        elif d == "endif" and cond: cond.pop()
        continue
    if not all(cond): continue
    for i, ch in enumerate(b):
        if ch == "{": st.append(starts[ln - 1] + i)
        elif ch == "}" and st: pairs.append((st.pop(), starts[ln - 1] + i))
LAMBDA = re.compile(r"\[([^\[\]]*)\]\s*(\([^()]*\))?\s*(mutable)?\s*(->\s*[\w:<> ]+)?\s*$")
lambdas = []
for p in pairs:
    m = LAMBDA.search(blanked[max(0, p[0] - 400):p[0]])
    if m:
        cap = raw[p[0] - (len(blanked[max(0, p[0] - 400):p[0]]) - m.start()):p[0]]
        lambdas.append((p, re.sub(r"\s+", " ", re.match(r"\[([^\]]*)\]", cap).group(1)).strip()))
inner_lambda = lambda off: min((l for l in lambdas if l[0][0] < off < l[0][1]), key=lambda l: l[0][1] - l[0][0], default=None)
builders = {short(d["name"]) for d in defs if re.search(r"new (GuiSettings|CloudConnectionsPage)\(", blanked[starts[d["start"] - 1]:starts[d["end"]]])}

# --- transitions ------------------------------------------------------------------
trans = []
for m in re.finditer(r"\bcloudSetupPresent\(", blanked):
    d = def_at(line_of(m.start()))
    if d and short(d["name"]) == "cloudSetupPresent" and line_of(m.start()) == d["start"]:
        continue
    args, end = call_args(m.end() - 1); a = [argtext(x) for x in args]
    lam = inner_lambda(m.start())
    blk = min((q for q in pairs if q[0] < m.start() < q[1]), key=lambda q: q[1] - q[0])
    blk_end = blk[1]
    semi = blanked.index(";", end)
    last = re.sub(r"\breturn\s*;", "", blanked[semi + 1:blk_end]).strip() == ""
    trans.append({"line": line_of(m.start()), "func": short(d["name"]) if d else "?", "closes": a[2] if len(a) > 2 else "?",
                  "new": a[1] if len(a) > 1 else "?", "captures": lam[1] if lam else "(the function's own scope)",
                  "last": last, "harness": harness(short(d["name"])) if d else []})
def owner_of(lam):
    """The receiver of the call a lambda is passed to: the object that holds it."""
    i = lam[0][0]; depth = 0
    cap0 = blanked.rfind("[", 0, i)
    j = cap0
    while j > 0:
        j -= 1; ch = blanked[j]
        if ch in ")]}": depth += 1
        elif ch in "([{":
            if depth == 0:
                if ch != "(":
                    loc = re.search(r"\b([A-Za-z_]\w*)\s*=\s*$", blanked[max(0, cap0 - 80):cap0])
                    return "local `%s`" % loc.group(1) if loc else "?"
                m = re.search(r"([A-Za-z_]\w*)\s*(?:->|\.)\s*(?:getMenu\(\)\s*\.\s*)?([A-Za-z_]\w*)\s*$", blanked[max(0, j - 120):j])
                if m: return "%s (%s)" % (m.group(1), m.group(2))
                m = re.search(r"([A-Za-z_]\w*)\s*$", blanked[max(0, j - 80):j])
                return "%s(...)" % m.group(1) if m else "?"
            depth -= 1
    return "?"
members = {short(d["name"]) for d in defs if d["name"].startswith("GuiMenu::")}
others = []
OPEN = r"(?<![\w:])(%s)\(|pushGui\(\s*new\s+(Gui\w+|Cloud\w+)" % "|".join(map(re.escape, sorted(builders)))
for (p, cap) in lambdas:
    body = blanked[p[0]:p[1]]
    if "cloudSetupPresent(" in body: continue
    # a close and an open whose innermost lambda is this one
    own = lambda m: inner_lambda(p[0] + m.start())[0] == p
    cl = [m for m in re.finditer(r"\b([A-Za-z_]\w*)\s*->\s*close\(\)|\bdelete\s+([A-Za-z_]\w*)\s*;", body) if own(m)]
    opens = [o for o in re.finditer(OPEN, body) if own(o) and not (o.group(2) or "").startswith("GuiMsgBox")]
    if not cl or not opens: continue
    c = cl[0]; closed = c.group(1) or c.group(2); coff = p[0] + c.start()
    capnames = set(re.findall(r"[A-Za-z_]\w*", cap)) - {"this"}
    after = blanked[coff + len(c.group(0)):p[1]]
    used = sorted(n for n in capnames if n != closed and re.search(r"\b%s\b" % re.escape(n), after))
    if "this" in cap and re.search(r"(?<![\w.>:])(%s)\(" % "|".join(map(re.escape, sorted(members))), after):
        used.append("this (a member call)")
    closed_after = re.search(r"\b%s\b" % re.escape(closed), after) is not None
    d = def_at(line_of(p[0]))
    owner = owner_of((p, cap))
    orecv = owner.split()[0].split("(")[0]
    ftext = blanked[starts[d["start"] - 1]:starts[d["end"]]] if d else ""
    in_closed = orecv == closed or re.search(r"\b%s\s*->\s*(?:getMenu\(\)\s*\.\s*)?add\w*\([^;]*\b%s\b" % (re.escape(closed), re.escape(orecv)), ftext) is not None
    others.append({"line": line_of(coff), "func": short(d["name"]) if d else "?", "closes": closed, "owner": owner,
                   "owner_closed": in_closed,
                   "how": "close()" if c.group(1) else "delete", "opens": ", ".join("%s %d" % (o.group(1) or o.group(2), line_of(p[0] + o.start())) for o in opens),
                   "order": "close first" if c.start() < opens[0].start() else "open first",
                   "captures": cap, "used_after": used, "closed_used_after": closed_after,
                   "harness": harness(short(d["name"])) if d else []})

# --- reads ------------------------------------------------------------------------
in_def = lambda off: def_at(line_of(off)) is not None
consts = {m.group(1): m.group(2) for m in re.finditer(r'(?:static\s+)?(?:const\s+)?(?:std::string|char\s*\*|auto)\s+(?:const\s+)?([A-Za-z_]\w*)\s*(?:\[\])?\s*=\s*("[^"]*")', raw)
          if not in_def(m.start())}
DECL = r"(?:\b(?:const\s+)?(?:std::string|auto|std::filesystem::path)\s*&?\s+)%s\s*(?:=\s*([^;]+)|\(([^;]*)\))\s*;"
reads = []
for m in re.finditer(r"\b(exists|isRegularFile)\(", blanked):
    if blanked[m.start() - 1] in ".>" and not raw[max(0, m.start() - 20):m.start()].endswith("FileSystem::"):
        continue                       # a member exists() of another type
    args, end = call_args(m.end() - 1); a = [argtext(x) for x in args]
    p0 = a[0] if a else "?"
    d = def_at(line_of(m.start()))
    res = p0
    if re.match(r"^[A-Za-z_]\w*$", p0):
        fs = starts[d["start"] - 1] if d else 0
        sig = raw[fs:raw.index("{", fs)] if d else ""
        asg = list(re.finditer(DECL % re.escape(p0), raw[fs:m.start()]))
        if re.search(r"\b%s\s*[,)]" % re.escape(p0), sig):
            res = "%s (a parameter)" % p0
        elif asg:
            e = re.sub(r"\s+", " ", (asg[-1].group(1) or asg[-1].group(2) or "")).strip()
            res = "%s = %s" % (p0, e[:90]) if "[" not in e and "{" not in e else "%s (declared at %d)" % (p0, line_of(fs + asg[-1].start()))
        elif p0 in consts:
            res = "%s = %s" % (p0, consts[p0])
    cached = "cached" if m.group(1) == "isRegularFile" or len(a) < 2 or a[1].strip() != "false" else "uncached"
    reads.append({"line": line_of(m.start()), "func": short(d["name"]) if d else "(file scope)", "call": m.group(1),
                  "path": res, "cached": cached})

# --- duplicates --------------------------------------------------------------------
BUILDERS = r"(addSwitch|addOptionList|addInputTextConfigRow|addFileBrowser|addWithLabel|addWithDescription|addEntry|addGroup)"
labels = collections.defaultdict(list)
for m in re.finditer(r"\b%s\(" % BUILDERS, blanked):
    args, _ = call_args(m.end() - 1)
    l = lit1(argtext(args[0])) if args else None
    if l: labels[l].append(("row", line_of(m.start())))
for m in re.finditer(r"\bnew GuiSettings\(", blanked):
    args, _ = call_args(m.end() - 1)
    for l in re.findall(r'_\(\s*"((?:[^"\\]|\\.)*)"', argtext(args[1]) if len(args) > 1 else ""):
        labels[l].append(("title", line_of(m.start())))
for m in re.finditer(r"\bnew GuiMsgBox\(", blanked):
    args, _ = call_args(m.end() - 1)
    l = lit1(argtext(args[1])) if len(args) > 1 else None
    if l: labels[l].append(("dialog", line_of(m.start())))
dups = {l: v for l, v in labels.items() if len({short(def_at(x[1])["name"]) if def_at(x[1]) else "?" for x in v}) >= 2}
alllits = collections.defaultdict(set)
for m in re.finditer(r'_\("([^"]*)"\)', raw):
    if blanked[m.start():m.start() + 2] != "_(": continue  # in a comment
    d = def_at(line_of(m.start())); alllits[m.group(1)].add(short(d["name"]) if d else "(file scope)")
lits2 = [l for l, f in alllits.items() if len(f) >= 2]

# --- conditionals ---------------------------------------------------------------------
DEF1 = {"ROCKNIX": True, "DISABLE_KODI": True}
DEF0 = {"BATOCERA", "WIN32", "_WIN32", "_RPI_", "_ENABLEEMUELEC", "_ENABLE_KODI_"}
def evaluate(expr):
    toks = re.findall(r"defined\s*\(\s*\w+\s*\)|defined\s+\w+|\w+|&&|\|\||!|\(|\)", expr)
    pos = [0]; unknown = set()
    def atom():
        t = toks[pos[0]]; pos[0] += 1
        if t == "!":
            v = atom(); return None if v is None else not v
        if t == "(":
            v = orr(); pos[0] += 1; return v
        mm = re.match(r"defined\s*\(?\s*(\w+)", t)
        name = mm.group(1) if mm else t
        if re.match(r"^\d+$", name): return name != "0"
        if name in DEF1: return True
        if name in DEF0: return False
        unknown.add(name); return None
    def andd():
        v = atom()
        while pos[0] < len(toks) and toks[pos[0]] == "&&":
            pos[0] += 1; w = atom()
            v = False if v is False or w is False else (None if v is None or w is None else True)
        return v
    def orr():
        v = andd()
        while pos[0] < len(toks) and toks[pos[0]] == "||":
            pos[0] += 1; w = andd()
            v = True if v is True or w is True else (None if v is None or w is None else False)
        return v
    v = orr(); return v, unknown
regions = []; stack = []; linestate = {}
for ln, r in enumerate(rl, 1):
    s = r.strip()
    m = re.match(r"#\s*(if|ifdef|ifndef|elif|else|endif)\b(.*)", s)
    if m:
        k, rest = m.group(1), m.group(2).split("//")[0].strip()
        if k in ("if", "ifdef", "ifndef"):
            expr = rest if k == "if" else ("defined(%s)" % rest if k == "ifdef" else "!defined(%s)" % rest)
            v, unk = evaluate(expr)
            stack.append({"line": ln, "expr": s, "taken": v is True, "arm": v, "unk": unk, "first": True,
                          "lines": collections.Counter(), "braces": 0})
            regions.append(stack[-1])
        elif k in ("elif", "else") and stack:
            top = stack[-1]
            if k == "else":
                v = None if top["arm"] is None and not top["taken"] else (not top["taken"])
                if top["taken"]: v = False
            else:
                v, unk = evaluate(rest); top["unk"] |= unk
                if top["taken"]: v = False
            top["arm"] = v; top["taken"] = top["taken"] or v is True; top["first"] = False
        elif k == "endif" and stack:
            stack.pop()
        continue
    if not s: continue
    arms = [x["arm"] for x in stack]
    state = "dead" if any(a is False for a in arms) else ("unknown" if any(a is None for a in arms) else "live")
    if state != "live":
        linestate[ln] = state
    if stack:
        stack[-1]["lines"][state] += 1
        if stack[-1]["first"]:
            stack[-1]["braces"] += bl[ln - 1].count("{") - bl[ln - 1].count("}")
# each line is counted once, in its innermost region, judged by the whole stack
deadlines = sum(x["lines"]["dead"] for x in regions); unknownlines = sum(x["lines"]["unknown"] for x in regions)
deadby = collections.Counter()
for x in regions:
    if x["lines"]["dead"]:
        deadby[x["expr"][:60]] += x["lines"]["dead"]
unbalanced = [x for x in regions if x["braces"] != 0]

incl = [(i + 1, r.strip()) for i, r in enumerate(rl) if re.match(r"\s*#\s*include\b", r)]
inclc = collections.Counter(re.sub(r"\s+", "", x[1]) for x in incl)
inclbase = collections.Counter(os.path.basename(re.sub(r'.*[<"](.*)[>"].*', r"\1", x[1])) for x in incl)
htext = t26defs.blank(open(hdr, encoding="utf-8").read())
cls = re.search(r"class\s+GuiMenu\b[^{]*\{", htext)
hbody = htext[cls.end():]
NOTNAME = {"GuiMenu", "~GuiMenu", "if", "for", "while", "return", "sizeof", "switch", "void"}  # the ctor, keywords, `void (*)` types
declared = set(re.findall(r"\b([A-Za-z_~]\w*)\s*\(", hbody)) - NOTNAME
defined = {short(d["name"]) for d in defs if d["name"].startswith("GuiMenu::")} - NOTNAME

got = {"transitions-present": len(trans), "transitions-other": len(others), "reads": len(reads),
       "reads-uncached": len([r for r in reads if r["cached"] == "uncached"]), "dup-labels": len(dups),
       "lits-2plus": len(lits2), "if-lines": len(regions), "dead-lines": deadlines, "includes": len(incl)}

if "--transitions" in sys.argv:
    print("| Line | Function | Kind | Closes | Held by | Captures | After the close | Harness |")
    print("| ---: | --- | --- | --- | --- | --- | --- | --- |")
    for t in trans:
        print("| %d | `%s` | `cloudSetupPresent` (new `%s`) | `%s` | %s | `[%s]` | %s | %s |" % (t["line"], t["func"], t["new"], t["closes"],
              "-", t["captures"], "last" if t["last"] else "**statements follow**", ", ".join(t["harness"]) or "none"))
    for t in sorted(others, key=lambda t: t["line"]):
        aft = ("uses " + ", ".join(t["used_after"])) if t["used_after"] else "nothing captured"
        if t["used_after"] and not t["owner_closed"]: aft += " (its holder is not the closed page)"
        if t["owner_closed"] and t["used_after"]: aft = "**" + aft + ": the holder is the closed page or one of its rows**"
        print("| %d | `%s` | %s, opens %s (%s) | `%s` | `%s` | `[%s]` | %s | %s |" % (t["line"], t["func"], t["how"], t["opens"], t["order"], t["closes"],
              t["owner"], t["captures"].replace("|", "\\|"), aft, ", ".join(t["harness"]) or "none"))
if "--reads" in sys.argv:
    print("| Line | Function | Call | Path | Cache |")
    print("| ---: | --- | --- | --- | --- |")
    for r in reads:
        print("| %d | `%s` | `%s` | `%s` | %s |" % (r["line"], r["func"], r["call"], r["path"].replace("|", "\\|"), r["cached"]))
if "--dups" in sys.argv:
    print("| Literal | Built at (role line, function) |")
    print("| --- | --- |")
    for l, v in sorted(dups.items(), key=lambda kv: kv[1][0][1]):
        print("| %s | %s |" % (l.replace("|", "\\|").replace("\\n", " / ")[:90],
              "; ".join("%s %d `%s`" % (k, ln, short(def_at(ln)["name"]) if def_at(ln) else "?") for k, ln in v)))
if "--lines" in sys.argv:
    for ln in sorted(linestate):
        print("line %d %s" % (ln, linestate[ln]))
if "--ifs" in sys.argv:
    for x in regions:
        if x["lines"]["dead"] or x["lines"]["unknown"] or x["braces"]:
            print("if %d %-60s dead %d unknown %d braces %+d %s" % (x["line"], x["expr"][:60], x["lines"]["dead"], x["lines"]["unknown"],
                  x["braces"], ("unknown: " + ",".join(sorted(x["unk"]))) if x["unk"] else ""))

print("definitions %d (%s); the ten longest: %s" % (len(defs), dict(collections.Counter(d["kind"] for d in defs)),
      ", ".join("%s %d" % (short(d["name"]), d["end"] - d["start"] + 1) for d in sorted(defs, key=lambda d: d["start"] - d["end"])[:10])))
print("transitions: cloudSetupPresent calls %d (last statement %d; harnessed %d); other page replacements %d (harnessed %d; a capture used after closing the lambda's own holder %d)"
      % (len(trans), len([t for t in trans if t["last"]]), len([t for t in trans if t["harness"]]), len(others),
         len([t for t in others if t["harness"]]), len([t for t in others if t["used_after"] and t["owner_closed"]])))
print("reads %d: uncached %d, cached %d (exists %d, isRegularFile %d)" % (len(reads), got["reads-uncached"], len(reads) - got["reads-uncached"],
      len([r for r in reads if r["call"] == "exists"]), len([r for r in reads if r["call"] == "isRegularFile"])))
print("labels (row, title, dialog) built in two or more functions %d; one-line _() literals in two or more functions %d" % (len(dups), len(lits2)))
print("conditional regions %d; lines no ROCKNIX image compiles %d; lines under an unknown macro %d; regions whose first arm's braces do not balance %d: %s"
      % (len(regions), deadlines, unknownlines, len(unbalanced), ", ".join("%d %+d" % (x["line"], x["braces"]) for x in unbalanced)))
print("dead lines by condition (top 6):", dict(deadby.most_common(6)))
print("unknown macros:", sorted(set().union(*[x["unk"] for x in regions])))
print("includes %d; repeated lines %s; one header by two spellings %s" % (len(incl), {k: v for k, v in inclc.items() if v > 1},
      {k: v for k, v in inclbase.items() if v > 1 and k not in {kk.split("/")[-1].strip('<>"') for kk, vv in inclc.items() if vv > 1}}))
print("header: declared %d, GuiMenu:: defined %d; declared without a definition %s; defined without a declaration %s"
      % (len(declared), len(defined), sorted(declared - defined), sorted(defined - declared)))
drift = {k: (got[k], EXPECT[k]) for k in EXPECT if got[k] != EXPECT[k]}
if drift:
    print("DRIFT (got, asserted):", drift); sys.exit(1)
print("asserted counts hold")

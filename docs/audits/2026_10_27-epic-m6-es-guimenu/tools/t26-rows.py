#!/usr/bin/env python3
"""T26 (#673): the settings rows of GuiMenu.cpp at the pin, one table row each.

    python3 -I t26-rows.py <pin.cpp> <distribution checkout> <commit> [--table] [--writes]

Method, stated so the figures can be checked:
- A builder call is `\\b<builder>(` for the nine builders, found in the text
  with comments and string literals blanked (so a commented-out call is not
  counted); the nine greps over the raw lines are printed beside them.
- Arguments are split at top-level commas (parentheses, brackets and braces
  tracked; angle brackets are not, and no call here needs them).
- A **value-binding row** is:
  * an `addSwitch`, `addOptionList`, `addInputTextConfigRow` or
    `addFileBrowser` call, whose key and store are its own arguments; or
  * an `addWithLabel` / `addWithDescription` whose component argument is an
    identifier that a store write in the same function names: the write sits
    inside a save hook (`addSaveFunc`, `setOnChangedCallback`,
    `setSelectedChangedCallback`, `setOnValueChanged`, an `onFinalize`
    assignment) whose text mentions the identifier. When the identifier is
    bound by several rows of one function, the write goes to the nearest
    row by line.
- A store write is `SystemConf::getInstance()->set(` / `setBool(` or
  `Settings::getInstance()->set<Type>(`; its key is the first argument when
  that is a string literal, else `dynamic: <expression>`.
- Save mechanism: `close` (an `addSaveFunc`, or the builder's own for
  `addSwitch`/`addOptionList`), `immediate` (a change callback), `finalize`
  (an `onFinalize`), `edit-memory` (`addInputTextConfigRow` and
  `addFileBrowser` write the store in memory when the editor returns; the
  file is written only by a page save that has a save function, or by an
  `onFinalize` save).
- A store write outside every save hook is listed apart: it runs when the
  page is built, or in an action's own lambda (a press, a callback, a helper
  another callback calls) -- which of these is read at its line.
- The ROCKNIX column (with `--live <file>`, `t26-structure.py --lines`'s
  output): `dead` for a row no ROCKNIX image builds, `unknown` for one a
  device or build macro decides, else `built`.
- The OS column, for a literal `SystemConf` key: `set_setting` when a file
  under `projects/ROCKNIX/packages` at <commit> writes it with
  `set_setting <key>`, `named` when the key appears there as a word
  otherwise, `-` when it does not appear at all.
Exits 1 when a figure drifts from the counts asserted below (the asserted
counts are this generator's own, at the pin; a change to the file or the
method is a change to them, made on purpose).
"""
import importlib.util, os, re, subprocess, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t26defs", os.path.join(HERE, "t26-defs.py"))
t26defs = importlib.util.module_from_spec(spec); spec.loader.exec_module(t26defs)

BUILDERS = ["addSwitch", "addOptionList", "addInputTextConfigRow", "addFileBrowser",
            "addWithLabel", "addWithDescription", "addEntry", "addGroup", "addRow"]
HOOKS = ["addSaveFunc", "setOnChangedCallback", "setSelectedChangedCallback", "setOnValueChanged"]
EXPECT = {"calls": 561, "binding": 275, "builder-own": 61, "by-write": 214,
          "component-unbound": 25, "writes": 267, "writes-in-rows": 247, "outside-hooks": 19}

pin_path, dist, commit = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(pin_path, encoding="utf-8").read()
blanked = t26defs.blank(raw)
assert len(blanked) == len(raw)
line_of = lambda off: raw.count("\n", 0, off) + 1
defs = t26defs.definitions(pin_path)
def func_at(ln):
    for d in defs:
        if d["start"] <= ln <= d["end"]:
            return d
    return None

def call_args(open_paren):
    """Offsets of each top-level argument of the call whose '(' is at open_paren."""
    depth = 0; start = open_paren + 1; args = []
    i = open_paren
    while i < len(blanked):
        c = blanked[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                args.append((start, i)); return args, i
        elif c == "," and depth == 1:
            args.append((start, i)); start = i + 1
        i += 1
    raise SystemExit("unbalanced call at line %d" % line_of(open_paren))

argtext = lambda a: re.sub(r"\s+", " ", raw[a[0]:a[1]]).strip()
def label_of(t):
    m = re.search(r'_\(\s*"((?:[^"\\]|\\.)*)"', t) or re.match(r'"((?:[^"\\]|\\.)*)"', t)
    return m.group(1) if m else "expr: " + t[:50]
def key_of(t):
    m = re.match(r'"((?:[^"\\]|\\.)*)"$', t)
    return m.group(1) if m else "dynamic: " + t[:50]

# --- store writes, and the save hook around each ------------------------------------
WRITE = re.compile(r"\b(?:(SystemConf|Settings)::getInstance\(\)->|(conf)->|(Settings)::)(set[A-Z]?[A-Za-z]*)\(")
hooks = []   # (start, end, kind)
for h in HOOKS:
    for m in re.finditer(r"\b%s\(" % h, blanked):
        _, end = call_args(m.end() - 1)
        # a change callback's receiver (`comp->setOnChangedCallback(`) names the component too
        recv = re.search(r"([A-Za-z_]\w*)\s*(->|\.)\s*$", blanked[max(0, m.start() - 80):m.start()])
        start = m.start() - (len(recv.group(0)) if recv and h != "addSaveFunc" else 0)
        hooks.append((start, end, "close" if h == "addSaveFunc" else "immediate"))
for m in re.finditer(r"\bonFinalize\b\s*\(", blanked):     # setter form
    _, end = call_args(m.end() - 1)
    hooks.append((m.start(), end, "finalize"))
for m in re.finditer(r"\bonFinalize\b\s*=\s*\[", blanked):   # assignment form: up to the lambda's end
    i = blanked.index("{", m.end()); depth = 0
    while True:
        if blanked[i] == "{": depth += 1
        elif blanked[i] == "}":
            depth -= 1
            if depth == 0: break
        i += 1
    hooks.append((m.start(), i, "finalize"))
writes = []
for m in WRITE.finditer(blanked):
    args, _ = call_args(m.end() - 1)
    store = m.group(1) or ("SystemConf" if m.group(2) else "Settings")
    form = "direct" if m.group(1) else "alias" if m.group(2) else "static"
    if form == "alias" and not re.search(r"auto conf = SystemConf::getInstance\(\)", blanked[max(0, m.start() - 3000):m.start()]):
        continue                       # a `conf` that is not the SystemConf alias
    key = key_of(argtext(args[0])) if args and form != "static" else ("static: " + m.group(4)) if form == "static" else "?"
    enclosing = [h for h in hooks if h[0] < m.start() < h[1]]
    hook = min(enclosing, key=lambda h: h[1] - h[0]) if enclosing else None
    writes.append({"off": m.start(), "end": _, "line": line_of(m.start()), "store": store, "setter": m.group(4),
                   "key": key, "hook": hook, "form": form})

# --- builder calls -------------------------------------------------------------------
calls = []
for b in BUILDERS:
    for m in re.finditer(r"\b%s\(" % b, blanked):
        d = func_at(line_of(m.start()))
        args, end = call_args(m.end() - 1)
        calls.append({"b": b, "off": m.start(), "line": line_of(m.start()), "args": [argtext(a) for a in args],
                      "func": d["name"] if d else "(file scope)", "d": d})
calls.sort(key=lambda c: c["off"])

rows = []; unbound = []
for c in calls:
    a = c["args"]; b = c["b"]; n = len(a)
    if b == "addSwitch":
        title, key, store = (a[0], a[2], a[3]) if n >= 5 else (a[0], a[1], a[2])
        rows.append(dict(c, label=label_of(title), key=key_of(key), store="Settings" if store == "true" else "SystemConf" if store == "false" else "expr: " + store, save="close", how="builder"))
    elif b == "addOptionList":
        if n >= 4 and a[3] in ("true", "false"):     # (title, values, key, store[, onChanged])
            title, key, store = a[0], a[2], a[3]
        else:                                          # (title, description, values, key, store, onChanged)
            title, key, store = a[0], a[3], a[4]
        rows.append(dict(c, label=label_of(title), key=key_of(key), store="Settings" if store == "true" else "SystemConf" if store == "false" else "expr: " + store, save="close", how="builder"))
    elif b in ("addInputTextConfigRow", "addFileBrowser"):
        store = a[3] if n >= 4 else "false"
        rows.append(dict(c, label=label_of(a[0]), key=key_of(a[1]), store="Settings" if store == "true" else "SystemConf" if store == "false" else "expr: " + store, save="edit-memory", how="builder"))
    elif b in ("addWithLabel", "addWithDescription"):
        ci = 1 if b == "addWithLabel" else 2
        comp = a[ci] if n > ci else ""
        if not re.match(r"^[A-Za-z_]\w*$", comp) or comp in ("nullptr", "NULL"):
            continue                       # an action row, or a component built inline
        c = dict(c, label=label_of(a[0]), comp=comp)
        c["writes"] = []
        rows.append(c)
# An `addRow(<row>)` row binds each component added to <row> by `<row>.addElement(<ident>, ...)`
# since the row's previous `addRow`, its declaration or its `elements.clear()`; its label is the
# first `_("...")` literal in that window. Only a component declared as a switch, an option
# list or a slider counts: the rest of a hand-built row is its label, arrows and spacers.
for c in [c for c in calls if c["b"] == "addRow"]:
    rv = c["args"][0] if c["args"] else ""
    if not re.match(r"^[A-Za-z_]\w*$", rv):
        continue
    d = c["d"]
    fstart = sum(len(l) + 1 for l in raw.split("\n")[:d["start"] - 1])
    marks = [m.end() for m in re.finditer(r"\b(ComponentListRow\s+%s\b|%s\.elements\.clear\(\)|\baddRow\(\s*%s\s*\))" % (rv, rv, rv), blanked[fstart:c["off"]])]
    lo = fstart + (marks[-1] if marks else 0)
    win = raw[lo:c["off"]]
    comps = [m.group(1) for m in re.finditer(r"\b%s\.addElement\(\s*([A-Za-z_]\w*)\s*," % rv, blanked[lo:c["off"]])]
    lab = re.search(r'_\(\s*"((?:[^"\\]|\\.)*)"', win)
    for comp in comps:
        if not re.search(r"\b%s\s*=\s*std::make_shared<\s*(SwitchComponent|OptionListComponent|SliderComponent)\b" % re.escape(comp), blanked[fstart:c["off"]]):
            continue                   # a label, an arrow, a spacer, an image: not a value
        rows.append(dict(c, label=(lab.group(1) if lab else "expr: (row)"), comp=comp, writes=[], row_built=True))
binding_by_write = [r for r in rows if r.get("comp")]
# Row-centric: a row's writes are in the save hooks of its function that name its component,
# inside the component's declaration window (from the declaration before the row to the next
# re-declaration of the same name). Within a hook, a write whose own arguments name a
# component (or a local assigned from it) belongs to that component; in a change callback,
# another write belongs to the callback's receiver; else to the component the lambda's
# body names last before it; a write with none before it
# belongs to no row (it is listed). Capture lists are not mentions. A write may serve two
# rows -- an if/else pair building one row.
def names(text, ident):
    return re.search(r"\b%s\b" % re.escape(ident), text) is not None
for r in binding_by_write:
    d = r["d"]; ident = r["comp"]
    decl = re.compile(r"(\bauto\s+|std::shared_ptr<[^;=]*>\s+|^\s*)%s\s*=\s*std::make_shared" % re.escape(ident), re.M)
    fstart = sum(len(l) + 1 for l in raw.split("\n")[:d["start"] - 1])
    fend = sum(len(l) + 1 for l in raw.split("\n")[:d["end"]])
    before = [m.start() for m in decl.finditer(blanked, fstart, r["off"])]
    after = [m.start() for m in decl.finditer(blanked, r["off"], fend)]
    lo = before[-1] if before else fstart; hi = after[0] if after else fend
    for w in writes:
        if not w["hook"] or not (lo <= w["off"] < hi):
            continue
        htext = blanked[w["hook"][0]:w["hook"][1]]
        if not names(htext, ident):
            continue
        wargs = blanked[w["off"]:w["end"]]
        comps = sorted(set(x["comp"] for x in binding_by_write if x["d"] is d and names(htext, x["comp"])))
        # the lambda's body: mentions in its capture list do not count
        body0 = htext.find("{", htext.find("]") + 1) if "[" in htext else 0
        body = htext[body0:]; rel = w["off"] - w["hook"][0] - body0
        # a local assigned from a component stands for it in a write's arguments
        alias = {}
        for m in re.finditer(r"\b([A-Za-z_]\w*)\s*=\s*([^;=][^;]*);", body[:max(rel, 0)]):
            alias.setdefault(m.group(1), set()).update(c for c in comps if names(m.group(2), c))
        inargs = [c for c in comps if names(wargs, c) or any(c in alias.get(v, ()) for v in re.findall(r"[A-Za-z_]\w*", wargs))]
        recv = re.match(r"\s*([A-Za-z_]\w*)\s*(->|\.)", htext)
        if inargs:
            owner = inargs
        elif recv and recv.group(1) in comps:   # a change callback's own component
            owner = [recv.group(1)]
        else:                          # the component the body names last before the write
            last = {c: max([m.start() for m in re.finditer(r"\b%s\b" % re.escape(c), body) if m.start() < rel] or [-1]) for c in comps}
            best = max(last.values()) if last else -1
            owner = [c for c in comps if last[c] == best] if best >= 0 else []
        if ident in owner:
            r["writes"].append(w); w.setdefault("rows", []).append(r); w["row"] = r
def unbound_class(r):
    """What saves a component row that no store write names, from the text around it."""
    d = r["d"]; ident = r["comp"]
    fstart = sum(len(l) + 1 for l in raw.split("\n")[:d["start"] - 1]); fend = sum(len(l) + 1 for l in raw.split("\n")[:d["end"]])
    ftext = blanked[fstart:fend]
    if re.search(r"\b%s\s*=\s*std::make_shared<\s*TextComponent\b" % re.escape(ident), ftext):
        return "read-only fact (a TextComponent)"
    named = [h for h in hooks if fstart <= h[0] < fend and re.search(r"\b%s\b" % re.escape(ident), blanked[h[0]:h[1]])]
    htext = " ".join(blanked[h[0]:h[1]] + raw[h[0]:h[1]] for h in named)
    if "ApiSystem::" in htext: return "a save hook calling ApiSystem"
    if "runSystemCommand" in htext: return "a save hook running a script"
    if named: return "a save hook with no store write (%s)" % ",".join(str(line_of(h[0])) for h in named)
    if re.search(r"(push_back\(\s*\{[^}]*\b%s\b|\.component\s*=\s*%s\b)" % (re.escape(ident), re.escape(ident)), ftext):
        return "collected into a container, saved by its reader"
    if re.search(r"addEntry\([^;]*\[[^\]]*\b%s\b" % re.escape(ident), ftext):
        return "an input to an action row"
    return "nothing found"
final = []
for r in rows:
    if r.get("comp"):
        if not r["writes"]:
            unbound.append(r); continue
        ws = r["writes"]
        r["key"] = "; ".join(sorted(set(w["key"] for w in ws)))
        r["store"] = "/".join(sorted(set(w["store"] for w in ws)))
        r["save"] = "/".join(sorted(set(w["hook"][2] for w in ws)))
        r["how"] = "write %s" % ",".join(str(w["line"]) for w in ws)
    final.append(r)

# --- the OS column --------------------------------------------------------------------
lit = sorted(set(k for r in final if r["store"] in ("SystemConf",) for k in r["key"].split("; ") if not k.startswith("dynamic")))
def git(*args):
    p = subprocess.run(["git", "-C", dist] + list(args), capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise SystemExit("git %s: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout
setters = set(re.findall(r"set_setting\s+\"?([A-Za-z0-9_.-]+)", git("grep", "-h", "-E", r"set_setting\s", commit, "--", "projects/ROCKNIX/packages")))
named = set()
for k in lit:
    rc = subprocess.run(["git", "-C", dist, "grep", "-q", "-w", "-F", "-e", k, commit, "--", "projects/ROCKNIX/packages"]).returncode
    if rc not in (0, 1):
        raise SystemExit("git grep for %s exited %d" % (k, rc))
    if rc == 0:
        named.add(k)
# get_setting falls back to global.<key> (001-functions:164-172), and the
# launch scripts ask for the suffix through get_setting, game_setting or
# add_setting: global.X is read when a script asks for X.
suffixed = set()
asked = git("grep", "-h", "-o", "-E", r"\b(get_setting|game_setting|add_setting)[[:space:]]+\"?[A-Za-z0-9_.-]+",
            commit, "--", "projects/ROCKNIX/packages")
for m in re.finditer(r"\b(?:get_setting|game_setting|add_setting)\s+\"?([A-Za-z0-9_.-]+)", asked):
    suffixed.add(m.group(1))
def os_col(r):
    if r["store"] != "SystemConf":
        return ""
    out = []
    for k in r["key"].split("; "):
        if k.startswith("dynamic"): out.append("dynamic")
        elif k in setters: out.append("set_setting")
        elif k in named: out.append("named")
        elif k.startswith("global.") and k[len("global."):] in suffixed: out.append("suffix")
        else: out.append("-")
    return ",".join(out)

build_time = [w for w in writes if not w["hook"]]
greps = {b: sum(1 for l in raw.split("\n") if re.search(r"\b%s\(" % b, l)) for b in BUILDERS}
got = {"calls": len(calls), "binding": len(final), "builder-own": len([r for r in final if r["how"] == "builder"]),
       "by-write": len([r for r in final if r["how"] != "builder"]), "component-unbound": len(unbound),
       "writes": len(writes), "writes-in-rows": len([w for w in writes if "row" in w]), "outside-hooks": len(build_time)}

# --live <file>: t26-structure.py --lines's output; a row on a line there is not
# built by a ROCKNIX image (`dead`) or depends on a device or build macro (`unknown`).
built = {}
if "--live" in sys.argv:
    for l in open(sys.argv[sys.argv.index("--live") + 1]):
        m = re.match(r"line (\d+) (dead|unknown)$", l.strip())
        if m: built[int(m.group(1))] = m.group(2)
built_of = lambda r: built.get(r["line"], "built") if built else ""
if "--table" in sys.argv:
    print("| Line | Function | Builder | Label | Key | Store | Save | OS | ROCKNIX |")
    print("| ---: | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in sorted(final, key=lambda r: r["line"]):
        lab = r["label"].replace("|", "\\|")[:70]
        print("| %d | `%s` | `%s` | %s | `%s` | %s | %s | %s | %s |" % (r["line"], r["func"].replace("GuiMenu::", ""), r["b"], lab,
              r["key"].replace("|", "\\|")[:80], r["store"], r["save"], os_col(r), built_of(r)))
if built:
    unread = [r for r in final if r["store"] == "SystemConf" and "-" in os_col(r).split(",")]
    print("SystemConf rows whose literal key nothing under projects/ROCKNIX/packages names: %d (%s)"
          % (len(unread), dict(collections.Counter(built_of(r) for r in unread))))
if "--writes" in sys.argv:
    print("\nwrites outside every save hook (at build, or in an action's own lambda):")
    for w in build_time:
        print("  %d %s %s->%s(%s)" % (w["line"], (func_at(w["line"]) or {"name": "?"})["name"], w["store"], w["setter"], w["key"]))
    print("\nwrites in a hook that no row's component names:")
    for w in writes:
        if w["hook"] and "row" not in w:
            print("  %d %s %s %s(%s) [%s]" % (w["line"], (func_at(w["line"]) or {"name": "?"})["name"], w["hook"][2], w["store"], w["key"], w["setter"]))
    print("\nrows with a component and no store write found:")
    for r in unbound:
        print("  %d %s %s %s (%s): %s" % (r["line"], r["func"], r["b"], r["label"][:60], r["comp"], unbound_class(r)))

stores = collections.Counter(r["store"] for r in final)
saves = collections.Counter(r["save"] for r in final)
oss = collections.Counter(x for r in final for x in os_col(r).split(",") if x)
print("greps (raw lines):", " ".join("%s %d" % (b, greps[b]) for b in BUILDERS), "= %d" % sum(greps.values()))
print("calls in code: %d; value-binding rows %d (builder-own %d, by a store write %d); component rows with no store write %d"
      % (got["calls"], got["binding"], got["builder-own"], got["by-write"], got["component-unbound"]))
print("stores:", dict(stores), "saves:", dict(saves))
print("component rows with no store write, by what saves them:", dict(collections.Counter(unbound_class(r) for r in unbound)))
print("store writes %d (SystemConf %d, Settings %d; literal keys %d, dynamic %d): in a row %d, in a hook no row names %d, outside every save hook %d"
      % (got["writes"], len([w for w in writes if w["store"] == "SystemConf"]), len([w for w in writes if w["store"] == "Settings"]),
         len([w for w in writes if not w["key"].startswith("dynamic")]), len([w for w in writes if w["key"].startswith("dynamic")]),
         got["writes-in-rows"], len([w for w in writes if w["hook"] and "row" not in w]), got["outside-hooks"]))
print("OS column over SystemConf keys:", dict(oss), "; distinct literal SystemConf row keys %d" % len(lit))
drift = {k: (got[k], EXPECT[k]) for k in EXPECT if got[k] != EXPECT[k]}
if drift:
    print("DRIFT (got, asserted):", drift); sys.exit(1)
print("asserted counts hold")

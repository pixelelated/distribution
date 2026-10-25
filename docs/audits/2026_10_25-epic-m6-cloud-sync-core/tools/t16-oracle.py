#!/usr/bin/env python3
"""T16 (#663): the oracle table -- T13's 79 assertion rows read against this slice's scripts.

  t16-oracle.py <T13 02-forward-audit.md> <cloud-round-trip at 8ebaf8daad> [--json OUT] [--markdown]

Reads T13's § Assertion shapes (79 rows: Row, Lines, Claim, Oracle with its
"(reviewed)" marks), takes each row's line span of the harness, and finds in
it the invocations of the slice's nine scripts (a script name followed by its
flags inside one string literal) and the check() calls (their `ok` text is
what a FAIL says was not true). Asserts 79 rows in and the Oracle column's
25 / 46 / 8; exits 1 naming any delta. Nothing is typed by hand.
"""
import ast, json, re, sys
from collections import Counter

SCRIPTS = ["cloud_backup", "cloud_restore", "cloud_capture", "cloud_saves_root", "cloud_sync_helper",
           "cloud_net_ready", "102-cloud-saves", "rasteratops-settings-archive", "cloud_sync_cleanup_duplicates.sh"]
INVOKE = re.compile(r"(?<![\w./-])(" + "|".join(re.escape(s) for s in SCRIPTS) + r")((?:\s+-{1,2}[A-Za-z][\w-]*(?:=\S+)?)*)")
EXPECT = {"both ends": 25, "synthetic": 46, "device report": 8}
T17 = re.compile(r"\b(cloud_(?:content_backup|content_restore|content_transfer|setup|scan|oauth|remote|device_id|folder_validate|log_scrub))\b")

def helpers(src):
    """Functions of the harness whose bodies invoke one of the nine: name -> the invocations, with flags."""
    defs = [(i, len(m.group(1)), m.group(2)) for i, l in enumerate(src) for m in [re.match(r"^(\s*)def (\w+)\(", l)] if m]
    out = {}
    for i, ind, n in defs:
        j = i + 1
        while j < len(src) and (not src[j].strip() or len(src[j]) - len(src[j].lstrip()) > ind):
            j += 1
        inv = invocations(src[i:j])
        if inv: out[n] = (i + 1, j, inv)
    return out

def invocations(lines):
    inv = []
    for ln in lines:
        for m in INVOKE.finditer(ln):
            flags = " ".join(sorted(set(m.group(2).split())))
            key = m.group(1) + (" " + flags if flags else "")
            if key not in inv: inv.append(key)
    return inv

def table(md):
    sec = re.search(r"^## Assertion shapes\n(.*?)(?=^## )", md, re.S | re.M).group(1)
    rows = [l for l in sec.splitlines() if l.startswith("| ")][2:]
    out = []
    for l in rows:
        c = [x.strip() for x in l.strip().strip("|").split(" | ")]
        name = c[0].strip("`"); lines = c[1]; claim = c[2]; oracle = c[3]
        reviewed = "(reviewed)" in oracle
        out.append({"row": name, "lines": lines, "claim": claim,
                    "oracle": oracle.replace(" (reviewed)", ""), "reviewed": reviewed})
    return out

def span(s):
    m = re.match(r"(\d+)-(\d+)$", s)
    return (int(m.group(1)), int(m.group(2))) if m else None

def checks(src_lines, a, b):
    """The ok text of each check() in [a, b], from the AST: check(cond, ok, bad)."""
    seg = "\n".join(src_lines[a - 1:b])
    oks = []
    for m in re.finditer(r"\bcheck\(", seg):
        i = m.end(); depth = 1; j = i
        while j < len(seg) and depth:
            depth += {"(": 1, ")": -1}.get(seg[j], 0); j += 1
        call = "check(" + seg[i:j]
        try:
            node = ast.parse(call.replace("\n", " "), mode="eval").body
            ok = node.args[1] if len(node.args) > 1 else None
            if isinstance(ok, ast.Constant): oks.append(str(ok.value))
            elif isinstance(ok, ast.JoinedStr):
                oks.append("".join(v.value if isinstance(v, ast.Constant) else "{...}" for v in ok.values))
            else: oks.append("(computed)")
        except SyntaxError:
            oks.append("(unparsed)")
    return oks

def main():
    md = open(sys.argv[1]).read(); src = open(sys.argv[2]).read().split("\n")
    rows = table(md)
    deltas = []
    if len(rows) != 79: deltas.append(f"rows {len(rows)} != 79")
    cnt = Counter(r["oracle"] for r in rows)
    for k, v in EXPECT.items():
        if cnt.get(k, 0) != v: deltas.append(f"{k} {cnt.get(k, 0)} != {v}")
    H = helpers(src)
    for r in rows:
        sp = span(r["lines"]); r["span"] = sp
        inv, via, t17 = [], [], []
        if sp:
            seg = src[sp[0] - 1:sp[1]]
            inv = invocations(seg)
            if not inv:   # the row's own text names none: the helpers it calls, outside its span
                for n, (a, b, hinv) in H.items():
                    if not (sp[0] <= a <= sp[1]) and any(re.search(r"\b" + n + r"\(", l) for l in seg):
                        via.append(n); inv += [x for x in hinv if x not in inv]
            t17 = sorted({m.group(1) for l in seg for m in T17.finditer(l)})
        r["invokes"] = inv; r["via"] = via; r["t17"] = t17
        r["scripts"] = sorted({i.split()[0] for i in inv})
        r["checks"] = checks(src, *sp) if sp else []
    out = {"rows": len(rows), "by_oracle": dict(cnt), "reviewed": sum(r["reviewed"] for r in rows),
           "reading_slice": sum(1 for r in rows if r["scripts"]), "via_helper": sum(1 for r in rows if r["via"]),
           "t17_only": sum(1 for r in rows if not r["scripts"] and r["t17"]), "deltas": deltas, "table": rows}
    if "--json" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "table"}))
    if "--markdown" in sys.argv:
        print("| Row | Harness lines | Oracle | Scripts invoked, with flags | What makes it FAIL (each check's ok, false) | proved: |")
        print("| --- | --- | --- | --- | --- | --- |")
        for r in rows:
            inv = "; ".join(f"`{i}`" for i in r["invokes"])
            if r["via"]: inv += " (via " + ", ".join(f"`{v}()`" for v in r["via"]) + ")"
            if not inv: inv = ("none of the nine; T17's " + ", ".join(f"`{t}`" for t in r["t17"])) if r["t17"] else "none of the nine"
            fail = "; ".join(f"not: {o}" for o in r["checks"][:3]) + (f" (+{len(r['checks']) - 3} more)" if len(r["checks"]) > 3 else "")
            print(f"| `{r['row']}` | {r['lines']} | {r['oracle']}{' (reviewed)' if r['reviewed'] else ''} | {inv} | {(fail or 'no check() in the span').replace('|', '/')} | tree |")
    return 1 if deltas else 0

sys.exit(main())

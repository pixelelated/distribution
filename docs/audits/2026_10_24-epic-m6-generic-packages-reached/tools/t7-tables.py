#!/usr/bin/env python3
"""T7's tables (#654), from the § 5 results under .qa-scratch/t7/, so 02's
coverage table, 04's Q4 currency table, q4-pins.json and 04's Q7 #645 rows
cannot disagree.

    python3 -I t7-tables.py <worktree> coverage|q4|q4json|q7 > out

Reads the slice's paths from the inventory with brief § 2's filter and every
result file the § 5 commands wrote. Asserts 266 paths and 243 recipes, and
that each result file covers every recipe it should, so a missing line fails
here rather than printing an empty cell.
"""
import json, re, sys, collections
from pathlib import Path

T = Path(sys.argv[1]); WHAT = sys.argv[2]; Q = T / ".qa-scratch/t7"
inv = json.load(open(T / "docs/reviews/inventory.json")); cols = inv["columns"]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
rows = {r["path"]: r for r in (dict(zip(cols, x)) for x in inv["rows"])
        if r["tree"] == "distribution" and r["area"] == "generic-packages"
        and gm(r["path"], "packages/**") and r["reach"] in ("shipped", "test", "n/a")}
assert len(rows) == 266, len(rows)
recipes = sorted(p for p in rows if p.endswith("/package.mk"))
assert len(recipes) == 243, len(recipes)
name = lambda p: p.split("/")[-2]
N = {name(p): p for p in recipes}; assert len(N) == 243

def lines(f): return [l for l in (Q / f).read_text().splitlines() if l.strip()]
q4a = {l.split()[1]: l.split()[0] for l in lines("q4a.txt")}
q4b = dict(l.split(" ", 1) for l in lines("q4b.txt"))
q4bo = {l.split()[0]: l.split()[1] for l in lines("q4b-other.txt")}
assert set(q4a) == set(recipes) and set(q4b) == set(recipes)
fresh = {}
for l in lines("q4c.txt")[1:]:
    f = l.split(None, 3); fresh[f[0]] = (f[1], f[2], f[3])
hashc = {}
for l in lines("q4c-hash.txt"):
    n, rest = l.split(" ", 1); hashc[n] = rest
PLANS = ["GENERIC_X64-x86_64", "H700-aarch64", "H700-arm", "SM8550-aarch64", "SM8550-arm"]
eff = {pl: {} for pl in PLANS}
for pl in PLANS:
    for l in lines(f"probe/expand-{pl}.txt"):
        n, s, v, u = l.split(" ", 3); eff[pl][n] = (v, s, u)
    assert set(eff[pl]) == set(N), pl
head = {}
for l in lines("probe/head.txt"):
    f = l.split(" "); head[f[0]] = (f[1], f[2] if len(f) == 4 else "")
assert set(head) == set(N)
fetch = {l.split()[0]: l.split(" ", 1)[1] for l in lines("probe/fetch.txt")}
mirror = {l.split()[0]: l for l in lines("probe/mirror.txt")}
stamp = {l.split()[1]: l.split()[0] for l in lines("stamps-url.txt")}
pk_tree = {l.split()[-1] if l.startswith("PASS") else l.split()[2]: l.split()[0] for l in lines("pkgcheck-pkgcheck.txt")}
pk_t6 = {l.split()[-1] if l.startswith("PASS") else l.split()[2]: l.split()[0] for l in lines("pkgcheck-pkgcheck-t6.txt")}
assert set(pk_tree) == set(N) and set(pk_t6) == set(N)
ROOTS = {"GENERIC_X64-x86_64": "build.pixelelated-GENERIC_X64.x86_64", "H700-aarch64": "build.pixelelated-H700.aarch64",
         "H700-arm": "build.pixelelated-H700.arm", "SM8550-aarch64": "build.pixelelated-SM8550.aarch64", "SM8550-arm": "build.pixelelated-SM8550.arm"}
stamps = {pl: set(lines(f"stamps-{r}.txt")) for pl, r in ROOTS.items()}
over = collections.defaultdict(list)
for l in lines("sourcing-overrides.txt"):
    g, _, o = l.split(" "); over[g].append(o)
def pin_of(p):
    m = re.search(r'^PKG_VERSION="([^"]*)"', (Q / "at-hash" / p).read_text(), re.M); return m.group(1) if m else None
def le_text(p):
    f = Q / "le" / p.replace("/", "_"); return f.read_text() if f.exists() else None

FORK_ADDED = {p for p, s in q4a.items() if s == "absent-upstream"}
FORK_EDITED = {p for p, s in q4a.items() if s == "differs"}
assert len(FORK_ADDED) == 13 and len(FORK_EDITED) == 3
HASH = {n for n in N if re.fullmatch(r"[0-9a-f]{40}", eff["GENERIC_X64-x86_64"][n][0])}
assert len(HASH) == 10, HASH
VIRTUAL = {n for n in N if N[n].startswith("packages/virtual/")}
# the findings by name, so a row can cite its own (02's F-numbers)
FIND = {"libfmt": "F-01", "wsdd2": "F-02", "newt": "F-03", "libmpeg2": "F-04", "configtools": "F-05",
        "brotli": "F-06", "ruby": "F-07", "glib-networking": "F-08", "webkitgtk": "F-09"}
RENAMED = {"lm_sensors": "groeck/lm-sensors -> lm-sensors/lm-sensors", "libfreeaptx": "iamthehorker -> regularhunter", "nss-mdns": "lathiat -> avahi"}

def shape(n):
    v = eff["GENERIC_X64-x86_64"][n][0]
    if n in VIRTUAL: return "virtual (no source)"
    if n == "harfbuzz-icu": return "inherited (sources harfbuzz)"
    if n == "nspr": return "version (unpacks from nss)"
    if n in HASH: return "hash"
    return "version"

def pin_cell(n):
    vs = {pl: eff[pl][n][0] for pl in PLANS}; g = pin_of(N[n])
    if len(set(vs.values())) == 1:
        v = vs[PLANS[0]]
        if v == "-": return "-"
        c = "`" + (v[:12] if n in HASH else v) + "`"
        return c + (f" (a ROCKNIX override's; the generic recipe `{g}`)" if g and g != v else "")
    return "; ".join(f"{pl} `{v}`" for pl, v in vs.items()) + f" (a ROCKNIX override's case; the generic recipe `{g}`)"

def a_cell(p):
    return {"identical": "identical", "differs": "differs (fork edit)", "absent-upstream": "absent (fork-added)"}[q4a[p]]

def b_cell(p):
    n = name(p); lv = q4b[p]
    if lv == "absent": return "absent"
    if lv == "not-read": return "not read"
    ours, le = (Q / "at-hash" / p).read_text(), le_text(p)
    if n == "harfbuzz-icu": return "inherits harfbuzz (master `" + q4b[N["harfbuzz"]] + "`); recipe identical" if ours == le else "inherits harfbuzz; recipe differs"
    gv = pin_of(p) or ""
    if ours == le: return "`" + (lv[:12] if n in HASH else lv) + "` (identical)" if lv else "no version (identical)"
    if lv == gv: return "`" + (lv[:12] if n in HASH else lv) + "` (same version, recipe differs)"
    return "`" + (lv[:12] if re.fullmatch(r"[0-9a-f]{40}", lv) else lv) + "` (ours `" + gv + "`)"

def c_cell(p):
    n = name(p)
    if p in FORK_ADDED:
        r, l, v = fresh[n]; return f"{v.split(':')[0]} (latest `{l}`)"
    if n in HASH:
        h = hashc[n]
        if h.startswith("unknown"): return "unknown: " + h.split(": ", 1)[1]
        m = re.search(r"\] (\S+) ahead_by=(\d+) behind_by=(\d+)", h); st, ah, bh = m.group(1), int(m.group(2)), int(m.group(3))
        if n == "fuse": return f"the head of `fuse_2_9_bugfix`, the 2.9 series (`master` is {ah} commits ahead and lacks {bh} of the pin's)"
        return "at the default branch's HEAD" if ah == 0 else f"{ah} commits behind the default branch"
    return "not read: follows LibreELEC"

def disp(p):
    n = name(p)
    if p in FORK_ADDED:
        v = fresh[n][2]
        if v.startswith("BEHIND"): return f"fork's: Backlog bump proposed (#839's shape), {fresh[n][0]} -> {fresh[n][1]} ({FIND[n]})"
        if v.startswith("CURRENT"): return "current"
        return v
    lv = q4b[p]
    if n in VIRTUAL: return "follows the base merge; LibreELEC master carries it (no version)"
    if n == "harfbuzz-icu": return "follows the base merge; LibreELEC master inherits harfbuzz `" + q4b[N["harfbuzz"]] + "`"
    lvs = lv[:12] if re.fullmatch(r"[0-9a-f]{40}", lv) else lv
    return f"follows the base merge; LibreELEC master at `{lvs}`" + (f" ({FIND[n]})" if n in FIND else "")

def probe_cell(n):
    code, tgt = head[n]
    if code == "no-url": return "no `PKG_URL` (nothing fetched)"
    if code == "200": return "HEAD 200 (not fetched)"
    if code == "404":
        return "HEAD 404 (a ranged GET too); ROCKNIX's mirror serves the recipe's sha256 (" + FIND[n] + ")"
    f = fetch.get(n, "")
    if f.startswith("sha-match"): r = "fetched: sha256 matches"
    elif n == "libfmt": r = "fetched: `5dea48d1...`, the recipe has none (" + FIND[n] + ")"
    elif f.startswith("fetch-failed"): r = "fetch failed at the target; ROCKNIX's mirror serves the recipe's sha256 (" + FIND[n] + ")"
    else: r = "fetched: " + f
    extra = f"; repository renamed ({RENAMED[n]})" if n in RENAMED else ""
    return f"HEAD {code}; {r}{extra}"

def q6_cell(p):
    r = rows[p]; n = name(p)
    by = r["reachable_by"] or []
    st = [pl for pl in by if n in stamps[pl]]
    s = f"{r['reach']}: {len(by)} plan(s), stamped in {len(st)} of their roots"
    miss = [pl for pl in by if n not in stamps[pl]]
    if miss: s += "; no stamp in " + ", ".join(miss) + (" (virtual: by construction)" if n in VIRTUAL else "")
    if n == "btrfs-progs": s += " (F-11)"
    return s

def q1_cell(p):
    n = name(p); u = eff["GENERIC_X64-x86_64"][n][2]
    out = []
    if u.startswith("http:"): out.append("`PKG_URL` over http (F-14)")
    if n in RENAMED: out.append("`PKG_URL` names a renamed repository (F-15)")
    if n == "oniguruma": out.append("`PKG_URL`'s repository archived since 2025-04 (F-15)")
    if n == "populatefs": out.append("`PKG_URL` names a personal fork of `lipnitsk/populatefs` (F-15)")
    if n in ("libsoup", "ruby"): out.append("`${PKG_VERSION:0:3}` in the URL (F-13)")
    return "; ".join(out) or "none read"

def q2_cell(n):
    return f"`pkgcheck` {pk_tree[n]}, T6's copy {pk_t6[n]}"

def ov_note(p):
    o = over.get(p)
    return (" Sourced by " + ", ".join(f"`{x}`" for x in o) + ".") if o else ""

def q5_cell(p):
    n = name(p)
    if p in FORK_ADDED or p in FORK_EDITED:
        return {"webkitgtk": "`PKG_MAKE_OPTS_TARGET=\"-j4\"` (`:39`), the memory cap; 114 lines; not measured",
                "ruby": "a host build only (`PKG_DEPENDS_HOST`), never on the image; not measured",
                "libyaml": "adds `ccache:host` to the host build's order; not measured",
                "syslinux": "two `cp` lines; not measured"}.get(n, "not measured: no build runs")
    return "n/a: upstream-carried, not measured"

def q7_cell(p):
    if p in FORK_ADDED or p in FORK_EDITED: return "a #645 row (04 § Q7, F-10)"
    if p in over: return "n/a; " + str(len(over[p])) + " ROCKNIX override(s) source it (F-12)"
    return "n/a"

def q3_cell(p):
    n = name(p); s = stamp.get(n, "")
    st = {"match": "cache stamp matches", "no-url": "", "STAMP-DIFFERS": "cache stamp differs (no checksum to match)"}.get(s, s)
    return probe_cell(n) + (("; " + st) if st else "")

if WHAT == "coverage":
    print("| Path | Tier | Reach | Lines | (a) upstream/next | (b) LibreELEC master | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |")
    print("| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in sorted(rows):
        r = rows[p]
        if p.endswith("/package.mk"):
            n = name(p)
            cells = [a_cell(p), b_cell(p), q1_cell(p), q2_cell(n), q3_cell(p), disp(p) + ov_note(p), q5_cell(p), q6_cell(p), q7_cell(p)]
        else:
            le = {"le-identical": "identical"}.get(q4bo.get(p), q4bo.get(p, "not read"))
            na = "n/a: a template or the format reference, not built" if r["reach"] == "n/a" else "n/a: a data file its recipe installs"
            cells = ["identical", le, "none read", "n/a: not a recipe", na, "follows the base merge (byte-identical to both)", "n/a", f"{r['reach']}: with its recipe" if r["reach"] != "n/a" else "n/a: read by people", "n/a"]
        print(f"| `{p}` | {r['tier']} | {r['reach']} | {r['lines']} | " + " | ".join(c.replace("|", "/") for c in cells) + " |")
elif WHAT == "q4":
    print("| Recipe path | Name | Pin (effective) | Shape | (a) upstream/next | (b) LibreELEC master | (c) the project | Disposition (the mover) |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in recipes:
        n = name(p)
        print(f"| `{p}` | `{n}` | {pin_cell(n)} | {shape(n)} | {a_cell(p)} | {b_cell(p)} | {c_cell(p)} | {disp(p)} |")
elif WHAT == "q4json":
    out = {"read_hash": "8ebaf8daad", "upstream_ref": "upstream/next e0f9deb899", "libreelec_ref": "LibreELEC/LibreELEC.tv master (contents API, 2026-10-24 10:15-10:19 UTC)", "rows": []}
    for p in recipes:
        n = name(p)
        out["rows"].append({"recipe": n, "path": p, "shape": shape(n),
            "pin": {pl: eff[pl][n][0] for pl in PLANS}, "sha256": {pl: eff[pl][n][1] for pl in PLANS}, "url": eff["GENERIC_X64-x86_64"][n][2],
            "a": q4a[p], "b_libreelec_version": q4b[p], "b_recipe_identical": (le_text(p) == (Q / "at-hash" / p).read_text()) if le_text(p) else None,
            "c": c_cell(p), "head_probe": head[n][0], "redirect": head[n][1].split("?", 1)[0],   # a signed redirect's query is a credential-shaped, expiring token: kept out "fetch": fetch.get(n, ""), "cache_stamp": stamp.get(n, ""),
            "sourced_by": over.get(p, []), "disposition": disp(p)})
    print(json.dumps(out, indent=1))
elif WHAT == "q7":
    REASON = {
     "brotli": ("move to `projects/ROCKNIX/packages/compress/brotli`", "the sign-in window's chain (#576, woff2's dependency); no upstream copy, so the move shadows nothing"),
     "ruby": ("move to `projects/ROCKNIX/packages/devel/ruby`", "a host interpreter only WebKit's generators need (#576); no upstream copy"),
     "unifdef": ("move to `projects/ROCKNIX/packages/devel/unifdef`", "a host tool only WebKit's build needs (#576); no upstream copy"),
     "openjpeg": ("move to `projects/ROCKNIX/packages/graphics/openjpeg`", "WebKit's JPEG 2000 decoder (#576); no upstream copy"),
     "woff2": ("move to `projects/ROCKNIX/packages/graphics/woff2`, with its `patches/`", "WebKit's web-font decoder (#576); the patch moves with it (#645's 21 files count it)"),
     "glib-networking": ("move to `projects/ROCKNIX/packages/network/glib-networking`", "libsoup's TLS backend (#576); no upstream copy"),
     "libtasn1": ("move to `projects/ROCKNIX/packages/security/libtasn1`", "WebKit's ASN.1 parser (#576); no upstream copy"),
     "dmidecode": ("move to `projects/ROCKNIX/packages/sysutils/dmidecode`", "GENERIC_X64's hardware report (`test` reach); no upstream copy"),
     "qrencode": ("move to `projects/ROCKNIX/packages/sysutils/qrencode`", "the cloud setup's QR code (shipped); no upstream copy"),
     "ryzenadj": ("move to `projects/ROCKNIX/packages/sysutils/ryzenadj`", "GENERIC_X64's power tool (`test` reach); no upstream copy"),
     "libpsl": ("move to `projects/ROCKNIX/packages/web/libpsl`", "libsoup's cookie scoping (#576); no upstream copy"),
     "libsoup": ("move to `projects/ROCKNIX/packages/web/libsoup`", "WebKit's network backend (#576); no upstream copy"),
     "webkitgtk": ("move to `projects/ROCKNIX/packages/web/webkitgtk`, with its two `patches/`", "the sign-in window (#576); the patches move with it"),
     "libyaml": ("propose the hunk to ROCKNIX through #585 (a `PKG_DEPENDS_HOST=\"ccache:host\"` line on the generic recipe), else a `projects/ROCKNIX/packages/.../libyaml` override that sources the generic and adds the line", "a cold-tree ordering fix (`071fef34ed`); only `ruby:host` needs `libyaml:host`, and ruby is the fork's, so the override is the fallback"),
     "libsamplerate": ("propose the hunk to ROCKNIX through #585 (`--with-pic`), else a ROCKNIX override that sources the generic and appends the option", "a one-option build fix; LibreELEC master is the same version without it"),
     "syslinux": ("propose the hunk to ROCKNIX through #585 (the two `ldlinux.c32` lines), else a `projects/ROCKNIX/packages/tools/syslinux` override", "GENERIC_X64's BIOS boot (`a6b28a469f`, `test` reach); syslinux 6.x needs `ldlinux.c32` beside the loader"),
    }
    assert set(REASON) == {name(p) for p in FORK_ADDED | FORK_EDITED}
    print("| # | Path | Provenance | Proposed disposition for #645 | Reason |")
    print("| ---: | --- | --- | --- | --- |")
    for i, p in enumerate(sorted(FORK_ADDED | FORK_EDITED), 1):
        n = name(p); d, why = REASON[n]
        print(f"| {i} | `{p}` | {'added by the fork, absent upstream' if p in FORK_ADDED else 'upstream recipe the fork edited'} | {d} | {why} |")
else:
    sys.exit("coverage|q4|q4json|q7")

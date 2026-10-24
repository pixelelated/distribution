#!/usr/bin/env python3
"""T8's tables (#655), from the § 5 results under .qa-scratch/t8/, so 02's
coverage table, 04's Q4 currency table, q4-pins.json, the orphan table and
the conflict list cannot disagree.

    python3 -I t8-tables.py <worktree> coverage|q4|q4json|orphans|conflicts > out

Asserts 485 paths and 260 recipes, and that each result file covers every
recipe it should, so a missing line fails here rather than printing an empty
cell.
"""
import json, re, sys, collections, subprocess
from pathlib import Path

T = Path(sys.argv[1]); WHAT = sys.argv[2]; Q = T / ".qa-scratch/t8"
inv = json.load(open(T / "docs/reviews/inventory.json")); cols = inv["columns"]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
rows = {r["path"]: r for r in (dict(zip(cols, x)) for x in inv["rows"])
        if r["tree"] == "distribution" and r["area"] == "generic-packages"
        and gm(r["path"], "projects/ROCKNIX/**") and not gm(r["path"], "projects/ROCKNIX/packages/virtual/emulators/**")
        and r["reach"] in ("shipped", "test", "n/a")}
assert len(rows) == 485, len(rows)
recipes = sorted(p for p in rows if p.endswith("/package.mk")); assert len(recipes) == 260
name = lambda p: p.split("/")[-2]
N = {name(p): p for p in recipes}; assert len(N) == 260
short = lambda p: p.replace("projects/ROCKNIX/packages/", "")
def lines(f): return [l for l in (Q / f).read_text().splitlines() if l.strip()]
def git(*a): return subprocess.run(["git", "-C", str(T), *a], capture_output=True, text=True).stdout

q4a = {}
for l in lines("q4a.txt"):
    st, p = l.split(" ", 1); q4a[p] = st
assert set(q4a) == set(rows)
PLANS = ["GENERIC_X64", "H700", "SM8550"]
eff = collections.defaultdict(dict)
for l in lines("effective.txt"):
    m = re.match(r"(\S+) (\S+) version=\[([^]]*)\] sha=\[([^]]*)\] shaset=(\S*) arch=\[([^]]*)\] url=\[([^]]*)\]", l)
    pl, n, v, s, ss, a, u = m.groups(); eff[n][pl] = dict(v=v, s=s, ss=ss, a=a, u=u)
assert set(eff) == set(N) and all(len(eff[n]) == 3 for n in N)
upd = set(lines("update-set-RK3588.txt")); block = set(l.split()[0] for l in lines("blocklist.txt"))
fresh = {}
for l in lines("q4c.txt")[1:]:   # fixed-width columns: %-26s %-14s %-14s %s; a long name pushes the rest right
    m = re.match(r"(\S+)\s+(.*)$", l); n, rest = m.group(1), m.group(2)
    v = re.search(r"(CURRENT|BEHIND|PINNED|UNKNOWN|INHERITED|LOCAL|AHEAD).*$", rest).group(0)
    pre = rest[:rest.index(v)].split(); fresh[n] = (pre[0] if pre else "", pre[1] if len(pre) > 1 else "", v)
hashc = {}
for l in lines("q4c-hash.txt"):
    n, rest = l.split(" ", 1); hashc[n] = rest
head = {}
for l in lines("probe/head.txt"):
    f = l.split(" "); head[f[0]] = (f[1], f[2] if len(f) == 5 else "")
fetch = {l.split()[0]: l.split(" ", 1)[1] for l in lines("probe/fetch.txt")}
git_ok = {l.split()[0]: l for l in lines("probe/git.txt")}
pk_tree = {}; pk_t6 = {}
for f, d in (("pkgcheck-pkgcheck.txt", pk_tree), ("pkgcheck-pkgcheck-t6.txt", pk_t6)):
    for l in lines(f):
        w = l.split(); d[w[-1] if w[0] == "PASS" else w[2]] = w[0]
assert set(pk_tree) == set(N) and set(pk_t6) == set(N)
stamped = {l.split()[1]: l.split()[0] == "1" for l in lines("record-stamps.txt")}
bashn = {l[3:] if l.startswith("ok ") else l.split(" ", 2)[1]: l.split(" ")[0] for l in lines("bashn.txt")}
units = set(lines("units.txt"))
unit_absent = collections.defaultdict(list)
for l in lines("units-exec.txt"):
    if l.startswith("ABSENT"):
        m = re.match(r"ABSENT (\S+)\s+\((.*)\)", l); unit_absent["projects/ROCKNIX/packages/" + m.group(2)].append(m.group(1))
conf = lines("conflicts.txt")
mt = (Q / "base-merge.txt").read_text()
def conflict_kind(p):
    for l in mt.splitlines():
        if l.startswith("CONFLICT") and p in l: return re.match(r"CONFLICT \(([^)]*)\)", l).group(1)
    return "auto-merges"
forklog = {}
for l in lines("fork-log.txt"):
    m = re.match(r"(\S) (.*?) :: (.*)", l); forklog["projects/ROCKNIX/packages/" + m.group(2)] = m.group(3).split("|")[0]
fork_own = {p for p, r in rows.items() if r["tier"] == "fork-own"}; assert len(fork_own) == 35
sourcing = set(lines("sourcing-true.txt")); assert len(sourcing) == 43
orph = sorted(p for p in recipes if q4a[p] == "orphan"); assert len(orph) == 11
addd = sorted(p for p in recipes if q4a[p] == "fork-added"); assert len(addd) == 7
UNBUILT = {"arm", "debug", "es-themes", "gamesupport", "image", "initramfs", "libc", "linux-drivers", "linux-firmware", "network", "swaywm-env", "synctools", "qcom-abl"}
MIRROR = {"libaio": "716c7059...", "rocknix-abl": "64034fb0...", "samba": "09bb56db..."}
FIND = {"simple-http-server": "F-01, #890", "image": "F-02, #852", "libaio": "F-03", "rocknix-abl": "F-04",
        "cairo": "F-05", "glslang": "F-11", "spirv-tools": "F-11"}
SHORTPIN = {n for n in N if re.fullmatch(r"[0-9a-f]{7,39}", eff[n]["GENERIC_X64"]["v"])}
ORPH_USE = {
 "libfreeaptx": ("its own `PKG_SHA256` over the generic URL", "0.2.2", "0.2.2"),
 "opus": ("1.5.2 over the generic 1.6.1, from a xiph mirror", "1.5.2", "1.6.1"),
 "libfmt": ("9.1.0 on every plan but SM's (#877)", "9.1.0 / 12.2.0", "12.2.0"),
 "glslang": ("16.6.0, the fork's own bump (`b4fc2a28cf`); spirv-tools' pin follows its `known_good.json`", "16.6.0", "16.5.0"),
 "vulkan-headers": ("ROCKNIX's own copy", "1.4.347", "1.4.359"),
 "cargo": ("ROCKNIX's own copy", "1.94.1", "$(get_pkg_version rust)"),
 "miniupnpc": ("ROCKNIX's own copy", "2.3.3", "2.3.3"),
 "rocknix-abl": ("SM8550's bootloader payload (`9aa7affee9`, #600)", "1.2", "none: replaced by `openabl` (`71d8932b33`)"),
 "tllist": ("ROCKNIX's own copy", "1.1.0", "1.1.0"),
 "mtdev": ("ROCKNIX's own copy", "1.1.6", "1.1.7"),
 "swaybg": ("ROCKNIX's own copy", "1.2.1", "1.2.2"),
}
CONF_DISP = {
 "apps/gamescope/package.mk": ("auto-merges", "different, keep ours: upstream bumps the pin to `6867f509...` (3.16.31), ours adds the glm/stb packages; the wraps at both commits name the same revisions, so the auto-merge builds (`:55` would stop it otherwise)"),
 "graphics/cairo/package.mk": ("content", "conflict: upstream's is a sourcing override too; take its shape, keep ours' xcb/xlib-xcb options; the version line becomes the generic's"),
 "graphics/glslang/package.mk": ("modify/delete", "conflict: upstream deleted it (the generic is 16.5.0); ours is 16.6.0 and `spirv-tools` follows 16.6.0's `known_good.json` -- taking the deletion downgrades glslang under spirv-tools (F-11)"),
 "graphics/spirv-tools/package.mk": ("content", "conflict: upstream made it a sourcing override; ours pins `ef96ed76...` to glslang 16.6.0 with a GCC 12 diagnostic; resolve with glslang (F-11)"),
 "lang/gcc/package.mk": ("content", "conflict: ours enables libatomic for x86_64; upstream restructured it for aarch64 only and dropped the 15.2.0 hold (the generic is 16.2.0); keep the x86_64 case and decide the hold"),
 "misc/modules/sources/gamelist.xml": ("auto-merges", "different, keep ours: ours rewrites descriptions (identity); upstream removes the AetherSX2 entry"),
 "multimedia/gstreamer/gst-plugins-base/package.mk": ("content", "conflict: both enable GL; ours keeps the install WebKit needs (#228); take upstream's GLES/EGL options and keep ours' install"),
 "multimedia/gstreamer/gstreamer/package.mk": ("add/add", "conflict: added on both sides; ours enables the plugin registry WebKit needs, upstream's removes `/usr/share`; keep ours, check upstream's removal against the registry"),
 "network/networkmanager/config/NetworkManager.conf": ("content", "same change: both add `hostname-mode=none`; drop ours' comment-only hunk"),
 "tools/rocknix-abl/package.mk": ("modify/delete", "conflict: upstream replaced it with `openabl`; ours carries the v1.2 checksum fix; take the deletion and check SM8550's bootloader against `openabl`"),
 "wayland/compositor/sway/autostart/111-sway-init": ("content", "different, keep ours: ours adds the virtio `Virtual` connector and the software cursor (GENERIC_X64); upstream adds essway masking, AFBC and the Duo Lite case; both"),
}
assert {short(p) for p in conf} == set(CONF_DISP)

def pin_cell(n):
    vs = {pl: eff[n][pl]["v"] for pl in PLANS}
    f = lambda v: "-" if not v else "`" + (v[:12] if re.fullmatch(r"[0-9a-f]{13,40}", v) else v) + "`"
    return f(vs["GENERIC_X64"]) if len(set(vs.values())) == 1 else "; ".join(f"{pl} {f(v)}" for pl, v in vs.items())
def shape(n):
    p = N[n]; v = eff[n]["GENERIC_X64"]["v"]
    if n in UNBUILT and not eff[n]["GENERIC_X64"]["u"]: return "virtual (no source)" if n != "qcom-abl" else "local payload (no `PKG_URL`)"
    if p in sourcing: return "sourcing override" + (" (sets its own pin)" if n in ("opus", "gcc", "libfmt") else "")
    if re.fullmatch(r"[0-9a-f]{7,40}", v): return "hash" + (" (short)" if n in SHORTPIN else "")
    return "version"
def a_cell(p):
    return {"identical": "identical", "differs": "differs", "orphan": "absent: orphan", "fork-added": "absent: fork-added"}[q4a[p]]
def upd_cell(n):
    if n not in upd: return "-"
    return "in the set, blocklisted" if n in block else "in the set (never run)"
def c_cell(n):
    p = N[n]
    if n in fresh and (p in fork_own or q4a[p] in ("orphan", "fork-added")):
        r, l, v = fresh[n]; return f"{v.split(':')[0].split(' (')[0]} (latest `{l}`)" if l else v.split(" (")[0]
    if n == "cairo": return "BEHIND (latest `1.18.6`, cairographics.org's listing)"
    if n in hashc:
        h = hashc[n]
        if h.startswith("unknown"): return "unknown: " + h.split(": ", 1)[1]
        m = re.search(r"\] (\S+) ahead_by=(\d+) behind_by=(\d+)", h)
        if not m: return "unknown: compare found no common ancestor"
        st, ah, bh = m.group(1), int(m.group(2)), int(m.group(3))
        if ah == 0: return "at the default branch's HEAD"
        return f"{ah} behind the default branch" + (f", {bh} not on it" if bh else "")
    if q4a[p] == "orphan": return "replaced upstream: " + ORPH_USE[n][2]
    if p in fork_own: return "not read: the tool lists only recipes added since the base"
    return "not read: follows the base merge"
def disp(n):
    p = N[n]; s = short(p)
    if n == "simple-http-server": return "#890: filed and fixed in a packet ahead of T5 (`fix-tree`); follows the base merge"
    if q4a[p] == "orphan":
        k = CONF_DISP.get(s, ("", ""))[0]
        return (f"orphan, a {k} conflict at the base merge: " if k else "orphan: ") + f"dropped by the base merge; the fork used it for {ORPH_USE[n][0]}; after it, {ORPH_USE[n][2]}; dependants resolve by name" + (f" ({FIND[n]})" if n in FIND else "")
    if s in CONF_DISP:
        k, d = CONF_DISP[s]; r = (f"conflict at the base merge ({k}): " if k != "auto-merges" else "follows the base merge (auto-merges): ") + d
        return r + ("; and fork's: Backlog bump proposed (#839's shape), 1.18.4 -> 1.18.6 (F-05)" if n == "cairo" else "")
    if n in fresh and q4a[p] == "fork-added":
        v = fresh[n][2]
        if v.startswith("CURRENT"): return "current"
        if v.startswith("PINNED"): return "pinned on purpose: " + v.split("PINNED: ", 1)[1].split(" (")[0]
        if v.startswith("INHERITED"): return "follows the generic recipe's pin (T7's row); the override adds options"
        return "unknown: " + v
    if n == "cairo": return "fork's: Backlog bump proposed (#839's shape), 1.18.4 -> 1.18.6 (F-05)"
    if n == "rocknix-splash": return "current"
    if n in upd and n not in block: return "make update's: moves to its branch head if run (never run); otherwise follows the base merge"
    if q4a[p] == "identical": return "follows the base merge (identical to `upstream/next`)" + (f" ({FIND[n]})" if n in FIND else "")
    uv = git("show", f"upstream/next:{p}")
    m = re.search(r'^\s*PKG_VERSION="([^"]*)"', uv, re.M)
    hv = eff[n]["GENERIC_X64"]["v"]
    if m and m.group(1) and m.group(1) != hv and not m.group(1).startswith("$"):
        return f"follows the base merge: upstream's pin `{m.group(1)[:12]}`" + (f" ({FIND[n]})" if n in FIND else "")
    return "follows the base merge: upstream changed the recipe, not its top-level pin" + (f" ({FIND[n]})" if n in FIND else "")
def probe_cell(n):
    if n not in head:
        if any(e["u"] and (e["u"].endswith(".git") or e["u"].startswith("git")) for e in eff[n].values()):
            return "git fetch: `ls-remote` answers" if n in git_ok else "git fetch"
        return "no `PKG_URL`"
    code, tgt = head[n]
    if code == "200": return "HEAD 200"
    if code == "404": return f"HEAD 404; the mirror serves the recipe's sha256 ({MIRROR[n]}, {FIND[n]})"
    if code == "000": return "no answer on two reads, 200 on a third; the mirror serves the recipe's sha256"
    f = fetch.get(n, "")
    if f.startswith("sha-match"): return f"HEAD {code}; fetched: sha256 matches"
    if f.startswith("NO-SHA"): return f"HEAD {code}; fetched `{f.split('=')[1][:8]}...` against no checksum" + (" (F-01, #890)" if n == "simple-http-server" else " (#877)" if n == "libfmt" else " (T5's E6, unmerged here)")
    return f"HEAD {code}; " + (f or "not fetched")

def rcells(p):
    n = name(p); r = rows[p]
    q1 = []
    if eff[n]["GENERIC_X64"]["u"].startswith("http:"): q1.append("`PKG_URL` over http")
    if q4a[p] == "orphan": q1.append("an orphan: upstream moved on (Q4)")
    q2 = f"`pkgcheck` {pk_tree[n]}, T6's {pk_t6[n]}" + (" (parser: functions in if/else, #657)" if n == "moonlight" else " (parser, #657)" if n == "wireplumber" else " (#852)" if n == "image" else "") + (" ; a short hash pin (F-07)" if n in SHORTPIN else "")
    q3 = probe_cell(n) + ("; writes at load (F-02, #852)" if n == "image" else "")
    q5 = "not measured: no build runs" if p in fork_own else "n/a: upstream-carried, not measured"
    by = r["reachable_by"] or []
    q6 = f"{r['reach']}: {len(by)} plan(s); stamped" + ("" if stamped.get(n) else "; NO STAMP") + ("; no build directory, by construction (virtual)" if n in UNBUILT and n != "qcom-abl" else "; no build directory: SM8550's plan builds it, local payload" if n == "qcom-abl" else "")
    q7 = ("fork-own: " + forklog.get(p, "-")[:90]) if p in fork_own else ("a sourcing override" if p in sourcing else "n/a")
    return [a_cell(p), "; ".join(q1) or "none read", q2, q3, disp(n), q5, q6, q7]
def ocells(p):
    r = rows[p]; s = short(p)
    q2 = []
    if p in bashn: q2.append(f"`bash -n` {bashn[p]}")
    if p in units: q2.append("`systemd-analyze verify`: host-only unresolved names, no directive warning")
    q3 = []
    if p in unit_absent: q3.append("Exec path absent from the GENERIC_X64 image: " + ", ".join(f"`{x}`" for x in unit_absent[p]) + (" (F-10)" if "xorg-configure" in s else " (device-scoped: present on its plan's image)" if any(k in s for k in ("batteryplus", "inputplumber")) else " (on /storage by design)"))
    if s.endswith("97-xorg.rules"): q3.append("wants `xorg-configure@<drv>`, whose script no image installs (F-10)")
    disp_ = ("conflict at the base merge (" + CONF_DISP[s][0] + "): " + CONF_DISP[s][1]) if s in CONF_DISP else {"identical": "follows the base merge (identical)", "differs": "follows the base merge: upstream changed it", "orphan": "orphan: dropped with its recipe", "fork-added": "fork-added: stays (no upstream copy)"}[q4a[p]]
    q6 = f"{r['reach']}: with its recipe" if r["reach"] != "n/a" else "n/a: installed by its recipe's GENERIC_X64 branch"
    q7 = ("fork-own: " + forklog.get(p, "-")[:90]) if p in fork_own else "n/a"
    return [a_cell(p), "none read", "; ".join(q2) or "n/a: data", "; ".join(q3) or "n/a: a file its recipe installs", disp_, "n/a", q6, q7]

if WHAT == "coverage":
    print("| Path | Tier | Reach | Lines | (a) upstream/next | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |")
    print("| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in sorted(rows):
        r = rows[p]; c = rcells(p) if p.endswith("/package.mk") else ocells(p)
        print(f"| `{p}` | {r['tier']} | {r['reach']} | {r['lines']} | " + " | ".join(x.replace("|", "/") for x in c) + " |")
elif WHAT == "q4":
    print("| Recipe path | Name | Pin (effective: GENERIC_X64, H700, SM8550) | Shape | (a) upstream/next | make update | (c) the project | Disposition (the mover) |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in recipes:
        n = name(p); print(f"| `{p}` | `{n}` | {pin_cell(n)} | {shape(n)} | {a_cell(p)} | {upd_cell(n)} | {c_cell(n)} | {disp(n).replace('|', '/')} |")
elif WHAT == "q4json":
    out = {"read_hash": "8ebaf8daad", "upstream_ref": "upstream/next e0f9deb899", "base": "c445081a59", "rows": []}
    for p in recipes:
        n = name(p)
        out["rows"].append({"recipe": n, "path": p, "shape": shape(n), "effective": {pl: {k: eff[n][pl][k] for k in ("v", "s", "a", "u")} for pl in PLANS},
            "a": q4a[p], "make_update": upd_cell(n), "c": c_cell(n), "head_probe": head.get(n, ("", ""))[0], "redirect": head.get(n, ("", ""))[1].split("?", 1)[0],
            "fetch": fetch.get(n, ""), "pkgcheck": [pk_tree[n], pk_t6[n]], "stamped": stamped.get(n), "fork_own": p in fork_own, "disposition": disp(n)})
    print(json.dumps(out, indent=1))
elif WHAT == "orphans":
    print("| # | Orphan | What the fork used it for | Effective now | After the base merge | Upstream's deleting commit | Fork-own dependants |")
    print("| ---: | --- | --- | --- | --- | --- | --- |")
    for i, p in enumerate(orph, 1):
        n = name(p); use, now, after = ORPH_USE[n]
        d = git("log", "--format=%h %as", "--diff-filter=D", "-1", "c445081a59..upstream/next", "--", p).strip()
        deps = [x for x in git("grep", "-l", "-w", "-E", rf"PKG_DEPENDS_[A-Z]+=.*\b{re.escape(n)}\b", "8ebaf8daad", "--", "projects/ROCKNIX").split("\n") if x and f"/{n}/package.mk" not in x]
        fo = [short(x.split(":", 1)[1]) for x in deps if x.split(":", 1)[1] in fork_own]
        print(f"| {i} | `{short(p)}` | {use} | `{now}` | {after} | `{d}` | {', '.join('`'+x+'`' for x in fo) or 'none'} (by name: {len(deps)} recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |")
elif WHAT == "conflicts":
    print("| # | Path | `merge-tree` | Disposition |")
    print("| ---: | --- | --- | --- |")
    for i, p in enumerate(conf, 1):
        s = short(p); k, d = CONF_DISP[s]
        assert conflict_kind(p) == k, (p, conflict_kind(p), k)
        print(f"| {i} | `{s}` | {k} | {d} |")
else:
    sys.exit("coverage|q4|q4json|orphans|conflicts")

#!/usr/bin/env python3
"""T25 (#672): the reachability tables, regenerated from the tree, never typed.

    python3 -I -B docs/audits/2026_10_25-epic-m6-devices-unshipped/tools/t25-tables.py <section>
    python3 -I -B .../t25-tables.py write <file>   # refresh every generated block in <file>
    python3 -I -B .../t25-tables.py check <file>   # exit 1 when a block differs from a fresh run

Sections: coverage (397), units (25), targets (12), projects (9), pins (10 +
2 cited), trees (53), q6 (25 dispositions), q7 (the duplicate map), edges (the
build-and-unpack edge sweep over the 52 recipes), counts.

Run from the worktree root.
Inputs:
- `.qa-scratch/t25/rows.tsv`, brief section 2's block output: reach, tier,
  lines, language, buildable_by, shadowed_by and path, read from
  `docs/reviews/inventory.json`;
- the inventory itself, for the override directories' reach;
- local git reads at `8ebaf8daad` (the read hash), `651150fc88` (the upstream
  head, by name) and `c445081a59` (the base).

No fetch, no network, no plan generation, no build. Each section asserts its
row count and no empty cell, so a short table fails instead of printing.
"""
import collections
import json
import re
import subprocess
import sys

H, U, BASE = "8ebaf8daad", "651150fc88", "c445081a59"
S = ".qa-scratch/t25"
TARGETS = ["AMD64", "RK3326", "RK3399", "RK3566", "RK3576", "RK3588", "S922X",
           "SM4450", "SM6115", "SM8250", "SM8650", "SM8750"]
FIRST_WIDENING = {"RK3566", "RK3326"}          # D-WORKFLOW-185
PROJECTS = ["ARM", "Allwinner", "Amlogic", "Generic", "NXP", "Qualcomm", "RPi",
            "Rockchip", "Samsung"]
DRIVERS = "projects/ROCKNIX/packages/{linux-drivers,linux-firmware}"
KERNEL = "projects/ROCKNIX/packages/linux/package.mk"
# F-01: the kernel recipe unpacks intel-ucode on x86_64 (:69-72) and copies its
# build dir into the built-in firmware (:202); the inventory's plan-derived
# buildable_by does not see an unpack edge. get_pkg_directory (config/functions
# :789-798, :1057-1079) resolves the device copy for AMD64 and the generic copy
# for GENERIC_X64, which has no override.
UNPACK_EDGE = {
    "projects/ROCKNIX/devices/AMD64/packages/intel-ucode/": ("AMD64", "unshipped"),
    "packages/linux-firmware/intel-ucode/": ("GENERIC_X64", "test"),
}
# F-01's second instance: the same recipe compiles generic-dsi's source for
# RK3326, RK3566 and RK3576 (:108-111) and unpacks it for the first two
# (:81-82); the inventory's buildable_by lists RK3326 alone. Reach unchanged.
EXTRA_TARGETS = {
    "projects/ROCKNIX/packages/linux-drivers/generic-dsi/": ["RK3326", "RK3566", "RK3576"],
}
# Every edge into a slice recipe from a shipped or test file, and which copy it
# resolves to (local before global, config/functions:789-798). A new reached
# edge fails the edges section until it is read and named here.
EDGE_NOTE = {
    "dmidecode": "x86_64 only (`virtual/image/package.mk:73`): AMD64 resolves its device copy, GENERIC_X64 the generic `packages/sysutils/dmidecode`",
    "ryzenadj": "x86_64 only (`virtual/image/package.mk:73`): AMD64 resolves its device copy, GENERIC_X64 the generic `packages/sysutils/ryzenadj`",
    "pciutils": "x86_64 only (`linux/package.mk:69-70`): AMD64 resolves its device copy, GENERIC_X64 the generic `packages/sysutils/pciutils`",
    "generic-dsi": "RK3326 and RK3566 unpack (`:81-82`); RK3326, RK3566 and RK3576 compile its source (`:108-111`); no shipped device: F-01's second instance",
    "intel-ucode": "x86_64 unpack (`:69-72`) and copy (`:202`): AMD64 resolves its device copy, GENERIC_X64 the generic copy, which the inventory calls unreached: F-01",
    "kernel-firmware": "resolves to the override `projects/ROCKNIX/packages/linux-firmware/kernel-firmware` (local first); the generic copy stays shadowed",
    "linux": "resolves to the override `projects/ROCKNIX/packages/linux` (local first); the generic copy stays shadowed",
    "mkbootimg": "`SM*` only (`linux/package.mk:19`): resolves to `projects/ROCKNIX/packages/tools/mkbootimg`; `projects/Qualcomm` is never on the search path (no target sets `PROJECT=Qualcomm`)",
}


def git(*a):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"t25-tables: git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout


def show(path, rev=H):
    return git("show", f"{rev}:{path}")


def load_rows():
    rows = []
    for line in open(f"{S}/rows.tsv"):
        reach, tier, lines, lang, bb, sh, path = line.rstrip("\n").split("\t")
        rows.append(dict(reach=reach, tier=tier, lines=0 if lines == "None" else int(lines),
                         lang=lang, bb=eval(bb, {}), shadow=None if sh == "None" else sh, path=path))
    assert len(rows) == 397, len(rows)
    return rows


def unit_of(p):
    s = p.split("/")
    if p.startswith("projects/ROCKNIX/devices/"):
        return "/".join(s[:4])
    if p.startswith("projects/ROCKNIX/packages/"):
        return DRIVERS
    return "/".join(s[:2])


UNIT_ORDER = ([f"projects/ROCKNIX/devices/{t}" for t in TARGETS] + [DRIVERS]
              + [f"projects/{p}" for p in PROJECTS]
              + ["packages/linux", "packages/linux-driver-addons", "packages/linux-firmware"])


def makefile():
    mk = show("Makefile").splitlines()
    world = next(l for l in mk if l.startswith("world:")).split()[1:]
    line = {l.split(":")[0]: i + 1 for i, l in enumerate(mk) if re.match(r"^[A-Z0-9_]+:\s*$", l)}
    return line, set(world)


def inventory_reach():
    inv = json.load(open("docs/reviews/inventory.json"))
    c = inv["columns"]
    return [dict(zip(c, r)) for r in inv["rows"] if r[c.index("tree")] == "distribution"]


def drift(paths):
    out = git("diff", "--name-status", U, H, "--", *paths)
    st = {}
    for l in out.splitlines():
        k, p = l.split("\t", 1)
        st[p.split("\t")[-1]] = k
    return st


def sizes(paths):
    b = {}
    for l in git("ls-tree", "-r", "-l", H, "--", *paths).splitlines():
        meta, p = l.split("\t", 1)
        b[p] = int(meta.split()[3]) if meta.split()[3] != "-" else 0
    return b


def targets_of(bb):
    return sorted({x.rsplit("-", 1)[0] for x in bb})


def override_reach(inv, o):
    rs = [r["reach"] for r in inv if r["path"].startswith(o.rstrip("/") + "/")]
    assert rs, o
    return "reached" if any(x in ("shipped", "test") for x in rs) else "unshipped"


def reach_read(r, mkline, world):
    p = r["path"]
    for pre, (t, kind) in UNPACK_EDGE.items():
        if p.startswith(pre):
            return (f"inventory `unreached`, `buildable_by []`; but `{KERNEL}:71` unpacks `intel-ucode` "
                    f"on x86_64 and `:202` copies it into the kernel's firmware; resolved for {t} "
                    f"(`config/functions:789-798`): F-01")
    if p.startswith("projects/ROCKNIX/devices/"):
        t = p.split("/")[3]
        return (f"`Makefile:{mkline[t]}` `{t}:`; `world` {'yes' if t in world else 'no'}; "
                f"`buildable_by` {len(r['bb'])} ({', '.join(sorted(set(x.rsplit('-', 1)[1] for x in r['bb'])))})")
    for pre, ts in EXTRA_TARGETS.items():
        if p.startswith(pre):
            return (f"`buildable_by` {', '.join(targets_of(r['bb']))}; but `{KERNEL}:81-82` unpacks it for RK3326 and "
                    f"RK3566 and `:108-111` compiles its source for {', '.join(ts)}: F-01")
    if p.startswith("projects/ROCKNIX/packages/"):
        if not r["bb"]:
            return "`buildable_by []`; no edge from a reached file (`edges`)"
        return f"`buildable_by` {', '.join(targets_of(r['bb']))}"
    if p.startswith("projects/"):
        pr = p.split("/")[1]
        s = f"no target sets `PROJECT={pr}` (27 `PROJECT=` lines, all ROCKNIX); engine: § The projects"
        if r["shadow"]:
            s += f"; `shadowed_by {r['shadow']}`"
        return s
    s = "`buildable_by []`; no edge from a reached file (`edges`)"
    if r["shadow"]:
        s = f"`buildable_by []`; `shadowed_by {r['shadow']}` (resolved first, `config/functions:789-798`)"
    return s


def disposition(r, world, inv):
    p = r["path"]
    for pre, (t, kind) in UNPACK_EDGE.items():
        if p.startswith(pre):
            if kind == "test":
                return "reached after all: the test image (GENERIC_X64), through the kernel's unpack edge (F-01)"
            return f"unshipped: target {t}, in world {'yes' if t in world else 'no'} (through the kernel's unpack edge, F-01)"
    if p == "packages/linux/package.mk":
        return (f"shadowed copy, override {r['shadow']}, override {override_reach(inv, r['shadow'])}; "
                "fork-own edit in a shadowed dead copy; Already written: nothing inherited")
    if r["shadow"]:
        return f"shadowed copy, override {r['shadow']}, override {override_reach(inv, r['shadow'])}"
    if r["reach"] == "unshipped":
        ts = [p.split("/")[3]] if p.startswith("projects/ROCKNIX/devices/") else targets_of(r["bb"])
        ts = next((v for k, v in EXTRA_TARGETS.items() if p.startswith(k)), ts)
        if set(ts) <= FIRST_WIDENING:
            return "unshipped: first widening, held (D-WORKFLOW-185)"
        s = f"unshipped: target {', '.join(ts)}, in world {'yes' if all(t in world for t in ts) else 'no'}"
        if set(ts) & FIRST_WIDENING:
            s += f" ({', '.join(sorted(set(ts) & FIRST_WIDENING))} the first widening, held)"
        return s
    return "dead, upstream-carried (#346's class)"


def table(head, rows, align=None):
    for r in rows:
        assert len(r) == len(head) and all(str(x).strip() for x in r), r
    out = ["| " + " | ".join(head) + " |",
           "| " + " | ".join(align or ["---"] * len(head)) + " |"]
    out += ["| " + " | ".join(str(x).replace("|", "\\|") for x in r) + " |" for r in rows]
    return "\n".join(out)


def sec_coverage():
    rows, inv = load_rows(), inventory_reach()
    mkline, world = makefile()
    st = drift([r["path"] for r in rows])
    body = []
    for r in rows:
        d = {"M": "differs (M)", "D": "absent upstream (D)", "A": "absent upstream"}.get(st.get(r["path"]), "identical")
        body.append([f"`{r['path']}`", f"`{unit_of(r['path']).split('/', 1)[1]}`", r["tier"], r["reach"],
                     r["lines"] if r["lines"] else "—", r["lang"], reach_read(r, mkline, world), d,
                     disposition(r, world, inv), "tree"])
    assert len(body) == 397
    return table(["Path", "Unit", "Tier", "Reach (inventory)", "Lines", "Language", "Reach read",
                  f"At `{U}`", "Disposition", "proved"], body,
                 ["---", "---", "---", "---", "---:", "---", "---", "---", "---", "---"])


def per_unit():
    rows = load_rows()
    g = collections.defaultdict(list)
    for r in rows:
        g[unit_of(r["path"])].append(r)
    assert list(g) and set(g) == set(UNIT_ORDER), sorted(set(g) ^ set(UNIT_ORDER))
    return g


def sec_units():
    g = per_unit()
    allp = [r["path"] for rs in g.values() for r in rs]
    st, b = drift(allp), sizes(allp)
    body = []
    for u in UNIT_ORDER:
        rs = g[u]
        ps = [r["path"] for r in rs]
        reach = dict(collections.Counter(r["reach"] for r in rs))
        newest = git("log", "-1", "--format=%h %ad", "--date=short", U, "--", *ps).strip()
        fork = len(git("log", "--no-merges", "--format=%h", f"{BASE}..{H}", "--", *ps).split())
        body.append([f"**`{u}`**", len(rs), f"{sum(r['lines'] for r in rs):,}", f"{sum(b[p] for p in ps):,}",
                     ", ".join(f"{k} {v}" for k, v in sorted(reach.items())),
                     sum(1 for p in ps if p in st), newest or "none", fork])
    assert len(body) == 25
    tot = [sum(int(str(x[i]).replace(",", "")) for x in body) for i in (1, 2, 3, 5, 7)]
    assert tot[0] == 397 and tot[1] == 49555 and tot[2] == 1424530, tot
    return table(["Unit", "Paths", "Lines", "Bytes", "Reach (inventory)", f"Rows differing at `{U}`",
                  f"Newest upstream commit on the rows, at `{U}`", f"Non-merge commits `{BASE}..{H}`"],
                 body, ["---", "---:", "---:", "---:", "---", "---:", "---", "---:"]) + \
        f"\n\nTotals: {tot[0]} paths, {tot[1]:,} lines, {tot[2]:,} bytes, {tot[3]} rows differing, {tot[4]} non-merge fork commit(s)."


def opt(t, key):
    hits = [(i + 1, l.strip()) for i, l in enumerate(show(f"projects/ROCKNIX/devices/{t}/options").splitlines())
            if re.match(rf"^\s*{key}=", l)]
    return f"{hits[0][0]} `{hits[0][1].split('=', 1)[1].strip(chr(34))}`" if hits else "none"


def sec_targets():
    mkline, world = makefile()
    mk = show("Makefile").splitlines()
    kver = {}
    case = re.search(r"case \$\{DEVICE\} in(.*?)esac", show(KERNEL), re.S).group(1)
    for m in re.finditer(r"^\s*([A-Z0-9_|]+)\)\s*\n\s*PKG_VERSION=\"([^\"]+)\"", case, re.M):
        for t in m.group(1).split("|"):
            kver[t] = m.group(2)
    body = []
    for t in TARGETS:
        d = f"projects/ROCKNIX/devices/{t}"
        files = git("ls-tree", "-r", "--name-only", H, "--", d).split()
        i = mkline[t]
        arches = []
        for l in mk[i:i + 4]:
            m = re.search(r"ARCH=(\S+)", l)
            if m:
                arches.append(m.group(1))
        conf = [f for f in files if re.search(r"/linux/linux\.[^/]+\.conf$", f)]
        head = show(conf[0]).splitlines()[2].lstrip("# ").replace(" Kernel Configuration", "") if conf else "none"
        loader = opt(t, "BOOTLOADER")
        fw = opt(t, "UBOOT_FIRMWARE")
        fork = len(git("log", "--no-merges", "--format=%h", f"{BASE}..{H}", "--", d).split())
        nd = len(git("diff", "--name-only", U, H, "--", d).split())
        up = git("log", "--format=%h %ad", "--date=short", "--since=2026-06-01T00:00:00Z", U, "--", d).splitlines()
        km = kver.get(t, "?")
        body.append([t, f"`Makefile:{i}`", "yes" if t in world else "no", " + ".join(arches), loader,
                     fw, opt(t, "GRAPHIC_DRIVERS"),
                     f"{sum(f.endswith('.dts') for f in files)} + {sum(f.endswith('.dtsi') for f in files)}",
                     f"`{head}`; recipe `{km}`", sum(f.endswith('.patch') for f in files), fork, nd,
                     f"{len(up)}; {up[0] if up else 'none'}"])
    assert len(body) == 12
    return table(["Target", "Target line", "In `world`", "Arches", "`BOOTLOADER` (options line)",
                  "`UBOOT_FIRMWARE`", "`GRAPHIC_DRIVERS`", "Trees (`.dts` + `.dtsi`)",
                  "Conf header; kernel recipe's version", "Patches (T43's)", "Fork edits (non-merge)",
                  f"Files differing at `{U}`", "Upstream since 2026-06-01; newest"], body)


def sec_projects():
    g = per_unit()
    st = drift([r["path"] for rs in g.values() for r in rs])
    body = []
    for p in PROJECTS:
        rs = g[f"projects/{p}"]
        devs = sorted({r["path"].split("/")[3] for r in rs if r["path"].startswith(f"projects/{p}/devices/")})
        refs = git("grep", "-n", "-w", p, H, "--", "Makefile", "config", "scripts").splitlines() if \
            subprocess.run(["git", "grep", "-q", "-w", p, H, "--", "Makefile", "config", "scripts"]).returncode == 0 else []
        refs = [":".join(x.split(":")[1:3]) for x in refs]
        has_opt = subprocess.run(["git", "cat-file", "-e", f"{H}:projects/{p}/options"],
                                 capture_output=True).returncode == 0
        fork = len(git("log", "--no-merges", "--format=%h", f"{BASE}..{H}", "--", f"projects/{p}").split())
        body.append([p, len(rs), f"{sum(r['lines'] for r in rs):,}", ", ".join(devs) or "none",
                     "yes" if has_opt else "no", ", ".join(f"`{x}`" for x in refs) or "none (as a whole word)",
                     fork, sum(1 for r in rs if r["path"] in st)])
    assert len(body) == 9
    return table(["Project", "Paths", "Lines", "Devices (in the slice's rows)", "Project `options`",
                  "Engine references, whole word, `Makefile config scripts`", "Fork commits (non-merge, `projects/<P>`)",
                  f"Rows differing at `{U}`"], body)


PINS = ["RK3326/packages/u-boot", "RK3326/packages/u-boot-legacy", "RK3399/packages/u-boot",
        "RK3566/packages/u-boot", "RK3566/packages/u-boot-Generic", "RK3566/packages/u-boot-Specific",
        "RK3576/packages/u-boot", "RK3588/packages/u-boot", "S922X/packages/amlogic-boot-fip",
        "S922X/packages/u-boot"]


def pin(path, rev):
    t = show(path, rev)
    v = re.search(r'^PKG_VERSION="([^"]*)"', t, re.M)
    s = re.search(r'^PKG_SHA256="([^"]*)"', t, re.M)
    return (v.group(1) if v else None), (s.group(1) if s else None)


def short(x):
    return f"`{x[:12]}...`" if x and len(x) > 16 else f"`{x}`"


def sec_pins():
    found = sorted(p for p in git("ls-tree", "-r", "--name-only", H, "--",
                                  *[f"projects/ROCKNIX/devices/{t}" for t in TARGETS]).split()
                   if re.search(r"/packages/(u-boot[^/]*|amlogic-boot-fip)/package\.mk$", p))
    assert found == sorted(f"projects/ROCKNIX/devices/{x}/package.mk" for x in PINS), found
    body = []
    for x in PINS:
        p = f"projects/ROCKNIX/devices/{x}/package.mk"
        v, s = pin(p, H)
        vu, su = pin(p, U)
        same = git("diff", "--name-only", U, H, "--", p).strip() == ""
        setby = git("log", "-1", "--format=%h %ad %an", "--date=short", f"-SPKG_VERSION=\"{v}\"", H, "--", p).strip()
        at_u = "the same file" if same else (f"`{vu}`, sha256 {short(su)}" if (vu, su) != (v, s)
                                             else "the same pin; the file differs")
        body.append([f"`{x.replace('/packages/', ' ')}`", f"`{v}`" + (f", sha256 {short(s)}" if s else ", no `PKG_SHA256`"),
                     at_u, setby, "CANNOT (no network)" if v != "1.0" else "n/a (no source: `PKG_URL=\"\"`)"])
    for c in ["projects/ROCKNIX/packages/tools/rkbin/package.mk", "projects/ROCKNIX/packages/tools/qcom-abl/package.mk"]:
        vs = re.findall(r'^\s*PKG_VERSION="([^"]*)"', show(c), re.M)
        body.append([f"`{c.split('/')[-2]}` (cited by path, outside the slice: `{c}`)",
                     ", ".join(short(v) for v in vs) + (f" ({len(vs)} branches of a device case)" if len(vs) > 1 else ""),
                     "the same file" if git("diff", "--name-only", U, H, "--", c).strip() == "" else "differs",
                     "not owned here", "not owned here"])
    assert len(body) == 12
    return table(["Unit", f"At `{H}`", f"At `{U}`", "Set by (`git log -1 -S`)", "Author's current release"], body)


def dts_rows():
    rows = [r for r in load_rows() if r["lang"] == "devicetree"]
    assert len(rows) == 53
    return rows


def includes(text):
    inc = re.findall(r'^\s*(?:#include|/include/)\s+"([^"]+)"', text, re.M)
    inc += re.findall(r'^\s*#include\s+<([^>]+)>', text, re.M)
    return [i for i in inc if not i.startswith("dt-bindings/")]


def sec_trees():
    rows = dts_rows()
    texts = {r["path"]: show(r["path"]) for r in rows}
    base = {r["path"]: r["path"].rsplit("/", 1)[1] for r in rows}
    body = []
    for r in rows:
        p, t = r["path"], texts[r["path"]]
        tgt = p.split("/")[3]
        inc = includes(t)
        if p.endswith(".dts"):
            model = re.search(r'^\s*model\s*=\s*"([^"]+)"', t, re.M)
            root = t[t.find("/ {"):] if "/ {" in t else t
            comp = re.search(r'compatible\s*=\s*"([^"]+)"', root)
            body.append([f"`{base[p]}`", tgt, ".dts", r["lines"], ", ".join(f"`{i}`" for i in inc) or "none",
                         f"\"{model.group(1)}\"" if model else "none (inherited)",
                         f"`{comp.group(1)}`" if comp else "none (inherited)",
                         "none" if "rocknix-dt-id" not in t else "present"])
        else:
            users = sorted(base[q] for q in texts if q != p and base[p] in includes(texts[q]))
            body.append([f"`{base[p]}`", tgt, ".dtsi", r["lines"], ", ".join(f"`{i}`" for i in inc) or "none",
                         "family: " + base[p].split("-")[0].split("_")[0], "included by: " + (", ".join(f"`{u}`" for u in users) or "none in the slice"),
                         "n/a"])
    assert len(body) == 53 and sum(b[2] == ".dts" for b in body) == 39
    return table(["Tree", "Target", "Kind", "Lines", "Local includes", "`model` (`.dts`) / family (`.dtsi`)",
                  "First root `compatible` (`.dts`) / includers (`.dtsi`)", "`rocknix-dt-id`"], body,
                 ["---", "---", "---", "---:", "---", "---", "---", "---"])


def sec_q6():
    g, inv = per_unit(), inventory_reach()
    _, world = makefile()
    body = []
    for u in UNIT_ORDER:
        rs = g[u]
        ds = collections.Counter(disposition(r, world, inv) for r in rs)
        aw = "Already written: nothing inherited (the generic recipe built for no target)" \
            if u == "packages/linux" else "no fork edit"
        body.append([f"**`{u}`**", len(rs), "; ".join(f"{d} ×{n}" if len(ds) > 1 else d for d, n in ds.most_common()), aw])
    assert len(body) == 25
    assert not any("remov" in b[2].lower() for b in body)
    return table(["Unit", "Paths", "Disposition (D-WORKFLOW-209's words; ×n where the unit's rows differ)",
                  "`Already written:`"], body, ["---", "---:", "---", "---"])


def sec_q7():
    rows, inv = load_rows(), inventory_reach()
    rock = sorted(p.split("/")[3] for p in git("ls-tree", "--name-only", H, "projects/Rockchip/devices/").split())
    body = []
    for d in rock:
        same = d in TARGETS or d in ("H700", "SM8550", "GENERIC_X64")
        # a near-name is a family wildcard (RK356X) that matches a target; RK3328
        # against RK3326 is two SoCs, not a near-name
        near = [t for t in TARGETS if not same and "X" in d and re.fullmatch(d.replace("X", "."), t)]
        if same or near:
            body.append([f"**`projects/Rockchip/devices/{d}`**",
                         f"`projects/ROCKNIX/devices/{d if same else near[0]}`",
                         "exact name" if same else "near-name", "different trees, different `options`"])
    for r in rows:
        if r["shadow"]:
            body.append([f"**`{r['path']}`**", f"`{r['shadow']}`", "shadowed pair",
                         f"override {override_reach(inv, r['shadow'])}"])
    hn = collections.defaultdict(list)
    for l in git("grep", "-n", "CONFIG_DEFAULT_HOSTNAME", H, "--", "projects", "packages").splitlines():
        _, f, n, txt = l.split(":", 3)
        hn[re.sub(r"\s+", " ", txt.strip())].append(f"{f}:{n}")
    for s, where in sorted(hn.items()):
        if "@" in s:
            note = "named, not read (T40's and T43's confs)"
        elif "scripts/config" in s:
            note = "the generic copy and the override, both set by `3d7c075f63`: " + ", ".join(f"`{w}`" for w in where)
        else:
            note = "a conf's literal, named, not read (T43's): " + ", ".join(f"`{w}`" for w in where)
        body.append([f"`{s[:90]}`", f"{len(where)} line(s)", "hostname string", note])
    assert len([b for b in body if b[2] == "shadowed pair"]) == 9
    assert len([b for b in body if b[2] in ("exact name", "near-name")]) == 4
    return table(["Name or path", "Its duplicate", "Kind", "Note"], body)


def sec_edges():
    rows = load_rows()
    inv = {r["path"]: r for r in inventory_reach()}
    sl = {r["path"] for r in rows}
    recipes = sorted(p for p in sl if p.endswith("/package.mk"))
    names = collections.defaultdict(list)
    for p in recipes:
        m = re.search(r'^PKG_NAME="([^"]+)"', show(p), re.M)
        names[m.group(1) if m else p.split("/")[-2]].append(p)
    body = []
    for n, ps in sorted(names.items()):
        e = re.escape(n)
        pat = (rf"(get_(build|install|pkg)_dir|get_pkg_variable)[[:space:]]+{e}([^A-Za-z0-9_.+-]|$)"
               rf"|PKG_DEPENDS_[A-Z]+\+?=.*(\"|[[:space:]]){e}(:[a-z]+)?(\"|[[:space:]]|$)")
        r = subprocess.run(["git", "grep", "-n", "-E", pat, H, "--", "projects", "packages", "scripts", "config"],
                           capture_output=True, text=True)
        assert r.returncode in (0, 1), r.stderr
        dirs = tuple(p.rsplit("/", 1)[0] + "/" for p in ps)
        hits = [l.split(":", 1)[1] for l in r.stdout.splitlines()
                if l.split(":")[1] not in sl and not l.split(":")[1].startswith(dirs)]
        reached = [h for h in hits if inv.get(h.split(":")[0], {}).get("reach") in ("shipped", "test")]
        body.append([f"`{n}`", len(ps), len(hits), len(reached),
                     ", ".join(f"`{':'.join(h.split(':')[:2])}`" for h in reached[:3]) + (" ..." if len(reached) > 3 else "") or "none",
                     EDGE_NOTE.get(n, "none reached") if reached else "no edge from a shipped or test file"])
    assert len(body) == 45 and sum(b[1] for b in body) == 52
    assert {b[0].strip("`") for b in body if b[3]} == set(EDGE_NOTE), sorted({b[0] for b in body if b[3]})
    return table(["Recipe name", "Copies in the slice", "Edges from outside", "From a shipped or test file",
                  "First reached edges", "Which copy the edge resolves to"], body, ["---", "---:", "---:", "---:", "---", "---"])


def sec_dead():
    rows, inv = load_rows(), inventory_reach()
    _, world = makefile()
    b = sizes([r["path"] for r in rows])
    g = collections.defaultdict(list)
    for r in rows:
        if disposition(r, world, inv).startswith("dead"):
            u = unit_of(r["path"])
            g["the nine projects" if u.startswith("projects/") and u != DRIVERS else u].append(r)
    order = ["the nine projects", "packages/linux-driver-addons", "packages/linux-firmware", DRIVERS]
    assert set(g) == set(order), sorted(g)
    body = [[f"**{k}**" if k == "the nine projects" else f"**`{k}`**", len(g[k]), f"{sum(r['lines'] for r in g[k]):,}",
             f"{sum(b[r['path']] for r in g[k]):,}"] for k in order]
    n = sum(len(v) for v in g.values())
    assert n == 203, n
    tl, tb = sum(r["lines"] for v in g.values() for r in v), sum(b[r["path"]] for v in g.values() for r in v)
    return table(["Group", "Rows", "Lines", "Bytes"], body + [["**all**", n, f"{tl:,}", f"{tb:,}"]],
                 ["---", "---:", "---:", "---:"])


def sec_counts():
    rows, inv = load_rows(), inventory_reach()
    _, world = makefile()
    c = collections.Counter()
    for r in rows:
        d = disposition(r, world, inv)
        c["dead" if d.startswith("dead") else "shadowed" if d.startswith("shadowed") else
          "unshipped" if d.startswith("unshipped") else "reached after all" if d.startswith("reached") else d] += 1
    return " ".join(f"{k} {v}" for k, v in sorted(c.items())) + f" total {sum(c.values())}"


SECTIONS = {"coverage": sec_coverage, "units": sec_units, "targets": sec_targets, "projects": sec_projects,
            "pins": sec_pins, "trees": sec_trees, "dead": sec_dead, "q6": sec_q6, "q7": sec_q7, "edges": sec_edges,
            "counts": sec_counts}


def refresh(path, check):
    text = open(path).read()
    new = text
    for name, fn in SECTIONS.items():
        b, e = f"<!-- begin t25:{name} -->\n", f"\n<!-- end t25:{name} -->"
        if b in new:
            i, j = new.index(b) + len(b), new.index(e)
            new = new[:i] + fn() + new[j:]
    if check:
        print("t25-tables: check", "same" if new == text else "DIFFERS", path)
        return 0 if new == text else 1
    open(path, "w").write(new)
    print("t25-tables: wrote", path)
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] in ("write", "check"):
        sys.exit(refresh(sys.argv[2], sys.argv[1] == "check"))
    if len(sys.argv) != 2 or sys.argv[1] not in SECTIONS:
        sys.exit(__doc__)
    print(SECTIONS[sys.argv[1]]())

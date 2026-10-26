#!/usr/bin/env python3
"""T29 (#676): the quirks slice's tables, regenerated from the tree, never typed.

    python3 -I -B docs/audits/2026_10_25-epic-m6-os-device-quirks/tools/t29-tables.py <section>
    python3 -I -B .../t29-tables.py write <file>   # refresh every generated block in <file>
    python3 -I -B .../t29-tables.py check <file>   # exit 1 when a block differs from a fresh run

Sections: entries (88), boards (26 + the sub-node), delta (31), coverage (333), counts.

Run from the worktree root. Inputs: the inventory (`docs/reviews/inventory.json`,
for the 333 and their tiers and languages) and local git reads at
`8ebaf8daad` (the read hash) and `651150fc88` (the upstream head, by name).
The paths carry spaces, so every git read here is `-z` or by blob id. No fetch,
no network, no build, nothing on a unit. Each section asserts its counts and
no empty cell, so a short table fails instead of printing.
"""
import collections
import json
import re
import subprocess
import sys

H, U = "8ebaf8daad", "651150fc88"
Q = "projects/ROCKNIX/packages/hardware/quirks/devices"
TIER_A = {"Retroid Pocket Nova", "QEMU Standard PC (Q35 + ICH9, 2009)"}
TIER_B = TIER_A | {"Anbernic RG40XX H", "Anbernic RG40XX V", "Anbernic RG CubeXX", "AYANEO Pocket ACE",
                   "AYANEO Pocket DMG", "AYANEO Pocket DS", "AYANEO Pocket EVO", "AYANEO Pocket S 2K",
                   "AYANEO Pocket S Mini", "AYN Odin 2", "AYN Odin 2 Portal", "AYN Thor", "Retroid Pocket 6",
                   "Retroid Pocket 6 TOP-DPAD"}
TREES = ["projects/ROCKNIX/devices/H700/linux/dts/allwinner", "projects/ROCKNIX/devices/SM8550/linux/dts/qcom"]
PATCH = "projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch"


def git(*a, ok=(0,)):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    if r.returncode not in ok:
        sys.exit(f"t29-tables: git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout


def tree(rev=H):
    """Every entry under Q at rev: path -> (mode, oid)."""
    out = {}
    for ent in git("ls-tree", "-r", "-z", rev, "--", Q + "/").split("\0"):
        if ent:
            meta, path = ent.split("\t", 1)
            mode, _, oid = meta.split()
            out[path] = (mode, oid)
    return out


def inventory():
    inv = json.load(open("docs/reviews/inventory.json"))
    c = inv["columns"]
    rows = {d["path"]: d for d in (dict(zip(c, r)) for r in inv["rows"]) if d["tree"] == "distribution"
            and d["path"].startswith(Q + "/")}
    assert len(rows) == 333, len(rows)
    return rows


def blob(oid):
    return git("cat-file", "-p", oid)


def table(head, rows, align=None):
    for r in rows:
        assert len(r) == len(head) and all(str(x).strip() for x in r), r
    out = ["| " + " | ".join(head) + " |", "| " + " | ".join(align or ["---"] * len(head)) + " |"]
    out += ["| " + " | ".join(str(x).replace("|", "\\|") for x in r) + " |" for r in rows]
    return "\n".join(out)


def boards():
    """(model, file:line) for every model line in the two trees and patch 0154's context."""
    res = []
    for d in TREES:
        for l in git("grep", "-n", "-E", r"^\s*model = ", H, "--", f"{d}/*.dts").splitlines():
            _, f, n, txt = l.split(":", 3)
            res.append((re.search(r'model = "([^"]*)"', txt).group(1), f"{f.rsplit('/', 1)[1]}:{n}"))
    for i, l in enumerate(blob(git("rev-parse", f"{H}:{PATCH}").strip()).splitlines(), 1):
        m = re.match(r'^ \s*model = "([^"]*)"', l)
        if m:
            res.append((m.group(1), f"0154-rocknix-dt-id.patch:{i} (context)"))
    return res


def entries():
    t, inv = tree(), inventory()
    top = {}
    for ent in git("ls-tree", "-z", H, "--", Q + "/").split("\0"):
        if ent:
            meta, path = ent.split("\t", 1)
            mode, _, oid = meta.split()
            top[path.rsplit("/", 1)[1]] = (mode, oid)
    assert len(top) == 88, len(top)
    alias = {n: blob(o).strip() for n, (m, o) in top.items() if m == "120000"}
    dirs = [n for n in top if n not in alias]
    assert len(alias) == 23 and len(dirs) == 65, (len(alias), len(dirs))
    assert len(t) == 333 and set(t) == set(inv), len(t)
    return t, inv, top, alias, dirs


def tier(name, alias):
    n = alias.get(name, name)
    if name in TIER_A or n in TIER_A:
        return "A"
    if name in TIER_B or n in TIER_B:
        return "B"
    return "rest"


def disposition(name, alias):
    tr = tier(name, alias)
    base = {"A": "selected by a shipped unit or the VM", "B": "selected by a board a shipped image boots",
            "rest": "carried by placement (D-WORKFLOW-185)"}[tr]
    return f"alias of {alias[name]}; {base}" if name in alias else base


def sec_entries():
    t, inv, top, alias, dirs = entries()
    model = collections.defaultdict(list)
    for m, where in boards():
        model[m].append(where)
    body = []
    for name in sorted(top, key=str.lower):
        ps = [p for p in t if p.startswith(f"{Q}/{name}/") or p == f"{Q}/{name}"]
        lines = sum(inv[p]["lines"] or 0 for p in ps)
        fork = sum(inv[p]["tier"] == "fork-own" for p in ps)
        files = [p[len(Q) + len(name) + 2:] for p in ps if p != f"{Q}/{name}"]
        tops = sorted(f for f in files if "/" not in f)
        prefixes = sorted({re.match(r"^(\d+)", f).group(1) for f in tops if re.match(r"^\d+", f)})
        flags = set()
        links = []
        for p in ps:
            mode, oid = t[p]
            if mode == "120000":
                if p != f"{Q}/{name}":
                    links.append(f"`{p[len(Q) + len(name) + 2:]}` -> `{blob(oid).strip()}`")
                continue
            flags |= set(re.findall(r"\b(DEVICE_[A-Z0-9_]+)=", blob(oid)))
        if name in alias:
            row = [f"**`{name}`**", f"alias -> `{alias[name]}`", 1, lines, fork, tier(name, alias), "—", "—",
                   ", ".join(model.get(name, [])) or "none in the two trees", disposition(name, alias)]
        else:
            row = [f"**`{name}`**", f"directory, {len(files)} files" + (f"; links: {'; '.join(links)}" if links else ""),
                   len(ps), lines, fork, tier(name, alias), ", ".join(sorted(flags)) or "none",
                   ", ".join(prefixes) or "none", ", ".join(model.get(name, [])) or "none in the two trees",
                   disposition(name, alias)]
        body.append(row)
    assert len(body) == 88
    assert sum(int(r[2]) for r in body if not r[1].startswith("alias")) + 23 == 333
    assert not any("remov" in r[-1].lower() for r in body)
    return table(["Entry", "Kind and shared files", "Paths", "Lines", "Fork-own", "Tier", "`DEVICE_*` flags set",
                  "Run-order prefixes", "`model` in the shipped trees", "Disposition (D-WORKFLOW-209)"], body,
                 ["---", "---", "---:", "---:", "---:", "---", "---", "---", "---", "---"])


def sec_boards():
    t = tree()
    seen, body = set(), []
    for m, where in sorted(boards(), key=lambda x: (x[0] == "AYN-Thor", x[0].lower())):
        has = f"{Q}/{m}" in t or any(p.startswith(f"{Q}/{m}/") for p in t)
        note = "a sub-node, not a board" if m == "AYN-Thor" else ("owned unit" if m in ("Anbernic RG35XX SP", "Anbernic RG-SP") else "")
        dup = "repeat" if m in seen else ""
        seen.add(m)
        body.append([f"`{m}`", f"`{where}`", "HAS" if has else "NONE", "; ".join(x for x in (note, dup) if x) or "—"])
    lines = len(body)
    distinct = len({r[0] for r in body if r[0] != "`AYN-Thor`"})
    has = len({r[0] for r in body if r[2] == "HAS"})
    assert lines == 28 and distinct == 26 and has == 15, (lines, distinct, has)
    return table(["`model`", "Where", "Entry", "Note"], body) + \
        f"\n\n{lines} lines; {distinct} distinct boards (the `AYN-Thor` sub-node set apart): {has} HAS, {distinct - has} NONE."


def sec_delta():
    out = git("diff", "--name-status", "-z", H, U, "--", Q + "/").split("\0")
    rows, i = [], 0
    while i < len(out) - 1:
        st = out[i]; p = out[i + 1]; i += 2
        rows.append([st, f"`{p[len(Q) + 1:]}`"])
    assert len(rows) == 31, len(rows)
    c = collections.Counter(r[0] for r in rows)
    assert (c["A"], c["D"], c["M"]) == (16, 3, 12), c
    return table(["Status (`8ebaf8daad` -> `651150fc88`)", "Path under `devices/`"], rows) + \
        f"\n\n31 paths: {c['A']} A, {c['D']} D, {c['M']} M."


def sec_coverage():
    t, inv, top, alias, dirs = entries()
    st = {}
    out = git("diff", "--name-status", "-z", H, U, "--", Q + "/").split("\0")
    for i in range(0, len(out) - 1, 2):
        st[out[i + 1]] = out[i]
    body = []
    for p in sorted(t):
        name = p[len(Q) + 1:].split("/")[0]
        r = inv[p]
        body.append([f"`{p}`", tier(name, alias), r["tier"], t[p][0], r["lines"] if r["lines"] else "—", r["language"],
                     {"M": "differs (M)", "D": "deleted upstream (D)"}.get(st.get(p), "identical"),
                     disposition(name, alias), "tree"])
    assert len(body) == 333
    return table(["Path", "Tier", "Provenance", "Mode", "Lines", "Language", f"At `{U}`", "Disposition", "proved"], body,
                 ["---", "---", "---", "---", "---:", "---", "---", "---", "---"])


def sec_counts():
    t, inv, top, alias, dirs = entries()
    c = collections.Counter(tier(p[len(Q) + 1:].split("/")[0], alias) for p in t)
    return f"paths 333; entries 88 = {len(dirs)} directories + {len(alias)} aliases; tiers A {c['A']}, B {c['B']} (A included in B: {c['A'] + c['B']}), rest {c['rest']}"

A = "docs/audits/2026_10_25-epic-m6-os-device-quirks"
FAIL = {
    "r01_block": "an inventory change, or a glob that is not the 333",
    "r02_counts": "a membership other than 333 paths and 88 entries",
    "r03_branch_vs_hash": "an edit on this branch to one of the 333",
    "r04_entries_symlinks": "an entry or a symlink added or removed",
    "r05_autostart_profile": "QUIRK_DEVICE derived another way",
    "r06_autostart_loop": "the loop running something other than the files directly in the directory",
    "r07_package_mk": "the install no longer copying every devices/* or setting the modes",
    "r08_wrapper": "the wrapper no longer dispatching to the device's bin/ first",
    "r09_model_lines": "a board's model line changed or added",
    "r10_dtid_patch": "patch 0154 no longer naming the RG35XX models",
    "r11_has_none": "an entry added or removed for a board string",
    "r12_tiers": "a tier count other than 6 / 70 / 263",
    "r13_fork_paths": "a fork commit on the 333 other than the six",
    "r14_fork_dir": "a fork commit on the directory other than the nine",
    "r15_delta": "an upstream delta other than 16 A 3 D 12 M, or other than 18 / 12 commits",
    "r16_delta_shipped": "the two panel-calibration files absent upstream",
    "r17_shape": "a shape count other than the brief's",
    "r18_spellings": "a 050-game*configs file added, removed or renamed",
    "r19_fixture": "tools/nova-led-test changed or no longer naming the Nova's bin",
    "r20_removal_rule": "a change under packages/, projects/ or tools/ since the dispatch tip",
    "r21_patch_models": "an entry added for one of patch 0154's models",
    "r22_board_count": "a board count other than 28 lines / 26 distinct",
}


def sec_runs():
    rows = [l.split("\t") for l in open(f"{A}/stage-a/runs.tsv").read().splitlines()[1:]]
    assert len(rows) == 22 and set(r[0] for r in rows) == set(FAIL), sorted(set(r[0] for r in rows) ^ set(FAIL))
    body = []
    for rid, rc, sec, start in rows:
        out = [l for l in open(f"{A}/stage-a/{rid}.out").read().splitlines() if l.strip()]
        fig = (out[0] if out else "(empty)")[:110].replace("`", "'")
        if len(out) > 1:
            fig += f" (+{len(out) - 1} lines)"
        body.append([f"`{rid}`", rc, sec, start, f"`{fig}`", FAIL[rid]])
    return table(["Run (`stage-a/runs.sh`)", "Exit", "Seconds", "Started (UTC)", "Figure (first line of `stage-a/<run>.out`)",
                  "A FAIL would mean"], body, ["---", "---:", "---:", "---", "---", "---"])


SECTIONS = {"entries": sec_entries, "boards": sec_boards, "delta": sec_delta, "coverage": sec_coverage, "counts": sec_counts, "runs": sec_runs}


def refresh(path, check):
    text = open(path).read()
    new = text
    for name, fn in SECTIONS.items():
        b, e = f"<!-- begin t29:{name} -->\n", f"\n<!-- end t29:{name} -->"
        if b in new:
            i, j = new.index(b) + len(b), new.index(e)
            new = new[:i] + fn() + new[j:]
    if check:
        print("t29-tables: check", "same" if new == text else "DIFFERS", path)
        return 0 if new == text else 1
    open(path, "w").write(new)
    print("t29-tables: wrote", path)
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] in ("write", "check"):
        sys.exit(refresh(sys.argv[2], sys.argv[1] == "check"))
    if len(sys.argv) != 2 or sys.argv[1] not in SECTIONS:
        sys.exit(__doc__)
    print(SECTIONS[sys.argv[1]]())

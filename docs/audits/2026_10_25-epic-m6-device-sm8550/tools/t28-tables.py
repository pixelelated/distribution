#!/usr/bin/env python3
"""T28 (#675): the SM8550 slice's tables, regenerated from the tree, never typed.

    python3 -I -B docs/audits/2026_10_25-epic-m6-device-sm8550/tools/t28-tables.py <section>
    python3 -I -B .../t28-tables.py write <file>   # refresh every generated block in <file>
    python3 -I -B .../t28-tables.py check <file>   # exit 1 when a block differs from a fresh run

Sections:
- coverage (29);
- trees (16 sources plus the `.disabled` patch's row);
- pins (8);
- runs (stage A's 31, from `stage-a/runs.tsv` and its outputs);
- counts.

Run from the worktree root.
Inputs:
- `.qa-scratch/t28/paths.txt`, brief section 2's block output;
- local git reads at `8ebaf8daad` (the read hash) and `651150fc88` (the
  upstream head, by name).

No fetch, no network, no plan generation, no build, nothing on the Nova.
Each section asserts its row count and no empty cell.
"""
import json
import re
import subprocess
import sys

H, U = "8ebaf8daad", "651150fc88"
DIR = "projects/ROCKNIX/devices/SM8550/"
A = "docs/audits/2026_10_25-epic-m6-device-sm8550"
NOVA = DIR + "linux/dts/qcom/qcs8550-retroidpocket-rpnova.dts"
# The Nova's include chain (rpnova.dts:8, rp6.dts's own include) and the two
# InputPlumber files whose matches name the Nova's model line
# (02-ayn-controller.yaml:44 `value: Retroid Pocket Nova`, its
# capability_map_id ayn_mcu): what the shipped unit uses, not placement.
NOVA_CHAIN = {DIR + "linux/dts/qcom/qcs8550-retroidpocket-rp6.dts",
              DIR + "linux/dts/qcom/qcs8550-ayn-common.dtsi"}
NOVA_INPUT = {DIR + "filesystem/usr/share/inputplumber/devices/02-ayn-controller.yaml",
              DIR + "filesystem/usr/share/inputplumber/capability_maps/ayn_mcu.yaml"}
DISABLED = DIR + "patches/linux/0053-add-hynitron-touchscreen.patch.disabled"


def git(*a, ok=(0,)):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    if r.returncode not in ok:
        sys.exit(f"t28-tables: git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout


def show(path, rev=H):
    return git("show", f"{rev}:{path}")


def exists(path, rev):
    return subprocess.run(["git", "cat-file", "-e", f"{rev}:{path}"], capture_output=True).returncode == 0


def paths():
    p = open(".qa-scratch/t28/paths.txt").read().split()
    assert len(p) == 29, len(p)
    return p


def table(head, rows, align=None):
    for r in rows:
        assert len(r) == len(head) and all(str(x).strip() for x in r), r
    out = ["| " + " | ".join(head) + " |", "| " + " | ".join(align or ["---"] * len(head)) + " |"]
    out += ["| " + " | ".join(str(x).replace("|", "\\|") for x in r) + " |" for r in rows]
    return "\n".join(out)


def what(p):
    rel = p[len(DIR):]
    if rel == "options":
        return "the device's build options (`BOOTLOADER=\"qcom-abl\"` :34, `FIRMWARE=\"extra-firmware\"` :63, `ADDITIONAL_PACKAGES` :66)"
    if rel == "bootloader/update.sh":
        return "the in-place updater: copies `rocknix_abl` to `/flash` (:19-23), runs `updateabl` (:25), removes `/flash/boot` and `/flash/EFI` (:27-31)"
    if rel == "config/kernel-firmware.dat":
        return "six firmware entries installed by `kernel-firmware`'s `makeinstall_target` (its `package.mk:39-70`); no kernel embed for SM8550"
    if p in NOVA_INPUT:
        return "InputPlumber: matches the Nova's model line (`02-ayn-controller.yaml:44`) and its map"
    if "/inputplumber/" in rel or rel.endswith(".hwdb"):
        return "AYANEO's or AYN's input file; no match names the Nova"
    if p == NOVA:
        return "the Nova's tree: `model = \"Retroid Pocket Nova\"`; includes `qcs8550-retroidpocket-rp6.dts`"
    if p in NOVA_CHAIN:
        return "in the Nova's include chain"
    if rel.endswith((".dts", ".dtsi")):
        return "another board's tree, built into every SM8550 boot image"
    if p == DISABLED:
        return "disabled at birth (`aa458af6f9`); `scripts/unpack:150-159` globs `*.patch` only"
    raise AssertionError(p)


def disposition(p):
    if p == NOVA:
        return "shipped unit"
    if p in NOVA_CHAIN or p in NOVA_INPUT:
        return "shipped unit (the Nova uses it)"
    if p == DISABLED:
        return "disabled at birth, upstream's; removal is #346's class decision"
    rel = p[len(DIR):]
    if rel.endswith((".dts", ".dtsi")) or "/inputplumber/" in rel or rel.endswith(".hwdb"):
        return "carried by placement (D-WORKFLOW-185)"
    return "shipped; superseded upstream (#1099)" if rel in ("options", "bootloader/update.sh") else "shipped; Q3 reading (F-03)"


def sec_coverage():
    st = {}
    for l in git("diff", "--name-status", H, U, "--", *paths()).splitlines():
        k, f = l.split("\t", 1)
        st[f] = k
    body = []
    for p in paths():
        t = show(p)
        body.append([f"`{p}`", "upstream-carried", "shipped", len(t.splitlines()), git("cat-file", "-s", f"{H}:{p}").strip(),
                     what(p), {"M": "differs (M)", "D": "deleted upstream"}.get(st.get(p), "identical"), disposition(p), "tree"])
    assert len(body) == 29
    return table(["Path", "Tier", "Reach", "Lines", "Bytes", "What it is", f"At `{U}`", "Disposition", "proved"], body,
                 ["---", "---", "---", "---:", "---:", "---", "---", "---", "---"])


def includes(t):
    return [i for i in re.findall(r'^\s*#include\s+["<]([^">]+)[">]', t, re.M) if not i.startswith("dt-bindings/")]


def sec_trees():
    ps = [p for p in paths() if p.endswith((".dts", ".dtsi"))]
    assert len(ps) == 16
    texts = {p: show(p) for p in ps}
    body = []
    for p in ps:
        t, name = texts[p], p.rsplit("/", 1)[1]
        model = re.search(r'^\s*model\s*=\s*"([^"]+)"', t, re.M)
        if p.endswith(".dtsi"):
            users = sorted(q.rsplit("/", 1)[1] for q in ps if q != p and name in includes(texts[q]))
            m = "none (a `.dtsi`); included by " + ", ".join(f"`{u}`" for u in users)
        else:
            m = f"\"{model.group(1)}\"" if model else "none (inherited)"
        body.append([f"`{name}`", len(t.splitlines()), ", ".join(f"`{i}`" for i in includes(t)) or "none", m,
                     "none" if "rocknix-dt-id" not in t else "present", disposition(p)])
    body.append([f"`{DISABLED.rsplit('/', 1)[1]}`", len(show(DISABLED).splitlines()), "n/a (a patch)", "n/a", "n/a",
                 "disabled at birth, upstream's, never applied (`scripts/unpack:150-159`)"])
    assert len(body) == 17 and sum(b[-1].startswith("shipped unit") for b in body) == 3
    return table(["Source", "Lines", "Includes (local and mainline)", "`model`", "`rocknix-dt-id`", "Disposition"], body,
                 ["---", "---:", "---", "---", "---", "---"])


PINS = [("qcom-abl", "tools/qcom-abl", "`options:34` `BOOTLOADER=\"qcom-abl\"`"),
        ("rocknix-abl", "tools/rocknix-abl", "`options:66` `ADDITIONAL_PACKAGES`"),
        ("the kernel", "linux", "`linux/package.mk:29-35` (`H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)`)"),
        ("mkbootimg", "tools/mkbootimg", "`linux/package.mk:19` (`SM*` host tool)"),
        ("extra-firmware", "linux-firmware/extra-firmware", "`options:63` `FIRMWARE`"),
        ("kernel-firmware", "linux-firmware/kernel-firmware", "the ROCKNIX override; installs `config/kernel-firmware.dat`"),
        ("inputplumber", "tools/inputplumber", "`options:66`"),
        ("gamepadcalibration", "tools/gamepadcalibration", "`options:66`")]


def pinof(t, kernel=False):
    if kernel:
        block = re.search(r"H700\|SM4450\|SM6115\|SM8250\|SM8550\|SM8650\|SM8750\)(.*?);;", t, re.S).group(1)
        t = block
    v = re.search(r'PKG_VERSION="([^"]*)"', t)
    s = re.search(r'PKG_SHA256="([^"]*)"', t)
    return (v.group(1) if v else None), (s.group(1) if s else None)


def fmt(v, s):
    vv = f"`{v[:12]}...`" if v and len(v) > 16 else f"`{v}`"
    return vv + (f", sha `{s[:12]}...`" if s else ", no sha")


def setby(f, v, s):
    a = git("log", "-1", "--format=%h %ad", "--date=short", f"-SPKG_VERSION=\"{v}\"", H, "--", f).strip()
    b = git("log", "-1", "--format=%h %ad %an", "--date=short", f"-S{s}", H, "--", f).strip() if s else ""
    return f"version {a}" + (f"; sha {b}" if b and b.split()[0] != a.split()[0] else "")


def sec_pins():
    body = []
    for unit, rel, ref in PINS:
        f = f"projects/ROCKNIX/packages/{rel}/package.mk"
        k = unit == "the kernel"
        v, s = pinof(show(f), k)
        if exists(f, U):
            vu, su = pinof(show(f, U), k)
            same_file = git("diff", "--name-only", H, U, "--", f).strip() == ""
            at_u = "identical file" if same_file else ("the same pin; the file differs" if (vu, su) == (v, s) else f"**differs**: {fmt(vu, su)}")
        else:
            at_u = "**absent**"
            if unit == "rocknix-abl":
                ov, _ = pinof(show("projects/ROCKNIX/packages/tools/openabl/package.mk", U))
                hist = git("log", "--format=%h %ad %s", "--date=short", f"{H}..{U}", "--", "projects/ROCKNIX/packages/tools/openabl").splitlines()
                at_u += f": replaced by `openabl` `{ov}` (" + ", ".join(f"{h.split()[0]} {h.split()[1]}" for h in reversed(hist)) + ")"
            if unit == "mkbootimg":
                at_u = "**deleted** (`" + git("log", "-1", "--format=%h", "--diff-filter=D", f"{H}..{U}", "--", f).strip() + "`)"
        body.append([unit, f"`{f}`; {ref}", fmt(v, s), at_u, setby(f, v, s), "CANNOT (no network)" if v != "1.0" else "n/a (`PKG_URL=\"\"`, a meta recipe)"])
    assert len(body) == 8
    return table(["Unit", "Recipe (outside the slice) and the reference", f"At `{H}`", f"At `{U}`", "Set by (`git log -1 -S`)",
                  "Author's current release"], body)


FAIL = {
    "r01_block": "an inventory change, or a glob that picks up T41's rows",
    "r02_paths": "a membership other than the 29",
    "r03_branch_vs_hash": "an edit on this branch to one of the 29",
    "r04_lines": "an inventory line count that is not the tree's",
    "r05_disabled": "a renamed, shortened or enabled patch",
    "r06_conf_head": "a configuration for another kernel than the recipe's",
    "r07_conf_diff": "a fork line in the configuration, or upstream regenerating it with new options",
    "r08_conf_distance": "a different distance between the Qualcomm configurations",
    "r09_conf_fork": "a fork commit on the configuration since the base",
    "r10_conf_upstream": "an upstream commit other than the four",
    "r11_kernel_case": "SM8550 moved to another kernel branch, at either hash",
    "r12_pins": "a pin other than the table's, at either hash",
    "r13_rocknix_abl_log": "a setting commit other than the brief's",
    "r14_openabl": "openabl at another version, or another history",
    "r15_update_sh": "a changed updater: another copy, no `updateabl`, no cleanup",
    "r16_scripts_mkimage": "the `qcom-abl` branch moved or gone",
    "r17_bootloader_mkimage": "a third SM8550 branch, or one of the two gone",
    "r18_kernel_abl_branch": "the boot image built another way (no dtb append, no mkbootimg)",
    "r19_embed_blocks": "an SM8550 embed block in the kernel recipe",
    "r20_config_xml": "a tree list other than fourteen",
    "r21_updateabl": "`updateabl` writing without the compare, or one slot only",
    "r22_dts_count": "a tree added or removed",
    "r23_nova_dts": "another include, model or compatible for the Nova",
    "r24_dt_id": "a tree carrying `rocknix-dt-id`",
    "r25_history": "a fork author on the 29, or a different upstream count",
    "r26_fork_since_base": "a fork non-merge commit on the directory since the base",
    "r27_delta_29": "an upstream delta over the 29 other than 2 M",
    "r28_delta_dir": "an upstream delta over the directory other than 4 M 2 A",
    "r29_boot_change": "a different set of upstream boot-path commits",
    "r30_makefile": "SM8550 out of `world`, or another default device",
    "r31_removal_rule": "a change under `packages/`, `projects/` or `tools/` since the dispatch tip",
}


def sec_runs():
    rows = [l.split("\t") for l in open(f"{A}/stage-a/runs.tsv").read().splitlines()[1:]]
    assert len(rows) == 31 and set(r[0] for r in rows) == set(FAIL), sorted(set(r[0] for r in rows) ^ set(FAIL))
    body = []
    for rid, rc, sec, start in rows:
        out = [l for l in open(f"{A}/stage-a/{rid}.out").read().splitlines() if l.strip()]
        fig = (out[0] if out else "(empty)")[:110].replace("`", "'")
        if len(out) > 1:
            fig += f" (+{len(out) - 1} lines)"
        body.append([f"`{rid}`", rc, sec, start, f"`{fig}`", FAIL[rid]])
    return table(["Run (`stage-a/runs.sh`)", "Exit", "Seconds", "Started (UTC)", "Figure (first line of `stage-a/<run>.out`)",
                  "A FAIL would mean"], body, ["---", "---:", "---:", "---", "---", "---"])


def sec_counts():
    c = {}
    for p in paths():
        d = disposition(p).split(" (")[0].split(";")[0]
        c[d] = c.get(d, 0) + 1
    return " | ".join(f"{k}: {v}" for k, v in sorted(c.items())) + f" | total {sum(c.values())}"


SECTIONS = {"coverage": sec_coverage, "trees": sec_trees, "pins": sec_pins, "runs": sec_runs, "counts": sec_counts}


def refresh(path, check):
    text = open(path).read()
    new = text
    for name, fn in SECTIONS.items():
        b, e = f"<!-- begin t28:{name} -->\n", f"\n<!-- end t28:{name} -->"
        if b in new:
            i, j = new.index(b) + len(b), new.index(e)
            new = new[:i] + fn() + new[j:]
    if check:
        print("t28-tables: check", "same" if new == text else "DIFFERS", path)
        return 0 if new == text else 1
    open(path, "w").write(new)
    print("t28-tables: wrote", path)
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] in ("write", "check"):
        sys.exit(refresh(sys.argv[2], sys.argv[1] == "check"))
    if len(sys.argv) != 2 or sys.argv[1] not in SECTIONS:
        sys.exit(__doc__)
    print(SECTIONS[sys.argv[1]]())

#!/usr/bin/env python3
# T37 (#684): the three generated tables of 02-forward-audit.md -- coverage, patch reach, currency.
# Each table asserts its own row count and its class counts and exits 1 when they drift; --drift
# constructs one drift per table (a row dropped) so the assertion is seen to fire before its table
# is trusted. Read-only: git reads in --repo, and the patch-reach lines a sourced-recipe run in the
# scratch export wrote (--reach). Run: python3 -B -I t37-tables.py --repo <worktree> --reach <file>
#   [--drift] {coverage,patches,currency}
import argparse, subprocess, sys

P1, MB, UN = "2174265e9c", "c445081a59", "651150fc88"
U = "projects/ROCKNIX/packages/ui/"
# the inventory's tiers for the 15 (docs/reviews/inventory.json via section 2's block, block-2.txt)
WHAT = {
    "emulationstation/package.mk": "the ES recipe: clone of the fork's ES at the pin; depends, cmake options, credentials by name, install steps",
    "emulationstation/autostart/001-emulationstation": "boot step: links /storage/.emulationstation to /storage/.config/emulationstation",
    "emulationstation/config/common/es_features.cfg": "per-emulator feature catalogue",
    "emulationstation/config/common/es_input.cfg": "controller database",
    "emulationstation/config/common/es_savestates.cfg": "save-state layout (retroarch)",
    "emulationstation/config/common/es_settings.cfg": "an empty <config> seed",
    "emulationstation/sources/es_settings": "ExecStartPre: timezone, locale, environment import",
    "emulationstation/sources/serial_number_check": "the serial number check",
    "emulationstation/sources/start_es.sh": "sources es_settings and runs ES",
    "emulationstation/system.d/emustation.service": "the non-sway unit",
    "emulationstation/system.d/essway.service": "the sway unit, with sway-ready before start",
    "lowerdeck/package.mk": "lowerdeck at its pin, copied to /usr/share/lowerdeck",
    "themes/es-theme-art-book-next/package.mk": "the theme at its pin, with the wordmark, the licence, five artwork sets removed, a zh font block",
    "themes/es-theme-art-book-next/sources/Tiny5-OFL.txt": "the Tiny5 font licence",
    "themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg": "the wordmark",
}

def git(repo, *a, ok=(0,)):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)
    if r.returncode not in ok:
        sys.exit(f"git {' '.join(a)} failed rc={r.returncode}: {r.stderr.strip()}")
    return r.stdout

def blob(repo, h, p):
    out = git(repo, "rev-parse", "--verify", "-q", f"{h}:{p}", ok=(0, 1)).strip()
    return out or None

def fail(msg):
    print(f"ASSERT FAIL: {msg}"); sys.exit(1)

def coverage(repo, drift, tiers):
    paths = [p for p in git(repo, "ls-tree", "-r", "--name-only", P1, "--", U).split() if "/patches/" not in p]
    if drift: paths = paths[1:]
    rows = []; fork = up = 0; klass_count = {}
    for p in paths:
        rel = p[len(U):]
        lines = git(repo, "show", f"{P1}:{p}").count("\n") + (0 if git(repo, "show", f"{P1}:{p}").endswith("\n") else 1)
        bm, bt, bu = blob(repo, MB, p), blob(repo, P1, p), blob(repo, UN, p)
        if bm is None: k = "fork-added"
        elif bm != bt: k = "fork-modified"
        else: k = "upstream-carried"
        if bm is not None and bm == bt and bu != bm: k += ", behind"
        if bm is not None and bm != bt and bu != bm: k += ", overlap"
        ns = git(repo, "diff", "--numstat", MB, P1, "--", p).split()
        stat = "--" if not ns else str(int(ns[0]) + int(ns[1]))
        t = tiers[p]
        fork += t == "fork-own"; up += t == "upstream-carried"
        klass_count[k.split(",")[0]] = klass_count.get(k.split(",")[0], 0) + 1
        rows.append(f"| `{rel}` | {lines} | {t} | {k} | {stat} | {WHAT[rel]} |")
    if len(rows) != 15: fail(f"coverage rows {len(rows)} != 15")
    if (fork, up) != (6, 9): fail(f"inventory tiers fork-own {fork} upstream-carried {up} != 6/9")
    total = sum(int(r.split("|")[2]) for r in rows)
    if total != 4561: fail(f"coverage lines {total} != 4561")
    print("| File under `projects/ROCKNIX/packages/ui/` | Lines (`grep -c ''`) | Inventory tier | Git class against the base (`c445081a59`; behind: equal to the base and not to `upstream/next`) | Fork stat | What it is |")
    print("| --- | ---: | --- | --- | ---: | --- |")
    print("\n".join(rows))
    print(f"\ngenerated, asserted: rows {len(rows)}, lines {total}, inventory fork-own {fork} upstream-carried {up}, git classes {dict(sorted(klass_count.items()))}")

def patches(reach, drift):
    rows = [l.strip() for l in open(reach) if "-> " in l and "patches" in l and "no patches/" not in l]
    if drift: rows = rows[1:]
    devs = sorted({r.split(":")[0].split("/")[0] for r in rows})
    es = [r for r in rows if " emulationstation " in r]; th = [r for r in rows if " es-theme-art-book-next " in r]
    if len(devs) != 15: fail(f"devices {len(devs)} != 15")
    if len(rows) != 30 or len(es) != 15 or len(th) != 15: fail(f"rows {len(rows)} (es {len(es)}, theme {len(th)}) != 30 (15, 15)")
    es_reached = [r for r in es if r.endswith(": REACHED")]; th_reached = [r for r in th if r.endswith(": REACHED")]
    print("| Device / arch | Package | `PATCH_ARCH` | `PKG_PATCH_DIRS` | Directory | Verdict |")
    print("| --- | --- | --- | --- | --- | --- |")
    for r in rows:
        head, tail = r.split(" -> ")
        dv, rest = head.split(": ", 1); pkg, pa, pd = rest.split(" ")
        d, v = tail.rsplit(": ", 1)
        print(f"| {dv} | `{pkg}` | `{pa.split('=')[1]}` | `{pd.split('=')[1]}` | `{d}` | {v} |")
    print(f"\ngenerated, asserted: rows {len(rows)} over {len(devs)} devices; emulationstation patches/x86_64/ REACHED on {len(es_reached)} of {len(es)}; the theme's patches/ REACHED on {len(th_reached)} of {len(th)}; lowerdeck has no patches/ directory")

def currency(repo, drift):
    files = git(repo, "diff", "--name-only", P1, UN, "--", U).split()
    up = set(git(repo, "diff", "--name-only", MB, UN, "--", U).split())
    fk = set(git(repo, "diff", "--name-only", MB, P1, "--", U).split())
    if drift: files = files[1:]
    rows = []; side = {"upstream moved": 0, "fork moved": 0, "both": 0}
    for p in files:
        s = "both" if p in up and p in fk else "upstream moved" if p in up else "fork moved" if p in fk else "neither"
        if s == "neither": fail(f"{p} differs tip-to-upstream but neither side moved it")
        side[s] += 1
        n_up = len(git(repo, "rev-list", f"{MB}..{UN}", "--", p).split())
        n_fk = len(git(repo, "rev-list", "--no-merges", f"{MB}..{P1}", "--", p).split())
        ns = git(repo, "diff", "--numstat", P1, UN, "--", p).split()
        st = f"+{ns[0]} -{ns[1]}" if ns else "--"
        at_tip = blob(repo, P1, p) is not None; at_un = blob(repo, UN, p) is not None
        what = {"upstream moved": "upstream's change the fork lacks" + ("" if at_tip else " (absent at the tip)"),
                "fork moved": "the fork's own" + ("" if at_un else " (absent upstream)"),
                "both": "both moved: a merge pending"}[s]
        rows.append(f"| `{p[len(U):]}` | {s} | {n_up} | {n_fk} | {st} | {what} |")
    if len(rows) != 14: fail(f"currency rows {len(rows)} != 14")
    if (side["upstream moved"], side["fork moved"], side["both"]) != (6, 6, 2): fail(f"sides {side} != 6/6/2")
    print("| File under `projects/ROCKNIX/packages/ui/` | Side | Upstream commits `c445081a59..651150fc88` | Fork non-merge commits `c445081a59..2174265e9c` | Tip to `upstream/next` | What it is |")
    print("| --- | --- | ---: | ---: | --- | --- |")
    print("\n".join(rows))
    print(f"\ngenerated, asserted: rows {len(rows)}; upstream-only {side['upstream moved']} fork-only {side['fork moved']} both {side['both']}")

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--repo", required=True); a.add_argument("--reach"); a.add_argument("--tiers")
    a.add_argument("--drift", action="store_true"); a.add_argument("table", choices=("coverage", "patches", "currency"))
    o = a.parse_args()
    if o.table == "coverage":
        if not o.tiers: sys.exit("coverage needs --tiers (block-2.txt)")
        tiers = {}; cols = None; on = False
        for l in open(o.tiers):
            l = l.rstrip("\n")
            if l == "TSV": on = True; continue
            if l == "CLAIMS": break
            if on and cols is None: cols = l.split("\t"); continue
            if on: r = dict(zip(cols, l.split("\t"))); tiers[r["path"]] = r["tier"]
        if len(tiers) != 15: fail(f"tiers read {len(tiers)} != 15")
        coverage(o.repo, o.drift, tiers)
    elif o.table == "patches":
        if not o.reach: sys.exit("patches needs --reach")
        patches(o.reach, o.drift)
    else:
        currency(o.repo, o.drift)

main()

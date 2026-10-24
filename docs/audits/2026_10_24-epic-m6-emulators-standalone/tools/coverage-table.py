#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
# Copied for M6 T30 (#677) from T3's docs/audits/2026_10_24-epic-m6-emulators-libretro/tools/coverage-table.py at b3cb4ec8c5
# (feature/m6-emulators-libretro-650); T30's changes, if any, are named below.
# T30 change: the body is rewritten for this slice (its membership, its
# findings, its file kinds); T3's contract is kept: one row per member, the
# path in backticks first, Q1 to Q7 never empty, the row count asserted.
"""coverage-table.py -- 02-forward-audit.md's coverage table for T30, one row
per path of the slice (#677 criterion 7).

    python3 -I coverage-table.py <tree> <audit-dir> > table.md

The membership is brief section 2's filter over docs/reviews/inventory.json
(543 rows). A cell is the finding that names the path (F, from 02's F-NN
list), else the slice table that answers it, else `n/a` with its reason.
The script asserts 543 rows and no empty cell.
"""
import json, os, re, sys

tree, audit = sys.argv[1:3]
inv = json.load(open(os.path.join(tree, "docs/reviews/inventory.json")))
cols = inv["columns"]
P = "projects/ROCKNIX/packages/emulators/standalone/"
sel = {r["path"]: r for r in (dict(zip(cols, x)) for x in inv["rows"])
       if r["tree"] == "distribution" and r["area"] == "emulators-and-cores"
       and r["path"].startswith(P) and r["reach"] in ("shipped", "test", "n/a")}

SHIPPED = {"H700", "SM8550", "GENERIC_X64"}
q4 = {r["path"]: r for r in json.load(open(os.path.join(audit, "q4-pins.json")))["rows"]}
q4shape = {"aethersx2-sa": "moving tarball, matches today; class 1 (deleted upstream, F-26)",
           "drastic-sa": "moving tarball, matches today", "duckstation-sa": "release asset, ~900 builds behind (F-27)",
           "dsperate-sa": "release asset 2.0.1, upstream 3.0.5 (F-27, class 1)", "bigpemu-sa": "release asset v119, project v1221 (F-27)",
           "steam": "release .deb 1.0.0.85, pool 1.0.0.87 (F-27)", "gzdoom-sa": "tag g4.14.2 = latest release",
           "scummvm-sa": "tag 2026.1.0, project v2026.4.0 (F-27)", "vice-sa": "tag 3.8, project 3.10 (F-27)",
           "mednafen": "fork tag 1.32.1-chd, current", "pico-8": "no project: the player's binary",
           "heroic": "no project: metapackage", "mupen64plus-sa": "no project: metapackage",
           "portaudio": "repo-missing: source gone (F-13)", "supermodel-sa": "pin on no default branch (F-28)",
           "yabasanshiro-sa": "pin on no default branch (F-28)", "azahar-sa": "behind-upstream (q4a, class 1)"}

# Findings by path (exact, or a prefix ending in /) -> {question: text}.
F = {}
def f(path, **qs):
    for q, v in qs.items():
        old = F.setdefault(path, {}).get(q)
        F[path][q] = f"{old}; {v}" if old else v
f("duckstation-sa/scripts/start_duckstation.sh", Q3="F-01 (kill target AppRun.wrapped matches no process; G1, G7); F-12 (memcards/savestates deleted uncopied; G8)", Q5="G12 launch-to-process 0.52-0.62 s; G11 helper 0.04-0.07 s", Q6="F-25 (cheevos call commented out, :130)")
f("duckstation-sa/sources/Start Duckstation.sh", Q3="F-01 (same kill target); creates neither save link", Q6="Tools launcher, installed to /usr/config/modules")
f("duckstation-sa/scripts/cheevos_duckstation.sh", Q3="F-09 shape, not called", Q2="F-10 (unquoted test)", Q6="F-25 (dead: start_duckstation.sh:130 commented)")
f("duckstation-sa/scripts/duckstation_screenshot_path", Q1="PASS (Python 3, stdlib)", Q2="PASS (staged write, identity re-check)", Q3="PASS (reading); G11 runs it", Q5="G11: 0.04-0.07 s per launch", Q7="PASS")
f("openbor/scripts/start_OpenBOR.sh", Q3="F-02 (no kill target; G1 survived)", Q2="no /etc/profile sourced")
f("mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh", Q3="F-03 (simplecore kill, G6); F-06 (zipped ROMs, G5; loose zip test)", Q5="F-29 (ROM copied to tmpfs; config in /tmp)", Q1="the fork's GENERIC_X64 repair block read (PASS)")
f("hatarisa/scripts/start_hatari.sh", Q3="F-04 (the route asks for start_hatarisa.sh; no kill target; G2); F-06 shape (:37)", Q2="echo -e ${ARGS} unquoted (Low, with F-04)", Q7="F-12 shape (:18-21 rm -rf /storage/.hatari)")
f("hatarisa/package.mk", Q3="F-04 (installs start_hatari.sh; upstream 2e7041d273 renames)")
f("scummvm-sa/scripts/start_scummvm.sh", Q3="F-07 (eval of the .scummvm file as root; G3)")
f("gzdoom-sa/scripts/start_gzdoom.sh", Q3="F-08 (xargs: an apostrophe stops the launch; G4)", Q5="G11: pk3 sha256 0.02 s x2 (not a finding)")
for s in ("ppsspp-sa/scripts/cheevos_ppsspp.sh", "flycast-sa/scripts/cheevos_flycast.sh", "armsx2-sa/scripts/cheevos_armsx2.sh", "aethersx2-sa/scripts/cheevos_aethersx2.sh", "skyemu-sa/scripts/cheevos_skyemu.sh"):
    f(s, Q3="F-09 (the previous session kept on switch-on, token-empty" + ("; G9" if "ppsspp" in s or "flycast" in s else "") + ")")
for s in ("armsx2-sa/scripts/cheevos_armsx2.sh", "aethersx2-sa/scripts/cheevos_aethersx2.sh", "flycast-sa/scripts/cheevos_flycast.sh"):
    f(s, Q2="F-10 (unquoted [ ! ${enabled} = 1 ]; G9 shows the fall-through)")
f("ppsspp-sa/scripts/cheevos_ppsspp.sh", Q2="F-22 (token written twice, default umask)")
f("dolphin-sa/scripts/cheevos_dolphin.sh", Q3="PASS (publish_disabled; G9 control)", Q2="PASS (umask 077, mktemp, mv -fT)", Q6="F-25 (password read, unused)")
f("melonds-sa/scripts/cheevos_melonds.sh", Q3="F-21 (RA_Password written plain each launch; the patch logs in with it)", Q2="F-21 (escape_sed escapes / and &, delimiter is |)")
for s, l in (("aethersx2-sa/scripts/start_aethersx2.sh", ":102"), ("armsx2-sa/scripts/start_armsx2.sh", ":113"), ("daedalusx64-sa/scripts/start_daedalusx64.sh", ":48 (<>; H3)"), ("mednafen/scripts/start_mednafen.sh", ":82,89,144,157,187"), ("melonds-sa/scripts/start_melonds.sh", ":93,100")):
    f(s, Q3=f"F-11 (comparison as redirection {l}; G10, G13)")
for s, l in (("rpcs3-sa/scripts/start_rpcs3.sh", ":25 dev_flash, dev_hdd0, dev_hdd1, custom_configs"), ("azahar-sa/scripts/start_azahar.sh", ":28,32,37,226"), ("drastic-sa/scripts/start_drastic.sh", ":57,61"), ("ares-sa/scripts/start_ares.sh", ":24"), ("skyemu-sa/scripts/start_skyemu.sh", ":30"), ("bigpemu-sa/scripts/start_bigpemu.sh", ":17"), ("cemu-sa/scripts/start_cemu.sh", ":40-43,53-81, copy unchecked")):
    f(s, Q3=f"F-12 (a real directory deleted before linking, {l})")
f("nanoboyadvance-sa/scripts/start_nanoboyadvance.sh", Q3="F-14 (a directory named gba_bios.bin)")
f("amiberry/scripts/start_amiberry.sh", Q3="F-15 (resolution keys deleted, H2; AGA grep literal; conf/* overwritten); F-06 shape (:76)")
f("supermodel-sa/scripts/start_supermodel.sh", Q3="F-16 (options passed as one argument; class 1)")
f("mednafen/scripts/start_mednafen.sh", Q7="F-17 (-vb.3dmode gets ${CE}; set -x every launch)")
f("yabasanshiro-sa/scripts/start_yabasanshiro.sh", Q3="F-19 (eval of a pad's self-reported name)")
f("gopher64-sa/scripts/start_gopher64.sh", Q3="F-20 (RA password on argv, unquoted)")
f("dolphin-sa/scripts/start_dolphin_gc.sh", Q6="F-24 (:436 -v overwritten)", Q7="F-24 (gc/wii: 282 shared lines)", Q3="PASS (reading; G1: started, exited on the synthetic input); dolphin-save-paths gates", Q5="G11: dolphin-save-paths 0.03-0.05 s x2 per launch")
f("dolphin-sa/scripts/start_dolphin_wii.sh", Q7="F-24 (shared with _gc; hotkey edited twice)", Q3="PASS (reading); :69 rm -r without -f (noisy)")
f("dolphin-sa/scripts/dolphin-save-paths", Q1="PASS (Python 3, stdlib)", Q2="PASS (plan before apply, exclusive links, lock, alarm)", Q3="PASS (reading); /storage/roms must be a mount point (G1's launch passed it)", Q5="G11: 0.03-0.05 s", Q7="PASS")
f("flycast-sa/scripts/start_flycast.sh", Q3="F-30 (mv/ln over data fragile; kill -9 \"$(pidof gptokeyb)\")")
f("ppsspp-sa/scripts/psp_save_mover.sh", Q6="F-25 (no caller in the tree)")
f("ppsspp-sa/scripts/start_ppsspp.sh", Q3="PASS: its kill target ends ppsspp (G1); :105 strips backslashes", Q5="G12 launch-to-process 0.61-0.67 s")
f("vice-sa/scripts/start_vice.sh", Q3="PASS: x64sc ended by its kill (G1)", Q5="G12 launch-to-process 0.56-0.67 s")
f("touchhle-sa/scripts/start_touchhle.sh", Q7="F-25 (echoes ${GOPHER64_JSON}, copy-paste)")
f("steam/scripts/start_steam.sh", Q3="PASS: execs a flavour that sets the kill target (resolves the route tool's 'none')")
f("aethersx2-sa/", Q4="F-26 (deleted upstream, class 1)", Q6="F-26 (deferred: base merge, class 1; Already written in 04)")
f("hatarisa/portaudio/package.mk", Q3="F-13 (archive URL 404; builds pass only from the shared cache)", Q4="F-13 (repo-missing; commit not in PortAudio/portaudio)")

# Phase 4.6 (both seats graded, 04 § Second opinion): F-31 to F-42.
f("steam/scripts/start_steam.sh", Q3="F-31 (exit 0 skips the flavours' cleanup); F-32 (URI and -silent one argument)")
f("steam/scripts/start_steam_x86.sh", Q3="F-31 (binfmt left stopped; kill names only FEX)")
f("steam/scripts/start_steam_arm64.sh", Q3="F-31 (dual-screen cleanup never runs)")
f("drastic-sa/scripts/start_drastic.sh", Q3="F-33 (the binary in /storage never refreshed by an update)")
f("dolphin-sa/scripts/start_dolphin_gc.sh", Q3="F-34 (Hotkeys.ini's swap alternates); F-39 (triforce codes dir deleted)")
f("dolphin-sa/scripts/start_dolphin_wii.sh", Q3="F-34 (Hotkeys.ini's swap alternates)")
f("melonds-sa/scripts/start_melonds.sh", Q3="F-35 (regenerated TOML may hold the credentials); F-39 (TOML deleted every launch)")
f("openbor/scripts/start_OpenBOR.sh", Q3="F-37 (Paks emptied every launch)")
f("duckstation-sa/scripts/start_duckstation.sh", Q1="F-38 (DuckStation's own achievements disabled every launch)")
f("xemu-sa/scripts/start_xemu.sh", Q3="F-39 (xemu.toml overwritten every launch)")
for s_ in ("ppsspp-sa/scripts/cheevos_ppsspp.sh", "flycast-sa/scripts/cheevos_flycast.sh", "armsx2-sa/scripts/cheevos_armsx2.sh", "aethersx2-sa/scripts/cheevos_aethersx2.sh", "skyemu-sa/scripts/cheevos_skyemu.sh", "melonds-sa/scripts/cheevos_melonds.sh"):
    f(s_, Q2="F-40 (sign-in values unescaped in sed)")
f("scummvm-sa/scripts/start_scummvm.sh", Q3="F-41 (first-run seed unreachable)")
for s_ in ("hypseus-singe/scripts/start_hypseus.sh", "daedalusx64-sa/scripts/start_daedalusx64.sh", "amiberry/scripts/start_amiberry.sh", "hatarisa/scripts/start_hatari.sh", "dsperate-sa/scripts/start_dsperate.sh", "ppsspp-sa/scripts/start_ppsspp.sh", "vice-sa/scripts/start_vice.sh", "cemu-sa/scripts/start_cemu.sh", "gzdoom-sa/scripts/start_gzdoom.sh", "pico-8/scripts/start_pico8.sh", "vita3k-sa/scripts/start_vita3k.sh", "rpcs3-sa/scripts/start_rpcs3.sh", "aethersx2-sa/scripts/start_aethersx2.sh", "armsx2-sa/scripts/start_armsx2.sh", "skyemu-sa/scripts/start_skyemu.sh", "azahar-sa/scripts/start_azahar.sh", "yabasanshiro-sa/scripts/start_yabasanshiro.sh"):
    f(s_, Q7="F-42 (launch-script hygiene, 04 § Second opinion)")
f("skyemu-sa/scripts/start_skyemu.sh", Q3="F-12 conditional: no mkdir -p of the link's parent (seats)")

def lookup(rel):
    cells = {}
    for k in sorted(F, key=len, reverse=True):
        if rel == k or (k.endswith("/") and rel.startswith(k)):
            for q, v in F[k].items():
                cells.setdefault(q, v)
    return cells

def recipe_of(rel):
    parts = rel.split("/")
    sub = parts[1] if len(parts) > 2 and os.path.isfile(os.path.join(tree, P, parts[0], parts[1], "package.mk")) else None
    return parts[0], sub

def reach(r):
    return ",".join(sorted({d.split("-")[0] for d in (r.get("reachable_by") or [])})) or "none"

def device_dir(rel):
    m = re.search(r"/(?:config|sources)/([A-Z0-9_]+)(?:/|$)", "/" + rel)
    return m.group(1) if m and re.fullmatch(r"[A-Z0-9_]{3,}", m.group(1)) else None

out = ["| Path | Recipe | Tier | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
empty = []
for p in sorted(sel):
    r = sel[p]; rel = p[len(P):]; rec, sub = recipe_of(rel); name = sub or rec
    cells = lookup(rel)
    lang = r["language"]; fo = r["tier"] == "fork-own"
    if rel.endswith("package.mk"):
        row = q4.get(p)
        cells.setdefault("Q2", "pkgcheck rc 0 (its own row); PKG_SHA256 present or a .git/empty URL")
        cells.setdefault("Q4", "q4-pins: " + q4shape.get(name, (row or {}).get("class", "?")))
        cells.setdefault("Q6", f"04 Q6 reachability row ({reach(r)})")
        cells.setdefault("Q5", "n/a: build-time recipe")
        for k in ("Q1", "Q3", "Q7"):
            cells.setdefault(k, "PASS (the fork's delta read; q4a fork-own table)" if fo else "n/a: upstream's recipe, unchanged here")
    elif lang in ("shell", "python", "c"):
        cells.setdefault("Q1", "PASS (read; no retired mechanism)" if fo else "n/a: upstream's script; read for the sweeps")
        cells.setdefault("Q2", "bash -n PASS" if lang == "shell" else "PASS (read)")
        cells.setdefault("Q3", "PASS (read; exit sweep and shell-line sweep rows in 04)")
        cells.setdefault("Q4", f"with {name}'s Q4 row")
        cells.setdefault("Q5", "nothing heavy before exec (read)" if "start" in rel.lower() else "n/a: not on the launch path's hot part")
        cells.setdefault("Q6", f"installed with {name} ({reach(r)})")
        cells.setdefault("Q7", "PASS (read)" if fo else "n/a: upstream's script, unchanged here")
    else:
        dev = device_dir(rel)
        cells.setdefault("Q1", "n/a: data")
        cells.setdefault("Q2", "n/a: data (no credential value shipped: the cheevos scripts write tokens at run time)")
        cells.setdefault("Q3", "n/a: data read by its emulator; GENERIC_X64's exercised by G1/G12" if dev == "GENERIC_X64" else "n/a: data read by its emulator")
        cells.setdefault("Q4", f"with {name}'s Q4 row")
        cells.setdefault("Q5", "n/a: read once at launch")
        if dev and dev not in SHIPPED:
            cells.setdefault("Q6", f"per-device file for {dev}, a device the fork does not ship (D-WORKFLOW-185): installed only on a {dev} build (T25's unshipped table)")
        elif dev:
            cells.setdefault("Q6", f"per-device file installed on {dev} only")
        else:
            cells.setdefault("Q6", f"installed with {name} ({reach(r)})")
        cells.setdefault("Q7", "n/a: data (62,331 lines; provenance only)" if "GameIndex" in rel else "n/a: data")
    for k in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"):
        if not cells.get(k): empty.append((p, k))
    esc = lambda s: s.replace("|", "/")
    out.append(f"| `{p}` | {name} | {r['tier']} | " + " | ".join(esc(cells.get(k, "")) for k in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7")) + " |")
assert not empty, f"empty cells: {empty[:10]}"
assert len(out) - 2 == 543, f"{len(out) - 2} rows"
assert not any("proved:" in l for l in out), "the token criterion 12 counts must not appear in the coverage table"
print("\n".join(out))
print(f"coverage-table: {len(out) - 2} rows, 0 empty cells", file=sys.stderr)

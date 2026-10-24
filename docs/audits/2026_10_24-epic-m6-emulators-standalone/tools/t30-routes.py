#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""t30-routes.py -- every standalone launch route an image's table offers,
resolved the way runemu.sh resolves it, against what that image installs
(M6 T30, #677; brief section 4 Q3 and Q6, the exit sweep's host half).

    python3 -I t30-routes.py <out.json> <out.md> <DEVICE>=<image/system> ...

For each <system> in <image/system>/usr/config/emulationstation/es_systems.cfg
and each <emulator> other than retroarch, each <core>:

  the script   runemu.sh at 8ebaf8daad: emulator mednafen runs
               start_mednafen.sh (235-236); otherwise -P<system> setup, shell,
               ports and windows run the ROM itself (354-386), gamecube and
               triforce start_dolphin_gc.sh, wii and wiiware start_dolphin_wii.sh
               (358-365), and everything else /usr/bin/start_${CORE%-*}.sh (391)
  present      the script exists in <image/system>/usr/bin
  kill         the installed script's `set_kill set "..."` arguments (each a
               name killall gets; -9 dropped), or none when it sets none
  binaries     for each kill name, the executables of that name anywhere in the
               tree (killall matches a process's name, which for an ELF is its
               file name, truncated to 15 characters)

A route whose script is absent, or whose kill names match no executable, is
printed for reading; the tool grades nothing beyond presence. It asserts that
every image has a table and at least one standalone route, and exits 1 when
one does not (a scan that read nothing is not a pass, blindspot 39).
"""
import json, os, re, sys, xml.etree.ElementTree as ET

out_json, out_md, *pairs = sys.argv[1:]
RUNS_ROM = {"setup", "shell", "ports", "windows"}
DOLPHIN = {"gamecube": "start_dolphin_gc.sh", "triforce": "start_dolphin_gc.sh",
           "wii": "start_dolphin_wii.sh", "wiiware": "start_dolphin_wii.sh"}

def script_for(system, emulator, core):
    if emulator == "mednafen":
        return "start_mednafen.sh"
    if system in RUNS_ROM:
        return None
    if system in DOLPHIN:
        return DOLPHIN[system]
    return f"start_{core.rsplit('-', 1)[0] if '-' in core else core}.sh"

def kill_names(path):
    names, found = [], False
    with open(path, errors="replace") as f:
        for line in f:
            m = re.search(r'set_kill\s+set\s+"([^"]*)"', line)
            if m:
                found = True
                names += [w for w in m.group(1).split() if w != "-9"]
    return names if found else None

def executables(root):
    seen = {}
    for d, _, files in os.walk(root):
        for n in files:
            p = os.path.join(d, n)
            if os.path.isfile(p) and os.access(p, os.X_OK):
                seen.setdefault(n, []).append(os.path.relpath(p, root))
    return seen

result, failed = {}, False
for pair in pairs:
    dev, root = pair.split("=", 1)
    table = os.path.join(root, "usr/config/emulationstation/es_systems.cfg")
    if not os.path.isfile(table):
        print(f"{dev}: no table at {table}", file=sys.stderr); failed = True; continue
    exes = executables(root)
    rows = []
    for s in ET.parse(table).getroot().findall("system"):
        name = s.findtext("name")
        for e in s.findall("emulators/emulator"):
            emu = e.get("name")
            if emu == "retroarch":
                continue
            for c in e.findall("cores/core"):
                core = (c.text or "").strip()
                scr = script_for(name, emu, core)
                row = {"system": name, "emulator": emu, "core": core, "default": c.get("default") == "true",
                       "script": scr}
                if scr is None:
                    row.update(present=None, kill=None, binaries={})
                else:
                    sp = os.path.join(root, "usr/bin", scr)
                    row["present"] = os.path.isfile(sp)
                    row["kill"] = kill_names(sp) if row["present"] else None
                    row["binaries"] = {k: exes.get(k, []) for k in (row["kill"] or [])}
                rows.append(row)
    if not rows:
        print(f"{dev}: no standalone route in {table}", file=sys.stderr); failed = True
    result[dev] = {"root": root, "rows": rows}

with open(out_json, "w") as f:
    json.dump(result, f, indent=1, sort_keys=True); f.write("\n")
with open(out_md, "w") as f:
    for dev, r in result.items():
        rows = r["rows"]
        absent = [x for x in rows if x["present"] is False]
        nokill = [x for x in rows if x["present"] and x["kill"] is None]
        unmatched = [x for x in rows if x["present"] and x["kill"] and not any(x["binaries"].values())]
        f.write(f"### {dev}\n\n`{r['root']}`: {len(rows)} standalone routes; "
                f"{len(absent)} with no script, {len(nokill)} whose script sets no kill target, "
                f"{len(unmatched)} whose kill names match no executable in the tree.\n\n")
        f.write("| System | Emulator | Core | Script | Present | Kill names | Executables of that name |\n| --- | --- | --- | --- | --- | --- | --- |\n")
        for x in rows:
            bins = "; ".join(f"{k}: {', '.join(v) if v else 'none'}" for k, v in x["binaries"].items()) or "-"
            f.write(f"| {x['system']} | {x['emulator']} | {x['core']}{' (default)' if x['default'] else ''} | "
                    f"{x['script'] or 'the ROM itself'} | {'-' if x['present'] is None else ('yes' if x['present'] else '**no**')} | "
                    f"{' '.join(x['kill']) if x['kill'] else ('**none**' if x['present'] else '-')} | {bins} |\n")
        f.write("\n")
for dev, r in result.items():
    rows = r["rows"]
    print(f"{dev}: routes={len(rows)} absent={sum(x['present'] is False for x in rows)} "
          f"nokill={sum(bool(x['present']) and x['kill'] is None for x in rows)} "
          f"unmatched={sum(bool(x['present']) and bool(x['kill']) and not any(x['binaries'].values()) for x in rows)}")
sys.exit(1 if failed else 0)

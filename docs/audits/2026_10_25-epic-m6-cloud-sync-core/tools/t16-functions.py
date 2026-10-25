#!/usr/bin/env python3
"""T16 (#663): one row per function of cloud_backup, cloud_restore and cloud_capture.

  t16-functions.py <dir holding the three at 8ebaf8daad> <oracle.json from t16-oracle.py> [--markdown]

For each function: its lines, its copy-twin's lines (the twins only) with
`identical` or `differs` (bodies compared line for line), the callers by a
static call graph (a function name appearing as a word in another body or in
the top-level code), and the oracle rows that reach it. A row reaches a
function when it invokes the script and the function is in the static
closure from the script's top level, with the phases the row's flags skip
removed (--system-only skips the saves phase, --saves-only the settings
phase) and, under --yes, the console-only prompt functions. For
cloud_capture the closure is the whole script's: its modes are not split
statically, which is a stated limit, not a claim of coverage. Asserts 45,
47 and 40 functions and 39 shared names; exits 1 naming any delta.
"""
import json, re, sys

DEF = re.compile(r"^([a-z_]+)\(\)")
EXPECT = {"cloud_backup": 45, "cloud_restore": 47, "cloud_capture": 40}
TWIN = {"cloud_backup": "cloud_restore", "cloud_restore": "cloud_backup"}
PHASE = {"--system-only": {"backup_game_saves", "restore_game_saves"},
         "--saves-only": {"backup_system_files", "restore_system_files"}}
PROMPT = {"controller_confirm", "read_controller_input", "get_controller_devices", "controller_menu"}

def parse(path):
    L = open(path).read().split("\n"); fns = {}; top = []; i = 0
    while i < len(L):
        m = DEF.match(L[i])
        if m:
            j = i
            if not L[i].rstrip().endswith("}") or L[i].count("{") != L[i].count("}"):
                j = i + 1
                while j < len(L) and not L[j].startswith("}"):
                    j += 1
            fns[m.group(1)] = {"a": i + 1, "b": j + 1, "body": L[i:j + 1]}
            i = j + 1; continue
        top.append(L[i]); i += 1
    return fns, top

def words(lines):
    return set(re.findall(r"[a-z_]+", "\n".join(l for l in lines if not l.lstrip().startswith("#"))))

def closure(fns, start_words, drop):
    seen = set(); todo = [n for n in fns if n in start_words and n not in drop]
    while todo:
        n = todo.pop()
        if n in seen: continue
        seen.add(n)
        todo += [m for m in fns if m != n and m not in drop and m in words(fns[n]["body"][1:])]
    return seen

def main():
    d, oracle = sys.argv[1], json.load(open(sys.argv[2]))
    S = {s: parse(f"{d}/{s}") for s in EXPECT}
    deltas = [f"{s} {len(S[s][0])} != {n}" for s, n in EXPECT.items() if len(S[s][0]) != n]
    shared = set(S["cloud_backup"][0]) & set(S["cloud_restore"][0])
    if len(shared) != 39: deltas.append(f"shared {len(shared)} != 39")
    rows = []
    for s in EXPECT:
        fns, top = S[s]
        topw = words(top)
        callers = {n: sorted([m for m in fns if m != n and n in words(fns[m]["body"][1:])] + (["(top level)"] if n in topw else [])) for n in fns}
        reach = {n: [] for n in fns}
        for r in oracle["table"]:
            for inv in r["invokes"]:
                parts = inv.split()
                if parts[0] != s: continue
                drop = set().union(*(PHASE.get(f, set()) for f in parts[1:]))
                if "--yes" in parts[1:]: drop |= PROMPT
                for n in closure(fns, topw, drop):
                    if r["row"] not in reach[n]: reach[n].append(r["row"])
        for n, f in fns.items():
            twin = ""
            if s in TWIN and n in S[TWIN[s]][0]:
                t = S[TWIN[s]][0][n]
                twin = f"{TWIN[s]}:{t['a']}-{t['b']} " + ("identical" if t["body"] == f["body"] else "differs")
            rows.append({"script": s, "fn": n, "lines": f"{f['a']}-{f['b']}", "twin": twin or "own",
                         "callers": callers[n], "rows": reach[n]})
    uncalled = [f"{r['script']}:{r['fn']}" for r in rows if not r["callers"]]
    print(json.dumps({"functions": len(rows), "by_script": {s: len(S[s][0]) for s in S}, "shared": len(shared),
                      "identical_shared": sum(1 for r in rows if r["script"] == "cloud_backup" and r["twin"].endswith("identical")),
                      "unrowed": sum(1 for r in rows if not r["rows"]), "uncalled": uncalled, "deltas": deltas}))
    if "--markdown" in sys.argv:
        print("| Script | Function | Lines | Copy-twin | Called from | Oracle rows that reach it | proved: |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        for r in rows:
            rr = r["rows"]
            cell = ("unrowed" if not rr else (", ".join(f"`{x}`" for x in rr[:6]) + (f" (+{len(rr) - 6})" if len(rr) > 6 else "")))
            print(f"| `{r['script']}` | `{r['fn']}` | {r['lines']} | {r['twin']} | {', '.join(r['callers']) or '**nothing**'} | {cell} | tree |")
    return 1 if deltas else 0

sys.exit(main())

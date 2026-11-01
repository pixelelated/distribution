# T37 (#684) stage A: shortest want-chains in genbuildplan's plan JSON (scripts/genbuildplan.py
# --with-json), from a root step to each named step, and vlc's declared target dependencies from
# pkgjson's records. Read-only over files under /workspace/tmp/m6-t37/stage-a/plans/.
import json, sys, os, collections
O = sys.argv[1]
def chains(tag, root, goals):
    pl = json.load(open(os.path.join(O, tag + ".plan.json")))
    wants = collections.defaultdict(set)
    for s in pl:
        if s.get("task") in ("build", "install"):
            for w in s.get("wants", []):
                wants[s["name"]].add(w)
    names = {s["name"] for s in pl}
    for g in goals:
        if g not in names:
            print(f"{tag}: {root} -> {g}: NOT IN PLAN"); continue
        prev = {root: None}; q = collections.deque([root])
        while q:
            n = q.popleft()
            if n == g: break
            for w in sorted(wants.get(n, ())):
                if w not in prev: prev[w] = n; q.append(w)
        if g not in prev: print(f"{tag}: {root} -> {g}: NO CHAIN"); continue
        path = []; n = g
        while n: path.append(n); n = prev[n]
        print(f"{tag}: " + " -> ".join(reversed(path)))
for tag, root in (("x64-es", "emulationstation:target"), ("h700-es", "emulationstation:target")):
    chains(tag, root, ["fribidi:target", "gettext:host", "pango:target", "systemd:target", "pugixml:target", "mesa:target", "libass:target"])
    pl = json.load(open(os.path.join(O, tag + ".plan.json")))
    es = [s for s in pl if s["name"] == "emulationstation:target" and s["task"] == "build"]
    print(f"{tag}: emulationstation:target build wants ({len(es[0]['wants'])}):", " ".join(es[0]["wants"]))
chains("x64-image", "image", ["libass:target", "fribidi:target"])
recs = []
raw = open(os.path.join(O, "x64-es.json")).read().replace("\n", "")
recs = json.loads("[" + raw[:-1] + "]")
for r in recs:
    if r["name"] in ("vlc", "libass", "fribidi", "pango", "sway", "swaywm-env", "SDL2", "gettext"):
        print("pkgjson", r["name"], r["hierarchy"], "target:", r["target"], "| host:", r["host"])

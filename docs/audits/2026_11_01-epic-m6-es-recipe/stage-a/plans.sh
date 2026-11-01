#!/bin/bash
# T37 (#684) stage A: open items 3, 5, 9 and fribidi's libass path, computed in the scratch export
# (ruling (k)) with the build system's own plan tools -- scripts/pkgjson | scripts/genbuildplan.py,
# piped as config/multithread:49 runs it (a file between them interleaved the parallel workers, 01:07) -- and named fields from a sourced mesa. Nothing is built.
X=/workspace/tmp/m6-t37/export; T=/workspace/tmp/m6-t37/tmp; O=/workspace/tmp/m6-t37/stage-a/plans; mkdir -p "$O"
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
[ -d "$X/.git" ] && { echo "STOP: the export is a git tree"; exit 2; }
plan() { # $1 device $2 arch $3 device_root $4 tag $5.. targets
  local dv=$1 ar=$2 dr=$3 tag=$4; shift 4
  s=$(date +%s)
  env -i HOME="$T/home" PATH=/usr/bin:/bin PROJECT=ROCKNIX DEVICE="$dv" ARCH="$ar" ${dr:+DEVICE_ROOT=$dr} bash -c 'cd "$1" || exit 2; shift; out=$1; shift; set -o pipefail; scripts/pkgjson 2>"$out.pkgjson.err" | tee "$out.json" | scripts/genbuildplan.py --show-wants --with-json "$out.plan.json" --build "$@" > "$out.plan" 2>"$out.plan.err"' _ "$X" "$O/$tag" "$@"; rc=$?
  e=$(date +%s); echo "plan $tag ($dv/$ar, build $*) rc=$rc wall=$((e-s))s json-bytes=$(wc -c < "$O/$tag.json") plan-lines=$(wc -l < "$O/$tag.plan" 2>/dev/null)"
}
plan GENERIC_X64 x86_64 "" x64-es emulationstation
plan GENERIC_X64 x86_64 "" x64-image image
plan H700 aarch64 "" h700-es emulationstation
plan RK3566 arm RK3566 rk3566-arm arm
echo "worktree build roots: $(ls -d build.* 2>/dev/null | wc -l); export build roots: $(ls -d "$X"/build.* | tr '\n' ' ')"
python3 -B -I - "$O" <<'PY'
import json, sys, os
O = sys.argv[1]
def load(tag):
    p = os.path.join(O, tag + ".plan.json")
    if not os.path.exists(p): print(tag, "NO PLAN JSON"); return None
    return json.load(open(p))
def names(pl):
    out = []
    for step in pl.get("plan", pl if isinstance(pl, list) else []):
        out.append(step.get("name") if isinstance(step, dict) else step)
    return out
for tag in ("x64-es", "x64-image", "h700-es", "rk3566-arm"):
    pl = load(tag)
    if pl is None: continue
    if isinstance(pl, dict): keys = sorted(pl.keys())
    else: keys = "list"
    steps = pl["plan"] if isinstance(pl, dict) and "plan" in pl else pl
    jobs = [s for s in steps if isinstance(s, dict)]
    def has(n): return any(j.get("name") == n for j in jobs)
    print(tag, "keys", keys, "steps", len(steps), "emulationstation:target", has("emulationstation:target"),
          "gettext:host", has("gettext:host"), "fribidi:target", has("fribidi:target"),
          "libass:target", has("libass:target"), "pango:target", has("pango:target"), "udev-ish",
          sorted({j["name"] for j in jobs if j.get("name","").split(":")[0] in ("systemd","eudev","udev","libudev")}),
          "pugixml:target", has("pugixml:target"))
PY

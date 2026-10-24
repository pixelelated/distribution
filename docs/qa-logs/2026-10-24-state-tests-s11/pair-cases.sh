#!/bin/bash
# pair-cases.sh -- T14 S11's control for #1011 (pixelelated-vm-cloud-boundaries),
# the tool before the fix (the given copy) and the fixed one:
#   refused -- a disposable fixture process the case owns, argv[0]
#              "qemu-system-fixture" and the run's pair path in its argv
#              (never a QEMU), beside a start that is refused: the start sees
#              a qemu-system-* process and refuses, and --image names a path
#              that does not exist, so vm-pair is never reached either way
#   hidden  -- the tool's own cleanup() as a started run's, with a stand-in
#              pidfile naming a pid no process holds (cleanup-probe.py)
# The fixture is ended by its own pid. Nothing outside the scratch.
# XDG_RUNTIME_DIR points into the scratch for the CLI runs, so a derived runtime
# directory could only land there; no bytecode is written beside the tools.
#   pair-cases.sh <tree> <tool before> <historical tree> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(readlink -f "$2")"; H="$(cd "$3" && pwd)"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S"
P="$T/docs/qa-logs/2026-10-24-state-tests-s11/cleanup-probe.py"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
DEAD=$(( (1 << 22) - 1 )); while kill -0 "$DEAD" 2>/dev/null; do DEAD=$((DEAD - 1)); done
for side in before:"$OLD" after:"$T/tools/pixelelated-vm-cloud-boundaries"; do
  n=${side%%:*}; t=${side#*:}; O="$S/$n-out"; mkdir -p "$O"
  # the tool's pair directory: <output>/pair before the fix, <output>/vm-pair after it (D-INFRA-031's name)
  pd=pair; [ "$n" = after ] && pd=vm-pair
  bash -c 'exec -a qemu-system-fixture python3 -c "import time; time.sleep(120)" "$1/$2/vm-a.qcow2"' _ "$O" "$pd" & FX=$!
  sleep 0.5; kill -0 "$FX" || { echo "the fixture did not start"; exit 2; }
  env -u VM_QEMU_RUNTIME_DIR XDG_RUNTIME_DIR="$S/xdg" python3 -I -B "$t" --tree "$H" --image "$S/no-such-image.img.gz" --build-id stand-in --output "$O" > "$S/$n-refused.txt" 2>&1; rc=$?
  sleep 0.3; if kill -0 "$FX" 2>/dev/null; then alive=yes; kill -TERM "$FX"; else alive=no; fi; wait "$FX" 2>/dev/null
  absent=$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("all_absent", "unset"))' "$O/cleanup.json" 2>/dev/null || echo "no cleanup.json")
  mkdir -p "$S/$n-hidden"; h=$(python3 -I -B "$P" "$t" "$H" "$S/$n-hidden" "$DEAD" "$S/$n-hidden-runtime" 2>&1)
  echo "  $n: refused start rc $rc ($(tail -1 "$S/$n-refused.txt" | cut -c1-60)) | fixture alive after: $alive | all_absent: $absent"
  echo "  $n: hidden pid $DEAD -> $h" | cut -c1-260
  if [ "$n" = before ]; then
    check "before: the refused start signals the fixture (the positive)" "$([ "$alive" = no ] && echo 0 || echo 1)"
    check "before: and records all_absent true (the positive)" "$([ "$absent" = True ] && echo 0 || echo 1)"
    check "before: a started run's cleanup records all_absent true without reading any pidfile (the positive)" "$(echo "$h" | grep -q '"all_absent": true' && echo 0 || echo 1)"
  else
    check "after: the refused start leaves the fixture alive" "$([ "$alive" = yes ] && echo 0 || echo 1)"
    check "after: and writes no all_absent" "$([ "$absent" = unset ] && echo 0 || echo 1)"
    want="$S/xdg/pixelelated-vm-$(printf '%s' "$(readlink -f "$O")" | sha256sum | cut -c1-8)"
    check "after: RUNTIME names \${XDG_RUNTIME_DIR}/pixelelated-vm-<8 hex of the output path>, and the refused start did not create it" "$([ "$(cat "$O/RUNTIME")" = "$want" ] && [ ! -e "$want" ] && echo 0 || echo 1)"
    check "after: a recorded pid not visible in /proc is an observation error, vm-pair down is not called, and no all_absent is written" "$(echo "$h" | grep -q '"observation_error": "recorded guest pid(s) \['"$DEAD"'\] not visible' && echo "$h" | grep -q '"called": \[\]' && ! echo "$h" | grep -q all_absent && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi

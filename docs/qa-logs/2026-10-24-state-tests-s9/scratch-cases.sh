#!/bin/bash
# scratch-cases.sh -- T14 S9's control for PL-17: is the state check's payload
# scratch removed when the run is interrupted? A synthetic update tar (one
# root, root/target/SYSTEM holding stand-in bytes) is inspected by the gate
# before this change (the given copy) and the fixed one with `unsquashfs` a
# shim that records its pid and sleeps, so the gate is sent SIGTERM while it
# holds the copied SYSTEM in its pix-state-* scratch. Each run has its own
# TMPDIR. Never a real image. Nothing outside the scratch.
#   scratch-cases.sh <tree> <gate before> <scratch>
set -u
T="$(cd "$1" && pwd)"; GB="$(readlink -f "$2")"; S="$3"; rm -rf "${S:?}"; mkdir -p "$S/bin" "$S/pkg/target"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
printf 'stand-in SYSTEM bytes, not a squashfs\n' > "$S/pkg/target/SYSTEM"
( cd "$S" && tar -cf update.tar pkg/target/SYSTEM )
printf '#!/bin/sh\necho $$ > "$SHIM_PID"\nexec sleep 30\n' > "$S/bin/unsquashfs"; chmod 755 "$S/bin/unsquashfs"
for side in before:"$GB" after:"$T/tools/pixelelated-state-check"; do
  n=${side%%:*}; g=${side#*:}; mkdir -p "$S/$n-tmp"
  SHIM_PID="$S/$n-shim.pid" TMPDIR="$S/$n-tmp" PATH="$S/bin:/usr/bin:/bin" python3 -I "$g" --payload "$S/update.tar" > "$S/$n.json" 2>&1 & p=$!
  for i in $(seq 1 50); do [ -s "$S/$n-shim.pid" ] && break; sleep 0.1; done
  [ -s "$S/$n-shim.pid" ] || { echo "the unsquashfs shim never started ($n)"; kill -TERM "$p"; exit 2; }
  held=$(find "$S/$n-tmp" -path '*pix-state-*' -name SYSTEM | wc -l)
  kill -TERM "$p"; wait "$p"; rc=$?; kill -TERM "$(cat "$S/$n-shim.pid")" 2>/dev/null
  left=$(find "$S/$n-tmp" -mindepth 1 | wc -l)
  echo "  $n: SYSTEM held in the scratch before the signal: $held | rc $rc | entries left $left | $(tr -d '\n ' < "$S/$n.json" | cut -c1-90)"
  check "$n: the copied SYSTEM was in the scratch when the signal came" "$([ "$held" = 1 ] && echo 0 || echo 1)"
  if [ "$n" = before ]; then
    check "before: the interrupted run leaves the scratch, SYSTEM in it (the positive)" "$([ "$left" -ge 2 ] && echo 0 || echo 1)"
  else
    check "after: the interrupted run removes the scratch and reports the value-free error, exit 2" "$([ "$left" = 0 ] && [ "$rc" = 2 ] && grep -q '"status": "error"' "$S/$n.json" && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi

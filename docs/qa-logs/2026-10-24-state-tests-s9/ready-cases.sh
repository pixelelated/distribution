#!/bin/bash
# ready-cases.sh -- T14 S9's control for #1000: the readiness predicate of the
# gate before the fix (the given copy) and the fixed one, run by ready-probe.py:
#   argument -- /usr/bin/autostart as an argument of another command
#   shipped  -- the shipped wrapper, exactly as systemd 255 prints it
# and the test's drift case: pixelelated-state-check-test --self-test from a
# scratch tree whose rocknix-autostart.service ExecStart is edited, run by the
# test before the fix and the fixed one; the scratch tree holds the two tools,
# the unit and ppsspp-sa's sources, the only tree files the test reads.
# Nothing outside the scratch.
#   ready-cases.sh <tree> <gate before> <test before> <scratch>
set -u
T="$(cd "$1" && pwd)"; GB="$(readlink -f "$2")"; TB="$(readlink -f "$3")"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S"
P="$T/docs/qa-logs/2026-10-24-state-tests-s9/ready-probe.py"; U=projects/ROCKNIX/packages/sysutils/autostart/system.d/rocknix-autostart.service
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
WRAP='/bin/bash -a -c source /etc/profile && exec /usr/bin/autostart'
for side in before:"$GB" after:"$T/tools/pixelelated-state-check"; do
  n=${side%%:*}; g=${side#*:}
  a=$(python3 -I "$P" "$g" /usr/bin/env "/usr/bin/env /usr/bin/autostart" 2>&1); b=$(python3 -I "$P" "$g" /bin/bash "$WRAP" 2>&1)
  echo "  $n: argument -> $a | shipped -> $b"
  check "$n: the shipped wrapper gets past the ExecStart check" "$(case "$b" in *ExecStart*|*autostart*) echo 1;; "REFUSED AT "*) echo 0;; *) echo 1;; esac)"
  if [ "$n" = before ]; then
    check "before: autostart as an argument gets past the ExecStart check (the positive)" "$(case "$a" in *ExecStart*) echo 1;; "REFUSED AT "*) echo 0;; *) echo 1;; esac)"
  else
    check "after: autostart as an argument is refused at the ExecStart check" "$([ "$a" = 'REFUSED AT require(runs_autostart(fields["ExecStart"]))' ] && echo 0 || echo 1)"
  fi
done
for side in before:"$TB" after:"$T/tools/pixelelated-state-check-test"; do
  n=${side%%:*}; t=${side#*:}; R="$S/$n-tree"; mkdir -p "$R/tools" "$R/$(dirname "$U")" "$S/$n-tmp"
  cp "$t" "$R/tools/pixelelated-state-check-test"; cp "$T/tools/pixelelated-state-check" "$R/tools/"; cp "$T/$U" "$R/$U"
  # the test also reads ppsspp-sa's shipped defaults from its tree
  PS=projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/sources; mkdir -p "$R/$PS"; cp -r "$T/$PS/." "$R/$PS/"
  sed -i 's#exec /usr/bin/autostart'"'"'$#exec /usr/bin/autostart --drifted'"'"'#' "$R/$U"; grep -q -- '--drifted' "$R/$U" || { echo "drift edit did not apply"; exit 2; }
  TMPDIR="$S/$n-tmp" python3 -I "$R/tools/pixelelated-state-check-test" --self-test > "$S/$n-drift.json" 2>&1; c=$?
  echo "  $n test over a drifted unit: rc $c ($(head -c 80 "$S/$n-drift.json" | tr '\n' ' '))"
  if [ "$n" = before ]; then check "before: the test passes a unit that drifted from the gate (the positive)" "$([ "$c" = 0 ] && echo 0 || echo 1)"
  else
    check "after: the test fails the drifted unit" "$([ "$c" != 0 ] && echo 0 || echo 1)"
    cp "$T/$U" "$R/$U"; TMPDIR="$S/$n-tmp" python3 -I "$R/tools/pixelelated-state-check-test" --self-test > "$S/$n-undrifted.json" 2>&1; d=$?
    check "after: the same scratch tree with the unit restored passes (the failure was the drift)" "$([ "$d" = 0 ] && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi

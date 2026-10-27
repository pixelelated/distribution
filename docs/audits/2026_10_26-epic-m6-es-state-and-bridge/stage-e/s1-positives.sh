#!/bin/bash
# T21 (#668) S1: state-units U1 to U3 and hostname-empty.py, against a
# state-fixture built from a given ES tree (the pin's, or the stream's).
#
#   bash s1-positives.sh <es tree> <scratch> <chksysconfig> <001-functions> <seed> <busybox> <os-release>
#
# Builds state-fixture as 02 § Positives names it (the tree's SystemConf.cpp
# and AtomicFileUtil.cpp, SystemConfTests' doubles), then prints each case.
# Values are masked; keys and counts only. Writes only under <scratch>.
set -uo pipefail
ES=${1:?es tree}; S=${2:?scratch}; CK=${3:?}; FN=${4:?}; SEED=${5:?}; BB=${6:?}; OSR=${7:?}
D=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$S"; F="$S/state-fixture"
g++ -std=c++17 -O0 -g -pthread -I "$ES/es-app/tests/unit/fakes" -I "$ES/es-core/src" -I "$ES/external" \
  "$D/stage-b/positives/state-fixture.cpp" "$ES/es-core/src/SystemConf.cpp" "$ES/es-core/src/utils/AtomicFileUtil.cpp" -o "$F" > "$S/build.log" 2>&1 \
  || { echo "BUILD FAIL"; tail -n 20 "$S/build.log"; exit 2; }
echo "== state-fixture built from $(git -C "$ES" rev-parse --short=10 HEAD)$(git -C "$ES" diff --quiet HEAD -- es-core || echo ' + the working tree')"
u="$S/units"; mkdir -p "$u"
echo "-- U1: an empty value (D-NET-009 writes system.hostname= on purpose)"
printf 'system.hostname=\n' > "$u/u1.cfg"; rm -f "$u/u1.cfg.backup"
"$F" parse "$u/u1.cfg" system.hostname; "$F" get "$u/u1.cfg" "$u/.lock" system.hostname
echo "-- U2: a value carrying a line end, set and saved by SystemConf"
printf 'system.hostname=qa\n' > "$u/u2.cfg"; rm -f "$u/u2.cfg.backup"; printf 'x\nroot.password=y' > "$u/u2.val"
"$F" set "$u/u2.cfg" "$u/.lock" qa.k "$u/u2.val"; echo "set rc $?"
echo "the file's lines, values masked:"; sed -E 's/=.*/=<value>/' "$u/u2.cfg"
printf 'root.password lines: %s\n' "$(grep -c '^root\.password=' "$u/u2.cfg")"
echo "-- U3: a key set to its table default (global.retroachievements.hardcore 0)"
printf 'system.hostname=qa\nglobal.retroachievements.hardcore=1\n' > "$u/u3.cfg"; rm -f "$u/u3.cfg.backup"; printf '0' > "$u/u3.val"
"$F" set "$u/u3.cfg" "$u/.lock" global.retroachievements.hardcore "$u/u3.val"; echo "set rc $?"
printf 'lines reading global.retroachievements.hardcore=0: %s\n' "$(grep -c '^global\.retroachievements\.hardcore=0' "$u/u3.cfg")"
echo "-- hostname-empty.py (stage C's chain)"
python3 -I -B "$D/stage-c/positives/hostname-empty.py" "$F" "$CK" "$FN" "$SEED" "$BB" "$OSR" "$S"

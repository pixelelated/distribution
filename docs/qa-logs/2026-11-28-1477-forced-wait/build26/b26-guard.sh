#!/bin/bash
# Guard for b26-carry.sh (the steward's 01:55 UTC observation): the chain goes
# on after #1477's proof whatever p1477.rc holds, so a failed proof would stop
# the handheld builds only if a lane were awake to write the hold file. This
# waits until run 20 has started (the chain checks the hold before run 20 and
# before each handheld launch; a hold before run 20 would also stop a run worth
# having), then checks what the proof left that a machine can read, and writes
# b26-carry/hold on any failure. The frames are still the coordinator's to
# review; this is the part that needs no lane.
C=/workspace/tmp/rocknix-session/b26-carry; P=/workspace/tmp/rocknix-session/p1477-b26; G=$C/guard.txt
end=$(( $(date +%s) + 5400 ))
until [ -f $C/standard-20.start ] || [ -f $C/STOPPED ] || [ -f $C/chain.rc ]; do [ "$(date +%s)" -ge $end ] && { echo "guard: run 20 never started" > $G; exit 3; }; sleep 15; done
fail=()
[ "$(cat $C/p1477.rc 2>/dev/null)" = 0 ] || fail+=("p1477.rc $(cat $C/p1477.rc 2>/dev/null || echo none)")
for l in en fr; do
    [ "$(cat $P/A-$l.rc 2>/dev/null)" = 0 ] || fail+=("A-$l rc $(cat $P/A-$l.rc 2>/dev/null || echo none)")
    j=$(ls $P/A-$l/time-to-play.json 2>/dev/null)
    if [ -n "$j" ]; then
        python3 -I - "$j" <<'PY' || fail+=("A-$l: no game frame after the wait, or no sync stamp")
import json, sys
b = json.load(open(sys.argv[1]))["cells"]["g2g-midsync"][0]
tok = (b.get("stamp_after") or "").split()
ok = b.get("t_second_game_frame") is not None and len(tok) >= 3 and tok[2] in ("completed", "cancelled")
sys.exit(0 if ok else 1)
PY
    else fail+=("A-$l: no time-to-play.json"); fi
    for x in B C; do
        t=$P/$x-$l.launch.txt
        grep -q 'http 200' $t 2>/dev/null || fail+=("$x-$l: the launch POST did not answer 200")
        grep -q -E '^retroarch: [0-9]+' $t 2>/dev/null || fail+=("$x-$l: no game running after the wait")
        grep -q -E '^last-sync-startup: [0-9]+ [0-9]+ (completed|cancelled)' $t 2>/dev/null || fail+=("$x-$l: no startup sync stamp")
    done
    grep -q -E '^pending now: 0$' $P/C-$l.launch.txt 2>/dev/null || fail+=("C-$l: the held award was not sent")
done
if [ ${#fail[@]} -gt 0 ]; then
    printf '%s\n' "$(date -u +%FT%TZ) the guard held the handheld builds: #1477's proof on build 26 failed a machine check: ${fail[*]}" > $C/hold
    { echo "$(date -u +%FT%TZ) HOLD"; printf '  %s\n' "${fail[@]}"; } > $G
else
    echo "$(date -u +%FT%TZ) PASS: every machine check of #1477's proof on build 26 passed; frames still for review" > $G
fi

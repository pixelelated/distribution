#!/bin/bash
# After b26-carry.sh (held by b26-guard.sh at 02:05 UTC: #1477's cases B and C
# launched a ROM the case A cell had removed -- the proof's fault, not the
# product's): every step gated by machine on the one before (#1507) --
#   1 b26-carry's run 20 finished with VERDICT PASS, then rc-preflight;
#   2 #1477's cases B and C again (p1477-bc.sh exits 1 on any failed check);
#   3 H700 cold from 6169621a4b, its reads; then SM8550 cold, its reads.
# A coordinator hold (b26-handhelds/hold) stops it before a handheld launch.
# Host builds and VM tests only (D-WORKFLOW-196); nothing on a handheld or in a cloud.
C=/workspace/tmp/rocknix-session/b26-handhelds; mkdir -p "$C"
B=/workspace/tmp/rocknix-session/b26-carry
NEXT=/workspace/repos/rocknix; ROUND=/workspace/repos/rocknix.worktrees/m7-rc-round-20261125; HEAD=6169621a4b
ES=/workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/m7-rc-round-20261128-16-es/inputs/es
stop() { echo "$(date -u +%FT%TZ) stopped at $1: $2" > "$C/STOPPED"; echo 1 > "$C/chain.rc"; exit 1; }
held() { [ -f "$C/hold" ] && stop "$1" "held by the coordinator: $(cat $C/hold)"; }
mark() { date -u +%FT%TZ > "$C/$1.$2"; }
wait_file() { local end=$(( $(date +%s) + $2 )); until [ -f "$1" ]; do [ "$(date +%s)" -ge $end ] && return 1; sleep 30; done; }

# 1
wait_file "$B/chain.rc" 5400 || stop run20 "b26-carry ended no chain.rc within 90 min"
rep=$(grep -o '/workspace/artifacts/rocknix-images/qa-[^ ]*report.md' "$B/standard-20.log" | head -1); echo "$rep" > "$C/run20-report.txt"
[ "$(cat $B/standard-20.rc 2>/dev/null)" = 0 ] && grep -q '^\*\*VERDICT: PASS\*\*' "$rep" || stop run20 "rc $(cat $B/standard-20.rc 2>/dev/null), $(grep -m1 VERDICT "$rep" 2>/dev/null)"
(cd $NEXT && python3 -I tools/rc-preflight --tree "$ROUND" --only vm-qa --build-set /workspace/repos/rocknix.worktrees/m7-round-x64-20261125/target) > "$C/rc-preflight.txt" 2>&1 || stop rc-preflight "$(tail -2 $C/rc-preflight.txt | tr '\n' ' ')"
# 2
pgrep -f 'qemu-system-x86_6[4]' >/dev/null && stop proof "a QEMU guest is still up"
mark proof start; rm -rf /workspace/tmp/rocknix-session/p1477-bc
/workspace/tmp/rocknix-session/p1477-bc.sh > "$C/proof.console" 2>&1; prc=$?; echo $prc > "$C/proof.rc"; mark proof end
[ "$prc" = 0 ] || stop proof "p1477-bc rc $prc: $(tr '\n' ';' < /workspace/tmp/rocknix-session/p1477-bc/FAILED 2>/dev/null)"
# 3
for dev in H700 SM8550; do
    held "$dev launch"
    name=m7-round-$(echo $dev | tr A-Z a-z)-20261128
    mark $dev start
    (cd $NEXT && python3 -I tools/device-build --device $dev --commit $HEAD --es-supplier $ES --set m7-round-x64 --move-set --name $name --dry-run) > "$C/$dev-dryrun.txt" 2>&1 ||
        stop "$dev dry run" "$(grep -E 'refus|ERROR|cannot' $C/$dev-dryrun.txt | head -2 | tr '\n' ' ')"
    (cd $NEXT && python3 -I tools/device-build --device $dev --commit $HEAD --es-supplier $ES --set m7-round-x64 --move-set --name $name) > "$C/$dev-launch.txt" 2>&1 ||
        stop "$dev launch" "$(tail -3 $C/$dev-launch.txt | tr '\n' ' ')"
    rd=$(sed -n 's/.*run directory \([^:]*\): build.pid.*/\1/p' "$C/$dev-launch.txt" | head -1)
    [ -d "$rd" ] || stop "$dev launch" "no run directory in the launch output"
    echo "$rd" > "$C/$dev-run-dir.txt"
    wait_file "$rd/build.rc" 36000 || stop "$dev build" "no build.rc within 10 h ($rd)"
    brc=$(cat "$rd/build.rc"); echo "$brc" > "$C/$dev-build.rc"; mark $dev end
    /workspace/tmp/rocknix-session/handheld-reads.sh $dev "$rd" "/workspace/repos/rocknix.worktrees/$name" "$C/image-reads-$dev.txt" > /dev/null 2>&1
    [ "$brc" = 0 ] || stop "$dev build" "build.rc $brc ($rd)"
done
echo 0 > "$C/chain.rc"

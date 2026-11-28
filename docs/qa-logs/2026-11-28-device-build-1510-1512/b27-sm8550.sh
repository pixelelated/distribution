#!/bin/bash
# The SM8550 build of the round's final head 6169621a4b, after the 06:27 refusal (#1512),
# with the device-build proofs that need an idle host first (#1510, #1512).
# Every step is gated by machine on the one before (tools/chain-lib, #1507); a stop writes
# the chain's friction stub (#1508). b27-sm8550/hold stops it before the next step.
#   p1  #1510 c1: H700 dry run on the used owner folder m7-round-h700-20261128-owner: exit 2
#   p2  #1510 c2 and #1512 c1's control: SM8550 dry run on an unused name: exit 0
#   p3  #1512 c1: the same dry run with a holder under H700's root: exit 2, naming it
#   p4  #1510 c3: a real SM8550 launch on the used owner folder: exit 2, set file unchanged
#   p5  #1512 c2: a real launch with a holder: exit 2, nothing written, set file unchanged
#   then SM8550 cold under -02 (#1512 c4); build.rc 0; its reads; duckstation-sa's pin.
# Host builds only (D-WORKFLOW-196); nothing on a handheld or in a cloud.
. /workspace/repos/rocknix/tools/chain-lib
chain_init /workspace/tmp/rocknix-session/b27-sm8550 b27-sm8550
C=$CHAIN_DIR
NEXT=/workspace/repos/rocknix; HEAD=6169621a4b
ES=/workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/m7-rc-round-20261128-16-es/inputs/es
PIN=f92319a0484e67bb62bfab7b0e56dac46165b50e45b51293038d9344a6288440
WT=/workspace/repos/rocknix.worktrees/m7-round-sm8550-20261128
H7=/workspace/repos/rocknix.worktrees/m7-round-h700-20261128
SET=/workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/build-sets/m7-round-x64.json
OWN=/workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs
HOLDER=
trap '[ -n "$HOLDER" ] && kill "$HOLDER" 2>/dev/null' EXIT

db() { (cd $NEXT && python3 -I tools/device-build --commit $HEAD --es-supplier $ES --set m7-round-x64 "$@"); }
# expect RC PATTERN -- command...: the command's exit is RC and its output carries PATTERN
expect() {
    local want=$1 pat=$2 rc; shift 2; [ "$1" = -- ] && shift
    "$@"; rc=$?
    echo "== exit $rc (want $want)"
    [ "$rc" = "$want" ] || return 1
    [ -z "$pat" ] || grep -q -E "$pat" "$C/$STEP.log" || { echo "== no line matching: $pat"; return 1; }
}
holder_on() { ( cd "$H7/build.pixelelated-H700.aarch64/.ccache" && exec sleep 600 ) & HOLDER=$!; sleep 1; echo "holder pid $HOLDER: $(tr '\0' ' ' < /proc/$HOLDER/cmdline) in $(readlink /proc/$HOLDER/cwd)"; }
holder_off() { kill "$HOLDER" 2>/dev/null; wait "$HOLDER" 2>/dev/null; HOLDER=; }
setm() { stat -c '%y %n' "$SET"; }
duck() { # duck WORKTREE -> the image's duckstation-sa sha256
    local X=/workspace/tmp/rocknix-session/duck-SM8550 tar sys
    rm -rf "${X:?}"; mkdir -p "$X"
    tar=$(ls "$1"/target/*.g${HEAD}*.tar 2>/dev/null | head -1); [ -n "$tar" ] || return 1
    ( cd "$X" && tar -xf "$tar" --wildcards '*/target/SYSTEM' ) || return 1
    sys=$(find "$X" -name SYSTEM -type f | head -1)
    unsquashfs -q -d "$X/sys" "$sys" usr/bin/duckstation-sa > /dev/null 2>&1 || return 1
    sha256sum "$X/sys/usr/bin/duckstation-sa" | cut -c1-64; rm -rf "${X:?}"
}

STEP=p1; step p1 -- expect 2 'one owner folder per launch' -- \
    db --device H700 --name m7-round-h700-20261128 --worktree $H7 --warm --dry-run
STEP=p2; step p2 -- expect 0 'DRY RUN: nothing was created or changed' -- \
    db --device SM8550 --name m7-round-sm8550-20261128-02 --worktree $WT --dry-run
p3() { holder_on; expect 2 'could not remove it \(waited 120 s\)' -- \
    db --device SM8550 --name m7-round-sm8550-20261128-02 --worktree $WT --dry-run; local r=$?; holder_off
    grep -q -E 'started [0-9TZ:-]+: sleep 600' "$C/p3.log" || { echo "== the refusal does not name the holder"; return 1; }; return $r; }
STEP=p3; step p3 -- p3
p4() { local a b; a=$(setm); echo "set before: $a"
    expect 2 'one owner folder per launch' -- db --device SM8550 --name m7-round-sm8550-20261128 --worktree $WT; local r=$?
    b=$(setm); echo "set after:  $b"; [ "$a" = "$b" ] || { echo "== the set file changed"; return 1; }; return $r; }
STEP=p4; step p4 -- p4
p5() { local a b r; a=$(setm); echo "set before: $a"; holder_on
    expect 2 'could not remove it \(waited 120 s\)' -- db --device SM8550 --name m7-round-sm8550-20261128-02 --worktree $WT; r=$?; holder_off
    grep -q -E 'started [0-9TZ:-]+: sleep 600' "$C/p5.log" || { echo "== the refusal does not name the holder"; return 1; }
    b=$(setm); echo "set after:  $b"; [ "$a" = "$b" ] || { echo "== the set file changed"; return 1; }
    ls -la "$OWN/m7-round-sm8550-20261128-02-owner" 2>&1
    for f in retention-plan.json admission-plan.json admission.json retention-report.json; do
        [ -e "$OWN/m7-round-sm8550-20261128-02-owner/$f" ] && { echo "== $f was written"; return 1; }; done
    echo "== no plans, no admission in the -02 owner folder"; return $r; }
STEP=p5; step p5 -- p5

held "SM8550 launch"
mark SM8550 start
db --device SM8550 --name m7-round-sm8550-20261128-02 --worktree $WT > "$C/SM8550-launch.txt" 2>&1 ||
    stop "SM8550 launch" "$(tail -n 3 "$C/SM8550-launch.txt" | tr '\n' ' ')"
rd=$(sed -n 's/.*run directory \([^:]*\): build.pid.*/\1/p' "$C/SM8550-launch.txt" | head -1)
[ -d "$rd" ] || stop "SM8550 launch" "no run directory in the launch output"
echo "$rd" > "$C/SM8550-run-dir.txt"
wait_file "$rd/build.rc" 43200 || stop "SM8550 build" "no build.rc within 12 h ($rd)"
brc=$(cat "$rd/build.rc"); echo "$brc" > "$C/SM8550-build.rc"; mark SM8550 end
[ "$brc" = 0 ] || stop "SM8550 build" "build.rc $brc ($rd)"
/workspace/tmp/rocknix-session/handheld-reads.sh SM8550 "$rd" "$WT" "$C/image-reads-SM8550.txt" > /dev/null 2>&1
grep -q "BUILD_ID=.*$HEAD" "$C/image-reads-SM8550.txt" || stop "SM8550 reads" "no BUILD_ID naming $HEAD in the image reads"
d=$(duck "$WT"); echo "duckstation-sa sha256 $d (pin $PIN)" > "$C/duck-SM8550.txt"
[ "$d" = "$PIN" ] || stop "SM8550 reads" "duckstation-sa sha256 '$d' is not the aarch64 pin"
chain_done

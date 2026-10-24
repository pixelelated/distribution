#!/bin/bash
# suites.sh -- T14's close-out: every one of the slice's 21 tools at the fixed
# tip, with its exit and wall time, as stage A ran them (02 § The runs), plus
# S2's environment case (sandbox-case.py, the caller's TMPDIR, RCLONE_*,
# BASH_ENV and a function exported) and the cloud-layout historical matrix.
# Each output lands under the scratch; the table goes to stdout. No guest; the
# build root is read and executed from only.
#   suites.sh <tree> <image rclone> <image busybox, under a build root's image/system> <ES clone at the pin> <wrapper source> <stage-D tools dir> <scratch>
set -u
T="$(cd "$1" && pwd)"; RC="$2"; BB="$3"; ES="$4"; WS="$5"; OLD="$6"; S="$7"; rm -rf "${S:?}"; mkdir -p "$S/tmp"
export TMPDIR="$S/tmp"
cd "$T" || exit 2
n=0
row() {  # <label> <command...>: runs it, prints a row; output in $S/<n>.txt
  local label=$1 t0 t1 rc; shift; n=$((n + 1))
  t0=$(date +%s%N); "$@" > "$S/$n.txt" 2>&1; rc=$?; t1=$(date +%s%N)
  local ds=$(( (t1 - t0) / 100000000 ))
  printf '| %s | %s | %d.%d s | %s |\n' "$label" "$rc" "$((ds / 10))" "$((ds % 10))" \
    "$(grep -v '^\s*$' "$S/$n.txt" | tail -1 | tr '|' '/' | cut -c1-110)"
}
PROF=projects/ROCKNIX/packages/rocknix/profile.d/001-functions; CK=projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
PU=projects/ROCKNIX/packages/rocknix/sources/post-update
echo '| Run | Exit | Wall | Last line |'
echo '| --- | ---: | ---: | --- |'
row 'wait-lock-test --busybox <image>' bash tools/wait-lock-test --busybox "$BB"
row 'wait-lock-test (host tools)' bash tools/wait-lock-test
row 'rocknix-info-test' python3 -I -B tools/rocknix-info-test
row 'nova-led-test' python3 -I -B tools/nova-led-test
row 'usb-gadget-test --output' python3 -I -B tools/usb-gadget-test --output "$S/usb"
row 'pixelelated-state-check-test --self-test' python3 -I -B tools/pixelelated-state-check-test --self-test
row 'pixelelated-state-check-test --payload-tests (no mcopy here)' python3 -I -B tools/pixelelated-state-check-test --payload-tests
row 'pixelelated-state-check --help' python3 -I -B tools/pixelelated-state-check --help
row 'build-identity-test --output' python3 -I -B tools/build-identity-test --output "$S/build-identity"
row 'retroarch-wrapper-test <source>' python3 -I -B tools/retroarch-wrapper-test "$WS"
row 'retroarch-wrapper-test (bare)' env -u RETROARCH_SRC python3 -I -B tools/retroarch-wrapper-test
row 'rasteratops-identity-check --tree --es' tools/rasteratops-identity-check --tree "$T" --es "$ES"
row 'settings-modes-test --busybox <image>' python3 -I -B tools/settings-modes-test --profile "$PROF" --chksysconfig "$CK" --busybox "$BB" --output "$S/settings.json"
row 'settings-modes-test --busybox <host> (refused)' python3 -I -B tools/settings-modes-test --profile "$PROF" --chksysconfig "$CK" --busybox /usr/bin/busybox --output "$S/settings-host.json"
row 'melonds-upgrade-test --busybox <image>' python3 -I -B tools/melonds-upgrade-test --post-update "$PU" --busybox "$BB" --output "$S/melonds.json"
row 'melonds-upgrade-test --busybox <host> (refused)' python3 -I -B tools/melonds-upgrade-test --post-update "$PU" --busybox /usr/bin/busybox --output "$S/melonds-host.json"
row 'rasteratops-cloud-layout-test --archives-only, TMPDIR set' python3 -I -B tools/rasteratops-cloud-layout-test --source-root "$T" --rclone "$RC" --output "$S/layout" --archives-only
row 'rasteratops-cloud-layout-test --ref 22571b47d2 (the historical matrix)' python3 -I -B tools/rasteratops-cloud-layout-test --ref 22571b47d2 --rclone "$RC" --output "$S/layout-hist"
row 'pixelelated-cloud-validator-test --rclone <image>' python3 -I -B tools/pixelelated-cloud-validator-test --rclone "$RC" --output "$S/validator"
row 'pixelelated-content-scope-test' python3 -I -B tools/pixelelated-content-scope-test --source-root "$T" --rclone "$RC" --output "$S/scope"
row 'pixelelated-save-layout-test --busybox <image>' python3 -I -B tools/pixelelated-save-layout-test --source-root "$T" --rclone "$RC" --busybox "$BB" --output "$S/save-layout"
row 'pixelelated-duckstation-capture-test' python3 -I -B tools/pixelelated-duckstation-capture-test --source-root "$T" --rclone "$RC" --output "$S/duckstation"
row 'pixelelated-cloud-folder-test (bare)' python3 -I -B tools/pixelelated-cloud-folder-test
row 'pixelelated-cloud-folder-vm-test (bare)' python3 -I -B tools/pixelelated-cloud-folder-vm-test
row 'rasteratops-vm-cloud-epic --output (refuses current source)' bash tools/rasteratops-vm-cloud-epic --output "$S/epic"
mkdir -p "$S/pair-out"
row 'pixelelated-vm-cloud-boundaries (bare)' python3 -I -B tools/pixelelated-vm-cloud-boundaries
row 'pixelelated-vm-cloud-boundaries --tree <current> (refuses, #508)' python3 -I -B tools/pixelelated-vm-cloud-boundaries --tree "$T" --image "$S/no-such.img.gz" --build-id x --output "$S/pair-out"
row 'rasteratops-candidate-store --help' python3 -I -B tools/rasteratops-candidate-store --help
mkdir -p "$S/s2"
row 'S2 environment case (sandbox-case.py, fixed tools)' python3 -I -B docs/qa-logs/2026-10-24-state-tests-s2/sandbox-case.py --tools "$T/tools" --source-root "$T" --rclone "$RC" --scratch "$S/s2"
echo
echo "busybox: $("$BB" 2>&1 | head -1) at $BB, sha256 $(sha256sum < "$BB" | cut -c1-16); the image's BUILD_ID $(sed -n 's/^BUILD_ID="\(.*\)"/\1/p' "${BB%/usr/bin/busybox}/etc/os-release")"
echo "rclone: $("$RC" version 2>/dev/null | head -1) at $RC"
ls -d "$T/tools/__pycache__" 2>/dev/null && echo "WARNING: tools/__pycache__ written"
exit 0

#!/bin/bash
set -uo pipefail
export TMPDIR=/workspace/tmp
python3 -u "/workspace/tmp/pixelelated-510-coverage02/build04/build.py"
rc=$?
if [ "$rc" -eq 0 ]; then
 cmake -S "/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup/es-app/tests/unit" -B "/workspace/tmp/pixelelated-510-coverage02/build04/unit" -DRAPIDJSON_INCLUDE_DIR=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64/toolchain/x86_64-rocknix-linux-gnu/sysroot/usr/include > "/workspace/tmp/pixelelated-510-coverage02/build04/artifacts/unit.log" 2>&1 && cmake --build "/workspace/tmp/pixelelated-510-coverage02/build04/unit" --target es-unit-tests -j1 >> "/workspace/tmp/pixelelated-510-coverage02/build04/artifacts/unit.log" 2>&1 && "/workspace/tmp/pixelelated-510-coverage02/build04/unit/es-unit-tests" >> "/workspace/tmp/pixelelated-510-coverage02/build04/artifacts/unit.log" 2>&1
 rc=$?
fi
printf "%s\n" "$rc" > "/workspace/tmp/pixelelated-510-coverage02/build04/inner.rc"
exit "$rc"

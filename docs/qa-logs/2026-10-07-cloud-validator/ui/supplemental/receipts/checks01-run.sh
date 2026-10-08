#!/bin/bash
set -uo pipefail
export TMPDIR=/workspace/tmp
TOOL=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64/toolchain/bin
SRC=/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup
OUT=/workspace/tmp/pixelelated-510-coverage02/checks01
"$TOOL/cmake" -G Ninja -S "$SRC/es-app/tests/unit" -B "$OUT/unit" -DCMAKE_MAKE_PROGRAM="$TOOL/ninja" -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DRAPIDJSON_INCLUDE_DIR=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64/toolchain/x86_64-rocknix-linux-gnu/sysroot/usr/include && "$TOOL/cmake" --build "$OUT/unit" --target es-unit-tests -j1 && "$OUT/unit/es-unit-tests"
rc=$?
if [ "$rc" -eq 0 ]; then
 /workspace/repos/rocknix.worktrees/conflict-resolution/tools/es-syntax-check --root /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64 --tree "$SRC" "$SRC/es-app/src/CloudText.cpp" "$SRC/es-app/src/guis/GuiCloudTransfer.cpp"
 rc=$?
fi
printf "%s\n" "$rc" > "$OUT/inner.rc"
exit "$rc"

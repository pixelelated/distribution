#!/bin/bash
set -uo pipefail
export TMPDIR=/workspace/tmp
/workspace/repos/rocknix.worktrees/conflict-resolution/tools/es-syntax-check --root /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64 --tree /home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup /home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup/es-app/src/guis/GuiMenu.cpp
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-510-coverage02/checks03/inner.rc
exit "$rc"

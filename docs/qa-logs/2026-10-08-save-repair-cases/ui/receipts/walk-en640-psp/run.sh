#!/bin/bash
set -uo pipefail
export TMPDIR=/workspace/tmp
python3 /workspace/repos/rocknix.worktrees/conflict-resolution/tools/vm-visual-qa --monitor /tmp/pix520-mon.sock run /workspace/tmp/pixelelated-520-ui-20261008/walk-en640-psp/steps.txt --outdir /workspace/tmp/pixelelated-520-ui-20261008/walk-en640-psp/frames
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/walk-en640-psp/inner.rc
exit "$rc"

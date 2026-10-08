#!/bin/bash
set -uo pipefail
ssh -i /workspace/tmp/pixelelated-520-ui-20261008/guest01/qa-key -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1 'python3 -' < /workspace/tmp/pixelelated-520-ui-20261008/capture-custom01/guest.py > /workspace/tmp/pixelelated-520-ui-20261008/capture-custom01/capture.json
rc=$?
python3 /workspace/repos/rocknix.worktrees/conflict-resolution/tools/vm-visual-qa --monitor /tmp/pix520-mon.sock shot /workspace/tmp/pixelelated-520-ui-20261008/capture-custom01/native-hotkey.png
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/capture-custom01/inner.rc
exit "$rc"

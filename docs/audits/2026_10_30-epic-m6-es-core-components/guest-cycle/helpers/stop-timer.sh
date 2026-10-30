#!/bin/bash
# T34 (#681): the window's detached stop, 35 minutes (2100 s) after it is armed at START.
echo $$ > /workspace/tmp/m6-t34/guest/timer.pid
sleep 2100
echo "$(date -u +%FT%TZ) timer fired: tools/vm-stop /workspace/tmp/m6-t34/guest/qemu.pid /workspace/tmp/m6-t34/guest/disk.qcow2"
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-core-components-681 && tools/vm-stop --timeout 90 /workspace/tmp/m6-t34/guest/qemu.pid /workspace/tmp/m6-t34/guest/disk.qcow2
echo "$(date -u +%FT%TZ) vm-stop rc=$?"

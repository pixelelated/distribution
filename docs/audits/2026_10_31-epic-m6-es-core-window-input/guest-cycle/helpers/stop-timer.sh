#!/bin/bash
# T35 (#682): the window's detached stop, 35 minutes (2100 s) after it is armed at START (T34's, adapted).
echo $$ > /workspace/tmp/m6-t35/guest/timer.pid
sleep $(( $(date -d "2026-10-31T11:42:41Z" +%s) - $(date +%s) ))
echo "$(date -u +%FT%TZ) timer fired: tools/vm-stop /workspace/tmp/m6-t35/guest/qemu.pid /workspace/tmp/m6-t35/guest/disk.qcow2"
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-core-window-input-682 && tools/vm-stop --timeout 60 /workspace/tmp/m6-t35/guest/qemu.pid /workspace/tmp/m6-t35/guest/disk.qcow2
echo "$(date -u +%FT%TZ) vm-stop rc=$?"

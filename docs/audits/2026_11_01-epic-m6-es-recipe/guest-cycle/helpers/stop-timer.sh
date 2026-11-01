#!/bin/bash
# T37 (#684): the window's detached stop (T36's shape). Arg 1 is the deadline (epoch seconds): at it,
# the guest is stopped by its pidfile through tools/vm-stop, whatever step the window is in.
echo $$ > /workspace/tmp/m6-t37/guest/timer.pid
DL=$1
sleep $(( DL - $(date +%s) ))
echo "$(date -u +%FT%TZ) timer fired: vm-stop /workspace/tmp/m6-t37/guest/qemu.pid"
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 && tools/vm-stop --timeout 60 /workspace/tmp/m6-t37/guest/qemu.pid /workspace/tmp/m6-t37/guest/disk.qcow2
echo "$(date -u +%FT%TZ) vm-stop rc=$?"

#!/bin/bash
# T36 (#683): the window's detached stop. Arg 1 is the deadline (epoch seconds); it stops the
# guest by its pidfile at the deadline, whatever step the window is in. Its PID is in timer.pid.
echo $$ > /workspace/tmp/m6-t36/guest/timer.pid
DL=$1
sleep $(( DL - $(date +%s) ))
echo "$(date -u +%FT%TZ) timer fired: vm-stop /workspace/tmp/m6-t36/guest/qemu.pid"
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-core-utils-resources-683 && tools/vm-stop --timeout 60 /workspace/tmp/m6-t36/guest/qemu.pid /workspace/tmp/m6-t36/guest/disk.qcow2
echo "$(date -u +%FT%TZ) vm-stop rc=$?"

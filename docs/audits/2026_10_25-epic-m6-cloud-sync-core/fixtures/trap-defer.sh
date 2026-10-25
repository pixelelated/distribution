#!/bin/bash
# T16 lead 12: a TERM to a bash script waits for its foreground child, as cloud_backup's
# automatic run's `command timeout -k 3 <left> rclone ...` is. `sleep` stands in for rclone.
trap 'echo "trap ran at +$(( $(date +%s) - T0 ))s"; exit 130' INT TERM
T0=$(date +%s); timeout -k 3 6 sleep 30; echo "child returned at +$(( $(date +%s) - T0 ))s"

#!/usr/bin/bash
# Preserve the original guest batch process exit outside that process.
set -u
packet=/tmp/pix-input/dolphin/batch
output=$1
/usr/bin/python3 -I -S -B "$packet/guest-batch.py" run
result=$?
printf '%s\n' "$result" > "$output/batch-session.exit.pending"
/usr/bin/mv "$output/batch-session.exit.pending" "$output/batch-session.exit"
exit "$result"

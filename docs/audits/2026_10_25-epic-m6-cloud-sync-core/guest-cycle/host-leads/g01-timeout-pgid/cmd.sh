#!/bin/bash
# G-01 (Astra): does a stop of the script's process group reach an automatic call's
# `timeout -k 3 N rclone ...`? GNU timeout without --foreground makes its own group.
# The image's coreutils is GNU 9.4; this host's gnutimeout is GNU 9.7. `sleep` stands for rclone.
echo "== $(date -u +%FT%TZ) $(gnutimeout --version | head -1)"
setsid bash -c 'gnutimeout 6 sleep 5 & T=$!; sleep 0.3; C=$(pgrep -P $T)
  printf "%s %s\n" "$T" "$C" > /workspace/tmp/m6-t16/g01.pids
  echo "script pid $$ pgid $(ps -o pgid= -p $$ | tr -d " ")"
  echo "timeout pid $T pgid $(ps -o pgid= -p $T | tr -d " ")"
  echo "child (rclone stand-in) pid $C pgid $(ps -o pgid= -p $C | tr -d " ")"
  wait' &
OUTER=$!
sleep 0.6
read -r T C < /workspace/tmp/m6-t16/g01.pids
G=$(ps -o pgid= -p "$OUTER" | tr -d ' ')
kill -TERM -- "-$G"; echo "TERM to the script's group -$G"
sleep 0.5
echo "after: script $(kill -0 "$OUTER" 2>/dev/null && echo alive || echo gone); timeout $(kill -0 "$T" 2>/dev/null && echo alive || echo gone); child $(kill -0 "$C" 2>/dev/null && echo alive || echo gone)"
sleep 6
echo "after timeout's own 6 s: child $(kill -0 "$C" 2>/dev/null && echo alive || echo gone)"

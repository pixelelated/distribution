#!/bin/bash
# Lead (d): does rclone 1.75.2 know --progress-terminal-width? cloud_restore:1893 and :2028, and
# cloud_backup:2054, add it only when `rclone help | grep -q progress-terminal-width` matches.
. /workspace/tmp/m6-t16/hl/lib.sh
R=${DONOR}/usr/bin/rclone
header "(d) --progress-terminal-width"
echo "\$ rclone help | grep -c progress-terminal-width   (the scripts' test)"; "${R}" help 2>/dev/null | grep -c progress-terminal-width
echo "\$ rclone help flags | grep -c -- --progress-terminal-width"; "${R}" help flags 2>/dev/null | grep -c -- --progress-terminal-width
echo "\$ rclone help flags | grep -c -- '--progress'   (the family is listed there)"; "${R}" help flags 2>/dev/null | grep -c -- '--progress'
D=$(mktemp -d "${HL}/cells/d.XXXXXX")
echo "\$ rclone lsf <empty dir> --progress-terminal-width=80"; "${R}" lsf "${D}" --progress-terminal-width=80 > "${D}.err" 2>&1; echo "rc=$?"; head -2 "${D}.err"
echo "\$ rclone lsf <empty dir>   (the control)"; "${R}" lsf "${D}"; echo "rc=$?"
echo "the scripts' probe, timed on this host (not the device's figure; lead (c) is (window)-pending):"
for i in 1 2 3; do s=$(date +%s%N); "${R}" help 2>/dev/null | grep -q progress-terminal-width; rc=$?; e=$(date +%s%N); echo "  rclone help | grep -q: $(( (e - s) / 1000000 )) ms, grep rc=${rc}"; done
echo "== end $(now)"

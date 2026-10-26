#!/bin/bash
# T17 stage C: re-read each Astra item at its lines, at 8ebaf8daad, masked (D-QA-021).
# bash docs/audits/2026_10_26-epic-m6-cloud-setup-content/stage-c/rereads/rereads.sh <group>
set -uo pipefail
R=8ebaf8daad
RC=projects/ROCKNIX/packages/network/rclone/sources
BT=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
SW=projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
show() { # show <path> <a> <b>
  echo "== $1:$2-$3"; git show "${R}:$1" | awk -v a="$2" -v b="$3" 'NR>=a && NR<=b {printf "%5d  %s\n", NR, $0}' | mask; }
case "$1" in
  c01) show $RC/cloud_remote 255 270; show $RC/cloud_remote 318 345; show $RC/cloud_connections.py 135 200 ;;            # A-45, A-50, A-1, A-17
  c02) show $RC/cloud_content_restore 1265 1300; show $RC/cloud_content_restore 1395 1420; show $RC/cloud_content_restore 430 450 ;;  # A-46, A-19/A-35, A-33
  c03) show $RC/cloud_setup 488 560 ;;                                                                                 # A-47, A-4, A-32
  c04) show $RC/cloud_scan 300 362 ;;                                                                                   # A-48, A-21
  c05) show $BT 1170 1190; show $BT 1280 1350; show $BT 640 665 ;;                                                      # A-49, A-23
  c06) show $RC/cloud_content_backup 700 760; show $RC/cloud_content_backup 570 600; git show "${R}:$RC/cloud_content_backup" | grep -n 'remote_for()' | mask ;;  # A-15, A-28
  c07) show $RC/cloud_oauth 470 495; show $RC/cloud_oauth 2265 2310; show $RC/cloud_oauth 2440 2470 ;;                   # A-14, A-34, A-50
  c08) show $RC/cloud_oauth 2300 2330; show $RC/cloud_oauth 2395 2420; git show "${R}:$RC/cloud_oauth" | grep -n -E 'MAX_CONNECTIONS|REQUEST_TIMEOUT|DEFAULT_SERVE|Content-Length|max_body|serve_timeout|600' | mask ;;  # A-13
  c09) show $RC/cloud_setup 765 785; show $RC/cloud_oauth 350 365; show $RC/cloud_oauth 2812 2830; show $RC/cloud_remote 98 106 ;;  # A-11
  c10) show $RC/cloud_connections.py 40 135; show $RC/cloud_connections.py 215 258 ;;                                   # A-17, A-18, A-40
  c11) show $SW 525 540; show $SW 845 870; git show "${R}:$SW" | grep -n -E 'ephemeral|create-web-view|popup|new_window|"create"' | mask ;;  # A-37, A-12
  c12) git show "${R}:$RC/cloud_content_backup" | grep -n -E 'RCLONE_NET_OPTS' | mask; git show "${R}:$RC/cloud_content_transfer" | grep -n -E 'rclone ' | mask; grep -rn --include='*' -E 'bounded_content_rclone ' $(git ls-tree -r --name-only $R -- $RC | sed "s|^|./|") 2>/dev/null | true; for f in cloud_content_backup cloud_content_restore cloud_content_transfer; do git show "${R}:$RC/$f" | grep -n 'bounded_content_rclone' | sed "s|^|$f:|" | mask; done ;;  # A-9, A-16
  c14) show $RC/cloud_oauth 440 452; show $RC/cloud_log_scrub 60 125; show $RC/cloud_log_scrub 160 190; show $RC/cloud_oauth 2700 2716; show $SW 528 536 ;;  # A-5, A-22, A-20, A-37
  c15) show $RC/cloud_log_scrub 186 206; git show "${R}:$RC/cloud_oauth" | grep -n -E 'def log_message|def log_request|log_message\(' | mask; show $RC/cloud_scan 250 282; show $RC/cloud_device_id 262 280; git show "${R}:$BT" | sed -n '1283,1287p' | mask ;;  # Argon R-6/R-49, R-4, R-17, R-44, R-45
  *) echo "usage: $0 c01..c15 (c13 is tools/t17-option-key-fixture.py)" >&2; exit 2 ;;
esac

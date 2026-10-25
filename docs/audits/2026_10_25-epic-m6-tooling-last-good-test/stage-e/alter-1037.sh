#!/bin/bash
# #1037: S3F's subjects absent. Must FAIL on the fixed file, PASS on the unfixed:
#   "conf_valid is one text in cloud_backup, cloud_restore and cloud_sync_helper"
#   "a producer that fails after the hostname line installs nothing"
#   "an ack for token A over a marker holding B keeps B in place"
. "$(dirname "$0")/alter-lib.sh"
for s in cloud_backup cloud_restore cloud_sync_helper; do drop_fn "${R}/network/rclone/sources/${s}" '^conf_valid\(\) *\{'; done
drop_fn "${R}/rocknix/profile.d/001-functions" '^function sort_settings\(\) \{'
drop_fn "${R}/network/raofflineproxy/sources/raofflineproxy-ctl" '^ack_index_pending\(\) *\{'

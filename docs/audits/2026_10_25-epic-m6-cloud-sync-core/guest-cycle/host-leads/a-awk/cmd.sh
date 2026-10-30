#!/bin/bash
# Lead (a): which awk the scripts get, and whether it has gensub. 04 Q2: cloud_sync_cleanup_duplicates.sh
# calls gensub; cloud_restore's near_names comment (:764-765) says busybox awk has none; A48 passes.
. /workspace/tmp/m6-t16/hl/lib.sh
header "(a) awk and gensub"
echo "\$ readlink ${DONOR}/usr/bin/awk"; readlink "${DONOR}/usr/bin/awk"
echo "\$ echo 'a=b' | busybox awk '{print gensub(/=.*/, \"\", 1)}'   (the cleanup's own call)"
echo 'a=b' | "${DONOR}/usr/bin/busybox" awk '{print gensub(/=.*/, "", 1)}'; echo "rc=$?"
echo "\$ busybox awk 'BEGIN{print gensub(/(b)/, \"<\\\\1>\", \"g\", \"abcb\")}'   (back-references, global)"
"${DONOR}/usr/bin/busybox" awk 'BEGIN{print gensub(/(b)/, "<\\1>", "g", "abcb")}'; echo "rc=$?"
echo
new_cell a
C=${CELL}/storage/.config/cloud_sync.conf
cat >> "${C}" <<'EOS'
LOG_LEVEL="DEBUG"
RCLONEOPTS="--progress \
--bwlimit 1M \
--filter-from /storage/.config/cloud_sync-rules.txt"
EOS
echo "the shipped conf with LOG_LEVEL and a three-line RCLONEOPTS repeated after it (A48's shape):"
echo "  before: $(grep -c '^LOG_LEVEL=' "${C}") LOG_LEVEL, $(grep -c '^RCLONEOPTS=' "${C}") RCLONEOPTS, bwlimit lines $(grep -c -- '--bwlimit' "${C}")"
echo "\$ (sandbox) command -v awk; cloud_sync_cleanup_duplicates.sh /storage/.config/cloud_sync.conf"
"${HL}/sbx.sh" bash -c 'readlink /usr/bin/awk; /usr/bin/cloud_sync_cleanup_duplicates.sh /storage/.config/cloud_sync.conf; echo "rc=$?"; bash -n /storage/.config/cloud_sync.conf; echo "bash -n rc=$?"' 2>&1
echo "  after: $(grep -c '^LOG_LEVEL=' "${C}") LOG_LEVEL ($(grep '^LOG_LEVEL=' "${C}")), $(grep -c '^RCLONEOPTS=' "${C}") RCLONEOPTS, bwlimit lines $(grep -c -- '--bwlimit' "${C}")"
echo "== end $(now)"

#!/bin/bash
# SPDX-License-Identifier: GPL-2.0
# Remove duplicate variable assignments from cloud_sync.conf, keeping only the first occurrence.
# Usage: ./cloud_sync_cleanup_duplicates.sh /path/to/cloud_sync.conf

CONF_FILE="${1:-/storage/.config/cloud_sync.conf}"
TMP_FILE="${CONF_FILE}.cleaned"

# A value continued with a trailing backslash (RCLONEOPTS is written that
# way) is one assignment over several lines: a repeated one is removed whole.
# Its first line alone used to go, and the lines that continued it stayed as
# bare lines -- a file that no longer parses, which every run after then
# refused or fell back from (found in the audit of the fixes to #307).
#
# Whether a line goes on is read as bash reads it (PL-23): inside an open
# quote, or after a backslash that ends the line outside a comment. A
# comment that ends in a backslash continues nothing, and the lines that
# continue a first occurrence belong to it -- they are not read again as
# assignments of their own.
awk '
  function goes_on(s,    i, c, n, bs) {
    n = length(s); bs = 0
    for (i = 1; i <= n; i++) {
      c = substr(s, i, 1)
      if (bs) { bs = 0; continue }
      if (sq) { if (c == "\047") sq = 0; continue }
      if (c == "\\") { bs = 1; continue }
      if (dq) { if (c == "\"") dq = 0; continue }
      if (c == "\"") { dq = 1; continue }
      if (c == "\047") { sq = 1; continue }
      if (c == "#" && (i == 1 || substr(s, i - 1, 1) ~ /[ \t]/)) return 0
    }
    return (dq || sq || bs)
  }
  inval { inval = goes_on($0); if (!drop) print; next }
  /^[[:space:]]*#/ { print; next }
  /^[[:space:]]*$/ { print; next }
  /^[A-Za-z0-9_]+=/ {
    var = $0; sub(/=.*/, "", var)
    dq = 0; sq = 0
    drop = (var in seen); seen[var] = 1
    inval = goes_on($0)
    if (!drop) print
    next
  }
  { print }
' "$CONF_FILE" > "$TMP_FILE" && mv "$TMP_FILE" "$CONF_FILE" \
  && echo "Duplicate variable assignments removed from $CONF_FILE." \
  || { rm -f "$TMP_FILE"; echo "Could not clean $CONF_FILE; left as it was." >&2; exit 1; }

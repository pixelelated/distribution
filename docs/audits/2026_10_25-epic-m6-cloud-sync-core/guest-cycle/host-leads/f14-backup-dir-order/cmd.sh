#!/bin/bash
# F-14's host proof (KILL2's three FAILs): with --backup-dir, when does the image's rclone move the
# file it will replace, and what is under the destination if the copy is killed before it lands?
# Then: does the shipped allowlist admit the .partial a SIGKILL leaves, so a backup before the next
# restore would send it? The donor rclone alone, on scratch directories; no script, no network.
. /workspace/tmp/m6-t16/hl/lib.sh
R=${DONOR}/usr/bin/rclone
header "F-14 --backup-dir order"
W=$(mktemp -d "${HL}/cells/f14.XXXXXX")
mkdir -p "${W}/cloud/savestates" "${W}/saves/savestates" "${W}/replaced"
for i in 1 2 3; do
    printf 'v1 local save %s\n' "${i}" > "${W}/saves/savestates/f${i}.state"
    head -c 1048576 /dev/urandom > "${W}/cloud/savestates/f${i}.state"
done
ls_tree() { echo "  saves:    $( (cd "${W}/saves" && find . -type f | sort | tr '\n' ' ') )"; echo "  replaced: $( (cd "${W}/replaced" && find . -type f | sort | tr '\n' ' ') )"; }
echo "before: three local saves (v1, 15 bytes each), three newer cloud copies (1 MiB each)"; ls_tree
echo "\$ rclone copy cloud/ saves/ --backup-dir replaced/run1 --bwlimit 200k --transfers 1 --checkers 8 --stats 1s -v &"
S=$(date +%s%N)
"${R}" copy "${W}/cloud/" "${W}/saves/" --backup-dir "${W}/replaced/run1" --bwlimit 200k --transfers 1 --checkers 8 --stats 1s -v > "${W}/rclone.log" 2>&1 &
P=$!
sleep 1.5
echo "+$(( ($(date +%s%N) - S) / 1000000 )) ms, mid-transfer:"; ls_tree
kill -KILL "${P}"; wait "${P}" 2>/dev/null; echo "SIGKILL to rclone (pid ${P}) at +$(( ($(date +%s%N) - S) / 1000000 )) ms"
echo "after the kill:"; ls_tree
echo "rclone's log, its order (masked):"; grep -E 'Moved|backup|Copied|Transferred:|Server Side|Renamed' "${W}/rclone.log" | grep -v -E '^\s*\*' | head -12 | mask | sed 's/^/  /'
echo
echo "\$ rclone lsf -R --files-only --filter-from <shipped cloud_sync-rules.txt> saves/   (what a backup's allowlist admits now)"
"${R}" lsf -R --files-only --filter-from "${ROOT}/usr/config/cloud_sync-rules.txt" "${W}/saves/"; echo "rc=$?"
echo "== end $(now)"

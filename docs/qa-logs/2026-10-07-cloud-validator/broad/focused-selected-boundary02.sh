#!/bin/bash
set -u
ROOT=/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders
RCLONE_REL=projects/ROCKNIX/packages/network/rclone/sources
OLD=${OLD:-0}; BASE_REF=${BASE_REF:-3268015c}
TMP=${FOCUSED_ROOT:?}
mkdir -p "$TMP"
FAIL=0; SKIPPED=0; NOT_APPLICABLE=0; BB=""; BB_HOST=""
check() { if [ "$1" -eq 0 ]; then echo "PASS $2"; else echo "FAIL $3"; FAIL=$((FAIL+1)); fi; }
src_of() { # <repo-relative path> <destination>
    if [ "${OLD}" -eq 1 ]; then
        git -C "${ROOT}" show "${BASE_REF}:${1}" > "${2}" || { echo "cannot read ${1} at ${BASE_REF}" >&2; exit 2; }
    else
        cp "${ROOT}/${1}" "${2}" || { echo "cannot read ${1}" >&2; exit 2; }
    fi
    case "${1}" in
        */cloud_setup)
            # Discovery shares the restore scanner's local membership.
            src_of "${RCLONE_REL}/cloud_content_restore" "$(dirname "$2")/cloud_content_restore"
            chmod +x "$(dirname "$2")/cloud_content_restore"
            if grep -q -- '--validate-folders)' "$2"; then
                src_of "${RCLONE_REL}/cloud_folder_validate" "$(dirname "$2")/cloud_folder_validate"
                chmod +x "$(dirname "$2")/cloud_folder_validate"
            fi ;;
        */cloud_content_backup|*/cloud_content_restore)
            local guard_rel="${RCLONE_REL}/cloud_content_transfer" guard_dst
            guard_dst="$(dirname "$2")/cloud_content_transfer"
            if [ "${OLD}" -eq 1 ]; then
                git -C "${ROOT}" show "${BASE_REF}:${guard_rel}" > "${guard_dst}" 2>/dev/null || rm -f "${guard_dst}"
            else
                cp "${ROOT}/${guard_rel}" "${guard_dst}" || exit 2
            fi ;;
        */cloud_scan|*/cloud_restore)
            local archive_rel="${RCLONE_REL}/rasteratops-settings-archive" archive_dst
            archive_dst="$(dirname "$2")/rasteratops-settings-archive"
            if [ "${OLD}" -eq 1 ]; then
                git -C "${ROOT}" show "${BASE_REF}:${archive_rel}" > "${archive_dst}" 2>/dev/null || rm -f "${archive_dst}"
            else
                cp "${ROOT}/${archive_rel}" "${archive_dst}" || exit 2
            fi ;;
    esac
}

echo "  l. a missing cloud folder reads as not there yet whatever the server's words (#142)"
# absent_not_broken, lifted from cloud_content_restore and run against a shim
# rclone whose cloud holds /QA/Saves and /QA/Content/ROMs and answers every
# other folder with an FTP-style plain error (exit 1, not rclone's 3). The
# walk must call an absent folder absent at any depth, a present one present,
# and a root that will not list broken. Then the copy in cloud_setup must be
# the same function, and the content backup must make its folder before it
# copies into it.
LL="${TMP}/l"; mkdir -p "${LL}/shim" "${LL}/src"
for rel in cloud_content_restore cloud_setup cloud_content_backup; do
    src_of "${RCLONE_REL}/${rel}" "${LL}/src/${rel}"
done
cat > "${LL}/shim/rclone" <<'EOR'
#!/bin/bash
# lsf lists a cloud of /QA/Saves, /QA/Content/ROMs and /QA/-Dash; every other
# folder is an FTP-style plain error (exit 1, not rclone's 3). lsd answers the
# same way, or "not found" (exit 3) under LSD_NOTFOUND. backend features says
# what FEATURES says -- bucket, path -- or fails outright (anything else).
[ -z "${LQ_CALLS:-}" ] || printf '%s\n' "$*" >> "${LQ_CALLS}"
p=""; for a in "$@"; do case "$a" in *:*) p="$a";; esac; done
rel="${p#*:}"; rel="${rel#/}"; rel="${rel%/}"
case "$1" in
  lsf)
    [ -n "${ROOT_DOWN:-}" ] && exit 1
    case "$rel" in
      "") printf 'QA/\n' ;;
      QA) printf 'Saves/\nContent/\n-Dash/\n' ;;
      QA/Content) printf 'ROMs/\n' ;;
      *) echo 'NOTICE: Failed to lsf: 501 "No such directory."' >&2; exit 1 ;;
    esac ;;
  lsd)
    case "$rel" in QA|QA/Saves|QA/Content|QA/Content/ROMs|QA/-Dash) exit 0 ;; esac
    if [ -n "${LSD_NOTFOUND:-}" ]; then echo 'ERROR : directory not found' >&2; exit 3; fi
    echo 'ERROR : Failed to lsd: 501 "No such directory."' >&2; exit 1 ;;
  backend)
    case "${FEATURES:-}" in
      bucket) printf '{\n\t"Features": {\n\t\t"BucketBased": true,\n\t\t"BucketBasedRootOK": true\n\t}\n}\n' ;;
      path)   printf '{\n\t"Features": {\n\t\t"BucketBased": false,\n\t\t"BucketBasedRootOK": false\n\t}\n}\n' ;;
      *) exit 1 ;;
    esac ;;
  *) exit 2 ;;
esac
EOR
chmod +x "${LL}/shim/rclone"
sed -n '/^absent_not_broken() {/,/^}/p' "${LL}/src/cloud_content_restore" > "${LL}/fn.sh"
grep -q 'rclone lsf --dirs-only' "${LL}/fn.sh"; check $? "absent_not_broken is lifted from cloud_content_restore" "no absent_not_broken() in cloud_content_restore"
LL_SCOPED=0
# This source generation confines missing-folder probes to the selected root.
grep -qE 'local .*boundary=.*\$\{ROOT' "${LL}/fn.sh" && LL_SCOPED=1
lq() { # <path> <expected rc> [selected root]; ROOT_DOWN passes through
    PATH="${LL}/shim:${PATH}" LQ_CALLS="${LL}/calls" timeout 5s bash -c         '. "$1"; ROOT="$3"; RCLONE_LIST_OPTS=(--retries 1); absent_not_broken "$2"'         _ "${LL}/fn.sh" "$1" "${3:-qa:/QA/Content/}" 2>/dev/null
    local actual=$?
    [ "${actual}" -ne 124 ] || echo "      metadata fixture timed out for $1" >&2
    [ "${actual}" -eq "$2" ]
}
lq qa:/QA/Content/BIOS/ 0; check $? "a folder its listable parent lacks is absent (QA/Content/BIOS)" "QA/Content/BIOS did not read as absent"
lq qa:/QA/Content/ROMs/ 1; check $? "a folder its parent lists is present, so the failure was something else (QA/Content/ROMs)" "QA/Content/ROMs read as absent"
if [ "${LL_SCOPED}" -eq 0 ]; then
    lq qa:/QA-Custom/Saves 0; check $? "historical walker reaches account root for an absent custom parent" "QA-Custom/Saves did not read as absent"
    lq qa:/Nope/A/B/ 0; check $? "historical walker reaches account root for an absent deep parent" "Nope/A/B did not read as absent"
else
    : > "${LL}/calls"
    lq qa:/QA-Custom/Saves 1 qa:/QA-Custom/ && ! grep -qE '^lsf --dirs-only qa:/ ' "${LL}/calls"
    check $? "unreadable selected parent stays unreadable without account-root discovery" "custom parent escaped its selected boundary or was guessed missing"
    : > "${LL}/calls"
    lq qa:/Nope/A/B/ 1 qa:/Nope/ && ! grep -qE '^lsf --dirs-only qa:/ ' "${LL}/calls"
    check $? "nested failed reads stop at their selected root" "nested probe escaped its root or was guessed missing"
    : > "${LL}/calls"
    lq qa:/QA/Content2/ROMs/ 1 qa:/QA/Content/ && [ ! -s "${LL}/calls" ]
    check $? "a sibling prefix outside the selected library causes no remote read" "out-of-scope sibling was probed"
    lq qa:/Nope/A/B/ 0 qa:/; check $? "explicit absolute account-root selection permits its own descendants" "explicit root did not establish missing descendant"
    : > "${LL}/calls"
    lq qa:ROMs/ 0 qa: && grep -q '^lsf --dirs-only qa: ' "${LL}/calls" && ! grep -q '^lsf --dirs-only qa:/ ' "${LL}/calls"
    check $? "explicit relative root stays qa: and completes without a parent loop" "relative root was rewritten or did not complete"
    : > "${LL}/calls"
    ROOT_DOWN=1 lq qa:ROMs/ 1 qa: && [ "$(wc -l < "${LL}/calls")" -eq 1 ]
    check $? "failed relative-root listing stops after its one selected-root probe" "relative-root error retried an ancestor or did not complete"
fi
lq qa:/QA/ 1 qa:/; check $? "a folder its selected root lists is present (QA)" "QA read as absent"
: > "${LL}/calls"
ROOT_DOWN=1 lq qa:/QA/Content/ROMs/ 1; check $? "a selected root that will not list is unreadable, not absent" "an unlistable selected root read as absent"
if [ "${LL_SCOPED}" -eq 1 ]; then
    [ "$(wc -l < "${LL}/calls")" -eq 1 ] && grep -qE '^lsf --dirs-only qa:/QA/Content/? ' "${LL}/calls"
    check $? "failed selected content-root read does not inspect its ancestors" "ancestor reads: $(cat "${LL}/calls")"
fi
lq qa:/ 1 qa:/; check $? "the root itself is never absent" "the root read as absent"
lq 'qa:/QA/-Dash/' 1 qa:/QA/; check $? "a hyphenated folder name is present rather than read as grep options" "QA/-Dash read as absent"
# cloud_setup's folder setter, lifted with the walk and its bound. The
# parent walk runs only on a remote rclone says is path-based; a bucket's
# refusal stands with the bucket message; and when `backend features`
# cannot be read at all the provider's answer is taken -- a folder is not
# stored on a guess (#151 PL-14: a failed call read as "not bucket-based").
sed -n '/^readonly -a RCLONE_LIST_OPTS/p; /^absent_not_broken() {/,/^}/p; /^syncpath_problem() {/,/^}/p' "${LL}/src/cloud_setup" > "${LL}/sp.sh"
grep -q '^syncpath_problem() {' "${LL}/sp.sh"; check $? "syncpath_problem is lifted from cloud_setup with the walk" "no syncpath_problem() in cloud_setup"
sp() { # <path> <expected rc>; FEATURES and LSD_NOTFOUND pass through; the reason to sp.out
    PATH="${LL}/shim:${PATH}" bash -c ". '${LL}/sp.sh'; syncpath_problem '$1' qa:" > "${LL}/sp.out" 2>/dev/null; [ $? -eq "$2" ]
}
FEATURES=path sp /QA/New 0; check $? "on a path-based remote a folder its parent lacks is accepted as not there yet (QA/New)" "QA/New was refused on a path-based remote: $(head -1 "${LL}/sp.out")"
FEATURES=bucket sp /Bad-Bucket/x 1 && grep -q 'buckets' "${LL}/sp.out"; check $? "on a bucket remote the provider's refusal stands, and the message names buckets (Bad-Bucket)" "bucket refusal: $(head -1 "${LL}/sp.out")"
FEATURES=fail sp /QA/New 1; check $? "when rclone cannot say which kind the remote is, the provider's refusal is taken rather than the walk's 'not there yet' (QA/New)" "QA/New was accepted with the remote's kind unknown -- a failed backend features read as path-based and the walk ran (#151 PL-14)"
FEATURES=fail LSD_NOTFOUND=1 sp /QA/New 0; check $? "and the provider's own 'not found' is accepted whatever the kind (QA/New)" "a not-found folder was refused: $(head -1 "${LL}/sp.out")"
if [ "${LL_SCOPED}" -eq 0 ]; then
    [ -s "${LL}/fn.sh" ] && diff -q <(sed -n '/^absent_not_broken() {/,/^}/p' "${LL}/src/cloud_setup") "${LL}/fn.sh" >/dev/null
    check $? "historical setup and content walkers are identical" "historical absent_not_broken functions differ or are missing"
fi
awk '/^    rclone mkdir "\$\{TARGET\}"/{m=NR} /^    (bounded_content_rclone|rclone) copy "\$\{SRC\}" "\$\{TARGET\}"/{c=NR} END{exit !(m && c && m < c)}' "${LL}/src/cloud_content_backup"; check $? "cloud_content_backup makes the folder before it copies into it" "no rclone mkdir of the target ahead of the copy in cloud_content_backup"
grep -q 'absent_not_broken "${ROOT}ROMs/"' "${LL}/src/cloud_content_restore" && grep -q 'absent_not_broken "${ROOT}BIOS/"' "${LL}/src/cloud_content_restore"; check $? "the scan checks both selected category paths before treating missing content as empty" "missing-category handling is absent for ROMs or BIOS"
# cloud_setup --check WHOLE, inside bwrap, against a shim rclone that answers
# listremotes with one remote, lsd with 0, and records every argv it was given:
# the probe must carry the listing bound (one run, three low-level retries).
# It carried only two timeouts until 2026-09-25, so rclone's defaults -- three
# runs of ten retries -- applied under a blocking spinner on three interface
# pages, the shape #113 bounded for the syncs (#273's trace of #113).
LC="${LL}/check"; mkdir -p "${LC}/shim" "${LC}/rec" "${LC}/repo"
cp "${LL}/src/cloud_setup" "${LC}/repo/cloud_setup"
printf 'export PATH=/shim:/usr/bin:/bin\n' > "${LC}/profile"
printf '#!/bin/sh\necho "logger $*" >&2\n' > "${LC}/shim/logger"
cat > "${LC}/shim/rclone" <<'EOR'
#!/bin/sh
printf '%s\n' "$*" >> /rec/argv
case "$1" in listremotes) echo "qa:" ;; esac
exit 0
EOR
chmod +x "${LC}/shim"/*
OUTC="${LC}/out"
RCC=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
    --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
    --ro-bind /etc /etc --ro-bind "${LC}/profile" /etc/profile \
    --ro-bind "${LC}/shim" /shim --bind "${LC}/rec" /rec --ro-bind "${LC}/repo" /repo \
    --dev /dev --proc /proc --tmpfs /tmp --tmpfs /storage \
    bash /repo/cloud_setup --check > "${OUTC}" 2>&1; echo $? ) 2>/dev/null )
[ "${RCC}" -eq 0 ] && grep -q '^OK qa:' "${OUTC}"; check $? "cloud_setup --check verifies the one remote the shim lists (rc ${RCC})" "rc ${RCC}; out: $(head -2 "${OUTC}" | tr '\n' ' ' | cut -c1-120)"
LSD=$(grep '^lsd ' "${LC}/rec/argv" 2>/dev/null | head -1)
echo "${LSD}" | grep -q -- '--retries 1' && echo "${LSD}" | grep -q -- '--low-level-retries 3'; check $? "its probe is bounded to one run and three low-level retries (RCLONE_LIST_OPTS), not rclone's three runs of ten" "lsd was called as: ${LSD:-(never)}"

printf "RESULT failures=%s\n" "$FAIL"
exit "$FAIL"

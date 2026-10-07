#!/bin/bash
# Extracted C1/C2+SC checks, synthetic only.
set -u

HARNESS_ROOT=/workspace/repos/rocknix.worktrees/conflict-resolution
ROOT="$(cd "${LAST_GOOD_SOURCE_ROOT:-${HARNESS_ROOT}}" && pwd)" || exit 2
[ -f "${ROOT}/projects/ROCKNIX/packages/network/rclone/package.mk" ] || { echo "last-good-scripts-test: source checkout has no rclone recipe" >&2; exit 2; }
BASE_REF="${BASE_REF:-1d1503180d}"
OLD=0
[ "${1:-}" = "--old" ] && OLD=1

CHK_REL=projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
BT_REL=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
FN_REL=projects/ROCKNIX/packages/rocknix/profile.d/001-functions
NBS_REL=projects/ROCKNIX/packages/sysutils/systemd/scripts/network-base-setup
WIFICTL_REL=projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl
RCLONE_REL=projects/ROCKNIX/packages/network/rclone/sources

command -v bwrap >/dev/null || { echo "needs bubblewrap (bwrap)" >&2; exit 2; }
command -v setsid >/dev/null || { echo "needs setsid" >&2; exit 2; }

TMP="$(mktemp -d)"; trap 'rm -rf "${TMP}"' EXIT
FAIL=0
SKIPPED=0
NOT_APPLICABLE=0
# skip <text>: a check that did not run is counted, never folded into PASSED
# (audit of the fix round PL-023): the verdict says how many, and exits 3
# when nothing failed but something was skipped -- vm-qa reads 3 as SKIP.
skip() { SKIPPED=$((SKIPPED + 1)); echo "    SKIP  $*"; }
# The signal dispositions this run inherited (PL-025): vm-qa's wrapper resets
# SIGINT and SIGPIPE before exec; SigIgn bit 1 is SIGINT, bit 12 SIGPIPE. Read
# from /proc/$$ -- the first cut read /proc/self inside $( ), which is awk's own
# process, and awk reads SIGPIPE ignored where this shell has it default.
sigign="$(awk '/^SigIgn:/{print $2}' "/proc/$$/status")"   # $$ is this script, not the awk
echo "signals: SigIgn=${sigign} SIGINT ignored=$(( (16#${sigign} >> 1) & 1 )) SIGPIPE ignored=$(( (16#${sigign} >> 12) & 1 ))"
check() { # <0|nonzero> ok-text bad-text
    if [ "$1" -eq 0 ]; then echo "    PASS  $2"; else echo "    FAIL  $3"; FAIL=$((FAIL + 1)); fi
}

# One file under test: the working tree's copy, or the base commit's under
# --old. A copy that cannot be read ends the run (exit 2) rather than
# leaving an empty file for a case to grade -- against an empty script every
# guard is absent, and the FAILs would read as the guards firing. Every case
# that lifts or runs a script takes it from here, so --old means the same
# thing in every case (#151 PL-10: cases l and m used to read the working
# tree whatever the flag said, and their checks had never been seen to fail).
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
            chmod +x "$(dirname "$2")/cloud_content_restore" ;;
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

# The scripts under test: the working tree, or the base commit's.
mkdir -p "${TMP}/src"
for rel in "${CHK_REL}" "${BT_REL}" "${FN_REL}"; do
    src_of "${rel}" "${TMP}/src/$(basename "${rel}")"
done
CHK="${TMP}/src/chksysconfig"; BT="${TMP}/src/backuptool"; FN="${TMP}/src/001-functions"
chmod +x "${BT}"

# busybox sed/mv/cp from the image when a build root is here, so the rename
# semantics tested are the device's.
image_tool_source() {
    local name="$1" b; shift
    if [ -n "${QA_SYSTEM_ROOT:-}" ]; then
        b="${QA_SYSTEM_ROOT}/usr/bin/${name}"
        if [ ! -x "${b}" ] || ! "${b}" "$@" >/dev/null 2>&1; then
            echo "cannot run candidate ${name} from QA_SYSTEM_ROOT: ${b}" >&2
            return 2
        fi
        printf '%s\n' "${b}"
        return 0
    fi
    for b in "${ROOT}"/../*/build.{ROCKNIX,RASTERATOPS,pixelelated}-*/image/system/usr/bin/"${name}" \
             "${ROOT}".worktrees/*/build.{ROCKNIX,RASTERATOPS,pixelelated}-*/image/system/usr/bin/"${name}" \
             "${ROOT}"/build.{ROCKNIX,RASTERATOPS,pixelelated}-*/image/system/usr/bin/"${name}"; do
        if [ -x "${b}" ] && "${b}" "$@" >/dev/null 2>&1; then
            printf '%s\n' "${b}"
            return 0
        fi
    done
    command -v "${name}" || true
}
BB_SRC=$(image_tool_source busybox sed --help) || exit 2
# The copy, not the build root's file. Every image step deletes image/system
# and re-installs every package (scripts/image), so a build running beside the
# harness pulls the busybox every sandbox here bind-mounts out from under it:
# on 2026-09-25 section t's eighteen checks after the cancel failed with rc 1
# and empty output while a GENERIC_X64 image step ran, and the log was read as
# a race in the scripts (#272) until the timestamps were put side by side. A
# bind of a file another process rewrites is a fixture the harness does not
# own; the copy is. BB_HOST is the copy on the host; BB is where every sandbox
# sees it -- a path of its own, since the sandboxes mount a tmpfs over /tmp
# and a copy under the run directory would vanish with it. The wrappers try
# the sandbox path first and fall back to the host copy, so the same wrapper
# serves the host-side checks (sections a and b) and the sandboxed ones.
BB=""; BB_HOST=""
if [ -n "${BB_SRC}" ]; then
    cp "${BB_SRC}" "${TMP}/busybox" || { echo "    FAIL  cannot copy ${BB_SRC} into the run (a build's image step?)"; exit 2; }
    BB_HOST="${TMP}/busybox"; BB="/lgst/busybox"
fi
mkdir -p "${TMP}/bbin"
if [ -n "${BB}" ]; then
    for a in sed mv cp tr head wc cut awk stat chmod cat; do printf '#!/bin/sh\n[ -x %s ] && exec %s %s "$@"\nexec %s %s "$@"\n' "${BB}" "${BB}" "${a}" "${BB_HOST}" "${a}" > "${TMP}/bbin/${a}"; chmod +x "${TMP}/bbin/${a}"; done
fi

echo "last-good-scripts-test: $([ "${OLD}" -eq 1 ] && echo "scripts at ${BASE_REF} (expect FAILs)" || echo "scripts in ${ROOT}")"
[ -n "${BB}" ] && echo "  sed/mv/cp/tr/head/wc/cut/awk: $("${BB_HOST}" 2>&1 | head -1) -- a copy of ${BB_SRC}"

echo "  C. the cloud sign-in broker and setup (audit #307 stream C)"
CS="${TMP}/C"; mkdir -p "${CS}/src"
for rel in cloud_setup cloud_oauth cloud_remote cloud_device_id; do
    src_of "${RCLONE_REL}/${rel}" "${CS}/src/${rel}"
done
# #508 retires migration; historical sources retain their actual engine tests.
# An accidentally missing installed script remains a setup failure.
MIGRATION_AVAILABLE=0
if { [ "${OLD}" -eq 1 ] && git -C "${ROOT}" cat-file -e "${BASE_REF}:${RCLONE_REL}/cloud_migrate_layout" 2>/dev/null; } \
    || { [ "${OLD}" -eq 0 ] && [ -e "${ROOT}/${RCLONE_REL}/cloud_migrate_layout" ]; }; then
    src_of "${RCLONE_REL}/cloud_migrate_layout" "${CS}/src/cloud_migrate_layout"
    MIGRATION_AVAILABLE=1
else
    src_of projects/ROCKNIX/packages/network/rclone/package.mk "${CS}/src/rclone-package.mk"
    if grep -qE '^[[:space:]]*cp[[:space:]]+cloud_migrate_layout([[:space:]]|$)' "${CS}/src/rclone-package.mk"; then
        echo "cannot test selected source: recipe installs missing cloud_migrate_layout" >&2
        exit 2
    fi
    NOT_APPLICABLE=$((NOT_APPLICABLE + 1))
    echo "    NOT APPLICABLE  historical migration cases: selected source has no engine and its recipe does not install one (#508); no migration checks counted as PASS"
fi
# busybox for the applets the device has, where this machine has the image's.
CSBB=(); CSPATH="/shim:/usr/bin:/bin"
if [ -n "${BB}" ]; then CSBB=(--ro-bind "${TMP}/bbin" /bbin --ro-bind "${BB_HOST}" "${BB}"); CSPATH="/shim:/bbin:/usr/bin:/bin"; fi

# C1. cloud_setup WHOLE inside bwrap: a stub profile, the shipped
# cloud_sync.conf as the device's, and a shim rclone whose remote "qa:" is
# path-based and holds no folder yet (lsd answers "directory not found").
C1="${CS}/c1"; mkdir -p "${C1}/shim" "${C1}/repo" "${C1}/storage/.config"
cp "${CS}/src/cloud_setup" "${C1}/repo/cloud_setup"
cp "${CS}/src/cloud_content_restore" "${C1}/repo/cloud_content_restore"
chmod +x "${C1}/repo/cloud_content_restore"
# Historical setup depended on the engine; current setup is independent.
if [ "${MIGRATION_AVAILABLE}" -eq 1 ]; then
    cp "${CS}/src/cloud_migrate_layout" "${C1}/repo/cloud_migrate_layout" && chmod +x "${C1}/repo/cloud_migrate_layout" || { echo "cannot place cloud_migrate_layout beside cloud_setup" >&2; exit 2; }
fi
printf 'export PATH=%s\n' "${CSPATH}" > "${C1}/profile"
printf '#!/bin/sh\nexit 0\n' > "${C1}/shim/logger"
cat > "${C1}/shim/rclone" <<'EOR'
#!/bin/sh
case "$1" in
  listremotes) echo "qa:" ;;
  lsd) echo 'ERROR : directory not found' >&2; exit 3 ;;
  backend) printf '{\n\t"Features": {\n\t\t"BucketBased": false\n\t}\n}\n' ;;
  *) exit 0 ;;
esac
EOR
chmod +x "${C1}/shim"/*
CONF1="${C1}/storage/.config/cloud_sync.conf"
c1() { # <args...>: cloud_setup in the sandbox; output to C1/out, rc in RC
    RC=$( ( bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${C1}/profile" /etc/profile "${CSBB[@]}" \
        --ro-bind "${C1}/shim" /shim --ro-bind "${C1}/repo" /repo --${C1RO:+ro-}bind "${C1}/storage" /storage \
        --dev /dev --proc /proc --tmpfs /tmp --tmpfs /var --dir /var/log \
        bash /repo/cloud_setup "$@" > "${C1}/out" 2>&1; echo $? ) 2>/dev/null )
}
conf1() { grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${CONF1}" | tr '\n' ' '; }
src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"; cp "${CONF1}" "${C1}/conf.before"
c1 --set-saves-remote /GAMES
[ "${RC}" -ne 0 ] && cmp -s "${CONF1}" "${C1}/conf.before"; check $? "a one-level saves folder (/GAMES) is refused and the config is left as it was (rc ${RC})" "rc ${RC}; the config now reads: $(conf1)-- the settings and content folders nested inside the saves folder a mirror deletes in (PL-015)"
grep -q '/GAMES/Saves' "${C1}/out" && ! grep -qi 'error' "${C1}/out"; check $? "and says why, in words, with the folder to use instead (/GAMES/Saves): $(head -1 "${C1}/out")" "said: '$(tr '\n' ' ' < "${C1}/out" | cut -c1-160)'"
c1 --check-syncpath /GAMES
[ "${RC}" -ne 0 ] && grep -q '/GAMES/Saves' "${C1}/out"; check $? "--check-syncpath refuses it too, where the folder is typed" "--check-syncpath /GAMES: rc ${RC}; said '$(tr '\n' ' ' < "${C1}/out" | cut -c1-120)'"
c1 --set-saves-remote Mine/Saves/
[ "${RC}" -eq 0 ] && [ "$(conf1)" = 'SAVES_REMOTE="/Mine/Saves" SETTINGS_REMOTE="/Mine/Backups" CONTENT_REMOTE="/Mine/Content" ' ]; check $? "a two-level folder (Mine/Saves/) is stored with its settings and content folders beside it" "rc ${RC}; config: $(conf1); said: $(head -1 "${C1}/out")"
c1 --set-saves-remote /a/b/Saves
[ "${RC}" -eq 0 ] && [ "$(conf1)" = 'SAVES_REMOTE="/a/b/Saves" SETTINGS_REMOTE="/a/b/Backups" CONTENT_REMOTE="/a/b/Content" ' ]; check $? "and a deeper one (/a/b/Saves) likewise" "rc ${RC}; config: $(conf1)"
# G-C-01 (the audit of stream C): the three destinations must be three
# folders. A saves folder named like its own sibling -- /Mine/Backups,
# /Mine/Content -- derives that sibling onto itself, so two tiers alias one
# folder. Refused where it is typed, case-folded (Dropbox and OneDrive fold
# case), with the folder to use instead; /Mine/Saves still derives its two.
src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"; cp "${CONF1}" "${C1}/conf.before"
for alias in /Mine/Backups /Mine/Content /Mine/backups; do
    cp "${C1}/conf.before" "${CONF1}"
    c1 --set-saves-remote "${alias}"
    [ "${RC}" -ne 0 ] && cmp -s "${CONF1}" "${C1}/conf.before" && grep -qx 'Try /Mine/Saves.' "${C1}/out"; check $? "a saves folder that would share a folder with its own siblings (${alias}) is refused, config untouched: $(head -1 "${C1}/out")" "${alias}: rc ${RC}; config: $(conf1); said: $(tr '\n' ' ' < "${C1}/out" | cut -c1-140) -- two tiers alias one folder (G-C-01)"
done
c1 --check-syncpath /Mine/Content
[ "${RC}" -ne 0 ] && grep -qx 'Try /Mine/Saves.' "${C1}/out"; check $? "--check-syncpath refuses /Mine/Content too" "--check-syncpath /Mine/Content: rc ${RC}; said '$(tr '\n' ' ' < "${C1}/out" | cut -c1-120)' (G-C-01)"
c1 --set-saves-remote /Mine/Saves
[ "${RC}" -eq 0 ] && [ "$(conf1)" = 'SAVES_REMOTE="/Mine/Saves" SETTINGS_REMOTE="/Mine/Backups" CONTENT_REMOTE="/Mine/Content" ' ]; check $? "while /Mine/Saves still derives /Mine/Backups and /Mine/Content beside it" "rc ${RC}; config: $(conf1)"

# --set-content-remote (the chooser, fork #352): the content root alone
# moves, the other two stay; a top-level folder is fine here; the root,
# traversal components, unsafe syntax and controls are refused unchanged.
src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"
c1 --set-saves-remote /Mine/Saves
c1 --set-content-remote Games/
[ "${RC}" -eq 0 ] && [ "$(conf1)" = 'SAVES_REMOTE="/Mine/Saves" SETTINGS_REMOTE="/Mine/Backups" CONTENT_REMOTE="/Games" ' ] && grep -qx 'OK /Games' "${C1}/out"; check $? "--set-content-remote Games/ stores /Games as the content root and leaves the saves and settings folders alone (rc ${RC})" "rc ${RC}; config: $(conf1); said '$(tr '\n' ' ' < "${C1}/out" | cut -c1-120)'"
cp "${CONF1}" "${C1}/conf.before"
for bad in / '/a/../b' '/a/./b' '/a//b' '/quote"' '/$HOME' '/`id`' $'/two\nlines' $'/trailing\n' $'/tab\tname'; do
    c1 --set-content-remote "${bad}"
    [ "${RC}" -ne 0 ] && cmp -s "${CONF1}" "${C1}/conf.before"; check $? "--set-content-remote refuses '${bad}' and leaves the config as it was (rc ${RC})" "rc ${RC}; said '$(tr '\n' ' ' < "${C1}/out" | cut -c1-120)'"
done
for good in '/MyGames' '/My Games' '/Games..old' "/Kid's Games"; do
    c1 --set-content-remote "${good}"
    [ "${RC}" -eq 0 ] && grep -qxF "CONTENT_REMOTE=\"${good}\"" "${CONF1}"; check $? "the content chooser accepts literal folder ${good}" "rc ${RC}; $(cat "${C1}/out")"
done

# PL-051: the config is written as text. & and | used to reach sed's
# replacement: & pasted the matched line into the value, | ended the
# expression and the write failed while OK was printed.
src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"
c1 --set-saves-remote '/R&D/Saves'
[ "${RC}" -eq 0 ] && [ "$(conf1)" = 'SAVES_REMOTE="/R&D/Saves" SETTINGS_REMOTE="/R&D/Backups" CONTENT_REMOTE="/R&D/Content" ' ]; check $? "a folder with & (/R&D/Saves) round-trips into the config" "rc ${RC}; config: $(conf1)-- & in a sed replacement is the matched text (PL-051)"
diff <(grep -vE '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${ROOT}/${RCLONE_REL}/cloud_sync.conf") <(grep -vE '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${CONF1}") >/dev/null; check $? "and every other line of the config, the multi-line RCLONEOPTS included, is byte for byte as it was" "the write changed other lines: $(diff <(grep -vE '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${ROOT}/${RCLONE_REL}/cloud_sync.conf") <(grep -vE '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${CONF1}") | head -3 | tr '\n' ' ')"
c1 --info
grep -qx 'SAVES_REMOTE=/R&D/Saves' "${C1}/out"; check $? "and --info reads it back as typed" "--info said: $(grep '^SAVES_REMOTE=' "${C1}/out")"
c1 --set-saves-remote '/a|b/Saves'
[ "${RC}" -eq 0 ] && [ "$(conf1)" = 'SAVES_REMOTE="/a|b/Saves" SETTINGS_REMOTE="/a|b/Backups" CONTENT_REMOTE="/a|b/Content" ' ]; check $? "a folder with | (/a|b/Saves) round-trips too" "rc ${RC}; config: $(conf1); said: $(head -1 "${C1}/out")"
cp "${CONF1}" "${C1}/conf.before"; rm -f "${C1}/storage/ran"
c1 --set-saves-remote '/x$(touch /storage/ran)/Saves'
[ "${RC}" -ne 0 ] && cmp -s "${CONF1}" "${C1}/conf.before" && grep -q "can't contain" "${C1}/out"; check $? "a name that would run as a command when the config is sourced is refused, config untouched: $(head -1 "${C1}/out")" "rc ${RC}; config: $(conf1); said: $(head -1 "${C1}/out")"
c1 --info
[ ! -e "${C1}/storage/ran" ]; check $? "and nothing ran" "a command in the folder name ran when --info sourced the config"
# A config an earlier build wrote with such a value: --info runs nothing in
# it, and names no folder for it -- the sync refuses that config
# (D-CLOUD-142), so it is not a folder anything uses; it used to be read out
# as text (the audit of the fix round, gpt G2-C-01, CF2 below).
sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE="/y$(touch /storage/ran)/Saves"|' "${CONF1}"
c1 --info
[ ! -e "${C1}/storage/ran" ] && grep -qx 'SAVES_REMOTE=' "${C1}/out"; check $? "--info runs nothing in an already-written value and names no folder for it" "ran: $([ -e "${C1}/storage/ran" ] && echo yes || echo no); --info said: $(grep '^SAVES_REMOTE=' "${C1}/out")"
c1 --seed-folders
[ ! -e "${C1}/storage/ran" ]; check $? "and so does --seed-folders, which used to eval the config's lines" "--seed-folders ran the command in an already-written SAVES_REMOTE (eval of the config)"
# G-C-05 (claude): and every other reader of the config. A guard: no
# cloud_setup subcommand sources or evals it (grep: only /etc/profile is
# sourced), so these pass on the tree the audit read as well.
sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE="/z$(touch /storage/ran)/Content"|' "${CONF1}"
for sub in --content-location --check-syncpath --use-content-root; do
    rm -f "${C1}/storage/ran"; c1 "${sub}"
    [ ! -e "${C1}/storage/ran" ]; check $? "and ${sub} runs nothing an already-written value holds" "${sub} ran a command held in the config (G-C-05)"
done
rm -f "${C1}/storage/ran"
src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"; cp "${CONF1}" "${C1}/conf.before"
C1RO=1 c1 --set-saves-remote /Other/Saves
[ "${RC}" -ne 0 ] && ! grep -q '^OK' "${C1}/out" && cmp -s "${CONF1}" "${C1}/conf.before"; check $? "a config that cannot be written is a failure, not OK (rc ${RC})" "read-only /storage: rc ${RC}; said '$(tr '\n' ' ' < "${C1}/out" | cut -c1-120)' -- the write failed and OK was printed (PL-051)"
C1RO=1 c1 --use-content-root
[ "${RC}" -ne 0 ] && ! grep -q '^OK' "${C1}/out"; check $? "and --use-content-root likewise (rc ${RC})" "read-only /storage: rc ${RC}; said '$(tr '\n' ' ' < "${C1}/out" | cut -c1-120)'"
# G-C-07 (gpt): and says so in its own words only. The redirection that
# failed came before the one that silenced stderr, so the shell printed its
# own diagnostic -- a line number, the temp file's path, "Read-only file
# system" -- ahead of the sentence.
C1RO=1 c1 --set-saves-remote /Other/Saves
[ "$(cat "${C1}/out")" = "Your cloud sync settings couldn't be saved." ]; check $? "a write that fails prints its one sentence and no shell diagnostic" "read-only /storage printed: '$(tr '\n' '|' < "${C1}/out" | cut -c1-200)' (G-C-07)"
# G-C-03 (gpt) and G-C-06 (claude): cloud_setup reads the config as the
# scripts that run with it read it, minus the running: a value may be
# double-quoted, single-quoted or bare with a trailing comment. The first
# reader took only "...". Of a key assigned twice, the FIRST assignment
# wins: that is what the duplicate cleanup keeps under every --yes run and
# what the content scripts read; this check said the last until the audit
# of the fix round reversed it (PL-021, CF2 below).
src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"
printf 'SAVES_REMOTE="/Mine/Saves"\n' >> "${CONF1}"
c1 --info
grep -qx 'SAVES_REMOTE=/pixelelated/Saves' "${C1}/out"; check $? "a key assigned twice reads as its first assignment, the one the scripts run with after the duplicate cleanup (PL-021)" "SAVES_REMOTE assigned twice, --info said: $(grep '^SAVES_REMOTE=' "${C1}/out") (PL-021)"
sed -i "s|^SAVES_REMOTE=.*|SAVES_REMOTE='/Q/Saves'|" "${CONF1}"
c1 --info
grep -qx 'SAVES_REMOTE=/Q/Saves' "${C1}/out"; check $? "a single-quoted value reads without its quotes" "SAVES_REMOTE='/Q/Saves', --info said: $(grep '^SAVES_REMOTE=' "${C1}/out") (G-C-03)"
sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=/B/Saves  # mine|' "${CONF1}"
c1 --info
grep -qx 'SAVES_REMOTE=/B/Saves' "${C1}/out"; check $? "a bare value with a trailing comment reads as the word" "SAVES_REMOTE=/B/Saves  # mine, --info said: $(grep '^SAVES_REMOTE=' "${C1}/out") (G-C-03)"
sed -i "s|^CONTENT_REMOTE=.*|CONTENT_REMOTE='/Mine/Content'|" "${CONF1}"
c1 --content-location
grep -qx 'CONTENT_REMOTE=/Mine/Content' "${C1}/out"; check $? "--content-location reads the config the same way" "CONTENT_REMOTE='/Mine/Content', --content-location said: $(grep '^CONTENT_REMOTE=' "${C1}/out") (G-C-03)"
src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"
# G-C-03 (claude): one name for one folder. The interface's row and its
# refusal dialog call it the CLOUD FOLDER; the refusals said "saves folder"
# in two of their four sentences.
for p1 in /GAMES /Mine/Backups; do
    c1 --check-syncpath "${p1}"
    [ "${RC}" -ne 0 ] && grep -q '^Your cloud folder' "${C1}/out" && ! grep -qi 'saves folder' "${C1}/out"; check $? "the refusal of ${p1} calls it the cloud folder, as the interface's row does" "${p1} refused as: $(head -1 "${C1}/out") (G-C-03 claude)"
done
# G-C-04 (gpt, the audit of stream C): a config path that is a directory is
# not a config. conf_set read it as absent and `mv -f` put the new file
# INSIDE it, then said OK; the artifact is what says whether it worked.
rm -f "${CONF1}"; mkdir "${CONF1}"
c1 --set-saves-remote /Other/Saves
[ "${RC}" -ne 0 ] && ! grep -q '^OK' "${C1}/out" && [ -d "${CONF1}" ] && [ -z "$(ls -A "${CONF1}")" ]; check $? "a config path that is a directory is a failure, not OK, and nothing is left inside it (rc ${RC})" "config path a directory: rc ${RC}; said '$(tr '\n' ' ' < "${C1}/out" | cut -c1-100)'; inside it: $(ls -A "${CONF1}" | tr '\n' ' ') (G-C-04)"
rm -rf "${CONF1}"; src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF1}"
c1 --use-content-root
[ "${RC}" -eq 0 ] && grep -qx 'CONTENT_REMOTE=""' "${CONF1}" && [ "$(grep -c '^CONTENT_REMOTE=' "${CONF1}")" -eq 1 ]; check $? "--use-content-root writes CONTENT_REMOTE=\"\" once" "rc ${RC}; $(grep '^CONTENT_REMOTE=' "${CONF1}" | tr '\n' ' ')"

# C2. --seed-folders against a cloud kept in a directory. The shim answers as
# rclone does: on a path-based remote (MODE=path) a folder or file that is not
# there is "directory not found", exit 3; on a bucket (MODE=bucket) a missing
# key or prefix lists as nothing, exit 0, and mkdir makes a folder only with
# --s3-directory-markers. FAIL_LSF=1 fails every listing (exit 1, a network
# error). Every argv is recorded.
C2="${CS}/c2"; mkdir -p "${C2}/shim" "${C2}/storage/.config" "${C2}/cloud" "${C2}/rec" "${C2}/run"
printf '#!/bin/sh\nexit 0\n' > "${C2}/shim/logger"
cat > "${C2}/shim/rclone" <<'EOR'
#!/bin/bash
printf '%s\n' "$*" >> /rec/argv
mode=$(cat /run/mode 2>/dev/null); fail=$(cat /run/fail-lsf 2>/dev/null)
p=""; files=0; dirs=0; markers=0; ignore=0; src=""; rec=0
for a in "$@"; do
    case "$a" in
        qa:*) p="$a" ;;
        -R) rec=1 ;;
        --files-only) files=1 ;; --dirs-only) dirs=1 ;;
        --s3-directory-markers) markers=1 ;; --ignore-existing) ignore=1 ;;
        /*) src="$a" ;;
    esac
done
rel="${p#qa:}"; rel="${rel#/}"; rel="${rel%/}"; target="/cloud/${rel}"
case "$1" in
  listremotes) echo "qa:" ;;
  cat) [ -f "${target}" ] || exit 3; cat "${target}" ;;
  rcat) mkdir -p "$(dirname "${target}")" && cat > "${target}" ;;
  mkdir)
    if [ "${mode}" = bucket ] && [ "${markers}" -eq 0 ]; then exit 0; fi
    mkdir -p "${target}" ;;
  lsd) exit 0 ;;
  backend) [ "${2:-}" = features ] || exit 1; printf '{"Features":{"CaseInsensitive":false},"Hashes":["MD5"]}\n' ;;
  lsf)
    [ -n "${fail}" ] && { echo 'ERROR : Failed to lsf: connection reset' >&2; exit 1; }
    if [ -f "${target}" ]; then basename "${target}"; exit 0; fi
    if [ -d "${target}" ] && [ "${rec}" -eq 1 ] && [ "${files}" -eq 1 ]; then
        (cd "${target}" && find . -type f | sed 's|^\./||'); exit 0
    fi
    if [ -d "${target}" ]; then
        shopt -s dotglob nullglob
        for e in "${target}"/*; do
            [ -e "$e" ] || continue
            if [ -d "$e" ]; then [ "${files}" -eq 1 ] || echo "$(basename "$e")/"
            else [ "${dirs}" -eq 1 ] || basename "$e"; fi
        done
        exit 0
    fi
    [ "${mode}" = bucket ] && exit 0
    echo 'ERROR : directory not found' >&2; exit 3 ;;
  copyto)
    [ "${ignore}" -eq 1 ] && [ -e "${target}" ] && exit 0
    mkdir -p "$(dirname "${target}")" && cp "${src}" "${target}" ;;
  *) echo "unsupported synthetic rclone command" >&2; exit 1 ;;
esac
EOR
chmod +x "${C2}/shim"/*
printf 'export PATH=%s\n' "${CSPATH}" > "${C2}/profile"
CONF2="${C2}/storage/.config/cloud_sync.conf"
c2() { # <args...>: cloud_setup against the cloud in C2/cloud; output to C2/out, rc in RC
    RC=$( ( bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${C2}/profile" /etc/profile "${CSBB[@]}" \
        --ro-bind "${C2}/shim" /shim --ro-bind "${C1}/repo" /repo --bind "${C2}/storage" /storage \
        --bind "${C2}/cloud" /cloud --bind "${C2}/rec" /rec --ro-bind "${C2}/run" /run \
        --dev /dev --proc /proc --tmpfs /tmp --tmpfs /var --dir /var/log \
        bash /repo/cloud_setup "$@" > "${C2}/out" 2>&1; echo $? ) 2>/dev/null )
}
c2reset() { # <path|bucket> [fail]: an empty cloud, the shipped config
    rm -rf "${C2}/cloud"/* "${C2}/rec/argv"; echo "$1" > "${C2}/run/mode"
    if [ -n "${2:-}" ]; then echo 1 > "${C2}/run/fail-lsf"; else rm -f "${C2}/run/fail-lsf"; fi
    src_of "${RCLONE_REL}/cloud_sync.conf" "${CONF2}"
}
readmes() { (cd "${C2}/cloud" && find . -name README.txt | sort | tr '\n' ' '); }
c2reset path
c2 --seed-folders
[ "${RC}" -eq 0 ] && [ "$(readmes)" = "./pixelelated/Backups/README.txt ./pixelelated/Content/BIOS/README.txt ./pixelelated/Content/README.txt ./pixelelated/Content/ROMs/README.txt ./pixelelated/Saves/README.txt " ] && [ "$(grep -c '^OK ' "${C2}/out")" -eq 4 ]; check $? "a fresh path-based cloud is seeded: five READMEs, four folders reported OK" "rc ${RC}; READMEs: $(readmes); said: $(tr '\n' ' ' < "${C2}/out")"
echo "mine" > "${C2}/cloud/pixelelated/Saves/README.txt"
c2 --seed-folders
[ "${RC}" -eq 0 ] && [ "$(cat "${C2}/cloud/pixelelated/Saves/README.txt")" = "mine" ]; check $? "an owner's README is left alone when the folder lists" "the owner's README now reads: $(head -1 "${C2}/cloud/pixelelated/Saves/README.txt")"
# PL-047: the listing fails, the upload would work.
echo 1 > "${C2}/run/fail-lsf"
c2 --seed-folders
[ "${RC}" -ne 0 ] && [ "$(cat "${C2}/cloud/pixelelated/Saves/README.txt")" = "mine" ]; check $? "a listing that fails does not overwrite the owner's README" "the owner's README now reads: $(head -1 "${C2}/cloud/pixelelated/Saves/README.txt") -- a failed probe was taken as 'absent' and the note was replaced (PL-047)"
c2reset path fail
c2 --seed-folders
[ -z "$(readmes)" ]; check $? "and on a fresh cloud whose listings fail, nothing is written" "READMEs written with every listing failing: $(readmes)(PL-047)"
[ "${RC}" -ne 0 ] && grep -q '^>>> why ' "${C2}/out" && ! grep -q '^OK ' "${C2}/out" \
    && ! grep -qE '^(mkdir|copyto|rcat) ' "${C2}/rec/argv"; check $? "failed folder reads report failure before any cloud write" "rc ${RC}; said: $(tr '\n' ' ' < "${C2}/out"); writes: $(grep -E '^(mkdir|copyto|rcat) ' "${C2}/rec/argv" | head -2 | tr '\n' '|')"
# claude F-RS-09: on a bucket the old probe (lsf of the README by name)
# exits 0 with nothing for a key that is not there.
c2reset bucket
c2 --seed-folders
[ "${RC}" -eq 0 ] && [ "$(readmes)" = "./pixelelated/Backups/README.txt ./pixelelated/Content/BIOS/README.txt ./pixelelated/Content/README.txt ./pixelelated/Content/ROMs/README.txt ./pixelelated/Saves/README.txt " ]; check $? "a fresh bucket cloud gets its five READMEs too" "bucket READMEs: '$(readmes)' -- a missing key lists as nothing with exit 0, which the probe took as 'there' (#308 claude F-RS-09)"
echo "mine" > "${C2}/cloud/pixelelated/Saves/README.txt"
c2 --seed-folders
[ "${RC}" -eq 0 ] && [ "$(cat "${C2}/cloud/pixelelated/Saves/README.txt")" = "mine" ]; check $? "and an owner's README in a bucket is left alone" "bucket: the owner's README now reads: $(head -1 "${C2}/cloud/pixelelated/Saves/README.txt")"

if [ "${MIGRATION_AVAILABLE}" -eq 1 ]; then
# The mixed-installation test's fresh device (D-CLOUD-158): seeding a cloud whose saves are in the
# fork's earlier /ROCKNIX joins that folder -- the conf points there, nothing is made at /pixelelated,
# and no layout marker is written under /ROCKNIX. The control first: a fresh cloud is seeded at
# /pixelelated with its marker, so the absence below is the join's doing and not a shim that never
# writes one.
c2reset path; c2 --seed-folders
grep -q '^rcat qa:/pixelelated/.layout' "${C2}/rec/argv"; check $? "seeding a fresh cloud writes the layout marker at /pixelelated (the control)" "argv: $(grep -E '^rcat' "${C2}/rec/argv" | head -2 | tr '\n' ' ')"
c2reset path
mkdir -p "${C2}/cloud/ROCKNIX/Saves/snes" "${C2}/cloud/ROCKNIX/Backups"; echo save > "${C2}/cloud/ROCKNIX/Saves/snes/a.srm"
c2 --seed-folders
[ "${RC}" -eq 0 ] && grep -q '^SAVES_REMOTE="/ROCKNIX/Saves"' "${CONF2}" && grep -q '^SETTINGS_REMOTE="/ROCKNIX/Backups"' "${CONF2}" && grep -q '^CONTENT_REMOTE="/ROCKNIX/Content"' "${CONF2}" \
    && [ ! -e "${C2}/cloud/pixelelated" ] && ! grep -q '^rcat ' "${C2}/rec/argv" && grep -qx 'OK /ROCKNIX/Saves' "${C2}/out"; check $? "seeding a cloud whose saves are in /ROCKNIX joins that folder: the conf points there, nothing at /pixelelated, no marker written (D-CLOUD-158's fresh device)" "rc ${RC}; conf: $(grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${CONF2}" | tr '\n' ' '); cloud: $(cd "${C2}/cloud" && find . -maxdepth 2 | sort | tr '\n' ' ' | cut -c1-200); said: $(tr '\n' ' ' < "${C2}/out" | cut -c1-160)"

# A carried /GAMES at the seeding (D-CLOUD-161, D-CLOUD-169): seeding it put a README in /GAMES that every
# later check read as saves. With the player's saves in /ROCKNIX it joins them; with nothing anywhere it is
# no folder at all, and the seeding makes the current folders, as for any new cloud. Neither makes /GAMES.
# An old config with no content choice omits the key; an explicit empty value
# means the cloud root and has its own preservation test below (#380).
c2games() { sed -i -e 's|^SAVES_REMOTE=.*|SAVES_REMOTE="/GAMES"|' -e 's|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE="/GAMES/backup"|' -e '/^CONTENT_REMOTE=/d' "${CONF2}"; }
c2reset path; c2games
mkdir -p "${C2}/cloud/ROCKNIX/Saves/snes"; echo save > "${C2}/cloud/ROCKNIX/Saves/snes/a.srm"
c2 --seed-folders
[ "${RC}" -eq 0 ] && grep -q '^SAVES_REMOTE="/ROCKNIX/Saves"' "${CONF2}" && grep -q '^CONTENT_REMOTE="/ROCKNIX/Content"' "${CONF2}" && [ ! -e "${C2}/cloud/GAMES" ] && [ ! -e "${C2}/cloud/pixelelated" ]; check $? "seeding a carried /GAMES whose cloud holds /ROCKNIX/Saves joins /ROCKNIX and makes no /GAMES (the Nova's shape)" "rc ${RC}; conf: $(grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${CONF2}" | tr '\n' ' '); cloud: $(cd "${C2}/cloud" && find . -maxdepth 2 | sort | tr '\n' ' ' | cut -c1-200)"
c2reset path; c2games
c2 --seed-folders
[ "${RC}" -eq 0 ] && grep -q '^SAVES_REMOTE="/pixelelated/Saves"' "${CONF2}" && grep -q '^SETTINGS_REMOTE="/pixelelated/Backups"' "${CONF2}" && grep -q '^CONTENT_REMOTE="/pixelelated/Content"' "${CONF2}" \
    && [ ! -e "${C2}/cloud/GAMES" ] && [ -f "${C2}/cloud/pixelelated/Saves/README.txt" ] && grep -q '^rcat qa:/pixelelated/.layout' "${C2}/rec/argv"; check $? "seeding a carried /GAMES on an empty cloud makes the current folders, with the marker, and no /GAMES (D-CLOUD-161)" "rc ${RC}; conf: $(grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' "${CONF2}" | tr '\n' ' '); cloud: $(cd "${C2}/cloud" && find . -maxdepth 2 | sort | tr '\n' ' ' | cut -c1-200)"

else
# Current setup preserves explicitly selected paths, even beside an older tree.
c2reset path
mkdir -p "${C2}/cloud/ROCKNIX/Saves/snes"; echo save > "${C2}/cloud/ROCKNIX/Saves/snes/a.srm"
cp "${CONF2}" "${C2}/before.conf"
c2 --seed-folders
[ "${RC}" -eq 0 ] && cmp -s "${CONF2}" "${C2}/before.conf" \
    && [ "$(cat "${C2}/cloud/ROCKNIX/Saves/snes/a.srm")" = save ] \
    && [ -f "${C2}/cloud/pixelelated/Saves/README.txt" ] \
    && grep -qx 'layout=2' "${C2}/cloud/pixelelated/.layout"
check $? "#508: fresh defaults seed /pixelelated beside legacy files without adopting or changing them" "rc ${RC}; configuration or original save changed, or fresh layout was not seeded"
for chosen in /ROCKNIX /GAMES /Chosen; do
    c2reset path
    printf 'SAVES_REMOTE="%s/Saves"\nSETTINGS_REMOTE="%s/Backups"\nCONTENT_REMOTE="%s/Content"\n' "${chosen}" "${chosen}" "${chosen}" > "${CONF2}"
    cp "${CONF2}" "${C2}/before.conf"
    c2 --seed-folders
    [ "${RC}" -eq 0 ] && cmp -s "${CONF2}" "${C2}/before.conf" \
        && [ -f "${C2}/cloud${chosen}/Saves/README.txt" ] \
        && [ -f "${C2}/cloud${chosen}/Backups/README.txt" ] \
        && [ -f "${C2}/cloud${chosen}/Content/ROMs/README.txt" ] \
        && [ ! -e "${C2}/cloud/pixelelated" ]
    check $? "#508: seeding preserves selected ${chosen} paths and creates their folders" "rc ${RC}; selected paths changed, selected folders missing, or default namespace unexpectedly created"
done

fi

# #308 claude F-RS-13, gpt F-RS-19: one run, three low-level retries, on every
# call these two make -- not rclone's three runs of ten under the wizard's
# spinner (the bound --check already carries, #273).
unbounded() { awk '/^(lsf|lsd|mkdir|copyto) / && !(/--low-level-retries 3/ && /--retries 1/)' "${C2}/rec/argv"; }
c2reset path; c2 --seed-folders
[ -s "${C2}/rec/argv" ] && [ -z "$(unbounded)" ]; check $? "every rclone call --seed-folders makes carries the listing bound ($(grep -cE '^(lsf|mkdir|copyto) ' "${C2}/rec/argv") calls)" "unbounded: $(unbounded | head -2 | tr '\n' '|')"
rm -f "${C2}/rec/argv"; c2 --content-location
[ -s "${C2}/rec/argv" ] && [ "$(grep -c '^lsf ' "${C2}/rec/argv")" -ge 1 ] && [ -z "$(unbounded)" ]; check $? "and so does every listing --content-location makes ($(grep -c '^lsf ' "${C2}/rec/argv") listings)" "unbounded: $(unbounded | head -2 | tr '\n' '|')"

# #308 gpt F-RS-20: CONTENT_REMOTE="" is --use-content-root's "the root",
# which the content scripts read as the root (ROOT="qa:"); seeding put
# /pixelelated/Content in its place. ROMs/ and BIOS/ go at the root, and no
# README is dropped into the top of somebody's cloud.
c2reset path
sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE=""|' "${CONF2}"
c2 --seed-folders
[ "${RC}" -eq 0 ] && [ -f "${C2}/cloud/ROMs/README.txt" ] && [ -f "${C2}/cloud/BIOS/README.txt" ] && [ ! -e "${C2}/cloud/pixelelated/Content" ] && [ ! -e "${C2}/cloud/README.txt" ] && grep -qx 'OK /ROMs' "${C2}/out" && grep -qx 'OK /BIOS' "${C2}/out"; check $? "an empty CONTENT_REMOTE seeds ROMs/ and BIOS/ at the cloud's root, with no README at the top" "READMEs: $(readmes); ROCKNIX/Content: $([ -e "${C2}/cloud/pixelelated/Content" ] && echo made || echo absent); said: $(grep -E '^(OK|MISSING) ' "${C2}/out" | tr '\n' ' ') (#308 gpt F-RS-20)"
c2reset path
sed -i '/^CONTENT_REMOTE=/d' "${CONF2}"
c2 --seed-folders
[ "${RC}" -eq 0 ] && [ -f "${C2}/cloud/pixelelated/Content/ROMs/README.txt" ]; check $? "while a config with no CONTENT_REMOTE line at all still gets the default /pixelelated/Content" "READMEs: $(readmes)"

echo "  ab. cloud_scan (#350, D-CLOUD-156): the opening scan's three items, the content scan's one, the selected folder facts and the failures said"
# The script whole under bwrap, its three sibling reads shimmed beside it (the
# scripts find siblings next to themselves first), rclone answering an
# archive listing, ip answering a route unless told not to.
SC="${TMP}/sc"; mkdir -p "${SC}/shim" "${SC}/rec" "${SC}/repo" "${SC}/storage/.config" "${SC}/storage/.cache"
src_of "projects/ROCKNIX/packages/network/rclone/sources/cloud_scan" "${SC}/repo/cloud_scan"
printf 'export PATH=/shim:/usr/bin:/bin\n' > "${SC}/profile"
printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="/pixelelated/Saves"\nSETTINGS_REMOTE="/pixelelated/Backups"\nCONTENT_REMOTE="/pixelelated/Content"\n' > "${SC}/storage/.config/cloud_sync.conf"
printf '#!/bin/sh\necho "logger $*" >> /rec/log\n' > "${SC}/shim/logger"
printf '#!/bin/sh\n[ -e /rec/noroute ] || echo "default via 10.0.2.2 dev eth0"\n' > "${SC}/shim/ip"
printf '#!/bin/sh\ncase "$1" in --label) echo QA;; esac\n' > "${SC}/repo/cloud_device_id"
cat > "${SC}/repo/cloud_migrate_layout" <<'EOR'
#!/bin/sh
printf '%s\n' "$*" >> /rec/argv
case "$1" in
  --state) if [ -e /rec/superseded ] && [ ! -e /rec/followed ]; then printf 'SAVES=/ROCKNIX/Saves\nCURRENT=/pixelelated/Saves\nCURRENT_EXISTS=1\nSTATE=superseded-empty\n'
           else printf 'SAVES=/pixelelated/Saves\nCURRENT=/pixelelated/Saves\nCURRENT_EXISTS=1\nSTATE=current\n'; fi; exit 0 ;;
  --follow) touch /rec/followed; exit 0 ;;
  --join) if [ -e /rec/join-fail ]; then echo '>>> why YOUR CLOUD STOPPED ANSWERING'; exit 5
          elif [ -e /rec/join-layout-fail ]; then echo '>>> why THE PREVIOUS CLOUD MOVE NEEDS ITS ORIGINAL CONNECTION'; exit 5
          elif [ -e /rec/join-timeout ]; then exit 124; elif [ -e /rec/join ]; then touch /rec/joined; exit 0; else exit 3; fi ;;
esac
exit 1
EOR
cat > "${SC}/repo/cloud_setup" <<'EOR'
#!/bin/sh
printf '%s\n' "$*" >> /rec/argv
case "$1" in
  --content-location) printf 'CONTENT_REMOTE=/pixelelated/Content\nSTATE=ok\n'; exit 0 ;;
  --folder-state)
    [ ! -e /rec/folder-fail ] || { echo '>>> why YOUR CLOUD STOPPED ANSWERING'; exit 5; }
    [ ! -e /rec/folder-format-fail ] || { echo " >>> why YOUR CLOUD FOLDER COULDN'T BE READ" | sed 's/^ //'; exit 4; }
    [ ! -e /rec/folder-timeout ] || exit 124
    if [ -e /rec/superseded ]; then printf 'SAVES=/ROCKNIX/Saves\nSTATE=missing\nSAVES_EXISTS=0\n'
    else printf 'SAVES=/pixelelated/Saves\nSTATE=ready\nSAVES_EXISTS=1\n'; fi
    exit 0 ;;
esac
exit 1
EOR
SC_READY=current
[ "${MIGRATION_AVAILABLE}" -eq 1 ] || SC_READY=ready
cat > "${SC}/repo/cloud_content_restore" <<'EOR'
#!/bin/sh
printf '%s\n' "$*" >> /rec/argv
case "$1" in
  --scan) [ -e /rec/scan-fail ] && { echo "Your cloud couldn't be read. Try again." >&2; exit 5; }; printf 'gb|100|1|50|1|0|50|0\nbios|10|1|10|0|0|0|0\n'; exit 0 ;;
  --systems) echo gb; exit 0 ;;
esac
exit 1
EOR
cat > "${SC}/shim/rclone" <<'EOR'
#!/bin/sh
printf '%s\n' "$*" >> /rec/argv
case "$1" in
  listremotes) [ -e /rec/noremote ] || echo "qa:" ;;
  lsf) case "$*" in *--dirs-only*) printf 'pixelelated/\nPhotos/\n' ;;
            *) printf '2026_09_01-000000-QA-ROCKNIX_SETTINGS.tar.gz\n2026_09_20-000000-Other-ROCKNIX_SETTINGS.tar.gz\n2026_09_10-000000-QA-ROCKNIX_SETTINGS.tar.gz\nROCKNIX_BACKUP.zip\n' ;; esac ;;
esac
exit 0
EOR
chmod +x "${SC}/shim"/* "${SC}/repo"/*
sc_run() { SCRC=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
      --ro-bind /etc /etc --ro-bind "${SC}/profile" /etc/profile --ro-bind "${SC}/shim" /shim --bind "${SC}/rec" /rec --ro-bind "${SC}/repo" /repo \
      --dev /dev --proc /proc --tmpfs /tmp --bind "${SC}/storage" /storage \
      bash /repo/cloud_scan "$@" > "${SC}/out" 2>&1; echo $? ) 2>/dev/null ); }
sc_out() { tr '\n' '|' < "${SC}/out" | cut -c1-200; }
SCO="${SC}/storage/.cache/cloud_sync/scan"
rm -f "${SC}"/rec/*; sc_run
[ "${SCRC}" = 0 ] && [ "$(grep '^>>> unit' "${SC}/out" | tr '\n' ' ')" = ">>> unit CLOUD FOLDER|| >>> unit SETTINGS BACKUPS|| >>> unit GAME CONTENT|| " ] && [ "$(grep -c '^>>> doing scan' "${SC}/out")" = 3 ]; check $? "the opening scan announces CLOUD FOLDER, SETTINGS BACKUPS, GAME CONTENT in that order, each with its doing line, and exits 0 (rc ${SCRC})" "$(sc_out)"
[ -f "${SCO}/done" ] && [ "$(sed -n 's/^STATE=//p' "${SCO}/state")" = "${SC_READY}" ] && [ "$(tr '\n' ' ' < "${SCO}/root-dirs")" = "pixelelated Photos " ] && [ ! -f "${SCO}/scan" ] && ! grep -q -- '--follow' "${SC}/rec/argv"; check $? "its files hold the state, the root folders and the done stamp; no content listing yet, no follow on a current folder" "$(ls "${SCO}" 2>/dev/null | tr '\n' ' ')"
[ "$(sed -n 's/^MINE=//p' "${SCO}/settings")" = "2026_09_10-000000-QA-ROCKNIX_SETTINGS.tar.gz" ] && [ "$(sed -n 's/^NEWEST=//p' "${SCO}/settings")" = "2026_09_20-000000-Other-ROCKNIX_SETTINGS.tar.gz" ] && [ "$(sed -n 's/^COUNT=//p' "${SCO}/settings")" = 4 ] && [ "$(sed -n 's/^LABEL=//p' "${SCO}/settings")" = QA ]; check $? "the settings facts: this device's newest by label, the newest overall, the count, the label (D-CLOUD-162)" "$(cat "${SCO}/settings" 2>/dev/null | tr '\n' ' ')"
grep -q 'lsf --files-only --include /\*.{zip,tar.gz} qa:/pixelelated/Backups/ --contimeout 15s' "${SC}/rec/argv"; check $? "the archive listing is bounded and reads the Backups folder" "$(grep '^lsf' "${SC}/rec/argv" | head -1)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/noroute"; sc_run
[ "${SCRC}" = 69 ] && ! grep -q '>>> unit' "${SC}/out" && [ ! -f "${SCO}/done" ]; check $? "no default route: exit 69, nothing announced, no done stamp (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/noremote"; sc_run
[ "${SCRC}" = 1 ] && grep -q "^>>> why YOUR CLOUD STORAGE ISN'T SET UP YET" "${SC}/out"; check $? "no remote: exit 1 with its why (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/scan-fail"; sc_run
[ "${SCRC}" = 0 ] && [ -f "${SCO}/done" ]; check $? "a content listing is not the opening scan's to fail: the scan-fail flag leaves the opening scan at 0 (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*; sc_run --content --with-media
[ "${SCRC}" = 0 ] && [ "$(grep '^>>> unit' "${SC}/out" | tr '\n' ' ')" = ">>> unit ROMS, BIOS, AND GAME CONTENT|| " ] && grep -q '^>>> doing compare' "${SC}/out" \
   && grep -qx -- '--scan --with-media' "${SC}/rec/argv" && [ "$(grep -c . "${SCO}/scan")" = 2 ] && [ "$(cat "${SCO}/systems")" = gb ] && [ -f "${SCO}/content-done" ]; check $? "--content --with-media announces one item in the ticked classes, passes the flag to --scan, writes the rows, the systems and its own stamp (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*; sc_run --content --media-only
[ "${SCRC}" = 0 ] && grep -q '^>>> unit GAME CONTENT||' "${SC}/out" && grep -qx -- '--scan --media-only' "${SC}/rec/argv"; check $? "--content --media-only is the GAME CONTENT item with --scan --media-only (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/scan-fail"; sc_run --content
[ "${SCRC}" = 5 ] && grep -q '^>>> why YOUR CLOUD STOPPED ANSWERING' "${SC}/out" && [ ! -f "${SCO}/content-done" ] && grep -q '^>>> unit ROMS AND BIOS||' "${SC}/out"; check $? "a content listing the cloud refused (5): the ROMS AND BIOS item, the why, no content stamp (rc ${SCRC})" "$(sc_out)"
if [ "${MIGRATION_AVAILABLE}" -eq 1 ]; then
rm -f "${SC}"/rec/*; touch "${SC}/rec/superseded"; sc_run
[ "${SCRC}" = 0 ] && grep -qx -- '--follow' "${SC}/rec/argv" && [ "$(sed -n 's/^STATE=//p' "${SCO}/state")" = current ] && [ "$(grep -cx -- '--state' "${SC}/rec/argv")" = 2 ]; check $? "a superseded, empty folder beside a current one that exists is followed in the scan, and the state re-read (rc ${SCRC})" "$(sc_out) $(tr '\n' ' ' < "${SC}/rec/argv")"

# The scan's join (D-CLOUD-169): run before --state; nothing to join (3) and a join (0) both go on to the
# state; a join the cloud refused, or one that ran out its time, ends the scan with the card's sentence, no
# state and no done stamp -- a cloud that cannot be read is not an empty one.
rm -f "${SC}"/rec/*; touch "${SC}/rec/join"; sc_run
[ "${SCRC}" = 0 ] && [ -e "${SC}/rec/joined" ] && [ "$(grep -nx -- '--join' "${SC}/rec/argv" | cut -d: -f1)" -lt "$(grep -nx -- '--state' "${SC}/rec/argv" | head -1 | cut -d: -f1)" ] && [ -f "${SCO}/done" ]; check $? "the scan joins before it reads the state, and goes on (rc ${SCRC})" "$(sc_out); argv: $(tr '\n' ' ' < "${SC}/rec/argv" | cut -c1-160)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/join-fail"; sc_run
[ "${SCRC}" = 5 ] && grep -q '^>>> why YOUR CLOUD STOPPED ANSWERING' "${SC}/out" && ! grep -qx -- '--state' "${SC}/rec/argv" && [ ! -f "${SCO}/done" ]; check $? "a join the cloud refused ends the scan with its why, before any state is written (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/join-layout-fail"; sc_run
[ "${SCRC}" = 5 ] && grep -q '^>>> why THE PREVIOUS CLOUD MOVE NEEDS ITS ORIGINAL CONNECTION' "${SC}/out" && ! grep -q '^>>> why YOUR CLOUD STOPPED ANSWERING' "${SC}/out" && [ ! -f "${SCO}/done" ]; check $? "an application refusal sharing code 5 keeps its own connection-recovery reason" "$(sc_out)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/join-timeout"; sc_run
[ "${SCRC}" = 124 ] && grep -q '^>>> why YOUR CLOUD STOPPED ANSWERING' "${SC}/out" && [ ! -f "${SCO}/done" ]; check $? "and one that ran out its time says the cloud stopped answering (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*
else
rm -f "${SC}"/rec/*; touch "${SC}/rec/superseded"; sc_run
[ "${SCRC}" = 0 ] && grep -qx 'STATE=missing' "${SCO}/state" \
    && grep -qx 'SAVES=/ROCKNIX/Saves' "${SCO}/state" \
    && ! grep -qE '^--(join|follow|settle|apply|state)$' "${SC}/rec/argv"
check $? "#508: scan retains selected legacy folder facts without joining or following" "$(sc_out) $(tr '\n' ' ' < "${SC}/rec/argv")"
for failure in folder-fail folder-format-fail folder-timeout; do
    rm -f "${SC}"/rec/*; touch "${SC}/rec/${failure}"; sc_run
    case "${failure}" in folder-fail) want=5; why="YOUR CLOUD STOPPED ANSWERING";; folder-format-fail) want=4; why="YOUR CLOUD FOLDER COULDN'T BE READ";; folder-timeout) want=124; why="YOUR CLOUD STOPPED ANSWERING";; esac
    [ "${SCRC}" = "${want}" ] && grep -qFx ">>> why ${why}" "${SC}/out" && [ ! -f "${SCO}/done" ]
    check $? "#508: ${failure} preserves its status/reason and writes no done stamp" "rc ${SCRC}; $(sc_out)"
done
rm -f "${SC}"/rec/*
fi

if [ "${MIGRATION_AVAILABLE}" -eq 1 ]; then
# --folder, the cloud folder step's scan (D-CLOUD-170, #363): the folder item alone -- the join, the state, the
# quiet follow -- with nothing listed for the options page and the opening scan's files left as they were.
rm -f "${SC}"/rec/*; sc_run
# a done stamp no run of this second could write, so a rewrite cannot pass for the old one
SCDONE=1700000000; echo "${SCDONE}" > "${SCO}/done"; rm -f "${SC}"/rec/*; touch "${SC}/rec/join"; sc_run --folder
[ "${SCRC}" = 0 ] && [ "$(grep '^>>> unit' "${SC}/out" | tr '\n' ' ')" = ">>> unit CLOUD FOLDER|| " ] && [ -e "${SC}/rec/joined" ] && [ "$(sed -n 's/^STATE=//p' "${SCO}/state")" = current ]; check $? "--folder announces the CLOUD FOLDER item alone, joins, and writes the state (rc ${SCRC})" "$(sc_out); argv: $(tr '\n' ' ' < "${SC}/rec/argv" | cut -c1-160)"
! grep -q '^lsf' "${SC}/rec/argv" && ! grep -q -- '--content-location' "${SC}/rec/argv" && [ "$(cat "${SCO}/done" 2>/dev/null)" = "${SCDONE}" ] && [ -s "${SCO}/settings" ]; check $? "--folder lists no archives and no root, and leaves the opening scan's files and done stamp as they were" "argv: $(tr '\n' ' ' < "${SC}/rec/argv" | cut -c1-200); done $(cat "${SCO}/done" 2>/dev/null) was ${SCDONE}"
rm -f "${SC}"/rec/*; touch "${SC}/rec/superseded"; sc_run --folder
[ "${SCRC}" = 0 ] && grep -qx -- '--follow' "${SC}/rec/argv" && [ "$(sed -n 's/^STATE=//p' "${SCO}/state")" = current ]; check $? "--folder follows a superseded, empty folder beside a current one -- the one place it does, since no sync asks (rc ${SCRC})" "$(sc_out) $(tr '\n' ' ' < "${SC}/rec/argv")"
rm -f "${SC}"/rec/*; touch "${SC}/rec/join-fail"; sc_run --folder
[ "${SCRC}" = 5 ] && grep -q '^>>> why YOUR CLOUD STOPPED ANSWERING' "${SC}/out" && [ ! -f "${SCO}/state" ]; check $? "--folder with a join the cloud refused ends with its why and no state, so the step offers nothing from a guess (rc ${SCRC})" "$(sc_out)"
else
# Current folder-only scan preserves the normal scan's unrelated results.
rm -f "${SC}"/rec/*; sc_run
SCDONE=1700000000; echo "${SCDONE}" > "${SCO}/done"
rm -f "${SC}"/rec/*; touch "${SC}/rec/superseded"; sc_run --folder
[ "${SCRC}" = 0 ] && grep -qx '>>> unit CLOUD FOLDER||' "${SC}/out" \
    && grep -qx 'STATE=missing' "${SCO}/state" && grep -qx -- '--folder-state' "${SC}/rec/argv" \
    && [ "$(cat "${SCO}/done")" = "${SCDONE}" ] && [ -s "${SCO}/settings" ] \
    && ! grep -qE '^(lsf |--(join|follow|settle|apply)$)' "${SC}/rec/argv"
check $? "#508: folder-only scan reads selected folder facts and preserves archive/done results" "rc ${SCRC}; $(sc_out)"
rm -f "${SC}"/rec/*; touch "${SC}/rec/folder-fail"; sc_run --folder
[ "${SCRC}" = 5 ] && grep -qx '>>> why YOUR CLOUD STOPPED ANSWERING' "${SC}/out" && ! grep -q '^STATE=' "${SCO}/state"
check $? "#508: failed folder-only read has its reason and no usable state" "rc ${SCRC}; $(sc_out)"
fi
rm -f "${SC}"/rec/*; touch "${SC}/rec/noroute"; sc_run --folder
[ "${SCRC}" = 69 ] && [ ! -f "${SCO}/state" ]; check $? "--folder with no route exits 69, the page's SKIPPED - YOU'RE NOT ONLINE (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*; sc_run --bogus
[ "${SCRC}" = 2 ] && grep -q -- '--folder' "${SC}/out"; check $? "an unknown mode is refused with the usage, which names --folder (rc ${SCRC})" "$(sc_out)"
rm -f "${SC}"/rec/*


printf "focused: failures=%s not_applicable=%s\n" "${FAIL}" "${NOT_APPLICABLE}"
[ "${FAIL}" -eq 0 ]

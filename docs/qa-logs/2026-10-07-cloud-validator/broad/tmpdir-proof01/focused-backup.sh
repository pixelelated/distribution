#!/bin/bash
set -u
ROOT=/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders
RCLONE_REL=projects/ROCKNIX/packages/network/rclone/sources
BT_REL=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
OLD=0; BASE_REF=3268015c; FAIL=0
check() { if [ "$1" -eq 0 ]; then echo "PASS $2"; else echo "FAIL $3"; FAIL=$((FAIL+1)); fi; }
# Honor the caller's build-drive TMPDIR for the owned host fixture tree only.
# Bubblewrap descendants get a private /tmp, so an inherited host-only path
# makes otherwise valid mktemp calls fail inside the device fixture.
TMP="$(mktemp -d)" || { echo "cannot create host fixture directory" >&2; exit 2; }
trap 'rm -rf "${TMP}"' EXIT
unset TMPDIR
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

mkdir -p "${TMP}/src"
src_of "${BT_REL}" "${TMP}/src/backuptool"
BT="${TMP}/src/backuptool"
printf 'host_fixture=%s inherited_TMPDIR=%s\n' "$TMP" "${TMPDIR-unset}"
echo "  b. backuptool: a kill mid-tar leaves the previous archive; a failed restore puts the snapshot back"
B="${TMP}/b"; ST="${B}/storage"
mkdir -p "${ST}/.config/system/configs" "${ST}/.config/test" "${ST}/roms/backup" "${B}/shim" "${B}/repo"
cp "${BT}" "${B}/repo/backuptool"
printf 'export PATH=/shim:/usr/bin:/bin\nexport OS_NAME=ROCKNIX\n' > "${B}/profile"
printf '#!/bin/sh\necho "logger $*" >&2\n' > "${B}/shim/logger"
printf '#!/bin/sh\necho "systemctl $*"\n' > "${B}/shim/systemctl"
printf '#!/bin/sh\nexit 0\n' > "${B}/shim/sleep"
chmod +x "${B}/shim"/*
printf 'system.hostname=X\nwifi.key=SECRET\n' > "${ST}/.config/system/configs/system.cfg"
printf 'LOCATIONS=(\n  /storage/.config/system/configs/system.cfg\n  /storage/.config/test/*\n)\n' > "${ST}/.config/backuptool.conf"
for i in 1 2 3; do echo "file${i}" > "${ST}/.config/test/f${i}"; done
# Run backuptool whole, inside bwrap: the repo copy at /repo, a stub profile,
# the fake /storage, shims first on PATH. setsid gives each run its own
# process group, which is what the dying tar kills.
bt() { # <verb...>; stdout+stderr to $OUT, rc in $RC (137 when the group was killed)
    # In a subshell so the shell's own "Killed" notice for the dying group
    # does not land in the test's output.
    RC=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${B}/profile" /etc/profile \
        --bind "${ST}" /storage --ro-bind "${B}/shim" /shim --ro-bind "${B}/repo" /repo \
        --dev /dev --proc /proc --tmpfs /tmp \
        bash /repo/backuptool "$@" > "${OUT}" 2>&1; echo $? ) 2>/dev/null )
}
OUT="${B}/out"
bt backup; rc1=${RC}
first=$(ls "${ST}/roms/backup"/*.tar.gz 2>/dev/null)
[ "${rc1}" -eq 0 ] && [ -n "${first}" ] && [ "$(echo "${first}" | wc -l)" -eq 1 ]; check $? "a first backup writes one archive at the root (rc 0)" "rc ${rc1}; root holds: $(ls "${ST}/roms/backup" 2>/dev/null | tr '\n' ' '); out: $(tail -3 "${OUT}" | tr '\n' '|')"
tar -tzf "${first}" 2>/dev/null | grep -q 'storage/.config/test/f1$'; check $? "and it lists back whole" "archive does not list"
! tar -xzOf "${first}" storage/.config/system/configs/system.cfg 2>/dev/null | grep -q SECRET; check $? "with the wifi key stripped" "the archive carries the wifi key"
sleep 1  # a new stamp, so the second archive has a distinct name
bt backup; rc2=${RC}
second=$(ls "${ST}/roms/backup"/*.tar.gz 2>/dev/null)
[ "${rc2}" -eq 0 ] && [ "$(echo "${second}" | wc -l)" -eq 1 ] && [ "${second}" != "${first}" ] && [ -f "${ST}/roms/backup/archive/$(basename "${first}")" ]; check $? "a second backup rotates the first into archive/ and leaves one at the root" "rc ${rc2}; root: $(ls "${ST}/roms/backup" | tr '\n' ' '); archive: $(ls "${ST}/roms/backup/archive" 2>/dev/null | tr '\n' ' ')"

# The kill: tar writing the archive emits 1 MiB and SIGKILLs its own
# process group -- bwrap, the script, itself. Every other tar call is real.
cat > "${B}/shim/tar" <<'EOS'
#!/bin/bash
out=""; prev=""
for a in "$@"; do [ "${prev}" = "-czf" ] && out="${a}"; prev="${a}"; done
if [ -n "${out}" ]; then
    head -c 1048576 /dev/zero > "${out}"
    kill -9 -- "-$(cut -d' ' -f5 /proc/self/stat)"
    sleep 5
    exit 1
fi
exec /usr/bin/tar "$@"
EOS
chmod +x "${B}/shim/tar"
sleep 1
bt backup; rck=${RC}
roots=$(ls "${ST}/roms/backup"/*.tar.gz 2>/dev/null)
partials=$(ls "${ST}/roms/backup"/*.partial 2>/dev/null)
[ "${rck}" -ne 0 ]; check $? "the run died (rc ${rck})" "the run exited 0 through a tar that killed the group"
[ "${roots}" = "${second}" ]; check $? "the previous archive is still the only *.tar.gz at the root" "root *.tar.gz: '$(echo "${roots}" | tr '\n' ' ')' -- expected only $(basename "${second}")"
[ -n "${partials}" ] && [ "$(echo "${partials}" | wc -l)" -eq 1 ]; check $? "a .partial sits beside it ($(basename "${partials:-none}"))" "partials at the root: '$(echo "${partials}" | tr '\n' ' ')' -- the truncated archive was written under the final name"
[ "$(ls "${ST}/roms/backup/archive"/*.tar.gz 2>/dev/null | wc -l)" -eq 1 ]; check $? "archive/ is unchanged (still one archive)" "archive/ holds $(ls "${ST}/roms/backup/archive" 2>/dev/null | wc -l) file(s): rotation ran before the new archive existed"
rm -f "${B}/shim/tar"

# A restore whose extraction fails: the shim extracts for real, then damages
# one restored file and exits 1 -- what a cut mid-extract leaves. The
# snapshot's own extraction (from archive/) is real.
echo changed > "${ST}/.config/test/f1"
cat > "${B}/shim/tar" <<'EOS'
#!/bin/bash
if [ "$1" = "-xzf" ] && [[ "$2" != */archive/* ]] && [ "$3" = "-C" ] && [ "$4" = "/" ]; then
    /usr/bin/tar "$@"
    echo garbage > /storage/.config/test/f2
    exit 1
fi
exec /usr/bin/tar "$@"
EOS
chmod +x "${B}/shim/tar"
bt restore; rcr=${RC}
[ "${rcr}" -ne 0 ]; check $? "a restore whose extraction fails exits non-zero" "rc 0 from a failed extraction"
[ "$(cat "${ST}/.config/test/f1")" = "changed" ] && [ "$(cat "${ST}/.config/test/f2")" = "file2" ]; check $? "and the pre-restore state was put back (f1 'changed', f2 'file2')" "f1='$(cat "${ST}/.config/test/f1")' f2='$(cat "${ST}/.config/test/f2")' -- the tree is half the archive, half the old state"
ls "${ST}/roms/backup/archive"/*PRE_RESTORE* >/dev/null 2>&1; check $? "the snapshot is in archive/ as *PRE_RESTORE*" "no PRE_RESTORE snapshot in archive/: $(ls "${ST}/roms/backup/archive" 2>/dev/null | tr '\n' ' ')"
grep -q 'YOUR SETTINGS ARE UNCHANGED' "${OUT}"; check $? "and the screen says the settings are unchanged" "screen: $(grep -v '^logger' "${OUT}" | tail -2 | tr '\n' '|')"

! grep -vE '^logger |^>>> ' "${OUT}" | grep -qiE "logger|/storage/|/var/log|exit [0-9]"; check $? "with no path, log or tool name on it" "a screen line carries one: $(grep -vE '^logger |^>>> ' "${OUT}" | grep -iE 'logger|/storage/|/var/log|exit [0-9]' | head -1)"
rm -f "${B}/shim/tar"
# A restore that works, asked to leave the journey marker.
echo changed > "${ST}/.config/test/f1"
bt restore --then-cloud; rcg=${RC}
[ "${rcg}" -eq 0 ] && [ "$(cat "${ST}/.config/test/f1")" = "file1" ] && [ -e "${ST}/.config/.cloud-journey-pending" ]; check $? "a good restore --then-cloud restores f1 and leaves .cloud-journey-pending" "rc ${rcg}; f1='$(cat "${ST}/.config/test/f1")'; marker: $([ -e "${ST}/.config/.cloud-journey-pending" ] && echo yes || echo no)"


echo "  f. backuptool: rclone.conf never enters an archive, and the scanner knows rclone's key names (#52)"
# Its own staging tree: the cases above read "the newest archive" and must
# not find this one.
B2="${TMP}/f"; ST2="${B2}/storage"
mkdir -p "${ST2}/.config/system/configs" "${ST2}/.config/test" "${ST2}/.config/rclone" "${ST2}/.config/emulationstation" "${ST2}/roms/backup" "${B2}/shim" "${B2}/repo"
cp "${BT}" "${B2}/repo/backuptool"
printf 'export PATH=/shim:/usr/bin:/bin\nexport OS_NAME=ROCKNIX\n' > "${B2}/profile"
printf '#!/bin/sh\necho "logger $*" >&2\n' > "${B2}/shim/logger"
printf '#!/bin/sh\necho "systemctl $*"\n' > "${B2}/shim/systemctl"
printf '#!/bin/sh\nexit 0\n' > "${B2}/shim/sleep"
chmod +x "${B2}/shim"/*
printf 'system.hostname=X\n' > "${ST2}/.config/system/configs/system.cfg"
printf '[qa]\ntype = dropbox\ntoken = {"access_token":"QA-SECRET-TOKEN","refresh_token":"QA-REFRESH"}\n' > "${ST2}/.config/rclone/rclone.conf"
echo plain > "${ST2}/.config/test/plain.txt"
# es_settings.cfg is XML, which the line-anchored leak scan cannot read, so the
# strip at the archive is its only guard: the ScreenScraper passwords (#64)
# and the IGDB client secret (#274, found by #221's trace). No harness case
# read this strip before 2026-09-25.
printf '<?xml version="1.0"?>\n<config>\n<string name="ScreenScraperUser" value="qa-user" />\n<string name="ScreenScraperPass" value="QA-SECRET-SS" />\n<string name="ScreenScraperDevPass" value="QA-SECRET-DEV" />\n<string name="IGDBClientID" value="qa-client" />\n<string name="IGDBSecret" value="QA-SECRET-IGDB" />\n<string name="ThemeSet" value="art-book-next" />\n</config>\n' > "${ST2}/.config/emulationstation/es_settings.cfg"
printf 'LOCATIONS=(\n  /storage/.config/system/configs/system.cfg\n  /storage/.config/test/*\n  /storage/.config/rclone/*\n  /storage/.config/emulationstation/*\n)\n' > "${ST2}/.config/backuptool.conf"
OUT2="${B2}/out"
RC2=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
    --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
    --ro-bind /etc /etc --ro-bind "${B2}/profile" /etc/profile \
    --bind "${ST2}" /storage --ro-bind "${B2}/shim" /shim --ro-bind "${B2}/repo" /repo \
    --dev /dev --proc /proc --tmpfs /tmp \
    bash /repo/backuptool backup > "${OUT2}" 2>&1; echo $? ) 2>/dev/null )
arc=$(ls "${ST2}/roms/backup"/*.tar.gz 2>/dev/null | head -1)
[ "${RC2}" -eq 0 ] && [ -n "${arc}" ]; check $? "a backup with rclone.conf in LOCATIONS completes (rc ${RC2})" "rc ${RC2}, archive: '${arc}'"
! tar -tzf "${arc}" 2>/dev/null | grep -q 'rclone/rclone.conf$'; check $? "rclone.conf is not in the archive" "the archive lists rclone.conf"
! tar -xzOf "${arc}" 2>/dev/null | grep -q 'QA-SECRET-TOKEN'; check $? "and no token travelled in any member" "a member carries the token"
tar -tzf "${arc}" 2>/dev/null | grep -q 'test/plain.txt$'; check $? "files that are not held back are archived as before" "plain.txt missing"
grep -q 'rclone.conf held back' "${OUT2}"; check $? "the log says rclone.conf was held back" "no held-back line: $(grep logger "${OUT2}" | tail -2 | tr '\n' ' ')"
# The scanner knows rclone's key names. Since #307 PL-005 a hit ends the
# backup before the archive is named (it used to warn and upload): so the
# file it must see is added for a second run, which leaves the first
# archive as the only one and counts the two lines in the log.
printf 'name = probe\npass = QA-SECRET-PASS\npassword2 = QA-SECRET-SALT\n' > "${ST2}/.config/test/leaky.conf"
RC2B=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
    --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
    --ro-bind /etc /etc --ro-bind "${B2}/profile" /etc/profile \
    --bind "${ST2}" /storage --ro-bind "${B2}/shim" /shim --ro-bind "${B2}/repo" /repo \
    --dev /dev --proc /proc --tmpfs /tmp \
    bash /repo/backuptool backup > "${OUT2}.leak" 2>&1; echo $? ) 2>/dev/null )
[ "${RC2B}" -ne 0 ] && grep -q '^>>> why A SIGN-IN WAS FOUND IN THE BACKUP' "${OUT2}.leak" && grep -q 'found 2 line(s) that look like a password or key' "${OUT2}.leak" && [ "$(ls "${ST2}/roms/backup"/*.tar.gz)" = "${arc}" ] && ! tar -xzOf "${arc}" 2>/dev/null | grep -q 'QA-SECRET-PASS'; check $? "the scanner sees the pass= and password2= lines in a file it does not hold back (2 lines), and the backup ends there with the last archive unchanged (#307 PL-005)" "rc ${RC2B}; said: $(grep -E '^>>> why|found [0-9]+ line' "${OUT2}.leak" | tr '\n' ' ' | cut -c1-200); archives: $(ls "${ST2}/roms/backup"/*.tar.gz 2>/dev/null | wc -l)"
rm -f "${ST2}/.config/test/leaky.conf"
# #221: a clean backup is silent. The keys every shipped retroarch.cfg and
# Amiberry's conf carry end in "key" or "pass" and are not credentials.
B3="${TMP}/f3"; ST3="${B3}/storage"
mkdir -p "${ST3}/.config/system/configs" "${ST3}/.config/test" "${ST3}/roms/backup"
printf 'system.hostname=X\n' > "${ST3}/.config/system/configs/system.cfg"
printf 'input_enable_hotkey = "nul"\ncore_info_savestate_bypass = "false"\ncheevos_password = ""\n' > "${ST3}/.config/test/retroarch.cfg"
printf 'default_open_gui_key=F12\n' > "${ST3}/.config/test/adfdir.conf"
printf 'LOCATIONS=(\n  /storage/.config/system/configs/system.cfg\n  /storage/.config/test/*\n)\n' > "${ST3}/.config/backuptool.conf"
OUT3="${B3}/out"
RC3=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
    --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
    --ro-bind /etc /etc --ro-bind "${B2}/profile" /etc/profile \
    --bind "${ST3}" /storage --ro-bind "${B2}/shim" /shim --ro-bind "${B2}/repo" /repo \
    --dev /dev --proc /proc --tmpfs /tmp \
    bash /repo/backuptool backup > "${OUT3}" 2>&1; echo $? ) 2>/dev/null )
[ "${RC3}" -eq 0 ] && ! grep -q 'LOOK LIKE PASSWORDS OR KEYS' "${OUT3}"; check $? "a clean backup is silent: input_enable_hotkey, core_info_savestate_bypass and default_open_gui_key are not credentials (#221)" "rc ${RC3}: $(grep 'LOOK LIKE' "${OUT3}" | head -1 | cut -c1-80)"
ESARC=$(tar -xzOf "${arc}" --wildcards '*/emulationstation/es_settings.cfg' 2>/dev/null)
[ -n "${ESARC}" ] && ! echo "${ESARC}" | grep -q 'QA-SECRET-SS\|QA-SECRET-DEV\|QA-SECRET-IGDB'; check $? "es_settings.cfg is archived without the ScreenScraper passwords or the IGDB client secret (#64, #274)" "archived es_settings.cfg: $(echo "${ESARC}" | grep -c 'QA-SECRET') secret value(s) present, $(echo "${ESARC}" | wc -l) lines"
echo "${ESARC}" | grep -q 'name="ScreenScraperUser"' && echo "${ESARC}" | grep -q 'name="IGDBClientID"' && echo "${ESARC}" | grep -q 'name="ThemeSet"'; check $? "and its other settings travel (the user names, the client id, the theme)" "archived es_settings.cfg lost a harmless line: $(echo "${ESARC}" | grep -c 'name=') of 4 kept"


echo "  k. backuptool: what the image ships does not travel, and an older archive's copy of it is not put back (#45); a RetroAchievements token travels in no shape (#169)"
# A fake /usr/config beside the real /usr (bwrap cannot make a mountpoint
# under a read-only /usr, so /usr is bound a subdirectory at a time). Under
# /storage/.config: shipped seeds unchanged (cheat.db, test/seed), a file the
# player edited (ppsspp.ini), a file with no counterpart (test/own), and an
# asset and a cache entry, which never travel, edited or not.
K="${TMP}/k"; KS="${K}/storage"; KU="${K}/usrconfig"
mkdir -p "${KS}/.config/ppsspp/assets/lang" "${KS}/.config/ppsspp/PSP/SYSTEM/CACHE" "${KS}/.config/ppsspp/PSP/Cheats" "${KS}/.config/test" "${KS}/roms/backup" \
         "${KU}/ppsspp/assets/lang" "${KU}/ppsspp/PSP/SYSTEM" "${KU}/ppsspp/PSP/Cheats" "${KU}/test"
head -c 65536 /dev/urandom > "${KU}/ppsspp/PSP/Cheats/cheat.db"; cp "${KU}/ppsspp/PSP/Cheats/cheat.db" "${KS}/.config/ppsspp/PSP/Cheats/cheat.db"
echo "shipped seed" > "${KU}/test/seed"; cp "${KU}/test/seed" "${KS}/.config/test/seed"
echo "shipped ini" > "${KU}/ppsspp/PSP/SYSTEM/ppsspp.ini"; echo "the player's ini" > "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp.ini"
echo "shipped strings" > "${KU}/ppsspp/assets/lang/en_US.ini"; echo "edited strings" > "${KS}/.config/ppsspp/assets/lang/en_US.ini"
echo "shader cache" > "${KS}/.config/ppsspp/PSP/SYSTEM/CACHE/x.cache"
echo "the player's own" > "${KS}/.config/test/own"
# The RetroAchievements token the standalone emulators' cheevos_*.sh scripts
# copy out of system.cfg at every launch (#169): the four files that hold
# only the token, the four settings files with a token line in them, each
# in the shape its script writes, and one file the strip does not know, with
# a different value, for the scanner. The planted value must appear in no
# member of the archive; the settings files must arrive with the key kept
# and the value gone.
KTOK="QA-RA-TOKEN-PLANTED"; KTOK2="QA-SECRET-TOKEN-UNKNOWN"
mkdir -p "${KS}/.config/dolphin-emu" "${KS}/.config/SkyEmu" "${KS}/.config/ARMSX2/inis" "${KS}/.config/duckstation" "${KS}/.config/melonDS" "${KS}/.config/flycast" "${KS}/.config/aethersx2/inis" "${KS}/.config/gopher64"
echo "${KTOK}" > "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat"
printf '[Achievements]\nEnabled = True\nUsername = qa\nApiToken = %s\n' "${KTOK}" > "${KS}/.config/dolphin-emu/RetroAchievements.ini"
printf 'qa\n%s\n' "${KTOK}" > "${KS}/.config/SkyEmu/ra_token.txt"
printf '[Achievements]\nToken = %s\n' "${KTOK}" > "${KS}/.config/ARMSX2/inis/secrets.ini"
# gopher64 writes its own token file after the launcher's --ra-password login (#169's trace, #273)
printf '{"username":"qa","token":"%s","enabled":true,"hardcore":false}\n' "${KTOK}" > "${KS}/.config/gopher64/retroachievements.json"
printf '[Cheevos]\nEnabled = true\nUsername = qa\nToken = %s\nLoginTimestamp = 1\n' "${KTOK}" > "${KS}/.config/duckstation/settings.ini"
printf 'RA_Enabled=1\nRA_Username=qa\nRA_Password=%s\nRA_Token=%s\nRA_HardcoreMode=0\n' "${KTOK}" "${KTOK}" > "${KS}/.config/melonDS/melonDS.ini"
printf '[achievements]\nEnabled = yes\nUserName = qa\nToken = %s\n' "${KTOK}" > "${KS}/.config/flycast/emu.cfg"
printf '[Achievements]\nEnabled = true\nUsername = qa\nToken = %s\nLoginTimestamp = 1\n' "${KTOK}" > "${KS}/.config/aethersx2/inis/PCSX2.ini"
# The offline RetroAchievements proxy's folder (#165): its SQLite cache with
# the token in a cached login row, the HMAC key that signs the award queue,
# its config and its log -- every file under it is held back, whatever it is
# called, so the fixture has one of each shape plus a nested one.
mkdir -p "${KS}/.config/raofflineproxy/image_cache/games"
printf 'SQLite format 3\0login2::qa {"Token":"%s"}\n' "${KTOK}" > "${KS}/.config/raofflineproxy/proxy.sqlite3"
head -c 32 /dev/urandom > "${KS}/.config/raofflineproxy/award_secret.key"
printf '{"proxy_port": 8080}\n' > "${KS}/.config/raofflineproxy/config.json"
printf 'service started\n' > "${KS}/.config/raofflineproxy/service.log"
printf 'PNG\n' > "${KS}/.config/raofflineproxy/image_cache/games/1.png"
printf 'LOCATIONS=(\n  /storage/.config/ppsspp/*\n  /storage/.config/test/*\n  /storage/.config/dolphin-emu/*\n  /storage/.config/SkyEmu/*\n  /storage/.config/ARMSX2/*\n  /storage/.config/duckstation/*\n  /storage/.config/melonDS/*\n  /storage/.config/flycast/*\n  /storage/.config/aethersx2/*\n  /storage/.config/gopher64/*\n  /storage/.config/raofflineproxy/*\n)\n' > "${KS}/.config/backuptool.conf"
UB=(); for d in /usr/*/; do d="${d%/}"; UB+=(--ro-bind "${d}" "${d}"); done
# tar and unzip are the image's busybox here when a build root is on this
# machine: the restore's -X and -x exclusion lists are what this case
# grades, and their semantics are the device's, not GNU tar's or Info-ZIP's
# (#151 PL-10 -- until then the device's -X had been proven once, by hand,
# on a guest). The binary is bound in at its own path so the shims' exec
# lines resolve inside the sandbox.
mkdir -p "${K}/kshim"; KBB=()
if [ -n "${BB}" ]; then
    # crc32: the zip check reads a stored member's CRC with it (the audit of
    # the fix round, PL-022).
    for a in tar unzip crc32; do printf '#!/bin/sh\n[ -x %s ] && exec %s %s "$@"\nexec %s %s "$@"\n' "${BB}" "${BB}" "${a}" "${BB_HOST}" "${a}" > "${K}/kshim/${a}"; chmod +x "${K}/kshim/${a}"; done
    KBB=(--ro-bind "${BB_HOST}" "${BB}")
fi
printf 'export PATH=/kshim:/shim:/usr/bin:/bin\nexport OS_NAME=ROCKNIX\n' > "${K}/profile"
btk() { # <verb...>; as bt, with /usr/config ours and the image's tar and unzip
    RC=$( ( setsid -w bwrap --die-with-parent --tmpfs / "${UB[@]}" --ro-bind "${KU}" /usr/config "${KBB[@]}" \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${K}/profile" /etc/profile \
        --bind "${KS}" /storage --ro-bind "${B}/shim" /shim --ro-bind "${K}/kshim" /kshim --ro-bind "${B}/repo" /repo \
        --dev /dev --proc /proc --tmpfs /tmp \
        bash /repo/backuptool "$@" > "${OUT}" 2>&1; echo $? ) 2>/dev/null )
}
OUT="${K}/out"
btk backup; rck1=${RC}
karch=$(ls "${KS}/roms/backup"/*.tar.gz 2>/dev/null)
[ "${rck1}" -eq 0 ] && [ -n "${karch}" ]; check $? "a backup writes (rc ${rck1})" "rc ${rck1}: $(tail -3 "${OUT}" | tr '\n' '|')"
klist=$(tar -tzf "${karch}" 2>/dev/null)
echo "${klist}" | grep -q 'ppsspp/PSP/SYSTEM/ppsspp.ini$' && echo "${klist}" | grep -q 'test/own$'; check $? "the edited ini and the player's own file travel" "archive lists: $(echo "${klist}" | tr '\n' ' ')"
! echo "${klist}" | grep -q -E 'cheat.db$|test/seed$'; check $? "shipped seeds identical to /usr/config do not (cheat.db, test/seed)" "a shipped seed is in the archive: $(echo "${klist}" | grep -E 'cheat.db$|test/seed$' | tr '\n' ' ')"
! echo "${klist}" | grep -q -E 'ppsspp/assets/|SYSTEM/CACHE/'; check $? "assets and the shader cache never do, edited or not" "the archive carries: $(echo "${klist}" | grep -E 'ppsspp/assets/|SYSTEM/CACHE/' | tr '\n' ' ')"
grep -q 'left out 2 file(s) identical' "${OUT}"; check $? "and the log says two were left out as the image's own" "log: $(grep 'left out' "${OUT}" | head -1)"
! echo "${klist}" | grep -q -E 'ppsspp_retroachievements.dat$|dolphin-emu/RetroAchievements.ini$|SkyEmu/ra_token.txt$|ARMSX2/inis/secrets.ini$|gopher64/retroachievements.json$'; check $? "the five files that hold only a RetroAchievements token are held back (PPSSPP's .dat, Dolphin's, SkyEmu's, ARMSX2's; #169)" "the archive carries: $(echo "${klist}" | grep -E 'ppsspp_retroachievements.dat$|RetroAchievements.ini$|ra_token.txt$|secrets.ini$' | tr '\n' ' ')"
KX="${K}/extract"; rm -rf "${KX}"; mkdir -p "${KX}"; tar -xzf "${karch}" -C "${KX}" 2>/dev/null
echo "${klist}" | grep -q 'duckstation/settings.ini$' && echo "${klist}" | grep -q 'melonDS/melonDS.ini$' && echo "${klist}" | grep -q 'flycast/emu.cfg$' && echo "${klist}" | grep -q 'aethersx2/inis/PCSX2.ini$' \
    && grep -qx 'Token = ' "${KX}/storage/.config/duckstation/settings.ini" && grep -qx 'Username = qa' "${KX}/storage/.config/duckstation/settings.ini" && grep -qx 'LoginTimestamp = 1' "${KX}/storage/.config/duckstation/settings.ini" \
    && grep -qx 'RA_Token=' "${KX}/storage/.config/melonDS/melonDS.ini" && grep -qx 'RA_Password=' "${KX}/storage/.config/melonDS/melonDS.ini" && grep -qx 'RA_Username=qa' "${KX}/storage/.config/melonDS/melonDS.ini" \
    && grep -qx 'Token = ' "${KX}/storage/.config/flycast/emu.cfg" && grep -qx 'Token = ' "${KX}/storage/.config/aethersx2/inis/PCSX2.ini"; check $? "the four settings files with a token line travel with the value blanked and every other line kept (DuckStation, melonDS, flycast, AetherSX2)" "duckstation: $(tr '\n' '|' < "${KX}/storage/.config/duckstation/settings.ini" 2>/dev/null) melonDS: $(tr '\n' '|' < "${KX}/storage/.config/melonDS/melonDS.ini" 2>/dev/null) flycast: $(tr '\n' '|' < "${KX}/storage/.config/flycast/emu.cfg" 2>/dev/null) aethersx2: $(tr '\n' '|' < "${KX}/storage/.config/aethersx2/inis/PCSX2.ini" 2>/dev/null)"
! grep -rqF "${KTOK}" "${KX}" 2>/dev/null; check $? "and the planted token appears in no member of the archive" "the token is in: $(grep -rlF "${KTOK}" "${KX}" 2>/dev/null | sed "s|${KX}/||" | tr '\n' ' ')"
grep -q 'held back 5 file(s) that hold only a RetroAchievements token' "${OUT}" && grep -q 'blanked the RetroAchievements token in 4 emulator settings file(s)' "${OUT}"; check $? "and the log counts five held back and four blanked" "log: $(grep -oE '(held back|blanked)[^|]*' "${OUT}" | tr '\n' ' ')"
! echo "${klist}" | grep -q 'storage/.config/raofflineproxy/'; check $? "the offline RetroAchievements proxy's folder travels in no shape: none of its five files is in the archive (#165)" "the archive carries: $(echo "${klist}" | grep 'raofflineproxy/' | tr '\n' ' ')"
grep -q "held back 5 file(s) under the offline RetroAchievements proxy's folder" "${OUT}"; check $? "and the log counts the five held back under it" "log: $(grep -o "held back [0-9]* file(s) under the offline[^|]*" "${OUT}" | head -1 | grep . || echo silent)"
# A Token = line in a file the strip does not know, with a value of its own.
# Since #307 PL-005 the scanner's hit ends the backup before the archive is
# named, so it is planted for a second run: that run is refused, the log
# counts the one line, and the first archive stays the only one.
printf '[Other]\nToken = %s\n' "${KTOK2}" > "${KS}/.config/test/unknown.ini"
btk backup; rck1b=${RC}
[ "${rck1b}" -ne 0 ] && grep -q '^>>> why A SIGN-IN WAS FOUND IN THE BACKUP' "${OUT}" && grep -q 'found 1 line(s) that look like a password or key, in: storage/.config/test/unknown.ini$' "${OUT}" && [ "$(ls "${KS}/roms/backup"/*.tar.gz)" = "${karch}" ]; check $? "the scanner sees a Token = line in a file the strip does not know (test/unknown.ini), and only that one: the backup ends there (#307 PL-005)" "rc ${rck1b}; scanner: $(grep -oE 'found [0-9]+ line[^|]*' "${OUT}" | head -1 | grep . || echo silent); archives: $(ls "${KS}/roms/backup"/*.tar.gz 2>/dev/null | wc -l) -- until #169 its anchor was lower-case only, and the emulators' keys are capitalised"
rm -f "${KS}/.config/test/unknown.ini"
# An archive from before #45: assets, cache, an ini and the player's file,
# all older. Restoring it must put back the ini and the file and leave the
# newer image's assets and cache alone.
rm -f "${KS}/roms/backup"/*.tar.gz
KO="${K}/old"; mkdir -p "${KO}/storage/.config/ppsspp/assets/lang" "${KO}/storage/.config/ppsspp/PSP/SYSTEM/CACHE" "${KO}/storage/.config/test"
echo "OLD strings" > "${KO}/storage/.config/ppsspp/assets/lang/en_US.ini"; echo "OLD cache" > "${KO}/storage/.config/ppsspp/PSP/SYSTEM/CACHE/x.cache"
echo "OLD ini" > "${KO}/storage/.config/ppsspp/PSP/SYSTEM/ppsspp.ini"; echo "OLD own" > "${KO}/storage/.config/test/own"
echo "OLD TOKEN" > "${KO}/storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat"  # every archive written before #169 has one
mkdir -p "${KO}/storage/.config/raofflineproxy"; echo "OLD QUEUE" > "${KO}/storage/.config/raofflineproxy/proxy.sqlite3"  # a custom-LOCATIONS archive from before #165
tar -C "${KO}" -czf "${KS}/roms/backup/20260101000000-ROCKNIX_SETTINGS.tar.gz" storage
btk restore; rck2=${RC}
[ "${rck2}" -eq 0 ]; check $? "a pre-#45 archive restores (rc ${rck2})" "rc ${rck2}: $(grep -v '^logger' "${OUT}" | tail -3 | tr '\n' '|')"
[ "$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp.ini")" = "OLD ini" ] && [ "$(cat "${KS}/.config/test/own")" = "OLD own" ]; check $? "the ini and the player's file come back from it" "ini='$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp.ini")' own='$(cat "${KS}/.config/test/own")'"
[ "$(cat "${KS}/.config/ppsspp/assets/lang/en_US.ini")" = "edited strings" ] && [ "$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/CACHE/x.cache")" = "shader cache" ]; check $? "its assets and cache are left where they were" "asset='$(cat "${KS}/.config/ppsspp/assets/lang/en_US.ini")' cache='$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/CACHE/x.cache")' -- an older emulator's program data was put under a newer one"
[ "$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat" 2>/dev/null)" = "${KTOK}" ]; check $? "its token file is not put back over the device's own (tar, #169)" "the .dat now reads '$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat" 2>/dev/null)' -- a token from before landed on this device"
! grep -q 'OLD QUEUE' "${KS}/.config/raofflineproxy/proxy.sqlite3" 2>/dev/null; check $? "the proxy's queue from the archive is not put over this device's own (tar, #165)" "proxy.sqlite3 now holds the archive's copy -- another device's award queue landed here"
ksnap=$(ls "${KS}/roms/backup/archive/"*PRE_RESTORE*.tar.gz 2>/dev/null | head -1)
[ -n "${ksnap}" ] && tar -xzOf "${ksnap}" storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat 2>/dev/null | grep -qF "${KTOK}"; check $? "while the copy kept before the restore still carries the device's own token (STRIP=0: it never leaves the device, and 'as they were' means exactly that)" "snapshot: ${ksnap:-none}; .dat in it: $(tar -xzOf "${ksnap}" storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat 2>/dev/null || echo absent)"
# The same archive as a zip: the shape every backup had before 2026-08-26,
# so the one most likely to carry assets whole -- and the zip branch skipped
# only live symlinks, so D-CLOUD-008's "from any archive" was tar-only until
# #151 PL-03 (D-CLOUD-124). A regular-file copy of a symlink the OS provides
# is in the fixture too, so the branch is seen to keep its original job.
rm -f "${KS}/roms/backup"/*.tar.gz
echo "edited strings" > "${KS}/.config/ppsspp/assets/lang/en_US.ini"; echo "shader cache" > "${KS}/.config/ppsspp/PSP/SYSTEM/CACHE/x.cache"
echo "the player's ini" > "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp.ini"; echo "the player's own" > "${KS}/.config/test/own"
rm -f "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat"  # so the zip's copy landing is simply its existence
rm -f "${KS}/.config/raofflineproxy/proxy.sqlite3"
ln -sfn /usr/config/test/seed "${KS}/.config/test/link"
echo "OLD link contents" > "${KO}/storage/.config/test/link"
(cd "${KO}" && python3 -c 'import zipfile, os, sys
z = zipfile.ZipFile(sys.argv[1], "w", zipfile.ZIP_DEFLATED)
for r, _, fs in os.walk("storage"):
    for f in fs: z.write(os.path.join(r, f))
z.close()' "${KS}/roms/backup/20260101000000-ROCKNIX_BACKUP.zip")
btk restore; rck3=${RC}
[ "${rck3}" -eq 0 ]; check $? "a pre-#45 zip archive restores (rc ${rck3})" "rc ${rck3}: $(grep -v '^logger' "${OUT}" | tail -3 | tr '\n' '|')"
[ "$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp.ini")" = "OLD ini" ] && [ "$(cat "${KS}/.config/test/own")" = "OLD own" ]; check $? "the ini and the player's file come back from the zip" "ini='$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp.ini")' own='$(cat "${KS}/.config/test/own")'"
[ "$(cat "${KS}/.config/ppsspp/assets/lang/en_US.ini")" = "edited strings" ] && [ "$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/CACHE/x.cache")" = "shader cache" ]; check $? "its assets and cache are left where they were (zip)" "asset='$(cat "${KS}/.config/ppsspp/assets/lang/en_US.ini")' cache='$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/CACHE/x.cache")' -- the zip branch skipped only symlinks, and the oldest archives put an older emulator's program data under a newer one (#151 PL-03)"
[ ! -e "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat" ]; check $? "its token file is not put back from a zip either (#169; the image's unzip -x on an exact member name)" "the .dat landed from the zip: '$(cat "${KS}/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat" 2>/dev/null)'"
! grep -q 'OLD QUEUE' "${KS}/.config/raofflineproxy/proxy.sqlite3" 2>/dev/null; check $? "nor is the proxy's queue (zip, #165)" "proxy.sqlite3 now holds the zip's copy"
[ -L "${KS}/.config/test/link" ] && grep -q 'KEEPING 1 FILE(S) THE SYSTEM PROVIDES' "${OUT}"; check $? "and the symlink the OS provides is still a symlink, said on the screen (KEEPING 1 FILE(S))" "link: $([ -L "${KS}/.config/test/link" ] && echo symlink || echo "regular file: $(cat "${KS}/.config/test/link" 2>/dev/null)"); screen: $(grep -c 'KEEPING' "${OUT}") KEEPING line(s)"
# The prune's grep dying part-way (exit 2, as a read error would): a pruned
# list from a grep that did not finish is a partial backup announced as a
# success. The shim writes one line of the list and dies; every other grep
# in the script is the real one (#151 PL-14: `|| true` took what was there).
cat > "${K}/kshim/grep" <<'EOS'
#!/bin/bash
for a in "$@"; do [ "$a" = -f ] && { head -1 "${@: -1}"; echo "grep: read error" >&2; exit 2; }; done
exec /usr/bin/grep "$@"
EOS
chmod +x "${K}/kshim/grep"
rm -f "${KS}/roms/backup"/*.tar.gz "${KS}/roms/backup"/*.zip
btk backup; rck4=${RC}
[ "${rck4}" -ne 0 ] && [ -z "$(ls "${KS}/roms/backup"/*.tar.gz 2>/dev/null)" ] && grep -q 'could not be filtered' "${OUT}"; check $? "a backup whose list filter dies part-way (grep exit 2) writes nothing and says why in the log" "rc ${rck4}; archives written: $(ls "${KS}/roms/backup"/*.tar.gz 2>/dev/null | wc -l); log: $(grep -o 'could not be filtered[^|]*' "${OUT}" | head -1) -- one line of the list became a backup announced as a success (#151 PL-14)"
rm -f "${K}/kshim/grep"


printf 'RESULT failures=%s\n' "$FAIL"
exit "$FAIL"

#!/bin/bash
set -u
ROOT=/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders
RCLONE_REL=projects/ROCKNIX/packages/network/rclone/sources
OLD=${OLD:-0}; BASE_REF=${BASE_REF:-3268015c}
TMP=${FOCUSED_ROOT:?}; mkdir -p "$TMP"
unset TMPDIR
FAIL=0
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

printf 'actual_BB_HOST=%s\n' "$BB_HOST"
"$BB_HOST" 2>&1 | head -1
echo "  A. audit #307/#308, stream A: the cloud scripts against the image's rclone"
SA="${TMP}/sa"; mkdir -p "${SA}/shim" "${SA}/nbin"
SA_RCLONE_SRC=$(image_tool_source rclone version) || exit 2
if [ -z "${SA_RCLONE_SRC}" ] || ! cp "${SA_RCLONE_SRC}" "${SA}/rclone.real"; then
    echo "    FAIL  no rclone to run the stream A cases against (none in a build root, none on the host)"; FAIL=$((FAIL + 1))
    : > "${SA}/rclone.real"
fi
chmod +x "${SA}/rclone.real" 2>/dev/null
echo "    rclone: $("${SA}/rclone.real" version 2>/dev/null | head -1) -- a copy of ${SA_RCLONE_SRC:-nothing}"
cat > "${SA}/shim/rclone" <<'EOR'
#!/bin/bash
# The image's rclone, with the calls /ctl/fail names ("<ERE><tab><exit>")
# failed instead; /ctl/kill ("<ERE><tab><n>") kills the caller's whole
# process group at the n-th matching call, before it runs -- a kill, not a
# failure; /ctl/post ("<ERE><tab><command>") runs a command after a
# matching call -- another
# writer landing between two steps; /ctl/nohash makes `backend features`
# describe a remote with no hashes (WebDAV, SFTP, SMB, FTP).
printf '%s\n' "$*" >> /ctl/argv
# A successful provider-features fixture must contain a valid answer.
if [ "$1" = backend ] && [ "$2" = features ] && [ -s /ctl/provider-features ]; then
    cat /ctl/provider-features; exit 0
fi
if [ -s /ctl/fail ]; then
    while IFS=$'\t' read -r pat code; do
        [ -n "${pat}" ] || continue
        if printf '%s' "$*" | grep -qE -- "${pat}"; then
            printf '%s\n' "$*" >> /ctl/fault-fired
            echo "ERROR : injected failure ${code}" >&2
            exit "${code}"
        fi
    done < /ctl/fail
fi
if [ -s /ctl/kill ]; then
    while IFS=$'\t' read -r pat nth; do
        [ -n "${pat}" ] || continue
        printf '%s' "$*" | grep -qE -- "${pat}" || continue
        n=$(( $(cat /ctl/kill.count 2>/dev/null || echo 0) + 1 )); echo "${n}" > /ctl/kill.count
        [ "${n}" -eq "${nth}" ] && kill -9 -- "-$(cut -d' ' -f5 /proc/self/stat)"
    done < /ctl/kill
fi
if [ -s /ctl/hang ]; then
    # /ctl/hang ("<ERE><tab><seconds>"): a call that sits silent, as a cloud
    # that accepts and never answers leaves it -- one process, so whatever
    # bound ends the call ends it.
    while IFS=$'\t' read -r pat secs; do
        [ -n "${pat}" ] || continue
        printf '%s' "$*" | grep -qE -- "${pat}" && exec sleep "${secs}"
    done < /ctl/hang
fi
if [ -e /ctl/nohash ] && [ "$1" = backend ] && [ "$2" = features ]; then
    printf '{\n\t"Name": "qa",\n\t"Hashes": [],\n\t"Features": {\n\t\t"BucketBased": false\n\t}\n}\n'
    exit 0
fi
if [ -s /ctl/post ]; then
    /sa/rclone.real "$@"; rc=$?
    while IFS=$'\t' read -r pat cmd; do
        [ -n "${pat}" ] || continue
        printf '%s' "$*" | grep -qE -- "${pat}" && eval "${cmd}"
    done < /ctl/post
    exit "${rc}"
fi
exec /sa/rclone.real "$@"
EOR
printf '#!/bin/sh\ncase "$*" in *"route show default"*) [ -e /ctl/noroute ] || echo "default via 10.0.2.2 dev eth0" ;; esac\n' > "${SA}/shim/ip"
printf '#!/bin/sh\n[ -e /ctl/noping ] && exit 1\nexit 0\n' > "${SA}/shim/ping"
printf '#!/bin/sh\nexit 0\n' > "${SA}/shim/logger"
printf '#!/bin/sh\nexit 0\n' > "${SA}/shim/systemd-tmpfiles"
chmod +x "${SA}/shim"/*
printf 'export PATH=/shim:/nbin:/usr/bin:/bin\nexport HOME=/storage\n' > "${SA}/profile"
SA_BB=()
if [ -n "${BB}" ]; then
    # Every applet the image's /usr/bin links to busybox that these scripts
    # call -- cp, mv, rm and the rest joined the list after the audit of the
    # fixes (gpt coverage note 3: the sandbox ran the host's cp and mv).
    # grep, sort and timeout are real binaries on the image, and the host's
    # stand in for them.
    for a in sed tr head wc cut awk tail tee mkfifo sleep flock stat md5sum find cmp mktemp unzip tar \
             cp mv rm mkdir cat date ls readlink uniq basename dirname touch chmod ln xargs; do
        printf '#!/bin/sh\n[ -x %s ] && exec %s %s "$@"\nexec %s %s "$@"\n' "${BB}" "${BB}" "${a}" "${BB_HOST}" "${a}" > "${SA}/nbin/${a}"
        chmod +x "${SA}/nbin/${a}"
    done
    SA_BB=(--ro-bind "${BB_HOST}" "${BB}")
fi
# /usr as a tmpfs of the host's directories, for a case that needs /usr/config
# to be the fixture's (the helper reads its defaults there).
SA_USR=(); for u in bin sbin lib lib64 libexec share; do [ -e "/usr/${u}" ] && SA_USR+=(--ro-bind "/usr/${u}" "/usr/${u}"); done
sa_new() { # <name>: a fresh fixture directory; its path on stdout
    local d="${SA}/f-$1"
    rm -rf "${d}"; mkdir -p "${d}"/storage/.config/rclone "${d}"/storage/.cache/cloud_sync "${d}"/storage/roms \
        "${d}"/cloud "${d}"/ctl "${d}"/log "${d}"/varrun "${d}"/repo
    printf '[qa]\ntype = alias\nremote = /cloud\n' > "${d}/storage/.config/rclone/rclone.conf"
    : > "${d}/ctl/argv"; : > "${d}/ctl/fail"; : > "${d}/ctl/kill"; : > "${d}/ctl/post"; : > "${d}/ctl/hang"
    printf '#!/bin/sh\ncase "$1" in --label) echo QA ;; --previous|--legacy) ;; *) echo QA-deadbeef01 ;; esac\n' > "${d}/repo/cloud_device_id"
    chmod +x "${d}/repo/cloud_device_id"
    printf '%s' "${d}"
}
sa_script() { # <fixture> <script...>: the scripts under test into its /repo (working tree, or BASE_REF under --old)
    local d="$1" s; shift
    for s in "$@"; do src_of "${RCLONE_REL}/${s}" "${d}/repo/${s}"; chmod +x "${d}/repo/${s}"; done
}
# SA_EXTRA: more bwrap arguments for the next runs, after /usr -- a file
# the image ships under /usr/bin, overlaid for a case (A47); empty otherwise.
SA_EXTRA=()
sa_run() { # <fixture> <script> [args...]: the script whole, in the sandbox; stdout+stderr to ${d}/out, rc in RC, seconds in DT
    local d="$1" s="$2" t0; shift 2
    t0=$(date +%s)
    RC=$( ( cd "${d}/storage" && setsid -w timeout 180 bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr ${SA_EXTRA[@]+"${SA_EXTRA[@]}"} "${SA_BB[@]}" \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${SA}/profile" /etc/profile \
        --bind "${d}/storage" /storage --bind "${d}/cloud" /cloud --bind "${d}/ctl" /ctl \
        --ro-bind "${SA}/shim" /shim --ro-bind "${SA}/nbin" /nbin --ro-bind "${SA}/rclone.real" /sa/rclone.real \
        --ro-bind "${d}/repo" /repo --bind "${d}/log" /var/log --bind "${d}/varrun" /var/run \
        --dev /dev --proc /proc --tmpfs /tmp --chdir "${SA_CWD:-/storage}" \
        --setenv PATH "/shim:/nbin:/usr/bin:/bin" --setenv HOME /storage \
        bash "/repo/${s}" "$@" > "${d}/out" 2>&1; echo $? ) 2>/dev/null )
    DT=$(( $(date +%s) - t0 ))
}
sa_tail() { sed 's/\x1b\[[0-9;]*m//g' "$1/out" | grep -v '^\s*$' | tail -${2:-4} | tr '\n' '|' | cut -c1-240; }
# The run's own outcome line, as case n reads it: colour off, no protocol
# marker, no rclone stats, no rule of dashes.
sa_outcome() {
    sed 's/\x1b\[[0-9;]*[A-Za-z]//g' "$1/out" | tr '\r' '\n' | grep -vE '^>>> |^(Transferred:|Checks:|Elapsed time:|Errors:|Deleted:|Renamed:|Transferring:|Checking:)|^[[:space:]]*\*[[:space:]]|^[=-]{4,}$|^[[:space:]]*$' | tail -1
}

# A1. PL-001 (#307, F-CS-01 both seats + F-CS-03 gpt): --match --apply acts
#     only on the plan the preview showed. A system whose listing fails is
#     neither planned nor removed; the preview writes its per-system plan and
#     apply reads it -- a system whose verb changed, or with more to remove
#     than the preview counted, or no plan at all, is refused, and
#     --max-delete is the preview's count.
echo "    A0. #352: the pre-tier rows list only folders this device has or systems it supports; --content-location names the folder that holds the games"
M0=$(sa_new pl352); sa_script "${M0}" cloud_content_restore; sa_script "${M0}" cloud_setup
# The selected source contract, not the --old switch, chooses the assertions.
SA_SCOPED=0
grep -q -- '--validate-folders)' "${M0}/repo/cloud_setup" && SA_SCOPED=1
if [ "${SA_SCOPED}" -eq 0 ]; then
printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="/pixelelated/Saves"\nSETTINGS_REMOTE="/pixelelated/Backups"\nCONTENT_REMOTE=""\n' > "${M0}/storage/.config/cloud_sync.conf"
rm -rf "${M0}/cloud" "${M0}/storage/roms"/*; mkdir -p "${M0}/cloud/Photos" "${M0}/cloud/Documents" "${M0}/cloud/gb" "${M0}/storage/roms/gb"
echo jpg > "${M0}/cloud/Photos/holiday.jpg"; echo txt > "${M0}/cloud/Documents/notes.txt"; echo a > "${M0}/cloud/gb/A.gb"
printf 'gb\n' > "${M0}/storage/.cache/cloud_sync/content-systems"; : > "${M0}/ctl/fail"; : > "${M0}/ctl/argv"
sa_run "${M0}" cloud_content_restore --scan
grep -q '^gb|' "${M0}/out" && ! grep -q '^Photos|' "${M0}/out" && ! grep -q '^Documents|' "${M0}/out" && [ "${RC}" -eq 0 ]; check $? "#352: with the content root at the cloud's root, the scan lists gb (a folder this device has) and neither Photos nor Documents (rc ${RC})" "rc ${RC}; out: $(sa_tail "${M0}")"
rm -rf "${M0}/cloud"/*; mkdir -p "${M0}/cloud/pixelelated/Content/ROMs/gb" "${M0}/cloud/Photos"; echo a > "${M0}/cloud/pixelelated/Content/ROMs/gb/A.gb"; echo jpg > "${M0}/cloud/Photos/x.jpg"
sa_run "${M0}" cloud_setup --content-location
grep -qx 'FOUND=/pixelelated/Content' "${M0}/out" && grep -qx 'STATE=found-elsewhere' "${M0}/out"; check $? "#352: with nothing of ours at the configured root, --content-location names /pixelelated/Content, where the ROMs folder is, and reads found-elsewhere" "rc ${RC}; out: $(sa_tail "${M0}")"
printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="/pixelelated/Saves"\nSETTINGS_REMOTE="/pixelelated/Backups"\nCONTENT_REMOTE="/pixelelated/Content"\n' > "${M0}/storage/.config/cloud_sync.conf"
sa_run "${M0}" cloud_setup --content-location
grep -qx 'FOUND=' "${M0}/out" && grep -qx 'STATE=ok' "${M0}/out"; check $? "and with the root configured where the games are, FOUND is empty and the state ok" "rc ${RC}; out: $(sa_tail "${M0}")"
# #471 PL-001/#467: membership is the scanner's, even on an empty device.
mkdir -p "${M0}/storage/.config/emulationstation"
printf '<systemList><system><name>Game Boy</name><path>/storage/roms/gb</path></system></systemList>\n' > "${M0}/storage/.config/emulationstation/es_systems.cfg"
rm -rf "${M0}/storage/roms"/* "${M0}/cloud"/*
printf 'SAVES_REMOTE="/pixelelated/Saves"\nCONTENT_REMOTE="/Mine"\n' > "${M0}/storage/.config/cloud_sync.conf"
mkdir -p "${M0}/cloud/Mine/Photos"; echo photo > "${M0}/cloud/Mine/Photos/x.jpg"
sa_run "${M0}" cloud_setup --content-location
[ "${RC}" -eq 0 ] && grep -qx STATE=empty "${M0}/out"; check $? "#467: unrelated configured folders do not count as games" "rc ${RC}; $(sa_tail "${M0}")"
mkdir -p "${M0}/cloud/pixelelated/Content/ROMs/gb"; echo game > "${M0}/cloud/pixelelated/Content/ROMs/gb/A.gb"
sa_run "${M0}" cloud_setup --content-location
[ "${RC}" -eq 0 ] && grep -qx STATE=found-elsewhere "${M0}/out" && grep -qx FOUND=/pixelelated/Content "${M0}/out"; check $? "#467: unrelated configured folders do not hide the usable fallback" "rc ${RC}; $(sa_tail "${M0}")"
rm -rf "${M0}/cloud"/*
mkdir -p "${M0}/cloud/ROMs/gb"; echo game > "${M0}/cloud/ROMs/gb/A.gb"
sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE=""|' "${M0}/storage/.config/cloud_sync.conf"
sa_run "${M0}" cloud_setup --content-location
[ "${RC}" -eq 0 ] && grep -qx STATE=ok "${M0}/out"; check $? "#467: explicit account root recognizes tiered games on an empty device" "rc ${RC}; $(sa_tail "${M0}")"
rm -rf "${M0}/cloud"/*; mkdir -p "${M0}/cloud/gb"; echo game > "${M0}/cloud/gb/A.gb"
sa_run "${M0}" cloud_setup --content-location
[ "${RC}" -eq 0 ] && grep -qx STATE=ok "${M0}/out"; check $? "#467: installed ES paths recognize flat games without a local directory" "rc ${RC}; $(sa_tail "${M0}")"
sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE="/Mine"|' "${M0}/storage/.config/cloud_sync.conf"
sa_run "${M0}" cloud_setup --content-location
[ "${RC}" -eq 0 ] && grep -qx STATE=stranded-at-root "${M0}/out" && grep -qx FOUND=/ "${M0}/out"; check $? "#467: legacy root discovery supplies the reachable root selection" "rc ${RC}; $(sa_tail "${M0}")"
sa_run "${M0}" cloud_setup --use-content-root
[ "${RC}" -eq 0 ]; check $? "#467: the root selection persists" "rc ${RC}; $(sa_tail "${M0}")"
sa_run "${M0}" cloud_content_restore --scan
[ "${RC}" -eq 0 ] && grep -q '^gb|5|' "${M0}/out"; check $? "#467: the next content scan actually sees the legacy-root game's bytes" "rc ${RC}; $(sa_tail "${M0}")"
cp "${M0}/storage/.config/cloud_sync.conf" "${M0}/conf-before"
printf '%s\t%s\n' '^lsf ' 5 > "${M0}/ctl/fail"
sa_run "${M0}" cloud_setup --content-location
[ "${RC}" -ne 0 ] && grep -qx STATE=unreadable "${M0}/out" && cmp -s "${M0}/conf-before" "${M0}/storage/.config/cloud_sync.conf"; check $? "#467: a refused listing stays unreadable and preserves the selection" "rc ${RC}; $(sa_tail "${M0}")"
: > "${M0}/ctl/fail"
else
    printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="/pixelelated/Saves"\nSETTINGS_REMOTE="/pixelelated/Backups"\nCONTENT_REMOTE=""\n' > "${M0}/storage/.config/cloud_sync.conf"
    mkdir -p "${M0}/cloud/Photos" "${M0}/cloud/gb" "${M0}/storage/roms/gb"
    echo photo > "${M0}/cloud/Photos/x.jpg"; echo game > "${M0}/cloud/gb/A.gb"
    printf 'gb\n' > "${M0}/storage/.cache/cloud_sync/content-systems"
    sa_run "${M0}" cloud_content_restore --scan
    [ "${RC}" -eq 0 ] && ! grep -qE '^(gb|Photos)\|' "${M0}/out" && [ ! -f "${M0}/storage/roms/gb/A.gb" ]
    check $? "flat folders are not scanned or restored as a selected structured library" "rc ${RC}; $(sa_tail "${M0}")"
    sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE="/Mine"|' "${M0}/storage/.config/cloud_sync.conf"
    mkdir -p "${M0}/cloud/Mine/Photos" "${M0}/cloud/pixelelated/Content/ROMs/gb"
    echo game > "${M0}/cloud/pixelelated/Content/ROMs/gb/A.gb"
    cp "${M0}/storage/.config/cloud_sync.conf" "${M0}/conf-before"; : > "${M0}/ctl/argv"
    sa_run "${M0}" cloud_setup --content-location
    [ "${RC}" -eq 0 ] && grep -qx STATE=empty "${M0}/out" && grep -qx FOUND= "${M0}/out" \
        && cmp -s "${M0}/conf-before" "${M0}/storage/.config/cloud_sync.conf" \
        && ! grep -qE '^lsjson qa:(/)? |^lsjson qa:/pixelelated/' "${M0}/ctl/argv"
    check $? "selected empty library neither discovers another library nor changes the choice" "rc ${RC}; $(sa_tail "${M0}"); calls $(cat "${M0}/ctl/argv")"
    sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE="/pixelelated/Content"|' "${M0}/storage/.config/cloud_sync.conf"
    sa_run "${M0}" cloud_setup --content-location
    [ "${RC}" -eq 0 ] && grep -qx STATE=ok "${M0}/out" && grep -qx FOUND= "${M0}/out"
    check $? "explicitly choosing the populated structured library recognizes its games" "rc ${RC}; $(sa_tail "${M0}")"
    mkdir -p "${M0}/storage/.config/emulationstation"
    printf '<systemList><system><name>Game Boy</name><path>/storage/roms/gb</path></system></systemList>\n' > "${M0}/storage/.config/emulationstation/es_systems.cfg"
    rm -rf "${M0}/storage/roms"/* "${M0}/cloud"/*
    mkdir -p "${M0}/cloud/ROMs/gb"; echo game > "${M0}/cloud/ROMs/gb/A.gb"
    sa_run "${M0}" cloud_setup --use-content-root
    [ "${RC}" -eq 0 ] && grep -qx 'CONTENT_REMOTE=""' "${M0}/storage/.config/cloud_sync.conf"
    check $? "explicit relative-root selection persists as an empty content pointer" "rc ${RC}; $(sa_tail "${M0}")"
    sa_run "${M0}" cloud_setup --content-location
    [ "${RC}" -eq 0 ] && grep -qx STATE=ok "${M0}/out"
    check $? "selected account root recognizes ROMs/system with installed ES membership" "rc ${RC}; $(sa_tail "${M0}")"
    sa_run "${M0}" cloud_content_restore --scan
    [ "${RC}" -eq 0 ] && grep -q '^gb|5|' "${M0}/out"
    check $? "the scan counts actual ROM bytes beneath the explicitly selected structured root" "rc ${RC}; $(sa_tail "${M0}")"
    cp "${M0}/storage/.config/cloud_sync.conf" "${M0}/conf-before"
    printf '%s\t%s\n' '^lsjson ' 5 > "${M0}/ctl/fail"; : > "${M0}/ctl/fault-fired"
    sa_run "${M0}" cloud_setup --content-location
    [ "${RC}" -ne 0 ] && grep -qx STATE=unreadable "${M0}/out" && ! grep -qx STATE=empty "${M0}/out" \
        && grep -q '^lsjson ' "${M0}/ctl/fault-fired" \
        && cmp -s "${M0}/conf-before" "${M0}/storage/.config/cloud_sync.conf"
    check $? "an actual failed metadata listing stays unreadable and preserves the selected root" "fault $(cat "${M0}/ctl/fault-fired"); rc ${RC}; $(sa_tail "${M0}")"
    : > "${M0}/ctl/fail"
fi
RH=$(sa_new pl020h); sa_script "${RH}" cloud_sync_helper
mkdir -p "${RH}/usrconfig"; src_of "${RCLONE_REL}/cloud_sync-rules.txt.defaults" "${RH}/usrconfig/cloud_sync-rules.txt.defaults"
src_of "${RCLONE_REL}/cloud_sync.conf.defaults" "${RH}/usrconfig/cloud_sync.conf.defaults"
cat > "${RH}/repo/cat" <<'EOR'
#!/bin/bash
# The defaults cut short: a write that fails part-way, as on a full card.
if [ -e /ctl/cutcat ] && [ "$1" = /usr/config/cloud_sync-rules.txt.defaults ]; then head -n 20 "$1"; exit 1; fi
exec /usr/bin/cat "$@"
EOR
chmod +x "${RH}/repo/cat"
rh_run() { # the helper, with /usr/config the fixture's and the cutting cat first on PATH
    : > "${RH}/out"
    RC=$( ( setsid -w bwrap --die-with-parent --tmpfs / --tmpfs /usr "${SA_USR[@]}" "${SA_BB[@]}" \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${RH}/usrconfig" /usr/config \
        --bind "${RH}/storage" /storage --ro-bind "${RH}/repo" /repo --bind "${RH}/ctl" /ctl --ro-bind "${SA}/nbin" /nbin \
        --dev /dev --proc /proc --tmpfs /tmp --tmpfs /var \
        --setenv PATH "/repo:/nbin:/usr/bin:/bin" \
        bash /repo/cloud_sync_helper /ctl/helper.log > "${RH}/out" 2>&1; echo $? ) 2>/dev/null )
    cat "${RH}/ctl/helper.log" >> "${RH}/out" 2>/dev/null; rm -f "${RH}/ctl/helper.log"
}
echo "    A14. PL-015 (script half): no content folder derived inside a top-level saves folder"
if [ "${SA_SCOPED}" -eq 0 ]; then
printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="/GAMES"\nBACKUPMETHOD="copy"\n' > "${RH}/storage/.config/cloud_sync.conf"
rh_run
ccr=$(sed -n 's/^CONTENT_REMOTE=//p' "${RH}/storage/.config/cloud_sync.conf" | head -1)
grep -q 'Checking cloud sync configuration' "${RH}/out" && [ "${ccr}" != '"/GAMES/Content"' ] && grep -qi 'top level' "${RH}/out"; check $? "an upgraded /GAMES config gains no CONTENT_REMOTE inside the saves folder (${ccr:-no line}), and the log says why" "CONTENT_REMOTE=${ccr:-(none)}; log: $(grep -i content "${RH}/out" | tail -2 | tr '\n' '|') -- dirname /GAMES is /, and the helper then derived the folder's own Content"
printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="/Custom/Saves"\nBACKUPMETHOD="copy"\n' > "${RH}/storage/.config/cloud_sync.conf"
rh_run
[ "$(sed -n 's/^CONTENT_REMOTE=//p' "${RH}/storage/.config/cloud_sync.conf" | head -1)" = '"/Custom/Content"' ]; check $? "a deeper saves folder still gets its sibling (/Custom/Saves -> /Custom/Content)" "CONTENT_REMOTE=$(sed -n 's/^CONTENT_REMOTE=//p' "${RH}/storage/.config/cloud_sync.conf")"
else
    for chosen in /GAMES /Custom/Saves; do
        printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="%s"\nSETTINGS_REMOTE="/Chosen/Backups"\nBACKUPMETHOD="copy"\n' "${chosen}" > "${RH}/storage/.config/cloud_sync.conf"
        rh_run
        [ "${RC}" -eq 0 ] && grep -qx 'CONTENT_REMOTE="/pixelelated/Content"' "${RH}/storage/.config/cloud_sync.conf" \
            && grep -qxF "SAVES_REMOTE=\"${chosen}\"" "${RH}/storage/.config/cloud_sync.conf" \
            && grep -qx 'SETTINGS_REMOTE="/Chosen/Backups"' "${RH}/storage/.config/cloud_sync.conf"
        check $? "missing content choice uses the shipped default and preserves ${chosen} plus independent settings" "rc ${RC}; CONTENT_REMOTE=$(sed -n 's/^CONTENT_REMOTE=//p' "${RH}/storage/.config/cloud_sync.conf")"
    done
fi
printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE="/GAMES"\nCONTENT_REMOTE="/GAMES/Content"\nBACKUPMETHOD="copy"\n' > "${RH}/storage/.config/cloud_sync.conf"
rh_run
[ "$(sed -n 's/^CONTENT_REMOTE=//p' "${RH}/storage/.config/cloud_sync.conf" | head -1)" = '"/GAMES/Content"' ]; check $? "a /GAMES/Content an earlier build derived is left as it stands" "CONTENT_REMOTE was rewritten to $(sed -n 's/^CONTENT_REMOTE=//p' "${RH}/storage/.config/cloud_sync.conf")"
NW=$(sa_new pl015w); sa_script "${NW}" cloud_backup cloud_saves_root
cat > "${NW}/storage/.config/cloud_sync.conf" <<'EOS'
SAVESPATH="/storage/roms"
SAVES_REMOTE="/GAMES"
SETTINGS_BACKUPS="/storage/roms/backup"
SETTINGS_REMOTE="/Backups"
CONTENT_REMOTE="/GAMES/Content"
BACKUPMETHOD="copy"
BACKUPFILE_BACKUP_OPTION="no"
RCLONEOPTS="--progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt"
RCLONE_NET_OPTS="--contimeout 5s --timeout 10s --low-level-retries 2 --retries 1"
LOG_LEVEL="INFO"
EOS
printf -- '+ /**/*.srm\n- /**\n' > "${NW}/storage/.config/cloud_sync-rules.txt"
mkdir -p "${NW}/storage/roms/gb" "${NW}/cloud/GAMES"; echo s > "${NW}/storage/roms/gb/A.srm"
sa_run "${NW}" cloud_backup --yes --saves-only
grep -q 'CONTENT_REMOTE=/GAMES/Content is inside SAVES_REMOTE=/GAMES' "${NW}/log/cloud_sync.log" && grep -qi 'ROMs and BIOS folder in the cloud sits inside your saves folder' <(sed 's/\x1b\[[0-9;]*m//g' "${NW}/out"); check $? "cloud_backup warns about a ROMs and BIOS folder nested in the saves folder, in the log and on a deliberate run's screen (rc ${RC})" "log: $(grep -i 'inside' "${NW}/log/cloud_sync.log" | head -2 | tr '\n' '|') -- the warning covered the settings folder only, and only under a condition that can no longer hold"

echo "    A40. G-A-07 (gpt) / G-A-03 (claude): every listing --all stands on is read fail-closed"
AF=$(sa_new ga07); sa_script "${AF}" cloud_content_restore
mkdir -p "${AF}/storage/roms/nes" "${AF}/storage/.config/emulationstation" "${AF}/storage/.cache/cloud_sync"
printf '<system><path>/storage/roms/nes</path></system>\n' > "${AF}/storage/.config/emulationstation/es_systems.cfg"
af_run() { # <CONTENT_REMOTE> <where nes sits in the cloud> <the listing to fail>
    rm -rf "${AF}/cloud"/* "${AF}/storage/roms/nes"/* "${AF}/storage/.cache/cloud_sync/last-content-restore"
    printf 'SAVESPATH="/storage/roms"\nCONTENT_REMOTE="%s"\n' "$1" > "${AF}/storage/.config/cloud_sync.conf"
    mkdir -p "${AF}/cloud$2"; echo n > "${AF}/cloud$2/N.nes"
    printf '%s\t%s\n' "$3" 5 > "${AF}/ctl/fail"
    sa_run "${AF}" cloud_content_restore --all
}
if [ "${SA_SCOPED}" -eq 0 ]; then
af_run /pixelelated/Content /pixelelated/Content/nes '^lsf --dirs-only qa:/pixelelated/Content/ '
af_stamp=$(awk '{print $2}' "${AF}/storage/.cache/cloud_sync/last-content-restore" 2>/dev/null)
[ "${RC}" -ne 0 ] && [ "${af_stamp:-none}" != 0 ] && ! grep -q '^Nothing to restore' "${AF}/out" && grep -q '^>>> why ' "${AF}/out"; check $? "--all on the flat layout whose root listing fails (5) ends Couldn't finish, not Nothing to restore (rc ${RC}, stamp ${af_stamp:-none})" "rc ${RC}, stamp ${af_stamp:-none}; out: $(sa_tail "${AF}")"
af_run /pixelelated/Content /nes '^lsf --dirs-only qa: '
af_stamp=$(awk '{print $2}' "${AF}/storage/.cache/cloud_sync/last-content-restore" 2>/dev/null)
[ "${RC}" -ne 0 ] && [ "${af_stamp:-none}" != 0 ] && ! grep -q '^Nothing to restore' "${AF}/out"; check $? "--all whose legacy root listing fails (5) ends Couldn't finish too (rc ${RC}, stamp ${af_stamp:-none})" "rc ${RC}, stamp ${af_stamp:-none}; out: $(sa_tail "${AF}")"
af_run /pixelelated/Content /pixelelated/Content/nes '^never$'
[ "${RC}" -eq 0 ] && [ -f "${AF}/storage/roms/nes/N.nes" ]; check $? "and with nothing failing the flat layout's nes comes down (rc ${RC})" "rc ${RC}; out: $(sa_tail "${AF}")"
else
    for target in ROMs/ ''; do
        : > "${AF}/ctl/fault-fired"
        af_run /pixelelated/Content /pixelelated/Content/ROMs/nes "^lsf --dirs-only qa:/pixelelated/Content/${target} "
        af_stamp=$(awk '{print $2}' "${AF}/storage/.cache/cloud_sync/last-content-restore" 2>/dev/null)
        [ "${RC}" -ne 0 ] && [ "${af_stamp:-none}" != 0 ] && [ -s "${AF}/ctl/fault-fired" ] \
            && ! grep -q '^Nothing to restore' "${AF}/out" && grep -q '^>>> why ' "${AF}/out" \
            && [ ! -f "${AF}/storage/roms/nes/N.nes" ]
        check $? "failed selected ${target:-content-root} metadata stops before restoration and never stamps success" "fault $(cat "${AF}/ctl/fault-fired"); rc ${RC}, stamp ${af_stamp:-none}; $(sa_tail "${AF}")"
    done
    af_run /pixelelated/Content /pixelelated/Content/ROMs/nes '^never$'
    [ "${RC}" -eq 0 ] && [ -f "${AF}/storage/roms/nes/N.nes" ]
    check $? "with successful metadata the selected structured ROM is restored" "rc ${RC}; $(sa_tail "${AF}")"
fi


printf "RESULT failures=%s\n" "$FAIL"
exit "$FAIL"

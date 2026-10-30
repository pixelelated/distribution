#!/bin/bash
# T16 stage E, S1 (#1300, D-CLOUD-188/189): conf_valid's allowlist. Run on a root: ROOT=<root> s1/cells.sh
#  S1-keys     conf_valid lifted from each of its three copies (cloud_backup, cloud_restore,
#              cloud_sync_helper) run in the sandbox (the image's busybox awk) over one conf per line
#  S1-upgraded the helper whole on a pre-rename conf (BACKUPPATH, no SAVESPATH), then conf_valid
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
header "S1 conf_valid's allowlist"
new_cell s1
D="${CELL}/drv"; mkdir -p "${D}/confs"
n=0; mk() { n=$((n + 1)); printf '%s\n' "$2" > "${D}/confs/$(printf %02d "${n}")-$1"; printf '%s\n' "$3" > "${D}/confs/$(printf %02d "${n}")-$1.want"; }
cp "${ROOT}/usr/config/cloud_sync.conf" "${D}/confs/00-shipped"; echo 0 > "${D}/confs/00-shipped.want"
for k in SAVESPATH SETTINGS_BACKUPS SAVES_REMOTE SETTINGS_REMOTE CONTENT_REMOTE LOG_LEVEL RCLONEOPTS RCLONE_NET_OPTS \
         RCLONE_SYNC_NET_OPTS SYNC_CEILING_SECONDS BACKUPMETHOD CLOUD_BACKUP_KEEP BACKUPFILE_BACKUP_OPTION \
         RESTOREMETHOD BACKUPFILE_RESTORE_OPTION RSYNCRMDIR; do mk "doc-${k}" "${k}=\"1\"" 0; done
mk undoc-RCLONE_OUTER 'RCLONE_OUTER="/storage/x"' 1
mk undoc-PARTIALS_CLEAN 'PARTIALS_CLEAN="/storage/roms/x"' 1
mk undoc-LOG_FILE 'LOG_FILE="/tmp/x"' 1
mk undoc-AUTOMATIC 'AUTOMATIC=1' 1
mk undoc-lowercase 'savespath="/storage/x"' 1
mk legacy-BACKUPPATH "$(printf 'SAVESPATH="/storage/roms"\nBACKUPPATH="/storage/roms"')" 0
mk legacy-BACKUPFOLDER "$(printf 'SETTINGS_BACKUPS="/storage/roms/backup"\nBACKUPFOLDER="/storage/roms/backup"')" 0
mk legacy-SYNCPATH "$(printf 'SAVES_REMOTE="/pixelelated/Saves"\nSYNCPATH="/GAMES"')" 0
mk legacy-SYNCPATH_BACKUP "$(printf 'SETTINGS_REMOTE="/pixelelated/Backups"\nSYNCPATH_BACKUP="/GAMES/backup"')" 0
mk legacy-CONTENTPATH "$(printf 'CONTENT_REMOTE="/pixelelated/Content"\nCONTENTPATH="/GAMES"')" 0
mk legacy-RESTOREPATH 'RESTOREPATH="/storage/roms"' 0
cat > "${D}/keys.sh" <<'EOD'
for f in cloud_backup cloud_restore cloud_sync_helper; do sed -n '/^conf_valid() {/,/^}/p' "/usr/bin/${f}" > "/tmp/cv-${f}"; done
echo "-- the three conf_valid bodies: cloud_backup $(wc -l < /tmp/cv-cloud_backup) lines; cmp restore $(cmp -s /tmp/cv-cloud_backup /tmp/cv-cloud_restore && echo same || echo DIFFERS); cmp helper $(cmp -s /tmp/cv-cloud_backup /tmp/cv-cloud_sync_helper && echo same || echo DIFFERS)"
printf '%-30s %-8s %-8s %-8s %-5s %s\n' conf backup restore helper want verdict
for c in /drv/confs/*; do case "${c}" in *.want) continue ;; esac
  line="$(printf '%-30s' "${c##*/}")"; ok=1; want=$(cat "${c}.want")
  for f in cloud_backup cloud_restore cloud_sync_helper; do
    bash -c '. "$1"; conf_valid "$2"; rc=$?; echo "${rc} ${CONF_WHY}"' _ "/tmp/cv-${f}" "${c}" > /tmp/r 2>&1
    rc=$(cut -d" " -f1 < /tmp/r); [ "${rc}" -eq 0 ] 2>/dev/null || rc=1
    [ "$(( rc != 0 ))" -eq "${want}" ] || ok=0
    line="${line} $(printf '%-8s' "rc=${rc}")"; why=$(cut -d" " -f2- < /tmp/r)
  done
  echo "${line} ${want}     $([ "${ok}" = 1 ] && echo PASS || echo FAIL)${why:+  (${why})}"
done
EOD
"${SBX}" bash /drv/keys.sh 2>&1
echo
echo "== S1-upgraded: the helper whole on a pre-rename conf (BACKUPPATH, no SAVESPATH)"
new_cell s1u
C="${CELL}/storage/.config/cloud_sync.conf"
grep -v '^SAVESPATH=' "${ROOT}/usr/config/cloud_sync.conf" > "${C}"; printf 'BACKUPPATH="/storage/roms"\n' >> "${C}"
echo "before: $(grep -c -E '^(SAVESPATH|BACKUPPATH)=' "${C}") path keys: $(grep -o -E '^(SAVESPATH|BACKUPPATH)=' "${C}" | tr '\n' ' ')"
cat > "${CELL}/drv/up.sh" <<'EOD'
/usr/bin/cloud_sync_helper /var/log/cloud_sync.log; echo "helper rc=$?"
sed -n '/^conf_valid() {/,/^}/p' /usr/bin/cloud_backup > /tmp/cv
bash -c '. /tmp/cv; conf_valid /storage/.config/cloud_sync.conf; echo "conf_valid (the copy in cloud_backup) rc=$? ${CONF_WHY}"'
echo "after: path keys: $(grep -o -E '^(SAVESPATH|BACKUPPATH)=[^ ]*' /storage/.config/cloud_sync.conf | tr '\n' ' ')"
echo ".bak: $( [ -f /storage/.config/cloud_sync.conf.bak ] && grep -o -E '^(SAVESPATH|BACKUPPATH)=' /storage/.config/cloud_sync.conf.bak | tr '\n' ' ' || echo none)"
echo "the helper's log lines on the keys: $(grep -i -E 'migrat|BACKUPPATH|legacy|renamed' /var/log/cloud_sync.log | cut -c1-140 | tr '\n' '|')"
EOD
"${SBX}" bash /drv/up.sh 2>&1
echo "== end $(now)"

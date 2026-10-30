#!/bin/bash
# G-20 (Argon): conf_valid refuses only shell-owned names, so the conf can set the scripts' own
# globals. RCLONE_OUTER is run as the program at cloud_restore:365-366. Here: the shipped conf
# with RCLONE_OUTER naming an executable under /storage/.config (as a settings archive, which
# sweeps /storage/.config and keeps modes, can carry one: backuptool:746-751 holds back only four
# files); conf_valid asked; then a deliberate restore whole in the sandbox. If the gate held, the
# program never runs. (A first cut named /usr/bin/touch, which refused rclone's options: out.touch.)
. /workspace/tmp/m6-t16/hl/lib.sh
header "G-20 RCLONE_OUTER from the conf"
new_cell g20
mkdir -p "${CELL}/storage/roms/savestates"
printf '#!/bin/sh\necho "ran as uid $(id -u) with: $*" >> /storage/.config/outer.ran\nexit 0\n' > "${CELL}/storage/.config/outer.sh"
chmod 755 "${CELL}/storage/.config/outer.sh"
printf 'RCLONE_OUTER="/storage/.config/outer.sh"\n' >> "${CELL}/storage/.config/cloud_sync.conf"
echo "appended to the shipped conf: $(tail -1 "${CELL}/storage/.config/cloud_sync.conf")"
"${HL}/sbx.sh" bash -c '
  . <(sed -n "/^conf_valid() {/,/^}/p" /usr/bin/cloud_sync_helper)
  conf_valid /storage/.config/cloud_sync.conf; echo "conf_valid rc=$? (${CONF_WHY:-no reason})"
  cd /tmp && : > /tmp/marker && cloud_restore --yes --saves-only > /tmp/r.out 2>&1; echo "cloud_restore rc=$?"
  echo "-- /storage/.config/outer.ran, which only the named program writes:"; cat /storage/.config/outer.ran 2>/dev/null | cut -c1-160 || echo "(absent)"
  echo "-- the run'"'"'s last lines:"; tr "\r" "\n" < /tmp/r.out | sed "s/\x1b\[[0-9;]*[A-Za-z]//g" | grep -v "^[[:space:]]*$" | tail -6' 2>&1
echo "== end $(now)"

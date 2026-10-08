#!/bin/bash
set -euo pipefail
B=/workspace/tmp/pixelelated-520-ui-20261008
SSH=(ssh -i "$B/guest01/qa-key" -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1)
SCP=(scp -q -i "$B/guest01/qa-key" -P 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null)
"${SSH[@]}" 'systemctl stop essway.service; mkdir -p /storage/qa520/upper /storage/qa520/work /storage/qa520/provider /storage/.config/rclone; mount -t overlay overlay -o lowerdir=/usr/bin,upperdir=/storage/qa520/upper,workdir=/storage/qa520/work /usr/bin'
"${SCP[@]}" "$B/build01/emulationstation" root@127.0.0.1:/storage/qa520/emulationstation
"${SCP[@]}" "$B/build01/artifacts/fr.mo" root@127.0.0.1:/storage/qa520/fr.mo
"${SSH[@]}" 'chmod 755 /storage/qa520/emulationstation; mount --bind /storage/qa520/emulationstation /usr/bin/emulationstation; mount --bind /storage/qa520/fr.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; . /etc/profile; set_setting cloudsync.startup 0; set_setting cloudsync.gameexit 0; set_setting retroachievements.enable 0; set_setting system.language en_US; sed -i "s|<string name=\"Language\" value=\"[^\"]*\"|<string name=\"Language\" value=\"en_US\"|;s|<int name=\"ScreenSaverTime\" value=\"[^\"]*\"|<int name=\"ScreenSaverTime\" value=\"0\"|;s|<bool name=\"UseOSK\" value=\"true\"|<bool name=\"UseOSK\" value=\"false\"|" /storage/.config/emulationstation/es_settings.cfg; sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; rclone version | head -1; ip route; systemctl start essway.service'

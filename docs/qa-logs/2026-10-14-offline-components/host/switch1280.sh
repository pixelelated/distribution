set -e
SYSTEMD_PAGER=cat systemctl stop essway.service
test ! -s /storage/qa575/launch-events
umount /usr/bin/emulationstation
umount /usr/bin/runemu.sh
umount /usr/config/emulationstation/es_systems.cfg
sync

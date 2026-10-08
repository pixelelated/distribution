set -eu
systemctl stop essway.service
p=$(cat /storage/qa520/provider.pid)
tr '\000' ' ' < /proc/$p/cmdline | grep -F 'rclone serve webdav /storage/qa520/provider' >/dev/null || exit 8
kill -TERM "$p"
sleep 1
ps | grep -E 'duckstation|cloud_folder_validate|cloud_scan|cloud_content_restore|rclone' | grep -v grep || true
sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo /usr/bin/duckstation-sa /usr/bin/duckstation_screenshot_path /usr/bin/start_duckstation.sh /usr/config/duckstation/settings.ini
stat -c '%a %s %n' /usr/bin/duckstation-sa
find /storage/qa521 -maxdepth 2 -type f | sort
ip route
sync

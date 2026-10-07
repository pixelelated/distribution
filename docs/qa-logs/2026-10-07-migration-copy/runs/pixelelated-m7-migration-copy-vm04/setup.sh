#!/bin/sh
set -eu
. /etc/profile >/dev/null 2>&1
set_setting cloudsaves.startup 0
set_setting cloudsaves.gameexit 0
set_setting global.retroachievements.offline 0
mkdir -p /storage/qa-copy/cloud/ROCKNIX/Saves/gb /storage/qa-copy/cloud/ROCKNIX/Backups /storage/qa-copy/cloud/ROCKNIX/Content
printf 'migration copy fixture only\n' > /storage/qa-copy/cloud/ROCKNIX/Saves/gb/QA.srm
cat > /storage/.config/rclone/rclone.conf <<'EOF'
[qa_copy]
type = alias
remote = /storage/qa-copy/cloud
EOF
chmod 600 /storage/.config/rclone/rclone.conf
/usr/bin/cloud_sync_helper >/dev/null 2>&1
sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE="/ROCKNIX/Saves"|;s|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE="/ROCKNIX/Backups"|;s|^CONTENT_REMOTE=.*|CONTENT_REMOTE="/ROCKNIX/Content"|;s|^LAYOUT_KEEP=.*|LAYOUT_KEEP=""|' /storage/.config/cloud_sync.conf
CFG=/storage/.config/emulationstation/es_settings.cfg
sed -i '/name="Debug"/d; /name="ScreenSaverTime"/d; /name="ScreenSaverBehavior"/d' "$CFG"
sed -i '/<\/config>/i\    <bool name="Debug" value="true" />\n    <int name="ScreenSaverTime" value="0" />' "$CFG"
/usr/bin/cloud_migrate_layout --state | grep -v -i -E 'key|pass|token|user|psk'

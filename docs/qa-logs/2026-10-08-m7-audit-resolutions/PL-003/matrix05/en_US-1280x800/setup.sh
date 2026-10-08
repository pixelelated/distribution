set -e
systemctl stop essway.service
cp /storage/qa524/delegate/cloud_setup /usr/bin/cloud_setup.qa524
mv /usr/bin/cloud_setup.qa524 /usr/bin/cloud_setup
cp /storage/qa524/matrix-rclone.conf /storage/.config/rclone/rclone.conf
chmod 600 /storage/.config/rclone/rclone.conf
/usr/bin/cloud_setup --set-saves-remote /QA/Saves
/usr/bin/cloud_setup --set-settings-remote /QA/Backups
/usr/bin/cloud_setup --set-content-remote /QA/Content
. /etc/profile
set_setting system.language en_US
cat > /storage/.config/emulationstation/es_settings.cfg <<'XML'
<?xml version="1.0"?>
<config>
<bool name="UseOSK" value="false" />
<int name="ScreenSaverTime" value="0" />
<string name="Language" value="en_US" />
</config>
XML
swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock "output Virtual-1 mode --custom 1280x800@60Hz"
systemctl start essway.service

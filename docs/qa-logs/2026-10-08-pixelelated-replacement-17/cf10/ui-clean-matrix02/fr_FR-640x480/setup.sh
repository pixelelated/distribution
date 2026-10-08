set -e
systemctl stop essway.service
. /etc/profile >/dev/null 2>&1
set_setting system.language fr_FR
cat > /storage/.config/emulationstation/es_settings.cfg <<'XML'
<?xml version="1.0"?>
<config>
<bool name="UseOSK" value="false" />
<int name="ScreenSaverTime" value="0" />
<string name="Language" value="fr_FR" />
</config>
XML
swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock "output Virtual-1 mode 640x480@60Hz"
systemctl start essway.service

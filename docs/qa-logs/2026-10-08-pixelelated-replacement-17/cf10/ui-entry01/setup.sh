set -e
systemctl stop essway.service
. /etc/profile >/dev/null 2>&1
set_setting system.language en_US
cat > /storage/.config/emulationstation/es_settings.cfg <<'XML'
<?xml version="1.0"?>
<config>
<bool name="UseOSK" value="false" />
<int name="ScreenSaverTime" value="0" />
<string name="Language" value="en_US" />
</config>
XML
systemctl start essway.service

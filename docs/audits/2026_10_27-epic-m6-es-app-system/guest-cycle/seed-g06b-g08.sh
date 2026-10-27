# T33 G-06 (black) and G-08 (L-28): ES stopped; the screensaver set to black;
# a game .keys file (FileData.cpp:2192: <rom>.keys) with one mapping on a
# known trigger and one on a trigger checkTriggerExists refuses.
systemctl stop essway
sed -i 's#name="ScreenSaverBehavior" value="dim"#name="ScreenSaverBehavior" value="black"#' /storage/.config/emulationstation/es_settings.cfg
grep ScreenSaverBehavior /storage/.config/emulationstation/es_settings.cfg
cat > /storage/roms/gb/Alpha.gb.keys <<'X'
{
    "actions_player1": [
        { "type": "key", "trigger": "up", "target": "KEY_UP", "description": "T33 KNOWN" },
        { "type": "key", "trigger": "t33unknown", "target": "KEY_DOWN", "description": "T33 UNKNOWN TRIGGER" }
    ]
}
X
md5sum /storage/roms/gb/Alpha.gb.keys
systemctl start essway

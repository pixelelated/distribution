# T33 G-03's second half (L-04): 100 zero-byte captures of Alpha in the
# SCREENSHOTS folder, named <stem>-YYMMDD-HHMMSS.png (DisplayAspectText's
# screenshotContent shape); the carousel started on the imageviewer system.
systemctl stop essway
i=0; while [ $i -lt 100 ]; do : > /storage/roms/screenshots/Alpha-261027-15$(printf %02d $((i / 60)))$(printf %02d $((i % 60))).png; i=$((i + 1)); done
ls /storage/roms/screenshots | wc -l
sed -i 's#name="StartupSystem" value="gb"#name="StartupSystem" value="imageviewer"#' /storage/.config/emulationstation/es_settings.cfg
grep StartupSystem /storage/.config/emulationstation/es_settings.cfg
systemctl start essway

#!/bin/sh
# T32 (#679) G-09: Bravo's picture named in gamelist.xml and absent; detailed style; the carousel on gb.
E=/storage/.config/emulationstation/es_settings.cfg
systemctl stop essway; sleep 1
printf '<?xml version="1.0"?>\n<gameList>\n<game><path>./Alpha.gb</path><name>Alpha</name><manual>/storage/roms/gb/manuals/Alpha.pdf</manual></game>\n<game><path>./Bravo.gb</path><name>Bravo</name><image>/storage/roms/gb/images/Bravo.png</image></game>\n</gameList>\n' > /storage/roms/gb/gamelist.xml
rm -rf /storage/roms/gb/images
for kv in "GamelistViewStyle:detailed" "StartupSystem:gb"; do k=${kv%%:*}; v=${kv#*:}
  if grep -q "name=\"$k\"" $E; then sed -i "s#<string name=\"$k\" value=\"[^\"]*\" />#<string name=\"$k\" value=\"$v\" />#" $E
  else sed -i "s#</config>#\t<string name=\"$k\" value=\"$v\" />\n</config>#" $E; fi; done
ls /storage/roms/gb/images 2>&1 | head -1
systemctl start essway

#!/bin/sh
# T32 (#679) G-02: set the global view style and the startup system with the interface stopped, then start it.
# Usage (by the host loop): STYLE=<style> SYS=<system> sh style.sh
E=/storage/.config/emulationstation/es_settings.cfg
systemctl stop essway; sleep 1
for kv in "GamelistViewStyle:$STYLE" "StartupSystem:$SYS"; do k=${kv%%:*}; v=${kv#*:}
  if grep -q "name=\"$k\"" $E; then sed -i "s#<string name=\"$k\" value=\"[^\"]*\" />#<string name=\"$k\" value=\"$v\" />#" $E
  else sed -i "s#</config>#\t<string name=\"$k\" value=\"$v\" />\n</config>#" $E; fi; done
grep -E 'GamelistViewStyle|StartupSystem' $E
systemctl start essway

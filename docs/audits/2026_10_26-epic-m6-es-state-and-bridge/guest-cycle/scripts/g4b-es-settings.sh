#!/bin/bash
# T21 (#668) G4b: es_settings.cfg emptied beside its whole record, then
# EmulationStation started (Settings::loadFile, Settings.cpp:549-634; no unit test).
echo "== G4b es_settings.cfg emptied beside a whole record ($(date -u +%H:%M:%SZ))"
E=/storage/.config/emulationstation
systemctl stop essway; echo "essway stopped: $(systemctl is-active essway)"
: > "$E/es_settings.cfg"; stat -c 'live now %s bytes' "$E/es_settings.cfg"
: > /var/log/es_log.txt 2>/dev/null
systemctl start essway; sleep 12
echo "essway: $(systemctl is-active essway)"
cmp -s "$E/es_settings.cfg" "$E/es_settings.cfg.backup" && echo "live == the record (written back)" || echo "live differs from the record"
cmp -s "$E/es_settings.cfg" /storage/t21-orig/es_settings.cfg && echo "live == the original live file" || echo "live differs from the original"
stat -c '%a %s bytes %n' "$E/es_settings.cfg" "$E/es_settings.cfg.backup"
grep -E 'es_settings|Settings file' /var/log/es_log.txt 2>/dev/null | cut -c1-200 | head -3

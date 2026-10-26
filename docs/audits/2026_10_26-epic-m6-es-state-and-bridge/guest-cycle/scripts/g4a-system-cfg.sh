#!/bin/bash
# T21 (#668) G4a: system.cfg cut mid-line beside its whole record, with the
# record's mtime (the cut-of-record case, AtomicFileUtil.cpp:339-350), then
# EmulationStation started. Originals kept in /storage/t21-orig for G4's restore.
echo "== G4a system.cfg cut beside a whole record ($(date -u +%H:%M:%SZ))"
C=/storage/.config/system/configs; E=/storage/.config/emulationstation
mkdir -p /storage/t21-orig
cp -p "$C/system.cfg" "$C/system.cfg.backup" "$E/es_settings.cfg" "$E/es_settings.cfg.backup" /storage/t21-orig/
systemctl stop essway; echo "essway stopped: $(systemctl is-active essway)"
size=$(stat -c %s "$C/system.cfg"); half=$((size / 2))
while [ "$(tail -c +"$half" /storage/t21-orig/system.cfg | head -c 1)" = "$(printf '\n')" ]; do half=$((half + 1)); done
head -c "$half" /storage/t21-orig/system.cfg > "$C/system.cfg"
touch -r "$C/system.cfg.backup" "$C/system.cfg"
printf 'live now %s of %s bytes, last byte a line end: %s\n' "$(stat -c %s "$C/system.cfg")" "$size" "$([ -z "$(tail -c 1 "$C/system.cfg")" ] && echo yes || echo no)"
: > /var/log/es_log.txt 2>/dev/null
systemctl start essway; sleep 12
echo "essway: $(systemctl is-active essway)"
cmp -s "$C/system.cfg" "$C/system.cfg.backup" && echo "live == the record (written back)" || echo "live differs from the record"
cmp -s "$C/system.cfg" /storage/t21-orig/system.cfg && echo "live == the original live file" || echo "live differs from the original"
stat -c '%a %s bytes %n' "$C/system.cfg" "$C/system.cfg.backup"
printf 'es_log lines naming the last-known-good record: '; grep -c 'last-known-good record' /var/log/es_log.txt 2>/dev/null
grep 'system.cfg' /var/log/es_log.txt 2>/dev/null | cut -c1-200 | head -3

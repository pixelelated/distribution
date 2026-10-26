#!/bin/bash
# T21 (#668): G4's and G5's originals put back, then EmulationStation restarted.
echo "== G4/G5 restore ($(date -u +%H:%M:%SZ))"
C=/storage/.config/system/configs; E=/storage/.config/emulationstation
systemctl stop essway
cp -p /storage/t21-orig/system.cfg /storage/t21-orig/system.cfg.backup "$C/"
cp -p /storage/t21-orig/es_settings.cfg /storage/t21-orig/es_settings.cfg.backup "$E/"
for f in system.cfg system.cfg.backup; do cmp -s "$C/$f" "/storage/t21-orig/$f" && echo "$f restored" || echo "$f DIFFERS"; done
for f in es_settings.cfg es_settings.cfg.backup; do cmp -s "$E/$f" "/storage/t21-orig/$f" && echo "$f restored" || echo "$f DIFFERS"; done
grep -c '^system.hostname=$' "$C/system.cfg" | sed 's/^/empty hostname lines now: /'
systemctl start essway; sleep 8; echo "essway: $(systemctl is-active essway)"

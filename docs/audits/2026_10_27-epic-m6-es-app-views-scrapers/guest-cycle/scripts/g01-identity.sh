#!/bin/sh
# T32 (#679) G-01: the guest's identity, before any verdict. Identities, hashes and counts only.
echo "== G-01 identity ($(date -u +%H:%M:%SZ))"
grep -E '^(OS_NAME|VERSION|BUILD_ID|BUILD_BRANCH)=' /etc/os-release
fbset 2>/dev/null | grep geometry
echo "-- the installed EmulationStation by literals: M7's composition, then the pin's slice strings"
E=/usr/bin/emulationstation
for lit in 'Pending achievements stay' 'SAVE STATES (HOLD)' 'SKIPPED - YOU CANCELLED IT' 'INVALID CREDENTIALS' \
           'The selected UI mode has nothing to show' '204 No game removed' 'ThreadedScraper::SearchResponse'; do
  printf '%s: %s\n' "$lit" "$(grep -a -c -F "$lit" $E)"
done
sha256sum $E | cut -c1-16
echo "-- systems and the SCREENSHOTS folder"
ls /storage/roms 2>/dev/null | head -40 | tr '\n' ' '; echo
ls /storage/screenshots 2>/dev/null | head -5; ls -d /storage/roms/screenshots /storage/screenshots 2>&1 | cut -c1-80
grep -E '^(GamelistViewStyle|UIMode|Language)' /storage/.emulationstation/es_settings.cfg 2>/dev/null; grep -c . /storage/.emulationstation/es_settings.cfg 2>/dev/null
ip -o link show | cut -d: -f2 | tr '\n' ' '; echo
id -u

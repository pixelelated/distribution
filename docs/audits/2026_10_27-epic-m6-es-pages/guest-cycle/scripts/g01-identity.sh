#!/bin/sh
# T31 (#678) G01: the guest's identity, before any verdict. Identities, hashes and counts only.
echo "== G01 identity ($(date -u +%H:%M:%SZ))"
grep -E '^(OS_NAME|VERSION|BUILD_ID|BUILD_BRANCH)=' /etc/os-release
fbset 2>/dev/null | grep geometry
echo "-- the installed EmulationStation, by two literals (M7's composition, the pin), then the leads' own"
E=/usr/bin/emulationstation
for lit in 'Pending achievements stay' 'SKIPPED - YOU CANCELLED IT' 'THE BIOS CHECK RETURNED NOTHING' 'MOONLIGHT GAME STREAMING' \
           'Unpaired and settings cleared' 'analog_sticks_ledcontrol' 'NO GAMES FIT THAT CRITERIA.' 'COPY TO FREE SLOT'; do
  printf '%s: %s\n' "$lit" "$(grep -a -c -F "$lit" $E)"
done
sha256sum $E | cut -c1-16
echo "-- the leads' binaries"
for b in /usr/bin/moonlight /usr/bin/rocknix-systems /usr/bin/analog_sticks_ledcontrol; do ls -l "$b" 2>&1 | cut -c1-100; done
echo "-- the stores"
ls -l /storage/.config/system/configs/system.cfg /storage/.emulationstation/es_settings.cfg 2>&1 | cut -c1-120
id -u; echo "HOME=$HOME"

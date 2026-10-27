#!/bin/sh
# T26 (#673) G01: the guest's identity, before any verdict. Identities, hashes and counts only.
echo "== G01 identity ($(date -u +%H:%M:%SZ))"
grep -E '^(OS_NAME|VERSION|BUILD_ID|BUILD_BRANCH)=' /etc/os-release
fbset 2>/dev/null | grep geometry
echo "-- the installed EmulationStation, by two literals, then the leads' own"
E=/usr/bin/emulationstation
for lit in 'Pending achievements stay' 'USE CONNECT OR REPAIR CLOUD STORAGE' 'global.videofilters' 'ScrollLoadMedias' \
           'GAME MEDIAS DURING FAST SCROLLING' 'CLOUD CONNECTIONS' 'cloud-oauth-qr.png' 'This version uses manual updates' \
           'WINDOWS SHARE (SMB)' 'system.battery.warning_threshold'; do
  printf '%s: %s\n' "$lit" "$(grep -a -c -F "$lit" $E)"
done
sha256sum $E | cut -c1-16
echo "-- the five scripts, hashed (compared with 8ebaf8daad on the host)"
for f in /usr/bin/cloud_oauth /usr/bin/cloud_remote "$(command -v setsettings.sh)" /etc/profile.d/001-functions "$(command -v setrootpass)"; do
  printf '%s %s\n' "$(sha256sum "$f" 2>/dev/null | cut -c1-64)" "$f"
done

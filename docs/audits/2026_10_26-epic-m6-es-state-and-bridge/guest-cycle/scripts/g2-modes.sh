#!/bin/sh
# T21 (#668) G2: the modes as written. Modes, owners and names only; no content.
echo "== G2 modes ($(date -u +%H:%M:%SZ))"
for f in /storage/.config/system/configs/system.cfg /storage/.config/system/configs/system.cfg.backup \
         /storage/.emulationstation/es_settings.cfg /storage/.emulationstation/es_settings.cfg.backup \
         /storage/.emulationstation/tmp/cookies.txt; do
  if [ -e "$f" ]; then stat -c '%a %U:%G %s bytes %n' "$f"; else echo "absent $f"; fi
done
ls -ld /storage/.emulationstation /storage/.config/system/configs 2>&1
echo "-- leftover temporaries beside the stores now"
ls -la /storage/.config/system/configs/ /storage/.emulationstation/ 2>/dev/null | grep -c '\.tmp\.' 
echo "-- NetworkManager: the keyfile directory, and a keyfile its own writer makes (a dummy key, not the page's join)"
grep -n -E 'keyfile|path' /etc/NetworkManager/NetworkManager.conf 2>/dev/null
kd=$(grep -E '^path=' /etc/NetworkManager/NetworkManager.conf 2>/dev/null | head -1 | cut -d= -f2)
[ -n "$kd" ] || kd=/etc/NetworkManager/system-connections
ls -ld "$kd" 2>&1
k="t21dummy$(date +%s)k"
nmcli connection add type wifi ifname '*' con-name T21-dummy ssid T21-dummy wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$k" >/dev/null 2>&1; echo "nmcli add rc $?"
unset k
for f in "$kd"/*; do [ -e "$f" ] && stat -c '%a %U:%G %n' "$f"; done
printf 'keyfiles carrying a psk line: '; grep -l '^psk=' "$kd"/* 2>/dev/null | wc -l
nmcli connection delete id T21-dummy >/dev/null 2>&1; echo "nmcli delete rc $?"
ls "$kd" 2>/dev/null | grep -c T21-dummy | sed 's/^/T21-dummy keyfiles left: /'

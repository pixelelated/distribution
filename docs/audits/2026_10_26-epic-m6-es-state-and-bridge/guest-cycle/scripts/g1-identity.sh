#!/bin/sh
# T21 (#668) G1: the guest's identity, before any verdict. Prints identities,
# hashes and counts only.
echo "== G1 identity ($(date -u +%H:%M:%SZ))"
uptime; df -h /storage | tail -1
grep -E '^(OS_NAME|VERSION|BUILD_ID|BUILD_BRANCH)=' /etc/os-release
fbset 2>/dev/null | grep geometry
echo "-- the installed EmulationStation, by two literals"
printf 'pin literal (wifi picker: stopping scan worker): '; grep -a -c 'wifi picker: stopping scan worker' /usr/bin/emulationstation
printf 'M7 composition literal (Pending achievements stay): '; grep -a -c 'Pending achievements stay' /usr/bin/emulationstation
sha256sum /usr/bin/emulationstation | cut -c1-16
echo "-- the six OS files, hashed (compared with 8ebaf8daad on the host)"
pu=$(command -v post-update || find /usr -name post-update -type f 2>/dev/null | head -1)
for f in /etc/profile.d/001-functions "$(command -v chksysconfig)" "$(command -v wifictl)" "$(command -v rocknix-evidence)" "$pu" /usr/config/system/configs/system.cfg; do
  printf '%s %s\n' "$(sha256sum "$f" 2>/dev/null | cut -c1-64)" "$f"
done
echo "-- the 7zr question and poppler"
ls -la /usr/bin/7z* /usr/bin/pdfinfo /usr/bin/pdftoppm 2>&1
echo "-- the CA bundle and curl"
ls -la /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt 2>&1 | head -3
curl --version 2>&1 | grep -E '^(curl|Protocols)'
echo "-- /storage's filesystem and options"
grep ' /storage ' /proc/mounts
echo "-- /bin/sh"
ls -la /bin/sh

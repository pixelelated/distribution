{
printf 'OBSERVED '; date -u +%Y-%m-%dT%H:%M:%SZ
awk '/^(VERSION|BUILD_ID)=/' /etc/os-release
printf 'BOOT_ID '; cat /proc/sys/kernel/random/boot_id
printf 'BOOTS\n'; journalctl --list-boots --no-pager | tail -n 8
for b in -1 -2 0; do
 printf '\nBOOT %s SHUTDOWN MARKERS\n' "$b"
 journalctl -b "$b" --no-pager -o short-iso | grep -i -E 'power.?off|shut.?down|reboot|restart|linuxloader|boot.?reason|reset.?reason|psci|watchdog|panic|thermal|qcom.*pon' | tail -n 180
 printf '\nBOOT %s FINAL JOURNAL\n' "$b"
 journalctl -b "$b" --no-pager -o short-iso -n 90
 done
printf '\nPSTORE PRESENT\n'
for d in /sys/fs/pstore /storage/.cache/log/pstore; do
 if test -d "$d"; then ls -l "$d"; else printf 'ABSENT %s\n' "$d"; fi
done
printf '\nBOOT REASON FIELDS\n'
for f in /sys/kernel/boot_reason /proc/sys/kernel/boot_reason /sys/class/pon/pon0/pon_reason /sys/class/pon/pon0/poff_reason; do
 if test -r "$f"; then printf '%s=' "$f"; cat "$f"; fi
done
} 2>&1 | grep -v -i -E 'key|pass|token|user|psk'

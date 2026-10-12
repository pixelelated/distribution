{
printf 'OBSERVED '; date -u +%Y-%m-%dT%H:%M:%SZ
for b in -4 -3; do
 printf '\nBOOT %s SHUTDOWN MARKERS\n' "$b"
 journalctl -b "$b" --no-pager -o short-iso | grep -i -E 'power.?off|shut.?down|reboot|restart|reset.?reason|psci|watchdog|panic' | tail -n 90
 printf '\nBOOT %s FINAL JOURNAL\n' "$b"
 journalctl -b "$b" --no-pager -o short-iso -n 100
 done
printf '\nBOOT IDS\n'; journalctl --list-boots --no-pager | tail -n 6
printf '\nPSTORE COUNTS\n'
for d in /sys/fs/pstore /storage/.cache/log/pstore; do
 if test -d "$d"; then printf '%s ' "$d"; find "$d" -maxdepth 1 -type f | wc -l; fi
done
} 2>&1 | grep -v -i -E 'key|pass|token|user|psk'

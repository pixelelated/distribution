{
printf 'OBSERVED '; date -u +%Y-%m-%dT%H:%M:%SZ
printf 'BOOT_ID '; cat /proc/sys/kernel/random/boot_id
printf '\nPOWER NOW\n'
for d in /sys/class/power_supply/*; do
 test -d "$d" || continue
 printf 'SUPPLY %s\n' "${d##*/}"
 for f in type online status capacity; do
  if test -r "$d/$f"; then printf '%s=' "$f"; cat "$d/$f"; fi
 done
done
printf '\nES QUIT MARKERS\n'
for f in /var/log/es_log.txt /var/log/es_log.0.txt /var/log/es_log.1.txt /var/log/es_log.2.txt /var/log/es_log.3.txt; do
 if test -r "$f"; then
  printf 'LOG %s\n' "$f"
  grep -i -E 'quit.*mode|shut.?down|power.?off|request.*reboot|reboot.*request|normal exit|clean exit' "$f" | tail -n 25
 fi
done
for b in 52543b41126a41cd901cf4484e7c6d16 496eb86292f64eaea72f261a8bf5b988 2f68a63fb8fe4caf9e61bcfbfa12ffe5; do
 printf '\nKERNEL %s\n' "$b"
 journalctl -b "$b" -k --no-pager -o short-iso | grep -i -E 'power.?off|shut.?down|reboot|reset|reason|panic|watchdog|qcom.*pon|pmic|usb.*disconnect|usb.*connect|charger|charging|pstore|ramoops' | tail -n 65
 printf '\nCLOCK %s\n' "$b"
 journalctl -b "$b" -u systemd-timesyncd --no-pager -o short-iso | tail -n 8
done
printf '\nREASON AVAILABILITY\n'
for f in /sys/kernel/boot_reason /proc/sys/kernel/boot_reason /sys/class/pon/pon0/pon_reason /sys/class/pon/pon0/poff_reason; do
 if test -r "$f"; then printf '%s=' "$f"; cat "$f"; else printf 'ABSENT %s\n' "$f"; fi
done
} 2>&1 | grep -v -i -E 'key|pass|token|user|psk'

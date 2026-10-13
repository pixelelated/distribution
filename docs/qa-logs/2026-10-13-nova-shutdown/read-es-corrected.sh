{
printf 'OBSERVED '; date -u +%Y-%m-%dT%H:%M:%SZ
printf 'BOOT_ID '; cat /proc/sys/kernel/random/boot_id
for f in /var/log/es_log.txt /var/log/es_log.0.txt /var/log/es_log.1.txt /var/log/es_log.2.txt /var/log/es_log.3.txt; do
 if test -r "$f"; then
  printf 'LOG %s\n' "$f"
  grep -i -E 'quit.*mode|shut.?down|shutting|rebooting|power.?off|request.*reboot|reboot.*request|normal exit|clean exit' "$f" | tail -n 25
 fi
done
} 2>&1 | grep -v -i -E 'key|pass|token|user|psk'

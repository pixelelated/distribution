{
printf 'OBSERVED '; date -u +%Y-%m-%dT%H:%M:%SZ
printf 'BOOT_ID '; cat /proc/sys/kernel/random/boot_id
printf '\nFRONTEND POWER INTENTS\n'
for f in /var/log/es_log.txt /var/log/es_log.0.txt /var/log/es_log.1.txt /var/log/es_log.2.txt /var/log/es_log.3.txt; do
 if test -r "$f"; then printf 'LOG %s\n' "$f"; grep -i -E 'fast.?shutdown|shutdown|power.?off|reboot|quitmode|quit mode|ignoregamelist' "$f" | tail -n 20; fi
done
printf '\nKERNEL EVIDENCE CONFIG\n'
if test -r /proc/config.gz; then zcat /proc/config.gz | grep -E '^(CONFIG_(PSTORE|PSTORE_RAM|PSTORE_CONSOLE|QCOM_PON|QCOM_SPMI_PMIC|SOFTLOCKUP_DETECTOR|DETECT_HUNG_TASK|WATCHDOG|QCOM_WDT)=|# CONFIG_(PSTORE|PSTORE_RAM|PSTORE_CONSOLE|SOFTLOCKUP_DETECTOR|DETECT_HUNG_TASK|QCOM_WDT) is not set)'; else printf 'NO PROC CONFIG\n'; fi
printf '\nJOURNAL STORE\n'
findmnt -n -o TARGET,FSTYPE /var/log
printf '\nNAMED BOOT POWER FIELDS\n'
for f in /sys/class/power_supply/*/online /sys/class/power_supply/*/status; do if test -r "$f"; then printf '%s=' "$f"; cat "$f"; fi; done
printf '\nBOOT KERNEL STORAGE AND POWER\n'
for b in 37a6ecb2cefb4dbc950d4c57459c3679 dd249ebc7aa84ec9a683c612ca9cc5f1 8fc07347084845548f349444ec823e4c 81034c70ddad49579f564f619a8b88f0 5f1419597e3a40ce81ff911ffaa30721; do
 printf 'BOOT %s\n' "$b"
 journalctl -k -b "$b" --no-pager -o short-iso | grep -i -E 'pstore|ramoops|boot.?reason|reset.?reason|pon.reason|poff.reason|qcom.*pon|reboot:|power down|I/O error|mmc.*(error|fail|timeout)|EXT4-fs.*(error|warning)|watchdog.*(reset|bite)|panic' | tail -n 30
done
} 2>&1 | grep -v -i -E 'key|pass|token|user|psk'

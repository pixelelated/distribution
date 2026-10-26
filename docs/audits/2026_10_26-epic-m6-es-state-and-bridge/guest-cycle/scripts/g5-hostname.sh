#!/bin/bash
# T21 (#668) G5: D-NET-009's empty system.hostname= written by the real
# set_setting, then EmulationStation restarted; the HOSTNAME row is framed.
echo "== G5 system.hostname= ($(date -u +%H:%M:%SZ))"
C=/storage/.config/system/configs
grep -c '^system.hostname=' "$C/system.cfg" | sed 's/^/hostname lines before: /'
systemctl stop essway
. /etc/profile.d/001-functions; set_setting system.hostname default; echo "set_setting rc $?"
printf 'lines reading exactly system.hostname= : '; grep -c '^system.hostname=$' "$C/system.cfg"
systemctl start essway; sleep 10; echo "essway: $(systemctl is-active essway)"

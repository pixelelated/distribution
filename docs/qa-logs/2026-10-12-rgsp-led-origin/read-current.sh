{
printf 'OBSERVED '; date -u +%Y-%m-%dT%H:%M:%SZ
printf 'BOOT_ID '; cat /proc/sys/kernel/random/boot_id
for f in /storage/.config/system/configs/system.cfg /storage/.config/system/configs/system.cfg.backup; do
 printf 'SETTINGS %s\n' "$f"
 if test -r "$f"; then awk -F= '$1=="led.color" || $1=="system.battery.warning_threshold" {print}' "$f"; else printf 'ABSENT\n'; fi
done
for f in /sys/class/leds/green:power/brightness /sys/class/leds/red:status/brightness /sys/class/leds/green:power/trigger /sys/class/leds/red:status/trigger /sys/class/power_supply/axp20x-usb/online /sys/class/power_supply/battery/status /sys/class/power_supply/battery/capacity; do
 if test -r "$f"; then printf '%s=' "$f"; cat "$f"; fi
done
printf 'WARNINGS\n'
journalctl --no-pager -o short-iso -u powerstate.service -n 60 | grep -E 'battery|Battery|Switching|Started|Stopped|Stopping|terminated|killed|signal'
} 2>&1 | grep -v -i -E 'key|pass|token|user|psk'

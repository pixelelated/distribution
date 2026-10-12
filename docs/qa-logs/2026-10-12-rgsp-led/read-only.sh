{
date -u +%Y-%m-%dT%H:%M:%SZ
awk '/^(VERSION|BUILD_ID|BUILD_VERSION)=/' /etc/os-release
for f in /storage/.config/system/configs/system.cfg /storage/.config/system/configs/system.cfg.backup; do
 printf 'CONFIG %s\n' "$f"
 awk '/^led\.color=/' "$f"
done
for d in /sys/class/leds/green:power /sys/class/leds/red:status; do
 for n in brightness trigger; do printf '%s/%s=' "$d" "$n"; cat "$d/$n"; done
done
for d in /sys/class/power_supply/*; do
 for n in type status capacity online; do
  if test -r "$d/$n"; then printf '%s/%s=' "$d" "$n"; cat "$d/$n"; fi
 done
done
if test -r /tmp/battery.percent; then printf 'DISPLAY_CACHE='; cat /tmp/battery.percent; fi
sha256sum /usr/bin/ledcontrol /usr/lib/autostart/quirks/platforms/H700/bin/ledcontrol /usr/bin/led_flash /usr/bin/powerstate
} | grep -v -i -E 'key|pass|token|user|psk'

#!/bin/bash
# T21 (#668) G3: the Wi-Fi key on argv, by the page's command shape
# (ApiSystem.cpp:635-637 through system()). A dummy network and a dummy key
# made here; counts only, the key is never printed.
echo "== G3 the key on argv ($(date -u +%H:%M:%SZ))"
stat -c 'seed %a %n' /usr/config/system/configs/system.cfg
printf 'network interfaces: '; ls /sys/class/net | tr '\n' ' '; echo
k="t21dummy$(date +%s)$$k"
sh -c "timeout 150 wifictl connect 'T21-dummy-net' '$k' 'US'" > /dev/null 2>&1 &
bg=$!
max=0; samples=0; topcount=-1
end=$(( $(date +%s) + 3 ))
while [ "$(date +%s)" -lt "$end" ]; do
  n=$(grep -l -F -- "$k" /proc/[0-9]*/cmdline 2>/dev/null | wc -l)
  samples=$((samples + 1)); [ "$n" -gt "$max" ] && max=$n
  if [ "$topcount" -lt 0 ]; then topcount=$(timeout 10 top -b -n 1 2>/dev/null | head -25 | grep -c -F -- "$k"); fi
  kill -0 "$bg" 2>/dev/null || break
done
wait "$bg"; rc=$?
echo "the connect's exit: $rc"
echo "samples $samples; the most processes whose cmdline carried the key at once: $max"
echo "rocknix-evidence's top line (top -b -n 1 | head -25), lines carrying the key: $topcount"
unset k
echo "-- what system.cfg says after a connect with no adapter (key names only)"
grep -c '^wifi.ssid=T21-dummy-net$' /storage/.config/system/configs/system.cfg | sed 's/^/wifi.ssid=T21-dummy-net lines: /'

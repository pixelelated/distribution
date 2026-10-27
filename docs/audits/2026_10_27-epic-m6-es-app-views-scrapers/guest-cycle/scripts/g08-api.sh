#!/bin/sh
# T32 (#679) G-08: the local HTTP API from inside the guest (127.0.0.1:1234). Codes and short bodies only.
U=http://127.0.0.1:1234
echo "== G-08 ($(date -u +%H:%M:%SZ))"
printf 'caps: '; wget -qO- $U/caps | tr -d '\n' | grep -o '"Version"[^,]*' | head -1
printf 'isIdle: '; wget -qO- $U/isIdle | tr -d '\n'; echo
LONG="T32 G-08 a notification body far longer than one line of a 640 by 480 panel can hold, to read what the toast does with it, $(date -u +%H%M%S)"
printf 'notify: '; wget -qO- --post-data="$LONG" $U/notify; echo "rc $?"
printf 'removegames (a path outside the system): '; wget -S -qO- --post-data='<gameList><game><path>/storage/t32-outside.gb</path></game></gameList>' $U/removegames/gb 2>&1 | grep -E 'HTTP/|No game' | tr '\n' ' '; echo
ls -l /storage/roms/gb | grep -c '\.gb$'

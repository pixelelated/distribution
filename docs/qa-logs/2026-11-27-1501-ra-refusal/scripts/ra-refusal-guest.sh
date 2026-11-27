#!/bin/bash
# The guest half of #1501's proof. QA guest only; no real account.
#   account token|password  a synthetic account (QA1501, with a local token,
#                  or a password and no cached sign-in), the proxy on, its
#                  upstream at the loopback stand-in. Persistent: reboot after
#                  it, so EmulationStation reads it (the scan row writes ES's
#                  own copy of system.cfg back).
#   standin <status>  the stand-in, answering every request <status>
#   release        the stand-in stopped; config.json, the proxy store and
#                  the account put back
#   scan           the ctl's scan from the shell: its >>> lines and rc
. /etc/profile >/dev/null 2>&1
D=/storage/m7-qa-1501; CFG=/storage/.config/raofflineproxy; PORT=18601
case "$1" in
account)
    set_setting global.retroachievements 0
    set_setting global.retroachievements.username QA1501
    case "$2" in
        token) set_setting global.retroachievements.token local-fixture-1501; set_setting global.retroachievements.password "" ;;
        password) set_setting global.retroachievements.token ""; set_setting global.retroachievements.password local-fixture-1501 ;;
        *) exit 2 ;;
    esac
    if [ "$(get_setting global.retroachievements.offlineproxy)" != 1 ]; then
        raofflineproxy-ctl enable >/dev/null 2>&1 || { echo "enable failed"; exit 1; }
    fi
    mkdir -p "$CFG" "$D"
    [ -e "$D/config.json.before" ] || [ -e "$D/config.json.absent" ] ||
        { if [ -e "$CFG/config.json" ]; then cp -p "$CFG/config.json" "$D/config.json.before"; else : > "$D/config.json.absent"; fi; }
    python3 - "$CFG/config.json" "$PORT" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1]); d = json.loads(p.read_text()) if p.exists() and p.read_text().strip() else {}
d["upstream_host"] = "http://127.0.0.1:%s" % sys.argv[2]; p.write_text(json.dumps(d, indent=2) + "\n")
PY
    # No cached sign-in, so a password is signed in with (and refused).
    if [ "$2" = password ] && ls "$CFG"/proxy.sqlite3* >/dev/null 2>&1; then
        systemctl stop raofflineproxy; mkdir -p "$D/store-aside"; mv "$CFG"/proxy.sqlite3* "$D/store-aside/"; systemctl start raofflineproxy
    fi
    echo "toggle=$(get_setting global.retroachievements.offlineproxy) service=$(systemctl is-active raofflineproxy) mode=$2"
    ;;
standin)
    systemctl stop ra-standin-1501 2>/dev/null
    systemd-run --unit=ra-standin-1501 --quiet python3 "$D/standin.py" "$PORT" "$2" || exit 1
    for i in 1 2 3 4 5; do sleep 1; c=$(curl -s -m 3 -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT/dorequest.php"); [ "$c" = "$2" ] && break; done
    echo "standin answers $c"; [ "$c" = "$2" ]
    ;;
release)
    systemctl stop ra-standin-1501 2>/dev/null
    if [ -e "$D/config.json.before" ]; then mv "$D/config.json.before" "$CFG/config.json"; else rm -f "$CFG/config.json" "$D/config.json.absent"; fi
    if [ -d "$D/store-aside" ]; then systemctl stop raofflineproxy; rm -f "$CFG"/proxy.sqlite3*; mv "$D/store-aside"/* "$CFG/" 2>/dev/null; rmdir "$D/store-aside"; systemctl start raofflineproxy; fi
    set_setting global.retroachievements.token ""; set_setting global.retroachievements.password ""; set_setting global.retroachievements.username ""
    echo "released"
    ;;
scan)
    raofflineproxy-ctl scan 2>/dev/null | grep '^>>>'; echo "rc=${PIPESTATUS[0]}"
    ;;
*) exit 2 ;;
esac

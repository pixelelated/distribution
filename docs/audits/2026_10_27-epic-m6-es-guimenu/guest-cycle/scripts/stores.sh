#!/bin/sh
# T26 (#673): the named keys' lines in system.cfg and es_settings.cfg, through the credential filter.
# Usage: sh stores.sh <label> <key regex>
echo "== stores: $1 ($(date -u +%H:%M:%SZ))"
printf 'system.cfg: '; grep -E "^($2)=" /storage/.config/system/configs/system.cfg | grep -v -i -E 'key|pass|token|user|psk' | tr '\n' ' '; echo
printf 'es_settings.cfg: '; grep -o -E "name=\"($2)\"[^/]*" /storage/.emulationstation/es_settings.cfg | grep -v -i -E 'key|pass|token|user|psk' | tr '\n' ' '; echo
printf 'mtimes: '; stat -c '%n %Y' /storage/.config/system/configs/system.cfg /storage/.emulationstation/es_settings.cfg | tr '\n' ' '; echo

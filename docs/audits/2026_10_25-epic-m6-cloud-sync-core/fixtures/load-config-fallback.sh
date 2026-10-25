#!/bin/bash
# T16 lead 1: load_config sources the conf conf_valid refused when the .bak copy fails.
#   run.sh <cloud_backup or cloud_restore at 8ebaf8daad> unfixed-shape
# Lifts conf_valid, load_config, log_message, say_why and clean_exit's stand-in from the
# script; rewrites /storage/.config to a scratch dir; the one planted input is a cp that
# fails (the full card), named here. The refused conf carries a line that, if sourced,
# leaves a marker file; conf_valid refuses it ("something after the value").
set -u
SRC=${1:?script}; W=$(mktemp -d "${TMPDIR:?}/lc.XXXXXX"); mkdir -p "$W/storage/.config"
python3 -I - "$SRC" "$W/funcs.sh" "$W" <<'PY'
import re, sys
src, out, w = sys.argv[1], sys.argv[2], sys.argv[3]
L = open(src).read().split("\n"); keep = {"conf_valid", "load_config", "say_why"}; buf = []; i = 0
while i < len(L):
    m = re.match(r"^([a-z_]+)\(\)", L[i])
    if m and m.group(1) in keep:
        j = i
        while not L[j].startswith("}"): j += 1
        buf += L[i:j + 1]; i = j + 1; continue
    i += 1
open(out, "w").write("\n".join(buf).replace("/storage/.config", w + "/storage/.config") + "\n")
PY
# a valid .bak (the shipped conf) and a refused live conf whose sourcing leaves a marker
cp "$(dirname "$SRC")/cloud_sync.conf" "$W/storage/.config/cloud_sync.conf.bak"
{ cat "$W/storage/.config/cloud_sync.conf.bak"; printf 'EXTRA=x; : > %s/SOURCED_REFUSED\n' "$W"; } > "$W/storage/.config/cloud_sync.conf"
for mode in cp-works cp-fails; do
  rm -f "$W/SOURCED_REFUSED"; cp "$W/storage/.config/cloud_sync.conf" "$W/live.$mode"
  bash -c '
    W=$1; mode=$2
    log_message() { echo "LOG[$3] $1" >> "$W/log.$mode"; }; clean_exit() { echo "clean_exit $1" >> "$W/log.$mode"; exit "$1"; }
    pause() { :; }; controller_confirm() { return 1; }
    [ "$mode" = cp-fails ] && cp() { return 1; }      # the planted input: the copy fails, as on a full card
    AUTOMATIC=1; ASSUME_YES=1; SYSTEM_ONLY=0; METHOD_OVERRIDE=""; EXTRA_UPDATE=0; START_TIME=$(date +%s); WHY_SAID=0
    RCLONE_NET_OPTS_FALLBACK="x"; RCLONE_SYNC_NET_OPTS_FALLBACK="x"; SYNC_CEILING_SECONDS_FALLBACK=90; LOG_FILE=/dev/null
    . "$W/funcs.sh"; load_config; echo "load_config returned $?" >> "$W/log.$mode"' _ "$W" "$mode" > "$W/out.$mode" 2>&1
  printf '%s: rc=%s sourced_refused=%s conf_now_valid=%s tmp_left=%s\n' "$mode" "$?" \
    "$([ -e "$W/SOURCED_REFUSED" ] && echo YES || echo no)" \
    "$(bash -c '. "$1/funcs.sh"; conf_valid "$1/storage/.config/cloud_sync.conf" && echo yes || echo no' _ "$W")" \
    "$(ls "$W/storage/.config/" | grep -c '\.tmp\.' )"
  cp "$W/live.$mode" "$W/storage/.config/cloud_sync.conf"
  grep -E 'clean_exit|putting back|returned' "$W/log.$mode" | sed 's/^/    /'
done
echo "scratch: $W"

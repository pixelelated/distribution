#!/bin/bash
# T22 stream S3 (#1107): does 095-cloud-ssh accept only a whole port?
#   drive.sh <path to 095-cloud-ssh> unfixed|fixed
# Extracts the quirk's port block (from `PORT=""` to the `fi` that closes
# it) and runs it over constructed fw_cfg values, with `logger` stubbed to
# record its calls. Writes only under $TMPDIR. One verdict line last.
set -u
f=${1:?file}; want=${2:?unfixed|fixed}
W=$(mktemp -d "${TMPDIR:?}/s3.XXXXXX")
blk="$W/block.sh"
awk '/^PORT=""$/{p=1} p{print} p&&/^fi$/{exit}' "$f" > "$blk"
[ -s "$blk" ] || { echo "s3: UNEXPECTED (no port block found in $f)"; exit 2; }
run() {   # run <label> <printf format for the fw_cfg file's bytes>
  printf "$2" > "$W/fwcfg"
  out=$(FWCFG="$W/fwcfg" bash -c 'logger(){ echo "LOGGER: $*" >&2; }; . "$1"; printf "%s" "${PORT}"' _ "$blk" 2>"$W/err")
  printf '%-8s -> port [%s]%s\n' "$1" "$out" "$(grep -q LOGGER "$W/err" && printf ' logged: %s' "$(grep LOGGER "$W/err" | head -1 | cut -c9-)")"
  eval "R_$3=\"\$out\""
}
run "1234"   '1234'    a
run "1234\\n" '1234\n' b
run "12x34"  '12x34'   c
run "70000"  '70000'   d
run "(empty)" ''       e
run "0"      '0'       f
# Two boots of the whole quirk, /storage and fw_cfg redirected under $W:
# boot 1 with the unfixed file at the stage-D tip ($T22_UNFIXED, or the file
# itself) writes its command from 12x34; boot 2 with the file under test
# and the same value: the fixed quirk finds no port and removes the command
# its record names (:72-74); the unfixed keeps it.
twoboot() {
  local q1="$1" q2="$2" st="$W/storage"; rm -rf "${st:?}"; mkdir -p "$st/.config"
  printf '12x34' > "$W/fwcfg"
  for q in "$q1" "$q2"; do
    sed -e "s#/sys/firmware/qemu_fw_cfg/by_name/opt/org.rocknix.cloud_ssh_port/raw#$W/fwcfg#" \
        -e "s#/storage/#$st/#g" "$q" > "$W/q.sh"
    bash -c 'logger(){ :; }; export -f logger; . "$1"' _ "$W/q.sh" >/dev/null 2>&1
  done
  [ -e "$st/.config/cloud_setup_ssh" ] && cat "$st/.config/cloud_setup_ssh" || echo "(removed)"
}
U1=${T22_UNFIXED:-$f}
R_g=$(twoboot "$U1" "$f")
printf 'two boots (12x34; boot 1 at the stage-D tip, boot 2 this file) -> %s\n' "$R_g"
rm -rf "${W:?}"
case "$want" in
  unfixed) [ "$R_a" = 1234 ] && [ "$R_c" = 1234 ] && [ "$R_g" != "(removed)" ] && { echo "s3: unfixed-expectation-met (12x34 kept as 1234; the wrong command stays)"; exit 0; } ;;
  fixed)   [ "$R_a" = 1234 ] && [ "$R_b" = 1234 ] && [ -z "$R_c" ] && [ -z "$R_d" ] && [ -z "$R_e" ] && [ -z "$R_f" ] && [ "$R_g" = "(removed)" ] \
             && { echo "s3: fixed-expectation-met (1234 accepted; 12x34, 70000, 0 and empty refused; the earlier wrong command removed)"; exit 0; } ;;
esac
echo "s3: UNEXPECTED ($want: 1234 [$R_a], 12x34 [$R_c], 70000 [$R_d], empty [$R_e], 0 [$R_f], two boots [$R_g])"; exit 1

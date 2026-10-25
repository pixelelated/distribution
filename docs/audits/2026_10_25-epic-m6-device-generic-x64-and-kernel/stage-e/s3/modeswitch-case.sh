#!/bin/bash
# T11 S3 (#1087): does the Netgear WNDA3200 modeswitch rule (line 7 of
# 40-usb_modeswitch.rules) queue its eject for non-block events?
#
#   modeswitch-case.sh <40-usb_modeswitch.rules> <unfixed|fixed>
#
# The host has no 0cf3:20ff dongle and no umockdev, so the case runs udev's
# own matcher (`udevadm test`, which simulates an event and runs no RUN
# program) over a copy of the rule whose vendor and product IDs -- and only
# those -- are swapped for the host's first USB root hub (1d6b:0002). It then
# tests two non-block events under that hub: the USB device (usb1) and its
# interface (1-0:1.0). This is a synthetic input, named (vm-first.md): the
# identity is substituted; the match semantics, ATTRS against the event's
# device and its parents, are udev's.
#   unfixed: eject is queued for both non-block events.
#   fixed:   eject is queued for neither (the match is scoped to block).
# The host has no USB block device, so the fixed rule's firing on a block
# child is not shown here. The rule file must also pass `udevadm verify`.
# Writes only under $TMPDIR; prints one verdict line last; exits 0 when the
# side's expectation is met, 1 when not, 2 when it cannot run.
set -u
F=${1:?rule file}; SIDE=${2:?unfixed or fixed}
[ -f "$F" ] || { echo "modeswitch-case: CANNOT -- no file $F"; exit 2; }
command -v udevadm >/dev/null || { echo "modeswitch-case: CANNOT -- no udevadm"; exit 2; }
for d in /sys/bus/usb/devices/usb1 /sys/bus/usb/devices/1-0:1.0; do
  [ -e "$d" ] || { echo "modeswitch-case: CANNOT -- no $d"; exit 2; }
done
[ "$(cat /sys/bus/usb/devices/usb1/idVendor):$(cat /sys/bus/usb/devices/usb1/idProduct)" = 1d6b:0002 ] || { echo "modeswitch-case: CANNOT -- usb1 is not 1d6b:0002"; exit 2; }
W=$(mktemp -d "${TMPDIR:?}/s3-udev.XXXXXX") || exit 2
mkdir -p "$W/rules"
grep -c 'ATTRS{idVendor}=="0cf3", ATTRS{idProduct}=="20ff"' "$F" | grep -qx 1 || { echo "modeswitch-case: CANNOT -- line 7's ID pair not found once"; exit 2; }
sed -e 's/ATTRS{idVendor}=="0cf3", ATTRS{idProduct}=="20ff"/ATTRS{idVendor}=="1d6b", ATTRS{idProduct}=="0002"/' "$F" > "$W/rules/99-t11-modeswitch.rules"
echo "  | udev $(udevadm --version); the rule under test, IDs swapped: $(grep -n '1d6b' "$W/rules/99-t11-modeswitch.rules")"
udevadm verify --no-style "$F" > "$W/verify" 2>&1; vrc=$?
queued=""
for d in usb1 1-0:1.0; do
  timeout 60 udevadm test --action=add -N never --extra-rules-dir="$W/rules" "/sys/bus/usb/devices/$d" > "$W/$d.out" 2>&1
  trc=$?
  [ "$trc" = 0 ] || { echo "modeswitch-case: CANNOT -- udevadm test $d rc=$trc"; exit 2; }
  grep -q '99-t11-modeswitch.rules' "$W/$d.out" || { echo "modeswitch-case: CANNOT -- the rule was not read for $d"; exit 2; }
  if grep -q "RUN{program} : /usr/bin/eject '/dev/$d'" "$W/$d.out"; then
    queued="$queued $d=eject"; grep -n "99-t11-modeswitch.rules:7" "$W/$d.out" | sed 's/^/  | /' | cut -c1-200
  else
    queued="$queued $d=none"
  fi
done
facts="verify-rc=$vrc${queued}"
case "$SIDE" in
  unfixed) [ "$vrc" = 0 ] && [ "${queued# }" = "usb1=eject 1-0:1.0=eject" ] && ok=1 || ok=0 ;;
  fixed)   [ "$vrc" = 0 ] && [ "${queued# }" = "usb1=none 1-0:1.0=none" ] && ok=1 || ok=0 ;;
  *) echo "modeswitch-case: CANNOT -- side $SIDE"; exit 2 ;;
esac
if [ "$ok" = 1 ]; then
  echo "modeswitch-case: $SIDE-expectation-met ($facts)"; exit 0
fi
echo "modeswitch-case: UNEXPECTED on $SIDE ($facts)"; exit 1

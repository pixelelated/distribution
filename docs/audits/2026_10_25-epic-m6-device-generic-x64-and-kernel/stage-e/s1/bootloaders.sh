#!/bin/bash
# T11 S1 (PL-06): every device's BOOTLOADER= at a commit is one the fixed
# install keeps (syslinux, u-boot, qcom-abl, arm-efi), so its refusal of any
# other value reaches no device.
#
#   bootloaders.sh <repository> <commit>
#
# Prints each device's line, then one verdict line; exits 0 when every value
# is kept and at least one device was read, 1 otherwise, 2 when it cannot run.
set -u
REPO=${1:?repository}; REF=${2:?commit}
lines=$(git -C "$REPO" grep -n -E '^\s*BOOTLOADER=' "$REF" -- 'projects/ROCKNIX/devices/*/options') || { echo "bootloaders: CANNOT -- git grep failed at $REF"; exit 2; }
printf '%s\n' "$lines" | sed 's/^/  | /'
total=0; bad=0
while IFS= read -r l; do
  [ -n "$l" ] || continue
  total=$((total + 1))
  v=$(printf '%s' "${l#*BOOTLOADER=}" | tr -d '"'"'"' \r')
  case "$v" in
    syslinux|u-boot|qcom-abl|arm-efi) ;;
    *) bad=$((bad + 1)); echo "  outside the kept loaders: $l" ;;
  esac
done <<< "$lines"
if [ "$total" -gt 0 ] && [ "$bad" = 0 ]; then
  echo "bootloaders: every value kept ($total devices at $REF)"; exit 0
fi
echo "bootloaders: FAIL ($bad of $total devices outside the kept loaders at $REF)"; exit 1

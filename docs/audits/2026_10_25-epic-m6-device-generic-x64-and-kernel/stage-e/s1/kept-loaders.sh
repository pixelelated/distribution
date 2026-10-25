#!/bin/bash
# T11 S1 (PL-06), the control: the branches install keeps by design --
# u-boot, qcom-abl and arm-efi, whose loaders the image step writes -- still
# return 0 with "installation completed" when sourced as scripts/image:280
# sources them. The same on both sides.
#
#   kept-loaders.sh <install file> <unfixed|fixed>
#
# Writes only under $TMPDIR; prints one verdict line last; exits 0 when all
# three succeed, 1 when one does not, 2 when it cannot run.
set -u
F=${1:?install file}; SIDE=${2:?unfixed or fixed}
[ -f "$F" ] || { echo "kept-loaders: CANNOT -- no file $F"; exit 2; }
W=$(mktemp -d "${TMPDIR:?}/s1-kept.XXXXXX") || exit 2
bad=0; facts=""
for bl in u-boot qcom-abl arm-efi; do
  mkdir -p "$W/$bl"
  INSTALL="$W/$bl" BOOTLOADER="$bl" DEVICE=FIXTURE \
    bash -c 'set +e; . "$1"; echo "SOURCED-RETURNED rc=$?"' _ "$F" > "$W/$bl.out" 2>&1
  rc=$?
  if [ "$rc" = 0 ] && grep -q 'installation completed' "$W/$bl.out" && grep -q '^SOURCED-RETURNED rc=0' "$W/$bl.out"; then
    facts="$facts $bl=ok"
  else
    facts="$facts $bl=rc$rc"; bad=$((bad + 1)); sed 's/^/  | /' "$W/$bl.out"
  fi
done
if [ "$bad" = 0 ]; then
  echo "kept-loaders: $SIDE-expectation-met (${facts# })"; exit 0
fi
echo "kept-loaders: UNEXPECTED on $SIDE (${facts# })"; exit 1

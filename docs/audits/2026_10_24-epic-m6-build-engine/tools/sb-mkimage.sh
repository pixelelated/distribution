#!/usr/bin/env bash
# E1 (#652, #827, F-16): run the real scripts/mkimage and the shared bootloader
# hook, as they are at a commit (or in the working tree), over fixture files in
# the scratch directory given, with SYSTEM either fitting the FAT partition or
# too large for it. Prints the script's last lines, its exit status and what
# landed in the fixture target/. Nothing is written outside the scratch
# directory; mtools, populatefs and xmlstarlet are copied read-only from a
# build root's toolchain (the host has none), as P3 copied xmlstarlet.
#   [TRACE=1] sb-mkimage.sh <scratch-dir> <qcom-abl|arm-efi> <fit|overflow|nearfull|noabl> [commit|WORKTREE] [toolchain]
# overflow: SYSTEM larger than part1; nearfull: kernel and SYSTEM under part1's
# raw size but over what the FAT can hold, so the copy itself fails; noabl:
# the hook's ABL file is missing, so the hook's own copy fails.
# No ROCKNIX device uses arm-efi; that run takes SM8550's config with the
# bootloader set to arm-efi, a synthetic input.
set -euo pipefail
S="${1:?scratch directory}"; BL="${2:?qcom-abl or arm-efi}"; MODE="${3:?fit, overflow, nearfull or noabl}"
R="${4:-8ebaf8daad}"
TC="${5:-/workspace/repos/rocknix.worktrees/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.aarch64/toolchain}"
REPO="$(git rev-parse --show-toplevel)"
W="$S/run-$BL-$MODE-$(date +%s%N)"; mkdir -p "$W/bin" "$W/tree" "$W/target" "$W/release/target" "$W/release/3rdparty/bootloader/boot" "$W/tc"
for f in bin/mtools bin/xmlstarlet sbin/populatefs; do cp "$TC/$f" "$W/bin/"; done
for n in mcopy mformat mmd; do ln -s mtools "$W/bin/$n"; done
FILES="scripts/mkimage projects/ROCKNIX/bootloader/mkimage projects/ROCKNIX/config.xml config/functions distributions/ROCKNIX/config/functions"
if [ "$R" = WORKTREE ]; then
  for f in $FILES; do mkdir -p "$W/tree/$(dirname "$f")"; cp "$REPO/$f" "$W/tree/$f"; done
else
  git -C "$REPO" archive "$R" $FILES | tar -x -C "$W/tree"
fi
# the fixture's inputs: a kernel, a SYSTEM that fits a 4 MiB FAT or does not, their md5s, the ABL
head -c 65536 /dev/zero > "$W/target/fixture-1.kernel"
case "$MODE" in overflow) sz=6291456 ;; nearfull) sz=4100000 ;; *) sz=1048576 ;; esac
head -c "$sz" /dev/zero > "$W/target/fixture-1.system"
echo "fixture-2  KERNEL" > "$W/release/target/KERNEL.md5"; echo "fixture-3  SYSTEM" > "$W/release/target/SYSTEM.md5"
[ "$MODE" = noabl ] || head -c 4096 /dev/zero > "$W/release/3rdparty/bootloader/rocknix_abl"
cd "$W/tree"
set +e
env -i PATH="$W/bin:/usr/sbin:/usr/bin:/sbin:/bin" HOME="$W" \
  SYSTEM_SIZE=4 SYSTEM_PART_START=2048 STORAGE_SIZE=4 TARGET_IMG="$W/target" IMAGE_NAME=fixture-1 \
  BUILD_NAME=fixture-1 BOOTLOADER="$BL" DISTRO=ROCKNIX DISTRO_BOOTLABEL=FIXTURE DISTRO_DISKLABEL=FIXTURE2 \
  UUID_SYSTEM=0000-0001 UUID_STORAGE=00000000-0000-0000-0000-000000000002 KERNEL_NAME=KERNEL \
  RELEASE_DIR="$W/release" PROJECT=ROCKNIX PROJECT_DIR="$W/tree/projects" DEVICE=SM8550 TOOLCHAIN="$W/tc" \
  bash ${TRACE:+-x} scripts/mkimage > "$W/mkimage.out" 2>&1
rc=$?
set -e
tail -4 "$W/mkimage.out" | sed "s#$S#<scratch>#g"
echo "mtools refusals: $(grep -v 'image: An error' "$W/mkimage.out" | grep -c -i -E 'disk full|no free|cannot|no such file|error') ($(grep -v 'image: An error' "$W/mkimage.out" | grep -i -m1 -E 'disk full|no free|cannot|no such file' | sed "s#$S#<scratch>#g" | cut -c1-90))"
echo "error path: $(grep -c 'image: An error has occurred' "$W/mkimage.out")"
[ -z "${TRACE:-}" ] || echo "trace: $W/mkimage.out ($(grep -c '^+' "$W/mkimage.out") lines)" | sed "s#$S#<scratch>#g"
echo "exit: $rc"
echo "target: $(cd "$W/target" && ls -A | grep -v '^tmp\.' | tr '\n' ' ')"

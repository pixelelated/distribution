#!/bin/bash
# T11 S4 (#1088): dtb_overlay's set path, judged in a fixture /flash.
#
#   dtb-overlay-case.sh <dtb_overlay file> <unfixed|fixed> <case>
#
# The script runs under bash, as on the image (ROCKNIX's busybox package
# relinks /usr/bin/sh to bash), inside bwrap with a tmpfs root holding:
#   /flash/extlinux/extlinux.conf and /flash/overlays/*.dtbo (fixtures);
#   /etc/profile.d/001-functions, a stub whose get_setting/set_setting keep
#     each value in /state/<key>;
#   a mount stub first on PATH, which succeeds or, for remount-fail, fails
#     (and /flash/extlinux is mode 555 so sed -i fails as on a read-only fs).
# Cases (positives fail on the unfixed script and hold on the fixed one):
#   remount-fail  set driver-gpu driver-gpu-panthor.dtbo with the remount
#                 failing: unfixed exits 0; fixed exits non-zero and leaves
#                 the setting as it was.
#   none-clear    set driver-gpu None with no driver-gpu overlay installed
#                 and the setting holding a stale value: unfixed exits 1
#                 ("dtbo doesn't exist: None"); fixed exits 0, the setting
#                 None and no FDTOVERLAYS line.
#   spaced-arg    set driver-gpu "x y": unfixed prints a shell test error on
#                 stderr; fixed refuses without one ("dtbo doesn't exist").
#   empty-arg     set driver-gpu "": the same expectation as spaced-arg.
#   dash-arg      set driver-gpu -o: fixed refuses without a test error;
#                 unfixed is recorded (bash reads `[ -o = None ]` as a
#                 comparison, so it may not error) and must not exit 0.
# Control (the same on both sides):
#   normal        set driver-gpu driver-gpu-panthor.dtbo with the remount
#                 working: exit 0, the setting written, and the FDTOVERLAYS
#                 line naming /overlays/driver-gpu-panthor.dtbo.
# Writes only under $TMPDIR; prints one verdict line last; exits 0 when the
# side's expectation is met, 1 when not, 2 when it cannot run.
set -u
F=${1:?dtb_overlay file}; SIDE=${2:?unfixed or fixed}; CASE=${3:?case}
[ -f "$F" ] || { echo "dtb-overlay-case: CANNOT -- no file $F"; exit 2; }
command -v bwrap >/dev/null || { echo "dtb-overlay-case: CANNOT -- no bwrap"; exit 2; }
[ "$(id -u)" != 0 ] || { echo "dtb-overlay-case: CANNOT -- root ignores mode 555"; exit 2; }
W=$(mktemp -d "${TMPDIR:?}/s4-dtbo.XXXXXX") || exit 2
mkdir -p "$W/flash/extlinux" "$W/flash/overlays" "$W/state" "$W/stub" "$W/profile.d"
cat > "$W/flash/extlinux/extlinux.conf" <<'CONF'
LABEL ROCKNIX
  LINUX /KERNEL
  FDT /dtb.img
  APPEND boot=LABEL=ROCKNIX disk=LABEL=STORAGE
CONF
cat > "$W/profile.d/001-functions" <<'FUNCS'
get_setting() { [ -f "/state/$1" ] && cat "/state/$1"; return 0; }
set_setting() { printf '%s' "$2" > "/state/$1"; }
FUNCS
mount_rc=0
case "$CASE" in
  remount-fail) mount_rc=1; : > "$W/flash/overlays/driver-gpu-panthor.dtbo"; ARGS=(set driver-gpu driver-gpu-panthor.dtbo) ;;
  normal) : > "$W/flash/overlays/driver-gpu-panthor.dtbo"; ARGS=(set driver-gpu driver-gpu-panthor.dtbo) ;;
  none-clear) : > "$W/flash/overlays/rk3566-undervolt-cpu-l1.dtbo"; printf '%s' 'driver-gpu-panthor.dtbo' > "$W/state/system.driver-gpu"
              printf '  FDTOVERLAYS /overlays/driver-gpu-panthor.dtbo \n' >> "$W/flash/extlinux/extlinux.conf"; ARGS=(set driver-gpu None) ;;
  spaced-arg) : > "$W/flash/overlays/driver-gpu-panthor.dtbo"; ARGS=(set driver-gpu "x y") ;;
  empty-arg) : > "$W/flash/overlays/driver-gpu-panthor.dtbo"; ARGS=(set driver-gpu "") ;;
  dash-arg) : > "$W/flash/overlays/driver-gpu-panthor.dtbo"; ARGS=(set driver-gpu -o) ;;
  *) echo "dtb-overlay-case: CANNOT -- unknown case $CASE"; exit 2 ;;
esac
printf '#!/bin/sh\necho "mount-stub: $*" >&2\nexit %s\n' "$mount_rc" > "$W/stub/mount"; chmod +x "$W/stub/mount"
# A missing and an empty setting both read as no value (get_setting prints nothing).
setting() { v=$(cat "$W/state/system.driver-gpu" 2>/dev/null); printf '%s' "${v:-(unset)}"; }
before_setting=$(setting)
[ "$CASE" = remount-fail ] && { chmod 444 "$W/flash/extlinux/extlinux.conf"; chmod 555 "$W/flash/extlinux"; }
bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib \
  --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin --proc /proc --dev /dev --tmpfs /tmp \
  --dir /etc --ro-bind "$W/profile.d" /etc/profile.d --bind "$W/flash" /flash --bind "$W/state" /state \
  --ro-bind "$W/stub" /stub --ro-bind "$F" /dtb_overlay --setenv PATH /stub:/usr/bin:/usr/sbin \
  bash /dtb_overlay "${ARGS[@]}" > "$W/out" 2> "$W/err"
rc=$?
chmod 755 "$W/flash/extlinux" 2>/dev/null; chmod 644 "$W/flash/extlinux/extlinux.conf" 2>/dev/null
after_setting=$(setting)
line=$(grep FDTOVERLAYS "$W/flash/extlinux/extlinux.conf" || true)
testerr=no; grep -q -E '\[: |too many arguments|unary operator|binary operator' "$W/err" && testerr=yes
sed 's/^/  | out: /' "$W/out"; sed 's/^/  | err: /' "$W/err"
echo "  | extlinux: ${line:-(no FDTOVERLAYS line)}"
facts="rc=$rc setting=${before_setting}->${after_setting} testerr=$testerr"
case "$SIDE:$CASE" in
  unfixed:remount-fail) [ "$rc" = 0 ] && ok=1 || ok=0 ;;
  fixed:remount-fail)   [ "$rc" != 0 ] && [ "$after_setting" = "$before_setting" ] && ok=1 || ok=0 ;;
  unfixed:none-clear)   [ "$rc" = 1 ] && grep -q "dtbo doesn't exist: None" "$W/out" && ok=1 || ok=0 ;;
  fixed:none-clear)     [ "$rc" = 0 ] && [ "$after_setting" = None ] && [ -z "$line" ] && ok=1 || ok=0 ;;
  unfixed:spaced-arg)   [ "$testerr" = yes ] && ok=1 || ok=0 ;;
  fixed:spaced-arg)     [ "$rc" != 0 ] && [ "$testerr" = no ] && grep -q "dtbo doesn't exist: x y" "$W/out" && ok=1 || ok=0 ;;
  unfixed:empty-arg)    [ "$testerr" = yes ] && ok=1 || ok=0 ;;
  fixed:empty-arg)      [ "$rc" != 0 ] && [ "$testerr" = no ] && grep -q "dtbo doesn't exist: $" "$W/out" && ok=1 || ok=0 ;;
  unfixed:dash-arg)     [ "$rc" != 0 ] && ok=1 || ok=0 ;;
  fixed:dash-arg)       [ "$rc" != 0 ] && [ "$testerr" = no ] && grep -q "dtbo doesn't exist: -o" "$W/out" && ok=1 || ok=0 ;;
  *:normal)             [ "$rc" = 0 ] && [ "$after_setting" = driver-gpu-panthor.dtbo ] && printf '%s' "$line" | grep -q '/overlays/driver-gpu-panthor.dtbo' && ok=1 || ok=0 ;;
  *) echo "dtb-overlay-case: CANNOT -- side $SIDE"; exit 2 ;;
esac
if [ "$ok" = 1 ]; then
  echo "dtb-overlay-case $CASE: $SIDE-expectation-met ($facts)"; exit 0
fi
echo "dtb-overlay-case $CASE: UNEXPECTED on $SIDE ($facts)"; exit 1

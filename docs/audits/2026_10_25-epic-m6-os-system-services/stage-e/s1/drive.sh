#!/bin/bash
# T22 stream S1 (#1105, #1106): scripts/init's update path, on the host.
#   T22_BUSYBOX=<the initramfs busybox> drive.sh <path to scripts/init> unfixed|fixed
# The initramfs runs /init under busybox ash with busybox's applets, so the
# case does too: $T22_BUSYBOX is a copy of the image's initramfs busybox
# (1.36.1; the README names where it came from), its applets installed as
# links in scratch and put first on PATH. Only the file's function
# definitions are loaded, with every absolute path the update path uses
# (/flash, /storage, /sysroot, /update, /tmp, /dev/console, /dev/kmsg)
# rewritten under a scratch directory in $TMPDIR; every command that could
# touch the host is stubbed after the source (reboot, do_reboot, poweroff,
# mount, umount, losetup, mountpoint, sync, avfsd). A stub dd writes 100
# bytes and fails when its output path contains FAIL_ON. check_update runs
# over a staged .tar:
#   a  the kernel write fails (room for a second copy on /flash)
#   b  the SYSTEM write fails (room)
#   c  every write succeeds
#   d  the staged update's md5 is wrong
#   e  the kernel write fails with no room for a second copy
#   f to j  the five other rejections that go on to a normal start:
#      f updating disabled (netboot), g the installed kernel missing,
#      h the update without a SYSTEM, i an incompatible update, j no room
# One line per case, then one verdict line.
set -u
src=${1:?scripts/init}; want=${2:?unfixed|fixed}
BB=${T22_BUSYBOX:?set T22_BUSYBOX to the initramfs busybox}
T=$(mktemp -d "${TMPDIR:?}/s1.XXXXXX")
# This busybox has no --install and its ash no `command` builtin; its ash
# runs its own applets first, so only `busybox` itself is put on PATH.
mkdir -p "$T/bin"; ln -sf "$BB" "$T/bin/busybox"

mkfuncs() {   # the file's functions, paths rewritten under $1
  awk '/^[A-Za-z_][A-Za-z0-9_]*\(\) *\{/{p=1} p{print} p&&/^\}/{p=0; print ""}' "$src" |
    sed -E "s#(^|[^A-Za-z0-9_.\$/])/(flash|storage|sysroot|update|tmp)([/ \"'\$;)&|]|\$)#\1$1/\2\3#g; s#/dev/(console|kmsg)#$1/\1#g"
}

run_case() {  # run_case <case> -> prints "<case>|<facts>"
  local c=$1 W="$T/$1" FAIL_ON="" SMALL=""
  mkdir -p "$W/flash" "$W/storage/.update" "$W/sysroot" "$W/update" "$W/tmp" "$W/pkg/dist/target"
  head -c 4096 /dev/urandom > "$W/flash/KERNEL"; head -c 8192 /dev/urandom > "$W/flash/SYSTEM"
  md5sum < "$W/flash/KERNEL" > "$W/old.k"; md5sum < "$W/flash/SYSTEM" > "$W/old.s"
  head -c 5000 /dev/urandom > "$W/pkg/dist/target/KERNEL"; head -c 9000 /dev/urandom > "$W/pkg/dist/target/SYSTEM"
  md5sum < "$W/pkg/dist/target/KERNEL" > "$W/new.k"; md5sum < "$W/pkg/dist/target/SYSTEM" > "$W/new.s"
  ( cd "$W/pkg/dist/target" && echo "$(md5sum < KERNEL | cut -d' ' -f1)  target/KERNEL" > KERNEL.md5 && echo "$(md5sum < SYSTEM | cut -d' ' -f1)  target/SYSTEM" > SYSTEM.md5 )
  [ "$c" = d ] && echo "00000000000000000000000000000000  target/SYSTEM" > "$W/pkg/dist/target/SYSTEM.md5"
  [ "$c" = g ] && rm -f "$W/flash/KERNEL"
  [ "$c" = h ] && rm -f "$W/pkg/dist/target/SYSTEM" "$W/pkg/dist/target/SYSTEM.md5"
  TAR="$W/storage/.update/t22-@DISTRONAME@-update.tar"
  ( cd "$W/pkg" && tar -cf "$TAR" dist )
  mkfuncs "$W" > "$W/funcs.sh"
  : > "$W/calls"   # a case that records nothing still has a count of 0
  case $c in a|e) FAIL_ON=KERNEL ;; b) FAIL_ON=SYSTEM ;; esac
  [ "$c" = e ] && SMALL=1
  local EXTRA=""
  case $c in
    f) EXTRA='UPDATE_DISABLED=yes' ;;
    i) EXTRA='check_is_compatible() { return 1; }' ;;
    j) EXTRA='FLASH_FREE_MIN=100'; SMALL=1 ;;
  esac
  cat > "$W/case.sh" <<EOF
cd "$W"
. "$W/funcs.sh"
rec() { echo "\$*" >> "$W/calls"; }
done_() { echo "\$1" > "$W/rc"; exit 0; }
reboot() { rec reboot; done_ 0; }
do_reboot() { rec do_reboot; done_ 0; }
poweroff() { rec poweroff; done_ 0; }
mount() { rec mount "\$@"; }
umount() { rec umount "\$@"; }
sync() { :; }
losetup() { [ "\${1:-}" = -a ] && return 0; rec losetup "\$@"; }
mountpoint() { [ "\${2:-}" = "$W/storage" ]; }
avfsd() { return 0; }
hdmi_con() { :; }; progress() { :; }; clear() { :; }; debug_msg() { :; }
StartProgress() { echo "PROGRESS: \$*"; }; StopProgress() { :; }; display_versions() { :; }; check_out_of_space() { :; }
mount_part() { rec mount_part "\$@"; }
check_is_compatible() { return 0; }
[ -n "$SMALL" ] && df() { printf 'F 1K-blocks Used Available Use%% M\nx 100 90 10 90%% /f\n'; }
dd() {
  o=; i=
  for a in "\$@"; do case \$a in of=*) o=\${a#of=} ;; if=*) i=\${a#if=} ;; esac; done
  if [ -n "$FAIL_ON" ]; then case "\$o" in *"$FAIL_ON"*) head -c 100 "\$i" > "\$o"; return 1 ;; esac; fi
  "$BB" dd "\$@"
}
UPDATE_ROOT="$W/storage/.update"; UPDATE_DIR="\$UPDATE_ROOT"; UPDATE_KERNEL=KERNEL; UPDATE_SYSTEM=SYSTEM
IMAGE_KERNEL=KERNEL; IMAGE_SYSTEM=SYSTEM; FLASH_FREE_MIN=0; disk="LABEL=STORAGE"; boot="LABEL=ROCKNIX"
$EXTRA
check_update > "$W/out" 2>&1
done_ \$?
EOF
  PATH="$T/bin:$PATH" "$BB" sh "$W/case.sh" > /dev/null 2> "$W/sub.err"
  local k s
  k=$(cmp_md5 "$W/flash/KERNEL" "$W/old.k" "$W/new.k"); s=$(cmp_md5 "$W/flash/SYSTEM" "$W/old.s" "$W/new.s")
  printf '%s|kernel=%s system=%s complete=%s failed_named=%s umount_storage=%s staged=%s rejected=%s rc=%s\n' "$c" "$k" "$s" \
    "$(grep -c 'Update complete' "$W/out")" "$(grep -c -E 'FAILED: .*(KERNEL|SYSTEM)' "$W/out")" \
    "$(grep -c "^umount $W/storage\$" "$W/calls" 2>/dev/null || true)" \
    "$([ -e "$TAR" ] && echo kept || echo gone)" \
    "$([ -e "$TAR.rejected" ] && [ -s "$TAR.rejected.reason" ] && echo "yes" || echo no)" "$(cat "$W/rc" 2>/dev/null || echo none)"
  [ -n "${T22_SHOW:-}" ] && { echo "--- $c out:"; sed 's/^/    /' "$W/out"; echo "--- $c calls:"; sed 's/^/    /' "$W/calls" 2>/dev/null; }
}
cmp_md5() { local h; [ -e "$1" ] || { echo absent; return; }; h=$(md5sum < "$1"); [ "$h" = "$(cat "$2")" ] && echo old && return; [ "$h" = "$(cat "$3")" ] && echo new && return; echo torn; }

declare -A R
for c in a b c d e f g h i j; do line=$(run_case $c); echo "$line" | sed -n '2,$p'; line=$(echo "$line" | head -1); R[$c]=${line#*|}; echo "$c: ${R[$c]}"; done
[ -n "${T22_KEEP:-}" ] && echo "kept $T" || rm -rf "${T:?}"
get() { local v=${R[$1]}; v=${v#*$2=}; echo "${v%% *}"; }
rejections() {  # the five other rejections, f to j, each as the mode expects
  local x
  for x in f g h i j; do
    if [ "$1" = unfixed ]; then [ "$(get $x umount_storage)" -ge 1 ] && [ "$(get $x staged)" = gone ] || return 1
    else [ "$(get $x umount_storage)" = 0 ] && [ "$(get $x rejected)" = yes ] || return 1; fi
  done
}
case "$want" in
  unfixed)
    if [ "$(get a complete)" = 1 ] && [ "$(get a kernel)" = torn ] && [ "$(get b complete)" = 1 ] && [ "$(get b system)" = torn ] \
       && [ "$(get c kernel)" = new ] && [ "$(get c system)" = new ] && [ "$(get d umount_storage)" -ge 1 ] && [ "$(get d staged)" = gone ] \
       && rejections unfixed; then
      echo "s1: unfixed-expectation-met (a failed write still says Update complete and leaves a torn file; each of the six rejections unmounts /storage and deletes the update)"; exit 0; fi ;;
  fixed)
    if [ "$(get a complete)" = 0 ] && [ "$(get a kernel)" = old ] && [ "$(get a failed_named)" -ge 1 ] && [ "$(get a umount_storage)" = 0 ] \
       && [ "$(get b complete)" = 0 ] && [ "$(get b system)" = old ] && [ "$(get b kernel)" = old ] && [ "$(get b failed_named)" -ge 1 ] \
       && [ "$(get c complete)" = 1 ] && [ "$(get c kernel)" = new ] && [ "$(get c system)" = new ] \
       && [ "$(get d umount_storage)" = 0 ] && [ "$(get d rejected)" = yes ] \
       && [ "$(get e complete)" = 0 ] && [ "$(get e failed_named)" -ge 1 ] \
       && rejections fixed; then
      echo "s1: fixed-expectation-met (a failed write is named and leaves the previous pair; success unchanged; each of the six rejections keeps /storage and the update as .rejected)"; exit 0; fi ;;
esac
echo "s1: UNEXPECTED ($want)"; exit 1

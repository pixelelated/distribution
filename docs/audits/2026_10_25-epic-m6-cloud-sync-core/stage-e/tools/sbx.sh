#!/bin/bash
# T16 host leads: run "$@" in a bwrap sandbox shaped like the device for the read scripts.
#   ROOT  -- a root from mkroot.sh;  CELL -- the cell's directory (storage/, log/, varrun/, run/)
#   RO=1  -- remount / read-only after the binds, as the image's squashfs is
# The host's network (the QA WebDAV on 127.0.0.1); its own pid namespace, so pidof and ps see
# only this sandbox's processes, and whatever is left when the command ends dies with it.
set -u
: "${ROOT:?}" "${CELL:?}"
DONOR=/workspace/artifacts/m6-donor/1a0266484423/image/system
mkdir -p "${CELL}/storage" "${CELL}/log" "${CELL}/varrun" "${CELL}/run"
RO_ARGS=()
[ "${RO:-0}" = 1 ] && RO_ARGS=(--remount-ro /)
# SBX_EXTRA: more bwrap mounts after the binds, word-split (stage E: a full card is
# "--size 32768 --tmpfs /storage/.config", a tmpfs the cell then fills).
EXTRA=()
[ -n "${SBX_EXTRA:-}" ] && read -r -a EXTRA <<< "${SBX_EXTRA}"
# SBX_LATE: bwrap arguments after the sandbox's own /dev, /proc and /tmp (stage E's S6: a
# read-only /tmp is "--remount-ro /tmp", which must follow the --tmpfs /tmp it remounts).
LATE=()
[ -n "${SBX_LATE:-}" ] && read -r -a LATE <<< "${SBX_LATE}"
exec bwrap --die-with-parent --unshare-pid --tmpfs / \
    --ro-bind /usr /host/usr --ro-bind "${DONOR}" /donor \
    --tmpfs /usr --ro-bind /usr/lib /usr/lib --ro-bind /usr/lib64 /usr/lib64 --ro-bind /usr/share /usr/share \
    --ro-bind /usr/libexec /usr/libexec \
    --ro-bind "${ROOT}/usr/bin" /usr/bin --ro-bind "${ROOT}/usr/sbin" /usr/sbin --ro-bind "${ROOT}/usr/config" /usr/config \
    --symlink usr/bin /bin --symlink usr/sbin /sbin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
    --dir /etc --ro-bind /etc/passwd /etc/passwd --ro-bind /etc/group /etc/group \
    --ro-bind "${DONOR}/etc/os-release" /etc/os-release \
    --bind "${CELL}/storage" /storage --bind "${CELL}/log" /var/log --bind "${CELL}/varrun" /var/run \
    --bind "${CELL}/run" /run --ro-bind-try "${CELL}/drv" /drv \
    "${EXTRA[@]}" \
    --dev /dev --proc /proc --tmpfs /tmp "${LATE[@]}" \
    --clearenv --setenv PATH /usr/bin:/usr/sbin --setenv HOME /storage --setenv TZ UTC --setenv TERM dumb \
    "${RO_ARGS[@]}" "$@"

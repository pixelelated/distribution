#!/bin/bash
# T16 stage E (#663): the host leads' mkroot.sh with one change -- SRC picks the scripts:
#   SRC=8ebaf8daad (the default: the unfixed bytes, by git show) or SRC=tree (the worktree's files,
#   the stream's fix). Builds $1 (a NEW directory; nothing is removed here):
#   usr/bin   -- the image's busybox applet links from the donor root (its /usr/bin, 146
#                links) -> the donor busybox; the donor rclone; the scripts at 8ebaf8daad;
#                every other name -> the host's, GNU coreutils' gnu<name> where the host
#                has one (the image's coreutils is GNU 9.4; the host's default is uutils)
#   usr/sbin  -- the host's (ip: iproute2 on the host; not in the donor)
#   usr/config -- the four files package.mk installs there, at 8ebaf8daad
set -eu
OUT="${1:?new root directory}"
DONOR=/workspace/artifacts/m6-donor/1a0266484423/image/system
WT=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663
REL=projects/ROCKNIX/packages/network/rclone/sources
[ ! -e "${OUT}" ] || { echo "exists: ${OUT}" >&2; exit 2; }
mkdir -p "${OUT}/usr/bin" "${OUT}/usr/sbin" "${OUT}/usr/config"
for p in /usr/bin/*; do
    n=${p##*/}
    if [ -x "/usr/bin/gnu${n}" ]; then ln -s "/host/usr/bin/gnu${n}" "${OUT}/usr/bin/${n}"
    else ln -s "/host/usr/bin/${n}" "${OUT}/usr/bin/${n}"; fi
done
for p in /usr/sbin/*; do ln -s "/host/usr/sbin/${p##*/}" "${OUT}/usr/sbin/${p##*/}"; done
nbb=0
for p in "${DONOR}"/usr/bin/*; do
    n=${p##*/}
    if [ -L "${p}" ] && [ "$(readlink "${p}")" = busybox ]; then
        ln -sfn /donor/usr/bin/busybox "${OUT}/usr/bin/${n}"; nbb=$((nbb + 1))
    fi
done
ln -sfn /donor/usr/bin/busybox "${OUT}/usr/bin/busybox"
# /usr/bin/sh is bash on the image (projects/ROCKNIX/packages/sysutils/busybox/package.mk's
# post_install relinks it), not busybox and not the host's dash (stage E, S7: found when
# cloud_net_ready's 10# met dash).
ln -sfn /host/usr/bin/bash "${OUT}/usr/bin/sh"
ln -sfn /donor/usr/bin/rclone "${OUT}/usr/bin/rclone"
for s in cloud_backup cloud_restore cloud_capture cloud_net_ready cloud_saves_root cloud_sync_helper \
         cloud_sync_cleanup_duplicates.sh rasteratops-settings-archive cloud_remote cloud_device_id \
         cloud_log_scrub cloud_scan cloud_connections.py; do
    if [ "${SRC:-8ebaf8daad}" = tree ]; then cp "${WT}/${REL}/${s}" "${OUT}/usr/bin/${s}.new"
    else git -C "${WT}" show "${SRC:-8ebaf8daad}:${REL}/${s}" > "${OUT}/usr/bin/${s}.new"; fi
    mv -f "${OUT}/usr/bin/${s}.new" "${OUT}/usr/bin/${s}"; chmod 755 "${OUT}/usr/bin/${s}"
done
for c in cloud_sync.conf cloud_sync.conf.defaults cloud_sync-rules.txt cloud_sync-rules.txt.defaults; do
    if [ "${SRC:-8ebaf8daad}" = tree ]; then cp "${WT}/${REL}/${c}" "${OUT}/usr/config/${c}"
    else git -C "${WT}" show "${SRC:-8ebaf8daad}:${REL}/${c}" > "${OUT}/usr/config/${c}"; fi
done
echo "${SRC:-8ebaf8daad}" > "${OUT}/SRC"
echo "root ${OUT}: busybox links ${nbb}; scripts from ${SRC:-8ebaf8daad}:"
( cd "${OUT}/usr/bin" && sha256sum cloud_backup cloud_restore cloud_capture cloud_net_ready cloud_saves_root \
    cloud_sync_helper cloud_sync_cleanup_duplicates.sh rasteratops-settings-archive )
( cd "${OUT}/usr/config" && sha256sum ./* )

#!/bin/bash
# #1068's shims, built into a directory you give it (under $TMPDIR):
#   <dir>/obscure/rclone  -- `rclone obscure` exits 1; every other subcommand
#                            is passed to the real rclone
#   <dir>/chmod/chmod     -- does nothing and exits 0
# Put one of them first on PATH for a run of tools/cloud-test-backend:
#   PATH=<dir>/obscure:$PATH tools/cloud-test-backend --backend webdav rclone-conf
#   PATH=<dir>/chmod:$PATH  CLOUD_QA_STATE=<fresh dir> tools/cloud-test-backend --backend s3 ls
set -euo pipefail
dir="${1:?usage: build.sh <directory, under \$TMPDIR>}"
case "${dir}" in "${TMPDIR:?TMPDIR is not set}"/*) ;; *) echo "build.sh: ${dir} is not under \$TMPDIR (${TMPDIR})" >&2; exit 2 ;; esac
real="$(command -v rclone)" || { echo "build.sh: no rclone on PATH" >&2; exit 2; }
mkdir -p "${dir}/obscure" "${dir}/chmod"
printf '#!/bin/sh\n[ "$1" = obscure ] && exit 1\nexec %s "$@"\n' "${real}" > "${dir}/obscure/rclone"
printf '#!/bin/sh\nexit 0\n' > "${dir}/chmod/chmod"
chmod +x "${dir}/obscure/rclone" "${dir}/chmod/chmod"
echo "shims built: ${dir}/obscure/rclone (obscure fails), ${dir}/chmod/chmod (a no-op)"

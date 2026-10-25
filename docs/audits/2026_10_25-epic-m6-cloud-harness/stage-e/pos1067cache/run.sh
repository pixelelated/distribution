#!/usr/bin/env bash
# #1067's second positive: does the SFTP endpoint show a fixture put after
# it started? The content tier's scan call, verbatim, with the image's own
# rclone as the client.
#
#   run.sh <cloud-test-backend> unfixed|fixed
#
# "unfixed" here is the tool at 22099cb7f9 (rclone serve sftp, default
# five-minute directory cache); the 8a2518fa44 clone serves sshd and has no
# cache, so it is not this case's control. Client: $T13_CLIENT, default the
# image's rclone retained under /workspace/artifacts/m6-donor. Writes only
# under $TMPDIR; brings the endpoint down before it exits.
set -u
tool=${1:?tool}; want=${2:?unfixed|fixed}
client=${T13_CLIENT:-/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone}
[ -x "${client}" ] || { echo "pos1067cache: UNEXPECTED (no client at ${client})"; exit 2; }
W=${TMPDIR:?}/pos1067cache
rm -rf "${W:?}/state"
mkdir -p "${W}/fx/ROMs/vectrex" "${W}/fx/ROMs/definitely-not-a-system"
printf 'rom\n' > "${W}/fx/ROMs/vectrex/game.vec"
printf 'x\n' > "${W}/fx/ROMs/definitely-not-a-system/x.rom"
export CLOUD_QA_STATE="${W}/state" CLOUD_QA_PORT=${CLOUD_QA_PORT:-9083}
B() { "${tool}" --backend sftp "$@"; }
trap 'B down >/dev/null 2>&1' EXIT
B up >/dev/null || { echo "pos1067cache: UNEXPECTED (up failed)"; exit 2; }
B rclone-conf > "${W}/conf" 2>/dev/null; chmod 600 "${W}/conf"
sed -i 's/^host = .*/host = 127.0.0.1/' "${W}/conf"
B put "${W}/fx" CONTENT >/dev/null      # after up, whose login check listed /
"${client}" --config "${W}/conf" lsf -R --files-only --format sp --separator '|' \
  qa-cloud:/CONTENT/ROMs/ --contimeout 15s --timeout 30s --low-level-retries 3 --retries 1 \
  > "${W}/out" 2>/dev/null
rc=$?; n=$(grep -c . "${W}/out")
echo "scan rc=${rc}, files listed ${n} of 2"
case "${want}:${rc}:${n}" in
  unfixed:3:0) echo "pos1067cache: unfixed-expectation-met (put fixture hidden, rc 3)"; exit 0 ;;
  fixed:0:2)   echo "pos1067cache: fixed-expectation-met (put fixture listed, rc 0)"; exit 0 ;;
  *)           echo "pos1067cache: UNEXPECTED (${want}: rc ${rc}, ${n} listed)"; exit 1 ;;
esac

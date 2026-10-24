#!/usr/bin/env bash
# E5b (#652, #833): scripts/image's sidecar block (from "# Record the identity"
# to "# Create legacy sym links", the markers tools/build-identity-test uses),
# lifted from a commit or the working tree and run under set -e with the EXIT
# trap config/functions sets (onexitcleanup, stubbed to print the status it
# sees), then a step after it that fails (do_mkimage's place) or succeeds.
#   sb-image-sidecar.sh <scratch-dir> [commit|WORKTREE]
set -u
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
W="$S/run-$(date +%s%N)"; mkdir -p "$W/target"
if [ "$R" = WORKTREE ]; then cat "$REPO/scripts/image"; else git -C "$REPO" show "$R:scripts/image"; fi \
  | awk '/^# Record the identity/{on=1} /^# Create legacy sym links/{on=0} on' > "$W/sidecar.sh"
for step in fails succeeds; do
  rm -f "$W/target/"*
  env -i PATH=/usr/bin:/bin TARGET_IMG="$W/target" IMAGE_NAME=fixture-1 RELEASE_VERSION=0.0.1-dev \
    BUILD_VERSION=fixture-2 BUILD_TIMESTAMP=20261024T000000Z GIT_HASH=fixture-3 BUILD_DIRTY=no DEVICE=H700 TARGET_ARCH=aarch64 \
    STEP="$step" SIDECAR="$W/sidecar.sh" bash -c '
      set -e
      onexitcleanup() { echo "onexitcleanup sees rc=$?"; }
      trap "onexitcleanup $0" EXIT
      . "$SIDECAR"
      [ "$STEP" = succeeds ]   # the image step after the sidecar
    ' > "$W/out-$step" 2>&1
  rc=$?
  echo "a step after the sidecar $step: exit $rc; $(cat "$W/out-$step" | tr '\n' ' ')sidecar: $(ls "$W/target" | grep -c identity.json)"
done

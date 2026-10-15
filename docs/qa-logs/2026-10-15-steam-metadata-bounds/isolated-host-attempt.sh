#!/bin/bash
set -euo pipefail
test "$(readlink /proc/self/ns/net)" != "$PIX_METADATA_PARENT_NETNS"
ip link set lo up
printf '%s\n' "$(readlink /proc/self/ns/net)" > /tmp/pix-steam-metadata-control-20261015/host02-network-namespace.txt
exec python3 -I -B /tmp/pix-steam-metadata-control-20261015/steam-metadata-control \
  --source '/workspace/repos/rocknix.worktrees/m7-player-setup/projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh' \
  --baseline-source '/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02/projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh' \
  --curl /usr/bin/curl --scope host-curl \
  --out /tmp/pix-steam-metadata-control-20261015/host02

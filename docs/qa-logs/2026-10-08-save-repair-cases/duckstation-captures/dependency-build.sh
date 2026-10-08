#!/bin/bash
# #523 isolated native package build; invoke through this owner's watch-build.
set -euo pipefail
owner=/workspace/repos/rocknix.worktrees/m7-duckstation-deps01
test "$(pwd)" = "$owner"
test "$(git rev-parse HEAD)" = dda2a04aaf411b8bc13aedf5ce44ff33ce4b3d3a
test "$(git branch --show-current)" = build/m7-duckstation-deps01
exec bwrap --die-with-parent --unshare-net --ro-bind / / \
    --bind "$owner" "$owner" --proc /proc --dev /dev --tmpfs /tmp \
    --chdir "$owner" /usr/bin/env \
    PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 \
    SOURCES_DIR="$owner/sources" CCACHE_DISABLE=1 \
    CONCURRENCY_MAKE_LEVEL=1 CONCURRENCY_LOAD=1 VERBOSE=yes \
    scripts/build libcom-err

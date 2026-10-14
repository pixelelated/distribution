#!/bin/bash
# UNRUN. Coordinator allocation only, inside pinned offline builder.
# Host accepted replacement20 SDK is mounted READ-ONLY at the old prefix below.
# Mount current coordinator checkout and this new ES worktree read-only at
# their identical absolute paths. Provide writable private /tmp for header farm.
# No change to frozen cache paths or symlinks. Invoke under admitted/watch owner.
set -eu
ES_COMPOSE=/home/max/Development/emulationstation-next.worktrees/m7-candidate-compose
/workspace/repos/rocknix.worktrees/m7-player-setup/tools/es-syntax-check \
  --root /workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64 \
  --tree "$ES_COMPOSE" --with "$ES_COMPOSE/external" \
  "$ES_COMPOSE/es-app/src/ApiSystem.cpp" \
  "$ES_COMPOSE/es-app/src/ThreadedHasher.cpp" \
  "$ES_COMPOSE/es-app/src/guis/GuiMenu.cpp" \
  "$ES_COMPOSE/es-app/src/guis/GuiWifi.cpp" \
  "$ES_COMPOSE/es-core/src/Settings.cpp"

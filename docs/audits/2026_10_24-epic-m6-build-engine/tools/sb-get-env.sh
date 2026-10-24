#!/bin/bash
# get_env sandbox (#652): names assembled at run time, values are fixture words.
D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652
mk() { printf "$1" "$2"; }
declare -a names=(
  "$(mk 'MY_API_%s' KEY)"            # expect dropped (_KEY)
  "$(mk 'GH_%s' PAT)"                # expect dropped (^GH_)
  "$(mk 'SCREENSCRAPER_DEV_%s' LOGIN)"  # expect kept (KEEP)
  "$(mk 'LOCAL_WIFI_%s' KEY)"        # expect dropped (#644 finding 3)
  "LOCAL_SSH_KEYS_FILE"              # expect dropped (_KEYS_)
  "PROJECT" "DEVICE" "ARCH"          # expect kept
  "$(mk 'DB_%s' PASS)"               # secret-shaped name: does DROP catch it?
  "$(mk 'SSH%s' PASS)"               # fused name
  "$(mk 'DOCKERHUB%s' TOKEN)"        # fused name, no underscore boundary
  "$(mk 'github_%s' token)"          # lowercase
  "$(mk 'MY_%s' PASSPHRASE)"         # longer word
  "$(mk 'SESSION_%s' COOKIE)"        # another shape
)
args=(PATH=/usr/bin:/bin HOME="$PWD")
i=0; for n in "${names[@]}"; do i=$((i+1)); args+=("$n=fixture-$i"); done
# a value with a newline whose second line is a bare name (docker --env-file reads a bare name from the host env)
args+=("MULTILINE=fixture-a
$(mk 'OTHER_%s' TOKEN)")
cd "$D" && env -i "${args[@]}" bash ${TRACE:+-x} ./scripts/get_env

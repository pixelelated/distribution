#!/bin/bash
# get_env sandbox (#652, #830): scripts/get_env, at a commit or from the working
# tree, over a synthetic environment (never the caller's: env -i). Names are
# assembled at run time and values are fixture words, so nothing here is
# credential-shaped at rest. Prints NAMES only -- never a value -- and a verdict.
#   [TRACE=1] sb-get-env.sh <scratch-dir> [commit|WORKTREE]
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$S"; G="$S/get_env-$$"
if [ "$R" = WORKTREE ]; then cp "$REPO/scripts/get_env" "$G"; else git -C "$REPO" show "$R:scripts/get_env" > "$G"; fi
mk() { printf "$1" "$2"; }
drop=(
  "$(mk 'MY_API_%s' KEY)" "$(mk 'GH_%s' PAT)" "$(mk 'LOCAL_WIFI_%s' KEY)" LOCAL_SSH_KEYS_FILE
  "$(mk 'DB_%s' PASS)" "$(mk 'SSH%s' PASS)" "$(mk 'DOCKERHUB%s' TOKEN)" "$(mk 'github_%s' token)"
  "$(mk 'MY_%s' PASSPHRASE)" "$(mk 'SESSION_%s' COOKIE)" "$(mk 'WIFI_%s' PSK)" "$(mk 'app_%s' secret)"
  "$(mk 'ROCKNIX_GH%s' TOKEN)" MULTILINE CRLINE
)
keep=(
  PROJECT DEVICE ARCH "$(mk 'SCREENSCRAPER_DEV_%s' LOGIN)" "$(mk 'CHEEVOS_DEV_%s' LOGIN)"
  "$(mk 'GAMESDB_%s' APIKEY)" "$(mk 'HFS_DEV_%s' LOGIN)"
  BUILD_TIMESTAMP OS_VERSION DIRTY SOURCES_DIR TMPDIR KEYBOARD_LAYOUT XDG_SESSION_TYPE BYPASS_CACHE
)
args=(PATH=/usr/bin:/bin HOME="$S")
i=0
for n in "${drop[@]}" "${keep[@]}"; do
  i=$((i+1))
  case "$n" in
    MULTILINE) args+=("$n=fixture-$i
$(mk 'OTHER_%s' TOKEN)") ;;     # a second line that is a bare name (docker --env-file reads its host value)
    CRLINE) args+=("$n=fixture-$i"$'\r') ;;
    *) args+=("$n=fixture-$i") ;;
  esac
done
cd "$S" && env -i "${args[@]}" bash ${TRACE:+-x} "$G" > "$S/out-$$" 2> "$S/err-$$"; rc=$?
# names only: the part of each line before '=', or the whole line when there is none
names=$(sed -e 's/=.*//' "$S/out-$$" | LC_ALL=C sort -u)
leaked=(); missing=()
for n in "${drop[@]}" "$(mk 'OTHER_%s' TOKEN)"; do grep -qx -- "$n" <<<"$names" && leaked+=("$n"); done
for n in "${keep[@]}"; do grep -qx -- "$n" <<<"$names" || missing+=("$n"); done
echo "exit: $rc"
echo "printed names: $(wc -l <<<"$names")"
echo "leaked (should be dropped): ${leaked[*]:-none}"
echo "missing (should be kept): ${missing[*]:-none}"
echo "notices on stderr (names only): $(sed -e 's/=.*//' "$S/err-$$" | grep -v '^+' | tr '\n' ' ')"
[ -z "${TRACE:-}" ] || echo "trace: $(grep -c '^+' "$S/err-$$") lines in $S/err-$$"
rm -f "$S/out-$$" "$G"

#!/bin/bash
# T16 stage E: rerun a stage-C cell (guest-cycle/host-leads/<cell>/cmd.sh) on a given root, unchanged
# but for two lines: it sources stage-e/tools/lib.sh instead of the scratch lib, and calls
# stage-e/tools/sbx.sh. Usage: ROOT=<root> rerun.sh <cmd.sh>   (output on stdout)
set -u
: "${ROOT:?}"; C="${1:?the cmd.sh of a cell}"
T="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
W=$(mktemp "${TMPDIR:-/workspace/tmp/m6-t16/tmp}/rerun.XXXXXX")
sed -e "s|^\. /workspace/tmp/m6-t16/hl/lib.sh|. ${T}/lib.sh|" -e 's|"\${HL}/sbx.sh"|"${SBX}"|g' "${C}" > "${W}"
echo "(rerun of ${C#*/docs/audits/2026_10_25-epic-m6-cloud-sync-core/} on ROOT=${ROOT}; lib and sandbox: stage-e/tools/)"
ROOT="${ROOT}" bash "${W}"
rc=$?
rm -f "${W}"
exit "${rc}"

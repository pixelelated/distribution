#!/bin/bash
# t10-history-scan.sh -- T10 S1's "Already written" read: the fixed diff reader
# (.githooks/guard-lib's guard_added_lines, the push guard's own call shape)
# run once over a range of the fork's history with the real lists, loaded by
# guard_load as the hooks load them. It prints COUNTS ONLY. Hit labels
# (commit:path:line, never the line) are written to <out-dir>/labels-*.txt and
# printed only when the labels themselves carry no listed word and no
# credential shape.
#   t10-history-scan.sh <repo> <range> <out-dir>
# Exit 0 when the scan ran (whatever it found); 2 when it could not.
set -uo pipefail
REPO="$(cd "${1:?repo}" && pwd)"; RANGE="${2:?range}"; OUT="${3:?out dir}"
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
LIB="$(cd "${HERE}/../../../.." && pwd)/.githooks/guard-lib"
. "${LIB}" || exit 2
guard_load t10-history-scan || exit 2
mkdir -p "${OUT}" || exit 2
cd "${REPO}" || exit 2
start=$(date +%s)
git log -p --text --no-ext-diff --no-textconv --src-prefix=a/ --dst-prefix=b/ --no-renames --diff-merges=first-parent \
  --format='commit %h' "${RANGE}" -- . 2>"${OUT}/log.err" | guard_added_lines > "${OUT}/lines.txt" 2>"${OUT}/reader.err" \
  || { echo "t10-history-scan: the reader could not run ($(head -c 200 "${OUT}/reader.err" "${OUT}/log.err" | tr '\n' ' '))"; exit 2; }
git log --format='commit %h%n%B' "${RANGE}" 2>>"${OUT}/log.err" | awk -v t="${guard_tab}" '/^commit [0-9a-f]+$/ { c = $2; n = 0; next } { n++; print c ":message:" n t $0 }' > "${OUT}/msgs.txt" \
  || { echo "t10-history-scan: the message read failed"; exit 2; }
count() {  # count <file> <patterns> <-i|''> -> the number of lines whose text after the label matches
  local n; n="$(grep -a ${3:+-i} -c -E -e "^([^${guard_tab}]*${guard_tab})+.*(${2})" "$1")"; local rc=$?
  [ "${rc}" -le 1 ] || { echo "t10-history-scan: grep failed (${rc})" >&2; exit 2; }
  printf '%s' "${n}"
}
labels() {  # labels <file> <patterns> <-i|''> <out>
  grep -a ${3:+-i} -E -e "^([^${guard_tab}]*${guard_tab})+.*(${2})" "$1" | sed -E "s/${guard_tab}.*//" > "$4"
}
echo "range ${RANGE}: $(wc -l < "${OUT}/lines.txt") added lines, $(wc -l < "${OUT}/msgs.txt") message lines, $(( $(date +%s) - start )) s"
for kind in lines msgs; do
  c=$(count "${OUT}/${kind}.txt" "${SECRET_PATTERNS}" ''); w=$(count "${OUT}/${kind}.txt" "${FORBIDDEN_PATTERNS}" -i)
  echo "${kind}: credential-shaped ${c}, listed word ${w}"
  labels "${OUT}/${kind}.txt" "${SECRET_PATTERNS}" '' "${OUT}/labels-${kind}-cred.txt"
  labels "${OUT}/${kind}.txt" "${FORBIDDEN_PATTERNS}" -i "${OUT}/labels-${kind}-word.txt"
done
for f in "${OUT}"/labels-*.txt; do
  [ -s "${f}" ] || continue
  if grep -a -q -i -E -e "${FORBIDDEN_PATTERNS}" "${f}" || grep -a -q -E -e "${SECRET_PATTERNS}" "${f}"; then
    echo "$(basename "${f}"): $(wc -l < "${f}") label(s), not printed (a label itself matches a list)"
  else
    echo "$(basename "${f}"):"; sed 's/^/  /' "${f}" | head -40
  fi
done
rm -f "${OUT}/lines.txt" "${OUT}/msgs.txt"
exit 0

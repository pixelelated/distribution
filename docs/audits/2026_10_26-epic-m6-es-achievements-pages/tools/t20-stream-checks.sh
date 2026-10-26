#!/bin/bash
# T20 (#667): the checks every stage-E stream runs before its commit on the
# EmulationStation branch (docs/reviews/briefs/t20-streams.md, "The rules every
# stream keeps"), in one place so no stream skips one:
#
#   RAPIDJSON_INCLUDE_DIR=<dir> bash t20-stream-checks.sh <es tree> <work dir> [app target ...]
#
# 1. es-app/tests/unit's four binaries, by the generated commands
#    (t20-build-tests.sh); their summary lines.
# 2. each tests/app-unit target named (jobs-tests, proxycards-tests,
#    hasher-tests, ...), by t20-build-app-tests.sh, under the sanitizers.
# 3. the non-ASCII comment grep over every file the working tree changes
#    against HEAD, and over the untracked ones (es-code-traps.md: xgettext
#    stops on a non-ASCII byte in a comment near _()).
# 4. the host's g++ -fsyntax-only on each changed .cpp under es-app/src or
#    es-core/src: PASS, or CANNOT with the first missing header named (#1137:
#    the host has no SDL, curl or cross toolchain; tools/es-syntax-check needs
#    a build root, which no lane may read).
# 5. tools/es-untranslated from the distribution checkout, when DIST is set.
#
# Each step's rc on its own line. Writes only under <work dir>. Exit 0 when
# 1, 2 and 3 pass (4's CANNOT and 5's count are reported, not judged here);
# 1 otherwise.
set -uo pipefail
ES=${1:?es tree}; WORK=${2:?work dir}; shift 2
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "${WORK}"
FAIL=0

echo "== 1. es-app/tests/unit"
bash "${HERE}/t20-build-tests.sh" "${ES}" "${WORK}/unit" > "${WORK}/unit.txt" 2>&1
rc=$?
echo "rc ${rc}"
grep -E '^(built|BUILD FAIL|RUN)|test cases|assertions' "${WORK}/unit.txt" | sed 's/^/  /'
[ "${rc}" -eq 0 ] || FAIL=1

for tgt in "$@"; do
  echo "== 2. tests/app-unit ${tgt}"
  bash "${HERE}/t20-build-app-tests.sh" "${ES}" "${WORK}/${tgt}" "${tgt}" > "${WORK}/${tgt}.txt" 2>&1
  rc=$?
  echo "rc ${rc}"
  grep -E '^(built|BUILD FAIL|RUN)' "${WORK}/${tgt}.txt" | sed 's/^/  /'
  [ "${rc}" -eq 0 ] || FAIL=1
done

echo "== 3. the non-ASCII comment grep"
mapfile -t CHANGED < <(cd "${ES}" && { git diff --name-only HEAD; git ls-files --others --exclude-standard; } | sort -u)
printf '  changed: %s\n' "${CHANGED[@]}"
hits=0
for f in "${CHANGED[@]}"; do
  [ -f "${ES}/${f}" ] || continue
  case "${f}" in *.cpp|*.h|*.c) ;; *) continue ;; esac
  n=$(grep -c -P '^\s*//.*[^\x00-\x7F]' "${ES}/${f}")
  [ "${n}" -gt 0 ] && { echo "  NON-ASCII comment: ${f} (${n})"; hits=$((hits + n)); }
done
echo "  ${hits} line(s)"
[ "${hits}" -eq 0 ] || FAIL=1

echo "== 4. the host g++ -fsyntax-only"
for f in "${CHANGED[@]}"; do
  case "${f}" in es-app/src/*.cpp|es-core/src/*.cpp) ;; *) continue ;; esac
  [ -f "${ES}/${f}" ] || continue
  out=$(g++ -std=c++17 -fsyntax-only -I "${ES}/es-app/src" -I "${ES}/es-core/src" -I "${ES}/external" -I "${RAPIDJSON_INCLUDE_DIR:-/nonexistent}" "${ES}/${f}" 2>&1)
  rc=$?
  if [ "${rc}" -eq 0 ]; then
    echo "  PASS ${f}"
  else
    miss=$(printf '%s\n' "${out}" | grep -m1 -o -E "[A-Za-z0-9_/.+-]+\.h(pp)?: No such file or directory" | cut -d: -f1)
    if [ -n "${miss}" ]; then echo "  CANNOT ${f}: ${miss} is not on this host"; else echo "  FAIL ${f}:"; printf '%s\n' "${out}" | grep -m3 'error' | sed 's/^/    /'; FAIL=1; fi
  fi
done

if [ -n "${DIST:-}" ]; then
  echo "== 5. tools/es-untranslated"
  ( cd "${DIST}" && tools/es-untranslated --upstream bccd715707 --es-src "${ES}" ) > "${WORK}/untranslated.txt" 2>&1
  rc=$?
  echo "rc ${rc}"
  grep -m1 "fork string" "${WORK}/untranslated.txt" | sed "s/^/  /"
fi

echo "== result: $([ "${FAIL}" -eq 0 ] && echo PASS || echo FAIL)"
exit "${FAIL}"

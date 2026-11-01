#!/bin/bash
# T37 (#684) stage E: the checks every S1 recipe edit is followed by (the stream brief's rules).
#   t37-edit-checks.sh <parent> <commit>
# Prints: the find positive and tools/pkgcheck by name (the three recipes and the control), bash -n
# on the recipe at <commit>, the non-ASCII / secret / forbidden-term counts over the added lines,
# the :39 line equal or differs between <parent> and <commit> (never the line or its hash), the
# PKG_VERSION / PKG_GIT_CLONE_BRANCH change count, the commit's paths, the recipe's line count, the
# worktree's build roots. Read-only but for tools/pkgcheck's own reads.
set -u
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
PAR=$1; COM=$2; E=projects/ROCKNIX/packages/ui/emulationstation/package.mk; G=/usr/bin/grep
T=/workspace/tmp/m6-t37/tmp
[ "$(git rev-parse HEAD)" = "$(git rev-parse "$COM")" ] || { echo "REFUSED: HEAD is not $COM"; exit 2; }
echo "== $(date -u +%FT%TZ) parent $PAR commit $COM"
for nm in emulationstation es-theme-art-book-next lowerdeck es-theme-no-such-package; do
  echo "find $nm: $(find packages projects -type f -path "*/$nm/package.mk" | tr '\n' ' ')"
  tools/pkgcheck "$nm" > "$T/pk" 2>&1; rc=$?
  echo "pkgcheck $nm rc=$rc lines=$(wc -l < "$T/pk") FAIL-lines=$($G -c -a FAIL "$T/pk") WARN-lines=$($G -c -a WARN "$T/pk")"
done
git show "$COM:$E" > "$T/recipe"; bash -n "$T/recipe"; rc=$?
echo "bash -n recipe rc=$rc; grep -c '' $(/usr/bin/grep -c '' "$T/recipe")"
git diff -U0 "$PAR" "$COM" -- "$E" | $G '^+' | $G -v '^+++' > "$T/added"
echo "added lines: $(wc -l < "$T/added")"
pna=$(printf 'x\xc3\xa9x\n' | LC_ALL=C $G -c -P '[^\x00-\x7F]'); echo "non-ascii planted $pna, added $(LC_ALL=C $G -c -P '[^\x00-\x7F]' "$T/added")"
( . .githooks/secret-patterns; printf '' | $G -E -e "$SECRET_PATTERNS" >/dev/null 2>&1; c=$?; pl=$(printf '%s\n' "$(printf -- '-----BEGIN %s-----' 'OPENSSH PRIVATE KEY')" | $G -c -E -e "$SECRET_PATTERNS"); echo "secret compile rc=$c planted $pl, added $($G -c -E -e "$SECRET_PATTERNS" "$T/added")" )
echo "x planted" | FORBIDDEN_PATTERNS='x planted' tools/forbidden-terms-check --stdin >/dev/null; prc=$?
tools/forbidden-terms-check --stdin < "$T/added" >/dev/null; frc=$?; echo "forbidden planted rc=$prc, added rc=$frc"
a=$(git show "$PAR:$E" | sed -n 39p | sha256sum); b=$(git show "$COM:$E" | sed -n 39p | sha256sum)
echo ":39 $([ "$a" = "$b" ] && echo equal || echo differs)"
echo "PKG_VERSION/PKG_GIT_CLONE_BRANCH changed lines: $(git diff -U0 "$PAR" "$COM" -- "$E" | $G -c -E '^[-+]PKG_(VERSION|GIT_CLONE_BRANCH)=')"
echo "commit paths: $(git show --stat --format= --name-only "$COM" | tr '\n' ' ')"
echo "worktree build roots: $(ls -d build.* 2>/dev/null | wc -l)"
rm -f "$T/recipe" "$T/added" "$T/pk"

#!/bin/bash
# T45 (#692) stage A: the toolchain's own checks on one tree, keyless.
# Every tools/council/run call carries COUNCIL_ENV_FILE=/nonexistent (the wrapper
# sources no key); FIREFLIES_API_KEY, the one credential-named variable in the
# session's environment, is dropped; invoke and efforts --refresh are never run.
#   runs.sh <tree> <outdir>
set -u
T=$1; O=$2; mkdir -p "$O"
export TMPDIR=/workspace/tmp/m6-t45/tmp; mkdir -p "$TMPDIR"
cd "$T" || exit 2
R() { env -u FIREFLIES_API_KEY COUNCIL_ENV_FILE=/nonexistent "$@"; }
echo "== $T at $(git rev-parse --short HEAD) ($(date -u +%T) UTC), node $(node --version), npm $(npm --version)"
s=$(date +%s); R npm install --prefix tools/council > "$O/npm-install.out" 2>&1; rc=$?
echo "npm install rc=$rc $(( $(date +%s) - s ))s; $(tail -3 "$O/npm-install.out" | tr '\n' ' ' | cut -c1-160)"
ls tools/council/node_modules/.bin/tsx >/dev/null && echo "tsx bin present"
R npm ls --prefix tools/council --depth=0 > "$O/npm-ls.out" 2>&1; echo "npm ls rc=$?"; tail -3 "$O/npm-ls.out"
for c in verify-pins drift efforts; do
  s=$(date +%s); R tools/council/run "$c" > "$O/$c.out" 2>&1; rc=$?
  echo "$c rc=$rc $(( $(date +%s) - s ))s: $(tail -1 "$O/$c.out" | cut -c1-140)"
done
s=$(date +%s); R tools/council/run test > "$O/test.out" 2>&1; rc=$?
echo "test rc=$rc $(( $(date +%s) - s ))s; per file (spec reporter's summaries, in run order):"
grep -E '^ℹ (tests|pass|fail|cancelled|skipped) ' "$O/test.out" | paste -d' ' - - - - - | sed 's/^/  /'
echo "  failing lines (✖): $(grep -c '✖' "$O/test.out")"
echo "done $(date -u +%T) UTC"

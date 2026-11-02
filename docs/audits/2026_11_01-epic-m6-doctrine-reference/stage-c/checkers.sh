#!/usr/bin/env bash
# T39 (#686) stage C: § 5's runs and the checkers' baseline re-run at the lane's tip, each output kept here
# (stage A recorded their one-line results only; see stage-a/README.md). Each run's exit is `rc=<n>` on its own
# line. Read-only: no --write, no fetch, no guest, no compile.
#   bash checkers.sh <worktree> <outdir>
R=${1:?worktree}; O=${2:?outdir}
cd "$R" || exit 2
export LC_ALL=C
G=/usr/bin/grep
T=/workspace/tmp/m6-t39
P=.qa-scratch/t39/paths.txt
X=.qa-scratch/t39/text.txt
mkdir -p "$O" "$T/tmp"
one() {  # one <name> <command...>: the command's output to $O/<name>.out, its exit and last line printed here
  local name=$1; shift
  "$@" > "$O/$name.out" 2>&1
  local rc=$?
  echo "rc=$rc" >> "$O/$name.out"
  printf '%-28s rc=%s  %s\n' "$name" "$rc" "$($G -v '^rc=' "$O/$name.out" | tail -n 1 | cut -c1-150)"
}
echo "== at $(git rev-parse --short HEAD), $(date -u +%Y-%m-%dT%H:%M:%SZ)"
one rules-check tools/rules-check
one register-check tools/register-check
one es-menu-map-check tools/es-menu-map-check
one release-catalog tools/release-catalog --check
one work-log-index tools/work-log-index --check
one prose-check tools/prose-check --self-test
one ceremony-check tools/ceremony-check
one hooks-test .githooks/hooks-test
one box-check tools/box-check
echo "== the byte identity of the 254 against the merge base and upstream (R1 C12)"
for B in c445081a59 651150fc88; do while IFS= read -r p; do if git cat-file -e "$B:$p" 2>/dev/null; then [ "$(git rev-parse "$B:$p")" = "$(git rev-parse "HEAD:$p")" ] && echo "vs $B identical" || echo "vs $B differs"; else echo "vs $B absent"; fi; done < "$P" | sort | uniq -c; done | tee "$O/byte-identity.out"
echo "== the identity words over the 223, lines and files (case-sensitive)"
for w in Rasteratops rasteratops RASTERATOPS ROCKNIX rocknix maxengel JELOS pixelelated Pixelelated PIXELELATED; do printf '%s lines %s files %s\n' "$w" "$(cd "$T/export" && xargs -d '\n' -a "$R/$X" $G -h -c -e "$w" | awk '{s+=$1} END {print s+0}')" "$(cd "$T/export" && xargs -d '\n' -a "$R/$X" $G -l -e "$w" | $G -c '')"; done | tee "$O/identity-words.out"
echo "== the retired names over the 223 (case-insensitive)"
for w in 'cloud_migrate_layout' 'migrate.?layout' 'rebase --onto' 'rclonectl' '\.github/instructions' 'copilot' 'rubber[- ]duck' '\brclone config\b' 'rocknix\.worktrees'; do printf '%s lines %s\n' "$w" "$(cd "$T/export" && xargs -d '\n' -a "$R/$X" $G -h -c -i -E -e "$w" | awk '{s+=$1} END {print s+0}')"; done | tee "$O/retired-names.out"
echo "== the secret scan in the hooks' form (compile rc at most 1, the runtime-built positive 1, then files with a hit)"
( F=$(mktemp "$T/tmp/sp.XXXXXX"); git show HEAD:.githooks/secret-patterns > "$F"; SECRET_PATTERNS=''; . "$F"; rm -f "${F:?}"
  printf '' | $G -E -e "$SECRET_PATTERNS" > /dev/null 2>&1; rc=$?
  echo "secret regex compile rc=$rc"
  printf -- '-----BEGIN %s-----\n' "$(printf '%s' 'OPENSSH PRIVATE KEY')" | $G -c -E -e "$SECRET_PATTERNS"
  cd "$T/export" && xargs -d '\n' -a "$R/$X" $G -c -E -e "$SECRET_PATTERNS" | $G -v -c ':0$' ) | tee "$O/secret-scan.out"
echo "== non-ASCII files over the 223"
(cd "$T/export" && xargs -d '\n' -a "$R/$X" $G -c -P '[^\x00-\x7F]') | $G -v -c ':0$' | tee "$O/non-ascii.out"
echo "== forbidden-terms over the 223, over empty input, and over a planted positive"
(cd "$T/export" && xargs -d '\n' -a "$R/$X" cat) > "$T/tmp/text223.txt"
{ tools/forbidden-terms-check --stdin < "$T/tmp/text223.txt"; echo "over the 223 rc=$?"
  tools/forbidden-terms-check --stdin < /dev/null; echo "over empty input rc=$?"
  printf 'a zzqplantedzz line\n' > "$T/tmp/planted.txt"
  FORBIDDEN_PATTERNS='zzqplantedzz' tools/forbidden-terms-check --stdin < "$T/tmp/planted.txt"; echo "a planted positive rc=$?"; } 2>&1 | tee "$O/forbidden-terms.out"
echo "== the licence files against #359's recorded bytes (L-45)"
for f in LICENSE.md TRADEMARK.md; do printf '%s %s\n' "$f" "$(git show "HEAD:$f" | sha256sum | cut -c1-64)"; done | tee "$O/licence-hashes.out"
echo "== the releases a reader of README.md finds (L-02)"
gh release list --repo pixelelated/distribution --limit 3 2>&1 | tee "$O/releases.out"
echo "== the removal check and the registers' removed lines, 86ebb6dffc to HEAD (expect no line, then 0)"
git diff --stat 86ebb6dffc HEAD -- docs/reviews docs/releases/catalog.md docs/pr-series/map.txt docs/releases/rc-accept.txt docs/vm-qa-log.md docs/cloud-sync-changelog.md docs/rasteratops/p0-sweep-hits.txt plans licenses documentation LICENSE.md docs/upstream .claude CLAUDE.md AGENTS.md NAMING.md tools scripts packages projects | tail -n 1 | tee "$O/removal-check.out"
git diff 86ebb6dffc HEAD -- docs/decision-register.md docs/blindspot-register.md docs/friction-log.md | $G -c -E '^-([^-]|$)' | tee -a "$O/removal-check.out"
echo "== the host file: lines since the dispatch's 712, this lane's (the coordinator's own block excluded)"
awk 'NR>712' /workspace/tmp/m7-m6-host-coordination.txt | $G -v '^== M6 coordinator' | $G -c -E 'T39|#686' | tee "$O/host-file.out"
echo "(end)"

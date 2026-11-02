#!/usr/bin/env bash
# t39-checks.sh: T39 (#686) stage C's checker over the 254 reference documents (brief § 5, R3 § 2.9's
# `tools/docs-check` design scaled to the slice). Written under the audit folder's tools/, never the
# repository's tools/ (its promotion to a fork tool is a Backlog the hand-back names).
#
#   bash t39-checks.sh --tree <export> --repo <worktree> --commit <ref> --since <ref> \
#        --paths <paths.txt> --allow <dir> --out <dir> [--withhold findings] [--coordinator-tip <exact authorized tip>]
#
# --tree   the read tree: the 254 exported by `git archive <ref> -- <the 254> | tar -x`, never a checkout
# --repo   the repository the register, the inventory, the history and the blobs are read from, by
#          `git -C <repo> show|log|diff|cat-file` at --commit and --since
# --since  the dispatch tip (MERGE_HASH); the untouched, generated and binaries steps compare against it
# --paths  § 2's paths.txt, 254 lines
# --allow  the directory holding allow-legit.txt, allow-inherited.txt and allow-findings.txt, every entry
#          `<path>:<line> <class> <reason>` (classes in t39-checks.py's docstring)
# --out    the only place it writes: one <step>.txt per step
# --withhold findings  reads allow-findings.txt as empty (the record's FAIL at the tip; never delete the file)
#
# Steps, one ok/FAIL line each: inventory, scope, links, paths, tools, identity, retired, cites, untouched,
# generated, binaries, leads (the § 3 check lines of the fix candidates), then allowlists (an entry that
# excused nothing is a failure). Exit 0 when every step
# passes, 1 when one fails, 2 when nothing could be checked (a refusal). The last line is
# `TOTAL: <passed> of <checks> steps`, printed by the script.
# Stage-H-only provenance input. Default invocation retains the accepted semantics.
# Only the owner's immutable 2026-11-02 hand-back tip is recognized; arbitrary
# ancestry exclusions are refused. Production tools and historical receipts stay unchanged.
TREE= REPO= COMMIT= SINCE= PATHS= ALLOW= OUT= WITHHOLD= COORDINATOR=
while [ $# -gt 0 ]; do
  case "$1" in
    --tree) TREE=$2; shift 2 ;;
    --repo) REPO=$2; shift 2 ;;
    --commit) COMMIT=$2; shift 2 ;;
    --since) SINCE=$2; shift 2 ;;
    --paths) PATHS=$2; shift 2 ;;
    --allow) ALLOW=$2; shift 2 ;;
    --out) OUT=$2; shift 2 ;;
    --withhold) WITHHOLD=$2; shift 2 ;;
    --coordinator-tip) COORDINATOR=$2; shift 2 ;;
    *) echo "t39-checks: refused: unknown argument $1; nothing checked"; exit 2 ;;
  esac
done
refuse() { echo "t39-checks: refused: $1; nothing checked"; exit 2; }
command -v python3 > /dev/null 2>&1 || refuse "python3 missing"
[ -n "$TREE" ] || refuse "no --tree"
[ -d "$TREE" ] || refuse "--tree $TREE is not a directory"
[ -e "$TREE/.git" ] && refuse "--tree $TREE is a checkout (it holds .git)"
[ -n "$PATHS" ] && [ -f "$PATHS" ] || refuse "--paths absent"
n=$(/usr/bin/grep -c '' "$PATHS")
[ "$n" = 254 ] || refuse "--paths $PATHS has $n lines, not 254"
[ -n "$REPO" ] && [ -n "$COMMIT" ] && [ -n "$SINCE" ] && [ -n "$ALLOW" ] && [ -n "$OUT" ] \
  || refuse "--repo, --commit, --since, --allow and --out are all required"
case "$WITHHOLD" in ""|findings) ;; *) refuse "--withhold takes only findings" ;; esac
git -C "$REPO" show "$COMMIT:docs/decision-register.md" > /dev/null 2>&1 || refuse "the register is unreadable at $COMMIT"
git -C "$REPO" show "$COMMIT:docs/reviews/inventory.json" > /dev/null 2>&1 || refuse "the inventory is unreadable at $COMMIT"
git -C "$REPO" rev-parse --verify --quiet "$SINCE^{commit}" > /dev/null || refuse "--since $SINCE is not a commit in $REPO"
if [ -n "$COORDINATOR" ]; then
  [ "$COORDINATOR" = 329011b9eae20922b4d0727e13bf1626b2e1c04f ] \
    || refuse "--coordinator-tip is not the exact owner-authorized Stage-H tip"
  git -C "$REPO" merge-base --is-ancestor "$COORDINATOR" "$COMMIT" \
    || refuse "the authorized coordinator tip is not an ancestor of --commit"
fi
mkdir -p "$OUT" || refuse "cannot write --out $OUT"
exec python3 -I "$(cd "$(dirname "$0")" && pwd)/t39-checks.py" "$TREE" "$REPO" "$COMMIT" "$SINCE" "$PATHS" "$ALLOW" "$OUT" "$WITHHOLD" "$COORDINATOR"

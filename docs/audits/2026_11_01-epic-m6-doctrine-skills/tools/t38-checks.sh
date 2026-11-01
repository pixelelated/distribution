#!/usr/bin/env bash
# t38-checks.sh: T38 (#685) stage C's checker over the 52 (brief § 5, ruling (f); its findings feed #1373).
#
#   bash t38-checks.sh --tree <export> --repo <worktree> --commit <ref> --allow <dir> --out <dir> [--withhold findings]
#
# --tree is the read tree (`git archive <ref> .claude/agents .claude/skills | tar -x`), never a checkout; the
# rule's rows, the pins and the lint are read from --repo with `git show <--commit>:<path>`. It writes only under
# --out. Steps, each one ok/FAIL line: inventory, front, refs, stale, roster, pins, contract, bundle (informational).
# The three allowlists under --allow are allow-legit.txt, allow-inherited.txt and allow-findings.txt, every entry
# `<path>:<line> <class> <reason>`; --withhold findings reads the third as empty (the record's FAIL at the tip).
# Exits 0 when every assertion passes or is allowlisted, 1 when one fails, 2 when nothing could be checked (a
# refusal). The last line is `TOTAL: <passed> of <checks> assertions`, printed by the script.
TREE= REPO= COMMIT= ALLOW= OUT= WITHHOLD=
while [ $# -gt 0 ]; do
  case "$1" in
    --tree) TREE=$2; shift 2 ;;
    --repo) REPO=$2; shift 2 ;;
    --commit) COMMIT=$2; shift 2 ;;
    --allow) ALLOW=$2; shift 2 ;;
    --out) OUT=$2; shift 2 ;;
    --withhold) WITHHOLD=$2; shift 2 ;;
    *) echo "t38-checks: refused: unknown argument $1; nothing checked"; exit 2 ;;
  esac
done
refuse() { echo "t38-checks: refused: $1; nothing checked"; exit 2; }
command -v python3 >/dev/null 2>&1 || refuse "python3 missing"
[ -n "$TREE" ] || refuse "no --tree"
[ -d "$TREE/.claude" ] || refuse "--tree $TREE holds no .claude/"
[ -e "$TREE/.git" ] && refuse "--tree $TREE is a checkout (it holds .git)"
[ -n "$REPO" ] && [ -n "$COMMIT" ] && [ -n "$ALLOW" ] && [ -n "$OUT" ] || refuse "--repo, --commit, --allow and --out are all required"
case "$WITHHOLD" in ""|findings) ;; *) refuse "--withhold takes only findings" ;; esac
git -C "$REPO" show "$COMMIT:tools/lint-audit-artifacts" >/dev/null 2>&1 || refuse "the lint is unreadable at $COMMIT"
git -C "$REPO" show "$COMMIT:verifier-pins.json" >/dev/null 2>&1 || refuse "verifier-pins.json is unreadable at $COMMIT"
mkdir -p "$OUT" || refuse "cannot write --out $OUT"
exec python3 -I "$(cd "$(dirname "$0")" && pwd)/t38-checks.py" "$TREE" "$REPO" "$COMMIT" "$ALLOW" "$OUT" "$WITHHOLD"

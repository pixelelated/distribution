D=/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-skills-685
cd "$D"
cat .github/sessions/saved-session-state-feature-m6-doctrine-skills-685.md   # the pointer: the dispatch's hashes; § 10 names the eleven keys to check
export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t38; mkdir -p "$T/tmp"; df -i /workspace | tail -n 1
date -u +%Y-%m-%dT%H:%M:%SZ
git branch --show-current                                                    # feature/m6-doctrine-skills-685
git status --short | $G -c ''                                                # 0
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-p1           # stacked-on-p1 (ruling (a))
git merge-base --is-ancestor 8ebaf8daad HEAD && echo next-is-here            # next-is-here
sha256sum docs/reviews/slices.json docs/reviews/inventory.json | cut -c1-16  # 49bc2745664e52f4, d17b9cac4b2c2245 (R1 C06): the membership block's inputs, present because the branch is stacked on P1
test -d /workspace/tmp/m6-coordinator/t11-research/tree && echo clone-here   # clone-here: the block's W, read by git -C only (R1 C21 re-ran the block from it)
# the lint's PASS on a Local plan, before anything else (ruling (m)): T4's finished Local folder, exported from T4's tip and linted by this tip's lint; then a copy with its tier_exception removed, which must FAIL
git rev-parse --verify origin/feature/m6-doctrine-rules-651 2>&1             # 6ec78bbf8c... at R5 C23; recorded whole as it prints, a hash or `fatal:` (R5 § B item 3)
F=docs/audits/2026_10_24-epic-m6-doctrine-rules; L=$T/lint-proof; mkdir -p "$L/pass" "$L/fail"
git archive 6ec78bbf8c "$F" | tar -x -C "$L/pass"; git archive 6ec78bbf8c "$F" | tar -x -C "$L/fail"
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("t4 plan:", d.get("depth"), d.get("tier_exception"), len(d.get("reviewers") or []))' "$L/pass/$F/second-opinions/review-plan.json"   # `t4 plan: local D-WORKFLOW-184 0` (the proof's run of this block at 2f42ff5ddf, proof Part 4)
python3 -I -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d.pop("tier_exception",None); json.dump(d,open(p,"w"),indent=2)' "$L/fail/$F/second-opinions/review-plan.json"
tools/lint-audit-artifacts "$L/pass/$F" > "$T/tmp/lint-local-pass.out" 2>&1; rc=$?
echo "lint, a Local plan, rc=$rc"; tail -n 3 "$T/tmp/lint-local-pass.out"   # rc=0, the output ending `PASS` (proof Part 4, at 2f42ff5ddf) -- this line is the proof ruling (m) asks for
tools/lint-audit-artifacts "$L/fail/$F" > "$T/tmp/lint-local-fail.out" 2>&1; rc=$?
echo "lint, tier_exception removed, rc=$rc"; $G -n 'FAIL' "$T/tmp/lint-local-fail.out"   # rc=1, `FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone` and `1 CONTRACT FAILURE(S)` (proof Part 4; the lint's :94-98, R5 C23) -- the PASS's FAIL-first
# the three moved files, against the P1 tip and against next (ruling (a), L-01): ` 3 files changed, 50 insertions(+), 1 deletion(-)` both (R1 C09; R4 C20)
X=':(exclude).claude/rules/'; git diff --shortstat 2174265e9c HEAD -- .claude/ "$X"; git diff --shortstat 8ebaf8daad HEAD -- .claude/ "$X"
# other lanes' refs (proof correction 1, § 1): each ref's 52 read from its merge base with the coordinator's tip, so a ref that only lacks later coordinator edits prints nothing; expect `refs scanned:` with the count that prints (82 at 2f42ff5ddf) and no `own change` line (none over 82 refs with 2f42ff5ddf for the coordinator's tip -- v2 read); any line is a ref that moved the 52 itself, recorded and named on #685
CO=3a9b0aec81   # the pointer's value, never the literal word (§ 1's placeholders): unfilled, every ref prints and the positive below exits 128, not 1
R=$(git for-each-ref --format='%(refname:short)' 'refs/heads/feature/m6-*' 'refs/remotes/origin/feature/m6-*'); printf '%s\n' "$R" | $G -c '' | sed 's/^/refs scanned: /'
for r in $R; do git diff --quiet "$CO...$r" -- .claude/agents .claude/skills || echo "own change to the 52: $r"; done
git diff --quiet "2174265e9c...$CO" -- .claude/agents .claude/skills; rc=$?
echo "the loop's positive, the P1 tip as base and the coordinator's tip as the ref: rc=$rc"   # rc=1 (the coordinator's three files; v2 read at 2f42ff5ddf): the comparison can fire
# the checkers' baseline at the dispatch tip (R3 C6, C24; their lines may move with the dispatch's own commits, so each line that prints is recorded beside the research's)
tools/rules-check > "$T/tmp/rules-check.out" 2>&1; rc=$?
echo "rules-check rc=$rc"; tail -n 1 "$T/tmp/rules-check.out"               # rc=0, `rules-check: 30 rule files, every one front-mattered and indexed` (R3 C6) -- no evidence for the 52 (§ 3 item 5)
tools/register-check > "$T/tmp/register-check.out" 2>&1; rc=$?
echo "register-check rc=$rc"; tail -n 1 "$T/tmp/register-check.out"         # rc=0, `register-check: 711 IDs, each once; every citation in the live documents names a row` at 926d1fbaee (R3 C24), `712 IDs` at 2f42ff5ddf with -217 (proof Part 3); the dispatch's -218 moves it again, so the line that prints is recorded
tools/ceremony-check > "$T/tmp/ceremony-check.out" 2>&1; rc=$?
echo "ceremony-check rc=$rc"; tail -n 1 "$T/tmp/ceremony-check.out"         # `nothing overdue.` at 926d1fbaee (R3 C24); what another lane owes is noted on #685, never paid here
gh --repo pixelelated/distribution issue view 685 --json title,state,body --jq '.title, .state, (.body | split("\n") | length)'   # the title, OPEN, and the body's line count after the coordinator's fill (27 before it, R5 C10)
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200   # read for the protocol only, with the time of the read; this slice writes no line there (§ 10)

# Brief: M6.P2 T10, the guards: hooks, the fork CI and the checkers (#657)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #657 differ, #657 wins and the
coordinator corrects the brief in the same session. **Version 2 (2026-10-24):** version 1 was written after the tooling area's futro
(`docs/futros/2026-10-24-m6-tooling-and-guards.md`, posted on #903) gained
its T10 kickoff addendum, and after T4 (#651, the doctrine, accepted at
`cceac27d6a`) read the rules that describe these tools and left this slice
two leads on #657 and the `ceremony-check` packet `9e12014623` (#905). Every
figure below was produced by a command on the tree at `8ebaf8daad`, on P1's
tip `2174265e9c` for the three tools that exist only there, on an export
under `/workspace/tmp/m6-coordinator/t10-hash/`, or on GitHub this afternoon,
and says which; a stranger's proof preceded the dispatch (read-only, 8 API calls), and version 2 records what it found: six figures wrong (the at-hash line counts, the fork-commit count, the `PERSONAL_PATTERNS` range and count, the register's ID count, the CI's red streak, one upstream script's bytes) and two partial (the secret listing, P1's read-line derivation), each corrected below and listed in the futro's errata. **Each command block sets its own variables** (`D`): a Bash
call in this harness starts a fresh shell. **This is a read of the fork's own
guards at Extended depth, the security list's**: the hooks that keep a
credential-shaped line and the words of a list kept outside every tree out of
the fork's history, the CI that reruns the record's checks, and the checkers
every slice closes on. **Nothing here pushes, removes a worktree, cuts a PR
series, publishes, or prints a word of the wordlist or a credential-shaped
line**; the tools are read, their own suites and fixtures are run in the
lane's worktree, and every mutating mode is named in § 8 as a stop.

## 1. Identity

- **Issue:** #657 `M6.P2 E903/T10: tooling-and-guards: the guards: hooks,
  the fork CI and the checkers`, slice `tooling-guards` (`k: 10`) in
  `docs/reviews/slices.json`, tenth in `docs/reviews/order.md` (its § T10
  paths line: *"31 paths, 6,676 lines, 6,400 read, of which 6,014 fork-own;
  0 patch and config lines; reach n/a 31"* -- *read* is P1's own derivation; the inventory's columns give fork-own 6,290 and upstream-carried 386 lines; its `why`: *"the secret and
  wordlist guards and the ceremony state machine; 28 blindspot entries name
  tooling; early, because every slice's commits pass through these guards
  and every slice closes on `tools/lint-audit-artifacts`, and because the
  survey's own tools (`renovation-inventory`, `-drift`, `-status`) are what
  the dead-end tables trust ..."*). **Epic:** #903 (the tooling and guards:
  T9 #656 running beside this slice, then T12 #659, T14 #661, T15 #662, T45
  #692), whose futro carries this slice's kickoff addendum. **Milestone:**
  M6; its body holds the live order; read it first. **Predecessors:** #346
  (the plan), #641 (the survey: its three tools are this slice's), #644, **T4
  #651** (accepted: `02-forward-audit.md` F-02, F-23, F-22 on
  `feature/m6-doctrine-rules-651` are this slice's leads -- the friction
  reader that failed open, the register's column shape and in-place edits,
  the index's tool-to-rule direction; the coordinator's two rows on #657 of
  2026-10-24 carry them), **the #905 packet** (`fix/m6-905-ceremony-check-friction`
  at `9e12014623`, reviewed: `ceremony-check`'s friction reader is fixed
  ahead of this slice; read the tool at the hash *and* the packet's diff, and
  say which you read), **T6 #653** (accepted: `tools/pkgcheck`'s exit-0 on an
  unknown name, #845, the same class), **T9 #656** (running beside this
  slice in the other lane, D-WORKFLOW-190: the supervision tools the CI's
  three controls exercise; the two share no path). **Beside it:** T9.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, change a workflow's
  triggers, or decide a question of scope: those are the coordinator's,
  reached through #657, one question at a time. What it does file: its own
  audit punch-list issue (stage D) and a `bug` issue for every defect it
  finds (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-tooling-guards-657` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-guards-657`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the two hashes are in the dispatch comment on #657). **The worktree exists since 16:1x UTC (cut by the coordinator at `50137e3ee0`, the coordinator's tip merged in); before the dispatch comment on #657 nothing runs in it.** The session is the T3 lane's (`m6-t3-emulators`, pane
  `wN:p6`), which ran T3, T30, T24 and T4; those worktrees stay beside this
  one, idle, until their merges, and nothing is written there. The primary
  checkout `/workspace/repos/pixelelated/distribution` stays on `next`
  (D-INFRA-025) and **its `.githooks/` is the copy every worktree runs**
  (`core.hooksPath` is absolute, `fork-workflow.md` § Safety net): the
  slice reads the hooks at `8ebaf8daad`, runs `hooks-test` in its own
  worktree, and never edits the primary's copy. The legacy checkout and
  `rocknix.worktrees/*` are the M7 lane's, read only. **The rules in this
  worktree are `next`'s except the paths the dispatch comment lists.** T4's
  accepted edits of the rules that describe these tools (`ceremonies.md`'s
  friction row, `instruction-files.md`'s index, `fork-workflow.md`'s PR
  command) are on T4's branch, not in this worktree: read them with
  `git -C /workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-rules-651 show 6ec78bbf8c:<path>`
  where the rule's description of a tool is the question.
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Extended** (plan § 6c: *a security, state-preservation or
  launch-path slice ... Extended: two reviewers from two other labs*;
  `slices.json` k 10 `depth_reason`: *`.githooks/**`, the secret and
  wordlist guards, are on the security list*). Two reviewers from two labs
  through the Facilitator (`tools/council/run invoke --member gpt|gemini-argon
  --provider openrouter`): **GPT-6 Astra at `max`** and **Gemini 4 Argon at
  `high`**, each a probe first (identity, effort, provider from the
  provider's own field), then a refutation pass over one packet given to
  both independently, as T30's Phase 4.6 did (its `second-opinions/` on
  `feature/m6-emulators-standalone-677` is the model: the briefs, the probe
  prompts, the provenance files beside each output). `npm install --prefix
  tools/council`, `verify-pins` and `test` first; the key is
  `~/.config/council/env`, sourced by `run`, never read into a transcript.
  **A failed seat is a hold**, never a one-seat grading; a seat cut by its
  output ceiling re-runs on a trimmed packet, same model, effort and
  provider (D-WORKFLOW-195: T30's Gemini seat hit 65,536 tokens on a packet
  far larger than this one). The packet is the whole slice -- **31 files,
  336,673 bytes (328 KiB)** at the hash and P1's tip -- plus, as read-only
  context, `fork-workflow.md`'s *Personal paths* and *Safety net* sections
  and `ceremonies.md`'s table (what the hooks and the checkers promise).
  **The packet carries no wordlist and no credential-shaped literal**: the
  wordlist lives outside every tree and is never quoted (D-WORKFLOW-061);
  `hooks-test` builds its fixtures at run time, so the file at rest is clean
  -- the lane checks the packet with `tools/forbidden-terms-check --stdin`
  and the pre-commit's own scan before it is sent. The seats are asked first
  for `.githooks/pre-push`, `guard-lib` and `secret-patterns` (the two
  guards), then `tools/forbidden-terms-check` and `fork-worktree` (the one
  that reads the list, the one that can destroy build output).
  `review-plan.json` records depth `extended`, scope `epic`, primary
  `anthropic/claude-opus-5-5` / lab `anthropic`, reviewers `gpt`
  (`openai/gpt-6-astra`, `openai`, `max`) and `gemini-argon`
  (`google/gemini-4-argon`, `google`, `high`), provider `openrouter`,
  `allow_fallbacks: false`.
- **The substrate, read on 2026-10-24 by the coordinator:** the fork's
  GitHub has **23 workflows active** (`gh api repos/pixelelated/distribution/actions/workflows`):
  the four fork workflows and all 19 of upstream's (`build-*.yml`,
  `build-nightly.yml`, `validate-pull-request.yml`, `check-freeze-period.yml`,
  `update-mirror-sources.yml`, ...), the latter the build-engine area's files
  (T5/T6's, upstream-carried), not this slice's -- what a scheduled upstream
  workflow does on a fork is a lead for the coordinator, named once, not this
  slice's row. `fork-checks.yml` has **failed on every run on `next` since 2026-10-19** (last green 2026-10-18T11:00Z): the 2026-10-24 run on one step, *ceremonies are not overdue* (the W42 summary, the M7 lane's), the 2026-10-21 run on *every open acceptance checkbox is agent-verifiable* (`box-check`); the 2026-10-22 and 2026-10-23 runs' failing steps are the lane's to read; `fork-wordlist.yml` last passed on `next` on 2026-10-17 and
  runs on every branch push (it ran on the coordinator's pushes today);
  `fork-mirror-build-container.yml` is `workflow_dispatch` only and logs into
  `ghcr.io` with `GITHUB_TOKEN` through `skopeo`; `fork-generic-x64.yml` is
  13 lines whose one step is an `echo`. The hooks run from the primary
  checkout; `ls "$(git config core.hooksPath)"` lists `pre-push` on this
  host. The wordlist is `~/.config/rocknix/forbidden-terms` (mode 0600) on
  the host and the repository secret `FORBIDDEN_PATTERNS` in the CI: the slice confirms the host's with `test -r` and reads neither; `gh secret list` fails for this token (it prints `failed`: no `secrets` scope), so the secret's existence is inferred from `fork-wordlist.yml`'s green runs, whose header says the job is red without it.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-guards-657
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-tooling-guards-657
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
cat .github/sessions/saved-session-state-feature-m6-tooling-guards-657.md
ls "$(git config core.hooksPath)"                                    # must list pre-push: the primary checkout's copy runs here too
test -r ~/.config/rocknix/forbidden-terms && echo "wordlist present (never read into a transcript)"
df -i /tmp | tail -1                                                 # never export a tree under /tmp
mkdir -p .qa-scratch/t10/at-hash && git archive 8ebaf8daad .githooks .github/workflows/fork-checks.yml .github/workflows/fork-generic-x64.yml .github/workflows/fork-mirror-build-container.yml .github/workflows/fork-wordlist.yml .github/scripts tools/archaeology tools/box-check tools/ceremony-check tools/es-menu-map-check tools/forbidden-terms-check tools/fork-package-freshness tools/fork-worktree tools/lint-audit-artifacts tools/pr-stack-check tools/prose-check tools/rc-preflight tools/register-check tools/release-catalog tools/rules-check tools/vocabulary-check tools/work-log-index | tar -x -C .qa-scratch/t10/at-hash   # the read tree for the 28 at the hash
mkdir -p .qa-scratch/t10/at-p1 && git archive 2174265e9c tools/renovation-inventory tools/renovation-drift tools/renovation-status tools/test-fixtures/lint-audit-artifacts | tar -x -C .qa-scratch/t10/at-p1   # the three that live only on P1, with the lint's fixtures
"$D/tools/rules-check"; echo "rc=$?"; "$D/tools/register-check"; echo "rc=$?"; "$D/tools/ceremony-check"; echo "rc=$?"   # rc 1 on 2026-10-24: W42 OVERDUE (M7's week), not this lane's to pay
git push -u origin feature/m6-tooling-guards-657
```

## 2. Scope

**31 paths; 6,676 lines by the inventory's column (computed on P1's tree) and 6,642 at the read refs; 29 fork-own and 2 upstream-carried; 14 Python, 11 shell, 4 YAML, 2 without a language tag (`guard-lib`, `secret-patterns`: `language` is `none`); reach `n/a` 31.** The membership is the inventory's at P1's `2174265e9c`
with the slice's rule (`k: 10`): the area `tooling-and-guards` and the globs
`.githooks/**`, `.github/**` and the nineteen named tools. **The brace glob
is written out here because a naive glob-to-regex misreads it** (the
coordinator's first pass matched one tool of nineteen; the stranger's proof
reproduces this block as written). The re-derivation, in the lane's worktree:

```bash
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
tools = "forbidden-terms-check,ceremony-check,register-check,rules-check,box-check,rc-preflight,lint-audit-artifacts,archaeology,work-log-index,vocabulary-check,es-menu-map-check,fork-package-freshness,pr-stack-check,prose-check,release-catalog,renovation-inventory,renovation-drift,renovation-status,fork-worktree".split(",")
def sel(p): return p.startswith(".githooks/") or p.startswith(".github/") or p in ["tools/" + t for t in tools]
t10 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "tooling-and-guards" and sel(r["path"])]
print("paths", len(t10), "lines", sum(r["lines"] or 0 for r in t10), dict(collections.Counter(r["tier"] for r in t10)), dict(collections.Counter(r["reach"] for r in t10)), dict(collections.Counter(r["language"] for r in t10)))
print("the glob also selects, in other areas:", sum(1 for r in rows if r["tree"] == "distribution" and sel(r["path"]) and r["area"] != "tooling-and-guards"), "paths (.github/ISSUE_TEMPLATE, the PR template, .github/sessions): not this slice's")
os.makedirs(".qa-scratch/t10", exist_ok=True)
open(".qa-scratch/t10/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t10, key=lambda r: r["path"])))
PY
wc -l < .qa-scratch/t10/paths.txt                                                                        # 31
while IFS= read -r p; do case "$p" in tools/renovation-*) r=2174265e9c;; *) r=8ebaf8daad;; esac; printf '%6d %s\n' "$(git show $r:"$p" | wc -l)" "$p"; done < .qa-scratch/t10/paths.txt | awk '{s+=$1; print} END {print s " lines"}'   # 6642 at the read refs: the inventory's 6,676 counts P1's +3 in pre-push and +32 in lint-audit-artifacts, and a stale 1,596 for renovation-inventory
```

Recorded (2026-10-24):

| Lines | Path | Last fork commit | What it is |
| ---: | --- | --- | --- |
| 470 (473 on P1's tip) | `.githooks/pre-push` | `60a5d7f9c7` 2026-10-13 | the push guard: personal paths on `pr/*`, the console-first rule, the credential and wordlist scans over every pushed commit and message, the index warning, `ceremony-check --gate`; its header records the refusals proven on 2026-09-13 (audit #151 PL-08) |
| 21 | `.githooks/pre-commit` | `eb4fbe9b2c` 2026-09-29 | refuses a commit that adds a credential-shaped or listed line (the coordinator's branch adds a conflict-marker refusal, #696, not at the hash) |
| 25 | `.githooks/commit-msg` | `eb4fbe9b2c` | the message against the same two lists |
| 107 | `.githooks/guard-lib` | `eb4fbe9b2c` | `guard_load`, `guard_added_lines`, `guard_numbered`, `guard_scan`: the shared scans, failing closed |
| 8 | `.githooks/secret-patterns` | `9e104c65f3` 2026-09-28 | `SECRET_PATTERNS`, one definition for both hooks |
| 120 | `.githooks/hooks-test` | `eb4fbe9b2c` | the guards' own suite: 20 `expect` cases at the hash, fixtures built at run time |
| 59 | `.github/workflows/fork-checks.yml` | `d7e2d6be41` 2026-10-13 | the record's checks on every push of `next` and daily: the index, the register, the rules, T9's three controls, two VM-harness tests, `rocknix-info-test`, `box-check --quiet`, `ceremony-check` |
| 40 | `.github/workflows/fork-wordlist.yml` | `10bdc63d92` 2026-09-28 | every branch's push: `forbidden-terms-check` with the repository secret |
| 49 | `.github/workflows/fork-mirror-build-container.yml` | `a9af618398` 2026-10-04 | `workflow_dispatch`: mirrors the build container to `ghcr.io` with `skopeo` and `GITHUB_TOKEN` |
| 13 | `.github/workflows/fork-generic-x64.yml` | `3d7c075f63` 2026-10-02 | `workflow_dispatch`: one `echo` step |
| 98 | `.github/scripts/generate-changelog.sh` | `8a7f33791d` 2026-09-11 | upstream's (ROCKNIX's release scripts); identical on `upstream/next`? -- § 2's (a) says |
| 288 | `.github/scripts/generate-release-body.sh` | `1ebff24f36` 2026-09-01 | upstream's |
| 290 | `tools/archaeology` | `a9af618398` 2026-10-04 | what the record says about a question: the registers, the logs, the rules, `git log -S`, the issues; `--issue N`, `--reversal` |
| 107 | `tools/box-check` | `a9af618398` | every open checkbox agent-verifiable (D-QA-044); reads the open issues through the API |
| 461 | `tools/ceremony-check` | `8e8ad7c406` 2026-10-08 | the ceremony state machine (D-WORKFLOW-028); `--gate` is the push guard's call; the #905 packet fixes its friction reader after the hash |
| 200 | `tools/es-menu-map-check` | `d52e3d81c7` 2026-09-24 | the menu map against the ES pin's screens (`--es-src`, `--ref`) |
| 50 | `tools/forbidden-terms-check` | `3e70ef9239` 2026-09-28 | a tree or stdin against the wordlist outside the tree; refuses when the list is unreadable; takes its first argument as the tree, so `--help` is a tree named `--help` (rc 2) |
| 164 | `tools/fork-package-freshness` | `a0f60255ab` 2026-10-11 | the fork's recipes against their projects' releases (network) |
| 309 | `tools/fork-worktree` | `ef1e53334f` 2026-10-06 | `list`, `sync`, `remove`, `repair`: refuses to destroy build output (D-WORKFLOW-005); the #460 permission scan |
| 394 (426 on P1's tip) | `tools/lint-audit-artifacts` | `850cf9bee7` 2026-10-06 | the audit folder against the artifact contract (`--phase pre-issue`, `--issue`); T6's and T4's fixes to it are on their branches |
| 167 | `tools/pr-stack-check` | `5ec054a768` 2026-09-29 | builds the upstream series by content in a throwaway worktree (#322): **mutating** |
| 131 | `tools/prose-check` | `1070d05378` 2026-09-29 | a rocknix.org draft's tells; `--self-test` |
| 420 | `tools/rc-preflight` | `3c31e2aa18` 2026-10-15 | may this tree be cut as a candidate (#271): packages, bases, bugs, the record; `--tree`, `--only`, `--no-fetch` |
| 105 | `tools/register-check` | `fa935ed6ba` 2026-09-29 | every decision ID once, every citation naming a row; `MISPLACED` for a decided row under the open table |
| 107 | `tools/release-catalog` | `83acc0921f` 2026-09-25 | the kept cuts' RECORD.txt into `docs/releases/catalog.md` |
| 245 | `tools/rules-check` | `c3f0c75661` 2026-10-03 | the rule files' front matter, the index, the two entry files' counts, Codex's budget (D-WORKFLOW-045) |
| 132 | `tools/vocabulary-check` | `e1839046ae` 2026-09-12 | back up / backup, save state, Wi-Fi over the ES strings and the scripts' sentences |
| 106 | `tools/work-log-index` | `51bbb9f95a` 2026-09-23 | the day/week/month index; `--check`, `--write` |
| 1,597 (the inventory's column says 1,596) | `tools/renovation-inventory` | `00ca350666` 2026-10-23 (P1's branch) | the survey's inventory: paths, tiers, reach from `viewplan`; **#898**: its reach omits `PKG_DEPENDS_UNPACK` |
| 212 | `tools/renovation-drift` | `a7cbde1737` 2026-10-22 (P1's) | closed slices whose paths changed |
| 147 | `tools/renovation-status` | `af24589b1c` 2026-10-22 (P1's) | the slices' states from the tracker |

**Provenance.** The two `.github/scripts/*.sh` are upstream's: `git
cat-file -e upstream/next:<path>` succeeds for both and for nothing else of
the 31; `generate-release-body.sh` is byte-identical to `upstream/next`; `generate-changelog.sh` differs by 1 insertion and 8 deletions **because the fork is two upstream commits behind on it** (`76693a738d` 2026-10-13 and `71d8932b33` 2026-10-14 add the release author's GitHub name and are not in `next`); the fork carries no hunk of its own on either script. A Q4 row, corrected from version 2's "fork hunk" by T10's stage A (16:31 UTC). The three `renovation-*` tools
exist only on P1's branch (`git cat-file -e 8ebaf8daad:tools/renovation-inventory`
fails): they are read at `2174265e9c`, and `reviewed-at:` names both hashes.
`git log --format=%h c445081a59..8ebaf8daad -- <the 28 at the hash> | wc -l`
is **128** fork commits since the base (125 without merges); their messages cite #383 (12 times),
#344 and #258 (7 each), and #532, #508, #471, #409, #361, #288, #268, #225,
#211, #148, #147, #120 (3 each) among others -- the guards' own record is on
#307, #312, #151 (the push guard's proofs), #696 (the marker refusal), #845
(`pkgcheck`'s class), #905 (the friction reader), #898 (the inventory's reach).
**Two lists must agree by construction**: the hook's `PERSONAL_PATTERNS`
(`pre-push:62-188`, 115 quoted entries at the hash, 84 of them `tools/` paths and 14 `scripts/`; 62-191 and 118 on P1's tip, which adds the three `renovation-*` tools) and `fork-workflow.md`
§ *Personal paths* (*"This list and `PERSONAL_PATTERNS` are the same list;
change one and change the other"*): the (a) read diffs them entry by entry,
not by count (the rule's prose names 84 `tools/` paths and other shapes
besides).

**The hash.** The 28 at-hash files are read at `8ebaf8daad`'s bytes and the three others at `2174265e9c`'s, both from the exports (`.qa-scratch/t10/at-hash/`, `.qa-scratch/t10/at-p1/`); `reviewed-at:` is the branch `HEAD` at stage A and names both hashes. **The lane's branch differs from the hash on five of the 28**, each with a known owner, and that is the expected shape, not a lead: `.githooks/pre-push` (+3: P1's personal patterns for the three `renovation-*` tools, `2174265e9c`), `tools/lint-audit-artifacts` (+61/-9: P1's renovation face, `fc88815ccb`, and #810's `18747fbc52`), `tools/register-check` (+17: f00ab3e163 (register: ten decided rows moved from under Open decisions into the De)), `.githooks/pre-commit` (+13/-1) and `.githooks/hooks-test` (+7) (the marker refusal, #696, `1b8ac30421`). It differs from P1's tip on none of the three `renovation-*` tools. `tr '\n' '\0' < .qa-scratch/t10/paths.txt | grep -zv renovation- | xargs -0 git diff --stat 8ebaf8daad HEAD --` prints exactly those five; **any other hunk is the first lead.** Off this branch, `tools/ceremony-check` changes in the #905 packet (`9e12014623`). The slice reads the hash, names every delta with its commit in `01` § Scope, runs `hooks-test` twice (the at-hash export: 20 call sites, 27 results; the worktree: 22 and 29), and reads the changed file beside the hash's where a finding would otherwise be already fixed (the friction reader, the lint's local-at-epic rule, the marker refusal).

**The policy on change (plan § 5; D-WORKFLOW-187):** a defect here is the
fork's alone and is fixed under a stream brief at stage E, never at stage B;
**a stream on a hook proves with a new `hooks-test` case that fails on the
unfixed hook** (the suite is the guards' own evidence floor,
`fork-workflow.md` § Safety net); a stream on a checker proves with the
checker's own fixture or self-test (`lint-audit-artifacts`' fixtures on P1's
branch, `prose-check --self-test`, `register-check`'s constructed `MISPLACED`
row, `ceremony-check`'s #905 fixture) or adds one; a stream never widens a
scan's pattern without the constructed line it now catches *and* the line it
must still pass (a placeholder in angle brackets, a sentence with the word in
another sense); a change to a guard's contract (D-WORKFLOW-061, 028, 045,
005) is a lead for the coordinator, not a stream. **The wordlist is never
quoted, described, or reproduced** (D-WORKFLOW-061): a finding about
`forbidden-terms-check` names the file and the line, never the word.

## 3. Read first

- **The rules the work touches**, from `next`, this session
  (`working-principles.md` § Pre-flight): `fork-workflow.md` (§ Personal
  paths, § Safety net: the three hooks, the wordlist, the absolute
  `core.hooksPath`), `ceremonies.md` (the state machine, what each gate
  refuses, the blindspot-guard rule), `engineering-practices.md` (§ Guards
  must fail closed, with *The positive is recorded where the guard is
  wired*, *A fixture for a secret scanner is built at run time*, *Success
  reported over a no-op*; § Never edit a shell tool while a run of it is in
  flight), `issue-tracking.md` (§ A criterion is agent-first, `box-check`; §
  What the tool checks, `ceremony-check`'s `issues` line), `decision-register.md`
  (`register-check`), `instruction-files.md` (`rules-check`, the tool index),
  `worktrees.md` (§ Removing a worktree, `fork-worktree`), `release-candidates.md`
  (`rc-preflight`), `learning-capture.md` (`work-log-index`), `vm-first.md`,
  `learning-capture.md`, `decision-register.md`. T4's accepted edits of
  `ceremonies.md`, `instruction-files.md` and `fork-workflow.md` are read
  from T4's branch (§ 1).
- **The registers for the scope:** D-WORKFLOW-028 (the ceremonies audited
  by a tool, enforced by the push guard and the CI), D-QA-040 (open: the
  cadences), D-QA-044/045 (`box-check`; *checkbox*, not *box*),
  D-WORKFLOW-045 (`rules-check`'s contract over the two entry files),
  D-WORKFLOW-061 (the wordlist outside every tree), D-WORKFLOW-088 (the
  council toolchain at scaffold's paths: not this slice's, T45's),
  D-WORKFLOW-132 (the `issues` line), D-WORKFLOW-137 (audit depth),
  D-WORKFLOW-005 (`fork-worktree` refuses build output), D-WORKFLOW-013 (a
  clerical ID fix). **Blindspots** naming these guards: 52 (a decisions list
  built twice), 53 (a headline typed, not summed), 60, 66 (a verification
  keyed by number), 67 (a credential-shaped fixture in history before any
  guard read it: the pre-commit's origin), 68, 70, 73, 76 (the chain that
  committed markers: the pre-commit's marker refusal), and the class 8, 14,
  22, 26 (the hooks-path blindspot), 42.
- **The guards' recorded positives** (`engineering-practices.md` § The
  positive is recorded where the guard is wired): the push guard's header
  (2026-09-13, audit #151 PL-08: one refusal each, the commands and the
  hook's answer); the 2026-09-28 work log's *The positives, recorded where
  the guards are wired* (#307, #312: the pre-commit, the ES fork's pre-push
  with a missing `secret-patterns`); `box-check`'s first run (2026-09-25:
  46 of 479 checkboxes failing, #268); `es-menu-map-check`'s first run
  (2026-09-18: 30 of 51 screens); `register-check`'s `MISPLACED` positive
  (2026-10-22/23, #646); `archaeology --reversal`'s constructed case (audit
  #258 P-02); `lint-audit-artifacts`'s pass and fail fixtures
  (`tools/test-fixtures/lint-audit-artifacts/`, P1's tree); `prose-check
  --self-test` (#323); `rc-preflight`'s `already written` item seen to fire
  (2026-09-26, #289); `ceremony-check`'s #905 fixture (2026-10-24:
  `fixture-before.txt` `ok`, `fixture-after.txt` `OVERDUE`); the pre-commit's
  marker case (2026-10-24, #696). A guard whose positive the lane cannot find
  in the record is a Q6 row saying so.
- **The two leads from T4 on #657** (the coordinator's rows of 2026-10-24):
  `register-check` checks neither the open table's column shape, nor an
  in-place edit of a decided row (D-RA-006 is the failing control), nor an
  unescaped pipe in a decided row (six at the hash); `rules-check` does not
  check that an index row's *Detail in* rule names the tool. **T6's lead**
  (#845, fixed on T6's branch): `pkgcheck` exits 0 for a name that matches no
  recipe -- the class to hunt here: a checker that reads nothing and passes.
  **The futro's U-1 for T9**, now known: three recorded controls under
  `docs/qa-logs/` fail at the hash because their fixtures never carried
  `build-admission`; `fork-checks.yml:42-44` runs three others. Does the CI
  run a control that cannot fail? The class is this slice's Q6.
- **The evidence folders**: `docs/qa-logs/2026-10-24-905-ceremony-friction/`
  (the fixed friction reader's before and after, on the #905 branch),
  `docs/qa-logs/2026-10-02-candidate-preflight/` (`rc-preflight`'s controls),
  the pre-push's own header, `.githooks/hooks-test`'s cases.
- **The stranger's proof of this brief** (version 2's errata).

## 4. The questions

All seven apply (plan § 4); for guards on the security list **Q3 (bugs: a
guard that fails open) and Q6 (brittleness: a guard without a constructed
positive) are the lenses**, Q2 the fail-closed shapes, Q7 the three
descriptions of each guard (the hook's header, the rule, the tool index)
against the code.

| Q | What is asked of these 31 | Where the answer lands |
| --- | --- | --- |
| Q1 Modernize | A tool that reads a layout or a path the tree has retired (`rocknix.worktrees` in `fork-worktree`'s defaults or `pre-push`'s header: #640's rows); a workflow pinned to an action version or a runner image that has moved; a Python or bash construct the host's 3.14 and the CI's runner read differently | the rows; #640 named, not changed |
| Q2 Standards | Fail-closed shapes (`engineering-practices.md` § Guards must fail closed): a scan that cannot run refuses; `pipefail`; every expansion quoted; a count asserted; the hooks path absolute; a fixture built at run time; no `--no-verify` path; a tool's exit codes defined where named | a finding per violation, with the line |
| Q3 Bugs | **A guard that can fail open**: a line the scan regex does not read (T4's F-02 in `ceremony-check`, fixed by #905 -- hunt the same shape in every other reader: `register-check`'s row regex, `rules-check`'s front-matter regex, `box-check`'s checkbox regex, `work-log-index`'s heading regex, `pre-push`'s `PERSONAL_PATTERNS` match, `guard_added_lines`'s diff parser); a checker that reads nothing and passes (#845's class); a CI step whose failure does not fail the job; a scan a quoted filename or `diff.noprefix` evades (the `hooks-test` cases say which shapes were met); `forbidden-terms-check`'s behaviour when the list is missing, empty or uncompilable; `fork-worktree remove`'s refusal and the #460 scan; `pr-stack-check`'s throwaway worktree left behind | a `bug` per defect, `Already written:` and the VM line, its fix under a stream with a case |
| Q4 Currency | Not a package slice. The row is the two upstream scripts' bytes against `upstream/next` (identical, or the hunk), the actions the four workflows pin (`actions/checkout@v4`, the runner image, `skopeo`), and what GitHub reports active | one table |
| Q5 Efficiency | What a push and a CI run cost: the push guard's scan over every pushed commit (its runtime on a hundred-commit push, read from the code, measured once on the lane's own branch with `time` on a `git push --dry-run`? -- no: the hook runs on a real push; the figure is read from the lane's own pushes' durations), `box-check`'s API calls per run (300 issues on 2026-10-24), `fork-checks.yml`'s duration from its run history (`gh run list`, one call) | the figures with their source |
| Q6 Dead ends and brittleness | **The guard table**: for each refusal the 31 wire -- the push guard's six (personal paths, console-first, credential tip and range, wordlist tip and range, message, the ceremony gate, the index warning), the pre-commit's two, the commit-msg's two, `guard_load`'s unreadable-list refusal, each checker's failing verdicts (`register-check`'s duplicate, missing-row and `MISPLACED`; `rules-check`'s count, list, mention and budget; `box-check`'s person-or-device checkbox; `ceremony-check`'s nine lines; `lint-audit-artifacts`'s phases; `archaeology`'s empty result; `es-menu-map-check`'s undeclared and stale screens; `fork-package-freshness`'s six classes; `pr-stack-check`'s head mismatch; `prose-check`'s tells; `rc-preflight`'s items; `release-catalog`'s missing RECORD; `vocabulary-check`'s allowlist; `work-log-index --check`; `fork-worktree remove`'s refusals; `forbidden-terms-check`'s refusals; the three `renovation-*` tools' refusals) -- the recorded positive (§ 3) or the `hooks-test` case that constructs it, by file and case name, or **none**, which is a finding; and **a tool nothing runs**: for each of the 31, who calls it (a hook, a workflow step, a rule's instruction, a skill, nobody) | the table in `04` § Q6, every row sourced |
| Q7 Clarity | The three descriptions of each guard -- the hook's or tool's header, the rule that describes it (T4's accepted text), the index row in `instruction-files.md` -- against the code: a claim the code does not keep is a Q3 bug if it hides a failure and a Q7 row otherwise; `fork-workflow.md`'s *Personal paths* list against `PERSONAL_PATTERNS`, entry by entry; `ceremonies.md`'s table against `ceremony-check`'s lines | the rows; a drift in a rule is a lead for the coordinator (T4 is accepted; a rule edit is a stream here only with #657's dispatch) |

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`, `git diff`), a suite's or fixture's run with its
   exit, a workflow run's recorded conclusion (`gh run list`, `gh run view`,
   read only), or a document's line.
2. Mechanical evidence outranks reading: a guard's behaviour is the
   constructed line it refuses and the exit it returns, not the comment
   above it.
3. **The target is the tree, the suites and the record**: the at-hash hooks
   and tools; `hooks-test` run in the lane's worktree (its scratch repository
   is its own); the checkers run read-only over the worktree; the lint's
   fixtures on P1's tree; `prose-check --self-test`; the CI's run history
   through the API. **No push to `origin` beyond the lane's own branch, no
   `fork-worktree sync|remove|repair`, no `pr-stack-check` without `--help`,
   no `work-log-index --write` outside this worktree, no `fork-package-freshness`
   or `rc-preflight` network loop without the budget read first, no
   `gh workflow run`, no `gh secret` write, no edit to the primary checkout's
   `.githooks/`, nothing printed from the wordlist or a credential-shaped
   line (the hooks' own redaction is the model: `[REDACTED]`).**
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The suites and self-tests, with the baseline from the coordinator's export
of the hash** (2026-10-24; the lane runs each at stage A in its worktree and
records the exit; a control that fails at the hash is a finding):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-guards-657
cd "$D"
.githooks/hooks-test 2>&1 | tail -3                                              # in the worktree: PASS, 22 expect call sites printing 29 results (the hash's 20 sites print 27: a site inside a loop runs more than once); the at-hash export's copy too: PASS, rc 0
tools/register-check; echo "rc=$?"                                               # the hash's export: 644 IDs, each once; the lane's branch after the merge: 667
tools/rules-check --quiet; echo "rc=$?"                                          # rc 0; `--help` is not handled: it runs the checks (read what it does with an argument)
tools/work-log-index --check; echo "rc=$?"                                       # current
tools/prose-check --self-test 2>&1 | tail -2                                     # the maintainer's page passes, the machine draft fails (#323)
tools/box-check --quiet; echo "rc=$?"                                            # reads every open issue through the API: rate_limit before and after
tools/ceremony-check; echo "rc=$?"                                               # rc 1 on W42 (M7's); the friction line ok; compare with the #905 packet's tool from a detached checkout of 9e12014623
python3 -I tools/lint-audit-artifacts .qa-scratch/t10/at-p1/tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass 2>&1 | tail -1   # PASS
python3 -I tools/lint-audit-artifacts .qa-scratch/t10/at-p1/tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail 2>&1 | tail -1   # a FAIL, named
tools/forbidden-terms-check 2>&1 | tail -1                                       # `0 hits in N tracked files`; its refusal with the list unreadable is read in the code, and constructed only with FORBIDDEN_TERMS_FILE pointing at a stand-in (as hooks-test does), never by touching the real list
tools/fork-worktree list 2>&1 | head -5                                          # read only; never sync, remove or repair here
tools/es-menu-map-check --help; tools/rc-preflight --help; tools/archaeology --help; tools/pr-stack-check --help 2>&1 | head -3   # the modes; nothing runs
```

**The CI, read only:**

```bash
gh api rate_limit --jq '.resources.core.remaining'
gh run list --repo pixelelated/distribution --workflow fork-checks.yml --branch next --limit 5 --json conclusion,createdAt,databaseId --jq '.[] | "\(.createdAt) \(.conclusion) \(.databaseId)"'   # red on every run since 2026-10-19 (last green 2026-10-18T11:00Z)
gh run view <id> --repo pixelelated/distribution --json jobs --jq '.jobs[] | .steps[] | "\(.name): \(.conclusion)"'                                                                         # which step fails; which steps run
gh run list --repo pixelelated/distribution --workflow fork-wordlist.yml --limit 5 --json conclusion,createdAt,headBranch --jq '.[] | "\(.createdAt) \(.headBranch) \(.conclusion)"'
gh api repos/pixelelated/distribution/actions/workflows --paginate --jq '.workflows[] | "\(.state) \(.path)"'                                                                                  # 23 active on 2026-10-24
gh secret list --repo pixelelated/distribution 2>&1 | awk '{print $1}' | head -1                                                                                                 # prints `failed`: this token cannot list secrets; the secret's existence is inferred from fork-wordlist.yml's runs, its value never read
```

**The reading, per file:** every refusal path of the three hooks and
`guard-lib` matched to a `hooks-test` case or marked uncovered (Q6's table);
`PERSONAL_PATTERNS` against the rule's list entry by entry; every checker's
verdicts matched to a recorded positive or a fixture; the four workflows'
triggers, permissions, secrets and steps against what they claim; the two
upstream scripts' bytes against `upstream/next`; the three `renovation-*`
tools' refusals and #898's reach gap (read, not fixed: #898 is filed).

**The seats (Phase 4.6, two seats):** `npm install --prefix tools/council`,
`tools/council/run verify-pins`, `tools/council/run test`; the packet
(`gpt-brief.md` and `gemini-argon-brief.md`, the 31 files and the two rule
sections, `packet-manifest.json` with the sha256 of each) **scanned before it
is sent** (`tools/forbidden-terms-check --stdin < packet`, and the
pre-commit's patterns over it); the probes (`gpt-probe.md`,
`gemini-argon-probe.md`, each with its `.provenance.json`); the refutations
(`gpt-audit.md`, `gemini-argon-audit.md`, each with its `.provenance.json`),
both seats asked first for the two guards and `forbidden-terms-check` and
`fork-worktree`; each item graded in `04` § Second opinion with the artifact
that decided it; a Gemini seat cut by its ceiling re-runs on a trimmed packet
(D-WORKFLOW-195). The two calls run plainly with a harness waiter each
(T5's retro: `watch-build --record-only` holds the worktree's lock).

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#657`
(`Refs #657`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-guards/00-running-log.md` | the flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` and `2174265e9c` beside it, every § 5 command with its exit status, every `PROOF:` line, the API budget before and after each loop, each time from `date -u` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 31 re-derived with § 2's block and its output, the provenance (128 fork commits, two upstream-carried, one of them with a fork hunk, three on P1 only), the branch's deltas from the hash and the three after-hash deltas named with their commits; § Phase 1: what each guard refuses, in the slice's words, and the suites' baseline with exits | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #657's checklist, plus **a coverage table with one row per path** (31; the first cell the path in backticks so ``grep -c -E '^\| `(\.githooks|\.github|tools)/'`` counts them), § Mechanical checks (every § 5 block with command, exit status, summary), § The suites (each run, its exit, *a FAIL would mean ...*), § The CI (the runs read, the failing step, the 23 active workflows); every proof with a `proved:` cell | B, then F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the hooks x the CI (the same two lists, two runners); `ceremony-check` x the push guard x `fork-checks.yml`; `rules-check` x the two entry files x the index; `lint-audit-artifacts` x every slice's close; the `renovation-*` tools x the dead-end tables | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), **§ Second opinion** (4.6: both seats' probes and refutations graded item by item), **§ Renovation face** Q1 to Q7, **Q6 carrying the guard table** (every refusal with its positive, its case, or `none`; every tool with its caller or `nobody`), Q7 the three descriptions per guard | C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (extended; `gpt` at `max`, `gemini-argon` at `high`), the two briefs, `packet-manifest.json`, the two probe prompts, each probe and refutation with its `.provenance.json` | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` with `review plan: extended, 3 model perspectives, 2 verified external calls` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where (file:line at the hash), acceptance, `Already written:` and the VM line; the YAML `punch_index`; a guard with no positive as a `Renovation` item; a tool nobody runs as a `Renovation` item with the coordinator's disposition pending | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #657 | `Audit: M6 T10 the guards -- N findings (...)`; one checkbox per item, agent-first | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect, with its code trace, `Already written:`, the VM line and the case that will prove the fix; **no bug body quotes a credential-shaped line or a listed word** (the hooks' redaction, `[REDACTED]`, is the form) | D |
| Streams | the coordinator's brief `docs/reviews/briefs/t10-streams.md` | one per fix the coordinator briefs at the stage-D pause; a stream on a hook adds the `hooks-test` case that fails on the unfixed hook | E |
| Retro | `docs/retros/<date>-m6-tooling-guards.md`, posted on #657 | the mini-retro, Instruction-Recommendations mode; what the slice did to the two time-to-play numbers (nothing, say so); what it did to a guard's refusals, if a stream touched one | G |

## 7. Acceptance

The checklist on #657 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #657 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-tooling-guards/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-tooling-guards/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: extended` with `gpt` (`openai/gpt-6-astra`, `max`) and `gemini-argon` (`google/gemini-4-argon`, `high`), and each seat's probe and refutation outputs have a `.provenance.json` beside them whose served model is the seat's and whose verification is PASS; `packet-manifest.json` lists the 31 files and the two rule sections with their sha256, and `02` records the packet's own scan (`forbidden-terms-check --stdin` 0 hits, the credential patterns 0 hits) before it was sent.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#640 for a legacy path; a `bug` for a defect; the coordinator's lead for a contract change or a tool nobody runs), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes for 28 files and `2174265e9c`'s for the three `renovation-*` tools, both hashes named; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hashes, the filter of brief § 2 with its output (31 paths; 6,676 lines by the inventory, 6,642 at the read refs; 29 fork-own, 2 upstream-carried; 14 Python, 11 shell, 4 YAML, 2 untagged; reach `n/a` 31, or the deltas beside them), the provenance (128 fork commits, 125 without merges, since `c445081a59` over the 28; the two `.github/scripts` on `upstream/next` with their (a) state; the three on P1 only), the branch-vs-hash diff over the 31 (the five hunks brief § 2 names, each with its owner; any other named as a lead), and the after-hash deltas by commit (`9e12014623` on `ceremony-check`, off this branch; `1b8ac30421`, `18747fbc52`, P1's `pre-push` and lint edits, and `register-check`'s, on it).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `(\.githooks|\.github|tools)/' 02-forward-audit.md`` prints 31; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` § The suites records every § 5 run with command, exit status and summary line, each with the sentence *a FAIL would mean ...*; `hooks-test` PASS with its case count; the lint's pass fixture PASS and fail fixture FAIL by name; `prose-check --self-test`'s two verdicts; `register-check`, `rules-check --quiet`, `work-log-index --check` rc 0; `box-check --quiet` with the API budget before and after; `ceremony-check` rc 1 on W42 alone, with the #905 packet's tool compared from a detached checkout.
- [ ] `02-forward-audit.md` § The CI records the `fork-checks.yml` runs on `next` read (red since 2026-10-19, last green 2026-10-18; each run's failing step by name), the `fork-wordlist.yml` runs, the 23 active workflows as GitHub lists them (the 19 upstream ones named as the build-engine area's, with one lead for the coordinator on what a scheduled upstream workflow does on a fork), and the `FORBIDDEN_PATTERNS` secret's existence inferred from `fork-wordlist.yml`'s runs (`gh secret list` fails for this token), its value never read.
- [ ] `00-running-log.md` shows no `git push` other than the lane's own branch, no `fork-worktree sync|remove|repair`, no `pr-stack-check` run past `--help`, no `gh workflow run`, no `gh secret set`, no write under the primary checkout's `.githooks/`, and no credential-shaped value or listed word anywhere in the folder, judged by the guards themselves and not by a literal grep (the briefs under `second-opinions/` legitimately carry the hooks' own bytes, whose pattern text a literal grep matches): every commit of the folder passed `.githooks/pre-commit`'s scan (the hooks ran, `core.hooksPath` absolute), `guard_scan` from `.githooks/guard-lib` re-run over every file in the folder reports 0 lines, and `tools/forbidden-terms-check` over the folder prints 0 hits; the three commands and their counts are quoted in `02` (the coordinator's edit of 2026-10-24 at stage C's end, on the lane's question).
- [ ] `04-analysis.md` § Renovation face Q6 carries the guard table: one row per refusal brief § 4 names (its list read against the code: every refusal the code wires is a row), each with its recorded positive or `hooks-test` case by file and name, or `none` (a punch item); and one row per tool with its caller (a hook, a workflow step, a rule, a skill) or `nobody`.
- [ ] `04-analysis.md` § Q3 hunts the fail-open shape T4 found in `ceremony-check` through every other reader the slice names (`register-check`, `rules-check`, `box-check`, `work-log-index`, `pre-push`'s personal-path match, `guard_added_lines`), each with the line read and a constructed input that would be skipped or the statement that none can be.
- [ ] `04-analysis.md` § Q7 diffs `fork-workflow.md`'s *Personal paths* list against `pre-push`'s `PERSONAL_PATTERNS` entry by entry (the entries on one side only, named), and reads each guard's three descriptions (header, rule, index) against the code, with each drift a Q7 row or a Q3 bug; a rule drift is a lead for the coordinator, not an edit here.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fix-tree`, `fix-case` (a fix proved by a new `hooks-test` or fixture case that failed on the unfixed guard) or `fix-pending-ci` (a fix whose proof is the fork CI's next run on `next`, the coordinator's); ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; every `bug` this lane files passes `tools/box-check --issue N`; no file under `.githooks/`, `.github/` or `tools/` is changed on this branch before a stream brief (`git diff --stat <the lane tip the dispatch comment names> <fixed-at> -- .githooks .github tools` is empty, or every hunk is a stream the coordinator briefed), and a stream on a hook records in `02` the `hooks-test` case that failed on the unfixed hook and passes on the fixed one.
- [ ] The retro exists at `docs/retros/<date>-m6-tooling-guards.md`, is posted on #657, says what the slice did to the two time-to-play numbers (nothing, or the change named), and, if a stream touched a guard, what it did to that guard's refusals.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder, each exit code in the hand-back comment.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #657; a blocker named on #657 with what is needed (a seat failed, a suite
that cannot run for a reason outside the tree, two commands that disagree);
a branch that differs from `8ebaf8daad` on one of the 28 or from
`2174265e9c` on one of the three at stage A in a hunk the dispatch comment
did not name; or an execution limit, stated as such with the running log
current. A checkpoint is not a stop; a differing count is a delta; `next`
moving is drift. An idle session says it is idle on #657, **and does not end
a turn on a post that asks nothing**.

**What never runs in this slice:** a `git push` to any branch but the
lane's own; `tools/fork-worktree sync`, `remove` or `repair`;
`tools/pr-stack-check` past `--help`; `tools/work-log-index --write` outside
this worktree; `gh workflow run`, `gh secret set`, `gh release`; an edit to
the primary checkout's `.githooks/` or to any hook while a push is in
flight; a Facilitator call outside the Phase 4.6 pairs; `npm install`
anywhere but `tools/council`; `cat`, `grep` or any read of
`~/.config/rocknix/forbidden-terms` or the `FORBIDDEN_PATTERNS` secret's
value, or of `~/.config/council/env` or `~/.ROCKNIX/options`; a credential-
shaped literal or a listed word written anywhere (a fixture is built at run
time, `printf` pieces); a build; a guest; an edit to a rule, `CLAUDE.md`,
`AGENTS.md`, a decided register row, or
`.github/sessions/saved-session-state-next.md`; `--no-verify`; bare `git
stash`; `git worktree remove --force` or `rm -rf` on a worktree.

## 9. Ceremonies owed

- A work-log entry per session headed `#657`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #657` or the
  guard -- and a line the fixed `ceremony-check` reads (the #905 shape:
  `- YYYY-MM-DD HH:MM UTC -- ... issue: #N` or a guard path).
- The VM question written before any proof (§ 5: the bench is the host,
  the suites and the CI's record; no guest is expected).
- The mini-retro at stage G, posted on #657, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided row is D-WORKFLOW-199, the coordinator's;
  T9 runs beside this lane and may take 200); it goes at the end of `##
  Decided`, and a row is never edited.
- The merge notes: `tools/ceremony-check`, `.githooks/pre-commit` and
  `tools/lint-audit-artifacts` carry after-hash changes on the coordinator's
  and other lanes' branches (§ 2); a stream on any of them is cut over the
  hash's bytes and the coordinator merges it after those; when `next` moves,
  the **coordinator** merges `next` into this branch, never between stage A
  and stage D; a merge with conflicts is checked for leftover markers before
  it is committed (#696; the coordinator's branch refuses them at commit),
  and the ledgers are united by whole entries.
- Commit messages `docs: ...` for the audit, `<tool>: ...` or `hooks: ...`
  for a stream's fix, each with `Refs #657` and the attribution line; `git
  add -A` only after `git status --short` shows nothing a suite left behind
  (`hooks-test` cleans its scratch; `.qa-scratch/` is gitignored).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#657's checkboxes against their artifacts; the lint's `PASS` line; the two
seats' `review-plan.json` and provenance (served model, provider, effort,
verification) and the packet's recorded scan; the audit issue's checkboxes
all at an outcome (the ticked and open counts read by name); the coverage
table's row count (31) and the guard table's rows against § 4's list;
**re-running on an export of the tip under `/workspace/tmp`: the membership
block, the file list with line counts, `hooks-test`, `register-check`,
`rules-check --quiet`, `work-log-index --check`, `prose-check --self-test`,
the lint on both fixtures, and the `PERSONAL_PATTERNS` diff**;
`register-check` and `rules-check` on a simulated merge with the
coordinator's tip (the ledgers united; `hooks-test` on the merged tree, since
both branches touch the hooks); the retro's four answers; the six exit codes.
The lane posts one hand-back comment naming the tip and each artifact by
path, writes `reviewed-at:` and `fixed-at:` into #657's body, then says it is
idle. After acceptance the coordinator closes the audit issue, prompts the
lane for `audit-completion.json` and the full lint, merges the branch in its
turn after the M7 candidate (after T9's, before T4's), regenerates the
ledgers, and closes #657 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#903) carries this slice's kickoff addendum, and a stranger's proof of this
brief is run by a reader with no context before dispatch; version 2 records
what each found.

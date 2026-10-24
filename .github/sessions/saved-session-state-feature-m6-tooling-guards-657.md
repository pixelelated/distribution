# Session pointer: M6.P2 T10, the guards: hooks, the fork CI and the checkers (#657)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-tooling-guards-657`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `2a4be1006b` merged in at `558439d2d4`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-guards-657`; the T3, T30, T24 and T4 worktrees beside it (`m6-emulators-libretro-650`, `m6-emulators-standalone-677`, `m6-emulators-dead-ends-671`, `m6-doctrine-rules-651`) are this session's earlier slices, accepted and idle: read only, until their merges
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); **its `.githooks/` is the copy every worktree's commits run** (`core.hooksPath` is absolute) and is never edited from this lane; the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T3 session, `m6-t3-emulators`), unless #657 says otherwise
> **Epic:** #903 (the tooling and guards: T9 #656 running beside this slice in the T5 session, then T12, T14, T15, T45); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Extended -- GPT-6 Astra at `max` and Gemini 4 Argon at `high` through the Facilitator (a probe each, then one refutation each over one packet; D-WORKFLOW-184, 195; a failed seat is a hold); `npm install` only under `tools/council`
> **The security list:** `.githooks/**` and the two guards are on it. The wordlist (`~/.config/rocknix/forbidden-terms`, the `FORBIDDEN_PATTERNS` secret) and every credential file are never read into a transcript; no credential-shaped line or listed word is written anywhere (fixtures are built at run time); the packet is scanned before it is sent (D-WORKFLOW-061)
> **The host:** M6's; this slice runs no build, no guest, no push beyond its own branch, no `fork-worktree sync|remove|repair`, no `pr-stack-check` past `--help`, no `gh workflow run`, no `gh secret set`

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the paths the dispatch comment
   on #657 lists: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   prints exactly those; anything else is STALE. T4's accepted edits of
   `ceremonies.md`, `instruction-files.md` and `fork-workflow.md` are on
   T4's branch (`6ec78bbf8c`), read with `git -C ... show`, not in this tree.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/tooling-guards.md` whole (version 2). The brief is
   the work; its § 7 is the contract, identical to the checklist on #657.
   Its § 8 names what is never run here.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #657 (with its comments: the two leads from T4 and the #905 row), #903
   (the epic, with its futro comment and the T10 addendum: U-1 to U-6 and
   A1 to A8), #339, #346 (the maintainer's channel: what is open there is
   not this lane's to decide), #651 (T4, accepted: F-02, F-22, F-23), #905
   (the `ceremony-check` packet, `9e12014623`), #696 (the marker refusal),
   #845 (`pkgcheck`'s class), #898 (the inventory's reach), #307, #312 and
   #151 (the guards' own record), #640 (the legacy paths). The M7 lane's
   canonical checkpoint `.github/sessions/saved-session-state-next.md` is
   read for what runs on this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-guards/00-running-log.md` and
   write stage A -- the two hashes, the counts, the host file's last line
   and the census, every suite and self-test with its exit -- before reading
   a tool.

## Current focus (19:49 UTC update)

**The lane is IDLE. T10 is accepted on #657 (19:47 UTC) at `afdce9a65b`, and #958 is closed as completed (44 ticked).**

- **The record:** `audit-completion.json` is written from #958's closed readback (`docs/audits/2026_10_24-epic-m6-tooling-guards/tools/write-completion.py`). The full `tools/lint-audit-artifacts` prints `PASS`, and `tools/ceremony-check` accepts the marker; its one DUE is W42, which is the M7 lane's.
- **Nothing is owed by this lane.** The coordinator owns:
  - the merge to `next`, which completes criterion 5's merge clause;
  - #944's fix-pending-ci read of the first red run;
  - closing the bugs once their fixes reach `next`.
- **If a new brief arrives on #657,** read it, then `00-running-log.md`'s tail, then this file's earlier sections.

## Earlier focus

**The stage-D pause (2026-10-24, after 17:44 UTC).**
- 29 bugs (#929-#957) and the audit issue #958, 44 checkboxes, a sub-issue of #657.
- `05` holds 44 items (6 High, 25 Medium, 13 Low); `lint --phase pre-issue` prints PASS.
- Waiting for the coordinator's stage-E stream briefs. A stream on a hook proves itself with a new `hooks-test` case that fails on the unfixed hook; one on a tool with its fixture.
- Nothing in `.githooks/`, `.github/` or `tools/` has been edited on this branch (criterion 15).

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-guards-657
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
ls "$(git config core.hooksPath)"                                                 # pre-push listed: the primary checkout's hooks run here
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -c -x qemu-system-x86
sed -n '1,170p' docs/reviews/briefs/tooling-guards.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905), T5, T6, T7, T8, T9, **then this
branch**, then T4's last. Three of this slice's files change after the hash
on other branches -- `tools/ceremony-check` (#905's packet), `.githooks/pre-commit`
(the coordinator's marker refusal, #696), `tools/lint-audit-artifacts`
(#810's fix) -- so a stream here on any of them is cut over the hash's bytes
and the coordinator merges it after those. When `next` moves, the
**coordinator** merges `next` into this branch, and never between stage A
and stage D (the read must stay a fact about one hash, plan § 8); after
stage D a merge re-baselines the slice over the diff, recorded on #657.
Never merge another lane's feature branch here. Every lane and the M7 lane
append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696; the coordinator's branch refuses them
at commit, `next` not yet), and a union of two ledgers is made by whole
entries. The highest Decided register ID on 2026-10-24 at the dispatch is
D-WORKFLOW-199 (the coordinator's); T9 runs beside this lane and may take
200: check both branches; a new row goes at the end of `## Decided`, and a
row is never edited. Nothing here builds, touches a device, a cloud, a
guest, the primary checkout's hooks, the wordlist, or another lane's
worktree.

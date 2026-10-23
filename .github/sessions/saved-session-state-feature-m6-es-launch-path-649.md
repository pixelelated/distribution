# Session pointer: M6.P2 T2, EmulationStation's launch path (#649)

> **Seeded:** 2026-10-23 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-es-launch-path-649`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip merged in at `ac9c80ba32`
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649`
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-launch-path-649`, branch `feature/m6-es-launch-path-649` at the pin `16dbac5211eea7e70db7394372033be2be7df829`; the primary `/home/max/Development/emulationstation-next` and the `qa-integration` and `m7-*` worktrees beside it are somebody else's: read only
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone, D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only
> **Repositories:** `pixelelated/distribution` (integration branch `next`; every `gh` call carries `--repo pixelelated/distribution`) and `pixelelated/emulationstation` (remote `origin` in the ES worktree; the integration branch `test/qa-integration` is the coordinator's to merge into)
> **Executor:** Opus 5.5 at high effort unless #649 says otherwise
> **Epic:** #700 (the interface); the renovation epic #339; the milestone M6; beside T1 (#648) in its own lane (D-WORKFLOW-190)

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except three files (P1's
   `fork-workflow.md` and `instruction-files.md`; M7's
   `.claude/skills/council/IMPORTED-FROM.md`, which came with the Argon
   route): `git diff --stat next -- .claude CLAUDE.md AGENTS.md` lists
   exactly those three; anything else is STALE. Known stale facts in the
   rules are listed in the brief § 1 and § 3; this lane's layout is the
   brief's, not `worktrees.md`'s. The ES repository's `AGENTS.md` and
   `CLAUDE.md` are pointers to the distribution's rules (D-WORKFLOW-010).
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/es-launch-path.md` whole. The brief is the work;
   its § 7 is the contract, identical to the checklist on #649.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #649 (with its comments), #700 (the area epic, with its futro comment),
   #339, #346 and #648 (the lane beside this one; its findings on
   `runemu.sh`'s argument parsing are the other side of this slice's
   command). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host, not for a work queue; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-es-launch-path/00-running-log.md` and
   write stage A (the hashes, the counts, the two upstream refs, the host
   handoff's state) before reading a line of the slice.

## Current focus

**Phases 1 to 4 written from the tree; waiting on the host** (2026-10-23 18:0x UTC, T2 session
`9adce27f-9c22-4065-af78-e6c9a2a1f6ff`). `reviewed-at:` distribution `f4e0f0a196`,
ES pin `16dbac5211`. `docs/audits/2026_10_23-epic-m6-es-launch-path/` holds
`00` to `04`, `q6-table.md` and `q6-reachability.py`. Its `second-opinions/` holds the plan
(pending), the probe prompts and both briefs. Leads before 4.6: four Medium (FD-14,
SS-1, SD-2, VC-1), the rest Low or Renovation. #699's fix is on the branch; its
compile proofs are queued. **Next, on the coordinator's `resource return` relay on #649:**
run `00-running-log.md`'s queue in order (`npm install`, #699's proofs, the unit
tests, `tests/app-unit`, the python harnesses, the guest, the tool trials, Q5).
Then Phase 4.6 (probe, then refutation, per seat), then Phase 5 and the audit and bug issues,
then the stage-D pause.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649
W=/home/max/Development/emulationstation-next.worktrees/m6-es-launch-path-649
PIN=16dbac5211eea7e70db7394372033be2be7df829
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md          # exactly the three files above
[ "$(git -C "$W" rev-parse HEAD)" = "$PIN" ] && echo "ES worktree at the pin"
ls "$(git -C "$W" config core.hooksPath)"                     # must list pre-push
sed -n '1,140p' docs/reviews/briefs/es-launch-path.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then the T1 branch, then
this branch; the ES branch is merged into `test/qa-integration` and the pin
bumped in `package.mk` by the coordinator at acceptance (`fixed-at-es:`).
When `next` moves, the **coordinator** merges `next` into this branch, and
never between stage A and stage D (the read must stay a fact about one
hash, plan § 8); after stage D a merge re-baselines the slice over the
diff, recorded on #649. Never merge another lane's feature branch here, in
either repository. This branch, the P0, P1 and T1 branches and the M7 lane
all append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made
by whole entries, never by an unanchored pattern over marker-shaped text.
The highest register ID on 2026-10-23 is D-WORKFLOW-190 in the Decided
table (D-WORKFLOW-191 is an open row; the M7 lane holds 171 to 180
unmerged; the T1 lane may add one beside this lane: check both branches);
a new row goes at the end of `## Decided`. The ES fork's `test/qa-integration`
is at the pin; no open `feature/m7-*` ES branch touches the twenty files
(checked 2026-10-23); when the pin moves on `next`, the coordinator reads
`tools/renovation-drift`'s report (`es=` hash) and re-opens this slice over
the diff at its depth. Nothing here builds, touches a device, a cloud, or
another lane's worktree or guest.

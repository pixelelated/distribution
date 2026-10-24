# Session pointer: M6.P2 T7, the generic packages the image builds (#654)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-generic-packages-reached-654`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip merged in at `e7978a1ca5`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-generic-packages-reached-654`; the T5 worktree `m6-build-engine-652` and the T6 worktree `m6-build-engine-upstream-tools-653` beside it are this session's earlier slices, accepted and idle until their merges: nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, `ls` of their `build/` directories is the one read this slice makes
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #654 says otherwise
> **Epic:** #848 (the generic packages); the renovation epic #339; the milestone M6; beside T30 (#677) in the other lane (D-WORKFLOW-190)
> **Depth:** Local -- no reviewer, no Facilitator call, no `npm install`; the review plan carries `tier_exception: D-WORKFLOW-184` (#810)
> **Budget:** the GitHub API (5,000 calls an hour, shared with the coordinator's monitors); the brief's loops read `gh api rate_limit` before and after and start only above 1,500 remaining

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the seven paths the brief § 1
   names: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   lists exactly those; anything else is STALE. Known stale facts in the
   rules are listed in the brief § 1 and § 3; this lane's layout is the
   brief's, not `worktrees.md`'s.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/generic-packages-reached.md` whole (version 2).
   The brief is the work; its § 7 is the contract, identical to the
   checklist on #654. Its first commands include the at-hash export under
   `.qa-scratch/t7/`; a tree export never goes under `/tmp`.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #654 (with its comments: T6's lead of 08:57 is the first), #848 (the
   epic, with its futro comment), #644 (findings 15, 16, 17), #645 (the
   move table this slice feeds), #841 and #849 (the two classes of a fetch
   that fails from an empty cache), #652 and #653 (T5 and T6, accepted: the
   fetch and the tools; their audit folders are the nearest readings). The
   M7 lane's canonical checkpoint `.github/sessions/saved-session-state-next.md`
   is read for what runs on this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-generic-packages-reached/00-running-log.md`
   and write stage A before reading a row of the slice.

## Current focus

**At the stage-D pause (10:57 UTC); waiting for the coordinator's stream briefs.**
- **Branch:** `reviewed-at` `4ea87f17dd`.
- **Audit:** `docs/audits/2026_10_24-epic-m6-generic-packages-reached/`, `00` to `05` with `q4-table.md` and `q4-pins.json`. The pre-issue lint passes.
- **Audit issue:** #884, fifteen items.
- **Bugs:** #880 to #883 (mirror-covered dead URLs), plus the coordinator's #877 (`libfmt`, fixed in packet `cf3a8d8e62`).
- **Dispositions:** PL-11 → #879; PL-12 withdrawn.
- **Incident 10:44 to 10:47:** an unquoted heredoc ran `scripts/update_packages`, which rewrote `hatarisa`'s recipe in this worktree. It was reverted before any commit (`00` § Incident). Write prose with a quoted heredoc or the Write tool only.
- **Next:** the stream briefs on #654, then stage E. Nothing under `packages/` changes before a brief.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-generic-packages-reached-654
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the seven paths
test -f docs/reviews/inventory.json && echo inventory
gh api rate_limit --jq '.resources.core.remaining'
sed -n '1,140p' docs/reviews/briefs/generic-packages-reached.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T5,
T6, then this branch, then T4's. When `next` moves, the **coordinator**
merges `next` into this branch, and never between stage A and stage D (the
read must stay a fact about one hash, plan § 8); after stage D a merge
re-baselines the slice over the diff, recorded on #654. Never merge another
lane's feature branch here. This branch, the P0, P1 and the other lanes'
branches and the M7 lane all append to `docs/decision-register.md`, the
day's work log and `docs/work-logs/INDEX.md`: keep every append, regenerate
the index, never edit another lane's rows; a merge with conflicts is checked
for leftover markers before it is committed (#696), and a union of two
ledgers is made by whole entries, never by an unanchored pattern over
marker-shaped text. The highest Decided register ID on 2026-10-24 is
D-WORKFLOW-194 (the coordinator's); T30 runs beside this lane and may take
195: check both branches; a new row goes at the end of `## Decided`.
Nothing here builds, touches a device, a cloud, a guest, the shared source
cache (read only), or another lane's worktree.

# Session pointer: M6.P2 T9, build supervision and host maintenance (#656)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-tooling-build-supervision-656`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `8826d2968d` merged in at `2a24aa2063`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-build-supervision-656`; the T5, T6, T7 and T8 worktrees beside it (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`) are this session's earlier slices, accepted and idle: read only, until their merges
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there; their `.build-runs/` are this slice's read-only evidence (#597)
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #656 says otherwise
> **Epic:** #903 (the tooling and guards: T9 first, then T10, T12, T14, T15, T45); the renovation epic #339; the milestone M6; beside T4 (#651) in the other lane (D-WORKFLOW-190)
> **Depth:** Independent -- one GPT-6 Astra seat at `max` through the Facilitator (a probe, then one refutation over one packet; D-WORKFLOW-184, 195); `npm install` only under `tools/council`
> **The host:** M6's; this slice runs no build, no reclamation, no installer, no guest stop, no disk format, no release action; its isolated tests run in this worktree after the host file is read and the census recorded

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the paths the dispatch comment
   on #656 lists: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   prints exactly those; anything else is STALE. Known stale facts in the
   rules are the legacy layout (#640's), which this slice records in two of
   its own files and changes nowhere.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/tooling-build-supervision.md` whole (version 2).
   The brief is the work; its § 7 is the contract, identical to the
   checklist on #656. Its § 8 names what is never run here.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #656 (with its comments), #903 (the epic, with its futro comment: this
   slice's kickoff, U-1 to U-6 and A1 to A8), #339, #346 (the maintainer's
   channel: what is open there is not this lane's to decide), #644 (*Our
   build path*), #652 (T5, accepted: the scripts that `exec` into the
   runner), #493, #597, #410, #461 (the record the 35 fork commits cite),
   #640 (the legacy paths), #506 and #549. The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-build-supervision/00-running-log.md`
   and write stage A -- the hashes, the counts, the host file's last line and
   the census, the eight controls with their exits -- before reading a tool.

## Current focus

**Idle. T9 is accepted on #656 (18:32 UTC), at `bf4445a13c`, the lane's tip with the coordinator's merged.**
- **The audit is complete:** `docs/audits/2026_10_24-epic-m6-tooling-build-supervision/audit-completion.json`, written by `tools/write-completion.py` from #924's closed readback (closed as completed at 18:32:34Z; 21 ticked, 0 open).
- **The checks at the marker:**
  - `tools/lint-audit-artifacts`: `PASS`;
  - `tools/register-check`: 0;
  - `tools/ceremony-check`: it reads the marker (`ok audit`), and stays red only on M7's W42 summary.
- **Still open:** criterion 5's merge clause, until this branch merges to `next` and `tools/renovation-status` lists the slice `closed`.
- **Nothing runs on this lane.** No process, guest or container was left by it. The scratch under `/workspace/tmp/m6-t9/` (exports, the record replay's copied logs) is disposable.
- **`reviewed-at` `cb8019a10b`; `fixed-at` `00e571b8a8`.**

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-build-supervision-656
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt; pgrep -c -x qemu-system-x86
sed -n '1,160p' docs/reviews/briefs/tooling-build-supervision.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the two checksum packets (#877, #890), T5, T6, T7, T8, **then this branch**,
then T4's last. `tools/watch-build` and `tools/host-maintenance/build-admission`
are files the M7 lane also changed (#597); a conflict there at the merge is
resolved in the coordinator's hands with the stream's paragraph re-applied
(futro A8). When `next` moves, the **coordinator** merges `next` into this
branch, and never between stage A and stage D (the read must stay a fact
about one hash, plan § 8); after stage D a merge re-baselines the slice over
the diff, recorded on #656. Never merge another lane's feature branch here.
Every lane and the M7 lane append to `docs/decision-register.md`, the day's
work log and `docs/work-logs/INDEX.md`: keep every append, regenerate the
index, never edit another lane's rows; a merge with conflicts is checked for
leftover markers before it is committed (#696; the coordinator's branch
refuses them at commit, `next` not yet), and a union of two ledgers is made
by whole entries. The highest Decided register ID on 2026-10-24 at the
dispatch is D-WORKFLOW-199 (the coordinator's); T4 runs beside this lane and
may take 200: check both branches; a new row goes at the end of `## Decided`,
and a row is never edited. Nothing here builds, touches a device, a cloud, a
guest, the host's swap, or another lane's worktree.

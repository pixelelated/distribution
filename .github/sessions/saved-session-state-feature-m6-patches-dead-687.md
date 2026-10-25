# Session pointer: M6.P2 T40, the patches and kernel configurations no plan applies (#687)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-patches-dead-687`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`92f2f35c16` at `26875c972d` (one merge, carrying versions 1 and 2)); the pointer seeded after the second merge
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-patches-dead-687`; the T5, T6, T7, T8, T9, T12, T45 and T23 worktrees beside it (`m6-packages-dead-ends-670` read with `git show`, never checked out) (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`, `m6-tooling-build-supervision-656`, `m6-tooling-vm-harness-659`, `m6-tooling-council-692`, `m6-packages-dead-ends-670`), idle until their merges; nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #687 says otherwise
> **Epic:** #1054 (the patches and kernel configurations: this slice first, then T41, T42, T43); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Local -- **no reviewer seat**; `review-plan.json` records depth `local`, reviewers `[]`, *the lint and the counts are the check*; **`tools/council/run invoke` is never run**
> **The lens:** reachability -- one table of 778 patch and configuration rows with a class, a header-read provenance, an upstream status and a disposition each (brief § 1), the coverage table (778), the five classes, the x86_64 five as a bug, the 72 shadowed patches as T41/T42 leads, and the class paragraph for the maintainer beside T23's (brief § 4 Q1)
> **The rule:** **the lane removes nothing and edits no recipe** (D-WORKFLOW-209): no `.patch`, `.conf`, recipe or tool changes on this branch; the class (c) fix (a `patches/x86` rename and the cpugov slip) is a bug and a packet after the maintainer's word, never this lane's edit
> **The host:** M6's; this slice runs **no guest**, no build, no compiler, no fetch, no provider call; no plan generation and no network at all (`config/options ""` makes no request); `TMPDIR` under `/workspace/tmp/m6-t40/`; never `/tmp`
> **Register:** the three workflow IDs before 209 are the M7 lane's; D-WORKFLOW-209 is the removal rule (the coordinator's); a row this slice forces takes D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-033 or higher (032 is the M7 lane's); a row is never edited
> **The brief:** `docs/reviews/briefs/patches-dead.md` at `92f2f35c16` (version 2, after a stranger's proof); #687's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Handed back; idle** (2026-10-25, 05:48 UTC). The hand-back comment on #687 names the tip and every artifact.
- **Commits:** `reviewed-at` `b8cde6f305`, `fixed-at` `9c3fa25cfb` (both on #687's body).
- **The audit:** `docs/audits/2026_10_25-epic-m6-patches-dead/`. The lint passes in the pre-issue and resolution phases and with `--issue 1074`. #1074's 6 items are at outcomes.
- **The bugs** #1056, #1071 and #1072 are filed by the lane. Pointing comments are on #689 and #688.
- **The retro:** `docs/retros/2026-10-25-m6-patches-dead.md`, posted on #687.
- **The checkers:** `register-check`, `work-log-index --check`, `rules-check --quiet` and `hooks-test` rc 0. `forbidden-terms-check` is the coordinator's.
- **Left for the coordinator's re-run:** `/workspace/tmp/m6-t40` (the `curl` shim, the caches, the scratch).
- **Running for this lane:** nothing.

## Next commands

None. The lane waits for the coordinator's acceptance; after it: `audit-completion.json` from #1074's closed readback, and the full lint.

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, **then this branch**, then T9, T10, T12, T14, T15, T45, then T4's last.
When `next` moves, the **coordinator** merges `next` into this branch, and
never between stage A and stage D; the coordinator merges its own branch
into this one at hand-back, before the last criterion's checkers run. Never
merge another lane's feature branch here. Every lane and the M7 lane append
to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made by
whole entries. Nothing here builds, touches a device, a cloud account, a
provider, a key file, the host's swap, another lane's worktree, or a guest.

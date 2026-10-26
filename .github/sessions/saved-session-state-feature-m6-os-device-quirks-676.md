# Session pointer: M6.P2 T29, the per-handheld quirks (#676)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-os-device-quirks-676`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`feefe8fd13` at `453e25a000`, one merge, carrying the brief's versions 1 and 2, D-WORKFLOW-209, the device briefs and T27's errata); the lane's commits on top
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676`; the earlier worktrees of its session beside it, read with `git show`, never checked out again
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read** (`m7-signin-sm8550-build-20261025-01` is a name, never a path opened)
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #676 names (`m6-t5-build-engine`)
> **Epic:** #695 (the OS area: T1 and T22 accepted and closed out; this slice); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed packet (D-WORKFLOW-195), a probe first, as T27's stage C; `review-plan.json` records depth `independent`, one reviewer; **exactly one keyed invoke pair**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`
> **The lens:** brittleness under currency over 333 quirk files (88 entries: 65 model directories and 23 aliases; 328 upstream's, 5 the fork's) -- the selection by dt `model` or DMI first; tier B (70 paths / 2,885 lines: every board the shipped images boot that has an entry, and the VM) read line by line, tier A (the owned units' and the VM's 6 files) against the facts and the fixture, the rest by its generated table row; neither owned H700 unit selects a device entry
> **The rule:** **the lane changes nothing under `packages/`, `projects/` or `tools/` at stages A to D** (D-WORKFLOW-209: 328 of the 333 are upstream-carried, a removal is never proposed); the five fork-own files are the fork's to fix; **nothing runs on a unit** (D-QA-015; the RG35XX SP is the QA handheld, D-QA-027, and is still asked nothing); counts over the scripts are taken unfiltered (the credential filter drops `user` and `key` lines)
> **The host:** M6's; this slice runs **no guest** unless a boot-only behaviour is named on #676 and a window granted, no build, no compiler, no fetch, no plan generation, nothing on a handheld, no M7 build root read; `TMPDIR` under `/workspace/tmp/m6-t29/`; a `bin/` helper is proven with `tools/nova-led-test`'s fixture shape
> **Register:** D-WORKFLOW-209 is the highest Decided row on the coordinator's branch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); other lanes may take the next IDs; a row this slice forces (none expected) takes an ID the coordinator assigns on #676
> **The brief:** `docs/reviews/briefs/os-device-quirks.md` at `feefe8fd13` (version 2, after a stranger's proof of version 1); #676's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Idle after the hand-back.** Stages E to H are done: S1 `39851da3e8` (#1120), S2 `04a9fe98b9` (#1124), the record, the retro, the checkers, and `reviewed-at` / `fixed-at` in #676's body.
- **Waiting on the coordinator:** acceptance; the #1124 criterion's rewording; #1125, the rehearsal seed, which is outside the brief's files; #332 being closed for the two texts.
- **After acceptance:** `audit-completion.json` with T5's writer (`A` and `ISSUE=1121`), the full lint with `--issue 1121`, the pointer idle, and `/workspace/tmp/m6-t29/` removed.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-WORKFLOW-209' docs/decision-register.md                                 # 1 or more: the coordinator's tip is merged
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,140p' docs/reviews/briefs/os-device-quirks.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, T23, T40, T11, T27, T25, **then this branch**, then T9, T10, T12, T13,
T22, T14, T15, T45, then T4's last. When `next` moves, the **coordinator**
merges `next` into this branch, and never between stage A and stage D; the
coordinator merges its own branch into this one at hand-back, before the
last criterion's checkers run. Never merge another lane's feature branch
here. Every lane and the M7 lane append to `docs/decision-register.md`, the
day's work log and `docs/work-logs/INDEX.md`: keep every append, regenerate
the index, never edit another lane's rows; a merge with conflicts is checked
for leftover markers before it is committed (#696), and a union of two
ledgers is made by whole entries. T11's F-09 note (a merge of `next` keeps
GENERIC_X64 in the kernel override's version case), T27's PL-02 (upstream's
atf URL with both checksums) and #1099 (upstream's Qualcomm boot change:
both ABL slots' `Already written:`, the loader entry's identity) are the
coordinator's merge notes, inherited here for the record. Nothing here
builds, touches a device, a cloud account, a provider, a key file, the
host's swap, another lane's worktree, or a guest.

## Checkpoints

- Stage A: `e8dcd0ace5`, 2026-10-25 11:5x UTC.
- Stage B: `c5e473d264`, 2026-10-26 04:5x UTC.
- Stage C: `2831c85a8f`, 2026-10-26 05:21 UTC.
- Stage D: `ce2af0ca7c`, 2026-10-26 05:25 UTC (#1120, #1121).
- Stage E: S1 `39851da3e8`, S2 `04a9fe98b9`, the record `dcb2bf63c1`, 05:31 to 05:46 UTC.
- Stages F to H: this commit, 05:50 UTC.

# Session pointer: M6.P2 T25, the devices the fork does not ship and the other projects (#672)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-devices-unshipped-672`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`55e414441d` at `7d61fe0f96`, one merge, carrying the brief's versions 1 and 2, D-WORKFLOW-209 and the T11/T23/T24/T27 briefs); the lane's commits on top
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672`; the earlier worktrees of its session beside it (`m6-device-h700-674` and the build-engine ones, read with `git show`, never checked out again)
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #672 names (`m6-t5-build-engine`)
> **Epic:** #1082 (the devices: T11 accepted, T27 accepted and closed out, this slice, then T28); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Local -- a reachability table (plan § 6c, D-WORKFLOW-184): `review-plan.json` with `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184`; **no `tools/council/run` call, keyed or not**
> **The lens:** reachability -- one coverage row per path (397), one unit row per target, project and `packages/**` unit (25), each with the reads that decided its reach and its disposition in D-WORKFLOW-209's words; the pin table (T27's shape), the DTS-by-unit table (53), the drift against `651150fc88` by name
> **The rule:** **the lane changes none of the 397 and nothing under `packages/`, `projects/` or `tools/`** (D-WORKFLOW-209: a table removes nothing; the class decision for upstream-carried units is #346's, the coordinator's to put); RK3566 and RK3326 are *first widening, held* (D-WORKFLOW-185; order.md § 1 item 4: unshipped is not dead)
> **The host:** M6's; this slice runs **no guest, no build, no compiler, no fetch, no plan generation, no network read, nothing on a handheld, no M7 root read**; anything temporary under `/workspace/tmp/m6-t25/` after `df -i`, never `/tmp`
> **Register:** D-WORKFLOW-209 is the highest Decided row on 2026-10-25; T22 runs beside this lane and may take the next IDs; a row this slice forces (none expected) takes an ID the coordinator assigns on #672
> **The brief:** `docs/reviews/briefs/devices-unshipped.md` at `55e414441d` (version 2, after a stranger's proof of version 1); #672's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage A complete; stage B next** (updated 2026-10-25, 09:42 UTC).
- **`reviewed-at`:** `b27889bce2`. **The audit folder:** `docs/audits/2026_10_25-epic-m6-devices-unshipped/`, with `00`, `01` (§ Scope) and `stage-a/` (the runner, 17 outputs, `runs.tsv`, `paths.txt`, `rows.tsv`).
- **Every brief figure reproduced:** 397 / 49,555; 216 / 181; 396 / 1; 25 units; 12 targets; 39 M; 65; 1,424,530 bytes; the control 28 rows. One delta: RPi's `image:349` is a substring.
- **Next (stage B):** the tables generator under the audit folder's `tools/` (the coverage of 397 and the units of 25), then § The targets (12), § The projects (9), § The pins (10), § The device trees (53), § Mechanical checks, § Positives, `03`, `04` Q1 to Q7.
- **Running for this lane:** nothing.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-WORKFLOW-209' docs/decision-register.md                                 # 1 or more: the coordinator's tip is merged
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,120p' docs/reviews/briefs/devices-unshipped.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, T23, T40, T11, T27, **then this branch**, then T9, T10, T12, T13, T22,
T14, T15, T45, then T4's last. This branch carries only `docs/` and
`.github/sessions/` (a table slice changes no file under `packages/` or
`projects/`). When `next` moves, the **coordinator** merges `next` into
this branch, and never between stage A and stage D; the coordinator merges
its own branch into this one at hand-back, before the last criterion's
checkers run. Never merge another lane's feature branch here. Every lane
and the M7 lane append to `docs/decision-register.md`, the day's work log
and `docs/work-logs/INDEX.md`: keep every append, regenerate the index,
never edit another lane's rows; a merge with conflicts is checked for
leftover markers before it is committed (#696), and a union of two ledgers
is made by whole entries. T11's F-09 note (a merge of `next` keeps
GENERIC_X64 in the kernel override's version case) and T27's PL-02
(upstream's atf URL with both checksums) are the coordinator's merge notes,
inherited here for the record. Nothing here builds, touches a device, a
cloud account, a provider, a key file, the host's swap, another lane's
worktree, or a guest.

## Checkpoints

- (none yet; the executor appends one line per stage: the stage, the tip, the time)

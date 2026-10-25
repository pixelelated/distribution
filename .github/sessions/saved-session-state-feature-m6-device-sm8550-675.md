# Session pointer: M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-device-sm8550-675`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`5f4430f676` at `4beb95adf6`, one merge, carrying the brief's versions 1 and 2, D-WORKFLOW-209, the device briefs and T27's errata); the lane's commits on top
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675`; the earlier worktrees of its session beside it, read with `git show`, never checked out again
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read** (`m7-signin-sm8550-build-20261025-01` is a name, never a path opened)
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #675 names (`m6-t5-build-engine`)
> **Epic:** #1082 (the devices: T11 accepted, T27 accepted and closed out, T25 running, this slice last); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed packet (D-WORKFLOW-195), a probe first, as T27's stage C; `review-plan.json` records depth `independent`, one reviewer; **exactly one keyed invoke pair**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`
> **The lens:** currency, under cost against value -- the eight pins read from the recipes outside the slice at `8ebaf8daad` and `651150fc88`, the configuration's 7 / 7 (T41's row, read for the shape), the boot path by line (the kernel recipe, `scripts/mkimage`, `bootloader/mkimage`, `update.sh`, T1's `updateabl`) and upstream's 2026-10-22 replacement (#1099), the 16 trees, the device-facts rows L17 to L20, L27, L28, L31
> **The rule:** **the lane changes none of the 29 and nothing under `packages/`, `projects/` or `tools/` at stages A to D** (D-WORKFLOW-209); **nothing runs on the Nova** (D-QA-015, D-QA-027): a fact only the unit can show is a device-facts row, cited, never produced
> **The host:** M6's; this slice runs **no guest** (the guest cannot be an SM8550), no build, no compiler, no fetch, no plan generation, no network read, nothing on a handheld; `TMPDIR` under `/workspace/tmp/m6-t28/`
> **Register:** D-WORKFLOW-209 is the highest Decided row on the coordinator's branch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); other lanes may take the next IDs; a row this slice forces (none expected) takes an ID the coordinator assigns on #675
> **The brief:** `docs/reviews/briefs/device-sm8550.md` at `5f4430f676` (version 2, after a stranger's proof of version 1); #675's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage C: the refutation is running** (started 10:46:53 UTC).
- **The packet:** `second-opinions/gpt-brief.md`, 72 sources, scanned 0 hits.
- **The probe:** PASS.
- **The refutation:** a harness background task in this session. It writes `second-opinions/gpt-audit.md`, with its exit code in `/workspace/tmp/m6-t28/refutation.rc`. **If the session dies, read the rc file and the log; do not re-run the keyed call** (the seat has exactly two).
- **Next:** grade the seat's items in `04` § Second opinion; `05`; the pre-issue lint; the stage-C checkpoint. Then stage D.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-WORKFLOW-209' docs/decision-register.md                                 # 1 or more: the coordinator's tip is merged
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,140p' docs/reviews/briefs/device-sm8550.md
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

- Stage B: 10:43 UTC (the commit below)
- Stage A: 10:33 UTC (the commit below)

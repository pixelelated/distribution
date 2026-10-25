# Session pointer: M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the project's boot files (#658)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-device-generic-x64-658`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`5bb8828b71` at `d72afeff0a` (one merge, carrying versions 1 and 2)); the pointer seeded after the second merge
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-device-generic-x64-658`; the T5, T6, T7, T8, T9, T12, T45, T23 and T40 worktrees beside it (`m6-packages-dead-ends-670` read with `git show`, never checked out) (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`, `m6-tooling-build-supervision-656`, `m6-tooling-vm-harness-659`, `m6-tooling-council-692`, `m6-packages-dead-ends-670`), idle until their merges; nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #658 says otherwise
> **Epic:** #1082 (the devices: this slice first, then T27, T28, T25); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed packet (D-WORKFLOW-195), a probe first, as T13's stage C; `review-plan.json` records depth `independent`, one reviewer; **every other `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`, `--help` included**
> **The lens:** cost against value -- a read of the 58 paths (10,418 lines: the GENERIC_X64 device with its 7,754-line kernel configuration that has no base in the tree, the override kernel recipe, the driver and firmware lists, the four project boot files), a coverage table of 58, the configuration's three-part statement, the boot-file table, the launcher design (brief § 4)
> **The rule:** **the lane changes none of the 58 and nothing under `packages/`, `projects/` or `tools/` at stages A to D** (D-WORKFLOW-209): a dead end is a disposition, a fix is a stage-E stream the coordinator writes; the class decision for anything upstream carries is the maintainer's on #346
> **The host:** M6's; this slice runs **no guest** (the device it reads is the guest, whose boot T12 proved), no build, no compiler, no fetch, no plan generation; `TMPDIR` under `/workspace/tmp/m6-t11/`; the M7 lane holds a full build window and T13's guest cycle waits behind its FINAL RETURN
> **Register:** the three workflow IDs before 209 are the M7 lane's; D-WORKFLOW-209 is the removal rule (the coordinator's); a row this slice forces takes D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-033 or higher (032 is the M7 lane's); a row is never edited
> **The brief:** `docs/reviews/briefs/device-generic-x64-and-kernel.md` at `5bb8828b71` (version 2, after a stranger's proof); #658's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage A complete; stage B next** (updated 2026-10-25, 06:46 UTC).
- **`reviewed-at`:** `2103f0271d`. **The audit folder:** `docs/audits/2026_10_25-epic-m6-device-generic-x64-and-kernel/`, with `00`, `01` (§ Scope) and `stage-a/`.
- **Scope:** 58 / 10,418; read 14 / 1,820 / 1,421; tier 11 / 46 / 1; reach 49 / 9; GENERIC_X64 fork-own 1,217 (the order's 989 an erratum).
- **The configuration:** 659 / 351 against the Generic conf, 7,671 / 2,980 against AMD64. The header says 6.15.6; the recipe builds 7.1.2; `listnewconfig` is at `:306` and `oldconfig` at `:309` and `:315`.
- **History:** 110 / 40 / 70. **Upstream:** 7 M / 11 D.
- **The boot files:** `install` (`scripts/image:280`, fork-only, ROCKNIX header), `release` (`:285`), `mkimage` (`scripts/mkimage:225-263`), `rkhelper` (Rockchip u-boot only).
- **The launcher:** invoked by full path (`tools/vm-pair:36/74`); the basename is only in comments and help text. This delta was put to the coordinator on #658.
- **No guest, build, plan, fetch or council call so far.** The one seat comes at stage C.
- **Running for this lane:** nothing.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-generic-x64-658
cd "$D"   # no fetch of any kind: 651150fc88 is already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,160p' docs/reviews/briefs/device-generic-x64-and-kernel.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, T23, T40, **then this branch**, then T9, T10, T12, T14, T15, T45, then T4's last.
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

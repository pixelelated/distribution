# Session pointer: M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-device-h700-674`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`cc8b6cf2a3` at `d48302d739` (one merge, carrying versions 1 to 3)); the pointer seeded after the second merge
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-device-h700-674`; the earlier worktrees of its session beside it (`m6-packages-dead-ends-670` read with `git show`, never checked out) (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`, `m6-tooling-build-supervision-656`, `m6-tooling-vm-harness-659`, `m6-tooling-council-692`, `m6-packages-dead-ends-670`), idle until their merges; nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #674 names
> **Epic:** #1082 (the devices: T11 first, then this slice, T28, T25); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed packet (D-WORKFLOW-195), a probe first, as T13's stage C; `review-plan.json` records depth `independent`, one reviewer; **every other `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`, `--help` included**
> **The lens:** currency, under cost against value -- the pins (u-boot DDR3/DDR4 and the wrapper, the suspend stub, atf, the kernel 7.2) at `8ebaf8daad` and `651150fc88`, the configuration's 12 / 13 against upstream's own copy (the fork's six lines, D-SYS-002/003/004), the loader and the `/dtb.img` selection, the 15 device trees by unit, a coverage table of 28 (brief § 4)
> **The rule:** **the lane changes none of the 28 and nothing under `packages/`, `projects/` or `tools/` at stages A to D** (D-WORKFLOW-209); **nothing runs on the RG35XX SP or the RG SP** (D-QA-015, D-QA-027): a device fact is a `docs/releases/device-facts.md` row, read, never produced
> **The host:** M6's; this slice runs **no guest** (the guest cannot be an H700), no build, no compiler, no fetch, no plan generation, nothing on a handheld; `TMPDIR` under `/workspace/tmp/m6-t27/`
> **Register:** the three workflow IDs before 209 are the M7 lane's; D-WORKFLOW-209 is the removal rule (the coordinator's); a row this slice forces takes D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-033 or higher (032 is the M7 lane's); a row is never edited
> **The brief:** `docs/reviews/briefs/device-h700.md` at `cc8b6cf2a3` (version 3, after a stranger's proof); #674's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

Not started. The first commit on this branch is the running log's header,
`01-research-notes.md` § Scope, this pointer updated, and the day's
work-log entry headed `#674` (prose through a quoted heredoc or the Write
tool). `.qa-scratch/` is gitignored and `git status --short` is read before
every `git add -A`. No network is used at all.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-h700-674
cd "$D"   # no fetch of any kind: 651150fc88 is already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,160p' docs/reviews/briefs/device-h700.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, T23, T40, T11, **then this branch**, then T9, T10, T12, T14, T15, T45, then T4's last.
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

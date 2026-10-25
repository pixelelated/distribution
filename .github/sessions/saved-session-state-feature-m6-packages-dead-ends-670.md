# Session pointer: M6.P2 T23, the generic packages no image builds (#670)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-packages-dead-ends-670`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`16dee83d38` at `f532c23876`, `74b71ab443` at `36cb455e3c`); the pointer seeded after the second merge
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-packages-dead-ends-670`; the T5, T6, T7, T8, T9, T12 and T45 worktrees beside it (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`, `m6-tooling-build-supervision-656`, `m6-tooling-vm-harness-659`, `m6-tooling-council-692`), idle until their merges; nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #670 says otherwise
> **Epic:** #848 (the generic packages: T7 and T8 accepted; this slice is the area's last); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Local -- **no reviewer seat**; `review-plan.json` records depth `local`, reviewers `[]`, *the lint and the counts are the check*; **`tools/council/run invoke` is never run**
> **The lens:** reachability -- one table of 731 package units with a disposition each (brief § 1's six), the coverage table (1,604 paths), the disagreements between the inventory's `reach` and the lane's own plans, and the one class decision prepared for the maintainer (brief § 4 Q1)
> **The rule:** **the lane removes nothing and edits no recipe** (D-WORKFLOW-209): nothing under `packages/`, `projects/` or `tools/` changes on this branch; a proposed removal is a punch item with its `Already written:` line, deferred to the coordinator
> **The host:** M6's; this slice runs **no guest**, no build, no compiler, no fetch, no provider call; `tools/viewplan` is plan generation in Python (seconds); `TMPDIR` under `/workspace/tmp/m6-t23/`; never `/tmp`
> **Register:** the three workflow IDs before 209 are the M7 lane's; D-WORKFLOW-209 is the removal rule (the coordinator's); a row this slice forces takes D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-032; a row is never edited
> **The brief:** `docs/reviews/briefs/generic-packages-dead-ends.md` at `74b71ab443` (version 2, after a stranger's proof); #670's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage A complete; stage B next** (updated 2026-10-25, 04:21 UTC).
- **`reviewed-at`:** `27b015c901`. **The audit folder:** `docs/audits/2026_10_25-epic-m6-generic-packages-dead-ends/`. It holds `00`, `01` (§ Scope), `stage-a/` and `tools/t23-tables.py`, the generator that asserts 1,604, 727 and 731.
- **Scope:** 1,604 / 95,892 / 1,601 + 3 / 1,565 + 39 / 727 / 260, as the brief says. 731 units, 4 with the recipe outside the set.
- **Plans:** 593 / 605 / 235 / 672 / 238 on the host. The header has 611 for H700-aarch64; the six are its bootloader chain (`xmlstarlet` absent, `SUBDEVICES` empty).
- **Dispositions:** 603 dead upstream, 94 shadowed and live, 7 shadowed with the override dead too, 21 unshipped, 5 reached after all, 1 fork-own dead (`cbindgen`).
- **Every plan run uses the curl shim** (`PATH=/workspace/tmp/m6-t23/shim:$PATH`). Loading `mesa-reusable` calls `curl`; the first five runs (04:12:13-16) reached the network once each, which is recorded in `00` and the friction log.
- **`pkgcheck`:** the brief's path arguments match nothing (exit 0). The corrected sweep found 4 FAIL in 3 recipes; T6's leads are false positives.
- **Running for this lane:** nothing.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-packages-dead-ends-670
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git log --oneline c445081a59..upstream/next -- packages | wc -l                  # 0
sed -n '1,140p' docs/reviews/briefs/generic-packages-dead-ends.md
```

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

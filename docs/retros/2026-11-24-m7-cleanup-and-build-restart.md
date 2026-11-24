# Mini-retro: build-drive cleanup and the M7 build restart

**Reviewed:** 2026-11-24, 12:45 UTC, by the OS work coordinator. **Scope:** November 23–24. That covers the build-drive cleanup ([#493](https://github.com/pixelelated/distribution/issues/493), D-INFRA-033 to D-INFRA-038) and the restart of M7's integrated builds ([#555](https://github.com/pixelelated/distribution/issues/555), D-INFRA-039/040, [#1441](https://github.com/pixelelated/distribution/issues/1441), [#1442](https://github.com/pixelelated/distribution/issues/1442), [#1444](https://github.com/pixelelated/distribution/issues/1444)). This closes a phase of work, not M7 or any release-candidate gate. `tools/ceremony-check --gate` owed it: 8 active days since [the October 15 retro](2026-10-15-m7-audit-to-device-builds.md), which this one read for continuity. Its lessons were fixture state, visible readiness, source identity and publication boundaries.

**Delta.**
- **Free space:** 181.67 GB to 2,249.79 GB on `/workspace`, measured with `df -B1` before and after each batch. Batch 1 freed +1,001.04 GB, batch 2 +499.06, batch 3 +72.23, the batch 2 rerun +244.58, batch 4 +60.91, compaction +164.44 in total, the failed H700 worktree +122.09 and batch 5 +251.16. Receipts are in `docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/`.
- **PC build:** one cold build of `ee74f157` (build commit `3258f06c09`, 655 packages) succeeded and was qualified on the VM: 294/294 checks, the upgrade and Smart mGBA all passed. That is early evidence only.
- **Candidate head:** `ace312b0d2`, which is p9's handheld EmulationStation activation (`d86c089eab`) plus the #1441 fix. H700 is rebuilding cold from it.
- **Commits:** 44 on `next` (`aaa6799ce4`..`34950757e5`).

## What worked well?

- **Delete as the default.** The cleanup stopped holding once Max's words were relayed verbatim and written as rows in the same session (D-INFRA-035 at 04:29, D-INFRA-036 at 04:33, D-INFRA-037 at 04:38). Each later batch was a script with a use check, a receipt and `df` before and after. Batch 5 ran beside a live H700 build without touching it. The use check read the running container's mounts (`docker inspect`) and `/proc` cwd and fd links for every candidate. A tree walk was never used as the in-use check.
- **Failure records and single-use admissions.** Every failed build (PC `f5eabac3` and `1bfb5a21`, H700 `5746bff5` and `8b97f52f`) kept its thread logs and diagnosis and was consumed as failed-investigated with a fresh admission for the next attempt. The H700 failure at 12:22:39 was read, traced to one line and fixed (`ace312b0d2`), and a cold rebuild started at 12:27:52, five minutes from failure to observed start.
- **Parallel lanes.** pB (VM qualification) and p9 (handheld ES source) ran alongside the coordinator's builds, and both returns were consumed within minutes, p9's into the candidate head.
- **Relays checked against artifacts.** The steward checked the 12:35 note against the artifacts and raised two dispositions (the push gate and the two PC build roots). Both were acted on in the same turn (#1444; batch 5).

## What was harder than expected?

- **A day lost to a cleanup that kept by default** (friction 03:27 and 04:45). The tools asked each old build to prove it could be deleted, a proof it could not give. They counted "the next build fits" as progress. They held on our own mode-bit guard, an item bound of 65,536 and a keep-by-rename of an empty `sources/` stub. Max: *"We've lost pretty much a day of work here."*
- **Five launches to get two builds running** (#1445). The PC build was refused by the frozen line's build-owner reservation, then by the EmulationStation custody root, then broken by CMake toolchain files that the previous attempt had written at the host path. H700 was then refused at the Docker entry for two ABIs (#1442). Each showed up at launch or in the first packages, and no preflight caught any of them. The working route existed only in a register row, a checkpoint and a transcript.
- **A recipe failure 2 h 17 m into a cold build** (#1441). The cost is the whole ARM pass and most of aarch64, because the failure is in install, near the end.
- **The session's shell stopped for about two hours.** `/tmp` is a 31 GB tmpfs, so it holds RAM, not disk. It filled at about 10:07 and every Bash call failed with ENOSPC. The next attempt, at 12:23, worked. The H700 waiter armed before the outage still delivered the 12:22 failure. What filled it is unknown; 13 GB was in use at 12:23, about 12 GB of it session scratch.
- **`next` had not been pushed since November 18.** CI on `origin/next` has failed the issue-citation check since `9a51171c34`, a commit that cannot be reworded. Six more uncited commits, plus this retro's own absence, held 48 commits and every November 24 decision on one machine (#1444).
- **A timestamp ahead of the clock.** The 12:35 note to the steward was written at 12:32. Recorded memory says to read `date -u` for a heading; that was skipped once more.

## What did we discover?

- **Fixing every instance does not stop a later merge reintroducing the shape.** #497 fixed seven `build.${DISTRO}-` recipes in October. yabadabadoo-lr arrived with the November 18 M7 tree in the old form. The guard is a `fork-checks.yml` step now (`1272656075`).
- **A retention reason must name the artifact the test actually reads.** The November 21 keeper's 118 GB build root was protected "for the upgrade check". The check's own record (`pix-m7-pc-20261124-up-01/records/image-create-overlay.json`) shows its old guest was backed by `m7-generic-post-release-boot-owner-20261122-03/boot-output/reader.raw`, not the build root. The steward found it from the other side.
- **Generated build files capture the container path.** A root created at one path cannot be reused at another, so every M7 device build mounts its checkout at the EmulationStation custody root (`DOCKER_WORK_DIR`).
- **`build-admission`'s two profile checks disagree for two-ABI builds** (#1442): `admit()` lets unset keys pass and fills them only for one profile, while `nested()` demands an exact match.
- **The issue-citation gate had no route for a commit that reached history uncited** (#1444). One such commit made CI red on `origin/next` for six days without anyone acting on it.
- **D-WORKFLOW-199 had no issue.** Max's request went straight to a register row and a commit, so its issue (#1443) was filed after the fact.

## What adjustments are needed?

- **Add a task, #1445:** one command for the admitted Docker build route. SM8550 and the PC rebuild launch by hand with the documented exports until it exists. Its dry run refuses an existing build root, which would have caught `1bfb5a21`.
- **Modify the order:** none. H700, then SM8550, then the PC cold rebuild, all from `ace312b0d2`, then the PC clean-install and upgrade checks, as in the M7 milestone body (updated 12:29 UTC).
- **Retention plans:** the next plans protect `m7-generic-post-release-boot-owner-20261122-03/boot-output/`, the d7ca image and the `reader.raw` the upgrade check reads (about 8.4 GB), released when the PC upgrade check on `ace312b0d2` passes. They do not protect the removed keeper root or the earlier PC root.
- **Push `next`** once this retro is committed: `ceremony-check --gate` then has no BLOCK line (#1444 criterion 3).

## Scoped audit (Step 2.5)

- **AC conformance:** PARTIAL. #1441: 1/3 ticked (build and CI pending). #1443 closed with evidence. #1444: 2/3 (push pending). #555's H700 and SM8550 items are open while builds run. #493's checkpoint inventory still lists the `/workspace/tmp` and staging batch.
- **Cornerstone spot-check:** PASS on five checks.
  - Verify the artifact: every batch read `df -B1`, and the keeper finding came from the check's record, not its summary.
  - Guards fail closed: the DISTRO step passes only on git grep rc 1, and the late-citation record fails on unreadable, malformed and non-commit lines.
  - A promise is not a mechanism: the H700 waiter, watch-job and PIDs are named, and the checkpoint says nothing alerts after a disconnect.
  - No `pkill -f`: the bfs scan was stopped by PID.
  - Worktrees: removed with `tools/fork-worktree remove`.
- **Interaction-defect scan:** PARTIAL. Removal batches and a live build were combined safely through mount and `/proc` checks. One real interaction defect earlier in the window: a tree-walking `bfs` inventory held file descriptors and made batch 2 hold three checkouts. The checkpoint now forbids scans during a batch, but no tool enforces it.
- **Futro prediction verification:** SKIP. No futro ran for this phase. The futro ceremony is overdue in CI for epics since September; this retro does not pay it.
- **Housekeeping:** PASS. On `next` at 12:44 UTC: `register-check` (671 IDs), `rules-check` (30 files), `work-log-index --check`, `test-build-admission` (92 checks PASS) and `test-watch-job.py` (32 PASS, 0 FAIL).
- **UI review:** SKIP. No UI surface touched.
- **Harness self-coverage:** PARTIAL. The DISTRO step covers its failure (constructed recipe, rc 1), and the late-citation record covers its four failure shapes. The admission tests had no two-profile Docker case (#1442), and nothing pre-launch catches a stale root at another path (#1445).
- **Docs freshness:** PARTIAL. `device-builds.md` describes neither the `DOCKER_WORK_DIR` route nor the two-ABI export; tracked in #1445 and #1442 criterion 3. `issue-tracking.md` and `ceremonies.md` were updated with #1444.
- **Build-vs-adopt:** SKIP. Tooling and operations.

## Practice adjustments

- **A retention reason names the consumed artifact.** The build-cleanup skill already says a kept item names its size, reason, owner and release. This phase shows the reason can still be wrong while looking complete. Read the consumer's record of what it opened before naming it. Added to the skill's table of holds on `next` with this retro.
- **The retro is owed by the calendar, and here it was only run because the push gate refused.** No change: the gate did its job. The gap was that nobody read `--gate` for six days while committing locally. The OS checkpoint now lists the gate's state as an open item.

## Housekeeping (not blocking)

- About 12 GB of session scratch on the RAM-backed `/tmp` and the `/workspace/tmp` and staging batch remain from #493's inventory. That pass runs beside the builds.

## Code-verifiable state

| Item | Evidence |
| --- | --- |
| #1441 fix | `ace312b0d2`, `refs/m7/candidate-ace312b0`; pkgcheck rc 0 |
| DISTRO guard | `1272656075` (`.github/workflows/fork-checks.yml`) |
| Late citations | `34950757e5` (`tools/ceremony-check`, `docs/issue-citations.txt`) |
| H700 rebuild | run `20261124T122752Z-42bd4e9d`, admission `81112ccd5a9d41b1a1f029a2b972ea12` |
| Cleanup | `20261124-october-roots/`, `20261124-post-h700-pass/batch5.log` |

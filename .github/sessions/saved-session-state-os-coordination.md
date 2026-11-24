# Saved session state for OS work coordination

## Start here

Saved 2026-11-24T05:05Z on `feature/conflict-resolution` in the pixelelated distribution repository. Resume this file for the **OS work coordinator**, the sole dispatcher for M7. Since November 24 that role runs in **Claude Code on the latest Opus** (`claude-opus-5-5`) in Herdr pane `w4:p2`; session `b19c3b8c-1c4f-4a57-8765-0b8fe1f11ae9` (D-WORKFLOW-200). The one-on-one steward runs Claude Code on the latest Fable in `w4:pF` (session `2032b6b6-3946-42d0-ab2c-cfb5469deeea`); worker lanes run Codex on `gpt-6.2-sol`. The daily operations worktree is `/workspace/repos/rocknix.worktrees/conflict-resolution`; the primary checkout `/workspace/repos/rocknix` carries local `next`. pixelelated builds an immutable Linux gaming OS. This worktree's rules lag `next`: read them with `git show next:<path>` (`AGENTS.md`, `.claude/rules/worktrees.md`, `.claude/rules/device-builds.md`, `.claude/skills/build-cleanup/SKILL.md`).

Read the [M7 milestone](https://github.com/pixelelated/distribution/milestone/7) (body updated 05:02Z), [#493](https://github.com/pixelelated/distribution/issues/493) (cleanup outcome comment 05:0xZ) and [#555](https://github.com/pixelelated/distribution/issues/555) (build qualification). Decisions made this session, all on local `next`: D-INFRA-035 to D-INFRA-039 and D-WORKFLOW-200.

## Current focus

**1. The integrated M7 PC build is running (#555, D-INFRA-039).** Cold GENERIC_X64 build of `ee74f157` on branch `build/m7-pc-ee74f157-20261124` (worktree `/workspace/repos/rocknix.worktrees/m7-pc-ee74f157-20261124`). The branch is `ee74f157` plus `3258f06c09`, a tools-only commit bringing in `next`'s build tooling; every product path is identical. First started 05:01:27Z; the running attempt is the 05:06:15Z rerun below.

- Run: `<worktree>/.build-runs/20261124T050615Z-8fd0015c` (rerun started 05:06:15Z, admission `814c6c9390c9452c87e8e83e243060ef`). Runner PID 312931, command PID 313035, `watch-job` PID 312938, container `6ab33d39b1bd`. 655 packages.
- Run `20261124T050127Z-1bfb5a21` (05:01Z) failed at zlib:host. It reused toolchain CMake files that the 05:00 attempt had written at the host path; its thread logs are kept, it is consumed as failed-investigated, and the stale build root was removed.
- Owner records: `conflict-resolution/.build-runs/m7-pc-ee74f157-owner-20261124/` (plans, admissions, `submit-03/`).
- Launch environment, needed again for the H700/SM8550 builds: `DOCKER_WORK_DIR=/workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/m7-candidate-build-20261118-01/checkout` (the EmulationStation recipe's fixed custody root), and `DOCKER_EXTRA_OPTS` mounting the main `.git`, `/workspace/cache/rocknix-sources` at `$DOCKER_WORK_DIR/sources`, the ES tar directory `conflict-resolution/.build-runs/m7-candidate-build-20261118-01/inputs/es` read-only at `/tmp/pix-m7-es-source-delivery-20261110-01`, and `-e TMPDIR=/tmp`. The admission plan sets `container_checkout` to the same path.
- Nothing alerts after a disconnect. A resumed session reads `build.rc`/`build.status` in the run directory first. The run's processes are in the container's mount namespace, so from the host their cwd reads as the alias path above, not the real worktree.
- Two earlier attempts are retained: `20261124T045750Z-41d498f5` (rc 125, refused by the private line's build-owner reservation; no admission) and `20261124T050025Z-f5eabac3` (rc 2, ES build-root mismatch; consumed as failed-investigated). Always launch at the one container path; a build root created at another path must be removed first.

**2. Leftover cleanup continues beside it (#493, D-INFRA-035/036/037).** Batches 1–3 measured +1,001.04, +499.06 and +72.23 GB; free space went from 182 GB to about 1.74 TB. Records, scripts and receipts are in `docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/20261124-october-roots/`. Kept compact records are in `/workspace/artifacts/pixelelated-release-sources/retired-october-roots-20261124/`.

- The batch 2 rerun finished rc 0 at +244.58 GB. Batch 4 is running (`b4/runner.pid`, `b4/runner.rc`), chained with `compact-kept-records-r2.sh` (`compact-r2.log`).
- Next: `retire-old-build-roots-b4.sh` (23 older October worktrees, about 92 GB of images; hard-excludes the running build, the keeper and the alias), then `compact-kept-records-r2.sh`. After those: finished QA disks and extracted firmware, `/workspace/tmp` scratch, and staging under `/workspace/artifacts`, largest first.
- Never touch: the running build's worktree; the keeper `conflict-resolution/.build-runs/m7-ntfs-source-candidate-20261121-01/checkout`; `m7-candidate-build-20261118-01/inputs/es`; any candidate's `.git` (the keeper borrows their objects); the M6 directories `/workspace/tmp/m6-coordinator` and `/workspace/repos/pixelelated/distribution.worktrees` (D-INFRA-038); the lane monitor directory `/workspace/artifacts/pixelelated-release-sources/m7-lane-monitor-20261112-01`.
- Do not run a tree-walking scan while a removal batch runs: the batches' in-use check reads open file descriptors.

**3. Update at 09:15Z.** The PC build **succeeded**: rc 0 at 08:08:46Z. Images are in `m7-pc-ee74f157-20261124/target/`: `img.gz` sha256 `91a364aa…` and `.tar` sha256 `c6d753a8…`, identity build_commit `3258f06c09`, dirty no. The session was paused by its usage limit from about 05:15Z to 09:10Z, so the success was announced late.
- **Dispatched to `w4:pB`** (Codex `gpt-6.2-sol`, worktree `m7-source-delivery-20261103`) at 09:12:45Z, observed working at 09:12:51Z. It runs the VM qualification for #555/#1423/#1424: clean first boot with the installed-state checks, an upgrade from keeper `d7ca912480ea` with game-exit backup and slot restore, and the Smart mGBA default. Brief: `/workspace/tmp/rocknix-session/dispatch-pB-pcqual.txt`.
- **Dispatched to `w4:p9`** (`m7-clean-state-565`) at 09:14Z, observed working at 09:14:15Z. Source only: successor EmulationStation custody activations for H700/aarch64 and SM8550/aarch64. Today the recipe accepts only GENERIC_X64, so handheld builds would stop at emulationstation. Brief: `/workspace/tmp/rocknix-session/dispatch-p9-es-handheld.txt`.
- Harness waiters in this session poll each pane's status; nothing watches the workers after a disconnect. On resume, read each pane with `herdr agent read w4:pB` / `w4:p9`.
- The cleanup is at 2.02 TB free. Batch 4 and the second compaction finished rc 0 (+60.91 GB; compaction total +164.44 GB). The `/workspace/tmp` and staging batches are deferred until pB's VM qualification ends, so no deletion runs beside a live M7 check.
- Then, in order (also in the M7 milestone body since 09:15Z): H700 and SM8550 cold builds from p9's commit, with fresh admissions. **Rebuild the PC image cold from that same head, then rerun its clean-install and upgrade checks:** `release-candidates.md` step 2 needs one synced head and a shared BUILD_ID across targets, so pB's current run on `3258f06c09` is early evidence only. The keeper is retired after the upgrade check passes.

## Open items owned by OS

1. **The lane observer is down.** It stopped at 04:16Z with `PINNED_SESSION_CHANGED_STOPPED` when this pane moved to Claude Code. Its config pins the old Codex root session `01a0faa5-…`; the human-escalation config pins the old steward session `01a1e512-…`. Re-pin both in a new configuration generation before the next worker dispatch. No worker is working: `p9` and `pA`–`pD` show done, `p7` idle, and `p8`'s client has exited.
2. **After the PC build:** qualify the image on the VM (clean first boot and an upgrade from `d7ca912480ea`), then consume the run with the qualification evidence. Then H700 and SM8550, cold through the same route with fresh admissions (D-INFRA-033).
3. **Local `next` commits are not pushed:** `27b3d1b9f0`, `bc294ba4e2`, `67faae8bb5`, `0fa33fbd57`, `2862db7226`, `36a9cf6c59`, `d60d7f6cac`. Run the pre-push checks before any push.

## Files and ownership

| File or record | Purpose |
| --- | --- |
| `.github/sessions/saved-session-state-next.md` and the feature-branch selector | Link to this file and the steward's checkpoint. |
| `.claude/skills/build-cleanup/SKILL.md` (on `next`) | Cleanup procedure: delete is the default; keep one build, source, the download cache and compact records. |
| `docs/decision-register.md` (on `next`) | D-INFRA-035–039, D-WORKFLOW-200. |
| `docs/work-logs/2026_11-work_logs/2026_11_24-work_log.md` (this branch) | The 04:45Z entry on the cleanup. |
| `tools/herdr-lane` (on `next`) | Role selects harness and tier; refuses a Codex coordinator or steward. |

The worktree also holds unrelated modified instructions, package recipes, scripts, logs and untracked evidence from earlier sessions. Commit only the paths you own. Use the session-resume skill with the role **OS work coordinator**.

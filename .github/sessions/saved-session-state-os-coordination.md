# Saved session state for OS work coordination

## Start here

Saved 2026-11-24T15:56Z on `feature/conflict-resolution` in the pixelelated distribution repository. Resume this file for the **OS work coordinator**, the sole dispatcher for M7. Since November 24 that role runs in **Claude Code on the latest Opus** (`claude-opus-5-5`) in Herdr pane `w4:p2`; session `b19c3b8c-1c4f-4a57-8765-0b8fe1f11ae9` (D-WORKFLOW-200). The one-on-one steward runs Claude Code on the latest Fable in `w4:pF` (session `2032b6b6-3946-42d0-ab2c-cfb5469deeea`); worker lanes run Codex on `gpt-6.2-sol`. The daily operations worktree is `/workspace/repos/rocknix.worktrees/conflict-resolution`; the primary checkout `/workspace/repos/rocknix` carries local `next`. pixelelated builds an immutable Linux gaming OS. This worktree's rules lag `next`: read them with `git show next:<path>` (`AGENTS.md`, `.claude/rules/worktrees.md`, `.claude/rules/device-builds.md`, `.claude/skills/build-cleanup/SKILL.md`).

Read the [M7 milestone](https://github.com/pixelelated/distribution/milestone/7) (body updated 12:29Z), [#555](https://github.com/pixelelated/distribution/issues/555) (build qualification; 12:30Z comment), [#1441](https://github.com/pixelelated/distribution/issues/1441) (the H700 recipe failure) and [#1442](https://github.com/pixelelated/distribution/issues/1442) (the two-ABI admission refusal). Decisions made this session, all on local `next`: D-INFRA-035 to D-INFRA-040 and D-WORKFLOW-200.

## Current focus

**1. The SM8550 cold build of the candidate head `ace312b0d2` is running (#555).** `ace312b0d2` = `d86c089eab` (p9's EmulationStation source activation for H700/SM8550, PC binding unchanged) + the #1441 one-line recipe fix. Kept as `refs/m7/candidate-ace312b0`. **All three targets build from it** (H700, SM8550, the PC rebuild) so they share one BUILD_ID (`release-candidates.md` step 2).

- **H700 is built and verified, not qualified.** Run `m7-h700-ace312b0-20261124/.build-runs/20261124T122752Z-42bd4e9d` ran 12:27:52 to 15:47:21Z and exited 0 at 672/672.
  - Its image `0.0.1-dev+20261124T130236Z.gace312b0d2d3` has `BUILD_ID` `ace312b0d2`.
  - Its update tar's sha256 is `1151e733…`. The DDR3 and DDR4 `.img.gz` hashes are in `m7-h700-ace312b0-owner-20261124/ACCEPTANCE.json`.
  - It ships the 32-bit yabadabadoo core: #1441 criterion 2 is ticked.
  - It stays as the most recent build (D-INFRA-036/037) until handheld qualification and GitHub.
- **SM8550.** Worktree `/workspace/repos/rocknix.worktrees/m7-sm8550-ace312b0-20261124` (branch `build/m7-sm8550-ace312b0-20261124`).
  - Owner records: `conflict-resolution/.build-runs/m7-sm8550-ace312b0-owner-20261124/` (plans, report, admission `e7b1e73c4f984e72b0f17dad25e9bfba`, `submit-02/`).
  - Run `<worktree>/.build-runs/20261124T155230Z-1d5546ee`, started 15:52:30Z after the guarded swap reclaim at 15:51Z. It does 258 ARM tasks, then about 672 aarch64.
  - Runs `15fc928c` and `07e9da7a` stopped before compiling (`REFUSED-BEFORE-COMPILE.json`, #1445): the plan protected a path batch 5 removed, and an ungated `| tail` chain hid it.
- **Delivery.** A harness waiter (`bv36skydh`) is on `build.rc` while this session is connected. Nothing alerts after a disconnect. A resumed session reads `build.rc`/`build.status` first. The container's processes show the alias path below as their cwd, not the real worktree.
- **Launch environment** (for the PC rebuild too):
  - `export PROJECT=ROCKNIX DEVICE=<D> ARCH=<last ABI>`. This is needed for two-ABI admissions (#1442).
  - `DOCKER_WORK_DIR=/workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/m7-candidate-build-20261118-01/checkout`. This is the EmulationStation recipe's fixed custody root.
  - `DOCKER_EXTRA_OPTS="-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v /workspace/cache/rocknix-sources:$DOCKER_WORK_DIR/sources -v <that root's parent>/inputs/es:/tmp/pix-m7-es-source-delivery-20261110-01:ro -e TMPDIR=/tmp"`.
  - The admission plan's `container_checkout` is the same alias.
- **Launch sequence:**
  1. `tools/fork-worktree add-build <name> <commit>`
  2. `mkdir -m 0755 <wt>/sources`
  3. the retention report (`tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report ...`); first check that every `protected` path still exists
  4. `build-admission prepare`
  5. `tools/build-preflight --reclaim-swap`
  6. `tools/watch-build-submit --owner <owner>/submit-NN -- --admission <admission> -- make docker-<D>`
- **Run the launch under `set -o pipefail`, with an explicit stop after each step.** Check for a running build with `ps -C make -o args=`, never `pgrep -f` (it matches the launching shell). SM8550's gated command is in this session's transcript at 15:52Z.
- The first H700 attempt from `d86c089eab` (run `20261124T100549Z-8b97f52f`) is consumed as failed-investigated (`m7-h700-d86c089e-owner-20261124/`).

**2. Then, in order:** the PC (GENERIC_X64) cold rebuild from `ace312b0d2`; then the PC clean-install and upgrade checks on that image (dispatch to a worker lane, as pB ran them on `3258f06c09`); then H700 and SM8550 qualification. Builds run one at a time. Before each: recheck free space and swap, and reclaim swap only while no guest or compiler runs.

**3. Evidence already in hand.** The PC image of `ee74f157` (build commit `3258f06c09`; `m7-pc-ee74f157-20261124/target/`, img.gz sha256 `91a364aa…`, tar `c6d753a8…`) passed pB's VM checks: 294/294 clean first boot, an upgrade from keeper `d7ca912480ea` with game-exit backup and slot restore, and the Smart mGBA default (`m7-source-delivery-20261103/docs/qa-logs/2026-11-24-integrated-pc-vm/RESULT.json`, sha256 `409ab8d7…`). It is early evidence only, because it is not the candidate head. Its run `20261124T050615Z-8fd0015c` is consumed as qualified (12:3xZ). That image is the kept warm base until the next build supersedes it (D-INFRA-037).

**4. Cleanup (#493, D-INFRA-035/036/037/038).** 2.250 TB free on `/workspace` at 12:40Z, after batch 5 (+251.16 GB: both GENERIC_X64 build roots, the earlier PC root and the November 21 keeper root, the two gtk4 worktrees, `rc-device-fixes` roots and the `/tmp` policy worktree; `20261124-post-h700-pass/batch5.log`). The keep set is now the running SM8550 build and the H700 build of the same head (most recent, not on GitHub), plus `m7-pc-ee74f157-20261124/target` (pB-qualified images, released when the PC image of `ace312b0d2` exists) and `m7-generic-post-release-boot-owner-20261122-03/boot-output/` (the d7ca image and `reader.raw` the PC upgrade check reads, released when that check passes on `ace312b0d2`). Batches 1–4 and two compactions are done; records in `docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/20261124-october-roots/`. **Deferred and now unblocked** (pB's VM qualification has ended): finished QA disks and extracted firmware, `/workspace/tmp` scratch and staging under `/workspace/artifacts`, largest first. Exclude the M6 directories (`/workspace/tmp/m6-coordinator`, `/workspace/repos/pixelelated/distribution.worktrees`, any `m6-*`), `/workspace/tmp/rocknix-session`, git object stores referenced as alternates (a `find` for `objects/info/alternates` under `/workspace/repos`, `/workspace/artifacts` and `/workspace/tmp` returned no paths, but it ran under a 300 s timeout and may have been cut short, so it is not conclusive; e.g. `/workspace/tmp/pix-m7-november-textual-merge-20261113-04` is a known store), files with more than one link, the running build's inputs (`m7-candidate-build-20261118-01/inputs/es`, the sources cache) and the keeper. Also the RAM-backed `/tmp` (tmpfs, 31 GB): about 12 GB of leftover session directories (`m7-493-*`, `pixelelated-policy-20261119`, `m6-assess-*` (M6-owned, leave), `pix-*`, `m7-es-handheld-activation.*`). The November 21 keeper's build root (`m7-ntfs-source-candidate-20261121-01/checkout/build.*`) is already gone (batch 5); its checkout's `.git` and update tar remain.

## Open items owned by OS

1. **No GitHub Actions workflow has run on the fork since 2026-10-29** ([#1446](https://github.com/pixelelated/distribution/issues/1446)). The November 18 and November 24 pushes started none, and the build host's token cannot read the Actions settings (HTTP 403). Every CI guard is silent, including the #1441 DISTRO step. Needs someone with org or repo Actions and billing access. The steward put it to Max in the one-on-one at about 14:47Z; wait for the relayed answer there (D-WORKFLOW-201).
2. **Batch 6 (`/workspace/tmp` compaction) awaits Max's yes.** Claude Code's auto-mode review refused the first version at 12:49Z and nothing ran (`20261124-post-h700-pass/REFUSAL-batch6.json`). After the steward's read-only preview (7,824 files, about 496 GB in 482 of 2,177 entries), the script was revised at about 12:56Z:
   - the November 5 PC image folder is a named keep (`KEEP-named-items.json`);
   - pictures are kept as frames;
   - `held.py` re-checks holders right before each entry's deletion.
   The new script sha256 starts `f06842247be9d0c0` and `held.py` starts `d4cfa4d580150a75`. The fixture run passed. The steward put it to Max in the one-on-one at about 14:47Z. Do not start it until the steward relays his exact yes (D-WORKFLOW-201, #1447). Then submit exactly that script. If the review refuses it again, send the refusal back to the one-on-one unchanged. /workspace/tmp will not be at the keep set afterwards: small generated output stays. The `/workspace/artifacts` pass (candidate stores, build custody, release sources) has not started and needs per-item review, because D-INFRA-033 holds a deliverable missing from GitHub.
2a. **The PC upgrade check on `ace312b0d2` starts from `672a7c995f`** (November 5 PC image, the build on the handhelds; `release-candidates.md` step 3), with `d7ca912480ea` as a second starting point (#555 comment).
3. `next` was pushed at 12:47Z (`9a51171c34..29bc9fd857`) and 12:51Z (`..6e30af8fac`); `ceremony-check --gate` prints no BLOCK line. The audit and futro ceremonies remain overdue (CI-red only). The retro is `docs/retros/2026-11-24-m7-cleanup-and-build-restart.md`.
4. **The lane observer is down** and its config pins the old Codex root session `01a0faa5-…`. The human-escalation config pins the old steward session `01a1e512-…`. Re-pin both before relying on them; `herdr agent prompt w4:pF` reaches the steward directly.
5. Open issues from today: #1441 (criterion 3, waits on CI), #1442 (two-ABI admission), #1444 (criterion 3), #1445 (one command for the build route; a failing-step criterion added after the SM8550 launch). #1443 is closed.
6. **#1447: Max speaks in one place (D-WORKFLOW-201).** Every question for Max goes to the one-on-one, never into this tab. The rule landed on `next` in `3aab3ee850` (pushed at 14:52Z). Still open: integrate or retire the rest of the uncommitted lane text in this worktree. That is the D-WORKFLOW-183/184/187/189/190/194/195 sections of `engineering-practices.md`, the 441-line `docs/coordination-continuity.md`, `docs/coordinator-one-on-one.md`, `tools/coordinator-escalation` and `tools/m7-lane-watch`.

## Files and ownership

| File or record | Purpose |
| --- | --- |
| `.github/sessions/saved-session-state-next.md` and the feature-branch selector | Link to this file and the steward's checkpoint. |
| `.claude/skills/build-cleanup/SKILL.md` (on `next`) | Cleanup procedure: delete is the default; keep one build, source, the download cache and compact records. |
| `docs/decision-register.md` (on `next`) | D-INFRA-035–040, D-WORKFLOW-200. |
| `docs/work-logs/2026_11-work_logs/2026_11_24-work_log.md` | 04:45Z cleanup entry; 12:33Z #1441 entry. Untracked here, committed to `next` by content in `1272656075`. |
| `.github/workflows/fork-checks.yml` (on `next`) | The DISTRO build-root guard (#1441). |
| `tools/herdr-lane` (on `next`) | Role selects harness and tier; refuses a Codex coordinator or steward. |

The worktree also holds unrelated modified instructions, package recipes, scripts, logs and untracked evidence from earlier sessions. Commit only the paths you own. Use the session-resume skill with the role **OS work coordinator**.

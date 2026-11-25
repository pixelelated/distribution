# Saved session state for OS work coordination

## Start here

Saved 2026-11-25T02:07Z on `feature/conflict-resolution` in the pixelelated distribution repository. Resume this file for the **OS work coordinator**, the sole dispatcher for M7. Since November 24 that role runs in **Claude Code on the latest Opus** (`claude-opus-5-5`) in Herdr pane `w4:p2`; session `b19c3b8c-1c4f-4a57-8765-0b8fe1f11ae9` (D-WORKFLOW-200). The one-on-one steward runs Claude Code on the latest Fable in `w4:pF` (session `2032b6b6-3946-42d0-ab2c-cfb5469deeea`); worker lanes run Codex on `gpt-6.2-sol`. The daily operations worktree is `/workspace/repos/rocknix.worktrees/conflict-resolution`; the primary checkout `/workspace/repos/rocknix` carries local `next`. pixelelated builds an immutable Linux gaming OS. This worktree's rules lag `next`: read them with `git show next:<path>` (`AGENTS.md`, `.claude/rules/worktrees.md`, `.claude/rules/device-builds.md`, `.claude/skills/build-cleanup/SKILL.md`).

Read the [M7 milestone](https://github.com/pixelelated/distribution/milestone/7) (body updated 12:29Z), [#555](https://github.com/pixelelated/distribution/issues/555) (build qualification; 12:30Z comment), [#1441](https://github.com/pixelelated/distribution/issues/1441) (the H700 recipe failure) and [#1442](https://github.com/pixelelated/distribution/issues/1442) (the two-ABI admission refusal). Decisions made this session, all on local `next`: D-INFRA-035 to D-INFRA-043 and D-WORKFLOW-200. Also read [#1448](https://github.com/pixelelated/distribution/issues/1448) (the SM8550 fex-emu stop).

## Current focus

**00. Newer (2026-11-25T02:07Z).**
- **H700 of `0a3e979e50` is running: the set's last image.**
  - Started 02:04:06Z as run `20261125T020406Z-f7a619db` in `/workspace/repos/rocknix.worktrees/m7-h700-0a3e979e-20261125` (branch `build/m7-h700-0a3e979e-20261125`), with owner `conflict-resolution/.build-runs/m7-h700-0a3e979e-owner-20261125/`.
  - Watcher 3012000, job 3011996, `make` 3012100, launcher 3011991.
  - The memory log is the owner's `memory-watch.log`.
  - Consume it like PC: `build.rc`, `runner-result.json`, `submit-01/launcher-result.json`, `tool-wrapper.rc`, process cleanup, the identity file, `os-release` and the hashes. Write `ACCEPTANCE.json`.
  - Then run `tools/rc-preflight --only build-set --build-set <SM8550 target> --build-set <PC target> --build-set <H700 target>` and quote it on #555.
- **PC of `0a3e979e50` is accepted** (`m7-pc-0a3e979e-owner-20261124/ACCEPTANCE.json`, #555).
  - Its root was removed (+128.4 GB).
  - Kept: `m7-pc-0a3e979e-20261124/target/` and `kept/emulationstation-m7-20261110-0d852e5d1106/emulationstation`.
  - The `ee74f157` PC `target/` is a named keep item whose release event ("the PC image of the set's final head exists") holds once H700 confirms the head. Remove it then.
- **CI (#1446): GitHub paused workflows on this fork for the scale of its Actions usage.** The banner is on the public Actions page.
  - An owner must re-enable workflows; the steward is asking Max.
  - Done on `next`: the wordlist tree scan greps in batches (3 min → 4 s), the wordlist checkout is treeless, and `tools/ci-silence-check` gains a `pause` item.
  - Once workflows return: read the first `fork wordlist check` run's step times, and read `fork record checks` (#1446 criteria 2–3, #1441 criterion 3, #1450 criteria 1 and 5).
- **The /tmp scratch removal (267 M7 entries, 4.6 GB) was refused at 02:02Z** and sent to `w4:pF` by pane; receipt is the pane going `working` at 02:02:42Z. It waits on Max. Record: `REFUSAL-tmp-m7.json`.
- **Deliver to the steward by pane, never by session name (#1447).** Run `herdr agent get w4:pF` (session `2032b6b6-3946-42d0-ab2c-cfb5469deeea`), then `herdr agent prompt w4:pF`. Take receipt from the pane's status changing.
- **Batch 6's ten leftovers are removed (D-INFRA-045)**, +26.26 GB. The 13-04 store and `root02` are named keep items.

**0. Latest (2026-11-24T23:05Z; supersedes the running/next parts of items 1, 2 and 4 below).**
- **SM8550 of `0a3e979e50` is accepted.** Run `20261124T184914Z-84d3f121`, rc 0; record `m7-sm8550-0a3e979e-owner-20261124/ACCEPTANCE.json`; #1448 criteria 1–3 ticked.
  - Its build roots were removed (+183.41 GB, `REMOVAL-build-roots.json`).
  - Kept: `m7-sm8550-0a3e979e-20261124/target/` and `kept/emulationstation-m7-20261110-0d852e5d1106/emulationstation` (sha256 `edcb8d26…`).
- **The PC cold build of `0a3e979e50` is running.** Started 22:54:54Z: run `20261124T225454Z-289bae16` in `/workspace/repos/rocknix.worktrees/m7-pc-0a3e979e-20261124` (branch `build/m7-pc-0a3e979e-20261124`), owner `conflict-resolution/.build-runs/m7-pc-0a3e979e-owner-20261124/`, watcher pid 1774390, job 1774384.
  - Consume it from `build.rc`, `runner-result.json`, `submit-01/launcher-result.json` and `tool-wrapper.rc`, then check process cleanup, the identity file and both hashes.
  - Then remove its build root, keeping `target/` and the unstripped ES binary.
  - Then H700 cold from the final head, last; then `tools/rc-preflight --only build-set` over the three `target/` folders.
- **Batch 6 is done** (D-INFRA-044): rc 0, +489.74 GB, outcome on #493.
  - 26.6 GB remains in `/workspace/tmp` outside the keep set: 11 git object stores and 2 held entries (`batch6-left-not-keep.txt`).
  - Removing those deletes more than batch 6 did, so it goes to the one-on-one first.
  - `KEEP-named-items.json` now names the set's final head in its release events.
- **CI (#1446, #1450).** Max set Actions budgets at about 22:37Z; a push at 22:38Z still got no check suite, so the budgets did not restore CI. Owner-only pages remain unread (Actions policy, audit log, payment).
  - #1450 (Max's *"why'd this go unnoticed?"*): on `next` and pushed in `4eb89d2e4c`, `f7f7755e8b` and `95e97bb50f`.
    - `tools/ci-silence-check`.
    - The push guard prints it for every push of `next` (criterion 2 ticked).
    - `rc-preflight --only ci` (D-WORKFLOW-202, criterion 3 ticked).
    - `fork-checks.yml` split into `guards` and `records` jobs.
    - Criteria 1 and 5 wait for a live run after Actions returns.
  - The daily timer (criterion 4) is blocked by #1451: `tools/coordinator-escalation`, `tools/m7-lane-watch` and `tools/priority-check` were never committed to any branch, and the rule text naming them is uncommitted in this worktree. Integrating them is coordinator work, and it comes next once the PC build is consumed.
  - Swap refilled to 7 of 8 GB within ten minutes of the 22:5xZ reclaim, with about 38 GB of RAM available. Watch the PC build for memory pressure.
  - Note: `0a3e979e50` is not on GitHub at all (`check-suites` answers 404), so the M7 head has never been checked by CI.

**1. The SM8550 cold build of `0a3e979e50` is running (#555, #1448).** `0a3e979e50` = `ace312b0d2` with `fex-emu`'s fork patch `0006` deleted. Upstream's `0003` in the November 18 tree already carries its change, so `0006` stopped the first SM8550 run at `[706/736]` unpack. Kept as `refs/m7/candidate-0a3e979e`. **Image heads (D-INFRA-043, #1449, reverses D-INFRA-042):** the whole M7 set comes from one commit with one build ID, now `0a3e979e50`. Max at about 19:21Z: *"make sure we institutionalize it and store that as our preference"*. SM8550 continues; the PC is rebuilt cold from `0a3e979e50`; H700 is rebuilt cold from the final head last. If a fix moves the head again, the not-yet-built targets take the new head and the built ones are rebuilt last. `ace312b0d2` stays `refs/m7/candidate-ace312b0`.

- **H700 of `ace312b0d2` is released (D-INFRA-043).** It was built and verified (run `20261124T122752Z-42bd4e9d`, 672/672, 32-bit yabadabadoo core shipped, #1441 criterion 2 ticked from it). Its build roots went at 16:00Z (+145.5 GB). Its `target/` worktree and the unstripped ES binary went at 19:26Z (+6.95 GB net, `REMOVAL-images.log`), because these images are no longer the ones to qualify. Its records, image hashes and `build.log.zst` are in `m7-h700-ace312b0-owner-20261124/` (`ACCEPTANCE.json`, `RELEASED.json`, `runs/`).
- **SM8550.** Worktree `/workspace/repos/rocknix.worktrees/m7-sm8550-0a3e979e-20261124` (branch `build/m7-sm8550-0a3e979e-20261124`).
  - Owner records: `conflict-resolution/.build-runs/m7-sm8550-0a3e979e-owner-20261124/` (plans, report, admission `9d93d899cd2b492c8568531841d0a0ec`, `submit-01/`).
  - Run `<worktree>/.build-runs/20261124T184914Z-84d3f121`, started 18:49:14Z after the guarded swap reclaim (8 GB used to 0). 258 ARM tasks, then about 736 aarch64.
  - The first run, `20261124T155230Z-1d5546ee` of `ace312b0d2`, is consumed as failed-investigated (`m7-sm8550-ace312b0-owner-20261124/FAILED-INVESTIGATED.json`; worktree removed, +148.44 GB). Its earlier refused launches are in `REFUSED-BEFORE-COMPILE.json` there.
  - Before the relaunch, the patches of the 15 unreached packages no build of the head had unpacked were replayed against pinned sources: 43 applications, 0 failures (`/workspace/tmp/rocknix-session/patch-replay-sm8550.sh`, seen to fail on the old `fex-emu`).
- **Delivery.** A harness waiter (`bvrffk3mf`) is on `build.rc` while this session is connected. Nothing alerts after a disconnect. A resumed session reads `build.rc`/`build.status` first. The container's processes show the alias path below as their cwd, not the real worktree.
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
  5. `tools/build-preflight --reclaim-swap 2>&1 | tee <owner>/PREFLIGHT-reclaim-swap.txt` (the record lives in the owner folder, not only the terminal; #555, 23:08Z). Remove `/tmp` (tmpfs) leftovers first: tmpfs pages refill swap within minutes of a reclaim.
  6. `tools/watch-build-submit --owner <owner>/submit-NN -- --admission <admission> -- make docker-<D>`
- **Run the launch under `set -o pipefail`, with an explicit stop after each step.** Check for a running build with `ps -C make -o args=`, never `pgrep -f` (it matches the launching shell). SM8550's gated command is in this session's transcript at 15:52Z.
- The first H700 attempt from `d86c089eab` (run `20261124T100549Z-8b97f52f`) is consumed as failed-investigated (`m7-h700-d86c089e-owner-20261124/`).

**2. Then, in order (D-INFRA-043):** (a) the PC (GENERIC_X64) cold from `0a3e979e50`. Before launching it, remove the SM8550 build roots and generated caches after the use check, and keep SM8550 `target/` and its unstripped ES binary (`emulationstation-*` under `build.pixelelated-SM8550.aarch64/build/`) as named items. Its patches are proven: the `3258f06c09` cold build differs only in the ES custody binding, the yabadabadoo path and `fex-emu` (not built on x86). (b) H700 cold from the final head, last; before it, remove the PC build roots and keep the PC `target/`. (c) `tools/rc-preflight --tree <final-head worktree> --only build-set --build-set <SM8550 target> --build-set <PC target> --build-set <H700 target>` must PASS; quote it on #555. (d) The PC clean-install and upgrade checks on that PC image, dispatched to a worker lane (as pB ran them on `3258f06c09`), from `672a7c995f` with `d7ca912480ea` as a second start; no guest runs beside a cold build. (e) H700 and SM8550 qualification. Builds run one at a time. Before each: recheck free space and swap, and reclaim swap only while no guest or compiler runs. A fix that moves the head again: not-yet-built targets take the new head, built ones are rebuilt last, and their VM checks rerun.

**3. Evidence already in hand.** The PC image of `ee74f157` (build commit `3258f06c09`; `m7-pc-ee74f157-20261124/target/`, img.gz sha256 `91a364aa…`, tar `c6d753a8…`) passed pB's VM checks: 294/294 clean first boot, an upgrade from keeper `d7ca912480ea` with game-exit backup and slot restore, and the Smart mGBA default (`m7-source-delivery-20261103/docs/qa-logs/2026-11-24-integrated-pc-vm/RESULT.json`, sha256 `409ab8d7…`). It is early evidence only, because it is not the candidate head. Its run `20261124T050615Z-8fd0015c` is consumed as qualified (12:3xZ). That image is the kept warm base until the next build supersedes it (D-INFRA-037).

**4. Cleanup (#493, D-INFRA-035/036/037/038).** 2.250 TB free on `/workspace` at 12:40Z, after batch 5 (+251.16 GB: both GENERIC_X64 build roots, the earlier PC root and the November 21 keeper root, the two gtk4 worktrees, `rc-device-fixes` roots and the `/tmp` policy worktree; `20261124-post-h700-pass/batch5.log`). The keep set is now the running SM8550 build of `0a3e979e50` (the H700 images of `ace312b0d2` were released at 19:26Z under D-INFRA-043), plus `m7-pc-ee74f157-20261124/target` (pB-qualified images, released when the PC image of the final head exists) and `m7-generic-post-release-boot-owner-20261122-03/boot-output/` (the d7ca image and `reader.raw` the PC upgrade check reads, released when that check passes on the PC image of the set's final head). Batches 1–4 and two compactions are done; records in `docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/20261124-october-roots/`. **Deferred and now unblocked** (pB's VM qualification has ended): finished QA disks and extracted firmware, `/workspace/tmp` scratch and staging under `/workspace/artifacts`, largest first. Exclude the M6 directories (`/workspace/tmp/m6-coordinator`, `/workspace/repos/pixelelated/distribution.worktrees`, any `m6-*`), `/workspace/tmp/rocknix-session`, git object stores referenced as alternates (a `find` for `objects/info/alternates` under `/workspace/repos`, `/workspace/artifacts` and `/workspace/tmp` returned no paths, but it ran under a 300 s timeout and may have been cut short, so it is not conclusive; e.g. `/workspace/tmp/pix-m7-november-textual-merge-20261113-04` is a known store), files with more than one link, the running build's inputs (`m7-candidate-build-20261118-01/inputs/es`, the sources cache) and the keeper. Also the RAM-backed `/tmp` (tmpfs, 31 GB): about 12 GB of leftover session directories (`m7-493-*`, `pixelelated-policy-20261119`, `m6-assess-*` (M6-owned, leave), `pix-*`, `m7-es-handheld-activation.*`). The November 21 keeper's build root (`m7-ntfs-source-candidate-20261121-01/checkout/build.*`) is already gone (batch 5); its checkout's `.git` and update tar remain.

## Open items owned by OS

1. **No GitHub Actions workflow has run on the fork since 2026-10-29** ([#1446](https://github.com/pixelelated/distribution/issues/1446)). The November 18 and November 24 pushes started none, and the build host's token cannot read the Actions settings (HTTP 403). Every CI guard is silent, including the #1441 DISTRO step. Needs someone with org or repo Actions and billing access. The steward put it to Max in the one-on-one at about 14:47Z; wait for the relayed answer there (D-WORKFLOW-201).
2. **Batch 6 (`/workspace/tmp` compaction) awaits Max's yes.** Claude Code's auto-mode review refused the first version at 12:49Z and nothing ran (`20261124-post-h700-pass/REFUSAL-batch6.json`). After the steward's read-only preview (7,824 files, about 496 GB in 482 of 2,177 entries), the script was revised at about 12:56Z:
   - the November 5 PC image folder is a named keep (`KEEP-named-items.json`);
   - pictures are kept as frames;
   - `held.py` re-checks holders right before each entry's deletion.
   The new script sha256 starts `f06842247be9d0c0` and `held.py` starts `d4cfa4d580150a75`. The fixture run passed. The steward put it to Max in the one-on-one at about 14:47Z. Do not start it until the steward relays his exact yes (D-WORKFLOW-201, #1447). Then submit exactly that script. If the review refuses it again, send the refusal back to the one-on-one unchanged. /workspace/tmp will not be at the keep set afterwards: small generated output stays. The `/workspace/artifacts` pass (candidate stores, build custody, release sources) has not started and needs per-item review, because D-INFRA-033 holds a deliverable missing from GitHub.
2a. **The PC upgrade check on the PC image of the set's final head (D-INFRA-043; `0a3e979e50` unless a fix moves it) starts from `672a7c995f`** (November 5 PC image, the build on the handhelds; `release-candidates.md` step 3), with `d7ca912480ea` as a second starting point (#555 comment).
3. `next` was pushed at 12:47Z (`9a51171c34..29bc9fd857`) and 12:51Z (`..6e30af8fac`); `ceremony-check --gate` prints no BLOCK line. The audit and futro ceremonies remain overdue (CI-red only). The retro is `docs/retros/2026-11-24-m7-cleanup-and-build-restart.md`.
4. **The lane observer is down** and its config pins the old Codex root session `01a0faa5-…`. The human-escalation config pins the old steward session `01a1e512-…`. Re-pin both before relying on them; `herdr agent prompt w4:pF` reaches the steward directly.
4a. **The P3 Tiny becomes the dedicated build machine, serval the development machine, once it is set up (D-INFRA-041, #1419).** Max is building its rack, and no date is set. The M7 build set stays here meanwhile. #1419 holds the first-build checklist. Copying `~/.ROCKNIX/options` there needs Max's yes, through the one-on-one.
5. Open issues from today: #1441 (criterion 3, waits on CI), #1442 (two-ABI admission), #1444 (criterion 3), #1445 (one command for the build route; a failing-step criterion added after the SM8550 launch), #1449 (one build set, one commit: criteria 1–3 done on `next` in `64986c543f`; 4 is the M7 set PASS; 5 is the #1445 criterion), #1448 (criteria 1–3 read from the running SM8550 run; criterion 4 is promoting the patch replay into a tree tool in the build route, #1445; criterion 5 is `next` dropping `0006` when it takes upstream's recipe). #1443 is closed. `tools/build-preflight`'s guest check is anchored on `next` (`6957ae9029`); build worktrees cut from `ace312b0d2`/`0a3e979e50` still carry the unanchored one, so keep the emulator's name out of a launch command line.
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

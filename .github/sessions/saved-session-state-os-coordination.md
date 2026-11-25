# Saved session state for OS work coordination

## Start here

Saved 2026-11-25T06:27Z on `feature/conflict-resolution` in the pixelelated distribution repository. Resume this file for the **OS work coordinator**, the sole dispatcher for M7. Since November 24 that role runs in **Claude Code on the latest Opus** (`claude-opus-5-5`) in Herdr pane `w4:p2`; session `b19c3b8c-1c4f-4a57-8765-0b8fe1f11ae9` (D-WORKFLOW-200). The one-on-one steward runs Claude Code on the latest Fable in `w4:pF` (session `2032b6b6-3946-42d0-ab2c-cfb5469deeea`); worker lanes run Codex on `gpt-6.2-sol`. The daily operations worktree is `/workspace/repos/rocknix.worktrees/conflict-resolution`; the primary checkout `/workspace/repos/rocknix` carries local `next`. pixelelated builds an immutable Linux gaming OS. This worktree's rules lag `next`: read them with `git show next:<path>` (`AGENTS.md`, `.claude/rules/worktrees.md`, `.claude/rules/device-builds.md`, `.claude/skills/build-cleanup/SKILL.md`).

Read the [M7 milestone](https://github.com/pixelelated/distribution/milestone/7) (body updated 12:29Z), [#555](https://github.com/pixelelated/distribution/issues/555) (build qualification; 12:30Z comment), [#1441](https://github.com/pixelelated/distribution/issues/1441) (the H700 recipe failure) and [#1442](https://github.com/pixelelated/distribution/issues/1442) (the two-ABI admission refusal). Decisions made this session, all on local `next`: D-INFRA-035 to D-INFRA-043 and D-WORKFLOW-200. Also read [#1448](https://github.com/pixelelated/distribution/issues/1448) (the SM8550 fex-emu stop).

## Current focus

**000. Newest (2026-11-25T08:47Z; supersedes the #1450, #1451 and allowance lines of item 00).**
- **Still waiting on Max for the RG SP copy.** It was put to him at 06:27:52Z; he had not answered by the steward's 08:29Z note. Nothing has run on any device. On a relayed yes, the plan in item 00 stands.
- **The steward's 08:29Z note (D-WORKFLOW-195):** move what needs no device, no Max and no Codex allowance. The allowance read 88% used at 08:08Z (reset 2026-11-30T06:35:50Z), and another lane is still drawing on it, so this lane dispatched nobody and did the work itself:
  - **#1454 criterion 1 ticked** (comment `7157175665`). The cause:
    - the second review's 10 s window (`RECHECK_REVIEW`, `visible_quit.py:151`), against ordinary approvals of 5.9 to 14.2 s;
    - triggered by the menu clock's minute changing between preview and check;
    - made worse because `CLOCK_TEXT` knows only four renders from Nov 21, and the quit dialog masks nothing.
  - **#1454 criteria 2 to 4 wait.** That is the fix, two VM proofs (about 12 Codex points) and the tool into the tree. The tool's only copies are pB's `/workspace/tmp/pix-m7-pc-20261125-backup-0{1,2,3}/code/`. **Keep those folders** until criterion 4. Owner: pB, on the next affordable dispatch or after the reset. It must close before the next PC VM run or any RC call.
  - **#1451 criteria 2 and 4 ticked** (`cc89bb4453`, `acbfe010e8`). The escalation tool writes only to the inbox and refuses a pane config (35 tests; the old tool fails 24). The coordination rules (D-WORKFLOW-183/184/185/187/189/190/195) are on `next`. Five decided rows that had never been committed (D-WORKFLOW-191/192/193/195, D-LAUNCH-008) are appended. Record: `docs/qa-logs/2026-11-25-1451-rules-review/REVIEW.md`. Criterion 3, the agenda, stays held for the steward.
  - **#1450 criterion 4 reworded and held under D-WORKFLOW-203.** It is no longer blocked by #1451. A CI silence is "something broken", which goes to #1452's monitoring tool, and nothing is built before #1452's inputs.
  - **#1449 criterion 5** waits on #1445, the one-command build route: a multi-hour tool whose proof is a real build launch, and no build is planned before the device step and the code audit.
- **`/workspace/artifacts` pass: first batch prepared and refused (#493 `7157556001`).** It retires the 46 October candidate images (70,587,789,508 B, 19 store entries), keeping each entry's records plus a `RETIRED.json`.
  - Script: `conflict-resolution/docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/20261125-artifacts-candidates/retire-candidate-images.sh`, **sha256 `e076737b…`** (floor exactly 46). This is the batch Max's yes must name.
    - The revision refused at 08:50 was `4cd6b903…`; `4a7eab82…` was the floor fix.
    - `e076737b…` corrects its wording: the RG35XX SP runs H700 `43d0bc3bf4` of 2026-10-07 by the device action log. Its images left the store on 2026-10-12, entry `d89b067a…`, so none is in the batch.
    - #493 correction comment `7157700039`.
  - **#1455 filed:** rehearse the RC's upgrade from the RG35XX SP's October 7 build on the VM. Needs a PC image of `43d0bc3bf4`, the old state listed and seeded, and `release-candidates.md` step 3 naming the device's own build.
  - The harness review refused it at 08:50:20Z; nothing ran (`REFUSAL-artifacts-candidates.json`).
  - **NEEDS MAX** `steward-inbox/20261125T0851Z-old-test-builds.md`, marked for after the RG SP question. On the relayed yes, run the script once and report the measured recovery on #493.
  - Not in this batch: `pixelelated-release-sources` (32.4 GB: October M7 source archives and the `materialization05` git store, which borrows from the 13-04 keep item), `pixelelated-build-custody` (23.5 GB) and `m6-*` (M6's, not inspected). Inventory: `/workspace/tmp/rocknix-session/artifacts-pass-20261125/inventory.tsv`.
- **Checkbox reads against pB's 2026-11-25 originals: done (09:05Z).**
  - **#1433: criteria 4 and 5 ticked** (comment `7157831598`; 19 cited files check against manifest `92a3e316…`).
    - The changed save reached the server and the preseeded version survived with its mtime; 8 server objects, 7 local files and 4 protected configs are unchanged.
    - The one difference is the system config's `global.netplay.nickname` line, which the frontend writes at launch. Untick 4 if that is read as "configuration changed".
    - Criterion 1 (binding the original incident: `c9864eea`, `7581756f`, `27b5793a`; DETAIL_UNOBSERVED) stays open.
  - **#1427 and #1423: nothing tickable from the run;** notes `7157851519` and `7157852103` say what it covers.
    - #1427 needs an installed COPY TO FREE SLOT run on the candidate image, and the ES-pin check for criterion 1.
    - #1423 needs the Nova case on a per-action yes.
- **#1455: started (owner OS coordinator).** Cold GENERIC_X64 build of `43d0bc3bf4`, run `20261125T091159Z-3c44fe1c`, at 09:11:59Z.
  - Worktree `m7-pc-43d0bc3b-20261125`, owner `conflict-resolution/.build-runs/m7-pc-43d0bc3b-owner-20261125/`.
  - Matched to the RG35XX SP's build: image `988c0ba5`, `CUSTOM_VERSION=0.0.1`, options `2cf98cb3`, ES `72494bc72e`.
  - Processes: job pid 2339622, `make` 2339651, `watch-job` 2339623. A harness waiter (task `brnquief0`) reports on `launcher-result.json` or job exit; it dies with the session.
  - Consume it from `submit-01/launcher-result.json`, `tool-wrapper.rc`, the run's `build.rc`, the identity file and the image hashes. Then remove the build root and keep the img.gz and tar as named keep items until #1455 passes.
  - Meanwhile: #1455 criterion 3 (what the October 7 scripts wrote that the candidate reads differently).
- **The code audit (RC step 4) is blocked, not started.** Exact blockers:
  - step 3 is incomplete: #1455's rehearsal (above), RECORD.txt and the catalog;
  - step 0 fails on `0a3e979e50`: `bugs FAIL` with 300 open bugs without a disposition (the tool's cap), `packages CANNOT` (rclone 1.75.2 against 1.76.0), and `base: emulationstation CANNOT` (the pin is a tarball tag).
  - **Full step 0 (09:25Z): `CANNOT ANSWER`, rc 2** (#555 `7158351275`; `m7-pc-0a3e979e-owner-20261124/RC-PREFLIGHT-full-20261125.txt`).
    - bugs FAIL: 542 open (320 M6, 205 no milestone, 17 M7). No register rule settles whether M6's findings count at an M7 call: a scope question to prepare.
    - already-written FAIL: #366 and #1154 lack the line; 27 bugs closed since 09-26 lack a code trace.
    - ci FAIL: `0a3e979e50` is not on GitHub. Pushing it is publication, separately governed: a decision to prepare.
    - CANNOT: rclone 1.76.0, the ES pin (tarball tag), device facts (#270).
  - **Next in the OS lane:**
    1. Record-keeping. #366 and #1154 are done (09:29Z): both traces had the line, but formatted so the pattern missed it (mid-line, and in backticks). Fixed with no words changed, and noted on each issue.
       - **Selected next, owner OS:** code traces for the 27 M7 bugs closed as completed since 2026-09-26 with none. The full list is in `m7-pc-0a3e979e-owner-20261124/UNTRACED-bugs-20261125.txt`; the tool itself truncates at about 200 characters. Product bugs first: #526, #320, #578, #479, #584, #592, #564, #582, #599, #600, #602, #1117, #1114. Then the QA-tooling ones, whose `Already written` is "nothing on devices".
       - The tool also listed #47 (closed 2026-09-20); check why before tracing it.
    2. A plan for step 0, with a futro.
    3. The two decisions in plain terms, queued behind the RG SP question and the October images.
- **The largest unblocked M7 item is the owed code audit** (release-candidates step 4, D-WORKFLOW-062; `ceremony-check` keeps CI red for it and for the futro). It runs through the Facilitator on OpenRouter, not Codex. Plan it with the futro before starting.

**00. Newer (2026-11-25T06:27Z).**
- **The M7 build set is built and passes on one commit (D-INFRA-043).** `tools/rc-preflight --only build-set` PASS at 05:20:42Z: SM8550, GENERIC_X64 and H700 all `0a3e979e50`. Quoted on #555 (`issuecomment-7153693555`); #1449's "The M7 set passes" checkbox ticked.
  - **H700 accepted:** run `20261125T020406Z-f7a619db` (02:04:06Z to 05:18:02Z), all result channels 0, owners exited, DDR3 `b4ff5ad3…`, DDR4 `7ae4d351…`, tar `cb705521…`. Record `m7-h700-0a3e979e-owner-20261125/ACCEPTANCE.json` and `RC-PREFLIGHT-build-set.txt`.
  - H700 roots removed at 05:23Z (+147.10 GB, `REMOVAL-build-roots.json`). Kept: `m7-h700-0a3e979e-20261125/target/` and `kept/emulationstation-m7-20261110-0d852e5d1106/emulationstation` (`62b84880…`). Logs compacted to `.zst`, the PC console log included.
  - The `ee74f157` PC worktree is gone (+7.90 GB, 05:25Z); its records are in `conflict-resolution/.build-runs/m7-pc-ee74f157-records-20261124/`.
- **The PC image of `0a3e979e50` passes its VM checks** (pB, `RESULT.json` sha256 `06283f88…`, manifest of 2,018 members verified; #555 `issuecomment-7154478975`). Checks 1 (294/294), 2a (from `672a7c995f`), 2b (from `d7ca912480ea`, the WebDAV leg on its third case) and 3 (Smart mGBA) PASS.
  - The two upgrade-start images were released and removed at 06:06Z (+12.88 GB). `KEEP-named-items.json` now holds the 13-04 store and `root02` only.
  - Nine small November 5 receipts were lost to a `find -size -1M` filter: `released-upgrade-starts/nov5-672a7c995f/LOST-RECEIPTS.md`; the lesson is in `engineering-practices.md`.
  - Open checkboxes on #1423, #1427 and #1433 are to be read against pB's receipts before any tick.
- **H700 and SM8550 host readback: PASS** (#555 `issuecomment-7154797416`; `READBACK.json` in both owner folders). Both images carry 509 dead 32-bit systemd/udev copies, noted, not a gap.
- **Waiting on Max: the RG SP copy** (NEEDS MAX `steward-inbox/20261125T0626Z-rg-sp-first-copy.md`, also on #555). Max said at 06:13Z he will get a device ready when told which; that is not a yes.
  - On the steward's relayed yes: read the RG SP first (boot id, build, idle, the update queue, auto-sync, through the read filter).
  - Then copy the H700 tar (`cb705521…`) to a staging folder, verify the hash on the device, and move it into `/storage/.update`, all through `tools/device-act`.
  - Then put the restart as its own NEEDS MAX. The Nova follows.
- **#1454 (bug, M7):** the game-exit QA case's frame-review deadline. It must close before the next PC VM run and before any RC call.
- **The shared Codex weekly allowance is 85% used, reset 2026-11-30T06:35:50Z.** Every Codex lane on the account draws on it, another project's included. Overnight, 12 of 14 points went while only that project's lanes ran. Read it from `~/.codex/sessions/**/rollout-*.jsonl` (`rate_limits.primary.used_percent`).
  - Order: no other M7 Codex dispatch until pB reports. The H700/SM8550 qualification preparation runs in this lane.
  - The steward has the finding (sent into `w4:pF` at 05:33:43Z, before D-WORKFLOW-205 stopped pane delivery). Only Max can add allowance.
- **Never stage `docs/coordinator-one-on-one.md`** (the steward's agenda, with their uncommitted edits) on any branch until the steward says so. #1451 criterion 3 is held for that; criteria 2 and 4 are this lane's.
- **#1451 criterion 1 is committed locally as `4badc4e6c0`** (the five coordination tools, tests 31/21 OK). Push it with the next material batch, then tick it.
- **CI is back (#1446 closed).** Max re-enabled workflows at about 02:58Z. The first runs on `next` (`d5d8e07350`) were the wordlist check in 53 s, green (`45537101984`), and the record checks (`45537101977`), red only for the audit and futro owed. `tools/ci-silence-check` passes live.
  - #1441 is closed. #1450 waits only on criterion 4, the daily timer, which needs #1451.
  - Branches that have not merged `next` keep the old four-minute scan; the one-line fix is on #1446. The M6 lane is not messaged.
  - Owed: the code audit and the futro (`ceremony-check`). They keep `fork record checks` red by design.
- **The /tmp scratch removal is done (D-INFRA-046).** Max said yes at about 03:53Z. 267 entries were removed in two passes: the second for two read-only evidence folders, kept in `20261125-tmp-m7/kept-records/`. 4.85 GB of `/tmp` was freed. Outcome on #493.
- **Alerts (#1452, D-WORKFLOW-203/204): scoped, not built.** Build results go by email from the build account's Hostinger mailbox, sent by the finished build's watcher; breakage goes to SkyWalking or another open-source tool over OTLP; everything else waits for the watcher agent. It waits on a refreshed mailbox credential and a destination address from Max. The address goes in a private file only, never the tree, tracker or commits.
- **Push cadence:** each push of `next` is two workflow runs. Batch records into one push per material outcome, and mirror this checkpoint to the feature branch only at a handoff.
- **Nothing goes into the one-on-one pane `w4:pF` (D-WORKFLOW-205, #1453; Max, 05:34Z).** No `herdr agent prompt` to it, no messaging-tool message to the steward's session, and no escalation delivery aimed at it.
  - A notice for the steward is one file in `/workspace/tmp/rocknix-session/steward-inbox/` (mode 700), named `<UTC time>-<slug>.md`, with a first line of `NEEDS MAX`, `STOPPED WORK` or `INFORMATION`.
  - A `NEEDS MAX` or `STOPPED WORK` notice also goes on its issue: nothing wakes a closed steward session.
  - Max still answers only in the one-on-one, and the steward relays his words here (D-WORKFLOW-201). The earlier by-pane rule (#1447) is reversed.
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
2a. **The PC upgrade check on the PC image of the set's final head (D-INFRA-043; `0a3e979e50` unless a fix moves it) starts from `672a7c995f`** (November 5 PC image, the build on the RG SP and the Nova; the RG35XX SP still runs the October 7 build `43d0bc3bf4` by the device action log, #1455; `release-candidates.md` step 3), with `d7ca912480ea` as a second starting point (#555 comment).
3. `next` was pushed at 12:47Z (`9a51171c34..29bc9fd857`) and 12:51Z (`..6e30af8fac`); `ceremony-check --gate` prints no BLOCK line. The audit and futro ceremonies remain overdue (CI-red only). The retro is `docs/retros/2026-11-24-m7-cleanup-and-build-restart.md`.
4. **The lane observer is down** and its config pins the old Codex root session `01a0faa5-…`. The human-escalation config pins the old steward session `01a1e512-…`. Re-pin the observer before relying on it. The escalation tool must deliver to the steward's inbox or make no human delivery, never to `w4:pF` (D-WORKFLOW-205, #1451).
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

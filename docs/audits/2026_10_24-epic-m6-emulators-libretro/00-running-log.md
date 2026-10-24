# Epic Audit Running Log — M6.P2 T3, RetroArch and the libretro cores

**Auditor:** Code Auditor skill (v1.13.0, identical to `next`'s copy: `diff -q` against `git show next:.claude/skills/code-auditor/SKILL.md`, no output), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #650 (issuecomment-6378830351, 2026-10-24T02:36:34Z) and the session's own metadata
**Session:** herdr agent `m6-t3-emulators`, session `a6d65411-5a44-4596-9a6c-337855905c17`, pane `wN:p6`
**Started:** 2026-10-24 02:38 UTC
**Scope:** slice `emulators-libretro` (#650, `M6.P2 E798/T3`), area epic #798 (the emulators and cores), renovation epic #339, milestone M6. The membership is the inventory's `k: 3` rules (brief § 2): 344 paths recorded
**Spec:** `docs/reviews/briefs/emulators-libretro.md` version 2 (`f650d65522`; its § 7 is #650's checklist); `docs/reviews/plan-for-the-plan.md`
**Depth:** Extended (two reviewers from two other labs: GPT-6 Astra `--member gpt` at `max`, Gemini 4 Argon `--member gemini-argon` at `high`; refutation pass alone each)
**Branch / worktree:** `feature/m6-emulators-libretro-650` at `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; `reviewed-at` is the branch `HEAD` at stage A, recorded below

---

## Log Entries

### [Phase 0] 02:38 — The brief's first commands (`date -u` 02:38:14)

- `git fetch origin`, `git fetch upstream --no-tags`: both exit 0.
- Branch `feature/m6-emulators-libretro-650`, `HEAD` `af35d54f87270ceafc351a08b38bc28a7f2c78ed`; `git merge-base --is-ancestor 2174265e9c HEAD` exit 0, so the branch is stacked on the P1 tip.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md` lists four files (37+/2-): `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `.claude/skills/council/IMPORTED-FROM.md`. These are exactly the four the dispatch and the pointer name, so nothing is stale.
- `grep -c 'Renovation face' tools/lint-audit-artifacts` 4; `grep -c gemini-argon tools/lint-audit-artifacts` 4; `grep -c gemini-argon scripts/council-invoke.ts` 7 (the brief: 7 and 4).
- P1's `tools/renovation-{inventory,status,drift}`, `docs/reviews/inventory.json` and `slices.json` are present.
- `next` = `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`. **`upstream/next` = `3421d7d178`** (Q4's upstream, fetched now). `git merge-base next upstream/next` = `c445081a59518f37d9776e5412dd7b14910696f7`.
- `git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators`: exit 0, so **the slice's bytes are `next`'s at `8ebaf8daad`**.
- The brief and the futro (`docs/futros/2026-10-24-m6-emulators-and-cores.md`) are both in the tree. `core.hooksPath` lists `pre-push`.
- `git push -u origin feature/m6-emulators-libretro-650`: already up to date; tracking set.
- The host file `/tmp/m7-m6-host-coordination-20261023.txt`: its last two blocks are M7's `resource return` at 02:22:37 UTC and the coordinator's relay at 02:23. **No window is open.**
- `node` v24.21.0, `npm` 11.19.0; `tools/council/node_modules` is absent (the § 1 install comes before Phase 4.6).

### [Phase 0] 02:39 — Start confirmed; lane start committed

- Start comment on #650: issuecomment-6378851675.
- Work-log entry `T3 lane started` in `2026_10_24-work_log.md`, then `tools/work-log-index --write` (rc 0); commit `e1af3b2ba5`, pushed. The entry's heading was written as `02:45 UTC`, an estimate; `date -u` read 02:40:44 just after. It is corrected to `02:40` in the next commit, and every time from here is read from `date -u`.
- `tools/register-check`: 660 IDs, each once (rc 0).
- `tools/ceremony-check --gate` exits **1** on `weekly: 2026-W42 summary missing`. No branch carries a W42 summary (`origin/next`, the P0 and P1 branches: 0). The pre-push hook enforces the gate only on pushes of `next` (`.githooks/pre-push` 329, `refs/heads/next`), so the feature push went through without `--no-verify`. W42 (2026-10-12 to 18) predates this lane; it is noted on #650 as owed elsewhere, as T1 noted it on #648. The same report shows `box-check` red in CI (one failing checkbox across the tracker), which is not this lane's.

### [Phase 0] 02:42 — Reading (§ 3, the pre-flight)

- **Read whole:** the lane's pointer; `docs/reviews/plan-for-the-plan.md`; the brief (version 2, 1,191 lines); the futro `docs/futros/2026-10-24-m6-emulators-and-cores.md` with its erratum (the comment on #798 of 02:32 says the same as the file's § 1); the skill `SKILL.md`; `packages/README.md`; `packaging-and-patches.md`.
- **Issues read:** #650's body. Its fifteen criteria equal brief § 7, with two wording differences, both noted: criterion 9 asks `git apply --check` of the eight patches where the brief's § 4 says `patch -p1 --dry-run` (#650 wins, so both are run and `git apply --check` is the cell); criterion 12 lists four `proved:` classes where § 6 adds `fix-walk-pending-image`. Also read: the dispatch comment; #798's body and comments; #339's body (first 3.5 KB: the tiers and Tier 2's *"there is no longer anyone to send them to"*); #346's last three comments; the hand-back and stage-F comments on #648 (T1: `reviewed-at` `efadfea08a`, `fixed-at` `0f7558cff7`, tip `ba22eea867`, nine `fix-pending-image` rows) and on #649 (T2: 21 `fix-walk-pending-image` walks, ES tip `55158d2a6`, `time-to-play` 0.65 s and 1.01 s median at the pin).
- **Criterion 12's token, carried:** `grep -c 'proved:' 02-forward-audit.md` must equal `grep -c '^GUEST-PROOF:' 00-running-log.md`. So the string `proved:` appears in `02` only in guest-proof rows, and a running-log line begins with `GUEST-PROOF:` only to announce one. This entry names the token without starting a line with it.
- **Rules:** the every-session set was loaded this session from the worktree, which differs from `next` only in the four files above; `AGENTS.md` equals `next`'s and carries the same facts as `CLAUDE.md` (kept equal by `tools/rules-check`, D-WORKFLOW-045). Read in this session's context: `time-to-play.md`, `upgrade-and-install.md`, `engineering-practices.md`, `bugs-are-agent-first.md`, `vm-first.md`, `issue-tracking.md`, `decision-register.md`, `learning-capture.md`, `ceremonies.md`, `worktrees.md`, `fork-workflow.md`, `milestone-phase-naming.md`, `adversarial-council.md`, `working-principles.md`, `device-builds.md`, `release-candidates.md`, `instruction-files.md`, `handheld-evidence.md`, and the four ES rules (the interface's, not this slice's).
- **Blindspots read in full:** 38, 39, 47, 48, 50, 54, 55, 63, 65, 73, 74; the table rows of 1 to 28 by title. Carried into the read: 39 (no empty cell in a measuring table: the Q4 scan's assertion), 47 (the `FetchContent` grep), 48 (`git log -p` before judging any option), 50 and 55 (a log line is this run's only once tied to its launch), 54 and 63 (read `Using resolution` and `[GL] Renderer` before any RetroArch number), 65 and 74 (a fixture or a bind is part of the claim, and its hash is printed before the verdict).
- **Not yet read, opened when their phase needs them:** `generic-x64-vm-testing.md`'s sections (before the guest), `rclone-cloud-sync.md` § the save layout (Phase 3.5), `change-log.md` (stage E), the remaining phases of the skill (`phases.md`, `templates.md`, `review-levels.md`, `anti-patterns.md`, each before its phase), the decisions by ID (from the register as each is cited), the open issues of brief § 3 (Phase 1), and the prior audits' punch lists (counts only, after stage B's Phase 2).

### [Stage A] 02:41-02:49 — Scope re-derived; #799 filed and fixed

- **Counts** (brief § 2's filter, `python3 -I`, over `inventory.json` at `00ca350666`): 344 paths, 31,961 lines; 24 fork-own / 6,557 lines (1,038 of them GENERIC_X64 configuration); 299 upstream-carried; 21 vendor-carried / 1,670 lines, 8 fork-written / 1,244; 294 / 21 / 29 by area; 342 `shipped`, 2 `n/a`. **No delta.** `git ls-files` over the two directories gives 406 = 344 + 57 core patches (T42's) + 5 recipes (T24's). The patches' numstat sums to 1,670. All recorded in `01` § Scope.
- **Upstream:** `c445081a59..upstream/next` (`3421d7d178`) on the two directories is 14 commits, the brief's list exactly; 54 fork commits on the same paths since the base.
- **Branch scan:** 54 `origin` branches, 18 ahead, 44 differ (the brief's counts). **Correction:** `origin/feature/m7-player-setup` is ahead by `d9054efc46`, with `Install Steam.sh` blob-equal to `next`'s, and `6101242e14` is on no `origin` branch (only `legacy/m7-audit-integration-603`). It goes to #650 as a lead.
- **M7 delta:** `next..069fc2704421` touches one file, `Install Steam.sh` +605/-6, one commit `6101242e14`, eight hunks; tabled in `01`.
- **Image:** copied to `/workspace/artifacts/m6-t3-20261024/`, `sha256sum -c` OK; `.identity.json` `build_commit` `069fc270442134fe771258418adf4e666e0473fb`, `dirty` `no`. The guest's `/etc/os-release` is still to read. `df /workspace` 1.8 T free; `free -g` 45 G available, **swap 6 of 7 G used**; no QEMU and no `make docker-` running.
- **#336's body read; the line is drawn as the brief § 4 draws it** (`01` § Scope).
- **#799** (`Bug: retroarch-wrapper-test cannot run without a path ...`) filed at 02:45 before the fix. The fix is `d606301784`. Runs:
  - unfixed no-argument rc 2;
  - fixed no-argument PASS rc 0 (pin `bdba046fa6`, 12 byte-identical candidates, sha256 `b578746e…`);
  - explicit path PASS rc 0;
  - constructed pin failure rc 2;
  - 0015 reversed: 2011 calls of 2000, FAIL, rc 1.
- **Found alongside:** `--gated` is dead since `e5d14d4220` (parsed at line 57, never read; a `--gated` run printed the plain run's lines). Recorded for the punch list.
- **Another small delta:** the brief names `m7-signin-h700-build-20261023-05`; the host also has `-06`, and `-06` holds the live H700 aarch64 root.
- **`reviewed-at: d606301784`**: the slice's bytes there equal `8ebaf8daad` (`git diff --quiet`, exit 0).

### [Stage B, Phase 1-2] 02:53-03:17 — Phase 1; the mechanical checks that need no compiler; Q4 (b); F-01 to F-09

- **Phase 1** (`01` § Phase 1): 22 of 139 closed bugs match the brief's pattern. Upstream's trackers: 0011's #19518 merged to RetroArch master 2026-09-08; 0015's #19577 closed by its author as already fixed on master; #19223 (merged after the pin) is 0018's neighbour. Prior audits: eight folders name the slice; verdicts are sequestered.
- **`pkgcheck`:** 152 runs, 151 rc 0; `sameboy-lr` FAIL (F-02).
- **shellcheck v0.11.0** (digest checked): 30 files, 6 errors, of which 4 were lift artifacts and 2 are line-2 shebangs (F-04).
- **The image's table parsed:** 128 / 152 / **348 `<core>`** (the recorded 500 counted `<cores>` too).
- **The host regeneration** (`tools/regen-es-systems.sh`, the build's own host `xmlstarlet` copied from the M7 root): **byte-identical to the GENERIC_X64, H700 and SM8550 images**; RK3326 and RK3566 regenerated too. Constructed cases for the one-default rule: F-06.
- **Q4 (b):** `tools/q4-pins.py`, 03:06-03:11 UTC (rate 4,744 to 4,143), then two fixes run from its cache. First run rc 1 on two errored rows: the guard fired as designed; the cause was GitHub's "No common ancestor", which is `pin-not-on-project`. Final: 151 rows, `current` 39, `behind-project` 102, `behind-upstream` 1 (`np2kai-lr`), `pin-not-on-project` 6, 3 by hand (`q4-pins-byhand.md`: `libxmp-lite` and `emuscv-lr` behind-project, `idtech-lr` current), rc 0.
- **Q4 (a) in progress:** all 14 commits are absent from `next` (none reverse-applies; the merge base precedes them). `git merge-tree --write-tree next upstream/next` (read-only, tree `d2df30a92a`) gives five conflicts on the slice, the rotation-table recipes; F-09 is the `build.${DISTRO}-` trap.
- **Leads posted on #650:**
  - 6379089613: F-07 aethersx2-sa licensing and F-06 to T5.
  - 6379206910: **F-08**, the H700/SM8550 default PSX core absent from `/usr/lib/libretro`, time-sensitive while M7 tests H700.
- **The coordinator's answers** (#650 comment 6379108501, relayed into this session):
  - **F-07** is `to merge` in the class-1 shape: the deletion lands with the next base merge, the coordinator's act; no removal on this branch; raised with the maintainer on #346.
  - **F-06** is routed to T5 (#652) with this lane's evidence; this lane's side is the recipe comment and the two constructed cases.
  - Nothing owed.
- Commits `772e116dca`, `8dbe5762bc`, pushed.
- 03:19 The coordinator: **F-08/F-09 verified and filed as #802** (the maintainer and the M7 lane told; no device run asked). F-08's row references #802; the fix comes with the base merge as `c9820d0e89` adapted to `DISTRONAME`; nothing on this branch. `gh issue view 802` read back.
GUEST-PROOF: 03:27:01 UTC -- P1, the installed set on the guest (ssh 10034, BUILD_ID 069fc270442134fe771258418adf4e666e0473fb): cores, table, retroarch.cfg, modules, retroarch32; inline commands, output /workspace/artifacts/m6-t3-20261024/p1-installed-set.out
GUEST-PROOF: 03:27:22 UTC -- P2, tools/time-to-play --vm --no-configure-remote --only launch,exit,g2g --repeat 3 on the image's own scripts (Q5); output /workspace/artifacts/m6-t3-20261024/ttp-1/, log /workspace/artifacts/m6-t3-20261024/ttp-1.log
GUEST-PROOF: 03:33:10 UTC -- P3, patches 0018 and 0017 on two real launches through runemu.sh (Auto slot asked; control without), script /workspace/artifacts/m6-t3-20261024/p3-guest.sh, output /workspace/artifacts/m6-t3-20261024/p3-guest.out
GUEST-PROOF: 03:34:01 UTC -- P3b, patch 0018 re-run with the AUTO SAVE tile's arguments as separate words (P3's run A packed them into --controllers and did not engage: a fixture fault), script /workspace/artifacts/m6-t3-20261024/p3-guest.sh, output /workspace/artifacts/m6-t3-20261024/p3b-guest.out
GUEST-PROOF: 03:35:37 UTC -- P4, tools/time-to-play --vm --no-configure-remote --only launch,exit,g2g --repeat 3 with log_verbosity = "false" in the guest's /storage retroarch.cfg (Q5: the logging key's cost), output /workspace/artifacts/m6-t3-20261024/ttp-2/, log /workspace/artifacts/m6-t3-20261024/ttp-2.log
- 03:40 The guest stopped (`tools/vm-stop` rc 0 at 03:39:37; no QEMU left); this VM cycle's section was appended to `docs/vm-qa-log.md`.
- 03:41 **M7 host window from 03:47** (coordinator, #650 comment 6379424513): no guest, compiler or npm install until the return relay. Acknowledged on #650; the guest has been down since 03:39:37; reading and host sandbox work continue.
  - The ack's check `pgrep -f 'time-to-pla[y]|retroarch-wrapper-tes[t]|npm instal[l]'` counted 1. That was the command's own bash, whose heredoc held the words npm install (the self-match trap). Re-run alone, it lists nothing, so the claim on #650 stands.
- 03:55 Phase 2 closed in `02`: the coverage table (344 rows, `tools/coverage-table.py`), the fifteen criterion entries (4 PASS, 5 PARTIAL, 6 OPEN for later stages), the summary and the boundary. `tools/fork-package-freshness --list` names only aethersx2-sa under emulators/ (T30's).
- 03:55 The coordinator: **F-19 is #806** (the grep recipe layer is T22's, #669; the script layer `deferred:M7-merge` referencing #806); F-20 resolved by the M7 merge; F-21 to F-23 this lane's, `deferred:M7-merge`. #806 read back.
- 04:01 Phase 4.6 prepared without runtime: `second-opinions/review-plan.json` (extended, epic, refutation alone each), `gpt-brief.md` and `gemini-argon-brief.md` (one packet, 308,850 bytes, sha256 55ecef11…, given to both independently), and the two probe prompts. The calls wait for the M7 window's return line.
- 04:05 `05-punch-list.md` DRAFTED before Phase 4.6 from `tools/punch-items.py`: 29 items (4 High, 6 Medium, 19 Low). `tools/lint-audit-artifacts --phase pre-issue` is left with 1 contract failure, the expected missing reviewer provenance. Its first runs refused 8 deferrals that named no issue or no backticked commit; those were set Open until their targets exist, and the cited commits were backticked. No issue is filed before Phase 4.6.
- 04:12 Ten `bug` bodies drafted in `stage-d-bug-drafts/` for stage D: the five Low defects the coordinator asked for on #650 (PL-011 to PL-015) and the five other defects without an issue (PL-005, 006, 009, 010, 021, the brief's every-defect rule). Each has a code trace, an `Already written:` line, the VM line and agent-verifiable criteria. Checked against `tools/box-check`'s own PERSON, DEVICE and FACT patterns: 0 failures.
- 04:14 Every stage-C and stage-D step that needs no runtime is done (the bug drafts, the audit issue body, the friction lines). A background waiter, harness task bjv3uppwd, polls #650's comments every 60 s for the coordinator's return relay and the host file for a new M7 `resource return` block. It exits on either, or after 3 h with a TIMEOUT line, and its exit is what delivers the notification. Its blind spot: a relay worded without any of its patterns would not fire it, and only the 3 h timeout ends it then. On firing, the host file is read before any runtime starts.
- 04:33 **Stream 802** (the coordinator's fix packet, posted on #802) is done. `fix/m6-802-pcsx-rearmed32` at `a0defbd527` is the cherry-pick of `c9820d0e89` with `DISTRONAME`. `pkgcheck` rc 0, the `DISTRO` grep empty, `git apply --check` against `8ebaf8daad` clean; pushed; handed back on #802 (issuecomment-6379900683). One note: this shell's `grep` is a ugrep function that misread the stream's test pattern, so the counts used `/usr/bin/grep`. Waiter `bjv3uppwd` is still armed for the M7 return.
- 04:36 The coordinator reviewed stream 802 on #802, asked for no change, and marked the packet ready for M7. Still waiting on the M7 window.
- 05:27 The waiter fired at 05:26:51 on a false positive: M7's 05:26 block says it "retains host window for this immediate check, then explicit resource return", an announcement, not a return. No relay on #650. Re-armed on M7's actual return phrasing.
- 05:43 **M7 returned the host at 05:42:07.** The host-file block was seen at 05:43:05 by waiter `bpcovzq0w`. The coordinator's relay on #650 followed: "Resume Phase 4.6 now". The pointer was updated first (`443a174955`).
- 05:44 `npm install --prefix tools/council`: rc 0, tsx v4.23.15, node v24.21.0. `tools/council/run verify-pins`: "OK - verifier pins match current files and every re-pin is accountable." `tools/council/run test`: 39/39, 127/127 and 19/19 pass, 0 fail.
- 05:45 **Probes**, one per seat, each with `--provider openrouter` and its own `*-probe-prompt.md`. Both passed identity, effort and provider verification.
  - `gpt`: served `openai/gpt-6-astra` by OpenAI, effort max, 374 reasoning tokens, 9.6 s.
  - `gemini-argon`: served `google/gemini-4-argon` by Google, effort high, 216 reasoning tokens, 7.2 s.
  - Outputs: `gpt-probe.md`, `gemini-argon-probe.md`, and their provenance files.
- 05:46:20 **The refutation passes started**, both seats in parallel, each on its own copy of the one packet (sha256 `55ecef113c703cbf…` for both briefs). Outputs go to `gpt-audit.md` and `gemini-argon-audit.md`.
  - Harness task `bdlih7ayr` waits on both and delivers their end; the per-seat logs are in the session scratchpad.
  - Its blind spot: a seat that hangs is ended only by the Facilitator's own timeouts, 1 h per attempt and 4 h in total.
- 05:50 **The coordinator's rule for a failed seat**, from #650:
  - Hold. There is no stage D on one seat: this is extended depth, and adversarial-council.md fails closed.
  - Record the failure's provenance line, and diagnose it from the seat's log.
  - Retry once on the same slug, and only for a transient cause; then post and wait.
  - Escalation (gpt-6-astra-pro for the GPT seat) is the coordinator's to authorize. gemini-argon has no recorded escalation, so a non-transient failure there is a hold.
  - Never reduce the depth, and never grade from one seat.
- 05:58 **Both refutation passes succeeded on their first attempt.**
  - **`gemini-argon`:** ended 05:53:25 after 424.9 s. Served `google/gemini-4-argon` by Google; effort high verified by 30,337 reasoning tokens. 111,568 prompt tokens, 25,217 B of output.
  - **`gpt`:** ended 05:57:51 after 691.7 s. Served `openai/gpt-6-astra` by OpenAI; effort max verified by 30,359 reasoning tokens. 97,025 prompt tokens, 18,174 B of output.
  - Identity, effort and provider verification are PASS for both. Both outputs are committed beside their provenance files.
  - The grading starts now; every seat item is a lead until it has been re-read at its artifact.
- 06:10 **Phase 4.6 graded.** `04` § Second opinion has every seat item with its verdict and its artifact.
  - **Check A:** each image's `retroarch` cores against its `usr/lib/libretro`. GENERIC_X64 is missing 7, H700 3 and SM8550 3. The `.sh` system `idtech` is not a missing core, because `runemu.sh:488` runs `.sh` ROMs itself.
  - **New items:** PL-030 (GENERIC_X64's skipped-core choices and the id Tech scanner, Low); PL-031 (`ffmpeg` for mplayer on every image, Low); PL-032 (patch 0012's `system()` on achievement text, Medium, Security); PL-033 (the misspelt Wii rule, Low, Renovation).
  - **Re-grades:** F-05 rises to Medium for `st-v`. F-22 stays Low: its launch is `||`-guarded.
  - **Read now:** AC-09's rows 7 and 14. np2kai's state serializer changed mode only across its range.
  - **The record:** the coverage table is regenerated with F-12 scoped to `retroarch.cfg`, `pcsx_rearmed-lr`'s F-08 cell, and the 13 non-`-lr` recipes' reach. The wording the seats refuted is corrected in `02`, `04` and the issue body.
  - **Withdrawn:** Astra G-06, 0019's race, is benign: the move re-reads under the lock.
  - **Refuted:** Argon G-02, G-07 and G-09, and SC3014.
  - **Result:** 33 items (4 High, 8 Medium, 21 Low); `tools/lint-audit-artifacts --phase pre-issue` prints `PASS pre-issue artifacts`. Thirteen bug drafts have 0 box-check failures; the issue body's 33 checkboxes have 0. Stage D next.
- 06:12 **Stage D filed.**
  - **Bugs:** #813 to #825, 13 issues labelled `bug` with no milestone, the T1 shape, one per defect that had no issue: PL-005, 006, 009, 010, 011, 012, 013, 014, 015, 021, 030, 031 and 032. Each passes `tools/box-check --issue N` with 0 failures.
  - **The audit issue:** #826, `Audit: M6 T3 RetroArch and the libretro cores -- 33 findings (0 critical, 4 high)`, labelled `audit` and `punch-list`, milestone M6, attached under #650. It has 33 checkboxes, with 0 failures.
  - **The punch list:** `05` names #826 and each bug's number. The pre-issue lint passes.
  - **Next:** the punch list goes on #650, then the lane pauses for the coordinator's stream briefs.
- 06:22 **A correction.** The two entries above were first stamped 06:40 and 06:55, and `04` § Second opinion said "graded by 06:40". Those times were written without reading the clock. The true times are the commits' own: `347ec37894` at 06:10:58 and `2081fc1a37` at 06:12:38, with #826 created at 06:12:21. Corrected in place in this log, in `04` and in the pointer. The #650 posts carried no time, so nothing to correct there.
- 06:23 **S0, PL-032/#825: the achievements hook without a shell.** On `fix/m6-825-cheevos-hook-no-shell`, cut from `next` at `8ebaf8daad` in `../m6-825-cheevos-hook-no-shell`: one commit, `fac139dd43`, pushed. Merged `--no-ff` into this branch as `faac89ffc0`; the merge carries the 2 files only.
  - PROOF: test 1 (after the hook edit, which followed the 06:18:47 dry runs; no file records the exact minute) -- test 1, the counts. `system(cmdargs)` 1 -> 0; `execv` 0 -> 2; the hook's `$*` 2 -> 0; `"$@"` 0 -> 2.
  - PROOF: 06:18:47 UTC (the dry-run outputs' mtime) -- test 2, the patch at the pin. The pin is `bdba046fa6`; the brief's `generic-x64/build.ROCKNIX-...` root is gone, so the source came from the live `m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64`. Its `cheevos.c` (sha256 `372dad3e2ee1a413…`, carrying the old hunk) was copied to `.qa-scratch/t3/s0/` and the old hunk reversed with `patch -R`, which needed an offset of -18. The pristine file (`227f1269550b171c…`) takes the new hunk with `patch -p1 --dry-run -F0`: rc 0, no offset. The whole patch onto the pristine three files: rc 0; the configuration hunks keep their old offsets, unchanged.
  - PROOF: 06:20:04 UTC (`cc-new.out`'s mtime) -- test 3, the compiler. `make -n -C <root> -W cheevos/cheevos.c obj-unix/release/cheevos/cheevos.o` gave the exact command. Its paths were rebased from the root's earlier location (`m7-pixelelated`) and its ccache wrapper replaced by `gcc-15.2.0`, then run with `-fsyntax-only` on stdin from the root's directory (`.qa-scratch/t3/s0/cc-syntax.sh`). Results: the patched file rc 0 with 0 warnings; the as-built control rc 0; a constructed `hook_argv_typo` rc 1 (`'hook_argv_typo' undeclared`).
  - GUEST-PROOF: 06:21:36 UTC (`s0-guest.out`'s mtime) -- test 4, the hook's half. The T3 guest (`069fc2704421`, uptime 58 s) was booted with `generic-x64-vm run --headless --daemonize --pidfile /workspace/tmp/m6-t3-s0/qemu.pid ... --ssh-port 10034`, after a census showing no QEMU on the host. A tmpfs copy of `quirks/platforms/GENERIC_X64` was bound over it, holding a stub `bin/achievements`; `global.retroachievements.leds` was 1 for the run. Results:
    - old hook, argv as `execv` passes it: `argc=7 arg2=[a] arg3=[b]`, marker absent;
    - new hook: `argc=3 arg2=[a b $(touch /tmp/t3-s0-marker)] arg3=[c d]`, marker absent;
    - control, the old `system()` shell line: the marker PRESENT. #825 reproduced.
    - Unbound and the setting put back (unset). Script `.qa-scratch/t3/s0/s0-guest.sh`, output `.qa-scratch/t3/s0/s0-guest.out`. Synthetic input, named: the call stands in for RetroArch's.
  - 06:21:53 The guest stopped: `tools/vm-stop` rc 0, 0 QEMU left.
  - Test 5: RetroArch's half is fix-pending-image (#825 criterion 1, the first image with the patch).
  - `tools/pkgcheck retroarch` rc 0; `git status --short` empty after the commit. PL-032 is Deferred with `state: fix-pending-image` in the index.
- 06:23 Every time above is read from a clock or a file's mtime; the first draft of these lines had guessed three of them, corrected before commit.
- 06:30 **S1, the recipes** (PL-006, 017, 012, 015, 024, 005). Five commits on this branch: `e8bfe9ddda` retroarch, `28968ae585` sameboy-lr, `b45a4f1f7a` wildmidi, `8210c7a960` flycast2021-lr, `df69f527ad` melonds-ds-lr. `tools/pkgcheck` is 0 FAIL and 0 WARN on all five after; `git status --short` empty.
  - PROOF: PL-006, `.qa-scratch/t3/s1/pl006-fixture.sh`. The recipe's aarch64 block runs under set -e against constructed arm roots.
    - Before (`next`): zero, two and stale are all rc 0, copying nothing, nothing and the stale binary.
    - After: zero, two and stale each die with the reason (rc 1); one current root copies.
  - PROOF: PL-017, `.qa-scratch/t3/s1/pl017-fixture.sh`. A failing make in scripts/build:407-408's shape gives rc 2 before and after, the line after never reached. The control without set -e reaches it.
  - PROOF: PL-012. `pkgcheck sameboy-lr` FAIL 013 (late binding, PKG_BUILD) before, rc 0 after. `pkgcheck` catches it, so there is no lead for #657.
  - PROOF: PL-015. `gh api …/commits/405ca73` gives `405ca73adfa11659b7579f0b09df1303f42659a4`, and `git ls-remote` lists it. GitHub's archive of the full hash has the same sha256 as the cached short one (`4f4a7f7a…`), and the extracted trees are identical, which answers Astra's "WildMIDI archive equality".
  - PROOF: PL-024. The global section evaluated before and after gives the identical `PKG_MAKE_OPTS_TARGET`. pkgcheck WARN 032 is gone.
  - PROOF: PL-005, `.qa-scratch/t3/s1/pl005-resolve.txt`. Each of the eleven resolved (`gh api` for a hash, `git ls-remote …^{}` for a tag) equals the HEAD of the M7 build's own clone; tracy resolved too. `patches/001` applies at fuzz 0 to the pinned source.
  - All six go to Deferred with `state: fix-pending-image`. The coordinator's non-stream dispositions (PL-001 to 004, 007 to 010, 021 to 023, 025, 026, 029) are in the Phase 7 table, recorded through `tools/set-outcome.py`. Pre-issue lint PASS.
- 06:38 **S2, the launch table** (PL-011, 030, 031, 019): `87e328640d`. PL-006's way out, the coordinator's ask on #650: `de4faa8465`.
  - PROOF: `tools/s2-regen-check.sh`, before the change.
    - The five regenerated tables are byte-identical to the GENERIC_X64, H700 and SM8550 images.
    - **Delta found:** the first run, in this shell's en_US.UTF-8 locale, ordered `amigacd32` differently and matched no image. `mk_es_systems` orders the table with `ls | sort` (`functions:106`). Stage B had run under `env -i`, and the tool now does too.
    - Missing `retroarch` cores: GENERIC_X64 6, H700 2, SM8550 2.
  - PROOF: the same check, after.
    - Each table differs by exactly the intended lines. GENERIC_X64 loses 5 skipped-core offers, `ffmpeg` and `st-v`, and `psx` defaults to `duckstation-sa`. H700, RK3326 and RK3566 lose `ffmpeg` and `st-v`; SM8550 loses `ffmpeg`.
    - Missing cores: GENERIC_X64 0, H700 and SM8550 only `pcsx_rearmed32` (#802).
    - No system without an emulator or a default on any of the five.
    - The scanner: installed on 4 devices, not GENERIC_X64; `generate-idtech.sh` present on the H700 and SM8550 images.
  - PROOF: the per-game fallback read in the pinned ES (`FileData.cpp:1954-2025`). A stored `<game>.core` or `<game>.emulator` the system no longer lists is dropped, and the system's default launches.
  - `pkgcheck emulators`: 0 FAIL, one WARN of `next`'s existing class (unknown function).
  - The four items are Resolved, `state: fix-host-regen`.
- 06:39 **S3, the scripts** (PL-013): `5935e3ce8e`. PL-022 has no site outside `Install Steam.sh`.
  - PROOF: `head -1` of `Start Azahar.sh` and `Start MelonDS.sh` reads `#!/bin/bash`; `bash -n` rc 0 on both; shellcheck reports 0 SC1128.
  - Line 2 never bit: the tools system runs `/usr/bin/foot %ROM%`, whose `execvp` falls back to `/bin/sh`, which is bash on the image (`02`, F-04).
  - PL-013 is Deferred, `state: fix-pending-image`.

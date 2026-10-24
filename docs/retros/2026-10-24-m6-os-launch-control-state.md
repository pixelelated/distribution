# Mini Retro: M6 T1, the OS scripts: launch, control and state (#648)

**Completed:** 2026-10-24
**Tier:** epic, in Instruction-Recommendations mode (`docs/reviews/briefs/os-launch-control-state.md` § 6, stage G).
**Scope of this retro:** the audit and its fixes:
- the audit, stages A to D, with two cross-lab second opinions;
- the punch list #701: 84 items from 81 findings;
- 61 bug issues, #702 to #762;
- the seven fix streams of `docs/reviews/briefs/t1-streams.md` and two tails;
- stage F's verification.

**Branch:** `feature/m6-os-launch-control-state-648`: `reviewed-at` `efadfea08a` (stage A), `fixed-at` `0f7558cff7` (the last fix commit).
**Delta:**
- 195 commits against `next` (101 code or harness commits, the rest docs and merges);
- 51 files under `projects/` and `tools/`, +3,955 / -368 lines;
- harness cases `ai` to `cc` in `tools/last-good-scripts-test`;
- the punch list at 66 Resolved or Withdrawn and 18 Deferred, each Deferred row with its issue or commit;
- `tools/lint-audit-artifacts` (resolution) PASS, and `tools/box-check` 0 fail on #701 and #702-#762.

## What worked well

- **A failing case before every fix, under the image's tools.** Every fix commit names an unfixed run (rc 1, its failures confined to its stream's sections) and a passing run. Running the cases under the image's bash and busybox caught three things the host's tools would have hidden:
  - the netplay host `sed` that GNU refuses (S1);
  - busybox `awk` running END after exit (#760);
  - `tr`'s classes (the blindspot-34 shape, already guarded).
- **The passing run is an audit of the fix.** In S6 and S7 the first passing run failed on the stream's own mistakes:
  - S6: three faults (a lifter miss, a refactor that broke #308's case, #714's new contract against #198's fake);
  - S7: six failed checks, my two case faults and four older cases whose stand-ins lacked `set_settings_values`.

  None reached a commit, because the commits were cut from intermediates only after a green run.
- **The commit method.** A Python patch list per stream, applied group by group to intermediate trees and staged with `git hash-object` and `update-index`, gave one commit per item with its whole body. Two message mistakes (S4's truncated bodies, S5's "0 ms") were recommitted before any push.
- **Destructive scripts proven without a device or a disk.**
  - The ABL slots were files, and on the guest loop devices with one read-only.
  - The internal card was fixture `/proc` and `/sys` listings, and on the guest a loop partition mounted over `/storage` in a private mount namespace.
  - `parted`, `mount`, `smbpasswd`, `syncthing`, `systemctl`, `killall` and `usbgadget` were stubs.
  - Nothing touched the guest's own disk, and every batch's restore compared `same`.
- **The host-window protocol.** Four M7 windows came during the streams. Each was acknowledged with the guest's real state, read by pidfile and by process name, not inferred. The streams kept going on source, and the batches fitted between windows.
- **Asking the coordinator only what was theirs.** The overlay-versus-bezel precedence, #758's and #761's wording, and #720's are their calls. Each was put once, with the evidence, while the work went on.

## What was harder than expected

- **My own faults in the proof and harness code, about sixteen.** Each was caught before a push or a tick, and each cost a run:
  - **S1:** the cases ran under the host's GNU `sed`.
  - **S2:** a lift stopped at a heredoc's `}`; `rm -rf` of an overlay mount point, `/tmp/joypads`, on the guest, repaired 518 of 518.
  - **S3:** `awk -v` stripping a pattern's backslashes.
  - **S4:** a shell `read` truncating commit bodies.
  - **S5:** a harness copy run from the scratchpad, which finds its sibling tools beside itself (twice in the session); "0 ms" for 3 ms.
  - **S6:** `bF` running the untransformed `setrootpass`; the three passing-run faults.
  - **S7:** a stub `pactl` never reached, because `001-functions` puts `/usr/bin` first on `PATH`; `saved_state` not lifted.
  - **Stage F:** a `sed` that rewrote its own inserted path (#740's block skipped); a stub not made executable (#744); a batch that sourced the image's `001-functions`, not the tree's (#714); a lifter that excluded `name () {` (#755).

  The common shape: a fixture or a stub that silently does not engage, so the case tests something other than what it names. Each was found because the case's own output named the wrong thing.
- **`time-to-play` measured the image while I meant the tree.** It reboots the guest when it seeds its ROM or changes the two cloud settings, which drops bind mounts. Two runs measured the image's `runemu.sh` before a hash check after the run showed it. A temporary `/storage/.config/autostart/` hook made the binds survive the reboot.
- **The briefs and the facts.** The stream briefs were missing from the commit that announced them (`4cb05330c5`, recommitted in `289a95eb05`), and the branch still lacked them at 17:25, until `2219ca0e85` was merged. The briefs said the image's `/bin/sh` is dash; it is bash, which the lane reported. Three issue criteria were written in a shape the fix does not have: #720 (loop devices, removability), #761 (a parenthesis that contradicted its own shape) and #758 (before `set_settings_values`).
- **The VM has limits that are facts, not gaps.** GENERIC_X64 has no swap (no `/proc/swaps`, no `swapon`), no Wi-Fi device, no fan and no USB gadget. #748, #758 and #728 wait for those facts, and F-50's prepare could show only "no Done.".

## Discoveries that affect future work

- **`system.cfg` cannot carry a comment.** `chksysconfig`'s `valid()` refuses a non-blank line without `=`, so a comment would stop the shutdown backup (F-46, withdrawn). Any change that wants to annotate the seed needs another home.
- **EmulationStation reads `updates.enabled`, `updates.branch` and `updates.force`** (`GuiMenu.cpp:1527-1539`, `NetworkThread.cpp:87` at the pin). They are #694's interface state, not leftovers (the note is on #694).
- **`usbgadget stop` and `usbgadget disabled` both write `USB_MODE=disabled`**, so any caller that only means "for now" turns off the player's choice for good. The new `pause` keeps it (#752).
- **`001-functions` line 8 puts `/usr/bin` first on `PATH`**, so anything that sources the profile loses a caller's `PATH` prefix. Prefix again after sourcing, or use `/storage/.config/profile.d`, which the profile reads last.
- **GENERIC_X64 has no swap support at all**, while the H700 roots carry `swapon`; the memory manager's swap-file path is untestable on the VM.
- **Two lines left for other lanes:**
  - `userconfig-setup` makes #740's two copies at first boot. The coordinator has carried it to T22.
  - Upstream removed `rocknix-retroachievements-info` in `03204074ef`, so it leaves the fork with #563.
- **What the slice did to time to play.**
  - **The two numbers:** with the tree's `runemu.sh`, `setsettings.sh` and `001-functions`, interface to first frame was 0.73 s and game to game 1.01 s (n=1, `time-to-play --vm --quick`). Stage B measured 0.64 s and 1.01 s with the image's scripts, and stage A 0.76 s. That spread at n=1 covers the difference, so no stream is named as having moved a number.
  - **The one new wait on the launch path** is S3's #727: a launch waits, at most 5 s, for the previous game's exit restores. On the guest, a launch right after an exit whose restore took 3 s (a stub) rose 3,059 ms. With the real restores (milliseconds) it costs nothing; a slow GPU governor write is the case it is bounded for.

## Adjustments to remaining work (Instruction-Recommendations)

For the coordinator and the instruction owners. The lane has made the edits marked *done*.

1. **`tools/last-good-scripts-test`'s lifter takes a comment after the opening brace** (*done*, this retro's commit). The miss cost a run in S6 and in S7 (`saved_state() { # ...`), the rule of three counting the q3 batch's own lifter miss.
   - Positive: the old pattern lifts 0 of `saved_state`, the new pattern 1.
   - Recommended next step: make the lifter fail when a case calls a name it did not lift, rather than letting "command not found" read as a product failure.
2. **`generic-x64-vm-testing.md`, a line for `time-to-play`** (recommended): its reboot drops bind mounts. A run meant to measure tree scripts binds them from a `/storage/.config/autostart/` hook, and reads the installed script's hash after the run. Better still, a `tools/time-to-play --bind <src>:<dst>` flag (a procedure becomes a tool, `learning-capture.md` § 3).
3. **`tools/last-good-scripts-test` should refuse to run as a copy** (recommended): resolve its sibling tools from `ROOT`, or refuse when `HARNESS_ROOT` lacks `tools/vm-qa`. The friction line of 21:31 carries it.
4. **Proof scripts that rewrite paths should rewrite the longer prefix first, then hash or grep the result** (recommended for the proof template). Two of stage F's faults were a fixture that silently did not engage.
5. **Issue criteria for device-shaped facts** (recommended to the coordinator): #720's wording, if it is to tick on the VM; #728's, #748's and #758's observations, if they move to the open-items list (`bugs-are-agent-first.md`).
6. **The fix-pending-image rows**, nine of them (`05`'s Phase 7 gate, `02` § Stage F verification), are the coordinator's at the first image after the merge:
   - #723's and #750's boot journals;
   - #724's seed;
   - #739;
   - F-24's ten boots;
   - F-31, F-41, F-43b and F-51.
7. **The running change log** (`change-log.md`) is owed the day these streams land on `next`. The player-visible lines include:
   - a DPMS choice kept across updates (#721);
   - a restored suspend mode applied (#761);
   - a Wi-Fi network named `default` kept (#758);
   - `factoryreset audio` leaving other programs' state (#743);
   - the fuel-gauge refusal's sentence (#742).

## Scoped audit findings (Step 2.5)

- **AC conformance:** PASS. 66 of 84 punch items are resolved or withdrawn, each naming its commit and the check that passes. The 18 deferred each name an issue or a commit. On the bug issues, every criterion 2 is ticked from its harness runs, and every criterion 1 the guest could show is ticked with the guest's lines on the issue. The rest say why not.
- **Cornerstone spot-check** (the briefs' shared rules): PASS.
  - Test first with both runs named: every fix commit.
  - `Already written:`: every bug fix commit.
  - Commit shape: subjects under 72 characters, `Refs` never a closing keyword, the trailer.
  - The image's tools: `QA_SYSTEM_ROOT` throughout.
  - M7's `runemu.sh` hunks untouched: lines 1-10 and 331-340.
  - Never `--no-verify`, never a bare `git stash`.
- **Interaction-defect scan:** PARTIAL. Three files changed in more than one stream:
  - `001-functions` (S4, S5's correction, S7's `set_settings_values`);
  - `runemu.sh` (S1, S3, the tails);
  - `setsettings.sh` (S1, S2, the tails).

  Their combinations ran together only in the full harness at the tip and in q3's launches (spectator and relay session through S2's eval filter, PASS). The M7 candidate's `runemu.sh` prologue is not combined with the tails until the coordinator's merge.
- **Futro prediction verification:** 1 known miss. The epic's futro and the brief said the image's `/bin/sh` is dash (friction line, 07:14). The rest of its predictions were the briefs' to check, not this lane's.
- **Housekeeping (full-suite scan):** PASS. `tools/last-good-scripts-test` PASSED at the last code commit (23:43:59-23:52:47). The stage-B checks passed again at the tip (`02` § Stage F verification). `vocabulary-check`'s 15 failures against a local, unpinned ES checkout belong to that checkout, not to this slice; the pinned checkout reads 0.
- **Harness self-coverage:** PARTIAL. The lifter's miss is now fixed (adjustment 1). A case whose stub never engages still reads as a product failure or a pass; adjustments 1 and 4 cover two of its shapes.
- **Documentation freshness:** PARTIAL.
  - The facts above are in the work log, `02` and the issues.
  - Two rule lines are recommended (adjustments 2 and 3).
  - The change log is owed at the merge (adjustment 7).
- **UI review:** SKIP, no interface surface touched (a script's refusal sentence only, #742, in the outcome dialog's existing shape).
- **Build-vs-adopt:** SKIP, no build-vs-adopt answer recorded for the slice.

## Practice adjustments

- **The passing run as a gate is worth naming** in the stream-brief template: cut commits from intermediates only after a green run, so a fault the passing run finds never reaches history. It did that for S6's three faults and S7's.
- **A stub or a fixture is part of the claim.** The proof template should print, per case, that the stub was called (its call log) and that the bound file is the tree's (its hash), before the verdict. Four of stage F's faults would have shown in that line.

## Housekeeping items (not blocking the hand-back)

- **#720's criterion wording**, the coordinator's.
- **The rocknix.org documentation pass:** none needed. The player-visible changes are behaviour, with no new setting, row or flag.

---

The slice is code-complete. Hand-back next (brief § 10).

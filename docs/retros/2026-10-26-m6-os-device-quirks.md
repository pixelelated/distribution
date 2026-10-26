# Mini Retro: M6.P2 T29, the per-handheld quirks (#676)

**Completed:** 2026-10-26
**Scope of this retro:** the T29 lane at Independent depth. It covers:
- stages A to D: the read of the 333 paths under `quirks/devices/` at `8ebaf8daad`, with one GPT-6 Astra seat;
- the bugs #1120 and #1124, and the audit issue #1121;
- stage E's two streams;
- the close-out to the hand-back.

Not retro'd here: the coordinator's acceptance; the #585 and #332 posts (the coordinator's, from `05`); #1119, #1122 and #1123 (the coordinator's Backlogs under #695); #1125 (the rehearsal's seed, found by S2).

**Commits:**
- `reviewed-at`: `5ee0dfefcf` (the dispatch tip).
- `fixed-at`: `04a9fe98b9` (S2, the last fix; S1 is `39851da3e8`).

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** Neither fix is on the launch path or the exit path.
- **S1** changes the Nova's battery LED helper. `098-deviceutils` starts it at boot in the background (`nohup systemctl start batteryledstatus &`), and it polls every 15 s. The fix makes it exit at once when `led.color` is not `battery`, and repaint after a critical blink.
- **S2** changes a GENERIC_X64 boot quirk.
  - Before the stamp, it now hashes a listed file before removing it: at most 16 `sha256sum` reads, at boot.
  - A guest with an edited file at a listed name hashes it at every boot. That happens at boot, on a developer's tool (D-QA-053).

Nothing ran on a unit or on a guest.

## What the OS epic's close (#695) inherits

- **The selection table.** `02` § The selection lists the 26 boards the two shipped trees and patch `0154` name: 15 select a device entry, 11 none. **Both owned H700 units are among the none**, so only `platforms/H700/*` runs on them. A model rename upstream silently drops an entry, and this table is the check.
- **The two defect families in upstream's battery helpers**, each fixed in the fork's Nova copy (#1120):
  - the unquoted `led.color` test, in 12 files reaching 15 model names;
  - the stale bucket after a critical blink, in four tier-B files.

  They are #585 lines, and upstream's own Odin 2 helper is the model.
- **The leads filed under #695:** #1119 (H700's `030-analog_leds:7`), #1122 (`QUIRK_DEVICE` derived twice, and an empty model), #1123 (the wrappers' `$*`).
- **#1125:** the upgrade rehearsal's PL-019 seed must be the old quirks' real bytes before the next candidate's step 3. Otherwise the rehearsal fails against #1124's fix.
- **The every-boot shapes:** 106 flag rewriters, and nine boards' `050-game-configs` over a player's `retroarch.cfg` (#585).

## What worked well

- **The seat earned its place again.** It found two defects my first draft missed and refuted three of its claims.
  - **Found:** F-11, the critical blink's stale cache (G-15), and F-12, the VM take-back's first pass (G-11, G-12).
  - **Refuted:** the unit's start (G-6), the wrappers' "load-bearing" `$*` (G-2), and "no defect" in `091` (G-11).
  - All 40 items were re-read at their lines before grading (`stage-c/rereads/`).
- **Test first, with a fixture that can fail.** After G-9, `t29-battery-unset.py` gained `--expect`, and `t29-takeback.py` was built with it. Both streams record a FAIL before the fix and a PASS after, and the unfixed file is shown failing the `fixed` expectation.
- **Real bytes, not a substituted hash.** S2's known contents were rebuilt from the retired `099` heredocs in history and checked against `WRITTEN`, so case (b) is the old quirks' own file.
- **Grepping a stamp's readers before the commit.** That grep found `last-good-scripts-test`, which then ran whole and passed (1378 / 0), and `vm-upgrade-rehearsal`, whose seed would have failed the next candidate's step 3. That is #1125, found before the merge rather than at the rehearsal.

## What was harder than expected

- **The brief named a donor bash that does not exist.** M6's donor is busybox and rclone. S1 ran under the host's bash 5.3.9, and the output names it. The only other image bash is under an M7 extract and was not used.
- **My own slips, each caught before commit:**
  - a hash typed with a leading `0` in `05` (PL-10);
  - the ruling's time copied from its text (`05:5x`) into 22 places, when the tracker says 05:29:36;
  - a readback time typed as `06:0x`;
  - case (f)'s first link pointed outside its directory, so it tested a dangling link twice.
- **Counting by file instead of by name.** Model names reach further than files (15 names for 12 files), the seat's G-38.
- **The session was cut once by a rate limit** (stage B; the friction line on 2026-10-25).

## What we discovered

- **The battery unit is not enabled.** `030-led-control` sets a flag and `098-deviceutils` starts it. `WantedBy=` is installation metadata, not a start.
- **GENERIC_X64's take-back trusted names before its stamp.** Its comment stated that as the contract, and the upgrade rehearsal's seed encoded the same assumption. A fixture that seeds "something at the name" tests the defect as if it were the contract.
- **The addendum's three known unknowns:**
  - (1) nothing the owned H700 units need sits in a device entry they never reach (F-02);
  - (2) the device writes without a node test are conditional failure modes; none was shown absent on a unit (F-06);
  - (3) no directory carries both `050-game*configs` spellings. `git ls-tree -r --name-only 8ebaf8daad .../devices | grep -E '/050-game[-_]configs$' | sed 's|/050-game[-_]configs$||' | sort | uniq -d` prints nothing.

## Adjustments, Instruction-Recommendations mode

These are proposals for the coordinator.

1. **A stream that changes what a stamp or marker requires greps every reader of that stamp, and every fixture that seeds its inputs, before the commit.** This slice did, and found #1125. No rule says so. `upgrade-and-install.md` § A marker/sentinel file asks *"is there still a consumer?"* but not *"does a fixture seed it?"*.
2. **A stream brief that names a donor binary checks the donor's `RECORD.txt` first.** M6's carries busybox and rclone, not bash.
3. **A host fixture asserts** (`--expect`), as `04` § Codification gaps item 3 records. No new rule: `engineering-practices.md` § Guards must fail closed says it.

## Scoped audit (the close-out's own checks)

- **AC conformance:** #676's sixteen criteria, read against their artifacts in `04` § Acceptance-criteria scorecard; the hand-back items are this stage's. PASS.
- **Cornerstone spot-check:** nothing under `packages/`, `projects/` or `tools/` changed at stages A to D. Stage E changed the two fork-own files its brief names, and nothing else under those trees. Nothing ran on a unit. PASS.
- **Interaction-defect scan:** `03` § 3.5's seams. The wrappers' `$*` seam is corrected (G-2, #1123). S2's interaction with `vm-upgrade-rehearsal` was found by grep (#1125). PARTIAL: the rehearsal must change before the next candidate.
- **Futro verification** (`docs/futros/2026-10-23-m6-os-scripts-and-launch.md` § T29 kickoff addendum, `:384-424`):
  - *What we know* held: 333 / 88 / 65 / 23, the owned units without an entry, tier B's 70 / 2,885, 18 pending, two panel files.
  - The three unknowns are answered above.
  - *What could be missed* warned against counting the 263 as dead, filing the owned units as a bug, asking a unit, and taking `100644` as a defect. None of those happened. The addendum did not foresee defects in the fork-own five, two of which the seat found. PASS, with that gap noted.
- **Housekeeping:** no `package.mk` in the slice, so `pkgcheck` has nothing to read. `tools/last-good-scripts-test` passed whole over the fixed tree. PASS.
- **Harness self-coverage (check 7):** both fixtures cover the failure modes met while landing them. The unfixed files fail `fixed`; the RP6 path rewrite is a flag; case (f) was found wrong by its own first run. PASS.
- **Documentation freshness:** no new proper noun. The VM take-back's header comment was corrected with its code (S2). PASS.

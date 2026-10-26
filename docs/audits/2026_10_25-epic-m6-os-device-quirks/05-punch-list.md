# Punch list — M6.P2 T29, the per-handheld quirks (#676)

**Independent depth** (one seat, GPT-6 Astra at `max`; `04` § Second opinion). The audit issue is #1121 (a sub-issue of #676).
- **Fourteen items:** 5 Low, 9 Info.
- **One `bug` filed, #1120**, for PL-01 (the coordinator's ruling). PL-02 is filed in it as its own section, and the coordinator may split it out. PL-03 is a candidate. Both are the coordinator's at the stage-D pause.
- **Nothing** in this list changes a file under `packages/`, `projects/` or `tools/` at stages A to D, and no item proposes a removal of an upstream-carried unit (D-WORKFLOW-209).
- **Nothing ran on a unit, and no guest ran.**

---

## PL-01: with `led.color` never set, the Nova's battery helper drives all eight stick LEDs at boot (the `bug`)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-01
- **Owner area:** projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status (fork-own, `a3d617ff54`; the line is upstream's `32a1d8570d`)
- **What:**
  - **The start.** `platforms/SM8550/030-led-control:7` sets `DEVICE_BATTERY_LED_STATUS="true"`, and `098-deviceutils:31-34` starts `batteryledstatus`, which execs this helper.
  - **The defect.** `:73` `if [ ! ${BAT_LED_STATE} == "battery" ]; then break`. With `led.color` unset, which nothing seeds, bash reads `[ ! == "battery" ]` as false and the loop runs battery mode.
  - **The model:** `AYN Odin 2/bin/battery_led_status:63` quotes it.
  - D-UI-121's *"the default comes on"* (#332).
- **Evidence:** P8, P15, P16
- **Can this be done on the VM?** Yes, on the host: `tools/t29-battery-unset.py --expect unfixed` meets its expectation on the file at `8ebaf8daad`, and a fixed file must pass `--expect fixed`. What the LEDs look like is device fact line 31.
- **Already written:** nothing persisted. The helper reads `led.color` and writes only sysfs, never `set_setting`, so a Nova that booted with it unset has nothing of the helper's on `/storage` to migrate.
- **Acceptance:** the bug's fixture case (`unset` unlit, `rgb` unlit, `battery` lit) passes on the fixed file and fails on the unfixed one
- **Bug issue:** #1120
- **Fix commit:** `39851da3e8` (S1; the positive before in `stage-e/s1-before.txt`; `02` § The streams)
- **Disposition note:** open

## PL-02: after a critical-battery blink, the Nova's LEDs stay off when the charge returns to the earlier bucket

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-11
- **Owner area:** the same file as PL-01
- **What:**
  - **The defect.** `:85-94` blinks five times, ends off, and `continue`s with `PREV_BATCAP` unchanged, so `:98` skips the repaint on a return to `D_RED` (15 % → 10 % → 15 %).
  - **The model:** the Odin 2 helper sets `PREV_CAP="critical"` before its blink (`:62`).
  - **Siblings, recorded, not fixture-run:**
    - an empty capacity read reaches `D_GREEN`, and a missing status reads as charging (the seat's G-16);
    - a mode change during the blink can be overwritten (G-17).
- **Evidence:** P15, P16
- **Can this be done on the VM?** Yes, on the host: the fixture's `critical-recovery` case reads `lit=no` unfixed and must read `lit=yes` fixed
- **Already written:** nothing persisted (sysfs only)
- **Acceptance:** the coordinator's disposition: the same `bug` as PL-01 with the `critical-recovery` case, or a bug of its own
- **Bug issue:** #1120 (its own section and criterion)
- **Fix commit:** `39851da3e8` (S1, with PL-01; `02` § The streams)
- **Disposition note:** stays in #1120 as its own section and criterion: one file, one fixture, one stream ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC). Fixed by S1 with PL-01.

## PL-03: the VM's take-back removes a listed file by name before its stamp exists (a candidate)

- **Severity:** Low
- **Category:** Correctness (candidate)
- **Question:** Q3
- **Source Finding:** F-12
- **Owner area:** projects/ROCKNIX/packages/hardware/quirks/devices/QEMU Standard PC (Q35 + ICH9, 2009)/091-retired-vm-fixes (fork-own)
- **What:**
  - **The first pass** (`:61-75`) removes a file at any of the 17 listed names, whatever it holds. The sha256 and non-symlink checks apply only after the stamp.
  - **A dangling symlink** at a listed name fails `-e`, so the stamp is written with it still there.
  - **The reach:** VM-specific paths, a developer's tool (D-QA-053), a one-boot window.
- **Evidence:** P7, P15, P16
- **Can this be done on the VM?** Yes, on the host: a fixture of the script over a scratch root covering unstamped user content, both known hashes, stamped unknown content, a dangling link and a missing stamp (the seat's G-12)
- **Already written:** a guest that booted this build once holds its `STAMP`, and its first-pass removals are done. Nothing to migrate.
- **Acceptance:** the coordinator's disposition: a `bug` with that fixture (unfixed removes edited content, fixed keeps it), or recorded
- **Bug issue:** #1124
- **Fix commit:** `04a9fe98b9` (S2; the positive before in `stage-e/s2-before.txt`; `02` § The streams)
- **Disposition note:** a `bug`, not a record ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC): #1124, filed by the lane, Low; fixed by S2. #1125 is the rehearsal fixture S2 found seeding bytes no old quirk wrote.

## PL-04: upstream's copies of the two battery defects

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q3
- **Source Finding:** F-01, F-11
- **Owner area:** upstream-carried `bin/battery_led_status` copies; `platforms/SM6115`, `SM8250` (T22's)
- **What:**
  - **The unquoted test:** 12 upstream files, which reach 15 model names with the Nova's (`stage-c/rereads/c08`), 11 of them tier B.
  - **The stale cache after a critical blink:** ACE, EVO, Odin 2 Portal and Thor (the seat's G-24).
  - **The model** for both is `AYN Odin 2/bin/battery_led_status`.
- **Evidence:** P8, P15, P16
- **Can this be done on the VM?** Yes, on the host: the fixture with `--redirect-paths` (met on RP6's copy)
- **Already written:** nothing proposed
- **Acceptance:** per-unit dispositions (D-WORKFLOW-209), with a #585 line naming the Odin 2 helper as the fix
- **Disposition note:** per-unit dispositions (D-WORKFLOW-209; removals none) ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC). The #585 line, for the coordinator to post at acceptance:

  > **ROCKNIX quirks, `bin/battery_led_status` (#676 PL-04).** Two defects in upstream's battery LED helpers, both fixed in the fork's Nova copy (#1120).
  > - **The unquoted test:** `[ ! ${BAT_LED_STATE} == "battery" ]` runs battery mode when `led.color` is unset. It is in 12 device copies, reaching 15 model names: ACE (DMG by symlink), DS, EVO, S 2K (S Mini), S2 (KONKR Pocket FIT), Odin 2 Portal, Odin 3, Thor, MANGMI Pocket Max, RP6 (TOP-DPAD). It is also in `platforms/SM6115` and `SM8250`.
  > - **The stale cache:** a critical blink ends off without resetting the cached bucket, so a return to the earlier bucket stays dark. It is in ACE, EVO, Odin 2 Portal and Thor.
  > - **The model is upstream's own** `AYN Odin 2/bin/battery_led_status:62-63`: the quoted test, and `PREV_CAP="critical"` before the blink.
  > - **Proof:** `t29-battery-unset.py --redirect-paths --expect unfixed|fixed`, a host fixture. **Target:** ROCKNIX/distribution. **Status:** prepared, not submitted (D-WORKFLOW-165).

## PL-05: nine boards' `050-game-configs` revert a player's RetroArch audio driver and microphone at every boot

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-03
- **Owner area:** upstream-carried `050-game-configs` (four tier-B directories, five model names)
- **What:**
  - `sed -i` over existing matching lines of `retroarch.cfg`, at every boot.
  - `009-commander-cfg` is an ownership contrast, not a drop-in fix (the seat's G-18).
  - A value already reverted cannot be given back, and the file is in the settings backup (`backuptool:288`).
- **Evidence:** P10, P15
- **Can this be done on the VM?** Yes, on the host: the two `sed` lines over a fixture `retroarch.cfg`
- **Already written:** players' earlier choices were reverted at each boot; nothing can restore them
- **Acceptance:** per-unit dispositions and a #585 line: defaults at creation, not at every boot
- **Disposition note:** per-unit dispositions ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC). The #585 line, for the coordinator to post at acceptance:

  > **ROCKNIX quirks, `050-game-configs` (#676 PL-05).** Nine boards' quirk runs `sed -i` over `retroarch.cfg`'s `audio_driver` and `microphone_enable` at every boot, reverting a player's choice: Pocket S2, Pocket S 2K (and S Mini), Odin 2, Odin 2 Portal, Odin 3, Thor, Thor Lite, Retroid Pocket 5, Retroid Pocket Mini.
  > - The fix is a default applied when the file is created, not a rewrite at every boot. `AYN Odin 2/009-commander-cfg`'s *"only if absent"* is the ownership contrast, not a drop-in: a guard on existence would skip every existing file.
  > - A value already reverted cannot be given back.
  > - **Target:** ROCKNIX/distribution. **Status:** prepared, not submitted (D-WORKFLOW-165).

## PL-06: the stick helpers on four tier-B boards keep #332's unset-preset shape; achievements' restore

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-04
- **Owner area:** upstream-carried `bin/ledcontrol` (EVO; the Portal blob: Odin 2 Portal, Thor, RP6, RP6 TOP-DPAD) and `bin/achievements`
- **What:**
  - `rgb` with `analogsticks.led` unset calls the helper with no arguments. It writes nothing, and `led.color=rgb` is saved anyway (G-19).
  - `achievements` runs only with `global.retroachievements.leds` on, and restores a valid preset. With none set the rainbow's last colour stays. On the H700 and ACE-derived boards `led.color` is the power LED (G-20).
  - The Nova's `:53-57` is the fork's fix.
- **Evidence:** P10, P15, P16
- **Can this be done on the VM?** Yes, on the host, by the fixture's shape; what the LEDs show is device fact line 31
- **Already written:** `led.color=rgb` saved over a failed application
- **Acceptance:** per-unit dispositions and a #585 line, #332 named
- **Disposition note:** per-unit dispositions ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC). The #585 line, and the #332 comment, for the coordinator to post at acceptance.

  #585:

  > **ROCKNIX quirks, the stick LED `rgb` default (#676 PL-06).** `AYANEO Pocket EVO/bin/ledcontrol:100-101` and the shared `AYN Odin 2 Portal/bin/ledcontrol:26-27` (Odin 2 Portal, Thor, RP6, RP6 TOP-DPAD) pass an unset `analogsticks.led` to `analog_sticks_ledcontrol`.
  > - The helper rejects the call and writes nothing, and `ledcontrol` saves `led.color=rgb` anyway.
  > - The model is the fork's Nova copy (`Retroid Pocket Nova/bin/ledcontrol:53-57`), which applies a white default at the saved brightness.
  > - **Target:** ROCKNIX/distribution. **Status:** prepared, not submitted (D-WORKFLOW-165).

  #332:

  > T29 (#676 F-04, PL-06) read the stick LED helpers on four tier-B boards against D-UI-121. On EVO, Odin 2 Portal, Thor and RP6, choosing RGB with no saved preset writes nothing and still saves `led.color=rgb`. So the sticks keep whatever they showed: not *"turned off"*, but not the colour the row says. The Nova's copy applies a default, and that fix is the fork's.
  > `bin/achievements` (Odin 2, DMG, EVO, CubeXX, RG40XX H and V) runs only with `global.retroachievements.leds` on. It restores a valid saved preset; with none set, the rainbow's last colour stays. On the H700 and ACE-derived boards `led.color` is the power LED, not the sticks. What the LEDs show on a unit stays device fact line 31.

## PL-07: `led.brightness` means words on the Nova and a percentage on the Thor

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-05
- **Owner area:** the Nova's `bin/ledcontrol` (fork-own) and Thor's `bin/battery_led_status` (upstream's); the interface outside the tree
- **What:**
  - The two dialects (`max|mid|min` against percent).
  - On the Nova a preset's first field overrides `led.brightness` at the next `rgb` (G-14).
  - Thor applies a brightness change only on the next repaint (G-22).
- **Evidence:** P10, P15
- **Can this be done on the VM?** Yes for the scripts, on the host; which value the interface writes is the interface's (#332)
- **Already written:** nothing proposed
- **Acceptance:** recorded on #332 (D-UI-121) with G-14 and G-22
- **Disposition note:** the #332 comment, for the coordinator to post at acceptance ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC):

  > T29 (#676 F-05, PL-07), two more for D-UI-121's *"the brightness row does nothing on that device"*:
  > - **The Nova:** once `analogsticks.led` holds a preset, `ledcontrol rgb` uses the preset's first field and never reads `led.brightness` (`Retroid Pocket Nova/bin/ledcontrol:53-58`). A `brightness min` is therefore undone by the next `rgb`, such as `powerstate.sh:16`'s at boot. The two settings can disagree.
  > - **The Thor** reads `led.brightness` as a percentage, and the Nova as `max|mid|min`. Thor's `led_bri` runs only when a colour is painted (`AYN Thor/bin/battery_led_status:16-22,48-56`), so a brightness change waits for the next battery-bucket change.
  > Which value the interface writes on each board is the interface's, outside the distribution tree.

## PL-08: device writes without a test for the node

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-06
- **Owner area:** upstream-carried tier-B files (`020-set-xbox-gamepad`, the DMG helper, RG40XX V's `/dev/ttyS2`)
- **What:** a redirect to an absent `/dev` node creates a regular file as root; one guard in the tree (the x55's `040-hdmi`). A conditional failure mode only.
- **Evidence:** P10, P11, P15
- **Can this be done on the VM?** Yes, on the host: the redirect over a scratch root
- **Already written:** nothing proposed
- **Acceptance:** recorded; a #585 line if the coordinator wants one
- **Disposition note:** recorded as it stands ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC).

## PL-09: naming a reader meets

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-07
- **Owner area:** upstream-carried
- **What:** Thor's `touchcontrol` is a file the loop runs; the two `050-game*configs` spellings; copied battery header comments at `:6-7`; RG40XX V parses a right-side colour it never sends.
- **Evidence:** P11, P15, P16
- **Can this be done on the VM?** No: a read; the host shows it
- **Already written:** nothing proposed
- **Acceptance:** recorded in `02` F-07
- **Disposition note:** recorded as it stands ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC).

## PL-10: 18 upstream commits pending over 31 paths; panel calibration for the Thor and the RP6

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-08
- **Owner area:** upstream's, via the next base merge
- **What:** 16 A, 3 D, 12 M. `56e5c48b74` (Thor) and `abfdcfb57f` (RP6, and TOP-DPAD by alias) add `040-panel_calibration`. No collision with the Nova's fork-own rows.
- **Evidence:** P12, P15
- **Can this be done on the VM?** No: a history read; the calibration is a device fact
- **Already written:** nothing proposed
- **Acceptance:** *settled by the next base merge*; not a correctness proof of the calibration
- **Disposition note:** recorded as it stands; *settled by the next base merge*, the merge's ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC).

## PL-11: two derivations of `QUIRK_DEVICE`, and an empty `model` that falls to nothing

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-09
- **Owner area:** `002-autostart:6-12` and `rocknix-info:6-12` (T22's and T1's lanes)
- **What:** `strings` against `tr -d '\0'`, both with `/` → `-` and an unquoted `echo`. An existing but empty `model` file does not fall back to DMI, so nothing is selected (G-39).
- **Evidence:** P13, P15
- **Can this be done on the VM?** Yes, on the host: both derivations over a fixture `model`
- **Already written:** nothing proposed
- **Acceptance:** a lead recorded for the derivations' owners, #1122
- **Disposition note:** recorded; the lead is **#1122**, filed under #695 by the coordinator in the lane's words ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC).

## PL-12: the owned H700 units select no device entry

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-02
- **Owner area:** `platforms/H700/*` (T22's)
- **What:** the RG35XX SP and the RG-SP run only `platforms/H700/*`. No missing need was identified in a device entry. `030-analog_leds:7`'s unquoted test is the coordinator's lead, #1119.
- **Evidence:** P5, P9, P15
- **Can this be done on the VM?** No: a selection read; the host shows it
- **Already written:** nothing proposed
- **Acceptance:** recorded in `02` § The selection; the lead is #1119
- **Disposition note:** recorded; the `030-analog_leds:7` lead is **#1119**, filed under #695 by the coordinator ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC).

## PL-13: the wrappers forward `$*` unquoted where `"$@"` would keep the arguments

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** F-04
- **Owner area:** `system-utils/sources/scripts/ledcontrol:14-17` and its siblings (T22's)
- **What:** the caller already splits `${LEDS_CONFIG}`, so `"$@"` passes the same seven arguments without a second split or glob expansion (G-2). Of 22 callers, one quotes (`c01`).
- **Evidence:** P15, P16
- **Can this be done on the VM?** Yes, on the host: the wrapper over a stub helper
- **Already written:** nothing proposed
- **Acceptance:** a lead recorded for the wrapper's owner, #1123
- **Disposition note:** recorded; the lead is **#1123**, filed under #695 by the coordinator in the lane's words ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC).

## PL-14: the design, and the 263 paths carried by placement

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-10
- **Owner area:** the whole membership
- **What:** flag files rewritten at every boot, dispatch by directory name, 23 alias symlinks. 6 + 64 + 263 = 333 by tier. **Removals none** (D-WORKFLOW-185, -209).
- **Evidence:** P6, P11, P15
- **Can this be done on the VM?** No: a design read
- **Already written:** nothing proposed
- **Acceptance:** recorded in `04` Q1 and Q6
- **Disposition note:** recorded as it stands ([#676 ruling](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC).

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-01"
  outcome: "resolved (39851da3e8)"
- id: PL-02
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-11"
  outcome: "resolved (39851da3e8)"
- id: PL-03
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-12"
  outcome: "resolved (04a9fe98b9)"
- id: PL-04
  severity: Info
  category: Renovation
  question: Q3
  source_finding: "F-01, F-11"
  outcome: "deferred:#585"
- id: PL-05
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "F-03"
  outcome: "deferred:#585"
- id: PL-06
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "F-04"
  outcome: "deferred:#585"
- id: PL-07
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-05"
  outcome: "deferred:#332"
- id: PL-08
  severity: Info
  category: Renovation
  question: Q2
  source_finding: "F-06"
  outcome: "resolved"
- id: PL-09
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-07"
  outcome: "resolved"
- id: PL-10
  severity: Info
  category: Renovation
  question: Q4
  source_finding: "F-08"
  outcome: "resolved"
- id: PL-11
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-09"
  outcome: "deferred:#1122"
- id: PL-12
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-02"
  outcome: "deferred:#1119"
- id: PL-13
  severity: Info
  category: Renovation
  question: Q2
  source_finding: "F-04"
  outcome: "deferred:#1123"
- id: PL-14
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-10"
  outcome: "resolved"
```

## Phase 7 resolution gate

The coordinator's stage-D dispositions (#676, [issuecomment-6408955761](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761), 05:29:36 UTC), each read back from the tracker at stage F (05:46 UTC: #1119 to #1125 open, #585 open, #332 closed).

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Resolved** | `39851da3e8`, S1 under `t29-streams.md` (before `stage-e/s1-before.txt`, after `stage-e/s1-after.txt`); bug #1120, its criteria ticked, open until on `next` |
| PL-02 | **Resolved** | `39851da3e8`, S1 with PL-01 (the `critical-recovery` case); in #1120 by the ruling [issuecomment-6408955761](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761) |
| PL-03 | **Resolved** | `04a9fe98b9`, S2 (before `stage-e/s2-before.txt`, after `stage-e/s2-after.txt`, the suite `stage-e/s2-suite.txt`); bug #1124, its criteria ticked; #1125 the rehearsal's seed |
| PL-04 | **Deferred** | deferred:#585, the line in § PL-04, for the coordinator's post at acceptance; per-unit dispositions [issuecomment-6408955761](https://github.com/pixelelated/distribution/issues/676#issuecomment-6408955761) |
| PL-05 | **Deferred** | deferred:#585, the line in § PL-05, for the coordinator's post at acceptance |
| PL-06 | **Deferred** | deferred:#585, the line and the #332 comment in § PL-06, for the coordinator's post at acceptance (#332 reads CLOSED at stage F) |
| PL-07 | **Deferred** | deferred:#332, the comment in § PL-07, for the coordinator's post at acceptance (#332 reads CLOSED at stage F) |
| PL-08 | **Resolved** | recorded at `dcb2bf63c1`: `02` F-06 |
| PL-09 | **Resolved** | recorded at `dcb2bf63c1`: `02` F-07 |
| PL-10 | **Resolved** | recorded at `dcb2bf63c1`: `02` § The upstream delta, regenerated, `check` 0; settled by the next base merge |
| PL-11 | **Deferred** | deferred:#1122, the coordinator's Backlog under #695 |
| PL-12 | **Deferred** | deferred:#1119, the coordinator's Backlog under #695; `02` § The selection lists both owned H700 units NONE |
| PL-13 | **Deferred** | deferred:#1123, the coordinator's Backlog under #695 |
| PL-14 | **Resolved** | recorded at `dcb2bf63c1`: `tools/t29-tables.py check` 0; removals none |

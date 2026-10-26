# Punch list — M6.P2 T29, the per-handheld quirks (#676)

**Independent depth** (one seat, GPT-6 Astra at `max`; `04` § Second opinion). The audit issue is opened at stage D, a sub-issue of #676.
- **Fourteen items:** 5 Low, 9 Info.
- **One `bug` to file at stage D**, PL-01 (the coordinator's ruling). PL-02 is proposed for the same bug, and PL-03 is a candidate. Both are the coordinator's at the stage-D pause.
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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Disposition note:** open

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
- **Acceptance:** a lead recorded for the derivations' owners
- **Disposition note:** open

## PL-12: the owned H700 units select no device entry

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-02
- **Owner area:** `platforms/H700/*` (T22's)
- **What:** the RG35XX SP and the RG-SP run only `platforms/H700/*`. No missing need was identified in a device entry. `030-analog_leds:7`'s unquoted test is the coordinator's lead under #695.
- **Evidence:** P5, P9, P15
- **Can this be done on the VM?** No: a selection read; the host shows it
- **Already written:** nothing proposed
- **Acceptance:** recorded in `02` § The selection; the lead is #695's
- **Disposition note:** open

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
- **Acceptance:** a lead recorded for the wrapper's owner
- **Disposition note:** open

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
- **Disposition note:** open

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-01"
  outcome: "open"
- id: PL-02
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-11"
  outcome: "open"
- id: PL-03
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-12"
  outcome: "open"
- id: PL-04
  severity: Info
  category: Renovation
  question: Q3
  source_finding: "F-01, F-11"
  outcome: "open"
- id: PL-05
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "F-03"
  outcome: "open"
- id: PL-06
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "F-04"
  outcome: "open"
- id: PL-07
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-05"
  outcome: "open"
- id: PL-08
  severity: Info
  category: Renovation
  question: Q2
  source_finding: "F-06"
  outcome: "open"
- id: PL-09
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-07"
  outcome: "open"
- id: PL-10
  severity: Info
  category: Renovation
  question: Q4
  source_finding: "F-08"
  outcome: "open"
- id: PL-11
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-09"
  outcome: "open"
- id: PL-12
  severity: Info
  category: Renovation
  question: Q7
  source_finding: "F-02"
  outcome: "open"
- id: PL-13
  severity: Info
  category: Renovation
  question: Q2
  source_finding: "F-04"
  outcome: "open"
- id: PL-14
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-10"
  outcome: "open"
```

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | the bug filed at stage D |
| PL-02 | Open | the coordinator's disposition at the stage-D pause |
| PL-03 | Open | the coordinator's disposition at the stage-D pause |
| PL-04 | Open | the coordinator's disposition at the stage-D pause |
| PL-05 | Open | the coordinator's disposition at the stage-D pause |
| PL-06 | Open | the coordinator's disposition at the stage-D pause |
| PL-07 | Open | the coordinator's disposition at the stage-D pause |
| PL-08 | Open | the coordinator's disposition at the stage-D pause |
| PL-09 | Open | the coordinator's disposition at the stage-D pause |
| PL-10 | Open | the coordinator's disposition at the stage-D pause |
| PL-11 | Open | the coordinator's disposition at the stage-D pause |
| PL-12 | Open | the coordinator's disposition at the stage-D pause |
| PL-13 | Open | the coordinator's disposition at the stage-D pause |
| PL-14 | Open | the coordinator's disposition at the stage-D pause |

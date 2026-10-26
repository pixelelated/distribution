# Analysis — M6.P2 T29, the per-handheld quirks (#676)

## Executive summary

- **What it read.** 333 files, 10,175 lines and 258,193 bytes of `quirks/devices/` at `8ebaf8daad`, copied into every image: 88 entries (65 directories, 23 aliases). 328 are upstream's and 5 the fork's.
- **The selection first.** `QUIRK_DEVICE` is the dt `model` (or the DMI pair) with `/` → `-`.
  - The two shipped trees and patch `0154` name **26 boards: 15 select an entry, 11 none, both owned H700 units among the none.**
  - On an RG35XX SP or an RG-SP no device quirk runs, only `platforms/H700/*`, and nothing they need is in a device entry (F-02).
- **Tier B** (70 paths: every board the shipped images boot that has an entry, and the VM) was read line by line as its 26 distinct blobs. Tier A was read again against the device facts and a host fixture.
- **One candidate bug, in a fork-own file (F-01, Low).**
  - The Nova's battery helper tests `led.color` unquoted (`:73`), and nothing seeds that setting.
  - On a fresh Nova, `batteryledstatus.service` lights all eight stick LEDs in battery colours at every boot. A host fixture shows it, with the `rgb` control unlit. This is D-UI-121's *"the default comes on"* (#332).
  - The same line is in 12 upstream files. The Odin 2's newer helper quotes it.
- **Brittleness, upstream's (F-03 to F-07):**
  - nine boards' `050-game-configs` revert a player's RetroArch audio driver and microphone at every boot;
  - four tier-B boards keep #332's unset-colour shapes the fork fixed only on the Nova;
  - `led.brightness` means words on the Nova and a percentage on the Thor;
  - no tier-B file guards a device node;
  - naming inconsistencies (`touchcontrol` is a file the loop runs).
- **Currency (F-08):** 18 commits pending, two of them panel calibration for the Thor and the RP6, *settled by the next base merge*.
- **Ten findings:** 3 Low (F-01, F-03, F-04), 7 Info. **Removals none.** **No guest; nothing on a unit.**

## Acceptance-criteria scorecard

#676's sixteen criteria (= brief § 7), at stage C before the punch-list issue. *Met* names its artifact; *waits* names the stage that ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C |
| 2 | the lint `PASS` | pre-issue at stage C; resolution waits for stage H |
| 3 | the plan, the provenance, the manifest | stage C |
| 4 | every punch item at a Phase 7 outcome | waits: stage D onward |
| 5 | `reviewed-at:` and `fixed-at:`; the 333 at `8ebaf8daad`'s bytes; nothing changed at A to D | the diffs are empty (r03, r20); the header lines wait for stage H |
| 6 | `01` § Scope | met (`e8dcd0ace5`), with the board-count delta |
| 7 | coverage, 333 rows | met: the brief's `awk` and `grep` print 333 |
| 8 | § The entries, 88 rows, generated with asserts | met (`tools/t29-tables.py entries`) |
| 9 | § The selection, § The tiers, § The fork-own five | met |
| 10 | § The shape, § The upstream delta | met |
| 11 | § The runs | met (generated, 22 rows) |
| 12 | `00` shows no guest, build, handheld command, M7 read or extra keyed call | met through stage B |
| 13 | `04` § Q2, Q3, Q4, Q6, Q7 and § Second opinion | met but § Second opinion (stage C) |
| 14 | every proof's cell; every punch item's `question:`; every `bug` `box-check` 0 fail | 14 proofs at stage B; `05` at stage C |
| 15 | the retro | waits: stage G |
| 16 | the five checkers | waits: stage H |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A fresh Nova's sticks light in battery colours before the player chooses anything | High (every fresh Nova) | Low (visible, not harmful) | F-01; the fixture shows it; #332 |
| A player's RetroArch audio driver or microphone choice reverted at every boot on nine boards | High where the board is used | Low | F-03; upstream's; four of the boards are in tier B |
| A model rename upstream silently drops an entry | Low | Medium | selection is by name only (`03` § 3.1); the board table is the check |
| A redirect to an absent `/dev` node creates a regular file there as root | Low | Low | F-06; on boards with that hardware the node exists |

## Coverage boundary

- **Read in full:** tier B, as its 26 distinct blobs, 1,692 lines; the fork-own five; the selection lines (T22's `002-autostart`, `autostart`, the wrapper, `quirks/package.mk:15-20`); `platforms/H700/*` by name and its `001-device_config`, `010-led_control` and `030-analog_leds`; the H700 trees' stick-LED nodes; `batteryledstatus.service`; `rocknix-info:6-12`; `backuptool`'s path list.
- **Read by row:** the rest, 263 paths and 7,290 lines (§ The entries: files, lines, flags, run-order prefixes).
- **Not read:** `platforms/**` beyond H700's by name (T22's); `call_achievements_hooks.sh` beyond its dispatch; the interface that writes `led.*` (ES, outside the tree).
- **Not run:** a guest or a unit. The LEDs' appearance is device fact line 31.

## Second opinion

*Written at stage C (the seat's probe and refutation).*

## Finding Verification

| Finding | Re-derivation | Verdict |
| --- | --- | --- |
| F-01 | b02 (13 copies; one quoted), b03 (the unit; no seed), b04 (the fixture: unset lit, `rgb` unlit, `battery` lit; RP6's copy the same) | confirmed |
| F-02 | b05 (`platforms/H700` by name; `030-analog_leds:7` rc 2), b06 (0 / 0 / 3 / 3 / 3 nodes), r11 and r21 (NONE) | confirmed |
| F-03 | b07 (106 rewriters; nine `050-game-configs` with the two `sed -i`; `009-commander-cfg` guarded); `backuptool:288` | confirmed |
| F-04 | b08 (EVO `:100-101`, Portal blob `:26-27`, achievements `:99-100`) | confirmed |
| F-05 | b09 (the Nova's words, Thor's percentage) | confirmed |
| F-06 | b10, r17 (one guard tree-wide) | confirmed |
| F-07 | r18, b11, the RG40XX V helper's `:21-23` and `:41-48` | confirmed |
| F-08 | r15, r16, b13 | confirmed |
| F-09 | r05, b14 | confirmed, with Delta 3 |
| F-10 | b12, r12, § The entries | confirmed |

**Narrowings made while writing:**
- F-03's tier-B count (four, not five) and F-01's class count (seven tier-B copies, not four) were corrected against b07 and b02.
- `03`'s settings-restore seam first said a backup carries `profile.d`. `backuptool`'s list carries `retroarch/*` and not `profile.d`, and the seam was rewritten.

## Renovation face

### Q1 Modernize

The design, as sentences for the coordinator (F-10):
- flag files rewritten at every boot (106) against a once-written file;
- dispatch by directory name against a declared capability;
- 23 alias symlinks against a table.

None is a defect, and the next base merge changes none of them.

### Q2 Standards

Tier B's findings, each file's lines quoted in `02`:
- **F-03:** `050-game-configs:6-7` (Thor `:8-9`) `sed -i '/^audio_driver =/c\audio_driver = "pulse"' ...retroarch.cfg` at every boot; `009-commander-cfg:6` the guarded counter-example.
- **F-04:** `AYANEO Pocket EVO/bin/ledcontrol:100-101` and the Portal blob's `:26-27`, `/usr/bin/analog_sticks_ledcontrol ${LEDS_CONFIG}` with no default; `bin/achievements:99-100`'s restore with no `led.color` check.
- **F-05:** `led.brightness` as `max|mid|min` (`Retroid Pocket Nova/bin/ledcontrol:24-26`) against percent (`AYN Thor/bin/battery_led_status:13-21`).
- **F-06:** `020-set-xbox-gamepad:7-16`, the DMG helper's `:37-53` and the RG40XX V's `/dev/ttyS2`, unguarded; one guard in 285 blobs.
- **The modes:** 71 `100644` (31 in tier B), masked by `package.mk:20`'s `chmod -R 0755`.
- **The wrappers' unquoted `$*`** is load-bearing for `analogsticks.led`'s seven numbers (`03` § 3.5), and no shipped caller passes a value that would split badly.

### Q3 Bugs

- **F-01, a candidate bug in a fork-own file.**
  - **The trace:** `batteryledstatus.service` (`WantedBy=multi-user.target`) → `/usr/bin/battery_led_status` → the Nova's `bin/battery_led_status:72-73`. `BAT_LED_STATE=$(get_setting led.color)`, then `if [ ! ${BAT_LED_STATE} == "battery" ]; then break`. With `led.color` unset, which nothing seeds, the loop runs battery mode.
  - **The VM line:** the host fixture `tools/t29-battery-unset.py`, in `tools/nova-led-test`'s shape. `unset lit=yes`, `rgb lit=no` (the control), `battery lit=yes`.
  - **`Already written:`** nothing persisted; `led.color` stays unset, and only the LEDs are driven at each boot.
  - **The fix is contained:** quote the variable, as upstream's Odin 2 helper does at `:63`. Its effect on what a fresh Nova shows is #332's question (D-UI-121). The coordinator decides a `bug` or #332.
- **The owned H700 units select no device entry (F-02).** `platforms/H700/*`, read by name: `001-device_config`, `010-led_control`, `010-governors`, `020-fan_control`, `030-suspend_mode`, `040-wifi_probe_retry`, `bin/ledcontrol`, `sleep.d/`, and the rest. It covers what the SP units need. The entries the H700 image selects add only stick-LED behaviour, and their trees declare the nodes while the SP trees do not (b06). Not a bug; no unit asked.
- **Upstream's F-03 and F-04 are not bugs here:** upstream behaviour on boards the fork does not own, so #585 lines (`bugs-are-agent-first.md` rule 6 asks for a contained fix *and* a host proof, and a fork that does not ship those boards gains nothing by carrying a fix).

### Q4 Package currency

- **The delta:** 18 commits pending, 12 without merges, over 31 paths (16 A, 3 D, 12 M). The two panel-calibration files for shipped boards are `AYN Thor/040-panel_calibration` (`56e5c48b74`) and `Retroid Pocket 6/040-panel_calibration` (`abfdcfb57f`). Both are *settled by the next base merge* (F-08).
- **No collision:** the Nova's three fork-own `M` rows have no upstream change behind them.
- **`rocknix-info:8`'s lead (F-09):** a second derivation, `tr -d '\0'` against `strings`, both with `/` → `-` (`:12`); T1's file, cited.

### Q5 Efficiency

- **The 333 by tier:** 6 / 70 / 263 paths; 396 / 2,885 / 7,290 lines.
- **The weight:** 258,193 bytes in every image, 263 of the paths selected by no shipped board.
- **The cost of placement** is bytes and a reader's time, not boot time: the loop runs only the selected directory.

### Q6 Dead ends

By tier, in D-WORKFLOW-209's words. The table, one row per entry, is `02` § The entries.

| Tier | Entries | Paths | Disposition |
| --- | ---: | ---: | --- |
| A | 2 directories | 6 | selected by a shipped unit or the VM |
| B (less A) | 12 directories, 2 aliases | 64 | selected by a board a shipped image boots |
| the rest | 51 directories, 21 aliases | 263 | carried by placement (D-WORKFLOW-185); an alias row names its target |

**Removals: none.** The generator asserts no disposition proposes one.

### Q7 Clarity and structure

**Partly.** The directory names are the dt `model` strings, so a reader who knows that rule can match a board to its entry. But:
- the rule is written in `002-autostart`, not in the directory;
- the aliases are symlinks, and nothing lists them;
- `bin/` is reached by wrappers, not by the loop, and only the `-f` test says which;
- a file with no numeric prefix, Thor's `touchcontrol`, also runs.

The owned H700 units select nothing, a fact only a table shows. `02` § The selection and § The entries are that table. The two `050-game*configs` spellings are a naming inconsistency, recorded. The Nova's runbook section is #1100's.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **None for a defect.**

### Codification gaps (proposals for the coordinator)

1. **A quirk that reads a setting must treat unset as its own case** (quote the variable; name the default). F-01's line is in 13 files. Upstream's Odin 2 helper is the model.
2. **A count over a selection rule's keys reads every source of the keys:** the trees *and* the kernel patches that set `model`. Patch `0154` held four of the 26.

## Quality self-check

- **Blindspot 13:** each scorecard row names its artifact.
- **Blindspot 22:** the fixture's `rgb` control shows the script can stay unlit; the HAS/NONE read's controls are the HAS rows.
- **Blindspot 31:** the selection was read from the code that runs it, not from a comment; the brief's `touchcontrol/` and `rocknix-info` claims were checked against the files.
- **Blindspot 46:** `touchcontrol` reads like a directory and is a file.
- **Blindspot 75:** every figure is a command at `8ebaf8daad`, counted unfiltered over paths with spaces (`-z`). Three typed claims were corrected after re-reading (§ Finding Verification).
- **Rules read this session:** `engineering-practices.md`, `upgrade-and-install.md`, `bugs-are-agent-first.md`, `issue-tracking.md`, `vm-first.md`, `adversarial-council.md`, `decision-register.md`. Decisions: D-WORKFLOW-185, -209, D-UI-121, D-QA-015, D-QA-027.

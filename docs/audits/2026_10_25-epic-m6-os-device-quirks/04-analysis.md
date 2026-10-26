# Analysis — M6.P2 T29, the per-handheld quirks (#676)

## Executive summary

- **What it read.** 333 files, 10,175 lines and 258,193 bytes of `quirks/devices/` at `8ebaf8daad`, copied into every image: 88 entries (65 directories, 23 aliases). 328 are upstream's and 5 the fork's.
- **The selection first.** `QUIRK_DEVICE` is the dt `model` (or the DMI pair) with `/` → `-`.
  - The two shipped trees and patch `0154` name **26 boards: 15 select an entry, 11 none, both owned H700 units among the none.**
  - On an RG35XX SP or an RG-SP no device quirk runs, only `platforms/H700/*`, and nothing they need is in a device entry (F-02).
- **Tier B** (70 paths: every board the shipped images boot that has an entry, and the VM) was read line by line as its 26 distinct blobs. Tier A was read again against the device facts and a host fixture.
- **Two defects in one fork-own file, the Nova's battery helper (F-01, F-11, Low), and one in the VM's (F-12, Low).**
  - **F-01:** the helper tests `led.color` unquoted (`:73`), and nothing seeds that setting. On a Nova that has not chosen a mode, the helper `098-deviceutils` starts at boot drives all eight stick LEDs in battery colours. A host fixture shows the writes, with the `rgb` control unlit. This is D-UI-121's *"the default comes on"* (#332). The coordinator ruled it a `bug`.
  - **F-11** (the seat's G-15): after a critical-battery blink, a return to the bucket painted before it leaves the LEDs off. The same fixture shows it.
  - **F-12** (the seat's G-11, G-12): the VM's `091-retired-vm-fixes` removes a listed file by name on its first pass, whatever it holds.
  - Both battery defects are in upstream's copies: the unquoted test reaches 15 model names. The Odin 2's newer helper avoids both.
- **Brittleness, upstream's (F-03 to F-07):**
  - nine boards' `050-game-configs` revert a player's RetroArch audio driver and microphone at every boot;
  - four tier-B boards keep #332's unset-colour shapes the fork fixed only on the Nova;
  - `led.brightness` means words on the Nova and a percentage on the Thor;
  - no tier-B file guards a device node;
  - naming inconsistencies (`touchcontrol` is a file the loop runs).
- **Currency (F-08):** 18 commits pending, two of them panel calibration for the Thor and the RP6, *settled by the next base merge*.
- **The seat** (GPT-6 Astra at `max`, served by OpenAI, `PASS`) returned 40 items: 9 confirmed, 18 narrowed, 4 refuted, 9 new. All 40 were re-read and accepted (§ Second opinion). Two findings came from it, and three of the first draft's claims were wrong.
- **Twelve findings:** 5 Low (F-01, F-03, F-04, F-11, F-12), 7 Info. 14 punch items. **Removals none.** **No guest; nothing on a unit.**

## Acceptance-criteria scorecard

#676's sixteen criteria (= brief § 7), at the hand-back (stage H). *Met* names its artifact; *waits* names who ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C |
| 2 | the lint `PASS` | pre-issue `PASS` at stages C to H; the full lint after acceptance, with `audit-completion.json` |
| 3 | the plan, the provenance, the manifest | met: `review-plan.json` `complete`; both provenance files `PASS`; `packet-manifest.json` |
| 4 | every punch item at a Phase 7 outcome | met: `05` § Phase 7, 7 Resolved, 7 Deferred, read back at stage F; #1121's checkboxes are the coordinator's at acceptance |
| 5 | `reviewed-at:` and `fixed-at:`; the 333 at `8ebaf8daad`'s bytes; nothing changed at A to D | the diffs were empty through stage D (r03, r20; `ce2af0ca7c`). Stage E changed the two fork-own files its brief names. `reviewed-at: 5ee0dfefcf` and `fixed-at: 04a9fe98b9` are in #676's body at the hand-back |
| 6 | `01` § Scope | met (`e8dcd0ace5`), with the board-count delta |
| 7 | coverage, 333 rows | met: the brief's `awk` and `grep` print 333 |
| 8 | § The entries, 88 rows, generated with asserts | met (`tools/t29-tables.py entries`) |
| 9 | § The selection, § The tiers, § The fork-own five | met |
| 10 | § The shape, § The upstream delta | met |
| 11 | § The runs | met (generated, 22 rows) |
| 12 | `00` shows no guest, build, handheld command, M7 read or extra keyed call | met through stage H: two keyed calls (P15); the M7 extract's bash was not used |
| 13 | `04` § Q2, Q3, Q4, Q6, Q7 and § Second opinion | met |
| 14 | every proof's cell; every punch item's `question:`; every `bug` `box-check` 0 fail | met: 18 proofs (16 in § Proofs, 2 in § The streams); `05`'s 14 items each carry `question:`; #1120 and #1124 `box-check` 0 fail, each with `Already written:` |
| 15 | the retro | met: `docs/retros/2026-10-26-m6-os-device-quirks.md`, posted on #676 at the hand-back |
| 16 | the five checkers | run at stage H on the branch (`00` § Stage H); re-run by the coordinator after its hand-back merge |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A fresh Nova's sticks are driven in battery colours before the player chooses anything | High (every Nova with `led.color` unset) | Low (visible, not harmful) | F-01; the fixture shows the writes; the appearance is device fact line 31; #332 |
| A Nova's sticks stay off after a critical-battery blink and a charge back to the bucket before it | Medium (every low-battery recovery in battery mode) | Low | F-11; the fixture shows it |
| A file a developer edited on a GENERIC_X64 guest is removed at the first boot of this build | Low (a one-boot window, a developer's tool, D-QA-053) | Low | F-12; the paths are VM-specific |
| A player's RetroArch audio driver or microphone choice reverted at every boot on nine boards | High where the board is used | Low | F-03; upstream's; four of the boards are in tier B |
| A model rename upstream silently drops an entry | Low | Medium | selection is by name only (`03` § 3.1); the board table is the check |
| A redirect to an absent `/dev` node creates a regular file there as root | Low | Low | F-06; on boards with that hardware the node exists |

## Coverage boundary

- **Read in full:** tier B, as its 26 distinct blobs, 1,692 lines; the fork-own five; the selection lines (T22's `002-autostart`, `autostart`, the wrapper, `quirks/package.mk:15-20`); `platforms/H700/*` by name and its `001-device_config`, `010-led_control` and `030-analog_leds`; the H700 trees' stick-LED nodes; `batteryledstatus.service`; `rocknix-info:6-12`; `backuptool`'s path list.
- **Read by row:** the rest, 263 paths and 7,290 lines (§ The entries: files, lines, flags, run-order prefixes).
- **Not read:** `platforms/**` beyond H700's by name (T22's); `call_achievements_hooks.sh` beyond its dispatch; the interface that writes `led.*` (ES, outside the tree).
- **Not run:** a guest or a unit. The LEDs' appearance is device fact line 31.

## Second opinion

**The seat.** GPT-6 Astra (`openai/gpt-6-astra`) at `max`, through the Facilitator on OpenRouter, pinned to OpenAI with no fallback.
- **The probe:** 04:57:41 to 04:57:52 UTC.
- **The refutation:** 04:57:57 to 05:11:15 UTC, rc 0, reasoning 26,416 tokens, `outcome=success`.
- Both provenance files read verification, effort and provider `PASS`, served by OpenAI (P15). Those were the only two keyed calls (D-WORKFLOW-195).
- **The packet:** `gpt-brief.md`, 178,989 bytes, scanned clean (`packet-manifest.json`).

**The result.** 40 items: **9 confirmed, 18 narrowed, 4 refuted, 9 new.**
- Every item was re-read against the tree at `8ebaf8daad` (`stage-c/rereads/` c01 to c09, all rc 0; P16) or against the lines the seat cites. **Every one was accepted.**
- Three of the first draft's claims were wrong: the VM's take-back *"no defect"* (G-11), the wrappers' *"load-bearing"* `$*` (G-2), and the unit's start (G-6).
- Two findings are the seat's: F-11 (G-15) and F-12 (G-11, G-12).
- The seat's *"I ran nothing"* holds: it had the fixture's output, not the fixture. G-9's point, that the RP6 run could not be reproduced from the tool as shown, was right, and the tool now carries the rewrite as a flag.

| Item | The seat | The seat's words (abridged) | Re-read | Lane's grade and where it landed |
| --- | --- | --- | --- | --- |
| G-1 | confirmed | *"executes direct, non-hidden entries satisfying `-f`, in shell glob order"* | r05 to r08 | accepted; `02` § The selection unchanged |
| G-2 | refuted | *"the shown caller does not justify retaining `$*`"* | c01: 22 callers, one quoted | accepted; `03` § 3.5 and `04` Q2 corrected; PL-13 |
| G-3 | narrowed | *"no omitted general-purpose quirk is identified ... not the unrestricted assertion"* | b05, b06 | accepted; F-02 says "identified", the lead is #1119 (under #695) |
| G-4 | confirmed | *"28 lines minus the repeated ... gives 26"* | r21, r22 | accepted |
| G-5 | confirmed | *"a valid software result, not proof of physical illumination"* | c03 | accepted; F-01 says "driven", device fact line 31 |
| G-6 | narrowed | *"`WantedBy=` is installation metadata, not evidence that the unit has actually been enabled"* | c02: `enable_service` 0; `030-led-control:7`, `098-deviceutils:31-34` | accepted; F-01's start rewritten to the real chain |
| G-7 | narrowed | *"nothing in the tree seeds it is a wider negative claim than these excerpts establish"* | c02: the seed `system.cfg` has no `led.*`; b03's four reads | accepted, with the tree-wide read the packet lacked |
| G-8 | narrowed | *"the sticks stay dark is too strong"* | the helper's `:14-23` | accepted; F-01's fix sentence rewritten |
| G-9 | refuted | *"not reproducible by the supplied tool against the supplied, unmodified RP6 script"* | c03: RP6 unlit without the rewrite, met with `--redirect-paths` | accepted; the tool has `--redirect-paths` and `--expect` |
| G-10 | narrowed | *"13 `DEVICE_*` assignments, not fourteen"* | c04: 13 | accepted; `02` corrected |
| G-11 | refuted | *"checks only `-e` and then unlinks the named path, regardless of its contents"* | c05: `:61-75` | accepted; F-12, PL-03 |
| G-12 | new | *"a listed dangling link can survive while the stamp is written"* | c05: `-e` on a dangling link is false | accepted; F-12 |
| G-13 | narrowed | *"a right RGB input of `255 0 0` produces the BGR write `0 0 255`"* | c06: `nova-led-test:54-55` | accepted; `02` corrected |
| G-14 | new | *"the next `ledcontrol rgb` uses the preset's 255 and never consults `led.brightness`"* | c07: `ledcontrol:53-58` | accepted; F-05, PL-07 |
| G-15 | new | *"the returning 15% pass therefore skips repainting and leaves the output off"* | c03: `critical-recovery lit=no` | accepted; F-11, PL-02 |
| G-16 | new | *"an empty capacity ... reaches the unconditional `D_GREEN` branch"* | the helper's `:82-85`, `:95-129` | accepted as a sibling in F-11; not fixture-run |
| G-17 | new | *"RGB can be applied, then overwritten by the remaining battery writes"* | the helper's `:72-74`, `:87-94` | accepted as a sibling in F-11; not fixture-run |
| G-18 | narrowed | *"the proposed 009 shape is not a drop-in fix"* | the two files | accepted; F-03 narrowed |
| G-19 | narrowed | *"turns them off is not what these branches do"* | c07, the DMG helper `:10-14` | accepted; F-04 says "writes nothing" |
| G-20 | narrowed | *"with a valid preset, it requests that preset ... `led.color` controls the power LED"* | c07: `call_achievements_hooks.sh:8-17` | accepted; F-04 narrowed |
| G-21 | narrowed | *"the supplied code does not identify which values the interface actually writes"* | the interface is outside the tree | accepted; F-05 |
| G-22 | new | *"`led_bri` is called only when a colour-paint function runs"* | Thor `battery_led_status:16-22`, `:48-56` | accepted; F-05 |
| G-23 | confirmed | *"conditional failure modes, not the first reader's unsupported reassurance"* | b10 | accepted; F-06's reassurance replaced |
| G-24 | new | *"not confined to the fork-owned Nova file"* | the four files' cited lines | accepted; F-11 class, PL-04 |
| G-25 | confirmed | *"the copied battery descriptions are at lines 6-7"* | c09 | accepted; F-07's lines corrected |
| G-26 | narrowed | *"a reasonable import disposition, not evidence that calibration has been tested"* | b13 (the log the packet lacked) | accepted; F-08 unchanged in disposition |
| G-27 | confirmed | *"both subsequently use an unquoted `echo` expansion"* | b14 | accepted; F-09 |
| G-28 | narrowed | F-01: *"enablement, actual initialization and physical illumination are separate questions"* | c02, c03 | accepted; F-01 |
| G-29 | narrowed | F-02: *"no missing device-entry functionality identified"* | b05, b06 | accepted; F-02's title kept, its body says "identified" |
| G-30 | narrowed | F-03: *"lack of an owned handheld is also not a valid dismissal"* | — | accepted; F-03's disposition reason rewritten |
| G-31 | narrowed | F-04: *"no new write, not necessarily turned off"* | c07 | accepted; F-04 |
| G-32 | narrowed | F-05: *"Thor additionally fails to apply a setting-only change"* | as G-22 | accepted; F-05 |
| G-33 | confirmed | F-06: *"a conditional code risk"* | b10, r17 | accepted |
| G-34 | confirmed | F-07: *"should remain informational"* | b11 | accepted |
| G-35 | narrowed | F-08: *"without calling it a completed correctness proof"* | b13 | accepted; the disposition is the merge's |
| G-36 | confirmed | F-09: *"the latent difference on short, non-printable or NUL-separated data"* | b14 | accepted |
| G-37 | narrowed | F-10: *"A is contained in B: 6 + 64 + 263 = 333"* | r12 | accepted; Q5 corrected |
| G-38 | new | *"affected file counts must not be substituted for affected model counts"* | c08: 15 names | accepted; F-01 and F-03 count names |
| G-39 | new | *"an existing-but-empty ... DT model is a missing selection test case"* | `002-autostart:6-12` | accepted; F-09, PL-11 |
| G-40 | refuted | *"ownership limits physical testing, not software relevance"* | — | accepted; F-03's and F-04's reasons, `03` § 3.2 |

**Where the seat's priority differs.** It ranks F-12 first (*"the highest-priority correction is the VM cleanup's deletion of unknown user content"*). The lane ranks the two Nova defects first, because the VM is a developer's tool (D-QA-053) and its window is one boot. The order is the coordinator's.

## Finding Verification

| Finding | Re-derivation | Verdict |
| --- | --- | --- |
| F-01 | b02 (13 copies; one quoted), b03 and c02 (the start chain; no seed), b04 and c03 (the fixture with `--expect`; RP6's copy with `--redirect-paths`), c08 (15 names) | confirmed, the start corrected |
| F-02 | b05 (`platforms/H700` by name; `030-analog_leds:7` rc 2), b06 (0 / 0 / 3 / 3 / 3 nodes), r11 and r21 (NONE) | confirmed |
| F-03 | b07 (106 rewriters; nine `050-game-configs` with the two `sed -i`; `009-commander-cfg` guarded); `backuptool:288` | confirmed |
| F-04 | b08 (EVO `:100-101`, Portal blob `:26-27`, achievements `:99-100`) | confirmed |
| F-05 | b09 (the Nova's words, Thor's percentage) | confirmed |
| F-06 | b10, r17 (one guard tree-wide) | confirmed |
| F-07 | r18, b11, the RG40XX V helper's `:21-23` and `:41-48` | confirmed |
| F-08 | r15, r16, b13 | confirmed |
| F-09 | r05, b14 | confirmed, with Delta 3 |
| F-10 | b12, r12, § The entries | confirmed, the tiers' sum corrected |
| F-11 | c03 (`critical-recovery lit=no`; `--expect fixed` refuses it); the Odin 2's `:62` | confirmed (the seat's G-15) |
| F-12 | c05 (`:61-75`; a dangling link's `-e` false) | confirmed by reading (the seat's G-11, G-12); no fixture run |

**The seat's corrections** are in § Second opinion; each landed in `02` with the item's number.

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
- **The wrappers' unquoted `$*`** adds a second round of splitting and pathname expansion; `"$@"` would pass the seven numbers unchanged (the seat's G-2, `03` § 3.5). No shipped caller passes a value that would split badly (c01). A lead for T22's wrapper (PL-13).

### Q3 Bugs

- **F-01 and F-11, two defects in one fork-own file: a `bug` (the coordinator's ruling for F-01; F-11 proposed for the same one).**
  - **The start:** `platforms/SM8550/030-led-control:7` sets `DEVICE_BATTERY_LED_STATUS="true"`. `098-deviceutils:31-34` then runs `systemctl start batteryledstatus`. The unit runs `/usr/bin/battery_led_status`, which execs the Nova's `bin/battery_led_status` (the seat's G-6 corrected the first draft's `WantedBy`).
  - **F-01:** `BAT_LED_STATE=$(get_setting led.color)`, then `:73` `if [ ! ${BAT_LED_STATE} == "battery" ]; then break`. With `led.color` unset, which nothing seeds (c02), the loop runs battery mode.
  - **F-11:** the critical branch (`:85-94`) ends off and `continue`s with `PREV_BATCAP` unchanged, so `:98` does not repaint a return to the earlier bucket.
  - **The VM line:** the host fixture `tools/t29-battery-unset.py --expect unfixed` (`unset lit=yes`, `rgb lit=no` the control, `battery lit=yes`, `critical-recovery lit=no`). A fixed file must pass `--expect fixed`; the unfixed one fails it on `unset, critical-recovery`.
  - **`Already written:`** nothing persisted. The helper reads `led.color` and writes only sysfs, never `set_setting`, so a Nova that booted with it unset holds nothing of this helper's on `/storage` to migrate.
  - **The fix is contained:** quote the variable and invalidate the cache before the blink, as upstream's Odin 2 helper does (`:63`, `:62`). What a fresh Nova then shows is #332's device fact (D-UI-121, line 31).
- **F-12, the VM's take-back.** `091-retired-vm-fixes:61-75` removes a listed file by name before the stamp exists, and a dangling link survives the stamp. Fork-own, VM-only (D-QA-053), a one-boot window. The disposition is the coordinator's: a hardening with a host fixture, or recorded (PL-03).
- **The upstream copies** of both battery defects (F-01's in 12 files, 15 model names; F-11's in ACE, EVO, Odin 2 Portal and Thor) are per-unit dispositions (D-WORKFLOW-209) and #585 lines, with the Odin 2's helper as the model (PL-04).
- **The owned H700 units select no device entry (F-02).** `platforms/H700/*`, read by name: `001-device_config`, `010-led_control`, `010-governors`, `020-fan_control`, `030-suspend_mode`, `040-wifi_probe_retry`, `bin/ledcontrol`, `sleep.d/`, and the rest. No missing need was identified there, which is narrower than *"everything they need"* (the seat's G-29). The entries the H700 image selects add only stick-LED behaviour, and their trees declare the nodes while the SP trees do not (b06). Not a bug; no unit asked.
- **Upstream's F-03 and F-04 are per-unit dispositions, not bugs filed one per copy:** upstream behaviour on boards the shipped images support (D-WORKFLOW-209), so #585 lines. The first draft's reason, *"boards the fork does not own"*, was wrong (the seat's G-40).

### Q4 Package currency

- **The delta:** 18 commits pending, 12 without merges, over 31 paths (16 A, 3 D, 12 M). The two panel-calibration files for shipped boards are `AYN Thor/040-panel_calibration` (`56e5c48b74`) and `Retroid Pocket 6/040-panel_calibration` (`abfdcfb57f`). Both are *settled by the next base merge* (F-08).
- **No collision:** the Nova's three fork-own `M` rows have no upstream change behind them.
- **`rocknix-info:8`'s lead (F-09):** a second derivation, `tr -d '\0'` against `strings`, both with `/` → `-` (`:12`); T1's file, cited.

### Q5 Efficiency

- **The 333 by tier:** A is inside B, so the disjoint sum is **6 + 64 + 263 = 333** paths (A, B less A, the rest; the seat's G-37). B whole is 70 paths. Lines: 396 in A, 2,885 in B whole, 7,290 in the rest.
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
3. **A host fixture asserts, and covers the path a helper hard-codes.** The first fixture printed and could not fail, and its RP6 result needed a rewrite the tool did not carry (the seat's G-9). `--expect` and `--redirect-paths` are that rule applied here. It is `engineering-practices.md` § Guards must fail closed, so no new rule is proposed: a work-log line.

## Quality self-check

- **Blindspot 13:** each scorecard row names its artifact.
- **Blindspot 22:** the fixture's `rgb` control shows the script can stay unlit; the HAS/NONE read's controls are the HAS rows.
- **Blindspot 31:** the selection was read from the code that runs it, not from a comment; the brief's `touchcontrol/` and `rocknix-info` claims were checked against the files.
- **Blindspot 46:** `touchcontrol` reads like a directory and is a file.
- **Blindspot 75:** every figure is a command at `8ebaf8daad`, counted unfiltered over paths with spaces (`-z`). Three typed claims were corrected after re-reading (§ Finding Verification), and the seat corrected four more (13 flags, the channel example, the header lines, the reach by name).
- **Blindspot 22 again, from the seat:** the first fixture could not fail. It asserts now, and the unfixed file fails `--expect fixed`.
- **Rules read this session:** `engineering-practices.md`, `upgrade-and-install.md`, `bugs-are-agent-first.md`, `issue-tracking.md`, `vm-first.md`, `adversarial-council.md`, `decision-register.md`. Decisions: D-WORKFLOW-185, -209, D-UI-121, D-QA-015, D-QA-027.

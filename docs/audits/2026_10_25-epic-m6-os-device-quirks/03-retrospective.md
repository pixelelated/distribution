# Retrospective audit — M6.P2 T29, the per-handheld quirks (#676)

Phase 3 over a currency slice read under brittleness. 328 of the 333 are upstream's and every one is copied into every image. The question is which of them run on the shipped units and the VM, how they fail, and what meets them at the seams.

## 3.1 Architectural coherence

- **Selection is by name, and the name is the device tree's.**
  - `QUIRK_DEVICE` is the dt `model` (or the DMI pair) with `/` → `-` (`002-autostart:6-12`), and a directory under `devices/` is selected when its name equals it.
  - Nothing declares which boards an entry serves; the name is the declaration. A model string changed upstream silently drops its entry, and an alias symlink is the only way two names share one.
  - So the 88-entry table, generated with each board's `model` line beside its entry (`02` § The entries, § The selection), is the first place the mapping is written down.
- **Two kinds of file, two ways in.**
  - Files directly in the directory run at boot, as root, in glob order (`autostart:31-43`, `-f`).
  - `bin/` helpers run when a wrapper calls them (`ledcontrol` and its siblings at `:14-17`).
  - A reader cannot tell from a directory which files run at boot except by that rule. `AYN Thor/touchcontrol` shows the rule bites both ways: it is a file, not a directory, so it runs (`02` Delta 2).
- **The owned H700 units select nothing, by design.** Entries exist for boards with stick LEDs, and the platform set covers the rest (`02` F-02).

## 3.2 Project conformance

- **`engineering-practices.md` § Guards must fail closed.** Tier B has no guard on a device node (`02` F-06). One unquoted test turns *"no setting"* into *"battery mode"* (F-01). The tree's one guard (the x55's `040-hdmi`) and the Odin 2's quoted, input-checking battery helper are upstream's own counter-examples.
- **`upgrade-and-install.md`: `Already written:`.**
  - Every-boot heredocs mean what a device already has is rewritten at the next boot. So a fix to a flag file needs no migration.
  - A fix to the `050-game-configs` `sed -i` (F-03) cannot give back a player's audio driver that every earlier boot reverted.
  - The VM's `091-retired-vm-fixes` applies the rule only once its stamp exists. Its first pass removes a listed file by name, whatever it holds, and a dangling link survives the stamp (`02` F-12, the seat's G-11 and G-12). The first draft called it *"applied well"*.
- **`engineering-practices.md` § A name is not a behaviour.** `touchcontrol` (a name that reads like a directory) and the `050-game*configs` spellings are the cases. The brief's *"`rocknix-info` has no `/` → `-` sed"* was a claim the file contradicts (`02` Delta 3).
- **`bugs-are-agent-first.md` rule 6.** F-01's and F-11's fixes are contained and fork-own, and their proof is a host fixture, so they are a `bug` (the coordinator's ruling for F-01, 05:0x UTC). F-03, F-04 and the upstream copies of both battery defects are upstream's behaviour on boards the shipped images support. They are per-unit dispositions (D-WORKFLOW-209) and #585 lines, not bugs filed one per copy. The first draft's *"boards the fork does not own"* was the wrong reason (the seat's G-40).

## 3.3 Spec fidelity

The brief's figures were re-derived at stage A. Four deltas are recorded rather than corrected (`02` § Deltas):
- 26 boards, not 28;
- `touchcontrol` is a file;
- `rocknix-info` does convert `/` to `-`;
- the first command's `tools` diff.

The tiers, the history, the delta, the shape and the fork-own five held.

## 3.4 Platform conformance

As behaviour, the Nova's helpers are proven on a host fixture (`tools/t29-battery-unset.py`, and `tools/nova-led-test`'s shape). The VM's two files run on every guest boot (T22's guest record). The H700 units run no device quirk. **No guest ran in this slice, and nothing ran on a unit.** What the LEDs look like is device fact line 31 (an open item to test, #332).

## 3.5 Cross-system interaction audit

### Interaction: T22's wrappers x the device helpers

- **The shared state:** the argument list.
  - `system-utils/sources/scripts/ledcontrol:15` `exec`s the device's helper with `$*`, unquoted.
  - The callers pass a fixed word (`off`, `rgb`, `battery`, `brightness max`) or `analogsticks.led`'s seven numbers, which the helpers then re-split (`ledcontrol:58`, `analog_sticks_ledcontrol ${LEDS_CONFIG}`).
- **The interaction, corrected by the seat (G-2).** The first draft called `$*` load-bearing for the seven numbers. It is not: the caller splits `${LEDS_CONFIG}` already, and `"$@"` in the wrapper would pass the same seven arguments. The unquoted `$*` adds a second round of splitting and pathname expansion.
  - Of the 22 caller lines (`stage-c/rereads/c01`), only RG Vita Pro's `achievements:40` quotes its single word. None passes a value with a space or a glob character today.
- **The two files' owners:** the wrapper is T22's (#669), the helpers this slice's. `"$@"` is a lead for the wrapper's owner (PL-13), not a change here.

### Interaction: the next base merge x the 31 paths

- **The shared state:** the directory.
  - Upstream adds 16 paths, two of them panel calibration for the Thor and the RP6 (`02` F-08), and deletes three.
  - It changes nine paths outside tier A.
  - It has not touched the Nova's directory since the base, so the fork's three `M` rows meet nothing.
- **Upstream-side cost.** The merge brings two new models' directories (the Duo Lite, the Classic 6 Rev Q) into every image, and they are *carried by placement*.

### Interaction: #332 and D-UI-121 x the fork-own LED helpers

- **The shared state:** `led.color`, `led.brightness` and `analogsticks.led` in `system.cfg`, read by the helpers and written by the interface.
- **The interaction.** The interface's writes decide what the helpers do.
  - F-01: an unset `led.color` reads as battery mode.
  - F-05: `led.brightness` is words to the Nova and a percentage to the Thor.
  - F-04: an unset `analogsticks.led` lights nothing on four tier-B boards.
- **Which issue owns it:** #332 owns the Nova's behaviour (D-UI-121 deferred it after RC2). This slice supplies the mechanism and a fixture, not a decision.

### Interaction: a settings restore x the every-boot rewrites

- **The shared state:** `retroarch.cfg`, which a settings backup carries (`backuptool:288`, `/storage/.config/retroarch/*`). `profile.d/` is not in `backuptool`'s list.
- **The interaction.** A restored `retroarch.cfg` keeps the player's audio driver and microphone choice only until the next boot, when `050-game-configs` rewrites both keys on the nine boards that carry it (F-03). The flag files are not restored at all; each boot's heredoc writes them fresh.
- **The VM's `091` names a restore as one way an earlier build's files come back** under `/storage/.config`, and takes them back by hash. Whether a given path is in a backup is `backuptool`'s list, not this slice's.

### Interaction: T27's and T28's trees x the entries

- **The shared state:** the `model` strings.
- **The interaction.** The H700 and SM8550 trees, and patch `0154`, are the only places a board's key is written; the entry's directory name must match it exactly.
  - 15 boards match. 11 do not, both owned H700 units among them, by design (F-02).
  - The duplicate `Anbernic RG34XX-SP` in two trees is harmless: both select the same name, which has no entry.

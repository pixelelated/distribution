# Research notes — M6.P2 T29, the per-handheld quirks (#676)

## Scope

- **The read hash:** `8ebaf8daad`; the 333 are byte-equal at the dispatch tip `5ee0dfefcf` (r03 `[]`, path-safe). **`reviewed-at`:** `5ee0dfefcf`. **Upstream read:** `651150fc88`, by name. **Base:** `c445081a59`.
- **The block** (brief § 2, `stage-a/scope.sh`, r01):

  ```text
  paths 333 lines 10175 {'shipped': 333} {'upstream-carried': 328, 'fork-own': 5} {'os-scripts-and-launch': 333}
  {'symlink': 48, 'shell': 266, 'none': 12, 'other': 7}
  read 266 9327 fork-own 5 fork-own paths [the VM's 001-device_config and 091-retired-vm-fixes; the Nova's bin/{analog_sticks_ledcontrol,battery_led_status,ledcontrol}]
  entries 88 of which top-level symlinks 23
  ```

  - **333 paths, 10,175 lines; shipped 333; upstream-carried 328, fork-own 5.**
  - **Read: 266 shell files / 9,327 lines.** The fork-own five are 389 lines (`02` § The fork-own five).
  - **88 top-level entries = 65 model directories + 23 aliases.** 48 symlinks in all: 23 top-level and 25 inside directories (r04).
- **The tiers** (`stage-a/tiers.sh`, r12):

| Tier | What | Paths | Lines | Fork-own |
| --- | --- | ---: | ---: | ---: |
| A | the units the maintainer owns, and the VM: `Retroid Pocket Nova/`, `QEMU Standard PC (Q35 + ICH9, 2009)/` | 6 | 396 | 5 |
| B | every board the H700 and SM8550 images boot that has an entry, and the VM: 14 directories and 2 aliases | 70 | 2,885 | 5 |
| the rest | selected by no board a shipped image boots: 51 directories and 21 aliases | 263 | 7,290 | 0 |

- **The selection** (r05 to r08, r11, r21, r22):
  - `QUIRK_DEVICE` comes from the dt `model`, else the DMI pair, with `/` → `-` (`002-autostart:6-12`).
  - Only files directly in `devices/${QUIRK_DEVICE}/` run, as root, in glob order (`autostart:31-43`, `-f`).
  - `bin/` is reached through the wrappers.
  - **26 distinct boards in the two shipped trees and patch `0154`: 15 HAS, 11 NONE. Both owned H700 units, `Anbernic RG35XX SP` and `Anbernic RG-SP`, select no device entry.**
- **History, with its populations** (r13, r14):
  - over the 333: **6** fork commits since the base; since `2026-06-01T00:00:00Z`, **28** non-merge, **6** the fork's;
  - over the directory: **9** since the base; since June **32**, **9** the fork's and **23** upstream's.
- **The delta** (r15, r16): **16 A, 3 D, 12 M** in upstream's direction. **18** commits pending, **12** without merges. The two `040-panel_calibration` files for shipped boards are AYN Thor and Retroid Pocket 6.
- **The weight:** 285 blobs (214 `100755`, 71 `100644`) and 48 symlinks (r17).
- **Deltas from the brief:**
  - the board count: 28 lines, 26 distinct boards, against the brief's 29 strings and 28 boards;
  - P1's 15 tools files in the first command's `tools` diff.
  - Every other figure held.

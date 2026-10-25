# Research notes — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

## Scope

- **The read hash:** `8ebaf8daad`; the 29 are byte-equal at the dispatch tip `458e2bfda1` (r03 `[]`). **`reviewed-at`:** `458e2bfda1`. **Upstream read:** `651150fc88`, by name. **Base:** `c445081a59`.
- **The block** (brief § 2, `stage-a/scope.sh`, r01):

  ```text
  paths 29 lines 28053 {'shipped': 29} {'upstream-carried': 29}
  {'shell': 2, 'other': 3, 'yaml': 8, 'devicetree': 16}
  read 2 118 fork-own 0
  whole directory in the inventory 85 57561 {'devices': 29, 'patches-and-configs': 56}
  ```

  - **29 paths, 28,053 lines; shipped 29; upstream-carried 29.**
  - **Read: 2 files / 118 lines / 0 fork-own:** `options` 81 and `bootloader/update.sh` 37.
  - **The whole directory:** 85 inventory rows / 57,561 lines, 56 of them T41's `patches-and-configs` rows (the configuration and the 55 live patches).
- **The 16 device-tree sources** (2 `.dtsi`, 14 `.dts`, 6,267 lines) are read here, though the language rule does not count them as *read*. `02` § The device trees has their rows.
- **`patches/linux/0053-add-hynitron-touchscreen.patch.disabled`:** 20,593 lines (r05), 73.4 % of the slice, born at that name (`aa458af6f9`).
- **The configuration** (T41's row, read for the shape, r06 to r10):
  - `# Linux/arm64 7.2.0 Kernel Configuration`, 8,608 lines, against the recipe's `7.2`.
  - Against `651150fc88`'s copy: **7 removed / 7 added**, every line a compiler stamp or one of two option flips.
  - **0 fork non-merge commits since the base;** upstream's four since.
  - Its distance from the other Qualcomm configurations (r08, the brief's command): SM8650 41/36, SM8750 81/105, SM6115 228/133, SM4450 229/189, SM8250 371/204. **Delta:** the brief's text gives each pair reversed.
- **History** (r25, r26):
  - **24 non-merge commits** over the 29 since `2026-06-01T00:00:00Z` (27 with merges), **fork 0**; the directory 54 / 63; a bare `--since=2026-06-01` prints 52.
  - `git log --no-merges 651150fc88..8ebaf8daad -- projects/ROCKNIX/devices/SM8550` is empty.
- **The upstream delta** (r27, r28):
  - **2 M over the 29** (`bootloader/update.sh`, `options`; +20 / -14);
  - **4 M 2 A over the directory** (+ the conf, patch 0104, and the new patches 0508 and 0509; +451 / -22).
- **Upstream's boot change, 2026-10-01 to 10-24** (r29, 18 commits on the directory, `scripts/mkimage`, `rocknix-abl` and `openabl`):
  - `0340192729` (10-01, ` gpt` on the command line);
  - `15123b2951` (10-01, rocknix-abl's sha);
  - `71d8932b33` (10-14, openabl `1.0`);
  - `a5d0dd4d57` (10-19, `1.1`);
  - `471a2711ce` (10-22, `HW_CPU`);
  - `7842b3b429` (10-22, the unused update case);
  - **`cafbb1657d` (10-22, Boot Loader Spec)**;
  - `73ffb8ee37` (10-24, openabl `1.2`);
  - the merge `651150fc88` (#3547, `qcom-bls`).
  - #1099 owns what the next base merge must answer.
- **Deltas from the brief:** r08's pair order. Every other figure held.

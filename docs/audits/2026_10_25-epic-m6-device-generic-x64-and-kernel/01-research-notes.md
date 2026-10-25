# Research notes — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

## Scope

- **The read hash:** `8ebaf8daad`; the 58 are byte-equal at the dispatch tip `2103f0271d`. **`reviewed-at`:** `2103f0271d`. **Upstream:** `651150fc88`, read locally.
- **The membership:** brief § 2's block, run at P1's `2174265e9c`:

  ```text
  paths 58 lines 10418
  read 14 1820 fork-own read 1421
  tier {'fork-own': 11, 'upstream-carried': 46, 'vendor-carried': 1} reach {'shipped': 49, 'test': 9}
  GENERIC_X64 fork-own lines 1217
  written 58 .qa-scratch/t11/paths.txt
  ```

  - The 58 are in `stage-a/paths.txt` and the 14 read in `stage-a/read.txt`.
  - **Erratum:** the order's *989 fork-own lines* does not reproduce. GENERIC_X64's fork-own rows sum to **1,217** over 8 paths, and no subset gives 989.
- **The configuration's two candidates** (`diff` line counts, removed / added):

  | Candidate | Lines | Its header | Removed | Added |
  | --- | ---: | --- | ---: | ---: |
  | `projects/Generic/linux/linux.x86_64.conf` | 8,062 | `Linux/x86 7.1.2` | 659 | 351 |
  | `projects/ROCKNIX/devices/AMD64/linux/linux.x86_64.conf` | 12,445 | `Linux/x86 7.1.2` | 7,671 | 2,980 |

  - Ours is 7,754 lines, with the header `Linux/x86 6.15.6`. The recipe builds `7.1.2` for GENERIC_X64 (`projects/ROCKNIX/packages/linux/package.mk:36-37`).
  - The Generic conf is the nearest. The AMD64 conf is not a base.
- **The history since 2026-06-01:** 110 non-merge commits on the 58. **40 fork-authored** across three identities (Max Engel 36, blitterbot 3, rasterabot 1); **70 upstream**.
- **The upstream delta** at `651150fc88`: **7 M** and **11 D**. The 11 are fork-only files that never existed upstream: the GENERIC_X64 device's nine, `bootloader/install` and `filesystem/etc/machine-info`.
- **A delta from the brief:** the `tools/vm-*` callers do not reach the launcher by basename. The one that runs it, `tools/vm-pair:36/74`, uses its full path through `$VM_TOOL`; the basename appears only in comments and help text (`00`).

## Phase 1

To be written at stage B: what each read file does, from the bytes at `8ebaf8daad`.

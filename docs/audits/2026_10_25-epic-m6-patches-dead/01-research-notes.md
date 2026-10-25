# Research notes — M6.P2 T40, the patches and kernel configurations no plan applies (#687)

## Scope

- **The read hash:** `8ebaf8daad`. `packages/` and `projects/` are unchanged at the dispatch tip `b8cde6f305`. **`reviewed-at`:** `b8cde6f305`.
- **T23's table:** `feature/m6-packages-dead-ends-670` at `f1561559aa`, `02-forward-audit.md` § Reachability, 731 units, read with `git show`.
- **The membership:** brief § 2's block, run at P1's `2174265e9c` over `docs/reviews/inventory.json`:

  ```text
  paths 778 lines 317908 {'vendor-carried': 778}
  patch 760 conf 18 shadowed 351 to the ROCKNIX linux 277
  ```

  `reachable_by`, `buildable_by` and `last_fork_commit` are empty on all 778 (`stage-a/scope.out`; the list is `stage-a/paths.txt`).
- **The five classes**, reproduced (`tools/t40-tables.py stats`; first match in order):

  | Class | Rows | Lines |
  | --- | ---: | ---: |
  | (a) generic kernel patches (`packages/linux/patches/{rockchip 187, rockchip-old 48, dvb 39, default 3}`) | 277 | 92,389 |
  | (b) other projects' (Amlogic 94, Allwinner 81, Rockchip 15, Samsung 15, NXP 14, RPi 7, Generic 3, Qualcomm 3, ARM 2; the 18 confs among them) | 234 | 160,488 |
  | (c) a `patches/x86_64` directory never selected | 5 | 99 |
  | (d) inside a T23 dead unit (117 units) | 234 | 63,795 |
  | (e) the rest | 28 | 1,137 |
  | **Total** | **778** | **317,908** |

  **(e) splits 6 + 16 + 2 + 4:**
  - e1, generic recipes a live override sources: fluidsynth 1, readline 1, and **gcc 3 and cmake 1**. The ROCKNIX `gcc` and `cmake` overrides carry `patches` as a git symlink (mode `120000`) to the generic directory, so `unpack`'s `${PKG_DIR}/patches/*.patch` applies these four on every image: **reached after all**.
  - e2: 16 LibreELEC `packages/emulation/libretro-*`, and 2 ROCKNIX-own rows in unbuilt recipes (`panda3ds-lr/patches/gles/000-enable-gles.patch`, 270 lines; `play-lr/patches/000-fix-build.patch`, 10).
  - 4 rows: the dvb `crazycat` and `dvb-latest` `disable-pci` patches, and `linux-firmware/rtl8723bs_bt`'s two.
- **The headers** (760 `.patch`): 746 with `From:` and `Subject:`; 14 hand-made diffs without them (`stage-a/headerless.txt`):
  - 12 ROCKNIX's: `strace-0001-autoreconf`, `connman-01-do-not-cleanup-routes`, grub's `gnulib-regcomp`, `menu-text` and `silent-boot`, `panda3ds-lr`'s `000-enable-gles`, `play-lr`'s `000-fix-build`, vitaquake2's four `001-set-platform`, and ES's `cpugov`;
  - 2 LibreELEC's: `mesa-001-fix-addrlib-lgcc-link` and `ffmpeg/patches/rpi/0001-rpi`.
- **Already deleted at `upstream/next`:** 6 rows, strace's two and grub's four (the local `upstream/next`, `651150fc88`).
- **The churn:** 102 upstream commits reach the 778 since 2026-06-01.
  - 99 are LibreELEC's: its developers' commits and its pull-request merges.
  - 3 are ROCKNIX's own: `74818e9c94`, `40fce2a089` (which added `cpugov.patch`, 2026-08-20) and the merge `96aff382c4`.
  - **0 fork-authored, ever.**
- **The shadowed 74 not the kernel's:** 2 content duplicates (kmod, systemd), 4 reached through the symlinks (gcc 3, cmake 1), and 68 others. Of the 68, 12 carry the same change re-offset in the override, 6 the same changed lines with the context moved, and 50 have no counterpart.

## Phase 1

To be written at stage B: what the dead patch set is, by class, and the x86_64 trace.

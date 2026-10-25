# Retrospective (Phase 3) — M6.P2 T23, the generic packages no image builds (#670)

The audit's Phase 3: how the dead set came to be, and where it meets the rest of the tree. This is not the slice's mini-retro (stage G, `docs/retros/`).

## 3.1 What the dead set is

- **LibreELEC's media centre, carried whole.** `packages/addons` (297 units, 65,790 lines) and `packages/mediacenter` (166, 4,885) are 463 of the 731 units and 70,675 of the 95,892 lines. 447 of those 463 are *dead, upstream-carried*: Kodi, its binary and service addons and their dependency trees, which no ROCKNIX image builds. One file in the set is 34,569 lines on its own (`snapserver`'s `snapweb/3rd-party`).
- **The generic copies the ROCKNIX overrides replace.** 101 units are shadowed copies:
  - 94 with the override live (`busybox`, `systemd`, `openssl`, `go`, `installer`, ...);
  - 7 with the override dead too (the generic halves of `connman`, `grub`, `qemu`, `strace`, `rkbin`, `weston` and `cbindgen`).
- **`projects/ROCKNIX`'s own dead rows,** 28 units and 1,300 lines:
  - 16 unshipped (other SoCs' recipes);
  - 7 dead, upstream-carried;
  - 4 reached after all;
  - 1 fork-own and dead (`cbindgen`).

## 3.2 How it stays

Upstream has made 0 commits on `packages/` since the base `c445081a59`. LibreELEC reaches it only through ROCKNIX's merges of LibreELEC (the last on `upstream/next` is `d43d166b7a`, 2026-08-12, a Kodi merge). The set is carried, not maintained here: nothing in this fork edits it except `installer` (`459feac81e`, 2026-07-01, an edit to the copy no plan uses).

## 3.3 What was hard

- **Plan generation is not offline.** `pkgjson` sources every recipe, and one dead recipe's global scope runs `curl`. The first five plans reached the network before that was seen; every later run used a shim (`00`).
- **The host is not the build container.** `xmlstarlet` is absent, so H700's bootloader chain drops out of a host plan with no error. The table had to take the container's plan where the host cannot see.
- **The brief's `pkgcheck` form checked nothing and passed.** The tool exits 0 when an argument matches no recipe.

## 3.5 The seams

| Seam | What crosses it | What the read found |
| --- | --- | --- |
| the inventory tool × the plans | `compute_reach` follows plan names and `. ${ROOT}/packages/...` sourcing | it does not follow `PKG_DEPENDS_UNPACK`: five units every plan unpacks read `unreached` (§ Disagreements); a `bug` at stage D |
| the plans × the host | `tools/viewplan` under `config/options` | `SUBDEVICES` through `xmlstarlet ... 2>/dev/null`: a host without `xmlstarlet` plans H700 without its bootloader chain, in silence |
| the plans × the network | `pkgjson` sources every recipe | `mesa-reusable:15` runs `curl` at parse time, so every plan generation makes a request; a `bug` at stage D |
| the overrides × the generic copies | `get_pkg_directory` prefers the project/device cache | all eleven basename pairs resolve to the ROCKNIX copy on all three devices. Four generic recipes are sourced by their overrides, and their other files are unused |
| this table × T7's and T8's | the live copy of a shadowed unit is T7's or T8's row | 94 units point at a live override in those tables; the 5 reached after all leave this slice's set (the coordinator hands them on) |
| this table × T40's patches | the patch directories of these units | no `.patch` in the set; under D-WORKFLOW-209 nothing is removed, so T40 records nothing as removed by T23 |
| this table × `upstream/next` | 11 upstream-carried rows differ there | 8 deleted upstream after the base, 3 modified. Of the 8: the three rust snapshots are reached today but leave with their override at the next merge; `strace`, `grub` (3 files) and `qemu` are dead and cost nothing to drop |

## 3.6 Time to play

Nothing. These are recipes no image builds, and nothing in the slice ran on a device or a guest.

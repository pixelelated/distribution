# Retrospective (Phase 3) — M6.P2 T40, the patches and kernel configurations no plan applies (#687)

The audit's Phase 3: how the dead patch set came to be, and where it meets the rest of the tree. This is not the slice's mini-retro (stage G, `docs/retros/`).

## 3.1 What the dead patch set is

- **LibreELEC's kernel patch tree** (class a, 277 rows, 92,389 lines): `packages/linux/patches/{rockchip, rockchip-old, dvb, default}`. Every ROCKNIX device builds `projects/ROCKNIX/packages/linux`, which neither sources the generic recipe nor shares a patch with it.
- **Eight other projects' patches and kernel configurations** (class b, 234 rows, 160,488 lines; the 18 confs are 125,933 of them). The fork's Makefile builds only `PROJECT=ROCKNIX`.
- **The patches of T23's dead units** (class d, 234 rows in 117 units). They follow T23's dispositions: 152 in units dead and upstream-carried, 67 in shadowed copies whose override is live, 9 where the override is dead too, and 6 already deleted at `upstream/next`.
- **Two ROCKNIX mistakes:** five `patches/x86_64` files `unpack` never selects (class c), and four generic patches that are not dead at all, applied through symlinked `patches` directories (e1).

## 3.2 How it stays

None of the 778 has ever had a fork commit. 102 upstream commits have reached them since 2026-06-01: 99 LibreELEC's, which arrived through ROCKNIX's merges of LibreELEC (`br-update`, PR #3172), and 3 ROCKNIX's own. Like T23's set, it is carried rather than maintained.

## 3.3 What was hard

- **What "a duplicate" means.** The strict test (the diff body byte-equal) gives the brief's 2. Setting hunk headers aside gives 14, and comparing changed lines only gives 20. The table keeps the strict 2 as duplicates and records each of the other 68's tier. So the *68 LibreELEC changes the override builds without* are really 50 with no counterpart, plus 18 the override carries in another form.
- **The generator's first symlink test compared the wrong path** and called gcc and cmake dead. It was caught before any figure was used.

## 3.5 The seams

| Seam | What crosses it | What the read found |
| --- | --- | --- |
| `unpack` × the arch directories | `PATCH_ARCH=x86` on x86_64 (`:127-128`, since 2014) | no recipe has `patches/x86/`; the only x86 directories are the five `patches/x86_64` that are never read (the bug) |
| `unpack` × the symlinked `patches` | `${PKG_DIR}/patches/*.patch` follows a symlinked directory | gcc's and cmake's overrides apply the generic patches on every image |
| the inventory × the symlinks | `selected_patch_dirs` normalizes without resolving a link | the four applied rows read `unreached` (the second bug, beside #1049's `PKG_DEPENDS_UNPACK` gap) |
| this table × T23's | class (d) rows carry their unit's T23 disposition | 234 rows in 117 units, so T23's #346 decision decides them too |
| the overrides × the generic copies | 74 shadowed non-kernel patches | 2 duplicates, 4 applied after all, 18 carried by the override in another form, and 50 changes the override builds without (T41's and T42's leads) |
| this table × `upstream/next` | 6 rows deleted there since the base | strace's two and grub's four; the next base merge settles them |
| this table × LibreELEC's merges | 99 of the 102 commits since June | the conflict cost of deleting upstream-carried patches |

## 3.6 Time to play

Nothing. No row is applied to an image that runs (except the four reached after all, which already are), and nothing here ran on a device or a guest.

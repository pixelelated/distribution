# T42 #689: bounded membership and boundary research

Author: Codex, `m6-p1-survey`, Herdr `wN:p3`, session
`01a19d11-dda5-72e3-86f9-416f36341c24`.
Completed: 2026-11-02T16:46:23.849087+00:00.
Authorization: https://github.com/pixelelated/distribution/issues/689#issuecomment-6582593675
and the coordinator's matching Herdr dispatch. Full #689 body and both comments
were read. This is research input, not a brief, acceptance decision, fresh audit
verdict, or T42 execution dispatch. Planning remains with `m6-coordinator`.

## Result

T42 is canonically `patches-shipped`, 384 distribution paths / 71,387 inventory
lines. The selected path membership, every selected mode/blob, and all five
survey ledgers are identical between P1 `2174265e9c` and coordinator `2c6885a54f`.
All 384 selected paths exist at both commits. There are no changed or missing
selected paths. Both full commit IDs appear in `result.txt` under `PINS`.

All rows have language `patch`, suffix `.patch`, tier `vendor-carried`, and no
`shadowed_by` or `overlap`. This includes 380 regular files and 4 symlinks.
There are no configuration files among these 384. Reach is shipped 379 / test 5.
The inventory's provenance marker is `tier_note: fork-written`: 12 paths,
498 lines, across nine package prefixes. The generated issue's zero read / zero
fork-own metric excludes vendor-carried files and does not mean zero fork-written
patches. The `why` examples omit the fork-written Dolphin lifecycle patch.

The inventory header records source head `eb4763e3cc9bcd729830cd85f1719bbd4f28db10`,
merge base `c445081a59518f37d9776e5412dd7b14910696f7`, and generation
`2026-10-23T02:20:48Z`. These are historical survey reachability facts; no plans
were regenerated and no present runtime applicability is claimed.

## Reproduce without generating ledgers

From any checkout of this repository containing the immutable objects:

```sh
python3 /tmp/m6-t42-membership-689.iJ4iCb/reproduce.py
```

The helper executes only five inspected pure functions taken by AST from
`2174265e9c:tools/renovation-inventory`: `glob_re` (130-131), `glob_body` (134-156),
`load_areas` (159-173), `assign` (176-180), and `slice_of` (1237-1246). Its selector
compilation reproduces `load_slices` 1221-1233 using the JSON already in memory.
Only area `patches-and-configs` is classified, against all canonical selectors;
the other inventory areas are not surveyed again. Neither the generator's CLI,
`order()`, config source helper, plan runner, nor filesystem-reading loader runs.

The helper reads all source/content via `git show REV:PATH`; metadata is read via
`git ls-tree -r -z REV -- <the 384 selected paths>`. For each selected path, it
compares the mode/type/object ID across pins and counts exact Git blob bytes.
It corroborates `tier_note` with:

```sh
git diff --name-only -z --no-renames c445081a59518f37d9776e5412dd7b14910696f7 2174265e9c -- <the 384 selected paths>
git diff --name-only -z --no-renames c445081a59518f37d9776e5412dd7b14910696f7 2c6885a54f -- <the 384 selected paths>
```

Both give exactly the 12 marked paths. The helper constructs the explicit path
arguments directly from the pure membership calculation; angle brackets above
describe that argument list, not a shell command to paste. Full exact runnable
arguments/logic are in `reproduce.py`.

Issue read: `gh issue view 689 --repo pixelelated/distribution --json number,title,state,body,url,comments`.
No fetch, build, guest, config sourcing, extraction, provider review, tracker
write, product edit, or repository-ledger generation was performed.

## Counts and group definitions

The stored-blob logical line count is 71,387 at both pins; newline-byte count
(`wc -l` semantics) is 71,378. Nine blobs have no trailing newline: four symlink
target strings and five regular patch files. Exact paths are `UNTERMINATED` rows.
All per-path inventory line counts agree with the logical Git-blob count.
Selected Git blobs total 3,809,748 bytes at each pin.

Following symlinks changes the quantity: summing logical lines per selected
filesystem path after one-hop dereference is 71,477 (71,472 newlines); regular
member blobs alone have 71,383 lines. These are not an inventory drift. The
supplement was computed from `SYMLINK` rows using `git show 2174265e9c:<resolved>`
and `data.count(b"\n") + int(bool(data) and not data.endswith(b"\n"))`, replacing
each link's one logical line with its referent count. No checkout files were
dereferenced. All four referents are identical at the coordinator pin.

172 package-prefix groups, 188 immediate containing directories. A package-prefix
group is the path before `/patches/`, except project-level
`projects/ROCKNIX/patches/<package>/` groups include `<package>`. This is an explicit
grouping convention, not an inferred build graph. Every group/count is in
`PACKAGE_GROUP` rows in `result.txt`.

| Root | Paths | Lines |
| --- | --- | --- |
| packages/ | 79 | 4936 |
| projects/ROCKNIX/packages/ | 302 | 66306 |
| projects/ROCKNIX/patches/ | 3 | 145 |

13 exact `reachable_by` groups:

| Plan set | Paths | Lines |
| --- | --- | --- |
| GENERIC_X64-x86_64 | 5 | 135 |
| GENERIC_X64-x86_64, H700-aarch64, H700-arm, SM8550-aarch64 | 2 | 61 |
| GENERIC_X64-x86_64, H700-aarch64, H700-arm, SM8550-aarch64, SM8550-arm | 109 | 12353 |
| GENERIC_X64-x86_64, H700-aarch64, SM8550-aarch64 | 132 | 7238 |
| GENERIC_X64-x86_64, H700-aarch64, SM8550-aarch64, SM8550-arm | 1 | 12 |
| GENERIC_X64-x86_64, SM8550-aarch64 | 22 | 2164 |
| H700-aarch64 | 5 | 625 |
| H700-aarch64, H700-arm | 2 | 110 |
| H700-aarch64, H700-arm, SM8550-aarch64, SM8550-arm | 2 | 102 |
| H700-aarch64, SM8550-aarch64 | 30 | 903 |
| H700-arm, SM8550-arm | 2 | 33 |
| SM8550-aarch64 | 60 | 46932 |
| SM8550-aarch64, SM8550-arm | 12 | 719 |

Fork-written subset (all remain vendor-carried):

| Path | Lines |
| --- | --- |
| `packages/graphics/woff2/patches/woff2-0001-include-cstdint.patch` | 108 |
| `packages/web/webkitgtk/patches/webkitgtk-0001-DocumentLoader-include-EventLoop.patch` | 23 |
| `packages/web/webkitgtk/patches/webkitgtk-0002-WebKit-includes-WebCore-platform-graphics-for-GStreamer-GL.patch` | 20 |
| `projects/ROCKNIX/packages/compat/fex-emu/patches/0006-guest-thunks-exclude-rebased-system-headers.patch` | 23 |
| `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch` | 35 |
| `projects/ROCKNIX/packages/graphics/SDL2/patches/0010-release-display-modes-on-display-removal.patch` | 25 |
| `projects/ROCKNIX/packages/graphics/mesa/patches/001-rtasm-release-executable-heap-on-unload.patch` | 69 |
| `projects/ROCKNIX/packages/graphics/mesa/patches/002-virgl-release-empty-screen-cache.patch` | 46 |
| `projects/ROCKNIX/packages/graphics/shaderc/patches/001-fix-overwriting-dependencies.patch` | 26 |
| `projects/ROCKNIX/packages/network/zerotier-one/patches/001-client-without-nonfree-headers.patch` | 81 |
| `projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch` | 31 |
| `projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch` | 11 |

Test-only rows:

| Path | Lines |
| --- | --- |
| `packages/addons/addon-depends/system-tools-depends/lm_sensors/patches/0001-link-static.patch` | 25 |
| `packages/sysutils/pciutils/patches/0001-fix-pkgconf.patch` | 27 |
| `packages/tools/syslinux/patches/0001-fix-build-with-glibc-2.28.patch` | 33 |
| `packages/tools/syslinux/patches/0002-fix-build-with-glibc-2.36.patch` | 31 |
| `projects/ROCKNIX/packages/emulators/libretro/mupen64plus-lr/patches/AMD64/001-optimizations.patch` | 19 |

## Boundaries the brief must describe accurately

The canonical T42 selector is `{"rest": true}` in area `patches-and-configs`.
`slice_of` first returns non-rest matches, then considers rest selectors only
when no explicit selector matched. Thus T42 is not simply all non-kernel paths
of this area. It excludes the RetroArch and RAOfflineProxy patch rows explicitly
owned by their code slices, as well as the two device-owned configurations.

All 1,742 area rows / 777,541 lines partition as follows (one owner per row):

| Owner | Paths | Lines | Reach |
| --- | --- | --- | --- |
| device-generic-x64-and-kernel | 1 | 7754 | {"test": 1} |
| device-h700 | 1 | 8129 | {"shipped": 1} |
| emulators-libretro | 21 | 1670 | {"shipped": 21} |
| offline-achievements | 18 | 1703 | {"shipped": 18} |
| patches-dead | 778 | 317908 | {"unreached": 778} |
| patches-shipped | 384 | 71387 | {"shipped": 379, "test": 5} |
| patches-shipped-kernel | 107 | 40474 | {"shipped": 103, "test": 4} |
| patches-unshipped | 432 | 328516 | {"unshipped": 432} |

- **T41:** 107 / 40,474, zero intersection with T42. Its globs include all
  `projects/ROCKNIX/devices/**`, `projects/ROCKNIX/packages/linux*/**`, and
  `packages/linux*/**` for shipped/test reach, excluding the H700 and GENERIC_X64
  `linux/*.conf`. The four H700 U-Boot patches and the kernel-firmware patch
  remain T41 even though they are not kernel-source patches. D-WORKFLOW-221
  explicitly names these five. The firmware *recipe* is T11's, not T42's
  (`area: devices`, `device-generic-x64-and-kernel`). T41 brief at
  `2c6885a54f:docs/reviews/briefs/patches-shipped-kernel.md:245-260` and
  `:2153-2162` corrects the old T42 wording, although historical passages still
  contain it. H700 config is T27; GENERIC_X64 config is T11.
- **T43:** 432 / 328,516, zero path intersection with T42. Its selector accepts
  `reach: unshipped` or `n/a`; this inventory has 432 unshipped and no n/a in T43.
  A cross-slice *referent* exists: the T42 MangoHud SM8550 symlink points to a
  37-line SM8750 patch assigned to T43. This fact changes no ownership; record
  the referent as context when describing the T42 link. The inventory alone
  does not establish whether every patch applies to its currently pinned source.
- **T40:** 778 / 317,908 with unreached reach. Its 50-lead handoff is separately
  assigned to T2 by comment 6582593675 and was not re-investigated here. Leads
  are context, not added T42 inventory rows.
- **Other explicit owners:** T3 owns 21 RetroArch patches / 1,670 lines; T17
  owns 18 RAOfflineProxy patches / 1,703 lines; T11 owns the 7,754-line
  GENERIC_X64 configuration and T27 the 8,129-line H700 configuration.

The four symlinks (each is one inventory line):

| Member link | Resolved referent | Referent owner | Referent lines |
| --- | --- | --- | --- |
| `projects/ROCKNIX/packages/apps/mangohud/patches/SM8550/0002-SM8750-Battery.patch` | `projects/ROCKNIX/packages/apps/mangohud/patches/SM8750/0002-SM8750-Battery.patch` | patches-unshipped | 37 |
| `projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr/vitaquake2-rogue-lr/patches/aarch64/001-set-platform.patch` | `projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr/patches/aarch64/001-set-platform.patch` | patches-shipped | 19 |
| `projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr/vitaquake2-xatrix-lr/patches/aarch64/001-set-platform.patch` | `projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr/patches/aarch64/001-set-platform.patch` | patches-shipped | 19 |
| `projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr/vitaquake2-zaero-lr/patches/aarch64/001-set-platform.patch` | `projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr/patches/aarch64/001-set-platform.patch` | patches-shipped | 19 |

## Canonical name and concrete inputs for the coordinator

At both immutable pins, `docs/reviews/slices.json:950-965` identifies T42 as
`patches-shipped`, table, package currency, Local. `docs/reviews/order.md:703-711`
and #689's body agree. Neither selector nor order defines a `patches-rest` ID.
The informal name occurs in the coordinator's saved session at lines 26, 55,
57 and 94 (including proposed branch/brief names). The dispatch comment
explicitly denies it renaming authority. No name was changed in this research.

Concrete brief inputs: the exact 384-row residual definition and fixed pins;
71,387 literal Git-blob lines with the separate newline/dereference quantities;
380 regular patches plus four symlink rows; 12 fork-written / 498 lines including
Dolphin; three roots, 172 package-prefix groups, 188 containing directories and
13 reachable plan sets; the T41 non-kernel exceptions and T43 MangoHud referent;
the four other explicit patch-area owners above. These facts do not choose
execution policy, new criteria, audit dispositions, or dispatch details.

## Evidence identities

Sorted T42 path list, each path followed by newline (not written as a ledger):
`91e980f455611fa81bc84c8ff5548abd05437452d02038cc5595f5c1521e5f07`.

| Equal at both pins | SHA-256 |
| --- | --- |
| docs/reviews/inventory.json | d17b9cac4b2c2245b7d924036a9402b2cfd066811a7ea3fc7502a380418cb2fc |
| docs/reviews/inventory.md | 05f32dce9bb943ce31075ca5eea8e2b355baec2ef3157d84a780af2524c343e6 |
| docs/reviews/areas.json | 985f742cfd4a2138339f1ed41bd5f5f9e3755fe69b309ff3ddb10d1466fced90 |
| docs/reviews/slices.json | 49bc2745664e52f4abb9037746d003fab54e21fde74f6308a81bf20ed00f12c6 |
| docs/reviews/order.md | d5b76af6f0865d1ce5b6f8ab36fe1e5fa33478d16033833c048fae0abfde4c18 |

Research helper SHA-256: `12e1ff066aa005da502e8d817dcc141cb7b2a246dec338d27b1cec15eb8eda6e`.
Raw bounded results SHA-256: `e14b364f95d299592d44c8b4648103779d53762567a41a5eb68843e72ec5abae`.

Private scratch contains only these small scripts/results/report; no tree or source archive was exported. Repository working tree remains unchanged. Research stops here.

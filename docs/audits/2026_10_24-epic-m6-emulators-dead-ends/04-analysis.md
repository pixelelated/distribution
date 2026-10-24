# Analysis — M6.P2 T24, emulator recipes and files no shipped image builds

## Executive summary

The 86 paths of the slice are all upstream-carried, and no image we build reaches any of them.
- **The 81 under `packages/emulation/`** are LibreELEC's recipe set for Kodi's RetroPlayer. Their only build edges come from Kodi addon recipes that are unreached themselves. They return with each merge of LibreELEC master, and master already differs from our copy in 67 of the 80 recipes.
- **The five ROCKNIX recipes** are ROCKNIX's own cores that no shipped device builds. Two are built by ROCKNIX's AMD64 image only. Three are built by no ROCKNIX configuration at all.

Every row is `kept: upstream's`, with an `Already written:` line. Nothing is deleted, moved or edited. The remedy for the 81 is one proposal to ROCKNIX on #585, which the coordinator posts (PL-01). The five are said once, citing T3 (PL-02).

One finding lies outside the 86. The fork's `core-pins` writer names `boom3-lr` and `vitaquake3-lr` on every device, so every shipped image's `/usr/share/rocknix/core-pins` lists two cores the image does not hold (PL-03). It is harmless, and it is the coordinator's to route.

**Defects: none.** No `bug` is filed. `pkgcheck` passes all 85 recipes, and all 85 primary URLs answer (the repository, not the commit: P15).

## Acceptance-criteria scorecard

#671's fourteen criteria, at stage C (before the punch-list issue). "Met" names its artifact; "waits" names the stage that ticks it.

| # | Criterion (short) | State | Artifact |
| --- | --- | --- | --- |
| 1 | `00` to `05` in the folder | met at D | this folder |
| 2 | lint `PASS`, with the D-WORKFLOW-184 line | pre-issue at C; resolution waits for H | `tools/lint-audit-artifacts --phase pre-issue` |
| 3 | `review-plan.json` Local | met at C | `second-opinions/review-plan.json` |
| 4 | every punch item at a Phase 7 outcome | waits for the coordinator's dispositions | `05` § Phase 7 |
| 5 | `reviewed-at`/`fixed-at` | waits for H (`reviewed-at: 81331b499e`) | #671's body |
| 6 | `01` § Scope | met at A | `01-research-notes.md` |
| 7 | the coverage table, 86 rows | met at B | `02` § Coverage table |
| 8 | § Mechanical checks | met at B | `02` § Mechanical checks |
| 9 | Q6's reachability table, 86 rows, `Already written:` on each | met at C | § Q6 below |
| 10 | Q7's twin map (77) and Q5's weight | met at C | § Q7, § Q5 below |
| 11 | proof cells equal proof lines | met at B (17 and 17) | `02` § Proofs, `00` |
| 12 | `question:` on every item; nothing changed under `packages/` or `projects/` | met at D; the diff is re-run at H | `05`, `git diff --stat 8ebaf8daad HEAD -- packages projects` |
| 13 | the retro | waits for G | `docs/retros/2026-10-24-m6-emulators-dead-ends.md` |
| 14 | the six checkers | waits for H | #671 |

## Code Quality Assessment

Not a code read: the slice is a table, and none of the 86 runs (plan § 6c). As files:
- the 85 recipes pass `pkgcheck` under two copies;
- two carry *intertwined vars & funcs* WARN lines, which are upstream's style;
- every `PKG_URL` is on GitHub, with no retired host.

### Strengths

- **One layer, cleanly unused.** No reached file has a build edge into the 81, and no name collides with a ROCKNIX recipe. The 81 cost the tree and the merges, never a build.

### Concerns

- **The base merge carries the 81 for nothing, and keeps doing so** (F-01).
- **`core-pins` names two cores no image holds** (F-03).

### Complexity Hotspots

None: the recipes are 12 to 65 lines each.

## Cornerstone Conformance

- `upgrade-and-install.md`: every row answers *Already written*.
- `engineering-practices.md` § Before deleting a duplicate: nothing is deleted, and each row says what it exposes, which is nothing to a shipped image.
- D-UI-079 and brief § 2: no upstream-carried file is changed.
- D-WORKFLOW-164/165: the remedy is a #585 candidate, and nothing is posted outward from this lane.

## Spec Fidelity

### Aligned

Every figure of brief § 2 re-derived with no delta (`01` § Scope). The method of § 5 was run as written, with two additions, each recorded:
- the wider plan column, which covers host and init steps;
- the bare-prefix second check on the record.

### Diverged

- **`upstream/next` moved** during the fetch, to `481c9d0d75`. The (a) states are recorded at both heads, and they are equal.
- **The Q3 probe** proves the repository, not the pin (P15). The brief's Q3 is answered as "the repository answers", with the limit named.

## Missing Artifacts

None for the slice. A stronger Q3, each pin's commit through the API (85 reads), was not run: it is outside the dispatch's network reads. For the five ROCKNIX recipes, T3's Q4 already read each pin's commit (P17). For the 81, nothing builds them.

## Risk Assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| a later lane removes the 81 locally | low | the next base merge restores them; a modify/delete conflict on every LibreELEC bump | the policy on change and the disposition say no; #585 is the remedy |
| the 81 are read as ours (a pin, a patch) | medium | a wrong answer about a core's version | the twin map puts both pins side by side |
| `core-pins` read as the list of cores an image carries | low | a tool or reader overcounts by two | F-03; the one consumer looks up by the running core |
| a dead pin among the 81 goes unseen | certain, unimportant | none: nothing builds them | the probe's limit is recorded |

## Coverage Boundary

- **Covered:** all 86 paths, each by the plans, the metapackage, the build edges, the name hits, the record and, for the five, the install trees. Each row's (a) and (b) states. `pkgcheck`. The URLs' hosts and HEAD answers. The weight.
- **Not covered:**
  - the 16 patches (T40's, #687);
  - the Kodi addon recipes that call the 81 (`packages/mediacenter/`, another area's rows);
  - the `core-pins` writer beyond its one line (T3's file, accepted);
  - whether each LibreELEC pin's commit exists (P15's limit).

## Finding Verification (Phase 4.5)

Each finding is argued against, and every PASS is asked what would have made it a FAIL (brief § 1, rule 4).

- **F-01, "unreached".**
  - *Against:* a plan reaches a `libretro-*` under another name, or a device's `packages/` overrides one.
  - *Read:* the wide plan column matches any `:<kind>` suffix and any `wants:` entry, and reads 0 for all 85. No other recipe shares a name with any of the 85: the `pkgcheck` match check finds exactly one `*/<name>/package.mk` per name across `packages/` and `projects/`, so there is no override (and the inventory's `shadowed_by` is 0). The record shows no build directory.
  - *Would have failed:* `snes9x-lr` reads 3 and 6 in the plans and is built in three roots, so each read can say "reached".
  - **Stands.**
- **F-01, "master rewrites 67 of 80".**
  - *Against:* the differences are ours, not master's.
  - *Read:* the fork changed none of the 81 since the base (P2), and each diff is adds-only on master's side for the 61 (`q4b-diffshape.txt`: `del=0`).
  - *Would have failed:* the control `libretro-snes9x` is moved, and 13 files are byte-identical, so the comparison does distinguish.
  - **Stands.**
- **F-02.**
  - *Against:* `boom3-lr`'s metapackage line is a build edge.
  - *Read:* line 1768 sits inside the `core-pins` writer, which calls `get_pkg_version` and builds nothing. The build edge is `idtech-lr/package.mk:21`, under `TARGET_ARCH = x86_64`. No `.so` is in the three install trees (P10).
  - *Would have failed:* the `.info`-and-`.so` read shows both files for `snes9x`.
  - **Stands.**
- **F-03.**
  - *Against:* the rows are intended, since #21's comment says the list covers *the cores idtech-lr pulls in*.
  - *Read:* the intent covers the cores `idtech-lr` pulls in on a device, and on aarch64 it pulls in neither. The rows exist on images that hold neither `.so` (P11).
  - *Against, second:* the rows cause a failure. They do not: `cloud_capture` reads by the running core.
  - **Stands as Low, Renovation, not a `bug`.**
- **The `pkgcheck` PASS.**
  - *Would have failed:* a recipe with a global `${PKG_BUILD}` fails both copies (control rc 1).
  - *Vacuous for an unmatched name?* No: each of the 85 names matches exactly one recipe.
  - **Stands.**
- **The Q3 "alive".**
  - *Would have failed:* a nonexistent repository answers 404. A nonexistent commit does not fail, so the claim is narrowed to the repository.
  - **Narrowed, not withdrawn.**

## Renovation face

All seven questions apply (brief § 4). For a reachability table, Q6 is the spine, Q4 and Q7 hang off it, and Q1, Q2, Q3 and Q5 are counts.

### Q1 Modernize

The 85 resolved `PKG_URL`s are all on `https://github.com`: 83 archive tarballs and 2 git clones (`panda3ds-lr`, `play-lr`). No recipe is pinned to a retired host or series (P14). **Nothing to modernize** in files nothing builds; a recipe's own idiom is upstream's to keep.

### Q2 Standards and best practices

`tools/pkgcheck` gives **85 PASS** under the tree's copy and **85 PASS** under T6's widened copy (`44f64842b6`). The only output is the same 2 WARN lines in both runs: *intertwined vars & funcs*, at `libretro-beetle-pcfx/package.mk:24` and `libretro-bsnes-hd/package.mk:19` (a `PKG_LIBNAME=` after a function).

The PASS is not vacuous:
- each name matches exactly one recipe;
- the late-binding control fails both copies (P12).

The two WARNs are upstream's style on files nothing builds, so they are a line in the #585 counts (PL-01), not an item.

### Q3 Bugs

**No defect.** The HEAD probe without `-L` gave 83 × 302 and 2 × 301, with no failures, so the mirror line (`DISTRO_MIRROR`, `distributions/ROCKNIX/options:186`) was not needed.

The probe's limit, from its own controls (P15): GitHub answers 302 for an archive at a commit that does not exist, and 404 only for a repository that does not exist. So the 85 answers prove each repository answers, not each pin.
- **For the five ROCKNIX recipes**, the pin's commit was read by T3 through the API (P17), so their pins exist.
- **For the 81**, nothing builds them, so a dead pin there would cost nothing.

The brief's Q3 is informational for those, and no `bug` follows.

### Q4 Package currency

- **(a) `upstream/next`:** 81 identical and 5 differing, at both `e0f9deb899` and `481c9d0d75` (P4). The five differ by upstream's `af70bd435b`, which the base merge brings onto files the fork never touched.
- **(b) LibreELEC master,** for the 80 `packages/emulation` recipes (P5; budget 4,450 to 4,339):

| State | Recipes |
| --- | ---: |
| pin identical, byte-identical | 13 |
| pin identical, master adds a version-stamp hunk (adds only) | 61 |
| pin moved | 6 |
| absent | 0 |
| not-read | 0 |
| **Total** | **80** |

The six moved pins:

| Recipe | Ours | LibreELEC master |
| --- | --- | --- |
| `libretro-common` | `5b5a830baa6c` | `0a2b63d903ea` |
| `libretro-mame2003_plus` | `5373e38e1091` | `23c1680f562c` |
| `libretro-snes9x` | `185488cd83aa` | `fae2fea08f74` |
| `libretro-stella` | `fe8afc9455f7` | `2c3d7023e913` |
| `libretro-vecx` | `8f671cc9d737` | `dccff5402a16` |
| `rcheevos` | 9.2.0 | 12.5.0, which also adds `libretro-common` to `PKG_DEPENDS_TARGET` |

The full pins are in `q4b-compare.txt`, and in the § Q6 table's (b) cells. The mover for all 86 is the base merge (ROCKNIX's import of LibreELEC master, then ours of ROCKNIX). **No row is the fork's to bump.**

- **The five ROCKNIX recipes against their projects:** T3's Q4 at `b3cb4ec8c5` (`04-analysis.md:227, 284, 303, 307, 354`) reads `behind-project` with upstream `same` for each. ROCKNIX's to take, since no shipped image builds them.

### Q5 Efficiency

Nothing here is built, so there is no launch, boot, memory or exit cost: time to play is untouched (`not measured`, nothing builds them). The cost is the tree's and the merges':

| Set | Files | Lines | Bytes |
| --- | ---: | ---: | ---: |
| the 81 LibreELEC files | 81 | 2,258 | 86,663 |
| the 5 ROCKNIX recipes | 5 | 141 | 4,889 |

- **The slice in all:** 86 files, 2,399 lines, 91,552 bytes.
- **`packages/emulation` whole:** 97 files and 106,103 bytes, of which 16 are T40's patch files (19,440 bytes).
- **The merge cost:** LibreELEC master already differs from our copy in 67 of the 80 recipes. ROCKNIX's next import of LibreELEC master rewrites them, and our next base merge carries that diff.

### Q6 Dead ends

The reachability table: 86 rows, one per path, generated by `tools/t24-tables.py <scratch> q6` from the § 5 outputs. The script asserts 86 rows and no empty cell. The columns:
- **The reads that decided it:**
  - the plans, narrow and wide, for GENERIC_X64, H700 and SM8550;
  - the metapackage;
  - the build edges;
  - the other name hits, each classed;
  - the record over the five roots.
- **The tier.**
- **(a) and (b).**
- **The disposition.**
- **`Already written:`.**

The control beside every zero is `snes9x-lr`: 3 and 6 in the plans, 2 lines in the metapackage, and built in three roots (P6, P7, P9).

**No row's disposition is a deletion, a move or an edit.** The 81 are `kept: upstream's; #585 candidate`. The five are `kept: upstream's; no shipped device builds it`, with T3's `Already written:` cited and extended by what T3 did not say: the `core-pins` rows (F-03).

| Path | Reach | The reads that decided it | Tier | (a) `upstream/next` | (b) LibreELEC master | Disposition | Already written |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `packages/emulation/cyclone68000/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; no build edge from any file; record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-2048/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-81/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-a5200/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-atari800/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 1 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-bsnes/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-gba/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-lynx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-ngp/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-pce-fast/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-pce/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 2 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-pcfx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-psx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-saturn/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-supergrafx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-vb/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-beetle-wswan/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-bk/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-blastem/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-bluemsx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-bnes/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-bsnes-hd/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-bsnes-mercury-performance/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-bsnes/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 4 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-bsnes2014-performance/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-cannonball/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-cap32/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 1 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-common/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 2 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin moved: ours `5b5a830baa6c`, master `0a2b63d903ea` | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-dinothawr/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-dosbox-pure/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-dosbox/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 2 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-fbneo/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-fceumm/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 1 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-fmsx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-fuse/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-gambatte/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-genplus/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-gw/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-handy/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 1 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-hatari/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mame2000/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mame2003_plus/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin moved: ours `5373e38e1091`, master `23c1680f562c` | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mame2010/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mesen-s/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mesen/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 2 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mgba/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mrboom/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-mupen64plus-nx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-nestopia/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-nx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 2 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-o2em/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 1 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-opera/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-pcsx-rearmed/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-picodrive/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-pokemini/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-prboom/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 1 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-prosystem/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-quicknes/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-sameboy/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-scummvm/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-snes9x/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin moved: ours `185488cd83aa`, master `fae2fea08f74` | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-snes9x2002/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-snes9x2010/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-stella/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin moved: ours `fe8afc9455f7`, master `2c3d7023e913` | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-supafaust/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-swanstation/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; file identical | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-tgbdual/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-tyrquake/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-uae/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 3 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-uae2021/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-uae4arm/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-vbam/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-vecx/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 1 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin moved: ours `8f671cc9d737`, master `dccff5402a16` | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-vice_x128/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-vice_x64/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-vice_xplus4/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-vice_xvic/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-virtualjaguar/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/libretro-yabause/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); record: no build directory in the five roots | upstream-carried | identical | pin identical; master adds a version-stamp hunk (adds only) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/rcheevos/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; edge from 1 Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached); 11 other name hit(s), none an edge (URLs, paths, another library); record: no build directory in the five roots | upstream-carried | identical | pin moved: ours `9.2.0`, master `12.5.0` | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `packages/emulation/rcheevos/source/CMakeLists.txt` | unreached | not a recipe: copied into `rcheevos`'s source by its recipe; reached only if `rcheevos` is | upstream-carried | identical | n/a: not a recipe (rcheevos's source overlay; its recipe's row carries the read) | kept: upstream's; #585 candidate | **Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers are Kodi addon recipes, and Kodi ships in no image |
| `projects/ROCKNIX/packages/emulators/libretro/boom3-lr/package.mk` | unshipped | plans 0/0 (narrow/wide, 3 devices); metapackage 1 (the `core-pins` list, `package.mk:1768`; no `add_emu_core`); edge from `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk` under `TARGET_ARCH = x86_64` only (`idtech-lr/package.mk:20-22`); other name hits, none an edge: `cloud_capture` (`cloud_capture:885`, a core-to-package map), `package.mk` (the `core-pins` list); record: no build directory in the five roots | upstream-carried | differs (`af70bd435b`) | n/a: ROCKNIX's own recipe; its project per T3's Q4 (`behind-project`, upstream `same`) | kept: upstream's; no shipped device builds it (AMD64 builds it) | **Already written:** no fork image carries the `.so` (0 in the GENERIC_X64, H700 and SM8550 install trees); `core-info` ships its `.info` in every image's `usr/lib/libretro/` (read only), and every image's `/usr/share/rocknix/core-pins` carries a row for it (F-03), which `cloud_capture:121` reads only for the core that ran, so no save manifest names it; nothing under `/storage` or in a cloud. ROCKNIX's AMD64 image builds it; pixelelated ships no AMD64 image, so no device on the ROCKNIX to pixelelated path ran it here (T3's `04` § Q6 at `b3cb4ec8c5`) |
| `projects/ROCKNIX/packages/emulators/libretro/mame2003-lr/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; no build edge from any file; record: no build directory in the five roots | upstream-carried | differs (`af70bd435b`) | n/a: ROCKNIX's own recipe; its project per T3's Q4 (`behind-project`, upstream `same`) | kept: upstream's; no shipped device builds it | **Already written:** nothing of the core: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration), so no image carries its `.so` and no device ran it; only `core-info`'s `.info` ships, read only (T3's `04` § Q6 at `b3cb4ec8c5`) |
| `projects/ROCKNIX/packages/emulators/libretro/panda3ds-lr/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; no build edge from any file; record: no build directory in the five roots | upstream-carried | differs (`af70bd435b`) | n/a: ROCKNIX's own recipe; its project per T3's Q4 (`behind-project`, upstream `same`) | kept: upstream's; no shipped device builds it | **Already written:** nothing of the core: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration), so no image carries its `.so` and no device ran it; only `core-info`'s `.info` ships, read only (T3's `04` § Q6 at `b3cb4ec8c5`) |
| `projects/ROCKNIX/packages/emulators/libretro/play-lr/package.mk` | unreached | plans 0/0 (narrow/wide, 3 devices); metapackage 0; no build edge from any file; record: no build directory in the five roots | upstream-carried | differs (`af70bd435b`) | n/a: ROCKNIX's own recipe; its project per T3's Q4 (`behind-project`, upstream `same`) | kept: upstream's; no shipped device builds it | **Already written:** nothing of the core: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile configuration), so no image carries its `.so` and no device ran it; only `core-info`'s `.info` ships, read only (T3's `04` § Q6 at `b3cb4ec8c5`) |
| `projects/ROCKNIX/packages/emulators/libretro/vitaquake3-lr/package.mk` | unshipped | plans 0/0 (narrow/wide, 3 devices); metapackage 1 (the `core-pins` list, `package.mk:1768`; no `add_emu_core`); edge from `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk` under `TARGET_ARCH = x86_64` only (`idtech-lr/package.mk:20-22`); other name hits, none an edge: `package.mk` (the `core-pins` list); record: no build directory in the five roots | upstream-carried | differs (`af70bd435b`) | n/a: ROCKNIX's own recipe; its project per T3's Q4 (`behind-project`, upstream `same`) | kept: upstream's; no shipped device builds it (AMD64 builds it) | **Already written:** no fork image carries the `.so` (0 in the GENERIC_X64, H700 and SM8550 install trees); `core-info` ships its `.info` in every image's `usr/lib/libretro/` (read only), and every image's `/usr/share/rocknix/core-pins` carries a row for it (F-03), which `cloud_capture:121` reads only for the core that ran, so no save manifest names it; nothing under `/storage` or in a cloud. ROCKNIX's AMD64 image builds it; pixelelated ships no AMD64 image, so no device on the ROCKNIX to pixelelated path ran it here (T3's `04` § Q6 at `b3cb4ec8c5`) |

<!-- t24-tables.py q6: 86 rows -->

### Q7 Clarity and structure

**The twin map** is 77 rows, one per LibreELEC `libretro-*` core, generated by `tools/t24-tables.py <scratch> q7` from `twin.json`. That file was made by `tools/t24-twin.py` from the at-hash export: each recipe's `PKG_URL` (or `PKG_SITE`) is resolved and reduced to its repository, then compared with the 151 ROCKNIX `libretro/` recipes by name (`<core>-lr`, with `_` read as `-`) and by repository.

| Twin | Cores |
| --- | ---: |
| by name and by source | 52 |
| by name only (the two recipes fetch from different repositories: `kodi-game/*` forks for `mupen64plus-nx`, `picodrive` and `swanstation`; `libretro/dosbox-pure` against `schellingb/dosbox-pure`; `visualboyadvance-m/visualboyadvance-m` against `libretro/vbam-libretro`) | 5 |
| by source only (another name: `genesis-plus-gx-lr`, `puae-lr`/`puae2021-lr`, `vice-lr` for the four `vice_*`, `pcsx_rearmed-lr`, `beetle-supafaust-lr`, `yabasanshiro-lr`) | 10 |
| no twin | 10 |
| **Total** | **77** |

- **12 twins sit at LibreELEC's pin.** The other 55 pins differ (which is newer was not read; neither is built from the LibreELEC recipe). That is where a reader is most likely to mistake one recipe for the other.
- **`libretro-yabause` against `yabasanshiro-lr`** is a twin by repository only: `libretro/yabause` builds both, but a different core of it.
- **The 10 with no twin** are cores LibreELEC offers and ROCKNIX does not build at all: `libretro-2048`, `libretro-beetle-bsnes`, `libretro-blastem`, `libretro-bnes`, `libretro-cannonball`, `libretro-dinothawr`, `libretro-dosbox` (ROCKNIX builds `dosbox-core-lr` and `dosbox-pure-lr` from other repositories), `libretro-mame2000`, `libretro-mrboom` and `libretro-nx`. A substring search over the 151 names finds only other cores: the `bsnes*` family for `beetle-bsnes`, `dosbox-core-lr` and `dosbox-pure-lr` for `dosbox` (each from another repository, by the source comparison), and `beetle-lynx-lr`, `gearlynx-lr` and `mupen64plus-nx-lr` for `nx`; nothing for the other seven. Their removal from our tree would cost a player nothing, since no image carries them, but they are named apart for the #585 proposal.
- **`libretro-common` and `rcheevos`** are libraries, and no recipe we build depends on either: each one's only build edge is Kodi's `game.libretro` (P8). RetroArch builds its DSP filters from the `libretro-common/` folder of its own source (`retroarch/package.mk:97,124,125`). The proxy builds `raofflineproxy-rcheevos` (`raofflineproxy/package.mk:30`).
- **`cyclone68000`** is named by no other file in the tree.

| LibreELEC core | Source (`PKG_URL`) | ROCKNIX twin | How | LibreELEC pin | Twin pin(s) |
| --- | --- | --- | --- | --- | --- |
| `libretro-2048` | `libretro/libretro-2048` | no twin | - | `c90437d3c391` | - |
| `libretro-81` | `libretro/81-libretro` | `81-lr` | name and source | `fa7094910d04` | `81-lr` `fa7094910d04` (same) |
| `libretro-a5200` | `libretro/a5200` | `a5200-lr` | name and source | `e09b29dd159b` | `a5200-lr` `40c6f2f1ad4a` |
| `libretro-atari800` | `libretro/libretro-atari800` | `atari800-lr` | name and source | `7f3456f16109` | `atari800-lr` `cd721790a0aa` |
| `libretro-beetle-bsnes` | `libretro/beetle-bsnes-libretro` | no twin | - | `e2b7694d12c4` | - |
| `libretro-beetle-gba` | `libretro/beetle-gba-libretro` | `beetle-gba-lr` | name and source | `145d4884ad24` | `beetle-gba-lr` `bb9edd1d611f` |
| `libretro-beetle-lynx` | `libretro/beetle-lynx-libretro` | `beetle-lynx-lr` | name and source | `fcdefcfb3c11` | `beetle-lynx-lr` `fcdefcfb3c11` (same) |
| `libretro-beetle-ngp` | `libretro/beetle-ngp-libretro` | `beetle-ngp-lr` | name and source | `0c81ce8991a4` | `beetle-ngp-lr` `a50d5ac288a8` |
| `libretro-beetle-pce` | `libretro/beetle-pce-libretro` | `beetle-pce-lr` | name and source | `ae99235c2139` | `beetle-pce-lr` `ae99235c2139` (same) |
| `libretro-beetle-pce-fast` | `libretro/beetle-pce-fast-libretro` | `beetle-pce-fast-lr` | name and source | `9ba79648d6ec` | `beetle-pce-fast-lr` `bebe2b13a840` |
| `libretro-beetle-pcfx` | `libretro/beetle-pcfx-libretro` | `beetle-pcfx-lr` | name and source | `650c30ea2203` | `beetle-pcfx-lr` `0580dee757ad` |
| `libretro-beetle-psx` | `libretro/beetle-psx-libretro` | `beetle-psx-lr` | name and source | `42ab8d9943b6` | `beetle-psx-lr` `ef51860dbd71` |
| `libretro-beetle-saturn` | `libretro/beetle-saturn-libretro` | `beetle-saturn-lr` | name and source | `02503506566b` | `beetle-saturn-lr` `ed549bdac0e1` |
| `libretro-beetle-supergrafx` | `libretro/beetle-supergrafx-libretro` | `beetle-supergrafx-lr` | name and source | `3c6fcd3deded` | `beetle-supergrafx-lr` `3c6fcd3deded` (same) |
| `libretro-beetle-vb` | `libretro/beetle-vb-libretro` | `beetle-vb-lr` | name and source | `1275bd7bddf2` | `beetle-vb-lr` `83ed42608601` |
| `libretro-beetle-wswan` | `libretro/beetle-wswan-libretro` | `beetle-wswan-lr` | name and source | `da6d0d9acb8d` | `beetle-wswan-lr` `4b01295838ea` |
| `libretro-bk` | `libretro/bk-emulator` | `bk-lr` | name and source | `fe64da42ee46` | `bk-lr` `fe64da42ee46` (same) |
| `libretro-blastem` | `libretro/blastem` | no twin | - | `277e4a626685` | - |
| `libretro-bluemsx` | `libretro/bluemsx-libretro` | `bluemsx-lr` | name and source | `0b23b79f6b8c` | `bluemsx-lr` `e3086eb5d36d` |
| `libretro-bnes` | `libretro/bnes-libretro` | no twin | - | `8e26e89a93be` | - |
| `libretro-bsnes` | `libretro/bsnes-libretro` | `bsnes-lr` | name and source | `d62d219ac22f` | `bsnes-lr` `b102d6d5817b` |
| `libretro-bsnes-hd` | `derkoun/bsnes-hd` | `bsnes-hd-lr` | name and source | `fc26b25ea236` | `bsnes-hd-lr` `fc26b25ea236` (same) |
| `libretro-bsnes-mercury-performance` | `libretro/bsnes-mercury` | `bsnes-mercury-accuracy-lr`, `bsnes-mercury-balanced-lr`, `bsnes-mercury-performance-lr` | name and source | `ac0b6b1fe5cb` | `bsnes-mercury-accuracy-lr` `ea22363fb0c1`, `bsnes-mercury-balanced-lr` `ea22363fb0c1`, `bsnes-mercury-performance-lr` `ea22363fb0c1` |
| `libretro-bsnes2014-performance` | `libretro/bsnes2014` | `bsnes2014-accuracy-lr`, `bsnes2014-balanced-lr`, `bsnes2014-performance-lr` | name and source | `7ed320dcbebb` | `bsnes2014-accuracy-lr` `1a6b3caf1876`, `bsnes2014-balanced-lr` `1a6b3caf1876`, `bsnes2014-performance-lr` `1a6b3caf1876` |
| `libretro-cannonball` | `libretro/cannonball` | no twin | - | `65cb1f5f227d` | - |
| `libretro-cap32` | `libretro/libretro-cap32` | `cap32-lr` | name and source | `4abfb8be233b` | `cap32-lr` `4abfb8be233b` (same) |
| `libretro-dinothawr` | `libretro/dinothawr` | no twin | - | `fbf022d21ce3` | - |
| `libretro-dosbox` | `libretro/dosbox-libretro` | no twin | - | `4024bf0048c2` | - |
| `libretro-dosbox-pure` | `libretro/dosbox-pure` | `dosbox-pure-lr` | name (another source) | `42485508b705` | `dosbox-pure-lr` `7f6e8fb7385f` |
| `libretro-fbneo` | `libretro/fbneo` | `fbneo-lr` | name and source | `3eeec034f9c7` | `fbneo-lr` `f3b774987e00` |
| `libretro-fceumm` | `libretro/libretro-fceumm` | `fceumm-lr` | name and source | `3a84a6fd0ba2` | `fceumm-lr` `236ccdfc911e` |
| `libretro-fmsx` | `libretro/fmsx-libretro` | `fmsx-lr` | name and source | `3933db571485` | `fmsx-lr` `f013e213458e` |
| `libretro-fuse` | `libretro/fuse-libretro` | `fuse-lr` | name and source | `bce196fb7748` | `fuse-lr` `2a5f1d43fec7` |
| `libretro-gambatte` | `libretro/gambatte-libretro` | `gambatte-lr` | name and source | `2147d9257911` | `gambatte-lr` `d9d6cd06382d` |
| `libretro-genplus` | `libretro/genesis-plus-gx` | `genesis-plus-gx-lr` | source (another name) | `252694adb9eb` | `genesis-plus-gx-lr` `b7e79b3641eb` |
| `libretro-gw` | `libretro/gw-libretro` | `gw-lr` | name and source | `91d599b951e7` | `gw-lr` `91d599b951e7` (same) |
| `libretro-handy` | `libretro/libretro-handy` | `handy-lr` | name and source | `bc55d462f0b2` | `handy-lr` `bc55d462f0b2` (same) |
| `libretro-hatari` | `libretro/hatari` | `hatari-lr` | name and source | `6aa7c7079b31` | `hatari-lr` `24e7bd744f24` |
| `libretro-mame2000` | `libretro/mame2000-libretro` | no twin | - | `cee538f9b28f` | - |
| `libretro-mame2003_plus` | `libretro/mame2003-plus-libretro` | `mame2003-plus-lr` | name and source | `5373e38e1091` | `mame2003-plus-lr` `a045126dad33` |
| `libretro-mame2010` | `libretro/mame2010-libretro` | `mame2010-lr` | name and source | `cc63285e2109` | `mame2010-lr` `484456818393` |
| `libretro-mesen` | `libretro/mesen` | `mesen-lr` | name and source | `0102910c39ad` | `mesen-lr` `0102910c39ad` (same) |
| `libretro-mesen-s` | `libretro/mesen-s` | `mesen-s-lr` | name and source | `1d475abd174d` | `mesen-s-lr` `9e4fdeb9b336` |
| `libretro-mgba` | `libretro/mgba` | `mgba-lr` | name and source | `6dce57eef127` | `mgba-lr` `e31759b24e7a` |
| `libretro-mrboom` | `kodi-game/mrboom-libretro` | no twin | - | `0e52349c6748` | - |
| `libretro-mupen64plus-nx` | `kodi-game/mupen64plus-libretro-nx` | `mupen64plus-nx-lr` | name (another source) | `47eb46ea8dba` | `mupen64plus-nx-lr` `f275caf4b2bf` |
| `libretro-nestopia` | `libretro/nestopia` | `nestopia-lr` | name and source | `b0fd87dd07e3` | `nestopia-lr` `b08b473f961e` |
| `libretro-nx` | `libretro/nxengine-libretro` | no twin | - | `a1c45fd4d045` | - |
| `libretro-o2em` | `libretro/libretro-o2em` | `o2em-lr` | name and source | `e03d3be88f79` | `o2em-lr` `679d6fec0496` |
| `libretro-opera` | `libretro/opera-libretro` | `opera-lr` | name and source | `4c4ca6bf741c` | `opera-lr` `a501a278d057` |
| `libretro-pcsx-rearmed` | `libretro/pcsx_rearmed` | `pcsx_rearmed-lr` | source (another name) | `a97efbb0646d` | `pcsx_rearmed-lr` `da2cb8ecd17f` |
| `libretro-picodrive` | `kodi-game/picodrive` | `picodrive-lr` | name (another source) | `cb818111ef2e` | `picodrive-lr` `733c711a477a` |
| `libretro-pokemini` | `libretro/pokemini` | `pokemini-lr` | name and source | `bb009b1379ad` | `pokemini-lr` `132111b76343` |
| `libretro-prboom` | `libretro/libretro-prboom` | `prboom-lr` | name and source | `01b7411dab3b` | `prboom-lr` `861959f30fe0` |
| `libretro-prosystem` | `libretro/prosystem-libretro` | `prosystem-lr` | name and source | `3f465db9c82f` | `prosystem-lr` `8a88014287c7` |
| `libretro-quicknes` | `libretro/quicknes_core` | `quicknes-lr` | name and source | `7848e1ac22b1` | `quicknes-lr` `26bb785c9ded` |
| `libretro-sameboy` | `libretro/sameboy` | `sameboy-lr` | name and source | `06c184f0b186` | `sameboy-lr` `aa158a889a48` |
| `libretro-scummvm` | `libretro/scummvm` | `scummvm-lr` | name and source | `7310d4e9f5d1` | `scummvm-lr` `292e40993838` |
| `libretro-snes9x` | `libretro/snes9x` | `snes9x-lr` | name and source | `185488cd83aa` | `snes9x-lr` `890b5d445538` |
| `libretro-snes9x2002` | `libretro/snes9x2002` | `snes9x2002-lr` | name and source | `39e0d8c6daf4` | `snes9x2002-lr` `5bd8bd6d449b` |
| `libretro-snes9x2010` | `libretro/snes9x2010` | `snes9x2010-lr` | name and source | `d9cba8a41b34` | `snes9x2010-lr` `7db129b1ecdc` |
| `libretro-stella` | `stella-emu/stella` | `stella-lr` | name and source | `fe8afc9455f7` | `stella-lr` `c1ffb833c8b1` |
| `libretro-supafaust` | `libretro/supafaust` | `beetle-supafaust-lr` | source (another name) | `2b93c0d7dff5` | `beetle-supafaust-lr` `642d1d1b6684` |
| `libretro-swanstation` | `kodi-game/swanstation` | `swanstation-lr` | name (another source) | `fc37fce91ded` | `swanstation-lr` `7f69c199ed88` |
| `libretro-tgbdual` | `libretro/tgbdual-libretro` | `tgbdual-lr` | name and source | `12540f0b2d37` | `tgbdual-lr` `0392c9c469e6` |
| `libretro-tyrquake` | `libretro/tyrquake` | `tyrquake-lr` | name and source | `0920dec3082d` | `tyrquake-lr` `e57bb11597e8` |
| `libretro-uae` | `libretro/libretro-uae` | `puae-lr`, `puae2021-lr` | source (another name) | `20e019d4405e` | `puae-lr` `96ebfcfc2c66`, `puae2021-lr` `96ebfcfc2c66` |
| `libretro-uae2021` | `libretro/libretro-uae` | `puae-lr`, `puae2021-lr` | source (another name) | `f6502b1990a2` | `puae-lr` `96ebfcfc2c66`, `puae2021-lr` `96ebfcfc2c66` |
| `libretro-uae4arm` | `chips-fr/uae4arm-rpi` | `uae4arm-lr` | name and source | `276979efa4f8` | `uae4arm-lr` `276979efa4f8` (same) |
| `libretro-vbam` | `visualboyadvance-m/visualboyadvance-m` | `vbam-lr` | name (another source) | `c6a055ed2800` | `vbam-lr` `115defb3a318` |
| `libretro-vecx` | `libretro/libretro-vecx` | `vecx-lr` | name and source | `8f671cc9d737` | `vecx-lr` `8f671cc9d737` (same) |
| `libretro-vice_x128` | `libretro/vice-libretro` | `vice-lr` | source (another name) | `626ee6872603` | `vice-lr` `91d0d4d884ac` |
| `libretro-vice_x64` | `libretro/vice-libretro` | `vice-lr` | source (another name) | `626ee6872603` | `vice-lr` `91d0d4d884ac` |
| `libretro-vice_xplus4` | `libretro/vice-libretro` | `vice-lr` | source (another name) | `626ee6872603` | `vice-lr` `91d0d4d884ac` |
| `libretro-vice_xvic` | `libretro/vice-libretro` | `vice-lr` | source (another name) | `626ee6872603` | `vice-lr` `91d0d4d884ac` |
| `libretro-virtualjaguar` | `libretro/virtualjaguar-libretro` | `virtualjaguar-lr` | name and source | `e04f95391573` | `virtualjaguar-lr` `e6709d27bd45` |
| `libretro-yabause` | `libretro/yabause` | `yabasanshiro-lr` | source (another name); the same repository builds another core (YabaSanshiro) | `7cb15b8f9eea` | `yabasanshiro-lr` `39535a6abcad` |

<!-- t24-tables.py q7: 77 rows -->

## Instruction File Recommendations

The epic tier runs this mode. These are proposals for the coordinator: this lane edits no rule.

### Coverage Gaps (would-have-prevented)

- **A HEAD probe of a GitHub archive URL proves the repository, not the commit.** Nothing in `engineering-practices.md` § Verify the artifact, or in the plan's § 6b stage-E list, says that a probe without `-L` answers 302 for a commit that does not exist. A lane reading "302, alive" as "the pin exists" would be wrong. The check that settles a pin is the commit through the API, as T3's `q4-pins.py` did (`commits/<pin>`), or a HEAD on the redirect target. A line for the plan's stage-E list, after T7's mirror line, would close it.
- **A brief's command block is one unit.** § 5's `mkdir` sat at the top of a block whose later lines depend on it. Run line by line, the dependency was lost, and the LibreELEC loop read nothing (failing closed). Two remedies: the brief template makes each loop create what it writes, or it says "run each block whole" beside its first block.

### Codification Gaps (needs-new-rule)

None. The slice's other shapes are already rules:
- `pkgcheck`'s unmatched name (T6's F-02, #845);
- the record by name prefix (plan § 6b);
- `viewplan`'s environment (version 2's errata).

### Recommended Action Sequence

1. The coordinator posts the #585 proposal from PL-01's counts.
2. The coordinator decides F-03 (PL-03): route it to a stream on T3's file, or withdraw it as harmless.
3. If the coordinator agrees, the two coverage gaps go in as lines of the plan's stage-E list or the brief template.

## Second opinion (Phase 4.6)

**Not applicable.** The depth is Local (D-WORKFLOW-184; plan § 6c, *a dead-end table*; `slices.json` k 24, a reachability table). `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and the reason. No reviewer, no Facilitator call, no `npm install`. Phase 4.5 above was done in full, and every PASS was asked what would have made it a FAIL.

## Quality Self-Check

- **Counts against commands:**
  - every figure in this folder is a command's output, with the command in `02` § Mechanical checks;
  - the three generated tables assert their row counts (86, 86, 77);
  - the two **Total** rows sum from their rows.
- **Typed or produced:**
  - times come from `date -u` or an output file's mtime;
  - hashes and pins are copied from command output, never typed;
  - the six moved pins in § Q4 were filled from `q4b-compare.txt` by a script.
- **Claims narrowed during writing:**
  - "the futro's A1 to A6" was first written from memory of brief version 2, then read from the futro and replaced (`03`);
  - "79 Kodi recipes" became 79 edges from 78 recipes;
  - "a substring search finds none" became the list it does find;
  - "every core vendors its own `libretro-common`" became what P8 shows.
- **Not checked, said so:**
  - which of the 55 differing twin pins is newer;
  - whether each LibreELEC pin's commit exists;
  - the Kodi addon recipes and the 16 patches, which are other rows.

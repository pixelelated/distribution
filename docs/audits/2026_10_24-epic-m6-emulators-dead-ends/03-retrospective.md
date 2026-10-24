# Retrospective Audit — M6.P2 T24, emulator recipes and files no shipped image builds

Phase 3 over a reachability table. The question is not whether the 86 are well written, since none of them runs. It is whether the table's verdicts hold where the 86 meet the rest of the tree.

## 3.1 Architectural coherence

- **The 81 sit in a layer the fork does not use.** `packages/emulation/` is the generic layer of LibreELEC's recipe tree. ROCKNIX overrides the generic layer by placing its own recipe under `projects/ROCKNIX/packages/...`, under the same name (CLAUDE.md § Package override model). These 81 are not overridden that way: ROCKNIX's cores carry different names (`snes9x-lr`, not `libretro-snes9x`). So the inventory's `shadowed_by` is 0 for all 86, and the duplication is by content (the twin map, `04` § Q7). The two trees never collide, and nothing ever chooses between them.
- **Two of the five ROCKNIX recipes hang off an architecture arm.** `boom3-lr` and `vitaquake3-lr` are built only through `idtech-lr/package.mk:20-22` (`TARGET_ARCH = x86_64`). Of the shipped devices only GENERIC_X64 is x86_64, and it skips `idtech-lr` (`virtual/emulators/package.mk:111`). The inventory's `unshipped` (`buildable_by` AMD64) is that arm, read correctly.

## 3.2 Project conformance

- **`packaging-and-patches.md` and `packages/README.md`.** `tools/pkgcheck` passes all 85 recipes under the tree's copy and T6's, each name matching exactly one recipe. The two WARN lines are upstream's style on files nothing builds.
- **`upgrade-and-install.md`.** Every row carries an `Already written:` line (`04` § Q6). For 83 rows the answer is that nothing was written. For `boom3-lr` and `vitaquake3-lr` it is a read-only row in the image's `core-pins` and a `.info` file, neither of which reaches `/storage` or a cloud.
- **`engineering-practices.md` § Before deleting a duplicate.** Nothing is deleted here. The test was still asked of each row: what does the file guard, stamp or expose? None of the 81 exposes anything to a shipped image. `libretro-common` and `rcheevos` share names with libraries the image does use, but those are RetroArch's vendored copies and `raofflineproxy-rcheevos`, not these recipes.

## 3.3 Spec fidelity

The brief's figures were re-derived, and every one held. The deltas are recorded rather than corrected:
- `upstream/next` moved during the fetch, to `481c9d0d75`; the (a) states are equal at both heads.
- `find -type f` counts 471 of the export's 474 tracked paths, because 3 are symlinks.
- The latest touch among all 86 is `9cdcb3d437`; among the 81 it is the brief's `e46157185c`.

One method in the brief can't show its claim. The Q3 HEAD probe cannot see a dead commit (`02` P15). So no row says its pin exists from the probe alone.

## 3.4 Platform conformance

Not applicable as behaviour: none of the 86 runs on a device or a guest. As record, the three install trees were read for the five ROCKNIX cores' `.info` and `.so` files, and for `core-pins` (P10, P11).

## 3.5 Cross-system interaction audit

### Interaction: the base merge x the 81

- **The shared state** is the tree itself. Every merge of `upstream/next` brings what ROCKNIX took from LibreELEC master. The last such merge on our base is ROCKNIX's `c12efbd574` (2026-08-12), carrying LibreELEC's `d43d166b7a`.
- **The race.** None: the fork changed none of the 81, so a merge meets no fork edit.
- **The cost.** LibreELEC master already differs from our copy in 67 of the 80 recipes (61 version-stamp hunks, 6 pins), so ROCKNIX's next import touches them again, and our base merge after that carries the change. It is churn in a merge's diff that no image reads. The remedy is upstream's (#585), and this slice proposes none of its own (brief § 2).

### Interaction: T3's `*-lr` twins x the 77 cores

- **The shared state.** The names a core is known by: the `.info` file `core-info` ships, the `core-pins` row, and the ES system's core list. All of these come from ROCKNIX's `*-lr` recipes. None comes from a `libretro-*` recipe: the metapackage and the plans name no `libretro-*`.
- **The seam that could bite.** A reader who searches the tree for a core by its upstream name (`libretro-snes9x`) finds the unreached recipe first and may read its pin as ours. The twin map shows the two pins side by side: 12 equal and 55 different among the 67 twins. That is Q7's finding, folded into the #585 proposal, which removes the confusion with the files.

### Interaction: T40's patches x the 12 recipes

- **The shared state.** The 16 patch files under `packages/emulation/*/patches/` (19,440 bytes) apply only when their recipe builds. The inventory puts all 16 in `patches-and-configs`, `unreached`, which is T40's set (#687).
- **This slice reads none of them.** If the 81 ever leave the tree, the 16 leave with them, and T40's rows for them close by the same proposal. T40's table and this one agree on reach because both read the same inventory column.

### Interaction: the `core-pins` writer x `idtech-lr`'s architecture arm

- **The shared state** is `/usr/share/rocknix/core-pins`, written by the metapackage on every device and read by `cloud_capture:121` for the core that ran.
- **The seam.** `IDTECH_CORES` lists `boom3-lr` and `vitaquake3-lr` on every device, while `idtech-lr` builds them on `x86_64` only. So the file names two cores no shipped image holds (F-03). The reader cannot meet them, so there is no failure, only a record that overstates. That is `engineering-practices.md`'s *a name is not a behaviour* applied to a table.

## The futro's predictions, checked

The epic's futro carries a T24 kickoff addendum (`docs/futros/2026-10-24-m6-emulators-and-cores.md:489-582`), with its errata folded into brief version 2. Each item is checked against what the read showed; none is transcribed as a finding.

| Item | The addendum | What the read showed |
| --- | --- | --- |
| U-1 | which of the 77 have a ROCKNIX twin | 67 do (52 by name and source, 5 by name, 10 by source) and 10 do not (`04` § Q7) |
| U-2 | whether anything in `projects/` names one of them | 27 hits in shipped files, none a build edge; the one edge from a shipped file is `idtech-lr`'s `x86_64` arm (P8) |
| U-3 | whether the `.info` files are the five's only trace on a device | not quite: the image's `core-pins` also names `boom3-lr` and `vitaquake3-lr` (F-03, P11); still nothing under `/storage` |
| U-4 | LibreELEC master against ours, by pin | 74 identical, 6 moved, 0 absent; 61 of the 74 differ by a version-stamp hunk (P5) |
| S-1, S-2 | a lane removes the 81 or the five | nothing removed; every row `kept: upstream's` (`04` § Q6) |
| S-3 | `shadowed_by` 0 read as "nothing duplicated" | the twin map reads by content |
| S-4 | archives fetched to compare | none; the contents API and the tree |
| S-5 | a patch edited | none read or touched; T40's (#687) |
| S-6 | a stripping `sed` on the roots | match by `^<name>-[A-Za-z0-9]`, and a bare prefix as the second check (P9) |
| S-7 | `.[-1]` without `--paginate` | #671 had one comment at dispatch; the contents API returns one file per call |
| A1 to A6 | no deletion; the twin map; cite T3; the API read with its budget; the record by prefix and the `.info` trace; the acceptance's re-runs | each done as written; for A6, the four blocks sit in `02` § Mechanical checks, and the tables come from `tools/t24-tables.py` |

What the addendum did not foresee:
- the `core-pins` rows (F-03);
- the HEAD probe's blindness to a dead commit (P15);
- the 61 identical-pin files that master has still rewritten.

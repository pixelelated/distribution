# Analysis — M6.P2 T8, the image's own packages (projects/ROCKNIX)

## Executive summary

The 260 recipes the images build from `projects/ROCKNIX`, and the 225 scripts, units and configs beside them, were read at `8ebaf8daad` against their three movers. **No pin moved; nothing under `projects/` changed.**

**The movers:**

| Mover | Rows |
| --- | --- |
| the base merge | 224 rows, plus the 5 conflict rows and the 11 orphans it drops |
| `make update` | 11 rows (it has never run) |
| the fork | 4 pinned on purpose, 3 that follow a generic pin, 1 current, and **one BEHIND: `cairo` 1.18.4 against 1.18.6 (F-05)** |

**Findings:**
- **#890 (F-01):** `simple-http-server`'s x86_64 binary has no checksum, so T5's fetch would stop every GENERIC_X64 build. The coordinator filed it and fixed it in a packet ahead of T5.
- **#852 (F-02):** `virtual/image` writes its `/opt` symlink at load. This worktree's own expansion reproduced it (P12); it is this slice's stream.
- **F-03, F-04:** two dead primary URLs (`libaio`, `rocknix-abl`), covered by ROCKNIX's mirror.
- **F-09:** the base merge conflicts on 9 of this slice's paths.
- **F-11:** one of those conflicts, `glslang`'s modify/delete, would downgrade it under `spirv-tools` if resolved the obvious way.
- **F-12:** the base merge drops 11 orphans and moves five pins.
- **From the second opinion** (graded in § Second opinion): F-13 (`mangohud` downloads three sources at configure with no checksum, a Medium `bug`), F-14 (the installer reports success over unchecked steps, a Medium `bug`), F-15 (`get_archive`'s cache hit trusts its stamp, a lead for #844), F-16 (`simple-http-server`'s unquoted password, Low), F-17 (eight small shapes, Low); F-11 widened to the `spirv-headers` triple.
- **Six Low items:**
  - a freshness tool that cannot see the fork's edited recipes (F-06);
  - six short hash pins (F-07);
  - a `pkgcheck` parser false positive (F-08);
  - a unit and udev rule wired to a script no image installs (F-10).

## Acceptance-criteria scorecard

| Bucket | Criteria | Met at stage C | Open (later stage) |
| --- | ---: | ---: | ---: |
| the folder, the lint, the review plan with the seat | 3 | 1 | 2 |
| the punch list at Phase 7, the hashes and the status | 2 | 0 | 2 |
| `01` § Scope | 1 | 1 | 0 |
| `02`'s coverage, checks, sweep, #644, proofs | 5 | 5 | 0 |
| `04`'s Q4 table, orphans, conflicts, Q6 | 2 | 2 | 0 |
| no `projects/` change before a brief, no deletion, `question:` | 2 | 2 | 0 |
| #852's fix | 1 | 0 | 1 |
| the retro, the checkers | 2 | 0 | 2 |
| **Total** | 18 | 11 | 7 |

## Code Quality Assessment

### Strengths

- Every fork change carries its reason in the recipe or its commit:
  - `gamescope`'s and `mangohud`'s pinned subprojects, with a guard that stops the build when wrap and package disagree (`gamescope:55`);
  - `gstreamer`'s plugin registry;
  - `cairo`'s xcb options;
  - `NetworkManager.conf`'s hostname rule.
- 48 shell files pass `bash -n`, and none has the four shapes T30 found.
- 30 units carry no directive `systemd 259` warns about.
- 140 of 143 redirected archives were fetched again today and matched their checksum.

### Concerns

- **A deletion upstream is a pin change here** (the orphans), and nothing reads it before the merge but this table.
- **`gcc`'s hold has no reason in its recipe.**
- **The freshness tool's set leaves out the 19 recipes the fork edited**, four of which carry the fork's own pin.

### Complexity Hotspots

- `tools/installer/scripts/installer` (561 lines, fork-own by its identity edits);
- `wayland/compositor/sway`'s recipe and its three fork scripts (`111-sway-init`, `sway-ready`);
- the GStreamer trio WebKit needs.

## Risk Assessment

| Risk | Likelihood | Impact | Where |
| --- | --- | --- | --- |
| GENERIC_X64 builds stop at `simple-http-server` once T5's fetch merges | none once #890's packet merges first, as ordered | every GENERIC_X64 build | F-01, #890 |
| the base merge takes `glslang`'s deletion and downgrades it under `spirv-tools` | medium: the obvious resolution of a modify/delete | the Vulkan shader tools' build, and anything they compile | F-11 |
| the base merge changes five pins with no review (`opus`, `libfmt`, `vulkan-headers`, `mtdev`, `swaybg`) and swaps SM8550's bootloader payload to `openabl` | certain at the merge | per consumer; SM8550's boot | F-12 |
| ROCKNIX drops `libaio` or `rocknix-abl` from `sources-v2` | low | those two fail from an empty cache; the shared cache still holds both | F-03, F-04 |
| a `make update` run moves 11 hash pins with no checksum | low (never run) | 11 recipes refused by T5's fetch | #644 finding 15 |

## Coverage Boundary

**Read:**
- all 485 paths (`02`'s coverage table) at `8ebaf8daad`;
- `upstream/next`, and the base for each absent path;
- a simulated base merge;
- every recipe's effective fields on three plans;
- `make update`'s set on four plans;
- the freshness tool's 34 and the fork's four moved pins by hand;
- the 49 hash pins (44 by `compare`);
- a HEAD on 228 URLs, with every redirect hashed;
- the mirror for the failures;
- the cache's stamps for the failures;
- `ls-remote` on 10 git URLs;
- the five roots' `build/` and `.stamps/`, and the three install trees (`ls`);
- both `pkgcheck`s, `bash -n`, `systemd-analyze verify`.

**Not read:**
- the project release of the upstream-carried recipes. Their (c) says so, and their disposition names the base merge;
- the four non-GitHub hash pins' projects;
- the 82 URLs that answered 200, whose bytes were not fetched;
- the 60 recipes' patches (T42's and T43's rows);
- `shellcheck` (not on the host).

**Not run:** a build, a guest, `make update`, `update-pkg`, `update-scan`.

## Finding Verification (Phase 4.5)

Each finding attacked; what would make it wrong, and what was checked.

- **F-01** (#890). *Wrong if* GENERIC_X64 does not build it: `virtual/network:26` adds it to every image, and the M7 GENERIC_X64 root holds `build/simple-http-server-0.8.0` with its stamp. *Wrong if* T5's tip fixed it: `git show 52e6794ba7:` counts one `PKG_SHA256` line. **Confirmed**; the coordinator's.
- **F-02** (#852). *Wrong if* the lines run only at install: they are at global scope (`:109-110`, outside any function), and this worktree's sourcing created the symlink in three build directories (P12). **Confirmed.** Medium: a write outside the build's own step, on every sourcing.
- **F-03, F-04.**
  - *Wrong if* transient: each answers 404 on HEAD and on a ranged GET.
  - *Wrong if* a build fails: it does not, because the mirror serves the right bytes.
  - **Confirmed as dead primary URLs, mirror-covered.** Low. `samba`'s no-answer was transient (200 on a third read) and is withdrawn before it became a finding.
- **F-05** (`cairo`). *Wrong if* 1.18.6 is not a stable release: cairo's even-minor series is stable, and the listing at cairographics.org carries 1.18.6. **Confirmed.** Low.
- **F-06.**
  - *Wrong if* the tool lists edited recipes: `packages()` is `git diff --diff-filter=A` plus `EXTRA_PACKAGES`.
  - *Wrong if* `$(get_pkg_version rust)` is LOCAL: `var()` reads the literal, and the verdict tests `-z "$url"` after its own empty `eval`.
  - **Confirmed** as a tool lead for #657. Low.
- **F-07.** *Wrong if* the rule allows short hashes: `packaging-and-patches.md` says *the full commit hash*. All six are upstream-carried (#585). **Confirmed.** Low.
- **F-08.** *Wrong if* `moonlight` defines the function twice at run time: the two are in an `if`/`else` (`:12-45`), so one is ever defined. **Confirmed as a parser false positive** (#657's class). Low.
- **F-09.** *Wrong if* the conflicts resolve themselves: `git merge-tree` reports each. Low as a finding; the conflicts are the integration's to resolve, and the list is its pre-read.
- **F-10.**
  - *Wrong if* an image carries the script: none of the three install trees has `/usr/lib/xorg/xorg-configure`.
  - *Wrong if* nothing pulls the unit in: `97-xorg.rules:13-17` wants it for `i915`, `amdgpu`, `radeon`, `vmwgfx` and `virtio-pci`, on a PCI display of class `0x030000`.
  - The guest's `virtio-gpu-pci` is `0x038000`, so it never fires on a shipped image.
  - **Confirmed as latent.** Low, a #585 candidate.
- **F-11.** *Wrong if* the generic `glslang` is 16.6.0: `git show upstream/next:packages/graphics/vulkan/glslang/package.mk` reads 16.5.0, as does our generic copy at the hash. **Confirmed.** Medium: a silent downgrade at a merge, beneath a coupled pin.
- **F-12.** *Wrong if* a dependant names the override's path: dependants name `PKG_NAME` only. **Confirmed as a pin-change list.** Low.

**Rule 4**, asked of every PASS, each with the FAIL it was seen to give:
- (a) said *orphan* and *fork-added* on the base's split;
- the probe gave 404 and 200 on the controls;
- `pkgcheck` failed `moonlight`, `wireplumber` and `image`;
- each script grep fired on its fixture;
- `merge-tree` reported 9 conflicts;
- `systemd-analyze` reported the host's missing binaries;
- the stamps reported none missing, which the plan-by-plan check could have broken (it found #879's shape on T7's set).

## Renovation face

### Q1 Modernize

- **The 11 orphans (F-12):** upstream moved each to the generic LibreELEC recipe, or for `rocknix-abl` to `openabl` (`71d8932b33`).
- **The fork's own recipes** have no retired series or host: the GNOME, GNU and GitHub hosts all answered.
- **http:** `ffmpeg`'s `PKG_URL` is http (`http://ffmpeg.org/releases/...`), along with the rest of the http rows in `02`'s coverage table's Q1. They are upstream's (#585 with T7's twenty), and integrity rests on the checksum.
- **The units:** no retired directive in the 30.

### Q2 Standards and best practices

- **`tools/pkgcheck`:**
  - the tree's copy: 258 PASS, 2 FAIL, both its parser's (F-08, #657);
  - T6's widened copy: 257 PASS, 3 FAIL, the third #852.
- **`bash -n`:** 48 of 48.
- **`systemd-analyze verify`:** no directive warning.
- **The full-hash rule:** six short pins (F-07).
- **Late binding in the 43 sourcing overrides:** nothing is set before a load that the load then overwrites.

### Q3 Bugs

| F | What | Builds from an empty cache today | Issue |
| --- | --- | --- | --- |
| F-01 | `simple-http-server` 0.8.0 x86_64 and arm: no `PKG_SHA256` | yes, unverified; no, after T5's fetch, until #890's packet | **#890** (the coordinator's) |
| F-02 | `virtual/image` writes `${INSTALL}/opt` at load | n/a: a write, not a fetch | **#852** (this slice's stream) |
| F-03 | `libaio`'s primary URL 404 | yes, from the mirror (`716c7059...`) | filed at stage D |
| F-04 | `rocknix-abl`'s primary URL 404 | yes, from the mirror (`64034fb0...`) | filed at stage D |

The script shapes (`eval`, `echo | xargs`, a redirection in a test, `rm` then `ln`): none in the 48 (P11). Each unit's `Exec*` path is present in its plan's image except `xorg-configure`'s (F-10, Q6) and `entware`'s `/opt` path (on `/storage` by design).

### Q4 Package currency

**The table, 260 rows** (also `q4-table.md` and `q4-pins.json`):

| Disposition | Rows |
| --- | ---: |
| follows the base merge | 224 |
| `make update`'s (never run) | 11 |
| orphan, dropped by the base merge (2 of them modify/delete conflicts) | 11 |
| conflict at the base merge | 5 |
| pinned on purpose | 4 |
| follows a generic recipe's pin | 3 |
| #890 | 1 |
| current | 1 |
| **Total** | 260 |

No row reads `current` beside a `not read`. The fork-own BEHIND row is `cairo` (F-05, a Backlog bump in #839's shape); `glslang` is CURRENT and an orphan.

**The effective pin is not always the recipe's** (`device-builds.md` § After rebasing item 3). Six of the 43 sourcing overrides reset what the build fetches:
- `opus`, 1.5.2 from a xiph mirror;
- `gcc`, 15.2.0;
- `libfmt`, 9.1.0 outside SM8550, #877;
- `wavpack` and `zlib`, their own release URLs;
- `libfreeaptx`, its own checksum.

The table's pin column carries the effective value per plan; `libfmt` is the only one that differs between plans.

**The orphan table (11):**

| # | Orphan | What the fork used it for | Effective now | After the base merge | Upstream's deleting commit | Fork-own dependants |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `audio/libfreeaptx/package.mk` | its own `PKG_SHA256` over the generic URL | `0.2.2` | 0.2.2 | `6103571f67 2026-10-11` | none (by name: 0 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 2 | `audio/opus/package.mk` | 1.5.2 over the generic 1.6.1, from a xiph mirror | `1.5.2` | 1.6.1 | `075a7c303b 2026-10-17` | `multimedia/opusfile/package.mk` (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 3 | `devel/libfmt/package.mk` | 9.1.0 on every plan but SM's (#877) | `9.1.0 / 12.2.0` | 12.2.0 | `6103571f67 2026-10-11` | none (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 4 | `graphics/glslang/package.mk` | 16.6.0, the fork's own bump (`b4fc2a28cf`); spirv-tools' and spirv-headers' pins follow its `known_good.json` | `16.6.0` | 16.5.0 only if the deletion is taken; `merge-tree` leaves ours, and D-WORKFLOW-198 keeps it | `6679670966 2026-10-01` | `apps/mangohud/package.mk` (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 5 | `graphics/vulkan/vulkan-headers/package.mk` | ROCKNIX's own copy | `1.4.347` | 1.4.359 | `075a7c303b 2026-10-17` | `apps/mangohud/package.mk` (by name: 4 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 6 | `rust/cargo/package.mk` | ROCKNIX's own copy | `1.94.1` | the generic's `$(get_pkg_version rust)`, evaluated in the merged tree (not read here) | `6679670966 2026-10-01` | none (by name: 5 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 7 | `tools/miniupnpc/package.mk` | ROCKNIX's own copy | `2.3.3` | 2.3.3 | `6103571f67 2026-10-11` | `virtual/network/package.mk` (by name: 3 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 8 | `tools/rocknix-abl/package.mk` | SM8550's bootloader payload (`9aa7affee9`, #600) | `1.2` | `openabl` (`71d8932b33`) if the deletion is taken; `merge-tree` leaves ours | `71d8932b33 2026-10-14` | none (by name: 0 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 9 | `wayland/lib/tllist/package.mk` | ROCKNIX's own copy | `1.1.0` | 1.1.0 | `6679670966 2026-10-01` | none (by name: 1 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 10 | `wayland/mtdev/package.mk` | ROCKNIX's own copy | `1.1.6` | 1.1.7 | `6103571f67 2026-10-11` | none (by name: 1 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |
| 11 | `wayland/util/swaybg/package.mk` | ROCKNIX's own copy | `1.2.1` | 1.2.2 | `6103571f67 2026-10-11` | `wayland/compositor/sway/package.mk` (by name: 1 recipe(s) under `projects/ROCKNIX`, each resolving to the generic copy after the merge) |

**The conflict list (11, `git merge-tree` at `8ebaf8daad` against `upstream/next`):**

| # | Path | `merge-tree` | Disposition |
| ---: | --- | --- | --- |
| 1 | `apps/gamescope/package.mk` | auto-merges | different, keep ours: upstream bumps the pin to `6867f509...` (3.16.31), ours adds the glm/stb packages; the wraps at both commits name the same revisions, so the auto-merge builds (`:55` would stop it otherwise) |
| 2 | `graphics/cairo/package.mk` | content | conflict: upstream's is a sourcing override too; take its shape, keep ours' xcb/xlib-xcb options and the dependencies they need (`:33-36`, `:56-65`); the version line becomes the generic's |
| 3 | `graphics/glslang/package.mk` | modify/delete | conflict, left as ours in the tree by `merge-tree`: upstream deleted it (the generic is 16.5.0); ours is 16.6.0 with `spirv-tools` and `spirv-headers` on 16.6.0's `known_good.json`; D-WORKFLOW-198 keeps ours (F-11) |
| 4 | `graphics/spirv-tools/package.mk` | content | conflict: upstream made it a sourcing override; ours pins `ef96ed76...` to glslang 16.6.0 with a GCC 12 diagnostic; resolve as a triple with `glslang` and `spirv-headers` (a third modify/delete outside this slice's paths, the seat's G-27), keeping or retiring the GCC 12 workaround deliberately (F-11) |
| 5 | `lang/gcc/package.mk` | content | conflict: ours enables libatomic for `arm`, `aarch64` and `x86_64` (`:10-17`); upstream restructured it around aarch64 and dropped the 15.2.0 hold (the generic is 16.2.0); keep all three architectures and decide the hold, which its recipe gives no reason for |
| 6 | `misc/modules/sources/gamelist.xml` | auto-merges | both: the merge keeps ours' rewritten descriptions and applies upstream's removal of the AetherSX2 entry (`:171-183` here); a whole-file 'ours' would restore it, so read with `aethersx2-sa`'s own modify/delete |
| 7 | `multimedia/gstreamer/gst-plugins-base/package.mk` | content | conflict: both enable GL; ours also builds `-Dapp=enabled` with its GL dependencies and keeps the install WebKit needs (#228; `:8`, `:31-35`, `:93-108`); take upstream's GLES/EGL options and keep all three of ours |
| 8 | `multimedia/gstreamer/gstreamer/package.mk` | add/add | conflict: added on both sides; ours enables the plugin registry, the tools and the scanner WebKit needs (`:18`, `:23`, `:36`) and already removes `/usr/share` (`:49-53`), which is upstream's whole override; keep ours |
| 9 | `network/networkmanager/config/NetworkManager.conf` | content | same change: both add `hostname-mode=none` (upstream's hunk `+# network-base-setup sets the hostname`, `+hostname-mode=none`); keep the line, drop ours' longer comment |
| 10 | `tools/rocknix-abl/package.mk` | modify/delete | conflict, left as ours in the tree: upstream replaced it with `openabl` (`71d8932b33`); ours carries the v1.2 checksum fix; verify `openabl` for SM8550's bootloader (`devices/SM8550/options:66` names `rocknix-abl`) before taking the deletion |
| 11 | `wayland/compositor/sway/autostart/111-sway-init` | content | different: ours adds the virtio `Virtual` connector and the software cursor (GENERIC_X64, `:31`, `:59-63`); upstream makes the existing essway mask conditional and adds AFBC and the Duo Lite case; take upstream's hunks over the lines ours shares and keep ours' two additions |

| Recipe path | Name | Pin (effective: GENERIC_X64, H700, SM8550) | Shape | (a) upstream/next | make update | (c) the project | Disposition (the mover) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/ROCKNIX/packages/apps/commander/package.mk` | `commander` | `b3c008cac3bf` | hash | differs | - | at the default branch's HEAD | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/apps/control-gen/package.mk` | `control-gen` | `1.0` | version | identical | in the set, blocklisted | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/gamecontrollerdb/package.mk` | `gamecontrollerdb` | `42f28e22d207` | hash | identical | in the set (never run) | 30 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/gamepadtester/package.mk` | `gamepadtester` | `6ac49e67aa98` | hash | differs | - | at the default branch's HEAD | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `b06fef21d7e6`; per-plan not expanded) |
| `projects/ROCKNIX/packages/apps/gamescope-glm/package.mk` | `gamescope-glm` | `0af55ccecd98` | hash | absent: fork-added | - | PINNED (latest `119`) | pinned on purpose: follows subprojects/glm.wrap at gamescope's pinned commit |
| `projects/ROCKNIX/packages/apps/gamescope-stb/package.mk` | `gamescope-stb` | `5736b15f7ea0` | hash | absent: fork-added | - | PINNED (latest `88`) | pinned on purpose: follows subprojects/stb.wrap at gamescope's pinned commit |
| `projects/ROCKNIX/packages/apps/gamescope/package.mk` | `gamescope` | `fa0b4d334207` | hash | differs | - | 197 behind the default branch | follows the base merge (auto-merges): different, keep ours: upstream bumps the pin to `6867f509...` (3.16.31), ours adds the glm/stb packages; the wraps at both commits name the same revisions, so the auto-merge builds (`:55` would stop it otherwise) |
| `projects/ROCKNIX/packages/apps/jstest-sdl/package.mk` | `jstest-sdl` | `f4fdf6daae68` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/list-guid/package.mk` | `list-guid` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/m8c/package.mk` | `m8c` | `v1.7.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/mako-notify/package.mk` | `mako-notify` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/mako-osd/package.mk` | `mako-osd` | `b131bc143f6b` | hash | identical | - | 23 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/mangohud-vulkan-headers/package.mk` | `mangohud-vulkan-headers` | `1.4.346` | version | absent: fork-added | - | PINNED (latest `1.4.366`) | pinned on purpose: follows subprojects/vulkan-headers.wrap at mangohud's pinned commit |
| `projects/ROCKNIX/packages/apps/mangohud-vulkan-utility-libraries/package.mk` | `mangohud-vulkan-utility-libraries` | `1.4.346` | version | absent: fork-added | - | PINNED (latest `1.4.366`) | pinned on purpose: follows subprojects/vulkan-utility-libraries.wrap at mangohud's pinned commit |
| `projects/ROCKNIX/packages/apps/mangohud/package.mk` | `mangohud` | `992103e4fb74` | hash | differs | - | 216 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/apps/moonlight/package.mk` | `moonlight` | `a6bf7154a743` | hash | differs | in the set (never run) | 16 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/oga_controls/package.mk` | `oga_controls` | `1604ee24150c` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/portmaster/package.mk` | `portmaster` | `2026.09.13-0343` | version | differs | in the set, blocklisted | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `2026.06.23-0`; per-plan not expanded) |
| `projects/ROCKNIX/packages/apps/qterminal/layer-shell-qt/package.mk` | `layer-shell-qt` | `v6.4.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/qterminal/lxqt-build-tools/package.mk` | `lxqt-build-tools` | `2.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/qterminal/package.mk` | `qterminal` | `2.2.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/qterminal/qtermwidget/package.mk` | `qtermwidget` | `2.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/rocknix-hotkey/package.mk` | `rocknix-hotkey` | `cc3a863199a7` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/rocknix-screenshot/package.mk` | `rocknix-screenshot` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/rocknix-touchscreen-keyboard/package.mk` | `rocknix-touchscreen-keyboard` | `v0.17` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/sdl2notify/package.mk` | `sdl2notify` | `1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/apps/sdl2text/package.mk` | `sdl2text` | `v1.0` | version | identical | in the set (never run) | not read: follows the base merge | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/sdljoytest/package.mk` | `sdljoytest` | `811d9875e0c1` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/apps/sdltouchtest/package.mk` | `sdltouchtest` | `b62dae0d6233` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/audio/SDL2_mixer/package.mk` | `SDL2_mixer` | `2.8.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/alsa-lib/package.mk` | `alsa-lib` | `1.2.14` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/audio/alsa-ucm-conf/package.mk` | `alsa-ucm-conf` | `1.2.13` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/audio/alsa-utils/package.mk` | `alsa-utils` | `1.2.14` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/audio/espeak/package.mk` | `espeak` | `1.48.04-source` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/fluidsynth/package.mk` | `fluidsynth` | `2.5.7` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/ldacBT/package.mk` | `ldacBT` | `2.0.2.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libao/package.mk` | `libao` | `1.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libfreeaptx/package.mk` | `libfreeaptx` | `0.2.2` | sourcing override | absent: orphan | - | INHERITED | orphan: dropped by the base merge; the fork used it for its own `PKG_SHA256` over the generic URL; after it, 0.2.2; dependants resolve by name |
| `projects/ROCKNIX/packages/audio/libogg/package.mk` | `libogg` | `1.3.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libsndfile/package.mk` | `libsndfile` | `e486f20` | hash (short) | identical | - | 50 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libvorbis/package.mk` | `libvorbis` | `1.3.7` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/libxmp/package.mk` | `libxmp` | `8201d26cf933` | hash | identical | - | 425 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/opus/package.mk` | `opus` | `1.5.2` | sourcing override (sets its own pin) | absent: orphan | - | UNKNOWN: no resolver for ftp.osuosl.org, or it did not answer | orphan: dropped by the base merge; the fork used it for 1.5.2 over the generic 1.6.1, from a xiph mirror; after it, 1.6.1; dependants resolve by name |
| `projects/ROCKNIX/packages/audio/pipewire/package.mk` | `pipewire` | `1.2.6` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `1.6.8`; per-plan not expanded) |
| `projects/ROCKNIX/packages/audio/pulseaudio/package.mk` | `pulseaudio` | `17.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/sndio/package.mk` | `sndio` | `1.10.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/wavpack/package.mk` | `wavpack` | `5.9.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/audio/wireplumber/package.mk` | `wireplumber` | `0.5.7` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `0.5.15`; per-plan not expanded) |
| `projects/ROCKNIX/packages/compat/box64/package.mk` | `box64` | `2f130fab1d6e` | hash | identical | in the set (never run) | 429 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/compat/box86/package.mk` | `box86` | `39d3ed203323` | hash | differs | in the set (never run) | 7 behind the default branch | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/compat/fex-emu/package.mk` | `fex-emu` | `e869aa644a16` | hash | differs | - | 522 behind the default branch | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `14c92681f4d6`; per-plan not expanded) |
| `projects/ROCKNIX/packages/compat/lib32/package.mk` | `lib32` | `1.0` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/compat/wine/package.mk` | `wine` | `11.0` | version | identical | in the set (never run) | not read: follows the base merge | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/compress/cabextract/package.mk` | `cabextract` | `1.11` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/gzip/package.mk` | `gzip` | `1.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/libarchive/package.mk` | `libarchive` | `3.8.9` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/libzip/package.mk` | `libzip` | `1.11.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/compress/p7zip/package.mk` | `p7zip` | `16.02` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/xz/package.mk` | `xz` | `5.8.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/compress/zip/package.mk` | `zip` | `3.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/compress/zlib/package.mk` | `zlib` | `1.3.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/debug/apitrace/package.mk` | `apitrace` | `45a005875d34` | hash | identical | - | 84 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_gfx/package.mk` | `SDL2_gfx` | `29927b3` | hash (short) | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_image/package.mk` | `SDL2_image` | `2.8.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_net/package.mk` | `SDL2_net` | `2.2.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL2_ttf/package.mk` | `SDL2_ttf` | `2.20.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/SDL3_ttf/package.mk` | `SDL3_ttf` | `3.2.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/boost/package.mk` | `boost` | `1.86.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/ccache/package.mk` | `ccache` | `4.13.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/cmake/package.mk` | `cmake` | `4.4.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/ecm/package.mk` | `ecm` | `v6.16.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/glib/package.mk` | `glib` | `2.89.3` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/glibc/package.mk` | `glibc` | `2.41` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `2.44`; per-plan not expanded) |
| `projects/ROCKNIX/packages/devel/json-glib/package.mk` | `json-glib` | `1.10.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/libaio/package.mk` | `libaio` | `0.3.113` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) (F-03) |
| `projects/ROCKNIX/packages/devel/libclc/package.mk` | `libclc` | `22.1.8` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libcom-err/package.mk` | `libcom-err` | `1.47.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libdatrie/package.mk` | `libdatrie` | `0.2.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libfmt/package.mk` | `libfmt` | GENERIC_X64 `9.1.0`; H700 `9.1.0`; SM8550 `12.2.0` | sourcing override (sets its own pin) | absent: orphan | - | INHERITED | orphan: dropped by the base merge; the fork used it for 9.1.0 on every plan but SM's (#877); after it, 12.2.0; dependants resolve by name |
| `projects/ROCKNIX/packages/devel/libpthread-stubs/package.mk` | `libpthread-stubs` | `0.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libserialport/package.mk` | `libserialport` | `21b3dfe5f68c` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/libthai/package.mk` | `libthai` | `0.1.29` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/make/package.mk` | `make` | `4.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/ncurses/package.mk` | `ncurses` | `6.5` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/patchelf/package.mk` | `patchelf` | `0.18.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/rapidjson/package.mk` | `rapidjson` | `1.1.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/devel/readline/package.mk` | `readline` | `8.3` | sourcing override | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/shared-mime-info/package.mk` | `shared-mime-info` | `2.4` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/swig/package.mk` | `swig` | `4.1.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/devel/xa/package.mk` | `xa` | `2.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/fonts/dejavu/package.mk` | `dejavu` | `2.37` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/fonts/noto-sans-cjk/package.mk` | `noto-sans-cjk` | `2.004` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/fonts/spleen-font/package.mk` | `spleen-font` | `2.0.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/SDL2/package.mk` | `SDL2` | `2.32.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/SDL3/package.mk` | `SDL3` | `3.4.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/armsx2-turnip/package.mk` | `armsx2-turnip` | `axfl1-011` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/cairo/package.mk` | `cairo` | `1.18.4` | version | differs | - | BEHIND (latest `1.18.6`, cairographics.org's listing) | conflict at the base merge (content): conflict: upstream's is a sourcing override too; take its shape, keep ours' xcb/xlib-xcb options and the dependencies they need (`:33-36`, `:56-65`); the version line becomes the generic's; and fork's: Backlog bump proposed (#839's shape), 1.18.4 -> 1.18.6 (F-05) |
| `projects/ROCKNIX/packages/graphics/capsimg/package.mk` | `capsimg` | `ed4cb0912fb1` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/fbgrab/package.mk` | `fbgrab` | `5c2481d2b67b` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/gdk-pixbuf/package.mk` | `gdk-pixbuf` | `2.42.10` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/glew/package.mk` | `glew` | `2.2.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/glfw/package.mk` | `glfw` | `e2c9264` | hash (short) | identical | - | 1055 behind the default branch, 627 not on it | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/glslang/package.mk` | `glslang` | `16.6.0` | version | absent: orphan | - | CURRENT (latest `16.6.0`) | orphan, a modify/delete conflict at the base merge: dropped by the base merge; the fork used it for 16.6.0, the fork's own bump (`b4fc2a28cf`); spirv-tools' and spirv-headers' pins follow its `known_good.json`; after it, 16.5.0 only if the deletion is taken; `merge-tree` leaves ours, and D-WORKFLOW-198 keeps it; dependants resolve by name (F-11) |
| `projects/ROCKNIX/packages/graphics/grim/package.mk` | `grim` | `1.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/gtk2/package.mk` | `gtk2` | `2.24.33` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/gtk3/package.mk` | `gtk3` | `3.24.52` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/harfbuzz-icu/package.mk` | `harfbuzz-icu` | `14.3.0` | sourcing override | absent: fork-added | - | INHERITED | follows the generic recipe's pin (T7's row); the override adds options |
| `projects/ROCKNIX/packages/graphics/imagemagick/package.mk` | `imagemagick` | `7.1.2-29` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libdrm/package.mk` | `libdrm` | `2.4.133` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libepoxy/package.mk` | `libepoxy` | `1.5.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libglvnd/package.mk` | `libglvnd` | `1.7.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libjpeg-turbo/package.mk` | `libjpeg-turbo` | `3.2.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libpng/package.mk` | `libpng` | `1.6.40` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/librashader/package.mk` | `librashader` | `76462c030b75` | hash | identical | - | 85 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/libwebp/package.mk` | `libwebp` | `1.6.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/lsfg-vk/package.mk` | `lsfg-vk` | `8b0da2661c6f` | hash | identical | - | unknown: compare found no common ancestor | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/mesa-demos/package.mk` | `mesa-demos` | `9.0.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/mesa/package.mk` | `mesa` | `26.2.2` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `26.2.4`; per-plan not expanded) |
| `projects/ROCKNIX/packages/graphics/plutosvg/package.mk` | `plutosvg` | `0.0.7` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/plutovg/package.mk` | `plutovg` | `1.3.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/qt6/package.mk` | `qt6` | `6.10.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/renderdoc/package.mk` | `renderdoc` | `v1.44` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/shaderc/package.mk` | `shaderc` | `2025.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/spirv-llvm-translator/package.mk` | `spirv-llvm-translator` | `22.1.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/spirv-tools/package.mk` | `spirv-tools` | `ef96ed763b43` | hash | differs | - | 73 behind the default branch | conflict at the base merge (content): conflict: upstream made it a sourcing override; ours pins `ef96ed76...` to glslang 16.6.0 with a GCC 12 diagnostic; resolve as a triple with `glslang` and `spirv-headers` (a third modify/delete outside this slice's paths, the seat's G-27), keeping or retiring the GCC 12 workaround deliberately (F-11) |
| `projects/ROCKNIX/packages/graphics/tiff/package.mk` | `tiff` | `4.7.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/graphics/vulkan/vulkan-headers/package.mk` | `vulkan-headers` | `1.4.347` | version | absent: orphan | - | BEHIND (latest `1.4.366`) | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.4.359; dependants resolve by name |
| `projects/ROCKNIX/packages/graphics/vulkan/vulkan-loader/package.mk` | `vulkan-loader` | `1.4.347` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/vulkan/vulkan-tools/package.mk` | `vulkan-tools` | `1.4.347` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/graphics/waffle/package.mk` | `waffle` | `5f1f48287e80` | hash | differs | - | unknown: gitlab.freedesktop.org is not GitHub | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `3b20e4d7bccc`; per-plan not expanded) |
| `projects/ROCKNIX/packages/graphics/wxwidgets/package.mk` | `wxwidgets` | `db1005db3dea` | hash | differs | - | 1631 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/lang/gcc/package.mk` | `gcc` | `15.2.0` | sourcing override (sets its own pin) | differs | - | not read: the tool lists only recipes added since the base | conflict at the base merge (content): conflict: ours enables libatomic for `arm`, `aarch64` and `x86_64` (`:10-17`); upstream restructured it around aarch64 and dropped the 15.2.0 hold (the generic is 16.2.0); keep all three architectures and decide the hold, which its recipe gives no reason for |
| `projects/ROCKNIX/packages/lang/go/package.mk` | `go` | `1.21.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/lang/llvm/package.mk` | `llvm` | `22.1.8` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/lang/lua54/package.mk` | `lua54` | `5.4.6` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/lang/luajit/package.mk` | `luajit` | `1edc3e52b67e` | hash | identical | - | 31 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/lang/nasm/package.mk` | `nasm` | `2.16.01` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/misc/modules/package.mk` | `modules` | `1.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/ffmpeg/package.mk` | `ffmpeg` | `7.1.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `9.0`; per-plan not expanded) |
| `projects/ROCKNIX/packages/multimedia/gmu/package.mk` | `gmu` | `3aed18be8a50` | hash | identical | - | 31 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-libav/package.mk` | `gst-libav` | `1.29.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-bad/package.mk` | `gst-plugins-bad` | `1.29.2` | sourcing override | absent: fork-added | - | INHERITED | follows the generic recipe's pin (T7's row); the override adds options |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-base/package.mk` | `gst-plugins-base` | `1.29.2` | sourcing override | differs | - | not read: the tool lists only recipes added since the base | conflict at the base merge (content): conflict: both enable GL; ours also builds `-Dapp=enabled` with its GL dependencies and keeps the install WebKit needs (#228; `:8`, `:31-35`, `:93-108`); take upstream's GLES/EGL options and keep all three of ours |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gst-plugins-good/package.mk` | `gst-plugins-good` | `1.29.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/gstreamer/gstreamer/package.mk` | `gstreamer` | `1.29.2` | sourcing override | differs | - | not read: the tool lists only recipes added since the base | conflict at the base merge (add/add): conflict: added on both sides; ours enables the plugin registry, the tools and the scanner WebKit needs (`:18`, `:23`, `:36`) and already removes `/usr/share` (`:49-53`), which is upstream's whole override; keep ours |
| `projects/ROCKNIX/packages/multimedia/libdvbpsi/package.mk` | `libdvbpsi` | `1.3.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/libplacebo/package.mk` | `libplacebo` | `05ac2cca6571` | hash | differs | - | unknown: code.videolan.org is not GitHub | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/libvpx/package.mk` | `libvpx` | `df655cf4fb6c` | hash | differs | - | 794 behind the default branch | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `1.16.0`; per-plan not expanded) |
| `projects/ROCKNIX/packages/multimedia/mpv/package.mk` | `mpv` | `41f6a6450684` | hash | differs | - | 1293 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/opusfile/package.mk` | `opusfile` | `9d718345ce03` | hash | differs | - | 19 behind the default branch | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/multimedia/vlc/package.mk` | `vlc` | `3.0.23` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/multimedia/x264/package.mk` | `x264` | `0480cb05fa18` | sourcing override | identical | - | unknown: code.videolan.org is not GitHub | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/avahi/package.mk` | `avahi` | `0.8` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/bluez/package.mk` | `bluez` | `5.83` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/enet/package.mk` | `enet` | `v1.3.18` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/fping/package.mk` | `fping` | `5.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/iwd/package.mk` | `iwd` | `3.12` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/libndp/package.mk` | `libndp` | `1.9` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/libpcap/package.mk` | `libpcap` | `1.10.4` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/libslirp/package.mk` | `libslirp` | `4.7.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/networkmanager/package.mk` | `networkmanager` | `1.51.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/nfs-utils/package.mk` | `nfs-utils` | `2.6.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/openssh/package.mk` | `openssh` | `9.8p1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/samba/package.mk` | `samba` | `4.21.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `4.24.5`; per-plan not expanded) |
| `projects/ROCKNIX/packages/network/simple-http-server/package.mk` | `simple-http-server` | `0.8.0` | version | identical | - | not read: follows the base merge | #890: filed and fixed in a packet ahead of T5 (`fix-tree`); follows the base merge |
| `projects/ROCKNIX/packages/network/sixaxis/package.mk` | `sixaxis` | `f53b0ca28c35` | hash | identical | in the set (never run) | at the default branch's HEAD | make update's: moves to its branch head if run (never run); otherwise follows the base merge |
| `projects/ROCKNIX/packages/network/speedtest-cli/package.mk` | `speedtest-cli` | `v2.1.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/syncthing/package.mk` | `syncthing` | `2.0.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/network/tailscale/package.mk` | `tailscale` | `1.98.8` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/network/zerotier-one/package.mk` | `zerotier-one` | `1.16.0` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/print/poppler/package.mk` | `poppler` | `23.05.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/python/devel/pyxel/package.mk` | `pyxel` | `2.9.9` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/rust/cargo/package.mk` | `cargo` | `1.94.1` | version | absent: orphan | - | LOCAL | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, the generic's `$(get_pkg_version rust)`, evaluated in the merged tree (not read here); dependants resolve by name |
| `projects/ROCKNIX/packages/rust/rust/package.mk` | `rust` | `1.94.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/security/gnutls/package.mk` | `gnutls` | `3.8.13` | sourcing override | absent: fork-added | - | INHERITED | follows the generic recipe's pin (T7's row); the override adds options |
| `projects/ROCKNIX/packages/security/libgpg-error/package.mk` | `libgpg-error` | `1.61` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/security/openssl/package.mk` | `openssl` | `3.6.3` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/bdf2psf/package.mk` | `bdf2psf` | `1.249` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/expat/package.mk` | `expat` | `2.8.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/icu/package.mk` | `icu` | `74.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/textproc/inih/package.mk` | `inih` | `r62` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/jsoncpp/package.mk` | `jsoncpp` | `1.9.8` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/libiconv/package.mk` | `libiconv` | `1.19` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/textproc/textviewer/package.mk` | `textviewer` | `fcbda2d1708e` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/at-spi2-atk/package.mk` | `at-spi2-atk` | `2.38.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/at-spi2-core/package.mk` | `at-spi2-core` | `2.45.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/tools/atf/package.mk` | `atf` | GENERIC_X64 `2.10.0`; H700 `2.12.0`; SM8550 `2.10.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `2.12.0`; per-plan not expanded) |
| `projects/ROCKNIX/packages/tools/batteryplus/package.mk` | `batteryplus` | `1c31e89ec182` | hash | differs | - | 2 behind the default branch | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `31a3b629bc22`; per-plan not expanded) |
| `projects/ROCKNIX/packages/tools/bin2c/package.mk` | `bin2c` | `1.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/coreutils/package.mk` | `coreutils` | `9.4` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/dialog/package.mk` | `dialog` | `1.3-20231002` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/empty/package.mk` | `empty` | `0.6.23c` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/entware/package.mk` | `entware` | - | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/freeimage/package.mk` | `freeimage` | `3180` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk` | `gamepadcalibration` | `2077e7af7e9a` | hash | differs | - | 1 behind the default branch, 8 not on it | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/tools/inputplumber/package.mk` | `inputplumber` | `v0.79.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `0.82.0`; per-plan not expanded) |
| `projects/ROCKNIX/packages/tools/installer/package.mk` | `installer` | `1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/joyutils/package.mk` | `joyutils` | `b6703ebf04c8` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/miniupnpc/package.mk` | `miniupnpc` | `2.3.3` | version | absent: orphan | - | UNKNOWN: no resolver for miniupnp.free.fr, or it did not answer | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 2.3.3; dependants resolve by name |
| `projects/ROCKNIX/packages/tools/mkbootimg/package.mk` | `mkbootimg` | `d2bb0af5ba6d` | hash | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/procps-ng/package.mk` | `procps-ng` | `4.0.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/pyudev/package.mk` | `pyudev` | `5e00141` | hash (short) | identical | - | 133 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/qcom-abl/package.mk` | `qcom-abl` | `1.0` | local payload (no `PKG_URL`) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/rocknix-abl/package.mk` | `rocknix-abl` | `1.2` | version | absent: orphan | - | UNKNOWN: no resolver for github.com, or it did not answer | orphan, a modify/delete conflict at the base merge: dropped by the base merge; the fork used it for SM8550's bootloader payload (`9aa7affee9`, #600); after it, `openabl` (`71d8932b33`) if the deletion is taken; `merge-tree` leaves ours; dependants resolve by name (F-04) |
| `projects/ROCKNIX/packages/tools/rocknix-splash/package.mk` | `rocknix-splash` | `8c71126ceef7` | hash | differs | - | at the default branch's HEAD | current |
| `projects/ROCKNIX/packages/tools/six/package.mk` | `six` | `02c3bca` | hash (short) | identical | - | 21 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/socat/package.mk` | `socat` | `1.7.4.4` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `1.8.1.3`; per-plan not expanded) |
| `projects/ROCKNIX/packages/tools/sound/libvorbisidec/package.mk` | `libvorbisidec` | `a76e41f6ece9` | hash | identical | - | 19 behind the default branch | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/sound/mpg123/package.mk` | `mpg123` | `1.33.7` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/tools/sound/soundfont-generaluser/package.mk` | `soundfont-generaluser` | `8fe2798` | hash (short) | identical | - | at the default branch's HEAD | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/arm/package.mk` | `arm` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/debug/package.mk` | `debug` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/es-themes/package.mk` | `es-themes` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/gamesupport/package.mk` | `gamesupport` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/image/package.mk` | `image` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) (F-02, #852) |
| `projects/ROCKNIX/packages/virtual/initramfs/package.mk` | `initramfs` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/libc/package.mk` | `libc` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/linux-drivers/package.mk` | `linux-drivers` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/linux-firmware/package.mk` | `linux-firmware` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/network/package.mk` | `network` | - | virtual (no source) | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/virtual/swaywm-env/package.mk` | `swaywm-env` | - | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/virtual/synctools/package.mk` | `synctools` | `0.0invalid` | virtual (no source) | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/compositor/sway/package.mk` | `sway` | `1.11` | version | differs | - | not read: the tool lists only recipes added since the base | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `1.9`; per-plan not expanded) |
| `projects/ROCKNIX/packages/wayland/lib/fcft/package.mk` | `fcft` | `3.1.9` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/wayland/lib/libdecor/package.mk` | `libdecor` | `0.2.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/lib/seatd/package.mk` | `seatd` | `0.9.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/lib/tllist/package.mk` | `tllist` | `1.1.0` | version | absent: orphan | - | CURRENT (latest `1.1.0`) | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.1.0; dependants resolve by name |
| `projects/ROCKNIX/packages/wayland/lib/wlroots/package.mk` | `wlroots` | `0.19.3` | version | differs | - | not read: follows the base merge | follows the base merge: upstream's recipe changed (its first `PKG_VERSION` literal `132e31cfe19f`; per-plan not expanded) |
| `projects/ROCKNIX/packages/wayland/libinput/package.mk` | `libinput` | `1.26.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/libxkbcommon/package.mk` | `libxkbcommon` | `1.8.0` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/mtdev/package.mk` | `mtdev` | `1.1.6` | version | absent: orphan | - | UNKNOWN: no resolver for sources.buildroot.net, or it did not answer | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.1.7; dependants resolve by name |
| `projects/ROCKNIX/packages/wayland/util/bemenu/package.mk` | `bemenu` | `0.6.15` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/util/foot/package.mk` | `foot` | `1.19.0` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/wayland/util/swaybg/package.mk` | `swaybg` | `1.2.1` | version | absent: orphan | - | BEHIND (latest `1.2.2`) | orphan: dropped by the base merge; the fork used it for ROCKNIX's own copy; after it, 1.2.2; dependants resolve by name |
| `projects/ROCKNIX/packages/wayland/util/swayimg/package.mk` | `swayimg` | `v2.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/wayland/util/wlr-randr/package.mk` | `wlr-randr` | `0.4.1` | version | differs | - | not read: follows the base merge | follows the base merge: upstream changed the recipe, not its top-level pin |
| `projects/ROCKNIX/packages/web/curl/package.mk` | `curl` | `8.21.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/app/xterm/package.mk` | `xterm` | `410` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libICE/package.mk` | `libICE` | `1.1.2` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libSM/package.mk` | `libSM` | `1.2.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXau/package.mk` | `libXau` | `1.0.12` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXaw/package.mk` | `libXaw` | `1.0.16` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXcursor/package.mk` | `libXcursor` | `1.2.3` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXdmcp/package.mk` | `libXdmcp` | `1.1.5` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXft/package.mk` | `libXft` | `2.3.9` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXinerama/package.mk` | `libXinerama` | `1.1.6` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXmu/package.mk` | `libXmu` | `1.3.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXpm/package.mk` | `libXpm` | `3.5.19` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXres/package.mk` | `libXres` | `1.2.3` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXt/package.mk` | `libXt` | `1.3.1` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libXxf86vm/package.mk` | `libXxf86vm` | `1.1.7` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libfontenc/package.mk` | `libfontenc` | `1.1.9` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libxcb-cursor/package.mk` | `libxcb-cursor` | `7b0fa99aa130` | hash | identical | - | unknown: gitlab.freedesktop.org is not GitHub | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/lib/libxkbfile/package.mk` | `libxkbfile` | `1.2.0` | sourcing override | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-image/package.mk` | `xcb-util-image` | `0.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-keysyms/package.mk` | `xcb-util-keysyms` | `0.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-renderutil/package.mk` | `xcb-util-renderutil` | `0.3.10` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util-wm/package.mk` | `xcb-util-wm` | `0.4.2` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/util/xcb-util/package.mk` | `xcb-util` | `0.4.1` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |
| `projects/ROCKNIX/packages/x11/xserver/xwayland/package.mk` | `xwayland` | `24.1.13` | version | identical | - | not read: follows the base merge | follows the base merge (identical to `upstream/next`) |

### Q5 Efficiency

**Not measured:** no build runs. Read:
- **`gcc`'s hold** at 15.2.0 keeps the cross toolchain a major behind the generic 16.2.0; its recipe gives no reason.
- **`box86` and `lib32`** carry the 32-bit chain on ARM (the fork renamed their compatibility roots, `43d0bc3bf4`).
- **The GStreamer trio** installs what WebKit loads.

**On the boot path:**
- **`sway-ready`** (fork-added, `c6afa31db1`) polls for a responsive compositor every 0.1 s with a 1 s bound per round trip, and gives up at 15 s.
- **`111-sway-init`'s added lines** are two greps and an echo.

Neither is measured here; `tools/time-to-play` would show a change.

### Q6 Dead ends

**The 13 unbuilt names:**
- the 12 virtual packages, by construction (no source);
- **`qcom-abl`**, built by SM8550's plan alone: `viewplan` lists it there and nowhere else, it is stamped in the SM8550 roots, and its `PKG_URL` is empty.

**Read by stamps,** every plan's reached recipes are built in that plan's root (P14): no plan reading is contradicted by a `PKG_ARCH`.

**The units:**
- **`xorg-configure@.service` and `97-xorg.rules`** (F-10) are wired to a script no image installs, and are reached only on a PCI VGA-class display, which no shipped image has.
- **`batteryplus` and `inputplumber`** are each device-scoped and present where they ship.

**The orphans' dependants** are in the orphan table: none breaks by name.

### Q7 Clarity and structure

**The fork's 35 changes, each with its reason and what the base merge does to it:**

| # | Fork change | Since the base | Reason (the newest commit) | At the base merge |
| ---: | --- | --- | --- | --- |
| 1 | `apps/gamescope-glm/package.mk` | added | `5b5005879e` gamescope: glm and stb come from pinned sources, never from a clone | stays: no upstream copy |
| 2 | `apps/gamescope-stb/package.mk` | added | `5b5005879e` gamescope: glm and stb come from pinned sources, never from a clone | stays: no upstream copy |
| 3 | `apps/gamescope/package.mk` | edited | `5b5005879e` gamescope: glm and stb come from pinned sources, never from a clone | auto-merges (both changed) |
| 4 | `apps/m8c/config/GENERIC_X64/config.ini` | added | `cbdb91a517` GENERIC_X64 - add per-device emulator/app configs | stays: no upstream copy |
| 5 | `apps/mangohud-vulkan-headers/package.mk` | added | `50f3eeb726` mangohud: the two Vulkan subprojects come from pinned sources in meson's cache, never from a downlo | stays: no upstream copy |
| 6 | `apps/mangohud-vulkan-utility-libraries/package.mk` | added | `50f3eeb726` mangohud: the two Vulkan subprojects come from pinned sources in meson's cache, never from a downlo | stays: no upstream copy |
| 7 | `apps/mangohud/package.mk` | edited | `50f3eeb726` mangohud: the two Vulkan subprojects come from pinned sources in meson's cache, never from a downlo | the fork's change stays (upstream did not touch it) |
| 8 | `compat/box86/package.mk` | edited | `43d0bc3bf4` build - use the distribution name for ARM compatibility roots | the fork's change stays (upstream did not touch it) |
| 9 | `compat/lib32/package.mk` | edited | `43d0bc3bf4` build - use the distribution name for ARM compatibility roots | the fork's change stays (upstream did not touch it) |
| 10 | `graphics/cairo/package.mk` | edited | `bccbf54cd4` packages: comments said once and true; an empty quirk removed | conflict (content): see § The conflict set |
| 11 | `graphics/glslang/package.mk` | edited | `b4fc2a28cf` dependencies: qualify current coupled shader and Rust tools | conflict (modify/delete): see § The conflict set |
| 12 | `graphics/harfbuzz-icu/package.mk` | added | `4e4c31fc4c` harfbuzz-icu: install into the sysroot so WebKit can link it | stays: no upstream copy |
| 13 | `graphics/spirv-tools/package.mk` | edited | `f5f815faff` spirv-tools: tolerate GCC 12 host vector diagnostic | conflict (content): see § The conflict set |
| 14 | `initramfs/config/initramfs.x86_64.conf` | added | `5a00d9963c` GENERIC_X64 - initramfs - add /lib64 symlink for x86_64 loader | stays: no upstream copy |
| 15 | `lang/gcc/package.mk` | edited | `74377a057f` GENERIC_X64 - gcc: enable libatomic for x86_64 | conflict (content): see § The conflict set |
| 16 | `misc/modules/sources/gamelist.xml` | edited | `13ae350769` pixelelated: fix Tools identity and retain qualified VM evidence | auto-merges (both changed) |
| 17 | `multimedia/gstreamer/gst-plugins-bad/package.mk` | added | `5faa73834e` gst-plugins-base/bad: a payload is a name that loads | stays: no upstream copy |
| 18 | `multimedia/gstreamer/gst-plugins-base/package.mk` | edited | `5faa73834e` gst-plugins-base/bad: a payload is a name that loads | conflict (content): see § The conflict set |
| 19 | `multimedia/gstreamer/gstreamer/package.mk` | added | `fac608ff89` gstreamer: retain network library for installed plugins | conflict (add/add): see § The conflict set |
| 20 | `multimedia/libplacebo/package.mk` | edited | `d47acf6693` GENERIC_X64 - libplacebo: fix glslang/SPIRV link + disable demos for x86_64 | the fork's change stays (upstream did not touch it) |
| 21 | `multimedia/opusfile/package.mk` | edited | `63a2090a56` packages: pin retained game data and record licence scope | the fork's change stays (upstream did not touch it) |
| 22 | `network/avahi/package.mk` | edited | `1d07330ae1` avahi: the fork's unit ships; network-base-setup tells an already-up responder the name -- PL-01 (# | the fork's change stays (upstream did not touch it) |
| 23 | `network/avahi/system.d/avahi-daemon.service` | edited | `e76bafe860` avahi: the mDNS responder is on, after the device has its name (#50, D-NET-003) | the fork's change stays (upstream did not touch it) |
| 24 | `network/enet/package.mk` | edited | `63a2090a56` packages: pin retained game data and record licence scope | the fork's change stays (upstream did not touch it) |
| 25 | `network/networkmanager/config/NetworkManager.conf` | edited | `22e43d47c7` network: system.hostname owns the device name; NetworkManager leaves it alone; the name is applied  | conflict (content): see § The conflict set |
| 26 | `network/tailscale/package.mk` | edited | `63a2090a56` packages: pin retained game data and record licence scope | the fork's change stays (upstream did not touch it) |
| 27 | `network/zerotier-one/package.mk` | edited | `077197e6cd` zerotier-one: isolate client sources and retain proof (#528) | the fork's change stays (upstream did not touch it) |
| 28 | `security/gnutls/package.mk` | added | `4e464d7045` gnutls: point it at the CA bundle the image already ships | stays: no upstream copy |
| 29 | `tools/installer/scripts/installer` | edited | `a9af618398` pixelelated: apply lowercase identity and LCD wordmark | the fork's change stays (upstream did not touch it) |
| 30 | `tools/rocknix-abl/package.mk` | edited | `9aa7affee9` rocknix-abl: apply upstream v1.2 checksum fix (#600) | conflict (modify/delete): see § The conflict set |
| 31 | `tools/rocknix-splash/package.mk` | edited | `b137d8c373` pixelelated: integrate Ocean splash and finalize candidate inputs | the fork's change stays (upstream did not touch it) |
| 32 | `virtual/network/package.mk` | edited | `6e35a5fd04` raofflineproxy: package RAOfflineProxy's Linux service natively (#165) | the fork's change stays (upstream did not touch it) |
| 33 | `wayland/compositor/sway/autostart/111-sway-init` | edited | `ca39dd3519` GENERIC_X64 - sway - use software cursor on virtual displays | conflict (content): see § The conflict set |
| 34 | `wayland/compositor/sway/package.mk` | edited | `c6afa31db1` sway: wait for usable Wayland before starting ES | the fork's change stays (upstream did not touch it) |
| 35 | `wayland/compositor/sway/scripts/sway-ready` | added | `c6afa31db1` sway: wait for usable Wayland before starting ES | stays: no upstream copy |

- **Same change on both sides:** `NetworkManager.conf` (`hostname-mode=none`): drop ours' comment-only hunk at the merge.
- **An override that could be smaller:** `cairo`'s, once upstream's sourcing override lands (its own comment says the version line becomes redundant).
- **A constraint without its reason:** `gcc`'s 15.2.0 (F-09's note).

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- **`device-builds.md` § After rebasing:** read a modify/delete conflict on an override against the generic copy's pin before taking the deletion (F-11). The sentence, for the coordinator: *a deletion upstream of an override the fork has bumped puts the generic pin back; compare the two before resolving.*

### Codification Gaps (needs-new-rule)

- **The pre-merge read of the fork-edited ∩ upstream-changed set**, by `git merge-tree` with each orphan's pin before and after, is what this slice did by hand. It belongs in `rc-preflight`'s step-0 base check, as the brief's ladder proposes (an issue the coordinator files).

### Recommended Action Sequence

1. #852's stream (this slice).
2. #890's packet ahead of T5 (done, the coordinator's).
3. The conflict list and the orphan table read at the base merge (the integration).
4. `cairo`'s Backlog bump.
5. The rest at their owners (#585, #657).

## Second opinion (Phase 4.6)

**One seat, GPT-6 Astra at `max`, through the Facilitator** (D-WORKFLOW-184, -049).
- **The probe** (12:37:35 to 12:37:43): served `openai/gpt-6-astra` by OpenAI, `final.verification` PASS.
- **The refutation** (12:40:00 to 12:55:20): one attempt, http 200, `model_field` `openai/gpt-6-astra` (`provider_response`), served by OpenAI, effort `max`, 40,720 reasoning tokens, `finish=stop`; `final.verification` **PASS**.
- **The packet:** **398,152 bytes, sha256 `7e93a08906a8168fe86ecf6b24c9e2d6381d1f316c28ce1af63cd59e41d6dca5`**, equal to the provenance's `user_prompt_sha256`. The output is `gpt-audit.md`, 26,313 bytes.

**The output is a second opinion, graded item by item below against the artifact that decides it** (brief § 5 rule 5). Nothing the seat says is taken as evidence on its own.

### The seat's new items

| G | Seat's grade | Verdict | The artifact that decided it | Disposition |
| --- | --- | --- | --- | --- |
| G-01 | High | **Confirmed, Medium**: the installer never checks `dd`, `parted`, `mkfs.vfat` or `mount` (`installer:207`, `:280`, `:303`; `grep` finds no `\|\|` guard), and `Install Complete` (`:374`) prints after the gauge whatever happened. Medium, not High: the installer ships only on GENERIC_X64 (`test` reach) | `tools/installer/scripts/installer` at the hash | **F-14**, a `bug` (upstream's logic: rule 6 and #585) |
| G-02 | High | **Plausible, not verified**: the exclusion is a text match on mount sources (`:89-118`); no device graph was read | the same lines | a lead in F-14 |
| G-03 | Medium | **Narrowed, Low**: `PARTID="p"` (`:178`) is never reset, but `prompt_gpt` has no return path, so it bites only on a second install in the same session after an MMC/NVMe one | `:170-180`, `prompt_gpt()` | a lead in F-14 |
| G-04 | Medium | **Plausible, Low**: `*512` assumes 512-byte sectors (`prompt_gpt`); not tested on a 4Kn device | `prompt_gpt()` | a lead in F-14 |
| G-05 | Medium | **Plausible, not verified**: the order of the boot-config writes and the `/flash/*` copy (`:321-339`) | the lines | a lead in F-14 |
| G-06 | Low | **Plausible, Low** | `:43-46`, `:553-558` | a lead in F-14 |
| G-07 | Medium | **Refuted**: `sway-ready` sources `/etc/profile` (`:7`), and `wayland/compositor/sway/profile.d/050-sway.conf:4-5` exports `WAYLAND_DISPLAY=wayland-1` and `XDG_RUNTIME_DIR=/var/run/0-runtime-dir`, the same values as its fallbacks | `050-sway.conf` at the hash | withdrawn |
| G-08 | Low | **True, not a defect**: the 15 s is checked between rounds of at most about 2 s, a bounded wait | `sway-ready:21-35` | withdrawn: no change |
| G-09 | Medium | **Confirmed, Low**: `cut -b 5` takes one digit of the card number (`111-sway-init:31`), and `head -n 1` takes the first connector before testing it is connected. Upstream's line; the fork added only `Virtual` | `:28-34` | in F-17 (#585) |
| G-10, G-11, G-12, G-13 | Medium, Medium, Low, Low | **Plausible, not verified**: the Retroid, Pocket S and Pocket DS branches; upstream's lines, no device here | `111-sway-init` | in F-17 (#585) |
| G-14 | Low | **Confirmed, Low**: `After=network-base.service` without `Wants=`; whether something else pulls it in was not read | `avahi-daemon.service:6` | in F-17 (the fork's unit) |
| G-15 | Medium | **Confirmed, Medium**: `pre_configure_target` `curl -L`s ImGui, ImPlot and spdlog with no checksum (`apps/mangohud/package.mk:66-91`), outside `get_archive`, the mirror and T5's guard; ROCKNIX's lines (`01520aff68`), SM8550 only | the recipe; `git log -S` | **F-13**, a `bug` (rule 6, #585) |
| G-16 | Medium | **Confirmed, folded into F-02**: `ln -sf` onto an existing `${INSTALL}/opt` directory makes the link inside it, and an empty `INSTALL` at load makes the target the host's `/opt`. #852's fix uses `ln -sfn` inside a hook that runs with `INSTALL` set | `virtual/image:109-110` | F-02's stream |
| G-17 | Medium | **Confirmed, Low**: both architectures' archives use the one cache name `tailscale-<v>.tgz` (`pre_unpack`); sequential builds re-fetch on the stamp mismatch, and parallel builds are excluded (`device-builds.md`) | `network/tailscale/package.mk:15-30` | in F-17 (the fork's edited recipe) |
| G-18, G-19 | Medium | **Not graded as defects**: the cross-root copies are the multi-ABI design; the wildcard and the ICD loop are leads with no failing case shown | `compat/box86`, `compat/lib32` | withdrawn as defects, noted |
| G-20 | Medium | **Confirmed, Low**: a cache hit trusts the stamp without hashing the file (`get_archive:4-11` at the hash; `52e6794ba7`'s too). `scripts/` is T5's slice | `scripts/get_archive` | **F-15**, a lead for #844 (the fetch check) |
| G-21 | Medium | **Confirmed, latent, Low**: `s\|-O.\|-O3\|g` would turn `-Ofast` into `-O3ast` (`devel/glibc:64`, `:73`); no plan sets `-Ofast`; the base merge replaces the lines | `git grep -- -Ofast` empty | in F-17 (follows the base merge) |
| G-22 | Medium | **Confirmed, Low**: `-a root:$(get_setting root.password)` is unquoted inside `bash -c`, and the password lands in the process's arguments | `simple-http-server.service:7` | **F-16** (#585) |
| G-23 | Medium | **Plausible, not verified**: upstream's parser, changed upstream | the diff | in F-17 (follows the base merge) |
| G-24 | Low | **Confirmed, Low**: `key_jazz_dec_velocity=69` and `key_toggle_audio=69` in both `m8c` configs; the fork's GENERIC_X64 copy inherits H700's | `apps/m8c/config/*/config.ini:30-31` | in F-17 |
| G-25 | Low | **Plausible, Low, not this slice's**: `scripts/update_packages` is T5's, never run | `:18-32` | withdrawn here: a note for the coordinator |
| G-26 | Low | **Confirmed and fixed**: the table's *upstream's pin* cell was the first `PKG_VERSION` literal; it now says so (17 rows), and per-plan pins are not expanded on `upstream/next` | `q4-table.md` | applied |
| G-27 | Medium | **Confirmed**: `spirv-headers`' override is a third modify/delete conflict (`base-merge.txt`), outside this slice's 485, and the inventory marks it `unreached` although `spirv-tools` unpacks it. The coupled set is a triple | `base-merge.txt`; `inventory.json` | **F-11** widened; reported to the coordinator (D-WORKFLOW-198 names a pair) |

### The seat's refutations of the first reader

| F | Seat | Verdict |
| --- | --- | --- |
| F-01 | agree; `virtual/network:25-27` is conditional | **Accepted, narrowed**: the line is inside a condition; GENERIC_X64's plan and root build it (`viewplan`, the stamp) |
| F-02 | agree, Medium | **Accepted**, with G-16 folded in |
| F-03, F-04 | agree, Low, as observed outages | **Accepted**: the bugs say *answered 404 on two reads*, not *gone forever* |
| F-05 | the listing was not in the packet | **Accepted as a packet gap**: the read is `curl -fsSL https://cairographics.org/releases/` listing 1.18.2, 1.18.4 and 1.18.6 as the newest even-minor files, run between the 12:26 `ls-remote` loop and the 12:28 `samba` read and not stamped itself; quoted in `02` |
| F-06 | the 19 is wrong; `libfmt`'s override hides behind INHERITED | **Accepted**: 17 of the 19 edited recipes are outside the tool's set (`glslang` and `rocknix-abl` are in it, as orphans); `var()` greps `^PKG_VERSION=` at column 0, so `libfmt`'s `case`-branch override reads INHERITED |
| F-07, F-08 | agree, Low | **Accepted** |
| F-09 | agree, as integration work | **Accepted**; the dispositions are corrected for `gcc` (all three arches), `gstreamer` (ours already removes `/usr/share`), `gamelist.xml` (the merge applies upstream's removal), `gst-plugins-base` (`-Dapp=enabled`), `spirv-tools` (a triple), `rocknix-abl` (verify `openabl` first), `cairo` (its dependencies) and `111-sway-init` |
| F-10 | the virtio class does not cover every GENERIC_X64 deployment | **Accepted, narrowed**: GENERIC_X64 installed on x86 hardware with an Intel or AMD display (the installer's purpose) does pull the unit in; Low stands |
| F-11 | agree, conditional; `merge-tree` leaves ours; add `spirv-headers` | **Accepted**: the hazard is a resolution choice, which D-WORKFLOW-198 settles; the triple is reported |
| F-12 | the two modify/delete orphans are not dropped automatically; `cargo` is unevaluated | **Accepted**: the orphan table now says *if the deletion is taken* for both, and `cargo`'s cell is unevaluated |
| the `make update` cells | eleven eligible is not eleven changes; `moonlight` is a git URL | **Accepted**: the cell says *moves to its branch head if run*, and five of the nine hash pins are already at their default branch's HEAD (`jstest-sdl`, `rocknix-hotkey`, `sdljoytest`, `sdltouchtest`, `sixaxis`: `q4c-hash.txt`), so a run would move four (`box64` 429, `gamecontrollerdb` 30, `moonlight` 16, `box86` 7) |

**The net effect:**
- **Three new items:** F-13 (`mangohud`'s downloads, a `bug`), F-14 (the installer's unchecked steps, a `bug`), F-15 (the cache-hit trust, a lead).
- **Two Low items:** F-16 (the password quoting) and F-17 (eight small shapes, grouped).
- **One widened item:** F-11 (the triple).
- **One folded into F-02:** G-16.
- **Six withdrawn:** G-07, G-08, G-18, G-19, G-25, and G-26 (applied).
- **Eight dispositions corrected.**

The seat's part 3 is carried into § Coverage Boundary: the sway session wiring, device topology, the merged ABI and the 82 unfetched 200s.

## Quality Self-Check

- **Tables:** every row of the coverage, currency, orphan and conflict tables comes from `tools/t8-tables.py`, which asserts 485 and 260 and that each conflict's kind equals `merge-tree`'s.
- **Times:** every time is a `date -u` reading or a file a command wrote.
- **The brief's deltas** are named in `03` § 3.3.
- **What was not read** is in § Coverage Boundary, and no row claims it.

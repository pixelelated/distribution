# Analysis — M6.P2 T3, RetroArch and the libretro cores

**Auditor:** Code Auditor skill (v1.13.0), primary Claude Opus 5.5 (`anthropic/claude-opus-5-5`) at high effort
**Date:** 2026-10-24
**Subject:** #650 (`M6.P2 E798/T3`), slice `emulators-libretro`, 344 paths; `reviewed-at: d606301784`, the slice's bytes equal to `8ebaf8daad`
**Spec:** `docs/reviews/briefs/emulators-libretro.md` version 2; #650's fifteen criteria
**Depth:** Extended. Phase 4.6 (GPT-6 Astra, Gemini 4 Argon) runs after the M7 window's return line (§ Second opinion)

---

## Executive summary

The slice is the recipes, patches and configuration that decide which libretro cores each image carries, how RetroArch is built and patched, and the launch table EmulationStation reads. Three things are now proven, so every finding below is a finding about what ships:

- **The table is the build's own:** the host regeneration of `es_systems.cfg` from the tree's shell is byte-identical to the GENERIC_X64, H700 and SM8550 images.
- **The guest carries the tree:** the installed set on the GENERIC_X64 guest equals the tree's.
- **The rotation tables are the build's:** the five regenerate byte-identically.

**24 findings.** Four are High:

- **#802 (F-08):** the default PlayStation core on H700, RK3326, RK3566 and SM8550, `pcsx_rearmed32`, is installed under `/usr/lib32/libretro` only, while `runemu.sh` loads cores from `/tmp/cores` over `/usr/lib/libretro`. P1 shows that overlay on the guest.
- **F-09:** the next base merge brings upstream's fix for that, and the new `yabadabadoo-lr`, as `build.${DISTRO}-` copies that fail on the fork's `build.${DISTRONAME}` roots. `git merge-tree` merges both cleanly.
- **#806 (F-19):** on the SM8550 image `grep` has no PCRE, through a build-order race in grep's recipe, so `Install Steam.sh`'s `grep -oP` stops Install Steam at its Proton step.
- **F-07:** `aethersx2-sa`, which upstream dropped for a licensing concern, still ships on SM8550 (its image) and RK3566 (its regenerated table; Argon, Phase 4.6). The coordinator has ruled it class 1, with the base merge.

**Medium:**

- `melonds-ds-lr` fetches eleven dependencies from the network at configure time (F-15, blindspot 47's shape);
- `retroarch32` is skipped silently when the ARM root is not exactly one install directory (F-11, latent);
- network data reaches `eval` in `Install Steam.sh` (F-20; M7's `6101242e14` fixes it);
- the Steam runtime and Proton install with no integrity check (F-21);
- the exit hotkey's RPCS3 target names a process that never runs (F-24);
- the table's one-default rule is enforced by accident on one shape and not at all on the other (F-06, T5's code).

**The rest are Low or `Renovation`:** dead options, keys, assignments and flags; a short pin; comments that name a closed issue or a check that does not exist; copies.

**Currency (Q4), the slice's question:**

- **Against ROCKNIX:** all 14 upstream commits on the two directories are absent from `next`, and all are `to merge`, two of them adapted.
- **Against the projects:** of the 151 recipes' pins, 40 are current, 104 behind their project (ROCKNIX's to take), 1 behind ROCKNIX (`np2kai-lr`), and 6 not on their project's default branch.
- **RetroArch:** the pin is 7,623 commits behind master. Against master 15 of the 21 patches fail outright, and two of the fork's eight are already fixed upstream. A bump is a re-cut of the series.

**Time to play** on the image as built: **0.62 s** to the first frame, **1.01 s** game to game (n = 3), beside T1's and T2's. The logging key costs nothing measurable.

## Acceptance-criteria scorecard

At the end of Phase 2 (`02` § Criterion entries): 4 PASS (AC-06, AC-07, AC-08, AC-12), 5 PARTIAL (AC-01, AC-05, AC-09, AC-10, AC-11), 6 open for later stages of this lane (AC-02, AC-03, AC-04, AC-13, AC-14, AC-15), 0 FAIL. This file closes AC-09's, AC-10's and AC-11's gaps (§ Renovation face); AC-09's needed rows 7 and 14 read for save and state changes, done in § Second opinion after both seats found them unread. AC-01's closes when `05` exists. AC-05 closes at hand-back.

## Code Quality Assessment

### Strengths

- The fork's own lines carry their reasons beside them: `ppsspp-lr`'s strip, `mupen64plus-lr`'s patch set, `idtech-lr`'s pinned data, the rotation hooks.
- The generators fail closed with a reason, and both constructed failures were seen.
- The table guard `Configure retroarch for ${DEVICE}` fails closed.
- The fork's patches 0011 to 0019 each say what they fix and against which report, and 0015's fix is mechanically proven.

### Concerns

- Silent failure paths: `retroarch32` (F-11), `mk_es_systems`' `2>/dev/null` (F-06), grep's autodetected PCRE (#806), cmake's `FetchContent` (F-15).
- Comments that claim what does not happen: F-06, F-18, F-12's `content_history_dir`.

### Complexity Hotspots

- `virtual/emulators/package.mk`'s `makeinstall_target`: one function of about 1,630 lines, three responsibilities (the device lists live above it; the table and the directories in it).
- `Install Steam.sh`: 2,755 lines, five embedded Python programs, logic in several copies (F-23).
- Fifteen `retroarch.cfg` profiles of 817 to 3,530 lines, four of them copies (F-12, Q7).

## Cornerstone Conformance

`03` § 3.2's table: the packaging rules, `device-builds.md`'s merge and fetch lessons, `engineering-practices.md`'s guards and names. **One blindspot was committed in the code (47, F-15)**, and one in this lane's own proof work (74, P3's first launch, caught by its own log).

## Spec Fidelity

### Aligned

Every count of the brief re-derived without delta (`01` § Scope). The #336 line is drawn as the brief draws it. The read hash holds.

### Diverged

Seven brief deltas, none a stop (`03` § 3.3):

- 500 against 348 `<core>`;
- 131 against 132 `*-lr` recipes;
- the `6101242e14` origin claim;
- the `xmlstarlet` gap;
- the H700 root name;
- criterion 9's `git apply` wording.

## Missing Artifacts

Recommended, not built here:

- a host check that every core the table names exists where the launcher loads it;
- a check that a build's optional features match across device roots;
- a no-fetch guard for cmake cores;
- a driving case for 0011 in `tools/retroarch-wrapper-test`;
- `#264`'s RetroArch syntax check, still proposed.

## Risk Assessment

| Risk | Severity × impact | Mitigation |
| --- | --- | --- |
| A PlayStation game launched with the default core fails on H700 and SM8550 (#802) | High; the most common console on the main handhelds | `c9820d0e89` adapted to `DISTRONAME` with the base merge; `pcsx_rearmed` (64-bit) is the selectable workaround (the coordinator's FYI to M7) |
| The base merge takes upstream's two `${DISTRO}` copies verbatim and the arm-enabled builds stop (F-09) | High for the merge, none for players | the `git grep -F 'build.${DISTRO}-'` check on the merged tree |
| Install Steam cannot complete on SM8550 (#806) | High; a Tools entry | parse with `python3` (deferred:M7-merge); the grep recipe's `pcre2` dependency (T22's, #669) |
| A licensed-elsewhere package ships (F-07) | High in kind, the coordinator's (#528) | class 1, with the base merge |
| An image's `melonds-ds-lr` built from unpinned code, or a build without network failing (F-15) | Medium | pinned sources and `FETCHCONTENT_FULLY_DISCONNECTED` |
| A future pin bump leaves two install directories, and `retroarch32` vanishes silently (F-11) | Medium, latent | fail loudly on not-exactly-one |
| A table edit lists a `false` core first and two defaults ship (F-06 case B) | Medium, latent; T5's | `.../cores/core[last()]`, `fo` errors printed |

## Coverage Boundary

As `02` § Coverage Boundary. In brief:

- **Read whole or by mechanism:** the fork-own and fork-written units.
- **Read at Q4 and Q6:** the upstream-carried ones.
- **Proven on the guest:** the installed set and RetroArch's start.
- **Proven on the host against three images:** the table and the generators.
- **Not reached:** 32-bit RetroArch, arm builds, devices, the exit hotkey end to end (T1's), the 57 core patches (T42's), the standalone emulators (T30's).

## Finding Verification (Phase 4.5)

Each Critical or High finding, attacked before it is published:

- **F-08 (#802).** Refutation sought: another writer putting `pcsx_rearmed32_libretro.so` under `/usr/lib/libretro` or `/storage/cores` (`git grep -E '/storage/cores|/tmp/cores'`: only the mount and the profiles' keys); `retroarch32` resolving `-L` through `libretro_directory` (`-L` is an absolute path); an overlay with a second lower directory (`tmp-cores.mount` and P1's live `mount` line: `lowerdir=/usr/lib/libretro` only). **None found.** It also stands independently verified: the coordinator verified it on both images before filing #802. What stays a lead: the load failure itself, on an arm device.
- **F-09.** Refutation sought: the fork's roots also existing under the `${DISTRO}` name (`ls -d /workspace/repos/rocknix.worktrees/*/build.ROCKNIX-*`: none on the host; the M7 roots are all `build.pixelelated-*`); `DISTRO` and `DISTRONAME` being equal here (`config/options:24` `ROCKNIX`, `distributions/ROCKNIX/options:17` `pixelelated`). **Survives.**
- **F-19 (#806).** Refutation sought: a PCRE-capable grep earlier on the script's `PATH` (after `source /etc/profile` the `PATH` is `/usr/bin:/usr/sbin`, and `/usr/bin/grep` is the GNU binary); the strings check misreading a PCRE build (the binary links no PCRE library, its size is a third of the PCRE builds', and its root's `config.h` lacks `HAVE_LIBPCRE`, with `config.log` showing why). **Survives.** Independently verified and filed by the coordinator.
- **F-07.** Not a defect claim but a provenance fact, read from `c4d353449e` itself. Survives.

## Renovation face

### Q1 Modernize

| Finding | What is behind | The replacement |
| --- | --- | --- |
| F-13 | three `[ $? -eq 0 ] && echo` checks under `set -e` | delete them; the build engine fails the package |
| F-12 | renamed RetroArch keys in every profile (`input_duty_cycle`, `input_turbo_default_button`, `video_hdr_*`, `video_scale_integer_overscale`) and retired ones (`video_layout_*`, `netplay_stateless_mode`) | the pin's own key names, read from `configuration.c` per key at fix time |
| F-23 | dead assignments; logic in copies | Python's `json` for the release parsing (also #806) |
| F-15 | cmake `FetchContent` at configure | pinned sources |

The rotation generators are current Python 3, standard library only, with floors. No Python 2 remnant.

### Q2 Standards and best practices

- `pkgcheck` over 152 recipes: one FAIL (F-02, `sameboy-lr`), two WARNs (F-03; `emulators`' `install_script` read and not a finding).
- shellcheck over 30 files: two real errors (F-04), the rest read (`02` § shellcheck).
- One short pin (F-16).
- One patch held by fuzz (F-10).
- Network data in `eval` (F-20).
- The headers keep their credits; the fork's lines carry their reasons.

### Q3 Bugs

| Finding | Severity | State |
| --- | --- | --- |
| F-08 (#802) | High | live on four built devices |
| F-19 (#806) | High | live on SM8550 |
| F-24 | Medium | live on SM8550 (RPCS3's exit kill target) |
| F-21 | Medium | live (no integrity check on two payloads) |
| F-11 | Medium | latent |
| F-06 | Medium | latent; T5's code |
| F-05 | Medium (Phase 4.6; was Low) | live: `psx` falls back to DuckStation standalone on the VM; `st-v` has no emulator on four devices |
| F-22 | Low | live on interrupt |

The proofs: P3b shows patch 0018's fix holding for the AUTO SAVE tile's arguments. The wrapper test shows 0015's.

### Q4 Package currency: (a) the fork against ROCKNIX, (b) the pins against the projects, (c) RetroArch itself

**(a)** All 14 commits of `c445081a59..upstream/next` (`3421d7d178`) on the two directories, each dispositioned: `q4a-dispositions.md`, reproduced in this subsection below. The one pin that differs from ROCKNIX's is `np2kai-lr` (`d1a40352e2` here, `5939e0c6d5` upstream, row 14). Every core bump among them is `to merge` with its range named for the stream to read for save and state changes, citing #10. Nothing is applied on this branch.

**(b)** One row per recipe (151), from `tools/q4-pins.py` (run 2026-10-24 03:06 to 03:11 UTC; GitHub API only; no empty cell, the script's assertion, rc 0) and the three non-GitHub rows by hand (`q4-pins-byhand.md`). **Classes: `current` 40, `behind-project` 104, `behind-upstream` 1 (`np2kai-lr`), `pin-not-on-project` 6** (`dosbox-pure-lr` and `hatari-lr`: no common ancestor with the default branch; `flycast2021-lr`: the pin is ahead of `master`, on another line; `retropie-shaders`, `sameduck-lr`, `yabasanshiro-lr`: diverged). `behind-project` is informational for an upstream-carried recipe (ROCKNIX's to take); for the fork-introduced or fork-changed ones it is a line for #585. Repository facts the API answered: `fbalpha2019-lr`'s is renamed (`libretro/beetle-finalarcade2019`), `mu-lr`'s moved (`SquirrelJME/Mu`), `emuscv-lr`'s moved (GitLab 301 to `MaaaX-EPOCH84/libretro-emuscv`), and **`mupen64plus-lr`'s is archived**.

**(c)** The pin `bdba046fa6` (2026-06-06) is on `libretro/RetroArch` master, 7,623 commits behind it (`compare`, 0 behind), and after the last release `v1.22.2` (2025-11-20). The 21 patches applied as the build applies them (`tools/q4c-patches.sh`): all 21 at the pin (0004 only with fuzz, F-10); at master `4fe09508d4`, 15 fail outright and two need fuzz. Of the fork's eight, 0011 is upstream's (#19518) and 0015's defect is fixed on master (#19577), so both retire at a bump, and the other six need re-cutting: five fail as the build would meet them and 0019 applies only with fuzz (Astra, Phase 4.6). **A RetroArch bump is a re-cut of the series, not a pin edit**, and so `deferred:` to a stream brief, never applied here. The table is reproduced in this subsection below.

`tools/fork-package-freshness --list` names no path of this slice (its one emulators path is T30's `aethersx2-sa`).

#### Q4 (a): the 14 dispositions

| # | Commit | What it changes on the slice | Disposition | Reason |
| ---: | --- | --- | --- | --- |
| 1 | `c4d353449e` (2026-10-18) aethersx2: drop package due to licensing concern | `virtual/emulators/package.mk` (27 lines), `Start AetherSX2.sh` removed | **to merge** (class 1, with the base merge; the coordinator's ruling on #650, maintainer told on #346) | F-07: a licensing removal; the fork's SM8550 carries the package. `Already written:` AetherSX2's settings and memory cards under `/storage` on devices that had it |
| 2 | `075a7c303b` (2026-10-17) the multimedia merge #3513 | adds `retroarch/patches/retroarch-0100-ffmpeg9-lavc63.patch` (189 lines) | **to merge**, with the rest of #3513 | the patch adapts RetroArch to the FFmpeg the same merge brings; one without the other breaks one build or the other. Applies cleanly alone |
| 3 | `bb8d0aab8e` (2026-10-16) s922x: remove 32bit yabadabadoo | `virtual/emulators/package.mk` (1 line) | **to merge**, after row 4 | S922X only (not a fork device) |
| 4 | `8704addb6b` (2026-10-15) yabadabadoo: new Saturn emulator | the `yabadabadoo-lr` recipe and patch; `EMUS_32BIT` and the `saturn` table lines | **to merge**, **adapted**: `yabadabadoo-lr/package.mk:46` copies from `build.${DISTRO}-${DEVICE}.arm`, which must become `${DISTRONAME}` (F-09) | a new core (player-visible: a new Saturn emulator on 32-bit-capable devices, H700 among them) arriving with ROCKNIX's merge; its `Already written:` is nothing (new). A core's save and state format is new, so #10 has nothing to compare |
| 5 | `a1ea79474b` (2026-10-11) rk3566: port to inputplumber | `retroarch/sources/RK3566/retroarch.cfg`: `input_enable_hotkey_btn`, `input_exit_emulator_btn`, `input_hold_fast_forward` to `nul` | **to merge**, only together with the rest of `a1ea79474b` (outside the slice) | RK3566 is a fork-built device: the hotkeys move from RetroArch's binds to InputPlumber, so the RetroArch half alone would leave RK3566 with no exit hotkey. `Already written:` the profile is copied to `/storage/.config/retroarch/retroarch.cfg` once (9fd73da845's note), so devices keep their old binds until the setsettings layer or a profile refresh writes them, which is to be read at the merge (T1's `setsettings.sh` writes hotkeys per launch) |
| 6 | `aca36dbad7` (2026-10-11) mame-lr: don't depend on retroarch | `mame-lr/package.mk` (1 line) | **to merge**, after row 8 | follows `af70bd435b` |
| 7 | `6103571f67` (2026-10-11) the core-updates merge #3470 | `doublecherrygb-lr/patches/001-*`, `flycast2021-lr/patches/02-*`, `np2kai-lr/patches/001-*` added; `emuscv-lr`, `mame-lr`, `same_cdi-lr`, `uae4arm-lr`, `vircon32-lr` recipes | **to merge** | core updates. Each changed core's save and state format is read against #10 by the stream that takes the bump (Q4 (b)'s `behind-upstream` row is `np2kai-lr`, row 14) |
| 8 | `af70bd435b` (2026-10-10) libretro-cores: add retroarch as PKG_DEPENDS_TARGET | 136 recipes, one line each | **to merge**, resolving five conflicts: the rotation-table recipes keep both, `toolchain Python3:host retroarch` (F-09) | a build-order dependency; no runtime change |
| 9 | `eeb33c5a37` (2026-10-05) fix quit hotkey targets for RPCS3, AetherSX2 and mupen64plus | `Start AetherSX2.sh` (`set_kill set "aethersx2"`), `Start RPCS3.sh` (`set_kill set "-9 rpcs3-sa"`) | **to merge** (`Start RPCS3.sh`; the AetherSX2 half goes with row 1) | **a defect on `next`**: the exit hotkey's kill target names a process that is not running for RPCS3 on SM8550 (`rpcs3` against the binary `rpcs3-sa`). Applies cleanly. The exit hotkey is T1's seam (`set_kill`), noted for the coordinator |
| 10 | `c9820d0e89` (2026-10-04) pcsx_rearmed-lr: install the 32-bit core where runemu loads it | `pcsx_rearmed-lr/package.mk` +3 | **to merge, adapted** to `${DISTRONAME}` (F-08, F-09; **#802**, the coordinator's) | the default `psx` core on H700, RK3326, RK3566 and SM8550 is absent where the launcher loads it |
| 11 | `dc781c0c75` (2026-10-04) udev-rules: non-blocking systemctl | `virtual/emulators/udev.d/99-automount.rules` | **to merge** | a hang avoided at card insertion (T1's automount seam) |
| 12 | `096c0d4e96` (2026-10-04) the mmc-resume merge #3304 | the same 3 lines as row 13 | **to merge** (with row 13; already present once row 13 is applied) | merge commit of row 13 |
| 13 | `142df62157` (2026-10-02) mmc: retry a failed SD card resume after a power cycle | `99-automount.rules` +3 | **to merge** | a fix for the card a handheld boots from |
| 14 | `6679670966` (2026-10-01) the gcc-glibc merge #3415 | `np2kai-lr` pin `d1a40352e2` to `5939e0c6d5` with its `PKG_SHA256` | **to merge** | Q4 (b)'s one `behind-upstream` row. A core bump: np2kai's commit range `d1a40352e2..5939e0c6d5` is read for save and state changes by the stream that takes it, citing #10. Not applied here |

**So all 14 are `to merge`, and two need adapting.** None is "not applicable".

- **Adapt rows 4 and 10:** `${DISTRO}` becomes `${DISTRONAME}`.
- **Resolve row 8:** keep both dependency lines in the five rotation-table recipes.
- **Order:** row 5 lands only with its out-of-slice half; rows 3 and 6 follow rows 4 and 8.
- **Row 9's RPCS3 half is a live defect on SM8550**, punch-listed as such.

#### Q4 (b): one row per recipe (151)

| Recipe | Pin | Pin date | Project head date | Days | Class | Upstream | Upstream pin (if it differs) |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| `81-lr` | `fa7094910d04` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `a5200-lr` | `40c6f2f1ad4a` | 2026-08-01 | 2026-08-01 | 0 | current | same |  |
| `arduous-lr` | `798e3950f1de` | 2026-04-20 | 2026-09-20 | 152 | behind-project | same |  |
| `atari800-lr` | `cd721790a0aa` | 2026-08-15 | 2026-09-01 | 17 | behind-project | same |  |
| `b2-lr` | `869a541f8659` | 2026-08-16 | 2026-09-06 | 20 | behind-project | same |  |
| `beetle-gba-lr` | `bb9edd1d611f` | 2026-08-23 | 2026-09-03 | 11 | behind-project | same |  |
| `beetle-lynx-lr` | `fcdefcfb3c11` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `beetle-ngp-lr` | `a50d5ac288a8` | 2026-06-14 | 2026-06-14 | 0 | current | same |  |
| `beetle-pce-fast-lr` | `bebe2b13a840` | 2026-08-21 | 2026-10-23 | 63 | behind-project | same |  |
| `beetle-pce-lr` | `ae99235c2139` | 2026-04-11 | 2026-09-26 | 167 | behind-project | same |  |
| `beetle-pcfx-lr` | `0580dee757ad` | 2026-08-23 | 2026-09-04 | 12 | behind-project | same |  |
| `beetle-psx-lr` | `ef51860dbd71` | 2026-08-23 | 2026-10-24 | 61 | behind-project | same |  |
| `beetle-saturn-lr` | `ed549bdac0e1` | 2026-08-11 | 2026-10-21 | 70 | behind-project | same |  |
| `beetle-supafaust-lr` | `642d1d1b6684` | 2026-08-23 | 2026-08-23 | 0 | current | same |  |
| `beetle-supergrafx-lr` | `3c6fcd3deded` | 2026-04-20 | 2026-10-06 | 168 | behind-project | same |  |
| `beetle-vb-lr` | `83ed42608601` | 2026-08-23 | 2026-10-12 | 50 | behind-project | same |  |
| `beetle-wswan-lr` | `4b01295838ea` | 2026-07-31 | 2026-07-31 | 0 | current | same |  |
| `bk-lr` | `fe64da42ee46` | 2026-04-20 | 2026-09-04 | 136 | behind-project | same |  |
| `bluemsx-lr` | `e3086eb5d36d` | 2026-08-23 | 2026-08-23 | 0 | current | same |  |
| `boom3-lr` | `0bea79abf5ec` | 2022-08-10 | 2026-10-18 | 1530 | behind-project | same |  |
| `bsnes-hd-lr` | `fc26b25ea236` | 2025-12-05 | 2025-12-05 | 0 | current | same |  |
| `bsnes-lr` | `b102d6d5817b` | 2025-04-11 | 2026-09-19 | 526 | behind-project | same |  |
| `bsnes-mercury-accuracy-lr` | `ea22363fb0c1` | 2026-08-23 | 2026-09-04 | 12 | behind-project | same |  |
| `bsnes-mercury-balanced-lr` | `ea22363fb0c1` | 2026-08-23 | 2026-09-04 | 12 | behind-project | same |  |
| `bsnes-mercury-performance-lr` | `ea22363fb0c1` | 2026-08-23 | 2026-09-04 | 12 | behind-project | same |  |
| `bsnes2014-accuracy-lr` | `1a6b3caf1876` | 2026-07-26 | 2026-09-04 | 39 | behind-project | same |  |
| `bsnes2014-balanced-lr` | `1a6b3caf1876` | 2026-07-26 | 2026-09-04 | 39 | behind-project | same |  |
| `bsnes2014-performance-lr` | `1a6b3caf1876` | 2026-07-26 | 2026-09-04 | 39 | behind-project | same |  |
| `cap32-lr` | `4abfb8be233b` | 2026-04-05 | 2026-10-21 | 198 | behind-project | same |  |
| `common-shaders` | `9c0d839a1965` | 2026-04-11 | 2026-04-11 | 0 | current | same |  |
| `core-info` | `b03bfc451381` | 2026-08-25 | 2026-10-22 | 57 | behind-project | same |  |
| `crocods-lr` | `a9c63b294437` | 2026-07-30 | 2026-07-30 | 0 | current | same |  |
| `daphne-lr` | `6f1695dd1f37` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `desmume-lr` | `8f6b32cb9a5e` | 2026-08-23 | 2026-09-20 | 28 | behind-project | same |  |
| `dolphin-lr` | `2ce4b654546b` | 2026-08-25 | 2026-10-23 | 58 | behind-project | same |  |
| `dosbox-core-lr` | `7bcf083e8309` | 2025-09-27 | 2025-09-27 | 0 | current | same |  |
| `dosbox-pure-lr` | `7f6e8fb7385f` | 2026-07-28 | 2026-10-03 | 67 | pin-not-on-project | same |  |
| `doublecherrygb-lr` | `1587acddb2b5` | 2026-07-30 | 2026-10-19 | 80 | behind-project | same |  |
| `duckstation-lr` | `24c373245ebd` | 2021-01-07 | 2026-10-23 | 2115 | behind-project | same |  |
| `easyrpg-lr` | `212f3466c9f2` | 2026-08-03 | 2026-10-19 | 77 | behind-project | same |  |
| `ecwolf-lr` | `0cccd9a85d7f` | 2026-08-20 | 2026-08-20 | 0 | current | same |  |
| `emuscv-lr` | `dfce10df090c` | 2022-10-18 | 2026-10-14 | 1457 | behind-project (by hand, q4-pins-byhand.md) | same |  |
| `fake08-lr` | `814991a2571a` | 2026-06-13 | 2026-06-13 | 0 | current | same |  |
| `fbalpha2012-lr` | `0ce31536bef3` | 2026-07-28 | 2026-07-28 | 0 | current | same |  |
| `fbalpha2019-lr` | `0581797db6fd` | 2022-10-08 | 2026-09-04 | 1426 | behind-project | same |  |
| `fbneo-lr` | `f3b774987e00` | 2026-08-23 | 2026-10-21 | 58 | behind-project | same |  |
| `fceumm-lr` | `236ccdfc911e` | 2026-08-22 | 2026-10-11 | 49 | behind-project | same |  |
| `flycast-lr` | `c3763d8fc420` | 2026-08-23 | 2026-10-24 | 61 | behind-project | same |  |
| `flycast2021-lr` | `603814c9f73b` | 2025-01-16 | 2022-04-06 | -1016 | pin-not-on-project | same |  |
| `fmsx-lr` | `f013e213458e` | 2026-06-04 | 2026-09-26 | 113 | behind-project | same |  |
| `freechaf-lr` | `76c7a84f1f7e` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `freeintv-lr` | `ef3e0fe322be` | 2026-08-11 | 2026-08-11 | 0 | current | same |  |
| `freej2me-lr` | `1.52` | 2025-12-24 | 2026-10-17 | 296 | behind-project | same |  |
| `fuse-lr` | `2a5f1d43fec7` | 2026-08-12 | 2026-09-26 | 44 | behind-project | same |  |
| `gambatte-lr` | `d9d6cd06382d` | 2026-08-21 | 2026-10-23 | 63 | behind-project | same |  |
| `gearboy-lr` | `542f60b70656` | 2026-08-25 | 2026-10-24 | 59 | behind-project | same |  |
| `gearcoleco-lr` | `fd6c7ccca763` | 2026-08-24 | 2026-10-24 | 60 | behind-project | same |  |
| `geargrafx-lr` | `ca629d729a36` | 2026-08-24 | 2026-10-24 | 60 | behind-project | same |  |
| `gearlynx-lr` | `6b8c8f781e43` | 2026-08-24 | 2026-10-24 | 60 | behind-project | same |  |
| `gearsystem-lr` | `2c725424715d` | 2026-08-24 | 2026-10-24 | 60 | behind-project | same |  |
| `genesis-plus-gx-lr` | `b7e79b3641eb` | 2026-08-21 | 2026-10-23 | 63 | behind-project | same |  |
| `genesis-plus-gx-wide-lr` | `b7ad005431f5` | 2026-07-28 | 2026-07-28 | 0 | current | same |  |
| `geolith-lr` | `20aa7cd25d1d` | 2026-08-12 | 2026-10-11 | 59 | behind-project | same |  |
| `glsl-shaders` | `4f4eb801b2db` | 2026-08-23 | 2026-10-23 | 61 | behind-project | same |  |
| `gpsp-lr` | `8d268a6bb2cd` | 2026-08-25 | 2026-09-19 | 25 | behind-project | same |  |
| `gw-lr` | `91d599b951e7` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `handy-lr` | `bc55d462f0b2` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `hatari-lr` | `24e7bd744f24` | 2026-08-11 | 2026-10-16 | 66 | pin-not-on-project | same |  |
| `idtech-lr` | `1.0` | 2024-04-19 | 2024-04-19 (the file's last change) | 0 | current (by hand, q4-pins-byhand.md) | same |  |
| `jaxe-lr` | `c767afd785e0` | 2026-07-24 | 2026-07-24 | 0 | current | same |  |
| `kronos-lr` | `46e687cb07f4` | 2024-10-25 | 2026-07-18 | 630 | behind-project | same |  |
| `liblcf` | `92c4450a1bc1` | 2025-04-06 | 2026-08-03 | 484 | behind-project | same |  |
| `libretro-database` | `4de37d2c8042` | 2026-08-24 | 2026-10-10 | 47 | behind-project | same |  |
| `libspeexdsp` | `738e17905e1c` | 2023-02-28 | 2025-07-05 | 857 | behind-project | same |  |
| `libxmp-lite` | `4.5.0` | 2021-06-10 | 2026-10-10 (`libxmp-4.7.4`) | 1948 | behind-project (by hand, q4-pins-byhand.md) | same |  |
| `mame-lr` | `24cffe763621` | 2026-08-20 | 2026-10-09 | 50 | behind-project | same |  |
| `mame2003-lr` | `259339e92d5f` | 2026-07-28 | 2026-09-26 | 59 | behind-project | same |  |
| `mame2003-plus-lr` | `a045126dad33` | 2026-08-24 | 2026-10-24 | 60 | behind-project | same |  |
| `mame2010-lr` | `484456818393` | 2026-07-03 | 2026-09-02 | 61 | behind-project | same |  |
| `mame2015-lr` | `283e04b03c12` | 2026-06-04 | 2026-09-06 | 94 | behind-project | same |  |
| `melonds-ds-lr` | `bc4e4b67d2d4` | 2026-08-22 | 2026-09-27 | 35 | behind-project | same |  |
| `melonds-lr` | `66b5d2634cd0` | 2026-07-19 | 2026-07-19 | 0 | current | same |  |
| `mesen-lr` | `0102910c39ad` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `mesen-s-lr` | `9e4fdeb9b336` | 2026-08-23 | 2026-08-23 | 0 | current | same |  |
| `mgba-lr` | `e31759b24e7a` | 2026-08-06 | 2026-09-17 | 41 | behind-project | same |  |
| `minivmac-lr` | `babdf7b53d36` | 2026-04-20 | 2026-04-20 | 0 | current | same |  |
| `mojozork-lr` | `f94c3104aa18` | 2026-07-25 | 2026-09-14 | 51 | behind-project | same |  |
| `mu-lr` | `f9d34a000644` | 2026-08-16 | 2026-09-26 | 40 | behind-project | same |  |
| `mupen64plus-lr` | `ab8134ac90a5` | 2019-07-05 | 2019-07-05 | 0 | current | same |  |
| `mupen64plus-nx-lr` | `f275caf4b2bf` | 2026-08-06 | 2026-10-22 | 77 | behind-project | same |  |
| `neocd_lr` | `8f2d42c1cebc` | 2026-08-24 | 2026-10-03 | 40 | behind-project | same |  |
| `nestopia-lr` | `b08b473f961e` | 2026-08-25 | 2026-10-23 | 58 | behind-project | same |  |
| `np2kai-lr` | `d1a40352e24f` | 2026-08-23 | 2026-09-05 | 12 | behind-upstream | differs | `5939e0c6d598` |
| `o2em-lr` | `679d6fec0496` | 2026-07-21 | 2026-07-21 | 0 | current | same |  |
| `opera-lr` | `a501a278d057` | 2026-08-21 | 2026-10-23 | 63 | behind-project | same |  |
| `panda3ds-lr` | `5aaa1d26565c` | 2026-08-11 | 2026-10-04 | 53 | behind-project | same |  |
| `parallel-n64-lr` | `f8605345e13c` | 2025-03-02 | 2026-10-23 | 599 | behind-project | same |  |
| `pcsx_rearmed-lr` | `da2cb8ecd17f` | 2026-08-01 | 2026-10-01 | 60 | behind-project | same |  |
| `picodrive-lr` | `733c711a477a` | 2026-08-20 | 2026-09-26 | 36 | behind-project | same |  |
| `play-lr` | `04bde0df87ee` | 2026-08-11 | 2026-10-22 | 71 | behind-project | same |  |
| `pokemini-lr` | `132111b76343` | 2026-07-31 | 2026-07-31 | 0 | current | same |  |
| `potator-lr` | `227c5f6f3ce7` | 2026-06-04 | 2026-06-04 | 0 | current | same |  |
| `ppsspp-lr` | `fa50bb197606` | 2026-05-16 | 2026-10-24 | 160 | behind-project | same |  |
| `prboom-lr` | `861959f30fe0` | 2026-08-20 | 2026-10-17 | 58 | behind-project | same |  |
| `prosystem-lr` | `8a88014287c7` | 2026-08-22 | 2026-08-22 | 0 | current | same |  |
| `puae-lr` | `96ebfcfc2c66` | 2026-07-30 | 2026-10-06 | 68 | behind-project | same |  |
| `puae2021-lr` | `96ebfcfc2c66` | 2026-07-30 | 2026-10-06 | 68 | behind-project | same |  |
| `px68k-lr` | `0ad84d7058a1` | 2026-08-22 | 2026-08-22 | 0 | current | same |  |
| `quasi88-lr` | `b5a0e044a914` | 2026-07-22 | 2026-10-06 | 75 | behind-project | same |  |
| `quicknes-lr` | `26bb785c9ded` | 2026-07-06 | 2026-07-06 | 0 | current | same |  |
| `race-lr` | `c7810dd7f172` | 2026-06-29 | 2026-06-29 | 0 | current | same |  |
| `retroarch` | `bdba046fa676` | 2026-06-06 | 2026-10-24 | 140 | behind-project | same |  |
| `retroarch-assets` | `76cc6cf03507` | 2025-11-10 | 2026-10-01 | 325 | behind-project | same |  |
| `retroarch-joypads` | `38cf938bba0a` | 2025-11-10 | 2026-10-22 | 345 | behind-project | same |  |
| `retroarch-overlays` | `ea3f2bf187ae` | 2025-11-21 | 2026-10-15 | 328 | behind-project | same |  |
| `retropie-shaders` | `43eaf9b91857` | 2024-11-16 | 2016-12-12 | -2896 | pin-not-on-project | same |  |
| `same_cdi-lr` | `7ee1d8e9cb43` | 2025-01-31 | 2026-09-26 | 603 | behind-project | same |  |
| `sameboy-lr` | `aa158a889a48` | 2026-07-22 | 2026-07-22 | 0 | current | same |  |
| `sameduck-lr` | `5619abdb01ce` | 2023-12-10 | 2026-10-13 | 1037 | pin-not-on-project | same |  |
| `scummvm-lr` | `292e40993838` | 2026-08-20 | 2026-10-22 | 63 | behind-project | same |  |
| `skyemu-lr` | `01516d6798e3` | 2026-06-26 | 2026-10-13 | 108 | behind-project | same |  |
| `slang-shaders` | `4812a82f6c9a` | 2026-08-25 | 2026-10-22 | 58 | behind-project | same |  |
| `smsplus-gx-lr` | `8a63f82d3c3b` | 2026-06-25 | 2026-09-04 | 70 | behind-project | same |  |
| `snes9x-lr` | `890b5d445538` | 2026-08-16 | 2026-09-19 | 33 | behind-project | same |  |
| `snes9x2002-lr` | `5bd8bd6d449b` | 2026-06-25 | 2026-09-21 | 88 | behind-project | same |  |
| `snes9x2005_plus-lr` | `deb49d80d183` | 2026-07-22 | 2026-09-26 | 65 | behind-project | same |  |
| `snes9x2010-lr` | `7db129b1ecdc` | 2026-08-16 | 2026-09-21 | 35 | behind-project | same |  |
| `stella-lr` | `c1ffb833c8b1` | 2026-08-23 | 2026-10-12 | 49 | behind-project | same |  |
| `supersnes9x-lr` | `691e47b40fb3` | 2026-08-25 | 2026-10-22 | 58 | behind-project | same |  |
| `swanstation-lr` | `7f69c199ed88` | 2026-08-11 | 2026-10-24 | 73 | behind-project | same |  |
| `tgbdual-lr` | `0392c9c469e6` | 2026-08-23 | 2026-08-23 | 0 | current | same |  |
| `theodore-lr` | `4d469ce0f71e` | 2026-08-17 | 2026-08-17 | 0 | current | same |  |
| `tic80-lr` | `7020500a6e88` | 2026-01-16 | 2026-10-23 | 280 | behind-project | same |  |
| `tyrquake-lr` | `e57bb11597e8` | 2026-07-15 | 2026-10-12 | 89 | behind-project | same |  |
| `uae4arm-lr` | `276979efa4f8` | 2026-05-08 | 2026-09-07 | 122 | behind-project | same |  |
| `uzem-lr` | `d991ee94547c` | 2026-08-23 | 2026-08-23 | 0 | current | same |  |
| `vba-next-lr` | `2b96fd3a7702` | 2026-07-21 | 2026-08-31 | 41 | behind-project | same |  |
| `vbam-lr` | `115defb3a318` | 2026-08-23 | 2026-08-23 | 0 | current | same |  |
| `vecx-lr` | `8f671cc9d737` | 2026-04-11 | 2026-10-17 | 188 | behind-project | same |  |
| `vice-lr` | `91d0d4d884ac` | 2024-04-01 | 2026-10-22 | 934 | behind-project | same |  |
| `vircon32-lr` | `3a1b4ae3fb75` | 2026-06-02 | 2026-10-11 | 131 | behind-project | same |  |
| `virtualjaguar-lr` | `e6709d27bd45` | 2026-08-25 | 2026-10-24 | 59 | behind-project | same |  |
| `vitaquake2-lr` | `59a511555106` | 2026-07-28 | 2026-09-20 | 53 | behind-project | same |  |
| `vitaquake2-rogue-lr` | `$(get_pkg_ve` | 2026-07-28 | 2026-09-20 | 53 | behind-project | same |  |
| `vitaquake2-xatrix-lr` | `$(get_pkg_ve` | 2026-07-28 | 2026-09-20 | 53 | behind-project | same |  |
| `vitaquake2-zaero-lr` | `$(get_pkg_ve` | 2026-07-28 | 2026-09-20 | 53 | behind-project | same |  |
| `vitaquake3-lr` | `8ab09d1f54bd` | 2026-07-28 | 2026-09-20 | 53 | behind-project | same |  |
| `wasm4-lr` | `3f7a861a818b` | 2026-08-23 | 2026-09-11 | 19 | behind-project | same |  |
| `wildmidi` | `405ca73` | 2018-11-24 | 2026-08-20 | 2825 | behind-project | same |  |
| `xmil-lr` | `3106aa54ffb2` | 2026-08-23 | 2026-08-23 | 0 | current | same |  |
| `yabasanshiro-lr` | `39535a6abcad` | 2024-05-23 | 2026-05-30 | 737 | pin-not-on-project | same |  |

#### Q4 (c): the 21 patches at the pin and at master

| Patch | Author | At the pin (control): `git apply` / fuzz 0 / applied | At master: `git apply` / fuzz 0 / applied |
| --- | --- | --- | --- |
| `0001-Increase-glui-size` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (2 of 2 hunks) |
| `0001-Increase-ozone-size` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (2 of 2) |
| `0001-Increase-ozone-widget_size` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 1) |
| `0002-quit-not-restart` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 1) |
| `0003-fix-oga-no-preferred` | upstream | ok / ok / clean | ok / ok / offset |
| `0004-drm-resolution` | upstream | **FAIL / FAIL / fuzz** | FAIL / FAIL / fuzz |
| `0006-no-screen-brightness` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 2) |
| `0008-disable_search` | upstream | ok / ok / offset | ok / ok / offset |
| `0009-hide-wayland-checkerboard` | upstream | ok / ok / offset | ok / ok / offset |
| `0010-paths` | upstream | ok / ok / clean | FAIL / FAIL / **FAILED** (1 of 4) |
| `0011-cheevos-sounds` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 2) |
| `0011-video-thread-wrapper-serialise-posters` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (4 of 4); **upstream's own form of it is on master** (#19518, merged 2026-09-08) |
| `0012-cheevos-cmd` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 1) |
| `0013-cheevos-offline-proxy-toast` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (`intl/msg_hash_fr.h`, `msg_hash.h`) |
| `0014-widgets-backdrop-follows-the-font` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (3 of 6) |
| `0015-video-thread-wrapper-run-a-command-once` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (2 of 2); **its defect is already fixed on master** (#19577, its author: *"master already fixes this"*) |
| `0016-widgets-message-queue-floor` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (2 of 4) |
| `0017-widgets-sharp-font-sizes` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (3 of 5) |
| `0018-auto-slot-survives-content-load` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (`runtime_file.c`, 1 of 2; #19223 changed `state_slot` there after the pin) |
| `0019-widgets-message-queue-keeps-its-place` | **fork** | ok / ok / clean | FAIL / FAIL / fuzz |
| `batteryplus/0001-batteryplus-capacity` | upstream | **FAIL** / ok / clean | FAIL / ok / offset |

### Q5 Efficiency

Measured on the guest (`BUILD_ID 069fc270442134fe771258418adf4e666e0473fb`, 4 vCPU, 8 GiB, virgl on the Intel iGPU, 1280x800; `system.loglevel=verbose`, the engineering image's default):

| Number (median / mean / max) | T3 (n = 3, the image) | T1 (`--quick` n = 1 with the tree's scripts / stage B median of three) | T2 (pin, median of three) | #336's baseline |
| --- | --- | --- | --- | --- |
| interface to the game's first frame | **0.62 / 0.68 / 0.83 s** | 0.73 s / 0.64 s | 0.65 s | 1.05 s |
| a game's exit to the next game's first frame | **1.01 / 1.01 / 1.02 s** | 1.01 s / 1.01 s | 1.01 s | 2.03 s |

The configuration P2 ran with is `/storage/.config/retroarch/retroarch.cfg` sha256 `7b31c3cdbe618a77…`, with `video_driver = "gl"` (the image's profile already says `gl`, so `--vm` was a no-op). The run ends `Not a pass` (no cloud for the exit sync, `--no-configure-remote`, as the brief expects).

Every key the brief names as a possible cost, measured or not with why:

| Key (GENERIC_X64 profile value) | Managed by `setsettings.sh` per launch? | Measured? |
| --- | --- | --- |
| `log_verbosity = "true"` (all fifteen profiles) | no | **measured (P4): 0.58 / 0.60 / 0.71 s with `"false"`**, inside T1's 0.64 to 0.76 s spread on the same image, so no measurable cost (configuration sha256 `f00841def91de6b8…`, restored after) |
| `video_shader_enable = "false"` | yes (2 mentions) | not measured: off in the profile, and the per-game value is `setsettings`' |
| `rewind_enable = "false"` | yes (3) | not measured: off; its cost exists only when a game enables it |
| `run_ahead_enabled = "false"` | yes (3) | not measured: off |
| `audio_latency = "32"` | yes (1) | not measured: no harness measures audio start; the first-frame number is video's |
| `netplay_*` | yes (20) | not measured: netplay is off at a plain launch |
| `cheevos_enable = "false"` | yes (2) | not measured here: the proxy path is the offline-achievements area's; off in the profile |
| `content_history_size = "200"`, `history_list_enable = "true"` | no | not measured: the history is written at exit, and the game-to-game number (1.01 s) is unchanged by it across T1's, T2's and this run |
| `menu_driver = "ozone"`, `menu_*` | yes (1) | not measured: no menu is drawn on a launch from the interface |
| `core_updater_buildbot_*` | no | not measured: no network request at launch (the key `9fd73da845` found dead is not read at all) |
| `video_threaded = "true"` | no | not measured: toggling it changes the threading patches 0011 and 0015 exist for; not a knob to measure against |
| the five `tmp-*.mount` units at boot (RetroArch's `post_install`) | n/a | not measured: boot time is `time-to-play`'s `startup` cell, which reboots the guest and was not in the brief's run set |

Build options (`-O` levels, LTO, `PKG_MAKE_OPTS_TARGET`) are leads for a build this lane does not run. `flycast2021-lr` raises `-O2`/`-O3` to `-Ofast` (its `post_unpack`), upstream's choice.

### Q6 Dead ends

The five reachability tables are reproduced below (`tools/q6-tables.py`, run 2026-10-24 ~03:50 UTC over the inventory and the five regenerated tables; `q6-tables.md`).

- **Table 1:** 137 recipes by suffix, 132 in the membership (the brief's 131 `*-lr` plus `neocd_lr`) and 5 outside it. Its source is the inventory's `reachable_by` and `buildable_by`, and its check the metapackage's lists per device, with 0 disagreements.
- **Carried by no built device: exactly the five outside the membership, all T24's (`emulators-dead-ends`):** `boom3-lr` and `vitaquake3-lr`, which `idtech-lr` adds only on x86_64, where GENERIC_X64 skips `idtech-lr`; and `mame2003-lr`, `panda3ds-lr` and `play-lr`, in no device's list. **Every core of the membership is carried by at least one built device.**
- **`Already written:` for the five:** no fork image carries their `.so`, so nothing of theirs was written on a fork device. Only `core-info`'s `.info` files for `boom3`, `vitaquake3` and others ship (read in the H700 and SM8550 images' `usr/lib/libretro/`). A device upgraded from upstream ROCKNIX on an x86_64 build could hold saves or states of theirs, which T24's table reads.
- **Table 2:** 142 `add_es_system` calls, 139 distinct systems (three called in two device arms), every one with its `config/emulators/<system>.conf`.
- **No emulator, or no default:** `st-v` has no emulator on four built devices and `psx` no default on the VM (F-05). There are no two-default systems (F-06's case B is latent).
- **Table 3:** all 24 `sources/*.sh` are installed on at least one built device (`Install Steam.sh` on SM8550 alone).
- **Table 4:** ten of the fifteen `sources/<DEVICE>/` sets are for devices the fork does not build, kept for upstream, a row each.
- **Table 5:** every patch with the files it touches.
- **The tokens:** the five the table emits and the five the interface also expands. The latter are emitted by no shipped system (`grep -c` over the five tables: 0 each), so they are reachable only through a player's own overlay (T2's FD-3).
- **Dead units inside reached files:** F-01 (`--gated`), F-02 (`BOOTROMS_DIR`), F-12 (24 or 25 profile keys per device), F-14 (0017's step engages on no shipped profile; P3), F-18 (`X64_SKIP_CORES` names a closed issue), F-23 (`Install Steam.sh`'s dead assignments), and `/etc/retroarch.cfg`, read by no script.

#### Q6: the five reachability tables

##### Table 1: the `*-lr` recipes (137) and the built devices whose image carries them

Cells: `listed` (in the metapackage's `LIBRETRO_CORES`, `EMUS_32BIT` or `PKG_EMUS` for that device), `dep` (carried through another recipe's dependency), `-` (not carried). Source: the inventory's `reachable_by` and `buildable_by`; check: the metapackage's lists evaluated per device.

| Recipe | Membership | H700 | RK3326 | RK3566 | SM8550 | GENERIC_X64 |
| --- | --- | --- | --- | --- | --- | --- |
| `81-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `a5200-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `arduous-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `atari800-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `b2-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-gba-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-lynx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-ngp-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-pce-fast-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-pce-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-pcfx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-psx-lr` | upstream-carried | - | - | - | listed | - |
| `beetle-saturn-lr` | upstream-carried | - | - | - | listed | - |
| `beetle-supafaust-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-supergrafx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-vb-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `beetle-wswan-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `bk-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `bluemsx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `boom3-lr` | T24's (outside) | - | - | - | - | - |
| `bsnes-hd-lr` | upstream-carried | - | - | - | listed | - |
| `bsnes-lr` | upstream-carried | - | - | - | listed | - |
| `bsnes-mercury-accuracy-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `bsnes-mercury-balanced-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `bsnes-mercury-performance-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `bsnes2014-accuracy-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `bsnes2014-balanced-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `bsnes2014-performance-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `cap32-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `crocods-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `daphne-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `desmume-lr` | fork-own | listed | listed | listed | listed | - |
| `dolphin-lr` | upstream-carried | - | - | listed | listed | - |
| `dosbox-core-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `dosbox-pure-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `doublecherrygb-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `duckstation-lr` | upstream-carried | listed | listed | listed | listed | - |
| `easyrpg-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `ecwolf-lr` | upstream-carried | dep | dep | dep | dep | - |
| `emuscv-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `fake08-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `fbalpha2012-lr` | fork-own | listed | listed | listed | listed | listed |
| `fbalpha2019-lr` | fork-own | listed | listed | listed | listed | listed |
| `fbneo-lr` | fork-own | listed | listed | listed | listed | listed |
| `fceumm-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `flycast-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `flycast2021-lr` | upstream-carried | listed | listed | listed | listed | - |
| `fmsx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `freechaf-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `freeintv-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `freej2me-lr` | fork-own | listed | listed | listed | listed | listed |
| `fuse-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `gambatte-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `gearboy-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `gearcoleco-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `geargrafx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `gearlynx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `gearsystem-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `genesis-plus-gx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `genesis-plus-gx-wide-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `geolith-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `gpsp-lr` | fork-own | listed | listed | listed | listed | - |
| `gw-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `handy-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `hatari-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `idtech-lr` | fork-own | listed | listed | listed | listed | - |
| `jaxe-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `kronos-lr` | upstream-carried | - | - | - | listed | - |
| `mame-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `mame2003-lr` | T24's (outside) | - | - | - | - | - |
| `mame2003-plus-lr` | fork-own | listed | listed | listed | listed | listed |
| `mame2010-lr` | fork-own | listed | listed | listed | listed | listed |
| `mame2015-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `melonds-ds-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `melonds-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `mesen-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `mesen-s-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `mgba-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `minivmac-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `mojozork-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `mu-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `mupen64plus-lr` | fork-own | listed | listed | listed | listed | listed |
| `mupen64plus-nx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `neocd_lr` | upstream-carried | listed | listed | listed | listed | listed |
| `nestopia-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `np2kai-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `o2em-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `opera-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `panda3ds-lr` | T24's (outside) | - | - | - | - | - |
| `parallel-n64-lr` | upstream-carried | listed | listed | listed | listed | - |
| `pcsx_rearmed-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `picodrive-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `play-lr` | T24's (outside) | - | - | - | - | - |
| `pokemini-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `potator-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `ppsspp-lr` | fork-own | listed | listed | listed | listed | - |
| `prboom-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `prosystem-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `puae-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `puae2021-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `px68k-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `quasi88-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `quicknes-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `race-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `same_cdi-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `sameboy-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `sameduck-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `scummvm-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `skyemu-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `smsplus-gx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `snes9x-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `snes9x2002-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `snes9x2005_plus-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `snes9x2010-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `stella-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `supersnes9x-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `swanstation-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `tgbdual-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `theodore-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `tic80-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `tyrquake-lr` | upstream-carried | dep | dep | dep | dep | - |
| `uae4arm-lr` | upstream-carried | listed | listed | listed | listed | - |
| `uzem-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `vba-next-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `vbam-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `vecx-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `vice-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `vircon32-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `virtualjaguar-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `vitaquake2-lr` | upstream-carried | dep | dep | dep | dep | - |
| `vitaquake2-rogue-lr` | upstream-carried | dep | dep | dep | dep | - |
| `vitaquake2-xatrix-lr` | upstream-carried | dep | dep | dep | dep | - |
| `vitaquake2-zaero-lr` | upstream-carried | dep | dep | dep | dep | - |
| `vitaquake3-lr` | T24's (outside) | - | - | - | - | - |
| `wasm4-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `xmil-lr` | upstream-carried | listed | listed | listed | listed | listed |
| `yabasanshiro-lr` | upstream-carried | listed | listed | listed | listed | listed |

137 recipes (132 in the membership); carried by no built device: 5 (`boom3-lr`, `mame2003-lr`, `panda3ds-lr`, `play-lr`, `vitaquake3-lr`); listed for a device but not in the inventory's set: 0 (none).

##### Table 2: the `add_es_system` calls (142; 139 distinct systems)

| System | `.conf` | H700 | RK3326 | RK3566 | SM8550 | GENERIC_X64 |
| --- | --- | --- | --- | --- | --- | --- |
| `3do` | yes | 1e/1c, default opera | 1e/1c, default opera | 1e/1c, default opera | 1e/1c, default opera | 1e/1c, default opera |
| `3ds` | yes | - | - | 1e/1c, default azahar-sa | 1e/1c, default azahar-sa | - |
| `amiga` | yes | 2e/4c, default puae2021 | 2e/4c, default puae2021 | 2e/4c, default puae2021 | 2e/4c, default puae2021 | 2e/3c, default puae |
| `amigacd32` | yes | 1e/3c, default puae2021 | 1e/3c, default puae2021 | 1e/3c, default puae2021 | 1e/3c, default puae2021 | 1e/3c, default puae |
| `amstradcpc` | yes | 1e/2c, default crocods | 1e/2c, default crocods | 1e/2c, default crocods | 1e/2c, default crocods | 1e/2c, default crocods |
| `arcade` | yes | 1e/7c, default mame2003_plus | 1e/7c, default mame2003_plus | 1e/7c, default mame2003_plus | 2e/8c, default mame2003_plus | 1e/7c, default mame2003_plus |
| `arduboy` | yes | 1e/1c, default arduous | 1e/1c, default arduous | 1e/1c, default arduous | 1e/1c, default arduous | 1e/1c, default arduous |
| `atari2600` | yes | 1e/1c, default stella | 1e/1c, default stella | 1e/1c, default stella | 1e/1c, default stella | 1e/1c, default stella |
| `atari5200` | yes | 1e/2c, default a5200 | 1e/2c, default a5200 | 1e/2c, default a5200 | 1e/2c, default a5200 | 1e/2c, default a5200 |
| `atari7800` | yes | 1e/1c, default prosystem | 1e/1c, default prosystem | 1e/1c, default prosystem | 1e/1c, default prosystem | 1e/1c, default prosystem |
| `atari800` | yes | 1e/1c, default atari800 | 1e/1c, default atari800 | 1e/1c, default atari800 | 1e/1c, default atari800 | 1e/1c, default atari800 |
| `atarijaguar` | yes | 1e/1c, default virtualjaguar | 1e/1c, default virtualjaguar | 1e/1c, default virtualjaguar | 2e/2c, default virtualjaguar | 1e/1c, default virtualjaguar |
| `atarilynx` | yes | 2e/4c, default handy | 2e/4c, default handy | 2e/4c, default handy | 2e/4c, default handy | 1e/3c, default handy |
| `atarist` | yes | 2e/2c, default hatari | 2e/2c, default hatari | 2e/2c, default hatari | 2e/2c, default hatari | 2e/2c, default hatari |
| `atomiswave` | yes | 2e/3c, default flycast2021 | 2e/3c, default flycast2021 | 2e/3c, default flycast2021 | 2e/3c, default flycast-sa | 2e/2c, default flycast |
| `bbcmicro` | yes | 1e/1c, default b2 | 1e/1c, default b2 | 1e/1c, default b2 | 1e/1c, default b2 | 1e/1c, default b2 |
| `bk` | yes | 1e/1c, default bk | 1e/1c, default bk | 1e/1c, default bk | 1e/1c, default bk | 1e/1c, default bk |
| `c128` | yes | 2e/2c, default vice_x128 | 2e/2c, default vice_x128 | 2e/2c, default vice_x128 | 2e/2c, default vice_x128 | 2e/2c, default vice_x128 |
| `c16` | yes | 2e/2c, default vice_xplus4 | 2e/2c, default vice_xplus4 | 2e/2c, default vice_xplus4 | 2e/2c, default vice_xplus4 | 2e/2c, default vice_xplus4 |
| `c64` | yes | 2e/2c, default vice_x64 | 2e/2c, default vice_x64 | 2e/2c, default vice_x64 | 2e/2c, default vice_x64 | 2e/2c, default vice_x64 |
| `cdi` | yes | 1e/1c, default same_cdi | 1e/1c, default same_cdi | 1e/1c, default same_cdi | 1e/1c, default same_cdi | 1e/1c, default same_cdi |
| `channelf` | yes | 1e/1c, default freechaf | 1e/1c, default freechaf | 1e/1c, default freechaf | 1e/1c, default freechaf | 1e/1c, default freechaf |
| `chip-8` | yes | 1e/1c, default jaxe | 1e/1c, default jaxe | 1e/1c, default jaxe | 1e/1c, default jaxe | 1e/1c, default jaxe |
| `colecovision` | yes | 1e/3c, default gearcoleco | 1e/3c, default gearcoleco | 1e/3c, default gearcoleco | 2e/4c, default gearcoleco | 1e/3c, default gearcoleco |
| `cps1` | yes | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo |
| `cps2` | yes | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo |
| `cps3` | yes | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo | 2e/5c, default fbneo |
| `daphne` | yes | 2e/2c, default hypseus-singe | 2e/2c, default hypseus-singe | 2e/2c, default hypseus-singe | 2e/2c, default hypseus-singe | 2e/2c, default hypseus-singe |
| `doom` | yes | 2e/2c, default gzdoom-sa | 2e/2c, default gzdoom-sa | 2e/2c, default gzdoom-sa | 2e/2c, default gzdoom-sa | 2e/2c, default gzdoom-sa |
| `dreamcast` | yes | 2e/3c, default flycast2021 | 2e/3c, default flycast2021 | 2e/3c, default flycast2021 | 2e/3c, default flycast-sa | 2e/2c, default flycast |
| `easyrpg` | yes | 1e/1c, default easyrpg | 1e/1c, default easyrpg | 1e/1c, default easyrpg | 1e/1c, default easyrpg | 1e/1c, default easyrpg |
| `famicom` | yes | 2e/5c, default nestopia | 2e/5c, default nestopia | 2e/5c, default nestopia | 3e/6c, default nestopia | 1e/4c, default nestopia |
| `fbn` | yes | 1e/7c, default fbneo | 1e/7c, default fbneo | 1e/7c, default fbneo | 1e/7c, default fbneo | 1e/7c, default fbneo |
| `fds` | yes | 2e/5c, default nestopia | 2e/5c, default nestopia | 2e/5c, default nestopia | 3e/6c, default nestopia | 1e/4c, default nestopia |
| `gameandwatch` | yes | 1e/2c, default gw | 1e/2c, default gw | 1e/2c, default gw | 1e/2c, default gw | 1e/2c, default gw |
| `gamecube` | yes | - | - | 2e/3c, default dolphin-sa-gc | 2e/3c, default dolphin-sa-gc | 1e/2c, default dolphin-sa-gc |
| `gamegear` | yes | 2e/5c, default gearsystem | 2e/5c, default gearsystem | 2e/5c, default gearsystem | 3e/6c, default gearsystem | 1e/4c, default gearsystem |
| `gb` | yes | 2e/11c, default gambatte | 2e/11c, default gambatte | 2e/11c, default gambatte | 4e/14c, default gambatte | 1e/10c, default gambatte |
| `gba` | yes | 2e/7c, default mgba | 2e/7c, default mgba | 2e/7c, default mgba | 5e/10c, default mgba | 1e/5c, default mgba |
| `gbah` | yes | 2e/7c, default mgba | 2e/7c, default mgba | 2e/7c, default mgba | 4e/9c, default mgba | 1e/5c, default mgba |
| `gbav` | yes | 2e/7c, default mgba | 2e/7c, default mgba | 2e/7c, default mgba | 3e/8c, default mgba | 1e/5c, default mgba |
| `gbc` | yes | 2e/10c, default gambatte | 2e/10c, default gambatte | 2e/10c, default gambatte | 4e/12c, default gambatte | 1e/9c, default gambatte |
| `gbch` | yes | 2e/10c, default gambatte | 2e/10c, default gambatte | 2e/10c, default gambatte | 4e/12c, default gambatte | 1e/9c, default gambatte |
| `gbh` | yes | 2e/11c, default gambatte | 2e/11c, default gambatte | 2e/11c, default gambatte | 4e/14c, default gambatte | 1e/10c, default gambatte |
| `genesis` | yes | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 3e/5c, default genesis_plus_gx | 1e/3c, default genesis_plus_gx |
| `genh` | yes | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 3e/5c, default genesis_plus_gx | 1e/3c, default genesis_plus_gx |
| `ggh` | yes | 2e/5c, default gearsystem | 2e/5c, default gearsystem | 2e/5c, default gearsystem | 3e/6c, default gearsystem | 1e/4c, default gearsystem |
| `gp32` | yes | 1e/1c, default mame | 1e/1c, default mame | 1e/1c, default mame | 1e/1c, default mame | 1e/1c, default mame |
| `heroic` | yes | - | - | - | 1e/1c, default heroic | - |
| `idtech` | yes | 1e/1c, default idtech | 1e/1c, default idtech | 1e/1c, default idtech | 1e/1c, default idtech | 1e/1c, default idtech |
| `imageviewer` | yes | 0e/0c, default NONE | 0e/0c, default NONE | 0e/0c, default NONE | 0e/0c, default NONE | 0e/0c, default NONE |
| `intellivision` | yes | 1e/1c, default freeintv | 1e/1c, default freeintv | 1e/1c, default freeintv | 1e/1c, default freeintv | 1e/1c, default freeintv |
| `ios` | yes | 1e/1c, default touchhle-sa | 1e/1c, default touchhle-sa | 1e/1c, default touchhle-sa | 1e/1c, default touchhle-sa | 1e/1c, default touchhle-sa |
| `j2me` | yes | 1e/1c, default freej2me | 1e/1c, default freej2me | 1e/1c, default freej2me | 1e/1c, default freej2me | 1e/1c, default freej2me |
| `macintosh` | yes | 1e/1c, default minivmac | 1e/1c, default minivmac | 1e/1c, default minivmac | 1e/1c, default minivmac | 1e/1c, default minivmac |
| `mame` | yes | 1e/7c, default mame2003_plus | 1e/7c, default mame2003_plus | 1e/7c, default mame2003_plus | 1e/7c, default mame2003_plus | 1e/7c, default mame2003_plus |
| `mastersystem` | yes | 2e/5c, default gearsystem | 2e/5c, default gearsystem | 2e/5c, default gearsystem | 3e/6c, default gearsystem | 1e/4c, default gearsystem |
| `megacd` | yes | 1e/2c, default genesis_plus_gx | 1e/2c, default genesis_plus_gx | 1e/2c, default genesis_plus_gx | 2e/3c, default genesis_plus_gx | 1e/2c, default genesis_plus_gx |
| `megadrive` | yes | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 1e/3c, default genesis_plus_gx |
| `megadrive-japan` | yes | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 1e/3c, default genesis_plus_gx |
| `megadriveh` | yes | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 2e/4c, default genesis_plus_gx | 1e/3c, default genesis_plus_gx |
| `megaduck` | yes | 1e/1c, default sameduck | 1e/1c, default sameduck | 1e/1c, default sameduck | 1e/1c, default sameduck | 1e/1c, default sameduck |
| `moonlight` | yes | 1e/1c, default moonlight | 1e/1c, default moonlight | 1e/1c, default moonlight | 1e/1c, default moonlight | 1e/1c, default moonlight |
| `moto` | yes | 1e/1c, default theodore | 1e/1c, default theodore | 1e/1c, default theodore | 1e/1c, default theodore | 1e/1c, default theodore |
| `mplayer` | yes | 2e/2c, default mplayer | 2e/2c, default mplayer | 2e/2c, default mplayer | 2e/2c, default mplayer | 2e/2c, default mplayer |
| `msx` | yes | 1e/2c, default bluemsx | 1e/2c, default bluemsx | 1e/2c, default bluemsx | 2e/3c, default bluemsx | 1e/2c, default bluemsx |
| `msx2` | yes | 1e/2c, default bluemsx | 1e/2c, default bluemsx | 1e/2c, default bluemsx | 1e/2c, default bluemsx | 1e/2c, default bluemsx |
| `music` | yes | 1e/1c, default gmu | 1e/1c, default gmu | 1e/1c, default gmu | 1e/1c, default gmu | 1e/1c, default gmu |
| `n64` | yes | 2e/4c, default mupen64plus_next | 2e/4c, default mupen64plus_next | 2e/4c, default mupen64plus_next | 5e/6c, default mupen64plus_next | 2e/3c, default mupen64plus_next |
| `n64dd` | yes | 2e/3c, default mupen64plus_next | 2e/3c, default mupen64plus_next | 2e/3c, default mupen64plus_next | 3e/4c, default mupen64plus_next | 2e/3c, default mupen64plus_next |
| `naomi` | yes | 2e/3c, default flycast2021 | 2e/3c, default flycast2021 | 2e/3c, default flycast2021 | 2e/3c, default flycast-sa | 2e/2c, default flycast |
| `nds` | yes | 3e/6c, default drastic-sa | 3e/6c, default drastic-sa | 4e/7c, default drastic-sa | 5e/8c, default melonds-sa | 3e/5c, default drastic-sa |
| `ndsiware` | yes | 2e/2c, default melondsds | 2e/2c, default melondsds | 3e/3c, default melondsds | 3e/3c, default melondsds | 3e/3c, default melondsds |
| `neocd` | yes | 1e/3c, default neocd | 1e/3c, default neocd | 1e/3c, default neocd | 1e/3c, default neocd | 1e/3c, default neocd |
| `neogeo` | yes | 1e/8c, default fbneo | 1e/8c, default fbneo | 1e/8c, default fbneo | 2e/9c, default fbneo | 1e/8c, default fbneo |
| `nes` | yes | 2e/5c, default nestopia | 2e/5c, default nestopia | 2e/5c, default nestopia | 3e/6c, default nestopia | 1e/4c, default nestopia |
| `nesh` | yes | 2e/5c, default nestopia | 2e/5c, default nestopia | 2e/5c, default nestopia | 3e/6c, default nestopia | 1e/4c, default nestopia |
| `ngp` | yes | 2e/3c, default beetle_ngp | 2e/3c, default beetle_ngp | 2e/3c, default beetle_ngp | 3e/4c, default beetle_ngp | 1e/2c, default beetle_ngp |
| `ngpc` | yes | 2e/3c, default beetle_ngp | 2e/3c, default beetle_ngp | 2e/3c, default beetle_ngp | 3e/4c, default beetle_ngp | 1e/2c, default beetle_ngp |
| `odyssey2` | yes | 1e/1c, default o2em | 1e/1c, default o2em | 1e/1c, default o2em | 1e/1c, default o2em | 1e/1c, default o2em |
| `openbor` | yes | 1e/1c, default OpenBOR | 1e/1c, default OpenBOR | 1e/1c, default OpenBOR | 1e/1c, default OpenBOR | 1e/1c, default OpenBOR |
| `palm` | yes | 1e/1c, default mu | 1e/1c, default mu | 1e/1c, default mu | 1e/1c, default mu | 1e/1c, default mu |
| `pc` | yes | 1e/2c, default dosbox_pure | 1e/2c, default dosbox_pure | 1e/2c, default dosbox_pure | 1e/2c, default dosbox_pure | 1e/2c, default dosbox_pure |
| `pc-8800` | yes | 1e/1c, default quasi88 | 1e/1c, default quasi88 | 1e/1c, default quasi88 | 1e/1c, default quasi88 | 1e/1c, default quasi88 |
| `pc-9800` | yes | 1e/1c, default np2kai | 1e/1c, default np2kai | 1e/1c, default np2kai | 1e/1c, default np2kai | 1e/1c, default np2kai |
| `pcengine` | yes | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 3e/7c, default beetle_pce_fast | 1e/4c, default beetle_pce_fast |
| `pcenginecd` | yes | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 3e/7c, default beetle_pce_fast | 1e/4c, default beetle_pce_fast |
| `pcfx` | yes | 2e/2c, default beetle_pcfx | 2e/2c, default beetle_pcfx | 2e/2c, default beetle_pcfx | 2e/2c, default beetle_pcfx | 1e/1c, default beetle_pcfx |
| `pet` | yes | 1e/1c, default vice_xpet | 1e/1c, default vice_xpet | 1e/1c, default vice_xpet | 1e/1c, default vice_xpet | 1e/1c, default vice_xpet |
| `pico-8` | yes | 2e/2c, default pico8 | 2e/2c, default pico8 | 2e/2c, default pico8 | 2e/2c, default pico8 | 2e/2c, default pico8 |
| `pokemini` | yes | 1e/1c, default pokemini | 1e/1c, default pokemini | 1e/1c, default pokemini | 1e/1c, default pokemini | 1e/1c, default pokemini |
| `ports` | yes | 1e/1c, default portmaster | 1e/1c, default portmaster | 1e/1c, default portmaster | 1e/1c, default portmaster | 1e/1c, default portmaster |
| `ps2` | yes | - | - | 2e/2c, default armsx2-sa | 2e/2c, default armsx2-sa | - |
| `ps3` | yes | - | - | - | 1e/1c, default rpcs3-sa | - |
| `psp` | yes | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa |
| `pspminis` | yes | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa | 2e/2c, default ppsspp-sa |
| `psvita` | yes | - | - | 1e/1c, default vita3k-sa | 1e/1c, default vita3k-sa | - |
| `psx` | yes | 2e/5c, default pcsx_rearmed32 | 2e/5c, default pcsx_rearmed32 | 2e/5c, default pcsx_rearmed32 | 3e/7c, default pcsx_rearmed32 | 2e/2c, default NONE |
| `satellaview` | yes | 1e/6c, default snes9x | 1e/6c, default snes9x | 1e/6c, default snes9x | 2e/7c, default snes9x | 1e/6c, default snes9x |
| `saturn` | yes | 2e/2c, default yabasanshiro-sa | 2e/2c, default yabasanshiro-sa | 2e/2c, default yabasanshiro-sa | 3e/5c, default yabasanshiro-sa | 2e/2c, default yabasanshiro-sa |
| `scummvm` | yes | 2e/2c, default scummvm | 2e/2c, default scummvm | 2e/2c, default scummvm | 2e/2c, default scummvm | 2e/2c, default scummvm |
| `scv` | yes | 1e/1c, default emuscv | 1e/1c, default emuscv | 1e/1c, default emuscv | 1e/1c, default emuscv | 1e/1c, default emuscv |
| `sega32x` | yes | 1e/1c, default picodrive | 1e/1c, default picodrive | 1e/1c, default picodrive | 2e/2c, default picodrive | 1e/1c, default picodrive |
| `segacd` | yes | 1e/2c, default genesis_plus_gx | 1e/2c, default genesis_plus_gx | 1e/2c, default genesis_plus_gx | 2e/3c, default genesis_plus_gx | 1e/2c, default genesis_plus_gx |
| `segamodel3` | yes | - | - | - | 1e/1c, default supermodel-sa | - |
| `sfc` | yes | 2e/14c, default snes9x | 2e/14c, default snes9x | 2e/14c, default snes9x | 3e/17c, default snes9x | 1e/13c, default snes9x |
| `sg-1000` | yes | 1e/3c, default gearsystem | 1e/3c, default gearsystem | 1e/3c, default gearsystem | 2e/4c, default gearsystem | 1e/3c, default gearsystem |
| `snes` | yes | 2e/14c, default snes9x | 2e/14c, default snes9x | 2e/14c, default snes9x | 3e/17c, default snes9x | 1e/13c, default snes9x |
| `snesh` | yes | 2e/14c, default snes9x | 2e/14c, default snes9x | 2e/14c, default snes9x | 3e/17c, default snes9x | 1e/13c, default snes9x |
| `snesmsu1` | yes | 2e/4c, default snes9x | 2e/4c, default snes9x | 2e/4c, default snes9x | 2e/4c, default snes9x | 1e/3c, default snes9x |
| `st-v` | yes | 0e/0c, default NONE | 0e/0c, default NONE | 0e/0c, default NONE | 1e/1c, default ss | 0e/0c, default NONE |
| `steam` | yes | - | - | - | 1e/1c, default steam | - |
| `sufami` | yes | 1e/2c, default snes9x | 1e/2c, default snes9x | 1e/2c, default snes9x | 2e/3c, default snes9x | 1e/2c, default snes9x |
| `supergrafx` | yes | 2e/5c, default beetle_supergrafx | 2e/5c, default beetle_supergrafx | 2e/5c, default beetle_supergrafx | 3e/6c, default beetle_supergrafx | 1e/3c, default beetle_supergrafx |
| `supervision` | yes | 1e/1c, default potator | 1e/1c, default potator | 1e/1c, default potator | 1e/1c, default potator | 1e/1c, default potator |
| `tg16` | yes | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 1e/4c, default beetle_pce_fast |
| `tg16cd` | yes | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 2e/6c, default beetle_pce_fast | 1e/4c, default beetle_pce_fast |
| `tic-80` | yes | 1e/1c, default tic80 | 1e/1c, default tic80 | 1e/1c, default tic80 | 1e/1c, default tic80 | 1e/1c, default tic80 |
| `tools` | yes | 0e/0c, default NONE | 0e/0c, default NONE | 0e/0c, default NONE | 0e/0c, default NONE | 0e/0c, default NONE |
| `triforce` | yes | - | - | - | 1e/2c, default dolphin-sa-gc | - |
| `uzebox` | yes | 1e/1c, default uzem | 1e/1c, default uzem | 1e/1c, default uzem | 1e/1c, default uzem | 1e/1c, default uzem |
| `vectrex` | yes | 1e/1c, default vecx | 1e/1c, default vecx | 1e/1c, default vecx | 1e/1c, default vecx | 1e/1c, default vecx |
| `vic20` | yes | 2e/2c, default vice_xvic | 2e/2c, default vice_xvic | 2e/2c, default vice_xvic | 2e/2c, default vice_xvic | 2e/2c, default vice_xvic |
| `videopac` | yes | 1e/1c, default o2em | 1e/1c, default o2em | 1e/1c, default o2em | 1e/1c, default o2em | 1e/1c, default o2em |
| `vircon32` | yes | 1e/1c, default vircon32 | 1e/1c, default vircon32 | 1e/1c, default vircon32 | 1e/1c, default vircon32 | 1e/1c, default vircon32 |
| `virtualboy` | yes | 2e/2c, default beetle_vb | 2e/2c, default beetle_vb | 2e/2c, default beetle_vb | 2e/2c, default beetle_vb | 1e/1c, default beetle_vb |
| `wasm4` | yes | 1e/1c, default wasm4 | 1e/1c, default wasm4 | 1e/1c, default wasm4 | 1e/1c, default wasm4 | 1e/1c, default wasm4 |
| `wii` | yes | - | - | 2e/3c, default dolphin-sa-wii | 2e/3c, default dolphin-sa-wii | 1e/2c, default dolphin-sa-wii |
| `wiiu` | yes | - | - | - | 1e/1c, default cemu-sa | - |
| `wiiware` | yes | - | - | 2e/3c, default dolphin-sa-wii | 2e/3c, default dolphin-sa-wii | - |
| `windows` | yes | 1e/1c, default wine | 1e/1c, default wine | 1e/1c, default wine | 1e/1c, default wine | 1e/1c, default wine |
| `wonderswan` | yes | 2e/2c, default beetle_wswan | 2e/2c, default beetle_wswan | 2e/2c, default beetle_wswan | 3e/3c, default beetle_wswan | 1e/1c, default beetle_wswan |
| `wonderswancolor` | yes | 2e/2c, default beetle_wswan | 2e/2c, default beetle_wswan | 2e/2c, default beetle_wswan | 3e/3c, default beetle_wswan | 1e/1c, default beetle_wswan |
| `x1` | yes | 1e/1c, default x1 | 1e/1c, default x1 | 1e/1c, default x1 | 1e/1c, default x1 | 1e/1c, default x1 |
| `x68000` | yes | 1e/1c, default px68k | 1e/1c, default px68k | 1e/1c, default px68k | 1e/1c, default px68k | 1e/1c, default px68k |
| `xbox` | yes | - | - | - | 1e/1c, default xemu-sa | - |
| `zmachine` | yes | 1e/1c, default mojozork | 1e/1c, default mojozork | 1e/1c, default mojozork | 1e/1c, default mojozork | 1e/1c, default mojozork |
| `zx81` | yes | 1e/1c, default 81 | 1e/1c, default 81 | 1e/1c, default 81 | 1e/1c, default 81 | 1e/1c, default 81 |
| `zxspectrum` | yes | 1e/1c, default fuse | 1e/1c, default fuse | 1e/1c, default fuse | 2e/2c, default fuse | 1e/1c, default fuse |

Systems without a `.conf`: none. Systems per regenerated table: H700 126, RK3326 126, RK3566 132, SM8550 139, GENERIC_X64 128.

##### Table 3: `virtual/emulators/sources/*.sh` (24) and the devices that install them

| Script | H700 | RK3326 | RK3566 | SM8550 | GENERIC_X64 |
| --- | --- | --- | --- | --- | --- |
| `Install Heroic Games Launcher.sh` | - | - | - | yes | - |
| `Install Steam.sh` | - | - | - | yes | - |
| `Scan Heroic Games.sh` | - | - | - | yes | - |
| `Scan ScummVM Games.sh` | yes | yes | yes | yes | yes |
| `Scan id Tech Games.sh` | yes | yes | yes | yes | yes |
| `Start ARMSX2.sh` | - | - | yes | yes | - |
| `Start AetherSX2.sh` | - | - | yes | yes | - |
| `Start Azahar.sh` | - | - | yes | yes | - |
| `Start BigPEmu.sh` | - | - | - | yes | - |
| `Start CEMU.sh` | - | - | - | yes | - |
| `Start DaedalusX64.sh` | - | - | - | yes | - |
| `Start Dolphin.sh` | - | - | yes | yes | yes |
| `Start Flycast.sh` | yes | yes | yes | yes | yes |
| `Start HATARISA.sh` | yes | yes | yes | yes | yes |
| `Start MelonDS.sh` | - | - | yes | yes | - |
| `Start PPSSPP.sh` | yes | yes | yes | yes | yes |
| `Start RPCS3.sh` | - | - | - | yes | - |
| `Start ScummVM.sh` | yes | yes | yes | yes | yes |
| `Start SkyEmu.sh` | - | - | - | yes | - |
| `Start Vita3K.sh` | - | - | yes | yes | - |
| `Start Xemu.sh` | - | - | - | yes | - |
| `Start touchHLE.sh` | yes | yes | yes | yes | yes |
| `Uninstall Heroic Games Launcher.sh` | - | - | - | yes | - |
| `Uninstall Steam.sh` | - | - | - | yes | - |

Installed on no built device: 0 (none).

##### Table 4: `retroarch/sources/<DEVICE>/` (15)

| Set | Files | The fork builds it |
| --- | ---: | --- |
| `AMD64` | 5 | no (kept for upstream) |
| `GENERIC_X64` | 4 | yes |
| `H700` | 5 | yes |
| `RK3326` | 5 | yes |
| `RK3399` | 5 | no (kept for upstream) |
| `RK3566` | 5 | yes |
| `RK3576` | 5 | no (kept for upstream) |
| `RK3588` | 5 | no (kept for upstream) |
| `S922X` | 5 | no (kept for upstream) |
| `SM4450` | 5 | no (kept for upstream) |
| `SM6115` | 5 | no (kept for upstream) |
| `SM8250` | 5 | no (kept for upstream) |
| `SM8550` | 5 | yes |
| `SM8650` | 5 | no (kept for upstream) |
| `SM8750` | 5 | no (kept for upstream) |

##### Table 5: the RetroArch patches (21) and the sources they touch at the pin

| Patch | Files |
| --- | --- |
| `0001-Increase-glui-size.patch` | `menu/drivers/materialui.c
` |
| `0001-Increase-ozone-size.patch` | `menu/drivers/ozone.c
` |
| `0001-Increase-ozone-widget_size.patch` | `gfx/gfx_widgets.c
` |
| `0002-quit-not-restart.patch` | `menu/menu_setting.c` |
| `0003-fix-oga-no-preferred.patch` | `deps/libgo2/src/display.c
`, `gfx/drivers/oga_gfx.c
` |
| `0004-drm-resolution.patch` | `gfx/common/drm_common.c
` |
| `0006-no-screen-brightness.patch` | `frontend/drivers/platform_unix.c` |
| `0008-disable_search.patch` | `menu/menu_driver.c
` |
| `0009-hide-wayland-checkerboard.patch` | `gfx/drivers/vulkan.c
` |
| `0010-paths.patch` | `frontend/drivers/platform_unix.c
` |
| `0011-cheevos-sounds.patch` | `audio/audio_driver.c
`, `configuration.c
`, `configuration.h
` |
| `0011-video-thread-wrapper-serialise-posters.patch` | `gfx/video_thread_wrapper.c`, `gfx/video_thread_wrapper.h` |
| `0012-cheevos-cmd.patch` | `cheevos/cheevos.c
`, `configuration.c
`, `configuration.h
` |
| `0013-cheevos-offline-proxy-toast.patch` | `cheevos/cheevos.c
`, `cheevos/cheevos_client.c
`, `cheevos/cheevos_locals.h
`, `intl/msg_hash_fr.h
`, `intl/msg_hash_us.h
`, `msg_hash.h
` |
| `0014-widgets-backdrop-follows-the-font.patch` | `gfx/gfx_widgets.c
` |
| `0015-video-thread-wrapper-run-a-command-once.patch` | `gfx/video_thread_wrapper.c
` |
| `0016-widgets-message-queue-floor.patch` | `gfx/gfx_widgets.c
` |
| `0017-widgets-sharp-font-sizes.patch` | `gfx/gfx_widgets.c
` |
| `0018-auto-slot-survives-content-load.patch` | `command.c
`, `command.h
`, `configuration.c
`, `runtime_file.c
` |
| `0019-widgets-message-queue-keeps-its-place.patch` | `gfx/gfx_widgets.c
`, `gfx/gfx_widgets.h
` |
| `batteryplus/0001-batteryplus-capacity.patch` | `frontend/drivers/platform_unix.c
` |

### Q7 Clarity and structure

- `virtual/emulators/package.mk`'s 1,630-line `makeinstall_target`. Its README comment claims a check that does not exist (F-06).
- `X64_SKIP_CORES`' comment names a closed issue (F-18).
- The rotation hook is written out five times (F-17).
- The fifteen profiles: SM4450, SM8250 and SM8550 are byte-identical, and SM8650 and SM8750 differ from them by 2 lines; GENERIC_X64 against H700 differs in 89 keys. Copies with no base.
- `Install Steam.sh`'s copies and comments (F-23).
- `retroarch/package.mk`'s duplicated `libass` and unexplained `empty` dependency.
- Three RetroArch patches share the `0001` prefix and there is no `0005` or `0007` (upstream's numbering).

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

| Finding | Would have been caught by | Uncovered? |
| --- | --- | --- |
| F-02 | `packaging-and-patches.md` § Late binding (and `pkgcheck`, which did catch it) | — |
| F-08 (#802), F-09 | `device-builds.md` § Late binding bites hardest in a merge (a fork-added block read during a merge), only partly: neither rule asks that a table's named core exist where the launcher loads it | **YES** for the table-against-image check |
| F-15 | `device-builds.md` § A build that fetches its own dependency (it names cmake's `FetchContent` as having no switch), but no tool reads for it | — (rule exists, no tool) |
| F-16 | `CLAUDE.md` § package.mk rules, full-hash pin | — |
| F-19 (#806) | `packaging-and-patches.md` § A shipped script's tools are dependencies too, which covers a missing tool, not a tool built without a feature | **YES** |
| F-06, F-18, F-12 (`content_history_dir`) | `engineering-practices.md` § A name is not a behaviour | — |
| F-11 | `engineering-practices.md` § Guards must fail closed | — |
| F-20, F-21 | none for network data in fork shell scripts | **YES** |

### Codification Gaps (needs-new-rule)

| Pattern | Instances | Recommendation |
| --- | --- | --- |
| P-01: what one part of the build produces is not checked against what another part expects of it | F-08 (the table names a core the image does not place), F-19 (a script needs a grep feature the build may drop), F-09 (a merge brings paths the fork renamed) | **Extend** `device-builds.md` with a section "A consumer's expectation is checked against the image", and make it a tool: (1) every `<core>` of an arm-enabled image's `es_systems.cfg` has `usr/lib/libretro/<core>_libretro.so` (minus the non-libretro emulators); (2) the merged tree's `git grep -F 'build.${DISTRO}-'` is empty; (3) a feature define list (`config.h` `HAVE_*`) per package compared across device roots |
| P-02: a payload fetched by a shipped script, or by a build, without a pin or a checksum | F-15, F-21, and `idtech-lr` before `63a2090a56` | **Extend** `packaging-and-patches.md`: a recipe or shipped script that downloads at build or run time names its pin and checksum, or says why it cannot |
| P-03: a comment or a usage line that claims a check or a mode that does not exist | F-01, F-06, F-18 | already `engineering-practices.md` § A name is not a behaviour; no new rule; the fixes edit the comments |

### Recommended Action Sequence

1. The coordinator routes P-01's tool to the tooling area (it reads three slices' artifacts).
2. P-02's sentence goes into `packaging-and-patches.md` with the F-15 fix's stream.
3. P-03 needs nothing beyond the fixes.

## Second opinion (Phase 4.6)

**Completed 2026-10-24 05:58 UTC; graded by 06:10.** Extended depth, epic tier: one refutation pass per seat, on the same packet (`gpt-brief.md` = `gemini-argon-brief.md`, 308,850 bytes, sha256 `55ecef113c703cbf…`). Neither seat saw the other's output.

| Seat | Served (provider-observed) | Effort (reasoning tokens) | Provider | Time | Output |
| --- | --- | --- | --- | --- | --- |
| `gpt` | `openai/gpt-6-astra` | max (30,359) | OpenAI | 691.7 s | `second-opinions/gpt-audit.md`, 18,174 B |
| `gemini-argon` | `google/gemini-4-argon` | high (30,337) | Google | 424.9 s | `second-opinions/gemini-argon-audit.md`, 25,217 B |

**Preparation:**
- **Toolchain:** `npm install --prefix tools/council` (tsx v4.23.15, node v24.21.0); `verify-pins` OK; `test` 185/185.
- **Probes:** one per seat (`*-probe.md`), each PASS on identity, effort and provider.
- **Grading rule:** every seat item is a lead until it has been re-read at its artifact. The verdicts below name that artifact.

### Seat items: own findings

The seats' own finding numbers are given as Astra G-nn and Argon G-nn. **PL** is the punch item that carries each one.

| Seat item | Verdict | The artifact that decided it | PL |
| --- | --- | --- | --- |
| Astra G-01, Argon G-01: the table offers cores the image lacks | **CONFIRMED, narrowed; Low, not High.** The non-default GENERIC_X64 choices `uae4arm`, `parallel_n64` ×2 and `ppsspp` ×2 are missing, and so is `ffmpeg` on every image. `idtech` is a `.sh` system, which `runemu.sh:488` runs itself, so it is not a missing core. The idtech *scanner* is the defect: on GENERIC_X64 it calls a `generate-idtech.sh` the image lacks. Argon's `nds`/`desmume` part is refuted: `desmume_libretro.so` is installed. | Every `retroarch` `<core>` of the GENERIC_X64, H700 and SM8550 images' `es_systems.cfg` against their `usr/lib/libretro` (7, 3 and 3 missing); `runemu.sh:488-492`; `usr/bin/generate-idtech.sh` absent from GENERIC_X64's image | PL-030, PL-031 |
| Astra G-02: a single stale ARM install directory is copied | **CONFIRMED** (reading). Folded into F-11's fix: pin the directory to `${PKG_VERSION}`. | `retroarch/package.mk:106-112` | PL-006 |
| Astra G-03: yabadabadoo-lr's 32-bit handoff | **Answered.** `8704addb6b` adds `yabadabadoo` to `runemu.sh`'s 32-bit selector, out of this slice. Recorded as a condition on Q4 (a) row 4. | `git show 8704addb6b -- …/runemu.sh` | PL-026 |
| Astra G-04, G-05; Argon G-03: `call_achievements_hooks.sh` | **SC2048 CONFIRMED** (`$*` re-splits the title). **SC3014 REFUTED:** `/bin/sh` is bash on the image (`02`, F-04). The lead found the real defect behind the hook: patch 0012 runs `system()` on a line built from server data. **New, Medium, Security.** | `0012-cheevos-cmd.patch:9-13`; `setsettings.sh:485`; `call_achievements_hooks.sh:15,17` | PL-032 |
| Astra G-06: 0019's unlocked `current_msgs_size` test | **WITHDRAWN.** The unlocked test only decides whether to call `gfx_widgets_msg_queue_move`, which re-reads the size under `current_msgs_lock` (`gfx_widgets.c:676-679`). Upstream's own line 1186 uses the same idiom. A stale read costs one re-place, the case the next message corrects. | pinned `gfx/gfx_widgets.c:676-728,1186,1219-1220` | - |
| Astra G-07, Argon G-12: AC-09 called closed with rows 7 and 14 unread | **CONFIRMED, and closed here.** Row 14 (np2kai `d1a40352e2..5939e0c6d5`, 7 commits, 217 files): `statsave.c`, `statsave.tbl` and `libretro.c` changed mode only, so the state serializer is unchanged. The disk-image handlers did change. Row 7 bumps no core: it makes build and link fixes and adds three patches. Argon's "contradicts Q4 (b)" is right, and the row's wording is corrected. | `gh api …/NP2kai/compare/…` (134 files with no line change); `git show 6103571f67` | PL-026 |
| Astra G-08; Argon F-12 scope: coverage-table mapping | **CONFIRMED; fixed in the table.** F-12 had attached to 56 remap and append files, and `pcsx_rearmed-lr`'s Q3 read `n/a` beside #802. The coverage table is regenerated: 344 rows, 0 empty cells. | `tools/coverage-table.py` diff; `02` § Coverage table | - |
| Astra G-09; Argon G-10: Table 5 is not reachability | **CONFIRMED as a limit, written down.** Table 5 maps each patch to its source files. Of the conditional set, `batteryplus` reaches H700 only (`BATTERYPLUS_SUPPORT="yes"` in `devices/H700/options:49`; `no` on RK3326 and RK3566). **Argon's Q2 claim is REFUTED:** `git apply --check` fails, but the build's `patch -p1` applies it clean at fuzz 0 (`q4c-at-pin.txt:22`), and that is the build's test. | device `options`; `q4c-at-pin.txt` | - |
| Astra G-10: the fetch scan's scope | **CONFIRMED, wording narrowed.** The scan covered top-level build files in the x86_64 root's unpacked trees. It did not cover included scripts or cores absent from that root. | the scan's command | - |
| Astra G-11: T24's "nothing written" | **CONFIRMED, wording narrowed.** "Nothing in the current images" is established. Earlier images and `/storage/cores` copies were not checked. | Q6 Table 1's five T24 rows | - |
| Argon G-02: `param_device` in `Start Dolphin.sh` | **REFUTED as a defect.** `control-gen` writes `param_device` in the `get_controls` it emits, and the script sources that (`control-gen.cpp:31`), so SC2154 is a false positive. **CONFIRMED as a record gap:** `02` promised a "group 2" read and never wrote it. The read is recorded here. | `control-gen.cpp:31`; `Start Dolphin.sh:20-28` | - |
| Argon G-04: the other deferred shellcheck sites | **CONFIRMED as a record gap; no defect.** Read now:<br>- `Start Azahar.sh:32`: `kill -9 $(pidof gptokeyb)` is meant to split, and an empty result is a harmless usage error.<br>- `Start BigPEmu.sh:11`: an empty `gpudriver` makes the test false, the safe branch.<br>- `Start DaedalusX64.sh:12`: the unchecked `cd` precedes an absolute path.<br>- `Start Vita3K.sh:17`: `-o` inside `[ ]` works in bash.<br>The 37 SC2086 lines are named in `.qa-scratch/t3-sc-out`, not here. | the four sites | - |
| Argon G-05: F-06's fix misses two emulators | **CONFIRMED** (reading `functions:212-214`: the XPath is scoped to `emulator[@name=X]`). The fix counts defaults over the whole system. | `functions:212-214` | PL-007 |
| Argon G-06: other `set_kill` mismatches | **CONFIRMED, one more.** `Start AetherSX2.sh` registers `aethersx2-sa` while running `…/aethersx2`. The consumer is `killall ${TO_KILL}` by name (`input_sense:224`). Upstream's `eeb33c5a37` corrects it, and F-07's removal deletes the script. The other 16 launchers match their binaries. | the 18 `set_kill` lines against their exec lines | PL-010 |
| Argon G-07: SameBoy's prebuilt boot ROMs | **REFUTED.** `BootROMs/prebuilt/` ships `agb`, `cgb`, `dmg`, `sgb` and `sgb2` boot ROMs in the pinned tarball, so F-02's fix stands. | `$B/build/sameboy-lr-aa158a889a…/BootROMs/prebuilt/` | PL-012 |
| Argon G-08: Table 1 omits 13 non-`-lr` recipes | **CONFIRMED; fixed in the coverage table.** Their Q6 cells now carry the inventory's reach. | `tools/coverage-table.py` | - |
| Argon G-09: 0016 forces M+ 1p onto a blurry size | **REFUTED as a defect, kept as a note.** The 13 px floor raises the text from 8.22 px. It does not make it blurrier than it was. Its sharpness rationale was measured on Inter, not on the shipped face. | `0016` and `0017` headers; P3 | PL-018 |
| Argon G-11: the misspelt Wii remote rule | **CONFIRMED** (byte-identical duplicate). | `diff` of the two files | PL-033 |
| Argon G-13: row 8's rebuild cost | **CONFIRMED as a cost**, written into the row. Not a defect. | `af70bd435b` | PL-026 |

### Seat items: refutations of the first reader

| Finding | Astra | Argon | Graded |
| --- | --- | --- | --- |
| F-07 | Low: no legal analysis was supplied | High holds; also RK3566; the removal must travel whole | **High holds.** The grade rests on upstream's removal for licensing (the coordinator's class 1 ruling, #650), not on a legal reading, and the item now says so. RK3566 added; the whole-commit condition added. |
| F-08 | holds; the claim is image-checked for H700 and SM8550 only | holds | **Holds, narrowed in its text:** RK3326 and RK3566 rest on the recipe and their tables. |
| F-09, F-19 | hold | hold | **Hold.** F-19's timeline rests on `config.log`, as Astra says. |
| F-06 | holds; the fix is incomplete | holds; Case C | **Holds, its fix widened** (PL-007). |
| F-11 | Medium; G-02 added | Low (a latent build-root guard) | **Medium holds.** A missing or stale `retroarch32` breaks the default PSX core of four devices, F-08's own sibling. |
| F-15 | holds; "eleven unpinned" is wrong | holds | **Holds,** the count's wording corrected: nine by short hash, two by tag. |
| F-20, F-21 | hold | hold | **Hold.** |
| F-24 | Low until the consumer is read | Medium if the match is by name | **Medium holds.** The consumer is read: `killall` by name, `input_sense:224`. Still unobserved: whether `rpcs3-sa` names its process `rpcs3`. |
| F-05 | split: `st-v` is Medium | Medium | **Medium** for `st-v` on four devices, which offers a system that cannot launch. `psx` on the VM is the fallback both describe. |
| F-22 | Medium | Medium, with a wider trigger | **Low holds.** The launch at 2703 is `||`-guarded, both `swaymsg` calls are guarded, and a reboot restores the entries. Argon's wider trigger is refuted by the line itself. |
| F-12 | | scope and renamed keys | **Scope fixed** in the table. Whether a profile sets a renamed key away from its default is PL-016's stream's to read when it names each successor. |
| F-13 | wording | | **Wording corrected.** |
| Q4 (c) | five fail, 0019 needs fuzz | | **Corrected** in § Q4 (c). |
| Q6 | counts hold; selection is not reachability | Table 1 and Table 5 gaps | **Counts hold;** the limits are written down. Check A (the image comparison above) is that reachability check, run once by hand. |

**What neither seat could judge, and nobody has observed yet:**
- ARM launch outcomes;
- RPCS3's process name;
- AetherSX2's licence terms;
- the out-of-slice halves of the incoming merge;
- end-to-end patch behaviour beyond P1 to P4;
- the Steam installer's redirect and extraction safety;
- WildMIDI's archive equality.

These stay where `02` § Coverage Boundary and the items put them.

**Outcome.** Four items added: PL-030 and PL-031 (Low), PL-032 (Medium) and PL-033 (Low). F-05 rises to Medium. Seven items are reworded or widened (PL-004, 005, 006, 007, 010, 017, 018), and PL-021 and PL-026 carry the graded notes. Two seat claims are withdrawn and four refuted, each with its artifact. The punch list is 33 items: 4 High, 8 Medium, 21 Low.

## Quality Self-Check

| Section | Present | Note |
| --- | --- | --- |
| Executive summary | yes | |
| Acceptance-criteria scorecard | yes | from `02` § Criterion entries |
| Code quality assessment | yes | |
| Cornerstone conformance | yes | `03` § 3.2 |
| Spec fidelity | yes | |
| Missing artifacts | yes | |
| Risk assessment | yes | |
| Coverage boundary | yes | |
| Finding verification (4.5) | yes | the four High |
| Second opinion (4.6) | yes | extended: Astra and Argon, both verified; graded item by item |
| Renovation face Q1 to Q7 | yes | Q4's three tables and Q6's five below |
| Instruction file recommendations | yes | epic tier, Instruction-Recommendations mode |

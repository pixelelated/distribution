# T37 (#684) forward audit -- the EmulationStation recipe and themes in the distribution

Stage B, 2026-11-01, the T3 session (Opus 5.5, high), at the distribution tip `2ce981005e`
(reviewed-at `9fa740a91b`; the slice's bytes are `2174265e9c`'s, `ui/` unchanged since:
`stage-a/s5-runs.out` R03, R22). `reviewed-at-es: none -- no ES change`. Every count is a tool's
own line in the file named beside it; `proved:` is one of `tree`, `history`, `tool-run`,
`fixture`, `guest`, `fix-fixture`, `fix-image-pending`, `design`. Every read of
`emulationstation/package.mk` went through the mask with `:39` withheld by line number (`W39`,
the coordinator's answer 3 of 6551707733). The three generated tables (Coverage, The patches, The
currency) are `tools/t37-tables.py`'s output, each seen to exit 1 on a constructed drift before it
was trusted (`stage-b/tables-*-drift.out`: `ASSERT FAIL: coverage rows 14 != 15`, `ASSERT FAIL:
rows 29 (es 14, theme 15) != 30 (15, 15)`, `ASSERT FAIL: currency rows 13 != 14`).

## Coverage

The inventory's 15 (`01` § Scope), one row each; inventory tier beside git's class against the
base `c445081a59` (`behind`: the blob equals the base's and not `upstream/next`'s; `overlap`: both
sides moved it). `python3 -B -I tools/t37-tables.py --repo <worktree> --tiers
stage-a/block-2.txt coverage`, `rc=0` (`stage-b/tables-coverage.out`):

| File under `projects/ROCKNIX/packages/ui/` | Lines (`grep -c ''`) | Inventory tier | Git class against the base (`c445081a59`; behind: equal to the base and not to `upstream/next`) | Fork stat | What it is |
| --- | ---: | --- | --- | ---: | --- |
| `emulationstation/autostart/001-emulationstation` | 13 | upstream-carried | upstream-carried | -- | boot step: links /storage/.emulationstation to /storage/.config/emulationstation |
| `emulationstation/config/common/es_features.cfg` | 2039 | upstream-carried | upstream-carried, behind | -- | per-emulator feature catalogue |
| `emulationstation/config/common/es_input.cfg` | 1810 | upstream-carried | upstream-carried | -- | controller database |
| `emulationstation/config/common/es_savestates.cfg` | 26 | fork-own | fork-added | 26 | save-state layout (retroarch) |
| `emulationstation/config/common/es_settings.cfg` | 3 | upstream-carried | upstream-carried | -- | an empty <config> seed |
| `emulationstation/package.mk` | 141 | fork-own | fork-modified, overlap | 47 | the ES recipe: clone of the fork's ES at the pin; depends, cmake options, credentials by name, install steps |
| `emulationstation/sources/es_settings` | 52 | upstream-carried | upstream-carried | -- | ExecStartPre: timezone, locale, environment import |
| `emulationstation/sources/serial_number_check` | 27 | upstream-carried | upstream-carried | -- | the serial number check |
| `emulationstation/sources/start_es.sh` | 8 | upstream-carried | upstream-carried, behind | -- | sources es_settings and runs ES |
| `emulationstation/system.d/emustation.service` | 20 | upstream-carried | upstream-carried, behind | -- | the non-sway unit |
| `emulationstation/system.d/essway.service` | 21 | fork-own | fork-modified, overlap | 3 | the sway unit, with sway-ready before start |
| `lowerdeck/package.mk` | 17 | upstream-carried | upstream-carried | -- | lowerdeck at its pin, copied to /usr/share/lowerdeck |
| `themes/es-theme-art-book-next/package.mk` | 28 | fork-own | fork-modified | 2 | the theme at its pin, with the wordmark, the licence, five artwork sets removed, a zh font block |
| `themes/es-theme-art-book-next/sources/Tiny5-OFL.txt` | 93 | fork-own | fork-added | 93 | the Tiny5 font licence |
| `themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg` | 263 | fork-own | fork-added | 263 | the wordmark |

generated, asserted: rows 15, lines 4561, inventory fork-own 6 upstream-carried 9, git classes {'fork-added': 3, 'fork-modified': 3, 'upstream-carried': 9}

**The four patches under the glob are not rows** (ruling (a)): `emulationstation/patches/x86_64/cpugov.patch`
(27 lines, inventory `vendor-carried`, git upstream-carried) is **T40's**; the theme's
`patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch` (20, `vendor-carried`, git
upstream-carried), `patches/001-pixelelated-splash.patch` (31, `vendor-carried`, git fork-added)
and `patches/001-tools-always-show-image.patch` (11, `vendor-carried`, git fork-added) are
**T42's** (`stage-a/block-2.txt` `CLAIMS`; 89 lines together, `stage-a/s5-runs.out` R02). They
are read here only as the recipe reaches them (§ The patches).

## The leads

L-01 to L-22 (L-14 and L-15 folded by R2, § 3); the FAIL-first five first. Lines at `2174265e9c`.
**Family**: *fail-open* (a guard that fails open), *install* (an install step whose output is not
what its line says), *build order* (a dependency taken by build order), *structure* (a structure or
merge-debt fact), *currency* (a currency fact). **Disposition** at stage B is the lane's proposal;
the pause decides (§ 9's rows: fribidi, the link, the patch directory, the freshness tool's reach,
a loud catalog, the ARMSX2 block).

| Lead | Lines | Family | Owner | Proved | What the read shows | Proposed disposition |
| --- | --- | --- | --- | --- | --- | --- |
| **L-02** | `emulationstation/patches/x86_64/`; `scripts/unpack:127-128`, `:137-160` | fail-open | T37 (`PKG_PATCH_DIRS`), T40 (the patch, #1072) | tool-run | `patches/x86_64/: NOT REACHED` on all 15 devices (§ The patches): `PATCH_ARCH` is `x86` for an `x86_64` target (`:127-128`), the recipe sets no `PKG_PATCH_DIRS`, and outside recipes only `scripts/unpack:137-138` read it (`stage-b/reads.out` B01). Intent: `git log --diff-filter=A` prints `40fce2a089 2026-08-20 amd64: wip am64 changes`; `-S cpugov` prints `0` commits (the word is the file's name). Its hunk header `@@ -745,12 +745,20 @@` | **take up as #1072** (not a new bug); T37's half at the pause: a recipe line `PKG_PATCH_DIRS="x86_64"` (reaches `patches/x86_64/` on every `x86_64` device, and the patch's text unchanged) against T40's rename to `patches/x86/`; only one of the two lands, and the build is the only proof the patch applies (#1072 `:29`). The checker's step 4 FAILs here at stage C |
| **L-03** | `emulationstation/package.mk:101` | install | T37 (#613 if routed) | tree, history | `ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/...`: `INSTALL` is `$BUILD/install_pkg/emulationstation-<pin>` there (`scripts/build:140`, `config/functions:1380`), and neither `scripts/install` nor `scripts/image` rewrites a link (`01` open item 2), so the image carries a build-host target. Upstream's form at `c445081a59:74` and `651150fc88:75`; `-S` for the device-path form prints `0` commits (B02). The other six links of the two functions take device paths (`:84`, `:97`, `:100`, `:134`, `:137`, `:140`; s5-runs R17) | **take up as #613** -- the fix `ln -sf /usr/config/emulationstation/es_systems.cfg ...` in this slice's stream if the coordinator routes it; a #585 line (upstream's form); G-03 reads the candidate's corrected link (ruling (h)). The checker's step 5 FAILs here |
| **L-07** | `emulationstation/package.mk:70-75`; `sources/es_settings:26-35` | fail-open | T37 | tree, history | the host's `localedef` pre-generates `en_US.UTF-8` and ends `\|\| true` (`:75`), so its failure is silent; `es_settings:26-35` regenerates a missing locale at first start, so the cost of a silent failure is first-boot time (*"a minute or two on RK3326"*, `:71`). Added by `96d387fffd 2025-12-22 emulationstation: pre-generate locale to spped up first boot on lower-end devices`, upstream's (`localedef` lines: `1` at both upstream hashes; B04) | **record as written** (a best-effort cache with a correct fallback), the checker's step 5 WARN quoting `:75`; a loud variant (warn in the build log on failure) is a stream question, not a defect. G-03 reads `/usr/config/locale/en_US.UTF-8` on the candidate |
| **L-08** | `emulationstation/package.mk:67-68`; the pin's `CMakeLists.txt:565-578`, `locale/CMakeLists.txt:9`, `:25`, `:31` | fail-open | T37 (the install line); the integration (ES's CMake, ruling (f)) | tree, tool-run | with no `msgfmt`, `msgmerge`, `xgettext` or `Intl`, ES's CMake prints `Native language support disabled.` and builds no `.mo` (`:573-578`); the recipe then copies whatever `locale/lang/` holds (`:68`), so French (D-UI-051) would be absent with no error. The tools reach ES's build by build order: `gettext:host` is in ES's plan through `toolchain -> gcc:host -> autoconf:host -> gettext:host` (`01` open item 3). Whether ES's CMake found them in a given build is its configure log's (`CANNOT`) | **a stream question at the pause** ("a loud catalog"): a `makeinstall_target` line that fails when `${PKG_BUILD}/locale/lang/fr/LC_MESSAGES/emulationstation2.mo` is absent (fork-own lines; moves only ES's stamp). G-03 reads the candidate's `.mo` |
| **L-04** | `emulationstation/package.mk:79` against `:81-82` | install | T37 | tree, history | `rm -f .../resources/logo.png` runs before `resources/` is made (`:81`) and filled (`:82`), so it removes nothing and the pin's `resources/logo.png` (a blob at the pin) ships. **Corrected after the seat (stage C, `04` § Second opinion):** `es-core/src/Splash.h:17`'s `":/logo.png"` is the `else` branch; under `ROCKNIX` the default splash is `":/pixelelated-wordmark.svg"` (`:10-11`), so the shipped file is the one the line meant to drop and the build's splash does not read it. Upstream's order too (`c445081a59:52` before `:54`; `651150fc88:53` before `:55`); `-S logo.png` prints `9f1fab30f6 2025-07-13 projects: add modifications for ROCKNIX`, upstream's first line (B03) | **a contained fix for the pause** (corrected after the seat): the `rm` moved after `:82`, so it drops the unused file as it says -- or recorded as written with a #585 note; G-05 read `logo.png` on the candidate (283,835 bytes). The checker's step 5 FAILs here |
| L-01 | `emulationstation/package.mk:125-129`; `es_features.cfg:1331`, `:1333`, `:1393`; `virtual/emulators/package.mk:49-103` | structure | T37 | history, fixture | upstream's block (`651150fc88:104-108`: `armsx2-sa`'s *vulkan driver* feature deleted except on `SM4450\|SM6115\|SM8250\|SM8550\|SM8650`) is absent at the tip: every one of the four merges `a06539d8ec`, `049765fba0`, `fa2990c1e7` (2026-09-29) and `f370dc8787` (2026-10-12) had an upstream parent with `2` ARMSX2 lines and a result with `0` (`stage-b/l01-merges.out`); the tip's catalogue holds `1` such feature (B13, `xml.etree`) and installs it on every `armsx2-sa` device (`virtual/emulators/package.mk:49`, `:55`, `:60`, `:65`, `:72`, `:78`, `:84`, `:89`, `:94`, `:103`) | **a bug candidate for the pause** ("the ARMSX2 block"): restore upstream's five lines after `:128` (fork-own lines; moves only ES's stamp; a device built from the tip offers a Turnip driver it does not have, RK3566 of the fork's devices). The fixture with upstream's two `xmlstarlet` edits reproduced in `xml.etree` is stage C's (upstream `0`, tip `1`) |
| L-05 | `emulationstation/package.mk:42-44`; `scripts/get_env:14-15`; the pin's `CMakeLists.txt:303-305`, `:328-330` | fail-open | T37 | tree | the loop logs `SCREENSCRAPER_DEV_LOGIN`, `GAMESDB_APIKEY`, `CHEEVOS_DEV_LOGIN` (B09); `get_env:14` forwards those three and `HFS_DEV_LOGIN`, which builds the HFS scraper (`CMakeLists.txt:328-330`; read at the pin's `HfsDBScraper.cpp:1`, `:181`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33` -- `:181` beyond the brief's list, s5-runs R10) with no `USING:` line; `SCREENSCRAPER_SOFTNAME` (`:303-305`) is not logged; **corrected after the seat (G-5):** `get_env:16-21` forwards every variable that is not secret-shaped, so it reaches a container build too -- the keep list is the exception for the four secret-shaped names, not an allowlist | **a stream candidate**: `HFS_DEV_LOGIN` added to `:42-44`'s list (names only; fork-own lines). The count of `USING:` lines with the four placeholders is stage C's sandbox fixture (4 loud, 3 at the tip) |
| L-09 | `emulationstation/package.mk:13`; `SDL2/package.mk`, `swaywm-env`, `sway`, `pango` | build order | T37 (D-WORKFLOW-216) | tool-run | ES's plan reaches fribidi only by `emulationstation:target -> SDL2:target -> swaywm-env:target -> sway:target -> pango:target -> fribidi:target`, on GENERIC_X64 and H700 alike (`01`, trace.out); no `libass` in ES's plan; an `arm` plan builds no ES. **T36's G-01 on the candidate image reads `libfribidi` NOT linked** while the pin links `${FRIBIDI_LIBRARIES}` when the `QUIET` find succeeds (`CMakeLists.txt:236-241`, `:375`, `:462`), so that build's find failed | **the pause's** (D-WORKFLOW-216): declare `fribidi` in `:13` or record the chain as the recipe's decision with the `QUIET` branch named. Either way the candidate shipped the built-in reordering, and why its find failed is the integration's build's configure log (`CANNOT` here, inherited) |
| L-19 | `emulationstation/package.mk:14`; `config/functions:1114`, `:1126` | fail-open | T37 | tree, history | `PKG_NEED_UNPACK="busybox"` is added to the stamp's path list as a bare word (`:1114`); `find -L busybox` from the root finds `0` files, while the package's directories are `packages/sysutils/busybox` and `projects/ROCKNIX/packages/sysutils/busybox`; no script reads the variable (`scripts/ readers: 0`); the framework's own uses pass directories (`config/functions:1322`, `:1328`, `:1333`). Upstream's line at both hashes (`:11`), from `9f1fab30f6` (B07) | **a rule-6 candidate for the pause**: `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"` (the form `:1333` uses), which makes busybox's recipe move ES's stamp -- or drop the line if no ES build reads busybox (intent not recorded upstream). A #585 line. The checker's step 5 FAILs here |
| L-06 | `emulationstation/package.mk:54` | install | T37 | tool-run | `echo a-b-c \| sed "s#-#_##g"` printed `a_b-c`: `#g` is a comment and only the first hyphen goes; `0` device names have a hyphen (B08); upstream's at `c445081a59:36`, `651150fc88:37` | **record as written** with a #585 line (`s#-#_#g`); no device is affected today (rule 6 governs a defect, and this one has no effect) |
| L-10 | `tools/fork-package-freshness:16-18`, `:42-44`, `:89-93` | currency | T6 (the tool); the coordinator (`EXTRA_PACKAGES`) | tool-run | `lines=48 ui=0` (s5-runs R21): the three recipes are not in its reach | **Backlog lead** for the coordinator; whether the three join `EXTRA_PACKAGES` is the pause's |
| L-21 | `tools/pkgcheck:157`, `:169`; `tools/fork-package-freshness:42-43` | fail-open | T6 | tool-run | `pkgcheck es-theme-no-such-package` `rc=0 lines=0` (R12); freshness exits 0 with a missing ref (proof C8) | **Backlog lead** naming the three fail-opens (ruling (d)), for the coordinator to file |
| L-20 | `config/common/es_settings.cfg:1-3`; the pin's `Settings.cpp:252`, `CollectionSystemManager.cpp:1360-1366` | structure | -- | tree | the seed is an empty `<config>`, so `ThemeSet` starts at ES's `"system-theme"`, and only when no such set exists is the first available set chosen and saved (B10). **Corrected after the seat (G-9):** on the guest `system-theme` exists -- a first-boot link to the shipped theme -- and no `ThemeSet` is saved (§ The guest cycle, G-02) | **design, recorded**; G-02 reads the installed themes and the setting the image chose |
| L-11 | `emulationstation/package.mk:30`, `:39-40`, `:46` | design | D-WORKFLOW-166 | design | `:30` always passes the runtime flag and `:40` always supplies a pair, so the runtime rows never show in a recipe-built image and `:46`'s warning is unreachable for that key | **design** (D-WORKFLOW-166), recorded so no stream "fixes" it |
| L-12 | `sources/serial_number_check:12`, `:20` | -- | upstream's (D-UI-079) | tree | `cat ${DEVICE_SERIAL_NUMBER_PATH}` unquoted (`:12`); *"storted"* in a log line (`:20`); `bash -n` rc 0 | **note**, outside the lanes |
| L-13 | `sources/es_settings:12-13`, `:47-50` | -- | upstream's (D-UI-079) | tree | two timezone files rewritten in place (`:12-13`); `:47` imports unquoted words from `999-export` | **note**, outside the lanes |
| L-16 | `emulationstation/package.mk:7` | currency | #990 (the tool), #528 (custody) | history | `git log -L7,7` prints `9f1fab30f6` (`+PKG_LICENSE="GPL"`), `3d7c075f63` 2026-10-02 (`GPL` to `MIT`) and `84ff94fb3d` 2026-10-13 (`MIT` to `MIT AND BSD-3-Clause`) (B06) | **read**: the expression is the source's (`84ff94fb3d` added the RVZ reader's BSD file, `:58-65`); #990's fix reads it from there |
| L-17 | `device-builds.md` § Iterating on EmulationStation; `:8` | structure | the coordinator's sweep | tree | the rule names `maxengel/emulationstation-next` and `~/Development/emulationstation-next`; `PKG_SITE` is `https://github.com/pixelelated/emulationstation` | **doc drift** for the coordinator |
| L-18 | `CLAUDE.md` (*"scope per device with `patches/<DEVICE>/`"*); `scripts/unpack:137-159` | structure | the coordinator's sweep | tree | a `patches/<DEVICE>/` directory under a package is reached only through `PKG_PATCH_DIRS` (`:137-145`); `:159` globs a device directory outside the package (`devices/<DEVICE>/patches/<pkg>/`), present for none of the three on any device (`stage-b/reach-15.out`: `0` project-side lines) | **doc drift** for the coordinator, or upstream's `PKG_PATCH_DIRS+=" ${DEVICE}"` (`651150fc88:14`) adopted with the merge (§ The currency) |
| L-22 | the theme's XML at its pin; `themes/.../package.mk:21-27` | structure | -- | tree | read by hash (`01` § L-22): 25 `fontPath` elements, each with a `fontSize`, naming the four bundled fonts, each in the tarball; the one absolute path is the recipe's `zh` block, `/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf` (`noto-sans-cjk`'s, T8's) | **sound**; the image half is a G-02 line (`candidate`) |

**Found at stage B, beside the leads:**

| Item | Lines | Family | Proved | What the read shows | Proposed disposition |
| --- | --- | --- | --- | --- | --- |
| PL-029's sibling | `system.d/emustation.service:12` | structure | tree | `ExecStart=/usr/bin/emulationstation --log-path /var/log --no-splash` carries the same flag as `start_es.sh:8` (B12) | with PL-029 (§ The recipe) |

### The take-up (§ 2), one row each

| Found by | Lines | Disposition at stage B |
| --- | --- | --- |
| D-WORKFLOW-216 (`decision-register.md:777` at HEAD): fribidi | `:13` | L-09: **the pause's**, with T36's G-01 `libfribidi` NOT linked cited (`775d0893fe`'s `00:54`) |
| D-WORKFLOW-216: the `:25` define | `:25` | **read** (§ The recipe: the define's chain); the three empty pairs named for T35 (the list) and T36 (the bodies) |
| T2 PL-029 (`deferred:#684`) | `sources/start_es.sh:8` | **the pause's** (§ The recipe, PL-029): proposed *kept with the reason*; G-04 reads `/var/log/es_log.txt` |
| #1072 | `patches/x86_64/`, the recipe | L-02: **the pause's**, T37's `PKG_PATCH_DIRS` against T40's rename |
| #613 | `:101` | L-03: **fix if routed** |
| #1193 | `config/common/*.cfg`, `:77-78` | **read** (§ The recipe, the seeds' modes) |
| #990 | `:7` | L-16: **read** |
| T20's RVZ notices | `:58-65` | **read** (§ The recipe, install row 1) |
| The credentials (#566 CLOSED, #586, #64) | `:30`, `:39-44` | **read** (§ The recipe, credentials); #64's `:54` recorded |
| The build options the neighbours read | `:13`, `:19-25` | **read** (§ The recipe, the `-D` table); udev and pugixml in § The dependencies |
| NDEBUG; `CPPHTTPLIB_OPENSSL_SUPPORT` | the build type; `:19-25` | **read** (§ The recipe, derived rows) |
| pugixml | `:13`, `:24` | **read** (§ The dependencies) |
| The theme (D-UI-090) | `themes/.../package.mk:5`, `:7` | **read** (§ The themes) |
| #69 | T42's Tools patch | **read**: its `:52` checkbox open, nothing sent (§ The themes) |
| The splash wordmark | `themes/.../package.mk:17-18` | **read** (§ The themes) |
| `lowerdeck` | `lowerdeck/package.mk` | **read** (§ The themes) |
| Currency against ROCKNIX's recipe | the 14 files | **read** (§ The currency, generated) |
| ES PRs through the distribution (D-WORKFLOW-012) | the recipe | **read** (§ The currency, the series) |
| The lanes that name the recipe; iterating on ES | `:5`, `:6` | **read** (§ The recipe, the pin table) |
| T36's § 5 item 3 and its stage-B lines | `:25` | **open until T36 hands back** (T36 at `775d0893fe`, in stage E) |
| The pin bump's inputs | `:5`, `:6` | **integration** (§ What the integration inherits) |
| #716; rapidjson; the earlier inherit lists; #1231; T35's `05` | -- | **none**, recorded |

## The recipe

### Q1 The pin and its bump

| Item | Value | Source | Proved |
| --- | --- | --- | --- |
| The pin (`:5`) | `16dbac5211eea7e70db7394372033be2be7df829` | s5-runs R07, R14 | tree |
| Its branch (`:6`) | `test/qa-integration`; local and `origin` both `16dbac5211` | R07, R08 | tree |
| Its site (`:8-9`) | `https://github.com/pixelelated/emulationstation`, cloned (`PKG_URL=...git`, `GET_HANDLER_SUPPORT="git"` `:17`, `PKG_SHA256` empty) | R07, R14 | tree |
| ROCKNIX's pin at the base | `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` (site `ROCKNIX/emulationstation-next`) -- the pin's merge base with `rocknix/master` | R07, R08 | tree |
| ROCKNIX's pin at `upstream/next` | `f6c542872e3850c5f432929ead219547a897cd4a`, `rocknix/master` itself | R07, R08 | tree |
| The distance | the pin lacks `14` of `rocknix/master`'s commits (`7` first-parent merges) and is `724` ahead | R08 | tree |
| The M7 candidate's ES | the same `PKG_VERSION` plus nine ES patches and a corrected link, recipe blob `35e5f45e79` (R3 § 2.2 C1, C2, § 2.3, cmd 21; ruling (h)); its `BUILD_ID` `069fc270442134fe771258418adf4e666e0473fb` (T36's G-01) and, at the window, G-01's own read | R3; G-01 | -- (cited) |
| The identity sidecar | carries no ES pin (#1013) | #1013 | -- |
| The bump's steps | the ES branches merged into `test/qa-integration`; `:5` moved to that tip in the same integration commit; the stamp cleared; the compiler sees every touched `.cpp` and the ES package is built before the pin lands on `next` (`device-builds.md` § Iterating on EmulationStation, `es-native-ui.md` § Before the pin moves); `tools/pkgcheck emulationstation` by name. **This slice moves nothing** (ruling (b)) | the rules | design |
| The ES branches' tips at stage A | T34 `52f0ff5128` (local and `origin`); T35 `b7fdb3a24c` (9 ahead of the pin); T36 local at the pin (`0` ahead), no `origin` ref; the others per § 8 item 1, read at the integration's turn | `stage-a/open-items.out` | tree |
| L-17 | the rule's repository names drift from `:8` | L-17 | tree |

### Q2 The build options, one row per `-D`

The pin's `CMakeLists.txt` read by hash (`stage-a/s5-runs.out` R09, R10; the option lines read at
stage B).

| `-D` | Recipe line | CMake test at the pin | Branch it selects |
| --- | --- | --- | --- |
| `-DROCKNIX=1` | `:19` | `option(ROCKNIX ...)` `:23`; `if(ROCKNIX)` `:130-133` | `add_definitions(-DROCKNIX)`; e.g. `es-core/src/Paths.cpp:76-81` (`/storage`, `/var/log`) |
| `-DDISABLE_KODI=1` | `:20` | `:26`; `:141-145` | no `-D_ENABLE_KODI_` |
| `-DENABLE_FILEMANAGER=0` | `:21` | `:25`; `:149-152` | no `-D_ENABLE_FILEMANAGER_` |
| `-DCEC=0` | `:22` | `option(CEC "CEC" ON)` `:18`; `:274-279`, `:297-300`, `:399`, `:494` | `CEC disabled`: no `find_package(libCEC)`, no `-DHAVE_LIBCEC` |
| `-DENABLE_PULSE=1` | `:23` | `:27`; `:247-250`, `:387-391`, `:481-484` | `find_package(PulseAudio REQUIRED)`, `-D_ENABLE_PULSE_`, its include and library |
| `-DUSE_SYSTEM_PUGIXML=1` | `:24` | `:29`; `:393-396`; the library at `:469` | `find_package(pugixml REQUIRED)`: the system `pugixml` (in `:13`) |
| `-DGLES3=1` | `:25` | `option(GLES3 ...)` `:5`; the four exclusive `:9-16`; `:164-165`; `:213-214`; `:362-363` | `GLSystem "OpenGL ES 3.0"`, `find_package(OpenGLES3 REQUIRED)`, `-DUSE_OPENGLES_30`; and in `es-core/CMakeLists.txt:278-280` the `Renderer_GLES30` listing |
| `-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1` | `:30` | `:311-318` | `add_definitions(-DSCREENSCRAPER_RUNTIME_DEV_LOGIN...)`; a compiled pair hides the rows (`:313-315`, L-11) |
| `-DBATTERYPLUS=1` | `:33`, when `BATTERYPLUS_SUPPORT=yes` (H700 `options:49`, S922X `:53`; empty on GENERIC_X64, R14) | `:135-138` | `-DBATTERYPLUS` |

**Derived, not passed:** `DEVICE` upper-cased by `:54` (L-06) feeds `:115-117`
(`-DHW_DEVICE="<DEVICE>"`, `-D<DEVICE>`); `HAVE_UDEV` from `find_package(udev)` (`:255-261`);
`_ENABLE_TTS_` not defined (`ENABLE_TTS` defaults `OFF`, `:28`, `:263-272`); `HAVE_LIBCEC` not
defined (`CEC=0`); `HAVE_INTL` from the gettext tools and `Intl` (`:568-578`, L-08); `HAVE_FRIBIDI`
from the `QUIET` find (`:236-241`, L-09); `ES_BUILD_TESTS` `OFF` (`:35`); the build type `Release`
(`scripts/build:152`, passed at `:174`) and `-DNDEBUG` in `TARGET_CFLAGS`/`TARGET_CXXFLAGS` when not
a debug build (`config/functions:385-388`) -- NDEBUG is the build system's, not a recipe line;
`CPPHTTPLIB_OPENSSL_SUPPORT` is defined nowhere (`es-app-views-scrapers.md:882-887`, cited), so the
HTTP server is plain HTTP. `proved: tree`.

**The define's chain** (D-WORKFLOW-216's `:25`): `GLES3` selects `GLSystem "OpenGL ES 3.0"`
(`:164-165`), and that one value both adds `-DUSE_OPENGLES_30` (`:362-363`) and lists
`Renderer_GLES30.{h,cpp}` (`es-core/CMakeLists.txt:278-280`, `if(${GLSystem} MATCHES "OpenGL ES
3.0")`); the define compiles no source. `Renderer_GLES20` is the `else` (`:281-283`) and never
compiled here; `Renderer_GL21` and `Renderer_GLES10` are listed unconditionally (`:244-245`). No
device `case` surrounds `:25`, so every device builds the GLES 3.0 renderer, and every device's
`${OPENGLES}` is `mesa` with `-Dgles2=enabled` (`01` open item 9). **The list is T35's, the
bodies T36's, the define T37's**; a change to any is reconciled with the other two at the
integration (§ What the integration inherits item 4). `proved: tree`.

### Q2 The install steps, one row each

| Lines | What it installs | How it fails | Lead |
| --- | --- | --- | --- |
| `:58-65` | `LICENSE.rvz-padding` and `RVZ-NOTICES.md` to `/usr/share/licenses/emulationstation/` when the pin's `external/libcheevos/LICENSE.rvz-padding` exists (it does, R2 cmd 28) | silently skipped on an older pin, by design (`:58-59`); T20's records, #528's custody | -- |
| `:67-68` | `${PKG_BUILD}/locale/lang/*` to `/usr/config/locale` | copies whatever the ES build left; no `.mo` without the gettext tools, and no error | L-08 |
| `:70-75` | the pre-generated `en_US.UTF-8` | `\|\| true`: silent; first boot regenerates | L-07 |
| `:77-78` | the four `.cfg` seeds to `/usr/config/emulationstation`, by `cp -a` (git modes `100644` for all four, B11) | -- | #1193 |
| `:79` | nothing (the `rm` precedes the directory) | the pin's `logo.png` ships | L-04 |
| `:81-85` | the pin's `resources/*`; `DroidSansFallbackFull.ttf` replaced by a link to `/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf` | a missing `noto-sans-cjk` file leaves a dangling link (G-05) | L-22 |
| `:87-90` | `es_settings`, `start_es.sh`, `serial_number_check` from `${PKG_BUILD}` (`scripts/unpack` copies `sources/*` into the unpack) | -- | -- |
| `:92-94` | the binary to `/usr/bin` (`:93` a commented link) | -- | -- |
| `:96-97` | `/etc/timezone` -> `/storage/.cache/system_timezone` | -- | -- |
| `:99-101` | `/etc/emulationstation/themes` -> `/storage/.config/emulationstation/themes`; **`/etc/emulationstation/es_systems.cfg` -> a build-host path** | the second dangles on a device | L-03, #613 |
| `:104-123` | a tools-only `es_systems.cfg`, only when `EMULATION_DEVICE=no` or `BASE_ONLY=true` (neither on GENERIC_X64, R14) | -- | -- |
| `:125-128` | the vulkan choices deleted when `VULKAN_SUPPORT` is not `yes` (`yes` on GENERIC_X64, so the catalogue ships whole there) | -- | L-01 (the block it lost) |
| `:132-140` | `/usr/share/locale` -> `/storage/.config/locale`, `/usr/lib/locale` -> `/usr/share/locale`, the ES `locale` -> `/usr/share/locale` | -- | -- |
| `scripts/install:96-99`, `:107-109` | `autostart/*` to `/usr/lib/autostart/common` (mode 0755) and `system.d/*.*` to `/usr/lib/systemd/system` -- the build system's conventions, not the recipe's lines | -- | -- |

`proved: tree`. **#1193, this recipe's half:** the ES recipe installs its four seeds by `cp -a`
from files git records `100644` (B11); the `/usr/config/system/configs/system.cfg` seed #1193 names
at 0645 is not installed by any of the 15 -- the issue's own checkbox for its build step is the
coordinator's (`#1193` `:20`), named here, not traced further in this slice.

**PL-029** (`start_es.sh:8`, `deferred:#684`): `--log-path` is parsed nowhere at the pin
(`es-app/src/main.cpp`: `0` lines naming it; `parseArgs` `:75-298`; and no file of the pin's
`es-app` or `es-core` names it, `git grep -c log-path`, stage C, answering the seat's PL-09), and under `-DROCKNIX`
`es-core/src/Paths.cpp:76-81` sets `mLogPath = "/var/log"`, which `es-core/src/Log.cpp:258-259`
makes `/var/log/es_log.txt` -- so the flag is inert and the path holds. Its sibling is
`emustation.service:12`. Both are upstream's lines (`c445081a59` `start_es.sh:8`, `651150fc88`
`:14`). **Proposed: kept with the reason** -- inert, and editing either makes an upstream-carried
file fork-modified, one of them (`start_es.sh`) already behind upstream; a #585 line instead. G-04
reads `/var/log/es_log.txt` on the candidate. `proved: tree`.

### Q4 The build credentials, by name

| Name | Recipe line | ES's CMake | `get_env` | Logged |
| --- | --- | --- | --- | --- |
| `SCREENSCRAPER_RUNTIME_DEV_LOGIN` | `:30` (the option, value `1`) | `:311-318` | -- (an option, not an environment name) | -- |
| `SCREENSCRAPER_DEV_LOGIN` | `:40` (exported, defaulting to the shared identity built from `:39`'s local; value never printed), `:42` | `:307-309` | `:14` keep | yes |
| `GAMESDB_APIKEY` | `:43` | `:320-322` | `:14` keep | yes |
| `CHEEVOS_DEV_LOGIN` | `:44` | `:324-326` | `:14` keep | yes |
| `HFS_DEV_LOGIN` | none | `:328-330` | `:14` keep | **no** (L-05) |
| `SCREENSCRAPER_SOFTNAME` | none | `:303-305` | forwarded (not secret-shaped; `get_env:16-21`, corrected after the seat's G-5) | no |

`count lines: 5` (`:30`, `:40`, `:42`, `:43`, `:44`; s5-runs R18), names and line numbers only. The
recipe passes no credential to cmake: ES's CMake reads the environment (R10). D-WORKFLOW-166's
route holds: a recipe-built image compiles the shared pair (`:40`) and the runtime option (`:30`),
so its developer rows are hidden (L-11). **#64's open checkbox `:54`** (*"An upstream-style build
(no runtime flag, `SCREENSCRAPER_DEV_LOGIN` set) shows no new rows and behaves as before."*) is
**not answerable from this recipe**: it always passes the runtime flag; the CMake read says the
runtime define comes only from that option or the environment (`:316`), so an upstream-style build
defines none, but the observation is a build's -- recorded for #64, `CANNOT` here. #586
(replacement credentials) is not a current gate. G-05 counts names in the binary (`0` expected; the
macro names do not survive compilation) and the state check runs on the host (§ The guest cycle).
`proved: tree`.

## The dependencies

**Effective `PKG_DEPENDS_TARGET`**, sourced in the export (ruling (k)): GENERIC_X64 `boost
toolchain SDL2 freetype curl freeimage bash rapidjson SDL2_mixer fping p7zip alsa vlc drm_tool
poppler pugixml noto-sans-cjk zstd mesa` (s5-runs R14); H700 the same 19 wants
(`stage-a/trace.out`: `emulationstation:target build wants (19)`, identical lists on both). The
theme `toolchain noto-sans-cjk`; `lowerdeck` `toolchain Python3 SDL2 SDL2_image SDL2_ttf` (R14).

**L-09's chain, each link's effective value** (`stage-a/trace.out`, from pkgjson in the export):
`SDL2` (local) `toolchain alsa-lib systemd dbus pulseaudio libdrm mesa glu mesa vulkan-loader
vulkan-headers wayland swaywm-env`; `swaywm-env` (local) `sway wlr-randr swayimg rocknix-screenshot`;
`sway` (local) `... cairo pango libjpeg-turbo ...`; `pango` (global) `toolchain cairo freetype
fontconfig fribidi glib json-glib harfbuzz`; `fribidi` (global) `toolchain`. The chain holds on
GENERIC_X64 and H700; it breaks if SDL2's `arm` branch or a device's `WINDOWMANAGER` changes, and
an `arm` plan builds no ES (`01` open item 5). `vlc` (local) declares no `libass` and no fribidi.
**The candidate shipped without fribidi** (T36's G-01) -- the pause's question, with the decision
D-WORKFLOW-216 hands here. `proved: tool-run`.

**udev**: `:13` names none; ES's plan reaches `systemd:target` through `SDL2` (trace.out), and
`HAVE_UDEV` comes from `find_package(udev)` -- build order, as fribidi. **pugixml**:
`-DUSE_SYSTEM_PUGIXML=1` and `pugixml:target` in ES's plan (trace.out), so the image links the
system library where the lanes' host harnesses used the ES gitlink's copy (R4 item 23). **mesa**:
`${OPENGLES}` is `mesa` on all 15 devices with `-Dgles2=enabled` (`01`). **L-19** above. The
dependencies' recipes are T7's, T8's, T22's and T23's (`stage-a/block-2.txt` `DEPS`). `proved:
tool-run`.

## The themes and `lowerdeck`

| Package | Pin | `PKG_SHA256` | Licence | Install (`makeinstall_target`) | At its author's `HEAD` (R1 C20, 2026-10-31) |
| --- | --- | --- | --- | --- | --- |
| `es-theme-art-book-next` | `9a50ef366e750aabfab29e6915a2867607212971` (`upstream/next`'s too, R07) | `7ee1e93f2c4e4f7385b78680ecfa3828acf12bc616e2111d23cc66a524231125` (the cached tarball's sha256 equal, `01` § L-22) | `CUSTOM` (`:7`) | `:15-16` the tarball to `/usr/share/themes/es-theme-art-book-next`; `:17-18` the wordmark and `Tiny5-OFL.txt` (the fork's); `:19` five artwork sets removed; `:20` four of their includes deleted (`classic` has none); `:21-27` the `zh` font block appended to `fonts.xml` | yes: the pin is its author's `HEAD` |
| `lowerdeck` | `ab735114ab318a84e4d28c9c5f1b154e450a579a` (ROCKNIX's too) | `2677d3ce675b9704487f9f09f82728b56009f9fa7c36403086e9c655af108f42` | `GPL-2.0-or-later` (`:7`) | `:14-17` the tarball to `/usr/share/lowerdeck` | **no**: its author's `HEAD` was `8fefe16e9c`, by a count nobody made (no fetch, ruling (e)) |

- **The three theme patches** (T42's text): applied in name order by `scripts/unpack:150`'s
  `patches/*.patch` glob, which REACHES the theme's `patches/` on all 15 devices (§ The patches):
  `0001-system-style-...` before `001-pixelelated-splash` before `001-tools-always-show-image`
  (R2 § 3: they apply at the pin). Two share the `001-` prefix.
- **#69's upstream offer**: its `:52` checkbox (*"Patch offered upstream to the theme repository"*)
  is open; nothing is sent (D-UI-090, D-WORKFLOW-165, #585).
- **The wordmark** (D-WORKFLOW-144 to -146, `decision-register.md:604`, `:608`, `:610`): the SVG and
  the Tiny5 licence are installed beside each other (`:17-18`); the SVG carries no `font` or
  `<text>` line (`0`, `01` § L-22), so the licence ships for letterforms drawn as paths and no font
  file is needed at run time. The splash patch is T42's.
- **The default theme**: L-20 (ES's `"system-theme"`, else the first set); G-02 reads which.
- **The theme draws its own picture** (`es-code-traps.md` § The picture beside a game list):
  recorded; nothing in the recipe touches it.
- **`lowerdeck` is installed by `PKG_UI`** (`virtual/image/package.mk:18`, consumed at `:42` unless
  `BASE_ONLY` is `true`; `BASE_ONLY=` empty on GENERIC_X64, R14), and used at run time by
  `runemu.sh:337-338`, `vertical-check:6-7`, `:143`, `:175`, `:180` and `111-sway-init:163-164`,
  owned by `os-launch-control-state` (T1) and `image-packages` (T8) (`01`, the extended run). Why
  it lives under `ui/`: it is a touch interface for a second screen (`:11`).
- **A bump of either is a finding, never a change** (ruling (b)): `lowerdeck` behind its author's
  `HEAD` is a currency finding for the pause; a bump needs a new `PKG_SHA256`, which needs the
  tarball, which needs a fetch. `proved: tree`.

## The patches and their directories

Every `patches/` subdirectory of the three packages on every device, reached or not by
`scripts/unpack:150-160`'s globs with `PATCH_ARCH` by `:127-133` and the recipe's
`PKG_PATCH_DIRS` (`stage-b/reach-15.sh`, sourced in the export, `reach rc=0`;
`tools/t37-tables.py patches`, `rc=0`):

| Device / arch | Package | `PATCH_ARCH` | `PKG_PATCH_DIRS` | Directory | Verdict |
| --- | --- | --- | --- | --- | --- |
| AMD64/x86_64 | `emulationstation` | `x86` | `[]` | `patches/x86_64/` | NOT REACHED |
| AMD64/x86_64 | `es-theme-art-book-next` | `x86` | `[]` | `patches/` | REACHED |
| GENERIC_X64/x86_64 | `emulationstation` | `x86` | `[]` | `patches/x86_64/` | NOT REACHED |
| GENERIC_X64/x86_64 | `es-theme-art-book-next` | `x86` | `[]` | `patches/` | REACHED |
| H700/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| H700/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| RK3326/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| RK3326/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| RK3399/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| RK3399/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| RK3566/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| RK3566/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| RK3576/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| RK3576/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| RK3588/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| RK3588/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| S922X/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| S922X/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| SM4450/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| SM4450/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| SM6115/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| SM6115/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| SM8250/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| SM8250/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| SM8550/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| SM8550/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| SM8650/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| SM8650/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |
| SM8750/aarch64 | `emulationstation` | `aarch64` | `[]` | `patches/x86_64/` | NOT REACHED |
| SM8750/aarch64 | `es-theme-art-book-next` | `aarch64` | `[]` | `patches/` | REACHED |

generated, asserted: rows 30 over 15 devices; emulationstation patches/x86_64/ REACHED on 0 of 15; the theme's patches/ REACHED on 15 of 15; lowerdeck has no patches/ directory

**L-02** is the 15 `NOT REACHED` rows: no device reaches `emulationstation/patches/x86_64/`,
because `PATCH_ARCH` is `x86` on the two `x86_64` devices and the arch name on the 13 others, and
the recipe sets no `PKG_PATCH_DIRS`. **T37's line is the recipe's `PKG_PATCH_DIRS`; the patch's
content and place are T40's** (ruling (a), #1072). **L-18:** the device directory `:159` globs
(`devices/<DEVICE>/patches/<pkg>/`) exists for none of the three on any device (`0`
`project-side` lines), and a package's own `patches/<DEVICE>/` is reached only through
`PKG_PATCH_DIRS` (`:137-145`), which upstream's recipe sets (`PKG_PATCH_DIRS+=" ${DEVICE}"`,
`651150fc88:14`) for its `patches/RK3566/fix_multistateinput.patch` (§ The currency). The theme's
three patches apply in name order; the GLES 3.0 context patch the fork added and reverted
(`6afeaa2681`, `5da39f7adf`) is history only. `proved: tool-run`.

## The currency

One row per file of the tip-to-`upstream/next` difference over `ui/` (`git diff --shortstat
2174265e9c 651150fc88 -- projects/ROCKNIX/packages/ui/` printed ` 14 files changed, 83
insertions(+), 536 deletions(-)`, s5-runs R05). Upstream's 16 commits since the base printed ` 8
files changed, 72 insertions(+), 75 deletions(-)`; the fork's change against the base ` 8 files
changed, 463 insertions(+), 13 deletions(-)` (R04); by side `upstream-only 6 fork-only 6 both 2`
(R06). `tools/t37-tables.py currency`, `rc=0` (`stage-b/tables-currency.out`):

| File under `projects/ROCKNIX/packages/ui/` | Side | Upstream commits `c445081a59..651150fc88` | Fork non-merge commits `c445081a59..2174265e9c` | Tip to `upstream/next` | What it is |
| --- | --- | ---: | ---: | --- | --- |
| `emulationstation/config/common/es_features.cfg` | upstream moved | 4 | 0 | +36 -71 | upstream's change the fork lacks |
| `emulationstation/config/common/es_savestates.cfg` | fork moved | 0 | 2 | +0 -26 | the fork's own (absent upstream) |
| `emulationstation/package.mk` | both | 8 | 241 | +14 -34 | both moved: a merge pending |
| `emulationstation/patches/RK3566/fix_multistateinput.patch` | upstream moved | 1 | 0 | +21 -0 | upstream's change the fork lacks (absent at the tip) |
| `emulationstation/sources/start_es.sh` | upstream moved | 1 | 0 | +6 -0 | upstream's change the fork lacks |
| `emulationstation/system.d/emustation.service` | upstream moved | 1 | 0 | +1 -1 | upstream's change the fork lacks |
| `emulationstation/system.d/emustation.service.d/20-thp.conf` | upstream moved | 1 | 0 | +2 -0 | upstream's change the fork lacks (absent at the tip) |
| `emulationstation/system.d/essway.service` | both | 1 | 1 | +1 -4 | both moved: a merge pending |
| `emulationstation/system.d/essway.service.d/20-thp.conf` | upstream moved | 1 | 0 | +2 -0 | upstream's change the fork lacks (absent at the tip) |
| `themes/es-theme-art-book-next/package.mk` | fork moved | 0 | 2 | +0 -2 | the fork's own |
| `themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch` | fork moved | 0 | 2 | +0 -31 | the fork's own (absent upstream) |
| `themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch` | fork moved | 0 | 1 | +0 -11 | the fork's own (absent upstream) |
| `themes/es-theme-art-book-next/sources/Tiny5-OFL.txt` | fork moved | 0 | 1 | +0 -93 | the fork's own (absent upstream) |
| `themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg` | fork moved | 0 | 2 | +0 -263 | the fork's own (absent upstream) |

generated, asserted: rows 14; upstream-only 6 fork-only 6 both 2

Each row is **a finding with its reason, never a merge here** (the distribution merge on `ui/` is
`release-candidates.md` step 0's, R3 § 1.8):

- **Upstream's changes the fork lacks** (the six `upstream moved` rows): `es_features.cfg`'s 107
  lines (`+36 -71`); the RK3566 patch with the recipe's `PKG_PATCH_DIRS+=" ${DEVICE}"` (its context
  matches the pin, R2 cmd 21); `start_es.sh`'s `prerotate_env` and `scanout_reset_stale` (`+6`);
  `start.games` moving to `/run/rocknix/` in `emustation.service`; the two `20-thp.conf` drop-ins
  (`MemoryTHP=system`). Their ES half is the ES merge's (the 14 below).
- **Both moved, a merge pending** (the two `overlap` files): `emulationstation/package.mk` --
  upstream's ROCKNIX pin `cada856d86` to `f6c542872e`, its `PKG_PATCH_DIRS` line and its ARMSX2
  block (L-01) against the fork's source, credentials, logging and RVZ hunks (§ 2); and
  `essway.service` -- upstream's comment at `:4` (`@@ -4 +4 @@`) against the fork's `sway-ready`
  wait (`@@ -11,0 +12,3 @@`).
- **The fork's own** (the six `fork moved` rows): `es_savestates.cfg` (#196), the theme recipe's two
  lines, the wordmark and the licence (D-WORKFLOW-144 to -146), and T42's two theme patches.
- **The ES 14**: the pin lacks `14` of `rocknix/master`'s commits (`7` first-parent merges) and is
  `724` ahead (R08) -- **#791's input**; this recipe's currency moves with that merge, not
  separately.
- **The tools that would measure currency and do not:** L-10 (`lines=48 ui=0`) and L-21; both
  Backlog leads. **The licence**: L-16 (#990). **The upstream series**: an ES change reaches upstream
  as the package bump plus patches in the distribution (D-WORKFLOW-012, `decision-register.md:240`),
  so this recipe is the ES bucket's carrier in #256's and #322's series; nothing is cut here.
- **The cost to the player** is boot to interface (`essway.service`'s `sway-ready` wait,
  `TimeoutStartSec=20`; `start_es.sh`; `es_settings`' locale generation, which L-07's silent
  failure would move onto first boot), priced from G-04. `proved: tool-run`.

## The structure

- **The 15 against the 19:** the inventory's 15 are the glob's 19 less the four patches, at the
  inventory's head and at the P1 hash (`01` § Scope, the two `diff`s); 14 of the 19 are in the
  merge base, the 19 less the five fork additions (`14`, the block's last count but one).
- **The doc drifts for the coordinator's sweep:** L-17 (`device-builds.md` § Iterating on
  EmulationStation names `maxengel/emulationstation-next`; `:8` names `pixelelated/emulationstation`)
  and L-18 (`CLAUDE.md`'s *"scope per device with `patches/<DEVICE>/`"*, true only with
  `PKG_PATCH_DIRS`). Also the brief's *"through the mask"*, which leaves `:39` unchanged: the
  coordinator recorded it as an erratum (6551707733 answer 3).
- **The candidate's provenance** (ruling (h)): the M7 candidate `069fc2704421` built the pin plus
  nine ES patches the tip's recipe lacks and a corrected `es_systems.cfg` link (R3 § 2.2 C1, C2,
  § 2.3, cmd 21); `069fc2704421` is not in this repository (open item 16), and nothing under
  `/workspace/repos/rocknix` was read. Its `SYSTEM` (sha256
  `ade55e79f85d8896610a7ffecb228193c8ce651f65640c67479d64ca4c6e6982`, from M6's artifact copy at
  stage B) carries `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`
  (`stage-b/state-check-root.out`).

### The rulings, one row each

| Ruling | Brief | How this slice keeps it |
| --- | --- | --- |
| (a) the inventory's 15; the four patches T40's and T42's; L-02's `PKG_PATCH_DIRS` T37's | `:150-157` | Coverage has 15 rows and names the four after it; L-02 splits the line from the patch |
| (b) only the 15, never `:5` or `:6`; a bump a finding | `:158-169` | no edit under `packages/`, `projects/` or `tools/` at stages A and B (s5-runs R22); `lowerdeck` behind its author's `HEAD` is a finding |
| (c) no ES worktree; `-es` fields `none -- no ES change` | `:170-177` | every ES read by `git -C qa-integration` (`show`, `grep`, `rev-parse`); `00`'s `reviewed-at-es` |
| (d) `pkgcheck` by name, each after its `find` positive, with the control | `:178-190` | s5-runs R12; the fail-opens as L-21's Backlog lead |
| (e) the upstream read from the refs already here; the authors' `HEAD`s R1 C20's | `:191-207` | no fetch, `ls-remote` or `gh api`; freshness `--list` only (R21); § The themes cites R1 C20 |
| (f) ES's top-level CMake the integration's; es-core's T35's; the virtual packages T8's; the dependencies T7/T8/T22/T23 | `:208-214` | read by hash only; owners named in § The recipe and § The dependencies |
| (g) PL-029, #1072 and D-WORKFLOW-216's two are the take-up table | `:215-217` | § The take-up |
| (h) the candidate's provenance the integration's | `:218-222` | § The structure; every G-row labelled by side |
| (i) the French catalog, the themes' content and every ES file outside the slice | `:223-225` | L-08 is the recipe's install line only; L-22 reads the theme by hash without a change |
| (j) D-WORKFLOW-217 the ownership row; D-WORKFLOW-215 governs any hold | `:226-230` | D-WORKFLOW-217 at `decision-register.md:778`; no hold met at stages A and B |
| (k) never `config/options` in the worktree | `:231-246` | every sourced call in `/workspace/tmp/m6-t37/export/`; `0` build roots in the worktree at each check |

## The runs

Every run with its exit, wall time, figure and what a FAIL would mean. Stage A's § 5 runs are
`stage-a/s5-runs.out` R01-R22 (each `rc=0`, walls 0-5 s; figures in `01` § The § 5 runs at stage
A); stage A's open-item runs and stage B's are below.

| Run | Exit | Wall | Figure | A FAIL would mean |
| --- | --- | --- | --- | --- |
| § 1 first commands (`stage-a/s1-first-commands.sh`) | 0 | 2 s | every line as expected; T36's ES `origin` ref `fatal:` | a stale base, a missing pin or a moved ref under the read |
| § 2 block (`stage-a/block.sh`) | 0 | 6 s | output equal to the brief's `:531-560` | the slice is not the inventory's 15, or a count drifted |
| § 2 extended run | 0 | not timed | 8 lines | a neighbour's owner misnamed |
| R01-R22 (`stage-a/s5-runs.sh`) | 0 each | 0-5 s | `01` § The § 5 runs | an expectation the read was built on is false |
| plans (`stage-a/plans.sh`) | 0 | 2 s | ES's plan 254 steps (GENERIC_X64), 247 (H700); the `arm` plan 271 with no ES | the dependency answers (open items 3, 5, fribidi's path) unfounded |
| trace (`stage-a/trace.py`) | 0 | not timed | the chains to fribidi and gettext | as above |
| mesa per device (`stage-a/mesa-gles.sh`) | 0 | not timed | `-Dgles2=enabled` on 15 of 15 | a device whose mesa ships no GLES 3 path |
| open items (`stage-a/open-items.sh`) | 0 | 5 s | open items 2, 13, 15; L-22; the lanes' tips | the stage-A answers unfounded |
| reach on 15 devices (`stage-b/reach-15.sh`) | 0 | not timed | 15 `NOT REACHED`, 15 `REACHED`, 15 `no patches/` | a patch directory reached somewhere, or a theme patch never applied |
| tables, drift (`tools/t37-tables.py --drift`) | 1 each | not timed | `ASSERT FAIL` per table | the generator cannot fail |
| tables (`tools/t37-tables.py`) | 0 each | not timed | 15 rows, 30 rows, 14 rows | a count drifted from the scope |
| reads (`stage-b/reads.sh`) | 0 | not timed | B01-B14 | a lead's intent or a line misread |
| L-01 merges (`stage-b/l01-merges.sh`) | 0 | not timed | four merges `2 -> 0` | the block was never upstream's, or the fork has it |
| state check, payload (`stage-b/state-check-host.sh`) | script 1 (its last `grep -c` of leftover temp directories printed `0`); the check `rc=2` | sha 4 s, the check 5 s | `status error`, `input-invalid`: `mcopy` absent on the host (`command -v` printed `sfdisk` and `unsquashfs` only) | -- (it could not run: not a pass) |
| state check, root (`stage-b/state-check-root.sh`) | 0; the check `rc=0` | gunzip 7 s, unsquashfs 3 s, the check 0 s; the rest not timed | `status pass`, 279 checks: 278 `clear`, 1 `allowed` (`/usr/bin/emulationstation approved-shared-developer-identity`); `developer-service-identity clear count 0` | a compiled pair other than D-WORKFLOW-166's |
| window plan's bounds | 0 | not timed | `780` | the bound is not the plan's |

**The `CANNOT`s:** a stamp, the `USING:` lines, the gettext pass, the CMake cache (`HAVE_FRIBIDI`,
`HAVE_INTL`, `HAVE_UDEV`), the tip's recipe output, the H700 and SM8550 branches and upstream's
RK3566 patch need a build, which this slice never runs (§ 5 item 1); they are the integration's.

## The guest cycle

**The window:** granted as slot 1 at 01:40 UTC (comment 6551886156 and the host-file block); **START
01:42:09 UTC** (comment 6551903971 and the host-file line), **RETURN inside the bound** (the
guest stopped 01:44:35, bound 01:57:09, grace 02:02:09). One GENERIC_X64 guest from M6's
`069fc2704421` copy (`ls -l` on the host: 2,122,289,964 bytes) on the fresh
`/workspace/tmp/m6-t37/guest/disk.qcow2` (16 GiB), one boot at 640x480, isolated by T36's
`qemu-wrap` (`guest-cycle/helpers/qemu-wrap`, sha256 `39a8bc357e84cfb281bd149875af2effc0c28aadb3c74cedfb5f13391b7b0a3b`,
equal to `7978463093`'s blob; the running `-netdev` `user,id=net0,restrict=on,...`, `guestfwd`
`0`). The detached stop timer, pid `426713`, set for 02:02:09, was stopped by its PID unfired
(and its orphaned `sleep`, pid `426715`, by its own). Every row over `tools/vm-serial sh` through
the device read filter; the guest's own first boot wrote what an image writes (the `system-theme`
link below is one); this lane wrote nothing there. Records under `guest-cycle/` (terminal colour
codes stripped after capture).

| G | Side | Read | Proved |
| --- | --- | --- | --- |
| G-01 | candidate | `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`, `BUILD_VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"`; `/usr/bin/emulationstation` `25155163fd7970f7da54b3f36d003b8c006111c894d4fe6f0c92d24d51831226` (R3 G2's). The `ldd` is T36's G-01 on this image, cited: `libfribidi` NOT linked (`g01-identity.txt`) | guest |
| G-02 | ui-equal (the font file candidate) | ES themes `es-theme-art-book-next` (beside two non-ES directories, `Default`, `Emacs`); the wordmark and `Tiny5-OFL.txt` present; only `_inc/systems/artwork-default` left (the five removed, `:19`); removed includes `0` (`:20`); `zh` blocks `1` (`:21-27`); T42's lines present (`logoText` `2`, the `pixelelated` include `1`, the splash wordmark `1`, the Tools path `1`); the four bundled fonts; **`/usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf` present, 16,437,364 bytes** (L-22's one image read); `/etc/emulationstation/themes` -> `/storage/.config/emulationstation/themes` (`:100`); the seed the empty `<config>`; **the default (L-20):** the user `es_settings.cfg` (41 bytes) carries no `ThemeSet` line (`0`), and `/storage/.config/emulationstation/themes/system-theme` is a link, made at first boot, to `/usr/share/themes/es-theme-art-book-next` -- so ES's default `"system-theme"` resolves to the shipped theme (`g02-themes.txt`, `g02b-g04b-followup.txt`, `g02c-themes-dir.txt`) | guest |
| G-03 | the cfgs ui-equal; the link candidate | the four cfg digests **equal to the tree's at `2174265e9c`** (es_features `588958bd...`, es_input `8e6033b5...`, es_savestates `93644274...`, es_settings `c93d8b29...`); vulkan lines `15`; **the candidate's link `/usr/config/emulationstation/es_systems.cfg`, `resolves rc=0`** (L-03's corrected form); modes `644` for the four seeds and `es_systems.cfg` (#1193's ES half); the French `.mo` present, 176,095 bytes (L-08); `/usr/share/locale` -> `/storage/.config/locale`, `/usr/lib/locale` -> `/usr/share/locale`; `/usr/config/locale/en_US.UTF-8` present (L-07); 36 locale entries (`g03-configs.txt`) | guest |
| G-04 | ui-equal | `essway.service` `ActiveState=active` with the fork's three lines (`sway-ready`, `TimeoutStartSec=20`); `emustation.service` `inactive`; both `is-enabled` `disabled` and named in no `.wants` directory (a starter, `Starting[1502]: sway.service essway.service...` at 4.97 s, starts them); the three scripts' digests **equal to the tree's**; **PL-029: the running ES's argv is `emulationstation --log-path /var/log --no-splash` and `/var/log/es_log.txt` is written** (14,802 bytes, this boot) -- the flag inert, the path held by `Paths.cpp:81`; **boot to interface:** `essway.service` started at **5.37 s** (kernel monotonic), ES logging at **5.82 s**; `vm-serial wait` found ES running at 01:42:48, 39 s after START, firmware included (`g04-services.txt`, `g02b-g04b-followup.txt`) | guest |
| G-05 | candidate | the two sources' heads read, not run; names in the binary `0`; the patch's string `0` (L-02: `cpugov.patch` not in the binary); `resources/logo.png` present, 283,835 bytes (L-04); `DroidSansFallbackFull.ttf` -> the noto-cjk file, resolving; **the state check: `CANNOT -- the tool is not on the image and the window writes nothing`**, its host half `status pass` (§ The runs) (`g05-sources.txt`) | guest |
| G-06 | ui-equal | `/usr/share/lowerdeck` present, 12 entries (`main.py`, `ra_proxy.py` among them) (`g06-lowerdeck.txt`) | guest |
| G-07 | -- | `tools/vm-stop` on the pidfile: `down: owned QEMU exited (pid 426693)`, `rc=0`; the timer stopped by PID, its log empty (unfired); the disk retired: `disk.qcow2` 2,308,440,064 bytes, sha256 `f334cde02be3802e3e994b5d6deb15645164f4cd47b686bc04f7118660fc392b`, with `disk.ovmf-vars.fd` and the logs (2,308,981,090 bytes in all), `disk.img` (4,333,764,608) removed before the boot; leftover census **`qemu 0, compilers 0`** (`g07-close.txt`, `retired.txt`) | guest |

**Time to play:** boot to interface on this guest is `essway.service` at 5.37 s and ES at 5.82 s
of kernel time; the slice changes nothing on that path at stage B (no fix yet), and the recipe's
cost there is `sway-ready`'s bounded wait and `es_settings`' locale step, which L-07's
pre-generated `en_US.UTF-8` (present) keeps off first boot.

## The streams

Written by the coordinator after stage D, as for T21 to T36; the lane leaves this heading and the
pause's dispositions.

## Positives

- The three recipes keep global scope to option variables, and `tools/pkgcheck` agrees by name
  (`rc=0`, no `FAIL` or `WARN` line; R12); `bash -n` passes on all seven scripts and recipes (R11).
- The theme and `lowerdeck` are pinned by full hash with `PKG_SHA256`; the theme's cached tarball
  hashes to it (`01` § L-22); the theme is at its author's `HEAD` (R1 C20).
- The credential path keeps names out of the log (`:48-50` print `USING: <key> (set)`, never the
  value) and `get_env:14-15` keeps exactly four secret-shaped names by exception and drops the rest of that shape (the other variables pass, G-5); the image's state check passes with the
  one allowed shared identity (D-WORKFLOW-166).
- The text checks over the 15 and the four patches are clean after their planted positives
  (non-ASCII `0`, secret patterns `0`, forbidden terms `0`, the four `.cfg` well-formed; R20).
- The theme's 25 `fontPath` elements all carry a `fontSize` and name bundled fonts (L-22), and
  T42's three patches are reached on every device.
- Six of the seven links in `makeinstall_target` and `post_install` take device paths (R17).
- `essway.service`'s `sway-ready` wait is bounded (`TimeoutStartSec=20`) and owned by the unit
  (`:12-14`).

## The #585 lines owed

One per upstream-carried defect the lane proves, in the lane's shape, never sent (D-WORKFLOW-164,
-165). At stage B, proposed pending the checker's FAIL at stage C:

- **L-03** (ROCKNIX, `projects/ROCKNIX/packages/ui/emulationstation/package.mk`): the
  `es_systems.cfg` fallback link interpolates `${INSTALL}` into its target, so the image carries a
  build-host path; the device path is `/usr/config/emulationstation/es_systems.cfg` (#613).
- **L-06** (ROCKNIX, the same recipe): `sed "s#-#_##g"` replaces only the first hyphen of `DEVICE`
  (`#g` is a comment); `s#-#_#g` is meant. No current device name has a hyphen.
- **L-19** (ROCKNIX, the same recipe): `PKG_NEED_UNPACK="busybox"` is a bare word where
  `calculate_stamp` expects a path, so busybox's recipe never moves the stamp; `$(get_pkg_directory
  busybox)` is the framework's own form.
- **PL-029** (ROCKNIX, `start_es.sh` and `emustation.service`): `--log-path /var/log` is parsed by
  no ES argument branch; under `ROCKNIX` the path is `/var/log` by `Paths.cpp`. Offered as a tidy-up,
  not a defect.

## What the integration inherits

1. **The pin bump**, with the ES branches' merged tip (none yet; § The recipe, Q1) and its steps;
   T34's eight ES commits (`52f0ff5128`, `ahead=8`) and its three patches
   `stage-e/s2-holders.patch`, `stage-e/s2-window.patch`, `stage-e/s3-msgbox.patch` in T34's audit
   folder, named by path and applied by no one here; T35 at `b7fdb3a24c` (9 ahead); T36's ES branch
   local at the pin.
2. **The French catalog merges**, counted at the integration's turn; `tools/es-untranslated` after
   them (L-08's loud line, if the pause takes it, then guards the image).
3. **The define's three owners** (`:25` T37's, `es-core/CMakeLists.txt:278-283` T35's, the bodies
   T36's).
4. **Fribidi** -- the pause's decision; and **why the candidate's `QUIET` find failed** although
   ES's plan builds fribidi first, which only that build's configure log shows (L-09).
5. **The candidate's provenance** (ruling (h)): nine ES patches and the corrected link the tip's
   recipe lacks.
6. **The identity sidecar** carries no ES pin (#1013).
7. **The distribution merge on `ui/`** (upstream's 16 commits on 8 files) is
   `release-candidates.md` step 0's; **the ES 14** are #791's.
8. **The fixes this slice proves**, each `fix-image-pending` until the first image built from the
   fixed recipe shows it.
9. **The state check's payload route on this host** needs `mcopy`, absent here; the `--root` route
   over an extracted `SYSTEM` ran instead (stage B). A tool note for the coordinator, not a slice
   fix.

# Punch list (Phases 5 and 6) — M6.P2 T37, the EmulationStation recipe and themes in the distribution (#684)

Written by `tools/t37-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 the pin, Q2 the build options and install steps, Q3 the dependencies, Q4 the credentials, Q5 the themes and `lowerdeck`, Q6 the patches, Q7 currency and structure); `04` § Renovation face maps them to the plan's seven. Every disposition is proposed; the stage-D pause rules them. At Phase 7 (stage E) every item has its outcome below; a record is written `**Deferred** | recorded ...` (the stream brief's ruling 11).

reviewed-at: 9fa740a91ba9fcaa21a26cc72f0b50fac10f32df
reviewed-at-es: none -- no ES change
fixed-at: the hand-back tip, as #684's header names it (t37-streams.md § The hand-back; the last recipe commit is c9e8d5a8df, and the commits after it change no product path)
fixed-at-es: none -- no ES change

## PL-01: The `es_systems.cfg` fallback link points at a build-host path

- **Severity:** Medium; **category:** Install step; **question:** Q2
- **Source finding:** L-03; #613
- **Lines at the tip:** `emulationstation/package.mk:101`; `scripts/build:140`; `config/functions:1380`
- **Owner:** T37 (the recipe's line, if the coordinator routes #613 here); upstream's form
- **What is wrong:** `ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/...`: in `makeinstall_target` `INSTALL` is `$BUILD/install_pkg/emulationstation-<pin>`, and neither `scripts/install` nor `scripts/image` rewrites a link, so an image built from the tip carries `/etc/emulationstation/es_systems.cfg` pointing into the build host. The candidate image's link is the corrected `/usr/config/...` and resolves (G-03), because its own recipe differs (ruling (h)).
- **Proposed disposition:** take up as #613: the device path in this slice's stream if routed (`fix-fixture` by the checker's L-03 assertion, `fix-image-pending`); a #585 line
- **Tracked:** #613
- **Proposed at the pause:** Resolve in stage E (a contained recipe edit at `:101`, if #613 is routed here); else Defer to #613
- **proved:** tool-run

## PL-02: `emulationstation/patches/x86_64/` is reached on no device

- **Severity:** Medium; **category:** Patch directories; **question:** Q6
- **Source finding:** L-02; #1072
- **Lines at the tip:** `emulationstation/patches/x86_64/`; `scripts/unpack:127-128`, `:137-160`
- **Owner:** T37 (the recipe's `PKG_PATCH_DIRS`); T40 (the patch's content and place, #1072)
- **What is wrong:** `PATCH_ARCH` is `x86` for an `x86_64` target and the recipe sets no `PKG_PATCH_DIRS`, so `cpugov.patch` applies on none of the 15 devices (`stage-b/reach-15.out`); its string is absent from the candidate's binary (G-05). Added by `40fce2a089 2026-08-20 amd64: wip am64 changes`.
- **Proposed disposition:** take up as #1072, **after** T40 corrects the patch's GPU call (the seat's G-1, confirmed: its `+` lines call `get_available_cpu_governors` 4 times and `get_available_gpu_governors` 0 times, so reaching it as it is wires the CPU list into the GPU rows): the pause chooses T37's `[ "${ARCH}" = "x86_64" ] && PKG_PATCH_DIRS+=" x86_64"` (appending, the seat's G-2; `TARGET_ARCH="${ARCH}"` at `config/options:36`, so the test is the unpacker's) or T40's rename to `patches/x86/`; only a build proves the patch applies
- **Tracked:** #1072
- **Proposed at the pause:** Defer to #1072 (T40 corrects the patch's GPU call first; then T37's `PKG_PATCH_DIRS+=` line or T40's rename)
- **proved:** tool-run

## PL-03: `PKG_NEED_UNPACK="busybox"` is a bare word, so busybox never moves the ES stamp

- **Severity:** Low; **category:** Build order; **question:** Q3
- **Source finding:** L-19
- **Lines at the tip:** `emulationstation/package.mk:14`; `config/functions:1114`, `:1126`
- **Owner:** T37; upstream's line (`9f1fab30f6`)
- **What is wrong:** `calculate_stamp` adds the word to its `find -L` paths relative to the root, where `busybox` names nothing (`0` files); the framework and upstream recipes pass a directory (`$(get_pkg_directory vdr)` in the vdr plugins' recipes, `config/functions:1322-1333`).
- **Proposed disposition:** rule 6: `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"` (the fixture passes `pkgcheck` and the checker with it), or the line dropped if no ES build needs busybox; a #585 line
- **Tracked:** #1382
- **Proposed at the pause:** Resolve in stage E (#1382): `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"`
- **proved:** tool-run

## PL-04: The `rm` of `resources/logo.png` runs before the directory exists

- **Severity:** Low; **category:** Install step; **question:** Q2
- **Source finding:** L-04
- **Lines at the tip:** `emulationstation/package.mk:79`, `:81-82`; the pin's `es-core/src/Splash.h:17`
- **Owner:** T37; upstream's order (`9f1fab30f6`)
- **What is wrong:** The line removes nothing, so the pin's `logo.png` ships (G-05, 283,835 bytes). Corrected after the seat: under `ROCKNIX` the default splash is `:/pixelelated-wordmark.svg` (the pin's `Splash.h:10-11`); `:/logo.png` is the `else` branch's (`:16-17`), so the shipped file is the one the line meant to drop, and nothing in the build's splash reads it.
- **Proposed disposition:** a contained fix for the pause: the `rm` moved after `:82` (it then does what it says and drops an unused file), or recorded as written with a #585 note
- **Tracked:** #1383
- **Proposed at the pause:** Resolve in stage E (#1383): the `rm` moved after `:82`
- **proved:** tree

## PL-05: Upstream's ARMSX2 *vulkan driver* block was dropped by four merges

- **Severity:** Low; **category:** Merge debt; **question:** Q7
- **Source finding:** L-01
- **Lines at the tip:** `emulationstation/package.mk:125-129` (`651150fc88:104-108`); `es_features.cfg:1331`, `:1333`, `:1393`
- **Owner:** T37
- **What is wrong:** `a06539d8ec`, `049765fba0`, `fa2990c1e7` and `f370dc8787` each had an upstream parent with the two ARMSX2 lines and a result without them (`stage-b/l01-merges.out`); the tip's catalogue keeps `armsx2-sa`'s *vulkan driver* feature on every device that ships `armsx2-sa`, so devices without ARMSX2's own Turnip offer it (RK3566 of the fork's). Lowered to Low at stage D: the launcher points the loader at the bundled Turnip only when its ICD file exists (`armsx2-sa/scripts/start_armsx2.sh:215-218`), so on those devices the row's two choices change nothing -- a misleading row, not a broken launch.
- **Proposed disposition:** a bug candidate for the pause: upstream's five lines restored after `:128` (moves only ES's stamp). The seat's G-3 asked for the capability: upstream's list `SM4450|SM6115|SM8250|SM8550|SM8650` is exactly `armsx2-sa`'s own `armsx2-turnip` predicate (`armsx2-sa/package.mk:25-29`; SM8750 *keeps the system driver*), so the block matches the installer. The fixture with upstream's two edits in `xml.etree` at stage E
- **Tracked:** #1384
- **Proposed at the pause:** Resolve in stage E (#1384): upstream's five ARMSX2 lines restored after `:128`
- **proved:** history

## PL-06: The candidate's ES does not link fribidi; the recipe declares it nowhere

- **Severity:** Low; **category:** Build order; **question:** Q3
- **Source finding:** L-09; D-WORKFLOW-216; T36's G-01
- **Lines at the tip:** `emulationstation/package.mk:13`; the pin's `CMakeLists.txt:236-241`, `:462`
- **Owner:** T37 (the declaration, D-WORKFLOW-216); the integration (why the find failed)
- **What is wrong:** ES's plan reaches fribidi only by `SDL2 -> swaywm-env -> sway -> pango -> fribidi`; T36's G-01 on the candidate reads `libfribidi` NOT linked, so its `QUIET` find failed and the built-in reordering shipped.
- **Proposed disposition:** the pause's ruling under D-WORKFLOW-216 (declare `fribidi` at `:13`, the seat's choice, or record the chain as the recipe's decision); lowered to Low after the seat: the fallback is designed (`CMakeLists.txt:230-233`) and an `ldd` absence alone does not show which branch compiled; the find's failure is the integration's configure log (`CANNOT` here)
- **Tracked:** D-WORKFLOW-216; the integration's configure log
- **Proposed at the pause:** Resolve in stage E: `fribidi` declared in `:13` (the seat's choice; the probe stays optional), the configure-log proof inherited by the integration
- **proved:** tool-run

## PL-07: A missing French catalog would install silently

- **Severity:** Low; **category:** Guard that fails open; **question:** Q2
- **Source finding:** L-08
- **Lines at the tip:** `emulationstation/package.mk:67-68`; the pin's `CMakeLists.txt:565-578`
- **Owner:** T37 (the install line); ES's CMake the integration's
- **What is wrong:** Without the gettext tools ES builds no `.mo` and says only `Native language support disabled.`; the recipe copies what is there. The tools reach the build by `toolchain -> gcc:host -> autoconf:host -> gettext:host`, and the candidate carries the French `.mo` (G-03).
- **Proposed disposition:** a stream question at the pause ("a loud catalog"): a line that fails when `fr/LC_MESSAGES/emulationstation2.mo` is absent; the checker WARNs at the tip
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Resolve in stage E: a `makeinstall_target` line that fails when the French `.mo` is missing
- **proved:** tree

## PL-08: `HFS_DEV_LOGIN` builds a scraper with no `USING:` line

- **Severity:** Low; **category:** Guard that fails open; **question:** Q4
- **Source finding:** L-05
- **Lines at the tip:** `emulationstation/package.mk:42-44`; `scripts/get_env:14`; the pin's `CMakeLists.txt:328-330`
- **Owner:** T37
- **What is wrong:** The log loop names three of the four secret-shaped names `get_env` keeps by exception; `HFS_DEV_LOGIN` (read at the pin's `HfsDBScraper.cpp:1`, `:181`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33`) is the fourth. Corrected after the seat (G-5): `get_env:16-21` forwards every variable that is not secret-shaped, so `SCREENSCRAPER_SOFTNAME` (`CMakeLists.txt:303-305`) reaches a container build too, also unlogged.
- **Proposed disposition:** a stream candidate: `HFS_DEV_LOGIN` added to the loop's list (names only)
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Resolve in stage E: `HFS_DEV_LOGIN` added to the loop at `:42-44` (names only)
- **proved:** tree

## PL-09: `--log-path /var/log` is passed to ES and parsed by nothing

- **Severity:** Low; **category:** Install step; **question:** Q2
- **Source finding:** T2 PL-029 (`deferred:#684`)
- **Lines at the tip:** `sources/start_es.sh:8`; `system.d/emustation.service:12`; the pin's `Paths.cpp:76-81`
- **Owner:** T37 (upstream's two lines)
- **What is wrong:** `parseArgs` has no such branch; under `-DROCKNIX` the log path is `/var/log`, and the candidate writes `/var/log/es_log.txt` with the flag in its argv (G-04).
- **Proposed disposition:** kept with the reason (inert; editing either file makes an upstream-carried file fork-modified, `start_es.sh` already behind upstream); a #585 line
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record: kept with its reason, a #585 line
- **proved:** guest

## PL-10: The two checkers that would measure these recipes pass over nothing

- **Severity:** Low; **category:** Guard that fails open; **question:** Q7
- **Source finding:** L-10, L-21
- **Lines at the tip:** `tools/pkgcheck:157`, `:169`; `tools/fork-package-freshness:16-18`, `:42-44`
- **Owner:** T6 (the tools); the coordinator (`EXTRA_PACKAGES`)
- **What is wrong:** `pkgcheck` with a name that matches nothing prints nothing and exits 0; freshness prints its header for an unknown name and exits 0 with a missing ref, and its `--list` reaches none of the three (`lines=48 ui=0`).
- **Proposed disposition:** a Backlog lead for the coordinator to file, naming the three fail-opens and the three recipes' reach
- **Tracked:** a Backlog the coordinator files
- **Proposed at the pause:** Defer to a Backlog the coordinator files
- **proved:** tool-run

## PL-11: `sed "s#-#_##g"` replaces only the first hyphen of `DEVICE`

- **Severity:** Low; **category:** Install step; **question:** Q2
- **Source finding:** L-06
- **Lines at the tip:** `emulationstation/package.mk:54`
- **Owner:** T37; upstream's line
- **What is wrong:** `echo a-b-c | sed "s#-#_##g"` prints `a_b-c`; no device name has a hyphen today.
- **Proposed disposition:** recorded as written, with a #585 line (`s#-#_#g`)
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record: as written, a #585 line
- **proved:** tool-run

## PL-12: The pre-generated locale's failure is silent

- **Severity:** Low; **category:** Guard that fails open; **question:** Q2
- **Source finding:** L-07
- **Lines at the tip:** `emulationstation/package.mk:70-75`; `sources/es_settings:26-35`
- **Owner:** T37; upstream's (`96d387fffd`)
- **What is wrong:** `|| true` ends the `localedef` step: a failure is silent in its status, though its verbose output still reaches the build log (the seat's narrowing); `es_settings:26-35` regenerates a missing locale at first start but checks neither that result nor the export after it. The candidate has the pre-generated locale (G-03).
- **Proposed disposition:** recorded as written (a best-effort cache with a correct fallback); the checker's WARN
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record: as written (a best-effort cache with a fallback)
- **proved:** tree

## PL-13: `lowerdeck` is behind its author's `HEAD`

- **Severity:** Low; **category:** Package currency; **question:** Q5
- **Source finding:** R1 C20 (2026-10-31)
- **Lines at the tip:** `lowerdeck/package.mk:5-6`
- **Owner:** T37 (a finding); a bump needs a fetch
- **What is wrong:** Pinned at `ab735114ab` (ROCKNIX's pin too); its author's `HEAD` was `8fefe16e9c` at R1's dated read, by a count nobody made.
- **Proposed disposition:** a currency finding, never a bump here (ruling (b)): the bump, with its new `PKG_SHA256`, at the integration or with ROCKNIX's
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record: the dated currency finding; the bump at the integration
- **proved:** tree

## PL-14: Upstream's six `ui/` changes and two overlaps wait for the distribution merge

- **Severity:** Low; **category:** Merge debt; **question:** Q7
- **Source finding:** § The currency (14 rows)
- **Lines at the tip:** the 14 files of `2174265e9c..651150fc88` over `ui/`
- **Owner:** `release-candidates.md` step 0 (the merge); #791 (the ES 14)
- **What is wrong:** `upstream-only 6 fork-only 6 both 2`: the RK3566 patch and `PKG_PATCH_DIRS+=" ${DEVICE}"`, the two THP drop-ins, `start_es.sh`'s two functions, `emustation.service`'s `start.games` path and 107 lines of `es_features.cfg` the fork lacks; the ES recipe and `essway.service` changed on both sides.
- **Proposed disposition:** deferred to the distribution merge and #791 (a finding per row in `02` § The currency, never a merge here)
- **Tracked:** the distribution merge; #791
- **Proposed at the pause:** Defer to the distribution merge (`release-candidates.md` step 0) and #791
- **proved:** tool-run

## PL-15: Two rules describe the recipe as it is not

- **Severity:** Low; **category:** Documentation; **question:** Q1
- **Source finding:** L-17, L-18
- **Lines at the tip:** `device-builds.md` § Iterating on EmulationStation; `CLAUDE.md` (patches per device)
- **Owner:** the coordinator's sweep
- **What is wrong:** The rule names `maxengel/emulationstation-next` where `:8` is `pixelelated/emulationstation`; `CLAUDE.md`'s `patches/<DEVICE>/` holds only where a recipe sets `PKG_PATCH_DIRS`.
- **Proposed disposition:** the coordinator's doc sweep
- **Tracked:** the coordinator's sweep
- **Proposed at the pause:** Defer to the coordinator's doc sweep
- **proved:** tree

## PL-16: `tools/pixelelated-state-check --payload` cannot run on this host

- **Severity:** Low; **category:** Tooling; **question:** Q4
- **Source finding:** stage B (G-05's host half)
- **Lines at the tip:** `tools/pixelelated-state-check:767-792`
- **Owner:** the coordinator (a tool note; the tool fails closed, as it should)
- **What is wrong:** The `.img.gz` route needs `mcopy`, absent here: `rc=2`, `input-invalid`. The `--root` route over an extracted `SYSTEM` ran instead and passed.
- **Proposed disposition:** a tool note for the integration (§ What the integration inherits item 9); no slice fix
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record: the tool note (`02` § What the integration inherits item 9)
- **proved:** tool-run

## PL-17: A verbose build prints the compiled-in pair in its compile commands

- **Severity:** Low; **category:** Credentials; **question:** Q4
- **Source finding:** G-6 (gpt)
- **Lines at the tip:** `emulationstation/package.mk:40`; the pin's `CMakeLists.txt:307-309`, `:320-330`; `config/functions:378-382`
- **Owner:** T37 (the recipe's comment); the build engine T6's
- **What is wrong:** CMake turns each credential variable into a `-D` definition; a build with the `verbose` flag (default `no`, `config/functions:379`) prints every compile command, so the log carries the definitions the recipe's echo at `:48-50` keeps out. No disclosure is shown; D-INFRA-006 tolerates a value in a local build log.
- **Proposed disposition:** recorded under D-INFRA-006 (a local build log), with a sentence beside `:48-50` naming the verbose route; judged outside D-WORKFLOW-215's hold test (not shipped code; an input only the builder sets)
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record under D-INFRA-006 (a mask on the verbose path is a Backlog candidate for the coordinator)
- **proved:** tree

## PL-18: The autostart alias repairs neither a real directory nor a wrong link

- **Severity:** Low; **category:** Install step; **question:** Q2
- **Source finding:** G-7 (gpt)
- **Lines at the tip:** `emulationstation/autostart/001-emulationstation:8-11`
- **Owner:** T37; upstream's (JELOS)
- **What is wrong:** A real `/storage/.emulationstation` directory passes `! -L`, and `ln -sf` then makes the link inside it; an existing symlink, right or wrong, is skipped. ES itself reads `/storage/.config/emulationstation` under `ROCKNIX` (`Paths.cpp:79`), so only the legacy alias is affected.
- **Proposed disposition:** recorded as written (upstream's; the alias is legacy), or a contained `ln -sfn` with a directory test at the pause
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record: as written (upstream's legacy alias)
- **proved:** tree

## PL-19: An empty serial-number read is treated as a changed device

- **Severity:** Low; **category:** Guard that fails open; **question:** Q2
- **Source finding:** G-8 (gpt)
- **Lines at the tip:** `emulationstation/sources/serial_number_check:8-24`
- **Owner:** T37; upstream's (D-UI-079: outside the fork's lanes)
- **What is wrong:** When the path is set and the read is empty, a stored serial differs from `""`, so the empty value is stored and the warning raised (`:21-24`); the unquoted path at `:12` is L-12.
- **Proposed disposition:** recorded for upstream (a #585 line); a contained guard (an empty read skips the check) only if the coordinator opens the lane
- **Tracked:** #1381 (this audit)
- **Proposed at the pause:** Record: for upstream, a #585 line
- **proved:** tree

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Deferred** | #613 (ruling 2): the M7 lane's; the checker's L-03 FAIL kept as its guard |
| PL-02 | **Deferred** | #1072 (ruling 3): after T40 corrects the GPU call; the checker's L-02 FAIL kept |
| PL-03 | **Resolved** | `c93b1cad7d` (#1382): the L-19 pair FAIL then PASS; the busybox stamp pair |
| PL-04 | **Resolved** | `39863d5af3` (#1383): the L-04 pair FAIL then PASS |
| PL-05 | **Resolved** | `e1e99c5a7e` (#1384): the two ARMSX2 assertions FAIL then PASS |
| PL-06 | **Deferred** | #1385 (ruling 4): the choice; the three reads in `02` |
| PL-07 | **Resolved** | `ce31abba74` (#1381): the catalog guard's assertion FAIL then PASS |
| PL-08 | **Resolved** | `c9e8d5a8df` (#1381): the USING count FAIL 3 then PASS 4 |
| PL-09 | **Deferred** | recorded: kept with its reason (ruling 5; #684 comment 6552560083), #585 line in `02` |
| PL-10 | **Deferred** | #1385 (ruling 6) |
| PL-11 | **Deferred** | recorded: as written (ruling 5; #684 comment 6552560083), #585 line in `02` |
| PL-12 | **Deferred** | recorded: as written (ruling 5; #684 comment 6552560083) |
| PL-13 | **Deferred** | recorded: the dated finding, the bump the integration's under D-WORKFLOW-024 (ruling 5; #684 comment 6552560083) |
| PL-14 | **Deferred** | #791 and the distribution merge (ruling 7) |
| PL-15 | **Deferred** | the coordinator's sweep in `1f9327d496` (ruling 8; #684 comment 6552560083) |
| PL-16 | **Deferred** | recorded: the tool note (ruling 5; #684 comment 6552560083); its tool half #1385 |
| PL-17 | **Deferred** | recorded under D-INFRA-006 (ruling 5; #684 comment 6552560083); its mask #1385 |
| PL-18 | **Deferred** | recorded: as written (ruling 5; #684 comment 6552560083) |
| PL-19 | **Deferred** | recorded: for upstream (ruling 5; #684 comment 6552560083), #585 line in `02` |

## punch_index

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: "Install step"
  question: Q2
  source_finding: "L-03; #613"
  outcome: "deferred"
- id: PL-02
  severity: "Medium"
  category: "Patch directories"
  question: Q6
  source_finding: "L-02; #1072"
  outcome: "deferred"
- id: PL-03
  severity: "Low"
  category: "Build order"
  question: Q3
  source_finding: "L-19"
  outcome: "resolved"
- id: PL-04
  severity: "Low"
  category: "Install step"
  question: Q2
  source_finding: "L-04"
  outcome: "resolved"
- id: PL-05
  severity: "Low"
  category: "Merge debt"
  question: Q7
  source_finding: "L-01"
  outcome: "resolved"
- id: PL-06
  severity: "Low"
  category: "Build order"
  question: Q3
  source_finding: "L-09; D-WORKFLOW-216; T36's G-01"
  outcome: "deferred"
- id: PL-07
  severity: "Low"
  category: "Guard that fails open"
  question: Q2
  source_finding: "L-08"
  outcome: "resolved"
- id: PL-08
  severity: "Low"
  category: "Guard that fails open"
  question: Q4
  source_finding: "L-05"
  outcome: "resolved"
- id: PL-09
  severity: "Low"
  category: "Install step"
  question: Q2
  source_finding: "T2 PL-029 (`deferred:#684`)"
  outcome: "deferred"
- id: PL-10
  severity: "Low"
  category: "Guard that fails open"
  question: Q7
  source_finding: "L-10, L-21"
  outcome: "deferred"
- id: PL-11
  severity: "Low"
  category: "Install step"
  question: Q2
  source_finding: "L-06"
  outcome: "deferred"
- id: PL-12
  severity: "Low"
  category: "Guard that fails open"
  question: Q2
  source_finding: "L-07"
  outcome: "deferred"
- id: PL-13
  severity: "Low"
  category: "Package currency"
  question: Q5
  source_finding: "R1 C20 (2026-10-31)"
  outcome: "deferred"
- id: PL-14
  severity: "Low"
  category: "Merge debt"
  question: Q7
  source_finding: "§ The currency (14 rows)"
  outcome: "deferred"
- id: PL-15
  severity: "Low"
  category: "Documentation"
  question: Q1
  source_finding: "L-17, L-18"
  outcome: "deferred"
- id: PL-16
  severity: "Low"
  category: "Tooling"
  question: Q4
  source_finding: "stage B (G-05's host half)"
  outcome: "deferred"
- id: PL-17
  severity: "Low"
  category: "Credentials"
  question: Q4
  source_finding: "G-6 (gpt)"
  outcome: "deferred"
- id: PL-18
  severity: "Low"
  category: "Install step"
  question: Q2
  source_finding: "G-7 (gpt)"
  outcome: "deferred"
- id: PL-19
  severity: "Low"
  category: "Guard that fails open"
  question: Q2
  source_finding: "G-8 (gpt)"
  outcome: "deferred"
```

Punch list of the M6 T3 audit (#650): RetroArch and the libretro cores, 344 paths, `reviewed-at: d606301784` (the slice's bytes equal to `next`'s `8ebaf8daad`). The audit is `docs/audits/2026_10_24-epic-m6-emulators-libretro/` on `feature/m6-emulators-libretro-650`. 33 items: 0 critical, 4 high, 8 medium, 21 low.

## Executive summary

The launch table is the build's own: the host regeneration from the tree's shell is byte-identical to the GENERIC_X64, H700 and SM8550 images, and the guest's installed set equals the tree's.

**The four High findings:**

- The default PlayStation core on four built devices is installed where the launcher does not load it (#802).
- The next base merge brings upstream's fix for that, and the new `yabadabadoo-lr`, as `build.${DISTRO}-` copies that fail on the fork's roots (#802).
- SM8550's grep has no PCRE, so Install Steam stops at its Proton step (#806).
- `aethersx2-sa`, dropped upstream for licensing, still ships on SM8550 and RK3566.

**The Medium found in the second opinion:** patch 0012 hands RetroArch's `system()` a shell line built from an achievement's title and description, on every unlock (PL-032).

**Currency:** all 14 upstream commits on the slice are `to merge`, two of them adapted. Of the 151 pins, 40 are current, 104 behind their project, 1 behind ROCKNIX and 6 not on their project's default branch. RetroArch is 7,623 commits behind master, and a bump is a re-cut of its patch series.

**Time to play** on the image as built: 0.62 s to the first frame and 1.01 s game to game (n = 3).

## Acceptance-criteria scorecard (#650, at the end of Phase 2)

4 PASS (AC-06, AC-07, AC-08, AC-12); 5 PARTIAL (AC-01, AC-05, AC-09, AC-10, AC-11); 6 open for later stages of the lane (AC-02, AC-03, AC-04, AC-13, AC-14, AC-15); 0 FAIL. `02-forward-audit.md` § Criterion entries has each with its evidence.

## The items

Each checkbox is ticked from its acceptance artifact when its Phase 7 outcome is recorded in `05-punch-list.md` (resolved with its commit, deferred to a named issue, or withdrawn with its reason).

- [ ] **PL-001** (High, Q3, Interaction Defect) (#802): The default PlayStation core on H700, RK3326, RK3566 and SM8550 is not where the launcher loads it. Acceptance: An arm-enabled build's install tree (H700 or SM8550) carries usr/lib/libretro/pcsx_rearmed32_libretro.so; tools/regen-es-systems.sh's table for that device is unchanged.
- [ ] **PL-002** (High, Q4, Interaction Defect) (#802): The next base merge brings two `build.${DISTRO}-` copies the fork's roots cannot satisfy, and git merges them cleanly. Acceptance: On the merged tree, git grep -F 'build.${DISTRO}-' -- projects packages scripts prints nothing, and the five rotation-table recipes carry Python3:host, retroarch and PKG_NEED_UNPACK.
- [ ] **PL-003** (High, Q3, Interaction Defect) (#806): On the SM8550 image Install Steam stops at its Proton step: `grep -oP` with a grep built without PCRE. Acceptance: git grep -n -E 'grep (-[a-zA-Z]*P|--perl-regexp)' on Install Steam.sh prints nothing, and a guest run of fetch_proton_latest_release against a fixture release JSON, with a grep that refuses -P first on PATH, sets PROTON_GE_URL and PROTON_GE_TAR.
- [ ] **PL-004** (High, Q4, Spec Drift): `aethersx2-sa`, dropped upstream for a licensing concern, still ships on SM8550 and RK3566. Acceptance: On the merged tree, git grep -n aethersx2 -- projects/ROCKNIX/packages/virtual/emulators prints nothing.
- [ ] **PL-005** (Medium, Q3, Code Quality): `melonds-ds-lr` fetches eleven dependencies from the network at configure time, by short hash or tag. Acceptance: The recipe sets FETCHCONTENT_FULLY_DISCONNECTED=ON and names each dependency with a full hash and a checksum, and a build of the core from an unseeded source cache in a container with no network configures, with find <root>/build/melonds-ds-lr-*/.*/_deps -name '*-subbuild' printing nothing.
- [ ] **PL-006** (Medium, Q3, Code Quality): `retroarch32` is skipped silently when the ARM root's install directory is not exactly one, and a single stale one is copied unchecked. Acceptance: The sandboxed makeinstall_target exits 1 with the path named for a root with no retroarch install directory and for one with two, refuses a root whose one directory carries another version, and installs retroarch32 for one with the pinned version.
- [ ] **PL-007** (Medium, Q7, Documentation Gap): The table's README claims a build failure on two default cores; one shape fails silently and the other ships two defaults. Acceptance: package.mk's README comment states the two behaviours or the check T5's fix adds, and the regeneration's tables for the five devices are byte-unchanged.
- [ ] **PL-008** (Medium, Q2, Code Quality): GitHub release data reaches `eval` in `fetch_proton_latest_release`. Acceptance: On the merged file, grep -n eval in fetch_proton_latest_release prints nothing.
- [ ] **PL-009** (Medium, Q3, Code Quality): The Steam runtime and Proton archives are installed with no integrity check. Acceptance: On the guest with a fixture release whose .sha512sum does not match its archive, install_proton_variant refuses with a named reason and installs nothing; with a matching one it installs.
- [ ] **PL-010** (Medium, Q3, Code Quality): On SM8550 the exit hotkey's kill target for RPCS3 names a process that never runs. Acceptance: On the merged tree, Start RPCS3.sh registers set_kill set "-9 rpcs3-sa".
- [ ] **PL-011** (Medium, Q3, Code Quality): The H700, RK3326, RK3566 and GENERIC_X64 tables offer `st-v` with no emulator, and GENERIC_X64's gives `psx` no default core. Acceptance: tools/regen-es-systems.sh's GENERIC_X64 table gives psx exactly one default core, and no device's table has a system with no emulator besides tools and imageviewer.
- [ ] **PL-012** (Low, Q2, Code Quality): `sameboy-lr` references PKG_BUILD at global scope, for an option its libretro build never reads. Acceptance: tools/pkgcheck sameboy-lr exits 0, and the next image's usr/lib/libretro/sameboy_libretro.so exists.
- [ ] **PL-013** (Low, Q2, Code Quality): `Start Azahar.sh` and `Start MelonDS.sh` put their shebang on line 2. Acceptance: shellcheck -f gcc on both files reports no SC1128, and head -1 of each is #!/bin/bash.
- [ ] **PL-014** (Low, Q2, Code Quality): `0004-drm-resolution.patch` applies to the pin only with fuzz. Acceptance: tools/q4c-patches.sh at the pin reads fuzz0=ok for 0004 and applied=clean or offset for all 21.
- [ ] **PL-015** (Low, Q2, Code Quality): `easyrpg-lr/wildmidi` pins a short hash. Acceptance: PKG_VERSION is the 40-hex hash and tools/pkgcheck wildmidi exits 0.
- [ ] **PL-016** (Low, Q6, Renovation): Every shipped retroarch.cfg carries 24 or 25 keys the pinned RetroArch never reads, and fourteen carry the armhf core-updater URL. Acceptance: The key test of q6-retroarch-cfg-keys-not-read.txt run over the edited profiles prints 0 for every profile, and grep -c core_updater_buildbot_url over sources/*/retroarch.cfg prints 0.
- [ ] **PL-017** (Low, Q1, Renovation): Three status checks after RetroArch's makes have failure arms set -e never reaches. Acceptance: grep -c '\[ \$? -eq 0 \]' retroarch/package.mk prints 0 and tools/pkgcheck retroarch exits 0.
- [ ] **PL-018** (Low, Q6, Renovation): Patch 0017's size step engages on no shipped profile. Acceptance: Either the profiles' video_font_path names an ozone face and P3's log reads a sharp-size table, or 0017 is absent from the series, or a comment beside video_font_path in the GENERIC_X64 profile names 0017 and why it waits.
- [ ] **PL-019** (Low, Q7, Documentation Gap): `X64_SKIP_CORES` says its cores are tracked in #16, which is closed. Acceptance: The comment above X64_SKIP_CORES names an open issue, or says the skip is permanent with each core's reason.
- [ ] **PL-020** (Low, Q6, Test Gap): `tools/retroarch-wrapper-test --gated` asserts nothing. Acceptance: grep -c gated tools/retroarch-wrapper-test prints 0, or a --gated run's output differs from the plain run's by what the flag checks.
- [ ] **PL-021** (Low, Q3, Code Quality): An interrupted first launch leaves x86/box64 binfmt disabled. Acceptance: On the guest, run_steam_first_launch with a stub client killed mid-run leaves /proc/sys/fs/binfmt_misc/box64 reading enabled.
- [ ] **PL-022** (Low, Q6, Renovation): Four dead assignments, comments that disagree with their code, and parsers in several copies. Acceptance: shellcheck reports no SC2034 for FEX_ARCH_USR_LIB, RUNTIME_DIR, STEAM_MANIFEST_URL or STEAM_CDN on the merged file.
- [ ] **PL-023** (Low, Q7, Renovation): The rotation-table hook is written out in five recipes. Acceptance: Withdrawn with the reason above, or a shared mechanism the build engine offers is named.
- [ ] **PL-024** (Low, Q7, Renovation): `flycast2021-lr` assigns PKG_MAKE_OPTS_TARGET between two functions. Acceptance: tools/pkgcheck flycast2021-lr prints no WARN.
- [ ] **PL-025** (Low, Q4, Renovation): RetroArch's pin is 7,623 commits behind master, and a bump is a re-cut of the patch series. Acceptance: A stream brief names the bump's target, or this item is deferred to a named issue.
- [ ] **PL-026** (Low, Q4, Renovation): Eleven more upstream commits on the slice are `to merge` with the base merge. Acceptance: git log next..upstream/next -- the two directories prints none of the eleven after the base merge.
- [ ] **PL-027** (Low, Q4, Renovation) (#585): Six pins are not on their project's default branch, and four recipes name a moved, renamed or archived repository. Acceptance: A comment on #585 lists the ten recipes with their rows.
- [ ] **PL-028** (Low, Q7, Renovation): Four of the fifteen RetroArch profiles are copies of another, with no base file. Acceptance: Withdrawn with the reason, or a stream brief names it.
- [ ] **PL-029** (Low, Q3, Missing Artifact): No check reads that every core the table names exists where the launcher loads it. Acceptance: The check run over the H700 install tree of 069fc2704421's generation reports pcsx_rearmed32 and mplayer's ffmpeg missing, over the GENERIC_X64 tree the PL-030 and PL-031 cores, and over a tree with them present nothing; systems whose games are .sh files (idtech: runemu.sh runs a .sh ROM itself) are excluded by extension, not by name.
- [ ] **PL-030** (Low, Q6, Interaction Defect): GENERIC_X64's table offers core choices its skip list does not build, and its id Tech scanner calls a script the image lacks. Acceptance: tools/regen-es-systems.sh's GENERIC_X64 table names no retroarch core missing from that image's usr/lib/libretro (the .sh system idtech excluded), and the GENERIC_X64 install tree carries Scan id Tech Games.sh only beside usr/bin/generate-idtech.sh.
- [ ] **PL-031** (Low, Q6, Interaction Defect): Every built table offers RetroArch's `ffmpeg` core for the media player, and no image installs it. Acceptance: No regenerated table names a retroarch ffmpeg core its device's install tree lacks, and the guest's mplayer system lists only the mplayer emulator.
- [ ] **PL-032** (Medium, Q3, Security): Patch 0012 builds a shell line from an achievement's title and description and passes it to system(). Acceptance: On the guest, an award through the loopback provider of an achievement titled with $(touch /tmp/t3-hook) leaves /tmp/t3-hook absent, and a stub achievements hook records the title as one argument ($# = 3).
- [ ] **PL-033** (Low, Q7, Renovation): `99-ninteno-wii-remote.rules` is a misspelt, byte-identical copy of `99-nintendo-wii-remote.rules`. Acceptance: git ls-files retroarch/udev.d lists one Wii remote rule file.

## Pre-existing tracked scope (not punch items)

#336 (the libretro runner: RetroArch's menu and widget items are `deferred:#336` for the 2D cores), #762 (Kronos's options, T1's), #730 (`-P` in the launch line, T1's), #613 (the table's fallback symlink, T2's), #652 (T5: the table's default-marking mechanism, F-06), #669 (T22: grep's PCRE dependency, #806's recipe layer).

Refs #650, #798, #339.

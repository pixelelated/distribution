# Analysis — M6.P2 T6, upstream's helper tools and the other distributions

**Date:** 2026-10-24. **Read at:** `reviewed-at: b96e1ca761`, the slice's bytes `8ebaf8daad`'s; `upstream/next` `e0f9deb899`. Findings are `02`'s `F-NN`; proofs its `P<n>`.

## Executive summary

The slice is LibreELEC's developer tooling under `tools/` and two distributions' identities under `distributions/`: 135 paths and 7,369 lines, 134 of them upstream's and 1 the fork has changed. As a reachability table it comes out as the futro expected, **mostly kept**:
- **Reached** (3 rows, 3 files): `adjust_kernel_config` and `check_kernel_config` from the `Makefile`'s `kconfig-*` targets, and `mtstats.py` after every build.
- **Reached by a document only** (8 rows, 17 files): `pkgcheck` is the one of these the fork depends on.
- **Unreached** (22 rows, 115 files): kept, because every base merge would bring them back, and proposed to ROCKNIX on #585 instead (F-04).

**Six findings, none above Low:**
- **F-02, the one defect in the fork's own row:** `tools/pkgcheck <name>` exits 0 when no recipe matches, like a clean recipe (P7). A `bug`.
- **F-03:** `distributions/LEIoT/kernel_options` is a dangling symlink, LibreELEC's since 2025-04-10 and read only by a `DISTRO=LEIoT` build. A #585 line.
- **F-01 and F-05, doctrine:** `pkgcheck`'s *(upstream's)* in `instruction-files.md` omits the fork's commit; `CLAUDE.md:131` lists the unreached `distro-tool` among the dev helpers. Both for T4 (#651).
- **F-04 and F-06, `Renovation`:** finding 24's class widened to 22 rows; several tools that do one job.

**What the slice does to the two time-to-play numbers: nothing.** No path here is on an image.

## Acceptance-criteria scorecard

#653's sixteen are evaluated in `02` § Criterion entries; the stage-B state is written there.

## Code Quality Assessment

### Strengths

- The three reached tools are short, single-purpose and `bash -n`-clean, with LibreELEC's headers kept.
- `pkgcheck`'s fork change (`81221658b3`) carries the reason in a three-line comment beside the code, and is queued upstream.

### Concerns

- `pkgcheck`'s silent pass on an unknown name (F-02).
- The late-binding list's gaps (a lead for #657).
- Tools that send or destroy, all unreached: `upload_to_filebin`, `checkunpack`, `download-cleaner`, `imgburn.sh`.

### Complexity Hotspots

`tools/distro-tool` (1,097 lines, bash with an embedded Python program) and `tools/mkpkg/` (1,134 lines over 10 files) are the slice's largest. Both are unreached, so neither was read line by line.

## Cornerstone Conformance

Fail-closed applies to `pkgcheck` (F-02). Least surprise applies to `CLAUDE.md:131` (F-05) and `tools/docker/README.md` (F-06). Time to play: untouched.

## Spec Fidelity

### Aligned

Every figure of brief § 2 reproduced at stage A. Every row has its two-way search, verdict, tier, Q4 state and disposition, and every unreached row its `Already written:`. No upstream file is deleted.

### Diverged

- The brief's first caller count gave `pkgcheck` 1; the two-way search gives 14 path hits, all documents.
- `check_kernel_config` is reached by `adjust_kernel_config:38`, which the brief's message-only class did not name.

## Missing Artifacts

None for stage B: `00` to `04` and `review-plan.json` exist; `05` is stage D.

## Risk Assessment

| Risk | From | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| a recipe edit "checked" with a mistyped package name | F-02 | low (a typo) | a late-binding violation ships unseen | exit non-zero when no recipe matched |
| a reader runs `distro-tool` as a helper | F-05 | low | a LibreELEC mirror run with no purpose here | the `CLAUDE.md:131` line corrected |
| a hand-run of an unreached tool that sends or destroys | leads | low (nothing calls them) | a published image, an emptied build root | the #585 proposal; they stay unreached |

## Coverage Boundary

- **Read whole:** `tools/pkgcheck` (the fork-own row), `adjust_kernel_config`, `check_kernel_config` and `upload_to_filebin`.
- **Read for its writes and its header:** every other single tool.
- **Not read line by line:** the directories (`update-functions/` 62, `mkpkg/` 10, `docker/` 7, the two distributions), as a table reads them.
- **Not run:** any tool but `pkgcheck` over a fixture.
- **Not runnable:** shellcheck (absent on the host).

## Finding Verification (Phase 4.5)

Every verdict is asked what result would have produced a FAIL (brief § 5 rule 4):

| Finding or verdict | What would make it false | Checked |
| --- | --- | --- |
| F-02 | `pkgcheck` exiting non-zero, or printing, for an unknown name | P7: exit 0, nothing printed; the violating recipe's exit 1 is the control that the fixture can see a FAIL |
| F-03 | the symlink resolving, or upstream differing | `test -e` false in the checkout; `git diff --quiet upstream/next` identical |
| F-01 | a second fork commit, or upstream's change since the base | `git log` gives exactly one and none upstream |
| an *unreached* verdict | a caller by either pattern, or in a reached tool | the second search found one (`adjust_kernel_config:38` calls `check_kernel_config`); for the 22 unreached rows both patterns are zero, with `pkgcheck` and `adjust_kernel_config` as the positive controls of the same commands |
| *reached by a document only* | a code caller | the path search over `Makefile scripts config .github distributions projects packages` gives none for the 8 rows |
| `Already written: nothing` | a trace in a tree or a root | `release/` 0; other distributions' roots 0; the git-writing tools' subjects 0; the 12 `update to` commits not the tool's (P9) |
| the two distributions unreached | a setter of `DISTRO` other than `config/options:24` | `git grep` over `Makefile config scripts distributions` (P4); `distributions/ROCKNIX/` reached by the same lines is the positive control |

One verdict changed: `check_kernel_config` moved from message-only to reached, found by reading `adjust_kernel_config`. Withdrawn: none.

## Renovation face

### Q1 Modernize

The reached tools use no retired mechanism. `mtstats.py` is Python 3, and the kernel tools call the engine's own `kernel_make`. `tools/docker/` describes six containers the fork does not use, beside the mirrored one (F-06). `update-pkg` already writes the checksum D-WORKFLOW-193 requires.

### Q2 Standards and best practices

- shell 37 of 37 `bash -n` ok;
- the 61 shell helpers ok;
- Python 3 of 3 parse;
- shellcheck not runnable (P5);
- `pkgcheck` obeys the late-binding rule it enforces: it sources no `package.mk`; it reads them as text.

The fail-closed rule is the standard it misses (F-02).

### Q3 Bugs

- **F-02**, the fork-own row: a `bug`.
- **F-03**, upstream's and unreached: a #585 line.
- **Leads on reached rows:** `adjust_kernel_config:32`'s substring match (latent), and `pkgcheck`'s list gaps (for #657).
- **Leads on unreached rows:** `update-pkg:63`'s missing `--fail`; `checkunpack:91`; `download-cleaner`; `upload_to_filebin`'s public uploads.

### Q4 Package currency

The upstream-state table, the 135 against `upstream/next` at `e0f9deb899`:

| Path | Against `upstream/next` (`e0f9deb899`) | The fork's commits since the base |
| --- | --- | --- |
| `distributions/LEIoT/LEIoT.png` | identical | none |
| `distributions/LEIoT/LEIoT_40x40.png` | identical | none |
| `distributions/LEIoT/kernel_options` | identical | none |
| `distributions/LEIoT/options` | identical | none |
| `distributions/LEIoT/show_config` | identical | none |
| `distributions/LEIoT/splash/splash-1080.png` | identical | none |
| `distributions/LEIoT/splash/splash-1200.png` | identical | none |
| `distributions/LEIoT/splash/splash-2160.png` | identical | none |
| `distributions/LEIoT/splash/splash-720.png` | identical | none |
| `distributions/LEIoT/splash/splash-768.png` | identical | none |
| `distributions/LEIoT/version` | identical | none |
| `distributions/LibreELEC/LibreELEC.png` | identical | none |
| `distributions/LibreELEC/LibreELEC_40x40.png` | identical | none |
| `distributions/LibreELEC/addons/Carlito-Bold.ttf` | identical | none |
| `distributions/LibreELEC/addons/addon-bg.png` | identical | none |
| `distributions/LibreELEC/addons/fanart.png` | identical | none |
| `distributions/LibreELEC/addons/overlay-flatpack.png` | identical | none |
| `distributions/LibreELEC/kernel_options` | identical | none |
| `distributions/LibreELEC/options` | identical | none |
| `distributions/LibreELEC/show_config` | identical | none |
| `distributions/LibreELEC/splash/boot-logo.bmp.gz` | identical | none |
| `distributions/LibreELEC/splash/splash-1080.png` | identical | none |
| `distributions/LibreELEC/splash/splash-1200.png` | identical | none |
| `distributions/LibreELEC/splash/splash-2160.png` | identical | none |
| `distributions/LibreELEC/splash/splash-720.png` | identical | none |
| `distributions/LibreELEC/splash/splash-768.png` | identical | none |
| `distributions/LibreELEC/version` | identical | none |
| `tools/RPi/gen-rpi-kodi-patch.sh` | identical | none |
| `tools/RPi/rpi-kodi-rebase.sh` | identical | none |
| `tools/adjust_kernel_config` | identical | none |
| `tools/change_addon_version` | identical | none |
| `tools/check_kernel_config` | identical | none |
| `tools/checkunpack` | identical | none |
| `tools/dashboard` | identical | none |
| `tools/distro-tool` | identical | none |
| `tools/docker/README.md` | identical | none |
| `tools/docker/bookworm/Dockerfile` | identical | none |
| `tools/docker/jammy/Dockerfile` | identical | none |
| `tools/docker/noble/Dockerfile` | identical | none |
| `tools/docker/questing/Dockerfile` | identical | none |
| `tools/docker/resolute/Dockerfile` | identical | none |
| `tools/docker/trixie/Dockerfile` | identical | none |
| `tools/download-cleaner` | identical | none |
| `tools/download-tool` | identical | none |
| `tools/ffmpeg/gen-patches.sh` | identical | none |
| `tools/find_build_warnings.sh` | identical | none |
| `tools/find_build_warnings_ignore.conf` | identical | none |
| `tools/fixlecode.py` | identical | none |
| `tools/icon-generate` | identical | none |
| `tools/imgburn.sh` | identical | none |
| `tools/mkpkg/mkpkg_bcm2835-bootloader` | identical | none |
| `tools/mkpkg/mkpkg_boblightd` | identical | none |
| `tools/mkpkg/mkpkg_libcec` | identical | none |
| `tools/mkpkg/mkpkg_media_build` | identical | none |
| `tools/mkpkg/mkpkg_pvr` | identical | none |
| `tools/mkpkg/mkpkg_rtmpdump` | identical | none |
| `tools/mkpkg/mkpkg_vboxguest` | identical | none |
| `tools/mkpkg/update_binary-addons` | identical | none |
| `tools/mkpkg/update_common_functions` | identical | none |
| `tools/mkpkg/update_retroplayer-addons` | identical | none |
| `tools/moby/gen-patches.sh` | identical | none |
| `tools/mtstats.py` | identical | none |
| `tools/packages-checker` | identical | none |
| `tools/pkgcheck` | differs | `81221658b3` pkgcheck: exit non-zero when any check failed |
| `tools/pkginfo` | identical | none |
| `tools/podman-bin/gen-patches.sh` | identical | none |
| `tools/refresh-patches` | identical | none |
| `tools/repo-tool` | identical | none |
| `tools/update-functions/LibreELEC-settings` | identical | none |
| `tools/update-functions/amlogic-boot-fip` | identical | none |
| `tools/update-functions/aspnet-runtime.py` | identical | none |
| `tools/update-functions/aspnet6-runtime` | identical | none |
| `tools/update-functions/aspnet8-runtime` | identical | none |
| `tools/update-functions/aspnet9-runtime` | identical | none |
| `tools/update-functions/bcm2835-utils` | identical | none |
| `tools/update-functions/bcmstat` | identical | none |
| `tools/update-functions/brcmfmac_sdio-firmware` | identical | none |
| `tools/update-functions/cargo-snapshot` | identical | none |
| `tools/update-functions/ccid` | identical | none |
| `tools/update-functions/chrome` | identical | none |
| `tools/update-functions/cli` | identical | none |
| `tools/update-functions/conmon` | identical | none |
| `tools/update-functions/containerd` | identical | none |
| `tools/update-functions/ctop` | identical | none |
| `tools/update-functions/docker-compose` | identical | none |
| `tools/update-functions/dotnet-runtime` | identical | none |
| `tools/update-functions/dt-overlays` | identical | none |
| `tools/update-functions/dvb-firmware` | identical | none |
| `tools/update-functions/eventlircd` | identical | none |
| `tools/update-functions/extra_commit_body` | identical | none |
| `tools/update-functions/filebrowser` | identical | none |
| `tools/update-functions/fluidsynth` | identical | none |
| `tools/update-functions/glslang` | identical | none |
| `tools/update-functions/gst-plugins-bad` | identical | none |
| `tools/update-functions/gst-plugins-base` | identical | none |
| `tools/update-functions/gstreamer` | identical | none |
| `tools/update-functions/iwlwifi-firmware` | identical | none |
| `tools/update-functions/jellyfin` | identical | none |
| `tools/update-functions/kmsxx` | identical | none |
| `tools/update-functions/libarchive` | identical | none |
| `tools/update-functions/libcec` | identical | none |
| `tools/update-functions/libde265` | identical | none |
| `tools/update-functions/libheif` | identical | none |
| `tools/update-functions/libopenmpt` | identical | none |
| `tools/update-functions/libraw` | identical | none |
| `tools/update-functions/meson-firmware` | identical | none |
| `tools/update-functions/misc-firmware` | identical | none |
| `tools/update-functions/moby` | identical | none |
| `tools/update-functions/pcsc-lite` | identical | none |
| `tools/update-functions/podman-bin` | identical | none |
| `tools/update-functions/polkit` | identical | none |
| `tools/update-functions/rpi_ws281x` | identical | none |
| `tools/update-functions/runc` | identical | none |
| `tools/update-functions/rust` | identical | none |
| `tools/update-functions/rust-std-snapshot` | identical | none |
| `tools/update-functions/rustc-snapshot` | identical | none |
| `tools/update-functions/script.config.vdr` | identical | none |
| `tools/update-functions/shairport-sync` | identical | none |
| `tools/update-functions/snapcast` | identical | none |
| `tools/update-functions/squeezelite` | identical | none |
| `tools/update-functions/tailscale` | identical | none |
| `tools/update-functions/tinc` | identical | none |
| `tools/update-functions/tvheadend43` | identical | none |
| `tools/update-functions/vdr` | identical | none |
| `tools/update-functions/vulkan-headers` | identical | none |
| `tools/update-functions/vulkan-loader` | identical | none |
| `tools/update-functions/vulkan-tools` | identical | none |
| `tools/update-functions/wlan-firmware` | identical | none |
| `tools/update-functions/x264` | identical | none |
| `tools/update-functions/x265` | identical | none |
| `tools/update-pkg` | identical | none |
| `tools/update-scan` | identical | none |
| `tools/upload_to_filebin` | identical | none |
| `tools/viewconfig` | identical | none |
| `tools/viewplan` | identical | none |

134 identical, 1 differs.

**`tools/pkgcheck`'s tier, settled:**
- `git log --oneline upstream/next..8ebaf8daad -- tools/pkgcheck`: `81221658b3 pkgcheck: exit non-zero when any check failed`.
- `git diff --stat upstream/next 8ebaf8daad -- tools/pkgcheck`: `1 file changed, 7 insertions(+)`.
- Upstream since the base: no commit.

The file is LibreELEC's, with one fork commit. The inventory's *fork-own* is right by the plan's definition (§ 2: changed since the merge base). `instruction-files.md`'s *(upstream's)*, and `CLAUDE.md`'s and `AGENTS.md`'s unqualified naming, describe the origin and omit the delta. **The document to correct is `instruction-files.md` § The fork's own tools** (F-01, for T4): `pkgcheck` *(upstream's, with the fork's exit-status commit `81221658b3`, in the upstream series)*.

### Q5 Efficiency

- **On a build:** one `mtstats.py` pipe after each multithread build, and nothing else.
- **On a developer:** `pkgcheck` per recipe edit; `adjust_kernel_config` per `make kconfig-*`.
- **On a reader:** 7,369 lines in every checkout. The unreached rows hold 115 files: `update-functions/` 784 lines, `mkpkg/` 1,134, `distro-tool` 1,097, the two distributions 832.
- **Time to play:** nothing here is on an image.

### Q6 Dead ends

The reachability table: 33 rows, one per tool or tool directory, their file counts summing to 135. For each row:
- **Path hits:** `git grep -l -F "<path>"` over brief § 4's roots, less audits, reviews and QA logs.
- **Name hits:** `git grep -l -w -F "<name>"` over the code roots.
- **The second search of every zero:** `02` § Mechanical checks.

| Tool or directory | Files | Path hits | Name hits | Verdict | Tier | Q4 | Disposition | Already written |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `tools/adjust_kernel_config` | 1 | 2 | 2 | reached by `Makefile:31,34` (`kconfig-olddefconfig-%`, `kconfig-menuconfig-%`) and `.github/workflows/update-kernel-configs-docs.yml:72` (red on the fork, T5's PL-15, #657) | upstream-carried | identical | kept: called by the `Makefile` | **Already written:** n/a: reached |
| `tools/check_kernel_config` | 1 | 2 | 2 | reached by `tools/adjust_kernel_config:38`; also named by the message `packages/linux/package.mk:221` and `projects/ROCKNIX/packages/linux/package.mk:332` print (0 of 28 recorded M7 runs that built `linux` printed it) | upstream-carried | identical | kept: called by `adjust_kernel_config` | **Already written:** n/a: reached |
| `tools/mtstats.py` | 1 | 1 | 1 | reached by `config/multithread:64` (after every finished multithread build; T5's E8 made its failure not the build's) | upstream-carried | identical | kept: called by `config/multithread` | **Already written:** n/a: reached |
| `tools/pkgcheck` | 1 | 14 | 1 | reached by a document only: `CLAUDE.md:109`, `AGENTS.md:343`, `.claude/rules/packaging-and-patches.md:46`, `packages/README.md:274` (run by hand after every recipe edit; no script calls it) | fork-own | differs | kept: the documented recipe lint; its exit-on-no-match defect filed as a `bug` (F-02) | **Already written:** n/a: reached |
| `tools/refresh-patches` | 1 | 1 | 2 | reached by a document only: `packages/README.md:36` (`PKG_NO_REFRESH_PATCHES`); run by hand to regenerate a recipe's patches | upstream-carried | identical | kept: documented hand-run tool | **Already written:** n/a: reached |
| `tools/ffmpeg/gen-patches.sh` | 1 | 3 | 52 (the word `ffmpeg`, not calls) | reached by a document only: `packages/multimedia/ffmpeg/package.mk:14` (`PKG_NO_REFRESH_PATCHES`), a generic recipe no image builds (the ROCKNIX override `projects/ROCKNIX/packages/multimedia/ffmpeg` carries its own patches and does not source it) | upstream-carried | identical | kept: upstream's, documented by an unreached recipe; #585 candidate | **Already written:** nothing: it writes `packages/multimedia/ffmpeg/patches/`, whose last change came from upstream |
| `tools/moby/gen-patches.sh` | 1 | 2 | 4 | reached by a document only: `packages/addons/addon-depends/docker/moby/package.mk:13`, an add-on dependency no fork image builds | upstream-carried | identical | kept: upstream's, documented by an unreached recipe; #585 candidate | **Already written:** nothing: the fork builds no add-on |
| `tools/podman-bin/gen-patches.sh` | 1 | 2 | 3 | reached by a document only: `packages/addons/addon-depends/podman/podman-bin/package.mk:14`, an add-on dependency no fork image builds | upstream-carried | identical | kept: upstream's, documented by an unreached recipe; #585 candidate | **Already written:** nothing: the fork builds no add-on |
| `tools/mkpkg/ (10 files)` | 10 | 0 | 1 | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it makes source tarballs in the working directory; none in any checkout |
| `tools/icon-generate` | 1 | 1 | 1 | reached by a document only: a comment in `packages/addons/service/nqptp/icon/icon-source.svg:7`, an add-on no fork image builds | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it writes an add-on's `resources/`; the fork builds no add-on |
| `tools/distro-tool` | 1 | 0 | 0 | reached by a document only: named in `CLAUDE.md:131`'s list of "dev helpers", with no instruction to run it; no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class); `CLAUDE.md:131`'s list is a Q7 lead for the doctrine slice | **Already written:** nothing: no artifact of it in any checkout or M7 root (no `release/` directory exists anywhere); it writes work files only while it runs |
| `tools/download-tool` | 1 | 1 | 1 | unreached: its only caller, `.github/workflows/update-mirror-sources.yml:30`, is skipped on the fork every week by its repository gate (#644 finding 11; T5's Q6 Table 4) | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing that can be told apart: it fills `sources/` through `scripts/get`, as every build does |
| `tools/update-pkg` | 1 | 0 | 0 | unreached: no caller in the tree; it sources the 62 helpers (`:70`, `:167`) | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: its commits read `<pkg>: update to <ver>` with no trailer, and the twelve fork commits of that shape since the base all carry a `Co-Authored-By: Claude` trailer (sessions, not the tool) |
| `tools/update-functions/ (62 files)` | 62 | 0 | 0 | unreached: sourced only by `tools/update-pkg:70,167`, which nothing calls (two layers) | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: they run only inside `update-pkg` |
| `tools/update-scan` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it queries the network and prints |
| `tools/viewplan` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it prints the build plan |
| `tools/viewconfig` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it prints the configuration |
| `tools/dashboard` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it watches a build's thread logs |
| `tools/pkginfo` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it prints |
| `tools/packages-checker` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it commits `<dir>: automated code cleanup`, and no fork commit since the base has that subject |
| `tools/checkunpack` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class); lead: `:91` `rm -rf "${BUILD}/"*` | **Already written:** nothing: it empties a build root; the 29 M7 roots are populated |
| `tools/repo-tool` | 1 | 0 | 0 | unreached: no caller (it drives `scripts/create_addon`, T5's Table 1) | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: the fork builds no add-on repository |
| `tools/change_addon_version` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it commits `distro: bump ADDON_VERSION`, and no fork commit since the base has that subject |
| `tools/download-cleaner` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class); lead: it removes cached tarballs | **Already written:** nothing that can be told apart: a removed tarball is fetched again by the next build |
| `tools/imgburn.sh` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing in a tree: it `dd`s an image onto a device (`:127`); the fork's route is `docs/device-flashing-runbook.md` |
| `tools/upload_to_filebin` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class); lead: it sends files to public `filebin.net` bins (its example `release/*.tar`) | **Already written:** not readable from here: an upload leaves nothing in a tree |
| `tools/fixlecode.py` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it rewrites recipe text in place when run |
| `tools/find_build_warnings.sh` | 1 | 0 | 0 | unreached: no caller | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: it reports from build logs |
| `tools/find_build_warnings_ignore.conf` | 1 | 0 | 0 | unreached: read only by `tools/find_build_warnings.sh:12`, which nothing calls | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: data |
| `tools/docker/ (7 files)` | 7 | 0 | 52 (the word `docker`: the add-on and `make docker-*`, not this path) | unreached: no caller; the fork's container is the root `Dockerfile`, built by the mirror workflow and pinned in the `Makefile` (T5) | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing in a tree: an image built from one of these lives in a local Docker store, which this lane does not read |
| `tools/RPi/ (2 files)` | 2 | 0 | 29 (the word `RPi`, not calls) | unreached: no caller; they rebase Kodi for Raspberry Pi, which the fork does not build | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: the fork carries no Kodi |
| `distributions/LEIoT/ (11 files)` | 11 | 1 (a record: `docs/rasteratops/p0-sweep-hits.txt`) | 0 | unreached: read by `config/options` only when `DISTRO=LEIoT`, and `config/options:24` (`DISTRO="${DISTRO:-ROCKNIX}"`) is the only setter; the positive control is `distributions/ROCKNIX/`, reached by the same lines | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: no `build.LEIoT-*` root in any checkout |
| `distributions/LibreELEC/ (16 files)` | 16 | 1 (the same record) | 1,542 (the word `LibreELEC`: copyright headers, not selections) | unreached: as LEIoT, `DISTRO=LibreELEC` is set by nothing | upstream-carried | identical | kept: upstream's, unreached; #585 candidate (finding 24's class) | **Already written:** nothing: no `build.LibreELEC-*` root in any checkout |

Rows 33, files 135.

**The shape:** 3 rows reached (3 files), 8 reached by a document only (17), 22 unreached (115). No row's disposition is a deletion. The unreached and the upstream document-only rows are finding 24's class, proposed as one #585 item (`02` § The #644 finding).

### Q7 Clarity and structure

- F-05: `CLAUDE.md:131` lists `distro-tool` as a helper.
- F-01: `pkgcheck`'s tier.
- F-06: several tools for one job; `tools/docker/README.md` against the mirrored container.

The reached tools' headers say what they do.

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

F-02 is the shape `engineering-practices.md` § Guards must fail closed already names (a check that cannot run has not passed). No rule says the documented lint must refuse an empty selection; the tool's own exit is the fix.

### Codification Gaps (needs-new-rule)

None. The ladder's guard for this table, a check that an unreached tool stays unreached, is proposed to the coordinator (`02` § Leads), not written as a rule.

### Recommended Action Sequence

1. F-02's fix in `tools/pkgcheck`, with the fixture first.
2. F-01's and F-05's two doctrine lines, for T4 (#651).
3. F-04's proposal posted on #585 by the coordinator, with F-03 and F-02 named in it.

## Second opinion (Phase 4.6)

Not applicable at Local depth (plan § 6c, D-WORKFLOW-184). `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and the `reason`. No call was made, so there is no provenance file. Phase 4.5 above is done in full in its place.

## Quality Self-Check

- **Counts:** the coverage table's `grep -c` gives 135, and the Q6 rows' files sum to 135.
- **`Already written:`:** every unreached row carries one.
- **Proofs:** the `proved:` cells equal the `PROOF:` lines.
- **Times:** each read from `date -u` in the command that wrote it.

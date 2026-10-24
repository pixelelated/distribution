# Q6 reachability tables (#652)

Generated from `.qa-scratch/t5/q6-callers.tsv` (the search below) and the readings named per row; `04-analysis.md` § Renovation face Q6 cites this file.

## Table 1: the 30 scripts and their callers

Search per script (2026-10-24 04:15 UTC): `git grep -l -F -e "scripts/<n>" -e "SCRIPTS}/<n>" -e "/<n> " -e "/<n>\"" -- . ':!docs' ':!.github/sessions' ':!research' ':!plans' ':!seed'`, the script itself excluded; a zero re-checked with `git grep -l -w -F <n>` before it is a verdict, and then with the dispatch read (`scripts/get` 48 to 53).

| Script | Files naming it | Reached by | Already written |
| --- | ---: | --- | --- |
| `scripts/autoreconf` | 2 | fork build: `config/functions` and `scripts/build` (the autotools step) | - |
| `scripts/autoremove` | 1 | CI only: `scripts/pkgbuilder.py` with `AUTOREMOVE` (upstream's staged graph); no fork build sets it | nothing on the fork: CI's path |
| `scripts/build` | 51 | fork build: every package (`Makefile` `package`, `build_distro`, `install`, the workflows) | - |
| `scripts/build_compat` | 2 | fork build: `scripts/build_distro` (the ARM compatibility root) | - |
| `scripts/build_distro` | 6 | fork build: the `Makefile`'s device targets; CI: three workflows | - |
| `scripts/build_mt` | 8 | CI only: the staged workflows; fork builds never call it (#644 finding 6, T9) | nothing on the fork: CI's path |
| `scripts/ccache_stats` | 0 | **no caller** (both searches zero): a developer helper run by hand (`${TOOLCHAIN}/bin/ccache -s`) | nothing: a script that writes only when run by hand |
| `scripts/checkdeps` | 9 | fork build: every entry point; `config/options` | - |
| `scripts/clean` | 9 | fork build: `Makefile` `package-clean`; documented first step (CLAUDE.md); recipes | - |
| `scripts/create_addon` | 1 | upstream tooling only: `tools/repo-tool` (Kodi add-ons; T6's); no fork build | nothing: no fork image builds an add-on |
| `scripts/create_docker_package` | 0 | **no caller** (both searches zero); its template is `config/docker` (`cp -R config/docker`, line 163) | nothing: it writes an add-on package directory only when run by hand |
| `scripts/extract` | 4 | fork build: `scripts/unpack` | - |
| `scripts/genbuildplan.py` | 2 | fork build: `config/multithread` (the plan every build runs); `tools/viewplan` | - |
| `scripts/get` | 31 | fork build: `scripts/unpack`, `config/functions`, the workflows | - |
| `scripts/get_archive` | 1 | fork build, dynamically: `scripts/get` 48 to 53 (`${SCRIPTS}/get_${get_handler}`); the fixed-string search finds only `tools/distro-tool` | nothing: a script that writes only when run by hand |
| `scripts/get_env` | 13 | fork build: the `Makefile`'s `docker-%` recipe; CI: the workflows | - |
| `scripts/get_file` | 0 | fork build, dynamically: `scripts/get` 48 to 53; both fixed-string searches zero, the dispatch is the reader | - |
| `scripts/get_git` | 0 | fork build, dynamically: `scripts/get` 48 to 53; both fixed-string searches zero, the dispatch is the reader | - |
| `scripts/image` | 13 | fork build: `Makefile` `system`/`release`/`image`/`noobs`, `build_distro` via `make image` | - |
| `scripts/install` | 21 | fork build: `build_distro`, recipes, `scripts/image` | - |
| `scripts/install_addon` | 1 | upstream add-on path only: `scripts/pkgbuild` when a package is an add-on; no fork image builds one | nothing: no fork image builds an add-on |
| `scripts/makefile_helper` | 1 | `Makefile` `clean`/`distclean` | - |
| `scripts/mkimage` | 13 | fork build: `scripts/image` `do_mkimage` | - |
| `scripts/pkgbuild` | 3 | fork build: `config/multithread` (the per-package worker), `scripts/pkgbuilder.py` | - |
| `scripts/pkgbuilder.py` | 1 | fork build: `config/multithread` (the parallel builder every build runs) | - |
| `scripts/pkgjson` | 2 | fork build: `config/multithread` (the plan's input); `tools/viewplan` | - |
| `scripts/test-audit-review.py` | 0 | **no caller** in the tree, the workflows or the hooks: the code-auditor's own offline test (#378), misfiled into this area by the `scripts/**` glob (a lead for `areas.json`) | nothing: it writes only a temporary directory |
| `scripts/uboot_helper` | 5 | fork build: the bootloader recipes (`u-boot`, `rkbin`, `crust`) and `projects/*/bootloader` | - |
| `scripts/unpack` | 10 | fork build: every package with a source | - |
| `scripts/update_packages` | 1 | `Makefile` `update` only; never run on the fork (#644 finding 15, T7/T8) | nothing on the fork: `make update` rewrites `PKG_VERSION`s when run, and it has not been |

## Table 2: the 139 system fragments against the five devices' tables

Each device's table regenerated from this tree with T3's script (`tools/regen-es-systems.sh`) and the build's own `xmlstarlet`: GENERIC_X64 128 systems, H700 126, RK3326 126, RK3566 132, SM8550 139; GENERIC_X64, H700 and SM8550 byte-identical to their install trees (P3, P11). **Every fragment is named by at least one device's table, and every system in the five tables has a fragment.**

| Fragment | Devices whose table names it |
| --- | --- |
| `config/emulators/3do.conf` | all five |
| `config/emulators/3ds.conf` | RK3566, SM8550 |
| `config/emulators/amiga.conf` | all five |
| `config/emulators/amigacd32.conf` | all five |
| `config/emulators/amstradcpc.conf` | all five |
| `config/emulators/arcade.conf` | all five |
| `config/emulators/arduboy.conf` | all five |
| `config/emulators/atari2600.conf` | all five |
| `config/emulators/atari5200.conf` | all five |
| `config/emulators/atari7800.conf` | all five |
| `config/emulators/atari800.conf` | all five |
| `config/emulators/atarijaguar.conf` | all five |
| `config/emulators/atarilynx.conf` | all five |
| `config/emulators/atarist.conf` | all five |
| `config/emulators/atomiswave.conf` | all five |
| `config/emulators/bbcmicro.conf` | all five |
| `config/emulators/bk.conf` | all five |
| `config/emulators/c128.conf` | all five |
| `config/emulators/c16.conf` | all five |
| `config/emulators/c64.conf` | all five |
| `config/emulators/cdi.conf` | all five |
| `config/emulators/channelf.conf` | all five |
| `config/emulators/chip-8.conf` | all five |
| `config/emulators/colecovision.conf` | all five |
| `config/emulators/cps1.conf` | all five |
| `config/emulators/cps2.conf` | all five |
| `config/emulators/cps3.conf` | all five |
| `config/emulators/daphne.conf` | all five |
| `config/emulators/doom.conf` | all five |
| `config/emulators/dreamcast.conf` | all five |
| `config/emulators/easyrpg.conf` | all five |
| `config/emulators/famicom.conf` | all five |
| `config/emulators/fbn.conf` | all five |
| `config/emulators/fds.conf` | all five |
| `config/emulators/gameandwatch.conf` | all five |
| `config/emulators/gamecube.conf` | GENERIC_X64, RK3566, SM8550 |
| `config/emulators/gamegear.conf` | all five |
| `config/emulators/gb.conf` | all five |
| `config/emulators/gba.conf` | all five |
| `config/emulators/gbah.conf` | all five |
| `config/emulators/gbav.conf` | all five |
| `config/emulators/gbc.conf` | all five |
| `config/emulators/gbch.conf` | all five |
| `config/emulators/gbh.conf` | all five |
| `config/emulators/genesis.conf` | all five |
| `config/emulators/genh.conf` | all five |
| `config/emulators/ggh.conf` | all five |
| `config/emulators/gp32.conf` | all five |
| `config/emulators/heroic.conf` | SM8550 |
| `config/emulators/idtech.conf` | all five |
| `config/emulators/imageviewer.conf` | all five |
| `config/emulators/intellivision.conf` | all five |
| `config/emulators/ios.conf` | all five |
| `config/emulators/j2me.conf` | all five |
| `config/emulators/macintosh.conf` | all five |
| `config/emulators/mame.conf` | all five |
| `config/emulators/mastersystem.conf` | all five |
| `config/emulators/megacd.conf` | all five |
| `config/emulators/megadrive.conf` | all five |
| `config/emulators/megadrive-japan.conf` | all five |
| `config/emulators/megadriveh.conf` | all five |
| `config/emulators/megaduck.conf` | all five |
| `config/emulators/moonlight.conf` | all five |
| `config/emulators/moto.conf` | all five |
| `config/emulators/mplayer.conf` | all five |
| `config/emulators/msx.conf` | all five |
| `config/emulators/msx2.conf` | all five |
| `config/emulators/music.conf` | all five |
| `config/emulators/n64.conf` | all five |
| `config/emulators/n64dd.conf` | all five |
| `config/emulators/naomi.conf` | all five |
| `config/emulators/nds.conf` | all five |
| `config/emulators/ndsiware.conf` | all five |
| `config/emulators/neocd.conf` | all five |
| `config/emulators/neogeo.conf` | all five |
| `config/emulators/nes.conf` | all five |
| `config/emulators/nesh.conf` | all five |
| `config/emulators/ngp.conf` | all five |
| `config/emulators/ngpc.conf` | all five |
| `config/emulators/odyssey2.conf` | all five |
| `config/emulators/openbor.conf` | all five |
| `config/emulators/palm.conf` | all five |
| `config/emulators/pc.conf` | all five |
| `config/emulators/pc-8800.conf` | all five |
| `config/emulators/pc-9800.conf` | all five |
| `config/emulators/pcengine.conf` | all five |
| `config/emulators/pcenginecd.conf` | all five |
| `config/emulators/pcfx.conf` | all five |
| `config/emulators/pet.conf` | all five |
| `config/emulators/pico-8.conf` | all five |
| `config/emulators/pokemini.conf` | all five |
| `config/emulators/ports.conf` | all five |
| `config/emulators/ps2.conf` | RK3566, SM8550 |
| `config/emulators/ps3.conf` | SM8550 |
| `config/emulators/psp.conf` | all five |
| `config/emulators/pspminis.conf` | all five |
| `config/emulators/psvita.conf` | RK3566, SM8550 |
| `config/emulators/psx.conf` | all five |
| `config/emulators/satellaview.conf` | all five |
| `config/emulators/saturn.conf` | all five |
| `config/emulators/scummvm.conf` | all five |
| `config/emulators/scv.conf` | all five |
| `config/emulators/sega32x.conf` | all five |
| `config/emulators/segacd.conf` | all five |
| `config/emulators/segamodel3.conf` | SM8550 |
| `config/emulators/sfc.conf` | all five |
| `config/emulators/sg-1000.conf` | all five |
| `config/emulators/snes.conf` | all five |
| `config/emulators/snesh.conf` | all five |
| `config/emulators/snesmsu1.conf` | all five |
| `config/emulators/st-v.conf` | all five |
| `config/emulators/steam.conf` | SM8550 |
| `config/emulators/sufami.conf` | all five |
| `config/emulators/supergrafx.conf` | all five |
| `config/emulators/supervision.conf` | all five |
| `config/emulators/tg16.conf` | all five |
| `config/emulators/tg16cd.conf` | all five |
| `config/emulators/tic-80.conf` | all five |
| `config/emulators/tools.conf` | all five |
| `config/emulators/triforce.conf` | SM8550 |
| `config/emulators/uzebox.conf` | all five |
| `config/emulators/vectrex.conf` | all five |
| `config/emulators/vic20.conf` | all five |
| `config/emulators/videopac.conf` | all five |
| `config/emulators/vircon32.conf` | all five |
| `config/emulators/virtualboy.conf` | all five |
| `config/emulators/wasm4.conf` | all five |
| `config/emulators/wii.conf` | GENERIC_X64, RK3566, SM8550 |
| `config/emulators/wiiu.conf` | SM8550 |
| `config/emulators/wiiware.conf` | RK3566, SM8550 |
| `config/emulators/windows.conf` | all five |
| `config/emulators/wonderswan.conf` | all five |
| `config/emulators/wonderswancolor.conf` | all five |
| `config/emulators/x1.conf` | all five |
| `config/emulators/x68000.conf` | all five |
| `config/emulators/xbox.conf` | SM8550 |
| `config/emulators/zmachine.conf` | all five |
| `config/emulators/zx81.conf` | all five |
| `config/emulators/zxspectrum.conf` | all five |

## Table 3: the three other configuration trees

| Tree | Reader | Reached by a fork build or image | Already written |
| --- | --- | --- | --- |
| `config/noobs/**` (15) | `scripts/image` 360 to 362, in the `noobs` mode only (`make noobs`) | no: no fork target or workflow runs `noobs`; the five devices build no NOOBS release | nothing |
| `config/addon/**` (7) | `config/functions` 1587 (`cp $ROOT/config/addon/${PKG_ADDON_TYPE}.xml`), the add-on packaging path | no: `DRIVER_ADDONS_SUPPORT="no"` (`distributions/ROCKNIX/options` 61); no fork image builds a Kodi add-on | nothing |
| `config/docker/**` (7) | `scripts/create_docker_package` 163 (`cp -R config/docker`), which nothing calls | no | nothing |

All three stay: upstream (LibreELEC) reaches them and the fork merges upstream through them (D-WORKFLOW-185's shape: unshipped is not dead when upstream reaches it). No removal is proposed.

## Table 4: the 19 upstream workflow files on the fork

Read 2026-10-24 04:08 UTC: `gh workflow list --repo pixelelated/distribution --all` (all 18 `.yml` active, beside the 4 `fork-*` and GitHub's Copilot agent) and `gh run list --repo pixelelated/distribution --workflow <file> --limit 3 --json conclusion,status,createdAt,event` per file; triggers, gates and secrets from each file. T10 decides the fork's gates; this table says what each would do here.

| Workflow | Trigger | On the fork | Result read by | Already written |
| --- | --- | --- | --- | --- |
| `.github/workflows/ai-usage.yml.disabled` | `pull_request_target` (as written) | not a workflow to GitHub (the `.disabled` suffix); last runs: could not find any workflows named ai-usage.yml.disabled | - | nothing |
| `.github/workflows/build-aarch64-emu-libretro.yml` | `workflow_call` from `build-device.yml` | only under `Build`; needs `GH_PAT` (absent on the fork); last runs: no runs | - | nothing |
| `.github/workflows/build-aarch64-emu-standalone.yml` | `workflow_call` | the same; `GH_PAT`; last runs: no runs | - | nothing |
| `.github/workflows/build-aarch64-image.yml` | `workflow_call` | the same; the three scraper/achievement secrets (absent); last runs: no runs | - | nothing |
| `.github/workflows/build-aarch64-mame-lr.yml` | `workflow_call` | the same; `GH_PAT`; last runs: no runs | - | nothing |
| `.github/workflows/build-aarch64-qt6.yml` | `workflow_call` | the same; `GH_PAT`; last runs: no runs | - | nothing |
| `.github/workflows/build-aarch64-rust.yml` | `workflow_call` | the same; last runs: no runs | - | nothing |
| `.github/workflows/build-aarch64-toolchain.yml` | `workflow_call` | the same; `GH_PAT`; last runs: no runs | - | nothing |
| `.github/workflows/build-aarch64.yml` | `workflow_call` | the same; `GH_PAT`; last runs: no runs | - | nothing |
| `.github/workflows/build-arm.yml` | `workflow_call` | the same; `GH_PAT`; last runs: no runs | - | nothing |
| `.github/workflows/build-device.yml` | `workflow_call` from `build-nightly.yml` | the same; last runs: no runs | - | nothing |
| `.github/workflows/build-docker-image.yml` | `workflow_call` | the same; it would push `ghcr.io/<owner>/rocknix-build` with `GITHUB_TOKEN`; last runs: no runs | - | nothing |
| `.github/workflows/build-nightly.yml` | `schedule` daily 00:00 UTC; `workflow_dispatch` | **runs daily and ends `startup_failure`** (a repository gate on `ROCKNIX` evaluated after startup; `NIGHTLY_APP_*`, `SF_SSH_KEY` absent): #644 finding 19, T10; last runs: 2026-10-24 schedule startup_failure; 2026-10-23 schedule startup_failure; 2026-10-22 schedule startup_failure | nobody | nothing: no job starts |
| `.github/workflows/check-freeze-period.yml` | `workflow_call` (from `validate-pull-request.yml`) | only with a PR to the fork's `next`; `ubuntu-24.04` (fork edit `3d7c075f63`); last runs: no runs | the PR's checks | nothing |
| `.github/workflows/retry-workflow.yml` | `workflow_dispatch` | only by hand; last runs: no runs | - | nothing |
| `.github/workflows/trigger-fail-if-upstream-changed.yml` | `pull_request` on `packages/**` | only with a PR to the fork that touches `packages/` (none has run); last runs: no runs | the PR's checks | nothing |
| `.github/workflows/update-kernel-configs-docs.yml` | `push` to `next` touching `projects/ROCKNIX/packages/linux/package.mk`; `workflow_dispatch`, `workflow_call` | **runs on the fork and fails**: 2026-09-04, 09-19, 09-28 (no repository gate; needs `NIGHTLY_APP_*`, absent). Not in #644's findings; last runs: 2026-09-28 push failure; 2026-09-19 push failure; 2026-09-04 push failure | nobody | nothing: it fails before it commits |
| `.github/workflows/update-mirror-sources.yml` | `schedule` weekly Sunday 22:00; `workflow_dispatch`, `workflow_call` | runs weekly and is `skipped` by its repository gate (10-04, 10-12, 10-18): #644 finding 11; last runs: 2026-10-18 schedule skipped; 2026-10-12 schedule skipped; 2026-10-04 schedule skipped | nobody | nothing |
| `.github/workflows/validate-pull-request.yml` | `pull_request` to `next`, `merge_group` | only with a PR to the fork's `next`; `ubuntu-24.04` (fork edits `3d7c075f63`, `7bd7f31312`); last runs: no runs | the PR's checks | nothing |

## Table 5: `.merge-head` and `scripts/test-audit-review.py`

| Unit | Reader | Note |
| --- | --- | --- |
| `.merge-head` (`d43d166b7a…`) | none in this tree or `upstream/next` (`git grep -n -F 'merge-head'`, code paths: zero) | upstream's record of the LibreELEC `master` commit its merge `96aff382c4` (2026-08-11) brought in (LibreELEC PR #11671); a human's marker for the next LibreELEC merge. Keep; unreached by any build, image or CI. Already written: nothing |
| `scripts/test-audit-review.py` | none (Table 1) | the code-auditor's offline test for reviewer independence (#378, `5150320de2`); classed `build-engine` by the `scripts/**` glob. Belongs with `tools/lint-audit-artifacts` (`tooling-and-guards`): a lead for the coordinator's `areas.json`. Not run by `fork-checks.yml` either. Already written: nothing |


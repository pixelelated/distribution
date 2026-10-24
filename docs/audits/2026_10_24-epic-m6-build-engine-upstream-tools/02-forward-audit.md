# Forward Audit — M6.P2 T6, upstream's helper tools and the other distributions

**Auditor:** Code Auditor skill, primary Claude Opus 5.5 at high effort; depth Local (plan § 6c, D-WORKFLOW-184)
**Date:** 2026-10-24
**Subject:** #653 (`M6.P2 E800/T6`), slice `build-engine-upstream-tools`; `reviewed-at: b96e1ca761`, the slice's bytes `8ebaf8daad`'s
**Spec:** `docs/reviews/briefs/build-engine-upstream-tools.md` version 2; #653's sixteen criteria

---

## Running Notes

A table slice: one row per path, read for reachability. A file is read line by line only where a row needs it: the one fork-own row (`tools/pkgcheck`, read whole) and the three reached tools (`adjust_kernel_config`, `check_kernel_config`, `mtstats.py`, read for Q2 and Q3). Every caller is a `git grep` hit with its file:line at `8ebaf8daad`. A tool is read to learn its reach and never run; the one tool run is `tools/pkgcheck`, a reader, over a fixture tree. **Can this be done on the VM? No**: these tools and files are on no image (brief § 5).

## Mechanical checks (brief § 5)

| Check | Command | Exit | Summary |
| --- | --- | --- | --- |
| The slice's paths | brief § 5's inventory filter into `.qa-scratch/t6/paths.txt` | 0 | 135 |
| Branch against hash, the 135 | `git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t6/paths.txt)` | 0 | empty |
| Branch against hash, the two roots | `git diff --stat 8ebaf8daad HEAD -- tools distributions ':!distributions/ROCKNIX'` | 0 | 15 files, all fork-only and outside the 135 (`01` § Scope names each with its owner) |
| Q4, upstream state | the loop over `paths.txt` with `git diff --quiet upstream/next 8ebaf8daad -- <path>` (`upstream/next` `e0f9deb899`) | 0 | **1 differs** (`tools/pkgcheck`), 134 identical |
| The two-way caller count, 24 single tools | brief § 5's loop: `git grep -l -F "tools/<t>"` over `Makefile scripts config .github/workflows distributions projects packages docs .claude CLAUDE.md AGENTS.md` (less `docs/qa-logs`, `docs/reviews`, `docs/audits`), then `git grep -l -w -F "<t>"` over the code roots | 0 | nonzero: `refresh-patches` 1/2, `pkgcheck` 14/1, `adjust_kernel_config` 2/2, `check_kernel_config` 2/2, `mtstats.py` 1/1, `download-tool` 1/1, `icon-generate` 1/1, `mkpkg` 0/1; the other 16 are 0/0. **Positive controls:** `pkgcheck` and `adjust_kernel_config` come out reached, so a zero from the same command is a zero |
| Every zero, the second way (blindspot 22) | the bare name over `docs .claude CLAUDE.md AGENTS.md packages/README.md` (less audits, reviews, qa-logs, work logs, the P0 sweep record), and inside `tools/` for a caller among the 135 | 0 | `distro-tool` named once (`CLAUDE.md:131`); every other zero stays zero. Read by hand: `tools/adjust_kernel_config:38` calls `tools/check_kernel_config` |
| The directories | the path and the directory's name, and its files' names, over the same roots | 0 | `tools/ffmpeg` 3, `tools/moby` 2, `tools/podman-bin` 2 (each its recipe's `PKG_NO_REFRESH_PATCHES` and patch headers); `tools/mkpkg` 0 (the name twice in `config/functions` messages); `tools/docker`, `tools/RPi`, `tools/update-functions` 0; the bare words `docker`, `RPi`, `ffmpeg`, `LibreELEC` hit 52, 29, 52 and 1,542 times in other senses and were classed by the path search, not read one by one |
| `update-functions` | `git grep -n -F 'update-functions' 8ebaf8daad -- tools/update-pkg tools/update-scan scripts config Makefile .github` | 0 | `tools/update-pkg:70`, `:167` only |
| `DISTRO=` | `git grep -n -E 'DISTRO=|DISTRO:=' 8ebaf8daad -- Makefile config scripts distributions` | 0 | `config/options:24` `DISTRO="${DISTRO:-ROCKNIX}"` is the only setter; `scripts/image:36`, `scripts/build_compat:35` pass it on; `scripts/checkdeps:47-54`'s `DISTRO` is the host's OS name in its own process |
| The syntax sweep | `bash -n` on every shell file at the hash (shebang-detected, plus the two `options` with no shebang and the 61 shell helpers of `update-functions`); `python3 -I -B -c ast.parse` on the 3 Python files | 0 | **shell 37 of 37 ok; helpers 61 of 61 ok; Python 3 of 3 parse** (`aspnet-runtime.py` is the helpers' one Python file) |
| shellcheck | `command -v shellcheck` | 1 | **not runnable**: not on the host. Recorded as not run, not as a pass |
| The tier of `tools/pkgcheck` | `git log --oneline upstream/next..8ebaf8daad -- tools/pkgcheck`; `git diff --stat upstream/next 8ebaf8daad -- tools/pkgcheck`; upstream's log since the base | 0 | one fork commit, `81221658b3` (+7 lines); upstream untouched since the base |
| What a hand-run tool left | `ls -d /workspace/repos/rocknix.worktrees/*/release` and the fork's checkouts (read only) | 0 | **0** `release/` directories; 29 `sources/` directories (the shared cache's mount points or builds' own), which cannot tell a hand-run `download-tool` from a build |
| The kernel-options message | `grep -c 'kernel options not correct'` over the recorded M7 build logs, through the filter (read only) | 0 | 0 of 28 runs that built `linux` |
| The git-writing tools' commits | `git log --grep` for `automated code cleanup`, `bump ADDON_VERSION`, `addons: reset version`, `: update to [0-9a-f]` from the merge base to `8ebaf8daad` | 0 | 0, 0, 0; 12 `update to` commits, each with a `Co-Authored-By: Claude` trailer that `update-pkg` (`:161-171`) never writes |
| Other distributions' roots | `ls -d .../build.LibreELEC* .../build.LEIoT*` across the checkouts (read only) | 0 | 0 |

## Findings, written as each row is read

### F-01 (Q4, Q7; Low; doctrine): `tools/pkgcheck` is upstream's file with a fork commit; the rules call it simply *upstream's*

The inventory's tier is *fork-own*, by the plan's rule (changed since the merge base, § 2). `instruction-files.md` § The fork's own tools lists it as `pkgcheck` *(upstream's)*, and `CLAUDE.md` and `AGENTS.md` introduce it as the only lint. `git log upstream/next..8ebaf8daad -- tools/pkgcheck` gives one commit, `81221658b3` (2026-09-12, "pkgcheck: exit non-zero when any check failed", +7 lines). Upstream has not touched the file since the base, and the change is already in the upstream series (`docs/pr-series/map.txt:20`). Neither document is wrong about what it claims: the inventory names the delta, the rule names the origin. The rule leaves out that the fork's copy differs and that the difference is queued upstream. A doctrine edit for T4 (#651), not a code change.

### F-02 (Q3; Low; the fork-own row): `tools/pkgcheck <name>` exits 0 when no recipe matches the name

`tools/pkgcheck` 155 to 161 loop over `find packages projects -type f -path */${arg}/package.mk`, and line 169 ends `[ ${FAILS} -eq 0 ]`. A name that matches no recipe processes nothing, so `FAILS` is 0 and the script exits 0, printing nothing, exactly as for a clean recipe. A mistyped package name reads as a pass (`engineering-practices.md` § Guards must fail closed). Upstream's copy behaves the same: before the fork's change it always exited 0. The fixture (P7): a clean recipe exits 0 with no FAIL; a global-scope `${PKG_BUILD}` exits 1 with one FAIL, the positive control; `fixture-no-such-package` exits 0 with nothing printed. A `bug` (D-WORKFLOW-187), and a #585 line beside `81221658b3`'s.

Also read, as leads for #657 and not this slice's fix: the late-binding list (47 to 61) names `PKG_BUILD`, the compilers and the `*_OPTS` families, but not `TOOLCHAIN`, `SYSROOT_PREFIX` or `INSTALL`, so a global-scope reference to those is not caught. `for arg in ${@}` (156) and the unquoted `-path */${arg}/package.mk` (157) expand against the working directory.

### F-03 (Q3; Low; upstream's, unreached): `distributions/LEIoT/kernel_options` is a dangling symlink

The symlink's target is `distributions/LibreELEC/kernel_options`. A relative symlink resolves from its own directory, so it points at `distributions/LEIoT/distributions/LibreELEC/kernel_options`, which does not exist: `test -e distributions/LEIoT/kernel_options` is false in the checkout (P8). LibreELEC added it so (`4130b59b50`, 2025-04-10), and upstream carries it identically. Only a `DISTRO=LEIoT` build reads it, through `packages/linux/package.mk:207` and `tools/check_kernel_config:10`, whose `[ -f ... ]` is then false, so a LEIoT build silently skips its kernel options. Nothing the fork builds sets `DISTRO=LEIoT`: a #585 line for LibreELEC, not a fork bug.

### F-04 (Q6; Renovation): finding 24's class, 22 tools and directories that nothing the fork runs reaches

The reachability table (`04` § Q6) has 33 rows over the 135 files:
- **Reached** (3 rows, 3 files): `adjust_kernel_config` by `Makefile:31,34`; `check_kernel_config` by `adjust_kernel_config:38`; `mtstats.py` by `config/multithread:64`.
- **Reached by a document only** (8 rows, 17 files): `pkgcheck`, `refresh-patches`, the three `gen-patches.sh`, `mkpkg/`, `icon-generate`, `distro-tool`.
- **Unreached** (22 rows, 115 files).

Every unreached row carries its `Already written:`, and none found anything a hand-run tool left. By brief § 2's policy nothing is removed: the rows are upstream's, every base merge would bring them back, and the class goes to ROCKNIX as one proposal on #585 (D-WORKFLOW-164, held by D-WORKFLOW-165).

### F-05 (Q7; Low; doctrine): `CLAUDE.md:131` lists `distro-tool` among the "dev helpers"

`CLAUDE.md:131` reads "`tools/` — dev helpers (`pkgcheck`, `distro-tool`, `adjust_kernel_config`)". `distro-tool` is LibreELEC's mirror tool, called by nothing in the tree; the other two are reached. A reader takes it for a helper to run. A doctrine edit for T4 (#651).

### F-06 (Q7; Renovation): several tools for one job

- `tools/update-pkg` and `tools/update-scan` beside `scripts/update_packages`, the version bump T5 changed (E6). None of the three is run on the fork.
- `tools/pkgcheck`, `tools/packages-checker` and `tools/fixlecode.py` all check or rewrite recipe style. Only `pkgcheck` is the documented lint.
- `tools/imgburn.sh` beside the fork's flashing route, `docs/device-flashing-runbook.md`.

Each pair is named with the reached one. They are kept, and listed in F-04's #585 proposal.

### Leads (not findings of this slice)

- `tools/upload_to_filebin` posts its arguments to public `filebin.net` bins; its usage example is `release/*.tar`. On this host an image can carry a personal credential compiled in (`device-builds.md` § Build credentials), so the tool is a publication route outside that policy. Unreached; named in F-04's proposal.
- `tools/checkunpack:91` runs `rm -rf "${BUILD}/"*`. `tools/download-cleaner` 101 to 113 remove and move cached tarballs. Both unreached.
- `tools/update-pkg:63` calls `curl` without `--fail`, so it would hash an HTTP error page as the checksum. Unreached.
- `tools/adjust_kernel_config:32` matches the config command by substring. It is reached by the `Makefile`; latent.
- **The ladder** (brief § 4): a guard that a tool the table calls *unreached* stays unreached (#838's cousin). Proposed for the coordinator to file, not built here.

### Leads from the sweeps (stage E, S1 and S2)

`tools/pkgcheck` with no argument over every recipe (P13): 12 FAIL lines at `8ebaf8daad` and after S1, the same 12; 21 after S2. Not fixed here (brief § 5: the 135 are this slice's; the recipes are T7's and T8's). Each line read at its site:

| Recipe and line | FAIL | Since | Read | For |
| --- | --- | --- | --- | --- |
| `projects/ROCKNIX/packages/sysutils/systemd/package.mk:105` | ref `BUILD_WITH_DEBUG` | S2 | real: `source_package` unsets it before the load (`config/functions:1303`), so the global `if [ -n ... ]` is always false and `-Ddebug-tty` is never added; `upstream/next` carries the same branch (its `:118`) | T8; a #585 candidate |
| `projects/ROCKNIX/packages/virtual/image/package.mk:109`, `:110` | ref `INSTALL` | S2 | real: `mkdir -p` and `ln -sf /storage/.opt` on `${INSTALL}` at global scope run on every sourcing, with `config/path`'s `$BUILD/image/system`; ROCKNIX's `3335fc7b76`, identical upstream | T8; a #585 candidate |
| `projects/ROCKNIX/packages/emulators/libretro/sameboy-lr/package.mk:13` | ref `PKG_BUILD` | before | real: `PKG_BUILD` is empty at load (`packages/README.md` § Late Binding), so the make options carry `BOOTROMS_DIR=/BootROMs/prebuilt`; already **#818** (`bug`, open) | T8 (#818) |
| `packages/addons/tools/jre.zulu/package.mk:12` | ref `PKG_SHORTDESC` | before | not classified: depends on whether the recipe sets it above; identical upstream | T7 |
| `packages/graphics/mesa-reusable/package.mk:14` | ref `PKG_SOURCE_NAME` | before | not classified, as above; identical upstream | T7 |
| `projects/ROCKNIX/packages/apps/moonlight/package.mk` | duplicate `post_makeinstall_target()` (`:23`, `:39`, both indented) | before | not classified: two definitions in branches may be deliberate | T8 |
| `packages/audio/wireplumber/package.mk:40`, `:48` | ref `INSTALL` | S2 | false: inside `post_makeinstall_target` (23 to 53); the parser ends a function at a heredoc's column-0 `}` | T7; the parser lead below |
| `projects/ROCKNIX/packages/audio/wireplumber/package.mk:43`, `:51`, `:57`, `:65`, `:100` | ref `INSTALL` (`:100` also `PKG_DIR`, before S2) | S2 | false, as above (the function is 23 to 102) | T8; the parser lead |
| `projects/ROCKNIX/packages/audio/wireplumber/package.mk:99` | ref `PKG_DIR` | before | false, as above | T8; the parser lead |
| both `wireplumber` recipes | duplicate function def (6 lines: `main =`, `wireplumber.profiles =`, `actions =`, `update-props =`) | before | false: Lua tables inside heredocs read as functions | the parser lead |

- **The parser lead (for #657):** `pkgcheck` takes any column-0 `}` as a function's end and any `<name> = {` line as a definition, so a heredoc inside a function yields false FAILs: 14 of the 21 after S2, all in the two `wireplumber` recipes. Skipping heredoc bodies is the fix; not done here (brief § 4 Q3: not a rewrite in this slice).
- **`SYSROOT_PREFIX` stays off the list** (P14): it keeps its value until `scripts/build:471`, after `post_make`, and its 66 global uses are configure, cmake, make and unpack options, where that value is the right one. A trial sweep with it listed gave 87 FAIL lines. A recipe that uses it at global scope for an install would be wrong, and the lint cannot tell the two apart.
- **`TOOLCHAIN` is not late** (P14), correcting PL-06's text and `03` § 3.2: `config/options:185` sources `config/path` before the recipe (`source_package`, `:197`), and nothing resets it.

## The #644 finding

**Finding 24** (`docs/reviews/build-path-read.md:177`): *"LibreELEC's `tools/update-scan`, `update-pkg`, `distro-tool`, `refresh-patches` are carried and unused by any ROCKNIX workflow"*, marked *candidate*; carrier T6.

| Tool it names | This slice's verdict | Disposition |
| --- | --- | --- |
| finding 24: `tools/update-scan` | unreached: no caller | kept: upstream's; #585 |
| finding 24: `tools/update-pkg` | unreached: no caller (it sources the 62 helpers) | kept: upstream's; #585 |
| finding 24: `tools/distro-tool` | reached by a document only (`CLAUDE.md:131`'s list; F-05) | kept: upstream's; #585; the list line to T4 |
| finding 24: `tools/refresh-patches` | reached by a document only (`packages/README.md:36`) | kept: documented hand-run tool |

**Disposition:** finding 24 holds for three of its four tools, and the table widens it to the 22 unreached rows (F-04). `refresh-patches` is documented in `packages/README.md` as the tool `PKG_NO_REFRESH_PATCHES` points around, so it is not dead to a contributor. **The #585 proposal's text**, for the coordinator to post (brief § 10):

> **ROCKNIX: the LibreELEC tools no ROCKNIX workflow runs.** The fork's reachability table (#653, `docs/audits/2026_10_24-epic-m6-build-engine-upstream-tools/04-analysis.md` § Q6) found nothing in `ROCKNIX/distribution` that calls these tools:
> - `update-pkg` with its 62 `update-functions/` helpers, `update-scan`;
> - `distro-tool`, `download-cleaner`, `checkunpack`, `repo-tool`, `change_addon_version`, `packages-checker`, `fixlecode.py`, `find_build_warnings.sh` with its `.conf`;
> - `viewplan`, `viewconfig`, `dashboard`, `pkginfo`;
> - `imgburn.sh`, `upload_to_filebin`;
> - `docker/` (six other distributions' containers), `RPi/`;
> - `distributions/LibreELEC/` and `distributions/LEIoT/`, which `DISTRO` never selects.
>
> `download-tool` is reached only by `update-mirror-sources.yml`, which ROCKNIX's own gate keeps to the upstream repository. Two defects on the way, if they stay: `distributions/LEIoT/kernel_options` is a dangling symlink, and `tools/pkgcheck` exits 0 for a package name that matches no recipe. Proposed: drop them, or say in `tools/README` which ones are LibreELEC's and kept on purpose. The fork removes nothing until ROCKNIX decides, because every base merge would bring them back.

**The other 25 findings and their carriers** (none taken here):
- **T5:** 1, 3, 4, 8, 9, 11, 13, 22.
- **T4:** 2, 14; and 18 with #645.
- **T9:** 5, 6, 7.
- **T7 and T8:** 15. **T8:** 16.
- **#645:** 17.
- **T10:** 19, 21.
- **#637's lane:** 20.
- **T12:** 23.
- **T32:** 25.
- **#585:** 10, 26.
- **T11:** 12.

## Coverage table: one row per path (135)

Generated by `tools/t6-tables.py coverage` (committed beside this file). It reads one list of the 33 groups, the per-path syntax result (`.qa-scratch/t6/syntax.txt`) and the upstream state (`.qa-scratch/t6/q4-upstream.txt`), and asserts 135 paths, each in exactly one group. Q6's cell is the verdict; `04` § Q6 carries each group's search counts, disposition and `Already written:`.

| Path | Tier | Lines | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `distributions/LEIoT/LEIoT.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/LEIoT_40x40.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/kernel_options` | upstream-carried | 1 | n/a | n/a: not a script (symlink) | F-03: a symlink to `distributions/LibreELEC/kernel_options`, relative to its own directory, so it dangles (since LibreELEC's `4130b59b50`, 2025-04-10; identical upstream); only a `DISTRO=LEIoT` build reads it | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/options` | upstream-carried | 271 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/show_config` | upstream-carried | 3 | n/a | n/a: not a script (none) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/splash/splash-1080.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/splash/splash-1200.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/splash/splash-2160.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/splash/splash-720.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/splash/splash-768.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LEIoT/version` | upstream-carried | 5 | n/a | n/a: not a script (none) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/LibreELEC.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/LibreELEC_40x40.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/addons/Carlito-Bold.ttf` | upstream-carried | 0 | n/a | n/a: not a script (font) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/addons/addon-bg.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/addons/fanart.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/addons/overlay-flatpack.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/kernel_options` | upstream-carried | 220 | n/a | n/a: not a script (none) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/options` | upstream-carried | 282 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/show_config` | upstream-carried | 42 | n/a | n/a: not a script (none) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/splash/boot-logo.bmp.gz` | upstream-carried | 0 | n/a | n/a: not a script (other) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/splash/splash-1080.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/splash/splash-1200.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/splash/splash-2160.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/splash/splash-720.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/splash/splash-768.png` | upstream-carried | 0 | n/a | n/a: not a script (image) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `distributions/LibreELEC/version` | upstream-carried | 8 | n/a | n/a: not a script (none) | n/a | Q4: identical to `upstream/next` | never | unreached | another distribution's identity |
| `tools/RPi/gen-rpi-kodi-patch.sh` | upstream-carried | 109 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job each |
| `tools/RPi/rpi-kodi-rebase.sh` | upstream-carried | 16 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job each |
| `tools/adjust_kernel_config` | upstream-carried | 40 | no current replacement; `kernel_make` is the engine's own | `bash -n` ok; shellcheck not on the host | line 32 matches the command by substring (`grep ${KERNEL_CONFIG_COMMAND}`): latent, an unknown command that is a substring of a real one passes the check; upstream's | Q4: identical to `upstream/next` | a developer's `make kconfig-*`; not on a build | reached by `Makefile:31,34` (`kconfig-olddefconfig-%`, `kconfig-menuconfig-%`) and `.github/workflows/update-kernel-configs-docs.yml:72` (re | one job, the header says it |
| `tools/change_addon_version` | upstream-carried | 101 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/check_kernel_config` | upstream-carried | 38 | n/a: no current replacement | `bash -n` ok; shellcheck not on the host | no defect read: it applies `distributions/${DISTRO}/kernel_options`, which ROCKNIX carries | Q4: identical to `upstream/next` | with `adjust_kernel_config` | reached by `tools/adjust_kernel_config:38`; also named by the message `packages/linux/package.mk:221` and `projects/ROCKNIX/packages/linux/p | one job |
| `tools/checkunpack` | upstream-carried | 111 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/dashboard` | upstream-carried | 53 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/distro-tool` | upstream-carried | 1097 | a bash script with an embedded Python program (LibreELEC's mirror tool, 1,097 lines); no current replacement | `bash -n` ok; shellcheck not on the host | n/a: not run | Q4: identical to `upstream/next` | never | reached by a document only: named in `CLAUDE.md:131`'s list of "dev helpers", with no instruction to run it; no caller | `CLAUDE.md:131` presents it beside `pkgcheck` as a helper |
| `tools/docker/README.md` | upstream-carried | 49 | six other distributions' containers | n/a: not a script (markdown) | n/a | Q4: identical to `upstream/next` | never | unreached | `README.md` describes containers the fork does not use |
| `tools/docker/bookworm/Dockerfile` | upstream-carried | 35 | six other distributions' containers | n/a: not a script (docker) | n/a | Q4: identical to `upstream/next` | never | unreached | `README.md` describes containers the fork does not use |
| `tools/docker/jammy/Dockerfile` | upstream-carried | 42 | six other distributions' containers | n/a: not a script (docker) | n/a | Q4: identical to `upstream/next` | never | unreached | `README.md` describes containers the fork does not use |
| `tools/docker/noble/Dockerfile` | upstream-carried | 41 | six other distributions' containers | n/a: not a script (docker) | n/a | Q4: identical to `upstream/next` | never | unreached | `README.md` describes containers the fork does not use |
| `tools/docker/questing/Dockerfile` | upstream-carried | 41 | six other distributions' containers | n/a: not a script (docker) | n/a | Q4: identical to `upstream/next` | never | unreached | `README.md` describes containers the fork does not use |
| `tools/docker/resolute/Dockerfile` | upstream-carried | 41 | six other distributions' containers | n/a: not a script (docker) | n/a | Q4: identical to `upstream/next` | never | unreached | `README.md` describes containers the fork does not use |
| `tools/docker/trixie/Dockerfile` | upstream-carried | 34 | six other distributions' containers | n/a: not a script (docker) | n/a | Q4: identical to `upstream/next` | never | unreached | `README.md` describes containers the fork does not use |
| `tools/download-cleaner` | upstream-carried | 133 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/download-tool` | upstream-carried | 47 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never on the fork | unreached | one job |
| `tools/ffmpeg/gen-patches.sh` | upstream-carried | 109 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: `packages/multimedia/ffmpeg/package.mk:14` (`PKG_NO_REFRESH_PATCHES`), a generic recipe no image builds (the ROC | named by its recipe |
| `tools/find_build_warnings.sh` | upstream-carried | 280 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/find_build_warnings_ignore.conf` | upstream-carried | 21 | n/a | n/a: not a script (config) | n/a | Q4: identical to `upstream/next` | never | unreached | its tool's data |
| `tools/fixlecode.py` | upstream-carried | 372 | Python 3 | `ast.parse` ok | n/a | Q4: identical to `upstream/next` | never | unreached | beside `pkgcheck` and `packages-checker` |
| `tools/icon-generate` | upstream-carried | 184 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: a comment in `packages/addons/service/nqptp/icon/icon-source.svg:7`, an add-on no fork image builds | one job |
| `tools/imgburn.sh` | upstream-carried | 128 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | a second flashing route beside the runbook |
| `tools/mkpkg/mkpkg_bcm2835-bootloader` | upstream-carried | 41 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/mkpkg_boblightd` | upstream-carried | 26 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/mkpkg_libcec` | upstream-carried | 28 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/mkpkg_media_build` | upstream-carried | 79 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/mkpkg_pvr` | upstream-carried | 113 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/mkpkg_rtmpdump` | upstream-carried | 28 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/mkpkg_vboxguest` | upstream-carried | 38 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/update_binary-addons` | upstream-carried | 284 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/update_common_functions` | upstream-carried | 265 | n/a | n/a: not a script (none) | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/mkpkg/update_retroplayer-addons` | upstream-carried | 232 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: the messages `config/functions:1342,1345` ("use mkpkg"); no caller | the messages name the directory, not a script |
| `tools/moby/gen-patches.sh` | upstream-carried | 66 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: `packages/addons/addon-depends/docker/moby/package.mk:13`, an add-on dependency no fork image builds | named by its recipe and its patch header |
| `tools/mtstats.py` | upstream-carried | 271 | Python 3; no replacement | `ast.parse` ok | no defect read; a failure is now said and not returned (T5 `7abea6eb86`) | Q4: identical to `upstream/next` | one pipe after each finished build: the statistics of its history file | reached by `config/multithread:64` (after every finished multithread build; T5's E8 made its failure not the build's) | one job |
| `tools/packages-checker` | upstream-carried | 23 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | beside `pkgcheck`: one rewrites, one reports |
| `tools/pkgcheck` | fork-own | 169 | no current replacement; the fork's `81221658b3` made its status mean something | `bash -n` ok; shellcheck not on the host | F-02: a name that matches no recipe processes nothing and exits 0, like a clean recipe (fixture); its late-binding list omits `SYSTEM_*`/`TOOLCHAIN`-class names (a lead for #657) | Q4: differs: the fork's `81221658b3` to `upstream/next` | by hand, one recipe at a time; none on a build | reached by a document only: `CLAUDE.md:109`, `AGENTS.md:343`, `.claude/rules/packaging-and-patches.md:46`, `packages/README.md:274` (run by  | upstream's header and the fork's 3-line comment agree with the code |
| `tools/pkginfo` | upstream-carried | 27 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/podman-bin/gen-patches.sh` | upstream-carried | 72 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | by hand | reached by a document only: `packages/addons/addon-depends/podman/podman-bin/package.mk:14`, an add-on dependency no fork image builds | named by its recipe and its patch header |
| `tools/refresh-patches` | upstream-carried | 167 | n/a | `bash -n` ok; shellcheck not on the host | n/a: not run on the fork | Q4: identical to `upstream/next` | by hand | reached by a document only: `packages/README.md:36` (`PKG_NO_REFRESH_PATCHES`); run by hand to regenerate a recipe's patches | one job |
| `tools/repo-tool` | upstream-carried | 218 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/update-functions/LibreELEC-settings` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/amlogic-boot-fip` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/aspnet-runtime.py` | upstream-carried | 134 | n/a | `ast.parse` ok | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/aspnet6-runtime` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/aspnet8-runtime` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/aspnet9-runtime` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/bcm2835-utils` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/bcmstat` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/brcmfmac_sdio-firmware` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/cargo-snapshot` | upstream-carried | 14 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/ccid` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/chrome` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/cli` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/conmon` | upstream-carried | 4 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/containerd` | upstream-carried | 4 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/ctop` | upstream-carried | 4 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/docker-compose` | upstream-carried | 15 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/dotnet-runtime` | upstream-carried | 23 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/dt-overlays` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/dvb-firmware` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/eventlircd` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/extra_commit_body` | upstream-carried | 66 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/filebrowser` | upstream-carried | 15 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/fluidsynth` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/glslang` | upstream-carried | 20 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/gst-plugins-bad` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/gst-plugins-base` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/gstreamer` | upstream-carried | 20 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/iwlwifi-firmware` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/jellyfin` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/kmsxx` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/libarchive` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/libcec` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/libde265` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/libheif` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/libopenmpt` | upstream-carried | 11 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/libraw` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/meson-firmware` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/misc-firmware` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/moby` | upstream-carried | 14 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/pcsc-lite` | upstream-carried | 10 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/podman-bin` | upstream-carried | 4 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/polkit` | upstream-carried | 10 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/rpi_ws281x` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/runc` | upstream-carried | 4 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/rust` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/rust-std-snapshot` | upstream-carried | 14 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/rustc-snapshot` | upstream-carried | 14 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/script.config.vdr` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/shairport-sync` | upstream-carried | 7 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/snapcast` | upstream-carried | 11 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/squeezelite` | upstream-carried | 25 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/tailscale` | upstream-carried | 16 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/tinc` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/tvheadend43` | upstream-carried | 25 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/vdr` | upstream-carried | 4 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/vulkan-headers` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/vulkan-loader` | upstream-carried | 3 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/vulkan-tools` | upstream-carried | 28 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/wlan-firmware` | upstream-carried | 8 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/x264` | upstream-carried | 15 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-functions/x265` | upstream-carried | 28 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | per-package hooks of a tool nobody runs |
| `tools/update-pkg` | upstream-carried | 181 | agrees with D-WORKFLOW-193: it writes a `PKG_SHA256` from one fetch (`:61-64`) | `bash -n` ok; shellcheck not on the host | lead: `:63` `curl` without `--fail` would hash an error page; latent, unreached | Q4: identical to `upstream/next` | never | unreached | two tools beside `scripts/update_packages` (T5's) for one job |
| `tools/update-scan` | upstream-carried | 226 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | see `update-pkg` |
| `tools/upload_to_filebin` | upstream-carried | 54 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/viewconfig` | upstream-carried | 12 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |
| `tools/viewplan` | upstream-carried | 11 | n/a | `bash -n` ok; shellcheck not on the host | n/a | Q4: identical to `upstream/next` | never | unreached | one job |

## Proofs

| # | What | Command / artifact | Result | Cell |
| --- | --- | --- | --- | --- |
| P1 | the two-way caller count for the 24 single tools, with its positive controls | brief § 5's loop (08:09:06), `.qa-scratch/t6/callers-two-way.txt` | `pkgcheck` 14/1 and `adjust_kernel_config` 2/2 reached; 16 tools 0/0 | proved: tree |
| P2 | every zero searched the second way, by bare name over the documents and inside the slice | the second search (08:10) | one document mention (`CLAUDE.md:131`); `adjust_kernel_config:38` calls `check_kernel_config`, found by reading the reached tool | proved: tree |
| P3 | the 62 helpers' only caller | `git grep -n -F 'update-functions'` (08:09:58) | `tools/update-pkg:70`, `:167` | proved: tree |
| P4 | the only `DISTRO` setter | `git grep -n -E 'DISTRO=\|DISTRO:='` (08:09:58) | `config/options:24` | proved: tree |
| P5 | the syntax sweep | `bash -n` and `ast.parse` (08:09:58, 08:10) | 37 of 37, 61 of 61, 3 of 3 | proved: tree |
| P6 | `tools/pkgcheck`'s tier | `git log upstream/next..8ebaf8daad -- tools/pkgcheck` (08:11:45) | one fork commit, `81221658b3`; upstream untouched since the base | proved: history |
| P7 | `tools/pkgcheck` exits 0 for a name no recipe matches | `tools/fx-pkgcheck.sh <scratch> 8ebaf8daad` (08:12:31) | clean 0, violating 1 (one FAIL), unknown name 0 with nothing printed | proved: fixture |
| P8 | `distributions/LEIoT/kernel_options` dangles | `test -e`, `readlink`, `git log --diff-filter=A` | dangling; added so in `4130b59b50`; identical upstream | proved: tree |
| P9 | the `update to` commits are not `update-pkg`'s | `git log --grep` and each commit's trailer | 12 of 12 carry a `Co-Authored-By: Claude` trailer `update-pkg` never writes | proved: history |
| P10 | Q4 over the 135 | the upstream-state loop (08:07:43) | 134 identical, 1 differs | proved: tree |
| P11 | `tools/pkgcheck` exits 2 for a name no recipe matches (S1, #845) | `tools/fx-pkgcheck.sh <scratch>` at `8ebaf8daad`, `7fa8bafba4` and the working tree (08:32:43, 08:38:18) | before: unknown name 0, nothing on stderr; after: 2, one stderr line naming it; clean 0 and violating 1 unchanged | proved: fixture |
| P12 | the list catches a global `${INSTALL}` and leaves `${TOOLCHAIN}` and `${SYSROOT_PREFIX}` clean (S2) | `tools/fx-pkgcheck.sh <scratch>` at `8ebaf8daad`, `7fa8bafba4` and the working tree (08:38:18) | `fixturelate` 0, 0, then 1 with one FAIL; `fixtureearly` 0 all three times | proved: fixture |
| P13 | the sweep over every recipe, before and after | `tools/pkgcheck` with no argument at `8ebaf8daad` (08:30:02 to 08:30:35), after S1 (08:32:50 to 08:33:23), after S2 (08:38:27 to 08:39:07) | exit 1 all three; FAIL 12, the same 12, then 21; WARN 43 all three; § Leads from the sweeps | proved: tool-run |
| P14 | which names the build sets after a recipe loads | `config/options:185,197`; `source_package` and `setup_toolchain` in `config/functions`; every reassignment of `config/path`'s names in `config/functions`, `config/options`, `scripts/build`, `scripts/install` (08:33 to 08:35); the trial sweep with `SYSROOT_PREFIX` listed (08:35:55 to 08:36:35) | 18 names added; `TOOLCHAIN` never reset; `SYSROOT_PREFIX` reset at `scripts/build:471`, 66 global uses: 43 configure, 7 cmake, 5 cmake continuation lines, 4 unpack, 2 host configure, 2 gcc configure, 2 make, 1 helper path | proved: tree |

## Criterion entries: #653's checklist (= brief § 7), at the end of Phase 2

Evaluated 08:23 UTC (`date -u`). The coordinator ticks at hand-back.

1. **The folder holds `00` to `05`:** PARTIAL. `00` to `04` are written; `05` is stage D.
2. **The lint prints PASS:** OPEN. The pre-issue run is at stage C to D; the full run at close.
3. **`review-plan.json`:** MET. `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184`, and a `reason` naming plan § 6c's row.
4. **The punch-list issue at Phase 7:** OPEN (stages D to F).
5. **`reviewed-at` and `fixed-at`:** PARTIAL. `reviewed-at: b96e1ca761` is in `00` and `01`; #653's body gets both at hand-back.
6. **`01` § Scope:** MET. The hash, the filter and its output (no delta), and the two-roots diff with each of the 15 hunks' owner.
7. **The coverage table, 135 rows:** MET. `grep -c` prints 135, and every cell is answered or `n/a` with its reason (the generator asserts each path is in exactly one group).
8. **§ Mechanical checks:** MET. The two diffs, the Q4 loop (1 differs), the two-way caller count for the 24 single tools, the `update-functions` and `DISTRO=` greps, and the syntax sweep with its counts. shellcheck is recorded as not runnable.
9. **`04` § Q6, the reachability table:** MET. 33 rows summing to 135, each with its two counts, verdict, tier, Q4 state and disposition; every unreached row carries `Already written:`; no deletion.
10. **`04` § Q4:** MET. The 135-row table, and `pkgcheck`'s tier settled with the two commands; `instruction-files.md` is named as the document to correct.
11. **§ The #644 finding:** MET. Finding 24 with its four tools' verdicts and the #585 proposal's text; the other 25 named with their carriers.
12. **The proofs:** MET. The proof cells in `02` (10) equal the `PROOF` lines in `00` (10), each class `tree`, `history` or `fixture`.
13. **Punch items with `question:`; the #585 item; `box-check`; no change to `tools/` or `distributions/` before a stream brief:** OPEN (stage D). Nothing under the two roots has changed on this branch (stage B's last line).
14. **No upstream file deleted:** MET so far. `git diff --diff-filter=D --name-only 8ebaf8daad HEAD -- tools distributions` is empty.
15. **The retro:** OPEN (stage G).
16. **The checkers and the lint; the six exit codes:** OPEN (stage H).

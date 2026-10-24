# Analysis — M6.P2 T5, the build engine

**Date:** 2026-10-24. **Read at:** `reviewed-at: 46f6c7d428`; **fixed at** `fixed-at: 877775e61e` (stage E, streams E1 to E8); the slice's bytes `next`'s `8ebaf8daad`; `upstream/next` `3421d7d178`. Findings are `02-forward-audit.md`'s `F-NN`; proofs its `P<n>`. Severity and category are set here and carried to `05`.

## Executive summary

The slice is the engine every build runs: LibreELEC's scripts and `config/functions`, ROCKNIX's distribution layer, and the fork's additions (the watch entry, the identity, the container's lifecycle, the meson guard, the name). **The fork's additions are small, commented and mostly right; the engine's weak points are where a failure is reported as success, or where a guarantee holds on one route and not the one people use.** Nothing was built: every claim is a reading at a site, a sandboxed call with its trace read first (P1 to P8, P11 to P13), an install tree (P7), or a recorded run (P10), and the build-only proofs are `fix-pending-image`.

**25 findings, after Phase 4.6. Two are High:**

- **F-16:** `scripts/mkimage` reports success over an incomplete image on the `qcom-abl` route, SM8550's, the Retroid Pocket Nova's (unchecked copies of the kernel and `SYSTEM` there and in the shared bootloader hook, unchecked compression and checksum, and a closing `exit` that returns 0 after any of them fails).
- **F-25** (from Astra's pass): a git cache directory the build user cannot enter makes `scripts/get_git` run `git clean -fdx` in the build tree, which deletes its build roots, `sources/` and untracked files without a word (P14). The trigger is narrow; the loss is hours of unrecoverable output. Upstream's code.

**Seven are Medium:**

- `scripts/get_env` keeps six constructed secret-shaped names (F-01).
- A multi-line value lets a dropped name return through docker's `--env-file` (F-02).
- `add_es_system` carries a system's fragment into the next, so `daphne` and `gp32` ship a wrong year on every image, and the next system appended would launch nothing (F-03).
- The launch table's one-default rule stops a build silently on one shape and ships two defaults on the other (F-04, T3's F-06).
- `build_distro`'s prune defeats the image's refusal to reuse an identity on the documented route (F-09).
- Archives are fetched without TLS verification and accepted unhashed (F-19).
- `checkdeps` changes the host's compiler and `/nix` with `sudo` when its conditions hold (F-20).
- `scripts/get_git` accepts a cached clone whose `HEAD` is not the pin when the pin matches any of its refs (F-18, P13). Re-graded from High in Phase 4.6: the cache directory is keyed by the pin, so an ordinary bump gets a fresh clone.

**The rest are Low or `Renovation`:** a stale rule (F-05: two items of `device-builds.md` describe defects fixed in August), dead identity code (F-06, F-07), upstream's glob test (F-08), a workflow red on every run (F-10), the options file's two spellings (F-15), small helper defects (F-21), two upstream lines that fail a run for the wrong reason (F-22), a device file outside the stamp, which a device build cleans anyway (F-17, P12), the identity's dirty check failing open (F-23), an initramfs clean that never fires off RK3566 (F-24), the container pin's age and three files behind upstream (F-11, F-12), and two items #644 assigned (finding 3's sentence, finding 8's measurement).

**Currency (Q4):**

- **Against ROCKNIX:** the slice is level but for three upstream commits, all `to merge` with the next base merge.
- **The container:** the pin is 29 days behind upstream's image of today; the `Dockerfile` is identical.
- **Upstream contributions (#585 candidates):** F-03, F-04, F-08, F-16, F-17, F-18, F-19, F-20, F-24 and F-25 are upstream's code; D-WORKFLOW-164, with submissions deferred by D-WORKFLOW-165.

## Acceptance-criteria scorecard

`02` § Criterion entries, at the end of Phase 2: PASS 5 (AC-06, 07, 08, 09, 13), PARTIAL 3 (AC-01, 03, 05), OPEN 8 (AC-02, 04, 10 to 12 here, 14, 15, 16). AC-10 to AC-12 are answered by § Renovation face below and re-evaluated in `05`'s Phase 7 gate.

## Code Quality Assessment

### Strengths
- The fork's additions sit beside the line they change and carry their reason (`scripts/build` 185 to 188; `config/graphic`'s LLVM comment; `scripts/image`'s identity comments; the `Makefile`'s `.env` paragraph).
- The identity fails closed on every malformed input (P9: 16 rejections), and its sidecar is written once per image.
- The `.env` lifecycle is careful about the file: removed first, written under `umask 077` and `set -C`, removed on exit, no container if `get_env` fails.
- The meson guard reached every configure (P10).

### Concerns
- Success reported over failure: F-16, F-04 case A (a stop with no message), F-03 (a silent wrong value), F-08.
- A guarantee that holds on a side route only: F-09 (the identity), F-15 (the credentials file).
- A filter that does less than its comment: F-01, F-02.

### Complexity Hotspots
`config/functions` (1,936 lines, about twelve responsibilities, `Q7`); `scripts/mkimage` (one block per bootloader, the guards present in four and absent in two, F-16); `scripts/get_git`'s two validity paths that disagree (F-18).

## Cornerstone Conformance

Least surprise and fail-closed (`03` § Cornerstone Alignment). Time to play is untouched: the engine is not on the launch path (Q5).

## Spec Fidelity

### Aligned
The nine #644 findings this slice carries are each recorded with their disposition (`02`); the brief's mechanical checks all ran or are recorded as not runnable.

### Diverged
- The brief's Q3 framing of `calculate_stamp` (from the stale rule, F-05).
- The brief's § 2 description of `scripts/image`'s refusal, which the device route never reaches (F-09).
- `build-path-read.md` finding 13's "T9 reads the identity test" (`slices.json` gives it to T14; the brief already says so).

## Missing Artifacts
- No test of `get_env` (P1 is the first).
- No test of the prune and the refusal together (F-09).
- No check of the launch table's invariants: one default, a command per system (F-03, F-04).
- No recorded bash version of the build container.

## Risk Assessment

| Risk | From | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| an SM8550 image missing part of `SYSTEM` reported built and staged on the Nova | F-16 | low (needs a full FAT partition or a full disk) | a device that does not boot, from an image the record calls good | the two branches' `|| show_error`, `pigz` checked, `exit` with a real status |
| a build tree's roots, `sources/` and untracked files deleted by a fetch | F-25 | low (a cache directory the build user cannot enter) | hours of build output lost, with nothing reporting it | `pushd ... \|\| return 1` |
| an image built from an older source than its recipe names | F-18 | low (the cache is keyed by the pin, so it needs a cached clone whose `HEAD` moved or whose files were edited) | the image's claimed version is false, and a fix said to ship does not | compare `HEAD` with `PKG_VERSION` |
| a secret in the developer's shell reaching `.env` and the container | F-01, F-02 | low (needs such a name, or a multi-line value) | a credential in a container and a world-unreadable file in the worktree | case-insensitive names, the missing words, values with newlines refused |
| a new system appended to the table launching nothing | F-03 | medium (upstream adds systems) | a system that does nothing when a game is chosen | unset the fragment's keys per call |
| a rebuilt identity's bytes replaced in `target/` | F-09 | low (a frozen timestamp and a rebuild of one device) | two different files under one identity until the store is checked | refuse before the prune |

## Coverage Boundary

- **Read line by line:** the 18 fork-own paths; `config/build-identity`; `scripts/get_env`; the `Makefile`'s Docker block; `distributions/ROCKNIX/config/functions` 95 to 230; `config/options` 86 to 152; `scripts/get_git`, `get_archive`, `update_packages` 46 to 66, `checkdeps` 255 to 345, `mkimage`'s copy and exit lines, `unpack` 84 to 125, `build_distro` whole, `build_compat` whole; the sites of every re-read lead.
- **Read whole by the research subagent, its leads re-read here:** `config/functions`, `options`, `path`, `optimize`, `multithread`, `arch.*` and the upstream scripts it named. A "no finding" cell there is the subagent's read plus this auditor's re-reading of its leads, not a line-by-line read by the auditor.
- **Not read line by line:** `scripts/pkgbuilder.py` (933), `genbuildplan.py` (396), `uboot_helper` (586): `py_compile`, their callers (Q6) and the recorded runs' successful plans only. The add-on scripts (`create_addon`, `install_addon`, `create_docker_package`): unreached by any fork build (Q6). The 139 fragments: their keys against the tables (P3, P11) and the five devices' tables (Table 2), not each value against its system's history. The 18 upstream workflows: their triggers, gates, secrets and runners, not their steps.
- **Not run:** a build of any kind; `docker run`; `actionlint` (absent); the container's bash. Everything a build alone can show is `fix-pending-image`.

## Finding Verification (Phase 4.5)

Each finding re-read against its primary artifact, asking what would refute it:

| Finding | Refutation tried | Result |
| --- | --- | --- |
| F-01 | does a later step re-filter `.env`? (`Makefile` 205 to 208: no; docker reads it whole) | stands |
| F-02 | does docker's `--env-file` take a bare name from the host? Docker's documented syntax for `--env-file`: a line `VAR` without `=` passes the local value. Not run here | stands, with the docker half cited rather than shown |
| F-03 | does anything unset `SYSTEM_*` between calls? (`grep -n 'unset' distributions/ROCKNIX/config/functions`, `virtual/emulators/package.mk`: none for these keys); is `1996` right for `daphne` or `gp32`? (Daphne's laserdisc games are 1983 on; the GP32 is 2001) | stands |
| F-04 | rerun of T3's cases (P4, P5) | stands |
| F-05 | is the rule perhaps about an older engine still in use? (both fixes are in `upstream/next` and `8ebaf8daad`) | stands |
| F-09 | does `build_distro`'s prune run when the image step is entered another way? (`make image` alone: no prune, the refusal fires; `make <DEVICE>`: prune first) | stands, scoped to the device route |
| F-16 | does `scripts/image` check the image after `mkimage`? (it trusts `do_mkimage`'s status, 337; the checksum is written by `mkimage` itself, 326 to 329) | stands |
| F-17 | does any recipe list its device file in `PKG_NEED_UNPACK`? (`kernel-firmware` lists the two package directories only, 10) | stands for `kernel-firmware`; other `find_file_path` readers are leads |
| F-18 | does `_get_repo` or `unpack` reset to `PKG_VERSION` after the cached path? (`main` exits at 198 before either) | stands |
| F-19 | does a later stage hash the archive? (`_get_file_already_downloaded` compares the stamp, 6) | stands |
| F-20 | is `prepare_nix_dir` gated? (called unconditionally at 345) | stands |
| the subagent's lead 11 | `json_worker` 18 to 21 catches the failure | **withdrawn** as a finding; kept as a partial lead |

## Renovation face

### Q1 Modernize

- **Idioms the tree has moved past, in upstream's lines:** `[ p -a q ]`/`-o` (SC2166, 32 sites), `for x in $(find ...)` (SC2044, 7), `cd` without a fallback (SC2164, 13); the `ls | sort` loop in `mk_es_systems` (106); `${3:none}` and `${PKG_NAME:exec}` for defaults (F-21); unquoted `${@}` in `build_mt` and `multithread` (an upstream idiom; package names have no spaces). Not defects; renovation only if the file is otherwise touched, so that each change stays upstreamable.
- **Dead control flow:** `build_distro` 103 to 106's `$?` after a `case` under `set -e` (F-14); `exec_thread_safe`'s `$?` (lead 15).
- **Dead code the fork's own changes left:** `build_compat`'s pre-identity naming (F-07), `ORIGIN_URL` and `BUILD_FILENAME` (F-06).

### Q2 Standards and best practices

- **`engineering-practices.md` § Guards must fail closed:** F-16 (two branches and `pigz` unguarded; exit 0), F-04 (the formatter's error silenced), F-08 (a test that errors into false), F-03 (a value taken from the previous call), F-02 (a line format that can be broken by data).
- **D-INFRA-006 (credentials):** F-01, F-02; F-13 (the options file mounted writable); F-15 (the two spellings).
- **The watcher's contract (D-WORKFLOW-142):** the five entry points carry it and `test-build-monitor` proves it (36 PASS); `build_mt` and `clean` do not (#644 finding 6, T9's).
- **The host belongs to its owner:** F-20.
- **`packages/README.md`'s hook order:** honoured; the fork changed none of it.
- **`fork-workflow.md`:** none of the 242 is a personal path; every fork hunk is upstreamable in shape.

### Q3 Bugs

F-01, F-02, F-03, F-04, F-08, F-09, F-16, F-17, F-18, F-19, F-20, F-21 (`02`). F-23, F-24 and F-25 were added in Phase 4.6. The `bug` issues are filed at stage D for the defects that a sandbox, a recorded run or an install tree can verify: F-01 with F-02 (one issue, `get_env`), F-03, F-04, F-09, F-16, F-17, F-18, F-19, F-20, F-25. Of these, F-04's issue is T3's lead made this slice's, and F-08 and F-21 stay punch items (Low, upstream's, no shipped effect).

### Q4 Package currency

The engine introduces no package (`tools/fork-package-freshness --list`: nothing of the slice).

#### Q4 (a): the fork against ROCKNIX

Upstream's commits on the membership since the merge base `c445081a59` (at `upstream/next` `3421d7d178`, fetched 2026-10-24 03:51 UTC):

| Commit | Date | What | Disposition |
| --- | --- | --- | --- |
| `c4d353449e` | 2026-10-18 | `aethersx2: drop package due to licensing concern` (`config/blocklist`) | **to merge** with the next base merge (the blocklist line; T3's F-07 carries the package, ruled class 1 by the coordinator on #650) |
| `76693a738d` | 2026-10-13 | `ci: add github username to release` (`build-nightly.yml`) | **to merge** (a workflow the fork never runs to completion, Table 4) |
| `c200cc906d` | 2026-10-07 | `github: update pull request template` | **to merge** (#644 finding 18's template, T4's facts) |

Every membership file that differs textually from `upstream/next` (`git diff --name-status upstream/next 8ebaf8daad -- <the 242 paths>`: 21 files; each file's commits from `git log c445081a59..8ebaf8daad` and `c445081a59..upstream/next`):

| File | Status | The difference | Whose | Disposition |
| --- | --- | --- | --- | --- |
| `.github/pull_request_template.md` | M | upstream's `c200cc906d` (the new template: tested devices, artifacts, the AI-assistance disclosure); the fork has not edited it | upstream's | to merge (the next base merge; #644 finding 18) |
| `.github/workflows/build-nightly.yml` | M | upstream's `76693a738d` (`GH_TOKEN` on two release steps); the fork's commits on it are base merges (`7bd7f31312`, `7650de7dd6`) | upstream's | to merge |
| `.github/workflows/check-freeze-period.yml` | M | `runs-on: ubuntu-24.04` for upstream's `self-hosted` (`3d7c075f63`) | the fork's | keep (#644 finding 19, T10's) |
| `.github/workflows/validate-pull-request.yml` | M | the same runner edit (`3d7c075f63`; `7bd7f31312` the merge) | the fork's | keep (T10's) |
| `.gitignore` | M | `/.qa-scratch/`, `tools/council/node_modules/`, `__pycache__/`, the council and audit artifacts, `/.build-runs/`, `*.local.md`, the local logs (`1aac875e88` and eight others) | the fork's | keep (personal paths of the fork's tooling; none reaches an upstream PR by path) |
| `Makefile` | M | the pinned container, the `.env` lifecycle, the watch entries, `GENERIC_X64` in `world` and its target, `docker-image-pull` (`d7e2d6be41`, `a9af618398`, `1aac875e88`, `440ad22b68`, `2c349c6d51`, `67cd0e6493`, `a79b7f82a5`, `d704c9d563`, `73b20caf86`; `7bd7f31312` a merge) | the fork's | keep; F-13 |
| `config/blocklist` | M | upstream's `c4d353449e` (the `aethersx2-sa` line removed); `7bd7f31312` is a merge | upstream's | to merge (with T3's F-07, the package itself) |
| `config/build-identity` | A | new (`40bc5469b9`, `f10eec1306`; #532, D-WORKFLOW-157/159) | the fork's | keep (#644 finding 13) |
| `config/graphic` | M | a device's `LLVM_SUPPORT=yes` kept, for GENERIC_X64's llvmpipe (`f483f215ad`, fork #291; `73b20caf86`) | the fork's | keep; #585 candidate (a device that sets LLVM loses it upstream too) |
| `config/show_config` | M | prints `RELEASE_VERSION` for upstream's official/community word (`f10eec1306`) | the fork's | keep |
| `distributions/ROCKNIX/config/functions` | M | generated documentation kept out of frozen inputs under the watcher; `mkdir -p` (`5e2509a25a`, `7650de7dd6` a merge) | the fork's | keep; F-03, F-04 are upstream's lines in the same file |
| `distributions/ROCKNIX/options` | M | the identity (`pixelelated`, the URLs), `BUILD_DATE` in UTC with a default, `DEVELOPMENT_DEFAULTS` (`f10eec1306`, `a9af618398`, `3d7c075f63`) | the fork's | keep |
| `distributions/ROCKNIX/version` | M | `OS_VERSION="0.0.1"`, the qualifier comment, `IMAGE_SUFFIX` (`40bc5469b9`, `f10eec1306`, `3d7c075f63`; D-WORKFLOW-128) | the fork's | keep |
| `scripts/build` | M | the watch entry and `--wrap-mode=nodownload` (`1aac875e88`, `79437a25c0`) | the fork's | keep; #585 candidate |
| `scripts/build_compat` | M | the watch entry (`1aac875e88`) | the fork's | keep; F-07 |
| `scripts/build_distro` | M | the watch entry, `DISTRONAME` roots, `rm -rf` of `target/` (`43d0bc3bf4`, `1aac875e88`, `c2bb7ec0b9`) | the fork's | keep; F-09 |
| `scripts/extract` | M | `mkdir -p` (`73b20caf86`) | the fork's | keep |
| `scripts/get_env` | M | the secret filter (`d704c9d563`, D-INFRA-006) | the fork's | keep; F-01, F-02 |
| `scripts/image` | M | the identity, the sidecar, the refusal, the licence files, the watch entry, `bootloader/install` (`f10eec1306`, `a9af618398`, `0159cb3235`, `1aac875e88`, `73b20caf86`) | the fork's | keep; F-06, F-09 |
| `scripts/install` | M | the watch entry (`1aac875e88`) | the fork's | keep |
| `scripts/test-audit-review.py` | A | new (`5150320de2`, #378) | the fork's | keep; misfiled (Table 5) |

#### Q4 (b): the build container

| | Digest | Created (config blob) | Platform | Read with |
| --- | --- | --- | --- | --- |
| The `Makefile`'s pin (138; `2c349c6d51`, `440ad22b68`, 2026-10-01) | `ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39` | 2026-09-25T03:09:54Z | linux/amd64, 12 layers | `docker manifest inspect`; config `sha256:9783cb20…` through GHCR's anonymous token |
| Upstream's `ghcr.io/rocknix/rocknix-build:latest` | `sha256:67e1fd0adbcfe71cc524ef49941242853f3daa7f1eecea74ec765b9b6d24973d` | 2026-10-24T03:03:03Z | linux/amd64, 12 layers | the same; config `sha256:3acf6ac8…` |

- **Same or different:** different; 10 of the 12 layer `diff_ids` differ, both labelled `org.opencontainers.image.version: 22.04`. The coordinator's read earlier on 2026-10-24 answered `a81b63a53612…`, so upstream rebuilt again during the day (it rebuilds on every non-PR CI run, #644 § 2).
- **`Dockerfile`:** `git diff upstream/next 8ebaf8daad -- Dockerfile` is empty; upstream's last change is `f6d1c3beac` (2026-05-02). So what changed between the two dates is Ubuntu 22.04's package updates, not a recipe change.
- **The refresh** (`fork-mirror-build-container.yml`, then the `Makefile` line) is **the coordinator's act**, recorded `to merge` (#644 finding 1). No pull was run.

### Q5 Efficiency

- **The recorded runs** (read-only, `build.start` to `build.rc`'s mtime, and `build.status`), all warm roots:

  | Run | Device | Wall time | Packages |
  | --- | --- | --- | --- |
  | `m7-signin-build-20261022-07/.build-runs/20261022T235954Z-4749157a` | GENERIC_X64 | 5 m 7 s | 654/654 |
  | `m7-signin-h700-build-20261023-06/.build-runs/20261024T014932Z-8a1ff937` | H700, both ABIs | 10 m 32 s | 671/671 |
  | `m7-signin-sm8550-build-20261023-03/.build-runs/20261024T020912Z-68374394` | SM8550, both ABIs | 11 m 4 s | 737/737 |

  The image step is not timed separately in the watcher's record.
- **ccache:**

  | Setting | The fork's `config/options` | CI's (#644 finding 8) |
  | --- | --- | --- |
  | `CCACHE_COMPRESSLEVEL` | `0` (109; zstd's level 1) | `6` |
  | `CCACHE_SLOPPINESS` | `pch_defines,time_macros` (118) | the same plus `include_file_*` additions |
  | `CCACHE_CACHE_SIZE` | `15G` per build root (100) | trimmed per stage (500 MB to 4.5 GB) |

  **Not measured:** no recorded run's log carries ccache statistics (the four read show `Local Ccache: no` and per-package `ccache:host` sequence lines only), and `ccache --show-stats` against an M7 root would start a process in the M7 lane's tree, so it is not run. Also, these values reach a build root only when `ccache:host` is built (the subagent's lead, `projects/ROCKNIX/packages/devel/ccache/package.mk` 26 to 28), so a changed setting needs that package rebuilt to take effect. That is a reason the measurement belongs to a build. LibreELEC #11890 (2026-10-12, *name the compiler to ccache by the toolchain key*) is the upstream lead. A punch item: measure at the first build after the merge.
- **The stamp's granularity:** a whole-directory hash, so a metadata-only change rebuilds the package. `device-builds.md` § A metadata-only upstream change gives the measure: the 2026-09-04 merge brought 446 changed recipes, 220 of them only by upstream's checksum sweep, and all 446 rebuilt. No new count here.
- **The watch entry:** one `exec` and a per-worktree lock per top-level entry, nested calls reusing the run; its cost is inside the recorded totals and not separable from them.
- **Concurrency:** `CONCURRENCY_MAKE_LEVEL=$(nproc)` (91) with per-package caps where memory demands (`webkitgtk`'s `-j4`, `device-builds.md`); `CONCURRENCY_LOAD` from `os.cpu_count()`, which ignores CPU affinity (lead 26).
- **The two time-to-play numbers:** untouched by this slice. The engine is not on the launch path. The one thing it writes that runs on a device at play time is nothing: the identity in `/etc/os-release` is read by `rocknix-info` on demand, not at a launch, and the launch table is read by EmulationStation at start, unchanged in size by any finding here.

### Q6 Dead ends

The five reachability tables are in `q6-tables.md`, each with its search command:

- **Table 1, the 30 scripts:** reached by a fork build: 21. CI only: `autoremove`, `build_mt`. By hand only: `ccache_stats`, `create_docker_package`, `create_addon` (with `tools/repo-tool`), `install_addon`, `update_packages`. Not the engine's at all: `test-audit-review.py`, misfiled. The `get_*` handlers are reached through `scripts/get`'s dispatch; their fixed-string zeros were not verdicts.
- **Table 2, the 139 fragments:** every one named by at least one of the five devices' tables (SM8550's names all 139); no system lacks one.
- **Table 3, the three configuration trees:** unreached by any fork build, image or CI; kept, because upstream reaches them and the fork merges through them.
- **Table 4, the 19 workflow files:** two run on the fork and never succeed (`Build`, `update-kernel-configs-docs`), one is skipped weekly by its gate, and the rest never run; nothing reads any result. T10's call.
- **Table 5:** `.merge-head` and `scripts/test-audit-review.py`.

Every unreached row carries its `Already written:` line in the table (nothing, in each case). No removal is proposed for a unit upstream reaches. The proposed removals are F-06's `ORIGIN_URL` and `BUILD_FILENAME` (the fork's comment and upstream's write) and F-07's dead lines in `build_compat`, each with `Already written:` in `05`.

### Q7 Clarity and structure

- **`config/functions`:** nine sections and about twelve responsibilities in 1,936 lines (the subagent's map, checked at its section boundaries):
  - core, 4 to 192;
  - the build system, 194 to 1009 (flags, toolchain files, package variables, debug and strip, the package cache, build-config save, checks, autoreconf);
  - packages, 1011 to 1438 (lookup, `calculate_stamp`, `find_path`, `pkg_call`, `source_package`, Python);
  - kernel, 1440 to 1530;
  - Kodi add-ons, 1533 to 1663;
  - users, groups and systemd, 1666 to 1721;
  - multithread locks, 1724 to 1913;
  - timing, 1915 to 1931;
  - the distro hook, 1933 to 1936.

  A reader new to it can find a helper by name, not by place. Splitting it is upstream's to decide, and a fork-only split would cost every LibreELEC merge.
- **The identity in four files:** `distributions/ROCKNIX/version` (the version and qualifier), `distributions/ROCKNIX/options` (the name and `BUILD_DATE`), `config/build-identity` (the rules), `scripts/image` (the use). Each file says what it holds, and `version`'s first line points at `build-identity`. `CLAUDE.md`'s `OS_VERSION/BUILD_DATE` sentence is #644 finding 14's, T4's.
- **Comments that disagree with the code:** `scripts/image` 71 (F-06); `get_env` 2 to 13 (F-01); `virtual/emulators/package.mk` 150 (T3's); `config/options` 98's "per project" for a per-build-root cache (the subagent's lead, re-read: `config/path` sets `CCACHE_DIR` under `$BUILD`); `device-builds.md` § After rebasing items 2 and 3 (F-05).
- **`scripts/mkimage`:** four bootloader blocks that each copy the same four files, two of them without the guard (F-16). The repetition is how the guard was lost.
- **Headers:** every upstream script names its origin (OpenELEC, LibreELEC, ROCKNIX); the fork's `config/build-identity` names ROCKNIX's copyright line as `packaging-and-patches.md` asks.

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)
- `device-builds.md` § After rebasing items 2 and 3: rewrite as history ("fixed in `5ce3dcc9d7`/`cb884edb0f`, upstream since PR #3213; the manual steps are for a root older than 2026-08-20") (F-05, T4's).
- `device-builds.md` § Build credentials: name the lower-case `~/.rocknix/options` the scripts read, and the two guide variables `get_env` drops (F-15; #644 finding 3).

### Codification Gaps (needs-new-rule)
- A stamp written in a running log is a `date -u` reading taken when it is written (this lane's friction twice; `lint-audit-artifacts` could refuse a log time ahead of its commit's).

### Recommended Action Sequence
The two High fixes first (F-16, F-25), each with its sandbox or trace, and F-18 with F-25 since both rewrite `_repo_exists_and_valid`; then the credential filter (F-01, F-02); then the table (F-03, F-04, proven by the regeneration); then F-09, F-17, F-19, F-20 under stream briefs that name the build proving them.

## Second opinion (Phase 4.6)

**Primary:** Claude Code, `anthropic/claude-opus-5-5`, Anthropic (the dispatch on #652, issuecomment-6379501933, and the session's model metadata). **Depth:** extended: three perspectives, two external reviewers from two other labs (OpenAI, Google), one refutation pass each (epic tier), each preceded by a probe (`second-opinions/review-plan.json`, written before any call). **Both seats ran, and both are graded below.**

**Run:** `tools/council/run invoke --member <m> --provider openrouter --prompt-file <abs>/second-opinions/<m>-brief.md --output <abs>/second-opinions/<m>-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`, the key sourced by the runner from `~/.config/council/env`. The gpt call ran under `tools/watch-build --record-only` (`.build-runs/20261024T054731Z-0b725524/`, `build.rc` 0). The watcher holds one run per worktree, so the gemini-argon call ran through the Facilitator directly, in parallel; its output and provenance are the Facilitator's own. Both briefs were built by `tools/build-briefs.sh` and committed before sending (`9c23bb5095`), each from the same packet, neither carrying the other's output.

**Identity** (each Facilitator receipt, `council-facilitator@1.14.1-pixelelated.2`; toolchain `verify-pins` OK and `test` 185 of 185 at 05:45):

| Seat | Probe | Refutation pass | Observed model / provider | Effort | Output sha256 |
| --- | --- | --- | --- | --- | --- |
| `gpt` | 05:47:07, rc 0, `provider_response` PASS, reply `READY unknown` | 05:47:31, 1,038,085 ms, rc 0, 0 retries, 45,291 reasoning tokens, brief sha256 `9fe8531132086a7a...` (246,501 bytes) | `openai/gpt-6-astra` / OpenAI (PASS) | max, PASS | `b8d3f25ce93ea19f38c146a56af0564c5f85cdae271cd2789d6197f0a9236884` |
| `gemini-argon` | 05:47:16, rc 0, `provider_response` PASS, reply `READY Gemini 4 Argon` | 05:47:53, 392,700 ms, rc 0, 0 retries, 32,195 reasoning tokens, brief sha256 `a88a961829f455a3...` (246,527 bytes) | `google/gemini-4-argon` / Google, route `google-vertex/global` (PASS) | high, PASS | `c7ea46aa7154961cd1c41f96d5eafde3fad28068aaf406951365cc2da1c9ea16` |

Every seat item is a lead until this lane reads its site. The two seats disagreed on F-18 (Argon: High stands; Astra: Medium) and agreed on F-16 (High) and on the dirty check (Argon G-01, Astra G-10, F-23). Neither proposed withdrawing a finding. Astra's G-01 is the one item that changed the audit's top: it is **F-25, High**, proven by P14.

**Outcome, carried to `05`:**
- Added: F-25 (High), F-23 and F-24 (Low).
- Re-graded: F-18 from High to Medium, and F-17 from Medium to Low.
- Narrowed: F-02, F-03, F-16, F-19, F-20 and F-22.
- Fix shapes extended: F-04, F-08, F-09, F-13, F-16, F-18, F-19, F-21 and F-24.
- Declined, each on an artifact: the seats' re-grades of F-08, F-15, F-19 and F-22, and items G-04 (Argon) and G-09 and G-17 (Astra).
- Final count: **25 findings, 26 punch items: 2 High (F-16, F-25), 7 Medium, 17 Low.**

### Argon's items, graded against the artifacts

Every seat item is a lead. Each grade below rests on this lane's own read of the cited lines at `8ebaf8daad` (`git show 8ebaf8daad:<path>`, 05:54-06:02 UTC, `date -u` readings), a sandbox, or a read-only look at an M7 build root, never on the seat's wording. Grades: **confirmed**, **agree, narrowed**, **agree, re-graded**, **folded** (into the named finding's punch item), **disagree** (with the artifact that refutes it).

**New findings (G-01 to G-17).**

| Seat item | Grade | Severity | Evidence from this lane's read |
| --- | --- | --- | --- |
| G-01 `config/build-identity:37` | **confirmed, re-graded High → Low**; new finding **F-23** | Low | `$(git status --porcelain=v1 ...)` has no status check, so a failing `git status` reads as clean and stamps `BUILD_DIRTY=no`, where line 16 returns on a failing `rev-parse`. The guard fails open (`engineering-practices.md` § Guards must fail closed). Narrow: the usual failures (dubious ownership, no repository) also fail line 16 first, and `git status` exits 0 with an `index.lock` present, so the open path needs a status failure that `rev-parse` does not share. Fork code (D-WORKFLOW-157). |
| G-02 `scripts/image:61,104,111` | **agree, narrowed**; the freeze half **disagree** | Low, folded into F-09 | That the identity is frozen at 61, before the package build, is by design: the identity names the commit the build started from, and `worktrees.md` forbids moving a worktree under a running build. The orphan half stands: `.identity.json` is written at 111, before `do_mkimage` (334/337), so a failed `mkimage` leaves a sidecar that names an image that does not exist. A retry with the same frozen `BUILD_TIMESTAMP` is then refused at 79-82, which is the policy (never reuse an identity). On `make <DEVICE>`, `build_distro`'s prune removes the sidecar first (F-09). Goes into F-09's item: write the sidecar after the image's checksum. |
| G-03 `scripts/build_distro:78` | **confirmed**; new finding **F-24** | Low (upstream's, identical at `upstream/next:72`) | The `Makefile` sets `DEVICE_ROOT` only for RK3566 (`Makefile:65-66`) and `unset`s it for every other target, so on H700, SM8550 and GENERIC_X64 line 78 removes `build.pixelelated-.<arch>/...`, a path that does not exist (read-only: no such directory beside the M7 roots). The initramfs is therefore never cleaned on the fork's devices. The M7 H700 root's `.stamps/initramfs/build_init` is dated 2026-10-07 07:12, and its `.stamps/image/build_target` is dated 2026-10-11 22:49. Whether the initramfs carries a stale version string is **not checked**. |
| G-04 `scripts/build_distro:72-93` | **disagree** | none | With `ENABLE_32BIT` not `true`, the `ARCH=arm` call cleans stamps in an arm root that is then not built (no cost) and prunes `target/<distro>-<device>.arm-*`, which only an arm image would match, and none is made. Nothing the next call needs is removed. |
| G-05 `scripts/get_git:33-48` | **agree, narrowed: no effect**; folded into F-18 | Low | The four error returns do skip `popd`. But `PACKAGE` is absolute (`scripts/get:27`, `SOURCES` from `config/path:10`), and `_get_repo`'s `cd ..` (129) runs before the clone. The clone and `rm -rf "${PACKAGE}"` do not depend on the working directory. F-18's fix rewrites this function, so the `popd` goes in with it. |
| G-06 `scripts/get_git:214-233` | **disagree** as a defect; **corrects F-18's wording** | none | A fresh clone is reset to the pin at 137 (`git reset --hard "${PKG_VERSION}" \|\| return 1`), so its `HEAD` is `PKG_VERSION`. The check at 214-233 compares only `PKG_GIT_SHA`, as the seat says. `02` F-18's sentence that "the fresh-clone path checks `HEAD` correctly (212 to 218)" cites the wrong lines: the fresh path is right because of 137. Corrected in F-18's item. The seat's point that the fix must accept the abbreviated hash that line 8 documents is adopted: compare `git rev-parse HEAD` with `git rev-parse "${PKG_VERSION}^{commit}"`. |
| G-07 `scripts/get_git:26-29,199` | **confirmed**; folded into F-18 | (part of the High item) | `_repo_exists_and_valid && exit 0` runs the function on the left of `&&`, so `set -e` does not apply inside it. `git restore --staged .` exits 0, so `git switch --force` never runs, and `git clean -fdx` removes only untracked files. A cached clone with an edited tracked file is accepted as it is. The one fix covers both halves: verify the pin, then `git reset --hard` to it. |
| G-08 `scripts/get_git:41,201-203` | **confirmed, latent**; folded into F-18 | Low | No recipe at `8ebaf8daad` sets `PKG_USETOKEN` (`git grep`: only `get_git:201`). If one did, the token would sit in the clone's `.git/config` and line 41 would miss the cache at every fetch. Note for F-01: `ROCKNIX_GHTOKEN` is a fused name that `DROP` does not match (the `GHTOKEN` component is not `TOKEN`), the same shape as P1's `DOCKERHUBTOKEN`. |
| G-09 `scripts/mkimage:31-53` | **confirmed**; folded into F-16 | (part of the High item) | `trap cleanup SIGINT` with a `cleanup` that does not exit lets an interrupted `mkimage` carry on with `IMG_TMP` gone. With F-16's unchecked steps and closing bare `exit`, that can still end 0. Neither `cleanup` nor `show_error` removes the partial `${DISK}` (53). F-16's item adds a trap that exits non-zero and removes `${DISK}`. |
| G-10 `scripts/mkimage:303-316,327-330` | **agree, narrowed: unreached on the fork**; folded into F-16 | Low | The OVA block runs only when `PROJECT` is `Generic` (287), and all 27 `PROJECT=` settings in the `Makefile` are `ROCKNIX` (`Makefile:46-113`). `SUBDEVICE` is not set by any image build: the only assignments are on-device in `RK3326`/`RK3399` `bootloader/update.sh`. The checksum subshell's unchecked `sha256sum` (327-330) is already in F-16's fix ("`exit 0` only after the checksum is written"). |
| G-11 `scripts/get_archive:4-8,41-54` | **agree, narrowed**; folded into F-19 | Low | `STAMP_URL`'s content is never compared, but with `PKG_SHA256` set line 6 compares the checksum, so this matters only for the unhashed recipes F-19 already covers. The leftover-archive half has no effect: the stamps are removed at 30, so line 5 refuses the leftover file at the next run. |
| G-12 `scripts/update_packages:40-64` | **confirmed, and wider than the seat says**; folded into F-19 | Low (unreached: `make update` has never run on the fork, `q6-tables.md` Table 1) | Line 52 deletes `PKG_SHA256` from every non-git recipe it visits, including one already up to date, and line 61 rewrites only a `PKG_SHA256=""` line, which line 52 has just removed. So no checksum is ever written back. This is the tool that would produce F-19's unhashed state, and F-19's fix (refuse an empty `PKG_SHA256`) has to keep it from running unchanged. |
| G-13 `config/functions:1112-1126,1188-1205` | **agree**: F-17 broadened | Medium (F-17) | `calculate_stamp` hashes `PKG_DIR`, the project patches and packages, and the device patches (1112-1113). `find_path` also searches `devices/$DEVICE/packages/$PKG_NAME` (1188) and `$DISTRO_DIR/$DISTRO/packages/$PKG_NAME` (1192). In the tree, 27 device or distribution package directories exist, and 2 have no `package.mk`: `devices/RK3566/packages/linux/modprobe.d/rtw88.conf`, which is read by `scripts/install` (80-82, 152-154; install stamps are removed at every image, `scripts/image:95`, so it is current), and `devices/AMD64/packages/initramfs/config/initramfs.x86_64.conf` (reader not found by search; not a fork device). No further shipped instance was found for the five devices. The wildcard half (1201-1202 ignores `-f`/`-d`, `FOUND_PATH` is the unexpanded glob) goes to F-21 as Low. |
| G-14 `scripts/unpack:90-105` | **agree, narrowed**; folded into F-08 | Low | The `mkdir` at 105 is by design for packages with no archive. For an archive whose top directory matches neither pattern, the build fails at configure instead of succeeding wrongly. F-08's fix (fail when an archive was extracted and nothing moved to `.intermediate`) covers both the zero-match and the many-match shapes. |
| G-15 `distributions/ROCKNIX/config/functions:129-214` | **agree, narrowed: latent**; folded into F-03 | Low | All 139 `add_es_system` calls in the tree have their fragment (a search of the calls against `config/emulators/*.conf`: 0 missing), and the fragments escape their own entities (`gameandwatch.conf:2` `Game &amp; Watch`). `2>&1 >/dev/null` sends `xmlstarlet`'s errors to the build log, which loses nothing. F-03's fix adds a refusal of a missing fragment. |
| G-16 `Makefile:150,153,205-208` | `.env` half **disagree**; `-n` half **confirmed**, folded into F-13 | Low | Docker reads `--env-file` when the container starts, so a later `.env` rewrite or delete by another recipe does not change a running container. The `-n` tests at 150 and 153 mount a set but missing path, which makes Docker create an empty host directory. That is Docker's documented `-v` behaviour; it was not run here (brief § 5). |
| G-17 `scripts/makefile_helper:10-11` | **agree, narrowed: latent**; folded into F-22 | Low | Sourcing `config/options` with `PROJECT= DEVICE= ARCH=` and a scratch `HOME` printed exactly one line, the echo (sandbox, between 05:54 and 06:00). A user's options file that prints would corrupt `BUILD_ROOT`, and line 13 guards only against empty. |

**The first reader's findings.**

| Item | Grade | Result | Evidence |
| --- | --- | --- | --- |
| F-16 | **confirmed** | High | -- |
| F-18 | **confirmed, wording corrected** | High | See G-06 and G-07: the fresh path is right because of 137, and the cache path also keeps edited tracked files. |
| F-01 | **confirmed** | Medium | The seat's allowlist is one fix shape for the stream brief to weigh against the extended `DROP`. |
| F-02, F-03, F-04, F-09, F-20 | **confirmed** | Medium | -- |
| F-17 | **agree, broadened** | Medium | G-13 |
| F-19 | **disagree with the re-grade to High**, kept Medium | Medium | Of 1,347 archive recipes (`PKG_URL` not ending `.git`), 8 lack a `PKG_SHA256` line; `wavpack`, `zlib` and `libevdev` inherit one from the generic recipe they source. The unverified-TLS fetch is therefore checked by a hash for all but a handful (`rkbin` is one). The exposure is real and narrow; Medium stands. |
| F-22 | **disagree with the re-grade to Medium**, kept Low | Low | The seat's reason, that `chmod -R` fails on dangling symlinks, is **refuted**. In a scratch tree with two dangling symlinks, `chmod -R u+rwX` exited 0 (the host's `chmod`, uutils coreutils 0.10.0, which is what `make distclean` runs; GNU documents that symlinks met in a recursive walk are ignored). The same command over a glob that matches nothing exited 1, which is F-22 as written. |
| F-08 | **disagree with the re-grade to Medium**, kept Low | Low | G-14: the empty build directory fails the build at configure, not silently. |
| F-15 | **disagree with the re-grade to Medium**, kept Low | Low | The fast development loop runs inside `make docker-shell`, whose `.env` carries the four credentials (`Makefile:1` includes the upper-case file, and `get_env`'s `KEEP` passes them). Only a bare host shell misses them, and the images are built through `make`. |

**What the seat could not judge** (part 3) is the coverage boundary `04` already states: the three Python builders, the 16 Group 2 files read by the subagent, the excerpt gaps in `scripts/build`, `scripts/build_compat` and `scripts/install`, and the container's runtime. One item is answered here: the recipe-level exposure count for F-19 (above).

### Astra's items, graded against the artifacts

The same standard as Argon's table above: each grade rests on this lane's read at `8ebaf8daad`, a sandbox, or a read-only M7 artifact (06:04-06:11 UTC, `date -u` readings).

**New findings (G-01 to G-19).**

| Seat item | Grade | Severity | Evidence from this lane's read |
| --- | --- | --- | --- |
| G-01 `scripts/get_git:26-34,199` | **confirmed by sandbox**; new finding **F-25** | **High** | P14 (`tools/sb-get-git-pushd.sh`, 06:07:52): a cache directory at mode 000 makes `pushd` fail, `_clean_repo` runs anyway (the function is on the left of `&&`, so `set -e` does not apply), and `git clean -fdx` removes the fixture worktree's `build.fixture-1/`, `sources/`, `.gitignore` and untracked file. Only `.git` is left, and the check prints `rejected rc=1`. Upstream carries the same lines (`upstream/next` 26 to 35). How such a directory arises on this host was not found; the loss is hours of build output. |
| G-02 `scripts/get_git:26-28` | **confirmed**; folded into F-18 | (F-18) | The same as Argon G-07. And `git clean`'s failure is hidden: `_clean_repo`'s status is the last command's. |
| G-03 `scripts/get_git:194-206,239` | **confirmed by a recorded run**; folded into F-21 | Low | Bare `main` (239) drops the arguments, so `lock_source_dir ""` (196) locks `${SOURCES}/` itself (`scripts/get:17`), which serialises every git fetch on one lock. The SM8550 run `20261024T020912Z-68374394`'s log (read through the filter) shows `GET       (git)` with no package name. |
| G-04 `scripts/get_git:15-16,36-38` | **confirmed, latent** (this lane's lead 5); folded into F-18 | Low | F-18's fix replaces the pipe with `git rev-parse`. |
| G-05 `Makefile:179,205-208` | **agree, narrowed**; folded into F-13 | Low | The race is real, since `BUILD_WATCH` takes its lock in the `docker run` line after `.env` is rewritten (205-208). Its outcomes are loud (`docker` cannot open a removed `--env-file`) or benign (both recipes write the same `get_env` output). One builder per worktree is the rule (`worktrees.md`). |
| G-06 `scripts/get_env:16-22` | **confirmed**; folded into F-01/F-02 | Low | A failed `echo` (a full disk) is not the script's status when a later iteration runs `continue`, so a truncated `.env` can pass the `Makefile`'s check (207). |
| G-07 `Makefile:153,207-208` | **confirmed by reading**; folded into F-13 | Low | Not run (no `make`, brief § 1). `projects/ROCKNIX/packages/rocknix/package.mk:36-39` does read `LOCAL_SSH_KEYS_FILE` in the container, so an exported value replaced by `-v "path:path"` reaches a `cp` that fails, a loud build failure. Nothing in the container reads `EMULATIONSTATION_SRC` (`device-builds.md` § Iterating on EmulationStation). |
| G-08 `scripts/get_archive:4-11` | **agree, narrowed**; folded into F-19 | Low | The same as Argon G-11. |
| G-09 `scripts/get_archive:23,33-35` | **disagree** | none | `DISTRO_MIRROR` is set for this distribution (`distributions/ROCKNIX/options:186`), so `PACKAGE_MIRROR` is a real mirror URL. |
| G-10 `config/build-identity:36-43` | **confirmed** (= Argon G-01), F-23; Medium **not** adopted | Low | See Argon G-01: the open path needs a `git status` failure that `rev-parse` at 16 does not share. |
| G-11 `scripts/image:74-75,111-124` | **agree, latent**; folded into F-09 | Low | None of the 47 `IMAGE_SUFFIX` or `UBOOT_SYSTEM` values in the tree carries a quote, a backslash or a glob character (search, before 06:07). |
| G-12 `scripts/image:74-81` | **agree, latent**; folded into F-09 | Low | As G-11: no value carries `[`, `*` or `?`. F-09's fix uses a literal test. |
| G-13 `config/functions:1114,1126-1129` | **confirmed**; folded into F-17 | Low (F-17) | `find -L ... -not -name '.*'` then `sha256sum`: modes are not hashed, a symlink is hashed by its target's content, and dotfiles are skipped even when `PKG_NEED_UNPACK` names them. No shipped case was looked for. |
| G-14 `config/functions:1180-1204` | **confirmed** (= Argon G-13's wildcard half); folded into F-21 | Low | -- |
| G-15 `distributions/ROCKNIX/config/functions:144-157` | **agree, latent** (= Argon G-15); folded into F-03 | Low | The fragments escape their own entities. |
| G-16 `scripts/build_distro:72-78` | **confirmed**; folded into F-24 | Low | `2>/dev/null \|\| true` is deliberate, so that a package never built does not stop the device build, but it also hides a real failure. F-24's item asks for the failure to be named. |
| G-17 `scripts/build_distro:44-64` | **disagree: unreached** | none | The block runs only when `DEVICE_ROOT` is set and differs from `DEVICE` (41-42). The only target that sets it sets it equal (`Makefile:65-66`, RK3566). |
| G-18 `scripts/unpack:94-100` | **agree, latent**; folded into F-08 | Low | The fallback is upstream's. The fix moves only a directory this unpack created. |
| G-19 `scripts/mkimage:31-34,49` | **confirmed** (= Argon G-09); folded into F-16 | (F-16) | -- |

**The first reader's findings.**

| Item | Grade | Result | Evidence |
| --- | --- | --- | --- |
| F-16 | **confirmed, wording narrowed** | High | The checked steps exit 1 through `show_error`. The script exits 0 when it reaches its end after an unchecked failure, not always. The checksum is unchecked too. Astra could not see the SM8550 hook, and it was read here: `projects/ROCKNIX/bootloader/mkimage` (no device hook exists) sets no shell option, and its own SM8550 copies (82, 110) are unchecked. |
| F-18 | **agree, re-graded High → Medium** | Medium | Astra's question, how `PACKAGE` is keyed, is answered against High. `PKG_SOURCE_NAME=${PKG_NAME}-${PKG_VERSION}` for a git URL (`config/functions:1350`) and `PACKAGE="${SOURCES}/${1}/${PKG_SOURCE_NAME}"` (`scripts/get:27`), so a pin bump gets a new directory and a fresh clone reset to the pin (`get_git:137`). The defect stands for a directory of the right name whose `HEAD` moved or whose tracked files were edited (G-02). The image-level consequence `02` first gave needs that rarer state. Argon kept it High on the predicate alone. Astra's reading is the one the code supports. |
| F-17 | **agree, re-graded Medium → Low** | Low | Astra asked about the automatic clean lists. `kernel-firmware` is in `CLEAN_OS_BASE` (`distributions/ROCKNIX/options:45`), cleaned at every `make <DEVICE>` without `DIRTY` (`build_distro:72-77`). The stale firmware set needs a single-package or `DIRTY` build. |
| F-01 | **confirmed** | Medium | -- |
| F-02 | **confirmed, wording narrowed** | Medium | `Makefile:208` also passes `RASTERATOPS_BUILD_RUN`, `BUILDER_NAME` and `BUILDER_VERSION` by `-e`. `02`'s "the rest" means every other name. |
| F-03 | **confirmed, narrowed** | Medium | "Launches nothing" means a following system that sets no command of its own. |
| F-04 | **confirmed; the fix shape is extended** | Medium | Case A's status is 2, a failure with no diagnostic and a truncated table, not a success. `core[last()]` alone lets two `true` rows produce two well-formed defaults, so PL-06 also refuses a second `true` row by name. |
| F-09 | **confirmed** | Medium | Scoped to `./target`, as `05` says: the candidate store is not touched. |
| F-19 | **confirmed, narrowed** | Medium | The exposure count Astra asked for: 8 of 1,347 archive recipes lack a `PKG_SHA256` line, and 3 inherit one. |
| F-20 | **confirmed, narrowed** | Medium | Not "on every entry": the compiler switch needs Debian or Ubuntu, `gcc-12` and no `gcc-12` in the query (296-306), and `/nix` is skipped when it is already writable (324-326). |
| F-15 | **disagree with the re-grade to Medium**, kept Low | Low | As Argon's row. |
| F-22 | **agree, split** | Low | The statistics half reaches only `scripts/build_mt` (16, bare, under `config/path`'s `set -e`), upstream's CI route. `scripts/image:104` and `scripts/build_compat:100` call it on the left of `\|\|`, and `create_addon:188` inside `if`. The `distclean` half stands. |

**What Astra could not judge** (its part 3). Answered here:
- the cache keying (F-18, above);
- the SM8550 hook (F-16, above);
- the clean lists (F-17, above);
- the recipe count (F-19, above);
- `lock_source_dir`'s body (`scripts/get:16-22`, G-03).

Left as the coverage boundary: the planner and builder (`pkgbuilder.py`, `genbuildplan.py`), `actionlint`, the container's package contents, and #801's two failures, which stay failures (`02` § Mechanical checks says expected, not passed).

## Quality Self-Check

- Every PASS in `02` cites a primary artifact, and says what would have failed it.
- Every finding was re-read at its site, and the subagent's leads were re-read before use. One lead was withdrawn, and seventeen stay leads.
- No build, container, guest or device was used; no credential or log define reached an artifact (every log read went through `readlog`).
- Two of my own errors are recorded, not hidden: stamps written ahead of the clock (corrected at 04:31, a friction line), and two sandbox scripts that wrote beside themselves (corrected before commit).

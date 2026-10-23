# The fork's build path read against ROCKNIX's documentation and scripts

**Issue:** #644 (M6.P1), the maintainer's request of 2026-10-23 recorded in
D-WORKFLOW-186: *"There's documentation on how the builds are generated via
the Docker image on ROCKNIX. It might be worth you going through everything
on the website to see how they've structured it, because we may find there
are better ways to generate builds, etc."* **Status:** read complete,
2026-10-23; every finding names the slice or issue that carries it (§ 4).
**Method:** a read-only research subagent on Opus 5.5 (D-WORKFLOW-183)
gathered the site's pages, upstream's build files and workflows, and the
fork's delta against them, and reported differences without judgement; the
coordinator lane verified the load-bearing claims against the tree and
GitHub (§ 5) and wrote the comparison. No build, container or device was run.

**Reference points.** `upstream/next` at `c1f1746828` (2026-10-23);
`next` at `8ebaf8daad` (2026-10-17); their merge base `c445081a59` is
upstream's release tag `20261001`. Upstream is 315 commits ahead of `next`
(204 non-merge). The site's pages were fetched 2026-10-23 00:39 UTC from
`https://rocknix.org/sitemap.xml` (188 URLs, all dated 2026-10-03).

## 1. What was read

The contribute section's navigation lists **seven pages**, all read in full
(the date is the last commit to the page in `ROCKNIX/rocknix.org`):

| URL | Title | Last edited | What it holds |
| --- | --- | --- | --- |
| https://rocknix.org/contribute/ | Contributing to ROCKNIX | 2024-04-10 | GitHub Flow in five steps (fork, branch from `dev`, build and test locally, document, PR to `dev`); style; licence; "become the maintainer of your contribution" |
| https://rocknix.org/contribute/code-of-conduct/ | Code of Conduct | 2024-04-10 | Contributor Covenant 2.0; no build content |
| https://rocknix.org/contribute/build/ | Building ROCKNIX locally | 2026-08-10 | the build guide: host and disk, Docker install, clone, `make docker-image-build`, `make docker-<SOC>` / `make <SOC>` / `world`, the rightsizing options, the `~/.ROCKNIX/options` variables, cleaning, troubleshooting |
| https://rocknix.org/contribute/build-gh/ | Build using GH runners | 2025-10-29 | fork `distribution` and `distribution-cache`, a classic PAT as `GH_PAT`, run the `Build` workflow; first run about 13 hours |
| https://rocknix.org/contribute/modify/ | Modifying ROCKNIX | 2026-07-04 | one package in `docker-shell` (`scripts/clean`, `scripts/build`), patches, a modified image (`scripts/install`, `scripts/image mkimage`), push to a device over scp |
| https://rocknix.org/contribute/quirks/ | Adding Quirks | 2024-04-10 | panel-orientation kernel quirks; hardware quirk folders by DMI name |
| https://rocknix.org/contribute/packages/ | Structure of package.mk files | 2026-07-04 | the `package.mk` reference, `tools/pkgcheck`, adding a package |

Seven more pages were read because their titles or paths name building,
updating or releasing: `play/update` (OTA, scp to `.update`, development
builds on Discord), `play/install`, `play/installtointernal` (scanned),
`configure/h700-installation` (`dtb.img`), `configure/packages` (Entware on a
device), `systems/build-engine` (a game system, unrelated) and `faqs`. The
other 174 pages of the sitemap (77 device pages, 85 game-system pages, the
rest of configure and play) were downloaded and their titles checked; none
names build, develop, test, release, docker, CI, package or PR, and a
full-text search of all 188 for "docker" matches only the build and modify
pages. **Not read:** the Discord dev-builds channel (login), the pages'
screenshots, and Docker Hub's web page (its API was read instead).

Upstream files read at `c1f1746828`: `Dockerfile`, `Makefile`,
`scripts/get_env`, `scripts/build_distro`, `scripts/image`,
`scripts/update_packages`, `config/blocklist`, `README.md`, `AGENTS.md`,
`.github/pull_request_template.md` and all 19 workflows. Fork files read at
`8ebaf8daad`: the same paths, `config/build-identity`, the four `fork-*`
workflows, and the headers of `tools/watch-build`, `watch-build-submit`,
`watch-job`, `build-preflight`, `host-maintenance/`, `rc-preflight`,
`fork-package-freshness` and `build-identity-test`.

## 2. Upstream's build path, as documented and as scripted

**Locally**, the guide's path is a clone at `~/distribution`, a builder
image made with `make docker-image-build`, then `make docker-<SOC>` (or
`make <SOC>` on a matching Ubuntu 22.04 host), with options on the make line
(`BASE_ONLY`, `ENABLE_32BIT`, `EMULATION_DEVICE`, `CONTAINER_SUPPORT`) and
the per-user variables in `~/.ROCKNIX/options`. One package is
`scripts/clean` then `scripts/build` inside `make docker-shell`; a modified
image adds `scripts/install` and `scripts/image mkimage`; a device is
updated by copying the tar to `~/.update` and rebooting. The Makefile runs
`ghcr.io/rocknix/rocknix-build:latest`, writes `.env` from every exported
variable each time make parses a `docker-%` target, and mounts the options
file, the SSH keys file and `EMULATIONSTATION_SRC` when set.

**In CI**, a device is not one `make`: `build-device.yml` runs a staged
graph on separate runners (arm, the aarch64 toolchain, the base with
`EMULATION_DEVICE: no` and `ENABLE_32BIT: no`, rust, mame-lr, qt6, the
libretro cores, the standalone emulators, then the image), each stage
driving `scripts/build_mt <packages>` in the same container, passing zstd
build-root tarballs as artifacts, deleting package build directories after
install (`AUTOREMOVE`), retrying each step up to six times and re-running
failed jobs up to three, with ccache kept as release assets of
`distribution-cache`. The build container is rebuilt from the Dockerfile and
pushed on every non-PR run; the image job cleans `retroarch` and
`emulationstation` first so they rebuild with 32-bit support and with the
repository's scraper and achievements credentials. An official release is
built on the first of each month and published from CI with generated notes;
nightlies go to `distribution-nightly` and SourceForge.

**Packages** are bumped by `make update` (`scripts/update_packages`): the
dependencies of the emulators, es-themes and gamesupport virtual packages,
each moved to its branch's head commit unless `config/blocklist` holds it
back. Generic `packages/` arrive by merging `LibreELEC/master` (last
2026-08-11), and a PR that touches `packages/**` fails outright
(`trigger-fail-if-upstream-changed.yml`, since 2026-03-04); upstream's
`AGENTS.md` says recipes go under `projects/ROCKNIX/packages` or a device's
`packages`. Since the `20261001` base, upstream has deleted 22 ROCKNIX
overrides so the generic LibreELEC recipes apply (PRs #3415, #3470, #3513),
dropped `aethersx2-sa` for a licensing concern, replaced `rocknix-abl` with
`openabl` and removed grub support.

**Pull requests** are validated for the commit-message shape the fork's
rules already state, must carry the `bugfix` label in the last seven days
of a month (for October 2026, from the 25th), merge through a merge queue,
and use a template asking for the devices tested, build artifacts or a
commit, test evidence, and an AI-assistance disclosure; upstream's
`AGENTS.md` requires `.img.gz` and `.tar` artifacts linked in the PR for
every affected device.

**Where upstream's documentation and scripts disagree** (so the fork's
corrections are worth keeping): the guide says images land in `release/`
(they land in `target/`); the contribute page says branch from and PR to
`dev` (only `next` exists); the modify page uses `PROJECT=Rockchip` and lists
`Amlogic`, `PC`, `Rockchip` (the Makefile and CI use `ROCKNIX`); the guide
says the container is hosted on Docker Hub (last updated 2024-06-05; the
Makefile pulls GHCR, rebuilt 2026-10-22); the guide's "all devices" table has
AMD64 and SM6115, `world` builds 11 SoCs without them, CI builds 13.

## 3. The fork's build path

The fork keeps upstream's engine and changes how it is run. The container
is a by-hand mirror pinned by digest (`ghcr.io/pixelelated/build@sha256:988c…`,
the upstream image of 2026-09-25; `fork-mirror-build-container.yml` refreshes
it and prints the pin) and the digest is written into every image as
`BUILDER_VERSION`. Every native device target and every watched `docker-%`
target runs under `tools/watch-build`, which needs a single-use admission
receipt from `tools/host-maintenance/build-admission` (#493), takes a
per-worktree lock and keeps a run record (`.build-runs/<id>/`); `scripts/build`,
`install`, `image`, `build_distro` and `build_compat` re-enter the same run.
`.env` is written owner-only inside the recipe, deleted on exit, and
secret-shaped variable names are dropped except the four EmulationStation
build credentials (D-INFRA-006). Images are named from `config/build-identity`
(`pixelelated-<DEVICE>.<arch>-0.0.1-dev+<UTC>.g<hash>-from-ROCKNIX`), carry an
`identity.json`, and an existing identity is never overwritten
(D-WORKFLOW-157). Builds run in frozen `build/*` worktrees with the main
`.git` and the shared source cache mounted. Meson may not download wrap
subprojects (#226). A candidate is cut only after `tools/rc-preflight`
(D-WORKFLOW-047): the fork-introduced packages current
(`tools/fork-package-freshness`), both bases level with ROCKNIX, no bug
without a disposition. Nothing is published from CI (D-WORKFLOW-119/120);
the fork CI runs the record checks, the tool self-tests and the wordlist
scan. Upstream PRs are built by content onto `upstream/next` as one commit
(`fork-workflow.md`), and testing is the GENERIC_X64 VM (`tools/vm-qa`,
`tools/vm-upgrade-rehearsal`) before any device.

## 4. Findings

One row per difference. *Deliberate* names the rule, register row or commit
that chose the fork's side; *candidate* means nothing in the tree says the
difference was chosen, and the carrier decides. Carriers are the third
order's slices (`docs/reviews/order.md`): T4 the doctrine, T5 the build
engine, T6 upstream's tools, T7 the generic packages the image builds, T8 the
image's own packages, T9 build supervision, T10 the guards, T11 the test
image, T12 the VM harness.

| # | Upstream | The fork | Difference | Deliberate, or candidate | Carrier |
| --- | --- | --- | --- | --- | --- |
| 1 | runs `ghcr.io/rocknix/rocknix-build:latest`, rebuilt from the unchanged Dockerfile on every CI run (current image 2026-10-22) | runs a digest-pinned mirror of the 2026-09-25 image; `docker-image-build` tags `:local`, never the pin | the pin is four weeks of Ubuntu package updates behind; the mirror workflow has run once | deliberate pin (`440ad22b68`, 2026-10-01; `device-builds.md` § After rebasing, step 1); the refresh cadence is a candidate | T5: refresh the mirror from upstream's current digest as its first act and say when the pin moves (each upstream base merge is the natural moment) |
| 2 | the guide says the container is on Docker Hub (2024-06-05) and builds it locally; the Makefile pulls GHCR | documents `make docker-image-pull` of the pin as the first step | the fork's documentation is the accurate one | deliberate (`CLAUDE.md` build commands) | T4: keep; nothing to change |
| 3 | writes `.env` from every exported variable whenever make parses a `docker-%` target | writes it owner-only in the recipe, deletes it on exit, drops secret-shaped names | the guide's shell `export LOCAL_SSH_KEYS_FILE=…` and `LOCAL_WIFI_KEY=…` do not reach the container through `.env` in the fork; set in `~/.ROCKNIX/options` they do | deliberate (`a79b7f82a5`, D-INFRA-006) but undocumented: no fork document says the two guide variables must live in the options file | T5: a sentence in `device-builds.md` § Build credentials naming the two variables, or a `get_env` comment; no code change |
| 4 | passes `BUILDER_NAME`/`BUILDER_VERSION` nowhere, though `scripts/image` writes them when set | passes the container digest as `BUILDER_VERSION` into `/etc/os-release` | the fork's images say which container built them | deliberate (the Makefile comment) | T5: keep |
| 5 | `make <SOC>`, `make docker-<SOC>`, `scripts/build`, `scripts/install`, `scripts/image` run directly, as the guide and modify page show | the same commands enter `tools/watch-build` and refuse to start without an admission receipt and the worktree lock | the site's command sequences do not run unchanged in the fork; a reader of the guide meets "build admission required" | deliberate (D-WORKFLOW-142 #394, #493) | T4: `CLAUDE.md` and `device-builds.md` already say so; T9 checks the refusal message names the guide to the admission tool |
| 6 | CI drives every stage with `scripts/build_mt`; `scripts/clean` is the documented first step of a one-package rebuild | `build_mt` and `clean` carry no watch guard; the watched set is build, install, image, build_distro, build_compat | a top-level `build_mt` run would start unwatched children that then re-enter their own run; behaviour not exercised | candidate | T9: exercise `build_mt` and `clean` under the watcher with a record-only run; wrap or document |
| 7 | no host memory or capacity gate; fixed disk figures (200 GB, 1 TB) and "about ten hours" | memory-bound host: `build-preflight`, guarded swap reclaim, per-build admission with measured retention, webkitgtk capped at `-j4` | the fork measures what upstream estimates | deliberate (D-INFRA-015/018/022/023, #493) | T9: keep; the admission's measured figures replace the guide's |
| 8 | CI builds a device as a staged graph on fresh runners with `AUTOREMOVE`, six retries per step, three re-runs per job, ccache trimmed per stage (500 MB to 4.5 GB) and kept as release assets | one whole-device run in a frozen worktree, no automatic retry, a 15 GB ccache per build root, poisoned packages enumerated by hand after a kill | different shapes for different hosts; the fork's rules forbid the retry loop (`engineering-practices.md` § Stop after three fixes) | deliberate for the retries and the frozen worktree (`device-builds.md` § Where to build; D-WORKFLOW-005); candidate for the ccache settings | T5: compare `config/options`' `CCACHE_COMPRESSLEVEL=0` and `CCACHE_SLOPPINESS` with CI's `6` and the `include_file_*` additions, and decide with a measurement, not by precedent |
| 9 | CI's image job cleans `retroarch` and `emulationstation` before the final image because its base stage built them without 32-bit support and without credentials | a single local run builds them once with the options and credentials in force | no local gap: the CI step repairs a staging artefact the local path never creates | not a difference in the product | T5: note it in the engine's audit so nobody imports the step |
| 10 | meson may download wrap subprojects at configure time | `--wrap-mode=nodownload` for host and target | pango built an unpinned cairo for three months upstream and here; upstream still can | deliberate (#226, blindspot 47) | #585: a candidate upstream contribution (D-WORKFLOW-164); T5 keeps it |
| 11 | `sources/` inside the clone; the `distribution-sources` mirror refreshed weekly by CI | one shared download cache (`SOURCES_DIR` or a mount); `DISTRO_MIRROR` unchanged, so the fork downloads from ROCKNIX's mirror; the fork's copy of the mirror workflow is skipped by its repository gate | the fork depends on upstream's mirror and its own cache, with no mirror of its own | candidate | T5: record the dependency; a mirror of our own is a decision for the maintainer only if upstream's goes away |
| 12 | the guide assumes a plain clone; `world` is 11 SoCs; no `GENERIC_X64` | worktrees with the main `.git` mounted; `world` adds `GENERIC_X64`; the VM device and its boot files are the fork's | the test image is a fork-only device every proof runs on | deliberate (D-INFRA-025, D-WORKFLOW-185; `worktrees.md`) | T11: keep |
| 13 | images named by date (`ROCKNIX-<DEVICE>.<arch>-<YYYYMMDD>`), `CUSTOM_VERSION`/`CUSTOM_IMAGE_NAME` honoured, a same-day rebuild replaces the files, `OS_BUILD` official/nightly/community | `config/build-identity`: semantic version, UTC timestamp, commit, `.dirty`, `identity.json`, custom names refused, an existing identity never overwritten, `OS_BUILD` dev/rc.N/stable | the fork can tell two same-day builds apart; upstream cannot | deliberate (D-WORKFLOW-157, D-WORKFLOW-159; `docs/releases/versioning.md`; `tools/build-identity-test`) | T5: keep; T9 reads the identity test |
| 14 | the modify page exports `OS_VERSION=$(date +%Y%m%d)` before `mkimage`; `config/options` then sources `distributions/ROCKNIX/version`, which assigns `OS_VERSION` unconditionally on both sides | `OS_VERSION="0.0.1"` in the version file; the export is overwritten here too | the documented export does nothing on either side | upstream's documentation defect; the fork's `CLAUDE.md` still says `mkimage` "needs OS_VERSION/BUILD_DATE exported" | T4: correct the `CLAUDE.md` sentence (only `BUILD_DATE` is honoured, and the fork defaults it) |
| 15 | `make update` (`scripts/update_packages`) moves the emulators, es-themes and gamesupport dependencies to their branch heads, honouring `config/blocklist`; LibreELEC's bump PRs reach `packages/` through the base merge | `tools/fork-package-freshness` checks the fork-introduced recipes against their authors' releases and `rc-preflight` makes a lag a finding; `make update` is present, never called, not documented | the upstream-carried emulator pins move only when the fork merges upstream; the fork has no check of its own on them | candidate: the maintainer's "package updates" covers both sets | T7 and T8: each slice's currency check names which mechanism moves each pin, and whether `make update` is run on the fork between base merges or the base merge is the only mover (the blocklist's 28 reasons are the input) |
| 16 | since the base, 22 ROCKNIX overrides deleted in favour of the generic LibreELEC recipes (#3415, #3470, #3513), `aethersx2-sa` dropped, `rocknix-abl` replaced by `openabl`, grub removed, 240 `package.mk` files changed | `next` carries all 22 and the `aethersx2-sa` blocklist line; `fork-package-freshness` counts them among its 46 "fork-introduced" recipes because they are absent upstream | the freshness tool's set is a diff, not a provenance: 22 of 46 are orphans, not the fork's packages | candidate (the tool's definition predates the deletions) | T8: separate "introduced here" from "deleted upstream" in the tool's set, by the merge base; the deletions themselves land with the next base merge (`release-candidates.md` step 0, `base: distribution`) |
| 17 | a PR touching `packages/**` fails outright; `AGENTS.md` puts recipes under `projects/ROCKNIX/packages` | 16 files added and 5 modified under `packages/` (webkitgtk, libsoup, linux, syslinux, installer, libyaml, libsamplerate) | none of those can go upstream where they are; the PR series (`docs/pr-series/map.txt`, #322) would be refused on the first bucket that includes them | candidate, with a release consequence | #645: move or re-home each before the series; T8 reads what remains under `projects/` |
| 18 | PRs need the `bugfix` label in a month's last seven days, merge through a merge queue, use the template (devices tested, artifacts, evidence, AI disclosure), and link `.img.gz` and `.tar` artifacts per device | `fork-workflow.md` states the commit-message rules and the one-commit-by-content recipe and nothing of the freeze, the queue, the template or the artifact links | a series cut after the 24th of a month, or without artifacts, is refused for reasons the rules do not mention | candidate (upstream's rules postdate the fork's) | #645 for the facts; T4 writes them into `fork-workflow.md` |
| 19 | `validate-pull-request.yml` and the freeze check run on `self-hosted`; all 19 upstream workflows are active on the fork's repository; the scheduled `Build` ends `startup_failure` daily (2026-10-19 to 10-22) | the fork edited the two PR checks to `ubuntu-24.04` and added four `fork-*` workflows; the inherited schedules are gated by repository name but the gate is evaluated after startup | a red run a day that means nothing, and inherited workflows nobody reads | candidate | T10: disable or gate the inherited scheduled workflows on the fork, or record why they stay |
| 20 | `fork record checks` is the fork's own CI | red since 2026-10-20 on `tools/box-check`: one open checkbox on #637 names the H700 without a physical fact | the ceremony's audited stage is doing its job; the tracker edit is owed | not a build-path difference; a tracker edit in the M7 lane | #637's lane: re-derive the checkbox against `docs/releases/device-facts.md` |
| 21 | releases by calendar from CI, notes generated, nightlies to SourceForge; a GH-runner build needs a classic PAT in the fork's secrets | nothing published from CI; a release plan prepared locally from exact bytes; no PAT exists; `rc-preflight` before any cut | different models by choice | deliberate (D-WORKFLOW-119/120, D-WORKFLOW-047, D-WORKFLOW-157/159; `fork-mirror-build-container.yml` header) | T10: keep; the fork CI's job is the record |
| 22 | the three scraper and achievements credentials come from repository secrets into the image job only; development builds lack them | from `~/.ROCKNIX/options` (0600) on the host; only those names cross `.env`; a runtime ScreenScraper path exists | the same outcome by a different route | deliberate (D-INFRA-006, D-WORKFLOW-166) | T5: keep |
| 23 | testing is building: CI builds every SoC, the template asks for device evidence, no test suite; `tools/pkgcheck` documented | the VM is the test bench (`vm-qa`, `vm-upgrade-rehearsal`, `frame-diff`), tool self-tests in CI, `pkgcheck` after every recipe edit | the fork tests what upstream only builds | deliberate (D-QA-007, D-QA-051) | T12: keep; the harness slice reads it first under D-WORKFLOW-186 |
| 24 | LibreELEC's `tools/update-scan`, `update-pkg`, `distro-tool`, `refresh-patches` are carried and unused by any ROCKNIX workflow | the same tools, unused | both carry dead tooling | candidate | T6: the reachability table decides (D-WORKFLOW-185's "unshipped is not dead" applies to devices, not to tools nothing calls) |
| 25 | EmulationStation from `ROCKNIX/emulationstation-next` as a tarball at a commit | from `pixelelated/emulationstation` branch `test/qa-integration` as a git clone; the `EMULATIONSTATION_SRC` mount documented as not building from the local tree | a fork of the interface, by design | deliberate (D-WORKFLOW-010/012; `device-builds.md` § Iterating on EmulationStation) | T32: the recipe slice |
| 26 | the contribute page's five steps name `dev`; the modify page names `Rockchip`, `RK3566-ML` and 2023 kernels; the guide says `release/` | the fork documents `target/`, `PROJECT=ROCKNIX`, `next` | upstream's site is behind its own tree in four places | upstream's documentation; a docs PR to `ROCKNIX/rocknix.org` is the fork's rule for user-facing drift, and this is contributor-facing | #585: a candidate documentation contribution, after the maintainer's deferral (D-WORKFLOW-165) |

## 5. What the coordinator verified

Run on 2026-10-23 in the coordinator's worktree, read-only: `git rev-list
--count next..upstream/next` is 315 with the base `c445081a59`; the Makefile
lines for the image pin on both sides; the fork-introduced set is 46
`package.mk` files and `opus`, `libfmt`, `strace`, `rocknix-abl` were deleted
upstream by the PRs named (`git log --diff-filter=D upstream/next`); the
`packages/` delta is 16 added and 5 modified, webkitgtk and libsoup among
them; upstream has 19 workflows and `trigger-fail-if-upstream-changed.yml`
exits 1 on `packages/**`; `fork-generic-x64.yml` has `if: ${{ false }}`;
`make update` exists on `next` and `config/blocklist` still names
`aethersx2-sa` (upstream's does not); `build_mt` and `clean` have no watch
guard and the other five do; `get_env`'s DROP pattern is as reported; no
rule or entry file mentions the freeze period, the merge queue or the AI
disclosure; on GitHub, `Build` ended `startup_failure` on each of
2026-10-19 to 10-22 and `fork record checks` failed on 2026-10-20 to 10-22
at the checkbox step on #637. Not verified: the site-repository edit dates,
the registry `created` timestamps, and the counts of changed `package.mk`
files, which are the subagent's reads.

## 6. For the maintainer

Two findings want a call; both are queued behind #641's gate questions and
are not put until those are answered.

1. **Finding 17.** Upstream refuses any PR that touches `packages/`. The
   fork's webkitgtk, libsoup and the other 19 files there cannot go upstream
   where they are. Recommendation: move them under `projects/ROCKNIX/packages`
   before the upstream series, as upstream's `AGENTS.md` directs (#645).
2. **Finding 16.** Upstream has retired 22 of the overrides the fork still
   builds. Recommendation: let the next base merge (release-candidates step 0)
   take upstream's deletions rather than keep them, and have the package
   slices read what remains; the freshness tool's set is corrected by the
   merge base so it stops counting orphans as the fork's packages.

Everything else in § 4 is carried by a slice and needs no call now.

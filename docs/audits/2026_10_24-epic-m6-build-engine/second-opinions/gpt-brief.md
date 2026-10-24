# Second opinion on a code audit -- M6.P2 T5, the build engine, epic tier

You are the second reader of a code audit. You cannot run commands or open
the repository; everything you may cite is in the packet below, and every
claim you make names the packet's `file:line` or the command output it rests
on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 242 paths of a handheld Linux distribution's build engine (a
LibreELEC/ROCKNIX fork): the build scripts under `scripts/`, `config/` (the
shared shell helpers `config/functions`, the options, 139 system fragments),
`distributions/ROCKNIX/`, the `Makefile` and `Dockerfile`, and 19 upstream
GitHub workflows, read at one commit. Nothing was built: claims about
behaviour are proven by sandboxed calls of the functions with scratch
variables, by the install trees and logs of builds another lane ran, or are
marked as needing a build. The first reader is Claude Opus 5.5 (Anthropic);
you are a reviewer from another lab. The audit is a renovation: besides
defects, its findings answer seven questions (Q1 modernize, Q2 standards, Q3
bugs, Q4 package currency, Q5 efficiency, Q6 dead ends, Q7 clarity).

Answer in three parts, in this order:

1. **Your own findings first.** Read the packet's evidence -- the code
   excerpts at the end, the checks, the proofs -- and list every defect,
   gap, or unsafe seam you find that is not already one of the first
   reader's findings. One line each: an id (G-01, G-02, ...), a severity
   (Critical / High / Medium / Low), the packet's `file:line`, what fails
   and when.
2. **Refute the first reader.** For every finding at Medium or above (High:
   F-16, F-18; Medium: F-01, F-02, F-03, F-04, F-09, F-17, F-19, F-20) and
   any Low you think mis-graded: agree, disagree, re-grade, or narrow -- and
   in each case say what would make the finding false and whether the
   packet shows it. Say whether F-16 and F-18 are really High, and whether
   any Low should be higher.
3. **What you could not judge.** The claims the packet does not let you
   verify, so the orchestrator knows where its evidence was thin.

Everyday words, no hedging: a finding either survives your reading or it
does not, and you say which.

---


# Packet file: `02-forward-audit.md`

# Forward Audit — M6.P2 T5, the build engine

**Auditor:** Code Auditor skill (v1.13.0), primary Claude Opus 5.5 at high effort
**Date:** 2026-10-24
**Subject:** #652 (`M6.P2 E800/T5`), slice `build-engine`; read at `reviewed-at: 46f6c7d428`, the slice's bytes equal to `next`'s `8ebaf8daad`
**Spec:** `docs/reviews/briefs/build-engine.md` version 2; #652's checklist (= brief § 7)

---

## Running Notes

Findings are numbered `F-NN` in the order they are written; each names its question (Q1 to Q7), its unit and its evidence. Severity and category are set in `04` and `05`. Every proof (a sandboxed call, a recorded-run or install-tree reading) is written once under § Proofs with its cell, and announced in `00-running-log.md` on a `PROOF:` line (criterion 12). Line numbers are `8ebaf8daad`'s. Every log or config line read here went through the `readlog` filter of brief § 5; no build command line and no `.env` content is reproduced.

**The VM question, for the slice (brief § 5):** *Can this be done on the VM?* **No, for what the engine does:** it runs on the build host or in the build container, and a guest has nothing to show about it; the evidence is the sandbox (a function or script run with every variable pointed at a scratch directory, the `bash -x` trace read first) and the M7 lane's recorded runs and install trees, read-only. **Yes, for what the engine writes into an image** (the identity in `/etc/os-release`, the launch table): read from the M7 build roots' install trees first; no finding so far needs a running guest, so this lane has started none.

## Mechanical checks (brief § 5)

| Check | When (UTC) | Command | Exit | Summary |
| --- | --- | --- | ---: | --- |
| `bash -n` | 03:58 | the brief's loop over the 26 shell scripts (the 30 less the 4 Python) and the 15 sourced fragments, `ok`/`FAIL` per file into `.qa-scratch/t5/bash-n.out` | 0 | **41 ok, 0 FAIL**: scripts 26, fragments 15. The brief's `uniq -c` prints one count when nothing fails; the two counts come from `grep -c ' scripts/'` and its complement |
| `python3 -I -m py_compile` | 03:58 | `scripts/pkgbuilder.py`, `genbuildplan.py`, `uboot_helper`, `test-audit-review.py`, `config/docker/source/default.py` | 0 each | 5 ok. It wrote `__pycache__/` beside the sources (gitignored); removed at 03:58, `git status` clean |
| `tools/build-identity-test` | 03:58 | `python3 -I tools/build-identity-test --output .qa-scratch/t5/build-identity-test-20261024T035837Z.json` | 1 | **`FAIL build identity: 21 passed, 2 failed`**, exactly the expected result of #801: the two failures are `rc1 public plan accepted` and `harness completed`, both `release preparation: selected-state inspection refused a firmware asset` (the release-plan half, T14's or T9's). The 21 passes are this slice's identity evidence: `engineering default dev`; ten rejected qualifiers (`alpha.1`, `beta.1`, `rc`, `rc.0`, `rc.01`, `rc.-1`, `rc.1.2`, `rc.1+extra`, `stable`, `bad/`); five rejected overrides (`OS_VERSION=01.0.1`, an invalid `BUILD_TIMESTAMP`, `CUSTOM_VERSION`, `CUSTOM_IMAGE_NAME`, a mismatched `CUSTOM_GIT_HASH`); `dirty build identified`; `rc1 one sidecar`; `rc1 actual filename and sidecar`; `rc1 installed metadata contract`; `rc1 duplicate output refused without replacement`. The JSON says `synthetic_only: true`, `assembled_image_tested: false` |
| `tools/host-maintenance/test-build-monitor` | 03:58 to 03:59 | `python3 -I tools/host-maintenance/test-build-monitor`; read first: it runs the real entry-point prefixes and the Makefile against stub payloads and a stub `docker` inside `tempfile.TemporaryDirectory(prefix='watch-build-394-')`, no compiler, no container | 0 | **`36 PASS; 0 FAIL`** (T9's tool; a trial that it runs here) |
| `tools/fork-package-freshness --list` | 03:59 | `tools/fork-package-freshness --list` | 0 | 47 lines, every one a `packages/` or `projects/` recipe; `grep -c -E '^(scripts|config|distributions/ROCKNIX)/'` 0: **the engine introduces no package**, and nothing of this slice is in the tool's set |
| `tools/pkgcheck rocknix` | 03:59 | `tools/pkgcheck rocknix` | 0 | no finding printed (only the tool's progress line for `projects/ROCKNIX/packages/rocknix/package.mk`); the trial that the tool runs from this tree. The engine changes no recipe |
| shellcheck v0.11.0 | 04:01 | downloaded into `.qa-scratch/t5-shellcheck-dl/` (own empty directory), `sha256sum -c` against the release's published digest `8c3be12b05d5c177a04c29e3c78ce89ac86f1595681cab149b65b97c4e227198` (`gh api repos/koalaman/shellcheck/releases/tags/v0.11.0`, the asset's `digest`): OK; extracted to `.qa-scratch/t5-shellcheck/`, run by path; `shellcheck -f gcc` with the file's shebang, `-s bash` where there is none, over the 26 shell scripts and the 15 sourced fragments | 1 on 38 files, 0 on 3 | **5 errors, 271 warnings, 788 notes.** Each error read at its site: § shellcheck errors below. Warnings by code: SC2034 150 (variables assigned in a sourced options file and read by other scripts: noise in a fragment), SC2166 32 (`-a`/`-o` in `[`), SC1090 22 (non-constant `source`), SC2164 13 (`cd` without `|| exit`), SC2155 10, SC2044 7, SC2069 6, SC2046 6, SC1007 6, the rest under 5. The fork-own files' warnings are listed in § shellcheck, fork-own lines |
| The `Makefile`'s recipes | — | not shellcheck's input; read (§ The Makefile and `.env`) | — | — |
| `actionlint` | — | not on the host; the 19 workflows read, and their state from `gh` (below) | — | — |
| The container manifests | 04:08 | `docker manifest inspect` (and `-v`) of `ghcr.io/pixelelated/build@sha256:988c0ba5…` and `ghcr.io/rocknix/rocknix-build:latest`; the two config blobs through GHCR's anonymous token flow (`https://ghcr.io/token?scope=repository:<repo>:pull`, then `GET /v2/<repo>/blobs/<config digest>`, 5,778 and 5,777 bytes; no layer fetched, **no `docker pull`**) | 0 | pin `sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`, linux/amd64, config `sha256:9783cb20…`, **created 2026-09-25T03:09:54Z**; upstream `latest` answers **`sha256:67e1fd0adbcfe71cc524ef49941242853f3daa7f1eecea74ec765b9b6d24973d`**, linux/amd64, config `sha256:3acf6ac8…`, **created 2026-10-24T03:03:03Z** (the coordinator's read earlier on 2026-10-24 answered `sha256:a81b63a53612…`: upstream rebuilt it since). Both single-platform v2 manifests of 12 layers, label `org.opencontainers.image.version: 22.04`; 10 of the 12 layer `diff_ids` differ; `git diff upstream/next 8ebaf8daad -- Dockerfile` empty. Q4 (b) in `04` |
| The 19 workflows | 04:08 | `gh workflow list --repo pixelelated/distribution --all`; `gh run list --workflow <file> --limit 3` per file; triggers, repository gates, secrets and runners read from each file | 0 | all 18 `.yml` **active**; `ai-usage.yml.disabled` is not a workflow to GitHub. Runs on the fork: `build-nightly.yml` (`Build`) `startup_failure` on 2026-10-22, 23, 24 (schedule); `update-kernel-configs-docs.yml` **`failure` on 2026-09-04, 09-19, 09-28 (push)**; `update-mirror-sources.yml` `skipped` on 10-04, 10-12, 10-18 (its repository gate); every other one never ran. Table in `04` Q6 |
| `.env` at rest | 04:11-04:31 | `test -e <checkout>/.env` over all 134 checkouts (the legacy primary, every `rocknix.worktrees/*`, the fresh primary, every `distribution.worktrees/*`); a hit would be reported by path, size and mode only | 0 | **none found** |
| `tools/vm-qa`'s suites | — | none is this slice's (the engine writes no surface a suite reads beyond the identity, which `tools/build-identity-test` covers); the runner not run | — | — |

### shellcheck errors, read at their sites

- `config/functions:1204` SC1072/SC1073 (one site, two codes): `[ $test_func "$dir/$search" ]` in `find_path`, where `$test_func` is the caller's test operator (`-f`, `-d`). **Intended**, a dynamic unary test shellcheck cannot parse; not a finding.
- `config/multithread:50` and `scripts/build_mt:16` SC2068: `${@}` unquoted where package names are passed through. Package names carry no spaces (`tools/pkgcheck`'s naming); an upstream idiom; Q1 note in `04`, not a defect.
- `scripts/unpack:90` SC2144: `[ -z "${PKG_SOURCE_DIR}" -a -d "${PKG_UNPACK_DIR}/${PKG_NAME}-${PKG_VERSION}"* ]`. **A real defect, F-08**, proven by its sandbox (P8).

### shellcheck, fork-own lines

`scripts/build` 26 warnings (SC2166 at 55, 114, 121, 143, 257, 295, 579, 616; SC2044 `for ... in $(find ...)` at 545 to 557; SC2046 at 244, 600, 608, 610; SC2164 at 255, 271, 620; SC2155 at 285, 291; SC2115 at 589; SC2045 at 23; SC1090 at 52). Every one of these lines is upstream's (`git blame` names the fork only on lines 7 to 12, 185 to 188, 196 and 227 (`git diff -U0 upstream/next 8ebaf8daad -- scripts/build`: the watch entry, the wrap-mode comment and the two flags, +12)). `scripts/image` 12, of which the fork's are **SC2034 `ORIGIN_URL` at 72 (F-06)** and SC2164 at 307 and 323 in upstream's lines. `scripts/build_compat` SC2034 `GIT_HASH` 59 and `ORIGIN_URL` 63 (F-07). `scripts/install` SC2166 at 164, `scripts/build_distro` SC1090 at 25, `config/show_config` SC1090 at 148 (upstream's lines). `distributions/ROCKNIX/options` 63 SC2034 (an options file: every assignment is read elsewhere; noise).

## Phase 1 reading, summarised (detail in `01` § Phase 1)

2 closed `bug` issues of 139 name an engine file by the brief's pattern (#226, #413); 3 prior audit folders' punch lists name the engine (2026-09-13 1 line, 2026-09-24 6, 2026-09-25 9); upstream's trackers read at 03:57 UTC.

## Findings, written as each unit is read

### F-01 (Q3, Q2; security): `scripts/get_env`'s DROP lets six constructed secret-shaped names through

`scripts/get_env` 14 to 21 forwards every exported variable but `PATH` into `.env` unless its name matches `DROP` and not `KEEP`. `DROP` (line 15) is case-sensitive and needs an underscore or the string's start before the word: `(^|_)(KEY|KEYS|TOKEN|TOKENS|SECRET|SECRETS|PASSWORD|PASSWD|CREDENTIAL|CREDENTIALS|AUTH|APIKEY|API_KEY|PRIVATE)($|_)` or a prefix `AWS_`, `GH_`, `GITHUB_`, `NPM_`, `OPENAI_`, `ANTHROPIC_`. The sandbox (P1) built a fixture environment with `env -i`, the names assembled at run time and the values the words `fixture-N`: dropped as designed `MY_API_KEY`, `GH_PAT`, `LOCAL_WIFI_KEY`, `LOCAL_SSH_KEYS_FILE` (#644 finding 3's two guide variables both dropped); kept as designed `SCREENSCRAPER_DEV_LOGIN`, `PROJECT`, `DEVICE`, `ARCH`; **kept although secret-shaped: `DB_PASS`, `SSHPASS`, `DOCKERHUBTOKEN`, `github_token`, `MY_PASSPHRASE`, `SESSION_COOKIE`.** The script's own comment (5 to 13) promises only names, and names "that look like" a secret; these six look like one to `.githooks/secret-patterns`' authors and to `engineering-practices.md`'s read filter (`key|pass|token|user|psk`, case-insensitive), not to `DROP`. The fix's shape (case-insensitive, `PASS`/`PASSPHRASE`/`COOKIE`/`SESSION` words, the boundary relaxed for `TOKEN`/`KEY` suffixes) changes what reaches the container: a stream brief's, `fix-pending-image` for its proof on a build (a variable a build needs being dropped is the risk). D-INFRA-006.

### F-02 (Q3; security): a value with a newline writes extra lines into `.env`, and a bare-name line imports the host's value of that name

`echo "$var=${!var}"` (`get_env` 21) writes a multi-line value as several lines. The Makefile hands `.env` to `docker run --env-file .env` (`Makefile` 208). The sandbox (P1) exported `MULTILINE` whose value's second line is the bare name `OTHER_TOKEN`: `.env` carries `MULTILINE=fixture-a` and then a line `OTHER_TOKEN` with no `=`. Docker's documented `--env-file` behaviour takes a name without `=` from the invoking environment, so **a name `DROP` removed comes back through a neighbour's value**. Any `NAME=value` line in a value likewise sets or overrides a container variable (`PROJECT`, `DEVICE`, `ARCH` are passed after with `-e`, so they win; the rest do not). Not run against docker (a `docker run` is outside this slice, brief § 5); the `.env` line is the sandbox's artifact, the import is docker's documentation. Fix shape: skip (or refuse) a value containing a newline; `fix-pending-image`.

### F-03 (Q3): `add_es_system` carries a system's fragment variables into the next system; two shipped systems carry the wrong release year

`distributions/ROCKNIX/config/functions` 127 to 142 sources `config/emulators/<system>.conf` into the calling shell and sets `SYSTEM_COMMAND` only `if [[ -z "${SYSTEM_COMMAND}" ]]`; nothing unsets a `SYSTEM_*` variable between calls, and the metapackage calls `add_es_system` 128 times in one shell (`virtual/emulators/package.mk`). **Shipped:** `daphne` and `gp32` have no `SYSTEM_RELEASE` (brief § 2), and both read `release="1996"` in the GENERIC_X64 (`069fc2704421`) and H700 (`m7-signin-h700-build-20261023-06`) install trees (P7): `1996` is `cps3`'s and `palm`'s, the systems registered just before them (`package.mk` 358 and 1686). **Latent:** `SYSTEM_COMMAND` carries over the same way; it is harmless today only because the three fragments that set it (`moonlight`, `tools`, `imageviewer`) are registered last (`package.mk` 1717 to 1723). The sandbox's case C (P6) registers a fixture system after `imageviewer` with a fragment that sets neither: it ships `command=/usr/bin/true` (the screenshot viewer's) and `release=System`, rc 0, nothing printed. So the next system upstream or the fork appends launches nothing. `arcade` and `segamodel3` lack `SYSTEM_WIKI_PATH`, which feeds only the document; the same carry-over applies there. Fix shape: unset the ten keys at the top of `add_es_system`, and give `daphne` and `gp32` their years; it changes two shipped `<release>` lines, so `fix-pending-image` with T3's regeneration as its sandbox. Upstream's code (#585 candidate).

### F-04 (Q3, Q7): T3's F-06 confirmed: the "one default" rule fails a build silently on one shape and ships two defaults on the other

`functions` 209 to 215 marks `default="true"` on every `cores/core` of the emulator so far, not the core just added; `mk_es_systems` (113) runs `xmlstarlet fo` with `2>/dev/null`. T3's two cases rerun here (P4, P5): **case A** (two `true` lines for `3do`) leaves `<core default="true" default="true">opera</core>` in `3do.tmp`, `ElementTree` refuses the pre-format table (`duplicate attribute: line 17, column 29`), `fo` exits 2 and the formatted `es_systems.cfg` is **left at 0 bytes**; under `set -e` the recipe stops with rc 2 and **no message** (the run's only non-trace output is unrelated). **Case B** (`first_false false` before `b2 true` for `bbcmicro`): rc 0, the pre-format table parses (128 systems), and `bbcmicro` ships `[('first_false', 'true'), ('b2', 'true')]`, two defaults. Today no device's table has either shape (T3's five tables). Fix shape: `.../cores/core[last()]` in the default step, and `fo`'s stderr kept (or its failure named) in `mk_es_systems`. The second is a build's diagnostics only; the first changes no shipped table today (T3's tables have every `true` first) and is proven by the regeneration being byte-identical before and after: `fix-sandbox` candidates. Upstream's code (#585).

### F-05 (Q7; doctrine): `device-builds.md` § After rebasing, item 3 says the generic recipe is never hashed; the engine has hashed it since 2026-08-20

The rule: *"`calculate_stamp` (`config/functions`) hashes `$PKG_DIR`, which resolves to the **override** directory. The generic file holding the version is never hashed, so bumping it does not invalidate the stamp."* `config/functions` 1109 to 1129 adds `get_global_pkg_directory "${PKG_NAME}"` (1098 to 1107) to the hashed paths, with a comment saying exactly why (`cb884edb0f`, 2026-08-20, *config/functions: hash the global recipe a project package sources*); upstream carries it (`git grep -c get_global_pkg_directory c445081a59 -- config/functions` 2; present at `upstream/next` 1100 and 1123). The sandbox (P2): a fixture override sourcing its generic twin; the stamp `588f5f64…` moves to `062579ba…` when the generic `PKG_VERSION` goes from 1.0 to 1.1, and with `get_global_pkg_directory` stubbed out (the pre-fix shape) a further bump does not move it. **The engine's behaviour is right; the rule's sentence is stale**, and the brief's Q3 cell inherited it (*"a defect in the engine, or a documented limit"*: neither). **The same section's item 2 is stale in the same way:** it prescribes deleting `libtoolize` from a warm root before a libtool bump, and `config/functions` 954 to 962 no longer exports a previously installed `libtoolize` while building libtool itself (`5ce3dcc9d7`, 2026-08-20); both fixes went upstream together as ROCKNIX PR #3213 (`02c9dd740e`, 2026-08-21). The rule edit is doctrine (T4's carrier, `device-builds.md`); deferred there.

### F-06 (Q6, Q7): `scripts/image` computes `ORIGIN_URL` for consumers that do not exist; `BUILD_FILENAME` is written and read by nothing

`scripts/image` 71 to 72: *"Keep source provenance available to the existing image metadata consumers."* `ORIGIN_URL` is assigned, not exported, and read nowhere (`git grep -n ORIGIN_URL -- scripts config distributions projects packages`: the two assignments in `scripts/image` and `scripts/build_compat` only; shellcheck SC2034). The comment names a consumer that does not exist (blindspot 46's shape). `${BUILD}/BUILD_FILENAME` (`scripts/image` 84, `build_compat` 82) is written and read by nothing in this tree, the workflows or `tools/` (`git grep -n -F BUILD_FILENAME`), and upstream likewise (`git grep -c -F BUILD_FILENAME upstream/next`: the same two writers). Removal candidates with their `Already written:` (a `BUILD_FILENAME` file in every build root; nothing reads it).

### F-07 (Q7, Q6): `scripts/build_compat` still carries the identity logic `config/build-identity` replaced in `scripts/image`

`scripts/build_compat` 56 to 80 (fork-own since `f6010e7b77`; the watch entry `1aac875e88`) computes `GIT_HASH` and `ORIGIN_URL` (both unused, SC2034), honours `CUSTOM_VERSION` and `CUSTOM_IMAGE_NAME` (which `pixelelated_build_identity` refuses: `config/build-identity` 21 to 23, and the identity test's two rejected overrides), and names the compatibility root's `IMAGE_NAME` from `OS_VERSION`, written to `BUILD_FILENAME` only (F-06). Nothing of it reaches an image or a name a reader sees. Its `ORIGIN_URL` sed also lacks the `s#://.*@#://#` that strips a credential from a remote URL (`scripts/image` 72 has it); harmless while the value is unused. Removal or alignment with `config/build-identity`; `Already written:` nothing read.

### F-08 (Q3; upstream's): `scripts/unpack` 90 silently empties a package whose unpack directory holds two `name-version*` entries

`[ -z "${PKG_SOURCE_DIR}" -a -d "${PKG_UNPACK_DIR}/${PKG_NAME}-${PKG_VERSION}"* ]`: the glob is expanded into `[`'s arguments. The sandbox (P8), the line lifted verbatim over a fixture: one match, the test is true; **two matches (`fixturepkg-1.0` and `fixturepkg-1.0-extra`), `[` prints `too many arguments`, returns 2, and nothing is moved**. `unpack` 94 to 116 then creates an empty `.intermediate` and moves it to `PKG_BUILD`: the package builds from an empty directory and fails later with an error that names nothing of the cause. A tarball that unpacks into two such directories is rare; no recorded run shows one. LibreELEC's code (`config/functions`' header), carried unchanged; Low, `Renovation` and #585.

### F-09 (Q3, interaction): `scripts/build_distro` prunes the device's earlier outputs before `scripts/image`, so the image step's refusal of an existing identity never fires on a device build

`scripts/build_distro` 82 to 84 (`set -e`, line 15): `rm -f ./release/${DISTRONAME}-${DEVICE}.${ARCH}-*` and `rm -rf ./target/${DISTRONAME}-${DEVICE}.${ARCH}-*` (`rm -rf` since `c2bb7ec0b9`, 2026-07-01, for the GENERIC_X64 image directory; the prune itself since `2c6aa73553`, 2025-07-23). Then `make image` (the `case` at 89 to 101) runs `scripts/image`, whose refusal (78 to 82, `f10eec1306`, 2026-10-09: *"A frozen timestamp is shared by device builds, never reused to replace bytes"*) looks for `${TARGET_IMG}/${IMAGE_NAME}.*` and `-*`: the prune has just removed every such file of this device. So on the documented route (`make <DEVICE>`, `make docker-<DEVICE>`) a rebuild with a frozen `BUILD_TIMESTAMP` (`docs/releases/versioning.md` 20 to 23: a coordinated set shares one) **replaces the bytes of an existing identity** in `target/` without a word. The refusal fires only when `scripts/image` is run directly (the modify page's route) and in `tools/build-identity-test`'s `rc1 duplicate output refused without replacement`, which calls the image blocks, not `build_distro`. The prune also deletes every earlier image of the device in that worktree's `target/` (by design since 2025: *"Clean previous device release when doing a new build"*); the three M7 `target/` directories read (`m7-pixelelated-h700-03`, `m7-signin-h700-build-20261023-06`, `m7-signin-build-20261022-07`) each hold exactly one identity per device, consistent with it. Candidates live in the immutable store, not `target/` (`release-candidates.md`, `tools/rasteratops-candidate-store`), so the bytes lost are a worktree's, but the identity guarantee is weaker than D-WORKFLOW-157's text. A trace with file:line; no build was run to show it. Fix shape (a stream brief's): refuse in `build_distro` when `BUILD_TIMESTAMP` is set and a matching identity exists, before the prune, or prune only names of a different timestamp; `fix-pending-image`.

### F-10 (Q6; with T10): `update-kernel-configs-docs.yml` runs on the fork and fails on every push that touches the linux recipe

The workflow's `push` trigger (`branches: next`, `paths: projects/ROCKNIX/packages/linux/package.mk`) has no repository gate, and its jobs need `NIGHTLY_APP_ID` and `NIGHTLY_APP_PRIVATE_KEY`, which the fork does not hold. `gh run list --workflow update-kernel-configs-docs.yml --limit 3`: `failure` on 2026-09-04, 09-19 and 09-28 (push). #644's finding 19 names `Build`'s daily `startup_failure` and not this one. The fork's CI gates are T10's (#644 finding 19's carrier); recorded here as the row of Table 4 and a lead for T10, not changed (a workflow trigger is never edited here, brief § 5).

### F-11 (Q4): the build container's pin is 29 days older than upstream's current image (#644 finding 1)

Q4 (b) in `04`. The pin `988c0ba5…` (`Makefile` 138; `2c349c6d51`, `440ad22b68`) was created 2026-09-25T03:09:54Z; upstream's `latest` was rebuilt today, `67e1fd0a…` created 2026-10-24T03:03:03Z, from the identical `Dockerfile`; 10 of 12 layers differ (Ubuntu 22.04 package updates). The refresh is the coordinator's act (`fork-mirror-build-container.yml` then the Makefile line): `to merge`, recorded with both digests.

### F-12 (Q4): three membership files are behind upstream by upstream's own commits

`git diff upstream/next 8ebaf8daad` on the membership names 21 files (`04` Q4 (a)); 18 differ by the fork's commits, and three only by upstream's since the base: `config/blocklist` (`c4d353449e`: upstream removed `aethersx2-sa # package is EOL` when it dropped the package for licensing; T3's F-07 carries the package itself), `.github/workflows/build-nightly.yml` (`76693a738d`: `GH_TOKEN` passed to two release steps) and `.github/pull_request_template.md` (`c200cc906d`: the new template with the AI-assistance disclosure, #644 finding 18). All three land with the next base merge (`to merge`); none is the fork's to edit separately.

### F-13 (Q2, Q7): the `Makefile`'s Docker recipe mounts `~/.ROCKNIX/options` writable, and builds a local container no target runs

`Makefile` 147: `-v "${HOME}/.ROCKNIX/options:${HOME}/.ROCKNIX/options"`, no `:ro`; the build inside the container runs as the invoking user (`--user $(UID):$(GID)`, 208) and can rewrite the credentials file it only needs to read (D-INFRA-006's file, mode 0600). Nothing in the tree writes it, so this is hardening, not a defect. `DOCKER_IMAGE_LOCAL` (140) is what `docker-image-build` (186 to 188) tags, and no target runs it: `docker-%` always runs the pinned digest (139, 208), so a contributor who follows upstream's guide (`make docker-image-build`, then `make docker-<SOC>`) builds with the pin, not the container they just built. The Makefile's comment (131 to 137) says so in one clause (*"A locally built container is tagged (DOCKER_IMAGE_LOCAL), never pinned"*); a reader of the guide is not told. Q7, documentation.

### F-14 (Q1): `scripts/build_distro`'s exit-status check after `make image` is dead under `set -e`

`build_distro` 15 sets `set -e`; the `case` at 89 to 101 runs `scripts/build_compat`/`scripts/install` or `make image`, and 103 to 106 then test `if [ $? -ne 0 ]`: a failing command has already ended the script, and after the `case` `$?` is the `case`'s own 0. Upstream's lines; `Renovation`, Low.

### F-15 (Q7, Q2): two options files a letter's case apart: the scripts read `~/.rocknix/options`, the `Makefile` and every rule name `~/.ROCKNIX/options`

`config/options` 132 to 140 sources `${ROOT}/.rocknix/options` and `${HOME}/.rocknix/options` (lower case; upstream's lines since `30e2f56f1c`, identical at `upstream/next` 133 to 139). The `Makefile` includes `$(HOME)/.ROCKNIX/options` (line 1) and mounts it into the container (147); `device-builds.md` § Build credentials (536), D-INFRA-006 and `scripts/get_env`'s comment (13) all name the upper-case file. On this host the upper-case file exists (mode 600, by `test -f` and `stat -c %a` only) and the lower-case one does not. So a build entered through `make` (native or Docker) gets the credentials (the include exports them, `get_env`'s `KEEP` carries them into `.env`), and a script run directly from a shell, the native route `CLAUDE.md` documents (`./scripts/build <package>`), reads only the lower-case file and builds EmulationStation without them, silently (the runtime ScreenScraper path covers one of the four, #64). Upstream ships the same split. No fork document mentions the lower-case file. Q7 documentation (a sentence in `device-builds.md` § Build credentials, T4's) or Q2 alignment (one path), the stream brief's.

### The upstream core: a research subagent's read, and what was re-read

The 23 upstream-carried core files were read whole by one read-only research subagent (dispatched after 04:11:41, returned before 04:31:01 UTC, 8 m 41 s; D-WORKFLOW-183's fan-out), which returned 28 ranked leads, an inventory of `config/functions`' sections and the `set -e` status of each script. It reported these files byte-identical to `upstream/next`: `config/functions`, `options`, `path`, `optimize`, `multithread`, `scripts/mkimage`, `unpack`, `get`, `get_git`, `get_archive`, `pkgbuild`, `clean`, `build_mt`, `checkdeps`, `autoreconf` (the Q4 (a) diff agrees: none is among the 21 that differ). **Every lead below was re-read at its site by this auditor before it became a finding;** the ones not re-read are listed as leads at the end of this section.

### F-16 (Q3, Q2): `scripts/mkimage` reports success over an incomplete `qcom-abl` or `arm-efi` image, the Retroid Pocket Nova's route

`scripts/mkimage` runs without `set -e` (it sources no `config/options`; `grep -n 'set -e'` empty) and guards its steps one by one with `>"${SAVE_ERROR}" 2>&1 || show_error`: every `mcopy` of the `syslinux`, `u-boot` and Raspberry Pi branches does (173 to 176, 194 to 197, 234 to 237, 292 to 293). **The `arm-efi` branch (252 to 255) and the `qcom-abl` branch (270 to 273) copy the kernel, `SYSTEM` and their `.md5` with no check**; `pigz --best --force "${DISK}"` (324) is unchecked; the `parted` calls (65, 76 to 82) are unchecked; and the script ends `cleanup` then a bare `exit` (333 to 334), whose status is `cleanup`'s `rm -rf` (0). `scripts/image` calls it through `do_mkimage` (56, 337) under `set -e` and so trusts its 0. `BOOTLOADER="qcom-abl"` is SM8550's (`projects/ROCKNIX/devices/SM8550/options` 34), the Nova, a test device (`device-builds.md` § Our devices). So an SM8550 image whose `SYSTEM` did not fit the FAT partition, or whose compression failed for a full disk, is written, checksummed (326 to 329) and reported built. Read at the site; no build was run to show it (a FAIL needs a full `SYSTEM`); a sandbox of the branch needs `mtools` and the image's files, so `fix-pending-image`. Upstream's (LibreELEC's structure, ROCKNIX's `qcom-abl` branch); #585 candidate. The project's own `projects/ROCKNIX/bootloader/mkimage` (the subagent's lead, `mkimage_abl` around 77 to 110) is T8's or the device slice's path, named here as a lead.

### F-17 (Q3): a device-level file that `find_file_path` reads is outside the stamp, so changing it rebuilds nothing

`find_path` (`config/functions` 1188 to 1191) searches `devices/$DEVICE/packages/$PKG_NAME`, then **`devices/$DEVICE`** and the project root; `calculate_stamp` (1109 to 1129) hashes `PKG_DIR`, the project's and the device's `patches/$PKG_NAME`, `PKG_NEED_UNPACK` and the generic recipe, not `devices/$DEVICE/config/`. `kernel-firmware` reads `config/kernel-firmware.dat` through `find_file_path` (`projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk` 39) and its `PKG_NEED_UNPACK` (10) names only the two `packages/` directories; eight devices carry the file (`projects/ROCKNIX/devices/{AMD64,H700,SM4450,SM6115,SM8250,SM8550,SM8650,SM8750}/config/kernel-firmware.dat`). The sandbox (P12): a fixture package with that recipe's `PKG_NEED_UNPACK`, `find_file_path` resolving the device file, the list extended, **the stamp unchanged** (`a20ed10a…` both). So an edit to a device's firmware list ships the old firmware set until someone cleans the package by hand; nothing says so. No fork commit has edited those files since the base (`git log c445081a59..8ebaf8daad -- 'projects/ROCKNIX/devices/*/config/'` empty). Fix shape: the recipe lists the device file in `PKG_NEED_UNPACK` (T8's), or `calculate_stamp` hashes what `find_file_path` found (the engine's; every package's stamp could move, a build's to prove). Upstream's.

### F-18 (Q3): `scripts/get_git` accepts a cached clone whose `HEAD` is not `PKG_VERSION`

`_repo_exists_and_valid` (`get_git` 30 to 52) checks `git ls-remote . | grep -q -m1 "^${PKG_VERSION}"` (36): **any** ref of the cached clone, not `HEAD`, and `main` then does `_repo_exists_and_valid && exit 0` (198) without a checkout. The fresh-clone path checks `HEAD` correctly (212 to 218). The sandbox (P13): a fixture clone reset to an older commit B while its `refs/remotes/origin/main` is A; with `PKG_VERSION=A` the cache is **accepted** and `HEAD` stays B. So when a recipe's pin moves to a commit its cached clone already knows as a remote branch tip (a pin bumped to the branch's tip as it was at the last clone), the package rebuilds (its stamp moved) **from the old source**, and the image carries a version it does not contain. The shared source cache (`device-builds.md` § The build command) keeps clones for months, which widens the window. Fix: compare `git rev-parse HEAD` with `PKG_VERSION` (`fix-sandbox` by the same fixture; the change alters what a build fetches, so its stream brief names the build). Upstream's; #585 candidate.

### F-19 (Q3; security): archives are fetched without TLS verification and accepted unhashed when a recipe has no `PKG_SHA256`

`scripts/get_archive` 25: `wget ... --no-check-certificate ...`; 45: `[ -z "${PKG_SHA256}" -o "${PKG_SHA256}" = "${CALC_SHA256}" ] && break 2`. A recipe without `PKG_SHA256` therefore takes whatever an unverified TLS peer serves, from `PKG_URL` or `DISTRO_MIRROR` (33 to 35). `_get_file_already_downloaded` (4 to 7) compares the stamp file with `PKG_SHA256`, not the archive's bytes. And `scripts/update_packages` 50 to 52 deletes a recipe's `PKG_SHA256` line before 61's `sed` looks for a `PKG_SHA256=""` line after `PKG_VERSION` to fill, which is gone, so every archive recipe `make update` bumps loses its checksum (latent on the fork: `make update` is never run, Table 1). How many recipes the image builds lack a checksum is the package slices' count (T7, T8). Upstream's; Medium.

### F-20 (Q2): `scripts/checkdeps` changes the build host on every entry: the default compiler and `/nix`

`checkdeps` runs at every entry point (Table 1). On Debian or Ubuntu with `gcc-12` present it runs `sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100 ...` and `--set gcc` (296 to 309, ROCKNIX's `8d0793be5f`, 2026-05-10): the host's system-wide default compiler changes, unasked. `prepare_nix_dir` (324 to 343) runs unconditionally (345) and, without a writable `/nix`, runs `sudo mkdir -p /nix` and `sudo chown "$(whoami)" /nix` (`214b17f900`, 2026-02-24, for FEX-emu): a prompt in the middle of a native build, or a stop under `set -e` without `sudo`. On this host `gcc-12` is absent and `/nix` is absent (`command -v`, `test -d`), so a native build here meets the `/nix` step; Docker builds meet it inside the container. Read at the site; nothing was run. A host change belongs to the person who owns the host (the spirit of D-QA-015 for the build box); fix shape: report and stop, or do it only behind an explicit opt-in. Upstream's (ROCKNIX's); Medium.

### F-21 (Q1, Q7; Low): small defects in upstream's helpers, each read at its site

- `config/functions` 201 and 208 `"${3:none}"`, 1894 and 1897 `"${PKG_NAME:exec}"`: substring expansions (`none` and `exec` evaluate to offset 0) where `:-` defaults were meant; they work by accident, and the lock name is empty when `PKG_NAME` is.
- `config/functions` 1694 `add_group`: `grep "$1:"` unanchored, so a group whose name ends in `$1` suppresses the add (`add_user` is anchored).
- `config/functions` 1511 `get_module_dir`: `basename $(ls -d .../lib/modules/*)` returns the wrong name when two module directories exist; `_CACHED_KERNEL_MODULE_DIR` (1508) is set nowhere.
- `scripts/pkgbuild` 32: `${fpkg}` is undefined (26 reads `fpkgname`), so an already-failed line prints an empty name.
- `config/functions` 1313: `. ${PKG_DIR}/package.mk || die`: bash disables errexit inside an `||` list, so a failing command at a recipe's global scope is ignored unless it is the last; recipes keep their global scope to assignments (late binding), so latent.

### Leads from the subagent not re-read (carried as leads, not findings)

`get_git` 28 `git restore --staged .` leaves working-tree edits in a cached clone (lead 4); `get_git` 36 under `pipefail` may SIGPIPE on a large ref list and force a re-clone (5); `get_git` 201 to 202 a token in the clone URL, dead (`PKG_USETOKEN` set by no recipe) (6); `get_archive` 33 a test that cannot fail (8); `pkgjson` 14's `exit` override (11: its failure path is caught at 18 to 21, so the claim is partial); `scripts/clean` and `scripts/build` `--all` unreachable (13); `exec_thread_safe`'s dead `$?` and its lock left on failure (15); `do_autoreconf` skipped without `intltoolize` (17); `CPPFLAGS_OPTIM_HARDENING` on C only, latent (18); the CMake toolchain conf appended non-atomically (20); `config/multithread` 64 the stats pipeline able to fail a finished build (21); `makefile_helper` 26 `distclean` exiting before its `rm` (22); `unpack` 196 default patch fuzz, 127 `PATCH_ARCH`, 100 the shared-`BUILD` fallback (24); `scripts/build` 600 to 611 `strip` errors silenced (25); `config/options` 92 `CONCURRENCY_LOAD` from `os.cpu_count()` ignoring affinity (26); `config/arch.aarch64` 19 to 36 no default CPU branch, and `cortex-a710` mapped to `armv8.2-a` there and `armv9-a` in `arch.arm` (27); the build stamp ignoring dependencies' stamps and settings, and `clean` leaving sysroot files (design notes). Each is re-read before it is carried to the punch list; otherwise it stays here.

## The nine #644 findings this slice carries

| # | #644's disposition for T5 | What this reading found | Disposition |
| --- | --- | --- | --- |
| 1 | record both container digests and dates; the refresh is the coordinator's | pin `988c0ba5…` created 2026-09-25T03:09:54Z; upstream `latest` `67e1fd0a…` created 2026-10-24T03:03:03Z (rebuilt since #644's read); `Dockerfile` identical; 10 of 12 layers differ (F-11) | recorded; refresh `to merge`, the coordinator's |
| 3 | a sentence naming `LOCAL_SSH_KEYS_FILE` and `LOCAL_WIFI_KEY`, no code change | both dropped by `DROP` (P1: `_KEYS_` and `_KEY`), as #644 says; the `Makefile` mounts `LOCAL_SSH_KEYS_FILE`'s file (150) but the container does not receive the variable unless it is in `~/.ROCKNIX/options` (sourced by the `Makefile` inside it, line 1). The same sandbox found F-01 and F-02 | a `get_env` comment or `device-builds.md` § Build credentials sentence: a punch item (documentation) |
| 4 | `BUILDER_VERSION` into `/etc/os-release`: keep | `Makefile` 208 passes `-e BUILDER_NAME=pixelelated-build -e BUILDER_VERSION=$(DOCKER_IMAGE_DIGEST)`; `scripts/image` writes it (168) | keep; no item |
| 8 | compare the ccache settings with CI's and decide with a measurement | `config/options`' settings quoted in `04` Q5; no recorded run's log carries ccache statistics (the four runs read: `Local Ccache: no` and per-package `ccache:host` sequence lines only), and `ccache --show-stats` against an M7 root is not run (brief § 4): **not measured**. LibreELEC #11890 (merged 2026-10-12, *name the compiler to ccache by the toolchain key*) is the upstream lead | `not measured`; a punch item to measure at the first build after the merge |
| 9 | note CI's clean of `retroarch` and `emulationstation` so nobody imports it | the step is in `build-aarch64-image.yml` (CI's base stage builds without 32-bit and credentials); a local whole-device run builds both once with the options in force (`build_distro`); the four recorded runs show one build of each | noted; no item |
| 10 | `--wrap-mode=nodownload`: keep; #585 candidate | `scripts/build` 196 and 227; **all 85 meson logs of the GENERIC_X64 build root record `-Dwrap_mode=nodownload`**, and no `subprojects/*/.git` exists under it (P10) | keep; #585 |
| 11 | record the dependency on ROCKNIX's mirror | `distributions/ROCKNIX/options` 186: `DISTRO_MIRROR="https://github.com/ROCKNIX/distribution-sources/releases/download/sources-v2"`; `update-mirror-sources.yml` is skipped by its gate weekly (Table 4) | recorded; a mirror of the fork's own only if upstream's goes away (the maintainer's call) |
| 13 | the identity: keep | `config/build-identity` read whole; 21 identity checks pass (P9); F-09 found the device route bypasses the duplicate refusal; `build-identity-test` is T14's by `slices.json` (#644's "T9" is its error, brief § 2) | keep, with F-09 |
| 22 | the credentials' path by name: keep | `KEEP` (get_env 14) passes the four by name; P1 shows `SCREENSCRAPER_DEV_LOGIN` kept; `~/.ROCKNIX/options` only `test -f` and its mode would be read (not read here at all) | keep |

The other seventeen are named with their carriers and not taken here: 2, 5, 14 (T4); 6, 7 (T9); 12, 23 (T11, T12); 15, 16 (T7, T8); 17, 18 (#645); 19, 21 (T10); 20 (#637's lane); 24 (T6); 25 (T32); 26 (#585).

## Coverage table: one row per path (242)

Generated by `tools/coverage-table.py` (committed beside this file) from brief § 2's membership over `inventory.json`, the Q4 (a) diff, `q6-tables.md` Table 1 and the per-path cells of `tools/coverage-cells.json` (each written from a finding, a check or a reading named in this file). It asserts 242 rows and no empty cell (`coverage-table: 242 rows, 0 empty cells`). Group is brief § 2's (1 the fork's own, 2 the upstream-carried engine core, 3 the system fragments, 4 the other configuration trees, 5 the workflows and templates). A group 3 to 5 file's Q1, Q2, Q3 and Q7 read `n/a: upstream's, unchanged here` unless a finding names it (brief § 4). Group 2's "read whole by the research subagent" cells are the subagent's read with every lead re-read here; the Python builders and the add-on scripts are marked as what was done to them. `Fork commits read` lists the fork's commits on a fork-own path since the base.

| Path | Group | Tier | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Fork commits read |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `.github/ISSUE_TEMPLATE/bug-report.md` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | read by GitHub when an issue or a PR is opened on the fork; none uses it (T10's) | n/a: upstream's, unchanged here | - |
| `.github/ISSUE_TEMPLATE/config.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | read by GitHub when an issue or a PR is opened on the fork; none uses it (T10's) | n/a: upstream's, unchanged here | - |
| `.github/pull_request_template.md` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): behind upstream (`c200cc906d`), F-12: to merge | n/a: runs on GitHub, not on the build host | read by GitHub when an issue or a PR is opened on the fork; none uses it (T10's) | n/a: upstream's, unchanged here | - |
| `.github/workflows/ai-usage.yml.disabled` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64-emu-libretro.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64-emu-standalone.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64-image.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64-mame-lr.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64-qt6.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64-rust.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64-toolchain.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-aarch64.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-arm.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-device.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-docker-image.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/build-nightly.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-10's sibling: daily `startup_failure` (#644 finding 19, T10) | Q4 (a): behind upstream (`76693a738d`), F-12: to merge | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/check-freeze-period.yml` | 1 | fork-own | no finding | the runner edit read | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a: GitHub | Table 4: called by `validate-pull-request.yml` only | no finding | 3d7c075f63 |
| `.github/workflows/retry-workflow.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/trigger-fail-if-upstream-changed.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/update-kernel-configs-docs.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-10: fails on every push to the linux recipe (3 runs) | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/update-mirror-sources.yml` | 5 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: runs on GitHub, not on the build host | Table 4 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `.github/workflows/validate-pull-request.yml` | 1 | fork-own | no finding | the runner edit read | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a: GitHub | Table 4: only on a PR to the fork's `next`; none has run | no finding | 3d7c075f63 7bd7f31312 |
| `.gitignore` | 1 | fork-own | no finding | `/.env` (51) and `/.qa-scratch/` ignored; `__pycache__/` | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a | git's, every checkout | each fork block commented | 1aac875e88 5f1b343d25 f3d19dc8fb 7b60fadaec b3e5c92559 ae060e9306 6003767521 4e46985442 330b9087a6 |
| `.merge-head` | 2 | upstream-carried | read: one LibreELEC commit hash: no finding | n/a: data, not code | read: one LibreELEC commit hash: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | Table 5: no reader in either tree | read: one LibreELEC commit hash: no finding | - |
| `Dockerfile` | 2 | upstream-carried | read whole (50 lines), identical to `upstream/next`: no finding | read whole; the fork never runs it (the pin is a mirror, F-13) | read whole (50 lines), identical to `upstream/next`: no finding | Q4 (b): identical to `upstream/next`; the pin is 29 days older than upstream's image (F-11) | n/a: no measurement of its own | CI's `build-docker-image.yml` and the fork's mirror workflow; `make docker-image-build` | read whole (50 lines), identical to `upstream/next`: no finding | - |
| `Makefile` | 1 | fork-own | the per-device recipes repeat two lines each; a pattern rule would do, upstream's shape | the `.env` lifecycle traced (205 to 208): sound for the file (`03` § 3.5); F-13 (the options mount writable) | no defect; F-02 lands through its `--env-file` | Q4 (a): differs (M), see `04` Q4 (a) | the container pin's age (F-11) | every fork build's entry | F-13: the local container no target runs; F-15: the options file's case | d7e2d6be41 a9af618398 1aac875e88 440ad22b68 2c349c6d51 67cd0e6493 a79b7f82a5 7bd7f31312 d704c9d563 73b20caf86 |
| `config/addon/dummy.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/addon/xbmc.broken.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/addon/xbmc.python.module.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/addon/xbmc.python.script.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/addon/xbmc.service.library.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/addon/xbmc.service.pluginsource.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/addon/xbmc.service.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/arch.aarch64` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read whole by the research subagent: no finding | - |
| `config/arch.arm` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read whole by the research subagent: no finding | - |
| `config/arch.x86_64` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read whole by the research subagent: no finding | - |
| `config/blocklist` | 2 | upstream-carried | read whole (29 lines): one reason per held-back package: no finding | read whole | read whole (29 lines): one reason per held-back package: no finding | Q4 (a): behind upstream (`c4d353449e`), F-12: to merge | n/a: no measurement of its own | `scripts/update_packages` (`make update`), never run on the fork | read whole (29 lines): one reason per held-back package: no finding | - |
| `config/build-identity` | 1 | fork-own | no finding | fails closed on every invalid input (P9's 16 rejections) | no defect (P9: 21 identity checks pass); F-09 is the caller's | Q4 (a): differs (A), see `04` Q4 (a) | n/a: one call per image | `scripts/image` 60 to 61 | one function, one responsibility; `04` Q7 on the identity's four files | 40bc5469b9 f10eec1306 |
| `config/docker/changelog.txt` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/docker/package.mk` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/docker/source/bin/docker` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/docker/source/default.py` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/docker/source/resources/language/English/strings.po` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/docker/source/resources/settings.xml` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/docker/source/system.d/docker.service` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/emulators/3do.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/3ds.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/amiga.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/amigacd32.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/amstradcpc.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/arcade.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-03: no `SYSTEM_WIKI_PATH`; the document inherits the previous system's | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/arduboy.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atari2600.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atari5200.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atari7800.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atari800.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atarijaguar.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atarilynx.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atarist.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/atomiswave.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/bbcmicro.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/bk.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/c128.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/c16.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/c64.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/cdi.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/channelf.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/chip-8.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/colecovision.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/cps1.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/cps2.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/cps3.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/daphne.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-03: no `SYSTEM_RELEASE`, so the image carries the previous system's (P7) | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/doom.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/dreamcast.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/easyrpg.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/famicom.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/fbn.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/fds.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gameandwatch.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gamecube.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gamegear.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gb.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gba.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gbah.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gbav.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gbc.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gbch.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gbh.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/genesis.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/genh.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ggh.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/gp32.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-03: no `SYSTEM_RELEASE`, so the image carries the previous system's (P7) | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/heroic.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/idtech.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/imageviewer.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-03: sets `SYSTEM_COMMAND`, which the next system would inherit (P6) | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/intellivision.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ios.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/j2me.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/macintosh.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/mame.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/mastersystem.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/megacd.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/megadrive-japan.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/megadrive.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/megadriveh.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/megaduck.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/moonlight.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-03: sets `SYSTEM_COMMAND`, which the next system would inherit (P6) | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/moto.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/mplayer.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/msx.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/msx2.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/music.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/n64.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/n64dd.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/naomi.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/nds.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ndsiware.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/neocd.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/neogeo.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/nes.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/nesh.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ngp.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ngpc.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/odyssey2.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/openbor.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/palm.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pc-8800.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pc-9800.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pc.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pcengine.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pcenginecd.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pcfx.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pet.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pico-8.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pokemini.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ports.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ps2.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/ps3.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/psp.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/pspminis.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/psvita.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/psx.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/satellaview.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/saturn.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/scummvm.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/scv.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/sega32x.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/segacd.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/segamodel3.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-03: no `SYSTEM_WIKI_PATH`; the document inherits the previous system's | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/sfc.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/sg-1000.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/snes.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/snesh.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/snesmsu1.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/st-v.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/steam.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/sufami.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/supergrafx.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/supervision.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/tg16.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/tg16cd.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/tic-80.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/tools.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | F-03: sets `SYSTEM_COMMAND`, which the next system would inherit (P6) | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/triforce.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/uzebox.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/vectrex.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/vic20.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/videopac.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/vircon32.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/virtualboy.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/wasm4.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/wii.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/wiiu.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/wiiware.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/windows.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/wonderswan.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/wonderswancolor.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/x1.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/x68000.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/xbox.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/zmachine.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/zx81.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/emulators/zxspectrum.conf` | 3 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: read once per build by `add_es_system`; no cost of its own | Table 2 (`q6-tables.md`) | n/a: upstream's, unchanged here | - |
| `config/functions` | 2 | upstream-carried | F-21: substring expansions for defaults; unquoted `$@` (996, 1437, 1656, 1895) | F-21: `. package.mk \\|\\| die` disables errexit for recipe globals | F-17 (device files outside the stamp, P12); F-21; `calculate_stamp`'s generic recipe correct (P2) | Q4 (a): identical to `upstream/next` | `calculate_stamp`'s whole-directory hash: `04` Q5 | sourced by `config/options` or `config/path` on every build | nine sections, about twelve responsibilities in 1,936 lines (`04` Q7); F-05 is the rule's | - |
| `config/graphic` | 1 | fork-own | no finding | the fork's `LLVM_SUPPORT` line (#291) read | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a: flags only | sourced by recipes through `config/options` | the fork's comment explains the change | f483f215ad 73b20caf86 |
| `config/multithread` | 2 | upstream-carried | SC2068 at 50: an upstream idiom | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read whole by the research subagent: no finding | - |
| `config/noobs/marketing/slides/A.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides/B.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides/C.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides/D.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides/E.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides/noobs.psd` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides_vga/A.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides_vga/B.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides_vga/C.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides_vga/D.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides_vga/E.png` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/marketing/slides_vga/noobs_vga.psd` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/os.json` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/partition_setup.sh` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/noobs/partitions.json` | 4 | upstream-carried | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | n/a: upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: not read by a fork build | Table 3: no fork build, image or CI reaches it | n/a: upstream's, unchanged here | - |
| `config/optimize` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read whole by the research subagent: no finding | - |
| `config/options` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | the ccache settings (100 to 118) and `CONCURRENCY_MAKE_LEVEL` (91): `04` Q5 | sourced by `config/options` or `config/path` on every build | F-15: the options files at 132 to 140; 98's comment says per project, the cache is per build root | - |
| `config/path` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read whole by the research subagent: no finding | - |
| `config/show_config` | 1 | fork-own | no finding | the fork's one line read | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a | `scripts/image`, `build_compat` | no finding | f10eec1306 |
| `config/sources` | 2 | upstream-carried | read whole (2 lines): `SOURCEFORGE_SRC`: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole (2 lines): `SOURCEFORGE_SRC`: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read whole (2 lines): `SOURCEFORGE_SRC`: no finding | - |
| `distributions/ROCKNIX/config/functions` | 1 | fork-own | `ls \| sort` in a loop (106); `2>/dev/null` over the formatter (113) | F-04: the formatter's error silenced (Guards must fail closed) | F-03 (carry-over, two shipped years wrong), F-04 (T3's F-06 confirmed) | Q4 (a): differs (M), see `04` Q4 (a) | n/a: one table per image | the `emulators` metapackage (T3's caller); P3, P11 regenerate its output byte-exactly | F-04: the default step marks every core so far | 5e2509a25a 7650de7dd6 |
| `distributions/ROCKNIX/kernel_options` | 2 | upstream-carried | read: empty (0 lines); `linux/package.mk` 318 tests for it: no finding | n/a: data, not code | read: empty (0 lines); `linux/package.mk` 318 tests for it: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | sourced by `config/options` or `config/path` on every build | read: empty (0 lines); `linux/package.mk` 318 tests for it: no finding | - |
| `distributions/ROCKNIX/logos/rocknix-logo.png` | 2 | upstream-carried | n/a: an image | n/a: an image | n/a: an image | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | read by nobody in the build; `.github/scripts/generate-release-body.sh` links upstream's copy by URL (T10's) | n/a: an image | - |
| `distributions/ROCKNIX/options` | 1 | fork-own | no finding | the fork's identity lines read; `DISTRO_MIRROR` 186 (#644 finding 11) | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a | sourced first by `config/options` on every build | 63 SC2034 notes: an options file, noise | f10eec1306 a9af618398 3d7c075f63 |
| `distributions/ROCKNIX/version` | 1 | fork-own | no finding | read whole (11 lines) | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a | sourced by `config/options` on every build | the identity's first file of four (`04` Q7) | 40bc5469b9 f10eec1306 3d7c075f63 |
| `scripts/autoreconf` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: `config/functions` and `scripts/build` (the autotools step) | read whole by the research subagent: no finding | - |
| `scripts/autoremove` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | CI only: `scripts/pkgbuilder.py` with `AUTOREMOVE` (upstream's staged graph); no fork build sets it | read whole by the research subagent: no finding | - |
| `scripts/build` | 1 | fork-own | SC2166/SC2044/SC2046 in upstream's lines: idioms, not defects (`02` § shellcheck) | the fork's 12 lines read: the watch entry (7 to 12) and `--wrap-mode=nodownload` (196, 227); the hook order is upstream's (`packages/README.md`) | no defect in the fork's lines; P10 proves the meson guard reached 85 of 85 configures | Q4 (a): differs (M), see `04` Q4 (a) | the watch entry: one exec and a lock per top-level entry; the recorded runs' timings in `04` Q5 | reached by every package of every fork build (Table 1) | 646 lines, upstream's structure; the fork's hunks commented in place | 1aac875e88 79437a25c0 |
| `scripts/build_compat` | 1 | fork-own | F-07: pre-identity naming kept | the watch entry read | F-07: honours `CUSTOM_VERSION`/`CUSTOM_IMAGE_NAME`, which the identity refuses | Q4 (a): differs (M), see `04` Q4 (a) | the ARM compatibility root, part of each H700/SM8550 run | `build_distro` for `arm` (Table 1) | F-07: `GIT_HASH`, `ORIGIN_URL` unused | 1aac875e88 |
| `scripts/build_distro` | 1 | fork-own | F-14: a dead `$?` check under `set -e` | `set -e` (15); the watch entry; `DISTRONAME` roots | F-09: the prune of `target/` (84) defeats the image's refusal | Q4 (a): differs (M), see `04` Q4 (a) | the whole-device run; timings in `04` Q5 | the `Makefile`'s device targets (Table 1) | F-09's reason lives in `c2bb7ec0b9`'s message only | 43d0bc3bf4 1aac875e88 c2bb7ec0b9 |
| `scripts/build_mt` | 2 | upstream-carried | SC2068 `${@}` unquoted: an upstream idiom | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | CI only: the staged workflows; fork builds never call it (#644 finding 6, T9) | read whole by the research subagent: no finding | - |
| `scripts/ccache_stats` | 2 | upstream-carried | read whole (9 lines): `${TOOLCHAIN}/bin/ccache -s`: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole (9 lines): `${TOOLCHAIN}/bin/ccache -s`: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | **no caller** (both searches zero): a developer helper run by hand (`${TOOLCHAIN}/bin/ccache -s`) | read whole (9 lines): `${TOOLCHAIN}/bin/ccache -s`: no finding | - |
| `scripts/checkdeps` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | F-20: changes the host's default compiler and `/nix` with `sudo` | F-20 | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: every entry point; `config/options` | read whole by the research subagent: no finding | - |
| `scripts/clean` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: `Makefile` `package-clean`; documented first step (CLAUDE.md); recipes | read whole by the research subagent: no finding | - |
| `scripts/create_addon` | 2 | upstream-carried | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | `bash -n` ok; shellcheck read | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | upstream tooling only: `tools/repo-tool` (Kodi add-ons; T6's); no fork build | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | - |
| `scripts/create_docker_package` | 2 | upstream-carried | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | `bash -n` ok; shellcheck read | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | **no caller** (both searches zero); its template is `config/docker` (`cp -R config/docker`, line 163) | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | - |
| `scripts/extract` | 1 | fork-own | no finding | the fork's `mkdir -p` (one line) | no defect | Q4 (a): differs (M), see `04` Q4 (a) | n/a: per-package unpack cost | `scripts/unpack` (Table 1) | no finding | 73b20caf86 |
| `scripts/genbuildplan.py` | 2 | upstream-carried | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | `py_compile` ok | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: `config/multithread` (the plan every build runs); `tools/viewplan` | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | - |
| `scripts/get` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: `scripts/unpack`, `config/functions`, the workflows | read whole by the research subagent: no finding | - |
| `scripts/get_archive` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | F-19: `--no-check-certificate` | F-19: an empty `PKG_SHA256` accepts any download | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build, dynamically: `scripts/get` 48 to 53 (`${SCRIPTS}/get_${get_handler}`); the fixed-string search finds only `tools/distro-tool` | read whole by the research subagent: no finding | - |
| `scripts/get_env` | 1 | fork-own | no finding | D-INFRA-006: F-01 (the names), F-02 (the line format) | F-01, F-02 (P1) | Q4 (a): differs (M), see `04` Q4 (a) | n/a: one listing per Docker build | the `Makefile`'s `docker-%` recipe (Table 1) | its comment promises more than `DROP` does (F-01) | d704c9d563 |
| `scripts/get_file` | 2 | upstream-carried | read whole (6 lines): no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole (6 lines): no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build, dynamically: `scripts/get` 48 to 53; both fixed-string searches zero, the dispatch is the reader | read whole (6 lines): no finding | - |
| `scripts/get_git` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | sets its own `set -e` and `pipefail` (15 to 16) | F-18: a cached clone accepted on any ref (P13) | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build, dynamically: `scripts/get` 48 to 53; both fixed-string searches zero, the dispatch is the reader | lead 6: a token-URL path set by no recipe | - |
| `scripts/image` | 1 | fork-own | SC2046/SC2061/SC2044 in upstream's lines | the identity blocks read (60 to 61, 78 to 82, 106 to 121, 139 to 168): fail closed on an invalid identity (`die`) | F-09: its refusal is bypassed by `build_distro`'s prune | Q4 (a): differs (M), see `04` Q4 (a) | image assembly 5 m 7 s for GENERIC_X64 in run `20261022T235954Z-4749157a` (the whole run; `04` Q5) | reached by every device build (Table 1); writes `/etc/os-release` and the sidecar on every image | F-06: `ORIGIN_URL` and `BUILD_FILENAME` written for nobody; the identity split over four files (`04` Q7) | f10eec1306 a9af618398 0159cb3235 1aac875e88 73b20caf86 |
| `scripts/install` | 1 | fork-own | SC2166 at 164 (upstream's) | the watch entry read (6 lines) | no defect in the fork's lines | Q4 (a): differs (M), see `04` Q4 (a) | the watch entry only | reached by every fork build | no finding | 1aac875e88 |
| `scripts/install_addon` | 2 | upstream-carried | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | `bash -n` ok; shellcheck read | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | upstream add-on path only: `scripts/pkgbuild` when a package is an add-on; no fork image builds one | n/a: unreached by any fork build, image or CI (Table 1); upstream's, unchanged here | - |
| `scripts/makefile_helper` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | `Makefile` `clean`/`distclean` | read whole by the research subagent: no finding | - |
| `scripts/mkimage` | 2 | upstream-carried | no `set -e`; per-step `\\|\\| show_error` | F-16: two branches and `pigz` unguarded | F-16: success reported over an incomplete `qcom-abl` (SM8550) or `arm-efi` image | Q4 (a): identical to `upstream/next` | part of the image step; not timed separately in the recorded runs | fork build: `scripts/image` `do_mkimage` | one structure per bootloader, repeated four times (`04` Q7) | - |
| `scripts/pkgbuild` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | F-21: `${fpkg}` undefined (32) | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: `config/multithread` (the per-package worker), `scripts/pkgbuilder.py` | read whole by the research subagent: no finding | - |
| `scripts/pkgbuilder.py` | 2 | upstream-carried | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | `py_compile` ok | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: `config/multithread` (the parallel builder every build runs) | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | - |
| `scripts/pkgjson` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | read whole by the research subagent, leads re-read: no finding | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: `config/multithread` (the plan's input); `tools/viewplan` | read whole by the research subagent: no finding | - |
| `scripts/test-audit-review.py` | 1 | fork-own | no finding | `py_compile` ok | n/a: the code-auditor's test, not the engine's | Q4 (a): differs (A), see `04` Q4 (a) | n/a | Table 5: no caller, not in CI; misfiled into this area | belongs with `tools/lint-audit-artifacts` (a lead for `areas.json`) | 5150320de2 |
| `scripts/uboot_helper` | 2 | upstream-carried | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | `py_compile` ok | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: the bootloader recipes (`u-boot`, `rkbin`, `crust`) and `projects/*/bootloader` | not read line by line: `py_compile` ok and its callers read (Q6); a coverage boundary (`04`) | - |
| `scripts/unpack` | 2 | upstream-carried | SC2144 at 90 (F-08) | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | F-08: two `name-version*` matches empty the package (P8); leads 24 | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | fork build: every package with a source | read whole by the research subagent; its leads re-read here: no finding | - |
| `scripts/update_packages` | 2 | upstream-carried | read whole by the research subagent, leads re-read: no finding | `bash -n` ok (shell); shellcheck read; leads re-read: no finding | F-19: strips the checksum of every archive recipe it bumps (latent: never run) | Q4 (a): identical to `upstream/next` | n/a: no measurement of its own | `Makefile` `update` only; never run on the fork (#644 finding 15, T7/T8) | read whole by the research subagent: no finding | - |

## Proofs

Each proof's cell names its class (brief § 6, Verification). The scripts are under `tools/` beside this file; the scratch outputs under `.qa-scratch/t5/` (gitignored).

| # | What | Script / artifact | Trace read (engagement, writes) | Result | Cell |
| --- | --- | --- | --- | --- | --- |
| P1 | `scripts/get_env` over a constructed environment | `tools/sb-get-env.sh` (04:00); `TRACE=1` run first into `sb-get-env/trace.txt` | 94 trace lines; `KEEP=`, `DROP=` and `compgen -e` executed; no write (the script only prints) | F-01's six names kept, four dropped as designed; F-02's bare `OTHER_TOKEN` line | proved: sandbox |
| P2 | `calculate_stamp` over a fixture override and its generic twin | `tools/sb-calculate-stamp.sh <scratch>` (04:02; rerun from the committed copy into `sb-stamp2`, the same two stamps) | 4 calls of `calculate_stamp`; `find -L` over the fixture's paths only; sourcing `config/functions` runs 3 top-level lines (an EXIT trap, `onexitcleanup`, which returns on rc 0) | the stamp moves on the generic bump; the stubbed control does not | proved: sandbox |
| P3 | the launch table regenerated for GENERIC_X64 from this tree (T3's script, unchanged) with the build root's own `xmlstarlet` (`toolchain/bin/xml` of `m7-signin-build-20261022-07`, copied, sha256 `3ee557da6cbdefa8…` both) | `tools/regen-es-systems.sh`, `bash -x` (04:04) | 128 `add_es_system` calls, 1 `mk_es_systems`; every `mkdir`/`ln`/`cp` target under the scratch (the sources read are the tree's) | rc 0, 128 systems; `install/usr/config/emulationstation/es_systems.cfg` **byte-identical** to that image's (`cmp`, no output); stub misses 0 | proved: sandbox |
| P4 | case A, two default lines in one emulator | `tools/sb-es-cases.sh` (04:05) | `fo` executed; rc 2 | F-04 case A | proved: sandbox |
| P5 | case B, a `false` core before the `true` one | the same | rc 0 | F-04 case B | proved: sandbox |
| P6 | case C, a system after `imageviewer` | the same | rc 0, 129 systems | F-03's carry-over | proved: sandbox |
| P7 | `<release>` of `daphne` and `gp32` in two install trees | `image/system/usr/config/emulationstation/es_systems.cfg` of `m7-signin-build-20261022-07` (GENERIC_X64, `069fc2704421`) and `m7-signin-h700-build-20261023-06` (H700), read-only, parsed with `ElementTree` | — | `1996` both, on both | proved: image-set |
| P8 | `scripts/unpack` 90's test with one and two matches | `tools/sb-unpack-glob.sh <scratch>` (04:10) | the lifted line runs twice; writes only the fixture directories | F-08 | proved: sandbox |
| P10 | `--wrap-mode=nodownload` reached meson | the GENERIC_X64 build root `m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/build/*/.<triple>/meson-logs/meson-log.txt`, read-only (04:11-04:31) | — | 85 of 85 logs carry `-Dwrap_mode=nodownload` in `Build Options`; `find ... -path '*/subprojects/*/.git'` empty | proved: recorded-run |
| P11 | the H700 and SM8550 launch tables regenerated from this tree | `tools/regen-es-systems.sh` (04:11-04:31) | — | rc 0, 126 and 139 systems, each byte-identical to its install tree (`m7-signin-h700-build-20261023-06`, `m7-signin-sm8550-build-20261023-03`); RK3326 126 and RK3566 132 have no image on the host | proved: sandbox |
| P12 | `calculate_stamp` against a device-level file `find_file_path` reads | `tools/sb-stamp-device-config.sh <scratch>` (04:11-04:31) | 4 calls of `calculate_stamp`; `find_file_path` resolved the fixture's `devices/H700/config/kernel-firmware.dat` | the list extended, the stamp unchanged | proved: sandbox |
| P13 | `get_git` 36's cache check over a clone whose `HEAD` is behind its remote branch | `tools/sb-get-git-head.sh <scratch>` (04:11-04:31; `GIT_CONFIG_GLOBAL=/dev/null`, fixture author) | the check's two runs and `ls-remote`'s refs printed | `PKG_VERSION=A` accepted with `HEAD` at B | proved: sandbox |
| P9 | the identity rules of `config/build-identity` and `scripts/image`'s blocks | `tools/build-identity-test` (T14's), synthetic only | — | 21 passed; the 2 failures #801's | proved: sandbox |

## Criterion entries: #652's checklist (= brief § 7), evaluated at the end of Phase 2 (2026-10-24 04:31 UTC, `date -u`)

Verdicts as the skill defines them. **OPEN (stage X)** means the criterion's artifact is produced by a later stage of this lane and is not yet due: neither PASS nor FAIL, re-evaluated at that stage.

### AC-01: the audit folder holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`
**Verdict:** PARTIAL ⚠ (OPEN for `04`, `05`: stages B to D). **Evidence:** `00` to `03`, `q6-tables.md`, `tools/`, `second-opinions/review-plan.json` present.

### AC-02: `tools/lint-audit-artifacts` prints PASS (pre-issue before stage D; resolution at close), the renovation face included
**Verdict:** OPEN (stage C to D, then H).

### AC-03: `second-opinions/review-plan.json` records Extended depth and two reviewers from two other labs, each provenance naming its served model
**Verdict:** PARTIAL ⚠. `review-plan.json` written before any call (depth `extended`, reviewers `gpt`/openai and `gemini-argon`/google); the probes and calls wait for the host window's return (opened 03:47).

### AC-04: the punch-list issue has every item at a Phase 7 outcome
**Verdict:** OPEN (stages D to F).

### AC-05: `reviewed-at:` and `fixed-at:` carry the lane's commits
**Verdict:** PARTIAL ⚠. `reviewed-at: 46f6c7d428`, the slice's bytes `8ebaf8daad`'s (the stage-A byte check, exit 0), the branch on the P1 tip (`merge-base --is-ancestor`, exit 0); in `00` and `01` § Scope. #652's body at hand-back; `fixed-at` after stage E.

### AC-06: `01` § Scope records the read hash, the filter's output with the order row's figures reproduced by the tool's `CODE` set, what the globs sweep in, the M7 delta, and the two trackers with dates
**Verdict:** PASS ✓. **Evidence:** `01` § Scope: `8ebaf8daad`; 242 / 13,910 / 18 fork-own 3,266 / 224 / 6,776 / 2,419, no delta, with `tools/renovation-inventory` 674 to 676's set and `order()`'s predicate at 1274; the 52 extra files of the glob directories, all T10's; the 353 `records` rows; the M7 delta none; ROCKNIX's and LibreELEC's PRs read 2026-10-24 03:57 UTC (`01` § Phase 1, each truncated at its `--limit`, said so). **What would have failed it:** any figure that differed without a delta row, or a tracker read without a date.

### AC-07: `02` carries a coverage table with exactly one row per path, `grep -c` 242, each Q cell answered or `n/a` with a reason
**Verdict:** PASS ✓. **Evidence:** ``grep -c -E '^\| `(scripts|config|distributions|Makefile|Dockerfile|\.gitignore|\.merge-head|\.github)' 02-forward-audit.md`` prints 242; the generator asserts 242 rows and 0 empty cells. Three Python builders' and three add-on scripts' Q1, Q3 and Q7 cells say what was done to them (not read line by line; unreached), which is the coverage boundary `04` states. **What would have failed it:** another table in this file whose rows begin with a membership path (none does: the mechanical and proof tables begin with a check or `P<n>`).

### AC-08: `02` records each mechanical check with command, exit status and summary, a check that could not run with its reason
**Verdict:** PASS ✓. **Evidence:** § Mechanical checks: `bash -n` (41 ok; 26 and 15), `py_compile` (5), `tools/build-identity-test` (`21 passed, 2 failed`, as #801 expects), `test-build-monitor` (36 PASS), shellcheck (5 errors read at their sites), the three sandboxed calls (P1 `get_env` with the constructed failing names, P2 `calculate_stamp`, P3 to P6 and P11 the launch table with the pre-format table through `ElementTree` in P4 and P5), the container manifests with both digests and both `created` dates, the 19 workflows' state and last three conclusions, `fork-package-freshness --list` (nothing of the slice); `actionlint` and the `Makefile` as shellcheck input recorded as not run, with the reason.

### AC-09: § The nine #644 findings, one row each with its disposition, the other seventeen named with their carriers
**Verdict:** PASS ✓. **Evidence:** § The nine #644 findings this slice carries: 1, 3, 4, 8, 9, 10, 11, 13, 22, and the seventeen with carriers.

### AC-10 to AC-12: `04` § Renovation face Q4 (two currency tables), Q5 (ccache, the stamp's cost, the recorded runs, time to play), Q6 (five reachability tables)
**Verdict:** OPEN (stage B, `04`). Inputs ready: `q6-tables.md` Tables 1 to 5; Q4 (a)'s 21 rows; Q4 (b)'s digests; the three runs' timings.

### AC-13: every proof carries a `proved:` cell; ``grep -c 'proved:' 02`` equals ``grep -c '^PROOF:' 00``
**Verdict:** PASS ✓ (at this point). **Evidence:** 13 and 13 (P1 to P13; `sandbox` 11, `image-set` 1, `recorded-run` 1). Re-counted at stages F and H.

### AC-14: `tracked:` items' bug issues carry the VM line and a verifiable criterion; `removal: yes` items carry `Already written:`; no pin, admission, watcher or trigger change without a stream brief; `box-check` passes on the issues
**Verdict:** OPEN (stage D). No change of any kind has been made to the slice's code on this branch (`git diff --stat 8ebaf8daad HEAD -- <the 242 paths>` empty but for nothing: the branch adds only `docs/`).

### AC-15: the retro exists, is posted, and answers what the slice did to the two time-to-play numbers
**Verdict:** OPEN (stage G).

### AC-16: the five checkers and `hooks-test` pass on the branch; the lint prints PASS; the six exit codes on #652
**Verdict:** OPEN (stage H).

# Packet file: `03-retrospective.md`

# Retrospective Audit — M6.P2 T5, the build engine

**Date:** 2026-10-24. **Read at:** `reviewed-at: 46f6c7d428` (the slice's bytes `next`'s `8ebaf8daad`). Findings `F-NN` are `02-forward-audit.md`'s; this file works backwards from the whole engine to what reading unit by unit can miss.

## 3.1 Architectural coherence

The engine is LibreELEC's (`config/functions`' header; `scripts/*`' copyright lines name OpenELEC 2009 and LibreELEC 2016 onward) with ROCKNIX's distribution layer (`distributions/ROCKNIX/`) and the fork's additions in five places only: the watch entry (one six-line block in five scripts, `1aac875e88`), the identity (`config/build-identity`, 44 lines, and its blocks in `scripts/image`, `f10eec1306`/`40bc5469b9`), the container's lifecycle (`Makefile` 131 to 208, `scripts/get_env`), the meson guard (`scripts/build` 185 to 196, 227, `79437a25c0`), and the name (`DISTRONAME="pixelelated"`, `a9af618398`, and `build_distro`'s `DISTRONAME` roots, `43d0bc3bf4`). Each addition is small and sits beside the upstream line it changes. **The incoherence is where an addition left an older mechanism in place:** `scripts/build_compat` keeps the naming the identity replaced (F-07); `scripts/image` keeps an `ORIGIN_URL` for consumers that do not exist (F-06); `build_distro`'s prune predates the identity and quietly cancels its refusal (F-09).

## 3.2 Project conformance

**Instruction files** (read from this session's context, `next`'s copies except the four the stage-A diff names):

| File | Relevance | Finding |
| --- | --- | --- |
| `device-builds.md` | the engine's own rule | § After rebasing item 3 is stale (F-05); § Build credentials says `get_env` drops "anything secret-shaped", which F-01 shows is narrower; § Publishing's "existing identities cannot be replaced" holds for `scripts/image` alone (F-09) |
| `engineering-practices.md` § Guards must fail closed | every guard in the engine | `mk_es_systems`' `2>/dev/null` over the formatter (F-04); `add_es_system`'s silent carry-over (F-03); `unpack` 90's test that errors into "false" (F-08); `get_env`'s line format (F-02) |
| `engineering-practices.md` § A name is not a behaviour | comments that claim | `scripts/image` 71's "existing image metadata consumers" (F-06); `virtual/emulators/package.mk` 150's "will result in a build failure" (T3's F-06, F-04 here: true for one shape, silent, false for the other) |
| `upgrade-and-install.md` (*Already written*) | the engine writes `/etc/os-release`, the sidecar, `target/` names, the launch table | F-03's two `<release>` values are on every image already built; a fix rewrites them at the next image (the table is regenerated each build, nothing on a device reads `<release>` back into state): `Already written:` the wrong year on images in the field; corrected by the next image, nothing to migrate |
| `fork-workflow.md` | which files are personal paths | none of the 242 is a personal path; `.githooks/pre-push`'s content rule applies to the product scripts, not the engine |
| `worktrees.md` § Build worktrees | `BUILD_BRANCH` from `git branch --show-current` | `scripts/image` writes it (154); unchanged by the fork; no finding |
| `packaging-and-patches.md`, `packages/README.md` | the contract the engine promises recipes | the hook order in `scripts/build` is upstream's, unchanged by the fork (the fork's hunks are the watch entry and the meson flags): no finding; read at the hook sites only, not whole (Coverage boundary, `04`) |

**Blindspot register** (titles read for all 74; bodies of the entries the brief names):

| Entry | Repeated here? |
| --- | --- |
| 14, 26 (a guard inside what it guards; a hooks path that runs nothing) | no: the watch entry's guard has its positive in `test-build-monitor` (36 PASS) and in every recorded run's `build.status` |
| 34 (proven only under the host's tools) | the sandboxes run the host's bash 5.3; the container's bash is not read (brief § 5). F-08's `[` behaviour is POSIX `test`'s and identical under any bash; F-01 and F-02 use `[[ =~ ]]` and `echo`, the same. Named as the boundary |
| 39 (a suite that passed over dashes) | avoided: every Q6 zero re-checked with a second pattern and then the dispatch read (`get_git`, `get_file`, `get_archive` are reached through `scripts/get` 48 to 53) |
| 43 (a safety claim in a header comment, never tested) | **yes**: `get_env`'s header claims "anything that looks like a secret" (F-01), `package.mk` 150's "will result in a build failure" (F-04) |
| 46 (a name read as a behaviour) | **yes**: `ORIGIN_URL`'s comment (F-06); `device-builds.md`'s stamp sentence read as the engine's behaviour by the brief (F-05) |
| 47 (a dependency the build fetched for itself) | no: P10 shows the guard reached all 85 meson configures |
| 48 (a constraint that lived only in a commit subject) | the `rm -rf` of `target/` (F-09) carries its reason only in `c2bb7ec0b9`'s message |
| 62 (a fix corrected the writer and left what it had written) | F-03's fix must say what is already on images (above) |
| 72 (a comment held an invariant the code had stopped keeping) | **yes**: `scripts/image` 78's comment and `build_distro`'s prune (F-09) |
| 73, 74 (completion not activity; a fixture that did not engage) | every sandbox's trace was read for the call under test (P1 to P8); T3's regeneration counted its stub's calls and misses (0) |

**Project invariants:** no secret in a committed file (the fixtures assemble names at run time; values are `fixture-N`); no write outside this lane's tree and `.qa-scratch/` (every trace read for writes).

## 3.3 Spec fidelity

The brief's Q3 framing of `calculate_stamp` (*"a defect in the engine, or a documented limit"*) was neither: the engine was fixed two months ago and the rule did not follow (F-05). The brief's § 2 (`scripts/image` 78 to 82, "the refusal of an existing identity") describes a guard that the documented route never reaches (F-09). Both are leads for the coordinator's template, not changes here.

## 3.4 Platform conformance

Upstream conformance: the fork's engine hunks are each small and upstreamable in shape; the wrap-mode guard (#585) and the stamp fix (already upstream) show the path works. F-03, F-04 and F-08 are upstream's defects in upstream's code (#585 candidates, D-WORKFLOW-164; submissions deferred, D-WORKFLOW-165).

## 3.5 Cross-system interaction audit

### Interaction: the entry points × `tools/watch-build` (T9's)

Five scripts (`build`, `image`, `install`, `build_distro`, `build_compat`) exec `./tools/watch-build --entry -- "$0" "$@"` unless `RASTERATOPS_WATCH_EXEC` equals `$0`; `watch-build` sets it to `command[0]` (`tools/watch-build` 88) and the nested call reuses the outer run. `build_mt` and `clean` carry no entry (#644 finding 6, T9's). Proven by `test-build-monitor`'s real entry-point prefixes (36 PASS) and by every recorded run's single `.build-runs/<id>/` per top-level invocation. A relative `./tools/watch-build` means every entry point must run from the tree's root, which `config/options ""` already requires. No finding.

### Interaction: `scripts/get_env` × the `Makefile`'s `.env` recipe × `~/.ROCKNIX/options`

The recipe (205 to 208) removes an older `.env`, writes it under `umask 077` and `set -C`, removes it on exit, and starts no container if `get_env` fails. The lifecycle is sound for files; **the content is not**: F-01 (the name filter) and F-02 (the line format). The options file reaches the container twice: mounted (147, writable: F-13) and included by the `Makefile` inside it (line 1). A SIGKILL of make leaves `.env` owner-only in the worktree (`/.env` is gitignored, `.gitignore` 51); no `.env` exists in this worktree (`test -e .env` false).

### Interaction: `calculate_stamp` × the overrides that source a generic recipe (T8's)

Correct since `cb884edb0f` (P2). The rule text is stale (F-05). The cost side (a metadata-only change rebuilds the package) is Q5's.

### Interaction: `mk_es_systems`/`add_es_system` × the `emulators` metapackage (T3's)

F-03 and F-04. The table is regenerated byte-exactly on the host (P3, P11), so every fix here has a sandbox proof before any build; the shipped bytes change only for F-03's two `<release>` lines.

### Interaction: `scripts/image`'s identity × `tools/rc-preflight`, `tools/fork-publish-release` (T9's, the release rules)

The identity is frozen once (`pixelelated_build_identity`) and exported to every package install; the sidecar and `/etc/os-release` carry it. `tools/build-identity-test` passes its 21 identity checks (P9); its release-plan half fails (#801). F-09: the device route prunes before the refusal.

### Interaction: the upstream workflows × the fork's own CI (T10's)

Table 4 of `q6-tables.md`: two workflows run on the fork and end red or skipped every time (`Build` daily, `update-kernel-configs-docs` on pushes, F-10); nothing reads them. T10's call.

## 3.6 What's missing?

- **A test that runs `build_distro`'s prune and the image's refusal together** (F-09): the identity test exercises the image's blocks alone.
- **A test of `get_env`** at all: the script has none; P1 is the first.
- **A check of the launch table's invariants** (one default per system, a command per system): T3's tables and P3 to P6 are the first.
- **The container's bash version** is not recorded anywhere a reader can find without pulling the image.

## 3.6.5 The futro's predictions, checked

| Prediction (`docs/futros/2026-10-24-m6-build-engine.md` § 4) | Outcome |
| --- | --- |
| a build log's defines pasted into an artifact | did not happen: every read went through `readlog`; no configure line reproduced |
| the sandbox writing into the worktree through `config/path` | the sandboxes never source `config/options`; the one function sourced (`config/functions`) runs three top-level lines (an EXIT trap); the committed scripts were changed to take an explicit scratch directory when two of them were found writing beside themselves (friction log 04:05) |
| `get_env`'s fixture as a credential-shaped literal | avoided: names built with `printf`, values `fixture-N`; the pre-commit scan passed |
| the identity test's 21/2 read as a broken identity | read as #801's, as predicted |
| a `docker pull` for the `created` label | not needed: the config blobs answered through GHCR's anonymous token, and both `created` dates were read |
| a zero caller from git's regex | prevented by the second pattern; three zeros were dynamic dispatch |
| the pre-mortem's forty shellcheck items | not repeated: 5 errors read at their sites, one a finding; warnings grouped, not itemised |

## Retrospective Summary

### Architectural Assessment
Sound and mostly upstream's; the fork's additions are small. Three of them left an older mechanism standing (F-06, F-07, F-09).

### Cornerstone Alignment
Least surprise and fail-closed are where the engine falls short: two silent outcomes in the launch table (F-03, F-04), a secret filter narrower than its comment (F-01, F-02), a guarantee bypassed on the main route (F-09).

### Cross-System Interactions
Six seams audited; findings on four (credentials, the launch table, the identity, the workflows).

### Spec Drift
`device-builds.md`'s stamp sentence (F-05); the brief's two framings (3.3).

### Missing Artifacts
Tests for `get_env`, for the prune and refusal together, and for the launch table's invariants (3.6).

# Packet file: `04-analysis.md`

# Analysis — M6.P2 T5, the build engine

**Date:** 2026-10-24. **Read at:** `reviewed-at: 46f6c7d428`, the slice's bytes `next`'s `8ebaf8daad`; `upstream/next` `3421d7d178`. Findings are `02-forward-audit.md`'s `F-NN`; proofs its `P<n>`. Severity and category are set here and carried to `05`.

## Executive summary

The slice is the engine every build runs: LibreELEC's scripts and `config/functions`, ROCKNIX's distribution layer, and the fork's additions (the watch entry, the identity, the container's lifecycle, the meson guard, the name). **The fork's additions are small, commented and mostly right; the engine's weak points are where a failure is reported as success, or where a guarantee holds on one route and not the one people use.** Nothing was built: every claim is a reading at a site, a sandboxed call with its trace read first (P1 to P8, P11 to P13), an install tree (P7), or a recorded run (P10), and the build-only proofs are `fix-pending-image`.

**21 findings. Two are High:**

- **F-16:** `scripts/mkimage` reports success over an incomplete image on the `qcom-abl` route, SM8550's, the Retroid Pocket Nova's (unchecked copies of the kernel and `SYSTEM`, unchecked compression, an exit status that is always 0).
- **F-18:** `scripts/get_git` accepts a cached clone whose `HEAD` is not the pinned commit when the pin matches any of the clone's refs, and the package then builds from the old source under the new version (P13).

**Eight are Medium:**

- `scripts/get_env` keeps six constructed secret-shaped names (F-01).
- A multi-line value lets a dropped name return through docker's `--env-file` (F-02).
- `add_es_system` carries a system's fragment into the next, so `daphne` and `gp32` ship a wrong year on every image, and the next system appended would launch nothing (F-03).
- The launch table's one-default rule stops a build silently on one shape and ships two defaults on the other (F-04, T3's F-06).
- `build_distro`'s prune defeats the image's refusal to reuse an identity on the documented route (F-09).
- A device-level file `find_file_path` reads is outside the stamp (F-17, P12).
- Archives are fetched without TLS verification and accepted unhashed (F-19).
- `checkdeps` changes the host's compiler and `/nix` with `sudo` (F-20).

**The rest are Low or `Renovation`:** a stale rule (F-05: two items of `device-builds.md` describe defects fixed in August), dead identity code (F-06, F-07), upstream's glob test (F-08), a workflow red on every run (F-10), the options file's two spellings (F-15), small helper defects (F-21), the container pin's age and three files behind upstream (F-11, F-12), and two items #644 assigned (finding 3's sentence, finding 8's measurement).

**Currency (Q4):**

- **Against ROCKNIX:** the slice is level but for three upstream commits, all `to merge` with the next base merge.
- **The container:** the pin is 29 days behind upstream's image of today; the `Dockerfile` is identical.
- **Upstream contributions (#585 candidates):** F-03, F-04, F-08, F-16, F-17, F-18, F-19 and F-20 are upstream's code; D-WORKFLOW-164, with submissions deferred by D-WORKFLOW-165.

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
| an image built from an older source than its recipe names | F-18 | low to medium (a pin bumped to a branch tip a cached clone already knows; the shared cache lives for months) | the image's claimed version is false, and a fix said to ship does not | compare `HEAD` with `PKG_VERSION` |
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

F-01, F-02, F-03, F-04, F-08, F-09, F-16, F-17, F-18, F-19, F-20, F-21 (`02`). The `bug` issues are filed at stage D for the defects that a sandbox, a recorded run or an install tree can verify: F-01 with F-02 (one issue, `get_env`), F-03, F-04, F-09, F-16, F-17, F-18, F-19, F-20. Of these, F-04's issue is T3's lead made this slice's, and F-08 and F-21 stay punch items (Low, upstream's, no shipped effect).

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
The two High fixes first (F-16, F-18), each with its sandbox or trace; then the credential filter (F-01, F-02); then the table (F-03, F-04, proven by the regeneration); then F-09, F-17, F-19, F-20 under stream briefs that name the build proving them.

## Second opinion (Phase 4.6)

**Pending: the Phase 4.6 calls wait for the host.** Depth Extended; two reviewers from two other labs: GPT-6 Astra (`--member gpt`, `max`) and Gemini 4 Argon (`--member gemini-argon`, `high`), refutation pass each, a probe of each seat first (`second-opinions/review-plan.json`, written 2026-10-24 before any call). The `npm install --prefix tools/council` and both calls wait for the M7 host window's return line, relayed on #652; the window opened at 03:47 UTC and was still held at the coordinator's 04:26 census. Until then no Phase 5 item is final and no issue is filed (brief § 8).

## Quality Self-Check

- Every PASS in `02` cites a primary artifact, and says what would have failed it.
- Every finding was re-read at its site, and the subagent's leads were re-read before use. One lead was withdrawn, and seventeen stay leads.
- No build, container, guest or device was used; no credential or log define reached an artifact (every log read went through `readlog`).
- Two of my own errors are recorded, not hidden: stamps written ahead of the clock (corrected at 04:31, a friction line), and two sandbox scripts that wrote beside themselves (corrected before commit).

# Packet file: `q6-tables.md`

# Q6 reachability tables (#652)

Generated from `.qa-scratch/t5/q6-callers.tsv` (the search below) and the readings named per row; `04-analysis.md` § Renovation face Q6 cites this file.

## Table 1: the 30 scripts and their callers

Search per script (2026-10-24, between 04:11 and 04:31 UTC): `git grep -l -F -e "scripts/<n>" -e "SCRIPTS}/<n>" -e "/<n> " -e "/<n>\"" -- . ':!docs' ':!.github/sessions' ':!research' ':!plans' ':!seed'`, the script itself excluded; a zero re-checked with `git grep -l -w -F <n>` before it is a verdict, and then with the dispatch read (`scripts/get` 48 to 53).

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


# Packet: the code at the findings' sites

### `scripts/get_env` lines 1 to 22 (at `8ebaf8daad`)

```
    1  #!/usr/bin/env bash
    2  # Forward the environment into the build container -- minus anything that looks
    3  # like a secret.
    4  #
    5  # The whole exported environment used to go through. On a developer's machine
    6  # that is also their shell: API keys and access tokens for unrelated tools
    7  # landed in a world-readable .env in the worktree and inside every build
    8  # container. The four scraper and achievement credentials EmulationStation
    9  # compiles in are the exception -- they are the reason a build needs a secret
   10  # at all -- so they pass by name; everything else that looks like one is
   11  # dropped. Names, not values, are matched, so a variable holding a secret under
   12  # an innocent name still leaks: keep such things out of the shell that runs
   13  # make, or in ~/.ROCKNIX/options where only the build sees them.
   14  KEEP='^(SCREENSCRAPER_DEV_LOGIN|GAMESDB_APIKEY|CHEEVOS_DEV_LOGIN|HFS_DEV_LOGIN)$'
   15  DROP='(^|_)(KEY|KEYS|TOKEN|TOKENS|SECRET|SECRETS|PASSWORD|PASSWD|CREDENTIAL|CREDENTIALS|AUTH|APIKEY|API_KEY|PRIVATE)($|_)|^(AWS|GH|GITHUB|NPM|OPENAI|ANTHROPIC)_'
   16  for var in $(compgen -e); do
   17    [[ "$var" == PATH ]] && continue
   18    if [[ ! "$var" =~ $KEEP ]] && [[ "$var" =~ $DROP ]]; then
   19      continue
   20    fi
   21    echo "$var=${!var}"
   22  done
```

### `Makefile` lines 126 to 208 (at `8ebaf8daad`)

```
  126  ## Docker builds - overview
  127  # docker-* commands just wire up docker to call the normal make command via docker
  128  # For example: make docker-SM8250 will use docker to call: make SM8250
  129  # All variables are scoped to docker-* commands to prevent weird collisions/behavior with non-docker commands
  130  
  131  # The build container, pinned by digest to the fork's own mirror (#344 P1,
  132  # D-WORKFLOW-119/120): what `docker pull` and `docker run` consume. The digest
  133  # is also handed to the build as BUILDER_VERSION, so every image's
  134  # /etc/os-release says which container it was built in (scripts/image). The
  135  # fork-mirror-build-container workflow refreshes the mirror and prints the
  136  # digest; this line moves with it, by hand. A locally built container is
  137  # tagged (DOCKER_IMAGE_LOCAL), never pinned.
  138  docker-%: DOCKER_IMAGE_DIGEST := sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39
  139  docker-%: DOCKER_IMAGE = ghcr.io/pixelelated/build@$(DOCKER_IMAGE_DIGEST)
  140  docker-%: DOCKER_IMAGE_LOCAL := ghcr.io/pixelelated/build:local
  141  
  142  # DOCKER_WORK_DIR is the directory in the Docker image - it is set to /work by default
  143  #   Anytime this directory changes, you must run `make clean` similarly to moving the distribution directory
  144  docker-%: DOCKER_WORK_DIR := $(shell if [ -n "${DOCKER_WORK_DIR}" ]; then echo ${DOCKER_WORK_DIR}; else echo "$$(pwd)" ; fi)
  145  
  146  # ${HOME}/.ROCKNIX/options is a global options file containing developer and build settings.
  147  docker-%: GLOBAL_SETTINGS := $(shell if [ -f "${HOME}/.ROCKNIX/options" ]; then echo "-v \"${HOME}/.ROCKNIX/options:${HOME}/.ROCKNIX/options\""; else echo ""; fi)
  148  
  149  # LOCAL_SSH_KEYS_FILE is a variable that contains the location of the authorized keys file for development build use.  It will be mounted into the container if it exists.
  150  docker-%: LOCAL_SSH_KEYS_FILE := $(shell if [ -n "${LOCAL_SSH_KEYS_FILE}" ]; then echo "-v \"${LOCAL_SSH_KEYS_FILE}:${LOCAL_SSH_KEYS_FILE}\""; else echo ""; fi)
  151  
  152  # EMULATIONSTATION_SRC is a variable that contains the location of local emulationstation source code. It will be mounted into the container if it exists.
  153  docker-%: EMULATIONSTATION_SRC := $(shell if [ -n "${EMULATIONSTATION_SRC}" ]; then echo "-v \"${EMULATIONSTATION_SRC}:${EMULATIONSTATION_SRC}\""; else echo ""; fi)
  154  
  155  # UID is the user ID of current user - ensures docker sets file permissions properly
  156  docker-%: UID := $(shell id -u)
  157  
  158  # GID is the main user group of current user - ensures docker sets file permissions properly
  159  docker-%: GID := $(shell id -g)
  160  
  161  # PWD is 'present working directory' and passes through the full path to current dir to docker (becomes 'work')
  162  docker-%: PWD := $(shell pwd)
  163  
  164  # Command to use (either `docker` or `podman`)
  165  docker-%: DOCKER_CMD:= $(shell if which docker 2>/dev/null 1>/dev/null; then echo "docker"; elif which podman 2>/dev/null 1>/dev/null; then echo "podman"; fi)
  166  
  167  # Podman requires some extra args (`--userns=keep-id` and `--security-opt=label=disable`).  Set those args if using podman
  168  #   Make sure that docker isn't just an alias for podman
  169  docker-%: PODMAN_ARGS:= $(shell if echo "$$(docker --version 2>/dev/null || podman --version 2>/dev/null )" | grep podman 1>/dev/null ; then echo "--userns=keep-id --security-opt=label=disable -v /proc/mounts:/etc/mtab"; fi)
  170  
  171  # Launch docker as interactive if this is an interactive shell (allows ctrl-c for manual and running non-interactive - aka: build server)
  172  docker-%: INTERACTIVE=$(shell [ -t 0 ] && echo "-it")
  173  
  174  # By default pass through anything after `docker-` back into `make`
  175  docker-%: COMMAND=make $*
  176  
  177  # Record from outside Docker so a container exit cannot erase its monitor.
  178  # Direct native scripts use the same runner; nested builds inherit its run.
  179  docker-%: BUILD_WATCH=$(if $(filter shell clean distclean package-clean update kconfig-%,$*),,./tools/watch-build --docker --)
  180  
  181  # If the user issues a `make docker-shell` just start up bash as the shell to run commands
  182  docker-shell: COMMAND=bash
  183  
  184  # Command: builds and saves a docker builder image locally.
  185  # The build user must also be a member of the "docker" group.
  186  docker-image-build:
  187  	$(DOCKER_CMD) buildx create --use
  188  	$(DOCKER_CMD) buildx build --tag $(DOCKER_IMAGE_LOCAL) --platform $(shell if [ "$$(uname -m)" = "aarch64" ]; then echo "linux/arm64"; else echo "linux/amd64"; fi) --load .
  189  
  190  # Command: pulls the pinned build container from the fork's mirror, by digest.
  191  docker-image-pull:
  192  	$(DOCKER_CMD) pull $(DOCKER_IMAGE)
  193  
  194  # Wire up docker to call equivalent make files using % to match and $* to pass the value matched by %
  195  # .env carries the forwarded environment into the container, credentials
  196  # included when a build has them (scripts/get_env drops the rest). It is
  197  # written here, in the recipe, and not as a prerequisite: a $(shell) there
  198  # ran whenever make read this file, for any target. rm first, so an older
  199  # copy's mode is never reused and umask 077 makes it owner-only -- and an
  200  # older copy that cannot be removed stops the recipe, since umask does not
  201  # tighten a file that already exists (set -C refuses to write into one); the
  202  # trap removes it when the container exits or the recipe is interrupted, and
  203  # a get_env that fails starts no container.
  204  docker-%:
  205  	rm -f .env && [ ! -e .env ] || { echo "an older .env cannot be removed: no container started" >&2; exit 1; }; \
  206  	trap 'rm -f .env' EXIT; trap 'exit 130' INT TERM HUP; \
  207  	( umask 077 && set -C && ./scripts/get_env > .env ) || { echo "scripts/get_env failed: no container started" >&2; exit 1; }; \
  208  	BUILD_DIR=$(DOCKER_WORK_DIR) $(BUILD_WATCH) $(DOCKER_CMD) run $(PODMAN_ARGS) $(INTERACTIVE) --init --env-file .env -e RASTERATOPS_BUILD_RUN -e PROJECT -e DEVICE -e ARCH -e BUILDER_NAME=pixelelated-build -e BUILDER_VERSION=$(DOCKER_IMAGE_DIGEST) --rm --user $(UID):$(GID) $(GLOBAL_SETTINGS) $(LOCAL_SSH_KEYS_FILE) $(EMULATIONSTATION_SRC) -v $(PWD):$(DOCKER_WORK_DIR) -w $(DOCKER_WORK_DIR) $(DOCKER_EXTRA_OPTS) $(DOCKER_IMAGE) $(COMMAND)
```

### `distributions/ROCKNIX/config/functions` lines 95 to 219 (at `8ebaf8daad`)

```
   95    echo "${2}|${3}|${4}" >>${ESTMP}/${1}-emulators.tmp
   96    add_emu_doc $*
   97  }
   98  
   99  mk_es_systems() {
  100  
  101    cat <<EOF >${ESTMP}/.es_systems.cfg
  102  <?xml version="1.0" encoding="UTF-8"?>
  103  <systemList>
  104  EOF
  105    rm -f ${ESTMP}/*-emulators.tmp
  106    for essystem in $(ls ${ESTMP}/*.tmp | sort)
  107    do
  108      cat ${essystem} >>${ESTMP}/.es_systems.cfg
  109    done
  110    cat <<EOF >>${ESTMP}/.es_systems.cfg
  111  </systemList>
  112  EOF
  113  xmlstarlet fo -t ${ESTMP}/.es_systems.cfg >${ESTMP}/es_systems.cfg 2>/dev/null
  114  
  115  }
  116  
  117  add_system_dir() {
  118    if [ ! -d "${ESTMP}" ]
  119    then
  120      mkdir -p "${ESTMP}"
  121    fi
  122    cat <<EOF >>${ESTMP}/system-dirs.conf
  123  d	${1}			0777 root root - -
  124  EOF
  125  }
  126  
  127  add_es_system() {
  128    RUNCMD='/usr/bin/runemu.sh %ROM% -P%SYSTEM% --core=%CORE% --emulator=%EMULATOR% --controllers="%CONTROLLERSCONFIG%"'
  129    if [ -e "${ROOT}/config/emulators/${1}.conf" ]
  130    then
  131      . ${ROOT}/config/emulators/${1}.conf
  132    fi
  133  
  134    if [ ! -d "${ESTMP}" ]
  135    then
  136      mkdir -p "${ESTMP}"
  137    fi
  138    if [[ -z "${SYSTEM_COMMAND}" ]];
  139    then
  140      SYSTEM_COMMAND=$RUNCMD
  141    fi
  142    if [ ! -e "${ESTMP}/${SYSTEM_NAME}.tmp" ]
  143    then
  144      cat <<EOF >${ESTMP}/${SYSTEM_NAME}.tmp
  145  <system>
  146  	<name>${SYSTEM_NAME}</name>
  147  	<fullname>${SYSTEM_FULLNAME}</fullname>
  148  	<manufacturer>${SYSTEM_MANUFACTURER}</manufacturer>
  149  	<release>${SYSTEM_RELEASE}</release>
  150  	<hardware>${SYSTEM_HARDWARE}</hardware>
  151  	<path>${SYSTEM_PATH}</path>
  152  	<extension>${SYSTEM_EXTENSION}</extension>
  153  	<command>${SYSTEM_COMMAND}</command>
  154  	<platform>${SYSTEM_PLATFORM}</platform>
  155  	<theme>${SYSTEM_THEME}</theme>
  156  </system>
  157  EOF
  158    fi
  159  
  160    add_system_dir "${SYSTEM_PATH}"
  161  
  162    if [ -e "${ESTMP}/${SYSTEM_NAME}-emulators.tmp" ]
  163    then
  164      while read -r line
  165      do
  166        SYSTEM_EMULATOR=$(echo ${line} | awk 'BEGIN {FS="|"} {print $1}')
  167        SYSTEM_CORE=$(echo ${line} | awk 'BEGIN {FS="|"} {print $2}')
  168        SYSTEM_DEFAULT=$(echo ${line} | awk 'BEGIN {FS="|"} {print $3}')
  169  
  170        ### Check to see if we've already added an emulator key.
  171        EMTEST=$(xmlstarlet sel -t -c "//system/emulators" ${ESTMP}/${SYSTEM_NAME}.tmp 2>/dev/null ||:)
  172        if [ -z "${EMTEST}" ]
  173        then
  174          ### Add the emulator element
  175          xmlstarlet ed --omit-decl --inplace \
  176            -s "//system" -t elem -n "emulators" -v "" \
  177            ${ESTMP}/${SYSTEM_NAME}.tmp 2>&1 >/dev/null
  178        fi
  179  
  180        ### Check to see if we've already added an emulator key.
  181        EETEST=$(xmlstarlet sel -t -c "//system/emulators/emulator[@name=\"${SYSTEM_EMULATOR}\"]" ${ESTMP}/${SYSTEM_NAME}.tmp 2>/dev/null ||:)
  182        if [ -z "${EETEST}" ]
  183        then
  184          ### Add the emulator element
  185          xmlstarlet ed --omit-decl --inplace \
  186            -s "//system/emulators" -t elem -n "emulator" -v "" \
  187            ${ESTMP}/${SYSTEM_NAME}.tmp 2>&1 >/dev/null
  188        fi
  189  
  190        ### Add an attribute defining the emulator's name.
  191        xmlstarlet ed --omit-decl --inplace \
  192            -s "//system/emulators/emulator[not(@name)]" -t attr -n "name" -v "${SYSTEM_EMULATOR}" \
  193            ${ESTMP}/${SYSTEM_NAME}.tmp 2>&1 >/dev/null
  194  
  195        ### Check to see if we've already added a core element.
  196        COTEST=$(xmlstarlet sel -t -c "//system/emulators/emulator[@name=\"${SYSTEM_EMULATOR}\"]/cores/core" ${ESTMP}/${SYSTEM_NAME}.tmp 2>/dev/null ||:)
  197        if [ -z "${COTEST}" ]
  198        then
  199          xmlstarlet ed --omit-decl --inplace \
  200              -s "//system/emulators/emulator[@name=\"${SYSTEM_EMULATOR}\"]" -t elem -n "cores" -v "" \
  201              ${ESTMP}/${SYSTEM_NAME}.tmp 2>&1 >/dev/null
  202        fi
  203  
  204        ### Add each core.
  205        xmlstarlet ed --omit-decl --inplace \
  206            -s "//system/emulators/emulator[@name=\"${SYSTEM_EMULATOR}\"]/cores" -t elem -n "core" -v "${SYSTEM_CORE}" \
  207            ${ESTMP}/${SYSTEM_NAME}.tmp 2>&1 >/dev/null
  208  
  209        if [ "${SYSTEM_DEFAULT}" = "true" ]
  210        then
  211          ### Add an attribute defining the default core
  212          xmlstarlet ed --omit-decl --inplace \
  213              -i "//system/emulators/emulator[@name=\"${SYSTEM_EMULATOR}\"]/cores/core" -t attr -n "default" -v "true" \
  214              ${ESTMP}/${SYSTEM_NAME}.tmp 2>&1 >/dev/null
  215        fi
  216      done <${ESTMP}/${SYSTEM_NAME}-emulators.tmp
  217    fi
  218    add_system_doc ${SYSTEM_NAME}
  219  }
```

### `scripts/mkimage` lines 1 to 60 (at `8ebaf8daad`)

```
    1  #!/bin/bash
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    5  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
    6  
    7  ################################################################################
    8  # variables such as ${ROOT} ${PATH} etc... that are required for this
    9  # script to work must be passed via env ... in scripts/image
   10  ################################################################################
   11  
   12  # set variables
   13  IMG_TMP=$(mktemp -d -p ${TARGET_IMG})
   14  SAVE_ERROR="${IMG_TMP}/save_error"
   15  
   16  if [ -z "${SYSTEM_SIZE}" -o -z "${SYSTEM_PART_START}" ]; then
   17    echo "mkimage: SYSTEM_SIZE and SYSTEM_PART_START must be configured!"
   18    exit 1
   19  fi
   20  
   21  DISK_START_PADDING=$(((${SYSTEM_PART_START} + 2048 - 1) / 2048))
   22  DISK_GPT_PADDING=1
   23  DISK_SIZE=$((${DISK_START_PADDING} + ${SYSTEM_SIZE} + ${STORAGE_SIZE} + ${DISK_GPT_PADDING}))
   24  DISK_BASENAME="${TARGET_IMG}/${IMAGE_NAME}"
   25  if [ -n "${SUBDEVICE}" ]; then
   26    DISK_BASENAME="${DISK_BASENAME}-${SUBDEVICE}"
   27  fi
   28  DISK="${DISK_BASENAME}.img"
   29  
   30  # functions
   31  cleanup() {
   32    echo -e "image: cleanup...\n"
   33    rm -rf "${IMG_TMP}"
   34  }
   35  
   36  show_error() {
   37    echo "image: An error has occurred..."
   38    echo
   39    if [ -s "${SAVE_ERROR}" ]; then
   40      cat "${SAVE_ERROR}"
   41    else
   42      echo "Folder ${IMG_TMP} might be out of free space..."
   43    fi
   44    echo
   45    cleanup
   46    exit 1
   47  }
   48  
   49  trap cleanup SIGINT
   50  
   51  # create an image
   52  echo -e "\nimage: creating sparse file for disk image ${DISK##*/}..."
   53  dd if=/dev/zero of="${DISK}" bs=1M count=0 seek="${DISK_SIZE}" conv=fsync >"${SAVE_ERROR}" 2>&1 || show_error
   54  
   55  if [ -n "${PARTITION_TABLE:-}" ]; then
   56    DISK_LABEL="${PARTITION_TABLE}"
   57  elif [ "${BOOTLOADER}" = "syslinux" ]; then
   58    DISK_LABEL=gpt
   59  else
   60    DISK_LABEL=msdos
```

### `scripts/mkimage` lines 160 to 334 (at `8ebaf8daad`)

```
  160          search --set -f /KERNEL
  161          linux /KERNEL boot=LABEL=${DISTRO_BOOTLABEL} disk=LABEL=${DISTRO_DISKLABEL} grub_portable ${EXTRA_CMDLINE}
  162  }
  163  EOF
  164  
  165    mcopy "${IMG_TMP}/syslinux.cfg" :: >"${SAVE_ERROR}" 2>&1 || show_error
  166  
  167    # install syslinux
  168    echo "image: installing syslinux to part1..."
  169    syslinux.mtools -i "${IMG_TMP}/part1.fat" >"${SAVE_ERROR}" 2>&1 || show_error
  170  
  171    # copy files
  172    echo "image: copying files to part1..."
  173    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}" >"${SAVE_ERROR}" 2>&1 || show_error
  174    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM >"${SAVE_ERROR}" 2>&1 || show_error
  175    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5" >"${SAVE_ERROR}" 2>&1 || show_error
  176    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5 >"${SAVE_ERROR}" 2>&1 || show_error
  177  
  178    mmd EFI EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
  179    mcopy "${TOOLCHAIN}/share/syslinux/bootx64.efi" ::/EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
  180    mcopy "${TOOLCHAIN}/share/syslinux/ldlinux.e64" ::/EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
  181    mcopy "${IMG_TMP}/grub.cfg" ::/EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
  182  
  183  elif [ "${BOOTLOADER}" = "bcm2835-bootloader" ]; then
  184    # create bootloader configuration
  185    echo "image: creating bootloader configuration..."
  186    cat <<EOF >"${IMG_TMP}/cmdline.txt"
  187  boot=UUID=${UUID_SYSTEM} disk=UUID=${UUID_STORAGE} quiet ${EXTRA_CMDLINE}
  188  EOF
  189  
  190    mcopy "${IMG_TMP}/cmdline.txt" :: >"${SAVE_ERROR}" 2>&1 || show_error
  191  
  192    # copy files
  193    echo "image: copying files to part1..."
  194    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}" >"${SAVE_ERROR}" 2>&1 || show_error
  195    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM >"${SAVE_ERROR}" 2>&1 || show_error
  196    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5" >"${SAVE_ERROR}" 2>&1 || show_error
  197    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5 >"${SAVE_ERROR}" 2>&1 || show_error
  198  
  199    for f in bootcode.bin fixup.dat start.elf; do
  200      if [ -f "${RELEASE_DIR}/3rdparty/bootloader/$f" ]; then
  201        mcopy "${RELEASE_DIR}/3rdparty/bootloader/$f" :: >"${SAVE_ERROR}" 2>&1 || show_error
  202      fi
  203    done
  204  
  205    mcopy "${RELEASE_DIR}/3rdparty/bootloader/config.txt" :: >"${SAVE_ERROR}" 2>&1 || show_error
  206    for distro in "${RELEASE_DIR}/3rdparty/bootloader/distroconfig"*.txt; do
  207      if [ -f "${distro}" ]; then
  208        mcopy "${distro}" ::/"${distro##*/}" >"${SAVE_ERROR}" 2>&1 || show_error
  209      fi
  210    done
  211  
  212    for dtb in "${RELEASE_DIR}/3rdparty/bootloader/"*.dtb; do
  213      if [ -f "${dtb}" ]; then
  214        mcopy "${dtb}" ::/"${dtb##*/}" >"${SAVE_ERROR}" 2>&1 || show_error
  215      fi
  216    done
  217  
  218    if [ -d "${RELEASE_DIR}/3rdparty/bootloader/overlays" ]; then
  219      mcopy -s "${RELEASE_DIR}/3rdparty/bootloader/overlays" :: >"${SAVE_ERROR}" 2>&1 || show_error
  220    fi
  221  
  222  elif [ "${BOOTLOADER}" = "u-boot" ]; then
  223    # create bootloader configuration
  224    echo "image: creating bootloader configuration... (u-boot)"
  225    if [ -f "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage" ]; then
  226      . "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage"
  227    elif [ -f "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage" ]; then
  228      . "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage"
  229    else
  230      echo "image: skipping u-boot. no mkimage script found"
  231    fi
  232  
  233    echo "image: copying files to part1..."
  234    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}" >"${SAVE_ERROR}" 2>&1 || show_error
  235    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM >"${SAVE_ERROR}" 2>&1 || show_error
  236    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5" >"${SAVE_ERROR}" 2>&1 || show_error
  237    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5 >"${SAVE_ERROR}" 2>&1 || show_error
  238  
  239  elif [ "${BOOTLOADER}" = "arm-efi" ]; then
  240    # create bootloader configuration
  241    echo "image: creating bootloader configuration... (arm-efi)"
  242    if [ -f "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage" ]; then
  243      . "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage"
  244    elif [ -f "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage" ]; then
  245      . "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage"
  246    else
  247      echo "image: skipping arm-efi. no mkimage script found"
  248    fi
  249  
  250    # copy files
  251    echo "image: copying files to part1..."
  252    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}"
  253    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM
  254    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5"
  255    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5
  256  
  257  elif [ "${BOOTLOADER}" = "qcom-abl" ]; then
  258    # create bootloader configuration
  259    echo "image: creating bootloader configuration... (qcom-abl)"
  260    if [ -f "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage" ]; then
  261      . "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage"
  262    elif [ -f "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage" ]; then
  263      . "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage"
  264    else
  265      echo "image: skipping qcom-abl. no mkimage script found"
  266    fi
  267  
  268    # copy files
  269    echo "image: copying files to part1..."
  270    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}"
  271    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM
  272    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5"
  273    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5
  274  
  275  fi # bootloader
  276  
  277  # run fsck
  278  echo "image: checking filesystem on part1..."
  279  sync
  280  fsck.fat -n "${IMG_TMP}/part1.fat" >"${SAVE_ERROR}" 2>&1 || show_error
  281  
  282  # merge part1 into disk image
  283  echo "image: merging part1 into disk image..."
  284  dd if="${IMG_TMP}/part1.fat" of="${DISK}" bs=512 seek="${SYSTEM_PART_START}" conv=fsync,notrunc >"${SAVE_ERROR}" 2>&1 || show_error
  285  
  286  # finalize virtual appliance
  287  if [ "${PROJECT}" = "Generic" ]; then
  288    # change syslinux default to 'run'
  289    echo "image: modifying files on part1 for open virtual appliance..."
  290    sed -e "/DEFAULT/ s/installer/run/" -i "${IMG_TMP}/syslinux.cfg"
  291    sed -e "/set default=/s/\"Installer\"/\"Run\"/" -i "${IMG_TMP}/grub.cfg"
  292    mcopy "${IMG_TMP}/syslinux.cfg" :: >"${SAVE_ERROR}" 2>&1 || show_error
  293    mcopy "${IMG_TMP}/grub.cfg" ::/EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
  294    sync
  295    # run fsck
  296    echo "image: checking filesystem on part1..."
  297    fsck.fat -n "${IMG_TMP}/part1.fat" >"${SAVE_ERROR}" 2>&1 || show_error
  298    # merge modified part1 into tmp disk image
  299    echo "image: merging part1 into open virtual appliance..."
  300    dd if="${IMG_TMP}/part1.fat" of="${DISK_BASENAME}.tmp" bs=512 seek="${SYSTEM_PART_START}" conv=fsync,notrunc >"${SAVE_ERROR}" 2>&1 || show_error
  301    # create vmdk from tmp ${DISK}
  302    echo "image: creating vmdk for open virtual appliance..."
  303    qemu-img convert -O vmdk -o subformat=streamOptimized "${DISK_BASENAME}.tmp" "${DISK_BASENAME}.vmdk"
  304    # generate ovf from template
  305    sed -e "s,@DISTRO@,${DISTRO},g" \
  306      -e "s,@DISTRO_HOME_URL@,${DISTRO_HOME_URL},g" \
  307      -e "s,@DISK@,${IMAGE_NAME},g" \
  308      -e "s,@OVA_SIZE@,$((${OVA_SIZE} * 1024 * 1024)),g" \
  309      "${PROJECT_DIR}/${PROJECT}/config/ovf.template" >"${DISK_BASENAME}.ovf"
  310    # combine ovf and vmdk into official ova
  311    tar -C "${TARGET_IMG}" -cf "${DISK_BASENAME}.ova" "${IMAGE_NAME}.ovf" "${IMAGE_NAME}.vmdk"
  312    # create sha256 checksum of ova image
  313    (
  314      cd "${TARGET_IMG}"
  315      sha256sum "${IMAGE_NAME}.ova" >"${IMAGE_NAME}.ova.sha256"
  316    )
  317    echo "image: cleaning up open virtual appliance..."
  318    # remove tmp ${DISK}, vmdk and ovf
  319    rm "${DISK_BASENAME}.tmp" "${DISK_BASENAME}.vmdk" "${DISK_BASENAME}.ovf"
  320  fi
  321  
  322  # gzip
  323  echo "image: compressing..."
  324  pigz --best --force "${DISK}"
  325  
  326  # create sha256 checksum of image
  327  (
  328    cd "${TARGET_IMG}"
  329    sha256sum "${DISK##*/}.gz" >"${DISK##*/}.gz.sha256"
  330  )
  331  
  332  # cleanup
  333  cleanup
  334  exit
```

### `scripts/get_git` lines 1 to 60 (at `8ebaf8daad`)

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-only
    3  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
    4  
    5  # Handler for git
    6  # Usage (in package.mk):
    7  # PKG_URL (mandatory) must point to a git repository (git://... or https://example.com/repo.git)
    8  # PKG_VERSION (mandatory) must point to a commit SHA, e.g. a1b2c3d
    9  # PKG_GIT_SHA (optional) full hash of git commit
   10  # PKG_GIT_CLONE_BRANCH (optional) clone specific branch
   11  # PKG_GIT_CLONE_SINGLE (optional) clone single branch only (set to yes)
   12  # PKG_GIT_CLONE_DEPTH (optional) history to clone, must be a number
   13  # PKG_GIT_SUBMODULE_DEPTH (optional) history of submodules to clone, must be a number
   14  
   15  set -e
   16  set -o pipefail
   17  
   18  
   19  #_debug=true
   20  if [[ "${_debug}" ]] ; then
   21    export PS4='+${BASH_SOURCE}:${LINENO}: '
   22    set -x
   23  fi
   24  
   25  
   26  _clean_repo() {
   27    git clean -fdx
   28    git restore --staged . || git switch --force # Clear changes and ensure correct branch
   29  }
   30  
   31  _repo_exists_and_valid() {
   32    if [[ -d "${PACKAGE}" ]]; then
   33      pushd "${PACKAGE}" > /dev/null
   34      _clean_repo || return 1
   35  
   36      if ! git ls-remote . | grep -q -m1 "^${PKG_VERSION}"; then
   37        echo "ERROR: ${PACKAGE}: failed to determine git HEAD" >&2
   38        return 1
   39      fi
   40  
   41      if [[ "${PKG_URL}" != "$(git remote get-url origin)" ]]; then
   42        echo "ERROR: ${PACKAGE}: failed to obtain URL of origin" >&2
   43        return 1
   44      fi
   45  
   46      if [[ -n "${PKG_GIT_CLONE_BRANCH}" && "${PKG_GIT_CLONE_BRANCH}" != "$(git rev-parse --abbrev-ref HEAD)" ]]; then
   47        echo "ERROR: ${PACKAGE}: failed to determine current git branch" >&2
   48        return 1
   49      fi
   50  
   51      popd > /dev/null
   52      return 0
   53    fi
   54    return 1
   55  }
   56  
   57  _update_submodules() {
   58    if [[ -n "${GIT_SUBMODULE_PARAMS}" ]]; then
   59      submodules=$(git config --file .gitmodules --get-regexp path | awk '{ print $2 }')
   60    else
```

### `scripts/get_git` lines 190 to 239 (at `8ebaf8daad`)

```
  190    done
  191  }
  192  
  193  
  194  main(){
  195    # Acquire lock on source dir
  196    lock_source_dir "${1}"
  197  
  198    # Check if repo already exists and is valid
  199    _repo_exists_and_valid && exit 0
  200  
  201    if [[ "${PKG_USETOKEN}" == "yes" && -n "${ROCKNIX_GHTOKEN}" ]]; then
  202      PKG_URL="${PKG_URL/https:\/\//https:\/\/${ROCKNIX_GHTOKEN}@}"
  203    fi
  204  
  205    # If not valid, proceed to get the repo
  206    build_msg "CLR_GET" "GET" "${1} (git)" "indent"
  207  
  208    # Remove stale stamps
  209    rm -f "${STAMP_URL}" "${STAMP_SHA}"
  210  
  211    # Clone or update the repository
  212    _get_repo || exit 1
  213  
  214    # Verify the git hash 
  215    GIT_SHA=""
  216    while IFS=$'\t' read -r sha ref; do
  217      if [[ "$ref" == "HEAD" ]]; then
  218        GIT_SHA="$sha"
  219        break
  220      fi
  221    done < <(git ls-remote "${PACKAGE}")
  222  
  223    # Check if GIT_SHA was successfully retrieved
  224    if [[ -z "$GIT_SHA" ]]; then
  225      echo "Failed to retrieve GIT_SHA." >&2
  226      exit 1
  227    fi
  228  
  229    # Verify that the retrieved SHA matches the expected one
  230    if [[ -n "${PKG_GIT_SHA}" && "${PKG_GIT_SHA}" != "${GIT_SHA}" ]]; then
  231      build_msg "CLR_WARNING" "WARNING" "Incorrect git hash in repository: got ${GIT_SHA}, wanted ${PKG_GIT_SHA}" >&2
  232      exit 1
  233    fi
  234  
  235    echo "Repository setup completed successfully."
  236  }
  237  
  238  
  239  main
```

### `scripts/get_archive` lines 1 to 59 (at `8ebaf8daad`)

```
    1  # SPDX-License-Identifier: GPL-2.0-only
    2  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
    3  
    4  _get_file_already_downloaded() {
    5    { [ ! -f "${PACKAGE}" ] || [ ! -f "${STAMP_URL}" ] || [ ! -f "${STAMP_SHA}" ]; } && return 1
    6    { [ -n "${PKG_SHA256}" ] && [ "$(cat ${STAMP_SHA} 2>/dev/null)" != "${PKG_SHA256}" ]; } && return 1
    7    return 0
    8  }
    9  
   10  # Latest file already present, exit now...
   11  _get_file_already_downloaded && exit 0
   12  
   13  lock_source_dir "${1}"
   14  
   15  # Check again in case of concurrent access - if nothing needs to be downloaded, exit now...
   16  _get_file_already_downloaded && exit 0
   17  
   18  # At this point, we need to download something...
   19  build_msg "CLR_GET" "GET" "${1} (archive)" "indent"
   20  
   21  pkg_lock_status "GETPKG" "${PKG_NAME}" "unpack" "downloading package..."
   22  
   23  PACKAGE_MIRROR="${DISTRO_MIRROR}/${PKG_SOURCE_NAME}"
   24  [ "${VERBOSE}" != "yes" ] && WGET_OPT=-q
   25  WGET_CMD="wget --secure-protocol=TLSv1_2 --output-file=- --timeout=30 --tries=3 --passive-ftp --no-check-certificate -c ${WGET_OPT} --progress=bar:force --retry-connrefused --waitretry=5 --retry-on-http-error=429,500,502,503,504 --show-progress -O ${PACKAGE}"
   26  
   27  # unset LD_LIBRARY_PATH to stop wget from using toolchain/lib and loading libssl.so/libcrypto.so instead of host libraries
   28  unset LD_LIBRARY_PATH
   29  
   30  rm -f "${STAMP_URL}" "${STAMP_SHA}"
   31  
   32  PKG_URLS="${PKG_URL}"
   33  if [ -n "${PACKAGE_MIRROR}" ]
   34  then
   35    PKG_URLS="${PKG_URL} ${PACKAGE_MIRROR}"
   36  fi
   37  
   38  NBWGET=10
   39  while [ ${NBWGET} -gt 0 ]; do
   40    for url in ${PKG_URLS}; do
   41      rm -f "${PACKAGE}"
   42      if ${WGET_CMD} "${url}"; then
   43        CALC_SHA256=$(sha256sum "${PACKAGE}" | cut -d" " -f1)
   44  
   45        [ -z "${PKG_SHA256}" -o "${PKG_SHA256}" = "${CALC_SHA256}" ] && break 2
   46  
   47        build_msg "CLR_WARNING" "WARNING" "Incorrect checksum calculated on downloaded file: got ${CALC_SHA256} wanted ${PKG_SHA256}"
   48      fi
   49    done
   50    NBWGET=$((NBWGET - 1))
   51  done
   52  
   53  if [ ${NBWGET} -eq 0 ]; then
   54    die "\nCannot get ${1} sources : ${PKG_URL}\nTry later!"
   55  else
   56    build_msg "CLR_INFO" "INFO" "Calculated checksum: ${CALC_SHA256}"
   57    echo "${PKG_URL}" > "${STAMP_URL}"
   58    echo "${CALC_SHA256}" > "${STAMP_SHA}"
   59  fi
```

### `scripts/update_packages` lines 40 to 66 (at `8ebaf8daad`)

```
   40        if [ "${UPS_VERSION}" ]; then
   41          echo "${PKG_NAME} updated from ${PKG_VERSION} to ${UPS_VERSION}"
   42          sed -i "s/PKG_VERSION=\"${PKG_VERSION}/PKG_VERSION=\"${UPS_VERSION}/" $f
   43        else
   44          echo "Could not find version, not updating ${PKG_NAME}."
   45        fi
   46      fi
   47  
   48      if [[ ! "${PKG_URL}" =~ git$ ]]
   49      then
   50       if grep -q PKG_SHA256 "${f}"; then
   51         echo "PKG_SHA256 exists on ${f}, clearing"
   52         sed -i "/PKG_SHA256=.*\$/d" ${f}
   53       fi
   54       source "${f}"
   55       ./scripts/get "${PKG_NAME}" >/dev/null
   56       if [ "${p}" != "linux" ]; then
   57         SHA=$(cat ./${SOURCES}/${PKG_NAME}/${PKG_NAME}-${UPS_VERSION}.*.sha256 2>/dev/null ||:)
   58       else
   59         SHA=$(cat ./${SOURCES}/${PKG_NAME}/linux-$LINUX-${UPS_VERSION}.tar.gz.sha256 2>/dev/null ||:)
   60       fi
   61       sed -e "/PKG_VERSION=\"${UPS_VERSION}\"/{ N; s/PKG_VERSION=\"${UPS_VERSION}\".*PKG_SHA256=\"\"/PKG_VERSION=\"${UPS_VERSION}\"\nPKG_SHA256=\"${SHA}\"/;}" -i ${f}
   62     else
   63       sed "/^PKG_SHA256=/d" -i ${f}
   64     fi
   65    done
   66  }
```

### `scripts/build_distro` lines 1 to 106 (at `8ebaf8daad`)

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  ###
    6  ### Simple script to build ROCKNX
    7  ###
    8  
    9  # Fork build monitoring: nested calls reuse the outer run (#394).
   10  if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
   11    exec ./tools/watch-build --entry -- "$0" "$@"
   12  fi
   13  unset RASTERATOPS_WATCH_EXEC
   14  
   15  set -e
   16  
   17  scripts/checkdeps
   18  
   19  if [ -z "${ARCH}" ]; then
   20    echo "Please export ARCH before building."
   21    exit 1
   22  fi
   23  
   24  . config/options ""
   25  . projects/${PROJECT}/devices/${DEVICE}/options
   26  
   27  echo "Building ${DISTRO} for ${DEVICE}"
   28  
   29  # Collect packages to clean
   30  PKG_CLEAN=""
   31  
   32  if [ "${ENABLE_32BIT}" == "true" ]; then
   33    PKG_CLEAN+=" ${CLEAN_EMU_32BIT}"
   34  fi
   35  
   36  if [ "${WINDOWMANAGER}" == "weston" ]; then
   37    PKG_CLEAN+=" ${CLEAN_WESTON}"
   38  fi
   39  
   40  # Handle DEVICE_ROOT logic
   41  if [ -n "${DEVICE_ROOT}" ]; then
   42    if [ "${DEVICE_ROOT}" != "${DEVICE}" ]; then
   43      # Remove existing build directory if present
   44      if [ -d "build.${DISTRONAME}-${DEVICE}.${ARCH}" ]; then
   45        echo "Removing stale build root."
   46        rm -rf build.${DISTRONAME}-${DEVICE}.${ARCH}
   47      fi
   48  
   49      # Ensure DEVICE_ROOT is built before DEVICE
   50      if [ ! -d "build.${DISTRONAME}-${DEVICE_ROOT}.${ARCH}" ]; then
   51        echo "ERROR: Can't find build root build.${DISTRONAME}-${DEVICE_ROOT}.${ARCH}"
   52        echo "You need to build ${DEVICE_ROOT} before ${DEVICE}"
   53        exit 1
   54      fi
   55  
   56      # Link build directory to DEVICE_ROOT
   57      if [ ! -L "build.${DISTRONAME}-${DEVICE}.${ARCH}" ]; then
   58        ln -sf build.${DISTRONAME}-${DEVICE_ROOT}.${ARCH} build.${DISTRONAME}-${DEVICE}.${ARCH}
   59      fi
   60  
   61      # Link sources if necessary
   62      if [ -d "sources-${DEVICE_ROOT}" ] && [ ! -L "sources-${DEVICE}" ]; then
   63        ln -sf sources-${DEVICE_ROOT} sources-${DEVICE}
   64      fi
   65    fi
   66    PKG_CLEAN+=" ${CLEAN_DEVICE_ROOT}"
   67  fi
   68  
   69  # Add standard packages to clean
   70  PKG_CLEAN+=" ${CLEAN_NETWORK} ${CLEAN_OS_BASE} ${CLEAN_PACKAGES}"
   71  
   72  if [ -z "${DIRTY}" ]; then
   73    # Clean packages to ensure build date and version are updated
   74    for package in ${PKG_CLEAN}; do
   75      echo "Clean: ${package}"
   76      ./scripts/clean "${package}" 2>/dev/null || true
   77    done
   78    rm -rf build.${DISTRONAME}-${DEVICE_ROOT}.${ARCH}/{.stamps/initramfs,initramfs}
   79  fi
   80  
   81  # Prune old releases
   82  echo "Prune old releases: ${DISTRONAME}-${DEVICE}.${ARCH}-*"
   83  rm -f ./release/${DISTRONAME}-${DEVICE}.${ARCH}-*
   84  rm -rf ./target/${DISTRONAME}-${DEVICE}.${ARCH}-*
   85  
   86  # Remove image root
   87  rm -rf ./build.${DISTRONAME}-${DEVICE}.${ARCH}/image
   88  
   89  case "${ARCH}" in
   90    arm)
   91      if [ "${BASE_ONLY}" == "true" ] || [ "${ENABLE_32BIT}" != "true" ]; then
   92        exit 0
   93      fi
   94      export PKG_BUILD_PERF=no
   95      scripts/build_compat arm
   96      scripts/install arm
   97      ;;
   98    *)
   99      make image
  100      ;;
  101  esac
  102  
  103  if [ $? -ne 0 ]; then
  104    echo "Build failed..exiting."
  105    exit 1
  106  fi
```

### `scripts/checkdeps` lines 290 to 345 (at `8ebaf8daad`)

```
  290      echo "The command 'sudo' was not found. Please install necessary packages manually."
  291      exit 1
  292    fi
  293  fi
  294  
  295  # Configure gcc-12/g++-12 as default via update-alternatives (Debian/Ubuntu)
  296  case "${DISTRO}" in
  297    ubuntu|debian)
  298      if command -v gcc-12 >/dev/null && command -v sudo >/dev/null; then
  299        if ! update-alternatives --query gcc >/dev/null 2>&1 || \
  300           ! update-alternatives --query gcc 2>/dev/null | grep -q "gcc-12"; then
  301          echo "Setting gcc-12/g++-12 as default via update-alternatives..."
  302          sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100 \
  303            --slave /usr/bin/g++ g++ /usr/bin/g++-12 \
  304            --slave /usr/bin/gcov gcov /usr/bin/gcov-12
  305          sudo update-alternatives --set gcc /usr/bin/gcc-12
  306        fi
  307      fi
  308      ;;
  309  esac
  310  
  311  # check if installed packages satisfied deps
  312  get_deps
  313  
  314  if [ "${#need_map[@]}" -gt 0 ]; then
  315    echo "**** The following packages were not installed correctly ****"
  316    for key in "${!need_map[@]}"; do
  317      echo "${key} provided by ${need_map[${key}]}"
  318    done
  319    echo "********"
  320    exit 1
  321  fi
  322  
  323  ### NIX PREPARATION ###
  324  prepare_nix_dir() {
  325    if [ -d /nix ] && [ -w /nix ]; then
  326      return 0
  327    fi
  328  
  329    if ! command -v sudo >/dev/null; then
  330      echo "**** Cannot prepare /nix - sudo not available ****"
  331      exit 1
  332    fi
  333  
  334    if [ ! -d /nix ]; then
  335      echo "Creating /nix directory..."
  336      sudo mkdir -p /nix
  337    fi
  338  
  339    if [ ! -w /nix ]; then
  340      echo "Setting /nix ownership to $(whoami)..."
  341      sudo chown "$(whoami)" /nix
  342    fi
  343  }
  344  
  345  prepare_nix_dir
```

### `config/build-identity` lines 1 to 44 (at `8ebaf8daad`)

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # Called once by image assembly. Export the frozen identity to package installs.
    6  pixelelated_build_identity() {
    7    local number='(0|[1-9][0-9]*)' qualifier="${BUILD_QUALIFIER-dev}" actual_hash
    8    [[ "${OS_VERSION}" =~ ^${number}\.${number}\.${number}$ ]] || {
    9      echo "build identity: OS_VERSION must be MAJOR.MINOR.PATCH" >&2; return 1;
   10    }
   11    # Two public forms; dev stays an unqualified engineering identity (#532).
   12    if [[ -n "$qualifier" && "$qualifier" != dev && ! "$qualifier" =~ ^rc\.[1-9][0-9]*$ ]]; then
   13      echo "build identity: qualifier must be dev, rc.N (N >= 1), or empty for a release" >&2
   14      return 1
   15    fi
   16    actual_hash=$(git rev-parse HEAD) || return 1
   17    [[ "$actual_hash" =~ ^[0-9a-f]{40}$ ]] || return 1
   18    if [[ -n "${CUSTOM_GIT_HASH:-}" && "$CUSTOM_GIT_HASH" != "$actual_hash" ]]; then
   19      echo "build identity: CUSTOM_GIT_HASH must match the checked-out commit" >&2; return 1
   20    fi
   21    if [[ -n "${CUSTOM_VERSION:-}${CUSTOM_IMAGE_NAME:-}" ]]; then
   22      echo "build identity: use OS_VERSION and BUILD_QUALIFIER, not custom version/image names" >&2; return 1
   23    fi
   24    BUILD_TIMESTAMP="${BUILD_TIMESTAMP:-$(date -u +%Y%m%dT%H%M%SZ)}"
   25    [[ "$BUILD_TIMESTAMP" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || {
   26      echo "build identity: timestamp must be YYYYMMDDTHHMMSSZ (UTC)" >&2; return 1;
   27    }
   28    local iso="${BUILD_TIMESTAMP:0:4}-${BUILD_TIMESTAMP:4:2}-${BUILD_TIMESTAMP:6:2}T${BUILD_TIMESTAMP:9:2}:${BUILD_TIMESTAMP:11:2}:${BUILD_TIMESTAMP:13:2}Z"
   29    [[ "$(date -u -d "$iso" +%Y%m%dT%H%M%SZ 2>/dev/null)" == "$BUILD_TIMESTAMP" ]] || {
   30      echo "build identity: invalid UTC date" >&2; return 1;
   31    }
   32    GIT_HASH="$actual_hash"
   33    RELEASE_VERSION="${OS_VERSION}${qualifier:+-$qualifier}"
   34    BUILD_VERSION="${RELEASE_VERSION}+${BUILD_TIMESTAMP}.g${GIT_HASH:0:12}"
   35    # Local edits may be useful for development, but never look like a clean cut.
   36    BUILD_DIRTY=no
   37    if [[ -n "$(git status --porcelain=v1 --untracked-files=normal)" ]]; then
   38      BUILD_DIRTY=yes
   39      BUILD_VERSION+=.dirty
   40    fi
   41    BUILD_DATE="$iso"
   42    OS_BUILD="${qualifier:-stable}"
   43    export GIT_HASH RELEASE_VERSION BUILD_VERSION BUILD_TIMESTAMP BUILD_DATE BUILD_DIRTY OS_BUILD
   44  }
```

### `scripts/image` lines 56 to 125 (at `8ebaf8daad`)

```
   56      ${SCRIPTS}/mkimage
   57  }
   58  
   59  # One identity for the installed system, all board variants and release planning.
   60  . "${ROOT}/config/build-identity"
   61  pixelelated_build_identity || die "Invalid build identity"
   62  show_config
   63  DISTRO_VERSION="${BUILD_VERSION}"
   64  DISTRO_ARCH="${DEVICE:-${PROJECT}}.${TARGET_ARCH}"
   65  TARGET_VERSION="${DISTRO_ARCH}-${DISTRO_VERSION}"
   66  IMAGE_NAME="${DISTRONAME}-${TARGET_VERSION}"
   67  if [ -n "${UBOOT_SYSTEM}" ] && [ "${UBOOT_SYSTEM}" != "${DEVICE:-${PROJECT}}" ]; then
   68    IMAGE_NAME="${IMAGE_NAME}-${UBOOT_SYSTEM}"
   69  fi
   70  
   71  # Keep source provenance available to the existing image metadata consumers.
   72  ORIGIN_URL="$(git remote get-url origin | sed -e 's#\.git$##' -e 's#^git:#https:#' -e 's#^git@github\.com:#https://github.com/#' -e 's#://.*@#://#')"
   73  
   74  if [ -n "${IMAGE_SUFFIX}" ]; then
   75    IMAGE_NAME="${IMAGE_NAME}-${IMAGE_SUFFIX}"
   76  fi
   77  
   78  # A frozen timestamp is shared by device builds, never reused to replace bytes.
   79  if compgen -G "${TARGET_IMG}/${IMAGE_NAME}.*" >/dev/null ||
   80     compgen -G "${TARGET_IMG}/${IMAGE_NAME}-*" >/dev/null; then
   81    die "Build identity already exists in target; choose a new BUILD_TIMESTAMP"
   82  fi
   83  
   84  echo "${IMAGE_NAME}" >${BUILD}/BUILD_FILENAME
   85  
   86  # Setup fakeroot
   87  rm -rf ${FAKEROOT_SCRIPT}   # remove ${FAKEROOT_SCRIPT} if it exist
   88  touch ${FAKEROOT_SCRIPT}    # create an empty ${FAKEROOT_SCRIPT}
   89  chmod +x ${FAKEROOT_SCRIPT} # make ${FAKEROOT_SCRIPT} executable
   90  echo "chown -R 0:0 ${INSTALL}" >>${FAKEROOT_SCRIPT}
   91  
   92  # Clean old install dirs
   93  rm -rf ${BUILD}/qa_checks/general
   94  rm -rf ${INSTALL}
   95  rm -rf ${STAMPS_INSTALL}
   96  mkdir -p ${INSTALL}
   97  
   98  # Create base layout of read-only file system
   99  for directory in etc dev proc run sys tmp usr var flash storage; do
  100    mkdir -p ${INSTALL}/${directory}
  101  done
  102  
  103  # Build image contents
  104  MTADDONBUILD=no start_multithread_build image || die "Parallel build failure - see log for details. Time of failure: $(date)"
  105  
  106  echo
  107  echo "Successful build, creating image..." >&2
  108  
  109  # Record the identity beside the artifacts; include this file in candidate custody.
  110  mkdir -p "${TARGET_IMG}"
  111  cat >"${TARGET_IMG}/${IMAGE_NAME}.identity.json" <<EOF
  112  {
  113    "schema": 1,
  114    "name": "pixelelated",
  115    "release_version": "${RELEASE_VERSION}",
  116    "build_version": "${BUILD_VERSION}",
  117    "build_timestamp": "${BUILD_TIMESTAMP}",
  118    "build_commit": "${GIT_HASH}",
  119    "dirty": "${BUILD_DIRTY}",
  120    "device": "${DEVICE:-${PROJECT}}",
  121    "arch": "${TARGET_ARCH}",
  122    "image_name": "${IMAGE_NAME}"
  123  }
  124  EOF
  125  
```

### `config/functions` lines 1095 to 1210 (at `8ebaf8daad`)

```
 1095  }
 1096  
 1097  # Return the global package directory for a package, ignoring any project
 1098  # package of the same name. Used by calculate_stamp; get_pkg_directory
 1099  # deliberately prefers the project package and so cannot answer this.
 1100  get_global_pkg_directory() {
 1101    local _PKG_ROOT_NAME=${1%:*} _ANCHOR="@?+?@" _DIR
 1102  
 1103    for _DIR in $(grep -F "/${_PKG_ROOT_NAME}${_ANCHOR}" "${_CACHE_PACKAGE_GLOBAL}"); do
 1104      echo "${_DIR%${_ANCHOR}}"
 1105      return
 1106    done
 1107  }
 1108  
 1109  calculate_stamp() {
 1110    local stamp data global_dir
 1111  
 1112    stamp="$PKG_DIR $PROJECT_DIR/$PROJECT/patches/$PKG_NAME $PROJECT_DIR/$PROJECT/packages/$PKG_NAME"
 1113    [ -n "$DEVICE" ] && stamp+=" $PROJECT_DIR/$PROJECT/devices/$DEVICE/patches/$PKG_NAME"
 1114    [ -n "$PKG_NEED_UNPACK" ] && stamp+=" $PKG_NEED_UNPACK"
 1115  
 1116    # A project package.mk routinely sources the global one to inherit
 1117    # PKG_VERSION, PKG_URL and PKG_SHA256, adding only project-specific hooks.
 1118    # $PKG_DIR resolves to the project copy in that case, so without this the
 1119    # global recipe is never hashed and a version bump there does not invalidate
 1120    # the stamp - the previous version stays built and installed, silently. For
 1121    # a package with no project override this adds a path already in the list,
 1122    # which the sort -u below discards, so existing stamps do not change.
 1123    global_dir="$(get_global_pkg_directory "${PKG_NAME}")"
 1124    [ -n "${global_dir}" ] && stamp+=" ${global_dir}"
 1125  
 1126    data="$(find -L ${stamp} -type f -not -name '.*' -print0 2>/dev/null | sed -z "s|^${ROOT}/||" | LC_ALL=C sort -zu | xargs -0 sha256sum)"
 1127    [ -n "${PKG_STAMP}" ] && data+=$'\n'"$(echo "${PKG_STAMP}" | sha256sum)"
 1128  
 1129    echo "${data}" | sha256sum | cut -d" " -f1
 1130  }
 1131  
 1132  target_has_feature() {
 1133    listcontains "$TARGET_FEATURES" "$1"
 1134  }
 1135  
 1136  # configure variables for go
 1137  go_configure() {
 1138    unset GOARCH GOARM
 1139    case ${TARGET_ARCH} in
 1140      x86_64)
 1141        export GOARCH=amd64
 1142        ;;
 1143      arm)
 1144        export GOARCH=arm
 1145  
 1146        case ${TARGET_CPU} in
 1147          arm1176jzf-s)
 1148            export GOARM=6
 1149            ;;
 1150          *)
 1151            export GOARM=7
 1152            ;;
 1153        esac
 1154        ;;
 1155      aarch64)
 1156        export GOARCH=arm64
 1157        ;;
 1158    esac
 1159  
 1160    export GOOS=linux
 1161    export GOROOT=${TOOLCHAIN}/lib/golang
 1162    export PATH=${PATH}:${GOROOT}/bin
 1163  
 1164    go_configure_path
 1165  
 1166    export CGO_ENABLED=1
 1167    export CGO_NO_EMULATION=1
 1168    export CGO_CFLAGS=$CFLAGS
 1169  }
 1170  
 1171  go_configure_path() {
 1172    export GOLANG=${TOOLCHAIN}/lib/golang/bin/go
 1173    export GOPATH=${PKG_BUILD}/.gopath
 1174    export GOFLAGS="-modcacherw"
 1175  }
 1176  
 1177  # find path for matching file or directory, searching standard directory hierarchy, using optional default
 1178  # if a path is located it will be set in FOUND_PATH and exit code will be 0.
 1179  find_path() {
 1180    local test_func="$1" search="$2" default="$3"
 1181    local dir match wildcard=0 ftype
 1182  
 1183    # support wildcard matches
 1184    [[ $search =~ \* || $search =~ \? ]] && wildcard=1
 1185  
 1186    [ "$test_func" = "-f" ] && ftype="file" || ftype="dir"
 1187  
 1188    for dir in $PROJECT_DIR/$PROJECT/devices/$DEVICE/packages/$PKG_NAME \
 1189               $PROJECT_DIR/$PROJECT/devices/$DEVICE \
 1190               $PROJECT_DIR/$PROJECT/packages/$PKG_NAME \
 1191               $PROJECT_DIR/$PROJECT \
 1192               $DISTRO_DIR/$DISTRO/packages/$PKG_NAME \
 1193               $DISTRO_DIR/$DISTRO \
 1194               $PKG_DIR \
 1195               ; do
 1196      # ignore directories with missing DEVICE or PKG_NAME components
 1197      [[ $dir =~ /packages/$ ]] && continue
 1198      [[ $dir =~ /devices/$ ]] && continue
 1199      [[ $dir =~ /devices//packages/$PKG_NAME$ ]] && continue
 1200  
 1201      if [ $wildcard -eq 1 ]; then
 1202        ls $dir/$search 1>/dev/null 2>&1 && match="$dir/$search" && break
 1203      else
 1204        [ $test_func "$dir/$search" ] && match="$dir/$search" && break
 1205      fi
 1206    done
 1207  
 1208    if [ -z "$match" -a -n "$default" ]; then
 1209      if [[ $default =~ \* || $default =~ \? ]]; then
 1210        ls $default 1>/dev/null 2>&1 && match="$default"
```

### `scripts/unpack` lines 84 to 118 (at `8ebaf8daad`)

```
   84      if [ -n "${PKG_URL}" ]; then
   85        ${SCRIPTS}/extract "${PKG_NAME}" "${PKG_UNPACK_DIR}"
   86      fi
   87      pkg_call_finish
   88    fi
   89  
   90    if [ -z "${PKG_SOURCE_DIR}" -a -d "${PKG_UNPACK_DIR}/${PKG_NAME}-${PKG_VERSION}"* ]; then
   91      mv "${PKG_UNPACK_DIR}/${PKG_NAME}-${PKG_VERSION}"* "${PKG_UNPACK_DIR}/.intermediate"
   92    fi
   93  
   94    if [ ! -d "${PKG_UNPACK_DIR}/.intermediate" ]; then
   95      if [ -n "${PKG_SOURCE_DIR}" ]; then
   96        if [ -d "${PKG_UNPACK_DIR}"/${PKG_SOURCE_DIR} ]; then
   97          mv "${PKG_UNPACK_DIR}"/${PKG_SOURCE_DIR} "${PKG_UNPACK_DIR}/.intermediate"
   98        else
   99          # fallback
  100          mv "${BUILD}"/${PKG_SOURCE_DIR} "${PKG_UNPACK_DIR}/.intermediate"
  101        fi
  102      fi
  103    fi
  104  
  105    [ ! -d "${PKG_UNPACK_DIR}/.intermediate" ] && mkdir -p "${PKG_UNPACK_DIR}/.intermediate"
  106  
  107    if [ -d "${PKG_DIR}/sources" ]; then
  108      cp -PRf "${PKG_DIR}/sources/"* "${PKG_UNPACK_DIR}/.intermediate"
  109    fi
  110  
  111    # Add a tag to the unpacked folder before transferring into the shared build folder
  112    echo "INFO_PKG_NAME=\"${PKG_NAME}\"" >"${PKG_UNPACK_DIR}/.intermediate/.rocknix-package"
  113  
  114    # Restore original PKG_BUILD, and transfer the unpacked folder
  115    PKG_BUILD="${PKG_BUILD_ORIG}"
  116    rm -fr "${PKG_BUILD}"
  117    mv "${PKG_UNPACK_DIR}/.intermediate" "${PKG_BUILD}"
  118  
```

### `config/options` lines 128 to 152 (at `8ebaf8daad`)

```
  128  if [ -z "$ADDON_URL" ]; then
  129    ADDON_URL="$ADDON_SERVER_URL/$ADDON_PATH"
  130  fi
  131  
  132  # read local persistent options from $ROOT if available
  133  if [ -f "${ROOT}/.rocknix/options" ]; then
  134    . "${ROOT}/.rocknix/options"
  135  fi
  136  
  137  # read global persistent options from $HOME if available
  138  if [ -f "${HOME}/.rocknix/options" ]; then
  139    . "${HOME}/.rocknix/options"
  140  fi
  141  
  142  if [ "${LOCAL_CCACHE_SUPPORT}" = "yes" ] && [ -z "${CCACHE_DISABLE}" ]; then
  143    # like LOCAL_CC check for local ccache only on the very first
  144    # call to config/options, before toolchain has been added to the path,
  145    # otherwise we might pick up ccache from toolchain/bin here
  146    if [ -z "${LOCAL_CCACHE}" ] && [ "${LOCAL_CCACHE_CHECKED}" != "yes" ]; then
  147      export LOCAL_CCACHE="$(command -v ccache)"
  148      export LOCAL_CCACHE_CHECKED="yes"
  149    fi
  150  else
  151    export LOCAL_CCACHE=""
  152  fi
```

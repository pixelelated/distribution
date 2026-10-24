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

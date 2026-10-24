# T5's remediation streams (#652, audit issue #837)

Written by the coordinator at T5's stage-D pause (2026-10-24, D-WORKFLOW-189),
one stream per group of related items in the D-WORKFLOW-056 shape: the files
owned, the test first (the lane's own sandbox fixtures, `tools/sb-*.sh` in
its audit folder, extended where a stream needs more), the `Already
written:` line, commits cut only after the checks are green. The brief
(`docs/reviews/briefs/build-engine.md`) § 5 still governs: **nothing here
builds an image or a package**; a sandbox is a fixture under
`.qa-scratch/`, a `bash -x` trace first; the engine's fixes are proven by
the fixtures now (`fix-sandbox`) and by the first image built after the
integration (`fix-pending-image`), each row saying which. Commits land on
the slice branch `feature/m6-build-engine-652`, cite the punch item and its
`bug` with `Refs` (no closing keyword), keep upstream's headers, pass
`bash -n` on every script touched, and leave `git status --short` empty;
the running log gets a `PROOF:` line per proof; the Phase 7 table and the
`punch_index` move at the end of each stream. The engine's changes merge to
`next` after the other slices' (brief § 10), so every stream states what a
later slice's fix depends on.

## Dispositions that are not streams (the coordinator's; the lane writes them into the Phase 7 table)

| Item | Disposition |
| --- | --- |
| PL-11, PL-19 | `deferred:#651` (T4): `device-builds.md` § After rebasing items 2 and 3, and § Build credentials' two spellings of the options file; T4's brief § 3 names them |
| PL-15 | `deferred:#657` (T10): `update-kernel-configs-docs.yml` fails on every fork push |
| PL-16 | `deferred:#652`, the coordinator's act: the container pin moves with the first M6 image build after the M7 candidate merges, in the stream brief that names that build (the `Makefile` digest and the `docker-image-pull` recipe); until then the row says *behind by 29 days, identical Dockerfile* |
| PL-17 | the base merge takes `config/blocklist`, `build-nightly.yml` and the PR template (the coordinator's act) |
| PL-25 | `deferred:#652`: `ccache --show-stats` before and after the first M6 build, recorded on #652 by the coordinator |
| PL-26 | `deferred:#652`: `scripts/test-audit-review.py` moves to `tooling-and-guards` in `areas.json` when the P1 branch merges (the coordinator's ledger edit, D-WORKFLOW-189); T10 reads it there |

## E1. `scripts/mkimage` fails closed over an incomplete image (PL-01, #827) -- High

- **Files owned:** `scripts/mkimage` (lines 49, 252 to 255, 270 to 273, 324 to 334), `projects/ROCKNIX/bootloader/mkimage` (82, 110).
- **The test first:** the lane's sandboxed `qcom-abl` branch over a FAT image too small for `SYSTEM` (#827's criterion): exits 0 and prints success before; exits non-zero and prints `image: An error has occurred...` after; the `arm-efi` branch the same with its own fixture. Every copy into the FAT image (`mcopy` or its equivalent) and every size the script computes checked, not only the one the fixture hits: list them in the hand-back.
- **The change:** check the return of each copy and each `truncate`/`dd` into the image, and the free space before the copy, dying through the script's own error path; no new tools.
- **Already written:** nothing on a device; an image that shipped incomplete would not have booted, and none is known to have (say so from the M7 build records read-only, `.build-runs/*/build.rc`).
- **Proof class:** `fix-sandbox` now; `fix-pending-image` for the next SM8550 and H700 builds' `target/` (their sidecars and `build.rc` 0).
- **Commit:** `mkimage: fail on an incomplete image instead of reporting success (#827)`.

## E2. `scripts/get_git`'s cache check (PL-02 #828, PL-03 #829) -- High and Medium, one stream

- **Files owned:** `scripts/get_git` (`_repo_exists_and_valid`, lines 26 to 36, 198 to 199).
- **The test first:** `tools/sb-get-git-pushd.sh <scratch> <commit>` prints `check: rejected` and an `after:` line still listing `build.fixture-1`, `sources` and `untracked-file` (today: `after: .git` alone, the `git clean -fdx` having run in the build tree); `tools/sb-get-git-head.sh` prints `refused` for `PKG_VERSION=A` with `HEAD` at `B` and `accepted` for `PKG_VERSION=B`. Both fixtures run before (fail) and after (pass), their lines pasted.
- **The change:** `pushd` checked on its own line (never on the left of `&&` as the condition the caller discards); a cache directory the user cannot enter is *not a valid repo* and the function returns false without touching the current directory; `HEAD` compared to `PKG_VERSION` (resolved: a tag or branch name resolves through `git rev-parse`), a mismatch making the clone invalid so the existing re-fetch-and-reset path (`get_git:137`) runs. Keep upstream's structure; the fix is a few lines.
- **Already written:** a cached clone whose `HEAD` drifted is corrected by the next fetch; a build tree once cleaned by the defect cannot be recovered and is not pretended to be (the row says so).
- **Proof class:** `fix-sandbox`; `fix-pending-image` for the first build that reuses a warm cache.
- **Commit:** `get_git: a cache directory that cannot be entered or whose HEAD is not the pin is invalid (#828, #829)`.

## E3. `scripts/get_env`'s credential filter (PL-04, #830) -- Medium

- **Files owned:** `scripts/get_env` (lines 2 to 21); the `Makefile`'s `.env` recipe (205 to 208) only if the mode or the removal needs a change (read it; D-INFRA-006 already has `.env` 0600 and removed on exit).
- **The test first:** `tools/sb-get-env.sh` with a **synthetic** environment (never the session's own; the fixture sets its names itself) prints none of `DB_PASS`, `SSHPASS`, `DOCKERHUBTOKEN`, `github_token`, `MY_PASSPHRASE`, `SESSION_COOKIE`, `MULTILINE` or a bare `OTHER_TOKEN` line, and still prints `PROJECT`, `DEVICE`, `ARCH` and `SCREENSCRAPER_DEV_LOGIN` (the four forwarded by name, D-INFRA-006 and D-WORKFLOW-166). Before the fix the first set leaks and a newline value writes its own lines.
- **The change:** the `DROP` pattern case-insensitive and widened to the shapes the fixture names (`PASS`, `TOKEN`, `COOKIE`, `PASSPHRASE`, `SECRET`, `KEY` as a word, `PSK`), a value containing a newline or a carriage return dropped with a one-line notice naming only the variable's name, and the four allowed names forwarded by exact name as today. **Nothing in this stream prints a value**: the fixture's output is names, and the hand-back pastes names.
- **Already written:** `.env` files are removed when the container exits; a stale one from a crashed run is the one risk, and the stream's hand-back says whether `Makefile` already removes a leftover at the next start.
- **Proof class:** `fix-sandbox`; `fix-pending-image`'s cousin is the next `make docker-*` run's `.env` read back as names only.
- **Commit:** `get_env: drop every secret-shaped name and any multi-line value (#830)`.

## E4. The launch table's mechanism (PL-05 #831, PL-06 #832) -- Medium, one stream

- **Files owned:** `distributions/ROCKNIX/config/functions` (`add_es_system` 127 to 142; the one-default rule at 113 and 209 to 215); `config/emulators/{daphne,gp32,arcade,segamodel3}.conf` only if a fragment is wrong rather than carried (read first). **T3's S2 edits the device arms of `projects/ROCKNIX/packages/virtual/emulators/package.mk` and must not touch this file**; the two streams meet at the integration, where the coordinator regenerates once more.
- **The test first:** `tools/sb-es-cases.sh`: case A (two `default="true"` lines) fails with a message naming the duplicate attribute (today: a silent stop); case B (a `false` core before the `true` one) ships one default, `b2` (today: two); case C (a system appended after `imageviewer`) gets the default `runemu.sh` command (today: nothing). Then the regeneration for all five devices (the lane's regeneration script, as its stage B used): `daphne` `1983` and `gp32` `2001`, and **every other line of the five tables byte-identical to today's** (`diff` per device pasted, two lines each).
- **The change:** every per-system variable the fragment sets is reset at the top of `add_es_system` (the carried-over year and command), and the one-default rule counts `default="true"` lines once over the whole system and dies with the system and the cores named when the count is not one -- a loud failure in place of a silent stop, and one default whatever the order.
- **Already written:** a device's `es_systems.cfg` is the image's and is replaced whole; `daphne` and `gp32` show the right year after the next image; no player state names a system's year.
- **Proof class:** `fix-host-regen` now (the regeneration is the build's own writer, byte-identical to the images as T3 proved); `fix-pending-image` for the three images' tables.
- **Commit:** `distributions: add_es_system resets each system's fragment; the one-default rule fails loudly and counts once (#831, #832)`.

## E5. The image path (PL-07 #833; PL-20, PL-24, PL-12, PL-13) -- Medium and four Lows

- **Files owned:** `scripts/build_distro` (72 to 78, 82 to 84, 103 to 106), `scripts/image` (71 to 72, 78 to 82, 84), `scripts/build_compat` (56 to 82).
- **The test first:** #833's fixture: with `BUILD_TIMESTAMP` set and a matching output in a fixture `target/`, the sandboxed prune-and-image sequence **refuses** and leaves the existing files byte-identical (today it prunes them, so `scripts/image`'s own refusal at 78 to 82 never sees them); PL-20: `bash -x` shows the dead `if` after `make image` never reached on failure under `set -e`, then a fixture where `make image` fails exits through the script's error path with its message; PL-24: the initramfs clean fires for a device without `DEVICE_ROOT` in the fixture (or the row says, from the history, why it was RK3566-only and keeps it with a comment); PL-12: `git grep -n 'ORIGIN_URL\|BUILD_FILENAME'` finds no reader after the removal (or the reader is named and the variable kept); PL-13: `build_compat`'s naming follows `config/build-identity`'s (`docs/releases/versioning.md`, D-WORKFLOW-157), the before/after file names from a fixture run pasted.
- **The change:** the prune happens after `scripts/image`'s identity refusal has had its say (reorder, or `image` refuses first), the dead check becomes a real one, the clean fires where it should, the dead variables go, the compat naming follows the identity's.
- **Already written:** an identity already published is immutable (D-WORKFLOW-157); this stream makes the documented route unable to replace one. Nothing to migrate.
- **Proof class:** `fix-sandbox`; `fix-pending-image` for the next build's `target/`.
- **Commit:** one per file, `build_distro: ...`, `image: ...`, `build_compat: ...`.

## E6. Fetch and unpack fail closed (PL-08 #834; PL-14; PL-10 #836) -- Medium and two Lows

- **Decision (D-WORKFLOW-193, written with this brief):** an archive recipe without `PKG_SHA256` fails its fetch, and the fetch verifies TLS; the eight recipes of 1,347 that lack a checksum gain theirs in this stream, computed from the archive as fetched once and said to be so (trust on first use, as upstream's own `PKG_SHA256` sweep was). The maintainer may reverse it by a new row.
- **Files owned:** `scripts/get_archive` (25, 45), `scripts/update_packages` (50 to 61) if it writes checksums, `scripts/unpack` (90 to 105), the eight recipes' `PKG_SHA256` lines (named in the hand-back with the command that produced each: `sha256sum` of the archive fetched into a scratch directory, **not** into the shared sources cache), `config/functions` 1109 to 1129 / 1188 to 1191 and `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk` (10, 39) for #836.
- **The test first:** #834: a sandboxed `get_archive` with an empty `PKG_SHA256` refuses with a message naming the recipe, and its `wget` line carries no `--no-check-certificate` (`bash -x`); a recipe with a wrong checksum still fails as today. PL-14: a fixture with two `name-version*` entries in the unpack directory makes `unpack` die naming both (today it empties the package); one entry unpacks as today. #836: `tools/sb-stamp-device-config.sh` with the recipe's fixed `PKG_NEED_UNPACK` prints that the stamp moved when the device-level file changes.
- **The change:** fail closed in `get_archive` and `unpack`; the device-level file `find_file_path` reads added to `PKG_NEED_UNPACK` in the recipe (or `calculate_stamp` taught to hash what `find_file_path` resolves -- say which and why; the recipe line is the contained fix, `config/functions` the general one, and the general one is a second commit if taken).
- **Already written:** a warm build root whose stamps predate the fix rebuilds `kernel-firmware` once (the stamp changes); archives in the shared cache are unaffected (checksums are checked at fetch).
- **Proof class:** `fix-sandbox`; `fix-pending-image` for the first build (the eight recipes fetch with their new checksums).
- **Commit:** `get_archive: verify TLS and refuse an archive without a checksum (#834, D-WORKFLOW-193)`, `unpack: ...`, `kernel-firmware: ... (#836)`, plus one `<package>: PKG_SHA256` per recipe or one commit for the eight.

## E7. The host side (PL-09 #835; PL-18) -- Medium and a Low

- **Files owned:** `scripts/checkdeps` (296 to 309, 324 to 345), `Makefile` (131 to 153, 186 to 188).
- **The test first:** #835: a sandboxed `checkdeps` with shimmed `sudo` and `update-alternatives` calls neither unless the opt-in (`CHECKDEPS_ALLOW_HOST_CHANGES=1`, or the name the script's style suggests) is set, and prints what it would have done; with the opt-in it calls both as today. PL-18: the options file mount gains `:ro` and `make -n docker-<X>` shows it; the `docker-image-build` target is either wired to a documented use or removed with the reason, and `make -n` of every `docker-*` target still resolves.
- **The change:** host changes behind an explicit opt-in with a printed plan otherwise; the mount read-only; the dead target dispositioned.
- **Already written:** a host already changed by `checkdeps` stays changed (the compiler alternative, `/nix`); the row says so and names what a host owner would undo by hand.
- **Proof class:** `fix-sandbox`; the next `make docker-*` run reads the `.env` and the mount (`fix-pending-image`'s cousin).
- **Commit:** `checkdeps: change the host only on an explicit opt-in (#835)`, `Makefile: ...`.

## E8. Upstream's helpers (PL-21, PL-22, PL-23) -- Lows, each contained

- **Files owned:** `config/functions` (201, 208, 1201 to 1202, 1511, 1694, 1894, 1897), `scripts/get_git` (196, 239), `scripts/pkgbuild` (32), `config/multithread` (64), `scripts/makefile_helper` (26), `config/build-identity` (37).
- **The test first:** per site, a `bash -x` fixture or a `bash -n` and a reading that names the wrong behaviour before and the right one after (PL-23: a failing `git status` in the fixture reads as *dirty, unknown* and refuses the identity, not *clean*); each is contained (`bugs-are-agent-first.md` rule 6: a defect in upstream's code is ours to close when the fix is contained).
- **The change:** the smallest fix per site; each commit separable so #585 can carry it upstream (D-WORKFLOW-164; held under D-WORKFLOW-165): the hand-back lists each with its upstream target, and the coordinator adds the rows to #585.
- **Already written:** nothing. **Commit:** one per site or per file, `Refs #837, #585`.

## Order and hand-back

E1, E2, E3, E4, E5, E6, E7, E8, each handed back with one comment on #652 (the stream, its commits, the fixture lines before and after, the `punch_index` rows moved with their `proved:` class) and the lane going straight on. At the end: the Phase 7 table complete, `tools/lint-audit-artifacts` on the folder, `fixed-at` written into #652, the retro (stage G), the hand-back comment (stage H). The coordinator reviews each stream as it lands and accepts at hand-back per the brief § 10; E4's regeneration is repeated by the coordinator at the integration after T3's S2 has landed, with the union of the two intended diffs.

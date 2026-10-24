# Mini Retro: M6.P2 T5, the build engine (#652)

**Completed:** 2026-10-24
**Scope of this retro:** the T5 lane, covering:
- stage A, the slice's 242 paths, read with the bytes equal to `next`'s `8ebaf8daad`;
- the audit, stages A to D (`docs/audits/2026_10_24-epic-m6-build-engine/`, #837's 26 items);
- the fix streams E1 to E8 and E5b of `docs/reviews/briefs/t5-streams.md`;
- the close-out.

Not retro'd here, because they are not this lane's:
- the coordinator's acceptance;
- the merge to `next`;
- the first image carrying the fixes, where the `fix-pending-image` halves are proved.

**Commits:** `reviewed-at` `46f6c7d428`, `fixed-at` `877775e61e`.

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** Interface to a game's first frame and game to game are untouched, as `04` § Q5 said before the fixes.

The engine is not on the launch path. Every change in E1 to E8 runs on the build host or in the build container:
- the image writer;
- the source fetch;
- the container's environment;
- the stamp;
- the host checks.

**On a device**, the slice changes three things, none of them at launch time:
- **The launch table:** two release years (`daphne` 1983, `gp32` 2001). EmulationStation reads the table at start, and its size changes by nothing.
- **The identity:** the identity's fields are unchanged.
- **The sidecar:** it does not reach a device.

No time-to-play run was made after the fixes, because there is no image yet. The first image after the integration is where the numbers are measured again.

## What worked well

- **Running the real script over fixture files, not a lifted line.** E1's `tools/sb-mkimage.sh` ran the real `scripts/mkimage` and the shared bootloader hook, with mtools and populatefs copied read-only from a build root. The trace showed `Disk full`, then `pigz`, `sha256sum` and exit 0. It also showed the hook's own copy (`mkimage_abl`) running, so the SM8550 route was covered whole.
- **Lifting by marker lines, not line numbers.** The fixtures for `get_git`, `unpack`, `build_distro`, `checkdeps` and `multithread` lift their blocks by marker lines, so a fix that moved lines was still tested whole. That's how P13's one-line lift became P16's whole-function test.
- **The reviewers' questions, answered from the tree.** Astra's "the packet does not show how `PACKAGE` is keyed" moved F-18 from High to Medium (`config/functions:1350`). Its "the clean lists are not supplied" moved F-17 to Low (`CLEAN_OS_BASE`). Its G-01 became F-25, a High proved in a sandbox. Argon's claim about `chmod` and dangling symlinks was refuted in a sandbox, so its re-grade was declined.
- **Reading the recorded runs before changing behaviour.** Each fail-closed change was first checked against what M7's builds show:
  - the hook's copies: 0 mtools refusals in 26 image steps;
  - the size guard: 75% and 61% of `SYSTEM_SIZE`;
  - the unpack die: every empty build directory is a no-archive package;
  - TLS: every `GET (git)` clone over verified `https`;
  - the git cache: 311 of 311 clones at their pin.

  So no working build was broken by a guard that only a broken build should meet.

## What was harder than expected

- **Timestamps ahead of the clock, three times in one session.** The 03:52 heading, the 04:33 to 04:50 stamps, and two lines of the 4.6 grading draft. Each was caught by the next `date -u` read; the third was caught before a commit. The guard proposed at the second instance, a lint refusing a stamp ahead of its commit, still does not exist.
- **Fixtures that were wrong before the code was.** Each was caught by the fixture itself, before a commit:
  - `bash -c '…' name` puts the name in `$0`, not `$1`;
  - `(exit 1); onexitcleanup` under `set -e` ends the handler before the call;
  - a loop variable in `find_path` not declared `local`.
- **One watched run per worktree.** `tools/watch-build --record-only` holds the worktree's build lock even for a network call, so the second reviewer call ran unwatched, with a harness waiter on it (friction line).
- **A count from a shallow test.** The "eight recipes without a checksum" was a test for a top-level line. A per-branch read found five versions in four recipes, after the decision row had already been written on the eight (D-WORKFLOW-194).

## What we discovered

- **`get_git` can delete a build tree (F-25).** A cache directory the build user cannot enter makes `git clean -fdx` run in the caller's directory, and the check says only "rejected". It's upstream's code, and the punch list's second High.
- **The fetch trusted the network twice.** There was no TLS check, and an empty checksum was accepted, including for an archive already in the cache. Only five archive versions in the tree had no checksum, and two of them were on the fork's own devices (`atf` for H700, `rkbin` for RK3326/RK3566).
- **The container differs from a native host in two ways that mattered.**
  - It already has the gcc alternative and `/nix` (the `Dockerfile`), so gating `checkdeps`' host changes touches no Docker build.
  - `get_env`'s `KEYS` word drops `LOCAL_SSH_KEYS_FILE` inside every container, so the development `authorized_keys` copy has not run in a Docker build since 2026-09-05. That's a lead, put to the maintainer on #346.
- **A rule that cannot hold yet.** One default per system holds on every table except GENERIC_X64's `psx`. Its recipe line is T3's, so the zero case warns here and becomes fatal at the integration (the coordinator's merge notes).

## Adjustments for the next lane

- **Run the real script over fixture files when its tools can be borrowed read-only from a build root.** A lifted line proves the line, not the route.
- **Lift by marker lines and take a commit or `WORKTREE` argument in every fixture,** so before and after are the same command.
- **Before a guard fails closed, read what the recorded builds show it would meet.** A new failure on a path every build takes is a regression, not a guard.
- **Count shapes per branch, not per file,** before a number goes into a decision row.

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-build-engine --phase pre-issue`: `PASS`.
- `PROOF:` lines 28 equal the `proved:` cells, 28.
- The coverage table has 242 rows.
- #837: 26 of 26 at a Phase 7 outcome (19 Resolved, 7 Deferred), each ticked naming its commit or target; `tools/box-check --issue 837`: 0 open, 0 fail.
- The ten `bug` issues: the met checkboxes ticked; #827's and #832's first checkbox left open, each with its reason on the issue. `box-check` 0 fail on each.
- The five checkers and `hooks-test`: exit codes on #652's stage-H hand-back.

# Mini Retro: M6.P2 T9, build supervision and host maintenance (#656)

**Completed:** 2026-10-24
**Scope of this retro:** the T9 lane, covering:
- the slice's 18 paths (3,795 lines), read with the bytes equal to `next`'s `8ebaf8daad`;
- the Independent-depth audit, stages A to D (`docs/audits/2026_10_24-epic-m6-tooling-build-supervision/`, #924's 21 items, one GPT-6 Astra seat);
- the eight fix streams of the coordinator's `t9-streams.md` (`4c842e2485`), and the S3 addendum (`16fe2b79ac`);
- the close-out.

Not retro'd here, because they are not this lane's:
- the coordinator's acceptance and its dispositions (#925, #926, #927, #528, #640, #657);
- the merge to `next`;
- the owner's reinstallation of `reclaim-swap` (D-INFRA-015).

**Commits:** `reviewed-at` `cb8019a10b`, `fixed-at` `00e571b8a8`.

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** Interface to a game's first frame and game to game are untouched. Every changed file is a build-host tool or its control. None is on an image, in a build's product, or on a device. No image was built, so no time-to-play run was made.

## What it did to the watchers' silence modes

`engineering-practices.md` § *Say how the watch fails* asks for each silence mode to be named. After S4 and S5:

- **`watch-job`:**
  - A PID this user cannot signal (EPERM) was reported `died`, a false death. It is now read from `/proc` and reported alive.
  - A PID whose `/proc` entry cannot be read is now an observation error (`state: error`), never `died`.
  - **Unchanged and still named:** a PID that another namespace hides reads as exited (#506's rule). A job killed outright writes no exit code, and the watcher reports `died` with no result.
- **`watch-build`:**
  - A watcher that ignores SIGTERM no longer leaves the runner raising with no finish recorded. It is killed after the second wait, and `runner-error` and `runner-result.json` are written.
  - A console that stops reading is dropped after 2 s, with a `console-dropped` note. Before, it froze the build.
  - The worktree lock now lasts the command's lifetime.
  - **The watch still fails silently in one way:** a runner killed outright leaves the detached watcher to report `died`, and the lock held by the orphaned command refuses the next build. That refusal is the intended loud state.

## What worked well

- **Constructing the failure first, for each stream.** Every case was seen to fail on the unfixed tool before the fix: an export of the stage's commit, or a temporary copy with its other cases cut. Where a fixture made a first "fail" for the wrong reason (S5's stubborn watcher, refused by admission instead), reading the record caught it before it was cited.
- **A real signal to a disposable child.** S7 sent SIGQUIT and the rest to a child running `recycle()` against the doubles, so the unfixed helper's default action ended the child (rc -3, -10, -12, -14), not the suite, and no swap command ran.
- **The pinned container, once, read-only and network-less.** The 3.10 proof (S3) took one posted start of seconds and named the interpreter, 3.10.12, with no pull.
- **Reading the record before a claim of "already written".** S6's 665 rows each equal their registry row and their receipts, which is what lets the fixed `consume` read every recorded run unchanged (counts printed only).

## What was harder than expected

- **Moving the registry moved the controls' isolation.** Each fixture had been isolated by its own `.git`. A per-filesystem registry would have put every control's in-process `prepare` into the user's real state directory. The fixture helper now binds a per-fixture state directory, and five controls pass it as `XDG_STATE_HOME`; three of those files belonged to S1.
- **A fixture bound to a reviewed launcher.** #923 changed `watch-build-submit`, and the #597 recovery fixture, which copied the current launcher, stopped matching `COLLISION_LAUNCHER_SHA256`. Recovery is right to accept only the reviewed bytes. The fixture now reads them from their git blob.
- **`rules-check` ties three lists together.** S8 could not drop the index row or the personal-paths entry while `.githooks/pre-push`, which is T10's, keeps its pattern. Each check said so in turn.
- **Typed times, again.** Two headings and a PROOF line were written with a guessed minute and corrected from the clock. The fix was to produce every time with `date -u` before the text went in.

## What we discovered

- **An admission refusal and a launch failure looked the same.** Both were logged as `command launch/output failed`. The addendum names the refusal (`86ef7ae6b1`), and rc 125 stays.
- **A report made before `82840dbc42` is refused, not valid for 900 s.** It binds the old tool's hash and has no `observation_start`.
- **`ceremony-check:113` still calls `hashlib.file_digest`.** It is host-only, so it never meets 3.10, and it is outside the slice. It is named on #915.
- **`unshare -Upf --mount-proc` is refused on this host,** so a namespace-hidden PID cannot be constructed here (S4).

## Slips of mine

- **A kill by pattern.** `kill $(pgrep -f 's6-record-rows.py')` matched the shell issuing it and ended it (exit 144). It broke the rule to kill by PID, and the case in its blindspot is the same shape. Nothing else was hit. Afterwards I listed processes by a fixed string with `ps`, and killed only by recorded PIDs.

## Adjustments for the next lane

- **When a change moves where state lives, find every control that reached it implicitly before the fix.** Fixture isolation by `.git`, by `HOME` or by the current tool's bytes is a dependency on the old location.
- **Read the record for "already written" with a counting script that prints counts only.**
- **Stop a process by its recorded PID.** A `pgrep -f` pattern also matches the shell that carries it.

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-tooling-build-supervision`: `PASS`, at the resolution phase.
- `PROOF:` lines equal the `proved:` cells: 21 and 21.
- The coverage table has 18 rows.
- #924: 21 of 21 at a Phase 7 outcome (15 Resolved, 5 Deferred, 1 Withdrawn).
- The bugs #913 to #923 each carry their fix comment.
- The controls at the tip are in `02` § Stage E, the close-out. The checkers' exit codes are on #656's hand-back.

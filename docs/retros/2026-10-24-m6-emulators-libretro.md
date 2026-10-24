# Mini Retro: M6.P2 T3, RetroArch and the libretro cores (#650)

**Completed:** 2026-10-24
**Scope of this retro:** the T3 lane from stage A (the slice's 344 paths, its
bytes equal to `next`'s `8ebaf8daad`) through the audit (stages A-D:
`docs/audits/2026_10_24-epic-m6-emulators-libretro/`, #826's 34 items) and
the seven fix streams S0-S6 of `docs/reviews/briefs/t3-streams.md`, to the
close-out. Not retro'd here, because they are not this lane's:
- the coordinator's acceptance;
- the merge to `next`;
- the first image carrying the fixes, where the `fix-pending-image` items are proved.

**Branch:** `feature/m6-emulators-libretro-650`, `reviewed-at: d606301784`,
`fixed-at: 3c47325fb2`.

**Delta:**
- **Code:** 26 fix commits on the slice's paths (40 files, +293 / -472), plus S0's fix branch `fix/m6-825-cheevos-hook-no-shell` (`fac139dd43`), merged `--no-ff`.
- **The punch list:** 34 items, all with a Phase 7 outcome.
  - **9 resolved:** 4 by host regeneration (`fix-host-regen`).
  - **25 deferred:** 11 `fix-pending-image` with their commits, and 14 by the coordinator's dispositions (#802, #806, #652, #838, #839, the base merge, M7's `Install Steam.sh` hunk).
- **Bugs:** 14 issues filed (#813-#825, #841). The host-met checkboxes of #817, #823, #824 and #841 are ticked; the others wait for the image.
- **Tools:** `tools/retroarch-wrapper-test --gated` now asserts patch 0015's gate, with its own failing control. The audit folder carries:
  - the regeneration check (`tools/s2-regen-check.sh`);
  - the profile key test (`tools/s5-keytest.py`);
  - the outcome writer (`tools/set-outcome.py`).

## What the slice did to the two time-to-play numbers

**Nothing measured after the fixes, and nothing on either path is expected to move.** On the lane's guest at stage B (`04-analysis.md` § Q5, n=3), interface to a game's first frame was **0.62 s** and game to game **1.01 s**.

Read from the code:
- **PL-032** replaces `system()` with `fork` and `execv` on an achievement unlock. That runs inside a game, not on either path, and it is one shell fewer.
- **PL-006, PL-005, PL-012, PL-015 and PL-024** are build-time.
- **PL-016** removes 24 to 26 dead lines from each profile, which RetroArch parses once at start. A device keeps its own copy, so only a fresh install gets the shorter file.
- **S2** changes which choices the table offers, not what launches by default anywhere (GENERIC_X64's `psx` default is the emulator that already launched).

The after numbers come with the first image, at the coordinator's stage.

## What worked well

- **The host regeneration of the launch table.** It was byte-identical to three images at stage B, so every table fix in S2 was proved on the host by its exact diff, plus a missing-core check (#838's check, done by hand). No guest was needed.
- **The second opinion found what the first reader had not.** Both seats flagged the hook script's unquoted `$*`. Following that lead to what calls the script found PL-032, a root-level shell injection carried by every ROCKNIX image. The grading rule (every seat item a lead until re-read at its artifact) also refuted four seat claims and withdrew two. Each verdict names its artifact.
- **A failing control with every fixture:**
  - PL-006's four arm-root cases;
  - PL-017's `set -e` shape, run with and without `-e`;
  - S0's `system()` line reproducing #825's marker;
  - `--gated`'s own ungated copy;
  - fbalpha2019-lr's old recipe failing its checksum.

  Each control was seen to fail before its pass was believed.
- **Streams handed back without waiting.** The coordinator reviewed each stream in parallel. S0's fix was committed at 06:22:37 UTC and S6's record at 06:56:05 (the two commits' times).

## What was harder than expected

- **Timestamps.** Four times in one session a time was written that no clock or file had shown: 06:40 and 06:55 for work done at 06:10 and 06:12, then three proof times, then three friction-log times. Each was corrected in place and logged, but a rule that the session broke four times is not holding (friction log, 06:22).
- **A staged deletion swept into the wrong commit.** `git add <paths> && git commit` commits everything staged, so S5's `git rm` landed in the profiles commit. It was recut before push.
- **The environment the build runs in.** The table is ordered by `ls | sort`, so its byte-identity holds only in the C locale. A missing `env -i` made a correct regeneration look like a mismatch.
- **Stale paths in the brief.** The S0 brief's `generic-x64/build.ROCKNIX-...` root is gone. The live root at the same pin stood in, recorded as a delta.

## What we discovered

- **A shared source cache hides a source that changed upstream (#841).** A GitHub rename changed fbalpha2019-lr's archive bytes, because the top directory now carries the new name. Every build on this host passed only because the cache still held the old file; a build from an empty cache fails. Nothing on the fork checks a recipe's `PKG_URL` against its `PKG_SHA256` from an empty directory, so the same shape can be sitting in other recipes.
- **A key test that searches the source for a word over-counts what is read.** `core_updater_buildbot_url` occurs only as a menu label, and stage B counted it as read. A stricter test (the `SETTING_*` tables plus literal reads) under-counts, because keys built at run time fail it. Neither alone is the truth; S5 used the word test plus the one label-only key confirmed by reading.
- **The core updater's URL is set empty in every profile, which overrides RetroArch's built-in default.** It is harmless only because the updater is hidden.
- **0013 moved from clean to offset** after S0 grew 0012's hunk in the same file. A later patch in a series pays for an earlier one's growth. It is harmless at offset, but #839's re-cut will meet it.

## Adjustments for the next lane

These are proposals for the coordinator: this lane files only bug issues.
1. **Time from a clock, as a tool (the friction line of 06:22).** A one-line helper that stamps a log line from `date -u` (or from a named file's mtime), used for every running-log, work-log and friction entry, so a time cannot be typed. `working-principles.md`'s ladder: broken four times, it moves from *written* to *audited*.
2. **An empty-cache fetch check (#841's class).** A host tool that downloads each recipe's `PKG_URL` into an empty directory and compares the result with `PKG_SHA256`, run on a schedule rather than per build, since it is network-bound. It is the guard for the blindspot above.
3. **`git commit -- <paths>`** in every stream brief's commit step, or `git status --short` read before each commit. The stream rule already asks for an empty status *after* a commit; checking *before* would have caught S5's sweep.
4. **Regeneration tools set their own environment** (`env -i`, the C locale), as `s2-regen-check.sh` now does. A brief that tells a lane to run `regen-es-systems.sh` should name the wrapper.

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts` on the folder, full mode: **PASS**.
- The Phase 7 table: 34 of 34 items carry an outcome word with a commit or an issue. The `punch_index` agrees with the table, item for item (the lint's check).
- `tools/box-check` on #826, #817, #823, #824 and #841: 0 failures.
- Every stream commit cites its punch item and its bug or #650, with no closing keyword (`Refs`).
- `fixed-at: 3c47325fb2` is the last fix commit; no slice path changes after it on the branch.

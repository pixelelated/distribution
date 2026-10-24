# Mini Retro: M6.P2 T30, the standalone emulators (#677)

**Completed:** 2026-10-24

**Scope of this retro:** the T30 lane, from stage A through stage F:
- stage A: the slice's 543 paths, their bytes equal to `next`'s `8ebaf8daad`;
- stages A to D: the audit in `docs/audits/2026_10_24-epic-m6-emulators-standalone/`, which found 41 punch items (#872) and 19 bugs (#853-#871);
- stage E: the six fix streams S0-S5 of `docs/reviews/briefs/t30-streams.md` (`bf8184e494`);
- stage F: the proof rows.

Not retro'd here, because they are not this lane's:
- the coordinator's acceptance;
- the merge to `next`;
- the first image carrying the fixes.

**Branch:** `feature/m6-emulators-standalone-677`, `reviewed-at: c7e3dfcc87`, `fixed-at: f8a0f35931` (the last commit touching the slice).

**Delta:**
- **Code:** 47 commits on the slice's paths (49 files, +1,046 / -1,162), plus one new file outside it that the coordinator authorised: `rocknix/sources/scripts/link_storage_dir`. Highlights:
  - the Dolphin scripts went from 990 lines to 292 plus a shared library;
  - two dead files were removed;
  - five recipes are restamped by a recipe line: hatarisa, nanoboyadvance-sa and dolphin-sa by changes, supermodel-sa and yabasanshiro-sa by comments.
- **The punch list:** 41 items, all with a Phase 7 outcome.
  - **32 resolved:** 12 `fix-guest`, 15 `fixture`, 5 `tree`.
  - **9 deferred:**
    - PL-005 → #857 and PL-022 → #873, at integration;
    - PL-013 → #849;
    - PL-016 and PL-025 → the base merge;
    - PL-026 → #878;
    - PL-034 → #887;
    - PL-035 → #874;
    - PL-038's melonDS half → #888.
- **Bugs:** 19 filed at stage D. Two more filed in stage E from what the streams found: #886 (NanoBoyAdvance exits without a BIOS, and the image's open BIOS is never used; routed back into S4) and #887 (backups carry the RetroAchievements password and token through `melonDS.toml`). Checkboxes met by a guest or a fixture are ticked; the rest say why on their issue.
- **Proofs:** 36 lines in `00` and 36 `proved:` cells in `02`. G1-G16 and four stream cycles (S0, S1, S2, S4) ran on the guest, each with the census, the pidfile and `tools/vm-stop`.
- **Tools:**
  - five stream fixtures, `s0-fixtures.sh` to `s4-fixtures.sh`, each running the real lines from a commit or the worktree under the image's bash and busybox;
  - `s5-dolphin-split-check.py`;
  - `tick-checkboxes.py`;
  - `t30-routes.py`, from stage B.

## What the slice did to the two time-to-play numbers

**The exit path is where the slice moved time to play: three emulators could not be quit before and can now.** With the image's scripts, DuckStation, OpenBOR and Mupen64Plus's simple core survived the exit hotkey's kill (G1, G7, S2-G1, S2-G2), so game to game never ended for them. The hatarisa route exited 127 and never started. With the fixes, each one ends on its own kill target, and hatarisa draws EmuTOS in 0.36-0.42 s (S2-G3).

| Path | Before (audit, n=3) | After (stream cycles, n=3) | RetroArch (T3, same image) |
| --- | --- | --- | --- |
| Launch to first frame, gzdoom (Freedoom 0.13.0) | 3.13 / 1.03 / 1.11 s, the first cold (G14) | 0.94 / 0.99 / 1.00 s; the renamed WAD 0.92-0.99 s, which never launched before (S0-G2) | interface to first frame 0.62 s |
| Launch to first draw, ScummVM (FOTAQ) | 0.64-1.08 s (G15) | 0.59 / 0.66 / 0.69 s (S0-G2) | -- |
| Launch to first frame, hatarisa (EmuTOS) | exit 127 (G2) | 0.39 / 0.42 / 0.36 s (S2-G3) | -- |
| Exit to the interface | DuckStation, OpenBOR and mupen64plus-simple not ended | each ended by its kill target; the window is gone 0.15-0.17 s after the kill (gzdoom, ScummVM) | game to game 1.01 s |

Caveats on these numbers:
- The standalone numbers start at `runemu.sh` (an SSH launch), not at the interface's press, so they are not RetroArch's.
- gzdoom's "before" includes one cold start.
- Nothing on the launch path got slower in a measurable way. Mupen64Plus no longer copies the ROM into tmpfs before every launch. DaedalusX64 copies its binary only when it differs. amiberry and xemu no longer rewrite their configs every launch. DraStic compares its binary each launch, which is a `cmp` of one file.

## What worked well

- **Every fixture ran under the image's own tools.** The fixtures borrowed the GENERIC_X64 root's bash, GNU grep and busybox. That caught a busybox difference no host test would have: `cp -an src/. tgt/` into an existing folder copies nothing, so `link_storage_dir`'s first cut failed every site. It now copies file by file.
- **Each fix was seen against the base before it was trusted.** Every fixture ran first at the unfixed commit (8, 20, 2, 15 and 18 failures), and every guest cycle ran the image's script beside the fixed one. Three vacuous passes at the base were caught and tightened:
  - a missing command's 127 passing "non-zero";
  - DuckStation's unquoted switch reaching rc 1 through another branch;
  - the redirection grep splitting a file name with a space.
- **The overlay on `/usr/bin` made new files testable on the guest.** S1's new helper and S2's renamed script don't exist in the image, and a bind mount needs an existing file. An overlay's upper layer in `/storage` carried them, unmounted (lazily, when `input_sense` held it) before the stop.
- **The Dolphin split was proved by rebuilding, not by reading.** `s5-dolphin-split-check.py` inlines the library back into each script and compares it with the pre-split text, allowing only the two named edits. Pointed at an older base, it fails at S4's change.
- **Reading the pinned source settled two premises.**
  - melonDS's `Config.cpp` at the pin (fetched to scratch, because the cache held another commit) confirmed PL-034. That is #887.
  - NanoBoyAdvance's SDL frontend showed the brief's HLE premise false. That is #886, which the coordinator routed back as PL-014b.

## What was harder than expected

- **I blanked three issue bodies.** A shell `sed -e $e`, whose expression split on its spaces, produced an empty file, and `gh issue edit --body-file` wrote it to #863, #864 and #871. Each was restored a minute later from the copy saved before the edit, with equal content hashes, and each issue carries a note. `tick-checkboxes.py` now refuses an empty or over-broad change and reads the body back (friction line 11:28).
- **Copying helper blocks by line range kept bringing extra lines.** P2's helper lines 7-39 were copied into four guest scripts. Each time the range picked up a P2 line, and once three route launches ran again. The lines should have been lifted by marker, the way the fixtures already did it.
- **The fixture's own rewrites broke what they tested.**
  - Rewriting `/tmp` after the fixture root, which lives under `/workspace/tmp`, rewrote paths twice.
  - Rewriting `/storage` inside an escaped sed replacement broke Steam's VDF line.
  - Both were found by reading the case's output, not its verdict.
- **Typed numbers and times, again.** I said "21 PASS" for S4's 20-case fixture, and typed a cycle's naming time. Both were corrected from the artifacts. A comment's time now comes from its `created_at`.
- **`git add` refuses a path whose deletion is already staged** (a rename, a removal). Twice that dropped a commit out of a chain of per-package commits. They were recut by pathspec, and the empty status after each commit caught it.

## What we discovered

- **A kill target can name no process, and nothing checks it.** That was PL-001 to PL-004, and #838 carries the kill-name check as a comment.
- **Comparisons written as redirections leave files.** `[ "$X" > "0" ]` is true for any value and writes `/storage/0`. Ten sites made `0`, `1`, `2]` and a file named after a sha1. Each script removes its own empty leftover once.
- **"Link the folder" meant "delete the folder" at nine sites.** One helper replaces them, and it fails closed: the folder stays, and the emulator runs with it, when a copy can't be verified.
- **The image ships the answer to its own failure in two places.** NanoBoyAdvance's open BIOS was downloaded at build time, unchecked and never pointed at. melonDS's TOML is deleted every launch, which is how the interface's settings apply, and also how the credentials reach the backup (#887, #888).
- **A face-button swap applied to a kept file is an alternating toggle.** The fix records the swapped state as a hash beside the file, and normalises files the old script left swapped.

## Adjustments for the next lane

These are proposals for the coordinator: this lane files only bug issues.
1. **A guest-script helper library** (`desc`, `launch`, `finish`, `emu_pids`) as a file the guest scripts source, instead of a line range copied from P2. It was copied four times and picked up an extra line each time.
2. **`tick-checkboxes.py` promoted to `tools/`**, with the push guard's list and the index updated (`instruction-files.md`). Every lane ticks checkboxes, and the shell route has already blanked bodies once.
3. **An overlay helper for guest proofs of new files.** `tools/vm-serial` or `vm-qa` could mount an upper layer over `/usr/bin` and detach it, with the lazy unmount named, so a fixed script set can be proved before an image.
4. **The log-stamp tool (#843)** still stands. A typed time recurred here too.
5. From the audit, still open: the kill-name check (#838's comment), standalone coverage in `tools/emulator-exit-test` (#875), and shellcheck in the fork CI (#876).

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts --phase pre-issue --issue 872`: **PASS**. The full-mode lint and `audit-completion.json` follow #872's close.
- The Phase 7 table: 41 of 41 items carry an outcome word with a commit or an issue.
- Criterion 12: 36 `proved:` cells in `02` and 36 proof lines in `00`.
- Every stream commit cites its punch item and its bug or #872 with `Refs`, never a closing keyword. `fixed-at: f8a0f35931` is the last commit touching the slice.
- The stream fixtures on the final tree: S0 14/14, S1 22/22, S2 2/2, S3 14 plus 1 SKIP (the removed script), S4 19 plus 1 DEFERRED (#888). The split check passes, and its control fails.

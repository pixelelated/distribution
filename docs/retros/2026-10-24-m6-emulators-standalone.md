# Mini Retro: M6.P2 T30, the standalone emulators (#677)

**Status: draft at the stage-D pause.** The answers below cover stages A to D.
The streams (stage E), the `proved:` cells and completion marker (stage F)
and the close-out are added when they happen, and the retro is posted on
#677 at stage G.

**Scope of this retro:** the T30 lane from stage A to the stage-D pause:
- stage A: the slice's 543 paths, their bytes equal to `next`'s `8ebaf8daad`;
- the audit, stages A to D, in `docs/audits/2026_10_24-epic-m6-emulators-standalone/`.

The punch list is #872: 41 items and 19 bugs, #853 to #871.

Not retro'd here, because they are not this lane's:
- the coordinator's stream briefs and acceptance;
- the merge to `next`;
- the first image carrying the fixes.

**Branch:** `feature/m6-emulators-standalone-677`, `reviewed-at: c7e3dfcc87`. `fixed-at` is set at stage H.

**Delta at the pause:**
- **Code:** none. `git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/standalone` is empty.
- **The punch list:** 41 items, 2 High (PL-007, PL-012), 16 Medium and 23 Low.
  - The Phase 7 gate is mostly `open`.
  - Deferred by disposition: PL-013 (#849, the portaudio source), PL-016 and PL-025 (class 1, the base merge).
- **Proofs:** 21 lines in `00` and 21 `proved:` cells in `02`. H1 to H5 ran on the host; G1 to G16 ran on the guest, over three cycles, each with the census, the pidfile and `tools/vm-stop`.
- **Tools:** `tools/t30-routes.py`, new. It resolves each image table's standalone routes the way `runemu.sh` does, and has a failing control (rc 1). The T3 tools were copied with provenance headers; `q4-pins.py` reads `standalone/`.

## What the slice did to the two time-to-play numbers

**Nothing has changed yet, because no fix has landed.** These are the standalone measurements, beside RetroArch's.

| Path | Standalone (this slice, n=3) | RetroArch (T3, same image) |
| --- | --- | --- |
| Launch to the emulator's process, `runemu.sh` start (G12) | ppsspp 0.61 / 0.63 / 0.63 s, x64sc 0.62 / 0.67 / 0.56 s, DuckStation 0.62 / 0.53 / 0.52 s | -- |
| Launch to first frame, real free content (G14, G15) | gzdoom (Freedoom 0.13.0) 3.13 / 1.03 / 1.11 s, the first cold; ScummVM (FOTAQ) to its splash 0.64 to 1.08 s | interface to first frame 0.62 s |
| Exit to the interface | gzdoom and ScummVM: the kill target works and the interface frame returns. DuckStation, OpenBOR and mupen64plus-simple survive the kill (G1, G7) | game to game 1.01 s |

These numbers are not interchangeable:
- The standalone numbers start at `runemu.sh`, because an SSH launch skips the interface's own launch path. T3's start at the interface's press.
- A launch driven from the interface is still owed for the standalones (`04` § Q5).

What sits on the standalone launch path before `exec` (`04` § Q5):
- Dolphin runs two Python helpers and about forty `sed -i` passes. DuckStation runs one helper and five passes. Each measured helper costs 0.02 to 0.07 s.
- Mupen64Plus copies the whole ROM into tmpfs (F-29).
- DaedalusX64 and amiberry copy files on every launch (F-11, F-15).

The streams' effect on these numbers goes here at stage G.

**The exit number matters more than the launch number here.** If the kill does not end the emulator, the player has no exit to the interface, so the game-to-game number never ends. PL-001's class is the time-to-play defect of this slice.

## What worked well

- **The route tool decided the dead-end questions mechanically.** `t30-routes.py` resolves the three images' tables the way `runemu.sh` does. It produced the routes that exit 127 on GENERIC_X64 (hatarisa, the nds default drastic, amiberry, the saturn default yabasanshiro) from the tables alone, and G2 then confirmed them on the guest. Its control was seen to fail (rc 1) once the piped `tail` that masked it was removed.
- **Real free content gave real frames.** Freedoom 0.13.0 and Flight of the Amazon Queen, checksummed under `/workspace/tmp/m6-t30/content/`, turned "the process started" into "the first frame drew" for two emulators. They also proved the two kill targets that do work.
- **Running the seats on different packets, and saying so.** Gemini's first run truncated three times at the same ceiling. The lane held, posted the numbers, and the coordinator chose a trimmed packet (D-WORKFLOW-195) rather than a substitute seat. `04` § Second opinion marks every item that seat saw only in excerpt.
- **A seat claim became a High through a guest proof, not through grading.** Gemini's G-03 was a lead. Cycle 3 (G16) proved it: the Tools launcher's DuckStation creates `savestates` as a real directory, and the next game launch deletes it. That is what moved F-12 to High; the seat's wording alone did not.
- **Grading refuted as well as added.** G-09 and G-45 were refuted at their artifacts, and G-08 and G-28 narrowed. The F-09, F-11 and F-30 wordings were corrected. Twelve new findings came in, F-31 to F-42.

## What was harder than expected

- **Typed times, again.** The stage-B checkpoint heading said 08:53 for a comment created at 08:43, the running log started at a tool's printed time (08:28 for 08:30), and three proof times were typed before they were replaced from artifact mtimes. T3 had broken the same rule four times the same morning. The friction line at 08:46 cites #843. Two lanes in one morning means writing the rule down is not enough.
- **Guest fixtures that changed what they measured:**
  - Cycle 1's exit sweep killed EmulationStation eight times, because the kill data already read `emulationstation` when no emulator had started. P2 kills only a live emulator.
  - C8's restore deleted the shipped `global.retroachievements=0` instead of restoring it. It was put back to 0.

  Both were found by reading the guest after the run, not from the fixture's own output.
- **A seat's output budget is fixed by the packet.** The 438,502-byte packet drove Argon to about 57,000 reasoning tokens of a 65,536 ceiling, three times. T3's 308 KB packet took it 30,337. Nothing measures that before the call.
- **Tooling edges, each costing a re-run:**
  - `comm` refused Python's codepoint order outside the C locale.
  - `generic-x64-vm --monitor` takes a path, not `unix:`.
  - The AppImage's first `hsqs` match was not its superblock.
  - The Facilitator's `--help` gives timeouts that its code does not use.
  - A bare `pkgcheck` prints the whole tree, which read like a single run.
  - A missing `/` in the `04` generator left a partial append.
- **The copied tools carried T3's constants.** `q4-pins.py` hardcoded 151 rows, as well as the `libretro/` path the brief named. The rc 1 came from the count, not the path.

## What we discovered

- **A kill name can name no process at all.** Busybox `killall` matches comm, argv0 or the exe basename:
  - DuckStation's `AppRun.wrapped` is none of those, because `AppRun` execs `duckstation-qt`.
  - OpenBOR writes no target.
  - mupen64plus-simple's process is not `mupen64plus`.

  Nothing on the fork checks that the name a start script writes resolves to a binary the image carries. `tools/emulator-exit-test` drives RetroArch only.
- **#825's class reaches the standalone launchers.** A `.scummvm` file goes through `eval` as root (PL-007). An apostrophe in a WAD's name stops `xargs`, so gzdoom never starts. Both are a player's own file name.
- **"Link the directory" deletes what is there.** Nine sites remove a real directory before linking it to `/storage/roms/...`, with no copy, and G16 shows the shipped Tools launcher creates exactly that real directory. The upgrade question (`Already written:`) is in each bug's trace.
- **A comparison written as a redirection writes a file.** `[ "$IRES" > "0" ]` creates `/storage/0` from EmulationStation's working directory, and is true for every value.
- **Achievements sign-in state differs by emulator.** After an offline account change or a refused sign-in, the switch is on and the token empty. ppsspp and flycast then keep the old token and their enabled flag, dolphin clears both, and melonDS disables and keeps the credentials.
- **A dead primary URL can be hidden twice (#849, the portaudio 404).** I took the shared cache for the only copy. ROCKNIX's source mirror (`scripts/get_archive:23,35`) also serves the archive with the recipe's sha256, so an empty-cache build succeeds. The coordinator caught that, not this lane. The finding is Low, but a fetch check for #841's class needs two answers per recipe: the primary URL and the mirror.

## Adjustments for the next lane

These are proposals for the coordinator: this lane files only bug issues.
1. **The log-stamp tool now (#843).** T3 proposed it, and T30 broke the rule the same morning. Under `working-principles.md`'s ladder, a rule broken by two lanes in one day moves to *audited*.
2. **A kill-target check.** For every start script, the name it writes to `/tmp/.process-kill-data` must resolve to an executable in the install tree, by comm, argv0 or basename. `t30-routes.py` already does the table half.
3. **Standalone coverage in `tools/emulator-exit-test`,** for the nine standalones the guest ships, using free content where it exists.
4. **shellcheck over the start and achievements scripts,** at least SC2071 (`>` in `[ ]`) and SC2086, as a `vm-qa` suite or a host lint.
5. **One `link_storage_dir` helper** in `001-functions`: copy, verify, then link, used by F-12's nine sites.
6. **A packet-size note in the Facilitator's run guide:** Argon's reasoning grows with the packet, and T3's 308 KB took 30,337 tokens while T30's 438 KB hit the 65,536 ceiling. Fix the stale `--help` timeouts at the same time.
7. **A fixture reads the guest's state before and after itself.** Cycle 1's ES kills and C8's deleted key would both have shown in a before/after diff of the files and processes the fixture touches.

## Scoped audit (at the pause)

- `tools/lint-audit-artifacts --phase pre-issue --issue 872`: **PASS pre-issue artifacts**.
- `tools/box-check`: 0 failures on #872 (41 checkboxes) and on each of #853 to #871.
- Criterion 12: 21 `proved:` cells in `02`, and 21 `^(GUEST-PROOF|PROOF):` lines in `00`.
- Membership: the diff of the 543 against the hash export is empty.
- The full-mode lint, the Phase 7 outcomes and `audit-completion.json` come at stage F, after #872 closes.

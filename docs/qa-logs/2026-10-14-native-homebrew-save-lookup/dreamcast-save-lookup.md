# Bounded save-capable Dreamcast lookup

The concrete candidate is [Viktor Gars's Tetris 2](https://github.com/vg132/dreamcast-tetris-2/tree/1390da9766a835c3ee62aabba770acee9f2e68fa),
commit `1390da9766a835c3ee62aabba770acee9f2e68fa`, under its BSD-3-Clause
license. Its original author repository includes a precompiled boot binary,
bootstrap header and game assets. `tetris2-candidate.json` records exact source,
asset, license, binary and inspected Flycast identities. This improves the fixture
choice; it is not a prepared disc or a passing native save test.

Confirmed source chain:

- `src/tetris.cpp:80` awards points for a landed block. At game over, lines 89–91
  call `SetHighScore()` then the game's `Save()` when game autosave is enabled.
- `src/game.cpp:174` serializes high-score names, dates and scores with game
  options, compresses them, creates a VMU package and calls
  `m_pVMU->Write(dev,"tetris2.sys",...)`. `Load()` reads that file and restores
  the score table. This is ordinary game data, separate from emulator states.
- `src/control.cpp:530` provides a menu path that selects an actual VMU and calls
  Save; the adjacent Load menu calls Load. Source does not justify treating a
  successful-looking menu transition as successful persistence.
- The author's `dreamcast-common` at
  `42153a864fb0f725d5f9b8916b2f919a8217dd7f`, `src/vmu.cpp:174`, writes through
  `fs_open`, `fs_write`, `fs_close`. Its return is not checked by the game Save
  function. Require disk bytes plus cold-relaunch score recovery.

Cached official files, fetched only after inspecting the save calls and license:

| File | Bytes | SHA256 |
|---|---:|---|
| build/1ST_READ.BIN | 587,456 | `065db55aab9b166f2a690654e906d62d9c839805cb7fd57fd3ffe900580f16b8` |
| build/IP.BIN | 32,768 | `ed98b488a9f139b804e99387e25508432c7f9dd27208c1cb33ad5b8c5f8ef019` |

Their exact Git blob IDs also match the pinned author's tree. Local paths are
`/tmp/pix-m7-native-homebrew-20261014/tetris2/build-1ST_READ.BIN` and
`build-IP.BIN`. No binary/source equivalence through a rebuild has been claimed.
No additional game binary, SDK or compiler was downloaded or run in this lookup.

## Loader result: a disc is required

Pinned Flycast `5aa091fde632fb332c8d8c34e280d62dc951954c` explicitly maps
`.bin`, `.dat` and `.lst` to **NAOMI**, in `core/emulator.cpp:556`. A raw
`1ST_READ.BIN` is therefore not a direct Dreamcast launch route. Its console
direct-load special case is `.elf`; `core/reios/reios_elf.cpp:30` validates an
actual ELF structure. Renaming the file is insufficient. That branch initializes
an empty disc drive (`core/emulator.cpp:635`).

Tetris 2 loads `/cd/graphics/...` and `/cd/themes/default/viperv6.theme`, whose
eleven image paths are also under `/cd/themes/default/`. An ELF wrapper alone
would not supply this filesystem. The source includes no standalone ELF release.
Do not claim that Flycast accepts this fixture just because another homebrew ELF
worked or a file filter includes `.bin`.

## Minimal remaining preparation

1. Fetch only the 54 asset files listed by exact Git blob ID in
   `tetris2-candidate.json`: graphics (632,871 B), sounds (68,978 B), and the
   complete default theme (4,382,241 B), total **5,084,090 bytes**. Strip the
   `Tetris CD/` prefix into a fresh disc root. This omits optional themes; the
   default theme's references are self-contained. Preserve the author license.
2. Obtain an already available, coordinator-admitted disc-authoring tool and bind
   its executable/source hash. No `mkdcdisc`, `mkisofs`, `genisoimage`, `xorriso`
   or `cdi4dc` was found in this worker's PATH, nor those names under the accepted
   parent toolchain's bin/sbin. This is bounded lookup, not proof they exist
   nowhere. No tool build or installation is proposed in this task.
3. Confirm whether the author's boot binary is scrambled. The filename is not
   proof. Use the pinned author packaging record or a static SH-4 bootstrap
   inspection with a known transform and expected entry sequence. Do not simply
   try flags until one appears to run and then relabel the artifact.
4. With that fact and an admitted `mkdcdisc`, the intended operation is a normal
   CDI with the exact boot binary, the staged directory contents and author
   bootstrap. The primary [mkdcdisc examples](https://gitlab.com/simulant/mkdcdisc/-/blob/main/docs/examples.md)
   distinguish `-b` (unscrambled) from `-B` (scrambled), and `-D` adds directory
   contents. Bind the actual tool revision/CLI before executing this template:

   ```sh
   "$MKDCDISC" "$CONFIRMED_BOOT_MODE" "$TETRIS_BOOT_BIN" \
     -D "$TETRIS_DISC_ROOT" -p "$TETRIS_IP_BIN" -o "$TETRIS_CDI"
   ```

   `CONFIRMED_BOOT_MODE` must be the reviewed `-b` or `-B`, not a guess. Keep the
   normal padding policy; budget up to 1 GiB scratch until that tool's output
   size is known. Retain original command exit and CDI hash. Source-only worker
   has done none of these packaging/runtime steps.
5. Stage the resulting hashed `.cdi` under `/storage/roms/dreamcast/` in the
   existing admitted offline QA guest. Select native flycast/flycast-sa with
   OpenGL, controller and fresh VMU. The actual installed route is:

   ```sh
   /usr/bin/runemu.sh /storage/roms/dreamcast/Tetris2-M7.cdi \
     -Pdreamcast --core=flycast-sa --emulator=flycast --controllers="$CONTROLLERSCONFIG"
   ```

For the eventual save observation, first use the game's explicit VMU Save menu
on fresh storage to select/bind the card; record the baseline score table/card.
Play a short round to a nonzero score and game over, then save from the game's
menu. Retain the observed score/name and changed VMU bytes, cleanly exit, and
relaunch with native auto-state loading disabled. Require that the same high score
is restored from `tetris2.sys`. Do not inject a fabricated score or state file.
The game implements its own automatic score save; that must not be confused with
Flycast automatic emulator state. If the old binary fails, preserve the failure;
the source has unchecked allocation/write paths, so suitability remains unproven.

## Alternatives checked and stopped

DCSquares has real score-save calls and an author-hosted 42,018,904-byte CDI ZIP,
but inspected source uses an external GOAT score library and provided no clear
license grant in its inspected files. No binary was downloaded. Dreamino's author
page establishes gameplay and VMU display, not persisted game scores; no binary
was downloaded. The initial 2048 repository searches found no suitable source.
Fruit'Y's author page is lawful distribution but did not establish source/save
calls within this bounded lookup; no binary was downloaded. BASIC remains a useful
VMU I/O control and is not relabeled as an in-game save.

This candidate and its remaining disc preparation can proceed after the
engineering image work. It adds no image dependency, new release criterion,
account/provider action or #581 memory-card gate.

# T2's stream briefs: EmulationStation's launch path, #790, in five streams (#649)

Written by the coordinator at T2's stage-D pause (2026-10-23; plan § 6b
stage E; D-WORKFLOW-189: a brief is planning; the shape is D-WORKFLOW-056's).
One section below is one stream brief. The lane that runs them is the T2
lane, alone, in its two worktrees, on its two branches, in the order given;
the per-item specification is the punch item in
`docs/audits/2026_10_23-epic-m6-es-launch-path/05-punch-list.md` (its
*What*, *Where*, *Already written* and *Acceptance*; the `bug` issues #767
to #789 point there), and this document does not restate it. Where this
document and an item differ, the item's text is the fact and this
document's grouping is the plan; say so on #649 and go on.

**What every stream shares.**

- **Two branches.** Source changes land on the ES branch
  `feature/m6-es-launch-path-649` in
  `/home/max/Development/emulationstation-next.worktrees/m6-es-launch-path-649`
  (from the pin `16dbac5211`; pushed to `origin`); the audit artifacts, the
  running log, the work log and the pointer on the distribution branch in
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649`,
  from its tip at the pause (`0d3febfc29`) after merging the coordinator
  tip that carries this document. One commit series per stream on the ES
  branch, headed by a commit whose subject names the stream
  (`emulationstation: stream S1, the command and the state file`) and
  whose body lists the items it takes; then one commit per item, or one
  per coherent group one change fixes (say which in the body).
- **The files owned** are listed per stream as files or line ranges of
  the pin's numbering; `FileData.cpp` is split between streams by range.
  Two streams never edit one file in interleaved commits: finish a stream
  before the next starts. A fix that needs a file outside the twenty (an
  `es-core` file, `GuiSaveState.cpp`, `OfflineAchievements.cpp`,
  `Scripting.cpp`, `FileSystemUtil.cpp`) stays open with the reason and a
  lead on #649 for that slice; the item's Phase 7 outcome is `deferred:`
  to that slice's issue.
- **The test first, and the failure seen.** Every `bug` issue's second
  criterion asks that the check was run against the unfixed source and
  failed. The compile-side floor is the brief's (§ 5): a doctest case in
  `es-app/tests/unit` where the code is pure (`LaunchCommandTests.cpp`,
  `SaveStateJobQueueTests.cpp`, a new file beside them for a function the
  fix extracts), a case in `tests/app-unit` (`proxycards-tests`,
  `bookkeeper-tests`) or in the python harnesses
  (`tests/launch-deferred-state.py`, `tests/launch-capture-gate.py`,
  `tests/hasher-offline-index.py`) where they already compile the
  function; the case written and seen to fail on the pin's code, then the
  fix, then the pass, both runs named in the commit body with their
  commands. A fix with no pure seam to test gets its walk written now
  (`tools/vm-walks/<name>.steps`, the frames it will file, the fixture it
  needs under `/storage`) and its `proved:` cell reads
  `fix-walk-pending-image`: the coordinator runs it at the first image
  carrying the pin (brief § 6, Verification; plan § 6b stage H).
- **The syntax-only compile before every ES commit that touches a
  `.cpp`**, with the recipe of brief § 5 (or `tools/es-syntax-check --root
  ... --tree ...` once #699's fix is on the distribution branch), and the
  unit tests run; the running log names, under a timestamp earlier than
  the commit's, the `PASS <file>` line and the test line (criterion 13).
  Never the compile command's text in any artifact (it carries the
  build's credential-shaped define).
- **`Already written:` in every bug fix's commit body**, copied from the
  item and corrected if the fix's shape changed it (D-WORKFLOW-050); a fix
  that changes what the interface writes to `es_settings.cfg`,
  `system.cfg`, a gamelist, a save-state file or a stamp says what the old
  writer already left on devices and how the new reader treats it.
- **Commit shape (the ES repository's):** subject `<Area>: <what changed>`
  under 72 characters (`SaveState: quote the state file into the command`,
  `FileData: refuse a DELETE GAME path outside the game's folder`); a
  blank line; a body with the item ids, `Refs pixelelated/distribution#649,
  pixelelated/distribution#7NN` (no closing keyword), the two test runs,
  the `Already written:` line; the trailer `Co-Authored-By: Claude Opus
  5.5 <noreply@anthropic.com>`. Never `--no-verify`; never a bare `git
  stash`; the ES repository's hooks run on every commit.
- **Every string a player reads** follows `es-player-text.md` and ships
  with its French in the same commit (D-UI-051; `tools/es-untranslated`
  prints `0 without` at the tip); ASCII only in a comment near `_()`; a
  copy-only edit is a screen-content change (D-WORKFLOW-155/156): the flow
  reference it touches in `docs/es-menu-map.md` (the distribution
  worktree) updated in the same change, and its frame at 640x480 owed at
  the image (`fix-walk-pending-image`). `tools/es-menu-map-check` prints
  `0 missing` at the tip.
- **The seam with T1.** T1's `runemu.sh` at its branch tip (read-only:
  `git -C /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346
  show origin/feature/m6-os-launch-control-state-648:projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh`)
  now reads `--core=` and `--emulator=` as whole arguments, the last
  winning (#730, `fe3e832e4a`), reads `--host` and `--connect` (lines 317
  and 321), and splices the netplay options only when every character is
  one an option needs (#702). A change here that would hand the launcher
  an argument it does not read, or a character its splice refuses, is
  announced on #648 before the commit and the item waits; the two readers
  of the `-P`, `--core=`, `--emulator=` tokens must agree at both tips,
  and `LaunchCommandTests.cpp`'s `runemu` stand-in is updated to T1's
  reading in S1 with T1's commit cited.
- **Phase 7 outcomes** are written into `05-punch-list.md`'s index and
  the audit issue #790 as each item ends: `resolved` with the commit,
  `deferred` to the issue named below, `withdrawn` with the artifact that
  refutes it. Decided here, not per item:
  1. **Upstream commits (PL-033, Q4):** a batocera commit is cherry-picked
     with `-x` onto the ES branch only where a stream's item needs it (S3
     and S4 below), each pick compiled and tested like a fix; a pick that
     conflicts with fork-own lines is not resolved by hand here (the item
     is fixed the fork's way and the commit stays in the list). The rest
     of the six are `deferred:#791` (the ES upstream sync, the
     coordinator's).
  2. **Another slice's path:** PL-029 is `deferred:#684` (T37, the
     recipe's `start_es.sh`), with its lead already on the list.
  3. **A removal upstream still carries** (PL-027, `renumberSlots`, and
     PL-028's dead members if batocera still declares them): a row in
     `04-analysis.md` § Q6 and a line on #585 (the contribution queue),
     not a removal here (brief § 4 Q6's rule); `resolved` by the row.
  4. **A restructuring** (PL-032, `launchGame`'s 400 lines): a row with
     the proposed split in `04-analysis.md` § Q7, and `deferred:` to the
     Backlog issue the coordinator files at acceptance; no restructuring
     without a binary to prove it on.
- **The guest.** No image carries a fix until the coordinator's pin bump
  reaches one (D-WORKFLOW-191 open), so stage F here is the tests, the
  syntax compiles, the walks written, and the re-run of the four host
  checks and the unit tests at the ES tip. The guest from
  `/workspace/artifacts/m6-t2-20261023/` comes up only for a proof the
  pin's binary can still give (a reproduction a fix's walk needs, a
  measurement); down when it ends.

## S1. The command and the state file (High first)

- **Items, in this order:** PL-001 #767 (High), PL-007 #773 (Medium),
  PL-021 #787, PL-034 (Q5, the unconditional input scan), PL-031 (Q7, the
  nickname written from the builder).
- **Files owned:** `es-app/src/SaveState.cpp` lines 60 to 161
  (`setupSaveState`'s argument building); `es-app/src/FileData.cpp` lines
  520 to 723 (`formatCommandLineArgument`, `getlaunchCommand`);
  `es-app/src/LaunchCommand.h`; `es-app/tests/unit/LaunchCommandTests.cpp`.
- **The fixes:** per item. The shape they share: a value that reaches the
  shell is one argument, quoted by `Utils::String::shellQuote`, at the
  call site that inserts it (the state file at 77, 97 and 111; the
  placeholders at 618 to 630 and the nickname and controllers blob at 647
  to 657; `formatCommandLineArgument` retired or made to quote fully); the
  readers in `LaunchCommand.h` keep a value's quoting out of the token and
  treat an explicitly empty value as present; the input scan runs only
  when the controllers blob is used (PL-034); the netplay nickname is
  written where a setting is chosen, not from the builder (PL-031, a row
  if the move is not small).
- **The test first:** `LaunchCommandTests.cpp` extended: a case per reader
  with a quoted value and an empty value; the `runemu` stand-in brought to
  T1's reading (#730) with the commit cited, so the case that says where
  the two readings part company now says they agree. A new pure function
  for the placeholder quoting (extracted from `getlaunchCommand`) with its
  own doctest file beside the others: one case per placeholder with a
  fixture name containing a space, a quote and a dollar sign, asserting
  one argument out. The credential-quoting harness
  (`tests/credential-quoting.py`) re-run at the tip (still `0 bare`). The
  guest walk for PL-001 and PL-007 (G-6's `$HOME`-named ROM by reference)
  written, `fix-walk-pending-image`.
- **Already written:** per item; PL-001's reads save-state files whose
  names already carry such characters (the fix launches them; the old
  code never did).

## S2. DELETE GAME and the save-state files

- **Items, in this order:** PL-002 #768 (Medium), PL-017 #783, PL-016
  #782, PL-012 #778, PL-023 #789, PL-027 (row and #585), PL-035's
  `SaveState.cpp` half (Q7).
- **Files owned:** `es-app/src/FileData.cpp` lines 1380 to 1510 (the
  delete); `es-app/src/SaveState.cpp` less S1's lines;
  `es-app/src/SaveStateBookkeeper.cpp`; `es-app/src/SaveStateConfigFile.cpp`
  (upstream-identical today: the fix diverges it, say so in the commit and
  on #585); `es-app/src/SaveStateRepository.cpp` (the row only).
- **The fixes:** per item. PL-002: a delete removes a disc the game's
  `.m3u`, `.cue` or `.gdi` lists only when that path resolves inside the
  game's folder, and removes every disc it lists there (the item's two
  halves); PL-017: the fallback NEW GAME path restores the `.bak`; PL-016:
  copy and remove report the file operations' results; PL-012: the
  retry is bounded with an outcome; PL-023: the cache under the lock,
  cleared on reload.
- **The test first:** the path filter of the delete extracted as a pure
  function (a folder, a listed path, in or out) with a doctest file; the
  bookkeeper's retry in `tests/app-unit`'s `bookkeeper-tests`; the
  save-state copy and remove in a doctest on a temporary directory; the
  walk for PL-002 with a fixture `.m3u` under `/storage` naming a disc in
  the folder and a path outside it, `fix-walk-pending-image`.
- **Already written:** PL-002's reads what such deletes already removed
  on devices (gone; the fix stops it; a game whose discs were left is
  cleaned by the next DELETE GAME); PL-017's reads `.bak` files already
  left beside auto saves (the fix restores on the next launch, say which).

## S3. The systems table

- **Items, in this order:** PL-033's `SystemData` commits that PL-015
  needs (`b69fb143c` by hand, with the depth passed to the rescan's
  `populateFolder`; `d17cf003e` if clean), then PL-003 #769 (Medium),
  PL-020 #786, PL-004 #770 (Medium), PL-005 #771 (Medium), PL-015 #781.
- **Files owned:** `es-app/src/SystemData.cpp` and `.h`;
  `es-app/src/FileData.cpp` lines 1650 to 1670 (the stored sort).
- **The fixes:** per item. PL-003 and PL-020: the folder filter matches a
  path component, not a substring, and a folder already in the map is not
  leaked; PL-004: an unreadable overlay is logged and the loop continues
  (`continue`, not `return`, at 1042 and 1049); PL-005: a stored sort id
  is bounded before it indexes the list; PL-015: the rescan walks
  sub-folders and keeps a multi-disc game's tracks hidden.
- **The test first:** the overlay loop and the folder filter extracted as
  pure functions with doctest cases (an overlay that fails to parse
  followed by one that parses; a path with `ports` inside a longer
  component); the sort bound in a doctest; the rescan in the walk with a
  fixture tree under `/storage/roms`, `fix-walk-pending-image`.
- **Already written:** PL-005's reads sort ids already stored in
  `es_settings.cfg` (the fix bounds them; nothing migrates); PL-004's
  reads overlays already ignored on devices (they load after the fix:
  say so, a behaviour a player sees).

## S4. The launch chain

- **Items, in this order:** PL-033's `ViewController` commits
  (`308221458`, `5f106acce`, `0806a0c5c`, in that order, before PL-014),
  then PL-014 #780, PL-008 #774, PL-013 #779, PL-018 #784, PL-009 #775,
  PL-019 #785, PL-022 #788, PL-035's `ViewController` half (Q7), PL-032
  (the row and the Backlog deferral).
- **Files owned:** `es-app/src/views/ViewController.cpp` and `.h`;
  `es-app/src/FileData.cpp` lines 90 to 110 and 760 to 1330; `es-app/src/FileData.h`;
  `es-app/src/ProxyCards.cpp` lines 240 to 275.
- **The fixes:** per item. PL-014: the gates ask before the transition and
  the splash, and a refusal shows the view again; PL-008: a deferred
  launch holds a liveness token (a path or an id looked up when it fires,
  never the raw pointer across the wait); PL-013: the running game's
  pointer behind an atomic or a lock, read through one accessor; PL-018:
  PLAY NOW's permission belongs to the launch that answered; PL-009: a
  finished capture's exit sync runs even when the waiting launch is
  refused; PL-019: the play time ends when the command returns; PL-022:
  the top-up card is made only while the screen is free.
- **The test first:** `tests/launch-deferred-state.py` and
  `tests/launch-capture-gate.py` already compile `launchNow` and
  `captureGate`: a case each for the token, the permission and the
  dropped sync, seen to fail on the pin; `proxycards-tests` for PL-022;
  the gate order in the walk (a sync fixture the guest can stage: a
  stub `cloud_backup` under `/storage` that sleeps), `fix-walk-pending-image`.
- **Already written:** PL-019's reads play times already recorded in
  gamelists (the fix changes what is added; nothing migrates: say so).

## S5. The process and the words

- **Items, in this order:** PL-006 #772 (Medium), PL-010 #776, PL-011
  #777, PL-024, PL-025, PL-026 (Q2, the strings), PL-030 (Q7, the
  comments).
- **Files owned:** `es-app/src/main.cpp`; `es-app/src/FileData.cpp` lines
  650 to 700 (the netplay client branch) and 724 to 765 (the error box's
  strings); `locale/lang/fr/LC_MESSAGES/emulationstation2.po` for the
  strings; `docs/es-menu-map.md` in the distribution worktree for the
  flows the strings sit in.
- **The fixes:** per item. PL-006: the boot game's command is rebuilt from
  the current table at boot (or the stored command is validated against
  it), never replayed blind; PL-010: the spectator mode, the relay session
  and the client password reach the launcher **as arguments T1's
  `runemu.sh` reads at its tip** (the seam rule above: read it first; if
  the launcher reads none of the three, the item waits on an announcement
  on #648 and T1's answer); PL-011: every flag that takes a value checks
  for it; the three string items in the player's register with their
  French and the flow reference updated; PL-030: the comments match the
  code (the renumbering comment at 1134 among them).
- **The test first:** `parseArgs` in a doctest (`CommandLineTests.cpp`
  exists); the boot game's command check as a pure function with a case;
  the strings by `tools/es-untranslated` and `tools/vocabulary-check` at
  the tip; the walks for the error box and the start-up messages,
  `fix-walk-pending-image`.
- **Already written:** PL-006's reads `global.bootgame.cmd` already stored
  on devices (the fix validates or rebuilds it; an old stored command that
  no longer matches the table is dropped with a log line, say so).

## After the five streams: stage F and the hand-back

- Re-run at the ES tip and record beside the stage-B lines: the unit
  tests (`0 failed`, the assertion count), `tests/app-unit`'s three
  targets, the three python harnesses, `tests/credential-quoting.py`,
  `tools/es-menu-map-check`, `tools/es-untranslated`, `tools/vocabulary-check`,
  the syntax recipe over every `.cpp` the branch touched
  (`git -C "$W" diff --name-only $PIN..HEAD -- '*.cpp'`); the guest only
  for what the pin's binary can show.
- `tools/lint-audit-artifacts <folder>` prints `PASS`; every item of #790
  at an outcome; `tools/box-check --issue 790` and on every `bug` issue
  still open; the walks listed in `02-forward-audit.md` with their
  `proved:` cells, one row per fix the image will prove.
- The retro (stage G), then the hand-back (brief § 10): `reviewed-at:`,
  `fixed-at:` and `fixed-at-es:` into #649, both branch tips, the
  hand-back comment, idle. The coordinator accepts (re-running the recipe
  and the tests), writes the hashes into `slices.json`, merges the ES
  branch into `test/qa-integration` and bumps the pin, and #649 stays
  `remediating` until the first image with that pin proves the walks
  (D-WORKFLOW-191; plan § 6b stage H).

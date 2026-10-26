# Futro: the interface area epic (#700), at T2's kickoff (#649)

**Prepared:** 2026-10-23, by the coordinator lane (Fable; D-WORKFLOW-189: the
futro of an area epic is planning).
**Scope of this futro:** the area epic #700 (`interface`: T2 #649, T18 #665,
T20 #667, T21 #668, T26 #673, T31 #678, T32 #679, T33 #680, T34 #681, T35
#682, T36 #683, T37 #684, T44 #691) at its first sub-issue's dispatch, T2,
run from `docs/reviews/briefs/es-launch-path.md`. It does not cover the
twelve later slices beyond what T2 learns for them; each gets its own
kickoff note on this epic when it is dispatched. T2 runs beside T1 (#648,
the OS scripts' launch path), the maintainer's call of the same day
(D-WORKFLOW-190).

**Upstream retro consulted:** P1's, `docs/retros/2026-10-23-m6-p1-survey.md`
(#641 comment 6358092855); T1 has no retro yet (it is at Phase 5 as this is
written) and no addendum exists. T1's futro
(`docs/futros/2026-10-23-m6-os-scripts-and-launch.md`) and the stranger's
proof of T1's brief (its § 10) are the nearest prior learning and are taken
as input for question 3.
**Inputs considered:** #700's and #649's bodies; the brief, version 1
(`289a95eb05`; `55ea579bcf` named it and did not carry it, a `commit -a`); `docs/reviews/order.md` § T2 and § The security,
state-preservation and launch-path files; `slices.json`'s T2 record; the
inventory's twenty `es` rows; `docs/reviews/plan-for-the-plan.md` § 3, § 4,
§ 6b, § 6c, § 7, § 8, § 11; the eight prior punch lists that name these
files; blindspots 7, 13, 30, 35, 44, 46, 49, 51, 54, 59, 63, 64, 65, 73;
D-WORKFLOW-056; #336, #613, #699; a read-only seam map of the twenty files
by a research subagent, its claims re-derived at the pin before use
(D-WORKFLOW-183); the host's artifacts named below, each inspected.

## 1. What do we know and what are we assuming?

**The plan.** One Opus 5.5 session, in two worktrees, reads the twenty
EmulationStation sources of the launch path at the pin `16dbac5211` under
the code-auditor lifecycle with the renovation face (plan § 4's seven
questions), at Extended depth (Astra and Argon through the Facilitator),
proves what it can on a GENERIC_X64 guest booted from the M7 lane's image
of 2026-10-23 (which carries the pin), pauses at stage D for the
coordinator's stream briefs, fixes on its ES branch with the unit tests and
a syntax-only compile as the compile-side floor, and hands back with three
hashes (`reviewed-at:`, `fixed-at:`, `fixed-at-es:`). The coordinator
accepts, merges the ES branch into `test/qa-integration`, bumps the pin,
and proves each fix on the first image that carries it.

**What the plan assumes, and what was checked** (the substrate-precondition
question; each row's evidence was run on 2026-10-23):

| Assumption | Evidence | State |
| --- | --- | --- |
| The slice is twenty files, 11,287 lines, 17 fork-own and 3 upstream-carried | `python3 -I` over the P1 branch's `inventory.json` (rows with `tree == "es"` matching the four globs): `20 rows ... total lines 11287 ... Counter({'fork-own': 17, 'upstream-carried': 3})`; `wc -l` over the same twenty at the pin: 11,284 (three files end without a newline) | verified |
| The ES worktree exists at the pin, clean, with the unit tests buildable | `git -C <W> log -1` → `16dbac521 GuiWifi: cancel scan worker on normal frontend exit`; `git status --short --ignored` → only `!! build-tests/`; `./build-tests/es-unit-tests` → `185 passed \| 0 failed`, `4795 assertions` after a cmake configure and build with the M7 root's toolchain cmake and the host's g++ | verified |
| The image's binary is the slice's bytes | `git -C /workspace/repos/rocknix show 069fc2704421:projects/ROCKNIX/packages/ui/emulationstation/package.mk \| grep PKG_VERSION=` → the pin; the image file exists at the path the brief names (2,122,289,964 bytes); **not yet checked:** a string from the slice found in the guest's `/usr/bin/emulationstation` (the lane's first proof on the guest) | verified in the recipe, open on the binary |
| The four host checks pass at the pin | `credential-quoting: 9 credential call site(s), 9 quoted, 0 bare`; `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`; `703 fork string(s) in the source, 703 with French, 0 without`; `163 string(s) ... judged, 0 wrong` | verified |
| A syntax-only compile of an edited file is possible without a build | `tools/es-syntax-check` as shipped: `FAIL` in 24 ms, no reason (every GENERIC_X64 root's toolchain wrapper names the retired `m7-pixelelated` path; #699); the brief's recipe through the real compiler at the live root: `FileData.cpp` rc 0 in 1.07 s, `ViewController.cpp` rc 0 in 0.84 s | verified, with a tool bug filed |
| The Argon reviewer route is in the lane's tree | the coordinator tip `6874394d49` carries M7's three commits; `grep -c gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts` → `7`, `4`; 29 pinned files hash to their pins; T1 ran the seat the same day (`google/gemini-4-argon`, 527 s, after `verify-pins` OK and routing 127/127 under its tsx) | verified |
| The host is shared and currently handed to M7 | `/tmp/m7-m6-host-coordination-20261023.txt`: the T1 lane's `M6 guest down 16:37:49 UTC`; no `resource return` yet; `pgrep -f 'qemu-system-x86_6[4]'` → none; `free -g` → swap 7 of 7 GiB used before the stop | verified; the return is a known unknown (§ 2) |
| Upstream's side of Q4 is small | `git -C <ES> log --oneline cada856d8..rocknix/master -- <20 files> \| wc -l` → `0`; `1750dded8..batocera/master` → `7` | verified |
| No branch in flight in the ES repository changes the twenty files | for every `feature/*` and `fix/*` branch ahead of the pin, `git log --oneline <pin>..<branch> -- <20 files>`: no `feature/m7-*` branch touches them; three older branches do (`feature/backup-restore-dialogs` 4 commits, `feature/cloud-epic` 1, `feature/restore-relink-wizard` 5), none of them the M7 lane's current work | verified |
| The shipped systems template uses the placeholders the brief's Q3 names | `grep -rn -o -E '%[A-Z_]+%' projects/ROCKNIX/packages/virtual/emulators/` → `%RUNCOMMAND%` (3), `%ROM%` (3) and nothing else: **`%BASENAME%`, `%ROM_RAW%`, `%GAMENAME%`, `%SYSTEMNAME%` and `%GAMEINFOXML%` are not in the shipped template**; the lane re-derives on the guest's generated `/etc/emulationstation/es_systems.cfg` | verified on the generator; the brief is adjusted (§ 5) |
| The lane can push its ES branch and its commits run the credential scan | `git -C <W> ls-remote origin HEAD` answers; `ls "$(git -C <W> config core.hooksPath)"` lists `commit-msg guard-lib pre-commit pre-push pre-push-test secret-patterns` (the `qa-integration` worktree's absolute path) | verified; the brief is adjusted to check both at stage A |
| The tools' flags the brief gives exist | `--help` of `es-launch-memory` (`--identity --cycles --output` required), `vm-visual-qa` (`--monitor`, `run`), `emulator-exit-test` (`--port --identity --vm`), `time-to-play` (`--monitor --out --no-configure-remote --vm`), `es-menu-map-check` (`--es-src --ref`), `es-untranslated` (`--es-src`), `vocabulary-check` (`--es`), `vm-stop` (`pidfile disk`), `generic-x64-vm run` (`--vnc --ssh-port --pidfile --serial --monitor`) | verified |
| The seam map's claims the brief rests on hold at the pin | `LaunchCommand.h` holds only `launchToken` (28) and `launchArgument` (51); `getlaunchCommand` at `FileData.cpp` 536 takes the template at 607 and substitutes at 618 to 630; the ROCKNIX netplay branch at 659 to 678 computes `pass` and `session`; `mRunningGame` at 83 beside `std::atomic sGamesStarted` at 90; `loadAdditionnalConfig` returns at `SystemData.cpp` 1042 and 1049; the wrapper at `Platform.cpp` 162 to 168; `SystemScreenSaver.cpp` 546 and `HttpServerThread.cpp` 625 as outside callers | verified by `git show \| nl` and `git grep` at the pin |

**Build-vs-adopt:** not applicable; a read slice of the fork's own code.

**Assumed and not checkable now:** that the maintainer wants ES fixes
proven on an image before an interface slice closes (§ 2, item 3); that
the Argon seat answers a second time as it did the first.

## 2. What known unknowns need investigation?

1. **When the host comes back.** M7's reclaim and bounded compile and VM
   work have no stated length. *Proceeding:* the brief makes the return
   line a wait, not a stop; stage A's reading, the counts and the four
   host checks need no runtime; Phases 1 to 4 can be written from the tree
   with the guest proofs held in a list and run when the line comes. The
   coordinator relays the line on #649 and #648.
2. **Whether `es-syntax-check` is fixed before stage E** (#699). *Decided
   here:* the lane fixes it at stage A on its distribution branch as the
   first `bug` it needs (lanes fix bugs; the fix is to the tool's command
   string, never to a build root's wrapper files, which are M7's frozen
   builds), and uses the brief's recipe until then.
3. **Which image proves an ES fix, and when.** M6 builds nothing
   (D-WORKFLOW-183); an ES fix has no binary until a pin bump reaches an
   image, and the M7 lane builds on its own cadence for its own candidate.
   The plan's stage F says every behaviour claim is proven on the VM, and
   its stage H closes at hand-back. For an interface slice the two cannot
   both be true on the day of hand-back. *Decided here, the coordinator's
   call (plan § 6b stage H is amended in the same change):* an interface
   slice is accepted at hand-back and its branches merged and the pin
   bumped, but it is closed only when the first image carrying the new pin
   proves each fix (`renovation-status` lists it as `remediating` until
   then, with `fixed-at-es:` set). Which build carries the renovation's pin
   bumps, M7's next or one the coordinator asks the maintainer for, is put
   to the maintainer on #346 and recorded as an open decision; nothing in
   T2 waits on the answer before its hand-back.
4. **Whether any player runs a custom `es_systems_custom.cfg` that uses
   the raw placeholders.** Not knowable from the tree. *Proceeding:* the
   raw substitutions are Q6 rows on the image (the shipped template uses
   `%RUNCOMMAND%` and `%ROM%` only) and Q3 leads under a custom template,
   which the VM can exercise with a template under `/storage`; a `bug` for
   one is filed with that fixture as its VM criterion, and its severity is
   graded against the custom-template precondition, not as a default path.
5. **Whether T1's punch list and T2's overlap at the command's seam.** T1
   found F-14 (a typed netplay host reaches `runemu.sh`'s root `eval`);
   the ES side `shellQuote`s the ip and nick under `#if ROCKNIX` and the
   shell unquotes them before `runemu.sh` evals. *Proceeding:* the brief
   tells the lane to read T1's audit issue before filing a `bug` on the
   command's quoting; the coordinator writes the two lanes' stream briefs
   for that seam together at the pauses.

## 3. What patterns from prior work apply that we haven't named?

- **T1's brief went out with seven wrong claims and nineteen unasked
  questions; the stranger's proof found them in an hour.** Every one was
  a fact a command could check. So this brief was written after the
  commands: every tool's `--help`, the four host checks run at the pin,
  the unit tests built, the syntax recipe proven, the remote and hooks
  probed, the seam map re-derived line by line. The proof runs again on
  version 1 anyway; what it finds is what the commands did not reach.
- **The same files broke the interface before, in the same shape the
  gates have.** #246 (2026-09-22): `rescanIfFolderChanged` deleted
  `FileData` the view's cursor still pointed at, found on the eighteenth
  screenshot because the heap chose; the rule became `es-code-traps.md` §
  A rescan that deletes FileData drops the view first. The launch gates
  hold raw `FileData*` across waits of up to 20 s while the same rescan
  can run from the UI thread (`SystemData.cpp` 456 to 473, posted from
  `FileData.cpp` 1223 and `GuiCloudTransfer.cpp` 335). The lane's Q3 reads
  the gates with that case open beside it, and a proof of it needs a
  rescan during a wait, which the guest can stage (a ROM removed while a
  STOP IT AND PLAY question is up).
- **#198's credential-quoting test reads the source rather than a list of
  sites.** The model for a new test of the command builder: a case per
  placeholder with a hostile file name, run under doctest beside
  `LaunchCommandTests.cpp`, so the next site is caught by the shape.
- **Blindspot 49 made the syntax check; the syntax check does not run
  here.** An edit made blind to the compiler cost a twenty-minute build on
  2026-09-21; the tool written for it fails silently on every root this
  host has today. The brief's recipe is the tool by hand; #699 is the tool
  fixed; the criterion that every `.cpp` commit names its compile line is
  the audit of it.
- **Two lanes, one host (the 2026-09-14 mixed-image failure, D-WORKFLOW-183).**
  Today it was the M7 lane's swap, not a build root, and the T1 lane's
  guest went down by its own hand within a minute of the ask. The brief
  gives T2 its own ports and sockets, a stop by pidfile, and the handoff
  file to read before any runtime.
- **D-UI-079: change stays inside the fork's lanes.** The launch path is a
  fork lane where it touches the sync, the saves, the capture and the
  cards (the gates, the exit sync, the save-state bookkeeping); the
  transition animation, the splash and the netplay downgrade are
  upstream's surfaces. A player-visible change to the latter is put to the
  maintainer through the coordinator; a defect there is fixed (D-WORKFLOW-187).
- **P1's retro, § Discoveries that affect future slices:** the ES survey
  runs in an ES worktree with the distribution's rules (plan § 11 item 4,
  now the brief's two-worktree shape), and the ledgers carry an `es` hash
  (`renovation-drift --pretend SLICE=HASH,es=HASH`; `renovation-status`
  reads `fixed-at-es:`), so the hand-back's third hash has somewhere to go.

## 4. What could we be missing?

**Agent-execution simulation, archetype one: a fresh Opus 5.5 session with
the brief, the two worktrees and nothing else.** Walked forward:

- *First commands.* It runs them; `git diff --stat next -- .claude ...`
  prints three files, as the brief says. It reads the ES pointers and goes
  to the distribution's rules. One hour of reading. No trip.
- *Stage A, the counts.* The python prints 20, 11,287, 17, 3, 10,804; the
  `ls-files` prints 20; the numstat prints 11,287. No trip. It fetches
  `rocknix` and records the refs.
- *Stage A, the guest.* It reads § 5, finds the handoff paragraph, checks
  the file, sees no `resource return`, and must decide: wait, or go on
  without a guest. **Trip:** a lane that reads "stage A's tool trials"
  as a prerequisite for stage B will sit idle for hours. *Fix:* the brief
  says in § 5 and § 8 that the wait is not a stop and that Phases 1 to 4
  proceed on the tree with the guest proofs listed and deferred; version 2
  says it again at the top of § 5 as the first bullet, and the running
  log's header carries the wait.
- *Stage A, the tool trials.* Once the guest is up it runs `time-to-play`
  with `--vm --no-configure-remote --monitor --out`, `emulator-exit-test
  --vm`, `es-launch-memory --identity --cycles --output`. **Trip:** the
  `--port` default is 10022 on all three and the guest is on 10033; a lane
  that forgets `--port` talks to nothing or to T1's guest if it is back
  up. *Fix:* the brief's commands carry `--port 10033` in every line; the
  running log records the port.
- *Stage B, the reading.* It reads `FileData.cpp` and reaches the gates.
  **Trip:** it may read the STOP IT AND PLAY question against `es-player-text.md`
  and open a Q2 finding about the words, which D-CLOUD-130 and D-UI-096
  settled with the maintainer's own shape. *Fix:* § 3 cites both; the
  rule is "cite, never re-argue".
- *Stage B, the seam.* It finds `head -300` in `Platform.cpp` and the
  character list in `FileSystemUtil.cpp`. **Trip:** fixing them in this
  slice. *Fix:* § 2 names both files as T35's and T36's and says a finding
  there is a lead posted on #649 with the slice named; the punch list has
  a column for it.
- *Stage C.* It runs `npm install` (after the return line), `verify-pins`,
  the probe, the two seats. **Trip:** the first call fails on a transient
  and the lane calls `--member gemini` because it is in the roster. *Fix:*
  § 1 says never; a seat failing verification is the 4.6 blocker.
- *Stage D.* It files the audit issue and `bug` issues. **Trip:** a `bug`
  for `%BASENAME%` with "a ROM named with a backtick runs code" as its
  criterion, which no shipped template reaches. *Fix:* § 2 of this futro
  (item 4) and the brief's Q6 row: the VM criterion names the custom
  template under `/storage` as its fixture and the grade says so. **Trip
  two:** a `bug` on the netplay host that T1 already filed from the script
  side. *Fix:* the brief's Phase 5 reads #648's audit issue first.
- *Stage E, a fix.* It edits `FileData.cpp` on the ES branch. **Trip:** it
  runs `tools/es-syntax-check` and gets `FAIL` with no reason, assumes its
  edit is wrong, and spends an hour. *Fix:* the brief says the tool cannot
  run as shipped and gives the recipe; #699's fix is the lane's own at
  stage A. **Trip two:** it bumps the pin in `package.mk` to prove the fix
  on a build. *Fix:* forbidden in § 5; the coordinator bumps at
  integration.
- *Stage H.* It writes the three hashes. **Trip:** `fixed-at-es:` written
  when nothing changed in the ES repository. *Fix:* the brief says the pin
  itself in that case.

**Archetype two: the coordinator, two weeks on, at acceptance.** It reads
the checkboxes against the artifacts. **Trip:** criterion thirteen (every
`.cpp` commit with its compile and test lines) is ticked from the running
log, which the lane wrote: a self-report. *Mitigation:* the coordinator
re-runs the recipe on the ES branch's tip for every `.cpp` the branch
touched (`git -C <W> diff --name-only <pin>..HEAD -- '*.cpp'`), one second
each, and the unit tests once; the acceptance paragraph in § 10 says so in
version 2. **Trip two:** the slice is closed at hand-back while no image
carries the fix, and the drift tool later says `closed` for bytes nobody
ran. *Mitigation:* § 2 item 3: `remediating` until the image proof; the
plan's stage H amended.

**Pre-mortem.** A month on: the pin was bumped, an image was built, a
player's launch over a sync shows the question and then launches twice.
The review says: the fix to the deferred-launch pointers was proven by a
unit test of a pure function and a reading, the walk for it was written
but never run because the integration image came six weeks later and the
coordinator had moved on to T5. The guard that would have caught it: the
`remediating` state above, and the coordinator's own next act list naming
"prove T2's fixes at image X" with the walk's path. Both are written into
the M6 body at acceptance.

**Blindspot check.** 49 (an edit made blind to the compiler): triggered by
design; the recipe and criterion thirteen are the guard, #699 the tool. 65
(a proof's substitute passed where the real input failed): the exit test
drives `execute_kill` with its own fixture; the brief says a pad's hotkey
is what the guest cannot have, so the tick names the substitute. 54 and 63
(the renderer): `--vm` on the two timing tools; the running log records
the renderer line. 44 (a fixture's size): frames at 640x480, the panel's.
59 (a memory measurement on a page that never loaded): `es-launch-memory`
refuses a changed PID or a lost launch, and the brief says omit the limits
for diagnosis. 30 (a resumed session built on its own summary): the lane
pointer at every checkpoint. 51 (an open checkbox is a claim): `box-check`
on every issue the lane files. 46 (a name read as a behaviour): the seam
map was re-derived; `launchToken` reads whole shell words, last wins, and `runemu.sh`'s
`${ARGUMENTS##*-P}` differs, rests on the header's own words and on
`LaunchCommandTests.cpp`; version 1 of the brief said the two agree, and
the stranger's proof caught it. 13 (assumed done): the four
host checks' baseline lines are quoted in the brief so a changed number is
seen. 35 (a remedy built on an audit's claim about a default nobody read):
the seam map is a lead; every line it cites is re-read by the lane. No new
blindspot surfaced; the tool defect (#699) is an instance of "a guard that
fails without saying why", already in `engineering-practices.md` § Guards
must fail closed.

**Replaced-mechanism archetype.** The slice replaces nothing by reading.
Two fixes it may propose would: consolidating the three readers of the
`-P`/`--core=`/`--emulator=` tokens (`launchToken` here, `runemu.sh`'s
`${ARGUMENTS##*-P}` in T1, the unit tests' `runemu` stand-in) would
replace a contract two repositories keep, and `LaunchCommandTests.cpp`
exists to say where they part company, so the stream brief names both
sides and keeps the test; and removing `renumberSlots` (no caller) would
retire a function whose intent (`.bak` restore and slot order) the manager
page may still assume, so its `Already written:` line reads
`GuiSaveState.cpp` for what it expected.

**Honesty check.** The first archetype returned trips only where the brief
already had an answer, which is the sign of simulating too gracefully; the
second archetype (the coordinator at acceptance) produced the two findings
that change the plan (the self-reported compile line; `closed` without an
image). A third pass, the M7 lane reading #649 a week on, found one more:
its ES worktrees and `test/qa-integration` are named in the brief as "never
write there", but nothing tells the M7 lane that an M6 branch exists beside
them in the same repository. *Fix:* the dispatch comment on #649 names the
ES branch, and the coordinator's block in the host coordination file
already names the worktree.

## 5. What adjustments or investigations must happen BEFORE execution?

Done in the same change as this futro, or named with its owner:

1. **Brief § 1, first commands:** add `ls "$(git -C "$W" config
   core.hooksPath)"` (must list `pre-push`) and the push of the ES branch
   at stage A (`git -C "$W" push -u origin feature/m6-es-launch-path-649`).
   *(version 2)*
2. **Brief § 2:** record that no `feature/m7-*` branch in the ES repository
   touches the twenty files (the three older branches named, not in
   flight), with the command; record the generator's two placeholders and
   what that makes of the raw substitutions (Q6 rows on the image; Q3
   leads under a custom template, which the VM exercises under
   `/storage`). *(version 2)*
3. **Brief § 1 and § 5:** the lane fixes #699 on its distribution branch
   at stage A as its first `bug` (the tool's command string only; a build
   root's wrapper files are never edited), and uses the recipe until the
   fix passes #699's criteria. *(version 2)*
4. **Brief § 5, first bullet, and § 8:** the host's return line is a wait;
   Phases 1 to 4 proceed on the tree with the guest proofs listed and run
   when the line comes; the running log's header carries the wait.
   *(version 2; already in § 5 and § 8, moved to the front)*
5. **Brief § 6, Phase 5:** read T1's audit issue before filing a `bug` on
   the command's quoting; one `bug` per defect across the two lanes; the
   coordinator dedupes at the pauses. *(version 2)*
6. **Brief § 10:** the coordinator re-runs the syntax recipe on every
   `.cpp` the ES branch touched and the unit tests once, at acceptance,
   rather than reading the running log alone. *(version 2)*
7. **Plan § 6b stage H:** an interface slice is accepted at hand-back and
   closed only when the first image carrying the new pin proves each fix;
   `remediating` in between, with `fixed-at-es:` set. *(the coordinator,
   this change)* **And an open decision for the maintainer, on #346:**
   which build carries the renovation's ES pin bumps, M7's next or one the
   coordinator asks for. *(the coordinator, this change: plan § 11 and the
   register's open table)*
8. **#649's criteria:** the eleven slice-specific criteria of brief § 7
   added to the issue body before dispatch, as #648's were. *(the
   coordinator, at dispatch)*
9. **#700's body:** no change; its fifth criterion already asks for the
   pin on `next` to carry every slice's fixes.
10. **No new blindspot entry.** The tool defect is #699 with its own
    criteria; the compiler-blind edit's guard in an ES slice is criterion
    thirteen until the tool is fixed.

Nothing else is needed before stage A. The stranger's proof of version 1
runs beside this futro; what it finds is answered in version 2 with these.

### T18 kickoff addendum (written with the brief's version 1, 2026-10-26)

The brief is `docs/reviews/briefs/es-cloud-pages.md`; the slice is #665
(`es-cloud-pages`, Extended, the brittleness and new-functionality lens;
30 paths of the EmulationStation fork at the pin `16dbac5211`, 11,193 lines,
every one the fork's own by origin). Written during T17's stage E, with the
host in M7's and M6's explicit queue; the dispatch waits for an idle lane
session and the window for its turn in the queue. **Streams predicted:
two** (the header comment at `ThreadedCloudSync.h:94-96` quoting the rule's
older why words; the why table's missing rows), stated as a number so the
retro reads it back.

- **Assumptions named.** The `GuiCloud*` glob reaches only the transfer
  page; the wizard, the scan launch and the connections pages are
  `GuiMenu.cpp`'s (T26) and the eight sources invoke no script by path --
  the slice reads a library whose callers are elsewhere. The shipped
  fallback map agrees with the scripts and it is the rule and the header
  comment that drifted (#909's half and this slice's). The ES repository's
  top-level `tests/app-unit/` and the Python harnesses are read as
  context, not membership (no re-cut). A fix reaches an image only through
  the pin, which the coordinator moves at integration.
- **Known unknowns.** (1) Whether any M6 GENERIC_X64 build root holds an
  `emulationstation-*` build directory for `tools/es-syntax-check` and a
  rapidjson copy for `es-unit-tests` (a § 5 run; `CANNOT` with the tool's
  words if none); (2) the one why sentence the digest's credential filter
  withheld and the eight variable-built `say_why "$var"` sentences (the
  lane re-derives); (3) whether the image the guest boots carries the pin's
  binary (the window's first step identifies it); (4) what `classifyProtocolLine`
  makes of a `>>>` line it does not know; (5) whether a conflict wizard
  exists in any ES source at the pin.
- **Patterns.** T2's two-worktree shape and its `proved:` values
  (`pin-binary`, `fix-unit-test`, `fix-walk-pending-image`); T16's and
  T17's generated tables with asserted counts; T17's packet trimmed before
  any seat; the stranger's proof (every version-1 brief needed it);
  #1061's lesson for test fixtures (`MaskSecretsTests.cpp` is the file to
  read first); the removal shape; the window's post contract and
  bound-plus-grace stop (`engineering-practices.md`, after #1135).
- **What could be missed.** A reader filing the header comment's older
  words as the code's defect (the code matches the scripts); a reader
  reading M7's `m7-*` ES worktrees for what the pin lacks (cited by number
  only); a reader taking a frame without reading its string back; a reader
  taking `es-unit-tests` PASS without the configure's rapidjson path named
  (the build fails closed, but a stale binary does not); a reader asking a
  unit for anything (nothing runs on a handheld); a reader bumping the pin
  (the coordinator's); a reader writing the walks' frames as proven before
  the integration build carries the moved pin.
- **Before execution.** The stranger's proof of version 1; #665 retitled
  `E700/T18` and re-parented under #700; the distribution worktree cut from
  `2174265e9c` with the coordinator's tip merged and the ES worktree cut
  from the pin, both by the coordinator; the body rewritten with the
  nineteen criteria and the VM line; the dispatch to the first idle
  session, with the window's place in the host file's queue stated.

### Errata from the stranger's proof of T18's brief (version 2, 2026-10-26)

Eight commands from the scratch clone and the `qa-integration` checkout at
the pin; the membership, every line count, the history, the test counts,
the markers and the tools held. What the proof corrected, and what the
addendum above had wrong:

- **Known unknown (1) is answered, and the answer stops version 1's floor:**
  the host has no `cmake` or `ninja`, and none of M6's five
  `build.pixelelated-GENERIC_X64.x86_64` directories holds a toolchain, a
  rapidjson copy or an EmulationStation build directory; the only roots
  that do are M7's, which M6 may not name. Version 2 builds the unit tests
  with the host's `g++` by a command generated from `CMakeLists.txt`,
  defers a GUI fix's compile proof to the integration build, keeps
  `ES_BUILD_ROOT` always set (its default is the legacy M7 root), and
  drops the stop; **#1137** files the gap under #903.
- **Known unknown (2) is closed:** 34 literal script sentences, not 37; 32
  shared, 2 the table lacks, 6 the scripts never print; no third withheld
  sentence; the variable emitters are 17 lines, not eight.
- The why table has 38 rows and 38 unique sentences, no duplicate; the
  header's declaration regex yields 47 lines; the `_( )` figures name
  their populations (220 occurrences; 50 unique / 58 for the card, 67 / 80
  for the page); `FileData.cpp:1310` is the exit sync's start, not the
  launch's question; the pin's last commit adds no `_( )` line, so the
  window's identity string is a literal of the 30 absent from the merge
  base; nine small line-number slips; `tests/app-unit/**` is 19 files.
- The stream prediction stands at two; a third candidate -- a toolchain
  that is not there -- is infrastructure, not a stream.

### Errata from T18's acceptance (2026-10-26)

- **"Streams predicted: two" was six.** The two predicted (the why table's
  missing sentence, the header comments) landed as S1; four more the seats
  and the lane found: the stamp's unchecked write (S2), the words (S3), the
  card's wrapper (S4), a stop or cancel against an ending run (S5), the
  job's why handling (S6). The addendum's simulation stopped at the text
  and the comments; it did not walk the lifetimes, where three of the four
  came from.
- The window ran at 1280x800 until relaunched: the harness had no
  resolution option (#1141), which no futro here asked.
- Three of the eight files cannot be compiled on the host (SDL headers), so
  the compile proof of three streams is the integration build's; the
  futro's known unknown (1) resolved that way, as version 2 of the brief
  said.
- Eight bugs, all Low; the audit #1153; `renovation-drift` reads `re-open`
  until the pin moves, which is the integration's step, not the slice's.

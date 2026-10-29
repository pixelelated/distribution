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

### T20 kickoff addendum (written with the brief's version 1, 2026-10-26)

**The plan, in the order's words:** T20 is *EmulationStation's
RetroAchievements and offline pages*, lens security and new functionality,
Extended: *the account pages and the offline scan, which drive the proxy;
with the fork-touched files of ES's vendored libcheevos, read as a diff
against their imported version*. 25 paths, 7,485 lines; 17 of them exist
in ROCKNIX's master and are rewritten by the fork, eight are new. The brief
is `docs/reviews/briefs/es-achievements-pages.md`.

**Assumptions the plan leans on and does not state:**

- *That the credential's exposure is on these pages.* The sharpest sink
  is one file over: `HttpReq.cpp:192` never verifies the TLS peer, so the
  password and the web API key the pages send travel unverified -- found
  by the research, filed as #1154 before the lane exists, owned at the
  stage-D pause (T20's stream or T21's).
- *That the ctl's contract is read as one.* `ask()` keeps the last line
  and `WEXITSTATUS` without `WIFEXITED`; the scan job's reader checks it.
  Two readers of one protocol, disagreeing on a killed child.
- *That "the vendored library's fork edits" can be diffed against their
  import.* rcheevos 12.2.1's tarball is not in the cache; the proxy's
  12.5.0 is, and the fork's `hash_disc.c` fixes are absent from it.
- *That three hashers hash alike.* Nothing at the pin proves the three RVZ
  readers agree on a padded region at a non-aligned offset; no synthetic
  RVZ exists.
- *That the pages have a frame baseline.* The one RetroAchievements walk is
  in no suite list; `frame-diff` has never compared these pages.
- *That the menu map describes the scan page.* Its `:595` describes the
  design D-UI-078 reversed, and the page's title is absent.
- *That the host builds the tests.* It does not (#1137); the generated
  `g++` command does, and the pages and the hasher include SDL.

**Known unknowns:** whether any launch script reads the two switches the
page keeps on `es_settings.cfg`; who reads `Settings.cpp:420`'s
`.hardcore`; `readAllText`'s two-byte trap at the pin; whether the image's
RetroArch carries `cheevos_rvz.c`; T19's inheritance table (lands during
this slice).

**Patterns:** T18's shape (the same lane, the same host floor, the same
two-worktree dispatch; its six streams where two were predicted -- the
lifetimes were where the surprise came from, and this slice has a reader,
a hasher and a detached thread of its own); blindspot 46 (names read as
behaviour in this subsystem: the brief names the digests' leads as leads);
blindspot 64 (confirmed in the hasher's code by the research).

**What we could be missing (the simulation):** a lane that files the
unverified peer again (the brief cites #1154); a lane that treats the
ctl's `>>> ` tokens as `say()`'s (they are `tell()`'s); a lane that
spends the QA account's achievements on the sign-in (one live sign-in,
last, spends nothing); a lane that builds a synthetic RVZ by fetching a
tool (a `CANNOT` and the coordinator's harness Backlog instead); a lane
that fixes `ask()` in `ApiSystem.cpp` (T21's file) without a ruling.
Pre-mortem: a month on, a player's password read on a hotel's Wi-Fi
(#1154's fix did not land before the candidate); a top-up killed by the
OOM reader read as COMPLETED on the card.

**Adjustments before execution:** carried into the brief: #1154 cited not
re-found; the four families; the window at 640x480 with the self-signed
endpoint positive; the generated test build; the menu map's correction
with any row touched. **Streams predicted: three** -- `ask()`'s
`WIFEXITED` and the unmapped exits (where the coordinator rules the file),
the `summary` line cap, and the menu map's drift with the page's entries;
#1154's stream is a fourth if ruled this lane's.

### Errata from the stranger's proof of T20's brief (version 2, 2026-10-26)

Nine commands from the scratch clone and the ES pin by hash; every line
number and nearly every figure held. What the proof corrected, and what
the addendum above had assumed:

- **The count that would have stopped the lane:** § 2's expected
  merge-base count said 17 where the brief's own list of new files gives
  15. A figure that is also a stop condition is reproduced before it is
  written, not derived in prose; version 2 says 15 and the block prints
  it.
- **Five run comments disagreed with their commands** (the
  query-parameter grep, `User-Agent` against `userAgent`, the `LOG(`
  count, the hasher's call sites, `grep -c` against `grep -o`), and the
  syntax check's `rc=$?` read `tail`'s exit -- the trap
  `engineering-practices.md` names, committed into a brief that names the
  rule. A run's expectation is written from the command's output on the
  clone, as the stranger's proof then checks.
- `maskSecrets` is used by ten files, this slice's reader among them; the
  account client does not use it, which is the finding.
- `RetroAchievements.cpp` falls on `curl/curl.h` on the host, not SDL;
  the hasher has six call sites, not four; `stopRun` ends at `:353`.
- A fact for Q4 from the proof: no script reads the two `es_settings.cfg`
  switches, so their store is right.
- The stream prediction stands at three (with #1154's as a fourth if ruled
  this lane's).

### T21 kickoff addendum (written with the brief's version 1, 2026-10-26)

**The plan, in the order's words:** T21 is *EmulationStation's state
primitives and its bridge to the OS*, lens security and state preservation,
Extended: *`Settings`, `SystemConf` and `AtomicFileUtil` write
`es_settings.cfg`, `system.cfg` and the last-good copies; `HttpReq` is the
network client; `ApiSystem` assembles the shell commands every page runs,
from player-entered strings (Wi-Fi, accounts); `GuiWifi` and
`ScreenScraper` carry credentials*. 14 paths, 9,249 lines; 12 exist in
ROCKNIX's master and are rewritten by the fork, `AtomicFileUtil.*` is new.
The brief is `docs/reviews/briefs/es-state-and-bridge.md`.

**Assumptions the plan leans on and does not state:**

- *That the shell quoting is one rule.* It is two: `shellQuote` where the
  fork wrote the call (13 sites, all `wifictl`) and double quotes where
  upstream did (16 functions, two live on this image: `7z` over a ROM's
  path, poppler over a manual's). A file name is a player's string.
- *That a failed script fails.* `executeEnumerationScript` discards the
  exit (`:2251`), so a failed `rocknix-systems` reads as "no BIOS problem"
  at every launch; eleven `WEXITSTATUS` reads without `WIFEXITED` read a
  killed child as exit 0.
- *That the two stores share one contract.* They share the primitive:
  `SystemConf` is locked and records after a re-read; `Settings` is
  unlocked, its maps unguarded under a worker's save, 0644 with
  credentials inside, and has no unit test.
- *That D-CLOUD-078 holds on the OS side.* The shell writers rename with
  no `fsync`, `chksysconfig` with no lock, `post-update` in place, and
  `set_setting` seeds a missing `system.cfg` from `/usr/config` before the
  lock and without the record.
- *That the mode is the writer's.* A replaced file keeps its bits (T1's
  PL-023): a 0644 `system.cfg` on an upgraded device stays so whatever the
  new writer does. The question is `upgrade-and-install.md`'s.
- *That the credential's sink is the file.* The Wi-Fi key is argv of four
  processes for up to 150 s; the scraper's account sits in a 0644 file;
  the server's error body is logged verbatim; the peer is never verified
  (#1154).
- *That the mask reaches the output.* `maskSecrets` guards the command
  line at four sites and never a script's stdout, which
  `executeScriptLegacy` echoes to the journal.
- *That the host builds the tests.* It does not (#1137); the generated
  `g++` command does, and `ApiSystem.cpp`, `GuiWifi.cpp` and
  `ScreenScraper.cpp` include SDL or curl.
- *That `Settings.cpp:420` is a live default.* It is a `#if WIN32` mirror
  (`:417-433`), where `SystemConf` forwards to `Settings`; T20's brief
  carries it as a lead and its lane is told at dispatch.

**Known unknowns:** the NetworkManager keyfile's mode after a join (the
guest); whether a media URL carries the account, where `ssid=<username>`
is unmasked at LogDebug; which service runs EmulationStation on the
pixelelated image (`emustation.service` or `essway`), hence where the echoed
stdout lands; whether the image carries a CA bundle `HttpReq` could verify
against (the #1154 fix's design question, for the stage-D pause); where
`Paths.cpp` puts `system.cfg`; the boot ordering of `001-setup` and
`save-sysconfig.service` against EmulationStation's first save (T22's,
read here); whether any page shows the "Error starting command" string;
the p7zip recipe's install step and the `7zr` it never names.

**Patterns:** T18's shape (the same lane kind, the same host floor, the
generated `g++` build, the stage-D pause, `02`'s generated sections);
T1's audit on the other end of `system.cfg` (PL-004, PL-014, PL-023: the
inherited half, cited not re-found; a fix in those files is T1's and lands
only on the coordinator's ruling); T2's own T21 lead at its `:611`; #102's
arc -- the truncated stores gave D-CLOUD-078, the EmulationStation side got
the record and the lock (#320), the shell side got modes (#421) and not the
record; blindspot 43 (a log with a password; `redact_credentials` is the
guard, and none of these files writes that log); the replaced-mechanism
archetype -- `AtomicFile` replaced the in-place write for two stores, and
five state writers still write in place.

**What we could be missing (the simulation):** a lane that files the
discarded exit as a bug and fixes it by failing the launch when
`rocknix-systems` fails -- the fix lands on the launch path; the ruling is
read the exit and say so, never block the launch. A lane that gives
`Settings` the `PidLock` and makes every page close take two locks --
measured on the guest before it is written. A lane that fixes the shell
writers -- T1's files, the pause. A lane that proves the key on argv by
printing `/proc/<pid>/cmdline` -- the value in the transcript; the brief
says a masked count. A lane that pastes the generated `g++` line into `02`
-- never. A lane that runs `git status` in the `qa-integration` checkout --
another lane's tree; `W` is its own. A lane that reads #1154 as its to fix
at stage A -- fixes land only under a stream brief, and the design question
goes to the pause. A lane that spends the window's first minutes on the
live scraper sign-in -- last, if the bound allows. A lane that constructs
the `7z` positive on a device -- never; the guest, a scratch library.

**Adjustments before execution:** carried into the brief: #1154 cited not
re-found; the four `maskSecrets` sites and both echo lines reproduced at
the pin; the WIN32 mirror; the per-file deltas by `numstat`; the
merge-base count reproduced (12); T1's files named as T1's with the ruling
route; `rc=$?` on its own line; `g++`'s first error line, not its last;
the `7z` positive on the guest; the key on argv as a masked count. Owed
before dispatch: the stranger's proof of version 1, version 2 with its
corrections, this futro's errata section, the kit. Owed at T20's dispatch:
the note that `Settings.cpp:420` is WIN32-only.

### Errata from the stranger's proof of T21's brief (version 2, 2026-10-26)

The T21 addendum above was written with version 1; the proof corrected
these of its sentences, and version 2 carries the corrections:

- *"a failed `rocknix-systems` reads as 'no BIOS problem' at every launch"*
  -- at launch when CHECK BIOS AT LAUNCH is on (`CheckBiosesAtLaunch`,
  default false, `Settings.cpp:207`); the time-to-play line is conditional.
- *"It is a `#if WIN32` mirror (`:417-433`), where `SystemConf` forwards
  to `Settings`"* -- the default is under `#if WIN32`, but the forward is
  the empty-path case (`SystemConf.cpp:288` and its siblings, the path from
  `Paths::getSystemConfFilePath()`), not `#if WIN32` and not `:19-25`;
  whether the path can be empty on ROCKNIX is the lane's Q4 to read in
  `Paths` before the "not a second live store" conclusion is drawn.
- *"The Wi-Fi key is ... typed in a popup with no password flag"* -- the
  key's popup is `GuiWifi.cpp:365`/`:367` (version 1 cited `update()`'s
  `:460`/`:462`), and neither popup class has a password parameter at all:
  masking is a mode to add.
- *"`timeout N` on every `wifictl` call"* -- four calls have no bound
  (`:642` `enable <ssid> <key>`, `:767`, `:771`, `:775`).
- *"the `7zr` the recipe owes"* -- the p7zip recipe builds `all3` and
  installs `bin/7z*`; whether `7zr` is on the image is a listing in the
  window, not a finding.
- *"62 `batocera-*` sites"* -- 105 lines naming a `batocera-` script, 36
  distinct names; and the prediction that the writers generator counts
  five in-place writers meets 27 `writeAllText` sites, sixteen of them
  sysfs writes in `ApiSystem.cpp`, which the brief now carries as `sysfs`
  rows so the generated count does not read as drift.

### T26 kickoff addendum (written with the brief's version 1, 2026-10-26)

**The plan, in the order's words:** T26 is *EmulationStation's main menu
(GuiMenu)*, lens new functionality and brittleness, Independent: *one
file, 11,883 lines, the largest fork-own unit, where every fork page is
reached from*. Two files, both in ROCKNIX's base and rewritten by the fork
(5,124 insertions over 225 commits; 156 function definitions at the pin
against 60). The brief is `docs/reviews/briefs/es-guimenu.md`; the closing
evidence the order names is `tools/es-menu-map-check`.

**Assumptions the plan leans on and does not state:**

- *That the wizard's lifetimes are the risk.* They were (blindspot 4, the
  2026-09-05 crash); at the pin every one of the sixteen transitions hands
  the new page on, and nine Python harnesses compile the callbacks on the
  host. The risk has moved to the reads and the threads: a cached `exists`
  on the sign-in's QR path, a cache-backed `isRegularFile` under a comment
  that says "uncached", and synchronous script starts on the interface
  thread with no bound, several per page build.
- *That a page saves what its rows change.* A page with only
  `addInputTextConfigRow` rows never writes a file by itself
  (`GuiSettings::save` returns with no save functions); six such pages
  persist only through fork-added `onFinalize` saves.
- *That a credential row guards its value.* Five do not: an untouched
  editor under `system.security.enabled=1` returns empty and the empty
  value deletes the line; only DEVICE PASSWORD guards.
- *That a key a row writes is read by something.* Thirty-three are read
  by nothing under `projects/ROCKNIX/packages`; `global.videofilters`
  against the scripts' `videofilter`, `led.colour` against `led.color`.
- *That a settings page changes nothing until the player does.* Three
  pages write a store at open.
- *That the map and the code agree.* The check passes (0 missing) while
  D-UI-046's name and the map's `:405` heading differ, and 86 of the
  map's row labels match no `_("")` literal -- prose or drift, to be read.
- *That the taller pages are #540's.* The wizard's 0.75-height pages are
  unpositioned and fit by arithmetic (0.15 + 0.75 = 0.90).
- *That the host builds nothing of this file.* `g++ -fsyntax-only` cannot
  (SDL), but the nine harnesses extract and compile its functions: the
  host floor is real and every pure lead has a proof of choice.
- *That the main menu's build is off the launch path.* START builds the
  menu; a page close saves both stores before a launch; the synchronous
  starts run when a page opens -- the retro's time-to-play line is
  conditional on which page, named.

**Known unknowns:** which of the 33 unread keys' rows are ever built on a
ROCKNIX image (gated by `isScriptingSupported`, `#if BATOCERA`, a config
file); what `setrootpass` does with an empty argument (T1's file);
whether the `GetShOutput` byte drop ever reaches a `cloud_remote` error
sentence in practice; whether `qrencode` is on the image; which of the
map's 86 unmatched labels are prose; whether the two identical-looking Wi-Fi verdict composers (`:10084-10090`,
`:8320-8332`) are meant to differ; how the fork's saved-networks design
(D-UI-118) and upstream's `cada856d8` refactor of the same rows are to be
reconciled at the next merge -- the integration's question, recorded by
the lane in § The merge debt.

**Patterns:** T18's shape (the same lane kind, the stage-D pause, `02`'s
generated sections, the nine harnesses it assigned here); T21's rows
rule (`addSwitch`'s bool; the stores' writers) now read from the rows'
side; blindspot 23 (two consolidations in this file dropped properties
only the removed copy had) -- the duplicates table records before any
stream removes; blindspot 57 (a fix that covered fewer sites than its
issue named: the three `setrootpass` callers, all quoted now); the
replaced-mechanism archetype -- the wizard's folder step (D-CLOUD-170/171)
against the retired migration (D-CLOUD-175/178/179): what the pin still
builds there is Q2's.

**What we could be missing (the simulation):** a lane that fixes the
credential rows in `GuiSettings.cpp` -- another interface slice's file;
the guard goes in this file's row callbacks or the ruling at the pause
says which. A lane that reads `global.videofilters` as a typo and renames
the key -- a device's `system.cfg` holds the old key: `Already written:`
read both. A lane that treats the 33 unread keys as dead and removes rows
-- D-WORKFLOW-209's shape: the table removes nothing. A lane that proves
the QR-path lead on a device -- never; the guest with `/tmp` remounted. A
lane that trims the packet by deleting upstream regions without saying so
in the manifest -- the manifest names every trimmed region. A lane that
rewrites `cloudSetupPresent` to position the 0.75 pages and moves the
buttons off the 640x480 panel -- the frames at both sizes before and
after, per locale. A lane that runs `git status` in `qa-integration` --
another lane's tree. A lane that measures the main menu's build and
reports "nothing" -- the number, with the page named.

**Adjustments before execution:** carried into the brief: the nine
harnesses as the host floor with their expected lines from the
coordinator's own run; the credential rows and the six unsaved pages as
Q2's leads with the file-ownership question named for the pause; the
cached reads as Q4 with the constructed positive; the synchronous starts
as Q3 with the time-to-play line; the unread keys as a table with a frame
or `gated: never built` each; D-UI-046's drift as a checkbox; the menu
map's update rule in the same commit as any row change. Owed before
dispatch: the stranger's proof of version 1, version 2 with its
corrections, this futro's errata section, the kit.

### Errata from the stranger's proof of T26's brief (version 2, 2026-10-26)

The T26 addendum above was written with version 1; the proof held every
count that is a stop condition for the lane (the membership block, the two
files' lines and deltas, the definitions, the ten harnesses' lines) and
corrected these of the addendum's and the brief's sentences, now in
version 2:

- *"nine Python harnesses compile the callbacks on the host"* -- ten:
  `tests/gpu-governor-save.py` also reads `GuiMenu.cpp` (the GPU governor
  row's save callback; `PASS fallback` on the pin extract).
- *"one gate behind three predicates"* -- the NO CLOUD STORAGE sentence has
  seven sites: the three gates, two `GuiMsgBox`es, the gate check's dialog
  and the hub's row line.
- *"264 settings rows from 568 builder calls"* -- 564 by the nine builder
  greps; the digest's generator counted four more, and the lane's
  generator says which.
- The runs block's own commands could not print what their comments
  promised (a width cut after the path prefix; regexes that missed the
  helper names and the `#if defined(...) && !defined(...)` guard) -- the
  fourth brief in a row whose runs block was proven only by running it,
  which the proof is for.
- The dispatch tip in a run expectation is the lane's own merge tip, never
  the P1 branch's `2174265e9c`, whose `tools/` differ from the coordinator's.
- D-WORKFLOW-210 (the suite ruling of the same afternoon) is the highest
  workflow row, not 209; and the digest-method counts (1,689 occurrences,
  166 shared literals, ~930 dead lines, 148 row builders, and the rest)
  now carry their method beside the proof's figures, so the lane's own
  are not read as drift.

### Errata from T20's acceptance (2026-10-26)

What the lane found between stage A and the hand-back that the T20 addendum and the brief did not foresee (the brief carries the full list under § Errata at acceptance):

- From T19's stage A (lane, 12:25): `scanWhy`'s `NO_GAMES_FOUND` row -- the ctl prints `>>> why NO GAMES FOUND` on an empty library and the page's why table has a row for it; the brief's why table omits it (T20's, told at dispatch).
- From T19's streams (the lane, 16:08): why tokens the ctl now emits, read at the ES pin: `RESULT_UNREADABLE` has no row in the interface's table; `TOOK_TOO_LONG` has a row in `scanWhy` (`CloudText.cpp:1036`) and none in `topUpWhy`; `SOME_IMAGES_NOT_SAVED` has rows in both; S5's `STAMP_UNWRITABLE` has none -- T20's rows and French (T19's `02` § What T20 inherits carries the list).
- Stage B (lane, 17:33): `topUpWhy` falls through to `scanWhy`, so `TOOK_TOO_LONG` has a row (T19's table said missing); `Paths.cpp:94` sets the ROCKNIX path, so `Settings.cpp:420`'s WIN32 default is no live second store (T21's Q4 owns `Paths`).
- The window (17:36 to 17:57): the installed EmulationStation carries the pin's literal but is M7's composition on top of the pin, so an identity check needs two literals (Backlog #1169); `tools/ra-ui-test` was `CANNOT` on its own preconditions after other steps left state (run it first on a clean guest); L-06 does not bite on the image (`/bin/sh` is bash and forks for `sh -c "cmd 2>/dev/null"`).
- Stage E (lane, 19:47 and the hand-back): S4 reads the toggle back through the ctl's `status` rather than the file directly (the ctl reads the file; the ruling's intent); the streams touched files outside the 25 under their rulings -- `HttpReq.{h,cpp}` (S2's one field `httpsRedirectsOnly`), `CloudText.{h,cpp}`, `ProxyCards.cpp`, `FileSystemUtil.cpp` (S8), and two new pure helpers `OfflineAchievementsText.{h,cpp}` and `RetroAchievementsText.h` with their tests -- the brief's § 1 said "nothing in the ES worktree outside the 25 before a stream brief", and the stream brief named these; `es-code-traps.md`'s non-ASCII grep over a whole touched file flags upstream's own em dashes (`FileSystemUtil.cpp`), so the check judges the added lines (the retro's recommendation 1).

### Errata from T21's acceptance (2026-10-27)

What the lane and the coordinator found between stage A and the hand-back that the T21 addendum and the brief did not foresee (the brief carries the full list under § Errata at acceptance):

- Stage A (lane, 21:02): `writeAllText(`'s 27 lines are 25 call sites plus the function's definition and declaration (sixteen of the sites `ApiSystem.cpp`'s sysfs writes); § 7's criterion restated in the body to 25 call sites, the generator naming the two lines it leaves out; the brief's § 5 comment and § 7 take this at acceptance. `wifictl`'s key is on four lines (177, 195, 209, 460): the § 5 pattern `nmcli|password|set_settings` prints 177 and 460 only; 195 and 209 are `802-11-wireless-security.psk "${PSK}"` -- the brief's run comment under-counted the key's path by the two psk lines.
- S1/S2 (lane, 00:50): the brief's S2 "a live file whose text is a strict prefix of its record's is a recovery whatever its mtime" is not buildable as written -- a whole file that is a line-prefix of its record cannot be told from a script removing the last key; the lane's reading (S1's save-side guard plus the re-choose on every save) covers PL-09's loss path and was accepted. `hostname-empty.py`'s step 3 had been run by hand at stage C and appended to its `.out`; the script now reproduces its own output.
- S8 (lane, 01:19): the ruling of 01:11 that `Settings` takes the unrecorded-save marker in S8 was wrong -- `Settings` rewrites every non-default value from memory, so a key the record holds and the file lacks is a reset, not a loss; ruled (b), no marker; `kUnrecordedSuffix` is `SystemConf`'s.
- Stage E (lane, 00:50 to 02:25): the case totals the lane posted for S2 to S13 were composed, not counted, each too high by 2 to 53; corrected in `02` and `00`, and the build script now prints `TOTAL: N test cases in B binaries` (the rule's sentence in `engineering-practices.md`). S12 edited `Scraper.cpp` (`:372`, `:631`) beyond the brief's file list so the two new status classes are skipped as `REQ_IO_ERROR` was: a contained edit in T32's file, accepted. `Retry-After` is read at two sites (`:356` and `:628`), the brief named one. `getMD5`'s pipeline exit is `md5sum`'s, so S3's reader, not the exit, is the check there. S14's self-signed listener is CANNOT on this host (libcurl's runtime without its headers): the integration window's walk. The brief's S1 "every text row gets the guard" and S2 "strict prefix" sentences, and the coordinator's "Settings takes the marker", are the errata above.

### T31 kickoff addendum (written with the brief's version 1, 2026-10-27)

**The plan, in the order's words:** T31 is *EmulationStation's other
pages*, kind currency, lens new functionality, Independent: *the remaining
pages under `guis/`: the fork-touched ones read line by line, the upstream
ones checked against `rocknix/master`*. Seventy-six paths, 15,537 lines by
the inventory's count, 4,230 of them in the twelve files the fork touched
-- three it added (`GuiScraperRun.{cpp,h}`, `WifiScanProcess.h`, 527 lines)
and nine it modified (1,207 lines added, 129 removed, against the merge
base; 25 of the fork's commits on `GuiSaveState.cpp` alone); the other 64
are byte-identical to the base and to ROCKNIX's master today. The brief is
`docs/reviews/briefs/es-pages.md`; the closing evidence the order names is
the audit folder, the lint and the punch list through Phase 7.

**Assumptions the plan leans on and does not state:**

- *That "4,230 fork-own" is what the fork wrote.* It is the lines of the
  files the fork touched: the inventory's tier is `fork-own` for any path
  the fork added or changed, and nine of the twelve are upstream pages
  carrying edits of 2 to 330 lines. The brief's § 2 carries both tiers so
  the lane neither reads 3,702 upstream lines as ours nor skips the 330
  that are.
- *That the merge base is `bccd715707`.* It is `cada856d86`, one commit
  later; the earlier ES briefs read a stale `upstream/master`. Nothing in
  this slice differs between the two, but a lane that names the old base
  names the wrong one and the next slice copies it (blindspot 75's shape).
- *That upstream has moved under these pages.* Its 14 commits since the
  base land in `GuiMenu.*`; no slice file differs between the base and
  `rocknix/master`. "Checked against `rocknix/master`" is a no-op at this
  hash and the brief says so, so the lane does not invent a delta.
- *That a harness exists for pages.* None of the 15 Python harnesses reads
  a file here; the one doctest naming `GuiSaveState` needs a toolchain the
  host lacks (#1137). The host floor is what the lane writes in the four
  patterns' shape, FAIL first.
- *That the map and the checker cover these pages.* Twelve titles are in
  neither the map nor `## Not mapped` -- the fork-own SCRAPING GAMES and
  the fork-modified BIOS CHECK among them -- and the checker's three
  regexes cannot see a page built on `GuiComponent` with its own
  `mMenu(window, _(..))`, so `0 missing` is true of what it can read
  (#951/#965 from the pages' side).
- *That the fork's confirmations are the risk.* Both fork YES/NO boxes are
  YES first, NO last; the ones to read whole are upstream's: WRITE and
  CLOSE as first buttons (`GuiGameOptions.cpp:274`, `:289`), FAILED as a
  message (`GuiNetPlay.cpp:336`), SAVE CHANGES? on two editors.
- *That the manager's long work moved to a worker.* DELETE did (#205);
  COPY at `:516` still runs `copyToSlot` on the interface thread, and since
  T2's `f11e7528a` that call can return `false` to a page that says nothing
  (PL-016, #782). And the scrape page ends in a fourth SKIPPED
  (`GuiScraperRun.cpp:141`) the register does not list.

**Known unknowns:** the second button of the NFC WRITE box and what back
does on it; whether the eight bar-less `.cpp` files inherit a true bar or
show none; whether any slice page calls `getMenu().setSize(` (#540; the
floor did not grep it); whether the `GuiMoonlight` boxes are reachable on a
ROCKNIX image; what a short `rocknix-systems` line does to `atoi(tokens[6])`;
`tools/es-untranslated`'s line against `cada856d86`; whether `Settings::saveFile`
is atomic under `GuiScraperStart`'s two rewrites per visit (T21's `:547`);
which es-core owner rules on a popup or `GuiMsgBox` change (the inherit
digest reads T35; the coordinator confirms); whether T26's `02` § What T31
to T37 inherit lands before stage A.

**Patterns:** T18's shape (the stage-D pause, `02`'s generated sections,
the one-seat packet); T20's two routed callers (the hasher from
`GuiHashStart.cpp:85` and `GuiNetPlaySettings.cpp:59`, #1170/#301: cited,
not re-found); T21's rows rule and writers' contract (`addSwitch`'s bool;
`AtomicFile::writeText`; a string from outside goes through one quoting
function or an argv executor -- `WifiScanProcess.h` is that executor and
is in this slice by the glob) and its retro's rule that a harness FAILs
against the unfixed code first; T26's method of reading every dialog's
first button whole (the floor's window mis-read six of fifty); blindspot 45
(the manager's DELETE proven at a fixture's speed -- COPY is the sibling);
blindspot 62 (the `Already written:` line on every manager bug); blindspot
4 (`close()` inside a page's own handler -- the scrape page's `delete this`
read and found safe); D-UI-079 against rule 6 (64 of 76 paths are
upstream's: a behaviour stays, a contained defect closes, the punch list
says which for every item).

**What we could be missing (the simulation):** an Opus lane at Independent
depth opens 76 files and reads `GuiNetPlay.cpp`'s 1,109 upstream lines at
the depth of the manager's 612 -- § 2 orders the read by provenance. A
lane that grades the 50 dialogs by the floor's heuristic and reports 17 /
10 / 6 without reading the six -- the brief names them. A lane that
rewords the fourth SKIPPED on the ES branch -- a register question for the
pause. A lane that moves `copyToSlot` to the worker because DELETE did --
blindspot 45 asks for the measurement first and the stream brief rules. A
lane that declares all twelve undescribed titles under `## Not mapped` --
BIOS CHECK and SCRAPING GAMES are the fork's rows and D-UI-039 maps them.
A lane that patches `tools/es-menu-map-check` under `tools/` -- a Backlog
the coordinator files from the lane's title-shape table. A lane that
changes `GuiSettings.cpp`'s `updateVal` for #1185 -- T21's bug, the pause
rules whose file. A lane that fetches `rocknix/master` "to be sure" -- a
write; the ref is shared. A lane that finds T21's `a73ed9efc` missing from
`GuiBios.cpp` at the pin -- the read is the pin's bytes, the stream's a fix
on top. A lane that proves the stale read by restarting ES between frames
-- one session: options menu, scrape, options menu again. A lane that
reports "nothing" for time to play -- the number, with the page named. A
lane that spends its window on the Bluetooth pages and never frames the
manager's help bar at 640x480.

**Adjustments before execution:** carried into the brief: the two counting
rules and the two tiers in § 2 with the membership block's recorded
output; the corrected merge base with the stale ref explained; the empty
harness floor as the lane's to build, a case per pure lead, FAIL first;
the dialog table read whole with the six mis-read sites named; the twelve
undescribed titles with the fork's two first and the checker's blind spot
as a Backlog; the fourth SKIPPED as the one register row expected; COPY's
synchronous call and the two rewrites per SCRAPER visit as Q3 with the
time-to-play line; the 12 cached reads as Q4 with the one-session positive;
`WifiScanProcess.h` claimed by the glob and read as the quoting model; the
sized-pages grep added to § 5 with no expectation. Owed before dispatch:
the stranger's proof of version 1 (the hand counts 12 / 27 / 11 of title
shapes and the `73` merge-base loop first), version 2 with its corrections,
this futro's errata section, the kit, the retitle to `E700/T31`.

### Errata from T26's acceptance (2026-10-27)

What the lane and the coordinator found between stage A and the hand-back that the T26 addendum and the brief did not foresee (the brief carries the full list under § Errata at acceptance):

- Stage B (lane, 08:05): MANUAL UPDATES is the fork's (`975235429`), not upstream's; the RGB LED page with `led.colour` and the first SECURITY page with `:3209` are under `BATOCERA` and never built on ROCKNIX (closing T21's `:2989` and `:3209` notes); the six unguarded credential rows are already fixed by T21's S1 in `buildInputTextConfigRow` (#1185), so `GuiMenu.cpp` needs no change there; of the brief's 33 "unread keys", 11 built rows hold once `get_setting`'s `global.` fallback is read, two of them upstream's one-word defects (L-09 `global.videofilters` against `videofilter`; L-10 `ScrollLoadMedias` written to `system.cfg`, read from `es_settings.cfg`).
- Stage E (lane, 09:43): S2 wrote the relink sentence as GAME SETTINGS > MANAGE CLOUD STORAGE > CLOUD CONNECTIONS (the words proposed under D-UI-112, quoted on #1216) and the map's relink heading as FINISH RESTORE PROCESS (D-UI-046's wording), which settles PL-15's "FINISH RESTORE SETUP" line; S1's positive is a new ASan harness `tests/cloud-setup-repair-lifetime.py`; the lane's host unit build is T21's script copied (`TOTAL: 221 test cases in 4 binaries` at the pin).
- S3 (lane, 09:58): the brief's "read both at load, writing only the new one" does not fit `Settings`, which omits a value equal to its default; the lane keeps the old `system.cfg` key equal to the new value where it already exists (never added, nothing removed), accepted as read-both for a store that cannot say "explicitly default".
- S4 (lane, 10:08): the every-close `setrootpass` the brief and `05` PL-05 named is the SECURITY page's, under `BATOCERA` and not built on ROCKNIX; the two built password pages already ran no `setrootpass` on an unchanged close at the pin, so S4's fix is the guard against persisting an emptied entry (new `tests/device-password-apply.py`, three negative controls).
- S7 (lane, 11:02): the brief's "the form's script-supplied labels through a table with French" was over-broad -- rclone's vendor names and choice labels are proper names in the provider's words and stay; only the fork's two phrase labels (WINDOWS SHARE (SMB), AMAZON S3 AND COMPATIBLE) and the script sentences take French.
- Hand-back (lane, 12:48): the S12-S13 checkpoint's "13 new tests and 6 existing ones" was composed; by `git diff --name-status` it is 14 added and 5 modified (the lane corrected it in the retro and `00`). `GetShOutput` is ROCKNIX's own (absent from batocera), so its #585 line names ROCKNIX alone. The brief's literal "`shellQuote` on the argument" for the LED colour leaves `$( )` live for the outer shell: S10 quoted for both shells and proved it by running the command in bubblewrap (`tests/led-color-quoting.py`); `credential-quoting.py` cannot see an outer shell. The stand-in syntax check cannot compile `Platform.cpp` (no `SDL_PushEvent` fake); S8's function was compiled by its test. Two acceptance checkboxes (#1224's and #1230's first) claimed pin behaviour that never happened and are reworded at acceptance.

### T32 kickoff addendum (written with the brief's version 2, 2026-10-27)

**The plan, in the order's words:** T32 is *EmulationStation's game list views, scrapers and services*, `es-app-views-scrapers`, kind currency, lens cost against value, Independent: the 42 paths under `es-app/src/{views,scrapers,services}/` at the pin `16dbac5211` less `ViewController.*` (T2's) and `ScreenScraper.*` (T21's), 17,311 lines, of which the fork modified six (+168/-46 against the base and the same against `cada856d86` and `rocknix/master`); 36 are byte-identical to ROCKNIX's master and no upstream commit has touched the slice since the merge base, so the merge-debt question is a one-line record. The brief is `docs/reviews/briefs/es-app-views-scrapers.md` at version 2 (`85307da3b3`, after the stranger's proof of version 1 `2ed286145d`).

**Assumptions the plan leans on and does not state:** that the inventory's `shipped` reach is true for every source (T31's PL-25 found `GuiAutoScrape.*` compiled nowhere and inventoried as shipped; Backlog #1235 derives reach from the CMake lists); that `slices.json` is the membership where `order.md:607` prints one negative glob (it is; the brief says so and the line is corrected at the inventory's regeneration); that the pin is the read while T21's ES branch at `3ae9610b0` has already changed `Scraper.cpp` (the D-NET-017 media opt-out, the Retry-After reads through a new `ScraperReplies`) -- the lane reads the pin for the audit and T21's tip for those deltas, records each as inherited, and names every collision in the hand-back; that a scraper's success path can be shown somewhere (a no-NIC guest shows none: only ArcadeDB is plain http and stub-able, the three https scrapers are unit cases only; the brief's G-07 and G-10 are CANNOT); that the host can compile (it cannot: the one precedent is `Scraper.cpp` syntax-only under T21's stand-in headers).

**Known unknowns:** the SCREENSHOTS grid's per-tile cost on the interface thread, which needs a seeded library the window can afford (the lane's stage-B judgement); whether anything defines `CPPHTTPLIB_OPENSSL_SUPPORT` (nothing does: the local API on 127.0.0.1:1234 is plain HTTP, reached from the host over SSH as `vm-qa:479` does, not by a forward); the IGDB path (`IGDBScraper.cpp:143` is an `if` on two settings and `:144` its `return false`; the digest's "unreachable token request" was a credential-filter artifact, withdrawn); the #246 cursor shape at `ISimpleGameListView.cpp:462-464` (`reloadCollection` then `reloadGameListView`), which needs `CollectionSystemManager` read -- a later slice's file, so the brief asks for the read and names the owner.

**Patterns:** T26's generators asserting their counts and seen to exit 1 on a constructed drift; T21's generated unit-build script (rapidjson from the recipe's tarball plus its four patches, pugixml from the pin's extracted source, the `TOTAL:` line quoted); the trimmed, scanned packet with every hit dispositioned by name (the scrapers' macro gates, `httplib.h`'s 42 library names); the FAIL-first stub checked against the unfixed code first (T21's S11); the seat correcting a lane's census (T31's switch count), so a generator's count is the seat's to question as well as the proof's.

**What we could be missing (the simulation):** an Opus lane at Independent depth with only the brief: it reads two earlier briefs' sentence that `GuiScraperStart.cpp` is "T32's" and audits a `guis/` file -- the brief's ownership sentence says the globs decide and T31 holds it; it fixes `Scraper.cpp` at `:351`/`:618` where T21's branch already moved the lines to `:356`/`:628` -- read both; it closes `ThreadedScraper`'s unjoined thread and `delete this` with a join on the interface thread and costs the scrape page its CANCEL (D-UI-078, time to play) -- the stream bounds the join; it moves `HttpServerThread.cpp:574`'s notification off the pool thread by posting and changes `/launch`'s reply timing that `vm-qa:479` depends on -- the harness line is the proof; it reads a scan hit in `httplib.h` as a credential and trims the file to nothing, or ships a macro gate's value in the packet -- names only, every hit dispositioned; it reports `SKIPPED - YOU CANCELLED IT` over a completed run as a word to reword where D-UI-129 makes it a defect (`stop()` after `run()` finished, L-02).

**Adjustments before execution:** all in version 2 of the brief: the thirty-four corrections (six `file:line`, six figures, the four § 5 expectations, the issue states as OPEN until the integration moves the pin); the four placeholders defined where first used and added to the placeholder check; the floor's thirty-five pure leads carried into § 4 so a reader with only the brief has them; T13's conditions spelled out once; one `W` with the `qa-integration` stand-in before dispatch; the guest plan G-01 to G-11 with a 35 + 5 minute bound and its two CANNOTs; and the kit's pointer lines rewritten for T32 before seeding (T31's seeded pointer carried T26's).

### Errata from the stranger's proof of T32's brief (version 2, 2026-10-27)

The proof ran fourteen read-only commands against version 1 at `2ed286145d` (the coordinator's scratch file `t32-proof.md`): the membership block and the git half of § 5 reproduced exactly; four § 5 expectations differed (the T21-delta run's pathspec prints 6 rows, not 4; the `ASYNC_DONE|Ignore` grep's real lines are `336 371 374 612 630 633`, with IGDB's sixth `return false` at `230`; plain `g++` on `ThreadedScraper.cpp` fails on `curl/curl.h` through `HttpReq.h:5`, not on SDL; three runs cannot run before dispatch and are marked as the lane's at stage A or C); six `file:line` citations were off (`ThreadedScraper.h:80` is `pause()`, `isRunning()` is `:77`; the IGDB and HfsDB host literals; `md_image` at `:1060`; INVALID CREDENTIALS thrown at `:172`; the pin's Retry-After lines `:351`/`:618` against T21's `:356`/`:628`; `44d3c7e25` +7/-2 and `3ae9610b0` +13/-4); six figures were wrong (16 distinct routes over 27 registrations at `:149-803`; 30 `getCursor()` lines in 9 files, 20 in one; `claims.txt:38-39`'s frames are 1280x800; `vm-qa:349` is the link suite; two `getHelpPrompts()` overrides, not one per view; po line 115 the msgid and 116 the empty msgstr); five accepted slices' issues are OPEN, not closed; and a stranger could not resolve `COHASH`/`MERGE_HASH`/`TIPHASH`/`V2HASH`, the digests' lead numbers, "T13's conditions" or two different `W`s. All corrected in version 2 (`85307da3b3`), listed at its end.

### Errata from T31's acceptance (2026-10-27)

Eleven, appended to `docs/reviews/briefs/es-pages.md` § Errata at acceptance: the § 5 non-ASCII grep's basic-regex `\(` (use `-F`); the seeded pointer carrying T26's lens and rule lines; `popen` 1 (`GuiMoonlight.cpp:42`, with a space); `GuiKeyboardLayout.cpp:164` writing under `/tmp`; the LED parse guarded by `tokens.size() == 7`; the tab-switch `save()` writing when a save function stores a never-chosen default; `GuiAutoScrape` compiled nowhere and inventoried as shipped (Backlog #1235); the dialog landings by the generated count (50 sites: OK 30, NO 18, CANCEL 1, CLOSE 1); 21 active switches, not 23 (the seat's correction); the stream brief's S6 cherry-pick that does not apply alone (the coordinator's error, superseded by the fallback ruling); three § 5 runs that cannot run before dispatch. Two practice notes from the lane's day: a checkpoint heading typed by hand read 12:28 on a post made at 12:07 (a heading's time comes from `date -u` in the posting command); a chat summary named five ES hashes wrongly while every post and record took its hashes from `git rev-parse` (the record is the artifact, the summary is not).

### T33 kickoff addendum (written with the brief's version 2, 2026-10-27)

**The plan, in the order's words:** T33 is *EmulationStation's system layer: ApiSystem, game lists, collections, metadata*, `es-app-system`, kind currency, lens cost against value, Independent, the `rest` of `es-app` after the earlier slices. The order's words are half true: `ApiSystem.*` is T21's by a non-rest glob, `FileData.*`/`SystemData.*` T2's, `CloudText.*` T18's, so the 77 paths the `rest` selector leaves are the game lists, collections, metadata and filter library (`Gamelist`, `CollectionSystemManager`, `MetaData`, `FileFilterIndex`, `FileSorts`, `Genres`, `PlatformId`, `CustomFeatures`, `KeyboardMapping`, `SystemScreenSaver`, `ContentInstaller`, `ScraperSearchComponent`, `ThreadedBluetooth`, `ZaparooSupport`, the animations: all upstream-carried and byte-identical to ROCKNIX), 29 small fork helper units whose pages live in other slices, and Windows residue no image compiles. 16,276 lines; 27 fork-added and 4 fork-modified files (+2,689/-7); 0 upstream commits on the 77 since the merge base, so the merge debt is a one-line record. The brief is `docs/reviews/briefs/es-app-system.md` at version 2 (`c48f8b387e`, after the stranger's proof of version 1 `f462dfcda7`); #680 is retitled at dispatch to name what the slice is.

**Assumptions the plan leans on and does not state:** that every inventory row's `shipped` reach is true (`ScraperCmdLine.*` is in no CMake list and `Win32ApiSystem.*`, the `.rc`, the `.ico`, the `.aps` and the `.h.in` are platform-gated; Backlog #1235 carries both shapes); that "fork-own lines" measures fork code (4,522 by the tier, of which 1,269 are `Win32ApiSystem.cpp`'s dead body; the fork's insertions are 2,689); that the credential macros are the slice's (they are the top-level `CMakeLists.txt`'s, outside the 77); that the pin is the whole read while T21's branch already changed `es-app/CMakeLists.txt` and `WifiText.*` and T20's `OfflineAchievementsText.*` (read both, every collision named); that the host can compile (none of the 31 `.cpp` was ever syntax-checked here; the `FileData`/`SystemData` chain reaches no SDL, curl or vlc, and `external/pugixml` is a gitlink at the pin, so the stand-in check needs the pin's extracted source from the cache).

**Known unknowns:** whether the five `app-unit` test targets at the pin (`JourneyTiers`, `FolderMerge`, `RunLock`, `TextFit`, `AppWindow`; 18 cases, never built by any lane) build and pass with T31's script extended to `tests/app-unit/`; whether `Gamelist.cpp`'s in-place `save_file` at `:308/:474/:622/:841` loses a `gamelist.xml` the cloud's content restore brings after startup (D-CLOUD-049/078: a unit lead and a guest step, no fault seam for the write's atomicity); the collections' `rootFolder->clear()` then `reloadGameListView` (#246's shape, T32's L-16 handed over) on the guest; whether `SystemScreenSaver.cpp:157`'s ten retries over a cached miss ever end in a frame.

**Patterns:** T32's generators and their constructed drifts; T31's build script and its `TOTAL:` line; T21's stand-in syntax check with T31's thirteen fakes; the trimmed packet with every hit dispositioned (no macro value, no binary); the FAIL-first stub checked against the unfixed code; D-UI-129 (a completed run reported as cancelled is a defect, not a word).

**What we could be missing (the simulation):** an Opus lane with only the brief: it audits `ApiSystem.cpp` because the title names it (the brief's § 1 says who owns it); it counts `Win32ApiSystem.cpp`'s 1,269 lines as fork code to read whole (dead under `#if WIN32`; the packet never carries it); it fixes `Gamelist.cpp`'s writes with a temp-and-rename and breaks the exit's timing budget (D-CLOUD-119's 3 s: measure, then decide at the stage-D pause); it moves `NetworkThread`'s checks off `WatchersManager`'s lock by changing es-core's `WatchersManager.cpp` (T21's file: the contained fix is in the fork's callers, the lock change is named for the integration); it "fixes" the screensaver, the content installer, Bluetooth or Zaparoo as behaviour (D-UI-079: read and record; fix only a contained defect under rule 6); it ships `FileTag.cpp`'s three tag names into the catalog without the French (D-UI-051: the same commit).

**Adjustments before execution:** in version 2: the 32 corrections (seven `file:line`, the eleven write sites, the 196/196 translation fact, the seven audit folders named with their branches, the one `W`, the pugixml gitlink); the ownership rulings in § 1 (`Scripting.cpp` es-core's and routed; `DisplayAspect.cpp` and `CollectionSystemManager.cpp` T33's; `AppWindow.h` T33's with T2's finding; the three `writeAllText` sites under #1186 ruled at stage D; `GameCubeRvzHashRetry.h` against #609 ruled at stage D); the guest plan G-01 to G-10 with a 25 + 5 minute bound and its four CANNOTs; the retitle at dispatch; #1235 extended with `ScraperCmdLine.*` and the platform-gated files.

### Errata from the stranger's proof of T33's brief (version 2, 2026-10-27)

The proof ran eight read-only commands against version 1 at `f462dfcda7` (the coordinator's scratch file `t33-proof.md`): the membership block reproduced byte for byte on its second pass; every § 1 command and § 5 count held except the write sites (eleven, with the dead `Win32ApiSystem.cpp:979`); 41 of 48 spot checks passed and seven did not (four CMake conditionals, not three; `ContentInstaller.cpp:200`; `CloudExit.h`'s constants at `:21/:22/:28/:29`; 19 files include the earlier slices' headers, not 20; `ScraperSearchComponent.cpp:738-740` has a `getHelpPrompts`; `rescanIfFolderChanged` at `SystemData.cpp:378`; #69's milestone); the "42 empty `msgstr`" were multi-line openers and every one of the 196 msgids has a translation; three `[unverified]` items settled (the parse counts; the map check's line; plain `g++` on `MetaData.cpp` dying at pugixml's gitlink); a stranger stalled on the other lanes' audit folders never named, bare neighbour file names, "the register's :155-162", a heredoc "repeated, not shown", § 5's `W` before dispatch, and a checkbox that asked for map rows § 10 forbids. All corrected in version 2 (`c48f8b387e`), listed at its end; the ~1,300-line aim was not met because the tables are the lane's one copy of each.

### Errata from T32's acceptance (2026-10-27)

Eight, appended to `docs/reviews/briefs/es-app-views-scrapers.md` § Errata at acceptance: `atol(` has two sites; the local API's routes are 25 patterns over 27 registrations, `HttpReq` constructions 9, the `_("` counts include a comment, and po L116's `msgstr` continues on L117 (L-11's French half withdrawn); no shipped theme draws a grid, so L-14's per-tile cost is unreachable on the image; IGDB's NO GAMES FIT is the platform map, not the client id; G-05's count was ten minus a thread; the stand-in cannot compile `SystemView.cpp`; `05`'s PL-14 line was `:220`; the kit's clone path. From the hand-back: a `COULDN'T FINISH` outcome needs its why on the page (D-UI-030), which the lane's S2 had left bare for media, rename and resize failures -- S2b adds it before the merge.

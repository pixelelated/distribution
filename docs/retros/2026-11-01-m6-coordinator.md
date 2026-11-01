# Mini Retro: the M6 coordinator lane, 2026-10-26 to 2026-11-01 (#346)

**Completed:** 2026-11-01, 03:34 UTC
**Scope of this retro:** the coordinator's own work (D-WORKFLOW-183, D-WORKFLOW-189)
on `feature/m6-renovation-plan-346` between the last retro on this branch
(2026-10-26, `docs/retros/2026-10-26-m6-coordinator.md`) and now: T16 (#663),
T34 (#681) and T35 (#682) accepted and complete; T36 (#683), T37 (#684) and T38
(#685) researched, briefed, proven, dispatched and taken through their stages
(T36 to its hand-back, T37 to its stage-E streams, T38 to stage B); T39 (#686)
researched; the acceptance-script discipline (one shared script, derived per
slice, proven by positives); the host-coordination protocol with the M7 lane
(the queue of slots, the acknowledger, the hand blocks); the usage-limit cuts
of 2026-10-31 (06:5x, 11:5x, 16:4x) and the context resets they forced. Phase
tier. The slices' own retros live on their lane branches and are read at each
acceptance; this is the retro of the lane that wrote the briefs, ruled the
pauses and ran the acceptances.

**Branch:** `feature/m6-renovation-plan-346`, 243 commits since 2026-10-26
(`git log --since=2026-10-26 --format=%h | wc -l`). **Delta:** three slices
accepted (T16 16 of 17 criteria, T34 21 of 21, T35 20 of 21) and complete;
three briefs at version 2 after a stranger's proof (corrections: T36 16, T37
16, T38 11); five dispatch kits; four acceptance scripts (T35's re-derived,
T36's re-pointed twice, T37's and T38's derived from the shared `t36-accept.sh`
by `derive-t3N.py`), 80 FAIL/PASS positive pairs on T38's alone; the decided
rows D-CLOUD-192, D-CLOUD-193, D-WORKFLOW-214 to D-WORKFLOW-218, D-UI-134 to
D-UI-137; Backlogs #1335, #1336, #1344 to #1347, #1372, #1373, #1385; ten
friction lines (`docs/friction-log.md:882-891`); the October monthly summary.

### What worked well

- **The stranger's proof before dispatch kept paying.** T37's found that
  sourcing `config/options` for the effective values writes two build-root
  caches into the tree it runs in -- its own run left them in the research
  clone -- and version 2's ruling (k) moved the read into a scratch export
  before any lane ran it. T38's found the stage-A refs loop compared every
  lane against the wrong base and would have reported all 82 refs as moving
  the slice; version 2 compares against the coordinator's tip. Neither would
  have been caught by the drafter, who wrote both from the research.
- **One shared acceptance script, derived per slice, with refusals.**
  `kit/t36-accept.sh` is the shared code; `derive-t35.py`, `derive-t37.py` and
  `derive-t38.py` write the per-slice scripts through counted substitutions
  and refuse to write when a constant is read but not defined, a T36-only name
  survives, or a verdict counter is assigned. Three times an edit to the shared
  script landed while another derivation ran (03:14, 03:18, 03:20), and three
  times the derivation refused instead of writing a broken script. Every new
  section shipped with its FAIL seen before its PASS; the acceptance runs
  themselves then found their own defects before any tick (below).
- **The acceptance runs found the record short, not the ticks wrong.** T35's
  first read was `pass 38, fail 8`, six of the eight the script's; its second
  `pass 41, fail 4`, three of the four the lane's record (asked as one
  amendment, closed in one commit); the compile run `pass 48, fail 1` and the
  re-run clean. Twenty of twenty-one criteria ticked from verdict lines, the
  twenty-first left open with the behaviour that did not happen named (G-06's
  key gap). T36's hand-back read the same way: `pass 20, fail 21`, every FAIL a
  named line of the record, sent back as one list.
- **The acknowledger made the host contract hold without the coordinator's
  attention.** `kit/compile-ack.sh` acknowledges every lane's compile
  START/END lines and M7's START/RETURN lines within seconds with a census;
  after its widening at 23:4x and 00:1x it acknowledged M7's 23:40, 00:04,
  00:10, 00:14, 00:28, 00:30, 00:42 and 00:48 lines inside the minute, where
  the hand had been four and eight minutes late across a restart.
- **Held material stayed held.** T36's three findings under D-WORKFLOW-215
  became neutral public bugs (#1369 to #1371: file and symptom class only),
  their fixes landed as three streams whose posts and commit messages carried
  the bug number, the file and one phrase, and the maintainer was told by path
  on #346. Nothing from `held/` reached a public line.
- **Backlogs carry what the slices find and cannot fix:** #1372 (T36's seat's
  leaks, races and classifications), #1373 (`tools/skills-check` from T38's
  research: no check reads a skill for meaning), #1385 (the recipe checks that
  pass over nothing: `pkgcheck`'s rc 0 on a missing name, the freshness tool's
  missing-ref fail-open, `pixelelated-state-check --payload`'s `mcopy`, the
  verbose build's defines, and the fribidi choice).

### What was harder than expected

- **The hand block that asserted an empty queue was stale on arrival.** At
  23:36 M7's START landed seconds before a block saying no START was open, and
  T36's lane compiled two seconds on it. The block was written from the
  monitor's view, not from a read of the file in the same command.
  `kit/host-ack.sh --empty` now re-reads the file and exits 3 when a START
  stands after the last RETURN; `kit/t35-compile-run.sh` and its T36 twin
  refuse the same way before compiling and write the coordinator's own
  START/END pair. (Memory `host-ack-reread`.)
- **Killing the acknowledger by its parent pid left its loop alive.** Six
  stale `tail | while` subshells were found at 00:15, each still writing
  acknowledgements under a dead parent's pid, one with the first copy's
  three-lane pattern. The loop now runs in the main shell over a process
  substitution with a trap on the tail, and the clean-up pass that killed the
  stale tails also killed the host-file monitor's own tail (exit 144, re-armed
  with no line lost) -- a kill by pattern reached a process that was not the
  acknowledger's (blindspot 22's shape).
- **The usage-limit cuts cost the lanes their coordinator three times in one
  day,** and each resume re-armed monitors, re-read the host file for lines
  landed in the gap and re-prompted lanes that had ended turns on progress
  posts. The lanes ended turns on a progress post or a START post five times
  this stretch (T36 at 23:11 and 00:52, T36 at 01:14, T37 at 02:02 waiting on
  a seat call, T36 at 03:08); each cost a prompt (#1183). "A turn ends on a
  post or a commit" reads as permission to stop after any post.
- **The pointer seeding left the lane the fill.** T37's pointer carried the
  four hash words `COHASH`/`MERGE_HASH`/`TIPHASH`/`V2HASH` and a `Register:`
  line with a commit hash where the brief's § 10 wanted the decided table's
  IDs; the lane found six unfilled lines at stage A and filled them itself
  (comment 6551479786). T38's kit made the four words placeholders and the
  seeding filled every one (`kit/t37-fill-notes.txt`'s erratum).
- **Two acceptance-script defects took a run each to find:** the rulings
  prefilter kept only lines carrying "ruling" or "§ 1", so a table row headed
  `| (e) |` read as absent; the TOTAL picker took the first `TOTAL:` line of
  `02` § The runs where the section keeps the whole history and ends in the
  build's own. Both fixed in the shared code and proven on constructed
  positives (G1 to G5, H1 to H3) before the tick.
- **The brief's placeholder pattern missed two of its own placeholders**
  (`__V2HASH__` with a digit, `__REGISTER_IDS__` with an underscore); the
  commit check's `__[A-Z0-9]+__` missed one too. The wide pattern
  `__[A-Z0-9_]+__` binds from T38's errata on.

### What did we discover

- **A rule can be stale for weeks where no slice reads it.** T35's L-22 found
  `es-native-ui.md:30` still calling the progress card "top-right" against the
  centred card the same file's § Spacing describes; T36's L-08 and L-13 found
  `es-code-traps.md`'s font-height paragraph and `es-native-ui.md`'s
  `runSystemCommand` line wrong against the pin; T37's L-17 and L-18 found
  `device-builds.md` naming `maxengel/emulationstation-next` where the recipe
  clones `pixelelated/emulationstation`, and the per-device patches sentence in
  `CLAUDE.md`, `AGENTS.md` and `packaging-and-patches.md` saying
  `patches/<DEVICE>/` scopes a patch where `scripts/unpack:137-145` reaches it
  only through `PKG_PATCH_DIRS`. Six rule errata swept this stretch, each
  routed from a lane's read to the coordinator under D-WORKFLOW-189.
- **The coordinator's kit is unversioned and lives under `/workspace/tmp`.**
  The acceptance scripts and their derivations, the acknowledger, `host-ack.sh`,
  the compile-run wrappers, the tick scripts, the dispatch kits and the
  research files are the lane's working tools, and the host reboot of
  2026-10-28 already emptied the previous `/tmp` scratch once (friction
  2026-10-29 18:02). A learning that is a procedure becomes a tool
  (`learning-capture.md` § 3); a tool nobody can find or rebuild is not yet
  one.
- **The doctrine slices' selectors put the coordinator's own documents in a
  lane's scope.** T38's 52 include the three skill files the coordinator
  edited after the inventory; T39's 254 include `docs/reviews/**` (the plan,
  the briefs' index, P1's order and inventory, 12 paths), the generated
  catalog, `map.txt` and `rc-accept.txt`. The daily ledgers (work logs,
  futros, retros, audits, qa-logs, pointers) are T46's `records`, not T39's,
  and the registers and `NAMING.md` are T4's -- a premise the T39 research had
  to correct before the brief could carve the edit scope.
- **`docs/reviews/README.md` and `plan-for-the-plan.md` name P1's files and
  tools that live on `feature/m6-p1-survey-641` and not on the coordinator's
  branch** (`order.md`, `slices.json`, `inventory.json`, `areas.json`,
  `tools/renovation-inventory`). Every lane worktree carries both branches, so
  the lanes never saw it; a reader of the coordinator's branch alone does. The
  T39 brief's ruling (p) merges the P1 branch into the coordinator's before
  T39's dispatch.
- **The lanes' sessions load the rules of their worktrees.** T38's lane found
  nine of its loaded rules stale against the dispatch tip (its session's
  worktree was T5's `52e6794ba7`) and read them from the tip by `git show`
  (#367's shape, from the lane's side).
- **Two merge commits on a lane branch carried git's default subject.**
  T36's merges of the coordinator's branch (`715ec8951d`, `af9ff5df5d`) cite no
  issue; `tools/ceremony-check`'s `issues` line reads every commit reachable
  from `next` outside upstream's history, merges included, so the lane's
  branch would have failed the gate at the integration. Found by the
  acceptance script's `dist-tip` section; sent back for a merge-preserving
  rewrite before the second hand-back.
- **The futro's predictions are not tallied at acceptance.** The kickoff
  addenda for T36, T37 and T38 each list what the slice could miss, and the
  acceptance posts never say which predictions held; the calibration loop the
  `futro` skill describes is open for the slices.

### What adjustments are needed

- **Add (tool, Backlog):** the coordinator's kit gets a durable home in the
  tree -- the acceptance scripts and derivations, `compile-ack.sh`,
  `host-ack.sh`, the compile-run wrapper, the tick scripts, the dispatch and
  pointer templates -- under the fork's personal paths, with the host-file
  blindspot's guard then named in the tree. **Filed this session: Backlog #1386.**
- **Add (rule, Backlog):** the host-coordination protocol as a rule file --
  the queue of numbered slots, one runtime at a time, a START within 20
  minutes of the previous RETURN or re-queued, the START/RETURN first lines
  with their census and the detached timer named, no M6 compile over an open
  START, the acknowledgement within the minute and what acknowledges
  automatically, the hand block re-reading the file before it asserts the
  queue. It lives today in the kit's texts and the day logs. **Filed this
  session: Backlog #1387.**
- **Modify (practice):** one owner at a time on the shared `t36-accept.sh`;
  a derivation agent is told whether another edit is in flight. The
  refusals held three times; the practice removes the collision rather than
  relying on the guard. (Memory `shared-script-one-owner`.)
- **Modify (practice, the dispatch text):** "a turn ends on a question or on
  the stage's checkpoint post" replaces "a turn ends on a post or a commit",
  and a window message says "your turn ends on the RETURN post". Into T39's
  brief at version 2 and the kit's dispatch template.
- **Modify (practice):** the futro's predictions are tallied in the
  acceptance post (predictions confirmed N of M, by line); routed to T38's
  lane as an inherited item for the `futro` skill's table (comment on #685
  this session), since the skill is in T38's read.
- **Modify (practice):** a research or kit agent uses a named subfolder of
  the session scratchpad and never deletes outside it; one agent's clean-up
  removed every top-level scratch file this stretch and another's working
  directory vanished mid-run. Into the agent briefs from now.
- **No change to the dispatch order:** T39 (#686) to whichever lane frees
  first, then T41 to T43, T44 and T46, as the order says.

### Scoped audit findings (Step 2.5)

- **AC conformance (the coordinator's own contract: the M6 body's current
  plan and #346's seed brief):** PASS -- T16, T34 and T35 each have the
  acceptance comment with the run's summary, the ticks from verdict lines, the
  audit issue closed from its Phase 7 table (#1295, #1307, #1337), the
  close-out verified on a fresh clone (the coordinator's tip an ancestor, the
  completion marker hash-bound, the lint PASS both ways), and the sentence in
  the M6 body. T16's criterion 13 and T35's criterion 14 are open with the
  behaviour that did not happen named, not ticked.
- **Cornerstone spot-check (`working-principles.md`):** PARTIAL -- *a promise
  is not a mechanism* holds (the acknowledger, the wrappers and `host-ack.sh`
  are processes and files, named by pid and path); *verify the artifact* holds
  (every tick from a verdict line, every close-out on a fresh clone); *guards
  fail closed* holds (the derivations refuse, the wrappers refuse on an open
  START); *read, don't recall* did not hold for the lanes' sessions, which
  load their worktrees' rules (T38's nine stale) -- #367's gap from the
  lane's side, carried to the host-coordination rule's Backlog as a line for
  the dispatch text (read the rules from the dispatch tip by `git show`).
- **Interaction-defect scan:** PARTIAL -- three shared-state pairs were
  found and fixed: the shared acceptance script edited while derived from
  (the refusal held; the practice now serializes), the host file written from
  memory while M7's START landed (`host-ack.sh --empty`), the acknowledger's
  stale subshells (the loop restructured). One remains by design: the three
  lanes' compiles and the coordinator's acceptance compiles share one host
  under the no-compile-over-a-START rule, which the lanes read themselves;
  T36's lane stood down for M7's START at 23:37 on its own pre-check, and for
  T37's window on the coordinator's word.
- **Futro prediction verification:** UNTESTABLE this retro -- the kickoff
  addenda's predictions were not tallied at the acceptances (see the
  discovery above and the adjustment that closes it).
- **Housekeeping (the gates):** PASS -- `tools/ceremony-check --gate` green
  on every push this stretch (`tools/register-check`, `tools/work-log-index
  --check`, `tools/rules-check --quiet` with it); the October monthly summary
  landed at `dac7211001`; this retro pays the `retro` line due since
  2026-10-26 plus five active days.
- **UI-review artifact:** SKIP -- no UI surface touched by the coordinator;
  the slices' frames are theirs (T36's and T37's windows ran inside their
  bounds with their disks retired).
- **Harness self-coverage:** PARTIAL -- the acceptance scripts cover the
  failure modes met while landing them (six defects in T35's first read, the
  rulings prefilter, the TOTAL picker, the `nf`/`nr` counter reuse, each with
  a positive after the fix), the acknowledger and the hand blocks cover the
  late and stale acknowledgements they were built for; none of it is in the
  tree (the Backlog above).
- **Documentation and glossary freshness:** PARTIAL -- six rule errata swept
  in the same session they were routed; the register carries the stretch's
  decisions by ID; the host contract's nouns (slot, the queue, the hand block,
  the acknowledger) have no rule of their own yet (the Backlog above).
- **Build-vs-adopt honor check:** SKIP -- no build-vs-adopt answer is recorded
  for the coordinator's tooling; the kit adopts the fork's own tools
  (`ceremony-check`, `register-check`, `lint-audit-artifacts`) and builds
  only the glue.

### Practice adjustments

- The `mini-retro` skill's scoped-audit check 4 (futro prediction
  verification) presumes the predictions were tallied at close; for the
  renovation's slices they are not, because the acceptance post has no line
  for them. The fix is in the acceptance post's shape, not the skill; routed
  to T38's lane for the `futro` skill's own table (comment on #685).
- The retro cadence is the coordinator's and the lanes' retros do not pay it
  (the 2026-10-26 retro's note); this retro ran at five active days, the
  check's first DUE line, not at seven, the block.

### Housekeeping items (not blocking the next slice)

- The register rows D-INFRA-024, D-WORKFLOW-171 to 180, 188 and 206 to 208 are
  not on this branch (they are on the P1 and M7 branches); the integration
  reconciles them, and `tools/register-check` reads only this branch's table.
- `kit/compile-ack-test*.txt`, `kit/host-ack-test.txt` and the retired scratch
  clones under `kit/selftest/` are the session's; the kit's promotion to the
  tree decides what is kept.
- `docs/reviews/README.md` and `plan-for-the-plan.md` name P1's files that
  this branch lacks until the P1 branch is merged (T39's ruling (p)).

### Code-verifiable state

| Slice | State | Tips |
| --- | --- | --- |
| T16 (#663) | complete | distribution `abc3181e44` |
| T34 (#681) | complete | distribution `49c6b43f27`, ES `52f0ff512` |
| T35 (#682) | complete | distribution `d828355e0a`, ES `b7fdb3a24` |
| T36 (#683) | hand-back read, amendment asked | distribution `af9ff5df5d`, ES `9c1bd5f09` |
| T37 (#684) | stage E, S1 landed | distribution `a22e13adee` |
| T38 (#685) | stage B | distribution `98019cea9f` |
| T39 (#686) | research in, brief v1 drafting | -- |

---

**Phase complete for the coordinator lane. The next kickoff is T39's dispatch
(begin-delivery's shape: the retro read, the futro addendum, the brief at
version 2).**

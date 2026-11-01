# T4's remediation streams (#651, audit issue #912)

Written by the coordinator at T4's stage-D pause (2026-10-24, 15:13 UTC post
at `9d67c57ab0`; D-WORKFLOW-189). Twenty-five items, eight streams on the
doctrine itself and one tool packet. The futro's pre-mortem rule holds: **one
stream per rule file (or pair) for wording; a rule wrong twice goes to a
tool**, and the one tool here (`ceremony-check`, #905) is another area's, so
it goes as a packet cut by the T1 session, not as this lane's stream. Every
stream is a doctrine edit under a brief, which is the one way a rule changes
in this slice (brief § 1); each edit **says what is true at the tree the
lane read (`8ebaf8daad`) and at its own `fixed-at`**, verified by the command
the bug or the item names, never a sentence the lane believes. Plan § 6b E
binds every stream: **a commit names its paths**; **a time is produced,
never typed**; **prose goes into a running log through a quoted heredoc or
the Write tool** (the lane's own 15:09 friction line is the reminder).
`tools/rules-check --quiet` runs after every stream that touches `CLAUDE.md`,
`AGENTS.md` or a rule's front matter: it holds `AGENTS.md` to Codex's budget
and the two entry files' counts to the rule directory (D-WORKFLOW-045). The
coordinator's own edits of today (`engineering-practices.md`,
`device-builds.md`, `generic-x64-vm-testing.md`, the registers) are already
on this branch through the merge at `e3897db16d`; a stream edits the
paragraph the item names and nothing beside it, so the merge after the M7
candidate stays a merge.

## S1. The two entry files: `CLAUDE.md` and `AGENTS.md` (PL-01's sentence, PL-03, PL-04, PL-06, PL-07, PL-08, PL-09; #904) -- `fix-tree`

- **Why a stream:** seven sentences a session reads at every start are wrong
  about the tree; each has a command that shows the true fact.
- **Files owned:** `CLAUDE.md`, `AGENTS.md`. Nothing else: the index
  (`instruction-files.md`) is S7's; the legacy-layout lines in both files
  are #640's (PL-23), unchanged.
- **The changes, each with its proof:**
  - **PL-01 (#904, first criterion -- the sentence, not the tool):**
    `AGENTS.md:19-20`'s claim that `tools/rules-check` keeps it and
    `CLAUDE.md` equal becomes what the tool's header says it checks (`git
    show HEAD:tools/rules-check | sed -n '11,27p'`): the count, the list and
    the mention. The tool is not changed here.
  - **PL-03 (#904, second):** `CLAUDE.md:88` and `AGENTS.md:86` stop saying
    `mkimage` *needs OS_VERSION/BUILD_DATE exported*; the replacement says
    what `distributions/ROCKNIX/version:8` and
    `distributions/ROCKNIX/options:212` do (read both; quote the lines in
    the commit).
  - **PL-04 (#904, third):** the vocabulary sentence in both files names the
    three things `tools/vocabulary-check` checks, from its header.
  - **PL-06:** `CLAUDE.md:27` *the four principles* names the count its list
    has (five).
  - **PL-07:** the make-target lists either match `Makefile`'s device
    targets at `fixed-at` (`grep -nE '^[A-Z0-9]+:' Makefile`, the list quoted)
    or say they are examples; `world` is described as `Makefile:42` has it.
  - **PL-08:** *pull Rasteratops mirror* (`CLAUDE.md:65`, `AGENTS.md:63`)
    names the image the Makefile pins (`grep -n 'ghcr.io' Makefile`), with
    Rasteratops left as the character D-WORKFLOW-144 says it is;
    `grep -n 'Rasteratops mirror' CLAUDE.md AGENTS.md` prints nothing after.
  - **PL-09:** *two* interface-law documents (`CLAUDE.md:34`, `AGENTS.md:31`)
    becomes the three `instruction-files.md:122` names, the same three in
    all three files.
- **The test:** the four `grep` lines above before (hits) and after (none);
  `tools/rules-check --quiet` rc 0 after (it is the guard on these two
  files: run it before the commit, and if it fails on a count, the count is
  what to fix, not the check).
- **Acceptance:** #904's four criteria; PL-06 to PL-09's acceptance lines
  as the punch list has them.
- **Commit:** `doctrine: the two entry files say what the tree does
  (rules-check's scope, mkimage's version, the vocabulary check, the counts,
  the targets, the mirror, the three interface documents)`, `Refs #904,
  #912, #651`, the attribution line; `git add -- CLAUDE.md AGENTS.md`.

## S2. `time-to-play.md` and `least-surprise.md` (PL-10; #906) -- `fix-tree`

- **Why a stream:** two every-session rules describe a launch over a running
  sync by rows D-CLOUD-130 superseded; a design read against them is a
  design read against a reversed decision (T2 met it).
- **Files owned:** `.claude/rules/time-to-play.md` (its *What ships today* /
  D-CLOUD-109 bullets), `.claude/rules/least-surprise.md:18-20`.
- **The change:** both describe the launch over a running sync as
  D-CLOUD-130 does -- the question (the statement, one consequence, two
  verbs: STOP IT AND PLAY / KEEP WAITING), citing D-CLOUD-130 by ID and
  leaving D-CLOUD-076 and 109 as the history they are (named as superseded,
  not deleted: `decision-register.md`'s reversal-sweep rule, audit #258
  P-01, is what this stream completes). `grep -n 'What ships today'
  .claude/rules/time-to-play.md` prints nothing after.
- **The test:** `tools/archaeology D-CLOUD-130` read first for the row's
  own words; `tools/register-check` and `tools/rules-check --quiet` rc 0
  after.
- **Acceptance:** #906's two criteria.
- **Commit:** `doctrine: the launch over a running sync is D-CLOUD-130's
  question in time-to-play.md and least-surprise.md`, `Refs #906, #912,
  #651`.

## S3. `generic-x64-vm-testing.md`, with `es-code-traps.md:182` (PL-11, PL-12, PL-13; #907, #908) -- `fix-tree`

- **Why a stream:** the VM rule is the one every QA proof follows, and it
  carries eight sentences the tree contradicts.
- **Files owned:** `.claude/rules/generic-x64-vm-testing.md`,
  `.claude/rules/es-code-traps.md` (line 182 only).
- **The changes, each with its proof:**
  - **#907 (PL-11):** the three sentences that say `/var/log` does not
    survive a boot (`generic-x64-vm-testing.md:763`, `:1003`;
    `es-code-traps.md:182`) say what `var-log.mount` does (the bind of
    `/storage/.cache/log`, the `volatile-log` opt-out where it matters;
    `handheld-evidence.md`'s table is the shape to agree with); `grep -n -E
    "/var/log. is lost|/var/log. does not survive|es_log.txt. is tmpfs"
    .claude/rules/*.md` prints nothing after.
  - **#908 (PL-12):** `:692` names the tool that makes the UTM bundle
    (`generic-x64-vm utm`); `realpath` leaves the list of applets the guest
    lacks (`CONFIG_REALPATH=y`); the `emustation` sentence says the unit is
    installed and inactive with ES under `essway.service`; the QA-run
    sentence carries `--record-only`.
  - **PL-13:** the headless comment's display, the four named `vm-qa`
    suites of 17, and the watchdog's home match `generic-x64-vm:281-295`,
    `vm-qa:63` and `generic-x64-vm:435` at `fixed-at` (each line read, not
    recalled).
- **The test:** the greps above; `tools/rules-check --quiet` rc 0.
- **Acceptance:** #907's and #908's criteria; PL-13's line.
- **Commit:** `doctrine: generic-x64-vm-testing.md and es-code-traps.md say
  what the image and the tools do (var-log.mount, the UTM tool, realpath,
  essway, --record-only, the headless display, the suites, the watchdog)`,
  `Refs #907, #908, #912, #651`.

## S4. `rclone-cloud-sync.md` (PL-18; #909) -- `fix-tree`

- **Files owned:** `.claude/rules/rclone-cloud-sync.md`.
- **The changes:** the bump sentence names the two per-arch `PKG_SHA256`
  values to refresh (`projects/ROCKNIX/packages/network/rclone/package.mk`
  read at `fixed-at`); the shipped version is not stated as a number, or
  matches `PKG_VERSION`; the settings-archive sentences name `tar.gz` and
  match `cloud_sync-rules.txt`'s include lines; the `cloud-round-trip`
  sentence names exit 69, matching the tool; the scope paragraph says the
  saves tier's allowlist is what it describes and points at the content tier
  for ROMs and BIOS.
- **The test:** each fact's source line quoted in the commit; `tools/rules-check
  --quiet` rc 0.
- **Acceptance:** #909's six criteria.
- **Commit:** `doctrine: rclone-cloud-sync.md says what the rclone package
  and the cloud scripts do today`, `Refs #909, #912, #651`.

## S5. `fork-workflow.md` and `device-builds.md`: the remotes (PL-16; #910) -- `fix-tree`

- **Files owned:** `.claude/rules/fork-workflow.md` (the PR command's
  `--head`), `.claude/rules/device-builds.md` § Iterating on EmulationStation
  (the ES checkout's `origin`).
- **The change:** the PR command's `--head` owner is `origin`'s (`git remote
  get-url origin`), or derived from it in the command; the ES section names
  the ES checkout's current `origin` (`git -C <the ES checkout> remote -v`,
  read only). Nothing else in either file: `device-builds.md`'s other
  paragraphs are the coordinator's today and S6's.
- **The test:** `grep -n 'maxengel' .claude/rules/fork-workflow.md
  .claude/rules/device-builds.md` before and after (the ES PR history line
  may keep the name as history, marked so); `tools/rules-check --quiet` rc 0.
- **Acceptance:** #910's three criteria.
- **Commit:** `doctrine: the PR command and the ES section name the fork's
  own remotes`, `Refs #910, #912, #651`.

## S6. The build-root names in four rules (PL-14) -- `fix-tree`

- **Files owned:** the eight lines `grep -n 'build\.ROCKNIX-'
  .claude/rules/*.md` prints at `8ebaf8daad` (in `device-builds.md`,
  `packaging-and-patches.md`, `es-code-traps.md`, `worktrees.md`), and only
  those lines.
- **The change:** each becomes `build.pixelelated-*` (`config/path:19`), or
  marks itself historical where it quotes a dated event (a 2026-09 crash
  read against a `build.ROCKNIX-` root is history and says so).
- **The test:** `grep -c 'build\.ROCKNIX-' .claude/rules/*.md` is 0 after,
  or each remaining line carries its historical marker; `tools/rules-check
  --quiet` rc 0.
- **Acceptance:** PL-14's line.
- **Commit:** `doctrine: the build roots are build.pixelelated-* in the
  rules, the dated cases marked as history`, `Refs #912, #651`.

## S7. `instruction-files.md`: the index (PL-15, PL-19) -- `fix-tree`

- **Files owned:** `.claude/rules/instruction-files.md` only.
- **The changes:** `:156` says `cloud-pair-migration` is retired, as
  `:205-206` do, matching `cloud-pair-migration:58-62` (PL-15). For PL-19,
  each of the 31 *Detail in* rows that names a rule which never names the
  tool is re-pointed at the rule that does carry the detail, or, where no
  rule describes the tool, says so in the row (*its own header is the
  detail*) -- the index is corrected, the eight rules are not grown here
  (a rule gaining a paragraph for every tool is a separate decision, the
  coordinator's; T10 reads the tools themselves).
- **The test:** `tools/t4-q6.py`-style search prints 0 unnamed pairs at
  `fixed-at`, or the rows say where the detail is; `tools/rules-check
  --quiet` rc 0.
- **Acceptance:** PL-15's and PL-19's lines.
- **Commit:** `doctrine: the tool index points at the rule that carries
  each detail, and names the retired tool as retired`, `Refs #912, #651`.

## S8. `ceremonies.md`'s friction row, after the #905 packet (PL-02's rule half) -- `fix-tree`

- **Why last, and only after the packet:** `tools/ceremony-check` is
  another area's (T10's) and is fixed by the packet
  `fix/m6-905-ceremony-check-friction` the T1 session cuts
  (`docs/reviews/briefs/fix-packet-905-ceremony-friction.md`); the rule's
  friction row then says the shape the fixed check reads, matching the
  tool. Until the packet is posted on #905, S8 waits; the lane reads the
  packet's diff on #905, not the T1 session's worktree.
- **Files owned:** `.claude/rules/ceremonies.md`, the friction row of the
  ceremonies table and the *What a friction entry is* paragraph if it names
  the shape.
- **Acceptance:** #905's third criterion.
- **Commit:** `doctrine: the friction row says the shape ceremony-check
  reads`, `Refs #905, #912, #651`.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-02 (#905, the tool half) and PL-21 (the six prose blocks under
  `## Entries`):** deferred to the packet `fix/m6-905-ceremony-check-friction`
  (the T1 session; the brief beside this one): the check reads every dated
  line, names the non-entry lines, and its constructed failure is a fixture
  that fails on the unfixed tool. The bug stays open until the packet is
  reviewed; S8 follows it.
- **PL-01's tool half (`rules-check`'s *twins*):** withdrawn as a tool
  change -- #904's first criterion is met by the sentence (S1), and a
  twin-check between `CLAUDE.md` and `AGENTS.md` is a design the two files
  were deliberately not given (AGENTS.md is held to Codex's budget,
  D-WORKFLOW-045); the lane records the verdict.
- **PL-05:** deferred to #808 (the 29 of 30 table), already filed.
- **PL-17 (#911):** deferred to **T38 (#685)**, the skills, agents and
  settings slice: `council-substrate-integrity.md` is adopted verbatim and
  refreshed by deliberate re-review, not edited here (`instruction-files.md`
  § The front-matter standard; #147 § 9), and the re-review against its
  source estate is T38's read; the coordinator posts the lead on #685; the
  bug stays open, Low.
- **PL-20 (`register-check`'s column shape; the in-place changes; the
  unescaped pipes):** deferred to **T10 (#657)** as a lead the coordinator
  posts: the shape check and an in-place-edit detector are the tool's, and
  the six unescaped pipes in decided rows are fixed only by a clerical row
  (D-WORKFLOW-013) if the maintainer wants them fixed at all -- a decided
  row is never edited for formatting. D-QA-040's `**Open:**` prefix is an
  open row's, allowed; D-RA-006's in-place change is named on #657 for the
  detector's control.
- **PL-22:** deferred to #811. **PL-23:** deferred to #640 (the 25 lines
  name the layout #640 says is current, at its cutover). **PL-25:** deferred
  to #645 (upstream's PR rules enter `fork-workflow.md` when #645's facts
  are established there; the coordinator's).
- **PL-24 (5,179 lines every session; the three largest rules' narrative;
  `handheld-evidence.md`'s `docs/**` glob):** **withdrawn** as a stream, with
  the reason: the every-session load is the maintainer's deliberate design
  (`instruction-files.md` § `paths:` is optional, and omitting it is a
  decision; D-WORKFLOW-008 split the ES rules by that reasoning), and a
  split of `generic-x64-vm-testing.md`, `rclone-cloud-sync.md` or
  `engineering-practices.md` into narrative and instruction is a doctrine
  design change the coordinator puts to the maintainer as an observation on
  #346 with the figures, not a stream of this slice. The glob question
  (`docs/**` loading `handheld-evidence.md` for any record) is a lead for
  T39 (#686, the reference documents), posted by the coordinator.

## Order and hand-back

S1 to S7 in order, each committed and proved before the next (the
`rules-check` run after each is the gate); S8 when the packet is posted on
#905. Then stage F (`02` appended, every proof's `proved:` cell one of
`tree`, `history`, `tool-run`, `fix-tree`, `fix-pending-session` -- the
last for a sentence whose proof is the next session that reads it), stage G
(the retro: what the slice did to the two time-to-play numbers -- nothing,
say so), stage H (the hand-back on #651, `reviewed-at:`/`fixed-at:` in its
body; the Phase 7 table with every item's outcome as above). The coordinator
accepts by brief § 10 on an export of the tip (`rules-check`,
`register-check`, the greps the streams name, `tools/t4-q6.py` for PL-19)
and closes #912. **A stream that would edit a rule outside the paragraph its
item names, a decided register row, `.github/sessions/saved-session-state-next.md`,
or any file outside the ones named, stops and asks on #651** -- and does not
end its turn on the question: it posts it and continues with what does not
depend on the answer.

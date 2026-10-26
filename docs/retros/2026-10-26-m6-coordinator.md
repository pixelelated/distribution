# Mini Retro: the M6 coordinator lane, 2026-10-15 to 2026-10-26 (#346)

**Completed:** 2026-10-26, 08:2x UTC
**Scope of this retro:** the coordinator's own work (D-WORKFLOW-183, D-WORKFLOW-189)
on `feature/m6-renovation-plan-346` between the last retro on this branch
(2026-10-15, M7's audit-to-device-builds) and now: the P2 slices briefed,
dispatched, accepted and closed out (T45, T23, T40, T11, T27, T13, T25, T22,
T28, T29; T2, T1, T3 and P1 before them), T15, T16 and T17 in flight, the
session cut of 2026-10-25 12:08 UTC and the recovery of 2026-10-26, and the
host handoff to M7. Phase tier. The slices' own retros live on their lane
branches and were read at each acceptance; this is the retro of the lane that
wrote the briefs, ruled the pauses and ran the acceptances.

**Branch:** `feature/m6-renovation-plan-346`, 381 commits since 2026-10-15
(51 / 8 / 5 / 11 / 31 / 150 / 104 / 21 by day, the 24th and 25th the dispatch
days). **Delta:** ten slices accepted and closed out in the window, each with
a brief at version 2 after a stranger's proof (corrections per brief: T25 15,
T28 15, T16 17, T29 12, T17 11), 84 friction lines, blindspots 52 to 76 on
the register, D-WORKFLOW-209 and D-CLOUD-185 decided, #1118 through #1135
filed by the coordinator this day.

### What worked well

- **The stranger's proof before every dispatch.** A reader with no context,
  ten commands, from a scratch clone: it found T29's tree-wide shape block
  unrunnable (`awk '{print $4}'` over paths with spaces) and T17's central
  premise wrong (two "writers through rclone" that did not exist). Every
  brief needed it; none would have survived dispatch unchanged. The version-2
  note at the brief's end, listing the corrections, is what the lane reads
  first.
- **Acceptance by re-running the brief's own blocks on a clone of the tip**
  (`$S/tNN-accept.sh`), never from the hand-back's words. T29's report
  reproduced every figure of version 2 with its population; the three
  streams' files were the only non-docs change since dispatch, read from
  `git diff --name-only`.
- **Generated tables with asserted counts, exiting 1 on drift** (T16's,
  T29's `t29-tables.py`, T17's `t17-tables.py`): the entries, the boards,
  the writers, the secrets' paths. A table nobody typed cannot be off by
  one.
- **Fixture first, then the fix, the FAIL recorded before the fix lands**
  (T29's S1 to S3, T17's six streams): the positive is on disk before the
  change, so a fix that could not have failed is visible at once.
- **Reconciliation from the host, not from timers**, at the recovery: the
  six dead monitors, the one live guest, the lanes' screens, M7's
  checkpoint read with provenance -- each a command and its output on
  #1118 before any allocation was posted.
- **The host file as the one place two programs meet.** M7 asked, M6
  granted, both posted START and RETURN; the handoff, the queue and the
  stop were explicit lines anyone could read.

### What was harder than expected

- **Watches that cannot report absence.** Three in one day: the T16 mirror
  ended on its cap with `return=0` after a RETURN that never came; the
  host-file monitor keyed on `== ` and missed M7's timestamped lines for an
  hour; the T17 mirror matched one START shape and said nothing when the
  lane wrote another. Each was a session shell loop with no positive run
  against its input and no exit for "the thing I watch for did not happen"
  -- blindspot 22's shape, in the coordinator's own tooling, three times.
  #1135 is the tool; `engineering-practices.md` § Say how the watch fails
  gains the window's sentence.
- **A bound that nothing enforced.** T16's window was granted for 30
  minutes; the lane's session was cut by its account's weekly limit; the
  guest ran 20 hours. The mirror knew the bound and could have stopped the
  guest by pidfile at bound plus grace -- it only mirrored. The stop, when
  it came, was refused to this session twice by its permission classifier
  and taken by the owner: a bound without a mechanism is a number in a
  comment.
- **Figures from memory.** The T29 stream brief named a donor bash that the
  donor does not hold (busybox and rclone only, says its own RECORD.txt);
  version 2 of T29's brief said `rocknix-info:12` lacks a `/`-to-`-` sed
  that is there; the T17 brief's "two writers through rclone" came from a
  verb's name in a grep, not from the write. Each was a claim about an
  artifact made without reading the artifact (blindspot 75's altitude),
  and each was caught -- by the lane, by the proof -- after it had cost a
  question.
- **Times typed as estimates.** Six log headings and comment stamps read
  `06:0x`, `06:1x`, `06:2x` while the clock read 05:3x to 05:58; fixed in a
  later commit from `git log`'s times. The lanes' rule, *its time from
  `date -u` in the same command*, applies to the coordinator too.
- **Attribution.** A pasted coordination prompt was recorded on #1118 as
  the maintainer's verbatim request; it was an agent's relay, and the
  owner's words were one sentence. D-QA-012 wants the requester's words,
  and a paste with no words of the owner's own says who wrote it.
- **The cadence the gate enforces.** This retro is two days past its
  cadence. The slice retros arrived every few hours on the lane branches
  and felt like retros; they are the lanes', and the coordinator's own scope
  had none since the 15th. The gate (`tools/ceremony-check --gate`) said so
  at the commit that wrote this sentence, which is the gate doing its job
  and the coordinator not having run it before each push.
- **A session cut mid-watch.** The usage limit at 12:08 on the 25th cut
  this session with a window open, a stage running and a research
  subagent launched; the three lane sessions fell at the same minutes on
  their own account's weekly limit. Nothing announced it; the recovery
  began sixteen hours later, from the pointer and the host.

### What did we discover

- **Every brief's first version carried a claim its proof refuted**, and the
  decisive ones were about the thing the lens was built on: the shape block
  (T29), the writers (T17). A brief is a plan; the proof is the first run of
  it, and ten commands from a clone is cheap against a dispatched lane
  reading a wrong premise for an hour.
- **A lane's deltas are the brief's errata, and they are consistent in
  kind:** a count the proof took over the directory rather than the slice
  (T29's history), a board list that kept a duplicate (28 against 26), a
  tool whose default checkout exists on the host (T17's vocabulary check).
  The errata sections at acceptance are the record that version 3 would
  be written from.
- **The seat's priority differs from the lane's, and the order is the
  coordinator's.** T29's seat ranked the VM take-back first; the lane
  proposed recording it under D-QA-053; the ruling made it a bug on
  `upgrade-and-install.md`'s "never move what you did not put there".
  T17's two seats raised F-02 and F-03 to Medium against the lane's Low,
  and the ruling followed the seats on impact. The pause exists for this.
- **One finding reaches two slices.** T17's F-02 (the conf's rclone flags
  reaching the deleting sync) is T16's twins' too; the allowlist became a
  register row (D-CLOUD-185) so the second lane fixes to the same contract
  without a second argument, and the seam was posted on #663 for a session
  that cannot read it until Oct 30.
- **M7 and M6 share one host and nothing else.** The handoff worked
  because it was explicit (what runs now, what waits, who asks where); it
  failed only where a watch assumed M7's line shape. The queue restated at
  06:44 (M7, then T17, then T16 when its session can run) is the model: a
  bound, an order, and the condition that moves each.
- **The lanes caught the coordinator twice**: T29's `rocknix-info:12`, the
  donor bash; T17's `tools/vocabulary-check` checkout. A lane that reads the
  artifact outranks a brief that remembered it.

### What adjustments are needed

- **Add:** `docs/reviews/plan-for-the-plan.md` § 6b carries the brief
  practice that grew in this window and lives nowhere else: a stranger's
  proof before dispatch, version 2 with its corrections listed, every
  figure with its population, every block run from a clone, every binary
  or path named only after `ls` has seen it, the errata at acceptance.
  **Done this session.**
- **Add:** `engineering-practices.md` § Say how the watch fails gains the
  granted window's sentence: a window names what stops the guest at bound
  plus grace, or says that nothing does; a mirror names its post contract
  and its exit for a START with no RETURN. **Done this session.**
- **Add (tool):** #1135, the guest-window mirror as a tool with a self-test
  over the recorded post shapes and a non-zero exit for a START with no
  RETURN. Filed.
- **Modify (practice):** the coordinator runs `tools/ceremony-check --gate`
  before each push, not only when the hook runs it; the retro cadence is
  the coordinator's own and the lanes' retros do not pay it.
- **Modify (practice):** every heading and comment stamp from `date -u` in
  the same command; no `0x` estimates.
- **No change to the dispatch order**: T18 (#665) and T41 to T43 next, as
  the order says; T16's resumption and T15's close-out wait on the owner's
  account decision, not on the plan.

### Scoped audit findings (Step 2.5)

- **AC conformance (the coordinator's own contract: the M6 body's item 4
  and #346's seed brief):** PASS -- every accepted slice has its acceptance
  comment with the report's path, its audit issue closed from the Phase 7
  table, its close-out verified (tip's parent, marker, lint, scratch), and
  its sentence in the M6 body; the body's header time moved with each. One
  PARTIAL: the pointer's `m6-t1-20261024` image copy never existed (T16's
  grant named the `m6-t3` copy; T17's lane found `m6-t2-20261023`); the
  pointer now names what `ls` shows.
- **Cornerstone spot-check (five, `working-principles.md`):** *evidence over
  opinion* PASS (accept scripts, generated tables); *explicit over implicit*
  PASS (D-WORKFLOW-209, D-CLOUD-185, the rulings posted); *preservation
  over deletion* PASS (T16's disk retained with its D-INFRA-022 reason, the
  take-back bounded to known bytes); *read, don't recall* **FAIL** (the
  donor bash, `rocknix-info:12`, the two writers -- three claims from
  memory); *fail loudly / fail closed* **FAIL** (three silent watches).
- **Interaction-defect scan:** PARTIAL -- the host file is shared state
  between two programs with two line shapes, and the M6 monitor read one;
  the ledgers (friction log, day logs, index, register) merged by union at
  every hand-back without a lost entry; the two image copies and the donor
  are read-only and never contended.
- **Futro prediction verification:** 2 of 5 kickoff addenda predicted the
  stream count (T25 none, none; T28 one, one; T22 four of which two struck,
  two landed; T29 none, three; T17 none, six) -- 40 %. The addenda predict
  structure well (tiers, seams, VM answers held every time) and defects
  badly, which is the honest shape: a futro cannot know what the read will
  find, and "none expected" should read "none predicted".
- **Housekeeping:** `tools/register-check` PASS (681 IDs, each once);
  `tools/rules-check --quiet` PASS; `tools/work-log-index --check` current;
  `tools/box-check` 1 FAIL (#1126's checkbox named a device; reworded, 0
  fail); `tools/ceremony-check --gate` BLOCK on this retro's absence (this
  file).
- **Harness self-coverage:** FAIL -- the mirror, three times (above); the
  accept scripts PASS on what they claim and miss section headings written
  with a prefix (`## § The pins`) and bold rows (`| **`), noted in the
  pointer and tolerated because the lanes' generators assert the counts.
- **UI-review artifact:** SKIP -- no UI surface touched by the coordinator.
- **Documentation and glossary freshness:** PARTIAL -- `generic-x64-vm-testing.md`
  took three paragraphs on the 25th (vendor-linked units, the candidate
  image, the initramfs busybox); `plan-for-the-plan.md` § 6b lacked the
  brief practice until this session; no new proper noun without a home.
- **Build-vs-adopt:** SKIP -- a coordination phase; no build-vs-adopt answer
  recorded.

### Practice adjustments

- **The mini-retro's own cadence check belongs in the coordinator's push
  chain**, not only in the hook: `tools/ceremony-check --gate` before every
  `git push`, and a BLOCK stops the push. The three accept scripts and
  every commit chain already gate on `register-check`; the gate is one more
  line.
- **The futro addendum's "Before execution" list should say "streams
  predicted: N" rather than "none expected"**, and the retro reads the
  number back. Written into the futro skill's reading of this retro, not
  into the skill file (the pixelelated continuation already asks for the
  kickoff receipts).
- **A watch written in a session is a watch with no positive.** The
  `engineering-practices.md` sentence added today says what a window's
  grant must name; #1135 makes the mirror a tool. Until it exists, every
  grant comment names the post contract (`START` or `RETURN` with a UTC
  time in the post's first line) and the coordinator reads the mirror's
  output within a minute of the lane's post.

### Housekeeping items (not blocking the next slice)

- The T1 and T3 lane sessions sit idle on an account whose weekly limit
  resets 2026-10-30 09:00 UTC; whether they move is the owner's (#346).
- T16's disk (`/workspace/tmp/m6-t16/vm-pair/vm-a.qcow2`, sha256
  `27d1a5e5dac3…`) is retained for its revival under #663; released at
  T16's close-out.
- M7's next window (UI and archive qualification) is asked for on the host
  file and granted explicitly; the host is free since T17's RETURN at
  08:06.

### Code-verifiable state

| Slice | Issue | Accepted at | Audit issue | Bugs (open until `next`) |
| --- | --- | --- | --- | --- |
| T11 | #658 | `47672fe4a0` | #1091 closed | #1087 to #1090 |
| T27 | #674 | `78579255e4` | #1096 closed | #1095 |
| T13 | #660 | `a7a5bb94aa` | #1073 closed | #1057 to #1070, #1081, #1092, #1093 |
| T25 | #672 | `68dc79793f` | #1102 closed | none |
| T22 | #669 | `8a4d5eb5b2` | #1103 closed | #1105, #1106, #1107 |
| T28 | #675 | `d6a4e08fda` | #1108 closed | #1109 |
| T29 | #676 | `54f323dc89` | #1121 closed | #1120, #1124, #1125 |
| T16 | #663 | stage C, window to re-grant | -- | -- |
| T17 | #664 | stage E, six streams | -- | six being filed |
| T15 | #662 | close-out, session blocked | #1040 | #1018 to #1039 |

---

**The coordinator's phase continues: T17's hand-back, then T18's brief.**

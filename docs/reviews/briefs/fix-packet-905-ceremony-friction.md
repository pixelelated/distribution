# Fix packet: `ceremony-check` reads every friction entry (#905)

Written by the coordinator on 2026-10-24 at T4's stage-D pause
(D-WORKFLOW-189), in the shape of `fix-packet-887-melonds-toml.md`: one
narrow stream, the files owned, the test first, the `Already written:`
line, one commit cut after the checks are green. **Nothing here builds.**
The packet is a branch on `origin` that merges to `next` in the integration
order beside the other packets (after P0 and P1, with the checksum packets).
The file is the tooling area's (`tools/ceremony-check`, T10's slice #657,
not yet dispatched), which is why it is a packet cut by the T1 session and
not a stream of T4 (#651), whose lane found it. **Review depth: Local**
(plan § 6c: a one-check fix with a fixture): the executor, the fixture, and
the coordinator reading the diff on #905. No guest, no compiler, no `npm`,
no process in an M7 worktree.

## The stream (#905)

- **The defect, from #905's trace:** `tools/ceremony-check:250-252` at
  `8ebaf8daad` skips any line under `## Entries` of `docs/friction-log.md`
  that its regex does not fit, and that is **125 of 445** entries (the T4
  lane's count, `02-forward-audit.md` F-02 on
  `feature/m6-doctrine-rules-651` at `9d67c57ab0`), while
  `.claude/rules/ceremonies.md` says a friction entry without an issue or a
  guard within three days refuses a push of `next`. The guard fails open: an
  ownerless entry in a shape the regex does not read is never owed. Today
  nothing is owed (the two entries with no `issue:` both name a guard), so
  the fix changes no verdict on the live log -- which is what makes it safe
  to make now.
- **Branch and worktree:** cut **from `next` at `8ebaf8daad`**, in its own
  worktree beside the lane's, never in a slice worktree:
  `git -C /workspace/repos/pixelelated/distribution worktree add ../distribution.worktrees/m6-905-ceremony-check-friction -b fix/m6-905-ceremony-check-friction 8ebaf8daad`.
  The coordinator removes the worktree with `tools/fork-worktree remove`
  after the merge. The hooks run from the primary checkout's `.githooks`
  (`core.hooksPath`), so the commit passes the pre-commit scans as every
  commit does.
- **Files owned:** `tools/ceremony-check` (the friction reader at
  `:250-252` and whatever it feeds) and a fixture directory
  `docs/qa-logs/2026-10-24-905-ceremony-friction/` holding the constructed
  log, the two runs' outputs and a `README.md` naming the command. **Not**
  `.claude/rules/ceremonies.md`: its friction row is T4's stream S8, written
  after this packet's diff is on #905. **Not** `docs/friction-log.md`: the
  six prose blocks under `## Entries` (T4's PL-21) are named by the fixed
  check, not moved by this packet.
- **The test first**, every output pasted on #905:
  1. Read `tools/ceremony-check` whole (its `friction` gate, how it finds
     `## Entries`, what it does with a line it cannot parse) before the
     regex is touched; read `docs/friction-log.md`'s shapes: `grep -c -E
     '^- [0-9]{4}-[0-9]{2}-[0-9]{2}' docs/friction-log.md` (every dated
     entry), the lines the current regex accepts (reproduce the tool's own
     count), and the difference, so 445 and 125 are reproduced or corrected
     with the command that produced them.
  2. **The constructed failure, on the unfixed tool:** a copy of the log
     under the fixture directory with one added entry, dated four days
     before today (`date -u -d '4 days ago' +%F`), in a shape the regex
     skips (one of the 125's shapes, chosen from the diff in step 1), with
     no `issue:` and no `guard`; the unfixed `ceremony-check`, pointed at
     the fixture (read how the tool finds the log; if it hardcodes the
     path, run it from a scratch tree whose `docs/friction-log.md` is the
     fixture), prints `ok` for `friction`: the guard seen to fail open.
  3. **After the fix:** the same fixture makes the `friction` line
     `OVERDUE`, naming the added entry; the live log at `8ebaf8daad` (and at
     the coordinator's tip, read with `git -C ... show`) still prints `ok`,
     with the count of entries read equal to the dated-line count less the
     prose blocks' lines, which the check names on its own line (`friction:
     N entries read, M lines under ## Entries are not entries: <line
     numbers>`). `tools/ceremony-check --gate` behaves the same (the push
     guard's call), and `ceremony-check`'s other lines are unchanged
     (compare the full output before and after on the live log: only the
     friction line differs).
  4. `bash -n tools/ceremony-check` (or the interpreter's syntax check it
     uses); the tool's own self-test if it has one (read its header).
- **The change:** the friction reader treats every `- YYYY-MM-DD` line under
  `## Entries` as an entry (the date, then the text, with `issue: #N` or a
  `guard` anywhere in it as the owner), reports lines under `## Entries`
  that are not entries by line number rather than skipping them, and keeps
  the three-day clock and the `OVERDUE` verdict exactly as they are. The
  smallest change that does that; no reshaping of the log.
- **Already written** (#905's, kept in the packet's commit): 125 friction
  entries were never gated and none is ownerless today; nothing on a device
  or in a cloud. The fixed check's first run on the live log changes no
  verdict.
- **Commit**, one, cut after the tests are green, by `git add --
  tools/ceremony-check docs/qa-logs/2026-10-24-905-ceremony-friction`:
  `ceremony-check: read every dated friction entry and name the lines that
  are not entries (#905)`, body: the counts from step 1, the fixture's
  before and after lines, `Refs #905, #912, #651, #657` (no closing keyword:
  the rule's row, #905's third criterion, is T4's S8), the attribution
  line. `git status --short` empty after. Push
  `fix/m6-905-ceremony-check-friction` to origin and post the tip, the diff
  and the outputs on #905; then the session is idle.
- **Ceremonies:** the work-log entry headed `#905` is the coordinator's, as
  for the other packets; the T1 session posts on #905 only; a friction line
  if anything slows -- and that line, under the fixed check, is one the
  check reads.

## After the packet

The coordinator reads the diff and the fixture lines on #905, ticks #905's
first two criteria from them, names the branch in the pointer's merge notes
(beside the checksum packets), tells the T4 lane on #651 that S8 may start,
and posts the row on #657 so T10 reads the tool as fixed when it is
dispatched.

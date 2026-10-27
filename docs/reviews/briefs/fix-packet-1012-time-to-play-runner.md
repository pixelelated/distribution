---
packet: "#1012"
kind: fix packet (a tool; T12's set, #659)
base: f77dc6325e (feature/m6-tooling-vm-harness-659, T12's accepted tip; tools/time-to-play there is the baseline M7 patched)
branch: fix/m6-1012-ttp-runner
worktree: /workspace/repos/pixelelated/distribution.worktrees/m6-1012-ttp-runner
depth: Local (a tool fix with a host-only control; no seat)
version: 1
written: 2026-10-25
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
---

# Fix packet #1012: `tools/time-to-play`'s game-to-game cell sends its answer blind and reads an absent stamp as the product's

**What this is.** The M7 lane reviewed the originals behind #1012 (its
comment of 2026-10-25 03:51 UTC on the issue, quoted there) and prepared a
**runner correction, not a product patch**, as a sealed packet the
coordinator preserved at
`/workspace/tmp/m6-coordinator/pix1012-prebuild-review-20261025-01/`
(fifteen files, `sha256sum -c SHA256SUMS` 15 OK; the seal
`c6d69ff455255693d28c4c9efcd100b263092bb74785e03393ad72372477db14` is the
sha256 of `SHA256SUMS`). Its `time-to-play.baseline` is byte-identical to
`tools/time-to-play` at `f77dc6325e`, T12's accepted tip, so the fix branch
is cut there. **The lane applies M7's patch, runs its control, proves it,
and hands back one commit.** Nothing runs on a guest (no runtime from M6
during M7's grant; the two discriminating guest cases are an open item to
test on #1012, D-QA-051, for the next qualification run).

**The defect, in M7's words (#1012, 03:51):** *"The recorded second
RetroArch appeared at 0.840s, its Nintendo boot frame was captured at
1.014s, and the tool sent its supposed STOP IT AND PLAY answer at 1.357s.
[...] The tool never verified a question before its blind input. [...]
Empty `stamp.raw` means the runner observed no changed stamp; it did not
retain the actual unchanged/absent final read."* So the product behaved as
D-LAUNCH-006 says (a new game takes ownership before the exit sync starts;
its next exit carries both sessions), and the tool (a) pressed its answer
into the running game, (b) called the press *question answered*, and (c)
left no readback of the stamp it judged by. The original run's failure
stays recorded as a failure, not relabelled.

**The fix (M7's `runner-labels.patch`, three hunks in `tools/time-to-play`):**
the answer press is suppressed once the second emulator has been observed
(`marks["ra2"] is None` joins the condition); the field `t_question_answered`
becomes `t_answer_input_sent` and the report's g2g row reads *answer input
sent (dialog not verified)*, with the renderer still reading the old key
from older JSON; `stamp_readback_after` is recorded on every repeat, so an
unchanged or absent final read is retained; the g2g section's title and its
closing sentence stop asserting what the launch did to the sync.

## What the lane does, in order

1. In the worktree (cut by the coordinator from `f77dc6325e`, the pointer
   seeded): `git apply --check` then `git apply` the packet's
   `runner-labels.patch`; `python3 -m py_compile tools/time-to-play`; `diff`
   the result against the packet's `time-to-play.candidate` -- **byte-equal
   is the expectation** (M7 prepared the candidate from the same baseline);
   a difference is explained hunk by hunk, never silently accepted.
2. Run the packet's `controls.py` (host-only; it extracts the answer
   condition and the renderer by AST and runs nine checks with the
   recorded chronology as the old-source failing control): against the
   baseline (the discriminating checks FAIL) and against the candidate (all
   PASS). Record both outputs. `controls.py` is M7's and is not edited; if
   it cannot run as shipped, say why and what was run instead.
3. The tool's own reading of old records: `tools/time-to-play --report` (or
   its render path) over the original `observed-time-to-play.json` from the
   packet must still render (the old key read through the fallback), and
   the original cell must still read as a failure (`headline_missing` or its
   token), never as a pass.
4. `tools/time-to-play --help` rc 0; `bash -n`/`py_compile` as applies;
   `tools/vocabulary-check` over the tool's player-facing strings if it
   reads them (it does not; say so).
5. One commit: `time-to-play: send no answer once the next emulator is seen; name the press an input, not an answer; keep the stamp readback (#1012)`,
   `Refs #1012`, the attribution line; the packet's seal and M7's comment
   cited in the body. Push. Post the hand-back on #1012 with the three
   diffs' byte-equality, the control's two outputs, and the render check.

**Can this be done on the VM?** Yes -- on the host: a patch, a syntax check,
an AST-extracted control over recorded JSON, a render of a recorded file;
no guest. The two guest cases M7 named (an immediate relaunch with capture
ownership then the second game's exit; a visible in-flight-sync question
answered STOP IT AND PLAY with a cancelled outcome) are the open item to
test, run on the next admitted qualification guest, not by this packet.

## Acceptance (the checkboxes on #1012 are these)

- [ ] `fix/m6-1012-ttp-runner` holds one commit over `f77dc6325e` touching `tools/time-to-play` only; `tools/time-to-play` at the tip is byte-equal to the packet's `time-to-play.candidate` (`sha256sum` both: `9d363751dc26f69138d46d74f2a09c78d13d4a7eb0180dfc840d2b2a9ccac77a`), or every differing hunk is explained on #1012.
- [ ] `controls.py` from the packet, run unchanged on the host: the baseline FAILs its discriminating checks and the candidate PASSes all nine; both outputs quoted on #1012 with the command.
- [ ] The renderer reads the original `observed-time-to-play.json` (old key) and the original g2g cell still reads as a failure in the output, quoted.
- [ ] `python3 -m py_compile tools/time-to-play` rc 0; `tools/time-to-play --help` rc 0; `tools/register-check`, `tools/rules-check --quiet` pass on the branch.
- [ ] #1012's open item to test (the two guest cases) is written on the issue with its `open item to test` label, and the original failure record is named as retained.

## What never runs

A guest, a build, a provider call, any edit outside `tools/time-to-play`,
any edit to `controls.py`, a push to any branch but `fix/m6-1012-ttp-runner`,
a write under `/tmp` (use `/workspace/tmp/m6-1012/`), bare `git stash`,
`--no-verify`.

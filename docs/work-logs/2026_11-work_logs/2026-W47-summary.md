# 2026-W47 (November 16–22): M7 packages built on the VM, coordination split into two lanes

Written 2026-11-25 by the OS work coordinator, a day late: the push guard refused a push of `next` until it existed. This is a bounded summary. It draws on:

- the day logs on `next` (November 17, 18, 19 and 22);
- the headings of the OS worktree's day logs for November 16–22, where most of the week's build entries live, uncommitted (#1451);
- the register rows dated in the week;
- the issues the tracker shows opened and closed.

Not every entry was read in full.

## What landed

- **Coordination rules.**
  - **D-WORKFLOW-185:** M7 stabilizes the candidate while M6 assesses in parallel.
  - **D-WORKFLOW-186:** the one-on-one is separate from OS worker traffic (#1436, closed).
  - **D-WORKFLOW-187:** stopped work is escalated to Max without being asked (#1437, closed).
  - **D-WORKFLOW-188:** Max approved the two-owner retention request once.
  - **D-WORKFLOW-189/190/194:** returns become actual next work; decisions are put in terms Max can weigh; the human lane is conversation.
  - **D-WORKFLOW-196:** standing host build and test authority.
  - **D-WORKFLOW-197:** the five execution changes.
  - **D-WORKFLOW-198:** lane models and account handoff (#1438, opened).
- **M7 package work on GENERIC_X64 (#555, #493).**
  - **November 18:** source assembled and the compiler bootstrap started. Assembly 13's failure was kept on record.
  - **November 19:** the EmulationStation French catalog stopped the package build; the corrected checkout built.
  - **November 20:** network, system, font, audio and WebKit-prerequisite batches built, ending with GTK3 on a corrected accessibility stack.
  - **November 21:** emulator cores were checked to load in RetroArch: MAME, melonDS (a normal rebuild fixed a load failure), Mesen, mGBA, PUAE and more.
- **Storage (#493).** D-INFRA-024 automates the read-only storage checks. D-INFRA-025 retires reproducible generated outputs once their successor is verified.

## What was hard

- **The VM backup and autosave tests of November 22** stopped several times before gameplay, and one measured press left the frame unchanged. The records stop there.
- **None of it reached `next`.** The week's coordination rules and tools stayed in the shared worktree, uncommitted or on its feature branch. This was found on November 24 (#1447, #1451).
- **The fork's CI had run nothing since October 29**, all week, and nobody noticed. This was found on November 24 (#1446). The alerts that would have caught it are #1450.
- **No friction line was written all week.** The friction log's next entries are dated November 24. Each hard item above should have had one when it happened.

## Rules, blindspots, issues

- **Rules on `next`:** the register rows above. The lane text in `engineering-practices.md` reached `next` only on November 24 (D-WORKFLOW-201, #1447).
- **Blindspots added:** none. The register's latest entry is 73.
- **Issues:** opened #1435, #1436, #1437 and #1438; closed #1436 and #1437.

## What W48 starts with

- Cleanup batches 1 to 6 (#493).
- The M7 build set from one commit, `0a3e979e50` (D-INFRA-043, #555): SM8550 accepted; GENERIC_X64 building; H700 last.
- CI silence (#1446, #1450).
- Bringing the coordination tools onto `next` (#1451).

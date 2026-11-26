# #1488: the ES tree's host tests, all run and all passing

OS coordinator, 2026-11-26.

**The fault.** Of the ES tree's 15 `tests/*.py`, three had stopped running when the composed M7 source (`409704f3b`) changed the code they read:
- `cloud-oauth-lifetime.py`: #1484, fixed in `b80e59646`.
- `cloud-folder-reopen.py`: a renamed label.
- `launch-capture-gate.py`: doubles from before the managed retirement mode.

The last two are fixed in ES `879ab6ce8`. **The new guard:** `tools/es-syntax-check` now runs every test of the tree a checked file lives in, against that tree's sources, and fails when one fails.

| File | What it shows |
| --- | --- |
| `es-syntax-check-round.out` | On the ES round head, GuiMenu.cpp compiles and all 15 tests pass, rc 0. The whole check took about 26 s. |
| `es-syntax-check-stale-anchor.out` | A detached checkout of `879ab6ce8` with only the hub's folder row renamed. It still compiles and 14 tests pass, but cloud-folder-reopen fails with "the hub has its folder row", rc 1. That is the stale-anchor failure, constructed. |
| `launch-capture-gate-round.out` | All checks pass on `6cdcb7a64`'s FileData.cpp, including three new managed-retirement cases. |
| `launch-capture-gate-planted.out` | A gate that never waits fails 9 checks, rc 1. |
| `launch-capture-gate-old-1272b3405.out` | The test still passes on its own commit's source. |

**One assertion changed meaning, by design.** Since PL-009, a slow capture's gate holds a claim on the exit sync (`sCaptureWaitedOn`), and `launchGame` takes it when the game starts. The gate no longer moves the generation itself. On the current source the test checks the claim; on an older one, the generation.

**Not done here.** The managed-retirement cases check that the launch waits. They do not follow it into `launchGame`, which the doubles do not model.

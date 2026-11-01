# Retrospective: M6.P2 T36, EmulationStation's utilities, resources and renderers (#683)

**The full retrospective runs at stage F**, after the stage-D pause's rulings and the stage-E fixes and their QA. This file records what stages A to C established, so the file exists for the pre-issue lint and a reader has the state; it is not the completed retro.

## What stage C established

- **The forward audit's leads hold, and L-19 is a real new finding.** The four FAIL-at-pin candidates fail on the VM (3.1, 3.2, 3.4, and 3.26 -- the last proving L-19, the deleted path reads present from the cache). The 11 controls/positives pass. `stage-c/build-tests.out`.
- **The independent seat earned its place.** GPT-6 Astra at max confirmed L-19, corrected three positives in `02`, and found a layer the audit missed -- four defects CONFIRMED at the pin (a dangling font-atlas pointer, a stack overflow, a source-destroying copy, a PDF loader that always fails). This is the value of a distinct model over the packet: the audit's own reading did not reach the `Font.cpp`/`TextureData.cpp` lifetime and return-value defects.
- **The guest showed what only the image can:** `HAVE_FRIBIDI` is false, the renderer is virgl, the launch ignores SIGPIPE (so it gets EPIPE, not a signal), the font scales between the two panel sizes, and the menu floats at 1280x800 where it is full-screen at 640x480.

## What was harder than expected

- **The host's toolchain gaps:** rapidjson 1.1.0 does not compile under g++ 15 (so es-unit-tests is not built here; the slice's 3 linked files are proven by T34/T35's runs); the renderers/Font/TextureData need four new fakes the stand-in does not yet carry.
- **The M7 host contention:** M7 cycled standing VMs through the window, and one compile overlapped an M7 START because the gate was printed but not branched on. Fixed (the compile now runs only inside the conditional); friction logged.
- **The guest has no scraped media,** so G-03 (the manual row) and G-04 (the play-time strings) could not be framed exactly; their proofs are the host unit cases.

## What stage D and E inherit

- The ten punch items (three High: G-1, G-7/PL-07, G-16/PL-08), the collisions, the pauses and the two rule errata (`05`).
- The remaining stage-C compile item: the stand-in's four T36 fakes and the renderers positive under `-DUSE_OPENGLES_30`.
- The three held findings, filed as neutral public bugs at stage D.
- The fixes, each proven twice at stage E, with an `Already written:` line.

## Time to play

Nothing in this slice sits on the launch path except `run()` itself (L-05, the pipe wrap) and `getEscapedPath` (the held h3). The audit changes neither at stage C; a fix to either is weighed against the launch at stage E. The two numbers were not measured this slice (no game launched on the guest -- no scraped ROM); they are the integration window's.

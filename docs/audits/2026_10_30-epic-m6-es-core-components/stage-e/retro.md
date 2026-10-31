## Mini Retro: T34 stage E, the streams (#681) -- 10:45 UTC 2026-10-31

**Scope:** S0 to S7, the S2 addendum and the hand-back. ES `16dbac5211` to `52f0ff512` (8 commits, 24 files under `es-core/src/components/` and the French catalog). Distribution: S0 `2568e64dc6` to `7c4a940bdb`, the audit folder only.
**Delta:** `components-tests` went from 7 to 46 cases. `TOTAL: 246 test cases in 6 binaries` at the pin became `TOTAL: 285 test cases in 6 binaries`, with 0 failed test cases in every binary and two `may_fail` (PL-14, PL-40). A fourth sanitizer program was added; all four are at rc 0. Twenty-five bugs are fixed at `fixed-at-es`, and 43 items are at Phase 7.

### What worked well
- **The extractor's refusal.** Each case lifts the tip's lines verbatim and is refused when a range no longer holds its code. It refused three times on lines a stream had moved (`button_pad` and `button_width` twice). Every refusal named the spec to move, and no case ran against lines it was not written for.
- **The case first, the stub against the pin.** The pin's run decided three things the drafted fixes had assumed:
  - PL-13: the pin already re-asks on the next bind, so the fix is the uncached state (ruling 5).
  - PL-43: `:365` sets the full text before any draw, so the item is withdrawn.
  - S1: 2 of 5 FAIL, not the predicted 3 of 4.
- **Scratch trees for other lanes' files.** `Window`'s patch and the holders' were proven on a full copy of `es-core/src` and `es-app/src`, so a quoted `Window.h` could not reach the unpatched one.

### What was harder than expected
- **The build script reported a stale binary.** A refused extraction left the previous run's `components-tests` to run, and the script printed its counts as the new run's. It was caught only because the counts matched the before-run exactly. Fixed: each binary and its run log are removed before compiling (S3, then S7; friction-log line).
- **My own expectations were wrong three times.** 3.14 put the first step at the delay less the speed, 3.27 left out the eleventh row instead of the tenth, and PL-30 asserted the grid's resize. Each was caught on the before-run, corrected before the fix, and said in its `sN-checks.txt`.
- **The holders' half of ruling 1** was first recorded as merge debt only. Writing it as patches showed that a `std::weak_ptr` alias would mean rewriting about 140 call sites. The handle became a forwarding class (the S2 addendum), and the patch shrank to the thirteen lines.
- **Two pushes were refused or denied.** The ES guard refuses a bare-URL push, so pushes go by remote name with an HTTPS push URL (friction-log line). The S1 record was refused once for excess detail and trimmed to the held stream's wording.

### Discoveries that affect future streams and slices
- **`git log -S` disagreed with the brief twice.** PL-01's and PL-03's lines are upstream's, so each gets a #585 line.
- **A template class is reached member by member.** `ImageGridComponent<T>` is lifted into a double one member body at a time, and its instantiations are compiled through three es-app includers. The same shape will do for `IList` and `TextListComponent`.
- **Uninitialised members are tested deterministically** by placement-new over a 0xAB-filled buffer (PL-28), not by hoping the heap is dirty.
- **One note for T36 (#683)** is in the held notes, for the coordinator to pass on.

### Adjustments to remaining work
- **The integration window owes:** Window's and the holders' patches together (`s2-window.patch`, `s2-holders.patch`), `s3-msgbox.patch` when `frame-diff` holds, the coordinator's `es-code-traps.md` paragraph, and each stream's guest half (`02` § The streams).
- **T35 (#682)** inherits `Window`'s ownership patch and the second copy of the button gap.
- **T18 (#665)** inherits the fake header's `handle()`, only if a holder test reaches it.

### Scoped audit findings (Step 2.5)
- **AC conformance: PARTIAL.** Every unit criterion is met at `fixed-at-es`. The guest halves and #1310's second checkbox wait on the integration, as the brief places them.
- **Cornerstone spot-check: PASS.** No change outside `es-core/src/components/**`, the catalog's one entry and the audit folder. `packages/`, `projects/` and `tools/` are unchanged since the dispatch merge `00d490e654`. Non-ASCII on added source lines: none.
- **Interaction-defect scan: PASS.** Four files took more than one stream (`WebImageComponent.cpp`, `ImageComponent.cpp`, `ComponentList.*`, `MenuComponent.cpp`). Each later stream's specs were re-derived from the earlier one's lines, and S3's PL-30 double was completed when S5 changed `setImage(texture)` (D-WORKFLOW-211).
- **Housekeeping: PASS.** The tree's five binaries pass 239 cases at every run: 185, 24, 10, 2 and 18.
- **Harness self-coverage: PASS.** The stale-binary gap found in the harness was closed in the harness.

### Practice adjustments
- **A build script that compiles and then runs** removes what it will run before compiling it. Any lane copying `t34-build-tests.sh` inherits the guard.

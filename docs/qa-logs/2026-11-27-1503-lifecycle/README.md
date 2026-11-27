# #1503: the lifecycle check that failed once without saying why

Packet for [#1503](https://github.com/pixelelated/distribution/issues/1503), 2026-11-27.

- **`run17-lifecycle.log`:** standard run 17 on build 23 (round `5bd8ad6dc0`), 19:03 UTC. Every check passed except `#1467: a later disable commits and restores hardcore once writes are possible (submit rc 0)`. The check named none of its five conditions, and the guest was taken down after the suite.
- **`direct-run-{1,2,3}.log`:** `tools/raofflineproxy-lifecycle-test` run directly on a fresh 640x480 guest of build 23, with a reboot between each, 23:40 to 23:43 UTC. PASSED each time.
- **`constructed-failure.log`:** the edited test (round `428f4661b1`), in a copy that forces the retry's submit rc to 7 (`constructed-test`; the diff is its two lines at the retry), on a fresh guest of build 23. It prints `  why: the submit ended rc 7`, then the FAIL line, then the owner's and the service's state, the flags, the marker, the pointer and the last journal lines. That is criterion 1's constructed failure.
- **Not yet seen: the edited test passing.** In the same session, the edited test refused to run (rc 2), because the constructed run had left a pending owner that needs a reboot, which is the test's own guard. Its pass is the standard run on the next build.

# Proxy consent regression and source qualification

Owners #457/#361; upstream draft #168. Candidate12 remains unchanged.

`consent01-failed/` retains the original installed failure:24 negative/restart
checks recorded no HTTP, then the granted-consent counter assertion failed.
All four result channels1. Actual cleanup00:12:03UTC2026-10-06 confirms owner,
runner, watcher and guest exited. It is not an accepted absence-of-reporting
proof because its positive control failed. Module hashes from the24 completed
cases match candidate12's assembled bytecode (`failed-loaded-bytecode-check.json`).
The failing positive case did not emit a module/result receipt; no such receipt
is invented. Original disk and results tar remain in the raw owner.

Source reproduction identifies a0.0 timestamp sentinel that suppresses the
first config read until system uptime30seconds. Existing consent is unchanged;
opted-in early counters can be lost, never retrospectively reconstructed.
Regression tests fail three assertions before patch019 and all eight consent
tests pass afterward, including grant/decline/regrant and unanswered controls.

Current parent b09d604ecaba7c973028a659b69106b72d3c9514 has219 Linux and53 native
files identical to3036478. Its sole commit changes Android automation/docs.
Both native submodule pins remain identical. Exact archive SHA256:
ff2f67b6620349d7821214c463a56dc9c4d008bba96bdde48b4c77819b9fe427.
All16 fork patches apply with zero fuzz. Schema bytes are unchanged and the
consumer review note names this pin. Package lint and schema guard pass.

`host-b09-01/` rebuilt the native library through the actual package recipe:
818 Linux tests pass, no native skips, plus11 integration checks against each
actual3036478 and historical865e21 predecessor. Sealed inputs pass before/after.
All four channels0 at00:20:30; actual cleanup00:20:53 confirms four owned PIDs
absent. First completion observation00:20:39. No VM or account success follows
from source checks. A fresh fixed image and installed reporting proof are next.

The upstream-only draft is `docs/upstream/raofflineproxy/early-consent/`.
Prepared only; no upstream submission. The new guest tool retains actual
counter/uptime evidence before assertion and can require early-uptime coverage.
No reporting guard or sending function is mocked. Its scope is installed
reporting functions, not scheduler timing, UI or real-account trust.

Full script qualification completed00:34:59/allfour0; observed00:35:14 and
actual owned-process cleanup00:35:42. It used the selected b09 archive/16patches
with candidate12's actual BusyBox/rclone. 1719 individual PASS lines,
0 FAIL/0 SKIP; the cloud-layout block reports316 PASS. This is host source
qualification using prior image applets, not a new image pass.
The two earlier upstream drafts were also rechecked independently against
b09 (image publication1test, platform discovery16tests); each fails on
pristine production code and passes with its standalone fix.

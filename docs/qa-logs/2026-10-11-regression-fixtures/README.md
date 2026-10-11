# Host regression fixes — #550, #551

Original replacement20 scripts qualification ends1 with7failures/0skips. Six
host compiler/patch calls fell back to quota-full /tmp; the seventh tried to
extract the retired AUTOSTARTED block. Original log digest/failure lines are
retained; no original result is rewritten and no firmware defect is inferred.

All host gcc/cc and patch calls now scope TMPDIR to their owned fixture tree.
Guest bubblewrap fixtures still use private /tmp. The main readiness regression
calls the reusable helper against source selected through src_of (including
historical --old). Seven controls execute the unchanged guest query: ready,
delayed, stale boot, failed unit, never-ready, absent answer and empty identity.
They check status and exact poll bounds. Three source mutations removing boot
identity, ignoring unit readiness or asking the wrong unit are rejected.

First watched proof01 ends0 with1378PASS/0FAIL/0SKIP against frozen firmware
source1a02664844 and installed image20 BusyBox/rclone. Ten focused boundary and
mutation controls pass. One retired historical feature group remains explicitly
not applicable and is not counted as PASS. After that owner exited, the helper's
query transport was made CI-portable: fixture-backed cat paths and systemctl
execute the same query without a new bubblewrap dependency in hosted CI.
Final ten controls and full proof02 pass:1378PASS/0FAIL/0SKIP, original owner0
at20:29:42UTC and actual exit. Both hosted checks pass on51ddf40833; delivery01
ends0 at20:29:23UTC. The final-source manifest binds the portable helper.
No device/cloud data, source pin or assembled firmware changed.

The explicit qualification wrapper initially counted the Markdown separator as
another suite and ended1; #552 retains that original. Corrected parsing checks
the exact15 named rows, not a count alone, and refuses failed/missing/duplicate
controls. Fresh acceptance02 ends0 at20:32:14UTC after checking all14 original
nonscript suites, all324 protocol assertions, four reviewed installed frames,
actual guest/endpoint shutdown and frozen source. Original QA20 remains1.
The prepared real19→20 upgrade binds a hash-sealed copy of this composed result;
it does not require or manufacture a successful original QA20 aggregate.

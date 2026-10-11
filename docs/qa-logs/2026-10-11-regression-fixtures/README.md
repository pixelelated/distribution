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
Final ten controls pass; a second full run is ACTIVE to bind the final helper.
Its final-source manifest is retained; do not claim its completion from submission.
No device/cloud data, source pin or assembled firmware changed.

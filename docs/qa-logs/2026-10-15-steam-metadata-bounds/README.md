# Bounded Steam release metadata — #580 / audit #590

The source request now ignores retained curlrc settings and has10s connection,
30s total and1MiB response limits. Existing parsing/error copy and ten-second
failure display are unchanged. Official metadata snapshots are well below the
cap; they are observations, not an all-time size guarantee.

Host01 remains FAIL: normal parses and streamed oversize refusal passed, and
the stalled request returned curl28 at30.01s and shell1 at40.03s. Two unexpected
root-path requests reached the listener, failing the strict request-count check.
Their source is unknown. All original timing/request/status records are retained;
no request-count assertion was waived. The isolated host attempt failed before
payload because user namespace uid_map was unavailable. No second host fixture
ran. An unchanged-helper continuation in the planned no-NIC VM is being prepared.

This source-function evidence does not qualify installed dependency behavior or
native Steam activation. The four-case helper and the14 existing recovery cases
keep their separate exact source bindings. Actual complete runtime remains due.

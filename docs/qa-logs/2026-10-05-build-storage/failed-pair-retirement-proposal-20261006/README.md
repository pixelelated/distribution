# Failed historical QA-pair retirement proposal

Prepared 2026-10-06T23:29:37.087087+00:00; **not approved and not executed**.

Delete only these two standalone, stopped, owner-owned files:

- `/workspace/tmp/pixelelated-m7-p4-no-join-negative-01/pair/vm-a.qcow2`
- `/workspace/tmp/pixelelated-m7-p4-no-join-negative-01/pair/vm-b.qcow2`

Allocated space: 10,713,485,312 bytes (9.98 GiB).
Available before: 341,081,661,440; projected after: 351,795,146,752.
Candidate16 budget stays 347,886,931,968 bytes, including the existing
40GiB package-growth,80GiB QA and100GiB operating allowances. No reserve changes.

The fresh read-only scan inspected 3,486,276 directories and 288 QCOW2 chains
under the same four project-storage roots as the prior cleanup. No discovery,
QEMU or backing-reference errors; no active container mounts reference these files.
No directory symlinks followed; no whole-host root file-descriptor claim.
Actual stopped-pair cleanup and original file SHA256/inode identities retained.

Keep all failed01 logs and source/state/usage evidence (already published),
the successful02 pair, original RC2/1ac images, every candidate/build, shared
sources and all earlier retention stores. These files are from the failed
fixture run, whose correction passed separately in historical02.

Fixed action is `execute.py`, guarded by proposal SHA256 `c00485914a6dec992f46db28e3a5f65fc085bf55e9c263be4c0755351a5f292d`.
It refuses stale dependency evidence, changed identities or any live QEMU;
checks both files before either unlink; records partial execution on any failure.
Prior cleanup approval covered only build worktrees03/05/06/07/08. This separate
two-file retirement requires a new owner yes before running that action.

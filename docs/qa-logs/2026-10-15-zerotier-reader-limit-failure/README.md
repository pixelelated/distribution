# ZeroTier reader01: original limit-contract and cleanup failures

Run `20261015T153108Z-9f9cdb27` failed before either proposed reader child
started. The reused container-owner check still expected 4,294,967,296 bytes
of memory, while the reader plan and actual container requested 1,073,741,824.
The original container result records an empty child list. Neither dependency
verification nor target readelf executed; no reader acceptance follows.

Preserved original outcomes:

| Channel or action | Original result |
| --- | --- |
| Command / monitor / runner | 1 / 0 / 1 |
| Launcher | 1 |
| Docker attach client | 0 |
| Container, from later daemon readback | 1 |
| Watchdog | 1 |
| Parent cleanup and watchdog cleanup | FAIL: container limits differ |
| Forced attach-client stop | true |
| Reader children / readelf children | none |

The attach client's exit0 does not establish container success. Both original
cleanup failures and watchdog1 remain failures. The later investigation found
the exact container stopped, removed that stopped container by its full CID,
and recorded container absence and absence of the recorded process identities.
CID: `cdaed818b56e078b572acdcd0ee132c3697dfccde1f35d037b231340efeda360`.
Those later recovery observations do not rewrite original cleanup receipts.

Admission `8a82b1f0f75d48ef8d5609d54210a7db` was ordinarily consumed as
failed-investigated at 2026-10-15T15:32:46.863657+00:00. Outputs remain held.
The accepted recipe result from compile02 remains separate: recipe0, followed
by its original dependency-reader failure and combined1/0/1, consumed as
`b4f1025d4ecb491088316269b99386f0`. Root's later investigation records that the
original compiled artifact is unchanged; this retention did not rebuild,
execute, replace or delete the original source, objects or binary.

`originals.tar.gz` contains the exact source packet, seal
`29a2554aad756e8f8c313216b333b9fc819cd25b0fc1e59ccabd62f630ff728c`,
the coordinator wrapper receipts, all small reader-owner records, the original
watched run and consumed record, and root's failure investigation, stopped-CID
removal and census receipts. The source packet's SOURCE ONLY / UNRUN labels
remain historical preparation statements; separate run evidence establishes
this later failed attempt. Proposed dependency acceptance remains uncompleted.

The full `failure-review/inspect-before.stdout` was inspected before retention.
Its environment contains only PATH, LANG, LANGUAGE and LC_ALL; its labels are
image version and the named owner/stage. Configured commands and mounts match
the isolated reader, completed-source and frozen-toolchain inputs; no credential
environment or credential mounts are present. The exact original inspection is
retained unchanged, including exited state, exit1, PID0 and OOMKilled=false.
No compiled binary, extracted source tree, toolchain/cache payload, image,
archive body or complete nonfree header is copied into this evidence packet.

`members.json` records every original path, SHA256, byte count, mode, uid/gid
and nanosecond mtime. Retention ran in the actual host context (uid/gid1000,
PID namespace4026531836, user namespace4026531837). Archive verification
compared all retained bytes and metadata with live originals. Historical nested
producer metadata remains unchanged; it is not substituted for host ownership.
`custody-verification.json` records this finite archive readback.

This is evidence retention only. No reader, test, compiler, container, VM,
admission or cleanup was run again. No firmware, device, license, source-bundle
or publication clearance is asserted.

# H700 ARM and AArch64 cache transfers: compact originals

This packet retains the exact transfer02 source packet, both actual owner
records, original coordinator wrappers and command observations, root's exact
assessment helper and produced assessments, original watched transfer runs,
retention/dependency runs, and ordinary consumption receipts. Source seal:
`4e844fda1c085b1a43d2cb6d6c6bbd032219c7c5ba6f583930ae537d74b769a8`.
Historical SOURCE ONLY/UNRUN wording in that packet describes preparation;
the separate original execution records establish the completed transfers.

| ABI | Original run | command/monitor/runner; launcher | Consumed admission | Recorded cache inode |
| --- | --- | --- | --- | --- |
| ARM | 20261015T163646Z-18f35105 | 0/0/0; 0 | 9fe9cbe7416f40d8bb204db7d7adebcc | 148539050 |
| AArch64 | 20261015T163801Z-0bad10ae | 0/0/0; 0 | 9170fa3ad82146a88d189e3b0973081a | 148539056 |

ARM was consumed at 16:37:01.720337 UTC before AArch64's admission; AArch64
was consumed at 16:38:13.985796 UTC on 2026-10-15. Both inner and wrapper
statuses are original zero. The preflight, preparation, retention report,
dependency recording, admission, submission and consumer command receipts
are retained unchanged. Submission and original completion remain distinct.
The four record-only retention/dependency watcher runs also preserve 0/0/0.

Each original result reports a separate same-filesystem rename, no copy,
and matching before/after device `66304` and the inode listed above. The
recorded old target identity remains device `66304`, inode `148419564`.
Cache ownership moved from `m7-pixelelated-h700-04` at
`f8636de1d105275dbf9420bbabbbc26f79abb10f` to
`m7-pixelelated-h700-05` at
`077197e6cd3ea31f33b28aaf3882a694b3423b53`. This retention verifies those
original record relationships; it does not stat, scan or rehash the live caches.
The two renames are not represented as one filesystem transaction.

The original dependency observations were 16:34:21.051224 UTC for ARM and
16:37:29.566666 UTC for AArch64, in host PID namespace `4026531836`.
Each reported zero root matches, container references and active admissions,
63 same-UID processes scanned, and respectively 523/520 other-UID processes
without an FD census. Root's separately recorded assessment includes actual
Docker mount metadata; it does not claim that no containers existed.

All six original PermissionError records remain explicit: `systemd` PID2325,
`(sd-pam)` PID2342, `ssh-agent` PID564119, zombie `exo-open` PIDs2590490 and
2739866, and `sshd-session` PID3133343. Their original start identities,
state, cgroup and failed cwd/root/exe observations are retained. The assessment
scopes the four live protected services out of FD inspection and identifies
the two zombies separately. It is limited to this atomic cache relocation:
there is no whole-host root-FD or deletion clearance. The original observed
timestamps were not refreshed by retention. Named prepared consumers were
resolved by the coordinator's recorded assessment, not by a new census here.

The older combined H700 producer `20261015T060011Z-92b2fe8b` remains
failed-investigated with original **1/0/1**. Its separate accepted DDR3/DDR4,
raw/update artifact proof at `20261015T064734Z-8868082e`, acceptance
`e8107b4bffac81fa72dd127a45ec1b6b7455518829f04c143690ec60687813db`,
remains separately bound. The new GENERIC build and accepted reader02
prerequisites remain separately consumed originals; reader01's failure is not
relabelled. The transfer results make no new GENERIC runtime claim.

This is custody succession only. New H700 compilation, installed-image proof,
physical-device behavior, licence/publication clearance and RC qualification
are not established by these transfer records. Historical capacity figures
remain historical measurements rather than current cache occupancy.

`members.json` maps each retained member to its original absolute path,
SHA256, bytes, mode, uid/gid and exact nanosecond mtime. The archive preserves
those original bytes and PAX metadata. The established compact custody writer
is used with only an explicit three-file list addition for the two standalone
coordinator wrappers and assessment helper; its original identity and exact
diff are retained. No `/tmp` or cache traversal is used by that addition.
Every archive member is verified against its original bytes and metadata.
The independent record readback separately checks source seals, original
statuses/consumption evidence, assessment hashes and recorded inode continuity.
No cache tree, firmware, source payload or large artifact is included or read.
No original was edited, moved or removed; no transfer, process/container census,
preparer, admission, VM, compiler, or shared canonical edit was run for retention.

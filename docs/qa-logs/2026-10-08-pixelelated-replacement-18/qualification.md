# Replacement18 engineering qualification — #508 / #526 / #527

The engineering image passes the applicable standard VM and local protocol
qualification, combining the original unaffected suites with the separately
qualified #527 navigation correction. This is not an RC designation or physical
device acceptance. Source/licence, device and release gates remain.

Firmware source: `7f58b7b1c592908dcd0ba5987955e59aaa79fe66`, ES
`1d76b3da7da75794066df1c089931b890304da7a`. Immutable bundle:
`f557176651026f59bb5931993b12491a6019c0383321fb89fa1a05a596514fe6`.
The build packet binds actual pinned container, source inventory, package output,
installed mappings and identical disk/update SYSTEM. Installed CF10 and the
31-check real candidate16→18 update preserve settings, credentials and file bytes.
#526 is closed after both complete installed-hook runs and 15 BusyBox controls.

## Standard suites and correction

The original [WebDAV/default report](qa21/artifacts/rocknix-images/qa-7f58b7b1c5-webdav-a-20261008-1950/report.md)
retains its rc1. Scripts, lifetime, wrapper, vocabulary, French, quoting,
menu-map, register, pair identity, clean install, WebDAV round trip, emulator
exit and time-to-play passed. All walk commands ran, but two stale folder walks
captured the wrong screens; their screenshot comparison correctly failed.
The original report and all five original failing result channels remain intact.

[#527's evidence](../2026-10-08-cloud-folder-walks/README.md) replaces only those
two walks. Frozen QA source `2e484871bd` passes them at 640×480 and 1280×800
with configuration/mode/path/local/cloud hash preservation and all 16 frames
directly reviewed. Claims `7233b237ee` cover measured intended differences;
neither the baseline nor masks changed. The old wrong-screen control still fails.

The [78-frame aggregate](../2026-10-08-cloud-folder-walks/aggregate/binding.json)
maps 70 unchanged original frames and eight corrected frames to their exact
source/hash. Its [comparison](../2026-10-08-cloud-folder-walks/aggregate/frame-diff.md)
passes with zero unexplained differences or missing frames. This is a composed
qualification with explicit provenance, not a claim that the original whole
run passed or that every suite was rerun under the corrected harness.

## Protocols and observed performance

| Local backend | Assertions | Evidence |
| --- | --- | --- |
| WebDAV | 108 PASS | Original default report above |
| SFTP | 108 PASS | [Report](qa21/artifacts/rocknix-images/qa-7f58b7b1c5-sftp-a-20261008-2019/report.md) |
| MinIO/S3 | 108 PASS | [Report](qa21/artifacts/rocknix-images/qa-7f58b7b1c5-s3-a-20261008-2020/report.md) |

All 324 protocol assertions pass, including provider refusal/recovery and
selected-category seeding/idempotence. Hosted Dropbox is not required by the
standing local baseline. No personal cloud or physical device was accessed.

The standard quick performance sample used virgl on the host Intel renderer:
first game frame 0.69s, next game frame 1.01s, exit-sync stamp 1.46s. These are
single fixture observations, not a statistical performance claim. Offline
achievement and link-loss opt-ins were not rerun here; their prior qualification
and unchanged-input mapping remain distinct from these standard suites.

## Custody and retention

[Completion consumption](qa21/completion-consumption.json) verifies original
results, successful protocols, final frozen-source custody and actual owner exits.
The pair and all three providers stopped and their ports closed. The 180-file
compact packet excludes private keys, provider state and VM disks. Its
[retirement](qa21/retirement.json) removed 4,533,874,688 allocated bytes after
seal verification. #527 separately retired 2,257,588,224 bytes. No test remains
running from either scope, and neither retired launcher should be rerun.

Next: publish/check the exact corrected QA and qualification record, reconcile
#508/#527 and M7, then freeze matched H700 inputs and build/verify H700 before
SM8550. #519 still precedes any owner-device update transfer or reboot.

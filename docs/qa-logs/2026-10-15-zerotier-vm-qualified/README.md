# ZeroTier: accepted isolated fresh and retained VM originals

This packet retains corrected immutable VM source packet03 once, both sanitized
completed exports, original watched runs and ordinary consumption receipts,
root's coordinator wrapper and command observations, and retention-report runs.
Source packet03 seal:
`45965fa05b467d77a14b0375a9b5ee592b24b3d92d14718e04e6d63c3ce60e33`.
Preparation-time SOURCE ONLY/UNRUN wording remains historical; the separate
actual records establish the execution below. The prior failure remains
unchanged under `../2026-10-15-zerotier-vm-failure01/`.

| Scope | Original run | command/monitor/runner; launcher | Consumed admission |
| --- | --- | --- | --- |
| Fresh clean02 | 20261015T165555Z-01fa0035 | 0/0/0; 0 | ba8e501430e642dba2a20a32882cc51b |
| Retained01 | 20261015T165733Z-1a993904 | 0/0/0; 0 | 41b09d12d60f423d98f6188a6538daab |

All seven exporter channels (launcher, tool-wrapper, build, command, monitor,
runner and VM) are original0 in both runs. Fresh was ordinarily consumed at
16:57:06.038852 UTC and retained at17:00:37.276301 UTC on2026-10-15. Root's
prepare, preflight, report, admission, submission, export and consume command
observations all retain their original zero status. The two report watcher
runs also preserve0/0/0; submission is kept distinct from completion.

The source/image binding is
`077197e6cd3ea31f33b28aaf3882a694b3423b53`, with compressed image SHA256
`c5de01b869c5bb28966ab5d654b95a8ed36581c38b380ed885a5946489009932`
and update TAR SHA256
`f2acfc239fd072dddfef08bec8444d149128272ba3d5b5f2ae5d6ff84890b0b6`.
The actual installed ZeroTier executable is bound to SHA256
`dffd15beeaa3be13ea6f5a697b633922ddb7b9566e3130f0b9bf61f5d9cdfb8f`.
Both guests were isolated with no NIC. No image, executable, disk or OVMF body
was opened during this compact retention task.

Fresh: the untouched first-boot check passed with zero blocked checks and zero
errors, and boot-ready was clear before synthetic ZeroTier state was created.
The actual installed service and local CLI passed readiness, version1.16.0,
offline info and empty-network checks. The service restart passed; selected
state and stable ZeroTier state matched, then the daemon stopped with no
remaining identities. The corrected probe explicitly recorded
`network_directory_present: false`, rather than requiring an uncreated empty
directory. One initial readiness return2 is preserved as an accepted starting
state; the original successful CLI operations remain0.

Retained: the original base is the accepted d6a image,
`d6a87f05c1935516115b2cca1af22151a0209224`, updated normally to077197 in a
disposable overlay. It is not described as a direct f863-to077197 rehearsal.
Before and after records show the base unchanged: device66304, inode191671688,
8,631,549,952 bytes, mtime1792017610178716730ns and SHA256
`cfa55b79c36dd6b7fa1186c2e32cacc8b5e253f749f64effb4ec61ff273e488d`.
The guest reboot IDs differ, every selected retained-state comparison passed,
and `changed_selected_paths` is empty. The exact comparison fields remain in
`state-after.json`, including selected bytes/modes, activity stamp, retained
receipts, account-field equality booleans, disabled automatic operations and
removal of the private comparison snapshot. No account values are exported.

The ZeroTier before/after guest phases each reported0 with local CLI version
1.16.0, offline status and zero networks. The pre-update phase created the
private comparison snapshot; the updated phase verified equality before
starting, passed restart and selected/stable-state checks, then removed the
snapshot. Both phases stopped the service with no remaining daemon identities.
The before phase preserves one initial readiness return2; after-phase original
commands are0. Absent `networks.d` was recorded in both phases. These are the
existing selected-state and isolated service/CLI criteria, not a claim about
all possible storage or network configurations.

Both original host closures report no forced cleanup, surviving host process,
remaining child, cleanup error or live QEMU. Exporter OWNERS_GONE observations
are in host PID namespace4026531836. No new process census was performed here.
This accepted scope does not establish an actual network join, external
connectivity, native ARM/physical-device behavior, publication clearance or RC
qualification.

The clean sanitized archive contains79 members totaling397,119 bytes; the
retained archive contains136 members totaling672,463 bytes. All215 nested
members were independently checked for exact membership, byte count and SHA256.
Their original tar metadata is retained unchanged and indexed by the additional
readback. Three fresh and six retained private originals remain only as the
exporter's existing path/byte/hash references. No owner `private/` body or raw
`*zerotier*.stdout`/`.stderr` is included or opened. Guest disks, OVMF, source
image, caches, credentials and identity/token values remain outside this packet.
The exporters' `acceptance_claimed: false` describes their export-only role;
the separate actual qualified ordinary consumption receipts are retained here.

`members.json` maps each outer archive member to the exact supplied original
path, SHA256, bytes, mode, uid/gid and nanosecond mtime. The compact writer
preserves and checks those original source/export/record bytes and metadata.
Nested archives are preserved byte-for-byte rather than reconstructed from
private owners. The independent record readback also checks source seals,
original channels, consumed evidence hashes, private exclusions, guest phase
results, retained-state booleans and recorded base identity equality.
No original was edited, moved or removed. No VM, fixture, test, preparer,
admission, source change, process census or shared canonical edit was run.

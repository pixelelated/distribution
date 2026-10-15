# ZeroTier fresh VM01: preserved fixture failure

This packet retains immutable VM source packet02, its sanitized original
export, original watcher/consumption records, root coordinator wrapper and
command observations, and the retention-report run. Source packet02 seal:
`fb970d76a9ad429ee9fe0b4e4c88181f6b14602193318a3acc6635a516108736`.
Its preparation claims remain historical; this packet records the actual
failed run and does not revise that source or any original outcome.

Run `20261015T165025Z-aed92d8e` ended with original command/monitor/runner
**1/0/1**, launcher1, tool-wrapper1, build1 and VM1. Admission
`5a8da1a9fe9f4c23acd0b5d928801513` was ordinarily consumed as
failed-investigated at 2026-10-15T16:51:56.279473+00:00. Export and root
consume command exits were0; export success does not make the VM run pass.

The untouched first-boot check passed with zero blocked checks and zero errors,
and its boot-ready check was clear. The original guest probe started the
installed ZeroTier service and reached local CLI readiness. Two initial CLI
info returns2 were retained as accepted starting states; the subsequent info,
version1.16.0 and listnetworks commands returned0, with `online: false` and
zero networks. These limited observations precede the failed assertion.

The guest then reported `FAIL` with
`RuntimeError: network-membership-present`. Source packet02's stable snapshot
assertion jointly required `networks.d` to exist as a directory, not be a
symlink, and contain no entries. Root identified the existence requirement as
the fixture defect and assigned a separate source correction. The sanitized
record retains this exact combined error and an empty CLI network list; it
is not supplemented here with a new guest directory observation. Serial
transport returned0 while the guest's explicit reported status was1, and the
host lifecycle correctly retained failure1. Restart, stable-state equality,
retained-storage behavior and overall fresh qualification are not claimed.

Guest cleanup recorded the daemon stopped, no remaining daemon identities,
and no cleanup errors. Host originals recorded normal final sync and VM stop,
no forced cleanup, no surviving host children/processes, and QEMU not live.
The exporter subsequently recorded OWNERS_GONE in host PID namespace
`4026531836`. These are original observations; no new process census or guest
operation was performed during retention.

The source/image binding is
`077197e6cd3ea31f33b28aaf3882a694b3423b53`; compressed image SHA256
`c5de01b869c5bb28966ab5d654b95a8ed36581c38b380ed885a5946489009932`.
The VM used a fresh16GiB disk and `--no-network`, recorded in the originals.
Its isolated local service observations establish no network join, physical
handheld, ARM, publication or release-candidate qualification.

The sanitized export contains79 original members totaling397,415 bytes in
`original-records.tar.gz`; the nested archive SHA256 is
`bfd0095b5051f3d1fdfc3e51fa8ff27e3a614cae239931950d83276f293b56e8`.
Every nested member was independently checked against the exact export
manifest, including membership, sizes and SHA256. Its original tar metadata
is retained unchanged and indexed in the independent readback receipt.
The three private originals remain held only at their original owner paths:
`private/commands-fresh-0.json` and raw `009-zerotier-fresh.stdout`/`.stderr`.
Only the exporter's existing byte-count/hash references are retained. None of
those bodies was opened, copied or archived. No guest identity, token or
account configuration values, VM disks, raw image, SYSTEM, KERNEL or cache
payload is included. The exporter itself explicitly reports no private
settings/account values exported and no acceptance claim.

`members.json` maps outer archive members to their exact supplied original
paths, SHA256, sizes, modes, uid/gid and nanosecond mtimes. The compact writer
preserves and verifies those live source/export/record bytes and metadata;
the nested producer archive is preserved as an exact original file rather
than reconstructed from the private owner. The independent record check
also verifies source seal, original exits, consumed evidence hash, clean and
failed guest status, and the stated sanitized membership exclusions.
No original was modified or removed. No VM, fixture, source correction,
preparer, admission, test, process census or shared canonical edit was run.

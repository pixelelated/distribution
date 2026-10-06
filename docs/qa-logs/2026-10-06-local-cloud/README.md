# Local cloud qualification — replacement14

Refs #462, #133, #351; D-QA-058. The maintainer's full request is in #462.

WebDAV, SFTP and local MinIO/S3 each pass106 round-trip assertions,0 failures,
0 skips:318 assertions total. These are fresh executions on the image's
installed rclone/cloud scripts, including actual uploaded/restored bytes,
content and settings paths, refusal behavior and cleanup. The three reports
retain their different endpoint capabilities. This run covers the standard
round-trip suite; it does not rerun every opt-in interruption/link case.

| Backend | Assertions | Result | Evidence |
| --- | ---: | --- | --- |
| WebDAV | 106 | PASS | [report](webdav/report.md), [log](webdav/round-trip.log) |
| SFTP | 106 | PASS | [report](sftp/report.md), [log](sftp/round-trip.log) |
| MinIO/S3 | 106 | PASS | [report](s3/report.md), [log](s3/round-trip.log) |

Frozen source7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2. Immutable bundle
b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1;
image SHA256c7df6a6f428086f79a377ca1b049f20694f34a868987cf12c493c78eab7b2254.
The sealed input verifier and candidate-store verification pass before and
after qualification. No product bytes changed; no new image build occurred.
`installed-rclone.txt` records the actual installed version/binary hash;
`minio-container.json` retains the exact container image identity without its
credential environment. Local fixtures alone were used.

Owner `/workspace/tmp/pixelelated-m7-cloud-01`, run20261006T055322Z-2568638b,
used the unchanged durable watch-build runner:5second sampling,5minute stall
detection over the actual QA logs, plus active-session supervision. Terminal
result05:58:54UTC; all four result channels0. Actual cleanup05:59:18 verifies
six recorded PIDs absent, no QEMU, no owned MinIO container/backend pidfiles,
and ports9010/9011/9012/9013/10022/10023 unbound. See completion.json and the
launcher receipts. No disconnected notification is claimed (#395).

`harness/` preserves the sealed, run-specific launcher and completion checker;
**never replay this used owner**. Prepare a fresh owner for another candidate,
retain its exact source/bundle seals and run the existing backend-aware
`vm-qa --skip-up --only round-trip --backend <webdav|sftp|s3>` commands under
the standard watcher. Pair/cloud/artifact directories and the MinIO container
name must belong to that owner; verify actual cleanup after terminal status.

## Sign-in criterion reconciliation

`signin-payload-continuity.json` reads replacement14's installed handset chassis
and byte-identical cloud-signin-window/cloud_oauth payloads against replacement10.
The latter's signin-ui14/15/16 retained40 passing checks/15 reviewed frames per
profile. In signin-ui14, build.log41–47 and all-local-navigator.json prove
handset identity and actual HTTP/navigator Mobile Safari. This explicitly reuses
prior runtime evidence for unchanged bytes; no new sign-in frame or
provider-authentication execution is claimed. #351's local criteria are complete;
authenticated Dropbox's trust-page observation is deferred to #463.

## Release scope

D-QA-058 reaffirms D-QA-041: WebDAV/SFTP/MinIO-S3 are the standing local baseline.
Hosted accounts, Dropbox credentials and an offsite endpoint do not gate this
or future routine RC qualification. OAuth/token refresh and provider-owned
pages remain outside these results, explicitly unverified. SMB/FTP remain
broader follow-up under #133/#232.

At this run's checkpoint, the separate RetroAchievements proof awaited the
Tobu softcore reset. The maintainer subsequently confirmed it; the fresh
[ordinary award proof](../2026-10-06-ra-award/README.md) passed33 assertions.
Its queue/send-card UI coverage remains separate. Next: remaining P3 criteria,
approved P4 fixes review, required requalification, then H700 arm/aarch64.
No RC/device-ready claim. #464 reset automation is backlog, not a new gate.

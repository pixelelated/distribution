# Installed Dolphin startup originals — 2026-10-15

The coordinator accepted the three installed startup cases at 01:28:28 UTC and consumed admission `7571f590b4a24d7799b61955447ecb7a`. The original scope is installed Dolphin startup/lifecycle and immutable resource availability on the new GENERIC_X64 image. The frozen source is `d4af5a255f4778a6ecf63ca5b37e05a0f1c83e3a`, branch `build/m7-p5-20261015-01`; lifecycle tooling ran from coordinator `c16285334add6e9ea0dbdb73a7a01aa809922ac8`.

| Case | Original native exit | Init/shutdown count | Loopback requests | CPU tick increase |
| --- | --- | --- | --- | --- |
| Enabled, synthetic 260-byte PowerPC loop | 0 after normal SIGTERM | 1 / 1 | 1 | 204 |
| Disabled, same synthetic loop | 0 after normal SIGTERM | 0 / 0 | 0 | 203 |
| Enabled, absent boot file | 1, expected failed boot | 1 / 1 | 1 | not sampled |

The requests were synthetic invalid login POSTs to guest loopback `127.0.0.1:8080/dorequest.php`; only `lo` was present. This does not establish successful authentication, gameplay, awards, renderer output, saves, an upgrade, or handheld behavior. The actual installed executable hash is `5cb5dacafbcd2227627ef687a65318e61890ef343e5c6553f07c0fb11231fea5`. Six Sys resources match the completed artifact result before and after the cases, through `../../config/dolphin-emu`. All four known badge-load failure strings are absent from each original stderr (12 explicit absence checks). Native exit 1 is preserved as the expected failed-boot result, not rewritten to success.

`original-records.tar.gz` retains every compact owner/export/run original, including the original lossless export archive, both guest manifests, synthetic fixture/configuration, stdout/stderr, per-case/guest/VM results, all 16 host command receipts, lifecycle launcher and both watched-run results, exact source scripts, source/image binding receipts, coordinator review, and consumed admission. The manifest records every original locator, size, hash, mode, ownership, and modification time. All new archive members and the pre-existing export archive/guest manifests were checked by bytes; no runtime operation was repeated.

`coordinator-review.json`, `case-result.json`, `consumption-evidence.json`, and `admission-consumed.json` are byte-exact convenient copies of archived originals. `review.json` is a derived reading aid. The original export's `accepted: false` and analysis's pending-review wording remain unchanged; the later coordinator review and consumed receipt carry the final scoped disposition. Cleanup claims come from their original guest/host/VM receipts, including the actual-host namespace record, not a new retention-time census.

Owned `vm/` disk/media/UEFI payloads are excluded and were not read, copied, deleted, or released here. Every required result channel is present; the export used a watched record-only command and has no separate launcher receipt contract. This packet does not replace build/readback originals or broaden their `runtime_qualified: false` scope. Root controls shared records, admission consumption, issue acceptance, and payload release.

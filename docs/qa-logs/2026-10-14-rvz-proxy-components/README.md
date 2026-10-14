# RVZ, proxy routing and MD5 component qualification — October 14

Completed 03:24 UTC. This is component evidence on accepted GENERIC_X64 VM20,
not a new image, release candidate, native Dolphin gameplay or an owner-device
diagnosis. Production scripts and pins remain unchanged in this record commit.
All test data was synthetic or the recorded public Steam archive; the VM had
no NIC from birth. No owner ROMs, accounts, saves, credentials or cloud were used.

## Results and limits

| Issue | Observed result | Remaining gate |
| --- | --- | --- |
| #583 proxy RVZ reader | Original mismatches all126 unaligned comparisons; candidate mismatches0. Both pass72 aligned controls and6 malformed controls. A real synthetic NONE packed-RVZ record matches the format oracle only after correction. | Independent compiled Dolphin reader parity; native bridge ISO/RVZ hashes, Zstd/crypto dependencies, codec/error coverage and full cache/account/award/reconnect protocol. Padding may lie outside a game's hashed ranges: this does not identify the owner's missing-achievements cause. |
| #583 explicit scanner |44 before/after listing controls pass. Exact all-zero RVZ failure retries only in explicit mode; unrelated indexed roots are not walked. Existing automatic policy, valid unmatched hashes, exclusions, cap/cursor and synthetic pending queue bytes are preserved. | Actual ctl/native hashing and installed-service proof; these are the complete embedded Python listing programs with controlled imports/SQLite, not the full shell/service. |
| #584 Dolphin routing |126 full-script before/after controls pass against actual guest Bash/cat in isolated roots. Exact toggle1/raw-hardcore0 plus IPv4-capable listener selects127.0.0.1:8080; fallbacks preserve customhost and input bytes. No remaining children, signals or observation errors. | Listener presence is not identity/readiness. Installed profile/service, native Dolphin host/login/cache/award/reconnect remain open. No ES UI changed or frame qualification claimed here. |
| #574 MD5 |43 cleanup-recovery controls pass. Ten target commands accepted;264 digest rows each for repaired baseline and candidate match hashlib (528 comparisons). GameCube ISO, Saturn ISO/CUE repeat controls and two Wii helper digests pass; expected truncated input exits2. Sanitizer stderr is empty. | Full formats/CHD, independent DolphinTool, whole Wii images, ARM/big-endian and final frontend/image proof. Current-upstream standalone MD5 contribution is prepared but UNRUN. |
| #582 public Steam archive | Exact110373661-byte SHA, all55 member CRCs and339635561 decoded bytes pass; five mixed-backslash names and three stored symlinks are identified. Required ELF structures are AArch64. No extraction, link creation or payload execution. | Installer repair, existing/self-updated-client recognition, metadata/profile ordering, actual loader/native-client qualification. Structure does not establish runtime readiness or signature authentication. |

Readable original results are in `results/`; all830 guest output files (381472
bytes) are retained in `guest-receipts.tar.gz`, indexed by `guest-members.json`.
The five early result readbacks were compared byte-for-byte to the stopped-disk
export. The archive contains synthetic INIs and logs, not game/media payloads.

## Original failures remain failures

- Proxy original probe1 preloaded no ASCII codec; ElementTree's lazy import hit
  the strict file guard. The additive fixture preloads only encodings.ascii before
  the hook; no extra allowed paths/events or weaker limits. Corrected run0.
- Routing original probe1 assumed the guest kernel exposed task/children. The
  additive fixture uses numeric proc stat PPID/start identities and pidfd-only
  cleanup, with observation errors treated as unknown/failure. Corrected run0;
  cleanup/error injection itself was not exercised.
- One proxy submission refused2 before payload because the VM lifecycle owned
  the coordinator worktree lock. Subsequent serial QA used verified copied tools
  in a separate control root; no lock bypass.
- MD5 compilation's Docker child and all four compile stages exited0, but its
  outer runner/watcher/launcher remain1: exact-container absence parsing expected
  different capitalization. Exact host/container absence readback and8568's
  recovery bind all source/artifact identities without changing that failure.
  The separate target VM run passed. Historical recovery runtime_status=UNRUN is
  intentionally unchanged inside the earlier preparation receipt.
- The public archive's original acquisition remains1 from an optional curl
  metadata key mismatch. Separate hash/recovery and offline inspection pass;
  the original failed receipt alone is refused before decoding. No redownload.

## Sources and contribution destinations

- Proxy original819d1c30 + revised22cfb238: adjacent proxy-rvz-source and
  proxy-rvz-revision-source packets. Executed additive codec fixture is
  `../2026-10-14-proxy-rvz-fixture-correction/`. The padding patch belongs in
  misantronic/RAOfflineProxy; current upstream decoder matches the pin. Linux RVZ
  support#51 is already included. The deliberate-scan exception is currently
  fork-specific distribution integration, preserving D-RA-013.
- Dolphin routing c22554a4 + fixture3a65a2d4: adjacent routing-source and
  routing-census-source packets. A focused ROCKNIX contribution is possible if
  its service/toggle contract matches; this is not a Dolphin decoder defect.
- MD5 candidate314da58d, target source0962c639, recovery8568a71b: source packets
  are retained alongside this one. Minimal current-upstream contributiona58b2313
  is in `../2026-10-14-md5-upstream-source/`: only utils/md5.c, original license
  preserved, public264-row reproducer and local draft PR. Its standalone source
  version has not been compiled/run. Destination is libretro/libretro-common,
  not rcheevos. No upstream report, PR or push was sent.
- Steam contract packet153f0663 is source-only, with25 UNRUN control
  specifications. No installer repair is represented as implemented.

D-WORKFLOW-164 now requires this contribution disposition for every applicable
fix, building on D-WORKFLOW-162 upstream research and earlier proxy decisions.

## Runtime custody and retirement

Single8GiB/4CPU640×480 GL-auto VM, source image SHA
1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490.
Lifecycle03:06:23–03:24:20 finished0 before the03:36 hard stop. Ten original
submission owners consumed; actual host PIDs and QEMU3686526 absent.
Output unmounted successfully before stop/debugfs export. Admission72c06db2 is
consumed. Disks/UEFI/input/output/duplicate staging plus MD5 object/source scratch
retired:2,631,122,944 allocated bytes. No test, compiler, guest or reusable socket
remains from this allocation. `host/retirement.json` records exact paths.

Only nine original target artifacts (~32MB) and one verified public Steam archive
remain for their immediately queued qualification. No completed VM history is
kept. The final closeout console print failed after successful retirement and
admission consumption due to a reused variable; an independent readback verified
consumed state and absence of every retired path. No mutation was replayed.

Next serialized experiment: independently generated DolphinTool/CHD fixtures
(plan1c0e93), then native proxy/hash/cache protocol proof using the actual corrected
reader. Fresh resource admission is required; no command in this packet is an
active allocation. Combined-image/clean/upgrade/audit gates remain separate.

Raw terminal/build outputs containing original trailing spaces are retained as
gzip files, never whitespace-normalized. `compressed-originals.json` maps all26
original paths and byte hashes to their lossless compressed copies.

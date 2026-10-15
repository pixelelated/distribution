# GENERIC_X64 engineering build and artifact originals — 2026-10-15

The three-stage build and assembled-image artifact readback completed with original exit 0 from frozen source `d4af5a255f4778a6ecf63ca5b37e05a0f1c83e3a`. The build/readback portion retains their compact originals. Those results do **not** qualify a booted guest, installed Dolphin startup, gameplay, saves, upgrade behavior, handhelds, or a release candidate. The original artifact result explicitly records `runtime_qualified: false`.

| Record | Original watched run | Completion UTC | Consumption UTC |
| --- | --- | --- | --- |
| Build: clean-dolphin-sa → build-dolphin-sa → image | `20261015T011511Z-8e690173` | 01:19:49 | 01:20:13 |
| Artifact readback | `20261015T012056Z-8c15b02d` | 01:21:11 | 01:24:30 |

The exact image identity is `0.0.1-dev+20261015T011500Z.gd4af5a255f47`; the ES pin is `3178b832b8d134198b2b4eede4f725d4ed283f8c`. [artifact-inputs.json](artifact-inputs.json) retains the actual image/update/source hashes, and [artifact-result.json](artifact-result.json) retains the original GPT, raw/update SYSTEM and KERNEL equality, bootloader configuration, and all 109 selected staged-versus-SYSTEM byte/mode/link-chain rows. The six #592 Dolphin Sys rows match the pinned-source manifest and the exact alias `../../config/dolphin-emu`. This is static artifact equality; it is not an ELF launch or guest runtime claim.

[original-records.tar.gz](original-records.tar.gz) contains 109 original regular files (6,686,545 uncompressed bytes) under `build/owner/`, `build/run/`, `readback/owner/`, `readback/run/`, and `frozen-source/`. Both complete logs are kept for the build, including compiler/linker warnings; successful exits do not establish that warnings are harmless. [original-records.json](original-records.json) gives every member's original absolute locator, size, SHA-256, mode, ownership, and modification time. All archive members were read back and checked against that inventory. Four small original input/result/manifest files are also copied at the packet root; `review.json` names their archive equivalents.

Retained lifecycle originals include launcher submission/start/result, tool wrapper exits, watched command/monitor/runner exits and terminal statuses, run-owned watch-job sources, all three container handshakes and host/inner command results, host/cgroup resource observations, owner/resource results, admission inputs and consumed receipts, and the coordinator's completed-readback/consumption evidence. Every referenced consumption-evidence hash matches a retained original. The frozen watch-build source matches both launcher hashes; the verifier's frozen state reader and selected-path input also match source commit `d4af5a255f4778a6ecf63ca5b37e05a0f1c83e3a`. No original result channel required by either execution contract is missing. Readback uses retained bounded `run.sh` controls and has no separate resource-sampler result contract.

The coordinator's original completed-readback receipts are the cleanup evidence. This retention task did not repeat a host census, compiler, image verifier, VM, service, or provider operation. Original terminal status `alive=yes` fields remain as sampled; later completed-readback receipts record the coordinator's cleanup checks.

Historical preparation fields remain byte-for-byte: readback input `PREPARED_UNRUN`, build planning `admission_prepared: false`, and prior-cache paths in the pinned-source manifest. They describe their original creation phase, not the final outcome or a current dependency. No old-cache path was reopened.

Excluded from the archive: extracted `candidate.img` (4,333,764,608 bytes), `SYSTEM` (2,073,149,440 bytes), and `KERNEL` (47,531,008 bytes), plus all firmware/cache outside the owners. Their recorded identities remain in the originals where provided; this task did not rehash or copy large payloads. No outputs were deleted or released, and corresponding-source custody remains a separate responsibility.

`review.json` is a derived reading aid, not a replacement for original results. `SHA256SUMS` seals every other file in this packet. No runtime acceptance, issue checkbox, admission, git index, or shared record was changed by this retention task.

A separately accepted, bounded installed startup proof is retained in [dolphin-installed/](dolphin-installed/README.md). Its three-case scope is independent of this build/artifact result. `build-readback-original-SHA256SUMS` preserves the initial build/readback seal (SHA-256 `f91fd5ded292f79c1151dbe7c52df5ce41cc2faa1a95488a32236df619a0d3cd`) before this index gained that subpacket; the current recursive `SHA256SUMS` seals the complete directory.

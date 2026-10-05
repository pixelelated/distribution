# Replacement12 build and qualification

Source `55d8ee8f75965a560f75d187e34c9beaa93133f1`; input-manifest SHA256
`bfdcf9b2655157b7e4d3a59f1c6fa803f68989b2cfb8b460eb0f2a666ee98192`.
Only the proxy/CHD recipes and reviewed schema-pin comment differ from
qualified replacement10. ES, splash and container inputs are unchanged.

The build finished at 22:45:46 UTC on 2026-10-05. All 642 tasks and all four
result channels passed. Actual process absence and removal of the observed
container were verified at 22:46:01. Its image, UID and source/cache mounts
were inspected while the build was running. Frozen input and assembled
identity, scripts, proxy configuration, licence payload and renderer checks
passed. This is a successful build, not an RC or a VM qualification claim.

Immutable bundle: `/workspace/artifacts/pixelelated-candidates/sha256/1b3c2c04de5ec6947cfb678279bcc9721167f8409ee825f8d72489838f1c2382`.
Image SHA256: `df753425dffdf567b8865eb9843c190c93d175951187b8d8230013b162dbef55`.
Update SHA256: `12f1734ff030b27edd8675eb2c7d0fbb8d572f936720ec8b97fe14c44fc4d03d`.

Independent cache copy11 completed first, preserving 2,526,406 independent
regular files. Guarded adoption renamed that unbuilt root into12, recorded
same-volume inode custody, and reverified complete checksums against10.
All adoption result channels were zero and all recorded PIDs absent at
22:43:22. No compilation occurred on11; its schema-guard failure is retained.
Full freshness03 on actual frozen12 passed; #362 and #452 are closed with
explicit criterion maps. Earlier freshness and fixture failures remain real.

Image13 completed at 22:47:07 with all four channels zero: the raw flash
image's SYSTEM equals the update SYSTEM, SHA256
`bd1ca70a65e094a7f4725e32f0c5c6deaeb6bd3cdb1a09ca3dc47b5ad1309429`.
Actual cleanup was verified at 22:47:20. Inventory09 completed at 22:46:56,
all four channels zero and actual cleanup at 22:47:21. It maps 583 components,
568 unpacked roots, 525 install stamps and 15 local/meta packages. The exact
new proxy archive and recovered rclone source/binary identity pass. Fourteen
recipe-licence gaps remain; this is not a complete publication source bundle.

QA15 started at 22:47:25 under the standard watcher. Default suites and the
actual September29 ROCKNIX RC2 upgrade are still running. Proxy12 and subset09
remain unstarted. `preparation-native-chd/` preserves the later sealed proxy
harness, which adds installed native-format tests and four legacy CHD v1/v2
cases with metadata bounds, signed integer edges and payload reads. Its host
fixture control passed; no installed result is claimed yet. The original
preparation remains under `preparation/`.

Remaining order: complete QA15 → installed proxy12 → subset09 → ordinary RA
and authenticated Dropbox QA-account proofs → approved independent P4 audit
→ H700 DDR4/RG35XX SP arm, then aarch64 → named physical/P5 gates.
Account inputs remain unanswered. Source09/10 evidence retains its own scope.

The full inputs.json remains sealed at the owner and in the immutable bundle.
The normal credential hook rejects two historical patch filenames in that
mapping as credential-shaped, so Git carries its digest/counts. No hook bypass.

Build-generated documentation observation: frozen12's tracked
`documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`
has a four-row generated update after image construction. This file is outside
the sealed product/QA inputs; the source hashes remain verified. Preserve it
and its retained diff under `generated-documentation/`; do not restore or
merge the build worktree during QA. This is not a clean-worktree claim.

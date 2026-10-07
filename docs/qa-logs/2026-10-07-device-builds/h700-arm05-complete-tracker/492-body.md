## Maintainer request

> You have my approval to do the cleanup, and you have my approval to generate the H700 build. Following the H700 build, we should try the SM8550 build.

## Current state and order

Candidate 16 is qualified on GENERIC_X64: all eight audit findings resolved, 15 VM suites and 318 protocol checks pass. #491 completed the exact approved22-file cleanup and independently verified42.05GiB recovery. Host compiler/proof repairs #495/#496 are completed and published on next63ef759a, with both hosted checks passing. Arm04 later failed at228/244 on a generated-path rename mismatch in box86. #497 repairs six ARM handoff recipes and build_distro with42 passing original/fixed controls and package lint. All failed owners and interrupted scopes remain preserved. Fresh H700 arm05 runs from frozen43d0bc3bf4 with seven sealed inputs and verified actual container/mounts; its separate completion/artifact check is actively watched. H700 arm05 completed at04:50:21UTC and independent acceptance passed at04:50:26UTC; details below. #494 independently preserved and verified14,489objects. Dependency discovery and five immutable-bundle checks completed. Retain replacement12 because two QA overlays still link to its source; replacement09/10/14 offer324.38GiB potential net recovery. A read-only administrator process check is pending before the concrete removal proposal; no further deletion is approved. Build H700 arm compatibility prerequisites, remeasure capacity and build H700 aarch64 firmware, then remeasure capacity and build SM8550. Keep each build in its own frozen build worktree using the standard watcher and active result consumption. No additional deletion, reserve change, release publication or physical-device operation is authorized by this issue.

Can this be done on the VM? Common software qualification is already complete there. Compilation, host capacity, artifact identity and archive inspection are build-host facts. Physical boot, panel and device smoke facts remain separately scoped in docs/releases/device-facts.md and do not gate compilation of the next requested target.

## Acceptance criteria

- [ ] Frozen input manifests show the qualified product-source comparison, distribution/ES pins, actual pinned container digest, source cache and concurrency for each target.
- [x] H700 arm compatibility build has matching terminal result channels, unchanged input seals and verified builder exit; retain its output/stamp manifest.
- [ ] H700 aarch64 firmware build follows a measured capacity pass and has verified terminal results, raw/update identity and hashed DDR3/DDR4 artifacts.
- [ ] SM8550 compilation follows completed H700 artifact verification and a measured capacity pass; retain verified terminal results and hashed image/update artifacts.
- [ ] Artifact inspection records lowercase pixelelated identity, expected qualified source pins and source/licence inventory; release/publication and separately authorized hardware facts remain explicit in the milestone.

Failure logs remain retained. Source repairs discovered by these builds receive their own issues and appropriate requalification; a build failure is not waived. Watcher status alone is not off-session delivery (#395).

After successful build/required qualification, #493 owns the broader review of old build trees, retained images and temporary QA stores, plus a recurring retention plan and the evidence for any drive expansion. That infrastructure follow-up does not replace the authorized H700 then SM8550 order.

## H700 arm acceptance — 2026-10-07 04:50 UTC

All244 tasks complete on43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa. Build owner has four0/seven seals; actual container/owner exited. Independent acceptance verified7,866 files,797 symlinks,938 ARM ELF objects and244 build stamps, including RetroArch/libretro. Acceptance owner four0/two seals/exits verified04:50:50. Output manifest SHA256116314730b3ce22407219f14c1646694ebabc2723a2c24c8ca9e553ff5783e18. Evidence: docs/qa-logs/2026-10-07-device-builds/h700-arm05 and h700-arm05-acceptance. This is compatibility output, not the aarch64 firmware image.

Current: #494 root-only readback and exact cleanup proposal. Post-arm availability173,770,547,200 bytes is below H700 firmware-stage budget287,480,930,304 bytes. The proposed three-tree retirement would fit the next stage, but remains unapproved. The administrator read-only check is pending; no compiler is running and firmware has not been submitted. H700 firmware and actual32-bit handoff evidence precede SM8550 capacity/build, as authorized.

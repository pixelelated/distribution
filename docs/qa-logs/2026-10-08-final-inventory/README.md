# Final engineering-image component inventory

Recorded 2026-10-08T22:17:00.082813+00:00. Refs #492, #344 and #528.

The five profiles below are bound to the accepted immutable VM18, H70002 and SM855003 bundles. This completes the per-image inventory attachment for the firmware-build task. Corresponding-source publication and licence dispositions remain open in #528; no RC or physical-device qualification is inferred.

| Profile | Components | Unpacked roots | Image install stamps | Missing recipe licences |
| --- | ---: | ---: | ---: | ---: |
| vm18-x86_64 | 584 | 569 | 526 | 14 |
| h70002-arm | 224 | 220 | 175 | 1 |
| sm855003-arm | 228 | 224 | 182 | 1 |
| h70002-aarch64 | 615 | 600 | 553 | 16 |
| sm855003-aarch64 | 676 | 659 | 619 | 15 |

These are per-profile counts, with overlap between architectures. Original `components.json` records are retained. `publication-worklist.json` corrects the old helper's inference that no install stamp means build-only: static or vendored inputs still require disposition.

## Evidence and limitations

- Inventory01 rejected unclassified device packages; inventory02 exposed an obsolete install staging assumption; inventory03 rejected installed LLVM with no unpacked root; inventory04 incorrectly equated development staging with shipped files. All four original aggregate results remain rc1 with actual host exits. Successful reports are composed explicitly: VM18/H700 ARM/SM8550 ARM from02, H700 aarch64 from03, SM8550 aarch64 mapping from05 using the exact successful source report from04. Inventory05 and supplement01 have five original rc0 channels and actual owner exits.
- Frozen recipes classify custom-name archives, shared LLVM input, local helpers, U-Boot DDR packaging and ARM handoff. LLVM's source archive matches the exact recipe hash and its three shipped libraries equal the retained package-stage bytes. Its unpacked source is absent; no original unpacked-tree observation or cause of absence is claimed.
- Both rclone1.75.1 prebuilt ZIPs match recipe hashes and actual unpacked binaries. Installed stripping is separate. These prebuilt archives are not corresponding source.
- The idtech recipe downloads an unpinned Doom shareware archive at install time. Its exact staged/image bytes are retained for both devices; upstream provenance/notice disposition remains open.
- Nix archive/toolchain hashes and81 reachable store paths are recorded read-only. Registered NAR hashes are metadata, not independently recomputed NAR proofs. FEX input/source/licence closure remains explicit.
- Seventeen unique recipe-licence gaps remain.47 component/profile rows retain located notice candidates; presence of a notice is not a concluded licence. Recipes' SPDX headers do not automatically license the third-party software they package.
- `supplement-custody.json` binds independent, read-only recovered input copies in the artifact store. Full corresponding-source bundle, independent retrieval and backup custody are not complete.

No firmware bytes, product recipe, device or personal cloud changed. Completed builds and audits must not be repeated to resume this work. #519 remains before the next owner handheld update.

## Continuation

Follow #528 and the live M7 body: assess the17 gaps and special inputs, package corresponding source with exact patches/build scripts, then prove retrieval/backup custody. #265 owns publication tooling and #359 release-note linkage. Only after immediate source dependencies are preserved may #493/#494 retire superseded large caches.

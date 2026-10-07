The authorized H700 arm build (#492) failed at 2026-10-07 04:05:41 UTC in `spirv-tools:host`, selected pin `ef96ed763b43b59b33b31b362f09a02b729fa1c9`. The pinned Docker host GCC12 treats `-Wfree-nonheap-object` in the optimized `getStructMembers`/`hasDecoration` vector code as an error. This is not a disk-capacity or OOM failure. Whether it is a compiler false positive remains to be established.

Owner `/workspace/tmp/pixelelated-m7-h700-arm-01`, run `20261007T035939Z-a3256af0`, frozen tree `c7e3bcd6b5634fc4841488ac724d6f619c994d0f`. All four result channels are 2, all five input seals unchanged, and the four owner PIDs have exited. Preserve the original failure and thread logs before any recovery.

The qualified GENERIC_X64 tree has a target SPIRV-Tools stamp but no host stamp; that qualification did not exercise this host-tool route. The selected SPIRV tools/headers pins are intentionally coupled to glslang16.6.0 (D-WORKFLOW-147/#386); do not arbitrarily advance one of them.

Can this be done on the VM? Yes: compiler behavior and generated tools can be tested on an isolated host/container without hardware. The exact pinned build container and actual compiler invocation are the relevant environment; no handheld action is needed.

## Acceptance criteria

- [x] Retained original failing compiler control, source history and diagnostics establish the cause and show the repaired compile passes without weakening unrelated warnings or changing coupled source pins without evidence.
- [x] The selected package builds under the pinned container, its installed host executables pass representative SPIR-V assembly/validation/disassembly, and package lint passes; retain logs and hashes.
- [x] All interrupted build scopes are enumerated and preserved before recovery; a fresh watched H700 arm run passes the formerly failing package using sealed, committed inputs. Full device-image completion remains #492.

Already written: this attempt produced partial local build output, no firmware image or deployed update. No player storage/cloud state changed. Preserve the failed owner and archive logs before repairing build intermediates.


## Verified completion

Published on next `63ef759ad508d27b0bebc4337a1ed7868cc180c5`, including recipe `f5f815faff4e18808d2c1c0298e4335cc0b20fe7`. [Original-failing and fixed compiler controls](https://github.com/pixelelated/distribution/tree/63ef759ad508d27b0bebc4337a1ed7868cc180c5/docs/qa-logs/2026-10-07-device-builds/spirv-host-control01), [failed state and interrupted-scope preservation](https://github.com/pixelelated/distribution/tree/63ef759ad508d27b0bebc4337a1ed7868cc180c5/docs/qa-logs/2026-10-07-device-builds/h700-arm01-failure), and [installed package / nine shader controls plus independent hash acceptance](https://github.com/pixelelated/distribution/tree/63ef759ad508d27b0bebc4337a1ed7868cc180c5/docs/qa-logs/2026-10-07-device-builds/h700-arm04-start). Upstream6919 matches the GCC12 diagnostic; source pins and target flags remain unchanged. Package lint passes. The actual full package compiled and installed in arm03; that overall owner remains failed on the separate #496 result-writer error. Fresh arm04 passes the unchanged shader stage and continues compatibility compilation. Full H700 arm/image completion remains #492, not a claim of this closure.

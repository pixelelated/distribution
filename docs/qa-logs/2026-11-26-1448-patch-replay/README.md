# #1448 criterion 4: every patch replayed before the build set

`tools/patch-replay` (`next`, `7ee12c6d52`). For one device and arch it runs the build's own `scripts/unpack` for each package with patches, in a scratch `BUILD_DIR`, with the shared source cache. Exit 1 means a patch does not apply; exit 2 means a package could not be checked.

**The constructed failure** (work log 2026-11-26 14:30 UTC). `fex-emu` alone, SM8550 aarch64, trees exported with `git archive`:

| Tree | Result | File |
| --- | --- | --- |
| `ace312b0d2` | exit 1, PATCH-FAIL on `0006-guest-thunks-exclude-rebased-system-headers.patch`: the November 24 build's own failure | `patch-replay-fex-ace312b0d2-RUN.txt` |
| `0a3e979e50` (the fix) | exit 0, 3 patches applied | `patch-replay-fex-0a3e979e50-RUN.txt` |

**The round head, `a069abd236`, for every target of the final build set.** Each run was planned from the last retained build log of its device (`--plan`):

| Target | Packages | Patch applications | Result |
| --- | --- | --- | --- |
| GENERIC_X64 x86_64 | 98 | 275 | every patch applies |
| H700 aarch64 | 112 | 341 | every patch applies |
| H700 arm | 112 | 341 | every patch applies |
| SM8550 aarch64 | 167 | 517 | every patch applies |
| SM8550 arm | 167 | 510 | every patch applies |

**Why H700's two halves match.** Their counts are identical because the arch-specific directories hold the same number of patches. The logs show the arm run applying `pcsx_rearmed-lr/patches/arm/` and the aarch64 run `patches/aarch64/`.

**Run times.**
- The four other targets took minutes.
- SM8550 arm took 45 minutes, almost all of it in `scripts/get`'s host-wide fetch lock while ppsspp-sa's `ffmpeg` submodule and three other git sources cloned into the shared cache. A build would have paid the same fetch.

`tool.sha256` is the retained copy the runner executed, and `tree-head.txt` is the tree it read. `tools/device-build` (#1445) runs the same replay before it submits.

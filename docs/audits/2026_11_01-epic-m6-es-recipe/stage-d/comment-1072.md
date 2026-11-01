**T37 (#684) on this issue: PL-02 of audit #1381** (`docs/audits/2026_11_01-epic-m6-es-recipe/` on `feature/m6-es-recipe-684` at `703470bcca`).

- **What T37 adds:**
  - **The reach on all 15 devices.** The patch reach was computed by `scripts/unpack:127-159`'s rule in a scratch export (`stage-b/reach-15.out`, `stage-b/tables-patches.out`). `emulationstation/patches/x86_64/` is **NOT REACHED on all 15**: `PATCH_ARCH` is `x86` on the two `x86_64` devices and the arch name on the other 13, and the recipe sets no `PKG_PATCH_DIRS`. The theme's `patches/` is reached on all 15.
  - **The candidate's binary.** On the `069fc2704421` guest (G-05), `strings /usr/bin/emulationstation | grep -c 100-amd64-freqfunctions` printed `0`.
  - **A guard.** `tools/t37-checks.sh` step 4 FAILs at `2174265e9c` (`patch-dir-reached patches/x86_64/ (emulationstation): reached for 0 of the listed devices`).
  - **The order.** The independent seat's G-1 confirms this issue's defect 2: the patch's added lines call `get_available_cpu_governors` 4 times and `get_available_gpu_governors` 0 times. Reaching the patch as it stands would put the CPU list in the GPU rows, so any reach lands after T40 corrects the call.
- **The two shapes, for whoever fixes it:**
  - T37's recipe line `[ "${ARCH}" = "x86_64" ] && PKG_PATCH_DIRS+=" x86_64"`. It appends, as the seat's G-2 asked. `config/options:36` sets `TARGET_ARCH="${ARCH}"`, so the test is the unpacker's. A scratch fixture with the line passes `tools/pkgcheck` and the checker.
  - This issue's rename to `patches/x86/` (T40's), which needs no recipe line. The seat preferred the rename.
  - Only one of the two lands; only a build proves the patch applies to the pin.
- **The #585 line:** none owed. The patch is the fork's own (`40fce2a089`, `amd64: wip am64 changes`), not upstream's.

**Severity:** Low · **category:** Install step · **T37 PL-04** · audit #1381

## Code trace

- **How it was found:** the brief's lead L-04 (T37 research, R2 L-04); `tools/t37-checks.sh` at the tip printed `FAIL step 5 no-rm-before-its-directory-is-filled (L-04): at emulationstation/package.mk:79 makeinstall_target (filled at :81)` (`docs/audits/2026_11_01-epic-m6-es-recipe/stage-c/checks-at-tip.out`); the seat confirmed it and corrected the lane's reading of the file's use.
- **The defect at its source (`2174265e9c`):** `projects/ROCKNIX/packages/ui/emulationstation/package.mk:79` runs `rm -f ${INSTALL}/usr/config/emulationstation/resources/logo.png` before `:81` makes `resources/` and `:82` copies the pin's `resources/*` into it, so the line removes nothing and the pin's `logo.png` ships (283,835 bytes on the M7 candidate's guest, G-05). Under `-DROCKNIX` EmulationStation's default splash is `:/pixelelated-wordmark.svg` (the pin's `es-core/src/Splash.h:10-11`); `:/logo.png` is the `else` branch's (`:16-17`), the only reader of the name in the pin's `es-app` and `es-core`, and the shipped theme's XML names no `logo.png` (`0` files). So the image carries a file the line meant to drop and the build never reads. Upstream's order (`c445081a59:52` before `:54`; `651150fc88:53` before `:55`), from `9f1fab30f6`.
- **The fix, located:** pending stage E under the coordinator's stream brief: the `rm` moved after `:82` (so it does what it says); the shipped behaviour is unchanged, and the image is 283,835 bytes smaller.
- **Siblings hunted:** the checker's L-04 assertion over the three recipes' `makeinstall_target` and `post_install` found only `:79`; `:83`'s `rm` of `DroidSansFallbackFull.ttf` follows `:82`, and the theme's `:19` follows its `:16`.
- **What reading cannot prove:** that no other theme a player installs names `:/logo.png`; a theme that did would lose it after the fix (`es-core`'s resource lookup is the integration's read).

**Already written:** every image built from this recipe carries `/usr/config/emulationstation/resources/logo.png` on its read-only system; the next image built from the fix replaces the system and the file goes with it. Nothing is in `/storage`: `post-update:32-35` links only the four `.cfg` files there, and nothing copies `resources/` out of `/usr/config`. Nothing in a cloud.

**Can this be done on the VM?** Yes: the host checker's L-04 assertion (FAIL at `2174265e9c`, PASS at `fixed-at`), then on the GENERIC_X64 guest of the first image built from `fixed-at` an `ls` of the path (the integration's window, `fix-image-pending`).

## Acceptance criteria

- [ ] `tools/t37-checks.sh --tree <export of fixed-at>` prints `PASS step 5 no-rm-before-its-directory-is-filled (L-04)` (at `2174265e9c` it prints FAIL at `:79`).
- [ ] On the GENERIC_X64 guest of the first image built from `fixed-at`, `ls /usr/config/emulationstation/resources/logo.png` reports no such file and `/usr/config/emulationstation/resources/` still lists its other files (the candidate's guest listed `logo.png` at 283,835 bytes).
- [ ] `tools/pkgcheck emulationstation` exits 0 with no FAIL line at `fixed-at`.

fixed-at: (stage E)

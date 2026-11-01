**Severity:** Low · **category:** Build order · **T37 PL-03** · audit #1381

## Code trace

- **How it was found:** the brief's lead L-19 (T37 research, R3 § 2.2 C4); `tools/t37-checks.sh` at the tip printed `FAIL step 5 GENERIC_X64 PKG_NEED_UNPACK-words-are-directories (L-19): unresolved: busybox` and the same for H700 (`docs/audits/2026_11_01-epic-m6-es-recipe/stage-c/checks-at-tip.out`); the independent seat confirmed it with narrowing (a stamp input, not a build-order edge).
- **The defect at its source (`2174265e9c`):** `projects/ROCKNIX/packages/ui/emulationstation/package.mk:14` sets `PKG_NEED_UNPACK="busybox"`. `calculate_stamp` adds the variable's words to its path list as they are (`config/functions:1114`) and hashes `find -L ${stamp}` from the build root (`:1126`), where `busybox` names nothing (`0` files); busybox's recipe lives in `packages/sysutils/busybox` and `projects/ROCKNIX/packages/sysutils/busybox`. So a change to busybox's recipe never moves EmulationStation's stamp. No script reads the variable otherwise (`scripts/`: `0` lines). Upstream's line (`c445081a59:11`, `651150fc88:11`), from `9f1fab30f6`.
- **The fix, located:** pending stage E under the coordinator's stream brief: `PKG_NEED_UNPACK="$(get_pkg_directory busybox)"`, the framework's own form at global scope (the vdr plugins' recipes, `packages/addons/addon-depends/vdr-plugins/*/package.mk:11-12`). The busybox override sources no global recipe, so its one directory is the whole input (the seat's G-4, refuted at stage C). The scratch fixture with this line passes `tools/pkgcheck emulationstation` and the checker (`stage-c/failfirst.out`: `66 of 66`, its stamp moving for `emulationstation` only).
- **Siblings hunted:** `git grep -n -E '^PKG_NEED_UNPACK="[a-z]'` over `packages/` and `projects/` at the tip prints this one line only.
- **What reading cannot prove:** why upstream made ES's stamp depend on busybox (the intent is unrecorded); dropping the line is the alternative if no ES build reads busybox.

**Already written:** nothing inherited -- the line decides which inputs move ES's stamp in a build root; no image, device or cloud holds the stamp, and an image built from the old recipe is byte-identical in what this line touches.

**Can this be done on the VM?** Yes, on the host: the checker's L-19 assertion (FAIL at `2174265e9c`, PASS at `fixed-at`), and the stamp moving with busybox's recipe in a scratch export. No guest row is needed: the stamp never reaches an image.

## Acceptance criteria

- [ ] `tools/t37-checks.sh --tree <export of fixed-at>` prints `PASS step 5 ... PKG_NEED_UNPACK-words-are-directories (L-19)` for both `--devices` entries, `GENERIC_X64:x86_64` and the aarch64 one (at `2174265e9c` it prints FAIL, `stage-c/checks-at-tip.out`).
- [ ] In a scratch export of `fixed-at`, a one-line change to `projects/ROCKNIX/packages/sysutils/busybox/package.mk` moves EmulationStation's `calculate_stamp` for both `--devices` entries, and the checker's step 7 `--compare` prints `moved=0 touched=0` for the theme and `lowerdeck`.
- [ ] `tools/pkgcheck emulationstation` exits 0 with no FAIL line at `fixed-at`, after its `find` positive.

fixed-at: (stage E)

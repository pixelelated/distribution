**Severity:** Low · **category:** Merge debt · **T37 PL-05** · audit #1381

## Code trace

- **How it was found:** the brief's lead L-01 (T37 research, R2 cmds 17-19); the lane's read of the four merges (`docs/audits/2026_11_01-epic-m6-es-recipe/stage-b/l01-merges.out`); the seat confirmed it with narrowing and asked for the device list's source (its G-3), which the lane read at stage C.
- **The defect at its source (`2174265e9c`):** upstream's recipe deletes `armsx2-sa`'s *vulkan driver* feature from `es_features.cfg` except on `SM4450|SM6115|SM8250|SM8550|SM8650` (`651150fc88:projects/ROCKNIX/packages/ui/emulationstation/package.mk:104-108`, from `b9a5d8caf1` 2026-09-24). The fork's merges `a06539d8ec`, `049765fba0`, `fa2990c1e7` (2026-09-29) and `f370dc8787` (2026-10-12) each had an upstream parent holding the two ARMSX2 lines and a result with none; the tip's recipe ends its vulkan step at `:125-128`, which removes vulkan *choices*, not this feature. So the tip's catalogue keeps the feature (`es_features.cfg:1392-1395`: `armsx2 turnip (default)` / `system mesa`; `1` such feature) on every device that ships `armsx2-sa` (`projects/ROCKNIX/packages/virtual/emulators/package.mk:49`, `:55`, `:60`, `:65`, `:72`, `:78`, `:84`, `:89`, `:94`, `:103`). The five devices are exactly where `armsx2-sa` installs its own Turnip (`armsx2-sa/package.mk:25-29`; SM8750 *keeps the system driver*, `:25-26`).
- **The effect, read:** the launcher points the loader at the bundled Turnip only when its ICD file exists (`armsx2-sa/scripts/start_armsx2.sh:215-218`), so on the other devices the row's two choices change nothing: a menu row that misleads, not a broken launch -- hence Low.
- **The fix, located:** pending stage E under the coordinator's stream brief: upstream's five lines restored after `:128` (the fork-own recipe's own lines; moves only ES's stamp).
- **Siblings hunted:** the recipe's other hunks the merges resolved as the fork's are named in `02` § The currency (the ROCKNIX pin, `PKG_PATCH_DIRS+=" ${DEVICE}"` with the RK3566 patch); none is another dropped filter.
- **What reading cannot prove:** that `xmlstarlet`'s delete matches the same nodes in a build as the lane's `xml.etree` count does -- the image built from the fix shows it.

**Already written:** an image built from the tip's recipe carries the feature in `/usr/config/emulationstation/es_features.cfg`; `/storage/.config/emulationstation/es_features.cfg` is a link to that file (`post-update:32-35`), so the next image's catalogue replaces it. A player who chose either value has a `vulkan_driver` setting in `system.cfg` (`start_armsx2.sh:47`); after the fix the row is hidden and the saved value stays, which is harmless: the launcher ignores it wherever the bundled ICD is absent (`:216`), and on the five devices the row stays. Nothing in a cloud.

**Can this be done on the VM?** Yes for the catalogue: a host fixture reproducing upstream's edit in `xml.etree` over a scratch copy of `es_features.cfg` per device (`0` on a device outside the five, `1` on the five), then the same count with `xmlstarlet` in the image built from `fixed-at`. GENERIC_X64 ships no `armsx2-sa` (`virtual/emulators/package.mk:97-100`), so no guest row reads the launcher.

## Acceptance criteria

- [ ] At `fixed-at`, the recipe's ARMSX2 lines reproduced over a scratch copy of `es_features.cfg` count `0` `//core[@name="armsx2-sa"]//feature[@name="vulkan driver"]` nodes with `DEVICE` set outside the recipe's five names and `1` with `DEVICE` set to one of them (at `2174265e9c` both count `1`).
- [ ] The image built from `fixed-at` with `DEVICE` outside the five carries `0` such nodes in `/usr/config/emulationstation/es_features.cfg` (`grep -c 'feature name="vulkan driver"'` within the `armsx2-sa` core block, read from its `SYSTEM` on the host).
- [ ] `tools/pkgcheck emulationstation` exits 0 with no FAIL line at `fixed-at`.

fixed-at: (stage E)

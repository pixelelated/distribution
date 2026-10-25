# Retrospective audit — M6.P2 T25, the devices the fork does not ship and the other projects (#672)

Phase 3 over a reachability table. None of the 397 runs on an image we ship, so the question is not whether they are well written. It is whether the table's verdicts hold where the 397 meet the rest of the tree.

## 3.1 Architectural coherence

- **Three layers, one search path.** `get_pkg_directory` searches `projects/${PROJECT}/devices/${DEVICE}/packages`, then `projects/${PROJECT}/packages`, then `packages/` (`config/functions:789-798`).
  - With `PROJECT=ROCKNIX` on all 27 `Makefile` lines (c06), the nine other projects are never searched. Their 172 unshadowed rows are dead by construction, not by omission.
  - The 9 shadowed rows are shadowed by that same order: the ROCKNIX override is found first.
- **The twelve target directories are ROCKNIX's own device layer,** reached only when `DEVICE` names them. Nine of the twelve are in `world`, and none is in the shipped pair (D-WORKFLOW-185). Their 181 rows plus AMD64's `intel-ucode` pair are what an unshipped build would use, which is why they are `unshipped`, not dead.
- **One recipe reaches across layers by unpack, not by build.** The kernel's `PKG_DEPENDS_UNPACK` and `get_pkg_directory` calls take `intel-ucode` and `generic-dsi` into the kernel without a build step. The plan-derived reach cannot see that (`02` F-01). This is the only place the slice's layers interact by a path the inventory does not model.

## 3.2 Project conformance

- **`packaging-and-patches.md` and `packages/README.md`.** `tools/pkgcheck` passes the 52 recipes with 1 WARN, each argument resolving to exactly its one file (b02). The control fails with rc 1 (b03). The whole tree's baseline is 12 FAIL and 43 WARN, none in the slice (b04).
- **`upgrade-and-install.md`.** One row carries a fork edit, `packages/linux/package.mk`. Its `Already written:` is nothing inherited: the generic recipe built for no target, and the edit's twin in the override is the live one (`02` F-04). Every other row is upstream-carried and untouched since the base, so there is nothing written to answer for.
- **`engineering-practices.md` § Before deleting a duplicate.** Nothing is deleted, but the test was asked of every shadowed pair: does the dead copy guard, stamp or expose something the override does not? The 9 dead copies are never resolved for any target, so none can. Whether the overrides cover what the generic copies did is the overrides' slices' question (T11 for the kernel), not this table's.
- **`device-builds.md` § After rebasing, item 3.** Every field is read as the build reads it. Each target's kernel version is the recipe branch's effective `PKG_VERSION`, not the generic file's. The override sources no generic recipe, so the generic `packages/linux/package.mk` version case is not read for any target.

## 3.3 Spec fidelity

The brief's figures were re-derived at stage A, and every one held. Recorded deltas:
- RPi's whole-word engine count is 2. The brief's third site, `scripts/image:349`, is `Distro_RPi` in a comment.
- The inventory's reach is wrong for four rows (the `intel-ucode` pairs) and incomplete for three (`generic-dsi`'s targets): `02` F-01. The brief's 172 + 32 + 3 = 207 dead rows become 172 + 30 + 1 = 203. The two generic `intel-ucode` rows take D-WORKFLOW-209's *reached after all*, and AMD64's pair `unshipped: target AMD64`.
- The brief's dt-id column has nothing to read here: no unshipped `.dts` carries `rocknix-dt-id`. The column records the absence (`02` § The device trees).

## 3.4 Platform conformance

Not applicable as behaviour: no row runs on a shipped device or the guest, except the generic `intel-ucode` copy F-01 finds in the guest's kernel. T11 read that payload (153 entries) and owns it.

## 3.5 Cross-system interaction audit

### Interaction: the base merge x the 39 drifted paths

- **The shared state** is the tree. `next` is 65 upstream commits behind `651150fc88` on the 397, and 39 of them differ. 38 differ by upstream's hand. The 39th, `packages/linux/package.mk`, differs by the fork's hostname edit, which upstream does not carry.
- **The race.** A merge meets one fork edit: `packages/linux/package.mk:132`. Upstream's copy keeps `"${DISTRONAME}"`, so the merge conflicts or keeps one side. The override at `:160` carries the same fork edit and is T11's. Either outcome of the dead copy builds nothing (F-04).
- **The cost.** Over the twelve target directories with their patches, `226 files changed, 14839 insertions(+), 29156 deletions(-)`, all upstream's. The one seam with a build consequence for these targets is S922X's loader: mainline `v2026.10`, built through `amlogic-boot-fip`'s `build-fip.sh` (`02` § The pins). A merge takes both recipes together; taking one without the other would pair the new u-boot with nothing to build its FIP. Neither is shipped, so the cost of getting it wrong is an unshipped target's build, not a device.

### Interaction: T23's unshipped generic rows x the twelve targets

- **The shared state** is `buildable_by`. The generic-packages area holds 39 unshipped rows (33 under `projects/ROCKNIX/packages/**`, 6 under `packages/**`), each built only by targets in this slice: AMD64 2, RK3326 28, RK3399 8, RK3566 24, RK3576 24, RK3588 39, S922X 11. 4 are built only by the first widening.
- **The interaction.** A disposition for a target here, held or not, is a disposition for those rows there. If a target were ever retired, its generic rows would turn from unshipped to dead. This table proposes no retirement (D-WORKFLOW-185, D-WORKFLOW-209), so nothing moves. The pairing is named so a later decision moves both tables together.
- **The same blind spot.** The plan-derived `buildable_by` that F-01 finds incomplete is the column T23's rows rest on too. Whether any generic row has an unpack-only edge is T23's question, carried as a lead.

### Interaction: T43's and T40's patch rows x the targets and the projects

- **The shared state** is the target directory. The `*.patch` and `linux*.conf` rows under the twelve directories are T43's, and those under the nine projects are T40's. Patch counts per target are in `02` § The targets (3 to 58).
- **The interaction.** A patch row's reach is its target's. So a target `unshipped` here makes its patches unshipped there, and a project dead here makes its patches dead there. The count `02` gives is the bridge, and both slices read the same `Makefile` lines.
- **One overlap worth naming.** Three `.dtsi` in the slice are included by nothing in it (`rk3326-odroid-go2-emmc`, `rk3326-odroid-go2-uart5`, `rk3566-powkiddy-rk2023`). A kernel patch, T43's, may include them, so they are recorded as unincluded in the slice, not as dead.

### Interaction: T11's kernel override x the shadowed generic copy

- **The shared state** is the kernel recipe's name. `projects/ROCKNIX/packages/linux` (T11's) shadows `packages/linux` (4 rows here) for every target, so none of the generic copy's four files reaches an image: the recipe, `sysctl.d/network.conf`, `sysctl.d/qdisc.conf` and `udev.d/40-modeswitch.rules`.
- **The interaction.** The two copies can drift independently. The fork edited both on the same day (`3d7c075f63`, whose comment cites D-WORKFLOW-123). Upstream has not touched the generic copy since the base: its one `M` against `651150fc88` is the fork's two-line hunk, and upstream's head still reads `"${DISTRONAME}"` at both `:132` and the override's `:160`. A reader comparing the two is comparing a live recipe with a dead one.
- **What the override carries that matters here.** The override's x86 block (`:197-207`) is what reaches `intel-ucode` (F-01), and T11 counted its payload. So the dead generic kernel recipe and the live override share one piece of logic, and only the live one's copy runs.

## The futro's predictions, checked

No futro ran for this slice. A table slice is Local and opened on the brief's stranger's proof (version 2), whose figures stage A reproduced. The prediction the brief makes, that no fork-own defect would be found, held (`04` § Q3).

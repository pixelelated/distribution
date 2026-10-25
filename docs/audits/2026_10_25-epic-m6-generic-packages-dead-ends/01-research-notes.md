# Research notes — M6.P2 T23, the generic packages no image builds (#670)

## Scope

- **The read hash:** `8ebaf8daad`. `packages/` and `projects/` are unchanged from it at the dispatch tip, `27b015c901` (`git diff --stat 8ebaf8daad 27b015c901 -- packages projects` is empty); the lane states the same at every stage.
- **`reviewed-at`:** `27b015c901`.
- **The membership:** brief § 2's block, run at P1's `2174265e9c` over `docs/reviews/inventory.json`:

  ```text
  paths 1604 lines 95892 {'upstream-carried': 1601, 'fork-own': 3} {'unreached': 1565, 'unshipped': 39}
  recipes 727 shadowed rows 260
  ```

  The 1,604 are listed in `stage-a/paths.txt`.
- **The units:** each file's nearest ancestor directory holding a `package.mk` in the inventory.
  - **731 units**: 727 whose recipe is in the set, and **4 whose recipe is outside it** (11 files):
    - `packages/addons/addon-depends/chrome-depends/gtk3` (1)
    - `packages/addons/tools/btrfs-progs` (4)
    - `packages/security/openssl` (3)
    - `packages/sysutils/udevil` (3)

    Each of the four recipes is reach `shipped`, because a ROCKNIX override sources it.
  - 0 orphans; 720 distinct basenames (eleven names occur twice).
- **The five plans** (`tools/viewplan`, plan generation only; host, `BUILD_DIR` outside the worktree; then re-run offline through a `curl` shim, byte-identical):

  | Config | `Packages loaded` | Distinct names (host) | The inventory header (container) |
  | --- | ---: | ---: | ---: |
  | GENERIC_X64-x86_64 (`image`) | 1435 | 593 | 593 |
  | H700-aarch64 (`image`) | 1438 | 605 | 611 |
  | H700-arm (`arm`) | 1438 | 235 | 235 |
  | SM8550-aarch64 (`image`) | 1435 | 672 | 672 |
  | SM8550-arm (`arm`) | 1435 | 238 | 238 |

  - The header's `plan_runner` is the pinned container (`sha256:988c0ba5…`, `mode: container`), over 26 configs.
  - **H700-aarch64's six names**, all of them the bootloader chain: `atf`, `h700-suspend-stub`, `pyelftools`, `swig`, `u-boot-DDR3`, `u-boot-DDR4`. On this host `xmlstarlet` is absent and `SUBDEVICES` is read through it with `2>/dev/null`, so it is silently empty.
  - The table therefore counts a name as plan-built when **either** the host plan or the inventory's container plan names it.
- **The fork-own rows:**

  | Row | Disposition at stage A |
  | --- | --- |
  | `packages/tools/installer` | shadowed copy, override live (resolves to `projects/ROCKNIX/packages/tools/installer` on all three devices; plan-built) |
  | `projects/ROCKNIX/packages/graphics/spirv-headers` | reached after all, through `PKG_DEPENDS_UNPACK` |
  | `projects/ROCKNIX/packages/rust/cbindgen` | fork-own, dead |

- **Provenance:** 1,601 upstream-carried rows (the inventory's tier: no fork commit since the base). Upstream has made 0 commits on `packages/` since the base `c445081a59` (against the local `upstream/next` at `651150fc88`, fetched 2026-10-22).

## Phase 1

To be written at stage B: what the dead set is made of, by group.

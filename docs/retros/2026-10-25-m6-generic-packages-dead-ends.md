# Mini Retro: M6.P2 T23, the generic packages no image builds (#670)

**Completed:** 2026-10-25
**Scope of this retro:** the T23 lane at Local depth, covering:
- stage A, the slice's 1,604 rows, read at `8ebaf8daad` (unchanged at the dispatch tip);
- the reachability table of 731 units (`docs/audits/2026_10_25-epic-m6-generic-packages-dead-ends/`);
- the three bugs (#1049, #1050, #1051) and the audit issue #1052;
- the close-out.

There was no stage E: the lane removes nothing and edits no recipe or tool (D-WORKFLOW-209). Not retro'd here: the coordinator's acceptance, the class decision on #346, and the work in #1048, #1049, #1050, #1051 and #1053.

**Commits:** `reviewed-at` `27b015c901` (the dispatch tip), `fixed-at` `ea19c27dee`.

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** These are recipes no image builds, nothing in the tree changed, and nothing ran on a device or a guest.

## What the #346 decision needs from the table

The coordinator carries the class decision to the maintainer. The table gives it:

- **The counts by class** (`04` § Q6): 603 units / 76,809 lines dead and upstream-carried, 447 of them LibreELEC's media centre; 101 shadowed copies (94 with the override live, 7 with it dead too); 21 unshipped; 1 fork-own and dead; 5 reached after all.
- **The cost of each direction** (`04` § Q1):
  - Deleting upstream-carried files means a modify/delete conflict at each merge that touches them. Upstream has made 0 commits on `packages/` since the base, but the media centre arrives through ROCKNIX's LibreELEC merges (the last a Kodi merge, `d43d166b7a`).
  - The cheap direction is small: the five dead files upstream already deleted, and `cbindgen`.
- **The lane's recommendation:** keep the upstream-carried set, drop `cbindgen` and the five files, and fix the inventory's `PKG_DEPENDS_UNPACK` gap (#1049) so the column every later slice reads is true. The decision is the maintainer's.
- **What the decision must not miss:** the five units reached after all are not dead. Removing ROCKNIX `spirv-headers` or the rust snapshots on the inventory's word would break every image's build.

## What worked well

- **Two commands for one quantity, kept apart.** The inventory's `reach` and the lane's own plans, resolutions and closure were computed separately and compared unit by unit. That surfaced five disagreements with a single cause instead of one anecdote (`spirv-headers`).
- **One generator, asserting its counts.** `tools/t23-tables.py` writes the 731-row and 1,604-row tables and the statistics from the same saved inputs, and refuses to run if 1,604, 727 or 731 does not hold. The coordinator's re-run is one command.
- **Proof that a tool did the work.** The `pkgcheck` sweep counted each recipe in the tool's own progress line (727 of 727), not by exit code, and that is how the brief's sweep turned out to have checked nothing.
- **A shim made offline provable.** A logging `curl` on `PATH` proved the parse-time request, made every later plan run network-free, and showed the plans do not depend on it (byte-identical, 5 calls intercepted).

## What was harder than expected

- **The first five plan runs reached the network** under a "no fetch" dispatch, through a dead recipe's global-scope `curl`. Plan generation sources every recipe, so this was invisible until it was looked for. The deviation was named on #670 at the first checkpoint; there is a friction line, and #1051 is filed.
- **The host is not the build container.** `xmlstarlet` is absent, so H700's bootloader chain falls out of a host plan with no error (#1053). The table had to read the container's plan from the inventory where the host could not see.
- **My own slips, each caught before it landed:**
  - a resolver under `set -u` died inside `config/options`;
  - a disposition order first called `installer` *fork-own, dead*;
  - a sibling grep with `[A-Z_]` missed `PKG_SHA256`;
  - two typed times.

## What we discovered

- **The inventory's `reach` misses a whole edge class,** `PKG_DEPENDS_UNPACK`: five live units read dead (#1049).
- **`pkgcheck` passes a run that checked nothing** (#1050).
- **Every plan generation and build makes an HTTPS request** for a recipe no image builds (#1051).
- **Upstream has already removed the ROCKNIX rust stack.** The fork's copies, reached today, leave cleanly at the next merge.
- **The fork once edited a dead copy** (`installer`, `459feac81e`); the question is #1048's.

## Adjustments, Instruction-Recommendations mode

These are proposals for the coordinator.

1. **`device-builds.md` or `generic-x64-vm-testing.md`:** a host plan is not the container's. Compare it with the inventory header before trusting it, and know that without `xmlstarlet` H700's bootloader chain is missing in silence (#1053).
2. **For any plan run meant to be offline:** put a `curl` shim on `PATH` until #1051 is fixed.
3. **For a lint sweep:** count what the tool processed, not only its exit (#1050's shape). This is the "a check that cannot fail is not evidence" rule (`engineering-practices.md` § Guards must fail closed), applied to the sweep's form.
4. **For a reachability table:** compute the `PKG_DEPENDS_UNPACK` closure until #1049 is fixed. Removing a dead unit on the column's word alone would remove a live tarball.

## Scoped audit (the close-out's own checks)

- **The lint:** `PASS` in the pre-issue and resolution phases and with `--issue 1052`.
- **The tables:** coverage 1,604 rows and reachability 731 rows (the `awk` counts); the dispositions sum to 731 units, 1,604 files and 95,892 lines.
- **The review plan** is local, `reviewers: []`, with no provenance file.
- **#1052:** 9 items, each at a Phase 7 outcome naming its issue or commit (#1048, #1049, #1050, #1051, #1053, `0a5676ea5d`). `box-check` 0 fail on #1049, #1050, #1051 and #1052.
- **Nothing changed** under `packages/`, `projects/` or `tools/` from the dispatch tip: no delete or rename, and `packages/`/`projects/` equal `8ebaf8daad`.
- **Stage F:** the plans re-run through the shim are byte-identical to stage A's, and the generator's statistics are identical.
- **The network:** five read-only requests, all in stage A's first plan runs, named in `00`; none since.

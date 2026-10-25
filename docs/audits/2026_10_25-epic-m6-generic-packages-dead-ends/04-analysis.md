# Analysis — M6.P2 T23, the generic packages no image builds (#670)

## Executive summary

The inventory's dead generic set is what it says, with five exceptions and one class decision to make:

- **Rows and units:** 1,604 rows, 95,892 lines, in 731 recipe units. All are read at `8ebaf8daad`, where `packages/` and `projects/` are unchanged at the dispatch tip.
- **Dispositions:**
  - 603 units are dead and upstream-carried, 447 of them LibreELEC's media centre;
  - 101 are shadowed copies of a ROCKNIX override (94 with it live, 7 with it dead too);
  - 21 are unshipped;
  - one is the fork's own and dead (`projects/ROCKNIX/packages/rust/cbindgen`);
  - **five are reached after all.**
- **The five reached after all:** `tools/renovation-inventory` does not follow `PKG_DEPENDS_UNPACK`. So it calls these five `unreached` although every plan unpacks them: ROCKNIX `spirv-headers`, the three ROCKNIX rust snapshots, and generic `binutils-gold`.

The lane removes nothing (D-WORKFLOW-209). It files three `bug`s at stage D:
- the inventory tool's `PKG_DEPENDS_UNPACK` gap;
- `pkgcheck`'s silent pass on an argument that matches no recipe;
- `mesa-reusable:15`'s `curl` at parse time, which makes every plan generation reach the network.

The class decision is the maintainer's (§ Q1).

## Acceptance-criteria scorecard

| # | Criterion | Stage B |
| --- | --- | --- |
| 1 | the folder holds `00` to `05` | `00` to `04`; `05` at stage D |
| 2 | the lint `PASS` | stage C, then close |
| 3 | the local review plan; no provenance file | met |
| 4 | the punch list at Phase 7 outcomes | stage D onward |
| 5 | `reviewed-at`/`fixed-at`; no change under `packages/`, `projects/` or `tools/` | met so far (`00`) |
| 6 | `01` § Scope | met |
| 7 | 1,604 coverage rows | met (the `awk` count prints 1604) |
| 8 | 731 reachability rows; the split; the pairs; the closure; `installer` | met (`02`) |
| 9 | § Disagreements; the tool's `bug` | met; the `bug` at stage D |
| 10 | § The runs | met |
| 11 | `00`'s record, the unshimmed runs named | met |
| 12 | § Q6 sums to 731; § Q1 the paragraph | met (below) |
| 13 | `05`, one item per fork-own row | stage D |
| 14 | `proved:` cells; no `tools/` change | met so far |
| 15 | the retro | stage G |
| 16 | the checkers | at hand-back |

## Risk assessment

- **No product risk.** No image builds these recipes, and nothing here changes.
- **Record risk.** Every later slice's membership reads the inventory's `reach`, which misses the `PKG_DEPENDS_UNPACK` class: the next table built on that column would call a live tarball dead. The `bug` and T10's set carry the fix.
- **Process risk.**
  - Two tools report success while doing nothing: `pkgcheck` with an unmatched argument, and a host plan without `xmlstarlet`.
  - Plan generation reaches the network through one dead recipe.

  All three are silent.

## Coverage boundary

- **Read:** the 1,604 rows' inventory entries; the five shipped and test plans, generated on the host; `get_pkg_directory` for every unit name on three devices; every `PKG_DEPENDS_UNPACK` line at the hash; `pkgcheck` over the 727 recipes; the overrides that source four of the generic recipes; `upstream/next` for the rows that differ there.
- **Not regenerated:** the other 21 configs of the inventory's 26 (their names are read from the header and `reachable_by`, as the brief allows).
- **Not run:** a build, a source fetch, any provider call.
- **The network:** used once by each of the first five plan runs, through `mesa-reusable`'s `curl` (`00`); never again.

## Second opinion

**Depth: Local, by the slice's plan** (`slices.json` k 23, *a reachability table: the counts are the check*; plan § 6c; D-WORKFLOW-184 tier exception). There is no reviewer seat and no provider call, and `second-opinions/` holds only `review-plan.json`. **The lint and the counts are the check:** 1,604 coverage rows, 731 reachability rows, the dispositions summing to 731, the 84/5 split reproduced, and the generator's asserts. Each can be re-run by the coordinator on an export of the tip.

## Finding Verification

| Id | Finding | Severity | Question | Verified by | Verdict | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | `tools/renovation-inventory` does not follow `PKG_DEPENDS_UNPACK`: five units every plan unpacks read `unreached` | Medium | Q3 | `02` § Disagreements: the namers' lines, the plans, the resolutions | confirmed | a `bug` on the tool at stage D (the fix is T10's set) |
| F-02 | `tools/pkgcheck` exits 0 when an argument matches no recipe, so a run that checked nothing reads as clean; the brief's sweep form did exactly that | Medium | Q2 | `tools/pkgcheck packages/addons/tools/jre.zulu` rc 0 and no output; `tools/pkgcheck tools/jre.zulu` rc 1 | confirmed | a `bug` at stage D (D-QA-051 rule 6; upstream's tool; the fix a packet the coordinator routes) |
| F-03 | `packages/graphics/mesa-reusable/package.mk:15` runs `curl` at global scope, so every plan generation (and every build's package scan) makes an HTTPS request | Medium | Q2 | the `pkgjson` worker with a logging `curl` shim; the offline plans byte-identical with 5 calls intercepted | confirmed | a `bug` at stage D; the lane edits no recipe |
| F-04 | a host plan without `xmlstarlet` drops H700's bootloader chain in silence (`SUBDEVICES` read with `2>/dev/null`) | Low | Q3 | `command -v xmlstarlet` empty; `distributions/ROCKNIX/config/functions:224`; the six names | confirmed | a lead for the coordinator (the build engine's, T5's area) |
| F-05 | `projects/ROCKNIX/packages/rust/cbindgen` is the fork's own and dead: named by nothing outside its own directory, not on `upstream/next` | Low | Q6 | `stage-b/cbindgen-grep.txt` (7 lines, all its own); `git cat-file -e upstream/next:...` fails | confirmed | a proposed removal on the punch list, deferred to the coordinator |
| F-06 | `packages/tools/installer` (fork-own, `459feac81e`) is a shadowed copy whose override is live: the fork edited a copy no plan uses | Low | Q7 | resolves to `projects/ROCKNIX/packages/tools/installer` on all three devices; that override is in the GENERIC_X64 plan | confirmed | a punch item: whether the edit belongs on the override, the coordinator's question |
| F-07 | `projects/ROCKNIX/packages/graphics/spirv-headers` (fork-own, D-WORKFLOW-199) is reached after all | Low | Q6 | four plan-built overrides unpack it | confirmed | a punch item: the row leaves this set; F-01 carries the tool's half |
| F-08 | the brief's figures that the run moved: 84/5 (86/3 with the container), *24 named directly* (25, 30 or 18 by method), *nothing is fetched* (false for any plan generation) | -- | Q7 | `02` § The split, `00` | confirmed | recorded; the brief corrected at `0a5676ea5d` |

## Renovation face

### Q1 Modernize

**The decision this slice prepares, for the maintainer on #346.**

What the dead set costs:
- It is **95,892 lines in 1,604 files** that the inventory, `rules-check`, the guards and every later slice carry, and that a reader must learn are dead before reading them.
- 76,809 of those lines are in 603 units that are dead and upstream-carried. 70,675 lines are LibreELEC's media centre (Kodi and its addons), which no ROCKNIX image builds.

What removing them would cost:
- They are upstream's files, and the fork tracks `upstream/next`. Deleting a file upstream still carries makes a modify/delete conflict whenever upstream next touches it.
- Upstream itself has made **0 commits on `packages/` since the base `c445081a59`**. But the media centre reaches this tree through ROCKNIX's merges of LibreELEC, the last of which (`d43d166b7a`, 2026-08-12) was itself a Kodi merge. So the conflicts would come in exactly the part that is most of the set.
- **The cheap direction exists and is small.** Upstream has already deleted 8 of these rows since the base. Three are the ROCKNIX rust snapshots, which every plan still unpacks and which leave with their override at the next merge. The other five files (`strace`, `grub`'s three, `qemu`) are dead here and cost nothing to drop.
- The one fork-own dead unit, `cbindgen`, costs nothing either.

**The lane's recommendation:**
1. Keep the upstream-carried dead set as it is.
2. Let this table be the map that says which recipes are dead and why.
3. Drop only `cbindgen` and the five files upstream already deleted.
4. Fix the inventory's `PKG_DEPENDS_UNPACK` gap, so the column every later slice reads is true.

**The decision is the maintainer's;** nothing is removed here (D-WORKFLOW-209).

### Q2 Standards

`tools/pkgcheck` over the 727 recipes, each confirmed processed: 4 FAIL in 3 recipes and 14 WARN.
- T6's two leads (`jre.zulu:12`, `mesa-reusable:14`) are false positives: each name is set on the line above.
- The two `wireplumber` FAILs are #657's parser false positive.
- No fault in a dead recipe is fixed (D-WORKFLOW-209).

Two standards findings: the tool's silent pass on an unmatched argument (F-02), and a dead recipe that reaches the network at parse time (F-03).

### Q3 Bugs

- F-01: the inventory tool's `PKG_DEPENDS_UNPACK` gap, with a constructed case at stage D.
- F-04: the silent host plan.
- **Not a bug:** the 11 files under the four outside recipes. The inventory marks them `unreached` correctly, because their recipes are used through an override's sourcing and their other files are not.

### Q4 Package currency

None. An unreached pin is not currency. The five units reached after all are handed to T7's or T8's table by the coordinator.

### Q5 Efficiency

None on a device. A plan run loads 1,435 to 1,438 recipes in about a second, while the three image plans build 593, 605 (611 in the container) and 672 names. The cost of the dead set is the reader's and the guards', not the build's: no image builds it.

### Q6 Dead ends

The dispositions by class (sum 731):

| Disposition | Units | Files | Lines | What happens to it |
| --- | ---: | ---: | ---: | --- |
| dead, upstream-carried | 603 | 1,284 | 76,809 | recorded; its removal is one class decision for the maintainer (§ Q1) |
| shadowed copy, override live | 94 | 257 | 17,412 | recorded; the override is T7's or T8's row |
| unshipped | 21 | 39 | 1,013 | recorded; T25's set |
| shadowed copy, override dead too | 7 | 18 | 526 | recorded |
| reached after all | 5 | 5 | 104 | leaves this set; F-01 |
| fork-own, dead | 1 | 1 | 28 | a proposed removal, deferred to the coordinator (F-05) |
| **Total** | **731** | **1,604** | **95,892** | |

### Q7 Clarity and structure

**What `packages/` is for in this fork, read from the table:** it is LibreELEC's tree as ROCKNIX carries it, and most of it is not this fork's product.
- Of the 731 units here, 463 are the media centre.
- 101 are generic copies the ROCKNIX overrides replace. Their live halves are in `projects/ROCKNIX/packages/`, and four of them still source the generic recipe.
- 28 are `projects/ROCKNIX` units no image builds, mostly other SoCs'.

A reader looking for what an image builds should start from a plan (`tools/viewplan`) and the override directory, not from `packages/`. Two of the fork's own rows sit in the wrong half: `installer`'s generic copy, which the fork edited (F-06), and ROCKNIX `spirv-headers`, live while the inventory says dead (F-07).

## Instruction File Recommendations

These are proposals for the coordinator.

1. **`generic-x64-vm-testing.md` or `device-builds.md`:** a plan generated on the host is not the container's. Without `xmlstarlet`, H700's bootloader chain is missing in silence, so compare against the inventory header before trusting a host plan (F-04).
2. **For briefs that say "no network":** plan generation reaches the network through `mesa-reusable` until F-03 is fixed, so put a `curl` shim on `PATH` for any plan run meant to be offline.
3. **For briefs that sweep with `pkgcheck`:** pass the recipe's name or a partial path, and check the tool processed it (its stderr progress line), until F-02 is fixed.

## Quality self-check

- **Every count re-derived by a command and kept:** the 1,604, the 731, the dispositions summing to 731, the 84/5 split on host plans and 86/3 with the container, the 11 pairs, the five reached after all, and the 727 `pkgcheck` runs.
- **Disagreements with the brief, stated with their commands:** H700's 605 against 611; 86/3 against 84/5; 25, 30 or 18 against 24; *nothing is fetched*.
- **A deviation, named:** the five unshimmed plan runs.
- **No file under `packages/`, `projects/` or `tools/` changed:** `git diff --stat 27b015c901 HEAD -- packages projects tools` is empty.

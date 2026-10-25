# Analysis — M6.P2 T40, the patches and kernel configurations no plan applies (#687)

## Executive summary

The inventory's 778 dead patch and configuration rows (317,908 lines) are what it says, with two exceptions and one decision to make.

- **The classes:** 277 are LibreELEC's generic kernel patches, which the ROCKNIX `linux` override never applies. 234 belong to eight projects the Makefile never builds. 234 sit inside T23's dead units and follow T23's dispositions; 6 of those are already deleted at `upstream/next`.
- **The two exceptions, both ROCKNIX's:**
  - **Five `patches/x86_64` files `unpack` never selects.** EmulationStation's `cpugov.patch` would carry a copy-paste slip if it ever applied.
  - **Four generic patches that are not dead.** The ROCKNIX `gcc` and `cmake` overrides symlink their `patches` to the generic directories, so these apply on every image while the inventory reads them unreached.
- **The lane removes nothing** (D-WORKFLOW-209). It files two `bug`s at stage D: class (c), and the inventory's symlink gap.
- **The decision:** the class decision for the 277 and the 234 is the maintainer's, beside T23's on #346.

## Acceptance-criteria scorecard

| # | Criterion | Stage B |
| --- | --- | --- |
| 1 | the folder holds `00` to `05` | `00` to `04`; `05` at stage D |
| 2 | the lint `PASS` | stage C, then close |
| 3 | the local review plan; no provenance file | met |
| 4 | the punch list at outcomes | stage D onward |
| 5 | `reviewed-at`/`fixed-at`; nothing changed | met so far |
| 6 | `01` § Scope | met |
| 7 | 778 coverage rows | met |
| 8 | 778 provenance rows; T23's dispositions on class (d) | met |
| 9 | § The x86_64 five; § The symlinked four; the bugs | met; the bugs at stage D |
| 10 | § The shadowed 74 | met |
| 11 | § The runs | met |
| 12 | `00`'s record | met |
| 13 | § Q6, § Q1, § Q4 | met (below) |
| 14 | `proved:` cells; `question:`; the bugs pass the checker | met so far |
| 15 | the retro | stage G |
| 16 | the checkers | at hand-back |

## Risk assessment

- **No product risk from the dead rows.** No image applies them.
- **A latent risk in class (c).** The day someone renames the `x86_64` directories so they apply, EmulationStation's GPU-governor list on x86 reads the CPU's, and vitaquake2-lr's `@DEVICE@` branch is still never chosen.
- **Record risk.** The inventory misses symlinked `patches` directories. A removal made on its word would delete four patches every image applies (gcc's three, cmake's one).

## Coverage boundary

- **Read:** the 778 rows; each patch's header at `8ebaf8daad`; `get_pkg_directory linux` on five configs; `scripts/unpack`; the Makefile; the symlinked entries; the overrides' patch directories (for the 74); `upstream/next` (for the deletions); the history since June; T23's table from its branch.
- **Not run:** any build, plan generation or network; whether a patch applies to its pinned source (an open item).
- **The 18 confs** are provenance only: no fork base exists to diff against (plan § 2; that is T41's for fork-written configs).

## Second opinion

**Depth: Local, by the slice's plan** (`slices.json` k 40, *a provenance table*; plan § 6c; D-WORKFLOW-184 tier exception). There is no reviewer seat and no provider call, and `second-opinions/` holds only `review-plan.json`. **The lint and the counts are the check:** 778 coverage and provenance rows, the five classes 277 / 234 / 5 / 234 / 28, the generator's asserts, and the runs' outputs, each re-runnable by the coordinator on an export of the tip.

## Finding Verification

| Id | Finding | Severity | Question | Verified by | Verdict | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | five `patches/x86_64` files under live ROCKNIX recipes are never selected (`unpack:127-128` sets `PATCH_ARCH=x86`); vitaquake2-lr's needs a `pre_make_target` x86 branch too; `cpugov.patch` carries a copy-paste slip (the GPU list would call `get_available_cpu_governors`) | Medium | Q3 | `02` § The x86_64 five | confirmed | a `bug` at stage D; the fix is a packet after the maintainer's word |
| F-02 | `tools/renovation-inventory` does not resolve a symlinked `patches` directory, so gcc's three and cmake's one generic patches read `unreached` while every image applies them | Medium | Q3 | `02` § The symlinked four; `selected_patch_dirs:397` and the patch reach at `:461-462` | confirmed | a `bug` at stage D, beside #1049 (the fix is T10's set) |
| F-03 | of the 74 shadowed non-kernel patches, 68 are not strict duplicates. 18 of those the override carries in another form (12 re-offset, 6 with the context moved); 50 have no counterpart | Low | Q4 | the generator's three tests | confirmed | leads for T41's and T42's rows by override |
| F-04 | 14 patches are hand-made diffs with no `From:` or `Subject:`, 12 of them ROCKNIX's | Low | Q2 | `stage-a/headerless.txt` | confirmed | recorded; a patch without a header cannot say what it is for |
| F-05 | the class decision: 277 generic kernel patches, 234 other projects', and class (d)'s 234 following T23's | Low | Q1 | `04` § Q1, § Q6 | -- | to #346 beside T23's, from the coordinator at acceptance; the removal question is #1048's |
| F-06 | the brief's figure that moved: *68 the override builds without* is 50 with no counterpart plus 18 carried in another form | -- | Q7 | `02` § The shadowed 74 | confirmed | recorded |

## Renovation face

### Q1 Modernize

**The class decision, continued from T23's on #346.**

- **What the set is:** besides T23's 603 dead upstream-carried units (76,809 lines), the dead patch set adds:
  - **277 generic kernel patches** (92,389 lines), LibreELEC's own kernel tree, which no ROCKNIX device builds;
  - **234 patches and kernel configurations of eight other projects** (160,488 lines, 125,933 of them in 18 confs), which the Makefile never builds;
  - **234 patches inside T23's dead units**, which follow T23's decision.
- **None has a fork commit.** 102 upstream commits reached them since June, 99 of them LibreELEC's, through ROCKNIX's merges of LibreELEC.
- **What deleting them would cost:** the same modify/delete conflict as T23's set, in the same merges. Patch files churn more than recipes: a LibreELEC kernel or ffmpeg bump rewrites them.
- **The cheap direction:** the six rows upstream has already deleted, which the next base merge settles with no decision.

**The lane's recommendation:**
- keep the 277 and the 234 as they are, as T23 recommended for its set, with this table as the map;
- let the next base merge drop the six;
- rename and fix class (c) through a packet (the bug);
- fix the inventory's symlink gap (the second bug).

**The decision is the maintainer's;** nothing is removed here (D-WORKFLOW-209).

### Q2 Standards

- **The headers:** 746 of 760 patches carry `From:` and `Subject:`; **14 are hand-made** (F-04). Twelve are ROCKNIX's: strace, connman, grub's three, panda3ds-lr, play-lr, vitaquake2's four and `cpugov`.
- **Arch-named patch directories:** across the tree there are 11 `aarch64`, 2 `arm` and 5 `x86_64`, and no `x86`. The class (c) shape, generalised: `x86_64` is the only arch-named directory that `unpack` (which produces `x86`, `aarch64` and `arm`) never selects. All five of them are class (c).

### Q3 Bugs

- F-01, class (c): the trace is in `02` § The x86_64 five. A rename alone would not suffice: vitaquake2-lr's `pre_make_target` names only aarch64, and `cpugov.patch`'s slip must be corrected.
- F-02, the inventory's symlink gap: `02` § The symlinked four.

### Q4 Package currency

**The 68 by override** (`02` § The shadowed 74 has each patch's subject and tier):

| Override | Leads | Of them, carried in another form |
| --- | ---: | ---: |
| `network/bluez` | 8 | 1 |
| `multimedia/ffmpeg` | 7 | 0 |
| `devel/glibc` | 7 | 0 |
| `sysutils/busybox` | 6 | 5 |
| `sysutils/systemd` | 4 | 1 |
| `network/samba` | 3 | 1 |
| `network/openssh` | 3 | 1 |
| `devel/ncurses` | 3 | 3 |
| `wayland/compositor/sway` | 2 | 0 |
| `sysutils/util-linux` | 2 | 0 |
| `audio/pulseaudio` | 2 | 1 |
| `audio/libsndfile` | 2 | 1 |
| 19 overrides with one each | 19 | 4 |
| **Total** | **68** | **18** |

Each is a lead for T41's (the overrides' own patches) or T42's row on that override, and none is a removal. The 50 with no counterpart are LibreELEC changes the ROCKNIX override builds without; whether each matters is a currency question for those slices.

### Q5 Efficiency

None on a device. The reader's cost is 317,908 dead lines beside the live patch set, 125,933 of them in 18 kernel configurations of projects the fork does not build.

### Q6 Dead ends

The dispositions (sum 778):

| Disposition | Rows | Lines |
| --- | ---: | ---: |
| dead: another project's, which no Makefile target builds (b) | 234 | 160,488 |
| dead: a generic kernel patch the ROCKNIX override never applies (a) | 277 | 92,389 |
| inside a T23 dead unit (shadowed copy, override live) (d) | 67 | 48,095 |
| inside a T23 dead unit (dead, upstream-carried) (d) | 152 | 13,916 |
| already deleted at `upstream/next` (d) | 6 | 1,159 |
| dead: an unbuilt recipe's (e2) | 22 | 984 |
| inside a T23 dead unit (shadowed copy, override dead too) (d) | 9 | 625 |
| reached after all (e1, the symlinks) | 4 | 112 |
| never selected: a `patches/x86_64` directory under `PATCH_ARCH=x86` (c) | 5 | 99 |
| dead: a sourced generic recipe's patches, which the live override's globbing never reaches (e1) | 2 | 41 |
| **Total** | **778** | **317,908** |

### Q7 Clarity and structure

**The shape:**
- a LibreELEC kernel patch tree the fork does not use;
- eight projects' patch and configuration trees the fork does not build;
- the patches of the generic twins T23 already mapped;
- five ROCKNIX files named so they are never read;
- four generic patches the fork does use, through a symlink.

A reader asking which patches an image applies should start from `unpack`'s directory list and the package's resolved directory (`get_pkg_directory`), following symlinks, not from `packages/*/patches/`. The inventory's `patches` column is a per-recipe count on `package.mk` rows (`tools/renovation-inventory:587-597`): every patch row's cell is `None` by construction, so the count lives on the recipe's row.

## Instruction File Recommendations

These are proposals for the coordinator.

1. **`packaging-and-patches.md`:** an x86_64 patch directory is named `patches/x86`, since `unpack` sets `PATCH_ARCH=x86`. A `patches/x86_64` directory is never read (F-01).
2. **For reachability work:** follow symlinked `patches` directories. An override may apply a generic recipe's patches through a link (F-02).
3. **For a "duplicate" claim about two patches,** name the test: byte-equal, hunk headers aside, or changed lines only. They give 2, 14 and 20 here (F-06).

## Quality self-check

- **Every count re-derived by a command and kept:** the 778, the five classes, the (e) split, the headers, the six deletions, the 102 commits and their split, the shadowed tiers, and T23's 731.
- **A delta from the brief, stated with its test:** *68 builds without* is 50 plus 18.
- **No `.patch`, `.conf`, recipe or tool changed; no network.**

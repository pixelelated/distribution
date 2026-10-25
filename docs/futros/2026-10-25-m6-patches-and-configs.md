# Futro: the patches and kernel configurations area epic (#1054), at T40's kickoff (#687)

**Prepared:** 2026-10-25, by the M6 coordinator lane (D-WORKFLOW-189),
before T40's dispatch to the T5 session; the area's four slices are T40
(the patches no plan applies), T41 (the shipped and test images' kernel
patches and configurations), T42 (their other patches) and T43 (the
unshipped devices' patches), all Local tables. The inputs: plan § 2, § 4
to § 6 and § 8, order § T40 to § T43 at `2174265e9c`, the inventory's 778
unreached rows, `scripts/unpack` and `config/functions` at `8ebaf8daad`,
T23's accepted dispositions (`feature/m6-packages-dead-ends-670`,
`02-forward-audit.md` § Reachability), D-WORKFLOW-209, and a read-only
research pass over the 778 whose notes carry every figure's command.

## 1. What do we know and what are we assuming?

**The plan, in the order's words:** T40 is *patches and kernel
configurations no plan applies*, lens reachability, Local: 778 paths,
317,908 lines -- *the 277 generic kernel patches the ROCKNIX `linux`
override never applies, `vitaquake2-lr`'s and EmulationStation's
`patches/x86_64` (which `PATCH_ARCH=x86` never selects), the other projects'
patches. Rows are generated from `inventory.json` and the patch headers
(`From:`, `Subject:`); the session decides origin and removal.*
D-WORKFLOW-209 (2026-10-25, T23) narrows the last clause: a dead-end table
records a disposition per unit and removes nothing; the removal of
upstream-carried dead code is one class decision for the maintainer.

**778 rows, 317,908 lines: 760 `.patch` and 18 `linux*.conf`, every row
`vendor-carried` with no fork commit ever** (`last_fork_commit` none on all
778; 0 fork-authored commits since the base; 102 upstream commits reach them
since 2026-06-01, all through ROCKNIX's merges of LibreELEC). The research
pass sorted them into five classes, first match in order, summing to 778
and 317,908: (a) 277 generic kernel patches under `packages/linux/patches/`
(rockchip 187, rockchip-old 48, dvb 39, default 3), every device resolving
`linux` to `projects/ROCKNIX/packages/linux`, which neither sources the
generic recipe nor shares a patch with it; (b) 234 under eight other
projects (216 patches and the 18 confs; the Makefile sets `PROJECT=ROCKNIX`
in all 27 of its build lines); (c) 5 under a `patches/x86_64` directory of a
live recipe (vitaquake2-lr's four `001-set-platform.patch`, EmulationStation's
`cpugov.patch`), which `scripts/unpack` never selects because it sets
`PATCH_ARCH=x86` on x86_64 (lines 127-128); (d) 234 inside 117 of T23's dead
units (158 rows in *dead, upstream-carried* units, 67 in *shadowed copy,
override live*, 9 in *shadowed copy, override dead too*; none in T23's five
*reached after all*); (e) 28 others -- 7 in generic recipes a live override
sources (gcc 3, cmake, readline, fluidsynth: the override's own `patches/`
is globbed, the sourced recipe's is not), 17 in LibreELEC `packages/emulation/`
recipes no plan builds (T24's area), 4 under driver and firmware recipes.

**Assumptions the plan leans on and does not state:**

- *That "the session decides removal" still holds.* It does not:
  D-WORKFLOW-209 makes it a disposition table, and every one of the 778 is
  upstream's; the class decision is on #346 already (T23's), and these rows
  follow it.
- *That the headers carry the provenance.* They do for 746 of 760 (`From
  <40-hex>`, `From:`, `Date:`, `Subject:`; 485 `Signed-off-by:`, 97 `Link:`
  or review trailers); the 14 header-less files are ROCKNIX's hand-made
  diffs and the only hand rows.
- *That a dead patch is never a bug.* Class (c) is one: vitaquake2-lr's
  `x86_64` patch is a real x86 variant (one hunk of four lines differs from the `aarch64` one -- corrected by the proof) that has never applied since 2025-07-13, and EmulationStation's
  `cpugov.patch` targets a file the ROCKNIX `rocknix` package installs and
  carries a copy-paste slip that has never compiled. A `patches/x86`
  directory would make both apply -- a recipe-tree edit the lane never
  makes (D-WORKFLOW-209; a packet after the maintainer's word).
- *That the 74 shadowed rows are duplicates of the override's patches.*
  Only 2 are, by content (kmod's `fix-pkgconf`, systemd's
  `remove-nonexistant-dependency`); the other 72 are LibreELEC changes the
  live ROCKNIX override builds without -- a currency question for T41's and
  T42's rows on the overrides, not T40's removal.
- *That the 18 confs have a base to diff against.* They do not: they are
  LibreELEC's own, 16 of them 6,600 to 8,600 lines and current upstream to
  2026-08-05, two of them nine-byte `# dummy` placeholders; plan § 2's "one
  diff per kernel config against its base" is for fork-written configs
  (T41's). The row is provenance only.
- *That the inventory's `patches` column counts patches on patch rows.* It
  is a per-recipe count on `package.mk` rows; every patch row's cell is
  `None` by construction.

**Substrate preconditions, and how each was verified:** the classes derive
from `config/options ""` and `get_pkg_directory` (no network: the research
pass's `curl` shim was never invoked), `scripts/unpack`'s patch selection,
the Makefile's `PROJECT=` lines, and T23's accepted table on its branch;
no plan generation, no build, no guest. Six rows are already deleted at
`upstream/next` (strace's two, grub's four), none in `next` yet.

**Build-vs-adopt:** not applicable. **Base divergence:** the coordinator's
branch ends at D-WORKFLOW-209; T23's branch holds the join target; the 778
are unchanged across `8ebaf8daad`, `2174265e9c` and the coordinator's tip.

## 2. What known unknowns need investigation?

1. Whether any of the 277 generic kernel patches has a subject match in the
   ROCKNIX kernel's own 427 live patches (the research pass found 0 of 277
   by subject; the table confirms by header and names any near match).
2. What each of the 72 non-duplicate shadowed patches changes, and whether
   the live override builds the same fix under different code -- the
   table points at the override's row for T41/T42; it does not answer.
3. Whether the five class-(c) patches apply cleanly to their recipes' pinned
   sources today (a `git apply --check` against the unpacked source is a
   build step; the table records the directory-name fact and the code
   trace, and the bug names the check for the next image).
4. The series position and target of each `git format-patch` row (the
   generator reads `diff --git a/` and the `[PATCH n/m]` subject).

## 3. What patterns from prior work apply that we haven't named?

T23's table and generator (one row per unit, counts asserted, dispositions
by class; its decision issue #1048 and its class question on #346); T45's
rule that a column is a claim and the second command the evidence; T23's
finding that plan generation reads the network through one recipe (not
needed here: no plan is generated); the T23 brief's own proof corrections
(a count made with the wrong unit grouping, twice) -- T40's unit is the
patch file, and its classes come from one script over the saved rows.

## 4. What could we be missing?

**Agent-execution simulation, a fresh lane with the brief:** it reads *the
session decides origin and removal* in the order and `git rm`s 277 kernel
patches: the brief forbids every edit to a `.patch` or `.conf` and § 7
checks the diff empty. It renames `patches/x86_64` to `patches/x86` to
"fix" class (c): forbidden; a bug with the trace, the rename a packet after
#346. It runs a package build to see whether a patch applies: no build;
the open item names it for the next image. It diffs the 18 confs against a
base that does not exist: the brief says provenance only. It reads the
`patches` column on patch rows: the brief says the column is the recipe's.
It counts shadowed rows as duplicates: 2 of 74 are.

**Pre-mortem.** A month on, GENERIC_X64 ships EmulationStation without
its cpugov patch again and nobody knows why: the bug filed here names the
directory and the slip, and its open item asks the next image's unpack log
for the patch line.

**Blindspot check.** 75 (a count over the wrong set: the first grouping of
T23); 22 (a probe that cannot report absence: a patch directory never
globbed is silent); 48 (an option's history unread: `PATCH_ARCH=x86` was
set on purpose). New: a dead patch that is a live defect.

**Replaced mechanism.** None.

**Honesty check.** A second archetype, the M7 root reading the bug: a
`bug` on the fork counts against its candidate's step 0; the brief says the
fix is a packet and the proof an image's unpack log, so the disposition is
clear before the candidate.

## 5. What adjustments or investigations must happen BEFORE execution?

**Written into version 1 of the brief:** the five classes with their sizes
as the coordinator's figures to reproduce; the generator's header fields;
D-WORKFLOW-209's rule and #1048/#346 as where the class decision lives;
class (c) as a bug with its trace and no fix here; the 72 shadowed rows as
T41/T42 leads by package; the confs as provenance only; the six
upstream-deleted rows as a third upstream status; the drift check as a
count. **Filed now:** the epic #1054. **Left for the stranger's proof:**
every figure above.

### Errata from the stranger's proof of T40's brief (version 2, 2026-10-25)

A read-only reader with no context checked 56 rows of version 1 (38
verified, 2 wrong, 11 partial, 1 uncheckable; 3 API calls). What version 2
corrects, each at the place it lands:

1. **Four rows of class (e1) are reached after all.** gcc's and cmake's
   overrides carry `patches` as a git symlink to the generic directory;
   `unpack`'s `${PKG_DIR}/patches/*.patch` follows it and applies gcc's three
   and cmake's one on every image. The inventory never resolves a symlinked
   `patches` entry: a second tool gap beside #1049, a bug the lane files. So
   the shadowed non-duplicates are 68, not 72.
2. **Class (e) is 6 + 16 + 2 + 4**, not 7 + 17 + 4: two ROCKNIX-own rows in
   unbuilt recipes (panda3ds-lr's gles patch, play-lr's build fix) sit in it
   unnamed.
3. **The class-(c) bug sketch had two gaps:** the vitaquake2 patches differ
   by one hunk of four lines, and a `patches/x86` rename alone would not take
   effect, because `pre_make_target` passes `platform=` only for aarch64
   after `unpack:196`; the test image never builds vitaquake2-lr, so the next
   image proves only the EmulationStation patch, whose slip is a wrong call
   at run time (not a compile failure) and sits in the non-x86 arm too.
4. Smaller: "427 live patches" is the device-level kernel count (the
   override has 20); two of the 14 header-less patches are LibreELEC's;
   three of the 102 upstream commits are ROCKNIX's own; T24 (#671) is open,
   not accepted; `get_pkg_directory` spans 1057-1090, the inventory's
   patch-row rule 447-460, the trailers are 96; #1054 had no futro comment
   until the dispatch posted it.

Not checked by the proof, and left to the lane's stage A: the generator's
own counts, the headers' tags and series positions, T23's join at the
lane's tree.


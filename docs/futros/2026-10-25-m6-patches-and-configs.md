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


## Errata, after T40's acceptance (2026-10-25)

- The futro's *68 LibreELEC changes the override builds without* is 50
  with no counterpart plus 18 the override carries in another form (T40's
  `02` § The shadowed 74). T42's brief inherits the 50 by override.
- The symlinked `patches` directories (gcc's, cmake's) are the inventory's
  second gap, filed as #1056 beside #1049; T41's and T42's reach columns are
  read with that gap in mind until the tool is fixed.
- Class (c) became two bugs, one per unit (#1071, #1072), and the M7 lane's
  GENERIC build01 failed the same day on a source manifest that had applied
  the dormant `cpugov.patch` -- the class (c) fact reached it through the
  host file within minutes, which is what the area futro's "a dead patch
  that is a live bug" paragraph was for.

## T41 kickoff addendum (written with the brief's version 2, 2026-11-02)

**The plan, in the order's words:** T41 is *the kernel patches and configurations the shipped and test images apply*, `patches-shipped-kernel` (`k: 41`), kind table, lens package currency, read before none, depth Local (*"a provenance table"*), globs `projects/ROCKNIX/devices/**`, `projects/ROCKNIX/packages/linux*/**`, `packages/linux*/**` less the H700 and GENERIC_X64 `linux/*.conf`, reach shipped and test; its why *"one provenance row per kernel patch and configuration a shipped image or the test image applies (#339 criterion 2) ... the fork-written H700 kernel patch is read line by line here"*; its closing evidence *"one row per patch; audit folder, lint PASS"* (`docs/reviews/order.md` § T41). The order's 40,474 lines are the inventory's column and `grep -c ''` at the P1 tip; `wc -l` prints 40,473, one file having no trailing newline (the brief's § 1 (a)). Five of the 107 are not the kernel's: the four H700 U-Boot patches and the one `kernel-firmware` patch, tabled `non-kernel` with their recipes' owners T27 and T11 (ruling (b), version 2 -- version 1 named T42 for the firmware recipe, which the inventory's area `devices` for that recipe corrects).

**Assumptions the plan leans on and does not state:** that every row is a kernel patch -- five are not (L-21); that `fork-own` finds the fork-written patch -- the inventory tiers all 107 `vendor-carried`, and only `tier_note` names the H700 ramoops patch fork-written (L-17); that the two fork-changed configurations are T41's -- the order carves the H700 and GENERIC_X64 `linux/*.conf` out (T27's and T11's; R1 § 8 delta 6), so the one `.conf` here is SM8550's, never fork-changed; that `0 fork-own` means no fork commit -- one row has one (`cbf75c0b06`); that a `patches/` directory the recipe names is the glob's -- `${LINUX}` is empty and the override has no `${DEVICE}` or `default` directory, each skipped by `unpack:143`'s `-d` test without a message (L-15); and, met by the proof, that the local ref `upstream/next` stands still -- it moved 59 commits during the drafting, so version 2 pins `651150fc88` in every command (proof X01).

**Known unknowns:** with this futro's `:67-73` (the shadowed rows and the config-diff clause), `:96` (the 427 live patches) and `:194` (the symlinked `patches` directories, #1056) as their spine, and the brief's `## Version 1` items with version 2's states (the proof settled 1, 4, 5, 9, 10, 16, 22, 23 and parts of 8 and 11): whether each of the 106 `.patch` applies at its device's pin (the dry-runs, ruling (g), now extended to the five `non-kernel` rows); the defconfig count against the 7.2 tarball (8 (b)); the kernel version at the builds' commits (12); the members `tar` reports absent (13); whether mainline 7.2's `sun50i-h616.dtsi` already carries a ramoops node (17); the ramoops patch's contribution layer and the `7.0/` triple as symlinks (§ 4's two questions, for the pause).

**Patterns:** a count from the wrong tree (blindspot 75: the P1 clone has no `upstream/next`, so every upstream read is the coordinator's store); a pin as a claim about the image (blindspot 47: the recipe's `case` names the pin, the image is not read); a duplicate edited on one side (the `7.0/`/`7.2/` `0010-msm-resource-cleanup.patch` pair, fixed upstream by `9416eec2c2` and carried unfixed here, L-01); a header that under-describes a squashed series (L-13); and from T40's table, a dead patch that is a live bug (`cpugov.patch`, #1071/#1072) -- the reason the applies-at-pin column exists.

**What we could be missing (the simulation):** an Opus lane with only the brief: it edits a `.conf` to "fix" a config the pin dropped; fetches a kernel tarball to test applies-at-pin instead of reading the cache; runs `git apply` against the generic `packages/linux` source, the wrong kernel; runs `tools/adjust_kernel_config` to read a config and rewrites the tree's conf; extracts a tarball into the worktree or `/tmp`; copies the fixed `0010` from upstream into `7.0/`; types `0 fork-authored` from T40's brief; sorts the table under the host locale; writes one pin for all 107; counts fork-own by `tier`; calls the four U-Boot rows kernel patches; sends the ramoops patch upstream; or reads `upstream/next` as the brief's commit after the ref has moved (R5 § C; proof X01).

**Adjustments before execution:** all in version 2 of the brief (`docs/reviews/briefs/patches-shipped-kernel.md`, `## Version 2: corrections from the proof`): the proof's seven corrections (`kit/t41-proof.md`; its tally `checks 112; PASS 93; MISMATCH 7; SETTLED 8; NOTE 4; corrections 7`), the heavy ones the pinned upstream commit (X01), the seven `reachable_by` groups (X02) and L-22's fourth directory (X03); and the coordinator's two rulings -- the firmware recipe T11's, the non-kernel five's applies-at-pin by the same method against the cached U-Boot and firmware tarballs. From this addendum, for the coordinator at dispatch: D-WORKFLOW-221 written, #688's body rewritten from § 7's 28, the branch cut from the coordinator's tip with the pointer seeded as its first commit.

Written for version 2 of the brief; the corrections from the stranger's proof of version 1 are the brief's `## Version 2: corrections from the proof`.

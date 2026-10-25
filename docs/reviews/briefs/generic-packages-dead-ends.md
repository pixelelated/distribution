---
slice: T23
id: packages-dead-ends
issue: "#670"
epic: "#848"
area: generic-packages
kind: table
lens: reachability
depth: Local
version: 1
written: 2026-10-25
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
---

# T23: the generic packages no image builds (a reachability table)

**Version 1, 2026-10-25, by the coordinator.** A brief for a lane that has
never seen this project, in the shape of T45's
(`docs/reviews/briefs/tooling-council.md`) and T7's
(`docs/reviews/briefs/generic-packages-reached.md`, the same area): a
**table slice at Local depth**. No reviewer seat; no fix streams, because
**this slice removes nothing and edits no recipe** (§ 1, D-WORKFLOW-209); the
output is one table of 731 package units with a disposition each, the
findings the table turns up, and the one decision it prepares for the
maintainer. The order's § T23 (`docs/reviews/order.md`, P1's `2174265e9c`)
is the slice's definition; this brief is the work. Every figure here was
produced by a command run at the hash named beside it; a stranger's proof
precedes dispatch, and version 2 records what it found.

## 1. Identity

- **Issue:** #670 `M6.P2 E848/T23: generic-packages: the generic packages no
  image builds`, slice `packages-dead-ends` (`k: 23`) in
  `docs/reviews/slices.json`, twenty-third in `docs/reviews/order.md` (its
  row: *1,604 | 95,892 | -- | 0 | Local*; its `why`: *the largest dead set:
  95,398 lines no plan reaches; 620 of the inventory's unreached rows are
  copies shadowed by a ROCKNIX override ... the session re-derives
  reachability for a sample with `tools/viewplan` (two commands for one
  quantity) and decides the removals*; its `depth_reason`: *a reachability
  table: the counts are the check*). **Epic:** #848 (the generic packages:
  T7 #654 accepted at `db6597356b`, T8 #655 accepted at `f50a031158`; this
  slice is the area's last; the epic's futro
  `docs/futros/2026-10-24-m6-generic-packages.md` carries its T23 addendum).
  **Milestone:** M6; its body holds the live order; read it first.
  **Predecessors that bear on these rows:** **T7** (the 266 reached generic
  rows: `docs/audits/2026_10_24-epic-m6-generic-packages-reached/02-forward-audit.md`
  § Coverage table) and **T8** (the image's own 485:
  `docs/audits/2026_10_24-epic-m6-image-packages/02-forward-audit.md`), whose
  rows say which ROCKNIX override is live where this slice's row is a
  shadowed copy; **T6's lead on #670** (two global-scope reads in unreached
  recipes, `packages/addons/tools/jre.zulu/package.mk:12` and
  `packages/graphics/mesa-reusable/package.mk:14`); **T10** (#657), which
  reviewed `tools/renovation-inventory`, the tool whose `reach` column is
  this slice's first command (D-WORKFLOW-204: `tools/renovation-status`
  reads the same column); **D-WORKFLOW-185/186/187** (the shipped set is
  H700 and SM8550, GENERIC_X64 the test image; the renovation gates no
  release); **D-WORKFLOW-198/199** (the base merge keeps three ROCKNIX
  overrides upstream deleted, `spirv-headers` among them -- one of this
  slice's three fork-own rows). **Beside it:** T15, in the T3 session, on a
  different file set (D-WORKFLOW-190).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #670, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves (D-WORKFLOW-187) -- here, most likely,
  a defect in `tools/renovation-inventory`'s reach (§ 2).
- **The removal rule, which this brief decides (D-WORKFLOW-209).** The lane
  **removes nothing and edits no recipe.** Of the 1,604 rows, 1,601 are
  upstream-carried (byte-identical to `upstream/next`; the fork tracks that
  branch and every `git merge upstream/next` would carry a deletion forward
  as a modify/delete conflict, D-WORKFLOW-198's class), and the futro for
  this area already holds T7 to *deletes nothing upstream carries*. So the
  table's deliverable is a **disposition per unit**, one of six:
  `dead, upstream-carried` (recorded; the removal of the class is **one
  decision for the maintainer**, which the coordinator puts on #346 with the
  table's numbers and the cost against the value -- § 4 Q1); `shadowed copy,
  override live` (the plan builds the ROCKNIX override; the copy is dead;
  recorded, same class); `shadowed copy, override dead too` (both copies are
  dead; recorded); `unshipped` (buildable only by a device the fork does not
  ship, T25's set; recorded); `fork-own, dead` (three rows; a removal is
  **proposed** on the punch list with its `Already written:` line and left
  for the coordinator, never made here); and `reached after all` (the
  inventory's column is wrong for it: a finding, and the row leaves this
  slice's set). Nothing in `packages/` or `projects/` changes on this
  branch.
- **One worktree, one session.** Branch `feature/m6-packages-dead-ends-670`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-packages-dead-ends-670`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #670). **Before that
  comment exists nothing runs in it.** The session is the T5 lane's
  (`m6-t5-build-engine`), which ran T5, T6, T7, T8, T9, T12 and T45; those
  worktrees stay beside this one, idle, until their merges, and nothing is
  written there. The primary checkout stays on `next` (D-INFRA-025); the
  legacy checkout and `rocknix.worktrees/*` are the M7 lane's, read only.
  **The rules in this worktree are `next`'s except the paths the dispatch
  comment lists.**
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Local** (plan § 6c; `slices.json` k 23: *a reachability
  table: the counts are the check*): **no reviewer seat**.
  `second-opinions/review-plan.json` records depth `local`, scope `epic`,
  primary `anthropic/claude-opus-5-5` / lab `anthropic`, reviewers `[]`, and
  the sentence *the lint and the counts are the check*; **`tools/council/run
  invoke` is never run in this slice.**
- **The host, read on 2026-10-25 by the coordinator:** M6's; the M7 lane
  holds a flexible component-qualification window granted at 03:43 (one
  compiler or one guest at a time, M7's); **this slice runs no guest, no
  build and no compiler.** Its one tool with a cost is `tools/viewplan`,
  which generates a device's build plan from the recipes in Python in
  seconds (`Packages loaded : 1435`, GENERIC_X64) -- plan generation, not a
  build. Nothing here touches the sources cache or a build root. Register: the three IDs from 206 to 208 in the workflow series are the M7 lane's (reserved, unpublished until its rows land); a row this slice forces takes **D-WORKFLOW-209 or higher** (D-WORKFLOW-209 itself is the removal rule above, the coordinator's, written at dispatch); D-QA-064 and
  D-INFRA-032 are the next free in their areas.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-packages-dead-ends-670
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-packages-dead-ends-670
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists
cat .github/sessions/saved-session-state-feature-m6-packages-dead-ends-670.md    # seeded by the dispatch
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git log --oneline c445081a59..upstream/next -- packages | wc -l      # 0: upstream has not touched packages/ since the base
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-packages-dead-ends-670
```

## 2. Scope

**1,604 paths, 95,892 lines (the inventory's column); 1,601 upstream-carried
and 3 fork-own; reach `unreached` 1,565 and `unshipped` 39; 727 recipes
(`package.mk`) and 877 other files (124 with no extension, 104 `.service`,
100 `.py`, 97 `.png`, 81 `.conf`, 73 `.xml`, 58 `.txt`, 37 `.po`, 35 `.svg`,
...); no `.patch` file -- the patch directories of these packages are
`patches-dead`'s rows (T40, #687), which that table records as this slice's.**
The membership is the inventory's rows in area `generic-packages` whose reach
is `unreached` or `unshipped` (`slices.json` k 23: `select: {reach:
[unreached, unshipped]}`; the area's own exclusions keep the emulation,
kernel, firmware and driver trees out). The block, at `2174265e9c`:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
t=[r for r in rows if r["area"]=="generic-packages" and r["reach"] in ("unreached","unshipped")]
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t), dict(collections.Counter(r["tier"] for r in t)), dict(collections.Counter(r["reach"] for r in t)))
print("recipes",sum(1 for r in t if r["path"].endswith("/package.mk")),"shadowed rows",sum(1 for r in t if r.get("shadowed_by")))
import os; os.makedirs(".qa-scratch/t23", exist_ok=True)
open(".qa-scratch/t23/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))'
# paths 1604 lines 95892 {'upstream-carried': 1601, 'fork-own': 3} {'unreached': 1565, 'unshipped': 39}
# recipes 727 shadowed rows 260
```

**By unit.** A unit is a recipe directory: every one of the 1,604 files has
an ancestor directory holding a `package.mk` in the inventory (none is an
orphan), and **731 such units** hold them -- 727 whose recipe is itself in
this set, and **4 whose recipe is outside it** (11 files, e.g.
`packages/addons/addon-depends/chrome-depends/gtk3/files/settings.ini` and
`packages/addons/tools/btrfs-progs/{changelog.txt,icon/*}`: a file marked
unreached under a recipe marked reached -- the first rows the table settles,
because `compute_reach` marks a file by its owning directory, so these say
something about the tool). By group (units): `packages/addons` 297,
`packages/mediacenter` 166, `packages/devel` 35, `projects/ROCKNIX` 28,
`packages/graphics` 25, `packages/tools` 23, `packages/sysutils` 21,
`packages/multimedia` 17, `packages/network` 17, `packages/audio` 16. **Kodi
and its addons are the bulk:** `addons` (851 rows) and `mediacenter` (208)
are 1,059 of the 1,604 -- LibreELEC's media centre, which no ROCKNIX image
builds. The largest units by lines: `packages/addons/service/snapserver`
36,749 (26 files; `snapweb/3rd-party` alone is one 34,569-line file),
`packages/sysutils/busybox` 5,440 (45 files, **shadowed**: the ROCKNIX
override `projects/ROCKNIX/packages/sysutils/busybox` is the live one),
`packages/security/openssl` 2,972 (3, shadowed), `tvheadend43` 1,852,
`sundtek-mediatv` 1,765, `packages/sysutils/systemd` 1,686 (38, shadowed).

**Shadowed.** The inventory's `shadowed_by` column is set on **260 rows in
93 units** at `2174265e9c` (the order's § T23 said 620; the column at the
hash is the figure, and the table states it). It names the override
directory a plan resolves the package name to (`get_pkg_directory`), e.g.
`packages/addons/addon-depends/go` -> `projects/ROCKNIX/packages/lang/go`.
**Unshipped:** 39 rows in 21 units, buildable only by RK3326, RK3566, RK3576,
RK3588 or S922X -- devices the fork does not ship (T25's, #672). **Fork-own,
three rows:** `packages/tools/installer/package.mk` (upstream has it; the
fork's `459feac81e` of 2026-07-01 dropped its grub dependency for
GENERIC_X64 -- and **`installer` is in the GENERIC_X64 plan** the
coordinator generated, so which directory that plan resolves it to decides
whether this row is a shadowed copy or reached after all);
`projects/ROCKNIX/packages/graphics/spirv-headers/package.mk` (kept at the
base merge by D-WORKFLOW-199; see the class below); and
`projects/ROCKNIX/packages/rust/cbindgen/package.mk` (named by nothing at
`8ebaf8daad` outside its own directory -- `git grep -n cbindgen 8ebaf8daad --
packages projects` -- and not on `upstream/next`: the one row that may be
simply dead and the fork's to remove).

**The coordinator's re-derivation, 2026-10-25, on its own tree** (the lane
repeats it on its branch at stage A; the recipes under `packages/` are
byte-identical to upstream and unchanged since the base, so the tree does not
matter for them): `tools/viewplan image` for `GENERIC_X64/x86_64`, `H700/aarch64` and `SM8550/aarch64` -- the three images the renovation reads (D-WORKFLOW-185) -- lists **593, 605 and 672 distinct package names (union 688)** on its `build`/`install` lines. The inventory itself ran **26 configs** (every device and arch the Makefile builds, each with its root: `image` for aarch64 and x86_64, `arm` for the 32-bit half) **inside the pinned build container** (its header's `plan_runner`, `mode: container`), and its `shipped`/`test`/`unshipped` split reads from that set: the shipped and test devices' five configs (`H700-arm`, `H700-aarch64`, `SM8550-arm`, `SM8550-aarch64`, `GENERIC_X64-x86_64`) decide `unreached` against the rest. The lane regenerates those five on the host, records the header's per-config package counts beside its own (611 for `H700-aarch64`, 672 for `SM8550-aarch64`, 593 for `GENERIC_X64-x86_64` in the header; the coordinator's host runs gave 605, 672 and 593, so the H700 plan differs by six names between the container and the host -- a disagreement to name, not to resolve in silence), and reads the other 21 configs' names from the header rather than regenerating them unless a row needs it. **84 of the 727 recipes carry a
name some plan builds, and every one of the 84 is a shadowed copy**: the plan
builds the override. **32 shadowed units carry a name no plan builds**: the
override is dead too, so both copies are (a disposition of its own). And
**one class the inventory's reach does not follow:
`PKG_DEPENDS_UNPACK`.** `tools/renovation-inventory`'s `compute_reach`
follows each plan's packages and the recipes a recipe sources with
`. ${ROOT}/packages/...` (its `SOURCED` regex), not `PKG_DEPENDS_UNPACK`.
`packages/graphics/spirv-tools/package.mk:16`,
`packages/graphics/vulkan/glslang/package.mk:17` and
`packages/lang/llvm/package.mk:46` -- all three in all three plans -- name
`spirv-headers` there and unpack its tarball
(`${SOURCES}/spirv-headers/spirv-headers-$(get_pkg_version spirv-headers).tar.gz`),
so **`projects/ROCKNIX/packages/graphics/spirv-headers` is fetched and
unpacked for every image while the inventory says `unreached`.** 24 of this
slice's recipes are named by some recipe's `PKG_DEPENDS_UNPACK`; a named
unit is reached when its namer is reached (spirv-headers is; tsdecrypt's,
hyperion's and kodi's dependants are named by recipes that are themselves in
this set). The table computes the closure; the tool's gap is a **finding
against `tools/renovation-inventory`** (T10's set) and a `bug` the lane
files, because D-WORKFLOW-204's status and every later slice's membership
read that column.

**What is not here, and where it is:** the patch directories of these
packages (T40's table, which records them as removed-by-T23 only if a removal
ever happens -- it does not, under D-WORKFLOW-209); the reached generic
recipes (T7); the overrides (T8); the unshipped devices themselves (T25).

## 3. Read first

1. `next:AGENTS.md`; the every-session rules; **`engineering-practices.md`
   § Before deleting a duplicate** (the shadowed copies) and § A name is not
   a behaviour (a column is a claim about one run of one tool);
   `upgrade-and-install.md` § Every fix answers what was already written
   (the `Already written:` line every proposed removal carries);
   `packaging-and-patches.md` and `packages/README.md` (what a recipe is).
2. `docs/reviews/plan-for-the-plan.md` whole (§ 4 Q6 and the Renovation
   category; § 5 on tables; § 6c on Local depth; § 8 on drift);
   `docs/reviews/order.md` § T23, § T7, § T8, § T25 and § T40; this brief
   whole; the area futro `docs/futros/2026-10-24-m6-generic-packages.md`
   with its T23 addendum.
3. `tools/renovation-inventory` at `2174265e9c` whole -- `compute_reach`,
   `split_reach`, the shadowed logic and the `SOURCED` regex -- and
   `tools/viewplan` (eleven lines: `pkgjson | genbuildplan.py --show-wants`);
   `scripts/genbuildplan.py` for what a plan line means; `config/functions`
   for `get_pkg_directory` and `PKG_DEPENDS_UNPACK`.
4. T7's `02-forward-audit.md` § Coverage table and T8's (the live copies);
   T6's `02-forward-audit.md` § Leads from the sweeps at `37d1d98aed` (the
   two late-binding reads); the live M6 body; #670 (with its comment); #848
   (the epic, its futro comment); #339; #346; #644; #657 (T10, the tool's
   review) and #585 (the upstream contribution queue, where a tool fix with
   upstream value is recorded).
5. The register rows D-WORKFLOW-185, 186, 187, 189, 198, 199, 204 and 209.

## 4. The questions

The seven renovation questions of plan § 4, with **reachability** as the
lens and the table as the answer:

- **Q6 Dead ends -- the table.** One row per unit (731), with: the unit, its
  files and lines, tier, the inventory's reach and `shadowed_by`, the
  re-derivation (named by which of the three plans; the directory each plan
  resolves the name to; named by a reached recipe's `PKG_DEPENDS_UNPACK`),
  and the disposition from § 1's six. The two commands for one quantity are
  the inventory's column and the lane's own three `viewplan` runs; a
  disagreement is a finding, never silently resolved either way.
- **Q1 Modernize -- the decision this slice prepares.** What the dead set
  costs the fork (95,892 lines the inventory, the rules check, the guards
  and every later slice carry; the time a reader spends finding out a
  recipe is dead) against what removing it would cost (a deletion of
  upstream's files is a modify/delete at every `upstream/next` merge; the
  evidence for the rate: `git log --oneline c445081a59..upstream/next --
  packages | wc -l` is **0** -- upstream has not touched `packages/` since
  the base, and LibreELEC master reaches it only through ROCKNIX's merges of
  LibreELEC, 453 such merges in upstream's history), written as one
  paragraph the coordinator carries to #346 with the table's counts. The
  lane recommends; the maintainer decides; nothing is removed here.
- **Q7 Clarity and structure:** the shape of the dead set (Kodi and its
  addons as the bulk; the shadowed copies that mirror an override; the
  `projects/ROCKNIX` units no image builds) in one section a reader can use
  to know what `packages/` is for in this fork.
- **Q2 Standards:** `tools/pkgcheck` over the 727 recipes (host, seconds):
  the late-binding faults in dead recipes are recorded in the table, not
  fixed (a dead recipe is not changed under D-WORKFLOW-209), and T6's two
  leads (`jre.zulu:12`, `mesa-reusable:14`) are judged -- set above in the
  recipe or not -- and dispositioned as rows.
- **Q3 Bugs:** the inventory tool's `PKG_DEPENDS_UNPACK` gap (a defect with
  a VM-free proof: a constructed recipe reached only that way reads
  `unreached`), the 11 files under a reached recipe marked unreached, and
  any recipe the plans build that the column calls unreached: each a `bug`
  on the tool with its constructed case, filed by the lane (the fix is
  T10's set, not this slice's: the lane edits no tool).
- **Q4 Package currency:** none -- an unreached pin is not currency; a unit
  found reached after all is handed to T7's or T8's table by the
  coordinator.
- **Q5 Efficiency:** none on a device; the cost here is the reader's and
  the build's (`Packages loaded : 1435` of which the three plans build 688).

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every cell cites a command's
   output (the inventory's row, the plan line, the `git grep` for the
   namer, `pkgcheck`'s line) or a file's field.
2. Mechanical evidence outranks reading: the inventory's `reach` is a
   claim; the plan the lane generates is the evidence; where the two
   disagree, both are quoted and the disagreement is the finding.
3. **The bench is the host; no guest, no build, no provider.** **Can this
   be done on the VM? Yes -- on the host: a table of inventory rows, three
   generated build plans, `git grep` and `pkgcheck`, none of which needs a
   guest, a device, a compiler or a provider; the network is not used at
   all** (the plans read the recipes; nothing is fetched). `tools/council/run
   invoke` is never run.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The runs, with what the coordinator read** (the lane runs each at stage A
in its worktree and records the exit, the wall time and the summary line;
`TMPDIR` under `/workspace/tmp/m6-t23/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-packages-dead-ends-670
cd "$D"; export TMPDIR=/workspace/tmp/m6-t23/tmp; mkdir -p "$TMPDIR" .qa-scratch/t23
# the shipped and test set's five plans (plan generation in Python; seconds each; no build, no fetch); the root per config as the inventory's header has it
for cfg in GENERIC_X64:x86_64:image H700:aarch64:image H700:arm:arm SM8550:aarch64:image SM8550:arm:arm; do dev=${cfg%%:*}; r=${cfg#*:}; arch=${r%:*}; root=${r#*:}; s=$(date +%s)
  PROJECT=ROCKNIX DEVICE=$dev ARCH=$arch tools/viewplan "$root" > ".qa-scratch/t23/plan-$dev-$arch.txt" 2>&1; rc=$?
  echo "$dev-$arch rc=$rc $(( $(date +%s) - s ))s $(grep -m1 'Packages loaded' ".qa-scratch/t23/plan-$dev-$arch.txt") names=$(grep -E '^\s*(build|install)\s' ".qa-scratch/t23/plan-$dev-$arch.txt" | awk '{print $2}' | sed 's/:.*//' | sort -u | wc -l)"; done
# the coordinator's, on the host, the three image roots only: 593 / 605 / 672 distinct names, union 688; rc 0, about 10 s each; the header's (container) 593 / 611 / 672
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c 'import json,sys; h=json.load(sys.stdin)["header"]; [print(c["config"], c["root"], c["packages"]) for c in h["configs"]]; print(h["plan_runner"])'
# which directory a plan resolves a name to (the shadowed check, per name): config/functions' get_pkg_directory
( . config/options "" >/dev/null 2>&1; for n in busybox go installer spirv-headers; do printf '%s -> %s\n' "$n" "$(get_pkg_directory "$n")"; done )
# the PKG_DEPENDS_UNPACK namers of this slice's recipes (the closure the table computes)
git grep -n -E '^PKG_DEPENDS_UNPACK=' 8ebaf8daad -- packages projects | wc -l
# the two late-binding leads from T6, read in place
git show 8ebaf8daad:packages/addons/tools/jre.zulu/package.mk | sed -n '1,14p'; git show 8ebaf8daad:packages/graphics/mesa-reusable/package.mk | sed -n '1,16p'
# pkgcheck over the 727 recipes (host; records, never fixes)
n=0; f=0; while read -r p; do case "$p" in */package.mk) n=$((n+1)); tools/pkgcheck "$(dirname "$p")" >/dev/null 2>&1 || f=$((f+1));; esac; done < .qa-scratch/t23/paths.txt; echo "pkgcheck: $n recipes, $f with findings"
# the removal rule's own check: nothing changes under packages/ or projects/ on this branch
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1      # empty
# upstream's touch on the dead set since the base (Q1's figure)
git log --oneline c445081a59..upstream/next -- packages | wc -l      # 0
```

**The table's generator** is the lane's, under `stage-b/` in the audit
folder (as T45's `provenance.py` and T7's `t7-tables.py`): it reads
`inventory.json` with § 2's filter, assigns every file to its nearest recipe
ancestor, reads the three plan files and the `PKG_DEPENDS_UNPACK` closure,
and asserts the counts (1,604 files, 727 recipes, 731 units) so that a
missing row fails there rather than printing an empty cell. `02`'s coverage
table (one row per path, 1,604) and § Reachability (one row per unit, 731)
come from the same script, so they cannot disagree.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#670`
(`Refs #670`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-generic-packages-dead-ends/00-running-log.md` | the flight recorder: model and effort, `reviewed-at` with `8ebaf8daad`, the host file's last line and census at stage A, every run with exit and wall time | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 1,604 re-derived with § 2's block, the 731 units, the three plans' counts, the shadowed and unshipped figures at the hash, the three fork-own rows | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #670's checklist; **§ Reachability: the 731-row unit table** (unit, files, lines, tier, inventory reach, `shadowed_by`, the plans that name it and the directory each resolves to, the `PKG_DEPENDS_UNPACK` namer and whether it is reached, disposition); § Disagreements (every unit where the column and the plans differ, with both quoted); **a coverage table with one row per path under `## Coverage`** (1,604); § The runs; § Proofs with `proved:` cells | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the inventory tool x the plans x the overrides x T7's and T8's rows x T40's patches | B |
| Analysis | `.../04-analysis.md` | Phase 4 § Finding Verification; **§ Renovation face Q1 to Q7, Q6 carrying the dispositions by class with counts and Q1 the cost-against-value paragraph for the maintainer**; § Instruction File Recommendations | B |
| Second opinions | `.../second-opinions/review-plan.json` | depth `local`, reviewers `[]`, the sentence *the lint and the counts are the check* | B |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where, acceptance, `Already written:`, the VM line; the YAML `punch_index`; the three fork-own rows' proposed removals as items with `Already written:`, outcome `deferred` to the coordinator's decision | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #670 | `Audit: M6 T23 the generic packages no image builds -- N findings (...)` | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect proven by a run: the tool's `PKG_DEPENDS_UNPACK` gap with its constructed case; a file marked unreached under a reached recipe; a plan-built recipe marked unreached; each with the VM line | D |
| Retro | `docs/retros/<date>-m6-generic-packages-dead-ends.md`, posted on #670 | the mini-retro; what the slice did to the two time-to-play numbers (nothing); what the maintainer's decision on #346 needs from the table | G |

## 7. Acceptance

The checklist on #670 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #670 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-generic-packages-dead-ends/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-generic-packages-dead-ends/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: local`, `reviewers: []` and the sentence *the lint and the counts are the check*; no `*.provenance.json` from a provider call exists in the folder (`ls second-opinions/ | grep -c provenance` is 0).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (the coordinator's decision issue for a proposed removal, the tool's bug, or a Backlog the coordinator files), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits; nothing under `packages/` or `projects/` changes on this branch: `git diff --stat 8ebaf8daad <fixed-at> -- packages projects` is empty and `git diff --diff-filter=DR --name-only 8ebaf8daad <fixed-at> -- packages projects` is empty (D-WORKFLOW-209).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (1,604 paths, 95,892 lines; 1,601 upstream-carried and 3 fork-own; 1,565 unreached and 39 unshipped; 727 recipes; 260 shadowed rows), the 731 units and the 4 whose recipe is outside the set, and the five plans' `Packages loaded` lines and distinct-name counts beside the header's.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `1604`.
- [ ] `02-forward-audit.md` § Reachability carries exactly 731 rows (``awk '/^## Reachability/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `731`), each with the § 6 columns and one of § 1's six dispositions; the shadowed split (the coordinator's 84 plan-named, all shadowed; 32 shadowed with no plan naming either copy) is reproduced or its delta stated with the command; every unit named by a reached recipe's `PKG_DEPENDS_UNPACK` is listed as reached after all (`spirv-headers` among them) and `installer`'s resolved directory is named.
- [ ] `02-forward-audit.md` § Disagreements lists every unit where the inventory's `reach` and the lane's plans differ, both quoted; each is a finding on the punch list and, where the tool is wrong, a `bug` on `tools/renovation-inventory` with a constructed case (a recipe reached only through `PKG_DEPENDS_UNPACK`, read as `unreached`), filed with its VM line and passing `tools/box-check --issue N`.
- [ ] `02-forward-audit.md` § The runs records the five `viewplan` runs (exit, wall time, `Packages loaded`, distinct names, each beside the inventory header's count for the same config), the `get_pkg_directory` reads for the shadowed sample, the `pkgcheck` sweep's counts over the 727 recipes, and T6's two leads judged, each with *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows no build, no guest, no compiler, no `tools/council/run invoke`, no fetch (`get_archive`, `scripts/get`) and no write under `/workspace/repos/rocknix*` or `/tmp`.
- [ ] `04-analysis.md` § Q6 carries the dispositions by class with counts summing to 731, and § Q1 the cost-against-value paragraph for the maintainer (the lines carried, upstream's 0 commits on `packages/` since the base, LibreELEC's route in, the merge cost of a deletion), ending in the lane's recommendation and the sentence that the decision is the maintainer's.
- [ ] `05-punch-list.md` carries one item per fork-own row (`installer`, `spirv-headers`, `cbindgen`) with its reachability verdict, and for a dead one a proposed removal with `Already written:`, outcome `deferred` to the coordinator; no removal is made.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`; no file under `tools/` is changed on this branch (`git diff --stat 8ebaf8daad <tip> -- tools` empty: the tool's fix is T10's set).
- [ ] The retro exists at `docs/retros/<date>-m6-generic-packages-dead-ends.md`, is posted on #670, says what the slice did to the two time-to-play numbers (nothing) and what the #346 decision needs from the table.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #670; a blocker named on #670 with what is needed; a branch that differs
from `8ebaf8daad` under `packages/` or `projects/` at stage A; or an
execution limit, stated as such with the running log current. A checkpoint
is not a stop; a differing count is a delta; `next` moving is drift. An idle
session says it is idle on #670, **does not end a turn on a post that asks
nothing**, and **updates its session pointer at every checkpoint** (#1014).

**What never runs in this slice:** a build, a package build, a compiler, a
guest, a fetch of any source; `tools/council/run invoke` or any provider
call; any removal, rename or edit under `packages/` or `projects/`
(D-WORKFLOW-209: the table proposes, the maintainer decides) or under
`tools/` (the inventory tool's fix is T10's set); a push to any branch but
the lane's own; `fork-worktree sync|remove|repair`; an edit to a rule,
`CLAUDE.md`, `AGENTS.md`, a decided register row or
`.github/sessions/saved-session-state-next.md`; a write under
`/workspace/repos/rocknix*` or `/tmp` (use `/workspace/tmp/m6-t23/`); a
credential-shaped literal written anywhere; `--no-verify`; bare `git stash`;
`git worktree remove --force` or `rm -rf` on a worktree or a bare variable
path.

## 9. Ceremonies owed

- A work-log entry per session headed `#670`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #670` or the
  guard.
- The VM question written before any proof (§ 5: the host; no guest; no
  network).
- The mini-retro at stage G, posted on #670, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator.
- A register row the same session for any decision the slice forces; the next Decided ID is D-WORKFLOW-209 or higher (the three before it are the M7 lane's; 209 is this brief's removal rule, written by the coordinator at dispatch),
  D-QA-064, D-INFRA-032; it goes at the end of `## Decided`, and a row is
  never edited.
- The merge notes: when `next` moves, the **coordinator** merges `next`
  into this branch, never between stage A and stage D; the coordinator
  merges its own branch into this one at hand-back before the last
  criterion's checkers run; a merge with conflicts is checked for leftover
  markers before it is committed (#696), and the ledgers are united by
  whole entries.
- Commit messages `docs: ...` (this slice edits no tool and no recipe), each
  with `Refs #670` and the attribution line; `git add -A` only after `git
  status --short` shows nothing a run left behind (`.qa-scratch/` is
  gitignored).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#670's checkboxes against their artifacts; the lint's `PASS` line; the
review plan (local, no reviewer, no provenance file); the audit issue's
checkboxes all at an outcome; the coverage table's row count (1,604) and the
reachability table's (731) against § 2; **re-running on an export of the tip under `/workspace/tmp`: the inventory block, the five plans regenerated and
the lane's generator run on them (the 84/32 split and the
`PKG_DEPENDS_UNPACK` closure recomputed), the empty diffs under `packages/`,
`projects/` and `tools/`;** `register-check` and `rules-check` on a
simulated merge with the coordinator's tip (the ledgers united; the archive
carrying `projects/`); the retro's answers. The lane posts one hand-back
comment naming the tip and each artifact by path, writes `reviewed-at:` and
`fixed-at:` into #670's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, carries the table's Q1 paragraph
and counts to the maintainer on #346 as the class decision, merges the
branch in its turn after the M7 candidate (after T8's, before T9's), and
closes #670 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#848) carries this slice's kickoff addendum, and a stranger's proof of
this brief is run by a reader with no context before dispatch; version 2
records what each found.

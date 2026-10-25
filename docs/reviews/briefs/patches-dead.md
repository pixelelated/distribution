---
slice: T40
id: patches-dead
issue: "#687"
epic: "#1054"
area: patches-and-configs
kind: table
lens: reachability
depth: Local
version: 1
written: 2026-10-25
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
  t23: feature/m6-packages-dead-ends-670 at f1561559aa
---

# T40: the patches and kernel configurations no plan applies (a provenance table)

**Version 1, 2026-10-25, by the coordinator.** A brief for a lane that has
never seen this project, in the shape of T23's
(`docs/reviews/briefs/generic-packages-dead-ends.md`, the same lens, the same
session): a **table slice at Local depth** that **removes nothing and edits
no patch** (D-WORKFLOW-209). The output is one table of 778 rows -- one per
patch or configuration file no image we build applies -- each with its
class, its provenance read from its header, its upstream status and its
disposition; the findings the table turns up; and one bug, already in sight.
The order's § T40 (`docs/reviews/order.md`, P1's `2174265e9c`) is the
slice's definition; this brief is the work. Every figure here was produced
by a command run at the hash named beside it (the research notes behind
§ 2 carry each command); a stranger's proof precedes dispatch, and version
2 records what it found.

## 1. Identity

- **Issue:** #687 `M6.P2 E1054/T40: patches-and-configs: patches and kernel
  configurations no plan applies`, slice `patches-dead` (`k: 40`) in
  `docs/reviews/slices.json`, fortieth in `docs/reviews/order.md` (its row:
  *778 | 317,908 | -- | 317,908 | Local*; its `why`: *the 277 generic kernel
  patches the ROCKNIX `linux` override never applies, `vitaquake2-lr`'s and
  EmulationStation's `patches/x86_64` (which `PATCH_ARCH=x86` never
  selects), the other projects' patches. Rows are generated from
  `inventory.json` and the patch headers (`From:`, `Subject:`); the session
  decides origin and removal*; its `depth_reason`: *a provenance table*).
  **Epic:** #1054 (the patches and kernel configurations: T40 first, then
  T41, T42, T43; its futro `docs/futros/2026-10-25-m6-patches-and-configs.md`).
  **Milestone:** M6; its body holds the live order; read it first.
  **Predecessors that bear on these rows:** **T23** (#670, accepted at
  `12374c733d`, close-out `f1561559aa`: its `02-forward-audit.md`
  § Reachability on `feature/m6-packages-dead-ends-670` is the join target --
  234 of these rows sit inside 117 of its dead units, and its class
  decision on #346 and its decision issue #1048 are where this table's
  removals, if any, are decided); **T24** (#671, accepted: the emulators'
  twelve recipes handed their patch directories here); **T5** (#652, the
  build engine: `scripts/unpack`'s patch selection and `config/functions`'
  `get_pkg_directory` are what makes a patch reached); **T10** (#657:
  `tools/renovation-inventory`'s `selected_patch_dirs` mirrors `unpack`'s
  directory list exactly, so #1049's `PKG_DEPENDS_UNPACK` gap does not reach
  patches); **D-WORKFLOW-209** (the removal rule), **D-WORKFLOW-185** (the
  shipped set), **D-WORKFLOW-198** (an upstream deletion at the base merge).
  **Beside it:** T15 in the T3 session and T13 in the T1 session, on
  different file sets (D-WORKFLOW-190).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #687, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves (D-WORKFLOW-187) -- here, class (c).
- **The removal rule (D-WORKFLOW-209).** The lane **removes nothing and
  edits no `.patch` or `.conf`.** Every one of the 778 is upstream's
  (`vendor-carried`, no fork commit ever). The table's deliverable is a
  **disposition per row**, one of: `dead: a generic kernel patch the ROCKNIX
  override never applies` (class a); `dead: another project's, which no
  Makefile target builds` (b); `never selected: a patches/x86_64 directory
  under PATCH_ARCH=x86` (c -- **a bug, filed, fixed by a packet, never
  here**); `inside a T23 dead unit` (d -- the unit's T23 disposition
  carried, so these rows follow T23's class decision on #346); `dead: a
  sourced generic recipe's patches, which the live override's globbing never
  reaches` (e1); `dead: an unbuilt recipe's` (e2); `already deleted at
  upstream/next` (the six: strace's two, grub's four, which the next base
  merge settles). The class decision for the 277 and the 234 of (a) and (b)
  is the maintainer's, on #346 beside T23's, put there by the coordinator
  with this table's counts at acceptance.
- **One worktree, one session.** Branch `feature/m6-patches-dead-687` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-patches-dead-687`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #687). **Before that
  comment exists nothing runs in it.** The session is the T5 lane's
  (`m6-t5-build-engine`), which ran T5, T6, T7, T8, T9, T12, T45 and T23;
  those worktrees stay beside this one, idle, until their merges, and
  nothing is written there -- T23's is read with `git show`. The primary
  checkout stays on `next` (D-INFRA-025); the legacy checkout and
  `rocknix.worktrees/*` are the M7 lane's, read only. **The rules in this
  worktree are `next`'s except the paths the dispatch comment lists.**
- **Model and effort:** Opus 5.5 at high effort. Record what ran in
  `00-running-log.md`'s header.
- **Review depth: Local** (plan § 6c; `slices.json` k 40: *a provenance
  table*): **no reviewer seat**. `second-opinions/review-plan.json` records
  depth `local`, scope `epic`, primary `anthropic/claude-opus-5-5` / lab
  `anthropic`, reviewers `[]`, and the sentence *the lint and the counts are
  the check*; **`tools/council/run invoke` is never run.**
- **The host, read on 2026-10-25 by the coordinator:** M6's; the M7 lane
  runs its input guests one at a time under its own grant and asks for a
  full build window next; **this slice runs no guest, no build, no compiler,
  no plan generation and no network** -- the classes come from
  `config/options ""` and `get_pkg_directory` (which make no request; the
  research pass's `curl` shim was never invoked), `scripts/unpack`, the
  Makefile, the headers and `git`. Register: the three workflow IDs before
  209 and D-INFRA-032 are the M7 lane's; 209 the coordinator's; a row this
  slice forces takes **D-WORKFLOW-210 or higher**, D-QA-064, D-INFRA-033.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-patches-dead-687
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-patches-dead-687
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists
cat .github/sessions/saved-session-state-feature-m6-patches-dead-687.md         # seeded by the dispatch
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git show feature/m6-packages-dead-ends-670:docs/audits/2026_10_25-epic-m6-generic-packages-dead-ends/02-forward-audit.md | awk '/^## Reachability/{p=1;next} /^## /{p=0} p' | grep -c -E '^\| `'   # 731: T23's join target, read, never checked out
git show 8ebaf8daad:Makefile | grep -o 'PROJECT=[A-Za-z0-9_]*' | sort | uniq -c   # 27 PROJECT=ROCKNIX
git show 8ebaf8daad:scripts/unpack | sed -n '125,134p'               # PATCH_ARCH=x86 on x86_64
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-patches-dead-687
```

## 2. Scope

**778 paths, 317,908 lines (the inventory's column); 760 `.patch` and 18
`linux*.conf`; all 778 tier `vendor-carried`, `reachable_by` and
`buildable_by` empty, `last_fork_commit` none; `shadowed_by` set on 351
(277 to `projects/ROCKNIX/packages/linux`, 74 to other overrides) and empty
on 427.** The membership is the inventory's rows in area
`patches-and-configs` whose reach is `unreached` (`slices.json` k 40). The
block, at `2174265e9c`:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
t=[r for r in rows if r["area"]=="patches-and-configs" and r["reach"]=="unreached"]
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t), dict(collections.Counter(r["tier"] for r in t)))
print("patch",sum(1 for r in t if r["path"].endswith(".patch")),"conf",sum(1 for r in t if r["path"].endswith(".conf")),"shadowed",sum(1 for r in t if r.get("shadowed_by")),"to the ROCKNIX linux",sum(1 for r in t if r.get("shadowed_by")=="projects/ROCKNIX/packages/linux"))
import os; os.makedirs(".qa-scratch/t40", exist_ok=True)
open(".qa-scratch/t40/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))'
# paths 778 lines 317908 {'vendor-carried': 778}
# patch 760 conf 18 shadowed 351 to the ROCKNIX linux 277
```

**The five classes, first match in order (the coordinator's, 2026-10-25, by
one script over the saved rows and T23's unit list; they sum to 778 rows and
317,908 lines):**

| Class | Rows | Lines | What it is, and why no plan applies it |
| --- | ---: | ---: | --- |
| (a) generic kernel patches | 277 | 92,389 | `packages/linux/patches/{rockchip 187, rockchip-old 48, dvb 39, default 3}`; every device resolves `linux` to `projects/ROCKNIX/packages/linux` (`get_pkg_directory linux` under each device's `config/options`), which neither sources the generic recipe nor shares a patch with it (0 of 277 subjects match the ROCKNIX kernel's 427 live patches); the generic dirs are chosen only by `LINUX=` values other projects' `options` set |
| (b) other projects' | 234 | 160,488 | 216 patches and the 18 confs under `projects/{Amlogic 94, Allwinner 81, Rockchip 15, Samsung 15, NXP 14, RPi 7, Generic 3, Qualcomm 3, ARM 2}`; the Makefile sets `PROJECT=ROCKNIX` in all 27 of its build lines, so the inventory marks every `projects/<other>/` path unreached before the patch rule is consulted |
| (c) an arch directory never selected | 5 | 99 | `projects/ROCKNIX/packages/emulators/libretro/vitaquake2-lr/{,vitaquake2-rogue-lr/,vitaquake2-xatrix-lr/,vitaquake2-zaero-lr/}patches/x86_64/001-set-platform.patch` (four, 18 lines each) and `projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch` (27 lines): `scripts/unpack` sets `PATCH_ARCH=x86` on x86_64 for every package (lines 127-128), so a `patches/x86_64` directory is never globbed. **Both recipes are live** (EmulationStation reached by GENERIC_X64; vitaquake2-lr buildable by AMD64) -- this class is the slice's bug, § 4 |
| (d) inside a T23 dead unit | 234 | 63,795 | in 117 of T23's 731 units: 158 rows in *dead, upstream-carried* units, 67 in *shadowed copy, override live*, 9 in *shadowed copy, override dead too* (strace 2, connman 6, grub 1); none in T23's five *reached after all* or its unshipped units |
| (e) the rest | 28 | 1,137 | (e1) 7 in generic recipes a live override sources -- gcc 3, cmake, readline, fluidsynth: the sourced recipe's `package.mk` row is `shipped`, but `PKG_DIR` is the override's and `unpack` globs `${PKG_DIR}/patches` only (lines 150-154), so the generic `patches/` is never reached; (e2) 17 in LibreELEC `packages/emulation/libretro-*` recipes no plan builds (T24's area); 4 under `linux-driver-addons/dvb/*/patches/disable-pci` and `linux-firmware*` recipes no plan builds |

**The headers (760 `.patch`):** 746 are `git format-patch` output (`From
<40-hex>`, `From:`, `Date:`, `Subject:` all present), 485 carry
`Signed-off-by:`, 97 a `Link:`, `Reviewed-by:` or `Acked-by:` trailer; the
14 without a header are ROCKNIX's hand-made diffs (the only hand rows; the
research notes list them). So the generator fills origin (`From:`), the
subject with its tag (`FROMGIT`, `FROMLIST`, `WIP`, `LOCAL`, `HACK`), the
series position (`[PATCH n/m]`) and the first target (`diff --git a/`) for
746 rows unattended.

**The shadowed 74 that are not the kernel's:** `get_pkg_directory` prefers
the override and `unpack` globs the override's `patches/`, so the generic
copy's patches never apply. **Only 2 of the 74 are duplicates by content**
of a patch the override carries (kmod's `fix-pkgconf`, systemd's
`remove-nonexistant-dependency`, re-homed under the override's naming); the
other 72 are LibreELEC changes the live ROCKNIX override builds *without* --
a package-currency question for T41's and T42's rows on the overrides, not
a removal here: T40's row points at the override's row and names the
patch's subject.

**Upstream since the base:** 0 fork-authored commits on the 778, ever; 102
upstream commits reach them since 2026-06-01, all through ROCKNIX's merges
of LibreELEC; **six rows are already deleted at `upstream/next`** (strace's
two, grub's four: `e6da8dad2b` 2026-10-22, `6103571f67` 2026-10-11, neither
in `next` yet) -- a third upstream status beside *carried* and *merged*,
which the next base merge settles without a decision.

**The 18 confs** (125,933 of the 317,908 lines): LibreELEC's and other
projects' kernel configurations, 16 of them 6,600 to 8,600 lines and
current upstream to 2026-08-05, two nine-byte `# dummy` placeholders; they
have no fork base to diff against (plan § 2's *one diff per kernel config
against its base* is for fork-written configs, T41's); the row is
provenance only.

**One trap in the inventory's columns:** the `patches` column is a
per-recipe count on `package.mk` rows (`tools/renovation-inventory`
lines 587-597); every patch row's cell is `None` by construction. A reader
asking *how many patches does this package carry* reads the recipe's row.

**What this slice does not touch:** any `.patch` or `.conf` (D-WORKFLOW-209;
the rename that would make class (c) apply is a packet after #346); the
recipes (T23's, T24's); the overrides' own patches (T41's, T42's: reach
`shipped`/`test`); the unshipped devices' (T43's); the inventory tool.

## 3. Read first

1. `next:AGENTS.md`; the every-session rules; `engineering-practices.md`
   § Before deleting a duplicate (the 74 shadowed), § Verify design intent
   (`PATCH_ARCH=x86` was set on purpose; read `git log -S` on it before
   calling it wrong) and § A name is not a behaviour; `packaging-and-patches.md`
   § patches (how a patch is produced and scoped per device).
2. `docs/reviews/plan-for-the-plan.md` (§ 2 on patches, § 4 Q6, § 5 on
   tables, § 6c on Local depth, § 8 on drift); `docs/reviews/order.md` § T40
   to § T43, § T23, § T24; this brief whole; the area futro
   `docs/futros/2026-10-25-m6-patches-and-configs.md`; T23's brief § 1 (the
   removal rule) and its `02-forward-audit.md` § Reachability on its branch.
3. `scripts/unpack` at `8ebaf8daad` (the patch directory list and
   `PATCH_ARCH`, lines 120-160), `config/functions` (`get_pkg_directory`,
   lines 1057-1092), `tools/renovation-inventory` (`selected_patch_dirs`
   382-401, the patch-row reach at 447-459, the `projects/<other>` rule
   455-456, the `patches` column 587-597), the Makefile's build lines.
4. The live M6 body; #687 (with its comments); #1054 (the epic, its futro
   comment); #339; #346 (the class decision as posted for T23); #1048;
   #670 and its retro; #671 (T24's hand-off); the register rows
   D-WORKFLOW-185, 187, 189, 198, 209.

## 4. The questions

The seven renovation questions of plan § 4, with **reachability** as the
lens and the table as the answer:

- **Q6 Dead ends -- the table.** One row per path (778): path, lines, kind,
  class (a to e2, or *deleted upstream*), the package unit and (for class d)
  T23's disposition of it, `shadowed_by`, the header's origin and subject
  with tag and series position, the first target, the upstream status
  (carried / deleted upstream since the base / a LibreELEC change the
  override lacks), and the disposition. The two commands for one quantity:
  the inventory's reach and the lane's own class script over `unpack`'s
  rules and T23's units; a row the script cannot class is a finding.
- **Q3 Bugs -- class (c).** Five patches under `patches/x86_64` in live
  recipes that `PATCH_ARCH=x86` never selects: vitaquake2-lr's x86 variant,
  never applied since `9f1fab30f6` (2025-07-13), four hunks different from
  the live `aarch64` one; EmulationStation's `cpugov.patch` (upstream
  `40fce2a089`, 2026-08-20), targeting `100-amd64-freqfunctions`, which the
  ROCKNIX `rocknix` package installs, with a copy-paste slip
  (`getAvailableGpuGovernors` calling `get_available_cpu_governors`) that has
  never compiled. The code trace is `scripts/unpack:127-128` plus the
  directory names; the fix is a rename to `patches/x86` and a corrected
  slip, **a packet after the maintainer's word, never this lane's edit**;
  the proof that the renamed patch applies and compiles is a package build's,
  an open item to test for the next image (D-QA-051). One `bug` for the
  five, or two (the emulator's and the interface's), with `Already
  written:` (nothing on a device: the patch never shipped) and the VM line.
- **Q1 Modernize -- the class decision, continued.** The 277 and the 234
  of (a) and (b) are the patches of code T23's #346 question covers (the
  dead generic tree) and of projects the fork never builds; T40's Q1
  paragraph states what dropping them would cost beside T23's (the same
  LibreELEC-merge conflict shape; 102 upstream commits reach these files
  since June through those merges) and recommends; the coordinator carries
  the counts to #346 beside T23's.
- **Q4 Package currency -- the 72.** The shadowed patches the live
  overrides build without, by package (glibc, ffmpeg, bluez, busybox,
  systemd, ...): each a lead for T41's or T42's row on that override, named
  with its subject; not answered here.
- **Q2 Standards:** the 14 header-less hand-made diffs (a patch without a
  `From:`/`Subject:` cannot say what it is for); a `patches/<arch>` directory
  naming an arch the build never names (the class (c) shape, generalised:
  grep every `patches/*/` directory name against the arches `unpack` can
  produce).
- **Q5 Efficiency:** none on a device; the reader's cost of 317,908 dead
  lines beside 440,000 live ones.
- **Q7 Clarity and structure:** the shape of the dead set in one section (a
  LibreELEC kernel tree the fork does not use; eight projects the fork does
  not build; the generic twins of ROCKNIX overrides).

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every cell cites a command's
   output (the inventory's row, the header line, `get_pkg_directory`'s
   answer, `git log`) or a file:line.
2. Mechanical evidence outranks reading: the inventory's reach is a claim;
   `unpack`'s directory list and `get_pkg_directory` are the evidence; a
   header is the patch's own claim about its origin, recorded as such.
3. **The bench is the host; no guest, no build, no plan, no network.**
   **Can this be done on the VM? Yes -- on the host, with no network at
   all:** the inventory, the headers, `config/options ""` and
   `get_pkg_directory` (no request), `scripts/unpack` read, `git log` and
   `git show`; whether a patch applies to a pinned source is a build step
   and is not run here (an open item). `tools/council/run invoke` is never
   run.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The runs, with what the coordinator read** (the lane runs each at stage A
in its worktree and records the exit, the wall time and the summary line;
`TMPDIR` under `/workspace/tmp/m6-t40/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-patches-dead-687
cd "$D"; export TMPDIR=/workspace/tmp/m6-t40/tmp; mkdir -p "$TMPDIR" .qa-scratch/t40
# which linux each device builds (no network; config/options makes no request)
for dev_arch in GENERIC_X64:x86_64 H700:aarch64 SM8550:aarch64 H700:arm SM8550:arm; do ( PROJECT=ROCKNIX DEVICE=${dev_arch%:*} ARCH=${dev_arch#*:}; . config/options "" >/dev/null 2>&1; printf '%s linux -> %s  PATCH_ARCH would be: %s\n' "$dev_arch" "$(get_pkg_directory linux)" "$( [ "$ARCH" = x86_64 ] && echo x86 || echo "$ARCH" )" ); done
# the Makefile's projects (expect 27 PROJECT=ROCKNIX, nothing else)
git show 8ebaf8daad:Makefile | grep -o 'PROJECT=[A-Za-z0-9_]*' | sort | uniq -c
# unpack's patch directories and PATCH_ARCH
git show 8ebaf8daad:scripts/unpack | sed -n '120,160p' | grep -n -E 'PATCH_ARCH|patches' | cut -c1-120
# the x86_64 directories under live recipes (class c; expect the five files)
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages | grep -E '/patches/x86_64/'
# the header coverage (expect 746 with From:+Subject:, 14 without)
n=0; h=0; while read -r p; do case "$p" in *.patch) n=$((n+1)); git show "8ebaf8daad:$p" | head -40 | grep -q -E '^Subject:' && h=$((h+1));; esac; done < .qa-scratch/t40/paths.txt; echo "patches $n with Subject: $h"
# T23's units, read from its branch, never checked out (expect 731)
git show feature/m6-packages-dead-ends-670:docs/audits/2026_10_25-epic-m6-generic-packages-dead-ends/02-forward-audit.md | awk '/^## Reachability/{p=1;next} /^## /{p=0} p' | grep -E '^\| `' | sed -E 's/^\| `([^`]+)`.*/\1/' > .qa-scratch/t40/t23-units.txt; wc -l < .qa-scratch/t40/t23-units.txt
# the six already deleted at upstream/next
while read -r p; do git cat-file -e "upstream/next:$p" 2>/dev/null || echo "DELETED-UPSTREAM $p"; done < .qa-scratch/t40/paths.txt | wc -l
# the removal rule's own check (expect empty) and the churn
git diff --stat 8ebaf8daad HEAD -- '*.patch' '*.conf' | tail -1
tr '\n' '\0' < .qa-scratch/t40/paths.txt | xargs -0 git log --oneline --since=2026-06-01 8ebaf8daad -- | wc -l    # 102, all upstream's
```

**The table's generator** is the lane's (`tools/t40-tables.py` in the audit
folder, as T23's `t23-tables.py`): it reads `inventory.json` with § 2's
filter, classes every row by `unpack`'s rules and T23's unit list, reads
each patch's header, and asserts the counts (778 rows, 760 and 18, the five
classes' sizes or a stated delta) so that a missing row fails there rather
than printing an empty cell. `02`'s coverage table (one row per path, 778)
and § Provenance (one row per path, 778, the full columns) come from the
same script.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#687`
(`Refs #687`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-patches-dead/00-running-log.md` | the flight recorder: model and effort, `reviewed-at` with `8ebaf8daad` and T23's `f1561559aa`, the host file's last line and census at stage A, every run with exit and wall time | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 778 re-derived with § 2's block, the five classes with their sizes, the header coverage, the six upstream-deleted, the 74 shadowed and the 2 duplicates | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #687's checklist; **§ Provenance: the 778-row table** (the § 4 Q6 columns); § Classes (the five, each with its rule and its count); § The x86_64 five (the code trace); § The shadowed 74 (the 2 duplicates; the 72 by override, each a T41/T42 lead); **a coverage table with one row per path under `## Coverage`** (778); § The runs; § Proofs with `proved:` cells | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: `unpack` x the inventory x T23's units x the overrides x the other projects x LibreELEC's merges | B |
| Analysis | `.../04-analysis.md` | Phase 4 § Finding Verification; **§ Renovation face Q1 to Q7, Q6 carrying the dispositions by class with counts summing to 778, Q1 the class paragraph for #346, Q4 the 72 by override, Q3 the bug**; § Instruction File Recommendations | B |
| Second opinions | `.../second-opinions/review-plan.json` | depth `local`, reviewers `[]`, the sentence *the lint and the counts are the check* | B |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where, acceptance, `Already written:`, the VM line; the YAML `punch_index`; the class decision deferred to #1048/#346, the 72 to T41/T42 by package | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #687 | `Audit: M6 T40 the patches no plan applies -- N findings (...)` | D |
| Bugs | GitHub, label `bug`, milestone M6 | the class (c) defect(s): the directory the build never selects, the trace, the slip, the open item for the next image's unpack log and compile | D |
| Retro | `docs/retros/<date>-m6-patches-dead.md`, posted on #687 | the mini-retro; what the slice did to the two time-to-play numbers (nothing); what T41, T42 and T43 inherit (the classes, the 72, the generator) | G |

## 7. Acceptance

The checklist on #687 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #687 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-patches-dead/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-patches-dead/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: local`, `reviewers: []` and the sentence *the lint and the counts are the check*; no `*.provenance.json` from a provider call exists in the folder (`ls second-opinions/ | grep -c provenance` is 0).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (the bug, #1048, a T41/T42 lead the coordinator files, or #346), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits; no `.patch`, `.conf`, recipe or tool changes on this branch by the lane: `git diff --stat <dispatch tip> <fixed-at> -- packages projects tools` is empty (D-WORKFLOW-209; the dispatch tip is the one the dispatch comment names).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (778 paths, 317,908 lines; 760 `.patch`, 18 `.conf`; 351 shadowed, 277 to the ROCKNIX linux), the five classes' sizes reproduced (277 / 234 / 5 / 234 / 28, summing to 778, or the delta with the command), the header coverage (746 with `From:`+`Subject:`, 14 without, named), the six upstream-deleted rows, the 102 upstream commits since 2026-06-01 and 0 fork-authored.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `778`.
- [ ] `02-forward-audit.md` § Provenance carries exactly 778 rows (``awk '/^## Provenance/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `778`), each with the § 4 Q6 columns, its class, its header's origin and subject (or `hand-made` for the 14), its upstream status and one of § 1's dispositions; the class (d) rows carry T23's disposition of their unit, read from T23's branch.
- [ ] `02-forward-audit.md` § The x86_64 five names the five files, quotes `scripts/unpack:127-128`, shows the four-hunk difference between vitaquake2-lr's `x86_64` and `aarch64` patches and the `cpugov.patch` slip, and the `bug` filed for them passes `tools/box-check --issue N` with its VM line (the trace on the host; the renamed patch's application and compile an open item for the next image).
- [ ] `02-forward-audit.md` § The shadowed 74 lists the 2 content duplicates by name and the 72 by override package with each patch's subject, each a lead for T41's or T42's row, none a removal.
- [ ] `02-forward-audit.md` § The runs records the five `get_pkg_directory linux` answers, the Makefile's project count, `unpack`'s directory lines, the x86_64 listing, the header count, T23's unit count (731, read from its branch), the upstream-deleted count and the churn, each with exit, wall time and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows no build, no guest, no compiler, no plan generation, no `curl` or fetch of any kind, no `tools/council/run invoke`, and no write under `/workspace/repos/rocknix*`, another lane's worktree or `/tmp`.
- [ ] `04-analysis.md` § Q6 carries the dispositions by class with counts summing to 778; § Q1 the class paragraph for the maintainer (the 277 and the 234 beside T23's 603 units, the LibreELEC-merge conflict shape, 102 upstream commits since June, the six already deleted), ending in the lane's recommendation and the sentence that the decision is the maintainer's; § Q4 the 72 by override.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`.
- [ ] The retro exists at `docs/retros/<date>-m6-patches-dead.md`, is posted on #687, says what the slice did to the two time-to-play numbers (nothing) and what T41, T42 and T43 inherit.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #687; a blocker named on #687 with what is needed; a branch that differs
from the dispatch tip under `packages/`, `projects/` or `tools/` at stage A;
or an execution limit, stated as such with the running log current. A
checkpoint is not a stop; a differing count is a delta; `next` moving is
drift. An idle session says it is idle on #687, **does not end a turn on a
post that asks nothing**, and **updates its session pointer at every
checkpoint** (#1014).

**What never runs in this slice:** a build, a package build, a compiler, a
guest, a plan generation, a fetch or any network use; `tools/council/run
invoke` or any provider call; any removal, rename or edit of a `.patch`, a
`.conf`, a recipe or a tool (D-WORKFLOW-209: the table records, the
maintainer decides, a fix is a packet); a checkout of T23's branch (it is
read with `git show`); a push to any branch but the lane's own;
`fork-worktree sync|remove|repair`; an edit to a rule, `CLAUDE.md`,
`AGENTS.md`, a decided register row or `.github/sessions/saved-session-state-next.md`;
a write under `/workspace/repos/rocknix*` or `/tmp` (use
`/workspace/tmp/m6-t40/`); a credential-shaped literal written anywhere;
`--no-verify`; bare `git stash`; `git worktree remove --force` or `rm -rf` on
a worktree or a bare variable path.

## 9. Ceremonies owed

- A work-log entry per session headed `#687`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #687` or the
  guard.
- The VM question written before any proof (§ 5: the host; no guest; no
  network).
- The mini-retro at stage G, posted on #687, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator.
- A register row the same session for any decision the slice forces; the
  next Decided ID is D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-033 or
  higher; it goes at the end of `## Decided`, and a row is never edited.
- The merge notes: when `next` moves, the **coordinator** merges `next`
  into this branch, never between stage A and stage D; the coordinator
  merges its own branch into this one at hand-back before the last
  criterion's checkers run; a merge with conflicts is checked for leftover
  markers before it is committed (#696), and the ledgers are united by
  whole entries.
- Commit messages `docs: ...` (this slice edits no tool and no patch), each
  with `Refs #687` and the attribution line; `git add -A` only after `git
  status --short` shows nothing a run left behind (`.qa-scratch/` is
  gitignored).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#687's checkboxes against their artifacts; the lint's `PASS` line; the
review plan (local, no reviewer, no provenance file); the audit issue's
checkboxes all at an outcome; the coverage table's row count (778) and the
provenance table's against § 2; **re-running on an export of the tip under
`/workspace/tmp`: the inventory block, the lane's generator (the class
sizes recomputed), the header count, the `get_pkg_directory` answers, the
Makefile count, the upstream-deleted count, the empty diffs under
`packages/`, `projects/` and `tools/` against the dispatch tip;**
`register-check` and `rules-check` on a simulated merge with the
coordinator's tip (the ledgers united; the archive carrying `projects/`);
the retro's answers. The lane posts one hand-back comment naming the tip
and each artifact by path, writes `reviewed-at:` and `fixed-at:` into
#687's body, then says it is idle. After acceptance the coordinator closes
the audit issue, prompts the lane for `audit-completion.json` and the full
lint, carries the Q1 paragraph and the counts to #346 beside T23's, routes
the class (c) fix as a packet after the maintainer's word, merges the
branch in its turn after the M7 candidate (after T23's, before T9's), and
closes #687 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#1054) carries this slice's kickoff, and a stranger's proof of this brief
is run by a reader with no context before dispatch; version 2 records what
each found.

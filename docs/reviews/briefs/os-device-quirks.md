# Brief: M6.P2 T29, the per-handheld quirks (#676)

**Version 2, 2026-10-25, the coordinator's** (D-WORKFLOW-189; version 1 the same day, corrected by a stranger's proof -- twelve corrections, listed at the end). Written from a read-only research digest taken at `2174265e9c` (P1's tip; for these 333
paths the same bytes as `next` at `8ebaf8daad`) and from T22's brief, the
model of a slice in the OS area, whose retro hands this one its selection
lines and run order. The stranger's proof of version 1 ran before dispatch (ten commands, from the scratch clone); this version records what it found. Every number below was pasted from a command's
output at the hash named beside it; the lane re-derives each one and writes
the delta where it differs.

## 1. Identity

- **Issue:** #676 `M6.P2 E695/T29: os-scripts-and-launch: the per-handheld quirks` (retitled and re-parented under #695 on 2026-10-25 at 11:2x, before dispatch; it carried `E339` until then; its body's P1 VM line, *every behaviour claim proven on the GENERIC_X64 guest*, is replaced at dispatch by § 5's answer), slice `os-device-quirks` (`k: 29`) in
  `docs/reviews/slices.json` (one `select` rule: the glob
  `projects/ROCKNIX/packages/hardware/quirks/devices/**`; the area and
  reach filters are inert: the glob alone selects the same 333),
  twenty-ninth in `docs/reviews/order.md` (its § T29 paths line: *"333
  paths, 10,175 lines, 9,327 read, of which 389 fork-own; 0 patch and
  config lines; reach shipped 333"*; its `why`: *"333 files over 88
  handheld models, all installed with the quirks package: the slice first
  derives which model directories the shipped pair (H700, SM8550) and the
  VM select at run time"*; kind currency; lens brittleness). **Epic:** #695 (the OS area: T1 #648 and T22 #669 accepted and closed out; this slice; #695's table cell for T29 said `quirks/**`, wider than the glob, and was corrected to the glob on 2026-10-25 -- the glob is the membership).
  **Milestone:** M6. **Predecessors:** #346, #641, **T22 #669**
  (`os-system-services.md`; its audit's `02` § The reachability table and
  § The units on `feature/m6-os-system-services-669`; its retro's *What T29
  inherits*: the selection lines, the boot order proven on the guest, the
  *runs on* column, the VM's `QUIRK_DEVICE`), **T1 #648** (`rocknix-info`,
  which derives `QUIRK_DEVICE` a second way), **T27 #674** and **T28 #675**
  (the two shipped devices' trees, whose `model` strings are the keys this
  slice matches), **T11 #658** (the VM's device), the Backlog **#1100**
  (no runbook section for the Nova) and the bug pair **#1095 / #1109** (the
  updaters' shared contract). **Beside it:** T16 in the T1 session, T15's
  close-out in the T3 session (D-WORKFLOW-190); neither shares a path with
  this slice.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346 or #585, or decide a question of scope:
  those are the coordinator's, reached through #676, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already
  written:` line (D-WORKFLOW-187). A fix lands only under a stream brief
  the coordinator writes at the stage-D pause. **Removal is never proposed
  for an upstream-carried unit** (D-WORKFLOW-209: 328 of the 333 are
  upstream's); the five fork-own files are the fork's to fix.
- **One worktree, one session.** Branch `feature/m6-os-device-quirks-676`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (`docs/reviews/{order.md,slices.json,inventory.json,status.md}`
  are there and on no other branch) with the coordinator's tip merged in
  (the briefs, the OS futro with its T29 addendum, the rules edited today)
  and the lane's pointer seeded; the two hashes are in the dispatch
  comment on #676. Until that comment exists the pointer is not seeded,
  the first command's `cat` fails, and nothing starts. The session is the
  one the dispatch comment names (the T5 lane after T28's close-out is the
  likely one; its earlier worktrees stay idle beside this one, read with
  `git show` only; T22's audit is on `feature/m6-os-system-services-669`).
- **Depth: Independent** -- one seat, GPT-6 Astra at `max`, over a trimmed
  packet (D-WORKFLOW-195: scanned with `tools/forbidden-terms-check
  --stdin`, the pre-commit patterns and T10's widened set read with `git
  show feature/m6-tooling-guards-657:.githooks/secret-patterns`, a manifest
  with sha256s), a probe first, as T28's stage C; `review-plan.json`
  records depth `independent`, one reviewer; **exactly one keyed invoke
  pair**, every other `tools/council/run` call with
  `COUNCIL_ENV_FILE=/nonexistent`, `--help` included. Every seat item is
  re-read at its lines before it is graded.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676
cat .github/sessions/saved-session-state-feature-m6-os-device-quirks-676.md    # the pointer: the dispatch's two hashes
git status --short | wc -l                                                      # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects tools | tail -1            # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
git show feature/m6-os-system-services-669:docs/audits/2026_10_25-epic-m6-os-system-services/02-forward-audit.md | grep -c '^| '   # T22's tables are reachable
tools/register-check >/dev/null && echo register-ok
```

## 2. Scope

**The membership block** (T22's shape over the inventory; one glob, no
exclusion):

```bash
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
P = "projects/ROCKNIX/packages/hardware/quirks/devices/"
t29 = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith(P)]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t29), "lines", L(t29), dict(collections.Counter(r["reach"] for r in t29)), dict(collections.Counter(r["tier"] for r in t29)), dict(collections.Counter(r["area"] for r in t29)))
print(dict(collections.Counter(r["language"] for r in t29)))
rd = [r for r in t29 if r["language"] == "shell"]
print("read", len(rd), L(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"), "fork-own paths", [r["path"][len(P):] for r in t29 if r["tier"] == "fork-own"])
ent = collections.defaultdict(lambda: [0, 0, 0])
for r in t29:
    e = r["path"][len(P):].split("/")[0]; ent[e][0] += 1; ent[e][1] += r["lines"] or 0; ent[e][2] += (r["tier"] == "fork-own")
print("entries", len(ent), "of which top-level symlinks", sum(1 for r in t29 if r["language"] == "symlink" and "/" not in r["path"][len(P):]))
os.makedirs(".qa-scratch/t29", exist_ok=True)
open(".qa-scratch/t29/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t29, key=lambda r: r["path"])))
open(".qa-scratch/t29/entries.tsv", "w").write("".join("%s\t%d\t%d\t%d\n" % (e, v[0], v[1], v[2]) for e, v in sorted(ent.items())))
PY
wc -l .qa-scratch/t29/paths.txt .qa-scratch/t29/entries.tsv     # 333, 88
```

Recorded (2026-10-25, at `2174265e9c`; the inventory there was generated at
`eb4763e3cc`): **333 paths, 10,175 lines; shipped 333; upstream-carried
328, fork-own 5; read 266 shell files / 9,327 lines, 389 of them fork-own**;
languages shell 266, symlink 48, none 12, other 7 (the 848 unread lines are
the 48 one-line symlinks, 12 `none` and 7 `other`); every row
`reachable_by` all three builds, because `quirks/package.mk:15` copies
every `devices/*` into every image. **88 top-level entries = 65 model
directories + 23 alias symlinks** (the order's *88 handheld models*); 25 more symlinks sit inside directories (shared files, the lane's table completes them: `Pocket DMG`'s and `Pocket EVO`'s → `Pocket ACE`'s, their `bin/achievements` → `AYN Odin 2`'s; `Pocket DS` two → `Pocket ACE`'s; `RG DS Plus` → `RG DS`'s `bin/`, `sleep.d/` and four files; `RG40XX H`'s and `V`'s `bin/achievements` → `CubeXX`'s; `RGB10` → `OGA BE`'s; `ARC-S` → `ARC-D`'s). The 23 aliases: eleven `AYANEO`-prefixed names and `AYA NEO AYA NEO Founder` → `AYANEO AIR`, `AYANEO Pocket S Mini` → `Pocket S 2K`, `Anbernic RG353M` → `RG353P` (the maintainer's RK3566 unit, unshipped), and the rest as the lane's table lists them.

**Run-time selection, the slice's first derivation** (the lines are
T22's, cited): `002-autostart:6-12` sets `QUIRK_DEVICE` from the device
tree's `model` (`strings /sys/firmware/devicetree/base/model`), else from
DMI (`sys_vendor product_name`), with `/` → `-`; `autostart:31-43` runs,
as root and in glob order, **only the files directly in
`devices/${QUIRK_DEVICE}/`** (`:38`'s `-f` skips `bin/`, `sleep.d/`,
`remappings/`, `touchcontrol/`); the `bin/` helpers are reached through
T22's wrappers (`system-utils/sources/scripts/{ledcontrol,analog_sticks_ledcontrol,battery_led_status,fancontrol}:14-17`,
which `exec` the device's `bin/<name> $*`, unquoted, else the platform's),
called by the platform quirks, the LED units, `powerstate.sh` and
`sleep.sh`; `bin/achievements` through `retroarch/scripts/call_achievements_hooks.sh:14-17`;
`020-configs:18-22` would rsync a `devices/<model>/config/` that no
directory has (T22's G-35). **A second derivation lives in `rocknix-info:8-10`** (T1's file: `tr -d '\0'` over the dt `model`, with its own DMI fallback at `:10`, and no `/` → `-`): a lead for the coordinator, cited not read.

**Which directories the shipped units and the VM select.** The dt `model`
strings at `8ebaf8daad`: the H700's two owned units are `Anbernic RG35XX
SP` (from `devices/H700/patches/linux/0154-rocknix-dt-id.patch:39`; **the
tree has no `sun50i-h700-anbernic-rg35xx-sp.dts`** -- its `-v2-panel.dts`
includes the kernel's and sets no model) and `Anbernic RG-SP`
(`sun50i-h700-anbernic-rg-sp.dts:10`); the Nova is `Retroid Pocket Nova`
(`qcs8550-retroidpocket-rpnova.dts:11`); the VM is the DMI pair `QEMU Standard PC (Q35 + ICH9, 2009)` (T22's guest). The two trees carry 29 `model =` strings in all (one a sub-node, `qcs8550-ayn-thor.dts:358 "AYN-Thor"`, not a board); of the 28 boards, **no `devices/` entry exists for `Anbernic RG35XX SP`, `Anbernic RG-SP`, nor for RG28XX, RG34XX, RG34XX-SP, RG35XX Pro, RG35XX H, RG35XX Plus, RG35XX 2024, AYANEO Pocket S 1K or AYN Odin 2 Mini: on both of the maintainer's H700 units no device quirk runs**, only `platforms/H700/*` (T22's). So the selection has two honest tiers,
and the lane records both:

| Tier | What | Paths | Lines | Fork-own |
| --- | --- | ---: | ---: | ---: |
| A: the units the maintainer owns, and the VM | `Retroid Pocket Nova/` (4 files), `QEMU Standard PC (Q35 + ICH9, 2009)/` (2) | 6 | 396 | 5 |
| B: every board the H700 and SM8550 images boot that has an entry, and the VM (14 directories and 2 aliases) | H700: `RG40XX H`, `RG40XX V`, `CubeXX` (7 / 190); SM8550: `Pocket ACE`, `DMG`, `DS`, `EVO`, `S 2K`, `S Mini` (alias), `Odin 2`, `Odin 2 Portal`, `Thor`, `Retroid Pocket 6`, `RP6 TOP-DPAD` (alias), `Nova` (61 / 2,569, fork-own 3); the VM (2 / 126) | 70 | 2,885 | 5 |
| the rest, selected by no board a shipped image boots | 51 directories and 21 aliases | 263 | 7,290 | 0 |

**The read is tier B line by line** (the order's *"the shipped pair ...
select at run time"* names the images, not the units) **and tier A twice**:
the Nova's four files and the VM's two are also read against the device
facts and the fixture; the rest is read by its table row (name, files,
lines, the run-order prefixes, the shared files, the flags it sets, the
sysfs paths it writes), not line by line. The fact that the owned H700
units select nothing is a finding in its own right (Q7, Q3: is a quirk
missing for the RG35XX SP or the RG-SP, or is the platform set complete by
upstream's design? -- read `platforms/H700/*`'s coverage by name, cite
T22's rows, and ask nothing of a unit).

**Fork-own (389 lines, 5 files).** The fork's commits since the base: **6 over the 333 paths** (`git log --no-merges c445081a59..8ebaf8daad -- <the paths>`), **9 over the directory** (three of the nine touched QEMU quirks since deleted: `bccbf54cd4`, `a9d97acf80`, `8bb74015e6`); since `2026-06-01T00:00:00Z` on `8ebaf8daad`: **28 non-merge over the 333, 6 the fork's; 32 over the directory, 9 the fork's and 23 upstream's**. Every figure names its population. `QEMU .../001-device_config` (29; `73b20caf86` 2026-06-30: the
VM's fourteen `DEVICE_*` flags, rewritten every boot),
`QEMU .../091-retired-vm-fixes` (97; `518aeffca5` 2026-09-28: the take-back
of retired quirks' leftovers under `/storage` by sha256, two stamps under
`/storage/.cache/`), and the Nova's `bin/{analog_sticks_ledcontrol 45,
battery_led_status 135, ledcontrol 83}` (`a3d617ff54` 2026-10-03,
`8ee3d9dfe6` #332: `ledcontrol` writes `set_setting led.color` and
`led.brightness`; the three take `LED_PATH` and `BATTERY_PATH` overrides,
which `tools/nova-led-test` uses). The Nova's fourth file, `010-analog_sticks_led_control` (7 lines, upstream's; the same 7-line file in 13 directories, twelve identical blobs and `RG Vita Pro`'s differing in its copyright line), is the only Nova file the autostart loop runs; the `bin/`
helpers are reached through the wrappers. Upstream has not touched the
Nova's directory since the base: no collision on the three fork-own `M`
rows. **Modes:** 71 files are `100644` (the Nova's four among them),
masked by `package.mk:20`'s `chmod -R 0755` at install.

**The upstream delta.** The delta `git diff --name-status 8ebaf8daad 651150fc88 -- <dir>` (upstream's
direction): **16 A, 3 D, 12 M**; among the 16 A two serve SM8550 boards the
shipped image boots (`AYN Thor/040-panel_calibration`, `Retroid Pocket
6/040-panel_calibration`) and two are new models (`Retroid Pocket Duo
Lite`, 7 files; `Retroid Pocket Classic 6 Rev Q`, 3); the 3 D are the two
QEMU files upstream never had and `RG DS/050-game_configs` (a real
deletion); the 12 M are the Nova's three (the fork's edits) and nine upstream changes to directories outside tier A. **18 upstream commits are pending** on the directory (12 without merges) (the ten most recent: Thor, RP6 and Odin 3 panel
calibration; the rk3566 inputplumber port; RG DS touch; Yabadabadoo; the RP
Classic 6 Rev Q). Every one of them is *settled by the next base merge*;
the two for shipped boards are the slice's currency finding.

**The scripts' shape, tree-wide** (a path-safe tally over the 285 blobs, 266 of them shell; § 5's block; the lane re-counts each and names the population): shebangs `#!/bin/sh` 256 and `#!/bin/bash` 10 (`/bin/sh` is bash on the image, T1's finding); 89 source `/etc/profile`; 46 call `set_setting`; 156 of the 285 touch `/storage` (145 of the 266 shell); **32 write into `/sys`**; 104 define `DEVICE_*` flags (101 of the shell); **one file in 285 guards a `/sys` path with a test before using it** (`Powkiddy x55/040-hdmi:6,11`, `[ -f "/sys/..."`, found by § 5's pattern, which admits the quote; the proof's unquoted pattern found none); the common pattern is *root rewrites `/storage/.config/profile.d/<n>` with a heredoc every boot, then a `bin/` helper reads settings and writes sysfs*; two spellings of one file name across the tree (`050-game-configs` 16, `050-game_configs` 12; no directory has both, tier B has one spelling in 4 files, 7 of the 28 are language `none`); `Powkiddy RGB30/001-detect-device` greps a hard-wired `/sys/devices/platform/fe000000.mmc/...` path.

**What the VM can prove.** The VM's own two files run on every guest boot
(a proof of the control flow, D-QA-053); another model's directory can be
*run* by hand on the guest as root with `QUIRK_DEVICE` exported, but is
*selected* only if DMI matches (a `-smbios type=1` profile question for
`tools/generic-x64-vm`, and the sysfs nodes would still be absent); **the
Nova's helpers already have a host fixture**, `tools/nova-led-test` (68
lines: the actual scripts under `LED_PATH`, `BATTERY_PATH`, `QA_ROOT`,
`QA_SETTINGS`; `docs/qa-logs/2026-10-03-led/`), which is the proof shape
for any `bin/` helper. **No guest cycle is planned**: a boot-only behaviour
the lane names on #676 can ask for one. The device facts that bear on this
slice (`docs/releases/device-facts.md` at `2174265e9c`, named by their Fact
cells and lines): line 14 (the RG SP's power LED at high charge), 16 (the
H700 boot on the RG SP), 27 (the Nova), 31 (the Nova's stick LEDs: the VM
proves eight sysfs writes; the illumination an open item to test, #332;
D-UI-121). Nothing runs on a unit (D-QA-015).

**What is not here, and where it is:** `quirks/package.mk`,
`quirks/autostart/*`, `quirks/profile.d/999-export`, `quirks/system.d/*`,
`quirks/platforms/**` (15 directories, 264 files), `/usr/bin/autostart`,
`002-autostart`, the four wrappers, `powerstate.sh`, `sleep.sh` -- all
T22's (#669), cited by line; `rocknix-info` and `rocknix-fake-suspend`
(T1's); `call_achievements_hooks.sh` (the RetroArch package's); the device
trees and `0154-rocknix-dt-id.patch` (T27's, T28's, T41's).

## 3. Read first

- `.github/sessions/saved-session-state-next.md` and this lane's own pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight):
  `engineering-practices.md` (§ Verify the artifact; § A name is not a
  behaviour; § Guards must fail closed; § Nothing runs on a person's
  device without their yes), `handheld-evidence.md` (what survives what;
  testing it on the VM), `generic-x64-vm-testing.md` (the guest's
  `QUIRK_DEVICE`; the image is the candidate, not the read tree; the
  credential filter -- **which drops any script line carrying `user` or
  `key`, so a count over these scripts is taken unfiltered and only a
  quoted line goes through the mask**), `upgrade-and-install.md`
  (`Already written:` -- every-boot heredoc rewrites are what a device
  already has), `bugs-are-agent-first.md`, `issue-tracking.md`,
  `vm-first.md`, `adversarial-council.md`, `council-substrate-integrity.md`,
  `worktrees.md` (superseded by § 1).
- The code-auditor skill whole; *the plan* is `docs/reviews/plan-for-the-plan.md`
  (§ 4 the questions, § 6b the renovation face, § 6c the depth rule).
- **T22's audit** (`git show feature/m6-os-system-services-669:docs/audits/2026_10_25-epic-m6-os-system-services/<file>`):
  `02-forward-audit.md` § The reachability table (the *runs on* column:
  `rows 422 / platform files 264 / run on no shipped device 213 / runs on
  none 225`), § The units (`led-poweroff`, `batteryledstatus`, `fancontrol`,
  `powerstate`), § The guest cycle (the boot order proven: platform
  quirks, device quirks, `common/*`, `/usr/lib/autostart/${HW_DEVICE}`,
  then `/storage/.config/autostart/*`, all as root); its `tools/t22-reach.py`
  (a generator that asserts its counts). **T27's and T28's audits** (`git
  show feature/m6-device-h700-674:...`, `git show feature/m6-device-sm8550-675:...`):
  § The device trees (the `model` lines).
- `docs/reviews/order.md` § T29 and § T22; `docs/futros/2026-10-23-m6-os-scripts-and-launch.md`
  (its T29 kickoff addendum).
- `tools/nova-led-test` and `docs/qa-logs/2026-10-03-led/` (the fixture
  shape for a `bin/` helper); `docs/releases/device-facts.md` lines 14, 16,
  27, 31.
- Decisions: D-WORKFLOW-185 (the shipped pair and the VM decide the
  run-time derivation; RK3566/RK3326 the first widening -- the RG353M's
  alias is a row, not a device), D-QA-015, D-QA-027 (the RG35XX SP is the
  QA handheld -- and selects no quirk), D-QA-042, D-QA-053 (the VM is a
  developer's tool), D-UI-121 (#332's LED behaviour), D-WORKFLOW-187, 189,
  195, 209.
- Issues: #676, #695, #669, #648, #674, #675, #658, #332, #1100, #1095,
  #1109, #585, #346. Every `gh` call carries `--repo pixelelated/distribution`.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`design`); the lens is brittleness under currency, so Q2 and Q3 lead over
tier B and Q6 carries the table:

- **Q2 Standards -- the lead question, over tier B.** For each of the 70
  files: the unguarded sysfs writes (one guard in 266 files; 32 writers),
  the every-boot heredoc rewrite of `/storage/.config/profile.d/<n>` as
  root (what it overwrites if a person edited it), the unquoted `$*` the
  wrappers hand down (T22's files; the helpers' side is this slice's: do
  they quote what they receive?), the 71 `100644` modes against the install's `chmod -R 0755`, a hard-wired sysfs path (`RGB30`'s is outside tier B;
  the tier's own are the finding), a setting written where a flag was
  meant, a helper that reads a setting the interface never writes
  (D-UI-121's brightness row). Tree-wide counts are stated for the 333 and
  the findings are tier B's.
- **Q3 Bugs.** A defect in the five fork-own files (the VM's two: the flags
  and the take-back by sha256; the Nova's three: #332's LED behaviour
  against D-UI-121, the brightness row that does nothing on that device,
  a colour applied only on a change) is a `bug` with its trace, its
  `Already written:` line (what every boot has rewritten under
  `/storage/.config/profile.d/` and `/storage/.cache/`) and its VM line
  (`tools/nova-led-test`'s fixture or a guest boot); a defect in an
  upstream-carried tier-B file is a `bug` only when the fix is contained
  and the proof is a host fixture (rule 6 of `bugs-are-agent-first.md`),
  else a #585 line. **The owned H700 units select no device quirk**: read
  `platforms/H700/*` by name against what `RG40XX`'s and `CubeXX`'s
  entries add, and say whether anything an RG35XX SP or RG-SP needs is in
  a device entry it never reaches -- a finding with the files named, no
  unit asked.
- **Q4 Currency.** The 18 upstream commits pending on the directory (12 without merges): the two panel-calibration files for shipped boards (Thor, RP6) as the currency finding, *settled by the next base merge*; the Nova's three fork-own `M` rows with no upstream change behind them (no collision); `rocknix-info:8-10`'s second `QUIRK_DEVICE` derivation (T1's file; a lead for the coordinator, cited).
- **Q1 Modernize.** The pattern as a design: a flag file rewritten every
  boot against a once-written one; a helper dispatch by directory name
  against a declared capability; the alias symlinks (23) against a table
  -- each a sentence for the coordinator, no edit.
- **Q5 Efficiency.** The 333 by tier (6 / 70 / 263 paths; 396 / 2,885 /
  7,290 lines); the 263 carried by placement (D-WORKFLOW-185: a row each,
  not a removal); the bytes `package.mk:15` copies into every image.
- **Q6 Dead ends -- the table.** One row per top-level entry (88 = 65
  directories + 23 aliases; an alias row names its target; the 25
  in-directory symlinks as shared-file notes on the target's row), each
  with files, lines, fork-own, the tier, the flags it sets, the run-order
  prefixes, the boards' `model` string where one is in the tree, and the
  disposition in D-WORKFLOW-209's words (*selected by a shipped unit or
  the VM*; *selected by a board a shipped image boots*; *carried by
  placement*; *alias of <target>*). **Generated by a script under the audit
  folder's `tools/` that asserts 333 / 88 / 65 / 23** (T25's practice).
  Removals none.
- **Q7 Clarity.** Can a reader tell from the directory which model string
  selects which entry, that the owned H700 units select none, that `bin/`
  is reached by wrappers and not by the loop, and that a directory's name must equal the dt `model` with `/` → `-`? The alias table and the selection paragraph are the answer; the two spellings of `050-game*configs` are a naming inconsistency recorded here, not a run-order question; #1100's runbook section is where the Nova's goes.

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seat (Phase 4.6) grades the
findings and the dispositions; its probe comes first.

## 5. The evidence floor

1. Tracker state is never sole evidence; every cell cites a command's
   output or a file:line at `8ebaf8daad`.
2. Mechanical evidence outranks reading: `git grep -n` over the 266, the
   `model` lines, `git cat-file -e` for an entry's existence, `git log`
   with the three fork identities; a comment is the author's claim
   (blindspot 31).
3. **The bench is the host; no guest is planned, no unit.** **Can this be
   done on the VM? Yes -- on the host, with no network:** every read and
   count runs on the build host at `8ebaf8daad` with `651150fc88` read
   locally; a `bin/` helper's behaviour is proven with `tools/nova-led-test`'s
   fixture shape (sysfs under a scratch root), never on the Nova; the VM's
   two files' control flow is T22's guest record, cited; a boot-only
   behaviour the lane names can ask for one window on #676. Nothing runs
   on a person's device (D-QA-015; the RG35XX SP is the QA handheld,
   D-QA-027, and still asked nothing here). `tools/council/run invoke` runs
   twice with the key, the one seat's probe and refutation.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.
5. **A count over these scripts is taken unfiltered** (the credential
   filter drops a line with `user` or `key` in it -- a `keyboard` comment,
   a `KEY_` constant); only a quoted line goes through the mask, and no
   quoted line is config-shaped here.

**What never runs in this slice:** a build, a compiler, a plan generation,
a fetch, a network read of any upstream, a guest outside a window granted
on #676 (none is planned), a command against a handheld, a read of an M7
build root, a `tools/council/run` call with the key beyond the one seat's
pair, and a change to any file under `packages/`, `projects/` or `tools/`
at stages A to D.

**The runs, with what the coordinator read** (the lane runs each at stage
A and records the exit, the wall time and the summary line; `TMPDIR` under
`/workspace/tmp/m6-t29/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676
cd "$D"; export TMPDIR=/workspace/tmp/m6-t29/tmp; mkdir -p "$TMPDIR" .qa-scratch/t29
Q=projects/ROCKNIX/packages/hardware/quirks/devices
# the membership block (§ 2) -> .qa-scratch/t29/{paths.txt,entries.tsv} (333, 88)
wc -l < .qa-scratch/t29/paths.txt; wc -l < .qa-scratch/t29/entries.tsv                                   # 333 88
tr '\n' '\0' < .qa-scratch/t29/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1          # empty
git ls-tree --name-only 8ebaf8daad -- "$Q/" | wc -l; git ls-tree 8ebaf8daad -- "$Q/" | grep -c '^120000'   # 88 23
git ls-tree -r 8ebaf8daad -- "$Q/" | grep -c '^120000'                                                     # 48 (23 top-level + 25 inside)
# the selection lines (T22's files, cited)
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart | sed -n '6,12p' | cut -c1-120
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart | sed -n '31,43p' | grep -n -E 'devices|-f ' | cut -c1-120
git show 8ebaf8daad:projects/ROCKNIX/packages/hardware/quirks/package.mk | sed -n '15,20p' | cut -c1-120   # :15 copies every devices/*; :20 chmod -R 0755
git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/ledcontrol | sed -n '14,17p' | cut -c1-120   # the wrapper's exec
# the model strings and which have an entry (expect: RG35XX SP and RG-SP NONE; Nova HAS; the DMI pair HAS)
git grep -n -E '^\s*model = ' 8ebaf8daad -- 'projects/ROCKNIX/devices/H700/linux/dts/allwinner/*.dts' 'projects/ROCKNIX/devices/SM8550/linux/dts/qcom/*.dts' | sed 's/^8ebaf8daad://' | cut -c1-120
git show 8ebaf8daad:projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch | grep -n 'RG35XX' | head -4 | cut -c1-100
git grep -h -E '^\s*model = ' 8ebaf8daad -- 'projects/ROCKNIX/devices/H700/linux/dts/allwinner/*.dts' 'projects/ROCKNIX/devices/SM8550/linux/dts/qcom/*.dts' | sed -E 's/.*model = "([^"]*)".*/\1/' | sort -u | while IFS= read -r m; do printf '%s: ' "$m"; git cat-file -e "8ebaf8daad:$Q/$m" 2>/dev/null && echo HAS || echo NONE; done   # 28 boards and the AYN-Thor sub-node; the owned H700 units NONE
printf '%s: ' 'QEMU Standard PC (Q35 + ICH9, 2009)'; git cat-file -e "8ebaf8daad:$Q/QEMU Standard PC (Q35 + ICH9, 2009)" && echo HAS
# the tiers (expect A 6 / 396 / 5; B 70 / 2885 / 5; the rest 263)
python3 -I - <<'PY'
import json
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
P = "projects/ROCKNIX/packages/hardware/quirks/devices/"
t = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith(P)]
A = ["Retroid Pocket Nova", "QEMU Standard PC (Q35 + ICH9, 2009)"]
B = A + ["Anbernic RG40XX H", "Anbernic RG40XX V", "Anbernic RG CubeXX", "AYANEO Pocket ACE", "AYANEO Pocket DMG", "AYANEO Pocket DS", "AYANEO Pocket EVO", "AYANEO Pocket S 2K", "AYANEO Pocket S Mini", "AYN Odin 2", "AYN Odin 2 Portal", "AYN Thor", "Retroid Pocket 6", "Retroid Pocket 6 TOP-DPAD"]
def tally(names):
    s = [r for r in t if r["path"][len(P):].split("/")[0] in names]
    return len(s), sum(r["lines"] or 0 for r in s), sum(1 for r in s if r["tier"] == "fork-own")
print("A", tally(A)); print("B", tally(B)); print("rest", len(t) - tally(B)[0])
PY
# the fork's commits, over the 333 paths (expect 6 since the base; 28 since June, 6 fork) and over the directory (expect 9; 32, 9 fork)
tr '\n' '\0' < .qa-scratch/t29/paths.txt | xargs -0 git log --no-merges --format='%h %ad %an %s' --date=short c445081a59..8ebaf8daad -- | wc -l
tr '\n' '\0' < .qa-scratch/t29/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- > "$TMPDIR/hist.txt"; wc -l < "$TMPDIR/hist.txt"; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"
git log --no-merges --format=%h c445081a59..8ebaf8daad -- "$Q" | wc -l; git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- "$Q" > "$TMPDIR/hist-dir.txt"; wc -l < "$TMPDIR/hist-dir.txt"; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist-dir.txt"
# the upstream delta (expect 16 A 3 D 12 M in upstream's direction; 18 commits pending, 12 without merges)
git diff --name-status 8ebaf8daad 651150fc88 -- "$Q" | awk '{print $1}' | sort | uniq -c; git log --oneline 8ebaf8daad..651150fc88 -- "$Q" | wc -l; git log --no-merges --oneline 8ebaf8daad..651150fc88 -- "$Q" | wc -l
git diff --name-status 8ebaf8daad 651150fc88 -- "$Q" | grep -E '^A' | grep -E 'Thor|Retroid Pocket 6/' | cut -c1-100   # the two for shipped boards
# the tree-wide shape, path-safe (paths carry spaces: never awk's $4; expect over the 285 blobs / the 266 shell: sh 256 bash 10; /etc/profile 89; set_setting 46; /storage 156 / 145; /sys writers 32; DEVICE_ 104 / 101; guard 1, the x55's 040-hdmi; modes 100644 71, 100755 214, 120000 48)
python3 -I - <<'PY'
import subprocess, re, collections
Q = "projects/ROCKNIX/packages/hardware/quirks/devices"
out = subprocess.run(["git", "ls-tree", "-r", "-z", "8ebaf8daad", "--", Q], capture_output=True, text=True, check=True).stdout
modes = collections.Counter(); blobs = []
for ent in out.split("\0"):
    if not ent: continue
    meta, path = ent.split("\t", 1); mode, typ, oid = meta.split()
    modes[mode] += 1
    if mode in ("100644", "100755"): blobs.append((path, oid))
print("modes", dict(modes), "blobs", len(blobs))
pats = {"/etc/profile": r"\. /etc/profile", "set_setting": r"set_setting", "/storage": r"/storage", "/sys writers": r"> */sys|tee /sys", "DEVICE_": r"DEVICE_[A-Z_]+=", "guard": r"\[ -[efd] \"?/(sys|dev)"}
she = collections.Counter(); hits = collections.Counter(); hits_sh = collections.Counter(); nsh = 0
for path, oid in blobs:
    body = subprocess.run(["git", "cat-file", "-p", oid], capture_output=True, text=True).stdout
    first = body.split("\n", 1)[0]; is_sh = first.startswith("#!")
    if is_sh: she[first] += 1; nsh += 1
    for k, rx in pats.items():
        if re.search(rx, body): hits[k] += 1; hits_sh[k] += is_sh
print("shebangs", she.most_common(3), "shell files", nsh)
print("over the blobs", dict(hits)); print("over the shell", dict(hits_sh))
PY
git ls-tree -r --name-only 8ebaf8daad -- "$Q" | grep -c -E '050-game-configs$'; git ls-tree -r --name-only 8ebaf8daad -- "$Q" | grep -c -E '050-game_configs$'   # 16 12
# the fixture that exists (expect tools/nova-led-test 68 lines naming the Nova's bin)
git show 8ebaf8daad:tools/nova-led-test | wc -l; git show 8ebaf8daad:tools/nova-led-test | grep -n -E 'devices/Retroid Pocket Nova/bin|LED_PATH|BATTERY_PATH' | head -4 | cut -c1-100
# the removal rule's own check against the dispatch tip (expect empty)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1
```

## 6. Outputs

As T22's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-os-device-quirks/`:
`00` to `05`, `second-opinions/` (the seat's plan, manifest, probe and
refutation with provenance), the lint before D, the audit issue (`Audit:
M6 T29 the per-handheld quirks -- N findings (...)`, a sub-issue of #676),
the bugs, and the retro at `docs/retros/<date>-m6-os-device-quirks.md`
(**what the slice did to the two time-to-play numbers**: nothing unless a
fix lands on a boot path -- say which; **what the OS epic's close
inherits**: the selection map, the tier table). **`02` carries § Coverage
(333), § The entries (the 88-row table, generated), § The selection (the
model strings, the entries they select, the two owned H700 units'
absence), § The tiers (A, B, the rest), § The fork-own five (each read
whole against #332 and D-UI-121), § The shape (the tree-wide counts),
§ The upstream delta (the 31 names and the 18 commits, the two for shipped
boards), § The runs (every § 5 command with exit, wall time, figure and *a
FAIL would mean*), § Positives, and every proof with `proved:`.** The
stage-D pause as T22's: the punch list posted on #676, the lane waits for
the coordinator's dispositions and any stream brief.

## 7. Acceptance

The checklist on #676 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-os-device-quirks/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-os-device-quirks/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); the probe's and the refutation's outputs have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named; `packet-manifest.json` lists every packet file with its sha256 and the scan's result (0 hits).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #1100, #332, T1's #648, T22's #669), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by the coordinator.
- [ ] `reviewed-at:` and `fixed-at:` in the checklist's header carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 333 (``tr '\n' '\0' < .qa-scratch/t29/paths.txt | xargs -0 git diff --stat 8ebaf8daad <reviewed-at> --`` empty -- the paths carry spaces, so never `$(cat ...)`) and nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (333 paths, 10,175 lines; read 266 / 9,327, fork-own 389 in 5; shipped 333; 88 entries = 65 + 23; 48 symlinks in all), the tiers (6 / 396 / 5; 70 / 2,885 / 5; the rest 263 in 51 directories and 21 aliases), the history with its populations (6 fork commits since the base over the 333 and 9 over the directory; since June 28 / 6 over the 333 and 32 / 9 / 23 over the directory) and the delta (16 A 3 D 12 M upstream's direction; 18 commits pending, 12 without merges), or the deltas beside them.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `333`.
- [ ] `02-forward-audit.md` § The entries has 88 rows generated by a script under the audit folder's `tools/` that asserts 333 / 88 / 65 / 23 (the alias rows naming their targets; the 25 in-directory symlinks noted on their targets' rows), each row with files, lines, fork-own, the tier, the flags set, the run-order prefixes, the board's `model` string where the tree has one, and its disposition in D-WORKFLOW-209's words; no row proposes a removal of an upstream-carried unit.
- [ ] `02-forward-audit.md` § The selection quotes the selection lines (`002-autostart:6-12`, `autostart:31-43` with `:38`'s `-f`, `package.mk:15,20`, the wrappers' `:14-17`), lists all 28 board `model` strings of the two shipped trees (the `AYN-Thor` sub-node set apart) with `HAS` or `NONE` for each, and states in those words that the two owned H700 units (`Anbernic RG35XX SP`, `Anbernic RG-SP`) select no device entry; § The tiers states the three tiers with their counts; § The fork-own five reads each file whole against #332 and D-UI-121 with its lines cited.
- [ ] `02-forward-audit.md` § The shape states the tree-wide counts from § 5's path-safe tally (shebangs, `/etc/profile` sourcers, `set_setting` callers, `/storage` writers, `/sys` writers, `DEVICE_*` definers, the guards by the widened pattern, the modes, the two `050-game*configs` spellings), each with its population (the 285 blobs or the 266 shell files) and taken unfiltered; § The upstream delta names the 31 paths and the 18 pending commits, the two panel-calibration files for shipped boards as the currency finding.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows no guest (or only one granted on #676 by its comment's time), no build, no compiler, no plan generation, no fetch, **no command against a handheld** (`ssh`, `device-act`, `scp` to a unit: 0 hits, or every hit a negation), no M7 build root read, no `tools/council/run invoke` but the one seat's probe and refutation, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent` (`--help` included), and the VM line.
- [ ] `04-analysis.md` § Q2 carries the tier-B findings with each file's lines quoted; § Q3 each bug decision with its trace, its `Already written:` line and its VM line (`tools/nova-led-test`'s fixture shape or a guest), and the owned-H700-units finding with `platforms/H700/*` read by name; § Q4 the two panel-calibration files and `rocknix-info:8`'s lead; § Q6 the dispositions by tier, removals none; § Q7 the clarity answer; § Second opinion grades every seat item with the seat's words quoted and the re-read lines named.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N` and carries its `Already written:` line.
- [ ] The retro exists at `docs/retros/<date>-m6-os-device-quirks.md`, is posted on #676, says what the slice did to the two time-to-play numbers (nothing, or the boot path a fix touched) and what the OS epic's close inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#676; a blocker named on #676 (a seat that fails its provenance gate twice,
two commands that disagree, a block whose output differs from § 2's beyond
the deltas it records); a branch that differs from `8ebaf8daad` on one of
the 333 at stage A; or an execution limit, stated as such with the running
log current. A checkpoint is not a stop. An idle session says it is idle
on #676, **and does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#676`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #676` or the
  guard.
- The VM question written before any proof (§ 5: yes, on the host; no
  guest planned; nothing on a unit).
- The mini-retro at stage G, posted on #676, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none
  expected); D-WORKFLOW-209 is the highest Decided row on the coordinator's
  branch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); a
  row this slice forces takes an ID the coordinator assigns on #676.
- `tools/ceremony-check` before every push; never `--no-verify`; a merge
  with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t29/` after `df -i`, never `/tmp`.
- Commit messages `docs: ...`, with `Refs #676`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#676's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and both provenance files (read with the current
reader); the audit issue's checkboxes all at an outcome; the coverage
table's row count (333), the entries' (88) and the generator's asserted
counts; every Q6 disposition and no removal; **re-running on a clone of
the branch at the tip under `/workspace/tmp/m6-coordinator/`: the
membership block and every § 5 run in full**; `register-check` on a
simulated merge with the coordinator's tip (the ledgers united); the
retro's answers; the six exit codes. The lane posts one hand-back comment
naming the tip and each artifact by path, writes `reviewed-at:` and
`fixed-at:` into #676's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, merges the branch in its turn
after the M7 candidate (after T22's), regenerates the ledgers, posts any
#585 lines in the shape the lane wrote, and closes #676 when every row is
proven.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#695) carries a T29 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

## Version 2: what the stranger's proof found (2026-10-25)

Ten commands from the scratch clone at `2174265e9c`; the membership, the
tiers, the selection, the fork-own five, the delta and every path held.
The corrections:

1. The tree-wide shape block cut every path at its first space (`awk`'s
   `$4`) and ran nothing; it is a path-safe Python tally now, and the
   figures are restated with their populations (256 / 10; 89; 46; 156 of
      285 or 145 of 266; 32; 104 or 101; one guard, found only when the
   pattern admits the quote the x55's `040-hdmi` writes).
2. The fork's commit counts were the directory's (9; 32 / 9 / 23); over
   the 333 paths they are 6 and 28 / 6, three of the nine having touched
   QEMU quirks since deleted. Both populations are stated and run.
3. Checkbox 5's `$(cat paths.txt)` word-split every spaced path and could
   not fail; it is the `xargs -0` form.
4. `rocknix-info` has a DMI fallback at `:10`; only the `/` → `-` sed is
   absent.
5. The 18 pending upstream commits are 12 without merges.
6. The rest is 51 directories and 21 aliases; tier B is 14 directories and
   2 aliases.
7. The HAS / NONE read covers all 28 board strings (nine more NONEs named),
   the `AYN-Thor` sub-node set apart.
8. #676 was retitled before dispatch, not at it; its P1 VM line is replaced
   at dispatch.
9. The `050-game*configs` spellings are a naming inconsistency for Q7, not a
   run-order question for Q2.
10. The shared-file examples are completed (Odin 2's `achievements`, Pocket
    DS's two, RG DS Plus's four files).
11. `010-analog_sticks_led_control` is twelve identical blobs and one that
    differs in its copyright line.
12. Unverified by the proof, stated as such: #695's cell (corrected by the
    coordinator), the inventory's `eb4763e3cc`, T22's 225 and G-35.

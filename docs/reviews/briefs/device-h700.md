---
slice: T27
id: device-h700
issue: "#674"
epic: "#1082"
area: devices
kind: currency
lens: cost against value
depth: Independent
version: 2
written: 2026-10-25
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
  upstream_next: 651150fc88
---

# T27: the H700 device (RG35XX SP, RG SP)

## 1. Identity

- **Issue:** #674 `M6.P2 E1082/T27: devices: the H700 device (RG35XX SP, RG
  SP)`, slice `device-h700` (`k: 27`) in `docs/reviews/slices.json`,
  twenty-seventh in `docs/reviews/order.md` (its row at the P1 tip: *28 | 12,901 | 327 (0) |
  8,129 | Independent*; its `why`: *the maintainer's test handhelds; options,
  device packages (u-boot DDR3/DDR4, the suspend stub), device trees and
  kernel configuration; its fork-written kernel configuration (8,129 lines)
  is read here as a diff against its base (plan § 2)* -- **the last clause
  is corrected below: the configuration is upstream's, and its base exists**).
  **Epic:** #1082 (the devices: T11 first, then this slice, T28, T25; its
  futro `docs/futros/2026-10-25-m6-devices.md`, whose guess that this
  configuration *will meet the same question* as T11's is answered no in
  its errata). **Milestone:** M6; its body holds the live order; read it
  first.
- **Predecessors that bear on these files:** **T11** (#658: the override
  kernel recipe every device builds, `projects/ROCKNIX/packages/linux/package.mk`,
  whose H700 branch at `:29-35` builds `7.2` and at `:223-243` embeds the
  rtl_bt/rtw88 firmware and ten `.panel` files into `CONFIG_EXTRA_FIRMWARE`
  (the `--set-str` at `:243`);
  the project `bootloader/mkimage:18-26`, which writes the SUBDEVICE's
  u-boot and copies `device_trees` but never creates `/dtb.img`; its
  `BOOTLOADER=` table, H700 `u-boot`; its membership holds the DDR3 overlay
  DTS `kernel-drivers/device-tree-overlays/sources/H700/sun50i-h700-anbernic-rg35xx-2024-ddr3.dts`
  and the H700 panel firmware files, read there, cited here); **T5**
  (#652: F-17 -- `find_file_path` reads of device-level files are outside
  the package stamp, so a change to `devices/H700/config/kernel-firmware.dat`
  leaves `kernel-firmware`'s stamp unchanged; the image-size check, H700
  1,317,472,264 of 2,147,483,648; atf 2.12.0); **T40** (#687: the
  32 live H700 kernel patches and the four u-boot patches are
  `patches-and-configs`, not this slice's; `packages/tools/u-boot/patches/0001-libfdt-...`
  is a shadowed copy because `devices/H700/packages/u-boot` overrides the
  generic u-boot, `02:111, 718`); **T29** (#676, the per-handheld quirks:
  the H700 quirks are its, not this slice's); **T41** (#688, the shipped
  kernel patches, where the fork-written ramoops patch `0950-...` belongs).
  Register: **D-SYS-002/003/004** (the watchdog 15 s; softlockup and
  hung-task panic; ramoops at the SoC dtsi's reserved memory -- the six
  configuration lines the fork wrote), **D-WORKFLOW-033** (#44, which image
  DDR3 or DDR4 a unit takes, parked until after the RC), **D-WORKFLOW-185**
  (the shipped set), **D-WORKFLOW-114** (the support matrix), **D-QA-027**
  (the RG35XX SP is the dedicated QA handheld; the RG SP the maintainer's),
  **D-WORKFLOW-100** (the RG35XX SP the migration device), **D-WORKFLOW-150**
  (build H700 first), **D-WORKFLOW-123** (`CONFIG_DEFAULT_HOSTNAME`
  "ROCKNIX" pinned at `package.mk:160`, where upstream now uses
  `${DISTRONAME}`), **D-WORKFLOW-187**, **D-WORKFLOW-209**, **D-WORKFLOW-195**.
  Device facts (`docs/releases/device-facts.md`): *H700 boot on the RG35XX
  SP (LPDDR4 unit)* (2026-10-16), *H700 boot on the RG SP (LPDDR3 unit)*
  (2026-10-12), *The H700 watchdog, panic-on-hang and ramoops* (never
  observed) -- the rows a device checkbox points at (`vm-first.md`,
  D-QA-044).
- **The division of labour (D-WORKFLOW-189)** and **the rule
  (D-WORKFLOW-209)** as T11's brief states them: the lane executes,
  changes none of the 28 and nothing under `packages/`, `projects/` or
  `tools/` at stages A to D; a dead end is a disposition; the class
  decision for anything upstream carries is the maintainer's on #346.
- **One worktree, one session.** Branch `feature/m6-device-h700-674` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-device-h700-674`,
  created by the coordinator, stacked on `feature/m6-p1-survey-641` at
  `2174265e9c` with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #674). **Before that
  comment exists nothing runs in it.** The session is named in the dispatch
  comment (the first freed session; T11's lane, the T5 session, if it has
  closed out). **The rules in this worktree are `next`'s except the paths
  the dispatch comment lists.**
- **Model and effort:** Opus 5.5 at high effort. Record what ran in
  `00-running-log.md`'s header.
- **Review depth: Independent** (plan § 6c, `slices.json` k 27: *an
  ordinary device slice*): **one seat, GPT-6 Astra at `max`**, a probe
  first, then one refutation pass over one trimmed packet
  (D-WORKFLOW-195), exactly as T11's brief § 1 and T13's stage C: the
  packet is the 8 read files (`options`, `update.sh`, the two udev rules,
  the four recipes) with the two defconfigs and `kernel-firmware.dat`, the 15 DTS
  (321 lines), the configuration's diff against `upstream/next`'s own copy
  (12 / 13 lines, not the 8,129), `02`, `03` and `04` whole, and the
  context sections (the order's § T27, this brief's § 2 and § 4, the
  register rows named above, the three device-facts rows). **Scanned before
  it is sent**; **every other `tools/council/run` call carries
  `COUNCIL_ENV_FILE=/nonexistent`, `--help` included.**
- **The host:** M6's; this slice runs **no guest, no build, no compiler, no
  plan generation and no network**, and **nothing on a handheld, ever** --
  the two H700 units are a person's (D-QA-015, D-QA-027); a fact only a
  board can show is a `device-facts.md` row, read, never produced here.
  `TMPDIR` under `/workspace/tmp/m6-t27/`. Register: a row this slice
  forces takes D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-033 or higher
  (the three before 209 and D-INFRA-032 are the M7 lane's; 209 the
  coordinator's).

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-h700-674
cd "$D"
git branch --show-current                                            # feature/m6-device-h700-674
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists
cat .github/sessions/saved-session-state-feature-m6-device-h700-674.md         # seeded by the dispatch
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo "upstream/next at 651150fc88 is here"   # read, never fetched
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-device-h700-674
```

No `git fetch` of any kind.

## 2. Scope

**28 paths, 12,901 lines; 8 read (shell 2 / 147, udev 2 / 3, recipe 4 /
177 -- 327 lines, 0 fork-own); the 15 device-tree sources (321 lines) are
not counted as read by the survey's language rule but are read here all
the same; upstream-carried 27 paths / 4,772 lines, vendor-carried 1 /
8,129 (the kernel configuration, `tier_note: fork-written`, area
`patches-and-configs`); reach shipped 28.** The membership is `slices.json`
k 27's rule on `inventory.json` at `2174265e9c`: area `devices` with reach
`shipped` under `projects/ROCKNIX/devices/H700/**`, **plus** area
`patches-and-configs` under `projects/ROCKNIX/devices/H700/linux/*.conf`.
The block (the same translator as T11's; its `{a,b}` is unused here):

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
A=rx("projects/ROCKNIX/devices/H700/**"); B=rx("projects/ROCKNIX/devices/H700/linux/*.conf")
t=[r for r in rows if (r["area"]=="devices" and r["reach"]=="shipped" and A.match(r["path"])) or (r["area"]=="patches-and-configs" and B.match(r["path"]))]
READ={"shell","udev","recipe"}
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",sum(1 for r in t if (r.get("language") or "") in READ),sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ),"fork-own",sum(r["lines"] or 0 for r in t if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("language",dict(collections.Counter((r.get("language") or "none") for r in t)))
import os; os.makedirs(".qa-scratch/t27", exist_ok=True)
open(".qa-scratch/t27/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))
print("written", len(t), ".qa-scratch/t27/paths.txt")'
# (the sorted(..., key=...) above is Python's keyword, not a credential: a reader applying the read filter to this block drops that line and sees nothing written -- run the block raw)
# paths 28 lines 12901
# read 8 327 fork-own 0
# tier {'upstream-carried': 27, 'vendor-carried': 1} reach {'shipped': 28}
# language {'shell': 2, 'other': 2, 'udev': 2, 'devicetree': 15, 'kernel-config': 1, 'recipe': 4, 'none': 2}
# written 28 .qa-scratch/t27/paths.txt
```

A different count is a delta to record with the command, not a reason to
stop. (The two `none` rows are the defconfigs, the two `other` rows
`kernel-firmware.dat` and the `.disabled` patch.)

**The device, at `8ebaf8daad`.** `options` (84 lines): aarch64
`TARGET_CPU=cortex-a53`, `TARGET_CPU_FLAGS="+crc+fp+simd"` (no `+crypto`;
the `arm` side carries `TARGET_FPU=crypto-neon-fp-armv8`, and
`device-builds.md`'s device table says *crypto-neon-fp-armv8* for H700 --
say which is read before any SIMD claim), `HW_CPU="Allwinner H700"`,
`KERNEL_TARGET=Image`, `BOOTLOADER="u-boot"` (`:34`), `UBOOT_FIRMWARE+=" atf"`,
`ATF_PLATFORM="sun50i_h616"`, `MALI_FAMILY=g31` / panfrost,
`BATTERYPLUS_SUPPORT=yes`, `DISPLAYSERVER=wl`, `ROCKNIX_DEVICE_TREE_OVERLAYS="yes"`,
`ZRAM_SWAP_SIZE=0`, `SWAP_FILE_SIZE=0`; **no `SUBDEVICES` line** -- the
SUBDEVICES are derived in `distributions/ROCKNIX/config/functions:224` from
`projects/ROCKNIX/config.xml` (`//rocknix/H700/*[@mkimage_options]`,
upstream `2e825afd0c` 2026-06-08 "h700: subdevices"), both outside the
slice, so the u-boot wrapper is not dead.

**u-boot, three recipes.** `packages/u-boot/package.mk` (36 lines,
`PKG_VERSION "1.0"`, no URL) depends on `u-boot-${SUBDEVICE}` and copies
each sysroot's `u-boot-sunxi-with-spl.bin` to
`usr/share/bootloader/H700_${SUBDEVICE}_u-boot-sunxi-with-spl.bin`;
`u-boot-DDR3` and `u-boot-DDR4` (43 lines each, `v2026.01`, the same
sha) differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG`
(`anbernic_rg35xx_h700_lpddr3_defconfig` / `lpddr4`); the two defconfigs
(35 lines) differ in 10 lines a side (§ 5's count prints 20), `CONFIG_SUNXI_DRAM_H616_LPDDR3` /
`LPDDR4` and `CONFIG_AXP_DCDC3_VOLT` 1200 / 1100; the u-boot patch pairs
(0001 dram, 0002 axp717 charge-only boot) are byte-identical between the
two and **outside the slice** (patches-and-configs). The suspend stub
(`h700-suspend-stub/package.mk`, 55 lines, pin `712653d11230...`) builds
one stub per memory type from each defconfig; **its line 43 matches the
credential read filter** (`key=` in a build flag), so a filtered read shows
54 lines -- read that line with the masking `sed`, never quote it raw.

**Device trees.** 15 fork-tree DTS under `linux/dts/allwinner/` (14 to 44
lines), 13 of them `#include`-ing a mainline board file and the two
`rg40xx-*-v2-panel` trees including their fork-tree siblings, each carrying
`rocknix-dt-id`: the RG SP is `sun50i-h700-anbernic-rg-sp` (model
"Anbernic RG-SP", `anbernic,rg34xx-sp-v2-panel`, added `fc89fab1a2`
2026-08-04); the RG35XX SP is mainline's `sun50i-h700-anbernic-rg35xx-sp`
(its dt-id from kernel patch 0154, T41's) or `-rg35xx-sp-v2-panel` here.
The kernel recipe copies every built dtb to `usr/share/bootloader/device_trees`
(`package.mk:419-431`); `bootloader/update.sh:21-32` copies them to
`/flash` and writes `/dtb.img` from `/proc/device-tree/rocknix-dt-id`;
`:34-49` reads the `vdd-dram` regulator (1,200,000 µV -> the DDR3
loader, 1,100,000 -> DDR4) and `:55` `dd`s it at `bs=1K seek=8`. The project
`mkimage` never creates `dtb.img`: a fresh card does not boot until it is
activated by hand (`docs/device-flashing-runbook.md`, the H700 section).

**The kernel configuration has a base, and it is upstream's own copy.**
`linux/linux.aarch64.conf`: 8,129 lines, header `# Linux/arm64 7.2.0
Kernel Configuration`, 2,104 `=` lines and 4,189 `is not set`; the override
recipe builds **`7.2`** for `H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750`
(`package.mk:29-35`), `listnewconfig` then `yes "" | kernel_make oldconfig`
at `:306-316`. Added by upstream (`9f1fab30f6` 2025-07-13, ROCKNIX Team,
"projects: add modifications for ROCKNIX", +7,773); 58 non-merge commits in all (64 with merges), 13
since 2026-06-01 (12 upstream's, 1 the fork's). **The fork's
edits are six lines in one commit**, `cbf75c0b06` (+6/-5: `WATCHDOG_SYSFS`,
`PSTORE_CONSOLE`, `PSTORE_RAM`, `SOFTLOCKUP_DETECTOR`, `DETECT_HUNG_TASK`
`=y`; `DEFAULT_HUNG_TASK_TIMEOUT=120` -- D-SYS-002/003/004). Against
`651150fc88`'s own copy the diff is **12 removed / 13 added** (the fork's
six and upstream's four commits since the merge base: `c0980b2b71`,
`5f56cd5150`, `6fbefc45c6`, `dcafa74090` 2026-10-22); against the other
confs in the tree it is far (RK3326 898 / 1,809; RK3566 1,518 / 1,908;
LibreELEC's Allwinner 1,871 / 1,953; SM8550 1,585 / 1,106). So plan § 2's
*one diff per kernel config against its base* is, here, the diff against
upstream's copy, with the fork's six lines named; T11's "no base" shape
does not apply, and the order's *fork-written* is an erratum (the
inventory's `tier_note` says it because the fork touched it).

**A third of the slice's lines is a patch nothing applies.**
`patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled`
(4,036 lines, 31 % of 12,901) is inside T27 only because `.disabled`
escapes the `*.patch` globs (`scripts/unpack:143-159` apply `*.patch`);
born disabled (`fad6d7d27a`). The 32 live H700 kernel patches (8,616 lines)
are T41's; the fork-written ramoops patch
`0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch` (38 lines,
`From: ROCKNIX fork`, `cbf75c0b06`, absent upstream) is tiered
`vendor-carried` with `tier_note: fork-written` -- marked wrongly for anyone
counting fork-own, outside this slice, while the six configuration lines
that enable it are inside: cite it, do not re-tier it (the inventory is
T10's).

**What `upstream/next` (`651150fc88`) already changes:** `D
filesystem/usr/lib/udev/rules.d/80-clock.rules` (`899193e5af` 2026-10-05,
"systemd: drop the hwclock udev rules, the kernel sets the clock"), `M
options` (+4/-1 by two commits of 2026-10-03: `e1b7d1f82f`, the ES ZRAM
menu, and `dc14669f69`, the systemd THP policy), `M
linux.aarch64.conf` (the four commits above); the `.disabled` patch and the
rest unchanged; the kernel version 7.2, u-boot `v2026.01`, the suspend
stub's pin unchanged upstream. Upstream's linux recipe (18+/35-) adds
`rocknix-joypad` to `PKG_PATCH_DIRS` for `RK3326|RK3399|S922X|H700`.
**History since 2026-06-01 over the 28:** 29 non-merge commits, 1 the
fork's (`cbf75c0b06`), 28 upstream's (options 2, bootloader 1, config 1,
filesystem 1, dts 6, conf 13, suspend-stub 3, u-boot-DDR3/DDR4 5 each,
the wrapper 4, the `.disabled` patch 0).

## 3. Read first

1. `.claude/rules/` from `next`: `engineering-practices.md`, `device-builds.md`
   (the device table, the H700 DDR3/DDR4 paragraphs, the flashing pointer),
   `handheld-evidence.md`, `vm-first.md`, `bugs-are-agent-first.md`,
   `upgrade-and-install.md`, `packaging-and-patches.md`,
   `decision-register.md`, `issue-tracking.md`, `working-principles.md`.
2. `docs/device-flashing-runbook.md` (the H700 section: the card, the
   readback, `/dtb.img`), `docs/releases/device-facts.md` (the three H700
   rows), `docs/device-testing-policy.md`.
3. `docs/reviews/plan-for-the-plan.md` § 2, § 6b, § 6c; `docs/reviews/order.md`
   § T27, § T11, § T28, § T25, § T41 (at the P1 tip `2174265e9c`, where
   `order.md` and `slices.json` live); `docs/futros/2026-10-25-m6-devices.md`
   with its errata.
4. The register rows named in § 1, by ID; `docs/blindspot-register.md`
   entries 22, 31, 75.
5. T11's `02` (`feature/m6-device-generic-x64-658`, `git show`): the
   override recipe, the boot files, the `BOOTLOADER=` table; T5's `02`
   F-17 and the image-size check (`feature/m6-build-engine-652`); T40's
   `02:111, 718` (`feature/m6-patches-dead-687`).
6. `distributions/ROCKNIX/config/functions:224` (SUBDEVICES),
   `projects/ROCKNIX/config.xml`'s H700 entries, `config/functions:1449-1461`
   (`kernel_config_path`), `scripts/unpack:143-159`, `projects/ROCKNIX/bootloader/mkimage:18-26`.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`design`); the lens is currency, so Q4 leads:

- **Q4 Package currency -- the lead question.** For each pinned unit
  (u-boot `v2026.01` with its sha; the suspend stub's commit; atf, read
  from the recipe that pins it for H700; the kernel `7.2` and its sha at
  `package.mk:29-35`): the pin at `8ebaf8daad`, the pin at `651150fc88`
  (unchanged, by the research), the pin's date from the recipe or the
  upstream commit that set it, and **`CANNOT (no network)`** for the
  author's current release -- that check is `tools/fork-package-freshness`'s
  at the RC (D-WORKFLOW-024) and is named, not run. The configuration's
  currency is its 12 / 13 diff against upstream's copy, each line
  attributed to its commit. The DTS currency: which of the 15 boards has a
  mainline board file at the kernel the recipe builds (`#include` targets
  present in the 7.2 tree is a build fact; here, the include lines and
  the patches that add them, T41's, are named).
- **Q1 Modernize.** The three u-boot recipes against one parameterised
  recipe (a design sentence, deferred to the coordinator; no edit);
  `update.sh`'s `vdd-dram` selection against a declared memory type;
  `/dtb.img` written by `update.sh` on an update but never by `mkimage`
  on a fresh card (the runbook's hand step): a design question for the
  coordinator, with D-WORKFLOW-033 (#44) cited, not reopened.
- **Q2 Standards.** The `.disabled` patch (a file the build never reads,
  31 % of the slice); the `tier_note: fork-written` on a file the fork
  touched once (an inventory reading, cited, not re-tiered); the two
  identical u-boot patch pairs (T41's) and the identical recipe bodies;
  `TARGET_CPU_FLAGS` without `+crypto` against the rule's table (which is
  wrong, the table or the flag? -- a finding with both lines quoted, a
  rule-edit lead for the coordinator if the table).
- **Q3 Bugs.** T5's F-17 (a `kernel-firmware.dat` change does not move the
  stamp): cite #836's state, do not re-file. `update.sh`'s regulator
  thresholds (`:34-49`): what happens at a voltage that is neither
  (a third memory type, a regulator read that fails) -- read, and a `bug`
  with its trace only if the script writes a loader it should not; its
  `Already written:` names the two units' cards (device-facts rows L15,
  L16) and argues nothing inherited or names the migration. Nothing runs
  on a unit.
- **Q5 Efficiency.** The configuration's size against upstream's copy
  (equal but for 25 lines); the 15 DTS against the two shipped units (13
  are other H700 handhelds' -- shipped by placement, used by no unit the
  fork ships: a disposition each, not a removal, D-WORKFLOW-185); the
  firmware `kernel-firmware.dat` (18 lines) against `CONFIG_EXTRA_FIRMWARE`'s
  list in the recipe (duplicates, misses).
- **Q6 Dead ends.** The `.disabled` patch (disposition: *disabled at
  birth, upstream's; its removal is #346's class decision*); the 13 DTS of
  unshipped H700 boards (*carried by placement*); `80-clock.rules` (gone
  upstream: *settled by the next base merge*). Removals none.
- **Q7 Clarity and structure.** Can a reader tell from the device
  directory which unit boots which loader and which tree, and where
  `/dtb.img` comes from? Does `options` say why `ZRAM_SWAP_SIZE=0`
  (upstream's ZRAM menu change moves it)? The `vm-first` answer for every
  device fact: the three rows named, nothing new asked of a unit.

## 5. The evidence floor

1. Tracker state is never sole evidence; every cell cites a command's
   output or a file:line at `8ebaf8daad`.
2. Mechanical evidence outranks reading: `diff` counts, `git log` with the
   three fork identities (`Max Engel|blitterbot|rasterabot`), `grep -n`
   on the scripts; a comment is the author's claim (blindspot 31).
3. **The bench is the host; no guest, no build, no unit.** **Can this be
   done on the VM? Yes -- on the host, with no network:** every read,
   diff, log and script read runs on the build host at `8ebaf8daad` with
   `651150fc88` read locally; the GENERIC_X64 guest cannot be an H700, so
   **no guest is asked for**, and a fact only a board can show is a
   `device-facts.md` row (L15, L16, L29), read and cited, **never produced
   here** (D-QA-015, D-QA-027: the RG35XX SP and RG SP are a person's).
   `tools/council/run invoke` runs once, the Phase 4.6 seat.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The runs, with what the coordinator read** (the lane runs each at stage
A and records the exit, the wall time and the summary line; `TMPDIR` under
`/workspace/tmp/m6-t27/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-h700-674
cd "$D"; export TMPDIR=/workspace/tmp/m6-t27/tmp; mkdir -p "$TMPDIR" .qa-scratch/t27
# the membership block (§ 2) -> .qa-scratch/t27/paths.txt (28)
# the configuration against upstream's own copy (expect removed 12 added 13) and the fork's edits (expect cbf75c0b06 alone since the merge base c445081a59)
C=projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf
git show "8ebaf8daad:$C" | sed -n '3p'; git show "8ebaf8daad:$C" | wc -l                          # Linux/arm64 7.2.0; 8129
git show "651150fc88:$C" > "$TMPDIR/up.conf"; git show "8ebaf8daad:$C" > "$TMPDIR/ours.conf"; echo "removed=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^<') added=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^>')"
git log --no-merges --format='%h %ad %an %s' --date=short c445081a59..8ebaf8daad -- "$C"            # the fork's: cbf75c0b06 alone (without --no-merges two merges print too)
git log --format='%h %ad %an %s' --date=short 8ebaf8daad..651150fc88 -- "$C"                        # upstream's four
git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '29,35p' | grep -n -E 'H700|PKG_VERSION'   # 7.2
# the pins (expect v2026.01 twice, the stub's commit, atf's version from its recipe; the same at 651150fc88)
for p in u-boot-DDR3 u-boot-DDR4 h700-suspend-stub u-boot; do for h in 8ebaf8daad 651150fc88; do printf '%s %s: %s\n' "$p" "$h" "$(git show "$h:projects/ROCKNIX/devices/H700/packages/$p/package.mk" | grep -E '^PKG_(VERSION|SHA256|UBOOT_CONFIG)=' | tr '\n' ' ')"; done; done | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
diff <(git show 8ebaf8daad:projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/sources/configs/anbernic_rg35xx_h700_lpddr3_defconfig) <(git show 8ebaf8daad:projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/sources/configs/anbernic_rg35xx_h700_lpddr4_defconfig) | grep -c -E '^[<>]'   # the DRAM lines
# the loader and tree selection (expect update.sh:21-32 dtb.img; :34-49 vdd-dram; mkimage never writes dtb.img)
git show 8ebaf8daad:projects/ROCKNIX/devices/H700/bootloader/update.sh | grep -n -E 'dtb.img|vdd-dram|microvolts|seek' | cut -c1-120
git show 8ebaf8daad:projects/ROCKNIX/bootloader/mkimage | grep -n -E 'dtb.img|device_trees|SUBDEVICE' | cut -c1-120
git show 8ebaf8daad:distributions/ROCKNIX/config/functions | sed -n '220,228p' | grep -n SUBDEVICES
# the DTS and their includes (expect 15; the RG SP's model line; the rg35xx-sp include)
git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/devices/H700/linux/dts | wc -l
for f in $(git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/devices/H700/linux/dts); do printf '%s: %s | %s\n' "$(basename "$f")" "$(git show "8ebaf8daad:$f" | grep -m1 '#include' | cut -c1-60)" "$(git show "8ebaf8daad:$f" | grep -m1 'rocknix-dt-id' | cut -c1-60)"; done
# the history with the three identities (expect 29; fork 1; upstream 28) and the upstream delta (expect 1 D, 2 M)
tr '\n' '\0' < .qa-scratch/t27/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since=2026-06-01 8ebaf8daad -- | tee "$TMPDIR/hist.txt" | wc -l; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"
tr '\n' '\0' < .qa-scratch/t27/paths.txt | xargs -0 git diff --name-status 8ebaf8daad 651150fc88 -- | cut -c1-120
# the removal rule's own check against the dispatch tip (expect empty)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1
```

## 6. Outputs

As T11's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-device-h700/`:
`00` to `05`, `second-opinions/` (the seat's plan, manifest, probe and
refutation with provenance), the lint before D, the audit issue (`Audit:
M6 T27 the H700 device -- N findings (...)`, a sub-issue of #674), the
bugs, and the retro at `docs/retros/<date>-m6-device-h700.md` (what T28
and T25 inherit: the pin table's shape, the DTS-by-unit table, the
device-facts citations). **`02` carries § The pins (one row per pinned
unit), § The configuration (the 12 / 13 against upstream's copy, the six
fork lines named), § The loader and the tree (how each of the two units
gets its loader and its `/dtb.img`, with the device-facts rows cited),
§ The device trees (one row per DTS: the board, the include, the dt-id,
shipped unit or carried by placement), and a coverage table of 28.**

## 7. Acceptance

The checklist on #674 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-device-h700/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-device-h700/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); the probe's and the refutation's outputs have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named; `packet-manifest.json` lists every packet file with its sha256 and the scan's result.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #346, #44, #836, T41's #688, T29's #676), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` in the checklist's header carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 28 (`git diff --stat 8ebaf8daad <reviewed-at> -- $(cat .qa-scratch/t27/paths.txt)` empty) and nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty; the dispatch tip is the one the dispatch comment names).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (28 paths, 12,901 lines; read 8 files / 327 lines / 0 fork-own; tier 27 / 1; reach 28; written 28), the 15 DTS named as read though not counted, the configuration's diff against `651150fc88`'s copy (12 / 13) and the fork's one commit, the history (29; 1 fork; 28 upstream) and the upstream delta (1 D, 2 M), or each delta with its command.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `28`.
- [ ] `02-forward-audit.md` § The pins has one row per pinned unit (u-boot DDR3, u-boot DDR4, the wrapper, the suspend stub, atf, the kernel): the pin at `8ebaf8daad`, at `651150fc88`, its date and setting commit, and `CANNOT (no network)` for the author's current release with `tools/fork-package-freshness` named as the RC's check.
- [ ] `02-forward-audit.md` § The configuration states the diff against upstream's own copy (12 removed / 13 added, each line attributed to its commit), the fork's six lines with D-SYS-002/003/004, and that the configuration is upstream's with a base (the order's *fork-written* and the futro's guess named as errata).
- [ ] `02-forward-audit.md` § The loader and the tree states, with `update.sh` and `mkimage` lines quoted, how each of the two units gets its loader (the `vdd-dram` thresholds) and its `/dtb.img` (on an update by `update.sh`; on a fresh card by hand, the runbook), citing device-facts rows L15 and L16 for the observed boots and naming #44 / D-WORKFLOW-033 as the parked question; nothing is run on a unit.
- [ ] `02-forward-audit.md` § The device trees has one row per DTS (15): the board, the `#include` target, the dt-id, and *shipped unit* or *carried by placement*; the `.disabled` patch's row says *disabled at birth, upstream's, 4,036 lines, never applied* with `scripts/unpack:143-159` cited.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows no guest, no build, no compiler, no plan generation, no fetch, **no command against a handheld** (`ssh`, `device-act`, `scp` to a unit: 0 hits, or every hit a negation), no `tools/council/run invoke` but the one Phase 4.6 call, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, and no write under `/workspace/repos/rocknix*`, another lane's worktree or `/tmp`.
- [ ] `04-analysis.md` § Q4 carries the pin table's verdicts; § Q2 the `TARGET_CPU_FLAGS` finding with both lines quoted (the device table's and `options:`'s); § Q3 the `update.sh` threshold read with its bug decision and `Already written:` line; § Q6 a disposition per unit, removals none; § Second opinion grades every seat item (confirmed, narrowed, refuted, new), the decisive ones re-read at their lines.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`.
- [ ] The retro exists at `docs/retros/<date>-m6-device-h700.md`, is posted on #674, says what the slice did to the two time-to-play numbers (nothing) and what T28 and T25 inherit.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

As T11's brief § 8, with #674 for #658 and the 28 for the 58; **and
anything against a handheld never runs** -- a device checkbox is a
`device-facts.md` row, and a fact the rows lack is an open item to test
(`bugs-are-agent-first.md`), never a run on the RG35XX SP or the RG SP.

## 9. Ceremonies owed

As T11's brief § 9, headed `#674`; `TMPDIR` under `/workspace/tmp/m6-t27/`;
commit messages `docs: ...` throughout.

## 10. Hand-back

As T11's brief § 10, with `$S/t27-accept.sh` (the block, the configuration's
diff against upstream's copy, the pin table's four recipes at both hashes,
the defconfig diff count, the `update.sh` and `mkimage` greps, the DTS
count and includes, the history, the upstream delta, the empty diffs, the
seat's provenance, the lint, the checkers, the simulated merge). After
acceptance the coordinator carries the pin table's shape and the
DTS-by-unit table into T28's brief. The merge order: after T11's.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#1082) carries the area's kickoff and, in its errata, this slice's
correction of the configuration guess; a stranger's proof of this brief
runs before dispatch; version 2 records what it found.

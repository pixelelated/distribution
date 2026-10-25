# Brief: M6.P2 T25, the devices the fork does not ship and the other projects (#672)

**Version 1, 2026-10-25, the coordinator's** (D-WORKFLOW-189). Written from a
read-only research digest taken at `2174265e9c` (P1's tip; for the 397 paths
the same bytes as `next` at `8ebaf8daad`, since the 64 commits between them
touch none of them) and from T24's brief, the model table slice. A stranger's
proof runs before dispatch; version 2 records what it found. Every number
below was pasted from a command's output at the hash named beside it; the
lane re-derives each one and writes the delta where it differs.

## 1. Identity

- **Issue:** #672 `M6.P2 E1082/T25: devices: the devices the fork does not
  ship and the other projects`, slice `devices-unshipped` (`k: 25`) in
  `docs/reviews/slices.json`, twenty-fifth in `docs/reviews/order.md` (its
  § T25 paths line: *"397 paths, 49,555 lines, -- read, of which -- fork-own;
  0 patch and config lines; reach unreached 216, unshipped 181"*; its `why`:
  *"the devices the fork neither ships nor tests on ... and the nine
  LibreELEC-era projects no Makefile target builds"*). **Epic:** #1082 (the
  devices: T11 #658 accepted, T27 #674 accepted and closed out, this slice,
  then T28 #675), whose futro
  (`docs/futros/2026-10-25-m6-devices.md`) carries a T25 kickoff addendum
  written with this version. **Milestone:** M6. **Predecessors:** #346,
  #641, #644 (finding 24's class), **T23 #670** (`generic-packages-dead-ends.md`:
  the disposition list of D-WORKFLOW-209; its 39 `unshipped` generic rows
  stay T23's -- what it hands this slice is the *targets*, not paths), **T24
  #671** (the table-slice shape: one coverage row per path, a positive
  control beside every zero), **T11 #658** (`02-forward-audit.md` § The boot
  files; errata F-09: a merge of `next` keeps GENERIC_X64 in the kernel
  override's version case), **T27 #674** (`02` § The pins and § The device
  trees: the pin table's shape and the DTS-by-unit table), **T6 #653** (the
  reachability-table method). **Beside it:** T22 (#669) runs in the T1
  session and T15's queue in the T3 session (D-WORKFLOW-190); the three
  share no path.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346 or #585, or decide a question of scope:
  those are the coordinator's, reached through #672, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect in a fork-own unit, should the table find one
  (D-WORKFLOW-187). **Removal is never proposed by this slice for an
  upstream-carried unit** (D-WORKFLOW-209: one class decision on #346, the
  coordinator's to put); the one fork-own row's disposition is recorded
  and left for the coordinator.
- **One worktree, one session.** Branch `feature/m6-devices-unshipped-672`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (which carries `order.md`, `slices.json`, `inventory.json`
  and `status.md`; none of them is on `next`) with the coordinator's tip
  merged in (D-WORKFLOW-209, the T11/T23/T24/T27 briefs and the inherited
  tables are only there) and the lane's pointer seeded; the two hashes are
  in the dispatch comment on #672. Until that comment exists the pointer is
  not seeded, the first command's `cat` fails, and nothing starts. The
  session is the T5 lane's (`m6-t5-build-engine`), which ran T27; its
  earlier worktrees stay idle beside this one.
- **Depth: Local** -- a reachability table (plan § 6c, D-WORKFLOW-184):
  `second-opinions/review-plan.json` with `depth: local`, `reviewers: []`,
  `tier_exception: D-WORKFLOW-184` and a `reason` naming plan § 6c and
  `slices.json`'s `k: 25`; **no `tools/council/run` call**, keyed or not.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672
cat .github/sessions/saved-session-state-feature-m6-devices-unshipped-672.md   # the pointer: the dispatch's two hashes
git status --short | wc -l                                                      # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                  # empty: the read is of next's bytes
tools/register-check >/dev/null && echo register-ok; grep -n 'D-WORKFLOW-209' docs/decision-register.md | head -1
```

## 2. Scope

**The membership block** (T24's, with the area filter; `slices.json` k 25's
`select` carries globs and reach only, and globs plus reach alone select
3,297 paths across four areas -- `slice_of` applies the slice's area on top,
so the block must too):

```bash
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
excl = ("projects/ROCKNIX/devices/H700/", "projects/ROCKNIX/devices/SM8550/", "projects/ROCKNIX/devices/GENERIC_X64/")
t25 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "devices"
       and (r["path"].startswith("projects/") or r["path"].startswith("packages/"))
       and not r["path"].startswith(excl) and r["reach"] in ("unreached", "unshipped")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t25), "lines", L(t25), dict(collections.Counter(r["reach"] for r in t25)), dict(collections.Counter(r["tier"] for r in t25)))
print(dict(collections.Counter(r["language"] for r in t25)))
u = collections.Counter("/".join(r["path"].split("/")[:3]) if r["path"].startswith("projects/ROCKNIX/") else "/".join(r["path"].split("/")[:2]) for r in t25)
print("units", len(u), sorted(u.items()))
CODE = {"shell", "recipe", "udev", "python", "c", "make"}
rd = [r for r in t25 if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached"]
print("read", L(rd), "rows", len(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"))
print("shadowed", sum(1 for r in t25 if r.get("shadowed_by")), "fork-own", [r["path"] for r in t25 if r["tier"] == "fork-own"])
os.makedirs(".qa-scratch/t25", exist_ok=True)
open(".qa-scratch/t25/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t25, key=lambda r: r["path"])))
open(".qa-scratch/t25/rows.tsv", "w").write("".join("\t".join(str(r[k]) for k in ("reach", "tier", "lines", "language", "buildable_by", "shadowed_by", "path")) + "\n" for r in sorted(t25, key=lambda r: r["path"])))
PY
wc -l .qa-scratch/t25/paths.txt     # 397
```

Recorded (2026-10-25, at `2174265e9c`; the inventory there was generated at
`eb4763e3cc`, 2026-10-23T02:20:48Z, in the container, 26 configs, upstream
read `c1f1746828`): **397 paths, 49,555 lines; unreached 216, unshipped
181; upstream-carried 396, fork-own 1.** The tool's own `load_slices` /
`slice_of` give the same set. The read figure in #672's body (3,619 lines,
0 fork-own) is the tool's `CODE` rule over the 397: **64 rows** (31 recipe,
26 shell, 4 udev, 1 python, 1 c, 1 make) -- a derived check, not a reading
plan; a table slice reads every row's identity, not its lines. Languages:
devicetree 53 rows / **34,437 lines (69 % of the slice)**, shell 95 /
4,378, yaml 21 / 2,536 (inputplumber maps), none 32 / 2,017, recipe 52 /
1,852, config 50 / 1,515, c 3 / 1,004, the rest under 700 each.
`shadowed_by` is set on **9 rows**; no path carries a space.

**The units (25), the table's rows:**

| Unit | Paths | Lines | Reach |
| --- | ---: | ---: | --- |
| `projects/ROCKNIX/devices/AMD64` | 15 | 494 | unshipped 13, unreached 2 (the `intel-ucode` pair) |
| `projects/ROCKNIX/devices/RK3326` | 37 | 9,880 | unshipped |
| `projects/ROCKNIX/devices/RK3399` | 4 | 1,554 | unshipped |
| `projects/ROCKNIX/devices/RK3566` | 16 | 3,953 | unshipped |
| `projects/ROCKNIX/devices/RK3576` | 6 | 1,907 | unshipped |
| `projects/ROCKNIX/devices/RK3588` | 3 | 212 | unshipped |
| `projects/ROCKNIX/devices/S922X` | 4 | 207 | unshipped |
| `projects/ROCKNIX/devices/SM4450` | 18 | 7,278 | unshipped |
| `projects/ROCKNIX/devices/SM6115` | 16 | 2,502 | unshipped |
| `projects/ROCKNIX/devices/SM8250` | 28 | 7,653 | unshipped |
| `projects/ROCKNIX/devices/SM8650` | 8 | 2,298 | unshipped |
| `projects/ROCKNIX/devices/SM8750` | 14 | 4,192 | unshipped |
| `projects/ROCKNIX/packages/{linux-drivers,linux-firmware}` | 15 | 1,264 | unshipped 14, unreached 1 (`dtbocfg`) |
| `projects/ARM` · `Allwinner` · `Amlogic` · `Generic` · `NXP` · `Qualcomm` · `RPi` · `Rockchip` · `Samsung` | 4 · 24 · 19 · 19 · 25 · 7 · 28 · 35 · 12 = 173 | 4,987 | unreached, all |
| `packages/linux` · `packages/linux-driver-addons` · `packages/linux-firmware` | 4 · 14 · 22 = 40 | 382 · 190 · 602 = 1,174 | unreached, all; `buildable_by []` |

Sums: the twelve target directories 169 paths / 42,130 lines; with the 15
ROCKNIX driver and firmware rows, **181 unshipped**; the nine projects and
the three `packages/**` units, with the three unreached rows inside the
devices area, **216 unreached**. `buildable_by` over the 397: `[]` 216;
AMD64 13; RK3326 41 (24 both arches, 17 aarch64); RK3399 5; RK3566 16;
RK3576 6; RK3588 8; S922X 5; SM4450 18; SM6115 16; SM8250 28; SM8650 9;
SM8750 14; and two rows buildable by four targets at once (`mali-bifrost`).

**What is not here, and where it is:** the `*.patch` and `linux*.conf`
rows under the twelve target directories (T43's) and under the nine
projects (T40's) -- which is why "Files / in slice" differ per target
(RK3326 62 on disk = 37 + 24 patches + 1 conf); `distributions/{LEIoT,LibreELEC}`
(27 unreached rows, T6's: the slice's globs do not reach `distributions/`);
the 39 `unshipped` rows of `packages/**` outside the devices area (T23's,
recorded there); the 17 ROCKNIX recipes only RK3566 and RK3326 build
(`libmali`, `librga`, `rkbin`, ..., T23's by order.md § 1 item 4); the
shipped pair's and the test image's directories (T27, T28, T11).

**The twelve targets at `2174265e9c`** (every one has a `Makefile` target;
`world` at line 42 is `RK3588 RK3576 RK3566 RK3326 RK3399 S922X SM8250
SM8550 H700 SM8650 SM8750 GENERIC_X64`, so **AMD64, SM4450 and SM6115 have
targets but are not in `world`**; AMD64 (44), SM8650 (103) and SM8750 (107)
are single-arch; RK3566's target carries `DEVICE_ROOT=RK3566` on lines
65-66; every target sets `PROJECT=ROCKNIX`):

| Target | `options` (line: value) | DTS on disk | Upstream commits since `2026-06-01T00:00:00Z`; last touch | `git diff --stat 651150fc88 8ebaf8daad -- <dir>` |
| --- | --- | ---: | --- | --- |
| AMD64 | 8 `TARGET_CPU="x86-64-v3"`, 23 `BOOTLOADER="syslinux"`, 26 `PARTITION_TABLE="msdos"`, 49 `GRAPHIC_DRIVERS="radeonsi"`, 75 `KERNEL_TARGET="bzImage"` | 0 | 7 | empty |
| RK3326 | 9 `cortex-a35`, 17 `TARGET_FPU="crypto-neon-fp-armv8"`, 21 `msdos`, 34 `u-boot`, 37 `UBOOT_FIRMWARE="rkbin"`, 41 `mali panfrost` | 25 | (the lane reads) | non-empty |
| RK3399 | 9 `cortex-a72.cortex-a53`, 17 `crypto-neon-fp-armv8`, 21 `gpt`, 37 `rkbin atf`, 42 `panfrost` | 1 | 12; `dcafa74090` 2026-10-22 | 1 file |
| RK3566 | 9 `cortex-a55`, 17 `neon-fp-armv8`, 21 `gpt`, 37 `rkbin`, 41 `mali panfrost` | 3 | 40 | non-empty |
| RK3576 | 9 `cortex-a72.cortex-a53`, 17 `neon-fp-armv8`, 21 `gpt`, 37 `rkbin`, 41 `mali panfrost` | 1 | 20; `dcafa74090` 2026-10-22 | 10 files |
| RK3588 | 9 `cortex-a76.cortex-a55`, 17 `crypto-neon-fp-armv8`, 21 `gpt`, 37 `rkbin`, 41 `mali panfrost` | 0 | 6; `5f56cd5150` 2026-10-04 | 2 files |
| S922X | 9 `cortex-a73.cortex-a53`, 17 `neon-fp-armv8`, 21 `msdos`, 37 `amlogic-boot-fip`, 41 `panfrost` | 0 | 58; `b48d63c445` 2026-10-23 | 65 files |
| SM4450 | 9 `cortex-a76.cortex-a55`, 17 `crypto-neon-fp-armv8`, 21 `gpt`, 35 `BOOTLOADER="qcom-abl"`, 38 `freedreno` | 2 | 37; `651150fc88` 2026-10-24 | 18 files |
| SM6115 | 9 `cortex-a73.cortex-a53`, 17 `crypto-neon-fp-armv8`, 21 `gpt`, 34 `qcom-abl`, 37 `freedreno` | 4 | 55; `651150fc88` | 59 files |
| SM8250 | 9 `cortex-a76.cortex-a55`, 17 `crypto-neon-fp-armv8`, 21 `gpt`, 34 `qcom-abl`, 37 `freedreno` | 11 | 79; `651150fc88` | 15 files |
| SM8650 | 7 `TARGET_CPU="cortex-x4"`, 10 `gpt`, 12 `ENABLE_32BIT="no"`, 24 `qcom-abl`, 27 `freedreno` | 3 | 41; `651150fc88` | 3 files |
| SM8750 | 7 `cortex-x4`, 10 `gpt`, 12 `ENABLE_32BIT="no"`, 24 `qcom-abl`, 27 `freedreno` | 3 | 91; `651150fc88` | 4 files |

**Provenance, the fact that sets the table's tone.** Against the base
(`c445081a59`, the `20261001` tag, `git merge-base 651150fc88 8ebaf8daad`)
the fork changed **one** of the 397 paths (`git diff --name-status
c445081a59 8ebaf8daad -- $(cat .qa-scratch/t25/paths.txt)`: `1 M
packages/linux/package.mk`), and `git log 651150fc88..8ebaf8daad -- <dir>`
on every target directory lists only the fork's six merges of upstream --
**no fork author touched any of the twelve.** But `next` is behind
`upstream/next`: over the 397, `git diff --name-status 651150fc88
8ebaf8daad` is **39 M**, and `git log --oneline c445081a59..651150fc88 --
<the 397> | wc -l` is **65** upstream commits since the base; over the
whole unshipped target set, patches included, `226 files changed, 14,839
insertions(+), 29,156 deletions(-)`. Every hunk is upstream's; the next
merge brings it and re-derives nothing. So a row is stated at `8ebaf8daad`'s
bytes and carries a drift cell read against **`651150fc88`** by name (the
inventory's own upstream read is the older `c1f1746828`; its
`last_upstream_commit` tops out at 2026-10-22).

**The nine projects:** no Makefile target sets `PROJECT` to anything but
ROCKNIX (`config/options:27` defaults it); the engine still names six of
them in `scripts/uboot_helper` (Allwinner :23, Amlogic :161, NXP :253,
Qualcomm :283, Rockchip :291, Samsung :507), `scripts/checkdeps:100-101`
tests Rockchip and Amlogic, `config/options:29` and `scripts/mkimage:118,287`
branch on Generic, `scripts/create_docker_package:90,93` and
`scripts/create_addon:117` name RPi; **ARM is referenced by none.**
Qualcomm has no project-level `options`. Fork commits 0, `diff --stat`
against `651150fc88` empty, for all nine. Four of Rockchip's device names
(`RK3399`, `RK3576`, `RK3588`, `RK356X`) duplicate ROCKNIX's -- different
trees, different `options` files.

**The one fork-own path, `packages/linux/package.mk`** (358 lines,
unreached, `shadowed_by projects/ROCKNIX/packages/linux`): `3d7c075f63`
(2026-10-02, the identity preparation, #337/#383) rewrote its line 132 from
`CONFIG_DEFAULT_HOSTNAME "${DISTRONAME}"` to `"ROCKNIX"` **and made the same
edit in the live override** (`projects/ROCKNIX/packages/linux/package.mk:160`),
which sources no generic recipe. A shadowed dead copy the fork edited
alongside the live one -- T23's `installer` shape -- harmless; `Already
written:` nothing inherited (the generic recipe never built for any target).

## 3. Read first

- `.github/sessions/saved-session-state-next.md` and this lane's own pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight):
  `engineering-practices.md` (§ Verify the artifact; § A name is not a
  behaviour, its bullet on counts, line numbers and hashes; § Before
  deleting a duplicate -- the test for every row, even where nothing is
  deleted), `packaging-and-patches.md`, `device-builds.md` (§ Our devices;
  § After rebasing item 3: every field as the build reads it),
  `fork-workflow.md`, `release-candidates.md` (step 0),
  `upgrade-and-install.md` (`Already written:`), `bugs-are-agent-first.md`,
  `issue-tracking.md`, `vm-first.md` (§ 5: no), `worktrees.md` (superseded
  by § 1).
- The code-auditor skill whole; the renovation face is plan § 6b; the
  Local plan file is § 1's.
- **T24's audit** (`docs/audits/2026_10_24-epic-m6-emulators-dead-ends/`):
  `02` § Coverage and § Mechanical checks (the shape of a table slice's
  evidence), `04` § Q6 (a disposition per row with `Already written:`).
  **T23's brief** § 1's disposition list (D-WORKFLOW-209). **T27's audit**
  (`docs/audits/2026_10_25-epic-m6-device-h700/02-forward-audit.md`): § The
  pins (the pin table's shape: the pin at `8ebaf8daad`, at `651150fc88`,
  its date and setting commit, `CANNOT (no network)` for the author's
  release) and § The device trees (the DTS-by-unit table: the board, the
  `#include` target, the dt-id, the `model` line). **T11's audit**
  (`docs/audits/2026_10_25-epic-m6-device-generic-x64-and-kernel/02-forward-audit.md`)
  § The boot files, and its errata F-09 in `device-generic-x64-and-kernel.md`.
- `docs/reviews/order.md` § T25 and § 1 item 4 (*"Unshipped is not dead ...
  a table row records the target; it is not a proposal to remove support"*).
- `docs/blindspot-register.md` entries **13**, **22**, **46**, **51**, **75**.
- Decisions: D-WORKFLOW-185 (the shipped-device set and the first
  widening), **D-WORKFLOW-209** (a table removes nothing), 184, 186, 187,
  188 (the order's fourth version), D-UI-079, D-INFRA-025/026.
- Issues: #672, #1082, #658, #674, #675, #670, #671, #653, #346, #585.
  Every `gh` call carries `--repo pixelelated/distribution`.

## 4. The questions

All seven apply (plan § 4); for a reachability table Q6 is the spine, Q4,
Q5 and Q7 hang off it, and Q1, Q2 and Q3 apply as counts.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A recipe among the 52 pinned to a retired host or series (rows only; no probe) | the `PKG_URL` hosts, listed |
| Q2 Standards | `tools/pkgcheck` over the 52 recipe rows (the tree's copy), the baseline counts first | the run's counts and FAIL list; a FAIL on an upstream-carried recipe is recorded, never fixed here |
| Q3 Bugs | A defect in a fork-own unit -- the one fork-own row is a dead copy, so none is expected; a `bug` only for a fork-own defect, with `Already written:` | the row's reads |
| Q4 Currency | (a) the drift per unit against `651150fc88` by name (files that differ, the newest upstream commit, `--since='2026-06-01T00:00:00Z'` with the timestamp); (b) **the pin table** in T27's shape for every loader recipe under the twelve target directories (`u-boot*`, `rkbin`'s consumer, `qcom-abl`'s, `amlogic-boot-fip`'s): the pin at `8ebaf8daad` and at `651150fc88`, its setting commit, `CANNOT (no network)` for the author's release; (c) each target's `linux*.conf` header line (`# Linux/<arch> <version> Kernel Configuration`) beside the kernel recipe's version case for that target (the conf is T43's row; the one line is the configuration shape T27 hands down) | the two hashes, `git log -1 -S`, the conf's first line |
| Q5 Efficiency | What the 397 cost: files, lines, bytes (`git ls-tree -r -l 8ebaf8daad`), DTS 34,437 of 49,555; what the drift costs the next merge (226 files, +14,839 / -29,156 over the target set) | the listings |
| Q6 Dead ends | **The table**: one coverage row per path (397) and one unit row per target, project and `packages/**` unit (25), each with the reads that decided its reach (`Makefile`'s target line, `world`, `buildable_by`, the engine's references for a project), the tier, and the disposition in D-WORKFLOW-209's words -- `unshipped: target <X>, in world yes/no` ; `unshipped: first widening, held (D-WORKFLOW-185)` for RK3566 and RK3326 ; `dead, upstream-carried (#346's class)` for the nine projects, the 37 unshadowed `packages/**` rows and the three unreached rows inside the devices area (AMD64's `intel-ucode` pair, `dtbocfg`) ; `shadowed copy, override <path>, override reached|unshipped` for the 9 ; `fork-own edit in a shadowed dead copy; Already written: nothing inherited` for `packages/linux/package.mk` -- and **no removal proposed for any upstream-carried unit** | the table |
| Q7 Clarity | **The duplicate map**: the four Rockchip device names that duplicate ROCKNIX's, the 9 shadowed pairs with the override's reach, the `CONFIG_DEFAULT_HOSTNAME` strings across the generic copy, the override and the projects' confs (`@DISTRONAME@`, `@DEVICENAME@`: T40's and T43's rows, named not read) | `git grep -n` at the hash |

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. **The class proposal** -- the dead
upstream-carried units with their counts and their cost against their
value, in the maintainer's terms -- is one `Renovation` punch item whose
text the lane writes and whose outcome names the coordinator's post on
#346 (D-WORKFLOW-209); the lane posts nothing there.

**The ladder:** the guard for this class is the inventory's reach
(`tools/renovation-inventory`, P1's) and `tools/renovation-drift`; a shape
they miss (T11 found three in #1086) is a lead for the coordinator, not a
tool change here.

## 5. The evidence floor

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`, `git diff`, `git ls-tree`), a `Makefile` line,
   an `options` line, or a document's line.
2. Mechanical evidence outranks reading.
3. **For a table, the target is the tree and the record**: the at-hash
   files, `651150fc88` in the repository's own store (no fetch), the
   `Makefile`, `config/options`, the engine's scripts. **No plan generation**
   (the inventory's `buildable_by` came from plan runs in the container,
   and is cited as the inventory's, at `eb4763e3cc`), no build, no guest,
   no M7 root read.
4. An assertion that cannot fail is not evidence: **the positive control**
   for every reachability read is the shipped pair -- the block with the
   exclusion lifted returns the H700's 28 rows as `shipped`, and `grep -n
   '^H700:' Makefile` finds its target -- run once before any row says
   `unreached`; `packages/linux/package.mk` (the one `M` against the base)
   is the control for the provenance loop before any row says `identical`.
5. Subagent output is a lead, never evidence (D-WORKFLOW-183).

**Can this be done on the VM? No** -- a reachability table over files no
image carries; its bench is the tree and the record. Nothing here touches a
handheld, a cloud, a shared backend, a guest or a build.

**What never runs in this slice:** a build, a plan generation, a guest, a
fetch, a network read of any upstream or author (Q4's `CANNOT (no
network)` is the row), a `tools/council/run` call, a command against a
handheld, a read of an M7 root, and a change to any file under `packages/`
or `projects/` on this branch.

- **The host-side checks**, each with its command, exit status and summary
  line in `02-forward-audit.md`:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672
  cd "$D"; mkdir -p .qa-scratch/t25
  wc -l < .qa-scratch/t25/paths.txt                                                                     # 397
  tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1        # empty
  grep -n -E '^(AMD64|RK3326|RK3399|RK3566|RK3576|RK3588|S922X|SM4450|SM6115|SM8250|SM8650|SM8750):' Makefile | wc -l   # 12
  sed -n '42p' Makefile                                                                                 # world: no AMD64, SM4450, SM6115
  grep -n 'PROJECT=' Makefile | grep -v -c 'PROJECT=ROCKNIX'                                              # 0: no target builds another project
  tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git diff --name-status c445081a59 8ebaf8daad -- | sort | uniq -c   # 1 M (packages/linux/package.mk)
  tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git diff --name-status 651150fc88 8ebaf8daad -- | awk '{print $1}' | sort | uniq -c   # 39 M
  tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git log --oneline c445081a59..651150fc88 -- | wc -l   # 65
  for d in AMD64 RK3326 RK3399 RK3566 RK3576 RK3588 S922X SM4450 SM6115 SM8250 SM8650 SM8750; do printf '%s ' "$d"; git log --format=%h 651150fc88..8ebaf8daad -- "projects/ROCKNIX/devices/$d" | wc -l; done   # the fork's merge commits only; read each
  for p in ARM Allwinner Amlogic Generic NXP Qualcomm RPi Rockchip Samsung; do printf '%s ' "$p"; git grep -l -c "$p" -- Makefile config scripts | wc -l; done   # the engine's references; ARM 0
  git grep -n 'DEFAULT_HOSTNAME' 8ebaf8daad -- packages/linux projects/ROCKNIX/packages/linux | cut -c1-160
  git log --format='%h %ad %s' --date=short -3 -- packages/linux/package.mk projects/ROCKNIX/packages/linux/package.mk | cut -c1-120
  tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git ls-tree -r -l 8ebaf8daad -- | awk '{b+=$4} END {print b " bytes"}'
  # the positive control: the shipped pair's rows and target under the same reads
  grep -n -E '^(H700|SM8550):' Makefile | wc -l                                                         # 2
  ```
- **The two tables' generation** is a script the lane keeps under the audit
  folder's `tools/` (as T13's `t13-shapes.py`): the coverage rows from
  `.qa-scratch/t25/rows.tsv` with the per-row reads joined, so the 397 rows
  and the 25 unit rows are regenerated, not typed, and `02` carries the
  command that regenerates them and its row counts.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#672`
(`Refs #672`); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-devices-unshipped/00-running-log.md` | the flight recorder: model and effort, `reviewed-at` with `8ebaf8daad` beside it, every § 5 command with its exit status, the VM question, the statement that nothing of § 5's list ran | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 397 re-derived with § 2's block and its output, the unit table (25), the provenance (one `M` against the base; 39 `M` and 65 commits against `651150fc88`, named), the branch's deltas from the hash (none expected) | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #672's checklist, plus **a coverage table with one row per path** (397; the first cell the path in backticks so ``grep -c -E '^\| `(packages|projects)/'`` counts them), **§ The units** (25 rows), **§ The targets** (12 rows: target line, `world`, arch pair, loader, GPU stack, DTS count, conf, patch count as T43's, fork edits, drift against `651150fc88`), **§ The projects** (9 rows), **§ The pins** (T27's shape), **§ The device trees** (one row per DTS, 53: the board, the `#include` target, the dt-id, the `model` line, the target directory; none shipped), § Mechanical checks (every § 5 command), § Positives, every proof with `proved:` | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the base merge x the 39 drifted paths; T23's unshipped generic rows x the twelve targets; T43's and T40's patch rows x the targets and projects; T11's kernel override x the shadowed generic copy | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), **§ Renovation face** Q1 to Q7, **Q6 carrying the unit table's dispositions** (25 rows, each with `Already written:` where a fork edit exists -- one), **Q7 carrying the duplicate map**, Q4 the drift and pin tables | B |
| Second opinions | `.../second-opinions/review-plan.json` | § 1's Local plan file with `tier_exception` and `reason`; no call | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` with the `review-plan: local at epic tier under D-WORKFLOW-184` line | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`; the #346 class proposal as one `Renovation` item whose outcome names the coordinator's post; the first-widening pair as one recorded item; the fork-own dead-copy row as one recorded item | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #672 | `Audit: M6 T25 the devices the fork does not ship and the other projects -- N findings (...)`; one checkbox per item, agent-first | D |
| **The stage-D pause** | #672 | the punch list posted; the lane waits for the coordinator's dispositions (no stream is expected: nothing here changes) | D |
| Verification | `02-forward-audit.md` appended; `audit-completion.json` after the coordinator closes the audit issue | every proof's `proved:` cell one of `tree`, `history`, `tool-run` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-devices-unshipped.md`, posted on #672 | the mini-retro's four answers, the scoped audit's checks (its check 7 step 5 included); **what the slice did to the two time-to-play numbers** (nothing: say so); **what T28 inherits** (the drift cell read against a named upstream head; the target-row shape) | G |
| Hand-back | #672 | `reviewed-at:` and `fixed-at:` in the body (the same commit when nothing changed); one comment: the tip, each artifact by path, the six checker exit codes | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-devices-unshipped-672.md` | seeded by the coordinator; updated at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session headed `#672`, stamped from the clock, prose through a quoted heredoc | every session |

## 7. Acceptance

The checklist on #672 is the contract (its body carries these fourteen,
written there with this version in place of the five generated ones; where
the two differ, #672 wins and the coordinator corrects the brief). Each
names the artifact that ticks it; the coordinator ticks at hand-back.

- [ ] `docs/audits/<date>-epic-m6-devices-unshipped/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-devices-unshipped/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and a `reason` naming plan § 6c and `slices.json`'s `k: 25`; `00-running-log.md` records no `tools/council/run` call.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#346 for the class proposal, a Backlog the coordinator files, T43's or T40's issue for a patch row), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits (the same commit where nothing changed; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the block of brief § 2 with its output (397 paths, 49,555 lines; unreached 216, unshipped 181; upstream-carried 396, fork-own 1; the 25 units with their counts, or the deltas beside them), and the provenance line: 1 `M` against `c445081a59`, 39 `M` and 65 commits against `651150fc88`, named as the upstream head read.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `(packages|projects)/' 02-forward-audit.md`` prints 397; each row's reach cell names the read that decided it (`Makefile:<line>`, `buildable_by`, the engine's reference or its absence), and the table is regenerated by a script under the audit folder's `tools/` whose command and counts `02` quotes.
- [ ] `02-forward-audit.md` § The targets has 12 rows (target line in `Makefile`, in `world` yes/no, arch pair, loader, GPU stack, DTS count, conf, fork edits none, drift against `651150fc88`), § The projects 9 rows (purpose, the engine's references by `file:line` or none, fork commits 0, drift empty), § The pins one row per loader recipe under the twelve target directories in T27's shape, and § The device trees one row per DTS (53) with the board, the `#include` target, the dt-id and the `model` line.
- [ ] `02-forward-audit.md` § Mechanical checks records, with command, exit status and summary line, each of brief § 5's checks: the branch-vs-hash diff (empty), the 12 target lines, the `world` line, the `PROJECT=` count (0), the three provenance loops (1 M; 39 M; 65), the per-target fork-commit loop (merges only), the engine-reference loop (ARM 0), the hostname grep, the byte total, and the positive control (the shipped pair's 2 target lines and its rows read as `shipped` with the exclusion lifted).
- [ ] `04-analysis.md` § Renovation face Q6 carries the unit table: 25 rows, each with its disposition in D-WORKFLOW-209's words (`unshipped: target <X>, in world yes/no`; `unshipped: first widening, held (D-WORKFLOW-185)` for RK3566 and RK3326; `dead, upstream-carried (#346's class)`; `shadowed copy, override <path>, override reached|unshipped` for the 9 shadowed rows' units; `fork-own edit in a shadowed dead copy; Already written: nothing inherited` for `packages/linux/package.mk`), and no row proposes a removal of an upstream-carried unit; § Q7 carries the duplicate map (the four Rockchip names, the 9 shadowed pairs, the hostname strings); § Q5 states the slice's bytes and lines and the drift's 226 files.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history` or `tool-run`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c 'PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; the #346 class proposal is one `Renovation` item whose outcome names the coordinator's post; no file under `packages/` or `projects/` is changed on this branch (`git diff --stat 8ebaf8daad <fixed-at> -- packages projects` empty).
- [ ] The retro exists at `docs/retros/<date>-m6-devices-unshipped.md`, is posted on #672, says in those words that the slice did nothing to the two time-to-play numbers, and names what T28 inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` at the hand-back tip (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#672; a blocker named on #672 (two commands that disagree; a block whose
output differs from § 2's beyond the deltas it records); a branch that
differs from `8ebaf8daad` on one of the 397 at stage A; or an execution
limit, stated as such with the running log current. A checkpoint is not a
stop. An idle session says it is idle on #672, **and does not end a turn on
a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#672`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #672` or the
  guard.
- The VM question written before any proof (§ 5: no).
- The mini-retro at stage G, posted on #672, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 (a fix's positive exercises the job the fix
  could break -- here there is no fix, so the step is marked so).
- A register row the same session for any decision the slice forces (none
  expected); the highest Decided row on 2026-10-25 is D-WORKFLOW-209, the
  coordinator's; T22 runs beside this lane and may take the next IDs, so a
  row this slice forces takes one the coordinator assigns on #672.
- `tools/ceremony-check` before every push; never `--no-verify`; a merge
  with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; the read tree is the worktree at
  the hash (no export needed: nothing is compared across trees); anything
  temporary under `/workspace/tmp/m6-t25/` after `df -i`, never `/tmp`.
- Commit messages `docs: ...`, with `Refs #672`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#672's checkboxes against their artifacts; the lint's `PASS` line with the
D-WORKFLOW-184 line; `review-plan.json`; the audit issue's checkboxes all at
an outcome; the coverage table's row count (397), the unit table's (25),
the targets' (12), the projects' (9) and the device trees' (53); every Q6
row's disposition and no removal; **re-running on a clone of the branch at
the tip under `/workspace/tmp/m6-coordinator/`: the membership block, every
§ 5 check in full and the positive control**; `register-check` on a
simulated merge with the coordinator's tip (the ledgers united); the retro's
four answers; the six exit codes. The lane posts one hand-back comment
naming the tip and each artifact by path, writes `reviewed-at:` and
`fixed-at:` into #672's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, merges the branch in its turn
after the M7 candidate (after T27's), regenerates the ledgers, posts the
#346 class proposal in the shape the lane wrote, and closes #672 when every
row is proven.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#1082) carries a T25 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

---
slice: T11
id: device-generic-x64-and-kernel
issue: "#658"
epic: "#1082"
area: devices
kind: read
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

# T11: the GENERIC_X64 VM device, the kernel and drivers recipes, and the project's boot files

## 1. Identity

- **Issue:** #658 `M6.P2 E1082/T11: devices: the GENERIC_X64 VM device, the
  kernel and drivers recipes, and the project's boot files`, slice
  `device-generic-x64-and-kernel` (`k: 11`) in `docs/reviews/slices.json`,
  eleventh in `docs/reviews/order.md` (its row: *58 | 10,418 | 1,820 |
  1,421 | Independent*; its `why`: *GENERIC_X64 is the fork's own (989
  fork-own lines) and the VM every proof runs on; the kernel recipes and
  project bootloader serve every device; its fork-written kernel
  configuration (7,754 lines) is read here as a diff against its base
  (plan § 2); the test image (D-WORKFLOW-185), read with the harness that
  boots it under D-WORKFLOW-186 [...]* -- **two of those words are corrected
  below**: the 989 does not reproduce, and the configuration has no base).
  **Epic:** #1082 (the devices: T11 first, then T27, T28, T25; its futro
  `docs/futros/2026-10-25-m6-devices.md`). **Milestone:** M6; its body
  holds the live order; read it first.
- **Predecessors that bear on these files:** **T5** (#652, the build
  engine: its E1 edited `bootloader/mkimage` lines 82 and 110 on T5's
  branch, F-16; its F-17/#836 moved `kernel-firmware`'s `PKG_NEED_UNPACK`;
  `scripts/image:280` runs `bootloader/install` and `scripts/mkimage:225-263`
  sources `bootloader/mkimage`); **T12** (#659, the VM harness under
  `tools/`: `vm-serial`, `vm-qa`, `vm-visual-qa`, `vm-pair` and the rest,
  which call the guest's launcher **by basename** -- `generic-x64-vm run
  --headless` at `tools/vm-serial:8`, `tools/cloud-round-trip:504/513/607`,
  `tools/cloud-test-backend:8`; `tools/last-good-scripts-test:3400-3414`
  names its path. There is **no `tools/generic-x64-vm`**: the launcher is
  `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm`, 817 lines of
  Python, **this slice's**, and #659's body names only
  `generic-x64-vm-testing.md`, so what T12 read of the launcher is a
  question for its `02`, not a fact); **T40** (#687: class (a), the
  277 generic kernel patches dead because `get_pkg_directory linux` resolves
  to the override on every device, and § The x86_64 five, where
  EmulationStation's `cpugov.patch` is reached by GENERIC_X64 and never
  applied -- cite, do not re-derive); **T23** (#670: no row under this
  slice's paths); **T22** (#669: the GENERIC_X64, AMD64 and QEMU quirks are
  its, not this slice's); **T27** and **T28** (the handhelds; the same
  override recipe builds their kernels, and T27 reads its configuration the
  way this slice sets). Register: **D-WORKFLOW-185** (the shipped set: H700
  and SM8550; GENERIC_X64 the test image, built and read, never shipped),
  **D-WORKFLOW-186** (the build process ahead of any device), **D-WORKFLOW-187**
  (the renovation gates no release), **D-QA-053** (GENERIC_X64 is a
  developers' tool and never a gameplay image), **D-QA-052** (the guests
  render in hardware: virtio-gpu-gl, egl-headless), **D-QA-054** (the
  loopback ssh command is not gated on the guest's address), **D-WORKFLOW-114**
  (0.0.1's support matrix), **D-INFRA-028** (a preflight reports; it never
  stops a guest), **D-WORKFLOW-209** (the removal rule), **D-WORKFLOW-195**
  (the trimmed packet); open: D-WORKFLOW-191.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #658, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` for a defect it proves (D-WORKFLOW-187). A fix to one of the 58 is a
  stage-E stream the coordinator writes after the stage-D pause.
- **The rule (D-WORKFLOW-209).** At stages A to D the lane **changes none
  of the 58 and nothing under `packages/`, `projects/` or `tools/`**; a
  dead end is a disposition in the table, never a removal; the class
  decision for anything upstream carries is the maintainer's on #346.
- **One worktree, one session.** Branch `feature/m6-device-generic-x64-658`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-device-generic-x64-658`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #658). **Before that
  comment exists nothing runs in it.** The session is the T5 lane's
  (`m6-t5-build-engine`), which ran T5, T6, T7, T8, T9, T12, T45, T23 and
  T40; those worktrees stay beside this one, idle, and nothing is written
  there. The primary checkout stays on `next` (D-INFRA-025); the legacy
  checkout and `rocknix.worktrees/*` are the M7 lane's, read only. **The
  rules in this worktree are `next`'s except the paths the dispatch comment
  lists.**
- **Model and effort:** Opus 5.5 at high effort. Record what ran in
  `00-running-log.md`'s header.
- **Review depth: Independent** (plan § 6c, `slices.json` k 11: *an
  ordinary code slice*): **one seat, GPT-6 Astra at `max`**, a probe first
  (identity, effort, provider from the provider's own field), then one
  refutation pass over one packet, as T13's stage C did (its
  `second-opinions/` on `feature/m6-cloud-harness-660` is the model: the
  probe, the packet manifest with sha256s, the scan, the refutation's
  provenance). The packet (D-WORKFLOW-195): the 14 read paths whole (1,820
  lines), the kernel configuration's header and its diff against the
  Generic conf (not the 7,754 lines), the four bootloader scripts, `02`,
  `03` and `04` whole, and the three context sections (the order's § T11,
  this brief's § 2 and § 4, D-WORKFLOW-185/186/187 and D-QA-053 quoted).
  **The packet is scanned before it is sent** (`tools/forbidden-terms-check
  --stdin` and the pre-commit's patterns, plus T10's widened set read with
  `git show feature/m6-tooling-guards-657:.githooks/secret-patterns`; a hit
  is a finding and the packet redacts it). **Every other `tools/council/run`
  call carries `COUNCIL_ENV_FILE=/nonexistent`**, `--help` included (T13's
  rule break, 05:2x). The seat's verdicts are graded in `04` § Second
  opinion: confirmed, narrowed, refuted, new -- the decisive ones re-read at
  their lines by the lane, the rest marked *accepted on the seat's
  citation*.
- **The host, read on 2026-10-25 by the coordinator:** M6's; the M7 lane
  holds a full build window (GENERIC_X64, then H700, then SM8550, with its
  qualification guests); T13's guest cycle is held behind its FINAL
  RETURN; T15's serial host suite runs on M6's retained donor. **This slice
  runs no guest, no build, no compiler, no plan generation and no network**
  at stages A to D: the device it reads is the guest, whose boot and
  harness proof T12 recorded; a guest cycle is asked for on #658 only if a
  punch item needs one, and granted by the coordinator after the FINAL
  RETURN. `TMPDIR` under `/workspace/tmp/m6-t11/`. Register: the three
  workflow IDs before 209 and D-INFRA-032 are the M7 lane's; 209 the
  coordinator's; a row this slice forces takes **D-WORKFLOW-210 or
  higher**, D-QA-064, D-INFRA-033 or higher.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-generic-x64-658
cd "$D"
git branch --show-current                                            # feature/m6-device-generic-x64-658
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists
cat .github/sessions/saved-session-state-feature-m6-device-generic-x64-658.md   # seeded by the dispatch
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo "upstream/next at 651150fc88 is here"   # read, never fetched
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-device-generic-x64-658
```

No `git fetch` of any kind: `651150fc88` is already in the repository
(`git rev-parse` proves it); the read is at `8ebaf8daad` and the upstream
delta at `651150fc88`, both local.

## 2. Scope

**58 paths, 10,418 lines; 14 of them read (code: shell, Python, recipe,
systemd, udev; 1,820 lines, 1,421 fork-own); fork-own 11 paths / 1,738
lines, upstream-carried 46 / 926, vendor-carried 1 / 7,754 (the kernel
configuration, `tier_note: fork-written`, area `patches-and-configs`);
reach shipped 49, test 9 (the nine are all `devices/GENERIC_X64`).** The
membership is `slices.json` k 11's rule on `inventory.json` at
`2174265e9c`: area `devices` with reach `shipped`, `test` or `n/a` under
the globs `projects/ROCKNIX/devices/GENERIC_X64/**`,
`projects/ROCKNIX/packages/**`, `projects/ROCKNIX/{bootloader,filesystem}/**`,
`projects/ROCKNIX/{options,config.xml}`, `packages/**`; **plus** area
`patches-and-configs` under `projects/ROCKNIX/devices/GENERIC_X64/linux/*.conf`.
`tools/renovation-inventory` has no single-slice selector (`--order` sizes
all 46), so the block reproduces the rule with the tool's glob semantics
(`**` crosses directories, `*` does not, `{a,b}` alternates):

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)   # the loop below escapes each character once
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
A=[rx(g) for g in ("projects/ROCKNIX/devices/GENERIC_X64/**","projects/ROCKNIX/packages/**","projects/ROCKNIX/{bootloader,filesystem}/**","projects/ROCKNIX/{options,config.xml}","packages/**")]
B=[rx("projects/ROCKNIX/devices/GENERIC_X64/linux/*.conf")]
t=[r for r in rows if (r["area"]=="devices" and r["reach"] in ("shipped","test","n/a") and any(p.match(r["path"]) for p in A)) or (r["area"]=="patches-and-configs" and any(p.match(r["path"]) for p in B))]
CODE={"assembly","c","c++","c++-header","c-header","cmake","css","docker","go","html","javascript","kconfig","lua","make","perl","python","recipe","rust","script","shader","shell","systemd","typescript","udev"}
read_=[r for r in t if r["tier"]!="vendor-carried" and r["reach"]!="unreached" and (r.get("language") or "") in CODE]
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",len(read_),sum(r["lines"] or 0 for r in read_),"fork-own read",sum(r["lines"] or 0 for r in read_ if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("GENERIC_X64 fork-own lines",sum(r["lines"] or 0 for r in t if r["path"].startswith("projects/ROCKNIX/devices/GENERIC_X64/") and r["tier"]=="fork-own"))
import os; os.makedirs(".qa-scratch/t11", exist_ok=True)
open(".qa-scratch/t11/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))
print("written", len(t), ".qa-scratch/t11/paths.txt")'
# paths 58 lines 10418
# read 14 1820 fork-own read 1421
# tier {'fork-own': 11, 'upstream-carried': 46, 'vendor-carried': 1} reach {'shipped': 49, 'test': 9}
# GENERIC_X64 fork-own lines 1217
# written 58 .qa-scratch/t11/paths.txt
```

(Version 1's block printed 57 paths: its `{a,b}` alternation was escaped twice, so `config.xml` never matched, and it never wrote `paths.txt`; the stranger's proof caught both.)

A different count is a delta to record with the command, not a reason to
stop. **The order's "989 fork-own lines" is an erratum**: GENERIC_X64's
fork-own rows sum to 1,217 lines over 8 paths (`vm/generic-x64-vm` 817,
`vm/README.md` 138, `options` 91, `profile.json` 52,
`serial-debug-shell.service` 41, `sway-generic-x64` 40,
`utm-bundle-readme.txt` 35, `10-generic-x64-renderer.conf` 3), 175 without
`vm/*`; no subset gives 989.

**By directory group** (paths / lines): `devices/GENERIC_X64` 9 / 8,971
(the configuration 7,754; the eight above); `packages/linux` 6 / 460 (the
override recipe `package.mk` 432, **fork-own** in the inventory with `overlap:
true` -- it is upstream's file the fork touched once, `3d7c075f63`, and the
tier rule marks it so; 20 patches; 42 commits on the file since June, 2 of
them the fork's (`3d7c075f63`, `dc948f59aa`), 50 on the directory; `sysctl.d/qdisc.conf`;
`udev.d/10-bfq-sched.rules`; three more); `packages/kernel-drivers` 9 /
357; `packages/linux-firmware` 26 / 143 (lists; 22 of the 26 rows carry no
line count, `lines: null`, and the 143 are the other four's: 93, 25, 24, 1);
`packages/linux-drivers/rocknix-joypad/package.mk` 1 / 25;
`bootloader/install` 80 (fork-own), `mkimage` 113, `release` 5, `rkhelper`
60; `config.xml` 154 (26 upstream commits since June, 0 fork);
`options` 41; `filesystem/etc/machine-info` 9 (fork-own, `rasterabot`,
2026-10-01).

**The kernel configuration has no base in the tree.**
`devices/GENERIC_X64/linux/linux.x86_64.conf` line 3 reads `# Linux/x86
6.15.6 Kernel Configuration` (7,754 lines); the override recipe builds
**7.1.2** for `RK3326|AMD64|GENERIC_X64`
(`projects/ROCKNIX/packages/linux/package.mk:36-40`), copies the device's
conf, runs `kernel_make listnewconfig` and `yes "" | kernel_make oldconfig`
(the recipe's configure step, about lines 306-314), so every option new
between 6.15 and 7.1 takes its default at build time and **the committed
file is not the configuration the kernel is built from**. Measured
candidates (`diff` line counts, removed / added): the AMD64 conf
(`devices/AMD64/linux/linux.x86_64.conf`, 12,445 lines, 7.1.2, unchanged
since the adding commit's parent `cb50b45f6e`): 7,671 / 2,980, not a base;
LibreELEC's `projects/Generic/linux/linux.x86_64.conf` (8,062 lines,
7.1.2): 659 / 351, the nearest. The adding commit `73b20caf86` (2026-06-30,
"Re-derived from origin/x64-build-fix", Copilot co-authored) names none;
the fork's own edits since are 13 lines in two commits (`1cd0093d67`,
2026-07-26, `FW_CFG_SYSFS`, 2 lines; `cbf75c0b06`, 2026-09-10, `WATCHDOG`
x3, `I6300ESB_WDT`, `PSTORE` x5, 11 lines). The slice does not build: it states
the three parts (§ 4 Q1) and proposes the regeneration as a packet.

**The project's boot files are four scripts.** `bootloader/install` is
absent at `651150fc88` (added by `73b20caf86`, last `7178f1b1f3`
2026-09-02) yet opens `# Copyright (C) 2024-present ROCKNIX`; `scripts/image:280`
runs it through `find_file_path bootloader/install`; its `syslinux` branch
is the one GENERIC_X64 and AMD64 take (`BOOTLOADER="syslinux"`,
`devices/GENERIC_X64/options:27`), its `u-boot` and `qcom-abl|arm-efi`
branches echo **by design** -- H700 (`BOOTLOADER="u-boot"`) and SM8550
(`qcom-abl`) both land there, and `install:51-58` says the loader is written
at image time by `mkimage_abl` (`7178f1b1f3`), so the echo is not a missing
loader; its `grub` branch tracks a path upstream deletes (`e6da8dad2b`); it
also has a `systemd-boot` branch (line 35) and a default `*)` (line 68) that
attempts a copy, which no shipped device reaches. `mkimage` differs from upstream by 24 lines (7 added, 17 removed), is
sourced by `scripts/mkimage:225-263`, and T5's E1 changes 15 of its lines on
T5's branch (`feature/m6-build-engine-652`, tip `52e6794ba7`: every `mcopy`
gains `>"${SAVE_ERROR}" 2>&1 || show_error`; F-16; that branch merges
before this one). `release` (5 lines) is run by `scripts/image:285`. `rkhelper` (60 lines) is
`reach: shipped` by placement; whether any shipped device reads it is § 4
Q6's question.

**What `upstream/next` (`651150fc88`) already changes:** 7 of the 58 are
`M` (`bootloader/mkimage`, `config.xml`, `linux-drivers/rocknix-joypad/package.mk`,
`linux-firmware/extra-firmware/package.mk`, `linux/package.mk`,
`linux/sysctl.d/qdisc.conf`, `linux/udev.d/10-bfq-sched.rules`;
`c803640655` 2026-10-16 bumps the RK35x6/S922X kernel in the override);
the 11 `D` are fork-only files that never existed upstream (the GENERIC_X64
device, `bootloader/install`, `machine-info`), not deletions. The upstream
cleanups of 2026-10-22 (`e6da8dad2b` grub, `05fc864362` qualcomm u-boot in
mkimage, `cafbb1657d` Qualcomm to Boot Loader Spec) land after the merge
base `c445081a59`.

**History since 2026-06-01 at `8ebaf8daad`:** 110 non-merge commits on the
58; **40 fork-authored** (Max Engel 36: 34 on `devices/GENERIC_X64`,
`7178f1b1f3` on `install`, `dc948f59aa` on the override recipe; blitterbot
3: `3d7c075f63` on the override recipe, `d6e8390c93` 2026-10-05 and
`bed8e2bb1e` on the device; `rasterabot` 1: `98e1a30362`, `machine-info`)
and 70 upstream (by group, with overlap: `packages/linux` 40, `config.xml`
26, `linux-firmware` 7, `linux-drivers` 5, `bootloader` 4, `kernel-drivers`
2, `options` 1; 70 after de-duplication). **Three fork identities**: a count by author
that forgets `rasterabot` prints 39.

**What the slice's globs do not take, so it does not read them:** the
generic `packages/linux/package.mk` (358 lines, `tier=fork-own`,
`reach=unreached`, shadowed by the override, which is a full recipe and
does not source it -- why it is marked fork-own is § 4 Q2's question, by
`git log`, not by reading the file whole); the per-device aggregators
`virtual/linux-drivers` and `virtual/linux-firmware` (area
`generic-packages`); `graphics/gpudriver` (unshipped); every generic
`packages/linux-firmware/*` (unreached); the GENERIC_X64, AMD64 and QEMU
quirks under `hardware/quirks/platforms/` (T22, #669); T40's 277 dead
generic kernel patches (class (a)).

## 3. Read first

1. `.claude/rules/` from `next`: `engineering-practices.md` (verify the
   artifact; a name is not a behaviour; a count is a claim about one tree;
   `rc=$?` on its own line), `generic-x64-vm-testing.md` (the guest, the
   harness, what the guest's busybox lacks), `device-builds.md` (the build
   command, the image step, the bootloader's place in it,
   `tools/build-preflight`), `vm-first.md`, `bugs-are-agent-first.md`,
   `upgrade-and-install.md`, `decision-register.md`, `issue-tracking.md`,
   `packaging-and-patches.md`, `working-principles.md` (the pre-flight).
2. `docs/reviews/plan-for-the-plan.md` § 2 (the kernel-configuration diff
   rule), § 6b (the procedure), § 6c (depth); `docs/reviews/order.md` § T11,
   § T25, § T27, § T28; `docs/futros/2026-10-25-m6-devices.md`.
3. The register rows named in § 1, by ID; `docs/blindspot-register.md`
   entries 22, 31, 75.
4. T5's `02-forward-audit.md` E1 and F-16/F-17 (on `feature/m6-build-engine-652`,
   read with `git show`); T12's `02` on the harness (`feature/m6-tooling-vm-harness-659`);
   T40's `02` § The x86_64 five and § Classes (`feature/m6-patches-dead-687`,
   `git show` only); T13's `second-opinions/` as the seat's model
   (`feature/m6-cloud-harness-660`).
5. `scripts/image` (the image step: where `bootloader/install` runs and
   what it is given), `scripts/mkimage` (where `bootloader/mkimage` is
   sourced), `config/functions` (`get_pkg_directory`, `find_file_path`),
   `scripts/unpack:120-135`.

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`design`):

- **Q1 Modernize -- the configuration and the launcher.** (a) The kernel
  configuration: state the three parts -- the nearest candidate and its
  removed/added counts (the Generic conf, 659 / 351; the AMD64 conf, 7,671
  / 2,980, named as not a base); the fork's own edits since the adding
  commit (`git log -p 73b20caf86..8ebaf8daad -- <conf>`, the 13 lines);
  the built-versus-committed gap (what `listnewconfig` would answer at
  7.1.2, stated from the recipe, **not built**: the slice names the
  regeneration as a packet, an open item, and says what a reviewer would
  compare after it). (b) `vm/generic-x64-vm` (817 lines) against the
  `tools/vm-*` that call it by basename (how the name resolves: `PATH`, a
  symlink, an install step -- read `generic-x64-vm-testing.md` and the
  callers' lines), what the callers assume of its flags, what the device
  directory should carry and what `tools/` should (a design, deferred to the
  coordinator; no edit).
- **Q2 Standards -- the headers and the marks.** `bootloader/install` is
  the fork's file under an upstream copyright header (`fork-workflow.md`:
  preserve upstream credits and add a ROCKNIX line -- here the reverse
  case: a fork-authored file must say so); the configuration's header
  names a kernel the recipe does not build; why the generic
  `packages/linux/package.mk` is marked fork-own (`git log --format='%h %an
  %s' 8ebaf8daad -- packages/linux/package.mk | head`: an upstream file
  the fork touched, or the inventory's tier rule) -- each a finding with
  its line, a `bug` only where behaviour is wrong.
- **Q3 Bugs -- what is wrong, read.** The `oldconfig` gap is a provenance
  defect, not a build failure: say whether any built image's configuration
  differs from the committed one in a way a reader of the file would be
  misled by (the 13 fork lines and the 6.15-to-7.1 options), and file it as
  a `bug` with its trace only if the file misleads a behaviour claim
  (`Already written:` the images built from it, nothing on a device).
  `install`'s echo branches are the design for H700 and SM8550 (the image
  step writes their loaders, `install:51-58`): not a bug. The questions are
  whether `install` says so where a reader lands (its header; Q2), and
  whether its `systemd-boot` and default `*)` branches are reached by any
  device at all (`grep -n BOOTLOADER projects/ROCKNIX/devices/*/options`
  for the shipped three and the rest): unreached ones are dead ends (Q6),
  a reached one whose copy would fail is a `bug` with its trace. T40's `cpugov.patch` is #1072's, cite.
- **Q4 Package currency.** The override recipe's kernel versions per device
  (`package.mk:36-40` at `8ebaf8daad` and at `651150fc88`, the
  `c803640655` bump), the GENERIC_X64 kernel 7.1.2 against the kernel's
  current stable (read from the recipe and `PKG_URL`, no fetch: the slice
  records the pin and the date, and the upstream bump that moves it);
  the firmware lists' upstream delta (`extra-firmware`); `rocknix-joypad`'s.
- **Q5 Efficiency.** The configuration's size against the Generic conf's
  for a QEMU guest (what the 351 added lines enable; whether the 659
  removed ones are the guest's or an AMD64 handheld's); the nine
  `kernel-drivers` recipes against the devices that reach them
  (`reachable_by`); `machine-info` on every image.
- **Q6 Dead ends -- what is carried and nobody reads.** `rkhelper` (who
  reads it: `grep -rn rkhelper scripts/ projects/ packages/ tools/`);
  `install`'s `u-boot`, `qcom-abl|arm-efi` and `grub` branches (upstream
  deleting grub); `README.md`'s and `utm-bundle-readme.txt`'s UTM/macOS
  instructions after D-QA-053 and D-QA-052; `profile.json`; any
  `kernel-drivers` or `linux-firmware` list no shipped device reaches.
  Dispositions per unit, removals none (D-WORKFLOW-209); fork-own dead
  units proposed on the punch list, deferred to the coordinator.
- **Q7 Clarity and structure.** Can a reader tell from the GENERIC_X64
  directory what the guest is for (D-QA-053) and how it is booted (T12's
  harness or the device's own `vm/generic-x64-vm`)? Does `options` say why
  `BOOTLOADER="syslinux"` and `UBOOT_SYSTEM`'s absence; does the
  configuration say where it came from?

## 5. The evidence floor

1. Tracker state is never sole evidence: every cell cites a command's
   output or a file:line at `8ebaf8daad`.
2. Mechanical evidence outranks reading: `diff` counts, `git log`
   counts with the three identities, `grep -n` on the scripts, the
   inventory's rows; a comment in a file is the author's claim (blindspot
   31).
3. **The bench is the host; no guest, no build, no plan, no fetch.**
   **Can this be done on the VM? Yes -- on the host, with no network:** the
   device this slice reads is the guest, whose boot and harness proof T12
   (#659) recorded; every read, diff, log and script-branch read runs on
   the build host at `8ebaf8daad` with `651150fc88` read locally. A guest
   cycle is asked for on #658 only if a punch item needs one (the
   coordinator grants it after the M7 lane's FINAL RETURN); none is
   planned. No handheld, ever. `tools/council/run invoke` runs once, the
   Phase 4.6 seat.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The runs, with what the coordinator read** (the lane runs each at stage
A in its worktree and records the exit, the wall time and the summary
line; `TMPDIR` under `/workspace/tmp/m6-t11/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-generic-x64-658
cd "$D"; export TMPDIR=/workspace/tmp/m6-t11/tmp; mkdir -p "$TMPDIR" .qa-scratch/t11
# the membership block (§ 2) -> .qa-scratch/t11/paths.txt (58)
# the configuration against its candidates (expect 659 / 351 and 7,671 / 2,980; order: removed, added)
C=projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf
for b in projects/Generic/linux/linux.x86_64.conf projects/ROCKNIX/devices/AMD64/linux/linux.x86_64.conf; do git show "8ebaf8daad:$b" > "$TMPDIR/base.conf"; git show "8ebaf8daad:$C" > "$TMPDIR/ours.conf"; echo "$b removed=$(diff "$TMPDIR/base.conf" "$TMPDIR/ours.conf" | grep -c '^<') added=$(diff "$TMPDIR/base.conf" "$TMPDIR/ours.conf" | grep -c '^>')"; done
git show "8ebaf8daad:$C" | sed -n '3p'                                   # Linux/x86 6.15.6
git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '30,45p' | grep -n -E 'PKG_VERSION|GENERIC_X64'   # 7.1.2 for RK3326|AMD64|GENERIC_X64
git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | grep -n -E 'listnewconfig|oldconfig'
git log --format='%h %ad %an %s' --date=short 73b20caf86..8ebaf8daad -- "$C"    # the fork's edits since the adding commit
# the history with the three identities (expect 110 non-merge; 40 fork, 70 upstream)
tr '\n' '\0' < .qa-scratch/t11/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since=2026-06-01 8ebaf8daad -- | tee "$TMPDIR/hist.txt" | wc -l
grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"; grep -v -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"
# the upstream delta (expect 7 M, 11 D; the D are fork-only files)
tr '\n' '\0' < .qa-scratch/t11/paths.txt | xargs -0 git diff --name-status 8ebaf8daad 651150fc88 -- | awk '{print $1}' | sort | uniq -c
# the boot files: who runs them (expect scripts/image:280 install; scripts/mkimage sources mkimage)
grep -n -E 'bootloader/(install|mkimage|release|rkhelper)' scripts/image scripts/mkimage scripts/* config/* 2>/dev/null | cut -c1-120   # image:280 install, image:285 release, mkimage:225-263
git show 8ebaf8daad:projects/ROCKNIX/bootloader/install | grep -n -E '^\s*[a-z|-]+\)|echo' | cut -c1-100
git cat-file -e 651150fc88:projects/ROCKNIX/bootloader/install 2>/dev/null && echo upstream-has-install || echo fork-only-install
grep -rn -E '^\s*BOOTLOADER=' projects/ROCKNIX/devices/*/options | cut -c1-100
grep -rn rkhelper scripts/ projects/ packages/ tools/ 2>/dev/null | grep -v '^projects/ROCKNIX/bootloader/rkhelper' | cut -c1-120
# the generic recipe's mark (expect: who touched packages/linux/package.mk, why fork-own)
git log --format='%h %ad %an %s' --date=short 8ebaf8daad -- packages/linux/package.mk | head -5
# the launcher, read, not run (python; no guest)
python3 -I -c 'import ast,sys; t=ast.parse(open(sys.argv[1]).read()); print(len([n for n in ast.walk(t) if isinstance(n,ast.FunctionDef)]),"functions")' projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
grep -rn -E 'generic-x64-vm' tools/ .claude/rules/generic-x64-vm-testing.md | grep -v '^tools/.*:#' | cut -c1-120 | head -12   # the callers by basename; no tools/generic-x64-vm exists
# the removal rule's own check against the dispatch tip (expect empty; against 8ebaf8daad, tools/ shows P1's own 15 files)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -1
```

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#658`
(`Refs #658`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-device-generic-x64-and-kernel/00-running-log.md` | the flight recorder: model and effort, `reviewed-at` with `8ebaf8daad` and `651150fc88`, the host file's last line and census at stage A, every § 5 run with exit and wall time, every `tools/council/run` call with its `COUNCIL_ENV_FILE` | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 58 re-derived with § 2's block (the counts, the erratum for 989), the configuration's candidates and counts, the history with the three identities, the upstream delta | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #658's checklist; **a coverage table with one row per path under `## Coverage`** (58); § The configuration (the three parts); § The boot files (each script: who runs it, which branch does work, the upstream delta); § The launcher (`vm/generic-x64-vm` against T12's tools); § The runs; § Proofs with `proved:` cells; § Positives (one row per check the slice runs: the input that would FAIL it, or `none` with why) | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the recipe x the configuration x `oldconfig`; `scripts/image` x `bootloader/install` x `options`; the device directory x `tools/` | B |
| Analysis | `.../04-analysis.md` | Phase 4 § Finding Verification; **§ Renovation face Q1 to Q7** (Q1 the configuration's three parts and the launcher design; Q6 the dispositions per unit); § Second opinion (the seat's items graded); § Instruction File Recommendations | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (depth `independent`, one reviewer `gpt` / `openai/gpt-6-astra` / `max`), `packet-manifest.json` with sha256s and the scan's result, the probe's and the refutation's outputs with their `.provenance.json` | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where, acceptance, `Already written:`, the VM line; the YAML `punch_index`; the Phase 7 gate | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #658 | `Audit: M6 T11 the GENERIC_X64 device, the kernel recipe and the boot files -- N findings (...)` | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect proven (a trace, `Already written:`, the VM line, `box-check` 0 fail) | D |
| Retro | `docs/retros/<date>-m6-device-generic-x64-and-kernel.md`, posted on #658 | the mini-retro; what the slice did to the two time-to-play numbers (nothing); what T27, T28 and T25 inherit (the configuration shape; the bootloader table; the launcher design) | G |

## 7. Acceptance

The checklist on #658 becomes this section at dispatch, written there by
the coordinator in place of P1's five generated ones. Every checkbox names
the artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-device-generic-x64-and-kernel/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-device-generic-x64-and-kernel/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); the probe's and the refutation's outputs have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named; `packet-manifest.json` lists every packet file with its sha256 and the scan's result (0 hits, or each hit redacted and filed).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #346, T22's #669, T27's #674), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 58 (`git diff --stat 8ebaf8daad <reviewed-at> -- $(cat .qa-scratch/t11/paths.txt)` empty) and nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty; the dispatch tip is the one the dispatch comment names).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (58 paths, 10,418 lines; read 14 / 1,820 / fork-own 1,421; tier 11 / 46 / 1; reach 49 / 9; GENERIC_X64 fork-own 1,217, the order's 989 named as an erratum), the configuration's two candidates with their removed/added counts, the history (110; 40 fork with the three identities; 70 upstream) and the upstream delta (7 M, 11 D fork-only), or each delta with its command.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `58`.
- [ ] `02-forward-audit.md` § The configuration states the three parts: the nearest candidate (`projects/Generic/linux/linux.x86_64.conf`) with its counts and the AMD64 conf named as not a base; the fork's own edits since `73b20caf86` quoted with their hashes; the built-versus-committed gap stated from the recipe's `listnewconfig`/`oldconfig` lines (quoted) without a build, with the regeneration named as a packet (an open item, not a bug, unless a behaviour claim reads the file).
- [ ] `02-forward-audit.md` § The boot files has one row per script (`install`, `mkimage`, `release`, `rkhelper`): who runs it (`scripts/image:280` for `install`, `:285` for `release`, `scripts/mkimage:225-263` for `mkimage`, or nobody -- `rkhelper` is read by seven Rockchip u-boot recipes and no shipped device -- with the `grep` quoted), which branch does work for which shipped device (`BOOTLOADER=` per device quoted), its upstream status at `651150fc88` (fork-only, modified, unchanged) and its disposition; `install`'s header finding (a fork-authored file under an upstream copyright line) with its line.
- [ ] `02-forward-audit.md` § The launcher states, with lines, how the `tools/vm-*` callers reach `vm/generic-x64-vm` by its basename (the resolution, from the rule file and the callers' lines), which of its flags they depend on, and a design sentence (deferred to the coordinator) for what the device directory should carry and what `tools/` should.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows no guest, no build, no compiler, no plan generation, no fetch (`git fetch` appears only in negations), no handheld, no `tools/council/run invoke` but the one Phase 4.6 call, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, and no write under `/workspace/repos/rocknix*`, another lane's worktree or `/tmp`.
- [ ] `04-analysis.md` § Q1 carries the configuration's three parts and the launcher design; § Q2 the three header/mark findings with their lines and the generic recipe's `git log` answer; § Q3 the bug decision for the `oldconfig` gap and for `install`'s echo branches with the `BOOTLOADER=` evidence; § Q6 a disposition per unit, removals none; § Second opinion grades every seat item (confirmed, narrowed, refuted, new), the decisive ones re-read at their lines.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`.
- [ ] The retro exists at `docs/retros/<date>-m6-device-generic-x64-and-kernel.md`, is posted on #658, says what the slice did to the two time-to-play numbers (nothing) and what T27, T28 and T25 inherit (the configuration shape; the boot-file table; the launcher design).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #658; a blocker named on #658 with what is needed; a branch that differs
from `8ebaf8daad` on one of the 58 at stage A; a failed seat (a hold, with
the provenance quoted); or an execution limit, stated as such with the
running log current. A checkpoint is not a stop; a differing count is a
delta; `next` moving is drift. An idle session says it is idle on #658,
**does not end a turn on a post that asks nothing**, and **updates its
session pointer at every checkpoint** (#1014).

**What never runs in this slice:** a guest outside a window the
coordinator granted on #658 (none is planned); a build, a compiler, a plan
generation, a fetch of any kind; anything against a handheld; a
`tools/council/run invoke` other than the one Phase 4.6 seat, or any other
`tools/council/run` call without `COUNCIL_ENV_FILE=/nonexistent` (`--help`
included); an edit to any of the 58 or to anything under `packages/`,
`projects/` or `tools/` at stages A to D; a push to any branch but the
lane's own; `fork-worktree sync|remove|repair`; an edit to a rule,
`CLAUDE.md`, `AGENTS.md`, a decided register row or
`.github/sessions/saved-session-state-next.md`; a write under
`/workspace/repos/rocknix*` or `/tmp` (use `/workspace/tmp/m6-t11/`); a
credential-shaped literal written anywhere; `--no-verify`; bare `git
stash`; `git worktree remove --force` or `rm -rf` on a worktree or a bare
variable path.

## 9. Ceremonies owed

- A work-log entry per session headed `#658`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #658` or the
  guard.
- The VM question written before any proof (§ 5: the host; no guest; no
  device).
- The mini-retro at stage G, posted on #658, Instruction-Recommendations
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
- Commit messages `docs: ...` throughout (a read slice; a stage-E stream,
  if any, comes with its own brief), each with `Refs #658` and the
  attribution line; `git add -A` only after `git status --short` shows
  nothing a run left behind (`.qa-scratch/` and `tools/council/node_modules/`
  are gitignored).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#658's checkboxes against their artifacts; the lint's `PASS` line; the
seat's `review-plan.json`, provenance and the packet's recorded scan; the
audit issue's checkboxes all at an outcome (the ticked and open counts read
by name); the coverage table's row count (58); **re-running on a clone of
the lane's branch under `/workspace/tmp/m6-coordinator/`: § 2's block, the
configuration's two diffs, the history count with the three identities, the
upstream delta, the boot-file greps, the empty diffs under `packages/`,
`projects/` and `tools/`;** `register-check` and `rules-check` on a
simulated merge with the coordinator's tip (the ledgers united; the archive
carrying `projects/`); the retro's answers. The lane posts one hand-back
comment naming the tip and each artifact by path, writes `reviewed-at:` and
`fixed-at:` into #658's body, then says it is idle. After acceptance the
coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the full lint, carries the configuration shape
into T27's brief and the boot-file table into T28's and T25's, merges the
branch in its turn after the M7 candidate (after T8's and T23's, before
T9's), and closes #658 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#1082) carries this slice's kickoff, and a stranger's proof of this brief
is run by a reader with no context before dispatch; version 2 records what
each found.

## Errata, 2026-10-25 (the coordinator's, at acceptance)

- **"The `tools/vm-*` call the launcher by basename" (§ 1, § 4 Q1(b), § 5,
  criterion 10) was the stranger's proof's grep over comments and help
  strings.** The one tool that runs `vm/generic-x64-vm` is `tools/vm-pair`,
  by full path through `VM_TOOL` (`:36`, `:74`), as the rule's `VM_TOOL=`
  lines do; nothing resolves the basename. The lane recorded the resolution
  as found (06:47 ruling); § The launcher reads that way.
- **The `options` comment the stream brief suggested ("a BIOS guest; the
  image step's `install` copies it") was wrong**: `vm/profile.json` boots
  UEFI, `scripts/mkimage` writes both the BIOS and UEFI loaders (`:89`,
  `:179-180`), and `install`'s copy is not what boots (F-05). The lane
  wrote the true sentence at `22c227d41c`.
- The seat writes `declared_model`, `attempts` and `final` into its
  provenance, no `.run.log` and no flat `served_model` key; the acceptance
  scripts read `final.verification` and the last attempt (`$S/prov-read.py`).
- **A merge of `next` must keep GENERIC_X64 in the override's version case**
  (F-09): upstream's case has none and no default, and the override sources
  no generic recipe, so a merge that takes upstream's case leaves
  GENERIC_X64 with no `PKG_VERSION` -- a broken build, not another version.
  Carried into the coordinator's merge notes and T25's and T28's briefs.
- Accepted at `47672fe4a0` (the lane's `871c5a6bc0` with the coordinator's
  `cc8b6cf2a3`); the re-run's reports are
  `/workspace/tmp/m6-coordinator/accept-t11.out` (stages A to D at
  `499628a049`) and `accept-t11-final.out` (the merged tip and
  `stage-e/run-all.sh`: 47 rows, 0 unexpected).

# Punch List — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

**Independent depth:** one seat, GPT-6 Astra at `max`, its 36 items graded in `04` § Second opinion. Every `where` is at `8ebaf8daad` (unchanged at the dispatch tip `ed7fd0ea50`). The lane changes none of the 28 and nothing under `packages/`, `projects/` or `tools/` (D-WORKFLOW-209). No defect behaves wrongly on a unit's normal path. The coordinator's dispositions (08:39 UTC, #674) made PL-12 a `bug`, filed by the lane as #1095, with its fix in stage-E stream S1.

The VM line, common to every item: **Can this be done on the VM? Yes, on the host:** reads at `8ebaf8daad`, local diffs, and two read-only reads of the M7 lane's H700 build root (`02` § Stage C re-reads). No guest, no build, no network, **nothing on a handheld**. A device fact is a `device-facts.md` row (L15, L16, L29) or an open item to test.

## PL-01: Every pin in the slice is current with upstream's version pins; the authors' releases are CANNOT (no network)

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q4
- **Source:** F-01
- **Owner area:** the H700 recipes; atf; the kernel
- **What:** Recorded; `tools/fork-package-freshness` is the RC's check (D-WORKFLOW-024).
- **Evidence:** `02` § The pins
- **Already written:** nothing: a record
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## PL-02: atf's H700 checksum and URL: a merge of `next` must take upstream's URL with both of upstream's checksums

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source:** F-02
- **Owner area:** `projects/ROCKNIX/packages/tools/atf/package.mk:16-28`; the merge of `next` (T25, #672)
- **What:** For the merge (T25): T5's E6 checksum is from the old URL (`430abc8f66`, D-WORKFLOW-194); upstream's `6103571f67` re-checksums both branches with the `TrustedFirmware-A` URL.
- **Evidence:** `02` § The pins; P5
- **Already written:** nothing on a device: a build-input hazard
- **Acceptance:** after the merge, `git show HEAD:projects/ROCKNIX/packages/tools/atf/package.mk` pairs the `TrustedFirmware-A` URL with `d95aaf29...` (H700) and `6b1d5e89...` (fallback)

## PL-03: The rule's device table mixes the two builds' flag dialects for H700 (*crypto-neon-fp-armv8* is the arm FPU; aarch64 is `+crc+fp+simd`); the hardware's crypto extension is unrecorded

- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source:** F-03
- **Owner area:** `.claude/rules/device-builds.md:22-23` (the coordinator's); `options:9-17`
- **What:** A rule-edit lead for the coordinator; the hardware capability an open item to test (a device-facts row of `HWCAP`).
- **Evidence:** `04` § Q2; G-13, G-14
- **Already written:** nothing: documentation
- **Acceptance:** the table's notes separate the aarch64 flags, the arm flags and the observed capability

## PL-04: `/dtb.img` is named by a fresh card's `extlinux.conf` and written only by `update.sh`; a fresh card needs the runbook's hand step

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source:** F-04
- **Owner area:** `bootloader/mkimage:45-50`, `:88`; `update.sh:26-32`; #44
- **What:** A design question for the coordinator, with #44 (D-WORKFLOW-033) cited, not reopened.
- **Evidence:** `02` § The loader and the tree; P6, P15
- **Already written:** the two units' cards carry `dtb.img` (L15, L16); nothing inherited
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## PL-05: `kernel-firmware.dat` and the kernel's embedded firmware name the same 13 files, and the embed reads `kernel-firmware`'s build directory: coupled, not merely duplicated

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source:** F-05
- **Owner area:** `config/kernel-firmware.dat`; `linux/package.mk:223-244`
- **What:** Recorded; the build-directory dependency is the build-engine lane's (T5's F-17 family, #836).
- **Evidence:** `02` F-05; G-34, G-35
- **Already written:** nothing on a device
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## PL-06: The `.disabled` sunxi_v2 patch: 4,036 lines no build applies

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source:** F-06
- **Owner area:** `patches/linux/0203-...patch.disabled`
- **What:** Disposition: disabled at birth, upstream's; its removal is #346's class decision.
- **Evidence:** `02` § The device trees; P10
- **Already written:** nothing: never applied
- **Acceptance:** the class decision recorded on #346

## PL-07: The 13 trees of unshipped H700 boards

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source:** F-07
- **Owner area:** `linux/dts/allwinner/` (13)
- **What:** Disposition: carried by placement (D-WORKFLOW-185); removals none.
- **Evidence:** `02` § The device trees
- **Already written:** nothing
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## PL-08: `80-clock.rules`, deleted upstream

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source:** F-08
- **Owner area:** `filesystem/usr/lib/udev/rules.d/80-clock.rules`
- **What:** Disposition: settled by the next base merge (`899193e5af`).
- **Evidence:** r15
- **Already written:** nothing persistent
- **Acceptance:** after the merge, the file is absent from `next`

## PL-09: `options` does not say why zram and swap are 0, and nothing joins unit, memory, loader and tree in one place

- **Severity:** Low
- **Category:** Documentation
- **Question:** Q7
- **Source:** F-09
- **Owner area:** `options:77-84`; the device directory
- **What:** A clarity note for the coordinator.
- **Evidence:** `04` § Q7; G-23
- **Already written:** nothing: documentation
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## PL-10: The DDR3 and DDR4 u-boot recipes differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG`

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q1
- **Source:** F-10
- **Owner area:** `packages/u-boot-DDR3`, `u-boot-DDR4`
- **What:** A design sentence (one parameterised recipe), deferred; the stub's textual defconfig lookup is a cost (G-30).
- **Evidence:** `04` § Q1
- **Already written:** nothing
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## PL-11: Two errata: the brief's `mkimage:18-26` (`:22-26` is the Qualcomm branch) and its bare `--since` date

- **Severity:** Info
- **Category:** Documentation
- **Question:** Q7
- **Source:** F-11
- **Owner area:** the brief (the coordinator's); T11's `02`
- **What:** Recorded; the cutoff ruling is the coordinator's (08:13).
- **Evidence:** `02` § The runs, § The loader and the tree
- **Already written:** nothing: a brief
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## PL-12: `update.sh` masks its failures and overwrites `dtb.img` in place; `init` reports success regardless

- **Severity:** Low
- **Category:** Bug
- **Question:** Q3
- **Source:** F-12
- **Owner area:** `bootloader/update.sh:19-63`; `init:427-440` (upstream-carried)
- **What:** A contained fix (checked steps, a copy to `dtb.img.new` and a rename, a non-zero exit) is ours by `bugs-are-agent-first.md` rule 6, verifiable on the host with a fixture `/flash`; bug or record is the coordinator's call.
- **Evidence:** `02` F-12; G-26, G-27, G-9
- **Already written:** a card whose update failed keeps what the failed copy left; a re-run update re-writes the tree and the loader
- **Acceptance:** under a fixture whose `cp` to `/flash` fails, `update.sh` exits non-zero and leaves `dtb.img` as it was (exit 0 and a truncated `dtb.img` today)
- **Bug issue:** #1095

## PL-13: Every H700 image's command line carries `systemd.debug_shell=ttyS0`, a root shell on the serial port

- **Severity:** Low
- **Category:** Policy
- **Question:** Q2
- **Source:** F-13
- **Owner area:** `options:31` (and six other devices)
- **What:** A shipping-policy question for the coordinator (#346's class); the UART's reachability a device fact.
- **Evidence:** `02` F-13; G-36
- **Already written:** nothing persistent: a boot argument
- **Acceptance:** the coordinator's decision recorded

## PL-14: `rg40xx-v.dts` declares `compatible = "anbernic,rg40xx-V"` (uppercase)

- **Severity:** Info
- **Category:** Standards
- **Question:** Q2
- **Source:** F-14
- **Owner area:** `linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-v.dts:10`
- **What:** A lead, recorded; not a unit of ours.
- **Evidence:** G-33
- **Already written:** nothing
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Info
  category: Renovation
  question: Q4
  source_finding: "F-01"
  owner_area: "the H700 recipes; atf; the kernel"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-02
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "F-02"
  owner_area: "`projects/ROCKNIX/packages/tools/atf/package.mk:16-28`; the merge of `next` (T25, #672)"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-03
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-03"
  owner_area: "`.claude/rules/device-builds.md:22-23` (the coordinator's); `options:9-17`"
  tracked: "#1094"
  outcome: "deferred"
- id: PL-04
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-04"
  owner_area: "`bootloader/mkimage:45-50`, `:88`; `update.sh:26-32`; #44"
  tracked: "#44"
  outcome: "deferred"
- id: PL-05
  severity: Low
  category: Renovation
  question: Q5
  source_finding: "F-05"
  owner_area: "`config/kernel-firmware.dat`; `linux/package.mk:223-244`"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-06
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-06"
  owner_area: "`patches/linux/0203-...patch.disabled`"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-07
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-07"
  owner_area: "`linux/dts/allwinner/` (13)"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-08
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-08"
  owner_area: "`filesystem/usr/lib/udev/rules.d/80-clock.rules`"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-09
  severity: Low
  category: Documentation
  question: Q7
  source_finding: "F-09"
  owner_area: "`options:77-84`; the device directory"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-10
  severity: Info
  category: Renovation
  question: Q1
  source_finding: "F-10"
  owner_area: "`packages/u-boot-DDR3`, `u-boot-DDR4`"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-11
  severity: Info
  category: Documentation
  question: Q7
  source_finding: "F-11"
  owner_area: "the brief (the coordinator's); T11's `02`"
  tracked: "`6d0e0892e4`"
  outcome: "resolved"
- id: PL-12
  severity: Low
  category: Bug
  question: Q3
  source_finding: "F-12"
  owner_area: "`bootloader/update.sh:19-63`; `init:427-440` (upstream-carried)"
  tracked: "#1095"
  outcome: "deferred"
- id: PL-13
  severity: Low
  category: Policy
  question: Q2
  source_finding: "F-13"
  owner_area: "`options:31` (and six other devices)"
  tracked: "#346"
  outcome: "deferred"
- id: PL-14
  severity: Info
  category: Standards
  question: Q2
  source_finding: "F-14"
  owner_area: "`linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-v.dts:10`"
  tracked: "#672"
  outcome: "deferred"
```

## Phase 7 resolution gate

The coordinator's dispositions, 08:39 UTC on #674.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Resolved** | recorded at `6d0e0892e4` (`02` § The pins): the pins current with upstream's version pins; the authors' releases `CANNOT (no network)`; `tools/fork-package-freshness` named as the RC's check |
| PL-02 | **Resolved** | recorded at `6d0e0892e4` (`02` § The pins); the coordinator carries it into the merge notes and T25's brief; pointing comment on #672 |
| PL-03 | **Deferred** | #1094, a Backlog the coordinator filed: the table's notes separate the aarch64 flags, the arm FPU and the observed capability; the crypto extension an open item to test |
| PL-04 | **Deferred** | #44 (D-WORKFLOW-033, parked until after the RC), with a pointing comment there naming `02` § The loader and the tree |
| PL-05 | **Resolved** | recorded at `6d0e0892e4` (`02` F-05): coupled, not duplicated; #836 cited for the stamp, not re-filed |
| PL-06 | **Resolved** | recorded at `6d0e0892e4`: disabled at birth, upstream's; its removal is #346's class decision |
| PL-07 | **Resolved** | recorded at `6d0e0892e4`: carried by placement (D-WORKFLOW-185); T25's brief names the 13 |
| PL-08 | **Resolved** | recorded at `6d0e0892e4`: settled by the next base merge (`899193e5af`) |
| PL-09 | **Resolved** | recorded at `6d0e0892e4` as a design: one comment in `options` and one place joining unit, memory, loader and tree, a lead for the coordinator |
| PL-10 | **Resolved** | recorded at `6d0e0892e4` as a design: one parameterised recipe, deferred to the coordinator; no edit |
| PL-11 | **Resolved** | recorded at `6d0e0892e4`: both errata the coordinator's, written into the brief at acceptance |
| PL-12 | **Deferred** | bug #1095, filed by the lane (box-check 0 fail); fixed in stage-E stream S1 (`t27-streams.md` at `64e56a3136`); `init`'s line pointed to T22's #669 |
| PL-13 | **Deferred** | #346, the maintainer's: the coordinator put it there beside T22's root-shell findings; the lane writes nothing on #346 |
| PL-14 | **Deferred** | #672, a lead for T25, in the pointing comment with PL-02's |

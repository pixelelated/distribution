# Punch list — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

**Independent depth** (one seat, GPT-6 Astra at `max`; `04` § Second opinion). The audit issue is #1108 (a sub-issue of #675).
- **Nine items:** 1 Medium, 2 Low, 6 Info. **No `bug` filed:** PL-01 and PL-09 are candidates whose disposition is the coordinator's at the stage-D pause.
- **Nothing** in this list changes a file under `packages/`, `projects/` or `tools/` at stages A to D, and no item proposes a removal of an upstream-carried unit (D-WORKFLOW-209).
- **Nothing ran on the Nova.**

---

## PL-01: `update.sh` ignores `updateabl`'s failure and reports the update done; upstream's replacement keeps that shape over the BLS files (a candidate bug)

- **Severity:** Medium
- **Category:** Correctness (candidate)
- **Question:** Q3
- **Source Finding:** F-04
- **Owner area:** projects/ROCKNIX/devices/SM8550/bootloader/update.sh (upstream-carried); `init:427-440` (T22's lane, #669)
- **What:**
  - **The defect.** `updateabl` exits 1 on a missing ELF, missing partitions or a failed sector-size read (`updateabl:24-40`).
    - `update.sh:25` ignores the exit, and `:27-37` carry on and write `UPDATE` to `/storage/.boot.hint`.
    - `init:427-440` ignores `update.sh`'s exit and prints *"Boot Files Updated."*.
    - `:17`'s remount and `:22`'s copy are unchecked too.
  - **What it is not.** It is not a wrong payload: `init:341-368` refuses an incompatible update, and every cached ELF is sector-aligned. The two `rm -rf` remove directories the `qcom-abl` boot does not read.
  - **At the merge.** Upstream's `update.sh` at `651150fc88` keeps the same shape over `dtbs/` and `loader/`, which the BLS boot reads, and over the hand-off that installs `openabl`. A silent `updateabl` failure there could leave the old ABL with no Android boot image.
  - **Precedent.** T27's #1095 (H700's `update.sh`) was this shape and was fixed by a stream.
- **Evidence:** P7, P12, P15, P16
- **Can this be done on the VM?** Yes, on the host: a fixture run of `update.sh` with a failing `updateabl` stub, as T27's S1 did in `bwrap`; nothing on the Nova
- **Already written:** a device whose `updateabl` failed during an update keeps the previous ABL in both slots and `UPDATE` in `.boot.hint`; nothing records the failure, so a fix cannot tell those devices apart, and the next update's checksum compare re-checks both slots anyway
- **Acceptance:** the coordinator's disposition: a `bug` with a stream (the fixture shows the unfixed `update.sh` exit 0 after a failing `updateabl` and the fixed one non-zero), or a named requirement on #1099's merge
- **Bug issue:** #1109
- **Disposition note:** deferred:#1109, the `bug` the lane filed with its trace, `Already written:` line and host fixture ([issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC); its fix is stage E's stream S1 (`docs/reviews/briefs/t28-streams.md` at `ad168e6d55`). #1099 carries the requirement into the merge ([issuecomment-6396876866](https://github.com/pixelelated/distribution/issues/1099#issuecomment-6396876866)).

## PL-02: the Nova's boot path is superseded upstream; the merge's migration questions

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-01
- **Owner area:** upstream's, via the next base merge
- **What:**
  - **The superseded path.** The `qcom-abl` boot path (`rocknix-abl`, `mkbootimg`, the kernel's branch, `update.sh`, `options`, `mkimage_options`) is replaced by `0340192729` to `73ffb8ee37`, with `cafbb1657d` the core.
  - **Named for #1099**, beyond the brief's two (both slots' `Already written:`; `pixelelated.conf`, `boot=LABEL=ROCKNIX disk=LABEL=STORAGE`):
    - the first boot with `rocknix_abl` left beside `openabl`;
    - failure handling (PL-01);
    - recovery after both slots change;
    - DTB selection with no `devicetree` in the entry;
    - the ` gpt` argument.
  - **Survives the merge:** the fourteen-tree list and the `qcom-abl` meta recipe.
- **Evidence:** P2, P5, P6, P12, P15
- **Can this be done on the VM?** No: the merge's first boot on the Nova is a device fact; the source comparison runs on the host
- **Already written:** nothing proposed here; #1099 owns the slots' line
- **Acceptance:** #1099 carries a comment linking `02` F-01 with the four added questions
- **Disposition note:** deferred:#1099, the lane's comment linking `02` F-01, the four migration questions and the ` gpt` argument ([issuecomment-6396876866](https://github.com/pixelelated/distribution/issues/1099#issuecomment-6396876866); disposition [issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC). No decision taken here.

## PL-03: the pins: four identical, two differ, two absent or deleted; the `kernel-firmware` override lags its generic recipe

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-02
- **Owner area:** upstream's recipes outside the slice
- **What:**
  - **The pins:**
    - `qcom-abl`, the kernel `7.2`, `kernel-firmware` `20260309` and `gamepadcalibration` are identical pins;
    - `extra-firmware` and `inputplumber` differ (InputPlumber moves from prebuilt to source-built);
    - `rocknix-abl` is absent, replaced by `openabl` 1.2;
    - `mkbootimg` is deleted.
  - **The override's lag:** the ROCKNIX `kernel-firmware` override is `20260309` against the generic `20260622`.
  - The authors' releases are `CANNOT (no network)`; `tools/fork-package-freshness` is the RC's check.
- **Evidence:** P5, P15
- **Can this be done on the VM?** No: a recipe read; the host shows it
- **Already written:** nothing proposed
- **Acceptance:** recorded in `02` § The pins; the merge carries the four upstream moves
- **Disposition note:** resolved as a record at `b13d5d8074`: `02` § The pins; the `kernel-firmware` override's lag cited, outside the slice ([issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC).

## PL-04: none of SM8550's six firmware entries is embedded, unlike SM8250, SM8650 and SM8750; its runtime effect observed only narrowly

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q3
- **Source Finding:** F-03
- **Owner area:** the kernel recipe (T11's) and `kernel-firmware` (T23's), outside the slice
- **What:**
  - **The divergence.** `config/kernel-firmware.dat` is installed as files (`kernel-firmware/package.mk:39-70`). The kernel embeds only `regulatory.db` and its `.p7s` on SM8550 (`linux/package.mk:93-97`, `:293-302`); its device embed blocks name SM8250, H700, SM8650 and SM8750 (`:83`, `:208-277`).
  - **Observed only narrowly:** L17, and L18, which disclaims a rendering proof.
  - **#836** is the `.dat`'s stamp issue, cited.
- **Evidence:** P8, P15, P16
- **Can this be done on the VM?** No: the firmware request timing on the Nova is a device fact; the packaging is read on the host
- **Already written:** nothing proposed
- **Acceptance:** recorded as a design question for the coordinator: should SM8550 embed its GPU firmware as its siblings do
- **Disposition note:** resolved as a record and a design question for the coordinator, written as one sentence in `04` § Q3 with #836 cited; the runtime *observed only narrowly* (lines 17, 18); no change, nothing asked of the Nova ([issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC).

## PL-05: a reader cannot tell from the directory how the Nova boots; seven trees share its Qualcomm identifiers; no runbook section (#1100)

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-05
- **Owner area:** the boot path's documentation
- **What:**
  - **The tree.** The Nova's dtb is one of fourteen appended. Seven share its `qcom,board-id = <0x1001f 0>` and `qcom,msm-id = <0x25b 0x20000>`, and no tree has a `rocknix-dt-id`.
  - **Selected in practice:** the ABL picks the Nova's tree (D-WORKFLOW-114's 1280x960 panel), by a rule written nowhere.
  - **The ELF** reaches both slots through three recipes and T1's `updateabl`.
  - **The only procedure** is `rocknix-abl/sources/README:1-6`.
  - Upstream's BLS entry names no `devicetree`.
- **Evidence:** P6, P9, P15, P16
- **Can this be done on the VM?** No: the ABL's selection rule is on the unit; the identifiers are read on the host
- **Already written:** nothing
- **Acceptance:** #1100 carries a comment linking `02` F-05 (the identifier table and the selection question)
- **Disposition note:** deferred:#1100, the lane's comment carrying the seven-tree fact ([issuecomment-6396877061](https://github.com/pixelelated/distribution/issues/1100#issuecomment-6396877061); disposition [issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC).

## PL-06: the `.disabled` patch: 20,593 lines, 89 % of the bytes, never applied

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-06
- **Owner area:** upstream's
- **What:**
  - `0053-add-hynitron-touchscreen.patch.disabled`, born disabled (`aa458af6f9`), never matched by `scripts/unpack:150-159`, still upstream. Its removal is #346's class decision (D-WORKFLOW-209).
- **Evidence:** P1, P9
- **Can this be done on the VM?** No: a file the build never reads
- **Already written:** nothing
- **Acceptance:** recorded; carried in #346's class
- **Disposition note:** resolved as a record at `b13d5d8074`, under #346's class ([issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC).

## PL-07: thirteen trees and seven input files carried by placement; the Nova's chain and two input files are the shipped unit

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-07
- **Owner area:** upstream's
- **What:**
  - **Shipped unit,** by the brief's correction: `02-ayn-controller.yaml:44` matches `Retroid Pocket Nova`, and `rpnova.dts` includes `rp6.dts`, which includes `ayn-common.dtsi`.
  - **Carried by placement (D-WORKFLOW-185):** the other thirteen trees and seven files. They are still built into every SM8550 image. `10-ayaneo.hwdb` matches an attached `AYANEO DEVICE*`, not a board.
- **Evidence:** P9, P10, P15
- **Can this be done on the VM?** No: placement is read from the tree
- **Already written:** nothing
- **Acceptance:** recorded in `04` § Q6
- **Disposition note:** resolved as a record at `b13d5d8074`: carried by placement with the brief's correction ([issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC).

## PL-08: two SM8550-naming `bootloader/mkimage` branches never run for SM8550

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-08
- **Owner area:** upstream's, `projects/ROCKNIX/bootloader/mkimage` (outside the slice)
- **What:**
  - `:22-26` (`rocknix-u-boot.img`, no producer) and `:81-83` (`mkimage_dtb`; `dtb` is not in SM8550's `mkimage_options`). Five trees keep an inert `rocknix-u-boot-dt-id`. Upstream drops the first branch and adds `dtb` to the options.
- **Evidence:** P6, P11
- **Can this be done on the VM?** No: dispatch read from the tree
- **Already written:** nothing
- **Acceptance:** recorded; the merge settles the branches
- **Disposition note:** resolved as a record at `b13d5d8074`: the two never-run branches, settled by the next base merge ([issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC).

## PL-09: the Nova's touchscreen selects pinctrl for gpio24/25 while its reset and interrupt are gpio14/15 (found by the seat)

- **Severity:** Low
- **Category:** Correctness (candidate)
- **Question:** Q3
- **Source Finding:** F-09
- **Owner area:** upstream's tree `qcs8550-retroidpocket-rp6.dts`, inherited by `qcs8550-retroidpocket-rpnova.dts`
- **What:**
  - **The mismatch.** `touchscreen@38`'s `interrupts = <15 ...>` and `reset-gpios = <&tlmm 14 ...>` select `ts_p_*`, which `ayn-common.dtsi` defines for `gpio24` and `gpio25`. The `ts_s_*` states for 14 and 15 exist, and Thor uses them.
  - **Effect:** unobserved.
  - **Upstream:** unchanged at `651150fc88`. A contribution candidate (D-WORKFLOW-164; submissions deferred by D-WORKFLOW-165).
- **Evidence:** P9, P15, P16
- **Can this be done on the VM?** No for the effect (the touchscreen is on the unit); yes for the mismatch, a host read of the trees
- **Already written:** nothing: a tree is rebuilt into every image
- **Acceptance:** the coordinator's disposition: an open item to test, a Backlog, or an upstream contribution queued on #585 with the two-line change named
- **Disposition note:** deferred:#585, one line in the queue's shape, written here and posted by the coordinator at acceptance ([issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC). **Not a bug.** The line:
  > **The Nova's touchscreen selects the wrong pinctrl states** (`projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rp6.dts:365-366`, inherited by `qcs8550-retroidpocket-rpnova.dts`): `touchscreen@38` uses reset gpio14 and interrupt gpio15 (`:359-360`) but selects `ts_p_*`, which `qcs8550-ayn-common.dtsi:1587,1601` defines for gpio24/25. The minimal fix is `ts_s_*` in both lines (`ayn-common.dtsi:1615,1629`), as Thor's secondary touchscreen does (`qcs8550-ayn-thor.dts:390`). Evidence: T28's `stage-c/rereads/c03_g30_touch.out`. Not a bug here (effect unobserved on a tree the VM cannot drive, `bugs-are-agent-first.md` rule 4). **An open item to test:** the Nova's touch input works and does not bounce after resume (line 18 is the frontend only); a wrong mux would show as missing or spurious touches.

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  tracked: "#1109"
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-04"
  outcome: "deferred:#1109"
- id: PL-02
  tracked: "#1099"
  severity: Info
  category: Renovation
  question: Q4
  source_finding: "F-01"
  outcome: "deferred:#1099"
- id: PL-03
  severity: Info
  category: Renovation
  question: Q4
  source_finding: "F-02"
  outcome: "resolved"
- id: PL-04
  severity: Info
  category: Renovation
  question: Q3
  source_finding: "F-03"
  outcome: "resolved"
- id: PL-05
  tracked: "#1100"
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-05"
  outcome: "deferred:#1100"
- id: PL-06
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-06"
  outcome: "resolved"
- id: PL-07
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-07"
  outcome: "resolved"
- id: PL-08
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-08"
  outcome: "resolved"
- id: PL-09
  tracked: "#585"
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-09"
  outcome: "deferred:#585"
```

## Phase 7 resolution gate

The coordinator's stage-D dispositions (#675, [issuecomment-6396865491](https://github.com/pixelelated/distribution/issues/675#issuecomment-6396865491), 11:07:44 UTC), each read back from the tracker at stage F.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Deferred** | deferred:#1109 (the bug; the fix is stage E's S1); #1099 carries the requirement ([issuecomment-6396876866](https://github.com/pixelelated/distribution/issues/1099#issuecomment-6396876866)) |
| PL-02 | **Deferred** | deferred:#1099, the lane's comment ([issuecomment-6396876866](https://github.com/pixelelated/distribution/issues/1099#issuecomment-6396876866)) |
| PL-03 | **Resolved** | recorded at `b13d5d8074`: `02` § The pins, regenerated, `check` 0 |
| PL-04 | **Resolved** | recorded at `b13d5d8074`, with `04` § Q3's design sentence; #836 cited |
| PL-05 | **Deferred** | deferred:#1100, the lane's comment ([issuecomment-6396877061](https://github.com/pixelelated/distribution/issues/1100#issuecomment-6396877061)) |
| PL-06 | **Resolved** | recorded at `b13d5d8074` under #346's class; `git diff --diff-filter=DR --name-only 8ebaf8daad b13d5d8074 -- projects/ROCKNIX/devices/SM8550` empty |
| PL-07 | **Resolved** | recorded at `b13d5d8074`: `tools/t28-tables.py counts` prints the five dispositions, total 29 |
| PL-08 | **Resolved** | recorded at `b13d5d8074`: `stage-b/b09_mkimage_branches.out` |
| PL-09 | **Deferred** | deferred:#585, the line in § PL-09, for the coordinator's post at acceptance; not a bug |

## Verdict

**Status: Ready with named changes.**  
The 43-slice structure, line-count boundaries, and D-WORKFLOW-102 gating are well-conceived, but critical survey misclassifications (core toolchain packages flagged as dead code in T3) and depth under-assignments for declared sensitive security/state paths must be corrected before maintainer sign-off.

---

## 1. The gates and the first three

### Findings

- **Gating compliance:** **Sound (No finding)**.  
  `docs/reviews/order.md` § Fixed constraints and the summary table place T1 (`os-launch-control-state`) at $k=1$ gating release `0.1` (D-WORKFLOW-102), and T2 (`es-launch-path`) at $k=2$ gating before `#336 Step 1` (D-WORKFLOW-102). T3 (`packages-dead-ends`) is placed at $k=3$ as a Local table slice. This satisfies `docs/reviews/plan-for-the-plan.md` § 6a and #346's criterion that the two gated slices and one table comprise the first three sessions.

- **Sizing of the first three:** **Sound (No finding)**.  
  T1 reads 11,560 lines (fork-own 7,441), T2 reads 9,598 lines (fork-own 9,115), and T3 reads 464 lines (95,398 total lines treated as a reachability table). Each fits comfortably within the 8,000–12,000 line guide of `plan-for-the-plan.md` § 5.

- **Carve-out of `backuptool` from T1:** **Minor**.  
  `docs/reviews/areas.json` line 18 explicitly excludes `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` from `os-scripts-and-launch` and reassigns it to `cloud-sync-and-saves`, routing it to T6 (`cloud-setup-content`). In `docs/reviews/inventory.md`, this single path accounts for 1,899 lines of shell code. Including it in T1 would push T1 to 13,459 read lines, exceeding the 12,000-line ceiling. While grouping `backuptool` with cloud content restore in T6 is defensible, `backuptool` is explicitly listed under `state (44 paths)` in `order.md` § The security, state-preservation and launch-path files. T1's description should explicitly note that `backuptool` was carved out to T6 specifically to protect T1's session sizing.

- **SaveState inclusion in T2:** **Minor**.  
  T2 includes `es:es-app/src/SaveState*` alongside `FileData`, `SystemData`, `LaunchCommand`, `ProxyCards`, and `main.cpp`. Because save-state slot selection and state preservation hooks are invoked directly during the launch/exit sequence in `FileData::launchGame`, bundling `SaveState*` into T2 is architecturally sound and respects state preservation constraints.

- **T10 gating contradiction:** **Material**.  
  In `order.md` § How the order was argued, T10 (`emulators-libretro`) is described as: *"RetroArch and the libretro cores, which `runemu.sh` configures and starts and #336's runner replaces; read before that work begins, beside T2's gate."* Yet in the summary table, T10 is placed at $k=10$ and its `Gate` column reads `none`. If #336 Step 1 replaces RetroArch invocation and requires RetroArch recipes and wrappers to be renovated before work begins, placing T10 behind slices T3–T9 (including cloud sync and offline achievements) means either #336 Step 1 is blocked until slice 10, or #336 Step 1 begins after T2 and creates immediate upstream drift against T10 before T10 is even audited (`plan-for-the-plan.md` § 8). T10 must either carry an explicit gate or be positioned adjacent to T2.

---

## 2. The argument from the lenses

### Findings

- **Premature placement of T4 (`patches-dead`):** **Material**.  
  `plan-for-the-plan.md` § 6a ranks the lenses in priority order: Security $\to$ Brittleness $\to$ Nearest new functionality $\to$ Nearest planned change $\to$ Cost against value $\to$ Reachability.  
  In `order.md`, T4 (778 dead patches and configs, 317,908 lines) is placed at $k=4$, ahead of Cloud Sync (T5, T6: 19 blindspots, 47 closed bugs, handling user saves), Offline Achievements (T7: network listener holding credentials), and RetroArch (T10: planned change). The justification given is that dead-end removals *"shrink a later slice or table."*  
  However, the 778 dead patches in T4 patch generic Linux kernels and unreached packages (e.g., `packages/linux/patches/dvb`, `ffmpeg/patches/rpi`, `vitaquake2-lr/patches/x86_64` per `inventory.md` § The unreached set). They patch **nothing** in T5, T6, T7, T8, T9, T10, T11, T12, or T13. Removing them only shrinks T39 and T40 (the patch tables at the very end of the renovation). Placing T4 at $k=4$ elevates Reachability above Security and Brittleness without functional benefit. T4 should be deferred to the table phase (alongside T36–T40).

- **Late placement of T14 (`doctrine`):** **Material**.  
  T14 (`doctrine`) covers `.claude/rules/`, `.claude/skills/`, `CLAUDE.md`, `AGENTS.md`, and the registers (336 paths, 190 code lines, Local depth). `order.md` argues: *"every session obeys it; a rule that lies is the most expensive cruft (plan § 5); #640's hardcoded paths live here."*  
  `plan-for-the-plan.md` § 6b requires every executing session (Stage A, Stage B, Stage G) to read and obey the rules in `.claude/rules/`. If doctrine contains stale rules and hardcoded host paths (#640), executing slices T1 through T13 under un-renovated doctrine risks compounding process errors across 13 sessions. Given that T14 requires reading only 190 lines of code and is Local depth, the "Cost against value" lens demands it run early (immediately after T2 or T3).

- **Late placement of T29 (`tooling-guards`):** **Material**.  
  T29 encompasses `.githooks/**`, `.github/**`, and audit guards like `lint-audit-artifacts`, `rules-check`, `ceremony-check`, and `box-check` (29 paths, 5,356 read lines). Every renovation slice from T1 onward must pass `lint-audit-artifacts` and `ceremony-check` to close (`plan-for-the-plan.md` § 6b). Placing T29 at $k=29$ means the tools enforcing audit validity and secret hygiene are renovated only after 28 slices have already passed through them. T29 should be scheduled earlier, adjacent to doctrine and the build engine.

- **Sequencing of T5–T9 (Cloud Sync and Achievements):** **Sound (No finding)**.  
  Pairing T5/T6 (cloud sync scripts) with T8 (ES cloud UI), and T7 (raofflineproxy) with T9 (ES achievements UI), directly adheres to `plan-for-the-plan.md` § 5 ("paths that share runtime state stay together, because interaction defects live at the seam").

---

## 3. Seams

### Findings

- **T1 seam omission with T11 (`os-system-services`) and T15 (`os-device-quirks`):** **Material**.  
  In `order.md` § T1, the `interacting subsystems` field lists `es-launch-path`, RetroArch, standalone emulators, `backuptool`, and `system.cfg`. It completely omits T11 (`projects/ROCKNIX/packages/sysutils/**`, which provides `system-utils`, `powerstate`, `sleep`, and `systemd` units) and T15 (`hardware/quirks/devices/**`). `runemu.sh` and `setsettings.sh` directly invoke system utility scripts and read device-specific quirks to configure displays, CPU governors, and controller mappings at launch time. An executor auditing T1 in isolation without T11 and T15 in scope will lack runtime context for platform hooks.

- **T1 seam omission with `ApiSystem` (T24):** **Material**.  
  `ApiSystem.cpp` (3,519 fork-own lines in T24) is the primary C++ bridge through which EmulationStation executes OS scripts (invoking `setsettings.sh`, volume controls, brightness, network hooks, and shutdown commands). While T24 lists `os-launch-control-state` as an interacting subsystem, T1 fails to list `ApiSystem.cpp`. Both sides of this bridge must name each other.

- **T2 and T8 omission of ES state-writing primitives (`Settings`, `AtomicFileUtil`):** **Material**.  
  In `order.md` § The security, state-preservation and launch-path files, `es:es-core/src/{Settings,SystemConf}.*` and `es:es-core/src/utils/AtomicFileUtil.*` are declared as sensitive `state (44 paths)`. They reside in T26 and T27.  
  T2 (`es-launch-path`, including `SaveState*`) and T8 (`es-cloud-pages`, including `ThreadedCloudSync` and `CloudTransferJob`) perform critical state-preservation operations that rely directly on `AtomicFileUtil` for atomic file writes and `Settings` for configuration persistence. Neither T2 nor T8 lists `AtomicFileUtil` or `Settings` in `interacting subsystems` (T2 only mentions the raw files `es_settings.cfg` and `system.cfg`). An executor auditing save-state or cloud-sync race conditions in T2/T8 must have `AtomicFileUtil.h` and `Settings.h` declared as read-only context.

- **T5 omission of emulator save directories:** **Minor**.  
  T5 (`cloud-sync-core`) lists ES cards, `backuptool`, and launch hooks, but omits the ROM directory structure and emulator save conventions defined across T10 and T16. Because `cloud_sync` operates on save paths generated by RetroArch and standalone emulators, the save-path layout must be named in T5's interacting subsystems.

---

## 4. Sizing and kinds

### Findings

- **Misclassification of T15 (`os-device-quirks`):** **Material**.  
  T15 is labelled `Kind: read` with 333 paths, 10,175 lines, and 9,327 read lines. However, `order.md` states: *"333 files over 88 handheld models: read the shipped devices' line by line and the rest as a table."*  
  Per `inventory.md`, only 5 SoC families (covering a fraction of the 88 models) are shipped. The fork-own code in T15 is only 389 lines; the remaining 8,938 lines are upstream-carried quirks for unshipped hardware. Labeling T15 as `Kind: read` implies line-by-line reading of all 9,327 lines, contradicting `plan-for-the-plan.md` § 2 & § 3 (provenance decides the lens). T15 should be classified as `Kind: currency` (or split into a shipped read slice and an unshipped table slice).

- **Sizing feasibility of patch provenance tables (T4, T39):** **Material**.  
  T4 (778 paths, 317,908 lines) and T39 (575 paths, 153,425 lines) require producing *"one row per patch with origin, upstream status and reason, the count equal to the slice's paths."*  
  Generating 778 or 575 thoroughly researched patch provenance rows within a single executing session exceeds realistic context and output limits for an LLM agent unless an automated tooling script pre-populates the ledger. T4 and T39 should either be partitioned into smaller batches or their closing evidence must specify that `tools/renovation-inventory` (or a dedicated patch-checker script) mechanically generates the base rows.

- **Doctrine size reporting metric:** **Minor**.  
  T14 (`doctrine`) reports `Read (fork-own): 190 (190)`. This occurs because `tools/renovation-inventory` defines "Read" strictly as programming language lines, categorizing Markdown and text as "Other text" (59,525 lines per `inventory.md`). While 190 lines of code (scripts in `docs/pixelelated`) is technically accurate according to the tool's parser, T14 actually requires auditing 30 rules (8,000 lines) and 44 skills (12,400 lines). The brief for T14 must clarify the true text audit scope so the executor does not treat it as a trivial 190-line pass.

- **T32 exception (`tools/last-good-scripts-test`):** **Sound (No finding)**.  
  T32 is 1 file of 14,238 lines. `plan-for-the-plan.md` § 5 explicitly provides for *"about 8,000 to 12,000 lines of code read line by line, or one package group, or one device... or one unit."* Splitting a comprehensive test suite across sessions breaks shared fixtures and mock context. A single 14,238-line test file is well within the context capacity of modern frontier models. The exception is fully justified.

- **Slices T17, T18, T19 sizing:** **Sound (No finding)**.  
  T17 (H700), T18 (SM8550), and T19 (RK3566/RK3326) have low read counts (327, 118, 617 lines respectively), but contain tens of thousands of lines of device trees and kernel `.conf` files. Keeping each shipped device family as an independent currency slice strictly adheres to `plan-for-the-plan.md` § 5 ("one slice per device we ship").

---

## 5. Review depth

### Findings

- **Under-assignment of review depth for sensitive security and state paths:** **Material**.  
  `plan-for-the-plan.md` § 6c mandates:  
  *"Extended (two reviewers from two other labs): a security, state-preservation or launch-path slice; the cloud sync; the updater."*  
  In `order.md` § The security, state-preservation and launch-path files, 49 paths are explicitly declared as sensitive `security` and 44 paths as sensitive `state`.  
  However, in the summary table, **only T1, T2, T5, T6, T7, and T10 are assigned `Extended` depth**. The remaining sensitive paths are assigned `Independent` depth:
  1. `scripts/get_env` (sensitive security: secret forwarding) $\to$ **T12 (`build-engine`) is Independent**.
  2. `.githooks/**` (sensitive security: secret/wordlist guards) $\to$ **T29 (`tooling-guards`) is Independent**.
  3. `es:es-app/src/guis/GuiWifi.*` (sensitive security: WiFi credentials) $\to$ **T22 (`es-pages`) is Independent**.
  4. `es:es-app/src/RetroAchievements.*` (sensitive security: account credentials) $\to$ **T9 (`es-achievements-pages`) is Independent**.
  5. `es:es-core/src/HttpReq.*` (sensitive security: TLS/network communication) $\to$ **T26 (`es-core-window-input`) is Independent**.
  6. `es:es-app/src/{CloudTransferJob,ThreadedCloudSync}.*` (sensitive state: cloud save-state transfer) $\to$ **T8 (`es-cloud-pages`) is Independent**.
  7. `es:es-core/src/{Settings,SystemConf}.*` (sensitive state: configuration persistence) $\to$ **T26 (`es-core-window-input`) is Independent**.
  8. `es:es-core/src/utils/AtomicFileUtil.*` (sensitive state: atomic disk writes) $\to$ **T27 (`es-core-utils-resources`) is Independent**.

  This creates a severe policy contradiction: `order.md` acknowledges that drift touching any of these paths forces the slice to re-open *"at its depth"* (`plan-for-the-plan.md` § 8), but because the parent slices are marked `Independent`, sensitive security and state code will never receive multi-lab Extended review.  
  At minimum, T8 (`CloudTransferJob`, `ThreadedCloudSync`) and T9 (`RetroAchievements`) must be elevated to **Extended**. For T12, T22, T26, T27, and T29, either the slices must be elevated to Extended, or `plan-for-the-plan.md` § 8 and `order.md` must explicitly stipulate that drift touching a declared sensitive file mandates Extended-depth review regardless of the slice's base depth.

---

## 6. Coverage and reachability

### Findings

- **Critical survey defect: Toolchain and virtual packages mislabelled as `unreached` in T3:** **Material**.  
  `inventory.md` reports 2,670 unreached paths (422,316 lines). In `order.md`, T3 (`packages-dead-ends`) groups all unreached generic packages (1,565 paths, 95,398 lines) into a reachability table for proposed removal (*"every removal shrinks later slices"*).  
  Inspection of `inventory.md` § The unreached set reveals that the following fundamental system and build-engine packages are classified as **unreached**:
  - `packages/devel/glibc` (paths: 5, lines: 245)
  - `packages/virtual/libc` (paths: 1, lines: 18)
  - `packages/virtual/initramfs` (paths: 2, lines: 28)
  - `packages/security/openssl` (paths: 3, lines: 2,972)
  - `packages/devel/make` (paths: 1, lines: 17)
  - `packages/devel/cmake/patches` (paths: 1, lines: 25)
  - `packages/devel/quilt` (paths: 1, lines: 17)
  - `packages/compress/xz` (paths: 1, lines: 25)
  - `packages/devel/swig` (paths: 1, lines: 44)
  - `packages/rust/cargo` (paths: 1, lines: 32)
  - `packages/lang/gcc-aarch64` (paths: 1, lines: 84)
  - `packages/devel/binutils-aarch64` (paths: 1, lines: 51)
  - `packages/sysutils/squashfs-tools` (paths: 1, lines: 31)

  *Inference based on build system architecture:* In LibreELEC/ROCKNIX builds, `virtual/libc` and `glibc` provide the core target C library; `virtual/initramfs` creates the bootable initramfs; `squashfs-tools` creates the system squashfs image; and `make`, `cmake`, `quilt`, `swig`, `cargo`, and cross-binutils provide host toolchain compilation.  
  `tools/renovation-inventory` evidently determined reachability by evaluating target rootfs runtime package dependency lists generated by `scripts/genbuildplan.py`, failing to account for `HOST_TOOLCHAIN`, `PKG_DEPENDS_HOST`, `PKG_DEPENDS_BUILD`, or initramfs dependencies.  
  If an executor in T3 follows the mandate to propose removing unreached packages, **core build-engine toolchain packages will be deleted**, breaking the distribution build. This is a critical defect in the survey ledger. `tools/renovation-inventory` must be patched to trace host/toolchain/virtual dependencies, and `inventory.md`/T3 must be regenerated before dispatch.

- **Records code line count distortion:** **Minor**.  
  `inventory.md` § Read size per area lists `records` as containing 15,392,661 lines of fork-own code. As shown in § Languages per area, test outputs, QA logs, and JSON dumps under `docs/` were classified as shell and python code. `order.md` handles this appropriately by assigning T43 as a Local table slice reviewed only on demand, but the anomaly should be noted in P1 documentation.

---

## 7. Anything else

### Findings

- **Remediation streaming within single-session bounds (D-WORKFLOW-054):** **Minor**.  
  `plan-for-the-plan.md` § 6b mandates that a slice's punch list is resolved in the same cycle (all findings fixed or withdrawn). For a large Extended slice like T1 (11,560 read lines of root shell scripts), auditing, obtaining two external opinions, writing remediation briefs, fixing issues across branches, and proving them on the VM is an exceptionally heavy workload. The brief for T1 must structure remediation streams tightly so the executor does not stall.

- **P1 tool dependencies:** **Minor**.  
  `plan-for-the-plan.md` § 6 requires `tools/renovation-drift`, `tools/renovation-status`, and the renovation face in `tools/lint-audit-artifacts` to be operational before P2 dispatches. Ensuring these tools are verified on `next` is a prerequisite for opening T1.

---

## Recommended changes (priority order)

1. **Fix reachability analysis in `tools/renovation-inventory` and regenerate T3 (Material):**  
   Update `tools/renovation-inventory` to recognize host toolchain dependencies (`PKG_DEPENDS_HOST`, `PKG_DEPENDS_BUILD`), virtual aliases (`virtual/libc`, `virtual/initramfs`), and rootfs image creation tools (`squashfs-tools`). Remove `glibc`, `openssl`, `initramfs`, and build tools from the unreached set before T3 is posted or executed.
2. **Elevate review depths for sensitive state and security slices (Material):**  
   Reassign T8 (`CloudTransferJob`, `ThreadedCloudSync`) and T9 (`RetroAchievements`) to **Extended** depth. For T12, T22, T26, T27, and T29, amend `order.md` to explicitly state that any finding or subsequent drift touching their declared sensitive security/state paths requires Phase 4.6 Extended second opinions (Astra and Argon).
3. **Reconcile T10 gating and position against #336 Step 1 (Material):**  
   Either move T10 adjacent to T2 (before cloud sync) so RetroArch is renovated before #336 Step 1 begins, or explicitly remove the claim that T10 is read "beside T2's gate before work begins" and establish how #336 development will avoid invalidating T10.
4. **Reschedule T14 (`doctrine`) and T29 (`tooling-guards`) earlier (Material):**  
   Move T14 (doctrine, 190 code lines, Local) to position $k=3$ or $k=4$, and advance T29 (guards) ahead of the product code slices. The rules, skills, and linter guards governing all executing sessions should be renovated before they are used to execute slices T5–T28.
5. **Defer T4 (`patches-dead`) to the table phase (Material):**  
   Move T4 from $k=4$ to the end of the order (adjacent to T36–T40). Dead patches that affect no active code should not take precedence over active security and save-state code (T5–T7).
6. **Complete missing interacting subsystem seams in T1, T2, and T8 (Material):**  
   - Add T11 (`os-system-services`), T15 (`os-device-quirks`), and T24 (`ApiSystem.cpp`) to T1's interacting subsystems.
   - Add T26 (`Settings`, `SystemConf`) and T27 (`AtomicFileUtil`) to T2's and T8's interacting subsystems.
7. **Reclassify T15 (`os-device-quirks`) as `currency` (Material):**  
   Change T15's kind from `read` to `currency` (or split into shipped read vs unshipped table) to accurately reflect that only shipped device quirks are read line by line while the 88 upstream quirks are checked as a table.
8. **Clarify patch table generation methodology for T4 and T39 (Minor):**  
   Update the acceptance criteria for T4 and T39 to specify that initial provenance rows are generated via automated tooling rather than manual entry across 778 and 575 paths.
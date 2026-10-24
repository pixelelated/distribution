## 1. My own findings

“Gap” below means a failure of the audit’s evidence or coverage, not a claim that a device failure was reproduced.

- **G-01 — Medium — `04-analysis.md`, Q6 Table 1 (`idtech-lr`, `ecwolf-lr`, `tyrquake-lr`, `vitaquake2-*`), Table 2 (`idtech`), Table 3 (`Scan id Tech Games.sh`):** GENERIC_X64 excludes the id Tech package and its dependent cores but still offers the `idtech` default and scanner; the audit leaves this offered path without an established provider.
- **G-02 — Medium — `retroarch/package.mk:106–112`:** One **stale** ARM install directory passes the `retroarch-*` test just as one current directory does; after a partial pin update, the recipe can copy an old `retroarch32` into a new image without checking its version. F-11 covers missing or multiple matches, not this case.
- **G-03 — Medium — `04-analysis.md`, Q4(a) row 4; `yabadabadoo-lr/package.mk:46`; `runemu.sh:268–279,302`:** The incoming 32-bit Saturn core has an unchecked launcher handoff: the reviewed launcher’s 32-bit selector names only `pcsx_rearmed32`, `gpsp`, and `desmume`; row 4 establishes the new ARM copy but supplies no matching dispatch change.
- **G-04 — Low — `retroarch/scripts/call_achievements_hooks.sh:15,17`, shellcheck SC2048 output:** Unquoted `$*` loses argument boundaries and expands matching filename patterns; a hook call containing an argument with spaces or wildcard characters is not forwarded intact.
- **G-05 — Low — `retroarch/scripts/call_achievements_hooks.sh:13`, shellcheck SC3014 output:** The script declares `/bin/sh` but uses `==` in `[ … ]`; its test depends on a shell extension and fails under a shell that implements only the POSIX form.
- **G-06 — Medium — pinned `gfx/gfx_widgets.c:1196,1219–1220,676,728`; coverage row for patch 0019:** The concurrency argument misses the unlocked `current_msgs_size` test after the layout unlock; the callee’s lock cannot protect that earlier read. The Q3 PASS lacks an atomic-field or single-owner argument for concurrent queue updates.
- **G-07 — Medium — `02-forward-audit.md`, AC-09; `04-analysis.md`, Q4(a) rows 7 and 14:** AC-09 is declared closed although the required save/state change review is assigned to a future stream; row 14 names a range without reporting its review, and row 7 supplies no reviewed ranges or changelog results.
- **G-08 — Low — `02-forward-audit.md`, coverage rows for `pcsx_rearmed-lr/package.mk` and `sources/H700/TATE-MAME 2003-Plus.rmp`:** The coverage map marks the defective PCSX installer’s Q3 cell `n/a` while assigning F-12’s main-configuration-key findings to a remap file; “344 rows, 0 empty cells” does not establish correct finding-to-path coverage.
- **G-09 — Low — `04-analysis.md`, Q6 Table 5, especially `batteryplus/0001-batteryplus-capacity.patch`; `retroarch/package.mk:26`:** The supposed patch-reachability table records touched filenames, not device, build-option, or runtime reachability; it cannot answer whether a conditional patch such as `batteryplus` reaches a shipped build.
- **G-10 — Low — the `grep -rl -E 'FetchContent|ExternalProject_Add|git clone|curl |wget '` command over 111 unpacked trees; `03-retrospective.md`, §3.6.5 “fetch-at-configure” row:** The “every site” conclusion exceeds the scan: top-level CMake/Make files in one x86_64 root do not cover fetches hidden in included scripts or cores absent from that root.
- **G-11 — Low — `04-analysis.md`, Q6 Table 1’s five T24 rows and their `Already written:` conclusion; P1’s `/tmp/cores` mount output:** Current package exclusion does not establish that no saves were written on fork devices; earlier images and user-installed `/storage/cores` copies are not checked before the audit declares “nothing.”

## 2. Refuting the first reader

### High findings

**F-07 — Survives as a Low currency/provenance finding; High is not established.**  
The removal upstream and continued inclusion here are supported by `c4d353449e` and `virtual/emulators/package.mk:49–94`. Those facts do not establish a licence breach by this fork. The coordinator’s removal decision can stand without treating the missing legal assessment as proof of High severity.  
**False if:** the fork had already removed the package or did not include it on the stated devices. The packet shows continued inclusion. Whether redistribution is permitted cannot be decided without the licence terms; Q4(a) row 1 supplies the removal decision, not those terms.

**F-08 / #802 — Survives, High, with the artifact claim limited to H700 and SM8550.**  
The requested absolute path is established by `runemu.sh:268–279,302`; the two image rows show the file absent there and present under `/usr/lib32/libretro`. P1’s mount output confirms the stated overlay arrangement on the guest. RK3326 and RK3566 have the same default in the regenerated tables, but no corresponding image inspection is supplied.  
**False if:** the launcher chose the `/usr/lib32` file, or the overlay supplied the missing file through another lower directory or a shipped upper-layer copy. The cited launcher, mount output, and image rows show none of those. A player’s own upper-layer copy is an acknowledged exception, not a repair to the factory image.

**F-09 — Survives, High as a merge blocker, not a current player failure.**  
The two incoming copies use `${DISTRO}`, while the fork’s roots use `${DISTRONAME}` (`pcsx_rearmed-lr/package.mk:27`, `yabadabadoo-lr/package.mk:46`, `config/options:24`, `distributions/ROCKNIX/options:17`). The merge-tree output establishes that Git does not flag these lines as conflicts.  
**False if:** the names were equal, compatible root aliases existed, or the copies were not executed on the stated ARM-enabled builds. The packet’s variable values and `ls -d …/build.ROCKNIX-*` result reject the first two; the finding is expressly conditional on the enabled copy paths.

**F-19 / #806 — Survives, High; narrow the claim about the exact build timeline.**  
The SM8550 image’s no-PCRE binary/configuration evidence and `Install Steam.sh:217,222,2747–2753` establish failure when installation reaches the Proton parsing step. The missing dependency and configure-time autodetection explain the build-order exposure. Two completion timestamps alone do not establish the exact instant configure ran; the stronger evidence is the `config.log` failure to find `pcre2.h`.  
**False if:** a PCRE-capable grep were selected, the script no longer used `-P`, or this step were unreachable. The supplied PATH read, SM8550 image row, and main-sequence read show the opposite.

### Medium findings

**F-06 — Survives, Medium; the proposed fix is incomplete.**  
The constructed case B succeeds with two defaults, and `SystemData.cpp:2179–2213` selects the first—the core originally marked `false`. The construction directly defeats the promised rule (`functions:212–214`; `virtual/emulators/package.mk:150–151`).  
**False if:** generation validated exactly one default per system or rejected the constructed case. The packet shows successful generation instead. Changing the XPath to `core[last()]` fixes over-marking, but still permits two different cores—or cores under different emulators—to be marked default. A separate per-system count check is required.

**F-11 — Survives, Medium, for builds that require 32-bit support.**  
The `if [ -f …/retroarch-*/usr/bin/retroarch ]` condition allows the function to continue after zero matches or a multiple-argument test error (`retroarch/package.mk:106–112`). Absence is not a defect on a deliberately 64-bit-only build.  
**False if:** the build engine guaranteed a current, unique ARM install before this function, or the function failed closed when the required binary was absent. Neither guarantee is supplied. The four healthy roots prove only their current state. G-02 adds the separate stale-single-match case.

**F-15 — Survives, Medium, but “eleven unpinned dependencies” is inaccurate.**  
There are nine abbreviated commit IDs and two mutable tags, not eleven floating sources. The configure-time fetch design and lack of recipe-controlled overrides remain established by `cmake/FetchDependencies.cmake:44–60`, `melonds-ds-lr/package.mk:14–21`, and the recorded `_deps` contents.  
**False if:** independently pinned sources were supplied before configure and downloads were disabled. The packet shows neither. A fresh, unseeded build needs network access; an already-populated cache is not evidence against that finding. Fix verification should test an offline configure and source identities, not merely demand an empty directory named `_deps`.

**F-20 — Survives, Medium.**  
The extraction excludes double quotes, not single quotes; those values then enter single-quoted shell text passed to `eval` (`Install Steam.sh:217,222,240–243`). Validation at `2584–2588` is too late. The attacker described by the finding is a release-metadata controller, not an arbitrary network observer.  
**False if:** restrictive validation occurred before `eval`, or the replacement assignments had already landed in the reviewed code. The packet shows neither: `6101242e14` is an incoming fix, not the reviewed implementation.

**F-21 — Survives, Medium, narrowly as missing payload verification.**  
The cited runtime and Proton paths lack the payload-digest check shown for the client (`Install Steam.sh:1060–1071,2630–2632`, versus `1749–1751`; checksum-asset exclusion at `222`). That supports an integrity-hardening finding, not a demonstrated transport compromise. A checksum obtained from the same compromised publisher would not independently authenticate that publisher’s payload.  
**False if:** the payload were verified against an expected digest or signature before use. No such check is supplied for these two paths. The redirect-policy and BusyBox claims remain unread leads and do not support this verdict.

**F-24 — The claimed live Medium failure does not survive; retain a Low name-mismatch investigation.**  
`Start RPCS3.sh:27–29` proves different strings: registered target `rpcs3`, executable `rpcs3-sa`. It does not prove the running process’s name or the consumer’s matching rules. The packet explicitly leaves the `input_sense` question unsettled.  
**False if:** the kill consumer uses a matching pattern that catches `rpcs3-sa`, or the process names itself `rpcs3`. The packet neither demonstrates nor rules out those cases. Upstream’s rename is a reasonable incoming correction, but its existence is not proof that the present hotkey fails.

### Low findings that need changing

**F-05 — Split the grade: `st-v` is Medium; GENERIC_X64’s missing explicit PSX default remains Low.**  
The empty `st-v` emulator entries are live configuration failures on four devices, not latent ones. The interface read says an empty emulator gives no launch command. In contrast, PSX deterministically falls back to DuckStation standalone (`virtual/emulators/package.mk:1165–1209,1395–1401`; `SystemData.cpp:2179–2213`; Q6 Table 2, `psx` and `st-v` rows).  
**False if:** `st-v` had another documented launch path without an emulator, or PSX had an explicit default. Neither is shown. The supplied fallback does refute treating PSX’s missing marker alone as a proven launch failure.

**F-22 — Re-grade to Medium.**  
An interrupted optional installer leaves a shared execution mechanism disabled, affecting later box64/FEX launches until repair or reboot (`Install Steam.sh:2692–2710`). That is broader than a failed Steam installation.  
**False if:** another guaranteed cleanup path restored the registrations whenever the function exited early. The packet’s zero-trap result and sole restoration at `2709` show no such path. The suggested shell trap also cannot repair a `SIGKILL`; the stated kill case needs recovery outside the killed shell.

**F-13 — Retain Low, but narrow the wording.**  
The successful status checks execute and print messages; they are not dead. Only the failure arms are bypassed when `errexit` is active at the function call (`retroarch/package.mk:92–98`, `config/path:4`).  
**False if:** the function is invoked in a context that suppresses `errexit`; that would invalidate the claimed failure-path equivalence of deletion. The packet supplies the setting, not the complete invocation context. Redundant success logging survives as a cleanup observation.

### Q4: do all fourteen “to merge” dispositions hold?

**They survive as a conditional integration backlog. They do not constitute a completed compatibility review, and AC-09 does not survive as closed.**

The packet’s own conditions matter:

- **Rows 2 and 5 are coupled changes:** the FFmpeg and InputPlumber halves must travel with their out-of-slice changes. Row 5 also leaves existing `/storage` profiles and launch-time hotkey rewriting to be checked.
- **Rows 3 and 6 follow rows 4 and 8.** Row 12 is the merge of row 13, not another independent implementation to apply.
- **Rows 4 and 10 need the root-name adaptations; row 8 needs the five dependency conflict resolutions.** Row 4 additionally has G-03’s undocumented 32-bit launcher handoff.
- **Row 1 is a recorded removal decision, not a supplied legal analysis. Row 9 is an incoming target correction, not proof of F-24’s runtime claim.**
- **Rows 7 and 14 lack the required completed save/state review.** Row 14 gives `d1a40352e2..5939e0c6d5` but delegates reading it. Row 7 gives no results from such a review. Q4(b) also says only `np2kai-lr` differs from ROCKNIX’s pin; “core updates” must not automatically be read as a pin bump for every recipe named in row 7.

These conclusions rest on `04-analysis.md`, Q4(a) rows 1–14 and Q4(b)’s `Upstream` column.

The RetroArch bump conclusion also survives: this is not a pin-only update. But the blanket statement that the other six fork patches all fail as the build meets them is wrong. **Five fail outright; 0019 applies with fuzz.** Refreshing all six for a fuzz-zero series remains justified (`04-analysis.md`, Q4(c), rows 0013–0019).

### Q6: do the reachability conclusions hold?

**The build-list counts hold; complete launch reachability does not follow from them.**

- Table 1 does show every in-membership core recipe selected by at least one device, and exactly five all-dash recipes outside the membership.
- Table 3 does show every one of the 24 scripts installed somewhere. Table 4 supports five built device sets and ten retained sets.
- Table 2 supports the reported `st-v` and PSX omissions. It also exposes G-01’s GENERIC_X64 `idtech` disagreement.
- Selection is not a launch path: GENERIC_X64 selects `pcsx_rearmed-lr`, while its PSX choices are only `duckstation-sa` and `swanstation` (`Q6 Table 1, pcsx_rearmed-lr`; `virtual/emulators/package.mk:1165–1209`). This does not make the core unusable by hand, but it disproves equating package selection with interface reachability.
- Table 5 is a source-file map, not a reachability proof. The five excluded recipes’ “nothing written” conclusion also exceeds the current-state evidence, as G-11 records.

F-14’s narrower result does hold: the shipped font does not activate the sharp-size step, while the patch’s logging still runs. That is exactly what `p3-guest.out` reports; it is not proof that the whole patch is dead.

## 3. What I could not judge

- **Actual ARM launch and installer outcomes.** The guest has no `retroarch32`; H700 and SM8550 provide host artifacts, not executed ARM failure traces. The static path and grep findings survive, but device execution is not supplied (`p1-installed-set.out`; F-08 image rows; F-19 image rows).
- **RPCS3’s kill semantics.** The missing evidence is the actual `set_kill` consumer/`input_sense` matching code and a running process-name observation, not another filename listing (`Start RPCS3.sh:27–29`).
- **AetherSX2 redistribution rights.** The packet supplies upstream’s removal and the coordinator’s decision, not the licence clauses or their application to this distribution (`04-analysis.md`, Q4(a) row 1).
- **Complete incoming-merge compatibility.** The out-of-slice FFmpeg, InputPlumber, and new-core launcher changes, plus the save/state review results, are absent. Existing-device hotkey migration is expressly left for later (`Q4(a) rows 2,4,5,7,14`).
- **The concurrency and end-to-end patch claims beyond the supplied checks.** The wrapper test drives one poster, so it does not exercise 0011. The packet omits 0019’s field type and writer discipline. P3b proves Auto-slot detection, not successful hotkey loading of the Auto state (`tools/retroarch-wrapper-test` output; `gfx_widgets.c:1196,1219–1220`; `p3b-guest.out`).
- **The full download and extraction safety story.** Redirect restrictions, the runtime checksum source, extraction safety, and repeated FEX-stage behaviour are not established by the supplied reads; several are explicitly labelled leads (`Install Steam.sh:856–875,1080–1101,1833–1872,499–501`).
- **The promised unchanged WildMIDI archive checksum.** Resolving the short commit proves object identity, not equality of two downloaded archives. No short-URL/full-URL archive comparison is supplied (`wildmidi/package.mk:22`; the recorded `gh api …/commits/405ca73` result).
- **Rotation-table correctness, rather than reproducibility.** The five `cmp` successes prove repeatable output. The two failure fixtures prove the minimum-count guard. Neither supplies an independent oracle for game rotations or the four parser regression cases (`02-forward-audit.md`, rotation-generator result table and constructed-failure outputs).
- **Every non-default interface choice against its installed artifact and ABI.** Q6 Table 2 omits those names. For example, GENERIC_X64’s two PSP choices cannot be fully reconciled with its absent `ppsspp-lr` package from the displayed table alone (`Q6 Table 1, ppsspp-lr`; Table 2, psp/pspminis).
- **Hardware performance and byte-identical profile-copy claims.** Q5 explicitly leaves device panels and boot mounts unmeasured. The profile comparison described under F-12 compares key/value dictionaries, which does not establish byte-for-byte equality of files (`04-analysis.md`, Q5 measurement table; the recorded Python dictionary comparison under F-12).
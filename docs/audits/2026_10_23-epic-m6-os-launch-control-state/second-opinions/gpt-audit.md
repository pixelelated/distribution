## 1. My own findings

Paths below are relative to `projects/ROCKNIX/packages/rocknix/`, unless stated otherwise. These are additional to the numbered F-findings; several were noted in the packet without receiving their own finding.

- **G-01 — Medium — `autostart/003-upgrade:8-17`:** When `post-update` returns a failure, the following removal of `/storage/.boot.hint` discards the retry request. An interrupted process leaving the hint behind does not cover a command that finishes unsuccessfully.
- **G-02 — Medium — `sources/post-update:38`:** The `rsync -a --delete` removes owner-created files beside the excluded `configs/` directory during an update. Finding no such files on a fresh guest does not make this safe for an existing installation.
- **G-03 — Low — `profile.d/001-functions:129-134`:** The shown per-game lookup pattern ends at the requested key, without an `=` boundary; a stored key beginning with that key also matches. This is separate from F-21’s filename escaping and value-splitting defects.
- **G-04 — Medium — `sources/scripts/installtointernal:63,89-108`:** A failed `parted` command that emits a nonempty partial listing passes through `mapfile` without its failure status being checked. The empty-result check does not establish that the partition inventory used by the destructive steps was successfully read.
- **G-05 — Medium — `sources/scripts/runemu.sh:378,385`:** PortMaster command construction inserts the ROM name into a `sed` program without escaping it; a filename containing the relevant `sed` metacharacters changes or breaks the transformation. The safe ROM expansion described for `:302,500` does not protect these separate substitutions.
- **G-06 — Low — `sources/scripts/rocknix-config:39`:** The key/value writer inserts data into a `sed` program without escaping it; when a key or value contains editing syntax, the writer changes the edit rather than storing the supplied data literally.
- **G-07 — Low — `sources/scripts/handle-hdmi-hotplug:15-17,28-30`; `autostart/081-usbgadget:1-5`:** The hotplug path tries to stop a `usbgadget` systemd unit, while the recorded installation starts the gadget through its script and has no such unit. On that installation, these stop calls do not reach the gadget’s shutdown code.

## 2. Refuting the first reader

### Every Medium finding

**F-01 — Survives, Medium; narrow the hardware claim.**  
The unsupported-name dispatch fails: the tree’s launch produced `conservative: command not found`, while `powersave` did not. That establishes the defect at `runemu.sh:465-467`, not an actual H700 governor transition or battery effect. The interface enumerates runtime governors, while the supplied H700 evidence is a kernel configuration, not a runtime list (`ApiSystem.cpp:1062-1065`; Group 1 guest output).  
**False if:** every offered name has a working command/function, or the interface filters unsupported names. The packet shows neither; the guest’s `type -t conservative` result shows the opposite for that guest.

**F-03 — Survives, Medium, as an unsynchronised-restore risk—not a measured race.**  
The previous launch leaves restores running after its own control flow proceeds (`runemu.sh:538,546,549,558,560`). That is enough to identify missing coordination with the next launch’s setters, but the promised completion trace is absent.  
**False if:** the caller waits for those jobs, or another lock prevents the next launch from changing the same state until they finish. The packet supplies no such protection. It also supplies no observed instance of a previous restore overtaking a subsequent launch.

**F-09 — Survives, Medium; the proposed fix does not survive.**  
The backgrounded first test does not control the `if`, and the guest emitted hardcore `"1"` despite the caller supplying `"false"` (`setsettings.sh:334-335,557`; Group 1 output).  
**False if:** explicit values are preserved at this call, or overriding the netplay prohibition is intended. The supplied call and output contradict that.  
The proposed “OS value when set, otherwise caller value” rule still returns `"1"` in this exact failing case. Forced values and fallback values need different treatment; preserving the analogue preference at `:989` does not justify defeating the forced netplay value at `:557`.

**F-10 — Survives, Medium; split the two explanations.**  
The joined regex test incorrectly treats `neogeo` as a member of lists containing `neogeocd`; the guest’s SNES control distinguishes that failure (`setsettings.sh:344-356,840-852,955-978`; Group 1 output).  
**False if:** membership compares complete entries. The code and guest result show that it does not.  
However, whole-entry matching does **not** fix the separate `pcsx_rearmed` architecture claim: an exact name still matches that name in `IS_32BIT`. That requires evidence about the installed core’s architecture and an architecture-aware decision (`setsettings.sh:170-172,801`).

**F-11 — Survives, Medium.**  
Checking for the staging file and then creating it with `>` is not safe across the parallel functions. The lifted-function test lost entries in 9 of 200 concurrent runs and none in its serial control (`setsettings.sh:310-325,1427-1478`; Group 1 output).  
**False if:** the header is created before any worker starts, or all modifications are serialised. Neither protection is shown. The test proves the race in the function; it does not establish a 9-in-200 failure rate for complete game launches.

**F-14 — Survives; raise to High.**  
A normal interface text field reaches a root shell evaluation. The tree-script proof created the marker and cut off the intended emulator arguments; the plain-host control did neither (`GuiNetPlaySettings.cpp:33`; `setsettings.sh:620,683,688`; `runemu.sh:355,500`; Group 1 output). This is more than malformed netplay arguments: input data becomes root commands.  
**False if:** the host is strictly validated before this path, or remains a single argument without passing through shell evaluation. The successful marker proof disproves those protections on the tested path. This is not evidence of unauthenticated network exploitation; it is a proven interface-input-to-root-command defect.

**F-16 — Survives, Medium.**  
The redirected `grep` leaves an empty command substitution, selecting the truncating branch. The guest reduced three core-option lines to one (`setsettings.sh:1012-1016`; Group 1 output).  
**False if:** the test uses `grep`’s status and the missing-key branch appends, or another step preserves and restores the other options. The shown code and resulting file show neither. Scope it to `mame2003_plus` launches with tate enabled.

**F-17 — Survives, Medium; narrow “every Game Boy launch.”**  
The defect applies to Gambatte launches when the options directory exists and the unrelated literal file `GAMBATTECONF` does not. It does not cover every Game Boy core. Under the tested conditions, three lines became one (`setsettings.sh:1247-1252`; Group 1 output).  
**False if:** the existence test checks `"${GAMBATTECONF}"`, or another step preserves the previous options. The packet shows the literal-name test and destructive result. A missing options directory causes a write failure instead, as the finding itself notes.

**F-19 — The Medium verdict does not survive; retain Low escaping defects.**  
The overlay test proves that the bezel branch takes precedence. It does not prove that this precedence violates the intended relationship between two overlay-producing features (`setsettings.sh:821-822`; Group 2 output: no overlay lines with the bezel enabled, overlay lines with `nes.bezel=none`).  
**False if:** bezels and overlays are intentionally exclusive and the player must disable the bezel first. The packet supplies no policy either way, so the experiment cannot establish the claimed ignored-choice bug.  
The unescaped shell substitutions and JSON construction remain defects for values containing the relevant characters (`setsettings.sh:1048-1087,1123,1405-1411`). **Those would be false if** input validation excluded those characters or the writers escaped them; neither protection is shown. The Medium default-device claim needs design evidence and a missing/failed-bezel test.

**F-21 — Survives, Medium; reject the universal wording.**  
The bracketed-name lookup failed while the plain-name control succeeded, and `print $NF` loses everything before the final `=` in a value (`001-functions:129-134`; Group 1 output). Not every regex character necessarily prevents a match: some patterns still match the original name or match another game’s name.  
**False if:** the complete game-key prefix is matched literally and the value is taken after its first separator. The shown implementation does neither. The claimed upstream repair is not independently verifiable from the supplied commit descriptions alone.

**F-29 — Survives, Medium.**  
The fault-injection test produced an empty root hash, exit status zero, and an updated `root.password`; the real-applet control produced a `$6$` hash (`setrootpass:32-45`; Group 2 output). A working normal case does not excuse the failure path.  
**False if:** hash failure or failure to replace the intended shadow record stops subsequent changes and returns failure. The guest result disproves that. I do not turn this into a proven passwordless remote-login claim: the packet contains no authentication-policy or login test.

**F-32 — Survives, Medium; narrow what the guest proved.**  
The direct edits bypass the guarded writers, and the append operation turns a cut final value into a newline-terminated one (`post-update:159-160,202`; Group 2 output). The guest did not prove a concurrent lost update or a subsequent bad last-good backup.  
**False if:** the entire operation is guaranteed to have a complete input and no competing writer, or it uses the shared guarded writer. The packet does show an earlier boot-time verification (`autostart/001-setup:28-38`), but not exclusion of writers for the entire update. Earlier verification is not proof of that stronger guarantee.

**F-39 — Survives, Medium, as a missing destructive-operation guard.**  
The script has no shown check that its target is separate from the running system before requesting partition removal and reformatting (`installtointernal:20,89-108`).  
**False if:** an earlier target check rejects every running-system device, or the complete utility sequence is demonstrated to refuse before any destructive change. Neither is supplied. Do not claim that a second invocation has been shown to format mounted filesystems: the packet explicitly leaves the `parted`/`umount` refusals and `set -e` consequences unresolved.

**F-40 — Survives; raise to High.**  
The guest demonstrated the decisive status error: `cp` failed, but BusyBox `find` returned zero. The installer then has a path to its success message despite an incomplete storage migration (`installtointernal:208-215,255`; 07:52 `nobody` fixture output). The inconsistent space calculation adds another route to that failure (`:48,200-205`).  
**False if:** every copy failure reaches the installer’s failure status, and the size calculation covers exactly what is copied. The supplied test and code contradict both protections. The source card is not automatically erased by this defect; the High risk is false assurance that a player-data migration is complete before that source is retired.

**F-44 — Survives, Medium.**  
The update deletes an explicit opt-in value, and the guest demonstrated that deletion (`post-update:199-202`; Group 2 output).  
**False if:** the deletion is a genuinely one-time migration, or it preserves an owner’s opt-in. Neither condition is present. Deleting a value because it equals an old default also cannot distinguish that default from an owner deliberately choosing the same value; the proposed repair must not repeat that mistake.

**F-57 — Survives, Medium on its affected callers; the “always maximum” claim is false.**  
The comparisons are redirections, and the guest demonstrated the upper branch plus creation of `100` (`paneladj:20,37-40`; 08:03 guest output). But if a readable file named `1` exists, the second test also succeeds and selects the minimum. The outcome depends on the working directory. An existing file named `100` is truncated, not merely accompanied by a new stray file.  
**False if:** these are numeric comparisons or the affected path is never called. The packet shows neither. It proves broken clamping, not one universal resulting value.

**F-58 — Survives, Medium, restricted to x86_64.**  
The script stops at the missing sourced file, so its later performance-setting work does not run (`008-perfmode:8,13-37`; `package.mk:119-126`; guest `sh -x` output and boot journal).  
**False if:** that file is installed, or the script chooses an installed architecture-specific file without aborting. The package rule and guest failure disprove both. This establishes skipped script work, not that the kernel necessarily starts with harmful CPU or GPU defaults.

**F-67 — Survives; raise to High.**  
The bootloader updater proceeds from the first slot write to the second without checking success or read-back, then announces success (`updateabl:69-72`). Losing both bootloader copies is a High-impact failure even without a device failure demonstration.  
**False if:** failure of the first write prevents the second, and each successful write is verified before proceeding. The shown sequence has neither protection. The 258,048-byte artifact check clears the separate sector-alignment suspicion; it says nothing about write failures.

**F-68 — Survives, Medium, as secret placement—not proven cloud exfiltration.**  
On a paired device, the script copies Bluetooth state into a backup beneath the games tree, and the service invokes that copy on stop (`rocknix-bluetooth:8-10,73-98`; `network/bluez/system.d/bluetooth.service:10,12`).  
**False if:** link-key files are excluded, or this destination is a deliberately protected credential store excluded from sharing and content backups. The packet establishes neither. It also does not establish that a cloud backup actually includes this archive or that an unauthorised client can fetch it over Samba.

**High promotions:** **F-14, F-40 and F-67**, for the specific effects above. I do not promote the other Mediums on this packet. F-19 drops to Low pending evidence that the bezel/overlay precedence is wrong.

### Lows whose grade or conclusion needs changing

| Finding | My verdict and evidence | What would make it false; does the packet show it? |
|---|---|---|
| **F-06** | **Raise to Medium.** An ordinary space in a ROM path can turn the removal into deletion of a different existing file, not just failure to remove NVRAM (`runemu.sh:309`). | Quoted pathname data, or enforced filename restrictions excluding splitting and glob expansion. Neither is shown. The wrong-file deletion requires the resulting operand to name an existing file. |
| **F-15** | **Raise to Medium.** The TGB Dual branch destroys other core options, the same class of loss graded Medium for F-16/F-17. The malformed client-port call also survives, without assuming it breaks clients using the default port (`setsettings.sh:621,671-675`; host contrast `:595`). | Correct argument positions and a preserving update of the options file. The shown two-argument call and `>` contradict those protections. |
| **F-18** | **Does not survive as an established defect.** A different path is not proof that RetroArch does not read it (`setsettings.sh:1065`, compared with `:1037,1096`). Keep a follow-up, not a confirmed bug. | A configured reader of that exact path would refute it. The packet supplies neither that reader nor evidence excluding it. |
| **F-33** | **Raise to Medium.** A later update destroys the retained copy of an owner’s interface configuration by replacing it with the installed symlink (`post-update:32-36`). This is persistent user-file loss. | Skipping already-installed links, or retaining the original backup under another name. Neither is shown. A fresh guest with no custom copy does not test this upgrade sequence. |
| **F-42** | **Raise to Medium.** Failed mounting changes where local game data is read and written; this is not merely a missing log message (`automount:57,68,167,174`). | Failure preventing normal launches, or a separate local check rejecting the wrong saves root. Neither is shown. The cited cloud-side guard does not establish local protection. |
| **F-43** | **Raise the storage-selection part to Medium; leave the odd assignment as clarity work.** Substring mount matching and choosing the first large unmounted partition do not establish that it is the intended external card (`automount:234-252`). | Exact mount-source matching and positive identification of the intended external device. Neither is shown. The quoted redirection text alone is not proof of a wrong branch: an assignment legitimately returns its substitution’s status. |
| **F-54** | **Narrow; keep Low.** Slash validation and the empty removal argument deserve hardening, but the supplied traversal example is wrong: `${index_bezel_name##*.}` removes through the **last** dot, so an ending `./../x` leaves `/x`, not `../x` (`rocknix-es-thebezelproject:401,438,454,570-600`). | Validated plain extensions and a rejected empty system name would remove the remaining concern. Those checks are not shown. The code itself defeats the stated `../` derivation. |
| **F-55** | **Keep Low only as “no in-tree callers found.”** The searches do not establish that installed commands have no manual or external users, and therefore do not prove removal is safe (packet’s distribution/interface `grep -rlF` searches: no hits). | A supported manual or external caller would refute complete deadness. The searches do not test that population. The packet itself treats the similarly caller-free `installtointernal` as a manual command rather than dead code. |
| **F-63** | **Raise to Medium, bounded to the permission defect.** A credential-bearing seed and its live copies retain mode `645`; the read permissions matter more than the pointless execute bit (`package.mk:29`; 08:06 `stat` results). | Private file modes or absence of secrets would refute this defect; the packet shows the opposite. Effective access by another account still requires traversable parent directories or an exporting service, which was not tested. |

## 3. What I could not judge

- **Actual hardware outcomes.** The governor proof records a missing command, not an H700 frequency change (`runemu.sh:465-467`; Group 1 output). The packet supplies no running-device evidence for CPU hotplug counting, panel behaviour, USB binding, Bluetooth pairing, backlight, suspend, internal repartitioning or ABL writes (`099-freqfunctions:12-45`; `paneladj:37-40`; `usbgadget:420-425`; `installtointernal:89-108`; `updateabl:69-72`).

- **Whether the background restores actually overtake another launch.** No completion trace, caller-side wait trace or shared-lock demonstration accompanies `runemu.sh:538-560`. The elapsed launch numbers do not answer that question.

- **Complete failure handling in the installer and bootloader updater.** The `find` fixture proves one command’s status behaviour, not the complete installer’s failure path. No full-script failed-write test is supplied for `updateabl:69-72`, nor a partial-listing test for `installtointernal:63`. Those control-flow tests can use stand-ins; physical hardware is needed for hardware consequences, not for every failure-handling check.

- **Upgrade behaviour as a whole.** The packet explicitly records no `tools/vm-upgrade-rehearsal` run. The passing `melonds-upgrade-test` covers the melonDS block, not the hint lifecycle, repeated interface-backup replacement, owner-file deletion or all update failures (`003-upgrade:8-17`; `post-update:32-38,208-251`).

- **Security exposure beyond the demonstrated unsafe state.** The empty-hash test does not establish acceptance of a blank password by SSH or another login service (`setrootpass:32-45`; Group 2 output). Mode `645` does not establish an unprivileged open through every parent directory (08:06 `stat` output). The packet also leaves the origin and writers of `/tmp/joypads` unresolved, so F-13’s “owner’s own trust domain” assertion is not established (`setsettings.sh:405-409`).

- **The Bluetooth archive’s complete trust boundary.** The save/restore locations are supplied, but archive permissions, share access rules, cloud selection rules and the extraction command’s protections are not (`rocknix-bluetooth:8-10,73-98`). I cannot verify either actual key export or safe handling of an archive replaced through the content-storage side.

- **Emulator semantics and intended precedence.** The packet does not supply the bezel-versus-overlay contract, the configured Kronos reader, or a real RetroArch result for the empty shader directory and empty core-option values (`setsettings.sh:778-790,821-822,1048-1087,1065`). Group 1’s `runemu.sh` proofs used a RetroArch stub; they prove command construction and file effects, not all emulator consequences.

- **The claimed upstream fixes and complete reachability dispositions.** The packet supplies counts of **43** upstream rows and **47** reachability rows, but not those complete tables or the relevant upstream diffs. Those counts do not verify the semantic repairs attributed to `25903bb59c`, `4e3972d037` and `6aa745572b`.

- **A measured improvement attributable to this reviewed code.** The time-to-play output says `Not a pass: the exit sync had no cloud to reach`; interface-based runs exercise the different image copy of `runemu.sh`, not the reviewed tree copy. The reported 0.64 s and 1.01 s are not proof of a completed cloud-enabled improvement over the stale baseline (`tools/time-to-play ... --no-configure-remote --vm --quick`, exit 1; recorded image/tree hash comparison).

- **Completion of the audit’s own acceptance criteria.** The supplied lint result is `13 CONTRACT FAILURE(S)`, with no passing final rerun. The packet does not supply completed punch-item outcomes, the final checker results or the outstanding reviewer artifacts. Those remain evidence gaps, not completed criteria (`tools/lint-audit-artifacts` output at 08:18; AC-02/03/04/13/15 scorecard).
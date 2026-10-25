## 1. My own findings

These findings concern the supplied read tree. Their status in the newer tree is addressed in part 3.

- **G-01 — Medium — `sysutils/busybox/scripts/init:883-889,1031-1081,298-331,432-437`** — The update acceptance path checks a filename substring and package-supplied MD5 files, not a trusted signature, before sourcing update metadata and running update scripts as root; compatibility checking itself executes update code. **Trigger: the player’s staged update files, including a hostile download; no remote delivery path is established.**
- **G-02 — High — `sysutils/busybox/scripts/init:394-437,853-858,1121-1136`** — Failed kernel, SYSTEM or bootloader writes do not stop the update: their exit status is discarded, “Update complete” is printed, staging files are deleted, and the machine reboots with an incomplete installation. **Trigger: nobody—an ordinary write or storage failure during an update.**
- **G-03 — High — `sysutils/busybox/scripts/init:403,420,899-906,1123-1129,1299-1311`** — Updates overwrite the only installed kernel/SYSTEM pair without retaining a bootable previous pair; an interrupted replacement has no rollback, and the next boot mounts SYSTEM before reaching update handling. **Trigger: nobody—a power cut or reset during replacement.**
- **G-04 — Medium — `sysutils/busybox/scripts/init:861-863,1063-1067,1075-1079,1142-1143`** — Update rejection calls cleanup that unmounts `/storage`, then returns to “Normal startup”; the next preparation step tries to move that now-missing mount instead of mounting storage again. **Trigger: the player’s invalid or incompatible staged update files, when cleanup successfully unmounts storage.**
- **G-05 — Medium — `sysutils/busybox/scripts/init:343-376`** — An empty old or new architecture string skips **both** architecture and device compatibility checks and returns success; missing metadata therefore bypasses the wrong-hardware protection without `.nocompat`. **Trigger: the player’s staged update files or damaged installed metadata.**
- **G-06 — Low — `sysutils/busybox/scripts/init:872-889,1010-1012`** — A bare kernel/SYSTEM pair passes the initial update-discovery test but fails the later branding test, which examines only archive filenames; the supposedly supported raw-pair update is deleted as unsupported. **Trigger: the player’s staged kernel/SYSTEM files.**
- **G-07 — Medium — `sysutils/busybox/scripts/init:1083-1104,1123-1129`** — The space check counts space that a smaller replacement SYSTEM will eventually release, but writes the kernel first; a growing kernel can exhaust the current free space after “Checking size: OK.” **Trigger: the player’s otherwise valid update files with that size combination.**
- **G-08 — Medium — `sysutils/busybox/scripts/init:50,201-211,261-263`** — NBD mounting constructs `/dev/nbd${NBD_DEV}S` instead of using the initialized `NBD_DEVS` counter; the ordinary first invocation targets `/dev/nbdS`, so the NBD boot path is broken. **Trigger: the player’s boot configuration selecting NBD.**
- **G-09 — Low — `sysutils/busybox/scripts/init:143-175`** — An unknown iSCSI option retains the previous iteration’s `option` value and is emitted as another instance of that previous flag, rather than being rejected. **Trigger: the player’s malformed iSCSI boot configuration.**
- **G-10 — Medium — `sysutils/busybox/scripts/init:621-633,651-665`** — Filesystem-check failures are mishandled: forced fsck result 4—errors remaining—takes the reboot path, while results of 16 or above bypass repair handling and continue boot. **Trigger: a damaged boot/storage medium or an ordinary filesystem-check failure.**
- **G-11 — Low — `sysutils/busybox/scripts/init:610-621`** — Every failed console read is treated as expiry of the repair countdown; EOF or another input error starts `fsck -y` immediately instead of preserving the advertised 120-second abort window. **Trigger: nobody—closed or unusable console input.**
- **G-12 — Low — `sysutils/busybox/scripts/init:86-99,1292-1294`** — Init errors open an unauthenticated shell without requiring `textmode` or `debugging`; the OS’s root-console paths are broader than the reviewed tty1 service. **Trigger: the player’s boot configuration or a failing boot medium.**
- **G-13 — Low — `sysutils/systemd/package.mk:332`; guest `s3`** — The recipe unconditionally requests enablement of `debug-shell.service`, but the guest check examines only `shell.service` on tty1; this additional boot-console path is outside the claimed shell assessment. **Trigger: nobody—image construction and boot; actual activation remains unverified.**
- **G-14 — Medium — `sysutils/systemd/scripts/userconfig-setup:17-40,46-66`** — First-boot copying and link creation are not checked before writing `.configured`; a partial initialization is marked complete and skipped on later boots. **Trigger: nobody—an I/O failure; the player’s existing files can also make these operations fail.**
- **G-15 — Low — `sysutils/systemd/scripts/userconfig-setup:70-78`** — A failed `ldconfig` still advances the OS stamp; when an older cache exists, subsequent boots stop trying to rebuild that stale cache. **Trigger: nobody—a cache-generation or cache-write failure.**
- **G-16 — Low — `sysutils/systemd/scripts/userconfig-setup:80-89`** — A locale copy interrupted after creating its destination directory is never retried, because directory existence is treated as completion. **Trigger: nobody—an interrupted or partially failed copy.**
- **G-17 — Low — `sysutils/autostart/sources/autostart:93-94`; `sysutils/system-utils/sources/scripts/input_sense:124-138,230-271`** — Ordinary settings are additional root-command inputs: `system.cpugovernor` and function-key action strings select executables and arguments, outside the two advertised hook directories. **Trigger: the player’s settings files; this is an additional trusted-code interface, not a privilege escalation over the owner.**
- **G-18 — Medium — `sysutils/autostart/sources/autostart:73-91`; `sysutils/autostart/system.d/rocknix-autostart.service:7-10`** — A custom hook runs in the foreground without a local execution limit, and UI startup comes afterwards; a hook that never returns prevents UI startup. **Trigger: the player’s hook files.**
- **G-19 — Low — `sysutils/autostart/sources/autostart:25,40,53,65,76,88-94`** — `2>&1 >>${BOOTLOG}` leaves stderr on the original stdout rather than sending it to `boot.log`; the boot log omits the error half of command output. **Trigger: nobody or the player’s hooks whenever a command writes an error.**
- **G-20 — Low — `sysutils/autostart/sources/autostart:81-97`** — UI startup is backgrounded and its result is never collected; autostart announces completion even when `systemctl start` fails. **Trigger: the player’s UI selection or an ordinary UI-unit failure.**
- **G-21 — Low — `sysutils/powerstate/system.d/powerstate.service:15`; `sysutils/busybox/config/profile:6-23`; `sysutils/powerstate/sources/powerstate.sh:11`** — `/etc/profile` is shell code, not an `EnvironmentFile`; systemd does not execute its loops or source its files. The script’s separate sourcing supplies the environment, masking this broken unit declaration. **Trigger: nobody—every service start.**
- **G-22 — Low — `sysutils/powerstate/sources/powerstate.sh:54-61`** — The warning threshold is not validated like the battery reading: Bash’s numeric comparison interprets it as an arithmetic expression, rather than safely rejecting non-numeric setting values. **Trigger: the player’s threshold setting when the discharge-warning branch runs.**
- **G-23 — Medium — `sysutils/system-utils/sources/scripts/input_sense:283-329,347-356`** — `INPUT_DEVICES` is cleared before the retry loop, not on each retry; a missing device category accumulates up to six copies of the same device and starts duplicate event readers. The `elif` classification also counts a key/joystick composite as only one category. **Trigger: nobody—missing, late or composite input hardware.**
- **G-24 — Low — `sysutils/system-utils/sources/scripts/input_sense:105-106,347-370`** — The disconnect “reload” only changes the consumer’s array and never recreates the already-running event readers; it cannot add a newly assigned device path. The two disconnect patterns are also identical, making the second arm unreachable. **Trigger: an inserted or disconnected input device.**
- **G-25 — Low — `sysutils/system-utils/sources/scripts/input_sense:93-96,360,483-508`** — The pipeline discards `EV_ABS` events before the `ABS_HAT0X/Y` handlers, so the hat-based D-pad mappings cannot run. **Trigger: an inserted controller using hat events with the player’s D-pad mapping enabled.**
- **G-26 — Medium — `sysutils/system-utils/sources/scripts/input_sense:151-165,364-370,401-425`** — The disconnect handler neither clears pressed states nor stops volume repeat; the repeat child retains its own copy of the pressed flag, leaving repeat and modifiers latched when a release is lost, until another release or a service restart. **Trigger: an input device disconnected while a relevant button is held.**
- **G-27 — Low — `sysutils/system-utils/sources/scripts/input_sense:230-271,360-443`** — Configurable actions execute synchronously in the sole event-consumer loop; one action that does not return prevents processing later releases, power events and lid events. **Trigger: the player’s action settings.**
- **G-28 — Low — `sysutils/system-utils/sources/scripts/input_sense:216-221`** — The kill-chord debounce uses wall-clock time; after a backward clock step, its negative elapsed time remains below three seconds and suppresses further kills until the clock catches up. **Trigger: nobody—a clock correction while the service remains running.**
- **G-29 — Low — `sysutils/system-utils/sources/scripts/input_sense:180-181,224`** — Kill-target file contents are split directly into `killall` arguments without `--`; a target string can change signal/options instead of merely naming processes. **Trigger: the player’s `/tmp/.process-kill-data` file.**
- **G-30 — Medium — `sysutils/udevil/system.d/udevil-mount@.service:7-11`** — Actual mount and unmount failures—not just the optional Samba calls—are ignored; a failed mount leaves the oneshot active because of `RemainAfterExit`, so another start does not retry it. **Trigger: an inserted medium whose mount operation fails.**
- **G-31 — Low — `sysutils/util-linux/system.d/fstrim.service:6-7`** — A real trim failure is ignored and followed by updating `fstrim.run`; the unit reports success, and that stamp cannot establish that trimming succeeded. **Trigger: nobody—a discard failure when the service runs.**
- **G-32 — Low — `sysutils/systemd/package.mk:222-224`** — The resolver-edit fallback does not handle a missing match: `sed` succeeds without replacing anything, so `|| echo` never adds the intended setting when the template line changes. **Trigger: nobody—a build against a changed or missing template line.**
- **G-33 — Low — `hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh:33-45`** — Port “validation” deletes invalid characters: `12x34` becomes valid port `1234`, contrary to the stated reject-invalid-input rule, and produces the wrong SSH destination. **Trigger: the player’s/developer’s VM host configuration; this is a harness defect.**
- **G-34 — Low — `sysutils/busybox/scripts/init:403,872-874,967,1095-1096`** — Update paths are not filename-safe: newline-bearing archive names are cut by `ls | head`, while space-bearing extracted target paths break the size-field parsing and unquoted transfer operands. **Trigger: the player’s staged filenames or archive directory names.**

## 2. Refuting the first reader

**F-04 should be Medium. None of F-01–F-16 warrants High on the supplied evidence. F-02 contains a real quoting defect that the “design” label excuses.** The relevant distinction is between the owner deliberately supplying root code and an inserted medium receiving weaker protections than the configured policy requires (`busybox/config/profile:19-23`; `udevil/config/udevil.conf:209-233`).

### F-01 — Agree: Low defect

The custom-loop failure survives, including execution of the wrong filename with an extra argument. The guest demonstrates that exact consequence. The common loop has the same unsafe shape, but operates on image files.

**Falsifier:** enforced filename/executable restrictions before iteration, or correctly quoted execution with suitable entry checks. The packet shows neither, and guest `s5` supplies counterexamples. A `-f` check alone does **not** fix the non-executable-file case; the executable policy also needs attention (`autostart:50-54,71-77`; guest `s5`).

### F-02 — Narrow: Low defect plus an intentional interface

Sourcing the owner’s profile files is an intentional root-code interface. Sourcing an **unquoted filename** is a separate code defect, not an architectural choice. It can source the wrong file, supply unintended arguments, or fail while preparing services.

**Falsifier:** quoting at the source operation or a prior filename restriction. Neither appears. Also, `EnvironmentFile=/etc/profile` does not source the profile a second time; that part of the retrospective is wrong—see G-21 (`busybox/config/profile:19-23`; `rocknix-autostart.service:9`; `powerstate.service:15`; `powerstate.sh:11`).

### F-03 — Narrow: the installation facts survive; the “unused applets are a bug” verdict does not

The setuid binary and enabled applets are established. A repository search with zero callers does not establish that interactive tools such as `passwd`, `su` and `login` are unused. Nor does the executable’s setuid bit establish that every applet retains that privilege or that HTTPD is listening.

**Falsifier for the factual portion:** a non-setuid installed binary or disabled applets; guest `s4` shows the opposite. **Falsifier for the unused-code argument:** legitimate interactive or non-script use; run `22-applet-callers` does not examine that. Keep this as a Low hardening question, not an instruction to disable four applets (`busybox/package.mk:177`; `busybox-target.conf:30-31,549-558,888-895`; runs `22`, guest `s4`).

### F-04 — Re-grade: Medium configuration-security defect

The omission survives. The configuration explicitly says that a filesystem-specific entry **overrides**, rather than supplements, the general defaults. Btrfs therefore lacks the three protections in the stated policy. An inserted medium is not equivalent to the owner deliberately writing a root hook.

**Falsifier for the runtime consequence:** another enforced layer supplying these flags, including an applicable fstab entry, or actual mount output showing them. The packet supplies no such result. It also supplies no insertion-to-code-execution chain, so High is not established (`udevil.conf:204-215,233`; guest `s6`).

### F-05 — Agree, narrowed to Low dead-reference/clarity work

The absent Samba helper is real on the tested image and consistent with the disabled feature. This is not proof that mounting fails: the prefix deliberately ignores the helper’s failure. The more consequential ignored mount failure is G-30.

**Falsifier:** the helper being installed on the relevant build, or the calls being omitted there. Guest `s6` shows the missing helper and the unit contains both calls (`udevil-mount@.service:9-10`; guest `s6`).

### F-06 — Narrow: Low conditional copy defect

The copy makes `.ssh` a regular file **when that path does not already exist as a directory**. The supplied guest does not exercise the affected build configuration.

**Falsifier:** guaranteed creation of `/storage/.ssh/` before either copy on every key-seeded build. The packet does not establish that guarantee. Absence of `/usr/config/ssh` on the guest proves only that this guest cannot reproduce the failure (`userconfig-setup:30-34`; reported second site `post-update:54-57`; guest `s1`).

### F-07 — Narrow: Low design for this service, not an OS-wide shell boundary

The observed automatic link selects `shell.service` through `textmode.target`, and its command contains no authentication. The ordinary guest boot proves inactivity, not successful behavior on a textmode boot.

**Falsifier:** an authentication wrapper or a different activation chain. Neither is shown for this service. The broader assertion that unauthenticated shells exist **only** in textmode fails: init’s error shell is another explicit route, and the debug-shell enablement requires examination (`shell.service:9,13-14,23`; `init:86-99,1215-1216`; `systemd/package.mk:332`; guest `s2c`, `s3`).

### F-08 — Agree as Low design, but the inventory is incomplete

Owner-controlled boot markers are not, by themselves, a privilege escalation. The three listed markers are not the complete set: init also selects factory reset from `reset_oe`/`reset_xbmc` and restore from a matching archive.

**Falsifier:** the markers not being consumed or not changing the selected behavior. The code directly shows both. Their existence does not establish that resize, reset or restore implementations are safe; those implementations need their own review (`init:1361-1369`; `var-log.mount:16-17`; `debugconfig.service:5-6`).

### F-09 — Agree as Low inventory information, not a running defect

The recipe disables the cron applets and omits the units when cron support is off. Keeping optional upstream support is not itself a defect.

**Falsifier:** a shipped configuration enabling cron, or another installed cron implementation. The supplied build-option report and guest show no such activation (`busybox/package.mk:81-85,193-201`; run `22`; guest `s6`).

### F-10 — Narrow: Low shipping-cost finding

The copy-all/install-selected distinction survives. The reported counts support dormant shipped content, not a security exposure merely from its presence.

**Falsifier:** platform-scoped copying, or a normal execution reference into those other platform trees. The recipe disproves scoped copying. The generator’s “runs on none” output is not a complete cross-reference or symlink-resolution proof; “not directly selected by these dispatchers” is the defensible wording (`quirks/package.mk:16-18`; `system-utils/package.mk:27-34`; `autostart:16-40`; reachability-generator output).

### F-11 — Agree as a Low currency/merge item, not an outstanding bug fixed independently

The old BusyBox and systemd pins are visible. The packet reports the newer upstream versions and HTTPS move, so the stated merge rule applies. Version distance alone does not establish a security vulnerability. The BusyBox recipe also declares a SHA-256 digest; plain HTTP alone does not prove accepted payload substitution.

**Falsifier:** matching old/new pins or an already-HTTPS read-tree URL. The supplied recipes and comparison report show otherwise. Actual digest enforcement and vulnerability status are not demonstrated (`busybox/package.mk:7-11`; `systemd/package.mk:6-10`; run `23-modified`).

### F-12 — Agree as Low merge planning, not a current runtime defect

The installed core pattern explicitly invokes the keeper, while the deletion report removes that configuration upstream. A merge decision is necessary.

**Falsifier:** the merged configuration retaining that invocation, or a replacement path that preserves the keeper’s contract. The packet shows neither completed resolution; it shows the deletion and current invocation (`busybox/sysctl.d/99-coredump.conf:4`; run `19-deleted`, commit `8bce25b3b7`).

### F-13 — Narrow: Low merge review, not a proved conflicting-key failure

The file move is established. The contents and precedence of the replacement `60-rocknix.conf` are not supplied, so an actual key conflict is not proved. Previously seeded settings also need consideration, not just the source-tree deletion.

**Falsifier:** compatible replacement keys and an upgrade path that handles existing stored defaults correctly. The packet does not establish that result (`systemd/config/sysctl.d/rocknix.conf:1-3`; `systemd/package.mk:256,264-265`; `userconfig-setup:9-17`; runs `15-added`, `19-deleted`).

### F-14 — Agree: Low clarity item

The recipes implement the distinction but do not explain it. The general boot-order description also needs the conditional `/usr/lib/autostart/${HW_DEVICE}` layer, which lies between common and custom hooks.

**Falsifier:** an explanation in the two complete recipes or a complete adjacent dispatch description. Neither is present in those supplied files (`system-utils/package.mk:14-34`; `quirks/package.mk:14-20`; `autostart:57-78`).

### F-15 — Narrow: Low hardening question

Root service launch is established. “29 units run as root” is imprecise because the count includes targets, mounts and a timer, not 29 service processes. Missing `User=` is not proof that every task can safely be changed to an unprivileged user, nor proof of an exploit.

**Falsifier:** explicit non-root service identities or demonstrated privilege dropping in the relevant execution paths. Run `10b` shows no declared identities, and guest `s2b` confirms root for the three sampled processes; that does not inspect every helper’s internal behavior (`10b-units-user-unmasked`; guest `s2b`; `fs-resize.target:1-5`; `fstrim.timer:1-10`).

### F-16 — Narrow: Low diagnostic warning, not an OS security defect

The observed mismatch between `is-enabled` and vendor links survives. The claim that only `.wants` links answer what runs does not: these sensing services are explicitly started by a script without such links.

**Falsifier for the observed tool result:** the tested units reporting enabled; guest `s2` reports otherwise. **Counterexample to the broader conclusion:** the supplied dynamic starter itself. Activation must include dependencies, conditions and script-driven starts, not just enablement state or symlinks (guest `s2`, `s2c`; `098-deviceutils:7-40`).

## 3. What I could not judge

- **Whether the guest exactly represents the read tree.** Guest `s1` reports BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`, while the supplied source is at `8ebaf8daad`. No per-file comparison ties the tested image to all reviewed sources. The guest proves its observed behavior, not every read-tree path.

- **Which new findings upstream has already settled.** Run `23-modified` gives change sizes and commits, not newer bodies for init, `input_sense`, `userconfig-setup` or the systemd recipe. Those comparisons are required before assigning post-merge work for the corresponding G findings. The packet does establish the BusyBox URL/version settlement and the udev rule’s `--no-block` change; those are not new bugs here (runs `23-modified`, `16-bb-systemd-log`).

- **Actual removable-media protections and applet privileges.** Guest `s6` prints configuration, not a mounted btrfs filesystem’s effective flags. Guest `s4` prints mode and applet presence, not per-applet privilege retention or listening sockets. Digest declaration is visible, but the downloader’s enforcement is not (`udevil.conf:204-233`; `busybox-target.conf:30-31`; `busybox/package.mk:8`; guest `s4`, `s6`).

- **The complete unit and event-control graph.** The generated `debug-shell.service`, its conditions, tty and actual link are absent. `usercache.service:5` names `automount.service` and `autostart.service`, but aliases and other ordering edges are not supplied, so I cannot establish a cache-startup race from those names alone. The contents of `99-input.rules` are also missing; they could provide an external service restart that contains the disconnect failures identified above (`systemd/package.mk:332`; `usercache.service:5`; `rocknix-autostart.service:4`; `input_sense:364-370`).

- **Whether power/lid handling is coordinated.** The recipe makes logind suspend on power and lid events, while `input_sense` invokes another suspend handler. The packet does not supply the inhibitor or helper behavior needed to decide whether both act on one event (`systemd/package.mk:217-219`; `input_sense:432-443`).

- **Remote reach and update provenance before staging.** Init’s acceptance behavior is visible, but the packet does not show who can deliver files into `.update`, whether the normal downloader authenticates them, or the network exposure of the running image. I therefore do not turn G-01 into a proved unauthenticated remote compromise. AVFS/tar path handling also cannot be judged from their invocation alone (`init:35-36,872-937,1031-1081`; guest `s2`, `s4`, `s6`).

- **Password-state recovery and destructive maintenance implementations.** `usercache-setup:18` is described but its body, replacement password source and installed permissions are not supplied. The resize implementation, factory-reset/restore implementations and the second SSH-copy site are not shown in full. “Finished userconfig.service” does not resolve their safety or prove successful initialization (`fs-resize.service:7`; `init:1363-1368`; `userconfig-setup:66`; guest `s1`).

- **Handheld behavior and exceptional-path recovery.** The supplied guest steps do not exercise real suspend, battery hardware, failed updates, interrupted initialization, a textmode boot, or seeded developer keys. They also do not prove the VM quirks’ power-cut guarantees or same-boot rescue-mask refresh (`powerstate.sh:19,54-61`; `092-retroarch-surface:104-111`; `095-cloud-ssh:58-71`; `097-retired-rescue-masks:25-39`; guest cycle `s1`–`s6`).

- **Full coverage and package security currency.** Membership and line counts are not substitutes for the omitted file bodies. The packet contains only excerpts of the BusyBox configurations and omits numerous helpers and platform implementations. Supplied pins also do not establish current author releases or applicable vulnerabilities (`01-membership` output; `12-busybox-flags`; `busybox/package.mk:7-11`; `systemd/package.mk:6-10`; `nvtop/package.mk:5-9`).
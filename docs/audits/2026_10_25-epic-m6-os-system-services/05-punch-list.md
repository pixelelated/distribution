# Punch list (Phases 5 and 6) — M6.P2 T22, the OS's system services and platform quirks (#669)

The audit issue is #1103, a sub-issue of #669. There is one item per finding of `04` after both seats' grading (`04` § Second opinion), with the severities graded there. The seats' 46 items are grouped by file under the item that owns them. Every confirmed line but G-33's is in the merge base and in upstream's tree at `651150fc88`, so it is upstream-carried, and its class decision is the maintainer's on #346 (D-WORKFLOW-209). Each item's **Proposed** line was this lane's proposal; the coordinator's ruling (#669, 10:13 and 10:25 UTC) is in § Phase 7 resolution gate. The audit issue #1103 carries one checkbox per item.

## PL-01: udevil mounts a btrfs medium without nosuid,noexec,nodev, against its own file's rule, or refuses it (the option is not allowed)
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-04, G-44, L-05
- **Owner area:** udevil
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-04, G-44, L-05; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Yes: on one GENERIC_X64 guest: a loop-backed btrfs filesystem presented as a USB-storage medium, or `udevil --mount` on a loop device, reading `/proc/mounts`
- **Already written:** nothing inherited: mounts are transient
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried, `c288a47e62`), with the VM proof

## PL-02: scripts/init writes the kernel and SYSTEM without checking either write, then reports Update complete
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-02
- **Owner area:** the initramfs update path
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-02; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Yes: on one GENERIC_X64 guest: a SYSTEM write that fails (a full or read-only `/flash`) during an in-place update
- **Already written:** a device whose update write failed reboots into what was written; nothing on `/storage`
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-03: a rejected update leaves /storage unmounted at switch_root and deletes the staged update
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-04 (Argon's extension)
- **Owner area:** the initramfs update path
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-04 (Argon's extension); file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Yes: on one GENERIC_X64 guest: stage an update with a wrong md5 in `/storage/.update`, reboot, read `/proc/mounts` and the journal
- **Already written:** a device that met a rejection booted once without `/storage`; the next boot mounts it
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried), with the VM proof

## PL-04: debug-shell.service is enabled on every boot: an unauthenticated root shell on its console
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** G-13
- **Owner area:** systemd's recipe
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-13; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Yes: on one GENERIC_X64 guest: `systemctl is-active debug-shell.service` and its tty
- **Already written:** nothing inherited: the unit is the image's
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** settled by the next base merge (`f2379f83b7`); the VM proof records it until then

## PL-05: input_sense starts up to six duplicate readers per device on a machine without a joystick
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-23, G-43 (1)
- **Owner area:** input_sense
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-23, G-43 (1); file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Yes: on one GENERIC_X64 guest: count `evtest` processes per `/dev/input/event*` on the guest
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried, `dc5f51ad72`), with the VM proof

## PL-06: autostart's common and custom loops run entries unguarded and unquoted; its redirects, waits and the interface's start are unchecked
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-01, G-19, G-20, G-42, L-01
- **Owner area:** autostart
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-01, G-19, G-20, G-42, L-01; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Proven on the guest (s5)
- **Already written:** nothing inherited: the loop writes nothing
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-07: /etc/profile sources /storage/.config/profile.d/* unquoted
- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-02, L-02
- **Owner area:** busybox's profile
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-02, L-02; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried); the hook itself recorded as a design

## PL-08: busybox is setuid root with su, login, passwd and httpd+CGI enabled and no caller in the tree
- **Severity:** Low
- **Category:** Security
- **Question:** Q5
- **Source Finding:** F-03, L-04
- **Owner area:** busybox
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-03, L-04; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Proven on the guest (s4)
- **Already written:** nothing inherited: a configuration choice
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (a hardening question; the pin itself is #997's)

## PL-09: unit lines that hide failures: samba-autoshare absent, udevil's mount and fstrim's trim ignored
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-05, G-30, G-31, L-06
- **Owner area:** udevil, util-linux
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-05, G-30, G-31, L-06; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Proven on the guest (s6) for samba-autoshare
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-10: #740's copy has a second site at post-update:54-57
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-06, L-07
- **Owner area:** userconfig-setup, post-update
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-06, L-07; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it (reachable only with `LOCAL_SSH_KEYS_FILE`)
- **Already written:** #740's own line
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #740 (a comment naming the second site)

## PL-11: four unauthenticated console or physical root paths: textmode, init's error shell, recovery_mode's USB export, /flash hooks
- **Severity:** Low
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-07, G-12, G-38, G-39, L-03
- **Owner area:** initramfs, busybox units
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-07, G-12, G-38, G-39, L-03; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Proven on the guest for `shell.service`; the rest read
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** design: LibreELEC's recovery and console paths for a device in the owner's hand; recorded, no change

## PL-12: boot markers under /storage switch root behaviour; two select targets this image lacks
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-08, L-10
- **Owner area:** initramfs, units
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-08, L-10; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** design for resize, volatile-log and debug; the reset and restore markers settled by the next base merge (`a98a3066f5`)

## PL-13: cron's units and default ship on no image (CRON_SUPPORT=no)
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-09, L-08
- **Owner area:** busybox
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-09, L-08; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Proven on the guest (s6)
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** design: carried, off by option

## PL-14: 213 platform files (108,294 bytes) and 8 system-utils rows ship where they are never selected
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-10
- **Owner area:** quirks, system-utils
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-10; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** design: carried by placement (D-WORKFLOW-185)

## PL-15: busybox 1.36.1 over http, systemd 255.8, util-linux 2.39.2 against upstream's 1.38.0, 261.2, 2.42.4
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-11
- **Owner area:** busybox, systemd, util-linux
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-11; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** settled by the next base merge; the busybox pin #997

## PL-16: collision C-1: upstream's journal crash logging deletes the fork's core pattern
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-12
- **Owner area:** busybox sysctl, the core keeper
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-12; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** design, deferred to the coordinator before the next base merge (D-INFRA-011/012/013)

## PL-17: collision C-2: upstream ships the sysctls in the image and deletes sysctl.d/rocknix.conf
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-13
- **Owner area:** systemd's sysctls
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-13; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** design, deferred to the coordinator before the next base merge

## PL-18: neither recipe says which files each image carries or runs; the boot order is written nowhere
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-14
- **Owner area:** quirks, system-utils
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-14; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (comments in upstream-carried recipes); `02`'s tables are the record meanwhile

## PL-19: no unit declares a user; every service runs as root
- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-15
- **Owner area:** the units
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-15; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Proven on the guest (s2)
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** design: a single-user handheld

## PL-20: systemctl is-enabled reads disabled for every vendor-linked unit
- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-16, L-15
- **Owner area:** tooling
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (F-16, L-15; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Proven on the guest (s2, s2c)
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** an Instruction File Recommendation to the coordinator (`generic-x64-vm-testing.md`)

## PL-21: the update path's acceptance and safety: metadata sourced before acceptance, both compat checks skipped on empty arch, a bare pair refused, the space check's order, no rollback pair, unquoted operands
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-01, G-03, G-05, G-06, G-07, G-34
- **Owner area:** the initramfs update path
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-01, G-03, G-05, G-06, G-07, G-34; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried); G-03 a design (no A/B)

## PL-22: init's netboot and fsck paths: the NBD device name, iSCSI option reuse, fsck results 4 and 16+, the repair countdown
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-08, G-09, G-10, G-11
- **Owner area:** initramfs
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-08, G-09, G-10, G-11; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-23: userconfig-setup marks first boot done without checking it, and its stamps and locale copy skip a retry; QUIRK_DEVICE is empty there
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-14, G-15, G-16, G-35
- **Owner area:** userconfig-setup
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-14, G-15, G-16, G-35; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** a device whose first boot failed part-way carries `/storage/.configured`; the copies are not retried
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-24: the autostart runner: a setting run as a command, a hook with no timeout, stale unit names in Before=
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-17, G-18, G-45
- **Owner area:** autostart, the units
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-17, G-18, G-45; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-25: powerstate: EnvironmentFile=/etc/profile reads no shell; the threshold as arithmetic; the first boot's LED variables; three loop defects
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-21, G-22, G-36, G-37
- **Owner area:** powerstate
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-21, G-22, G-36, G-37; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-26: input_sense: reload restarts nothing, hat events filtered out, a latched repeat on disconnect, blocking actions, a wall-clock debounce, killall operands
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-24, G-25, G-26, G-27, G-28, G-29, G-43 (2, 3)
- **Owner area:** input_sense
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-24, G-25, G-26, G-27, G-28, G-29, G-43 (2, 3); file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried)

## PL-27: systemd's recipe and hosts: a dead resolver fallback, /etc linked into /storage, /etc/hosts dangling, two nobody shells
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-32, G-40, G-41, G-46
- **Owner area:** systemd
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-32, G-40, G-41, G-46; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** No guest needed: the tree shows it
- **Already written:** --
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** #346 (upstream-carried); G-40 a design

## PL-28: 095-cloud-ssh keeps 12x34 as port 1234, against its own comment
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-33
- **Owner area:** the GENERIC_X64 quirks (a developer's tool, D-QA-053)
- **Where:** `04-analysis.md` § Risk Assessment and § Second opinion (G-33; file:line at `8ebaf8daad`); `02-forward-audit.md` § Proofs
- **Can this be done on the VM?** Yes: on the host, the quirk's port block over a constructed fw_cfg value; then on a guest
- **Already written:** nothing inherited: the VM's own file
- **Acceptance:** the owner's criteria once ruled; for a VM proof named above, its line quoted on the owning issue
- **Proposed:** a fork `bug` (the fork's own code)

## For #585: one line each (the coordinator posts them at acceptance)

```
- PL-01 (T22, #669) projects/ROCKNIX/packages/sysutils/udevil/config/udevil.conf:233,245 -- default_options_btrfs = compress=zstd:3 is not in allowed_options, so udevil refuses every btrfs medium ("denied 90: option 'compress=zstd:3' is not an allowed option") while the unit reads active; fix: give btrfs nosuid,noexec,nodev,noatime defaults and allow what they use (allowed_options_btrfs), or drop btrfs from allowed_types; evidence: guest-cycle-2/c1b-btrfs.txt (vfat control mounts nosuid,nodev,noexec).
- PL-06 (T22) sysutils/autostart/sources/autostart:50-53,73-76 -- the common and custom loops run ${script} unguarded and unquoted: an empty directory runs the literal glob, a directory or a mode-644 file errors, and a hook named "40 split" runs "40" with the argument "split"; fix: [ -f "${script}" ] && [ -x "${script}" ] && "${script}" (as :23-25 do), plus 2>&1 order at :25,40,53,65,76,88,89,91,94 (>>${BOOTLOG} 2>&1), and collect the backgrounded UI start (:91); evidence: guest-cycle/s5b-result.txt.
- PL-07 (T22) sysutils/busybox/config/profile:19-21 -- . ${CONFIG} sources /storage/.config/profile.d/* unquoted, so a name with a space sources another file with arguments; fix: . "${CONFIG}" (one quoted expansion); evidence: the line (the hook itself is a design).
- PL-09 (T22) sysutils/udevil/system.d/udevil-mount@.service:7,9-10; sysutils/util-linux/system.d/fstrim.service:6-7 -- ExecStart=- hides a refused mount and RemainAfterExit leaves the unit active; ExecStartPost calls /usr/lib/samba/samba-autoshare, absent when SAMBA_SUPPORT=no; fstrim's failure is ignored and its stamp written anyway; fix: drop the - on the mount, guard the samba lines by existence (ExecStartPost=-/bin/sh -c '[ -x ... ] && ...' or ConditionPathExists), stamp only on success; evidence: guest-cycle-2/c1b-btrfs.txt, guest-cycle/s6b-udevil-rule.txt.
- PL-18 (T22) hardware/quirks/package.mk:16-18; sysutils/system-utils/package.mk:27-34 -- neither recipe says that every platform ships to every image (selected at boot by HW_DEVICE) or that device files install for ${DEVICE} only; fix: a comment in each; evidence: 02 § The reachability table.
- PL-21 (T22) sysutils/busybox/scripts/init:298-331,349,872-889,1083-1129,403 -- update acceptance sources the update's os-release and runs its canupdate.sh before acceptance; an empty arch skips both compat checks; a bare KERNEL/SYSTEM pair is refused and deleted; the space check credits the old SYSTEM but writes the kernel first; ls|head and unquoted dd operands; fix: quote the operands and test the bare pair at :883; the rest are notes for the update path's owner; evidence: 04 § Second opinion (G-01, G-05, G-06, G-07, G-34).
- PL-22 (T22) sysutils/busybox/scripts/init:205,143-174,618,623-633,652-654 -- mount_nbd uses /dev/nbd${NBD_DEV}S (the unset NBD_DEV, not NBD_DEVS); the iSCSI loop never resets option; read's status is tested twice at :618 (the second $? is the first test's); fsck result 4 after -y reboots and 16+ continues; fix: ${NBD_DEVS}; option=""; save $? once; evidence: 04 § Second opinion (G-08 to G-11).
- PL-23 (T22) sysutils/systemd/scripts/userconfig-setup:17-66,76-77,80-83,24-27 -- .configured is touched without checking the copies before it; the ld.so stamp is written whatever ldconfig returned; the locale copy is done when its directory exists; QUIRK_DEVICE is empty there (dead today: no device has a config/); fix: write each stamp only on success; evidence: 04 § Second opinion (G-14, G-15, G-16, G-35).
- PL-24 (T22) sysutils/autostart/sources/autostart:93-94; sysutils/autostart/system.d/rocknix-autostart.service; sysutils/systemd/system.d/usercache.service:5, userconfig.service:5 -- a setting (system.cpugovernor) is run as a command; a hook that never returns holds off the interface (Type=oneshot, no TimeoutStartSec); Before= names automount.service and autostart.service, which do not exist; fix: case on the governor names, a TimeoutStartSec, the real unit names; evidence: 04 § Second opinion (G-17, G-18, G-45).
- PL-25 (T22) sysutils/powerstate/system.d/powerstate.service (EnvironmentFile=/etc/profile); sysutils/powerstate/sources/powerstate.sh:19-20,59-61,71 -- EnvironmentFile reads KEY=VALUE lines, not the profile's shell; the threshold setting is evaluated as arithmetic; an empty AC_STATUS (no battery) never selects a mode; no head -n1 for two batteries; the >97% branch runs ledcontrol every 2 s while charging; fix: drop the EnvironmentFile, validate the threshold as digits, head -n1, move the elif; evidence: 04 § Second opinion (G-21, G-22, G-36, G-37).
- PL-26 (T22) sysutils/system-utils/sources/scripts/input_sense:105-106,151-163,216-224,302-311,360,364-371,512-536 -- the two disconnect patterns are identical and a reload restarts no reader; the hat handlers never see an event (the grep passes EV_KEY and EV_SW only); the volume repeat survives a disconnect; actions block the loop; a wall-clock debounce; killall ${TO_KILL} unquoted with no --; the if/elif counts a composite device as keys only; fix: per line in 04 § Second opinion; evidence: G-24 to G-29, G-43.
- PL-27 (T22) sysutils/systemd/package.mk:222-224,258-276,295,322; sysutils/busybox/package.mk:184; sysutils/systemd/scripts/network-base-setup:111-114 -- sed -i ... || echo never falls back (sed succeeds without a match); /etc/hosts dangles without hosts.conf and never names the hostname; two nobody entries with different shells, systemd-network with /bin/sh; fix: grep -q before sed, write 127.0.0.1 and the hostname, one nobody with /bin/false; evidence: 04 § Second opinion (G-32, G-41, G-46; G-40 is a design).
```

## For #346: the root-surfaces list's sentence (the coordinator posts it)

The images give root without authentication to anyone holding the device:
- **a console on a `textmode` boot** (`shell.service`, `scripts/init:1215-1216`);
- **a console on any initramfs error** (`init:86-99`);
- **`debug-shell.service` on tty9 on every boot** in the read tree (`systemd/package.mk:332`, proven on the guest; upstream's `f2379f83b7` settles it at the next base merge);
- **a USB mass-storage export of every card with Vol- held at boot**, or `recovery` on the command line (`init:537-592`);
- **busybox installed setuid root** with `su`, `login`, `passwd` and `httpd`+CGI enabled and no caller in the tree (`busybox/package.mk:177,209`; `busybox-target.conf:30,549,554,556,888,894`);
- **every service and hook running as root**, with no unit naming a user (29 units; the hook directories `/storage/.config/autostart/` and `/storage/.config/profile.d/`).

Each is a design for a single-user handheld in its owner's hand. Which of them the maintainer keeps is the policy question.

## Index

```yaml
punch_index:
- id: PL-01
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-04, G-44, L-05"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-02
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-02"
  tracked: "#1105"
  outcome: resolved # `6cfe1fdba1`
- id: PL-03
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-04 (Argon's extension)"
  tracked: "#1106"
  outcome: resolved # `ffd1e34dbd`
- id: PL-04
  severity: Medium
  category: Security
  question: Q3
  source_finding: "G-13"
  tracked: "#346"
  outcome: deferred:#346
- id: PL-05
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-23, G-43 (1)"
  tracked: "#344"
  outcome: deferred:#344
- id: PL-06
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-01, G-19, G-20, G-42, L-01"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-07
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-02, L-02"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-08
  severity: Low
  category: Security
  question: Q5
  source_finding: "F-03, L-04"
  tracked: "#346"
  outcome: deferred:#346
- id: PL-09
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-05, G-30, G-31, L-06"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-10
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-06, L-07"
  tracked: "#740"
  outcome: deferred:#740
- id: PL-11
  severity: Low
  category: Security
  question: Q3
  source_finding: "F-07, G-12, G-38, G-39, L-03"
  tracked: "#669"
  outcome: resolved # #669
- id: PL-12
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-08, L-10"
  tracked: "#669"
  outcome: resolved # #669
- id: PL-13
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-09, L-08"
  tracked: "#669"
  outcome: resolved # #669
- id: PL-14
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-10"
  tracked: "#669"
  outcome: resolved # #669
- id: PL-15
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "F-11"
  tracked: "#669"
  outcome: resolved # #669
- id: PL-16
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-12"
  tracked: "#1104"
  outcome: deferred:#1104
- id: PL-17
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-13"
  tracked: "#1104"
  outcome: deferred:#1104
- id: PL-18
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-14"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-19
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-15"
  tracked: "#669"
  outcome: resolved # #669
- id: PL-20
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-16, L-15"
  tracked: "#669"
  outcome: deferred:#669
- id: PL-21
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-01, G-03, G-05, G-06, G-07, G-34"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-22
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-08, G-09, G-10, G-11"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-23
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-14, G-15, G-16, G-35"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-24
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-17, G-18, G-45"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-25
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-21, G-22, G-36, G-37"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-26
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-24, G-25, G-26, G-27, G-28, G-29, G-43 (2, 3)"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-27
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-32, G-40, G-41, G-46"
  tracked: "#585"
  outcome: deferred:#585
- id: PL-28
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-33"
  tracked: "#1107"
  outcome: resolved # `9145b90fac`
```

## Phase 7 resolution gate

The coordinator's ruling on #669 (10:13 UTC, PL-01 and PL-05 at 10:25 UTC). A bug's item is Deferred to its issue until its stream's commit, then Resolved with it.

| Item | Outcome | Tracked |
| --- | --- | --- |
| PL-01 | Deferred | #585: a Low (the window: udevil refuses every btrfs medium, `guest-cycle-2/c1b-btrfs.txt`); the line below |
| PL-02 | Resolved | `6cfe1fdba1` (#1105, stream S1; `stage-e/s1` a, b, c, e) |
| PL-03 | Resolved | `ffd1e34dbd` (#1106, stream S1; `stage-e/s1` d, f to j; the guest's after is a fix-pending-image row on #1106: the coordinator proves it at the first image built after the merge) |
| PL-04 | Deferred | #346: settled by the next base merge (`f2379f83b7`); the guest's state recorded (`guest-cycle-2/c2-debugshell.txt`); the unit joins the root-surfaces list below |
| PL-05 | Deferred | #344: fixed on the M7 line by `6101242e14`, which reaches `next` with M7's integration (the window: `guest-cycle-2/c3*`) |
| PL-06 | Deferred | #585: the line below |
| PL-07 | Deferred | #585: the line below |
| PL-08 | Deferred | #346: a hardening policy the coordinator posts (the pin is #997's) |
| PL-09 | Deferred | #585: the line below |
| PL-10 | Deferred | #740: the second site named (issuecomment-6396488186) |
| PL-11 | Resolved | #669 (recorded as a design under the 10:13 ruling; its four paths join the root-surfaces list below) |
| PL-12 | Resolved | #669 (recorded: a design for resize, volatile-log and debug; the reset and restore markers settled by the next base merge, `a98a3066f5`) |
| PL-13 | Resolved | #669 (recorded: carried, off by option) |
| PL-14 | Resolved | #669 (recorded: carried by placement, D-WORKFLOW-185) |
| PL-15 | Resolved | #669 (recorded: settled by the next base merge; the busybox pin #997's) |
| PL-16 | Deferred | #1104 (the coordinator's Backlog; the design sentence in `02` § The upstream delta) |
| PL-17 | Deferred | #1104 (as PL-16) |
| PL-18 | Deferred | #585: the line below |
| PL-19 | Resolved | #669 (recorded: a single-user handheld; joins the root-surfaces list below) |
| PL-20 | Deferred | #669: the coordinator's edit of `generic-x64-vm-testing.md` at acceptance |
| PL-21 | Deferred | #585: the line below |
| PL-22 | Deferred | #585: the line below |
| PL-23 | Deferred | #585: the line below |
| PL-24 | Deferred | #585: the line below |
| PL-25 | Deferred | #585: the line below |
| PL-26 | Deferred | #585: the line below |
| PL-27 | Deferred | #585: the line below |
| PL-28 | Resolved | `9145b90fac` (#1107, stream S3; `stage-e/s3`) |

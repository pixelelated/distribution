# Mini Retro: M6.P2 T22, the OS's system services and platform quirks (#669)

**Completed:** 2026-10-25
**Scope of this retro:** T22 from dispatch (`4a48d388c4`, 09:05 UTC) to the end of stage E (`5eb41ebccb`). That covers:
- stage A's runs and stage B's reads;
- two guest windows granted on #669;
- stage C's two seats;
- stage D's punch list and rulings;
- stage E's streams S1 and S3 (S2 and S4 were struck).

The audit is `docs/audits/2026_10_25-epic-m6-os-system-services/`. Its Phase 3 retrospective (`03`) is about the *area*; this one is about the *slice*.

**Branch:** `feature/m6-os-system-services-669`, 16 non-merge commits since dispatch. Two files outside `docs/` changed, both at stage E: `scripts/init` (+138 / -28) and `095-cloud-ssh` (+9 / -4).

**Delta:**
- **422 paths** read, each with a reachability row and a coverage row.
- **29 units**, each with its identity, writable input, guard and what pulls it in.
- **46 items from the two seats**, every one graded against its lines.
- **28 punch items**, all with outcomes. The audit issue #1103 reads 28 of 28.
- **Three bugs** (#1105, #1106, #1107) fixed with host cases (`run-all.sh`: 8 of 8). #1106 holds two fix-pending-image criteria.
- **Two guest windows**, 3 and 9 minutes, both disks retired with their records kept.

## The two questions the brief asks the retro to answer

**What the slice did to time to play:** nothing measurable.
- **S1** changes `scripts/init` only on the update path. `check_update` returns at once when nothing is staged (`:876-879` at `8ebaf8daad`, `:967-970` after the fix; that test is unchanged), so an ordinary boot runs no new code.
- **S3** changes a GENERIC_X64 quirk: four shell tests during autostart, on the VM only.
- **No unit, launch script or interface file** changed.

**What T29 inherits:**
- **The run-time selection lines:**
  - `quirks/package.mk:16-18` copies every platform into every image with a platform of its own;
  - `/usr/bin/autostart:16-28` selects by `HW_DEVICE` and `:31-43` by `QUIRK_DEVICE` (set at `002-autostart:8-12`);
  - `sleep.sh:44,84` selects by `HW_DEVICE`, and `userconfig-setup:19-27` copies `config/` by both;
  - `quirks/devices/` has no `config/` today (G-35).
- **The boot order, proven on the guest:** platform quirks, device quirks, `common/*`, `/usr/lib/autostart/${HW_DEVICE}`, then `/storage/.config/autostart/*`, all as root.
- **The *runs on* column** of `02` § The reachability table. T29 should know that the VM's `QUIRK_DEVICE` is `QEMU Standard PC (Q35 + ICH9, 2009)`, a `quirks/devices/` entry (T29's), which sets the VM's `DEVICE_*` flags.
- **What the next base merge settles:** `debug-shell.service` (`f2379f83b7`), the reset and restore markers (`a98a3066f5`), busybox 1.38.0 over https, and the two collisions (#1104).

## What worked well

- **The guest decided what reading could not, three times, and once against the reading.**
  - PL-01 read as "btrfs mounts without `nosuid`"; the guest showed udevil refusing it outright.
  - PL-05 read as six readers per device; the guest showed one each. That sent me to diff the image's `input_sense` against the tree, which found the M7 line's `6101242e14`.
  - PL-03 read as "`/storage` gone"; the guest showed it gone, with every service on it failing.

  Each verdict followed the record, and the record is kept (`guest-cycle-2/`).
- **Every seat item re-read at its lines before grading.** It caught two of my errors that the seats had named (the tty1 "only" claim, the `EnvironmentFile` sentence). It also caught one the seats' grading had carried: I had called an upstream comment the fork's.
- **The fixture under the shell that really runs the code.** S1's case runs `init`'s own functions under the initramfs busybox. That exposed two things the host's tools hid: the host's `md5sum` lacks `-s`, and the initramfs ash has no `command` builtin. The fix is written to both facts.
- **Generated tables.** `t22-reach.py` asserts its own counts (422, 8, 213) and `t22-packet.py` scans before sending, so no table or packet was typed.

## What was harder than expected

- **Fixture slips in S1, six of them before the case was right:**
  - `set -u` leaking into `init`;
  - a returning `reboot` stub;
  - the host `md5sum`;
  - the missing `command` builtin;
  - a path rewrite that missed `/storage;`;
  - a missing `calls` file.

  Each was found by reading the fixture's own output before trusting a verdict, and none produced a false verdict. The `command` one is worth naming: the stub's exit 127 made the unfixed file print `Update complete` over an unwritten kernel. That is the very bug, produced by the fixture rather than by a write.
- **Times written ahead of the clock, three times** (two in `04`, one in `00`). Each was corrected, and the rule kept since is: write a time only after `date -u` has printed it.
- **A criterion I wrote and then had to meet.** #1106's third checkbox asked the fixture for all six rejection paths, and the first passing case covered one. Cases f to j were added before ticking it.
- **The brief's unit loop masked its own figure:** its credential `sed` matches `User=`. It was found at stage A and recorded as the brief's erratum.

## What we discovered

- **The OS update path is the slice's real risk, and it is upstream's.** A failed write reported success over a torn kernel or SYSTEM, and a rejected update booted without `/storage`. The fixes are contained to `init`, and both rows stand at `651150fc88`.
- **The guest is the M7 candidate, not the read tree.** `input_sense` differs. The second window's PL-05 reading would have been wrong without the diff. Astra had named this exact limit ("whether the guest exactly represents the read tree").
- **There are four unauthenticated root paths for a device in hand,** and the read tree adds a fifth on every boot (`debug-shell`). They are listed for #346 in `05`.

## Adjustments (proposals for the coordinator)

1. **A window plan should name each guest proof's image-versus-tree check.** T1's `02` had § Image versus tree; this slice did not, until PL-05 forced it. A line in the next brief's guest section: *before trusting a guest's verdict on a file, compare the installed file with the read tree's*.
2. **An initramfs fixture runs under the initramfs busybox.** S1's driver and README say how. A line in `generic-x64-vm-testing.md`'s § What the guest's busybox lacks: the initramfs busybox's ash has no `command` builtin and no `--install`. This lane edits no rule, so it is offered.
3. **No changes to T29's order;** its brief inherits the list above.

## Scoped audit (Step 2.5)

- **AC conformance:** PARTIAL until the hand-back. Every punch item has its outcome, and #1103 reads 28 of 28. #669's own criteria are the hand-back's, and #1106's two guest criteria are fix-pending-image rows.
- **Cornerstone spot-check:** PASS.
  - No file under `packages/`, `projects/` or `tools/` changed at stages A to D (`git diff --stat 4a48d388c4 <stage-D tip>`: empty), and only the two stream files at stage E.
  - Four `invoke` calls (two seats, a probe and a refutation each); every other `tools/council/run` call carried `COUNCIL_ENV_FILE=/nonexistent`.
  - No fetch: the runtime came from `npm install --offline`.
  - No handheld; guests only inside the two granted windows.
  - The packet scanned clean three ways; one file name was reworded for the commit scanner.
- **Interaction-defect scan:** PASS for what the guest could reach (udev x udevil x samba; the autostart layers; the update path x `/storage`). The interaction of the H700 and SM8550 platform quirks with their device quirks is T29's and was not run.
- **Futro prediction verification:** the kickoff's facts all reproduced at stage A. It foresaw none of the update path's defects, the debug shell, or the M7 line's `input_sense` fix.
- **Housekeeping:** PASS. `run-all.sh` 8 of 8; both lints PASS; `box-check` 0 fail on #1103 and the three bugs. Both guest disks are retired with records in `00`.
- **Harness self-coverage, and did each fix's positive exercise the job it could break?** (the stream brief's step-5 question):
  - **S1, yes.** Case c runs a successful update end to end and shows both new files in place with `Update complete`, so the success path the fix could break is checked beside the failures. Case e checks the in-place path that `/flash` without room still takes. The guest's *after* waits for an image.
  - **S3, yes.** A valid port is accepted (with and without a newline), and the two-boot case runs the whole quirk, so the command-writing job is exercised, not only the parser.
- **Documentation freshness:** PARTIAL. Neither recipe documents the selection mechanisms yet (PL-18, on #585). PL-20's rule line is the coordinator's.

## Practice adjustments

- The scoped audit's step 5 question ("did the positive exercise the job the fix could break?") worked as written. Its useful sharpening was T13's: run the success path beside the failure cases. That is case c here.

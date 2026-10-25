# Mini Retro: M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

**Completed:** 2026-10-25
**Scope of this retro:** the T11 lane at Independent depth. It covers:
- stages A to D, the read of the 58 paths at `8ebaf8daad`, with one GPT-6 Astra seat;
- the five bugs (#1086 to #1090) and the audit issue #1091;
- stage E, the coordinator's four streams;
- the close-out to the hand-back.

Not retro'd here: the coordinator's acceptance, the three Backlogs it filed (#1083, #1084, #1085), and T10's fix of #1086.

**Commits:** `reviewed-at` `2103f0271d` (the dispatch tip); `fixed-at` `0c32b2bac6` (the last of seven fix commits).

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** No fix sits on the interface-to-first-frame or the exit-to-next-frame path:
- the boot scripts run at image build;
- the launcher starts a QA guest;
- the udev rule fires on one USB dongle;
- `dtb_overlay` runs when a player changes an overlay.

F-01's firmware payload and F-02's kernel size touch the guest's boot and image size, not the launch path, and neither was changed here (#1083, #1084). No guest ran for this lane.

## What T27, T28 and T25 inherit

- **T27 (#674), the configuration shape.** A device's kernel configuration is stated in three parts:
  - the nearest candidate with `diff` counts;
  - the fork's own lines since the adding commit;
  - the built-versus-committed gap. The gap is stated from the recipe first; a built `.config` from an existing build root is corroboration, with its provenance written (the root's head, the transfer argument, each copy's sha256).

  T11's gap was 18 changed values, 97 set options gone and 137 new. The fork's 10 settings survived. One proof had read the committed file, and its claim held.
- **T28 (#675), the boot-file table.** Who runs each of `install`, `mkimage`, `release` and `rkhelper`; the branch per shipped device; the upstream status.
  - `install` now refuses an unknown loader, and both `install` and `release` exit on a failure, which stops the image step.
  - `scripts/mkimage`'s own masking is #827.
  - `mkimage_abl` copies `rocknix_abl` correctly without `-s` (mtools 4.0.49 fixture).
  - Upstream's `651150fc88` rewrites the SM boot chain.
- **T25 (#672), the merge seam.** Upstream's version case never had GENERIC_X64 and has no default, and the override sources no generic recipe. So a merge that takes upstream's case leaves GENERIC_X64 with no `PKG_VERSION` (PL-09, in the merge notes). The bfq rule's partition match comes with the same merge.
- **The launcher design** (accepted at stage B): the launcher stays in the device directory beside its profile, `tools/vm-pair` is the one operational caller through one `VM_TOOL` line, and no basename goes on `PATH`.

## What worked well

- **The recipe statement first, the build root second.** The coordinator's 07:10 ruling kept the read-only slice honest. The gap is what the recipe implies, and the M7 root's `.config` showed it with numbers, not instead of it.
- **The seat earned its place.** It confirmed the main findings and caught three of my statements: the ancestry claim, F-09's consequence, and the recipe's "four values". It raised four real defects (F-11 to F-14). Re-reading every decisive item refuted two of its claims, G-8 and G-26, the second by a fixture T5's earlier test could not have shown.
- **Tests first, kept on the branch, with controls.** Each stream's driver judged both sides. A normal-path control ran on both sides, so a fail-closed fix could not pass by breaking the normal path. `run-all.sh` repeats all 47 rows in one command.
- **The interpreter and the paths matched to the device.** `dtb_overlay` ran under bash (the image's `/bin/sh`) with the real `/flash` paths in `bwrap`, because rewriting a path would have broken its `cut`.

## What was harder than expected

- **My own slips, each caught before it landed:**
  - typed times (an ad-hoc read window, a fixture's end time, the refutation's start);
  - three line ranges in `02`;
  - the GPU drivers called ours when they are the Generic conf's;
  - a driver that judged `release` by the sourced status rather than by whether the step carried on;
  - PL-04's owner at first named T27.
- **Drivers that had to be corrected against the code's real behaviour:**
  - `release-case`: `.` returns `cp`'s status, and `scripts/image` ignores it;
  - `dtb-overlay-case`: an empty and a missing setting read alike.
- **What the host could not give,** each named rather than worked around:
  - no `umockdev` and no USB block device, so #1087's block-child firing stays open;
  - `last-good-scripts-test` compiles host helpers, which the brief rules out, so its launcher section did not run;
  - the runner's `node_modules` was absent and a fetch was forbidden; a local copy from my own idle worktree served.
- **Two acceptance checkboxes asked for what the host cannot do,** and two trace claims were wrong in detail. Each was reworded or narrowed on its bug in the same action: #1090's "returns 0", #1087's constructed sysfs tree, and #1088's `-o`.

## What we discovered

- **The QA guest installs all of linux-firmware**: 2.88 GB staged, because it has no `config/kernel-firmware.dat`. Its kernel embeds 1,254 firmware files for real hardware.
- **The committed configuration has been 6.15.6 since the day it was added,** while the in-tree Generic conf was already 7.1.2. The build silently turns it into a different 7.1.2 configuration, voluntary preemption to full among the changes.
- **`mcopy <dir> ::` copies a directory without `-s`** when the directory is named on the command line (mtools 4.0.49). T5's fixture had used a file there.
- **The inventory's reach is coarser than the build** for files read through `find_file_path` or from `${DEVICE}` directories: the opposite direction to #1049 and #1056 (#1086).

## Adjustments, Instruction-Recommendations mode

These are proposals for the coordinator.

1. **`generic-x64-vm-testing.md`:** the guest's kernel configuration is the built one. Read `.image/.config`, or `/proc/config.gz` after `modprobe configs`, never the committed file, until #1084 regenerates it.
2. **`device-builds.md` or `packaging-and-patches.md`:** a device with no `config/kernel-firmware.dat` installs its arch's fallback, which on x86_64 is everything.
3. **For stream drivers:** judge a sourced script by whether its caller carries on, not by its return status. Run a device script under the image's interpreter and real paths. Give each fail-closed fix a normal-path control on both sides.
4. **For a seeded worktree:** name the council runner's dependencies in the pointer, or add a keyless `tools/council/run test` to stage A's first commands (the friction line of 07:09).

## Scoped audit (the close-out's own checks)

- **The lint:** `PASS` in the pre-issue and resolution phases, and with `--issue 1091`.
- **The tables:** 58 coverage rows; the brief's § 2 block unchanged at the tip; `git diff --stat 8ebaf8daad 2103f0271d -- <the 58>` empty; `git diff --stat 2103f0271d 499628a049 -- packages projects tools` empty (stages A to D); stage E's diff exactly the brief's six files.
- **The seat:** probe and refutation PASS, served `openai/gpt-6-astra` by OpenAI, 36 items graded; the packet scanned 0 hits.
- **#1091:** 14 items, each at an outcome (6 Resolved, 8 Deferred to issues with their fix commits named). `box-check` 0 fail on #1086 to #1091.
- **Stage E:** `run-all.sh` 47 rows, 0 unexpected. No guest started by this lane (`pgrep` read 0 before T13's guest at 07:51:38, then 1, unchanged by any case).

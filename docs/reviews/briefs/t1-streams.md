# T1's stream briefs: the OS scripts' punch list, #701, in seven streams (#648)

Written by the coordinator at T1's stage-D pause (2026-10-23; plan § 6b
stage E; D-WORKFLOW-189: a brief is planning; the shape is D-WORKFLOW-056's:
the verdict's lines, the fix as a specification, the test first, the
`Already written:` line, the files owned, the commit shape, the branch).
One section below is one stream brief. The lane that runs them is the T1
lane, alone, in its own worktree, on its own branch, in the order given;
the per-item specification is the `bug` issue the lane filed (its *The
fix* line, its *Already written* line, its two criteria), and this document
does not restate it. Where this document and an issue differ, the issue's
trace is the fact and this document's grouping is the plan; say so on #648
and go on.

**What every stream shares.**

- **Branch and worktree:** `feature/m6-os-launch-control-state-648` in
  `/workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648`,
  from its tip at the pause (`9bacbc2c2a`) after merging the coordinator
  tip that carries this document. One commit series per stream, headed by
  a commit whose subject names the stream (`rocknix: stream S1, the
  netplay host and the eval`) and whose body lists the items it will
  take; then one commit per item, or one per coherent group of items that
  one change fixes (say which items in the body).
- **The files owned** are listed per stream. A fix that genuinely needs a
  file outside its stream's list waits for that file's stream (reorder
  within the series) or, when the file belongs to no stream (another slice's
  path), stays open with the reason and a lead on #648 for that slice. Two
  streams never edit one file in interleaved commits: finish a stream
  before the next starts.
- **The test first, and the failure seen.** Every `bug` issue's second
  criterion asks that the check was run against the unfixed script and
  failed. So for each item: write or extend the check (a case in the
  harness named per stream, or the guest recipe the issue gives), run it
  on the unfixed tree and record the failing line, make the fix, run it
  again and record the passing line; the fix's commit body names both runs
  with their commands. A check that cannot run before the host returns
  (§ The guest, below) is written and recorded as pending in
  `00-running-log.md`, and its item stays open until it has run.
- **`Already written:` in every bug fix's commit body**, copied from the
  issue and corrected if the fix's shape changed it (D-WORKFLOW-050,
  `upgrade-and-install.md`); a renovation item (no `bug` issue) that
  removes or renames anything writes the same line in its commit.
- **Commit shape:** subject `<script or package>: <what changed>` under 72
  characters, no space before the colon (`setsettings.sh: quote the netplay
  host and refuse shell characters`, `rocknix: stream S4, the destructive
  scripts`); a blank line; a body with the item ids, `Refs #648, #7NN` (no
  closing keyword while any criterion is open), the two test runs, the
  `Already written:` line; the trailer `Co-Authored-By: Claude Opus 5.5
  <noreply@anthropic.com>`. Never `--no-verify`; never a bare `git stash`;
  never edit a shell script while a run of it is in flight.
- **Under the image's tools.** Every script here runs under the image's
  busybox and dash, not the host's (`upgrade-and-install.md` § Verify on a
  device; blindspot 34): the harness cases run with
  `QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system`
  as brief § 5 says, and a `#!/bin/sh` script is proven under dash. An
  external command a fix adds is one the image has (`command -v` in the
  guest, or the build root's `image/system/usr/bin`).
- **The words a player reads** (a console line, a log line the interface
  shows, a `>>> why` line) follow `es-player-text.md`; a player-visible
  change (a default that changes, a behaviour a player sees) is written
  into the running change log the day it lands (`change-log.md`), and a
  menu row that moves updates `docs/es-menu-map.md` (none expected here).
- **`tools/pkgcheck rocknix`** after any `package.mk` edit (stream S5), its
  output quoted.
- **The guest.** The host is handed to the M7 lane until its `resource
  return` line in `/tmp/m7-m6-host-coordination-20261023.txt`, which the
  coordinator relays on #648. Until then no guest, no compile. The streams
  are written so that every host-side case (the harness tools under
  `QA_SYSTEM_ROOT`, the busybox shims) runs now and every guest proof is
  queued; when the line comes, bring the guest up from the kept
  `t1.qcow2` (`generic-x64-vm run --headless --daemonize` with the lane's
  instance paths, SSH 10032, VNC 19) and run the queue in stream order.
  Bring it down when the queue is empty (`tools/vm-stop`); the host is
  shared.
- **Phase 7 outcomes** are written into `05-punch-list.md`'s index and the
  audit issue #701 as each item ends: `resolved` with the commit, `deferred`
  to the issue or decision named below, `withdrawn` with the artifact that
  refutes it. The three deferral classes are decided here, not per item:
  1. **Fixed upstream already** (the lane's finding; the stream is the
     merge, not a fork patch): F-21 #712, F-45 #745 and F-49 #747 are
     `deferred:#563` (M7.P5, the adoption of ROCKNIX's current `next`,
     which carries `25903bb59c`, `4e3972d037` and `6aa745572b`). Each
     issue gets one comment naming the upstream commit that resolves it
     and stays open until `next` takes it; the coordinator closes them at
     that merge. Do not cherry-pick the three: `25903bb59c` rewrites
     `get_setting` and the fork's settings lock (D-INFRA-012, D-SYS-011/012)
     sits in the same function; that reconciliation is the adoption's,
     not this slice's.
  2. **A maintainer's call:** F-68 #725 is `deferred:D-SYS-014` (the
     register's open table; the coordinator put it to the maintainer on
     #346). The issue stays open; the stream writes nothing for it unless a
     change is design-neutral (the file's mode, say), and then only that.
  3. **Items to verify** (F-18, F-27, A-10, F-08's timing) are not fixes:
     each is a guest run that confirms or withdraws a finding, queued for
     the guest, with its outcome `withdrawn` (the artifact that refutes it)
     or a new `bug` issue filed then and its fix taken into the stream
     that owns the file.
- **The M7 candidate's hunks.** The candidate `069fc2704421` changes
  `runemu.sh` in two places against `next`'s `8ebaf8daad`: 61 lines
  inserted after line 4 (a lifecycle-admission block, `ra_lifecycle_*`
  functions) and one line at 335 (the proxy's `exec 199>&-` before
  `python3 ... ra_proxy.py`). Streams S1 and S3 edit `runemu.sh` elsewhere
  (S1 at 327, 349, 355 and 500; S3 at 27 to 65, 245 to 254, 309, 378 to
  385, 432 to 467, 537 to 561). Do not touch lines 1 to 10 or 331 to 340,
  so the coordinator's merge at the candidate's landing is clean; if a fix
  must, say so on #648 first. Announced on #642.
- **Across the seam with T2** (#649, the interface's launch path, dispatched
  beside this lane): the netplay host the interface stores
  (`GuiNetPlaySettings`), the ip and nick it `shellQuote`s under `#if
  ROCKNIX` before the shell unquotes them for `runemu.sh`, and the `-P`,
  `--core=`, `--emulator=` tokens both sides parse. S1's fix is on this
  side only (validate and quote what `setsettings.sh` reads from
  `system.cfg`); it does not depend on an interface change, and the
  coordinator carries the seam to T2's stream briefs. A fix here that would
  change what the interface must send (an argument's shape) is a lead on
  #648, not a change.
- **Unreached code.** A script or function no caller reaches (Q6) is
  removed only when it is fork-own; an unreached script that upstream
  ROCKNIX still carries (`git log --oneline c445081a59..upstream/next --
  <path>` non-empty, or the file present in `upstream/next`) stays, with
  its row in `04-analysis.md` § Q6 and a line on #585 (the upstream
  contribution queue: the removal is upstream's to take), because a file
  the fork deletes and upstream keeps is a conflict at every sync. Every
  removal carries `Already written:` and names what the unit guarded,
  stamped and exposed (brief § 4, Q6).

## S1. The netplay host and the eval (High first)

- **Items:** PL-001 F-14 #702 (High), PL-007 F-15 #708 (Medium).
- **Files owned:** `sources/scripts/setsettings.sh` lines 595 to 690 (the
  netplay block: `global.netplay.host` at 620, the `add_setting` calls at
  595, 621, 647, 671 to 675, 683, 688) and `sources/scripts/runemu.sh`
  lines 320 to 360 and 495 to 505 (the `eval` sites at 327, 349, 355 and
  500), both under `projects/ROCKNIX/packages/rocknix/`. Nothing else in
  either file (S2 owns the rest of `setsettings.sh`, S3 the rest of
  `runemu.sh`).
- **The fix as a specification:** #702's: accept a hostname or an IP
  address only (`[A-Za-z0-9.:-]`), refuse anything else with a log line
  that names the refused value masked, and pass the host to RetroArch as
  one quoted argument so `runemu.sh`'s `eval` sees a word, not a command;
  #708's: the two malformed `add_setting` calls corrected and the TGB Dual
  client's core options kept. Read the audit's § 3.6.5 sibling table
  (`03-retrospective.md`) before the commit: every site of the shape
  "a stored value reaches `eval`" is either fixed here or named as not
  this stream's with the reason.
- **The test first:** a case in `tools/last-good-scripts-test` (read its
  header for how cases are written; the image's busybox and dash through
  `QA_SYSTEM_ROOT`) that runs `setsettings.sh`'s netplay block with
  `global.netplay.host='127.0.0.1;touch /tmp/t1-f14-marker;'` and asserts
  the written RetroArch config holds one quoted host and no marker is
  created when the resulting `EXTRAOPTS` is `eval`ed the way `runemu.sh`
  does it; the guest run #702 names (the stub launch through the tree's
  `runemu.sh` under `/storage`) queued for the guest. The failing run on
  the unfixed tree recorded first.
- **Already written:** #702's line (old values in `system.cfg` and in
  settings archives are validated by the new reader, refused, never run).
- **Commits:** the stream head, then one per item.

## S2. `setsettings.sh`: the per-core settings writer (Mediums)

- **Items, in this order:** PL-004 F-09 #705, PL-006 F-11 #707, PL-005
  F-10 #706, PL-032 F-10b #731, PL-008 F-16 #709, PL-009 F-17 #710, PL-010
  F-19 #711, PL-033 F-12 #732, PL-034 F-13 #733, PL-080 A-06 #760; then
  the two verifications PL-035 F-18 and PL-042 F-27 (guest).
- **Files owned:** `projects/ROCKNIX/packages/rocknix/sources/scripts/setsettings.sh`
  whole, less S1's lines.
- **The fixes:** each issue's *The fix* line. The shared shapes: the
  `add_setting` condition (#705, #707: the backgrounded test and the
  check-then-create of the staged `sed` file, which the 24-writer loop the
  issue names must survive), the substring `match()` (#706, #731: a
  word-boundary test; `neogeo` stays apart from `neogeocd` and
  `pcsx_rearmed` from the 32-bit list), the one-line truncations (#709,
  #710: the options file rewritten whole, never cut), the unquoted `sed`
  programs (#711: values escaped or passed through a file, and the overlay
  settings written whether or not a bezel applied), `set_config_save`'s
  argument order (#732), the sourced autoconfig (#733: read the values, do
  not `source` a file as root) and the two-pad name join (#760).
- **The test first:** `tools/settings-modes-test` already exercises the
  writers' modes; extend `tools/last-good-scripts-test` with one case per
  item that runs the function on a fixture `system.cfg` and asserts the
  written lines (the issue's criterion gives the exact assertion); the
  F-11 loop (200 iterations, 24 writers) as the issue names it, under
  the image's busybox; the guest runs the issues name (`setsettings.sh
  neogeo <rom> fbneo` with `rewind=1`, the Gambatte and MAME launches)
  queued for the guest.
- **Already written:** per issue; #709 and #710 read the options files a
  previous launch already cut to one line (the fix must rebuild them from
  the core's defaults or leave them as they are and say which).
- **The two verifications:** F-18 (`setsettings.sh:1065`) and F-27 (the
  shader block, 778 to 790) run on the guest when it returns; `withdrawn`
  with the artifact, or a `bug` issue filed and fixed in this stream.

## S3. `runemu.sh` and the launch helpers (the rest of the launch path)

- **Items, in this order:** PL-003 F-01 #704 (Medium), PL-025 F-02 #726,
  PL-026 F-03 #727, PL-027 F-04 #728, PL-040 F-25 #736, PL-029 F-06 #729,
  PL-030 F-07 #730, PL-076 G-05 #757, PL-041 F-26 #737, PL-036 F-20 #734,
  PL-038 F-23 #735, PL-028 F-05 (renovation, Q6), PL-031 F-08 (renovation,
  Q7; its timing half is a guest measurement), PL-082 A-10 (verify,
  `vertical-check`, guest).
- **Files owned:** `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh`
  less S1's lines and less lines 1 to 10 and 331 to 340 (the M7 hunks);
  `sources/scripts/run`; `sources/scripts/vertical-check`;
  `profile.d/099-freqfunctions`; `profile.d/100-gamecontroller-functions`;
  `profile.d/001-functions` line 664 only (the sway helper, #735; S4 owns
  the rest of that file).
- **The fixes:** per issue. The governor and thread shapes (#704, #726,
  #736: a setting is a value to look up, never a command to run; the
  `online` count read from one source; `onlinethreads` guarded where it
  does not exist), the exit-time restores (#727: run them in the
  foreground or sequence them before the next launch can start; the race
  was never measured, so the test is the ordering, not a timing), the fan
  profile (#728), the quoting (#729, #730, #757), the controller functions
  (#737), the two helpers printing into their callers (#734, #735: output
  to stderr or to a variable, never to stdout the caller captures).
- **The test first:** `tools/last-good-scripts-test` cases for every
  function that can run outside a launch (the governor lookup, the thread
  count, the `rm` with a spaced name, the controller db builder with a pad
  that has no hotkey); `tools/emulator-exit-test --vm` and
  `tools/time-to-play --vm` on the guest after the stream, their lines
  beside the stage-B baselines (Q5: the stream must not cost a launch
  anything it cannot name); #727's ordering proven on the guest with the
  issue's recipe.
- **Already written:** per issue; #728 reads the device setting a game
  left behind (the fix restores it on the next boot or launch, and says
  which).
- **Renovation items:** F-05 (dead branches at 33 to 254) and F-08 (the
  61-to-84 block's clarity): a row and a reading, and a change only where
  the Q6 rule above allows it.

## S4. The settings library (`001-functions`)

- **Items, in this order:** PL-075 G-03 #756, PL-079 A-02 #759, PL-078
  A-01 #758, PL-037 F-22 (renovation, Q7, the lock), PL-039 F-24
  (renovation, Q5, logging); PL-011 F-21 #712 is `deferred:#563` (above).
- **Files owned:** `projects/ROCKNIX/packages/rocknix/profile.d/001-functions`
  (less line 664, S3's), and the one caller #758 names outside it
  (`sources/scripts/rocknix-settings`, lines 34 and 61 to 74, which S5
  otherwise owns: take them here).
- **The fixes:** per issue, **written small**: `get_setting`'s prefix
  boundary (#756), its quoting (#759) and the literal `default` (#758) are
  a few lines each, and upstream's `25903bb59c` rewrites the same function
  with a `flock` where the fork has its own lock. So: no restructuring of
  `get_setting`/`set_setting` in this stream; the three fixes land as
  minimal diffs with a comment naming the upstream commit, and the merge
  note in the lane pointer says the adoption (#563) reconciles them. F-22
  and F-24 are rows unless the change is a comment or a log line's
  shape.
- **The test first:** `tools/last-good-scripts-test` already covers
  `set_setting` and `write_stamp`; add the three cases the issues give
  (a key that prefixes another; a value with spaces, a `*` and `-n`; a
  value literally `default`), under the image's busybox; `tools/wait-lock-test`
  unchanged and passing.
- **Already written:** #758's (values of `default` already deleted from
  `system.cfg` are gone; the fix stops the deletion, it cannot restore
  them, say so); #759's and #756's read nothing.

## S5. The updater, the sysconfig units and the defaults

- **Items, in this order:** PL-012 G-01 #713, PL-014 F-32 #715, PL-015
  F-33 #716, PL-020 F-44 #721, PL-043 F-28 #738, PL-046 F-34 #740, PL-047
  F-35 #741, PL-044 F-30 #739, PL-023 F-63 #724, PL-048 G-02 (renovation),
  PL-073 F-65 (renovation; its lines are S4's, the row is here), PL-070
  F-62 (renovation), PL-056 F-46 (renovation, Q6); PL-055 F-45 #745 is
  `deferred:#563`.
- **Files owned:** `projects/ROCKNIX/packages/rocknix/sources/post-update`;
  `autostart/003-upgrade`; `system.d/save-sysconfig.service`;
  `config/system/configs/system.cfg`; `package.mk` (lines 15 and 29, and
  whatever #724's mode fix needs).
- **The fixes:** per issue. The updater's contract: a failed `post-update`
  keeps the hint so it runs again (#713), its writers go through the
  settings lock and the torn-file guard (#715: `set_setting`, never a raw
  `sed` on `system.cfg`), the `last_` copies survive a second update
  (#716), the DPMS choice is read before it is written (#721), the
  update's log is kept (#738), `cd` is checked (#741), the engineering
  blocks do not overwrite an owner's `authorized_keys` or Wi-Fi files
  (#740: a build-time default never replaces a player's file), the
  shutdown backup has a timeout (#739), `system.cfg` is not world-writable
  (#724: the recipe's mode, with `tools/pkgcheck rocknix`).
- **The test first:** `tools/melonds-upgrade-test --post-update <tree copy>
  --busybox $QA_SYSTEM_ROOT/usr/bin/busybox --output <scratch>` already
  runs `post-update`'s melonDS half; extend `tools/last-good-scripts-test`
  with a case per item that runs the block in a fixture `/storage` (a
  failed step, a second update, a DPMS value set, an `authorized_keys`
  present); the in-place `.update` path on the guest (the `-06` image
  booted from a second qcow2 under `$ROCKNIX_ARTIFACTS`, the `-07` tar in
  `/storage/.update`, the reboot over serial) queued for the guest as the
  end-to-end proof, with no backend and no pair (brief § 5's rehearsal
  answer).
- **Already written:** every item here reads a device's state: #716 the
  `last_` copies already lost (the fix cannot restore them; the next
  update starts the series again), #721 the DPMS value already reset (the
  fix stops the reset; a player's earlier choice is gone), #740 files
  already overwritten (gone; the fix stops it), #738 logs already
  overwritten. Each commit says so in those words.

## S6. The destructive and state scripts (High second)

- **Items, in this order:** PL-002 F-67 #703 (High), PL-016 F-39 #717,
  PL-017 F-40 #718, PL-052 G-04 #744, PL-018 F-42 #719, PL-019 F-43 #720,
  PL-050 F-37 #742, PL-051 F-38 #743, PL-013 F-29 #714, PL-049 F-36
  (renovation), PL-053 F-41 (renovation, Q6), PL-054 F-43b (renovation),
  PL-045 F-31 (renovation, the unit).
- **Files owned:** `projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl`,
  `installtointernal`, `automount`, `factoryreset`, `setrootpass`;
  `system.d/rocknix-automount.service`.
- **The fixes:** per issue. The shape they share is the guard that fails
  closed (`engineering-practices.md`): a write checked and read back
  before the next (#703: `abl_a` verified before `abl_b`, success only
  when both), a target refused when it holds the running system (#717),
  a copy's failure ending the script non-zero (#718), a process
  substitution checked (#744), a mount checked and reported (#719), the
  wrong device refused (#720), a reset that did nothing saying so (#742),
  a reset scoped to its subject (#743), a hash that failed to compute never
  written (#714).
- **The test first:** these scripts touch partitions and `/storage`, so
  every case runs against loop files and a fixture tree, never the host's
  devices: #703's two loop files (one read-only) with the partition paths
  made overridable (the fix adds the override; the test uses it), #717's
  and #718's fixture target under `$ROCKNIX_ARTIFACTS`, `automount`'s
  cases with fixture `/dev` listings; all under the image's busybox in
  `tools/last-good-scripts-test`; the guest runs the issues name queued
  for the guest. `installtointernal` and `updateabl` are never run for
  real on the guest or anywhere (the guest has no internal target and no
  ABL slots; #703's VM line says loop files stand in, and the Nova's
  write is an open item to test, `docs/releases/device-facts.md`).
- **Already written:** #703's (a device whose slots were written badly is
  not repaired; the skip check rewrites a slot that does not hash as the
  update), #743's (`/storage/.local/state` already emptied is gone), the
  rest per issue.

## S7. The control scripts and fragments

- **Items, in this order:** PL-021 F-57 #722 (Medium), PL-022 F-58 #723
  (Medium), PL-066 F-56 #750, PL-067 F-59 #751, PL-068 G-07 #752, PL-081
  A-07 #761, PL-069 F-60 #753, PL-063 F-53 #748, PL-064 F-54 #749, PL-058
  F-48 #746, PL-071 F-64 #754, PL-072 G-06 #755; the renovation rows
  PL-057 F-47 (credentials in evidence, Q2: a change only if a value is
  printed today, then the filter of D-INFRA-011), PL-060 F-50 (`usbgadget`
  under dash, Q2), PL-061 F-51, PL-062 F-52, PL-065 F-55 and PL-074 F-66
  (unreached scripts, Q6: the rule above), PL-077 F-69 (the `tz` list,
  Q1), PL-083 A-11a (the python interpreter lines), PL-084 A-11b
  (`tools/vocabulary-check`'s default `--scripts` set: a tool change,
  allowed, with the tool's own self-test run); PL-059 F-49 #747 is
  `deferred:#563`; PL-024 F-68 #725 is `deferred:D-SYS-014`.
- **Files owned:** `projects/ROCKNIX/packages/rocknix/sources/scripts/paneladj`,
  `volume`, `rocknix-memory-manager`, `rocknix-es-thebezelproject`,
  `wifictl`, `rocknix-evidence`, `rocknix-config`, `suspendmode`,
  `handle-hdmi-hotplug`, `usbgadget`, `rocknix-systems`,
  `rocknix-bluetooth-agent`, `rocknix-scraper`, the unreached scripts F-55
  names; `autostart/008-perfmode`, `050-audio`, `055-hdmi-check` and the
  fragment A-07 names; `system.d/rocknix-report-stats.service`;
  `config/system/configs/tz`; `tools/vocabulary-check` (for A-11b only).
- **The fixes:** per issue. Two to read twice: #723 (`008-perfmode` stops
  at its third line on x86_64: the fix must not change what the fragment
  does on aarch64, where `099-freqfunctions` exists; prove both shapes,
  the guest for x86_64 and the harness with the aarch64 functions sourced
  for the other) and #722 (`paneladj` clamping every value: the fix reads
  the panel's range from the kernel, and the guest has no panel, so the
  proof is the harness with a fixture sysfs, the shape
  `tools/rocknix-info-test` uses; the stray file is the simpler half).
- **The test first:** `tools/usb-gadget-test --output <scratch>` for
  `usbgadget` (F-50's dash conformance checked by running the script
  under `$QA_SYSTEM_ROOT`'s `sh`); `tools/rocknix-info-test`'s fixture
  shape reused for `paneladj` and `volume`; `tools/last-good-scripts-test`
  cases for `rocknix-config`'s `sed` (a `/`, an `&`, a prefixing key),
  `wifictl`'s verbs with no device, `suspendmode`'s compare, the swap
  resize with a failed `swapoff`, the bezel list's names; the guest for
  the fragments (`050-audio`, `055-hdmi-check`, `008-perfmode` on x86_64)
  after the return.
- **Already written:** #722's (panel values already clamped in the stored
  setting: the fix re-reads the range; a stored value at the maximum is
  left, say so), #751's (the 1080p mode written to the wrong file on
  devices: the fix writes the right one and removes the wrong one if it
  is the fix's own shape), the rest per issue.

## After the seven streams: stage F and the hand-back

- Run the queued guest proofs in stream order once the host returns;
  then the stage-B checks again at the branch tip and record them beside
  the stage-B lines: `tools/pkgcheck rocknix`, `QA_SYSTEM_ROOT=...
  tools/last-good-scripts-test`, `tools/settings-modes-test`,
  `tools/wait-lock-test`, `tools/usb-gadget-test`, `tools/rocknix-info-test`,
  `tools/melonds-upgrade-test`, `tools/vocabulary-check`,
  `tools/emulator-exit-test --vm`, `tools/time-to-play --vm` (Q5: the two
  numbers after the streams beside the numbers before them; a stream that
  moved a number names why).
- `tools/lint-audit-artifacts <folder>` prints `PASS`; every item of #701
  at an outcome; `tools/box-check --issue 701` and on every `bug` issue
  still open (the deferred ones carry their deferral in a comment, their
  checkboxes untouched).
- The retro (stage G), then the hand-back (brief § 10): `reviewed-at:`
  and `fixed-at:` into #648, the hand-back comment, idle. The coordinator
  accepts, closes #648 and the resolved `bug` issues (each with its fix
  commit named, `Already written:` present), writes the hashes into
  `slices.json`, and merges in its turn: P0, P1, then this branch, after
  the M7 candidate (the `runemu.sh` hunks reconciled by the coordinator).

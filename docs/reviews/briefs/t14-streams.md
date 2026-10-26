# T14's remediation streams (#661, audit issue #1006)

Written by the coordinator on 2026-10-24 at T14's stage-D pause
(D-WORKFLOW-189), in the shape of `t12-streams.md`: twelve streams, each with
the files it owns, the test first, its `Already written:` line, its
acceptance and its commits; then the dispositions that are not streams, which
the lane writes into the Phase 7 table; then the order and the hand-back. The
lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-state-tests-661`,
branch `feature/m6-tooling-state-tests-661`, stage-D tip `7aa8eac253`).
**Review depth per stream: Local** (plan § 6c). Every tool in this slice *is*
a test, so the rule the slice was read under applies to the fix of each:
**a stream lands with the new case that fails on the unfixed tool and passes
on the fixed one, or it is not a stream** -- and the positive is produced by
running the case against an export of the stage-D tip, or a copy of the tool
with its other cases cut, never by reasoning (`engineering-practices.md`
§ Guards must fail closed; blindspot 39). The positives are quoted in `02`
§ The streams' positives beside the fixed runs.

**Where the tests run.** On the host, in the lane's worktree, with `TMPDIR`
under `/workspace/tmp/m6-t14/` and the cases' own scratch under
`.qa-scratch/t14/` (gitignored); the real-rclone four against the local
backends or their own isolated filesystems, after their binding is read
(D-QA-058); the two writer tests with a busybox whose provenance is recorded
(S8). **No guest cycle is needed in stage E**: every item answered *Can this
be done on the VM?* with *No: host-side, a test run in a scratch root shows
it*. The M7 lane holds the host under a window bounded 00:30 UTC 2026-10-25;
nothing here needs it. **Never run here:** a handheld action; a cloud test
against a real provider or account; `fork-publish-release` without
`--prepare`; `rasteratops-candidate-store` or `pixelelated-state-check`
against the real store or a real image root (the cases build synthetic
bundles and payloads under `.qa-scratch/t14/`); an edit to
`tools/last-good-scripts-test` (T15's, #662 -- its `image_tool_source`
fallback is a lead for T15, named in S8); a build; `fork-worktree
sync|remove|repair`; a write under `/workspace/repos/rocknix*` or `/tmp`.
No rule edit: the rule and index leads are #1007's and #988's (below).

**The lane's two questions, answered first.** (1) **PL-09, the guest pair:**
the disposition stands (retire in place as refusing markers, beside the
stubs), **and one defect on it is a Bug the lane files at S11**: the
substring kill of any QEMU naming the pair path that runs even after a
refused start (`pixelelated-vm-cloud-boundaries:675-690` after `:709-710`).
That runs on current source, on a shared host, by pattern -- the thing
D-INFRA-028 and `engineering-practices.md`'s pidfile rule forbid -- so it is
a defect with a fix and a host-side proof whatever the tool's caller count.
The rest of the historical path's defects (the vacuous `all_absent` receipt,
the epic's unbound pidfile, setup failures that do not stop it, overwritten
witnesses, absence probes passing on an ssh failure) are listed in the
disposition and retire with the path. (2) **PL-11, the tenth tool:** both --
`pixelelated-cloud-validator-test` is in the class item (#986, where the
coordinator has added T14's ten) *and* has its own Bug (#994); the 21:03
ruling's last sentence is the rule: a tool that is uncalled and broken is
two facts.

**What the lane found, in one sentence each, so the streams read in order:**
two release-identity tests fail at the hash on expectations the tree moved
past, and accept any non-zero exit or an empty input as the refusal they
name (F-01, F-02, G-5, G-6, G-36); the sandbox the four real-rclone tests
share passes the caller's environment and, for three, the host network --
the one High (F-04, G-1, G-8) -- and the connections fixture's fake-provider
guard admits a real rclone and drops `--config` (G-20); five cloud tests can
pass without exercising what they name, two of them refusing the package's
own rclone on a hard-coded version (F-03, F-05, F-06, F-14, G-28 to G-31,
G-40, G-41); two hardware tests carry their verdicts on `assert` (F-07); the
wrapper test counts globally and leaves its sources behind (F-08); the two
settings writer tests accept any busybox as the candidate's (F-13); the
release state check, its control and the candidate store each accept a
neighbour of what they name (G-25, G-32, G-38); and the lock test never reads
the lock's status (G-35). Five Renovation items and one conditional are
dispositioned below.

## S1. The release identity tests read the recipe, not a literal, and refuse by reason: `build-identity-test` and `rasteratops-identity-check` (PL-01, PL-02; #989, #990) -- `fix-case`

- **Why a stream:** both fail at the hash on a literal the tree moved past
  (`build-identity-test:132`'s plain-text firmware stand-in, refused by the
  `pixelelated-state-check` gate `fork-publish-release` gained at
  `d9f428e1a0`; `rasteratops-identity-check:143`'s `PKG_LICENSE == "MIT"`
  against a recipe that has said `MIT AND BSD-3-Clause` since `84ff94fb3d`),
  and both pass things they should refuse (any non-zero exit as *the*
  refusal; an empty gamelist; a shadowed assignment).
- **Files owned:** `tools/build-identity-test`, `tools/rasteratops-identity-check`.
- **The shape:** the identity test's stand-in is a payload the gate accepts
  (the smallest squashfs the test can build from `mksquashfs` when present,
  else the gate is given a double that records its call and the case says
  so), and each refusal case asserts the gate's named reason and exit, not
  `rc != 0`; the identity check reads the licence from the recipe's effective
  value (`config/options` with `PROJECT`, `DEVICE`, `ARCH` set, as
  `device-builds.md` § 3 says) and asserts it against an allowed set with the
  recipe's own text quoted on mismatch; an empty gamelist is a failure named
  *empty*; a shadowed assignment is detected by reading the last assignment
  of the name, not the first.
- **The test first:** at the stage-D export both tools exit 1 (`00` § Stage
  A: 21 passed/2 failed; 38/1) -- that is the positive for the first half;
  for the second, a case per accepted-wrongly input: a gate double exiting 1
  with the wrong reason (the unfixed test credits it), an empty gamelist
  (the unfixed check passes it), a recipe with two assignments of
  `PKG_LICENSE` (the unfixed check reads the first).
- **Already written:** the record's identity and candidate-store receipts
  under `docs/releases/` and the catalog stand as history; the coordinator
  re-reads the rows that cite a `build-identity-test` PASS from before
  `d9f428e1a0` at integration and marks them; nothing on a device.
- **Acceptance (#989, #990):** both tools exit 0 at the fixed tip on the
  tree; the new cases named with their positives.
- **Commits:** `build-identity-test: a stand-in the gate accepts; refusals by reason (#989)`,
  `rasteratops-identity-check: the licence from the recipe; an empty gamelist and a shadowed assignment refused (#990)`.

## S2. The shared sandbox and the connections fixture: an allowlisted environment, the network unshared where the backend is local, the fake-provider guard exact, `--config` passed (PL-04 High, PL-15; #992, #999) -- `fix-case`

- **Why a stream:** the one High. `Fixture.run` in
  `rasteratops-cloud-layout-test:138-147` -- the sandbox the four
  real-rclone tests share, and the validator's adoption sandbox
  (`:326-335`) with it -- asks only `--unshare-pid`, sets `HOME` and `PATH`,
  and passes every other caller variable: `RCLONE_CONFIG`,
  `RCLONE_CONFIG_<REMOTE>_*`, `BASH_ENV`, exported functions, and a `TMPDIR`
  that names a path not mounted inside (2 false FAILs, 13 of 13 with it
  unset). The connections fixture's fake-provider guard admits a real
  rclone at another path and drops the stage's `--config`, so a `config
  create` would write the caller's default configuration (G-20).
- **Files owned:** `tools/rasteratops-cloud-layout-test` (the `Fixture`),
  `tools/pixelelated-cloud-validator-test` (its sandbox), the fixture under
  `tools/test-fixtures/` the connections test uses (its guard; the
  consumer, T15's `cloud-connections-test`, is read, never edited).
- **The shape:** the sandbox runs its command under `env -i` with an
  allowlist (`HOME`, `PATH`, `LANG`, `TERM`, and the fixture's own
  variables, each named), `TMPDIR` set to a path mounted inside, no exported
  function; `--unshare-net` wherever the test's backend is a local filesystem
  or an in-sandbox process, and where a test reaches the host's QA backend
  over loopback the network stays with the reason in the test's header (the
  lane reads each binding first, D-QA-058, and records which of the four is
  which in `02`); the fake-provider guard identifies the binary by its path
  *and* a marker the fake prints on `version`, refuses a real rclone wherever
  it sits, and passes the stage's `--config` through so nothing can reach
  `~/.config/rclone/rclone.conf`.
- **The test first:** with the caller exporting `RCLONE_CONFIG=<a stand-in
  path>`, `BASH_ENV=<a file that writes a marker>` and
  `TMPDIR=/workspace/tmp/m6-t14/x`: the unfixed sandbox lets the marker
  appear and the two `T24-local-*-recovery` cases fail (the positive); the
  fixed one shows none of them inside and 13 of 13 pass; a real rclone
  copied to another path: the unfixed guard admits it (positive), the fixed
  refuses by name; a `config create` through the fixture: the written file
  is the stage's, and `~/.config/rclone/rclone.conf` is untouched (checked
  by mtime before and after on a stand-in `HOME`, never the lane's own).
- **Already written:** whether any past run of the four reached the
  caller's rclone configuration cannot be read from the record (the tests
  print no environment); the lane records the host's `~/.config/rclone`
  mtime beside the stage-D export's run so a later question has a baseline
  (read through the dropping filter; the value never printed); nothing on a
  device, nothing in a cloud.
- **Acceptance (#992, #999):** the cases named with their positives; the
  four tests pass under the allowlisted sandbox with the caller's
  `TMPDIR`, `RCLONE_CONFIG` and `BASH_ENV` set.
- **Commits:** `rasteratops-cloud-layout-test, pixelelated-cloud-validator-test: the sandbox allowlists its environment and unshares the network where the backend is local (#992)`,
  `test-fixtures: the fake-provider guard is exact and keeps --config (#999)`.

## S3. `pixelelated-cloud-validator-test` and `pixelelated-duckstation-capture-test`: the rclone pin from the recipe, an unknown case refused, controls that discriminate, the payload inside the sandbox (PL-03, PL-06, PL-14; #991, #994, #998) -- `fix-case`

- **Why a stream:** both hard-code `rclone v1.75.1` (`:58`, `:178`) and
  refuse the package's own 1.75.2 (pinned since `a0f60255ab`); the
  validator's `--case <nothing>` returns early from every case and prints
  `PASS 0 controls`, rc 0 (P5, T12's `--only` shape), and several controls
  accept an empty or non-discriminating result; the capture test runs its
  installed payload on the host outside its `bwrap` (`:334`) and drops
  unknown `--cases` names.
- **Files owned:** `tools/pixelelated-cloud-validator-test`,
  `tools/pixelelated-duckstation-capture-test`.
- **The shape:** the required rclone version is read from the recipe's
  effective `PKG_VERSION` at run time and compared with `rclone version`'s
  first line, mismatch named with both; an unknown or empty `--case` /
  `--cases` is exit 2 naming it; every control asserts the specific value
  or refusal it was written for (a positive control that passes on an empty
  result is rewritten or removed with its reason); the payload runs inside
  the same `bwrap` as the rest, with S2's allowlist.
- **The test first:** at the export both refuse the 1.75.2 binary (the
  positive); `--case nosuch` exits 0 with `PASS 0 controls` (P5, the
  positive) and exits 2 fixed; each rewritten control, fed the
  non-discriminating result it used to accept, fails on the fixed tool; the
  payload case, with a marker the payload writes, shows the marker inside
  the sandbox's root and nowhere on the host.
- **Already written:** the record's validator and capture PASSes predate
  the pin move and are history; nothing on a device.
- **Acceptance (#991, #994, #998):** the cases named with their positives;
  both tools exit 0 against the package's rclone.
- **Commits:** one per bug, in that order.

## S4. `pixelelated-content-scope-test`: the refusal that got safer is asserted as a refusal, and each case exercises what it names (PL-05; #993) -- `fix-case`

- **Why a stream:** two cases read `ctl/argv` unconditionally (`:132`,
  `:222`) while the script now refuses `..` before calling rclone
  (`e6645cb5ea`), so the read raises before the assertion -- a failure at
  the hash on a product change that made the path safer; several other
  cases can pass without exercising what they name (G-9, G-23, G-29, G-30).
- **Files owned:** `tools/pixelelated-content-scope-test`.
- **The shape:** a traversal case asserts the script's refusal by its
  reason sentence and asserts that rclone was *not* called (the argv file's
  absence is the proof, not an exception); each case named in `04` as
  passing vacuously gains the assertion that proves its name (the lane
  lists them in `02` with the line each now checks).
- **The test first:** at the export the tool fails on the two traversal
  cases (the positive for the first half); each vacuous case, run against a
  copy of the script with the behaviour it names removed, must fail on the
  fixed test and is recorded passing on the unfixed one.
- **Already written:** nothing on a device; the test's scratch roots are
  its own.
- **Acceptance (#993):** the tool exits 0 at the fixed tip on the tree; the
  cases named with their positives.
- **Commits:** `pixelelated-content-scope-test: a refusal is asserted as one; the vacuous cases exercise their names (#993)`.

## S5. `rasteratops-cloud-layout-test` and `pixelelated-save-layout-test`: the legacy case compares the new backup, failure controls assert the failure, applets required only where used, the historical ref's names (PL-21, PL-22; #1004, #1005) -- `fix-case`

- **Why a stream:** the legacy backup case accepts its input archive as the
  new backup and two failure controls never assert the failure (G-28, G-29,
  G-31); the save-layout test requires both applets on every selection and
  lists today's source names for a historical ref (G-40, G-41).
- **Files owned:** `tools/rasteratops-cloud-layout-test` (its cases; the
  `Fixture` is S2's and lands first), `tools/pixelelated-save-layout-test`.
- **The shape:** the legacy case asserts the new backup's identity differs
  from the input's (name and hash) and carries the migrated layout; each
  failure control asserts the specific failure (exit and reason); the
  save-layout test requires an applet only for the selection that uses it
  and reads the source names of the ref it is given, not of the working tree.
- **The test first:** the legacy case fed its own input as the "new" backup
  passes on the unfixed test (positive) and fails fixed; a failure control
  run against a script that does not fail passes unfixed (positive) and
  fails fixed; a selection that needs one applet, with the other absent,
  refuses unfixed (positive) and runs fixed; a historical ref with a renamed
  source lists the ref's names.
- **Already written:** nothing on a device or in a cloud.
- **Acceptance (#1004, #1005):** the cases named with their positives.
- **Commits:** one per bug.

## S6. The hardware fixture tests carry their verdicts on checks that survive `-O`, and assert their substitutions: `rocknix-info-test`, `nova-led-test` (PL-07; #995) -- `fix-case`

- **Why a stream:** the verdict is `assert` (`rocknix-info-test:29`) under
  an unconditional `PASS` print (`:58`); under `python3 -O` or
  `PYTHONOPTIMIZE=1` a regression recorded failed in `result.json` prints
  `PASS 12`, rc 0 (P4); the production-path adaptations use unchecked
  `str.replace` (`nova-led-test:35-41`, `rocknix-info-test:21-26`), so a
  path that no longer matches is adapted to nothing and the test runs the
  unadapted script.
- **Files owned:** `tools/rocknix-info-test`, `tools/nova-led-test`.
- **The shape:** every verdict is an explicit check that sets the result
  and the exit (the T12 S12 shape); the tool refuses to run under
  optimisation if any `assert` remains (`sys.flags.optimize` → exit 2); each
  `replace` asserts it changed the text, or fails naming the pattern it
  expected.
- **The test first:** `PYTHONOPTIMIZE=1` with the constructed regression
  (P4): `PASS 12`, rc 0 unfixed (positive); rc 1 fixed; a source with the
  adapted path renamed: the unfixed test runs the unadapted script and
  passes (positive); the fixed one fails naming the pattern.
- **Already written:** the CI runs neither under `-O`, so no recorded pass
  was hollow on that account; nothing on a device.
- **Acceptance (#995):** the cases named with their positives; both tools
  rc 0 on the tree.
- **Commits:** one per tool.

## S7. `retroarch-wrapper-test` counts per call site, removes its sources, and treats a missing compiler as a refusal (PL-08; #996) -- `fix-case`

- **Why a stream:** one global call counter is compared with the post
  count (`:111`, `:123`, `:203`), so two sites calling once each read as one
  site calling twice and the inverse; `<tmp>/t` and `t.c` are left behind
  (`:213`); a missing `gcc` raises at `:216` and exits 1 -- the code the
  docstring reserves for *the command ran twice* (`:27`). Its default roots
  (`:42-43`) are #640's retired layout and stay #640's: this stream makes the
  bare run exit 2 with a usage line naming `RETROARCH_SRC`, and moves no
  default.
- **Files owned:** `tools/retroarch-wrapper-test`.
- **The shape:** a counter per call site, each compared with its own
  expectation; a `trap` removes the scratch sources on every exit; a missing
  compiler is exit 2 with its name, never 1.
- **The test first:** two sites posting once each: the unfixed test's
  global count passes (positive) where the per-site count must; `find` after
  a run lists `t.c` unfixed (positive) and nothing fixed; `PATH` without a
  compiler: exit 1 unfixed (positive), exit 2 fixed with the name.
- **Already written:** `t.c` leftovers under earlier runs' `TMPDIR`s are
  the record's; the lane lists and removes its own; nothing on a device.
- **Acceptance (#996):** the cases named with their positives; the tool
  passes with `RETROARCH_SRC` pointed at a copy of
  `gfx/video_thread_wrapper.c` under `.qa-scratch/t14/` (never an M7 build
  root written to; a read of one is allowed and recorded).
- **Commits:** `retroarch-wrapper-test: a counter per call site, the sources removed, a missing compiler is exit 2 (#996)`.

## S8. The settings writer tests record their busybox's provenance and refuse an unverified one: `settings-modes-test`, `melonds-upgrade-test` (PL-13; #997) -- `fix-case`

- **Why a stream:** both take any `--busybox` and run it as the
  candidate's (`settings-modes-test:9`, `:26`; `melonds-upgrade-test:43`);
  with no build root T15's `image_tool_source` falls back to the host's
  busybox (`last-good-scripts-test:381-400`, `command -v busybox || true`),
  so a host BusyBox 1.37.0 passes as the image's 1.36.1 unmarked
  (`upgrade-and-install.md` § under the device's tools, blindspot 34);
  `settings-modes-test` leaves host commands unshimmed and its applet path
  unquoted (`:10`).
- **Files owned:** `tools/settings-modes-test`, `tools/melonds-upgrade-test`.
  **Not** `tools/last-good-scripts-test` (T15's): the fallback there is a
  lead the coordinator carries to #662's brief, named in the Phase 7 table.
- **The shape:** `--busybox <path>` is accepted when the path lies under a
  build root's `image/system/` (the BUILD_ID read from that root's
  `/etc/os-release` and printed in the result), or when
  `--busybox-from <BUILD_ID|image>` names its origin, which the result
  records; a bare host busybox is refused unless `--unverified-busybox` is
  given, and then every result line carries `host busybox, not the
  candidate's` and the exit is 3 (a run that could not qualify the
  candidate has not passed; D-QA-061's shape); every host command the
  writer scripts call that is a busybox applet on the device is shimmed;
  the applet path is quoted.
- **The test first:** the host's `/usr/bin/busybox` as `--busybox`: the
  unfixed test runs and prints PASS as the candidate's (positive); the
  fixed one refuses, and with `--unverified-busybox` exits 3 with the
  marker on every line; a busybox under a scratch tree shaped like a build
  root (`image/system/usr/bin/busybox` beside an `etc/os-release` naming a
  stand-in BUILD_ID): accepted, the id in the result; a path with a space:
  the unquoted wrapper breaks unfixed (positive), works fixed.
- **Already written:** the record's `settings-modes-test` and
  `melonds-upgrade-test` passes name no busybox; the lane records which
  busybox this host offers (`readlink -f $(command -v busybox)`, its
  version) in `02` so the record can be read; the M7 build roots' busybox
  (image BUILD_ID `1a026648442321609b2288c2c9c06803817f9df2`, the one the
  lane used at stage A) counts as a build root's; nothing on a device.
- **Acceptance (#997):** the cases named with their positives; both tools
  pass with a build root's busybox and refuse the host's bare.
- **Commits:** one per tool.

## S9. The release state check, its control and the candidate store accept only what they name: `ExecStart`'s command word, a credited control's reason and count, the bundle's given name (PL-16, PL-18, PL-19; #1000, #1001, #1002; PL-17's header) -- `fix-case`

- **Why a stream:** three inputs to release gates. `pixelelated-state-check:839`
  accepts `/usr/bin/autostart` anywhere in `ExecStart`, an argument
  included (G-25); `pixelelated-state-check-test:125-137`, `:772` credits a
  control when the gate fails for any reason and never asserts its control
  count (G-32); `rasteratops-candidate-store verify` resolves its argument
  before comparing the bundle's name with its manifest digest (`:30`,
  `:57`), so a symlink named for one digest can point at another bundle
  (G-38). **What the gates require stays the coordinator's**
  (`release-candidates.md`, D-WORKFLOW-157/159/168): these streams fix what
  the tools read, not what the procedure asks.
- **Files owned:** `tools/pixelelated-state-check`,
  `tools/pixelelated-state-check-test`, `tools/rasteratops-candidate-store`.
- **The shape:** the readiness check parses `ExecStart` as systemd does and
  compares the command word (the first token after the optional prefix
  characters), never a substring; the control credits a case only on the
  gate's named refusal (its reason line and exit) and asserts the total
  number of controls run against the number declared; `verify` compares the
  name it was *given* with the manifest digest and refuses a symlink (or
  compares both the given and the resolved name and requires agreement),
  naming what it saw. **PL-17's wording lands here too:** the state check's
  header says the accurate guarantee -- *no value in reports*: its payload
  inspection writes raw selected bytes to private temp files (`:100-112`,
  `:366-371`) which are removed on exit -- and the stream adds the removal
  on every exit path (a `finally`) so the sentence is also true of the
  scratch; the rules' wording is #1007's.
- **The test first:** a unit whose `ExecStart` carries `/usr/bin/autostart`
  as an argument of another command: ready unfixed (positive), not ready
  fixed; a gate double failing with an unrelated reason: credited unfixed
  (positive), uncredited fixed; a declared count of N with N-1 controls run:
  PASS unfixed (positive), FAIL fixed; a symlink named for digest A pointing
  at bundle B: verify passes unfixed (positive), refuses fixed naming both;
  a payload inspection interrupted by a signal: the temp file remains
  unfixed (positive), is gone fixed. All against synthetic units, bundles and
  payloads under `.qa-scratch/t14/`, never the real store or an image root.
- **Already written:** `docs/releases/` receipts that cite a `verify` PASS
  or a readiness PASS stand; the coordinator re-reads the ones since
  `d9f428e1a0` at integration against the fixed tools and marks them;
  nothing on a device.
- **Acceptance (#1000, #1001, #1002):** the five cases named with their
  positives; `pixelelated-state-check-test --self-test` rc 0; the header's
  sentence quoted.
- **Commits:** one per bug; `pixelelated-state-check: the guarantee stated as no value in reports; the scratch removed on every exit (#661)`.

## S10. `wait-lock-test` reads the lock's status and races two acquirers (PL-20; #1003) -- `fix-case`

- **Why a stream:** the test never checks `wait_lock`'s return status
  (`:59-64`) and never races two acquirers from an absent lock, so a
  `wait_lock` that returns failure while the caller proceeds would pass, and
  the one property a lock exists for -- two acquirers, one winner -- is
  unproved (G-35).
- **Files owned:** `tools/wait-lock-test`.
- **The shape:** every call's status is asserted; a new case starts two
  acquirers with no lock present and asserts exactly one wins within the
  bound and the other waits or fails as documented; the case is run under
  the image's busybox through the same shims as `last-good-scripts-test`
  uses (the function under test runs on the device).
- **The test first:** a `wait_lock` copy that returns 1 and proceeds: the
  unfixed test passes (positive), the fixed one fails; the race case against
  a copy whose lock is advisory-only: both win unfixed (positive), one wins
  fixed.
- **Already written:** nothing on a device; `/var/run/cloud_sync.lock`'s
  semantics on devices are unchanged by a test.
- **Acceptance (#1003):** the cases named with their positives.
- **Commits:** `wait-lock-test: every status read; two acquirers, one winner (#1003)`.

## S11. The guest pair's live defect, and the stubs' docstrings: no kill after a refused start, and never by pattern (PL-09's Bug; PL-10's docstring) -- `fix-case`

- **Why a stream:** `pixelelated-vm-cloud-boundaries` stops guests by
  scanning `/proc/*/cmdline` for its pair path and signalling (`:675-690`),
  and runs that after a refused start (`:709-710`, rc 1): on a shared host a
  pattern kill reaches a guest that is not its own, and a sandbox hiding
  host PIDs (#506) makes it record `all_absent: True` over a live guest. The
  tool refuses every run on current source and stays a refusing marker
  (below), but this path runs on refusal. The stub
  `pixelelated-cloud-folder-test`'s docstring names rclone 1.75.1 as the
  current coverage (F-03's third site).
- **Files owned:** `tools/pixelelated-vm-cloud-boundaries`,
  `tools/rasteratops-vm-cloud-epic` (the refusal path only),
  `tools/pixelelated-cloud-folder-test`, `tools/pixelelated-cloud-folder-vm-test`
  (docstrings only).
- **The shape:** the lane files the Bug first (its stage-D shape: code
  trace, VM line, `Already written:`, agent-checkable criteria, scanned,
  `box-check` 0 fail), then: a refused start exits with nothing stopped and
  nothing scanned; any stop goes through `tools/vm-stop` by the pidfile the
  tool itself wrote, never by pattern; `all_absent` is recorded only from
  pidfiles it owns, and a hidden `/proc` is an observation error, not an
  absence; the stubs' docstrings name the current coverage by tool and
  flow, not by a version.
- **The test first:** a fixture process whose cmdline carries the pair path
  and a refused start: the unfixed tool signals it (positive, against a
  disposable fixture process the case owns -- never a QEMU); the fixed tool
  exits without a signal, and `all_absent` is not written; the docstrings
  read by `grep -c '1.75.1'` → 0.
- **Already written:** the two tools have refused every run since #508
  retired `cloud_migrate_layout`, so no recorded run of the current tree
  took this path; the historical runs are the record's; nothing on a device.
- **Acceptance (the Bug the lane files; #661):** the cases named with their
  positives; the Bug's criteria ticked from them.
- **Commits:** `pixelelated-vm-cloud-boundaries: nothing stopped on a refused start, and never by pattern (#<the Bug>)`,
  `cloud-folder stubs: the docstrings name the current coverage (#661)`.

## S12. The lint's fail fixtures prove one guard each (PL-23) -- `fix-case`

- **Why a stream:** the renovation face's fail fixture couples two
  violations (the renovation face and `question:`), so a runner that checks
  pass and fail proves neither guard alone (G-42). T10's `run.sh`
  (`2444828e89`, on T10's branch, which merges before this one) checks the
  fail fixture for one named `CONTRACT FAILURE` and adds an index-boundary
  fixture; it does not split this one.
- **Files owned:** `tools/test-fixtures/lint-audit-artifacts/` -- a **new**
  fixture directory per violation (`fixture-epic-m6-renovation-fail-face`,
  `fixture-epic-m6-renovation-fail-question`), the existing coupled fixture
  left as it is. **Not `run.sh`**, which is T10's on its branch and absent
  here: the two new check lines are the coordinator's at the merge.
- **The test first:** `tools/lint-audit-artifacts` over each new fixture
  exits 1 with the one named failure, and over the pass fixture exits 0;
  the unfixed state is the coupled fixture, whose two failures cannot be
  told apart in one run (the positive is the run's output naming both).
- **Already written:** nothing on a device.
- **Acceptance (PL-23):** the two runs quoted; the Phase 7 table carries
  PL-23 at `fixed` with the two directory names and the note that `run.sh`
  gains its lines at the merge.
- **Commits:** `lint fixtures: one fail fixture per violation (#661)`.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-09 (the guest pair) and PL-10 (the stubs): retire in place, as
  refusing markers.** The four tools refuse every run by design --
  `cloud_migrate_layout` was retired by D-CLOUD-175/#508, and the stubs
  refuse on purpose -- and are kept in the tree as markers until the
  maintainer answers the removal the coordinator puts to them on #346 as one
  bundle: these four, with T12's `vm-walks/cloud-epic/migration-protocol.sh`
  and `vnc-grab.py`, whose only caller is `rasteratops-vm-cloud-epic`.
  Nothing is removed by the lane (preservation over deletion,
  `working-principles.md`; `engineering-practices.md` § Before deleting a
  duplicate: the lane's `02` lists what each marker still carries -- a
  historical proof's shape, a docstring, a list entry). The index rows and
  list entries that should say *retired* are #1007's. S11 fixes the one
  path that runs on refusal.
- **PL-11 (the ten uncalled tools):** #986, where the coordinator added
  T14's ten at this pause with the suites each could join; each row's
  disposition is the coordinator's with the maintainer; the lane writes
  `deferred: #986`.
- **PL-12 (thirteen index rows; the stubs' entries):** #1007 (the T14 rules
  Backlog, filed at this pause, a sub-issue of #903), made at integration in
  the doctrine packet after T4's merge; no rule edit by the lane.
- **PL-17 (the state check's guarantee):** the tool's header and the scratch
  removal are S9's; the rules' sentence is #1007's; `release-candidates.md`'s
  gate contract is unchanged (D-WORKFLOW-157/159/168).
- **PL-16 and PL-19 (release-gate inputs):** S9 fixes the tools; the gates'
  requirements are not changed by this slice. The coordinator re-reads the
  `docs/releases/` receipts since `d9f428e1a0` against the fixed tools at
  integration and marks any that the fixed tools would have refused.
- **PL-23:** S12, with `run.sh`'s two lines the coordinator's at #945's
  merge.
- **F-13's T15 half** (`image_tool_source`'s silent host fallback,
  `last-good-scripts-test:381-400`): a lead the coordinator carries to T15's
  brief (#662); not touched here.
- **F-15:** withdrawn by the seat; nothing.
- **For the maintainer, on #346 (the coordinator posts them at this
  pause):** the removal bundle (four refusing markers and two walk scripts);
  the note that two release-gate inputs (#1000, #1002) are fixed in the tools
  with the gates' words unchanged.

## Order and hand-back

S2 first (the sandbox the cloud tests share, so S3 to S5 run under it);
then S1, S3, S4, S5; S6, S7, S8, S9, S10 in any order; S11 (file the Bug,
then fix); S12 last. Each commit cites its bugs (`Refs #N, #661`, no closing
keyword: a bug closes when its fix is on `next`) and carries the attribution
line; `git status --short` before every `git add -A` (`.qa-scratch/` is
gitignored; the positives and the scratch roots stay there). No guest; the
host file is read before any run that could be mistaken for a guest (none
is), and the census stays 0 for this lane.

After S12: the Phase 7 table and the `punch_index` at their outcomes
(`fixed`, `deferred` with its issue, `design` with its sentence), `02` § The
suites re-run (every one of the 21 tools at the fixed tip with its exit and
wall time, the S2 environment case, the busybox provenance line), the lint on
the folder (`PASS`, the default phase), `fixed-at:` in #661's body, the retro
(stage G, posted on #661: what the slice did to the two time-to-play numbers
-- nothing; what each stream did to a test's refusals -- the list; the
brittleness table's after-column), then the hand-back comment naming the tip
and each artifact by path. The coordinator accepts by
`AUDIT_ISSUE=1006 $S/t14-accept.sh <tip> <coordinator tip>` on an export
(membership, line counts, the bare-run tests, the two stubs' rc 2, the lint
fixtures, `register-check`, `rules-check --quiet`, `work-log-index --check`),
reads every stream's diff and positives, ticks #661 and #1006 from the
artifacts, closes #1006 when its checkboxes read back ticked by name, and
merges the branch in its turn (after T12's, before T4's); the receipts
re-read and the `run.sh` lines are the coordinator's, made at the merge.

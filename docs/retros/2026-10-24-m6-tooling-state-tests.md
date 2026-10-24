# Mini Retro: M6.P2 T14, the last-good, settings and state tests (#661)

**Completed:** 2026-10-24
**Scope of this retro:** T14 from its dispatch on #661 (20:16 UTC) to the
hand-back. Stages A to D were the audit: the 21 tools read through the
brittleness lens, with one GPT-6 Astra seat. Stage E was the twelve streams of
`docs/reviews/briefs/t14-streams.md` (`13242d182a`).

**Branch:** `feature/m6-tooling-state-tests-661`. Reviewed at `30da4853bb`;
the stage-D tip is `7aa8eac253`; the fixed tip is the hand-back's.
**Delta:** 23 punch items. Twenty-one are resolved and two deferred (PL-11 to
#986, PL-12 to #1007). The 17 audit bugs (#989 to #1005) are fixed, and the
lane filed two more and fixed them (#1009, #1011). 27 proofs, each a control
under `docs/qa-logs/2026-10-24-state-tests-s*/` that passes the stage-D tool
(or the commit before its fix) and fails the fixed one, or the reverse where
the fix adds a pass.

## Time to play

**Nothing changes, by construction.** Every file changed is a host-side test
tool, a test fixture or a record. No product script, package or image byte
changed, so interface → first frame and exit → next first frame are untouched.
No guest was started in stage E.

## What each stream did to a test's refusals

| Stream | Before | After |
| --- | --- | --- |
| S2 (#992, #999) | The real-rclone sandboxes passed on the caller's environment (`TMPDIR`, `RCLONE_*`, `BASH_ENV`) and the host network, and the connections fixture admitted a real rclone at another path | `--clearenv` with a named allowlist, `--unshare-net`; only a non-ELF shim inside the fixture runs as the fake provider, and `--config` is kept |
| S1 (#989, #990) | A refusal case passed on any non-zero exit; the identity check passed an empty gamelist and a shadowed `PKG_LICENSE` | Each refusal names its reason and code; the last assignment is read; an empty gamelist fails; a missing `mksquashfs` is CANNOT, exit 2 |
| S3 (#991, #994, #998) | Two tests refused the package's own rclone; an unknown `--case` passed with 0 controls; the DuckStation payload ran on the host | The pin is read from the recipe; unknown cases exit 2; the counts are asserted; the payload runs inside the sandbox |
| S4 (#993) | Traversal and failure cases passed without the refusal they name, or without the fault firing | Each asserts its sentence, the absent argv, the selected library's listing, or `/ctl/fault-fired` |
| S5 (#1004, #1005) | The legacy backup accepted its input as the new archive; two failure controls never asserted the failure; save-layout required both applets always | A new archive is required; a backup after a failed read must exit 0 with `COMPLETED` into the configured folder, and a restore must exit non-zero (22:08 ruling); applets are required only where used |
| S6 (#995, #1009) | Verdicts rode on `assert`, so `-O` passed a regression; unchecked replacements; the scratch was left on a failure | `raise`; every adaptation pattern required; Nova's paths must keep their defaults; the scratch is removed on every exit |
| S7 (#996) | One global count; `t.c` left behind; a missing `gcc` read as "ran twice" (1) | A count per call site; the scratch removed on every exit, signals included; CANNOT, exit 2; a usage line |
| S8 (#997) | Any busybox was run as the candidate's; eleven shims; the path unquoted | A build root's busybox (BUILD_ID recorded), `--busybox-from`, or exit 2; `--unverified-busybox` marks every line and exits 3 when every case passed, 1 when one failed (22:29 ruling); every applet shimmed and quoted |
| S9 (#1000, #1001, #1002, PL-17) | `autostart` anywhere in `ExecStart` read as ready; a crash satisfied an expected-2 control; the count was unchecked; `verify` followed a symlink; a signal left raw bytes in the scratch | Two shapes and a constant, with a drift check on the tree's unit (22:30); `reader-failure` is reported and refused, and the self-test names are required (the payload half is #1010); the given name is verified; signals unwind to a value-free exit 2 |
| S10 (#1003) | `wait_lock`'s status was never read; no race | `WL=0` is required everywhere; two acquirers hold their turns without overlap; `--busybox` runs the device's applets |
| S11 (#1011, PL-10) | A refused start ran a `/proc` pattern kill and wrote `all_absent: True` | A refused start stops nothing; a stop goes through `vm-pair down` by pidfile in D-INFRA-031's runtime (22:54); a hidden pid is an observation error; the stub names its coverage, not a version |
| S12 (PL-23) | One fail fixture coupled two violations | One fixture per violation, each resting on its own guard |

## The brittleness table's after-column

`04-analysis.md` § Q6 column (a) holds what each tool depended on and what
that dependency's absence did, at `8ebaf8daad`. This is the same column at
the fixed tip.

| Tool | (a) after |
| --- | --- |
| `wait-lock-test` | Unchanged exits 2. The device's applets are used with `--busybox`, and the first line names the tools that ran. GNU `date` is still the host's (the timing harness, not the function under test) |
| `rocknix-info-test` | A changed spelling fails, naming the pattern. `-O` no longer strips a verdict. The scratch goes on a failure too (#1009) |
| `nova-led-test` | Every adaptation pattern is required. A hardcoded `LED_PATH`/`BATTERY_PATH` or a bare `/sys/` is refused before running. `-O` is safe |
| `usb-gadget-test` | Unchanged (not a stream). `--shell` still defaults to the host's `/bin/sh` |
| `settings-modes-test` | A busybox of unknown origin gives exit 2, or with `--unverified-busybox`, marked lines and exit 3 (1 on a failing case). Every applet is shimmed, including `cat`, `rm` and `mktemp`; `grep` and `sort` are the image's other packages' and stay the host's |
| `melonds-upgrade-test` | The same provenance contract; its five commands were already shimmed |
| `retroarch-wrapper-test` | No source: exit 2 with a usage line. No `gcc`: CANNOT, exit 2. The scratch is removed. The default roots are still #640's |
| `build-identity-test` | The stand-in is a real update tar the gate accepts. No `mksquashfs`: CANNOT, exit 2 |
| `rasteratops-identity-check` | The licence is read from the recipe's last assignment. An empty gamelist fails |
| `rasteratops-candidate-store` | A symlink or a mismatched name is refused, naming both |
| `pixelelated-state-check` | A gate fault is `reader-failure`, not `input-invalid`. A signal leaves no scratch. Readiness reads `ExecStart`'s command |
| `pixelelated-state-check-test` | A crash fails its control; a lost registration fails the run. `--payload-tests` still needs `mcopy` (#1010) |
| `rasteratops-cloud-layout-test` | The caller's environment no longer reaches the sandbox. The backup contract is asserted |
| `pixelelated-cloud-validator-test` | The rclone must be the recipe's. An unknown case exits 2. Each control discriminates |
| `pixelelated-content-scope-test` | Each case proves the path it names. Unknown cases exit 2 |
| `pixelelated-save-layout-test` | The applets are required only by a full run. `--ref` lists that ref's own names |
| `pixelelated-duckstation-capture-test` | The rclone must be the recipe's. The payload runs inside the case sandbox (a synthetic 0755 witness, not the AppImage runtime) |
| `pixelelated-vm-cloud-boundaries` | Still refuses current source (#508). A refused start stops nothing. The runtime is its own, and a hidden pid is an observation error |
| `rasteratops-vm-cloud-epic` | Unchanged: its refusal precedes its trap |
| `pixelelated-cloud-folder-test`, `-vm-test` | Unchanged refusals; the docstring names the coverage by tool and flow |

## What worked well

- **The stage-D export as the fixed point.** Every positive ran against
  `git archive 7aa8eac253`, so "the unfixed test passes" was always observed
  by running, never argued. 26 proofs, and 26 `PROOF:` lines.
- **Questions put with the evidence and a default, work continuing.** Seven
  of the coordinator's rulings (22:08, 22:22, 22:29, 22:30, 22:35, 22:46,
  22:54) each settled a fork the brief could not have foreseen. One example:
  the shipped `ExecStart` really does carry `autostart` as an argument.
- **Disposable fixtures for dangerous shapes.** The pattern kill was proved
  against a `qemu-system-fixture` process the case owned, beside another
  lane's live guests, and nothing else could match.

## What was harder than expected

- **My own controls slipped, more than once each.** Some mutations proved
  nothing: one stole a live holder's lock, one failed a lock release that a
  trap repaired, and one put a space in every TMPDIR. Some checks were too
  strict: an exact `input-invalid` failed a named Check row. These were
  corrected before the controls were kept, each logged in `00`. The
  recurring cause: a mutation that changes more than the one property under
  test. The fix was the same each time: confirm the stage-D run passes for
  the right reason, by reading its output, before trusting the positive.
- **A shared fixture broke its consumer, and only running the consumer
  showed it.** S2 moved `--config` before the command in the connections
  fixture, and T15's shims read the command from `$1 $2`. S2's own control
  asserted the moved shape, so it passed. The close-out's single
  `last-good-scripts-test` run, which the coordinator asked for at 21:39
  because a consumer proves a shared fixture, failed two broker checks.
  Fixed in `9df25309f3`, with T15's shim shape added to the control. The
  same run showed S8's provenance contract refusing T15's copied busybox
  (#662's file). Both should have been found at their streams: run the
  consumer when a stream changes something it calls.
- **Bytecode written beside the tools.** `SourceFileLoader` under `-I` writes
  `tools/__pycache__`, and so does `py_compile`. It happened in
  stages A to D and again in S9 and S11, each time removed by name, before both
  probes ran with `-B` and `dont_write_bytecode`.
- **A removal on a possibly-empty variable** raised a permission dialog that
  was rightly dismissed (22:35). Every control now guards its removal with
  `${S:?}`, and removals go in short commands of their own. This is kept as
  a memory.

## Discoveries that affect future work

- `vm-pair` defaulted the runtime to the shared `/tmp`, so a tool that set
  only `VM_PAIR_DIR` shared pidfiles with every pair on the host. D-INFRA-031
  settles it for the harness; #1011 applies it here.
- The image's systemd 255.8 prints `ExecStart`'s argv joined by spaces,
  unquoted. A parser of it cannot see token boundaries; the gate compares the
  path and the whole joined argv.
- `--payload-tests` cannot run on this host (no `mcopy`). Its names go
  unlisted until #1010.

## Adjustments to remaining work

- **#662 (T15):** `last-good-scripts-test`'s `image_tool_source` falls back
  to the host's busybox silently. The hand-back's single run shows which
  busybox it resolved here.
- **#1007:** the index rows, the stubs' list entries and the state check's
  rule sentence.
- **#986:** the ten uncalled tools; #1010: the payload names.
- **At the merge (the coordinator's):** `run.sh`'s two fixture lines, and the
  re-read of the `docs/releases/` receipts against the fixed state check and
  store.

## Practice adjustments

- **A stream that changes a shared fixture or a tool's contract runs that
  thing's callers before it closes.** Not at the close-out:
  `git grep -n <tool or fixture> tools/` lists them, and T15's file is
  run read-only.
- **A control's mutation changes one property.** Before keeping it, read the
  stage-D run's output for the reason it passed, not only its exit. The two
  discarded mutations, S8's `rm` and S10's lock-stealer, would each have been
  caught that way.

---

Handed back on #661; the coordinator accepts with `t14-accept.sh`.

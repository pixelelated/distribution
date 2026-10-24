# Forward audit: M6.P2 T14, the last-good, settings and state tests (#661)

Read at `8ebaf8daad` (the 22) and `2174265e9c` (the ten lint fixtures); `reviewed-at` is `30da4853bb`.

## Phase 2: #661's checklist

| # | Criterion (#661 body, brief § 7) | State at stage B | Where |
| ---: | --- | --- | --- |
| 1 | the folder holds `00` to `05` | `00`, `01`, `02` exist | this folder |
| 2 | the lint prints `PASS` (pre-issue before D, default at close) | not yet run | `00` |
| 3 | `review-plan.json`, the seat's provenance, the packet's scan | not yet | `second-opinions/` |
| 4 | the punch-list issue's items all at an outcome | stage D onward | — |
| 5 | `reviewed-at` and `fixed-at` in #661's body | `reviewed-at` known (`30da4853bb`); written at hand-back | #661 |
| 6 | `01` § Scope | done | `01-research-notes.md` |
| 7 | the coverage table, 32 rows | stage B | § Coverage |
| 8 | § The runs | done for stage A | § The runs |
| 9 | § The guest cycle | no cycle so far | § The guest cycle |
| 10 | `00` shows none of the never-run actions | so far | `00` |
| 11 | `04` Q6's brittleness table | stage B | `04` |
| 12 | `04` Q3's hunt | stage B | `04` |
| 13 | `04` Q7's descriptions | stage B | `04` |
| 14 | `04` Q5's costs | the stage-A walls recorded | § The runs, `04` |
| 15 | every proof with `proved:`; the counts equal | running | § Proofs |
| 16 | `question:` on every item; the bugs pass `box-check --issue`; no tool edited before a stream | stage D onward | `05` |
| 17 | the retro | stage G | — |
| 18 | the six checkers and the lint at hand-back | stage H | — |

## The runs

Every run is in this worktree with `TMPDIR=/workspace/tmp/m6-t14/tmp`, except the two marked as run with `TMPDIR` unset. Each output is in `.qa-scratch/t14/`, and each exit is in `00` § Stage A.

| Run | Exit | Wall | Summary | A FAIL would mean |
| --- | ---: | ---: | --- | --- |
| `tools/wait-lock-test` | 0 | 7.5 s | `PASSED` | `wait_lock()` in `001-functions` waited past its bound, returned success without the lock, or let a second holder in |
| `tools/rocknix-info-test` | 0 | 0.5 s | `PASS 12 full-script positive/negative controls` | a hardware reading printed when its source was absent, or a quirk failure reported as a value |
| `tools/nova-led-test` | 0 | 0.2 s | `14 PASS, 0 FAIL` | an LED node, the saved brightness or the battery writer misbehaving under the real scripts |
| `usb-gadget-test --output ...` | 0 | 0.3 s | `18 cases, 72/72 checks` | a USB descriptor identity (`bcdDevice`, D-WORKFLOW-160) or a mode link wrong after preparation |
| `pixelelated-state-check-test --self-test` | 0 | 9.1 s | `status: pass`, 183 controls | the state check accepted a contaminated root, or disclosed a value |
| `pixelelated-state-check-test --payload-tests` | CANNOT | — | `mcopy` is absent on this host (`mksquashfs`, `unsquashfs` and `sfdisk` are present) | — |
| `build-identity-test --output ...` | **1** | 0.2 s | 21 passed, 2 failed: the state-check gate refuses the firmware stand-in | this is the FAIL. A product defect would show as an identity block or a plan that no longer carries the version, timestamp or source; here the test's own input is refused |
| `retroarch-wrapper-test <source>` | 0 | 0.1 s | `PASS: every command ran exactly once` (the source is the M7 root `m7-pixelelated-replacement20`'s `retroarch-bdba046fa...`) | the threaded video wrapper ran a posted command twice or not at all |
| `retroarch-wrapper-test` (bare) | 2 | — | no source given and none under #640's roots | — (cannot run; not a verdict) |
| `rasteratops-identity-check --tree <wt> --es <ES clone at the pin>` | **1** | 0.1 s | 38 PASS, 1 FAIL `ES licence matches its source` | this is the FAIL. It expects `MIT`, and the recipe says `MIT AND BSD-3-Clause` since `84ff94fb3d` |
| `settings-modes-test`, a build root's applets (BusyBox 1.36.1 from `m7-pixelelated-replacement20`, image `BUILD_ID 1a026648442321609b2288c2c9c06803817f9df2`; the effective pin is 1.36.1) | 0 | 0.4 s | `PASS refuse-rename` | a shell settings writer lost a file's private mode or published a failed staging file under the image's applets |
| `settings-modes-test`, the host's applets (BusyBox 1.37.0, Ubuntu): **a PASS of the host** | 0 | 0.4 s | `PASS refuse-rename` | the same, under the host's applets |
| `melonds-upgrade-test`, a build root's applets | 0 | 0.1 s | `PASS temp-failure` | post-update erased an owner's melonDS setting or added a hotkey non-atomically |
| `melonds-upgrade-test`, the host's applets: **a PASS of the host** | 0 | 0.1 s | `PASS temp-failure` | the same, under the host's applets |
| `rasteratops-cloud-layout-test` without `--archives-only` | 1 | 0.1 s | it refuses: the migration matrix was retired by #508 | — (a usage refusal) |
| `rasteratops-cloud-layout-test --archives-only`, `TMPDIR` set | **1** | 9.2 s | 11 PASS, 2 FAIL (`T24-local-*-recovery`): the sandbox inherits `TMPDIR` | this is the FAIL, and it is the test's (`00` § Stage B, trace 1) |
| the same, `TMPDIR` unset | 0 | 19.8 s | 13 PASS, 0 FAIL | an archive selected, written or read wrongly, or a missing remote not refused |
| `pixelelated-cloud-validator-test --rclone <image rclone 1.75.2>` | **1** | 0.1 s | it refuses: `Use the package-pinned rclone1.75.1` | this is the FAIL: the hardcoded version is stale against the pin |
| `pixelelated-content-scope-test` (`TMPDIR` set, and again unset) | **1** | 3.4 s / 3.3 s | 19 PASS, 2 FAIL (`system-traversal-refused`, `content-pointer-traversal-refused`) | this is the FAIL, and it is the test's (`00` § Stage B, trace 2) |
| `pixelelated-save-layout-test` (a build root's busybox) | 0 | 29.2 s | `39 PASS, 0 FAIL` | a standalone emulator's save path missing from the save coverage, or swept into a library transfer |
| `pixelelated-duckstation-capture-test` | **1** | 0.1 s | it refuses: `use package-pinned rclone` (1.75.1 hardcoded) | this is the FAIL: the same stale version |
| `tools/pixelelated-cloud-folder-test` | 2 | — | `Retired historical folder-contract control (#524 PL-002).` | — (a refusal by design) |
| `tools/pixelelated-cloud-folder-vm-test` | 2 | — | `Retired historical folder-overlay control (#524 PL-002).` | — (a refusal by design) |
| `tools/rasteratops-vm-cloud-epic` (bare) | 2 | — | `This migration suite is retired. ...` | — (a refusal) |
| `--help` of the other eight | 0 each | — | usage only | — |

**The three greps:**
- **`|| true`:** 0 lines in the 21 tools.
- **`^\s*assert `:** `nova-led-test` 1 and `pixelelated-vm-cloud-boundaries` 1.
- **Host paths:** 28 lines in 10 files (`.qa-scratch/t14/hostpaths.txt`).

## T15's call sites (read, not edited)

`tools/last-good-scripts-test` (T15's slice) calls four of these tools:

- `rasteratops-cloud-layout-test`, at `:252` (`--cloud-layout` execs it) and `:14175-14189` (`--output`, `--source-root`, `--rclone "${SA_RCLONE_SRC}"`, and `--archives-only` once `MIGRATION_AVAILABLE=0`);
- `settings-modes-test`, at `:14224`, with `TMPDIR="${TMP}"`, `--busybox "${BB_HOST}"`;
- `melonds-upgrade-test`, at `:14231`, the same way;
- `wait-lock-test`'s functions, lifted the same way at `:148` and `:8608`; the tool itself is not invoked.

**For T15 (#662, through the coordinator):** `image_tool_source` (`:381-400`) looks for a build root's binary and otherwise ends in `command -v "${name}" || true`. So with no root, it hands the host's busybox or rclone to every callee, which accept it. The run prints the busybox's source (`:426`), but no verdict marks the result as the host's.

**The recorded runs used build roots:**
- `docs/qa-logs/2026-10-08-pixelelated-replacement-18/qa21/.../scripts.log:3` and `2026-10-04-pixelelated-57cbc-qualification/qa-07/.../scripts.log:3` show `BusyBox v1.36.1 ... a copy of /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement...`.
- Their cloud-layout sections pass: `13 PASS, 0 FAIL` (2026-10-08) and `316 PASS, 0 FAIL` (2026-10-04, migration still available).
- Their artifacts are under `/tmp/cloud-layout-*`, so `vm-qa` ran T15 without a `TMPDIR` that would leak into the sandbox.

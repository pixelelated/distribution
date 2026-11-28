# #1506: the runner's branches that ended without a line, fixed on `next` and seen to fire

Can this be done on the VM? Yes. These are the host runner's own branches, constructed on vm-pair's guests from build 26's PC image (`6169621a4b`), on 2026-11-28 from 11:10 to 11:27 UTC. Nothing ran on a handheld or in a person's cloud. The QA cloud is the host's WebDAV.

Each fix was run against a constructed failure, and the unchanged tool was run against the same failure as the control.

## A. `link`'s pass with nothing run (`tools/cloud-round-trip`)

`vm-qa --only link` on a guest with no serial console (`VM_QEMU_RUNTIME_DIR` set to an empty folder):

- **Fixed:** the round trip ends `NOTHING RAN: every fixture --only LINK1,…,LINK7 asked for was skipped, so this is not a pass` with exit 3. The `vm-qa` table reads `link | SKIP`, and the report reads `PASSED with 1 suite(s) SKIPPED`. Files: `A-link.log`, `A-report.md`, `A-vmqa-link-noserial.out`.
- **Control:** the unchanged tool, with the same arguments, ends `PASSED (LINK fixtures: no serial console …)` with exit 0, which `vm-qa` showed as PASS (`A-control-old.out`).

## B. The same shape in the KILL cells (`tools/cloud-round-trip`)

`--only KILL12`, a power-cut cell, with no serial console and no monitor:

- **Fixed:** `NOTHING RAN … (KILL cells: every requested cell was skipped …)`, exit 3 (`B-kill12-fixed.out`).
- **Control:** `PASSED`, exit 0 (`B-kill12-old.out`).
- **A run with one real cell is still judged by its checks:** `--only KILL10,KILL12` runs KILL10, skips KILL12 with its line, and ends `PASSED` with exit 0 (`B-kill10-12-fixed.out`).

## C. The walks (`tools/vm-qa`)

`VM_QA_WALK_SUITE` names `constructed-suite.txt`, which has three walks:

| Walk | Constructed with | Fixed (`C-walks-fixed.walks.log`) | Control (`C-walks-old.walks.log`) |
| --- | --- | --- | --- |
| `bad-pre` | a pre-hook that prints and exits 7 | `walk bad-pre: pre hook exited 7 (want 0): constructed-pre-failure`; the walk still runs | nothing about the hook |
| `manager-hookdir` | a file where the system-selected hook folder goes | `walk manager-hookdir: could not make the system-selected hook folder or clear the last selection on the guest (ssh exit 1, want 0)` | no `walk manager-hookdir:` line at all; the suite failed with only scp's own error in the log |
| `es-down` | a drop-in under `/storage/.config/system.d/essway.service.d/` that delays essway's start by 240 s | `walk es-down: EmulationStation was not running 45 polls (about 2.5 min) after the reboot (want a pgrep match); the walk did not run. Guest: starting activating inactive` | `walk es-down: 0 frames [wake]`: it waited out the polls and then ran the walk |

- **The first fixed run, `C-walks-fixed-run1.*`, found two more defects:**
  - The folder step was `mkdir -p …; rm -f …`, so its exit status was `rm`'s, and a failed `mkdir` passed. Only the scp after it failed. It is `&&` now.
  - `systemctl mask essway emustation` did not keep ES down. The mask on `essway` did not survive the reboot, and essway, though "disabled", is started at boot. The construct moved to the start-delay drop-in.
- **`--walk` checks its name against the same file** the loop reads (`WALK_SUITE`), so a constructed walk can be run alone.

## D. A friction stub that could not be written (`tools/vm-qa`)

`vm-qa` ran `tools/friction-stub … > /dev/null 2>&1 || true`, so a refused stub vanished. The constructed runs above were themselves an example: `FRICTION_STUB_LOG` named a file that did not exist, the stub refused it with exit 2, and nothing said so.

A `frame-diff` failure against a stub baseline:

- **Stub log missing:** `vm-qa: the run's friction stub was not written (want a line in the friction log): friction-stub: no friction log at …` (`D-stub-missing.out`).
- **Stub log present:** the stub's line is written there (`D-stub-present.out`, `D-friction-scratch.log`).

No constructed run wrote to `docs/friction-log.md`.

## Not yet done

- **`raofflineproxy-lifecycle-test:455`** (`|| exit 1` with no FAIL line) exists only on the round, and the round must not move now. That fix lands with the round's next move.
- **#1506's criteria 1 to 3 remain open:**
  - criterion 1 is the remaining "partly" rows of the audit;
  - criterion 2 is a failed suite's `<suite>-guest/` folder;
  - criterion 3 is a failed suite's re-run classification.

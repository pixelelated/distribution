# Research notes — M6.P2 T12, the VM harness (#659)

## Scope

- **The read hash:** `8ebaf8daad`. The 60 are read from its bytes, in the export `.qa-scratch/t12/at-hash/`. `reviewed-at` is `facb2ae523`, the branch `HEAD` at stage A, whose 60 paths equal the hash's: `tr '\n' '\0' < .qa-scratch/t12/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD --` is empty.
- **The filter:** brief § 2's block over `docs/reviews/inventory.json` (P1's `2174265e9c`). The area is `tooling-and-guards`; the names are `vm-*, vm-walks/**, frame-diff, time-to-play, emulator-exit-test, es-launch-memory, signin-memory, png-blackout, qa-accounts, ra-*, raofflineproxy-*, device-act, es-syntax-check, es-untranslated, font-stems`. Its output:

```
paths 60 lines 8790 {'fork-own': 60} {'n/a': 60} {'shell': 10, 'python': 20, 'markdown': 2, 'other': 22, 'text': 3, 'image': 3}
the glob also selects, in other areas: 0 paths (expect 0)
```

- **The counts,** equal to the brief:
  - 60 paths and 8,790 lines, all 60 fork-own;
  - 20 Python, 10 shell, 22 `.steps` (`other`), 3 text, 2 Markdown, 3 PNG (`image`);
  - reach `n/a` 60.
  - Bytes: 484,627 (`git cat-file -s` summed).
  - `wc -l` at the hash sums to 8,813: the three PNGs hold 23 newline bytes, and the inventory stores no line count for an image. The per-path list is `.qa-scratch/t12/lines-at-hash.txt`.
- **Provenance:** none of the 60 is on `upstream/next` (`git cat-file -e` fails for each). There are 145 fork commits since `c445081a59` (144 without merges).
- **The branch against the hash:** empty over the 60.
- **The interacting subsystems** (read-only context):
  - the image under test;
  - the cloud suites and `tools/cloud-test-backend` (another slice's);
  - `register-check`, `vocabulary-check` and `es-menu-map-check` (called by `vm-qa`);
  - the host's memory (`device-builds.md`);
  - the M7 lane's guests (the host file);
  - the fork CI (`fork-checks.yml:45-48`).

## Phase 1: what each tool is

Each tool is described from its own header and code at the hash (the export), in the slice's words. Who calls it, what it costs and what it has caught are `04` § Q5 and § Q6.

**The runner and the pair:**
- **`vm-qa`:** the runner. It has 17 suites in one `SUITES` list (`:63`). The default is all of them except `link` and `ra-offline` (`:64`). It writes one report under `$ROCKNIX_ARTIFACTS/rocknix-images/qa-<build>-<backend>-<guest>-<minute>/`, and it exits non-zero only when a suite FAILs. A rc-3 SKIP does not change the exit (`:141-148`, `:541`).
- **`vm-pair`:** two guests from one image, each with its own MAC, ports and pidfile. It stops a guest through `vm-stop` by pidfile and owned disk (`:124-130`), and after launch it checks that the started PID owns its disk (`:81-95`). Its disks go in `$VM_PAIR_DIR`, by default `/tmp/rocknix-vm-pair`.
- **`vm-stop`:** stops the QEMU whose pidfile names it and whose command line owns the given disk. It uses a pidfd, re-checks the process's identity before signalling, waits up to 20 s by default (at most 60), and on a timeout keeps the pidfile and exits 1.
- **`vm-serial`:** a root shell over a headless guest's serial socket: `sh`, `script` and `wait --up-to`.

**The walks and the frames:**
- **`vm-visual-qa`:** drives a guest through a `.steps` file over the QEMU monitor (`sendkey`, `screendump`, or VNC when the monitor has no surface).
  - `settle` and `wait-for-change` watch the framebuffer. An eaten key is re-sent once, then the walk fails with exit 3.
  - A failed screendump only warns (`:524-530`).
- **`frame-diff`:** compares every PNG of a run with the accepted baseline's.
  - Every changed pixel outside `masks.txt` must lie inside a live claim in `claims.txt`. A MISSING frame, an UNCLAIMED box or a size change is a FAIL.
  - Exit 0 pass, 1 fail, 2 with no `BASELINE.txt`. `accept` moves the previous baseline aside and keeps it.
- **`png-blackout`:** paints a rectangle of a PNG black, stdlib only.

**The measurements:**
- **`time-to-play`:** two numbers, a game's first frame from the interface and the next game's first frame from an exit, beside the exit sync's stamp, on one guest.
  - `headline_missing` fails a run whose cells ran without their numbers. `over_budget` fails an exit-sync median over D-CLOUD-119's 3 s.
  - `--quick` (the runner's form) is one repeat of launch, exit and g2g. `--vm` sets RetroArch to GL and restores it after.
- **`signin-memory`:** the cloud sign-in window's peak memory on a guest. It is a FAIL unless the window, its web process and the page's load-finished line were all seen.
- **`es-launch-memory`:** EmulationStation's VmSize and RSS growth over N launch/exit cycles. Its acceptance needs both bounds (`:39-42`); without them it reports only.
- **`font-stems`:** stroke and stem measurements of a widget face per pixel size, on FreeType, on the host.

**The cloud, the exit and the upgrade:**
- **`emulator-exit-test`:** checks the exit hotkey: A, one press ends the game with the save written; B, a held combo ends it once; C, the debounce window; D, no marker left behind. It uses a synthetic Game Boy ROM.
- **`vm-upgrade-rehearsal`:** boots the previous image, seeds state, updates in place to the new tar, checks each piece of state, and writes `RESULT PASS|FAIL` under `/workspace/artifacts/rocknix-images/`.
- **`vm-upgrade-readiness-test`:** the rehearsal's storage-readiness wait and guest query against disposable fixtures. The fork CI runs it.

**The offline achievements:**
- **`ra-offline-test`:** the offline RetroAchievements scenario end to end on a QA guest (#166), with `--control` for #162's loss. It is opt-in in `vm-qa`.
- **`ra-ui-test`:** the installed reconnect cards with local fixtures, and full-panel frames (#465).
- **`ra-candidate-games`:** which homebrew titles have cheap achievements, and whether a ROM carries its set.
- **`raofflineproxy-integration-test`:** the shipped preparation helper against an unpacked patched proxy source (#361).
- **`raofflineproxy-consent-test`:** installed reporting consent, in an isolated guest with no default route.
- **`raofflineproxy-installed-native-test`:** upstream's format tests against the installed modules and native library. Any skip is refused.

**The interface's sources:**
- **`es-untranslated`:** the fork's interface strings without French, against the upstream base derived each run. It is rc 1 while any remain, and rc 2 when it cannot read the checkout or the base.
- **`es-syntax-check`:** one EmulationStation file compiled syntax-only with the image build's own command. It exits 2 without a build root, and its default root (`:53`) is a legacy path.

**Accounts and devices:**
- **`qa-accounts`:** carries a QA account from `~/.ROCKNIX/qa-accounts` into a guest on ports 10022 to 10029 without printing it. It is read here, never run.
- **`device-act`:** one command on a person's device over SSH, recorded with the boot id before and after in `/workspace/artifacts/rocknix-device-actions.log`. It is read here, never run (D-QA-015).

**The controls:**
- **`vm-pair-test`:** `vm-pair`'s launch functions with controlled failures; 9 controls. The fork CI runs it.
- **`vm-stop-test`:** delayed exit, a self-removed pidfile, a timeout, the wrong disk and the wrong process; 7 controls.
- **`vm-manager-system-check`:** refuses a manager walk whose requested system is missing, hidden, empty or not selected. It takes two arguments and stdin; its checks are `assert` statements.

**`tools/vm-walks/`:**
- **`suite.txt`:** 16 walks and a `default-pre` reset, each a composition of legs with an optional guest command before the reboot.
- **`claims.txt`:** 391 claim lines, every one against baseline `d72084ccad`.
- **`masks.txt`:** 7 masks.
- **22 `.steps` files:** 14 are legs `suite.txt` replays; the rocknix.org walks are under `docs/`; `m7-*` are M7's hand walks; `reset` and `wake` are utility legs.
- **`fixtures/`:** the three PNGs that `vm-qa`'s manager fixture copies onto the guest, and `system-selected.sh`, the hook a manager walk installs.
- **`cloud-epic/`:** `migration-protocol.sh`, sourced by `rasteratops-vm-cloud-epic`, which refuses without `cloud_migrate_layout`; and `vnc-grab.py`, a cadenced VNC frame grabber.

## The no-guest controls' baseline

The no-guest controls are recorded in `00` § Stage A: three controls rc 0, `vm-qa --list` with 17 names, the usage lines, and `es-syntax-check` rc 2, which is not a pass.

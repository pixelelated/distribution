# Running log: M6.P2 T14, the last-good, settings and state tests (#661)

- **Executor:** Opus 5.5 at high effort (`claude-opus-5-5`), the T3 session (`m6-t3-emulators`), under the coordinator's dispatch on #661 (2026-10-24 20:16 UTC).
- **Brief:** `docs/reviews/briefs/tooling-state-tests.md` version 2 (`27d8942071`).
- **Depth:** Independent: one GPT-6 Astra seat at `max` through the Facilitator.
- **Branch:** `feature/m6-tooling-state-tests-661` at `30da4853bb` (stacked on P1's `2174265e9c`), pushed with upstream `origin/feature/m6-tooling-state-tests-661`.
- **`reviewed-at`:** `30da4853bb`, the branch `HEAD` at stage A. It names both read hashes: `8ebaf8daad` for the 22 tools and fixture, `2174265e9c` for the ten lint fixtures. The branch differs from neither on the 32 paths.
- **Temp roots:** `TMPDIR=/workspace/tmp/m6-t14/tmp`; outputs under `/workspace/tmp/m6-t14/` and `.qa-scratch/t14/` (gitignored).

## [Stage A] 20:18 to 20:25 UTC — scope, the host and the host-side runs

### The brief's first commands (20:18:18Z)

- `git fetch origin && git fetch upstream --no-tags`: rc 0. The branch is `feature/m6-tooling-state-tests-661`.
- `git merge-base --is-ancestor 2174265e9c HEAD`: stacked on P1. `docs/reviews/inventory.json` is present.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`: exactly the dispatch's eight paths (`device-builds.md`, `engineering-practices.md`, `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, the code-auditor `templates.md`, the council `IMPORTED-FROM.md`, `tools/lint-audit-artifacts`), 8 files, +127/-11.
- **The host file's last line:** `== M6 T12 lane (#659) -- 2026-10-24T19:30:19Z: the cycle is done. tools/vm-stop rc 0 in 0.25 s (pid 1439420 gone, pidfile removed); the isolated QA cloud down; census qemu 0. ...`
- **The census:** `pgrep -c -x qemu-system-x86` prints 0. `df -i /tmp`: 418,000 of 1,048,576 inodes used (40 %); nothing here is exported under `/tmp`.
- **Build roots under the M6 worktrees:** 20 `build.*` directories, and **no busybox in any** (`image/system/usr/bin/busybox` and `build/busybox-*/.install_pkg/usr/bin/busybox`: 0 matches).
- `tools/rules-check --quiet`: rc 0. `tools/register-check`: `676 IDs, each once; every citation in the live documents names a row`.
- `git push -u origin feature/m6-tooling-state-tests-661`: the upstream is set.

### Scope (brief § 2's block)

- **Membership:** 32 paths, 6,911 lines. Tier `fork-own` 32; reach `n/a` 32; 20 Python, 2 shell, 10 Markdown. The globs select 0 paths in other areas. The list is `.qa-scratch/t14/paths.txt`; the per-path line counts at the read refs, `.qa-scratch/t14/lines.txt`, also total **6,911**.
- **The branch against the read hashes:** the 22 against `8ebaf8daad`, and the ten lint fixtures against `2174265e9c`. Both `git diff --stat` runs are **empty**.
- **Provenance:**
  - `git log c445081a59..8ebaf8daad` over the 22 gives **35** commits, 35 without merges.
  - `git cat-file -e upstream/next:<path>` fails for **all 32**.
  - The ten lint fixtures are absent at `8ebaf8daad` (10 of 10).
  - T10's delta to `tools/test-fixtures/lint-audit-artifacts/` is `2444828e89` (#945, on `feature/m6-tooling-guards-657`), read as a delta, not a member.
- **The exports:** `.qa-scratch/t14/at-hash/` (22 files, **394,711 bytes**) and `.qa-scratch/t14/at-p1/` (10 files).

### The host-side runs (20:18:54Z onward; `TMPDIR=/workspace/tmp/m6-t14/tmp`; each command's output in `.qa-scratch/t14/<name>.out`)

| Command | Exit | Wall | Summary |
| --- | ---: | ---: | --- |
| `tools/wait-lock-test` | 0 | 7.5 s | `PASSED` |
| `tools/rocknix-info-test` | 0 | 0.5 s | `PASS 12 full-script positive/negative controls` |
| `tools/nova-led-test` | 0 | 0.2 s | `14 PASS, 0 FAIL` |
| `python3 -I tools/usb-gadget-test --output .qa-scratch/t14/out/usb-gadget` | 0 | 0.3 s | `PASS USB descriptor fixture: 18 cases, 72/72 checks` |
| `python3 -I tools/pixelelated-state-check-test --self-test` | 0 | 9.1 s | JSON `status: pass`, `control_count: 183`, every control `pass`. `--payload-tests` needs `mksquashfs`, `unsquashfs`, `sfdisk` and `mcopy`; `mcopy` is absent on this host, so it is **CANNOT** and was not run |
| `python3 -I tools/build-identity-test --output .qa-scratch/t14/out/build-identity` | **1** | 0.2 s | `FAIL build identity: 21 passed, 2 failed`. The two checks are below |
| `python3 -I tools/retroarch-wrapper-test <source>` | 0 | 0.1 s | `PASS: every command ran exactly once`. The source was read only from the M7 root `m7-pixelelated-replacement20`'s `build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf/gfx/video_thread_wrapper.c`. **It left `tmpi9wqx8u7/t` and `t.c` in `TMPDIR`** |
| `python3 -I tools/retroarch-wrapper-test` (bare) | **2** | — | `no video_thread_wrapper.c given and none under /workspace/repos/rocknix.worktrees/devi...` (#640's roots) |
| `tools/rasteratops-identity-check --tree <worktree> --es <export>` | 1 | 0.1 s | 6 failures, against an export of the two ES files it names. It reads more files than those, and the ES commit from git, so this run is **not a verdict**; the rerun below is |
| `tools/rasteratops-identity-check --tree <worktree> --es /workspace/tmp/m6-t14/es-clone` | **1** | 0.1 s | `identity source contracts: 1 failure(s)`: 38 PASS, and `FAIL ES licence matches its source`. The clone is `--shared --no-checkout` of `~/Development/emulationstation-next`, at the pin `16dbac521`, under `/workspace/tmp/m6-t14/` |
| `settings-modes-test` (image busybox) | 0 | 0.4 s | `PASS refuse-rename` |
| `melonds-upgrade-test` (image busybox) | 0 | 0.1 s | `PASS temp-failure` |
| `settings-modes-test` (host busybox) | 0 | 0.4 s | `PASS refuse-rename` |
| `melonds-upgrade-test` (host busybox) | 0 | 0.1 s | `PASS temp-failure` |
| `rasteratops-cloud-layout-test --source-root <wt> --rclone <image rclone> --output ...` | 1 | 0.1 s | `AssertionError: migration matrix retired by #508; use --ref ... or --archives-only` |
| the same with `--archives-only`, as T15's call passes it | **1** | 9.2 s | `11 PASS, 2 FAIL`: `T24-local-legacy-recovery` and `T24-local-renamed-recovery`, `restore rc=1` with `>>> why COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS` |
| `pixelelated-cloud-validator-test --rclone <image rclone> --output ...` | **1** | 0.1 s | `AssertionError: Use the package-pinned rclone1.75.1, not the host fallback: rclone v1.75.2` |
| `pixelelated-content-scope-test --source-root <wt> --rclone <image rclone> --output ...` | **1** | 3.4 s | 19 PASS, 2 FAIL: `system-traversal-refused` and `content-pointer-traversal-refused`, `[Errno 2] No such file or directory: .../ctl/argv` |
| `pixelelated-save-layout-test --source-root <wt> --rclone <image rclone> --busybox <image busybox> --output ...` | 0 | 29.2 s | `save-layout: 39 PASS, 0 FAIL` |
| `pixelelated-duckstation-capture-test --source-root <wt> --rclone <image rclone> --output ...` | **1** | 0.1 s | `AssertionError: use package-pinned rclone: rclone v1.75.2` |
| `tools/pixelelated-cloud-folder-test` (bare) | 2 | — | `Retired historical folder-contract control (#524 PL-002).` |
| `tools/pixelelated-cloud-folder-vm-test` (bare) | 2 | — | `Retired historical folder-overlay control (#524 PL-002).` |
| `tools/rasteratops-vm-cloud-epic` (bare) | 2 | — | `This migration suite is retired. Use a historical source checkout for historical firmware; #508 qualifies manual cloud setup.` |

`--help` exits 0 for the other eight: `pixelelated-duckstation-capture-test`, `melonds-upgrade-test`, `settings-modes-test`, the real-rclone four, `rasteratops-candidate-store`, `pixelelated-state-check` and `pixelelated-vm-cloud-boundaries`. Their usage lines are in `.qa-scratch/t14/help.txt`.

**The binaries the runs used:**
- **busybox:** none under the M6 roots. The image's copy is from the M7 root `m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/busybox` (`BusyBox v1.36.1 (2026-10-05)`, sha256 `79e7b20ddbe5abb6d186...`), read only and copied to `/workspace/tmp/m6-t14/busybox-image`. The host's is `/usr/bin/busybox`, `BusyBox v1.37.0 (Ubuntu 1:1.37.0-7ubuntu1)`, copied to `/workspace/tmp/m6-t14/busybox-host`.
- **rclone:** the recipe pins `PKG_VERSION="1.75.2"`. The image's copy is from the same root, `rclone v1.75.2`; the host's is `/usr/bin/rclone`, `rclone v1.60.1-DEV`. No 1.75.1 binary exists on this host (both GENERIC_X64 roots hold `build/rclone-1.75.2`).
- **The real-rclone four's binding, read before any run:**
  - each runs its scripts under `bwrap` with `--tmpfs /`, read-only `/usr` and `/etc`, the fixture's `storage` bound as `/storage` and `HOME=/storage`;
  - its `rclone.conf` is the fixture's (`[qa] type = alias`, `remote = /cloud`), and the binary is bound as `/rclone.real`;
  - the host's home is never mounted;
  - `env | grep -c '^RCLONE'` is **0** in this shell, so `bwrap`'s pass-through of the environment carried no remote definition.

**The two `build-identity-test` failures** (from its JSON, `.qa-scratch/t14/out/build-identity`):
- `rc1 public plan accepted: PASS candidate bundle .../pix-build-identity-.../420ec4ab... release preparation: selected-state inspection refused a firmware asset`;
- `harness completed`, the same error.

`synthetic_only: true`, `assembled_image_tested: false`.

**The `rasteratops-identity-check` failure:** the check expects `PKG_LICENSE == "MIT"`. The ES recipe reads `PKG_LICENSE="MIT AND BSD-3-Clause"`, unchanged at `8ebaf8daad`, since `84ff94fb3d` (2026-10-13, *emulationstation: prepare RVZ hash dependency and evidence*). The check's last change is `7d64713537` (2026-10-04).

**The rclone pin:** `pixelelated-cloud-validator-test:58` and `pixelelated-duckstation-capture-test:178` require `version == 'rclone v1.75.1'`. The recipe moved to 1.75.2 at `a0f60255ab` (2026-10-11, *network: refresh dependencies before the combined M7 build*). Both tests were last changed at `bc4ae05d30` (2026-10-08).

### The three greps (brief § 5)

- **`|| true`** over the 21 tools: **0** lines.
- **`^\s*assert `:** 2 files, `tools/nova-led-test` (1) and `tools/pixelelated-vm-cloud-boundaries` (1).
- **Host paths** (`/tmp/`, `HOME`, `rocknix.worktrees`, `/workspace/repos/rocknix`): **28 lines in 10 files** (`.qa-scratch/t14/hostpaths.txt`):

  | File | Lines |
  | --- | ---: |
  | `rasteratops-vm-cloud-epic` | 9 |
  | `rasteratops-cloud-layout-test` | 5 |
  | `pixelelated-cloud-validator-test` | 2 |
  | `pixelelated-duckstation-capture-test` | 2 |
  | `pixelelated-vm-cloud-boundaries` | 2 |
  | `rasteratops-identity-check` | 2 |
  | `retroarch-wrapper-test` | 2 |
  | `wait-lock-test` | 2 |
  | `build-identity-test` | 1 |
  | `rocknix-info-test` | 1 |

  These match the stranger's proof: 0, 2 files, and 28 lines in 10 files.

### What stage A found before any reading

Five tests do not pass at the hash with the package's own inputs:
- `build-identity-test` (the brief's known stage-D bug);
- `rasteratops-identity-check` (a licence string the recipe moved past);
- `pixelelated-cloud-validator-test` and `pixelelated-duckstation-capture-test` (an rclone version the recipe moved past);
- `rasteratops-cloud-layout-test --archives-only` (2 FAIL);
- `pixelelated-content-scope-test` (2 FAIL).

The last two are traced at stage B before they are called defects: an environmental cause (an applet the sandbox lacks on this host, a `/usr` tool absent) is a dependence row in Q6, not a code bug, until the trace says which. `retroarch-wrapper-test` leaves `t.c` in its temp root.

- **Host footprint after the runs:** `/workspace/tmp/m6-t14/` holds 173 MB (the ES clone, the rclone and busybox copies, the outputs). `TMPDIR` holds only the wrapper test's `tmpi9wqx8u7/`. `git status --short` is clean.
- **No guest:** the census is 0 throughout. No handheld, no real provider or account, no build, no edit to `tools/last-good-scripts-test`, no write under `/tmp` or `/workspace/repos/rocknix*` (the M7 roots were only read and executed from).

## [Stage B] 20:29 UTC — the two traces; the coordinator's busybox ruling

- **The coordinator's post (20:28 UTC):** the busybox copied read-only from the M7 GENERIC_X64 root's image is a build root's applet set, recorded with the root, its BUILD_ID and the pin; the host's run is recorded as the host's. The four failing tools are stage-D bugs, and the two traced cases stay dependence rows until the trace says otherwise.
- **The applet set:**
  - **The root:** `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64`, image `BUILD_ID="1a026648442321609b2288c2c9c06803817f9df2"`, `VERSION="0.0.1-dev+20261011T194522Z.g1a0266484423"`, `BUILD_BRANCH="build/m7-pixelelated-replacement20"`; its `build/busybox-1.36.1`; the binary `BusyBox v1.36.1`.
  - **The tree's effective pin** is `projects/ROCKNIX/packages/sysutils/busybox/package.mk:7` `PKG_VERSION="1.36.1"`, the override. The generic `packages/sysutils/busybox/package.mk:6` reads `1.38.0`, and the override wins (`device-builds.md` § After rebasing: the effective version). So the root's binary is the tree's pin.
  - **The host's:** BusyBox v1.37.0 (Ubuntu). Both writer tests passed under each, and the second pass is recorded as the host's.
- **Trace 1: `rasteratops-cloud-layout-test --archives-only`, the two `T24-local-*-recovery` FAILs.**
  - The case's logger journal (`ctl/journal`) reads `a temporary file could not be made (mktemp failed or gave no file)`, then `the restore's lists could not be made (a temporary file)`.
  - The sandbox (`:138-146`) mounts `--tmpfs /tmp`, sets `HOME` and `PATH` with `--setenv`, and otherwise passes the caller's environment through `bwrap`. The caller's `TMPDIR=/workspace/tmp/m6-t14/tmp` is not mounted inside, so `backuptool`'s `mktemp` fails.
  - **Rerun with `env -u TMPDIR`** (the test makes no host temp when `--output` is given, `:1201`; the host's `/tmp` held 9,562 entries before and after): `13 PASS, 0 FAIL`, rc 0, 19.8 s.
  - **The cause is the test's sandbox,** which inherits a caller variable that names a host path. It is not the scripts. A caller that sets `TMPDIR` as `device-builds.md` § Temporary directories (#549) asks gets a false FAIL.
- **Trace 2: `pixelelated-content-scope-test`, `system-traversal-refused` and `content-pointer-traversal-refused`.**
  - Unchanged with `TMPDIR` unset: 19 PASS, 2 FAIL.
  - The current `cloud_content_restore` refuses `../gb` before any rclone call (`02-cloud_content_restore.log`: `That system folder name can't be used. Nothing was restored.`), so the case's `ctl/` holds no `argv`.
  - The cases read `ctl/argv` unconditionally (`:121`, `:222`), and the read raises `[Errno 2]` before their assertion. The sibling cases at `:178` and `:195` already test `not exists()`.
  - The refusal moved earlier at `e6645cb5ea` (2026-10-08 07:19Z, *cloud: integrate explicit folder setup and save coverage*), five hours after the test's last commit `083f4fad86` (02:25Z).
  - **The cause is the test,** stale against a safer script. The property it protects (no transfer started) holds; the test reports FAIL over it. Nothing calls this test, so the failure has gone unseen since that day.

## [Stage B] 20:32 UTC — the 20:31 ruling; the read fanned out

- **The coordinator's post (20:31 UTC):** both traces are accepted as test defects; the busybox correction stands (the override's 1.36.1 is the effective pin); the two rclone-pin tests are one bug. The post says *six stage-D bugs*. The defects are six: `build-identity-test`, `rasteratops-identity-check`, the two rclone-pin tests, cloud-layout's `TMPDIR` inheritance and content-scope's stale read. Issued one bug per shape, that is **five bug issues**. The count is confirmed at stage D.
- **The read, fanned out:** two read-only research agents read the 21 tools for Q6's four columns and Q3's shapes, eleven and ten tools each, with no tool run and no file written. Their leads are re-derived here before they enter `04`.
- **Written:** `02` § Phase 2, § The runs (every stage-A run with *a FAIL would mean*) and § T15's call sites.

## [Stage B] 20:42 UTC — the constructed inputs; the guest question; the proofs

- **Constructed 1, `rocknix-info-test` under `python3 -O`** (`/workspace/tmp/m6-t14/q3-info/`, a scratch root): the tool is copied, beside a copy of `rocknix-info` with `exit 0` appended (a quirk failure that no longer propagates). The plain run gives rc 1, `AssertionError: real quirk failure survives later success`. Under `python3 -I -O` it gives **rc 0, `PASS 12 full-script positive/negative controls`**, and its own `result.json` lists `real quirk failure survives later success` as failed.
- **Constructed 2, `pixelelated-cloud-validator-test --case no-such-case`** (`/workspace/tmp/m6-t14/q3-validator/`): a copy whose only change is `:58`'s version literal, 1.75.1 to 1.75.2, so it gets past the stale pin (`diff` shows the one line), beside the rclone sources. It gives **rc 0, `PASS 0 controls`**, and `result.json` reads `result: PASS`, 0 cases.
- **The guest question.** Can this be done on the VM? **Not needed.** Both guest tests refuse before any guest on this tree:
  - `pixelelated-vm-cloud-boundaries:709-710` requires `.../sources/cloud_migrate_layout`;
  - `rasteratops-vm-cloud-epic:22-25` refuses without it, rc 2 (the bare run in `00` § Stage A);
  - `git cat-file -e 8ebaf8daad:projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout` fails.

  A cycle would only show the refusal. The two tests' find, wait and stop paths are classified from the source (`04` § Q3). The authorized cycle was not used; the census stays 0.
- **The research passes** (two read-only agents, no tool run, no file written): every lead that entered `04` was re-read at its line or reproduced. Two were withdrawn or demoted (`04` § Finding Verification). One claim was corrected against `00`: the pass said the payload controls passed, where `00` records `--payload-tests` as CANNOT.
PROOF: P1 the membership -- brief § 2's block: 32 paths, 6,911 lines, 32 fork-own, reach n/a 32, 20 Python, 2 shell, 10 Markdown, 0 in other areas; both read-hash diffs empty; 35 commits; none upstream (`00` § Stage A).
PROOF: P2 the host-side runs -- every stage-A run with its exit and wall (`00` § Stage A, `.qa-scratch/t14/runs.txt`): five tools fail at the hash with the package's own inputs, the rest pass, the stubs and the epic refuse.
PROOF: P3 the two traces -- cloud-layout `--archives-only`: 2 FAIL with `TMPDIR` set, 13 of 13 unset; content-scope: 2 FAIL either way, the script refusing `..` before rclone (`00` § Stage B).
PROOF: P4 rocknix-info-test under -O -- a constructed regression: plain rc 1, `-O` rc 0 `PASS 12`, `result.json` listing the failed case.
PROOF: P5 the validator's empty selection -- `--case no-such-case`: rc 0, `PASS 0 controls`, `result: PASS`.
PROOF: P6 the guest pair refuses on this tree -- `cloud_migrate_layout` absent at `8ebaf8daad`; the boundaries test's require (`:709-710`) and the epic's refusal (rc 2).
PROOF: P7 the thirteen no-caller tools -- `git grep -n -F <name> 8ebaf8daad -- tools .github/workflows .claude/skills .githooks`, per tool: no invocation for thirteen; T15's four call sites and `vm-qa:185` and `fork-checks.yml:50` for the rest.
PROOF: P8 the index and its rules -- `instruction-files.md` at the hash: 21 of 21 rows; 13 whose *Detail in* rule never names the tool (the per-tool loop over the index and each rule at the hash; its output `.qa-scratch/t14/q7-index.txt`, 13 lines ending `naming it: 0`).

## [Stage C] 20:46 UTC — the seat: the Facilitator, the packet, the probe, the refutation started

- `npm install --prefix tools/council`: rc 0. It warned that install scripts were not run, as in the earlier slices.
- `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` `tools/council/run test`: rc 0, with 39/39, 127/127 and 19/19 passing and 0 failing. `run` sources `~/.config/council/env` itself; the file was not read here.
- **The packet** (`tools/t14-packet.py`, manifest `second-opinions/packet-manifest.json`): 38 sources, the 32 files among them at **396,588 bytes**, as the brief says, each with its sha256 at its read ref. The rest:
  - `02`, `03` and `04` whole;
  - `engineering-practices.md` § Guards must fail closed and `upgrade-and-install.md` § Verify on a device, not on the host, from `next`;
  - the stage-A run lines.

  The body is 510,784 bytes. `gpt-brief.md` is the ask plus the body, 513528 bytes, sha256 `6ce0b2e7362c71a69cde3ea1e1f1c1d09716c706f03198b8e254ab7c0862a3e6`. The ask puts the brief § 5's four questions first.
- **The packet's scan, before it was sent:**
  - `tools/forbidden-terms-check --stdin`: `0 hits on stdin`.
  - The pre-commit's `SECRET_PATTERNS` (`/usr/bin/grep -a -c -E`): **0 lines** under each of three pattern sets (this branch's `.githooks/secret-patterns`, the primary checkout's, and T10's widened copy on `feature/m6-tooling-guards-657`).
  - No redaction was needed.
- **The probe**, 20:45:38 to 20:45:47Z, `--member gpt --provider openrouter`, the one-line prompt: served `openai/gpt-6-astra` by `OpenAI`, effort `max` (230 reasoning tokens). Identity source `provider_response`; verification PASS (semantic), effort PASS, provider PASS. The model's own reply was `READY unknown`; the provider's field is the identity.
- **The refutation** started with `--per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000`, its log `/workspace/tmp/m6-t14/audit.log`.
  - **What watches it:** the harness background task that runs it, which delivers its end.
  - **Its silent mode:** a hung seat is ended only by those timeouts. The failed-seat rule holds: hold, diagnose, one same-slug retry on a transient cause.

## [Stage C] 21:05 UTC — the 21:03 ruling, while the seat runs

- **The coordinator's answer on #661 (21:03 UTC):**
  - one `Renovation` item for the no-caller class, with the nine tools named (T12's PL-19 shape; the Backlog is #986);
  - the six broken-and-unseen tools each a `bug` of its own;
  - the two stubs a separate disposition.
- **One conflict, to raise at the stage-D pause, not to resolve here:** F-11's six broken-and-unseen tools include the two rclone-pin tests, which the 20:31 ruling made one bug, and the guest pair. The pair refuses because #508 retired the migration it proves; that refusal is by design, which makes it a disposition beside the stubs rather than a defect. Until the coordinator answers, `05` drafts them as the 20:31 ruling and F-10 read.

## [Stage C/D] 21:19 UTC — the seat's return and grading; the punch list; the issues; the stage-D pause

- **The refutation returned** (`/workspace/tmp/m6-t14/audit.log`): 20:46:18Z to 21:11:19Z, attempt 1 of 4, `finish=stop`, 47,033 bytes.
  - **Tokens and time:** 146,499 prompt and 61,214 completion (50,762 reasoning), 1,501,038 ms, 0 retries.
  - **Served:** `openai/gpt-6-astra` by OpenAI at `max`; verification (semantic), effort and provider PASS.
  - **Scanned before it was read:** `forbidden-terms-check --stdin` 0 hits, and 0 credential-pattern lines.
- **The grading** (`04` § Second opinion): 42 items, G-1 to G-42.
  - **Re-read in this session at their lines:** G-1, G-2/G-13, G-9, G-19, G-20 (and T15's fake `subprocess` at `last-good-scripts-test:5062-5067`), G-24 to G-29, G-34, G-35, G-38, G-39 and G-40.
  - **G-15's caller count rerun** for the validator (`.qa-scratch/t14/validator-callers.txt`): three mentions, no invocation.
  - **Result:** 37 confirmed or confirmed-with-narrowing; 4 accepted as corrections to the first reader (F-10, F-11, F-12 and F-15 revised, F-15 withdrawn); 1 left conditional (G-42).
  - **Raised:** F-04 to High and F-09 to Medium.
- **The punch list** (`05`, generated by hand from the graded items, `tools/t14-bugs.py` for the bug bodies): 23 items, 0 Critical, 1 High, 15 Medium and 7 Low.
  - **Bugs:** 17 (#989 to #1005), every body scanned before filing (0 hits, 0 credential-pattern lines under two pattern sets). Each passes `tools/box-check --issue N` with 0 fail.
  - **For the coordinator:** 5 Renovation items (PL-09, PL-10, PL-11 into #986, PL-12, PL-17) and 1 conditional (PL-23).
- **The audit issue:** #1006, `Audit: M6 T14 the state tests -- 23 findings (0 critical, 1 high)`, labels `audit` and `punch-list`, milestone M6, a sub-issue of #661 (read back: `1006`). `box-check --issue 1006`: 23 open checkboxes, 0 fail.
- **`04` gained the five sections the lint requires.** `tools/lint-audit-artifacts <folder> --phase pre-issue`: `review plan: independent, 2 model perspectives, 1 verified external calls`, then `PASS pre-issue artifacts (does not certify resolution)`.
- **API budget** before the filing: core 4,939 and GraphQL 4,977.
- **The stage-D pause:** no file under `tools/` has changed on this branch. The lane waits for the coordinator's stream briefs.

## [Stage E] 21:37 UTC — S2: the shared sandbox and the connections fixture (#992, #999)

- **The dispatch** (#661, 21:30 UTC) and the stream brief (`docs/reviews/briefs/t14-streams.md` at `13242d182a`, read with `git show`, not merged):
  - PL-09 stays the disposition, and its kill after a refused start is a bug filed at S11;
  - PL-11's tenth tool is in both #986 and #994;
  - twelve streams, S2 first, and no guest in stage E.
- **The test first:** `docs/qa-logs/2026-10-24-state-tests-s2/sandbox-case.py`, run against `git archive 7aa8eac253 -- tools`, exported to `/workspace/tmp/m6-t14/export-D/`.
  - **Part A:** a probe script through `Fixture.run`.
  - **Part B:** the whole `--archives-only` run.
  - **What the caller exports in both:** `TMPDIR` (a host path), `RCLONE_CONFIG` (a stand-in, absent), an `RCLONE_CONFIG_QA_TYPE` remote, `BASH_ENV=/shim/logger` and an exported function.
  - **Part C:** the connections fixture with a real rclone copied to another path, on a stand-in `HOME`.
  - **Unfixed: 9 of 10 checks FAIL:**
    - all four variables and the function reach the script, and `BASH_ENV` is sourced;
    - `mktemp` fails, and the sandbox sees 39 network interfaces;
    - cloud-layout gives 0 PASS, 13 FAIL;
    - the fixture admits the copied rclone and writes the stand-in `HOME`'s default `rclone.conf`.
- **The fix:**
  - `2e6639ec57`: `SANDBOX_ENV` (`--clearenv`, `--unshare-net`, `LANG=C`, `TERM=dumb`, `TMPDIR=/tmp`) in `Fixture.run` and the validator's adoption sandbox.
  - `89efee384c`: the fixture admits real `subprocess` only for a non-ELF shim inside its own directory, and passes `--config`; the table fake's argv shape is unchanged.
  - **Fixed: 10 of 10:** nothing of the caller's inside; `TMPDIR=/tmp`; loopback only; cloud-layout 13 PASS; the copy refused and nothing written; T15's shim receives `--config <stage>`; the FakeSP shape intact.
- **The four under the same variables:**
  - cloud-layout 13/13 (part B);
  - save-layout `39 PASS, 0 FAIL`;
  - content-scope 19 PASS, 2 FAIL, the two traversal cases, which are S4's (#993);
  - the validator's adoption case: a scratch copy cannot supply the `git` history it reads, so it runs under the variables at S3, once the pin no longer refuses 1.75.2.
- **Bindings, read first (D-QA-058):** each of the four binds the fixture's local `/cloud` alias; none reaches the host's QA backend or a loopback service. So all four unshare the network, and none keeps it.
- **The lane's `~/.config/rclone/rclone.conf` mtime:** `2026-07-29 05:00:22.58Z` before and after (the mtime only).
- **For T15 (#662), through the coordinator:** the fixture's change keeps every argv shape T15's FakeSP and its authorize shim use (`last-good-scripts-test:5244-5250`, `:5062-5067`). T15's run was not repeated here.
PROOF: P9 S2's control -- `docs/qa-logs/2026-10-24-state-tests-s2/sandbox-case.py` with the caller's TMPDIR, RCLONE_CONFIG, an RCLONE_CONFIG_* remote, BASH_ENV and a function exported: at 7aa8eac253 9 of 10 FAIL (`.qa-scratch/t14/s2-unfixed.txt`), fixed 10 of 10 (`s2-fixed.txt`); save-layout 39/39 and content-scope 19/2 (S4's) under the same variables.

## [Stage E] 21:43 UTC — S1: the release identity tests (#989, #990); the 21:39 ruling

- **The coordinator's post (21:39 UTC):** `tools/last-good-scripts-test` runs once on the host before hand-back, read-only, with its exit, wall time and the resolved busybox recorded beside S2. T15's acceptance stays #662's.
- **`build-identity-test` (`3c9730bc78`).**
  - **The stand-in** is an update tar whose SYSTEM is a squashfs of `pixelelated-state-check-test`'s `clean()` root, built with its `make_tar()`, and this build's os-release. Without `mksquashfs` the run exits 2.
  - **Each refusal** checks its exit and reason. The reasons were read from a discovery copy under `/workspace/tmp/m6-t14/bi-root/` that printed each one: `build identity fields disagree`, `public release version must be ...`, `checksum file disagrees with manifest`, `bundle contains firmware without matching identity`, the store's `artifact does not match`, and the policy's and the image block's own messages.
  - **Positives:**
    - at `7aa8eac253`, from a full export (`/workspace/tmp/m6-t14/export-D-full/`): rc 1, 21 passed, 2 failed; fixed: rc 0, **57 passed** (1 s).
    - `identity-reasons-case.sh`: with the preparer, or the identity policy, refusing for a wrong reason, the fixed test fails (2 checks each), while the same test with `refused()` reverted to any non-zero credits it (57/57).
- **`rasteratops-identity-check` (`648e9ca228`).**
  - **The fix:** the licence is read from the recipe's expression (MIT from the ES `LICENSE.md`, and each further term from the named `ES_EXTRA_LICENCES`); `value()` reads the last assignment; an empty gamelist fails.
  - **The control,** `identity-check-case.sh` over scratch trees from `HEAD`:

    | Tree | Stage-D tool | Fixed tool |
    | --- | --- | --- |
    | the tree as is | FAIL | PASS |
    | an empty gamelist | PASS | FAIL |
    | a shadowed licence, `MIT` then `GPL-2.0` | PASS | FAIL, quoting `'GPL-2.0'` |

  - **On the tree,** with the ES clone at the pin: 0 failures.
PROOF: P10 S1's controls -- build-identity-test at 7aa8eac253 rc 1 (21/2), fixed rc 0 (57/57); `docs/qa-logs/2026-10-24-state-tests-s1/identity-reasons-case.sh` PASS (wrong reasons failed by the fixed test, credited by any-non-zero); `identity-check-case.sh`: stage-D FAIL/PASS/PASS, fixed PASS/FAIL/FAIL (`.qa-scratch/t14/s1-identity-check.txt`).

## [Stage E] 21:53 UTC — S3: the validator and the capture test (#991, #994, #998); the 21:44 ruling

- **The coordinator's post (21:44 UTC):** `build-identity-test` keeps CANNOT (exit 2, the reason named) without `mksquashfs`, and no gate double. Its `--help` names the requirement: `python3 -I tools/build-identity-test --help` prints a line with `mksquashfs`, 1 match.
- **#991 (`2f614eef1f`): the pin from the recipe, in both tools.**
  - **Positives:** at `7aa8eac253` both refuse 1.75.2 (`00` § Stage A). Fixed, with the image's 1.75.2: the validator passes 30 controls (16 s) and DuckStation 31 PASS (5 s). With a scratch recipe pinning 9.9.9, both refuse, naming the recipe and the version.
  - **S2's pending case:** the validator's full run under the caller's witness variables passes 30.
- **#994 (`6b5cd16160`): the validator's controls.**
  - **The fix:** an unknown or empty `--case` exits 2, and the control count is asserted. `request()` requires exactly the requested categories. The ROM seed requires its folder and note, the byte limit is fed valid JSON over 2 MiB, and the timeout is fed a listing that sleeps 12 s and fails, with the elapsed time asserted under 12 s. The receipt hashes the binary first.
  - **Two slips of mine in the fixture, each corrected before the commit:** the timeout inject first exited 3, which rclone means as "directory not found", so the listing read as missing; it now exits 5. The seed mutation first broke the script instead of making it a no-op.
  - **The control,** `validator-controls-case.sh`: four product mutations in scratch roots. The stage-D controls credit three of them (empty categories, a no-op ROM seed, a raised byte bound), and a state-only timeout check credits the fourth (a raised time bound). The fixed controls fail all four. `--case no-such-case`: rc 0 `PASS 0 controls` at stage D (P5), rc 2 fixed.
- **#998 (`fe41fca9a9`): DuckStation.**
  - **The fix:** the payload runs through `Fixture.run`, its shebang now `/bin/bash` because the sandbox binds no `sh`. The sandbox takes S2's `--clearenv` allowlist, and an unknown `--cases` name exits 2.
  - **The control,** `duckstation-case.sh`, with one named substitution: the payload also writes a host marker named by a caller variable. Stage D: the marker present (host execution), and the unknown name dropped (rc 0). Fixed: the marker absent, the case passes, and the unknown name gives rc 2.
- **Slip, and its fix:** my `sed` adding `import re` also matched a `from pathlib import Path` inside a script the test embeds as a string. That stray line was removed before the commit, and the full run reread: 31 PASS.
PROOF: P11 S3's controls -- #991: the stage-D refusals of 1.75.2, the fixed passes (30, 31), a 9.9.9 recipe refused; #994: `docs/qa-logs/2026-10-24-state-tests-s3/validator-controls-case.sh` PASS (four mutations credited by the old controls, failed by the fixed), `--case no-such-case` rc 0 then rc 2; #998: `duckstation-case.sh` PASS (host marker present at stage D, absent fixed; unknown name rc 0 then 2).

## [Stage E] 21:55 UTC — S4: content-scope (#993); the 21:54 ruling

- **The coordinator's post (21:54 UTC):** `#!/bin/bash` stays, and no `sh` is bound. The payload case's scope string now says what the witness proves (`802bb51924`). The receipt reads `... not the AppImage runtime: it proves the installed 0755 mode and direct execution inside the case sandbox`.
- **#993 (`6b41f05962`): what changed.**
  - **The traversal cases** assert the refusal sentence and that rclone was never run.
  - **The missing-\* cases** require a listing of the selected library.
  - **The failure cases** require the injected fault to have fired. The shim's `/ctl/fault-fired` records it, and the partial injection now writes there too.
  - **An unknown `--cases` name** exits 2.
- **#993: the evidence.**
  - **The tree:** fixed, 21 PASS, 0 FAIL; at `7aa8eac253`, 19/2.
  - **The control,** `docs/qa-logs/2026-10-24-state-tests-s4/scope-cases.sh`, with two product mutations in scratch source roots:
    - a script that lists remotes and exits 0: the stage-D missing cases pass it (rc 0), and the fixed ones fail it (rc 1);
    - the same exiting 1: the stage-D failure cases pass it, and the fixed ones fail it;
    - `--cases missing-list,no-such-case`: rc 0 at stage D, rc 2 fixed.
PROOF: P12 S4's control -- `docs/qa-logs/2026-10-24-state-tests-s4/scope-cases.sh` PASS (the stage-D test credits both mutations and the typo; the fixed fails them, rc 2 on the typo); the tree 21/0 fixed against 19/2 at the stage-D tip.

## [Stage E] 22:07 UTC — S5: cloud-layout and save-layout (#1004, #1005)

- **#1004 (`c25f69d19a`): the cloud-layout cases.**
  - **The legacy case** now requires a new archive: another name, other bytes, the restored sentinel inside.
  - **`settle_failure`** requires its `--settle` witness and a non-zero caller status.
  - **`provider_failure`** requires a restore's status to show the failure. A first cut required it of every script, which failed 7 historical backup cases. Read on the historical source, a backup whose layout read failed goes on into the configured folder, copies and reports `COMPLETED`, rc 0 by design. The requirement now covers restores only, with the reason in the code.
  - **Positives:** `layout-cases.sh` mutates three scripts in scratch roots: a `backup` that writes nothing, a `--seed-folders` that never settles, and a restore that swallows its listing failure (the last two at `22571b47d2`, the parent of `e6645cb5ea` and the last tree with `cloud_migrate_layout`). The stage-D test credits each, rc 0; the fixed one fails each.
  - **Fixed runs:** the tree's `--archives-only` 13/13; the whole historical matrix **398 PASS, 0 FAIL** (391 s).
  - **Not changed:** the migration reader-grammar cases (G-31, historical, Low).
- **#1005 (`15bce9aa23`): save-layout.**
  - **The fix:** the applets are required of a full run only, and the receipt lists the ref's own files.
  - **Positives,** in `save-layout-cases.sh`: `--busybox --cases filter-psp` and `--ref a1b0c65165 --cases filter-psp` both exit 1 at stage D and both pass fixed.
  - **The full suite:** 39/39.
PROOF: P13 S5's controls -- `docs/qa-logs/2026-10-24-state-tests-s5/layout-cases.sh` PASS (three mutations credited at stage D, failed fixed), `save-layout-cases.sh` PASS (rc 1 both at stage D, rc 0 fixed); the historical matrix 398/0 and the archive cases 13/13 fixed.

## [Stage E] 22:16 UTC — S5's follow-up (#1004) after the 22:08 ruling; S6: the hardware tests (#995)

- **The coordinator's post (22:08 UTC):** my reading of the backups is the historical contract, not a design question. A backup whose layout read failed exits 0, says `COMPLETED`, and copies into the configured folder, never a derived one; restores keep the non-zero requirement; the layout detection is retired by D-CLOUD-175, so no product change.
- **#1004's follow-up (`ef31b4bf22`):** `provider_failure` asserts that contract for a backup: rc 0, `COMPLETED`, and every `copy` target exactly `qa:/ROCKNIX/Saves/`.
  - **The control,** `docs/qa-logs/2026-10-24-state-tests-s5/backup-contract-cases.sh`, two mutations of the historical `cloud_backup` (`22571b47d2`) run with `--case T18-bucket-backup-unknown` by the test as committed at `c25f69d19a` and by the current one:
    - **silent** (makes the faulted listing, exits 0): rc 0 before, rc 1 after (no `COMPLETED`);
    - **derived** (the copy goes to `/pixelelated/Saves/`): rc 0 before, rc 1 after (`copied into ['qa:/pixelelated/Saves/'], not the configured /ROCKNIX/Saves/`);
    - the unmutated backup passes both. PASS.
  - **A slip of mine, corrected before the commit:** the first derived mutation changed the layout read at `:1671`, not the copy; it now changes the copy destination at `:1931`.
  - **The historical T18 set after:** 17 PASS, 0 FAIL.
- **#995: `rocknix-info-test` (`359dd435ce`).**
  - **The fix:** each adaptation pattern must be found in the script, or the run raises naming it; `check()` raises rather than asserting, so `PYTHONOPTIMIZE` cannot strip it.
  - **The control,** `docs/qa-logs/2026-10-24-state-tests-s6/info-cases.sh`:
    - a `rocknix-info` with `exit 0` appended, run under `PYTHONOPTIMIZE=1`: rc 0 at stage D (`PASS 12`), rc 1 fixed (`real quirk failure survives later success`);
    - `/tmp/battery.percent` renamed (a path the script only tests and reads): rc 0 at stage D, rc 1 fixed (`adaptation pattern not found in the script: /tmp/battery.percent`). PASS.
  - **A slip of mine, corrected before the control was kept:** the first rename was `/storage/games-internal`, which made stage D fail downstream for a different reason and so proved nothing.
  - **The tree:** `PASS 12`, rc 0.
- **#995: `nova-led-test` (`081f19d2f0`).**
  - **The fix:** a per-script adaptation table with every pattern required; the `LED_PATH` and `BATTERY_PATH` assignments must keep their `"${VAR:-` default, and no bare `/sys/` may remain; `run()` raises `SystemExit` rather than asserting.
  - **The control,** `docs/qa-logs/2026-10-24-state-tests-s6/nova-cases.sh`:
    - a `ledcontrol` with an EXIT trap exiting 3, under `PYTHONOPTIMIZE=1`: rc 0 at stage D (`14 PASS`), rc 1 fixed;
    - `LED_PATH` hardcoded to a stand-in tree under the scratch, every file seeded `untouched`: stage D ran it and wrote 8 of the stand-in's files; fixed refuses at `ledcontrol:9` before running and writes none. PASS.
  - **Two slips of mine in the control:** `standin()`'s loops clobbered the caller's `side` and `n` (now locals), and seeding the stand-in with `0` hid the writes (now `untouched`).
  - **The tree:** 14 PASS, 0 FAIL.
PROOF: P14 S6's controls -- `docs/qa-logs/2026-10-24-state-tests-s6/info-cases.sh` PASS (both mutations credited at stage D, failed fixed, naming the pattern) and `nova-cases.sh` PASS (credited at stage D with 8 stand-in files written; failed fixed with none written); the trees PASS 12 and 14/0.
PROOF: P15 S5's follow-up -- `docs/qa-logs/2026-10-24-state-tests-s5/backup-contract-cases.sh` PASS (the silent and derived backups pass the test at `c25f69d19a` and fail it at `ef31b4bf22`; the unmutated backup passes both); the historical T18 set 17/0.

## [Stage E] 22:21 UTC — S7: retroarch-wrapper-test (#996); a leak in rocknix-info-test (#995)

- **The source:** a copy of the M7 root's `build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf/gfx/video_thread_wrapper.c` (`m7-pixelelated-replacement20`, GENERIC_X64), read only, sha256 `b578746ee1b053b5211961f6f56f08cd0b2568fef8bb8bfc84b374b307c76952`, at `.qa-scratch/t14/retroarch/gfx/` (ignored by `.gitignore:63`). Nothing was written under the root.
- **#996 (`0037b04172`): what changed.**
  - **Per-site counting:** two call sites post in turn, each a different method reading its own local, and each site's count is compared with its own 1000.
  - **Cleanup:** the scratch `t.c` and binary are removed on every exit, through `atexit`, with SIGTERM, SIGINT and SIGHUP turned into an exit.
  - **No compiler:** a missing or unrunnable `gcc` is CANNOT, exit 2, naming it.
  - **The bare run** exits 2 with a usage line naming `RETROARCH_SRC`. The retired default roots (`:42-43`) stay #640's, and none moved.
- **The control,** `docs/qa-logs/2026-10-24-state-tests-s7/wrapper-cases.sh`: the stage-D test and the fixed one against the same copies, each with a fresh `TMPDIR` under the scratch.
  - **A `send_packet` that keeps the first command's method** (every post runs site 0's method, and the total is still 2000): rc 0 at stage D (`PASS: every command ran exactly once`), rc 1 fixed (`site 1 posted 1000 command(s); its method ran 0 time(s)`).
  - **The plain copy:** rc 0 both; stage D leaves one `t.c`, fixed leaves nothing.
  - **`PATH` holding only `python3`:** rc 1 at stage D (`FileNotFoundError ... 'gcc'`), rc 2 fixed (`CANNOT -- no gcc on PATH`).
  - **SIGTERM during a build by a `gcc` shim that sleeps:** rc 143 both; stage D leaves 2 entries, fixed none.
  - **The bare run:** rc 2 both; fixed prints the usage line. PASS, 5 s.
- **A slip of mine in the control:** the first cut ended the shim by an anchored `pgrep -f` pattern, and my own check `pgrep -af shim-bin` matched the session's shell (the self-match trap). The shim now writes its pid and `exec`s the sleep, and the control kills that pid; both pids were read afterwards as gone from `/proc`.
- **Already written:** the lane's own leftover from stage A, `/workspace/tmp/m6-t14/tmp/tmpi9wqx8u7/{t,t.c}`, was listed and removed. Earlier runs' `TMPDIR`s elsewhere are the record's, and were not touched.
- **Found while listing that `TMPDIR`: `rocknix-info-test` left its scratch on every failing run.** There were eleven `rocknix-info-test-*` directories from S6's own control runs; its `shutil.rmtree` at the end ran only after a pass, at stage D and after `359dd435ce` alike.
  - **The fix (`84a2b73140`, under #995):** an `atexit` handler registered when the scratch is made.
  - **The control,** `docs/qa-logs/2026-10-24-state-tests-s6/info-cleanup-case.sh`: at `359dd435ce` a failing run leaves one directory, fixed none; a passing run leaves none either way. PASS.
  - **After:** the tree PASS 12, and `info-cases.sh` PASS. The eleven were listed and removed.
  - `nova-led-test` already uses a `TemporaryDirectory` context and leaves nothing.
PROOF: P16 S7's control -- `docs/qa-logs/2026-10-24-state-tests-s7/wrapper-cases.sh` PASS (the wrong-site mutation, the leftover `t.c`, exit 1 without gcc and the killed run's scratch, all at stage D; per-site FAIL, nothing left, exit 2 naming gcc, the scratch removed when killed, and the usage line, fixed).
PROOF: P17 S6's cleanup follow-up -- `docs/qa-logs/2026-10-24-state-tests-s6/info-cleanup-case.sh` PASS (a failing run leaves its scratch at `359dd435ce` and nothing at `84a2b73140`).

## [Stage E] 22:27 UTC — #1009 filed after its fix; S8: the writers' busybox (#997)

- **The coordinator's answer (22:22 UTC):** file the scratch leak as its own Bug, after the fact. Filed as **#1009**, whose body says it was filed after `84a2b73140` (which cites #995) and carries the code trace and its two ticked criteria. A comment on #995 points at it, and the Phase 7 table will carry both.
- **The image's applets, read from the M7 root** `m7-pixelelated-replacement20` (BUILD_ID `1a026648442321609b2288c2c9c06803817f9df2`, its `image/system/etc/os-release`): its busybox lists 182 applets.
  - Every one except `sh` is a `usr/bin` or `usr/sbin` link to busybox; `sh` is bash.
  - `grep` and `sort` are real binaries from other packages, not applets.
  - **A trap met on the way:** the root's `bin` is an absolute symlink to `/usr/bin`, so `<root>/bin/sort` resolves to the **host's** uutils `sort`. I read it once that way, and the reading was wrong; only `<root>/usr/bin` is the image's.
- **#997, `settings-modes-test` (`929355c417`).**
  - **Provenance:** `--busybox` is accepted under a build root's `image/system/`, with its BUILD_ID read, printed and in the receipt, or with `--busybox-from <BUILD_ID|image>`. Any other is CANNOT, exit 2. `--unverified-busybox` marks every line and exits 3, or 1 when a case failed.
  - **Shims:** every listed applet but `sh` is shimmed, and quoted. The receipt hashes the copy that ran.
- **#997, `melonds-upgrade-test` (`30d9339ea3`):** the same contract; the function's five commands were already shimmed and quoted.
- **The controls,** `docs/qa-logs/2026-10-24-state-tests-s8/settings-cases.sh` and `melonds-cases.sh`, each run with a TMPDIR under the scratch.
  - **At the stage-D tip:**
    - the host's BusyBox 1.37.0 passes both tests as the candidate's (29/29, 15/15), and melonDS's receipt names no origin;
    - a `settings_base` reading with `cat --squeeze-blank`, an option the image's 1.36.1 `cat` lacks, passes 29/29, because `cat` falls through to the host;
    - a TMPDIR with a space gives 5 PASS, 24 FAIL (the unquoted wrapper; the refuse cases take the 127).
  - **Fixed:**
    - the host's busybox is refused, exit 2, naming the remedy;
    - `--unverified-busybox` exits 3, with 29 of 29 and 15 of 15 lines marked;
    - the build root's busybox passes, naming its BUILD_ID;
    - a stand-in root's id, and a declared copy's origin, land in the receipts;
    - the GNU-only writer fails, 13 PASS, 16 FAIL;
    - the space passes 29/29.
  - Both controls PASS.
- **Two slips of mine in the settings control**, corrected before it was kept:
  - every run's TMPDIR held a space, so stage D failed throughout, which proved nothing;
  - the first GNU-only mutation (`rm --interactive=never` on the lock release) changed nothing the test reads, because the shell's EXIT trap removes the lock anyway. It became the `cat` in `settings_base`.
- **For #662 (T15's), not this lane's:** `last-good-scripts-test`'s host fallback (`:381-400`) is unchanged; it is the coordinator's lead, named in the Phase 7 table.
- **A note for any caller:** a guest run that passed `--busybox /usr/bin/busybox` (the qualification records of 2026-10-04 to 2026-10-08) now needs `--busybox-from image`. No live caller exists in `.github/workflows` or `tools/vm-qa`.
PROOF: P18 S8's controls -- `docs/qa-logs/2026-10-24-state-tests-s8/settings-cases.sh` PASS and `melonds-cases.sh` PASS (the host busybox passed as the candidate's, a GNU-only writer passing and a spaced TMPDIR breaking, all at stage D; refusal, exit 3 with every line marked, the BUILD_ID or origin recorded, the GNU-only writer failed and the space passing, all fixed).

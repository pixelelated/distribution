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

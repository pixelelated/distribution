# Running log — M6.P2 T40, the patches and kernel configurations no plan applies (#687)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`).
- **Brief:** `docs/reviews/briefs/patches-dead.md`, version 2 (`92f2f35c16`, the same bytes at the branch's `HEAD`).
- **Dispatch:** the coordinator's comment on #687, 05:25 UTC on 2026-10-25.
- **Depth:** Local. There is no reviewer seat, `tools/council/run invoke` is never run, and the counts are the check.
- **`reviewed-at`:** `b8cde6f305`, the dispatch tip and the branch `HEAD` at stage A. The read is of `8ebaf8daad`'s bytes: `git diff --stat 8ebaf8daad b8cde6f305 -- packages projects` is empty.
- **T23's table** is read from `feature/m6-packages-dead-ends-670` at `f1561559aa` with `git show`, never checked out.
- **The rule (D-WORKFLOW-209):** the lane removes nothing and edits no `.patch`, `.conf`, recipe or tool.
- **No network at all:** no `git fetch`, no plan generation. `config/options ""` and `get_pkg_directory` ran with a logging `curl` shim first on `PATH`, and it was never called.
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t40/tmp`; `BUILD_DIR=/workspace/tmp/m6-t40/plan-build` takes `config/options`' caches out of the worktree. Outputs are under `.qa-scratch/t40/`, and copies are in `stage-a/`.
- **Prose** goes in through a quoted heredoc or the Write tool; **times** come from `date -u`.

## [Stage A] 05:26:49 to 05:31 UTC — scope, the five classes, the headers, linux, the symlinks, the upstream status

- **The first commands** (brief § 1):
  - **No `git fetch`** (the dispatch: *no network*). Local refs were read; the last fetch was 2026-10-22 16:09:46, and `upstream/next` is `651150fc88`.
  - T23's branch tip is `f1561559aa`.
  - The branch is `feature/m6-patches-dead-687`, stacked on P1 (`2174265e9c`); `inventory.json` is present.
  - `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 8 files, the dispatch's eight.
  - `git diff --stat b8cde6f305 HEAD -- packages projects tools` is empty, and so is `git diff --stat 8ebaf8daad HEAD -- packages projects`.
  - T23's units, read from its branch: **731**.
  - The Makefile: **27 `PROJECT=ROCKNIX`**, nothing else.
  - `scripts/unpack:127-128`: `if [ "${TARGET_ARCH}" = "x86_64" ]; then PATCH_ARCH="x86"`.
  - `rules-check --quiet` rc 0; `register-check`: 681 IDs.
  - `df -i /tmp`: 40 %. Nothing was written there.
- **The host before anything ran:**
  - The host file's last line is the M7 lane's 05:25:39 note: its build preparation is blocked on T15 shell PIDs. That is not this lane's, and this lane holds none.
  - Census: qemu 0, compilers 0.
- **Membership** (§ 2's block at `2174265e9c`; `stage-a/scope.out`): 778 paths and 317,908 lines; all `vendor-carried`; 760 `.patch` and 18 `.conf`; 351 shadowed, 277 of them to `projects/ROCKNIX/packages/linux`; `reachable_by`, `buildable_by` and `last_fork_commit` empty on all 778.
- **`get_pkg_directory linux`** on GENERIC_X64/x86_64, H700/aarch64, SM8550/aarch64, H700/arm and SM8550/arm all resolve to `projects/ROCKNIX/packages/linux` (rc 0, 1 s, 0 `curl` calls; the worktree's ignored set is unchanged; `stage-a/linux.out`). The kernel's `PATCH_ARCH` is `x86` on x86_64 and `aarch64` on the other four.
- **`unpack`'s patch directories** (`stage-a/unpack-lines.out`): `${PKG_DIR}/patches/*.patch`, `patches/${PATCH_ARCH}/`, `patches/${PKG_VERSION}/` and `.../${PATCH_ARCH}/`, the project's and the device's `patches/${PKG_NAME}/`. `:196` substitutes `@TARGET_CPU@` and `@DEVICE@` into each patch before applying it.
- **The x86_64 directories under `projects/ROCKNIX/packages`:** exactly the five files (`stage-a/x86_64.out`), vitaquake2-lr's four and EmulationStation's `cpugov.patch`.
- **The headers** (5 s; `stage-a/headers.out`): **746 with `From:` and `Subject:`, 14 without** (`stage-a/headerless.txt`).
  - 12 are ROCKNIX's: strace, connman, grub's three, panda3ds-lr, play-lr, vitaquake2's four, ES's `cpugov`.
  - 2 are LibreELEC's: `mesa-001-fix-addrlib-lgcc-link`, `ffmpeg/patches/rpi/0001-rpi`.
- **Upstream** (`stage-a/deleted-upstream.txt`, `stage-a/churn.txt`):
  - **6 deleted at `upstream/next`**: strace's two and grub's four.
  - **102 commits since 2026-06-01:** 99 LibreELEC's (88 commits by its developers, 10 of its pull-request merges, 1 more contributor's) and **3 ROCKNIX's own**: `74818e9c94` (spycat88, libretro bump), `40fce2a089` (rocknix, *amd64: wip am64 changes*, which added `cpugov.patch`) and the merge `96aff382c4` (*Merge remote-tracking branch 'LibreELEC/master' into next*).
  - From `8ebaf8daad`'s first-parent line, 100 came in with ROCKNIX's PR #3172 (`br-update`) and 2 with the fork's merge of `upstream/next`.
  - **0 fork-authored, since June or ever.**
- **The symlinked `patches` entries** (`git ls-tree -r 8ebaf8daad | awk '$1=="120000"'`; `stage-a/symlinks.txt`): `projects/ROCKNIX/packages/lang/gcc/patches -> ../../../../../packages/lang/gcc/patches/` and `projects/ROCKNIX/packages/devel/cmake/patches -> ../../../../../packages/devel/cmake/patches/`, each mode `120000`. (Others: `SDL2_glesonly/patches -> ../SDL2/patches`, `Generic-legacy/patches`, and per-file links in mangohud, vitaquake2 and ppsspp-sa.)
- **The five classes** (`tools/t40-tables.py stats`, `stage-a/stats.out`; first match in order; asserts 778, 317,908, 760 and 18):

  | Class | Rows | Lines | The brief |
  | --- | ---: | ---: | --- |
  | (a) generic kernel | 277 | 92,389 | 277 / 92,389 |
  | (b) other projects | 234 | 160,488 | 234 / 160,488 |
  | (c) `patches/x86_64` | 5 | 99 | 5 / 99 |
  | (d) inside a T23 dead unit | 234 | 63,795 | 234 / 63,795 |
  | (e) the rest | 28 | 1,137 | 28 / 1,137 |

  - (a) by directory: rockchip 187, rockchip-old 48, dvb 39, default 3.
  - (b) by project: Amlogic 94, Allwinner 81, Rockchip 15, Samsung 15, NXP 14, RPi 7, Generic 3, Qualcomm 3, ARM 2; the 18 confs among them.
  - (d) sits in **117** T23 units: 158 rows *dead, upstream-carried* (6 of which are the upstream-deleted, so 152 under that disposition), 67 *shadowed copy, override live*, 9 *shadowed copy, override dead too*.
  - (e) splits **6 + 16 + 2 + 4**:
    - e1: fluidsynth 1, readline 1, and **gcc 3 and cmake 1, reached after all through the symlinks**;
    - e2: 16 LibreELEC `libretro-*`, plus the 2 ROCKNIX-own `panda3ds-lr` and `play-lr`;
    - the 4 dvb `disable-pci` and `rtl8723bs_bt` rows.
- **The shadowed 74 not the kernel's:**
  - **2 content duplicates** by the strict test (the diff body byte-equal, `index` lines aside): `kmod/0001-fix-pkgconf` and `systemd/0003-remove-nonexistant-dependency`.
  - **4 applied after all** through the symlinks.
  - **68 others.** Of those, 12 carry the same change at different offsets in the override, 6 the same changed lines with the context moved, and **50 have no counterpart in the override.**
  - The brief's *68 LibreELEC changes the override builds without* is 50 by these tests; the 18 are named in `02`.
- **The generator's first symlink test compared the target with the unit directory, not `unit/patches`,** and called `gcc` and `cmake` dead. It was corrected and re-run before any figure was used.
- **Nothing written** under `/tmp`, `/workspace/repos/rocknix*`, another lane's worktree, `packages/`, `projects/` or `tools/`. No build, compiler, guest, plan generation or network.

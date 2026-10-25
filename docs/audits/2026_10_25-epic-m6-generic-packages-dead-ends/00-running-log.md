# Running log — M6.P2 T23, the generic packages no image builds (#670)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`).
- **Brief:** `docs/reviews/briefs/generic-packages-dead-ends.md`, version 2 (`74b71ab443`, the same bytes at the branch's `HEAD`).
- **Dispatch:** the coordinator's comment on #670, 04:10 UTC on 2026-10-25.
- **Depth:** Local. There is no reviewer seat, `tools/council/run invoke` is never run, and the counts are the check.
- **`reviewed-at`:** `27b015c901`, the dispatch tip and the branch `HEAD` at stage A. The read is of `8ebaf8daad`'s bytes: `git diff --stat 8ebaf8daad 27b015c901 -- packages projects` is empty.
- **The rule (D-WORKFLOW-209):** the lane removes nothing and edits no recipe and no tool.
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t23/tmp`. `BUILD_DIR=/workspace/tmp/m6-t23/plan-build` takes `config/options`' package caches out of the worktree. The run outputs are under `.qa-scratch/t23/`, and copies are in `stage-a/`.
- **Prose** goes in through a quoted heredoc or the Write tool; **times** come from `date -u` or a file's mtime.

## [Stage A] 04:11:31 to 04:21 UTC — scope, the five plans, resolution, the closure, pkgcheck

- **The first commands** (brief § 1):
  - **No `git fetch`.** The dispatch says *no fetch* and brief § 5 *the network is not used at all*, so local refs were read. The last fetch was at 2026-10-22 16:09:46 (`FETCH_HEAD`); `upstream/next` is `651150fc88` and `origin/next` is `8ebaf8daad`.
  - The branch is `feature/m6-packages-dead-ends-670`, stacked on P1 (`2174265e9c`); `inventory.json` is present.
  - `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 8 files, exactly the dispatch's eight paths.
  - `git diff --stat 27b015c901 HEAD -- packages projects tools` is empty, and so is `git diff --stat 8ebaf8daad HEAD -- packages projects`.
  - `git log --oneline c445081a59..upstream/next -- packages | wc -l` prints 0, against the local `upstream/next`.
  - `rules-check --quiet` rc 0; `register-check`: 681 IDs, every citation resolves.
  - `df -i /tmp`: 40 % used. Nothing was written there.
- **The host before anything ran:**
  - The host file's last line is the coordinator's 04:10 UTC grant to the M7 lane (a lifetime guest, then one bounded successor).
  - Census: qemu 0, compilers 0. This slice runs no guest and no compiler.
- **Membership** (§ 2's block at `2174265e9c`; `stage-a/scope.out`, `stage-a/paths.txt`):
  - 1,604 paths and 95,892 lines;
  - 1,601 upstream-carried and 3 fork-own;
  - 1,565 unreached and 39 unshipped;
  - 727 recipes;
  - 260 shadowed rows.
- **Units:** 731, of which 727 have their recipe in the set and **4 have it outside**: `chrome-depends/gtk3` (1 file), `addons/tools/btrfs-progs` (4), `security/openssl` (3) and `sysutils/udevil` (3), 11 files in all. There are no orphans and 720 distinct basenames.
- **The five plans** (`tools/viewplan`, plan generation only):

  | Config | Root | rc | Seconds | `Packages loaded` | Distinct names | The header's |
  | --- | --- | ---: | ---: | ---: | ---: | ---: |
  | GENERIC_X64-x86_64 | image | 0 | 1 | 1435 | 593 | 593 |
  | H700-aarch64 | image | 0 | 1 | 1438 | 605 | **611** |
  | H700-arm | arm | 0 | 1 | 1438 | 235 | 235 |
  | SM8550-aarch64 | image | 0 | 0 | 1435 | 672 | 672 |
  | SM8550-arm | arm | 0 | 1 | 1435 | 238 | 238 |

  - **The worktree stayed untouched:** `git status --porcelain --ignored` was identical before and after.
  - **The H700 delta, named:** the six names the inventory's container plan has and the host's lacks are `atf`, `h700-suspend-stub`, `pyelftools`, `swig`, `u-boot-DDR3` and `u-boot-DDR4`.
    - Cause: `SUBDEVICES` comes from `xmlstarlet ... 2>/dev/null` (`distributions/ROCKNIX/config/functions:224`). `xmlstarlet` is absent on this host, so `SUBDEVICES` is silently empty and H700's `u-boot` wants only `toolchain`.
    - The two arm configs' only difference, `emulators`, is an artifact of matching by directory basename, outside this set. The other two configs match name for name.
- **A deviation: the five plan runs at 04:12:13 to 04:12:16 UTC made five HTTPS requests.**
  - `scripts/pkgjson` sources every recipe in the package caches (`:54-55`). The unreached generic `packages/graphics/mesa-reusable/package.mk:15` sets `PKG_SHA256="$(curl --fail --connect-timeout 30 --retry 3 --location --max-redirs 5 ${PKG_URL}.sha256)"` at global scope. So every plan generation runs that `curl` against `https://github.com/LibreELEC/mesa-reusable/releases/download/...`.
  - **Proved offline:** the `pkgjson` worker on that one recipe, with a logging `curl` shim first on `PATH`, logged the call (`stage-a/shim/mesa-reusable-load.txt`).
  - **The five plans re-run through the shim:** rc 0, each byte-identical to the first run, and exactly 5 calls intercepted (`stage-a/plans-offline.out`, `stage-a/shim/curl-offline-plans.log`).
  - So the first runs reached the network once each, read-only (a public checksum file), and no source was fetched.
  - **From here every plan run goes through the shim.** The brief's *nothing is fetched* is not true of any plan generation on this tree; the coordinator's runs and the inventory's 26 make the same request. That is a finding (Q2).
- **Resolution** (`config/functions`' `get_pkg_directory`, per device, `BUILD_DIR` outside the worktree; `stage-a/shim/resolve.sh`):
  - 720 unit names × 3 devices = 2,160 lines, 0 errors. Another 50 names from the unpack graph give 150 lines; the 15 empty ones are another device's own package.
  - A first run under `set -u` died inside `config/options`, which reads unset variables. The script was corrected and re-run.
- **The shadowed split** (`stage-a/stats.out`, from `tools/t23-tables.py`):
  - **Reproduced on the host plans:** 84 recipes whose name some plan builds, every one a shadowed copy, and 5 shadowed units with no plan naming the name (`swig`, `amlogic-boot-fip`, `atf`, `rkbin`, `weston`).
  - **With the container's H700 plan**, `swig` and `atf` are built (H700's bootloader chain), giving **86 and 3** (`amlogic-boot-fip`, `rkbin`, `weston`, each with its override dead too).
  - `shadowed_by` covers 93 units and 260 rows.
- **The eleven basename pairs** (strace, connman, grub, qemu, rkbin, weston, cbindgen, spirv-headers and the three rust snapshots) each resolve, on all three devices, to the `projects/ROCKNIX` copy.
- **The `PKG_DEPENDS_UNPACK` closure** (`stage-a/unpack-lines.txt`):
  - Lines at `8ebaf8daad`: 38 anchored, **40 indented**, 94 counting `+=`.
  - **Five units are reached after all**, every one `unreached` in the inventory:
    - `projects/ROCKNIX/packages/graphics/spirv-headers`, named by the overrides `glslang:18`, `shaderc:12`, `spirv-tools:18` and `llvm:17`;
    - the three ROCKNIX rust snapshots, named by the override `rust:11` (`cargo-snapshot` also by `cargo:9`);
    - generic `packages/devel/binutils-gold`, named by generic `binutils:11`.
  - All the namers are in all three plans.
  - The brief's *24 recipes named directly* reads 25 by basename on the indented `=` lines, 30 counting `+=`, and 18 resolved per device. The closure, not this count, decides a row.
- **The four outside units are not a tool error:** each ROCKNIX override sources the generic `package.mk` at its line 4, and carries its own copies of the files the recipe reads through `${PKG_DIR}`.
- **`pkgcheck`** (`stage-a/pkgcheck.txt`):
  - **The brief's sweep checks nothing.** `tools/pkgcheck packages/addons/tools/jre.zulu` matches `-path */packages/...`, which `find`'s output never has. It prints nothing and exits 0. `jre.zulu` or `tools/jre.zulu` finds the FAIL.
  - The sweep was re-run with each argument less its first component. All 727 recipes were processed (each named in the tool's stderr progress line); 3 exit non-zero; 4 FAIL lines and 14 WARN, in 55 s.
  - **T6's two leads are judged false positives:** `jre.zulu:12` reads `PKG_SHORTDESC`, set at `:11`, and `mesa-reusable:14` reads `PKG_SOURCE_NAME`, set at `:13`. The two `wireplumber` duplicate-function FAILs are #657's parser false positive.
- **Dispositions at stage A** (sum 731): 603 dead, upstream-carried; 94 shadowed copy, override live (`installer` among them); 7 shadowed copy, override dead too; 21 unshipped; 5 reached after all; 1 fork-own, dead (`projects/ROCKNIX/packages/rust/cbindgen`).
- **Nothing written** under `/tmp`, `/workspace/repos/rocknix*`, `packages/`, `projects/` or `tools/`. No build, no compiler, no guest, no source fetch, no provider call.

## [Stage B] 04:21 (after the stage-A commit) to 04:27 UTC — the tables, the disagreements, Q1 to Q7

- **The coordinator's answer (04:23 UTC on #670):** file the `pkgcheck` bug at stage D (D-QA-051 rule 6), and a second bug for `mesa-reusable:15`'s parse-time `curl`. The brief's *nothing is fetched* and its `pkgcheck` form are corrected at `0a5676ea5d`; criterion 11 is rewritten (the five unshimmed runs named). T6's two leads are false positives on this evidence.
- **The tables:** `tools/t23-tables.py <tree> reach` and `coverage` write `02`'s § Reachability (731 rows) and § Coverage (1,604 rows), and the `awk` counts print 731 and 1604. The dispositions sum to 731 units, 1,604 files and 95,892 lines.
- **`upstream/next`** (the local ref, fetched 2026-10-22): 14 of the 1,604 rows differ there, 3 of them fork-own. The 11 upstream-carried are 8 deleted upstream after the base and 3 modified, as the brief says (`stage-b/upstream-diff.txt`).
  - The three rust snapshots among the 8 are reached today: the fork's ROCKNIX `rust` override unpacks them.
  - Upstream deleted that override too, so its generic `packages/rust/rust:11` unpacks the generic snapshots. The next merge drops the fork's copies without a conflict.
- **`cbindgen`:** `git grep -n cbindgen 8ebaf8daad -- packages projects` gives 7 lines, all inside its own two directories (`stage-b/cbindgen-grep.txt`). It is not on `upstream/next`.
- **Written:**
  - `02`: Phase 2, § The split, § Reachability, § Disagreements, § Coverage, § The runs, § Proofs;
  - `03`: § 3.5 seams;
  - `04`: eight findings, Q1 to Q7, Q6 summing to 731, Q1's paragraph ending in the recommendation and *the decision is the maintainer's*;
  - `second-opinions/review-plan.json`: local, `reviewers: []`, D-WORKFLOW-184.
- **No plan run at stage B,** so no network. Nothing changed under `packages/`, `projects/` or `tools/`.

## [Stage C] to 04:29 UTC — the punch list drafted; the pre-issue lint PASS

- **`05-punch-list.md`** is generated by `tools/punch-items.py` from one list: 9 items.
  - PL-01 to PL-03 are the three bugs: the inventory's `PKG_DEPENDS_UNPACK` gap, `pkgcheck`'s silent pass, and `mesa-reusable:15`'s `curl`.
  - PL-04: the `xmlstarlet` lead.
  - PL-05 to PL-07: the three fork-own rows (`installer`, ROCKNIX `spirv-headers`, `cbindgen`), each with its verdict. `cbindgen` carries a proposed removal with `Already written:`.
  - PL-08: the Q1 class decision.
  - PL-09: the brief's moved figures.
  - Every item carries `question:` and is open.
- **`tools/lint-audit-artifacts docs/audits/2026_10_25-epic-m6-generic-packages-dead-ends --phase pre-issue`:** `PASS pre-issue artifacts`.

## [Stage D] to 04:32 UTC — three bugs, the audit issue #1052, the outcomes, the lint; the pause

- **The coordinator's answers on #670:** at 04:23, file the `pkgcheck` bug and a second for `mesa-reusable:15`; at 04:29, the four deferrals point at the decision issue #1048.
- **Bugs filed by the lane** (label `bug`, milestone M6, `tools/box-check` 0 fail on each):
  - **#1049:** the inventory's `PKG_DEPENDS_UNPACK` gap, with its five cases and a constructed-tree criterion;
  - **#1050:** `pkgcheck`'s silent pass on an unmatched argument;
  - **#1051:** `mesa-reusable:15`'s parse-time `curl`.
- **#1051's sibling grep:** the first form (`[A-Z_]`) printed nothing because `PKG_SHA256` has digits. Re-run with `[A-Z0-9_]`, and with a wider form, each lists exactly `packages/graphics/mesa-reusable/package.mk:15`. #1051's body was corrected before anyone read the first form.
- **The audit issue:** **#1052**, a sub-issue of #670 (the sub-issue list reads `1052`), with 9 checkboxes, each naming its outcome. `tools/box-check --issue 1052`: 0 fail.
- **`05`'s Phase 7 table:**
  - 8 Deferred: to #1049 (PL-01, PL-06), #1050 (PL-02), #1051 (PL-03), #1048 (PL-05, PL-07, PL-08), and PL-04 to #670 pending its issue;
  - 1 Resolved, by `0a5676ea5d` (PL-09).
- **The lint on the folder:** `--phase pre-issue` PASS, the default phase `PASS`, `--issue 1052` `PASS`.
- **Paused at stage D**, per brief § 8. Nothing changed under `packages/`, `projects/` or `tools/`.

## [Stage F] 04:34 to 04:34 UTC — the counts, the plans through the shim and the lint at the tip (no stage E: the coordinator, 04:33 UTC)

- **PL-04** defers to Backlog **#1053** (the coordinator's answer at 04:33). `05` is regenerated and #1052's body updated; `box-check` 0 fail.
- **At `bf510a0ac9`** (`stage-f/counts.txt`):
  - The five plans, re-run **through the `curl` shim**, have rc 0 and are byte-identical to stage A's. 5 calls were intercepted and none reached the network. The worktree's ignored set is unchanged.
  - `tools/t23-tables.py stats` is identical to stage A's.
  - Coverage rows: 1604. Reachability rows: 731.
  - `git diff --stat 27b015c901 HEAD -- packages projects tools` is empty; deletes and renames against the dispatch tip: 0. `packages/` and `projects/` equal `8ebaf8daad`.
  - Provenance files in `second-opinions/`: 0.
- **The lint:** pre-issue, resolution and `--issue 1052` each print `PASS`. `box-check` gives 0 fail on #1049, #1050, #1051 and #1052.

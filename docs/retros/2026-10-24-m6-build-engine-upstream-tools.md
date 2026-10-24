# Mini Retro: M6.P2 T6, upstream's helper tools and the other distributions (#653)

**Completed:** 2026-10-24
**Scope of this retro:** the T6 lane, covering:
- the slice's 135 paths (7,369 lines), read with the bytes equal to `next`'s `8ebaf8daad`;
- the Local-depth audit, stages A to D (`docs/audits/2026_10_24-epic-m6-build-engine-upstream-tools/`, #846's six items);
- the two fix streams, S1 (#845) and S2 (PL-06), of the coordinator's `t6-streams.md`;
- the close-out.

Not retro'd here, because they are not this lane's:
- the coordinator's acceptance and the #585, #651 and #657 dispositions;
- the merge to `next`.

**Commits:** `reviewed-at` `b96e1ca761`, `fixed-at` `820e413179`.

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** Interface to a game's first frame and game to game are untouched, as `04` § Q5 said before the fixes.

The two changes are to `tools/pkgcheck`, a lint run by hand on the build host after a recipe edit. It is not part of a build, not on an image and not on a device. The two other distributions are never selected (`config/options:24`). No time-to-play run was made, because no image changes.

## What worked well

- **The two-way caller search.** Every zero from the path search was searched again by bare name, with `pkgcheck` and `adjust_kernel_config` as positive controls. The second search is how `check_kernel_config` moved from unreached to reached: `adjust_kernel_config:38` calls it, and the path search could not see that (P2).
- **Deriving the late names from where the build sets them, not from a list.** S2's brief and the lane's own PL-06 named `TOOLCHAIN`, `SYSROOT_PREFIX` and `INSTALL` as examples. Reading `config/options:185,197`, `source_package`, `setup_toolchain` and `scripts/build` showed only `INSTALL` late of the three, plus 17 more (P14).
- **A trial sweep before the list changed.** A scratch copy with `SYSROOT_PREFIX` listed gave 87 FAIL lines. Reading the 66 sites showed every global use was a configure, cmake, make or unpack option, where the value is the right one. That kept a lint that cries wolf on 66 correct recipes out of the tree.
- **T5's fixture shape, reused.** `fx-pkgcheck.sh` takes a commit or `WORKTREE`, so before, S1 and S2 are the same command (P11, P12).

## What was harder than expected

- **A brief's expected count that was not the tree's.** The stream brief expected 0 FAIL lines before the change; the sweep gave 12, all on real recipes. Each stream reports a delta instead, and each line is read in `02` § Leads from the sweeps.
- **My own lead was wrong.** PL-06 and `03` § 3.2 named `TOOLCHAIN` as late, from the README's direction rather than from the load order. Corrected at stage E, with the correction left visible in `03`.
- **Estimated timestamps, again.** P8 and P9 were written as `08:2x` and replaced with the bracket `08:12-08:23` (the friction line names the fourth instance of the shape this session). A guard for it still does not exist.
- **Two slips caught before a push.**
  - The fixture took a relative scratch path and its first run failed on its own stderr file; the script now resolves the path.
  - S2's commit message counted the new FAIL lines wrongly; it was amended while the branch was unpushed.

## What we discovered

- **`config/path` is sourced before the recipe.** `config/options:185` comes before `source_package` at `:197`, so `TOOLCHAIN`, `LIB_PREFIX`, `TARGET_PREFIX` and `BUILD` are early. Only what is reset later is late: `INSTALL` (`scripts/build:140`), `SYSROOT_PREFIX` after `post_make` (`:471`), and what `setup_toolchain` and `source_package` set.
- **Three real defects on ROCKNIX recipes, all from upstream:**
  - `systemd:105`'s global `BUILD_WITH_DEBUG` test is always false, because `source_package` unsets the variable before the load (upstream's `:118` too);
  - `virtual/image:109,110` writes into the image directory every time the recipe is sourced;
  - `sameboy-lr:13`'s `PKG_BUILD` is empty at load (already #818).
- **`pkgcheck`'s parser ends a function at a heredoc's column-0 `}`.** 14 of the 21 FAIL lines after S2 are that, all in the two `wireplumber` recipes. It is a lead for #657, not fixed here.
- **`distributions/LEIoT/kernel_options` has dangled since LibreELEC's `4130b59b50`.** No fork build reads it; it is a #585 line.

## Adjustments for the next lane

- **Derive a list a lint checks from the code that sets the values, and trial-sweep it before committing it.** An example list in a brief or a lead is a hypothesis.
- **Run a lint over the whole tree before quoting what it should print.** A delta needs its baseline read, not assumed.
- **A fixture resolves its scratch path first** (`cd "$1" && pwd`), so a relative argument cannot make every case fail the same way.
- **Read a reachability zero a second way** (by bare name, inside the slice as well as outside), with a known-reached control beside it.

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-build-engine-upstream-tools --phase pre-issue`: `PASS`. The full lint also prints `PASS`.
- `PROOF:` lines 14 equal the `proved:` cells, 14.
- The coverage table has 135 rows.
- #846: 6 of 6 at a Phase 7 outcome (2 Resolved, 4 Deferred), each ticked naming its commit or target; `tools/box-check --issue 846`: 0 open, 0 fail.
- #845: both checkboxes ticked from P11; open until the merge, as T5's #827; `box-check` 0 fail.
- Of the 135 paths, only `tools/pkgcheck` differs between `8ebaf8daad` and `fixed-at`; no path is deleted.
- The checkers and `hooks-test`: exit codes on #653's stage-H hand-back.

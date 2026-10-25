# Retrospective: M6.P2 T15, the last-good scripts test (#662)

Read at `8ebaf8daad`; the runs are `02` § The runs. The lens is brittleness.

## 3.1 What the suite was for

It was written on 2026-09-10 (`52c4249759`) as *a device-less check that the scripts keep the last known good state when they are killed mid-write* (D-CLOUD-078, #105, the header `:5-6`). The same day, blindspot 34 gave it its second purpose: run every busybox applet a script calls through the image's busybox, because GNU `tr` had passed a check that busybox `tr` failed on every device (`:152-160`).

In 408 commits it grew from those two claims to 34 sections. Three audits' punch items became cases: #307/#308's streams in `x` and `y`, the fix round in `y` and `z`, and the audit of the fixes in `z`'s `S3F`. Section `y` alone is 5,386 lines, and `x` and `y` together hold 61 % of the 1,313 checks.

## 3.2 What drifted

- **The busybox it exists to run.** No M6 worktree has a build root that `image_tool_source`'s three globs reach (`:392-394`: `${ROOT}/../*`, `${ROOT}.worktrees/*`, `${ROOT}/build.*`). The M7 roots live under `/workspace/repos/rocknix.worktrees/`, which none of them names. So since M6's worktrees were cut, every run but those given `QA_SYSTEM_ROOT` has fallen to `:400`'s `command -v busybox || true`, the host's 1.37.0. It judged the host: 319 checks FAIL, and 61 of their lines say `flock: applet not found`. The banner at `:426` names the copy; nothing in the verdict does. The founding lesson was undone by its own fallback.
- **The rclone stream A claims.** *The cloud scripts against the image's rclone* (`:8906`) take the host's `/usr/bin/rclone` by the same fallback: v1.60.1-DEV against the recipe's 1.75.2. Measured: no verdict changes (`rchost`, 1,313 / 0). The version is printed (`:8914`) and never asserted.
- **The `--old` controls.**
  - Two of the header's twelve refs no longer exist (`0f7785e6ed`, `d79281066c`).
  - The other ten stop at `s` or `x`, because `src_of` exits 2 for the whole run at the first script a ref predates.
  - The newest sections, `x` to `ah`, were added after every ref the header names, so no recipe reaches them.
  - One recipe (`70b6c70ca7`) fires on patch application, not on the `012` checks it promises.
  - The header was not updated as sections were added; its claims stop at `w`.

## 3.3 What none of them noticed

- **The record's last PASS under the image's busybox is 2026-10-06** (qa-18). Every run since from an M6 worktree FAILed 319 checks. #1015 (T12) filed them as *the last-good scripts test fails 319 checks on this host wherever its scratch is (backuptool's staging first; host tools suspected)*, the suspicion right and unproven, until this slice's attribution runs settled it: the busybox, by `bbhost` (319) and `rchost` (0). Nothing in a run's own verdict could have said so.
- **The coordinator's ten FAILs at the hash** were an export's: no `.git`, so the fixtures that read `417dcd8610` from git came up empty. Each was caught only by a vacuity detector downstream of a read that fails open (`f1_tree_at` `:3205-3215`; `:4271`). The read itself says nothing.
- **A host without the sources cache** would turn section `D`'s 33 busybox FAILs into 21 SKIPs (exit 3, read as SKIP by `vm-qa:148`), because they sit behind section `t`'s client tarball (`DT_OK`, `:6649`).

## 3.4 What the record says about catches

- **The header and the comments name what each section caught:** #105 to #546, the streams' PL and G items, and blindspot 34.
- **The `--old` recipes are the positives.** Before each stops, the promised FAILs fire in `a` to `v`, with the exceptions in `02` § The runs.
- **The later groups carry their own positive refs in comments,** unnamed in the header: `417dcd8610` (`:8905`, `:3194`, `:6636`), `f3d19dc8fb` (`:11068`, `:12089`, `:12321`, `:12603`, `:13172`), `320d2b2bea` (`:13586`), `286759eb6d` (`:13663`) and `a06539d8ec` (`:8593`). None of them was run here. Each would stop where `src_of` meets a script it predates.

## 3.5 The seams

| Seam | What crosses it | What breaks it |
| --- | --- | --- |
| this file and `tools/vm-qa`'s `scripts` suite | the exit code: `vm-qa:148` reads 3 as SKIP and any other non-zero as FAIL | a `NOT APPLICABLE` group exits 0 and reads PASS. A run on the host's busybox reads `FAIL (1)` with nothing to say it judged the host. An `--old` run is never `vm-qa`'s |
| this file and T14's four tools | `--cloud-layout` and `ae` (`rasteratops-cloud-layout-test`), and `ag`/`ah` (`settings-modes-test`, `melonds-upgrade-test` with `--busybox "${BB_HOST}"`) | T14's S8 refuses a busybox that is not a build root's, and `BB_HOST` is the run's copy, so `ag` and `ah` FAIL on every host until #997's two flags land here (S1). The connections fixture's `--config` order was fixed by T14 for this file's shims (#999) |
| this file and the scripts it proves | `src_of`'s copy of each script, from the tree or `BASE_REF` | a script added after a ref ends every `--old` run at its section. A script moved to another path, or a function renamed, empties a lifted fixture, and some checks then pass on nothing (`04` § Q3) |
| this file and the busybox source | `image_tool_source`: `QA_SYSTEM_ROOT`, then three globs, then the host's | no glob reaches the M7 roots, and the host fallback is silent. No busybox at all means GNU tools, with no banner |
| this file and git history | the fixtures that read `417dcd8610` and `73b20caf86` (`F1.`, `F1r.`, `C.`) | an export or a shallow clone: the read fails open, and only a vacuity detector catches it |

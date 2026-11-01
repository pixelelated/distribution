# Retrospective: M6.P2 T37, the EmulationStation recipe and themes in the distribution (#684)

The audit's look back over the slice's history: what these 15 files are for, what the fork changed
against ROCKNIX's base, what drifted, and what nobody's earlier fix noticed. The lane's own retro
is stage G's (`docs/retros/<date>-m6-es-recipe.md`).

## 3.1 What the files are for

They are how the distribution builds and installs the interface: the ES recipe clones the fork's
EmulationStation at its pin and installs the binary, its seeds, its catalog and its boot pieces
(the two units, the autostart link, the three scripts); the theme recipe installs ROCKNIX's shipped
theme with the fork's wordmark; `lowerdeck` is a second-screen touch interface that `PKG_UI`
installs on every image. None of them holds a menu or a player string; their effect on the player
is what the image carries and how quickly it reaches the interface.

## 3.2 What the fork changed, and what drifted

- **The source moved to the fork's own clone** (`:5-13`, `cb50b45f6e` 2026-08-19 first in the
  range's log, `84ff94fb3d` adding `zstd`), so the recipe's history is the pin's: 241 of the 246
  non-merge commits on `ui/` since the base touch the ES recipe (`stage-a/s5-runs.out` R04).
- **The credentials** (`:27-50`, #566, D-WORKFLOW-166), **the RVZ licence files** (`:58-65`), the
  **log loop that prints names only** (`144b3eccb6`), the **sway-ready wait** (`essway.service:12-14`,
  `c6afa31db1`), the **save-state layout** (`es_savestates.cfg`, #196), and the **wordmark and its
  licence** (D-WORKFLOW-144 to -146) are the fork's.
- **The licence expression** moved twice (`GPL` -> `MIT` -> `MIT AND BSD-3-Clause`), which a
  consuming check (#990) did not follow.
- **Drift by merge:** four merges of `upstream/next` resolved the ES recipe as the fork's file and
  dropped upstream's ARMSX2 block each time (PL-05); since the base upstream moved six more files the
  fork lacks and changed the two the fork also changed (PL-14).

## 3.3 What none of the fixes noticed

- **The link** at `:101` is upstream's form and dangled on every image built from this recipe; M7
  corrected it in its candidate's own recipe (#613) and the fork's tip still carries the old form
  (PL-01).
- **The patch directory**: `cpugov.patch` was added under a directory no device reaches
  (`40fce2a089`, "wip"), and nothing reported that it never applied (PL-02, #1072).
- **The stamp**: `PKG_NEED_UNPACK="busybox"` has never named a path (PL-03); upstream's line.
- **The no-op `rm`** has been upstream's order since the first ROCKNIX recipe (PL-04).
- **fribidi**: a dependency the plan supplies and the shipped binary did not take (PL-06), found only
  by an `ldd` on an image.

## 3.4 What the record says about catches

Each of the five was visible in the recipe's text and none tripped a check: `tools/pkgcheck` reads
late binding only, `fork-package-freshness` reaches none of the three recipes, and the image build
reports success over a dangling link, an unapplied patch and a missing library alike. This slice's
`tools/t37-checks.sh` FAILs on four of them at the tip and passes a fixture with them fixed
(`stage-c/failfirst.out`).

## 3.5 The seams

The ES pin is the integration's (D-WORKFLOW-191); the renderer source list T35's and the bodies
T36's beside `:25`'s define; T40's patch and T42's theme patches; T8's `virtual/image`. A fix here
moves only the ES recipe's stamp (the fixture's step 7: `moved=1 touched=1` for
`emulationstation`, `moved=0 touched=0` for the other two, on both devices).

## 3.6 Time to play

The recipe sits on boot to interface. On the candidate guest `essway.service` started at 5.37 s
and ES was logging at 5.82 s of kernel time (G-04), with the pre-generated `en_US.UTF-8` present
(PL-12's step worked there). Nothing in this slice's proposals adds work to that path.

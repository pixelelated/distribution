# Analysis tracking: M6.P1, the survey (#641) -- 2026-10-22

The multi-pass tracking file for P1 (`docs/reviews/briefs/p1-survey.md` § 6).
Rigour: **comprehensive** (first analysis of the scope; all seven passes,
N-to-N cross-reference by area). Every count below is the output of the
command written beside it. A resumed session re-runs the command rather than
trusting the number.

## Header

| Field | Value | Command |
| --- | --- | --- |
| Executor | Opus 5.5 (`claude-opus-5-5`), high effort; Claude Code session `dbac446e-3b41-4b28-966d-0a6efe07ea2b`, Herdr pane `wN:p3` | the dispatch on #641 (no model or effort named by the maintainer; the brief's default) |
| Branch | `feature/m6-p1-survey-641`, stacked on `feature/m6-renovation-plan-346` | `git merge-base --is-ancestor origin/feature/m6-renovation-plan-346 HEAD` → true after merging the P0 tip `fac868f2fb` as `bff1ccec2a` |
| Worktree `HEAD` at survey start | `bff1ccec2a2f88596d4198335938c73daf4438df` | `git rev-parse HEAD` |
| `next` | `8ebaf8daad8eaac6331dff6fc048fb4411d7decb` | `git rev-parse next` |
| `upstream/next` | `03d71e321737a95ca7f3b8a738261dd6af790b43` | `git rev-parse upstream/next` after `git fetch upstream --no-tags` |
| Merge base `next`/`upstream/next` | `c445081a59518f37d9776e5412dd7b14910696f7` | `git merge-base next upstream/next` |
| ES pin | `16dbac5211eea7e70db7394372033be2be7df829` | `PKG_VERSION` in `projects/ROCKNIX/packages/ui/emulationstation/package.mk` |
| `rocknix/master` (ES) | `e282b05627c0d2193c19d7cc526176e047530c3d` | `git -C $ES rev-parse rocknix/master` after `git -C $ES fetch rocknix --no-tags` (moved from `cada856d8` during this fetch) |
| `batocera/master` (ES) | `b2ceb55a7e3d205a11f055b7d93c8be50cd6f9c9` | `git -C $ES rev-parse batocera/master` after `git -C $ES fetch batocera --no-tags` |
| ES merge base pin/`rocknix/master` | `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` | `git -C $ES merge-base rocknix/master $PIN` |
| ES worktree | `/home/max/Development/emulationstation-next.worktrees/m6-p1-survey`, detached at the pin | `git -C $ES worktree add --detach ...`; removed at the end with `git -C $ES worktree remove` |

`ES=/home/max/Development/emulationstation-next`.

## Counts re-derived at the start

| Quantity | Recorded (brief, `8ebaf8daad`) | Now (`bff1ccec2a`) | Delta | Command |
| --- | ---: | ---: | ---: | --- |
| tracked paths | 133,465 | 133,471 | +6 (this branch's files) | `git ls-files \| wc -l` |
| `package.mk` | 1,607 (1,040 + 567) | 1,607 (1,040 + 567) | 0 | `find packages projects -name package.mk \| wc -l`; `git ls-files 'packages/**/package.mk' 'projects/**/package.mk' \| wc -l` agrees |
| patches | 1,709 | 1,709 | 0 | `find packages projects -name '*.patch' \| wc -l`; `git ls-files` form agrees |
| fork-own (`$MB..next`) | 126,855 (125,225 `docs/`) | 126,855 (125,225) | 0 | `git diff --name-only $MB next \| wc -l` |
| fork-own (`$MB..HEAD`) | -- | 126,861 | -- | `git diff --name-only $MB HEAD \| wc -l` (the inventory's basis) |
| upstream-only | 912 | 912 | 0 | `git diff --name-only $MB upstream/next \| wc -l` |
| ES tracked at pin | 1,114 | 1,114 | 0 | `git -C $ES.worktrees/m6-p1-survey ls-files \| wc -l` |
| ES `es-app/src` + `es-core/src` | 486 | 486 | 0 | `find ... -type f \| wc -l`; `git ls-files` form agrees |
| ES fork-own | 236 | 236 | 0 | `git -C $ES diff --name-only $EMB $PIN \| wc -l` |
| ES upstream-only | -- | 2 | -- | `git -C $ES diff --name-only $EMB rocknix/master \| wc -l` |
| history, `upstream/next` | -- | 58,471 commits | -- | `git rev-list --count upstream/next` |
| history, fork side | -- | 2,871 commits | -- | `git rev-list --count $MB..next` |
| history, ES `rocknix/master` / fork side | -- | 7,477 / 724 | -- | `git -C $ES rev-list --count ...` |

No two commands for one quantity disagreed; no stop.

## Progress

- Futro: complete (`docs/futros/2026-10-22-m6-p1-survey.md`, and on #641)
- Pass 1 (Inventory): **complete** -- 134,589 rows (133,475 distribution + 1,114 ES), 12 areas, 26 plans (see § Pass 1)
- Pass 2 (Clustering): pending
- Pass 3 (Assessment): pending
- Pass 4 (Cross-reference): pending
- Pass 5 (Classification): pending
- Pass 6 (Reconciliation, then the preliminary review): pending
- Pass 7 (Action): pending -- gated on the maintainer's yes on #641

## Read first (brief § 3), what was read this session

From files, not from what loaded at session start (the instruction files load
truncated; lane-start comment on #641): the M7 stash on `next` (its opening
and running-state lines); every-session rules and `worktrees.md`,
`fork-workflow.md`, `issue-tracking.md`, `milestone-phase-naming.md`,
`learning-capture.md`, `ceremonies.md`, `decision-register.md`, `vm-first.md`,
`instruction-files.md`, `adversarial-council.md`, `engineering-practices.md`
(in context); `packaging-and-patches.md` (read from file);
`council-substrate-integrity.md` (owed before pass 6);
`docs/blindspot-register.md` (every entry's heading; 13, 51 and 64 in full);
`review-formats.md`; the multi-pass pattern outside the tree; plan § 2, § 5,
§ 6, § 6a (the whole plan was read).

## Pass 1: inventory

Generated by `tools/renovation-inventory --plans <scratch>/plans-p1` at
`61d1d016eb` (tool committed in `9966dbcd12`, unit display fixed in
`ea186f4f5f`, credential-shaped names escaped in `61d1d016eb`); plans in the pinned build image
`sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`
(`header.plan_runner`). 3.5 s of git, 68.3 s of plans.

```
$ tools/renovation-inventory --plans <scratch>/plans-p1; echo rc=$?
paths: 133475 (git ls-files: 133475)
es-paths: 1114 (git ls-files: 1114)
patches: 1709 (find: 1709)
unassigned: 0
ambiguous: 0
escaped: 2 (rows whose path matches a credential pattern, hyphens written as \u002d)
rc=0
```

The two escaped rows are upstream kernel patch names whose `mask-...` matches
the guards' API-key pattern `sk-[A-Za-z0-9_-]{24,}` once a path is file
content (the pre-commit guard refused the first commit of the inventory);
`header.escaped_rows` names them, `json.load` returns them byte-identical,
and `grep -cE "$SECRET_PATTERNS"` over both outputs is 0.

`docs/reviews/inventory.json` is 32,526,224 bytes (945,357 gzipped; under the
futro's 50 MB stop line); `tools/forbidden-terms-check --stdin` over both
outputs: 0 hits.

**The counters were seen to fail before the zero was trusted** (brief § 5):

| Constructed failure | Command | Result |
| --- | --- | --- |
| a path in no area, pure | `tools/renovation-inventory --self-test` | `PASS distribution:y/none -> 0 area(s)`; a bare `**` refused; `self-test: PASS` |
| a path in no area, on the real tree | `--inject-path renovation-fixture/matches-no-area` | `paths: 133474 (git ls-files: 133473)`, `unassigned: 1`, rc=1 |
| a path in two areas, on the real tree | `--areas <scratch>/areas-overlap.json` (the map plus an area claiming `Makefile`) | `ambiguous: 1 ... Makefile -> build-engine, fixture-overlap`, rc=1 |
| a real gap, unplanned | the first real run | `unassigned: 1 docs/retrospective/carry-forward.md`; the directory went to `records` |

**Reachability, checked against facts independent of the tool:**

| Claim | Check | Result |
| --- | --- | --- |
| a shipped product script is reached | `cloud_backup`'s row | `shipped` by GENERIC_X64, H700, RK3326, RK3566, SM8550 aarch64/x86_64 |
| the 32-bit plans' shape | `awk '{print $1}' plan-H700-arm.txt \| sort \| uniq -c` | only `build` lines, root `arm`; the first parser kept only `:`-suffixed names and had to accept both (`install rclone`, `build arm`) |
| subdevice bootloaders | `grep u-boot plan-H700-aarch64.txt` | container plan: `u-boot-DDR3`, `u-boot-DDR4`, `atf`; host plan: none. Only H700-aarch64 (665 vs 671 lines) and RK3566-aarch64 (704 vs 712) differ between host and container |
| shadowed generic recipes | `projects/ROCKNIX/packages/sysutils/{busybox,systemd}/package.mk` | present, no `${ROOT}/packages/...` source line, so `get_pkg_directory` never resolves the generic directory: 45 and 38 generic paths unreached |
| explicit file references into a package directory | `git grep -nE '\$\{?ROOT\}?/(packages\|projects)/...'` excluding `package.mk` | none that read a file (the `create_addon` and `LINUX_DEPENDS` lines are roots) |
| the other nine projects | `git grep -lE 'projects/(ARM\|Allwinner\|...)'` over packages, projects/ROCKNIX, scripts, config, distributions, Makefile | no hit: all 407 paths unreached |

**Totals** (from `inventory.md`, generated): 134,589 rows, 24,817,974 lines;
4,420 shipped, 494 unshipped, 2,643 unreached (421,484 lines, 977 units),
127,032 `n/a`; 55 overlap paths.

**Leads for the slices** (P1 answers no Q1-Q7; each is a lead for the named
area's slice to confirm or overturn):

- *patches-and-configs, devices*: all 277 `packages/linux/patches/` are
  unreached: the ROCKNIX `linux` override takes `PKG_DIR` and its relative
  `PKG_PATCH_DIRS` resolve under it; the generic kernel patches are carried
  and never applied.
- *emulators-and-cores*: `vitaquake2-lr`'s four `patches/x86_64/` directories
  never apply: `scripts/unpack` sets `PATCH_ARCH=x86` on x86_64, and the core
  is built for AMD64-x86_64. The aarch64 siblings apply.
- *build-engine*: `distributions/ROCKNIX/config/functions:224` computes
  `SUBDEVICES` with `xmlstarlet ... 2>/dev/null`; without the tool it is
  silently empty and the plan loses bootloaders (guards fail closed). The
  container has it; `tools/viewplan` on a host does not say so.
- *generic-packages*: the generic `busybox` and `systemd` directories are
  wholly shadowed by ROCKNIX overrides (Q6 candidates, with
  `engineering-practices.md` § Before deleting a duplicate).

**Deltas against the brief:** the council toolchain is 46 of `scripts/`' 76
tracked files, not 45: `fork-workflow.md`'s list includes
`scripts/lib/verifier-pins.ts`, which the brief's list omits; it is placed
under tooling-and-guards with the rest. `podman-bin` is an upstream tool
directory, placed under build-engine.

## Item analysis table

Filled from pass 2 (one row per area).

## Relationships discovered

Filled from pass 4.

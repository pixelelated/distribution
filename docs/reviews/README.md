# Reviews: the codebase renovation program (M6)

The whole codebase, reviewed and brought up to date in slices, progressively,
beside feature work (D-WORKFLOW-083, D-WORKFLOW-102, D-WORKFLOW-181). The
milestone is M6; the epic is #339; the plan for the plan is #346.

| File | What it is | Written by |
| --- | --- | --- |
| `plan-for-the-plan.md` | how the program is planned: the survey, the slicing, the ordering lenses, the per-slice procedure, the brief an executor receives, the drift rules, the ledgers | P0 (#346) |
| `order.md` | the slices in order, each with its lens, paths, line count, the release it gates, its depth and the evidence that closes it (#346's first criterion) | P1 |
| `inventory.json`, `inventory.md` | every path's root, provenance tier, language, lines, patches, last fork and upstream commits, reachability; the per-area totals | `tools/renovation-inventory` (P1), re-run at every slice close |
| `status.md` | one row per slice: area, lines, depth, state, reviewed-at, drift since | `tools/renovation-status` (P1) |
| `briefs/<slice>.md` | the brief an executing session runs a slice from, ten sections, committed before dispatch | the planner |

The audits themselves live under `docs/audits/<date>-epic-m6-<slice>/`, the
retros under `docs/retros/`, and the decisions in `docs/decision-register.md`.

## The tools

All fork-only (listed in `fork-workflow.md` § Personal paths, `PERSONAL_PATTERNS`
in `.githooks/pre-push`, and `instruction-files.md` § The fork's own tools).

### `tools/renovation-inventory`

Writes `inventory.json` (a header, the column names, then one row per tracked
path of both trees, sorted) and `inventory.md` (the per-area totals and the
unreached and unshipped sets). The hand-written input is `areas.json`: a list
of `{"area", "epic", "globs"}`, where a glob is relative to the distribution
unless prefixed `es:`, a `!` glob excludes within its own area, `**` crosses
`/`, and `{a,b}` alternates globs (no nesting).

It prints five lines and exits 1 unless each pair agrees and both counters are
0, or 2 when it cannot run:

```
paths: N (git ls-files: N)        # the distribution at HEAD
es-paths: N (git ls-files: N)     # the ES checkout at HEAD (a detached worktree at the pin)
patches: N (find: N)              # *.patch under packages/ and projects/
unassigned: N                     # a path in no area
ambiguous: N                      # a path in two or more areas
```

What its columns mean:

- **tier**: `fork-own` (changed since the merge base with `upstream/next`, or
  on ES with `rocknix/master`), `upstream-carried` (everything else), or
  `vendor-carried` (every `*.patch` and kernel `linux*.conf` under
  `packages/` or `projects/`, with `tier_note: fork-written` when fork-own).
  `overlap` marks a fork-own path upstream also changed since the base.
- **lines**: git's numstat against the empty tree; `null` for a binary.
- **patches**: on a `package.mk` row, the patches under that package's own
  directory; `null` elsewhere.
- **last_fork_commit**, **last_upstream_commit**: `<hash10> <date>` of the
  newest commit touching the path on each side, from one `git log
  --name-only` pass per side.
- **reach**: `shipped` (in a plan of a device we ship, `device-builds.md` §
  Our devices), `unshipped` (only in other devices' plans), `unreached` (a
  package or project path no plan reaches), `n/a` (a path no image plan can
  hold: the build engine, tools, doctrine, records). `reachable_by` and
  `buildable_by` name the plans.

How reachability is computed. `tools/viewplan` runs once per device and
architecture the `Makefile` builds (`image` for 64-bit, the virtual `arm` for
32-bit where `ENABLE_32BIT` is true), in the **build image the Makefile pins by
digest**, with the checkout mounted read-only and no network. It does not run
on the host by default: the host lacks `xmlstarlet`, which
`distributions/ROCKNIX/config/functions` uses to compute `SUBDEVICES` with its
errors discarded, so a host plan silently drops H700's and RK3566's subdevice
bootloaders (`--runner host` is the explicit, recorded alternative). Each
plan package is then sourced with `source_package`, and its `PKG_DIR`,
`PKG_VERSION`, `PATCH_ARCH` and `PKG_PATCH_DIRS` give exactly the patch
directories `scripts/unpack` would apply. A path in a package directory is
reached when that directory is a plan package's `PKG_DIR` (a patch only when
its directory is selected); a generic `package.mk` sourced by a reached
override is reached with it; a device's own files by that device's plans;
`projects/ROCKNIX`'s bootloader, filesystem, options and `config.xml` by
every plan; the other projects and the other `distributions/` (nothing sets
`DISTRO` but its `ROCKNIX` default) by none; the ES tree by the plans that build
`emulationstation`. Reachability errs toward reached: a file in a reached
package counts as reached even when its recipe installs it only for some
devices, so `unreached` is a conservative claim and the slice read refines
the rest.

`--self-test` proves the area counters and the glob rules can fail;
`--inject-path PATH` adds a synthetic path to a real run (it must fail with
`unassigned: 1`); `--plans DIR` keeps the plan files.

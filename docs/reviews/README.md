# Reviews: the codebase renovation program (M6)

The whole codebase, reviewed and brought up to date in slices, progressively,
beside feature work (D-WORKFLOW-083, D-WORKFLOW-102, D-WORKFLOW-181), and it gates no release (D-WORKFLOW-187). The
milestone is M6; the epic is #339; the plan for the plan is #346.

| File | What it is | Written by |
| --- | --- | --- |
| `plan-for-the-plan.md` | how the program is planned: the survey, the slicing, the ordering lenses, the per-slice procedure, the brief an executor receives, the drift rules, the ledgers | P0 (#346) |
| `order.md` | the slices in order, each with its lens, paths, line count, any reading-order prerequisite (the renovation gates no release, D-WORKFLOW-187), its depth and the evidence that closes it (#346's first criterion) | P1 |
| `inventory.json`, `inventory.md` | every path's root, provenance tier, language, lines, patches, last fork and upstream commits, reachability; the per-area totals | `tools/renovation-inventory` (P1), re-run at every slice close |
| `assessment.md` | per area, the evidence for the six ordering lenses: security-token files, blindspot, friction, bug and open-issue mentions, churn since 2026-06-01, change since the merge base, callers, unreached and unshipped sizes | `tools/renovation-inventory --assess` (P1), from `inventory.json` and the tracker |
| `cross-reference.md` | every area against every other: call edges, shared state, rule-to-area and patch-to-area edges | `tools/renovation-inventory --cross` (P1) |
| `slices.json` | the order's hand-written input: each slice's number, area, kind, lens, selector, reading-order prerequisite (`read_before`), depth, interacting subsystems and closing evidence; the security, state and launch-path globs the drift tool reads | P1, then the planner when the order changes |
| `areas.json` | the area map: every tracked path in exactly one area (the one hand-written input to the inventory) | P1, edited when an area is split or an epic filed |
| `p1-tracking.md` | the survey's multi-pass tracking file: hashes, counts with their commands, each pass's evidence | P1 |
| `status.md` | the `order:` row, then one row per slice: area, lines, depth, state, issue, reviewed-at, fixed-at, drift since | `tools/renovation-status --write docs/reviews/status.md` (P1), at every slice close |
| `drift.md` | per closed slice, what changed under its paths since `fixed-at` | `tools/renovation-drift --write docs/reviews/drift.md`, at every slice close, the renovation's own cadence, not a release step (D-WORKFLOW-187) |
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
- **reach**: `shipped` (in a plan of a device we ship: H700 and SM8550,
  D-WORKFLOW-185), `test` (in the test image's plan, GENERIC_X64, and no
  shipped device's), `unshipped` (only in other devices' plans), `unreached` (a
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

`--assess` writes `assessment.md` from the committed `inventory.json` and the
tracker (`gh issue list --repo pixelelated/distribution`, bounded, failing if
a list reaches its limit): per area, over its reached code files, the files
matching the brief's security tokens; the blindspot entries, friction lines,
closed bugs and open issues naming one of the area's identifiers (its units'
and code files' names, six characters or more) as a whole word; commits since
2026-06-01 and the change since the merge base on both trees; callers of its
ten largest units outside it; its unreached and unshipped sizes. Every count
is a search, so a lead: the slice read confirms or overturns it. Records are
not scored.

`--cross` writes `cross-reference.md`: for every ordered pair of the ten code
areas, the area's code files naming an identifier only the other area owns;
the shared state (`system.cfg`, `es_settings.cfg`, the cloud configuration,
stamps and lock, `rclone.conf`, `retroarch.cfg`, the proxy's state, ...)
each area touches; each rule's `paths:` globs resolved to areas; each patch
against the area of the package it patches.

`--order` reads `slices.json`, puts every inventory row in its slice (a row
belongs to a slice when its area is one of the slice's, it matches the
slice's globs, and its reach is one the slice names; a `rest` slice takes
only rows no other slice in its area claims), prints each slice's paths,
lines, read lines and fork-own read lines, and renders the block of
`order.md` between its markers. It exits 1 when a row is in no slice or in
two, when a slice is empty, or when one of the first three reads more than
12,000 lines (a currency slice counts its fork-own lines, a table none).
`--no-write` prints only.

`--slice-issues DIR` writes each slice issue's title (`M6.P2 E339/T<k>: <area>:
<title>`) and body (scope, `reviewed-at:` and `fixed-at:` empty, the VM
question, five agent-verifiable criteria) into DIR, from `slices.json` and
`inventory.json`; it touches no tracker. Pass 7 files them after the
maintainer's yes.

`--self-test` proves the area counters and the glob rules can fail;
`--inject-path PATH` adds a synthetic path to a real run (it must fail with
`unassigned: 1`); `--plans DIR` keeps the plan files.

### `tools/renovation-drift`

For every slice whose issue is closed as completed with a `fixed-at:` line
(plus `fixed-at-es:` for EmulationStation paths; read from the slice issues,
the same reader `renovation-status` imports, #957), `git diff --numstat
<baseline>..next`, the baseline being `slices.json`'s `drift_checked_at` once
a drift review has accepted the changes, else the issue's fixed-at, filtered
to the slice's paths (the same membership `--order` uses; the ES
target is the pin `next` carries). It reports files, lines changed, the share
of the slice's lines, and any `sensitive` file touched (a glob's `!` exclusions honoured), with plan § 8's
verdict: `small` (under 20 % and nothing sensitive: an issue-tier pass over
the diff) or `re-open`. Exit 1 when any slice must re-open, 2 when it cannot
run. `--pretend SLICE=HASH[,es=HASH]` sets a baseline for one run (and
`--no-issues` reads no tracker): on
2026-10-22 a pretend close of T1 at the merge base reported `re-open`
(29 files, 3,273 lines, 24.6 %, all three sensitive lists) and exit 1, and
the same at `HEAD` reported `none` and exit 0. `--self-test` checks the
thresholds.

### `tools/renovation-status`

Writes `status.md`: the `order:` row from `order.md`'s review status line,
then one row per slice, its lines from the inventory, its depth from
`slices.json`, and its state from the slice issue on milestone M6 (title
`M6.P2 E<epic>/T<k>: ...`; body lines `reviewed-at:`, `fixed-at:`,
`fixed-at-es:`) and the audit folders: `unreviewed`, `reading`,
`remediating`, `fixed` (both lines set, the issue still open), `closed`
(closed as completed with fixed-at), `drifted` (closed, and drift's verdict
for that slice is re-open) or `withdrawn` (closed for another reason). *Drift
since* is drift's share of the slice and its verdict, from
`renovation-drift`'s own functions, imported (#957). One bounded `gh issue
list`, drift's; it fails at its limit.

### The renovation face of `tools/lint-audit-artifacts`

For an audit folder whose name carries `-epic-m6-` (a renovation slice), the
lint also requires a `## Renovation face` section in `04-analysis.md` with a
`### Q1` to `### Q7` subsection each (plan § 4's seven questions), a
`punch_index` YAML block, and on every item `question: Q1..Q7`, or
`question: none` with its reason on the line or in `question_reason:`.
`tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass`
passes (`PASS`, rc 0) and `...-fail`, the same folder without the face,
fails on exactly those two checks (rc 1). On 2026-10-22 a face missing Q4
and a `question: none` without a reason each failed alone, and the 21
existing audit folders kept their verdicts.

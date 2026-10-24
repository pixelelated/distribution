#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""t4-coverage.py -- 02's coverage table for M6 T4 (#651, criterion 7): one
row per path of the 36, with its group (brief § 2), its lines at the hash,
when it loads, and Q1 to Q7 each answered by a finding of 02 or `none` with
what was read.

    python3 -I t4-coverage.py <read-tree> <paths.txt> <q6-rules.md>

The answers are the lane's; the script joins them to the tree's line counts
and the load column of `t4-q6.py rules`, and refuses when a path has no row,
a row has no path, or a cell is empty.
"""
import re, sys

root, paths, q6 = sys.argv[1:4]
loads = {}
for l in open(q6).read().splitlines():
    m = re.match(r"^\| `([^`]+)` \| \d+ \| .* \| (every session|on a match) \|", l)
    if m: loads[".claude/rules/" + m.group(1)] = m.group(2)
N = "none"
# path: (group, Q1, Q2, Q3, Q4, Q5, Q6, Q7)
ROWS = {
    "CLAUDE.md": (1, "F-07, F-08, F-26", "F-08 (the brand)", "F-03, F-04, F-05", "IDs resolve (`t4-q4.py ids`); F-04's tool scope", "202 lines, every session", N + ": a pointer file", "F-06, F-09; differs from `AGENTS.md` (F-01)"),
    "AGENTS.md": (1, "F-07, F-08, F-26", "within Codex's budget; names all 30 (`rules-check` `agents`, `list`)", "F-01, F-03, F-04", "IDs resolve", "351 lines; Codex reads it whole", N + ": a pointer file", "F-01, F-09"),
    "NAMING.md": (1, "time-bound #416 line (reader; not re-verified)", "`pixelelated` lowercase throughout (grep)", N + " found by this lane; the reader checked its paths (a lead, not re-run here)", "D-WORKFLOW-128/144/151, D-CLOUD-174-176 resolve", "60 lines; loads nowhere", N, "title is the issue's, not the file's (`01`)"),
    ".claude/rules/instruction-files.md": (2, "F-18, F-26", "front matter ok (`rules-check`)", "F-22", "72 tools all exist (`t4-q6.py tooltable`)", "every session", "F-18", "F-22"),
    ".claude/rules/working-principles.md": (2, N, "ok", N + " found: its index rows name rules that exist", "IDs resolve", "every session", N, N + ": the ladder is the slice's own test"),
    ".claude/rules/learning-capture.md": (2, N, "ok", N + " found", "IDs resolve", "every session", N, "dated counts (*17 of 29*) read as history"),
    ".claude/rules/decision-register.md": (2, N, "ok", N + " found", "IDs resolve", "every session", N, "silent on open rows (F-23)"),
    ".claude/rules/ceremonies.md": (2, N, "ok", "F-02", "IDs resolve", "every session", N, N),
    ".claude/rules/issue-tracking.md": (2, N, "ok", N + " found", "D-QA-044 refined by D-QA-051, both cited where they apply", "every session", N, "dated counts (*46 of 479*) read as history"),
    ".claude/rules/milestone-phase-naming.md": (2, N, "ok", N + " found", "IDs resolve", "every session", N, N),
    ".claude/rules/adversarial-council.md": (2, N, "ok", N + " found", "IDs resolve", "every session", N, "the seat-length section is long for the seats it now concerns"),
    ".claude/rules/bugs-are-agent-first.md": (2, N, "ok; says *no `paths:`* in its first paragraph", N + " found", "IDs resolve", "every session", N, N),
    ".claude/rules/vm-first.md": (2, N, "ok", N + " found", "D-QA-007, D-QA-044 (both still decided; refined, not reversed)", "every session", N, N),
    ".claude/rules/least-surprise.md": (2, N, "ok", "F-10 (`:18-20`)", "F-10: D-CLOUD-109 cited, D-CLOUD-130 in force", "every session", N, N),
    ".claude/rules/player-language.md": (2, N, "ok", N + " found", "IDs resolve", "every session", N, N),
    ".claude/rules/time-to-play.md": (2, "F-10", "ok", "F-10", "F-10: D-CLOUD-076/109 cited as current", "every session; this slice changes neither number", N, N),
    ".claude/rules/documentation-accuracy.md": (2, N + ": retired tools said retired", "ok", N + " found", "IDs resolve", "every session", N + ": its drift list is dated", N),
    ".claude/rules/change-log.md": (2, N, "ok", N + " found", "IDs resolve", "on a match (`projects/ROCKNIX/packages/**`, the change log)", N, "`:41` cites the moved § Conventions (redirected by `es-native-ui.md`)"),
    ".claude/rules/engineering-practices.md": (3, N, "ok", N + " found in the sections re-read (the filters ran as written, `02` § Command blocks)", "IDs resolve", "every session; 836 lines", N, "F-27: a dozen sections"),
    ".claude/rules/upgrade-and-install.md": (3, N, "ok", N + " found", "IDs resolve", "every session", N, "F-22 (two tools pointed here, unnamed)"),
    ".claude/rules/fork-workflow.md": (3, "F-19, F-26", "ok; the personal-paths list matches the hook (`rules-check` `tools`)", "F-19 (`:62`)", "#644 f18 waits on #645", "every session", N, "the fork-only tools list is one 100-entry line"),
    ".claude/rules/worktrees.md": (3, "F-17, F-26", "ok", N + " beyond #640's paths", "IDs resolve", "every session", N, N),
    ".claude/rules/device-builds.md": (3, "F-17, F-19, F-26", "ok", N + " found beyond F-19; #644 f5 holds", "IDs resolve", "every session; 695 lines", N, "F-22 (`fork-newdrive`)"),
    ".claude/rules/release-candidates.md": (3, N, "ok", N + " found", "D-QA-049 reversed by D-WORKFLOW-062, which it cites", "every session", N, "F-22 (four tools pointed here, unnamed)"),
    ".claude/rules/packaging-and-patches.md": (3, "F-17", "ok", N + " found by this lane; the reader's `PKG_DEPENDS_TARGET` lead not re-verified", "IDs resolve", "on a match (`packages/**`, `projects/**`)", N, "`:28-47` repeat `CLAUDE.md` nearly verbatim (reader)"),
    ".claude/rules/generic-x64-vm-testing.md": (4, "F-16, F-26", "ok", "F-11, F-12, F-13, F-14, F-15", "IDs resolve", "on a match; 1,398 lines, the largest", N, "F-27"),
    ".claude/rules/rclone-cloud-sync.md": (4, "F-21", "ok", "F-21", "IDs resolve; D-CLOUD-050 cited where the content tier is", "on a match; 895 lines", "13 retired mentions said retired (`t4-q6.py retired`)", "F-22; duplicates of other rules (reader)"),
    ".claude/rules/handheld-evidence.md": (4, N, "ok", N + " found: every fact the reader checked holds", "IDs resolve", "on a match; its `docs/**` matches 125,306 paths (F-27)", N, "a maintenance-mask section under the VM heading (reader)"),
    ".claude/rules/council-substrate-integrity.md": (4, N, "description is long (adopted verbatim; `instruction-files.md` excuses it)", "F-20", "IDs resolve", "on a match", "F-20: `research/council-research/**` matches 0", "another estate's names (F-20)"),
    ".claude/rules/es-native-ui.md": (4, N, "ok", N + " found", "D-CLOUD-130's question described", "every session (`**`)", N, "F-22 (two tools pointed here, unnamed)"),
    ".claude/rules/es-player-text.md": (4, N, "ok", N + " found", "D-UI-101 cited for the cards' content (D-UI-109 changed their order)", "every session (`**`)", N, "the outcome section reads as a dated list"),
    ".claude/rules/es-ui-style-guide.md": (4, N, "ok", N + " found", "IDs resolve", "every session (`**`)", N, N),
    ".claude/rules/es-code-traps.md": (4, "F-17, F-26", "ok", "F-11 (`:182`)", "IDs resolve", "every session (`**`)", N, N),
    "docs/decision-register.md": (5, N, "F-23", N + ": a record", "the ledger itself; `register-check` 667 IDs once", "728 lines at the hash; read by `archaeology`, `register-check`", N + ": a decided row cited by nothing is a record", "F-23"),
    "docs/blindspot-register.md": (5, N, "F-25 (#811)", N + ": a record", "40 IDs cited across the two ledgers resolve (`t4-q4.py ledger-ids`)", "1,198 lines; read by `ceremony-check` `guards`", "every named guard exists (`t4-q6.py blindspots`)", "three entry formats (reader)"),
    "docs/friction-log.md": (5, N, "F-24", "F-02 (its check)", "IDs resolve", "856 lines; read by `ceremony-check` `friction`", "F-02: 125 entries no check reads", "F-24"),
}
ps = open(paths).read().split()
if set(ps) != set(ROWS):
    sys.exit(f"t4-coverage: paths without a row {sorted(set(ps) - set(ROWS))}; rows without a path {sorted(set(ROWS) - set(ps))}")
print("| Path | Group | Lines at the hash | Loads | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |")
print("| --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |")
for p in sorted(ps, key=lambda p: (ROWS[p][0], p)):
    r = ROWS[p]; n = open(f"{root}/{p}").read().count("\n")
    ld = loads.get(p, "a register (loads nowhere)" if p.startswith("docs/") else "the entry file" if p in ("CLAUDE.md", "AGENTS.md") else "nowhere")
    cells = [str(r[0]), str(n), ld] + list(r[1:])
    if any(not c.strip() for c in cells): sys.exit(f"t4-coverage: empty cell for {p}")
    print(f"| `{p}` | " + " | ".join(cells) + " |")
print()
print(f"<!-- t4-coverage: {len(ps)} rows -->")

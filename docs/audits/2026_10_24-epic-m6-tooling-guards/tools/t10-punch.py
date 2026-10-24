#!/usr/bin/env python3
"""t10-punch.py -- write T10's 05-punch-list.md from 02's finding headings, the
graded severities (04 § Second opinion) and the filed bugs. One item per
finding, PL-nn for F-nn. Run from the lane worktree:
  python3 -I docs/audits/2026_10_24-epic-m6-tooling-guards/tools/t10-punch.py <grades.json> <bugs.json>
"""
import json, re, sys
A = "docs/audits/2026_10_24-epic-m6-tooling-guards/"
G = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2]))
sev = {f: k for k, v in G.items() for f in v}
f2 = open(A + "02-forward-audit.md").read()
heads = dict(re.findall(r"^\*\*(F-\d\d) — (.+?)\*\*(?: |$)", f2, re.M))  # one line each: a heading never wraps
assert len(heads) == 44 and set(heads) == set(sev), (len(heads), set(heads) ^ set(sev))
covers = {"f41": ["F-41", "F-10"], "f42": ["F-42", "F-12", "F-13", "F-14"], "f05": ["F-05", "F-15", "F-44"], "f08": ["F-08", "F-43"], "f27": ["F-27", "F-28", "F-29"]}
track = {}
for b in B:
    for f in covers.get(b["key"], ["F-" + b["key"][1:]]): track[f] = "#%d" % b["number"]
lead = {
 "F-16": "the coordinator's recorded lead (#657, 16:57 UTC ruling: a contract question under D-WORKFLOW-028 and #258 PL-004; not a stream)",
 "F-30": "the coordinator's recorded lead (#657, 16:57 UTC ruling: the CI half of D-WORKFLOW-061; not a stream)",
 "F-31": "a Renovation item with the coordinator's disposition pending (#657)",
 "F-32": "#640 (the legacy layout's cutover), with `fork-worktree:72,74`'s hint named first",
 "F-33": "the coordinator's lead for the build-engine area (the merge of `upstream/next`), and #585 for the empty-success paths as a contribution candidate",
 "F-34": "a Renovation item with the coordinator's disposition pending (#657)",
}
for f, t in lead.items(): track[f] = t
assert set(track) == set(sev), set(sev) ^ set(track)
def cat(f):
    if f in ("F-01","F-02","F-03","F-10","F-35","F-36","F-37","F-38","F-39","F-40","F-41","F-07","F-30","F-31"): return "Security"
    if f in ("F-11","F-12","F-13","F-14","F-42"): return "Data Safety"
    if f in ("F-31","F-32","F-33","F-34"): return "Renovation"
    return "Correctness"
q = {"F-06": "Q6", "F-14": "Q2", "F-29": "Q7", "F-30": "Q6", "F-31": "Q2", "F-32": "Q1", "F-33": "Q4", "F-34": "Q7", "F-43": "Q7"}
area = lambda f: ("the hooks: `.githooks/`" if cat(f) == "Security" and f not in ("F-07", "F-30", "F-31") else
                  "`tools/fork-worktree`" if cat(f) == "Data Safety" else "the fork CI and its tools" if f in ("F-06","F-07","F-30","F-31") else "the record checkers: `tools/`")
out = ["# Punch list (Phases 5 and 6) — M6.P2 T10, the guards (#657)", "",
 "One item per finding of `02` (PL-nn for F-nn), with the severities graded in `04` § Second opinion. A `bug` carries every defect the coordinator has not held as a lead (D-WORKFLOW-187). Five bugs carry more than one item each: #937 (PL-41, PL-10), #940 (PL-42, PL-12, PL-13, PL-14), #943 (PL-05, PL-15, PL-44), #945 (PL-08, PL-43) and #957 (PL-27, PL-28, PL-29).",
 "",
 "Every constructed input is a recipe, never bytes: a stand-in list, values built from `printf` pieces, a throwaway repository (the coordinator's 17:44 ruling). Every item answers *Can this be done on the VM?* No: the hooks, the tools and the CI run on the build host or on GitHub, and their proof is a suite, a fixture or a run record (brief § 5).", ""]
idx = ["```yaml", "punch_index:"]
gate = ["## Phase 7 resolution gate", "", "Pre-issue: every item is open until the coordinator's stage-E dispositions. Each row names what tracks the item.", "", "| Item | Outcome | Tracked |", "| --- | --- | --- |"]
for f in sorted(sev):
    pl = "PL-" + f[2:]; what = " ".join(heads[f].split())
    out += [f"## {pl}: {what[:200]}{'…' if len(what) > 200 else ''}",
            f"- **Severity:** {sev[f]}", f"- **Category:** {cat(f)}", f"- **Question:** {q.get(f, 'Q3')}", f"- **Source Finding:** {f}",
            f"- **Owner area:** {area(f)}", f"- **Where:** `02-forward-audit.md` § Findings, {f} (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)",
            "- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name" if track[f].startswith("#") else "- **Ladder:** recorded; the next rung is the coordinator's",
            "- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it",
            "- **Already written:** the tracked issue's *Already written:* line" if track[f].startswith("#") else "- **Already written:** nothing on a device or in a cloud; a record or a hint, read where it is",
            f"- **Acceptance:** {'the criteria of ' + track[f] if track[f].startswith('#') else 'the disposition recorded on #657'}",
            f"- **Tracked:** {track[f]}", ""]
    idx += [f"- id: {pl}", f"  severity: {sev[f]}", f"  category: {cat(f)}", f"  question: {q.get(f, 'Q3')}", f"  source_finding: \"{f}\"", f"  tracked: \"{track[f][:80]}\"", "  outcome: \"open\""]
    gate.append(f"| {pl} | Open | {track[f]} |")
idx.append("```")
out += ["## Index", ""] + idx + [""] + gate + [""]
open(A + "05-punch-list.md", "w").write("\n".join(out))
print("items", len(sev), {k: len(v) for k, v in G.items()}, "bugs", len(B))

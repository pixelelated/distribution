#!/usr/bin/env python3
"""T31 (#678): the audit issue's body, generated from 05-punch-list.md (T26's t26-issue-body.py, adapted).

    python3 -I t31-issue-body.py <05-punch-list.md> <head commit> > body.md

One checkbox per item: its severity, question and source from the punch
index, its title from its heading, and the artifact that ticks it. Asserts
27 items, the index and the headings agreeing.
"""
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
head = sys.argv[2]
titles = dict(re.findall(r"^## (PL-\d+): (.*)$", text, re.M))
idx = re.findall(r"- id: (PL-\d+)\n  severity: \"(\w+)\"\n  category: (\w+)\n  question: (Q\d)\n  source_finding: \"([^\"]*)\"", text)
assert len(idx) == len(titles) == 27, (len(idx), len(titles))
sev = {}
for _, s, *_ in idx:
    sev[s] = sev.get(s, 0) + 1
out = [
    "Punch list of the M6.P2 T31 audit: EmulationStation's other pages (#678).",
    "",
    "- **What was read:** the 76 paths under `es-app/src/guis/` outside GuiMenu, the cloud, RetroAchievements, offline-scan and Wi-Fi pages, at the pin `16dbac5211`: the twelve fork-touched files whole, the 64 upstream ones (byte-identical to `rocknix/master`) at their leads' lines and by six generators.",
    "- **reviewed-at:** `da7922a7bd`; **reviewed-at-es:** `16dbac5211`.",
    "",
    "**Independent depth:** one seat, two keyed calls and no others (`stage-c/keyed-calls.txt`).",
    "- **GPT-6 Astra at `max`:** probe PASS; refutation PASS, served `openai/gpt-6-astra` by OpenAI; 43 items (41 accepted, 1 in part, 1 not kept; `stage-c/astra-grades.md`).",
    "- **The packet:** 411,984 bytes; the three-way scan found no value (`second-opinions/packet-manifest.json`); 5,798 of 15,537 slice lines sent, the trimmed ranges named.",
    "",
    "**One guest window,** 12:26:47 to 12:45:00 UTC on 2026-10-27, on the M6 image (M7's composition over the pin): L-01, L-03, L-06, L-07, L-11, L-12, L-13, L-15 and L-26 shown on the image; G10 and G11 not reached (`02` § The guest cycle). **Five host harnesses** fail at the pin and pass their controls (`stage-c/runs.txt`).",
    "",
    "- **The folder:** `docs/audits/2026_10_27-epic-m6-es-pages/` on `feature/m6-es-pages-678` at `%s`." % head,
    "- **The list:** `05-punch-list.md`. `tools/lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.",
    "",
    "**%d items:** 0 critical, %d high, %d medium, %d low, 0 info. Every item is open until the stage-D ruling and stage F's outcomes." % (
        len(idx), sev.get("High", 0), sev.get("Medium", 0), sev.get("Low", 0)),
    "",
    "## Items",
    "",
]
for pl, s, cat, q, src in idx:
    out.append("- [ ] **%s** (%s, %s, %s): %s **Checked by:** its Phase 7 row in `05-punch-list.md` at the outcome the stage-D ruling sets (a commit with its proof, an issue, or the record as written)." % (pl, s, q, src, titles[pl]))
print("\n".join(out))

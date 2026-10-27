#!/usr/bin/env python3
"""T26 (#673): the audit issue's body, generated from 05-punch-list.md.

    python3 -I t26-issue-body.py <05-punch-list.md> <head commit> > body.md

One checkbox per item, its severity, question and source from the punch
index, its title from its heading, and the artifact that ticks it.
"""
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
head = sys.argv[2]
titles = dict(re.findall(r"^## (PL-\d+): (.*)$", text, re.M))
idx = re.findall(r"- id: (PL-\d+)\n  severity: \"(\w+)\"\n  category: (\w+)\n  question: (Q\d)\n  source_finding: \"([^\"]*)\"", text)
assert len(idx) == len(titles) == 29, (len(idx), len(titles))
sev = {}
for _, s, *_ in idx:
    sev[s] = sev.get(s, 0) + 1
out = [
    "Punch list of the M6.P2 T26 audit: EmulationStation's main menu, GuiMenu (#673).",
    "",
    "- **What was read:** `es-app/src/guis/GuiMenu.{h,cpp}` at the pin `16dbac5211`, with the scripts it meets at `8ebaf8daad`.",
    "- **reviewed-at:** `db7be4b104`; **reviewed-at-es:** `16dbac5211`.",
    "",
    "**Independent depth:** one seat, two keyed calls and no others (`stage-c/keyed-calls.txt`).",
    "- **GPT-6 Astra at `max`:** probe PASS; refutation PASS, served `openai/gpt-6-astra` by OpenAI; 42 items (40 accepted, 1 in part, 1 plausible; `stage-c/astra-grades.md`).",
    "- **The packet:** 563,026 bytes; the three-way scan found no value (`second-opinions/packet-manifest.json`); `GuiMenu.cpp` 6,305 of 11,747 lines sent, the trimmed ranges named.",
    "",
    "**One guest window,** 08:08:16 to 08:31:02 UTC on 2026-10-27, on the M6 image (M7's composition over the pin): L-01, L-09, L-10, L-18 and L-20 proved on the image; L-02 and L-16 not reached (`02` § The guest cycle).",
    "",
    "- **The folder:** `docs/audits/2026_10_27-epic-m6-es-guimenu/` on `feature/m6-es-guimenu-673` at `%s`." % head,
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

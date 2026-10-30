"""Render 05-punch-list.md from stage-c/punch-items.py (#680).

    python3 -I t33-05.py <audit folder> [header-file]

One `## PL-NN: title` section per item, with every field the lint and
#680's checkboxes read (Severity, Category, Question, Family, Source
Finding, Owner area, What, Fix shape, Can this be done on the VM?,
Already written, Acceptance, Disposition with its `question:`); then the
Phase 7 resolution gate (one row per item, `Open` until stage F) and the
`punch_index` YAML, whose outcomes agree with the table. Exits 1 on a
missing field, a duplicate id or ids out of order.
"""
import os
import sys

A = sys.argv[1]
ns = {}
exec(open(os.path.join(A, "stage-c/punch-items.py")).read(), ns)
items = ns["ITEMS"]
header = open(sys.argv[2]).read() if len(sys.argv) > 2 else ""
ids = [i["id"] for i in items]
need = ("id", "title", "sev", "cat", "q", "fam", "src", "owner", "what", "fix", "vm", "aw", "acc", "disp")
fail = [f"{i.get('id','?')} lacks {k}" for i in items for k in need if not i.get(k)]
if len(set(ids)) != len(ids) or ids != ["PL-%02d" % n for n in range(1, len(ids) + 1)]:
    fail.append("ids not PL-01.. in order: " + ", ".join(ids))
if fail:
    print("FAIL t33-05: " + "; ".join(fail)); sys.exit(1)
out = [header.rstrip("\n"), "", "---", ""]
for i in items:
    out += [f"## {i['id']}: {i['title']}", "",
            f"- **Severity:** {i['sev']}", f"- **Category:** {i['cat']}", f"- **Question:** {i['q']}",
            f"- **Family:** {i['fam']}", f"- **Source Finding:** {i['src']}", f"- **Owner area:** {i['owner']}",
            "- **What:**"] + [f"  - {w}" for w in i["what"]] + \
           ["- **Fix shape:**"] + [f"  - {w}" for w in i["fix"]] + \
           [f"- **Can this be done on the VM?** {i['vm']}", f"- **Already written:** {i['aw']}", "- **Acceptance:**"] + \
           [f"  - [ ] {a}" for a in i["acc"]] + \
           [f"- **Disposition (proposed for the stage-D pause):** {i['disp']}"] + \
           ([f"- **Bug:** {i['bug']}"] if i.get("bug") else []) + [""]
resolved = all(i.get("res") for i in items)
gate_lead = ("Stage E's hand-back, 2026-10-30: every item at its outcome, the table and the index rewritten together from `stage-c/punch-items.py`'s `RES`. "
             "The ES commits are on `feature/m6-es-app-system-680` (pixelelated/emulationstation), fixed-at-es `f802c55c6`; each stream's before, after and checks are under `stage-e/`, "
             "the tip's are `stage-e/handback-checks.txt`, and `02` § The streams carries one row per stream.") if resolved else \
            "Stage F rewrites this table and the index together. Until then every item is `Open`."
out += ["## Phase 7 resolution gate", "", gate_lead, "",
        "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
out += [f"| {i['id']} | {i['res'][0]} | {i['res'][1]} |" if i.get("res") else f"| {i['id']} | Open | -- |" for i in items]
out += ["", "```yaml", "punch_index:"]
for i in items:
    out += [f"- id: {i['id']}", f"  severity: \"{i['sev']}\"", f"  category: {i['cat']}", f"  question: {i['q']}",
            "  source_finding: \"%s\"" % i["src"].split(" -- ")[0].replace('"', "'"), "  outcome: \"%s\"" % (i["res"][0].lower() if i.get("res") else "open")]
out += ["```", ""]
open(os.path.join(A, "05-punch-list.md"), "w").write("\n".join(out))
words = [i["res"][0] if i.get("res") else "Open" for i in items]
print("t33-05: %d items rendered (%s); the gate and the index: %s" % (len(items), ", ".join("%s %s" % (i["id"], i["sev"]) for i in items),
      ", ".join("%d %s" % (words.count(w), w) for w in ("Resolved", "Deferred", "Withdrawn", "Open") if words.count(w))))

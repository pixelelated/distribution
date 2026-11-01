"""audit-issue-body.py: the T38 audit issue's title and body (#685, stage D), written from 05-punch-list.md so the
issue carries one checkbox per item and the counts are computed. python3 -I audit-issue-body.py <05> <title-out> <body-out>"""
import re, sys
s = open(sys.argv[1]).read()
items = re.findall(r"^## (PL-\d+): (.*)\n\n- \*\*Severity:\*\* (\S+)\n- \*\*Category:\*\* .*\n- \*\*Question:\*\* (Q\d)\n- \*\*Source finding:\*\* (.*)\n(?:- .*\n)*?- \*\*Proposed:\*\* (.*)\n", s, re.M)
n = len(re.findall(r"^## PL-\d+:", s, re.M))
if not items or len(items) != n:
    sys.exit(f"audit-issue-body: refused: parsed {len(items)} of {n} items")
sev = {k: sum(1 for i in items if i[2] == k) for k in ("Critical", "High", "Medium", "Low")}
bugs = [(i[0], i[5].split("#")[1]) for i in items if i[5].startswith("bug #")]
qs = [i[0] for i in items if i[5].startswith("question")]
inh = [i[0] for i in items if i[5].startswith("inherit")]
U = "https://github.com/pixelelated/distribution/blob/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills"
T = "https://github.com/pixelelated/distribution/tree/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills"
title = f"Audit: M6 T38 the skills, agents and settings -- {n} findings ({sev['Critical']} critical, {sev['High']} high)"
out = [f"The T38 audit of the skills, agents and settings (#685, area epic #807, renovation #339). It covers the 52 paths of `.claude/**` less `.claude/rules/**`: the ten skills and the eight agent definitions, 12,783 lines at the dispatch tip `87c2ab0fed` (`reviewed-at`). Nothing was built, run against a provider, or edited under `.claude/` before this issue.",
"",
"**Depth: Local** (plan § 6c, *a doctrine read*; D-WORKFLOW-184's tier exception in `second-opinions/review-plan.json`). There is no reviewer seat and no keyed call, and Phase 4.6 is recorded as not applicable at Local depth. The checks are the artifact lint and the slice's own checker, `tools/t38-checks.sh` under the folder, seen to fail first on a planted positive per probe.",
"",
f"**{n} items:** {sev['Critical']} Critical, {sev['High']} High, {sev['Medium']} Medium, {sev['Low']} Low.",
f"- **`bug` issues:** the {len(bugs)} sentences a reader acts on wrongly each have one: " + ", ".join(f"{k} #{v}" for k, v in bugs) + ".",
f"- **Questions put to the coordinator at the stage-D pause:** {', '.join(qs)}.",
f"- **Inherited:** {', '.join(inh)}: the export's refresh (#911), the coordinator's rule errata and Backlog leads, and `tools/skills-check`'s inputs (#1373).",
f"- **The rest** are punch items for the fork-adapted skills (begin-delivery, code-auditor, futro, mini-retro, session-resume, session-stash, developer-relations, release-notes). They are fixed only at stage E, under the coordinator's stream brief `docs/reviews/briefs/t38-streams.md`, and never in the council family.",
"",
f"**Folder:** [`docs/audits/2026_11_01-epic-m6-doctrine-skills/`]({T}). The punch list is [`05-punch-list.md`]({U}/05-punch-list.md), with each item's where, acceptance and ladder, and the analysis is [`04-analysis.md`]({U}/04-analysis.md).",
"",
"**Stage:** D, the pause. Every item is Open until the stream brief; each checkbox is ticked at Phase 7 from its artifact.",
"",
"## Items",
""]
for pl, ttl, sv, q, src, prop in items:
    ref = f", #{prop.split('#')[1]}" if prop.startswith("bug #") else ""
    out.append(f"- [ ] **{pl}** ({sv}, {q}, {src}{ref}): the acceptance check in `05-punch-list.md` § {pl} passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.")
open(sys.argv[2], "w").write(title + "\n")
open(sys.argv[3], "w").write("\n".join(out) + "\n")
print(title); print(f"checkboxes {len(items)}; bugs {len(bugs)}; questions {len(qs)}; inherited {len(inh)}")

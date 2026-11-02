"""t39-punch.py: writes 05-punch-list.md for T39 (#686) from the leads of 02 § The table, one item per lead
(PL-NN is L-NN), every item open until the stage-D pause's stream brief and Phase 7. Run from the worktree:
    python3 -I docs/audits/2026_11_01-epic-m6-doctrine-reference/tools/t39-punch.py > .../05-punch-list.md
It asserts 46 items and the severity counts it prints, so a dropped lead fails here."""
import sys

DOCS = "t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)"
# lead: (title, severity, category, question, where, disposition, ladder-next, already-written)
L = {
 1: ("the renovation's README and plan name P1's files and tools", "Low", "Renovation", "Q6", "`docs/reviews/README.md:10-12`, `plan-for-the-plan.md`", "ledger: resolved at dispatch (ruling (p)); the 15-name loop prints no MISSING", "no tool can (a merge order)", "nothing: resolved before any reader acted"),
 2: ("the front page sends a player to instructions attached to a release that does not exist", "Medium", "Bug", "Q3", "`README.md:9`", "fix (ruling (c)); bug", f"{DOCS}'s `leads` step", "every session that opens the front page; #344 is open"),
 3: ("the device-testing policy calls D-QA-016 open", "Medium", "Bug", "Q3", "`docs/device-testing-policy.md:5`", "fix (ruling (l)); bug; `vm-first.md`'s sentence inherit:coordinator", f"{DOCS} with a decided-row-called-open check", "the five rule files that send testers to the policy"),
 4: ("the retired cloud-folder migration script described as current", "Medium", "Bug", "Q3", "`docs/rasteratops/cloud-layout.md:16`, `docs/releases/pr/08-saves.md:5`", "fix (ruling (l)); bug", f"{DOCS}'s `retired` step (it fails at the tip today)", "the 08-saves PR description; the cloud-layout record"),
 5: ("the flashing runbook names the OS ROCKNIX throughout", "Medium", "Bug", "Q3", "`docs/device-flashing-runbook.md` (21 lines)", "fix where NAMING.md decides the word; the rest classed", f"{DOCS}'s `identity` step with a ROCKNIX-as-the-OS class", "`CLAUDE.md`, `AGENTS.md` and `device-builds.md:616` send every fresh-card flasher here"),
 6: ("an M7 order of closed issues", "Low", "Code Quality", "Q4", "`docs/cloud-save-integrity.md:4`", "fix", f"{DOCS} with an issue-state check (Q4 (c))", "nothing traced"),
 7: ("labels the pin does not ship, in banned words, in the public docs' stated source", "Medium", "Bug", "Q3", "`docs/backup-contents.md:3-4`", "fix (labels re-derived from the pin); bug", "a label check against the ES pin (`es-menu-map-check`'s reach widened)", "the rocknix.org backup page drafts that copy it"),
 8: ("the map's journal calls closed #570 work pending", "Low", "Code Quality", "Q4", "`docs/es-menu-map.md:758`, `:806`, `:817`", "fix: the headings only (ruling (b)); the journal's home is § 4 question 1", f"{DOCS} with an issue-state check", "agents placing a row read it"),
 9: ("a superseded baseline build named as the baseline", "Low", "Code Quality", "Q4", "`docs/releases/next-candidate-work.md:4`", "fix", "no tool can (a baseline is a judgement)", "nothing traced"),
 10: ("the player's cloud-folder guide ends in internal release status", "Low", "Code Quality", "Q7", "`docs/pixelelated/cloud-folders.md:32-35`", "fix", "no tool can", "`README.md:22` sends players here"),
 11: ("words and numbers run together", "Low", "Code Quality", "Q7", "ten files (`02` § The table)", "fix in the edit scope; `docs/upstream/README.md`'s share inherit:#585; `rc-accept.txt`'s ledger", "no tool can (a heuristic, not a check)", "nothing traced"),
 12: ("a counter note for a seat outside every run profile, no banner", "Low", "Renovation", "Q5", "`docs/council-mistral-counter.md:3`", "fix: a banner; `council-limits.md` is § 4 question 2", f"{DOCS}'s `leads` step", "nothing traced"),
 13: ("rocknix.org drafts naming pages without their repository", "Low", "Code Quality", "Q6", "four files (`02` § The table)", "fix: the repository named beside each page", f"{DOCS}'s `paths` step (`external` class)", "nothing traced"),
 14: ("the splash repository's wordmark tool, named with its repository", "Low", "Renovation", "Q6", "`docs/pixelelated/art/README.md:20-21`", "withdrawn as a defect: a Coverage `none` (X02)", "held by the `paths`/`tools` steps' `external` class", "--"),
 15: ("the device facts point to a catalog with none of their cuts", "Low", "Code Quality", "Q4", "`docs/releases/device-facts.md:7`", "fix the pointer without moving a cited row; inherit:#270 (the tool); inherit:coordinator (the catalog's regeneration, #964)", "#270's device-facts check", "#1100, #1126 and #1094 cite its rows"),
 16: ("the read mask's long form lacks the flag form", "Medium", "Bug", "Q3", "`docs/device-testing-policy.md:94`", "fix; bug", f"{DOCS}'s `leads` step", "readers who copy the policy's mask"),
 17: ("the wizard's IA against its decided rows", "Low", "Code Quality", "Q4", "`docs/conflict-wizard-ia.md`", "fix where a sentence contradicts a decided row and no screen change owns it; else inherit:the interface lanes ([unverified]: the reading is owed)", "no tool can", "#23 still says rev 5"),
 18: ("low-inbound reference documents presenting themselves as current", "Low", "Renovation", "Q5", "the Q5 table's LOW-INBOUND set", "fix: a dated first line where a record presents itself as current; retirement is § 4 question 2", "the Q5 generator's inbound columns, promoted with the checker", "search results that look current"),
 19: ("the splash repository's tool in a historical artifact's README", "Low", "Renovation", "Q6", "`docs/rasteratops/art/README.md:8`", "ledger (a historical artifact; X02)", "held by the `external` class", "--"),
 20: ("`packages/rocknix` in dated P0 records", "Low", "Renovation", "Q6", "`docs/rasteratops/p0-read.md:11`, `p0-sweep.md:39`", "ledger (a dated record)", "held by the `paths` step's `historical` class", "--"),
 21: ("Rasteratops as the OS's identity in dated records", "Low", "Renovation", "Q2", "`docs/rasteratops/raofflineproxy-refresh.md:180,188`, `cloud-folder-state-table.md:38`", "ledger (records of their date)", "held by the `identity` step's `historical` class", "--"),
 22: ("a current plan says the site remotes still name the retired owner", "Low", "Code Quality", "Q4", "`docs/pixelelated/site-plan.md:72`", "fix where it misstates the present; else inherit:#511", f"{DOCS}'s `identity` step", "nothing traced"),
 23: ("`maxengel/rocknix` links resolving only by redirect", "Low", "Renovation", "Q2", "`docs/cloud-sync-changelog.md:706-735`", "ledger (dated changelog entries)", "held by the `identity` step", "--"),
 24: ("the one plan, superseded and unmarked", "Low", "Renovation", "Q1", "`plans/conflict-resolution/vita-style-conflict-resolution.md:8-9`", "ledger: one historical-plan row naming the superseding row (ruling (d))", "no tool can", "--"),
 25: ("0.0.1 called the first Rasteratops release in the RC ledger", "Low", "Renovation", "Q2", "`docs/releases/rc-accept.txt:13`", "inherit:coordinator (ruling (l))", "held by the `identity` step's allow-inherited entry", "--"),
 26: ("two stale acceptances kept as the record", "Low", "Renovation", "Q4", "`docs/releases/rc-accept.txt`", "ledger", "`tools/rc-preflight`", "--"),
 27: ("the upstream-series map names two deleted paths", "Low", "Renovation", "Q6", "`docs/pr-series/map.txt:112`, `:174`", "inherit:coordinator (ruling (e))", "`tools/pr-stack-check` failing on an absent path", "--"),
 28: ("the plan says it exists on next; next has no docs/reviews/", "Low", "Renovation", "Q4", "`docs/reviews/plan-for-the-plan.md`", "inherit:coordinator (ruling (a))", "no tool can", "--"),
 29: ("a preliminary slice number in the order", "Low", "Renovation", "Q7", "`docs/reviews/order.md:792`", "inherit:coordinator", "no tool can", "--"),
 30: ("current release records under the retired name's folder", "Low", "Renovation", "Q2", "`docs/rasteratops/release-readiness.md`, `support-matrix.md`", "inherit:#509 (a reviewed rename batch)", "#509's batch", "--"),
 31: ("the fork's GENERIC_X64 emulator table has drifted and has no generator", "Low", "Renovation", "Q6", "`documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`", "inherit:coordinator: a Backlog candidate, generate or drop (ruling (j))", "a generator from the image's systems list", "--"),
 32: ("the most-cited map, cited by line by open issues", "Low", "Renovation", "Q4", "`docs/es-menu-map.md:134`, `:405`, `:595`", "inherit:the interface lanes (ruling (b)); #1216's quoted label differs at `:405`", "no tool can", "--"),
 33: ("two open issues cite a document the tree lacks", "Low", "Renovation", "Q6", "#576 `:7`, #620 `:16`", "inherit:coordinator", "no tool can", "--"),
 34: ("register rows describe a series D-WORKFLOW-084 ended", "Low", "Renovation", "Q4", "`docs/decision-register.md` rows; `documentation-accuracy.md:48-52`", "inherit:coordinator (rows and a rule)", "no tool can", "--"),
 35: ("a docs/** glob loads a device rule for any record", "Low", "Renovation", "Q5", "`.claude/rules/handheld-evidence.md`", "inherit:coordinator (T4's file)", "`tools/rules-check` reporting glob reach", "--"),
 36: ("two documents or three that load nowhere", "Low", "Renovation", "Q7", "`CLAUDE.md:34`, `AGENTS.md:31`, `instruction-files.md:122`", "inherit:coordinator", "`tools/rules-check`'s twin-fact check", "--"),
 37: ("an area sentence untrue of this slice", "Low", "Renovation", "Q4", "#807 `:15`", "inherit:coordinator: the erratum is present (06:43 UTC)", "no tool can", "--"),
 38: ("citations no tool checks", "Low", "Renovation", "Q4", "the reference files outside `register-check`'s LIVE", "inherit:#947", "`register-check`'s LIVE widened (#947)", "--"),
 39: ("an open criterion on the versioning document", "Low", "Renovation", "Q4", "`docs/releases/versioning.md`", "inherit:#1013", "#1013's criterion", "--"),
 40: ("a path word the machine retired", "Low", "Renovation", "Q2", "`worktrees.md`, `CLAUDE.md`", "inherit:coordinator (T4's rules)", "no tool can until the coordinator rules", "--"),
 41: ("upstream's generated tables, behind upstream", "Low", "Renovation", "Q4", "13 of the 15 upstream-carried `documentation/` tables", "inherit:the next upstream base merge", "the upstream base merge", "--"),
 42: ("an open checkbox against the licence file", "Low", "Renovation", "Q4", "#335 `:19`", "inherit:coordinator (a tracker edit)", "no tool can", "--"),
 43: ("the licence statements disagree", "Low", "Renovation", "Q2", "`TRADEMARK.md:5-6`; `LICENSE.md:3,13,18`", "inherit:#528 (a legal reading)", "no tool can", "--"),
 44: ("a licence upstream dropped for a licensing concern", "Low", "Renovation", "Q1", "`licenses/AETHERSX2.pdf`", "inherit:#528", "no tool can", "--"),
 45: ("a qualified candidate's recorded licence bytes", "Low", "Renovation", "Q4", "#359 `:9`, `:13`, `:14`", "inherit:#528; the tree's hashes equal #359's", "`tools/rasteratops-identity-check`", "--"),
 46: ("the contribution queue's drafts, read-only", "Low", "Renovation", "Q4", "`docs/upstream/**`", "inherit:#585 (lines owed, never sent)", "no tool can", "--"),
}
assert len(L) == 46
sev = {"Medium": [k for k, v in L.items() if v[1] == "Medium"], "Low": [k for k, v in L.items() if v[1] == "Low"]}
o = []
o.append("# Punch list -- M6.P2 T39, the reference documents (#686)\n")
o.append(f"**Local depth** (plan § 6c, D-WORKFLOW-184): no reviewer; Phase 4.5 is in `04`. **46 items, one per lead** (PL-NN is L-NN, brief § 3):")
o.append(f"- **{len(sev['Medium'])} Medium**, each a `bug` filed at stage D: " + ", ".join(f"PL-{k:02d}" for k in sev["Medium"]) + ".")
o.append(f"- **{len(sev['Low'])} Low**: the remaining fix candidates, and the ledger, inherited, #528 and #585 items, each with its owner.\n")
o.append("Each item gives the rung of `working-principles.md`'s ladder its statement sits at (*written*: the sentence exists) and the tool that would hold it at the next rung, or *no tool can*. **Nothing in the 254 is changed here.** Every edit waits for the stage-D pause's stream brief (`docs/reviews/briefs/t39-streams.md`, the coordinator's). The audit issue (a sub-issue of #686) and the bugs are filed at stage D; until then each item's `Tracked:` reads *stage D*. Drafted at stage C so the pre-issue lint reads the shape.\n")
o.append("---\n")
for k, (t, s, c, q, w, d, lad, aw) in L.items():
    o.append(f"## PL-{k:02d}: {t}")
    o.append(f"- **Severity:** {s}")
    o.append(f"- **Category:** {c}")
    o.append(f"- **Question:** {q}")
    o.append(f"- **Source Finding:** L-{k:02d} (`02` § The table)")
    o.append(f"- **Where:** {w}, at the dispatch tip `86ebb6dffc`")
    o.append(f"- **Disposition:** {d}")
    o.append(f"- **Ladder:** written; next rung: {lad}")
    o.append("- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)")
    o.append(f"- **Already written:** {aw}")
    o.append(f"- **Acceptance:** L-{k:02d}'s check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it")
    o.append("- **Tracked:** stage D\n")
o.append("## Machine-readable index\n")
o.append("```yaml")
o.append("punch_index:")
for k, (t, s, c, q, w, d, lad, aw) in L.items():
    o.append(f"- id: PL-{k:02d}")
    o.append(f"  severity: {s}")
    o.append(f"  category: {c}")
    o.append(f"  question: {q}")
    o.append(f"  source_finding: \"L-{k:02d}\"")
    o.append(f"  disposition: \"{d.split(';')[0].split(' (')[0]}\"")
    o.append("  tracked: \"stage D\"")
    o.append("  outcome: \"open\"")
o.append("```\n")
o.append("## Phase 7 resolution gate\n")
o.append("Every item is **Open** at the pre-issue lint; the outcomes are written at stage F from the streams' commits and the owners' issues.\n")
o.append("| Item | Outcome | Evidence |")
o.append("| --- | --- | --- |")
for k in L:
    o.append(f"| PL-{k:02d} | Open | stage D/E |")
print("\n".join(o))
print(f"PUNCH items {len(L)} Medium {len(sev['Medium'])} Low {len(sev['Low'])}", file=sys.stderr)

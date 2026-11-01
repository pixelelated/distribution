"""t38-punch.py: writes 05-punch-list.md (T38, #685) from one list, so the items, the Phase 7 table and the
punch_index cannot disagree. Every item is Open until the stage-D pause's stream brief decides it; the lint's
pre-issue phase accepts an explicit Open row with its index entry (#470).
    python3 -I t38-punch.py [<02-forward-audit.md>] > ../05-punch-list.md   (refuses an unaccounted lead)"""

# (title, severity, category, question, leads, owner, where, acceptance, ladder, proposed)
ITEMS = [
 ("Phase 4.6 fails a Local epic-tier slice closed in four sentences and a table row", "Medium", "Spec Drift", "Q3", "L-56", "code-auditor",
  "`code-auditor/SKILL.md:247`, `:508`; `references/phases.md:439`, `:486-491`; `references/review-levels.md:9`; `references/templates.md:94`, `:164`",
  "each names D-WORKFLOW-184's Local epic-tier exception as `templates.md:144-146` does; `grep -c 'D-WORKFLOW-184'` over the four files prints a count in each",
  "written -> audited by `tools/skills-check`'s contract step (#1373)", "bug (stage D)"),
 ("scoped-audit's pre-existing check pops the shared stash and fetches vitest", "Medium", "Code Quality", "Q3", "L-10", "mini-retro",
  "`mini-retro/references/scoped-audit.md:347-359`, `:292-321`",
  "the block uses a detached scratch worktree at `<base_sha>` and the repository's own checks; `sed -n '340,365p' | grep -c -E 'git stash( |$)|npx vitest'` prints `0`",
  "written -> audited by `tools/skills-check`'s stale step (a bare `git stash` and `npx` as terms)", "bug (stage D)"),
 ("release-notes says fork-publish-release uploads the files", "Medium", "Documentation Gap", "Q3", "L-11", "release-notes",
  "`release-notes/SKILL.md:19-21`",
  "the sentence says the tool prepares a plan (`--prepare`) and that publication waits on #265, #344 and #528; `sed -n '19,20p' | grep -c uploads` prints `0`",
  "written -> no tool can (a sentence about another tool's behaviour)", "bug (stage D)"),
 ("code-auditor runs the lint with --issue before the issue exists, and never names --phase pre-issue", "Low", "Documentation Gap", "Q3", "L-52", "code-auditor",
  "`code-auditor/SKILL.md:252-256`",
  "the paragraph runs `--phase pre-issue` before Phase 6 and the default phase with `--issue <n>` after Phase 7; `git grep -c 'pre-issue'` over the skill prints a count",
  "written -> audited by `tools/skills-check`'s contract step", "bug (stage D)"),
 ("futro's comment read uses gh api {owner}/{repo}", "Low", "Code Quality", "Q3", "L-13", "futro",
  "`futro/SKILL.md:479`",
  "the command names `repos/pixelelated/distribution`; `grep -c -F '{owner}/{repo}'` prints `0`",
  "written -> audited by `tools/skills-check`'s stale step", "bug (stage D)"),
 ("the evidence floor says three rules and numbers five 1, 2, 3, 4, 3", "Medium", "Documentation Gap", "Q7", "L-02", "code-auditor",
  "`code-auditor/SKILL.md:159`, `:161`-`:191`, `:370`; `references/phases.md:60`",
  "five rules numbered 1 to 5, the count said, both citations of the subagent rule moved; `sed -n '157,200p' | grep -c -E '^3\\. \\*\\*'` prints `1`",
  "written -> audited by `tools/skills-check` (a numbered list's count against its sentence)", "punch"),
 ("templates.md's scorecard heading fails the lint", "Medium", "Spec Drift", "Q3", "L-60", "code-auditor",
  "`code-auditor/references/templates.md:23`",
  "`## Acceptance-criteria scorecard`; `tools/t38-checks.sh`'s contract step passes without its allow-findings entry",
  "evidenced -> audited by `tools/t38-checks.sh`'s contract step, then #1373's", "punch"),
 ("the scoped audit's checks are counted ten, nine, six, nine and five", "Medium", "Documentation Gap", "Q4", "L-63", "mini-retro, begin-delivery",
  "`mini-retro/SKILL.md:199-252`, `:353-358`; `mini-retro/references/template.md:71-79`; `begin-delivery/SKILL.md:168-171`",
  "one count; the format and the template list the ten checks; `tools/t38-tables.py q4` (c) prints `yes` for each row",
  "written -> audited by `tools/t38-tables.py q4`'s counts, then #1373's", "punch"),
 ("phases.md says Epic tier trusts the retros while SKILL.md says re-derive two", "Medium", "Spec Drift", "Q7", "L-57", "code-auditor",
  "`code-auditor/references/phases.md:71-72` against `SKILL.md:110`",
  "`phases.md` states the re-derivation quota as `SKILL.md` does", "written -> no tool can (two texts' meanings)", "punch"),
 ("phases.md says the repo has no artifact lint, so verify by hand", "Medium", "Documentation Gap", "Q1", "L-59", "code-auditor",
  "`code-auditor/references/phases.md:574-577`; `references/anti-patterns.md:26`",
  "Phase 5's final step runs `tools/lint-audit-artifacts --phase pre-issue`; `grep -c 'none today'` prints `0`",
  "written -> audited by `tools/skills-check`'s stale step", "punch"),
 ("Phase 0's stale-copy check reads SKILL.md alone", "Medium", "Test Gap", "Q3", "L-53", "code-auditor",
  "`code-auditor/SKILL.md:278-281`",
  "the check compares the whole skill directory, and says a renovation lane reads the dispatch tip's skill; the block at this tip prints the `templates.md` difference",
  "written -> no tool can until #1373 checks the block", "punch"),
 ("futro MUSTs a git fetch origin main this repository cannot run", "Medium", "Documentation Gap", "Q3", "L-66", "futro",
  "`futro/SKILL.md:207-230`",
  "the base-divergence check compares against `next` with no fetch; `grep -c 'origin/main'` prints `0`",
  "written -> audited by `tools/skills-check`'s stale step (`origin/main`)", "punch"),
 ("session-stash's exact template has no Start here", "Medium", "Documentation Gap", "Q2", "L-69", "session-stash",
  "`session-stash/SKILL.md:64-117` against `:32`",
  "the template opens with `## Start here`; `grep -c '^## Start here'` over the skill prints `1`",
  "written -> audited by `tools/skills-check` (the template's headings against learning-capture.md § 4)", "punch"),
 ("release-notes' description promises PR bodies a details block the body forbids", "Medium", "Documentation Gap", "Q5", "L-70", "release-notes",
  "`release-notes/SKILL.md:3` against `:97-102`",
  "the description says the details block is the release note's only; its length recorded before and after",
  "written -> no tool can (the description's meaning)", "punch"),
 ("mini-retro's order of Step 2.5 and its two closing lists", "Medium", "Documentation Gap", "Q7", "L-81", "mini-retro",
  "`mini-retro/SKILL.md:187-189`, `:152`, `:351`, `:461-462`; `references/scoped-audit.md:3-6`; `references/template.md:137-152`",
  "one order for Step 2.5, one closing list, no self-referring Step 7", "written -> no tool can", "punch"),
 ("code-auditor names no completion marker and no held-reply sidecar", "Medium", "Missing Artifact", "Q2", "L-06, L-07", "code-auditor",
  "`code-auditor/SKILL.md:555-617`; `references/templates.md` (second-opinions layout)",
  "Phase 7 names `docs/audits/<scope>/audit-completion.json` (#540) and the layout names `<reply>.held.json` (#1308); the stage-A check prints a line each",
  "written -> audited by `tools/ceremony-check`'s completed-audit marker", "punch"),
 ("futro and mini-retro write their artifacts to homes the ceremonies do not read", "Medium", "Missing Artifact", "Q2", "L-08, L-20", "futro, mini-retro",
  "`futro/SKILL.md:379-388`; `futro/references/template.md:3-4`; `mini-retro/SKILL.md:310-320`; `mini-retro/references/template.md:3-4`; `session-stash/SKILL.md:60`",
  "each artifact step names `docs/futros/<date>-<scope>.md` or `docs/retros/<date>-<scope>.md` (or the work-log heading) and `tools/ceremony-check`",
  "written -> audited by `tools/ceremony-check`", "punch"),
 ("code-auditor's Twelve recorded failure modes", "Low", "Documentation Gap", "Q4", "L-03", "code-auditor", "`code-auditor/SKILL.md:420`",
  "no number, or one a command prints; `grep -c 'Twelve recorded'` prints `0`", "written -> audited by `tools/t38-tables.py q4`'s counts", "punch"),
 ("code-auditor's legacy worktree layout", "Low", "Documentation Gap", "Q1", "L-04", "code-auditor", "`code-auditor/SKILL.md:711`",
  "the layout the lanes use, #640 named; `grep -c 'rocknix\\.worktrees'` prints `0`", "written -> audited by `tools/skills-check`'s stale step", "punch"),
 ("durations used as estimates", "Low", "Improvement", "Q2", "L-05", "code-auditor, mini-retro, begin-delivery, futro",
  "the widened pattern's 10 lines (stage A) and `code-auditor/SKILL.md:612`, `begin-delivery/SKILL.md:256`, `mini-retro/SKILL.md:189`, `scoped-audit.md:8-9`, `futro/SKILL.md:377`, `futro/references/blindspot-register.md:74-78`",
  "every estimate gone or an ordering (D-WORKFLOW-091); the widened pattern prints `0`; `code-auditor/SKILL.md:3`'s length before and after",
  "written -> audited by `tools/skills-check`'s stale step (#342)", "punch"),
 ("a main branch this repository has not", "Low", "Documentation Gap", "Q1", "L-09", "session-stash, session-resume",
  "`session-stash/SKILL.md:7`, `:34-41`; `session-resume/SKILL.md:7`, `:30`",
  "the main rules gone; `git grep -c 'saved-session-state-main'` prints `0`", "written -> audited by `tools/t38-checks.sh`'s stale step (`state-main`)", "punch"),
 ("Copilot-era rule-file names and a missing agent-terminal-safety rule", "Low", "Documentation Gap", "Q1", "L-12, L-73", "code-auditor, mini-retro, begin-delivery",
  "`code-auditor/SKILL.md:366`, `:425`, `:432`; `scoped-audit.md:209`; `begin-delivery/SKILL.md:466`",
  "each points at its `.claude/rules/` successor or is dropped", "written -> audited by `tools/skills-check`'s refs step", "punch"),
 ("Copilot's mcp_github_* names and the advice to avoid gh", "Low", "Documentation Gap", "Q1", "L-14, L-21", "all six imported skills",
  "`futro/SKILL.md:79-81`, `:112`; `mini-retro/SKILL.md:116-118`; `begin-delivery/SKILL.md:136-141`, `:154`, `:284`, `:384`, `:440`; `code-auditor/SKILL.md:365`; `phases.md:31`, `:587`; `anti-patterns.md:20`; `session-resume/SKILL.md:49`; `session-stash/SKILL.md:57`; `futro/references/techniques.md:28`, `:35`; `futro/references/template.md:72`",
  "one shared sentence with `mcp__github__*` and `gh --repo pixelelated/distribution`; the stale step's `copilot` count over the fork-adapted skills prints `0`",
  "written -> audited by `tools/t38-checks.sh`'s stale step", "punch"),
 ("the source estate's checks, stacks and examples kept as this repository's", "Low", "Documentation Gap", "Q1", "L-15", "all six imported skills",
  "`02` § The leads, L-15's row (mini-retro, scoped-audit, code-auditor, futro, begin-delivery, session-resume, session-stash)",
  "each replaced with this repository's checks and examples or dropped, one stream per skill", "written -> audited by `tools/skills-check`'s stale step (the estate's terms)", "punch"),
 ("another estate's issue numbers cited as this tracker's", "Low", "Documentation Gap", "Q6", "L-58", "code-auditor, mini-retro, futro, begin-delivery",
  "`02` § The leads, L-58's row; `futro/SKILL.md:163-164` (`audit #203`)",
  "each citation names its estate or is dropped; `#203` no longer cited as an audit", "written -> audited by `tools/skills-check` (a `#N` above the tracker's highest)", "punch"),
 ("version histories inside procedures", "Low", "Improvement", "Q5", "L-16", "begin-delivery, code-auditor",
  "`begin-delivery/SKILL.md:541-609`; `code-auditor/SKILL.md:8-9`",
  "the histories in the commit log; the front matter's note shortened, its length recorded", "written -> no tool can", "punch"),
 ("futro's blindspot register 'when created'", "Low", "Documentation Gap", "Q1", "L-17", "futro",
  "`futro/SKILL.md:426-435`, `:480`", "the sentence names `docs/blindspot-register.md`; the starter stays a starter", "written -> no tool can", "punch"),
 ("session-stash's stranger's proof is stated in no step", "Low", "Documentation Gap", "Q2", "L-19", "session-stash",
  "`session-stash/SKILL.md:32`", "Step 3 carries the proof as a step", "written -> no tool can", "punch"),
 ("templates.md's Local example writes anthropic/claude-opus-5.5", "Low", "Documentation Gap", "Q3", "L-51", "code-auditor",
  "`code-auditor/references/templates.md:136`", "`anthropic/claude-opus-5-5`; `grep -c -F 'anthropic/claude-opus-5.5'` prints `0`",
  "written -> audited by `tools/skills-check`'s stale step", "punch"),
 ("subagents do not inherit terminal access", "Low", "Documentation Gap", "Q1", "L-54", "code-auditor",
  "`code-auditor/SKILL.md:369`, `:682`; `phases.md:61`, `:593`; `anti-patterns.md:18`", "the sentence says what the harness does", "written -> no tool can", "punch"),
 ("Phase Z.6, PZ, Outcome A/B and P7, defined nowhere", "Low", "Documentation Gap", "Q6", "L-55", "code-auditor, mini-retro",
  "`code-auditor/SKILL.md:659-661`; `mini-retro/SKILL.md:269`; `scoped-audit.md:39`, `:703`, `:519-520`, `:576-577`; `mini-retro/references/template.md:105`",
  "each defined or replaced with this repository's words", "written -> audited by `tools/skills-check` (an undefined token list)", "punch"),
 ("templates.md's escaped fences", "Low", "Code Quality", "Q7", "L-61", "code-auditor", "`code-auditor/references/templates.md:236`, `:247`",
  "a nested fence that copies as one", "written -> no tool can", "punch"),
 ("the criterion entry 'reproduced' in templates.md has drifted", "Low", "Documentation Gap", "Q7", "L-62", "code-auditor",
  "`code-auditor/references/templates.md:268-295` against `phases.md:146-172`", "one copy, or `tools/t38-tables.py q7` prints no difference", "evidenced -> audited by `tools/t38-tables.py q7`", "punch"),
 ("the full 6-phase methodology", "Low", "Documentation Gap", "Q4", "L-64", "mini-retro, code-auditor",
  "`mini-retro/SKILL.md:547-548`; `code-auditor/SKILL.md:84-85`", "the phases named, not counted", "written -> audited by `tools/t38-tables.py q4`'s counts", "punch"),
 ("scoped-audit's reference/template.md and cornerstone-conformance.md", "Low", "Documentation Gap", "Q6", "L-65", "mini-retro",
  "`mini-retro/references/scoped-audit.md:71`, `:176`", "each path resolves or is dropped; `tools/t38-checks.sh`'s refs step without the entry", "evidenced -> audited by `tools/t38-checks.sh`'s refs step", "punch"),
 ("futro's four techniques, five listed, three in the template", "Low", "Documentation Gap", "Q4", "L-67", "futro",
  "`futro/SKILL.md:288`; `futro/references/techniques.md:3-5`, `:264`; `futro/references/template.md:68`", "one list and its count", "written -> audited by `tools/t38-tables.py q4`'s counts", "punch"),
 ("review-levels.md's status line for #375", "Low", "Documentation Gap", "Q4", "L-71", "code-auditor",
  "`code-auditor/references/review-levels.md:41-44`", "the status line gone (#375 is closed)", "written -> no tool can", "punch"),
 ("code-auditor's list of the checks that exist here", "Low", "Documentation Gap", "Q4", "L-72", "code-auditor",
  "`code-auditor/SKILL.md:171-177`", "the list points at `instruction-files.md`'s tool table", "written -> no tool can", "punch"),
 ("the audit issue's checkbox shape (D-QA-044, #268)", "Low", "Improvement", "Q2", "L-74", "code-auditor",
  "`code-auditor/SKILL.md:541-552`", "Phase 6 gives `- [ ] <behaviour> -- <artifact>` and `tools/box-check --issue N`", "written -> audited by `tools/box-check`", "punch"),
 ("register sections futro and begin-delivery cite and no register has", "Low", "Documentation Gap", "Q6", "L-75", "futro, begin-delivery",
  "`futro/SKILL.md:141-143`, `:258-259`; `begin-delivery/SKILL.md:491-492`", "each cites an entry `docs/blindspot-register.md` holds, or drops the citation", "written -> audited by `tools/skills-check` (a register section named)", "punch"),
 ("developer-relations' dash, split list and walk counts", "Low", "Documentation Gap", "Q7", "L-79", "developer-relations",
  "`developer-relations/SKILL.md:103-104`, `:116-135`, `:178`, `:181-183`", "each read once by a no-context reader without the stumble", "written -> no tool can", "punch"),
 ("release-notes' claims about its tools, and RC1", "Low", "Documentation Gap", "Q4", "L-80", "release-notes",
  "`release-notes/SKILL.md:66`, `:68`, `:119-121`, `:125`", "each claim the tool's own (`prose-check`'s strict paths; `pr-stack-check`'s `BANNED`)", "written -> no tool can", "punch"),
 ("futro's thresholds, the committed comment and the heading levels", "Low", "Documentation Gap", "Q7", "L-82", "futro",
  "`futro/SKILL.md:339-341`, `:401-413`, `:462-464`; `futro/references/template.md:10`, `:20`", "one threshold; the commit step said; the template's `## 1.` as the futros use", "written -> no tool can", "punch"),
 ("begin-delivery's own history and step order", "Low", "Documentation Gap", "Q7", "L-83", "begin-delivery",
  "`begin-delivery/SKILL.md:207`, `:212-215`, `:392`, `:401`, `:469`", "one order, the history consistent", "written -> no tool can", "punch"),
 ("the session skills' stat, staleness tiers and approval", "Low", "Documentation Gap", "Q7", "L-84", "session-resume, session-stash",
  "`session-resume/SKILL.md:40`, `:42`, `:45`, `:112`; `session-stash/SKILL.md:30`, `:38`", "each sentence a reader can act on", "written -> no tool can", "punch"),
 ("code-auditor's tiers, mode trigger and phase counts", "Low", "Documentation Gap", "Q7", "L-85", "code-auditor",
  "`code-auditor/SKILL.md:77`, `:92`, `:612`, `:623`, `:665`; `phases.md:3`, `:353`, `:412`", "each said once", "written -> no tool can", "punch"),
 ("begin-exploration: write the skill or sweep the references", "Medium", "Improvement", "Q6", "L-22", "the maintainer, the coordinator",
  "19 lines of the 52 (`02` § The leads, L-22's row); `adversarial-council.md:36-38`",
  "the maintainer's answer recorded on #685, then the stream that applies it", "routed -> audited by `tools/t38-checks.sh`'s refs step once swept", "question (the pause)"),
 ("the renovation face in code-auditor or in the plan", "Low", "Improvement", "Q7", "L-24", "the coordinator", "`code-auditor/**`",
  "the coordinator's ruling recorded", "written -> no tool can", "question (the pause)"),
 ("the levels' third lab and D-WORKFLOW-195", "Low", "Improvement", "Q4", "L-28", "the coordinator", "`code-auditor/references/review-levels.md:11`, `:48-51`",
  "the coordinator's ruling recorded", "written -> no tool can", "question (the pause)"),
 ("the continuity section and the payload's pid", "Low", "Improvement", "Q2", "L-29", "the coordinator", "`code-auditor/SKILL.md:28-57`",
  "the coordinator's ruling recorded", "written -> no tool can", "question (the pause)"),
 ("a working branch's session file: pointer or state", "Low", "Spec Drift", "Q7", "L-68", "the coordinator", "`session-resume/SKILL.md:26`; #1014",
  "the coordinator's ruling recorded, then the stream", "written -> audited by #1014's freshness check", "question (the pause)"),
 ("#645's checkbox against D-WORKFLOW-078", "Low", "Spec Drift", "Q2", "L-27", "the coordinator", "#645 `:25`; `release-notes/SKILL.md:93-99`",
  "the coordinator's ruling on #645 recorded", "written -> no tool can", "question (the pause)"),
 ("the export's refresh list", "Low", "Improvement", "Q6", "L-30 to L-50, L-76 to L-78", "#911",
  "`02` § The leads and § What ... inherit", "#911 carries the list; the export refreshed by copying", "written -> audited by `tools/skills-check` over the export (#1373)", "inherit:#911"),
 ("council-research kept or retired", "Low", "Improvement", "Q5", "L-47", "the maintainer, #911",
  "`council-research/**` (4,150 lines)", "the maintainer's answer on #807, then #911's refresh", "written -> no tool can", "inherit:#911"),
 ("the rule errata", "Low", "Spec Drift", "Q1", "L-22's rule half, L-23, L-50, D-QA-040, worktrees.md, the lost spaces", "the coordinator",
  "`02` § What ... inherit", "the coordinator's sweep", "written -> audited by `tools/archaeology --reversal`", "inherit:coordinator"),
 ("tools/skills-check's inputs", "Low", "Test Gap", "Q2", "the checker's steps; register-check's LIVE", "#1373",
  "`tools/t38-checks.sh`, `tools/allow-*.txt`; `tools/register-check:49`", "#1373 carries them", "evidenced -> audited once #1373 is wired", "inherit:#1373"),
 ("Backlog leads: the stash archive's tool and the roster's prose copies", "Low", "Test Gap", "Q6", "L-18, L-44", "the coordinator",
  "`session-stash/SKILL.md:28`; `council/references/member-roster.md:19-25`", "the coordinator files them", "written -> audited by the tool each Backlog asks for", "inherit:coordinator"),
]

import os as _os, re as _re, sys as _sys
_A02 = _sys.argv[1] if len(_sys.argv) > 1 else _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "02-forward-audit.md")
def _leads(t):
    out = set()
    for _a, _b in _re.findall(r"L-(\d+) to L-(\d+)", t):
        out.update(range(int(_a), int(_b) + 1))
    return out | {int(_x) for _x in _re.findall(r"L-(\d+)", t)}
def pl(lead):  # the item that cites a lead, so no item number is typed
    hit = [n for n, _it in enumerate(ITEMS, 1) if lead in _leads(_it[4])]
    if len(hit) != 1:
        _sys.exit(f"t38-punch: refused: L-{lead:02d} is cited by {len(hit)} items")
    return f"PL-{hit[0]:02d}"
NO_ITEM = {  # a lead with no item of its own, and where it lives instead
 1: f"the drift overview; its in-scope halves are {pl(60)} (L-60) and {pl(51)} (L-51), its council half #911's ({pl(30)})",
 25: "a positive: no `TOTAL:` a reader would compute by hand (`02` § Positives)",
 26: "#314 `:14` and #287 `:16`: each issue's own checkbox, pre-existing tracked scope below",
}
_cited = set().union(*(_leads(_it[4]) for _it in ITEMS))
_rows = {int(_m) for _m in _re.findall(r"^\| L-(\d+) \|", open(_A02).read(), _re.M)}
_gap = sorted(_rows - _cited - set(NO_ITEM)); _extra = sorted((_cited | set(NO_ITEM)) - _rows); _both = sorted(_cited & set(NO_ITEM))
if not _rows or _gap or _extra or _both:
    _sys.exit(f"t38-punch: refused: leads {len(_rows)}, uncited {_gap}, unknown {_extra}, both {_both}")
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _read(name):  # stage D's records, once they exist: the bugs filed and the audit issue
    f = _os.path.join(_HERE, "..", "stage-d", name)
    return open(f).read() if _os.path.exists(f) else None
BUGS = {}
_t = _read("bugs.tsv")
if _t is not None:
    for _l in _t.splitlines():
        _k, _n, _ = _l.split("\t", 2)
        BUGS[_k] = int(_n)
    _want = {f"PL-{n:02d}" for n, _it in enumerate(ITEMS, 1) if _it[9].startswith("bug")}
    if set(BUGS) != _want:
        _sys.exit(f"t38-punch: refused: bugs.tsv names {sorted(BUGS)}, the items proposed as bugs are {sorted(_want)}")
AUDIT = (_read("audit-issue.txt") or "").strip()
# Stage E (S0's closing): every item's Phase 7 outcome. Resolved items cite their fix commits, read from the
# stage-e records by tools/t38-streams.py (never retyped); the six ruled with no stream are Deferred to their owners
# (the stream brief's rulings 3 and 8; the dispatch comment on #685 is 6553579374).
import json as _json, subprocess as _sp
DISPATCH = "6553579374"
DEFERRED = {
    "PL-48": f"recorded as written, the face stays in the plan (ruling 3; #685 comment {DISPATCH})",
    "PL-53": "#911 (the export's refresh; the list stays in `02` § What ... inherit)",
    "PL-54": "#807 (comment 6553118160, the maintainer's answer), then #911",
    "PL-55": f"the coordinator's sweep `b344408e46`; L-23, D-QA-040 and L-50 open, the coordinator's (#685 comment {DISPATCH})",
    "PL-56": "#1373 (`tools/skills-check`'s inputs)",
    "PL-57": "#1395 (L-18), #1396 (L-44)",
}
OUTCOMES = {}
if _read("bugs.tsv") is not None and _os.path.isdir(_os.path.join(_HERE, "..", "stage-e")):
    _r = _sp.run([_sys.executable, "-I", _os.path.join(_HERE, "t38-streams.py"), "outcomes"], capture_output=True, text=True)
    if _r.returncode:
        _sys.exit("t38-punch: refused: t38-streams.py outcomes failed: " + _r.stderr.strip())
    OUTCOMES = _json.loads(_r.stdout)
    _stream = {}
    for _f in sorted(_os.listdir(_os.path.join(_HERE, "..", "stage-e"))):
        _m = _re.match(r"^(S\d)-(PL-\d\d)[b-f]?\.txt$", _f)
        if _m:
            _stream.setdefault(_m.group(2), set()).add(_m.group(1))
    _all = {f"PL-{n:02d}" for n in range(1, len(ITEMS) + 1)}
    _miss = sorted(_all - set(OUTCOMES) - set(DEFERRED))
    _both = sorted(set(OUTCOMES) & set(DEFERRED))
    if _miss or _both:
        _sys.exit(f"t38-punch: refused: items with no outcome {_miss}, items both resolved and deferred {_both}")
    _log = _sp.run(["git", "-C", _HERE, "rev-list", "--abbrev=10", "--abbrev-commit", "87c2ab0fed..HEAD"], capture_output=True, text=True).stdout.split()
    _fixes = {c for cs in OUTCOMES.values() for c in cs}
    FIXED_AT = next((c for c in _log if c in _fixes), None)
    if FIXED_AT is None:
        _sys.exit("t38-punch: refused: no fix commit is in the lane's history")
def _outcome(k):
    if k in OUTCOMES:
        return "Resolved", ", ".join(f"`{c}`" for c in OUTCOMES[k]) + " (" + "/".join(sorted(_stream[k])) + ")"
    if k in DEFERRED:
        return "Deferred", DEFERRED[k]
    return "Open", None
def _prop(n, it):
    k = f"PL-{n:02d}"
    return f"bug #{BUGS[k]}" if k in BUGS else it[9]
print("# Punch List — M6.P2 T38, the skills, agents and settings\n")
print("**Generated:** 2026-11-01, by `tools/t38-punch.py` from one list (the items, the Phase 7 table and the index cannot disagree)")
print("**Source Audit:** `04-analysis.md`; the leads are `02` § The leads")
if OUTCOMES:
    print(f"**reviewed-at:** 87c2ab0fed; **fixed-at:** {FIXED_AT} (the last fix commit; a file cannot name the commit that writes it)")
if AUDIT:
    print(f"**Audit issue:** #{AUDIT}, a sub-issue of #685; the bugs: " + ", ".join(f"#{v} ({k})" for k, v in sorted(BUGS.items())))
sev = {s: sum(1 for i in ITEMS if i[1] == s) for s in ("Critical", "High", "Medium", "Low")}
print(f"**Total Items:** {len(ITEMS)} (Critical: {sev['Critical']}, High: {sev['High']}, Medium: {sev['Medium']}, Low: {sev['Low']})\n")
print("---\n")
print("## Instructions for the executing stream\n")
print("Every item is at a Phase 7 outcome since stage E (the gate below): the stream brief `docs/reviews/briefs/t38-streams.md` at `95052eaf78`, the coordinator's, decided each.")
print("Items whose proposal reads `bug` are filed at stage D with their trace, their `Already written:` line and their VM line, *\"Can this be done on")
print("the VM? No -- the tree, the tool or the register shows it\"*. A fix lands only in the fork-adapted skills, never in the council family")
print("(ruling (d)); each fix's commit records its acceptance line before and after and `tools/t38-checks.sh`'s exit.\n")
print("---\n")
for n, (title, s, cat, q, leads, owner, where, acc, ladder, prop) in enumerate(ITEMS, 1):
    print(f"## PL-{n:02d}: {title}\n")
    print(f"- **Severity:** {s}")
    print(f"- **Category:** {cat}")
    print(f"- **Question:** {q}")
    print(f"- **Source finding:** {leads}")
    print(f"- **Owner area:** {owner}")
    print(f"- **Where:** {where} (lines at the dispatch tip `87c2ab0fed`)")
    print(f"- **Acceptance:** {acc}")
    print(f"- **Ladder:** {ladder}")
    print(f"- **Proposed:** {_prop(n, ITEMS[n - 1])}")
    _w, _e = _outcome(f"PL-{n:02d}")
    print(f"- **Phase 7:** {_w}" + (f", {_e}" if _e else "") + "\n")
print("## Pre-existing tracked scope (NOT punch items -- exempt from the Phase 7 gate)\n")
print(f"- #810 -- the lint's Local epic tier; closes when `templates.md`'s fix reaches `next` ({pl(56)} is outside its checkbox)")
print(f"- #342 -- time-free estimates; {pl(5)} answers it for the fork-adapted skills")
print(f"- #640 -- the layout's drift; {pl(4)} names it")
print(f"- #1044, #1045 -- the export's toolchain and refresh; {pl(30)} carries the export's list\n")
print("- #314, #287 -- L-26: neither checkbox is met by the skill's text; each stays with its issue or goes to the stream brief\n")
print("## Leads with no item of their own\n")
print(f"Every one of the {len(_rows)} leads in `02` § The leads is cited by an item above or listed here; the generator refuses otherwise.\n")
for _n, _why in sorted(NO_ITEM.items()):
    print(f"- L-{_n:02d} -- {_why}")
print()
print("## Phase 7 resolution gate\n")
print("| Item | Outcome | Evidence |")
print("| --- | --- | --- |")
for n, it in enumerate(ITEMS, 1):
    _w, _e = _outcome(f"PL-{n:02d}")
    print(f"| PL-{n:02d} | **{_w}** | {_e} |" if _e else f"| PL-{n:02d} | Open | {_prop(n, it)} |")
print("\n## Machine-readable index\n")
print("```yaml")
print("punch_index:")
for n, (title, s, cat, q, leads, owner, where, acc, ladder, prop) in enumerate(ITEMS, 1):
    print(f"- id: PL-{n:02d}")
    print(f"  severity: {s}")
    print(f"  category: {cat}")
    print(f"  question: {q}")
    print(f"  source_finding: \"{leads}\"")
    print(f"  owner_area: \"{owner}\"")
    print(f"  outcome: {_outcome(f'PL-{n:02d}')[0].lower()}")
    print(f"  proposed: \"{_prop(n, ITEMS[n - 1])}\"")
print("```")

"""t38-tables.py: T38 (#685) stage B's generated tables. Each subcommand prints Markdown on stdout and exits 1
when its own assertion fails, so a table is trusted only after its failure was seen on a constructed drift
(tools/t38-tables-drift.sh). EXPORT is the read tree (`git archive HEAD .claude/agents .claude/skills`), REPO the
lane's worktree, read with `git -C REPO show <ref>:<path>` only. Nothing here calls a provider or writes a file.

    t38-tables.py coverage EXPORT ANSWERS  -- 02 § Coverage: one row per path, joined with ANSWERS (a TSV)
    t38-tables.py q4 EXPORT REPO           -- 04 Q4: the IDs, the tools, the counts, the roster, the pins
    t38-tables.py q5 EXPORT REPO           -- 04 Q5: the load table
    t38-tables.py q6 EXPORT REPO           -- 04 Q6: the reachability table
    t38-tables.py q7 EXPORT                -- 04 Q7: the duplicated sections and their diff
"""
import collections, difflib, hashlib, json, pathlib, re, subprocess, sys

CO = "3a9b0aec81"  # the coordinator's tip merged at dispatch: the register is read there (brief § 9)
SKILLS = ["code-auditor", "mini-retro", "futro", "session-resume", "session-stash", "begin-delivery",
          "developer-relations", "release-notes", "council", "council-research"]
AGENTS = ["claude", "deepseek", "gemini", "gpt", "grok", "kimi", "mistral", "muse"]
ACTIVE = ["claude", "gemini", "gpt", "kimi", "muse"]
fails = []


def fail(msg):
    fails.append(msg)
    print("FAIL " + msg, file=sys.stderr)


def done():
    print(f"t38-tables: {len(fails)} failure(s)", file=sys.stderr)
    sys.exit(1 if fails else 0)


def git(repo, ref, path, ok_missing=False):
    r = subprocess.run(["git", "-C", repo, "show", f"{ref}:{path}"], capture_output=True, text=True)
    if r.returncode:
        if ok_missing:
            return None
        sys.exit(f"t38-tables: cannot read {ref}:{path}")
    return r.stdout


def gitc(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True).stdout


def files(export):
    base = pathlib.Path(export) / ".claude"
    return sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file())


def text(export, rel):
    return (pathlib.Path(export) / ".claude" / rel).read_text(errors="replace")


def origin(rel):
    if rel.startswith("agents/") or rel.startswith("skills/council/") or rel.startswith("skills/council-research/"):
        return "the export"
    if rel.startswith(("skills/developer-relations/", "skills/release-notes/")):
        return "synthesized here"
    return "imported and adapted"


def front(src):
    """The front matter's top-level keys, parsed whole (a `model:` list is the next lines)."""
    if not src.startswith("---\n"):
        return {}
    body = src[4:src.index("\n---", 4)]
    out, key = {}, None
    for line in body.split("\n"):
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = m.group(2)
        elif key and line.startswith("  - "):
            out[key] = (out[key] + " " + line[4:]).strip()
    return out


def scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        v = v[1:-1]
        v = v.replace("''", "'") if v and "''" in v else v
    return v


def cell(s):
    return s.replace("|", "\\|")


def coverage(export, answers):
    paths = files(export)
    rows = {}
    for n, line in enumerate(open(answers), 1):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) != 9:
            fail(f"{answers}:{n} has {len(f)} fields, not 9")
            continue
        if f[0] in rows:
            fail(f"{answers}:{n} repeats {f[0]}")
        rows[f[0]] = f[1:]
    if len(paths) != 52:
        fail(f"the export holds {len(paths)} paths, not 52")
    for p in sorted(set(paths) - set(rows)):
        fail(f"no answers row for {p}")
    for p in sorted(set(rows) - set(paths)):
        fail(f"an answers row names {p}, which the export does not hold")
    print("| Path | Origin | Tier | Order | Lines | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |")
    print("| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |")
    for p in sorted(paths, key=lambda p: (int(rows.get(p, ["99"])[0]), p)):
        if p not in rows:
            continue
        a = rows[p]
        lines = text(export, p).count("\n")
        print(f"| `.claude/{p}` | {origin(p)} | fork-own | {a[0]} | {lines} | " + " | ".join(cell(x) for x in a[1:]) + " |")
    print(f"\n`t38-tables.py coverage`: {len(paths)} paths, {len(rows)} answers rows, one row per path.")
    done()


def q4(export, repo):
    paths = files(export)
    reg = git(repo, CO, "docs/decision-register.md")
    cut = reg.index("\n## Open decisions")
    decided, opened = reg[:cut], reg[cut:]
    ids = collections.defaultdict(set)
    tools = collections.defaultdict(set)
    for p in paths:
        t = text(export, p)
        for m in re.finditer(r"D-[A-Z]+-[0-9]+", t):
            ids[m.group(0)].add(p)
        for m in re.finditer(r"(?<![\w/.-])tools/[A-Za-z0-9_][A-Za-z0-9_./-]*", t):
            tools[m.group(0).rstrip(".,;:)")].add(p)
    print("#### (a) Every decision ID the 52 cite, at the coordinator's tip `%s`\n" % CO)
    print("| ID | Decided rows | Open rows | Files citing it |")
    print("| --- | ---: | ---: | --- |")
    for i in sorted(ids, key=lambda s: (s.rsplit("-", 1)[0], int(s.rsplit("-", 1)[1]))):
        d, o = decided.count(f"| {i} |"), opened.count(f"| {i} |")
        if d != 1 or o:
            fail(f"{i}: decided {d}, open {o}")
        print(f"| {i} | {d} | {o} | {', '.join('`'+x+'`' for x in sorted(ids[i]))} |")
    print(f"\n{len(ids)} IDs, each in one decided row and no open row.\n")
    allowed_missing = {"tools/call", "tools/list", "tools/council/node_modules"}  # MCP method names; an install dir
    print("#### (b) Every `tools/...` the 52 name, at HEAD\n")
    print("| Tool | At HEAD | Files naming it |")
    print("| --- | --- | --- |")
    missing = set()
    for t in sorted(tools):
        present = subprocess.run(["git", "-C", repo, "cat-file", "-e", f"HEAD:{t.rstrip('/')}"], capture_output=True).returncode == 0
        if not present:
            missing.add(t)
        print(f"| `{t}` | {'present' if present else 'absent'} | {len(tools[t])} |")
    for t in sorted(missing - allowed_missing):
        fail(f"{t} is named and absent, and is not one of the three known non-tools")
    print(f"\n{len(tools)} named, {len(tools) - len(missing)} present, {len(missing)} absent: "
          f"{', '.join('`'+m+'`' for m in sorted(missing))} (MCP method names and an untracked install directory).\n")
    print("#### (c) Every count the read found a skill stating, recomputed\n")
    print("| Where | Stated | Recomputed | Holds |")
    print("| --- | --- | --- | --- |")
    words = {"three": 3, "four": 4, "five": 5, "six": 6, "twelve": 12}

    def row(where, stated, got):
        print(f"| {where} | {stated} | {got} | {'yes' if str(stated).split()[0] == str(got).split()[0] else 'no'} |")
    ca = text(export, "skills/code-auditor/SKILL.md")
    sec = ca[ca.index("## Evidence floor"):ca.index("\n## When to use")]
    m = re.search(r"(\w+) hard rules", sec)
    row("`code-auditor/SKILL.md` § Evidence floor: *\"%s hard rules\"*" % m.group(1), words[m.group(1).lower()],
        "%d (numbered %s)" % (len(re.findall(r"^\d+\. \*\*", sec, re.M)), ", ".join(re.findall(r"^(\d+)\. \*\*", sec, re.M))))
    br = git(repo, "HEAD", "docs/blindspot-register.md")
    m = re.search(r"(\w+) recorded\s+failure modes", ca)
    heads = re.findall(r"^## (\d+)\.", br, re.M)
    row("`code-auditor/SKILL.md`: *\"%s recorded failure modes\"*" % m.group(1), words[m.group(1).lower()],
        "%s (the last numbered heading; %d numbered headings)" % (heads[-1], len(heads)))
    lifecycle = re.findall(r"^\| (\d+(?:\.\d+)?)\s+\|", ca[ca.index("## Audit lifecycle"):ca.index("**Before Phase 6")], re.M)
    mr = text(export, "skills/mini-retro/SKILL.md")
    m = re.search(r"full (\d+)-phase methodology", mr)
    row("`mini-retro/SKILL.md`: *\"the full %s-phase methodology\"*" % m.group(1), int(m.group(1)),
        "%d (`code-auditor`'s lifecycle rows: %s)" % (len(lifecycle), ", ".join(lifecycle)))
    sa = text(export, "skills/mini-retro/references/scoped-audit.md")
    n_sa = len(re.findall(r"^### Check \d+ ", sa, re.M))
    proc = mr[mr.index("Summary:\n\n1. **AC conformance"):mr.index("Each check produces a verdict")]
    n_proc = len(re.findall(r"^\d+\. \*\*", proc, re.M))
    fmt = mr[mr.index("### Scoped audit findings (Step 2.5)"):mr.index("### Practice adjustments")]
    n_fmt = len(re.findall(r"^- \*\*", fmt, re.M))
    n_tpl = len(re.findall(r"^- \*\*Check \d+", text(export, "skills/mini-retro/references/template.md"), re.M))
    row("`mini-retro/SKILL.md` Step 2.5's procedure, its checks", n_proc, f"{n_sa} (`### Check` headings in `scoped-audit.md`)")
    row("`mini-retro/SKILL.md` § format, *Scoped audit findings* lines", n_fmt, n_sa)
    row("`mini-retro/references/template.md`, `Check N` lines", n_tpl, n_sa)
    bd = text(export, "skills/begin-delivery/SKILL.md")
    m = re.search(r"contains the (\w+) phase-tier audit spot-check verdicts", bd)
    row("`begin-delivery/SKILL.md`: *\"the %s phase-tier audit spot-check verdicts\"*" % m.group(1), words[m.group(1)], n_sa)
    fu = text(export, "skills/futro/SKILL.md")
    q4s = fu[fu.index("**4. What could we be missing?**"):fu.index("**5. What adjustments")]
    m = re.search(r"Apply (\w+) techniques", q4s)
    row("`futro/SKILL.md` question 4: *\"Apply %s techniques\"*" % m.group(1), words[m.group(1)], len(re.findall(r"^- \*\*", q4s, re.M)))
    rn = text(export, "skills/release-notes/SKILL.md")
    m = re.search(r"(\w+) or (\w+)\s+short paragraphs", rn)
    pr = rn[rn.index(m.group(0)):rn.index("What it never carries")]
    row("`release-notes/SKILL.md`: *\"%s\"*" % " ".join(m.group(0).split()), f"{words[m.group(1)]} or {words[m.group(2)]}", len(re.findall(r"^\d+\. ", pr, re.M)))
    cb = text(export, "skills/council/COUNCIL-BUNDLE.md")
    sums = [l.split(None, 1) for l in text(export, "skills/council/COUNCIL-BUNDLE.SHA256SUMS").splitlines() if l.strip()]
    m_, d_, a_ = 0, 0, 0
    for h, p in sums:
        b = subprocess.run(["git", "-C", repo, "show", "HEAD:" + p.lstrip("*")], capture_output=True)
        if b.returncode:
            a_ += 1
        elif hashlib.sha256(b.stdout).hexdigest() == h:
            m_ += 1
        else:
            d_ += 1
    n = re.search(r"\*\*Files:\*\* (\d+), byte-identical", cb).group(1)
    row("`council/COUNCIL-BUNDLE.md:4`: *\"Files: %s, byte-identical to that commit\"*" % n, n,
        f"{len(sums)} entries; {m_} match the tree, {d_} differ, {a_} absent")
    print("\n#### (e) The roster: the rule, `member-roster.md` and the agents\n")
    rule = git(repo, "HEAD", ".claude/rules/adversarial-council.md")
    rule_rows = {r.group(1).lower(): (r.group(2), r.group(3)) for r in re.finditer(r"^\| (Claude|GPT) \| `([^`]+)` \| `([^`]+)` \|", rule, re.M)}
    roster = text(export, "skills/council/references/member-roster.md")
    mr_rows = {r.group(1): (r.group(2), r.group(3)) for r in re.finditer(r"^\| `council-member-(\w+)`\s*\| `([^`]+)`[^|]*?effort=`(\w+)`", roster, re.M)}
    print("| Seat | Agent's `model:` | `member-roster.md` | `adversarial-council.md:77-78` | Agree |")
    print("| --- | --- | --- | --- | --- |")
    for a in ACTIVE:
        fm = front(text(export, f"agents/council-member-{a}.agent.md"))
        mm = re.match(r'"?([^ "]+) \(.*effort=(\w+)', scalar(fm.get("model", "")))
        agent = (mm.group(1), mm.group(2)) if mm else ("?", "?")
        listed = mr_rows.get(a, ("?", "?"))
        ruled = rule_rows.get(a)
        ok = agent == listed and (ruled is None or ruled == agent)
        if not ok:
            fail(f"roster: {a} agent {agent} roster {listed} rule {ruled}")
        print(f"| {a} | `{agent[0]}` `{agent[1]}` | `{listed[0]}` `{listed[1]}` | {('`%s` `%s`' % ruled) if ruled else '-- (not a rule row)'} | {'yes' if ok else 'no'} |")
    print("\n#### (f) The pins: each agent's sha256 against `verifier-pins.json` at HEAD\n")
    pins = json.loads(git(repo, "HEAD", "verifier-pins.json"))["pins"]
    print("| Agent file | Pin | Bytes | Match |")
    print("| --- | --- | --- | --- |")
    for a in AGENTS:
        p = f".claude/agents/council-member-{a}.agent.md"
        h = hashlib.sha256((pathlib.Path(export) / p).read_bytes()).hexdigest()
        pin = pins.get(p, {}).get("sha", "")
        if h != pin:
            fail(f"pin: {p}")
        print(f"| `{p}` | `{pin[:16]}` | `{h[:16]}` | {'MATCH' if h == pin else 'DIFF'} |")
    done()


RECORDS = {"code-auditor": "docs/audits", "mini-retro": "docs/retros", "futro": "docs/futros",
           "session-stash": ".github/sessions/archived", "council": "research/council-runs",
           "council-research": "research/council-research", "release-notes": "docs/releases/pr"}


def named(repo, pathspec, name):
    """Lines under pathspec at HEAD naming the skill: `name`, `name` skill, or skills/name/."""
    pat = r"`%s`|%s skill|skills/%s/" % (re.escape(name), re.escape(name), re.escape(name))
    out = gitc(repo, "grep", "-h", "-c", "-E", pat, "HEAD", "--", pathspec)
    return sum(int(x.rsplit(":", 1)[-1]) for x in out.split() if x.rsplit(":", 1)[-1].isdigit())


def entries(repo, d):
    return len([x for x in gitc(repo, "ls-tree", "--name-only", f"HEAD:{d}").split("\n") if x]) if git(repo, "HEAD", d, ok_missing=True) is not None else 0


def q5(export, repo):
    paths = files(export)
    print("| Skill or agent | Files | Lines | Description (characters) | Records under | Entries | Commits there | Plan lines | Brief lines |")
    print("| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |")
    tf = tl = 0
    for s in SKILLS:
        fs = [p for p in paths if p.startswith(f"skills/{s}/")]
        if not fs:
            fail(f"q5: no files for {s}")
            continue
        lines = sum(text(export, p).count("\n") for p in fs)
        desc = scalar(front(text(export, f"skills/{s}/SKILL.md")).get("description", ""))
        if not desc:
            fail(f"q5: {s} has no description")
        d = RECORDS.get(s)
        ent = entries(repo, d) if d else 0
        com = len([x for x in gitc(repo, "log", "--oneline", "HEAD", "--", d).split("\n") if x]) if d else 0
        tf += len(fs); tl += lines
        print(f"| `{s}` | {len(fs)} | {lines} | {len(desc)} | {('`'+d+'/`') if d else '--'} | {ent} | {com} | "
              f"{named(repo, 'docs/reviews/plan-for-the-plan.md', s)} | {named(repo, 'docs/reviews/briefs', s)} |")
    for a in AGENTS:
        p = f"agents/council-member-{a}.agent.md"
        lines = text(export, p).count("\n")
        desc = scalar(front(text(export, p)).get("description", ""))
        if not desc:
            fail(f"q5: {a} has no description")
        tf += 1; tl += lines
        print(f"| `council-member-{a}` | 1 | {lines} | {len(desc)} | -- | -- | -- | -- | -- |")
    print(f"| **Total** | {tf} | {tl} | | | | | | |")
    if tf != 52:
        fail(f"q5: {tf} files, not 52")
    done()


ALREADY = {  # a row the record shows nothing run under: what sessions already did on its strength
    "council-research": "Already written: nothing a run left -- `research/council-research/` holds 0 entries; three work-log lines name the skill; every session's listing carried its description.",
    "begin-delivery": "Already written: no kickoff comment or plan names it; every session's listing carried its description, and its `begin-exploration` hedges reach readers through `mini-retro` and `futro` (L-22).",
    "session-resume": "Already written: sessions resumed from the pointers and the canonical stash; the skill's own pointer rule (L-68) is what a lane would have read.",
    "developer-relations": "Already written: rocknix.org pages drafted under it (#323, D-WORKFLOW-068); its records live in the site's repository, not here.",
}


def q6(export, repo):
    paths = files(export)
    got = sorted({p.split("/")[1] for p in paths if p.startswith("skills/")})
    if got != sorted(SKILLS):
        fail(f"q6: the skills are {got}")
    print("| Skill or agent | Trigger in the description | Other skills naming it | Plan lines | Brief lines | Work-log lines | Records | Reachable by record | Already written (rows with no record) |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |")
    for s in SKILLS:
        desc = scalar(front(text(export, f"skills/{s}/SKILL.md")).get("description", ""))
        trig = "Use when" if "Use when" in desc else ("Use for" if "Use for" in desc else "none")
        others = sum(len(re.findall(r"`%s`|%s skill" % (re.escape(s), re.escape(s)), text(export, p)))
                     for p in paths if not p.startswith(f"skills/{s}/"))
        d = RECORDS.get(s)
        ent = entries(repo, d) if d else 0
        plan, briefs, logs = (named(repo, x, s) for x in ("docs/reviews/plan-for-the-plan.md", "docs/reviews/briefs", "docs/work-logs"))
        reach = "yes" if ent else "no record kept"
        note = ALREADY.get(s, "")
        if reach != "yes" and not note:
            fail(f"q6: {s} has no record and no Already written line")
        print(f"| `{s}` | {trig} | {others} | {plan} | {briefs} | {logs} | {ent if d else '--'} | {reach} | {note} |")
    roster = git(repo, "HEAD", "scripts/lib/council-roster.ts")
    for a in AGENTS:
        desc = scalar(front(text(export, f"agents/council-member-{a}.agent.md")).get("description", ""))
        inactive = bool(re.search(r"do not invoke|Inactive|Outside every run profile", desc, re.I))
        ids = re.search(r'MEMBER_IDS = \[([^\]]*)\]', roster)
        if not ids:
            fail("q6: council-roster.ts defines no MEMBER_IDS")
        prof = (["definitive"] if ids and f'"{a}"' in ids.group(1) else []) + \
            [k for k, v in re.findall(r'"?([a-z-]+)"?: \[([^\]]*)\]', roster) if f'"{a}"' in v]
        how = ", ".join(prof) if prof else ("the env override (`:87-90`)" if a == "mistral" else "none")
        if (a in ACTIVE) == inactive:
            fail(f"q6: {a}'s description and the active list disagree")
        print(f"| `council-member-{a}` | {'inactive: says do not invoke' if inactive else 'Use when'} | -- | -- | -- | -- | -- | "
              f"{'pinned; profiles: ' + how} | {'Already written: kept and pinned, ruling (e); its description is in every listing' if inactive else ''} |")
    done()


SECTIONS = [("## pixelelated continuation", ["futro", "mini-retro", "begin-delivery"]),
            ("## Execution discipline — SERIAL (hard gate)", ["code-auditor", "futro", "mini-retro", "begin-delivery"])]


def section(src, head):
    i = src.find("\n" + head + "\n")
    if i < 0:
        return None
    j = src.find("\n## ", i + len(head) + 2)
    return src[i + 1:j if j > 0 else len(src)].rstrip("\n").split("\n")


def q7(export):
    for head, skills in SECTIONS:
        print(f"#### `{head}`\n")
        secs = {}
        for s in skills:
            sec = section(text(export, f"skills/{s}/SKILL.md"), head)
            if sec is None:
                fail(f"q7: {s} has no section {head!r}")
                continue
            secs[s] = sec
        base = skills[0]
        for s in skills[1:]:
            if s not in secs or base not in secs:
                continue
            d = [l for l in difflib.unified_diff(secs[base], secs[s], f"{base}", f"{s}", lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
            print(f"- `{base}` and `{s}`: " + ("identical, %d lines" % len(secs[s]) if not d else "differ on %d line(s)" % len(d)))
            for l in d:
                print("  - `" + l[:160].replace("`", "'") + "`")
        print()
    t = text(export, "skills/code-auditor/references/templates.md")
    p = text(export, "skills/code-auditor/references/phases.md")

    def entry(src):
        i = src.index("### AC-NN: [Criterion Text]")
        return src[i:src.index("```", i)].rstrip("\n").split("\n")
    d = [l for l in difflib.unified_diff(entry(p), entry(t), "phases.md", "templates.md", lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
    print("#### The criterion entry: `phases.md` § Phase 2 against `templates.md`'s *\"Reproduced here\"*\n")
    print(f"- {len(d)} line(s) differ:")
    for l in d:
        print("  - `" + l[:160].replace("`", "'") + "`")
    if not d:
        fail("q7: the two criterion entries are identical, against the read")
    done()


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"coverage": coverage, "q4": q4, "q5": q5, "q6": q6, "q7": q7}[cmd](*args)

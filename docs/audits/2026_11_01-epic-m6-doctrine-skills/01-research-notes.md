# Research notes — M6.P2 T38, the skills, agents and settings (#685)

Stage A, 2026-11-01, at the dispatch tip `87c2ab0fed`; the lane's HEAD `11fa8f95b8` adds only the seeded pointer. Every tool line below reaches this file through an include marker (`tools/include.py`), copied from the file under `stage-a/` it names, never retyped.

## Pre-flight: what this session has read

- **The dispatch comment** on #685 (6552443399) and **the brief whole** at the dispatch tip: `docs/reviews/briefs/doctrine-skills.md`, version 2 at `fa4a9a5b0d` plus `## Errata before dispatch`.
- **#685's body**, 77 lines after the coordinator's fill: the 22 criteria and § 5's VM paragraph in place of the generated one. Its four comments are the three leads and the dispatch (`stage-a/issues.txt`).
- **The rules: not yet at the coordinator's tip.** The session loaded the rules of T5's worktree (`52e6794ba7`) when it started, and those differ from the coordinator's tip `3a9b0aec81` in 9 files, +175 -27 (`stage-a/stage-a-extra.out`).
  - At stage A the lane read the changes at `3a9b0aec81` of the four that bind how it works: `engineering-practices.md`, `instruction-files.md`, `fork-workflow.md` and `device-builds.md`. What they bind here: `rc=$?` on its own line; the widened read mask, which is § 5's `M`; a count is a claim about one tree; a FAIL-first stub is checked against the unfixed text first.
  - At stage B every rule in the brief's § 3 item 1 table is read at `3a9b0aec81` by `git show`, section by section, and listed here as it is read. Then come the blindspots and the friction log at their lines, T4's audit at `6ec78bbf8c`, and T45's records at `ae08d48392` (§ 3 items 3 to 7).
- **The register** at `3a9b0aec81`: its decided table above `:780`, for the 16 IDs the 52 cite (each `dec:1 open:0`) and the highest decided row per area (`00`, A-08).

## § Scope

### The membership block, as run

The block is the brief's § 2, extracted from the brief at the dispatch tip by `sed -n '390,507p'` between its fences (`:389`, `:508`): 118 lines. Its sha256 prefix, computed on the copy below after it is extracted back out of this file, is checked against the brief's `7fa0430cf613e867` in `00` (A-02) and again before each commit.

<!-- include: stage-a/membership.sh lang bash -->
```bash
mkdir -p .qa-scratch/t38
cat > .qa-scratch/t38/membership.py <<'PYEOF'
import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
def gre(g):
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i]=="?": out+="[^/]"; i+=1
        elif g[i]=="{":
            j=g.index("}",i); out+="(?:"+"|".join(gre(x) for x in g[i+1:j].split(","))+")"; i=j+1
        else: out+=re.escape(g[i]); i+=1
    return out
def compile_globs(globs):
    inc=collections.defaultdict(list); exc=collections.defaultdict(list)
    for g in globs:
        neg=g.startswith("!"); g=g[1:] if neg else g
        tree="es" if g.startswith("es:") else "distribution"
        g=g[3:] if tree=="es" else g
        (exc if neg else inc)[tree].append(re.compile(gre(g)+r"\Z"))
    return inc,exc
doc=json.load(open("docs/reviews/slices.json"))
sl=[]
for s in doc["slices"]:
    sels=s.get("select",{}); sels=sels if isinstance(sels,list) else [sels]
    comp=[]
    for sel in sels:
        comp.append((set(sel.get("areas",[s["area"]])), compile_globs(sel["globs"]) if sel.get("globs") else None,
                     set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")), set(sel["tier"]) if sel.get("tier") else None))
    sl.append((s,comp))
inv=json.load(open("docs/reviews/inventory.json"))
hd=inv["header"]["distribution"]
print("distribution head:",hd["head"]); print("distribution merge_base:",hd["merge_base"]); print("distribution upstream:",hd["upstream"],hd["upstream_head"])
cols=inv["columns"]; print("columns:",cols)
rows=[dict(zip(cols,r)) for r in inv["rows"]]
def match(row,areas,comp,reach,tier):
    if row["area"] not in areas: return False
    if reach and row["reach"] not in reach: return False
    if tier and row["tier"] not in tier: return False
    if comp is None: return True
    inc,exc=comp; t=row["tree"]; p=row["path"]
    return any(r.match(p) for r in inc.get(t,())) and not any(r.match(p) for r in exc.get(t,()))
def hits(row):
    non=[s["id"] for s,c in sl if any(not rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)]
    if non: return non,"non-rest"
    return [s["id"] for s,c in sl if any(rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)],"rest"
def globhits(p):
    out=[]
    for s,c in sl:
        for a,cm,r,rest,t in c:
            if cm is None: continue
            inc,exc=cm
            if any(x.match(p) for x in inc.get("distribution",())) and not any(x.match(p) for x in exc.get("distribution",())):
                out.append((s["id"],s["k"],"rest" if rest else "non-rest")); break
    return out
kof={s["id"]:s["k"] for s,_ in sl}
mine=[]
for r in rows:
    if r["tree"]!="distribution": continue
    h,kind=hits(r)
    if h==["doctrine-skills"]: mine.append(r)
mine.sort(key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine), "reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)),"lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"))
rd=[r for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"]
print("read lines:",sum((r["lines"] or 0) for r in rd),"of which fork-own:",sum((r["lines"] or 0) for r in rd if r["tier"]=="fork-own"),"vendor-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="vendor-carried"))
print("overlap:",sum(1 for r in mine if r["overlap"]),"last_upstream_commit set:",sum(1 for r in mine if r["last_upstream_commit"]))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("CLAIMS")
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
tree=[l.strip() for l in open(sys.argv[2]) if l.strip()]
named=tree+[".claude/settings.json",".claude/settings.local.json",".claude/rules/adversarial-council.md",".claude/rules/council-substrate-integrity.md",".claude/rules/instruction-files.md","CLAUDE.md","AGENTS.md","scripts/council-invoke.ts","scripts/lib/council-verification.ts","tools/lint-audit-artifacts","tools/rules-check","docs/reviews/plan-for-the-plan.md",".github/sessions/saved-session-state-next.md"]
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY; globs:",globhits(p)); continue
    h,kind=hits(r); print(p, "in-T38" if p in got else "not-in-T38", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"lang",r["language"],"area",r["area"],"reach",r["reach"])
print("CLAUDE TREE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["path"].startswith(".claude/"):
        h,kind=hits(r)
        k=(r["tree"],".claude/"+r["path"].split("/")[1],tuple(h),kind,r["area"])
        cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:(kv[0][0],kv[0][1])): print(v,"paths",ln[k],"lines",k)
print("DOCTRINE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["area"]=="doctrine":
        h,kind=hits(r)
        k=(r["tree"],tuple(h),kind)
        cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; MB=c445081a59
git -C "$W" ls-tree -r --name-only "$P1" -- .claude/ | /usr/bin/grep -v '^\.claude/rules/' > .qa-scratch/t38/tree.txt
python3 -I .qa-scratch/t38/membership.py /dev/null .qa-scratch/t38/tree.txt > .qa-scratch/t38/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="distribution" {print $2}' .qa-scratch/t38/block-1.txt > .qa-scratch/t38/paths.txt
wc -l .qa-scratch/t38/paths.txt .qa-scratch/t38/tree.txt
python3 -I .qa-scratch/t38/membership.py .qa-scratch/t38/paths.txt .qa-scratch/t38/tree.txt > .qa-scratch/t38/block-2.txt
/usr/bin/grep -E '^(distribution |mine:|only-|lines:|fork-own lines:|read lines:|overlap:)' .qa-scratch/t38/block-2.txt
IH=$(sed -n 's/^distribution head: //p' .qa-scratch/t38/block-2.txt)
git -C "$W" ls-tree -r --name-only "$IH" -- .claude/ | /usr/bin/grep -v '^\.claude/rules/' | diff - .qa-scratch/t38/paths.txt && echo "ls-tree at the inventory's head = paths.txt"
diff .qa-scratch/t38/paths.txt .qa-scratch/t38/tree.txt && echo "paths.txt = ls-tree at $P1"
for p in $(cat .qa-scratch/t38/tree.txt); do git -C "$W" show "$P1:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t38/tree.txt); do git -C "$W" show "$P1:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t38/paths.txt); do git -C "$W" show "$IH:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, the inventory paths at its head:", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t38/tree.txt | wc -l
git -C "$W" diff --shortstat "$MB" "$P1" -- .claude/ ':(exclude).claude/rules/'
git -C "$W" diff --shortstat "$IH" "$P1" -- .claude/ ':(exclude).claude/rules/'
echo "(end)"
```

**Its output** (`stage-a/membership.out`), run from the lane's worktree at 02:44:16. `diff` against the brief's expected lines (`:516-536`) printed nothing, rc 0, so these are its lines byte for byte and no delta stands beside them:

<!-- include: stage-a/membership.out -->
```text
  52 .qa-scratch/t38/paths.txt
  52 .qa-scratch/t38/tree.txt
 104 total
distribution head: eb4763e3cc9bcd729830cd85f1719bbd4f28db10
distribution merge_base: c445081a59518f37d9776e5412dd7b14910696f7
distribution upstream: upstream/next c1f1746828ca47dfc751ffe44bb47b6b259883d7
mine: 52 paths.txt: 52 equal: True
only-mine: []
only-paths.txt: []
lines: 12734 reach: {'n/a': 52} tier: {'fork-own': 52} lang: {'markdown': 51, 'other': 1}
fork-own lines: 12734
read lines: 0 of which fork-own: 0 vendor-carried lines: 0
overlap: 0 last_upstream_commit set: 0
ls-tree at the inventory's head = paths.txt
paths.txt = ls-tree at 2174265e9c
wc -l, every path at the P1 hash: 12734
grep -c, every path at the P1 hash: 12734
grep -c, the inventory paths at its head: 12734
0
 52 files changed, 12734 insertions(+)
(end)
```

**The CLAIMS** (`stage-a/membership-block-2.txt`): the 52, each `in-T38 non-rest [('doctrine-skills', 38)]`, then the thirteen neighbours the block names:

<!-- include: stage-a/membership-block-2.txt match NOT IN INVENTORY|not-in-T38 -->
```text
.claude/settings.json NOT IN INVENTORY; globs: [('doctrine-skills', 38, 'non-rest')]
.claude/settings.local.json NOT IN INVENTORY; globs: [('doctrine-skills', 38, 'non-rest')]
.claude/rules/adversarial-council.md not-in-T38 non-rest [('doctrine-rules', 4)] tier fork-own lines 124 lang markdown area doctrine reach n/a
.claude/rules/council-substrate-integrity.md not-in-T38 non-rest [('doctrine-rules', 4)] tier fork-own lines 253 lang markdown area doctrine reach n/a
.claude/rules/instruction-files.md not-in-T38 non-rest [('doctrine-rules', 4)] tier fork-own lines 224 lang markdown area doctrine reach n/a
CLAUDE.md not-in-T38 non-rest [('doctrine-rules', 4)] tier fork-own lines 202 lang markdown area doctrine reach n/a
AGENTS.md not-in-T38 non-rest [('doctrine-rules', 4)] tier fork-own lines 351 lang markdown area doctrine reach n/a
scripts/council-invoke.ts not-in-T38 non-rest [('tooling-council', 45)] tier fork-own lines 3701 lang typescript area tooling-and-guards reach n/a
scripts/lib/council-verification.ts not-in-T38 non-rest [('tooling-council', 45)] tier fork-own lines 431 lang typescript area tooling-and-guards reach n/a
tools/lint-audit-artifacts not-in-T38 non-rest [('tooling-guards', 10)] tier fork-own lines 426 lang python area tooling-and-guards reach n/a
tools/rules-check not-in-T38 non-rest [('tooling-guards', 10)] tier fork-own lines 245 lang python area tooling-and-guards reach n/a
docs/reviews/plan-for-the-plan.md not-in-T38 rest [('doctrine-reference', 39)] tier fork-own lines 499 lang markdown area doctrine reach n/a
.github/sessions/saved-session-state-next.md not-in-T38 non-rest [('records', 46)] tier fork-own lines 355 lang markdown area records reach n/a
```

**`.claude/` and the doctrine, by slice:**

<!-- include: stage-a/membership-block-2.txt from ^CLAUDE TREE BY SLICE$ -->
```text
CLAUDE TREE BY SLICE
8 paths 334 lines ('distribution', '.claude/agents', ('doctrine-skills',), 'non-rest', 'doctrine')
30 paths 8002 lines ('distribution', '.claude/rules', ('doctrine-rules',), 'non-rest', 'doctrine')
44 paths 12400 lines ('distribution', '.claude/skills', ('doctrine-skills',), 'non-rest', 'doctrine')
DOCTRINE BY SLICE
254 paths 38598 lines ('distribution', ('doctrine-reference',), 'rest')
52 paths 12734 lines ('distribution', ('doctrine-skills',), 'non-rest')
36 paths 11414 lines ('distribution', ('doctrine-rules',), 'non-rest')
```

**The other neighbours the skills name** (§ 2's `hits()` read, `stage-a/neighbours.out`): `docs/council-*` is T39's, the area's `rest`, and `research/` is T46's:

<!-- include: stage-a/neighbours.out -->
```text
9 ('docs/council-*', ('doctrine-reference',), 'rest', 'doctrine')
717 ('research/', ('records',), 'non-rest', 'records')
```

### Both totals, at the dispatch tip

§ 2's dispatch-tip lines (`stage-a/dispatch-tip.sh`, run at 02:44:38) print the tree the lane carries. The script's exit is its last `grep -c ''`, which printed `0` (rc 1).

<!-- include: stage-a/dispatch-tip.out -->
```text
dispatch tip: paths 52 lines 12783
 3 files changed, 50 insertions(+), 1 deletion(-)
 3 files changed, 50 insertions(+), 1 deletion(-)
18	1	.claude/skills/code-auditor/references/templates.md
25	0	.claude/skills/council/IMPORTED-FROM.md
7	0	.claude/skills/mini-retro/references/scoped-audit.md
0
0
```

- **The two totals:** the block measures **12,734** lines at the P1 hash (and at the inventory's head `eb4763e3cc`). The dispatch tip carries **12,783** (`dispatch tip: paths 52 lines 12783`).
- **Why they differ:** the coordinator's branch moved three of the 52 after the inventory. The shortstat is the same against `2174265e9c` and against `8ebaf8daad`, and the numstat gives `18 1`, `25 0` and `7 0` for the three files.
- **No settings path is tracked** (ruling (g)): the last two lines are `0` tracked paths under `.claude/` matching *settings* and `0` commits in all history touching `.claude/settings*`. The title keeps the order's word.

### The drift: the three files and their five commits

The three files' lines at the P1 tip, at `next` and at the dispatch tip (`stage-a/stage-a-extra.out`):

<!-- include: stage-a/stage-a-extra.out from ^-- the three moved files to scoped-audit\.md -->
```text
-- the three moved files, lines at the P1 tip, at next and at HEAD (grep -c ''):
.claude/skills/code-auditor/references/templates.md 331 331 348
.claude/skills/council/IMPORTED-FROM.md 102 102 127
.claude/skills/mini-retro/references/scoped-audit.md 709 709 716
```

The commits on the three since the P1 tip (`git log 2174265e9c..HEAD`, the runs' L-01 chunk, subjects through the read mask `M`):

<!-- include: stage-a/runs.out match ^[0-9a-f]{10} 2026-1 -->
```text
161effca8f 2026-10-25 skills: scoped-audit check 7 asks whether a fix's positive exercised the job the fix could break (#660)
18747fbc52 2026-10-24 Merge fix/m6-810-lint-local-epic: the lint accepts Local depth at epic tier under D-WORKFLOW-184 (#810)
fa6bcdafa8 2026-10-24 lint-audit-artifacts: accept Local depth at epic tier under D-WORKFLOW-184 (#810)
0ceb2994c5 2026-10-22 council: add explicit Argon audit route and refusal diagnostics
033eb7ed23 2026-10-22 council: stop retrying explicitly filtered responses
```

- **`161effca8f`'s hunk** is item 5 of Check 7, as its subject says. It lands at `@@ -502,6 +502,13 @@`, adding `+5.` after Check 7's heading at `:456` and before Check 8's at `:524`:

<!-- include: stage-a/runs.out match ^(21|25|456|524): -->
```text
21:@@ -502,6 +502,13 @@ justification.
25:+5. For each fix that landed with a positive, ask: **did the positive
456:### Check 7 — Harness self-coverage scan
524:### Check 8 — Documentation & glossary freshness
```

- **The other two files' changes:** `templates.md`'s is #810's Local epic-tier example (`fa6bcdafa8`, merged at `18747fbc52`). `IMPORTED-FROM.md`'s are the two October 22 sections (`0ceb2994c5`, `033eb7ed23`). Which commit touched which file comes from `stage-a/moved-commits.sh`:

<!-- include: stage-a/moved-commits.out -->
```text
02:53:15
161effca8f
.claude/skills/mini-retro/references/scoped-audit.md
18747fbc52
fa6bcdafa8
.claude/skills/code-auditor/references/templates.md
0ceb2994c5
.claude/skills/council/IMPORTED-FROM.md
033eb7ed23
.claude/skills/council/IMPORTED-FROM.md
--- the merge 18747fbc52 against its first parent, on the three:
 .claude/skills/code-auditor/references/templates.md | 19 ++++++++++++++++++-
 1 file changed, 18 insertions(+), 1 deletion(-)
```

- **Who reads these in which hunk:** `git log -p 2174265e9c..HEAD -- <the three>`, under L-01 at stage B. `templates.md` and `scoped-audit.md` are read under the skills they belong to, which are the skills this slice is judged by (R1 § 7).

## § Read order

**The two clusters** (R1 § 6, read again here):
- **By path,** `council`, `council-research` and the eight agents name each other, and the six workflow skills name only themselves.
- **By name,** `begin-delivery` <-> `futro` <-> `mini-retro` <-> `code-auditor` is one cluster, joined to the council family by a handful of lines. `stage-b/tables/q6.md`'s *Other skills naming it* counts each skill's name in the other skills' files: `code-auditor` 38, `council` 85, `futro` 27, `mini-retro` 23, `begin-delivery` 22.
- **The writing pair** names only itself and `es-player-text.md`.

**The order the reading took** (ruling (j); open item 1 answered by the dispatch and the errata), each step after the reader's pass for that skill, every time from the export at the dispatch tip:
1. `code-auditor` -- `SKILL.md`, `phases.md`, `templates.md`, `anti-patterns.md`, `review-levels.md`, whole (`stage-b/notes-code-auditor.md`, `checks-code-auditor.*`).
2. `mini-retro` -- `SKILL.md`, `scoped-audit.md`, `template.md`, whole (`notes-mini-retro.md`, `checks-mini-retro.*`).
3. `futro` -- `SKILL.md`, `techniques.md`, `template.md`, `blindspot-register.md`, whole (`notes-futro.md`, `checks-futro.*`).
4. `session-resume`, then `session-stash`, whole (`notes-sessions.md`, `checks-sessions.*`).
5. `begin-delivery`, whole (`notes-begin-delivery.md`).
6. The writing pair: `developer-relations`, then `release-notes`, whole (`notes-writing-pair.md`, `checks-writing-pair*`).
7. The council family, read and never edited (`notes-council-family.md`, `council-lines.*`, `checks-council.*`):
   - `council/SKILL.md`, `IMPORTED-FROM.md`, `COUNCIL-BUNDLE.md` and `member-roster.md` whole;
   - `council-research/SKILL.md` whole;
   - the eight agents (`claude` whole, the four other active seats and `mistral` as their diffs against it, `deepseek` and `grok` whole);
   - the other references at the lines the leads and the readers name.

**The rules the work touches, read this session at `3a9b0aec81`:**
- `adversarial-council.md` (`:36-38`, `:49-58`, `:77-78`), `release-candidates.md` (`:71-76`), `device-builds.md` (`:596-597`, and its changes since the session's start);
- `ceremonies.md` (the marker table), `learning-capture.md` (§ 3, § 4), `issue-tracking.md`, `worktrees.md`, `engineering-practices.md` (its changes since the session's start: `rc=$?` on its own line, the widened mask, a count as a claim about one tree, a stub checked against the unfixed text);
- `working-principles.md` § Enforcement depth, `instruction-files.md` (its changes), `decision-register.md`, `upgrade-and-install.md` § Every fix answers what was already written, `bugs-are-agent-first.md`, `vm-first.md`, `time-to-play.md`;
- `council-substrate-integrity.md`, the one rule not loaded at the session's start, read by `git show` at the lines L-50 needs.

The rules outside the 9 changed files equal the session's loaded copies byte for byte (`git diff --quiet 52e6794ba7 3a9b0aec81`, the list in `00`).

**The rest of § 3's floor** (`stage-b/floor-reads.*`):
- the blindspot register at `:4`, `:10`, `:18`, `:30`, `:36`, `:37`, `:915`, `:1089`, `:1134`, `:1215`;
- the friction log at its ten lines;
- T4's `05-punch-list.md:568` (`deferred:#685`);
- T4's `04-analysis.md:705-892` (the table of every path a rule or register line cites: `15` rows name the 52);
- the doctrine futro's T38 kickoff addendum (`:472` on);
- #314 `:14`, #287 `:16` and L-27's checkboxes (`checks-writing-pair.out`).

## § The reader's pass

Eleven no-context read-only subagents (Explore type), one per skill and one for the eight agents. Each was given only its directory of the export and asked what it would have had to ask (brief § 5 rule 5). Their reports are `stage-b/reader-*.md`, verbatim: leads, never evidence. Each item that became a row of `02` was re-read by the lane at its lines first; an item that did not is one the lane read and found answered by the text or the brief.

| Skill | Reader's file | Items | Its one-sentence reading | The items that became leads |
| --- | --- | ---: | --- | --- |
| `code-auditor` | `reader-code-auditor.md` | 15 | verifies, with a second model, that work claimed complete meets its criteria and rules | 1 (L-02), 2, 3 (L-85), 4 (L-59), 5 (L-52), 6 (L-15), 8 (L-03), 9 (L-57), 10 (L-56), 11 (L-15), 14 (L-62), 15 (L-12) |
| `mini-retro` | `reader-mini-retro.md` | 15 | turns a finished phase's lessons into edits, issues or comments | 1 (L-81), 2 (L-63), 4, 5, 6 (L-81), 7 (L-55), 9 (L-15), 10 (L-10), 11 (L-81), 15 (L-64, L-65) |
| `futro` | `reader-futro.md` | 15 | finds a plan's traps before work starts | 1 (L-67), 2 (L-67), 3 (L-15, L-58), 4 (L-82), 5 (L-75), 6 (L-82), 9 (L-82), 10 (L-15), 14 (L-82) |
| `session-resume` | `reader-session-resume.md` | 12 | decides which saved state is the handoff and how far to trust it | 4 (L-09), 5, 6, 7 (L-84), 10, 11 (L-84) |
| `session-stash` | `reader-session-stash.md` | 12 | saves the session's state so a fresh agent can resume | 1 (L-68), 3 (L-19), 4 (L-69), 5 (L-84), 8 (L-84) |
| `begin-delivery` | `reader-begin-delivery.md` | 15 | decides whether an Execution Epic may start and what it starts with | 3, 4, 6 (L-63), 8, 11 (L-83), 13 (L-12, L-83), 14 (L-15, L-58) |
| `developer-relations` | `reader-developer-relations.md` | 12 | sets how a rocknix.org page reads, in the site's voice | 8, 9, 12 (L-79) |
| `release-notes` | `reader-release-notes.md` | 12 | sets the shape of a release note and a PR description | 1 (L-70), 2, 3 (L-80), 6, 9 (L-80) |
| `council` | `reader-council.md` | 15 | picks one plan of five through analysis, review, revision and votes | 1 (L-38), 2, 3, 7, 10, 15 (L-77); 4, 5 (L-38, L-39); 14 (L-76) |
| `council-research` | `reader-council-research.md` | 15 | runs research across five models before a council deliberates | 1 (L-76), 3 (L-38), 14 (L-30, L-31) |
| the agents | `reader-agents.md` | 15 | pin one provider model to each of five seats; three are historical | 1 (L-40), 3 (L-41), 10 (L-41), 15 (L-38) |

The readers' first answers -- what each skill decides and when to open it -- all match the skills' own descriptions. The stumbles are where the bodies are not as clear as the descriptions. Four of the eleven asked which repository they were in (`code-auditor` 6, `mini-retro` 9, `futro` 10, `begin-delivery` 14), the strongest single signal for L-15.

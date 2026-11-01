export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t38; X=':(exclude).claude/rules/'
M='s/((token|key|pass(w[a-z]*)?|psk|user|login|apikey) *[=:] *)[^ "]*/\1***/Ig; s/(--(token|key|pass(w[a-z]*)?|psk|user)[= ]+)[^ ]+/\1***/Ig'   # the read mask, engineering-practices.md's two substitutions widened as T37's was
# the read tree, once (expect 52 -- R1 C05; R2 C1; R3 C1)
mkdir -p "$T/export" && git archive HEAD .claude/agents .claude/skills | tar -x -C "$T/export"; find "$T/export" -type f | $G -c ''
# L-01: the moved files' commits and the scoped-audit hunk (expect the five commits of § 2 -- R1 C09, proof Part 1; then `@@ -502,6 +502,13 @@` and the added `+5. For each fix that landed with a positive, ...`, and the headings `456:### Check 7` and `524:### Check 8`: item 5 of Check 7 -- v2 read at 2f42ff5ddf)
git log --format='%h %ad %s' --date=short 2174265e9c..HEAD -- .claude/skills/code-auditor/references/templates.md .claude/skills/council/IMPORTED-FROM.md .claude/skills/mini-retro/references/scoped-audit.md | sed -E "$M"
git show 161effca8f -- .claude/skills/mini-retro/references/scoped-audit.md | $G -n -E '^@@|^\+[0-9]+\. '
git show HEAD:.claude/skills/mini-retro/references/scoped-audit.md | $G -n -E '^### Check (7|8)'
# front matter (expect `FRONT-MATTER 18 NONE 34` -- R3 C17: the 10 SKILL.md and the 8 agents carry it)
find "$T/export" -type f -print0 | python3 -I -c 'import sys; fs=[f for f in sys.stdin.buffer.read().split(b"\0") if f]; n=sum(1 for f in fs if open(f,"rb").readline().rstrip(b"\r\n")==b"---"); print("FRONT-MATTER", n, "NONE", len(fs)-n)'
# L-02: the evidence floor (expect 157 the heading, 159 `Three hard rules`, then 161, 166, 179, 186 and 191, the last two numbered 4 and 3 -- R1 C17; R4 item 30)
git show HEAD:.claude/skills/code-auditor/SKILL.md | $G -n -E '^## Evidence floor|Three hard rules|^[0-9]+\. \*\*' | awk -F: '$1>=155 && $1<=200'
# L-03, L-04 (expect `420:` and `711:` -- R4 C24, C26)
git show HEAD:.claude/skills/code-auditor/SKILL.md | $G -n -E 'Twelve recorded|rocknix\.worktrees'
# L-05: durations used as estimates, by the widened pattern (`~N min`, `~N hr`, `~N–N hr`, `~1 day`, `N minutes`, `N seconds to N minutes`; proof correction 2) over the eight fork-adapted skills: expect 10 lines -- begin-delivery/SKILL.md :398, :429; code-auditor/SKILL.md :3, :135; mini-retro/SKILL.md :67 to :70; mini-retro/references/scoped-audit.md :69, :184 -- then `10` (v2 read at 2f42ff5ddf; the same 10 over all 52; version 1's narrower pattern printed 7); after stage E the same two lines print no line and `0` (L-05)
P5='~ ?[0-9]+((-|–)[0-9]+)? ?(min|mins|minute|minutes|hr|hrs|hour|hours|h|day|days)([^a-z]|$)|[0-9]+ (seconds|minutes)([^a-z]|$)'
S8=(.claude/skills/begin-delivery .claude/skills/code-auditor .claude/skills/futro .claude/skills/mini-retro .claude/skills/session-resume .claude/skills/session-stash .claude/skills/developer-relations .claude/skills/release-notes)
git grep -n -E "$P5" HEAD -- "${S8[@]}" | cut -d: -f2,3; git grep -n -E "$P5" HEAD -- "${S8[@]}" | $G -c ''
# L-06, L-07, L-08, L-20: what the skills do not name (expect no line from either, the second's rc 1 -- R2 C9, C19, C24; R4 C23, C26)
git grep -n -E 'audit-completion|\.held\.json|1308' HEAD -- .claude/skills/code-auditor
git grep -c -E 'docs/futros|docs/retros/|ceremony-check' HEAD -- .claude/skills/futro .claude/skills/mini-retro .claude/skills/begin-delivery
# L-09 (expect 5 lines in 2 files by `state-main` -- R3 C21)
git grep -n 'saved-session-state-main' HEAD -- .claude/skills
# L-10, L-11, L-13: the blocks and sentences a reader would act on (expect the stash and vitest lines; `uploads`; `{owner}/{repo}` -- R2 L-08, L-09, L-16)
git show HEAD:.claude/skills/mini-retro/references/scoped-audit.md | sed -n '340,365p' | $G -n -E 'git stash|npx vitest'
git show HEAD:.claude/skills/release-notes/SKILL.md | sed -n '19,20p'; git show HEAD:.claude/rules/device-builds.md | sed -n '596,597p'
git show HEAD:.claude/skills/futro/SKILL.md | $G -n -F '{owner}/{repo}'
# L-23: the two texts, quoted whole into 02 (expect release-candidates.md:74-76 and review-levels.md:10 as R2 L-06 quotes them, and adversarial-council.md's section :49-58 with the sentence at :51-52 -- proof correction 8)
git show HEAD:.claude/rules/release-candidates.md | sed -n '71,76p'; git show HEAD:.claude/skills/code-auditor/references/review-levels.md | sed -n '9,12p'; git show HEAD:.claude/rules/adversarial-council.md | sed -n '49,58p'
# the brief's grep (expect `80` -- R1 C19)
git grep -n -o -E '\.claude/(skills|agents)/[A-Za-z0-9_./-]+' HEAD -- .claude/ "$X" | $G -c ''
# L-22 (expect `19`, `1`, and no line -- R1 C13, C19)
git grep -n 'begin-exploration' HEAD -- .claude/ "$X" | $G -c ''; git grep -n 'begin-exploration' HEAD -- .claude/rules | $G -c ''; git ls-tree -d HEAD .claude/skills/begin-exploration
# L-30, L-31, L-47: the council family's absences (expect no line; a non-zero rc; `0` -- R2 L-01, L-02, L-03)
git ls-tree -r --name-only HEAD scripts | $G lint-council-research
git cat-file -e HEAD:.claude/agents/researcher.agent.md; rc=$?
echo "researcher agent rc=$rc"
git ls-tree --name-only HEAD research/council-research/ | $G -c ''
# #1044's loop over the slice, its criterion's pattern (R4 item 33): every MISSING line recorded -- six at 2f42ff5ddf (proof Part 2): the pattern cannot reach scripts/__tests__/, so the line after it reads the three test paths L-30 names (their absence is L-30's open mark)
git grep -h -o -E 'scripts/[a-z-]+\.ts' HEAD -- .claude/skills .claude/agents | sort -u | while read -r p; do git cat-file -e "HEAD:$p" 2>/dev/null || echo "MISSING $p"; done
git grep -h -o -E 'scripts/__tests__/[A-Za-z0-9_.-]+' HEAD -- .claude/skills .claude/agents | sort -u | while read -r p; do git cat-file -e "HEAD:$p" 2>/dev/null && echo "PRESENT $p" || echo "MISSING $p"; done
# L-34: the bundle's sums against the tree (expect `BUNDLE match=52 diff=39 absent=3` -- R3 C15; R1 C12)
git show HEAD:.claude/skills/council/COUNCIL-BUNDLE.SHA256SUMS | python3 -I -c 'import sys,subprocess,hashlib
m=d=a=0
for ln in sys.stdin.read().splitlines():
    if not ln.strip(): continue
    h,p=ln.split(None,1); p=p.lstrip("*")
    r=subprocess.run(["git","show","HEAD:"+p],capture_output=True)
    if r.returncode: a+=1
    elif hashlib.sha256(r.stdout).hexdigest()==h: m+=1
    else: d+=1
print("BUNDLE match=%d diff=%d absent=%d" % (m,d,a))'
# the pins, recomputed offline, never by running scripts/verify-pins.ts (expect eight MATCH lines and `pins MATCH 8 of 8` -- R3 C15, proof Part 4, v2 read at 2f42ff5ddf): the file's top level is `['created_at', 'note', 'pins', 'schema_version']` and an entry's `['repin_reason', 'repinned_at', 'repinned_by', 'sha']` (proof Part 4; v2 read), so each pin is `d["pins"][path]["sha"]`, the sha256 of the file's bytes; 8 of the 30 pins are under .claude/
git show HEAD:verifier-pins.json | python3 -I -c 'import sys,json,hashlib,subprocess
d=json.load(sys.stdin)["pins"]; ps=sorted(p for p in d if p.startswith(".claude/")); m=0
for p in ps:
    b=subprocess.run(["git","show","HEAD:"+p],capture_output=True,check=True).stdout
    ok=hashlib.sha256(b).hexdigest()==d[p]["sha"]; m+=ok; print("MATCH" if ok else "DIFF", p)
print("pins MATCH %d of %d" % (m,len(ps)))'
# the stale names (R3 C21's terms, case-insensitive; expect its table: rubber[- ]duck 0/0, copilot 42/12, \.github/instructions 27/17, \.github/prompts 3/3, test/qa-integration 0/0, opus 4.8 6/2, gpt-5[.]5 2/1, gpt-5[.]6 5/3, mistral 50/13, trio 20/9, rasteratops 5/4, state-main 5/2, scaffold 83/26 -- lines/files)
for t in 'rubber[- ]duck' 'copilot' '\.github/instructions' '\.github/prompts' 'test/qa-integration' 'opus[- ]4[.]8|claude-opus-4' 'gpt-5[.]5' 'gpt-5[.]6' 'mistral' 'trio' 'rasteratops' 'state-main' 'scaffold'; do printf '%s: %s lines in %s files\n' "$t" "$(git grep -h -i -E -e "$t" HEAD -- .claude/ "$X" | $G -c '')" "$(git grep -l -i -E -e "$t" HEAD -- .claude/ "$X" | $G -c '')"; done
# the IDs the 52 cite (expect 16, each resolving -- R2 C24; R2's loop is not printed, so the lane's look-up of each in the decided and open tables is recorded beside it)
git grep -h -o -E 'D-[A-Z]+-[0-9]+' HEAD -- .claude/ "$X" | sort -u | $G -c ''
# the roster's rows in the rule (expect the Claude and GPT rows of adversarial-council.md:77-78 -- R2 § 4; R3 C18)
git show HEAD:.claude/rules/adversarial-council.md | sed -n '75,80p'
# the contract read: the lint's constants against the templates (R3 § 2.6), parsed from the lint at the tip with Python's ast, never retyped; expect `28:REQUIRED = [...` and `30:ANALYSIS_SECTIONS = [...`, then `REQUIRED 5 missing in templates.md: ['01-research-notes.md']` and `ANALYSIS_SECTIONS 5 missing in templates.md: ['Acceptance-criteria scorecard', 'Coverage boundary', 'Quality self-check']` by exact substring (v2 read at 2f42ff5ddf; proof Part 4); the case rule is § 3 item 5's open mark
$G -n -E '^(REQUIRED|ANALYSIS_SECTIONS) ' tools/lint-audit-artifacts | cut -c1-40
git show HEAD:tools/lint-audit-artifacts | python3 -I -c 'import sys,ast,subprocess
src=sys.stdin.read(); t=subprocess.run(["git","show","HEAD:.claude/skills/code-auditor/references/templates.md"],capture_output=True,check=True).stdout.decode()
c={n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(src).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ("REQUIRED","ANALYSIS_SECTIONS")}
for k in ("REQUIRED","ANALYSIS_SECTIONS"): print(k, len(c[k]), "missing in templates.md:", [v for v in c[k] if v not in t])'
# the text checks over the 52, in the hooks' own form (expect the compile rc at most 1, the planted positive `1`, then `0` files; NON-ASCII 48 files; forbidden-terms rc=0 twice -- R3 C24)
( P=$(mktemp "$T/tmp/sp.XXXXXX"); git show HEAD:.githooks/secret-patterns > "$P"; SECRET_PATTERNS=''; . "$P"; rm -f "${P:?}"
  printf '' | $G -E -e "$SECRET_PATTERNS" >/dev/null 2>&1; rc=$?
  echo "secret regex compile rc=$rc"
  printf -- '-----BEGIN %s-----\n' "$(printf '%s' 'OPENSSH PRIVATE KEY')" | $G -c -E -e "$SECRET_PATTERNS"
  $G -r -c -E -e "$SECRET_PATTERNS" "$T/export" | $G -v -c ':0$' )
$G -r -c -P '[^\x00-\x7F]' "$T/export" | $G -v -c ':0$'
find "$T/export" -type f -print0 | sort -z | xargs -0 cat > "$T/tmp/the52.txt"
tools/forbidden-terms-check --stdin < "$T/tmp/the52.txt"; rc=$?
echo "forbidden-terms over the 52 rc=$rc"
tools/forbidden-terms-check --stdin < /dev/null; rc=$?
echo "forbidden-terms over empty input rc=$rc"   # rc=0 too (R3 C24): not evidence until the positive below fires
printf 'a zzqplantedzz line\n' > "$T/tmp/planted.txt"
FORBIDDEN_PATTERNS='zzqplantedzz' tools/forbidden-terms-check --stdin < "$T/tmp/planted.txt"; rc=$?
echo "forbidden-terms, a planted positive, rc=$rc"   # rc=1 and `forbidden-terms-check: 1 line(s) on stdin carry a listed word` (proof Part 4; v2 read): with FORBIDDEN_PATTERNS set the tool never reads the list (its :14)
.githooks/hooks-test > "$T/tmp/hooks-test.out" 2>&1; rc=$?
echo "hooks-test rc=$rc"; tail -n 1 "$T/tmp/hooks-test.out"   # neither this, `tools/box-check` below nor stage A's `tools/ceremony-check` was run by the proof `[unverified]`: the lines that print at stage A are the record
tools/box-check > "$T/tmp/box-check.out" 2>&1; rc=$?
echo "box-check rc=$rc"; tail -n 1 "$T/tmp/box-check.out"     # once here, once at hand-back, and --issue N once per issue this lane files (T4's § 5)

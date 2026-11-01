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

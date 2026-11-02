import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
SID = "doctrine-reference"
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
def gm(comp,p,t="distribution"):
    inc,exc=comp
    return any(r.match(p) for r in inc.get(t,())) and not any(r.match(p) for r in exc.get(t,()))
doc=json.load(open("docs/reviews/slices.json"))
sl=[]
for s in doc["slices"]:
    sels=s.get("select",{}); sels=sels if isinstance(sels,list) else [sels]
    comp=[]
    for sel in sels:
        comp.append((set(sel.get("areas",[s["area"]])), compile_globs(sel["globs"]) if sel.get("globs") else None,
                     set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")), set(sel["tier"]) if sel.get("tier") else None))
    sl.append((s,comp))
ar=json.load(open("docs/reviews/areas.json")); ar=ar["areas"] if isinstance(ar,dict) else ar
DOCA=compile_globs([a for a in ar if a["area"]=="doctrine"][0]["globs"])
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
    return gm(comp,row["path"],row["tree"])
def hits(row):
    non=[s["id"] for s,c in sl if any(not rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)]
    if non: return non,"non-rest"
    return [s["id"] for s,c in sl if any(rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)],"rest"
def nonrest_doctrine(p):
    return [s["id"] for s,c in sl if any(not rest and "doctrine" in a and cm is not None and gm(cm,p) for a,cm,r,rest,t in c)]
kof={s["id"]:s["k"] for s,_ in sl}
mine=sorted((r for r in rows if r["tree"]=="distribution" and hits(r)[0]==[SID]), key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine),"reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)))
print("lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"),"upstream-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="upstream-carried"))
rd=[r for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"]
print("read lines:",sum((r["lines"] or 0) for r in rd),"of which fork-own:",sum((r["lines"] or 0) for r in rd if r["tier"]=="fork-own"),"read rows:",[(r["path"],r["language"],r["lines"]) for r in rd])
print("overlap:",sum(1 for r in mine if r["overlap"]),"last_upstream_commit set:",sum(1 for r in mine if r["last_upstream_commit"]),"binary (lines None):",[r["path"] for r in mine if r["lines"] is None])
def grp(p):
    q=p.split("/")
    if len(q)==1: return p
    if q[0]=="docs":
        if len(q)==2: return "docs/*"
        if q[1]=="reviews" and len(q)>3: return "docs/reviews/"+q[2]+"/"
        return "docs/"+q[1]+"/"
    return q[0]+"/"
print("GROUPS (group: paths lines | fork-own paths lines | upstream-carried paths lines)")
g=collections.defaultdict(lambda:[0,0,0,0,0,0])
for r in mine:
    x=g[grp(r["path"])]; n=r["lines"] or 0; x[0]+=1; x[1]+=n
    if r["tier"]=="fork-own": x[2]+=1; x[3]+=n
    else: x[4]+=1; x[5]+=n
for k in sorted(g): print("  %-26s %4d %6d | %4d %6d | %4d %6d" % ((k,)+tuple(g[k])))
print("GROUPS TOTAL", len(mine), sum(v[1] for v in g.values()), "groups", len(g))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("TREE-SIDE (doctrine area by areas.json, less the doctrine non-rest slices' globs)")
for tf in sys.argv[2:]:
    ps=[l.strip() for l in open(tf) if l.strip()]
    der=sorted(p for p in ps if gm(DOCA,p) and not nonrest_doctrine(p))
    print(tf,"derived:",len(der),"equal to mine:",der==got,"only-derived:",sorted(set(der)-set(got)),"only-mine:",sorted(set(got)-set(der)))
print("CLAIMS")
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
named=["README.md","NAMING.md","CLAUDE.md","AGENTS.md","docs/decision-register.md","docs/blindspot-register.md","docs/friction-log.md","docs/reviews/inventory.json","docs/reviews/order.md","docs/reviews/plan-for-the-plan.md","docs/es-menu-map.md","docs/vm-qa-log.md","docs/releases/catalog.md","docs/work-logs/INDEX.md","docs/futros/2026-10-24-m6-doctrine.md",".github/sessions/saved-session-state-next.md",".claude/skills/futro/SKILL.md"]
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p,"in-T39" if p in got else "not-in-T39",kind,[(x,kof[x]) for x in h],"tier",r["tier"],"lines",r["lines"],"lang",r["language"],"area",r["area"])
print("DOCS TREE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="distribution" and r["path"].startswith("docs/"):
        h,kind=hits(r); q=r["path"].split("/")
        k=("docs/*" if len(q)==2 else "docs/"+q[1]+"/",tuple(h),r["area"])
        cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items()): print(v,"paths",ln[k],"lines",k)
print("DOCTRINE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["area"]=="doctrine":
        h,kind=hits(r); k=(r["tree"],tuple(h),kind); cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)

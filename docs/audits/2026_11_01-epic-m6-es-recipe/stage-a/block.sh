mkdir -p .qa-scratch/t37
cat > .qa-scratch/t37/membership.py <<'PYEOF'
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
    if h==["es-recipe"]: mine.append(r)
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
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("CLAIMS")
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
tree=[l.strip() for l in open(sys.argv[2]) if l.strip()]
named=tree+["projects/ROCKNIX/packages/virtual/es-themes/package.mk","projects/ROCKNIX/packages/virtual/image/package.mk","docs/qa-logs/2026-10-14-screenscraper-provisioning/attempt02/inputs/baseline/package.mk","docs/qa-logs/2026-10-14-screenscraper-provisioning/attempt02/inputs/candidate/package.mk","tools/pkgcheck","tools/es-menu-map-check"]
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY; globs:",globhits(p)); continue
    h,kind=hits(r); print(p, "in-T37" if p in got else "not-in-T37", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"lang",r["language"],"area",r["area"])
print("DEPS")
deps=["toolchain","boost","SDL2","freetype","curl","freeimage","bash","rapidjson","SDL2_mixer","fping","p7zip","alsa","vlc","drm_tool","poppler","pugixml","noto-sans-cjk","zstd","Python3","SDL2_image","SDL2_ttf"]
for d in deps:
    rx=re.compile(r"(?:^|/)packages/(?:.*/)?"+re.escape(d)+r"/package\.mk\Z")
    found=sorted(p for p in byp if rx.search(p))
    if not found: print(d,"NO RECIPE IN INVENTORY")
    for p in found:
        h,kind=hits(byp[p]); print(d,p,kind,[(x,kof[x]) for x in h],"tier",byp[p]["tier"])
print("RECIPE TREES BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="distribution" and (r["path"].startswith("packages/") or r["path"].startswith("projects/ROCKNIX/packages/")):
        k=("packages/" if r["path"].startswith("packages/") else "projects/ROCKNIX/packages/",)+tuple(hits(r)[0])+(hits(r)[1],)
        cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:(kv[0][0],-kv[1])): print(v,"paths",ln[k],"lines",k)
PYEOF
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; MB=c445081a59
git -C "$W" ls-tree -r --name-only "$P1" -- projects/ROCKNIX/packages/ui/ > .qa-scratch/t37/tree.txt
python3 -I .qa-scratch/t37/membership.py /dev/null .qa-scratch/t37/tree.txt > .qa-scratch/t37/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="distribution" {print $2}' .qa-scratch/t37/block-1.txt > .qa-scratch/t37/paths.txt
wc -l .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt
python3 -I .qa-scratch/t37/membership.py .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt > .qa-scratch/t37/block-2.txt
/usr/bin/grep -E '^(distribution |mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t37/block-2.txt
IH=$(sed -n 's/^distribution head: //p' .qa-scratch/t37/block-2.txt)
git -C "$W" ls-tree -r --name-only "$IH" -- projects/ROCKNIX/packages/ui/ | diff - .qa-scratch/t37/paths.txt && echo "ls-tree at the inventory's head = paths.txt"
diff .qa-scratch/t37/paths.txt .qa-scratch/t37/tree.txt; echo "paths.txt against ls-tree at $P1: diff rc=$?"
for p in $(cat .qa-scratch/t37/tree.txt); do git -C "$W" show "$P1:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t37/tree.txt); do git -C "$W" show "$P1:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, every path at the P1 hash:", s}'
for p in $(cat .qa-scratch/t37/paths.txt); do git -C "$W" show "$IH:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c, the inventory paths at its head:", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t37/tree.txt | wc -l
git -C "$W" diff --shortstat "$MB" "$P1" -- projects/ROCKNIX/packages/ui/
git -C "$W" diff --shortstat "$IH" "$P1" -- projects/ROCKNIX/packages/ui/

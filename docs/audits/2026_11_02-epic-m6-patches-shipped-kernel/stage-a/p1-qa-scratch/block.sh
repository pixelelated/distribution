mkdir -p .qa-scratch/t41
cat > .qa-scratch/t41/membership.py <<'PYEOF'
import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
SID = "patches-shipped-kernel"
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
PCA=compile_globs([a for a in ar if a["area"]=="patches-and-configs"][0]["globs"])
ME=[s for s,_ in sl if s["id"]==SID][0]; MYG=compile_globs(ME["select"]["globs"]); MYR=set(ME["select"]["reach"])
POS=compile_globs([g for g in ME["select"]["globs"] if not g.startswith("!")])
inv=json.load(open("docs/reviews/inventory.json"))
hd=inv["header"]["distribution"]
print("distribution head:",hd["head"]); print("distribution merge_base:",hd["merge_base"]); print("distribution upstream:",hd["upstream"],hd["upstream_head"])
print("header keys:",sorted(inv["header"].keys())); print("shipped_devices:",inv["header"].get("shipped_devices"),"test_devices:",inv["header"].get("test_devices"))
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
kof={s["id"]:s["k"] for s,_ in sl}
mine=sorted((r for r in rows if r["tree"]=="distribution" and hits(r)[0]==[SID]), key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine),"reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)))
print("lang:",dict(c(r["language"] for r in mine)),"area:",dict(c(r["area"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"),"upstream-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="upstream-carried"),"vendor-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="vendor-carried"))
rd=[r for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"]
print("read lines:",sum((r["lines"] or 0) for r in rd),"of which fork-own:",sum((r["lines"] or 0) for r in rd if r["tier"]=="fork-own"),"read rows:",[(r["path"],r["language"],r["lines"]) for r in rd])
print("overlap:",sum(1 for r in mine if r["overlap"]),"last_upstream_commit set:",sum(1 for r in mine if r["last_upstream_commit"]),"binary (lines None):",[r["path"] for r in mine if r["lines"] is None])
print("fork-own rows:",[(r["path"],r["lines"],r["last_fork_commit"]) for r in mine if r["tier"]=="fork-own"])
print("reachable_by:",dict(c(tuple(r["reachable_by"]) if isinstance(r["reachable_by"],list) else r["reachable_by"] for r in mine)))
print("buildable_by:",dict(c(tuple(r["buildable_by"]) if isinstance(r["buildable_by"],list) else r["buildable_by"] for r in mine)))
def kind(p):
    m=re.match(r"packages/linux/patches/([^/]+)/",p)
    if m: return "K1 packages/linux/patches/<dir>/", m.group(1)
    m=re.match(r"projects/ROCKNIX/packages/(linux[^/]*)/patches/([^/]+)/",p)
    if m: return "K2 projects/ROCKNIX/packages/%s/patches/<dir>/" % m.group(1), m.group(2)
    m=re.match(r"projects/ROCKNIX/devices/([^/]+)/patches/([^/]+)/",p)
    if m: return "K3 projects/ROCKNIX/devices/<DEVICE>/patches/%s/" % m.group(2), m.group(1)
    m=re.match(r"projects/ROCKNIX/devices/([^/]+)/linux/linux[^/]*\.conf\Z",p)
    if m: return "K4 projects/ROCKNIX/devices/<DEVICE>/linux/linux*.conf", m.group(1)
    return "K5 other", p.rsplit("/",1)[0]
print("GROUPS (kind | dir: paths lines | shipped test | fork-own upstream-carried vendor-carried)")
g=collections.defaultdict(lambda:[0,0,0,0,0,0,0])
for r in mine:
    x=g[kind(r["path"])]; n=r["lines"] or 0; x[0]+=1; x[1]+=n
    x[2 if r["reach"]=="shipped" else 3]+=1
    x[{"fork-own":4,"upstream-carried":5,"vendor-carried":6}[r["tier"]]]+=1
for k in sorted(g): print("  %-58s %-14s %4d %6d | %4d %4d | %3d %3d %3d" % ((k[0],k[1])+tuple(g[k])))
kt=collections.defaultdict(lambda:[0,0])
for k,v in g.items(): kt[k[0]][0]+=v[0]; kt[k[0]][1]+=v[1]
for k in sorted(kt): print("  KIND TOTAL %-50s %4d %6d" % (k,kt[k][0],kt[k][1]))
print("GROUPS TOTAL", len(mine), sum(v[1] for v in g.values()), "groups", len(g))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
print("TREE-SIDE (the slice's globs and the patches-and-configs area globs over ls-tree; reach from the inventory)")
for tf in sys.argv[2:]:
    ps=[l.strip() for l in open(tf) if l.strip()]
    mg=[p for p in ps if gm(MYG,p)]; ma=[p for p in mg if gm(PCA,p)]
    print(tf,"glob-matched:",len(mg),"also in area globs:",len(ma),"by inventory reach:",dict(c(byp[p]["reach"] if p in byp else "not-in-inventory" for p in ma)))
    der=sorted(p for p in ma if p in byp and byp[p]["reach"] in MYR)
    print(tf,"derived:",len(der),"equal to mine:",der==got,"only-derived:",sorted(set(der)-set(got)),"only-mine:",sorted(set(got)-set(der)))
print("CLAIMS (area rows under the slice's positive globs, not in the slice: owner, reach)")
cl=collections.Counter(); cll=collections.Counter()
for r in rows:
    if r["tree"]=="distribution" and r["area"]=="patches-and-configs" and gm(POS,r["path"]) and r["path"] not in got:
        h,kd=hits(r); k=(tuple((x,kof[x]) for x in h),kd,r["reach"]); cl[k]+=1; cll[k]+=(r["lines"] or 0)
        if r["path"].endswith(".conf"): print("  CONF",r["path"],"->",[(x,kof[x]) for x in h],kd,"reach",r["reach"],"tier",r["tier"],"lines",r["lines"],"last_fork_commit",r["last_fork_commit"])
for k,v in sorted(cl.items(), key = lambda kv:-kv[1]): print("  ",v,"paths",cll[k],"lines",k)
print("NAMED")
for p in ["packages/linux/package.mk","projects/ROCKNIX/packages/linux/package.mk","scripts/unpack","projects/ROCKNIX/options","projects/ROCKNIX/devices/H700/options","projects/ROCKNIX/devices/SM8550/options","projects/ROCKNIX/devices/GENERIC_X64/options","projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf","projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf","projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf"]:
    r=byp.get(p)
    if not r: print(" ",p,"NOT IN INVENTORY"); continue
    h,kd=hits(r); print(" ",p,"in-T41" if p in got else "not-in-T41",kd,[(x,kof[x]) for x in h],"tier",r["tier"],"reach",r["reach"],"lines",r["lines"],"lang",r["language"],"area",r["area"],"last_fork_commit",r["last_fork_commit"])
print("AREA BY SLICE (patches-and-configs: tree, owning slices, reach: paths lines)")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["area"]=="patches-and-configs":
        h,kd=hits(r); k=(r["tree"],tuple((x,kof[x]) for x in h),r["reach"]); cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:(kv[0][1],kv[0][2])): print(" ",v,"paths",ln[k],"lines",k)
st=collections.Counter(); stl=collections.Counter()
for r in rows:
    if r["area"]=="patches-and-configs":
        h,kd=hits(r); k=tuple((x,kof[x]) for x in h); st[k]+=1; stl[k]+=(r["lines"] or 0)
for k,v in sorted(st.items(), key = lambda kv:kv[0]): print("  SLICE TOTAL",v,"paths",stl[k],"lines",k)
PYEOF
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; MB=c445081a59
echo "MB type: $(git -C "$W" cat-file -t "$MB")"
IH=$(python3 -I -c 'import json; print(json.load(open("docs/reviews/inventory.json"))["header"]["distribution"]["head"])')
git -C "$W" ls-tree -r --name-only "$IH" > .qa-scratch/t41/tree-ih.txt
git -C "$W" ls-tree -r --name-only "$P1" > .qa-scratch/t41/tree-p1.txt
python3 -I .qa-scratch/t41/membership.py /dev/null > .qa-scratch/t41/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^TREE-SIDE/{p=0} p && $1=="distribution" {print $2}' .qa-scratch/t41/block-1.txt > .qa-scratch/t41/paths.txt
python3 -I .qa-scratch/t41/membership.py .qa-scratch/t41/paths.txt .qa-scratch/t41/tree-ih.txt .qa-scratch/t41/tree-p1.txt > .qa-scratch/t41/block-2.txt
awk -F'\t' '/^TSV$/{p=1;getline;for(i=1;i<=NF;i++)ix[$i]=i;next} /^TREE-SIDE/{p=0} p && $1=="distribution" && $ix["lines"]!="None" {print $ix["path"]}' .qa-scratch/t41/block-2.txt > .qa-scratch/t41/text.txt
wc -l .qa-scratch/t41/paths.txt .qa-scratch/t41/text.txt
awk '/^TSV$/{s=1} /^TREE-SIDE/{s=0} !s' .qa-scratch/t41/block-2.txt | cut -c1-600
while IFS= read -r p; do git -C "$W" show "$P1:$p" | wc -l; done < .qa-scratch/t41/text.txt | awk '{s+=$1} END {print "wc -l, the text rows at the P1 hash:", s}'
while IFS= read -r p; do git -C "$W" show "$P1:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t41/text.txt | awk '{s+=$1} END {print "grep -c, the text rows at the P1 hash:", s}'
while IFS= read -r p; do git -C "$W" show "$IH:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t41/text.txt | awk '{s+=$1} END {print "grep -c, the text rows at the inventory head:", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t41/paths.txt | wc -l | sed 's/^/present at the merge base: /'
while IFS= read -r p; do a=$(git -C "$W" rev-parse -q --verify "$P1:$p"); b=$(git -C "$W" rev-parse -q --verify "$MB:$p" 2>/dev/null); if [ -z "$b" ]; then echo "ADDED $p"; elif [ "$a" = "$b" ]; then echo "SAME $p"; else echo "CHANGED $p"; fi; done < .qa-scratch/t41/paths.txt > .qa-scratch/t41/mb-compare.txt
awk '{n[$1]++} END {for (k in n) print "blob vs merge base:", k, n[k]}' .qa-scratch/t41/mb-compare.txt | sort
/usr/bin/grep -v '^SAME' .qa-scratch/t41/mb-compare.txt
xargs -d '\n' -a .qa-scratch/t41/paths.txt git -C "$W" diff --shortstat "$MB" "$P1" -- | sed 's/^/MB..P1:/'
xargs -d '\n' -a .qa-scratch/t41/paths.txt git -C "$W" diff --shortstat "$IH" "$P1" -- | sed 's/^/IH..P1:/'
echo "(end)"

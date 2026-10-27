mkdir -p .qa-scratch/t33
cat > .qa-scratch/t33/membership.py <<'PYEOF'
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
kof={s["id"]:s["k"] for s,_ in sl}
mine=[]
for r in rows:
    if r["tree"]!="es": continue
    h,kind=hits(r)
    if h==["es-app-system"]: mine.append(r)
mine.sort(key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine), "reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)),"lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"))
print("read lines:",sum((r["lines"] or 0) for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("CLAIMS")
named=["es-app/src/ApiSystem.cpp","es-app/src/ApiSystem.h","es-app/src/FileData.cpp","es-app/src/FileData.h","es-app/src/SystemData.cpp","es-app/src/SystemData.h","es-app/src/CollectionSystemManager.cpp","es-app/src/CollectionSystemManager.h","es-app/src/Gamelist.cpp","es-app/src/Gamelist.h","es-app/src/MetaData.cpp","es-app/src/MetaData.h","es-app/src/FileFilterIndex.cpp","es-app/src/FileFilterIndex.h","es-app/src/Win32ApiSystem.cpp","es-app/src/CloudText.cpp","es-app/src/CloudText.h","es-app/src/OfflineAchievementsText.cpp","es-app/src/OfflineAchievementsText.h","es-app/src/NetworkThread.cpp","es-app/src/NetworkThread.h","es-app/CMakeLists.txt"]
byp={r["path"]:r for r in rows if r["tree"]=="es"}
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p, "in-T33" if p in got else "not-in-T33", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"area",r["area"])
print("ES-APP BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="es" and r["path"].startswith("es-app/"):
        h,kind=hits(r); cnt[(tuple(h),kind)]+=1; ln[(tuple(h),kind)]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
python3 -I .qa-scratch/t33/membership.py /dev/null > .qa-scratch/t33/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="es" {print $2}' .qa-scratch/t33/block-1.txt > .qa-scratch/t33/paths.txt
wc -l .qa-scratch/t33/paths.txt                                             # 77
python3 -I .qa-scratch/t33/membership.py .qa-scratch/t33/paths.txt > .qa-scratch/t33/block-2.txt
/usr/bin/grep -E '^(mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t33/block-2.txt
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
T=$(/usr/bin/grep -v -E '\.(aps|ico)$' .qa-scratch/t33/paths.txt); printf '%s\n' $T | wc -l           # 75 text paths
for p in $T; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l text", s}'            # 16272
for p in $T; do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c text", s}'   # 16276
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t33/paths.txt | wc -l   # 50: the upstream-carried 46 and the 4 modified
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t33/paths.txt | wc -l   # 50
git -C "$W" diff --shortstat "$MB" "$PIN" -- $(cat .qa-scratch/t33/paths.txt)           # 31 files changed, 2689 insertions(+), 7 deletions(-)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $(cat .qa-scratch/t33/paths.txt)     # the same line

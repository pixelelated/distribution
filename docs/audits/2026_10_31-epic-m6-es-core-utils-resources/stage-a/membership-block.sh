mkdir -p .qa-scratch/t36
cat > .qa-scratch/t36/membership.py <<'PYEOF'
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
    if h==["es-core-utils-resources"]: mine.append(r)
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
named=["es-core/src/utils/FileSystemUtil.cpp","es-core/src/utils/StringUtil.cpp","es-core/src/utils/Platform.cpp","es-core/src/utils/OfflineProxyUrl.cpp","es-core/src/utils/TimeText.cpp","es-core/src/utils/TimeUtil.cpp","es-core/src/utils/CommandLineUtil.h","es-core/src/utils/zip_file.hpp","es-core/src/resources/Font.cpp","es-core/src/resources/TabStops.h","es-core/src/resources/TextureResource.cpp","es-core/src/renderers/Renderer.cpp","es-core/src/utils/AtomicFileUtil.cpp","es-core/src/utils/AtomicFileUtil.h","es-core/src/utils/DownloadFile.cpp","es-core/src/Settings.cpp","es-core/src/SystemConf.cpp","es-core/src/HttpReq.cpp","es-core/src/components/TextComponent.cpp","es-core/src/components/MenuComponent.cpp","es-core/src/ImageIO.cpp","es-core/src/Log.cpp","es-core/src/Window.cpp","es-core/CMakeLists.txt","es-app/src/CloudText.cpp","es-app/src/ApiSystem.cpp","es-app/src/guis/GuiMenu.cpp","es-app/tests/unit/CMakeLists.txt"]
byp={r["path"]:r for r in rows if r["tree"]=="es"}
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p, "in-T36" if p in got else "not-in-T36", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"area",r["area"])
print("ES-CORE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="es" and r["path"].startswith("es-core/"):
        h,kind=hits(r); cnt[(tuple(h),kind)]+=1; ln[(tuple(h),kind)]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
python3 -I .qa-scratch/t36/membership.py /dev/null > .qa-scratch/t36/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="es" {print $2}' .qa-scratch/t36/block-1.txt > .qa-scratch/t36/paths.txt
wc -l .qa-scratch/t36/paths.txt
python3 -I .qa-scratch/t36/membership.py .qa-scratch/t36/paths.txt > .qa-scratch/t36/block-2.txt
/usr/bin/grep -E '^(mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t36/block-2.txt
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
git -C "$W" ls-tree -r --name-only "$PIN" -- es-core/src/utils/ es-core/src/resources/ es-core/src/renderers/ | /usr/bin/grep -v -E '^es-core/src/utils/AtomicFileUtil\.[^/]*$' | diff - .qa-scratch/t36/paths.txt && echo "ls-tree at the pin = paths.txt"
for p in $(cat .qa-scratch/t36/paths.txt); do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'
for p in $(cat .qa-scratch/t36/paths.txt); do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t36/paths.txt | wc -l
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t36/paths.txt | wc -l
git -C "$W" diff --shortstat "$MB" "$PIN" -- $(cat .qa-scratch/t36/paths.txt)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $(cat .qa-scratch/t36/paths.txt)

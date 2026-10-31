mkdir -p .qa-scratch/t35
cat > .qa-scratch/t35/membership.py <<'PYEOF'
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
    if h==["es-core-window-input"]: mine.append(r)
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
named=["es-core/src/Window.cpp","es-core/src/Window.h","es-core/src/InputManager.cpp","es-core/src/InputConfig.cpp","es-core/src/GuiComponent.cpp","es-core/src/ThemeData.cpp","es-core/src/Scripting.cpp","es-core/src/Log.cpp","es-core/src/guis/GuiMsgBox.cpp","es-core/src/guis/GuiTextEditPopupKeyboard.cpp","es-core/src/guis/GuiInfoPopup.cpp","es-core/src/watchers/WatchersManager.cpp","es-core/CMakeLists.txt","es-core/src/Settings.cpp","es-core/src/Settings.h","es-core/src/SystemConf.cpp","es-core/src/HttpReq.cpp","es-core/src/HttpReq.h","es-core/src/utils/AtomicFileUtil.cpp","es-core/src/utils/AtomicFileUtil.h","es-core/src/components/MenuComponent.cpp","es-core/src/components/AsyncNotificationComponent.cpp","es-core/src/utils/FileSystemUtil.cpp","es-core/src/utils/StringUtil.cpp","es-core/src/resources/Font.cpp","es-core/src/renderers/Renderer.cpp","es-core/src/utils/OfflineProxyUrl.cpp","es-app/src/CloudText.cpp","es-app/src/main.cpp","es-app/src/ApiSystem.cpp"]
byp={r["path"]:r for r in rows if r["tree"]=="es"}
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p, "in-T35" if p in got else "not-in-T35", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"area",r["area"])
print("ES-CORE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="es" and r["path"].startswith("es-core/"):
        h,kind=hits(r); cnt[(tuple(h),kind)]+=1; ln[(tuple(h),kind)]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
python3 -I .qa-scratch/t35/membership.py /dev/null > .qa-scratch/t35/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="es" {print $2}' .qa-scratch/t35/block-1.txt > .qa-scratch/t35/paths.txt
wc -l .qa-scratch/t35/paths.txt                                             # 96 (R1 C04)
python3 -I .qa-scratch/t35/membership.py .qa-scratch/t35/paths.txt > .qa-scratch/t35/block-2.txt
/usr/bin/grep -E '^(mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t35/block-2.txt
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
for p in $(cat .qa-scratch/t35/paths.txt); do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'                  # wc -l 22567 (R1 C11)
for p in $(cat .qa-scratch/t35/paths.txt); do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c", s}'   # grep -c 22575 (R1 C11)
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t35/paths.txt | wc -l   # every path but LogPolicy.h (R1 C12's `N N N N` row); the count is the lane's line
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t35/paths.txt | wc -l   # the same set
git -C "$W" diff --shortstat "$MB" "$PIN" -- $(cat .qa-scratch/t35/paths.txt)           # 13 files changed, 247 insertions(+), 71 deletions(-) (R1 C13)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $(cat .qa-scratch/t35/paths.txt)     # the same line (R1 C15)

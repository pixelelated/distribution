git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
A=rx("projects/ROCKNIX/devices/H700/**"); B=rx("projects/ROCKNIX/devices/H700/linux/*.conf")
t=[r for r in rows if (r["area"]=="devices" and r["reach"]=="shipped" and A.match(r["path"])) or (r["area"]=="patches-and-configs" and B.match(r["path"]))]
READ={"shell","udev","recipe"}
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",sum(1 for r in t if (r.get("language") or "") in READ),sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ),"fork-own",sum(r["lines"] or 0 for r in t if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("language",dict(collections.Counter((r.get("language") or "none") for r in t)))
import os; os.makedirs(".qa-scratch/t27", exist_ok=True)
open(".qa-scratch/t27/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))
print("written", len(t), ".qa-scratch/t27/paths.txt")'

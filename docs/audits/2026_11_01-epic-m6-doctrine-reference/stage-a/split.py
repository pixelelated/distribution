import collections
rows=[]; ix=None; p=False
for l in open(".qa-scratch/t39/block-2.txt"):
    l=l.rstrip("\n")
    if l=="TSV": p=True; continue
    if l.startswith("TREE-SIDE"): break
    if p and ix is None: ix={k:i for i,k in enumerate(l.split("\t"))}; continue
    if p: f=l.split("\t"); rows.append({k:f[i] for k,i in ix.items()})
L2={"docs/vm-qa-log.md","docs/cloud-sync-changelog.md","docs/releases/catalog.md"}
ASSET={"image","other","none"}
def cls(r):
    p=r["path"]
    if p.startswith("docs/reviews/"): return "L1-renovation-records"
    if p in L2: return "L2-running-records"
    if r["tier"]=="upstream-carried": return "R-upstream-carried"
    if r["language"] in ASSET: return "R-fork-assets"
    return "R-fork-reference"
def grp(p):
    q=p.split("/")
    if len(q)==1: return p
    if q[0]=="docs": return "docs/*" if len(q)==2 else "docs/"+q[1]+"/"
    return q[0]+"/"
c=collections.Counter(); n=collections.Counter()
with open(".qa-scratch/t39/classes.tsv","w") as out:
    for r in rows:
        k=cls(r); ln=0 if r["lines"]=="None" else int(r["lines"]); c[k]+=1; n[k]+=ln
        out.write("%s\t%s\t%s\t%s\n" % (k,grp(r["path"]),r["lines"],r["path"]))
for k in sorted(c): print("CLASS %-22s %4d paths %6d lines" % (k,c[k],n[k]))
print("LEDGER", sum(c[k] for k in c if k.startswith("L")), "paths", sum(n[k] for k in n if k.startswith("L")), "lines; REFERENCE", sum(c[k] for k in c if k.startswith("R")), "paths", sum(n[k] for k in n if k.startswith("R")), "lines")
for r in rows:
    if cls(r).startswith("L"): print("  ", cls(r), r["lines"], r["path"])

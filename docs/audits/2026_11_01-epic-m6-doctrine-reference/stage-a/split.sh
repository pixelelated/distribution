W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; G=${G:-/workspace/repos/pixelelated/distribution}; TIP=${TIP:-2174265e9c}
cat > .qa-scratch/t39/split.py <<'PYEOF'
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
PYEOF
python3 -I .qa-scratch/t39/split.py
while IFS=$'\t' read -r k g l p; do [ "$l" = None ] && continue; printf '%s\t%s\t%s\n' "$k" "$g" "$(git -C "$W" show "$P1:$p" | /usr/bin/grep -c '')"; done < .qa-scratch/t39/classes.tsv | awk -F'\t' '{a[$1]+=$3; b[substr($1,1,1)" "$2]+=$3; t+=$3} END {for (k in a) printf "P1 grep -c class %s %d\n", k, a[k]; for (k in b) printf "P1 grep -c group %s %d\n", k, b[k]; print "P1 grep -c total", t}' | sort
echo "tip: $TIP"
while IFS=$'\t' read -r k g l p; do if git -C "$G" cat-file -e "$TIP:$p" 2>/dev/null; then if [ "$(git -C "$G" rev-parse "$TIP:$p")" = "$(git -C "$G" rev-parse "$P1:$p")" ]; then s=same; else s=changed; fi; else s=absent; fi; printf '%s %s\n' "$k" "$s"; done < .qa-scratch/t39/classes.tsv | sort | uniq -c
git -C "$G" ls-tree -r --name-only "$TIP" > .qa-scratch/t39/tree-tip.txt
python3 -I .qa-scratch/t39/membership.py .qa-scratch/t39/paths.txt .qa-scratch/t39/tree-tip.txt | /usr/bin/grep '^\.qa-scratch/t39/tree-tip\.txt' | python3 -I -c 'import sys, ast
l=sys.stdin.read(); a=ast.literal_eval(l.split(" only-derived: ")[1].split(" only-mine: ")[0]); b=ast.literal_eval(l.split(" only-mine: ")[1].strip())
print("at the tip the selector reaches:", l.split(" derived: ")[1].split()[0], "paths; added since P1:", len(a), "; of the 254 absent:", len(b))
print("  added under docs/reviews/briefs/:", sum(1 for x in a if x.startswith("docs/reviews/briefs/")))
for x in a:
    if not x.startswith("docs/reviews/briefs/"): print("  added", x)'
echo "(end split)"

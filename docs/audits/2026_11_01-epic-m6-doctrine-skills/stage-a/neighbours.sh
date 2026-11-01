python3 -I -c 'import sys,collections
src=open(sys.argv[1]).read(); exec(src[:src.index("kof=")])
c=collections.Counter()
for r in rows:
    if r["tree"]!="distribution": continue
    for pre in ("docs/council-","research/"):
        if r["path"].startswith(pre):
            h,kind=hits(r); c[(pre+"*" if pre.endswith("-") else pre,tuple(h),kind,r["area"])]+=1
for k,v in sorted(c.items()): print(v,k)' .qa-scratch/t38/membership.py | /usr/bin/grep -v -E '^(distribution |columns:)'

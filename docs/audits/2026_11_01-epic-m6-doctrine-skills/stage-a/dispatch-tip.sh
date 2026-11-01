export LC_ALL=C; X=':(exclude).claude/rules/'
git ls-tree -r -z --name-only HEAD -- .claude/ | python3 -I -c 'import sys,subprocess
ps=[p for p in sys.stdin.buffer.read().split(b"\0") if p and not p.startswith(b".claude/rules/")]
n=0
for p in ps:
    d=subprocess.run(["git","show",b"HEAD:"+p],capture_output=True,check=True).stdout
    n+=d.count(b"\n")+(1 if d and not d.endswith(b"\n") else 0)
print("dispatch tip: paths",len(ps),"lines",n)'
git diff --shortstat 2174265e9c HEAD -- .claude/ "$X"; git diff --shortstat 8ebaf8daad HEAD -- .claude/ "$X"
git diff --numstat 2174265e9c HEAD -- .claude/ "$X"
git ls-tree -r --name-only HEAD -- .claude/ | /usr/bin/grep -c -i settings; git log --all --oneline -- '.claude/settings*' | /usr/bin/grep -c ''

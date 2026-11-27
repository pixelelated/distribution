#!/usr/bin/env python3
# offnext-check.py -- #1463 criterion 1: is every decided row of every M7
# register on `next`? Reads the working register of every M7 worktree and the
# committed register of every M7 ref (the candidate line, the round, the m7
# feature branches), and looks each Decided row up on next's register BY
# CONTENT: the text after the ID cell, with every decision number written as
# a placeholder, because a clerical rekey (D-WORKFLOW-013; D-INFRA-049,
# D-WORKFLOW-252, D-INFRA-053) changes the ID cell and the cross-references a
# row carries and nothing else. Prints each row found under another ID, and every row not
# found. M6's registers are not read (D-INFRA-038): their rows are M6's.
#   python3 -I offnext-check.py [--repo /workspace/repos/rocknix]
# Exit 0 when every M7 row is on next, 1 with the absent rows, 2 when a
# register could not be read.
import re, subprocess, sys
from pathlib import Path

repo = sys.argv[sys.argv.index('--repo') + 1] if '--repo' in sys.argv else '/workspace/repos/rocknix'
REG = 'docs/decision-register.md'

def git(*a):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True)

def rows(text):
    out = {}
    for l in text.split('\n'):
        m = re.match(r'\| (D-[A-Z]+-\d+) \| (\d{4}-\d{2}-\d{2}) \|(.*)$', l)
        if m:
            out.setdefault(m.group(1), []).append(m.group(2) + '|' + m.group(3))
    return out

# A quote escaped in one copy and plain in another (D-CLOUD-159 on an October
# branch) is the same text.
norm = lambda body: re.sub(r'\s+', ' ', re.sub(r'D-[A-Z]+-\d+(?:/\d+)*', 'D-#', body.replace('\\"', '"'))).strip()

r = git('show', f'next:{REG}')
if r.returncode:
    print('cannot read next:' + REG); sys.exit(2)
nxt = rows(r.stdout)
by_body = {}
for rid, bodies in nxt.items():
    for b in bodies:
        by_body.setdefault(norm(b), []).append(rid)

sources = []
wt = git('worktree', 'list', '--porcelain').stdout
for block in wt.split('\n\n'):
    path = next((l[9:] for l in block.split('\n') if l.startswith('worktree ')), None)
    branch = next((l[7:] for l in block.split('\n') if l.startswith('branch ')), '')
    if not path or Path(path).name.startswith('m6') or 'm6-' in branch:
        continue
    if not (Path(path).name.startswith('m7') or '/m7' in branch or 'm7-' in branch):
        continue
    f = Path(path) / REG
    if f.exists():
        sources.append((f'worktree {path}', f.read_text(encoding='utf-8')))
refs = [l for l in git('for-each-ref', '--format=%(refname:short)', 'refs/heads/', 'refs/m7/').stdout.split('\n')
        if l and ('m7' in l) and 'm6' not in l]
for ref in refs:
    s = git('show', f'{ref}:{REG}')
    if s.returncode == 0:
        sources.append((f'ref {ref}', s.stdout))

absent, moved, seen = [], {}, set()
for name, text in sources:
    for rid, bodies in rows(text).items():
        for b in bodies:
            key = (rid, norm(b))
            if key in seen:
                continue
            seen.add(key)
            hits = by_body.get(norm(b), [])
            if rid in hits:
                continue
            if hits:
                moved.setdefault((rid, ','.join(hits)), name)
            else:
                absent.append((rid, b[:10], name))
print(f'offnext-check: {len(sources)} M7 registers read; next has {sum(len(v) for v in nxt.values())} rows')
for (rid, to), name in sorted(moved.items()):
    print(f'  on next as {to}: {rid} (from {name})')
for rid, d, name in sorted(set(absent)):
    print(f'ABSENT {rid} {d} (first seen in {name})')
print('offnext-check: ' + ('every M7 row is on next' if not absent else f'{len(set(absent))} row(s) absent from next'))
sys.exit(1 if absent else 0)

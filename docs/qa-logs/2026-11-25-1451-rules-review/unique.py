#!/usr/bin/env python3
"""Read-only: for each file, the worktree's lines that next does not carry (whitespace-normalised), grouped in runs."""
import subprocess, sys, difflib, pathlib
wt = pathlib.Path(sys.argv[1]); files = sys.argv[2:]
for f in files:
    import os
    base = os.environ.get('BASE')
    if base:
        q = pathlib.Path(base)/f; nxt = q.read_text().splitlines() if q.is_file() else []
    else:
      try: nxt = subprocess.run(['git','-C',str(wt),'show','next:'+f],capture_output=True,text=True,check=True).stdout.splitlines()
      except subprocess.CalledProcessError: nxt = []
    p = wt/f
    cur = p.read_text().splitlines() if p.is_file() else []
    sm = difflib.SequenceMatcher(None,[' '.join(l.split()) for l in nxt],[' '.join(l.split()) for l in cur],autojunk=False)
    runs = [(j1,j2) for tag,i1,i2,j1,j2 in sm.get_opcodes() if tag in ('insert','replace') and j2>j1]
    n = sum(j2-j1 for j1,j2 in runs)
    print(f"##### {f}: {n} worktree-only lines in {len(runs)} runs")
    for j1,j2 in runs:
        print(f"--- worktree {j1+1}-{j2}")
        for l in cur[j1:j2]: print("  + "+l[:220])

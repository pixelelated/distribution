"""Compose 02-forward-audit.md from stage-b/02-template.md and the generators (#682).

    python3 -I t35-02.py <es worktree> <commit> <paths.txt> <template> <out>

Each `<!-- GEN <script> <key=value ...> -->` line in the template is replaced by the
script's output (run from the distribution worktree with the same worktree, commit and
paths; `t35-runs.py` takes the audit folder). A generator that exits non-zero stops the
composition and nothing is written. The coverage section's row count is re-checked on the
composed text with the acceptance's own awk rule.
"""
import os
import re
import subprocess
import sys

if len(sys.argv) != 6:
    sys.exit("usage: t35-02.py <es worktree> <commit> <paths.txt> <template> <out>")
W, ref, paths, tpl, out = sys.argv[1:]
here = os.path.dirname(os.path.abspath(__file__))
audit = os.path.dirname(here)
parts, labels = [], []
for line in open(tpl).read().split("\n"):
    m = re.match(r"^<!-- GEN (\S+)((?: \S+=\S+)*) -->$", line)
    if not m:
        parts.append(line)
        continue
    g, args = m.group(1), m.group(2).split()
    cmd = ["python3", "-I", os.path.join(here, g)] + ([os.path.relpath(audit)] if g == "t35-runs.py" else [W, ref, paths]) + args
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stdout[-2000:] + r.stderr[-2000:])
        sys.exit(f"t35-02: {g} exited {r.returncode}; nothing written")
    body = r.stdout.rstrip("\n")
    last = body.split("\n")[-1]
    labels.append(f"{g}: {last}")
    parts.append(body)
text = "\n".join(parts)
cov = re.search(r"^## Coverage\n(.*?)^## ", text, re.S | re.M).group(1)
n = len([l for l in cov.split("\n") if l.startswith("| `")])
if n != 96:
    sys.exit(f"t35-02: the composed coverage section has {n} rows, not 96; nothing written")
ph = re.findall(r"__[A-Z]+__|\b(?:CO" "HASH|MERGE_" "HASH|TIP" "HASH|V2" "HASH)\b", text)
if ph:
    sys.exit(f"t35-02: {len(ph)} placeholder(s) in the composition; nothing written")
open(out, "w").write(text if text.endswith("\n") else text + "\n")
print(f"composed {out}: {len(labels)} generated sections, coverage rows {n}, placeholders 0")
for l in labels:
    print("  " + l)

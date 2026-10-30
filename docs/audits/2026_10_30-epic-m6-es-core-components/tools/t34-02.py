"""Compose 02-forward-audit.md (#681) from tools/t34-02.template.md and the
generators: each {{name}} is replaced by tools/t34-<name>.py's output. Refuses
(exit 1, nothing written) if a generator fails or a marker stays unfilled.
    t34-02.py <ES worktree>"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
PIN = "16dbac5211eea7e70db7394372033be2be7df829"
GEN = {"coverage": [W], "leads": [], "layouts": [W], "constants": [W], "input": [W], "lifetimes": [W], "reads": [W], "words": [W], "structure": None}
tpl = open(os.path.join(HERE, "t34-02.template.md"), encoding="utf-8").read()
out = tpl
for name, args in GEN.items():
    script = "t34-includes.py" if name == "structure" else "t34-%s.py" % name
    argv = [W, PIN] if name == "structure" else args
    r = subprocess.run([sys.executable, "-B", "-I", os.path.join(HERE, script)] + argv, capture_output=True, text=True)
    if r.returncode != 0:
        print("t34-02: %s exited %d: %s" % (script, r.returncode, r.stderr.strip()), file=sys.stderr)
        sys.exit(1)
    marker = "{{%s}}" % name
    if out.count(marker) != 1:
        print("t34-02: the template holds %r %d times" % (marker, out.count(marker)), file=sys.stderr)
        sys.exit(1)
    out = out.replace(marker, r.stdout.rstrip("\n"))
left = re.findall(r"\{\{[a-z]+\}\}", out)
if left:
    print("t34-02: unfilled markers %s" % left, file=sys.stderr)
    sys.exit(1)
dest = os.path.join(os.path.dirname(HERE), "02-forward-audit.md")
open(dest, "w", encoding="utf-8").write(out)
print("t34-02: wrote %s, %d lines, %d generated sections" % (os.path.relpath(dest), out.count("\n"), len(GEN)))

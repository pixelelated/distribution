"""Run brief § 5's block run by run: the preamble (the lines before the first
'# ' comment) then each comment's commands, timed, with the last command's
exit. Writes one section per run."""
import subprocess, sys, time
src = open(sys.argv[1]).read().split("\n")
skip = sys.argv[3:] if len(sys.argv) > 3 else []
pre, runs, cur = [], [], None
for line in src:
    if line.startswith("# "):
        cur = [line[2:], []]; runs.append(cur)
    elif cur is None:
        pre.append(line)
    elif line.strip():
        cur[1].append(line.replace("TIPHASH", "3d591f7e30"))
out = []
for title, cmds in runs:
    if any(s in title for s in skip):
        out.append("## %s\nNOT RUN AT STAGE A (%s)\n" % (title, "its script is written at stage B")); continue
    script = "\n".join(pre + cmds)
    t0 = time.time()
    r = subprocess.run(["bash", "-c", script + "\necho \"__rc=$?\""], capture_output=True, text=True, cwd=sys.argv[2])
    dt = time.time() - t0
    body = r.stdout + (("\n[stderr]\n" + r.stderr) if r.stderr.strip() else "")
    out.append("## %s\nwall %.1f s\n%s" % (title, dt, body))
print("\n".join(out))

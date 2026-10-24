#!/usr/bin/env python3
"""The coverage table of 02-forward-audit.md: one row per membership path (#652).

    python3 -I coverage-table.py <tree> > table.md

Reads the membership from the inventory with brief section 2's filter, the
Q4 (a) differences (`git diff --name-status upstream/next 8ebaf8daad`), the
Q6 caller counts (q6-tables.md), and the per-path cells below. Asserts 242
rows and no empty cell, and says so on stderr.
"""
import json, re, subprocess, sys
T = sys.argv[1]
A = T + "/docs/audits/2026_10_24-epic-m6-build-engine"
inv = json.load(open(T + "/docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
globs = ["scripts/**", "config/**", "distributions/ROCKNIX/**", "Makefile", "Dockerfile", ".gitignore", ".merge-head", ".github/**"]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
mem = sorted((r for r in rows if r["tree"] == "distribution" and r["area"] == "build-engine" and any(gm(r["path"], g) for g in globs)), key=lambda r: r["path"])
diff = {}
for l in subprocess.run(["git", "-C", T, "diff", "--name-status", "upstream/next", "8ebaf8daad", "--"] + [r["path"] for r in mem], capture_output=True, text=True, check=True).stdout.splitlines():
    st, p = l.split("\t", 1); diff[p] = st
forkc = {}
for r in mem:
    if r["tier"] == "fork-own":
        forkc[r["path"]] = " ".join(subprocess.run(["git", "-C", T, "log", "--format=%h", "c445081a59..8ebaf8daad", "--", r["path"]], capture_output=True, text=True, check=True).stdout.split()) or "before the base"
q6 = {}
for l in open(A + "/q6-tables.md"):
    m = re.match(r"^\| `(scripts/[^`]+)` \| (\d+) \| (.*?) \|", l)
    if m: q6[m.group(1)] = m.group(3)
CELLS = json.load(open(A + "/tools/coverage-cells.json"))   # per-path overrides: {path: {Q1..Q7: text}}
def group(r):
    p = r["path"]
    if r["tier"] == "fork-own": return 1
    if p.startswith("config/emulators/"): return 3
    if p.startswith(("config/noobs/", "config/addon/", "config/docker/")): return 4
    if p.startswith(".github/"): return 5
    return 2
UP = "n/a: upstream's, unchanged here"
def q4(p):
    st = diff.get(p)
    if st is None: return "Q4 (a): identical to `upstream/next`"
    return "Q4 (a): differs (" + st + "), see `04` Q4 (a)"
def default(r):
    p, g = r["path"], group(r)
    c = {"Q4": q4(p)}
    if g == 3:
        c.update(Q1=UP, Q2=UP, Q3=UP, Q5="n/a: read once per build by `add_es_system`; no cost of its own", Q6="Table 2 (`q6-tables.md`)", Q7=UP)
        if p.endswith(("/daphne.conf", "/gp32.conf")): c["Q3"] = "F-03: no `SYSTEM_RELEASE`, so the image carries the previous system's (P7)"
        if p.endswith(("/arcade.conf", "/segamodel3.conf")): c["Q3"] = "F-03: no `SYSTEM_WIKI_PATH`; the document inherits the previous system's"
        if p.endswith(("/imageviewer.conf", "/moonlight.conf", "/tools.conf")): c["Q3"] = "F-03: sets `SYSTEM_COMMAND`, which the next system would inherit (P6)"
    elif g == 4:
        c.update(Q1=UP, Q2=UP, Q3=UP, Q5="n/a: not read by a fork build", Q6="Table 3: no fork build, image or CI reaches it", Q7=UP)
    elif g == 5:
        c.update(Q1=UP, Q2=UP, Q3=UP, Q5="n/a: runs on GitHub, not on the build host", Q7=UP,
                 Q6="Table 4 (`q6-tables.md`)" if "/workflows/" in p else "read by GitHub when an issue or a PR is opened on the fork; none uses it (T10's)")
    elif g == 2:
        c.update(Q1="read whole by the research subagent, leads re-read: no finding", Q2="`bash -n` ok (shell); shellcheck read; leads re-read: no finding", Q3="read whole by the research subagent, leads re-read: no finding", Q5="n/a: no measurement of its own", Q7="read whole by the research subagent: no finding",
                 Q6=q6.get(p, "sourced by `config/options` or `config/path` on every build"))
    else:
        c.update(Q6=q6.get(p, "reached by every fork build"))
    c.update(CELLS.get(p, {}))
    return c
out = ["| Path | Group | Tier | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Fork commits read |", "| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
empty = 0
for r in mem:
    c = default(r)
    cells = [c.get(q, "") for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7")]
    empty += sum(1 for x in cells if not x.strip())
    out.append("| `{}` | {} | {} | {} | {} |".format(r["path"], group(r), r["tier"], " | ".join(x.replace("|", "\\|") for x in cells), forkc.get(r["path"], "-")))
print("\n".join(out))
assert len(mem) == 242, len(mem)
print(f"coverage-table: {len(mem)} rows, {empty} empty cells", file=sys.stderr)
sys.exit(1 if empty else 0)

#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""t4-q6.py -- the reachability tables of M6 T4 (#651, brief § 4 Q6) and the
load table of Q5, read from the doctrine at a hash and never typed by hand.

    python3 -I t4-q6.py <read-tree> <tree-list> rules|load|pointers|tooltable|blindspots|retired|friction

<read-tree> is the at-hash export (`.qa-scratch/t4/at-hash/`), <tree-list>
`git ls-tree -r --name-only 8ebaf8daad`. Tool text is read with
`git show 8ebaf8daad:<path>`; nothing else is read.

  rules       per rule: lines, its `paths:` globs and each glob's match count at
              the hash, loads (every session / on a match), and a 0-match glob
  tooltable   every row of instruction-files.md's fork-tools table: each tool
              it names, tracked or not, and the rule it points at, tracked or not
  blindspots  every entry (table rows 1-29 and `## N.` headings): its number,
              the guard paths it names in backticks, and whether each exists
  retired     every line naming a mechanism a register row retired
              (`cloud_migrate_layout`, join/follow, `rclonectl`, `.github/instructions`),
              for the auditor to class as retired-and-said-so or described-as-current
  friction    the friction log's dated entries that tools/ceremony-check's own
              matcher never sees (its regex lifted from the tool at the hash)

Each mode prints a Markdown table and a count line, and exits 1 on an empty cell.
"""
import os, re, subprocess, sys

root, tree_list, mode = sys.argv[1], sys.argv[2], sys.argv[3]
tree = open(tree_list).read().splitlines()
tset = set(tree)
dirs = {"/".join(p.split("/")[:i]) for p in tree for i in range(1, p.count("/") + 1)}
read = lambda p: open(os.path.join(root, p), errors="replace").read()
show = lambda p: subprocess.run(["git", "show", "8ebaf8daad:" + p], capture_output=True, text=True).stdout
R = ".claude/rules/"
out = []


def glob_rx(g):
    s, i = "", 0
    while i < len(g):
        if g.startswith("**/", i): s += "(?:.*/)?"; i += 3
        elif g.startswith("**", i): s += ".*"; i += 2
        elif g[i] == "*": s += "[^/]*"; i += 1
        elif g[i] == "?": s += "[^/]"; i += 1
        else: s += re.escape(g[i]); i += 1
    return re.compile(s + r"\Z")


def exists(p):
    p = p.rstrip("/")
    return p in tset or p in dirs


if mode == "rules":
    out += ["| Rule | Lines | `paths:` | Loads | Globs matching nothing at the hash |", "| --- | ---: | --- | --- | --- |"]
    tot = {"every session": [0, 0], "on a match": [0, 0]}
    for f in sorted(os.listdir(os.path.join(root, R))):
        s = read(R + f); n = s.count("\n")
        m = re.match(r"^---\n(.*?)\n---\n", s, re.S); fm = m.group(1) if m else ""
        pm = re.search(r"^paths:\s*\n((?:[ \t]*(?:-.*|#.*)\n?)+)", fm + "\n", re.M)
        globs = re.findall(r'^[ \t]*-\s*"([^"]+)"', pm.group(1), re.M) if pm else []
        counts = [(g, sum(1 for p in tree if glob_rx(g).match(p))) for g in globs]
        every = (not pm) or globs == ["**"]
        k = "every session" if every else "on a match"; tot[k][0] += 1; tot[k][1] += n
        shown = "none (every session)" if not pm else ", ".join(f"`{g}` {c}" for g, c in counts)
        zero = ", ".join(f"`{g}`" for g, c in counts if c == 0) or "none"
        out.append(f"| `{f}` | {n} | {shown} | {k} | {zero} |")
    out += ["", f"<!-- rules: 30; every session {tot['every session'][0]} rules, {tot['every session'][1]} lines; on a match {tot['on a match'][0]} rules, {tot['on a match'][1]} lines -->"]
elif mode == "load":
    import json
    inv = json.load(open(os.environ.get("T4_INVENTORY", "docs/reviews/inventory.json"))); cols = inv["columns"]
    rows = [dict(zip(cols, r)) for r in inv["rows"] if r[cols.index("tree")] == "distribution"]
    areas = sorted({r["area"] for r in rows})
    out += ["| Rule | Lines | Loads | Areas whose paths it reaches (of %d) |" % len(areas), "| --- | ---: | --- | ---: |"]
    per_area = {a: 0 for a in areas}; tot = 0
    for f in sorted(os.listdir(os.path.join(root, R))):
        s2 = read(R + f); n = s2.count("\n")
        m = re.match(r"^---\n(.*?)\n---\n", s2, re.S); fm = m.group(1) if m else ""
        pm = re.search(r"^paths:\s*\n((?:[ \t]*(?:-.*|#.*)\n?)+)", fm + "\n", re.M)
        globs = re.findall(r'^[ \t]*-\s*"([^"]+)"', pm.group(1), re.M) if pm else []
        every = (not pm) or globs == ["**"]
        if every:
            hit = set(areas)
        else:
            rx = [glob_rx(g) for g in globs]
            hit = {r["area"] for r in rows if any(x.match(r["path"]) for x in rx)}
        for a in hit: per_area[a] += 1
        if every: tot += n
        out.append(f"| `{f}` | {n} | {'every session' if every else 'on a match'} | {len(hit)} |")
    out += ["", "| Area | Rules reaching it |", "| --- | ---: |"] + [f"| {a} | {per_area[a]} |" for a in areas]
    out += ["", f"<!-- load: {len(areas)} areas; every-session lines {tot} -->"]
elif mode == "pointers":
    # PL-19: each fork tool's *Detail in* rule must name the tool, unless the row
    # points the tool at its own header (`<rule>` for `<tool>` assigns a rule to one tool).
    s2 = read(R + "instruction-files.md")
    sec = s2[s2.index("## The fork's own tools"):s2.index("**When a rule earns")]
    named = lambda txt, t: re.search(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", txt) is not None
    pairs = bad = own = 0
    out += ["| Tool | Rule the row points at | The rule names the tool |", "| --- | --- | --- |"]
    for line in sec.splitlines():
        if not line.startswith("| `"): continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        tools = [t.split(" ")[0].rstrip("/") for t in re.findall(r"`([^`]+)`", cells[0])]
        cell = cells[-1]
        for t in tools:
            m = re.search(r"`([a-z0-9-]+\.md)` for `" + re.escape(t) + "`", cell)
            if m:
                rs = [m.group(1)]
            elif re.search(r"`" + re.escape(t) + r"`: its own header", cell) or ("own header" in cell and not re.search(r"`[a-z0-9-]+\.md`", cell)):
                own += 1; out.append(f"| `{t}` | its own header | n/a |"); continue
            else:
                rs = [r for r in re.findall(r"`([a-z0-9-]+\.md)`", cell) if not re.search(r"`" + re.escape(r) + r"` for `", cell)]
            for r in rs:
                pairs += 1; ok = named(read(R + r), t); bad += not ok
                out.append(f"| `{t}` | `{r}` | {'yes' if ok else '**no**'} |")
    out += ["", f"<!-- pointers: {pairs} tool-to-rule pairs; the rule never names the tool: {bad}; tools pointed at their own header: {own} -->"]
elif mode == "tooltable":
    s = read(R + "instruction-files.md")
    sec = s[s.index("## The fork's own tools"):s.index("**When a rule earns")]
    out += ["| Row | Tools named | All tracked | Rule it points at | Rule exists |", "| --- | --- | --- | --- | --- |"]
    k = bad = 0
    for line in sec.splitlines():
        if not line.startswith("| `"): continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        tools = re.findall(r"`([^`]+)`", cells[0]); k += 1
        missing = [t for t in tools if not exists("tools/" + t.split(" ")[0])]
        rules = re.findall(r"`([a-z0-9-]+\.md)`", cells[-1])
        rmiss = [r for r in rules if not exists(R + r)]
        bad += bool(missing or rmiss)
        out.append(f"| {k} | {', '.join('`' + t + '`' for t in tools)} | {'yes' if not missing else 'MISSING: ' + ', '.join(missing)} | {cells[-1].replace('|', '/') or '-'} | {'yes' if rules and not rmiss else ('MISSING: ' + ', '.join(rmiss) if rmiss else 'n/a: names no rule file')} |")
    out += ["", f"<!-- tooltable: {k} rows; {bad} with a missing tool or rule -->"]
elif mode == "blindspots":
    s = read("docs/blindspot-register.md").splitlines()
    ents = []
    for n, l in enumerate(s, 1):
        m = re.match(r"^\| (\d+) \|", l) or re.match(r"^## (\d+)\.", l)
        if m: ents.append((int(m.group(1)), n))
    out += ["| Entry | Line | Form | Guard paths named (backticked `tools/`, `.githooks/`, `.claude/rules/`) | All exist at the hash |", "| ---: | ---: | --- | --- | --- |"]
    for i, (num, n) in enumerate(ents):
        end = ents[i + 1][1] - 1 if i + 1 < len(ents) else len(s)
        body = "\n".join(s[n - 1:end]) if s[n - 1].startswith("## ") else s[n - 1]
        paths = sorted(set(re.findall(r"`((?:tools|\.githooks)/[A-Za-z0-9_./-]+|\.claude/rules/[A-Za-z0-9_.-]+\.md)", body)))
        ok = [p for p in paths if exists(p.split(" ")[0])]
        out.append(f"| {num} | {n} | {'table row' if s[n - 1].startswith('|') else 'heading'} | {', '.join('`' + p + '`' for p in paths) or 'none named'} | {('yes' if len(ok) == len(paths) else 'NO: ' + ', '.join(sorted(set(paths) - set(ok)))) if paths else 'n/a'} |")
    nums = [e[0] for e in ents]
    dup = sorted({x for x in nums if nums.count(x) > 1})
    out += ["", f"<!-- blindspots: {len(ents)} entries, numbers {min(nums)} to {max(nums)}, used twice: {dup or 'none'}; entries naming a guard path {sum(1 for l in out if re.match(r'^\| \d+ \|', l) and 'none named' not in l)} -->"]
elif mode == "retired":
    pat = re.compile(r"cloud_migrate_layout|\bjoin(?:s|ed|ing)?\b.{0,40}\bfollow|rclonectl|\.github/instructions|copilot", re.I)
    files = [R + f for f in sorted(os.listdir(os.path.join(root, R)))] + ["CLAUDE.md", "AGENTS.md", "NAMING.md"]
    out += ["| File:line | The mention |", "| --- | --- |"]
    k = 0
    for f in files:
        for n, l in enumerate(read(f).splitlines(), 1):
            if pat.search(l):
                out.append(f"| `{f.split('/')[-1]}:{n}` | {l.strip()[:170].replace('|', '/')} |"); k += 1
    out += ["", f"<!-- retired: {k} mentions -->"]
elif mode == "friction":
    src = show("tools/ceremony-check")
    rx = re.compile(re.search(r"m = re\.match\(r'([^']+)', line\.strip\(\), re\.I\)", src).group(1), re.I)
    out += ["| Line | Date | Why the check skips it | Issue named in the text |", "| ---: | --- | --- | --- |"]
    k = tot = 0
    for n, l in enumerate(read("docs/friction-log.md").splitlines(), 1):
        t = l.strip(); m = re.match(r"^- (\d{4}-\d\d-\d\d)", t)
        if not m: continue
        tot += 1
        if rx.match(t): continue
        k += 1
        why = "no `issue:` field" if not re.search(r"issue:", t, re.I) else "`issue:` present in another shape"
        iss = ", ".join(sorted(set(re.findall(r"#\d+", t)))[:4]) or "none"
        out.append(f"| {n} | {m.group(1)} | {why} | {iss} |")
    out += ["", f"<!-- friction: {tot} dated entries; {k} never seen by the check's matcher -->"]
else:
    sys.exit("usage: t4-q6.py <read-tree> <tree-list> rules|load|pointers|tooltable|blindspots|retired|friction")

for l in out:
    if re.search(r"\|\s*\|", l):
        print("EMPTY CELL: " + l, file=sys.stderr); sys.exit(1)
print("\n".join(out))

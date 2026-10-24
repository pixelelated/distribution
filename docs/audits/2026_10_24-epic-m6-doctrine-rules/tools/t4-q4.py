#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""t4-q4.py -- the four currency tables of M6 T4 (#651, brief § 4 Q4), read
from the doctrine at a hash and never typed by hand (futro A3).

    python3 -I t4-q4.py <read-tree> <tree-list> ids|ledger-ids|tools|paths|counts

<read-tree> is `git archive 8ebaf8daad <the 36> | tar -x` (`.qa-scratch/t4/at-hash/`);
<tree-list> is `git ls-tree -r --name-only 8ebaf8daad` (every tracked path at
the hash, `.qa-scratch/t4/tree-hash.txt`). Nothing is read from the network,
the working tree or another branch.

  ids         every decision ID cited in the 33 non-register files: its table
              (Decided / Open), its date, the files citing it, and the later
              register rows that cite it with a reversal word -- a candidate
              for "superseded", which the auditor reads and classes by hand
  ledger-ids  the same for the IDs the blindspot register and friction log cite
  tools       every `tools/<name>` and `.githooks/<name>` the 36 files name:
              tracked at the hash or not, and each `--option` written beside
              it on the same line: present as a literal in the tool's text or not
  paths       every backticked repo path the 36 files name: tracked at the
              hash (file or directory), a glob, a legacy path (#640), or absent
  counts      every sentence in the 33 that states a count of rules, entries,
              tools, screens, rows or files, for the auditor's recount

Each mode prints a Markdown table and a class-count line, and exits 1 when a
row has an empty cell.
"""
import os, re, sys, collections

root, tree_list, mode = sys.argv[1], sys.argv[2], sys.argv[3]
tree = set(open(tree_list).read().splitlines())
dirs = {"/".join(p.split("/")[:i]) for p in tree for i in range(1, p.count("/") + 1)}
REG = "docs/decision-register.md"
LEDGERS = ["docs/blindspot-register.md", "docs/friction-log.md"]
rules = sorted(".claude/rules/" + f for f in os.listdir(os.path.join(root, ".claude/rules")))
NONREG = rules + ["CLAUDE.md", "AGENTS.md", "NAMING.md"]
ALL36 = NONREG + [REG] + LEDGERS
read = lambda p: open(os.path.join(root, p), errors="replace").read()
ID = re.compile(r"\bD-[A-Z]+-\d+\b")
REV = re.compile(r"\b(revers|supersed|replac|refin|withdr|retir|overrid|narrow|amend|correct)", re.I)
out = []


def register_rows():
    rows, section = {}, None
    for n, line in enumerate(read(REG).splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
        m = re.match(r"^\| (D-[A-Z]+-\d+) \|(.*)$", line)
        if m:
            d = re.match(r"\s*(\d{4}-\d\d-\d\d)\s*\|", m.group(2))
            rows[m.group(1)] = dict(line=n, section=section, date=d.group(1) if d else "-", text=m.group(2))
    return rows


def id_table(files, title):
    rows = register_rows()
    cited = collections.defaultdict(set)
    for f in files:
        for i in ID.findall(read(f)):
            cited[i].add(f.split("/")[-1])
    out.append(f"| ID | Table | Date | Cited by | Later rows citing it with a reversal word |")
    out.append("| --- | --- | --- | --- | --- |")
    cls = collections.Counter()
    for i in sorted(cited, key=lambda x: (x.split("-")[1], int(x.split("-")[2]))):
        r = rows.get(i)
        if not r:
            out.append(f"| `{i}` | **absent** | - | {', '.join(sorted(cited[i]))} | - |"); cls["absent"] += 1; continue
        later = [k for k, v in rows.items() if k != i and i in ID.findall(v["text"]) and REV.search(v["text"])
                 and (v["date"] == "-" or r["date"] == "-" or v["date"] >= r["date"])]
        tab = "Decided" if r["section"] == "Decided" else "Open" if r["section"] == "Open decisions" else r["section"]
        cls[tab] += 1
        if later:
            cls["with a reversal-word citer"] += 1
        out.append(f"| `{i}` | {tab} (line {r['line']}) | {r['date']} | {', '.join(sorted(cited[i]))} | {', '.join('`' + k + '`' for k in sorted(later)) or 'none'} |")
    out.append("")
    out.append(f"<!-- {title}: {len(cited)} IDs; " + "; ".join(f"{k} {v}" for k, v in sorted(cls.items())) + " -->")


if mode == "ids":
    id_table(NONREG, "ids in the 33 non-register files")
elif mode == "ledger-ids":
    id_table(LEDGERS, "ids in the two record ledgers")
elif mode == "tools":
    seen = collections.OrderedDict()
    for f in ALL36:
        for n, line in enumerate(read(f).splitlines(), 1):
            for m in re.finditer(r"(?<![\w/.-])((?:tools|\.githooks)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/?)", line):
                t = m.group(1).rstrip("/.")
                opts = re.findall(r"(?<![\w-])(--[a-z][a-z0-9-]+)", line[m.end():m.end() + 160].split("`")[0])
                seen.setdefault(t, []).append((f.split("/")[-1], n, opts))
    out.append("| Tool | At the hash | Named in (first three) | Options written beside it | Options not in its text |")
    out.append("| --- | --- | --- | --- | --- |")
    cls = collections.Counter()
    for t, uses in seen.items():
        tracked = t in tree or t in dirs
        cls["tracked" if tracked else "absent"] += 1
        opts = sorted({o for _, _, os_ in uses for o in os_})
        text = ""
        if t in tree:
            try:
                text = os.popen(f"git show 8ebaf8daad:{t} 2>/dev/null").read()
            except Exception:
                text = ""
        missing = [o for o in opts if text and o not in text] if t in tree else []
        if missing:
            cls["option not in the tool's text"] += 1
        where = ", ".join(f"{f}:{n}" for f, n, _ in uses[:3]) + (f" (+{len(uses) - 3})" if len(uses) > 3 else "")
        out.append(f"| `{t}` | {'tracked' if t in tree else 'directory' if t in dirs else '**absent**'} | {where} | {' '.join('`' + o + '`' for o in opts) or '-'} | {' '.join('`' + o + '`' for o in missing) or ('n/a: a directory' if t in dirs and t not in tree else 'none' if tracked else 'n/a: absent')} |")
    out.append("")
    out.append(f"<!-- tools: {len(seen)} named; " + "; ".join(f"{k} {v}" for k, v in sorted(cls.items())) + " -->")
elif mode == "paths":
    ROOTS = ("docs/", "projects/", "packages/", "scripts/", ".claude/", ".github/", "config/", "distributions/", "research/", "seed/", "plans/")
    seen = collections.OrderedDict()
    for f in ALL36:
        for n, line in enumerate(read(f).splitlines(), 1):
            for m in re.finditer(r"`([^`\s]+)`", line):
                p = m.group(1).rstrip(".,;:)")
                if p.startswith("/workspace/repos/rocknix") or "rocknix.worktrees" in p:
                    seen.setdefault(p, []).append((f.split("/")[-1], n, "legacy")); continue
                if p.startswith(ROOTS) and "/" in p:
                    seen.setdefault(p, []).append((f.split("/")[-1], n, "repo"))
    out.append("| Path | At the hash | Named in (first three) |")
    out.append("| --- | --- | --- |")
    cls = collections.Counter()
    for p, uses in seen.items():
        q = re.sub(r"[:#].*$", "", p).rstrip("/")
        if uses[0][2] == "legacy":
            st = "legacy: #640"
        elif any(c in q for c in "*?{<[") or "..." in q or "…" in q:
            st = "glob or placeholder"
        elif q in tree:
            st = "tracked file"
        elif q in dirs:
            st = "tracked directory"
        else:
            st = "**absent**"
        cls[st] += 1
        where = ", ".join(f"{f}:{n}" for f, n, _ in uses[:3]) + (f" (+{len(uses) - 3})" if len(uses) > 3 else "")
        out.append(f"| `{p}` | {st} | {where} |")
    out.append("")
    out.append(f"<!-- paths: {len(seen)} named; " + "; ".join(f"{k} {v}" for k, v in sorted(cls.items())) + " -->")
elif mode == "counts":
    pat = re.compile(r"\b(\d[\d,]*)\s+(?:of\s+(?:the\s+)?\d[\d,]*\s+)?(rule files?|rules|entries|tools|fork tools|screens|rows|files|instruction files|suites|skills|open checkbox(?:es)?|checkboxes|IDs|decisions)\b")
    out.append("| File:line | The count as written |")
    out.append("| --- | --- |")
    k = 0
    for f in NONREG:
        for n, line in enumerate(read(f).splitlines(), 1):
            for m in pat.finditer(line):
                s = line[max(0, m.start() - 50):m.end() + 30].replace("|", "\\|").strip()
                out.append(f"| `{f.split('/')[-1]}:{n}` | ...{s}... |"); k += 1
    out.append("")
    out.append(f"<!-- counts: {k} stated -->")
else:
    sys.exit("usage: t4-q4.py <read-tree> <tree-list> ids|ledger-ids|tools|paths|counts")

for l in out:
    if re.search(r"\|\s*\|", l):
        print("EMPTY CELL: " + l, file=sys.stderr); sys.exit(1)
print("\n".join(out))

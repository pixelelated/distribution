"""t38-inherit.py: T38 (#685) stage E's amendment (the acceptance read's ask 7): one row per export lead, L-30 to
L-50 and L-76 to L-78, for 02 § What the coordinator, the export's refresh and the next slices inherit, each at its
file:line. A lead whose 02 § The leads row names its lines carries that cell; a lead whose row describes them (the
agents' links, the descriptions, a term's lines) carries the lines `git grep -n` prints at the dispatch tip
87c2ab0fed, by the pattern recorded here. Exits 2 when a lead's row is missing or a grep prints nothing.

    python3 -I t38-inherit.py <worktree>
"""
import collections, pathlib, re, subprocess, sys

REPO = sys.argv[1]
TIP = "87c2ab0fed"
A02 = pathlib.Path(__file__).resolve().parent.parent / "02-forward-audit.md"
FAMILY = [".claude/skills/council", ".claude/skills/council-research", ".claude/agents"]
GREP = {  # lead -> (git grep arguments, paths): the lines a descriptive row means
    35: (["-F", "references/member-roster.md"], [".claude/agents"]),
    38: (["-F", ".github/instructions"], [".claude/agents"]),
    41: (["-E", "^(description|tools):"], [".claude/agents"]),
    42: (["-F", "research/trio-runs"], FAMILY),
    44: (["-E", r"^\| `council-member-|^model:|^  - "], [".claude/skills/council/references/member-roster.md", ".claude/agents"]),
    45: (["-i", "-F", "rasteratops"], FAMILY),
    49: (["-i", "-F", "shadow"], FAMILY),
    50: (["-i", "-E", "all in place|adaptations"], [".claude/rules/council-substrate-integrity.md", ".claude/skills/council/IMPORTED-FROM.md"]),
}
LEAD_IN = {49: "a positive, the 52 hold no shadow-seat instruction; the term's one line is a path in the bundle's list: "}
OWNER = {32: "#911, noted so it is not re-found (L-32 withdrawn at stage B: the file is council-research's, and the sentence names it)",
         47: "#807 (comment 6553118160, the maintainer's answer), then #911 (PL-54)",
         50: "#911's re-review; the rule half is the coordinator's open erratum (the row below)"}


def grep(n):
    args, paths = GREP[n]
    r = subprocess.run(["git", "-C", REPO, "grep", "-n", *args, TIP, "--", *paths], capture_output=True, text=True)
    if r.returncode not in (0, 1):
        sys.exit(f"t38-inherit: refused: git grep for L-{n} exited {r.returncode}")
    by = collections.OrderedDict()
    for l in r.stdout.splitlines():
        _, path, ln = l.split(":", 3)[:3]
        by.setdefault(path, []).append(ln)
    if not by:
        sys.exit(f"t38-inherit: refused: git grep for L-{n} printed nothing")
    cell = "; ".join(f"`{p.replace('.claude/skills/', '').replace('.claude/agents/', 'agents/')}:{', :'.join(lns)}`" for p, lns in by.items())
    cell = LEAD_IN.get(n, "") + cell + f" (`git grep -n {' '.join(args)}` at `{TIP}`)"
    return cell.replace("|", "\\|")  # a regex's alternation inside a table cell


s = A02.read_text()
print("| Lead | Lines | Owner |")
print("| --- | --- | --- |")
for n in list(range(30, 51)) + [76, 77, 78]:
    m = re.search(rf"^\| L-{n} \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|", s, re.M)
    if not m:
        sys.exit(f"t38-inherit: refused: 02 has no row for L-{n}")
    lines, family, owner, disp = (x.strip() for x in m.groups())
    what = family if family != "--" else disp.split(":")[0].split(",")[0]
    cell = grep(n) if n in GREP else lines
    own = OWNER.get(n, owner if owner != "read" else "#911")
    print(f"| L-{n} ({what}) | {cell} | {own}; PL-53 |")

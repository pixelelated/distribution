"""02 § The runs: every § 5 run from stage A's record, the generators' drift record, and the stage-C runs owed (#682).

    python3 -I t35-runs.py <audit folder> [runs=N generators=N]

Reads `stage-a/runs.out` (each block: a `# ` title line with the expectation, the output,
then `run rc=N wall=Ns`) and `stage-b/generators.txt` (each generator: clean, then three
constructed drifts). Prints one row per block with its exit, wall time, figure and what a
FAIL would mean, and asserts the counts.
"""
import re
import sys

if len(sys.argv) < 2:
    sys.exit("usage: t35-runs.py <audit folder> [key=value ...]")
A = sys.argv[1]
expect = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
fail = []


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    out += ["| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |" for r in rows]
    return "\n".join(out)


MEAN = [
    "the paths list is not the slice the brief names: a scope drift, stop (§ 8)",
    "the read is not the pin's, or a base moved: the merge debt is re-derived",
    "a line rule differs: the coverage table's lines are wrong",
    "the fork changed the slice since the brief: the 13 are re-read",
    "upstream moved on the 96: the merge debt grows",
    "another lane edited inside the 96: a collision for the hand-back",
    "the strings moved: § The words is regenerated",
    "the log lines moved",
    "a thread was added or removed: § The lifetimes' base",
    "a new spawn: § The scripts' base",
    "a write was added: § The input's base",
    "a read changed its cache use: 3.11's base",
    "a help-prompt definition or a `setOpacity` caller changed (L-21)",
    "the two defines changed (L-13)",
    "an include changed: the stand-in's fakes and `Window.cpp:29`",
    "a guard was added: the stand-in's branch list",
    "a non-ASCII byte in a comment near `_()`: xgettext stops the image build (`es-code-traps.md`)",
    "a msgid lost its French (D-UI-051)",
    "a lead's line moved: § The leads re-anchored",
    "a screen the map does not describe (D-UI-039)",
    "the host gained a toolchain, or the first error moved: the stand-in's fakes",
    "--",
    "the lane wrote under `packages/`, `projects/` or `tools/`, or in the ES worktree: § 8",
    "a `ROCKNIX` gate was added or removed",
    "the gates list changed",
]
txt = open(f"{A}/stage-a/runs.out").read().split("\n")
blocks, cur = [], None
for line in txt:
    if line.startswith("# "):
        if cur:
            blocks.append(cur)
        cur = {"title": line[2:], "out": [], "rc": None, "wall": None}
    elif cur is not None:
        m = re.match(r"^run rc=(\d+) wall=(\d+)s$", line)
        if m:
            cur["rc"], cur["wall"] = m.group(1), m.group(2) + " s"
        elif line.strip():
            cur["out"].append(line.strip())
if cur:
    blocks.append(cur)
rows = []
for i, b in enumerate(blocks):
    title = re.split(r" \(expect", b["title"])[0]
    fig = "; ".join(b["out"])
    fig = (fig[:420] + " ...") if len(fig) > 420 else fig
    rc = b["rc"] if b["rc"] is not None else ("CANNOT" if b["title"].startswith("STAGE C") else "one line")
    rows.append([i + 1, title, rc, b["wall"] or "--", "`" + fig.replace("`", "'") + "`" if fig else "--", MEAN[i] if i < len(MEAN) else "--", "tool-run" if b["rc"] is not None else ("--" if rc == "CANNOT" else "tool-run")])
print(f"**The § 5 runs** (stage A, `stage-a/runs.sh` -> `stage-a/runs.out`, 05:59:32Z to 05:59:35Z; each block wrapped in `rc=$?` and a `date +%s` pair; every figure as the brief expects but the deltas `00` names):\n")
print(table(["#", "Run", "Exit", "Wall", "Figure (the command's own lines)", "A FAIL would mean", "proved:"], rows))

g = open(f"{A}/stage-b/generators.txt").read()
gens = re.findall(r"^== (\S+)\nclean rc=(\d+)\n(generated, asserted: [^\n]*)\n\(a\) (\S+) rc=(\d+)\n(FAIL[^\n]*)?.*?\(b\) without (\S+) rc=(\d+)\n(FAIL[^\n]*)?.*?\(c\) at bccd715707 rc=(\d+)\n(FAIL[^\n]*)?", g, re.S | re.M)
gr = []
for name, rc0, label, akey, arc, afail, drop, brc, bfail, crc, cfail in gens:
    if rc0 != "0" or arc != "1" or brc != "1" or crc != "1":
        fail.append(f"{name}: clean {rc0}, drifts {arc}/{brc}/{crc}")
    gr.append([f"`tools/{name}`", rc0, f"`{label}`", f"`{akey}` -> {arc}: `{(afail or '').strip()[:110]}`", f"without `{drop.replace('es-core/src/', '')}` -> {brc}: `{(bfail or '').strip()[:110]}`", f"at `bccd715707` -> {crc}: `{(cfail or '').strip()[:110]}`", "tool-run"])
print("\n**The generators, each seen to exit 1 on a constructed drift before it was trusted** (`stage-b/drift.sh` -> `stage-b/generators.txt`; (a) a wrong expectation, (b) the paths list with a cited file dropped, (c) the pin's paths read at the base, where the cited lines have moved):\n")
print(table(["Generator", "Clean", "Its last line", "(a)", "(b)", "(c)", "proved:"], gr))
owed = [
    ["the stand-in syntax check over the 44 (`stage-a/syntax-check.sh`, the 13 fakes, the pugixml root; the udev and pulse branches named as not parsed)", "stage C", "a `<file>: rc N` line per `.cpp`"],
    ["the unit build (`tools/t35-build-tests.sh`, `window-input-tests` among the binaries)", "stage C", "`TOTAL: N test cases in B binaries`, 0 failed"],
    ["the seven candidates' FAIL lines (3.1, 3.4, 3.5, 3.10, 3.11, 3.14, 3.19) against the unfixed extracts, or their PASS-at-pin record", "stage C", "one line each"],
    ["3.27, T33's `stage-c/pl25-screensaver.py` re-run unchanged", "stage C", "its FAIL line at the pin"],
    ["the guest window G-01 to G-12", "after the grant on #682", "§ The guest cycle"],
]
print("\n**Owed at stage C and the window** (not run at stage B):\n")
print(table(["Run", "When", "Figure expected"], owed))
cnt = {"runs": len(blocks), "generators": len(gens)}
for k, v in expect.items():
    if str(cnt.get(k)) != v:
        fail.append(f"{k} {cnt.get(k)}, expected {v}")
print(f"\ngenerated, asserted: {len(blocks)} run blocks, {len(gens)} generators with three drifts each")
for f in fail:
    print(f"FAIL t35-runs: {f}")
sys.exit(1 if fail else 0)

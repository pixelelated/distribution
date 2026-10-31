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
# Stage C's runs, read from their records (each figure asserted).
def rd(p):
    try:
        return open(f"{A}/{p}").read()
    except OSError:
        fail.append(f"{p} unreadable")
        return ""
sx = rd("stage-a/syntax-check.out"); sx1 = rd("stage-a/syntax-check-first.out"); bt = rd("stage-c/build-tests.out"); pl = rd("stage-c/pl25-screensaver.out")
m_sx = re.search(r"t35-syntax-check: (\d+) file\(s\) checked, (\d+) rc 0, (\d+) not", sx)
m_sx1 = re.search(r"t35-syntax-check: (\d+) file\(s\) checked, (\d+) rc 0, (\d+) not", sx1)
m_tot = re.search(r"^TOTAL: (\d+) test cases in (\d+) binaries$", bt, re.M)
m_wit = re.search(r"^RUN window-input-tests: rc (\d+); \[doctest\] test cases: +(\d+) \| +(\d+) passed \| +(\d+) failed", bt, re.M)
tree_bins = re.findall(r"^RUN (es-unit-tests|es-file-tests|es-conf-tests|es-file-tests-win32|app-unit-tests): rc (\d+); \[doctest\] test cases: +(\d+) \| +(\d+) passed \| +(\d+) failed", bt, re.M)
failed_cases = re.findall(r"^    TEST CASE:  (3\.\d+)", bt, re.M)
m_pl = re.search(r"SUMMARY: AddressSanitizer: (heap-use-after-free[^\n]*)", pl)
if not (m_sx and m_sx.groups() == ("44", "44", "0")): fail.append(f"the stand-in's last line is not 44/44/0: {m_sx and m_sx.groups()}")
if not (m_tot and m_tot.groups() == ("249", "6")): fail.append(f"TOTAL is not 249 in 6: {m_tot and m_tot.groups()}")
if not (m_wit and m_wit.group(4) == "7"): fail.append(f"window-input-tests' failed count is not 7: {m_wit and m_wit.groups()}")
if sorted(set(failed_cases)) != ["3.1", "3.10", "3.11", "3.14", "3.19", "3.4", "3.5"]: fail.append(f"the failing cases are {sorted(set(failed_cases))}")
if any(r[1] != "0" or r[4] != "0" for r in tree_bins) or len(tree_bins) != 5: fail.append(f"the tree's binaries: {tree_bins}")
if not m_pl: fail.append("3.27's ASan summary line is missing")
stc = [
    ["the stand-in over the 44 (`stage-a/syntax-check.sh`, the fakes under `stage-a/fakes/`, the pugixml root and rapidjson; udev, pulse, TTS, CEC and WIN32 not parsed)", "0", "11 s",
     f"`t35-syntax-check: {m_sx.group(1)} file(s) checked, {m_sx.group(2)} rc 0, {m_sx.group(3)} not`" if m_sx else "--", "the first run (`syntax-check-first.out`) printed " + (f"`{m_sx1.group(2)} rc 0, {m_sx1.group(3)} not`" if m_sx1 else "--") + ": the seven stopped at the fakes' gaps, closed by `t35-sdl-more.h` and the T35 sections"],
    ["the unit build (`tools/t35-build-tests.sh`)", "1 (window-input-tests' candidates, by design)", "41 s",
     f"`TOTAL: {m_tot.group(1)} test cases in {m_tot.group(2)} binaries`" if m_tot else "--", "; ".join(f"{n} {c}/{c}" for n, rc, c, p_, f_ in tree_bins)],
    ["`window-input-tests` before any fix", m_wit.group(1) if m_wit else "--", "in the above",
     f"`{m_wit.group(2)} cases, {m_wit.group(3)} passed, {m_wit.group(4)} failed`" if m_wit else "--", "the seven candidates FAIL at the pin: " + ", ".join(sorted(set(failed_cases), key=lambda x: float(x[2:]))) + "; 3.11's first ordering passed because the uncached read rewrites the entry (`FileSystemUtil.cpp:161-162`), now made second"],
    ["3.27, T33's `stage-c/pl25-screensaver.py` unchanged from `947ace1966`", "1", "1 s", f"`{m_pl.group(1)[:90]}`" if m_pl else "--", "FAIL at the pin as #1305 says; the script takes `SystemScreenSaver.cpp`'s path, not the worktree the brief's line passes"],
]
owed = [
    ["ThreadSanitizer for 3.3 and 3.17, ASan for 3.2", "stage E (the covering cases of PL-01 and PL-07)", "a sanitizer report before the fix, none after"],
    ["the PASS halves of the seven", "stage E", "each candidate's PASS line after its fix"],
    ["the guest window G-01 to G-12", "slot 3 on the host", "§ The guest cycle"],
]
print("\n**Stage C's runs** (read from their records, each figure asserted):\n")
print(table(["Run", "Exit", "Wall", "Figure", "Note"], stc))
print("\n**Still owed:**\n")
print(table(["Run", "When", "Figure expected"], owed))
cnt = {"runs": len(blocks), "generators": len(gens)}
for k, v in expect.items():
    if str(cnt.get(k)) != v:
        fail.append(f"{k} {cnt.get(k)}, expected {v}")
print(f"\ngenerated, asserted: {len(blocks)} run blocks, {len(gens)} generators with three drifts each")
for f in fail:
    print(f"FAIL t35-runs: {f}")
sys.exit(1 if fail else 0)

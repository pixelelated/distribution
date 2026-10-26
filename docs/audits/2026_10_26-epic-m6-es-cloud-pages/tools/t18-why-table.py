"""T18 (#665): the why table, generated from the two lists.

    python3 -I -B docs/audits/2026_10_26-epic-m6-es-cloud-pages/tools/t18-why-table.py \
        <es tree> <pin> <distribution rev>        (from the distribution worktree)

The ES rows are CloudText::whySentences at the pin (the first string of each
pair). The scripts' side is every ">>> why" the cloud scripts and backuptool
print at the distribution rev: the literal emitters (echo ">>> why ...",
say_why "...", why "...") and the variable ones (say_why "$x", why "$x"),
expanded through what can fill them -- each script's why_for table, the
connection layer's selection_reason, cloud_saves_root's own literals
(relayed), and the stamps' offline why. Every count is asserted against what
stage A read (r13): a drift exits 1 and names the count, so the table cannot
quietly describe other trees. Writes markdown on stdout. Exit 2 when a tree
cannot be read.
"""
import re
import subprocess
import sys

ES, PIN, REV = sys.argv[1:4]
SCRIPT_DIRS = ["projects/ROCKNIX/packages/network/rclone/sources",
               "projects/ROCKNIX/packages/rocknix/sources/scripts",
               "projects/ROCKNIX/packages/network/raofflineproxy/sources"]
EXPECT = {"es_rows": 38, "es_unique": 38, "literal": 34, "shared_literal": 32,
          "script_only": 2, "es_only_literal": 6, "variable_lines": 17,
          "es_only_unproduced": 1}


def git(*args, cwd=None):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write("t18-why-table: git %s failed: %s\n" % (" ".join(args), r.stderr.strip()))
        sys.exit(2)
    return r.stdout


def es_rows():
    text = git("-C", ES, "show", PIN + ":es-app/src/CloudText.cpp").splitlines()
    start = next(i for i, l in enumerate(text) if "whySentences()" in l and "{" not in l.split("whySentences()")[0] and not l.strip().startswith("//"))
    rows = []
    for i in range(start, len(text)):
        if text[i].strip() == "};" and rows:
            break
        m = re.match(r'\s*\{ "([^"]+)", _\("([^"]+)"\) \},', text[i])
        if m:
            rows.append((m.group(1), i + 1, m.group(1) == m.group(2)))
    return rows


def script_files():
    out = git("ls-tree", "-r", "--name-only", REV, "--", *SCRIPT_DIRS)
    return [p for p in out.split("\n") if p]


LIT = re.compile(r'''(?:echo ">>> why ([A-Z][^"$]*)"|say_why "([A-Z][^"$]*)"|\bwhy "([A-Z][^"$]*)")''')
VAR = re.compile(r'''(?:say_why "\$|\bwhy "\$)''')


def scan():
    literal, variable, why_for, selection, stamp = {}, [], {}, [], []
    for path in script_files():
        lines = git("show", "%s:%s" % (REV, path)).split("\n")
        name = path.rsplit("/", 1)[-1]
        in_why_for = False
        for n, line in enumerate(lines, 1):
            s = line.strip()
            if s.startswith("#"):
                continue
            if re.match(r"why_for\(\)\s*\{", s):
                in_why_for = True
            elif in_why_for and s == "}":
                in_why_for = False
            if in_why_for:
                for w in re.findall(r'echo "([A-Z][^"]*)"', line):
                    why_for.setdefault(w, []).append("%s:%d" % (name, n))
                continue
            for m in LIT.finditer(line):
                w = next(g for g in m.groups() if g)
                literal.setdefault(w.rstrip(), []).append("%s:%d" % (name, n))
            if VAR.search(line):
                variable.append("%s:%d" % (name, n))
            if "gaps YOU WENT OFFLINE PART-WAY THROUGH" in line:
                stamp.append("%s:%d" % (name, n))
            if name == "cloud_connections.py":
                for w in re.findall(r'"([A-Z][A-Z \'.,-]+)"', line):
                    if "selection_reason" in "".join(lines[max(0, n - 6):n]):
                        selection.append((w, "%s:%d" % (name, n)))
    return literal, variable, why_for, selection, stamp


def main():
    rows = es_rows()
    es = {r[0]: r for r in rows}
    literal, variable, why_for, selection, stamp = scan()
    sel = {w: where for w, where in selection}
    counts = {
        "es_rows": len(rows),
        "es_unique": len(es),
        "literal": len(literal),
        "shared_literal": len(set(es) & set(literal)),
        "script_only": len(set(literal) - set(es)),
        "es_only_literal": len(set(es) - set(literal)),
        "variable_lines": len(variable),
    }
    produced = set(literal) | set(why_for) | set(sel) | ({"YOU WENT OFFLINE PART-WAY THROUGH"} if stamp else set())
    unproduced = sorted(set(es) - produced)
    counts["es_only_unproduced"] = len(unproduced)
    drift = [k for k, v in EXPECT.items() if counts[k] != v]
    mismatched = [r[0] for r in rows if not r[2]]

    print("| # | Sentence | ES row (`CloudText.cpp`) | Literal emitters at `%s` | Filled by a variable emitter | Status |" % REV[:10])
    print("| ---: | --- | --- | --- | --- | --- |")
    union = sorted(set(es) | set(literal), key=lambda w: (es[w][1] if w in es else 10 ** 6, w))
    for i, w in enumerate(union, 1):
        filled = []
        if w in why_for:
            filled.append("`why_for` " + ", ".join(why_for[w]))
        if w in sel:
            filled.append("`selection_reason` " + sel[w])
        if w == "YOU WENT OFFLINE PART-WAY THROUGH" and stamp:
            filled.append("the stamp's why " + ", ".join(stamp))
        if w in es and w in literal:
            status = "shared"
        elif w in es and filled:
            status = "ES row; filled by a variable emitter"
        elif w in es:
            status = "**ES-only: no producer at the rev**"
        else:
            status = "**script-only: no ES row**"
        print("| %d | `%s` | %s | %s | %s | %s |" % (
            i, w, (":%d" % es[w][1]) if w in es else "--",
            ", ".join(literal.get(w, [])) or "--", "; ".join(filled) or "--", status))
    print()
    print("Counts: " + ", ".join("%s %d (expected %d)" % (k, counts[k], EXPECT[k]) for k in EXPECT))
    print("Variable emitter lines: " + ", ".join(variable))
    print("ES-only with no producer: " + (", ".join("`%s`" % w for w in unproduced) or "none"))
    print("Pairs whose two spellings differ: " + (", ".join(mismatched) or "none"))
    drift += fallback_map(why_for)
    drift += lock_held_wordings(literal)
    if drift or mismatched:
        sys.stderr.write("t18-why-table: DRIFT %s\n" % ", ".join(
            "%s=%d" % (k, counts[k]) if k in counts else k for k in drift))
        sys.exit(1)


def fallback_map(why_for):
    """whyForCode's words beside cloud_backup's why_for, the header comment
    above it and the rule's sentence, one row per code group."""
    code = git("-C", ES, "show", PIN + ":es-app/src/ThreadedCloudSync.cpp").splitlines()
    head = git("-C", ES, "show", PIN + ":es-app/src/ThreadedCloudSync.h").splitlines()
    text = open(".claude/rules/es-player-text.md").read()
    # The rule's rc-keyed sentence alone: "**Why** comes from ..." to the blank line.
    at = text.index("**Why** comes from")
    rule = text[at:text.index("\n\n", at)]
    start = next(i for i, l in enumerate(code) if l.startswith("std::string ThreadedCloudSync::whyForCode"))
    es = {}
    for i in range(start, start + 20):
        m = re.match(r'\s*((?:case [A-Za-z0-9:]+: ?)+|default:)\s*return _\("([^"]+)"\);', code[i])
        if m:
            es[m.group(1).replace("case ", "").replace(":", "").replace("CloudExit", "").strip()] = (m.group(2), i + 1)
    comment = " ".join(l.strip().lstrip("/ ") for l in head[92:99])
    print()
    print("**The fallback map** (`ThreadedCloudSync::whyForCode` at the pin; `why_for` in the scripts; the header comment `ThreadedCloudSync.h:93-99`; `es-player-text.md` § Outcome vocabulary's **Why** sentence):")
    print()
    print("| Code | Code says (`ThreadedCloudSync.cpp`) | Scripts' `why_for` | Header comment | Rule |")
    print("| --- | --- | --- | --- | --- |")
    groups = [("3 4", ["3", "4"], "YOUR CLOUD FOLDER WASN'T FOUND"), ("5 124", ["5", "124"], "YOUR CLOUD STOPPED ANSWERING"),
              ("7 8", ["7", "8"], "YOUR CLOUD REFUSED THE TRANSFER"), ("Stopped", ["130"], "IT WAS STOPPED"),
              ("default", ["*"], "SOMETHING WENT WRONG")]
    bad = 0
    for key, codes, rule_words in groups:
        said, line = es.get(key, ("(missing)", 0))
        sw = {"3 4": "COULDN'T FIND YOUR CLOUD FOLDER", "5 124": "YOUR CLOUD STOPPED ANSWERING",
              "7 8": "YOUR CLOUD WOULDN'T TAKE THE FILES", "Stopped": "IT WAS STOPPED",
              "default": "SOMETHING WENT WRONG"}[key]
        in_scripts = sw in why_for
        in_comment = said in comment
        in_rule = said in rule
        rule_has_old = rule_words in rule
        print("| %s | `%s` (:%d) | %s | %s | %s |" % (
            key, said, line, ("`%s`" % sw) if in_scripts else "**absent**",
            "same" if in_comment else "**differs** (names something else)",
            "same" if in_rule else ("**differs**: says `%s` (#909)" % rule_words if rule_has_old else "**absent** (#909)")))
        bad += 0 if said == sw else 1
    return ["fallback_map_vs_scripts=%d" % bad] if bad else []


def lock_held_wordings(literal):
    """Every wording exit 75 is given: the scripts' whys and the eight's words."""
    eight = ["es-app/src/CloudText.cpp", "es-app/src/ThreadedCloudSync.cpp", "es-app/src/guis/GuiCloudTransfer.cpp"]
    rows = []
    for path in eight:
        for n, l in enumerate(git("-C", ES, "show", PIN + ":" + path).splitlines(), 1):
            for w in re.findall(r'_\("([^"]*(?:ALREADY RUNNING|IS RUNNING|CURRENT CLOUD TASK)[^"]*)"\)', l):
                rows.append((w, "%s:%d" % (path.rsplit("/", 1)[-1], n)))
    for w, where in literal.items():
        if "RUNNING" in w:
            rows.append((w, ", ".join(where) + " (a script's `>>> why`)"))
    print()
    print("**Exit 75's wordings** (every string the eight and the scripts give a held lock):")
    print()
    print("| Wording | Where |")
    print("| --- | --- |")
    for w, where in rows:
        print("| `%s` | %s |" % (w, where))
    print()
    distinct = len({w for w, _ in rows})
    print("Distinct wordings: %d (expected 8)" % distinct)
    return [] if distinct == 8 else ["lock_held_wordings=%d" % distinct]


main()

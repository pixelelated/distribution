"""include.py <file.md> ...: expand each include marker in an audit note (T38, #685).

A marker is a line of its own:

    <!-- include: <path> [lang <word>] [match <regex>] [from <regex>] [to <regex>] -->

<path> is relative to the audit folder (the note's own directory). The marker is kept and is
followed by a fenced block holding that file's lines -- all of them, those matching `match`,
or those from the first line matching `from` up to and including the first later line matching
`to` -- so a tool's output reaches the notes copied by a program, never retyped. A fenced block
already under a marker is replaced, so the expansion can be re-run. Exits 1, writing nothing,
when a path is missing, a pattern selects no line, or a selected line holds a fence."""
import re
import sys
from pathlib import Path

MARK = re.compile(r"^<!-- include: (\S+)(.*) -->$")


def options(rest):
    """' lang bash match ^x' -> {'lang': 'bash', 'match': '^x'}; a regex holds no ' lang ',
    ' match ', ' from ' or ' to '."""
    if not rest:
        return {}
    parts = re.split(r" (lang|match|from|to) ", rest)
    if parts[0] != "" or len(parts) % 2 != 1:
        sys.exit(f"include.py: cannot read the options {rest!r}")
    return dict(zip(parts[1::2], parts[2::2]))


def select(lines, opts):
    if "match" in opts:
        rx = re.compile(opts["match"])
        return [l for l in lines if rx.search(l)]
    if "from" in opts:
        rf, rt = re.compile(opts["from"]), re.compile(opts["to"]) if "to" in opts else None
        out = []
        for l in lines:
            if not out and not rf.search(l):
                continue
            out.append(l)
            if rt and len(out) > 1 and rt.search(l):
                break
        return out
    return lines


def expand(md):
    base = md.parent
    src = md.read_text().split("\n")
    out, i, n = [], 0, 0
    while i < len(src):
        line = src[i]
        out.append(line)
        i += 1
        m = MARK.match(line)
        if not m:
            continue
        n += 1
        opts = options(m.group(2))
        path = base / m.group(1)
        if not path.is_file():
            sys.exit(f"include.py: {md}: {m.group(1)} is not a file")
        body = select(path.read_text().rstrip("\n").split("\n"), opts)
        if not body:
            sys.exit(f"include.py: {md}: {line} selects no line")
        if any(l.startswith("```") for l in body):
            sys.exit(f"include.py: {md}: {m.group(1)} holds a fence line")
        if i < len(src) and src[i].startswith("```"):
            j = i + 1
            while j < len(src) and not src[j].startswith("```"):
                j += 1
            i = j + 1
        out.append("```" + opts.get("lang", "text"))
        out.extend(body)
        out.append("```")
    return "\n".join(out), n


results = []
for arg in sys.argv[1:]:
    md = Path(arg)
    text, n = expand(md)
    results.append((md, text, n))
for md, text, n in results:
    md.write_text(text)
    print(f"include.py: {md}: {n} marker(s) expanded")

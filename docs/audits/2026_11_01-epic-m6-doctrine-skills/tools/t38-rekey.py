"""t38-rekey.py: T38 (#685) stage E. Move the allowlists' exact-line entries with their lines (t38-streams.md
§ The rules every stream keeps: "an edit that moves lines above an allowlisted key re-keys the entries that moved").

    python3 -I t38-rekey.py <parent-export> <worktree> <allow-file> ...

For every `<path>:<N> <class> <reason>` entry whose file differs between the parent's export and the worktree,
the entry's line is found again by its text:
  - one match:  re-keyed to it (printed `rekeyed`);
  - none:       dropped (printed `dropped`): the fix rewrote the finding's line, and the checker then shows
                whether anything it excused still fails;
  - two or more: a refusal (exit 2), nothing written, since a guess could excuse the wrong line.
`*` and named keys (a contract item) never move. Files are rewritten in place only when every entry resolved.
"""
import pathlib, re, sys

parent, work, files = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3:]
if not files:
    sys.exit("t38-rekey: refused: no allowlist named")
ENTRY = re.compile(r"^(\S+):(\d+)(\s.*)$")
out, notes, refusals = {}, [], []
for f in files:
    lines = pathlib.Path(f).read_text().splitlines()
    new = []
    for raw in lines:
        m = ENTRY.match(raw)
        if not m or raw.startswith("#"):
            new.append(raw)
            continue
        path, n, rest = m.group(1), int(m.group(2)), m.group(3)
        a, b = parent / path, work / path
        if not a.is_file() or not b.is_file():
            new.append(raw)
            continue
        old_text, new_text = a.read_text().splitlines(), b.read_text().splitlines()
        if old_text == new_text:
            new.append(raw)
            continue
        if n < 1 or n > len(old_text):
            refusals.append(f"{f}: {path}:{n} is past the parent's {len(old_text)} lines")
            continue
        want = old_text[n - 1]
        hits = [i + 1 for i, t in enumerate(new_text) if t == want]
        if len(hits) == 1:
            if hits[0] != n:
                notes.append(f"rekeyed {pathlib.Path(f).name}: {path}:{n} -> :{hits[0]}")
            new.append(f"{path}:{hits[0]}{rest}")
        elif not hits:
            notes.append(f"dropped {pathlib.Path(f).name}: {path}:{n} (its line is gone)")
        else:
            refusals.append(f"{f}: {path}:{n} matches {len(hits)} lines {hits[:6]}")
            new.append(raw)
    out[f] = new
if refusals:
    for r in refusals:
        print("t38-rekey: refused: " + r)
    sys.exit(2)
for f, new in out.items():
    pathlib.Path(f).write_text("\n".join(new) + "\n")
for x in notes:
    print(x)
print(f"t38-rekey: {len(notes)} entr{'y' if len(notes) == 1 else 'ies'} moved or dropped")

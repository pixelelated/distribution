"""Count the GuiMsgBox calls with three buttons and none named exactly OK or NO (T35 #682,
stage E S1, ruling 5; the brief's § Figures not found, item 10). Each `new GuiMsgBox(`
call at <ref> is split into its top-level arguments (brackets, braces, string
literals and comments respected); the names are arguments 3, 5 and 7, as the constructors in
`guis/GuiMsgBox.h:23-37` order them. A name is "OK" or "NO" only when the argument is
exactly `_("OK")` or `_("NO")`, the comparison `GuiMsgBox.cpp:125` makes after `_()`.
Back then binds the last button (`:132-133`), which the row prints. Two-button calls with
neither name are counted on a second line (NEW DRIVE DETECTED without an id is one).
    t35-msgbox-count.py <ES worktree> <ref> <paths.txt | -> [prefix ...]
With `-`, the files are every `.cpp` under the prefixes (es-app's count for #1344)."""
import re
import subprocess
import sys

W, REF, PATHS = sys.argv[1:4]
PREFIXES = sys.argv[4:]
if PATHS == "-":
    out = subprocess.run(["git", "-C", W, "ls-tree", "-r", "--name-only", REF, "--", *PREFIXES],
                         capture_output=True, text=True, check=True).stdout.split()
    files = [f for f in out if f.endswith(".cpp")]
else:
    files = [l.strip() for l in open(PATHS) if l.strip().endswith(".cpp")]


def args_of(text, i):
    """The top-level arguments of the call whose '(' is at text[i]."""
    depth, j, start, out, q = 0, i, i + 1, [], None
    while j < len(text):
        c = text[j]
        if q:
            if c == "\\":
                j += 2
                continue
            if c == q:
                q = None
        elif text.startswith("//", j):
            j = text.find("\n", j)
            if j < 0:
                return None
            continue
        elif text.startswith("/*", j):
            j = text.find("*/", j)
            if j < 0:
                return None
            j += 2
            continue
        elif c in "\"'":
            q = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                out.append(text[start:j].strip())
                return out
        elif c == "," and depth == 1:
            out.append(text[start:j].strip())
            start = j + 1
        j += 1
    return None


rows, three, unsafe, two, two_unsafe = [], 0, 0, 0, 0
for f in files:
    r = subprocess.run(["git", "-C", W, "show", f"{REF}:{f}"], capture_output=True, text=True, errors="replace")
    if r.returncode:
        sys.exit(f"t35-msgbox-count: {f} not at {REF}")
    text = r.stdout
    for m in re.finditer(r"new\s+GuiMsgBox\s*\(", text):
        a = args_of(text, m.end() - 1)
        if a is None:
            sys.exit(f"t35-msgbox-count: unbalanced call at {f}:{text.count(chr(10), 0, m.start()) + 1}")
        # (window, text, name, func, ...[, icon]): the buttons are (len - 2) // 2, so a
        # trailing icon is never read as a name
        names = [a[2 + 2 * k] for k in range(min(3, (len(a) - 2) // 2))]
        line = text.count("\n", 0, m.start()) + 1
        safe = any(n in ('_("OK")', '_("NO")') for n in names)
        if len(names) == 2:
            two += 1
            if not safe:
                two_unsafe += 1
                rows.append(f"{f}:{line}  {' / '.join(names)}  -> back: {names[-1]} (two buttons)")
            continue
        if len(names) < 3:
            continue
        three += 1
        if not safe:
            unsafe += 1
        rows.append(f"{f}:{line}  {' / '.join(names)}  -> back: {'the first OK/NO' if safe else names[-1]}")
for row in rows:
    print(row)
print(f"t35-msgbox-count: {len(files)} file(s) at {REF[:10]}; {three} GuiMsgBox call(s) with three buttons, {unsafe} with none named OK or NO")
print(f"t35-msgbox-count: {two} with two buttons, {two_unsafe} with neither named OK or NO")

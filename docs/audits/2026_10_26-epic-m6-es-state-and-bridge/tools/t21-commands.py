#!/usr/bin/env python3
"""T21 (#668): 02 § The commands, generated from ApiSystem.cpp at the pin.

    python3 -I -B t21-commands.py <es worktree> <distribution worktree> [--expect N]

One row per command-running call in es-app/src/ApiSystem.cpp at 16dbac5211:
every executeScript(, executeEnumerationScript(, executeScriptLegacy(,
popen( and system( outside the four executors' own definitions and outside
comments. Each row: the line, the function it is in, the executor, the
command's first literal, what is joined to it from outside the literal and
how it is quoted, how the output and the exit are read, the thread (every
executor runs on its caller's: ApiSystem has none of its own), whether the
`#if WIN32` branch holds it, and whether the script it names ships at
8ebaf8daad (a file of that name under projects/ or packages/, or a busybox
or coreutils name).

Prints a Markdown table on stdout. Exits 1 when the row count differs from
--expect (the drift the brief asks the generator to catch), 2 on a usage error.
"""
import re, subprocess, sys

es, dist = sys.argv[1], sys.argv[2]
expect = int(sys.argv[sys.argv.index("--expect") + 1]) if "--expect" in sys.argv else None
PIN, BASE = "16dbac5211", "8ebaf8daad"
src = subprocess.run(["git", "-C", es, "show", f"{PIN}:es-app/src/ApiSystem.cpp"], capture_output=True, text=True, check=True).stdout.split("\n")
shipped = set(p.rsplit("/", 1)[-1] for p in subprocess.run(["git", "-C", dist, "ls-tree", "-r", "--name-only", BASE, "--", "projects", "packages"],
                                                           capture_output=True, text=True, check=True).stdout.split("\n") if p)
# Commands the image has as busybox applets or base tools, not as package files.
BASE_TOOLS = {"echo", "printf", "uname", "cat", "sh", "timeout", "ping", "tr", "grep", "awk", "md5sum", "/usr/bin/sh"}
WRAPPERS = {"timeout", "/usr/bin/sh", "sh"}
# Built by a package rather than shipped as a file of that name: whether the
# image has it is the window's `ls /usr/bin`, never a "no" from the tree.
BINARIES = {"7zr", "pdftoppm", "pdfinfo", "kodi", "evmapy", "wlr-randr", "filemanagerlauncher", "md5sum"}

# Where each line sits: the enclosing function, and inside #if WIN32 or not.
func_of, win32_of = {}, {}
cur, depth, stack = "", 0, []
for i, line in enumerate(src, 1):
    s = line.strip()
    m = re.match(r"^[A-Za-z_][\w:<>,\s\*&]*\s+\*?ApiSystem::(\w+)\s*\(", line)
    if m and depth == 0:
        cur = m.group(1)
    if s.startswith("#if"):
        stack.append("WIN32" in s and "!WIN32" not in s and "!" not in s.split("WIN32")[0][-2:])
    elif s.startswith("#else") and stack:
        stack[-1] = not stack[-1]
    elif s.startswith("#endif") and stack:
        stack.pop()
    depth += line.count("{") - line.count("}")
    func_of[i] = cur
    win32_of[i] = any(stack)

EXEC = re.compile(r"\b(executeScript|executeEnumerationScript|executeScriptLegacy|popen|system)\s*\(")
DEFS = {"executeEnumerationScript", "executeScriptLegacy", "executeScript"}
rows = []
for i, line in enumerate(src, 1):
    code = line.split("//", 1)[0]
    if not EXEC.search(code) or code.strip().startswith(("*", "/*", "#define")):
        continue
    for m in EXEC.finditer(code):
        name = m.group(1)
        # the executors' own bodies run popen/system on `command`: those are the executors, not call sites
        if func_of[i] in DEFS and name in ("popen", "system"):
            continue
        if re.search(r"^\s*(std::|virtual|static|bool|int|void)", code) and "ApiSystem::" + name in code:
            continue
        call = code[m.end():]
        # the call may run onto the next lines: take until the parentheses close
        j, text = i, call
        while text.count("(") + 1 > text.count(")") and j < len(src):
            text += " " + src[j].split("//", 1)[0].strip(); j += 1
        # A command built in a variable first (cmd, command, oss.str(),
        # updatecommand): read its assignment above the call, in the function.
        var = re.match(r"\s*([A-Za-z_]\w*)(?:\.str\(\)\.c_str\(\)|\.c_str\(\)|\.str\(\))?\s*[,)]", text)
        if var and not re.match(r'\s*"', text):
            name_v = var.group(1)
            for k in range(i - 1, max(0, i - 12), -1):
                prev = src[k - 1].split("//", 1)[0]
                if func_of.get(k) != func_of[i]:
                    break
                if re.search(r"\b" + re.escape(name_v) + r"\s*(=|<<)\s*", prev):
                    text = prev[re.search(r"\b" + re.escape(name_v) + r"\s*(=|<<)\s*", prev).end():] + " " + text
                    if name_v == "oss":
                        continue
                    break
        lits = re.findall(r'"((?:[^"\\]|\\.)*)"', text)
        first = lits[0] if lits else ""
        joined = re.findall(r"(?:\+|<<)\s*([A-Za-z_][\w:\.\->\(\)]*)", text)
        joined = [x for x in joined if not x.startswith(("std::string", "std::to_string", "_("))]
        if not joined and not lits:
            quoting, args = "a variable: the command built earlier", re.match(r"\s*([\w\.]+)", text).group(1)
        elif not joined:
            quoting, args = "none joined", "-"
        else:
            args = ", ".join(sorted(set(joined)))
            if "shellQuote" in text:
                quoting = "shellQuote"
            elif re.search(r'\\"\s*"\s*\+\s*[A-Za-z_]', text) or re.search(r'\\"\s*\+', text):
                quoting = "double quotes"
            elif re.search(r"'\"\s*(?:\+|<<)\s*[A-Za-z_]", text):
                quoting = "single quotes"
            else:
                quoting = "bare"
        out = {"executeEnumerationScript": "every line, 1023-byte pieces", "executeScript": "the lines to func, the last as result" if "," in text.split(")")[0] or "[&" in text else "none (system)",
               "executeScriptLegacy": "every line to func", "popen": "fgets in the caller", "system": "none (inherits stdout)"}[name]
        ext = {"executeEnumerationScript": "discarded (:2251)", "executeScript": "WEXITSTATUS without WIFEXITED (:2319)" if out.startswith("the lines") else "system() == 0 (:2328)",
               "executeScriptLegacy": "WEXITSTATUS without WIFEXITED (:2291)", "popen": "the caller's pclose", "system": "the caller's"}[name]
        if name == "popen":
            ext = "WEXITSTATUS without WIFEXITED" if any("WEXITSTATUS(pclose" in src[k - 1] and "WIFEXITED" not in src[k - 1] for k in range(i, min(i + 30, len(src)) + 1)) else "pclose, status unread"
        if name == "system" and any("WIFEXITED" in src[k - 1] for k in range(i, min(i + 6, len(src)) + 1)):
            ext = "WIFEXITED then WEXITSTATUS"
        if "getSevenZipCommand()" in text and not first.startswith("7z"):
            first = "7zr" + first   # getSevenZipCommand() returns "7zr" (ApiSystem.h:422)
        words = first.split()
        script = ""
        for w in words:
            if w in WRAPPERS or re.fullmatch(r"\d+|-\w+", w):
                continue
            script = w.strip("\\\"'")
            break
        if not script:
            present = "-"
        else:
            base = script.rsplit("/", 1)[-1]
            present = ("base tool" if script in BASE_TOOLS or base in BASE_TOOLS else "binary: the window's ls"
                       if base in BINARIES else ("yes" if base in shipped else "no"))
        rows.append((i, func_of[i], name, first.replace("|", "\\|")[:70], args.replace("|", "\\|")[:60], quoting, out, ext, "WIN32 only" if win32_of[i] else "", script or "-", present))

print("| Line | Function | Executor | First literal | Joined from outside | Quoting | Output read | Exit read | Thread | Branch | Script | Ships at 8ebaf8daad |")
print("| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for r in rows:
    i, f, n, lit, args, q, out, ext, br, sc, pr = r
    print(f"| {i} | `{f}` | `{n}` | `{lit}` | {args} | {q} | {out} | {ext} | the caller's | {br} | `{sc}` | {pr} |")
from collections import Counter
print()
print(f"{len(rows)} rows. Quoting: " + ", ".join(f"{k} {v}" for k, v in Counter(r[5] for r in rows).most_common())
      + ". Scripts not shipped at 8ebaf8daad: " + str(sum(1 for r in rows if r[10] == "no")) + " rows.")
if expect is not None and len(rows) != expect:
    print(f"DRIFT: {len(rows)} rows, expected {expect}", file=sys.stderr)
    sys.exit(1)

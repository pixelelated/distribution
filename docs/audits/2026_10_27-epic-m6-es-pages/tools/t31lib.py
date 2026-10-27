"""Shared readers for T31's generators (#678): a C++ call's top-level arguments,
read by balanced brackets with strings, chars and comments skipped, and a
file at a commit."""
import re
import subprocess


def show(tree, commit, path):
    return subprocess.run(["git", "-C", tree, "show", "%s:%s" % (commit, path)],
                          capture_output=True, text=True, check=True).stdout


def skip(src, i):
    """If src[i] opens a comment, string or char, return the index after it; else None."""
    if src.startswith("//", i):
        return src.index("\n", i)
    if src.startswith("/*", i):
        return src.index("*/", i) + 2
    if src[i] in "\"'":
        q = src[i]
        j = i + 1
        while src[j] != q:
            j += 2 if src[j] == "\\" else 1
        return j + 1
    return None

def call_args(src, open_paren):
    """The top-level arguments of the call whose '(' is at open_paren, and the index after ')'."""
    out, depth, start, i = [], 0, open_paren + 1, open_paren
    while True:
        j = skip(src, i)
        if j is not None:
            i = j
            continue
        c = src[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                out.append(src[start:i].strip())
                return [a for a in out if a != "" or len(out) > 1], i + 1
        elif c == "," and depth == 1:
            out.append(src[start:i].strip())
            start = i + 1
        i += 1

def in_comment_or_string(src, at):
    """Is the match at `at` inside a // comment or an open string on its line?"""
    prefix = src[src.rfind("\n", 0, at) + 1:at]
    return "//" in prefix or prefix.count('"') % 2 == 1


def literal(expr):
    """The text of _("...") or "...", else None."""
    m = re.fullmatch(r'(?:Utils::String::toUpper\()?_\("((?:[^"\\]|\\.)*)"\)\)?', expr) or re.fullmatch(r'"((?:[^"\\]|\\.)*)"', expr)
    return m.group(1) if m else None

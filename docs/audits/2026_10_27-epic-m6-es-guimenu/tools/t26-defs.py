#!/usr/bin/env python3
"""T26 (#673): the file-scope function definitions of GuiMenu.cpp at the pin
and at the merge base, and how they changed.

    python3 -I t26-defs.py <pin.cpp> <base.cpp> [--list]

The parser's rules, stated so its figures can be checked:
- Comments, string and character literals (raw strings included) are
  blanked before braces are counted.
- In a conditional (#if/#ifdef/#ifndef ... #elif/#else ... #endif) braces are
  counted in the first arm only: the file opens braces under one #if and
  closes them under another (the brief's § 2), and first-arm counting keeps
  such pairs balanced. Every arm's text still belongs to the definition that
  encloses it.
- A definition is a `{` at file scope (inside no brace but a namespace's or
  an extern block's) whose preceding text since the last `;`, `}` or
  preprocessor line has a name followed by `(` before any `=`, and is not a
  class, struct, union, enum or namespace head. Its name is the identifier
  (qualified) before that first `(`.
- Kind: `member` for `GuiMenu::name`, `static` for a definition whose text
  starts with `static`, `other-member` for another class's `X::name`, and
  `free` otherwise.
- Changed or unchanged compares the definition's whole text (signature and
  body) byte for byte after stripping trailing spaces from each line
  (`exact`); a second figure compares with all whitespace removed (`ws`).
  Overloads are told apart by their parameter text.
Exits 1 when the braces do not balance at the end of either file.
"""
import re, sys, collections

def blank(src):
    out = []; i = 0; n = len(src)
    while i < n:
        c = src[i]
        if src.startswith("//", i):
            j = src.find("\n", i); j = n if j < 0 else j
            out.append(" " * (j - i)); i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2); j = n if j < 0 else j + 2
            out.append("".join(ch if ch == "\n" else " " for ch in src[i:j])); i = j
        elif c in "\"'":
            # a raw string R"delim( ... )delim": blanked to its closing delimiter
            if c == '"' and i > 0 and src[i - 1] == "R":
                k = src.find("(", i + 1)
                close = ")" + src[i + 1:k] + '"'
                j = src.find(close, k + 1)
                if k < 0 or j < 0:
                    sys.exit("an unterminated raw string at offset %d" % i)
                j += len(close)
                out.append("".join(ch if ch == "\n" else " " for ch in src[i:j])); i = j
                continue
            j = i + 1
            while j < n and src[j] != c:
                if src[j] == "\\":
                    j += 1
                elif src[j] == "\n":
                    break
                j += 1
            out.append(c + " " * (j - i - 1) + (c if j < n else "")); i = j + 1
        else:
            out.append(c); i += 1
    return "".join(out)

HEAD = re.compile(r"^\s*(template\s*<[^>]*>\s*)?(class|struct|union|enum|namespace)\b")
NAME = re.compile(r"((?:[A-Za-z_]\w*\s*::\s*)*~?[A-Za-z_]\w*|operator\s*\S+)\s*\($")

def definitions(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    text = blank(raw)
    lines = text.split("\n")
    rawlines = raw.split("\n")
    defs = []
    stack = []          # brace kinds: 'ns' (transparent) or 'def' or 'other'
    cond = []           # per #if: True while in its first arm
    sig = ""; sig_line = None
    cur = None          # (name, kind, start line, params)
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("#"):
            d = re.match(r"#\s*(\w+)", s); d = d.group(1) if d else ""
            if d in ("if", "ifdef", "ifndef"): cond.append(True)
            elif d in ("elif", "else"):
                if cond: cond[-1] = False
            elif d == "endif":
                if cond: cond.pop()
            if not stack: sig = ""
            continue
        counting = all(cond)
        for col, ch in enumerate(line):
            if not counting:
                continue
            if ch == "{":
                file_scope = all(k == "ns" for k in stack)
                if file_scope:
                    head = sig.strip()
                    if HEAD.match(head) and re.match(r"^\s*namespace\b", head) or head.startswith('extern "C"') or head == "extern":
                        stack.append("ns")
                    elif HEAD.match(head):
                        stack.append("other")
                    else:
                        par = head.find("(")
                        eq = head.find("=")
                        m = NAME.search(head[:par + 1]) if par >= 0 else None
                        if m and (eq < 0 or eq > par):
                            name = re.sub(r"\s+", "", m.group(1))
                            kind = ("member" if name.startswith("GuiMenu::") else
                                    "static" if re.match(r"^\s*static\b", head) else
                                    "other-member" if "::" in name else "free")
                            depth = head.count("(") - head.count(")")
                            params = re.sub(r"\s+", " ", head[par:]).strip()
                            cur = (name, kind, sig_line or ln, params)
                            stack.append("def")
                        else:
                            stack.append("other")
                    sig = ""; sig_line = None
                else:
                    stack.append("inner")
            elif ch == "}":
                if not stack:
                    sys.exit("%s:%d: a closing brace with none open" % (path, ln))
                k = stack.pop()
                if k == "def" and all(x == "ns" for x in stack):
                    name, kind, start, params = cur
                    defs.append({"name": name, "kind": kind, "start": start, "end": ln, "params": params,
                                 "text": "\n".join(l.rstrip() for l in rawlines[start - 1:ln])})
                    cur = None
                if all(x == "ns" for x in stack):
                    sig = ""; sig_line = None
            elif ch == ";" and all(x == "ns" for x in stack):
                sig = ""; sig_line = None
            elif all(x == "ns" for x in stack):
                if not sig.strip() and not ch.isspace():
                    sig_line = ln
                sig += ch
        if all(x == "ns" for x in stack):
            sig += "\n"
    if stack:
        sys.exit("%s: %d brace(s) left open at the end" % (path, len(stack)))
    return defs

pin, base = definitions(sys.argv[1]), definitions(sys.argv[2])
key = lambda d: (d["name"], d["params"])
P = {key(d): d for d in pin}; B = {key(d): d for d in base}
if len(P) != len(pin) or len(B) != len(base):
    print("note: duplicate (name, parameters) keys: pin %d of %d, base %d of %d" % (len(P), len(pin), len(B), len(base)))
added = [k for k in P if k not in B]; removed = [k for k in B if k not in P]
common = [k for k in P if k in B]
changed = [k for k in common if P[k]["text"] != B[k]["text"]]
wsk = lambda t: re.sub(r"\s+", "", t)
changed_ws = [k for k in common if wsk(P[k]["text"]) != wsk(B[k]["text"])]
kinds = collections.Counter(d["kind"] for d in pin)
print("pin %d definitions %s; base %d" % (len(pin), dict(kinds), len(base)))
print("added %d, removed %d, common %d: changed %d / unchanged %d (exact), changed %d / unchanged %d (whitespace removed)"
      % (len(added), len(removed), len(common), len(changed), len(common) - len(changed), len(changed_ws), len(common) - len(changed_ws)))
print("removed:", ", ".join(k[0] for k in removed) or "none")
longest = sorted(pin, key=lambda d: d["end"] - d["start"] + 1, reverse=True)[:10]
print("the ten longest:", "; ".join("%s %d-%d (%d)" % (d["name"], d["start"], d["end"], d["end"] - d["start"] + 1) for d in longest))
if "--list" in sys.argv:
    for d in pin:
        st = "added" if key(d) in added else "changed" if key(d) in changed else "unchanged"
        print("%s\t%d\t%d\t%s\t%s" % (d["name"], d["start"], d["end"], d["kind"], st))

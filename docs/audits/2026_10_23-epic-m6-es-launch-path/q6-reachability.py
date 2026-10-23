#!/usr/bin/env python3
"""Q6 reachability: every function the ten headers declare (one line or several, inline bodies
included), every file-static function, and every preprocessor conditional of the twenty paths,
each with the number of lines elsewhere in es-app/src and es-core/src that name it."""
import re, subprocess, sys
W, PIN = sys.argv[1], sys.argv[2]
H = ["es-app/src/FileData.h","es-app/src/SystemData.h","es-app/src/LaunchCommand.h","es-app/src/ProxyCards.h",
     "es-app/src/SaveState.h","es-app/src/SaveStateRepository.h","es-app/src/SaveStateConfigFile.h",
     "es-app/src/SaveStateJobQueue.h","es-app/src/SaveStateBookkeeper.h","es-app/src/views/ViewController.h"]
C = [h.replace(".h",".cpp") for h in H if h != "es-app/src/LaunchCommand.h"] + ["es-app/src/main.cpp"]
C = [c for c in C if c != "es-app/src/ProxyCards.cpp"] + ["es-app/src/ProxyCards.cpp"]
def show(p): return subprocess.run(["git","-C",W,"show",f"{PIN}:{p}"],capture_output=True,text=True,check=True).stdout
grepcache = {}
def hits(name):
    if name not in grepcache:
        r = subprocess.run(["git","-C",W,"grep","-n","-w","-e",name,PIN,"--","es-app/src","es-core/src"],capture_output=True,text=True)
        grepcache[name] = [l.split(":",1)[1] for l in r.stdout.splitlines()]
    return grepcache[name]
KW = {"if","for","while","switch","return","sizeof","defined","catch","case"}
sig = re.compile(r'(?:^|[\s*&~:])(~?[A-Za-z_]\w*)\s*\(')
rows = []
for h in H:
    lines = show(h).splitlines(); i = 0; depth_class = []
    while i < len(lines):
        raw = lines[i]; s = raw.strip()
        if s.startswith(("#","//","/*","*")) or not s:
            i += 1; continue
        stmt, j = s, i
        # join a declaration split across lines until ; or { appears
        while not re.search(r'[;{]\s*(//.*)?$', stmt) and j + 1 < len(lines) and "(" in stmt:
            j += 1; stmt += " " + lines[j].strip()
        m = sig.search(stmt.split("{")[0] if "(" in stmt.split("{")[0] else "")
        if m and "(" in stmt and not stmt.startswith(("return","if ","else","for ","while")) and m.group(1) not in KW \
           and not re.match(r'^\s*[A-Za-z_][\w:<>]*\s*=\s*', stmt) and ")" in stmt:
            name = m.group(1)
            rows.append(("decl", h, i+1, name, stmt[:110]))
        i = j + 1
for c in C:
    for n, l in enumerate(show(c).splitlines(), 1):
        if l.startswith("static ") and "(" in l and not re.search(r'=\s*$|=\s*\{|\{\s*[0-9a-z"]', l.split("(")[0]):
            m = sig.search(l)
            if m and m.group(1) not in KW: rows.append(("static", c, n, m.group(1), l.strip()[:110]))
for p in H + C:
    for n, l in enumerate(show(p).splitlines(), 1):
        if re.match(r'^\s*#\s*(if|ifdef|ifndef|else|elif)\b', l): rows.append(("pp", p, n, "", l.strip()))
out = []
for kind, path, line, name, text in rows:
    if kind == "pp":
        out.append((kind, path, line, name, "", text)); continue
    own = f"{path}:{line}:"
    others = [h for h in hits(name) if not h.startswith(own)]
    def isdef(h):
        t = h.split(":",2)[2]
        m2 = re.search(r'(\w+)::' + re.escape(name) + r'\s*\(', t)
        if not m2: return False
        before = t[:m2.start()]
        return not re.search(r'[(=!&|?,]|\breturn\b|->|\.', before) and not t.rstrip().endswith(";")
    defs = [h for h in others if isdef(h)]
    uses = [h for h in others if h not in defs and not h.split(":",2)[2].lstrip().startswith("//")]
    out.append((kind, path, line, name, str(len(uses)), text))
print("\t".join(["kind","path","line","name","use_lines","text"]))
for r in out: print("\t".join(str(x) for x in r))

"""02 § The structure, its generated half (#681): the include graph inside and
into the 80 at the pin, the es-core/CMakeLists.txt lists, the in-source platform
gates and the non-ASCII bytes. Asserts 352 quoted include lines over 91 headers,
37 angle, 1 to es-app (AsyncNotificationComponent.cpp:12), 274 outside lines in
112 files, each of the 80 named once in CMakeLists.txt with `if(` only at 278
and 287, 13 gate lines, and one non-ASCII byte (VideoVlcComponent.cpp:859).
    t34-includes.py <ES worktree> <pin> [paths file]"""
import collections, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import COMP, die, show, paths

W, PINARG = sys.argv[1], sys.argv[2]
files = paths(sys.argv[3] if len(sys.argv) > 3 else None)
quoted, angle, toapp, hq = 0, 0, [], collections.Counter()
gates, nonascii = [], []
GATE = re.compile(r"^\s*#\s*(if|ifdef|ifndef|elif)\b.*(_RPI_|WIN32|USE_OPENGLES_30|LIBVLC_VERSION_MAJOR|BATOCERA)")
for f in files:
    for n, l in enumerate(show(W, f, PINARG).split("\n"), 1):
        m = re.match(r'^\s*#\s*include\s*"([^"]+)"', l)
        if m:
            quoted += 1; hq[m.group(1)] += 1
            if m.group(1).startswith("../"):
                toapp.append("%s:%d `%s`" % (f[len(COMP):], n, m.group(1)))
        if re.match(r"^\s*#\s*include\s*<", l):
            angle += 1
        if GATE.match(l):
            gates.append("%s:%d" % (f[len(COMP):], n))
        if any(ord(c) > 127 for c in l):
            nonascii.append("%s:%d" % (f[len(COMP):], n))
heads = sorted({p[len(COMP):-2] for p in files if p.endswith(".h")})
alt = "|".join(re.escape(h) for h in heads)
out = subprocess.run(["git", "-C", W, "grep", "-n", "-E", r'^\s*#\s*include\s*[<"]([a-z/]*/)?(%s)\.h[>"]' % alt, PINARG, "--", ".", ":!es-core/src/components"], capture_output=True, check=True).stdout.decode("utf-8", "replace").split("\n")
outside = [l[len(PINARG) + 1:] for l in out if l]
ofiles = {l.split(":")[0] for l in outside}
by_head, by_tree = collections.Counter(), collections.Counter()
for l in outside:
    m = re.search(r'[<"](?:[a-z/]*/)?(%s)\.h[>"]' % alt, l)
    by_head[m.group(1) + ".h"] += 1
    by_tree[l.split("/")[0]] += 1
cm = show(W, "es-core/CMakeLists.txt", PINARG).split("\n")
named = {}
for p in files:
    rel = p[len("es-core/src/"):]
    named[p] = [i + 1 for i, l in enumerate(cm) if rel in l]
ifs = [i + 1 for i, l in enumerate(cm) if re.match(r"^\s*if\s*\(", l)]
bad = {p: v for p, v in named.items() if len(v) != 1}
for what, have, want in [("quoted include lines", quoted, 352), ("distinct quoted headers", len(hq), 91), ("angle include lines", angle, 37), ("includes to es-app", len(toapp), 1),
                         ("outside include lines", len(outside), 274), ("outside files", len(ofiles), 112), ("paths not named exactly once in CMakeLists.txt", len(bad), 0),
                         ("gate lines", len(gates), 13), ("lines with a non-ASCII byte", len(nonascii), 1)]:
    if have != want:
        die("%s: %d, expected %d" % (what, have, want))
if ifs != [278, 287]:
    die("CMakeLists.txt if( at %s, expected [278, 287]" % ifs)
if nonascii != ["VideoVlcComponent.cpp:859"]:
    die("the non-ASCII line moved: %s" % nonascii)
hs = [n for p, v in named.items() for n in v if p.endswith(".h")]; cs = [n for p, v in named.items() for n in v if p.endswith(".cpp")]
print("- **Includes inside the 80:** %d quoted lines over %d distinct headers (most: %s), %d angle-bracket lines; **one to es-app:** %s (**L-07**: resolves only through `-I es-core/src` plus `../../`; the unit build links `CloudText.cpp` for `:144`; a `CloudText` that moves to es-core is T18's and T35's call)." % (
    quoted, len(hq), ", ".join("`%s` %d" % kv for kv in hq.most_common(6)), angle, toapp[0]))
print("- **Includes into the 80 from outside:** %d lines in %d files (%s); most-included: %s." % (len(outside), len(ofiles), ", ".join("%s %d" % kv for kv in sorted(by_tree.items())), ", ".join("`%s` %d" % kv for kv in by_head.most_common(6))))
print("- **`es-core/CMakeLists.txt`:** every one of the 80 named exactly once and unconditionally: the 42 headers at `:%d-%d`, the 38 sources at `:%d-%d`; `if(` only at `:%d` and `:%d`." % (min(hs), max(hs), min(cs), max(cs), ifs[0], ifs[1]))
print("- **The in-source platform gates** (%d lines): %s. `VideoPlayerComponent.{cpp,h}` sit whole under `#ifdef _RPI_` and compile to nothing on every image; the `WIN32` blocks are dead on the images; D-WORKFLOW-209's disposition: a dead-end table removes nothing." % (len(gates), ", ".join("`%s`" % g for g in gates)))
print("- **The non-ASCII byte:** `%s`, 0x96 (a Windows-1252 en dash) in the comment `// use: vlc<0x96>long-help`; `git grep -P` sees it only under a C locale; an upstream hit, recorded and not fixed (`es-code-traps.md:60`); 0 in the 21 fork-modified files." % nonascii[0])
print()
print("Generated, asserted by `tools/t34-includes.py`: %d quoted include lines over %d headers, %d angle, %d to es-app; %d outside lines in %d files; the 80 each named once in `es-core/CMakeLists.txt`, `if(` at %s; %d gate lines; %d non-ASCII line." % (quoted, len(hq), angle, len(toapp), len(outside), len(ofiles), " and ".join(map(str, ifs)), len(gates), len(nonascii)))

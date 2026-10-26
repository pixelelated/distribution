"""T18 (#665, #1145): the sync card's stamp writer, run as shipped, under a
full disk and beside a stale temporary.

    python3 -I -B docs/audits/2026_10_26-epic-m6-es-cloud-pages/tools/t18-stamp-fixture.py \
        <es tree> <rev or WORKTREE> <build dir> --expect unfixed|fixed

ThreadedCloudSync.cpp needs a Window and does not link into a unit binary,
so this compiles the shipped `ThreadedCloudSync::writeStamp` out of the file
at <rev> (or the worktree's file), unchanged, beside the real
`Utils::FileSystem::writeAllText` extracted the same way from
es-core/src/utils/FileSystemUtil.cpp and the real es-core AtomicFileUtil.cpp
and StringUtil.cpp. Only `createDirectory`, `getParent`, the file cache and
the log are small doubles. The tests' shape is the repo's own (tests/*.py
compile shipped functions out of GuiMenu.cpp).

Three cases, each in a fresh directory under <build dir>:
  full-disk  a previous stamp, then a write under RLIMIT_FSIZE 0 with SIGXFSZ
             ignored (a full card's stand-in, T17's S5): the previous stamp
             must survive, and a writer that returns bool must say false;
  stale-tmp  a previous stamp and a stale `<stamp>.tmp` that cannot be
             opened for writing: the stamp must be the new line, never the
             stale file;
  read-only  #1145's own wording: a previous stamp and a stale `<stamp>.tmp`
             in a directory made unwritable (mode 0555): the previous stamp
             must survive, and a writer that returns bool must say false;
  normal     the new line, whole.
`--expect unfixed` exits 0 when at least one case fails as #1145 says;
`--expect fixed` exits 0 when every case holds. Writes only under <build dir>.
Exit 2 when it cannot build.
"""
import os, re, subprocess, sys

ES, REV, B, _, EXPECT = sys.argv[1:6]
assert sys.argv[4] == "--expect" and EXPECT in ("fixed", "unfixed")
os.makedirs(B, exist_ok=True)


def src(path):
    if REV == "WORKTREE":
        return open(os.path.join(ES, path)).read()
    r = subprocess.run(["git", "-C", ES, "show", f"{REV}:{path}"], capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr); sys.exit(2)
    return r.stdout


def extract(text, head):
    """The function whose definition line starts with `head`, braces matched."""
    i = text.index(head)
    j = text.index("{", i)
    depth = 0
    for k in range(j, len(text)):
        if text[k] == "{":
            depth += 1
        elif text[k] == "}":
            depth -= 1
            if depth == 0:
                return text[i:k + 1]
    raise SystemExit("unbalanced " + head)


tsc = src("es-app/src/ThreadedCloudSync.cpp")
m = re.search(r"^(void|bool) ThreadedCloudSync::writeStamp\(", tsc, re.M)
ret = m.group(1)
writer = extract(tsc, m.group(0))
fsu = src("es-core/src/utils/FileSystemUtil.cpp")
wat = extract(fsu, "void writeAllText(const std::string& fileName, const std::string& text)")
uses_atomic = "AtomicFile::" in writer

harness = r'''
#include <cerrno>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <csignal>
#include <sys/resource.h>
#include <sys/stat.h>
#include <unistd.h>
#include "utils/AtomicFileUtil.h"
#include "utils/StringUtil.h"
enum LogLevel { LogError, LogWarning, LogInfo, LogDebug };
struct LogLine { std::ostringstream s; ~LogLine() { std::cerr << "LOG: " << s.str() << "\n"; } };
#define LOG(level) LogLine().s
namespace Utils { namespace FileSystem {
  namespace FileCache { inline void remove(const std::string&) {} }
  inline std::string getGenericPath(const std::string& p) { return p; }
  inline std::string getParent(const std::string& p) { auto i = p.rfind('/'); return i == std::string::npos ? "." : p.substr(0, i); }
  inline bool createDirectory(const std::string& p) { struct stat st; return ::stat(p.c_str(), &st) == 0 && S_ISDIR(st.st_mode); }
  WRITEALLTEXT
} }
struct ThreadedCloudSync { static RET writeStamp(const std::string& path, int rc, const std::string& token, const std::string& why); };
WRITER
static std::string slurp(const std::string& p) { std::ifstream f(p, std::ios::binary); std::stringstream s; s << f.rdbuf(); return s.str(); }
static void put(const std::string& p, const std::string& t) { std::ofstream f(p, std::ios::binary); f << t; }
static const char* PREV = "1700000000 0 completed\n";
int main(int argc, char** argv)
{
  const std::string base = argv[1];
  int bad = 0;
  // full-disk
  { const std::string d = base + "/full"; mkdir(d.c_str(), 0755); const std::string s = d + "/last-sync-exit";
    put(s, PREV);
    signal(SIGXFSZ, SIG_IGN);
    struct rlimit old, zero = {0, 0}; getrlimit(RLIMIT_FSIZE, &old); zero.rlim_max = old.rlim_max; setrlimit(RLIMIT_FSIZE, &zero);
    RESULT_DECL ThreadedCloudSync::writeStamp(s, 5, "cloud-stopped", "YOUR CLOUD STOPPED ANSWERING");
    setrlimit(RLIMIT_FSIZE, &old);
    const std::string got = slurp(s);
    const bool kept = got == PREV;
    std::cout << "full-disk: previous stamp " << (kept ? "kept" : ("REPLACED by " + std::to_string(got.size()) + " byte(s)")) << "; writer reported " << RESULT_SAY << "\n";
    if (!kept || RESULT_BAD) bad++; }
  // stale-tmp
  { const std::string d = base + "/stale"; mkdir(d.c_str(), 0755); const std::string s = d + "/last-sync-exit";
    put(s, PREV); put(s + ".tmp", "1600000000 5 STALE\n"); chmod((s + ".tmp").c_str(), 0444);
    ThreadedCloudSync::writeStamp(s, 0, "completed", "");
    const std::string got = slurp(s);
    const bool stale = got.find("STALE") != std::string::npos, fresh = got.find(" 0 completed") != std::string::npos;
    std::cout << "stale-tmp: the stamp is " << (stale ? "THE STALE TEMPORARY" : fresh ? "the new line" : "neither") << "\n";
    if (stale || !fresh) bad++; }
  // read-only: the directory unwritable, a stale temporary in it
  { const std::string d = base + "/readonly"; mkdir(d.c_str(), 0755); const std::string s = d + "/last-sync-exit";
    put(s, PREV); put(s + ".tmp", "1600000000 5 STALE\n");
    chmod(d.c_str(), 0555);
    RESULT_DECL ThreadedCloudSync::writeStamp(s, 5, "cloud-stopped", "YOUR CLOUD STOPPED ANSWERING");
    chmod(d.c_str(), 0755);
    const std::string got = slurp(s);
    const bool kept = got == PREV;
    std::cout << "read-only: previous stamp " << (kept ? "kept" : ("REPLACED by " + std::to_string(got.size()) + " byte(s)")) << "; writer reported " << RESULT_SAY << "\n";
    if (!kept || RESULT_BAD) bad++; }
  // normal
  { const std::string d = base + "/normal"; mkdir(d.c_str(), 0755); const std::string s = d + "/last-sync-exit";
    ThreadedCloudSync::writeStamp(s, 0, "completed", "");
    const std::string got = slurp(s);
    const bool whole = got.size() > 12 && got.back() == '\n' && got.find(" 0 completed") != std::string::npos;
    std::cout << "normal: " << (whole ? "whole" : "NOT WHOLE") << "\n";
    if (!whole) bad++; }
  std::cout << "cases failing as #1145 says: " << bad << "\n";
  return bad;
}
'''
if ret == "bool":
    decl, say, badr = "const bool wrote = ", '(wrote ? "true" : "false")', "wrote"
else:
    decl, say, badr = "", '"nothing (void)"', "false"
harness = (harness.replace("WRITEALLTEXT", wat).replace("WRITER", writer).replace("RET", ret)
           .replace("RESULT_DECL ", decl).replace("RESULT_SAY", say).replace("RESULT_BAD", badr))
cpp = os.path.join(B, "stamp-fixture.cpp")
open(cpp, "w").write(harness)
srcs = [cpp, os.path.join(ES, "es-core/src/utils/AtomicFileUtil.cpp"), os.path.join(ES, "es-core/src/utils/StringUtil.cpp")]
exe = os.path.join(B, "stamp-fixture")
cmd = ["g++", "-std=c++17", "-pthread", "-I", os.path.join(ES, "es-core/src"), *srcs, "-o", exe]
r = subprocess.run(cmd, capture_output=True, text=True)
print(f"rev {REV}: writeStamp returns {ret}; uses Utils::AtomicFile: {'yes' if uses_atomic else 'no'}")
print("$ g++ -std=c++17 -pthread -I es-core/src stamp-fixture.cpp AtomicFileUtil.cpp StringUtil.cpp")
if r.returncode:
    print(r.stderr[-2000:]); sys.exit(2)
base = os.path.join(B, "cases")
os.makedirs(base, exist_ok=True)
for sub in ("full", "stale", "readonly", "normal"):
    if os.path.isdir(os.path.join(base, sub)):
        os.chmod(os.path.join(base, sub), 0o755)
    for f in ("last-sync-exit", "last-sync-exit.tmp"):
        p = os.path.join(base, sub, f)
        if os.path.exists(p):
            os.chmod(p, 0o644); os.remove(p)
run = subprocess.run([exe, base], capture_output=True, text=True)
print(run.stdout.rstrip())
failing = run.returncode
met = (failing > 0) if EXPECT == "unfixed" else (failing == 0)
print(f"{EXPECT}-expectation-{'met' if met else 'NOT met'}")
sys.exit(0 if met else 1)

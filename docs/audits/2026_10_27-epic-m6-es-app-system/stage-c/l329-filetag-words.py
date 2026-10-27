"""3.29 (#680, L-25): FileTag's nine names against xgettext and the French catalog.

    python3 -I l329-filetag-words.py <FileTag.cpp> <emulationstation2.po (fr)> [--control]

The rule asserted: every tag name a player reads (`defaultTags`, the pin's
:13-26) is a literal xgettext extracts (inside `_("...")`, here the
`fake_gettext_*` defines :6-11) and has a non-empty French msgstr. At the
pin three do not: IN PROGRESS, DROPPED and ON HOLD reach T31's filter and
editor pages in English under French. Then getDisplayIcons (:30-44) is
extracted as written and run: "FINISHED" -> one icon, "finished" -> none
(exact case: recorded, the brief's 3.29 second half, not a FAIL).
--control adds the three defines and three French entries to copies of
the inputs, the lane's proposed fix, and must PASS.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
po = Path(sys.argv[2]).read_text()
if "--control" in sys.argv:
    src = src.replace('#define fake_gettext_disliked _("DISLIKED")', '#define fake_gettext_disliked _("DISLIKED")\n#define fake_gettext_inprogress _("IN PROGRESS")\n#define fake_gettext_dropped _("DROPPED")\n#define fake_gettext_onhold _("ON HOLD")')
    po += '\nmsgid "IN PROGRESS"\nmsgstr "EN COURS"\n\nmsgid "DROPPED"\nmsgstr "ABANDONNÉ"\n\nmsgid "ON HOLD"\nmsgstr "EN PAUSE"\n'
tags = re.findall(r'^\t\{ "([^"]+)", _U\(', src, re.M)
literals = set(re.findall(r'_\("([^"]+)"\)', src))
entries = {}
for m in re.finditer(r'^msgid "((?:[^"\\]|\\.)*)"\n((?:"(?:[^"\\]|\\.)*"\n)*)msgstr "((?:[^"\\]|\\.)*)"\n((?:"(?:[^"\\]|\\.)*"\n)*)', po, re.M):
    mid = m.group(1) + "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
    ms = m.group(3) + "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(4)))
    entries[mid] = ms
bad = []
for t in tags:
    ext = t in literals
    fr = entries.get(t)
    print("tag %-12s extracted %-3s French %s" % (t, "yes" if ext else "NO", repr(fr) if fr else "NONE"))
    if not ext or not fr:
        bad.append(t)
print("%d tag names, %d without an extracted literal or a French msgstr" % (len(tags), len(bad)))
fn = function(src, r"^std::vector<std::string> FileTag::getDisplayIcons\(const std::string& names\)", "3.29")
harness = r'''
#include <algorithm>
#include <cstdio>
#include <string>
#include <vector>
#define _U(x) std::string(x)
namespace Utils { namespace String {
std::vector<std::string> split(const std::string& s, char c) { std::vector<std::string> o; std::string cur; for (char x : s) { if (x == c) { o.push_back(cur); cur.clear(); } else cur += x; } o.push_back(cur); return o; }
std::string trim(const std::string& s) { auto b = s.find_first_not_of(' '); if (b == std::string::npos) return ""; return s.substr(b, s.find_last_not_of(' ') - b + 1); } } }
struct FileTag { std::string Name; std::string displayIcon; static std::vector<std::string> getDisplayIcons(const std::string& names); };
static std::vector<FileTag> defaultTags = { { "FINISHED", "f" }, { "IN PROGRESS", "p" } };
''' + fn + r'''
int main(int argc, char** argv) {
    printf("getDisplayIcons(\"FINISHED\") -> %zu icon(s); (\"finished\") -> %zu (exact case, recorded); (\"FINISHED, IN PROGRESS\") -> %zu\n",
        FileTag::getDisplayIcons("FINISHED").size(), FileTag::getDisplayIcons("finished").size(), FileTag::getDisplayIcons("FINISHED, IN PROGRESS").size());
    if (argv[1][0] != '0') { printf("FAIL 3.29: %s tag name(s) a player reads are not extracted or have no French (L-25)\n", argv[1]); return 1; }
    return 0;
}
'''
run(harness, "l329", ("-fsanitize=address,undefined",), args=(str(len(bad)),))

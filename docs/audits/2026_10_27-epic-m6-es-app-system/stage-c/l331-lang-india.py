"""3.31 (#680, L-26): LangInfo::extractLang's India token, extracted as written.

    python3 -I l331-lang-india.py <LangParser.cpp> [--control]

extractLang (the pin's :33-139) over a LangInfo double with the same
members, a SystemConf double answering `system.language` = en_US, and the five Utils::String calls from stage-c/fakes-l321's
StringUtil.h plus `replace`. A ROM's tags are lowercased before they reach
extractLang (`parse`, :148), so "(India)" arrives as "india". The rule
asserted: "india" reads language `in`, region `in`, as the table's own row
(:65) intends. At the pin the row's token is "ìndia" (U+00EC), which no
lowercased ASCII name matches: only "in" works, and "india" reads nothing.
Controls that pass at the pin are printed too: "usa, europe" -> en + us/eu.
--control writes the row's token as "india", the lane's proposed fix, and
must PASS.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
fn = function(src, r"^void LangInfo::extractLang\(const std::string& val\)", "3.31")
if "--control" in sys.argv:
    assert fn.count('"ìndia"') == 1
    fn = fn.replace('"ìndia"', '"india"')
fakes = str(Path(__file__).resolve().parent / "fakes-l321")
harness = r'''
#include <algorithm>
#include <cstdio>
#include <set>
#include <string>
#include <unordered_set>
#include <vector>
#include "utils/StringUtil.h"
namespace Utils { namespace String { std::string replace(std::string s, const std::string& a, const std::string& b) {
    size_t p = 0; while ((p = s.find(a, p)) != std::string::npos) { s.replace(p, a.size(), b); p += b.size(); } return s; } } }
struct SystemConf { static SystemConf* getInstance() { static SystemConf c; return &c; } std::string get(const std::string&) { return "en_US"; } };   // system.language, read at :77 (the guest's default)
struct LangData { std::vector<std::string> value; std::string lang; std::string region; };
struct LangInfo { std::string region; std::unordered_set<std::string> languages; bool mHardRegion = false; void extractLang(const std::string& val); };
''' + fn + r'''
static std::string show(const char* tag) { LangInfo i; i.extractLang(tag); std::string l; for (auto& x : i.languages) l += (l.empty() ? "" : "+") + x; return "lang [" + l + "] region [" + i.region + "]"; }
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    for (auto t : {"usa", "usa, europe", "in", "india"}) printf("%-12s -> %s\n", t, show(t).c_str());
    LangInfo i; i.extractLang("india");
    if (i.region != "in") { printf("FAIL 3.31: \"india\" reads no region: the table's token is \"\xc3\xacndia\" (L-26)\n"); return 1; }
    return 0;
}
'''
run(harness, "l331", ("-fsanitize=address,undefined", "-I" + fakes))

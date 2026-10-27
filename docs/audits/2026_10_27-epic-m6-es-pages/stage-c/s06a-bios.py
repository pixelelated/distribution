"""S6a (#678, #1245, #1246): BIOS CHECK's summary, a system's name, and DETAILS.

    python3 -I s06a-bios.py <es tree> [<GuiBios.cpp>]

Three pieces of GuiBios.cpp are taken as written, between anchors that hold
in the pin's file and the fixed one, and compiled under AddressSanitizer
over doubles (es-app/src is on the include path, so BiosText.h is the
tree's own when the source uses it):
  summary  loadList's block from after the spacer row to the
           MultiLineMenuEntry, as a function of missing, untested and
           present, under a French catalog double: _() from the catalog's
           entries (OF -> SUR, MISSING -> MANQUANT, ...), ngettext with
           French's plural rule (0 and 1 singular). 1 of 7 missing reads
           1 SUR 7 MANQUANT, 7 of 7 reads 7 SUR 7 MANQUANTS, nothing
           missing TOUS PRESENTS (3) with its accent, 2 unknown 2 DE VERSION
           INCONNUE; and the English 1 OF 7 MISSING (the pin: the fragments
           joined, 7 SUR 7 MANQUANT, no agreement).
  name     loadList's block from `std::vector<Entry> entries;` to the sort,
           with nds not loaded and defined in es_systems.cfg as Nintendo DS,
           and snes loaded: nds reads Nintendo DS (the pin: Nds), snes its
           loaded full name.
  details  getHelpPrompts: the list focused on the sentence row with mBios
           not empty (T21's not-run sentence, a73ed9efc) offers no DETAILS;
           the list on a system's row does; the buttons focused do not (the
           pin: DETAILS whenever mBios is non-empty).
render's early draw of the help bar has no host proof: it is read, and the
frame proves it (fix-walk-pending-image).
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

ES = Path(sys.argv[1])
src = Path(sys.argv[2] if len(sys.argv) > 2 else ES / "es-app/src/guis/GuiBios.cpp").read_text()


def between(start, end):
    a = src.index(start) + len(start)
    return src[a:src.index(end, a)]


summary = between("row.addElement(spacer, false);\n", "\t\tauto line = std::make_shared<MultiLineMenuEntry>")
names = between("\tstd::vector<Entry> entries;\n", "\t// What needs doing first")
prompts = function(src, r"^std::vector<HelpPrompt> GuiBios::getHelpPrompts\(\)", "s06a").replace("GuiBios::getHelpPrompts", "Page::getHelpPrompts", 1)
uses_bios_text = '#include "BiosText.h"' in src

harness = r'''
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <vector>
// The catalog double: the French entries of locale/lang/fr/.../emulationstation2.po.
static const std::map<std::string, std::string> FR = {
    { "OF", "SUR" }, { "MISSING", "MANQUANT" }, { "NOT A KNOWN VERSION", "VERSION INCONNUE" },
    { "ALL PRESENT", "TOUS PR\xC3\x89SENTS" }, { "ALL PRESENT (%i)", "TOUS PR\xC3\x89SENTS (%i)" },
};
static const std::map<std::string, std::pair<std::string, std::string>> FR_PLURAL = {
    { "%i OF %i MISSING", { "%i SUR %i MANQUANT", "%i SUR %i MANQUANTS" } },
    { "%i NOT A KNOWN VERSION", { "%i DE VERSION INCONNUE", "%i DE VERSION INCONNUE" } },
};
static bool gFrench = true;
static std::string tr(const char* m) { if (!gFrench) return m; auto it = FR.find(m); return it == FR.end() ? m : it->second; }
static const char* ngettext(const char* one, const char* many, unsigned long n) {
    static std::string out;
    if (!gFrench) { out = n == 1 ? one : many; return out.c_str(); }
    auto it = FR_PLURAL.find(one); if (it == FR_PLURAL.end()) { out = n == 1 ? one : many; return out.c_str(); }
    out = n <= 1 ? it->second.first : it->second.second; return out.c_str();
}
#define _(x) tr(x)
''' + ('#include "BiosText.h"\n' if uses_bios_text else "") + r'''
namespace Utils { namespace String {
    inline std::string proper(const std::string& s) { std::string o = s; for (size_t i = 0; i < o.size(); i++) o[i] = i == 0 ? toupper(o[i]) : tolower(o[i]); return o; }
} }
struct BiosFile { std::string status, md5, path; };
struct BiosSystem { std::string name; std::vector<BiosFile> bios; };
struct SystemData {
    std::string name, full;
    std::string getName() { return name; } std::string getFullName() { return full; }
    static std::vector<SystemData*> sSystemVector;
    static std::map<std::string, std::string> getKnownSystemNames() { return { { "nds", "Nintendo DS" }, { "snes", "Super Nintendo Entertainment System" } }; }
};
std::vector<SystemData*> SystemData::sSystemVector;
struct Entry { BiosSystem data; std::string name; bool hasGames; int missing; int untested; int present; };

static std::string summaryOf(int missing, int untested, int present)
{
    Entry e; e.missing = missing; e.untested = untested; e.present = present;
''' + summary + r'''
    return summary;
}

static std::vector<std::string> namesOf(const std::vector<BiosSystem>& mBios)
{
    std::vector<Entry> entries;
''' + names + r'''
    std::vector<std::string> out; for (auto& e : entries) out.push_back(e.name); return out;
}

#define BUTTON_OK "a"
#define BUTTON_BACK "b"
struct HelpPrompt { std::string button, label; HelpPrompt(const std::string& b, const std::string& l) : button(b), label(l) {} };
struct GuiComponent { virtual ~GuiComponent() {} };
struct ComponentList : GuiComponent { int rows = 1; int size() { return rows; } };
struct ComponentGrid { std::shared_ptr<GuiComponent> focused; std::shared_ptr<GuiComponent> getSelectedComponent() { return focused; } };
struct Page {
    std::vector<BiosSystem> mBios; std::shared_ptr<ComponentList> mList = std::make_shared<ComponentList>();
    ComponentGrid mGrid; int mSystemRows = 0;
    std::vector<HelpPrompt> getHelpPrompts();
};
''' + prompts + r'''
static int failed = 0;
static void check(bool ok, const std::string& what) { std::cout << (ok ? "ok   " : "FAIL ") << what << std::endl; if (!ok) failed++; }
static bool offersDetails(Page& p) { for (auto& h : p.getHelpPrompts()) if (h.label == "DETAILS") return true; return false; }
int main()
{
    gFrench = true;
    const std::string one = summaryOf(1, 0, 6), all = summaryOf(7, 0, 0), none = summaryOf(0, 0, 3), unknown = summaryOf(0, 2, 1);
    check(one == "1 SUR 7 MANQUANT", "summary: 1 of 7 missing reads [" + one + "]");
    check(all == "7 SUR 7 MANQUANTS", "summary: 7 of 7 missing reads [" + all + "]");
    check(none == "TOUS PR\xC3\x89SENTS (3)", "summary: nothing missing reads [" + none + "]");
    check(unknown == "2 DE VERSION INCONNUE", "summary: 2 not a known version reads [" + unknown + "]");
    gFrench = false;
    const std::string en = summaryOf(1, 0, 6);
    check(en == "1 OF 7 MISSING", "summary: English, 1 of 7 missing reads [" + en + "]");

    SystemData snes{ "snes", "Super Nintendo" }; SystemData::sSystemVector = { &snes };
    BiosSystem nds{ "nds", { { "MISSING", "", "bios/firmware.bin" } } }, sn{ "snes", { { "PRESENT", "", "bios/x.bin" } } };
    const auto n = namesOf({ nds, sn });
    check(n.size() == 2 && n[0] == "Nintendo DS", "name: nds, not loaded, reads [" + (n.empty() ? std::string() : n[0]) + "]");
    check(n.size() == 2 && n[1] == "Super Nintendo", "name: snes, loaded, reads [" + (n.size() < 2 ? std::string() : n[1]) + "]");

    Page p; p.mBios = { nds };
    p.mGrid.focused = p.mList; p.mSystemRows = 0;           // the not-run sentence, mBios not empty
    check(!offersDetails(p), "details: the sentence row focused offers DETAILS? " + std::string(offersDetails(p) ? "yes" : "no"));
    p.mSystemRows = 1;                                       // a system's row focused
    check(offersDetails(p), "details: a system's row focused offers DETAILS? " + std::string(offersDetails(p) ? "yes" : "no"));
    p.mGrid.focused = std::make_shared<GuiComponent>();      // the buttons focused
    check(!offersDetails(p), "details: the buttons focused offer DETAILS? " + std::string(offersDetails(p) ? "yes" : "no"));
    if (failed) { std::cout << "FAIL s06a: " << failed << " of 10 checks" << std::endl; return 1; }
    std::cout << "s06a: PASS, 10 checks" << std::endl;
    return 0;
}
'''
run(harness, "s06a", flags=("-fsanitize=address,undefined", "-I", str(ES / "es-app/src")))

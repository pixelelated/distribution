"""S12 (#678, #1254): the SCRAPE tab's remembered filters and SCRAPE FROM.

    python3 -I s12-scrape-filters.py <GuiScraperStart.cpp> [--control]

GuiScraperStart::loadScrapPage and ::loadActivePage are extracted as written
(t31extract) and compiled under AddressSanitizer as members of a test page
over doubles: the page base (addGroup, addWithLabel keeping each row's
component in the menu, addSaveFunc, save running the save functions,
clearSaveFuncs, the menu whose clear() drops the rows, lifeToken), the window
(postToUiThread queues; the test runs the queue as the next frame would),
Settings (a map; setString counted), two scrapers, A and B, whose
hasMissingMedia records its own name, three SystemData with platform ids,
ViewController on the main menu, and OptionListComponent (the selection, the
change callback called last, as OptionListComponent::onSelectedChanged does).
Four cases:
  first-visit  open the tab, change nothing, close: nothing is written to
               ScraperSystems (the pin: the default set written).
  empty        clear every system, close, reopen: no system is selected (the
               pin: "" read back as nothing remembered, the default selected).
  scrape-from  SCRAPE FROM moved to B, the next frame run, a game filtered by
               GAMES TO SCRAPE FOR: B is asked (the pin: A, the tab never rebuilt).
  in-callback  the SCRAPE FROM list is still alive when its own callback
               returns: a rebuild inside the callback would destroy the list
               whose callback is running (es-code-traps.md). --control runs the
               window's posted work inline, the rebuild an inline one: FAIL.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
control = "--control" in sys.argv
scrap = function(src, r"^void GuiScraperStart::loadScrapPage\(\)", "s12").replace("GuiScraperStart::", "Page::", 1)
active = function(src, r"^void GuiScraperStart::loadActivePage\(\)", "s12").replace("GuiScraperStart::", "Page::", 1)

harness = r'''
#include <algorithm>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <vector>
#define _(x) std::string(x)
static const bool INLINE = ''' + ("true" if control else "false") + r''';
struct Settings {
    std::map<std::string, std::string> s; std::map<std::string, int> i; int writes = 0;
    static Settings* getInstance() { static Settings x; return &x; }
    std::string getString(const std::string& k) { return s.count(k) ? s[k] : ""; }
    void setString(const std::string& k, const std::string& v) { if (k == "ScraperSystems") writes++; s[k] = v; }
    int getInt(const std::string& k) { return i.count(k) ? i[k] : 3; }
    void setInt(const std::string& k, int v) { i[k] = v; }
};
namespace Utils { namespace String {
    inline std::vector<std::string> split(const std::string& t, char c) { std::vector<std::string> o; std::string cur; for (char ch : t) { if (ch == c) { o.push_back(cur); cur.clear(); } else cur += ch; } o.push_back(cur); return o; }
} namespace Time { inline long now() { return 1789000000; } } }
struct DateT { bool isValid() { return false; } long getTime() { return 0; } };
struct Metadata { DateT* getScrapeDate(const std::string&) { return nullptr; } };
struct SystemData;
struct FileData { Metadata md; Metadata& getMetadata() { return md; } FileData* getSourceFileData() { return this; } SystemData* getSystem() { return nullptr; } };
static std::vector<std::string> gAsked;
struct Scraper {
    std::string name;
    bool hasMissingMedia(FileData*) { gAsked.push_back(name); return true; }
    bool hasAnyMedia(FileData*) { gAsked.push_back(name); return false; }
    template <class S> bool isSupportedPlatform(S*) { return true; }
    static std::vector<std::string> getScraperList() { return { "A", "B" }; }
    static std::shared_ptr<Scraper> getScraper(const std::string& n) { auto s = std::make_shared<Scraper>(); s->name = n.empty() ? "A" : n; return s; }
};
namespace PlatformIds { enum PlatformId { PLATFORM_IGNORE = 0, NES = 1 }; }
struct SystemData {
    std::string name; std::vector<int> ids;
    static std::vector<SystemData*> sSystemVector;
    bool isGameSystem() { return true; } bool isCollection() { return false; } bool isGroupSystem() { return false; }
    bool hasPlatformId(PlatformIds::PlatformId p) { return std::find(ids.begin(), ids.end(), (int) p) != ids.end(); }
    std::vector<int> getPlatformIds() { return ids; }
    std::string getName() { return name; } std::string getFullName() { return name; }
};
std::vector<SystemData*> SystemData::sSystemVector;
struct GameList { FileData* getCursor() { return nullptr; } };
struct ViewState { int viewing = 0; SystemData* getSystem() { return nullptr; } };
struct ViewController { enum { GAME_LIST = 1 }; ViewState st; static ViewController* get() { static ViewController v; return &v; } ViewState& getState() { return st; } GameList* getGameListView(SystemData*, bool) { return nullptr; } };
struct Component { virtual ~Component() {} };
static std::vector<std::weak_ptr<Component>> gLiveLists;
static int gDiedInOwnCallback = 0;
template <class T>
struct OptionListComponent : Component, std::enable_shared_from_this<OptionListComponent<T>> {
    struct E { std::string name; T obj; bool sel; };
    std::vector<E> entries; bool multi; std::function<void(const T&)> cb;
    OptionListComponent(void*, const std::string&, bool m) : multi(m) {}
    void add(const std::string& n, const T& o, bool s) { entries.push_back({ n, o, s }); }
    bool hasSelection() { for (auto& e : entries) if (e.sel) return true; return false; }
    void selectFirstItem() { for (auto& e : entries) e.sel = false; if (!entries.empty()) entries[0].sel = true; }
    T getSelected() { for (auto& e : entries) if (e.sel) return e.obj; return T(); }
    int getSelectedIndex() { for (size_t k = 0; k < entries.size(); k++) if (entries[k].sel) return (int) k; return -1; }
    std::vector<T> getSelectedObjects() { std::vector<T> o; for (auto& e : entries) if (e.sel) o.push_back(e.obj); return o; }
    void setSelectedChangedCallback(const std::function<void(const T&)>& f) { cb = f; }
    void unselectAll() { for (auto& e : entries) e.sel = false; }
    // The player moves the selection: the callback last, as onSelectedChanged calls it.
    void choose(size_t k) {
        for (auto& e : entries) e.sel = false; entries[k].sel = true;
        std::weak_ptr<OptionListComponent<T>> self = this->shared_from_this();
        T value = entries[k].obj;
        auto f = cb; f(value);
        if (self.expired()) gDiedInOwnCallback++;
    }
};
using FilterFunc = std::function<bool(FileData*)>;
struct Window {
    std::vector<std::function<void()>> posted;
    void postToUiThread(const std::function<void()>& f) { if (INLINE) f(); else posted.push_back(f); }
    void runPosted() { auto q = posted; posted.clear(); for (auto& f : q) f(); }
};
struct Menu {
    std::vector<std::shared_ptr<Component>> rows;
    void clear() { rows.clear(); } void clearButtons() {} void addButton(const std::string&, const std::string&, const std::function<void()>&) {}
};
struct Page {
    Window* mWindow; Menu mMenu; bool mOverwriteMedias = true; int mTab = 0;
    std::shared_ptr<OptionListComponent<FilterFunc>> mFilters, mDateFilters;
    std::shared_ptr<OptionListComponent<SystemData*>> mSystems;
    std::vector<std::function<void()>> mSaveFuncs;
    std::shared_ptr<OptionListComponent<std::string>> lastScraperList;
    std::shared_ptr<int> mLife = std::make_shared<int>(0);
    std::shared_ptr<void> lifeToken() { return mLife; }
    void addGroup(const std::string&) {}
    template <class C> void addWithLabel(const std::string& l, std::shared_ptr<C> c) {
        mMenu.rows.push_back(c);
        if (l == "SCRAPE FROM") lastScraperList = std::dynamic_pointer_cast<OptionListComponent<std::string>>(std::shared_ptr<Component>(c));
    }
    void addSaveFunc(const std::function<void()>& f) { mSaveFuncs.push_back(f); }
    void save() { for (auto& f : mSaveFuncs) f(); }
    void clearSaveFuncs() { mSaveFuncs.clear(); }
    int getTabIndex() { return mTab; }
    void close() { save(); }
    void pressedStart() {}
    void loadSettingsPage() {} void loadAccountsPage() {}
    void loadScrapPage();
    void loadActivePage();
};
using GuiScraperStart = Page;
''' + scrap + "\n" + active + r'''
static int failed = 0;
static void check(bool ok, const std::string& what) { std::cout << (ok ? "ok   " : "FAIL ") << what << std::endl; if (!ok) failed++; }
static void fresh() {
    Settings::getInstance()->s.clear(); Settings::getInstance()->writes = 0; gAsked.clear(); gDiedInOwnCallback = 0;
    Settings::getInstance()->s["Scraper"] = "A"; Settings::getInstance()->s["ScraperFilter"] = "missing-any";
}
int main()
{
    SystemData nes{ "nes", { 1 } }, snes{ "snes", { 1 } }, gb{ "gb", { 1 } };
    SystemData::sSystemVector = { &nes, &snes, &gb };
    Window w;
    {   fresh(); Page p; p.mWindow = &w; p.loadActivePage(); p.close();
        check(Settings::getInstance()->writes == 0, "first-visit: ScraperSystems written " + std::to_string(Settings::getInstance()->writes) + " time(s) (now \"" + Settings::getInstance()->getString("ScraperSystems") + "\")");
    }
    {   fresh(); { Page p; p.mWindow = &w; p.loadActivePage(); p.mSystems->unselectAll(); p.close(); }
        const std::string stored = Settings::getInstance()->getString("ScraperSystems");
        Page q; q.mWindow = &w; q.loadActivePage();
        check(q.mSystems->getSelectedObjects().empty(), "empty: stored \"" + stored + "\", " + std::to_string(q.mSystems->getSelectedObjects().size()) + " system(s) selected at the reopen");
    }
    {   fresh(); Page p; p.mWindow = &w; p.loadActivePage();
        p.lastScraperList->choose(1);                    // SCRAPE FROM -> B
        w.runPosted();                                   // the next frame
        FileData g; gAsked.clear(); p.mFilters->getSelected()(&g);
        check(!gAsked.empty() && gAsked.back() == "B", "scrape-from: the filter asked " + (gAsked.empty() ? std::string("nobody") : gAsked.back()) + " after SCRAPE FROM moved to B");
        check(gDiedInOwnCallback == 0, std::string("in-callback: the SCRAPE FROM list ") + (gDiedInOwnCallback ? "was destroyed inside its own callback" : "outlived its own callback"));
        w.runPosted();
    }
    if (failed) { std::cout << "FAIL s12: " << failed << " of 4 cases\n"; return 1; }
    std::cout << "s12: PASS, 4 cases\n";
    return 0;
}
'''
run(harness, "s12")

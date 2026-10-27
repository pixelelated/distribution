"""S4 (#679; #1266 PL-17, #1263 PL-07): an empty grid's rebuild, and the
scraper's media reads.

    python3 -I s4-views.py <ISimpleGameListView.cpp> <GridGameListView.cpp> <Scraper.cpp>

- **placeholder** (PL-17, EP-35): `ISimpleGameListView::onFileChanged` and
  `createNoEntriesPlaceholder`, and `GridGameListView::setCursor` and
  `addPlaceholder`, extracted as written into one fake view (both classes'
  names mapped to it) whose grid holds the entries it is given and answers
  `setCursor` by pointer. The root is empty: the first populate makes a
  placeholder, the cursor. A file change then repopulates. No placeholder may
  be read after its delete. At the pin, under ASan: a heap-use-after-free at
  `cursor->isPlaceHolder()` in the grid's setCursor, on the placeholder
  `createNoEntriesPlaceholder` deleted.
- **reads** (PL-07): `Scraper::hasAnyMedia` and `Scraper::hasMissingMedia`,
  extracted as written, over an `exists` double that records whether each
  call asked the cached form (the default) or the uncached (`false`). Each
  must ask uncached: the media's writer can be outside ES (the cloud content
  restore, the player over SSH). At the pin: every call cached.
DetailedContainer's nine reads are proved by `tools/t32-reads.py` (tool-run):
the container needs vlc and the window, which the host cannot give a harness.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

isv = Path(sys.argv[1]).read_text()
grid = Path(sys.argv[2]).read_text()
sc = Path(sys.argv[3]).read_text()
ofc = function(isv, r"^void ISimpleGameListView::onFileChanged\(FileData\* /\*file\*/, FileChangeType /\*change\*/\)", "S4")
cnp = function(isv, r"^FileData\* ISimpleGameListView::createNoEntriesPlaceholder\(\)", "S4")
gsc = function(grid, r"^void GridGameListView::setCursor\(FileData\* cursor\)", "S4")
gap = function(grid, r"^void GridGameListView::addPlaceholder\(\)", "S4")
view = "\n".join(x.replace("ISimpleGameListView::", "View::").replace("GridGameListView::", "View::") for x in (ofc, cnp, gsc, gap))
ha = function(sc, r"^bool Scraper::hasAnyMedia\(FileData\* file\)", "S4")
hm = function(sc, r"^bool Scraper::hasMissingMedia\(FileData\* file\)", "S4")
harness = r'''
#include <cstdio>
#include <map>
#include <memory>
#include <stack>
#include <string>
#include <vector>
#define _(x) std::string(x)
enum FileType { GAME = 1, FOLDER = 2, PLACEHOLDER = 3 };
enum FileChangeType { FILE_ADDED, FILE_METADATA_CHANGED, FILE_REMOVED, FILE_SORTED };
enum class MetaDataId { Image, Thumbnail, Marquee, Manual, Map, FanArt, Video, BoxBack, Cartridge, Magazine, TitleShot, Bezel, Wheel, Mix, Box3d, BoxArt };
struct SystemData {};
struct FolderData;
struct FileData {
    FileType type; std::string name; std::map<MetaDataId, std::string> md;
    FileData(FileType t, const std::string& n, SystemData*) : type(t), name(n) {}
    bool isPlaceHolder() { return type == PLACEHOLDER; }
    FolderData* getParent() { return nullptr; }
    std::string getName() { return name; }
    std::string getMetadata(MetaDataId id) { return md[id]; }
};
struct FolderData : FileData { std::vector<FileData*> kids;
    FolderData() : FileData(FOLDER, "root", nullptr) {}
    std::vector<FileData*> getChildrenListToDisplay() { return kids; }
    SystemData* getSystem() { return nullptr; }
    std::shared_ptr<std::vector<FileData*>> findChildrenListToDisplayAtCursor(FileData*, std::stack<FileData*>&) { return nullptr; } };
struct Grid { std::vector<FileData*> e; FileData* cur = nullptr;
    void add(const std::string&, const std::string&, FileData* f) { e.push_back(f); if (!cur) cur = f; }
    void clear() { e.clear(); cur = nullptr; }
    bool setCursor(FileData* f) { for (auto x : e) if (x == f) { cur = f; return true; } return false; } };
struct View {
    Grid mGrid; FolderData* mRoot; std::stack<FileData*> mCursorStack; FileData* mLastParentFolderData = nullptr;
    ~View() { delete mLastParentFolderData; }   // as ISimpleGameListView's destructor (:63-69)
    FileData* getCursor() { return mGrid.cur; }
    void populateList(const std::vector<FileData*>& files) { mGrid.clear(); for (auto f : files) mGrid.add(f->getName(), "", f); if (files.empty()) addPlaceholder(); }
    void onFileChanged(FileData* file, FileChangeType change);
    FileData* createNoEntriesPlaceholder();
    void setCursor(FileData* cursor);
    void addPlaceholder();
};
''' + view + r'''
struct Settings { std::map<std::string, std::string> s; std::map<std::string, bool> b;
    static Settings* getInstance() { static Settings x; return &x; }
    std::string getString(const std::string& k) { return s[k]; } bool getBool(const std::string& k) { return b.count(k) ? b[k] : true; } };
static int gCached = 0, gUncached = 0;
namespace Utils { namespace FileSystem { bool exists(const std::string&, bool cache = true) { (cache ? gCached : gUncached)++; return true; } } }
struct Scraper {
    enum ScraperMediaSource { Screenshot = 1, Video, Marquee, Box2d, Box3d, FanArt, TitleShot, Cartridge, Map, Manual, Wheel, Mix, BoxBack, Magazine, PadToKey, Ratings, Bezel_16_9, ShortTitle, Region };
    bool isMediaSupported(const ScraperMediaSource&) { return true; }
    bool hasAnyMedia(FileData* file); bool hasMissingMedia(FileData* file);
};
typedef Scraper::ScraperMediaSource ScraperMediaSource;
''' + ha + "\n" + hm + r'''
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    int bad = 0;
    for (auto k : {"ScrapperImageSrc", "ScrapperThumbSrc", "ScrapperLogoSrc"}) Settings::getInstance()->s[k] = "x";
    FileData f(GAME, "g", nullptr);
    for (auto id : {MetaDataId::Image, MetaDataId::Thumbnail, MetaDataId::Marquee, MetaDataId::Manual, MetaDataId::Map, MetaDataId::FanArt, MetaDataId::Video, MetaDataId::BoxBack, MetaDataId::Cartridge, MetaDataId::Magazine, MetaDataId::TitleShot, MetaDataId::Bezel, MetaDataId::Wheel, MetaDataId::Mix})
        f.md[id] = "/roms/gb/media/x.png";
    Scraper s; s.hasAnyMedia(&f); s.hasMissingMedia(&f);
    printf("reads: hasAnyMedia and hasMissingMedia asked exists %d time(s) cached, %d uncached\n", gCached, gUncached);
    if (gCached) { printf("FAIL PL-07: the scraper's media reads ask the cached form, which remembers a miss or a hit made before an outside write\n"); bad++; }
    View v; FolderData root; v.mRoot = &root;
    v.populateList(root.getChildrenListToDisplay());
    printf("placeholder: an empty grid, cursor %s\n", v.getCursor() && v.getCursor()->isPlaceHolder() ? "on its placeholder" : "?");
    v.onFileChanged(nullptr, FILE_ADDED);
    printf("placeholder: after a file change, cursor %s\n", v.getCursor() && v.getCursor()->isPlaceHolder() ? "on the new placeholder" : "?");
    return bad ? 1 : 0;
}
'''
run(harness, "s4", ("-fsanitize=address,undefined",))

"""S2 (#680; #1272 PL-02, EP-37): l06's extension, the dynamic collection's reload over the real drop/remake pair.

    python3 -I l06-collections.py <CollectionSystemManager.cpp> <ViewController.cpp> [case ...]

CollectionSystemManager's reloadCollection and repopulateGameListView, and
ViewController's dropGameListView and remakeGameListView (the fork's pair,
#246; T2's file, read), extracted as written, over doubles: a view whose
cursor and cursor stack are what ViewController.cpp:1140-1142 and
ISimpleGameListView.cpp:637-649 read (repopulate reads mCursorStack's top
and mRoot; populateList clears without reading the old cursor,
BasicGameListView.cpp:65), and populateCustomCollection mirroring
:1115-1117 (the root cleared, its games deleted, new ones made). The cases:
  bundled     the collection inside the bundle, the bundle's view open with
              its cursor on one of its games: no freed game is read (l06's case)
  nonbundled  the collection shown as its own system, its view open, the
              cursor on one of its games: no freed game is read (the route
              read for #1272; the record says whether the pin faults)
  ep37        after the reload the folder moved to is the registered view's
              (at the pin :1593 moves the retained old view); the cursor on no
              game, so the case asks only which view is moved
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

csm = Path(sys.argv[1]).read_text(); vc = Path(sys.argv[2]).read_text()
cases = sys.argv[3:] or ["bundled", "nonbundled", "ep37"]
rel = function(csm, r"^void CollectionSystemManager::reloadCollection\(const std::string& collectionName, bool repopulateGamelist\)", "S2")
rep = function(csm, r"^void CollectionSystemManager::repopulateGameListView\(const std::string& collectionName\)", "S2")
drop = function(vc, r"^std::string ViewController::dropGameListView\(SystemData\* system, bool\* wasCurrent\)", "S2")
remake = function(vc, r"^void ViewController::remakeGameListView\(SystemData\* system, const std::string& cursorPath, bool wasCurrent\)", "S2")
harness = r'''
#include <cstdio>
#include <map>
#include <memory>
#include <stack>
#include <string>
#include <vector>
enum FileType { GAME = 1, FOLDER = 2, PLACEHOLDER = 3 };
struct Vector3f { float x = 0, y = 0, z = 0; };
struct SystemData;
struct FileData { FileType type; std::string path, name; SystemData* sys = nullptr;
    FileData(FileType t, const std::string& p, const std::string& n) : type(t), path(p), name(n) {} virtual ~FileData() {}
    FileType getType() { return type; } std::string getName() { return name; } std::string getPath() { return path; } bool isPlaceHolder() { return type == PLACEHOLDER; } };
struct FolderData : FileData { std::vector<FileData*> kids; FolderData(const std::string& n) : FileData(FOLDER, "/collections/" + n, n) {}
    std::vector<FileData*> getChildren() { return kids; } std::vector<FileData*> getFilesRecursive(int, bool = false) { return kids; }
    void clear() { for (auto k : kids) delete k; kids.clear(); } };
struct SystemData { std::string name; FolderData* root; bool collection = true; static std::vector<SystemData*> sSystemVector;
    FolderData* getRootFolder() { return root; } std::string getName() { return name; } bool isCollection() { return collection; }
    void setUIModeFilters() {} void updateDisplayedGameCount() {} };
std::vector<SystemData*> SystemData::sSystemVector;
static int gGeneration = 0;
struct IGameListView { SystemData* sys; FileData* cursor = nullptr; std::stack<FileData*> mCursorStack; int id; FolderData* movedTo = nullptr; Vector3f pos;
    IGameListView(SystemData* s) : sys(s), id(++gGeneration) {} virtual ~IGameListView() {}
    FileData* getCursor() { return cursor; } void setCursor(FileData* f) { cursor = f; }
    Vector3f getPosition() { return pos; } void setPosition(const Vector3f& p) { pos = p; } void onShow() {} void onHide() {}
    // ISimpleGameListView.cpp:637-649 as written, populateList's clear (BasicGameListView.cpp:65) reading no old cursor
    void repopulate() { FolderData* folder = sys->getRootFolder(); if (mCursorStack.size()) { auto top = mCursorStack.top(); if (top->getType() == FOLDER) folder = (FolderData*)top; }
        cursor = folder->getChildren().empty() ? nullptr : folder->getChildren()[0]; } };
struct ISimpleGameListView : IGameListView { using IGameListView::IGameListView; void moveToFolder(FolderData* f) { movedTo = f; } };
struct ViewController {
    std::map<SystemData*, std::shared_ptr<IGameListView>> mGameListViews; std::shared_ptr<IGameListView> mCurrentView; struct { Vector3f position; } mDropped;
    static ViewController* get() { static ViewController v; return &v; }
    std::shared_ptr<IGameListView> getGameListView(SystemData* s, bool create = true) { auto it = mGameListViews.find(s); if (it != mGameListViews.end()) return it->second;
        if (!create) return nullptr; auto v = std::make_shared<ISimpleGameListView>(s); mGameListViews[s] = v; return v; }
    // ViewController.cpp:1140-1142 as written: the old view's cursor is read
    void reloadGameListView(SystemData* s) { auto v = getGameListView(s, false); std::string cursorPath; FileData* cursor = v->getCursor();
        if (cursor != nullptr && !cursor->isPlaceHolder()) cursorPath = cursor->getPath(); mGameListViews.erase(s); auto n = getGameListView(s);
        for (auto f : s->getRootFolder()->getFilesRecursive(GAME, true)) if (f->getPath() == cursorPath) n->setCursor(f); }
    std::string dropGameListView(SystemData* system, bool* wasCurrent);
    void remakeGameListView(SystemData* system, const std::string& cursorPath, bool wasCurrent);
    void updateHelpPrompts() {}
};
''' + drop + "\n" + remake + r'''
struct FileFilterIndex {};
struct CollectionSystemData { SystemData* system = nullptr; FileFilterIndex* filteredIndex = nullptr; bool isPopulated = false; };
struct CollectionSystemManager {
    std::map<std::string, CollectionSystemData> mAutoCollectionSystemsData, mCustomCollectionSystemsData; SystemData* mBundle = nullptr;
    static CollectionSystemManager* get() { static CollectionSystemManager m; return &m; }
    SystemData* getCustomCollectionsBundle() { return mBundle; }
    // :1115-1117: the root cleared (its games deleted), then made again
    void populateCustomCollection(CollectionSystemData* d) { d->isPopulated = true; FolderData* r = d->system->getRootFolder(); r->clear();
        for (auto n : {"Alpha", "Bravo"}) r->kids.push_back(new FileData(GAME, std::string("/roms/gb/") + n + ".gb", n)); }
    void repopulateGameListView(const std::string& collectionName); void reloadCollection(const std::string& collectionName, bool repopulateGamelist);
};
''' + rep + "\n" + rel + r'''
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0); int bad = 0;
    for (int k = 1; k < argc; k++) {
        std::string c = argv[k]; auto* m = CollectionSystemManager::get(); auto* vc = ViewController::get();
        m->mCustomCollectionSystemsData.clear(); vc->mGameListViews.clear(); vc->mCurrentView = nullptr; SystemData::sSystemVector.clear();
        FolderData* dynRoot = new FolderData("t33dyn"); for (auto n : {"Alpha", "Bravo"}) dynRoot->kids.push_back(new FileData(GAME, std::string("/roms/gb/") + n + ".gb", n));
        SystemData* dyn = new SystemData{"t33dyn", dynRoot}; FolderData* bundleRoot = new FolderData("bundle"); SystemData* bundle = new SystemData{"collections", bundleRoot};
        m->mBundle = bundle; FileFilterIndex idx; m->mCustomCollectionSystemsData["t33dyn"] = CollectionSystemData{dyn, &idx, true};
        std::shared_ptr<IGameListView> before;
        if (c == "bundled" || c == "ep37") { bundleRoot->kids.push_back(dynRoot); before = vc->getGameListView(bundle); before->cursor = c == "ep37" ? nullptr : dynRoot->kids[1]; vc->mCurrentView = before; }
        else { SystemData::sSystemVector.push_back(dyn); before = vc->getGameListView(dyn); before->cursor = dynRoot->kids[1]; vc->mCurrentView = before; }
        printf("%s: the view open, cursor %s\n", c.c_str(), before->cursor ? ("on " + before->cursor->getPath()).c_str() : "on no game (the case asks only which view is moved)");
        m->reloadCollection("t33dyn", true);
        if (c == "ep37") { auto now = vc->getGameListView(bundle, false); bool ok = now && now->movedTo == dynRoot;
            printf("ep37: the folder moved to on the %s view\n", now && now->movedTo ? "registered" : (before->movedTo ? "retained OLD" : "no"));
            if (!ok) { printf("FAIL ep37: moveToFolder acted on the retained old view, not the one registered after the reload (EP-37)\n"); bad++; } }
        else printf("%s: no freed game was read\n", c.c_str());
        bundleRoot->kids.clear(); vc->mGameListViews.clear(); vc->mCurrentView = nullptr; before.reset(); dynRoot->clear(); delete dynRoot; delete bundleRoot; delete dyn; delete bundle;
    }
    if (bad) { printf("FAIL S2: %d case(s)\n", bad); return 1; }
    return 0;
}
'''
run(harness, "s2r", ("-fsanitize=address,undefined",), args=tuple(cases))

"""L-06 (#680): CollectionSystemManager::reloadCollection frees, then the view reads.

    python3 -I l06-reload-collection.py <CollectionSystemManager.cpp> [--control]

reloadCollection (the pin's :1558-1600) extracted as written, over doubles:
- populateCustomCollection mirrors its :1115-1117 (`rootFolder->clear()`,
  which deletes the children, then the repopulate with new FileData);
- the bundle holds the collection's own root folder as its child, as
  :1302 builds it (`bundle->getRootFolder()->addChild(newSysRootFolder)`);
- ViewController::reloadGameListView(bundle) reads the old view's cursor as
  ViewController.cpp:1140-1142 does (`getCursor()`, `isPlaceHolder()`,
  `getPath()`).
The scenario is a dynamic collection (filteredIndex set: the only kind
:1573 repopulates), the bundle's view open with its cursor on a game in
that collection, and reloadCollection(name, true): the call
GuiGamelistOptions.cpp:425 and ISimpleGameListView.cpp:462 make. Asserted:
no freed FileData is read. At the pin, under ASan: a heap-use-after-free
at the cursor read. The guest's G-02 ran a plain custom collection, which
never takes this path (:1573). --control reads the cursor's path before
the clear and remakes the view from it (es-code-traps.md:191's two
halves), the lane's proposed fix, and must PASS.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
fn = function(src, r"^void CollectionSystemManager::reloadCollection\(const std::string& collectionName, bool repopulateGamelist\)", "L-06")
if "--control" in sys.argv:
    a = "\t\tdata->second.isPopulated = false;\n\t\tpopulateCustomCollection(&data->second);"
    assert fn.count(a) == 1
    fn = fn.replace(a, "\t\tstd::string t33cp = ViewController::get()->cursorPathOf(CollectionSystemManager::get()->getCustomCollectionsBundle());\n" + a)
    assert fn.count("ViewController::get()->reloadGameListView(bundle);") == 1
    fn = fn.replace("ViewController::get()->reloadGameListView(bundle);", "ViewController::get()->reloadGameListView(bundle, t33cp);")
harness = r'''
#include <cstdio>
#include <map>
#include <memory>
#include <string>
#include <vector>
enum FileType { GAME = 1, FOLDER = 2, PLACEHOLDER = 3 };
struct FileData { FileType type; std::string path; std::string name;
    FileData(FileType t, const std::string& p, const std::string& n) : type(t), path(p), name(n) {}
    virtual ~FileData() {}
    FileType getType() { return type; } std::string getName() { return name; } std::string getPath() { return path; } bool isPlaceHolder() { return type == PLACEHOLDER; } };
struct FolderData : FileData { std::vector<FileData*> kids;
    FolderData(const std::string& n) : FileData(FOLDER, "/collections/" + n, n) {}
    std::vector<FileData*> getChildren() { return kids; }
    void clear() { for (auto k : kids) delete k; kids.clear(); } };
struct SystemData { FolderData* root; FolderData* getRootFolder() { return root; } };
struct FileFilterIndex {};
struct CollectionSystemData { SystemData* system = nullptr; FileFilterIndex* filteredIndex = nullptr; bool isPopulated = false; };
struct IGameListView { FileData* cursor = nullptr; virtual ~IGameListView() {} FileData* getCursor() { return cursor; } };
struct ISimpleGameListView : IGameListView { void moveToFolder(FolderData*) {} };
static int gGeneration = 0;
struct ViewController {
    std::map<SystemData*, std::shared_ptr<IGameListView>> views;
    static ViewController* get() { static ViewController v; return &v; }
    std::shared_ptr<IGameListView> getGameListView(SystemData* s, bool) { auto it = views.find(s); return it == views.end() ? nullptr : it->second; }
    std::string cursorPathOf(SystemData* s) { auto v = getGameListView(s, false); FileData* c = v ? v->getCursor() : nullptr; return c && !c->isPlaceHolder() ? c->getPath() : ""; }
    // ViewController.cpp:1140-1142, as written there: the old view's cursor is read.
    void reloadGameListView(SystemData* s) { auto v = getGameListView(s, false); std::string cursorPath; FileData* cursor = v->getCursor();
        if (cursor != nullptr && !cursor->isPlaceHolder()) cursorPath = cursor->getPath(); remake(s, cursorPath); }
    void reloadGameListView(SystemData* s, const std::string& cursorPath) { remake(s, cursorPath); }
    void remake(SystemData* s, const std::string& cursorPath) { auto n = std::make_shared<ISimpleGameListView>();
        for (auto k : s->getRootFolder()->getChildren()) for (auto g : ((FolderData*)k)->getChildren()) if (g->getPath() == cursorPath) n->cursor = g;
        views[s] = n; printf("reload: the bundle's view remade, cursor %s\n", n->cursor ? n->cursor->getPath().c_str() : "(none)"); }
};
struct CollectionSystemManager {
    std::map<std::string, CollectionSystemData> mAutoCollectionSystemsData, mCustomCollectionSystemsData;
    SystemData* mBundle = nullptr;
    static CollectionSystemManager* get() { static CollectionSystemManager m; return &m; }
    SystemData* getCustomCollectionsBundle() { return mBundle; }
    void repopulateGameListView(const std::string&) {}
    // :1115-1117, then the repopulate with new FileData (the index's games).
    void populateCustomCollection(CollectionSystemData* d) { d->isPopulated = true; FolderData* r = d->system->getRootFolder(); r->clear();
        gGeneration++; for (auto n : {"Alpha", "Bravo"}) r->kids.push_back(new FileData(GAME, std::string("/roms/gb/") + n + ".gb", n)); }
    void reloadCollection(const std::string& collectionName, bool repopulateGamelist);
};
''' + fn + r'''
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    auto* m = CollectionSystemManager::get();
    FolderData* dynRoot = new FolderData("t33dyn");
    for (auto n : {"Alpha", "Bravo"}) dynRoot->kids.push_back(new FileData(GAME, std::string("/roms/gb/") + n + ".gb", n));
    SystemData dyn{dynRoot};
    FolderData* bundleRoot = new FolderData("bundle"); bundleRoot->kids.push_back(dynRoot);   // :1302
    SystemData bundle{bundleRoot}; m->mBundle = &bundle;
    FileFilterIndex idx; m->mCustomCollectionSystemsData["t33dyn"] = CollectionSystemData{&dyn, &idx, true};
    auto view = std::make_shared<ISimpleGameListView>(); view->cursor = dynRoot->kids[1];
    ViewController::get()->views[&bundle] = view;
    printf("before: the bundle's view open, cursor on %s inside the dynamic collection\n", view->cursor->getPath().c_str());
    m->reloadCollection("t33dyn", true);
    printf("after: no freed entry was read\n");
    ViewController::get()->views.clear(); bundleRoot->kids.clear(); dynRoot->clear(); delete dynRoot; delete bundleRoot;   // the fixture's own (D-WORKFLOW-211)
    return 0;
}
'''
run(harness, "l06", ("-fsanitize=address,undefined",))

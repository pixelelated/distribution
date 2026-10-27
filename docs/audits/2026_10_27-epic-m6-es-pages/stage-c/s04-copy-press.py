"""S4 (#678, #1242, #782): COPY TO FREE SLOT as the save state manager presses it.

    python3 -I s04-copy-press.py <GuiSaveState.cpp>

The X branch of GuiSaveState::input (`if (input.value != 0 &&
config->isMappedTo("x", input)) {...}`) and the whole of GuiSaveState::update
are extracted as written (t31extract: balanced braces, strings and comments
skipped) and compiled under AddressSanitizer as members of a test page over
doubles: the grid (START NEW GAME first, then a tile per state on "disk"), the
repository (getNextFreeSlot, refresh), SaveState (copyToSlot records a write
at the press and returns what the case says), the saves-tree probe
(savesTreeBusy records that the lock was asked), and SaveStateBookkeeper
(recordCopy, and copyLater/copyOutcome for the worker's copy, whose outcome
the case scripts: the worker's own copy and its lock are bookkeeper-tests').
The cursor starts on the first state's tile. Five cases:
  failed    the copy is not made: a box says THE COPY COULDN'T BE MADE. YOUR
            SAVE STATES ARE AS THEY WERE., and no tile is added (the pin: silent).
  made      the copy is made: the cursor on the new tile, and the toast SAVE
            STATE COPIED. (the pin: the cursor on START NEW GAME, no word).
  no-slot   no free slot: a box says THERE'S NO FREE SLOT LEFT. DELETE A SAVE
            STATE FIRST. (the pin: silent).
  lock      the press writes nothing: the copy is handed to the worker, which
            takes the transfer lock for it (the pin: the lock asked, let go,
            then the copy written at the press).
  twice     a second press before the first copy's outcome asks for no second
            copy. A guard for the worker's shape: it holds at the pin too,
            where the copy is made at the press and the rebuilt grid puts the
            cursor on START NEW GAME, which X ignores.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
xblock = function(src, r'^\tif \(input\.value != 0 && config->isMappedTo\("x", input\)\)', "s04")
update = function(src, r"^void GuiSaveState::update\(int deltaTime\)", "s04").replace("GuiSaveState::update", "Page::update", 1)

harness = r'''
#include <algorithm>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>
#include <vector>
#define _(x) std::string(x)
enum LogLevel { LogInfo, LogWarning, LogError };
struct LogLine { std::ostringstream o; template <class T> LogLine& operator<<(const T& v) { o << v; return *this; } };
#define LOG(level) LogLine()
static std::vector<std::string> gEvents, gDisk;
static bool gCopyReturns = false, gCopyWrites = false;
static int gFreeSlot = 2, gOutcome = -1;
static unsigned gTicket = 0, gCompleted = 0;
struct Input { int value = 1; };
struct InputConfig { bool isMappedTo(const std::string& n, Input) { return n == "x"; } };
struct Window;
struct GuiComponent { Window* mWindow = nullptr; virtual ~GuiComponent() {} void update(int) {} };
struct Window {
    void pushGui(GuiComponent* g) { delete g; }
    void displayNotificationMessage(std::string m, int = -1) { gEvents.push_back("toast: " + m); }
};
struct GuiMsgBox : GuiComponent { GuiMsgBox(Window*, const std::string& t) { gEvents.push_back("box: " + t); } };
struct SaveState {
    std::string fileName; int config = 0;
    bool isSlotValid() const { return true; }
    std::string getScreenShot() const { return ""; }
    std::string makeStateFilename(int s, bool = false, bool = false) const { return "/s/nes/Bobl.state" + std::to_string(s); }
    bool copyToSlot(int s, bool = false) const { gEvents.push_back("write@press"); if (gCopyWrites) gDisk.push_back(makeStateFilename(s)); return gCopyReturns; }
};
struct SaveStateItem { SaveState* saveState; SaveStateItem(SaveState* s = nullptr) : saveState(s) {} };
struct Grid {
    std::vector<SaveStateItem> items; int cursor = 0;
    int size() { return (int) items.size(); }
    const SaveStateItem& getSelected() { return items[cursor]; }
    std::vector<SaveStateItem> getObjects() { return items; }
    int getCursorIndex() { return cursor; }
    void setCursorIndex(int i) { cursor = i; }
};
struct FileData;
struct Repo {
    std::vector<std::unique_ptr<SaveState>> states; SaveState newGame;
    int getNextFreeSlot(FileData*, int) { return gFreeSlot; }
    void refresh() { states.clear(); for (auto& f : gDisk) { auto s = std::make_unique<SaveState>(); s->fileName = f; states.push_back(std::move(s)); } }
};
struct System { std::string getName() { return "nes"; } };
struct FileData { System sys; System* getSystem() { return &sys; } std::string getPath() { return "/r/Bobl.nes"; } FileData* getSourceFileData() { return this; } };
struct SaveStateBookkeeper {
    static void recordCopy(const std::string&, const std::string&, const std::string&, const std::string&) { gEvents.push_back("record"); }
    static unsigned copyLater(const std::string&, const std::string&, const std::string&, const std::string&, const std::string&, const std::string&) { gEvents.push_back("queued"); return ++gTicket; }
    static int copyOutcome(unsigned t) { if (t == 0 || gOutcome == -1) return -1; int o = gOutcome; gOutcome = -1; return o; }
    static unsigned completed() { return gCompleted; }
    static bool isPending(const std::string&) { return false; }
    static bool holdsTransferLock() { return false; }
};
static std::string savesTreeBusy(const std::string&) { gEvents.push_back("probe"); return ""; }
class Page : public GuiComponent {
public:
    std::shared_ptr<Grid> mGrid = std::make_shared<Grid>();
    FileData game; FileData* mGame = &game; Repo repo; Repo* mRepository = &repo;
    unsigned mDeletionsSeen = 0; std::vector<std::string> mShown;
    unsigned mCopyTicket = 0; std::string mCopyFile;
    void loadGrid() {
        mGrid->items.clear(); mGrid->cursor = 0; mShown.clear();
        mGrid->items.push_back(SaveStateItem(&mRepository->newGame));      // START NEW GAME
        for (auto& s : mRepository->states) { mGrid->items.push_back(SaveStateItem(s.get())); mShown.push_back(s->fileName); }
        std::sort(mShown.begin(), mShown.end());
    }
    std::vector<std::string> filesOnDisk() { auto v = gDisk; std::sort(v.begin(), v.end()); return v; }
    bool pressX(InputConfig* config, Input input) {
''' + xblock + r'''
        return false;
    }
    void update(int deltaTime);
};
''' + update + r'''
static int failed = 0;
static void check(bool ok, const std::string& what) { std::cout << (ok ? "ok   " : "FAIL ") << what << "\n"; if (!ok) failed++; }
static bool has(const std::string& e) { return std::find(gEvents.begin(), gEvents.end(), e) != gEvents.end(); }
static int count(const std::string& e) { return (int) std::count(gEvents.begin(), gEvents.end(), e); }
static std::string events() { std::string s; for (auto& e : gEvents) s += (s.empty() ? "" : " | ") + e; return s; }
static Page* open(Window& w) {
    gEvents.clear(); gDisk = { "/s/nes/Bobl.state1" }; gFreeSlot = 2; gOutcome = -1; gCopyReturns = gCopyWrites = false;
    auto* p = new Page(); p->mWindow = &w; p->repo.refresh(); p->loadGrid(); p->mGrid->cursor = 1;   // on the state's tile
    return p;
}
int main()
{
    Window w; InputConfig cfg; Input in;
    const std::string failWords = "box: THE COPY COULDN'T BE MADE. YOUR SAVE STATES ARE AS THEY WERE.";
    {   // failed: copyToSlot false at the pin; the worker's outcome 0 after
        Page* p = open(w); p->pressX(&cfg, in); gOutcome = 0; p->update(0);
        check(has(failWords) && p->mGrid->size() == 2, "failed: " + events() + "; tiles " + std::to_string(p->mGrid->size()));
        delete p;
    }
    {   // made: the pin's copyToSlot writes; after, the worker has written the file when its outcome is 1
        Page* p = open(w); gCopyReturns = gCopyWrites = true; p->pressX(&cfg, in);
        if (!has("write@press")) gDisk.push_back("/s/nes/Bobl.state2");   // the worker's copy
        gOutcome = 1; p->update(0);
        const SaveStateItem& sel = p->mGrid->getSelected();
        const std::string on = sel.saveState && !sel.saveState->fileName.empty() ? sel.saveState->fileName : "START NEW GAME";
        check(on == "/s/nes/Bobl.state2" && has("toast: SAVE STATE COPIED."), "made: the cursor on " + on + "; " + events());
        delete p;
    }
    {   // no free slot
        Page* p = open(w); gFreeSlot = -1; p->pressX(&cfg, in); p->update(0);
        check(has("box: THERE'S NO FREE SLOT LEFT. DELETE A SAVE STATE FIRST."), "no-slot: " + events());
        delete p;
    }
    {   // lock: nothing written at the press; the copy handed to the worker
        Page* p = open(w); gCopyReturns = gCopyWrites = true; p->pressX(&cfg, in);
        check(!has("write@press") && has("queued"), "lock: " + events());
        delete p;
    }
    {   // twice before the outcome
        Page* p = open(w); gCopyReturns = gCopyWrites = true; p->pressX(&cfg, in); p->pressX(&cfg, in);
        const int asked = count("write@press") + count("queued");
        check(asked == 1, "twice: " + std::to_string(asked) + " copies asked for; " + events());
        delete p;
    }
    if (failed) { std::cout << "FAIL s04: " << failed << " of 5 cases\n"; return 1; }
    std::cout << "s04: PASS, 5 cases\n";
    return 0;
}
'''
run(harness, "s04")

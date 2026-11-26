
#include <algorithm>
#include <cstdio>
#include <memory>
#include <vector>

struct SaveStateConfig { int firstslot; };
struct SaveState { int slot; };
struct SaveStateRepository;
struct SystemData { SaveStateRepository* repo; SaveStateRepository* getSaveStateRepository() { return repo; } };
struct FileData { SystemData* sys; FileData* getSourceFileData() { return this; } SystemData* getSystem() { return sys; } };

static bool g_enabled = true;
static std::vector<SaveState*> g_states;

struct SaveStateRepository {
    static bool isEnabled(FileData*) { return g_enabled; }
    std::vector<SaveState*> getSaveStates(FileData*, std::shared_ptr<SaveStateConfig> = nullptr) { return g_states; }
    static int getNextFreeSlot(FileData* game, std::shared_ptr<SaveStateConfig> config);
};

#include "allocator-body.inc"

int main()
{
    SaveStateRepository repo; SystemData sys{&repo}; FileData game{&sys};
    struct C { const char* name; bool enabled; int firstslot; bool hasConfig; std::vector<int> slots; };
    const C cases[] = {
        {"disabled", false, 0, false, {}},
        {"empty, no config", true, 0, false, {}},
        {"empty, firstslot 0", true, 0, true, {}},
        {"empty, firstslot 1", true, 1, true, {}},
        {"empty, firstslot 7", true, 7, true, {}},
        {"autosave only, no config", true, 0, false, {-1}},
        {"autosave only, firstslot 0", true, 0, true, {-1}},
        {"autosave only, firstslot 1", true, 1, true, {-1}},
        {"autosave only, firstslot 7", true, 7, true, {-1}},
        {"slot 0", true, 0, false, {0}},
        {"slots 0 1 2", true, 0, false, {0, 1, 2}},
        {"gap 0 2", true, 0, false, {0, 2}},
        {"autosave and slot 3", true, 0, false, {-1, 3}},
        {"high bound 99999", true, 0, false, {99999}}
    };
    for (const C& c : cases)
    {
        g_enabled = c.enabled;
        std::vector<SaveState> backing; backing.reserve(c.slots.size());
        g_states.clear();
        for (int s : c.slots) { backing.push_back(SaveState{s}); }
        for (auto& b : backing) g_states.push_back(&b);
        std::shared_ptr<SaveStateConfig> cfg = c.hasConfig ? std::make_shared<SaveStateConfig>(SaveStateConfig{c.firstslot}) : nullptr;
        std::printf("%s\t%d\n", c.name, SaveStateRepository::getNextFreeSlot(&game, cfg));
    }
    return 0;
}

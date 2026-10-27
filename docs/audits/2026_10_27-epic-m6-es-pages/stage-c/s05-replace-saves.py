"""S5 (#678, #1243): does a page that replaces itself from an option's callback save first?

    python3 -I s05-replace-saves.py <GuiNetPlaySettings.cpp> <GuiControllersSettings.cpp> <GuiSettings.cpp>

The two callbacks are extracted as written -- USE RELAY SERVER's
`relayServer->setSelectedChangedCallback(<lambda>)` and SHOW CONTROLLER
ACTIVITY's `activity->setOnChangedCallback(<lambda>)` -- and compiled under
AddressSanitizer as members of test pages built on GuiSettings::save and
::close extracted from the tree given, over doubles of the stores with the
real rules (a set of the held value changes nothing; a store writes only what
changed). Each page has a save function for a switch the player moved before
the callback, as addSwitch's and the pages' own (ENABLE NETPLAY's
`global.netplay`, AUTOCONFIGURE RETROARCH HOTKEYS' `system.autohotkeys`). The
callback replaces the page; the case asks whether the moved switch reached
system.cfg. At the pin both replace the page without save(): both FAIL.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

net, ctl, gs = (Path(a).read_text() for a in sys.argv[1:4])


def lambda_of(src, anchor):
    """The lambda passed to `anchor(`, read by balanced brackets."""
    i = src.index(anchor)
    j = src.index("(", i + len(anchor) - 1)
    depth, k = 0, j
    while True:
        c = src[k]
        if src.startswith("//", k):          # a comment's apostrophe is no char literal
            k = src.index("\n", k)
            continue
        if c in "\"'":
            k += 1
            while src[k] != c:
                k += 2 if src[k] == "\\" else 1
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return src[j + 1:k]
        k += 1


relay = lambda_of(net, "relayServer->setSelectedChangedCallback(")
activity = lambda_of(ctl, "activity->setOnChangedCallback(")
harness = r'''
#include <algorithm>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <utility>
#include <vector>
static std::map<std::string, std::string> gSystemCfg; static int gSystemCfgWrites = 0;
struct Settings {
    std::map<std::string, bool> b; bool changed = false;
    static Settings* getInstance() { static Settings s; return &s; }
    bool getBool(const std::string& k) { return b.count(k) && b[k]; }
    bool setBool(const std::string& k, bool v) { if (getBool(k) == v) return false; b[k] = v; changed = true; return true; }
    bool saveFile() { if (!changed) return false; changed = false; return true; }
};
struct SystemConf {
    std::map<std::string, std::string> v, pending;
    static SystemConf* getInstance() { static SystemConf c; return &c; }
    std::string get(const std::string& k) { return v.count(k) ? v[k] : ""; }
    bool set(const std::string& k, const std::string& x) { if (v.count(k) && v[k] == x) return false; v[k] = x; pending[k] = x; return true; }
    bool setBool(const std::string& k, bool x) { return set(k, x ? "1" : "0"); }
    bool saveSystemConf() { if (pending.empty()) return false; for (auto& kv : pending) gSystemCfg[kv.first] = kv.second; pending.clear(); gSystemCfgWrites++; return true; }
};
struct Window; struct GuiComponent { Window* mWindow = nullptr; virtual ~GuiComponent() {} };
struct Window { std::vector<GuiComponent*> pushed; void pushGui(GuiComponent* g) { pushed.push_back(g); } };
struct GuiSettings : GuiComponent {
    bool mDoSave = true;
    std::vector<std::function<void()>> mSaveFuncs;
    std::function<void()> mOnFinalizeFunc;
    void addSaveFunc(const std::function<void()>& f) { mSaveFuncs.push_back(f); }
    void close();
    void save();
};
''' + function(gs, r"^void GuiSettings::close\(\)", "s5") + "\n" + function(gs, r"^void GuiSettings::save\(\)", "s5") + r'''
struct GuiNetPlaySettings : GuiComponent { GuiNetPlaySettings(Window* w, int) { mWindow = w; } };
struct NetPage : GuiSettings {
    std::vector<std::pair<std::string, std::string>> communityRelayServers;
    std::function<void(const std::string&)> callback() { return ''' + relay + r'''; }
};
struct SwitchComponent { bool on = true; bool getState() { return on; } };
struct CtlPage : GuiSettings {
    static void openControllersSettings(Window* w, int) { w->pushGui(new GuiComponent()); }
    std::function<void()> callback(Window* window, std::shared_ptr<SwitchComponent> activity) { return ''' + activity + r'''; }
};
int main()
{
    int failed = 0;
    {   // USE RELAY SERVER moved after ENABLE NETPLAY was switched on
        Window w; auto* p = new NetPage(); p->mWindow = &w;
        bool enable = true;                                  // the switch, moved
        p->addSaveFunc([&enable] { SystemConf::getInstance()->setBool("global.netplay", enable); });
        p->callback()("nyc");
        std::cout << "relay: system.cfg written " << gSystemCfgWrites << " time(s); global.netplay=" << (gSystemCfg.count("global.netplay") ? gSystemCfg["global.netplay"] : "(absent)") << "\n";
        if (gSystemCfg["global.netplay"] != "1") { std::cout << "FAIL s05: the relay change replaced the page and dropped ENABLE NETPLAY\n"; failed++; }
        for (auto* g : w.pushed) delete g;
    }
    gSystemCfg.clear(); gSystemCfgWrites = 0;
    {   // SHOW CONTROLLER ACTIVITY toggled after AUTOCONFIGURE was moved
        Window w; auto* p = new CtlPage(); p->mWindow = &w;
        bool autohotkeys = true;
        p->addSaveFunc([&autohotkeys] { SystemConf::getInstance()->setBool("system.autohotkeys", autohotkeys); });
        auto activity = std::make_shared<SwitchComponent>();
        p->callback(&w, activity)();
        std::cout << "activity: system.cfg written " << gSystemCfgWrites << " time(s); system.autohotkeys=" << (gSystemCfg.count("system.autohotkeys") ? gSystemCfg["system.autohotkeys"] : "(absent)") << "\n";
        if (gSystemCfg["system.autohotkeys"] != "1") { std::cout << "FAIL s05: SHOW CONTROLLER ACTIVITY replaced the page and dropped AUTOCONFIGURE\n"; failed++; }
        for (auto* g : w.pushed) delete g;
    }
    if (failed) return 1;
    std::cout << "2 cases\n";
    return 0;
}
'''
run(harness, "s05")

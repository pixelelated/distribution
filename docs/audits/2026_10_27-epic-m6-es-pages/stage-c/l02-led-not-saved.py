"""L-02 / S2 (#678, #1237): does a settings page with no save function write the stores on its own close?

    python3 -I l02-led-not-saved.py <GuiAnalogSticksLedControls.cpp> <GuiSettings.cpp> [--fixed]

The page's applyChanges lambda is extracted as written (from `auto applyChanges`
to its closing `};`) with GuiSettings::close and ::save, over doubles:
runSystemCommand records the command; SystemConf keeps the real rule (set marks
the key changed, saveSystemConf writes only what changed, GuiSettings::save is
the only caller on this path). A slider moved once, then BACK. Expected: the
key in system.cfg. At the pin the page has no save function, save() returns at
its `!mSaveFuncs.size()` and nothing is written -- the case FAILs. Two more
cases (S2): a text-row-only page (one value set through SystemConf::set, as
addInputTextConfigRow's updateVal does, no save function) whose close must
write system.cfg once (FAIL at the pin); and a no-change page (no save
function, nothing set) whose close must write nothing (PASS at the pin: the
guard that the fix does not rewrite the stores on every close). --fixed adds
one empty save function to each page (the stage-C control).
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

led = Path(sys.argv[1]).read_text()
gs = Path(sys.argv[2]).read_text()
fixed = "--fixed" in sys.argv
a = led.index("\tauto applyChanges = ")
b = led.index("\t};", a) + 3
apply = led[a:b]
if "SystemConf::getInstance()->set(\"analogsticks.led\", buffer);" not in apply:
    sys.exit("FAIL l02: applyChanges no longer sets analogsticks.led as the pin does")
harness = r'''
#include <cstdint>
#include <cstdio>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <vector>
static std::vector<std::string> gCommands; static int gSystemCfgWrites = 0;
static std::map<std::string, std::string> gOnDisk;
namespace Utils { namespace Platform { int runSystemCommand(const std::string& c, const std::string&, void*) { gCommands.push_back(c); return 0; } } }
struct Settings { static Settings* getInstance() { static Settings s; return &s; } bool saveFile() { return false; } };
struct SystemConf {
    std::map<std::string, std::string> v, changed;
    static SystemConf* getInstance() { static SystemConf c; return &c; }
    bool set(const std::string& k, const std::string& x) { if (v.count(k) && v[k] == x) return false; v[k] = x; changed[k] = x; return true; }
    bool saveSystemConf() { if (changed.empty()) return false; for (auto& kv : changed) gOnDisk[kv.first] = kv.second; changed.clear(); gSystemCfgWrites++; return true; }
};
struct Slider { float val; float getValue() { return val; } };
struct GuiSettings {
    bool mDoSave = true;
    std::vector<std::function<void()>> mSaveFuncs;
    std::function<void()> mOnFinalizeFunc;
    void addSaveFunc(const std::function<void()>& f) { mSaveFuncs.push_back(f); }
    void close();
    void save();
};
''' + function(gs, r"^void GuiSettings::close\(\)", "l02") + "\n" + function(gs, r"^void GuiSettings::save\(\)", "l02") + r'''
int main()
{
    auto mk = [](float v) { return std::make_shared<Slider>(Slider{v}); };
    auto brightness = mk(1.0f), left_red = mk(0.5f), left_green = mk(0.f), left_blue = mk(0.f),
         right_red = mk(0.f), right_green = mk(1.0f), right_blue = mk(0.f);
    const std::string analogSticksLedScript = "/usr/bin/analog_sticks_ledcontrol";
''' + apply + r'''
    int failed = 0;
    auto fresh = [] { gOnDisk.clear(); gSystemCfgWrites = 0; SystemConf::getInstance()->v.clear(); SystemConf::getInstance()->changed.clear(); };
    {   // the LED page
        fresh(); auto* s = new GuiSettings();
''' + ("        s->addSaveFunc([] {});\n" if fixed else "") + r'''        applyChanges(); s->close();
        const bool saved = gOnDisk.count("analogsticks.led") > 0;
        std::cout << "led: commands run " << gCommands.size() << "; system.cfg written " << gSystemCfgWrites << " time(s); analogsticks.led "
                  << (saved ? "saved: " + gOnDisk["analogsticks.led"] : std::string("not saved")) << "\n";
        if (!saved) { std::cout << "FAIL l02: the LED colour set on the page never reaches system.cfg\n"; failed++; }
    }
    {   // a text-row-only page: updateVal's SystemConf::set, no save function
        fresh(); auto* s = new GuiSettings();
''' + ("        s->addSaveFunc([] {});\n" if fixed else "") + r'''        SystemConf::getInstance()->set("moonlight.host", "192.0.2.1"); s->close();
        std::cout << "text-rows: system.cfg written " << gSystemCfgWrites << " time(s)\n";
        if (gSystemCfgWrites != 1) { std::cout << "FAIL l02: a page of text rows did not write system.cfg on its close\n"; failed++; }
    }
    {   // a no-change page: nothing set, nothing written
        fresh(); auto* s = new GuiSettings();
''' + ("        s->addSaveFunc([] {});\n" if fixed else "") + r'''        s->close();
        std::cout << "no-change: system.cfg written " << gSystemCfgWrites << " time(s)\n";
        if (gSystemCfgWrites != 0) { std::cout << "FAIL l02: a page with nothing changed wrote system.cfg\n"; failed++; }
    }
    if (failed) return 1;
    std::cout << "3 cases\n";
    return 0;
}
'''
run(harness, "l02")

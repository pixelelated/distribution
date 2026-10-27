"""L-02 (#678): is the analog sticks' LED colour saved to system.cfg when the page closes?

    python3 -I l02-led-not-saved.py <GuiAnalogSticksLedControls.cpp> <GuiSettings.cpp> [--fixed]

The page's applyChanges lambda is extracted as written (from `auto applyChanges`
to its closing `};`) with GuiSettings::close and ::save, over doubles:
runSystemCommand records the command; SystemConf keeps the real rule (set marks
the key changed, saveSystemConf writes only what changed, GuiSettings::save is
the only caller on this path). A slider moved once, then BACK. Expected: the
key in system.cfg. At the pin the page has no save function, save() returns at
its `!mSaveFuncs.size()` and nothing is written -- the case FAILs. --fixed adds
one empty save function to the page (the control), and the case passes.
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
    auto* s = new GuiSettings();
''' + ("    s->addSaveFunc([] {});\n" if fixed else "") + r'''
    applyChanges();               // one slider step
    s->close();                   // BACK
    const bool saved = gOnDisk.count("analogsticks.led") > 0;
    std::cout << "commands run " << gCommands.size() << "; system.cfg written " << gSystemCfgWrites << " time(s); analogsticks.led "
              << (saved ? "saved: " + gOnDisk["analogsticks.led"] : std::string("not saved")) << "\n";
    if (!saved) { std::cout << "FAIL l02: the LED colour set on the page never reaches system.cfg\n"; return 1; }
    return 0;
}
'''
run(harness, "l02")

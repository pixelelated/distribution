"""Run the actual GPU save callback and OptionList selection methods (#436).

Only the settings store, command runner and rendering are replaced. The
empty-capability case must not write a preference or invoke a command.
Accept a source tree argument to demonstrate failure against the old code.
"""
from pathlib import Path
import subprocess
import sys
import tempfile

tree = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
menu = (tree / "es-app/src/guis/GuiMenu.cpp").read_text()
options = (tree / "es-core/src/components/OptionListComponent.h").read_text()


def body(source, signature):
    start = source.index(signature)
    brace = source.index("{", start)
    end, depth = brace + 1, 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[start:end]


methods = "\n".join(body(options, signature) for signature in [
    "std::vector<T> getSelectedObjects()", "T getSelected()",
    "bool changed()", "bool hasSelection()"])
callback = body(menu, "s->addSaveFunc([selectedGpuGovernor, optionsGpuGovernors]") + ");"
harness = r'''
#include <cassert>
#include <functional>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
static void require(bool value) { if (!value) throw std::runtime_error("contract failed"); }
struct SystemConf {
    std::string saved; int writes = 0;
    static SystemConf* getInstance() { static SystemConf state; return &state; }
    void set(const std::string& key, const std::string& value) {
        require(key == "system.gpuperf"); saved = value; ++writes;
    }
};
static std::vector<std::string> commands;
namespace Utils { namespace Platform {
    void runSystemCommand(const std::string& command, const std::string&, void*) {
        commands.push_back(command);
    }
}}
template<class T> struct OptionListComponent {
    struct Entry { T object; bool selected; };
    std::vector<Entry> mEntries;
    T firstSelected;
    bool mMultiSelect = false;
''' + methods + r'''
};
struct SettingsPage {
    std::function<void()> save;
    void addSaveFunc(std::function<void()> fn) { save = fn; }
};
int main() {
    int passed = 0;
    for (std::string name : {"absent", "absent-retained", "no-selection",
                             "unchanged", "changed", "fallback"}) {
        auto state = SystemConf::getInstance();
        state->saved = "performance"; state->writes = 0; commands.clear();
        auto optionsGpuGovernors = std::make_shared<OptionListComponent<std::string>>();
        std::string selectedGpuGovernor = name == "absent" ? "" : "performance";
        if (name == "absent") state->saved.clear();
        optionsGpuGovernors->firstSelected = selectedGpuGovernor;
        if (name == "no-selection") optionsGpuGovernors->mEntries = {{"default", false}};
        if (name == "unchanged") optionsGpuGovernors->mEntries = {{"performance", true}};
        if (name == "changed" || name == "fallback")
            optionsGpuGovernors->mEntries = {{"default", true}, {"performance", false}};
        if (name == "fallback") optionsGpuGovernors->firstSelected.clear();
        SettingsPage page; auto s = &page;
''' + callback + r'''
        try { page.save(); }
        catch (const std::exception& error) {
            std::cerr << "FAIL " << name << ": " << error.what() << "\n"; return 1;
        }
        if (name == "absent" || name == "absent-retained" || name == "no-selection") {
            require(state->writes == 0 && commands.empty());
            require(state->saved == selectedGpuGovernor);
        } else {
            const bool changed = name != "unchanged";
            require(state->writes == (changed ? 1 : 0));
            require(state->saved == (changed ? "default" : "performance"));
            require(commands.size() == 1);
            require(commands[0].find("gpu_performance_level " + state->saved + "\"") != std::string::npos);
        }
        std::cout << "PASS " << name << "\n"; ++passed;
    }
    require(passed == 6);
}
'''
with tempfile.TemporaryDirectory(prefix="es-gpu-governor-") as directory:
    root = Path(directory)
    source, binary = root / "test.cpp", root / "test"
    source.write_text(harness)
    # Match release builds: getSelected's assert is disabled, but vector::at
    # still throws. Contract checks above deliberately remain active.
    subprocess.run(["g++", "-std=c++17", "-DNDEBUG", "-Wall", "-Wextra",
                    str(source), "-o", str(binary)], check=True)
    subprocess.run([str(binary)], check=True)

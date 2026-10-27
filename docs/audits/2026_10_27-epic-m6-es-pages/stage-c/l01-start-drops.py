"""L-01 (#678): does START (CLOSE) keep an open settings page's choice?

    python3 -I l01-start-drops.py <GuiSettings.cpp> [--fixed]

GuiSettings::input, ::close and ::save are extracted as written (balanced
braces, strings and comments skipped) and compiled over doubles: a Window
whose stack the page is pushed on, ViewController at the stack's bottom, an
InputConfig that maps "back" and "start", and Settings / SystemConf with the
real stores' rule (a set of the held value changes nothing; saveFile writes
only after a change). A page is given one save function that sets a switch's
key, as addSwitch's does (GuiSettings.cpp:408-413), with the switch moved.

Case BACK: the page closes; the key is written and the file saved once.
Case START: the expectation is the same. At the pin START deletes the page
(`delete window->peekGui()`), no save function runs, and the case FAILs --
which is the lead. --fixed replaces START's deletion loop with one that
closes each GuiSettings page through close() (the constructed variant, to
show the case can pass); it is not a proposed fix, only the test's control.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

src = Path(sys.argv[1]).read_text()
fixed = "--fixed" in sys.argv

def function(head):
    m = re.search(head, src, re.M)
    if not m:
        sys.exit("FAIL l01: %s not found" % head)
    i = src.index("{", m.end() - 1)
    depth, j = 0, i
    while True:
        c = src[j]
        if src.startswith("//", j):
            j = src.index("\n", j); continue
        if c in "\"'":
            j += 1
            while src[j] != c:
                j += 2 if src[j] == "\\" else 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[m.start():j + 1]
        j += 1

close_fn = function(r"^void GuiSettings::close\(\)")
save_fn = function(r"^void GuiSettings::save\(\)")
input_fn = function(r"^bool GuiSettings::input\(InputConfig\* config, Input input\)")
loop = "while(window->peekGui() && window->peekGui() != ViewController::get())\n\t\t\tdelete window->peekGui();"
if loop not in input_fn:
    sys.exit("FAIL l01: START's deletion loop is not as the pin writes it -- this test models the pin")
if fixed:
    input_fn = input_fn.replace(loop, "while(window->peekGui() && window->peekGui() != ViewController::get())\n\t\t\twindow->peekGui()->closeForTest();")

harness = r'''
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <vector>
struct Input { int value = 1; std::string name; };
struct InputConfig { bool isMappedTo(const std::string& n, Input in) { return in.name == n; } };
#define BUTTON_BACK "back"
static int gSettingsWrites = 0;
struct Settings {
    std::map<std::string, bool> b; bool changed = false;
    static Settings* getInstance() { static Settings s; return &s; }
    bool getBool(const std::string& k) { return b.count(k) && b[k]; }
    bool setBool(const std::string& k, bool v) { if (getBool(k) == v) return false; b[k] = v; changed = true; return true; }
    bool saveFile() { if (!changed) return false; changed = false; gSettingsWrites++; return true; }
};
struct SystemConf { static SystemConf* getInstance() { static SystemConf c; return &c; } bool saveSystemConf() { return false; } };
struct GuiComponent;
struct Window {
    std::vector<GuiComponent*> stack;
    GuiComponent* peekGui() { return stack.empty() ? nullptr : stack.back(); }
    void removeGui(GuiComponent* g) { for (size_t i = 0; i < stack.size(); i++) if (stack[i] == g) { stack.erase(stack.begin() + i); return; } }
};
struct GuiComponent {
    Window* mWindow;
    explicit GuiComponent(Window* w) : mWindow(w) {}
    virtual ~GuiComponent() { mWindow->removeGui(this); }   // GuiComponent.cpp:28-30's removal
    virtual bool input(InputConfig*, Input) { return false; }
    virtual void closeForTest() { delete this; }
};
struct ViewController : GuiComponent {
    using GuiComponent::GuiComponent;
    static ViewController*& inst() { static ViewController* v = nullptr; return v; }
    static GuiComponent* get() { return inst(); }
};
struct GuiSettings : GuiComponent {
    using GuiComponent::GuiComponent;
    bool mDoSave = true;
    std::vector<std::function<void()>> mSaveFuncs;
    std::function<void()> mOnFinalizeFunc;
    std::string mCloseButton = "start";
    void addSaveFunc(const std::function<void()>& f) { mSaveFuncs.push_back(f); }
    void close();
    void save();
    bool input(InputConfig* config, Input input) override;
    void closeForTest() override { close(); }
};
''' + close_fn + "\n" + save_fn + "\n" + input_fn + r'''
static int failed = 0;
static void check(bool ok, const std::string& what) { if (!ok) { std::cout << "FAIL l01: " << what << "\n"; failed++; } }
static void run(const std::string& key)
{
    Settings::getInstance()->b.clear(); Settings::getInstance()->changed = false; gSettingsWrites = 0;
    Window w; ViewController vc(&w); ViewController::inst() = &vc; w.stack.push_back(&vc);
    auto* parent = new GuiSettings(&w); w.stack.push_back(parent);
    auto* page = new GuiSettings(&w); w.stack.push_back(page);
    bool switchState = true;                                  // the player moved the switch
    page->addSaveFunc([switchState] { Settings::getInstance()->setBool("ScrapeNames", switchState); });
    bool finalized = false;
    page->mOnFinalizeFunc = [&finalized] { finalized = true; };
    InputConfig cfg; Input in; in.name = key;
    page->input(&cfg, in);
    bool kept = Settings::getInstance()->getBool("ScrapeNames");
    check(kept && gSettingsWrites == 1 && finalized,
          key + ": the moved switch " + (kept ? "kept" : "dropped") + ", es_settings.cfg written " + std::to_string(gSettingsWrites)
          + " time(s), onFinalize " + (finalized ? "ran" : "did not run"));
    while (w.stack.size() > 1) w.peekGui()->closeForTest();
}
int main()
{
    run("back");
    run("start");
    if (failed) return 1;
    std::cout << "2 cases\n";
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix="l01-", dir="/workspace/tmp/m6-t31/tmp") as d:
    d = Path(d)
    (d / "a.cpp").write_text(harness)
    b = subprocess.run(["g++", "-std=c++17", "-O0", "-g", "-fsanitize=address,undefined", str(d / "a.cpp"), "-o", str(d / "a")],
                       capture_output=True, text=True)
    if b.returncode:
        print("FAIL l01: the extract does not compile\n" + b.stderr[-2000:]); sys.exit(2)
    r = subprocess.run([str(d / "a")], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode and "FAIL" not in r.stdout:
        print("FAIL l01: rc %d %s" % (r.returncode, r.stderr[-600:]))
    sys.exit(1 if r.returncode else 0)

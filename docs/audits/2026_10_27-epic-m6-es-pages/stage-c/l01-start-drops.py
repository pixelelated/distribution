"""L-01 / S1 (#678, #1236): does closing from the top save what BACK would have saved (D-UI-128)?

    python3 -I l01-start-drops.py <GuiSettings.cpp> [--fixed]

GuiSettings::input, ::close, ::save, ::onMouseClick and (where the source has
it) ::closeAllFromTop are extracted as written (t31extract: balanced braces,
strings and comments skipped) and compiled under AddressSanitizer over
doubles: a Window whose stack the pages are pushed on (`peekGui`,
`getGuiStackSize`, the destructor's removal as GuiComponent.cpp:28-30 does),
ViewController at the stack's bottom, an InputConfig mapping "back" and
"start", and Settings with the real store's rule (a set of the held value
changes nothing; saveFile writes only after a change). Each settings page has
one save function that sets a switch's key, as addSwitch's does
(GuiSettings.cpp:408-413), with the switch moved.

Five cases:
  back          B on one page: its key written, the file saved, onFinalize run (the control).
  start         START on the same page: the same expected.
  outside-click a left click outside the menu: the same expected.
  mixed-stack   view, settings A, plain P, settings B on top; START: A and B saved, P deleted, the stack at the view.
  finalize-push view, A, B; B's onFinalize pushes a plain page C; START: B saved, C on top, A still open and unsaved.
At the pin START and the click delete without close(): every case but back FAILs.
--fixed is the stage-C control (START's loop replaced by close() per page); it
applies only to the pin's loop and is not the fix.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
fixed = "--fixed" in sys.argv
close_fn = function(src, r"^void GuiSettings::close\(\)", "l01")
save_fn = function(src, r"^void GuiSettings::save\(\)", "l01")
input_fn = function(src, r"^bool GuiSettings::input\(InputConfig\* config, Input input\)", "l01")
click_fn = function(src, r"^bool GuiSettings::onMouseClick\(", "l01")
walk_fn = function(src, r"^void GuiSettings::closeAllFromTop\(", "l01") if re.search(r"^void GuiSettings::closeAllFromTop\(", src, re.M) else ""
loop = "while(window->peekGui() && window->peekGui() != ViewController::get())\n\t\t\tdelete window->peekGui();"
if fixed:
    if loop not in input_fn:
        sys.exit("FAIL l01: --fixed models the pin's START loop, which this source no longer has")
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
    int getGuiStackSize() { return (int)stack.size(); }
    void pushGui(GuiComponent* g) { stack.push_back(g); }
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
struct Menu { bool isMouseOver() { return false; } };
struct GuiSettings : GuiComponent {
    using GuiComponent::GuiComponent;
    bool mDoSave = true;
    std::vector<std::function<void()>> mSaveFuncs;
    std::function<void()> mOnFinalizeFunc;
    std::string mCloseButton = "start";
    Menu mMenu;
    std::string key;
    void addSaveFunc(const std::function<void()>& f) { mSaveFuncs.push_back(f); }
    void close();
    void save();
    bool input(InputConfig* config, Input input) override;
    virtual bool onMouseClick(int button, bool pressed, int x, int y);
    static void closeAllFromTop(Window* window);
    void closeForTest() override { close(); }
};
''' + close_fn + "\n" + save_fn + "\n" + input_fn + "\n" + click_fn + "\n" + walk_fn + r'''
static int failed = 0;
static void check(bool ok, const std::string& what) { if (!ok) { std::cout << "FAIL l01: " << what << "\n"; failed++; } }
static int finalized = 0;
static GuiSettings* page(Window& w, const std::string& key)
{
    auto* p = new GuiSettings(&w); p->key = key; w.pushGui(p);
    p->addSaveFunc([key] { Settings::getInstance()->setBool(key, true); });   // the switch moved
    p->mOnFinalizeFunc = [] { finalized++; };
    return p;
}
static bool saved(const std::string& k) { return Settings::getInstance()->getBool(k); }
static void reset() { Settings::getInstance()->b.clear(); Settings::getInstance()->changed = false; gSettingsWrites = 0; finalized = 0; }
static void teardown(Window& w) { while (w.stack.size() > 1) w.peekGui()->closeForTest(); }
int main()
{
    InputConfig cfg;
    { // back, start: one page over the view
        for (std::string key : { std::string("back"), std::string("start") }) {
            reset(); Window w; ViewController vc(&w); ViewController::inst() = &vc; w.pushGui(&vc);
            auto* p = page(w, "ScrapeNames"); Input in; in.name = key; p->input(&cfg, in);
            check(saved("ScrapeNames") && gSettingsWrites == 1 && finalized == 1 && w.stack.size() == 1,
                  key + ": the moved switch " + (saved("ScrapeNames") ? "kept" : "dropped") + ", es_settings.cfg written " + std::to_string(gSettingsWrites) + " time(s), onFinalize ran " + std::to_string(finalized) + " time(s)");
            teardown(w);
        }
    }
    { // outside click
        reset(); Window w; ViewController vc(&w); ViewController::inst() = &vc; w.pushGui(&vc);
        auto* p = page(w, "ScrapeNames"); p->onMouseClick(1, true, -1, -1);
        check(saved("ScrapeNames") && finalized == 1 && w.stack.size() == 1,
              std::string("outside-click: the moved switch ") + (saved("ScrapeNames") ? "kept" : "dropped") + ", onFinalize ran " + std::to_string(finalized) + " time(s)");
        teardown(w);
    }
    { // mixed stack: view, A, plain P, B; START from B
        reset(); Window w; ViewController vc(&w); ViewController::inst() = &vc; w.pushGui(&vc);
        page(w, "A"); auto* P = new GuiComponent(&w); w.pushGui(P); auto* B = page(w, "B");
        Input in; in.name = "start"; B->input(&cfg, in);
        check(saved("A") && saved("B") && finalized == 2 && w.stack.size() == 1,
              std::string("mixed-stack: A ") + (saved("A") ? "saved" : "dropped") + ", B " + (saved("B") ? "saved" : "dropped") + ", onFinalize ran " + std::to_string(finalized) + " time(s), " + std::to_string(w.stack.size() - 1) + " page(s) left over the view");
        teardown(w);
    }
    { // an onFinalize that pushes a page stops the walk
        reset(); Window w; ViewController vc(&w); ViewController::inst() = &vc; w.pushGui(&vc);
        auto* A = page(w, "A"); auto* B = page(w, "B");
        GuiComponent* C = nullptr;
        B->mOnFinalizeFunc = [&w, &C] { finalized++; C = new GuiComponent(&w); w.pushGui(C); };
        Input in; in.name = "start"; B->input(&cfg, in);
        bool cOnTop = C != nullptr && w.peekGui() == C;
        bool aOpen = w.stack.size() == 3 && w.stack[1] == A;
        check(saved("B") && !saved("A") && cOnTop && aOpen,
              std::string("finalize-push: B ") + (saved("B") ? "saved" : "dropped") + ", A " + (saved("A") ? "saved" : "unsaved") + ", the pushed page " + (cOnTop ? "on top" : "gone") + ", A " + (aOpen ? "still open" : "closed"));
        teardown(w);
    }
    if (failed) return 1;
    std::cout << "5 cases\n";
    return 0;
}
'''
run(harness, "l01")

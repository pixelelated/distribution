"""S13 (#678, #1255): does a text row's editor reopen on the value it last saved?

    python3 -I s13-text-row.py <GuiSettings.cpp>

GuiSettings::addInputTextRow is extracted as written (t31extract) and compiled
under AddressSanitizer over doubles: the menu theme and its font, the row's
components, ComponentListRow (which keeps the accept handler), and the two
text editors (GuiTextEditPopup / GuiTextEditPopupKeyboard), which record the
text they open with and keep the OK callback. The row is built with value A
and an onsave that records what it is handed. Two cases:
  reopen  open the editor, OK with B; open it again: it opens on B (the pin: A).
  ok-only reopen and OK without editing: onsave gets B (the pin: A written back over B).
A third, the control, holds at the pin too: the first open shows A.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
fn = function(src, r"^void GuiSettings::addInputTextRow\(", "s13")
harness = r'''
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
struct Vector2f { float x_, y_; Vector2f(float a = 0, float b = 0) : x_(a), y_(b) {} float x() const { return x_; } };
struct Font { Vector2f sizeText(const std::string& t) const { return Vector2f((float)t.size(), 1); } float getLetterHeight() const { return 1; } };
enum Alignment { ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER };
struct Window;
struct GuiComponent { GuiComponent() {} explicit GuiComponent(Window*) {} virtual ~GuiComponent() {} void setSize(float, float) {} };
struct TextComponent : GuiComponent {
    std::string value;
    TextComponent(Window*, const std::string& t, std::shared_ptr<Font>, unsigned int, Alignment = ALIGN_LEFT) : value(t) {}
    void setHorizontalAlignment(Alignment) {}
    void setValue(const std::string& v) { value = v; }
    std::shared_ptr<Font> getFont() { return std::make_shared<Font>(); }
};
struct ImageComponent : GuiComponent { explicit ImageComponent(Window*) {} void setImage(const std::string&) {} void setResize(Vector2f) {} void setFlipX(bool) {} };
struct Theme { struct { std::shared_ptr<Font> font = std::make_shared<Font>(); unsigned int color = 0; } Text; struct { std::string arrow; } Icons; };
struct ThemeData { static std::shared_ptr<Theme> getMenuTheme() { static auto t = std::make_shared<Theme>(); return t; } };
struct EsLocale { static bool isRTL() { return false; } };
namespace Renderer { inline int getScreenWidth() { return 640; } }
struct Settings { static Settings* getInstance() { static Settings s; return &s; } bool getBool(const std::string&) { return false; } };
struct ComponentListRow {
    std::function<void()> accept;
    void addElement(std::shared_ptr<GuiComponent>, bool) {}
    void makeAcceptInputHandler(const std::function<void()>& f) { accept = f; }
};
static std::string gOpenedWith; static std::function<void(const std::string&)> gOk;
struct GuiTextEditPopup : GuiComponent {
    GuiTextEditPopup(Window*, const std::string&, const std::string& data, const std::function<void(const std::string&)>& ok, bool) { gOpenedWith = data; gOk = ok; }
};
struct GuiTextEditPopupKeyboard : GuiTextEditPopup { using GuiTextEditPopup::GuiTextEditPopup; };
struct Window { void pushGui(GuiComponent* g) { delete g; } };
struct Menu { void updateSize() {} };
struct GuiSettings {
    Window* mWindow; Menu mMenu; ComponentListRow last;
    void addRow(const ComponentListRow& r) { last = r; }
    void addInputTextRow(const std::string& title, const std::string& value, bool password,
        const std::function<void(Window*, std::string, std::string, const std::function<void(std::string)>&)>& customEditor = nullptr,
        const std::function<void(std::string)>& onsave = nullptr);
};
''' + fn + r'''
int main()
{
    Window w; GuiSettings s; s.mWindow = &w;
    std::vector<std::string> saved;
    s.addInputTextRow("JOYSTICK NAME", "A", false, nullptr, [&saved](std::string v) { saved.push_back(v); });
    int failed = 0;
    s.last.accept();                                   // open
    if (gOpenedWith != "A") { std::cout << "FAIL s13: the first open showed '" << gOpenedWith << "', not A (control)\n"; failed++; }
    gOk("B");                                          // OK with B
    s.last.accept();                                   // reopen
    std::cout << "reopen: the editor opened on '" << gOpenedWith << "'\n";
    if (gOpenedWith != "B") { std::cout << "FAIL s13: reopen: the editor opened on the first value, not the saved one\n"; failed++; }
    gOk(gOpenedWith);                                  // OK without editing
    std::cout << "ok-only: onsave handed '" << saved.back() << "'\n";
    if (saved.back() != "B") { std::cout << "FAIL s13: ok-only: the old value was written back over the new\n"; failed++; }
    if (failed) return 1;
    std::cout << "3 cases\n";
    return 0;
}
'''
run(harness, "s13")

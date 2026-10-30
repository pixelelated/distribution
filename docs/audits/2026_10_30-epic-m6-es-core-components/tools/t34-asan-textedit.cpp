// T34 (#681) PL-03, 3.20: the text field's onFocusLost, lifted verbatim
// (TextEditComponent.cpp:44-47), posting raw this to a queue that drains
// later, as Window::postToUiThread does; the field is deleted before the
// drain. Built with -fsanitize=address: a use after free is the positive.
#include <functional>
#include <string>
#include <vector>
struct Window { std::vector<std::function<void()>> q;
	void postToUiThread(const std::function<void()>& f) { q.push_back(f); }
	void drain() { auto qq = q; q.clear(); for (auto& f : qq) f(); } };
struct IconsT { std::string textinput_ninepatch, textinput_ninepatch_active; };
struct MenuThemeT { IconsT Icons; };
namespace ThemeData { inline MenuThemeT* getMenuTheme() { static MenuThemeT t; return &t; } }
struct Box { void setImagePath(const std::string&) {} };
struct TextEdit {
	Window* mWindow; bool mFocused = true; Box mBox; std::string mText = "a name"; bool mEditing = true;
	void stopEditing() { mEditing = false; mText.clear(); }
	void onFocusLost() {
#include "x_textedit_focuslost.inc"
	}
};
int main() {
	Window w;
	TextEdit* t = new TextEdit{&w};
	t->onFocusLost(); // posts [this] { stopEditing(); }
	delete t;         // the page closes before the queue drains
	w.drain();        // stopEditing() on the freed field
	return 0;
}

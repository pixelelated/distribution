// T34 (#681) 3.19: a DOUBLE of the option list popup's shape, not its lines
// (OptionListComponent.h:158 needs MenuComponent and the theme behind it): a
// button whose std::function deletes the popup that owns the button, then
// returns, with nothing above it touching the popup (T31's invariant). Built
// with -fsanitize=address: clean is the invariant holding for the shape.
#include <functional>
#include <memory>
#include <vector>
struct Button { std::function<void()> fn; bool press() { fn(); return true; } };
struct Popup {
	std::vector<std::unique_ptr<Button>> buttons;
	Popup() { auto b = std::make_unique<Button>(); b->fn = [this] { delete this; }; buttons.push_back(std::move(b)); }
};
int main() { Popup* p = new Popup(); Button* b = p->buttons[0].get(); return b->press() ? 0 : 1; }

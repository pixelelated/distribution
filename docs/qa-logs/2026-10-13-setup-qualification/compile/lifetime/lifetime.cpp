
#include <algorithm>
#include <cassert>
#include <deque>
#include <functional>
#include <iostream>
#include <memory>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
#define _(s) std::string(s)
enum LogLevel { LogInfo };
struct LogLine { template<class T> LogLine& operator<<(const T&) { return *this; } };
#define LOG(level) LogLine()
static int cancels = 0, starts = 0, connected = 0;
static std::string status = "waiting";
namespace Utils { namespace Platform {
int runSystemCommand(const std::string& cmd, const std::string&, void*) {
    if (cmd == "/usr/bin/cloud_oauth cancel") ++cancels;
    return 0;
}
std::vector<std::string> GetShOutputLines(const std::string& cmd) {
    assert(cmd == "/usr/bin/cloud_oauth status");
    return status.empty() ? std::vector<std::string>() : std::vector<std::string>{status};
}
} namespace String {
std::string trim(const std::string& s) { return s; }
std::string format(const char* s, const char*) { return s; }
} namespace FileSystem { bool exists(const std::string&) { return false; } }
}
namespace Renderer {
int getScreenWidth() { return 640; }
int getScreenHeight() { return 480; }
struct ScreenSettings { static bool fullScreenMenus() { return false; } };
}
struct Gui;
struct Window { std::vector<Gui*> stack; void pushGui(Gui* s) { stack.push_back(s); } };
struct Gui {
    Window* window;
    explicit Gui(Window* w) : window(w) {}
    virtual ~Gui() {
        auto& v = window->stack;
        v.erase(std::remove(v.begin(), v.end(), this), v.end());
    }
};
struct Menu {
    std::vector<std::pair<std::string, std::function<void()>>> buttons;
    void setSize(float, float) {}
    void setPosition(float, float) {}
    void clearButtons() { buttons.clear(); }
    void addButton(const std::string& s, const std::string&, std::function<void()> f) {
        buttons.emplace_back(s, f);
    }
};
struct GuiSettings : Gui {
    Menu menu;
    std::function<void()> finalize;
    std::vector<std::pair<std::string, std::function<void()>>> choices;
    GuiSettings(Window* w, const std::string&) : Gui(w) {}
    Menu& getMenu() { return menu; }
    void setSubTitle(const std::string&) {}
    void addGroup(const std::string&) {}
    void onFinalize(std::function<void()> f) { finalize = f; }
    void close() { if (finalize) finalize(); delete this; }
    void addWithDescription(const std::string& s, const std::string&, std::nullptr_t,
        std::function<void()> f, const std::string&, bool, bool) { choices.emplace_back(s, f); }
};
enum class GuiMsgBoxIcon { ICON_ERROR };
struct GuiMsgBox : Gui {
    std::string text;
    std::vector<std::function<void()>> actions;
    GuiMsgBox(Window* w, const std::string& t, const std::string&, std::function<void()> a,
        const std::string&, std::function<void()> b,
        GuiMsgBoxIcon = GuiMsgBoxIcon::ICON_ERROR) : Gui(w), text(t), actions{a, b} {}
    // Same deletion/copy order as the shipped GuiMsgBox::deleteMeAndCall.
    void press(unsigned i) { auto action = actions.at(i); delete this; if (action) action(); }
};
struct CloudBackend { std::string name, label; };
struct CloudOAuthReady {
    bool started = true, onDevice = true;
    std::string url = "http://synthetic.invalid/fixture", exitHint = "SELECT + START";
};
namespace CloudText {
std::string providerSubtitle(const std::string&, const std::string& s) { return s; }
}
std::string cloudShellQuote(const std::string& s) { return s; }
static void cloudSetupAddProse(GuiSettings*, Window*, const std::string&, const std::string&) {}
static void cloudSetupAddSpacer(GuiSettings*, Window*) {}
static void cloudSetupAddInfoRow(GuiSettings*, Window*, const std::string&, bool = false) {}
static void cloudSetupAddQrRow(GuiSettings*, Window*, const std::string&,
    const std::vector<std::pair<std::string, bool>>&) {}
static std::set<GuiSettings*> sOAuthSessionPages;
struct ApiSystem {
    struct Result { bool ok; std::string after; };
    std::deque<Result> replies;
    std::vector<bool> phone;
    static ApiSystem* getInstance() { static ApiSystem api; return &api; }
    bool launchCloudSignIn(Window*, bool usePhone) {
        assert(!replies.empty());
        phone.push_back(usePhone);
        const auto r = replies.front(); replies.pop_front(); status = r.after;
        return r.ok;
    }
};

static void cloudOAuthOwnSession(GuiSettings* s)
{
	sOAuthSessionPages.insert(s);
	s->onFinalize([s]
	{
		if (sOAuthSessionPages.erase(s) == 0)
			return;   // handed on: the next page owns the session
		LOG(LogInfo) << "cloud_oauth: the sign-in was left; cancelling its session";
		Utils::Platform::runSystemCommand("/usr/bin/cloud_oauth cancel", "", nullptr);
	});
}
static void cloudSetupPresent(Window* window, GuiSettings* s, GuiSettings* prev, bool completeInstructions = false)
{
	if (prev != nullptr)
		sOAuthSessionPages.erase(prev);   // handed on, not left
	if (!Renderer::ScreenSettings::fullScreenMenus())
	{
		float width = Renderer::getScreenWidth() * 0.90f;
		if (!completeInstructions && width > Renderer::getScreenHeight())
			width = (float)Renderer::getScreenHeight();
		// Instruction-only rows cannot scroll into view by cursor movement.
		// Resize AND position this page; GuiSettings otherwise keeps its
		// 15% top offset, pushing a taller page's buttons below the panel.
		s->getMenu().setSize(width, Renderer::getScreenHeight() * (completeInstructions ? 0.90f : 0.75f));
		if (completeInstructions)
			s->getMenu().setPosition((Renderer::getScreenWidth() - width) / 2,
				Renderer::getScreenHeight() * 0.025f);
	}
	window->pushGui(s);
	if (prev != nullptr)
		prev->close();
}
static void cloudSetupSetButtons(GuiSettings* s, const std::function<void()>& onContinue)
{
	s->getMenu().clearButtons();
	// One word each. A button bar is read at a glance and the page title
	// already says what is being exited, so "EXIT SETUP" spent width on a
	// word that carried nothing -- and the wider the buttons, the more two
	// of them read as a single control.
	s->getMenu().addButton(_("EXIT"), _("exit setup"), [s] { s->close(); });
	if (onContinue != nullptr)
		s->getMenu().addButton(_("CONTINUE"), _("continue"), onContinue);
}
// The real broker start and connected destination do external work. Model only
// their ownership boundary, keeping the extracted page/callback code unchanged.
static void cloudOAuthStart(Window* w, const CloudBackend&, const std::string& name, GuiSettings* prev) {
    assert(name.size() > 128); ++starts; ++cancels; status = "waiting";
    auto next = new GuiSettings(w, "new attempt");
    cloudOAuthOwnSession(next); cloudSetupPresent(w, next, prev);
}
static void cloudOAuthShowConnected(Window* w, const CloudBackend&, const std::string& name, GuiSettings* prev) {
    assert(name.size() > 128); ++connected;
    cloudSetupPresent(w, new GuiSettings(w, "connected"), prev);
}
static void cloudOAuthShowSignIn(Window*, CloudBackend, std::string, GuiSettings*, bool, const CloudOAuthReady&);

static void cloudOAuthOpenSignIn(Window* window, CloudBackend backend,
	std::string remoteName, GuiSettings* page, bool usePhone,
	std::function<void()> onReturn)
{
	if (ApiSystem::getInstance()->launchCloudSignIn(window, usePhone))
	{
		if (onReturn)
			onReturn();
		return;
	}

	// A completed authorization wins even if the window failed to return.
	const auto lines = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth status");
	const std::string status = lines.empty() ? "" : Utils::String::trim(lines.front());
	if (status == "signed-in")
	{
		cloudOAuthShowConnected(window, backend, remoteName, page);
		return;
	}

	// The bool also covers a failed wait, so do not claim every failure was
	// at startup. No OK action returns to a page still claiming to open.
	window->pushGui(new GuiMsgBox(window,
		_("THE SIGN-IN WINDOW DID NOT OPEN OR STOPPED WORKING.\n\nTRY AGAIN, OR CANCEL SIGN-IN."),
		_("TRY AGAIN"), [window, backend, remoteName, page, usePhone, onReturn]
		{
			// Recheck on the press: authorization can finish or expire while
			// the question is open. A waiting attempt keeps its phone pairing.
			const auto lines = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth status");
			const std::string status = lines.empty() ? "" : Utils::String::trim(lines.front());
			if (status == "signed-in")
				cloudOAuthShowConnected(window, backend, remoteName, page);
			else if (status == "waiting")
				cloudOAuthOpenSignIn(window, backend, remoteName, page, usePhone, onReturn);
			else
				cloudOAuthStart(window, backend, remoteName, page);
		},
		_("CANCEL SIGN-IN"), [page] { page->close(); }, GuiMsgBoxIcon::ICON_ERROR));
}
static void cloudOAuthShowSignIn(Window* window, CloudBackend backend,
	std::string remoteName, GuiSettings* prev, bool usePhone,
	const CloudOAuthReady& ready)
{
	auto s = new GuiSettings(window, _("CONNECT CLOUD STORAGE"));
	s->setSubTitle(CloudText::providerSubtitle(backend.name, backend.label));

	// The address carries its own PIN in its path. ADDRESS and PIN are still
	// reported by `info` for anything driving this from a shell, but the page
	// has nothing to do with them separately -- two numbers on one screen is
	// what made "code" ambiguous the first time.
	const std::string url = ready.url;
	const bool onDevice = ready.onDevice;
	const std::string exitHint = ready.exitHint;

	if (!ready.started)
	{
		cloudSetupAddProse(s, window, _("SIGN-IN DID NOT START"),
			_("THE DEVICE COULD NOT REACH THE PROVIDER. CHECK THE NETWORK AND TRY AGAIN."));
		// One button, and it goes back. This page used to carry CONTINUE as
		// well, which offered to continue with a sign-in that had not begun.
		s->getMenu().clearButtons();
		s->getMenu().addButton(_("GO BACK"), _("go back"), [s] { s->close(); });
		cloudOAuthOwnSession(s);
		cloudSetupPresent(window, s, prev);
		return;
	}

	// Typing on the handheld: nothing to read off the screen, nothing to
	// scan. Open the provider's page and get out of the way. The keyboard
	// raises itself on the first field, so there is no instruction to give
	// that the page does not give better.
	const bool openImmediately = onDevice && !usePhone;
	if (openImmediately)
	{
		cloudSetupAddProse(s, window, _("SIGNING IN"),
			_("THE PROVIDER'S PAGE IS OPENING. A KEYBOARD APPEARS WHEN YOU PICK A BOX; MOVE WITH THE D-PAD AND CHOOSE WITH A."));
		cloudSetupAddSpacer(s, window);
		cloudSetupAddInfoRow(s, window,
			Utils::String::format(_("TO COME BACK HERE, PRESS %s").c_str(), exitHint.c_str()));
		cloudSetupAddInfoRow(s, window, _("THEN CHOOSE 'CONTINUE' TO FINISH"));
	}
	else
	{
		// The phone is a keyboard, not the place the sign-in happens. Saying
		// "sign in on your phone" sent people looking for a provider page
		// there; the page is on the handheld either way.
		const std::string qrPath = "/tmp/cloud-oauth-qr.png";
		Utils::Platform::runSystemCommand(
			"rm -f " + qrPath + "; /usr/bin/qrencode -o " + qrPath
			+ " -s 8 -m 4 --background=FFFFFF --foreground=000000 -l M "
			+ cloudShellQuote(url), "", nullptr);

		std::vector<std::pair<std::string, bool>> lines;
		if (onDevice)
		{
			s->addGroup(_("USE YOUR PHONE AS A KEYBOARD"));
			cloudSetupAddSpacer(s, window);
			lines.push_back(std::make_pair(_("SCAN THIS, OR OPEN"), false));
			lines.push_back(std::make_pair(url, true));
			lines.push_back(std::make_pair(_("WHAT YOU TYPE THERE APPEARS HERE"), false));
		}
		else
		{
			// The older route, for an image that cannot host the page: the
			// player signs in on their phone and brings an address back.
			lines.push_back(std::make_pair(_("OPEN THIS IN A BROWSER"), false));
			lines.push_back(std::make_pair(url, true));
			lines.push_back(std::make_pair(_("THE LAST 4 DIGITS ARE A PIN"), false));
			lines.push_back(std::make_pair(_("IT KEEPS OTHERS OFF THIS PAGE"), false));
		}

		if (Utils::FileSystem::exists(qrPath))
			cloudSetupAddQrRow(s, window, qrPath, lines);
		else
			for (auto& line : lines)
				cloudSetupAddInfoRow(s, window, line.first, line.second);

		if (onDevice)
			cloudSetupAddProse(s, window, _("THEN"),
				_("CONNECT YOUR PHONE FIRST, THEN CHOOSE 'CONTINUE', AND THE PROVIDER'S PAGE OPENS ON THIS SCREEN."));
		else
			cloudSetupAddProse(s, window, _("THEN"),
				_("THAT PAGE WALKS YOU THROUGH SIGNING IN. COME BACK HERE AND SELECT 'CONTINUE' WHEN IT SAYS YOU ARE CONNECTED."));
	}

	// Ask cloud_oauth, which asks rclone. Nothing here decides on its own
	// that a sign-in worked.
	//
	// Keep this callback separate so a successful phone-window retry runs
	// the same completion check as its original CONTINUE press.
	auto finishSignIn = [window, backend, remoteName, s]
	{
		auto lines = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth status");
		std::string status = lines.empty() ? "" : Utils::String::trim(lines.front());
		LOG(LogInfo) << "cloud_oauth status=" << status;

		if (status == "signed-in")
		{
			cloudOAuthShowConnected(window, backend, remoteName, s);
			return;
		}
		if (status == "failed")
		{
			window->pushGui(new GuiMsgBox(window,
				_("THE SIGN-IN DID NOT COMPLETE. TRY AGAIN TO START A NEW SIGN-IN."),
				_("TRY AGAIN"), [window, backend, remoteName, s] { cloudOAuthStart(window, backend, remoteName, s); },
				_("CANCEL SIGN-IN"), [s] { s->close(); }));
			return;
		}
		window->pushGui(new GuiMsgBox(window,
			_("STILL WAITING FOR THE SIGN-IN.\n\nFINISH IT, THEN CHOOSE 'CONTINUE' AGAIN."),
			_("OK"), nullptr,
			_("CANCEL SIGN-IN"), [window, s]
			{
				Utils::Platform::runSystemCommand("/usr/bin/cloud_oauth cancel", "", nullptr);
				s->close();
			}));
	};

	// Native CONTINUE checks completion; phone CONTINUE first opens the
	// window while the session is waiting. A failed launch owns its dialog
	// and must not fall through to the generic still-waiting message.
	const bool openOnContinue = onDevice && usePhone;
	cloudSetupSetButtons(s, [window, backend, remoteName, s, openOnContinue, finishSignIn]
	{
		if (openOnContinue)
		{
			auto info = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth status");
			std::string now = info.empty() ? "" : Utils::String::trim(info.front());
			if (now == "waiting")
			{
				cloudOAuthOpenSignIn(window, backend, remoteName, s, true, finishSignIn);
				return;
			}
		}
		// Completion can delete s and its buttons; own the invocation first.
		auto finish = finishSignIn;
		finish();
	});

	cloudOAuthOwnSession(s);
	cloudSetupPresent(window, s, prev);

	// After the page is on the stack, never while it is being built: this
	// blocks for as long as somebody is signing in, and ES is suspended for
	// the duration. The page has to already be there for ES to come back to.
	// backend and remoteName are owned values: presenting s deleted prev,
	// which may have held the callback that supplied them.
	if (openImmediately)
		cloudOAuthOpenSignIn(window, backend, remoteName, s, false, nullptr);
}
static void pressContinue(GuiSettings* page) {
    auto it = std::find_if(page->menu.buttons.begin(), page->menu.buttons.end(),
        [](const auto& entry) { return entry.first == "CONTINUE"; });
    assert(it != page->menu.buttons.end());
    it->second(); // no caller-side copy: the production callback owns its invocation
}
static GuiMsgBox* failure(Window& w) {
    auto dialog = dynamic_cast<GuiMsgBox*>(w.stack.back());
    assert(dialog && dialog->text.find("THE SIGN-IN WINDOW DID NOT OPEN") == 0);
    assert(w.stack.size() == 3); return dialog;
}
int main(int argc, char** argv) {
    assert(argc == 3);
    const bool phone = std::string(argv[1]) == "phone";
    const std::string mode = argv[2];
    Window w;
    auto hub = new GuiSettings(&w, "hub"); w.pushGui(hub);
    auto chooser = new GuiSettings(&w, "chooser"); w.pushGui(chooser);
    cloudOAuthOwnSession(chooser);
    // Heap-backed captures expose borrowing from a predecessor after deletion.
    CloudBackend backend{std::string(256, 'b'), "Synthetic provider"};
    std::string name(256, 'n');
    CloudOAuthReady ready;
    auto api = ApiSystem::getInstance();
    api->replies.push_back({mode == "success", mode == "already-complete" || mode == "success" ? "signed-in" : "waiting"});
    chooser->choices.emplace_back("select", [&w, backend, name, chooser, phone, ready] {
        cloudOAuthShowSignIn(&w, backend, name, chooser, phone, ready);
    });
    chooser->choices.front().second();
    if (phone) pressContinue(dynamic_cast<GuiSettings*>(w.stack.back()));
    assert(cancels == 0 && starts == 0 && api->phone.size() == 1 && api->phone[0] == phone);
    if (mode == "success" || mode == "already-complete") {
        if (!phone && mode == "success") pressContinue(dynamic_cast<GuiSettings*>(w.stack.back()));
        assert(connected == 1 && w.stack.size() == 2);
    } else if (mode == "cancel" || mode == "back") {
        // Shipped GuiMsgBox maps Back to the last button (CANCEL SIGN-IN).
        failure(w)->press(1);
        assert(cancels == 1 && w.stack.size() == 1);
    } else if (mode == "repeat") {
        for (int i = 0; i < 2; ++i) {
            api->replies.push_back({false, "waiting"}); failure(w)->press(0);
            assert(cancels == 0 && starts == 0);
        }
        assert(api->phone.size() == 3); failure(w)->press(1);
        assert(cancels == 1 && w.stack.size() == 1);
    } else if (mode == "retry-success") {
        api->replies.push_back({true, "signed-in"}); failure(w)->press(0);
        if (!phone) pressContinue(dynamic_cast<GuiSettings*>(w.stack.back()));
        assert(connected == 1 && starts == 0 && cancels == 0 && api->phone.size() == 2);
    } else if (mode == "completed-while-prompted") {
        status = "signed-in"; failure(w)->press(0);
        assert(connected == 1 && starts == 0 && cancels == 0 && api->phone.size() == 1);
    } else {
        assert(mode == "ended" || mode == "unknown");
        status = mode == "ended" ? "failed" : ""; failure(w)->press(0);
        assert(starts == 1 && cancels == 1 && connected == 0 && w.stack.size() == 2);
        assert(api->phone.size() == 1);
    }
    for (bool choice : api->phone) assert(choice == phone);
    assert(api->replies.empty());
    while (!w.stack.empty()) {
        auto page = dynamic_cast<GuiSettings*>(w.stack.back()); assert(page); page->close();
    }
    assert(sOAuthSessionPages.empty());
    std::cout << "PASS " << argv[1] << ' ' << mode << '\n';
}

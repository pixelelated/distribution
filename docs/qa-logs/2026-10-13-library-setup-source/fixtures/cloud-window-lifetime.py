#!/usr/bin/env python3
"""UNRUN coordinator fixture: actual OAuth UI functions, ASan, synthetic launch.

Compiles only when explicitly invoked under a coordinator runtime allocation.
No broker/browser/network launches: those calls are doubles. Rendering is not
covered. Source bytes must match the adjacent packet's static-review.json.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


def definition(source, name):
    needle = "static void " + name + "("
    start = source.index(needle)
    while source.index(";", start) < source.index("{", start):
        start = source.index(needle, start + 1)
    pos = source.index("{", start)
    depth = 1
    end = pos + 1
    while depth:
        if source[end] == "{":
            depth += 1
        elif source[end] == "}":
            depth -= 1
        end += 1
    return source[start:end]


PREAMBLE = r'''
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
'''

BOUNDARIES = r'''
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
'''

CASES = r'''
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
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--compiler", required=True)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent.parent
    binding = json.loads((packet / "static-review.json").read_text())
    raw = args.source.read_bytes()
    expected = binding["changed_files"]["es-app/src/guis/GuiMenu.cpp"]["sha256"]
    if hashlib.sha256(raw).hexdigest() != expected:
        raise SystemExit("refuse: source bytes differ from the frozen packet")
    source = raw.decode()
    # Guard the two production caller seams as well as extracting their bodies.
    page = definition(source, "cloudOAuthShowSignIn")
    if "launchCloudSignIn(" in page or page.count("cloudOAuthOpenSignIn(") != 2:
        raise SystemExit("refuse: expected native/phone launch seams missing")
    harness = PREAMBLE
    for name in ("cloudOAuthOwnSession", "cloudSetupPresent", "cloudSetupSetButtons"):
        harness += "\n" + definition(source, name)
    harness += BOUNDARIES
    harness += "\n" + definition(source, "cloudOAuthOpenSignIn")
    harness += "\n" + page + CASES
    args.out.mkdir(parents=False, exist_ok=False)
    cpp, exe = args.out / "lifetime.cpp", args.out / "lifetime"
    cpp.write_text(harness)
    build = subprocess.run([args.compiler, "-std=c++14", "-O1", "-g", "-fsanitize=address",
                            "-fno-omit-frame-pointer", str(cpp), "-o", str(exe)],
                           capture_output=True, text=True, timeout=60)
    (args.out / "compile.stdout").write_text(build.stdout)
    (args.out / "compile.stderr").write_text(build.stderr)
    report = {"source_commit": binding["source_commit"], "source_sha256": expected,
              "scope": "extracted C++ callbacks with UI/API doubles; no real broker or rendering",
              "compile_rc": build.returncode, "cases": [], "rc": 1}
    if build.returncode == 0:
        for route in ("native", "phone"):
            for mode in ("cancel", "back", "repeat", "retry-success", "ended", "unknown",
                         "completed-while-prompted", "already-complete", "success"):
                result = subprocess.run([str(exe.resolve()), route, mode], capture_output=True,
                                        text=True, timeout=5,
                                        env=dict(os.environ, ASAN_OPTIONS="detect_leaks=1:halt_on_error=1"))
                stem = route + "-" + mode
                (args.out / (stem + ".stdout")).write_text(result.stdout)
                (args.out / (stem + ".stderr")).write_text(result.stderr)
                report["cases"].append({"case": stem, "rc": result.returncode,
                                        "pass_line": result.stdout.strip() == "PASS " + route + " " + mode,
                                        "stderr_empty": not result.stderr})
        report["rc"] = int(not all(row["rc"] == 0 and row["pass_line"] and row["stderr_empty"]
                                   for row in report["cases"]))
    (args.out / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    return report["rc"]


if __name__ == "__main__":
    raise SystemExit(main())

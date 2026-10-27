"""S3 (#678): Moonlight's page, run as the source writes it -- PL-03 (#1238), PL-04 (#1239),
PL-05 (#1240), PL-06 (#1241), PL-15 (#1249), PL-16 (#1250).

    python3 -I s03-moonlight.py <es tree> [<GuiMoonlight.cpp>]

The whole of es-app/src/guis/GuiMoonlight.cpp is compiled -- not an excerpt,
so the pin's file and a rewritten one are tested alike -- against stand-in
headers for what it includes (written below: the page base, the window, the
message box, SystemConf, ApiSystem's executeScriptLegacy as `popen` reads
lines, Utils::Platform::runSystemCommand as `system`, HttpReq answering from
/w/http), and the tree's own StringUtil.cpp and AtomicFileUtil.cpp. Each
scenario is one run of the binary inside bubblewrap (--clearenv): the page's
paths under /storage are a fresh directory, PATH holds stub `moonlight` and
`controller-layout` that record their arguments, umask 022, and a watchdog of
5 s. Hostile values are assembled at run time from parts; no injection string
is at rest in this file (D-WORKFLOW-211).

Scenarios and what each expects (the fix's behaviour; the pin FAILs them):
  quit / pair       the SERVER IP is one argument; no canary
  launcher          UPDATE over a crafted title: the generated script runs the
                    title as one argument; no canary
  update-empty /    a failed or unparsable fetch leaves the seeded library
  update-malformed  (launcher, image, gamelist.xml) as it was
  update-keeps      a successful UPDATE over a library holding a dot file and a folder of the
                    player's: the old launchers replaced, those two kept, nothing left aside
                    (the control: the pin's `rm *` kept them too)
  update-readonly   /storage/roms read-only: no restart, the library as it was
  update-pinned     the library a mount point (its rename refused): no restart, the library as it was
  unpair            the two directories removed and the box true
  unpair-fail       a removal that cannot happen: not the success box
  conf-empty        an empty Moonlight.conf in the pairing callback: returns (no hang)
  conf-malformed    a certificate with no escaped line end: no throw
  embedded          `moonlight -v` printing Embedded: isEmbedded() true; no descriptor left after two calls
  key-mode          the extracted key 0600 under umask 022; an existing 0644 key narrowed at the page's open;
                    a new pairing's key replaces an old one, 0600
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ES = Path(sys.argv[1])
SRC = Path(sys.argv[2]) if len(sys.argv) > 2 else ES / "es-app/src/guis/GuiMoonlight.cpp"   # the page, or another copy of it

FAKES = {
"guis/GuiMoonlight.h": r'''
#pragma once
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <vector>
#define _(x) std::string(x)
#define _U(x) std::string(x)
struct Window;
struct GuiComponent { Window* mWindow = nullptr; virtual ~GuiComponent() {} };
struct Font {};
struct ThemeTextT { std::shared_ptr<Font> font = std::make_shared<Font>(); unsigned int color = 0; };
struct Theme { ThemeTextT Text; };
struct ThemeData { static std::shared_ptr<Theme> getMenuTheme() { static auto t = std::make_shared<Theme>(); return t; } };
struct TextComponent : GuiComponent { std::string text; TextComponent(Window*, const std::string& t, std::shared_ptr<Font>, unsigned int) : text(t) {} };
struct Entry { std::string label; std::function<void()> func; };
extern std::vector<Entry> gEntries;
struct GuiSettings : GuiComponent {
    GuiSettings(Window* w, const std::string&) { mWindow = w; }
    void addGroup(const std::string&) {}
    void addEntry(const std::string& l, bool, const std::function<void()>& f) { gEntries.push_back({l, f}); }
    void addInputTextConfigRow(const std::string&, const std::string&, bool, bool = false) {}
    void addWithLabel(const std::string&, std::shared_ptr<GuiComponent>) {}
    void addSaveFunc(const std::function<void()>&) {}
    void close() {}
};
class GuiMoonlight : public GuiSettings
{
public:
	static void show(Window* window);
protected:
  GuiMoonlight(Window* window);
  static bool ParseServerIp(const std::string& line, std::string* server_ip);
  static std::vector<std::string> ParseAppList(const std::vector<std::string>& vec);
};
''',
"Window.h": r'''
#pragma once
#include <string>
#include <vector>
struct GuiComponent;
extern std::vector<std::string> gBoxes;
struct Window { void pushGui(GuiComponent* g); void displayNotificationMessage(const std::string& m, int = 0) { gBoxes.push_back("toast: " + m); } };
''',
"guis/GuiMsgBox.h": r'''
#pragma once
#include "Window.h"
#include <functional>
#include <string>
enum GuiMsgBoxIcon { ICON_AUTOMATIC, ICON_INFORMATION, ICON_QUESTION, ICON_WARNING, ICON_ERROR };
struct GuiMsgBox : GuiComponent { std::string text; GuiMsgBox(Window*, const std::string& t, const std::string& = "OK", const std::function<void()>& = nullptr, GuiMsgBoxIcon = ICON_AUTOMATIC) : text(t) {} };
''',
"ApiSystem.h": r'''
#pragma once
#include <cstdio>
#include <functional>
#include <string>
#include <utility>
#include <vector>
struct ApiSystem {
  static std::pair<std::string, int> executeScriptLegacy(const std::string& command, const std::function<void(const std::string)>& func = nullptr) {
    FILE* p = popen(command.c_str(), "r"); if (!p) return {"", -1};
    char buff[1024]; while (fgets(buff, sizeof buff, p)) { std::string l(buff); while (!l.empty() && (l.back() == '\n' || l.back() == '\r')) l.pop_back(); if (func) func(l); }
    int rc = pclose(p); return {"", WIFEXITED(rc) ? WEXITSTATUS(rc) : -1};
  }
};
#include <sys/wait.h>
''',
"Scripting.h": r'''
#pragma once
#include <string>
namespace Scripting { inline void fireEvent(const std::string&, const std::string& = "") {} }
''',
"utils/Platform.h": r'''
#pragma once
#include <cstdlib>
#include <string>
extern bool gQuit;
namespace Utils { namespace Platform {
  enum QuitMode { QUIT = 0 };
  inline int runSystemCommand(const std::string& cmd, const std::string&, void*) { int r = std::system(cmd.c_str()); return WIFEXITED(r) ? WEXITSTATUS(r) : -1; }
  inline int quitES(QuitMode) { gQuit = true; return 0; }
} }
#include <sys/wait.h>
''',
"Log.h": r'''
#pragma once
#include <sstream>
enum LogLevel { LogError, LogWarning, LogInfo, LogDebug };
struct LogLine { std::ostringstream o; template <class T> LogLine& operator<<(const T& v) { o << v; return *this; } };
#define LOG(level) LogLine()
''',
"SystemConf.h": r'''
#pragma once
#include <map>
#include <string>
struct SystemConf { std::map<std::string, std::string> v; static SystemConf* getInstance() { static SystemConf c; return &c; }
  std::string get(const std::string& k) { return v.count(k) ? v[k] : ""; } bool set(const std::string& k, const std::string& x) { v[k] = x; return true; } };
''',
"HttpReq.h": r'''
#pragma once
#include <fstream>
#include <sstream>
#include <string>
struct HttpReqOptions { std::string clientCert, clientKey, outputFilename; };
struct HttpReq {
  enum Status { REQ_IN_PROGRESS, REQ_SUCCESS, REQ_IO_ERROR };
  std::string body; bool ok = false;
  HttpReq(const std::string& url, HttpReqOptions* o) {
    std::string name = url.find("applist") != std::string::npos ? "/w/http/applist" : "/w/http/asset";
    std::ifstream f(name); if (!f) return; std::stringstream s; s << f.rdbuf(); body = s.str(); ok = true;
    if (o && !o->outputFilename.empty()) { std::ofstream out(o->outputFilename); out << body; ok = (bool)out; }
  }
  void wait() {} Status status() { return ok ? REQ_SUCCESS : REQ_IO_ERROR; } std::string getContent() { return body; } std::string getErrorMsg() { return "fake"; }
};
''',
}
MAIN = r'''
#include "guis/GuiMoonlight.h"
#include "Window.h"
#include "guis/GuiMsgBox.h"
#include "SystemConf.h"
#include <dirent.h>
#include <iostream>
std::vector<Entry> gEntries; std::vector<std::string> gBoxes; bool gQuit = false;
void Window::pushGui(GuiComponent* g) { if (auto* b = dynamic_cast<GuiMsgBox*>(g)) gBoxes.push_back(b->text); delete g; }
bool isEmbedded(void);
static int fds() { int n = 0; DIR* d = opendir("/proc/self/fd"); while (d && readdir(d)) n++; if (d) closedir(d); return n; }
int main(int argc, char** argv)
{
  std::string what = argv[1];
  if (what == "embedded") { int a = fds(); bool e1 = isEmbedded(); bool e2 = isEmbedded(); int b = fds();
    std::cout << "embedded " << e1 << e2 << " fds+" << (b - a) << "\n"; return 0; }
  if (argc > 2) SystemConf::getInstance()->set("moonlight.host", argv[2]);
  Window w; GuiMoonlight::show(&w);
  if (what == "open") { std::cout << "opened\n"; return 0; }
  for (auto& e : gEntries) if (e.label == what) { e.func(); for (auto& b : gBoxes) std::cout << "box: " << b << "\n"; std::cout << "quit " << gQuit << "\n"; return 0; }
  std::cout << "no entry " << what << "\n"; return 3;
}
'''

base = Path("/workspace/tmp/m6-t31/tmp")
fail = []
cases = 0
with tempfile.TemporaryDirectory(prefix="s03-", dir=base) as d:
    d = Path(d)
    for name, text in FAKES.items():
        (d / "fakes" / name).parent.mkdir(parents=True, exist_ok=True)
        (d / "fakes" / name).write_text(text)
    (d / "main.cpp").write_text(MAIN)
    pugi = os.environ.get("PUGIXML_INCLUDE_DIR", "")
    pugi_src = Path(pugi) / "pugixml/src"
    b = subprocess.run(["g++", "-std=c++17", "-O0", "-g", "-fsanitize=address,undefined", "-I", str(d / "fakes"),
                        "-I", str(ES / "es-core/src"), "-I", str(pugi_src), str(SRC), str(d / "main.cpp"),
                        str(ES / "es-core/src/utils/StringUtil.cpp"), str(ES / "es-core/src/utils/AtomicFileUtil.cpp"),
                        str(pugi_src / "pugixml.cpp"), "-o", str(d / "page"), "-pthread"], capture_output=True, text=True)
    if b.returncode:
        print("FAIL s03: the page does not compile against the stand-ins\n" + b.stderr[-3000:]); sys.exit(2)
    bins = d / "bin"; bins.mkdir()
    (bins / "moonlight").write_text('#!/bin/sh\nfor a in "$@"; do printf "[%s]" "$a"; done >> /w/argv; echo >> /w/argv\n'
                                     'case "$1" in -v) [ -f /w/embedded ] && echo "Moonlight Embedded 2.6";; pair) echo "Connect to 192.0.2.7..."; echo "Succesfully paired";; esac\n')
    (bins / "controller-layout").write_text("#!/bin/sh\nexit 0\n")
    for f in bins.iterdir():
        f.chmod(0o755)
    canary = "".join(["/w/", "can", "ary"])
    hostile_ip = "".join(["192.0.2.7", ";", "touch", " ", canary])
    hostile_title = "".join(["Game ", "$", "(", "touch ", canary, ")"])
    applist = ('<?xml version="1.0"?><root><App><AppTitle>%s</AppTitle><ID>1</ID></App>'
               '<App><AppTitle>Plain</AppTitle><ID>2</ID></App></root>')
    conf_dir = "/storage/.config/Moonlight Game Streaming Project"
    cache_dir = "/storage/.cache/Moonlight Game Streaming Project"

    def scenario(name, entry, host=None, prep=None, ro=(), rw=()):
        root = d / ("run-" + name)
        if root.exists():
            shutil.rmtree(root)
        (root / "storage/roms/moonlight/images").mkdir(parents=True)
        (root / "w/http").mkdir(parents=True)
        if prep:
            prep(root)
        argv = ["bwrap", "--clearenv", "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
                "--symlink", "usr/lib64", "/lib64", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
                "--bind", str(root / "storage"), "/storage", "--bind", str(root / "w"), "/w", "--ro-bind", str(bins), "/opt/bin",
                "--ro-bind", str(d / "page"), "/opt/page"]
        for p in ro:
            argv += ["--ro-bind", str(root / p.lstrip("/")), p]
        for p in rw:
            argv += ["--bind", str(root / p.lstrip("/")), p]
        argv += ["--setenv", "PATH", "/opt/bin:/usr/bin", "--setenv", "HOME", "/storage",
                 "--setenv", "ASAN_OPTIONS", "detect_leaks=0", "/bin/sh", "-c", 'umask 022; exec /opt/page "$@"', "page", entry]
        if host is not None:
            argv.append(host)
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=5)
            out, rc = r.stdout + r.stderr[-600:], r.returncode
        except subprocess.TimeoutExpired:
            out, rc = "TIMEOUT after 5 s", 124
        return root, out, rc

    def seed_library(root):
        m = root / "storage/roms/moonlight"
        (m / "Old.sh").write_text("#!/bin/sh\n"); (m / "gamelist.xml").write_text("<gameList><game/></gameList>\n")
        (m / "images/Old.png").write_text("png")

    def library_as_was(root):
        m = root / "storage/roms/moonlight"
        return (m / "Old.sh").exists() and (m / "gamelist.xml").read_text().startswith("<gameList><game/>") and (m / "images/Old.png").exists()

    def check(cond, what):
        global cases
        cases += 1
        print(("ok   " if cond else "FAIL ") + what)
        if not cond:
            fail.append(what)

    # PL-03: the immediate commands
    for entry, label in (("QUIT CURRENT GAME", "quit"), ("PAIR WITH SERVER", "pair")):
        root, out, rc = scenario(label, entry, hostile_ip)
        made = (root / "w/canary").exists()
        argv_seen = (root / "w/argv").read_text().strip() if (root / "w/argv").exists() else ""
        check(not made and ("[" + hostile_ip + "]") in argv_seen,
              "%s: the SERVER IP is one argument and runs nothing (canary %s; argv %s)" % (label, "MADE" if made else "absent", argv_seen[:90]))
    # PL-03: the generated launchers
    def prep_launch(root):
        (root / "w/http/applist").write_text(applist % hostile_title); (root / "w/http/asset").write_text("png")
        (root / "storage/.config/Moonlight Game Streaming Project").mkdir(parents=True)
        (root / "storage/.config/Moonlight Game Streaming Project/Moonlight.conf").write_text("")
    root, out, rc = scenario("launcher", "UPDATE MOONLIGHT GAMES", "192.0.2.7", prep_launch)
    scripts = sorted((root / "storage/roms/moonlight").glob("*.sh"))
    ran = []
    for sc in scripts:
        rel = "/storage/roms/moonlight/" + sc.name
        subprocess.run(["bwrap", "--clearenv", "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
                        "--symlink", "usr/lib64", "/lib64", "--proc", "/proc", "--dev", "/dev", "--bind", str(root / "storage"), "/storage",
                        "--bind", str(root / "w"), "/w", "--ro-bind", str(bins), "/opt/bin", "--setenv", "PATH", "/opt/bin:/usr/bin",
                        "/bin/sh", rel], capture_output=True, text=True, timeout=5)
        ran.append(sc.name)
    made = (root / "w/canary").exists()
    argv_seen = (root / "w/argv").read_text() if (root / "w/argv").exists() else ""
    check(len(scripts) == 2 and not made and ("[" + hostile_title + "]") in argv_seen,
          "launcher: %d script(s) generated, run: the title one argument and nothing run (canary %s)" % (len(scripts), "MADE" if made else "absent"))
    # PL-04
    def prep_empty(root): seed_library(root)
    def prep_malformed(root): seed_library(root); (root / "w/http/applist").write_text("<<not xml")
    def prep_update(root):
        seed_library(root); (root / "w/http/applist").write_text(applist % "Plain2"); (root / "w/http/asset").write_text("png")
    root, out, rc = scenario("update-empty", "UPDATE MOONLIGHT GAMES", "192.0.2.7", prep_empty)
    check(library_as_was(root) and "quit 0" in out, "update-empty: a failed fetch leaves the library as it was (%s)" % ("kept" if library_as_was(root) else "removed"))
    root, out, rc = scenario("update-malformed", "UPDATE MOONLIGHT GAMES", "192.0.2.7", prep_malformed)
    check(library_as_was(root) and "quit 0" in out, "update-malformed: an unparsable list leaves the library as it was (%s)" % ("kept" if library_as_was(root) else "removed"))
    def prep_keeps(root):
        prep_update(root); m = root / "storage/roms/moonlight"
        (m / ".keep").write_text("k"); (m / "mine").mkdir(); (m / "mine/note.txt").write_text("n")
    root, out, rc = scenario("update-keeps", "UPDATE MOONLIGHT GAMES", "192.0.2.7", prep_keeps)
    m = root / "storage/roms/moonlight"
    left = sorted(x.name for x in (root / "storage/roms").iterdir())
    ok = ("quit 1" in out and not (m / "Old.sh").exists() and (m / "Plain2.sh").exists() and (m / ".keep").exists()
          and (m / "mine/note.txt").exists() and left == ["moonlight"])
    check(ok, "update-keeps: restart %s, Old.sh %s, .keep %s, mine/ %s, /storage/roms holds %s" % (
          "yes" if "quit 1" in out else "no", "gone" if not (m / "Old.sh").exists() else "left", "kept" if (m / ".keep").exists() else "lost",
          "kept" if (m / "mine/note.txt").exists() else "lost", left))
    for label, kw in (("update-readonly", {"ro": ("/storage/roms",)}), ("update-pinned", {"rw": ("/storage/roms/moonlight",)})):
        root, out, rc = scenario(label, "UPDATE MOONLIGHT GAMES", "192.0.2.7", prep_update, **kw)
        boxes = [l for l in out.splitlines() if l.startswith("box:")]
        check("quit 0" in out and library_as_was(root),
              "%s: %s, the library %s; %s" % (label, "no restart" if "quit 0" in out else "the page restarts ES",
                                             "as it was" if library_as_was(root) else "changed", boxes))
    # PL-05
    def prep_pairing(root):
        for p in (conf_dir, cache_dir):
            (root / p.lstrip("/")).mkdir(parents=True); (root / p.lstrip("/") / "marker").write_text("x")
        (root / conf_dir.lstrip("/") / "Moonlight.conf").write_text("")
    root, out, rc = scenario("unpair", "UNPAIR WITH SERVER", None, prep_pairing)
    gone = not (root / conf_dir.lstrip("/")).exists() and not (root / cache_dir.lstrip("/")).exists()
    check(gone and "box: Unpaired and settings cleared" in out, "unpair: the directories %s; %s" % ("removed" if gone else "left", [l for l in out.splitlines() if l.startswith("box:")]))
    root, out, rc = scenario("unpair-fail", "UNPAIR WITH SERVER", None, prep_pairing, ro=("/storage/.cache",))
    check("box: Unpaired and settings cleared" not in out and "box:" in out, "unpair-fail: a removal that cannot happen says %s" % [l for l in out.splitlines() if l.startswith("box:")])
    # PL-06
    def prep_conf(text):
        def p(root):
            (root / conf_dir.lstrip("/")).mkdir(parents=True); (root / cache_dir.lstrip("/")).mkdir(parents=True)
            (root / conf_dir.lstrip("/") / "Moonlight.conf").write_text(text)
        return p
    root, out, rc = scenario("conf-empty", "PAIR WITH SERVER", "192.0.2.7", prep_conf(""))
    check(rc != 124, "conf-empty: the pairing callback over an empty conf %s" % ("returned" if rc != 124 else "hung (the watchdog)"))
    cert = "".join(["certificate=", "@ByteArray(", "-----BEGIN CERT-----", "ABC", ")"])
    root, out, rc = scenario("conf-malformed", "PAIR WITH SERVER", "192.0.2.7", prep_conf(cert + "\n"))
    check(rc == 0 and "terminate" not in out and "out_of_range" not in out, "conf-malformed: a certificate with no escaped line end %s" % ("handled" if rc == 0 else "rc %d (%s)" % (rc, out.strip().splitlines()[-1][:80] if out.strip() else "")))
    # PL-15
    root, out, rc = scenario("embedded", "embedded", None, lambda r: (r / "w/embedded").write_text("1"))
    line = next((l for l in out.splitlines() if l.startswith("embedded ")), out[:80])
    check(line.startswith("embedded 11") and line.endswith("fds+0"), "embedded: %s (expected both true, no descriptor left)" % line)
    # PL-16
    key_text = "".join(["key", "=", "@ByteArray(", "-----BEGIN PRIVATE", " KEY-----\\n", "QUJD", "\\n-----END PRIVATE", " KEY-----\\n", ")"])
    cert_text = "".join(["certificate", "=", "@ByteArray(", "-----BEGIN CERT-----\\n", "QUJD", "\\n-----END CERT-----\\n", ")"])
    root, out, rc = scenario("key-mode", "PAIR WITH SERVER", "192.0.2.7", prep_conf(cert_text + "\n" + key_text + "\n"))
    kp = root / cache_dir.lstrip("/") / "key.pem"
    mode = oct(kp.stat().st_mode & 0o777) if kp.exists() else "absent"
    check(mode == "0o600", "key-mode: the extracted key is %s under umask 022" % mode)
    def prep_open_key(root):
        prep_conf(cert_text + "\n" + key_text + "\n")(root)
        k = root / cache_dir.lstrip("/") / "key.pem"; k.write_text("old"); k.chmod(0o644)
    root, out, rc = scenario("key-narrow", "open", None, prep_open_key)
    mode = oct(kp.stat().st_mode & 0o777) if (kp := root / cache_dir.lstrip("/") / "key.pem").exists() else "absent"
    check(mode == "0o600", "key-narrow: an existing 0644 key at the page's open is %s" % mode)
    root, out, rc = scenario("key-replace", "PAIR WITH SERVER", "192.0.2.7", prep_open_key)
    kp = root / cache_dir.lstrip("/") / "key.pem"
    mode = oct(kp.stat().st_mode & 0o777) if kp.exists() else "absent"
    fresh = kp.exists() and kp.read_text() != "old"
    check(mode == "0o600" and fresh, "key-replace: after a new pairing the key is %s, %s" % (mode, "replaced" if fresh else "the old one"))
if fail:
    print("FAIL s03: %d of %d cases" % (len(fail), cases)); sys.exit(1)
print("s03: PASS, %d cases" % cases)

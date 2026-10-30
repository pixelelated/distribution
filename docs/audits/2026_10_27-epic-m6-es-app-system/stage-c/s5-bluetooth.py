"""S5 (#680; #1290 EP-47): a Bluetooth scan, and a disk format, that end before start() has published them.

    python3 -I s5-bluetooth.py <es-app/src>

ThreadedBluetooth.cpp and the two classes in ThreadedBluetooth.h, extracted
as written, under ASan/UBSan. Doubled: the window, its notification card and
GuiMsgBox (which records the refusal), ApiSystem's scanNewBluetooth and
formatDisk (each returns at once, as a scan with no adapter does), _ and _U.
std::thread is the harness's T33Thread: a real thread, detached, whose
constructor lets the worker run for 50 ms before it returns -- the schedule in
which the worker ends before its starter has stored anything, made certain
rather than left to chance. At the pin the worker deletes the object and
clears mInstance (:46-47) while the constructor is still storing its handle
(:19) and before :58 publishes it: a write into the freed object, and
mInstance left naming it, so the second start() refuses (:52) though no scan
runs. Asserted: no sanitizer report, two scans run, nothing refused; the
formatter (:76, :110-111, :122) the same. Leak checking is off: upstream's
std::thread handle is never deleted (L-10's habit, recorded).
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import run  # noqa: E402

src = Path(sys.argv[1])
cpp = (src / "ThreadedBluetooth.cpp").read_text()
hdr = (src / "ThreadedBluetooth.h").read_text()
cpp = re.sub(r'^#include .*$', '', cpp, flags=re.M)
hdr = re.sub(r'^#(include|pragma) .*$', '', hdr, flags=re.M)
cpp = cpp.replace("std::thread", "T33Thread")
hdr = hdr.replace("std::thread", "T33Thread")

harness = r'''
#include <atomic>
#include <chrono>
#include <cstdio>
#include <functional>
#include <mutex>
#include <string>
#include <thread>
extern "C" const char* __asan_default_options() { return "detect_leaks=0"; }
static std::string _(const char* s) { return s; }
static std::string _U(const char* s) { return s; }
static std::atomic<int> gScans(0), gFormats(0), gRefused(0);
struct AsyncNotificationComponent {
	void updateTitle(const std::string&) {} void updateText(const std::string&) {} void updatePercent(int) {} void close() {} };
struct GuiComponent { virtual ~GuiComponent() {} };
struct Window {
	AsyncNotificationComponent* createAsyncNotificationComponent() { return new AsyncNotificationComponent(); }
	void pushGui(GuiComponent* g) { gRefused++; delete g; }
	void displayNotificationMessage(const std::string&) {} };
struct GuiMsgBox : GuiComponent { GuiMsgBox(Window*, const std::string&) {} };
struct ApiSystem {
	static ApiSystem* getInstance() { static ApiSystem a; return &a; }
	void scanNewBluetooth(const std::function<void(const std::string)>& f) { gScans++; f("x"); }
	int formatDisk(const std::string&, const std::string&, const std::function<void(const std::string)>& f) { gFormats++; f("x"); return 0; } };
// A real thread whose starter waits 50 ms before going on: the worker ends first.
struct T33Thread {
	std::thread t;
	template <class F, class A> T33Thread(F f, A a) : t(f, a) { t.detach(); std::this_thread::sleep_for(std::chrono::milliseconds(50)); } };
''' + hdr + cpp + r'''
int main()
{
	setvbuf(stdout, nullptr, _IONBF, 0);
	Window w;
	ThreadedBluetooth::start(&w);
	std::this_thread::sleep_for(std::chrono::milliseconds(200));
	ThreadedBluetooth::start(&w);
	std::this_thread::sleep_for(std::chrono::milliseconds(200));
	printf("bluetooth: two start()s a scan apart: %d scan(s) ran, %d refused as already running; running now: %s\n", gScans.load(), gRefused.load(), ThreadedBluetooth::isRunning() ? "yes" : "no");
	int refusedBefore = gRefused.load();
	ThreadedFormatter::start(&w, "/dev/x", "ext4");
	std::this_thread::sleep_for(std::chrono::milliseconds(200));
	ThreadedFormatter::start(&w, "/dev/x", "ext4");
	std::this_thread::sleep_for(std::chrono::milliseconds(200));
	printf("formatter: two start()s a format apart: %d format(s) ran, %d refused; running now: %s\n", gFormats.load(), gRefused.load() - refusedBefore, ThreadedFormatter::isRunning() ? "yes" : "no");
	bool ok = gScans == 2 && gFormats == 2 && gRefused == 0 && !ThreadedBluetooth::isRunning() && !ThreadedFormatter::isRunning();
	if (!ok)
		printf("FAIL EP-47: a scan or a format that ended before start() published it is still named as running\n");
	return ok ? 0 : 1;
}
'''
run(harness, "s5-bt")

// T35 (#682) 3.17: unregisterPostedFunctions (Window.cpp:1262-1274) against postToUiThread
// (:1276-1290), both lifted verbatim by tools/t35-extract.py, on two threads under
// -fsanitize=thread. The erase loop takes no lock; the post takes mNotificationMessagesLock.
// A data race report is the FAIL at the pin.
// Stage E S2 (PL-26, #1355) extends it with the interface thread: the drain
// (processPostedFunctions, :1292-1307), update's idle count (:540) and isSleeping
// (Window.h:69) against the post's wake. The members are Window.h's own lines
// (Window.h:174-175 at the pin), so the double's types follow the tree. The
// power saver reads as off, so every post takes the wake branch the pin writes in.
#include <atomic>
#include <functional>
#include <mutex>
#include <thread>
#include <vector>
namespace PowerSaver { static bool getState() { return false; } static void pushRefreshEvent() {} }
#define TRYCATCH(name, f) f;
static std::mutex mNotificationMessagesLock;
struct Window
{
	struct PostedFunction { std::function<void()> func; void* container; };
	std::vector<PostedFunction> mFunctions;
#include "x_win_idle.inc"
#include "x_win_issleeping.inc"
	void unregisterPostedFunctions(void* data);
	void postToUiThread(const std::function<void()>& func, void* data);
	void processPostedFunctions();
	void tick(int deltaTime) {
#include "x_upd_idle.inc"
	}
};
#include "x_posts_unreg.inc"
#include "x_posts_post.inc"
#include "x_posts_drain.inc"
int main()
{
	// Phase 1 (PL-26): a worker posts while the interface thread drains, counts idle
	// time and reads isSleeping -- no unregister, so the vector stays whole and a
	// report here is the wake's. Phase 2 (3.17, PL-07): the post against the
	// unregister, as stage C wrote it; at the pin it can corrupt the vector, which
	// is why it runs second.
	Window w;
	w.mSleeping = false;
	w.mTimeSinceLastInput = 0;
	int a, b;
	{
		std::atomic<bool> done{ false };
		std::thread poster([&] { for (int i = 0; i < 20000; i++) w.postToUiThread([] {}, (void*)&b); done = true; });
		std::thread ui([&] { int sleeping = 0; while (!done) { w.processPostedFunctions(); w.tick(16); sleeping += w.isSleeping(); } (void)sleeping; });
		poster.join(); ui.join();
	}
	w.processPostedFunctions();
	std::thread poster([&] { for (int i = 0; i < 20000; i++) w.postToUiThread([] {}, (i & 1) ? (void*)&a : (void*)&b); });
	std::thread page([&] { for (int i = 0; i < 20000; i++) w.unregisterPostedFunctions(&a); });
	poster.join(); page.join();
	return 0;
}

// T35 (#682) 3.17: unregisterPostedFunctions (Window.cpp:1262-1274) against postToUiThread
// (:1276-1290), both lifted verbatim by tools/t35-extract.py, on two threads under
// -fsanitize=thread. The erase loop takes no lock; the post takes mNotificationMessagesLock.
// A data race report is the FAIL at the pin.
#include <functional>
#include <mutex>
#include <thread>
#include <vector>
namespace PowerSaver { static bool getState() { return true; } static void pushRefreshEvent() {} }
static std::mutex mNotificationMessagesLock;
struct Window
{
	struct PostedFunction { std::function<void()> func; void* container; };
	std::vector<PostedFunction> mFunctions;
	bool mSleeping = false;
	int mTimeSinceLastInput = 0;
	void unregisterPostedFunctions(void* data);
	void postToUiThread(const std::function<void()>& func, void* data);
};
#include "x_posts_unreg.inc"
#include "x_posts_post.inc"
int main()
{
	Window w;
	int a, b;
	std::thread poster([&] { for (int i = 0; i < 20000; i++) w.postToUiThread([] {}, (i & 1) ? (void*)&a : (void*)&b); });
	std::thread page([&] { for (int i = 0; i < 20000; i++) w.unregisterPostedFunctions(&a); });
	poster.join(); page.join();
	return 0;
}

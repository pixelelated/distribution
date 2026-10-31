// T35 (#682) stage E S9: PowerSaver's push flag (PowerSaver.cpp:15-36 and PowerSaver.h:68-69,
// lifted verbatim as ps_push and ps_members) under -fsanitize=thread. A worker's post calls
// pushRefreshEvent (Window.cpp's postToUiThread), which reads and writes the static
// mHasPushedEvent, while the interface thread calls resetRefreshEvent (es-app/src/main.cpp:1194),
// which writes it, with no lock between them. A data race report is the FAIL at the pin. The
// members are the header's own lines, so the double's types follow the tree.
#include <atomic>
#include <thread>
union SDL_Event { unsigned int type; };
static unsigned int SDL_RegisterEvents(int) { return 0x8000; }
static int SDL_PushEvent(SDL_Event*) { return 1; }
struct PowerSaver
{
	static void pushRefreshEvent();
	static void resetRefreshEvent();
#include "x_ps_members.inc"
	static bool mState;
	static int mPauseCounter;
};
bool PowerSaver::mState = true;
#include "x_ps_push.inc"
int main()
{
	PowerSaver::pushRefreshEvent();   // the first push registers the event type on this thread
	std::thread worker([] { for (int i = 0; i < 20000; i++) PowerSaver::pushRefreshEvent(); });
	std::thread ui([] { for (int i = 0; i < 20000; i++) PowerSaver::resetRefreshEvent(); });
	worker.join(); ui.join();
	return 0;
}

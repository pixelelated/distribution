// T35 (#682) 3.3: WatchersManager's mRunning and mPaused (watchers/WatchersManager.cpp:151,
// :161, :187; .h:85-86) under -fsanitize=thread, with the pin's WatchersManager.cpp linked
// behind tests/app-unit/fakes/Log.h. The destructor writes mRunning without a lock while
// run() reads it; pause() writes mPaused under mThreadLock while run() reads it there.
// A data race report is the FAIL at the pin.
#include <atomic>
#include <chrono>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
#include "watchers/WatchersManager.h"
namespace FakeLog
{
	std::vector<std::string>& lines() { static std::vector<std::string> l; return l; }
	std::mutex& lock() { static std::mutex m; return m; }
}
struct Fast : IWatcher
{
	bool enabled() override { return true; }
	int updateTime() override { return 1; }
	int initialUpdateTime() override { return 0; }
	bool check() override { std::this_thread::sleep_for(std::chrono::milliseconds(2)); return false; }
};
int main()
{
	static Fast w;
	WatchersManager::getInstance();
	WatchersManager::RegisterComponent(&w);
	std::this_thread::sleep_for(std::chrono::milliseconds(1200));
	WatchersManager::pause();
	WatchersManager::resume();
	std::this_thread::sleep_for(std::chrono::milliseconds(1200));
	WatchersManager::UnregisterComponent(&w);
	WatchersManager::stop();
	return 0;
}

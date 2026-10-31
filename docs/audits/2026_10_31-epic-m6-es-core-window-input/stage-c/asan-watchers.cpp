// T35 (#682) 3.2: unregister a watcher while its probe runs (watchers/WatchersManager.cpp:76-90
// against :181-199), the pin's WatchersManager.cpp under -fsanitize=address behind
// tests/app-unit/fakes/Log.h. At the pin the list lock spans the probe, so the unregister waits
// and the WatcherInfo is freed only between iterations: no report is expected at the pin. The
// case is the guard PL-01's fix (a probe outside the lock) must keep passing (EP-13: re-validate).
#include <atomic>
#include <chrono>
#include <cstdio>
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
struct Slow : IWatcher
{
	std::atomic<bool> started{ false };
	bool enabled() override { return true; }
	int updateTime() override { return 1; }
	int initialUpdateTime() override { return 0; }
	bool check() override { started = true; std::this_thread::sleep_for(std::chrono::milliseconds(400)); return true; }
};
struct Obs : IWatcherNotify { std::atomic<int> n{ 0 }; void OnWatcherChanged(IWatcher*) override { n++; } };
int main()
{
	auto* w = new Slow();
	static Obs o;
	WatchersManager::getInstance();
	WatchersManager::RegisterNotify(&o);
	WatchersManager::RegisterComponent(w);
	for (int i = 0; i < 400 && !w->started; i++) std::this_thread::sleep_for(std::chrono::milliseconds(10));
	WatchersManager::UnregisterComponent(w);   // during the probe
	delete w;                                  // the caller frees its watcher once unregistered
	std::this_thread::sleep_for(std::chrono::milliseconds(1500));
	WatchersManager::UnregisterNotify(&o);
	WatchersManager::stop();
	std::printf("asan-watchers: done, %d notification(s)\n", o.n.load());
	return 0;
}

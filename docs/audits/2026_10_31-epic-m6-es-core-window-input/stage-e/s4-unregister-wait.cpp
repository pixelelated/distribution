// T35 (#682) stage E S4 (ruling 13): the wait that remains after PL-01's fix, measured.
// Watcher A's probe takes 1500 ms; B is registered and not due. While A probes, B's
// UnregisterComponent is timed (every other watcher's call returns at once), then A's
// (its own probe's remainder: the one wait left, bounded by that probe). Built twice,
// against WatchersManager.cpp/.h read by git show at S3's tip and at S4's, behind
// tests/app-unit/fakes/Log.h; not part of t35-build-tests.sh.
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
	int updateTime() override { return 60000; }
	int initialUpdateTime() override { return 0; }
	bool check() override { started = true; std::this_thread::sleep_for(std::chrono::milliseconds(1500)); return false; }
};
struct Idle : IWatcher
{
	bool enabled() override { return true; }
	int updateTime() override { return 60000; }
	int initialUpdateTime() override { return 60000; }
	bool check() override { return false; }
};
static long ms(std::chrono::steady_clock::time_point t0) { return (long)std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - t0).count(); }
int main()
{
	static Slow a;
	static Idle b;
	WatchersManager::getInstance();
	WatchersManager::RegisterComponent(&a);
	WatchersManager::RegisterComponent(&b);
	for (int i = 0; i < 400 && !a.started; i++) std::this_thread::sleep_for(std::chrono::milliseconds(10));
	auto t0 = std::chrono::steady_clock::now();
	WatchersManager::UnregisterComponent(&b);
	long other = ms(t0);
	auto t1 = std::chrono::steady_clock::now();
	WatchersManager::UnregisterComponent(&a);
	long own = ms(t1);
	std::printf("s4-unregister-wait: another watcher's unregister %ld ms; the probing watcher's own unregister %ld ms (its probe takes 1500 ms)\n", other, own);
	WatchersManager::stop();
	return 0;
}

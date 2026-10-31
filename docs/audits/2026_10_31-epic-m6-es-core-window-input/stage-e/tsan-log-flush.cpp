// T35 (#682) stage E S7, PL-28 (ruling 10): AsyncLogger (Log.cpp:29-196, lifted verbatim as
// log_async) under -fsanitize=thread: emergencyFlush -- the crash handler's call -- flushes
// mFile on its own thread (:98) while the worker writes and flushes the same stream (:133,
// :147). Ruling 10: the handler's own flush goes only if this program reports the race on
// mFile at the pin; if it cannot, the handler's limits are written beside it instead. The
// stream's code is libstdc++'s, compiled outside this program, so ThreadSanitizer sees only
// the accesses this translation unit makes.
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <fstream>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
#include <unistd.h>
#include "LogPolicy.h"   // brings the tree's Log.h from its own directory (san puts the app-unit fakes first)
#include "x_log_async.inc"
int main()
{
	std::string p = "/workspace/tmp/m6-t35/tmp/tsan-log-flush-" + std::to_string(getpid()) + ".txt";
	AsyncLogger::instance().open(p, LogInfo, false);
	std::atomic<bool> done{ false };
	std::thread writer([&] { for (int i = 0; i < 20000; i++) AsyncLogger::instance().enqueue(LogInfo, "line " + std::to_string(i)); done = true; });
	std::thread handler([&] { while (!done) AsyncLogger::instance().emergencyFlush(); });
	writer.join(); handler.join();
	AsyncLogger::instance().close();
	unlink(p.c_str());
	return 0;
}

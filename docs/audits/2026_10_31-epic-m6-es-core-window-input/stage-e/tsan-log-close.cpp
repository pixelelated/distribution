// T35 (#682) stage E S7, PL-27 (#1343): AsyncLogger (Log.cpp:29-196, lifted verbatim as
// log_async) under -fsanitize=thread: close() writes mShutdown under mMutex while the worker
// reads it at :152 without it. A data race report is the FAIL at the pin. close() runs while
// the worker drains one 16 MiB line, so the worker's read comes after close's write with no
// lock between them (a first shape, which let the worker go idle before close, reported
// nothing at the pin: the wait's own lock then orders the two).
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
	std::string p = "/workspace/tmp/m6-t35/tmp/tsan-log-close-" + std::to_string(getpid()) + ".txt";
	for (int round = 0; round < 5; round++)
	{
		AsyncLogger::instance().open(p, LogInfo, false);
		AsyncLogger::instance().enqueue(LogInfo, std::string(16u << 20, 'x'));
		std::this_thread::sleep_for(std::chrono::milliseconds(1));
		AsyncLogger::instance().close();
	}
	unlink(p.c_str());
	return 0;
}

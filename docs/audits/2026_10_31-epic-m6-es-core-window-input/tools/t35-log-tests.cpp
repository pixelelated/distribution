// T35 (#682) stage E S7: log-tests. Log.cpp's AsyncLogger (Log.cpp:29-196) is file-local,
// so it is lifted whole by tools/t35-extract.py (log_async, refused unless its first and
// last lines hold) beside the tree's own Log.h and LogPolicy.h, and driven through its own
// open, enqueue and close: 3.23 (every batch reaches the file, #178) and PL-27 (#1343, the
// lines enqueued after the worker's last swap at close).
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include "Log.h"
#include "LogPolicy.h"
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
#include "x_log_async.inc"

static std::string logPath(const char* tag) { return std::string("/workspace/tmp/m6-t35/tmp/") + tag + "-" + std::to_string(getpid()) + ".txt"; }
static std::string slurp(const std::string& p) { std::ifstream f(p, std::ios::binary); std::stringstream ss; ss << f.rdbuf(); return ss.str(); }

TEST_CASE("3.23 every batch reaches the file before the worker sleeps (Log.cpp:117-154, #178; PASS expected)")
{
	std::string p = logPath("t323");
	AsyncLogger::instance().open(p, LogInfo, false);
	AsyncLogger::instance().enqueue(LogInfo, "a line on an idle carousel");
	bool seen = false;
	for (int i = 0; i < 200 && !seen; i++)
	{
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
		seen = slurp(p).find("a line on an idle carousel\n") != std::string::npos;
	}
	CHECK(seen);   // read before close(): the worker's own flush put it there
	AsyncLogger::instance().close();
	unlink(p.c_str());
}

TEST_CASE("S7 every line enqueued before close() is in the file afterwards, those after the worker's last swap included (Log.cpp:63-82 against :117-154; PL-27, #1343)")
{
	// One 64 MiB line keeps the worker draining (:133) after its swap (:130); the last
	// line is enqueued meanwhile, into the other buffer, and close() runs at once, so its
	// mShutdown is set before the worker reads it at :152. Five rounds, 1 to 5 ms apart.
	// (A first shape -- 200,000 short lines, then the last -- passed at the pin: the worker
	// kept pace, swapping small batches, and was asleep when the last line came.)
	int lost = 0;
	for (int round = 0; round < 5; round++)
	{
		std::string p = logPath("s7close");
		AsyncLogger::instance().open(p, LogInfo, false);
		AsyncLogger::instance().enqueue(LogInfo, std::string(64u << 20, 'x'));
		std::this_thread::sleep_for(std::chrono::milliseconds(1 + round));
		std::string last = "the last line of round " + std::to_string(round);
		AsyncLogger::instance().enqueue(LogInfo, std::string(last));
		AsyncLogger::instance().close();
		if (slurp(p).find(last + "\n") == std::string::npos)
			lost++;
		unlink(p.c_str());
	}
	MESSAGE(lost << " of 5 rounds lost their last line");
	CHECK(lost == 0);
}

// T36 S0, 3.25 (R3 s6 item 2): concurrent exists() and cache writers over FileCache's
// shared_mutex. Run under ThreadSanitizer. A clean run (no report) is the positive the
// lock discipline earns; a report would name the unsynchronized access.
#include "utils/FileSystemUtil.h"
#include "Paths.h"
#include "Settings.h"
#include "utils/TimeUtil.h"
#include "utils/ZipFile.h"
#include <thread>
#include <vector>
#include <fstream>
Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = true;
namespace Utils { namespace Zip { unsigned int ZipFile::computeCRC(unsigned int c, const void*, size_t) { return c; } } }
Utils::Time::DateTime::DateTime() {} Utils::Time::DateTime::DateTime(const time_t&) {} Utils::Time::DateTime::~DateTime() {}
int main() {
	std::string base = "/tmp/m6-t36-tsan-cache";
	std::system(("mkdir -p '" + base + "'").c_str());
	for (int i = 0; i < 8; i++) { std::ofstream((base + "/f" + std::to_string(i))) << "x"; }
	std::vector<std::thread> ts;
	for (int t = 0; t < 4; t++)
		ts.emplace_back([&, t] {
			for (int i = 0; i < 400; i++) {
				std::string p = base + "/f" + std::to_string((i + t) % 8);
				(void)Utils::FileSystem::exists(p);                 // cache read (shared lock)
				if (i % 3 == 0) Utils::FileSystem::FileSystemCache::reset(p);  // erase (unique lock)
			}
		});
	for (auto& th : ts) th.join();
	return 0;
}

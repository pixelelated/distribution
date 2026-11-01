// T36 S0, 3.6 (L-15): preloadFileSystemCache's [&] lambda reads trySaveStates on a detached
// thread after the function returned -> stack-use-after-return. Run under
// ASAN_OPTIONS=detect_stack_use_after_return=1. FileSystemUtil.cpp linked whole with doubles.
#include "utils/FileSystemUtil.h"
#include "Paths.h"
#include "Settings.h"
#include "utils/TimeUtil.h"
#include "utils/ZipFile.h"
#include <unistd.h>
Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = true;
namespace Utils { namespace Zip { unsigned int ZipFile::computeCRC(unsigned int c, const void*, size_t) { return c; } } }
Utils::Time::DateTime::DateTime() {} Utils::Time::DateTime::DateTime(const time_t&) {} Utils::Time::DateTime::~DateTime() {}
int main() {
	Utils::FileSystem::preloadFileSystemCache("/tmp/m6-t36-asan-preload-dir", true);
	usleep(300000);   // let the detached thread run after the frame returned
	return 0;
}

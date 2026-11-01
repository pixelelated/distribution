// T36 #683 S5 (#1370): the contained fix the held record describes, in
// es-core/src/utils/FileSystemUtil.cpp. The input is read at run time from the held record's
// path (argv[1]); the program only calls the function and lets AddressSanitizer judge. The
// report goes whole to the held directory; the public record carries its first line only.
#include "utils/FileSystemUtil.h"
#include "Paths.h"
#include "Settings.h"
#include "utils/TimeUtil.h"
#include "utils/ZipFile.h"
#include <fstream>
#include <sstream>
Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = false;
namespace Utils { namespace Zip { unsigned int ZipFile::computeCRC(unsigned int c, const void*, size_t) { return c; } } }
Utils::Time::DateTime::DateTime() {} Utils::Time::DateTime::DateTime(const time_t&) {} Utils::Time::DateTime::~DateTime() {}
int main(int argc, char** argv) {
	if (argc < 2) return 2;
	std::ifstream f(argv[1]); if (!f) return 2;
	std::string input; std::getline(f, input);
	volatile std::string r = Utils::FileSystem::getCanonicalPath(input);
	return 0;
}

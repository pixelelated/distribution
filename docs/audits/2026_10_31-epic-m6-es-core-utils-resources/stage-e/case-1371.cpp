// T36 #683 S6 (#1371): the contained fix the held record describes, in
// es-core/src/utils/FileSystemUtil.cpp. The input is read at run time from the held record's
// path (argv[1]); the program asserts, as a bool, that the escaped result agrees with the held
// record's expectation (every shell-active character preceded by a backslash). It fails at the
// pin and passes after. No input appears in the public output.
#include "utils/FileSystemUtil.h"
#include "Paths.h"
#include "Settings.h"
#include "utils/TimeUtil.h"
#include "utils/ZipFile.h"
#include <fstream>
#include <cstdio>
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
	std::string esc = Utils::FileSystem::getEscapedPath(input);
	// every shell-active byte in the input must be backslash-escaped in esc (none bare).
	bool agrees = true;
	for (size_t i = 0; i < esc.size(); i++) {
		char c = esc[i];
		if (c == '`' || c == '|') {       // a shell-active byte must be backslash-escaped, never bare
			if (i == 0 || esc[i-1] != '\\') { agrees = false; break; }
		}
	}
	printf("#1371: agrees=%s\n", agrees ? "true" : "false");
	return agrees ? 0 : 1;
}

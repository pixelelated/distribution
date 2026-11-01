// T36 #683 S7 (#1369): the contained fix the held record describes, in
// es-core/src/utils/ZipFile.cpp. A sibling binary: ZipFile.cpp is linked whole (so its real
// computeCRC is used -- no double, which would collide), with the usual Paths/Settings/DateTime
// doubles. The archive is read at run time from the held record's path (argv[1]); argv[2] is an
// empty scratch root the run is given. The program mirrors ApiSystem::unzipFile's loop into a
// destination under the scratch root and asserts, as a bool, that every file written lands under
// that destination -- never above it. It fails at the pin and passes after. No input or member
// name appears in the public output.
#include "utils/ZipFile.h"
#include "utils/FileSystemUtil.h"
#include "utils/StringUtil.h"
#include "utils/TimeUtil.h"
#include "Paths.h"
#include "Settings.h"
#include "Log.h"
#include <cstdio>
#include <string>
#include <sstream>
#include <filesystem>

Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = false;
Utils::Time::DateTime::DateTime() {} Utils::Time::DateTime::DateTime(const time_t&) {} Utils::Time::DateTime::~DateTime() {}
// Log doubles: mEnabled is false, so the LOG macro's body is never evaluated at run time;
// these resolve the symbols the compiled ZipFile.o still references.
LogLevel Log::mReportingLevel = LogError; bool Log::mEnabled = false;
Log::Log(LogLevel level) : mLevel(level) {} Log::~Log() {}
std::ostringstream& Log::stream() { static std::ostringstream s; return s; }

namespace fs = std::filesystem;

int main(int argc, char** argv)
{
	if (argc < 3) return 2;
	std::string zip = argv[1];
	std::string root = argv[2];
	std::string dest = root + "/dest";
	Utils::FileSystem::createDirectory(dest);

	Utils::Zip::ZipFile file;
	if (!file.load(zip)) return 2;
	// ApiSystem::unzipFile's loop: a name ending in '/' is a directory, every other is extracted.
	for (auto name : file.namelist())
	{
		if (Utils::String::endsWith(name, "/"))
		{
			Utils::FileSystem::createDirectory(Utils::FileSystem::combine(dest, name.substr(0, name.length() - 1)));
			continue;
		}
		file.extract(name, dest);
	}

	// every regular file under the scratch root must sit under dest; one above it is an escape.
	std::string destc;
	try { destc = fs::canonical(dest).string(); } catch (...) { return 2; }
	bool confined = true;
	std::error_code ec;
	for (fs::recursive_directory_iterator it(root, ec), end; it != end; it.increment(ec))
	{
		if (ec) { confined = false; break; }
		if (!it->is_regular_file(ec)) continue;
		std::string pc;
		try { pc = fs::canonical(it->path()).string(); } catch (...) { confined = false; break; }
		if (pc.rfind(destc + "/", 0) != 0) { confined = false; break; }
	}
	printf("#1369: confined=%s\n", confined ? "true" : "false");
	return confined ? 0 : 1;
}

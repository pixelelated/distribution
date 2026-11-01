// T36 #683 S10 G-14: removeFile of a broken symlink. The pin's guard uses exists() (which
// follows the link), so a dangling link looks absent and removeFile returns true without
// unlinking it. The fixed guard also asks isSymlink(), so the dangling link is unlinked.
#include "utils/FileSystemUtil.h"
#include "Paths.h"
#include "Settings.h"
#include "utils/TimeUtil.h"
#include "utils/ZipFile.h"
#include <cstdio>
#include <cstdlib>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = false;
namespace Utils { namespace Zip { unsigned int ZipFile::computeCRC(unsigned int c, const void*, size_t) { return c; } } }
Utils::Time::DateTime::DateTime() {} Utils::Time::DateTime::DateTime(const time_t&) {} Utils::Time::DateTime::~DateTime() {}
int main()
{
	std::system("rm -rf /workspace/tmp/m6-t36/s10/g14 && mkdir -p /workspace/tmp/m6-t36/s10/g14");
	const char* target = "/workspace/tmp/m6-t36/s10/g14/target";
	const char* link   = "/workspace/tmp/m6-t36/s10/g14/link";
	FILE* f = fopen(target, "w"); if (f) { fputs("x", f); fclose(f); }
	if (symlink(target, link) != 0) { printf("G-14: could not create symlink\n"); return 2; }
	unlink(target);   // the link is now dangling

	bool r = Utils::FileSystem::removeFile(link);

	struct stat st;
	bool stillThere = (lstat(link, &st) == 0);   // lstat sees the link itself
	printf("G-14: removeFile=%d; dangling link still present=%d (want 0)\n", r, stillThere);
	if (stillThere) { printf("S10 G-14: FAIL (the broken symlink was not unlinked)\n"); return 1; }
	printf("S10 G-14: PASS\n");
	return 0;
}

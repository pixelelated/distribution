"""S4b (#680; #1289 PL-24, #1285 PL-16): the rotation record and the key maps, written and read back, extracted as written.

    python3 -I s4b-writes.py <es-app/src> [case ...]

From CaptureRotation.cpp: read(), recordAfterSession() and what sits
between `struct Known` (or the stamp before it) and read() -- the cache and
the stat helpers -- as the file has them. From KeyboardMapping.cpp:
KeyMappingFile::save, over the real KeyboardMapping.h and rapidjson.
Doubled: FileData and recordPath (a temporary path), fromTable (0),
CaptureRotationText (`turns=<n> from=own-launch`, the shape of fork #288's
record), DisplayAspect, LOG, and the two writers --
Utils::FileSystem::writeAllText as es-core has it (fopen "wb" in place; it
returns nothing and a failed open writes nothing) and
Utils::AtomicFile::writeText (a temporary, then rename; false and the
target untouched on a failure) -- each of which can be made to fail, or to
be killed after a number of bytes, like S2's.

  writefail        a failed write of the rotation record leaves the turns
                   read before (at the pin :175's write is unchecked and
                   :178-181 caches the new turns under the old record's mtime)
  samemtime-rename a record replaced by rename with the same mtime and size
                   (a restore through rclone keeps the modtime and writes a
                   temporary): the new turns are read (at the pin :103-108
                   answers from the cache by mtime alone)
  samemtime-size   a record rewritten in place, its mtime put back, one byte
                   longer: the new turns are read
  rotkill          the rotation record's write killed half-way leaves the
                   previous record whole
  keyskill-path    a key map saved to its own path, killed half-way, leaves
                   the previous map whole (:477 at S3's tip, the pin's :426)
  keyskill-file    the same through save(fileName) (:480, the pin's :429)
"""
import os
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1])
cases = sys.argv[2:] or ["writefail", "samemtime-rename", "samemtime-size", "rotkill", "keyskill-path", "keyskill-file"]
rot = (src / "CaptureRotation.cpp").read_text()
keys = (src / "KeyboardMapping.cpp").read_text()
keys_h = (src / "KeyboardMapping.h").read_text()
start = re.search(r"^\s*struct (RecordStamp|Known)\b", rot, re.M).start()
end = re.search(r"^\s*int read\(FileData\* game\)", rot, re.M).start()
cache = rot[start:end]
read = function(rot, r"^\s*int read\(FileData\* game\)", "S4b")
record = function(rot, r"^\s*void recordAfterSession\(FileData\* game, const std::string& emulator, time_t started\)", "S4b")
save = function(keys, r"^void KeyMappingFile::save\(const std::string& fileName\)", "S4b")
orders = re.search(r"^std::vector<std::string> targetOrders =.*?^};", keys, re.M | re.S).group(0)
rj = os.environ.get("RAPIDJSON_INCLUDE_DIR", "/workspace/tmp/m6-t33/rj/rapidjson-1.1.0/include")
print("writers: rotation %s; key maps %s" % (
    "AtomicFile::writeText" if "AtomicFile::writeText" in record else "writeAllText",
    "AtomicFile::writeText" if "AtomicFile::writeText" in save else "writeAllText"))

harness = r'''
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <map>
#include <mutex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <rapidjson/rapidjson.h>
#include <rapidjson/pointer.h>
#include <rapidjson/prettywriter.h>
#include <rapidjson/stringbuffer.h>
struct NullLog { template <class T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()

static long gKillAfter = -1;
static bool gFail = false;
struct Killed : std::runtime_error { Killed() : std::runtime_error("killed") {} };
static void writeMaybeKilled(const std::string& p, const std::string& t)
{
	std::ofstream o(p, std::ios::binary | std::ios::trunc);
	if (gKillAfter >= 0 && (long) t.size() > gKillAfter) { o << t.substr(0, gKillAfter); o.close(); throw Killed(); }
	o << t;
}
static std::string readAll(const std::string& p) { std::ifstream i(p, std::ios::binary); std::stringstream s; s << i.rdbuf(); return s.str(); }

namespace Utils
{
	namespace FileSystem
	{
		bool exists(const std::string& p, bool = true) { struct stat st; return ::stat(p.c_str(), &st) == 0; }
		bool isDirectory(const std::string& p) { struct stat st; return ::stat(p.c_str(), &st) == 0 && S_ISDIR(st.st_mode); }
		std::string getParent(const std::string& p) { auto s = p.rfind('/'); return s == std::string::npos ? "." : p.substr(0, s); }
		bool createDirectory(const std::string& p) { ::mkdir(p.c_str(), 0755); return true; }
		std::string readAllText(const std::string& p) { return readAll(p); }
		// es-core's: fopen "wb" in place, nothing returned; a failed open writes nothing.
		void writeAllText(const std::string& p, const std::string& t) { if (gFail) return; writeMaybeKilled(p, t); }
		struct FileSystemCache { static void reset(const std::string&) {} };
	}
	namespace AtomicFile
	{
		bool writeText(const std::string& p, const std::string& t, int = -1)
		{
			if (gFail) return false;
			std::string tmp = p + ".tmp.t33";
			try { writeMaybeKilled(tmp, t); } catch (...) { throw; }
			return ::rename(tmp.c_str(), p.c_str()) == 0;
		}
	}
}

namespace CaptureRotationText
{
	std::string recordText(int turns) { return "turns=" + std::to_string(turns) + " from=own-launch\n"; }
	bool recordFromOwnLaunch(const std::string& r) { return r.find("from=own-launch") != std::string::npos; }
	int parseRecord(const std::string& r) { auto i = r.find("turns="); return i == std::string::npos ? 0 : atoi(r.c_str() + i + 6); }
	int turnsFromLog(const std::string& log) { return atoi(log.c_str()); }
	int fold(int core, const std::string&) { return core; }
	bool shouldRecord(const std::string&, const std::string&, int, int) { return true; }
}
namespace DisplayAspect { void forgetScreenshots() {} }
struct FileData { std::string name, record; std::string getName() { return name; } };

static std::string gLaunchLog, gRetroarchConfig;
#define LAUNCH_LOG gLaunchLog.c_str()
#define RETROARCH_CONFIG gRetroarchConfig.c_str()
static std::mutex sLock;
static std::string recordPath(FileData* game) { return game->record; }
static int fromTable(FileData*) { return 0; }

''' + cache + "\n" + read + "\n" + record + "\n" + keys_h.replace("#pragma once", "") + "\n#include <algorithm>\n" + orders + "\n" + save + r'''

static int bad = 0;
static void verdict(const std::string& name, bool ok, const std::string& what)
{
	printf("%s %s: %s\n", ok ? "PASS" : "FAIL", name.c_str(), what.c_str());
	if (!ok) bad++;
}
static void writeFile(const std::string& p, const std::string& t) { std::ofstream o(p, std::ios::binary | std::ios::trunc); o << t; }
static void session(FileData* game, int turns)
{
	writeFile(gLaunchLog, std::to_string(turns) + "\n");
	recordAfterSession(game, "retroarch", 0);
}

int main(int argc, char** argv)
{
	setvbuf(stdout, nullptr, _IONBF, 0);
	char tmpl[] = "/workspace/tmp/m6-t33/tmp/s4b-w-XXXXXX";
	const std::string dir = mkdtemp(tmpl);
	gLaunchLog = dir + "/exec.log";
	gRetroarchConfig = dir + "/retroarch.cfg";
	for (int a = 1; a < argc; a++)
	{
		const std::string c = argv[a];
		gKillAfter = -1; gFail = false;
		FileData game { c, dir + "/" + c + ".rotation" };
		if (c == "writefail" || c == "rotkill")
		{
			writeFile(game.record, CaptureRotationText::recordText(1));
			const int before = read(&game);
			if (c == "writefail") gFail = true; else gKillAfter = 3;
			try { session(&game, 3); } catch (const Killed&) {}
			gFail = false; gKillAfter = -1;
			const std::string onDisk = readAll(game.record);
			const int after = read(&game);
			char line[256];
			snprintf(line, sizeof line, "read %d before; the record on disk \"%s\"; read %d after", before, onDisk.substr(0, onDisk.find('\n')).c_str(), after);
			if (c == "writefail")
				verdict("writefail (PL-24)", before == 1 && after == 1, line);
			else
				verdict("rotkill (PL-16)", onDisk == CaptureRotationText::recordText(1) && after == 1, line);
		}
		else if (c == "samemtime-rename" || c == "samemtime-size")
		{
			writeFile(game.record, CaptureRotationText::recordText(1));
			struct stat old; ::stat(game.record.c_str(), &old);
			const int before = read(&game);
			std::string text = CaptureRotationText::recordText(2);
			if (c == "samemtime-size") text = "turns=2 from=own-launch \n";
			const std::string target = c == "samemtime-rename" ? game.record + ".new" : game.record;
			writeFile(target, text);
			struct timespec times[2] = { old.st_atim, old.st_mtim };
			::utimensat(AT_FDCWD, target.c_str(), times, 0);
			if (c == "samemtime-rename") ::rename(target.c_str(), game.record.c_str());
			struct stat now; ::stat(game.record.c_str(), &now);
			const int after = read(&game);
			char line[256];
			snprintf(line, sizeof line, "read %d before; replaced with turns 2, mtime %s, size %s, inode %s; read %d after", before,
				(now.st_mtim.tv_sec == old.st_mtim.tv_sec && now.st_mtim.tv_nsec == old.st_mtim.tv_nsec) ? "the same" : "CHANGED",
				now.st_size == old.st_size ? "the same" : "one longer", now.st_ino == old.st_ino ? "the same" : "new", after);
			verdict(c + " (PL-24)", before == 1 && after == 2, line);
		}
		else if (c == "keyskill-path" || c == "keyskill-file")
		{
			KeyMappingFile map;
			map.path = dir + "/" + c + ".keys";
			const std::string other = dir + "/" + c + "-other.keys";
			const std::string target = c == "keyskill-path" ? map.path : other;
			writeFile(target, "previous keys");
			KeyMappingFile::PlayerMapping p;
			KeyMappingFile::KeyMapping m;
			m.triggers = { "a" };
			m.targets = { "KEY_ENTER" };
			p.mappings.push_back(m);
			map.players.push_back(p);
			gKillAfter = 5;
			try { if (c == "keyskill-path") map.save(); else map.save(other); } catch (const Killed&) {}
			gKillAfter = -1;
			const std::string onDisk = readAll(target);
			verdict(c + " (PL-16)", onDisk == "previous keys", "after a write killed at 5 bytes the previous map is " + std::string(onDisk == "previous keys" ? "whole" : "cut: \"" + onDisk + "\""));
		}
	}
	if (bad)
		printf("FAIL S4b writes: %d case(s)\n", bad);
	return bad ? 1 : 0;
}
'''
run(harness, "s4b-writes", ("-fsanitize=address,undefined", "-I", rj), args=tuple(cases))

// T36 (#683): utils-resources-tests -- the floor's cases over es-core/src/utils, with
// FileSystemUtil.cpp, StringUtil.cpp and md5.cpp linked whole and the few things they
// reach outside the slice defined here as doubles (Paths, Settings, ZipFile::computeCRC,
// DateTime, the Platform functions). The parse-only seams (GetShOutput, runSystemCommand,
// quitES, the Font scaling, cleanupVRAM) are read as text from tools/t36-extract.py's
// lifts under T36_X; no FreeType, no Renderer, no SDL is linked. Each case asserts what
// the brief's floor table says the pin does, and is run at the pin: the FAIL-at-pin
// candidates are seen to FAIL before any fix. 3.19 and 3.20 are NOT here -- they are held
// (D-WORKFLOW-215) and run by the held scripts into the held directory.
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"

#include "Paths.h"
#include "Settings.h"
#include "utils/FileSystemUtil.h"
#include "utils/StringUtil.h"
#include "utils/TimeUtil.h"
#include "utils/ZipFile.h"

#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
#include <unistd.h>
#include <sys/stat.h>

// ------------------------------------------------------------ the doubles
Paths* Paths::_instance = nullptr;
Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {}
std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; }
void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = true;   // the image default; a case that wants it off sets it
namespace Utils { namespace Zip {
unsigned int ZipFile::computeCRC(unsigned int crc, const void*, size_t) { return crc; }
} }
Utils::Time::DateTime::DateTime() {}
Utils::Time::DateTime::DateTime(const time_t&) {}
Utils::Time::DateTime::~DateTime() {}

// ------------------------------------------------------------ a scratch dir
namespace {
struct Scratch {
	std::string path;
	Scratch() {
		(void)std::system("mkdir -p /workspace/tmp/m6-t36/scratch");
		std::string t = "/workspace/tmp/m6-t36/scratch/ur.XXXXXX";
		std::vector<char> b(t.begin(), t.end()); b.push_back('\0');
		REQUIRE(mkdtemp(b.data()) != nullptr);
		path = b.data();
	}
	~Scratch() { std::string c = "rm -rf '" + path + "'"; (void)std::system(c.c_str()); }
	std::string at(const std::string& n) { return path + "/" + n; }
};
std::string slurp(const std::string& name) {
	std::ifstream f(std::string(T36_X) + "/x_" + name + ".inc");
	std::stringstream ss; ss << f.rdbuf(); return ss.str();
}
size_t count(const std::string& hay, const std::string& needle) {
	size_t n = 0; for (size_t i = hay.find(needle); i != std::string::npos; i = hay.find(needle, i + 1)) n++; return n;
}
void writeFile(const std::string& p, const std::string& s) {
	std::ofstream f(p, std::ios::binary); f.write(s.data(), (std::streamsize)s.size());
}
}

using namespace Utils;

// ======================= FAIL-at-pin candidates ===========================

TEST_CASE("3.1 toUpper/toLower fold a 3-byte UTF-8 codepoint wrongly (StringUtil.cpp:357-362, :398-403) [L-01]")
{
	// A 2-byte French pair is handled: U+00E9 e-acute <-> U+00C9.
	CHECK(String::toUpper("\xC3\xA9") == "\xC3\x89");
	CHECK(String::toLower("\xC3\x89") == "\xC3\xA9");
	// A 3-byte codepoint is the lead: U+1EA1 (a with dot below) upper is U+1EA0;
	// U+FF21 (fullwidth A) lower is U+FF41. The pin folds byte-wise, so these FAIL.
	CHECK(String::toUpper("\xE1\xBA\xA1") == "\xE1\xBA\xA0");
	CHECK(String::toLower("\xEF\xBC\xA1") == "\xEF\xBD\x81");
}

TEST_CASE("3.2 renameFile/copyFile return true over an absent source (FileSystemUtil.cpp:1451-1455, :1472-1474) [L-03]")
{
	Scratch s;
	// renameFile over an absent source: the pin returns true (T21's #1191; a collision).
	CHECK_FALSE(FileSystem::renameFile(s.at("nope"), s.at("dst"), false));
	// copyFile over an absent source: the pin returns true (this slice's half).
	CHECK_FALSE(FileSystem::copyFile(s.at("nope2"), s.at("dst2")));
	CHECK_FALSE(FileSystem::exists(s.at("dst2"), false));
}

TEST_CASE("3.3 writeAllText returns void and does not report a short write (FileSystemUtil.cpp:1429-1446) [L-04]")
{
	// At the pin there is no return to test; /dev/full makes fwrite short and nothing says so.
	std::ofstream probe("/dev/full"); bool haveDevFull = probe.is_open(); probe.close();
	if (!haveDevFull) { MESSAGE("no /dev/full on this host; recorded as untestable"); return; }
	FileSystem::writeAllText("/dev/full", "x");   // returns void: the failure is unreported
	MESSAGE("writeAllText is void at the pin; a fix's CHECK_FALSE comes with #1186");
}

TEST_CASE("3.4 readAllText/readAllLines read a file under three bytes as empty (FileSystemUtil.cpp:1369-1427) [L-02]")
{
	Scratch s; std::string p = s.at("two");
	writeFile(p, "1\n");   // two bytes
	// T20's fix (#1177, d9afa5c7c) is a collision: at the pin the BOM-skip fails the stream.
	CHECK(FileSystem::readAllText(p) == "1\n");
	CHECK(FileSystem::readAllLines(p).size() == 1);
	// A file of three+ bytes is read (the control).
	writeFile(s.at("three"), "abc\n");
	CHECK(FileSystem::readAllText(s.at("three")) == "abc\n");
}

TEST_CASE("3.26 removeFile leaves the deleted path cached as present (FileSystemUtil.cpp:1059-1087) [L-19, new]")
{
	Scratch s; std::string p = s.at("gone");
	writeFile(p, "x");
	CHECK(FileSystem::exists(p));                 // a miss then a hit: cached present
	CHECK(FileSystem::removeFile(p));             // erases, re-stats (isDirectory), unlinks
	// On disk it is gone:
	struct stat64 st; CHECK(stat64(p.c_str(), &st) != 0);
	// The cache still answers present (L-19): exists() with the cache on is stale.
	CHECK(FileSystem::exists(p) == false);        // FAIL at the pin: reads true from the cache
	// Uncached is correct:
	CHECK(FileSystem::exists(p, false) == false);
}

// ======================= the controls and the rest ========================

TEST_CASE("3.10 maskSecrets keeps a non-placeholder value at the pin (StringUtil.cpp:446-804) [L-14]")
{
	// The value is built at run time, never a literal (engineering-practices.md).
	std::string v; for (char c : std::string("ABCDEF0123456789")) v += c;
	std::string json = "{\"token\":\"" + v + "\"}";
	std::string masked = String::maskSecrets(json);
	// L-14: a JSON "token":"..." is not masked -- the value survives.
	bool survives = masked.find(v) != std::string::npos;
	CHECK(survives);   // records the pin's reach; the fix shrinks it
}

TEST_CASE("3.13 the exists cache: a miss then a write then exists(p,false) rewrites (FileSystemUtil.cpp) [L-12]")
{
	Scratch s; std::string p = s.at("late");
	CHECK_FALSE(FileSystem::exists(p));           // a miss, stored
	writeFile(p, "y");                            // written outside the cache's knowledge
	CHECK_FALSE(FileSystem::exists(p));           // the remembered miss, cached
	CHECK(FileSystem::exists(p, false));          // uncached rewrites the entry
	CHECK(FileSystem::exists(p));                 // now the cache agrees
}

TEST_CASE("3.15 createDirectory is idempotent and makes parents (FileSystemUtil.cpp:1089-1120) [L-16]")
{
	Scratch s; std::string d = s.at("a/b/c");
	CHECK(FileSystem::createDirectory(d));
	CHECK(FileSystem::isDirectory(d));
	CHECK(FileSystem::createDirectory(d));        // again: harmless, true
}

TEST_CASE("3.18 shellQuote wraps in single quotes and escapes ' (StringUtil.cpp:426-444)")
{
	CHECK(String::shellQuote("a b") == "'a b'");
	CHECK(String::shellQuote("it's") == "'it'\\''s'");
	CHECK(String::shellQuote("") == "''");
	CHECK(String::shellQuote("$`\\\"") == "'$`\\\"'");   // nothing but ' is special inside ''
}

TEST_CASE("3.21 createRelativePath by string prefix: a sibling gives .//a.png (FileSystemUtil.cpp:986) [R4 item 17]")
{
	bool contains = false;
	std::string rel = FileSystem::createRelativePath("/storage/roms/snes2/a.png", "/storage/roms/snes", false);
	CHECK(rel == ".//a.png");   // the prefix match at :980-997 does not stop at a component
	(void)contains;
}

TEST_CASE("3.7 runSystemCommand returns 0 and reads neither name nor window (Platform.cpp:853-880) [L-13]")
{
	std::string t = slurp("runsys");
	// strip the signature line (which names the params) and check the body never uses them.
	std::string body = t.substr(t.find('\n', t.find("runSystemCommand")) + 1);
	CHECK(count(t, "return 0;") == 1);                  // the body's only return
	CHECK(body.find("window") == std::string::npos);    // the body never reads window
	CHECK(body.find("name") == std::string::npos);      // nor name
	CHECK(count(t, "fork()") == 2);                     // a double fork that does not detach
	CHECK(count(t, "waitpid") == 2);                    // the caller waits
}

TEST_CASE("3.9 GetShOutput drops the last byte of each chunk (Platform.cpp:891-905) [L-06, T26 collision]")
{
	std::string t = slurp("gsh");
	CHECK(t.find("file.substr(0, file.size() - 1)") != std::string::npos);  // the lost byte
	CHECK(t.find("popen") != std::string::npos);
	// popen's failure is unchecked at the pin (no `if (pipe` guard before fgets).
	CHECK(t.find("if (pipe") == std::string::npos);
}

TEST_CASE("3.24 quitES news an SDL_Event and never frees it (Platform.cpp:216-239) [L-18]")
{
	std::string t = slurp("quites");
	CHECK(t.find("new SDL_Event()") != std::string::npos);
	CHECK(t.find("delete") == std::string::npos);
	CHECK(t.find("SDL_PushEvent(quit)") != std::string::npos);
}

TEST_CASE("3.8 Font::getHeight returns mMaxGlyphHeight, which grows as glyphs rasterise (Font.cpp) [L-08]")
{
	// The rule erratum: es-code-traps.md:118 says the height is fixed; the source grows it.
	std::string h = slurp("font_getheight"), g = slurp("font_glyph_grow");
	CHECK(h.find("return mMaxGlyphHeight * lineSpacing;") != std::string::npos);
	CHECK(g.find("mMaxGlyphHeight = glyphSize.y();") != std::string::npos);  // grown in getGlyph
	// so getHeight() before any glyph is rasterised under-reports: the positive is the guest's.
}

TEST_CASE("3.16 Font scales twice: the ctor scales mSize and getFromTheme asks again (Font.cpp) [L-07]")
{
	std::string c = slurp("font_ctor_scale"), t = slurp("font_fromtheme_scale");
	bool ctorScales = c.find("fontScale()") != std::string::npos || c.find("menuFontScale()") != std::string::npos;
	CHECK(ctorScales);
	CHECK(t.find("Font::get") != std::string::npos);   // getFromTheme calls Font::get, which scales again
}

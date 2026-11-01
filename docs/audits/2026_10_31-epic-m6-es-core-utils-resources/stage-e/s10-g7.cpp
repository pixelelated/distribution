// T36 #683 S10 G-7: chars2Unicode's `_cursor < length() - 2` underflows on a short string, so the
// 4-byte branch over-reads. The underflow only triggers for length-0/1 strings, which are always
// short-string-optimized (inline in the std::string object), so ASan cannot see the over-read on
// a real std::string, and a sub-granule poison of the bytes adjacent to the one valid byte is a
// no-op. The brief's ruling (option 2): the behaviour case over "" and "a" records what proper()
// does on the safe inputs (real function), and the FAIL-at-pin positive is SYNTHETIC -- the
// decoder's bounds logic lifted verbatim over a raw one-byte heap buffer, where the over-read
// crosses a real allocation boundary and ASan reports. The audit checkbox stays partial under
// the synthetic-input rule.
#include "utils/StringUtil.h"
#include "Paths.h"
#include "Settings.h"
#include <cstdio>
#include <cstddef>
#include <string>
Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = false;
#include G7C2U_INC   // inline unsigned int c2u(const char* _string, size_t _len, size_t& _cursor) -- the lifted bounds logic
int main(int argc, char** argv)
{
	std::string mode = argc > 1 ? argv[1] : "synthetic";
	if (mode == "behaviour")
	{
		std::string e = Utils::String::proper(std::string());
		std::string a = Utils::String::proper(std::string("a"));
		printf("G-7 behaviour: proper(\"\")=len%zu; proper(\"a\")=\"%s\"\n", e.size(), a.c_str());
		if (!e.empty() || a != "A") { printf("S10 G-7 behaviour: FAIL\n"); return 1; }
		printf("S10 G-7 behaviour: PASS\n");
		return 0;
	}
	// a two-byte heap buffer models c_str(): one logical byte and the null terminator, so the
	// safe 2-byte branch's read of index 1 is valid and only the 4-byte underflow over-reads.
	char* buf = new char[2];
	buf[0] = (char)0xF0;
	buf[1] = '\0';   // like c_str()[size()]
	size_t cursor = 0;
	unsigned int cp = c2u(buf, 1, cursor);   // pin: the underflow reads buf[2..3] past the buffer
	delete[] buf;
	printf("S10 G-7 synthetic: PASS (no over-read; cp=%u cursor=%zu)\n", cp, cursor);
	return 0;
}

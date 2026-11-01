// T36 #683 S10 G-6/G-7: StringUtil.cpp linked whole under AddressSanitizer. argv[1] picks the
// finding so each is proven to fail at the pin on its own (ASan halts at the first overflow).
// G-6: startsWithIgnoreCase("abc","abc") must not read past either terminator.
// G-7: proper("a\xF0") feeds a one-byte string starting with a 4-byte lead into chars2Unicode;
//      the pin's `_cursor < length() - 2` underflows and reads past the end.
#include "utils/StringUtil.h"
#include "Paths.h"
#include "Settings.h"
#include <cstdio>
#include <string>
Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = false;
int main(int argc, char** argv)
{
	using namespace Utils::String;
	std::string which = argc > 1 ? argv[1] : "6";
	if (which == "6")
	{
		bool a = startsWithIgnoreCase("abc", "abc");
		bool b = startsWithIgnoreCase("abcdef", "abc");
		bool c = startsWithIgnoreCase("ab", "abc");
		printf("G-6: (abc,abc)=%d (abcdef,abc)=%d (ab,abc)=%d\n", a, b, c);
		if (!a || !b || c) { printf("S10 G-6: FAIL (semantics)\n"); return 1; }
		printf("S10 G-6: PASS\n");
	}
	else
	{
		std::string p = proper(std::string("a\xF0", 2));
		printf("G-7: proper len=%zu\n", p.size());
		printf("S10 G-7: PASS\n");
	}
	return 0;
}

// T36 #683 S10 G-10: stringToTime lifted (linking TimeUtil.cpp whole cascades). A 20-char heap
// input (past short-string optimization) with a format of 20 literals then %d: at the pin the
// literals advance s to the terminator while parsedChars stays 0, so %d reads past the heap
// buffer (ASan); the fix advances parsedChars for a literal too, so the loop ends first.
#include <ctime>
#include <string>
#include <cstddef>
#include <cstdio>
namespace Utils { namespace Time {
#include G10_INC
}}
int main()
{
	std::string in(20, 'x');
	std::string fmt = in + "%d";
	volatile time_t t = Utils::Time::stringToTime(in, fmt);
	(void)t;
	printf("S10 G-10: PASS (the literal kept the field bounds honest; no read past the input)\n");
	return 0;
}

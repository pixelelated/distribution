// T36 #683 S2 (PL-07/#1360, G-9): the date format's stack buffer overflow. timeToString is
// lifted verbatim (T36_INC) and run under ASan with a format whose expansion passes 256 bytes.
// At the pin: stack-buffer-overflow. After the fix: no report, and a short format's output is
// unchanged (the control).
#include <string>
#include <ctime>
#include <cstdio>
#include T36_INC
int main(){
	std::string longfmt; for (int i = 0; i < 200; i++) longfmt += "%Y";   // 800 bytes of digits
	volatile std::string r = timeToString(time(nullptr), longfmt);
	std::string c = timeToString(0, "%Y-%m-%d");                          // control
	printf("control: '%s' (len %zu)\n", c.c_str(), c.size());
	return 0;
}

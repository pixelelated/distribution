// T21 (#668) S10: T20's five reader cases (distribution ffb6b686cb,
// docs/audits/2026_10_26-epic-m6-es-achievements-pages/stage-b/positives/reader.cpp)
// run through the tree's ScriptOutput -- the reader and the exit the
// executors use since S10 -- with the executors' loop as S10 writes it:
// popen, fread into LineReader, finish, exitCode(pclose).
//   g++ -std=c++17 -I <es>/es-app/src s10-reader.cpp <es>/es-app/src/ScriptOutput.cpp
#include "ScriptOutput.h"

#include <cstdio>
#include <iostream>
#include <string>

int main()
{
	struct Case { const char* name; const char* cmd; };
	Case cases[] = {
		{"popen-child-killed", "echo hardcore=0; kill -KILL $$"},
		{"killed-by-signal", "sh -c 'echo hardcore=0; kill -KILL $$'"},
		{"exit-143", "sh -c 'echo hardcore=0; exit 143'"},
		{"line-1500-bytes", "python3 -I -c 'print(\"{\\\"id\\\":1,\\\"title\\\":\\\"\" + \"x\"*1480 + \"\\\"}\"); print(\"{\\\"id\\\":2}\")'"},
		{"last-line-no-newline", "printf 'first\\nhardcore=1'"},
	};
	for (auto& c : cases)
	{
		std::string last; int n = 0; size_t longest = 0;
		FILE* pipe = popen(c.cmd, "r");
		ScriptOutput::LineReader reader([&](const std::string& l) { if (l.empty()) return; last = l; n++; if (l.size() > longest) longest = l.size(); });
		char buffer[4096];
		size_t got;
		while ((got = fread(buffer, 1, sizeof(buffer), pipe)) > 0)
			reader.feed(buffer, got);
		reader.finish();
		const int rc = ScriptOutput::exitCode(pclose(pipe));
		std::cout << "RESULT " << c.name << " rc=" << rc << " lines=" << n << " longest=" << longest << " last=[" << last.substr(0, 40) << "]\n";
	}
}

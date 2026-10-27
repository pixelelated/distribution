// T26 (#673) stage B fixture: Platform.cpp's GetShOutput, lifted verbatim at
// the pin (es-core/src/utils/Platform.cpp:891-905, below between the markers),
// fed four outputs. Shows what GuiMenu.cpp's readers of it receive.
#include <cstdio>
#include <string>
#include <iostream>
#include <algorithm>
namespace Utils { namespace Platform {
// ---- verbatim from the pin ----
		std::string GetShOutput(const std::string& mStr)
		{
			std::string result, file;
			FILE* pipe{popen(mStr.c_str(), "r")};
			char buffer[256];

			while(fgets(buffer, sizeof(buffer), pipe) != NULL)
			{
				file = buffer;
				result += file.substr(0, file.size() - 1);
			}

			pclose(pipe);
			return result;
		}
// ---- end verbatim ----
}}
static void show(const char* what, const std::string& cmd)
{
	const std::string out = Utils::Platform::GetShOutput(cmd);
	std::cout << what << ": " << out.size() << " bytes; ";
	const size_t ok = out.find("OK=");
	std::cout << "find(OK=) " << (ok == std::string::npos ? std::string("none") : "name '" + out.substr(ok + 3) + "'");
	std::cout << "; newlines " << std::count(out.begin(), out.end(), '\n');
	std::cout << "; 'Turn off both automatic' " << (out.find("Turn off both automatic") != std::string::npos ? "found" : "NOT found") << "\n";
}
int main()
{
	// 1. cloud_remote's success: one short line.
	show("1 one line 'OK=dropbox\\n'", "printf 'OK=dropbox\\n'");
	// 2. a 300-byte line, then OK=: the long line loses a byte at 255; OK= intact.
	show("2 300-byte line then OK=", "printf '%0300d\\nOK=dropbox\\n' 0");
	// 3. the last line without a newline: its last character goes.
	show("3 'OK=dropbox' with no newline", "printf 'OK=dropbox'");
	// 4. the refusal sentence straddling byte 255 of a long stderr line.
	show("4 refusal across byte 255", "printf '%0240dTurn off both automatic save sync options first.\\n' 0");
	return 0;
}

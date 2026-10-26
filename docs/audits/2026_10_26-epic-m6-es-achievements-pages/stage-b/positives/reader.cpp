#include <cstdio>
#include <sstream>
#include <string>
#include <functional>
#include <iostream>
#include <sys/wait.h>
namespace Utils{namespace String{static std::string maskSecrets(const std::string& s){return s;}}}
struct NullLog{template<class T> NullLog& operator<<(const T&){return *this;}};
#define LOG(x) NullLog()
struct ApiSystem{static std::pair<std::string,int> executeScriptLegacy(const std::string&, const std::function<void(const std::string)>&);};
// ---- verbatim from ApiSystem.cpp:2262-2293 at 16dbac5211 ----

std::pair<std::string, int> ApiSystem::executeScriptLegacy(const std::string& command, const std::function<void(const std::string)>& func)
{
	const std::string shown = Utils::String::maskSecrets(command);
	std::cout << "ApiSystem::executeScriptLegacy -> " << shown << std::endl;
	LOG(LogInfo) << "ApiSystem::executeScriptLegacy -> " << shown;

	FILE *pipe = popen(command.c_str(), "r");
	if (pipe == NULL)
	{
		LOG(LogError) << "Error executing " << shown;
		return std::pair<std::string, int>("Error starting command : " + shown, -1);
	}

	std::stringstream output_stream;
	char buff[1024];
	while (fgets(buff, 1024, pipe))
	{
		std::stringstream output_stream(buff);
		std::string line;
		while (getline(output_stream, line).good()) {
			if (line.empty()) continue;
			std::cout << line << std::endl;
			if (func != nullptr) {
				func(std::string(line));
			}
		}
	}

	int exitCode = WEXITSTATUS(pclose(pipe));
	return std::pair<std::string, int>("", exitCode);
}
// ---- end verbatim ----
int main(){
  struct Case{const char* name; const char* cmd;};
  Case cases[] = {
    {"popen-child-killed", "echo hardcore=0; kill -KILL $$"},
    {"killed-by-signal", "sh -c 'echo hardcore=0; kill -KILL $$'"},
    {"exit-143", "sh -c 'echo hardcore=0; exit 143'"},
    {"line-1500-bytes", "python3 -I -c 'print(\"{\\\"id\\\":1,\\\"title\\\":\\\"\" + \"x\"*1480 + \"\\\"}\"); print(\"{\\\"id\\\":2}\")'"},
    {"last-line-no-newline", "printf 'first\\nhardcore=1'"},
  };
  for (auto& c : cases) {
    std::string last; int n = 0; size_t longest = 0;
    auto r = ApiSystem::executeScriptLegacy(c.cmd, [&](const std::string l){ last = l; n++; if (l.size() > longest) longest = l.size(); });
    std::cerr << "RESULT " << c.name << " rc=" << r.second << " lines=" << n << " longest=" << longest << " last=[" << last.substr(0, 40) << "]\n";
  }
}

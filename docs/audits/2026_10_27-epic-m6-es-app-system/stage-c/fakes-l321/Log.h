// T33 3.21 fake (#680): LOG lines recorded in gLogLines, so a harness can
// assert whether the parse said anything. The macro's shape is es-core's
// Log.h:9.
#pragma once
#include <sstream>
#include <string>
#include <vector>
enum LogLevel { LogError, LogWarning, LogInfo, LogDebug };
inline std::vector<std::string>& gLogLines() { static std::vector<std::string> v; return v; }
struct Log { std::ostringstream s; explicit Log(LogLevel) {} ~Log() { gLogLines().push_back(s.str()); } std::ostringstream& stream() { return s; } };
#define LOG(level) Log(level).stream()

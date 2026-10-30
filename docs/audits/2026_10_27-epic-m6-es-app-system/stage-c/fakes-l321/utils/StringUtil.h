// T33 3.21 fake (#680): the five Utils::String calls KeyboardMapping.cpp makes.
#pragma once
#include <algorithm>
#include <cstdarg>
#include <cstdio>
#include <string>
#include <vector>
namespace Utils { namespace String {
inline std::vector<std::string> splitAny(const std::string& s, const std::string& seps, bool removeEmpty = false) {
    std::vector<std::string> out; std::string cur;
    for (char c : s) { if (seps.find(c) != std::string::npos) { if (!removeEmpty || !cur.empty()) out.push_back(cur); cur.clear(); } else cur += c; }
    if (!removeEmpty || !cur.empty()) out.push_back(cur); return out; }
inline std::vector<std::string> split(const std::string& s, char sep, bool removeEmpty = false) { return splitAny(s, std::string(1, sep), removeEmpty); }
inline std::string format(const char* fmt, ...) { char buf[1024]; va_list a; va_start(a, fmt); vsnprintf(buf, sizeof(buf), fmt, a); va_end(a); return buf; }
inline bool startsWith(const std::string& s, const std::string& p) { return s.rfind(p, 0) == 0; }
inline std::string toLower(std::string s) { std::transform(s.begin(), s.end(), s.begin(), ::tolower); return s; }
inline std::string trim(const std::string& s) { auto b = s.find_first_not_of(" \t\r\n"); if (b == std::string::npos) return ""; auto e = s.find_last_not_of(" \t\r\n"); return s.substr(b, e - b + 1); }
} }

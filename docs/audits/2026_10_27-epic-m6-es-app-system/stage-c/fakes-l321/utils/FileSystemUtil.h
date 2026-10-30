// T33 3.21 fake (#680): the calls KeyboardMapping.cpp makes, on the host's files (S4b: the cache reset after its save).
#pragma once
#include <fstream>
#include <sstream>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
namespace Utils { namespace FileSystem {
inline bool exists(const std::string& p, bool = true) { struct stat st; return ::stat(p.c_str(), &st) == 0; }
inline bool isDirectory(const std::string& p) { struct stat st; return ::stat(p.c_str(), &st) == 0 && S_ISDIR(st.st_mode); }
inline std::string getParent(const std::string& p) { return p.substr(0, p.rfind('/')); }
inline bool createDirectory(const std::string& p) { return ::mkdir(p.c_str(), 0755) == 0; }
inline std::string readAllText(const std::string& p) { std::stringstream ss; ss << std::ifstream(p).rdbuf(); return ss.str(); }
inline bool removeFile(const std::string& p) { return ::unlink(p.c_str()) == 0; }
inline void writeAllText(const std::string& p, const std::string& t) { std::ofstream(p) << t; }
struct FileSystemCache { static void reset(const std::string&) {} };
} }

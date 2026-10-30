// T33 3.21 fake (#680, S4b): KeyMappingFile::save's writer since S4b, temp-and-rename on the host's files.
#pragma once
#include <cstdio>
#include <fstream>
#include <string>
namespace Utils { namespace AtomicFile {
inline bool writeText(const std::string& p, const std::string& t, int = -1) { const std::string tmp = p + ".tmp.t33"; { std::ofstream o(tmp, std::ios::binary | std::ios::trunc); o << t; if (!o) return false; } return std::rename(tmp.c_str(), p.c_str()) == 0; }
} }

// T21 (#668) stage B: the pin's SystemConf.cpp and AtomicFileUtil.cpp, built
// with the host's g++ against the doubles es-app/tests/unit/SystemConfTests.cpp
// uses (copied below as they stand at 16dbac5211), driven from the command
// line so a run can be killed at any step (killer.c) and the files read after.
//
//   state-fixture write <path> <textfile>              AtomicFile::writeText(path, text)
//   state-fixture settings-shape <path> <textfile>     Settings::saveFile's two writes, in its order
//   state-fixture choose <path>                        AtomicFile::chooseConfig: source and record
//   state-fixture set <path> <lock> <key> <valuefile>  SystemConf::set and saveSystemConf
//   state-fixture get <path> <lock> <key>              a fresh SystemConf's load, then get(key)
//   state-fixture parse <path> <key>                   AtomicFile::parseKeyValues: is the key there
//
// Writes only the paths it is given. Exit 0 on the call's success, 1 on its
// failure, 2 on a usage error.
#include "Log.h"
#include "Paths.h"
#include "Settings.h"
#include "SystemConf.h"
#include "utils/AtomicFileUtil.h"

#include <cstdio>
#include <fstream>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>

// ---- the doubles, as SystemConfTests.cpp:38-76 has them at the pin ----
LogLevel Log::mReportingLevel = LogDebug;
bool Log::mEnabled = true;
namespace
{
	std::mutex gLogMutex;
	std::string gLog;
	thread_local std::ostringstream tlLine;
}
Log::Log(LogLevel level) : mLevel(level) { tlLine.str(""); tlLine.clear(); }
Log::~Log() { std::lock_guard<std::mutex> lock(gLogMutex); gLog += tlLine.str() + "\n"; }
std::ostringstream& Log::stream() { return tlLine; }
Paths* Paths::_instance = nullptr;
Paths::Paths() {}
Settings* Settings::getInstance() { return nullptr; }
bool Settings::saveFile() { return false; }
std::string Settings::getString(const std::string&) { return ""; }
bool Settings::setString(const std::string&, const std::string&) { return false; }
bool Settings::getBool(const std::string&) { return false; }
bool Settings::setBool(const std::string&, bool) { return false; }

struct SystemConfTestAccess
{
	static SystemConf* fresh(const std::string& path, const std::string& lockPath, int budgetMs)
	{
		delete SystemConf::sInstance;
		SystemConf::sInstance = nullptr;
		SystemConf::sRecovered = false;
		SystemConf::sLockPath = lockPath;
		SystemConf::sLockBudgetMs = budgetMs;
		Paths::getSystemConfFilePath() = path;
		return SystemConf::getInstance();
	}
};
// ---- end of the doubles ----

static std::string slurp(const std::string& path)
{
	std::ifstream in(path, std::ios::binary);
	std::stringstream ss;
	ss << in.rdbuf();
	return ss.str();
}

static const char* sourceName(Utils::AtomicFile::LoadedConfig::Source s)
{
	switch (s)
	{
	case Utils::AtomicFile::LoadedConfig::Source::Live: return "Live";
	case Utils::AtomicFile::LoadedConfig::Source::Temporary: return "Temporary";
	case Utils::AtomicFile::LoadedConfig::Source::Backup: return "Backup";
	case Utils::AtomicFile::LoadedConfig::Source::Damaged: return "Damaged";
	case Utils::AtomicFile::LoadedConfig::Source::Missing: return "Missing";
	}
	return "?";
}

int main(int argc, char** argv)
{
	if (argc < 3)
		return 2;
	const std::string mode = argv[1];
	if (mode == "write" && argc == 4)
		return Utils::AtomicFile::writeText(argv[2], slurp(argv[3])) ? 0 : 1;
	if (mode == "settings-shape" && argc == 4)
	{
		// Settings.cpp:524 and :533 at the pin: the live file, then its record
		// with the live file's mode. (The pugixml serialisation before them is
		// not built here: the host has no pugixml.)
		const std::string path = argv[2], text = slurp(argv[3]);
		if (!Utils::AtomicFile::writeText(path, text))
			return 1;
		return Utils::AtomicFile::writeText(path + ".backup", text, Utils::AtomicFile::modeOf(path, 0644)) ? 0 : 1;
	}
	if (mode == "choose" && argc == 3)
	{
		const auto chosen = Utils::AtomicFile::chooseConfig(argv[2]);
		std::cout << "source=" << sourceName(chosen.source) << " record=" << (chosen.record ? 1 : 0) << std::endl;
		return 0;
	}
	if (mode == "set" && argc == 6)
	{
		SystemConf* conf = SystemConfTestAccess::fresh(argv[2], argv[3], 500);
		conf->set(argv[4], slurp(argv[5]));
		return conf->saveSystemConf() ? 0 : 1;
	}
	if (mode == "get" && argc == 5)
	{
		SystemConf* conf = SystemConfTestAccess::fresh(argv[2], argv[3], 500);
		std::cout << "value=[" << conf->get(argv[4]) << "]" << std::endl;
		return 0;
	}
	if (mode == "parse" && argc == 4)
	{
		const auto values = Utils::AtomicFile::parseKeyValues(slurp(argv[2]));
		std::cout << "keys=" << values.size() << " has[" << argv[3] << "]=" << (values.count(argv[3]) ? 1 : 0) << std::endl;
		return 0;
	}
	return 2;
}

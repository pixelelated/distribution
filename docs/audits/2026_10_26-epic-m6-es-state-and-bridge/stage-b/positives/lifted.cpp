// T21 (#668) stage B: four functions lifted verbatim from the pin
// (16dbac5211) where the host cannot build their files (curl, SDL), each run
// on the input its lead names. Built with AddressSanitizer and UBSan, and
// linked with the pin's es-core/src/utils/StringUtil.cpp for the helpers the
// first one calls. One case per run, so a sanitizer's abort ends only that one:
//
//   lifted header   HttpReq::header_callback      (HttpReq.cpp:579-594)
//   lifted led      ApiSystem::getLEDColours      (ApiSystem.cpp:1868-1890)
//   lifted enum     ApiSystem::executeEnumerationScript (ApiSystem.cpp:2233-2253)
//   lifted script   ApiSystem::executeScript(cmd, func) (ApiSystem.cpp:2295-2321)
#include "utils/StringUtil.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <sys/wait.h>
#include <vector>

struct NullLog { template <class T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()

// ---- HttpReq.cpp:579-594, verbatim but for the class name ----
struct HttpReqLift
{
	std::map<std::string, std::string> mResponseHeaders;
	static size_t header_callback(char *buffer, size_t size, size_t nitems, void *userdata);
};
size_t HttpReqLift::header_callback(char *buffer, size_t size, size_t nitems, void *userdata)
{
	HttpReqLift* request = ((HttpReqLift*)userdata);

	std::string data = Utils::String::trim(buffer);
	if (!data.empty() && !Utils::String::startsWith(data, "HTTP/"))
	{
		auto splitPost = data.find(":");
		if (splitPost != std::string::npos)
			request->mResponseHeaders[Utils::String::trim(data.substr(0, splitPost))] = Utils::String::trim(data.substr(splitPost + 1));
		else
			request->mResponseHeaders[data] = "";
	}

	return nitems * size;
}

// ---- ApiSystem.cpp:1868-1890, verbatim; SystemConf's get is the argument ----
static void getLEDColours(const std::string& confValue, int& red, int& green, int& blue)
{
	std::string colourValue = confValue;   // SystemConf::getInstance()->get("led.colour");
	if (colourValue.empty())
		colourValue = "255 0 165";

    std::stringstream ss(colourValue);
    std::string token;

	// Extract red value
    std::getline(ss, token, ' ');
    red = std::stoi(token);

	// Extract green value
    std::getline(ss, token, ' ');
    green = std::stoi(token);

	// Extract blue value
    std::getline(ss, token);
    blue = std::stoi(token);

	LOG(LogInfo) << "ApiSystem::getLEDColours > LED colours are: " << red << " " << green << " " << blue;
}

// ---- ApiSystem.cpp:2233-2253, verbatim ----
static std::vector<std::string> executeEnumerationScript(const std::string command)
{
	LOG(LogDebug) << "ApiSystem::executeEnumerationScript -> " << Utils::String::maskSecrets(command);

	std::vector<std::string> res;

	FILE *pipe = popen(command.c_str(), "r");

	if (pipe == NULL)
		return res;

	char line[1024];
	while (fgets(line, 1024, pipe))
	{
		strtok(line, "\n");
		res.push_back(std::string(line));
	}

	pclose(pipe);
	return res;
}

// ---- ApiSystem.cpp:2295-2321, verbatim ----
static std::pair<std::string, int> executeScript(const std::string command, const std::function<void(const std::string)>& func)
{
	const std::string shown = Utils::String::maskSecrets(command);
	LOG(LogInfo) << "ApiSystem::executeScript -> " << shown;

	FILE *pipe = popen(command.c_str(), "r");
	if (pipe == NULL)
	{
		LOG(LogError) << "Error executing " << shown;
		return std::pair<std::string, int>("Error starting command : " + shown, -1);
	}

	// Zeroed: the pair's first member is built from this buffer after the
	// loop, and a command that printed nothing -- wifictl current with no
	// network joined -- used to hand it back uninitialised.
	char line[1024] = "";
	while (fgets(line, 1024, pipe))
	{
		strtok(line, "\n");

		if (func != nullptr)
			func(std::string(line));
	}

	int exitCode = WEXITSTATUS(pclose(pipe));
	return std::pair<std::string, int>(line, exitCode);
}

static std::string show(const std::vector<std::string>& v)
{
	std::string s = "[";
	for (size_t i = 0; i < v.size(); i++)
		s += (i ? "," : "") + std::string("\"") + v[i] + "\"";
	return s + "]";
}

int main(int argc, char** argv)
{
	const std::string which = argc > 1 ? argv[1] : "";
	if (which == "header")
	{
		// curl hands the header callback a buffer of size*nitems bytes that is
		// not NUL-terminated (CURLOPT_HEADERFUNCTION's contract). A heap block
		// of exactly that size, as a response header arrives.
		const char text[] = "X-Pixel: abc\r\n";
		const size_t n = sizeof(text) - 1;
		char* buffer = (char*) malloc(n);
		memcpy(buffer, text, n);
		HttpReqLift req;
		HttpReqLift::header_callback(buffer, 1, n, &req);
		std::cout << "header parsed: " << req.mResponseHeaders.size() << " header(s)" << std::endl;
		free(buffer);
		return 0;
	}
	if (which == "led")
	{
		for (const char* value : { "255 0 165", "255 0", "red", "255,0,165" })
		{
			int r = -1, g = -1, b = -1;
			try
			{
				getLEDColours(value, r, g, b);
				std::cout << "led.colour=[" << value << "] -> " << r << " " << g << " " << b << std::endl;
			}
			catch (const std::exception& e)
			{
				std::cout << "led.colour=[" << value << "] -> THROWS " << e.what() << " (the pin's code has no catch)" << std::endl;
			}
		}
		return 0;
	}
	if (which == "enum")
	{
		for (const char* cmd : { "printf 'a\\nb\\n'", "printf 'a\\nb\\n'; exit 3", "printf 'a\\nb\\n'; kill -9 $$" })
			std::cout << "[" << cmd << "] -> " << show(executeEnumerationScript(cmd)) << std::endl;
		return 0;
	}
	if (which == "script")
	{
		for (const char* cmd : { "echo joined; exit 0", "echo joined; exit 1", "echo joined; kill -9 $$", "echo joined; kill -TERM $$" })
		{
			std::vector<std::string> lines;
			const auto r = executeScript(cmd, [&lines](const std::string line) { lines.push_back(line); });
			std::cout << "[" << cmd << "] -> exit " << r.second << ", lines " << show(lines) << std::endl;
		}
		return 0;
	}
	return 2;
}

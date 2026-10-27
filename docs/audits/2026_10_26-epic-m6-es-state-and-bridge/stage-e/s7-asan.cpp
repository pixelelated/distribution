// T21 (#668) S7: HttpReq's three bounds under AddressSanitizer and UBSan,
// on a host without curl. One case per run, so a sanitizer's abort ends
// only that one:
//
//   s7-asan header       the tree's HttpText::parseHeaderLine over a heap
//                        buffer of exactly the header's bytes, as curl gives it
//   s7-asan status-pin   HttpReq.cpp's response-code lines at the pin, lifted:
//                        int http_status_code; curl_easy_getinfo(..., &code)
//   s7-asan status-s7    the same lines as S7 writes them: a long
//   s7-asan leak-pin     the custom-header list at the pin, lifted: appended,
//                        handed to curl, never freed
//   s7-asan leak-s7      as S7 keeps it: freed when the request goes
//
// The stand-in for curl_easy_getinfo writes a long, as curl does for
// CURLINFO_RESPONSE_CODE; the stand-in slist allocates as curl's does. The
// lifted lines are copied from the pin and from the S7 commit, and say so.
//
//   g++ -std=c++17 -O0 -g -fsanitize=address,undefined -fno-omit-frame-pointer \
//     -I <es>/es-core/src s7-asan.cpp <es>/es-core/src/HttpText.cpp <es>/es-core/src/utils/StringUtil.cpp
#include "HttpText.h"

#include <cstdarg>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>

namespace
{
	// curl_easy_getinfo(handle, CURLINFO_RESPONSE_CODE, long*): writes a long.
	int stub_getinfo(void*, int, ...)
	{
		va_list ap;
		va_start(ap, 0);
		long* out = va_arg(ap, long*);
		va_end(ap);
		*out = 404;
		return 0;
	}

	struct slist { char* data; slist* next; };
	slist* stub_slist_append(slist* list, const char* s)
	{
		slist* item = (slist*) malloc(sizeof(slist));
		item->data = strdup(s);
		item->next = nullptr;
		if (list == nullptr)
			return item;
		slist* last = list;
		while (last->next != nullptr)
			last = last->next;
		last->next = item;
		return list;
	}
	void stub_slist_free_all(slist* list)
	{
		while (list != nullptr)
		{
			slist* next = list->next;
			free(list->data);
			free(list);
			list = next;
		}
	}
}

int main(int argc, char** argv)
{
	const std::string which = argc > 1 ? argv[1] : "";
	if (which == "header")
	{
		const std::string line = "Content-Type: image/png\r\n";
		char* buffer = (char*) malloc(line.size());   // no terminator, as curl's
		memcpy(buffer, line.data(), line.size());
		std::string name, value;
		const bool ok = HttpText::parseHeaderLine(buffer, line.size(), name, value);
		std::cout << "header parsed: " << ok << " [" << name << "] [" << value << "]" << std::endl;
		free(buffer);
		return 0;
	}
	if (which == "status-pin")
	{
		// HttpReq.cpp:432-433 at the pin.
		int http_status_code;
		stub_getinfo(nullptr, 0, &http_status_code);
		std::cout << "status read: " << http_status_code << std::endl;
		return 0;
	}
	if (which == "status-s7")
	{
		// HttpReq.cpp as S7 writes it.
		long http_status_code = 0;
		if (stub_getinfo(nullptr, 0, &http_status_code) != 0)
			http_status_code = 0;
		std::cout << "status read: " << http_status_code << std::endl;
		return 0;
	}
	if (which == "leak-pin" || which == "leak-s7")
	{
		// HttpReq.cpp:174-179 at the pin: a local list, handed over, kept by
		// nothing. S7 keeps it in mHeaders and frees it in the destructor.
		slist* hs = nullptr;
		hs = stub_slist_append(hs, "Referer: https://example.invalid/");
		hs = stub_slist_append(hs, "X-Other: 1");
		if (which == "leak-s7")
			stub_slist_free_all(hs);
		std::cout << "headers sent" << std::endl;
		return 0;
	}
	std::cerr << "usage: s7-asan header|status-pin|status-s7|leak-pin|leak-s7" << std::endl;
	return 2;
}

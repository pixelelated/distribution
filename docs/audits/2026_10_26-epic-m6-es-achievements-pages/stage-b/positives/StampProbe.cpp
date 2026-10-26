// T20 positive (#667): CloudText::parseScanStamp on a stamp carrying T19 S8's ready=unknown.
#include "doctest/doctest.h"
#include "CloudText.h"
#include <iostream>
TEST_CASE("T20 probe: ready=unknown in last-scan")
{
	const auto s = CloudText::parseScanStamp("1789000000 0 topup cached=0 skipped=0 ready=unknown limit=0 indexed=0 errors=0 added=0");
	std::cout << "PROBE ran=" << s.ran << " code=" << s.code << " topup=" << s.topup << " ready=" << s.ready << " added=" << s.added << std::endl;
	CHECK(s.ran);
}

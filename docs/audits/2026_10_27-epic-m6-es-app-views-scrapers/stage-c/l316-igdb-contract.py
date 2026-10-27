"""3.16's remainder and L-22 (#679): IGDB's process() breaks the scrapers' return
contract, and the IGDB and HfsDB token reads use the response's shape unchecked.

    python3 -I l316-igdb-contract.py <IGDBScraper.cpp> <HfsDBScraper.cpp> <rapidjson include dir> [--control]

IGDBRequest::process, IGDBScraper::ensureToken and HfsDBScraper::ensureToken are
extracted as written and compiled against the recipe's rapidjson 1.1.0 with
NDEBUG, as the shipped build has it (l310's note), and RAPIDJSON_ASSERT
counting each violated precondition. The HttpReq, Settings and clock are
doubles; the token request's body is the case's.
- 3.16's remainder. The contract is written above process() in IGDB
  (:313) and in GamesDB and ArcadeDB: "Process should return false only when
  we reached a maximum scrap by minute, to retry". IGDB returns false for an
  empty answer (no match, :324-329) and on a parse error (:318-322). Each must
  return true, as the three others do. At the pin both return false -- FAIL.
  Today the return is dropped (Scraper.cpp:337, 3.13), so the defect is a
  trap for 3.13's fix: a caller that honours the contract would retry an
  empty answer as if rate-limited. The fix lands with 3.13's or before it.
- L-22 (new at C, 3.10's shape). The token body is read with HasMember before
  IsObject and GetString before IsString (IGDBScraper.cpp:155-157,
  HfsDBScraper.cpp:202-204). A body of [] or {"access_token": 5} (a captive
  portal, a proxy's error, an API change) must leave no token and violate
  nothing. At the pin it violates rapidjson's preconditions -- FAIL; a number
  read as a string is a wild pointer in the shipped build.
--control returns true from the two process() exits and checks IsObject and
IsString first in both token reads. --plain builds without the sanitizers.
--hfs-only runs HfsDB's token reads alone (S3, EP-10: measured apart from IGDB's).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

ig = Path(sys.argv[1]).read_text()
hf = Path(sys.argv[2]).read_text()
rj = sys.argv[3]
proc = function(ig, r"^bool IGDBRequest::process\(const std::string& response, std::vector<ScraperSearchResult>& results\)", "3.16")
igt = function(ig, r"^bool IGDBScraper::ensureToken\(\)", "3.16")
hft = function(hf, r"^bool HfsDBScraper::ensureToken\(\)", "3.16")
if "--control" in sys.argv:
    a = "\t\tsetError(err);\n\t\tLOG(LogError) << err;\n\t\treturn false;"
    b = "\t\tLOG(LogWarning) << warn;\n\t\treturn false;"
    assert a in proc and b in proc
    proc = proc.replace(a, "\t\tsetError(err);\n\t\tLOG(LogError) << err;\n\t\treturn true;").replace(b, "\t\tLOG(LogWarning) << warn;\n\t\treturn true;")
    for key, src in (("access_token", "igt"), ("token", "hft")):
        old = 'if (!doc.HasParseError() && doc.HasMember("%s"))' % key
        new = 'if (!doc.HasParseError() && doc.IsObject() && doc.HasMember("%s") && doc["%s"].IsString())' % (key, key)
        if src == "igt":
            assert old in igt
            igt = igt.replace(old, new)
        else:
            assert old in hft
            hft = hft.replace(old, new)
EXTRACTS = [v for k, v in list(globals().items()) if isinstance(v, str) and k in ('fn', 'proc', 'igt', 'hft', 'gs', 'gi', 'gi1', 'pg')]
SRCDIR = str(Path(sys.argv[1]).resolve().parent.parent)  # es-app/src, for scrapers/ScraperJson.h (S3, D-WORKFLOW-211)
harness = r'''
#include <cstdio>
#include <stdexcept>
#include <string>
#include <vector>
static int gViolations = 0;
#define RAPIDJSON_ASSERT(x) ((x) ? (void)0 : (void)(++gViolations))
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
''' + ('#include "scrapers/ScraperJson.h"\n' if 'ScraperJson' in ''.join(EXTRACTS) else '') + r'''
using namespace rapidjson;
struct NullLog { template<typename T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
struct ScraperSearchResult {};
static void processIgdbGame(const Value&, std::vector<ScraperSearchResult>& r, bool) { r.push_back({}); }
struct IGDBRequest { std::string err; bool errored = false; bool mIsArcade = false;
    void setError(const std::string& e) { err = e; errored = true; }
    bool process(const std::string& response, std::vector<ScraperSearchResult>& results); };
struct Settings { static Settings* getInstance() { static Settings s; return &s; } std::string getString(const std::string&) { return "set"; } };
namespace Utils { namespace Time { struct DateTime { static DateTime now() { return {}; } long elapsedSecondsSince(const DateTime&) { return 0; } }; }
}
// The build's macro, given a placeholder of the shape the code splits ("a:b").
#define HFS_DEV_LOGIN "a:b"
namespace httplib { namespace detail { std::string base64_encode(const std::string& s) { return s; } } }
struct HttpReqOptions { std::vector<std::string> customHeaders; std::string dataToPost; long timeout = 0, stallTimeout = 0; };
#ifndef SCRAPER_STALL_TIMEOUT
#define SCRAPER_STALL_TIMEOUT 30L
#define SCRAPER_TOKEN_TIMEOUT 30000L
#endif
static std::string gBody;
struct HttpReq { enum Status { REQ_IO_ERROR = 3, REQ_SUCCESS = 200 }; HttpReq(const std::string&, HttpReqOptions*) {} bool wait() { return true; } Status status() { return REQ_SUCCESS; } std::string getContent() { return gBody; } };
struct IGDBScraper { std::string mToken; Utils::Time::DateTime mTokenDate; bool mTokenUnreachable = false; bool ensureToken(); };
struct HfsDBScraper { std::string mToken; Utils::Time::DateTime mTokenDate; bool mTokenUnreachable = false; bool ensureToken(); };
''' + proc + "\n" + igt + "\n" + hft + r'''
static bool gHfsOnly = false;
int main(int argc, char**) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    gHfsOnly = argc > 1;
    int bad = 0;
    struct P { const char* what; const char* body; } ps[] = { {"an empty answer []", "[]"}, {"an object {}", "{}"}, {"not JSON", "<html>"}, {"one game", "[{}]"} };
    for (auto& p : ps) {
        IGDBRequest r; std::vector<ScraperSearchResult> res; gViolations = 0;
        bool ret = r.process(p.body, res);
        printf("3.16 process(%-20s) returns %d, error set %d, results %zu%s\n", p.what, ret, r.errored, res.size(), ret ? "" : "   (the contract: false only when rate-limited)");
        if (!ret) bad++;
    }
    struct T { const char* what; const char* body; } ts[] = { {"[]", "[]"}, {"access_token 5", "{\"access_token\":5,\"token\":5}"}, {"well formed", "{\"access_token\":\"a\",\"token\":\"a\"}"} };
    for (auto& t : ts) {
        gBody = t.body;
        bool ig = false; int iv = 0;
        if (!gHfsOnly) { IGDBScraper i; gViolations = 0; printf("L-22 IGDB  token body %-15s ... ", t.what); ig = i.ensureToken(); iv = gViolations;
            printf("token %d, preconditions violated %d\n", ig, iv); }
        HfsDBScraper h; gViolations = 0; printf("L-22 HfsDB token body %-15s ... ", t.what); bool hf = h.ensureToken(); int hv = gViolations;
        printf("token %d, preconditions violated %d\n", hf, hv);
        if (iv || hv) bad++;
    }
    if (bad) { printf("FAIL 3.16/L-22: %d case(s): a false the contract reserves for rate limits, or a token body read unchecked\n", bad); return 1; }
    return 0;
}
'''
run(harness, "l316", (() if "--plain" in sys.argv else ("-fsanitize=address,undefined",)) + ("-DNDEBUG", "-Wno-deprecated-declarations", "-I" + rj, "-I" + SRCDIR),
    ("hfs",) if "--hfs-only" in sys.argv else ())

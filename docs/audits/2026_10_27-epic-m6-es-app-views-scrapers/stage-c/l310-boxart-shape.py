"""3.10 (#679): TheGamesDB's response is read with HasMember before IsObject.

    python3 -I l310-boxart-shape.py <GamesDBJSONScraper.cpp> <rapidjson include dir> [--control]

TheGamesDBJSONRequest::process is extracted as written and compiled against the
recipe's rapidjson 1.1.0 (the tarball PKG_SHA256 names, its four patches
applied), with RAPIDJSON_ASSERT counting each violated precondition instead of
aborting. rapidjson's HasMember asserts IsObject(); the shipped build defines
NDEBUG (config/functions: the ndebug flag, on by default, and the ES recipe's
PKG_BUILD_FLAGS is "-gold"), so the assertion is compiled out there and
HasMember walks an array's elements, or a string's bytes, as if they were
members -- a read of memory the value does not own as members. A Debug build
aborts instead. Either way the response's shape must be checked before it is
read, and the parse-error path's `return true` (no results, no error a page
shows) is upstream's design, not this lead.
Responses fed, each a body a server or a proxy could send:
  "boxart": [], "boxart": [1,2], "data": [], a root array, a root string (S3), a well-formed body,
  and "boxart": "x" last (it ends the run at the pin).
Each must return with no precondition violated and no game processed. At the
pin the boxart cases violate HasMember's precondition at :605 -- FAIL; the
`doc["data"].HasMember("games")` read at :590 and the root's at :590/:598 have
the same shape and are counted too.
--control reorders each check to IsObject first, to show the case can pass.
--plain builds without the sanitizers, as the shipped binary is (-O0 still).
Reach: TheGamesDB is compiled only with GAMESDB_APIKEY (Scraper.cpp:29).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
rj = sys.argv[2]
fn = function(src, r"^bool TheGamesDBJSONRequest::process\(const std::string& response, std::vector<ScraperSearchResult>& results\)", "3.10")
if "--control" in sys.argv:
    for a, b in [
        ('if (!doc.HasMember("data") || !doc["data"].HasMember("games") || !doc["data"]["games"].IsArray())',
         'if (!doc.IsObject() || !doc.HasMember("data") || !doc["data"].IsObject() || !doc["data"].HasMember("games") || !doc["data"]["games"].IsArray())'),
        ('if (!doc.HasMember("include") || !doc["include"].HasMember("boxart"))',
         'if (!doc.HasMember("include") || !doc["include"].IsObject() || !doc["include"].HasMember("boxart"))'),
        ('if (!boxart.HasMember("base_url") || !boxart.HasMember("data") || !boxart.IsObject())',
         'if (!boxart.IsObject() || !boxart.HasMember("base_url") || !boxart.HasMember("data"))')]:
        assert a in fn, a
        fn = fn.replace(a, b)
EXTRACTS = [v for k, v in list(globals().items()) if isinstance(v, str) and k in ('fn', 'proc', 'igt', 'hft', 'gs', 'gi', 'gi1', 'pg')]
SRCDIR = str(Path(sys.argv[1]).resolve().parent.parent)  # es-app/src, for scrapers/ScraperJson.h (S3, D-WORKFLOW-211)
harness = r'''
#include <cstdio>
#include <sstream>
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
static int gProcessed = 0;
struct Res { void ensureResources() {} } resources;
struct TheGamesDBJSONRequest { std::string err; void setError(const std::string& e) { err = e; }
    bool process(const std::string& response, std::vector<ScraperSearchResult>& results); };
static void processGame(const Value&, const Value&, std::vector<ScraperSearchResult>&, const TheGamesDBJSONRequest&) { gProcessed++; }
''' + fn + r'''
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    const char* bodies[][2] = {
        {"boxart []", "{\"data\":{\"games\":[{\"id\":1}]},\"include\":{\"boxart\":[]}}"},
        {"boxart [1,2]", "{\"data\":{\"games\":[{\"id\":1}]},\"include\":{\"boxart\":[1,2]}}"},
        {"data []", "{\"data\":[],\"include\":{\"boxart\":{}}}"},
        {"root []", "[]"},
        {"root \"x\"", "\"x\""},
        {"well formed", "{\"data\":{\"games\":[{\"id\":1}]},\"include\":{\"boxart\":{\"base_url\":{},\"data\":{}}}}"},
        {"boxart \"x\"", "{\"data\":{\"games\":[{\"id\":1}]},\"include\":{\"boxart\":\"x\"}}"},
    };
    int bad = 0;
    for (auto& b : bodies) {
        gViolations = 0; gProcessed = 0;
        printf("%-14s ... ", b[0]);
        TheGamesDBJSONRequest r; std::vector<ScraperSearchResult> res;
        bool ret = r.process(b[1], res);
        printf("returns %d, preconditions violated %d, games processed %d\n", ret, gViolations, gProcessed);
        if (gViolations) bad++;
    }
    if (bad) { printf("FAIL 3.10: %d response shape(s) read with HasMember before IsObject\n", bad); return 1; }
    return 0;
}
'''
run(harness, "l310", (() if "--plain" in sys.argv else ("-fsanitize=address,undefined",)) + ("-DNDEBUG", "-I" + rj, "-I" + SRCDIR))

"""S3 (#679; #1260, PL-03, EP-14): TheGamesDB's images JSON and its media base
are read before their shape is checked.

    python3 -I s3-images.py <GamesDBJSONScraper.cpp> <rapidjson include dir> [--plain]

`processGame`, `getStringOrThrow` and both `getIntOrThrow` are extracted as
written from GamesDBJSONScraper.cpp's anonymous namespace, compiled against
the recipe's rapidjson 1.1.0 with NDEBUG (as the shipped build) and
RAPIDJSON_ASSERT counting each violated precondition. The game and the
boxart are well formed; the case varies the dependency's images body
(`req.getDependencyResponse(id)`, `:458`) and the boxart's `base_url` (`:415`,
the floor's 3.8). Each must be refused with no precondition violated: a
logged skip or a thrown runtime_error the caller's catch takes (`:622-626`),
never a read. At the pin: violations, and the shapes that read a number or
an array as a string are wild reads.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
rj = sys.argv[2]
gs = function(src, r"^\tstd::string getStringOrThrow\(const Value& v, const std::string& key\)", "S3")
gi = function(src, r"^\tint getIntOrThrow\(const Value& v, const std::string& key\)", "S3")
gi1 = function(src, r"^\tint getIntOrThrow\(const Value& v\)\n", "S3")
pg = function(src, r"^\tvoid processGame\(const Value& game, const Value& boxart, std::vector<ScraperSearchResult>& results, const TheGamesDBJSONRequest& req\)", "S3")
EXTRACTS = [v for k, v in list(globals().items()) if isinstance(v, str) and k in ('fn', 'proc', 'igt', 'hft', 'gs', 'gi', 'gi1', 'pg')]
SRCDIR = str(Path(sys.argv[1]).resolve().parent.parent)  # es-app/src, for scrapers/ScraperJson.h (S3, D-WORKFLOW-211)
harness = r'''
#include <cstdio>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
static int gViolations = 0;
#define RAPIDJSON_ASSERT(x) ((x) ? (void)0 : (void)(++gViolations))
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
''' + ('#include "scrapers/ScraperJson.h"\n' if 'ScraperJson' in ''.join(EXTRACTS) else '') + r'''
using namespace rapidjson;
enum class MetaDataId { Name, Desc, ReleaseDate, Developer, Publisher, Genre, Players, Rating, Image, Thumbnail, Marquee, TitleShot, FanArt, BoxBack };
struct MDL { std::map<MetaDataId, std::string> m; void set(MetaDataId k, const std::string& v) { m[k] = v; } template<class T> void set(MetaDataId k, const T&) { m[k] = "x"; } std::string get(MetaDataId k) { return m[k]; } };
struct ScraperSearchItem { std::string url; ScraperSearchItem(const std::string& u = "") : url(u) {} };
struct ScraperSearchResult { std::string scraper; MDL mdl; std::map<MetaDataId, ScraperSearchItem> urls; ScraperSearchResult(const std::string& s) : scraper(s) {} };
struct Settings { static Settings* getInstance() { static Settings s; return &s; } std::string getString(const std::string&) { return "box-2D"; } bool getBool(const std::string&) { return true; } };
namespace Utils { namespace Time { struct DateTime { DateTime(long) {} }; long stringToTime(const std::string&, const std::string&) { return 0; } } }
namespace Genres { void convertGenreToGenreIds(MDL*) {} }
static std::string gImages;
struct TheGamesDBJSONRequest { std::string getDependencyResponse(const std::string&) const { return gImages; } };
static std::string getDeveloperString(const Value&) { return ""; }
static std::string getPublisherString(const Value&) { return ""; }
static std::string getGenreString(const Value&) { return ""; }
static std::string getBoxartImage(const Value&) { return ""; }
static std::string findMedia(const std::map<std::string, std::string>& m, const std::string& k) { auto it = m.find(k); return it == m.end() ? "" : it->second; }
namespace {
''' + gs + "\n" + gi + "\n" + gi1 + "\n" + pg + r'''
}
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    Document game; game.Parse("{\"id\":1,\"game_title\":\"Alpha\"}");
    struct C { const char* what; const char* boxart; const char* images; } cases[] = {
        {"well formed", "{\"base_url\":{\"thumb\":\"t/\",\"large\":\"l/\"},\"data\":{}}", "{\"data\":{\"base_url\":{\"medium\":\"m/\",\"large\":\"l/\"},\"images\":{\"1\":[{\"type\":\"fanart\",\"filename\":\"f.jpg\"}]}}}"},
        {"images: root a string", "{\"base_url\":{\"thumb\":\"t/\",\"large\":\"l/\"},\"data\":{}}", "\"x\""},
        {"images: data a number", "{\"base_url\":{\"thumb\":\"t/\",\"large\":\"l/\"},\"data\":{}}", "{\"data\":5}"},
        {"images: base_url a string", "{\"base_url\":{\"thumb\":\"t/\",\"large\":\"l/\"},\"data\":{}}", "{\"data\":{\"base_url\":\"x\"}}"},
        {"images: images a string", "{\"base_url\":{\"thumb\":\"t/\",\"large\":\"l/\"},\"data\":{}}", "{\"data\":{\"images\":\"x\"}}"},
        {"images: an element's type a number", "{\"base_url\":{\"thumb\":\"t/\",\"large\":\"l/\"},\"data\":{}}", "{\"data\":{\"images\":{\"1\":[{\"type\":5,\"filename\":\"f.jpg\"}]}}}"},
        {"images: medium a number", "{\"base_url\":{\"thumb\":\"t/\",\"large\":\"l/\"},\"data\":{}}", "{\"data\":{\"base_url\":{\"medium\":5}}}"},
        {"base_url a string (:415)", "{\"base_url\":\"x\",\"data\":{}}", ""},
    };
    int bad = 0;
    for (auto& c : cases) {
        Document boxart; boxart.Parse(c.boxart); gImages = c.images; gViolations = 0;
        printf("%-38s ... ", c.what);
        std::vector<ScraperSearchResult> results; std::string outcome = "returned";
        try { processGame(game, boxart, results, TheGamesDBJSONRequest()); }
        catch (std::runtime_error& e) { outcome = "threw (the caller's catch takes it)"; }
        printf("%s, results %zu, preconditions violated %d\n", outcome.c_str(), results.size(), gViolations);
        if (gViolations) bad++;
    }
    if (bad) { printf("FAIL S3: %d shape(s) read before they were checked\n", bad); return 1; }
    return 0;
}
'''
run(harness, "s3img", (() if "--plain" in sys.argv else ("-fsanitize=address,undefined",)) + ("-DNDEBUG", "-Wno-deprecated-declarations", "-I" + rj, "-I" + SRCDIR))

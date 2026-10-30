"""S3 (#680; #1274 PL-04, #1292 PL-18's 3.5, #1291 PL-13's stored key): three tables, extracted as written.

    python3 -I s3-tables.py <Genres.cpp> <MetaData.cpp> <FileFilterIndex.cpp> [case ...]

  genre   Genres::fromGenreName over its two maps (doubled: a whole name
          "Shooter" and a parent "Action"), under ASan: "Foo / Shooter"
          returns Shooter's entry (at the pin :305 returns through the
          whole name's end iterator)
  import  MetaDataList::importScrappedMetadata over a MetaDataList double
          (the declarations of the fields it reaches, get and set by key):
          a source with no developer, publisher, genre, players or release
          date leaves those fields as they were (at the pin :568 writes ""
          over each)
  xcc0    CollectionFilter::load over a .xcc holding <ratings>0 STARS</ratings>:
          the selection reads as 1 STARS (ruling 3: read both; at the pin
          it reads 0 STARS, a key no positive rating has after the fix)
"""
import re
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

gen, md, ffi = (Path(p).read_text() for p in sys.argv[1:4])
cases = sys.argv[4:] or ["genre", "import", "xcc0"]
fgn = function(gen, r"^GameGenre\* Genres::fromGenreName\(const std::string& name\)", "S3")
imp = function(md, r"^void MetaDataList::importScrappedMetadata\(const MetaDataList& source\)", "S3")
load = function(ffi, r"^bool CollectionFilter::load\(const std::string file\)", "S3")
sets = sorted(set(re.findall(r"\b(\w+IndexFilteredKeys)\b", load)))
harness = r'''
#define PUGIXML_HEADER_ONLY
#include <pugixml/src/pugixml.hpp>
#include <cstdio>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <sys/stat.h>
#define WINSTRINGW(x) (x)
struct NullLog { template<class T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
namespace Utils {
  namespace String { bool startsWith(const std::string& s, const std::string& p) { return s.rfind(p, 0) == 0; }
    std::string toUpper(std::string s) { for (auto& c : s) c = toupper(c); return s; }
    std::string trim(const std::string& s) { auto b = s.find_first_not_of(" \t"); if (b == std::string::npos) return ""; return s.substr(b, s.find_last_not_of(" \t") - b + 1); }
    std::vector<std::string> splitAny(const std::string& s, const std::string& seps, bool removeEmpty = false) { std::vector<std::string> o; std::string cur;
        for (char c : s) { if (seps.find(c) != std::string::npos) { if (!removeEmpty || !cur.empty()) o.push_back(cur); cur.clear(); } else cur += c; } if (!removeEmpty || !cur.empty()) o.push_back(cur); return o; } }
  namespace FileSystem { bool exists(const std::string& p, bool = true) { struct stat st; return ::stat(p.c_str(), &st) == 0; }
    std::string getStem(const std::string& p) { return p; } }
}
struct GameGenre { int id; std::string name; };
struct Genres { static std::map<int, GameGenre*> mGenres; static std::map<std::string, int> mAllGenresNames; static GameGenre* fromGenreName(const std::string& name); };
std::map<int, GameGenre*> Genres::mGenres; std::map<std::string, int> Genres::mAllGenresNames;
''' + fgn + r'''
enum MetaDataId { Name, Desc, Image, Thumbnail, Marquee, Video, FanArt, TitleShot, BoxBack, Map, Manual, Cartridge, Rating, ReleaseDate, Developer, Publisher, Genre, Players,
    Favorite, Hidden, Emulator, Core, KidGame, Tags, Region, Language, ScraperId, MetaDataIdCount };
enum MetaDataType { MD_STRING, MD_PATH, MD_BOOL };
struct MetaDataDecl { MetaDataId id; std::string key; MetaDataType type; std::string defaultValue; bool isStatistic; };
namespace MetaDataImportType { enum Types { IMAGE = 1, THUMB = 2, MARQUEE = 4, VIDEO = 8, FANART = 16, BOXBACK = 32, TITLESHOT = 64, MAP = 128, MANUAL = 256, CARTRIDGE = 512, ALL = 1023 }; }
struct Settings { static Settings* getInstance() { static Settings s; return &s; } std::string getString(const std::string&) { return "ScreenScraper"; } bool getBool(const std::string&) { return true; } };
struct MetaDataList { std::map<int, std::string> v;
    static std::vector<MetaDataDecl> getMDD() { std::vector<MetaDataDecl> d; const char* keys[] = {"name","desc","image","thumbnail","marquee","video","fanart","titleshot","boxback","map","manual","cartridge","rating","releasedate","developer","publisher","genre","players","favorite","hidden","emulator","core","kidgame","tags","region","lang","scraperid"};
        for (int i = 0; i < MetaDataIdCount; i++) d.push_back({ (MetaDataId)i, keys[i], i >= Image && i <= Cartridge ? MD_PATH : MD_STRING, "", false }); return d; }
    std::string get(MetaDataId id) const { auto it = v.find(id); return it == v.end() ? "" : it->second; }
    float getFloat(MetaDataId id) const { auto s = get(id); return s.empty() ? 0.0f : std::stof(s); }
    void set(MetaDataId id, const std::string& x) { v[id] = x; } std::string getName() const { return get(Name); }
    void importScrappedMetadata(const MetaDataList& source); };
''' + imp + r'''
struct FilterDataDecl { bool* filteredByRef; std::set<std::string>* currentFilteredKeys; };
struct FileFilterIndex { std::map<int, FilterDataDecl> mFilterDecl; void clearAllFilters() {} };   // the filters' flags, set at load's end; empty here
struct CollectionFilter : FileFilterIndex { std::string mPath, mName, mTextFilter; std::set<std::string> mSystemFilter;
''' + "".join("    std::set<std::string> %s;\n" % k for k in sets) + r'''    bool load(const std::string file); };
''' + load + r'''
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0); std::string base = argv[1]; int bad = 0;
    for (int k = 2; k < argc; k++) {
        std::string c = argv[k];
        if (c == "genre") {
            GameGenre action{10, "Action"}, shooter{11, "Shooter"}; Genres::mGenres = { {10, &action}, {11, &shooter} };
            Genres::mAllGenresNames = { {"ACTION", 10}, {"SHOOTER", 11} };
            GameGenre* g = Genres::fromGenreName("Foo / Shooter");
            printf("genre: \"Foo / Shooter\" -> %s\n", g == &shooter ? "Shooter" : (g ? g->name.c_str() : "nothing"));
            if (g != &shooter) { printf("FAIL genre: a genre found by its part did not return that part (:305 reads through the end iterator)\n"); bad++; }
        } else if (c == "import") {
            MetaDataList game, source; MetaDataId ids[] = {Developer, Publisher, Genre, Players, ReleaseDate};
            for (auto id : ids) game.set(id, "the player's"); source.set(Desc, "a scraped description");
            game.importScrappedMetadata(source); int blanked = 0;
            for (auto id : ids) if (game.get(id).empty()) blanked++;
            printf("import: %d of 5 filled fields blanked by a scrape that returned nothing for them; desc %s\n", blanked, game.get(Desc).empty() ? "not imported" : "imported");
            if (blanked) { printf("FAIL import: a scrape that returned nothing for a field blanked the filled one (:568, 3.5)\n"); bad++; }
        } else if (c == "xcc0") {
            std::string p = base + "/t33dyn.xcc"; FILE* f = fopen(p.c_str(), "w"); fputs("<filter name=\"t33dyn\"><ratings>0 STARS</ratings></filter>\n", f); fclose(f);
            CollectionFilter cf; cf.load(p); bool one = cf.ratingsIndexFilteredKeys.count("1 STARS") && !cf.ratingsIndexFilteredKeys.count("0 STARS");
            printf("xcc0: a stored 0 STARS loads as %s\n", cf.ratingsIndexFilteredKeys.count("0 STARS") ? "0 STARS" : (one ? "1 STARS" : "nothing"));
            if (!one) { printf("FAIL xcc0: a stored 0 STARS selection is not read as 1 STARS (ruling 3: read both)\n"); bad++; }
        }
    }
    if (bad) { printf("FAIL S3: %d case(s)\n", bad); return 1; }
    return 0;
}
'''
import os
d = tempfile.mkdtemp(prefix="s3-data-", dir="/workspace/tmp/m6-t33/tmp")
run(harness, "s3t", ("-fsanitize=address,undefined", "-I" + os.environ["PUGIXML_INCLUDE_DIR"]), args=(d, *cases))

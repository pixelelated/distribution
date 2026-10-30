"""S1b (#680; #1271 under D-CLOUD-187, EP-36): l313's merge extension.

    python3 -I l313-gamelist-merge.py <Gamelist.cpp> <MetaData.cpp> <MetaData.h> <pugixml root> [case ...] [--entries N]

updateGamelist and addFileDataNode (Gamelist.cpp), MetaDataList's set,
appendToXML, wasChanged, resetChangedFlag and, when the file has them,
overlayXML (MetaData.cpp) and the header's setDirty, all extracted as
written, over a declaration table of five fields (name, desc, image,
favorite, genreids) and doubles for paths and the cache (S1a's shape). The
game list is read uncached (S1a). The cases:
  same     a description and a picture written into Alpha's node after
           startup survive a save of Alpha's favourite (EP-36)
  desc     a description changed this session wins over the file's, and
           the file's picture stays
  default  a favourite set back to its default this session is removed
           from the node, and the file's description stays
  whole    a node marked dirty whole (setDirty: a recovery record) is
           rebuilt from memory, as at the pin (a control: PASS before and after)
  cost     --entries N: the save of one dirty game in a list of N, timed
The first three FAIL at S1a's commit (the node is rebuilt from memory).
"""
import re
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

gl, md, mdh, pugi = sys.argv[1:5]
rest = sys.argv[5:]
n_entries = "0"
if "--entries" in rest:
    i = rest.index("--entries"); n_entries = rest[i + 1]; rest = rest[:i] + rest[i + 2:]
cases = rest or ["same", "desc", "default", "whole"]
g = Path(gl).read_text(); m = Path(md).read_text(); h = Path(mdh).read_text()
helper = re.search(r"^static bool writeXmlDocument\(.*?^\}\n", g, re.S | re.M)
upd = function(g, r"^void updateGamelist\(SystemData\* system\)", "S1b")
afd = function(g, r"^bool addFileDataNode\(pugi::xml_node& parent, FileData\* file, const char\* tag, SystemData\* system, bool fullPaths = false\)", "S1b")
mset = function(m, r"^void MetaDataList::set\(MetaDataId id, const std::string& value\)", "S1b")
app = function(m, r"^void MetaDataList::appendToXML\(", "S1b")
wch = function(m, r"^bool MetaDataList::wasChanged\(\) const", "S1b")
rcf = function(m, r"^void MetaDataList::resetChangedFlag\(\)", "S1b")
ovl = re.search(r"^bool MetaDataList::overlayXML\(", m, re.M)
ovl = function(m, r"^bool MetaDataList::overlayXML\(", "S1b") if ovl else ""
asd = re.search(r"^void MetaDataList::appendScrapeDates\(", m, re.M)
asd = function(m, r"^void MetaDataList::appendScrapeDates\(", "S1b") if asd else ""
sd = re.search(r"const void setDirty\(\)\s*(\{.*?\n\t\})", h, re.S).group(1)
TYPES = r'''
struct FileData { std::string path; SystemData* sys; MetaDataList md; FileType type = GAME;
    SystemData* getSystem() { return sys; } MetaDataList& getMetadata() { return md; } std::string getPath() { return path; } FileType getType() { return type; }
    std::string getDisplayName() { auto f = path.substr(path.rfind('/') + 1); return f.substr(0, f.rfind('.')); } };
struct FolderData { std::vector<FileData*> files; std::vector<FileData*> getFilesRecursive(int, bool = false, void* = nullptr, bool = false) { return files; } };
struct SystemData { std::string dir; FolderData root; bool isGameSystem() { return true; } bool isCollection() { return false; } bool isHidden() { return false; }
    FolderData* getRootFolder() { return &root; } std::string getName() { return "gb"; } std::string getStartPath() { return dir; }
    std::string getGamelistPath(bool) { return dir + "/gamelist.xml"; } };
'''
harness = r'''
#define PUGIXML_HEADER_ONLY
#include <pugixml/src/pugixml.hpp>
#include <bitset>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <map>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>
#include <sys/stat.h>
#include <unistd.h>
#define WINSTRINGW(x) (x)
struct NullLog { template<class T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
enum FileType { GAME = 1, FOLDER = 2 };
enum MetaDataId { Name = 0, Desc = 1, Image = 2, Favorite = 3, GenreIds = 4, MetaDataIdCount };
enum MetaDataType { MD_STRING, MD_PATH, MD_BOOL };
struct MetaDataDecl { MetaDataId id; std::string key; MetaDataType type; std::string defaultValue; bool isStatistic; bool isAttribute; };
static MetaDataType gTypes[MetaDataIdCount] = { MD_STRING, MD_STRING, MD_PATH, MD_BOOL, MD_STRING };
static MetaDataType* mGameTypeMap = gTypes;
static std::map<std::string, int> KnowScrapersIds = { {"ScreenScraper", 0} };
namespace Utils {
  namespace Time { struct DateTime { std::string getIsoString() const { return "20261030T000000"; } }; }
  namespace String { std::string trim(const std::string& s) { auto b = s.find_first_not_of(" \t\r\n"); if (b == std::string::npos) return ""; return s.substr(b, s.find_last_not_of(" \t\r\n") - b + 1); } }
  namespace FileSystem {
    static std::map<std::string, bool> gCache;
    bool exists(const std::string& p, bool cache = true) { if (cache) { auto it = gCache.find(p); if (it != gCache.end()) return it->second; }
        struct stat st; bool r = ::stat(p.c_str(), &st) == 0; if (cache) gCache[p] = r; return r; }
    struct FileSystemCache { static void reset(const std::string& p) { gCache.erase(p); } };
    std::string getCanonicalPath(const std::string& p) { return p; }
    std::string getParent(const std::string& p) { return p.substr(0, p.rfind('/')); }
    bool createDirectory(const std::string&) { return true; }
    std::string resolveRelativePath(const std::string& p, const std::string& rel, bool) { return p.rfind("./", 0) == 0 ? rel + "/" + p.substr(2) : p; }
    std::string createRelativePath(const std::string& p, const std::string& rel, bool) { return p.rfind(rel + "/", 0) == 0 ? "./" + p.substr(rel.size() + 1) : p; }
  }
  namespace AtomicFile { bool writeText(const std::string& p, const std::string& t, int = -1) {
    std::string tmp = p + ".tmp.t33"; { std::ofstream o(tmp, std::ios::binary); o << t; } return std::rename(tmp.c_str(), p.c_str()) == 0; } }
}
struct Settings { static bool IgnoreGamelist() { return false; } static bool HiddenSystemsShowGames() { return true; } };
struct SystemData;
struct MetaDataList {
    std::map<int, Utils::Time::DateTime> mScrapeDates;
    std::string mName; bool mWasChanged = false; SystemData* mRelativeTo = nullptr;
    int8_t mIndices[MetaDataIdCount]; std::vector<std::string> mValues;
    std::vector<std::tuple<std::string, std::string, bool>> mUnKnownElements;
    std::bitset<MetaDataIdCount> mChangedFields; bool mWholeNode = false; bool mScrapeDatesChanged = false;   // the fix's members; unused at S1a
    MetaDataList() { memset(mIndices, -1, sizeof(mIndices)); }
    static const std::vector<MetaDataDecl>& getMDD() { static std::vector<MetaDataDecl> d = {
        {Name, "name", MD_STRING, "", false, false}, {Desc, "desc", MD_STRING, "", false, false}, {Image, "image", MD_PATH, "", false, false},
        {Favorite, "favorite", MD_BOOL, "false", false, false}, {GenreIds, "genreids", MD_STRING, "", false, false} }; return d; }
    void set(MetaDataId id, const std::string& value);
    void appendToXML(pugi::xml_node& parent, bool ignoreDefaults, const std::string& relativeTo, bool fullPaths = false) const;
    bool overlayXML(pugi::xml_node& node, bool ignoreDefaults, const std::string& relativeTo, bool fullPaths = false) const;
    void appendScrapeDates(pugi::xml_node& parent) const;
    bool wasChanged() const; void resetChangedFlag();
    const void setDirty() ''' + sd + r'''
};
''' + TYPES + mset + "\n" + app + "\n" + wch + "\n" + rcf + "\n" + ovl + "\n" + asd + r'''
static void clearTemporaryGamelistRecovery(SystemData*) {}
''' + (helper.group(0) if helper else "") + "\n" + afd + "\n" + upd + r'''
static std::string readAll(const std::string& p) { std::ifstream i(p); std::stringstream s; s << i.rdbuf(); return s.str(); }
static bool has(const std::string& s, const std::string& x) { return s.find(x) != std::string::npos; }
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    std::string base = argv[1]; long entries = atol(argv[2]); int bad = 0;
    auto setup = [&](const std::string& name, SystemData& sys, FileData& a, const std::string& alphaNode) {
        sys.dir = base + "/" + name; ::mkdir(sys.dir.c_str(), 0755); a.path = sys.dir + "/Alpha.gb"; a.sys = &sys; sys.root.files = {&a};
        a.md.mRelativeTo = &sys; a.md.mName = "Alpha"; a.md.resetChangedFlag();
        std::string gl = sys.dir + "/gamelist.xml"; Utils::FileSystem::exists(gl);   // the session's first look: absent
        std::ofstream(gl) << "<?xml version=\"1.0\"?>\n<gameList>\n" << alphaNode << "\t<game>\n\t\t<path>./Bravo.gb</path>\n\t\t<desc>bravo's</desc>\n\t</game>\n</gameList>\n";
        return gl; };
    for (int k = 3; k < argc; k++) {
        std::string c = argv[k]; SystemData sys; FileData a;
        if (c == "same") {
            auto gl = setup(c, sys, a, "\t<game>\n\t\t<path>./Alpha.gb</path>\n\t\t<name>Alpha</name>\n\t\t<desc>restored</desc>\n\t\t<image>./images/a.png</image>\n\t</game>\n");
            a.md.set(Favorite, "true"); updateGamelist(&sys); auto s = readAll(gl);
            bool ok = has(s, "<desc>restored</desc>") && has(s, "a.png") && has(s, "<favorite>true</favorite>") && has(s, "bravo's");
            printf("same: desc %s, image %s, favorite %s, Bravo %s\n", has(s, "<desc>restored</desc>") ? "kept" : "LOST", has(s, "a.png") ? "kept" : "LOST", has(s, "<favorite>true</favorite>") ? "written" : "MISSING", has(s, "bravo's") ? "kept" : "LOST");
            if (!ok) { printf("FAIL same: the dirty game's restored fields were lost by the save (EP-36)\n"); bad++; }
        } else if (c == "desc") {
            auto gl = setup(c, sys, a, "\t<game>\n\t\t<path>./Alpha.gb</path>\n\t\t<name>Alpha</name>\n\t\t<desc>the file's</desc>\n\t\t<image>./images/a.png</image>\n\t</game>\n");
            a.md.set(Desc, "the session's"); updateGamelist(&sys); auto s = readAll(gl);
            bool ok = has(s, "<desc>the session's</desc>") && !has(s, "the file's") && has(s, "a.png");
            printf("desc: desc %s, image %s\n", has(s, "the session's") ? "the session's" : (has(s, "the file's") ? "the file's" : "none"), has(s, "a.png") ? "kept" : "LOST");
            if (!ok) { printf("FAIL desc: a field changed this session did not win, or the file's picture was lost\n"); bad++; }
        } else if (c == "default") {
            auto gl = setup(c, sys, a, "\t<game>\n\t\t<path>./Alpha.gb</path>\n\t\t<name>Alpha</name>\n\t\t<desc>restored</desc>\n\t\t<favorite>true</favorite>\n\t</game>\n");
            a.md.set(Favorite, "true"); a.md.resetChangedFlag(); a.md.set(Favorite, "false"); updateGamelist(&sys); auto s = readAll(gl);
            bool ok = !has(s, "<favorite>") && has(s, "<desc>restored</desc>");
            printf("default: favorite %s, desc %s\n", has(s, "<favorite>") ? "still written" : "removed", has(s, "<desc>restored</desc>") ? "kept" : "LOST");
            if (!ok) { printf("FAIL default: a field set back to its default was not removed, or the file's description was lost\n"); bad++; }
        } else if (c == "whole") {
            auto gl = setup(c, sys, a, "\t<game>\n\t\t<path>./Alpha.gb</path>\n\t\t<name>Alpha</name>\n\t\t<desc>old</desc>\n\t</game>\n");
            a.md.set(Favorite, "true"); a.md.setDirty(); updateGamelist(&sys); auto s = readAll(gl);
            bool ok = !has(s, "<desc>old</desc>") && has(s, "<favorite>true</favorite>");
            printf("whole: a node marked dirty whole is %s\n", ok ? "rebuilt from memory (the pin's rule for setDirty)" : "not rebuilt");
            if (!ok) { printf("FAIL whole: setDirty's node was not rebuilt whole\n"); bad++; }
        } else if (c == "cost") {
            sys.dir = base + "/cost"; ::mkdir(sys.dir.c_str(), 0755); a.path = sys.dir + "/G0.gb"; a.sys = &sys; sys.root.files = {&a}; a.md.mRelativeTo = &sys; a.md.mName = "G0";
            std::string gl = sys.dir + "/gamelist.xml"; { std::ofstream o(gl); o << "<?xml version=\"1.0\"?>\n<gameList>\n";
                for (long i = 0; i < entries; i++) o << "\t<game>\n\t\t<path>./G" << i << ".gb</path>\n\t\t<name>G" << i << "</name>\n\t\t<desc>a description of game " << i << " long enough to be a description</desc>\n\t\t<image>./images/G" << i << ".png</image>\n\t</game>\n";
                o << "</gameList>\n"; }
            a.md.set(Favorite, "true"); auto t0 = std::chrono::steady_clock::now(); updateGamelist(&sys); auto t1 = std::chrono::steady_clock::now();
            printf("cost: one dirty game in a list of %ld: %.1f ms (read, parse, %s, write, rename)\n", entries, std::chrono::duration<double, std::milli>(t1 - t0).count(), %s);
        }
    }
    if (bad) { printf("FAIL S1b: %d case(s)\n", bad); return 1; }
    return 0;
}
'''.replace('%s);\n        }\n    }', '"%s");\n        }\n    }' % ("overlay" if ovl else "rebuild"), 1)
d = tempfile.mkdtemp(prefix="s1b-data-", dir="/workspace/tmp/m6-t33/tmp")
flags = ("-O2",) if "cost" in cases else ("-fsanitize=address,undefined",)
run(harness, "s1b", flags + ("-I" + pugi,), args=(d, n_entries, *cases))

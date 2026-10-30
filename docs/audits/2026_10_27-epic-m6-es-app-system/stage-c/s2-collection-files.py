"""S2 (#680; #1275 PL-05, #1287 PL-22): the collections' files and the filter index.

    python3 -I s2-collection-files.py <CollectionSystemManager.cpp> <FileFilterIndex.cpp> [case ...]

saveCustomCollection, getCustomCollectionConfigPath, getCollectionsFolder,
getFilteredCollectionPath and deleteCustomCollection (CollectionSystemManager.cpp),
and CollectionFilter::save, FileFilterIndex::resetIndex and clearIndex
(FileFilterIndex.cpp), extracted as written, over doubles: the file cache
(S1a's shape), a std::ofstream and a pugixml save_file that can be killed
after N bytes, and AtomicFile::writeText as a temporary and a rename (the
contract es-file-tests proves). The cases:
  cfgkill  a custom collection's list killed mid-write leaves the previous list whole
  xcckill  a dynamic collection's filter killed mid-write leaves the previous filter whole
  delete   a filter saved this session after the session remembered its
           absence is found and removed by deleteCustomCollection
  reset    resetIndex leaves no stale key in any facet's map (EP-44); the
           TRUE/FALSE keys it seeds again are its own
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

csm = Path(sys.argv[1]).read_text(); ffi = Path(sys.argv[2]).read_text()
cases = sys.argv[3:] or ["cfgkill", "xcckill", "delete", "reset"]
fns_c = [function(csm, r"^std::string getCollectionsFolder\(\)", "S2"),
         function(csm, r"^std::string getCustomCollectionConfigPath\(const std::string& collectionName\)", "S2"),
         function(csm, r"^std::string getFilteredCollectionPath\(const std::string& collectionName\)", "S2"),
         function(csm, r"^void CollectionSystemManager::saveCustomCollection\(SystemData\* sys\)", "S2"),
         function(csm, r"^bool CollectionSystemManager::deleteCustomCollection\(CollectionSystemData\* data\)", "S2")]
save = function(ffi, r"^bool CollectionFilter::save\(\)", "S2")
reset = function(ffi, r"^void FileFilterIndex::resetIndex\(\)", "S2")
cl_m = re.search(r"^void FileFilterIndex::clearIndex\((.*?)\)", ffi, re.M)
clear = function(ffi, r"^void FileFilterIndex::clearIndex\(", "S2")
filtered = sorted(set(re.findall(r"\b(\w+IndexFilteredKeys)\b", save)))
allkeys = sorted(set(re.findall(r"\b(\w+IndexAllKeys)\b", reset)))
body_c = "\n".join(fns_c).replace("std::ofstream configFile;", "T33Ofstream configFile;")
save = save.replace("doc.save_file(", "t33SaveFile(doc, ")
harness = r'''
#define PUGIXML_HEADER_ONLY
#include <pugixml/src/pugixml.hpp>
#include <algorithm>
#include <cstdio>
#include <fstream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <sys/stat.h>
#include <unistd.h>
#define WINSTRINGW(x) (x)
struct NullLog { template<class T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
static long gKillAfter = -1;
struct Killed : std::runtime_error { Killed() : std::runtime_error("killed") {} };
static void writeMaybeKilled(const std::string& p, const std::string& t) { std::ofstream o(p, std::ios::binary | std::ios::trunc);
    if (gKillAfter >= 0 && (long)t.size() > gKillAfter) { o << t.substr(0, gKillAfter); o.close(); throw Killed(); } o << t; }
static bool t33SaveFile(const pugi::xml_document& d, const std::string& p) { std::ostringstream s; d.save(s); writeMaybeKilled(p, s.str()); return true; }
struct T33Ofstream { std::ofstream o; long n = 0;   // std::ofstream as the pin uses it, killable after gKillAfter bytes
    void open(const std::string& p) { o.open(p, std::ios::binary | std::ios::trunc); }
    template<class T> T33Ofstream& operator<<(const T& v) { std::ostringstream s; s << v; std::string t = s.str();
        if (gKillAfter >= 0 && n + (long)t.size() > gKillAfter) { o << t.substr(0, gKillAfter - n); o.close(); throw Killed(); } n += t.size(); o << t; return *this; }
    T33Ofstream& operator<<(std::ostream& (*)(std::ostream&)) { return *this << "\n"; }
    void close() { o.close(); } };
static std::map<std::string, bool> gCache;
namespace Utils {
  namespace String { std::string toUpper(std::string x) { for (auto& ch : x) ch = toupper(ch); return x; }
    std::vector<std::string> split(const std::string& s, char c, bool = false) { std::vector<std::string> o; std::string cur; for (char x : s) { if (x == c) { if (!cur.empty()) o.push_back(cur); cur.clear(); } else cur += x; } if (!cur.empty()) o.push_back(cur); return o; }
    std::string vectorToCommaString(const std::vector<std::string>& v) { std::string o; for (auto& x : v) o += (o.empty() ? "" : ",") + x; return o; } }
  namespace FileSystem {
    bool exists(const std::string& p, bool cache = true) { if (cache) { auto it = gCache.find(p); if (it != gCache.end()) return it->second; }
        struct stat st; bool r = ::stat(p.c_str(), &st) == 0; if (cache) gCache[p] = r; return r; }
    struct FileSystemCache { static void reset(const std::string& p) { gCache.erase(p); } };
    bool removeFile(const std::string& p) { gCache.erase(p); return ::unlink(p.c_str()) == 0; }
    std::string getGenericPath(const std::string& p) { return p; }
    std::string createRelativePath(const std::string& p, const std::string&, bool) { return p; }
  }
  namespace AtomicFile { bool writeText(const std::string& p, const std::string& t, int = -1) { std::string tmp = p + ".tmp.t33"; writeMaybeKilled(tmp, t); return ::rename(tmp.c_str(), p.c_str()) == 0; } }
}
namespace Genres { std::string genreStringFromIds(const std::vector<std::string>&) { return ""; } }
struct FileTag { std::string Name; static std::vector<FileTag> Values() { return { {"FINISHED"} }; } };
struct Paths { static std::string gHome; static std::string getUserEmulationStationPath() { return gHome; } static std::string getRootPath() { return gHome; } };
std::string Paths::gHome;
struct Settings { std::map<std::string, std::string> s; static Settings* getInstance() { static Settings x; return &x; }
    std::string getString(const std::string& k) { return s[k]; } void setString(const std::string& k, const std::string& v) { s[k] = v; } };
struct FileData { std::string key; std::string getKey() { return key; } };
struct FolderData { std::vector<FileData*> kids; std::vector<FileData*> getChildren() { return kids; } };
struct SystemData { std::string name; FolderData root; std::string getName() { return name; } FolderData* getRootFolder() { return &root; } };
struct FileFilterIndex {
    bool mUseRelevency = true; std::string mTextFilter;
''' + "".join("    std::map<std::string, int> %s;\n" % k for k in allkeys) + "".join("    std::vector<std::string> %s;\n" % k for k in filtered) + r'''
    void clearAllFilters() {}
    void manageIndexEntry(std::map<std::string, int>* index, const std::string& key, bool remove, bool = false) { if (!remove) (*index)[key]++; }   // seeds a facet; the test reads only the stale key
    void resetIndex(); void clearIndex(''' + cl_m.group(1) + r''');
};
struct CollectionFilter : FileFilterIndex { std::string mName, mPath; std::vector<std::string> mSystemFilter; bool save(); };
struct CollectionSystemData { SystemData* system = nullptr; FileFilterIndex* filteredIndex = nullptr; bool needsSave = true; };
struct CollectionSystemManager { std::map<std::string, CollectionSystemData> mCustomCollectionSystemsData;
    void saveCustomCollection(SystemData* sys); bool deleteCustomCollection(CollectionSystemData* data); };
''' + body_c + "\n" + save + "\n" + reset + "\n" + clear + r'''
static std::string readAll(const std::string& p) { std::ifstream i(p, std::ios::binary); std::stringstream s; s << i.rdbuf(); return s.str(); }
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0); std::string base = argv[1]; int bad = 0;
    for (int k = 2; k < argc; k++) {
        std::string c = argv[k]; Paths::gHome = base + "/" + c; ::mkdir(Paths::gHome.c_str(), 0755); ::mkdir((Paths::gHome + "/collections").c_str(), 0755);
        gCache.clear(); gKillAfter = -1; CollectionSystemManager m;
        if (c == "cfgkill") {
            SystemData sys{"t33"}; FileData a{"/roms/A"}, b{"/roms/B"}, cc{"/roms/C"}; sys.root.kids = {&a, &b, &cc};
            m.mCustomCollectionSystemsData["t33"] = CollectionSystemData{&sys, nullptr, true};
            std::string p = getCustomCollectionConfigPath("t33"); std::ofstream(p) << "/roms/A\n/roms/B\n"; gKillAfter = 10;
            try { m.saveCustomCollection(&sys); } catch (Killed&) {}
            bool whole = readAll(p) == "/roms/A\n/roms/B\n"; printf("cfgkill: the previous list %s\n", whole ? "whole" : "cut");
            if (!whole) { printf("FAIL cfgkill: a custom collection's list killed mid-write is left cut (D-CLOUD-078)\n"); bad++; }
        } else if (c == "xcckill") {
            CollectionFilter f; f.mName = "t33dyn"; f.mPath = getFilteredCollectionPath("t33dyn"); std::string before = "<filter name=\"t33dyn\"><genre>10</genre></filter>\n";
            std::ofstream(f.mPath) << before; gKillAfter = 10; try { f.save(); } catch (Killed&) {}
            bool whole = readAll(f.mPath) == before; printf("xcckill: the previous filter %s\n", whole ? "whole" : "cut");
            if (!whole) { printf("FAIL xcckill: a dynamic collection's filter killed mid-write is left cut; a cut .xcc empties the collection (EP-19)\n"); bad++; }
        } else if (c == "delete") {
            CollectionFilter f; f.mName = "t33dyn"; f.mPath = getFilteredCollectionPath("t33dyn");
            Utils::FileSystem::exists(f.mPath);   // the session's look at load (:963): absent
            f.save(); SystemData sys{"t33dyn"}; CollectionSystemData d{&sys, &f, false}; m.mCustomCollectionSystemsData["t33dyn"] = d;
            bool ok = m.deleteCustomCollection(&d); struct stat st; bool gone = ::stat(f.mPath.c_str(), &st) != 0;
            printf("delete: deleteCustomCollection returned %s, the .xcc %s\n", ok ? "true" : "false", gone ? "removed" : "still there");
            if (!ok || !gone) { printf("FAIL delete: a filter written this session was not found by the delete (the cache remembered its absence)\n"); bad++; }
        } else if (c == "reset") {
            FileFilterIndex x;
''' + "".join('            x.%s["k"] = 1;\n' % k for k in allkeys) + r'''
            x.resetIndex(); int left = 0;
''' + "".join("            left += (int)x.%s.count(\"k\");\n" % k for k in allkeys) + r'''
            printf("reset: %d facet map(s) cleared by resetIndex, %d key(s) left\n", %d, left);
            if (left) { printf("FAIL reset: resetIndex clears copies (clearIndex takes its map by value; EP-44)\n"); bad++; }
        }
    }
    if (bad) { printf("FAIL S2: %%d case(s)\n", bad); return 1; }
    return 0;
}
'''
harness = harness.replace('printf("reset: %d facet map(s) cleared by resetIndex, %d key(s) left\\n", %d, left);', 'printf("reset: %%d facet map(s) given to resetIndex, %%d stale key(s) left\\n", %d, left);' % len(allkeys)).replace('%%d', '%d')
import tempfile, os
d = tempfile.mkdtemp(prefix="s2-data-", dir="/workspace/tmp/m6-t33/tmp")
pugi = os.environ["PUGIXML_INCLUDE_DIR"]
run(harness, "s2f", ("-fsanitize=address,undefined", "-I" + pugi), args=(d, *cases))

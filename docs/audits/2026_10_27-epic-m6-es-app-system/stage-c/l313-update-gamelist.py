"""3.13 (#680, L-05): updateGamelist's read and write, extracted as written.

    python3 -I l313-update-gamelist.py <Gamelist.cpp> <pugixml include root> [--control]

updateGamelist (the pin's :374-481) over doubles for the system, its files
and recovery, with real pugixml (header-only) and a Utils::FileSystem::exists
double that remembers each answer, as es-core's cache does until a launch
(FileSystemUtil.cpp:345, T21's file). The scenario is the cloud's game
content restore (D-CLOUD-049): the system's gamelist.xml is absent when the
session first asks (the cache remembers the miss), a gamelist.xml with an
entry for Bravo then arrives from outside ES, Alpha is marked favourite, and
the save runs. Asserted:
- Bravo's entry survives the save (the read must see the file);
- the write replaces the file rather than truncating it in place (a new
  inode: temp-and-rename, D-CLOUD-078).
At the pin both fail: Bravo is lost, and the inode is the same. --control
applies the lane's proposed fix (`exists(xmlReadPath, false)`; the save to a
temp file and a rename) and must PASS. The guest's G-04 showed the first on
the image.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
pugi = sys.argv[2]
fn = function(src, r"^void updateGamelist\(SystemData\* system\)", "3.13")
# S1a (D-WORKFLOW-211): the fixed file's write helper, extracted when present.
helper = re.search(r"^static bool writeXmlDocument\(.*?^\}\n", src, re.S | re.M)
fn = (helper.group(0) + "\n" if helper else "") + fn
if "--control" in sys.argv and "Utils::FileSystem::exists(xmlReadPath)" not in fn:
    print("CANNOT: --control rewrites the pin's lines, which this file no longer has (S1a: the default run is the positive)")
    sys.exit(2)
if "--control" in sys.argv:
    fn = fn.replace("Utils::FileSystem::exists(xmlReadPath)", "Utils::FileSystem::exists(xmlReadPath, false)")
    fn = fn.replace("!doc.save_file(WINSTRINGW(xmlWritePath).c_str())", "!(doc.save_file((xmlWritePath + \".tmp\").c_str()) && std::rename((xmlWritePath + \".tmp\").c_str(), xmlWritePath.c_str()) == 0)")
harness = r'''
#define PUGIXML_HEADER_ONLY
#include <pugixml/src/pugixml.hpp>
#include <cstdio>
#include <fstream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
#include <sys/stat.h>
#include <unistd.h>
#define WINSTRINGW(x) (x)
struct NullLog { template<class T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
enum FileType { GAME = 1, FOLDER = 2 };
static std::map<std::string, bool> gCache;
namespace Utils { namespace FileSystem {
    bool exists(const std::string& p, bool cache = true) {
        if (cache) { auto it = gCache.find(p); if (it != gCache.end()) return it->second; }
        struct stat st; bool r = ::stat(p.c_str(), &st) == 0; if (cache) gCache[p] = r; return r; }
    std::string getCanonicalPath(const std::string& p) { return p; }
    std::string resolveRelativePath(const std::string& p, const std::string& rel, bool) { return p.rfind("./", 0) == 0 ? rel + "/" + p.substr(2) : p; }
    std::string getParent(const std::string& p) { return p.substr(0, p.rfind('/')); }
    bool createDirectory(const std::string&) { return true; }
    struct FileSystemCache { static void reset(const std::string& p) { gCache.erase(p); } };   // S1a, D-WORKFLOW-211
}
  namespace AtomicFile { bool writeText(const std::string& p, const std::string& t, int = -1) {   // S1a: temp and rename, as AtomicFileUtil.h:30-41
    std::string tmp = p + ".tmp.t33"; { std::ofstream o(tmp, std::ios::binary); o << t; } return std::rename(tmp.c_str(), p.c_str()) == 0; } }
}
struct Settings { static bool IgnoreGamelist() { return false; } static bool HiddenSystemsShowGames() { return true; } };
struct SystemData;
struct MD { bool changed = false; bool wasChanged() { return changed; } bool overlayXML(pugi::xml_node&, bool, const std::string&, bool = false) { return false; } };   // S1b (D-WORKFLOW-211): the rebuild path, as these cases assume
struct FileData { std::string path; SystemData* sys; MD md; FileType type = GAME;
    SystemData* getSystem() { return sys; } MD& getMetadata() { return md; } std::string getPath() { return path; } FileType getType() { return type; } };
struct FolderData { std::vector<FileData*> files; std::vector<FileData*> getFilesRecursive(int, bool, void*, bool) { return files; } };
struct SystemData { std::string dir; FolderData root;
    bool isGameSystem() { return true; } bool isCollection() { return false; } bool isHidden() { return false; }
    FolderData* getRootFolder() { return &root; } std::string getName() { return "gb"; }
    std::string getStartPath() { return dir; } std::string getGamelistPath(bool) { return dir + "/gamelist.xml"; } };
static void clearTemporaryGamelistRecovery(SystemData*) {}
static bool addFileDataNode(pugi::xml_node& parent, FileData* file, const char* tag, SystemData* system, bool = false) {
    pugi::xml_node n = parent.append_child(tag); n.append_child("path").text().set(("./" + file->path.substr(file->path.rfind('/') + 1)).c_str());
    n.append_child("favorite").text().set("true"); return true; }
''' + fn + r'''
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    std::string dir = argv[1];
    SystemData sys; sys.dir = dir;
    FileData alpha{dir + "/Alpha.gb", &sys}; sys.root.files = {&alpha};
    const std::string gl = dir + "/gamelist.xml";
    printf("startup: gamelist.xml %s (the session's first answer, remembered)\n", Utils::FileSystem::exists(gl) ? "present" : "absent");
    { std::ofstream o(gl); o << "<?xml version=\"1.0\"?>\n<gameList>\n\t<game>\n\t\t<path>./Bravo.gb</path>\n\t\t<desc>restored from the cloud</desc>\n\t</game>\n</gameList>\n"; }
    struct stat before; ::stat(gl.c_str(), &before);
    printf("outside ES: gamelist.xml written with Bravo's entry\n");
    alpha.md.changed = true;
    updateGamelist(&sys);
    std::stringstream ss; ss << std::ifstream(gl).rdbuf(); std::string after = ss.str();
    struct stat st; ::stat(gl.c_str(), &st);
    bool bravo = after.find("Bravo.gb") != std::string::npos, alphaIn = after.find("Alpha.gb") != std::string::npos;
    printf("after the save: Alpha %s, Bravo %s; inode %s\n", alphaIn ? "present" : "absent", bravo ? "present" : "absent", st.st_ino == before.st_ino ? "the same (written in place)" : "new (replaced)");
    int bad = 0;
    if (!bravo) { printf("FAIL 3.13: the entry that arrived from outside was lost by the save (L-05)\n"); bad++; }
    if (st.st_ino == before.st_ino) { printf("FAIL 3.13: gamelist.xml written in place, no temp-and-rename (D-CLOUD-078)\n"); bad++; }
    return bad ? 1 : 0;
}
'''
import tempfile
d = tempfile.mkdtemp(prefix="l313-data-", dir="/workspace/tmp/m6-t33/tmp")
run(harness, "l313", ("-fsanitize=address,undefined", "-I" + pugi), args=(d,))

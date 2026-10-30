"""S1 (#680; #1271 PL-01, #1285 PL-16's saveToXml): l313's extension, the game list's save end to end.

    python3 -I l313-gamelist-save.py <Gamelist.cpp> <pugixml include root> [case ...]

updateGamelist, packGamelist, cleanupGamelist, saveToXml and
clearTemporaryGamelistRecovery extracted as written, over real pugixml
(header-only) and doubles: a Utils::FileSystem whose exists remembers each
answer as es-core's cache does until a launch (FileSystemUtil.cpp:345) and
forgets a path on FileSystemCache::reset(path) (:348-350); a writer for
pugixml's save_file and for AtomicFile::writeText that can be killed after
half the bytes (a power loss mid-write). AtomicFile::writeText's double
writes a temporary and renames it, the contract es-file-tests proves of the
real one (AtomicFileUtil.h:30-41), so after the fix this harness proves the
call shape and es-file-tests the atomicity. The cases, each with what it
asserts (each FAILs at the pin):
  outside  a gamelist.xml written from outside after the session's first look survives a save (L-05, D-CLOUD-187)
  inode    the save replaces the file (a new inode), not truncates it (D-CLOUD-078)
  unparsed a gamelist.xml that does not parse is not written over (EP-1)
  recovery packGamelist, run before parseGamelist as SystemData.cpp:125-128 runs them, leaves the recovery folder (EP-2)
  media    a picture restored after the session remembered its absence keeps its reference through CLEAN GAMELISTS (3.15)
  record   saveToXml killed at its write leaves the previous recovery record (EP-3, #1285)
  kill     updateGamelist, packGamelist and cleanupGamelist killed mid-write leave the previous file whole
S1b's cases (same-game, ...) are added by S1b.
"""
import os
import re
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
pugi = sys.argv[2]
cases = sys.argv[3:] or ["outside", "inode", "unparsed", "recovery", "media", "record", "kill"]
fns = [function(src, r"^std::string getGamelistRecoveryPath\(SystemData\* system\)", "S1"),
       function(src, r"^void clearTemporaryGamelistRecovery\(SystemData\* system\)", "S1")]
helper = re.search(r"^static bool writeXmlDocument\(.*?^\}\n", src, re.S | re.M)
if helper:
    fns.append(helper.group(0))
fns += [function(src, r"^bool saveToXml\(FileData\* file, const std::string& fileName, bool fullPaths\)", "S1"),
        function(src, r"^void updateGamelist\(SystemData\* system\)", "S1"),
        function(src, r"^void packGamelist\(SystemData\* system\)", "S1"),
        function(src, r"^void cleanupGamelist\(SystemData\* system\)", "S1")]
body = "\n".join(fns).replace("doc.save_file(", "t33SaveFile(doc, ")
harness = r'''
#define PUGIXML_HEADER_ONLY
#include <pugixml/src/pugixml.hpp>
#include <cstdio>
#include <dirent.h>
#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include <sys/stat.h>
#include <unistd.h>
#define WINSTRINGW(x) (x)
struct NullLog { template<class T> NullLog& operator<<(const T& v) { std::ostringstream s; s << v; gLog += s.str(); return *this; } ~NullLog() { gLog += "\n"; } static std::string gLog; };
std::string NullLog::gLog;
#define LOG(x) NullLog()
enum FileType { GAME = 1, FOLDER = 2 };
enum class MetaDataId { Image, Thumbnail, Marquee, Video, FanArt, TitleShot, BoxBack, Map, Manual, Magazine, Cartridge, Wheel, BoxArt, Mix, Bezel };
enum MetaDataType { MD_STRING, MD_PATH };
struct MetaDataDecl { MetaDataId id; std::string key; MetaDataType type; };
namespace PlatformIds { enum PlatformId { IMAGEVIEWER }; }
static long gKillAfter = -1;   // bytes a writer writes before it dies; -1: never
struct Killed : std::runtime_error { Killed() : std::runtime_error("killed") {} };
static void writeMaybeKilled(const std::string& p, const std::string& text) {
    std::ofstream o(p, std::ios::binary | std::ios::trunc);
    if (gKillAfter >= 0) { o << text.substr(0, gKillAfter); o.close(); throw Killed(); }
    o << text; }
static bool t33SaveFile(const pugi::xml_document& d, const std::string& p) { std::ostringstream s; d.save(s); writeMaybeKilled(p, s.str()); return true; }
static std::map<std::string, bool> gCache;
namespace Utils {
  namespace String { std::string toLower(std::string s) { for (auto& c : s) c = tolower(c); return s; } }
  namespace FileSystem {
    bool exists(const std::string& p, bool cache = true) {
        if (cache) { auto it = gCache.find(p); if (it != gCache.end()) return it->second; }
        struct stat st; bool r = !p.empty() && ::stat(p.c_str(), &st) == 0; if (cache) gCache[p] = r; return r; }
    struct FileSystemCache { static void reset(const std::string& p) { gCache.erase(p); } static void reset() { gCache.clear(); } };
    bool isDirectory(const std::string& p) { struct stat st; return ::stat(p.c_str(), &st) == 0 && S_ISDIR(st.st_mode); }
    std::string getParent(const std::string& p) { auto i = p.rfind('/'); return i == std::string::npos ? "" : p.substr(0, i); }
    std::string getFileName(const std::string& p) { auto i = p.rfind('/'); return i == std::string::npos ? p : p.substr(i + 1); }
    std::string getExtension(const std::string& p) { auto f = getFileName(p); auto i = f.rfind('.'); return i == std::string::npos ? "" : f.substr(i); }
    std::string getGenericPath(const std::string& p) { return p; }
    std::string getCanonicalPath(const std::string& p) { return p; }
    std::string resolveRelativePath(const std::string& p, const std::string& rel, bool) { return p.rfind("./", 0) == 0 ? rel + "/" + p.substr(2) : p; }
    std::string createRelativePath(const std::string& p, const std::string& rel, bool) { return p.rfind(rel + "/", 0) == 0 ? "./" + p.substr(rel.size() + 1) : p; }
    bool createDirectory(const std::string& p) { if (p.empty() || isDirectory(p)) return true; createDirectory(getParent(p)); return ::mkdir(p.c_str(), 0755) == 0; }
    bool removeFile(const std::string& p) { gCache.erase(p); return ::unlink(p.c_str()) == 0; }
    bool copyFile(const std::string& a, const std::string& b) { std::ifstream i(a, std::ios::binary); if (!i) return false; std::ofstream o(b, std::ios::binary); o << i.rdbuf(); return true; }
    std::vector<std::string> getDirContent(const std::string& d, bool recursive) { std::vector<std::string> out; DIR* dir = opendir(d.c_str()); if (!dir) return out;
        while (auto e = readdir(dir)) { std::string n = e->d_name; if (n == "." || n == "..") continue; std::string p = d + "/" + n; out.push_back(p); if (recursive && isDirectory(p)) for (auto& q : getDirContent(p, true)) out.push_back(q); }
        closedir(dir); return out; }
    void deleteDirectoryFiles(const std::string& d, bool) { for (auto& p : getDirContent(d, true)) if (!isDirectory(p)) removeFile(p); }
  }
  namespace AtomicFile {
    bool writeText(const std::string& p, const std::string& text, int = -1) {
        std::string tmp = p + ".tmp.t33"; writeMaybeKilled(tmp, text); return ::rename(tmp.c_str(), p.c_str()) == 0; }
  }
}
struct Settings { static Settings* getInstance() { static Settings s; return &s; } bool getBool(const std::string&) { return true; }
    static bool IgnoreGamelist() { return false; } static bool HiddenSystemsShowGames() { return true; } };
struct Paths { static std::string gHome; static std::string getUserEmulationStationPath() { return gHome; } };
std::string Paths::gHome;
struct SystemData;
struct MD { bool changed = false; bool wasChanged() { return changed; } bool overlayXML(pugi::xml_node&, bool, const std::string&, bool = false) { return false; } };   // S1b (D-WORKFLOW-211): the rebuild path, as these cases assume
struct FileData { std::string path; SystemData* sys; MD md; FileType type = GAME;
    SystemData* getSystem() { return sys; } MD& getMetadata() { return md; } std::string getPath() { return path; } FileType getType() { return type; }
    std::string getDisplayName() { auto f = Utils::FileSystem::getFileName(path); return f.substr(0, f.rfind('.')); }
    FileData* getSourceFileData() { return this; } };
struct FolderData { std::vector<FileData*> files; std::vector<FileData*> getFilesRecursive(int, bool = false, void* = nullptr, bool = false) { return files; } };
struct SystemData { std::string dir; FolderData root;
    bool isGameSystem() { return true; } bool isCollection() { return false; } bool isHidden() { return false; } bool isVisible() { return true; }
    bool hasPlatformId(PlatformIds::PlatformId) { return false; }
    FolderData* getRootFolder() { return &root; } std::string getName() { return "gb"; } unsigned getGamelistHash() { return 0; }
    std::string getStartPath() { return dir; } std::string getGamelistPath(bool) { return dir + "/gamelist.xml"; } };
struct MetaDataList { static std::vector<MetaDataDecl> getMDD() { return { {MetaDataId::Image, "image", MD_PATH}, {MetaDataId::Thumbnail, "thumbnail", MD_PATH} }; } };
static bool addFileDataNode(pugi::xml_node& parent, FileData* file, const char* tag, SystemData*, bool = false) {
    pugi::xml_node n = parent.append_child(tag); n.append_child("path").text().set(("./" + Utils::FileSystem::getFileName(file->path)).c_str());
    n.append_child("favorite").text().set("true"); return true; }
''' + body + r'''
static std::string readAll(const std::string& p) { std::ifstream i(p, std::ios::binary); std::stringstream s; s << i.rdbuf(); return s.str(); }
static void writeAll(const std::string& p, const std::string& t) { Utils::FileSystem::createDirectory(Utils::FileSystem::getParent(p)); std::ofstream(p, std::ios::binary) << t; }
static const std::string GL = "<?xml version=\"1.0\"?>\n<gameList>\n\t<game>\n\t\t<path>./Bravo.gb</path>\n\t\t<desc>restored from the cloud</desc>\n\t</game>\n</gameList>\n";
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    std::string base = argv[1]; int bad = 0;
    auto fresh = [&](const std::string& name, SystemData& sys, FileData& alpha) {
        sys.dir = base + "/" + name + "/roms/gb"; Paths::gHome = base + "/" + name + "/es"; gCache.clear(); gKillAfter = -1;
        Utils::FileSystem::createDirectory(sys.dir); alpha.path = sys.dir + "/Alpha.gb"; alpha.sys = &sys; writeAll(alpha.path, ""); sys.root.files = {&alpha}; };
    for (int a = 2; a < argc; a++) {
        std::string c = argv[a]; SystemData sys; FileData alpha; fresh(c, sys, alpha); std::string gl = sys.dir + "/gamelist.xml";
        if (c == "outside" || c == "inode") {
            Utils::FileSystem::exists(gl); writeAll(gl, GL); struct stat b; ::stat(gl.c_str(), &b);
            alpha.md.changed = true; updateGamelist(&sys); std::string after = readAll(gl); struct stat s; ::stat(gl.c_str(), &s);
            if (c == "outside") { bool ok = after.find("Bravo.gb") != std::string::npos && after.find("Alpha.gb") != std::string::npos;
                printf("outside: Alpha %s, Bravo %s\n", after.find("Alpha.gb") != std::string::npos ? "present" : "absent", after.find("Bravo.gb") != std::string::npos ? "present" : "absent");
                if (!ok) { printf("FAIL outside: the entry that arrived from outside was lost by the save (L-05)\n"); bad++; } }
            else { printf("inode: %s\n", s.st_ino == b.st_ino ? "the same (written in place)" : "new (replaced)");
                if (s.st_ino == b.st_ino) { printf("FAIL inode: gamelist.xml written in place (D-CLOUD-078)\n"); bad++; } }
        } else if (c == "unparsed") {
            std::string cut = GL.substr(0, 60); writeAll(gl, cut); alpha.md.changed = true; updateGamelist(&sys);
            bool same = readAll(gl) == cut; printf("unparsed: the file %s\n", same ? "kept its bytes" : "was written over");
            if (!same) { printf("FAIL unparsed: a gamelist.xml that did not parse was written over with the dirty entry alone (EP-1)\n"); bad++; }
        } else if (c == "recovery") {
            writeAll(gl, GL); std::string rec = Paths::gHome + "/recovery/gb/Alpha.xml"; writeAll(rec, "<gameList><game><path>./Alpha.gb</path><favorite>true</favorite></game></gameList>");
            packGamelist(&sys); struct stat s; bool there = ::stat(rec.c_str(), &s) == 0;
            printf("recovery: after packGamelist the record is %s\n", there ? "still there for parseGamelist" : "gone");
            if (!there) { printf("FAIL recovery: recovery cleared before parse (EP-2)\n"); bad++; }
        } else if (c == "media") {
            std::string img = sys.dir + "/images/Alpha-image.png";
            writeAll(gl, "<?xml version=\"1.0\"?>\n<gameList>\n\t<game>\n\t\t<path>./Alpha.gb</path>\n\t\t<image>./images/Alpha-image.png</image>\n\t</game>\n</gameList>\n");
            Utils::FileSystem::exists(img); writeAll(img, "png");   // the session looked before the restore wrote it
            cleanupGamelist(&sys); bool kept = readAll(gl).find("Alpha-image.png") != std::string::npos;
            printf("media: the restored picture's reference %s\n", kept ? "kept" : "removed");
            if (!kept) { printf("FAIL media: CLEAN GAMELISTS removed the reference to a picture restored after the session's first look (3.15)\n"); bad++; }
        } else if (c == "record") {
            std::string rec = Paths::gHome + "/recovery/gb/Alpha.xml"; writeAll(rec, "previous record"); gKillAfter = 0;
            try { saveToXml(&alpha, rec, false); } catch (Killed&) {}
            bool kept = readAll(rec) == "previous record"; printf("record: after a write killed at its start the previous record is %s\n", kept ? "whole" : "gone or cut");
            if (!kept) { printf("FAIL record: saveToXml removed the previous recovery record before its write (EP-3)\n"); bad++; }
        } else if (c == "kill") {
            const char* fs[] = {"updateGamelist", "packGamelist", "cleanupGamelist"};
            for (auto f : fs) {
                SystemData s2; FileData a2; fresh(std::string("kill-") + f, s2, a2); std::string g2 = s2.dir + "/gamelist.xml";
                std::string before = "<?xml version=\"1.0\"?>\n<gameList>\n\t<game>\n\t\t<path>./Alpha.gb</path>\n\t\t<image>./images/gone.png</image>\n\t</game>\n\t<game>\n\t\t<path>./Gone.gb</path>\n\t</game>\n</gameList>\n";
                writeAll(g2, before); a2.md.changed = true; gKillAfter = 20;
                try { if (std::string(f) == "updateGamelist") updateGamelist(&s2); else if (std::string(f) == "packGamelist") packGamelist(&s2); else cleanupGamelist(&s2); } catch (Killed&) {}
                bool whole = readAll(g2) == before; printf("kill %s: the previous file %s\n", f, whole ? "whole" : "cut");
                if (!whole) { printf("FAIL kill %s: a write killed half-way left a cut gamelist.xml (D-CLOUD-078)\n", f); bad++; }
            }
        }
    }
    if (bad) { printf("FAIL S1: %d case(s)\n", bad); return 1; }
    return 0;
}
'''
d = tempfile.mkdtemp(prefix="s1-data-", dir="/workspace/tmp/m6-t33/tmp")
run(harness, "s1", ("-fsanitize=address,undefined", "-I" + pugi), args=(d, *cases))

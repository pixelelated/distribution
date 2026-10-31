"""PL-25 (#680; a lead for the rescan's owner, T2): the screensaver's game list against the rescan's delete.

    python3 -I pl25-screensaver.py <SystemScreenSaver.cpp>

SystemScreenSaver's countGameListNodes, pickRandomGameMedia and
selectGameMedia, extracted as written, over doubles: a FileData with an image
path and a system, SystemData::sSystemVector with one system of three games,
PlatformIds, Randomizer (index 0), Utils::FileSystem::exists (true), LOG.
The sequence is the one a long transfer allows: a slideshow screensaver
starts during the transfer (nothing holds it off while GuiCloudTransfer runs;
Window.cpp:777-779) and fills its list (countGameListNodes); the transfer
ends and posts SystemData::rescanChangedFolders (GuiCloudTransfer.cpp:335),
whose `vanished` deletes a game gone from disk (SystemData.cpp:459-473,
`delete n`); the screensaver picks its next picture. The list is cleared
only when the screensaver stops (resetCounts, Window.cpp:1117,
SystemScreenSaver.h:95). Asserted: the pick reads no freed FileData. At the
pin: a heap-use-after-free in selectGameMedia. The fix is the rescan's
owner's (T2's SystemData.cpp), recorded, not made here.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
count = function(src, r"^unsigned long SystemScreenSaver::countGameListNodes\(bool video\)", "PL-25")
pick = function(src, r"^std::string SystemScreenSaver::pickRandomGameMedia\(bool video\)", "PL-25")
select = function(src, r"^std::string\s+SystemScreenSaver::selectGameMedia\(FileData\* game, bool video\)", "PL-25")

harness = r'''
#include <algorithm>
#include <cstdio>
#include <string>
#include <unordered_set>
#include <vector>
struct NullLog { template <class T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
enum FileType { GAME = 1, FOLDER = 2 };
namespace PlatformIds { enum PlatformId { IMAGEVIEWER, PLATFORM_IGNORE }; }
struct SystemData;
struct FileData {
	std::string image; SystemData* system;
	std::string getVideoPath() { return ""; } std::string getImagePath() { return image; }
	FileData* getSourceFileData() { return this; } SystemData* getSystem() { return system; } };
struct FolderData { std::vector<FileData*> files;
	std::vector<FileData*> getFilesRecursive(unsigned int, bool = false) { return files; } };
struct SystemData {
	FolderData root;
	static std::vector<SystemData*> sSystemVector;
	bool isGameSystem() { return true; } bool isCollection() { return false; }
	bool hasPlatformId(PlatformIds::PlatformId) { return false; }
	FolderData* getRootFolder() { return &root; }
	std::string getFullName() { return "Game Boy"; } std::string getName() { return "gb"; } };
std::vector<SystemData*> SystemData::sSystemVector;
namespace Utils { namespace FileSystem { bool exists(const std::string&) { return true; } } }
namespace Randomizer { int random(int) { return 0; } }
struct SystemScreenSaver {
	bool mGamesWithVideosLoaded = false, mGamesWithImagesLoaded = false;
	std::vector<FileData*> mGamesWithImages, mGamesWithVideos;
	FileData* mCurrentGame = nullptr;
	std::string mSystemName, mGameName;
	unsigned long countGameListNodes(bool video);
	std::string pickRandomGameMedia(bool video);
	std::string selectGameMedia(FileData* game, bool video);
};
''' + count + "\n" + pick + "\n" + select + r'''
int main()
{
	setvbuf(stdout, nullptr, _IONBF, 0);
	SystemData gb;
	SystemData::sSystemVector.push_back(&gb);
	for (const char* n : { "Alpha", "Bravo", "Charlie" })
		gb.root.files.push_back(new FileData{ std::string("/roms/gb/images/") + n + ".png", &gb });
	SystemScreenSaver saver;
	printf("the slideshow starts during a transfer: %lu game(s) in its list\n", saver.countGameListNodes(false));
	FileData* gone = gb.root.files[0];
	gb.root.files.erase(gb.root.files.begin());
	delete gone;   // the transfer's rescan: SystemData.cpp's vanished(), `delete n`
	printf("the rescan deleted one game gone from disk; the next picture is picked\n");
	std::string path = saver.pickRandomGameMedia(false);
	printf("picked %s: nothing read a freed FileData\n", path.c_str());
	return 0;
}
'''
run(harness, "pl25")

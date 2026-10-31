"""02 § The input: every write site, every exists( of the input files, the hotkey names, the hot-plug (#682, Q2).

    python3 -I t35-input.py <es worktree> <commit> <paths.txt> [writes=N real_writes=N reads_counted=N exists=N rows=N]

The seven write sites are the § 5 writes grep's (R2 cmd 13) less the two CMake
registrations; each is read at its line for its mechanism (the opening mode or the
library call), whether it is atomic, and what its reader makes of a cut file. The
`exists(` rows are every check of an input file, with the file's writer. The cache's
answer (3.11) is read from `utils/FileSystemUtil.cpp` (T36's, outside the 96, checked as
such); the unit case at stage C proves it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-input.py <es worktree> <commit> <paths.txt> [key=value ...]")
IM, FM, LG, AM = "es-core/src/InputManager.cpp", "es-core/src/FavoriteMusicManager.cpp", "es-core/src/Log.cpp", "es-core/src/AudioManager.cpp"
GD, GI, IC = "es-core/src/guis/GuiDetectDevice.cpp", "es-core/src/guis/GuiInputConfig.cpp", "es-core/src/InputConfig.cpp"
FS = "es-core/src/utils/FileSystemUtil.cpp"

# The writes grep's own hits, recomputed: the alternation of § 5's writes run.
hits = [(p, n) for p, n, t in c.grep(r"std::ofstream|ofstream|AtomicFile|save_file\(|fopen\(|writeText|writeFile|std::rename|rename\(")]
cnt = {"writes": len(hits), "real_writes": 0, "reads_counted": 0, "exists": 0, "rows": 0}

W = [
    (IM, 1225, r"doc\.save_file\(WINSTRINGW\(path\)", "`es_input.cfg` (`getConfigPath()`)", "pugixml `save_file`: the path opened for writing and the document written in place", "no",
     "`load_file` fails: at load `tryLoadInputConfig` logs `Error parsing input config` and returns false (`:899-903`), the pad reads as unconfigured; at the next write the merge is skipped (`:1191-1193`) and the file is rewritten with that one device", "write"),
    (IM, 1232, r"lastdoc\.save_file\(WINSTRINGW\(lastpath\)", "`es_last_input.cfg` (`getTemporaryConfigPath()`, `:1291-1293`)", "pugixml `save_file`, in place; the last device alone, *so that people can easily share their config* (`:1227`)", "no",
     "nothing in es-core or es-app reads it back (the two lines that name it are `:1231`, `:1293`); a cut file is a cut share", "write"),
    (FM, 71, r"std::ofstream ofs\(favoritesFile, std::ios::app\)", "the favourites file (`getFavoriteMusicFilePath()`)", "`std::ofstream`, `std::ios::app`: one `path;name` line appended", "no (an append)",
     "a cut last line: `readAllLines` (`:34`, `:89`) returns it as one more line that matches no song", "write"),
    (FM, 115, r"std::ofstream ofs\(favoritesFile, std::ios::trunc\)", "the favourites file", "`std::ofstream`, `std::ios::trunc` then the remaining lines (`:121-123`); the last removal deletes the file instead (`:104-106`)", "no",
     "the file emptied or cut at a line: favourites lost from that line on, with no error", "write"),
    (LG, 179, r"std::ofstream\s+mFile;", "the log (`es_log.txt`)", "the member, opened `std::ios::out | std::ios::trunc` at `:46`; the worker flushes per batch (`:98`, `:147`)", "no (a log, rewritten each start)",
     "a shorter log; nothing reads it back (#178's proof is the batch reaching the file)", "write"),
    (AM, 539, r"fopen\(song\.c_str\(\), \"r\"\)", "a song file", "`fopen(..., \"r\")`: **a read**, counted by the grep's `fopen\\(` alternation", "--", "--", "read"),
    (AM, 610, r"fopen\(song\.c_str\(\), \"r\"\)", "a song file (its ID3 tag)", "`fopen(..., \"r\")`: **a read**, as above", "--", "--", "read"),
]
rows = []
for f, n, needle, target, mech, atomic, cut, kind in W:
    c.need(f, n, needle)
    if (f, n) not in hits:
        c.fail.append(f"{f}:{n} is not among the writes grep's hits")
    cnt["real_writes" if kind == "write" else "reads_counted"] += 1
    rows.append([f"`{f.replace('es-core/src/', '')}:{n}`", kind, target, mech, atomic, cut, "tree"])
c.need(LG, 46, r"mFile\.open\(path, std::ios::out \| std::ios::trunc\)")
c.need(IM, 899, r"if \(!res\)")
c.need(IM, 1191, r"if \(!result\)")
cmake = [h for h in hits if h[0] == "es-core/CMakeLists.txt"]
if [n for _, n in cmake] != [122, 257]:
    c.fail.append(f"the CMake hits are {cmake}, expected :122 and :257")
if any("AtomicFile::" in t for _, _, t in c.grep(r"AtomicFile::")):
    c.fail.append("an AtomicFile:: call appeared")
print("**The write sites** (the writes grep's 9 hits less the two CMake registrations `:122`, `:257`; `AtomicFile::` 0):\n")
print(table(["Site", "Kind", "File", "Mechanism", "Atomic", "A cut file reads as", "proved:"], rows))

# Every exists( of an input file, with its writer.
X = [
    (IM, 420, r"if \(!Utils::FileSystem::exists\(mappingFile\)\)", "the SDL mapping files (`gamecontrollerdb.txt`, shipped and user)", "none in ES",
     "**WIN32 only**: the block `:404-483` is `#if WIN32`; it never runs on the device"),
    (IM, 893, r"if \(!Utils::FileSystem::exists\(path\)\)", "`es_input.cfg` (`tryLoadInputConfig`)", "`:1225`", "cached; a miss is remembered, and `loadInputConfig` after a write (`:1239`) reads it"),
    (IM, 1187, r"if \(Utils::FileSystem::exists\(path\)\)", "`es_input.cfg` (`writeDeviceConfig`'s merge)", "`:1225`", "cached; a remembered miss skips the merge and the save keeps only this device (L-07)"),
    (IM, 1250, r"if\(Utils::FileSystem::exists\(path\)\)", "`es_input.cfg` (`doOnFinish`)", "`:1225`", "cached; a remembered miss skips the `onfinish` commands written a line earlier"),
    (GD, 127, r"mFirstRun && Utils::FileSystem::exists\(InputManager::getConfigPath\(\)\)", "`es_input.cfg` (the detect page's first-run skip)", "`InputManager.cpp:1225`", "cached"),
]
c.need(IM, 404, r"^#if WIN32")
c.need(IM, 483, r"^#endif")
xr = []
for f, n, needle, target, writer, note in X:
    c.need(f, n, needle)
    cnt["exists"] += 1
    xr.append([f"`{f.replace('es-core/src/', '')}:{n}`", target, writer, note, "tree; 3.11 at stage C"])
print("\n**Every `exists(` of an input file** (none passes `false`; the § 5 reads run: 41 `FileSystem::exists(` lines, 0 uncached):\n")
print(table(["Site", "File checked", "Writer", "Cache", "proved:"], xr))

# 3.11's answer, from T36's file (outside the 96).
c.need(FS, 1127, r"if \(enableCache\)", outside=True)
c.need(FS, 323, r"return mFileCache\.try_emplace\(hash, std::move\(fetched\)\)", outside=True)
c.need(FS, 296, r"bool exists = ret == 0;", outside=True)
c.need("es-core/src/Settings.cpp", 155, r'mBoolMap\["UseFileCache"\] = true;', outside=True)
print("\n**3.11, the cache's answer, read:** `exists(p)` with the cache on (`Settings.cpp:155`, T36's) asks the cache first (`FileSystemUtil.cpp:1127-1131`) and on a miss stores what `stat64` found, **absence included** (`:296`, `:306`, `:323`); `pugi::xml_document::save_file` writes through `fopen`, never through `Utils::FileSystem`, so nothing clears the entry. On a device whose `es_input.cfg` was absent at the first check, every later `exists(` of it in the session reads false until a cache reset. The unit case 3.11 proves the sequence at stage C; G-01 reads whether the user file exists before any configuration on the image (L-07's precondition). For T36's `FileSystemUtil`: the cache remembers misses; a writer outside `Utils::FileSystem` is invisible to it.\n")

# The two hotkey names.
c.need(IM, 1105, r'if \(!config->getInputByName\("hotkey", &tmp\)\)')
c.need(IM, 1107, r'config->mapInput\("hotkey", tmp\);')
c.need(GI, 73, r'\{ "HotKeyEnable",')
c.need(GI, 273, r'mapInput\("HotKeyEnable", input\)')
c.need(GI, 279, r'mapInput\("HotKeyEnable", Input\(DEVICE_KEYBOARD, TYPE_KEY, 0, 1, true\)\)')
c.need(IC, 188, r"mNameMap\[toLower\(name\)\] = input;")
print("**The two hotkey names:** the SDL-mapping fallback copies `select` to **`hotkey`** (`InputManager.cpp:1105-1107`); the configuration page maps **`HotKeyEnable`** (`GuiInputConfig.cpp:73`, `:273`, `:279`), stored as `hotkeyenable` (`InputConfig.cpp:188`). Which one the launch scripts read is T3's templates; the two names are a fact of these lines (L-09, 3.12). `proved: tree`.\n")

# doOnFinish and the hot-plug.
c.need(IM, 1262, r'find_child_by_attribute\("inputAction", "type", "onfinish"\)')
c.need(IM, 1272, r"int exitCode = Utils::Platform::ProcessStartInfo\(tocall\)\.run\(\);")
print("**`doOnFinish`'s `<command>`** (`:1242-1284`): every `<inputAction type=\"onfinish\">` `<command>` text runs through `ProcessStartInfo(tocall).run()` at `:1272`, **synchronously, on the interface thread**, from `writeDeviceConfig` (`:1238`); a non-zero exit is a `LogWarning` (`:1277`). The shipped `es_input.cfg`'s `inputAction` count is G-01's line (owed). `proved: tree`.\n")
c.need(IM, 813, r"case SDL_JOYDEVICEADDED:")
c.need(IM, 852, r"rebuildAllJoysticks\(\);")
c.need(IM, 864, r"case SDL_JOYDEVICEREMOVED:")
c.need(IM, 875, r"rebuildAllJoysticks\(\);")
c.need(IM, 605, r"writeDeviceConfig\(mInputConfigs\[joyId\]\)")
print("**The hot-plug rebuild's cost:** a pad added (`:813`) or removed (`:864`) rebuilds every joystick on the interface thread (`:852`, `:875`): the joystick subsystem quit and re-initialised (`:376-382`, `:402`), every device reopened (`:517-`), each configuration re-read from `es_input.cfg` (`loadInputConfig`, `:583`), and an SDL-mapped device written back (`:605`, the hot-plug write); the mapping-file pass and the 500 ms settle poll are WIN32-only (`:404-483`). One file parse per pad per event; G-10 is `CANNOT` (no pad on the guest). `proved: tree`.\n")
c.need(IM, 1481, r'command << " -p" << player\+1 << "index "')
c.need(IM, 1482, r'command << " -p" << player\+1 << "guid "')
print("**The controllers blob, for T3's half:** `configureEmulators` (`:1474-1488`) writes `-pNindex <int> -pNguid <hex>` per seat and **no device name**; the GUID string is SDL's hex. The quoting T2 FD-6/FD-7 describe is where a name enters, not here; the blob is built on every launch (`FileData.cpp:547`, T2's) whether `includeControllers` is set or not (L-20). `proved: tree`.")
cnt["rows"] = len(rows) + len(xr)
c.finish("t35-input", cnt, f"{len(rows)} write-site rows ({cnt['real_writes']} writes, {cnt['reads_counted']} reads the grep counts), {len(xr)} exists rows; the writes grep {cnt['writes']} hits")

"""02 § The services: every route the local HTTP server registers (#679, Q1, Q2).

    python3 -I t32-services.py <es worktree> <commit> [registrations=27,patterns=25,literal=16,allowed=27,posts=10]

The registrations are `mHttpServer->Get|Post|Delete(<path>, ...)` in
es-app/src/services/HttpServerThread.cpp at the commit. Every handler runs
on cpp-httplib's pool thread (`new_task_queue`, :145; the server's own
thread is `new std::thread` at :74). ROUTES records, by the registration's
line, what the handler does on that thread, what it posts to the interface
thread and what it writes -- read at the handler's lines. A pattern is the
path string; a raw-regex path (R"(...)") is counted once per pattern, so
two methods on one pattern are one pattern and two registrations.

Exits 1 when a registration has no entry, an entry has no registration, a
handler lacks its isAllowed() call, or a count differs.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t32lib import show  # noqa: E402

POOL = "pool"
ROUTES = {
    149: ("the web page (`/` serves index.html's body)", "-", "-"),
    157: ("the favicon from resources", "-", "-"),
    167: ("a page with Reload games and Quit buttons that call `/reloadgames` and `/quit`", "-", "-"),
    219: ("`?confirm=switchscreen` / `menu`: a confirmation; else `Utils::Platform::quitES()` at `:241` on the pool thread", "a YES/NO `GuiMsgBox` (`:229`)", "-"),
    244: ("`quitES(SHUTDOWN)` at `:249` on the pool thread", "-", "-"),
    252: ("`quitES(REBOOT)` at `:257` on the pool thread", "-", "-"),
    260: ("`ApiSystem::emuKill()` (`:264`, T21's)", "-", "-"),
    268: ("the capabilities JSON (`HttpApi`, `\"Version\"` `HttpApi.cpp:332`)", "-", "-"),
    276: ("every system as JSON, read from `sSystemVector` on the pool thread", "-", "-"),
    284: ("the running game's JSON, `201` with none", "-", "-"),
    299: ("`[ true ]` 200 when no game runs and neither the scraper, the content installer, the hasher nor the updater is running (`:304-308`); else `[ false ]` 201. A cloud sync or the RetroAchievements proxy's work is not asked (D-QA-057's walks rely on it)", "-", "-"),
    323: ("a system's logo from its theme", "-", "-"),
    353: ("a system's games as JSON, walked on the pool thread", "-", "-"),
    370: ("a game's media file by metadata name", "-", "-"),
    407: ("`HttpApi::ImportMedia` (`:440`): the media written on the pool thread (`HttpApi.cpp:258`, `writeAllText` in place, Backlog #1186), the game's metadata set there (L-13)", "`onFileChanged(game, FILE_METADATA_CHANGED)` (`:443`)", "the media file; the metadata in memory"),
    456: ("`HttpApi::ImportFromJson` (`:476`): the game's metadata set on the pool thread (L-13)", "`onFileChanged(game, FILE_METADATA_CHANGED)` (`:479`)", "the metadata in memory"),
    491: ("a game's JSON", "-", "-"),
    514: ("a system's JSON", "-", "-"),
    533: ("nothing on the pool thread; no idle check", "`GuiMenu::updateGameLists(w, false)` (`:539`)", "-"),
    545: ("the body as a message box's text", "a `GuiMsgBox` (`:559`)", "-"),
    562: ("**`mWindow->displayNotificationMessage(req.body)` at `:574`, on the pool thread, unbounded** (L-12)", "-", "the window's toast queue, from the pool thread"),
    577: ("a storage event line", "its handling (`:592`)", "-"),
    599: ("`getFilesRecursive(GAME)` over every game system on the pool thread, no `break` on a match (`:615-630`)", "**a raw `FileData*` to `ViewController::launch` (`:623-626`), one post per match**", "-"),
    632: ("`loadGamelistFile` and `updateGamelist(system)` on the pool thread (`:659`, `:688`); a `new SystemData` for an unloaded system, deleted at `:676`/`:692`", "`updateGameLists` (`:698`) or `onFileChanged(root, FILE_METADATA_CHANGED)` (`:702-704`)", "gamelist.xml (`updateGamelist`)"),
    711: ("`loadGamelistFile` against the system's own `fileMap`; each listed file's recovery entry removed and the file deleted on the pool thread (`:751-755`, a cached `exists` first); the `FileData` leaked on purpose (`:771`) (L-13)", "`onFileChanged(root, FILE_REMOVED)` per system (`:776-779`)", "the game files removed"),
    786: ("a resource file", "-", "-"),
    803: ("any other path under the web root, else 404", "-", "-"),
}

tree, commit = sys.argv[1:3]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[3].split(","))) if len(sys.argv) > 3 else {}
src = show(tree, commit, "es-app/src/services/HttpServerThread.cpp")
regs = []
for m in re.finditer(r'mHttpServer->(Get|Post|Delete)\(\s*(R"\((.*?)\)"|"([^"]*)")', src):
    line = src.count("\n", 0, m.start()) + 1
    raw = m.group(3) is not None
    regs.append((line, m.group(1).upper(), m.group(3) if raw else m.group(4), raw))
starts = [r[0] for r in regs] + [src.count("\n") + 1]
lines = src.split("\n")
fail = []
for i, (line, meth, path, raw) in enumerate(regs):
    body = "\n".join(lines[line - 1:starts[i + 1] - 1])
    if "isAllowed(req, res)" not in body:
        fail.append("%s %s (:%d) has no isAllowed() call" % (meth, path, line))
fail += [":%d has no entry" % r[0] for r in regs if r[0] not in ROUTES]
fail += ["an entry names :%d, where there is no registration" % l for l in ROUTES if l not in [r[0] for r in regs]]
print("| Line | Method | Path | On the pool thread | Posts to the interface thread | Writes |")
print("| --- | --- | --- | --- | --- | --- |")
for line, meth, path, raw in regs:
    work, post, write = ROUTES.get(line, ("?", "?", "?"))
    shown = ('R"(%s)"' % path) if raw else path
    print("| `:%d` | %s | `%s` | %s | %s | %s |" % (line, meth, shown.replace("|", "\\|"), work, post, write))
patterns = set(p for _, _, p, _ in regs)
counts = {"registrations": len(regs), "patterns": len(patterns), "literal": len(set(p for _, _, p, raw in regs if not raw)),
          "allowed": src.count("isAllowed(req, res)"), "posts": src.count("postToUiThread(")}
print()
print("generated, asserted: %d registrations over %d distinct path patterns (%d plain strings, %d raw regex); isAllowed() in every handler (%d calls); %d postToUiThread( calls; listen(ip, 1234) at :%d"
      % (counts["registrations"], counts["patterns"], counts["literal"], counts["patterns"] - counts["literal"], counts["allowed"], counts["posts"],
         src.count("\n", 0, src.index("listen(ip.c_str(), 1234)")) + 1))
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t32-services: " + "; ".join(fail))
    sys.exit(1)

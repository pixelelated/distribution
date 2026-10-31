"""02 § The surfaces: the window's toast queue, its cards and its posted functions (#682, Q1, Q4).

    python3 -I t35-surfaces.py <es worktree> <commit> <paths.txt> [rows=N containers=N sites=N]

One row per container, the lock, and every enqueue, dequeue, layout and free of the
toast queue, the popups, the card vector and the posted functions; each cited line is
checked for its text at <commit>. The card's position is read against T34's component
(`AsyncNotificationComponent.cpp`, outside the 96, checked as such). T34's held
`stage-e/s2-window.patch` is the last row, read from T34's distribution branch by the
coordinator's 06:07 UTC instruction (#682 comment 6539898291).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-surfaces.py <es worktree> <commit> <paths.txt> [key=value ...]")
WH, WC = "es-core/src/Window.h", "es-core/src/Window.cpp"
ANC = "es-core/src/components/AsyncNotificationComponent.cpp"

# (file, line, needle, kind, function, container(s), lock, what it does, invariant, proof, proved, outside)
R = [
    (WH, 123, r"std::vector<AsyncNotificationComponent\*> mAsyncNotificationComponent", "container", "--", "the card vector", "the lock below",
     "raw pointers the window `new`s at `:1168` and frees at `:1248`; the caller keeps the same raw pointer", "a card is owned by the window and freed only once `isRunning()` is false", "Q4's lifetimes table; L-02", "tree", False),
    (WH, 133, r"std::vector<PostedFunction> mFunctions", "container", "--", "the posted functions", "the lock below (not in `unregisterPostedFunctions`)",
     "each a `std::function` and an owner token `void* container` (`:127-131`)", "a post runs once, on the interface thread, at the next update", "L-03", "tree", False),
    (WH, 135, r"std::vector<GuiInfoPopup\*> mNotificationPopups", "container", "--", "the toasts on screen", "taken where they are removed under a card or a song; not in `update`/`render`",
     "raw `GuiInfoPopup` pointers, top-centred, stacked", "one floating surface at a time with the cards (D-UI-093)", "G-02", "tree", False),
    (WH, 154, r"std::vector<NotificationMessage> mNotificationMessages", "container", "--", "the toast queue", "the lock below",
     "pairs of words and a duration in ms (`:153`)", "nothing is dropped (D-UI-093's sentence)", "3.14", "tree", False),
    (WC, 293, r"static std::mutex mNotificationMessagesLock", "lock", "--", "the queue, the cards, the posts", "--",
     "one file-static mutex", "every enqueue and dequeue of the queue, the cards and the posts takes it, except `unregisterPostedFunctions`", "Q3's locks table", "tree", False),
    (WC, 311, r"void Window::displayNotificationMessage", "enqueue", "displayNotificationMessage", "the toast queue", "taken (`:313`)",
     "`push_back` of the words with `notificationDuration(duration)` (`:298-309`: `<= 0` is the display-titles setting within 2..120 s, else 10 s)", "kept: any thread may call it", "3.15", "tree", False),
    (WC, 324, r"void Window::processNotificationMessages", "dequeue", "processNotificationMessages (update `:466`)", "the queue -> the popups", "taken (`:326`)",
     "returns while any card is up (`:336-337`); takes the **back** of the queue (`:339-340`), builds a `GuiInfoPopup`, lays out", "one surface at a time: kept; *the order is the order things happened* (`:334-335`): **not kept** -- the newest first (L-01)", "3.14; G-02 (the toast after the card); G-03 `CANNOT`", "tree", False),
    (WC, 353, r"void Window::stopNotificationPopups", "free", "stopNotificationPopups", "the popups", "the caller's (`:1165` holds it)",
     "deletes every popup and clears the vector", "kept: called with the lock from the card's creation", "--", "tree", False),
    (WC, 365, r"void Window::updateNotificationPopups", "free", "updateNotificationPopups (update `:557`)", "the popups", "not taken",
     "updates each popup, deletes one whose fade has ended (`:373-379`), lays out", "kept while every card is created on the interface thread (each caller at the pin does; a read, Q4)", "Q4's caller read", "tree", False),
    (WC, 396, r"void Window::layoutNotificationPopups", "layout", "layoutNotificationPopups", "the popups", "the caller's",
     "stacks from 0.02 H with a 0.02 H gap, a fading popup sliding up by its eased height", "kept", "G-02", "tree", False),
    (WC, 418, r"void Window::processSongTitleNotifications", "free + enqueue", "processSongTitleNotifications (update `:465`)", "the popups, the queue", "taken (`:427`), released before the enqueue (`:441`)",
     "removes an on-screen song toast, then queues the new title through `displayNotificationMessage` (`:442`)", "kept: a song toast queues like any other", "--", "tree", False),
    (WC, 782, r"if \(!mRenderScreenSaver\)", "draw", "render", "the popups, the cards", "the cards' pass takes it (`:1179`); the popups' loop does not",
     "popups then cards, both only while no screensaver draws (`:782-788`)", "kept: the screensaver hides both", "G-09", "tree", False),
    (WC, 1146, r"bool Window::hasAsyncNotifications", "read", "hasAsyncNotifications", "the card vector", "taken (`:1148`)",
     "true while any card is queued, lingering or fading (`.h:100-101`)", "kept", "--", "tree", False),
    (WC, 1152, r"AsyncNotificationComponent\* Window::createAsyncNotificationComponent", "enqueue", "createAsyncNotificationComponent", "the cards; the queue", "taken (`:1154`)",
     "a toast on screen goes back on the queue with `notificationDuration(-1)` (`:1164`) -- **a fresh default duration, not its remainder** -- and the popups stop (`:1165`); the card is `new`ed and its raw pointer returned (`:1168-1174`)", "one surface at a time: kept; the toast's words: kept whole", "3.14's second half; G-02", "tree", False),
    (WC, 1177, r"void Window::renderAsyncNotifications", "layout + draw", "renderAsyncNotifications", "the cards", "taken for the whole pass (`:1179`)",
     "each card centred, `posX = W*0.5 - w*0.5` (`:1192`), from 0.02 H (`:1183`), stacked by height + 0.01 W (`:1194`, `:1231`); fades in place (`:1217-1221`), slides up under a clip when closing (`:1203-1215`)", "the position re-applied every frame agrees with the component's own (next row)", "G-02's two edges", "tree", False),
    (ANC, 112, r"setPosition\(Renderer::getScreenWidth\(\) \* 0\.5f - mSize\.x\(\) \* 0\.5f", "position (T34's)", "AsyncNotificationComponent ctor", "the card", "--",
     "the card's own position before its first render, centred at 0.02 H (`:112-113`); its width `max(text, 0.9 W)` (`:62-64`); the comment `:110-111` asks the two to agree", "kept at the pin: `:1192` and `:112` compute the same x", "G-02 measures the edges at 640", "tree", True),
    (WC, 1236, r"void Window::updateAsyncNotifications", "free", "updateAsyncNotifications (update `:556`)", "the card vector", "taken (`:1238`)",
     "**the one place a card is freed** (`:1246-1248`), once `isRunning()` is false", "kept while the caller stops using its raw pointer before the card ends; `deinit` (`:188-207`) and `~Window` (`:49-63`) never free a card, a popup or the queue (L-02)", "Q4", "tree", False),
    (WC, 1262, r"void Window::unregisterPostedFunctions", "free", "unregisterPostedFunctions", "the posted functions", "**not taken**",
     "erases the owner's posts while iterating `mFunctions` (`:1267-1273`)", "**not kept**: `postToUiThread` (`:1278`) and `processPostedFunctions` (`:1296`) take the lock (L-03)", "3.17 (TSan)", "tree", False),
    (WC, 1276, r"void Window::postToUiThread", "enqueue", "postToUiThread", "the posted functions", "taken (`:1278`)",
     "appends the function and its owner token, and wakes a sleeping window (`:1284-1289`)", "kept; it promises nothing to a poster that dies before the drain (L-03, T34 L-12)", "Q4", "tree", False),
    (WC, 1292, r"void Window::processPostedFunctions", "dequeue", "processPostedFunctions (update `:464`)", "the posted functions", "taken to copy and clear (`:1296-1303`), released to run",
     "runs each copied function under `TRYCATCH` (`:1305-1306`)", "kept: a post may post again without a deadlock", "--", "tree", False),
]
rows = []
cnt = {"rows": 0, "containers": 0, "sites": 0}
for f, n, needle, kind, fn, cont, lock, what, inv, proof, proved, outside in R:
    c.need(f, n, needle, outside=outside)
    loc = f"`{f.replace('es-core/src/', '')}:{n}`" + (" (T34's)" if outside else "")
    rows.append([loc, kind, fn, cont, lock, what, inv, proof, proved])
    cnt["rows"] += 1
    cnt["containers" if kind in ("container", "lock") else "sites"] += 1

# T34's held patch: read from T34's distribution branch (outside both of this lane's trees).
import subprocess  # noqa: E402
T34 = "/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-components-681"
P = "docs/audits/2026_10_30-epic-m6-es-core-components/stage-e/s2-window.patch"
r = subprocess.run(["git", "-C", T34, "show", f"feature/m6-es-core-components-681:{P}"], capture_output=True, text=True)
if r.returncode or "std::weak_ptr<AsyncNotificationComponent> createAsyncNotificationComponent" not in r.stdout:
    c.fail.append("T34's s2-window.patch not read, or its shape changed")
rows.append(["T34's `stage-e/s2-window.patch` (#1310)", "held patch", "createAsyncNotificationComponent, updateAsyncNotifications", "the card vector", "taken, as now",
             "the window owns each card through a `shared_ptr` whose deleter frees it on the interface thread; the caller gets a `weak_ptr`; a stopped card is retired until the window holds the last reference",
             "would make the card's free safe against a holder's late use (L-02's half); **changes `createAsyncNotificationComponent`'s return type**, so the 10 callers in es-app (`ContentInstaller.cpp:60`, `ProxyCards.cpp:215`, `:257`, `:514`, `ThreadedBluetooth.cpp:15`, `:72`, `ThreadedCloudSync.cpp:46`, `ThreadedHasher.cpp:126`, `guis/GuiMenu.cpp:11717`, `guis/GuiUpdate.cpp:162`: five lanes) and the three doubles (`tests/app-unit/fakes/Window.h:11`, `ProxyCardsTests.cpp:154`, `tests/hasher-offline-index.py:65`) change with it",
             "proposed for the pause: adopted into a stage-E stream only with its callers' half named for their owners, else a collision named (§ 1 i)", "design"])
cnt["rows"] += 1
print(table(["Site", "Kind", "Function", "Container", "Lock", "What it does", "Invariant", "Proof or frame", "proved:"], rows))
c.finish("t35-surfaces", cnt, f"{cnt['rows']} rows: {cnt['containers']} containers and the lock, {cnt['sites']} sites (one of them T34's component's, outside the 96), and T34's held patch")

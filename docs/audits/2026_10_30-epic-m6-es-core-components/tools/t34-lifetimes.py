"""02 § The lifetimes (#681): every `delete this`, `std::thread`, `.detach(` and
`postToUiThread` in the 80 at the pin (asserted 4 / 1 / 1 / 2, each with a row),
and every lifetime the read found beyond the four shapes, each row's cited line
asserted to still hold the code the row describes.
    t34-lifetimes.py <ES worktree> [paths file]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import COMP, die, show, paths

W = sys.argv[1]
files = paths(sys.argv[2] if len(sys.argv) > 2 else None)
SHAPES = {"delete this": (r"\bdelete this\b", 4), "std::thread": (r"std::thread\b", 1), ".detach(": (r"\.detach\(", 1), "postToUiThread": (r"postToUiThread\(", 2)}
G = {  # file:line -> (who joins, drains or owns it; what it touches after; disposition; proved)
 "OptionListComponent.h:96": ("the popup, deleted from its own row's accept handler (a `std::function` inside `mMenu`'s row)", "nothing: the handler's last statement (`:97`)", "L-11: sound by the invariant (nothing above it touches the popup after the call returns); 3.19's ASan case at stage C", "tree"),
 "OptionListComponent.h:145": ("the same, the second row template", "nothing: the handler's last statement (`:146`)", "L-11, as `:96`", "tree"),
 "OptionListComponent.h:158": ("the popup, deleted from its own BACK button's callback: the button's `std::function` is destroyed while it runs (`es-code-traps.md:22`'s shape)", "nothing: the lambda is `{ delete this; }`", "L-11: sound only while `ButtonComponent` and the grids above it return without touching their members; 3.19", "tree"),
 "OptionListComponent.h:195": ("the popup, deleted from its own `input()`", "nothing: `return true` (`:196`)", "L-11, sound", "tree"),
 "VideoVlcComponent.cpp:91": ("a detached thread that releases the media player and deletes the `VideoContext` (`:93-94`)", "VLC's thread may still be in `display` (`:53-61`) reading `ctx->component`, nulled at `:89` on the interface thread with no lock", "L-10: a data race, and a call into a component being destroyed (`~VideoVlcComponent` -> `stopVideo` `:911`); upstream surface outside the lanes; recorded (G-10 `CANNOT`: no media)", "tree"),
 "VideoVlcComponent.cpp:95": ("the same thread, joined by nobody", "`ctx`, after the release returns", "L-10", "tree"),
 "TextEditComponent.cpp:39": ("`Window`'s post queue (T35's `postToUiThread`), drained later on the interface thread", "raw `this` (`startEditing()`): a text edit destroyed before the post runs is a use after free", "L-12: 3.20's case at stage C with the fakes' `Window.h`; a weak token the posts check is the pause's, with T33's `AppWindow` named", "S2 `2cbb62d7b` (#1311): the post holds the field's token weakly; `SAN asan-textedit` rc 0 after, rc 1 before (`stage-e/s2-after.txt`, `s2-before.txt`)"),
 "TextEditComponent.cpp:47": ("the same queue", "raw `this` (`stopEditing()`)", "L-12, as `:39`", "S2 `2cbb62d7b` (#1311), as `:39`"),
}
R = [  # (file, line, the code the line must still hold, what it is, disposition, proved)
 ("AsyncNotificationComponent.cpp", 119, "mClosing = true", "`close()` writes `mClosing` and `mFadeTime` (`:119-120`) with no lock, from the holders' worker threads (`ThreadedCloudSync`, `ProxyCards`, `ThreadedBluetooth`, ...), while the interface thread's `update()` reads and writes both (`:267-299`; plain `bool` and `int`, h `:72`, `:74`); `mMutex` guards the text only (`:149`-`:196`)",
  "**L-22 (new): a data race on the card's closing state**, in a lane surface; a host ThreadSanitizer case at stage C (a card double-free of `Window`, `close()` on one thread, `update()` on the other); a `bug` at stage D if it fires", "S2 `2cbb62d7b` (#1309): `close()` is one atomic request, `update()` turns it; `SAN tsan-card` rc 0 after, rc 66 before; the interleaving case PASS after, FAIL before"),
 ("AsyncNotificationComponent.cpp", 123, "~AsyncNotificationComponent", "the card is owned by `Window` (`Window.h:123`, a vector of raw pointers) and deleted once it stops running (`Window.cpp:1242-1252`, T35's); every holder keeps the raw pointer `createAsyncNotificationComponent` returned (`Window.cpp:1152-1169`)",
  "**§ 1 (b), T2 PC-1, the component's half:** the card promises a holder nothing after the window deletes it, and it cannot refuse a late `close()` or `updateText()` (no handle, no generation); the window's teardown order is T35's, the holders' half T18's and T20's; a handle the window keeps alive until the holder lets go is the pause's", "S2 `2cbb62d7b` (#1310), the component's half: `handle()`; Window's half `stage-e/s2-window.patch` (T35's), the holders' merge debt; `SAN asan-card-handle` rc 0 after (2 of 2 late calls refused), rc 1 before"),
 ("MenuComponent.cpp", 478, "MenuComponent::clearButtons()", "`clearButtons()` (`:478-483`) deletes the button bar, whose buttons own their callbacks", "`es-code-traps.md:22`'s rule restated beside the lines; no component-side guard exists at the pin, and the rule's `postToUiThread` with a weak handle is the callers' discipline", "tree"),
 ("SwitchComponent.h", 53, "std::function<void()> mOnChangedCallback", "the switch stores its callback by value", "**§ 1 (c), T26 PL-27:** a page's lambda that captures a `shared_ptr` to the component that stores it makes a cycle the page's `onFinalize` must break; the type is not weak by design; LeakSanitizer over an extracted builder at stage C; a design ruling at the pause", "tree"),
 ("OptionListComponent.h", 658, "std::function<void(const T&)> mSelectedChangedCallback", "the option list stores its callback by value, called from `onSelectedChanged` (`:632-633`)", "§ 1 (c), as the switch's", "tree"),
 ("OptionListComponent.h", 310, "onSelectedChanged();", "`input()` left: the callback, then `return true` (`:311`)", "**§ 1 (d), T31 L-03 / #1243's invariant, kept:** a page that deletes the option list's owner inside the callback is safe only because nothing after the callback touches the component (`:311`, `:324`)", "tree"),
 ("OptionListComponent.h", 323, "onSelectedChanged();", "`input()` right: the callback, then `return true` (`:324`)", "§ 1 (d), as `:310`", "tree"),
 ("ImageGridComponent.h", 91, "virtual void clear()", "`clear()` and `resetGrid()` (#207) drop the entries and the tiles", "**§ 1 (e), #1266's contract, corrected by the seat (G-7, verified):** `clear()` -> `resetGrid()` clears `mVisibleTiles` (`:1383`) but never `mScrollLoopTiles`, which `ensureVisibleTileExist` clears only after its early return for an empty list (`:316-317` before `:339-340`), and `render` still draws it (`:762-763`): a cleared looping grid keeps its loop-copy tiles. The stage-B reading here said the grid held no tile after `clear()`, which was wrong. T32's `s4-views.py` is the harness shape; the view's fix is T32's `1655e2f4c`", "S6 `6050b8419` (#1329): `resetGrid()` clears the loop-copy tiles too; PL-33's case PASS after, FAIL before (`stage-e/s6-before.txt`, `s6-after.txt`)"),
 ("WebImageComponent.cpp", 243, "new HttpReq(mUrlToLoad, &options)", "a stack `HttpReqOptions` (`:239`) handed by pointer to a heap `HttpReq`", "L-21: sound, the constructor consumes the options before it returns (`HttpReq.cpp:119-123`, `:131-132`, `:172-176`, T21's)", "tree"),
]
got = {}
for f in files:
    for n, line in enumerate(show(W, f).split("\n"), 1):
        code = line.split("//")[0]
        for name, (rx, _) in SHAPES.items():
            if re.search(rx, code):
                got.setdefault("%s:%d" % (f[len(COMP):], n), []).append(name)
counts = {name: sum(1 for v in got.values() if name in v) for name in SHAPES}
for name, (_, want) in SHAPES.items():
    if counts[name] != want:
        die("%s: %d, expected %d" % (name, counts[name], want))
missing = sorted(set(got) - set(G)); extra = sorted(set(G) - set(got))
if missing or extra:
    die("shape rows without a disposition: %s; dispositions without a row: %s" % (missing, extra))
for f, n, must, *_ in R:
    lines = show(W, COMP + f).split("\n")
    if n > len(lines) or must not in lines[n - 1]:
        die("%s:%d no longer holds %r" % (f, n, must))
print("| Site | Shape | Who joins, drains or owns it | What it touches after | Disposition | proved |")
print("| --- | --- | --- | --- | --- | --- |")
for k in sorted(got, key=lambda k: (k.split(":")[0], int(k.split(":")[1]))):
    who, after, disp, proved = G[k]
    print("| `%s` | %s | %s | %s | %s | %s |" % (k, " + ".join(got[k]), who, after, disp, proved))
for f, n, must, what, disp, proved in R:
    print("| `%s:%d` | read | %s | - | %s | %s |" % (f, n, what, disp, proved))
print()
print("Generated, asserted by `tools/t34-lifetimes.py`: %d shape rows (`delete this` %d, `std::thread` %d, `.detach(` %d, `postToUiThread` %d), each with a disposition; %d read rows, each cited line asserted to hold its code at the pin." % (
    len(got), counts["delete this"], counts["std::thread"], counts[".detach("], counts["postToUiThread"], len(R)))

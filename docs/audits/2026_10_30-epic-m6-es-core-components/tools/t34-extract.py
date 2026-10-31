"""Lift the seams' lines from the pin, verbatim, into <out>/x_<name>.inc for
T34's components-tests and sanitizer cases (#681). Each spec names its file,
its line range and the code its first and last lines must hold; a range that
no longer holds it is refused (exit 1, nothing written), so a case never runs
against lines it was not written for.
    t34-extract.py <ES worktree> <pin> <out dir>"""
import os, subprocess, sys
W, PIN, OUT = sys.argv[1:4]
C = "es-core/src/components/"
def where(f):  # a component by its name; anything else (read only, other lanes' files) by its tree path
    return f if f.startswith("es-") else C + f
SPECS = [  # name, file, first, last, the first line holds, the last line holds
 ("mlme_shares", "MultiLineMenuEntry.cpp", 72, 75, "float h = th + sh;", "setRowHeightPerc(1, (sh * 1.1) / h);"),
 ("text_limit", "TextComponent.cpp", 486, 486, "int limit = mSize.y() - mPadding.y() - mPadding.y();", "int limit"),
 ("slider_text", "SliderComponent.cpp", 276, 299, "std::stringstream ss;", "const std::string val = ss.str();"),
 ("slider_precision", "SliderComponent.cpp", 44, 59, "int calculatePrecision(float step)", "}"),
 ("button_pad", "MenuComponent.cpp", 14, 14, "#define BUTTON_GRID_HORIZ_PADDING", "0.022"),
 ("button_width", "MenuComponent.cpp", 547, 552, "float buttonGridWidth = (float)BUTTON_GRID_HORIZ_PADDING * buttons.size();", "}"),
 ("carousel_fast", "CarouselComponent.cpp", 76, 89, "int value = mCursor;", "return value;"),
 ("ilist_scroll", "IList.h", 381, 406, "int cursor = mCursor + amt;", "}"),
 ("textlist_range", "TextListComponent.h", 262, 269, "float entrySize = getRowHeight();", "listCutoff = size();"),
 ("textlist_camera", "TextListComponent.h", 593, 607, "auto rowHeight = getRowHeight();", "mCameraOffset = 0;"),
 ("scroll_defines", "ScrollableContainer.cpp", 6, 8, "#define AUTO_SCROLL_RESET_DELAY 6000", "#define AUTO_SCROLL_SPEED 150"),
 ("scroll_update", "ScrollableContainer.cpp", 64, 104, "if(mAutoScrollSpeed != 0)", "}"),
 ("scroll_reset", "ScrollableContainer.cpp", 128, 131, "mScrollPos = Vector2f(0, 0);", "mAtEnd = false;"),
 ("help_map", "HelpComponent.cpp", 18, 33, "static const std::map<std::string, std::string> ICON_PATH_MAP", "};"),
 ("card_close", "AsyncNotificationComponent.cpp", 122, 122, "mCloseRequested.store(true, std::memory_order_release);", "mCloseRequested.store"),
 ("card_update", "AsyncNotificationComponent.cpp", 268, 283, "if (!mClosing && mCloseRequested.load(std::memory_order_acquire))", "mFadeTime += deltaTime;"),
 ("card_update_full", "AsyncNotificationComponent.cpp", 265, 314, "GuiComponent::update(deltaTime);", "setOpacity((unsigned char)alpha);"),
 ("card_choose", "AsyncNotificationComponent.cpp", 138, 147, "std::string AsyncNotificationComponent::chooseThatFits(", "}"),
 ("textedit_move", "TextEditComponent.cpp", 267, 281, "void TextEditComponent::moveCursor(int amt)", "}"),
 ("str_cursor", "es-core/src/utils/StringUtil.cpp", 278, 327, "size_t nextCursor(const std::string& _string, const size_t _cursor)", "} // moveCursor"),
 ("textedit_focuslost", "TextEditComponent.cpp", 44, 47, "mFocused = false;", "mWindow->postToUiThread([this, alive = std::weak_ptr<void>(mAlive)]() { if (alive.lock()) stopEditing(); });"),
 ("card_handle", "AsyncNotificationComponent.h", 53, 54, "using Handle = std::weak_ptr<AsyncNotificationComponent>;", "Handle handle() { return weak_from_this(); }"),
]
os.makedirs(OUT, exist_ok=True)
for old in os.listdir(OUT):  # nothing a spec no longer names survives into this build
    if old.startswith("x_") and old.endswith(".inc"):
        os.remove(os.path.join(OUT, old))
lines_of = {}
for name, f, a, b, first, last in SPECS:
    if f not in lines_of:
        lines_of[f] = subprocess.run(["git", "-C", W, "show", "%s:%s" % (PIN, where(f))], capture_output=True, check=True).stdout.decode("latin-1").split("\n")
    L = lines_of[f]
    if (first and first not in L[a - 1]) or last not in L[b - 1]:
        print("t34-extract: %s:%d-%d no longer holds %r ... %r" % (f, a, b, first, last), file=sys.stderr); sys.exit(1)
specs_ok = []
for name, f, a, b, first, last in SPECS:
    L = lines_of[f]
    body = "\n".join(L[a - 1:b])
    open(os.path.join(OUT, "x_%s.inc" % name), "w").write("// lifted from %s:%d-%d at %s, verbatim\n#line %d \"%s\"\n%s\n" % (where(f), a, b, PIN[:10], a, f, body))
    specs_ok.append("%s %s:%d-%d" % (name, f, a, b))
print("t34-extract: %d extracts, each holding its first and last line: %s" % (len(SPECS), "; ".join(specs_ok)))

"""02 § The constants (#681): each house value with its one definition and every
reader in the 80 at the pin (definitions asserted once each; readers generated),
the frame that shows it, the second BUTTON_GRID_HORIZ_PADDING in T35's keyboard
popup against MenuComponent.cpp's claim, and each pixel constant with its share
of a 640 and a 1920 panel (each cited line asserted to hold its code).
    t34-constants.py <ES worktree> [paths file]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import COMP, die, show, paths

W = sys.argv[1]
files = paths(sys.argv[2] if len(sys.argv) > 2 else None)
G02 = "G-02 `CANNOT` in the window (the RETURN post, comment 6531938082): the card needs a startup sync, and the guest had no remote and no network under `restrict=on` -- a harness no, not a physical one; moved to the integration window"
HOUSE = [  # (name, defining file, must hold, value, frame at 640x480 and 1280x800, disposition)
 ("BUTTON_GRID_HORIZ_PADDING", "MenuComponent.cpp", "getScreenWidth()*0.022", "0.022 W (14.08 px at 640, 28.16 at 1280)", "G-03 (640), G-11 (1280): the gap between YES's and NO's nine-patch edges, read in the frame's columns", "D-UI-012; L-04 (a bar wider than its cell overhangs: 3.26), L-05 (the second copy, below)"),
 ("BUTTON_GRID_VERT_PADDING", "MenuComponent.cpp", "getScreenHeight()*0.0296296", "0.0296 H (14.2 px at 480)", "G-03", "upstream's; recorded"),
 ("NOTIFICATION_OPACITY", "AsyncNotificationComponent.cpp", "NOTIFICATION_OPACITY  255", "255", "%s; there, a pixel inside the card over the game art equals the panel colour, not a blend" % G02, "D-UI-016; sound"),
 ("DIMMED_ALPHA", "ComponentList.h", "DIMMED_ALPHA = 0x50", "0x50 of 0xFF", "G-04: the unconfigured rows' text against the selectable rows' over one panel", "#182's mechanism (`dimmed()` h `:26`, applied in each element's own `setColor`); 3.25"),
 ("TOTAL_HORIZONTAL_PADDING_PX", "ComponentList.cpp", "TOTAL_HORIZONTAL_PADDING_PX 20", "20 px (10 a side)", "G-04 (640), G-11 (1280): the row inset", "L-06: upstream's pixel constant the fork exported through `rowInset()` to two pages; a screen fraction is the pause's"),
 ("ICON_TEXT_SPACING", "HelpComponent.cpp", "getScreenWidth() * 0.0042f", "0.0042 W (2.7 px at 640)", "G-03, G-04, G-11: the help bar", "upstream's; sound"),
 ("ENTRY_SPACING", "HelpComponent.cpp", "ICON_TEXT_SPACING * 2.0f", "0.0084 W", "the same", "upstream's; the last entry's trailing spacer 0 (fork `7dc8bf373`, #210)"),
]
CARD = [("AsyncNotificationComponent.cpp", 64, "getScreenWidth() * 0.9f", "the card's width, `max(sizeText(30 chars), 0.9 W)` (`:63-65`)", G02 + "; there, edges at x 32 and x 608 at 640 (0.9 W centred); L-19: the measured floor never binds on a panel 640 or wider, dead text"),
        ("AsyncNotificationComponent.cpp", 112, "getScreenWidth() * 0.5f - mSize.x() * 0.5f", "the card centred at the top (`:112-113`); `Window::renderAsyncNotifications` re-applies the position every frame (`Window.cpp:1183`, `:1192`, T35's, cited)", G02)]
PIXEL = [  # (file, line, must hold, px, axis, what it sizes, disposition)
 ("ComponentList.cpp", 11, "20", 20, "w", "every row's horizontal inset", "L-06; read by two fork pages through `rowInset()`; S3 `db12b1598` (#1320): `ROW_INSET_FRACTION 0.015625`, PL-15's case PASS after (10 at 640, 20 at 1280), FAIL before"),
 ("TextEditComponent.cpp", 8, "10", 10, "w", "the text field's horizontal padding", "upstream's; outside the lanes unless a fork page reads it (the Wi-Fi and cloud key fields do, through the popups, T35's)"),
 ("TextEditComponent.cpp", 9, "2", 2, "h", "the text field's vertical padding", "as `:8`"),
 ("TextEditComponent.cpp", 31, "4096", 4096, "w", "the field's initial width, replaced by its owner's layout", "harmless: a placeholder width"),
 ("ButtonComponent.cpp", 10, "Math::max(12", 12, "w", "a button's text padding floor, `max(12, 0.014 W)`: the 12 wins below 857 px", "upstream's; G-03's bar at 640 is built on it"),
 ("GridTileComponent.cpp", 56, "16.0f", 16, "w", "a grid tile's default padding", "upstream's; G-08 if a grid theme exists"),
 ("GridTileComponent.h", 148, "16, 16", 16, "w", "a tile frame's corner size", "upstream's"),
 ("MenuComponent.cpp", 167, "setSize(10, 0)", 10, "w", "the spacer before a row's right-hand component", "upstream's"),
 ("MenuComponent.cpp", 192, "setSize(10, 0)", 10, "w", "the same, the second builder", "upstream's"),
 ("VideoVlcComponent.cpp", 782, "400, 300", 400, "w", "a video's default max size", "upstream surface outside the lanes; recorded"),
 ("NinePatchComponent.cpp", 177, "margin = 50", 50, "w", "the post-process shader's margin", "upstream's; recorded"),
 ("AsyncNotificationComponent.cpp", 94, "Vector2f(-32, -32)", 32, "w", "the card's nine-patch corner (`fitTo(..., -32, -32)`)", "the corner of every framed surface; outside a fraction by design (the frame image's corner)"),
 ("MenuComponent.cpp", 453, "Vector2f(-32, -32)", 32, "w", "the menu's background corner", "as above"),
 ("VolumeInfoComponent.cpp", 45, "Vector2f(-32, -32)", 32, "w", "the volume overlay's corner", "as above"),
 ("TextEditComponent.cpp", 53, "-32 - TEXT_PADDING_VERT", 32, "w", "the text field's frame corner (`-34, -32 - 2`)", "as above"),
]
defs, readers = {}, {}
for f in files:
    for n, line in enumerate(show(W, f).split("\n"), 1):
        code = line.split("//")[0]
        for name, df, must, *_ in HOUSE:
            if re.search(r"\b%s\b" % name, code):
                if re.search(r"#define\s+%s\b|\b%s\s*=" % (name, name), code):
                    defs.setdefault(name, []).append("%s:%d" % (f[len(COMP):], n))
                else:
                    readers.setdefault(name, []).append("%s:%d" % (f[len(COMP):], n))
for name, df, must, *_ in HOUSE:
    d = defs.get(name, [])
    if len(d) != 1 or not d[0].startswith(df + ":"):
        die("%s defined at %s, expected once in %s" % (name, d, df))
    n = int(d[0].split(":")[1])
    if must not in show(W, COMP + df).split("\n")[n - 1]:
        die("%s no longer holds %r" % (d[0], must))
kb = show(W, "es-core/src/guis/GuiTextEditPopupKeyboard.cpp").split("\n")
if "BUTTON_GRID_HORIZ_PADDING" not in kb[13] or "0.0052083333" not in kb[13]:
    die("GuiTextEditPopupKeyboard.cpp:14 no longer holds the second copy")
claim = show(W, COMP + "MenuComponent.cpp").split("\n")
if not any("one place" in claim[i] for i in range(6, 13)):
    die("MenuComponent.cpp:7-13 no longer carries the one-place claim")
for f, n, must, *_ in [(c[0], c[1], c[2]) for c in CARD] + [(p[0], p[1], p[2]) for p in PIXEL]:
    if not must or must not in show(W, COMP + f).split("\n")[n - 1]:
        die("%s:%d no longer holds %r" % (f, n, must))
MEASURED = {  # the window's readings (`guest-cycle/`, the RETURN post), `image`
 "BUTTON_GRID_HORIZ_PADDING": "guest (`image`): 14 px at 640x480 (panel colour x 313-326 between YES and NO, `g03-4-yesno.png`), 28 px at 1280x800 (x 626-653, `g11-2-yesno-1280.png`); the house value 14.08 and 28.16",
 "DIMMED_ALPHA": "guest (`image`): a dimmed label's brightest pixel 91 over the panel's 16 against a header's 255, `(91-16)/(255-16) = 0.314`, which is `0x50/0xFF` (`g04-1-cloud-hub-en.png`)",
 "NOTIFICATION_OPACITY": "`CANNOT` (G-02, the harness's reason in the frame cell); the integration window",
}
print("**The house values:**")
print()
print("| Value | Its one definition | Value at the panels | Every reader in the 80 | The frame that shows it | Disposition | proved |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for name, df, must, val, frame, disp in HOUSE:
    print("| `%s` | `%s` | %s | %s | %s | %s | %s |" % (name, defs[name][0], val, ", ".join("`%s`" % r for r in readers.get(name, [])) or "-", frame, disp, MEASURED.get(name, "tree")))
for f, n, must, what, disp in CARD:
    print("| the card's %s | `%s:%d` | 0.9 W | - | %s | D-UI-016; sound | `CANNOT` (G-02); the integration window |" % ("width" if n == 64 else "position", f, n, what + "; " + disp))
print("| `BUTTON_GRID_HORIZ_PADDING`, the second copy | `guis/GuiTextEditPopupKeyboard.cpp:14` (T35's) | 0.0052083333 W (3.3 px at 640) | that popup's key buttons (`:220`) | - | **L-05:** `MenuComponent.cpp:7-13` says the gap is defined in \"the one place\"; the keyboard popup keeps its own at the old value; recorded, not deleted (`engineering-practices.md:576`); the comment is this slice's, the popup T35's | tree |")
print()
print("**The pixel constants** (`es-native-ui.md:299`: fractions, never pixel constants; each with its share of a 640 and a 1920 panel's width):")
print()
RIGHT_ON = {  # a fixed value is right on exactly one panel (`es-native-ui.md` § Spacing); which one, or why none applies
 "ComponentList.cpp:11": "640 (10 px a side, 0.0156 W); since S3 a fraction, right on every panel",
 "TextEditComponent.cpp:8": "640, where 10 px is the 0.0156 W the row inset uses",
 "TextEditComponent.cpp:9": "none in particular: 2 px is the field's hairline, a few per cent of a line on every panel",
 "TextEditComponent.cpp:31": "none: a placeholder width its owner's layout replaces",
 "ButtonComponent.cpp:10": "857 (where 0.014 W reaches 12 px); below it the floor wins, above it the fraction",
 "GridTileComponent.cpp:56": "a theme's: the default padding a grid theme overrides; none ships on the image (G-08)",
 "GridTileComponent.h:148": "every panel: a frame image's corner, not a layout length",
 "MenuComponent.cpp:167": "640 (1.6% of the width), the smallest panel",
 "MenuComponent.cpp:192": "640, as `:167`",
 "VideoVlcComponent.cpp:782": "none on a handheld: a default the theme replaces",
 "NinePatchComponent.cpp:177": "every panel: the shader's margin around a frame, not a layout length",
 "AsyncNotificationComponent.cpp:94": "every panel: the frame image's corner",
 "MenuComponent.cpp:453": "every panel: the frame image's corner",
 "VolumeInfoComponent.cpp:45": "every panel: the frame image's corner",
 "TextEditComponent.cpp:53": "every panel: the frame image's corner",
}
print("| Site | Pixels | Share of 640 / 1920 | What it sizes | The panel it is right on | Disposition |")
print("| --- | ---: | --- | --- | --- | --- |")
for f, n, must, px, axis, what, disp in PIXEL:
    print("| `%s:%d` | %d | %.1f%% / %.1f%% | %s | %s | %s |" % (f, n, px, 100.0 * px / 640, 100.0 * px / 1920, what, RIGHT_ON["%s:%d" % (f, n)], disp))
if set(RIGHT_ON) != {"%s:%d" % (f, n) for f, n, *_ in PIXEL}:
    die("the right-on cells and the pixel rows disagree")
print()
print("Generated, asserted by `tools/t34-constants.py`: %d house values, each defined once in the 80 with %d readers in all; the card's width and position; the keyboard popup's second copy and `MenuComponent.cpp`'s one-place claim, both asserted present; %d pixel constants, each cited line asserted to hold its code." % (len(HOUSE), sum(len(v) for v in readers.values()), len(PIXEL)))

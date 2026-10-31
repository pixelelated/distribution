"""02 § The layouts (#681): every font-height read in the 80 at the pin (asserted
19; the brief's eight layout reads among the layout rows) with what it sizes and
the surface that shows it, and every size the read found computed from a size a
pass wrote or from a moving number, each cited line asserted to hold its code.
    t34-layouts.py <ES worktree> [paths file]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import COMP, die, show, paths

W = sys.argv[1]
files = paths(sys.argv[2] if len(sys.argv) > 2 else None)
MOVING = "`Font::getHeight` is the tallest ASCII glyph rasterised so far (`resources/Font.cpp:754-756`, `:420-421`, from 0 `:107`; T36's): a size taken before the font has drawn its tallest glyph is a few px short of one taken after (`es-code-traps.md:118`)"
FONT = {  # file:line -> (kind, what it sizes, the surface that shows it, disposition)
 "MultiLineMenuEntry.cpp:55": ("layout (constructor)", "a label-and-description row's text height (`naturalHeight`, `:50-56`)", "every cloud, achievements and settings row built on `MultiLineMenuEntry`; G-05's reopened page", "**L-02**: " + MOVING + "; a rasterise-first in the component or a record, the pause's"),
 "SwitchComponent.cpp:14": ("layout (constructor)", "the switch image's height (`getHeight(1.1f)`)", "every on/off row; G-04", "L-16: the moving number"),
 "OptionListComponent.h:255": ("layout (constructor)", "the option row's height", "every option row", "L-16"),
 "OptionListComponent.h:276": ("layout", "the option text's height on a resize", "every option row", "L-16"),
 "TextEditComponent.cpp:31": ("layout (constructor)", "the text field's height", "the key popups' fields (T35's pages)", "L-16"),
 "MenuComponent.cpp:393": ("layout", "the button bar's height when there is no bar yet", "every settings page's footer", "L-16"),
 "TextListComponent.h:613": ("layout", "a game-list row's height when no line count is themed", "the text game list", "L-16; upstream surface outside the lanes"),
 "TextListComponent.h:725": ("layout", "the game list's selector bar height", "the text game list", "L-16; upstream surface outside the lanes"),
 "HelpComponent.cpp:276": ("layout", "whether the help bar fits below its grid (`getHeight(1.5f)`)", "the help bar on every page", "the moving number; not in the brief's eight; recorded beside them"),
 "TextComponent.cpp:336": ("layout", "a single-line auto-height text's height", "every auto-height single-line label", "the moving number; not in the brief's eight (it is `TextComponent`'s own, L-17's file); recorded"),
 "TextComponent.cpp:176": ("render", "a line's height while drawing", "-", "per frame: re-read each draw"),
 "TextComponent.cpp:200": ("render", "the same, the second draw path", "-", "per frame"),
 "TextComponent.cpp:359": ("layout (decision)", "AUTO's one-line-or-wrap choice: `sy > getHeight * 1.8` where `sy` is the height `:336`/`:338` wrote", "every AUTO text", "the rule's shape (a decision from the size the auto pass wrote, and a moving number): stable at the pin (a text that wrapped to one line is drawn as one) -- 3.5's case confirms at stage C"),
 "TextComponent.cpp:432": ("layout (decision)", "the same decision in `buildTextCache`'s second form", "every AUTO text", "as `:359`"),
 "TextEditComponent.cpp:298": ("scroll", "whether the field must scroll down", "-", "per input"),
 "TextEditComponent.cpp:300": ("scroll", "the scroll offset", "-", "per input"),
 "TextEditComponent.cpp:364": ("render", "the cursor's height", "-", "per frame"),
 "TextEditComponent.cpp:370": ("render", "the cursor's position", "-", "per frame"),
 "TextEditComponent.cpp:377": ("layout (decision)", "whether the field is multi-line (`getSize().y() > getHeight * 1.25`)", "-", "a decision from the size its owner set; recorded"),
}
BRIEF8 = ["MultiLineMenuEntry.cpp:55", "SwitchComponent.cpp:14", "OptionListComponent.h:255", "OptionListComponent.h:276", "TextEditComponent.cpp:31", "MenuComponent.cpp:393", "TextListComponent.h:613", "TextListComponent.h:725"]
SIZE = [  # (file, line, must hold, what it computes and from what, the surface, disposition)
 ("MultiLineMenuEntry.cpp", 74, "(th * 0.9) / h", "the two rows' shares, `th*0.9/h` and `sh*1.1/h` of `h = th + sh` (`:72-75`), measured from the fonts since #241 (`7c7ffab43`), not from the cells", "every two-line row", "**L-03**: the shares sum to 1 only when `th == sh`: a taller Text font underfills, a taller TextSmall overflows by `0.1*(sh-th)/h`; upstream's formula moved whole into `layoutRows`; 3.4's `rowPercs(26, 20)` and `(20, 26)` FAIL at the pin; the fix (a pair that sums to 1) is the pause's"),
 ("MultiLineMenuEntry.cpp", 71, "mSubstring->getSize().y()", "in multi-line mode, the description's height read back from the text (`:71`)", "the multi-line rows (re-laid in `onSizeChanged`, `:121-136`)", "the rule's shape (a size the text's own auto pass wrote); stable while the width is: 3.4's 300 `setDescription` calls at stage C"),
 ("TextComponent.cpp", 338, "getSize().x()", "the auto height, wrapped at the full width `getSize().x()`", "every padded auto-height text that is not a `GuiMsgBox`", "**L-17** (#48's root): drawn at `mSize.x() - padding` (`:350`), so a wrap in that band paints a line the height never budgeted; 3.5's case; a 640x480 frame of a padded auto-height text; the reproducer for #585; the root fix the pause's (§ 1 f)"),
 ("TextComponent.cpp", 483, "getSize().x()", "the vertical marquee's text length, wrapped at the full width", "a vertically scrolling text with padding", "L-17's second site: the same full-width measure"),
 ("TextComponent.cpp", 486, "mPadding.y() - mPadding.y()", "the vertical marquee's limit, `mSize.y() - mPadding.y() - mPadding.y()`", "a vertically scrolling text with unequal top and bottom padding", "**3.6**: `:351` and `:428` subtract `.y()` and `.w()`; with padding (0,10,0,30) the limit is 20 px too large; a contained one-token fix under rule 6 and a #585 line"),
 ("MenuComponent.cpp", 396, "", "`updateSize`'s row-fit loop: rows added while `height + rowHeight < maxHeight` (`:396-424`)", "every settings page's height", "3.27: the strict `<` drops a row that fits exactly; a case at stage C"),
 ("ComponentList.cpp", 521, "mSize.x() - (row.selectable", "each element's width from the list's own width less the inset", "every row", "sound: from the parent's size, not the element's"),
 ("HelpComponent.cpp", 143, "", "the bar's grid width from the entries kept (`:143-152`), floored at 1", "the help bar", "sound since `7dc8bf373` (#210): measured before an entry is added; 3.16"),
 ("AsyncNotificationComponent.cpp", 63, "", "the card's width, `max(sizeText(30 chars), 0.9 W)`", "the card", "L-19: the floor never binds at 640 or wider; dead text, harmless"),
 ("ScrollableContainer.cpp", 69, "680.0f", "`widthMod = 680.0f / getSize().x()`, computed and never used", "-", "3.14: lint, recorded"),
]
got = {}
rx = re.compile(r"([Ff]ont\)?(->|\.)|[Ff]ont\(\)->)getHeight\(")
for f in files:
    for n, line in enumerate(show(W, f).split("\n"), 1):
        if rx.search(line.split("//")[0]):
            got["%s:%d" % (f[len(COMP):], n)] = True
if len(got) != 19:
    die("font-height reads: %d, expected 19" % len(got))
if set(got) != set(FONT):
    die("reads without a row: %s; rows without a read: %s" % (sorted(set(got) - set(FONT)), sorted(set(FONT) - set(got))))
for k in BRIEF8:
    if not FONT[k][0].startswith("layout"):
        die("%s is one of the brief's eight but not a layout row" % k)
for f, n, must, *_ in SIZE:
    line = show(W, COMP + f).split("\n")[n - 1]
    if must and must not in line:
        die("%s:%d no longer holds %r" % (f, n, must))
    if not must and not line.strip():
        die("%s:%d is blank" % (f, n))
print("**Every font-height read** (" + MOVING + "):")
print()
print("| Site | Kind | What it sizes | The surface that shows it | Disposition | proved |")
print("| --- | --- | --- | --- | --- | --- |")
for k in sorted(FONT, key=lambda k: (not FONT[k][0].startswith("layout"), k.split(":")[0], int(k.split(":")[1]))):
    kind, what, surf, disp = FONT[k]
    print("| `%s`%s | %s | %s | %s | %s | tree |" % (k, " (brief)" if k in BRIEF8 else "", kind, what, surf, disp))
print()
print("**Every size computed from a size a pass wrote, or measured at one width and drawn at another:**")
print()
print("| Site | What it computes, and from what | The surface | Disposition | proved |")
print("| --- | --- | --- | --- | --- |")
SE = {  # stage E: the size rows a stream fixed, by the pin's line
 "MultiLineMenuEntry.cpp:74": "S3 `db12b1598` (#1314): `th / h`, `sh / h`; 3.4 and PL-07's case PASS after, FAIL before",
 "TextComponent.cpp:338": "S3 `db12b1598` (#1315): measured at the drawn width; 3.5 PASS after, FAIL before",
 "TextComponent.cpp:483": "S3 `db12b1598` (#1315), as `:338`",
 "TextComponent.cpp:486": "S3 `db12b1598` (#1313): `mPadding.w()`; 3.6 PASS after, FAIL before",
}
for f, n, must, what, surf, disp in SIZE:
    print("| `%s:%d` | %s | %s | %s | %s |" % (f, n, what, surf, disp, SE.get("%s:%d" % (f, n), "tree")))
print()
print("Generated, asserted by `tools/t34-layouts.py`: %d font-height reads (%d layout, %d render or scroll), the brief's eight among the layout rows; %d size rows, each cited line asserted to hold its code or be non-blank." % (
    len(got), sum(1 for v in FONT.values() if v[0].startswith("layout")), sum(1 for v in FONT.values() if not v[0].startswith("layout")), len(SIZE)))

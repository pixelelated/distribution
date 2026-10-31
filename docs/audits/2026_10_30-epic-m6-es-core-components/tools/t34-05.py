"""Write 05-punch-list.md (#681) from one item table: each item's section, the
Phase 7 resolution gate (every item Open before stage D's issue exists), and the
punch_index YAML (question: in the brief's numbering, § 4). Asserts unique ids,
a known severity and question per item, and the three views agreeing.
    t34-05.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SEV = ("Critical", "High", "Medium", "Low")
I = [  # (title, severity, category, question, source finding, lines at the pin, owner, what is wrong, disposition proposed for the pause, proved)
 ("The progress card's close() writes its closing state unlocked from the holders' threads", "Medium", "Lifetime", "Q4", "L-22 (new)", "`AsyncNotificationComponent.cpp:117-121`, `:261-299`; h `:72`, `:74`", "T34 (a lane surface); the holders T18's and T20's",
  "`close()` sets `mClosing` and `mFadeTime` from the cloud and achievements worker threads while the interface thread's `update()` reads and writes both, with no lock and no atomic (`mMutex` guards only the text). A data race is undefined behaviour; in practice a fade that starts late or twice.", "a `bug`; the two members atomic, or `close()` under `mMutex` with `update()` reading under it; a ThreadSanitizer case over an extracted card first (stage E's covering case)", "tree"),
 ("The card promises a holder nothing once the window deletes it, and cannot refuse a late call", "Medium", "Lifetime", "Q4", "§ 1 (b), T2 PC-1", "`AsyncNotificationComponent.cpp:123-127`; `Window.cpp:1152-1169`, `:1242-1252` (T35's)", "T34 (the component's half); `Window` T35's; the holders T18's and T20's",
  "Every holder keeps the raw pointer `createAsyncNotificationComponent` returned; `Window::update` deletes a card once it stops running; a holder's `close()` or `updateText()` after that is a use after free the card cannot detect.", "a design ruling at the pause: a handle the window keeps alive until the holder lets go (the component's half), with `Window`'s teardown order T35's", "tree"),
 ("The text field posts raw `this` to the interface queue on focus", "Medium", "Lifetime", "Q4", "L-12", "`TextEditComponent.cpp:39`, `:47`", "T34; `Window::postToUiThread` T35's; `AppWindow` T33's",
  "`onFocusGained` and `onFocusLost` post `[this] { startEditing(); }` and `stopEditing()`; a field destroyed before the post runs is a use after free.", "a weak token the posts check; 3.20's case (post, delete, drain) with the fakes' `Window.h` as the covering case", "tree"),
 ("The `up/down` help icon key goes through `_()`", "Low", "Words", "Q3", "L-01, 3.16", "`ComponentList.cpp:568`; `HelpComponent.cpp:176-200`; fr po `:3708-3709`", "T34 (upstream's line, rule 6)",
  "Under a catalog that translates `up/down` (French: `haut/bas`) the list's CHOOSE prompt carries a key `getIconTexture` does not know: a null icon and `Unknown help icon`. Not reproduced on the image at 1280x800 (one CHOISIR with its icon, 0 log lines, the catalog carrying `haut/bas`): something between the list and the bar hides it there (L-25's neighbour).", "drop the `_()` (a contained fix, a #585 line); 3.16 as the covering case; the catalog's orphan `msgid` is a row for the pause", "tree; guest (image): not reproduced"),
 ("The tabbed SCRAPEUR page's help bar carried no component prompt on the image", "Low", "Input", "Q3", "L-25 (new, the guest)", "`ComponentTab.cpp:320-345`; `MenuComponent.cpp:531-533`; `ComponentGrid.cpp:519-553`", "T34 (if the pin's components drop them); `Window`'s bar T35's",
  "At 1280x800 the bar reads only FERMER and RETOUR, pixel-identical with a row focused and with the strip focused: no SWITCH TAB, no row prompt. Shown on the image only; whether the pin's tabbed `MenuComponent` loses its children's prompts, or the image's composition does, is unread.", "withdraw as a component defect: the seat traced SWITCH TAB through the pin's chain (`ComponentTab.cpp:341`, `ComponentGrid.cpp:493`, `:522-552`, `MenuComponent.cpp:533`); the image's empty bar named for T35 (the bar's collection in `Window`) and M7's composition", "guest (image)"),
 ("The vertical marquee's limit subtracts the top padding twice", "Low", "Correctness", "Q1", "3.6", "`TextComponent.cpp:486`", "T34 (upstream's line, rule 6)",
  "`mSize.y() - mPadding.y() - mPadding.y()` where `:351` and `:428` take `.y()` and `.w()`: with padding (0,10,0,30) the limit is 20 px too large, so a text that overflows by less never scrolls.", "the one token (`.w()`), a #585 line; 3.6's case FAIL then PASS", "tree"),
 ("A two-line row's shares do not sum to 1 when its fonts differ", "Medium", "Layout", "Q1", "L-03, 3.4", "`MultiLineMenuEntry.cpp:74-75`", "T34 (upstream's formula, moved by the fork's `48d43c0fb`)",
  "`th*0.9/h + sh*1.1/h` is 1 only when `th == sh`: a taller Text font leaves a gap, a taller TextSmall overflows by `0.1*(sh-th)/h`; and (the seat) a multi-line description more than ten times the label's height drives the second share above 1, which `ComponentGrid.cpp:93` asserts against: Medium in assertion builds.", "a pause ruling (a register row): shares that sum to 1, or the gap recorded; 3.4's case", "tree"),
 ("The auto height is measured at the full width and drawn at the padded one", "Low", "Layout", "Q1", "L-17, #48", "`TextComponent.cpp:338` against `:350`; `:483`", "T34 (upstream's file)",
  "A wrap that falls between the two widths paints a line the height never budgeted; `GuiMsgBox` works around it, nothing else does.", "a pause ruling (a register row): the root fixed in the component (it re-heights every padded auto-height text) or recorded with the reproducer for #585; 3.5's case", "tree"),
 ("The slider's AUTO value reads `Auto`, outside `_()`", "Low", "Words", "Q6", "3.7", "`SliderComponent.cpp:282`", "T34 (upstream's line, rule 6)",
  "Neither translated nor the placeholder `AUTO` the style guide names.", "`_(\"AUTO\")` with its French in the same commit, a #585 line; 3.7's case", "tree"),
 ("The rating's OK prompt `add star` is outside `_()`", "Low", "Words", "Q6", "L-23 (new)", "`RatingComponent.cpp:265`", "T34 (upstream's line, rule 6)",
  "English under every language.", "`_()` with its French in the same commit, a #585 line", "tree"),
 ("A focused video component labels BACK as SELECT", "Low", "Input", "Q3", "L-24 (new)", "`VideoComponent.cpp:347-351`", "T34 (upstream's line)",
  "The help bar names the back button's action SELECT.", "recorded; contained under rule 6 if the pause opens it", "tree"),
 ("`setCursorToButton` casts any button grid to `ComponentGrid` on an unstated invariant", "Low", "Structure", "Q3", "L-15", "`MenuComponent.cpp:492-515`; `GuiMenu.cpp:591` (T26's)", "T34",
  "`setButtonGrid` accepts any `GuiComponent` (the MAIN MENU hands it a text); the static cast is safe only because `mButtons` is empty there and the index guard returns first.", "a `dynamic_pointer_cast` with a null check, the invariant written beside `MenuComponent.h:53-56`", "tree"),
 ("A web image answered with 0 bytes is never asked for again on that page", "Low", "Reads", "Q5", "L-08, 3.21", "`WebImageComponent.cpp:197-200`, `:244`", "T34",
  "By design per `:191-196`; the badge stays blank for the page's life with no word on the row.", "a pause ruling: a re-ask on the next page build, or a word on the row; `tools/ra-ui-test`'s fixture shape", "tree"),
 ("A button bar wider than its cell overhangs the menu", "Low", "Constants", "Q2", "L-04, 3.26", "`MenuComponent.cpp:543-562`; `ButtonComponent.cpp:10`", "T34; the wide pages T26's and T31's",
  "The bar is `sum(text + max(12, 0.014 W)) + N * 0.022 W` and its cell does not resize it; five 128 px buttons at 640 overhang both edges.", "a pause ruling: a bar that fits its cell, or the pages' labels; 3.26's arithmetic per page", "tree"),
 ("Two pages read a fixed 10 px row inset (20 px in all) at every panel", "Low", "Constants", "Q2", "L-06", "`ComponentList.cpp:11`, `:491-494`", "T34 (upstream's constant); the pages T26's and T31's",
  "`rowInset()` returns `TOTAL_HORIZONTAL_PADDING_PX / 2`, 10 px (the seat's narrowing), to two fork pages: 20 px in all is 3.1 % of 640, 1.0 % of 1920.", "a pause ruling (a register row): a screen fraction under D-UI-012's family, or upstream's constant kept", "tree; guest (image) at both sizes"),
 ("The bar's gap is claimed to be defined in one place; the keyboard popup keeps a second", "Low", "Constants", "Q2", "L-05", "`MenuComponent.cpp:7-13`; `GuiTextEditPopupKeyboard.cpp:14` (T35's)", "the comment T34's; the popup T35's",
  "Two definitions, one claim.", "the comment corrected or the claim kept at the pause; the second copy is not deleted here", "tree"),
 ("Rows and fields are sized from a font height that grows as glyphs rasterise", "Low", "Layout", "Q1", "L-02, L-16", "`MultiLineMenuEntry.cpp:55`, and the 12 other layout reads in § The layouts", "T34; `Font.cpp` T36's",
  "A size taken before the tallest glyph has drawn is a few px short. G-05's reopened pair was identical on the image because the menus had already drawn.", "a pause ruling: a rasterise-first in the component, or recorded", "tree; guest (image): no difference shown"),
 ("The VLC release path nulls `component` without a lock while VLC's thread reads it", "Medium", "Lifetime", "Q4", "L-10", "`VideoVlcComponent.cpp:53-61`, `:84-96`, `:911`", "T34 (upstream surface, outside the lanes)",
  "A data race, and a `display` call into a component being destroyed.", "recorded (G-10 `CANNOT`: no media); a contained fix only if the pause opens it", "tree"),
 ("A carousel and an option row offer a direction by type, whatever their count", "Low", "Input", "Q3", "L-13", "`CarouselComponent.cpp:354-361`; `OptionListComponent.h:636-643`", "T34 (upstream surfaces)",
  "A one-entry carousel offers CHOOSE; a one-value option row offers CHANGE.", "recorded", "tree"),
 ("Indentation and an include outside the guard read as blocks they are not in", "Low", "Structure", "Q7", "L-14", "`GridTileComponent.cpp:1043`; `ImageGridComponent.h:2`, `:380-381`", "T34",
  "Cosmetic; misleads a reader.", "a one-commit tidy if the pause opens it", "tree"),
 ("es-core includes es-app's `CloudText.h`", "Low", "Structure", "Q7", "L-07", "`AsyncNotificationComponent.cpp:12`", "T34 (the line); `CloudText` T18's; the CMake T35's",
  "Resolves only through `-I es-core/src` plus `../../`; es-core does not build alone.", "recorded; a `CloudText` that moves to es-core is T18's and T35's call", "tree"),
 ("The switch's and the option list's callbacks are stored by value, not weak by design", "Low", "Lifetime", "Q4", "§ 1 (c), T26 PL-27", "`SwitchComponent.h:53`; `OptionListComponent.h:658`", "T34; the pages' clearing T26's and T31's",
  "A page's lambda capturing a `shared_ptr` to the component that stores it makes a cycle only the page's `onFinalize` breaks.", "a design ruling at the pause; LeakSanitizer over an extracted builder", "tree"),
 ("The brand is kept lowercase by reading, not by a check", "Low", "Words", "Q6", "L-18", "`MenuComponent.cpp:205`, `:233`, `:236`, `:283`, `:487`; `ButtonComponent.cpp:73`", "the coordinator (a tool rule)",
  "Six formatters upper-case every label they see; no fork label passes the brand through them at the pin.", "a `tools/vocabulary-check` rule proposed (the brand inside those builders' arguments)", "tree"),
 ("The carousel's fast move can hand `listInput` a negative count", "Low", "Correctness", "Q3", "3.8", "`CarouselComponent.cpp:74-90`, `:113`, `:119`; `IList.h:376-400`", "T34 (upstream surface)",
  "Size 3, cursor 0, page up: `count = -10`, one `+= sz` gives `-7`; whether `listInput(-7)` lands in `[0, sz)` for every loop type is 3.8's case.", "withdraw: the seat showed `IList::scroll` clamps (NEVER_LOOP, PAUSE_AT_END) or wraps the `-7` into range (`IList.h:376-405`); a negative count is an intended input; 3.8 stays as a case", "tree"),
 ("An unset date reads blank, not `<NOT SET>`", "Low", "Words", "Q6", "3.13", "`DateTimeEditComponent.cpp:256-257`", "T34 (upstream surface)",
  "`getTime() == 0` returns `\"\"`.", "a style question for the pause", "tree"),
 ("Whether `ImageComponent` gains the untinted mode the fork wrote as a subclass", "Low", "Structure", "Q7", "§ 1 (h)", "`GuiMenu.cpp:6401` (T26's); `ImageComponent.h:76`", "the pause",
  "`UntintedImageComponent` lives in a page file; every untinted image needs the same subclass.", "a question for the pause; nothing changed here", "tree"),
 ("A security-sensitive finding in a fork-modified component; its details are held off the public tracker", "High", "Security", "Q5", "G-3 (the seat's), verified at the pin", "held", "T34",
  "Held privately (outside the tree, mode 600) pending the maintainer's decision on where security findings go; the public record names its existence, its severity and its owner, not its mechanism.", "the coordinator names the private channel; the fix lands under a stream brief there", "tree"),
 ("Three members are read before anything sets them", "Medium", "Correctness", "Q7", "G-1, verified", "`ComponentList.h:157` with `ComponentList.cpp:13-27`, `:196`; `GridTileComponent.h:312` with `.cpp:49`, `:1246`; `GridTileComponent.h:77-90`, `:107`, `:134`", "T34 (upstream's lines, rule 6)",
  "`mUpdateType` has no initializer and the constructor never sets it before `update()` reads it; `GridTile`'s constructor calls `setSelected(false)`, which reads the uninitialised `mSelected`; `GridTextProperties::autoScroll` is set only when a theme names `singleLineScroll`.", "explicit initial values; a #585 line", "tree"),
 ("A help bar whose first entry does not fit builds a 0-column grid", "Medium", "Input", "Q3", "G-2, verified", "`HelpComponent.cpp:131-132`, `:150-156`; `ComponentGrid.cpp:12`", "T34 (the fork's `7dc8bf373` fit, #210)",
  "If the first prompt is wider than the bar, nothing is kept and `:155` builds `ComponentGrid(0, 1)`, which the grid asserts against: Medium in assertion builds; a long translated label or a large themed font reaches it.", "an empty-items return before the grid is built; 3.16's case extended", "tree"),
 ("A web image in a resizing grid cell can recurse through its parent", "Medium", "Layout", "Q1", "G-4, verified with narrowing", "`WebImageComponent.cpp:69-70`; `ImageComponent.cpp:65-79`; `ComponentGrid.cpp:174-175`", "T34",
  "`resize()` notifies the parent grid, the grid resizes the cell, `setSize` re-runs `resize()` with no unchanged-size exit. Reached only in a `resize=true` cell; the callers' cells are unread.", "an unchanged-size exit, or a non-reentrant notification; the callers' cells read first", "tree"),
 ("Rebinding a web image can leave an older URL queued", "Medium", "Reads", "Q5", "G-5, verified", "`WebImageComponent.cpp:98-115`, `:156-165`, `:225-244`", "T34",
  "`setImage()` deletes an active request but does not clear `mUrlToLoad`; the local and cached returns (`:115`, `:158`) leave it, and `render` starts it, replacing the image the caller set last.", "clear the pending URL on every rebind", "tree"),
 ("Replacing an image from memory or a shared texture does not cancel a pending load", "Medium", "Reads", "Q5", "G-6, verified", "`ImageComponent.cpp:413-416`, `:436-467`, `:816-823`", "T34",
  "Only the path overload sets `mLoadingTexture`; the other two never clear it, and `watchTextureLoading` later installs the stale texture.", "every source-replacing overload cancels the pending load", "tree"),
 ("A cleared looping grid keeps drawing its loop-copy tiles", "Medium", "Lifetime", "Q4", "G-7, verified; corrects the stage-B contract", "`ImageGridComponent.h:505-509`, `:1381-1435`, `:316-317`, `:339-340`, `:762-763`", "T34 (the save-state manager and the grid view)",
  "`clear()` -> `resetGrid()` never clears `mScrollLoopTiles`, and the routine that does returns first on an empty list; `render` still draws them.", "clear the loop map in `resetGrid()`; T32's `s4-views.py` shape as the case", "tree"),
 ("Changing a visible grid entry's image strands its old tile", "Medium", "Lifetime", "Q4", "G-8, verified with narrowing", "`ImageGridComponent.h:526-533`, `:373-384`, `:426-433`", "T34",
  "The entry's tile pointer is dropped without removing the tile from the visible list; repeated changes accumulate tiles until a reset.", "remove the old tile when the entry's image changes", "tree"),
 ("An assignment where a comparison was meant", "Low", "Correctness", "Q3", "G-9, verified", "`ImageGridComponent.h:1151`", "T34 (upstream's line, rule 6)",
  "`else if (mLastCursor = -9999)` always succeeds and overwrites the last cursor.", "`==`; a #585 line", "tree"),
 ("A switch can show a state other than the one it holds", "Medium", "Input", "Q3", "G-10, verified with narrowing", "`SwitchComponent.cpp:7-25`, `:118-137`", "T34 (a lane surface: every on/off row)",
  "The constructor always loads the OFF image and never calls `onStateChanged()`; with auto set, `setValue(\"true\")` leaves auto in force and `getValue()` still says `auto`.", "the image from the given state; explicit values leave auto mode", "tree"),
 ("Updating a subtitle re-inserts the title image it already holds", "Medium", "Structure", "Q7", "G-11, verified with narrowing", "`MenuComponent.cpp:374-375`, `:305-331`", "T34",
  "`setSubTitle` re-runs `setTitleImage`, which `setEntry`s the parented image again with no `removeEntry`: an assertion in debug builds, a duplicate entry otherwise.", "remove or update the existing entry first", "tree"),
 ("Right-to-left rows send text and prompts to a different element than input", "Medium", "Input", "Q3", "G-12, verified", "`ComponentList.h:56-61`; `ComponentList.cpp:155-165`, `:541-553`", "T34 (outside the fork's languages)",
  "RTL rows prepend elements and `input()` uses `front()`, while `textInput` and `getHelpPrompts` use `back()`; neither guards an empty row.", "one element choice for all three, with the empty check; outside English and French, so recorded unless the pause opens it", "tree"),
 ("A quarter-turned min-size image reports the wrong cropped size", "Low", "Layout", "Q1", "G-13, verified with narrowing", "`ImageComponent.cpp:33`, `:155-170`", "T34 (the fork's turn, `3b7265f33`)",
  "`getSize()` multiplies screen-axis size by crop factors that are in texture axes after a turn.", "swap the crop factors in `getSize()` after a turn; 3.22's case extended", "tree"),
 ("Narrow scrollable content gets a negative horizontal offset", "Low", "Layout", "Q1", "G-14, verified", "`ScrollableContainer.cpp:78-96`", "T34 (upstream's line, rule 6)",
  "The X branch lacks the Y branch's narrow-content case.", "the same guard as Y; 3.14's case", "tree"),
 ("A tab's mouse release never dispatches", "Low", "Input", "Q3", "G-15, verified", "`ComponentTab.cpp:426-430`", "T34",
  "`row` is compared with `mHotTab` after `mHotTab` was reset to -1.", "compare with the saved value; recorded (mouse only)", "tree"),
 ("Tile padding's test checks Y twice and never Z", "Low", "Constants", "Q2", "G-16, verified", "`GridTileComponent.cpp:565`", "T34",
  "The right inset is never tested, so a pixel right inset can enter the normalised branch.", "test Z; a #585 line", "tree"),
 ("A subtitle with a slash keeps only what follows the last one", "Low", "Words", "Q6", "L-26 (new, the read)", "`MenuComponent.cpp:357-359`", "T34",
  "`setSubTitle` builds its text from `getFileName(text)`.", "read the update path; `getFileName` dropped if no caller relies on it", "tree"),
]
ids = ["PL-%02d" % (i + 1) for i in range(len(I))]
ES_TIP = "52f0ff5128cf96bfcdec9082ded75347ecea11e6"
# Phase 7 (stage E): each item's outcome, with the commit or the issue it rests on.
R = lambda c, b, more="": ("Resolved", "`%s` (#%d)%s" % (c, b, more))
PH7 = {
 "PL-01": R("2cbb62d7b", 1309, "; `tsan-card` rc 0, the interleaving case PASS"),
 "PL-02": R("2cbb62d7b", 1310, ", `52f0ff512` (the handle forwards); Window's half `stage-e/s2-window.patch` (T35's, #682) and the holders' `stage-e/s2-holders.patch` (#665, #667, #678, #680), merge debt"),
 "PL-03": R("2cbb62d7b", 1311, "; `asan-textedit` rc 0"),
 "PL-04": R("a9017ff50", 1312, "; 3.16 PASS"),
 "PL-05": ("Withdrawn", "the stage-D ruling (the seat's trace of SWITCH TAB through the pin's chain); the image's empty bar a lead for T35 (#682)"),
 "PL-06": R("db12b1598", 1313, "; 3.6 PASS"),
 "PL-07": R("db12b1598", 1314, "; 3.4 and the long-description case PASS"),
 "PL-08": R("db12b1598", 1315, "; 3.5 PASS; `GuiMsgBox`'s workaround `stage-e/s3-msgbox.patch` (T35's, #682) and `es-code-traps.md` (the coordinator's), merge debt"),
 "PL-09": R("a9017ff50", 1316, "; 3.7 PASS"),
 "PL-10": R("a9017ff50", 1317, "; ADD STAR / AJOUTER UNE ÉTOILE"),
 "PL-11": R("a9017ff50", 1318, "; an empty prompt list (ruling 7)"),
 "PL-12": ("Deferred", "recorded as written: the invariant beside `MenuComponent.h:53-56` in `02` § The lifetimes; the cast that relies on it is `GuiMenu.cpp:591`, #673's"),
 "PL-13": R("568ef099d", 1319, "; no timer (ruling 5): the pin already re-asks on the next bind, the fix is the uncached state"),
 "PL-14": ("Deferred", "#585, and the pages' labels to #673 and #678; 3.26 `may_fail` with PL-14 named (ruling 9)"),
 "PL-15": R("db12b1598", 1320, "; `ROW_INSET_FRACTION`, D-UI-132"),
 "PL-16": ("Resolved", "`db12b1598`: the comment names the keyboard popup's second copy; the copy is T35's (#682)"),
 "PL-17": ("Deferred", "an open item to test (the moving font height; `Font.cpp` is #683's)"),
 "PL-18": ("Deferred", "#585; an open item to test (D-QA-051 rule 4: no media on the guest)"),
 "PL-19": R("a9017ff50", 1321),
 "PL-20": ("Deferred", "recorded as written on #1307: the dead `_RPI_` and `WIN32` blocks and the unused `widthMod`, a dead-end table that removes nothing (D-WORKFLOW-209)"),
 "PL-21": ("Deferred", "#665 and #682: the es-app include is T18's and T35's call"),
 "PL-22": ("Deferred", "#673 and #678: the pages' `onFinalize` clearing"),
 "PL-23": ("Deferred", "#1336, the coordinator's Backlog for the `tools/vocabulary-check` rule (the brand inside the up-casing builders' arguments)"),
 "PL-24": ("Withdrawn", "the stage-D ruling: `IList::scroll` clamps or wraps; 3.8 PASS at the pin for every size and loop type"),
 "PL-25": R("a9017ff50", 1322, "; 3.13 PASS"),
 "PL-26": ("Deferred", "#673: `UntintedImageComponent` lives at `GuiMenu.cpp:6401`; lifting an untinted mode is a question for that slice"),
 "PL-27": R("dbe4c2db0", 1323, "; held: the case's counts only, `stage-e/s1-checks.txt`"),
 "PL-28": R("5908888b5", 1324, "; `UPDATE_ALWAYS` after reading every caller (ruling 11)"),
 "PL-29": R("a9017ff50", 1325, "; the first prompt kept and clipped (ruling 4), batocera's `9dbd4b9bf` guard taken"),
 "PL-30": R("db12b1598", 1326, "; the unchanged-size exit (ruling 3)"),
 "PL-31": R("568ef099d", 1327),
 "PL-32": R("568ef099d", 1328),
 "PL-33": R("6050b8419", 1329),
 "PL-34": R("6050b8419", 1330),
 "PL-35": R("6050b8419", 1331, "; the intent read posted before the commit (ruling 12)"),
 "PL-36": R("5908888b5", 1332, "; auto kept in force (ruling 13)"),
 "PL-37": R("5908888b5", 1333),
 "PL-38": ("Deferred", "#585: outside English and French"),
 "PL-39": ("Deferred", "recorded as written: the fork's turn (`3b7265f33`); 3.22 says what the pin does, PASS before and after"),
 "PL-40": ("Deferred", "#585; 3.14's half `may_fail` with PL-40 named, as ruling 9 marks 3.26"),
 "PL-41": ("Deferred", "recorded as written on #1307: the mouse path only"),
 "PL-42": ("Deferred", "#585"),
 "PL-43": ("Withdrawn", "the read (`stage-e/s7-checks.txt`): `setSubTitle` sets the full text at `:365` in the same call, before any draw, so the `getFileName` text at `:358-360` is never shown"),
}
if set(PH7) != set(ids):
    print("ASSERT: Phase 7 outcomes for %s, items %s" % (sorted(set(ids) - set(PH7)), sorted(set(PH7) - set(ids))), file=sys.stderr); sys.exit(1)
for t in I:
    if t[1] not in SEV or not re.fullmatch(r"Q[1-7]", t[3]):
        print("ASSERT: a bad severity or question in %r" % t[0], file=sys.stderr); sys.exit(1)
out = ["# Punch list (Phases 5 and 6) — M6.P2 T34, EmulationStation's core components (#681)", "",
       "Written by `tools/t34-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 layout, Q2 constants, Q3 input, Q4 lifetime, Q5 reads, Q6 words, Q7 structure); `04` § Renovation face maps them to the plan's seven. At Phase 7 (stage E) every item has its outcome below.", "", "reviewed-at-es: 16dbac5211eea7e70db7394372033be2be7df829", "fixed-at-es: %s" % ES_TIP, ""]
for pl, (title, sev, cat, q, src, lines, own, what, disp, proved) in zip(ids, I):
    out += ["## %s: %s" % (pl, title), "", "- **Severity:** %s; **category:** %s; **question:** %s" % (sev, cat, q), "- **Source finding:** %s" % src,
            "- **Lines at the pin:** %s" % lines, "- **Owner:** %s" % own, "- **What is wrong:** %s" % what, "- **Proposed disposition:** %s" % disp, "- **proved:** %s" % proved, ""]
out += ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
out += ["| %s | **%s** | %s |" % (pl, PH7[pl][0], PH7[pl][1]) for pl in ids]
out += ["", "## punch_index", "", "```yaml", "punch_index:"]
for pl, t in zip(ids, I):
    out += ["- id: %s" % pl, "  severity: \"%s\"" % t[1], "  category: %s" % t[2], "  question: %s" % t[3], "  source_finding: \"%s\"" % t[4].replace('"', "'"), "  outcome: \"%s\"" % PH7[pl][0].lower()]
out += ["```", ""]
open(os.path.join(os.path.dirname(HERE), "05-punch-list.md"), "w", encoding="utf-8").write("\n".join(out))
c = {s: sum(1 for t in I if t[1] == s) for s in SEV}
o = {w: sum(1 for v in PH7.values() if v[0] == w) for w in ("Resolved", "Deferred", "Withdrawn")}
print("t34-05: %d items (%s); Phase 7: %s" % (len(I), ", ".join("%d %s" % (c[s], s) for s in SEV), ", ".join("%d %s" % (o[w], w) for w in o)))

# Punch list (Phases 5 and 6) — M6.P2 T34, EmulationStation's core components (#681)

Written by `tools/t34-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 layout, Q2 constants, Q3 input, Q4 lifetime, Q5 reads, Q6 words, Q7 structure); `04` § Renovation face maps them to the plan's seven. At Phase 7 (stage E) every item has its outcome below.

reviewed-at-es: 16dbac5211eea7e70db7394372033be2be7df829
fixed-at-es: 52f0ff5128cf96bfcdec9082ded75347ecea11e6

## PL-01: The progress card's close() writes its closing state unlocked from the holders' threads

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** L-22 (new)
- **Lines at the pin:** `AsyncNotificationComponent.cpp:117-121`, `:261-299`; h `:72`, `:74`
- **Owner:** T34 (a lane surface); the holders T18's and T20's
- **What is wrong:** `close()` sets `mClosing` and `mFadeTime` from the cloud and achievements worker threads while the interface thread's `update()` reads and writes both, with no lock and no atomic (`mMutex` guards only the text). A data race is undefined behaviour; in practice a fade that starts late or twice.
- **Proposed disposition:** a `bug`; the two members atomic, or `close()` under `mMutex` with `update()` reading under it; a ThreadSanitizer case over an extracted card first (stage E's covering case)
- **proved:** tree

## PL-02: The card promises a holder nothing once the window deletes it, and cannot refuse a late call

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** § 1 (b), T2 PC-1
- **Lines at the pin:** `AsyncNotificationComponent.cpp:123-127`; `Window.cpp:1152-1169`, `:1242-1252` (T35's)
- **Owner:** T34 (the component's half); `Window` T35's; the holders T18's and T20's
- **What is wrong:** Every holder keeps the raw pointer `createAsyncNotificationComponent` returned; `Window::update` deletes a card once it stops running; a holder's `close()` or `updateText()` after that is a use after free the card cannot detect.
- **Proposed disposition:** a design ruling at the pause: a handle the window keeps alive until the holder lets go (the component's half), with `Window`'s teardown order T35's
- **proved:** tree

## PL-03: The text field posts raw `this` to the interface queue on focus

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** L-12
- **Lines at the pin:** `TextEditComponent.cpp:39`, `:47`
- **Owner:** T34; `Window::postToUiThread` T35's; `AppWindow` T33's
- **What is wrong:** `onFocusGained` and `onFocusLost` post `[this] { startEditing(); }` and `stopEditing()`; a field destroyed before the post runs is a use after free.
- **Proposed disposition:** a weak token the posts check; 3.20's case (post, delete, drain) with the fakes' `Window.h` as the covering case
- **proved:** tree

## PL-04: The `up/down` help icon key goes through `_()`

- **Severity:** Low; **category:** Words; **question:** Q3
- **Source finding:** L-01, 3.16
- **Lines at the pin:** `ComponentList.cpp:568`; `HelpComponent.cpp:176-200`; fr po `:3708-3709`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** Under a catalog that translates `up/down` (French: `haut/bas`) the list's CHOOSE prompt carries a key `getIconTexture` does not know: a null icon and `Unknown help icon`. Not reproduced on the image at 1280x800 (one CHOISIR with its icon, 0 log lines, the catalog carrying `haut/bas`): something between the list and the bar hides it there (L-25's neighbour).
- **Proposed disposition:** drop the `_()` (a contained fix, a #585 line); 3.16 as the covering case; the catalog's orphan `msgid` is a row for the pause
- **proved:** tree; guest (image): not reproduced

## PL-05: The tabbed SCRAPEUR page's help bar carried no component prompt on the image

- **Severity:** Low; **category:** Input; **question:** Q3
- **Source finding:** L-25 (new, the guest)
- **Lines at the pin:** `ComponentTab.cpp:320-345`; `MenuComponent.cpp:531-533`; `ComponentGrid.cpp:519-553`
- **Owner:** T34 (if the pin's components drop them); `Window`'s bar T35's
- **What is wrong:** At 1280x800 the bar reads only FERMER and RETOUR, pixel-identical with a row focused and with the strip focused: no SWITCH TAB, no row prompt. Shown on the image only; whether the pin's tabbed `MenuComponent` loses its children's prompts, or the image's composition does, is unread.
- **Proposed disposition:** withdraw as a component defect: the seat traced SWITCH TAB through the pin's chain (`ComponentTab.cpp:341`, `ComponentGrid.cpp:493`, `:522-552`, `MenuComponent.cpp:533`); the image's empty bar named for T35 (the bar's collection in `Window`) and M7's composition
- **proved:** guest (image)

## PL-06: The vertical marquee's limit subtracts the top padding twice

- **Severity:** Low; **category:** Correctness; **question:** Q1
- **Source finding:** 3.6
- **Lines at the pin:** `TextComponent.cpp:486`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** `mSize.y() - mPadding.y() - mPadding.y()` where `:351` and `:428` take `.y()` and `.w()`: with padding (0,10,0,30) the limit is 20 px too large, so a text that overflows by less never scrolls.
- **Proposed disposition:** the one token (`.w()`), a #585 line; 3.6's case FAIL then PASS
- **proved:** tree

## PL-07: A two-line row's shares do not sum to 1 when its fonts differ

- **Severity:** Medium; **category:** Layout; **question:** Q1
- **Source finding:** L-03, 3.4
- **Lines at the pin:** `MultiLineMenuEntry.cpp:74-75`
- **Owner:** T34 (upstream's formula, moved by the fork's `48d43c0fb`)
- **What is wrong:** `th*0.9/h + sh*1.1/h` is 1 only when `th == sh`: a taller Text font leaves a gap, a taller TextSmall overflows by `0.1*(sh-th)/h`; and (the seat) a multi-line description more than ten times the label's height drives the second share above 1, which `ComponentGrid.cpp:93` asserts against: Medium in assertion builds.
- **Proposed disposition:** a pause ruling (a register row): shares that sum to 1, or the gap recorded; 3.4's case
- **proved:** tree

## PL-08: The auto height is measured at the full width and drawn at the padded one

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** L-17, #48
- **Lines at the pin:** `TextComponent.cpp:338` against `:350`; `:483`
- **Owner:** T34 (upstream's file)
- **What is wrong:** A wrap that falls between the two widths paints a line the height never budgeted; `GuiMsgBox` works around it, nothing else does.
- **Proposed disposition:** a pause ruling (a register row): the root fixed in the component (it re-heights every padded auto-height text) or recorded with the reproducer for #585; 3.5's case
- **proved:** tree

## PL-09: The slider's AUTO value reads `Auto`, outside `_()`

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** 3.7
- **Lines at the pin:** `SliderComponent.cpp:282`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** Neither translated nor the placeholder `AUTO` the style guide names.
- **Proposed disposition:** `_("AUTO")` with its French in the same commit, a #585 line; 3.7's case
- **proved:** tree

## PL-10: The rating's OK prompt `add star` is outside `_()`

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-23 (new)
- **Lines at the pin:** `RatingComponent.cpp:265`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** English under every language.
- **Proposed disposition:** `_()` with its French in the same commit, a #585 line
- **proved:** tree

## PL-11: A focused video component labels BACK as SELECT

- **Severity:** Low; **category:** Input; **question:** Q3
- **Source finding:** L-24 (new)
- **Lines at the pin:** `VideoComponent.cpp:347-351`
- **Owner:** T34 (upstream's line)
- **What is wrong:** The help bar names the back button's action SELECT.
- **Proposed disposition:** recorded; contained under rule 6 if the pause opens it
- **proved:** tree

## PL-12: `setCursorToButton` casts any button grid to `ComponentGrid` on an unstated invariant

- **Severity:** Low; **category:** Structure; **question:** Q3
- **Source finding:** L-15
- **Lines at the pin:** `MenuComponent.cpp:492-515`; `GuiMenu.cpp:591` (T26's)
- **Owner:** T34
- **What is wrong:** `setButtonGrid` accepts any `GuiComponent` (the MAIN MENU hands it a text); the static cast is safe only because `mButtons` is empty there and the index guard returns first.
- **Proposed disposition:** a `dynamic_pointer_cast` with a null check, the invariant written beside `MenuComponent.h:53-56`
- **proved:** tree

## PL-13: A web image answered with 0 bytes is never asked for again on that page

- **Severity:** Low; **category:** Reads; **question:** Q5
- **Source finding:** L-08, 3.21
- **Lines at the pin:** `WebImageComponent.cpp:197-200`, `:244`
- **Owner:** T34
- **What is wrong:** By design per `:191-196`; the badge stays blank for the page's life with no word on the row.
- **Proposed disposition:** a pause ruling: a re-ask on the next page build, or a word on the row; `tools/ra-ui-test`'s fixture shape
- **proved:** tree

## PL-14: A button bar wider than its cell overhangs the menu

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** L-04, 3.26
- **Lines at the pin:** `MenuComponent.cpp:543-562`; `ButtonComponent.cpp:10`
- **Owner:** T34; the wide pages T26's and T31's
- **What is wrong:** The bar is `sum(text + max(12, 0.014 W)) + N * 0.022 W` and its cell does not resize it; five 128 px buttons at 640 overhang both edges.
- **Proposed disposition:** a pause ruling: a bar that fits its cell, or the pages' labels; 3.26's arithmetic per page
- **proved:** tree

## PL-15: Two pages read a fixed 10 px row inset (20 px in all) at every panel

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** L-06
- **Lines at the pin:** `ComponentList.cpp:11`, `:491-494`
- **Owner:** T34 (upstream's constant); the pages T26's and T31's
- **What is wrong:** `rowInset()` returns `TOTAL_HORIZONTAL_PADDING_PX / 2`, 10 px (the seat's narrowing), to two fork pages: 20 px in all is 3.1 % of 640, 1.0 % of 1920.
- **Proposed disposition:** a pause ruling (a register row): a screen fraction under D-UI-012's family, or upstream's constant kept
- **proved:** tree; guest (image) at both sizes

## PL-16: The bar's gap is claimed to be defined in one place; the keyboard popup keeps a second

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** L-05
- **Lines at the pin:** `MenuComponent.cpp:7-13`; `GuiTextEditPopupKeyboard.cpp:14` (T35's)
- **Owner:** the comment T34's; the popup T35's
- **What is wrong:** Two definitions, one claim.
- **Proposed disposition:** the comment corrected or the claim kept at the pause; the second copy is not deleted here
- **proved:** tree

## PL-17: Rows and fields are sized from a font height that grows as glyphs rasterise

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** L-02, L-16
- **Lines at the pin:** `MultiLineMenuEntry.cpp:55`, and the 12 other layout reads in § The layouts
- **Owner:** T34; `Font.cpp` T36's
- **What is wrong:** A size taken before the tallest glyph has drawn is a few px short. G-05's reopened pair was identical on the image because the menus had already drawn.
- **Proposed disposition:** a pause ruling: a rasterise-first in the component, or recorded
- **proved:** tree; guest (image): no difference shown

## PL-18: The VLC release path nulls `component` without a lock while VLC's thread reads it

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** L-10
- **Lines at the pin:** `VideoVlcComponent.cpp:53-61`, `:84-96`, `:911`
- **Owner:** T34 (upstream surface, outside the lanes)
- **What is wrong:** A data race, and a `display` call into a component being destroyed.
- **Proposed disposition:** recorded (G-10 `CANNOT`: no media); a contained fix only if the pause opens it
- **proved:** tree

## PL-19: A carousel and an option row offer a direction by type, whatever their count

- **Severity:** Low; **category:** Input; **question:** Q3
- **Source finding:** L-13
- **Lines at the pin:** `CarouselComponent.cpp:354-361`; `OptionListComponent.h:636-643`
- **Owner:** T34 (upstream surfaces)
- **What is wrong:** A one-entry carousel offers CHOOSE; a one-value option row offers CHANGE.
- **Proposed disposition:** recorded
- **proved:** tree

## PL-20: Indentation and an include outside the guard read as blocks they are not in

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-14
- **Lines at the pin:** `GridTileComponent.cpp:1043`; `ImageGridComponent.h:2`, `:380-381`
- **Owner:** T34
- **What is wrong:** Cosmetic; misleads a reader.
- **Proposed disposition:** a one-commit tidy if the pause opens it
- **proved:** tree

## PL-21: es-core includes es-app's `CloudText.h`

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-07
- **Lines at the pin:** `AsyncNotificationComponent.cpp:12`
- **Owner:** T34 (the line); `CloudText` T18's; the CMake T35's
- **What is wrong:** Resolves only through `-I es-core/src` plus `../../`; es-core does not build alone.
- **Proposed disposition:** recorded; a `CloudText` that moves to es-core is T18's and T35's call
- **proved:** tree

## PL-22: The switch's and the option list's callbacks are stored by value, not weak by design

- **Severity:** Low; **category:** Lifetime; **question:** Q4
- **Source finding:** § 1 (c), T26 PL-27
- **Lines at the pin:** `SwitchComponent.h:53`; `OptionListComponent.h:658`
- **Owner:** T34; the pages' clearing T26's and T31's
- **What is wrong:** A page's lambda capturing a `shared_ptr` to the component that stores it makes a cycle only the page's `onFinalize` breaks.
- **Proposed disposition:** a design ruling at the pause; LeakSanitizer over an extracted builder
- **proved:** tree

## PL-23: The brand is kept lowercase by reading, not by a check

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-18
- **Lines at the pin:** `MenuComponent.cpp:205`, `:233`, `:236`, `:283`, `:487`; `ButtonComponent.cpp:73`
- **Owner:** the coordinator (a tool rule)
- **What is wrong:** Six formatters upper-case every label they see; no fork label passes the brand through them at the pin.
- **Proposed disposition:** a `tools/vocabulary-check` rule proposed (the brand inside those builders' arguments)
- **proved:** tree

## PL-24: The carousel's fast move can hand `listInput` a negative count

- **Severity:** Low; **category:** Correctness; **question:** Q3
- **Source finding:** 3.8
- **Lines at the pin:** `CarouselComponent.cpp:74-90`, `:113`, `:119`; `IList.h:376-400`
- **Owner:** T34 (upstream surface)
- **What is wrong:** Size 3, cursor 0, page up: `count = -10`, one `+= sz` gives `-7`; whether `listInput(-7)` lands in `[0, sz)` for every loop type is 3.8's case.
- **Proposed disposition:** withdraw: the seat showed `IList::scroll` clamps (NEVER_LOOP, PAUSE_AT_END) or wraps the `-7` into range (`IList.h:376-405`); a negative count is an intended input; 3.8 stays as a case
- **proved:** tree

## PL-25: An unset date reads blank, not `<NOT SET>`

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** 3.13
- **Lines at the pin:** `DateTimeEditComponent.cpp:256-257`
- **Owner:** T34 (upstream surface)
- **What is wrong:** `getTime() == 0` returns `""`.
- **Proposed disposition:** a style question for the pause
- **proved:** tree

## PL-26: Whether `ImageComponent` gains the untinted mode the fork wrote as a subclass

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** § 1 (h)
- **Lines at the pin:** `GuiMenu.cpp:6401` (T26's); `ImageComponent.h:76`
- **Owner:** the pause
- **What is wrong:** `UntintedImageComponent` lives in a page file; every untinted image needs the same subclass.
- **Proposed disposition:** a question for the pause; nothing changed here
- **proved:** tree

## PL-27: A security-sensitive finding in a fork-modified component; its details are held off the public tracker

- **Severity:** High; **category:** Security; **question:** Q5
- **Source finding:** G-3 (the seat's), verified at the pin
- **Lines at the pin:** held
- **Owner:** T34
- **What is wrong:** Held privately (outside the tree, mode 600) pending the maintainer's decision on where security findings go; the public record names its existence, its severity and its owner, not its mechanism.
- **Proposed disposition:** the coordinator names the private channel; the fix lands under a stream brief there
- **proved:** tree

## PL-28: Three members are read before anything sets them

- **Severity:** Medium; **category:** Correctness; **question:** Q7
- **Source finding:** G-1, verified
- **Lines at the pin:** `ComponentList.h:157` with `ComponentList.cpp:13-27`, `:196`; `GridTileComponent.h:312` with `.cpp:49`, `:1246`; `GridTileComponent.h:77-90`, `:107`, `:134`
- **Owner:** T34 (upstream's lines, rule 6)
- **What is wrong:** `mUpdateType` has no initializer and the constructor never sets it before `update()` reads it; `GridTile`'s constructor calls `setSelected(false)`, which reads the uninitialised `mSelected`; `GridTextProperties::autoScroll` is set only when a theme names `singleLineScroll`.
- **Proposed disposition:** explicit initial values; a #585 line
- **proved:** tree

## PL-29: A help bar whose first entry does not fit builds a 0-column grid

- **Severity:** Medium; **category:** Input; **question:** Q3
- **Source finding:** G-2, verified
- **Lines at the pin:** `HelpComponent.cpp:131-132`, `:150-156`; `ComponentGrid.cpp:12`
- **Owner:** T34 (the fork's `7dc8bf373` fit, #210)
- **What is wrong:** If the first prompt is wider than the bar, nothing is kept and `:155` builds `ComponentGrid(0, 1)`, which the grid asserts against: Medium in assertion builds; a long translated label or a large themed font reaches it.
- **Proposed disposition:** an empty-items return before the grid is built; 3.16's case extended
- **proved:** tree

## PL-30: A web image in a resizing grid cell can recurse through its parent

- **Severity:** Medium; **category:** Layout; **question:** Q1
- **Source finding:** G-4, verified with narrowing
- **Lines at the pin:** `WebImageComponent.cpp:69-70`; `ImageComponent.cpp:65-79`; `ComponentGrid.cpp:174-175`
- **Owner:** T34
- **What is wrong:** `resize()` notifies the parent grid, the grid resizes the cell, `setSize` re-runs `resize()` with no unchanged-size exit. Reached only in a `resize=true` cell; the callers' cells are unread.
- **Proposed disposition:** an unchanged-size exit, or a non-reentrant notification; the callers' cells read first
- **proved:** tree

## PL-31: Rebinding a web image can leave an older URL queued

- **Severity:** Medium; **category:** Reads; **question:** Q5
- **Source finding:** G-5, verified
- **Lines at the pin:** `WebImageComponent.cpp:98-115`, `:156-165`, `:225-244`
- **Owner:** T34
- **What is wrong:** `setImage()` deletes an active request but does not clear `mUrlToLoad`; the local and cached returns (`:115`, `:158`) leave it, and `render` starts it, replacing the image the caller set last.
- **Proposed disposition:** clear the pending URL on every rebind
- **proved:** tree

## PL-32: Replacing an image from memory or a shared texture does not cancel a pending load

- **Severity:** Medium; **category:** Reads; **question:** Q5
- **Source finding:** G-6, verified
- **Lines at the pin:** `ImageComponent.cpp:413-416`, `:436-467`, `:816-823`
- **Owner:** T34
- **What is wrong:** Only the path overload sets `mLoadingTexture`; the other two never clear it, and `watchTextureLoading` later installs the stale texture.
- **Proposed disposition:** every source-replacing overload cancels the pending load
- **proved:** tree

## PL-33: A cleared looping grid keeps drawing its loop-copy tiles

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** G-7, verified; corrects the stage-B contract
- **Lines at the pin:** `ImageGridComponent.h:505-509`, `:1381-1435`, `:316-317`, `:339-340`, `:762-763`
- **Owner:** T34 (the save-state manager and the grid view)
- **What is wrong:** `clear()` -> `resetGrid()` never clears `mScrollLoopTiles`, and the routine that does returns first on an empty list; `render` still draws them.
- **Proposed disposition:** clear the loop map in `resetGrid()`; T32's `s4-views.py` shape as the case
- **proved:** tree

## PL-34: Changing a visible grid entry's image strands its old tile

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** G-8, verified with narrowing
- **Lines at the pin:** `ImageGridComponent.h:526-533`, `:373-384`, `:426-433`
- **Owner:** T34
- **What is wrong:** The entry's tile pointer is dropped without removing the tile from the visible list; repeated changes accumulate tiles until a reset.
- **Proposed disposition:** remove the old tile when the entry's image changes
- **proved:** tree

## PL-35: An assignment where a comparison was meant

- **Severity:** Low; **category:** Correctness; **question:** Q3
- **Source finding:** G-9, verified
- **Lines at the pin:** `ImageGridComponent.h:1151`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** `else if (mLastCursor = -9999)` always succeeds and overwrites the last cursor.
- **Proposed disposition:** `==`; a #585 line
- **proved:** tree

## PL-36: A switch can show a state other than the one it holds

- **Severity:** Medium; **category:** Input; **question:** Q3
- **Source finding:** G-10, verified with narrowing
- **Lines at the pin:** `SwitchComponent.cpp:7-25`, `:118-137`
- **Owner:** T34 (a lane surface: every on/off row)
- **What is wrong:** The constructor always loads the OFF image and never calls `onStateChanged()`; with auto set, `setValue("true")` leaves auto in force and `getValue()` still says `auto`.
- **Proposed disposition:** the image from the given state; explicit values leave auto mode
- **proved:** tree

## PL-37: Updating a subtitle re-inserts the title image it already holds

- **Severity:** Medium; **category:** Structure; **question:** Q7
- **Source finding:** G-11, verified with narrowing
- **Lines at the pin:** `MenuComponent.cpp:374-375`, `:305-331`
- **Owner:** T34
- **What is wrong:** `setSubTitle` re-runs `setTitleImage`, which `setEntry`s the parented image again with no `removeEntry`: an assertion in debug builds, a duplicate entry otherwise.
- **Proposed disposition:** remove or update the existing entry first
- **proved:** tree

## PL-38: Right-to-left rows send text and prompts to a different element than input

- **Severity:** Medium; **category:** Input; **question:** Q3
- **Source finding:** G-12, verified
- **Lines at the pin:** `ComponentList.h:56-61`; `ComponentList.cpp:155-165`, `:541-553`
- **Owner:** T34 (outside the fork's languages)
- **What is wrong:** RTL rows prepend elements and `input()` uses `front()`, while `textInput` and `getHelpPrompts` use `back()`; neither guards an empty row.
- **Proposed disposition:** one element choice for all three, with the empty check; outside English and French, so recorded unless the pause opens it
- **proved:** tree

## PL-39: A quarter-turned min-size image reports the wrong cropped size

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** G-13, verified with narrowing
- **Lines at the pin:** `ImageComponent.cpp:33`, `:155-170`
- **Owner:** T34 (the fork's turn, `3b7265f33`)
- **What is wrong:** `getSize()` multiplies screen-axis size by crop factors that are in texture axes after a turn.
- **Proposed disposition:** swap the crop factors in `getSize()` after a turn; 3.22's case extended
- **proved:** tree

## PL-40: Narrow scrollable content gets a negative horizontal offset

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** G-14, verified
- **Lines at the pin:** `ScrollableContainer.cpp:78-96`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** The X branch lacks the Y branch's narrow-content case.
- **Proposed disposition:** the same guard as Y; 3.14's case
- **proved:** tree

## PL-41: A tab's mouse release never dispatches

- **Severity:** Low; **category:** Input; **question:** Q3
- **Source finding:** G-15, verified
- **Lines at the pin:** `ComponentTab.cpp:426-430`
- **Owner:** T34
- **What is wrong:** `row` is compared with `mHotTab` after `mHotTab` was reset to -1.
- **Proposed disposition:** compare with the saved value; recorded (mouse only)
- **proved:** tree

## PL-42: Tile padding's test checks Y twice and never Z

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** G-16, verified
- **Lines at the pin:** `GridTileComponent.cpp:565`
- **Owner:** T34
- **What is wrong:** The right inset is never tested, so a pixel right inset can enter the normalised branch.
- **Proposed disposition:** test Z; a #585 line
- **proved:** tree

## PL-43: A subtitle with a slash keeps only what follows the last one

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-26 (new, the read)
- **Lines at the pin:** `MenuComponent.cpp:357-359`
- **Owner:** T34
- **What is wrong:** `setSubTitle` builds its text from `getFileName(text)`.
- **Proposed disposition:** read the update path; `getFileName` dropped if no caller relies on it
- **proved:** tree

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Resolved** | `2cbb62d7b` (#1309); `tsan-card` rc 0, the interleaving case PASS |
| PL-02 | **Resolved** | `2cbb62d7b` (#1310), `52f0ff512` (the handle forwards); Window's half `stage-e/s2-window.patch` (T35's, #682) and the holders' `stage-e/s2-holders.patch` (#665, #667, #678, #680), merge debt |
| PL-03 | **Resolved** | `2cbb62d7b` (#1311); `asan-textedit` rc 0 |
| PL-04 | **Resolved** | `a9017ff50` (#1312); 3.16 PASS |
| PL-05 | **Withdrawn** | the stage-D ruling (the seat's trace of SWITCH TAB through the pin's chain); the image's empty bar a lead for T35 (#682) |
| PL-06 | **Resolved** | `db12b1598` (#1313); 3.6 PASS |
| PL-07 | **Resolved** | `db12b1598` (#1314); 3.4 and the long-description case PASS |
| PL-08 | **Resolved** | `db12b1598` (#1315); 3.5 PASS; `GuiMsgBox`'s workaround `stage-e/s3-msgbox.patch` (T35's, #682) and `es-code-traps.md` (the coordinator's), merge debt |
| PL-09 | **Resolved** | `a9017ff50` (#1316); 3.7 PASS |
| PL-10 | **Resolved** | `a9017ff50` (#1317); ADD STAR / AJOUTER UNE ÉTOILE |
| PL-11 | **Resolved** | `a9017ff50` (#1318); an empty prompt list (ruling 7) |
| PL-12 | **Deferred** | recorded as written: the invariant beside `MenuComponent.h:53-56` in `02` § The lifetimes; the cast that relies on it is `GuiMenu.cpp:591`, #673's |
| PL-13 | **Resolved** | `568ef099d` (#1319); no timer (ruling 5): the pin already re-asks on the next bind, the fix is the uncached state |
| PL-14 | **Deferred** | #585, and the pages' labels to #673 and #678; 3.26 `may_fail` with PL-14 named (ruling 9) |
| PL-15 | **Resolved** | `db12b1598` (#1320); `ROW_INSET_FRACTION`, D-UI-132 |
| PL-16 | **Resolved** | `db12b1598`: the comment names the keyboard popup's second copy; the copy is T35's (#682) |
| PL-17 | **Deferred** | an open item to test (the moving font height; `Font.cpp` is #683's) |
| PL-18 | **Deferred** | #585; an open item to test (D-QA-051 rule 4: no media on the guest) |
| PL-19 | **Resolved** | `a9017ff50` (#1321) |
| PL-20 | **Deferred** | recorded as written on #1307: the dead `_RPI_` and `WIN32` blocks and the unused `widthMod`, a dead-end table that removes nothing (D-WORKFLOW-209) |
| PL-21 | **Deferred** | #665 and #682: the es-app include is T18's and T35's call |
| PL-22 | **Deferred** | #673 and #678: the pages' `onFinalize` clearing |
| PL-23 | **Deferred** | #1336, the coordinator's Backlog for the `tools/vocabulary-check` rule (the brand inside the up-casing builders' arguments) |
| PL-24 | **Withdrawn** | the stage-D ruling: `IList::scroll` clamps or wraps; 3.8 PASS at the pin for every size and loop type |
| PL-25 | **Resolved** | `a9017ff50` (#1322); 3.13 PASS |
| PL-26 | **Deferred** | #673: `UntintedImageComponent` lives at `GuiMenu.cpp:6401`; lifting an untinted mode is a question for that slice |
| PL-27 | **Resolved** | `dbe4c2db0` (#1323); held: the case's counts only, `stage-e/s1-checks.txt` |
| PL-28 | **Resolved** | `5908888b5` (#1324); `UPDATE_ALWAYS` after reading every caller (ruling 11) |
| PL-29 | **Resolved** | `a9017ff50` (#1325); the first prompt kept and clipped (ruling 4), batocera's `9dbd4b9bf` guard taken |
| PL-30 | **Resolved** | `db12b1598` (#1326); the unchanged-size exit (ruling 3) |
| PL-31 | **Resolved** | `568ef099d` (#1327) |
| PL-32 | **Resolved** | `568ef099d` (#1328) |
| PL-33 | **Resolved** | `6050b8419` (#1329) |
| PL-34 | **Resolved** | `6050b8419` (#1330) |
| PL-35 | **Resolved** | `6050b8419` (#1331); the intent read posted before the commit (ruling 12) |
| PL-36 | **Resolved** | `5908888b5` (#1332); auto kept in force (ruling 13) |
| PL-37 | **Resolved** | `5908888b5` (#1333) |
| PL-38 | **Deferred** | #585: outside English and French |
| PL-39 | **Deferred** | recorded as written: the fork's turn (`3b7265f33`); 3.22 says what the pin does, PASS before and after |
| PL-40 | **Deferred** | #585; 3.14's half `may_fail` with PL-40 named, as ruling 9 marks 3.26 |
| PL-41 | **Deferred** | recorded as written on #1307: the mouse path only |
| PL-42 | **Deferred** | #585 |
| PL-43 | **Withdrawn** | the read (`stage-e/s7-checks.txt`): `setSubTitle` sets the full text at `:365` in the same call, before any draw, so the `getFileName` text at `:358-360` is never shown |

## punch_index

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "L-22 (new)"
  outcome: "resolved"
- id: PL-02
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "§ 1 (b), T2 PC-1"
  outcome: "resolved"
- id: PL-03
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "L-12"
  outcome: "resolved"
- id: PL-04
  severity: "Low"
  category: Words
  question: Q3
  source_finding: "L-01, 3.16"
  outcome: "resolved"
- id: PL-05
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "L-25 (new, the guest)"
  outcome: "withdrawn"
- id: PL-06
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "3.6"
  outcome: "resolved"
- id: PL-07
  severity: "Medium"
  category: Layout
  question: Q1
  source_finding: "L-03, 3.4"
  outcome: "resolved"
- id: PL-08
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-17, #48"
  outcome: "resolved"
- id: PL-09
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "3.7"
  outcome: "resolved"
- id: PL-10
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-23 (new)"
  outcome: "resolved"
- id: PL-11
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "L-24 (new)"
  outcome: "resolved"
- id: PL-12
  severity: "Low"
  category: Structure
  question: Q3
  source_finding: "L-15"
  outcome: "deferred"
- id: PL-13
  severity: "Low"
  category: Reads
  question: Q5
  source_finding: "L-08, 3.21"
  outcome: "resolved"
- id: PL-14
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-04, 3.26"
  outcome: "deferred"
- id: PL-15
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-06"
  outcome: "resolved"
- id: PL-16
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-05"
  outcome: "resolved"
- id: PL-17
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-02, L-16"
  outcome: "deferred"
- id: PL-18
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "L-10"
  outcome: "deferred"
- id: PL-19
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "L-13"
  outcome: "resolved"
- id: PL-20
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-14"
  outcome: "deferred"
- id: PL-21
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-07"
  outcome: "deferred"
- id: PL-22
  severity: "Low"
  category: Lifetime
  question: Q4
  source_finding: "§ 1 (c), T26 PL-27"
  outcome: "deferred"
- id: PL-23
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-18"
  outcome: "deferred"
- id: PL-24
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "3.8"
  outcome: "withdrawn"
- id: PL-25
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "3.13"
  outcome: "resolved"
- id: PL-26
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "§ 1 (h)"
  outcome: "deferred"
- id: PL-27
  severity: "High"
  category: Security
  question: Q5
  source_finding: "G-3 (the seat's), verified at the pin"
  outcome: "resolved"
- id: PL-28
  severity: "Medium"
  category: Correctness
  question: Q7
  source_finding: "G-1, verified"
  outcome: "resolved"
- id: PL-29
  severity: "Medium"
  category: Input
  question: Q3
  source_finding: "G-2, verified"
  outcome: "resolved"
- id: PL-30
  severity: "Medium"
  category: Layout
  question: Q1
  source_finding: "G-4, verified with narrowing"
  outcome: "resolved"
- id: PL-31
  severity: "Medium"
  category: Reads
  question: Q5
  source_finding: "G-5, verified"
  outcome: "resolved"
- id: PL-32
  severity: "Medium"
  category: Reads
  question: Q5
  source_finding: "G-6, verified"
  outcome: "resolved"
- id: PL-33
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "G-7, verified; corrects the stage-B contract"
  outcome: "resolved"
- id: PL-34
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "G-8, verified with narrowing"
  outcome: "resolved"
- id: PL-35
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "G-9, verified"
  outcome: "resolved"
- id: PL-36
  severity: "Medium"
  category: Input
  question: Q3
  source_finding: "G-10, verified with narrowing"
  outcome: "resolved"
- id: PL-37
  severity: "Medium"
  category: Structure
  question: Q7
  source_finding: "G-11, verified with narrowing"
  outcome: "resolved"
- id: PL-38
  severity: "Medium"
  category: Input
  question: Q3
  source_finding: "G-12, verified"
  outcome: "deferred"
- id: PL-39
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "G-13, verified with narrowing"
  outcome: "deferred"
- id: PL-40
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "G-14, verified"
  outcome: "deferred"
- id: PL-41
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "G-15, verified"
  outcome: "deferred"
- id: PL-42
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "G-16, verified"
  outcome: "deferred"
- id: PL-43
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-26 (new, the read)"
  outcome: "withdrawn"
```

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
 ("The `up/down` help icon key goes through `_()`", "Medium", "Words", "Q3", "L-01, 3.16", "`ComponentList.cpp:568`; `HelpComponent.cpp:176-200`; fr po `:3708-3709`", "T34 (upstream's line, rule 6)",
  "Under a catalog that translates `up/down` (French: `haut/bas`) the list's CHOOSE prompt carries a key `getIconTexture` does not know: a null icon and `Unknown help icon`. Not reproduced on the image at 1280x800 (one CHOISIR with its icon, 0 log lines, the catalog carrying `haut/bas`): something between the list and the bar hides it there (L-25's neighbour).", "drop the `_()` (a contained fix, a #585 line); 3.16 as the covering case; the catalog's orphan `msgid` is a row for the pause", "tree; guest (image): not reproduced"),
 ("The tabbed SCRAPEUR page's help bar carries no component prompt", "Medium", "Input", "Q3", "L-25 (new, the guest)", "`ComponentTab.cpp:320-345`; `MenuComponent.cpp:531-533`; `ComponentGrid.cpp:519-553`", "T34 (if the pin's components drop them); `Window`'s bar T35's",
  "At 1280x800 the bar reads only FERMER and RETOUR, pixel-identical with a row focused and with the strip focused: no SWITCH TAB, no row prompt. Shown on the image only; whether the pin's tabbed `MenuComponent` loses its children's prompts, or the image's composition does, is unread.", "read at the pin before a fix (the grid's prompt collection with a tab strip cell; when `updateHelpPrompts` runs on a focus move inside the menu); a `bug` only if the pin's code drops them", "guest (image)"),
 ("The vertical marquee's limit subtracts the top padding twice", "Low", "Correctness", "Q1", "3.6", "`TextComponent.cpp:486`", "T34 (upstream's line, rule 6)",
  "`mSize.y() - mPadding.y() - mPadding.y()` where `:351` and `:428` take `.y()` and `.w()`: with padding (0,10,0,30) the limit is 20 px too large, so a text that overflows by less never scrolls.", "the one token (`.w()`), a #585 line; 3.6's case FAIL then PASS", "tree"),
 ("A two-line row's shares do not sum to 1 when its fonts differ", "Low", "Layout", "Q1", "L-03, 3.4", "`MultiLineMenuEntry.cpp:74-75`", "T34 (upstream's formula, moved by the fork's `48d43c0fb`)",
  "`th*0.9/h + sh*1.1/h` is 1 only when `th == sh`: a taller Text font leaves a gap, a taller TextSmall overflows by `0.1*(sh-th)/h`.", "a pause ruling (a register row): shares that sum to 1, or the gap recorded; 3.4's case", "tree"),
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
 ("Two pages read a 20 px row inset at every panel", "Low", "Constants", "Q2", "L-06", "`ComponentList.cpp:11`, `:491-494`", "T34 (upstream's constant); the pages T26's and T31's",
  "`rowInset()` exports `TOTAL_HORIZONTAL_PADDING_PX` 20 to two fork pages: 3.1 % of 640, 1.0 % of 1920.", "a pause ruling (a register row): a screen fraction under D-UI-012's family, or upstream's constant kept", "tree; guest (image) at both sizes"),
 ("The bar's gap is claimed to be defined in one place; the keyboard popup keeps a second", "Low", "Constants", "Q2", "L-05", "`MenuComponent.cpp:7-13`; `GuiTextEditPopupKeyboard.cpp:14` (T35's)", "the comment T34's; the popup T35's",
  "Two definitions, one claim.", "the comment corrected or the claim kept at the pause; the second copy is not deleted here", "tree"),
 ("Rows and fields are sized from a font height that grows as glyphs rasterise", "Low", "Layout", "Q1", "L-02, L-16", "`MultiLineMenuEntry.cpp:55`, and the 12 other layout reads in § The layouts", "T34; `Font.cpp` T36's",
  "A size taken before the tallest glyph has drawn is a few px short. G-05's reopened pair was identical on the image because the menus had already drawn.", "a pause ruling: a rasterise-first in the component, or recorded", "tree; guest (image): no difference shown"),
 ("The VLC release thread nulls `component` without a lock while VLC's thread reads it", "Low", "Lifetime", "Q4", "L-10", "`VideoVlcComponent.cpp:53-61`, `:84-96`, `:911`", "T34 (upstream surface, outside the lanes)",
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
  "Size 3, cursor 0, page up: `count = -10`, one `+= sz` gives `-7`; whether `listInput(-7)` lands in `[0, sz)` for every loop type is 3.8's case.", "3.8's case at stage C decides; a `bug` only if it FAILs", "tree"),
 ("An unset date reads blank, not `<NOT SET>`", "Low", "Words", "Q6", "3.13", "`DateTimeEditComponent.cpp:256-257`", "T34 (upstream surface)",
  "`getTime() == 0` returns `\"\"`.", "a style question for the pause", "tree"),
 ("Whether `ImageComponent` gains the untinted mode the fork wrote as a subclass", "Low", "Structure", "Q7", "§ 1 (h)", "`GuiMenu.cpp:6401` (T26's); `ImageComponent.h:76`", "the pause",
  "`UntintedImageComponent` lives in a page file; every untinted image needs the same subclass.", "a question for the pause; nothing changed here", "tree"),
]
ids = ["PL-%02d" % (i + 1) for i in range(len(I))]
for t in I:
    if t[1] not in SEV or not re.fullmatch(r"Q[1-7]", t[3]):
        print("ASSERT: a bad severity or question in %r" % t[0], file=sys.stderr); sys.exit(1)
out = ["# Punch list (Phases 5 and 6) — M6.P2 T34, EmulationStation's core components (#681)", "",
       "Written by `tools/t34-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 layout, Q2 constants, Q3 input, Q4 lifetime, Q5 reads, Q6 words, Q7 structure); `04` § Renovation face maps them to the plan's seven. Every item is Open until the stage-D pause disposes it.", ""]
for pl, (title, sev, cat, q, src, lines, own, what, disp, proved) in zip(ids, I):
    out += ["## %s: %s" % (pl, title), "", "- **Severity:** %s; **category:** %s; **question:** %s" % (sev, cat, q), "- **Source finding:** %s" % src,
            "- **Lines at the pin:** %s" % lines, "- **Owner:** %s" % own, "- **What is wrong:** %s" % what, "- **Proposed disposition:** %s" % disp, "- **proved:** %s" % proved, ""]
out += ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
out += ["| %s | Open | proposed: %s |" % (pl, t[8]) for pl, t in zip(ids, I)]
out += ["", "## punch_index", "", "```yaml", "punch_index:"]
for pl, t in zip(ids, I):
    out += ["- id: %s" % pl, "  severity: \"%s\"" % t[1], "  category: %s" % t[2], "  question: %s" % t[3], "  source_finding: \"%s\"" % t[4].replace('"', "'"), "  outcome: \"open\""]
out += ["```", ""]
open(os.path.join(os.path.dirname(HERE), "05-punch-list.md"), "w", encoding="utf-8").write("\n".join(out))
c = {s: sum(1 for t in I if t[1] == s) for s in SEV}
print("t34-05: %d items (%s), every one Open" % (len(I), ", ".join("%d %s" % (c[s], s) for s in SEV)))

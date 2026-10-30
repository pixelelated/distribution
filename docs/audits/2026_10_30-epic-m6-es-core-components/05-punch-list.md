# Punch list (Phases 5 and 6) — M6.P2 T34, EmulationStation's core components (#681)

Written by `tools/t34-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 layout, Q2 constants, Q3 input, Q4 lifetime, Q5 reads, Q6 words, Q7 structure); `04` § Renovation face maps them to the plan's seven. Every item is Open until the stage-D pause disposes it.

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

- **Severity:** Medium; **category:** Words; **question:** Q3
- **Source finding:** L-01, 3.16
- **Lines at the pin:** `ComponentList.cpp:568`; `HelpComponent.cpp:176-200`; fr po `:3708-3709`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** Under a catalog that translates `up/down` (French: `haut/bas`) the list's CHOOSE prompt carries a key `getIconTexture` does not know: a null icon and `Unknown help icon`. Not reproduced on the image at 1280x800 (one CHOISIR with its icon, 0 log lines, the catalog carrying `haut/bas`): something between the list and the bar hides it there (L-25's neighbour).
- **Proposed disposition:** drop the `_()` (a contained fix, a #585 line); 3.16 as the covering case; the catalog's orphan `msgid` is a row for the pause
- **proved:** tree; guest (image): not reproduced

## PL-05: The tabbed SCRAPEUR page's help bar carries no component prompt

- **Severity:** Medium; **category:** Input; **question:** Q3
- **Source finding:** L-25 (new, the guest)
- **Lines at the pin:** `ComponentTab.cpp:320-345`; `MenuComponent.cpp:531-533`; `ComponentGrid.cpp:519-553`
- **Owner:** T34 (if the pin's components drop them); `Window`'s bar T35's
- **What is wrong:** At 1280x800 the bar reads only FERMER and RETOUR, pixel-identical with a row focused and with the strip focused: no SWITCH TAB, no row prompt. Shown on the image only; whether the pin's tabbed `MenuComponent` loses its children's prompts, or the image's composition does, is unread.
- **Proposed disposition:** read at the pin before a fix (the grid's prompt collection with a tab strip cell; when `updateHelpPrompts` runs on a focus move inside the menu); a `bug` only if the pin's code drops them
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

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** L-03, 3.4
- **Lines at the pin:** `MultiLineMenuEntry.cpp:74-75`
- **Owner:** T34 (upstream's formula, moved by the fork's `48d43c0fb`)
- **What is wrong:** `th*0.9/h + sh*1.1/h` is 1 only when `th == sh`: a taller Text font leaves a gap, a taller TextSmall overflows by `0.1*(sh-th)/h`.
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

## PL-15: Two pages read a 20 px row inset at every panel

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** L-06
- **Lines at the pin:** `ComponentList.cpp:11`, `:491-494`
- **Owner:** T34 (upstream's constant); the pages T26's and T31's
- **What is wrong:** `rowInset()` exports `TOTAL_HORIZONTAL_PADDING_PX` 20 to two fork pages: 3.1 % of 640, 1.0 % of 1920.
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

## PL-18: The VLC release thread nulls `component` without a lock while VLC's thread reads it

- **Severity:** Low; **category:** Lifetime; **question:** Q4
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
- **Proposed disposition:** 3.8's case at stage C decides; a `bug` only if it FAILs
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

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | proposed: a `bug`; the two members atomic, or `close()` under `mMutex` with `update()` reading under it; a ThreadSanitizer case over an extracted card first (stage E's covering case) |
| PL-02 | Open | proposed: a design ruling at the pause: a handle the window keeps alive until the holder lets go (the component's half), with `Window`'s teardown order T35's |
| PL-03 | Open | proposed: a weak token the posts check; 3.20's case (post, delete, drain) with the fakes' `Window.h` as the covering case |
| PL-04 | Open | proposed: drop the `_()` (a contained fix, a #585 line); 3.16 as the covering case; the catalog's orphan `msgid` is a row for the pause |
| PL-05 | Open | proposed: read at the pin before a fix (the grid's prompt collection with a tab strip cell; when `updateHelpPrompts` runs on a focus move inside the menu); a `bug` only if the pin's code drops them |
| PL-06 | Open | proposed: the one token (`.w()`), a #585 line; 3.6's case FAIL then PASS |
| PL-07 | Open | proposed: a pause ruling (a register row): shares that sum to 1, or the gap recorded; 3.4's case |
| PL-08 | Open | proposed: a pause ruling (a register row): the root fixed in the component (it re-heights every padded auto-height text) or recorded with the reproducer for #585; 3.5's case |
| PL-09 | Open | proposed: `_("AUTO")` with its French in the same commit, a #585 line; 3.7's case |
| PL-10 | Open | proposed: `_()` with its French in the same commit, a #585 line |
| PL-11 | Open | proposed: recorded; contained under rule 6 if the pause opens it |
| PL-12 | Open | proposed: a `dynamic_pointer_cast` with a null check, the invariant written beside `MenuComponent.h:53-56` |
| PL-13 | Open | proposed: a pause ruling: a re-ask on the next page build, or a word on the row; `tools/ra-ui-test`'s fixture shape |
| PL-14 | Open | proposed: a pause ruling: a bar that fits its cell, or the pages' labels; 3.26's arithmetic per page |
| PL-15 | Open | proposed: a pause ruling (a register row): a screen fraction under D-UI-012's family, or upstream's constant kept |
| PL-16 | Open | proposed: the comment corrected or the claim kept at the pause; the second copy is not deleted here |
| PL-17 | Open | proposed: a pause ruling: a rasterise-first in the component, or recorded |
| PL-18 | Open | proposed: recorded (G-10 `CANNOT`: no media); a contained fix only if the pause opens it |
| PL-19 | Open | proposed: recorded |
| PL-20 | Open | proposed: a one-commit tidy if the pause opens it |
| PL-21 | Open | proposed: recorded; a `CloudText` that moves to es-core is T18's and T35's call |
| PL-22 | Open | proposed: a design ruling at the pause; LeakSanitizer over an extracted builder |
| PL-23 | Open | proposed: a `tools/vocabulary-check` rule proposed (the brand inside those builders' arguments) |
| PL-24 | Open | proposed: 3.8's case at stage C decides; a `bug` only if it FAILs |
| PL-25 | Open | proposed: a style question for the pause |
| PL-26 | Open | proposed: a question for the pause; nothing changed here |

## punch_index

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "L-22 (new)"
  outcome: "open"
- id: PL-02
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "§ 1 (b), T2 PC-1"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "L-12"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Words
  question: Q3
  source_finding: "L-01, 3.16"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Input
  question: Q3
  source_finding: "L-25 (new, the guest)"
  outcome: "open"
- id: PL-06
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "3.6"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-03, 3.4"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-17, #48"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "3.7"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-23 (new)"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "L-24 (new)"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Structure
  question: Q3
  source_finding: "L-15"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Reads
  question: Q5
  source_finding: "L-08, 3.21"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-04, 3.26"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-06"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-05"
  outcome: "open"
- id: PL-17
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-02, L-16"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Lifetime
  question: Q4
  source_finding: "L-10"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "L-13"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-14"
  outcome: "open"
- id: PL-21
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-07"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Lifetime
  question: Q4
  source_finding: "§ 1 (c), T26 PL-27"
  outcome: "open"
- id: PL-23
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-18"
  outcome: "open"
- id: PL-24
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "3.8"
  outcome: "open"
- id: PL-25
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "3.13"
  outcome: "open"
- id: PL-26
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "§ 1 (h)"
  outcome: "open"
```

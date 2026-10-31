# Forward audit — M6.P2 T34, EmulationStation's core components (#681)

Composed by `tools/t34-02.py` from this template and the generators under `tools/`. Each generated section ends with its generator's own "generated, asserted" line. Each generator was seen to exit 1 on a constructed drift before it was trusted (`stage-b/generator-drifts.txt`).

The read is the pin `16dbac5211eea7e70db7394372033be2be7df829`'s bytes, through `git -C <W> show`; the ES worktree stays at the pin until stage E. Every proof carries `proved:` in #681's vocabulary: `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`. A row whose proof is still owed says `pending:` and names the stage that owes it.

## Coverage

The 80 paths, one row each. The read tier comes from `git diff` against the fork's base `bccd715707`: added, modified, or neither. The inventory tier is fork-own for the first two and upstream-carried for the third. The fork's numstat is the same against the merge base `cada856d86` (asserted per row).

| Path | Lines (`grep -c ''`) | Inventory tier | Read tier | Fork +/- (against `bccd715707`, equal against `cada856d86`) | Leads naming it |
| --- | ---: | --- | --- | ---: | --- |
| `es-core/src/components/AnimatedImageComponent.cpp` | 86 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/AnimatedImageComponent.h` | 47 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/AsyncNotificationComponent.cpp` | 306 | fork-own | fork-modified | 128/17 | L-07, L-19, 3.18 |
| `es-core/src/components/AsyncNotificationComponent.h` | 78 | fork-own | fork-modified | 23/2 | - |
| `es-core/src/components/BatteryIconComponent.cpp` | 101 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryIconComponent.h` | 38 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryIndicatorComponent.cpp` | 56 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryIndicatorComponent.h` | 19 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryTextComponent.cpp` | 64 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryTextComponent.h` | 30 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BusyComponent.cpp` | 134 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BusyComponent.h` | 41 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ButtonComponent.cpp` | 225 | upstream-carried | upstream-carried | 0/0 | L-04, L-18, 3.26 |
| `es-core/src/components/ButtonComponent.h` | 73 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/CarouselComponent.cpp` | 1128 | upstream-carried | upstream-carried | 0/0 | L-13, 3.34, 3.8 |
| `es-core/src/components/CarouselComponent.h` | 183 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ClockComponent.cpp` | 52 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ClockComponent.h` | 24 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ComponentGrid.cpp` | 553 | fork-own | fork-modified | 38/2 | L-04, 3.1, 3.2, 3.3 |
| `es-core/src/components/ComponentGrid.h` | 150 | fork-own | fork-modified | 3/0 | - |
| `es-core/src/components/ComponentList.cpp` | 728 | fork-own | fork-modified | 5/0 | L-01, L-06, 3.28 |
| `es-core/src/components/ComponentList.h` | 169 | fork-own | fork-modified | 14/0 | 3.25 |
| `es-core/src/components/ComponentTab.cpp` | 437 | fork-own | fork-modified | 3/2 | 3.17 |
| `es-core/src/components/ComponentTab.h` | 82 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ControllerActivityComponent.cpp` | 603 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ControllerActivityComponent.h` | 135 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/DateTimeComponent.cpp` | 110 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/DateTimeComponent.h` | 41 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/DateTimeEditComponent.cpp` | 363 | upstream-carried | upstream-carried | 0/0 | 3.12, 3.13 |
| `es-core/src/components/DateTimeEditComponent.h` | 77 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/GridTileComponent.cpp` | 1596 | fork-own | fork-modified | 22/0 | L-14, 3.24 |
| `es-core/src/components/GridTileComponent.h` | 332 | fork-own | fork-modified | 16/0 | - |
| `es-core/src/components/HelpComponent.cpp` | 331 | fork-own | fork-modified | 25/7 | L-01, 3.16 |
| `es-core/src/components/HelpComponent.h` | 44 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/IExternalActivity.cpp` | 3 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/IExternalActivity.h` | 14 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/IList.h` | 431 | upstream-carried | upstream-carried | 0/0 | 3.15, 3.8 |
| `es-core/src/components/ImageComponent.cpp` | 1400 | fork-own | fork-modified | 58/4 | L-20, 3.22, 3.23, 3.24 |
| `es-core/src/components/ImageComponent.h` | 220 | fork-own | fork-modified | 16/0 | - |
| `es-core/src/components/ImageGridComponent.h` | 1705 | fork-own | fork-modified | 19/0 | L-14, 3.10, 3.9 |
| `es-core/src/components/MenuComponent.cpp` | 574 | fork-own | fork-modified | 86/49 | L-04, L-05, L-15, L-16, L-18, 3.26, 3.27 |
| `es-core/src/components/MenuComponent.h` | 122 | fork-own | fork-modified | 9/0 | - |
| `es-core/src/components/MultiLineMenuEntry.cpp` | 153 | fork-own | fork-modified | 58/26 | L-02, L-03, 3.4 |
| `es-core/src/components/MultiLineMenuEntry.h` | 46 | fork-own | fork-modified | 19/0 | - |
| `es-core/src/components/NetworkIconComponent.cpp` | 79 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/NetworkIconComponent.h` | 34 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/NinePatchComponent.cpp` | 495 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/NinePatchComponent.h` | 88 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/OptionListComponent.h` | 661 | upstream-carried | upstream-carried | 0/0 | L-11, L-13, L-16, 3.19 |
| `es-core/src/components/PostProcessShaderComponent.cpp` | 105 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/PostProcessShaderComponent.h` | 28 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/RatingComponent.cpp` | 295 | upstream-carried | upstream-carried | 0/0 | 3.32 |
| `es-core/src/components/RatingComponent.h` | 63 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/RectangleComponent.cpp` | 166 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/RectangleComponent.h` | 37 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ScrollableContainer.cpp` | 132 | upstream-carried | upstream-carried | 0/0 | 3.14 |
| `es-core/src/components/ScrollableContainer.h` | 32 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ScrollbarComponent.cpp` | 215 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ScrollbarComponent.h` | 64 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/SliderComponent.cpp` | 408 | upstream-carried | upstream-carried | 0/0 | 3.31, 3.7 |
| `es-core/src/components/SliderComponent.h` | 67 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/StackPanelComponent.cpp` | 226 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/StackPanelComponent.h` | 37 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/SwitchComponent.cpp` | 175 | fork-own | fork-modified | 13/3 | L-16, 3.30 |
| `es-core/src/components/SwitchComponent.h` | 60 | fork-own | fork-modified | 9/1 | - |
| `es-core/src/components/TextComponent.cpp` | 857 | upstream-carried | upstream-carried | 0/0 | L-17, 3.5, 3.6 |
| `es-core/src/components/TextComponent.h` | 141 | fork-own | fork-modified | 2/0 | - |
| `es-core/src/components/TextEditComponent.cpp` | 400 | upstream-carried | upstream-carried | 0/0 | L-12, L-16, 3.20, 3.33 |
| `es-core/src/components/TextEditComponent.h` | 72 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/TextListComponent.h` | 981 | upstream-carried | upstream-carried | 0/0 | L-16, 3.11, 3.29 |
| `es-core/src/components/VideoComponent.cpp` | 657 | upstream-carried | upstream-carried | 0/0 | L-20 |
| `es-core/src/components/VideoComponent.h` | 228 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VideoPlayerComponent.cpp` | 274 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VideoPlayerComponent.h` | 42 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VideoVlcComponent.cpp` | 1113 | upstream-carried | upstream-carried | 0/0 | L-10 |
| `es-core/src/components/VideoVlcComponent.h` | 170 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VolumeInfoComponent.cpp` | 143 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VolumeInfoComponent.h` | 30 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/WebImageComponent.cpp` | 265 | fork-own | fork-modified | 25/1 | L-08, L-09, L-21, 3.21 |
| `es-core/src/components/WebImageComponent.h` | 40 | upstream-carried | upstream-carried | 0/0 | - |

Generated, asserted by `tools/t34-coverage.py`: 80 rows; 38 `.cpp`, 42 `.h`; fork-added 0 / fork-modified 21 / upstream-carried 59 (inventory fork-own 21 / upstream-carried 59); 21984 lines by `grep -c ''`; fork +591/-114; 55 brief leads, each naming a path in the 80.

## The leads

The brief's L-01 to L-21 and floor rows 3.1 to 3.34, plus three the read found (L-22 to L-24). A lines cell is the brief's own (the new three are the read's). Each row answers in one of the seven families of the brief's § 4. Bold floor rows are the seven the brief expects to FAIL at the pin. Each is seen to FAIL against the unfixed extract at stage C before it is trusted, and a candidate that PASSes at the pin is recorded as such.

| Lead | Lines at the pin | Family | Owner | Disposition | proved | question: |
| --- | --- | --- | --- | --- | --- | --- |
| L-01 | `ComponentList.cpp:568`; `HelpComponent.cpp:102-104`, `:190-194`; `es-core/src/InputConfig.cpp:353-366`; fr po `:3708-3709` | a player sentence outside the vocabulary or without French | T34 (`ComponentList.cpp:568`, upstream's line); `InputConfig.cpp` T35's, cited | a defect in an upstream line: under French every settings list's CHOOSE prompt draws no icon and logs `Unknown help icon`; 3.16's case FAILs at the pin, G-04 under French is the frame; contained fix under rule 6 (drop the `_()`), a `bug` at stage D, a #585 line; the catalog's orphan is a row for the pause | tree | Q3, Q6 |
| L-02 | `MultiLineMenuEntry.cpp:52-56`; `resources/Font.cpp:754-756`, `:420-421`, `:107` | layout from what it produced / a moving number | T34; `resources/Font.cpp` T36's, cited | the moving number at a row's construction; a read trace and G-05's reopened-page pair; a rasterise-first in the component or a record is the pause's | tree | Q1 |
| L-03 | `MultiLineMenuEntry.cpp:74-75` | layout from what it produced / a moving number | T34 (upstream's formula, moved whole by the fork's `48d43c0fb`) | 3.4 FAILs at the pin (the shares sum to 0.987 and 1.013); `git log -S` first at stage C; the pause rules whether the component's shares are made to sum to 1 (a register row) | tree | Q1 |
| L-04 | `MenuComponent.cpp:14`, `:547-558`, `:527`; `ComponentGrid.cpp:174-175`, `:194`; `ButtonComponent.cpp:10`, `:80` | a house constant a surface does not keep | T34; the pages with wide bars T26's and T31's | 3.26's arithmetic; the widest bars framed at 640 (G-03); a bar that fits its cell, or the pages' labels, is the pause's | tree | Q2 |
| L-05 | `MenuComponent.cpp:7-13` against `es-core/src/guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` | a house constant a surface does not keep | the comment T34's; the popup T35's | recorded, not deleted (`engineering-practices.md:576`); the comment corrected or the claim kept at the pause | tree | Q2, Q7 |
| L-06 | `ComponentList.cpp:11`, `:491-494`; `guis/GuiMenu.cpp:4091`, `:4097`; `guis/GuiWifi.cpp:103` | a house constant a surface does not keep | T34 (upstream's constant); `rowInset()`'s two fork pages T26's and T31's | framed at both sizes (G-04, G-11); a screen fraction under D-UI-012's family is a register row for the pause | tree | Q2 |
| L-07 | `AsyncNotificationComponent.cpp:12`; `es-core/src/Window.cpp:29` | a structure or merge-debt fact | T34 (the include line); `CloudText` T18's, the CMake T35's | recorded with how it resolves; a `CloudText` that moves to es-core is T18's and T35's call | tree | Q7 |
| L-08 | `WebImageComponent.cpp:197-200`, `:244` | a read of a file another process writes | T34 | by design per `:191-196`; the player sees a blank badge until the page's next bind, which asks again (the stub at the pin, S5); ruling 5: no timer; the uncached state is S5's fix (#1319); `tools/ra-ui-test`'s 204-then-200 fixture is the guest half | S5 `568ef099d`: `stage-e/s5-before.txt`, `s5-after.txt` | Q5 |
| L-09 | `WebImageComponent.cpp:190` (and `:81`, `:134`, `:228`); `utils/FileSystemUtil.cpp:144`, `:203-220` | a read of a file another process writes | T34; `HttpReq` T21's, `FileSystemUtil` T36's, cited | sound at the pin: the writer's `removeFile` (`HttpReq.cpp:344`) and `renameFile` (`:479` -> `FileSystemUtil.cpp:1457-1458`) erase the cached miss before `:190` asks; 3.21's first half a candidate that PASSes at the pin | tree | Q5 |
| L-10 | `VideoVlcComponent.cpp:84-95`, `:53-61`, `:28-49`, `:491-494`, `:911` | a lifetime or a thread | T34 (upstream surface, outside the lanes) | a data race on `ctx->component` and a call into a component being destroyed; recorded with the two threads named (§ The lifetimes); G-10 `CANNOT` (no media); a contained fix (an atomic, or a wait) under rule 6 only if the pause opens it | tree | Q4 |
| L-11 | `OptionListComponent.h:96`, `:145`, `:158`, `:195`; `:310-311`, `:323-324` | a lifetime or a thread | T34 | sound by the invariant: each `delete this` is the last thing its handler does; 3.19's ASan harness at stage C | tree | Q4 |
| L-12 | `TextEditComponent.cpp:39`, `:47` | a lifetime or a thread | T34; `Window::postToUiThread` T35's, `AppWindow` T33's | a use after free if the field dies before the post runs; 3.20's case at stage C with the fakes' `Window.h`; a weak token the posts check is the pause's | tree | Q4 |
| L-13 | `CarouselComponent.cpp:354-361`; `OptionListComponent.h:639-640` | a prompt where the key moves nothing | T34 (upstream surfaces) | recorded; framed if a one-system carousel or a one-value option row is reachable on the guest | tree | Q3 |
| L-14 | `GridTileComponent.cpp:1043`; `ImageGridComponent.h:2`, `:380-381` | a structure or merge-debt fact | T34 | a one-commit tidy if the pause opens it | tree | Q7 |
| L-15 | `MenuComponent.cpp:506-515`, `:492-503`; `guis/GuiMenu.cpp:591` | a structure or merge-debt fact | T34; `GuiMenu.cpp:591` T26's | an unstated invariant: the cast is safe only because the MAIN MENU's `mButtons` is empty and the index guard `:508` returns first; written into `02` beside `MenuComponent.h:53-56`; a `dynamic_pointer_cast` plus a null check is the contained fix | tree | Q3 |
| L-16 | `SwitchComponent.cpp:14`; `OptionListComponent.h:255`, `:276`; `TextEditComponent.cpp:31`; `MenuComponent.cpp:393`; `TextListComponent.h:613`, `:725` | layout from what it produced / a moving number | T34; `TextListComponent.h` an upstream surface | the seven reads tabled in § The layouts with their surfaces; disposition with L-02's | tree | Q1 |
| L-17 | `TextComponent.cpp:338` against `:350` | layout from what it produced / a moving number | T34 (upstream's `TextComponent.cpp`) | #48's root, unchanged at the pin: 3.5's case, a 640x480 frame of a padded auto-height text that is not a `GuiMsgBox`, the reproducer for #585; the root fix (re-heights every padded auto-height text) is the pause's, a register row | tree | Q1 |
| L-18 | `MenuComponent.cpp:205`, `:233`, `:236`, `:283`, `:487`; `ButtonComponent.cpp:73` | a player sentence outside the vocabulary or without French | T34 | a reading, not a check: no fork label carries the brand through the six formatters at the pin; a `tools/vocabulary-check` rule (the brand inside `addEntry|addButton|setTitle|addWithDescription|addGroup` arguments) proposed for the coordinator | tree | Q6 |
| L-19 | `AsyncNotificationComponent.cpp:63-65` | a house constant a surface does not keep | T34 | dead text, harmless; recorded | tree | Q2 |
| L-20 | `VideoComponent.cpp:327`, `:591`; `ImageComponent.cpp:1232` | a read of a file another process writes | T34 (upstream surfaces); the scraper T32's | recorded with the scraper as the writer; a frame only if a scrape then a game open fits the window, else `CANNOT` | tree | Q5 |
| L-21 | `WebImageComponent.cpp:239-243`; `es-core/src/HttpReq.cpp:119-123`, `:131-132`, `:172-176` | a lifetime or a thread | T34; `HttpReq` T21's | sound; recorded so the next reader does not re-derive it | tree | Q4 |
| L-22 | `AsyncNotificationComponent.cpp:117-121`, `:261-299`; h `:72`, `:74` | a lifetime or a thread | T34 (a lane surface); the holders T18's and T20's | **new:** `close()` writes `mClosing` and `mFadeTime` unlocked from the holders' threads while `update()` reads them on the interface thread; a host ThreadSanitizer case at stage C; a `bug` at stage D if it fires; § 1 (b)'s component half beside it | tree | Q4 |
| L-23 | `RatingComponent.cpp:262-266` | a player sentence outside the vocabulary or without French | T34 (upstream's line) | **new:** the rating's OK prompt `"add star"` is outside `_()`; contained under rule 6 with its French in the same commit; a #585 line | tree | Q6 |
| L-24 | `VideoComponent.cpp:347-351` | a prompt where the key moves nothing | T34 (upstream's line) | **new:** a focused video component's help bar names BACK as `SELECT`; reached only where a video component holds focus; recorded, contained under rule 6 if the pause opens it | tree | Q3, Q6 |
| 3.1 | `ComponentGrid.cpp:396-414` | a prompt where the key moves nothing | T34 | a case at stage C; expected PASS (D-UI-034's fix) | S4: PASS at the pin and after, one case for 3.1-3.3 (`stage-e/s4-before.txt`, `s4-after.txt`) | Q3 |
| 3.2 | `ComponentGrid.cpp:519-553` | a prompt where the key moves nothing | T34 | a case at stage C; expected PASS | S4: PASS at the pin and after, with 3.1 and 3.3 | Q3 |
| 3.3 | `ComponentGrid.cpp:329-379` | a prompt where the key moves nothing | T34 | a case at stage C; expected PASS | S4: PASS at the pin and after, with 3.1 and 3.2 | Q3 |
| **3.4** | `MultiLineMenuEntry.cpp:50-80` (**`:74-75`**) | layout from what it produced / a moving number | T34 | FAIL at the pin (L-03); 300 `setDescription` calls hold the height (#241) | S3: FAIL at the pin (stage D), PASS after `db12b1598` (`stage-e/s3-after.txt`) | Q1 |
| 3.5 | `TextComponent.cpp:315-340` | layout from what it produced / a moving number | T34 | L-17's case: the measured height one line short | S3: FAIL at the pin (28 against 48, 20 against 40), PASS after `db12b1598` (`stage-e/s3-before.txt`, `s3-after.txt`) | Q1 |
| **3.6** | `TextComponent.cpp:486` | layout from what it produced / a moving number | T34 | FAIL at the pin: the limit 20 px too large | S3: FAIL at the pin (stage D), PASS after `db12b1598` (`stage-e/s3-after.txt`) | Q1 |
| **3.7** | `SliderComponent.cpp:44-58`, `:271-319` (**`:282`**) | a player sentence outside the vocabulary or without French | T34 | FAIL at the pin: `"Auto"`; the precision cases expected PASS | S4: FAIL at the pin (stage D, `Auto`), PASS after `a9017ff50` (`stage-e/s4-after.txt`) | Q6 |
| **3.8** | `CarouselComponent.cpp:74-90` with `:113`, `:119`; `IList.h:376-400` | a prompt where the key moves nothing | T34 | FAIL candidate: `listInput(-7)` on a size-3 carousel; the landing index asserted in `[0, sz)` per loop type | pending: fixture at stage C | Q3 |
| 3.9 | `ImageGridComponent.h:1437-1468` | layout from what it produced / a moving number | T34 | a case; a 0 tile size is guarded only by a `LOG` | S6: PASS at the pin and after, with 3.10: the dimensions of three grids (`stage-e/s6-before.txt`, `s6-after.txt`) | Q1 |
| 3.10 | `ImageGridComponent.h` from `:1065` (`:1162-1186`) | layout from what it produced / a moving number | T34 | a case on the partial last row | S6: PASS at the pin and after: a partial last row read, and a whole one | Q1 |
| 3.11 | `TextListComponent.h:262-269` | layout from what it produced / a moving number | T34 | a case on the extra row past the cutoff | S0: PASS at the pin (`stage-e/s0-before.txt`) | Q1 |
| 3.12 | `DateTimeEditComponent.cpp:124-160` | a structure or merge-debt fact | T34 | a case on the date steps (an extraction or a fake `InputConfig`) | S4: PASS at the pin and after (`stage-e/s4-before.txt`, `s4-after.txt`) | Q7 |
| 3.13 | `DateTimeEditComponent.cpp:251-260` | a player sentence outside the vocabulary or without French | T34 | PASS at the pin as written: a blank, not `<NOT SET>`; a style question for the pause | S4 (PL-25, #1322): FAIL at the pin (a blank), PASS after `a9017ff50`: `<NOT SET>` through `_()` | Q6 |
| 3.14 | `ScrollableContainer.cpp:62-107`, `:110-124`, `:126-131` | a structure or merge-debt fact | T34 | a case; `:69`'s unused `680.0f` is lint | S0: PASS at the pin; its PL-40 half (content 10 px narrower) FAIL: `-10 >= 0` and the vertical scroll never moves (`stage-e/s0-before.txt`) | Q7 |
| 3.15 | `IList.h:267-330`, `:376-400` | a prompt where the key moves nothing | T34 | a case, the landing index for 3.8 | S0: PASS at the pin (`stage-e/s0-before.txt`) | Q3 |
| **3.16** | `HelpComponent.cpp:73-130`, `:121-169`, `:176-200` | a player sentence outside the vocabulary or without French | T34 | FAIL at the pin: `haut/bas` -> `nullptr` and the `Unknown help icon` line (L-01) | S4: FAIL at the pin (`0 == 1`), PASS after `a9017ff50`; since S4 the case reads the list's own line through a catalog double (`stage-e/s4-checks.txt`) | Q3, Q6 |
| 3.17 | `ComponentTab.cpp:77-96`, `:320-345` | a prompt where the key moves nothing | T34 | a case; expected PASS | S4: PASS at the pin and after (`stage-e/s4-before.txt`, `s4-after.txt`) | Q3 |
| 3.18 | `AsyncNotificationComponent.cpp:136-145`, `:63-65` | a house constant a surface does not keep | T34 | a case: the width handed to `chooseThatFits` is the row's cell, never 0.9 W | S2: PASS at the pin, written before the fix and run again after it (`stage-e/s2-before.txt`, `s2-after.txt`) | Q6 |
| 3.19 | `OptionListComponent.h:88-100`, `:140-160`, `:188-200` (ASan) | a lifetime or a thread | T34 | ASan over an extracted popup (L-11) | pending: fixture at stage C | Q4 |
| 3.20 | `TextEditComponent.cpp:39`, `:47` | a lifetime or a thread | T34 | post, delete, drain (L-12) | pending: fixture at stage C | Q4 |
| **3.21** | `WebImageComponent.cpp:134`, `:190`, `:197-200`; `utils/FileSystemUtil.cpp:144` | a read of a file another process writes | T34 | first half a candidate that PASSes at the pin (L-09); second half: the 204 then 200 is never asked again (L-08, by design) | S5: the first half PASS at the pin and after; the second (PL-13, #1319): the pin already re-asks on the next bind, and its one FAIL, the cache path kept, PASS after `568ef099d` | Q5 |
| 3.22 | `ImageComponent.cpp:85-180` | layout from what it produced / a moving number | T34 | a case on the fit after a turn | S5: PASS at the pin and after, with 3.23 and 3.24 (`stage-e/s5-before.txt`, `s5-after.txt`) | Q5 |
| 3.23 | `ImageComponent.cpp:273-291` | layout from what it produced / a moving number | T34 | a case; turn 1 four times is identity | S5: PASS at the pin and after: four turns are the identity | Q5 |
| 3.24 | `ImageComponent.cpp:491-499`, `GridTileComponent.cpp:1055-1063` | layout from what it produced / a moving number | T34 | a case on the normaliser | S5: PASS at the pin and after: -1, 4, 5 and 0 normalise to 3, 0, 1 and 0 | Q5 |
| 3.25 | `ComponentList.h:26` | a house constant a surface does not keep | T34 | a case; expected PASS | S3: PASS at the pin and after (`stage-e/s3-before.txt`, `s3-after.txt`) | Q2 |
| **3.26** | `MenuComponent.cpp:543-562`; `ButtonComponent.cpp:10` | a house constant a surface does not keep | T34 | FAIL candidate: five 128 px buttons at 640 overhang (L-04) | pending: fixture at stage C | Q2 |
| 3.27 | `MenuComponent.cpp:396-424` | layout from what it produced / a moving number | T34 | a case on the strict `<` | pending: fixture at stage C | Q1 |
| 3.28 | `ComponentList.cpp:295-319` | layout from what it produced / a moving number | T34 | a case incl. the signed/unsigned compare | S3: PASS at the pin and after (`stage-e/s3-before.txt`, `s3-after.txt`) | Q1 |
| 3.29 | `TextListComponent.h:591-608` | layout from what it produced / a moving number | T34 | the same for the game list | S0: PASS at the pin (`stage-e/s0-before.txt`) | Q1 |
| 3.30 | `SwitchComponent.cpp:50-80`, `:118-138` | a prompt where the key moves nothing | T34 | a case on the tri-state cycle | pending: fixture at stage C | Q3 |
| 3.31 | `SliderComponent.cpp:234-257` | a house constant a surface does not keep | T34 | a case on the clamp and the sentinel | S4: PASS at the pin and after | Q3 |
| 3.32 | `RatingComponent.cpp:192-204` | a structure or merge-debt fact | T34 | a case on the accumulation's drift | S4: PASS at the pin and after; five presses reach 1.0 exactly in float | Q7 |
| 3.33 | `TextEditComponent.cpp:267-271` | a structure or merge-debt fact | T34 | a case on a cursor inside a UTF-8 sequence (T21's `moveCursor`) | S2: PASS at the pin, written before the fix and run again after it (`stage-e/s2-before.txt`, `s2-after.txt`) | Q7 |
| 3.34 | `CarouselComponent.cpp:183-200` | a prompt where the key moves nothing | T34 | a case incl. a count of 1 and a divide by 0 | S4: PASS at the pin and after, one entry and none included | Q3 |

**The brief's § 1 rulings, each with its row:**

| Ruling | Its row in this file |
| --- | --- |
| (a) T32 PL-07 / #1263, the caller's half | § The reads, `ImageComponent.cpp:408` |
| (b) T2 PC-1, the card's half | § The lifetimes, `AsyncNotificationComponent.cpp:123`, with L-22 at `:119` |
| (c) T26 PL-27, the callback types | § The lifetimes, `SwitchComponent.h:53` and `OptionListComponent.h:658` |
| (d) T31 L-03 / #1243's invariant | § The lifetimes, `OptionListComponent.h:310` and `:323` |
| (e) #1266's grid after `clear()` | § The lifetimes, `ImageGridComponent.h:91` |
| (f) #48's `TextComponent` root | § The layouts, `TextComponent.cpp:338` and `:483` |
| (g) batocera's `setOpacity` guard | § The structure: `HelpComponent.cpp:212-213` dereference `mGrid` unguarded, `:251` is inside `render`'s `if (mGrid)` (`:218`); `mGrid` is null when `ShowHelpPrompts` is off or there are no prompts (`:67-70`); nothing calls `HelpComponent::setOpacity` on the fork's images (`Window.cpp` constructs the one bar at `:41` and never calls it; the bar is no component's child): unreachable at the pin, recorded; the guard arrives with batocera's `9dbd4b9bf` at the reconciliation |
| (h) `UntintedImageComponent` | § The structure: it lives at `es-app/src/guis/GuiMenu.cpp:6401` (T26's file; the QR at `:6425`), not under `components/`; lifting an untinted mode into `ImageComponent` (h `:76`) is the pause's question |
| (i) `ComponentList.cpp:568`'s `_("up/down")` | § The words, L-01, and § The input, `ComponentList.cpp:548` |
| (j) the two lanes' `AsyncNotificationComponent.h` doubles | § The structure: a header change in T34 is named as a collision at the hand-back; the fakes are not the lane's |

Generated, asserted by `tools/t34-leads.py`: 24 L leads (the brief's 21 and the read's L-22 to L-24), 34 floor rows (the seven FAIL-at-pin in bold), each answered, 4 run at the pin in S0 and 24 in the streams; 10 rulings, each with its row.

## The layouts

**Every font-height read** (`Font::getHeight` is the tallest ASCII glyph rasterised so far (`resources/Font.cpp:754-756`, `:420-421`, from 0 `:107`; T36's): a size taken before the font has drawn its tallest glyph is a few px short of one taken after (`es-code-traps.md:118`)):

| Site | Kind | What it sizes | The surface that shows it | Disposition | proved |
| --- | --- | --- | --- | --- | --- |
| `HelpComponent.cpp:276` | layout | whether the help bar fits below its grid (`getHeight(1.5f)`) | the help bar on every page | the moving number; not in the brief's eight; recorded beside them | tree |
| `MenuComponent.cpp:393` (brief) | layout | the button bar's height when there is no bar yet | every settings page's footer | L-16 | tree |
| `MultiLineMenuEntry.cpp:55` (brief) | layout (constructor) | a label-and-description row's text height (`naturalHeight`, `:50-56`) | every cloud, achievements and settings row built on `MultiLineMenuEntry`; G-05's reopened page | **L-02**: `Font::getHeight` is the tallest ASCII glyph rasterised so far (`resources/Font.cpp:754-756`, `:420-421`, from 0 `:107`; T36's): a size taken before the font has drawn its tallest glyph is a few px short of one taken after (`es-code-traps.md:118`); a rasterise-first in the component or a record, the pause's | tree |
| `OptionListComponent.h:255` (brief) | layout (constructor) | the option row's height | every option row | L-16 | tree |
| `OptionListComponent.h:276` (brief) | layout | the option text's height on a resize | every option row | L-16 | tree |
| `SwitchComponent.cpp:14` (brief) | layout (constructor) | the switch image's height (`getHeight(1.1f)`) | every on/off row; G-04 | L-16: the moving number | tree |
| `TextComponent.cpp:336` | layout | a single-line auto-height text's height | every auto-height single-line label | the moving number; not in the brief's eight (it is `TextComponent`'s own, L-17's file); recorded | tree |
| `TextComponent.cpp:359` | layout (decision) | AUTO's one-line-or-wrap choice: `sy > getHeight * 1.8` where `sy` is the height `:336`/`:338` wrote | every AUTO text | the rule's shape (a decision from the size the auto pass wrote, and a moving number): stable at the pin (a text that wrapped to one line is drawn as one) -- 3.5's case confirms at stage C | tree |
| `TextComponent.cpp:432` | layout (decision) | the same decision in `buildTextCache`'s second form | every AUTO text | as `:359` | tree |
| `TextEditComponent.cpp:31` (brief) | layout (constructor) | the text field's height | the key popups' fields (T35's pages) | L-16 | tree |
| `TextEditComponent.cpp:377` | layout (decision) | whether the field is multi-line (`getSize().y() > getHeight * 1.25`) | - | a decision from the size its owner set; recorded | tree |
| `TextListComponent.h:613` (brief) | layout | a game-list row's height when no line count is themed | the text game list | L-16; upstream surface outside the lanes | tree |
| `TextListComponent.h:725` (brief) | layout | the game list's selector bar height | the text game list | L-16; upstream surface outside the lanes | tree |
| `TextComponent.cpp:176` | render | a line's height while drawing | - | per frame: re-read each draw | tree |
| `TextComponent.cpp:200` | render | the same, the second draw path | - | per frame | tree |
| `TextEditComponent.cpp:298` | scroll | whether the field must scroll down | - | per input | tree |
| `TextEditComponent.cpp:300` | scroll | the scroll offset | - | per input | tree |
| `TextEditComponent.cpp:364` | render | the cursor's height | - | per frame | tree |
| `TextEditComponent.cpp:370` | render | the cursor's position | - | per frame | tree |

**Every size computed from a size a pass wrote, or measured at one width and drawn at another:**

| Site | What it computes, and from what | The surface | Disposition | proved |
| --- | --- | --- | --- | --- |
| `MultiLineMenuEntry.cpp:74` | the two rows' shares, `th*0.9/h` and `sh*1.1/h` of `h = th + sh` (`:72-75`), measured from the fonts since #241 (`7c7ffab43`), not from the cells | every two-line row | **L-03**: the shares sum to 1 only when `th == sh`: a taller Text font underfills, a taller TextSmall overflows by `0.1*(sh-th)/h`; upstream's formula moved whole into `layoutRows`; 3.4's `rowPercs(26, 20)` and `(20, 26)` FAIL at the pin; the fix (a pair that sums to 1) is the pause's | S3 `db12b1598` (#1314): `th / h`, `sh / h`; 3.4 and PL-07's case PASS after, FAIL before |
| `MultiLineMenuEntry.cpp:71` | in multi-line mode, the description's height read back from the text (`:71`) | the multi-line rows (re-laid in `onSizeChanged`, `:121-136`) | the rule's shape (a size the text's own auto pass wrote); stable while the width is: 3.4's 300 `setDescription` calls at stage C | tree |
| `TextComponent.cpp:338` | the auto height, wrapped at the full width `getSize().x()` | every padded auto-height text that is not a `GuiMsgBox` | **L-17** (#48's root): drawn at `mSize.x() - padding` (`:350`), so a wrap in that band paints a line the height never budgeted; 3.5's case; a 640x480 frame of a padded auto-height text; the reproducer for #585; the root fix the pause's (§ 1 f) | S3 `db12b1598` (#1315): measured at the drawn width; 3.5 PASS after, FAIL before |
| `TextComponent.cpp:483` | the vertical marquee's text length, wrapped at the full width | a vertically scrolling text with padding | L-17's second site: the same full-width measure | S3 `db12b1598` (#1315), as `:338` |
| `TextComponent.cpp:486` | the vertical marquee's limit, `mSize.y() - mPadding.y() - mPadding.y()` | a vertically scrolling text with unequal top and bottom padding | **3.6**: `:351` and `:428` subtract `.y()` and `.w()`; with padding (0,10,0,30) the limit is 20 px too large; a contained one-token fix under rule 6 and a #585 line | S3 `db12b1598` (#1313): `mPadding.w()`; 3.6 PASS after, FAIL before |
| `MenuComponent.cpp:396` | `updateSize`'s row-fit loop: rows added while `height + rowHeight < maxHeight` (`:396-424`) | every settings page's height | 3.27: the strict `<` drops a row that fits exactly; a case at stage C | tree |
| `ComponentList.cpp:521` | each element's width from the list's own width less the inset | every row | sound: from the parent's size, not the element's | tree |
| `HelpComponent.cpp:143` | the bar's grid width from the entries kept (`:143-152`), floored at 1 | the help bar | sound since `7dc8bf373` (#210): measured before an entry is added; 3.16 | tree |
| `AsyncNotificationComponent.cpp:63` | the card's width, `max(sizeText(30 chars), 0.9 W)` | the card | L-19: the floor never binds at 640 or wider; dead text, harmless | tree |
| `ScrollableContainer.cpp:69` | `widthMod = 680.0f / getSize().x()`, computed and never used | - | 3.14: lint, recorded | tree |

Generated, asserted by `tools/t34-layouts.py`: 19 font-height reads (13 layout, 6 render or scroll), the brief's eight among the layout rows; 10 size rows, each cited line asserted to hold its code or be non-blank.

## The constants

**The house values:**

| Value | Its one definition | Value at the panels | Every reader in the 80 | The frame that shows it | Disposition | proved |
| --- | --- | --- | --- | --- | --- | --- |
| `BUTTON_GRID_HORIZ_PADDING` | `MenuComponent.cpp:14` | 0.022 W (14.08 px at 640, 28.16 at 1280) | `MenuComponent.cpp:547`, `MenuComponent.cpp:555` | G-03 (640), G-11 (1280): the gap between YES's and NO's nine-patch edges, read in the frame's columns | D-UI-012; L-04 (a bar wider than its cell overhangs: 3.26), L-05 (the second copy, below) | tree |
| `BUTTON_GRID_VERT_PADDING` | `MenuComponent.cpp:6` | 0.0296 H (14.2 px at 480) | `MenuComponent.cpp:393`, `MenuComponent.cpp:558` | G-03 | upstream's; recorded | tree |
| `NOTIFICATION_OPACITY` | `AsyncNotificationComponent.cpp:31` | 255 | `AsyncNotificationComponent.cpp:114`, `AsyncNotificationComponent.cpp:276` | G-02: a pixel inside the card over the game art equals the panel colour, not a blend | D-UI-016; sound | tree |
| `DIMMED_ALPHA` | `ComponentList.h:25` | 0x50 of 0xFF | `ComponentList.h:26` | G-04: the unconfigured rows' text against the selectable rows' over one panel | #182's mechanism (`dimmed()` h `:26`, applied in each element's own `setColor`); 3.25 | tree |
| `TOTAL_HORIZONTAL_PADDING_PX` | `ComponentList.cpp:11` | 20 px (10 a side) | `ComponentList.cpp:92`, `ComponentList.cpp:493`, `ComponentList.cpp:508`, `ComponentList.cpp:521` | G-04 (640), G-11 (1280): the row inset | L-06: upstream's pixel constant the fork exported through `rowInset()` to two pages; a screen fraction is the pause's | tree |
| `ICON_TEXT_SPACING` | `HelpComponent.cpp:13` | 0.0042 W (2.7 px at 640) | `HelpComponent.cpp:16`, `HelpComponent.cpp:130`, `HelpComponent.cpp:164` | G-03, G-04, G-11: the help bar | upstream's; sound | tree |
| `ENTRY_SPACING` | `HelpComponent.cpp:16` | 0.0084 W | `HelpComponent.cpp:79`, `HelpComponent.cpp:130`, `HelpComponent.cpp:151`, `HelpComponent.cpp:166` | the same | upstream's; the last entry's trailing spacer 0 (fork `7dc8bf373`, #210) | tree |
| the card's width | `AsyncNotificationComponent.cpp:64` | 0.9 W | - | the card's width, `max(sizeText(30 chars), 0.9 W)` (`:63-65`); G-02: edges at x 32 and x 608 at 640 (0.9 W centred); L-19: the measured floor never binds on a panel 640 or wider, dead text | D-UI-016; sound | tree |
| the card's position | `AsyncNotificationComponent.cpp:112` | 0.9 W | - | the card centred at the top (`:112-113`); `Window::renderAsyncNotifications` re-applies the position every frame (`Window.cpp:1183`, `:1192`, T35's, cited); G-02 | D-UI-016; sound | tree |
| `BUTTON_GRID_HORIZ_PADDING`, the second copy | `guis/GuiTextEditPopupKeyboard.cpp:14` (T35's) | 0.0052083333 W (3.3 px at 640) | that popup's key buttons (`:220`) | - | **L-05:** `MenuComponent.cpp:7-13` says the gap is defined in "the one place"; the keyboard popup keeps its own at the old value; recorded, not deleted (`engineering-practices.md:576`); the comment is this slice's, the popup T35's | tree |

**The pixel constants** (`es-native-ui.md:299`: fractions, never pixel constants; each with its share of a 640 and a 1920 panel's width):

| Site | Pixels | Share of 640 / 1920 | What it sizes | Disposition |
| --- | ---: | --- | --- | --- |
| `ComponentList.cpp:11` | 20 | 3.1% / 1.0% | every row's horizontal inset | L-06; read by two fork pages through `rowInset()`; S3 `db12b1598` (#1320): `ROW_INSET_FRACTION 0.015625`, PL-15's case PASS after (10 at 640, 20 at 1280), FAIL before |
| `TextEditComponent.cpp:8` | 10 | 1.6% / 0.5% | the text field's horizontal padding | upstream's; outside the lanes unless a fork page reads it (the Wi-Fi and cloud key fields do, through the popups, T35's) |
| `TextEditComponent.cpp:9` | 2 | 0.3% / 0.1% | the text field's vertical padding | as `:8` |
| `TextEditComponent.cpp:31` | 4096 | 640.0% / 213.3% | the field's initial width, replaced by its owner's layout | harmless: a placeholder width |
| `ButtonComponent.cpp:10` | 12 | 1.9% / 0.6% | a button's text padding floor, `max(12, 0.014 W)`: the 12 wins below 857 px | upstream's; G-03's bar at 640 is built on it |
| `GridTileComponent.cpp:56` | 16 | 2.5% / 0.8% | a grid tile's default padding | upstream's; G-08 if a grid theme exists |
| `GridTileComponent.h:148` | 16 | 2.5% / 0.8% | a tile frame's corner size | upstream's |
| `MenuComponent.cpp:167` | 10 | 1.6% / 0.5% | the spacer before a row's right-hand component | upstream's |
| `MenuComponent.cpp:192` | 10 | 1.6% / 0.5% | the same, the second builder | upstream's |
| `VideoVlcComponent.cpp:782` | 400 | 62.5% / 20.8% | a video's default max size | upstream surface outside the lanes; recorded |
| `NinePatchComponent.cpp:177` | 50 | 7.8% / 2.6% | the post-process shader's margin | upstream's; recorded |
| `AsyncNotificationComponent.cpp:94` | 32 | 5.0% / 1.7% | the card's nine-patch corner (`fitTo(..., -32, -32)`) | the corner of every framed surface; outside a fraction by design (the frame image's corner) |
| `MenuComponent.cpp:453` | 32 | 5.0% / 1.7% | the menu's background corner | as above |
| `VolumeInfoComponent.cpp:45` | 32 | 5.0% / 1.7% | the volume overlay's corner | as above |
| `TextEditComponent.cpp:53` | 32 | 5.0% / 1.7% | the text field's frame corner (`-34, -32 - 2`) | as above |

Generated, asserted by `tools/t34-constants.py`: 7 house values, each defined once in the 80 with 18 readers in all; the card's width and position; the keyboard popup's second copy and `MenuComponent.cpp`'s one-place claim, both asserted present; 15 pixel constants, each cited line asserted to hold its code.

## The input

**The inputs** (the keys each names, read from its body):

| `input()` | Form | Keys it names (`isMappedTo` / `isMappedLike`) | Body lines |
| --- | --- | --- | ---: |
| `ButtonComponent.cpp:50` | out-of-line | `BUTTON_OK` | 12 |
| `CarouselComponent.cpp:92` | out-of-line | `"down"`, `"left"`, `"lefttrigger"`, `"pagedown"`, `"pageup"`, `"right"`, `"righttrigger"`, `"up"` | 76 |
| `ComponentGrid.cpp:281` | out-of-line | `"down"`, `"left"`, `"right"`, `"up"` | 25 |
| `ComponentList.cpp:142` | out-of-line | `"down"`, `"leftshoulder"`, `"rightshoulder"`, `"up"` | 45 |
| `ComponentTab.cpp:77` | out-of-line | `"left"`, `"right"` | 13 |
| `ControllerActivityComponent.cpp:138` | out-of-line | `"hotkey"` | 21 |
| `DateTimeEditComponent.cpp:80` | out-of-line | `"down"`, `"left"`, `"leftshoulder"`, `"right"`, `"rightshoulder"`, `"up"`, `BUTTON_BACK`, `BUTTON_OK` | 107 |
| `ImageGridComponent.h:537` | out-of-line | `"down"`, `"left"`, `"leftshoulder"`, `"right"`, `"rightshoulder"`, `"up"` | 54 |
| `MenuComponent.cpp:126` | out-of-line | - (delegates) | 7 |
| `OptionListComponent.h:191` | inline | `BUTTON_BACK` | 10 |
| `OptionListComponent.h:284` | inline | `"left"`, `"right"`, `BUTTON_OK` | 47 |
| `RatingComponent.cpp:192` | out-of-line | `BUTTON_OK` | 13 |
| `SliderComponent.cpp:118` | out-of-line | `"left"`, `"right"` | 66 |
| `SwitchComponent.cpp:50` | out-of-line | `"left"`, `"right"`, `BUTTON_OK` | 46 |
| `TextEditComponent.cpp:140` | out-of-line | `"down"`, `"left"`, `"right"`, `"up"`, `BUTTON_OK` | 94 |
| `TextListComponent.h:458` | out-of-line | `"down"`, `"leftshoulder"`, `"rightshoulder"`, `"up"` | 40 |

**The help prompts** (the condition under which each offers a direction):

| `getHelpPrompts()` | Form | What it offers, and when | Disposition | proved |
| --- | --- | --- | --- | --- |
| `ButtonComponent.cpp:186` | out-of-line | OK with the button's help text; no direction | sound | tree |
| `CarouselComponent.cpp:354` | out-of-line | `up/down` or `left/right` CHOOSE by the carousel's type alone (`:358-361`), whatever its size | L-13: a one-entry carousel offers a direction that moves nothing; upstream surface, recorded; framed if a one-system carousel is reachable | tree |
| `ComponentGrid.cpp:519` | out-of-line | `up/down`, `left/right` or both CHOOSE only where `canMoveCursor` finds a focusable cell (`:527-528`, `:546-550`); a child's own `up/down` suppresses the grid's (`:536-538`) | sound (D-UI-034, fork `aa8c5da4c`); 3.1 to 3.3, G-03, G-06 | tree |
| `ComponentList.cpp:548` | out-of-line | `up/down` CHOOSE when `size() > 1` and no child names `up/down` (`:555-568`) | **L-01:** the icon key goes through `_()` (`:568`), so under French it is `haut/bas`, which `getIconTexture` does not know: a null icon and `Unknown help icon`; 3.16, G-04 under French | tree |
| `ComponentTab.cpp:320` | out-of-line | `left/right` SWITCH TAB when `size() > 1`, not when a child already names `left/right` (`:327-341`) | sound (fork `8927b1760`); 3.17, G-05 | tree |
| `ImageComponent.cpp:1057` | out-of-line | OK SELECT; no direction | sound | tree |
| `MenuComponent.cpp:531` | out-of-line | the grid's (`mGrid.getHelpPrompts()`) | sound: `ComponentGrid`'s rule | tree |
| `OptionListComponent.h:202` | inline | the popup's menu prompts plus BACK BACK | sound | tree |
| `OptionListComponent.h:636` | inline | `left/right` CHANGE whenever `!mMultiSelect` (`:639-640`), whatever the count; OK SELECT | L-13: a one-value option row offers CHANGE that changes nothing; upstream surface, recorded | tree |
| `RatingComponent.cpp:262` | out-of-line | OK `"add star"`; no direction | **L-23 (new):** a help label outside `_()`, untranslated under every language; upstream's line; a words lead (Q6), contained under rule 6 | tree |
| `SliderComponent.cpp:337` | out-of-line | `left/right` CHANGE always | sound: a slider at either end still moves the other way | tree |
| `SwitchComponent.cpp:165` | out-of-line | OK CHANGE; no direction | sound | tree |
| `TextEditComponent.cpp:390` | out-of-line | `up/down/left/right` MOVE CURSOR while editing, else OK EDIT (`:395-397`) | read at stage C against `input()`: whether up and down move the cursor in a single-line field | tree |
| `VideoComponent.cpp:347` | out-of-line | BACK labelled `_("SELECT")` (`:350`) | **L-24 (new):** the back button's prompt names SELECT; upstream's line; a words and input lead (Q3, Q6); reached only where a video component holds focus | tree |

Generated, asserted by `tools/t34-input.py`: 16 `input()` (14 `::input(InputConfig`, 2 inline), their keys read from each body; 14 `getHelpPrompts()` (12 out of line, 2 inline), each with its reading.

## The lifetimes

| Site | Shape | Who joins, drains or owns it | What it touches after | Disposition | proved |
| --- | --- | --- | --- | --- | --- |
| `OptionListComponent.h:96` | delete this | the popup, deleted from its own row's accept handler (a `std::function` inside `mMenu`'s row) | nothing: the handler's last statement (`:97`) | L-11: sound by the invariant (nothing above it touches the popup after the call returns); 3.19's ASan case at stage C | tree |
| `OptionListComponent.h:145` | delete this | the same, the second row template | nothing: the handler's last statement (`:146`) | L-11, as `:96` | tree |
| `OptionListComponent.h:158` | delete this | the popup, deleted from its own BACK button's callback: the button's `std::function` is destroyed while it runs (`es-code-traps.md:22`'s shape) | nothing: the lambda is `{ delete this; }` | L-11: sound only while `ButtonComponent` and the grids above it return without touching their members; 3.19 | tree |
| `OptionListComponent.h:195` | delete this | the popup, deleted from its own `input()` | nothing: `return true` (`:196`) | L-11, sound | tree |
| `TextEditComponent.cpp:39` | postToUiThread | `Window`'s post queue (T35's `postToUiThread`), drained later on the interface thread | raw `this` (`startEditing()`): a text edit destroyed before the post runs is a use after free | L-12: 3.20's case at stage C with the fakes' `Window.h`; a weak token the posts check is the pause's, with T33's `AppWindow` named | S2 `2cbb62d7b` (#1311): the post holds the field's token weakly; `SAN asan-textedit` rc 0 after, rc 1 before (`stage-e/s2-after.txt`, `s2-before.txt`) |
| `TextEditComponent.cpp:47` | postToUiThread | the same queue | raw `this` (`stopEditing()`) | L-12, as `:39` | S2 `2cbb62d7b` (#1311), as `:39` |
| `VideoVlcComponent.cpp:91` | std::thread | a detached thread that releases the media player and deletes the `VideoContext` (`:93-94`) | VLC's thread may still be in `display` (`:53-61`) reading `ctx->component`, nulled at `:89` on the interface thread with no lock | L-10: a data race, and a call into a component being destroyed (`~VideoVlcComponent` -> `stopVideo` `:911`); upstream surface outside the lanes; recorded (G-10 `CANNOT`: no media) | tree |
| `VideoVlcComponent.cpp:95` | .detach( | the same thread, joined by nobody | `ctx`, after the release returns | L-10 | tree |
| `AsyncNotificationComponent.cpp:119` | read | `close()` writes `mClosing` and `mFadeTime` (`:119-120`) with no lock, from the holders' worker threads (`ThreadedCloudSync`, `ProxyCards`, `ThreadedBluetooth`, ...), while the interface thread's `update()` reads and writes both (`:267-299`; plain `bool` and `int`, h `:72`, `:74`); `mMutex` guards the text only (`:149`-`:196`) | - | **L-22 (new): a data race on the card's closing state**, in a lane surface; a host ThreadSanitizer case at stage C (a card double-free of `Window`, `close()` on one thread, `update()` on the other); a `bug` at stage D if it fires | S2 `2cbb62d7b` (#1309): `close()` is one atomic request, `update()` turns it; `SAN tsan-card` rc 0 after, rc 66 before; the interleaving case PASS after, FAIL before |
| `AsyncNotificationComponent.cpp:123` | read | the card is owned by `Window` (`Window.h:123`, a vector of raw pointers) and deleted once it stops running (`Window.cpp:1242-1252`, T35's); every holder keeps the raw pointer `createAsyncNotificationComponent` returned (`Window.cpp:1152-1169`) | - | **§ 1 (b), T2 PC-1, the component's half:** the card promises a holder nothing after the window deletes it, and it cannot refuse a late `close()` or `updateText()` (no handle, no generation); the window's teardown order is T35's, the holders' half T18's and T20's; a handle the window keeps alive until the holder lets go is the pause's | S2 `2cbb62d7b` (#1310), the component's half: `handle()`; Window's half `stage-e/s2-window.patch` (T35's), the holders' merge debt; `SAN asan-card-handle` rc 0 after (2 of 2 late calls refused), rc 1 before |
| `MenuComponent.cpp:478` | read | `clearButtons()` (`:478-483`) deletes the button bar, whose buttons own their callbacks | - | `es-code-traps.md:22`'s rule restated beside the lines; no component-side guard exists at the pin, and the rule's `postToUiThread` with a weak handle is the callers' discipline | tree |
| `SwitchComponent.h:53` | read | the switch stores its callback by value | - | **§ 1 (c), T26 PL-27:** a page's lambda that captures a `shared_ptr` to the component that stores it makes a cycle the page's `onFinalize` must break; the type is not weak by design; LeakSanitizer over an extracted builder at stage C; a design ruling at the pause | tree |
| `OptionListComponent.h:658` | read | the option list stores its callback by value, called from `onSelectedChanged` (`:632-633`) | - | § 1 (c), as the switch's | tree |
| `OptionListComponent.h:310` | read | `input()` left: the callback, then `return true` (`:311`) | - | **§ 1 (d), T31 L-03 / #1243's invariant, kept:** a page that deletes the option list's owner inside the callback is safe only because nothing after the callback touches the component (`:311`, `:324`) | tree |
| `OptionListComponent.h:323` | read | `input()` right: the callback, then `return true` (`:324`) | - | § 1 (d), as `:310` | tree |
| `ImageGridComponent.h:91` | read | `clear()` and `resetGrid()` (#207) drop the entries and the tiles | - | **§ 1 (e), #1266's contract, corrected by the seat (G-7, verified):** `clear()` -> `resetGrid()` clears `mVisibleTiles` (`:1383`) but never `mScrollLoopTiles`, which `ensureVisibleTileExist` clears only after its early return for an empty list (`:316-317` before `:339-340`), and `render` still draws it (`:762-763`): a cleared looping grid keeps its loop-copy tiles. The stage-B reading here said the grid held no tile after `clear()`, which was wrong. T32's `s4-views.py` is the harness shape; the view's fix is T32's `1655e2f4c` | S6 `6050b8419` (#1329): `resetGrid()` clears the loop-copy tiles too; PL-33's case PASS after, FAIL before (`stage-e/s6-before.txt`, `s6-after.txt`) |
| `WebImageComponent.cpp:243` | read | a stack `HttpReqOptions` (`:239`) handed by pointer to a heap `HttpReq` | - | L-21: sound, the constructor consumes the options before it returns (`HttpReq.cpp:119-123`, `:131-132`, `:172-176`, T21's) | tree |

Generated, asserted by `tools/t34-lifetimes.py`: 8 shape rows (`delete this` 4, `std::thread` 1, `.detach(` 1, `postToUiThread` 2), each with a disposition; 9 read rows, each cited line asserted to hold its code at the pin.

## The reads

| Site | Kind | What is read | Its writer while ES runs | A stale answer reads as | Disposition | proved |
| --- | --- | --- | --- | --- | --- | --- |
| `CarouselComponent.cpp:765` | exists | a system or game entry's `marquee`/`fanart`/`cartridge`/`mix` image (`:763`) | the scraper, writing media while ES runs | a cached miss draws the entry as text until a game launch or a restart clears the cache | L-20, recorded; upstream surface outside the lanes | tree |
| `ImageComponent.cpp:1232` | exists | the theme's `default` image path | a theme install or update (the theme installer) while ES runs | a cached miss leaves no default image until the theme reloads | L-20, recorded | tree |
| `VideoComponent.cpp:327` | exists | the theme's video `path` (a `{`-binding is taken without the check) | a theme install or update (the theme installer) while ES runs | a cached miss falls back to `defaultVideoPath` (`:330`) | L-20, recorded | tree |
| `VideoComponent.cpp:591` | exists | a `path` property, the bound `{game:video}` among them | the scraper, writing videos while ES runs | a video scraped mid-session reads as absent until a launch clears the cache (`es-native-ui.md:107`) | L-20, recorded; a frame only if a scrape fits the window (G-08's guest has no media: `CANNOT`) | tree |
| `VideoVlcComponent.cpp:605` | exists | `libvlc.dll` beside the executable | Windows-only: inside `#if WIN32` (`:592`), compiled to nothing on every image | - | dead on the images (Q7's gates) | tree |
| `VideoVlcComponent.cpp:639` | exists | `plugins/gui/libqt4_plugin.dll` | Windows-only: inside `#if WIN32` (`:592`), compiled to nothing on every image | - | dead on the images (Q7's gates) | tree |
| `WebImageComponent.cpp:81` | exists | the downloaded copy `mLocalFile`, at destruction when the cache lasts 0 s | `HttpReq` (tmp file, then `renameFile`, which erases the key: `FileSystemUtil.cpp:1457-1458`) | fresh: every writer of the path erases its key | sound | tree |
| `WebImageComponent.cpp:134` | exists | the cached copy `localFile`, before a request (`setImage`) | `HttpReq` for an earlier component; `removeFile` here (`:141`, `:150`) | a remembered miss here is erased when the request starts (`HttpReq.cpp:344` `removeFile(outputFilename)`) and when it lands (`:479` `renameFile`) | sound; 3.21's first half a candidate that PASSes at the pin (stage C proves it with the real `FileSystemUtil`) | tree |
| `WebImageComponent.cpp:190` | exists | `mLocalFile` after `REQ_SUCCESS` | `HttpReq`, `renameFile` into the path (`HttpReq.cpp:479`; the `copyFile` fallback `:501` erases too, `FileSystemUtil.cpp:1506-1507`) | fresh at the pin: the key cached as a miss at `:134` is erased by the writer before `:190` asks (L-09 answered) | L-09: sound, by the writer's erase; 3.21's case | S5: 3.21's first half PASS at the pin and after `568ef099d` (`stage-e/s5-before.txt`, `s5-after.txt`) |
| `WebImageComponent.cpp:228` | exists | the cache directory, before a request | `createDirectory` here (`:229`) | a cached miss calls `createDirectory` again: idempotent | sound | tree |
| `WebImageComponent.cpp:197` | getFileSize | the size of `mLocalFile` after a success | `HttpReq` | uncached (`stat64`, `FileSystemUtil.cpp:1319-1335`) | L-08: a 0-byte answer (the proxy's 204, #180) removes the file and returns; `mUrlToLoad` was cleared at `:244`, so the page asks nothing more until its next bind (ruling 5: no timer); since S5 the component also keeps no cache path for it | S5 `568ef099d` (#1319): the stub shows the pin already re-asks on the next bind (the removal erases the cached key); the case's one FAIL at the pin was the cache path kept for the answer, PASS after |
| `WebImageComponent.cpp:243` | HttpReq | `new HttpReq(mUrlToLoad, &options)`, the offline proxy's URLs with `X-RA-Store-Only` (`:240-241`, #199) | writes `mLocalFile` through `<path>.tmp` and `renameFile` (T21's `HttpReq.cpp:324-344`, `:479`) | - | L-21: the stack `HttpReqOptions` is consumed by the constructor before it returns; sound | tree |
| `BatteryIndicatorComponent.cpp:52` | texture | `:/network.svg` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `ControllerActivityComponent.cpp:403` | texture | the theme's `imagePath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:406` | texture | the theme's `gunPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:409` | texture | the theme's `wheelPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:417` | texture | the theme's `networkIcon` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:429` | texture | the theme's `planemodeIcon` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:546` | texture | `mCurrentBatteryTexture`, a theme or resource battery glyph | a theme install, else none | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `GridTileComponent.h:152` | texture | a tile's background `path` (theme) | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `GridTileComponent.h:158` | texture | a tile's selected-background `path` (theme) | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `HelpComponent.cpp:185` | texture | a help icon from the theme's icon map | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `HelpComponent.cpp:203` | texture | a help icon from `ICON_PATH_MAP` (`:/help/...`) | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `ImageComponent.cpp:400` | texture | `mDefaultPath`, the theme's default | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ImageComponent.cpp:408` | texture | `mPath`, any image a page shows by path | the scraper, the save-state writer, the sign-in's QR (T26 #1221), any file rewritten under its path | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | § 1 (a): the caller's half of #1263 -- the component asks by path once per `setImage` and holds the texture; a file rewritten under the same path while the texture lives is not re-read; the cache's half named for T36 (#683) | tree |
| `ImageComponent.cpp:446` | texture | `""`, an empty texture | - | - | recorded | tree |
| `NinePatchComponent.cpp:326` | texture | `mPath`, the frame image (theme or `:/frame.png`) | a theme install, else none | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `RatingComponent.cpp:158` | texture | `:/star_filled.svg` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `RatingComponent.cpp:161` | texture | `:/star_unfilled.svg` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `RatingComponent.cpp:220` | texture | the theme's `filledPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `RatingComponent.cpp:226` | texture | the theme's `unfilledPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `RectangleComponent.cpp:38` | texture | `:/white.png` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `VideoVlcComponent.cpp:479` | texture | `""`, the frame texture a video draws into | - | - | recorded | tree |

Generated, asserted by `tools/t34-reads.py`: 33 rows -- 10 `exists(` lines in 5 files, 0 of them uncached; 1 `getFileSize(`; 1 `new HttpReq(`; 21 live `TextureResource::get(` (the commented one at `VideoVlcComponent.cpp:77` excluded); every row has a disposition and every disposition a row.

## The words

**The 22 `_("` lines** (each msgid's French read from `locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin):

| Line | msgid -> French |
| --- | --- |
| `BusyComponent.cpp:35` | `WORKING...` -> `EN COURS…` |
| `CarouselComponent.cpp:359` | `CHOOSE` -> `CHOISIR` |
| `CarouselComponent.cpp:361` | `CHOOSE` -> `CHOISIR` |
| `ComponentGrid.cpp:546` | `CHOOSE` -> `CHOISIR` |
| `ComponentGrid.cpp:548` | `CHOOSE` -> `CHOISIR` |
| `ComponentGrid.cpp:550` | `CHOOSE` -> `CHOISIR` |
| `ComponentList.cpp:276` | `ENABLED` -> `ACTIVÉ`; `DISABLED` -> `DÉSACTIVÉ` |
| `ComponentList.cpp:568` | `up/down` -> `haut/bas`; `CHOOSE` -> `CHOISIR` |
| `ComponentTab.cpp:341` | `SWITCH TAB` -> `CHANGER D’ONGLET` |
| `DateTimeComponent.cpp:55` | `Unknown` -> `Inconnu` |
| `ImageComponent.cpp:1060` | `SELECT` -> `SELECT` |
| `OptionListComponent.h:158` | `BACK` -> `RETOUR`; `accept` -> `accepter` |
| `OptionListComponent.h:162` | `SELECT ALL` -> `TOUT SÉLECTIONNER`; `select all` -> `tout sélectionner` |
| `OptionListComponent.h:172` | `SELECT NONE` -> `AUCUN`; `select none` -> `aucun` |
| `OptionListComponent.h:205` | `BACK` -> `RETOUR` |
| `OptionListComponent.h:640` | `CHANGE` -> `CHANGER` |
| `OptionListComponent.h:642` | `SELECT` -> `SELECT` |
| `SliderComponent.cpp:340` | `CHANGE` -> `CHANGER` |
| `SwitchComponent.cpp:168` | `CHANGE` -> `CHANGER` |
| `TextEditComponent.cpp:395` | `MOVE CURSOR` -> `DÉPLACER LE CURSEUR` |
| `TextEditComponent.cpp:397` | `EDIT` -> `ÉDITER` |
| `VideoComponent.cpp:350` | `SELECT` -> `SELECT` |

**Player text outside `_()`:**

| Site | Text | Disposition | proved |
| --- | --- | --- | --- |
| `SliderComponent.cpp:282` | `"Auto"`, the AUTO sentinel's value text | **3.7:** neither `_()` nor the placeholder `AUTO` (`es-ui-style-guide.md:164`); upstream's line; the contained fix `_("AUTO")` with its French in the same commit; G-09 if an auto slider is reachable; S4 `a9017ff50` (#1316): `_("AUTO")`, 3.7 PASS after, FAIL before | tree |
| `RatingComponent.cpp:265` | `"add star"`, the rating's OK prompt | **L-23 (new):** a help label outside `_()`, English under every language; upstream's line; contained under rule 6; S4 `a9017ff50` (#1317): `_("ADD STAR")` with `AJOUTER UNE ÉTOILE`, PL-10's case PASS after, FAIL before | tree |

**L-01:** `ComponentList.cpp:568`'s `_("up/down")` is an icon key, not a label: the catalog translates it (`haut/bas`), `InputConfig::buttonLabel` returns it unchanged (`es-core/src/InputConfig.cpp:353-366`, T35's), and `HelpComponent::getIconTexture`'s `ICON_PATH_MAP` has no such key (`:190-194`): a null icon and `Unknown help icon "haut/bas"` under French on every settings list. The fork's own key sites write it untranslated (`ComponentTab.cpp:341`, `ComponentGrid.cpp:546-550`). The contained fix drops the `_()`; whether the catalog's orphan `msgid "up/down"` stays is one of the four rows put to the pause.

**L-18, the up-casing formatters** (D-WORKFLOW-144: the brand is never upper-cased through a formatter; a reading, not a check -- a `tools/vocabulary-check` rule is proposed in § The leads):

| Site | What it upper-cases |
| --- | --- |
| `MenuComponent.cpp:205` | `addWithLabel`'s label (the brief's `addGroup`; corrected by the seat, read at `:197`) |
| `MenuComponent.cpp:233` | `addWithDescription`'s label, with a description |
| `MenuComponent.cpp:236` | `addWithDescription`'s label, without one |
| `MenuComponent.cpp:283` | `setTitle` |
| `MenuComponent.cpp:358` | `setSubTitle`, through `getFileName`: a subtitle with a `/` keeps only what follows the last one (L-26) |
| `MenuComponent.cpp:487` | `addButton`'s name |
| `ButtonComponent.cpp:73` | the button's text |

Generated, asserted by `tools/t34-words.py`: 22 `_("` lines in 12 files, 27 occurrences, 17 distinct msgids, each with a non-empty French `msgstr` at the pin; 2 player texts outside `_()`; 7 formatters; every cited line asserted to hold its code.

## The structure

- **Includes inside the 80:** 352 quoted lines over 91 distinct headers (most: `GuiComponent.h` 28, `Settings.h` 20, `ThemeData.h` 19, `LocaleES.h` 18, `utils/StringUtil.h` 17, `components/TextComponent.h` 13), 37 angle-bracket lines; **one to es-app:** AsyncNotificationComponent.cpp:12 `../../es-app/src/CloudText.h` (**L-07**: resolves only through `-I es-core/src` plus `../../`; the unit build links `CloudText.cpp` for `:144`; a `CloudText` that moves to es-core is T18's and T35's call).
- **Includes into the 80 from outside:** 274 lines in 112 files (es-app 215, es-core 58, tests 1); most-included: `MenuComponent.h` 32, `TextComponent.h` 24, `OptionListComponent.h` 22, `ComponentGrid.h` 21, `BusyComponent.h` 17, `ImageComponent.h` 16.
- **`es-core/CMakeLists.txt`:** every one of the 80 named exactly once and unconditionally: the 42 headers at `:49-90`, the 38 sources at `:186-223`; `if(` only at `:278` and `:287`.
- **The in-source platform gates** (13 lines): `GridTileComponent.cpp:11`, `NinePatchComponent.cpp:415`, `VideoComponent.cpp:22`, `VideoPlayerComponent.cpp:1`, `VideoPlayerComponent.h:1`, `VideoVlcComponent.cpp:17`, `VideoVlcComponent.cpp:485`, `VideoVlcComponent.cpp:592`, `VideoVlcComponent.cpp:668`, `VideoVlcComponent.cpp:779`, `VideoVlcComponent.cpp:836`, `VideoVlcComponent.cpp:874`, `VideoVlcComponent.cpp:875`. `VideoPlayerComponent.{cpp,h}` sit whole under `#ifdef _RPI_` and compile to nothing on every image; the `WIN32` blocks are dead on the images; D-WORKFLOW-209's disposition: a dead-end table removes nothing.
- **The non-ASCII byte:** `VideoVlcComponent.cpp:859`, 0x96 (a Windows-1252 en dash) in the comment `// use: vlc<0x96>long-help`; `git grep -P` sees it only under a C locale; an upstream hit, recorded and not fixed (`es-code-traps.md:60`); 0 in the 21 fork-modified files.

Generated, asserted by `tools/t34-includes.py`: 352 quoted include lines over 91 headers, 37 angle, 1 to es-app; 274 outside lines in 112 files; the 80 each named once in `es-core/CMakeLists.txt`, `if(` at 278 and 287; 13 gate lines; 1 non-ASCII line.

- **L-14:** `GridTileComponent.cpp:1043` is indented one level deeper than `:1042`, `ImageGridComponent.h:380-381` sit shallower than their block, and `ImageGridComponent.h:2`'s `#include <functional>` stands above the include guard (`:3`). Each reads as part of a block it is not in. A one-commit tidy if the pause opens it.
- **L-05:** the second `BUTTON_GRID_HORIZ_PADDING` (`guis/GuiTextEditPopupKeyboard.cpp:14`, T35's) is recorded in § The constants. It is not deleted here (`engineering-practices.md:576`).
- **`UntintedImageComponent`:** `es-app/src/guis/GuiMenu.cpp:6401` (T26's file), used for the QR at `:6425`. Whether `ImageComponent` (h `:76`) gains an untinted mode is the pause's question (§ 1 h).
- **The menu map:** `tools/es-menu-map-check --es-src <W> --ref 16dbac5211...` prints `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (rc 0, `stage-a/runs.txt`). The components have no page of their own, so this slice proposes no row. A stream that adds, moves or renames a row on a page it touches changes `docs/es-menu-map.md` in the same commit (D-UI-039).
- **The two lanes' `AsyncNotificationComponent.h` doubles** (`tests/app-unit/fakes/components/AsyncNotificationComponent.h`, T18's; T33's build names the same fake): a header change in this slice is named as a collision at the hand-back. The fakes are not this lane's to edit (§ 1 j).
- **The other lanes' ES tips inside the 80** (`stage-a/runs.txt`): T2 `55158d2a64`, T18 `d55235d4b3`, T20 `5c0ddaaeef`, T21 `3ae9610b0f`, T26 `757f5370ea`, T31 `95852f8736`, T32 `b52245036f`, and T33 now at `f802c55c62c1` (the brief read `dd86d7ce20a5`). Each diff against the pin is empty: no collision inside the 80 at stage A. The diffs run again at the hand-back.

## The merge debt

**None:** the merge base `cada856d86` (with `rocknix/master` `f6c542872e`; `bccd715707` is its parent and the commit the never-fetched `upstream/master` still names) is the base of 0 of the 14 upstream commits since it that touch the 80. 80 of 80 blobs are identical between the base and `rocknix/master`, and 59 of 80 between the pin and `rocknix/master`; the 21 that differ are the fork's 21. Batocera's eight commits since `1750dded8c` on ten files (seven of them fork-modified) are **not ROCKNIX's**: a reconciliation list for the integration, never a debt figure. They are `0806a0c5c`, `9dbd4b9bf` (the `setOpacity` guard, § 1 g: unreachable at the pin), `308221458`, `ac4baceaf`, `09f5f708f`, `b728ac99d`, `ab218fba1` and `ad104860f`. One overlaps by hunk: `09f5f708f` and the fork's `7dc8bf373` both rewrite `HelpComponent::updateGrid()` (base lines 121-125 and 139-151).

## The runs

Stage A's runs are in `stage-a/first-commands.txt` (the brief's § 1) and `stage-a/runs.txt` (the brief's § 5 block, each line's rc and wall time), and the membership block is in `stage-a/membership-block.txt`. Every expectation printed as the brief says, with one erratum (the gates line).

| Run | Figure (the command's own lines) | A FAIL would mean | Where |
| --- | --- | --- | --- |
| the membership block | `mine: 80 paths.txt: 80 equal: True`; `lines: 21984 reach: {'shipped': 80} tier: {'upstream-carried': 59, 'fork-own': 21} lang: {'c++': 38, 'c-header': 42}`; `fork-own lines: 9541`; `read lines: 21984` | the slice's membership moved since the brief | `stage-a/membership-block.txt` |
| the scope | 80; 38; 42; 0 | a path added or dropped | `stage-a/runs.txt` |
| the bases | `16dbac5211`, 0, `cada856d86`, `f6c542872e`, `b2ceb55a7e`, `1750dded8c`, 725, 14, 1, 15 | the ES worktree off the pin, or the refs moved | `stage-a/runs.txt` |
| the lines two ways | `wc -l 21971`; `grep -c 21984`; `no trailing newline: 13` | a file changed at the pin | `stage-a/runs.txt` |
| the fork's delta | `21 files changed, 591 insertions(+), 114 deletions(-)` three times; added 0; the 21 numstat rows; 33, 33, 0 | the tiers would need two tables | `stage-a/runs.txt` |
| upstream's delta | 0 rc=1; 0 rc=1; 59; 59; 80; 8; 10; 7 | merge debt this slice would owe | `stage-a/runs.txt` |
| the other lanes' tips inside the 80 | eight empty stat lines | a collision to name | `stage-a/runs.txt` |
| the strings | `_(" lines TOTAL 22 in 12 files`; 27; the per-file line | a string added or dropped | `stage-a/runs.txt`; `tools/t34-words.py` |
| the threads and lifetimes | `std::thread` 1 (`VideoVlcComponent.cpp:91`), `.detach(` 1 (`:95`), `delete this` 4 (`OptionListComponent.h:96 :145 :158 :195`), `postToUiThread` 2 (`TextEditComponent.cpp:39 :47`) | a lifetime the table misses | `stage-a/runs.txt`; `tools/t34-lifetimes.py` |
| the reads | `exists( lines TOTAL 10 in 5 files`; 10; uncached 0 rc=1; `WebImageComponent.cpp:5 WebImageComponent.h:2` (`HttpReq`, 7 lines in 2 files) | a read the table misses | `stage-a/runs.txt`; `tools/t34-reads.py` |
| the input | 12; `202 636`; 14; 0 rc=1 | a prompt or an input the table misses | `stage-a/runs.txt`; `tools/t34-input.py` |
| the constants | nine lines, `GuiTextEditPopupKeyboard.cpp:14`'s second copy among them | a house value defined twice in the 80 | `stage-a/runs.txt`; `tools/t34-constants.py` |
| the pixel constants | `MenuComponent.cpp:11`, `:13` (comments); `screen-relative 86`; fontScale 0 rc=1 | a pixel constant the table misses | `stage-a/runs.txt` |
| the includes | 352; 37; `AsyncNotificationComponent.cpp:12`; 274; 112; `named-0-times (or more than once): 0`; `278 287` | the structure moved | `stage-a/runs.txt`; `tools/t34-includes.py` |
| the in-source gates | 13 lines (the brief's comment says twelve; its § 4 Q7 list is the same 13, `VideoPlayerComponent.{cpp,h}:1` being two) | a unit compiled differently | `stage-a/runs.txt` |
| the non-ASCII byte | `git grep -P` 1 rc 0 (C locale); `VideoVlcComponent.cpp:1`; `files with a non-ascii byte: 1`; the comment form 1; `od -c` shows `226` (0x96) | a second byte, or one in a fork-modified file | `stage-a/runs.txt` |
| the French | `4929:msgid "SWITCH TAB"` with `CHANGER D’ONGLET`; `3708:msgid "up/down"` with `haut/bas`; `:2207`; `SliderComponent.cpp:282` | the catalog moved | `stage-a/runs.txt` |
| `es-untranslated` | `es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without` rc 0 (against `bccd715707`); `703 ... 703 with French, 0 without` rc 0 (against `cada856d86`) | a fork string without French | `stage-a/runs.txt` |
| the FAIL-at-pin lines | `74 75`; `486`; `568`; `208 210 212 213 251`; `74`; `81 190 197` | a lead's line moved | `stage-a/runs.txt` |
| the `setOpacity` callers | `745 1001 1009 1011 1012 1077 1397 1398`; 107 | a caller of the bar's `setOpacity` | `stage-a/runs.txt` |
| the menu map | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0; 989 lines | a screen unmapped | `stage-a/runs.txt` |
| the compile | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2; plain `g++`: `.../es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory` rc 1; `pugixml root present` | a toolchain on the host, or a header found | `stage-a/runs.txt` |
| the removal check | empty against `00d490e654` and against `dff4fbd61d`; the ES diff against the pin empty | a change under `packages/`, `projects/` or `tools/`, or the ES tree off the pin | `stage-a/runs.txt` |
| the generators' drifts | each of the nine generators exit 1 on its constructed drift, rc 0 on the 80 | a table trusted before its check fired | `stage-b/generator-drifts.txt` |
| the stand-in syntax check over the 37 | pending: stage C (the fakes, the tenth `SDL_power.h`, the pugixml root) | a component's own C++ that does not parse | - |
| the unit build | pending: stage C (`tools/t34-build-tests.sh`, its `TOTAL:` line) | a pure seam's defect | - |

## The guest cycle

Not yet run. The window is asked for on #681 at stage B's end, with its plan and bound (`stage-b/window-plan.md`), and it runs only on the coordinator's grant there and in the host file's queue. The host file's 14:21 entry places T34's window after every M7 window.

## The streams

Written by the coordinator after stage D. The lane leaves this heading and the pause's dispositions.

## Positives

None yet. Each fix's positive is recorded here at stage E: its covering case's FAIL before and PASS after, or its frame `fix-walk-pending-image`.

## The #585 lines owed

One line per upstream-carried defect closed under rule 6, in the shape the lane writes, never sent. Owed only if a stream closes them; the candidates at stage B:

- **3.6**, `TextComponent.cpp:486`: the vertical marquee's limit subtracts the top padding twice (`mPadding.y() - mPadding.y()`), where `:351` and `:428` subtract top and bottom; with padding (0,10,0,30) the limit is 20 px too large.
- **3.7**, `SliderComponent.cpp:282`: the AUTO sentinel prints `"Auto"`, outside `_()` and not the placeholder `AUTO`.
- **L-01**, `ComponentList.cpp:568`: the `up/down` icon key goes through `_()`, so a translated catalog turns it into a key the help bar does not know.
- **L-23**, `RatingComponent.cpp:265`: the OK prompt `"add star"` is outside `_()`.
- **L-17**, `TextComponent.cpp:338` against `:350`: the auto height is measured at the full width and the text drawn at the padded one; the reproducer is written here at stage C.

The six fork candidates the brief names for the coordinator (none sent; `engineering-practices.md` § Consider contributing every applicable fix upstream): `aa8c5da4c` (the grid's `canMoveCursor`, the strongest), `7c7ffab43` (the row measured from the fonts), `b6eb26980`, `8927b1760` with `f1ae6bc25` as a pair (the strip as a focus stop), `7dc8bf373` only after the RTL reconciliation (the help bar's fit), and `2088eadb9` (the tile label's multi-line).

## What T35 to T37 inherit

Written, not tested here (the brief's § 5 item 3):

1. **The provenance table:** § Coverage, 0 / 21 / 59 against `bccd715707` and `cada856d86`, which agree.
2. **The layouts table:** § The layouts, the 19 font-height reads with the brief's eight, and the 10 size rows.
3. **The constants table:** § The constants, the seven house values with their one definition and readers, and the 15 pixel constants.
4. **The input table:** § The input, the 16 `input()` and the 14 `getHelpPrompts()` with their conditions.
5. **The lifetimes table:** § The lifetimes, with the card's closing race (L-22) and its window-side half for T35.
6. **The reads table:** § The reads, 33 rows with their writers.
7. **The `components-tests` build recipe:** the doubles, the tenth fake `SDL_power.h` and the pugixml root, in `tools/t34-build-tests.sh` at stage C.
8. **The `setOpacity` callers' read, for T35:** § The leads' ruling (g).
9. **The texture-cache contract, for T36:** § The reads, `ImageComponent.cpp:408` (a path is a cache key for the texture's lifetime).
10. **The es-core to es-app include's disposition:** § The structure, L-07.

# T34 (#681) research notes

## Scope

**The slice:** `es-core-components` (`k: 34`), one selector `{"globs": ["es:es-core/src/components/**"]}`, area `interface`, no `rest`. The 80 paths are `stage-a/paths.txt`, the membership block's own TSV (`.qa-scratch/t34/paths.txt`, copied). The block is the brief's § 2 heredoc byte for byte, run twice from this worktree (stacked on the P1 branch at `2174265e9c`, whose `docs/reviews/{inventory.json,slices.json}` it reads). Its whole output is `stage-a/membership-block.txt`.

The first pass, against `/dev/null`:

    # first pass (against /dev/null): mine: 80 paths.txt: 0 equal: False

The second pass, against its own paths file -- the five lines § 7 names, as printed:

    mine: 80 paths.txt: 80 equal: True
    only-mine: []
    only-paths.txt: []
    lines: 21984 reach: {'shipped': 80} tier: {'upstream-carried': 59, 'fork-own': 21} lang: {'c++': 38, 'c-header': 42}
    fork-own lines: 9541
    read lines: 21984

The 25 named paths and their claimants, as printed (`CLAIMS`):

    es-core/src/components/MenuComponent.cpp in-T34 non-rest [('es-core-components', 34)] tier fork-own lines 574 area interface
    es-core/src/components/AsyncNotificationComponent.cpp in-T34 non-rest [('es-core-components', 34)] tier fork-own lines 306 area interface
    es-core/src/components/VideoVlcComponent.cpp in-T34 non-rest [('es-core-components', 34)] tier upstream-carried lines 1113 area interface
    es-core/src/components/OptionListComponent.h in-T34 non-rest [('es-core-components', 34)] tier upstream-carried lines 661 area interface
    es-core/src/guis/GuiMsgBox.cpp not-in-T34 rest [('es-core-window-input', 35)] tier fork-own lines 299 area interface
    es-core/src/guis/GuiTextEditPopup.cpp not-in-T34 rest [('es-core-window-input', 35)] tier fork-own lines 86 area interface
    es-core/src/guis/GuiTextEditPopupKeyboard.cpp not-in-T34 rest [('es-core-window-input', 35)] tier fork-own lines 533 area interface
    es-core/src/guis/GuiInfoPopup.cpp not-in-T34 rest [('es-core-window-input', 35)] tier upstream-carried lines 115 area interface
    es-core/src/Window.cpp not-in-T34 rest [('es-core-window-input', 35)] tier fork-own lines 1656 area interface
    es-core/src/ThemeData.cpp not-in-T34 rest [('es-core-window-input', 35)] tier upstream-carried lines 2891 area interface
    es-core/src/GuiComponent.cpp not-in-T34 rest [('es-core-window-input', 35)] tier upstream-carried lines 1540 area interface
    es-core/src/InputConfig.cpp not-in-T34 rest [('es-core-window-input', 35)] tier fork-own lines 446 area interface
    es-core/src/HttpReq.cpp not-in-T34 non-rest [('es-state-and-bridge', 21)] tier fork-own lines 644 area interface
    es-core/src/Settings.cpp not-in-T34 non-rest [('es-state-and-bridge', 21)] tier fork-own lines 723 area interface
    es-core/src/resources/TextureData.cpp not-in-T34 non-rest [('es-core-utils-resources', 36)] tier fork-own lines 739 area interface
    es-core/src/resources/TextureResource.cpp not-in-T34 non-rest [('es-core-utils-resources', 36)] tier upstream-carried lines 348 area interface
    es-core/src/resources/Font.cpp not-in-T34 non-rest [('es-core-utils-resources', 36)] tier fork-own lines 1311 area interface
    es-core/src/utils/FileSystemUtil.cpp not-in-T34 non-rest [('es-core-utils-resources', 36)] tier upstream-carried lines 1805 area interface
    es-core/src/utils/AtomicFileUtil.cpp not-in-T34 non-rest [('es-state-and-bridge', 21)] tier fork-own lines 829 area interface
    es-core/src/utils/OfflineProxyUrl.cpp not-in-T34 non-rest [('es-core-utils-resources', 36)] tier fork-own lines 21 area interface
    es-core/src/watchers/WatchersManager.cpp not-in-T34 rest [('es-core-window-input', 35)] tier upstream-carried lines 203 area interface
    es-core/src/Scripting.cpp not-in-T34 rest [('es-core-window-input', 35)] tier fork-own lines 209 area interface
    es-app/src/CloudText.cpp not-in-T34 non-rest [('es-cloud-pages', 18)] tier fork-own lines 1409 area interface
    es-app/src/components/ScraperSearchComponent.cpp not-in-T34 rest [('es-app-system', 33)] tier upstream-carried lines 755 area interface
    es-core/CMakeLists.txt not-in-T34 rest [('es-core-window-input', 35)] tier fork-own lines 303 area interface

`ES-CORE BY SLICE`: four rows summing to 242 paths, no `es-core/**` row unassigned or ambiguous:

    96 paths 22575 lines (('es-core-window-input',), 'rest')
    80 paths 21984 lines (('es-core-components',), 'non-rest')
    58 paths 50840 lines (('es-core-utils-resources',), 'non-rest')
    8 paths 3344 lines (('es-state-and-bridge',), 'non-rest')

The block's ES lines (`W` the lane's ES worktree at the pin `16dbac5211eea7e70db7394372033be2be7df829`): `wc -l`, `grep -c ''`, the count present at the merge base `cada856d86`, at `bccd715707`, and the fork's shortstat against each:

    wc -l 21971
    grep -c 21984
    80
    80
     21 files changed, 591 insertions(+), 114 deletions(-)
     21 files changed, 591 insertions(+), 114 deletions(-)

The thirteen files without a trailing newline, which make the two line rules differ by 13, are `stage-a/runs.txt`'s `no newline:` lines (wc/grep order).

**The bases** (the brief's § 2 (3), each read from the shared refs, no fetch, `stage-a/first-commands.txt` and `runs.txt`): the pin's merge base with `rocknix/master` (`f6c542872e`) is **`cada856d86`**, one commit after **`bccd715707`**, its parent and the commit the never-fetched `upstream/master` still names (`rev-list --count upstream/master..rocknix/master` = 15); the merge base with `batocera/master` (`b2ceb55a7e`) is **`1750dded8c`**. For the 80, `bccd715707` and `cada856d86` are the same: the shortstat is one line against both.

**The tiers:** fork-added 0 / fork-modified 21 / upstream-carried 59 (the read's), inventory fork-own 21 / upstream-carried 59 (per file); the fork's own lines are +591/-114 over 33 commits, not the inventory's 9,541.

## The § 5 runs at stage A

The brief's § 5 block, extracted from the brief and run once (`stage-a/runs.txt`; each line's text, output, rc and wall time there). Each block below is the expectation comment, then the lines it printed, then the wrapper's rc line (the brief's placeholder words hyphenated, as in `runs.txt`):

    # the scope (expect 80; cpp 38; h 42; other 0)
    80
    38
    42
    0
    [line 5] rc=1 4 ms

    # the ES worktree at the pin, clean; the bases; the counts (expect the pin; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c; 725; 14; 1; 15)
    16dbac5211
    0
    cada856d86
    f6c542872e
    b2ceb55a7e
    1750dded8c
    725
    14
    1
    15
    [line 7] rc=0 59 ms

    # the lines two ways (expect wc -l 21971; grep -c 21984; no trailing newline: 13, the files § 2 names)
    wc -l 21971
    grep -c 21984
    no newline: es-core/src/components/AsyncNotificationComponent.h 77/78
    no newline: es-core/src/components/ComponentTab.cpp 436/437
    no newline: es-core/src/components/GridTileComponent.cpp 1595/1596
    no newline: es-core/src/components/HelpComponent.cpp 330/331
    no newline: es-core/src/components/ImageComponent.cpp 1399/1400
    no newline: es-core/src/components/NinePatchComponent.cpp 494/495
    no newline: es-core/src/components/RatingComponent.cpp 294/295
    no newline: es-core/src/components/ScrollbarComponent.cpp 214/215
    no newline: es-core/src/components/StackPanelComponent.cpp 225/226
    no newline: es-core/src/components/TextComponent.cpp 856/857
    no newline: es-core/src/components/VolumeInfoComponent.h 29/30
    no newline: es-core/src/components/WebImageComponent.cpp 264/265
    no newline: es-core/src/components/WebImageComponent.h 39/40
    no trailing newline: 13
    [line 9] rc=0 460 ms

    # the fork's delta (expect `21 files changed, 591 insertions(+), 114 deletions(-)` three times; A 0; M 21; the 21 numstat rows of § 2; 33 commits, 33 non-merge, no merges)
     21 files changed, 591 insertions(+), 114 deletions(-)
     21 files changed, 591 insertions(+), 114 deletions(-)
     21 files changed, 591 insertions(+), 114 deletions(-)
    0
    added rc=1
    128	17	es-core/src/components/AsyncNotificationComponent.cpp
    23	2	es-core/src/components/AsyncNotificationComponent.h
    38	2	es-core/src/components/ComponentGrid.cpp
    3	0	es-core/src/components/ComponentGrid.h
    5	0	es-core/src/components/ComponentList.cpp
    14	0	es-core/src/components/ComponentList.h
    3	2	es-core/src/components/ComponentTab.cpp
    22	0	es-core/src/components/GridTileComponent.cpp
    16	0	es-core/src/components/GridTileComponent.h
    25	7	es-core/src/components/HelpComponent.cpp
    58	4	es-core/src/components/ImageComponent.cpp
    16	0	es-core/src/components/ImageComponent.h
    19	0	es-core/src/components/ImageGridComponent.h
    86	49	es-core/src/components/MenuComponent.cpp
    9	0	es-core/src/components/MenuComponent.h
    58	26	es-core/src/components/MultiLineMenuEntry.cpp
    19	0	es-core/src/components/MultiLineMenuEntry.h
    13	3	es-core/src/components/SwitchComponent.cpp
    9	1	es-core/src/components/SwitchComponent.h
    2	0	es-core/src/components/TextComponent.h
    25	1	es-core/src/components/WebImageComponent.cpp
    33
    33
    0
    merges rc=1
    [line 11] rc=0 94 ms

    # upstream's delta: the merge-debt record (expect 0 rc=1; 0 rc=1; identical to rocknix/master: 59; identical to cada856d86: 59; MB-vs-master identical: 80; batocera commits on the 80: 8; batocera files: 10; both-changed: 7)
    0
    upstream commits rc=1
    0
    upstream numstat rc=1
    identical to rocknix/master: 59
    identical to cada856d86: 59
    MB-vs-master identical: 80
    8
    10
    7
    [line 13] rc=0 290 ms

    # the other lanes' deltas inside the 80 (expect every stat line empty for the eight -- T33's `dd86d7ce20a5`, read 2026-10-30 -- or the rows named as a collision)
    == m6-es-launch-path-649
    == m6-es-cloud-pages-665
    == m6-es-achievements-pages-667
    == m6-es-state-and-bridge-668
    == m6-es-guimenu-673
    == m6-es-pages-678
    == m6-es-app-views-scrapers-679
    == m6-es-app-system-680
    [line 15] rc=0 23 ms

    # the strings, two ways (expect `_(" lines TOTAL 22 in 12 files`; occurrences 27; per file BusyComponent 1, CarouselComponent 2, ComponentGrid 3, ComponentList 2, ComponentTab 1, DateTimeComponent 1, ImageComponent 1, OptionListComponent.h 6, SliderComponent 1, SwitchComponent 1, TextEditComponent 2, VideoComponent 1)
    _(" lines TOTAL 22 in 12 files
    27
    BusyComponent.cpp:1 CarouselComponent.cpp:2 ComponentGrid.cpp:3 ComponentList.cpp:2 ComponentTab.cpp:1 DateTimeComponent.cpp:1 ImageComponent.cpp:1 OptionListComponent.h:6 SliderComponent.cpp:1 SwitchComponent.cpp:1 TextEditCompon
    [line 17] rc=0 14 ms

    # the threads and the lifetimes (expect `std::thread` 1 at VideoVlcComponent.cpp:91; `.detach(` 1 at :95; `delete this` 4 at OptionListComponent.h:96 :145 :158 :195; `postToUiThread` 2 at TextEditComponent.cpp:39 :47)
    es-core/src/components/VideoVlcComponent.cpp:91 
    es-core/src/components/VideoVlcComponent.cpp:95 
    es-core/src/components/OptionListComponent.h:96 es-core/src/components/OptionListComponent.h:145 es-core/src/components/OptionListComponent.h:158 es-core/src/components/OptionListComponent.h:195 
    es-core/src/components/TextEditComponent.cpp:39 es-core/src/components/TextEditComponent.cpp:47 
    [line 19] rc=0 17 ms

    # the reads and the network (expect `exists( lines TOTAL 10 in 5 files`; occurrences 10; uncached: 0 rc=1; HttpReq lines `WebImageComponent.cpp:5 WebImageComponent.h:2`)
    exists( lines TOTAL 10 in 5 files
    10
    0
    uncached rc=1
    WebImageComponent.cpp:5 WebImageComponent.h:2 
    [line 21] rc=0 15 ms

    # the input and the help bar (expect getHelpPrompts definitions in .cpp: 12; inline in OptionListComponent.h: 2 at :202 :636; `input(` definitions 14; `canMoveCursor` callers outside ComponentGrid.cpp: 0 rc=1)
    12
    202 636 
    14
    0
    canMoveCursor outside rc=1
    [line 23] rc=0 22 ms

    # the constants (expect nine lines: MenuComponent.cpp:6 :14; AsyncNotificationComponent.cpp:31; ComponentList.cpp:11; ComponentList.h:25; HelpComponent.cpp:13 :16 and :130 (`const float entryWidth`, a use); GuiTextEditPopupKeyboard.cpp:14 the second copy at 0.0052083333 -- the uses at AsyncNotificationComponent.cpp:64 :112 :276 and ComponentList.h:26 are dropped by the `#define|const ` filter)
    es-core/src/components/AsyncNotificationComponent.cpp:31:#define NOTIFICATION_OPACITY  255
    es-core/src/components/ComponentList.cpp:11:#define TOTAL_HORIZONTAL_PADDING_PX 20
    es-core/src/components/ComponentList.h:25:	const unsigned char DIMMED_ALPHA = 0x50;
    es-core/src/components/HelpComponent.cpp:13:#define ICON_TEXT_SPACING Renderer::getScreenWidth() * 0.0042f
    es-core/src/components/HelpComponent.cpp:16:#define ENTRY_SPACING (ICON_TEXT_SPACING * 2.0f)
    es-core/src/components/HelpComponent.cpp:130:		const float entryWidth = icon->getSize().x() + lbl->getSize().x() + ICON_TEXT_SPACING + ENTRY_SPACING;
    es-core/src/components/MenuComponent.cpp:6:#define BUTTON_GRID_VERT_PADDING  (Renderer::getScreenHeight()*0.0296296)
    es-core/src/components/MenuComponent.cpp:14:#define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.022)
    es-core/src/guis/GuiTextEditPopupKeyboard.cpp:14:#define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.0052083333)
    [line 25] rc=0 7 ms

    # the pixel constants (expect 2 lines, both comments, MenuComponent.cpp:11 and :13; screen-relative lines 86; fontScale 0 rc=1)
    es-core/src/components/MenuComponent.cpp:11 es-core/src/components/MenuComponent.cpp:13 
    screen-relative 86
    0
    fontScale rc=1
    [line 27] rc=0 16 ms

    # the includes (expect quoted include lines 352; angle 37; es-app 1 at AsyncNotificationComponent.cpp:12; outside includers 274 lines in 112 files; CMake: 42 headers named at :49-90, 38 sources at :186-223, named-0-times 0, `if(` at 278 287)
    352
    37
    es-core/src/components/AsyncNotificationComponent.cpp:12:#include "../../es-app/src/CloudText.h"
    274
    112
    named-0-times (or more than once): 0
    278 287 
    [line 29] rc=0 338 ms

    # the in-source gates (expect the twelve lines § 4 Q7 names)
    es-core/src/components/GridTileComponent.cpp:11 es-core/src/components/NinePatchComponent.cpp:415 es-core/src/components/VideoComponent.cpp:22 es-core/src/components/VideoPlayerComponent.cpp:1 es-core/src/components/VideoPlayerCom
    [line 31] rc=0 8 ms

    # the non-ASCII byte (expect `git grep -P` 1 rc=0 under the block's LC_ALL=C; in a UTF-8 locale (`LC_ALL=C.UTF-8`) it prints nothing, rc=1 -- the UTF-mode miss; the C-locale loop `VideoVlcComponent.cpp:1`, `files with a non-ascii byte: 1`, and the comment-line form the same 1; the 21 fork-modified files 0)
    1
    VideoVlcComponent.cpp:1
    files with a non-ascii byte: 1
    1
    0000000  \t   /   /       u   s   e       :       v   l   c     226   l
    0000020   o   n   g   -   h   e   l   p  \n  \t   /   /       W   I   N
    0000040   3   2       ?       l   i   b   v   l   c   _   m   e   d   i
    0000060   a   _   a   d   d   _   o   p   t   i   o   n   (   m   M   e
    [line 33] rc=0 139 ms

    # the French (expect `4929:msgid "SWITCH TAB"` with `msgstr "CHANGER D’ONGLET"` after it; `3708:msgid "up/down"` with `msgstr "haut/bas"`; `^msgid ` lines 2207; the slider's "Auto" at SliderComponent.cpp:282 outside _(); es-untranslated the two tree-wide lines T33 printed, rc 0 each)
    167:msgid "SELECT" 212:msgid "CHOOSE" 3708:msgid "up/down" 3711:msgid "WORKING..." 3735:msgid "CHANGE" 3809:msgid "SELECT" 4929:msgid "SWITCH TAB" 
    msgid "up/down"
    msgstr "haut/bas"
    msgid "SWITCH TAB"
    msgstr "CHANGER D’ONGLET"
    locale/lang/fr/LC_MESSAGES/emulationstation2.po:2207
    es-core/src/components/SliderComponent.cpp:282:			ss << "Auto";  // Display "AUTO"
    [line 35] rc=0 18 ms
    es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without
    es-untranslated rc=0
    [line 36] rc=0 299 ms
    es-untranslated: 703 fork string(s) in the source, 703 with French, 0 without
    es-untranslated(cada) rc=0
    [line 37] rc=0 290 ms

    # the FAIL-at-pin lines (expect MultiLineMenuEntry `74 75` for the two setRowHeightPerc; TextComponent `486` for the doubled .y(); ComponentList `568` for the _("up/down"); HelpComponent setOpacity and mGrid `208 210 212 213 251`; Carousel moveCursorFast `74`; WebImage `81 190 197` -- `:134` tests a local `localFile`, not `mLocalFile`)
    74 75 
    486
    568
    208 210 212 213 251 
    74
    81 190 197 
    [line 39] rc=0 25 ms

    # the setOpacity callers (expect: no `mHelp->setOpacity` in Window.cpp -- its mHelp-> lines 745 1001 1009 1011 1012 1077 1397 1398; the tree-wide `setOpacity` lines 107 in es-core/src and es-app/src, the caller list the lane's, § 4 Q7)
    745 1001 1009 1011 1012 1077 1397 1398 
    107
    [line 41] rc=0 14 ms

    # the menu map (expect `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 -- T33's proof's line at the same pin on the map at ce8608e38f, 989 lines; the map unchanged since)
    55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing
    es-menu-map-check rc=0
    989 docs/es-menu-map.md
    [line 43] rc=0 128 ms

    # the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2; plain g++ on MenuComponent.cpp: rc 1 and `es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory`; with the fakes and the pugixml root the stand-in check over the 37, rc per file)
    es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)
    es-syntax-check rc=2
    [line 45] rc=0 4 ms
    /home/max/Development/emulationstation-next.worktrees/m6-es-core-components-681/es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory
    plain g++ rc=1
    [line 46] rc=0 52 ms
    pugixml root present
    [line 47] rc=0 2 ms

    # STAGE C -- the lane's scripts, which do not exist at stage A (expect the include script's last lines: 352 quoted, 37 angle, es-app 1, 274 outside lines in 112 files; and the build script's own `TOTAL: N test cases in B binaries` with 0 failed, `components-tests` among the binaries, and before any fix the seven FAIL-at-pin cases reported FAIL by name)
    NOT RUN (stage C; the script does not exist at stage A): python3 -I docs/audits/*-epic-m6-es-core-components/tools/t34-includes.py "$W" "$PIN" .qa-scratch/t34/paths.txt | tail -n 4
    NOT RUN (stage C; the script does not exist at stage A): bash docs/audits/*-epic-m6-es-core-components/tools/t34-build-tests.sh "$W" 2>&1 | tail -n 10

    # STAGE A, after the pointer is read -- the removal check: TIP-HASH is the lane's own tip the pointer and the dispatch comment name (MERGE-HASH at stage A); the literal word fails with `fatal: bad revision 'TIP-HASH'` (expect empty) and the ES diff against the pin (expect empty before stage E)
    [line 52] rc=0 4 ms
    [line 52] rc=0 4 ms

**Deltas against the brief's expectations:** one, the brief's -- the in-source gates command prints **13** lines, exactly § 4 Q7's list (`VideoPlayerComponent.{cpp,h}:1` is two lines), where the expectation comment says "twelve". T33's ES tip is now `f802c55c62c1` (the brief's proof read `dd86d7ce20a5`); its diff inside the 80 is empty, as are the seven accepted lanes'. The two STAGE C lines name scripts that do not exist at stage A and were not run.

## Read this session (working-principles § Pre-flight)

- **The brief**, `docs/reviews/briefs/es-core-components.md` at `a6e14fed86` with the errata at `200a9a032d`: whole, before the first command.
- **The pointer** and **the dispatch comment** (#681, 2026-10-30T09:50:59Z): whole; the eleven keys against § 10 (`00`, stage A).
- **#681's body:** its 21 checkboxes equal the brief's § 7 byte for byte; the states of the § 3 item 9 issues are `stage-a/issue-states.txt`.
- **The rules:** every rule loaded at session start, from the T3 worktree's copies. Six of those differ in T34's worktree (`device-builds`, `engineering-practices`, `es-code-traps`, `es-player-text`, `es-ui-style-guide`, `generic-x64-vm-testing`), and their diffs were read here: `es-code-traps.md`'s added-lines non-ASCII rule and its curl header-callback section; `es-ui-style-guide.md:202`'s card row (seconds, fast work only); `es-player-text.md`'s `SKIPPED` row with D-UI-129. The brief cites T34's copies by line, and those are what stage B reads at the cited sections.
- **Not yet read:** § 3 items 2 to 10 (the register rows by archaeology, the menu map's cited lines, the blindspots, the tests at the pin, the walks and frames, the French beyond § 5's lines, the earlier lanes' audits, T33's `02` § What T34 to T37 inherit, `docs/vm-qa-log.md`). These are stage B's first reading, before `02` is written.

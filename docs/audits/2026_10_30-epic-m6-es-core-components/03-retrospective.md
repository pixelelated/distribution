# Retrospective: M6.P2 T34, EmulationStation's core components (#681)

What the 80 paths were for, how the fork's 33 commits changed them, and where the seams are. This is the audit's retrospective (code-auditor Phase 3), not the lane's mini-retro, which is stage G's.

## 3.1 What the components are for

Every page the player sees is built from these: the menu and its button bar, the row list and its rows, the tab strip, the cell grid, the help bar, the progress card, the images and the text. The fork's lanes (D-UI-079) run through ten of them. The other surfaces (video, carousel, rating, date editor, text list, glyphs) are upstream's, read for cost and brittleness and left as upstream has them.

## 3.2 What the fork changed, and what drifted

The fork's 33 commits (2026-08-28 to 2026-10-01) are mostly fixes found on frames:
- the button gap (D-UI-012);
- the strip as a focus stop (D-UI-021, #65, #325);
- the help bar that offers only a direction that moves (D-UI-034, #115);
- the dim that survives the list's re-tint (#182);
- the row measured from its fonts (#241);
- the help bar's fit (#210);
- the image's aspect and turn (#243, #245, #250);
- the card's candidate rows (D-UI-035), opacity (D-UI-016) and width.

Little drifted from what each fix claimed. The one claim the tree contradicts is `MenuComponent.cpp:7-13`'s "the one place", which T35's keyboard popup does not honour (PL-16).

## 3.3 What none of the fixes noticed

- The card's `close()` is called from worker threads and was never made thread-safe; only its text is locked (PL-01).
- Two upstream lines put player text outside `_()` (PL-09, PL-10).
- One puts an icon key inside it (PL-04).
- Upstream's `TextComponent` keeps #48's measurement root, which `GuiMsgBox` works around and nothing else does (PL-08).

## 3.4 What the record says about catches

Each fork fix was caught on a frame, by a person or a walk, after it shipped once. No unit case has ever linked a component: the only component in a test tree is a double. The 34 seam cases this slice owes would be the first.

## 3.5 The seams

The floor's 3.1 to 3.34 (`02` § The leads), each a pure function a case can pin: the grid's cursor scan, the row shares, the marquee limit, the slider's text, the carousel's fast move, the help bar's fit, the card's chooser width, the image's fit and turn, the dim, the bar's widths. The lifetimes need sanitizers rather than cases: the popup's `delete this`, the field's posts, the card's race.

## 3.6 Time to play

The slice's effect on the two numbers (`time-to-play.md`, D-CLOUD-098: interface to a game's first frame, and a game's exit to the next game's first frame), stream by stream:

- **What runs every frame.** `ComponentList::render` re-tints every element of every row every frame (upstream's, unchanged here). The three func-form rows force per-frame updates, and `UPDATE_ALWAYS` (S7, PL-28) refreshes every row each frame.
  - Before S7, an uninitialised `mUpdateType` gave one of the three branches by chance.
  - S7 fixes the value that the observed behaviour and the explicit callers already asked for, so a list that was updating keeps the same per-frame cost.
- **What S2 to S6 add.**
  - S2: one atomic load per card `update()`, and one lock per holder call (an `updateText` per rclone progress line).
  - S3: `setSize` returns on an unchanged size, which removes a second resize on pages that size an image twice (the game list's grid among them).
  - S5: two string clears per bind, and one cancel per memory or shared-texture image.
  - S6: a map clear per grid reset, an erase per image change, and a compare.
  - None of it is on the launch path's length.
- **S1** names a cache file by one md5 of its URL and a canonical-path compare per bind, microseconds. After the update each web image (badges, scraper results, store items) is fetched once more, since the old names are not read. That is on the achievements and scraper pages, not on the launch path.
- **S4** rebuilds no bar more often than before: a bar is rebuilt on a page change, and the clip adds one `setSize` when a first prompt overflows.
- **The measurement:** `CANNOT` this slice, with the harness's reason. The guest window's tools capture frames, not frame times, and the guest exposes no per-frame counter, so the per-frame work above and the card were not priced on the guest. The last figure on record is `docs/vm-qa-log.md:171` (2026-10-06, `7afa9efcfc0`: 0.603 s to the first pixels, 1.33 s exit with backup, 1.017 s rapid relaunch), from before this slice. The integration image's `tools/time-to-play` run is the first to read it.

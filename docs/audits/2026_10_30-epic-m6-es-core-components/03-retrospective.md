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

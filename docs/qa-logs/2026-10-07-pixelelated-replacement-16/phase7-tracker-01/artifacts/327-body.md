## Accepted on candidate 16

Before and English/French at 640×480 explanation frames show the approved separated paragraphs without clipping. French/menu/vocabulary checks pass. Local website asset commit 4f6df54 matches the reviewed a40331aa screenshot hash; the current ES page source is unchanged. This closes the retaken-asset criterion; website publication remains P5.

[Primary acceptance](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/qa-logs/2026-10-07-pixelelated-replacement-16/unchanged-dependency-custody/327-site-frame-readback.json); [criterion reconciliation](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/10-closure-reconciliation.md); [fix commits and existing-state dispositions](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md).

Already written: this closure records verified evidence and changes no player files or cloud data; the original runtime failures and prior source states remain retained.

## Historical request and execution record

## First-release carry-forward — 2026-10-02 (#385)

The source fix and RC2 before/after frames exist. The approved design uses two readable, wrapping description-size paragraphs; the original single-line criterion is stale. Candidate frame and docs image reconciliation remain. The old rc-accept exception is not renewed. Current scope: docs/rasteratops/release-readiness.md.

**Maintainer, 2026-09-29 (chat, D-QA-012), play-testing RC1 on the RG SP:** *"Another item to fix is that the copy below, 'Enabling offline achievements,' just looks odd in all caps, the rows aren't separated, and the general readability isn't great. Can you look at a screenshot of that and then see what we might be able to do to just improve the usability and readability of that page? It'd be another good thing to fix in RC2."*

**What exists today** (`GuiRetroAchievementsSettings.cpp`, `openOfflineAchievements`, on `8dd6765af0`): the page carries the OFFLINE ACHIEVEMENTS (BETA) switch, the SCAN GAMES FOR OFFLINE ACHIEVEMENTS row with its last-run line, and below them one block of explanation in the menu's upper-case text font: `EARN CASUAL ACHIEVEMENTS WITHOUT A CONNECTION. THEY ARE SENT WHEN YOU'RE BACK ONLINE. CASUAL ACHIEVEMENTS ONLY, SO TURNING IT ON TURNS HARDCORE MODE OFF. '!RA!' IN A GAME'S CORNER MEANS AN ACHIEVEMENT HASN'T REACHED RETROACHIEVEMENTS YET. NEW GAMES ARE ADDED THE NEXT TIME YOU'RE CONNECTED.` (D-UI-054 asked for the options first and one block after.) The frame at 640x480 is `docs/_inc/images/retro-achievements/offline-achievements.png` on the site branch (from `tools/vm-walks/docs/retro-achievements.steps`).

**For RC2** (D-WORKFLOW-072's shape: a small interface fix, proven on the VM): the proposal follows in a comment after reading the frame beside `es-ui-style-guide.md` (descriptions are one sentence, small font, under the row they explain) and `es-player-text.md` (clear, then brief, then sized to the space).

Can this be done on the VM? **Yes** -- the page's frame at the handheld's size, before and after, from the docs walk.

## Acceptance criteria

- [x] A frame of the page at 640x480 from `tools/vm-walks/docs/retro-achievements.steps` on the first-release candidate image shows the explanation as short lines under the rows they explain (or one short block in the description size), each row visibly separated, the approved two paragraphs wrap within the panel without clipping (D-UI-119), and the frame filed under `docs/qa-frames/` beside the before frame.
- [x] `tools/es-menu-map-check` PASS, the French strings for every changed sentence in the same commit (D-UI-051), `tools/vocabulary-check` PASS.
- [x] The site's `retro-achievements/offline-achievements.png` retaken from the walk after the change.


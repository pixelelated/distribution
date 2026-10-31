# Retrospective: M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

The code auditor's retrospective of the slice (the audit's Phase 3), not the lane's ceremony retro (that is `docs/retros/`, after stage E).

## 3.1 What the slice is for

The window is the one object every page, card and toast goes through: it owns the page stack, the floating surfaces, the posted functions and the screensaver. The input manager turns SDL's devices into configurations and writes `es_input.cfg`. The watchers poll the network and the battery on their own thread. The script runner fires the event hooks. The six es-core dialogs are the box, the two text popups, the toast, the detect page and the configuration page. Most of it is upstream's and unchanged since the base; the fork's 13 files carry one floating surface at a time (D-UI-093), the centred card, the log policy, the masked logs and the dialog's measured height.

## 3.2 What the fork changed, and what drifted

`13 files changed, 247 insertions(+), 71 deletions(-)` against `bccd715707`. The fork's own rule for the queue (D-UI-093) was written over an upstream pop that contradicts it (`Window.cpp:339-340`); the fork's comment beside the re-queue (`:1159-1160`) even relies on the contradiction. The card moved to the centre and one rule sentence did not follow (`es-native-ui.md:30`). Upstream has not touched the 96 since the base.

## 3.3 What none of the fixes noticed

- The D-UI-093 fix tested that a toast waits for a card; nothing tested two toasts.
- The input file's writer and its readers go through different layers (pugixml and `Utils::FileSystem`), so the cache that serves the readers never hears from the writer.
- The quoting rule in `executeScript` was written for spaces; the shell it feeds reads `$`, backticks and quotes.
- `WatchersManager`'s lock was sized for the list and held for the probe.

## 3.4 What the record says about catches

T33 found the watcher lock (#1283) and the screensaver use-after-free (#1305) from the es-app side; this slice proves the es-core halves with cases that fail at the pin. T34's held patches (the card handle, the dialog's height) land on files of this slice, which is why both are named collisions rather than adopted.

## 3.5 The seams

The slice's cases are extracts of the pin's lines in the smallest double that compiles them (`tools/t35-extract.py` refuses a range that moved), and `WatchersManager.cpp` linked whole behind the tree's own `Log.h` double. The next slice that touches `Window.cpp` or `InputManager.cpp` inherits those extracts and the stand-in's fakes.

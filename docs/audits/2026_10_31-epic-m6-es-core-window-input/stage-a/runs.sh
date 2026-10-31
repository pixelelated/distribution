#!/bin/bash
# T35 stage A: brief § 5's runs, each wrapped in its own rc=$? line and a date +%s pair (the brief's own lines unchanged inside)
set +e
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t35/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
FILES=$(cat .qa-scratch/t35/paths.txt)
echo; echo '# the scope (expect 96; cpp 44; h 51; other 1 -- es-core/CMakeLists.txt; R1 C06)'
t0=$(date +%s)
( printf '%s\n' $FILES | $G -c .; printf '%s\n' $FILES | $G -c '\.cpp$'; printf '%s\n' $FILES | $G -c '\.h$'; printf '%s\n' $FILES | $G -c -v -E '\.(cpp|h)$' )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the ES worktree at the pin, clean; the bases; the counts (expect the pin; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c -- R1 C15, C17; then 725; 14; 1; 15 -- printed by the proof on 2026-10-31 at the same pin and refs; 531 without merges)'
t0=$(date +%s)
( git -C "$W" rev-parse HEAD | cut -c1-10; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" rev-parse rocknix/master | cut -c1-10; git -C "$W" rev-parse batocera/master | cut -c1-10; git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10; git -C "$W" rev-list --count bccd715707.."$PIN"; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count bccd715707.."$MB"; git -C "$W" rev-list --count upstream/master..rocknix/master )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the lines two ways (expect wc -l 22567; grep -c 22575; no trailing newline: 8, the files § 2 names; R1 C11)'
t0=$(date +%s)
( for p in $FILES; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'; for p in $FILES; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c", s}'; n=0; for p in $FILES; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && { n=$((n+1)); echo "no newline: $p $a/$b"; }; done; echo "no trailing newline: $n" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the fork'"'"'s delta (expect `13 files changed, 247 insertions(+), 71 deletions(-)` three times -- R1 C13, C15, and C14 read from master'"'"'s side; A 1; M 12 -- R1 C15'"'"'s name-status; the 12 numstat rows; 19 commits with merges, 17 without, 2 merges -- R1 C16, the proof'"'"'s lines)'
t0=$(date +%s)
( git -C "$W" diff --shortstat bccd715707 "$PIN" -- $FILES; git -C "$W" diff --shortstat "$MB" "$PIN" -- $FILES; git -C "$W" diff --shortstat rocknix/master "$PIN" -- $FILES; git -C "$W" diff --diff-filter=A --name-only bccd715707 "$PIN" -- $FILES | $G -c .; rc=$?; echo "added rc=$rc"; git -C "$W" diff --diff-filter=M --numstat bccd715707 "$PIN" -- $FILES; git -C "$W" log --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --no-merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; rc=$?; echo "merges rc=$rc" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# upstream'"'"'s delta: the merge-debt record (expect upstream commits 0 rc=1 and numstat 0 rc=1; identical to rocknix/master: 83; identical to cada856d86: 83; MB-vs-master identical: 96; batocera commits on the 96: 12; batocera files: 9; both-changed: 6 -- R1 C12, C14, C17, C18 and R1 § 3, every line printed by the proof on 2026-10-31)'
t0=$(date +%s)
( git -C "$W" log --format=%h "$MB"..rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream commits rc=$rc"; git -C "$W" diff --numstat "$MB" rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream numstat rc=$rc"; n=0; for p in $FILES; do git -C "$W" diff --quiet rocknix/master "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to rocknix/master: $n"; n=0; for p in $FILES; do git -C "$W" diff --quiet "$MB" "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to cada856d86: $n"; n=0; for p in $FILES; do git -C "$W" diff --quiet "$MB" rocknix/master -- "$p" && n=$((n+1)); done; echo "MB-vs-master identical: $n"; git -C "$W" log --format=%h 1750dded8c..batocera/master -- $FILES | $G -c .; git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | $G -c .; comm -12 <(git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | sort) <(git -C "$W" diff --name-only "$MB" "$PIN" -- $FILES | sort) | $G -c . )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the other lanes'"'"' deltas inside the 96 (expect every stat line empty except T21'"'"'s `es-core/CMakeLists.txt`, `1 file changed, 5 insertions(+)` -- R1 C20, C21, the proof'"'"'s line; T34'"'"'s `origin/` ref prints `fatal: bad revision` -- recorded, not a stop, R1 C19)'
t0=$(date +%s)
( for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680 m6-es-core-components-681; do echo "== $b"; git -C "$W" diff --stat "$PIN" "origin/feature/$b" -- $FILES 2>&1 | tail -n 1; done )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the strings, two ways (expect `_(" lines TOTAL 86 in 10 files` -- R2 cmd 8'"'"'s 86, the proof'"'"'s 10; the per-file -c: Window.cpp 37, guis/GuiInputConfig.cpp 14, guis/GuiTextEditPopupKeyboard.cpp 11, GunManager.cpp 6, guis/GuiDetectDevice.cpp 5, InputManager.cpp 4, guis/GuiMsgBox.cpp 3, guis/GuiTextEditPopup.cpp 3, BindingManager.cpp 2, TextToSpeech.cpp 1 -- R3 cmd 23 and the proof; the occurrence count 97)'
t0=$(date +%s)
( git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "_(\" lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F '_("' "$PIN" -- $FILES | wc -l; git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN:es-core\/src\///" | tr '\n' ' '; echo )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the log lines (expect `LOG(Log lines TOTAL 158 in 20 files` -- R2 cmd 9; VolumeControl.cpp 32, ThemeData.cpp 25, InputManager.cpp 20, AudioManager.cpp 19 the four largest)'
t0=$(date +%s)
( git -C "$W" grep -c 'LOG(Log' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "LOG(Log lines TOTAL", s, "in", NR, "files"}' )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the threads and the lifetimes (expect 18 matching lines -- R2 cmd 10: Log.cpp 60 180; Scripting.cpp 18 68; TextToSpeech.cpp 92, .h 47; VolumeControl.cpp 32 203; Window.cpp 1554 1563 1572 1575 1608 1619 1634 1637; watchers/WatchersManager.cpp 61, .h 88; `.detach(` 4, all Window.cpp -- R2 § 6; Scripting.cpp:68 is `new std::thread(&executeCommandsThread)` under WIN32, not a detach (the proof); `postToUiThread`: Window.cpp:1276 the definition, :1556 :1574 :1612 :1636 the calls, Window.h:91 (the proof))'
t0=$(date +%s)
( git -C "$W" grep -n -E 'std::thread|\.detach\(|new std::thread|std::async' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::thread|\.detach\(|new std::thread|std::async' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F '.detach(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'postToUiThread' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the process spawns (expect 4, all ProcessStartInfo: InputManager.cpp:1272, Scripting.cpp:43 :131 :140 -- R2 cmd 11; system( / popen( / runSystemCommand( 0 rc=1)'
t0=$(date +%s)
( git -C "$W" grep -n -E '(^|[^A-Za-z_:])system\(|popen\(|runSystemCommand\(|ProcessStartInfo' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E '(^|[^A-Za-z_:])system\(|popen\(|runSystemCommand\(' "$PIN" -- $FILES | $G -c .; rc=$?; echo "shell spawns rc=$rc" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the writes (expect 9 lines -- R2 cmd 13'"'"'s seven write sites, InputManager.cpp:1225 :1232 save_file; FavoriteMusicManager.cpp:71 :115 ofstream; Log.cpp:179; AudioManager.cpp:539 :610 fopen; plus es-core/CMakeLists.txt:122 :257, the `AtomicFileUtil` registrations the alternation matches (the proof); AtomicFile:: 0 rc=1)'
t0=$(date +%s)
( git -C "$W" grep -n -E 'std::ofstream|ofstream|AtomicFile|save_file\(|fopen\(|writeText|writeFile|std::rename|rename\(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::ofstream|ofstream|AtomicFile|save_file\(|fopen\(|writeText|writeFile|std::rename|rename\(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'AtomicFile::' "$PIN" -- $FILES | $G -c .; rc=$?; echo "atomic rc=$rc" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the reads (expect `FileSystem::exists(` 41; uncached 0 rc=1 -- R2 cmd 12; the per-file list R2 § 2.3 names)'
t0=$(date +%s)
( git -C "$W" grep -n -E 'FileSystem::exists\(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E 'FileSystem::exists\([^)]*,[[:space:]]*false' "$PIN" -- $FILES | $G -c .; rc=$?; echo "uncached rc=$rc" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the input and the help bar (expect `getHelpPrompts` definitions 3 -- guis/GuiMsgBox.cpp:296, guis/GuiTextEditPopup.cpp:81, guis/GuiTextEditPopupKeyboard.cpp:449 -- and `input(InputConfig` definitions 6 -- GuiComponent.cpp:54, Window.cpp:215, guis/GuiDetectDevice.cpp:87, guis/GuiMsgBox.cpp:246, guis/GuiTextEditPopup.cpp:66, guis/GuiTextEditPopupKeyboard.cpp:335 (the proof); the eight `mHelp->` lines in Window.cpp: 745 1001 1009 1011 1012 1077 1397 1398 -- T34'"'"'s brief `:1422`, R4 item 12; `mHelp->setOpacity` 0 rc=1)'
t0=$(date +%s)
( git -C "$W" grep -n -E '::getHelpPrompts\(\)' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '::input\(InputConfig' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'mHelp->' "$PIN" -- es-core/src/Window.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'mHelp->setOpacity' "$PIN" -- es-core/src/Window.cpp | $G -c .; rc=$?; echo "mHelp setOpacity rc=$rc" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the constants (expect the two BUTTON_GRID_HORIZ_PADDING definitions: components/MenuComponent.cpp:14 at 0.022 and guis/GuiTextEditPopupKeyboard.cpp:14 at 0.0052083333 -- R2 cmd 20; the keyboard'"'"'s use at :220; GuiMsgBox.cpp:21-23 MSGBOX_WIDTH 0.6 / WIDE 0.8 / LINES 4; GuiInfoPopup.cpp:17-18 0.9f / 0.2f; Window.cpp:1181 PADDING_H, :1183 :1192 the card'"'"'s position -- R2 § 1.3, § 4)'
t0=$(date +%s)
( git -C "$W" grep -n -E 'BUTTON_GRID_HORIZ_PADDING' "$PIN" -- es-core/src/components/MenuComponent.cpp es-core/src/guis/GuiTextEditPopupKeyboard.cpp | sed "s/^$PIN://" | cut -c1-160; git -C "$W" grep -n -E 'MSGBOX_(WIDTH|WIDE_WIDTH|WIDE_LINES)|maxWidth|maxHeight|PADDING_H|posX = ' "$PIN" -- es-core/src/guis/GuiMsgBox.cpp es-core/src/guis/GuiInfoPopup.cpp es-core/src/Window.cpp | sed "s/^$PIN://" | $G -E '#define|const |float |posX' | cut -c1-160 )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the includes (expect SDL/VLC/GL angle lines over the 101: 18 -- R3 cmd 4; quoted SDL: 2 -- R3 cmd 16; the cross-tree include: Window.cpp:29 -- R2 § 1.7; the named-once loop prints `named-0-times (or more than once): 9` -- seven entries named once with a trailing `# batocera` comment the anchor rejects (LocaleES.cpp, LocaleES.h, gettext.h, guis/GuiInfoPopup.cpp, guis/GuiInfoPopup.h, guis/GuiTextEditPopupKeyboard.cpp, guis/GuiTextEditPopupKeyboard.h) and two headers registered nowhere (HelpPrompt.h, Scripting.h); every .cpp of the 44 named once (the proof; R3 cmd 21'"'"'s claim held for the sources); `if(` at 278 287 -- R3 cmd 21)'
t0=$(date +%s)
( git -C "$W" grep -n -E '#include <SDL|#include <vlc|#include <GL' "$PIN" -- es-core/src | $G -v -E 'components|utils|resources|renderers' | $G -c .; git -C "$W" grep -n -E '#include "(SDL|vlc|GL|curl|libudev)' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '^\s*#\s*include\s*"\.\./' "$PIN" -- $FILES | sed "s/^$PIN://"; n=0; for p in $FILES; do [ "$p" = es-core/CMakeLists.txt ] && continue; b=${p#es-core/}; git -C "$W" grep -c -E "/${b}[[:space:]]*\$" "$PIN" -- es-core/CMakeLists.txt | sed "s/^$PIN://" | $G -q ':1$' || { echo "not once: $p"; n=$((n+1)); }; done; echo "named-0-times (or more than once): $n"; git -C "$W" grep -n -E '^\s*if\s*\(' "$PIN" -- es-core/CMakeLists.txt | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the in-source gates (expect 128 lines (the proof), the ROCKNIX, BATOCERA, WIN32, HAVE_UDEV, _ENABLE_PULSE_, HAVE_LIBCEC, _ENABLE_TTS_ guards of R3 § 2.2 and R2 § 0 among them -- Splash.h:10, InputManager.cpp:585, VolumeControl.cpp:11 (its include :14), CECInput.h:7 (:8), TextToSpeech.cpp:53 (:54); `git grep -n ROCKNIX` over the 96: 3 lines, InputManager.cpp:585, Paths.cpp:76, Splash.h:10)'
t0=$(date +%s)
( git -C "$W" grep -n -E '^\s*#\s*(if|ifdef|ifndef|elif)\b.*(ROCKNIX|BATOCERA|WIN32|HAVE_UDEV|_ENABLE_PULSE_|HAVE_LIBCEC|_ENABLE_TTS_|_RPI_)' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the non-ASCII bytes (expect 28 lines rc=0 under LC_ALL=C; files with a non-ascii byte: 4 -- AudioManager.cpp 3, GunManager.cpp 1, InputManager.cpp 2, guis/GuiTextEditPopupKeyboard.cpp 22, the glyph literals es-code-traps.md:60 allows; files with a non-ascii comment line: 3 -- AudioManager.cpp:352 :362 :383, GunManager.cpp:145, InputManager.cpp:393 :1437, every one upstream'"'"'s: the fork'"'"'s -U0 diff against cada856d86 adds 0 (the proof); InputManager.cpp:856 :869 are ASCII)'
t0=$(date +%s)
( git -C "$W" grep -n -P '[^\x00-\x7F]' "$PIN" -- $FILES | $G -c .; rc=$?; echo "git grep -P rc=$rc"; n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | LC_ALL=C $G -c -P '[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "${f#es-core/src/}:$c"; n=$((n+1)); }; done; echo "files with a non-ascii byte: $n"; n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | LC_ALL=C $G -c -P '^\s*//.*[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "comment: ${f#es-core/src/}:$c"; n=$((n+1)); }; done; echo "files with a non-ascii comment line: $n" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the French (expect six lines -- CANCEL 49, GAMEPAD %i 3898, SET SELECT AS HOTKEY 3915, DO NOT ASSIGN HOTKEY 3918, the detect sentence with its period 3779, CLEAR 6923 (the proof; HOTKEY ENABLE is no msgid, the key is the identifier HotKeyEnable); `^msgid ` lines 2207 -- T34'"'"'s brief `:1416` at the same pin; es-untranslated `706 fork string(s) in the source, 706 with French, 0 without` rc 0 and `703 ... 0 without` rc 0 -- the proof, over the qa-integration checkout at the pin)'
t0=$(date +%s)
( git -C "$W" grep -n -E '^msgid "(CLEAR|CANCEL|HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT\.|GAMEPAD %i|SET SELECT AS HOTKEY|DO NOT ASSIGN HOTKEY)"$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://" | cut -d: -f2,3 | tr '\n' ' '; echo; git -C "$W" grep -c -E '^msgid ' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://"
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream "$MB" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated(cada) rc=$rc" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the candidate lines (expect Window.cpp `339 340` for back()/pop_back(); `1164` for notificationDuration(-1); WatchersManager.cpp `181` for the unique_lock and `196` for check(); Scripting.cpp `92 93` and `109 112` for the quoting; InputManager.cpp `946 960` for the two approximate logs, `1225 1232` save_file; GuiMsgBox.cpp `44 234` say; GuiInputConfig.cpp `134` -- R2 §§ 1-5)'
t0=$(date +%s)
( git -C "$W" grep -n -E 'mNotificationMessages\.(back|pop_back)\(' "$PIN" -- es-core/src/Window.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'notificationDuration(-1)' "$PIN" -- es-core/src/Window.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -E 'unique_lock<std::mutex> lock\(mWatchersLock\)|component->check\(\)' "$PIN" -- es-core/src/watchers/WatchersManager.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'Approximative device found' "$PIN" -- es-core/src/InputManager.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'save_file(' "$PIN" -- es-core/src/InputManager.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'TextToSpeech::getInstance()->say(' "$PIN" -- es-core/src/guis/GuiMsgBox.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'getDeviceId() + 1' "$PIN" -- es-core/src/guis/GuiInputConfig.cpp | sed "s/^$PIN://" | cut -d: -f2 )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the menu map (expect `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 -- T34'"'"'s brief `:1424` at the same pin, the map 989 lines and unchanged since; the checker'"'"'s SOURCE_DIRS at its :58 include es-core/src/guis)'
t0=$(date +%s)
( out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"; wc -l docs/es-menu-map.md; sed -n '58p' tools/es-menu-map-check )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2 -- R3 cmd 12, #1137; plain g++ on GuiMsgBox.cpp rc 1 with `es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory` -- printed by the proof for this file over a `git archive` of the pin (g++ 15.2.0; Window.cpp the same line, InputManager.cpp at InputManager.h:5:10; WatchersManager.cpp, Scripting.cpp, math/Vector2f.cpp rc 0 plain), as R4 item 25 and T31 `02:565` predicted; the pugixml root present -- R3 cmd 17; then the stand-in check over the 44 with the fakes, rc per file, R3 § 3.3'"'"'s classes the prediction)'
t0=$(date +%s)
( F=es-core/src/guis/GuiMsgBox.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:'; echo "plain g++ rc=$rc"
PUGI=/workspace/cache/rocknix-sources/emulationstation/emulationstation-$PIN/external; test -d "$PUGI/pugixml/src" && echo "pugixml root present" )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"
echo; echo '# STAGE C -- the lane'"'"'s scripts, which do not exist at stage A (expect the stand-in'"'"'s `<file>: rc N` line per .cpp, 44 lines; the build script'"'"'s own `TOTAL: N test cases in B binaries` with 0 failed and `window-input-tests` among the binaries; before any fix the candidates'"'"' FAIL lines by name and 3.27'"'"'s script FAILing at the pin)'
echo 'CANNOT at stage A: the three scripts below are the lane'"'"'s stage-C inputs (stage-a/syntax-check.sh, tools/t35-build-tests.sh, stage-c/pl25-screensaver.py) and do not exist yet; each runs at stage C'
echo '  (not run) bash docs/audits/*-epic-m6-es-core-window-input/stage-a/syntax-check.sh 2>&1 | tail -n 46'
echo '  (not run) bash docs/audits/*-epic-m6-es-core-window-input/tools/t35-build-tests.sh "$W" 2>&1 | tail -n 10'
echo '  (not run) python3 -I docs/audits/*-epic-m6-es-core-window-input/stage-c/pl25-screensaver.py "$W" 2>&1 | tail -n 3'
echo; echo '# STAGE A, after the pointer is read -- the removal check: the own tip of the lane, b51dd8a805 at stage A (the merge commit the dispatch comment and the pointer name, filling the placeholder of the brief) (expect empty) and the ES diff against the pin (expect empty before stage E)'
echo '(the own tip of the lane is b51dd8a805 at stage A: the merge commit the dispatch comment and the pointer name)'
t0=$(date +%s)
( git diff --stat b51dd8a805 HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1 )
rc=$?
t1=$(date +%s); echo "run rc=$rc wall=$((t1-t0))s"

#!/bin/bash
# T36 stage A: the brief's § 5 runs (es-core-utils-resources.md:1574-1624 at b1f34ce658), each command verbatim in its own
# subshell with an rc= line and a date +%s pair. The three STAGE C lines are recorded, not run (their scripts do not exist
# at stage A). TIPHASH is the pointer's value at stage A, 4b8285f4ab. Run from the distribution worktree.
echo "run at $(date -u +%FT%TZ)"
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t36/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
FILES=$(cat .qa-scratch/t36/paths.txt)
echo; printf "=== r01 (brief :1577) %s\n" 'the scope (expect 58; cpp 25; h 32; hpp 1; 14 renderers, 11 resources, 33 utils -- R1 C05)'
t0=$(date +%s)
( printf '%s\n' $FILES | $G -c .; printf '%s\n' $FILES | $G -c '\.cpp$'; printf '%s\n' $FILES | $G -c '\.h$'; printf '%s\n' $FILES | $G -c '\.hpp$'; printf '%s\n' $FILES | sed -E 's#^es-core/src/([^/]+)/.*#\1#' | sort | uniq -c )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r02 (brief :1579) %s\n" 'the ES worktree at the pin, clean; the bases (expect the pin; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c; bccd715707 the merge base'"'"'s parent -- R1 C01; 14 commits cada856d86..rocknix/master on '
t0=$(date +%s)
( git -C "$W" rev-parse HEAD | cut -c1-10; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" rev-parse rocknix/master | cut -c1-10; git -C "$W" rev-parse batocera/master | cut -c1-10; git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10; git -C "$W" rev-parse --short=10 "$MB^1"; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count "$MB"..rocknix/master -- es-core/ )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r03 (brief :1581) %s\n" 'the lines two ways (expect wc -l 50827; grep -c 50840; no trailing newline: 13, the files § 2 names; han.h + zip_file.hpp grep -c 30934 -- R1 C09)'
t0=$(date +%s)
( for p in $FILES; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'; for p in $FILES; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c", s}'; n=0; for p in $FILES; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && { n=$((n+1)); echo "no newline: $p $a/$b"; }; done; echo "no trailing newline: $n"; for p in es-core/src/utils/han.h es-core/src/utils/zip_file.hpp; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "han.h + zip_file.hpp grep -c", s}' )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r04 (brief :1583) %s\n" 'the fork'"'"'s delta (expect `15 files changed, 1032 insertions(+), 60 deletions(-)` against bccd715707 and against cada856d86 -- R1 C07, C11; `15 files changed, 60 insertions(+), 1032 deletions(-)` from '
t0=$(date +%s)
( git -C "$W" diff --shortstat bccd715707 "$PIN" -- $FILES; git -C "$W" diff --shortstat "$MB" "$PIN" -- $FILES; git -C "$W" diff --shortstat "$PIN" rocknix/master -- $FILES; git -C "$W" diff --name-status "$MB" "$PIN" -- $FILES | cut -c1 | sort | uniq -c; git -C "$W" diff --numstat "$MB" "$PIN" -- $FILES; git -C "$W" log --oneline "$MB".."$PIN" -- $FILES | $G -c .; git -C "$W" log --oneline --merges "$MB".."$PIN" -- $FILES | $G -c .; git -C "$W" rev-list --count bccd715707.."$PIN" -- $FILES )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r05 (brief :1585) %s\n" 'upstream'"'"'s delta: the merge-debt record (expect upstream commits 0 rc=1 -- R1 C13; blob-identical to rocknix/master 43 -- R1 C10; batocera on the 58: 13 commits and `9 files changed, 668 insertions(+)'
t0=$(date +%s)
( git -C "$W" log --format=%h "$MB"..rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream commits rc=$rc"; n=0; for p in $FILES; do [ "$(git -C "$W" rev-parse "$PIN:$p")" = "$(git -C "$W" rev-parse -q --verify "rocknix/master:$p")" ] && n=$((n+1)); done; echo "identical to rocknix/master: $n"; git -C "$W" rev-list --count 1750dded8c..batocera/master -- $FILES; git -C "$W" diff --shortstat 1750dded8c batocera/master -- $FILES; comm -12 <(git -C "$W" diff --name-only "$MB" "$PIN" -- $FILES | sort) <(git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | sort) )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r06 (brief :1587) %s\n" 'the other lanes'"'"' deltas inside the 58 (expect T20 `1 file changed, 4 insertions(+)`; T26 `1 file changed, 15 insertions(+), 5 deletions(-)`; T21'"'"'s stat naming utils/FileSystemUtil.cpp, and with the tw'
t0=$(date +%s)
( for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680 m6-es-core-components-681 m6-es-core-window-input-682; do echo "== $b"; git -C "$W" diff --stat "$PIN" "origin/feature/$b" -- $FILES 2>&1 | tail -n 2; done; git -C "$W" diff --shortstat "$PIN" origin/feature/m6-es-state-and-bridge-668 -- $FILES es-core/src/utils/DownloadFile.cpp es-core/src/utils/DownloadFile.h )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r07 (brief :1589) %s\n" 'the collisions'"'"' commits (expect d9afa5c7c to resolve, an ancestor of T20'"'"'s tip, its stat `FileSystemUtil.cpp | 4` -- proof U-8, CMD3; f7c16144d'"'"'s stat `FileSystemUtil.cpp | 17` with the path given, it'
t0=$(date +%s)
( git -C "$W" show --stat --format='%h %ad %s' --date=short d9afa5c7c -- es-core/src/utils/FileSystemUtil.cpp 2>&1; git -C "$W" show --stat --format='%h %ad %s' --date=short f7c16144d -- es-core/src/utils/FileSystemUtil.cpp 2>&1; git -C "$W" log --oneline "$PIN"..origin/feature/m6-es-guimenu-673 -- es-core/src/utils/Platform.cpp 2>&1 )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r08 (brief :1591) %s\n" 'the strings, two ways (expect `_(" lines TOTAL 11 in 2 files` -- R2 cmd 28, R3 cmd 17, proof K-148 -- MathExpr.cpp and TimeUtil.cpp; the occurrence count 12, MathExpr.cpp:95 carrying two strings -- R2'
t0=$(date +%s)
( git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "_(\" lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F '_("' "$PIN" -- $FILES | wc -l; git -C "$W" grep -n -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r09 (brief :1593) %s\n" 'the French of the seven msgids (expect each with a non-empty msgstr: never jamais, %d d %d j, %d h %d h, %d mn %d mn, %d sec %d sec, Unknown Inconnu, None Aucun, at po :143 :1673 :3554 :4007 :4011 :40'
t0=$(date +%s)
( git -C "$W" grep -n -A1 -E '^msgid "(never|%d d|%d h|%d mn|%d sec|Unknown|None)"$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://" )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
t0=$(date +%s)
( out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc" )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r10 (brief :1596) %s\n" 'the log lines (expect `LOG(Log lines TOTAL 99 in 16 files` -- R2 cmd 28, proof K-149)'
t0=$(date +%s)
( git -C "$W" grep -c 'LOG(Log' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "LOG(Log lines TOTAL", s, "in", NR, "files"}' )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r11 (brief :1598) %s\n" 'the threads and the lifetimes (expect `threads count: 10` -- TextureDataManager.cpp 217 222 234, .h 45; FileSystemUtil.cpp 1788 1797; ThreadPool.cpp 26 84 91, .h 68 -- and one `.detach(`, FileSystemUt'
t0=$(date +%s)
( git -C "$W" grep -n -E 'std::thread|\.detach\(|std::async|pthread_create' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::thread|\.detach\(|std::async|pthread_create' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F '.detach(' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'weak_ptr' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'delete this' "$PIN" -- $FILES | $G -c .; rc=$?; echo "delete this rc=$rc" )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r12 (brief :1600) %s\n" 'the locks (expect 63 lines: ResourceManager.cpp 2, TextureData.cpp 7, TextureData.h 1, TextureDataManager.cpp 12, TextureDataManager.h 7, ConcurrentVector.h 9, FileSystemUtil.cpp 14, StringListLock.cp'
t0=$(date +%s)
( git -C "$W" grep -c -E 'std::mutex|shared_mutex|recursive_mutex|lock_guard|unique_lock|shared_lock|condition_variable|std::atomic' "$PIN" -- $FILES | sed "s/^$PIN:es-core\/src\///" | tr '\n' ' '; echo; git -C "$W" grep -n -E 'std::mutex|shared_mutex|recursive_mutex|lock_guard|unique_lock|shared_lock|condition_variable|std::atomic' "$PIN" -- $FILES | $G -c . )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r13 (brief :1602) %s\n" 'the process spawns (expect `spawn count: 16`, every line in utils/Platform.cpp -- R2 cmd 17, § 5)'
t0=$(date +%s)
( git -C "$W" grep -n -E 'system\(|popen\(|execl|execv|fork\(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'system\(|popen\(|execl|execv|fork\(' "$PIN" -- $FILES | $G -c . )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r14 (brief :1604) %s\n" 'the writes (expect the `fopen(... "w"` lines FileSystemUtil.cpp 1432 1434 1490 1492 -- R2 cmd 28'"'"'s corrected listing, the first pattern'"'"'s 8 having missed them, R2 § 5; zip_file.hpp'"'"'s `fopen\(|ofstream'
t0=$(date +%s)
( git -C "$W" grep -n -E 'fopen\(.*"[wa]' "$PIN" -- es-core/src/utils/FileSystemUtil.cpp es-core/src/utils/Platform.cpp | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'fopen\(|ofstream' "$PIN" -- es-core/src/utils/zip_file.hpp | $G -c . )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r15 (brief :1606) %s\n" 'the helpers'"'"' reach over es-app/src and es-core/src (expect runSystemCommand\( 80, ProcessStartInfo 13, GetShOutput\( 27, GetShOutputLines\( 9, writeAllText\( 27, renameFile\( 17, copyFile\( 12, readAl'
t0=$(date +%s)
( for pat in 'runSystemCommand\(' 'ProcessStartInfo' 'GetShOutput\(' 'GetShOutputLines\(' 'writeAllText\(' 'renameFile\(' 'copyFile\(' 'readAllText\(' 'readAllLines\(' 'AtomicFile::'; do printf '%s ' "$pat"; git -C "$W" grep -n -E "$pat" "$PIN" -- es-app/src es-core/src | $G -c .; done )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r16 (brief :1608) %s\n" 'the includes and the gates (expect the angle-include line count 241 -- proof CMD4; of them 41 non-standard by R3 cmd 9'"'"'s rule (NON-STD ANGLE INCLUDES: 41), whose standard list is unstated, so the lane'
t0=$(date +%s)
( git -C "$W" grep -n -E '^\s*#\s*include\s*<' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '^\s*#\s*include\s+[A-Z_]+' "$PIN" -- $FILES | sed "s/^$PIN://"; git -C "$W" grep -n -E '^\s*#\s*(if|ifdef|ifndef|elif)\b.*ROCKNIX' "$PIN" -- $FILES | $G -c .; rc=$?; echo "ROCKNIX gates rc=$rc"; git -C "$W" grep -n -F 'USE_OPENGLES_30' "$PIN" -- es-core/src/renderers | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -w 'GLES3' "$PIN" -- es-core/src | $G -c .; rc=$?; echo "GLES3 macro rc=$rc" )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r17 (brief :1610) %s\n" 'the non-ASCII bytes (expect files with a non-ASCII byte 3 -- FileSystemUtil.cpp 3 (`//` comments 225 287 718), StringUtil.cpp 2 (1406 1407, trailing comments after code), StringUtil.h 7 (62-68, string'
t0=$(date +%s)
( n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | LC_ALL=C $G -c -P '[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "${f#es-core/src/}:$c"; n=$((n+1)); }; done; echo "files with a non-ascii byte: $n"; git -C "$W" grep -n -P '[^\x00-\x7F]' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r18 (brief :1612) %s\n" 'the candidate lines (expect `text[pos] +=` at StringUtil.cpp `359 400`, inside 359-361 and 400-402 -- R2 § 1.1, proof K-157; `head -300` at Platform.cpp `162` and `164`, the second the log-off variant'
t0=$(date +%s)
( git -C "$W" grep -n -F 'text[pos] +=' "$PIN" -- es-core/src/utils/StringUtil.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'head -300' "$PIN" -- es-core/src/utils/Platform.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -i -F 'always initialize ascii' "$PIN" -- es-core/src/resources/Font.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -F '[&]' "$PIN" -- es-core/src/utils/FileSystemUtil.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'exists(localFile' "$PIN" -- es-core/src/resources/TextureData.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" show "$PIN:es-core/src/utils/Platform.cpp" | sed -n '853,880p' | $G -n -E 'return|name|window' )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r19 (brief :1614) %s\n" 'the pipe'"'"'s literal, 3.5, in two forms (expect `seq 400 rc=0` -- 1,492 bytes held whole by the pipe, the PASS-at-pin control -- and `seq 200000 rc=141` -- output past the pipe buffer, the FAIL-at-pin c'
t0=$(date +%s)
( for n in 400 200000; do sh -c "((((seq 1 $n 2> /dev/null ; echo \$? >&3) | head -300 > /dev/null) 3>&1) | (read xs; exit \$xs))"; rc=$?; echo "seq $n rc=$rc"; done; seq 1 400 | wc -c; readlink -f "$(command -v sh)" )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r20 (brief :1616) %s\n" 'the menu map (expect the checker'"'"'s line, and its SOURCE_DIRS at :58 naming es-app/src/guis and es-core/src/guis, no slice directory -- R3 § 5)'
t0=$(date +%s)
( out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"; sed -n '58p' tools/es-menu-map-check )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r21 (brief :1618) %s\n" 'the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2 -- R3 § 5, cmd 19, #1137)'
t0=$(date +%s)
( F=es-core/src/utils/Platform.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc" )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"
echo; printf "=== r22 (brief :1620) %s\n" 'STAGE C -- the lane'"'"'s scripts, which do not exist at stage A (expect the stand-in'"'"'s `rc=N <file>` line per .cpp, 25 lines, with the renderer positives -- nonzero with -DUSE_OPENGLES_30, zero without -'
echo "not run at stage A: the lane's stage-C scripts (stage-a/syntax-check.sh, tools/t36-build-tests.sh) do not exist yet"
echo; printf "=== r23 (brief :1623) %s\n" 'STAGE A, after the pointer is read -- the removal check: TIPHASH is the lane'"'"'s own tip the pointer and the dispatch comment name (MERGE_HASH at stage A); the literal word fails with `fatal: bad revisi'
t0=$(date +%s)
( git diff --stat 4b8285f4ab HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1 )
rc=$?; echo "rc=$rc wall=$(( $(date +%s) - t0 ))s"

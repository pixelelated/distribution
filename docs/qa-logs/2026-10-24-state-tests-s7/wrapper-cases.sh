#!/bin/bash
# wrapper-cases.sh -- T14 S7's control for #996 (retroarch-wrapper-test): the
# stage-D test and the fixed one, each run against the same scratch copies of
# video_thread_wrapper.c, each with a fresh TMPDIR under the scratch:
#   plain      -- the source as copied
#   wrong-site -- send_packet keeps the first command's method and takes only
#                 the new data: every post runs the first site's method, so one
#                 site runs twice as often and the other never, and the total
#                 is still the number posted
#   no-gcc     -- PATH holds python3 and nothing else
#   killed     -- gcc is a shim that sleeps; the tool is sent SIGTERM mid-build
#   bare       -- no source given and RETROARCH_SRC unset
# Nothing outside the scratch.
#   wrapper-cases.sh <tree> <stage-D tools dir> <video_thread_wrapper.c> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; SRC="$(readlink -f "$3")"; S="$4"; rm -rf "$S"; mkdir -p "$S"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
mkdir -p "$S/plain/gfx" "$S/wrong/gfx" "$S/nogcc-bin" "$S/shim-bin"
cp "$SRC" "$S/plain/gfx/"; cp "$SRC" "$S/wrong/gfx/"
W="$S/wrong/gfx/video_thread_wrapper.c"
sed -i 's#^   thr->cmd_data  = \*pkt;$#   if (!thr->cmd_data.data.custom_command.method) thr->cmd_data = *pkt; else { thr->cmd_data.type = pkt->type; thr->cmd_data.data.custom_command.data = pkt->data.custom_command.data; }#' "$W"
grep -q 'if (!thr->cmd_data.data.custom_command.method)' "$W" || { echo "wrong-site mutation did not apply"; exit 2; }
ln -s "$(command -v python3)" "$S/nogcc-bin/python3"
# the shim records its pid, then becomes the sleep, so the control ends it by that pid
printf '#!/bin/sh\necho $$ > "$SHIM_PID"\nexec sleep 30\n' > "$S/shim-bin/gcc"; chmod 755 "$S/shim-bin/gcc"
leftovers() { find "$1" -name t.c | wc -l; }
for side in old:"$OLD/retroarch-wrapper-test" new:"$T/tools/retroarch-wrapper-test"; do
  n=${side%%:*}; t=${side#*:}
  for c in plain wrong nogcc killed bare; do mkdir -p "$S/$n-$c-tmp"; done
  TMPDIR="$S/$n-plain-tmp" python3 -I "$t" "$S/plain/gfx/video_thread_wrapper.c" > "$S/$n-plain.txt" 2>&1; a=$?
  TMPDIR="$S/$n-wrong-tmp" python3 -I "$t" "$W" > "$S/$n-wrong.txt" 2>&1; b=$?
  TMPDIR="$S/$n-nogcc-tmp" PATH="$S/nogcc-bin" python3 -I "$t" "$S/plain/gfx/video_thread_wrapper.c" > "$S/$n-nogcc.txt" 2>&1; c=$?
  SHIM_PID="$S/$n-shim.pid" TMPDIR="$S/$n-killed-tmp" PATH="$S/shim-bin:/usr/bin:/bin" python3 -I "$t" "$S/plain/gfx/video_thread_wrapper.c" > "$S/$n-killed.txt" 2>&1 & p=$!
  sleep 2; [ -s "$S/$n-shim.pid" ] || { echo "the gcc shim never started"; exit 2; }
  kill -TERM "$p"; wait "$p"; d=$?; kill -TERM "$(cat "$S/$n-shim.pid")" 2>/dev/null
  ( cd "$S" && env -u RETROARCH_SRC TMPDIR="$S/$n-bare-tmp" python3 -I "$t" > "$S/$n-bare.txt" 2>&1 ); e=$?
  la=$(leftovers "$S/$n-plain-tmp"); lk=$(find "$S/$n-killed-tmp" -mindepth 1 | wc -l)
  echo "  $n: plain rc $a ($la t.c left) | wrong-site rc $b ($(grep -m1 -E '^(PASS|FAIL)' "$S/$n-wrong.txt")) | no gcc rc $c ($(tail -1 "$S/$n-nogcc.txt" | cut -c1-70)) | killed rc $d, $lk entries left | bare rc $e"
  if [ "$n" = old ]; then
    check "stage-D passes the plain source and leaves t.c behind (the positive)" "$([ "$a" = 0 ] && [ "$la" -ge 1 ] && echo 0 || echo 1)"
    check "stage-D passes the wrong-site source: the total still equals the posts (the positive)" "$([ "$b" = 0 ] && echo 0 || echo 1)"
    check "stage-D exits 1, the 'ran twice' code, when gcc is missing (the positive)" "$([ "$c" = 1 ] && echo 0 || echo 1)"
    check "stage-D leaves its scratch behind when killed (the positive)" "$([ "$lk" -ge 1 ] && echo 0 || echo 1)"
  else
    check "fixed passes the plain source and leaves nothing" "$([ "$a" = 0 ] && [ "$la" = 0 ] && [ -z "$(ls -A "$S/$n-plain-tmp")" ] && echo 0 || echo 1)"
    check "fixed fails the wrong-site source, per site" "$([ "$b" = 1 ] && grep -q 'site 1 posted 1000 command(s); its method ran 0 time(s)' "$S/$n-wrong.txt" && echo 0 || echo 1)"
    check "fixed exits 2 naming gcc when it is missing" "$([ "$c" = 2 ] && grep -q 'no gcc on PATH' "$S/$n-nogcc.txt" && echo 0 || echo 1)"
    check "fixed removes its scratch when killed" "$([ "$lk" = 0 ] && echo 0 || echo 1)"
    check "fixed's bare run exits 2 with a usage line naming RETROARCH_SRC" "$([ "$e" = 2 ] && grep -q '^usage: .*RETROARCH_SRC=' "$S/$n-bare.txt" && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi

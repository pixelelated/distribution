#!/bin/bash
# T26 (#673) stage A: the brief's § 5 runs, each with its exit and wall time.
# Run from the distribution worktree. The lane's generators for 02's tables
# (t26-rows.py, t26-structure.py) are stage B's and are not run here.
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; F=es-app/src/guis/GuiMenu.cpp
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t26/tmp; mkdir -p "$TMPDIR"; A=docs/audits/2026_10_27-epic-m6-es-guimenu
run() { # <label> <command string>
  local t0 t1 out rc
  t0=$(date +%s.%N); out=$(eval "$2" 2>&1); rc=$?; t1=$(date +%s.%N)
  printf '== %s  (rc %s, %.2f s)\n%s\n\n' "$1" "$rc" "$(echo "$t1 - $t0" | bc)" "$out"
}
run "df -i" 'df -i /workspace | tail -n 1'
run "the ES worktree, the merge base, the delta" 'git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l; git -C "$W" merge-base bccd715707 HEAD | cut -c1-10; git -C "$W" diff --numstat bccd715707 "$PIN" -- es-app/src/guis/GuiMenu.cpp es-app/src/guis/GuiMenu.h'
run "the definitions" 'git -C "$W" show "$PIN:$F" > "$TMPDIR/pin.cpp"; git -C "$W" show "bccd715707:$F" > "$TMPDIR/base.cpp"; python3 -I -B $A/tools/t26-defs.py "$TMPDIR/pin.cpp" "$TMPDIR/base.cpp"; git -C "$W" log --oneline bccd715707.."$PIN" -- "$F" | wc -l'
run "the transitions" 'git -C "$W" grep -n "cloudSetupPresent(" "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr "\n" " "; echo; git -C "$W" grep -c "cloudSetupPresent(" "$PIN" -- "$F" | sed "s/^$PIN://"'
run "the reads of files other processes write" 'git -C "$W" grep -n -E "exists\(|isRegularFile\(" "$PIN" -- "$F" | sed "s/^$PIN://" | $G -c ", false)"; git -C "$W" grep -n -E "qrPath|isRegularFile\(" "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr "\n" " "; echo; git -C "$W" show "$PIN:$F" | sed -n "4154,4156p" | cut -c1-120'
run "the synchronous starts and the output reader" 'git -C "$W" grep -n -E "cloudRemoteLines\(|cloudRemoteBackends\(|cloudSetSystemsCommand\(|cloud_remote|cloud_setup|cloud_oauth" "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f2 | tr "\n" " "; echo; git -C "$W" grep -n "GetShOutput" "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f2 | tr "\n" " "; echo'
run "the dialogs, the chain, the quoting, the guards" 'git -C "$W" grep -n -E "CANCEL SIGN-IN|MANUAL UPDATES|backuptool|setrootpass|cloudShellQuote\(|want\.second\.c_str|_DEV_LOGIN" "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f2 | tr "\n" " "; echo; git -C "$W" show "$PIN:$F" | sed -n "5006p;6140p" | cut -c1-120'
run "the ten harnesses on the host" '( cd "$W" && for t in maintenance-why cloud-sync-last-run cloud-oauth-lifetime cloud-set-systems-quoting cloud-gated-row cloud-folder-reopen cloud-content-selection cloud-oauth-await credential-quoting gpu-governor-save; do out=$(timeout 600 python3 -I "tests/$t.py" 2>&1); rc=$?; printf "%s rc=%s: %s\n" "$t" "$rc" "$(printf "%s\n" "$out" | tail -n 1 | cut -c1-120)"; done )'
run "the menu map" 'out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf "%s\n" "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"'
run "the French" 'out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf "%s\n" "$out" | $G -m1 "fork string"; echo "es-untranslated rc=$rc"'
run "the non-ASCII comments" 'git -C "$W" show "$PIN:$F" | $G -c -P "^\s*//.*[^\x00-\x7F]"; rc=$?; echo "non-ascii grep rc=$rc"'
run "es-syntax-check" 'out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf "%s\n" "$out" | tail -n 1; echo "es-syntax-check rc=$rc"'
run "g++ -fsyntax-only" 'out=$(g++ -std=c++17 -fsyntax-only -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf "%s rc=%s\n" "$(printf "%s\n" "$out" | $G -m1 -E "fatal error|error:" | cut -c1-90)" "$rc"'
run "the builders (the greps; t26-rows.py is stage B)" 'for b in addSwitch addOptionList addInputTextConfigRow addFileBrowser addWithLabel addWithDescription addEntry addGroup addRow; do printf "%s %s\n" "$b" "$(git -C "$W" show "$PIN:$F" | $G -c -E "\b$b\(")"; done'
run "the credential rows, the writers, the page-open writes" 'git -C "$W" grep -n -E "addInputTextConfigRow\(|onFinalize|global\.videofilters|\.videofilter|led\.colour|warning_threshold|useFavoriteMusic|system\.timezone" "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f2 | tr "\n" " "; echo'
run "the keys both sides touch" 'git grep -n -E "set_setting (rocknix\.bottomscreen\.type|system\.automount|system\.merged\.device|system\.suspendmode)\b" "$C" -- projects/ROCKNIX/packages/rocknix/sources/scripts | sed "s/^$C://" | cut -d: -f1,2 | tr "\n" " "; echo; git grep -n -E "videofilter|led\.colou?r" "$C" -- projects/ROCKNIX/packages/rocknix/sources/scripts | sed "s/^$C://" | cut -d: -f1,2 | tr "\n" " " | cut -c1-300; echo'
run "the reboot flags and the sized pages" 'git -C "$W" grep -n -E "setVariable\(\"(reboot|exitreboot)\"|getVariable\(\"(reboot|exitreboot)\"" "$PIN" -- es-app/src | sed "s/^$PIN://" | cut -d: -f1,2 | tr "\n" " "; echo; git -C "$W" grep -n -E "getMenu\(\)\.(setSize|setPosition)|mMenu\.(setSize|setPosition)" "$PIN" -- es-app/src/guis | sed "s/^$PIN://" | cut -d: -f1,2 | tr "\n" " "; echo'
run "the structure (the greps; t26-structure.py is stage B)" 'git -C "$W" show "$PIN:$F" | $G -c -E "^\s*#\s*if"; git -C "$W" show "$PIN:$F" | $G -c "new GuiMsgBox"; git -C "$W" grep -n -E "FINISH RESTORE PROCESS|NO CLOUD STORAGE IS SET UP" "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr "\n" " "; echo'
run "the strings" 'git -C "$W" show "$PIN:$F" | $G -c "_(\""; git -C "$W" show "$PIN:$F" | $G -o -E "_\(\"[^\"]*\"\)" | sort -u | wc -l; python3 -I -B $A/tools/t26-french.py "$TMPDIR/pin.cpp" <(git -C "$W" show "$PIN:locale/lang/fr/LC_MESSAGES/emulationstation2.po") | tail -n 3'
run "the merge debt" 'git -C "$W" log --oneline bccd715707..rocknix/master -- "$F" | wc -l; git -C "$W" diff --numstat bccd715707 rocknix/master -- "$F"; git -C "$W" log --oneline bccd715707..rocknix/master -- "$F" | $G -c cada856d8; git -C "$W" show --stat cada856d8 -- "$F" | tail -n 1'
run "the removal check (the dispatch tip db7be4b104)" 'git diff --stat db7be4b104 HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1; echo end'

# Independent review, second packet: M6 T15, `tools/last-good-scripts-test` (#662)

This is the second call of the same review. It carries, in order:
- **the sections you asked for** under `## Sections I need`, at `8ebaf8daad`, line-numbered;
- **the two callee tools F-07 turns on,** `settings-modes-test` and `melonds-upgrade-test`, whole, at `8ebaf8daad` (this file's read hash) and at `7c1d729b57`. That is T14's fixed tip, accepted on 2026-10-24, whose S8 contract (a busybox must lie under a build root's `image/system/`, or be named by `--busybox-from`, or be marked `--unverified-busybox`) merges before this file's fixes;
- **your first reply,** whole;
- **the first packet,** whole, for reference.

**Please do this:**
1. Revisit each item you marked **cannot tell from the packet** (F-07, F-09, F-17, F-19, F-21) with these sections, giving one line each: `confirmed`, `confirmed with narrowing`, `refuted` or still `cannot tell`, why, and the lines. For F-07, say which revision's contract the finding holds against.
2. **F-08:** with `x/C`'s gate (`:4540-4565`) and `aa` in hand, does the availability gate establish the feature's retirement, or mistake a missing file for it? Does your refutation stand?
3. Add any further G-n findings these sections show.

Keep it to these items. Your earlier answers stand unless you change them here.


## Excerpt: F-08: x/C's applicability gate (`:4540-4565` at 8ebaf8daad)

```text
 4540  echo "  C. the cloud sign-in broker and setup (audit #307 stream C)"
 4541  CS="${TMP}/C"; mkdir -p "${CS}/src"
 4542  for rel in cloud_setup cloud_oauth cloud_remote cloud_device_id cloud_sync.conf; do
 4543      src_of "${RCLONE_REL}/${rel}" "${CS}/src/${rel}"
 4544  done
 4545  # #508 retires migration; historical sources retain their actual engine tests.
 4546  # An accidentally missing installed script remains a setup failure.
 4547  MIGRATION_AVAILABLE=0
 4548  if { [ "${OLD}" -eq 1 ] && git -C "${ROOT}" cat-file -e "${BASE_REF}:${RCLONE_REL}/cloud_migrate_layout" 2>/dev/null; } \
 4549      || { [ "${OLD}" -eq 0 ] && [ -e "${ROOT}/${RCLONE_REL}/cloud_migrate_layout" ]; }; then
 4550      src_of "${RCLONE_REL}/cloud_migrate_layout" "${CS}/src/cloud_migrate_layout"
 4551      MIGRATION_AVAILABLE=1
 4552  else
 4553      src_of projects/ROCKNIX/packages/network/rclone/package.mk "${CS}/src/rclone-package.mk"
 4554      if grep -qE '^[[:space:]]*cp[[:space:]]+cloud_migrate_layout([[:space:]]|$)' "${CS}/src/rclone-package.mk"; then
 4555          echo "cannot test selected source: recipe installs missing cloud_migrate_layout" >&2
 4556          exit 2
 4557      fi
 4558      NOT_APPLICABLE=$((NOT_APPLICABLE + 1))
 4559      echo "    NOT APPLICABLE  historical migration cases: selected source has no engine and its recipe does not install one (#508); no migration checks counted as PASS"
 4560  fi
 4561  # Select by the source contract, including a --old ref that already has it.
 4562  VALIDATOR_AVAILABLE=0; SEED_ARGS=()
 4563  if grep -q -- '--validate-folders)' "${CS}/src/cloud_setup"; then
 4564      [ -x "${CS}/src/cloud_folder_validate" ] || { echo "validator helper missing" >&2; exit 2; }
 4565      VALIDATOR_AVAILABLE=1; SEED_ARGS=(saves,settings,roms,bios)
```

## Excerpt: F-08: aa's head (`:13723-13740` at 8ebaf8daad)

```text
13723  echo "  aa. cloud_migrate_layout --state, --keep and --follow (#353, D-CLOUD-160/161): the layout as facts, a kept folder, the fleet followed"
13724  # The whole tool under bwrap against a shim rclone that answers by path and
13725  # by flag files: /GAMES or /ROCKNIX/Saves hold a save when the flag says so,
13726  # /pixelelated/Saves exists when another device has made it, the marker
13727  # answers when it is there. The conf is a real file under /storage, so
13728  # --keep and --follow are read back from what they wrote.
13729  LY="${TMP}/ly"; mkdir -p "${LY}/shim" "${LY}/rec" "${LY}/repo" "${LY}/storage/.config/rclone"
13730  printf '[qa]\ntype = alias\nremote = /cloud\n' > "${LY}/storage/.config/rclone/rclone.conf"
13731  src_of "projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout" "${LY}/repo/cloud_migrate_layout"
13732  printf 'export PATH=/shim:/usr/bin:/bin\n' > "${LY}/profile"
13733  printf '#!/bin/sh\necho "logger $*" >> /rec/log\n' > "${LY}/shim/logger"
13734  cat > "${LY}/shim/rclone" <<'EOR'
13735  #!/bin/sh
13736  printf '%s\n' "$*" >> /rec/argv
13737  cmd="$1"; shift
13738  path=""; for a in "$@"; do case "$a" in qa:*) path="$a";; esac; done
13739  case "$cmd" in
13740    listremotes) echo "qa:" ;;
```

## Excerpt: F-08: aa's tail (`:13890-13912` at 8ebaf8daad)

```text
13890  ly_run "$(ly_conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)
13891  LAYOUT_KEEP=\"/ROCKNIX/Saves\"" --needs-step; [ "${LYRC}" = 1 ]; check $? "--needs-step: nor an earlier folder the player kept (rc ${LYRC})" "$(ly_out)"
13892  : > "${LYRCONF}"
13893  ly_run "$(ly_conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)" --needs-step; [ "${LYRC}" = 1 ]; check $? "--needs-step: nor a device with no remote set up, whose way in is the setup wizard (rc ${LYRC})" "$(ly_out)"
13894  printf '[qa]\ntype = webdav\n' > "${LYRCONF}"
13895  ly_run 'SAVES_REMOTE="/ROCKNIX/Saves' --needs-step; [ "${LYRC}" = 2 ]; check $? "--needs-step: a conf it cannot read answers 2, which the interface takes as no step (rc ${LYRC})" "$(ly_out)"
13896  ly_run "$(ly_conf /rocknix/saves /rocknix/backups /rocknix/content)" --needs-step; [ "${LYRC}" = 1 ]; check $? "--needs-step: names compared as written: a hand-typed /rocknix/saves is not asked about at every boot, whatever the cloud folds (rc ${LYRC})" "$(ly_out)"
13897  rm -f "${LYRCONF}" "${LY}"/rec/*
13898  else
13899      echo "    aa. NOT APPLICABLE: historical layout facts/join/follow engine retired (#508)"
13900  fi
13901  
13902  # And no sync pays for the folder question any more: the check before every backup and restore
13903  # (D-CLOUD-160's follow, 147 ms on the current folder and 419 ms in transition) is the step's.
13904  for lyf in cloud_backup cloud_restore; do
13905      src_of "projects/ROCKNIX/packages/network/rclone/sources/${lyf}" "${LY}/${lyf}"
13906      # The follow and the layout's other network verbs; the --superseded list (a string test, no network)
13907      # is the one verb the backup may ask for (D-CLOUD-172).
13908      lyhit=$(grep -nE '^[^#]*(follow_layout|--(follow|join|settle|apply|state)\b)' "${LY}/${lyf}" || true)
13909      [ -z "${lyhit}" ]; check $? "${lyf} runs no folder check before its sync (D-CLOUD-170)" "${lyf}: $(echo "${lyhit}" | head -3 | tr '\n' '|' | cut -c1-200)"
13910  done
13911  
13912  
```

## Excerpt: F-09: x/F2 (`:3990-4015` at 8ebaf8daad)

```text
 3990  # S922X); the fork's own patches are held to fuzz 0 here, since a hunk that
 3991  # applies only by fuzz is one a reviewer applying the series strictly gets
 3992  # rejected (0017 needed a fuzz of 2 after 0016 was hand-edited to 13 px).
 3993  # The patched tree is then compiled syntax-only with the host's gcc, the
 3994  # widget font step is compiled on its own and asked which table each face
 3995  # gets, and the claims the audit found false are read from the patched
 3996  # source.
 3997  echo "  F2-4. RetroArch's patches: the fork's apply at fuzz 0, the tree compiles, the sharp-size table follows the face that is drawn (#307 PL-032; #308 F-RW-02..10)"
 3998  RA_REL=projects/ROCKNIX/packages/emulators/libretro/retroarch
 3999  RA_PIN="$(sed -n 's/^PKG_VERSION="\([0-9a-f]*\)".*/\1/p' "${ROOT}/${RA_REL}/package.mk" | head -1)"
 4000  RA_TAR=""
 4001  for d in "${SOURCES_DIR:-}" /workspace/cache/rocknix-sources "${ROOT}/sources" "${ROOT}"/../*/sources; do
 4002      [ -n "${d}" ] && [ -f "${d}/retroarch/retroarch-${RA_PIN}.tar.gz" ] && { RA_TAR="${d}/retroarch/retroarch-${RA_PIN}.tar.gz"; break; }
 4003  done
 4004  if [ -z "${RA_TAR}" ]; then
 4005      # A check that cannot run has not passed (the audit of the fixes, claude
 4006      # G-F2-10, gpt G-F2-06): with no pinned tree none of F2-4 runs, and the
 4007      # run says so as a FAIL rather than a SKIP an aggregate PASSED hides.
 4008      check 1 "" "retroarch-${RA_PIN:-?}.tar.gz is not under SOURCES_DIR, /workspace/cache/rocknix-sources or a build worktree's sources/ -- F2-4's eleven-plus checks did not run (an empty pin reads the same)"
 4009  else
 4010  RX="${F2}/ra"; mkdir -p "${RX}/patches/batteryplus" "${RX}/src"
 4011  if [ "${OLD}" -eq 1 ]; then
 4012      git -C "${ROOT}" ls-tree --name-only "${BASE_REF}" "${RA_REL}/patches/" "${RA_REL}/patches/batteryplus/" | grep '\.patch$' \
 4013        | while read -r f; do git -C "${ROOT}" show "${BASE_REF}:${f}" > "${RX}/patches/${f#${RA_REL}/patches/}"; done
 4014  else
 4015      cp "${ROOT}/${RA_REL}"/patches/*.patch "${RX}/patches/"; cp "${ROOT}/${RA_REL}"/patches/batteryplus/*.patch "${RX}/patches/batteryplus/"
```

## Excerpt: F-09: x/F2 (`:4290-4310` at 8ebaf8daad)

```text
 4290  echo "  F2-6. ppsspp-lr: the x86_64 strip of -mno-outline-atomics runs after the patches that add it (#308 F-EM-02)"
 4291  PP_PIN="$(sed -n 's/^PKG_VERSION="\([0-9a-f]*\)".*/\1/p' "${ROOT}/${F2P}/emulators/libretro/ppsspp-lr/package.mk" | head -1)"
 4292  PP_SRC=""
 4293  for d in "${SOURCES_DIR:-}" /workspace/cache/rocknix-sources "${ROOT}/sources" "${ROOT}"/../*/sources; do
 4294      [ -n "${d}" ] && [ -f "${d}/ppsspp-lr/ppsspp-lr-${PP_PIN}/CMakeLists.txt" ] && { PP_SRC="${d}/ppsspp-lr/ppsspp-lr-${PP_PIN}"; break; }
 4295  done
 4296  if [ -z "${PP_SRC}" ]; then
 4297      check 1 "" "the ppsspp-lr source ppsspp-lr-${PP_PIN:-?} is not under SOURCES_DIR, /workspace/cache/rocknix-sources or a build worktree's sources/ -- F2-6 did not run (a check that cannot run has not passed)"
 4298  else
 4299  PX="${F2}/ppsspp"; mkdir -p "${PX}/pkg/patches"
 4300  src_of "${F2P}/emulators/libretro/ppsspp-lr/package.mk" "${PX}/pkg/package.mk"
 4301  if [ "${OLD}" -eq 1 ]; then
 4302      git -C "${ROOT}" ls-tree --name-only "${BASE_REF}" "${F2P}/emulators/libretro/ppsspp-lr/patches/" | while read -r f; do git -C "${ROOT}" show "${BASE_REF}:${f}" > "${PX}/pkg/patches/${f##*/}"; done
 4303  else
 4304      cp "${ROOT}/${F2P}"/emulators/libretro/ppsspp-lr/patches/*.patch "${PX}/pkg/patches/"
 4305  fi
 4306  for arch in x86_64 aarch64; do
 4307      B="${PX}/build-${arch}"; rm -rf "${B}"
 4308      for f in CMakeLists.txt Common/ArmCPUDetect.cpp Core/Util/PathUtil.cpp ffmpeg/linux_arm64.sh libretro/libretro_vulkan.cpp ext/glew/glew.c; do
 4309          mkdir -p "$(dirname "${B}/${f}")"; cp "${PP_SRC}/${f}" "${B}/${f}"
 4310      done
```

## Excerpt: F-09: x/C (`:6475-6495` at 8ebaf8daad)

```text
 6475  
 6476  # Each of webkitgtk's patches says what it fixes before its first hunk --
 6477  # 0001 was a bare hunk (#308 claude F-RS-26) -- and every one still applies
 6478  # to the pinned release, dry, as scripts/unpack applies it: `patch` reads
 6479  # the prose before the first --- as a comment. The release's tarball comes
 6480  # from the sources cache; without it the dry run is skipped and says so.
 6481  WKP="${ROOT}/packages/web/webkitgtk/patches"
 6482  for wp in "${WKP}"/*.patch; do
 6483      [ -n "$(sed -n '/^--- /q; /[^[:space:]]/p' "${wp}")" ]; check $? "$(basename "${wp}") says what it fixes before its first hunk" "$(basename "${wp}") is a bare hunk: nothing says which build error it fixes, or why it is carried (#308 claude F-RS-26)"
 6484  done
 6485  WKV="$(sed -n 's/^PKG_VERSION="\(.*\)"$/\1/p' "${ROOT}/packages/web/webkitgtk/package.mk" | head -1)"
 6486  WKT=""
 6487  for d in "${SOURCES_DIR:-}" /workspace/cache/rocknix-sources "${ROOT}/sources" "${ROOT}"/../*/sources; do
 6488      [ -n "${d}" ] && [ -f "${d}/webkitgtk/webkitgtk-${WKV}.tar.xz" ] && { WKT="${d}/webkitgtk/webkitgtk-${WKV}.tar.xz"; break; }
 6489  done
 6490  if [ -z "${WKT}" ]; then
 6491      skip "webkitgtk-${WKV}.tar.xz is not under SOURCES_DIR, /workspace/cache/rocknix-sources or a build worktree's sources/ -- the patches' dry run needs the release they apply to"
 6492  else
 6493      WKD="${CS}/wk"; mkdir -p "${WKD}"
 6494      wkfiles=$(sed -n 's|^+++ b/\([^[:space:]]*\).*|webkitgtk-'"${WKV}"'/\1|p' "${WKP}"/*.patch | sort -u)
 6495      # shellcheck disable=SC2086
```

## Excerpt: F-09: x/D (DT_OK and its guarded branches) (`:6635-7795` at 8ebaf8daad)

```text
 6635  echo "  D. audit #307 stream D: the offline-achievements service -- the control script, its helpers, the client's patches, the unit and the emulators' cheevos scripts (#307 PL-013, 055, 057, 058, 059, 060; #308's sweep)"
 6636  # Each fix below was written after its case, and each case was seen to FAIL
 6637  # against the scripts from before it; to watch them fire again:
 6638  #
 6639  #     BASE_REF=417dcd8610 tools/last-good-scripts-test --old
 6640  #
 6641  # (417dcd8610 is next where stream D was cut.) The ctl's cases run in section
 6642  # t's sandbox -- its client from the sources cache with the patches applied,
 6643  # its shims, its virtual clock and fixture store -- and SKIP with it when the
 6644  # pinned client's tarball is not on this machine. The helpers' cases load the
 6645  # real helpers against the same patched client; the cheevos cases run the
 6646  # scripts whole with the image's busybox, like section w.
 6647  DD="${TMP}/stream-d"; mkdir -p "${DD}"
 6648  DT_OK=0
 6649  if declare -F tctl >/dev/null && [ -n "${CLIENT:-}" ] && [ -d "${CLIENT}/raofflineproxy" ]; then DT_OK=1; fi
 6650  DCFG_ON='system.hostname=X\nglobal.retroachievements=1\nglobal.retroachievements.offlineproxy=1\nglobal.retroachievements.username=QA\nglobal.retroachievements.token=FIXTURETOKEN\n'
 6651  # A run of the ctl in the background, as the interface starts one: stdout and
 6652  # stderr to ${DD}/bg.out and bg.err, the exit code to bg.rc when it ends.
 6653  dbg() { # <verb...>
 6654      rm -f "${DD}/bg.rc"
 6655      ( bwrap --die-with-parent --tmpfs / --tmpfs /usr "${USR_BINDS[@]}" "${TBB[@]}" \
 6656          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 6657          --ro-bind /etc /etc --ro-bind "${T}/profile" /etc/profile \
 6658          --bind "${TS}" /storage --ro-bind "${T}/repo" /repo --ro-bind "${T}/shim" /shim --ro-bind "${CLIENT}" /client --ro-bind "${T}/pypath" /pypath \
 6659          --bind "${TR}" /run --tmpfs /var --bind "${T}/varrun" /var/run \
 6660          --dev /dev --proc /proc --tmpfs /tmp --setenv PYTHONPATH /client:/pypath "${TENV[@]}" \
 6661          bash /repo/raofflineproxy-ctl "$@" > "${DD}/bg.out" 2> "${DD}/bg.err"; echo $? > "${DD}/bg.rc" ) &
 6662      DBG=$!
 6663  }
 6664  dnow() { date +%s.%N; }
 6665  dsince() { awk -v a="$1" -v b="$(dnow)" 'BEGIN{printf "%.2f", b - a}'; }
 6666  # A stand-in for raofflineproxy-cache-images beside the ctl, driven by
 6667  # /run/images-mode: "ok" (exit 0), "fail" (the helper's own failure lines,
 6668  # exit 1), "verify-left" (a verify slice left, no why, exit 3), "crash" (a
 6669  # traceback and Python's exit 1, no protocol line), "cancel" (the
 6670  # page's CANCEL: SIGINT to the ctl through the lock's pid, then a real 20 s),
 6671  # "group-cancel" (the interface's own CANCEL: SIGINT to the run's whole
 6672  # process group, then a real 20 s), "hang" (a real 20 s); every start is
 6673  # logged with its pid and a real time, and a SIGINT or SIGTERM it receives.
 6674  dfake_images() {
 6675      cat > "${T}/repo/raofflineproxy-cache-images" <<'EOS'
 6676  #!/bin/bash
 6677  echo $$ > /run/images.pid
 6678  echo "start $(date +%s.%N) budget=${FAKE_BUDGET:-none} $*" >> /run/images-calls
 6679  trap 'echo "term $(date +%s.%N)" >> /run/images-calls; exit 143' TERM
 6680  trap 'echo "int $(date +%s.%N)" >> /run/images-calls' INT
 6681  case "$(cat /run/images-mode 2>/dev/null || echo ok)" in
 6682      fail) printf '>>> doing images\n>>> total 3\n>>> why SOME_IMAGES_NOT_SAVED\n>>> done 0|3\n'; exit 1 ;;
 6683      verify-left) printf '>>> doing images\n>>> verified 10|40\n>>> note VERIFY_LEFT 30\n>>> total 0\n>>> note NOTHING_MISSING\n>>> done 0|0\n'; exit 3 ;;
 6684      crash) printf '>>> doing images\n'; echo 'Traceback (most recent call last):' >&2; exit 1 ;;
 6685      cancel) kill -INT "$(head -n 1 /var/run/raofflineproxy-scan.lock)"; i=0; while [ "$i" -lt 20 ]; do /bin/sleep 1; i=$((i+1)); done; echo "done $(date +%s.%N)" >> /run/images-calls; exit 0 ;;
 6686      group-cancel) kill -INT -- -"$(head -n 1 /var/run/raofflineproxy-scan.lock)"; i=0; while [ "$i" -lt 20 ]; do /bin/sleep 1; i=$((i+1)); done; echo "done $(date +%s.%N)" >> /run/images-calls; exit 0 ;;
 6687      hang) i=0; while [ "$i" -lt 20 ]; do /bin/sleep 1; i=$((i+1)); done; echo "done $(date +%s.%N)" >> /run/images-calls; exit 0 ;;
 6688  esac
 6689  printf '>>> doing images\n>>> total 0\n>>> note NOTHING_MISSING\n>>> done 0|0\n'
 6690  exit 0
 6691  EOS
 6692      chmod +x "${T}/repo/raofflineproxy-cache-images"
 6693  }
 6694  
 6695  # D1. #307 PL-013 (F-RA-01, claude): the page's CANCEL during the image pass
 6696  # ends the run inside two seconds. The helper: the interface signals the
 6697  # whole process group, the helper gets KeyboardInterrupt inside as_completed,
 6698  # and the pool's with-block used to wait for every queued download before the
 6699  # process could exit. Driven here on the real raofflineproxy-cache-images,
 6700  # against the patched client, with forty badges missing and each download a
 6701  # one-second sleep behind four workers: SIGINT once four have started.
 6702  # Also the helper started with SIGINT ignored (a shell's background job, as
 6703  # the ctl now starts it).
 6704  src_of "projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images" "${DD}/raofflineproxy-cache-images"
 6705  if [ "${DT_OK}" -eq 1 ]; then
 6706  python3 - "${DD}/raofflineproxy-cache-images" "${CLIENT}" "${DD}/images" > "${DD}/d1.out" 2>&1 <<'EOS'
 6707  import os, signal, subprocess, sys, time
 6708  from pathlib import Path
 6709  helper, client, work = sys.argv[1], sys.argv[2], Path(sys.argv[3])
 6710  cfg = work / "cfg"; site = work / "site"
 6711  for d in (cfg, site): d.mkdir(parents=True, exist_ok=True)
 6712  (site / "sitecustomize.py").write_text(
 6713      "import os, time\n"
 6714      "from pathlib import Path\n"
 6715      "import raofflineproxy.auth as _auth\n"
 6716      "_auth.resolve_credentials = lambda *a, **k: {'user': 'qa', 'token': 't'}\n"
 6717      "import raofflineproxy.image_cache as _ic\n"
 6718      "def _slow(url, path, ua, game_id=None):\n"
 6719      "    with open(os.environ['D_CALLS'], 'a') as f: f.write(path + '\\n')\n"
 6720      "    time.sleep(float(os.environ['D_EACH']))\n"
 6721      "_ic.download_static_image = _slow\n")
 6722  os.environ["RAOFFLINEPROXY_CONFIG_DIR"] = str(cfg)
 6723  sys.path.insert(0, client)
 6724  from raofflineproxy import cache_keys
 6725  from raofflineproxy.storage import Storage
 6726  st = Storage()
 6727  badges = [{"ID": 5000 + i, "Flags": 3, "BadgeURL": f"https://media.retroachievements.org/Badge/{9100 + i}.png"} for i in range(40)]
 6728  import json
 6729  st.upsert_cache(cache_keys.patch(1, "qa"), json.dumps({"Success": True, "PatchData": {"ID": 1, "Achievements": badges}}))
 6730  st.close()
 6731  def run(each, seconds, ignore_int, signal_after):
 6732      calls = work / "calls"; calls.write_text("")
 6733      env = dict(os.environ, PYTHONPATH=f"{site}:{client}", HOME=str(work), D_CALLS=str(calls), D_EACH=str(each))
 6734      pre = (lambda: signal.signal(signal.SIGINT, signal.SIG_IGN)) if ignore_int else None
 6735      p = subprocess.Popen([sys.executable, helper, "--seconds", str(seconds)], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=pre)
 6736      t0 = time.monotonic()
 6737      if signal_after:
 6738          while time.monotonic() - t0 < 10 and len(calls.read_text().split()) < signal_after:
 6739              time.sleep(0.05)
 6740          t0 = time.monotonic(); p.send_signal(signal.SIGINT)
 6741      try:
 6742          out, _ = p.communicate(timeout=20)
 6743      except subprocess.TimeoutExpired:
 6744          p.kill(); out, _ = p.communicate()
 6745      return p.returncode, time.monotonic() - t0, len(calls.read_text().split()), out.decode(errors="replace")
 6746  rc, took, started, out = run(1, 60, False, 4)
 6747  print(f"{'PASS' if rc not in (0, None) and took < 2.0 and started <= 8 and '>>> why CANCELLED' in out else 'FAIL'} cancel: SIGINT with 4 of 40 downloads started -- exit {rc} after {took:.2f}s, {started} started")
 6748  rc, took, started, out = run(1, 60, True, 4)
 6749  print(f"{'PASS' if rc not in (0, None) and took < 2.0 and started <= 8 else 'FAIL'} ignored: SIGINT to a helper started with SIGINT ignored -- exit {rc} after {took:.2f}s, {started} started")
 6750  EOS
 6751  grep -q '^PASS cancel:' "${DD}/d1.out"; check $? "PL-013 cache-images: the CANCEL's SIGINT drops the queued downloads and the helper ends inside two seconds ($(sed -n 's/^PASS cancel: //p' "${DD}/d1.out"))" "PL-013 cache-images: $(grep 'cancel:' "${DD}/d1.out" || tail -3 "${DD}/d1.out" | tr '\n' '|') -- the pool drained its queue before the interrupt was honoured"
 6752  grep -q '^PASS ignored:' "${DD}/d1.out"; check $? "PL-013 cache-images: started with SIGINT ignored (a background job), the group's SIGINT still ends it inside two seconds" "PL-013 cache-images: $(grep 'ignored:' "${DD}/d1.out" || echo 'no verdict') -- a background helper never heard the CANCEL"
 6753  # The ctl's side: the image pass ran in the foreground, so the INT trap (and
 6754  # disable's TERM, #308 gpt F-RA-11) waited for the helper to return. A scan
 6755  # that cached its games reaches the image pass; the stand-in sends the
 6756  # interface's SIGINT to the ctl and then works for a real 20 s.
 6757  dfake_images
 6758  printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 6759  treset; printf 'ok\nok\n' > "${TR}/helper-plan"; echo cancel > "${TR}/images-mode"; rm -f "${TR}/images-calls" "${TR}/images.pid"
 6760  DT0=$(dnow); tctl scan; DEND=$(dnow); DTOOK=$(awk -v a="${DT0}" -v b="${DEND}" 'BEGIN{printf "%.2f", b - a}')
 6761  IP="$(cat "${TR}/images.pid" 2>/dev/null)"; for _ in $(seq 1 30); do kill -0 "${IP:-1}" 2>/dev/null || break; sleep 0.1; done
 6762  [ "${RC}" -eq 130 ] && awk -v t="${DTOOK}" 'BEGIN{exit !(t < 12)}' && grep -qx '>>> why CANCELLED' "${OUT}" && grep -q ' 130 scan .*why=CANCELLED$' "${TSTAMP}" && ! grep -q '^done ' "${TR}/images-calls"; check $? "PL-013 ctl: CANCEL during a scan's image pass -- exit 130, why CANCELLED, stamped, the image helper ended (the whole scan ${DTOOK}s, jobs included)" "PL-013 ctl: rc ${RC} after ${DTOOK}s; out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | cut -c1-160); stamp: $(cat "${TSTAMP}" 2>/dev/null); helper: $(tr '\n' ' ' < "${TR}/images-calls" 2>/dev/null) -- the INT trap waited for the foreground image pass"
 6763  DI0="$(sed -n 's/^start \([0-9.]*\).*/\1/p' "${TR}/images-calls" 2>/dev/null | head -n 1)"
 6764  [ -n "${DI0}" ] && [ -n "${DEND}" ] && awk -v a="${DI0}" -v b="${DEND}" 'BEGIN{exit !(b - a < 2)}'; check $? "PL-013 ctl: from the image pass's start to the run's exit: $(awk -v a="${DI0:-0}" -v b="${DEND:-0}" 'BEGIN{printf "%.2f", b - a}')s, inside two seconds" "PL-013 ctl: the image pass started at ${DI0:-?} and the run exited at ${DEND:-?} -- $(awk -v a="${DI0:-0}" -v b="${DEND:-0}" 'BEGIN{printf "%.2f", b - a}')s"
 6765  ! kill -0 "${IP:-1}" 2>/dev/null && flock -n "${T}/varrun/raofflineproxy-scan.lock" true; check $? "PL-013 ctl: the cancelled run's image helper (pid ${IP:-?}) is gone and the lock is free" "PL-013 ctl: image helper alive: $(kill -0 "${IP:-1}" 2>/dev/null && echo yes || echo no); lock free: $(flock -n "${T}/varrun/raofflineproxy-scan.lock" true && echo yes || echo no)"
 6766  [ -n "${IP}" ] && kill -9 "${IP}" 2>/dev/null
 6767  # #308 1-raoffline gpt F-RA-11: disable during a scan's image pass ends the
 6768  # helper through the run's TERM trap within disable's own wait.
 6769  treset; rm -f "${TR}/fast-sleep"; printf 'ok\n' > "${TR}/helper-plan"; echo hang > "${TR}/images-mode"; rm -f "${TR}/images-calls" "${TR}/images.pid"
 6770  dbg scan
 6771  for _ in $(seq 1 100); do [ -s "${TR}/images.pid" ] && break; sleep 0.1; done
 6772  IP="$(cat "${TR}/images.pid" 2>/dev/null)"; sleep 0.3
 6773  DT0=$(dnow); tctl disable; DRC=${RC}; DTOOK=$(dsince "${DT0}")
 6774  GONE=0; for _ in $(seq 1 30); do kill -0 "${IP:-1}" 2>/dev/null || { GONE=1; break; }; sleep 0.1; done
 6775  wait "${DBG}" 2>/dev/null
 6776  [ "${DRC}" -eq 0 ] && [ -n "${IP}" ] && [ "${GONE}" -eq 1 ] && grep -q 'scan or top-up stopped' "${ERR}" && awk -v t="${DTOOK}" 'BEGIN{exit !(t < 5)}'; check $? "#308 gpt F-RA-11: disable during a scan's image pass -- the helper (pid ${IP:-?}) ended through the run's TERM trap, disable done in ${DTOOK}s (the scan exited $(cat "${DD}/bg.rc" 2>/dev/null))" "#308 gpt F-RA-11: disable rc ${DRC} after ${DTOOK}s; helper ${IP:-none} gone: ${GONE}; disable said: $(grep -i 'asking\|stop' "${ERR}" | tr '\n' '|' | cut -c1-200) -- the TERM waited for the foreground image pass"
 6777  [ -n "${IP}" ] && kill -9 "${IP}" 2>/dev/null; touch "${TR}/fast-sleep"; rm -f "${TR}/images-mode" "${TR}/helper-plan"
 6778  printf "${DCFG_ON}" > "${TCFG}"
 6779  else
 6780      skip "PL-013's cases: section t did not run (the pinned client is not on this machine)"
 6781  fi
 6782  
 6783  # D2. #307 PL-055 (F-RA-02 gpt = F-RA-03 claude): index-pending, the promise
 6784  # that the link's return lists the library once for an index that ran
 6785  # offline, is kept until that listing and its games have been handled: a
 6786  # listing that fails (an error, or the deadline), a run stopped part-way and a
 6787  # game whose fetch failed all leave it; only a run whose indexed pass ended
 6788  # with nothing wrong removes it. A marker that survives a failed attempt waits
 6789  # out the half hour like any other run (it bypasses the interval only when it
 6790  # was written after the last attempt), so a flapping link does not turn it
 6791  # into a request storm.
 6792  if [ "${DT_OK}" -eq 1 ]; then
 6793  # The listing fails on demand: /run/listing-fail holds the exit code.
 6794  grep -q 'listing-fail' "${T}/shim/python3" || sed -i 's|^if \[ "\$1" = "-" \] && \[ -s /run/listing-delay \]|if [ "$1" = "-" ] \&\& [ -s /run/listing-fail ]; then exit "$(cat /run/listing-fail)"; fi\n&|' "${T}/shim/python3"
 6795  grep -q 'listing-fail' "${T}/shim/python3"; check $? "the python3 shim fails a listing on demand (/run/listing-fail)" "the shim edit did not take: $(grep -n 'listing' "${T}/shim/python3" | tr '\n' '|')"
 6796  TENV=(--setenv RAOFFLINEPROXY_HISTORY /storage/.config/retroarch/content_history.lpl)
 6797  dpending() { # the marker, the mark two hours old, no game played since
 6798      treset; touch -d '3 hours ago' "${THISTORY}"; touch -d '2 hours ago' "${TMARK}"
 6799      tctl index-offline; : > "${TR}/probe.log"; : > "${TR}/helper-jobs.log"; : > "${TLOG}"
 6800  }
 6801  dpending; echo 1 > "${TR}/listing-fail"
 6802  tctl topup; rm -f "${TR}/listing-fail"
 6803  [ "${RC}" -eq 1 ] && grep -q "index could not be read" "${TLOG}" && grep -q 'why=LIBRARY_UNREADABLE$' "${TSTAMP}" && grep -q '^smart budget=' "${TR}/probe.log" && [ -e "${TPD}/index-pending" ]; check $? "PL-055: a link-return listing for the marker that fails (rc 1) leaves index-pending; the run still does the recently played pass and ends COULDN'T FINISH, why LIBRARY_UNREADABLE (claude G-D-13) (rc ${RC})" "PL-055 / claude G-D-13: rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null); marker: $([ -e "${TPD}/index-pending" ] && echo kept || echo gone); log: $(tr '\n' '|' < "${TLOG}" | cut -c1-200) -- a listing that failed was stamped COMPLETED, or the marker went"
 6804  dpending; echo 124 > "${TR}/listing-fail"
 6805  tctl topup; rm -f "${TR}/listing-fail"
 6806  [ "${RC}" -eq 1 ] && grep -q 'why=TOOK_TOO_LONG$' "${TSTAMP}" && [ -e "${TPD}/index-pending" ]; check $? "PL-055: a listing cut by the deadline (124): TOOK_TOO_LONG, index-pending kept" "PL-055: rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null); marker: $([ -e "${TPD}/index-pending" ] && echo kept || echo gone)"
 6807  # The same link flapping a minute later: the marker is older than the attempt
 6808  # the failed run made, so the half hour holds -- no probe, no listing.
 6809  # (On the virtual clock: the failed attempt a minute ago, the marker written before it.)
 6810  touch -d "@$(( $(cat "${TR}/clock") - 60 ))" "${TMARK}"; [ -e "${TPD}/index-pending" ] && touch -d "@$(( $(cat "${TR}/clock") - 120 ))" "${TPD}/index-pending"
 6811  : > "${TR}/probe.log"; : > "${TLOG}"
 6812  tctl topup
 6813  [ "${RC}" -eq 0 ] && [ ! -s "${TR}/probe.log" ] && ! grep -q 'listed once' "${TLOG}" && [ -e "${TPD}/index-pending" ]; check $? "PL-055: the next link event inside the half hour after a failed attempt waits (no probe, no listing), the marker still there" "PL-055: rc ${RC}; probes: $(grep -c . "${TR}/probe.log"); log: $(tr '\n' '|' < "${TLOG}" | cut -c1-200); marker: $([ -e "${TPD}/index-pending" ] && echo kept || echo gone)"
 6814  # Past the half hour it lists again, and a run that handled the games clears it.
 6815  touch -d "@$(( $(cat "${TR}/clock") - 3600 ))" "${TMARK}"; : > "${TLOG}"
 6816  tctl topup
 6817  [ "${RC}" -eq 0 ] && grep -q 'listed once' "${TLOG}" && grep -q 'topup start: found=3 new=2' "${TLOG}" && [ ! -e "${TPD}/index-pending" ]; check $? "PL-055: past the half hour the marker's listing runs again, caches the games and removes the marker" "PL-055: rc ${RC}; log: $(tr '\n' '|' < "${TLOG}" | cut -c1-240); marker: $([ -e "${TPD}/index-pending" ] && echo kept || echo gone)"
 6818  # A game whose fetch failed in the marker's pass: SOME_GAMES_NOT_SAVED, kept.
 6819  dpending; printf 'fail\nok\n' > "${TR}/helper-plan"
 6820  tctl topup; rm -f "${TR}/helper-plan"
 6821  [ "${RC}" -eq 1 ] && grep -q 'why=SOME_GAMES_NOT_SAVED$' "${TSTAMP}" && [ -e "${TPD}/index-pending" ]; check $? "PL-055: a failed game in the marker's pass: SOME_GAMES_NOT_SAVED, index-pending kept" "PL-055: rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null); marker: $([ -e "${TPD}/index-pending" ] && echo kept || echo gone)"
 6822  # A run stopped part-way (STOP IT AND PLAY, disable: SIGTERM to the pid in
 6823  # the lock) keeps it too.
 6824  dpending; rm -f "${TR}/fast-sleep"; printf 'wait 20\n' > "${TR}/helper-plan"; rm -f "${TR}/helper.pid"
 6825  dbg topup
 6826  for _ in $(seq 1 100); do [ -s "${TR}/helper.pid" ] && break; sleep 0.1; done; sleep 0.3
 6827  DHP="$(cat "${TR}/helper.pid" 2>/dev/null)"
 6828  kill -TERM "$(head -n 1 "${T}/varrun/raofflineproxy-scan.lock" 2>/dev/null)" 2>/dev/null
 6829  for _ in $(seq 1 100); do [ -s "${DD}/bg.rc" ] && break; sleep 0.1; done
 6830  wait "${DBG}" 2>/dev/null
 6831  [ "$(cat "${DD}/bg.rc" 2>/dev/null)" = "143" ] && [ -e "${TPD}/index-pending" ]; check $? "PL-055: a marker's run stopped part-way (TERM, exit 143) keeps index-pending" "PL-055: the run exited $(cat "${DD}/bg.rc" 2>/dev/null); marker: $([ -e "${TPD}/index-pending" ] && echo kept || echo gone)"
 6832  [ -n "${DHP}" ] && kill -9 "${DHP}" 2>/dev/null; touch "${TR}/fast-sleep"; rm -f "${TR}/helper-plan"
 6833  else
 6834      skip "PL-055's cases: section t did not run"
 6835  fi
 6836  
 6837  # D3. #307 PL-057 (F-RA-04/05 gpt): the summary lists a game cached by a
 6838  # launch alone -- an achievementsets row and no patch row -- from that row's
 6839  # core set, once; and a game whose unlock row is missing or cannot be read
 6840  # says its unlocks are unknown (null), never that nothing was earned.
 6841  # (The store also holds the waiting awards 03b reads, and D18 runs the
 6842  # ctl's other reads on a store the same client wrote.)
 6843  if [ "${DT_OK}" -eq 1 ]; then
 6844  TENV=(); printf "${DCFG_ON}" > "${TCFG}"
 6845  treset; PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
 6846  import json
 6847  from raofflineproxy import cache_keys
 6848  from raofflineproxy.storage import Storage
 6849  s = Storage()
 6850  core = lambda *pairs: [{"ID": i, "Title": f"a{i}", "Points": p, "Flags": 3} for i, p in pairs]
 6851  # 201: a launch's rows only (RetroArch asked achievementsets, never patch).
 6852  s.upsert_cache(cache_keys.achievementsets("aaaa0201", "qa"), json.dumps({"Success": True, "GameId": 201, "Title": "Sets Only", "ImageIconUrl": "https://media.retroachievements.org/Images/000201.png",
 6853      "Sets": [{"Type": "bonus", "Achievements": core((3901, 50))}, {"Type": "core", "Achievements": core((3001, 5), (3002, 10)) + [{"ID": 3003, "Points": 25, "Flags": 5}]}]}))
 6854  s.upsert_cache(cache_keys.unlocks(201, "qa"), json.dumps({"Success": True, "UserUnlocks": [3001]}))
 6855  # 202: a patch row whose unlock row is damaged; 203: a patch row with no unlock row.
 6856  s.upsert_cache(cache_keys.patch(202, "qa"), json.dumps({"Success": True, "PatchData": {"ID": 202, "Title": "Bad Unlocks", "Achievements": core((3101, 5), (3102, 5))}}))
 6857  s.upsert_cache(cache_keys.unlocks(202, "qa"), "{not json")
 6858  s.upsert_cache(cache_keys.patch(203, "qa"), json.dumps({"Success": True, "PatchData": {"ID": 203, "Title": "No Unlocks", "Achievements": core((3201, 5))}}))
 6859  # 204: another account's launch rows; 102: a patch row and a sets row, listed once.
 6860  s.upsert_cache(cache_keys.achievementsets("dddd0204", "other"), json.dumps({"Success": True, "GameId": 204, "Title": "Theirs", "Sets": [{"Type": "core", "Achievements": core((3301, 5))}]}))
 6861  s.upsert_cache(cache_keys.patch(102, "qa"), json.dumps({"Success": True, "PatchData": {"ID": 102, "Title": "Bee", "ImageIcon": "/Images/000102.png", "Achievements": core((1001, 5), (1002, 10))}}))
 6862  s.upsert_cache(cache_keys.unlocks(102, "qa"), json.dumps({"Success": True, "UserUnlocks": [1001]}))
 6863  s.upsert_cache(cache_keys.achievementsets("bbbb", "qa"), json.dumps({"Success": True, "GameId": 102, "Title": "Bee", "Sets": [{"Type": "core", "Achievements": core((1001, 5), (1002, 10))}]}))
 6864  # Waiting awards: 1002 earned by another account on this device, 3002 by qa.
 6865  now = 1789400000000
 6866  s.upsert_pending_award({"achievementId": 1002, "queryString": "/dorequest.php?r=awardachievement&u=Other&a=1002&h=0", "requestBody": "", "userAgent": "ra", "queuedAt": now})
 6867  s.upsert_pending_award({"achievementId": 3002, "queryString": "/dorequest.php", "requestBody": "r=awardachievement&u=QA&t=x&a=3002&h=0", "userAgent": "ra", "queuedAt": now + 1000})
 6868  s.close()
 6869  EOS
 6870  tctl summary; cp "${OUT}" "${DD}/summary.out"
 6871  grep -qx '{"id":201,"title":"Sets Only","icon":"http://127.0.0.1:8080/Images/000201.png","achievements":2,"points":15,"unlocked":2,"unlockedPoints":15,"pending":1}' "${DD}/summary.out"; check $? "PL-057 summary: a game cached by a launch alone (achievementsets row, no patch row) is listed from its core set -- 2 achievements, 15 points, both unlocked (one earned, one waiting to be sent)" "PL-057 summary: rc ${RC}; no line for game 201: $(tr '\n' '|' < "${DD}/summary.out" | cut -c1-400) -- the summary read patch rows only"
 6872  grep -q '"id":202,.*"unlocked":null,"unlockedPoints":null' "${DD}/summary.out" && grep -q '"id":203,.*"unlocked":null,"unlockedPoints":null' "${DD}/summary.out"; check $? "PL-057 summary: a damaged unlock row (202) and a missing one (203) read unlocked null -- unknown, not none" "PL-057 summary: $(grep -E '"id":20[23],' "${DD}/summary.out" | tr '\n' '|' | cut -c1-300) -- an unreadable unlock row read as nothing earned"
 6873  [ "$(grep -c '"id":102,' "${DD}/summary.out")" -eq 1 ] && ! grep -q '"id":204,' "${DD}/summary.out"; check $? "PL-057 summary: a game with both rows is listed once; another account's launch rows are not listed" "PL-057 summary: 102 x$(grep -c '"id":102,' "${DD}/summary.out"), 204 x$(grep -c '"id":204,' "${DD}/summary.out")"
 6874  else
 6875      skip "PL-057's cases: section t did not run"
 6876  fi
 6877  
 6878  # D3b. #308 1-raoffline gpt F-RA-09: a waiting award is counted for the account
 6879  # that earned it -- its request's u=, in the query or the body -- and not for
 6880  # whoever is signed in now, in the summary and in pending-ids alike; an
 6881  # award whose request names no account is counted as before. D3's store:
 6882  # 1002 earned by "Other" on this device, 3002 by "QA".
 6883  if [ "${DT_OK}" -eq 1 ]; then
 6884  grep -qx '{"id":102,"title":"Bee","icon":"http://127.0.0.1:8080/Images/000102.png","achievements":2,"points":15,"unlocked":1,"unlockedPoints":5,"pending":0}' "${DD}/summary.out"; check $? "#308 gpt F-RA-09 summary: another account's waiting award (1002, u=Other) is not counted as this account's -- 102 reads 1 unlocked, none waiting" "#308 gpt F-RA-09: $(grep '"id":102,' "${DD}/summary.out") -- the queue was merged into whoever is signed in"
 6885  tctl pending-ids
 6886  [ "${RC}" -eq 0 ] && [ "$(cat "${OUT}")" = "3002 1789400001" ]; check $? "#308 gpt F-RA-09 pending-ids: only this account's waiting award (3002, u=QA in the body), not the other account's 1002" "#308 gpt F-RA-09 pending-ids: rc ${RC}; out: $(tr '\n' '|' < "${OUT}")"
 6887  tctl pending
 6888  [ "${RC}" -eq 0 ] && [ "$(cat "${OUT}")" = "2" ]; check $? "pending still counts every award the queue holds for sending (2): the service sends each with its own account" "pending: rc ${RC}; out: $(tr '\n' '|' < "${OUT}")"
 6889  else
 6890      skip "#308 F-RA-09's cases: section t did not run"
 6891  fi
 6892  
 6893  # D4. #307 PL-058 (F-RA-06 gpt): raofflineproxy-refresh counts a game whose
 6894  # startsession row could not be dropped as failed -- the row carries the
 6895  # unlocks a launch reads, so a refresh that could not remove it did not do
 6896  # its job. The real helper, loaded against the patched client, its network
 6897  # calls replaced (the driver also runs 04b's two cases).
 6898  src_of "projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh" "${DD}/raofflineproxy-refresh"
 6899  if [ "${DT_OK}" -eq 1 ]; then
 6900  RAOFFLINEPROXY_CONFIG_DIR="${DD}/refresh-cfg" PYTHONPATH="${CLIENT}" python3 - "${DD}/raofflineproxy-refresh" > "${DD}/d4.out" 2>&1 <<'EOS'
 6901  import contextlib, io, os, sys, importlib.machinery, importlib.util
 6902  from pathlib import Path
 6903  Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
 6904  spec = importlib.util.spec_from_loader("refresh_helper", importlib.machinery.SourceFileLoader("refresh_helper", sys.argv[1]))
 6905  helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
 6906  from raofflineproxy import cache_keys
 6907  from raofflineproxy.storage import Storage
 6908  helper.resolve_credentials = lambda *a, **k: {"user": "qa", "token": "t"}
 6909  fails = set()
 6910  def fake_patch(gid, *a, **k):
 6911      if gid in fails: raise RuntimeError(f"patch request failed for {gid}")
 6912      return '{"PatchData":{"Title":"G%d"}}' % gid
 6913  helper.proxy_service.refresh_game_patch = fake_patch
 6914  helper.proxy_service.cache_unlocks = lambda *a, **k: None
 6915  def run(args):
 6916      sys.argv = ["raofflineproxy-refresh"] + args
 6917      buf = io.StringIO()
 6918      with contextlib.redirect_stdout(buf):
 6919          rc = helper.main()
 6920      return rc, buf.getvalue()
 6921  st = Storage()
 6922  # The client lists patch rows newest first (ORDER BY cachedAt DESC), so each
 6923  # row gets its own time: game 1 the newest, the order 1..6 whatever the clock
 6924  # does between inserts.
 6925  for gid in range(1, 7):
 6926      st.upsert_cache(cache_keys.patch(gid, "qa"), '{"Success":true,"PatchData":{"ID":%d}}' % gid, cached_at=1789400000000 - gid * 1000)
 6927  st.upsert_cache(cache_keys.start_session(5, "qa"), '{"Success":true,"Unlocks":[1]}')
 6928  st.close()
 6929  # The drop fails: the store refuses the delete.
 6930  real_delete = Storage.delete_cache
 6931  def refusing(self, key):
 6932      raise OSError("disk I/O error")
 6933  Storage.delete_cache = refusing
 6934  rc, out = run(["--game", "5", "--seconds", "30"])
 6935  Storage.delete_cache = real_delete
 6936  ok = rc == 1 and "re-read 0 game(s), 1 failed" in out and ">>> done 0|1" in out
 6937  print(("PASS" if ok else "FAIL") + f" drop: rc {rc}; " + " | ".join(l for l in out.splitlines() if "re-read" in l or l.startswith(">>> done") or "startsession" in l))
 6938  # Three failures, never two in a row: every game is tried.
 6939  fails.clear(); fails.update({1, 3, 5})
 6940  rc, out = run(["--all", "--seconds", "30"])
 6941  ok = rc == 1 and "re-read 3 game(s), 3 failed" in out and "REPEATED_FAILURES" not in out
 6942  print(("PASS" if ok else "FAIL") + f" apart: rc {rc}; " + " | ".join(l for l in out.splitlines() if "re-read" in l and "game(s)" in l or "REPEATED" in l or "in a row" in l))
 6943  # Three in a row: it stops.
 6944  fails.clear(); fails.update({2, 3, 4})
 6945  rc, out = run(["--all", "--seconds", "30"])
 6946  ok = rc == 1 and "REPEATED_FAILURES" in out and "re-read 5/6" not in out and "re-read 6/6" not in out
 6947  print(("PASS" if ok else "FAIL") + f" row: rc {rc}; " + " | ".join(l for l in out.splitlines() if "REPEATED" in l or "in a row" in l or l.startswith(">>> done")))
 6948  EOS
 6949  grep -q '^PASS drop:' "${DD}/d4.out"; check $? "PL-058 refresh: a startsession row that could not be dropped makes the game failed -- re-read 0 game(s), 1 failed, exit 1" "PL-058 refresh: $(grep 'drop:' "${DD}/d4.out" || tail -3 "${DD}/d4.out" | tr '\n' '|') -- a failed drop was reported as a game re-read"
 6950  else
 6951      skip "PL-058's cases: section t did not run"
 6952  fi
 6953  
 6954  # D4b. #308 1-raoffline claude F-RA-12 = gpt F-RA-19: raofflineproxy-refresh
 6955  # stops after three failures in a row, as it says, not after three in all
 6956  # (D4's driver: games 1, 3 and 5 failing, then 2, 3 and 4).
 6957  if [ "${DT_OK}" -eq 1 ]; then
 6958  grep -q '^PASS apart:' "${DD}/d4.out"; check $? "#308 claude F-RA-12 / gpt F-RA-19 refresh: three failures never two in a row -- every game tried (3 re-read, 3 failed)" "#308 F-RA-12/19 refresh: $(grep 'apart:' "${DD}/d4.out" || echo 'no verdict') -- three failures in all were read as three in a row"
 6959  grep -q '^PASS row:' "${DD}/d4.out"; check $? "#308 claude F-RA-12 / gpt F-RA-19 refresh: three failures in a row stop the run (REPEATED_FAILURES)" "#308 F-RA-12/19 refresh: $(grep 'row:' "${DD}/d4.out" || echo 'no verdict')"
 6960  else
 6961      skip "#308 F-RA-12/19's cases: section t did not run"
 6962  fi
 6963  
 6964  # D5. #307 PL-059 (F-RA-07 gpt): the walk over unindexed folders keeps a
 6965  # cursor between runs, so files that never cache (a ROM RetroAchievements does
 6966  # not know is skipped, and stays uncached) cannot hold the front of the walk
 6967  # for ever; and a walk cut at the cap says so to the page (note TRUNCATED)
 6968  # and in the stamp (truncated=1). The cap is lowered to ten, as in t's PL-17
 6969  # case, over thirteen files nobody can cache (gb's two and gbc's eleven): the
 6970  # second scan reaches the ones the first did not, the thirteenth included.
 6971  if [ "${DT_OK}" -eq 1 ]; then
 6972  printf "${DCFG_ON}" > "${TCFG}"
 6973  treset; rm -rf "${TS}/roms/gbc"; mkdir -p "${TS}/roms/gbc"; for i in $(seq -w 1 11); do printf 'GBC %s' "${i}" > "${TS}/roms/gbc/g${i}.gbc"; done
 6974  TENV=(--setenv RA_TEST_SCAN_CAP 10)
 6975  for _ in $(seq 1 20); do echo skip; done > "${TR}/helper-plan"
 6976  : > "${TR}/helper-jobs.log"
 6977  tctl scan; cp "${OUT}" "${DD}/scan1.out"; cp "${TR}/helper-jobs.log" "${DD}/scan1.jobs"
 6978  [ "${RC}" -eq 0 ] && grep -qx '>>> note TRUNCATED' "${DD}/scan1.out" && grep -q ' 0 scan .* truncated=1' "${TSTAMP}"; check $? "PL-059: a walk cut at the cap tells the page (note TRUNCATED) and the stamp (truncated=1)" "PL-059: rc ${RC}; out: $(grep '^>>>' "${DD}/scan1.out" | tr '\n' '|' | cut -c1-200); stamp: $(cat "${TSTAMP}" 2>/dev/null) -- the truncation was in the log alone"
 6979  : > "${TR}/helper-jobs.log"
 6980  tctl scan; cp "${TR}/helper-jobs.log" "${DD}/scan2.jobs"
 6981  grep -qP '^H\t\t\t/storage/roms/gbc/g11.gbc$' "${DD}/scan2.jobs" && grep -qP '^H\t\t\t/storage/roms/gbc/g09.gbc$' "${DD}/scan2.jobs"; check $? "PL-059: the second scan walks on from where the first stopped -- g09, g10 and g11, none of which can be cached, are its jobs" "PL-059: second scan's jobs: $(sed 's|.*/||' "${DD}/scan2.jobs" | tr '\n' ' ') -- the same first ten files held the front of the walk"
 6982  [ "$(sort "${DD}/scan1.jobs" "${DD}/scan2.jobs" | uniq | grep -c "^H")" -eq 13 ]; check $? "PL-059: two scans together have tried all thirteen uncacheable files" "PL-059: $(sort "${DD}/scan1.jobs" "${DD}/scan2.jobs" | uniq | grep -c "^H") distinct files over two scans"
 6983  # Under the cap the walk comes round whole: no note, no cursor left behind.
 6984  rm -f "${TS}"/roms/gbc/g0[1-9].gbc; : > "${TR}/helper-jobs.log"
 6985  tctl scan
 6986  [ "${RC}" -eq 0 ] && ! grep -q 'note TRUNCATED' "${OUT}" && ! grep -q 'truncated=1' "${TSTAMP}" && [ ! -e "${TPD}/scan-cursor" ]; check $? "PL-059: a walk that fits under the cap says nothing of truncation and leaves no cursor" "PL-059: rc ${RC}; out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | cut -c1-160); stamp: $(cat "${TSTAMP}" 2>/dev/null); cursor: $(cat "${TPD}/scan-cursor" 2>/dev/null || echo none)"
 6987  TENV=(); rm -rf "${TS}/roms/gbc"; rm -f "${TR}/helper-plan"
 6988  else
 6989      skip "PL-059's cases: section t did not run"
 6990  fi
 6991  
 6992  # D6. #307 PL-060 (F-RA-08 gpt): the image pass is part of the scan and the
 6993  # top-up (D-RA-027: a game whose badges are missing offline reads as half
 6994  # working), so a pass that left images behind makes the run COULDN'T FINISH
 6995  # with its why (SOME_IMAGES_NOT_SAVED, D-UI-030) -- and a scan with no new
 6996  # game still runs it, so pressing SCAN again repairs what the last pass left.
 6997  # A verify slice the pass did not finish (exit 3, since 06b) is the sweep
 6998  # working through the store a slice a run, by design (D-RA-024), not a failure.
 6999  if [ "${DT_OK}" -eq 1 ]; then
 7000  dfake_images; printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7001  treset; printf 'ok\nok\n' > "${TR}/helper-plan"; echo fail > "${TR}/images-mode"; rm -f "${TR}/images-calls"
 7002  tctl scan
 7003  [ "${RC}" -eq 1 ] && grep -qx '>>> why SOME_IMAGES_NOT_SAVED' "${OUT}" && grep -q ' 1 scan cached=4 .*why=SOME_IMAGES_NOT_SAVED$' "${TSTAMP}" && grep -qE '^>>> done 4\|' "${OUT}"; check $? "PL-060: a scan that cached its games and whose image pass left images behind ends COULDN'T FINISH (rc 1, why SOME_IMAGES_NOT_SAVED), the games still counted" "PL-060: rc ${RC}; out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | cut -c1-200); stamp: $(cat "${TSTAMP}" 2>/dev/null) -- the image pass's failure was dropped"
 7004  rm -f "${TR}/helper-plan" "${TR}/images-calls"
 7005  tctl scan
 7006  [ "${RC}" -eq 1 ] && grep -qx '>>> note NOTHING_NEW' "${OUT}" && grep -qx '>>> why SOME_IMAGES_NOT_SAVED' "${OUT}" && [ -s "${TR}/images-calls" ]; check $? "PL-060: a scan with nothing new still runs the image pass, and its failure is the run's (rc 1, why SOME_IMAGES_NOT_SAVED)" "PL-060: rc ${RC}; image pass run: $(grep -c '^start' "${TR}/images-calls" 2>/dev/null || echo 0) time(s); out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | cut -c1-200) -- the nothing-new branch exited before the pass"
 7007  echo ok > "${TR}/images-mode"; rm -f "${TR}/images-calls"
 7008  tctl scan
 7009  [ "${RC}" -eq 0 ] && grep -qx '>>> note NOTHING_NEW' "${OUT}" && [ -s "${TR}/images-calls" ] && grep -q ' 0 scan cached=0 ' "${TSTAMP}"; check $? "PL-060: and once the pass fetches what was missing, the same scan reads COMPLETED with nothing new (rc 0)" "PL-060: rc ${RC}; image pass run: $(grep -c '^start' "${TR}/images-calls" 2>/dev/null || echo 0); stamp: $(cat "${TSTAMP}" 2>/dev/null)"
 7010  # The top-up: a failed pass is the run's too; a verify slice left is not.
 7011  treset; touch -d '2 hours ago' "${TMARK}"; echo fail > "${TR}/images-mode"
 7012  tctl topup --after-index
 7013  [ "${RC}" -eq 1 ] && grep -q ' 1 topup cached=2 .*why=SOME_IMAGES_NOT_SAVED$' "${TSTAMP}"; check $? "PL-060: a top-up whose image pass left images behind ends rc 1, why SOME_IMAGES_NOT_SAVED" "PL-060: rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null)"
 7014  treset; touch -d '2 hours ago' "${TMARK}"; echo verify-left > "${TR}/images-mode"
 7015  tctl topup --after-index
 7016  [ "${RC}" -eq 0 ] && grep -q ' 0 topup cached=2 ' "${TSTAMP}" && ! grep -q 'why=' "${TSTAMP}"; check $? "PL-060: a top-up whose verify slice did not come round the store (the helper's exit 3) finished (rc 0) -- the sweep takes several runs by design" "PL-060: rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null)"
 7017  rm -f "${TR}/images-mode" "${TR}/images-calls"
 7018  else
 7019      skip "PL-060's cases: section t did not run"
 7020  fi
 7021  
 7022  # D6b. Found while fixing PL-060: the image helper said "a verify slice is
 7023  # left" with exit 1 and no why line -- and exit 1 with no why is also what
 7024  # Python gives a helper that dies of an uncaught exception, so a crash
 7025  # would have read as the sweep working and the run as COMPLETED. The helper
 7026  # now says a verify slice left with exit 3 (D-RA-024's "exits non-zero"
 7027  # still holds), and every other failure -- a crash included -- is images
 7028  # left behind.
 7029  if [ "${DT_OK}" -eq 1 ]; then
 7030  dfake_images; printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7031  treset; touch -d '2 hours ago' "${TMARK}"; echo crash > "${TR}/images-mode"
 7032  tctl topup --after-index
 7033  [ "${RC}" -eq 1 ] && grep -q ' 1 topup cached=2 .*why=SOME_IMAGES_NOT_SAVED$' "${TSTAMP}"; check $? "a top-up whose image helper crashed (a traceback, exit 1, no protocol line) ends rc 1, why SOME_IMAGES_NOT_SAVED -- not read as a verify slice left" "rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null) -- a crash read as the sweep working"
 7034  rm -f "${TR}/images-mode"
 7035  else
 7036      skip "the verify exit cases: section t did not run"
 7037  fi
 7038  # The helper itself: a verify pass that stops at its half of the budget
 7039  # with files left to verify and nothing missing exits 3, and says so.
 7040  if [ "${DT_OK}" -eq 1 ]; then
 7041  python3 - "${DD}/raofflineproxy-cache-images" "${CLIENT}" "${DD}/images" > "${DD}/d6b.out" 2>&1 <<'EOS'
 7042  import os, subprocess, sys, time
 7043  from pathlib import Path
 7044  helper, client, work = sys.argv[1], sys.argv[2], Path(sys.argv[3])
 7045  cfg = work / "cfg-verify"; cfg.mkdir(parents=True, exist_ok=True)
 7046  site = work / "site-verify"; site.mkdir(exist_ok=True)
 7047  # Every file present and whole, and verifying one takes a tenth of a second:
 7048  # with --seconds 1 the verify half-budget ends long before the 40 are done.
 7049  (site / "sitecustomize.py").write_text(
 7050      "import time\n"
 7051      "import raofflineproxy.auth as _auth\n"
 7052      "_auth.resolve_credentials = lambda *a, **k: {'user': 'qa', 'token': 't'}\n"
 7053      "import raofflineproxy.image_cache as _ic\n"
 7054      "_real = _ic.png_problem if hasattr(_ic, 'png_problem') else None\n"
 7055      "def _slow(payload):\n"
 7056      "    time.sleep(0.1)\n"
 7057      "    return None\n"
 7058      "_ic.png_problem = _slow\n")
 7059  os.environ["RAOFFLINEPROXY_CONFIG_DIR"] = str(cfg)
 7060  sys.path.insert(0, client)
 7061  import json, struct, zlib
 7062  from raofflineproxy import cache_keys, image_cache
 7063  from raofflineproxy.storage import Storage
 7064  st = Storage()
 7065  badges = [{"ID": 6000 + i, "Flags": 3, "BadgeURL": f"https://media.retroachievements.org/Badge/{9200 + i}.png"} for i in range(40)]
 7066  st.upsert_cache(cache_keys.patch(2, "qa"), json.dumps({"Success": True, "PatchData": {"ID": 2, "Achievements": badges}}))
 7067  st.close()
 7068  def _chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
 7069  PNG = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + _chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00" * 40)) + _chunk(b"IEND", b"")
 7070  for i in range(40):
 7071      f = image_cache.STATIC_DIR / "Badge" / f"{9200 + i}.png"; f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(PNG)
 7072  env = dict(os.environ, PYTHONPATH=f"{site}:{client}", HOME=str(work))
 7073  p = subprocess.run([sys.executable, helper, "--seconds", "1", "--verify"], env=env, capture_output=True, text=True, timeout=60)
 7074  out = p.stdout
 7075  print(f"{'PASS' if p.returncode == 3 and '>>> note VERIFY_LEFT' in out and '>>> why' not in out else 'FAIL'} verify-left: exit {p.returncode}; {' | '.join(l for l in out.splitlines() if 'VERIFY' in l or 'why' in l)}")
 7076  EOS
 7077  grep -q '^PASS verify-left:' "${DD}/d6b.out"; check $? "cache-images: a verify pass that stops with files left to verify and nothing missing exits 3 with note VERIFY_LEFT, no why ($(sed -n 's/^PASS verify-left: //p' "${DD}/d6b.out"))" "cache-images: $(grep 'verify-left:' "${DD}/d6b.out" || tail -3 "${DD}/d6b.out" | tr '\n' '|')"
 7078  fi
 7079  
 7080  # D7. #308 1-raoffline claude F-RA-06: the listing reads the systems the
 7081  # interface reads. SystemData::getConfigPath takes the first of
 7082  # es_systems_custom.cfg, the user's es_systems.cfg and the image's as the base
 7083  # -- a custom file IS the base there too, so the seat's scenario is the
 7084  # interface's own rule -- and then loadAdditionnalConfig merges every
 7085  # es_systems_*.cfg in the user's folder and beside the binary into it, by
 7086  # system name. The listing read the base alone: a system added by an
 7087  # es_systems_<name>.cfg was never indexed, and one whose <path> the file moved
 7088  # was looked for where it no longer is.
 7089  if [ "${DT_OK}" -eq 1 ]; then
 7090  printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7091  ESD="${TS}/.config/emulationstation"
 7092  treset; touch -d '2 hours ago' "${TMARK}"
 7093  mkdir -p "${TS}/roms/snes" "${TS}/roms/nes2"
 7094  printf 'SNES x' > "${TS}/roms/snes/x.sfc"
 7095  printf '<?xml version="1.0"?>\n<gameList>\n  <game><path>./x.sfc</path><name>X</name><cheevosHash>ssss</cheevosHash><cheevosId>301</cheevosId></game>\n</gameList>\n' > "${TS}/roms/snes/gamelist.xml"
 7096  # gb's folder moved by the extra file: its games are looked for in nes2.
 7097  printf 'GB m' > "${TS}/roms/nes2/m.gb"
 7098  printf '<?xml version="1.0"?>\n<gameList>\n  <game><path>./m.gb</path><name>M</name><cheevosHash>mmmm</cheevosHash><cheevosId>302</cheevosId></game>\n</gameList>\n' > "${TS}/roms/nes2/gamelist.xml"
 7099  cat > "${ESD}/es_systems_extra.cfg" <<'EOS'
 7100  <?xml version="1.0"?>
 7101  <systemList>
 7102    <system><name>snes</name><fullname>SNES</fullname><path>/storage/roms/snes</path></system>
 7103    <system><name>gb</name><path>/storage/roms/nes2</path></system>
 7104  </systemList>
 7105  EOS
 7106  : > "${TR}/helper-jobs.log"
 7107  tctl topup --after-index
 7108  grep -qP '^I\t301\tssss\t/storage/roms/snes/x.sfc$' "${TR}/helper-jobs.log"; check $? "#308 claude F-RA-06: a system an es_systems_<name>.cfg adds is read with the rest -- its indexed game is a job (rc ${RC})" "#308 claude F-RA-06: rc ${RC}; jobs: $(tr '\t' ',' < "${TR}/helper-jobs.log" | tr '\n' '|' | cut -c1-240) -- the listing read the base file alone"
 7109  grep -qP '^I\t302\tmmmm\t/storage/roms/nes2/m.gb$' "${TR}/helper-jobs.log"; check $? "#308 claude F-RA-06: a system whose <path> an es_systems_<name>.cfg moves is read at the new path" "#308 claude F-RA-06: jobs: $(tr '\t' ',' < "${TR}/helper-jobs.log" | tr '\n' '|' | cut -c1-240)"
 7110  rm -f "${ESD}/es_systems_extra.cfg"; rm -rf "${TS}/roms/snes" "${TS}/roms/nes2"
 7111  else
 7112      skip "#308 F-RA-06's cases: section t did not run"
 7113  fi
 7114  
 7115  # D8. #308 1-raoffline gpt F-RA-14: in an unindexed folder, a ROM is passed
 7116  # over as cached only when its game is whole for this account -- the patch
 7117  # row that names its path, the unlocks row, and an achievementsets row of
 7118  # the game -- as the index's test (is_cached) already asks. A patch row alone
 7119  # (a fetch that failed after the first write, or rows the eviction thinned
 7120  # on an older client) used to mark the ROM done for ever.
 7121  if [ "${DT_OK}" -eq 1 ]; then
 7122  printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7123  treset; PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
 7124  from raofflineproxy import cache_keys
 7125  from raofflineproxy.storage import Storage
 7126  s = Storage()
 7127  # h.gb: a patch row naming it and nothing else. i.gb: whole (patch, unlocks, sets).
 7128  s.upsert_cache(cache_keys.patch(150, "qa"), '{"Success":true,"PatchData":{"ID":150}}', source_rom_path="/gb/h.gb")
 7129  s.upsert_cache(cache_keys.patch(151, "qa"), '{"Success":true,"PatchData":{"ID":151}}', source_rom_path="/gb/i.gb")
 7130  s.upsert_cache(cache_keys.unlocks(151, "qa"), '{"Success":true,"UserUnlocks":[]}')
 7131  s.upsert_cache(cache_keys.achievementsets("iiii", "qa"), '{"Success":true,"GameId":151,"Sets":[]}')
 7132  s.close()
 7133  EOS
 7134  : > "${TR}/helper-jobs.log"
 7135  tctl scan
 7136  grep -qP '^H\t\t\t/storage/roms/gb/h.gb$' "${TR}/helper-jobs.log" && ! grep -q '/storage/roms/gb/i.gb$' "${TR}/helper-jobs.log"; check $? "#308 gpt F-RA-14: a ROM whose game has a patch row and nothing else is a job again; one whose game is whole is passed over" "#308 gpt F-RA-14: jobs: $(tr '\t' ',' < "${TR}/helper-jobs.log" | tr '\n' '|' | cut -c1-240) -- a patch path alone read as a complete cache"
 7137  else
 7138      skip "#308 F-RA-14's case: section t did not run"
 7139  fi
 7140  
 7141  # D9. #308 1-raoffline claude F-RA-10 = gpt F-RA-15: added= is the games that
 7142  # became ready for this account during the run -- read from the store before
 7143  # and after (a game is ready with its patch and unlocks rows) -- not the count
 7144  # of cache operations. A game the recently played pass caches for the first
 7145  # time is added (the client's run-smart-cache counts only games it newly
 7146  # cached); a second dump of a game already ready is cached and is not "more
 7147  # games" (D-UI-107's N MORE GAMES ARE READY).
 7148  if [ "${DT_OK}" -eq 1 ]; then
 7149  printf "${DCFG_ON}" > "${TCFG}"
 7150  # The recently played pass writes a game's rows on demand: /run/smart-rows.py
 7151  # runs through the client before the shim prints its result.
 7152  grep -q 'smart-rows' "${T}/shim/python3" || sed -i 's|^    "-m raofflineproxy.main run-smart-cache")$|&\n        [ -s /run/smart-rows.py ] \&\& /usr/bin/python3 /run/smart-rows.py|' "${T}/shim/python3"
 7153  grep -q 'smart-rows' "${T}/shim/python3"; check $? "the python3 shim's recently played pass can write rows (/run/smart-rows.py)" "the shim edit did not take"
 7154  TENV=(--setenv RAOFFLINEPROXY_HISTORY /storage/.config/retroarch/content_history.lpl)
 7155  treset; touch -d '2 hours ago' "${TMARK}"; touch "${THISTORY}"
 7156  cat > "${TR}/smart-rows.py" <<'EOS'
 7157  from raofflineproxy import cache_keys
 7158  from raofflineproxy.storage import Storage
 7159  s = Storage()
 7160  s.upsert_cache(cache_keys.patch(160, "qa"), '{"Success":true,"PatchData":{"ID":160}}', source_rom_path="/gb/h.gb")
 7161  s.upsert_cache(cache_keys.unlocks(160, "qa"), '{"Success":true,"UserUnlocks":[]}')
 7162  s.upsert_cache(cache_keys.achievementsets("hhhh", "qa"), '{"Success":true,"GameId":160,"Sets":[]}')
 7163  s.close()
 7164  EOS
 7165  echo '{"type":"result","scanned":1,"total":1,"cached":1,"skipped":0,"limit_reached":false}' > "${TR}/smart-result"
 7166  tctl topup
 7167  [ "${RC}" -eq 0 ] && grep -q ' 0 topup cached=1 .* added=1$' "${TSTAMP}"; check $? "#308 claude F-RA-10: a game the recently played pass caches for the first time is added (cached=1 added=1)" "#308 claude F-RA-10: rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null) -- the recently played pass's new game was not counted as added"
 7168  rm -f "${TR}/smart-rows.py" "${TR}/smart-result"
 7169  # A second dump of game 102 (already ready) among the index's jobs: cached,
 7170  # not added.
 7171  GLSIZE=$(stat -c %s "${TS}/roms/nes/gamelist.xml")
 7172  printf '<?xml version="1.0"?>\n<gameList parentHash="%s">\n  <game><path>./g.nes</path><name>G</name><cheevosHash>gggg</cheevosHash><cheevosId>102</cheevosId></game>\n</gameList>\n' "${GLSIZE}" > "${TS}/.config/emulationstation/recovery/nes/g.xml"
 7173  treset; touch -d '2 hours ago' "${TMARK}"; : > "${TR}/helper-jobs.log"
 7174  tctl topup --after-index
 7175  [ "${RC}" -eq 0 ] && grep -qP '^I\t102\tgggg\t' "${TR}/helper-jobs.log" && grep -q ' 0 topup cached=3 .* added=2$' "${TSTAMP}"; check $? "#308 gpt F-RA-15: three games cached by the index, one a second dump of a game already ready -- added=2" "#308 gpt F-RA-15: rc ${RC}; jobs: $(tr '\t' ',' < "${TR}/helper-jobs.log" | tr '\n' '|' | cut -c1-200); stamp: $(cat "${TSTAMP}" 2>/dev/null) -- a cache operation was counted as a new game"
 7176  rm -f "${TS}/.config/emulationstation/recovery/nes/g.xml"; TENV=()
 7177  else
 7178      skip "#308 F-RA-10/15's cases: section t did not run"
 7179  fi
 7180  
 7181  # D10. #308 1-raoffline gpt F-RA-13: the link's return asks whether a game was
 7182  # played since the last attempt (D-RA-035), and a game played in PPSSPP is a
 7183  # game played -- the pass it gates reads PPSSPP's recent list as well as
 7184  # RetroArch's history (the client's load_content_history_paths), and PPSSPP
 7185  # is the toggle's other emulator (D-RA-002). So ppsspp.ini, which PPSSPP
 7186  # writes at every exit and cheevos_ppsspp.sh at every launch, is read beside
 7187  # RetroArch's two history files, the newest winning.
 7188  if [ "${DT_OK}" -eq 1 ]; then
 7189  printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7190  DPINI="${TS}/.config/ppsspp/PSP/SYSTEM/ppsspp.ini"
 7191  treset; rm -f "${THISTORY}" "${TS}/playlists/builtin/content_history.lpl"; mkdir -p "$(dirname "${DPINI}")"
 7192  printf '[Recent]\nFileName0 = /storage/roms/psp/x.iso\n' > "${DPINI}"
 7193  touch -d '2 hours ago' "${TMARK}"; touch "${DPINI}"; : > "${TR}/probe.log"
 7194  tctl topup
 7195  [ "${RC}" -eq 0 ] && grep -q '^smart budget=' "${TR}/probe.log"; check $? "#308 gpt F-RA-13: a game played in PPSSPP since the mark (ppsspp.ini newer, no RetroArch history) makes the link's return run the recently played pass (rc ${RC})" "#308 gpt F-RA-13: rc ${RC}; probes: $(tr '\n' '|' < "${TR}/probe.log" | cut -c1-120); log: $(tail -n 1 "${TLOG}" | cut -c1-200) -- PPSSPP's play was invisible to the question"
 7196  touch -d '3 hours ago' "${DPINI}"; : > "${TR}/probe.log"; touch -d '2 hours ago' "${TMARK}"
 7197  tctl topup
 7198  [ "${RC}" -eq 0 ] && [ ! -s "${TR}/probe.log" ] && grep -q 'no game played since the last attempt' "${TLOG}"; check $? "#308 gpt F-RA-13: and with ppsspp.ini older than the mark, nothing played: skipped before the probe" "#308 gpt F-RA-13: rc ${RC}; probes: $(tr '\n' '|' < "${TR}/probe.log" | cut -c1-120)"
 7199  rm -rf "${TS}/.config/ppsspp"; touch -d '3 hours ago' "${THISTORY}"
 7200  else
 7201      skip "#308 F-RA-13's cases: section t did not run"
 7202  fi
 7203  
 7204  # D11. #308 1-raoffline gpt F-RA-18: disable verifies each step before it
 7205  # consumes what the step's recovery needs. The toggle is read back before
 7206  # anything is stopped (a toggle that would not clear leaves the device on,
 7207  # service and marker included, consistently); hardcore is read back before
 7208  # the record of what it was is removed, so a disable that could not put it
 7209  # back leaves the record for the next one. Section p's sandbox and its
 7210  # /run/fail-set, which makes one key's write fail.
 7211  if declare -F ctl >/dev/null && [ -n "${PCFG:-}" ]; then
 7212  rm -f "${P}/run/fail-set" "${P}/run/fail-start"
 7213  printf 'system.hostname=X\nglobal.retroachievements=1\nglobal.retroachievements.hardcore=1\n' > "${PCFG}"
 7214  ctl enable
 7215  echo global.retroachievements.hardcore > "${P}/run/fail-set"
 7216  ctl disable; rm -f "${P}/run/fail-set"
 7217  [ "${RC}" -eq 1 ] && [ "$(pv global.retroachievements.offlineproxy.hardcore_was)" = "1" ]; check $? "#308 gpt F-RA-18: a disable whose hardcore write fails exits 1 and keeps the record (hardcore_was=1)" "#308 gpt F-RA-18: rc ${RC}; system.cfg: $(tr '\n' '|' < "${PCFG}") -- the record went before the restore was verified"
 7218  ctl disable
 7219  [ "${RC}" -eq 0 ] && [ "$(pv global.retroachievements.hardcore)" = "1" ] && [ -z "$(pv global.retroachievements.offlineproxy.hardcore_was)" ]; check $? "#308 gpt F-RA-18: the next disable puts hardcore back to 1 from the kept record and then removes it" "#308 gpt F-RA-18: rc ${RC}; system.cfg: $(tr '\n' '|' < "${PCFG}") -- the player's hardcore setting was lost"
 7220  printf 'system.hostname=X\nglobal.retroachievements=1\nglobal.retroachievements.hardcore=1\n' > "${PCFG}"; : > "${P}/run/systemctl.log"
 7221  ctl enable
 7222  echo global.retroachievements.offlineproxy > "${P}/run/fail-set"; : > "${P}/run/systemctl.log"
 7223  ctl disable; rm -f "${P}/run/fail-set"
 7224  [ "${RC}" -eq 1 ] && [ "$(pv global.retroachievements.offlineproxy)" = "1" ] && [ -e "${PMARK}" ] && ! grep -q 'systemctl stop' "${P}/run/systemctl.log" && [ "$(pv global.retroachievements.offlineproxy.hardcore_was)" = "1" ]; check $? "#308 gpt F-RA-18: a toggle that will not clear stops nothing -- the service, the marker and the record stay, exit 1" "#308 gpt F-RA-18: rc ${RC}; toggle '$(pv global.retroachievements.offlineproxy)'; marker $([ -e "${PMARK}" ] && echo kept || echo gone); systemctl: $(tr '\n' '|' < "${P}/run/systemctl.log")"
 7225  ctl disable
 7226  else
 7227      skip "#308 F-RA-18's cases: section p did not run"
 7228  fi
 7229  
 7230  # D12a. #308 1-raoffline claude F-RA-20: the unit's start limit sits in
 7231  # [Unit], as StartLimitIntervalSec= and StartLimitBurst=, where systemd has
 7232  # read it since 230 (in [Service] it is the old spelling, accepted for
 7233  # compatibility with a deprecation line in the journal).
 7234  UNIT_REL=projects/ROCKNIX/packages/network/raofflineproxy/system.d/raofflineproxy.service
 7235  src_of "${UNIT_REL}" "${DD}/raofflineproxy.service"
 7236  awk '/^\[/{s=$0} s=="[Unit]" && /^StartLimitIntervalSec=[0-9]+$/{a=1} s=="[Unit]" && /^StartLimitBurst=5$/{b=1} s=="[Service]" && /^StartLimit/{c=1} END{exit !(a && b && !c)}' "${DD}/raofflineproxy.service"; check $? "#308 claude F-RA-20 unit: StartLimitIntervalSec and StartLimitBurst=5 in [Unit], nothing of the start limit in [Service] (the interval sized in D25)" "#308 claude F-RA-20 unit: $(grep -n 'StartLimit\|^\[' "${DD}/raofflineproxy.service" | tr '\n' '|')"
 7237  
 7238  # D12b. #308 1-raoffline gpt F-RA-26: the unit is started when the proxy is
 7239  # listening, not when its process has forked. Type=simple made `systemctl
 7240  # start` (and so enable, which sets the routing toggle after it) and the
 7241  # Before= on the interface return the moment Python began importing;
 7242  # ExecStartPost now waits, bounded, for 127.0.0.1:8080 to be in LISTEN,
 7243  # through the ctl's `listening` verb, which reads /proc/net/tcp{,6}
 7244  # (RAOFFLINEPROXY_PROC_NET here) and runs no tool.
 7245  UNIT_REL=projects/ROCKNIX/packages/network/raofflineproxy/system.d/raofflineproxy.service
 7246  src_of "${UNIT_REL}" "${DD}/raofflineproxy.service"
 7247  awk '/^\[/{s=$0} s=="[Service]" && /^ExecStartPost=\/usr\/bin\/raofflineproxy-ctl listening --wait [0-9]+$/{f=1} END{exit !f}' "${DD}/raofflineproxy.service"; check $? "#308 gpt F-RA-26 unit: ExecStartPost waits for the listener (raofflineproxy-ctl listening --wait N)" "#308 gpt F-RA-26 unit: no readiness wait: $(grep -n '^Type=\|^ExecStart' "${DD}/raofflineproxy.service" | tr '\n' '|')"
 7248  if [ "${DT_OK}" -eq 1 ]; then
 7249  DPN="${TS}/procnet"; mkdir -p "${DPN}"
 7250  dproc() { # <tcp line or empty> <tcp6 line or empty>
 7251      printf '  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n%s' "${1:+   0: $1 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 1 1 0000000000000000 100 0 0 10 0
 7252  }" > "${DPN}/tcp"
 7253      printf '  sl  local_address                         remote_address                        st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n%s' "${2:+   0: $2 00000000000000000000000000000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 2 1 0000000000000000 100 0 0 10 0
 7254  }" > "${DPN}/tcp6"
 7255  }
 7256  TENV=(--setenv RAOFFLINEPROXY_PROC_NET /storage/procnet)
 7257  dproc 0100007F:1F90 ""; tctl listening; DL1=${RC}
 7258  dproc 00000000:1F90 ""; tctl listening; DL2=${RC}
 7259  dproc "" 00000000000000000000000001000000:1F90; tctl listening; DL3=${RC}
 7260  dproc "" 0000000000000000FFFF00000100007F:1F90; tctl listening; DL6=${RC}
 7261  dproc 0100007F:1F91 ""; tctl listening; DL4=${RC}
 7262  printf '  sl  local_address rem_address   st\n   0: 0100007F:1F90 0100007F:9C40 01 00000000:00000000\n' > "${DPN}/tcp"; : > "${DPN}/tcp6"; tctl listening; DL5=${RC}
 7263  [ "${DL1}" -eq 0 ] && [ "${DL2}" -eq 0 ] && [ "${DL6}" -eq 0 ] && [ "${DL3}" -eq 1 ] && [ "${DL4}" -eq 1 ] && [ "${DL5}" -eq 1 ]; check $? "#308 gpt F-RA-26 listening: 127.0.0.1:8080, 0.0.0.0:8080 and ::ffff:127.0.0.1:8080 in LISTEN read as listening; [::1]:8080 does not -- it cannot take the IPv4 connection the emulators make (gpt G-D-02) -- nor another port, nor 8080 only as a connection's end" "#308 gpt F-RA-26 / G-D-02 listening: rc ${DL1}/${DL2}/${DL6} (want 0/0/0), ${DL3}/${DL4}/${DL5} (want 1/1/1)"
 7264  dproc "" ""; : > "${TR}/sleep.log"
 7265  tctl listening --wait 5
 7266  [ "${RC}" -eq 1 ] && [ "$(grep -c . "${TR}/sleep.log")" -eq 4 ]; check $? "#308 gpt F-RA-26 listening --wait 5 with nothing listening: five looks a second apart, then exit 1" "#308 gpt F-RA-26: rc ${RC}; sleeps: $(tr '\n' ',' < "${TR}/sleep.log")"
 7267  rm -f "${TR}/fast-sleep"; dproc "" ""
 7268  ( sleep 1.5; dproc 0100007F:1F90 "" ) &
 7269  DT0=$(dnow); tctl listening --wait 10; DTOOK=$(dsince "${DT0}"); wait
 7270  [ "${RC}" -eq 0 ] && awk -v t="${DTOOK}" 'BEGIN{exit !(t < 5)}'; check $? "#308 gpt F-RA-26 listening --wait 10: the listener that appears after 1.5 s is seen, exit 0 after ${DTOOK}s" "#308 gpt F-RA-26: rc ${RC} after ${DTOOK}s"
 7271  touch "${TR}/fast-sleep"; TENV=(); rm -rf "${DPN}"
 7272  else
 7273      skip "#308 F-RA-26's listening cases: section t did not run"
 7274  fi
 7275  
 7276  # D13a. #308 1-raoffline gpt F-RA-27 (patch 008): only a JSON true opts in to
 7277  # the automatic log upload -- "false", 1 and "yes" do not -- on the patched
 7278  # tree section t built.
 7279  if [ "${DT_OK}" -eq 1 ]; then
 7280  RAOFFLINEPROXY_CONFIG_DIR="${DD}/d13a-cfg" PYTHONPATH="${CLIENT}" python3 -  > "${DD}/d13a.out" 2>&1 <<'EOS'
 7281  import json, os, socket, struct, sys, threading, time, zlib, importlib.machinery, importlib.util
 7282  from pathlib import Path
 7283  Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
 7284  def verdict(ok, name, detail=""):
 7285      print(("PASS " if ok else "FAIL ") + name + (f" -- {detail}" if detail and not ok else ""))
 7286  from raofflineproxy import image_cache, network, proxy_service, storage_corruption
 7287  # 008 / F-RA-27
 7288  uploads = []
 7289  saved = proxy_service.log_uploader.report_storage_corruption
 7290  proxy_service.log_uploader.report_storage_corruption = lambda incident: uploads.append(incident) or "up-1"
 7291  try:
 7292      got = {}
 7293      for label, value in (("string false", "false"), ("number 1", 1), ("string yes", "yes"), ("true", True)):
 7294          (Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]) / "storage_corruption.json").write_text(json.dumps({"detected_at": 1, "quarantined_path": "x", "reason": "r", "size_bytes": 1, "lost_pending_awards": None, "reported": False, "upload_id": None, "notified": False}))
 7295          uploads.clear()
 7296          proxy_service.retry_storage_corruption_report({"upload_logs": value})
 7297          got[label] = len(uploads)
 7298      verdict(got == {"string false": 0, "number 1": 0, "string yes": 0, "true": 1}, "F-RA-27 upload opt-in: only a JSON true sends the report", f"uploads by value: {got}")
 7299  finally:
 7300      proxy_service.log_uploader.report_storage_corruption = saved
 7301  EOS
 7302  grep -q '^\(PASS\|FAIL\) ' "${DD}/d13a.out"; check $? "stream D's d13a predicates ran ($(grep -c '^PASS' "${DD}/d13a.out") PASS / $(grep -c '^FAIL' "${DD}/d13a.out") FAIL)" "stream D's d13a predicates printed no verdicts: $(tail -5 "${DD}/d13a.out" | tr '\n' '|' | cut -c1-300)"
 7303  while IFS= read -r line; do
 7304      case "${line}" in
 7305          PASS\ *) check 0 "#308 ${line#PASS }" "" ;;
 7306          FAIL\ *) check 1 "" "#308 ${line#FAIL }" ;;
 7307      esac
 7308  done < "${DD}/d13a.out"
 7309  else
 7310      skip "the d13a predicates: section t did not run"
 7311  fi
 7312  
 7313  # D13b. #308 1-raoffline claude F-RA-13 (patch 013, cache-images): a PNG with
 7314  # bytes after its IEND is a whole PNG -- published, and left alone by
 7315  # --verify -- since the chunk walk, not the last twelve bytes, is the test;
 7316  # and gpt F-RA-12 (cache-images): --verify applies the test a download passes,
 7317  # CRCs and the image data included (image_cache.png_problem, patch 013), so a
 7318  # file damaged inside before patch 013 existed is found and re-fetched.
 7319  if [ "${DT_OK}" -eq 1 ]; then
 7320  RAOFFLINEPROXY_CONFIG_DIR="${DD}/d13b-cfg" PYTHONPATH="${CLIENT}" python3 - "${DD}/raofflineproxy-cache-images" > "${DD}/d13b.out" 2>&1 <<'EOS'
 7321  import json, os, socket, struct, sys, threading, time, zlib, importlib.machinery, importlib.util
 7322  from pathlib import Path
 7323  Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
 7324  def verdict(ok, name, detail=""):
 7325      print(("PASS " if ok else "FAIL ") + name + (f" -- {detail}" if detail and not ok else ""))
 7326  from raofflineproxy import image_cache, network, proxy_service, storage_corruption
 7327  # 013 / F-RA-13 and cache-images / F-RA-12
 7328  def _chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
 7329  PNG = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + _chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00" * 40)) + _chunk(b"IEND", b"")
 7330  TRAILING = PNG + b"\x00" * 16 + b"encoder note"
 7331  bad = bytearray(zlib.compress(b"\x00\xff\x00\x00" * 40)); bad[6] ^= 0xFF
 7332  BAD_IDAT = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + _chunk(b"IDAT", bytes(bad)) + _chunk(b"IEND", b"")
 7333  saved_fetch = image_cache._fetch_image
 7334  try:
 7335      image_cache._fetch_image = lambda url, user_agent: TRAILING
 7336      image_cache.download_static_image("https://media.retroachievements.org/Badge/d13-trailing.png", "/Badge/d13-trailing.png", "ua")
 7337      verdict(image_cache.resolve_cached_static_asset("/Badge/d13-trailing.png") is not None, "F-RA-13 patch 013: a whole PNG with bytes after its IEND is published")
 7338  finally:
 7339      image_cache._fetch_image = saved_fetch
 7340  spec = importlib.util.spec_from_loader("images_helper", importlib.machinery.SourceFileLoader("images_helper", sys.argv[1]))
 7341  helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
 7342  badge = image_cache.STATIC_DIR / "Badge"; badge.mkdir(parents=True, exist_ok=True)
 7343  (badge / "d13-verify-trailing.png").write_bytes(TRAILING)
 7344  (badge / "d13-verify-good.png").write_bytes(PNG)
 7345  (badge / "d13-verify-bad-idat.png").write_bytes(BAD_IDAT)
 7346  (badge / "d13-verify-bad-crc.png").write_bytes(PNG[:-1] + bytes([PNG[-1] ^ 1]))
 7347  got = {n: helper.damaged(f"/Badge/d13-verify-{n}.png") for n in ("good", "trailing", "bad-idat", "bad-crc")}
 7348  verdict(got["trailing"] is None, "F-RA-13 --verify: a cached PNG with bytes after its IEND is whole, never deleted", f"damaged() said {got['trailing']!r}")
 7349  verdict(got["good"] is None and got["bad-idat"] is not None and got["bad-crc"] is not None, "F-RA-12 --verify: a cached PNG whose image data or a chunk's CRC is damaged is found; a whole one is not", f"damaged(): {got}")
 7350  EOS
 7351  grep -q '^\(PASS\|FAIL\) ' "${DD}/d13b.out"; check $? "stream D's d13b predicates ran ($(grep -c '^PASS' "${DD}/d13b.out") PASS / $(grep -c '^FAIL' "${DD}/d13b.out") FAIL)" "stream D's d13b predicates printed no verdicts: $(tail -5 "${DD}/d13b.out" | tr '\n' '|' | cut -c1-300)"
 7352  while IFS= read -r line; do
 7353      case "${line}" in
 7354          PASS\ *) check 0 "#308 ${line#PASS }" "" ;;
 7355          FAIL\ *) check 1 "" "#308 ${line#FAIL }" ;;
 7356      esac
 7357  done < "${DD}/d13b.out"
 7358  else
 7359      skip "the d13b predicates: section t did not run"
 7360  fi
 7361  
 7362  # D13c. #308 1-raoffline gpt F-RA-20 (patch 015): a host the bounded lookup
 7363  # has just resolved is answered from that answer when the connection looks it
 7364  # up again, so a resolver that stops answering between the two cannot hold
 7365  # the request; and claude F-RA-11 (patch 015): the upstream forwarder's half,
 7366  # untested before -- a lookup that fails returns the 503 network_error at
 7367  # once and opens no connection (its urlsplit is the module's own import,
 7368  # proxy_service.py line 14 at the pin). Then the client's own network tests.
 7369  if [ "${DT_OK}" -eq 1 ]; then
 7370  RAOFFLINEPROXY_CONFIG_DIR="${DD}/d13c-cfg" PYTHONPATH="${CLIENT}" python3 -  > "${DD}/d13c.out" 2>&1 <<'EOS'
 7371  import json, os, socket, struct, sys, threading, time, zlib, importlib.machinery, importlib.util
 7372  from pathlib import Path
 7373  Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
 7374  def verdict(ok, name, detail=""):
 7375      print(("PASS " if ok else "FAIL ") + name + (f" -- {detail}" if detail and not ok else ""))
 7376  from raofflineproxy import image_cache, network, proxy_service, storage_corruption
 7377  # 015 / F-RA-20: the connection's second lookup of a host just resolved.
 7378  real = socket._socket.getaddrinfo
 7379  calls = []
 7380  def resolver(host, port, family=0, type=0, proto=0, flags=0):
 7381      calls.append((host, port))
 7382      if len(calls) == 1:
 7383          return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.7", 0))]
 7384      time.sleep(5)
 7385      raise OSError("the resolver stopped answering")
 7386  socket._socket.getaddrinfo = resolver
 7387  try:
 7388      ok, why = network.resolve_host_bounded("dns-test.invalid", seconds=1.0)
 7389      result = {}
 7390      def connect_lookup():
 7391          try:
 7392              result["answer"] = socket.getaddrinfo("dns-test.invalid", 443, 0, socket.SOCK_STREAM)
 7393          except Exception as exc:
 7394              result["error"] = repr(exc)
 7395      t0 = time.monotonic(); th = threading.Thread(target=connect_lookup, daemon=True); th.start(); th.join(2.0); took = time.monotonic() - t0
 7396      answer = result.get("answer") or []
 7397      verdict(ok and not th.is_alive() and any(a[4][:2] == ("192.0.2.7", 443) and a[1] == socket.SOCK_STREAM for a in answer),
 7398              "F-RA-20 patch 015: the connection's own lookup of a host the bounded lookup just resolved is answered at once from that answer (port 443), not from a resolver that has stopped",
 7399              f"bounded ok={ok} ({why}); second lookup {'still waiting' if th.is_alive() else result} after {took:.2f}s")
 7400  finally:
 7401      socket._socket.getaddrinfo = real
 7402  # 015 / claude F-RA-11: the forwarder with a lookup that fails.
 7403  opened = []
 7404  saved_urlopen = proxy_service.urllib.request.urlopen if hasattr(proxy_service, "urllib") else None
 7405  import urllib.request
 7406  saved_global_urlopen = urllib.request.urlopen
 7407  urllib.request.urlopen = lambda *a, **k: opened.append(a) or (_ for _ in ()).throw(AssertionError("no connection may be opened"))
 7408  def failing(host, port, family=0, type=0, proto=0, flags=0):
 7409      raise OSError("Temporary failure in name resolution")
 7410  socket._socket.getaddrinfo = failing
 7411  class Srv:
 7412      config_data = {"upstream_host": "https://forward-test.invalid"}
 7413  try:
 7414      t0 = time.monotonic()
 7415      res = proxy_service.ProxyRuntimeServer.forward_to_upstream_result(Srv(), "GET", "/dorequest.php?r=login2&u=qa", "", {"User-Agent": "ra"})
 7416      took = time.monotonic() - t0
 7417      verdict(res[0] == "network_error" and res[1] == 503 and opened == [] and took < 2.0 and b"name lookup" in res[3],
 7418              "F-RA-11 patch 015: the forwarder with a failed lookup returns network_error 503 at once and opens no connection",
 7419              f"{res[:3]} after {took:.2f}s, opened {len(opened)}")
 7420  except Exception as exc:
 7421      verdict(False, "F-RA-11 patch 015: the forwarder with a failed lookup returns network_error 503 at once and opens no connection", repr(exc))
 7422  finally:
 7423      socket._socket.getaddrinfo = real; urllib.request.urlopen = saved_global_urlopen
 7424      network.reset_retroachievements_reachability_for_tests()
 7425  EOS
 7426  grep -q '^\(PASS\|FAIL\) ' "${DD}/d13c.out"; check $? "stream D's d13c predicates ran ($(grep -c '^PASS' "${DD}/d13c.out") PASS / $(grep -c '^FAIL' "${DD}/d13c.out") FAIL)" "stream D's d13c predicates printed no verdicts: $(tail -5 "${DD}/d13c.out" | tr '\n' '|' | cut -c1-300)"
 7427  while IFS= read -r line; do
 7428      case "${line}" in
 7429          PASS\ *) check 0 "#308 ${line#PASS }" "" ;;
 7430          FAIL\ *) check 1 "" "#308 ${line#FAIL }" ;;
 7431      esac
 7432  done < "${DD}/d13c.out"
 7433  # The patched client's own tests for patch 015's network half still pass
 7434  # with the lookup's answer remembered.
 7435  ( cd "${T}/patched" && PYTHONPATH=. RAOFFLINEPROXY_CONFIG_DIR="${DD}/unittest-cfg" python3 -m unittest linux.tests.test_linux_network > "${DD}/unittest.out" 2>&1 ); DUT=$?
 7436  [ "${DUT}" -eq 0 ]; check $? "the patched client's tests/test_linux_network.py pass ($(tail -n 3 "${DD}/unittest.out" | grep -o 'Ran [0-9]* tests\?' || echo '?'))" "the client's network tests: rc ${DUT}: $(grep -E '^(FAIL|ERROR):' "${DD}/unittest.out" | head -3 | tr '\n' '|') $(tail -n 3 "${DD}/unittest.out" | tr '\n' '|')"
 7437  else
 7438      skip "the d13c predicates: section t did not run"
 7439  fi
 7440  
 7441  # D14. #308 9-emulators claude F-EM-03 = gpt F-EM-03, claude F-EM-09 = gpt
 7442  # F-EM-05: cheevos_armsx2.sh leaves secrets.ini with one [Achievements]
 7443  # section holding one Token line, whatever it held before -- a second
 7444  # [Achievements] header (the shape the pre-#170 script appended on a device
 7445  # whose PCSX2.ini lacked the section), an empty file, no file -- and keeps
 7446  # every other line; a second launch changes nothing. Run whole, with the
 7447  # image's busybox for sed and awk (the device's), as section w runs it.
 7448  src_of "projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/scripts/cheevos_armsx2.sh" "${DD}/cheevos_armsx2.sh"
 7449  DA="${DD}/armsx2"; DAI="${DA}/storage/.config/ARMSX2/inis"; mkdir -p "${DAI}" "${DA}/repo" "${DA}/shim"
 7450  cp "${DD}/cheevos_armsx2.sh" "${DA}/repo/cheevos_armsx2.sh"
 7451  DABB=(); DAPATH="/shim:/usr/bin:/bin"
 7452  if [ -n "${BB}" ]; then DABB=(--ro-bind "${TMP}/bbin" /bbin --ro-bind "${BB_HOST}" "${BB}"); DAPATH="/shim:/bbin:/usr/bin:/bin"; fi
 7453  cat > "${DA}/profile" <<PEOF
 7454  export PATH=${DAPATH}
 7455  get_setting() {
 7456      case "\$1" in
 7457          global.retroachievements) echo 1 ;;
 7458          global.retroachievements.username) echo player ;;
 7459          global.retroachievements.token) echo TOKEN-NEW ;;
 7460          *) echo 0 ;;
 7461      esac
 7462  }
 7463  PEOF
 7464  dar() { # one launch's script; rc in $RC
 7465      RC=$( ( bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr "${DABB[@]}" \
 7466          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 7467          --ro-bind /etc /etc --ro-bind "${DA}/profile" /etc/profile \
 7468          --bind "${DA}/storage" /storage --ro-bind "${DA}/shim" /shim --ro-bind "${DA}/repo" /repo \
 7469          --dev /dev --proc /proc --tmpfs /tmp --tmpfs /var \
 7470          bash /repo/cheevos_armsx2.sh > "${DA}/out" 2>&1; echo $? ) 2>/dev/null )
 7471  }
 7472  dasecrets() { printf "$1" > "${DAI}/secrets.ini"; }
 7473  dashape() { # <name> <expected other lines, | separated>: one header, one Token, the others kept, a second launch a no-op
 7474      local want="$2" n_hdr n_tok other
 7475      n_hdr=$(grep -cFx '[Achievements]' "${DAI}/secrets.ini" 2>/dev/null); n_tok=$(grep -c '^Token *=' "${DAI}/secrets.ini" 2>/dev/null)
 7476      other="$(grep -v '^Token *=' "${DAI}/secrets.ini" 2>/dev/null | grep -vFx '[Achievements]' | grep -v '^$' | tr '\n' '|')"
 7477      cp "${DAI}/secrets.ini" "${DA}/first" 2>/dev/null; dar
 7478      [ "${n_hdr:-0}" -eq 1 ] && [ "${n_tok:-0}" -eq 1 ] && grep -qx 'Token = TOKEN-NEW' "${DAI}/secrets.ini" && [ "${other}" = "${want}" ] && cmp -s "${DA}/first" "${DAI}/secrets.ini" \
 7479          && awk '/^\[Achievements\]$/{a=1; next} /^\[/{a=0} /^Token *=/{exit !a} END{}' "${DAI}/secrets.ini"
 7480      check $? "#308 F-EM-03/05/09 cheevos_armsx2.sh, $1: one [Achievements], one Token (the current one) inside it, the rest kept, the next launch changes nothing" "#308 F-EM-03/05/09 cheevos_armsx2.sh, $1: rc ${RC}; secrets.ini: $( { tr '\n' '|' < "${DAI}/secrets.ini"; } 2>/dev/null || echo absent) (want the other lines '${want}')"
 7481  }
 7482  printf '[Achievements]\nEnabled = true\nUsername = player\n' > "${DAI}/PCSX2.ini"
 7483  dasecrets '[Achievements]\nToken = old\n[Achievements]\nToken = old\n'; dar; dashape "two headers, a Token under each (claude's shape)" ""
 7484  dasecrets '[Achievements]\nToken =\n[Achievements]\nToken = old\n'; dar; dashape "the seed's bare Token, then a second header (gpt's shape)" ""
 7485  dasecrets '[Other]\nKey = 1\n[Achievements]\nToken = x\nFoo = bar\n[More]\nZ = 2\n[Achievements]\nToken = y\nBaz = 3\n'; dar; dashape "two sections apart, other sections and keys" "[Other]|Key = 1|Foo = bar|Baz = 3|[More]|Z = 2|"
 7486  : > "${DAI}/secrets.ini"; dar; dashape "an empty file" ""
 7487  rm -f "${DAI}/secrets.ini"; dar; dashape "no file" ""
 7488  dasecrets '[Achievements]\nToken = old\n'; dar; dashape "the ordinary file" ""
 7489  
 7490  # D15. #308 9-emulators claude F-EM-04: cheevos_ppsspp.sh asks whether the
 7491  # proxy is listening without netstat -- which no package of PPSSPP's declares,
 7492  # and whose absence read as "nothing answers" -- by reading /proc/net/tcp and
 7493  # tcp6 itself (bash and grep, both on the image), and says apart "nothing is
 7494  # listening" and "couldn't tell". 0.0.0.0 and [::1] count as the loopback's.
 7495  # Run whole, with the image's busybox for sed; the socket table is a fixture
 7496  # (RAOFFLINEPROXY_PROC_NET, as for the ctl's `listening`).
 7497  src_of "projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/scripts/cheevos_ppsspp.sh" "${DD}/cheevos_ppsspp.sh"
 7498  DP="${DD}/ppsspp"; DPS="${DP}/storage/.config/ppsspp/PSP/SYSTEM"; mkdir -p "${DPS}" "${DP}/repo" "${DP}/shim" "${DP}/procnet"
 7499  cp "${DD}/cheevos_ppsspp.sh" "${DP}/repo/cheevos_ppsspp.sh"
 7500  cat > "${DP}/profile" <<PEOF
 7501  export PATH=$([ -n "${BB}" ] && echo /shim:/bbin:/usr/bin:/bin || echo /shim:/usr/bin:/bin)
 7502  get_setting() {
 7503      case "\$1" in
 7504          global.retroachievements) echo 1 ;;
 7505          global.retroachievements.username) echo player ;;
 7506          global.retroachievements.token) echo TOKEN ;;
 7507          global.retroachievements.hardcore) echo 0 ;;
 7508          global.retroachievements.offlineproxy) echo 1 ;;
 7509          *) echo "" ;;
 7510      esac
 7511  }
 7512  PEOF
 7513  dpp() { # one launch's script against the fixture socket table; rc in $RC, the log in ${DP}/log
 7514      RC=$( ( bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr $([ -n "${BB}" ] && echo "--ro-bind ${TMP}/bbin /bbin --ro-bind ${BB_HOST} ${BB}") \
 7515          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 7516          --ro-bind /etc /etc --ro-bind "${DP}/profile" /etc/profile \
 7517          --bind "${DP}/storage" /storage --ro-bind "${DP}/shim" /shim --ro-bind "${DP}/repo" /repo --ro-bind "${DP}/procnet" /procnet \
 7518          --dev /dev --proc /proc --tmpfs /tmp --tmpfs /var --dir /var/log --setenv RAOFFLINEPROXY_PROC_NET "${1:-/procnet}" \
 7519          bash -c 'bash /repo/cheevos_ppsspp.sh; rc=$?; cat /var/log/cheevos.log > /storage/cheevos.log 2>/dev/null; exit $rc' > "${DP}/out" 2>&1; echo $? ) 2>/dev/null )
 7520  }
 7521  dppini() { printf '[General]\nX = 1\n[Achievements]\nAchievementsEnable = False\nAchievementsUserName = player\nAchievementsChallengeMode = False\nAchievementsHost = \n' > "${DPS}/ppsspp.ini"; rm -f "${DP}/storage/cheevos.log"; }
 7522  printf '  sl  local_address rem_address   st\n   0: 0100007F:1F90 00000000:0000 0A 00000000:00000000\n' > "${DP}/procnet/tcp"; : > "${DP}/procnet/tcp6"
 7523  dppini; dpp
 7524  grep -qx 'AchievementsHost = 127.0.0.1:8080' "${DPS}/ppsspp.ini"; check $? "#308 claude F-EM-04 cheevos_ppsspp.sh: 127.0.0.1:8080 in LISTEN in the socket table routes PPSSPP to the proxy (no netstat)" "#308 claude F-EM-04: rc ${RC}; ppsspp.ini: $(grep AchievementsHost "${DPS}/ppsspp.ini"); log: $(cat "${DP}/storage/cheevos.log" 2>/dev/null | tr '\n' '|')"
 7525  printf '  sl  local_address                         remote_address                        st\n   0: 00000000000000000000000001000000:1F90 00000000000000000000000000000000:0000 0A 00000000:00000000\n' > "${DP}/procnet/tcp6"; : > "${DP}/procnet/tcp"
 7526  dppini; dpp
 7527  grep -qx 'AchievementsHost = ' "${DPS}/ppsspp.ini" && grep -q 'nothing is listening on 127.0.0.1:8080' "${DP}/storage/cheevos.log"; check $? "gpt G-D-02 cheevos_ppsspp.sh: [::1]:8080 alone in LISTEN (tcp6) is not the IPv4 endpoint PPSSPP is pointed at -- launched direct" "gpt G-D-02: ppsspp.ini: $(grep AchievementsHost "${DPS}/ppsspp.ini") -- an IPv6-loopback listener read as 127.0.0.1:8080"
 7528  printf '  sl  local_address                         remote_address                        st\n   0: 0000000000000000FFFF00000100007F:1F90 00000000000000000000000000000000:0000 0A 00000000:00000000\n' > "${DP}/procnet/tcp6"; : > "${DP}/procnet/tcp"
 7529  dppini; dpp
 7530  grep -qx 'AchievementsHost = 127.0.0.1:8080' "${DPS}/ppsspp.ini"; check $? "gpt G-D-02 cheevos_ppsspp.sh: ::ffff:127.0.0.1:8080 in LISTEN (tcp6, an IPv4-mapped socket) routes to the proxy" "gpt G-D-02: ppsspp.ini: $(grep AchievementsHost "${DPS}/ppsspp.ini")"
 7531  printf '  sl  local_address rem_address   st\n   0: 0100007F:1F91 00000000:0000 0A 00000000:00000000\n' > "${DP}/procnet/tcp"; : > "${DP}/procnet/tcp6"
 7532  dppini; dpp
 7533  grep -qx 'AchievementsHost = ' "${DPS}/ppsspp.ini" && grep -q 'nothing is listening on 127.0.0.1:8080' "${DP}/storage/cheevos.log"; check $? "#308 claude F-EM-04 cheevos_ppsspp.sh: nothing on 8080 launches direct, and the log says nothing is listening" "#308 claude F-EM-04: ppsspp.ini: $(grep AchievementsHost "${DPS}/ppsspp.ini"); log: $(cat "${DP}/storage/cheevos.log" 2>/dev/null | tr '\n' '|')"
 7534  dppini; dpp /nonexistent
 7535  grep -qx 'AchievementsHost = ' "${DPS}/ppsspp.ini" && grep -q "couldn't tell whether" "${DP}/storage/cheevos.log" && ! grep -q 'nothing is listening' "${DP}/storage/cheevos.log"; check $? "#308 claude F-EM-04 cheevos_ppsspp.sh: a socket table it cannot read launches direct and says it couldn't tell -- not that nothing answers" "#308 claude F-EM-04: ppsspp.ini: $(grep AchievementsHost "${DPS}/ppsspp.ini"); log: $(cat "${DP}/storage/cheevos.log" 2>/dev/null | tr '\n' '|')"
 7536  
 7537  # D16. #308 1-raoffline claude F-RA-23 = gpt F-RA-24: the recipe declares the
 7538  # packages that provide the tools its shipped scripts call
 7539  # (packaging-and-patches.md, "A shipped script's tools are dependencies too"):
 7540  # bash (the ctl's interpreter), busybox (flock, mkfifo, mktemp, stat, logger,
 7541  # sed, awk, head, tail, date, sleep), coreutils (timeout: the image's is
 7542  # coreutils', a file in /usr/bin, not a busybox link), grep (GNU grep; the
 7543  # image's busybox has no grep applet) and systemd (systemctl).
 7544  src_of "${PKG_REL:-projects/ROCKNIX/packages/network/raofflineproxy/package.mk}" "${DD}/package.mk"
 7545  DDEPS=" $(sed -n 's/^PKG_DEPENDS_TARGET="\(.*\)"$/\1/p' "${DD}/package.mk" | head -n 1) "
 7546  DMISS=""; for p in Python3 bash busybox coreutils grep systemd; do case "${DDEPS}" in *" ${p} "*) ;; *) DMISS="${DMISS} ${p}" ;; esac; done
 7547  [ -z "${DMISS}" ]; check $? "#308 F-RA-23/24 package.mk: PKG_DEPENDS_TARGET names Python3, bash, busybox, coreutils, grep and systemd (${DDEPS# })" "#308 F-RA-23/24 package.mk: PKG_DEPENDS_TARGET is '${DDEPS# }', missing:${DMISS}"
 7548  
 7549  # D17. #308 1-raoffline gpt F-RA-10: a helper's budget bounds its blocking
 7550  # work. The image helper waited in as_completed for a download to finish
 7551  # before it could look at its deadline, and then for the running ones as the
 7552  # pool closed: with downloads of five seconds and --seconds 1 it now returns
 7553  # at its bound (D1's store and stand-in download, forty badges missing).
 7554  # And the ctl's half: each helper the ctl runs is bounded at the process as
 7555  # well as by its own --seconds -- the scan's and the top-up's image pass, the
 7556  # `images` verb and the `refresh` verb run under `timeout` (the harness's shim
 7557  # hands the budget to the child as FAKE_BUDGET).
 7558  if [ "${DT_OK}" -eq 1 ]; then
 7559  python3 - "${DD}/raofflineproxy-cache-images" "${CLIENT}" "${DD}/images" > "${DD}/d17.out" 2>&1 <<'EOS'
 7560  import os, subprocess, sys, time
 7561  from pathlib import Path
 7562  helper, client, work = sys.argv[1], sys.argv[2], Path(sys.argv[3])
 7563  calls = work / "calls"; calls.write_text("")
 7564  env = dict(os.environ, PYTHONPATH=f"{work / 'site'}:{client}", RAOFFLINEPROXY_CONFIG_DIR=str(work / "cfg"), HOME=str(work), D_CALLS=str(calls), D_EACH="5")
 7565  t0 = time.monotonic()
 7566  p = subprocess.Popen([sys.executable, helper, "--seconds", "1"], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 7567  try:
 7568      out, _ = p.communicate(timeout=30)
 7569  except subprocess.TimeoutExpired:
 7570      p.kill(); out, _ = p.communicate()
 7571  took = time.monotonic() - t0; out = out.decode(errors="replace")
 7572  print(f"{'PASS' if p.returncode == 1 and took < 3.0 and '>>> why SOME_IMAGES_NOT_SAVED' in out else 'FAIL'} budget: --seconds 1 over five-second downloads -- exit {p.returncode} after {took:.2f}s")
 7573  EOS
 7574  grep -q '^PASS budget:' "${DD}/d17.out"; check $? "#308 gpt F-RA-10 cache-images: a pass of --seconds 1 returns at its bound with SOME_IMAGES_NOT_SAVED, not after the running downloads ($(sed -n 's/^PASS budget: //p' "${DD}/d17.out"))" "#308 gpt F-RA-10 cache-images: $(grep 'budget:' "${DD}/d17.out" || tail -3 "${DD}/d17.out" | tr '\n' '|') -- the deadline waited for the downloads"
 7575  dfake_images; printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7576  treset; printf 'ok\n' > "${TR}/helper-plan"; echo ok > "${TR}/images-mode"; rm -f "${TR}/images-calls"
 7577  tctl scan
 7578  grep -q '^start [0-9.]* budget=[0-9][0-9]* --seconds [0-9][0-9]*' "${TR}/images-calls"; check $? "#308 gpt F-RA-10 ctl: the scan's image pass runs under a process bound ($(sed -n 's/^start [0-9.]* \(budget=[0-9]* --seconds [0-9]*\).*/\1/p' "${TR}/images-calls" | head -n 1))" "#308 gpt F-RA-10 ctl: the scan's image pass: $(tr '\n' '|' < "${TR}/images-calls" 2>/dev/null | cut -c1-160) -- no bound but the helper's own"
 7579  rm -f "${TR}/images-calls"
 7580  tctl images
 7581  [ "${RC}" -eq 0 ] && grep -q '^start [0-9.]* budget=[0-9][0-9]* --seconds [0-9][0-9]*' "${TR}/images-calls"; check $? "#308 gpt F-RA-10 ctl: the images verb's helper runs under a process bound" "#308 gpt F-RA-10 ctl: images rc ${RC}: $(tr '\n' '|' < "${TR}/images-calls" 2>/dev/null | cut -c1-160)"
 7582  cat > "${T}/repo/raofflineproxy-refresh" <<'EOS'
 7583  #!/bin/bash
 7584  echo "budget=${FAKE_BUDGET:-none} $*" > /run/refresh-calls
 7585  EOS
 7586  chmod +x "${T}/repo/raofflineproxy-refresh"; rm -f "${TR}/refresh-calls"
 7587  tctl refresh --all
 7588  [ "${RC}" -eq 0 ] && grep -q '^budget=[0-9][0-9]* --seconds [0-9][0-9]* --all$' "${TR}/refresh-calls"; check $? "#308 gpt F-RA-10 ctl: the refresh verb's helper runs under a process bound ($(cat "${TR}/refresh-calls" 2>/dev/null))" "#308 gpt F-RA-10 ctl: refresh rc ${RC}: $(cat "${TR}/refresh-calls" 2>/dev/null) -- no bound but the helper's own"
 7589  rm -f "${TR}/images-mode" "${TR}/images-calls" "${TR}/refresh-calls" "${TR}/helper-plan"
 7590  else
 7591      skip "#308 F-RA-10's ctl cases: section t did not run"
 7592  fi
 7593  
 7594  # D18. #308 1-raoffline claude F-RA-07: the ctl's own reads of the proxy's
 7595  # store -- pending, pending-ids, account and summary -- are run here against
 7596  # a store the pinned client made (its Storage, at the commit package.mk
 7597  # pins, patches applied), so a schema the client changes shows here as a
 7598  # FAIL, not as cannot_tell on a device. The header names the pin it was last
 7599  # read against, and D3 runs summary and pending-ids on the same kind of store.
 7600  if [ "${DT_OK}" -eq 1 ]; then
 7601  printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7602  treset; PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
 7603  from raofflineproxy import cache_keys
 7604  from raofflineproxy.storage import Storage
 7605  s = Storage()
 7606  s.upsert_cache(cache_keys.login("qa"), '{"Success":true,"User":"QA","Token":"planted","Score":1234,"SoftcoreScore":56}')
 7607  s.upsert_pending_award({"achievementId": 4242, "queryString": "/dorequest.php?r=awardachievement&u=QA&a=4242&h=0", "requestBody": "", "userAgent": "ra", "queuedAt": 1789400000000})
 7608  s.close()
 7609  EOS
 7610  tctl pending; DPR=${RC}; DPO="$(cat "${OUT}")"
 7611  tctl pending-ids; DIR=${RC}; DIO="$(cat "${OUT}")"
 7612  tctl account; DAR=${RC}; DAO="$(cat "${OUT}")"
 7613  tctl summary; DSR=${RC}
 7614  [ "${DPR}" -eq 0 ] && [ "${DPO}" = "1" ] && [ "${DIR}" -eq 0 ] && [ "${DIO}" = "4242 1789400000" ] && [ "${DAR}" -eq 0 ] && [ "${DAO}" = "score=1234 softcore=56" ] && [ "${DSR}" -eq 0 ] && ! grep -q 'planted' "${OUT}"; check $? "#308 claude F-RA-07: pending, pending-ids, account and summary read a store the pinned client's Storage wrote (1 / 4242 1789400000 / score=1234 softcore=56 / exit 0), the token never printed" "#308 claude F-RA-07: pending rc ${DPR} '${DPO}'; pending-ids rc ${DIR} '${DIO}'; account rc ${DAR} '${DAO}'; summary rc ${DSR} -- the ctl's SQL no longer fits the client's schema"
 7615  src_of "${CTL_REL}" "${DD}/ctl-header"
 7616  DPINHDR="$(sed -n '1,/^\. \/etc\/profile$/p' "${DD}/ctl-header" | grep -o 'package.mk pins ([0-9a-f]\{40\}' | head -n 1 | grep -o '[0-9a-f]\{40\}')"
 7617  [ -n "${DPINHDR}" ] && [ "${DPINHDR}" = "${PIN}" ]; check $? "#308 claude F-RA-07 / gpt F-RA-28: the ctl's header names the pin package.mk pins (${PIN:0:10}) as the schema it was read against" "#308 F-RA-07/28: the header names '${DPINHDR:-nothing}', package.mk pins ${PIN}"
 7618  else
 7619      skip "#308 F-RA-07's case: section t did not run"
 7620  fi
 7621  
 7622  # D19. Follow-up to #307 PL-060 (the coordinator, 2026-09-28): a badge the
 7623  # RetroAchievements image server does not have -- 404 or 410, a permanent
 7624  # "not there" -- is recorded as absent, is not asked for again, and does not
 7625  # fail the run; a transient failure (a timeout, a 5xx, a refused connection,
 7626  # a short read) still fails it with SOME_IMAGES_NOT_SAVED and is tried again
 7627  # next time. download_static_image says which, and logs the URL's outcome
 7628  # class with the HTTP status, where it used to swallow the reason (patch
 7629  # 016). First on the patched client; then a scan through the ctl with the
 7630  # real image helper beside it and the image server answered from a plan
 7631  # (/run/image-plan, read by a hook in section t's sitecustomize).
 7632  if [ "${DT_OK}" -eq 1 ]; then
 7633  RAOFFLINEPROXY_CONFIG_DIR="${DD}/d19-cfg" PYTHONPATH="${CLIENT}" python3 - > "${DD}/d19.out" 2>&1 <<'EOS'
 7634  import io, logging, os, struct, urllib.error, zlib
 7635  from pathlib import Path
 7636  Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
 7637  from raofflineproxy import image_cache
 7638  def _chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
 7639  PNG = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + _chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00")) + _chunk(b"IEND", b"")
 7640  log = io.StringIO(); handler = logging.StreamHandler(log)
 7641  logger = logging.getLogger("raofflineproxy"); logger.addHandler(handler); logger.setLevel(logging.INFO)
 7642  def answer(kind):
 7643      def fetch(url, user_agent):
 7644          if kind.isdigit():
 7645              raise urllib.error.HTTPError(url, int(kind), "status", {}, None)
 7646          if kind == "timeout":
 7647              raise TimeoutError("timed out")
 7648          return PNG
 7649      return fetch
 7650  got = {}
 7651  saved = image_cache._fetch_image
 7652  try:
 7653      for kind in ("404", "410", "503", "timeout", "ok"):
 7654          image_cache._fetch_image = answer(kind)
 7655          got[kind] = image_cache.download_static_image(f"https://media.retroachievements.org/Badge/d19-{kind}.png", f"/Badge/d19-{kind}.png", "ua")
 7656  finally:
 7657      image_cache._fetch_image = saved
 7658  text = log.getvalue()
 7659  ok = got == {"404": "absent", "410": "absent", "503": "transient", "timeout": "transient", "ok": "cached"}
 7660  print(("PASS" if ok else "FAIL") + f" outcome: {got}")
 7661  ok = all(s in text for s in ("absent", "HTTP 404", "HTTP 410", "HTTP 503", "https://media.retroachievements.org/Badge/d19-404.png", "transient"))
 7662  print(("PASS" if ok else "FAIL") + " logged: " + " | ".join(l for l in text.splitlines() if "d19-" in l)[:400])
 7663  EOS
 7664  grep -q '^PASS outcome:' "${DD}/d19.out"; check $? "PL-060 follow-up, patch 016: download_static_image says what became of an image -- 404 and 410 absent, a 503 and a timeout transient, a whole PNG cached" "PL-060 follow-up, patch 016: $(grep 'outcome:' "${DD}/d19.out" || tail -3 "${DD}/d19.out" | tr '\n' '|') -- the reason was swallowed"
 7665  grep -q '^PASS logged:' "${DD}/d19.out"; check $? "PL-060 follow-up, patch 016: the outcome class, the HTTP status and the URL are logged" "PL-060 follow-up, patch 016: $(grep 'logged:' "${DD}/d19.out" | cut -c1-300 || echo 'no verdict')"
 7666  # Through the ctl: the real helper beside it, the image server a plan.
 7667  src_of "projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images" "${T}/repo/raofflineproxy-cache-images"; chmod +x "${T}/repo/raofflineproxy-cache-images"
 7668  grep -q 'image-plan' "${T}/pypath/sitecustomize.py" || cat >> "${T}/pypath/sitecustomize.py" <<'EOS'
 7669  if os.path.exists("/run/image-plan"):
 7670      import json as _json, struct as _struct, urllib.error as _ue, zlib as _zlib
 7671      import raofflineproxy.auth as _auth
 7672      import raofflineproxy.image_cache as _ic
 7673      _auth.resolve_credentials = lambda *a, **k: {"user": "qa", "token": "t"}
 7674      def _chunk(t, d): return _struct.pack(">I", len(d)) + t + d + _struct.pack(">I", _zlib.crc32(t + d) & 0xFFFFFFFF)
 7675      _PNG = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", _struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + _chunk(b"IDAT", _zlib.compress(b"\x00\xff\x00\x00")) + _chunk(b"IEND", b"")
 7676      def _fetch(url, user_agent):
 7677          path = "/" + url.split("://", 1)[-1].split("/", 1)[-1]
 7678          with open("/run/image-fetches", "a") as f:
 7679              f.write(path + "\n")
 7680          what = _json.load(open("/run/image-plan")).get(path, "ok")
 7681          if what.isdigit():
 7682              raise _ue.HTTPError(url, int(what), "status", {}, None)
 7683          if what == "timeout":
 7684              raise TimeoutError("timed out")
 7685          return _PNG
 7686      _ic._fetch_image = _fetch
 7687  EOS
 7688  printf "${DCFG_ON}" > "${TCFG}"; TENV=()
 7689  treset; PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
 7690  import json
 7691  from raofflineproxy import cache_keys
 7692  from raofflineproxy.storage import Storage
 7693  s = Storage()
 7694  badges = [{"ID": 9300 + i, "Flags": 3, "BadgeURL": f"https://media.retroachievements.org/Badge/{9300 + i}.png"} for i in (1, 2, 3, 4)]
 7695  s.upsert_cache(cache_keys.patch(102, "qa"), json.dumps({"Success": True, "PatchData": {"ID": 102, "Achievements": badges}}), source_rom_path="/nes/b.nes")
 7696  s.close()
 7697  EOS
 7698  # Resolve the writer's current sharded paths; removing only the legacy path
 7699  # would leave a cache hit and never exercise the timeout/retry below (#361).
 7700  mapfile -t D19_IMAGES < <(PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
 7701  from raofflineproxy import image_cache
 7702  for badge in (9301, 9302, 9304):
 7703      print(image_cache.sharded_static_path(f"Badge/{badge}.png"))
 7704  EOS
 7705  )
 7706  D19_ABSENT=${D19_IMAGES[0]}; D19_OK=${D19_IMAGES[1]}; D19_RETRY=${D19_IMAGES[2]}
 7707  # 9301 404, 9303 410, 9302 and 9304 served.
 7708  echo '{"/Badge/9301.png": "404", "/Badge/9303.png": "410"}' > "${TR}/image-plan"; : > "${TR}/image-fetches"
 7709  tctl scan
 7710  [ "${RC}" -eq 0 ] && ! grep -q '>>> why' "${OUT}" && [ -s "${D19_OK}" ] && [ ! -e "${D19_ABSENT}" ]; check $? "PL-060 follow-up: a scan whose image server answers 404 and 410 for two badges completes (rc 0, no why) -- they are absent, not a failure of the run" "PL-060 follow-up: rc ${RC}; out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | cut -c1-200); stamp: $(cat "${TSTAMP}" 2>/dev/null) -- a badge the server does not have failed the scan"
 7711  : > "${TR}/image-fetches"
 7712  tctl scan
 7713  [ "${RC}" -eq 0 ] && ! grep -qx '/Badge/9301.png' "${TR}/image-fetches" && ! grep -qx '/Badge/9303.png' "${TR}/image-fetches"; check $? "PL-060 follow-up: the next scan does not ask for the absent badges again (rc ${RC})" "PL-060 follow-up: rc ${RC}; requested: $(tr '\n' ' ' < "${TR}/image-fetches") -- an absent badge was asked for at every pass"
 7714  # A timeout and a 503: a failure of the run, not recorded as absent, asked again.
 7715  rm -f "${D19_OK}" "${D19_RETRY}"
 7716  echo '{"/Badge/9301.png": "404", "/Badge/9302.png": "timeout", "/Badge/9303.png": "410", "/Badge/9304.png": "503"}' > "${TR}/image-plan"; : > "${TR}/image-fetches"
 7717  tctl scan
 7718  [ "${RC}" -eq 1 ] && grep -qx '>>> why SOME_IMAGES_NOT_SAVED' "${OUT}" && grep -q ' 1 scan .*why=SOME_IMAGES_NOT_SAVED$' "${TSTAMP}"; check $? "PL-060 follow-up: a badge that timed out and one the server answered 503 end the scan COULDN'T FINISH (rc 1, why SOME_IMAGES_NOT_SAVED)" "PL-060 follow-up: rc ${RC}; out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | cut -c1-200)"
 7719  : > "${TR}/image-fetches"; echo '{"/Badge/9301.png": "404", "/Badge/9303.png": "410"}' > "${TR}/image-plan"
 7720  tctl scan
 7721  [ "${RC}" -eq 0 ] && grep -qx '/Badge/9302.png' "${TR}/image-fetches" && grep -qx '/Badge/9304.png' "${TR}/image-fetches" && [ -s "${D19_OK}" ] && [ -s "${D19_RETRY}" ]; check $? "PL-060 follow-up: the next scan asks for the timed-out and the 503 badges again, and with the server answering, completes" "PL-060 follow-up: rc ${RC}; requested: $(tr '\n' ' ' < "${TR}/image-fetches")"
 7722  rm -f "${TR}/image-plan" "${TR}/image-fetches"; dfake_images
 7723  else
 7724      skip "the PL-060 follow-up's cases: section t did not run"
 7725  fi
 7726  
 7727  # D20. #308 1-raoffline claude F-RA-17's part in this file: the usage line
 7728  # names every verb the ctl answers -- summary was missing from it.
 7729  if [ "${DT_OK}" -eq 1 ]; then
 7730  tctl no-such-verb
 7731  [ "${RC}" -eq 2 ] && grep -q '|summary|' "${ERR}"; check $? "#308 claude F-RA-17: the usage line names summary with the other verbs" "#308 claude F-RA-17: rc ${RC}; usage: $(head -c 300 "${ERR}")"
 7732  fi
 7733  
 7734  # D21. #308 1-raoffline claude F-RA-17's remaining parts in this package:
 7735  # raofflineproxy-cache-images read the whole store once more before --verify
 7736  # and threw the answer away ("warm the same read"); its -h printed
 7737  # `__doc__ or "usage: ... [--seconds N]"` from a file with no docstring, so
 7738  # the help left out --verify; and raofflineproxy-cache-indexed, which is
 7739  # executed, was mode 100644 among 100755 siblings.
 7740  if [ "${DT_OK}" -eq 1 ]; then
 7741  RAOFFLINEPROXY_CONFIG_DIR="${DD}/d21-cfg" PYTHONPATH="${CLIENT}" python3 - "${DD}/raofflineproxy-cache-images" > "${DD}/d21.out" 2>&1 <<'EOS'
 7742  import contextlib, io, os, sys, importlib.machinery, importlib.util
 7743  from pathlib import Path
 7744  Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
 7745  spec = importlib.util.spec_from_loader("images_helper", importlib.machinery.SourceFileLoader("images_helper", sys.argv[1]))
 7746  helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
 7747  from raofflineproxy import cache_keys
 7748  from raofflineproxy.storage import Storage
 7749  st = Storage(); st.upsert_cache(cache_keys.patch(1, "qa"), '{"Success":true,"PatchData":{"ID":1,"Achievements":[]}}'); st.close()
 7750  helper.resolve_credentials = lambda *a, **k: {"user": "qa", "token": "t"}
 7751  walks = []
 7752  real = helper.missing_paths
 7753  helper.missing_paths = lambda storage: walks.append(1) or real(storage)
 7754  sys.argv = ["raofflineproxy-cache-images", "--seconds", "5", "--verify"]
 7755  with contextlib.redirect_stdout(io.StringIO()):
 7756      rc = helper.main()
 7757  print(("PASS" if len(walks) == 1 else "FAIL") + f" walks: --verify walked the store's missing images {len(walks)} time(s), rc {rc}")
 7758  buf = io.StringIO()
 7759  sys.argv = ["raofflineproxy-cache-images", "-h"]
 7760  with contextlib.redirect_stdout(buf):
 7761      rc = helper.main()
 7762  text = buf.getvalue()
 7763  print(("PASS" if rc == 0 and "--seconds" in text and "--verify" in text else "FAIL") + " help: " + " | ".join(text.strip().splitlines()[:2])[:200])
 7764  EOS
 7765  grep -q '^PASS walks:' "${DD}/d21.out"; check $? "#308 claude F-RA-17: --verify walks the store once, not once more to throw away" "#308 claude F-RA-17: $(grep 'walks:' "${DD}/d21.out" || tail -3 "${DD}/d21.out" | tr '\n' '|')"
 7766  grep -q '^PASS help:' "${DD}/d21.out"; check $? "#308 claude F-RA-17: cache-images -h names --seconds and --verify (a docstring of its own)" "#308 claude F-RA-17: $(grep 'help:' "${DD}/d21.out" || tail -3 "${DD}/d21.out" | tr '\n' '|')"
 7767  fi
 7768  # The helpers the ctl runs are executable in the tree (the index's mode, or
 7769  # BASE_REF's under --old), as package.mk installs them.
 7770  DMODES=""
 7771  for h in raofflineproxy-ctl raofflineproxy-cache-indexed raofflineproxy-cache-images raofflineproxy-refresh; do
 7772      rel="projects/ROCKNIX/packages/network/raofflineproxy/sources/${h}"
 7773      if [ "${OLD}" -eq 1 ]; then m="$(git -C "${ROOT}" ls-tree "${BASE_REF}" -- "${rel}" | awk '{print $1}')"; else m="$(git -C "${ROOT}" ls-files -s -- "${rel}" | awk '{print $1}')"; fi
 7774      DMODES="${DMODES} ${h}=${m:-none}"
 7775  done
 7776  ! printf '%s' "${DMODES}" | grep -q '=\(100644\|none\)'; check $? "#308 claude F-RA-17: the four scripts under sources/ are mode 100755 in the tree" "#308 claude F-RA-17: modes:${DMODES}"
 7777  # ---- audit #307, stream B ----
 7778  # Stream B's cases for audit #307's punch list and #308's sweep, in the
 7779  # files the stream owns: backuptool, wifictl, 001-functions (the settings
 7780  # writer, the lock, the redaction), factoryreset, chksysconfig,
 7781  # rocknix-evidence, rocknix-corekeep, runemu.sh and automount. Every case
 7782  # names its item (#307 PL-NNN, or #308 <packet> <seat> <id>) and was seen to
 7783  # FAIL against the script before its fix. Which tools each part runs under,
 7784  # when the image's busybox is found (BB): backuptool (y1) whole under bwrap
 7785  # with the image's tar, unzip, crc32, find, readlink, mktemp, flock, stat, mv, cp,
 7786  # ln, touch, chmod, sed, awk, head, tail, wc, cut, tr, cmp, dirname,
 7787  # basename, mkdir, rm and date; the evidence collector and the core keeper
 7788  # (y4) whole under bwrap with the image's applets for every one they call,
 7789  # which a check in y4 proves by asking each for its banner (the audit of the
 7790  # fixes, gpt G-B-15: they ran on the host's until then); wifictl (y2), the
 7791  # settings writer, lock and redaction (y3), chksysconfig's functions,
 7792  # factoryreset and automount's disk test (y4) with the harness's bbin (sed,
 7793  # mv, cp, tr, head, wc, cut, awk) first on PATH and the host's for the rest;
 7794  # the runemu parsers are bash alone.
 7795  # grep, sort and gzip are the device's GNU ones, the host's here.
```

## Excerpt: F-09: y/A (`:10120-10365` at 8ebaf8daad)

```text
10120  # The scan ran its image pass only when it had cached a game: a library with
10121  # one ROM RetroAchievements does not know lists a job at every scan, every
10122  # job skipped, and the scan stamped COMPLETED over badges it never looked at.
10123  # The pass now runs whenever the run worked through its jobs (not when it
10124  # stopped on a refused sign-in or a server that stopped answering). And a
10125  # top-up that reaches its image pass with ten seconds or less of its
10126  # deadline left says it did not get to it (TOOK_TOO_LONG), where it said
10127  # COMPLETED over images nobody checked.
10128  if [ "${DT_OK}" -eq 1 ]; then
10129  dfake_images; printf "${DCFG_ON}" > "${TCFG}"; TENV=()
10130  treset; for _ in 1 2 3 4; do echo skip; done > "${TR}/helper-plan"; echo fail > "${TR}/images-mode"; rm -f "${TR}/images-calls"
10131  tctl scan
10132  [ "${RC}" -eq 1 ] && grep -qx '>>> why SOME_IMAGES_NOT_SAVED' "${OUT}" && grep -q '^start' "${TR}/images-calls" 2>/dev/null; check $? "gpt G-D-01 / claude G-D-02: a scan whose jobs were all skipped still runs the image pass, and its failure is the run's (rc 1, SOME_IMAGES_NOT_SAVED)" "G-D-01/02: rc ${RC}; image pass run: $(grep -c '^start' "${TR}/images-calls" 2>/dev/null || echo 0) time(s); out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | cut -c1-200) -- COMPLETED over images nobody looked at"
10133  treset; for _ in 1 2 3 4; do echo skip; done > "${TR}/helper-plan"; echo ok > "${TR}/images-mode"; rm -f "${TR}/images-calls"
10134  tctl scan
10135  [ "${RC}" -eq 0 ] && grep -q '^start' "${TR}/images-calls" 2>/dev/null; check $? "gpt G-D-01 / claude G-D-02: and with the pass fetching what was missing, that scan completes (rc 0)" "G-D-01/02: rc ${RC}; image pass run: $(grep -c '^start' "${TR}/images-calls" 2>/dev/null || echo 0)"
10136  # The top-up with seven seconds left at its image pass.
10137  treset; touch -d '2 hours ago' "${TMARK}"; printf 'ok\nslow 893\n' > "${TR}/helper-plan"; echo ok > "${TR}/images-mode"; rm -f "${TR}/images-calls"
10138  tctl topup --after-index
10139  [ "${RC}" -eq 1 ] && grep -q ' 1 topup cached=2 .*why=TOOK_TOO_LONG$' "${TSTAMP}" && [ ! -e "${TR}/images-calls" ]; check $? "gpt G-D-01: a top-up with seven seconds left at its image pass ends rc 1, why TOOK_TOO_LONG -- the images were not checked" "gpt G-D-01: rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null); image pass: $(grep -c '^start' "${TR}/images-calls" 2>/dev/null || echo 0) -- a pass that never ran read as done"
10140  rm -f "${TR}/helper-plan" "${TR}/images-mode" "${TR}/images-calls"
10141  fi
10142  
10143  # D23. claude G-D-03: the shipped topology of a cancel during the image pass,
10144  # under the real timeout rather than the harness's shim. GNU timeout puts
10145  # itself and the helper in a process group of their own, so the interface's
10146  # SIGINT to the run's group reaches the ctl and not the helper; the ctl's INT
10147  # trap stamps CANCELLED, and its EXIT trap ends the helper by SIGTERM
10148  # through timeout. The run is started as the interface starts it -- a
10149  # session and a process group of its own (setsid) -- and the stand-in sends
10150  # the group SIGINT itself.
10151  # The image's timeout is GNU coreutils' (9.4); this host's `timeout` may be
10152  # another implementation (uutils), so GNU's is found by name.
10153  DGNU=""; for c in gnutimeout timeout; do command -v "${c}" >/dev/null && "${c}" --version 2>/dev/null | head -n 1 | grep -q 'GNU coreutils' && { DGNU="$(command -v "${c}")"; break; }; done
10154  if [ "${DT_OK}" -eq 1 ] && [ -n "${DGNU}" ]; then
10155  dfake_images; printf "${DCFG_ON}" > "${TCFG}"; TENV=()
10156  mv "${T}/shim/timeout" "${T}/shim/timeout.shim"
10157  printf '#!/bin/sh\nexec %s "$@"\n' "${DGNU}" > "${T}/shim/timeout"; chmod +x "${T}/shim/timeout"
10158  treset; printf 'ok\n' > "${TR}/helper-plan"; echo group-cancel > "${TR}/images-mode"; rm -f "${TR}/images-calls" "${TR}/images.pid"
10159  DT0=$(dnow)
10160  RC=$( ( bwrap --die-with-parent --tmpfs / --tmpfs /usr "${USR_BINDS[@]}" "${TBB[@]}" \
10161      --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
10162      --ro-bind /etc /etc --ro-bind "${T}/profile" /etc/profile \
10163      --bind "${TS}" /storage --ro-bind "${T}/repo" /repo --ro-bind "${T}/shim" /shim --ro-bind "${CLIENT}" /client --ro-bind "${T}/pypath" /pypath \
10164      --bind "${TR}" /run --tmpfs /var --bind "${T}/varrun" /var/run \
10165      --dev /dev --proc /proc --tmpfs /tmp --setenv PYTHONPATH /client:/pypath \
10166      setsid -w bash /repo/raofflineproxy-ctl scan > "${OUT}" 2> "${ERR}"; echo $? ) 2>/dev/null )
10167  DEND=$(dnow)
10168  mv -f "${T}/shim/timeout.shim" "${T}/shim/timeout"
10169  DI0="$(sed -n 's/^start \([0-9.]*\).*/\1/p' "${TR}/images-calls" 2>/dev/null | head -n 1)"
10170  IP="$(cat "${TR}/images.pid" 2>/dev/null)"; for _ in $(seq 1 30); do kill -0 "${IP:-1}" 2>/dev/null || break; sleep 0.1; done
10171  [ "${RC}" -eq 130 ] && grep -qx '>>> why CANCELLED' "${OUT}" && [ -n "${DI0}" ] && awk -v a="${DI0}" -v b="${DEND}" 'BEGIN{exit !(b - a < 3)}' && grep -q '^term ' "${TR}/images-calls" && ! grep -q '^int ' "${TR}/images-calls" && ! kill -0 "${IP:-1}" 2>/dev/null; check $? "claude G-D-03: under the real timeout the group's SIGINT reaches the ctl, not the helper; the run is CANCELLED (rc 130) $(awk -v a="${DI0:-0}" -v b="${DEND}" 'BEGIN{printf "%.2f", b - a}')s after the pass began and the helper is ended by SIGTERM through timeout" "claude G-D-03: rc ${RC}; the helper saw: $(tr '\n' ' ' < "${TR}/images-calls" 2>/dev/null | cut -c1-200); $(awk -v a="${DI0:-0}" -v b="${DEND}" 'BEGIN{printf "%.2f", b - a}')s; out: $(grep '^>>>' "${OUT}" | tail -n 2 | tr '\n' '|')"
10172  [ -n "${IP}" ] && kill -9 "${IP}" 2>/dev/null; rm -f "${TR}/images-mode" "${TR}/helper-plan"
10173  else
10174      skip "claude G-D-03's case: needs section t and GNU coreutils' timeout on this machine"
10175  fi
10176  
10177  # D24. claude G-D-04: patch 016's classification against the real
10178  # _fetch_image and a real HTTP server on loopback -- 404, 410, a 301 to
10179  # a 404, a 503, a refused connection and a whole PNG -- not a stubbed
10180  # fetcher. And claude G-D-12: an image already in the cache is "cached" (the
10181  # function falls through its `if not target.exists()` to the one return).
10182  if [ "${DT_OK}" -eq 1 ]; then
10183  RAOFFLINEPROXY_CONFIG_DIR="${DD}/d24-cfg" PYTHONPATH="${CLIENT}" python3 - > "${DD}/d24.out" 2>&1 <<'EOS'
10184  import http.server, os, socket, struct, threading, zlib
10185  from pathlib import Path
10186  Path(os.environ["RAOFFLINEPROXY_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
10187  from raofflineproxy import image_cache
10188  def _chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
10189  PNG = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)) + _chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00")) + _chunk(b"IEND", b"")
10190  class Handler(http.server.BaseHTTPRequestHandler):
10191      def log_message(self, *a): pass
10192      def do_GET(self):
10193          name = self.path.rsplit("/", 1)[-1]
10194          if name == "ok.png":
10195              self.send_response(200); self.send_header("Content-Length", str(len(PNG))); self.end_headers(); self.wfile.write(PNG); return
10196          if name == "short.png":
10197              self.send_response(200); self.send_header("Content-Length", str(len(PNG) + 8)); self.end_headers(); self.wfile.write(PNG); self.close_connection = True; return
10198          if name == "moved.png":
10199              self.send_response(301); self.send_header("Location", "/Badge/gone404.png"); self.send_header("Content-Length", "0"); self.end_headers(); return
10200          code = {"gone404.png": 404, "gone410.png": 410, "busy503.png": 503}.get(name, 404)
10201          self.send_response(code); self.send_header("Content-Length", "0"); self.end_headers()
10202  server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
10203  threading.Thread(target=server.serve_forever, daemon=True).start()
10204  base = f"http://127.0.0.1:{server.server_address[1]}"
10205  closed = socket.socket(); closed.bind(("127.0.0.1", 0)); dead = closed.getsockname()[1]; closed.close()
10206  got = {}
10207  for name in ("gone404", "gone410", "moved", "busy503", "ok", "short"):
10208      got[name] = image_cache.download_static_image(f"{base}/Badge/{name}.png", f"/Badge/d24-{name}.png", "ua")
10209  got["refused"] = image_cache.download_static_image(f"http://127.0.0.1:{dead}/Badge/refused.png", "/Badge/d24-refused.png", "ua")
10210  want = {"gone404": "absent", "gone410": "absent", "moved": "absent", "busy503": "transient", "ok": "cached", "refused": "transient", "short": "transient"}
10211  print(("PASS" if got == want else "FAIL") + f" real: {got}")
10212  seeded = image_cache.STATIC_DIR / "Badge" / "d24-seeded.png"; seeded.parent.mkdir(parents=True, exist_ok=True); seeded.write_bytes(PNG)
10213  there = image_cache.download_static_image(f"http://127.0.0.1:{dead}/Badge/seeded.png", "/Badge/d24-seeded.png", "ua")
10214  print(("PASS" if there == "cached" else "FAIL") + f" there: an image already cached returned {there!r}")
10215  server.shutdown()
10216  EOS
10217  grep -q '^PASS real:' "${DD}/d24.out"; check $? "claude G-D-04: against a real HTTP server and the real fetcher, 404, 410 and a 301 to a 404 are absent; a 503 and a refused connection transient; a whole PNG cached" "claude G-D-04: $(grep 'real:' "${DD}/d24.out" || tail -3 "${DD}/d24.out" | tr '\n' '|')"
10218  grep -q '^PASS there:' "${DD}/d24.out"; check $? "claude G-D-12: an image already in the cache returns cached" "claude G-D-12: $(grep 'there:' "${DD}/d24.out" || tail -3 "${DD}/d24.out" | tr '\n' '|')"
10219  fi
10220  
10221  # D25. claude G-D-05: the start limit bounds a proxy that never listens. A
10222  # failed start now lasts the readiness wait plus RestartSec, so the limit's
10223  # interval has to hold StartLimitBurst of them, or five-in-sixty never trips
10224  # and the unit restarts for ever.
10225  DU="${DD}/raofflineproxy.service"
10226  DIV="$(awk -F= '/^StartLimitIntervalSec=/{print $2}' "${DU}")"; DBU="$(awk -F= '/^StartLimitBurst=/{print $2}' "${DU}")"
10227  DRS="$(awk -F= '/^RestartSec=/{print $2}' "${DU}")"; DWA="$(sed -n 's/^ExecStartPost=.* --wait \([0-9]*\)$/\1/p' "${DU}")"
10228  [ -n "${DIV}" ] && [ -n "${DBU}" ] && [ -n "${DRS}" ] && [ -n "${DWA}" ] && [ "${DIV%s}" -ge $(( DBU * (DWA + ${DRS%s}) )) ]; check $? "claude G-D-05: the start limit's interval (${DIV}s) holds its burst of failed starts (${DBU} x (wait ${DWA}s + RestartSec ${DRS}s) = $(( ${DBU:-0} * (${DWA:-0} + ${DRS:-0}) ))s)" "claude G-D-05: StartLimitIntervalSec=${DIV:-?} < StartLimitBurst=${DBU:-?} x (--wait ${DWA:-?} + RestartSec=${DRS:-?}) -- five in sixty never trips"
10229  
10230  # D26. claude G-D-06 and gpt G-D-06: the scan's cursor is the walk's promise
10231  # to continue, so it moves only when kept: the listing proposes it
10232  # (scan-cursor.next), and the run commits it once it has worked through its
10233  # jobs (the helper's DONE) -- a scan cancelled after its listing starts the
10234  # next one where it started -- and a cursor that could not be written is
10235  # said, not passed over: the run ends COULDN'T FINISH (SOMETHING_WENT_WRONG)
10236  # with no TRUNCATED promise, and the cursor that was there stays.
10237  if [ "${DT_OK}" -eq 1 ]; then
10238  dfake_images; printf "${DCFG_ON}" > "${TCFG}"
10239  dgbc() { rm -rf "${TS}/roms/gbc"; mkdir -p "${TS}/roms/gbc"; for i in $(seq -w 1 11); do printf 'GBC %s' "${i}" > "${TS}/roms/gbc/g${i}.gbc"; done; }
10240  treset; dgbc; TENV=(--setenv RA_TEST_SCAN_CAP 10)
10241  { echo skip; echo cancel; } > "${TR}/helper-plan"; : > "${TR}/helper-jobs.log"
10242  tctl scan; grep '^H' "${TR}/helper-jobs.log" | sort > "${DD}/d26-1.jobs"
10243  for _ in $(seq 1 20); do echo skip; done > "${TR}/helper-plan"; : > "${TR}/helper-jobs.log"
10244  tctl scan; grep '^H' "${TR}/helper-jobs.log" | sort > "${DD}/d26-2.jobs"
10245  cmp -s "${DD}/d26-1.jobs" "${DD}/d26-2.jobs"; check $? "claude G-D-06: a scan cancelled after its listing does not move the cursor -- the next scan takes the same slice" "claude G-D-06: after a cancelled scan the next took $(sed 's|.*/||' "${DD}/d26-2.jobs" | tr '\n' ' ')against $(sed 's|.*/||' "${DD}/d26-1.jobs" | tr '\n' ' ')-- the cursor moved at the listing"
10246  # A cursor that cannot be written: scan-cursor is a directory.
10247  treset; dgbc; rm -rf "${TPD}/scan-cursor"; mkdir -p "${TPD}/scan-cursor"
10248  for _ in $(seq 1 20); do echo skip; done > "${TR}/helper-plan"
10249  tctl scan
10250  [ "${RC}" -eq 1 ] && grep -qx '>>> why SOMETHING_WENT_WRONG' "${OUT}" && ! grep -q 'note TRUNCATED' "${OUT}"; check $? "gpt G-D-06: a truncated walk whose cursor cannot be saved ends rc 1, why SOMETHING_WENT_WRONG, and promises no continuation (no note TRUNCATED)" "gpt G-D-06: rc ${RC}; out: $(grep '^>>>' "${OUT}" | tr '\n' '|' | tail -c 200) -- a cursor write failure passed over"
10251  rm -rf "${TPD}/scan-cursor"
10252  # The proposal cannot be written: the cursor a previous scan kept stays.
10253  treset; dgbc; for _ in $(seq 1 20); do echo skip; done > "${TR}/helper-plan"
10254  tctl scan; DKEPT="$(cat "${TPD}/scan-cursor" 2>/dev/null)"
10255  rm -rf "${TPD}/scan-cursor.next"; mkdir -p "${TPD}/scan-cursor.next"
10256  tctl scan
10257  [ "${RC}" -eq 1 ] && [ -n "${DKEPT}" ] && [ "$(cat "${TPD}/scan-cursor" 2>/dev/null)" = "${DKEPT}" ]; check $? "gpt G-D-06: when the new cursor cannot be written the run ends rc 1 and the cursor the last scan kept stays (${DKEPT##*/})" "gpt G-D-06: rc ${RC}; cursor before '${DKEPT##*/}', after '$(cat "${TPD}/scan-cursor" 2>/dev/null | sed 's|.*/||')'"
10258  rm -rf "${TPD}/scan-cursor.next" "${TS}/roms/gbc"; TENV=(); rm -f "${TR}/helper-plan"
10259  fi
10260  
10261  # D27. claude G-D-07, a guard (the finding is refuted: EX_USAGE=64 is
10262  # defined in the ctl's sysexits block): `listening` with a wait that is not
10263  # a number is a usage error, exit 64, never 0.
10264  if [ "${DT_OK}" -eq 1 ]; then
10265  tctl listening --wait abc
10266  [ "${RC}" -eq 64 ] && grep -q '^usage: raofflineproxy-ctl listening' "${ERR}"; check $? "claude G-D-07: listening --wait abc -- usage on stderr, exit 64" "claude G-D-07: rc ${RC}; stderr: $(head -c 160 "${ERR}")"
10267  fi
10268  
10269  # D28. claude G-D-08, gpt G-D-04, gpt G-D-05: one definition of a game ready
10270  # for the account -- its unlocks row and an achievementsets row of the game,
10271  # the rows a launch reads -- behind both added= and the walk's "already
10272  # cached", read from the head of each sets row rather than a parse of every
10273  # body (a sets row whose GameId sits past the head still counts). A game a
10274  # launch cached (sets and unlocks, no patch) was ready before a top-up gave
10275  # it a patch row, so it is not "more". And the count of games made ready
10276  # fails closed: a comparison that could not be read is no count at all.
10277  if [ "${DT_OK}" -eq 1 ]; then
10278  printf "${DCFG_ON}" > "${TCFG}"; TENV=()
10279  GLSIZE=$(stat -c %s "${TS}/roms/nes/gamelist.xml")
10280  printf '<?xml version="1.0"?>\n<gameList parentHash="%s">\n  <game><path>./g.nes</path><name>G</name><cheevosHash>aaaa0201</cheevosHash><cheevosId>201</cheevosId></game>\n</gameList>\n' "${GLSIZE}" > "${TS}/.config/emulationstation/recovery/nes/g.xml"
10281  treset; touch -d '2 hours ago' "${TMARK}"; PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
10282  import json
10283  from raofflineproxy import cache_keys
10284  from raofflineproxy.storage import Storage
10285  s = Storage()
10286  # 201: a launch's rows (another dump's sets, the unlocks), no patch row; the
10287  # Title is long, so GameId sits past the first 512 bytes of the body.
10288  s.upsert_cache(cache_keys.achievementsets("feed0201", "qa"), json.dumps({"Success": True, "Title": "T" * 800, "GameId": 201, "Sets": []}))
10289  s.upsert_cache(cache_keys.unlocks(201, "qa"), '{"Success":true,"UserUnlocks":[]}')
10290  s.close()
10291  EOS
10292  : > "${TR}/helper-jobs.log"
10293  tctl topup --after-index
10294  [ "${RC}" -eq 0 ] && grep -qP '^I\t201\taaaa0201\t' "${TR}/helper-jobs.log" && grep -q ' 0 topup cached=3 .* added=2$' "${TSTAMP}"; check $? "gpt G-D-04: a game a launch had already cached (sets and unlocks, no patch row) is cached by the index and not counted as added -- cached=3 added=2" "gpt G-D-04: rc ${RC}; jobs: $(tr '\t' ',' < "${TR}/helper-jobs.log" | tr '\n' '|' | cut -c1-200); stamp: $(cat "${TSTAMP}" 2>/dev/null)"
10295  rm -f "${TS}/.config/emulationstation/recovery/nes/g.xml"
10296  # The walk's "already cached" is the same rule: patch and unlocks without a
10297  # sets row is a job; with the long-titled sets row it is not.
10298  treset; PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
10299  import json
10300  from raofflineproxy import cache_keys
10301  from raofflineproxy.storage import Storage
10302  s = Storage()
10303  s.upsert_cache(cache_keys.patch(152, "qa"), '{"Success":true,"PatchData":{"ID":152}}', source_rom_path="/gb/h.gb")
10304  s.upsert_cache(cache_keys.unlocks(152, "qa"), '{"Success":true,"UserUnlocks":[]}')
10305  s.upsert_cache(cache_keys.patch(153, "qa"), '{"Success":true,"PatchData":{"ID":153}}', source_rom_path="/gb/i.gb")
10306  s.upsert_cache(cache_keys.unlocks(153, "qa"), '{"Success":true,"UserUnlocks":[]}')
10307  s.upsert_cache(cache_keys.achievementsets("iiii", "qa"), json.dumps({"Success": True, "Title": "T" * 800, "GameId": 153, "Sets": []}))
10308  s.close()
10309  EOS
10310  : > "${TR}/helper-jobs.log"; dfake_images
10311  tctl scan
10312  grep -qP '^H\t\t\t/storage/roms/gb/h.gb$' "${TR}/helper-jobs.log" && ! grep -q '/storage/roms/gb/i.gb$' "${TR}/helper-jobs.log"; check $? "claude G-D-08: the walk's rule is the same -- patch and unlocks with no sets row is a job; a sets row whose GameId lies past the head still makes the game whole" "claude G-D-08: jobs: $(tr '\t' ',' < "${TR}/helper-jobs.log" | tr '\n' '|' | cut -c1-200)"
10313  fi
10314  # games_made_ready, lifted from the ctl: a before file that cannot be read.
10315  src_of "${CTL_REL:-projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl}" "${DD}/ctl-for-gmr"
10316  sed -n '/^games_made_ready() {/,/^}/p' "${DD}/ctl-for-gmr" > "${DD}/gmr.sh"
10317  mkdir -p "${DD}/gmr-dir"; printf '101\n102\n' > "${DD}/gmr-after"
10318  DGM="$(bash -c ". '${DD}/gmr.sh'; games_made_ready '${DD}/gmr-dir' '${DD}/gmr-after'"; echo "rc=$?")"
10319  [ -s "${DD}/gmr.sh" ] && [ "${DGM}" = "rc=1" ]; check $? "gpt G-D-05: games_made_ready with a before file that cannot be read prints nothing and fails, so the caller keeps its own count" "gpt G-D-05: it answered '$(printf '%s' "${DGM}" | tr '\n' ' ')' -- a failed comparison read as a count"
10320  
10321  # D29. gpt G-D-03: the top-up removes index-pending only if it is the
10322  # marker its listing was made for -- one an index writes while the run is at
10323  # its jobs is a newer promise, and it stays. claude G-D-10: the log says the
10324  # listing is repeated after the half hour when a run does not finish.
10325  if [ "${DT_OK}" -eq 1 ]; then
10326  printf "${DCFG_ON}" > "${TCFG}"; TENV=(--setenv RAOFFLINEPROXY_HISTORY /storage/.config/retroarch/content_history.lpl)
10327  treset; touch -d '3 hours ago' "${THISTORY}"; touch -d '2 hours ago' "${TMARK}"
10328  tctl index-offline; printf 'wait 3\nok\n' > "${TR}/helper-plan"; rm -f "${TR}/helper.pid" "${TR}/helper-times"
10329  dbg topup
10330  for _ in $(seq 1 100); do grep -q '^start' "${TR}/helper-times" 2>/dev/null && break; sleep 0.1; done
10331  tctl index-offline; DIO=${RC}
10332  for _ in $(seq 1 150); do [ -s "${DD}/bg.rc" ] && break; sleep 0.1; done; wait "${DBG}" 2>/dev/null
10333  [ "${DIO}" -eq 0 ] && [ "$(cat "${DD}/bg.rc" 2>/dev/null)" = "0" ] && [ -e "${TPD}/index-pending" ]; check $? "gpt G-D-03: a marker an index writes while a top-up is at its jobs outlives that top-up (it was not the one the run listed for)" "gpt G-D-03: the run exited $(cat "${DD}/bg.rc" 2>/dev/null); marker: $([ -e "${TPD}/index-pending" ] && echo kept || echo gone) -- the older run acknowledged the newer notification"
10334  grep -q 'listed once for it.*again' "${TLOG}"; check $? "claude G-D-10: the log line says the marker's listing is repeated when a run does not finish" "claude G-D-10: $(grep 'listed once' "${TLOG}" | tail -n 1 | cut -c1-200)"
10335  rm -f "${TR}/helper-plan"; TENV=()
10336  fi
10337  
10338  # D30. claude G-D-11: the comment's claim that PPSSPP consumes
10339  # AchievementsHost, checked against the PPSSPP source the package pins, when
10340  # that source is on this machine (the sources cache, as section t finds the
10341  # client): the key is a ConfigSetting of [Achievements], and a non-empty
10342  # value is handed to rc_client_set_host; and the script names the pin
10343  # ppsspp-sa's package.mk pins. The launch through the proxy is the guest's.
10344  PPV="$(sed -n 's/^PKG_VERSION="\([0-9a-f]*\)".*/\1/p' "${ROOT}/projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/package.mk" | head -n 1)"
10345  PPSRC=""; for d in "${SOURCES_DIR:-}" /workspace/cache/rocknix-sources "${ROOT}/sources"; do [ -n "${d}" ] && [ -d "${d}/ppsspp-sa/ppsspp-sa-${PPV}/Core" ] && { PPSRC="${d}/ppsspp-sa/ppsspp-sa-${PPV}"; break; }; done
10346  grep -q "afbc66a3\|${PPV:0:8}" "${DD}/cheevos_ppsspp.sh" && grep -q "${PPV:0:8}" "${DD}/cheevos_ppsspp.sh"; check $? "claude G-D-11: cheevos_ppsspp.sh names the PPSSPP commit ppsspp-sa pins (${PPV:0:8}) where it cites the source" "claude G-D-11: the script's citation does not name the pin ${PPV:0:8}"
10347  if [ -n "${PPSRC}" ]; then
10348      grep -q 'ConfigSetting("AchievementsHost", SETTING(g_Config, sAchievementsHost)' "${PPSRC}/Core/Config.cpp" && grep -q 'rc_client_set_host(g_rcClient, g_Config.sAchievementsHost.c_str())' "${PPSRC}/Core/RetroAchievements.cpp"; check $? "claude G-D-11: the pinned PPSSPP source reads AchievementsHost from [Achievements] and hands it to rc_client_set_host (${PPSRC##*/})" "claude G-D-11: the pinned PPSSPP source at ${PPSRC} does not read AchievementsHost as cited"
10349  else
10350      skip "claude G-D-11's source check: PPSSPP ${PPV:0:10} is not in a sources cache on this machine"
10351  fi
10352  
10353  # D31. claude G-D-14: a badge answered 404 while a new set's images were
10354  # still reaching the image server is asked for again the next day, not a
10355  # month on -- a day's wait is one request a badge, and a new set's badges
10356  # land within it. An absent entry a day old or more is asked for once more;
10357  # one younger is not.
10358  if [ "${DT_OK}" -eq 1 ]; then
10359  python3 - "${DD}/raofflineproxy-cache-images" "${CLIENT}" "${DD}/d31" > "${DD}/d31.out" 2>&1 <<'EOS'
10360  import json, os, subprocess, sys, time
10361  from pathlib import Path
10362  helper, client, work = sys.argv[1], sys.argv[2], Path(sys.argv[3])
10363  cfg = work / "cfg"; site = work / "site"
10364  for d in (cfg, site): d.mkdir(parents=True, exist_ok=True)
10365  (site / "sitecustomize.py").write_text(
```

## Excerpt: F-09: y/F1r (`:11170-11205` at 8ebaf8daad)

```text
11170  else
11171      check 1 "-" "G2-F1-03: 092-retroarch-surface is not in the tree under test -- nothing to grade"
11172  fi
11173  
11174  # F1r-d. The gpt seat's G2-F1-04 (and the claude seat's): a start removed any
11175  #        socket at its monitor and serial paths, a live guest's included, and
11176  #        removed the monitor's before it had looked at the serial path. A
11177  #        socket that still answers a connection is held by a running QEMU
11178  #        and is refused (after a short grace, for one that is shutting
11179  #        down); every path is checked before any is removed.
11180  if [ -n "${F1_QIMG}" ]; then
11181      f1r_listen() { # <socket> <stop file>: a running guest's socket -- bound and listening until the stop file appears, 60 s at most
11182          python3 -c 'import os, socket, sys, time
11183  s = socket.socket(socket.AF_UNIX); s.bind(sys.argv[1]); s.listen(8); s.settimeout(0.05); t = time.time()
11184  while not os.path.exists(sys.argv[2]) and time.time() - t < 60:
11185      try:
11186          c, _ = s.accept(); c.close()   # as QEMU does: take the connection; the prober hangs up
11187      except socket.timeout:
11188          pass' "$1" "$2" &
11189          F1R_LPID=$!
11190          for _ in $(seq 1 100); do [ -S "$1" ] && break; sleep 0.05; done
11191      }
11192      f1r_answers() { python3 -c 'import socket, sys
11193  s = socket.socket(socket.AF_UNIX); s.settimeout(2); s.connect(sys.argv[1])' "$1" 2>/dev/null; }
11194      rm -f "${F1V}/r-live.sock" "${F1V}/r-live.stop" "${F1V}/qemu.argv"
11195      f1r_listen "${F1V}/r-live.sock" "${F1V}/r-live.stop"
11196      f1r_answers "${F1V}/r-live.sock"; check $? "the fixture's live socket answers a connection before the start (the probe can see a live guest)" "the fixture's listener at ${F1V}/r-live.sock does not answer -- the case proves nothing"
11197      f1_vm run --monitor "${F1V}/r-live.sock" --ovmf-vars "${F1V}/r-vars.fd" "${F1_OVMF[@]}" "${F1V}/disk.qcow2"
11198      [ "${F1_RC}" -ne 0 ] && [ -S "${F1V}/r-live.sock" ] && f1r_answers "${F1V}/r-live.sock" && [ ! -e "${F1V}/qemu.argv" ] && grep -q 'r-live.sock' "${F1V}/out"
11199      check $? "G2-F1-04: a start refuses a socket a running guest still listens on, names it, and the guest keeps it" "G2-F1-04: run --monitor <a live guest's socket> (rc ${F1_RC}): the socket $([ -S "${F1V}/r-live.sock" ] && echo kept || echo REMOVED), $(f1r_answers "${F1V}/r-live.sock" && echo "still answers" || echo "no longer answers"), QEMU $([ -e "${F1V}/qemu.argv" ] && echo started || echo "not started"); $(head -c 160 "${F1V}/out")"
11200      : > "${F1V}/r-live.stop"; wait "${F1R_LPID}" 2>/dev/null; rm -f "${F1V}/r-live.sock" "${F1V}/r-live.stop"
11201      # A start refused at its serial path has removed nothing: the monitor
11202      # path's stale socket is still there.
11203      rm -f "${F1V}/r-mon.sock" "${F1V}/qemu.argv"; f1_sock "${F1V}/r-mon.sock"; echo "a file of somebody's" > "${F1V}/r-serial.txt"
11204      f1_vm run --headless --monitor "${F1V}/r-mon.sock" --serial "${F1V}/r-serial.txt" --ovmf-vars "${F1V}/r-vars.fd" "${F1_OVMF[@]}" "${F1V}/disk.qcow2"
11205      [ "${F1_RC}" -ne 0 ] && [ -S "${F1V}/r-mon.sock" ] && [ "$(cat "${F1V}/r-serial.txt")" = "a file of somebody's" ] && [ ! -e "${F1V}/qemu.argv" ]
```

## Excerpt: F-17: g to i (`:839-933` at 8ebaf8daad)

```text
  839  echo "  g. the in-script RCLONE_NET_OPTS fallback is the shipped value (#146)"
  840  # Four scripts carry a constant for a conf the helper has not reached, and
  841  # their comments promise it equals the shipped RCLONE_NET_OPTS. #107 moved
  842  # the shipped value to ten low-level retries and left all four at two; on
  843  # the fallback path (a torn conf, a blanked line) that is #107 back, and no
  844  # check read the constants (audit 2026-09-12, F-03). A comment is not a check.
  845  shipped=$(sed -n 's/^DEFAULT_RCLONE_NET_OPTS="\(.*\)"$/\1/p' "${ROOT}/${RCLONE_REL}/cloud_sync.conf.defaults")
  846  [ -n "${shipped}" ]; check $? "cloud_sync.conf.defaults ships RCLONE_NET_OPTS (${shipped})" "no DEFAULT_RCLONE_NET_OPTS line in cloud_sync.conf.defaults"
  847  conf=$(sed -n 's/^RCLONE_NET_OPTS="\(.*\)"$/\1/p' "${ROOT}/${RCLONE_REL}/cloud_sync.conf")
  848  [ "${conf}" = "${shipped}" ]; check $? "cloud_sync.conf carries the same value" "cloud_sync.conf has '${conf}'"
  849  for scr in cloud_backup cloud_restore cloud_content_backup cloud_content_restore; do
  850    fb=$(sed -n 's/^RCLONE_NET_OPTS_FALLBACK="\(.*\)"$/\1/p' "${ROOT}/${RCLONE_REL}/${scr}")
  851    [ -n "${fb}" ] && [ "${fb}" = "${shipped}" ]; check $? "${scr}: RCLONE_NET_OPTS_FALLBACK is the shipped value" "${scr}: fallback is '${fb:-(none)}', shipped is '${shipped}'"
  852  done
  853  
  854  echo "  h. the rclone wrapper: an automatic run's stalled call ends at the ceiling, a deliberate run's at the stall ceiling (D-CLOUD-118, D-CLOUD-126)"
  855  # The wrapper and its helpers are lifted out of cloud_backup (from BASE_REF
  856  # under --old, as every case does since #151 PL-10) and run against a shim
  857  # rclone that sleeps. With AUTOMATIC=1 and a deadline 3 s away it must
  858  # return 124 within a few seconds. With AUTOMATIC=0 and a 3 s stall ceiling
  859  # a shim that finishes returns its own status, and one that prints nothing
  860  # and sleeps is ended at the ceiling and returns 124 as well -- the shipped
  861  # scripts left it to sleep its 20 s out and returned 0 (#153). The shim
  862  # execs its sleep so a TERM reaches the process holding the wrapper's fifo.
  863  H="${TMP}/h"; mkdir -p "${H}/shim" "${H}/run"
  864  printf '#!/bin/sh\nexec sleep "${SHIM_SLEEP:-60}"\n' > "${H}/shim/rclone"; chmod +x "${H}/shim/rclone"
  865  src_of "${RCLONE_REL}/cloud_backup" "${H}/cloud_backup"; src_of "${RCLONE_REL}/cloud_restore" "${H}/cloud_restore"
  866  {
  867      sed -n '/^child_running() {/,/^}/p; /^progress_mark() {/,/^}/p; /^advance_mark() {/,/^}/p; /^bounded_rclone() {/,/^}/p; /^rclone() {/,/^}/p' "${H}/cloud_backup"
  868      printf 'RCLONE_OUTER=""; RCLONE_CHILD=""; CEILING_DIR_ROOT=%q; DELIBERATE_CEILING_SECONDS=3\nlog_message() { :; }\n' "${H}/run"
  869  } > "${H}/wrapper.sh"
  870  grep -q 'command timeout' "${H}/wrapper.sh"; check $? "the wrapper is lifted from cloud_backup" "no rclone() wrapper found in cloud_backup"
  871  t0=$(date +%s)
  872  RC_H=$(PATH="${H}/shim:${PATH}" bash -c ". '${H}/wrapper.sh'; AUTOMATIC=1; SYNC_DEADLINE=\$(( \$(date +%s) + 3 )); RCLONE_SYNC_NET_OPTS_ARRAY=(--retries 1); rclone lsd x: ; echo \$?" 2>/dev/null | tail -1)
  873  dt=$(( $(date +%s) - t0 ))
  874  [ "${RC_H}" = "124" ]; check $? "an automatic run's stalled rclone returns 124 (timeout)" "returned '${RC_H}'"
  875  [ "${dt}" -le 10 ]; check $? "and within the ceiling (${dt}s)" "took ${dt}s"
  876  RC_H=$(PATH="${H}/shim:${PATH}" SHIM_SLEEP=0 bash -c ". '${H}/wrapper.sh'; AUTOMATIC=0; SYNC_DEADLINE=0; rclone lsd x: ; echo \$?" 2>/dev/null | tail -1)
  877  [ "${RC_H}" = "0" ]; check $? "a deliberate run's rclone that finishes returns its own status" "returned '${RC_H}'"
  878  t0=$(date +%s)
  879  RC_H=$(PATH="${H}/shim:${PATH}" SHIM_SLEEP=20 bash -c ". '${H}/wrapper.sh'; AUTOMATIC=0; SYNC_DEADLINE=0; rclone lsd x: ; echo \$?" 2>/dev/null | tail -1)
  880  dt=$(( $(date +%s) - t0 ))
  881  [ "${RC_H}" = "124" ] && [ "${dt}" -le 10 ]; check $? "a deliberate run's rclone that shows no progress is ended at the stall ceiling and returns 124 (${dt}s)" "returned '${RC_H}' after ${dt}s -- a deliberate run's stalled rclone was left to itself (#153)"
  882  for scr in cloud_backup cloud_restore; do
  883    bash -c ". <(sed -n '/^why_for() {/,/^}/p' '${H}/${scr}'); AUTOMATIC=1; why_for 124" 2>/dev/null | grep -q "TOOK TOO LONG"; check $? "${scr}: why_for 124 on an automatic run says the cloud took too long" "${scr}: $(bash -c ". <(sed -n '/^why_for() {/,/^}/p' '${H}/${scr}'); AUTOMATIC=1; why_for 124" 2>/dev/null)"
  884    bash -c ". <(sed -n '/^why_for() {/,/^}/p' '${H}/${scr}'); AUTOMATIC=0; why_for 124" 2>/dev/null | grep -q "STOPPED ANSWERING"; check $? "${scr}: and on a deliberate run that the cloud stopped answering (TRY AGAIN is in reach)" "${scr}: '$(bash -c ". <(sed -n '/^why_for() {/,/^}/p' '${H}/${scr}'); AUTOMATIC=0; why_for 124" 2>/dev/null)' -- the automatic sync's words, promising a retry nobody scheduled (#153)"
  885  done
  886  for scr in cloud_backup cloud_restore cloud_content_backup cloud_content_restore; do :; done
  887  shipped_sync=$(sed -n 's/^DEFAULT_RCLONE_SYNC_NET_OPTS="\(.*\)"$/\1/p' "${ROOT}/${RCLONE_REL}/cloud_sync.conf.defaults")
  888  for scr in cloud_backup cloud_restore; do
  889    fb=$(sed -n 's/^RCLONE_SYNC_NET_OPTS_FALLBACK="\(.*\)"$/\1/p' "${ROOT}/${RCLONE_REL}/${scr}")
  890    [ -n "${fb}" ] && [ "${fb}" = "${shipped_sync}" ]; check $? "${scr}: RCLONE_SYNC_NET_OPTS_FALLBACK is the shipped value" "${scr}: '${fb:-(none)}' vs '${shipped_sync}'"
  891  done
  892  
  893  echo "  i. cloud_net_ready settles on a held default route however NetworkManager judges connectivity"
  894  # The RG SP case (2026-09-12): NetworkManager stuck at "connected (site
  895  # only)" / "limited" with the internet reachable; the helper waited 60 s and
  896  # said no network. Shims stand in for ip (a default route) and nmcli (that
  897  # verdict); the helper must settle within the grace, not wait to the deadline.
  898  I="${TMP}/i"; mkdir -p "${I}/shim"
  899  printf '#!/bin/sh\ncase "$*" in *"route show default"*) echo "default via 192.168.1.1 dev wlan0" ;; esac\n' > "${I}/shim/ip"
  900  printf '#!/bin/sh\ncase "$*" in *STATE*) echo "connected (site only)" ;; *CONNECTIVITY*) echo "limited" ;; esac\n' > "${I}/shim/nmcli"
  901  chmod +x "${I}/shim"/*
  902  t0=$(date +%s)
  903  PATH="${I}/shim:${PATH}" bash "${ROOT}/${RCLONE_REL}/cloud_net_ready" --wait 12 > "${I}/out" 2>&1; RC_I=$?
  904  dt=$(( $(date +%s) - t0 ))
  905  [ "${RC_I}" -eq 0 ]; check $? "connected (site only) + limited settles (rc ${RC_I}, ${dt}s)" "rc ${RC_I} after ${dt}s: $(tail -1 "${I}/out" | cut -c1-120)"
  906  [ "${dt}" -lt 12 ]; check $? "and before the deadline" "took the whole wait: ${dt}s"
  907  printf '#!/bin/sh\ncase "$*" in *STATE*) echo "connecting" ;; *CONNECTIVITY*) echo "unknown" ;; esac\n' > "${I}/shim/nmcli"
  908  t0=$(date +%s)
  909  PATH="${I}/shim:${PATH}" bash "${ROOT}/${RCLONE_REL}/cloud_net_ready" --wait 3 > "${I}/out" 2>&1; RC_I=$?
  910  [ "${RC_I}" -eq 69 ]; check $? "still connecting at the deadline exits 69" "rc ${RC_I}: $(tail -1 "${I}/out" | cut -c1-120)"
  911  # The reachable wait (#192, D-CLOUD-136): with no route, a link that is
  912  # coming up is waited for and announced, one that is not exits at once.
  913  printf '#!/bin/sh\ncase "$*" in *"route show default"*) [ -e "%s/route-up" ] && echo "default via 192.168.1.1 dev wlan0" ;; esac\n' "${I}" > "${I}/shim/ip"
  914  printf '#!/bin/sh\ncase "$*" in *STATE*) echo "connecting" ;; *CONNECTIVITY*) echo "unknown" ;; esac\n' > "${I}/shim/nmcli"
  915  chmod +x "${I}/shim"/*; rm -f "${I}/route-up"
  916  t0=$(date +%s)
  917  PATH="${I}/shim:${PATH}" bash "${ROOT}/${RCLONE_REL}/cloud_net_ready" --wait 3 > "${I}/out" 2>&1; RC_I=$?
  918  dt=$(( $(date +%s) - t0 ))
  919  [ "${RC_I}" -eq 69 ] && [ "${dt}" -ge 3 ] && grep -q '^>>> doing network' "${I}/out" && grep -q "didn't come up in time" "${I}/out"; check $? "no route while NetworkManager says connecting: announced, waited the bound, then 69 (rc ${RC_I}, ${dt}s)" "rc ${RC_I} after ${dt}s: $(tr '\n' '|' < "${I}/out" | cut -c1-160)"
  920  printf '#!/bin/sh\ncase "$*" in *STATE*) echo "disconnected" ;; *CONNECTIVITY*) echo "none" ;; esac\n' > "${I}/shim/nmcli"
  921  t0=$(date +%s)
  922  PATH="${I}/shim:${PATH}" bash "${ROOT}/${RCLONE_REL}/cloud_net_ready" --wait 12 > "${I}/out" 2>&1; RC_I=$?
  923  dt=$(( $(date +%s) - t0 ))
  924  [ "${RC_I}" -eq 69 ] && [ "${dt}" -le 1 ] && ! grep -q '^>>> doing network' "${I}/out" && grep -q "there's no network connection" "${I}/out"; check $? "no route and disconnected (the radio off): 69 at once, nothing announced (rc ${RC_I}, ${dt}s)" "rc ${RC_I} after ${dt}s: $(tr '\n' '|' < "${I}/out" | cut -c1-160)"
  925  printf '#!/bin/sh\ncase "$*" in *STATE*) [ -e "%s/route-up" ] && echo "connected" || echo "connecting" ;; *CONNECTIVITY*) echo "full" ;; esac\n' "${I}" > "${I}/shim/nmcli"
  926  ( sleep 2; touch "${I}/route-up" ) &
  927  t0=$(date +%s)
  928  PATH="${I}/shim:${PATH}" bash "${ROOT}/${RCLONE_REL}/cloud_net_ready" --wait 12 > "${I}/out" 2>&1; RC_I=$?
  929  dt=$(( $(date +%s) - t0 ))
  930  wait
  931  [ "${RC_I}" -eq 0 ] && [ "${dt}" -ge 4 ] && [ "${dt}" -lt 12 ] && grep -q '^>>> doing network' "${I}/out"; check $? "a route that arrives while the link comes up: announced, then settled after the grace, before the deadline (rc ${RC_I}, ${dt}s)" "rc ${RC_I} after ${dt}s: $(tr '\n' '|' < "${I}/out" | cut -c1-160)"
  932  rm -f "${I}/route-up"
  933  
```

## Excerpt: F-17: t (`:2410-2445` at 8ebaf8daad)

```text
 2410  # case above (killed before DONE) stays TOOK_TOO_LONG.
 2411  treset; touch -d '2 hours ago' "${TMARK}"; printf 'ok\nok\n' > "${TR}/helper-plan"; echo 'slow 1000' > "${TR}/helper-linger"
 2412  tctl topup --after-index; [ "${RC}" -eq 0 ] && grep -qE ' 0 topup cached=2 skipped=0 ready=[0-9]+ limit=0 indexed=2 errors=0 added=2$' "${TSTAMP}" && grep -q 'had reported DONE and ended with rc 124' "${TLOG}"; check $? "topup whose helper reported DONE and was then killed by the bound: the run finished, rc 0, no why (#188)" "rc ${RC}; stamp: $(cat "${TSTAMP}" 2>/dev/null); log: $(grep -E 'DONE|topup' "${TLOG}" | tail -3 | tr '\n' '|')"
 2413  rm -f "${TR}/helper-linger" "${TR}/helper-plan"
 2414  # The same on the scan route: a helper that dies after its DONE.
 2415  treset; printf 'ok\nok\n' > "${TR}/helper-plan"; echo die > "${TR}/helper-linger"
 2416  tctl scan; [ "${RC}" -eq 0 ] && grep -qE '^>>> done [0-9]+\|0\|[0-9]+\|0$' "${OUT}" && ! grep -q '>>> why' "${OUT}" && grep -qE ' 0 scan cached=[0-9]+ ' "${TSTAMP}" && grep -q 'had reported DONE and ended with rc 3' "${TLOG}"; check $? "scan whose helper died after its DONE: COMPLETED, no why (#188)" "rc ${RC}; out: $(grep '^>>>' "${OUT}" | tr '\n' '|'); stamp: $(cat "${TSTAMP}" 2>/dev/null)"
 2417  rm -f "${TR}/helper-linger" "${TR}/helper-plan"
 2418  # While the jobs run the ctl keeps the progress file the page reads (fork
 2419  # #189): route, the game it is on, the total; gone when the run ends.
 2420  treset; touch -d '2 hours ago' "${TMARK}"; printf 'ok\nok\n' > "${TR}/helper-plan"
 2421  tctl topup --after-index; [ "${RC}" -eq 0 ] && grep -qE '^route=topup at=[0-9]+ index=1 total=2 name=' "${TR}/running-seen" && grep -qE '^route=topup at=[0-9]+ index=2 total=2 name=' "${TR}/running-seen" && [ ! -e "${TPD}/running" ] && [ ! -e "${TPD}/running.tmp" ]; check $? "topup keeps running (route topup, game 1 then 2 of 2) while its jobs run and removes it after (#189)" "rc ${RC}; seen: $(tr '\n' '|' < "${TR}/running-seen" 2>/dev/null); left: $(ls "${TPD}" | tr '\n' ' ')"
 2422  treset; printf 'ok\nok\n' > "${TR}/helper-plan"
 2423  tctl scan; [ "${RC}" -eq 0 ] && grep -qE '^route=scan at=[0-9]+ index=1 total=[0-9]+ name=' "${TR}/running-seen" && grep -qE '^route=scan at=[0-9]+ index=2 total=[0-9]+ name=' "${TR}/running-seen" && [ ! -e "${TPD}/running" ]; check $? "scan keeps running (route scan, game 1 then 2 of n) while its jobs run and removes it after (#189)" "rc ${RC}; seen: $(tr '\n' '|' < "${TR}/running-seen" 2>/dev/null); left: $(ls "${TPD}" | tr '\n' ' ')"
 2424  rm -f "${TR}/helper-plan"
 2425  # The real helper's badge wait (fork #188): with downloads still queued it
 2426  # returns within its bound and shuts the pool down, dropping the rest.
 2427  PYTHONPATH="${CLIENT}" python3 - "${ROOT}/${HELPER_REL}" <<'EOS' >"${OUT}" 2>"${ERR}"
 2428  import sys, time, importlib.machinery, importlib.util, concurrent.futures as cf
 2429  from raofflineproxy import image_cache
 2430  spec = importlib.util.spec_from_loader("helper", importlib.machinery.SourceFileLoader("helper", sys.argv[1]))
 2431  helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
 2432  image_cache._image_download_executor = cf.ThreadPoolExecutor(max_workers=1)
 2433  for _ in range(3): image_cache._image_download_executor.submit(time.sleep, 4)
 2434  t0 = time.time(); helper.wait_for_badges(0.5); took = time.time() - t0
 2435  assert took < 3, took
 2436  assert image_cache._image_download_executor._shutdown
 2437  print(f"ok {took:.2f}")
 2438  EOS
 2439  RC=$?; [ "${RC}" -eq 0 ] && grep -q '^ok ' "${OUT}"; check $? "the helper's badge wait returns within its bound and shuts the pool down ($(cat "${OUT}" 2>/dev/null))" "rc ${RC}; $(tail -3 "${ERR}" 2>/dev/null | tr '\n' '|')"
 2440  # summary (#190): the page's whole offline summary in one read of the store.
 2441  # The core set only (Flags 3), unlocked = the store's unlocks and the awards
 2442  # still waiting; a set with nothing in it is not a game; another account's
 2443  # game is not listed; the icon carries the service's address.
 2444  treset; PYTHONPATH="${CLIENT}" RAOFFLINEPROXY_CONFIG_DIR="${TPD}" python3 - <<'EOS'
 2445  import json, sqlite3
```

## Excerpt: F-17: x/C7 (`:6495-6525` at 8ebaf8daad)

```text
 6495      # shellcheck disable=SC2086
 6496      tar -xJf "${WKT}" -C "${WKD}" ${wkfiles} 2>/dev/null
 6497      for wp in "${WKP}"/*.patch; do
 6498          TMPDIR="${WKD}" patch -d "${WKD}/webkitgtk-${WKV}" -p1 --dry-run < "${wp}" > "${WKD}/out" 2>&1; check $? "$(basename "${wp}") applies to webkitgtk ${WKV}" "$(basename "${wp}") does not apply to ${WKV}: $(tail -2 "${WKD}/out" | tr '\n' ' ')"
 6499      done
 6500  fi
 6501  
 6502  # C7. The four scripts this stream owns are committed executable, as the
 6503  # others the recipe installs are (#308 claude F-RS-21). The recipe's chmod
 6504  # 0755 covers the image either way; the mode is what a reviewer reads.
 6505  for f in cloud_oauth cloud_device_id cloud_remote cloud_setup; do
 6506      [ "$(git -C "${ROOT}" ls-files -s -- "${RCLONE_REL}/${f}" | cut -c1-6)" = 100755 ] && [ -x "${ROOT}/${RCLONE_REL}/${f}" ]; check $? "${f} is committed executable" "${f} is committed as $(git -C "${ROOT}" ls-files -s -- "${RCLONE_REL}/${f}" | cut -c1-6) (#308 claude F-RS-21)"
 6507  done
 6508  
 6509  # C8. cloud-signin-window.c. The scripts it runs in the page are C string
 6510  # literals; they are pulled out as the compiler would join them and run by
 6511  # node against a small document. The C around them is compiled only by the
 6512  # image build (and syntax-checked with the image's toolchain by whoever
 6513  # changes it).
 6514  C8="${CS}/c8"; mkdir -p "${C8}"
 6515  src_of projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c "${C8}/window.c"
 6516  cat > "${C8}/cstrings.py" <<'EOPY'
 6517  # Print the C string a `static const char *NAME =` declaration builds from its
 6518  # adjacent literals, in the file given -- the JavaScript the window runs.
 6519  import re, sys
 6520  src = open(sys.argv[1]).read()
 6521  m = re.search(r"static const char \*%s =(.*?);\n" % re.escape(sys.argv[2]), src, re.S)
 6522  if not m:
 6523      sys.exit("no %s in %s" % (sys.argv[2], sys.argv[1]))
 6524  body = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
 6525  out = "".join(bytes(s, "utf-8").decode("unicode_escape") for s in re.findall(r'"((?:[^"\\]|\\.)*)"', body))
```

## Excerpt: F-19: z/S3F (`:13665-13722` at 8ebaf8daad)

```text
13665  echo "  S3F. the audit of the fixes: shell-owned names and NUL bytes refused by the grammar; the sorter's pipeline gates its rename; the ZIP listing's CRC column asserted; the restore gate's mount state; the pointer reader; the scrubber's truncated line; the ack's rename"
13666  SF="${TMP}/s3f"; mkdir -p "${SF}"
13667  # The grammar (cloud_backup's conf_valid), on canaries the seats wrote (gpt G3-D-01, claude G3-D-02).
13668  awk '/^conf_valid\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}' "${TMP}/src/cloud_backup" > "${SF}/cv.sh" 2>/dev/null || src_of "${RCLONE_REL}/cloud_backup" "${SF}/cb"; [ -s "${SF}/cv.sh" ] || awk '/^conf_valid\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}' "${SF}/cb" > "${SF}/cv.sh"
13669  for c in cloud_restore cloud_sync_helper; do src_of "${RCLONE_REL}/${c}" "${SF}/${c}"; awk '/^conf_valid\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}' "${SF}/${c}" > "${SF}/cv-${c}.sh"; done
13670  cmp -s "${SF}/cv.sh" "${SF}/cv-cloud_restore.sh" && cmp -s "${SF}/cv.sh" "${SF}/cv-cloud_sync_helper.sh"; check $? "conf_valid is one text in cloud_backup, cloud_restore and cloud_sync_helper" "the copies differ"
13671  sf_valid() { bash -c ". '${SF}/cv.sh'; conf_valid '$1' || { echo \"why: \${CONF_WHY}\"; exit 1; }"; }
13672  printf 'SAVESPATH="/storage/roms"\nRANDOM="BASH_VERSINFO[\\$(printf x > /tmp/s3f-ran)0]"\n' > "${SF}/c1"
13673  ! sf_valid "${SF}/c1" > "${SF}/o" 2>&1 && grep -q 'a name the shell owns' "${SF}/o"; check $? "RANDOM=... is refused as a name the shell owns (the seat's canary ran when sourced on the host)" "accepted, or another why: $(cat "${SF}/o" | tr '\n' '|' | cut -c1-120)"
13674  printf 'SAVESPATH="/storage/roms"\nPATH="/tmp/evil"\n' > "${SF}/c2"; ! sf_valid "${SF}/c2" > "${SF}/o" 2>&1 && grep -q 'a name the shell owns' "${SF}/o"; check $? "PATH=... is refused" "accepted"
13675  printf 'SAVESPATH="/storage/roms"\nRCLONEOPTS="--x \\$(printf y > /tmp/s3f-y)"\n' > "${SF}/c3"; ! sf_valid "${SF}/c3" > "${SF}/o" 2>&1 && grep -q 'followed by' "${SF}/o"; check $? "a backslash-dollar-paren inside double quotes is refused (a literal dollar-paren a shell context could run)" "accepted"
13676  printf 'SAVESPATH="/storage/roms"\nRCLONEOPTS="--filter-from \\"/a b\\" --bwlimit 1M \\$5 \\\\x"\nLOG_LEVEL=INFO\n' > "${SF}/c4"; sf_valid "${SF}/c4" > "${SF}/o" 2>&1; check $? "PL-015's escapes still pass: an escaped quote, a doubled backslash, a backslash-dollar before an ordinary character" "refused: $(cat "${SF}/o" | tr '\n' '|' | cut -c1-120)"
13677  printf 'SAVESPATH="/storage/roms"\nEXTRA="x"\000#$(printf z > /tmp/s3f-z)\n' > "${SF}/c5"; ! sf_valid "${SF}/c5" > "${SF}/o" 2>&1 && grep -q 'a NUL byte' "${SF}/o"; check $? "a NUL byte in the file is refused before awk reads a truncated record (claude G3-D-02)" "accepted: $(cat "${SF}/o" | tr '\n' '|' | cut -c1-120)"
13678  [ ! -e /tmp/s3f-ran ] && [ ! -e /tmp/s3f-y ] && [ ! -e /tmp/s3f-z ]; check $? "none of the canaries ran while being judged" "a canary file exists under /tmp"
13679  # sort_settings (001-functions) refuses to install a copy whose producer failed (gpt G3-D-04).
13680  src_of "${ROCKNIX_REL:-projects/ROCKNIX/packages/rocknix}/profile.d/001-functions" "${SF}/fn" 2>/dev/null || cp "${FN}" "${SF}/fn"
13681  mkdir -p "${SF}/cfg"; printf 'z=1\nsystem.hostname=MINE\nb=2\na=3\n' > "${SF}/cfg/system.cfg"
13682  { sed -n '/^function sort_settings() {/,/^}/p' "${SF}/fn"
13683    cat <<EOS
13684  wait_lock() { return 0; }
13685  logger() { echo "logger \$*" >&2; }
13686  J_CONF="${SF}/cfg/system.cfg"; J_CONF_LOCK="${SF}/cfg/lock"
13687  settings_base() { printf 'system.hostname=MINE\\nb=2\\n'; return 1; }   # the hostname, then a failure
13688  EOS
13689  } > "${SF}/ss.sh"
13690  bash -c ". '${SF}/ss.sh'; sort_settings" 2>/dev/null; [ "$(cat "${SF}/cfg/system.cfg" | tr '\n' '|')" = "z=1|system.hostname=MINE|b=2|a=3|" ] && [ ! -e "${SF}/cfg/system.cfg.tmp" ]; check $? "a producer that fails after the hostname line installs nothing: the live file is untouched, no temporary left" "system.cfg is now '$(cat "${SF}/cfg/system.cfg" | tr '\n' '|')'"
13691  # backuptool's zip_stored_ok asserts the CRC column (claude G3-D-01).
13692  src_of "${ROCKNIX_REL:-projects/ROCKNIX/packages/rocknix}/sources/scripts/backuptool" "${SF}/bt" 2>/dev/null || cp "${BT}" "${SF}/bt"
13693  grep -q "grep -q 'CRC-32'" "${SF}/bt"; check $? "zip_stored_ok refuses a listing with no CRC column (the image's busybox prints one; a lesser build would pass every member)" "no CRC-32 header check in zip_stored_ok"
13694  # chksysconfig: roms-mounted=no proceeds only while the folder is still not a mount (gpt G3-D-07).
13695  src_of "${ROCKNIX_REL:-projects/ROCKNIX/packages/rocknix}/sources/scripts/chksysconfig" "${SF}/ck" 2>/dev/null || cp "${CHK}" "${SF}/ck"
13696  grep -q '\[ "${mounted}" = "0" \] && return 1' "${SF}/ck" && grep -q 'it is mounted now' "${SF}/ck"; check $? "finish_restore: a restore that ran with no roms mount waits when a mount is there now, or the table cannot be read" "the was=no branch still proceeds unconditionally"
13697  # The setup reader (historically the migration reader) uses the shared pointer grammar (claude G3-D-05).
13698  sf_reader=cloud_setup; sf_getter=conf_get
13699  if [ "${MIGRATION_AVAILABLE}" -eq 1 ]; then sf_reader=cloud_migrate_layout; sf_getter=conf_value; fi
13700  src_of "${RCLONE_REL}/${sf_reader}" "${SF}/ml"
13701  printf 'SAVESPATH="/storage/roms"\nSAVES_REMOTE=%s/Mine/Saves%s\nSETTINGS_REMOTE=/Mine/Backups\nCONTENT_REMOTE="/Mine/Content"\n' "'" "'" > "${SF}/ml.conf"
13702  v=$(bash -c "SYNC_CONF='${SF}/ml.conf'; $(awk '/^conf_get\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}; /^conf_value\(\) *\{/{q=1} q{print} q&&/^\}/{q=0}' "${SF}/ml"); ${sf_getter} SAVES_REMOTE; ${sf_getter} SETTINGS_REMOTE" 2>/dev/null | tr '\n' '|')
13703  [ "${v}" = "/Mine/Saves|/Mine/Backups|" ]; check $? "a single-quoted and a bare pointer read as their values, not as the whole line" "read as '${v}'"
13704  # cloud_log_scrub: a config line cut before its suffix keeps nothing after the verb (gpt G3-D-09).
13705  src_of "${RCLONE_REL}/cloud_log_scrub" "${SF}/ls"
13706  SCRUB=$(bash -c ". <(sed -n '/^SCRUB_SED=/,/^'\"'\"'$/p' '${SF}/ls'); printf '%s' \"\${SCRUB_SED}\"")
13707  printf '[2026-09-28 10:00:00] [INFO] [cloud_remote] rclone config create qa webdav url=http://x pass="front back" vendor=other\n' | sed -E -e "${SCRUB}" > "${SF}/scrubbed"
13708  ! grep -q 'front\|back\|http://x' "${SF}/scrubbed" && grep -q 'url=<redacted> pass=<redacted> vendor=<redacted>' "${SF}/scrubbed"; check $? "a truncated config line masks a quoted value whole, key by key (a quoted value with a space left its tail readable)" "scrubbed line: $(cat "${SF}/scrubbed" | cut -c1-160)"
13709  printf '[2026-09-28 10:00:00] [INFO] [cloud_remote] rclone config create qa webdav url=http://x pass="front ba\n' | sed -E -e "${SCRUB}" > "${SF}/scrubbed2"
13710  ! grep -q 'front\|ba$\|http://x' "${SF}/scrubbed2" && grep -q 'pass=<redacted>' "${SF}/scrubbed2"; check $? "a line cut inside a quoted value masks it to the end" "scrubbed line: $(cat "${SF}/scrubbed2" | cut -c1-160)"
13711  # raofflineproxy-ctl: the acknowledgement takes the marker aside by rename (gpt G3-D-03).
13712  src_of "projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl" "${SF}/ctl"
13713  mkdir -p "${SF}/pd"; printf 'B\n' > "${SF}/pd/index-pending"
13714  bash -c "INDEX_PENDING='${SF}/pd/index-pending'; pending_lock() { return 0; }; pending_unlock() { :; }; $(awk '/^ack_index_pending\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}' "${SF}/ctl"); ack_index_pending A; echo rc=\$?" > "${SF}/o" 2>&1
13715  grep -q 'rc=1' "${SF}/o" && [ "$(cat "${SF}/pd/index-pending" 2>/dev/null)" = "B" ] && [ -z "$(ls "${SF}/pd"/index-pending.ack.* 2>/dev/null)" ]; check $? "an ack for token A over a marker holding B keeps B in place and leaves no aside file" "$(cat "${SF}/o" | tr '\n' '|'); marker: $(cat "${SF}/pd/index-pending" 2>/dev/null)"
13716  printf 'A\n' > "${SF}/pd/index-pending"
13717  bash -c "INDEX_PENDING='${SF}/pd/index-pending'; pending_lock() { return 0; }; pending_unlock() { :; }; $(awk '/^ack_index_pending\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}' "${SF}/ctl"); ack_index_pending A; echo rc=\$?" > "${SF}/o" 2>&1
13718  grep -q 'rc=0' "${SF}/o" && [ ! -e "${SF}/pd/index-pending" ]; check $? "an ack for token A over a marker holding A removes it" "$(cat "${SF}/o" | tr '\n' '|')"
13719  
13720  
13721  LY="${TMP}/ly"; mkdir -p "${LY}"
13722  if [ "${MIGRATION_AVAILABLE}" -eq 1 ]; then
```

## Excerpt: F-21: z (`:13390-13430` at 8ebaf8daad)

```text
13390  if dmg != "-":
13391      b = bytearray(open(out, "rb").read())
13392      zi = zipfile.ZipFile(out).getinfo(dmg)
13393      o = zi.header_offset; nl, el = struct.unpack("<HH", b[o + 26:o + 30]); start = o + 30 + nl + el
13394      b[start + 2] ^= 0x20
13395      open(out, "wb").write(b)
13396  EOS
13397  }
13398  P7ZLONG=$(printf 'retroarch_setting_%s = "value"\n' $(seq 1 60) | tr -d '\n')
13399  if [ -n "${BB}" ]; then
13400      p7reset '  /storage/.config/test/*'
13401      p7zipm m.zip storage/.config/test/s.cfg "storage/.config/test/s.cfg|stored|STORED-ORIGINAL-CONTENT" "storage/.config/test/d.cfg|deflated|${P7ZLONG}"
13402      "${BB_HOST}" unzip -t "${P7S}/roms/backup/m.zip" >/dev/null 2>&1; p7t=$?
13403      "${BB_HOST}" unzip -p "${P7S}/roms/backup/m.zip" >/dev/null 2>&1; p7p=$?
13404      p7zipm m2.zip storage/.config/test/d.cfg "storage/.config/test/s.cfg|stored|STORED-ORIGINAL-CONTENT" "storage/.config/test/d.cfg|deflated|${P7ZLONG}"
13405      "${BB_HOST}" unzip -p "${P7S}/roms/backup/m2.zip" >/dev/null 2>&1; p7p2=$?
13406      [ "${p7t}" -eq 0 ] && [ "${p7p}" -eq 0 ] && [ "${p7p2}" -ne 0 ]; check $? "audit of the fix round PL-022 (the measurement, BS-3): the image's busybox unzip passes a damaged STORED member (-t rc ${p7t}, -p rc ${p7p}) and fails a damaged DEFLATED one (-p rc ${p7p2})" "PL-022 measurement: -t ${p7t}, -p ${p7p} on the stored damage; -p ${p7p2} on the deflated -- busybox's behaviour is not what this case was written against"
13407      p7reset '  /storage/.config/test/*'
13408      echo LIVE > "${P7S}/.config/test/f1"
13409      p7zipm 20260101000000-ROCKNIX_BACKUP.zip storage/.config/test/f1 "storage/.config/test/f1|stored|STORED-ORIGINAL-CONTENT" "storage/.config/test/d.cfg|deflated|${P7ZLONG}"
13410      p7bt restore --no-restart
13411      [ "${RC}" -ne 0 ] && [ "$(p7why)" = "THIS DEVICE'S SETTINGS BACKUP IS DAMAGED" ] && [ "$(cat "${P7S}/.config/test/f1")" = "LIVE" ] && [ ! -e "${P7S}/.config/test/d.cfg" ] && [ -z "$(ls "${P7S}/roms/backup/archive"/*PRE_RESTORE* 2>/dev/null)" ]; check $? "audit of the fix round PL-022: a legacy zip whose STORED member's bytes do not match its listed CRC is refused as damaged before anything is written" "PL-022 (stored, damaged): rc ${RC}; why '$(p7why)'; f1 '$(head -c 30 "${P7S}/.config/test/f1")'; d.cfg $([ -e "${P7S}/.config/test/d.cfg" ] && echo written || echo absent) -- the corrupted bytes were restored as settings"
13412      p7reset '  /storage/.config/test/*'
13413      echo LIVE > "${P7S}/.config/test/f1"
13414      p7zipm 20260101000000-ROCKNIX_BACKUP.zip storage/.config/test/d.cfg "storage/.config/test/f1|stored|STORED-ORIGINAL-CONTENT" "storage/.config/test/d.cfg|deflated|${P7ZLONG}"
13415      p7bt restore --no-restart
13416      [ "${RC}" -ne 0 ] && [ "$(p7why)" = "THIS DEVICE'S SETTINGS BACKUP IS DAMAGED" ] && [ "$(cat "${P7S}/.config/test/f1")" = "LIVE" ]; check $? "audit of the fix round PL-022: a legacy zip with a damaged DEFLATED member is refused as damaged" "PL-022 (deflated, damaged): rc ${RC}; why '$(p7why)'; f1 '$(head -c 30 "${P7S}/.config/test/f1")'"
13417      p7reset '  /storage/.config/test/*'
13418      echo LIVE > "${P7S}/.config/test/f1"
13419      p7zipm 20260101000000-ROCKNIX_BACKUP.zip - "storage/.config/test/f1|stored|STORED-ORIGINAL-CONTENT" "storage/.config/test/my [x] *file?.cfg|stored|BRACKETS" "storage/.config/test/d.cfg|deflated|${P7ZLONG}" "storage/.config/test/empty.cfg|stored|"
13420      p7bt restore --no-restart
13421      [ "${RC}" -eq 0 ] && [ "$(cat "${P7S}/.config/test/f1")" = "STORED-ORIGINAL-CONTENT" ] && [ "$(cat "${P7S}/.config/test/my [x] *file?.cfg")" = "BRACKETS" ] && [ "$(cat "${P7S}/.config/test/d.cfg")" = "${P7ZLONG}" ] && [ -e "${P7S}/.config/test/empty.cfg" ]; check $? "audit of the fix round PL-022: a whole legacy zip -- stored and deflated members, a stored name with brackets, a star and a space, an empty stored file -- restores (rc ${RC})" "PL-022 (healthy): rc ${RC}; why '$(p7why)'; f1 '$(head -c 30 "${P7S}/.config/test/f1")'; brackets '$(cat "${P7S}/.config/test/my [x] *file?.cfg" 2>/dev/null)'"
13422  else
13423      skip "audit of the fix round PL-022: the image's busybox is not on this machine, and the case is its behaviour"
13424  fi
13425  
13426  # == PL-028: an archive with a member outside storage/ is refused before anything is written
13427  mkdir -p "${P7Z}/outside"
13428  p7zforeign() { # <verb...>: backuptool with /outside bound from the host, so a write there is seen
13429      rm -rf "${P7Z}/outside"; mkdir -p "${P7Z}/outside"
13430      P7X=(--bind "${P7Z}/outside" /outside)
```

## External: tools/settings-modes-test at 8ebaf8daad (whole)

```text
    1  #!/usr/bin/env python3
    2  """#421: real shell writer functions, scratch paths, candidate busybox applets."""
    3  import argparse, hashlib, json, os, re, shutil, subprocess, tempfile
    4  from pathlib import Path
    5  p=argparse.ArgumentParser();p.add_argument('--profile',type=Path,required=True);p.add_argument('--chksysconfig',type=Path,required=True);p.add_argument('--busybox',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    6  fn=a.profile.read_text();ck=a.chksysconfig.read_text();rows=[]
    7  with tempfile.TemporaryDirectory(prefix='pixelelated-settings-modes-') as tmp:
    8   root=Path(tmp);bb=root/'busybox';shutil.copy2(a.busybox,bb);bin=root/'bin';bin.mkdir()
    9   for applet in ['stat','chmod','cp','mv','awk','sed','head','tail','wc','tr','cut']:
   10    f=bin/applet;f.write_text('#!/bin/sh\nexec '+str(bb)+' '+applet+' "$@"\n');f.chmod(0o755)
   11   functions='\n'.join(re.findall(r'^function \w+\(\) \{.*?^\}',fn,re.M|re.S))
   12   functions+='\n'+'\n'.join(re.findall(r'^\w+\(\) \{.*?^\}',ck,re.M|re.S))
   13   for operation in ['set_setting','set_settings','del_setting','sort_settings','backup','restore']:
   14    for scenario in ['private_live','private_record','wide_temp','restricted_group']:
   15     case=root/(operation+'-'+scenario);configroot=case/'config';cfgdir=configroot/'system/configs';cfgdir.mkdir(parents=True)
   16     live=cfgdir/'system.cfg';record=Path(str(live)+'.backup')
   17     original=b'system.hostname=qa\nqa.setting=older\nqa.keep=kept\n';oldrecord=b'system.hostname=qa\nqa.setting=record\nqa.keep=kept\n'
   18     live.write_bytes(original);record.write_bytes(oldrecord)
   19     live.chmod(0o644 if scenario=='private_record' else 0o660 if scenario=='restricted_group' else 0o600)
   20     record.chmod(0o644 if scenario=='private_live' else 0o640 if scenario=='restricted_group' else 0o600)
   21     expectedmode=0o640 if scenario=='restricted_group' else 0o600
   22     if scenario=='wide_temp':
   23      for f in [Path(str(live)+'.tmp'),Path(str(record)+'.tmp')]:f.write_bytes(b'stale\n');f.chmod(0o666)
   24     commands={'set_setting':'set_setting qa.setting newer','set_settings':'set_settings qa.setting newer qa.other second','del_setting':'del_setting qa.setting','sort_settings':'sort_settings','backup':'backup','restore':'restore'}
   25     setup=functions.replace('/storage/.config',str(configroot))+f'\nJ_CONF="{live}"; J_CONF_LOCK="{case}/lock"; CFG="{live}"; BACKUP="{record}"; logger() {{ :; }}\numask 022\n'
   26     result=subprocess.run(['bash','-c',setup+commands[operation]],capture_output=True,text=True,timeout=15,env={**os.environ,'PATH':str(bin)+':/usr/bin:/bin'})
   27     target=record if operation=='backup' else live
   28     expected=oldrecord if operation=='restore' else original if operation=='backup' else b''.join(sorted(original.splitlines(keepends=True))) if operation=='sort_settings' else original.replace(b'qa.setting=older\n',b'')+(b'qa.setting=newer\n'+(b'qa.other=second\n' if operation=='set_settings' else b'') if operation!='del_setting' else b'')
   29     okay=result.returncode==0 and target.read_bytes()==expected and target.stat().st_mode&0o777==expectedmode
   30     rows.append({'case':case.name,'pass':okay,'rc':result.returncode,'expected_mode':oct(expectedmode),'actual_mode':oct(target.stat().st_mode&0o777),'bytes_match':target.read_bytes()==expected})
   31     print(('PASS ' if okay else 'FAIL ')+case.name,flush=True)
   32   # Every refused staging action leaves the published file and other file intact.
   33   for fault in ['symlink','chmod','stat','producer','rename']:
   34    case=root/('refuse-'+fault);configroot=case/'config';cfgdir=configroot/'system/configs';cfgdir.mkdir(parents=True)
   35    live=cfgdir/'system.cfg';live.write_bytes(b'system.hostname=qa\nqa.setting=older\n');live.chmod(0o600);original=live.read_bytes();victim=case/'other';victim.write_bytes(b'unchanged\n')
   36    if fault=='symlink':Path(str(live)+'.tmp').symlink_to(victim)
   37    injected={'symlink':'','chmod':'chmod() { return 1; }','stat':'stat() { return 1; }','producer':'settings_base() { printf "system.hostname=qa\\n"; return 1; }','rename':'mv() { return 1; }'}[fault]
   38    setup=functions.replace('/storage/.config',str(configroot))+f'\nJ_CONF="{live}"; J_CONF_LOCK="{case}/lock"; logger() {{ :; }}\numask 022\n'+injected+'\n'
   39    command='sort_settings' if fault=='rename' else 'set_setting qa.setting newer'
   40    result=subprocess.run(['bash','-c',setup+command],capture_output=True,text=True,timeout=15,env={**os.environ,'PATH':str(bin)+':/usr/bin:/bin'})
   41    okay=result.returncode!=0 and not live.is_symlink() and live.read_bytes()==original and live.stat().st_mode&0o777==0o600 and victim.read_bytes()==b'unchanged\n'
   42    rows.append({'case':'refuse-'+fault,'pass':okay,'rc':result.returncode});print(('PASS ' if okay else 'FAIL ')+'refuse-'+fault,flush=True)
   43  report={'pass':all(x['pass'] for x in rows),'checks':rows,'profile_sha256':hashlib.sha256(a.profile.read_bytes()).hexdigest(),'chksysconfig_sha256':hashlib.sha256(a.chksysconfig.read_bytes()).hexdigest(),'busybox_sha256':hashlib.sha256(a.busybox.read_bytes()).hexdigest()}
   44  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(0 if report['pass'] else 1)
```

## External: tools/settings-modes-test at 7c1d729b57 (whole)

```text
    1  #!/usr/bin/env python3
    2  """#421: real shell writer functions, scratch paths, candidate busybox applets.
    3  
    4  The busybox must be the candidate's (#997): a path under a build root's
    5  image/system/ (its BUILD_ID read from that root's etc/os-release), or one
    6  whose origin --busybox-from names (a BUILD_ID, or `image` on the candidate
    7  itself, as a guest run passes /usr/bin/busybox). Any other is refused, exit 2;
    8  --unverified-busybox runs it anyway and marks every line `host busybox, not the
    9  candidate's`: it exits 3 when every case passed, because a run that could not
   10  qualify the candidate has not passed, and 1 when a case failed, because a
   11  defect found under another busybox is still a defect. Every applet that busybox lists is shimmed (on the image each
   12  is the busybox's, sh aside, which is bash), so a writer's command runs as the
   13  device runs it, and the receipt hashes the bytes that ran.
   14  """
   15  import argparse, hashlib, json, os, re, shlex, shutil, subprocess, sys, tempfile
   16  from pathlib import Path
   17  UNVERIFIED="host busybox, not the candidate's"
   18  def cannot(why):print('settings-modes-test: CANNOT -- '+why,file=sys.stderr);raise SystemExit(2)
   19  def origin(path,declared,unverified):
   20   real=path.resolve()
   21   for d in real.parents:
   22    if d.name=='system' and d.parent.name=='image':
   23     rel=d/'etc/os-release'
   24     ids=re.findall(r'^BUILD_ID="?([^"\n]*)"?$',rel.read_text(),re.M) if rel.is_file() and not rel.is_symlink() else []
   25     if not ids or not ids[-1]:cannot(f'{path} is under {d} but {rel} names no BUILD_ID')
   26     return {'kind':'build-root','root':str(d.parent.parent),'build_id':ids[-1]}
   27   if declared:return {'kind':'declared','from':declared}
   28   if unverified:return {'kind':'unverified','marker':UNVERIFIED}
   29   cannot(f'{path} is not under a build root\'s image/system/; name its origin with --busybox-from <BUILD_ID|image>, or pass --unverified-busybox (exit 3)')
   30  p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter);p.add_argument('--profile',type=Path,required=True);p.add_argument('--chksysconfig',type=Path,required=True);p.add_argument('--busybox',type=Path,required=True);p.add_argument('--busybox-from',help='the busybox\'s origin when it is not under a build root: a BUILD_ID, or image');p.add_argument('--unverified-busybox',action='store_true',help='run a busybox of no known origin: every line is marked; exit 3 when every case passed, 1 when one failed');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
   31  src=origin(a.busybox,a.busybox_from,a.unverified_busybox);mark=' -- '+UNVERIFIED if src['kind']=='unverified' else ''
   32  print('busybox: '+(f"build root {src['root']}, BUILD_ID {src['build_id']}" if src['kind']=='build-root' else f"declared from {src['from']}" if src['kind']=='declared' else UNVERIFIED),flush=True)
   33  fn=a.profile.read_text();ck=a.chksysconfig.read_text();rows=[]
   34  with tempfile.TemporaryDirectory(prefix='pixelelated-settings-modes-') as tmp:
   35   root=Path(tmp);bb=root/'busybox';shutil.copy2(a.busybox,bb);bbsha=hashlib.sha256(bb.read_bytes()).hexdigest();bin=root/'bin';bin.mkdir()
   36   applets=[x for x in subprocess.run([str(bb),'--list'],capture_output=True,text=True).stdout.split() if x!='sh']
   37   if not {'stat','chmod','cp','mv','awk','sed','mktemp','cat','rm'}<=set(applets):cannot(f'{a.busybox} --list lacks the writers\' applets')
   38   for applet in applets:
   39    f=bin/applet;f.write_text('#!/bin/sh\nexec '+shlex.quote(str(bb))+' '+applet+' "$@"\n');f.chmod(0o755)
   40   functions='\n'.join(re.findall(r'^function \w+\(\) \{.*?^\}',fn,re.M|re.S))
   41   functions+='\n'+'\n'.join(re.findall(r'^\w+\(\) \{.*?^\}',ck,re.M|re.S))
   42   for operation in ['set_setting','set_settings','del_setting','sort_settings','backup','restore']:
   43    for scenario in ['private_live','private_record','wide_temp','restricted_group']:
   44     case=root/(operation+'-'+scenario);configroot=case/'config';cfgdir=configroot/'system/configs';cfgdir.mkdir(parents=True)
   45     live=cfgdir/'system.cfg';record=Path(str(live)+'.backup')
   46     original=b'system.hostname=qa\nqa.setting=older\nqa.keep=kept\n';oldrecord=b'system.hostname=qa\nqa.setting=record\nqa.keep=kept\n'
   47     live.write_bytes(original);record.write_bytes(oldrecord)
   48     live.chmod(0o644 if scenario=='private_record' else 0o660 if scenario=='restricted_group' else 0o600)
   49     record.chmod(0o644 if scenario=='private_live' else 0o640 if scenario=='restricted_group' else 0o600)
   50     expectedmode=0o640 if scenario=='restricted_group' else 0o600
   51     if scenario=='wide_temp':
   52      for f in [Path(str(live)+'.tmp'),Path(str(record)+'.tmp')]:f.write_bytes(b'stale\n');f.chmod(0o666)
   53     commands={'set_setting':'set_setting qa.setting newer','set_settings':'set_settings qa.setting newer qa.other second','del_setting':'del_setting qa.setting','sort_settings':'sort_settings','backup':'backup','restore':'restore'}
   54     setup=functions.replace('/storage/.config',str(configroot))+f'\nJ_CONF="{live}"; J_CONF_LOCK="{case}/lock"; CFG="{live}"; BACKUP="{record}"; logger() {{ :; }}\numask 022\n'
   55     result=subprocess.run(['bash','-c',setup+commands[operation]],capture_output=True,text=True,timeout=15,env={**os.environ,'PATH':str(bin)+':/usr/bin:/bin'})
   56     target=record if operation=='backup' else live
   57     expected=oldrecord if operation=='restore' else original if operation=='backup' else b''.join(sorted(original.splitlines(keepends=True))) if operation=='sort_settings' else original.replace(b'qa.setting=older\n',b'')+(b'qa.setting=newer\n'+(b'qa.other=second\n' if operation=='set_settings' else b'') if operation!='del_setting' else b'')
   58     okay=result.returncode==0 and target.read_bytes()==expected and target.stat().st_mode&0o777==expectedmode
   59     rows.append({'case':case.name,'pass':okay,'rc':result.returncode,'expected_mode':oct(expectedmode),'actual_mode':oct(target.stat().st_mode&0o777),'bytes_match':target.read_bytes()==expected})
   60     print(('PASS ' if okay else 'FAIL ')+case.name+mark,flush=True)
   61   # Every refused staging action leaves the published file and other file intact.
   62   for fault in ['symlink','chmod','stat','producer','rename']:
   63    case=root/('refuse-'+fault);configroot=case/'config';cfgdir=configroot/'system/configs';cfgdir.mkdir(parents=True)
   64    live=cfgdir/'system.cfg';live.write_bytes(b'system.hostname=qa\nqa.setting=older\n');live.chmod(0o600);original=live.read_bytes();victim=case/'other';victim.write_bytes(b'unchanged\n')
   65    if fault=='symlink':Path(str(live)+'.tmp').symlink_to(victim)
   66    injected={'symlink':'','chmod':'chmod() { return 1; }','stat':'stat() { return 1; }','producer':'settings_base() { printf "system.hostname=qa\\n"; return 1; }','rename':'mv() { return 1; }'}[fault]
   67    setup=functions.replace('/storage/.config',str(configroot))+f'\nJ_CONF="{live}"; J_CONF_LOCK="{case}/lock"; logger() {{ :; }}\numask 022\n'+injected+'\n'
   68    command='sort_settings' if fault=='rename' else 'set_setting qa.setting newer'
   69    result=subprocess.run(['bash','-c',setup+command],capture_output=True,text=True,timeout=15,env={**os.environ,'PATH':str(bin)+':/usr/bin:/bin'})
   70    okay=result.returncode!=0 and not live.is_symlink() and live.read_bytes()==original and live.stat().st_mode&0o777==0o600 and victim.read_bytes()==b'unchanged\n'
   71    rows.append({'case':'refuse-'+fault,'pass':okay,'rc':result.returncode});print(('PASS ' if okay else 'FAIL ')+'refuse-'+fault+mark,flush=True)
   72  report={'pass':all(x['pass'] for x in rows),'checks':rows,'profile_sha256':hashlib.sha256(a.profile.read_bytes()).hexdigest(),'chksysconfig_sha256':hashlib.sha256(a.chksysconfig.read_bytes()).hexdigest(),'busybox_sha256':bbsha,'busybox_origin':src,'shimmed_applets':len(applets)}
   73  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(1 if not report['pass'] else 3 if mark else 0)
```

## External: tools/melonds-upgrade-test at 8ebaf8daad (whole)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  """#526: preserve melonDS configuration while adding missing hotkey defaults.
    4  
    5  Runs the actual post-update function with owned paths and candidate BusyBox
    6  applets. An older post-update runs its exact legacy tail with those paths
    7  relocated into the fixture; its failures are discriminating negative controls.
    8  """
    9  import argparse
   10  import hashlib
   11  import json
   12  import os
   13  from pathlib import Path
   14  import re
   15  import shlex
   16  import shutil
   17  import subprocess
   18  import tempfile
   19  
   20  
   21  def main():
   22      parser = argparse.ArgumentParser(description=__doc__)
   23      parser.add_argument('--post-update', required=True, type=Path)
   24      parser.add_argument('--busybox', required=True, type=Path)
   25      parser.add_argument('--output', required=True, type=Path)
   26      args = parser.parse_args()
   27      source = args.post_update.read_text()
   28      function = re.search(r'^update_melonds_hotkeys\(\) \{.*?^\}', source, re.M | re.S)
   29      legacy = re.search(r'^rm -rf /storage/\.config/melonDS\ncp -r /usr/config/melondDS /storage/\.config/\s*$', source, re.M)
   30      if not function and not legacy:
   31          parser.error('no recognized current function or historical update block')
   32      rows = []
   33      cases = ['missing-defaults', 'missing-config', 'empty-defaults', 'add-missing',
   34               'already-current', 'no-final-newline', 'empty-config', 'file-link',
   35               'directory-link', 'whitespace-key', 'non-hotkey-defaults',
   36               'copy-failure', 'producer-failure', 'rename-failure', 'temp-failure']
   37      with tempfile.TemporaryDirectory(prefix='pixelelated-melonds-') as temporary:
   38          root = Path(temporary)
   39          busybox = root / 'busybox'
   40          shutil.copy2(args.busybox, busybox)
   41          binary = root / 'bin'
   42          binary.mkdir()
   43          for applet in ['mktemp', 'cp', 'awk', 'mv', 'rm']:
   44              wrapper = binary / applet
   45              wrapper.write_text('#!/bin/sh\nexec ' + shlex.quote(str(busybox)) + ' ' + applet + ' "$@"\n')
   46              wrapper.chmod(0o700)
   47          for name in cases:
   48              case = root / (name + ' with spaces')
   49              defaults = case / 'usr/config/melonDS/melonDS.ini'
   50              config = case / 'storage/.config/melonDS/melonDS.ini'
   51              defaults.parent.mkdir(parents=True)
   52              config.parent.mkdir(parents=True)
   53              defaults.write_text('HKKey_New=-1\nHKJoy_Custom=5\nHKJoy_New=4\nScreenLayout=2\n')
   54              original = '# owner settings\nHKJoy_Custom=99\nScreenLayout=7\nOwnerUnknown=yes\n'
   55              config.write_text(original)
   56              config.chmod(0o600)
   57              sentinel = config.parent / 'owner-extra.txt'
   58              sentinel.write_text('keep extra file\n')
   59              expected = original + 'HKKey_New=-1\nHKJoy_New=4\n'
   60              injected = ''
   61              expected_rc = 0
   62              if name == 'missing-defaults':
   63                  defaults.unlink(); expected = original
   64              elif name == 'missing-config':
   65                  config.unlink(); expected = None
   66              elif name == 'empty-defaults':
   67                  defaults.write_text(''); expected = original
   68              elif name == 'already-current':
   69                  config.write_text(expected); original = expected
   70              elif name == 'no-final-newline':
   71                  config.write_text(original.rstrip('\n'))
   72              elif name == 'empty-config':
   73                  config.write_text(''); expected = 'HKKey_New=-1\nHKJoy_Custom=5\nHKJoy_New=4\n'
   74              elif name == 'file-link':
   75                  target = case / 'owner-target.ini'; config.rename(target); config.symlink_to(target); expected = original
   76              elif name == 'directory-link':
   77                  target = case / 'owner-directory'; config.parent.rename(target); config.parent.symlink_to(target); expected = original
   78              elif name == 'whitespace-key':
   79                  original = original.replace('HKJoy_Custom=99', ' HKJoy_Custom = 99')
   80                  config.write_text(original); expected = original + 'HKKey_New=-1\nHKJoy_New=4\n'
   81              elif name == 'non-hotkey-defaults':
   82                  defaults.write_text('ScreenLayout=2\n'); config.write_text(original.rstrip('\n')); expected = original.rstrip('\n')
   83              elif name.endswith('-failure'):
   84                  injected = {'copy-failure': 'cp() { return 1; }',
   85                              'producer-failure': 'awk() { printf "partial output\\n"; return 1; }',
   86                              'rename-failure': 'mv() { return 1; }',
   87                              'temp-failure': 'mktemp() { return 1; }'}[name]
   88                  expected = original; expected_rc = 1
   89              inode = config.stat().st_ino if config.exists() else None
   90              if function:
   91                  command = function.group() + '\n' + injected + '\nupdate_melonds_hotkeys ' + shlex.quote(str(defaults)) + ' ' + shlex.quote(str(config))
   92              else:
   93                  command = legacy.group().replace('/storage/', shlex.quote(str(case / 'storage')) + '/').replace('/usr/config/', shlex.quote(str(case / 'usr/config')) + '/')
   94              result = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
   95                                      timeout=15, env={**os.environ, 'PATH': str(binary) + ':/usr/bin:/bin'})
   96              actual = config.read_text() if config.exists() else None
   97              okay = result.returncode == expected_rc and actual == expected
   98              okay = okay and sentinel.exists() and sentinel.read_text() == 'keep extra file\n'
   99              okay = okay and not list(config.parent.glob('melonDS.ini.??????'))
  100              if config.exists():
  101                  okay = okay and config.stat().st_mode & 0o777 == 0o600
  102              if name == 'file-link':
  103                  okay = okay and config.is_symlink()
  104              if name == 'directory-link':
  105                  okay = okay and config.parent.is_symlink()
  106              if name in ['already-current', 'non-hotkey-defaults'] and config.exists():
  107                  okay = okay and config.stat().st_ino == inode
  108              if okay and name == 'add-missing':
  109                  after = config.stat().st_ino
  110                  repeat = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
  111                                          timeout=15, env={**os.environ, 'PATH': str(binary) + ':/usr/bin:/bin'})
  112                  okay = repeat.returncode == 0 and config.read_text() == expected and config.stat().st_ino == after
  113              rows.append({'case': name, 'pass': okay, 'rc': result.returncode, 'stderr': result.stderr})
  114              print(('PASS ' if okay else 'FAIL ') + name, flush=True)
  115      report = {'pass': all(row['pass'] for row in rows), 'checks': rows,
  116                'legacy_negative_control': not bool(function),
  117                'post_update_sha256': hashlib.sha256(args.post_update.read_bytes()).hexdigest(),
  118                'busybox_sha256': hashlib.sha256(args.busybox.read_bytes()).hexdigest()}
  119      args.output.parent.mkdir(parents=True, exist_ok=True)
  120      args.output.write_text(json.dumps(report, indent=2) + '\n')
  121      return 0 if report['pass'] else 1
  122  
  123  
  124  if __name__ == '__main__':
  125      raise SystemExit(main())
```

## External: tools/melonds-upgrade-test at 7c1d729b57 (whole)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  """#526: preserve melonDS configuration while adding missing hotkey defaults.
    4  
    5  Runs the actual post-update function with owned paths and candidate BusyBox
    6  applets. An older post-update runs its exact legacy tail with those paths
    7  relocated into the fixture; its failures are discriminating negative controls.
    8  
    9  The busybox must be the candidate's (#997): a path under a build root's
   10  image/system/ (its BUILD_ID read from that root's etc/os-release), or one
   11  whose origin --busybox-from names (a BUILD_ID, or `image` on the candidate
   12  itself, as a guest run passes /usr/bin/busybox). Any other is refused, exit 2;
   13  --unverified-busybox runs it anyway and marks every line "host busybox, not the
   14  candidate's": it exits 3 when every case passed, because a run that could not
   15  qualify the candidate has not passed, and 1 when a case failed, because a
   16  defect found under another busybox is still a defect. Every applet that busybox lists is shimmed (sh aside), and
   17  the receipt hashes the bytes that ran.
   18  """
   19  import argparse
   20  import hashlib
   21  import json
   22  import os
   23  from pathlib import Path
   24  import re
   25  import shlex
   26  import shutil
   27  import subprocess
   28  import sys
   29  import tempfile
   30  
   31  UNVERIFIED = "host busybox, not the candidate's"
   32  
   33  
   34  def cannot(why):
   35      print('melonds-upgrade-test: CANNOT -- ' + why, file=sys.stderr)
   36      raise SystemExit(2)
   37  
   38  
   39  def busybox_origin(path, declared, unverified):
   40      """Where the busybox came from: a build root's image, a named origin, or
   41      nowhere known (only with --unverified-busybox)."""
   42      for directory in path.resolve().parents:
   43          if directory.name == 'system' and directory.parent.name == 'image':
   44              release = directory / 'etc/os-release'
   45              ids = []
   46              if release.is_file() and not release.is_symlink():
   47                  ids = re.findall(r'^BUILD_ID="?([^"\n]*)"?$', release.read_text(), re.M)
   48              if not ids or not ids[-1]:
   49                  cannot(f'{path} is under {directory} but {release} names no BUILD_ID')
   50              return {'kind': 'build-root', 'root': str(directory.parent.parent), 'build_id': ids[-1]}
   51      if declared:
   52          return {'kind': 'declared', 'from': declared}
   53      if unverified:
   54          return {'kind': 'unverified', 'marker': UNVERIFIED}
   55      cannot(f"{path} is not under a build root's image/system/; name its origin with "
   56             '--busybox-from <BUILD_ID|image>, or pass --unverified-busybox (exit 3)')
   57  
   58  
   59  def main():
   60      parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
   61      parser.add_argument('--post-update', required=True, type=Path)
   62      parser.add_argument('--busybox', required=True, type=Path)
   63      parser.add_argument('--busybox-from', help="the busybox's origin when it is not under a build root: a BUILD_ID, or image")
   64      parser.add_argument('--unverified-busybox', action='store_true',
   65                          help='run a busybox of no known origin: every line is marked; exit 3 when every case passed, 1 when one failed')
   66      parser.add_argument('--output', required=True, type=Path)
   67      args = parser.parse_args()
   68      origin = busybox_origin(args.busybox, args.busybox_from, args.unverified_busybox)
   69      mark = ' -- ' + UNVERIFIED if origin['kind'] == 'unverified' else ''
   70      if origin['kind'] == 'build-root':
   71          print(f"busybox: build root {origin['root']}, BUILD_ID {origin['build_id']}", flush=True)
   72      else:
   73          print('busybox: ' + (f"declared from {origin['from']}" if origin['kind'] == 'declared' else UNVERIFIED), flush=True)
   74      source = args.post_update.read_text()
   75      function = re.search(r'^update_melonds_hotkeys\(\) \{.*?^\}', source, re.M | re.S)
   76      legacy = re.search(r'^rm -rf /storage/\.config/melonDS\ncp -r /usr/config/melondDS /storage/\.config/\s*$', source, re.M)
   77      if not function and not legacy:
   78          parser.error('no recognized current function or historical update block')
   79      rows = []
   80      cases = ['missing-defaults', 'missing-config', 'empty-defaults', 'add-missing',
   81               'already-current', 'no-final-newline', 'empty-config', 'file-link',
   82               'directory-link', 'whitespace-key', 'non-hotkey-defaults',
   83               'copy-failure', 'producer-failure', 'rename-failure', 'temp-failure']
   84      with tempfile.TemporaryDirectory(prefix='pixelelated-melonds-') as temporary:
   85          root = Path(temporary)
   86          busybox = root / 'busybox'
   87          shutil.copy2(args.busybox, busybox)
   88          busybox_sha256 = hashlib.sha256(busybox.read_bytes()).hexdigest()
   89          binary = root / 'bin'
   90          binary.mkdir()
   91          applets = [a for a in subprocess.run([str(busybox), '--list'], capture_output=True, text=True).stdout.split() if a != 'sh']
   92          if not {'mktemp', 'cp', 'awk', 'mv', 'rm'} <= set(applets):
   93              cannot(f"{args.busybox} --list lacks the function's applets")
   94          for applet in applets:
   95              wrapper = binary / applet
   96              wrapper.write_text('#!/bin/sh\nexec ' + shlex.quote(str(busybox)) + ' ' + applet + ' "$@"\n')
   97              wrapper.chmod(0o700)
   98          for name in cases:
   99              case = root / (name + ' with spaces')
  100              defaults = case / 'usr/config/melonDS/melonDS.ini'
  101              config = case / 'storage/.config/melonDS/melonDS.ini'
  102              defaults.parent.mkdir(parents=True)
  103              config.parent.mkdir(parents=True)
  104              defaults.write_text('HKKey_New=-1\nHKJoy_Custom=5\nHKJoy_New=4\nScreenLayout=2\n')
  105              original = '# owner settings\nHKJoy_Custom=99\nScreenLayout=7\nOwnerUnknown=yes\n'
  106              config.write_text(original)
  107              config.chmod(0o600)
  108              sentinel = config.parent / 'owner-extra.txt'
  109              sentinel.write_text('keep extra file\n')
  110              expected = original + 'HKKey_New=-1\nHKJoy_New=4\n'
  111              injected = ''
  112              expected_rc = 0
  113              if name == 'missing-defaults':
  114                  defaults.unlink(); expected = original
  115              elif name == 'missing-config':
  116                  config.unlink(); expected = None
  117              elif name == 'empty-defaults':
  118                  defaults.write_text(''); expected = original
  119              elif name == 'already-current':
  120                  config.write_text(expected); original = expected
  121              elif name == 'no-final-newline':
  122                  config.write_text(original.rstrip('\n'))
  123              elif name == 'empty-config':
  124                  config.write_text(''); expected = 'HKKey_New=-1\nHKJoy_Custom=5\nHKJoy_New=4\n'
  125              elif name == 'file-link':
  126                  target = case / 'owner-target.ini'; config.rename(target); config.symlink_to(target); expected = original
  127              elif name == 'directory-link':
  128                  target = case / 'owner-directory'; config.parent.rename(target); config.parent.symlink_to(target); expected = original
  129              elif name == 'whitespace-key':
  130                  original = original.replace('HKJoy_Custom=99', ' HKJoy_Custom = 99')
  131                  config.write_text(original); expected = original + 'HKKey_New=-1\nHKJoy_New=4\n'
  132              elif name == 'non-hotkey-defaults':
  133                  defaults.write_text('ScreenLayout=2\n'); config.write_text(original.rstrip('\n')); expected = original.rstrip('\n')
  134              elif name.endswith('-failure'):
  135                  injected = {'copy-failure': 'cp() { return 1; }',
  136                              'producer-failure': 'awk() { printf "partial output\\n"; return 1; }',
  137                              'rename-failure': 'mv() { return 1; }',
  138                              'temp-failure': 'mktemp() { return 1; }'}[name]
  139                  expected = original; expected_rc = 1
  140              inode = config.stat().st_ino if config.exists() else None
  141              if function:
  142                  command = function.group() + '\n' + injected + '\nupdate_melonds_hotkeys ' + shlex.quote(str(defaults)) + ' ' + shlex.quote(str(config))
  143              else:
  144                  command = legacy.group().replace('/storage/', shlex.quote(str(case / 'storage')) + '/').replace('/usr/config/', shlex.quote(str(case / 'usr/config')) + '/')
  145              result = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
  146                                      timeout=15, env={**os.environ, 'PATH': str(binary) + ':/usr/bin:/bin'})
  147              actual = config.read_text() if config.exists() else None
  148              okay = result.returncode == expected_rc and actual == expected
  149              okay = okay and sentinel.exists() and sentinel.read_text() == 'keep extra file\n'
  150              okay = okay and not list(config.parent.glob('melonDS.ini.??????'))
  151              if config.exists():
  152                  okay = okay and config.stat().st_mode & 0o777 == 0o600
  153              if name == 'file-link':
  154                  okay = okay and config.is_symlink()
  155              if name == 'directory-link':
  156                  okay = okay and config.parent.is_symlink()
  157              if name in ['already-current', 'non-hotkey-defaults'] and config.exists():
  158                  okay = okay and config.stat().st_ino == inode
  159              if okay and name == 'add-missing':
  160                  after = config.stat().st_ino
  161                  repeat = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
  162                                          timeout=15, env={**os.environ, 'PATH': str(binary) + ':/usr/bin:/bin'})
  163                  okay = repeat.returncode == 0 and config.read_text() == expected and config.stat().st_ino == after
  164              rows.append({'case': name, 'pass': okay, 'rc': result.returncode, 'stderr': result.stderr})
  165              print(('PASS ' if okay else 'FAIL ') + name + mark, flush=True)
  166      report = {'pass': all(row['pass'] for row in rows), 'checks': rows,
  167                'legacy_negative_control': not bool(function),
  168                'post_update_sha256': hashlib.sha256(args.post_update.read_bytes()).hexdigest(),
  169                'busybox_sha256': busybox_sha256, 'busybox_origin': origin,
  170                'shimmed_applets': len(applets)}
  171      args.output.parent.mkdir(parents=True, exist_ok=True)
  172      args.output.write_text(json.dumps(report, indent=2) + '\n')
  173      return 1 if not report['pass'] else 3 if mark else 0
  174  
  175  
  176  if __name__ == '__main__':
  177      raise SystemExit(main())
```

## Your first reply (whole)

I reviewed the supplied source excerpts. I did not rerun the suite; execution results below are the first reader’s reported observations, not independently reproduced runs.

## 1. BusyBox fallback and banner

**Read:** `:147–160`, `:234–250`, `:381–426`, `:14235–14238`.

**F-01’s substantive defect is real, but “silently” is inaccurate when a BusyBox is found.**

- After the three searches fail, `:400` returns the host’s BusyBox path—or an empty string with success.
- With host BusyBox, `:426` **does print its banner and source path**. What is missing is an explicit qualification that this is **not candidate-image evidence**, especially in the final verdict.
- With no BusyBox, no copy or wrappers are created (`:415–423`), and the **tool banner** is absent (`:426`). The general suite banner at `:425` still appears. Wrapped commands can then resolve to host tools; this does not guarantee the entire suite will finish, because other cases may require BusyBox-specific paths/applets.

**I recommend refusal, exit 2, for the existing command.** Its foundational requirement is candidate-device applet semantics, not merely finding something named BusyBox. A suitable diagnostic is:

> CANNOT RUN: no candidate image BusyBox found; host tools will not be substituted. Set QA_SYSTEM_ROOT.

An explicitly requested **host-diagnostic mode** could instead exit 3, but it should mark every result as unverified host-tool evidence and finish with **NOT DEVICE EVIDENCE**, never ordinary `PASSED`. Host-diagnostic failures must not masquerade as candidate regressions.

The normal verdict should identify the selected tool provenance, not leave that information hundreds of lines above it. Fixing selection alone also does not fix the unwrapped execution in section **b**; see G-01.

## 2. Sandbox network and environment

**Read:** `:289–295`, `:8895–9032`, particularly `:8993–9022`.

**F-16 is substantially right about `sa_run`’s default sandbox.**

There is no `--unshare-net` or `--clearenv`. `setsid`, `timeout`, filesystem mounts and `--die-with-parent` do not provide either isolation. The helper overrides `PATH` and `HOME`; the harness previously unsets `TMPDIR`. Other exported caller variables remain available, subject to normal executable/setuid sanitization. This is not a claim that every unexported shell variable survives, or that every other sandbox in the suite has this configuration.

The fixture’s alias remote (`:8997`) and route/ping shims (`:8970–8971`) make ordinary execution local; **they do not enforce locality**. Inherited `RCLONE_*` settings can change behavior, and an inherited `BASH_ENV` naming a visible file can affect shell execution. The shared network permits unintended external access.

That matters both for reproducibility and for the claimed safety boundary. The packet establishes no actual external connection, but “no cloud or player-data risk” is stronger than this containment supports.

Use network isolation and an environment allowlist by default, with explicit case-specific exceptions. Sanitize the launcher too: clearing the sandbox environment cannot undo `BASH_ENV` effects on the harness’s own startup.

## 3. `check $?` after compound tests

**Read:** `:270`, `:309–311`, `:481–514`, `:533–604`, `:2086`, `:3013–3062`, `:3324–3329`, `:8776–8787`.

### Correct findings

- **F-11 is correct at `:3051`.** Semicolons separate the three `is` tests; only the final status reaches `check`. A concrete counterexample: make the first `sa` incorrectly produce the **third** case’s expected configuration. The first `is` fails, skipping the second `sa`; the second `is` fails, skipping the third `sa`; the final `is` nevertheless passes on the first run’s files. This is the three-case fallback test, not the separate START NEW GAME check at `:3052`. Record each case separately.
- **Ordinary `[ ... ] && [ ... ] && grep ...; check $?` preserves failure correctly**, as at `:511` and `:8723`: success requires every command to succeed. That validates status propagation, not necessarily the adequacy of the predicates or fixture.
- **F-15 is correct at `:548`.** `!` negates the pipeline’s status, which here comes from `grep`. An unreadable archive/member can therefore become successful “absence.”

**Adding `pipefail` alone does not repair that negative assertion.** A failed producer still gives a nonzero pipeline status that `!` turns into success; `grep -q` can also cause producer SIGPIPE. First require successful extraction into an owned file, then distinguish grep’s **no-match status 1** from its error statuses.

The companion at `:547` is weaker than the first reader suggests: listing `test/f1` does not prove that the particular `system.cfg` member at `:548` exists and was read successfully.

### Corrections and additional sites

- **The Q3 criticism of `:3053` is wrong for a nonzero `sa` return.** Every `sa` there participates in the `&&` chain; its nonzero status cannot be discarded. By contrast, `:3061–3062` really does discard `sa`’s status before checking that no `-e` appeared.
- **The claim that `:3329` passes on empty `F1_WROTE` is also wrong.** The here-string supplies one empty line. At `:3328`, that makes the tested path the existing `${F1}/b/` directory, and the assignment appends a space to `F1_LEFT`; `:3329` then fails. Moreover, `:3326` already rejects an empty `F1_WROTE`.
- **Another negative-pipeline weakness is `:8784`.** A nonempty archive pathname and a readable summary do not prove that the complete archive was successfully scanned for the planted value. Both tar pipelines discard producer failure.
- **`:599` has the same negative-pipeline problem** if the first grep cannot read the output. Its adjacent positive screen assertion may catch the broader failure, but that particular PASS is not evidence of a successful scan.

## 4. Standing of the `--old` controls

**Read:** `:162–226`, `:313–369`, `:1781–1789`, `:1857`, `:2051–2086`, `:3002–3003`, `:14235–14238`; first reader `02`’s control-run table.

The reported twelve runs establish **broken full-run recipes**, not that every earlier observed negative control is worthless. A correctly reached, correctly attributed FAIL before the eventual exit 2 remains evidence for that particular guard. The first reader’s blanket “no controls from s onward” formulation is contradicted by its own reported runs reaching s, t, u and v.

**Do not implement F-05 as “any script absent at BASE_REF makes its section NOT APPLICABLE.”** `src_of`’s refusal protects against grading empty source as a genuine historical implementation. The header even explicitly expects absence of the old proxy script to be a failing observation (`:180–184`).

Distinguish:

1. **Invalid/unavailable ref or unreadable required input:** CANNOT, exit 2.
2. **A required historical feature is absent:** an explicit presence-contract failure may be valid, but it does not demonstrate execution of a behavioral guard.
3. **An unrelated, newer section excluded from a particular control’s declared scope:** legitimately unselected/not applicable.
4. **A selected check that cannot execute:** incomplete/SKIP, not PASS. If execution continues, preserve that incompleteness in the summary and exit policy.

The useful fix is **per-control selection with explicit fixture dependencies and expected failing check IDs**, plus ref/input preflight. Section t must also select the historical package pin, not mix current source with old patches.

A genuinely retired feature can be outside the current product’s test obligations. That is why **F-08’s categorical objection to N/A is not sound**. The important question is whether the availability gate establishes retirement or merely mistakes a missing required file for retirement; that gate is absent from this packet.

## 5. Splitting the file

**Read:** `04` § Q6, the section/group index, `:320–369`, `:8684–8715`, `:8993–9022`, `:14177–14238`.

I agree with a **subject-oriented split**, and with establishing smaller independently runnable controls before physically splitting everything.

The costs are real: fixtures currently depend on earlier sections’ globals and artifacts; tool selection/copying, source selection and sandbox policy need shared implementations; result aggregation must preserve FAIL, CANNOT and SKIP rather than flattening every nonzero child status.

The gains are maintainability, independently selectable controls, clearer attribution and explicit dependencies—not automatically shorter full-suite runtime. A split alone also does not solve historical applicability.

Two qualifications to the proposal:

- The quoted **2,166-line maximum** describes stream A, not the proposed combined cloud subject file containing A, CF and other sections.
- **ae is not wholly retired**: `:14183–14189` deliberately retains live archive contracts after retiring the migration matrix.

**Yes to the cheaper half first—but not its blanket N/A implementation.** Add control selection, explicit setup dependencies and reliable completeness reporting first.

## Findings F-01 to F-21

| Finding | Review | Reason and lines |
|---|---|---|
| **F-01** | **confirmed with narrowing** | Automatic host/no-BusyBox fallback is real (`:400–423`), and the verdict is unqualified (`:14236–14238`); host BusyBox is nevertheless disclosed by `:426`, so it is not literally silent. |
| **F-02** | **confirmed with narrowing** | rclone has the same unverified selection (`:8908–8914`), but its provenance is printed; compatible behavior under two versions is not itself a test defect or a reason to demand an artificial version-sensitive failure. |
| **F-03** | **confirmed** | Historical read failures do not reliably propagate: the pipeline and final `true` defeat failure handling (`:3208–3214`), and `git show` at `:4271` is unchecked and silenced; downstream failures are not a proper input preflight. |
| **F-04** | **confirmed with narrowing** | The reported runs establish that the refs documented at `:185` and `:191` are unresolved in that checkout; neither global disappearance nor the suggested replacement refs is independently established here. |
| **F-05** | **confirmed with narrowing** | Required-source failure exits the whole run (`:320–325`), making the reported recipes incomplete; that refusal is intentional protection, and automatic N/A is not a sound general replacement. |
| **F-06** | **confirmed** | The pin is read from the working tree (`:2051`) while patches come from `BASE_REF` (`:2075–2083`), contradicting the historical-client claim at `:2034–2036`. |
| **F-07** | **cannot tell from the packet** | The calls pass the copied BusyBox (`:14224–14232`), but the callee validation code is absent and cited at another revision; `02` reports both calls passing at the audited baseline. |
| **F-08** | **refuted** | N/A is explicitly not counted as PASS (`:14235`); excluding a genuinely retired feature can coexist with passing applicable checks. Whether the omitted availability gate wrongly declares retirement remains unresolved. |
| **F-09** | **cannot tell from the packet** | No-BusyBox probe omission is visible (`:8776–8812`), but the download/DT_OK/qemu gates are mostly absent; the explicit group SKIP at `:2059` is not itself a false pass. |
| **F-10** | **confirmed with narrowing** | Failed startup can satisfy individual assertions at `:573`, `:594`, `:8787` and `:8828`; this does not establish whole-suite false success, and the criticism of nonzero `sa` at `:3053` is incorrect. |
| **F-11** | **confirmed** | The final `is` alone determines the recorded status at `:3051`, and it can accept output left by an earlier incorrect run while intervening runs were skipped. |
| **F-12** | **confirmed** | `:13826` supplies two arguments; on failure, `check` expands absent `$3` (`:309–310`) under `set -u` (`:270`) and aborts before counting/reporting the FAIL. |
| **F-13** | **confirmed with narrowing** | `:1835` reports `wait` rather than the sourced pass’s status, and `:1840` pre-creates markers; however, positive start/stop log checks at `:1846–1854` reject a wholesale no-op. |
| **F-14** | **confirmed** | At `:2086`, only `TPATCH_OK` determines the result; compilation occurs inside message construction and cannot make that check fail. |
| **F-15** | **confirmed with narrowing** | `:548` converts extraction failure into successful absence; `:547` checks a different member, not successful reading of `system.cfg`. The same producer-status weakness appears at `:8784`. |
| **F-16** | **confirmed with narrowing** | The default helper shares the network and retains unspecified exported environment (`:9013–9021`); PATH/HOME are overridden, TMPDIR was removed, and actual external access is not demonstrated. |
| **F-17** | **cannot tell from the packet** | The named g/h/i, t and C7 bodies are absent; the independently visible historical-pin mismatch at `:2051` is already F-06. |
| **F-18** | **confirmed with narrowing** | Help overclaims image-tool execution (`:241`) and the header is incomplete (`:7–226`); however, foreground `setsid -f` from a clean parent can avoid shell-background SIGINT inheritance—it merely cannot reset an already ignored signal (`:258–268`). |
| **F-19** | **cannot tell from the packet** | The actual canary construction, execution context and cleanup at the claimed `:13672–13678` sites are not supplied. |
| **F-20** | **confirmed with narrowing** | The probes establish “BusyBox,” not candidate identity (`:8777–8779`, `:8809–8811`); the reported host 1.37 **does not pass these probes**, because it lacks flock. Provenance is chiefly the central F-01 issue. |
| **F-21** | **cannot tell from the packet** | The unzip test and its availability gate at `:13400–13424` are not supplied; the general tool-provenance problem alone does not verify this particular branch. |

## Additional findings / omissions from the F-list

- **G-01 — Medium: candidate BusyBox selection does not ensure candidate applet execution.** Section b’s profile selects `/shim:/usr/bin:/bin` (`:522`), and its sandbox mounts neither the BusyBox copy nor its wrappers (`:536–541`); normal tar delegation uses host `/usr/bin/tar` (`:566`, `:586–590`). Thus the original whole-script kill/restore tests remain host-tool tests even after F-01 is fixed. The first reader notes the missing wrappers in its table but does not carry this independent defect into the findings.

- **G-02 — Medium: `LAST_GOOD_SOURCE_ROOT` also replaces one verifier.** Help promises a separate source checkout **without replacing this harness** (`:248–249`), but ag executes `${ROOT}/tools/settings-modes-test` (`:14224`), whereas ae and ah use `${HARNESS_ROOT}` (`:14188`, `:14231`). Selecting an older/different subject checkout can therefore select a missing or weaker checker. ag should use the harness-owned verifier.

- **G-03 — Low: q’s historical fragment set is the intersection of two trees.** `:1781–1789` enumerates current working-tree filenames, then reads their historical contents and excludes names absent historically. A fragment present only at `BASE_REF` can never run. This undermines the promised whole historical boot pass independently of source-read failure; enumerate the selected ref’s own tree.

- **G-04 — Medium: the corekeeper contention test does not establish overlap.** `:8854–8860` uses sleeps rather than acquisition/entry acknowledgments. If the second handler starts late, the midpoint sees no note and both archives eventually exist—even with broken locking. Use bounded barriers proving that the first handler holds the protected operation and the second has reached it before testing that it waits.

## Sections I need

- **F-08:** `x/C :4540–4565`, plus `aa :13723–13740` and `:13890–13912`, to inspect the retirement/applicability decision.
- **F-09:** `x/F2 :3990–4015` and `:4290–4310`; `x/C :6475–6495`; `x/D :6635–7795` for the DT_OK definition and guarded branches; `y/A :10120–10365`; `y/F1r :11170–11205`.
- **F-17:** `g–i :839–933`, `t :2410–2445`, and `x/C7 :6495–6525`.
- **F-19/F-21:** `z/S3F :13665–13722` and `z :13390–13430`.
- **F-07 requires external code, not another section of this file:** the argument/provenance validation and exit contracts of `settings-modes-test` and `melonds-upgrade-test`, identifying what exists at `8ebaf8daad` versus the later T14 revision cited by the reader.

## The first packet (whole, for reference)

# Independent review: M6 T15, `tools/last-good-scripts-test` (#662)

You are the independent reviewer for one slice of a code audit. You come from another lab than the first reader (Claude Opus 5.5). The subject is **one bash test suite, `tools/last-good-scripts-test`**: 14,238 lines and 1,167,697 bytes at commit `8ebaf8daad`. It runs the operating system's shell scripts (backup, cloud sync, settings writers, boot quirks) whole, inside `bwrap` sandboxes on a build host, against fixtures, **under the device's own BusyBox applets** (that was its founding lesson, blindspot 34: a check passed under GNU `tr` and failed on every device under busybox `tr`). The file is too large to send whole. This packet carries:
- the section index and the groups;
- the harness (`:1-430`);
- the history helpers;
- stream A's sandbox helpers;
- the call sites and the verdict;
- the sections the first reader's Q3 names as suspect, each whole and line-numbered;
- the first reader's `02`, `03` and `04` whole;
- two rule sections that define what a guard must do.

**If you need other sections to judge a claim, name them by letter or line range at the end of your reply, under `## Sections I need`.** They will come in a second packet.

**Answer these first, each with the lines you read:**
1. **The busybox fallback and its banner** (`:381-426`). Is the first reader's F-01 right? It says that with no `QA_SYSTEM_ROOT` and no build root reachable by the three globs, the suite takes the host's busybox silently, or runs on GNU tools with no banner when there is none. What should the verdict say, and what should the run do (refuse, as exit 2, or mark every line, as exit 3)?
2. **The sandbox's network and environment** (`sa_run`, `:9010-9022`). Is F-16 right that the host network and the caller's environment reach every script it runs, and does it matter for what this suite proves?
3. **`check $?` after compound tests.** Are the first reader's sound and unsound cases right (F-11 at `:3051`; F-15's `! tar | grep -q`; the `[ ] && [ ] && grep` chains judged sound)? Find any it missed in the excerpts.
4. **The `--old` controls' standing** (the header's recipes `:162-226`; `src_of` `:320-325`). The first reader ran all twelve: all exit 2, two refs dead, and ten stopped where `src_of` meets a script the ref predates. Is its proposed fix right (F-05: a script absent at `BASE_REF` makes its section NOT APPLICABLE)? Or does that weaken "a check that cannot run has not passed"?
5. **The file's split** (`04` § Q6's proposal). Do you agree with the cost and gain, and with the cheaper half first?

**Then refute or confirm every finding F-01 to F-21 in `04`.** One line each:
- `confirmed`, `confirmed with narrowing`, `refuted` or `cannot tell from the packet`;
- why, and the line;
- add any finding the first reader missed, as G-n.

Be concrete and cite lines. Severity is yours to challenge. Do not restate the packet.


## The section index (every `echo "  <letter>. "` line, at 8ebaf8daad)

```text
  429  echo "  a. chksysconfig keeps and restores the last good system.cfg"
  518  echo "  b. backuptool: a kill mid-tar leaves the previous archive; a failed restore puts the snapshot back"
  607  echo "  c. set_setting is one rename; sort_settings refuses an empty result"
  650  echo "  d. cloud_sync_helper and the saves scripts keep the config's last good copy; stamps survive a kill"
  723  echo "  e. nothing a screen can show carries an exit code, a log path, a tool's name or a flag"
  766  echo "  f. backuptool: rclone.conf never enters an archive, and the scanner knows rclone's key names (#52)"
  839  echo "  g. the in-script RCLONE_NET_OPTS fallback is the shipped value (#146)"
  854  echo "  h. the rclone wrapper: an automatic run's stalled call ends at the ceiling, a deliberate run's at the stall ceiling (D-CLOUD-118, D-CLOUD-126)"
  893  echo "  i. cloud_net_ready settles on a held default route however NetworkManager judges connectivity"
  934  echo "  j. cloud_sync_helper migrates the shipped retry bound once, and leaves a hand-tuned value alone (#107)"
  962  echo "  k. backuptool: what the image ships does not travel, and an older archive's copy of it is not put back (#45); a RetroAchievements token travels in no shape (#169)"
 1114  echo "  l. a missing cloud folder reads as not there yet whatever the server's words (#142)"
 1251  echo "  m. the shipped device name becomes this unit's own, once; a player's name is never touched (#50)"
 1403  echo "  n. a deliberate cloud_backup ends a transfer that stops making progress at the stall ceiling, and says it couldn't finish (D-CLOUD-126)"
 1534  echo "  o. set_setting system.hostname default keeps the line chksysconfig's sentinel reads, empty (D-NET-009)"
 1565  echo "  p. raofflineproxy-ctl: enable records hardcore and turns it off, disable puts it back; both harmless twice (#165, D-RA-002); pending and flushed answer the sync cards (#173); pending-ids and account answer the achievements pages (#180)"
 1752  echo "  q. 099-networkservices: a daemon fragment that sets no CONF inherits none from the fragment before it (#166)"
 1860  echo "  r. the launch log carries no credential value: setsettings' Added setting and Fetch lines, runemu's Executing line, the helper's shapes (#176, D-INFRA-010)"
 1949  echo "  s. rocknix-evidence: every file in the bundle has been through the credential filter, summary.txt says so, and without the filter nothing is collected (#176)"
 2033  echo "  t. raofflineproxy-ctl scan, topup and ready against the client the tree describes: the refusals, the index rule by account and hash, the probe's own folder and patience, one deadline, the failure verdict, the cap over uncached files, a stop on disable, and the patched client's own predicates (#186 PL-01..05, 12, 17, 23, 24, 25, 28, 30, 33; #190; #194; #199)"
 2856  echo "  u. wifictl current, saved, forget and join read NetworkManager, not the setting; forget says when it dropped the connection; join activates the saved profile and moves the settings onto it (#191)"
 2991  echo "  v. the save state manager's arguments reach RetroArch as Batocera's launcher carries them (#196, D-UI-057): runemu reads -state_slot, -autosave and -state_file each on its own and takes the path whole; setsettings turns a .auto file into savestate_auto_load and any other into -e <slot>; without -state_file, today's lines byte for byte"
 3067  echo "  w. cheevos_armsx2.sh writes one Token line to secrets.ini, however often it runs (#170)"
 3113  echo "  x. the launcher's incremental-save modes, the password's handoff, and the keeper's cut/whole note (#209, #198, #247)"
 7796  echo "  y. audit #307 / #308, stream B: backuptool, wifictl, the settings writer and lock, factoryreset, chksysconfig, rocknix-evidence, rocknix-corekeep, runemu and automount"
13182  echo "  z. the audit of the fix round, stream B: the conf read as text, a flag's password redacted, the restore's lists and its own control files, a quoted password, the roms mount, the upstream-era move, a zip's stored members, members outside storage/, the lock's path, the seed list, the Wi-Fi pair"
13723  echo "  aa. cloud_migrate_layout --state, --keep and --follow (#353, D-CLOUD-160/161): the layout as facts, a kept folder, the fleet followed"
13913  echo "  ab. cloud_scan (#350, D-CLOUD-156): the opening scan's three items, the content scan's one, the selected folder facts and the failures said"
14121  echo "  ac. the Retroid Pocket Nova's ledcontrol (#332): LED BRIGHTNESS writes the LEDs, rgb with no colour set lights white, off zeroes"
14142  echo "  ad. a backup does not make a missing earlier-default saves folder (D-CLOUD-172, #363): the offer instead, nothing written"
14177  echo "  ae. cloud folder state table and archive writer/reader contracts (#365, #383)"
14191  echo "  af. content inactivity across provider retries (#401)"
14221  echo "  ag. settings writers retain private file permissions"
14229  echo "  ah. melonDS update preserves settings and adds missing hotkeys"
```

The groups inside x, y and z (echoed, or comment-headed):

```text
 3198  echo "  F1. GENERIC_X64, the developers' QA device (D-QA-053): the boot quirks write only what a guest keeps, the serial shell stays on a VM, the launcher's print verb touches nothing (#307 PL-019, PL-022, PL-023, PL-033, PL-034, PL-073; #308)"
 4540  echo "  C. the cloud sign-in broker and setup (audit #307 stream C)"
 6635  echo "  D. audit #307 stream D: the offline-achievements service -- the control script, its helpers, the client's patches, the unit and the emulators' cheevos scripts (#307 PL-013, 055, 057, 058, 059, 060; #308's sweep)"
 7799  # y1. backuptool whole, the device's applets in front of the host's, a fake
 8397  # y2. wifictl whole, against an nmcli that answers as the target's does
 8607  # y3. 001-functions: the settings writer, the lock and the redaction, lifted
 8684  # y4. chksysconfig's boot pass, factoryreset, rocknix-evidence,
 8906  echo "  A. audit #307/#308, stream A: the cloud scripts against the image's rclone"
11072  echo "  F1r. The audit of the fix round, stream F1 (#309 PL-024; the gpt seat's G2-F1 leads): each check names its item"
11224  echo "  CF. the audit of the fix round, stream C (D-WORKFLOW-060)"
13592  echo "  S315. #315: the size-only remote gets --update on every saves pass; every other remote nothing; the detection's edges"
13665  echo "  S3F. the audit of the fixes: shell-owned names and NUL bytes refused by the grammar; the sorter's pipeline gates its rename; the ZIP listing's CRC column asserted; the restore gate's mount state; the pointer reader; the scrubber's truncated line; the ack's rename"
```

## Excerpt: the harness: header, dispatch, check/skip/src_of, image_tool_source, the busybox copy (`:1-430` at 8ebaf8daad)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # last-good-scripts-test - a device-less check that the scripts keep the last
    6  # known good state when they are killed mid-write (D-CLOUD-078, fork #105):
    7  #
    8  #   a. chksysconfig: verify with an empty system.cfg and a valid .backup
    9  #      restores the backup, not the image defaults; backup with an empty
   10  #      current file leaves .backup unchanged;
   11  #   b. backuptool backup killed mid-tar (a tar shim that writes 1 MiB and
   12  #      SIGKILLs the whole process group) leaves the previous archive as the
   13  #      only *.tar.gz at the root and a .partial beside it; a restore whose
   14  #      extraction fails puts the pre-restore snapshot back and says so;
   15  #   c. set_setting is one rename: the single sed produces the right file for
   16  #      values carrying /, & and spaces, deletes on "default", and gives an
   17  #      empty file its one line -- there is no longer a step between delete
   18  #      and add for a kill to land in;
   19  #   d. write_stamp killed mid-write leaves the previous stamp;
   20  #   e. every line the scripts can print to a screen is free of exit codes,
   21  #      log paths, tool names and flags (the harness's FORBIDDEN regex).
   22  #   f. backuptool never archives rclone.conf and its scanner knows rclone's
   23  #      key names (#52);
   24  #   g. each script's RCLONE_NET_OPTS_FALLBACK equals the shipped
   25  #      RCLONE_NET_OPTS, so a torn conf does not silently restore #107 (#146).
   26  #   h. --automatic's rclone wrapper ends a stalled call at the ceiling and
   27  #      returns 124; a deliberate run's is ended at the stall ceiling and
   28  #      returns 124 too, while one that finishes returns its own status;
   29  #      why_for says what 124 means to each; the automatic fallback equals
   30  #      the shipped value (D-CLOUD-118, D-CLOUD-126).
   31  #   i. cloud_net_ready settles on a held default route in any connected
   32  #      NetworkManager state; a still-connecting network exits 69 at the deadline.
   33  #   j. cloud_sync_helper migrates the pre-#107 retry bound once, with a marker,
   34  #      and leaves a hand-tuned value alone.
   35  #   k. backuptool leaves out what the image ships (a file identical to its
   36  #      /usr/config copy; PPSSPP's assets and shader cache always), and a
   37  #      restore of an older archive does not put those back (#45).
   38  #   l. a missing cloud folder reads as not there yet whatever the server's
   39  #      words: absent_not_broken walks up to the nearest listable parent, the
   40  #      setup wizard carries the same function, the content backup makes its
   41  #      folder before copying (#142).
   42  #   m. network-base-setup gives the shipped device name (the build family) a
   43  #      per-unit suffix once and writes it back; a name the player typed, or
   44  #      another family's, is left alone; the script no longer calls hostnamectl and
   45  #      the unit orders before systemd-hostnamed and NetworkManager (#50).
   46  #   n. a deliberate cloud_backup whose rclone stops making progress is ended
   47  #      at the stall ceiling (rclone's idle timeout plus a grace, sized from
   48  #      RCLONE_NET_OPTS): exit non-zero, no success stamp, the why on the
   49  #      protocol line and Couldn't finish ... Try again. as the outcome line;
   50  #      a run that completes ends on Completed. and stamps 0; a transfer that
   51  #      keeps moving past the ceiling is not ended (D-CLOUD-126, #153).
   52  #   o. set_setting system.hostname default (and del_setting) leaves an empty
   53  #      system.hostname= line rather than none, so chksysconfig still reads
   54  #      the file as usable and network-base-setup gives the unit its own name
   55  #      at the next boot; any other key deleted with default is removed as
   56  #      before (D-NET-009, #154).
   57  #   p. raofflineproxy-ctl, the OFFLINE RETROACHIEVEMENTS toggle's backend
   58  #      (#165, D-RA-002): enable writes the marker the unit conditions on,
   59  #      starts the service, records the hardcore setting as it was and turns
   60  #      it off; disable stops, removes the marker and puts hardcore back as
   61  #      recorded; both are harmless run twice; a service that will not start
   62  #      leaves the settings untouched and the marker gone; the last stdout
   63  #      line is hardcore=<0|1> and nothing else is printed. And in k: the
   64  #      proxy's folder under /storage/.config is held back whole from a
   65  #      backup and never put back on a restore (its token cache and award
   66  #      queue, D-INFRA-010). Then the two answers the sync cards ask for
   67  #      (#173, D-RA-004): pending counts the pending rows of a fixture store
   68  #      shaped like the proxy's (0 and 1, exit 1 and 0; 0 with the toggle
   69  #      off; exit 2 and nothing on stdout when the store cannot be read),
   70  #      and flushed prints the service's last-flush stamp once and removes
   71  #      it (exit 1 when there is none, or none worth the name). Since audit
   72  #      #186: an enable whose settings write fails at any of its three
   73  #      writes leaves the device as it was (PL-16); a flush stamp the service
   74  #      replaces between the read and the remove is the next caller's, not
   75  #      lost (PL-32); a cached sign-in without points answers exit 1, never
   76  #      0 points (PL-26).
   77  #   q. 099-networkservices, the boot pass over /usr/lib/autostart/daemons/*:
   78  #      a fragment that sets no CONF inherits none from the fragment before
   79  #      it, so the marker the previous fragment wrote (raofflineproxy.conf,
   80  #      smb.conf) is still there when the backgrounded systemctl start reads
   81  #      the unit's ConditionPathExists; the pass still removes the marker and
   82  #      stops the service when the toggle is off (#166).
   83  #   r. the launch log carries no credential value: setsettings' Added setting
   84  #      and Fetch lines, runemu's Executing line and loginit header, and the
   85  #      shapes redact_credentials (001-functions) knows -- the key or flag
   86  #      kept, the value <redacted>, an empty value left empty, a value under
   87  #      a plain key untouched, and RetroArch's appendconfig still carrying the
   88  #      real password, since only the log is redacted (#176, D-INFRA-010).
   89  #   s. rocknix-evidence: no planted value survives into the archive or a
   90  #      snapshot page (a process list can carry --ra-password), the key names
   91  #      do, summary.txt says the filter ran and over how many files, and
   92  #      without the helper nothing is collected and no page is written (#176).
   93  #   t. raofflineproxy-ctl scan, topup and ready (#179, #184; audit #186
   94  #      PL-05), against the client the tree describes -- its tarball from
   95  #      the sources cache with the package's patches applied in order, the
   96  #      client's own probe, smart cache and helper shimmed, a virtual clock
   97  #      (date +%s and sleep are shims over /run/clock): the four refusals
   98  #      with no stamp; the listing follows the index and asks "cached" of
   99  #      this account's rows and this hash (PL-23, PL-02); the probe writes
  100  #      its own folder and never the service's online_state.json (PL-03);
  101  #      the top-up probes with the token check's patience and marks the
  102  #      attempt only after an answer (PL-04); one deadline over the lock
  103  #      wait, the listing and both passes (PL-28); a failed game ends the
  104  #      run COULDN'T FINISH (PL-24); the helper's DONE is the verdict and a
  105  #      kill after it is not (#188); the progress file while the jobs run
  106  #      (#189); the walk's cap counts uncached files
  107  #      (PL-17); disable stops a running run (PL-30); refresh with a bad
  108  #      argument exits 64, an images run writes route=images at=<epoch> and
  109  #      disable ends its helper too (audit #258 PL-012/PL-013). And the client's own
  110  #      predicates, from the patched tree: the refresh bound and the
  111  #      surviving thread (patch 005, PL-01/PL-25), a game evicted whole
  112  #      (006, PL-02), the configured account's cached sign-in (007, PL-23),
  113  #      the log upload gated off (008, PL-12), a badge temp name per thread
  114  #      (009, PL-33), a store-only request served from the store (010, #190),
  115  #      the store's login answer marked X-RA-Offline: 1 and every answer
  116  #      X-RA-Proxy: 1 (011, #194), an image the store does not hold answered
  117  #      404 at once through the whole request handler -- store-only, or the
  118  #      process's own state offline -- with is_online never asked and nothing
  119  #      fetched, while a hit is served and a miss with the state online still
  120  #      asks the link and fetches (012, #199).
  121  #   u. wifictl current, saved, forget and join (#191), the four verbs the network
  122  #      rows read NetworkManager through: saved lists every wireless profile
  123  #      as <name><TAB>active|saved, the one in use first, a wired profile
  124  #      never, a colon in a name unescaped as nmcli -t escapes it; current
  125  #      prints the joined network's SSID, nothing and exit 1 when joined to
  126  #      none; forget deletes exactly the named profile -- a name with a space
  127  #      and a colon -- and says disconnected on a second line when it was the
  128  #      one in use; a name that is not a remembered wireless network, an
  129  #      empty one, or a NetworkManager that does not answer is a refusal
  130  #      with nothing printed and nothing deleted, and saved and current tell
  131  #      "no answer" from "none" (exit 1 and 2) rather than reading a silence
  132  #      as an empty list.
  133  #   v. the save state manager's arguments reach RetroArch as Batocera's
  134  #      launcher carries them (#196, D-UI-057): runemu's
  135  #      parse_savestate_arguments reads -state_slot, -autosave and -state_file
  136  #      each on its own -- once es_savestates.cfg is there the interface sends
  137  #      "-autosave 0" alone for START NEW GAME and "-autosave 1 -state_file
  138  #      <auto>" for the AUTO SAVE tile -- and takes the path whole (spaces,
  139  #      parentheses, " - "); setsettings reads --state_file= ahead of
  140  #      --controllers= and set_autosave turns a .auto file into
  141  #      savestate_auto_load and any other into " -e <slot>" on stdout, spliced
  142  #      before --config like --host; a slot that is not a number gets no -e;
  143  #      without -state_file the appendconfig is today's, byte for byte.
  144  #   w. cheevos_armsx2.sh writes one Token line to secrets.ini however often it
  145  #      runs, and gives a secrets.ini without the section its header once (#170).
  146  #
  147  # The chksysconfig and 001-functions functions are lifted out of the files
  148  # under test and run in a fresh bash against temp paths, as wait-lock-test
  149  # does. backuptool is run WHOLE and unmodified inside bwrap, with a stub
  150  # /etc/profile, a fake /storage and PATH shims (logger, systemctl, sleep,
  151  # and the tar that dies) -- bubblewrap needs no user namespace here, only
  152  # setuid or an allowing profile. sed, mv, cp, tr, head, wc, cut and awk --
  153  # and, in k, tar and unzip; in m, the same applets under network-base-setup
  154  # -- are the image's busybox when its build root is on this machine, the
  155  # host's otherwise -- every external command a check under test leans on
  156  # that IS a busybox applet on the device (grep and sort there are GNU, and
  157  # the image's busybox has no grep applet), not only the ones already known
  158  # to differ: chksysconfig's text test passed here for a day under GNU tr and
  159  # failed on every device under busybox tr (2026-09-10), so the checks in a.
  160  # run through the image's binary.
  161  #
  162  # To watch the guards fire, point it at the scripts from before the change.
  163  # Every case that runs or lifts a script takes it from BASE_REF under --old
  164  # (src_of), so a case whose FAILs have never been seen is a case with no
  165  # evidence (#151 PL-10):
  166  #
  167  #     tools/last-good-scripts-test --old      # a, b, c, d, e, f, j, k, l, m
  168  #                                             # FAIL against 1d1503180d
  169  #     BASE_REF=53f390b1e9 tools/last-good-scripts-test --old
  170  #                                             # k, l, m FAIL: the scripts from
  171  #                                             # before #45, #142 and #50
  172  #     BASE_REF=c15050c897 tools/last-good-scripts-test --old
  173  #                                             # a FAILS: the text test that
  174  #                                             # busybox tr never passed
  175  #     BASE_REF=8707919349 tools/last-good-scripts-test --old
  176  #                                             # h (the deliberate stall, the
  177  #                                             # deliberate why), n and o FAIL:
  178  #                                             # the scripts from before #153
  179  #                                             # and #154
  180  #     BASE_REF=34aca64afd tools/last-good-scripts-test --old
  181  #                                             # k's proxy-folder checks FAIL
  182  #                                             # (the folder travelled) and p
  183  #                                             # FAILS whole: the tree before
  184  #                                             # #165 has no raofflineproxy-ctl
  185  #     BASE_REF=0f7785e6ed tools/last-good-scripts-test --old
  186  #                                             # q FAILS: the boot pass before
  187  #                                             # #166 removed raofflineproxy.conf
  188  #                                             # through 007-syncthing (and
  189  #                                             # smb.conf through 004-tailscaled,
  190  #                                             # at every BASE_REF: upstream's leak)
  191  #     BASE_REF=d79281066c tools/last-good-scripts-test --old
  192  #                                             # p's pending and flushed checks
  193  #                                             # FAIL: the ctl before #173 has
  194  #                                             # neither verb (usage, exit 2)
  195  #     BASE_REF=cee1656c33 tools/last-good-scripts-test --old
  196  #                                             # the audited tip of #163: p's
  197  #                                             # PL-16/26/32 checks, r's three
  198  #                                             # PL-29 canaries and t's fix
  199  #                                             # checks FAIL (the audit's
  200  #                                             # findings, each seen to fire)
  201  #     BASE_REF=28a80357ed tools/last-good-scripts-test --old
  202  #                                             # r and s FAIL: the scripts from
  203  #                                             # before #176 -- the password in
  204  #                                             # exec.log's Added setting and
  205  #                                             # Fetch lines, in the bundle and
  206  #                                             # in a snapshot page, and a
  207  #                                             # collect that runs with no filter
  208  #     BASE_REF=3387cf5da0 tools/last-good-scripts-test --old
  209  #                                             # t's #188 and #189 checks FAIL:
  210  #                                             # the ctl from before the DONE
  211  #                                             # verdict and the progress file
  212  #     BASE_REF=655f103cc5 tools/last-good-scripts-test --old
  213  #                                             # u FAILS whole: the wifictl
  214  #                                             # from before #191 has none of
  215  #                                             # current, saved and forget
  216  #                                             # v FAILS: the launcher before
  217  #                                             # #196 has no parse function
  218  #                                             # and no --state_file= parser
  219  #     BASE_REF=70b6c70ca7 tools/last-good-scripts-test --old
  220  #                                             # t's four 012 checks FAIL: the
  221  #                                             # client before #199 asks
  222  #                                             # is_online about every image
  223  #                                             # (its log line), again about
  224  #                                             # one it does not hold, and
  225  #                                             # fetches it; a miss is a 200
  226  #     tools/last-good-scripts-test            # PASSED
  227  #
  228  # One FAIL in m that names "the built image" is about the build root on this
  229  # machine, not the tree: case m grades the avahi unit the image ships, and a
  230  # root built before the avahi recipe removed the stock units (#151 PL-01)
  231  # holds the wrong one until avahi and the image are rebuilt. It is a true
  232  # statement about that image and is left to fail rather than softened.
  233  #
  234  # Exit 0 when every check passes, 1 otherwise, 2 when it cannot run.
  235  # Dispatch before signal checks or fixture creation: help must never run tests.
  236  case "${1:-}" in
  237    -h|--help)
  238      [ "$#" -eq 1 ] || { echo "usage: last-good-scripts-test [--old | --cloud-layout [options]]" >&2; exit 2; }
  239      cat <<'USAGE'
  240  Usage: tools/last-good-scripts-test [--old | --cloud-layout [options]]
  241  Run the host script regression suite with the image's busybox.
  242    --old           Test BASE_REF (default 1d1503180d), for failing controls.
  243    --cloud-layout  Run only the layout suite; remaining options go to it.
  244    -h, --help      Show this help without creating fixtures or running tests.
  245  Run in the foreground; the full suite requires a usable SIGINT handler.
  246  QA_SYSTEM_ROOT names the candidate's image/system directory for BusyBox and
  247  rclone. An unusable explicit input is an error, never a fallback to another build.
  248  LAST_GOOD_SOURCE_ROOT selects a separate source checkout without replacing this
  249  harness. Historical --old still reads BASE_REF from that checkout.
  250  USAGE
  251      exit 0 ;;
  252    --cloud-layout) shift; exec "$(dirname "$(readlink -f "$0")")/rasteratops-cloud-layout-test" "$@" ;;
  253    --old) [ "$#" -eq 1 ] || { echo "--old accepts no additional arguments" >&2; exit 2; } ;;
  254    '') [ "$#" -eq 0 ] || { echo "empty argument is not an option" >&2; exit 2; } ;;
  255    *) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
  256  esac
  257  
  258  # Refuse to run with SIGINT ignored at entry. A shell background job (`cmd &`
  259  # in a non-interactive shell -- a harness waiter, `setsid nohup ... &`) starts
  260  # with SIGINT set to SIG_IGN, every sandboxed script inherits it across exec,
  261  # and bash cannot trap a signal ignored at entry: the scan-cancel checks then
  262  # see the run complete with rc 0, twice on 2026-09-25, while the same file
  263  # passed in the foreground and on the guest. Start it in the foreground or
  264  # with `setsid -f`, which forks without a shell job.
  265  if [ $(( 0x$(awk '/^SigIgn/{print $2}' /proc/self/status) & 2 )) -ne 0 ]; then
  266      echo "last-good-scripts-test: SIGINT is ignored in this process (started as a shell background job?); the cancel checks cannot run -- start it in the foreground or with setsid -f" >&2
  267      exit 2
  268  fi
  269  
  270  set -u
  271  
  272  HARNESS_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
  273  ROOT="$(cd "${LAST_GOOD_SOURCE_ROOT:-${HARNESS_ROOT}}" && pwd)" || exit 2
  274  [ -f "${ROOT}/projects/ROCKNIX/packages/network/rclone/package.mk" ] || { echo "last-good-scripts-test: source checkout has no rclone recipe" >&2; exit 2; }
  275  BASE_REF="${BASE_REF:-1d1503180d}"
  276  OLD=0
  277  [ "${1:-}" = "--old" ] && OLD=1
  278  
  279  CHK_REL=projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
  280  BT_REL=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
  281  FN_REL=projects/ROCKNIX/packages/rocknix/profile.d/001-functions
  282  NBS_REL=projects/ROCKNIX/packages/sysutils/systemd/scripts/network-base-setup
  283  WIFICTL_REL=projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl
  284  RCLONE_REL=projects/ROCKNIX/packages/network/rclone/sources
  285  
  286  command -v bwrap >/dev/null || { echo "needs bubblewrap (bwrap)" >&2; exit 2; }
  287  command -v setsid >/dev/null || { echo "needs setsid" >&2; exit 2; }
  288  
  289  # Honor the caller's build-drive TMPDIR for the owned host fixture tree.
  290  # Host compilers and patch commands below explicitly use this owned tree too.
  291  # Bubblewrap descendants get a private /tmp, so an inherited host-only path
  292  # makes otherwise valid mktemp calls fail inside the device fixture.
  293  TMP="$(mktemp -d)" || { echo "cannot create host fixture directory" >&2; exit 2; }
  294  trap 'rm -rf "${TMP}"' EXIT
  295  unset TMPDIR
  296  FAIL=0
  297  SKIPPED=0
  298  NOT_APPLICABLE=0
  299  # skip <text>: a check that did not run is counted, never folded into PASSED
  300  # (audit of the fix round PL-023): the verdict says how many, and exits 3
  301  # when nothing failed but something was skipped -- vm-qa reads 3 as SKIP.
  302  skip() { SKIPPED=$((SKIPPED + 1)); echo "    SKIP  $*"; }
  303  # The signal dispositions this run inherited (PL-025): vm-qa's wrapper resets
  304  # SIGINT and SIGPIPE before exec; SigIgn bit 1 is SIGINT, bit 12 SIGPIPE. Read
  305  # from /proc/$$ -- the first cut read /proc/self inside $( ), which is awk's own
  306  # process, and awk reads SIGPIPE ignored where this shell has it default.
  307  sigign="$(awk '/^SigIgn:/{print $2}' "/proc/$$/status")"   # $$ is this script, not the awk
  308  echo "signals: SigIgn=${sigign} SIGINT ignored=$(( (16#${sigign} >> 1) & 1 )) SIGPIPE ignored=$(( (16#${sigign} >> 12) & 1 ))"
  309  check() { # <0|nonzero> ok-text bad-text
  310      if [ "$1" -eq 0 ]; then echo "    PASS  $2"; else echo "    FAIL  $3"; FAIL=$((FAIL + 1)); fi
  311  }
  312  
  313  # One file under test: the working tree's copy, or the base commit's under
  314  # --old. A copy that cannot be read ends the run (exit 2) rather than
  315  # leaving an empty file for a case to grade -- against an empty script every
  316  # guard is absent, and the FAILs would read as the guards firing. Every case
  317  # that lifts or runs a script takes it from here, so --old means the same
  318  # thing in every case (#151 PL-10: cases l and m used to read the working
  319  # tree whatever the flag said, and their checks had never been seen to fail).
  320  src_of() { # <repo-relative path> <destination>
  321      if [ "${OLD}" -eq 1 ]; then
  322          git -C "${ROOT}" show "${BASE_REF}:${1}" > "${2}" || { echo "cannot read ${1} at ${BASE_REF}" >&2; exit 2; }
  323      else
  324          cp "${ROOT}/${1}" "${2}" || { echo "cannot read ${1}" >&2; exit 2; }
  325      fi
  326      # Ship the real reader and transaction module beside the script, as the
  327      # package does. Historical --old scripts without that dependency stay old.
  328      if grep -q 'cloud_connections as connections\|/cloud_remote" active' "${2}"; then
  329          local connection_dir
  330          connection_dir="$(dirname "$2")"
  331          if [[ "${1}" != */cloud_remote ]]; then
  332              src_of "${RCLONE_REL}/cloud_remote" "${connection_dir}/cloud_remote"
  333              chmod +x "${connection_dir}/cloud_remote"
  334          fi
  335          src_of "${RCLONE_REL}/cloud_connections.py" "${connection_dir}/cloud_connections.py"
  336      fi
  337      case "${1}" in
  338          */cloud_setup)
  339              # Discovery shares the restore scanner's local membership.
  340              src_of "${RCLONE_REL}/cloud_content_restore" "$(dirname "$2")/cloud_content_restore"
  341              chmod +x "$(dirname "$2")/cloud_content_restore"
  342              if grep -q -- '--validate-folders)' "$2"; then
  343                  src_of "${RCLONE_REL}/cloud_folder_validate" "$(dirname "$2")/cloud_folder_validate"
  344                  chmod +x "$(dirname "$2")/cloud_folder_validate"
  345              fi ;;
  346          */cloud_content_backup|*/cloud_content_restore)
  347              # Install the scanner that binds the production preflight context,
  348              # including its real sibling dependencies.
  349              if grep -q '/cloud_scan" --context' "$2"; then
  350                  src_of "${RCLONE_REL}/cloud_scan" "$(dirname "$2")/cloud_scan"
  351                  chmod +x "$(dirname "$2")/cloud_scan"
  352              fi
  353              local guard_rel="${RCLONE_REL}/cloud_content_transfer" guard_dst
  354              guard_dst="$(dirname "$2")/cloud_content_transfer"
  355              if [ "${OLD}" -eq 1 ]; then
  356                  git -C "${ROOT}" show "${BASE_REF}:${guard_rel}" > "${guard_dst}" 2>/dev/null || rm -f "${guard_dst}"
  357              else
  358                  cp "${ROOT}/${guard_rel}" "${guard_dst}" || exit 2
  359              fi ;;
  360          */cloud_scan|*/cloud_restore)
  361              local archive_rel="${RCLONE_REL}/rasteratops-settings-archive" archive_dst
  362              archive_dst="$(dirname "$2")/rasteratops-settings-archive"
  363              if [ "${OLD}" -eq 1 ]; then
  364                  git -C "${ROOT}" show "${BASE_REF}:${archive_rel}" > "${archive_dst}" 2>/dev/null || rm -f "${archive_dst}"
  365              else
  366                  cp "${ROOT}/${archive_rel}" "${archive_dst}" || exit 2
  367              fi ;;
  368      esac
  369  }
  370  
  371  # The scripts under test: the working tree, or the base commit's.
  372  mkdir -p "${TMP}/src"
  373  for rel in "${CHK_REL}" "${BT_REL}" "${FN_REL}"; do
  374      src_of "${rel}" "${TMP}/src/$(basename "${rel}")"
  375  done
  376  CHK="${TMP}/src/chksysconfig"; BT="${TMP}/src/backuptool"; FN="${TMP}/src/001-functions"
  377  chmod +x "${BT}"
  378  
  379  # busybox sed/mv/cp from the image when a build root is here, so the rename
  380  # semantics tested are the device's.
  381  image_tool_source() {
  382      local name="$1" b; shift
  383      if [ -n "${QA_SYSTEM_ROOT:-}" ]; then
  384          b="${QA_SYSTEM_ROOT}/usr/bin/${name}"
  385          if [ ! -x "${b}" ] || ! "${b}" "$@" >/dev/null 2>&1; then
  386              echo "cannot run candidate ${name} from QA_SYSTEM_ROOT: ${b}" >&2
  387              return 2
  388          fi
  389          printf '%s\n' "${b}"
  390          return 0
  391      fi
  392      for b in "${ROOT}"/../*/build.{ROCKNIX,RASTERATOPS,pixelelated}-*/image/system/usr/bin/"${name}" \
  393               "${ROOT}".worktrees/*/build.{ROCKNIX,RASTERATOPS,pixelelated}-*/image/system/usr/bin/"${name}" \
  394               "${ROOT}"/build.{ROCKNIX,RASTERATOPS,pixelelated}-*/image/system/usr/bin/"${name}"; do
  395          if [ -x "${b}" ] && "${b}" "$@" >/dev/null 2>&1; then
  396              printf '%s\n' "${b}"
  397              return 0
  398          fi
  399      done
  400      command -v "${name}" || true
  401  }
  402  BB_SRC=$(image_tool_source busybox sed --help) || exit 2
  403  # The copy, not the build root's file. Every image step deletes image/system
  404  # and re-installs every package (scripts/image), so a build running beside the
  405  # harness pulls the busybox every sandbox here bind-mounts out from under it:
  406  # on 2026-09-25 section t's eighteen checks after the cancel failed with rc 1
  407  # and empty output while a GENERIC_X64 image step ran, and the log was read as
  408  # a race in the scripts (#272) until the timestamps were put side by side. A
  409  # bind of a file another process rewrites is a fixture the harness does not
  410  # own; the copy is. BB_HOST is the copy on the host; BB is where every sandbox
  411  # sees it -- a path of its own, since the sandboxes mount a tmpfs over /tmp
  412  # and a copy under the run directory would vanish with it. The wrappers try
  413  # the sandbox path first and fall back to the host copy, so the same wrapper
  414  # serves the host-side checks (sections a and b) and the sandboxed ones.
  415  BB=""; BB_HOST=""
  416  if [ -n "${BB_SRC}" ]; then
  417      cp "${BB_SRC}" "${TMP}/busybox" || { echo "    FAIL  cannot copy ${BB_SRC} into the run (a build's image step?)"; exit 2; }
  418      BB_HOST="${TMP}/busybox"; BB="/lgst/busybox"
  419  fi
  420  mkdir -p "${TMP}/bbin"
  421  if [ -n "${BB}" ]; then
  422      for a in sed mv cp tr head wc cut awk stat chmod cat; do printf '#!/bin/sh\n[ -x %s ] && exec %s %s "$@"\nexec %s %s "$@"\n' "${BB}" "${BB}" "${a}" "${BB_HOST}" "${a}" > "${TMP}/bbin/${a}"; chmod +x "${TMP}/bbin/${a}"; done
  423  fi
  424  
  425  echo "last-good-scripts-test: $([ "${OLD}" -eq 1 ] && echo "scripts at ${BASE_REF} (expect FAILs)" || echo "scripts in ${ROOT}")"
  426  [ -n "${BB}" ] && echo "  sed/mv/cp/tr/head/wc/cut/awk: $("${BB_HOST}" 2>&1 | head -1) -- a copy of ${BB_SRC}"
  427  
  428  # ---------------------------------------------------------------- a.
  429  echo "  a. chksysconfig keeps and restores the last good system.cfg"
  430  A="${TMP}/a"; mkdir -p "${A}/cfg/system/configs" "${A}/cfg/retroarch" "${A}/def/system/configs" "${A}/def/retroarch"
```

## Excerpt: a (`:429-517` at 8ebaf8daad)

```text
  429  echo "  a. chksysconfig keeps and restores the last good system.cfg"
  430  A="${TMP}/a"; mkdir -p "${A}/cfg/system/configs" "${A}/cfg/retroarch" "${A}/def/system/configs" "${A}/def/retroarch"
  431  printf 'system.hostname=DEFAULT\n' > "${A}/def/system/configs/system.cfg"
  432  echo d > "${A}/def/retroarch/retroarch.cfg"; echo d > "${A}/def/retroarch/retroarch-core-options.cfg"
  433  echo user > "${A}/cfg/retroarch/retroarch.cfg"; echo user > "${A}/cfg/retroarch/retroarch-core-options.cfg"
  434  {
  435      # Every function the file defines, whatever it calls them.
  436      sed -n '/^function prepare_settings_temp() {/,/^}/p' "${FN}"
  437      awk '/^[a-z_]+\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}' "${CHK}"
  438      cat <<EOS
  439  logger() { echo "logger \$*" >&2; }
  440  CONFIG_ROOT="${A}/cfg"; DEFAULT_ROOT="${A}/def"
  441  CFG_PATH="\${CONFIG_ROOT}/system/configs"; CFG="\${CFG_PATH}/system.cfg"; BACKUP="\${CFG}.backup"
  442  EOS
  443  } > "${A}/fns.sh"
  444  # The old script names /storage and /usr/config outright, so its rsync must
  445  # be shimmed to do what it would do -- copy the default tree over the config
  446  # tree -- against the fixture; the new one takes the roots from variables.
  447  mkdir -p "${A}/bin"
  448  cat > "${A}/bin/rsync" <<EOS
  449  #!/bin/bash
  450  args=(); ign=0
  451  for x in "\$@"; do case "\$x" in --ignore-existing) ign=1 ;; -a) ;; /usr/config/) args+=("${A}/def/") ;; /storage/.config) args+=("${A}/cfg") ;; *) args+=("\$x") ;; esac; done
  452  opts=(-a); [ "\$ign" = 1 ] && opts+=(--ignore-existing)
  453  exec /usr/bin/rsync "\${opts[@]}" "\${args[@]}"
  454  EOS
  455  chmod +x "${A}/bin/rsync"
  456  CFGF="${A}/cfg/system/configs/system.cfg"
  457  
  458  printf 'a.b=1\nsystem.hostname=MINE\n' > "${CFGF}.backup"; : > "${CFGF}"
  459  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; verify" 2>"${A}/err"
  460  [ "$(grep '^system.hostname=' "${CFGF}" 2>/dev/null)" = "system.hostname=MINE" ]; check $? "empty system.cfg + valid .backup: verify restored the backup (hostname MINE)" "system.cfg after verify: '$(tr '\n' '|' < "${CFGF}" | cut -c1-80)' -- expected the backup's hostname MINE"
  461  [ "$(cat "${A}/cfg/retroarch/retroarch.cfg")" = "user" ]; check $? "and the player's retroarch.cfg was left alone" "retroarch.cfg was overwritten with the image default"
  462  grep -q 'logger -t chksysconfig .*restored' "${A}/err"; check $? "one syslog line names the recovery" "no recovery line in syslog; stderr: '$(tr '\n' '|' < "${A}/err" | cut -c1-200)'"
  463  
  464  printf 'a.b=1\nsystem.host' > "${CFGF}"
  465  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; verify" 2>/dev/null
  466  [ "$(grep '^system.hostname=' "${CFGF}" 2>/dev/null)" = "system.hostname=MINE" ]; check $? "truncated system.cfg (no hostname): verify restored the backup" "system.cfg after verify: '$(tr '\n' '|' < "${CFGF}" | cut -c1-80)'"
  467  
  468  printf 'a.b=1\n\0\0\0\nsystem.hostname=X\n' > "${CFGF}"
  469  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; verify" 2>/dev/null
  470  [ "$(grep -a '^system.hostname=' "${CFGF}" 2>/dev/null)" = "system.hostname=MINE" ]; check $? "binary system.cfg: verify restored the backup" "system.cfg after verify: '$(tr '\n' '|' < "${CFGF}" | cut -c1-80)'"
  471  
  472  : > "${CFGF}"; : > "${CFGF}.backup"
  473  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; verify" 2>/dev/null
  474  [ "$(grep '^system.hostname=' "${CFGF}" 2>/dev/null)" = "system.hostname=DEFAULT" ]; check $? "both empty: verify fell back to the image's system.cfg" "system.cfg after verify: '$(tr '\n' '|' < "${CFGF}" | cut -c1-80)'"
  475  
  476  printf 'system.hostname=GOOD\n' > "${CFGF}.backup"; : > "${CFGF}"
  477  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; backup" 2>/dev/null
  478  [ "$(cat "${CFGF}.backup")" = "system.hostname=GOOD" ]; check $? "backup with an empty current file left .backup unchanged" ".backup after backup: '$(tr '\n' '|' < "${CFGF}.backup" | cut -c1-80)' -- the empty file replaced the good copy"
  479  printf 'system.hostname=NEW\nx=1\n' > "${CFGF}"
  480  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; backup" 2>/dev/null
  481  [ "$(head -1 "${CFGF}.backup")" = "system.hostname=NEW" ] && [ ! -e "${CFGF}.backup.tmp" ]; check $? "backup with a valid current file replaced .backup, no temp left" ".backup: '$(head -1 "${CFGF}.backup")'; temp present: $([ -e "${CFGF}.backup.tmp" ] && echo yes || echo no)"
  482  
  483  # The fixtures above are three lines long. A device's system.cfg is the
  484  # image's, 220-odd lines, and that is the file the check has to accept --
  485  # under the device's tr (busybox reads "[:print:]" as eight characters).
  486  sed 's/@DEVICENAME@/QA/' "${ROOT}/projects/ROCKNIX/packages/rocknix/config/system/configs/system.cfg" > "${CFGF}"
  487  : > "${CFGF}.backup"
  488  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; backup" 2>/dev/null
  489  cmp -s "${CFGF}" "${CFGF}.backup"; check $? "the image's own system.cfg ($(wc -l < "${CFGF}") lines) is valid and became the record" "the image's system.cfg was refused as damaged; .backup: $(wc -c < "${CFGF}.backup") bytes"
  490  printf 'system.hostname=X\nwifi.ssid=caf\303\251 \342\230\205\n' > "${CFGF}"
  491  PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; backup" 2>/dev/null
  492  cmp -s "${CFGF}" "${CFGF}.backup"; check $? "a UTF-8 value (an accented Wi-Fi name) is text" "the UTF-8 system.cfg was refused as damaged"
  493  
  494  # A settings restore cut off mid-extract: backuptool left .restore-in-progress
  495  # naming the copy it took aside; verify puts the copy back over the tree
  496  # (EXTRACT_ROOT, / on a device), says so for EmulationStation, and clears the
  497  # marker (D-CLOUD-078, KILL18).
  498  mkdir -p "${A}/root/storage/.config/test" "${A}/snapsrc/storage/.config/test"
  499  echo HALF-RESTORED > "${A}/root/storage/.config/test/x.cfg"
  500  echo LIVE > "${A}/snapsrc/storage/.config/test/x.cfg"
  501  tar -czf "${A}/cfg/pre-restore.tar.gz" -C "${A}/snapsrc" storage
  502  printf '%s\n' "${A}/cfg/pre-restore.tar.gz" > "${A}/cfg/.restore-in-progress"
  503  printf 'system.hostname=X\n' > "${CFGF}"; cp "${CFGF}" "${CFGF}.backup"
  504  EXTRACT_ROOT="${A}/root" PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; verify" 2>"${A}/err"
  505  [ "$(cat "${A}/root/storage/.config/test/x.cfg")" = "LIVE" ] && [ ! -e "${A}/cfg/.restore-in-progress" ] && [ "$(cat "${A}/cfg/.restore-reverted" 2>/dev/null)" = "reverted" ]; check $? "a cut-off restore is undone at boot: the copy is back, the marker gone, 'reverted' left for the screen" "x.cfg='$(cat "${A}/root/storage/.config/test/x.cfg")'; marker: $([ -e "${A}/cfg/.restore-in-progress" ] && echo present || echo gone); said: '$(cat "${A}/cfg/.restore-reverted" 2>/dev/null)'"
  506  rm -f "${A}/cfg/.restore-reverted"
  507  # The copy's folder not mounted yet (sysinit runs before /storage/roms is
  508  # bound): the marker stays for the later verify, nothing is said.
  509  printf '%s\n' "${A}/not-mounted-yet/pre-restore.tar.gz" > "${A}/cfg/.restore-in-progress"
  510  EXTRACT_ROOT="${A}/root" PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; verify" 2>"${A}/err"
  511  [ -e "${A}/cfg/.restore-in-progress" ] && [ ! -e "${A}/cfg/.restore-reverted" ] && grep -q 'not mounted yet' "${A}/err"; check $? "a copy whose folder is not mounted yet is left for the later verify, marker kept, nothing said" "marker: $([ -e "${A}/cfg/.restore-in-progress" ] && echo present || echo gone); said: '$(cat "${A}/cfg/.restore-reverted" 2>/dev/null)'; log: $(grep -c 'not mounted yet' "${A}/err") line(s)"
  512  printf '%s\n' "${A}/cfg/missing.tar.gz" > "${A}/cfg/.restore-in-progress"
  513  EXTRACT_ROOT="${A}/root" PATH="${A}/bin:${TMP}/bbin:${PATH}" bash -c ". '${A}/fns.sh'; verify" 2>"${A}/err"
  514  [ ! -e "${A}/cfg/.restore-in-progress" ] && [ "$(cat "${A}/cfg/.restore-reverted" 2>/dev/null)" = "failed" ]; check $? "with the copy missing the marker is cleared and 'failed' is said instead" "marker: $([ -e "${A}/cfg/.restore-in-progress" ] && echo present || echo gone); said: '$(cat "${A}/cfg/.restore-reverted" 2>/dev/null)'"
  515  rm -f "${A}/cfg/.restore-reverted"
  516  
  517  # ---------------------------------------------------------------- b.
```

## Excerpt: b (`:518-606` at 8ebaf8daad)

```text
  518  echo "  b. backuptool: a kill mid-tar leaves the previous archive; a failed restore puts the snapshot back"
  519  B="${TMP}/b"; ST="${B}/storage"
  520  mkdir -p "${ST}/.config/system/configs" "${ST}/.config/test" "${ST}/roms/backup" "${B}/shim" "${B}/repo"
  521  cp "${BT}" "${B}/repo/backuptool"
  522  printf 'export PATH=/shim:/usr/bin:/bin\nexport OS_NAME=ROCKNIX\n' > "${B}/profile"
  523  printf '#!/bin/sh\necho "logger $*" >&2\n' > "${B}/shim/logger"
  524  printf '#!/bin/sh\necho "systemctl $*"\n' > "${B}/shim/systemctl"
  525  printf '#!/bin/sh\nexit 0\n' > "${B}/shim/sleep"
  526  chmod +x "${B}/shim"/*
  527  printf 'system.hostname=X\nwifi.key=SECRET\n' > "${ST}/.config/system/configs/system.cfg"
  528  printf 'LOCATIONS=(\n  /storage/.config/system/configs/system.cfg\n  /storage/.config/test/*\n)\n' > "${ST}/.config/backuptool.conf"
  529  for i in 1 2 3; do echo "file${i}" > "${ST}/.config/test/f${i}"; done
  530  # Run backuptool whole, inside bwrap: the repo copy at /repo, a stub profile,
  531  # the fake /storage, shims first on PATH. setsid gives each run its own
  532  # process group, which is what the dying tar kills.
  533  bt() { # <verb...>; stdout+stderr to $OUT, rc in $RC (137 when the group was killed)
  534      # In a subshell so the shell's own "Killed" notice for the dying group
  535      # does not land in the test's output.
  536      RC=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
  537          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
  538          --ro-bind /etc /etc --ro-bind "${B}/profile" /etc/profile \
  539          --bind "${ST}" /storage --ro-bind "${B}/shim" /shim --ro-bind "${B}/repo" /repo \
  540          --dev /dev --proc /proc --tmpfs /tmp \
  541          bash /repo/backuptool "$@" > "${OUT}" 2>&1; echo $? ) 2>/dev/null )
  542  }
  543  OUT="${B}/out"
  544  bt backup; rc1=${RC}
  545  first=$(ls "${ST}/roms/backup"/*.tar.gz 2>/dev/null)
  546  [ "${rc1}" -eq 0 ] && [ -n "${first}" ] && [ "$(echo "${first}" | wc -l)" -eq 1 ]; check $? "a first backup writes one archive at the root (rc 0)" "rc ${rc1}; root holds: $(ls "${ST}/roms/backup" 2>/dev/null | tr '\n' ' '); out: $(tail -3 "${OUT}" | tr '\n' '|')"
  547  tar -tzf "${first}" 2>/dev/null | grep -q 'storage/.config/test/f1$'; check $? "and it lists back whole" "archive does not list"
  548  ! tar -xzOf "${first}" storage/.config/system/configs/system.cfg 2>/dev/null | grep -q SECRET; check $? "with the wifi key stripped" "the archive carries the wifi key"
  549  sleep 1  # a new stamp, so the second archive has a distinct name
  550  bt backup; rc2=${RC}
  551  second=$(ls "${ST}/roms/backup"/*.tar.gz 2>/dev/null)
  552  [ "${rc2}" -eq 0 ] && [ "$(echo "${second}" | wc -l)" -eq 1 ] && [ "${second}" != "${first}" ] && [ -f "${ST}/roms/backup/archive/$(basename "${first}")" ]; check $? "a second backup rotates the first into archive/ and leaves one at the root" "rc ${rc2}; root: $(ls "${ST}/roms/backup" | tr '\n' ' '); archive: $(ls "${ST}/roms/backup/archive" 2>/dev/null | tr '\n' ' ')"
  553  
  554  # The kill: tar writing the archive emits 1 MiB and SIGKILLs its own
  555  # process group -- bwrap, the script, itself. Every other tar call is real.
  556  cat > "${B}/shim/tar" <<'EOS'
  557  #!/bin/bash
  558  out=""; prev=""
  559  for a in "$@"; do [ "${prev}" = "-czf" ] && out="${a}"; prev="${a}"; done
  560  if [ -n "${out}" ]; then
  561      head -c 1048576 /dev/zero > "${out}"
  562      kill -9 -- "-$(cut -d' ' -f5 /proc/self/stat)"
  563      sleep 5
  564      exit 1
  565  fi
  566  exec /usr/bin/tar "$@"
  567  EOS
  568  chmod +x "${B}/shim/tar"
  569  sleep 1
  570  bt backup; rck=${RC}
  571  roots=$(ls "${ST}/roms/backup"/*.tar.gz 2>/dev/null)
  572  partials=$(ls "${ST}/roms/backup"/*.partial 2>/dev/null)
  573  [ "${rck}" -ne 0 ]; check $? "the run died (rc ${rck})" "the run exited 0 through a tar that killed the group"
  574  [ "${roots}" = "${second}" ]; check $? "the previous archive is still the only *.tar.gz at the root" "root *.tar.gz: '$(echo "${roots}" | tr '\n' ' ')' -- expected only $(basename "${second}")"
  575  [ -n "${partials}" ] && [ "$(echo "${partials}" | wc -l)" -eq 1 ]; check $? "a .partial sits beside it ($(basename "${partials:-none}"))" "partials at the root: '$(echo "${partials}" | tr '\n' ' ')' -- the truncated archive was written under the final name"
  576  [ "$(ls "${ST}/roms/backup/archive"/*.tar.gz 2>/dev/null | wc -l)" -eq 1 ]; check $? "archive/ is unchanged (still one archive)" "archive/ holds $(ls "${ST}/roms/backup/archive" 2>/dev/null | wc -l) file(s): rotation ran before the new archive existed"
  577  rm -f "${B}/shim/tar"
  578  
  579  # A restore whose extraction fails: the shim extracts for real, then damages
  580  # one restored file and exits 1 -- what a cut mid-extract leaves. The
  581  # snapshot's own extraction (from archive/) is real.
  582  echo changed > "${ST}/.config/test/f1"
  583  cat > "${B}/shim/tar" <<'EOS'
  584  #!/bin/bash
  585  if [ "$1" = "-xzf" ] && [[ "$2" != */archive/* ]] && [ "$3" = "-C" ] && [ "$4" = "/" ]; then
  586      /usr/bin/tar "$@"
  587      echo garbage > /storage/.config/test/f2
  588      exit 1
  589  fi
  590  exec /usr/bin/tar "$@"
  591  EOS
  592  chmod +x "${B}/shim/tar"
  593  bt restore; rcr=${RC}
  594  [ "${rcr}" -ne 0 ]; check $? "a restore whose extraction fails exits non-zero" "rc 0 from a failed extraction"
  595  [ "$(cat "${ST}/.config/test/f1")" = "changed" ] && [ "$(cat "${ST}/.config/test/f2")" = "file2" ]; check $? "and the pre-restore state was put back (f1 'changed', f2 'file2')" "f1='$(cat "${ST}/.config/test/f1")' f2='$(cat "${ST}/.config/test/f2")' -- the tree is half the archive, half the old state"
  596  ls "${ST}/roms/backup/archive"/*PRE_RESTORE* >/dev/null 2>&1; check $? "the snapshot is in archive/ as *PRE_RESTORE*" "no PRE_RESTORE snapshot in archive/: $(ls "${ST}/roms/backup/archive" 2>/dev/null | tr '\n' ' ')"
  597  grep -q 'YOUR SETTINGS ARE UNCHANGED' "${OUT}"; check $? "and the screen says the settings are unchanged" "screen: $(grep -v '^logger' "${OUT}" | tail -2 | tr '\n' '|')"
  598  
  599  ! grep -vE '^logger |^>>> ' "${OUT}" | grep -qiE "logger|/storage/|/var/log|exit [0-9]"; check $? "with no path, log or tool name on it" "a screen line carries one: $(grep -vE '^logger |^>>> ' "${OUT}" | grep -iE 'logger|/storage/|/var/log|exit [0-9]' | head -1)"
  600  rm -f "${B}/shim/tar"
  601  # A restore that works, asked to leave the journey marker.
  602  echo changed > "${ST}/.config/test/f1"
  603  bt restore --then-cloud; rcg=${RC}
  604  [ "${rcg}" -eq 0 ] && [ "$(cat "${ST}/.config/test/f1")" = "file1" ] && [ -e "${ST}/.config/.cloud-journey-pending" ]; check $? "a good restore --then-cloud restores f1 and leaves .cloud-journey-pending" "rc ${rcg}; f1='$(cat "${ST}/.config/test/f1")'; marker: $([ -e "${ST}/.config/.cloud-journey-pending" ] && echo yes || echo no)"
  605  
  606  # ---------------------------------------------------------------- c.
```

## Excerpt: q (`:1752-1859` at 8ebaf8daad)

```text
 1752  echo "  q. 099-networkservices: a daemon fragment that sets no CONF inherits none from the fragment before it (#166)"
 1753  # The boot pass sources every /usr/lib/autostart/daemons/* in turn and, for
 1754  # each, removes the marker CONF names before rewriting it from STATE and
 1755  # backgrounding a systemctl start or stop. It never reset the variables
 1756  # between fragments, so a fragment that sets no CONF (004-*, 005-fstrim,
 1757  # 007-syncthing) inherited the previous one's and removed the marker it had
 1758  # just written: 007-syncthing took raofflineproxy.conf from
 1759  # 006-raofflineproxy, and the unit's ConditionPathExists read false by the
 1760  # time the backgrounded start was processed, so the toggle died on the
 1761  # second boot while the row still read on (#166 s. 6). The same leak has
 1762  # removed samba's smb.conf through 004-tailscaled at every boot since the
 1763  # fragments were written, which is why the smb.conf check below fails at
 1764  # every BASE_REF and the raofflineproxy.conf one from #165 on.
 1765  #
 1766  # The pass runs WHOLE and unmodified under bwrap over the real fragments,
 1767  # every one the tree ships, at their real path: /usr/lib is the host's bound
 1768  # entry by entry so the fixture's daemons/ can sit under it, /etc is a tmpfs
 1769  # holding the loader's cache and a stub 001-functions (get_setting lifted
 1770  # from the file under test, on the fixture's system.cfg; tocon and log to
 1771  # stderr), /storage the fixture's, and systemctl a shim that reads the
 1772  # raofflineproxy unit's condition the way systemd does -- when the start is
 1773  # processed, a moment after the loop has moved on -- and logs what it found.
 1774  # Both starts and stops are backgrounded by the pass, so the wrapper waits
 1775  # for them before the log is read.
 1776  NS_REL=projects/ROCKNIX/packages/rocknix/autostart/099-networkservices
 1777  Q="${TMP}/q"; QS="${Q}/storage"; mkdir -p "${QS}/.config/system/configs" "${QS}/.cache/services" "${Q}/repo" "${Q}/shim" "${Q}/run" "${Q}/daemons" "${Q}/etc"
 1778  src_of "${NS_REL}" "${Q}/repo/099-networkservices"
 1779  bash -n "${Q}/repo/099-networkservices"; check $? "099-networkservices parses (bash -n)" "099-networkservices does not parse"
 1780  QHAVE_RA=0
 1781  while IFS= read -r frag; do
 1782      rel="${frag#* }"
 1783      if [ "${OLD}" -eq 1 ] && ! git -C "${ROOT}" cat-file -e "${BASE_REF}:${rel}" 2>/dev/null; then
 1784          echo "    note  ${rel##*/} is absent at ${BASE_REF}; left out of the pass"
 1785          continue
 1786      fi
 1787      src_of "${rel}" "${Q}/daemons/${rel##*/}"
 1788      [ "${rel##*/}" = "006-raofflineproxy" ] && QHAVE_RA=1
 1789  done < <(cd "${ROOT}" && find projects -path '*/daemons/[0-9]*' -type f -printf '%f %p\n' | sort)
 1790  QFRAGS="$(ls "${Q}/daemons" | tr '\n' ' ')"
 1791  echo "    fragments: ${QFRAGS}"
 1792  {
 1793      sed -n '/^function get_setting() {/,/^}/p' "${FN}"
 1794      cat <<'EOS'
 1795  tocon() { echo "tocon $*" >&2; }
 1796  log() { echo "log $*" >&2; }
 1797  J_CONF=/storage/.config/system/configs/system.cfg
 1798  EOS
 1799  } > "${Q}/etc/001-functions"
 1800  cat > "${Q}/shim/systemctl" <<'EOS'
 1801  #!/bin/sh
 1802  # systemd reads ConditionPathExists when it processes the start, not when
 1803  # systemctl is invoked, and the boot pass backgrounds every call and moves
 1804  # on to the next fragment; a short wait puts this shim on the same side of
 1805  # that race as the real unit.
 1806  sleep 1
 1807  case "$1" in
 1808      start)
 1809          case "$2" in
 1810              raofflineproxy|raofflineproxy.service)
 1811                  if [ -e /storage/.cache/services/raofflineproxy.conf ]; then echo "start $2 started" >> /run/systemctl.log; else echo "start $2 condition-unmet" >> /run/systemctl.log; fi ;;
 1812              *) echo "start $2 started" >> /run/systemctl.log ;;
 1813          esac ;;
 1814      stop) echo "stop $2" >> /run/systemctl.log ;;
 1815      *) echo "$*" >> /run/systemctl.log ;;
 1816  esac
 1817  exit 0
 1818  EOS
 1819  printf '#!/bin/sh\necho "logger $*" >&2\n' > "${Q}/shim/logger"
 1820  chmod +x "${Q}/shim"/*
 1821  QUSR=(--tmpfs /usr); for u in bin sbin lib64 libexec share; do [ -e "/usr/${u}" ] && QUSR+=(--ro-bind "/usr/${u}" "/usr/${u}"); done
 1822  for e in /usr/lib/* /usr/lib/.[!.]*; do [ -e "${e}" ] && QUSR+=(--ro-bind "${e}" "${e}"); done
 1823  QETC=(--tmpfs /etc); for e in /etc/ld.so.cache /etc/alternatives /etc/passwd /etc/group; do [ -e "${e}" ] && QETC+=(--ro-bind "${e}" "${e}"); done
 1824  QBB=(); QPATH="/shim:/usr/bin:/bin"
 1825  if [ -n "${BB}" ]; then QBB=(--ro-bind "${TMP}/bbin" /bbin --ro-bind "${BB_HOST}" "${BB}"); QPATH="/shim:/bbin:/usr/bin:/bin"; fi
 1826  QOUT="${Q}/out"; QCFG="${QS}/.config/system/configs/system.cfg"; QSVC="${QS}/.cache/services"; QLOG="${Q}/run/systemctl.log"
 1827  qpass() { # run the boot pass once; rc in $RC, output in $QOUT, systemctl's log in $QLOG
 1828      : > "${QLOG}"
 1829      RC=$( ( bwrap --die-with-parent --tmpfs / "${QUSR[@]}" "${QBB[@]}" \
 1830          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 1831          "${QETC[@]}" --ro-bind "${Q}/etc/001-functions" /etc/profile.d/001-functions \
 1832          --ro-bind "${Q}/daemons" /usr/lib/autostart/daemons \
 1833          --bind "${QS}" /storage --ro-bind "${Q}/repo" /repo --ro-bind "${Q}/shim" /shim --bind "${Q}/run" /run \
 1834          --dev /dev --proc /proc --tmpfs /tmp --setenv PATH "${QPATH}" \
 1835          bash -c 'source /repo/099-networkservices; wait' > "${QOUT}" 2>&1; echo $? ) 2>/dev/null )
 1836  }
 1837  # Boot 2 of #166 s. 6: the toggle on in system.cfg, its marker already there
 1838  # from the toggle's own enable, samba on beside it, everything else off.
 1839  printf 'system.hostname=X\nglobal.retroachievements.offlineproxy=1\nsamba.enabled=1\nssh.enabled=0\nsyncthing.enabled=0\n' > "${QCFG}"
 1840  rm -f "${QSVC}"/*; touch "${QSVC}/raofflineproxy.conf" "${QSVC}/smb.conf"
 1841  qpass
 1842  [ "${RC}" -eq 0 ]; check $? "the boot pass ran over ${QFRAGS% } (rc ${RC})" "rc ${RC}; output: $(tr '\n' '|' < "${QOUT}" | cut -c1-240)"
 1843  [ -e "${QSVC}/smb.conf" ]; check $? "samba on: smb.conf is still there after the pass" "smb.conf is gone after the pass: a fragment without CONF (004-tailscaled) inherited samba's and removed it; markers left: $(ls "${QSVC}" | tr '\n' ' ')"
 1844  if [ "${QHAVE_RA}" -eq 1 ]; then
 1845      [ -e "${QSVC}/raofflineproxy.conf" ]; check $? "toggle on: raofflineproxy.conf is still there after the pass" "raofflineproxy.conf is gone after the pass: 007-syncthing inherited CONF from 006-raofflineproxy and removed it; markers left: $(ls "${QSVC}" | tr '\n' ' ')"
 1846      grep -qx 'start raofflineproxy started' "${QLOG}"; check $? "and the unit's condition held when its start was processed" "systemctl saw: $(grep raofflineproxy "${QLOG}" | tr '\n' '|')"
 1847      ! grep -q 'condition-unmet' "${QLOG}"; check $? "no start found its marker missing" "systemctl saw: $(tr '\n' '|' < "${QLOG}")"
 1848      [ ! -e "${QSVC}/sshd.conf" ] && grep -qx 'stop sshd' "${QLOG}"; check $? "ssh off: no sshd.conf, sshd stopped (the pass still does its job)" "sshd.conf: $([ -e "${QSVC}/sshd.conf" ] && echo present || echo absent); systemctl saw: $(tr '\n' '|' < "${QLOG}")"
 1849      # Step 7 of the upgrade shape: the toggle off (or never set) and a marker
 1850      # left behind -- the pass removes it and stops the service.
 1851      printf 'system.hostname=X\nglobal.retroachievements.offlineproxy=0\nsamba.enabled=1\n' > "${QCFG}"
 1852      rm -f "${QSVC}"/*; touch "${QSVC}/raofflineproxy.conf" "${QSVC}/smb.conf"
 1853      qpass
 1854      [ "${RC}" -eq 0 ] && [ ! -e "${QSVC}/raofflineproxy.conf" ] && grep -qx 'stop raofflineproxy' "${QLOG}"; check $? "toggle off with a marker left behind: the marker is removed and the service stopped (rc ${RC})" "rc ${RC}; marker: $([ -e "${QSVC}/raofflineproxy.conf" ] && echo present || echo gone); systemctl saw: $(tr '\n' '|' < "${QLOG}")"
 1855      [ -e "${QSVC}/smb.conf" ]; check $? "and samba's marker is still there" "smb.conf gone; markers left: $(ls "${QSVC}" | tr '\n' ' ')"
 1856  else
 1857      check 1 "" "006-raofflineproxy is absent at ${BASE_REF}: the toggle had no boot pass"
 1858  fi
 1859  
```

## Excerpt: t: the client, its patches and the compile message (`:2033-2100` at 8ebaf8daad)

```text
 2033  echo "  t. raofflineproxy-ctl scan, topup and ready against the client the tree describes: the refusals, the index rule by account and hash, the probe's own folder and patience, one deadline, the failure verdict, the cap over uncached files, a stop on disable, and the patched client's own predicates (#186 PL-01..05, 12, 17, 23, 24, 25, 28, 30, 33; #190; #194; #199)"
 2034  # The client is built as the package builds it: the pinned tarball from the
 2035  # sources cache (PKG_VERSION in package.mk), the package's patches applied
 2036  # in order (from BASE_REF under --old, so the client is the one that tree
 2037  # describes). Its own network verbs -- probe-online, run-smart-cache,
 2038  # cached-games-count -- and the helper the ctl runs are shims that answer
 2039  # from files under /run; everything else the ctl imports (the storage, the
 2040  # export, the browser's rules, the history reader) is the real, patched
 2041  # code, and the fixture store is written through the real Storage. Time is
 2042  # virtual: date +%s reads /run/clock, sleep advances it (real when
 2043  # /run/fast-sleep is absent), timeout runs its command with the budget in
 2044  # FAKE_BUDGET and returns 124 when the command says it ran past it -- so a
 2045  # fifteen-minute deadline is tested in milliseconds, and a real wait is
 2046  # taken only where a real process must be stopped (PL-30).
 2047  T="${TMP}/t"; TS="${T}/storage"; TR="${T}/run"; mkdir -p "${TS}/.config/system/configs" "${TS}/.config/raofflineproxy" "${TS}/.config/emulationstation/recovery/nes" "${TS}/roms/nes" "${TS}/roms/gb/images" "${T}/repo" "${T}/shim" "${TR}" "${T}/varrun" "${T}/pypath"
 2048  PKG_REL=projects/ROCKNIX/packages/network/raofflineproxy/package.mk
 2049  PATCHES_REL=projects/ROCKNIX/packages/network/raofflineproxy/patches
 2050  HELPER_REL=projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed
 2051  PIN="$(sed -n 's/^PKG_VERSION="\([0-9a-f]*\)"$/\1/p' "${ROOT}/${PKG_REL}" 2>/dev/null | head -1)"
 2052  TARBALL=""
 2053  for d in "${SOURCES_DIR:-}" /workspace/cache/rocknix-sources "${ROOT}/sources" "${ROOT}"/../*/sources; do
 2054      [ -n "${d}" ] && [ -f "${d}/raofflineproxy/raofflineproxy-${PIN}.tar.gz" ] && { TARBALL="${d}/raofflineproxy/raofflineproxy-${PIN}.tar.gz"; break; }
 2055  done
 2056  if [ "${OLD}" -eq 1 ] && ! git -C "${ROOT}" cat-file -e "${BASE_REF}:${CTL_REL}" 2>/dev/null; then
 2057      check 1 "" "raofflineproxy-ctl is absent at ${BASE_REF}: no scan to test"
 2058  elif [ -z "${TARBALL}" ]; then
 2059      skip "the client's tarball raofflineproxy-${PIN:-?}.tar.gz is not under SOURCES_DIR, /workspace/cache/rocknix-sources or a build worktree's sources/ -- case t needs the pinned client to drive the ctl's listing against"
 2060  else
 2061  src_of "${CTL_REL}" "${T}/repo/raofflineproxy-ctl"
 2062  # The archive's top directory is the project's name and the pin (a GitHub
 2063  # archive: RAOfflineProxy-<hash>); only the module is taken out of it.
 2064  # The module and its tests: a patch may carry a test for what it changes
 2065  # (015 does), and a patch with a hunk for a file that was not unpacked does
 2066  # not apply at all -- which read as "the tree describes a client the build
 2067  # does not" on 2026-09-22 while the build had applied it (fork #242).
 2068  tar -xzf "${TARBALL}" -C "${T}" --wildcards '*/linux/raofflineproxy/*' '*/linux/tests/*' 2>/dev/null
 2069  mkdir -p "${T}/patched"
 2070  mv "${T}"/*-"${PIN}"/linux "${T}/patched/linux" 2>/dev/null; rm -rf "${T}"/*-"${PIN}"
 2071  rm -rf "${T}/patched/linux/raofflineproxy/__pycache__"
 2072  [ -f "${T}/patched/linux/raofflineproxy/storage.py" ]; check $? "the pinned client unpacked from $(basename "${TARBALL}")" "no linux/raofflineproxy/storage.py came out of ${TARBALL}: $(ls "${T}" | tr '\n' ' ')"
 2073  # The patches, in order, as scripts/unpack applies them (patch -p1).
 2074  TPATCH_OK=1; TPATCHES=""
 2075  if [ "${OLD}" -eq 1 ]; then
 2076      TPATCHES="$(git -C "${ROOT}" ls-tree --name-only "${BASE_REF}" -- "${PATCHES_REL}/" 2>/dev/null | grep '\.patch$' | sort)"
 2077  else
 2078      TPATCHES="$(cd "${ROOT}" && ls "${PATCHES_REL}"/*.patch 2>/dev/null | sort)"
 2079  fi
 2080  for prel in ${TPATCHES}; do
 2081      src_of "${prel}" "${T}/one.patch"
 2082      if ! TMPDIR="${T}" patch -d "${T}/patched" -p1 -N -s < "${T}/one.patch" >"${T}/patch.out" 2>&1; then
 2083          TPATCH_OK=0; check 1 "" "${prel##*/} does not apply to the pinned client: $(tr '\n' '|' < "${T}/patch.out" | cut -c1-200)"
 2084      fi
 2085  done
 2086  [ "${TPATCH_OK}" -eq 1 ]; check $? "the client at ${PIN:0:10} with $(echo "${TPATCHES}" | grep -c .) patch(es) applied in order, each compiled: $(cd "${T}/patched/linux/raofflineproxy" && python3 -m py_compile *.py 2>&1 | head -1 || true)ok" "a patch did not apply; the runs below are against a client the tree does not describe"
 2087  CLIENT="${T}/patched/linux"
 2088  # The upstream subset-award regression runs against exactly the patched
 2089  # source above, including the HTTP queue/flush cases (#384).
 2090  PYTHONPATH="${T}/patched:${CLIENT}" python3 -m unittest discover -s "${CLIENT}/tests" -p test_linux_award_parity.py > "${T}/award-parity.log" 2>&1
 2091  check $? "the pinned proxy's award-parity suite, including subset game ids" "award-parity suite: $(tail -8 "${T}/award-parity.log" | tr '\n' '|')"
 2092  {
 2093      sed -n '/^function get_setting() {/,/^}/p; /^function wait_lock_say() {/,/^}/p; /^function wait_lock() {/,/^}/p; /^function settings_base() {/,/^}/p; /^function prepare_settings_temp() {/,/^}/p; /^function write_setting_line() {/,/^}/p; /^function del_setting() {/,/^}/p; /^function set_setting() {/,/^}/p' "${FN}"
 2094  } > "${T}/repo/fns.sh"
 2095  TBB=(); TPATH="/shim:/usr/bin:/bin"
 2096  if [ -n "${BB}" ]; then
 2097      mkdir -p "${T}/bbin"; for a in sed mv cp tr head wc cut awk tail flock mkfifo mktemp stat; do printf '#!/bin/sh\n[ -x %s ] && exec %s %s "$@"\nexec %s %s "$@"\n' "${BB}" "${BB}" "${a}" "${BB_HOST}" "${a}" > "${T}/bbin/${a}"; chmod +x "${T}/bbin/${a}"; done
 2098      TBB=(--ro-bind "${T}/bbin" /bbin --ro-bind "${BB_HOST}" "${BB}"); TPATH="/shim:/bbin:/usr/bin:/bin"
 2099  fi
 2100  printf 'export PATH=%s\nexport OS_NAME=ROCKNIX\nJ_CONF=/storage/.config/system/configs/system.cfg\nJ_CONF_LOCK=/tmp/.system.cfg.lock\n. /repo/fns.sh\n' "${TPATH}" > "${T}/profile"
```

## Excerpt: t: the verdict reading (`:2840-2856` at 8ebaf8daad)

```text
 2840      verdict(r.status == 200 and body == b"\x89PNG fixture 903" and srv.asked == [], "012 / #199 store-only header in another client's capitalisation (X-Ra-Store-Only, urllib's): still the store's copy, no probe, no fetch (G-02; until #258 only the exact and the all-lower spellings counted)", f"status {r.status}, asked {srv.asked}")
 2841      st.close()
 2842  except Exception as exc:
 2843      verdict(False, "012 / #199 image miss: store-only or offline is 404 at once with no probe and no fetch; a hit is served; an online miss still fetches", repr(exc))
 2844  finally:
 2845      network.reset_retroachievements_reachability_for_tests()
 2846  EOS
 2847  grep -q 'PL-' "${T}/predicates.out"; check $? "the patched client's predicates ran ($(grep -c '^PASS' "${T}/predicates.out") PASS / $(grep -c '^FAIL' "${T}/predicates.out") FAIL lines)" "the predicate run printed no verdicts: $(tr '\n' '|' < "${T}/predicates.out" | cut -c1-300)"
 2848  while IFS= read -r line; do
 2849      case "${line}" in
 2850          PASS\ *) check 0 "${line#PASS }" "" ;;
 2851          FAIL\ *) check 1 "" "${line#FAIL }" ;;
 2852      esac
 2853  done < "${T}/predicates.out"
 2854  fi
 2855  
 2856  echo "  u. wifictl current, saved, forget and join read NetworkManager, not the setting; forget says when it dropped the connection; join activates the saved profile and moves the settings onto it (#191)"
```

## Excerpt: v (`:2991-3066` at 8ebaf8daad)

```text
 2991  echo "  v. the save state manager's arguments reach RetroArch as Batocera's launcher carries them (#196, D-UI-057): runemu reads -state_slot, -autosave and -state_file each on its own and takes the path whole; setsettings turns a .auto file into savestate_auto_load and any other into -e <slot>; without -state_file, today's lines byte for byte"
 2992  # parse_savestate_arguments lifted from runemu.sh and called with the argument
 2993  # list the interface's command line becomes after sh -c (the quotes gone, the
 2994  # state file one argument, the controllers value one argument); setsettings'
 2995  # argument parsers (the block from #Autosave to the --state_file= loop's done)
 2996  # and set_autosave with log, game_setting, clear_setting and add_setting lifted
 2997  # the same way, get_setting shimmed to the AUTO SAVE/LOAD value under test, the
 2998  # appendconfig in a temp file, redact_credentials from 001-functions. The -e
 2999  # fragment is what set_autosave prints; runemu splices every setsettings
 3000  # fragment before --config (--host, --set-shader), and that splice line is
 3001  # checked to still be there before the same line is applied here. At a
 3002  # BASE_REF before #196 the function and the parser are absent: one FAIL each,
 3003  # not a silent skip.
 3004  U="${TMP}/u"; mkdir -p "${U}/repo" "${U}/log" "${U}/savestates"
 3005  src_of "${SS_REL}" "${U}/repo/setsettings.sh"; src_of "${RE_REL}" "${U}/repo/runemu.sh"
 3006  TENNIS="Mario Tennis - Power Tour (USA, Australia) (En,Fr,De,Es,It)"
 3007  UROM="/storage/roms/gba/${TENNIS}.zip"; USTATES="/storage/roms/savestates/gba"
 3008  UPADS="-p1index 0 -p1guid 030000005e0400008e02000014010000 -p2index 1 -p2guid 03000000790000000600000010010000"
 3009  sed -n '/^function parse_savestate_arguments() {/,/^}/p' "${U}/repo/runemu.sh" > "${U}/parse.sh"
 3010  if [ -s "${U}/parse.sh" ]; then
 3011      grep -qE '^\s*parse_savestate_arguments "\$@"' "${U}/repo/runemu.sh"; check $? "runemu.sh calls parse_savestate_arguments with its own \"\$@\"" "the call is missing or does not pass \"\$@\": $(grep -n 'parse_savestate_arguments' "${U}/repo/runemu.sh" | tr '\n' '|' | cut -c1-200)"
 3012      # pa <manager args...>: the lifted function over an interface command line; C= S= A= F= on four lines
 3013      pa() { bash -c '. "$0"; ARGUMENTS="$@"; parse_savestate_arguments "$@"; printf "%s\n" "C=${CONTROLLERCONFIG}" "S=${SNAPSHOT}" "A=${AUTOSAVE}" "F=${STATEFILE}"' "${U}/parse.sh" "${UROM}" -Pgba --core=mgba --emulator=retroarch --controllers="${UPADS}" "$@" 2>"${U}/pa.err"; }
 3014      # want <S> <A> <F> <manager args...>: the four variables as expected, controllers intact, no error
 3015      want() { local exp got; exp="$(printf 'C=%s\nS=%s\nA=%s\nF=%s' "${UPADS}" "$1" "$2" "$3")"; shift 3; got="$(pa "$@")"; [ "${got}" = "${exp}" ] && [ ! -s "${U}/pa.err" ]; }
 3016      said() { pa "$@" | tr '\n' '|'; [ -s "${U}/pa.err" ] && printf ' err: %s' "$(tr '\n' '|' < "${U}/pa.err")"; }
 3017      want 3 "" "${USTATES}/${TENNIS}.state3" -state_slot 3 -state_file "${USTATES}/${TENNIS}.state3"; check $? "a numbered slot (-state_slot 3 -state_file <slot file>): SNAPSHOT 3, no AUTOSAVE, the path whole -- spaces, parentheses and \" - \" -- the controllers intact" "got: $(said -state_slot 3 -state_file "${USTATES}/${TENNIS}.state3")"
 3018      want "" 1 "${USTATES}/${TENNIS}.state.auto" -autosave 1 -state_file "${USTATES}/${TENNIS}.state.auto"; check $? "the AUTO SAVE tile, and a plain launch with AUTO SAVE/LOAD on (-autosave 1 -state_file <auto>, no -state_slot): AUTOSAVE 1, the .auto path whole, no SNAPSHOT" "got: $(said -autosave 1 -state_file "${USTATES}/${TENNIS}.state.auto")"
 3019      want "" 0 "" -autosave 0; check $? "START NEW GAME (-autosave 0 alone): AUTOSAVE 0 and the controllers cut before it -- the shape the old parser dropped into CONTROLLERCONFIG" "got: $(said -autosave 0)"
 3020      want -1 1 "" -autosave 1 -state_slot -1; check $? "START NEW AUTO SAVE (-autosave 1 -state_slot -1): SNAPSHOT -1, RetroArch's auto slot" "got: $(said -autosave 1 -state_slot -1)"
 3021      want 2 1 "" -autosave 1 -state_slot 2 && want 2 "" "" -state_slot 2 && want 2 0 "" -autosave 0 -state_slot 2 && want "" "" "" && want "" "" "" --host --port 55435 --nick qa; check $? "without -state_file, the shapes the built-in fallback sends (-autosave 1 -state_slot 2; -state_slot 2; -autosave 0 -state_slot 2; none; a netplay tail) read exactly as today" "got: $(said -autosave 1 -state_slot 2) / $(said -state_slot 2) / $(said -autosave 0 -state_slot 2) / $(said) / $(said --host --port 55435 --nick qa)"
 3022      grep -qF -- '--state_file="${STATEFILE}" --controllers="${CONTROLLERCONFIG}" --autosave="${AUTOSAVE}" --snapshot="${SNAPSHOT}"' "${U}/repo/runemu.sh"; check $? "runemu hands setsettings --state_file= ahead of --controllers=, so the path never lands in CONTROLLERS (a ROM name can hold p1)" "the setsettings call: $(grep -n 'setsettings.sh "' "${U}/repo/runemu.sh" | tr '\n' '|' | cut -c1-240)"
 3023  else
 3024      check 1 "" "runemu.sh has no parse_savestate_arguments: -autosave and -state_file are read only beside -state_slot (#196)"
 3025  fi
 3026  if grep -q '^#State file' "${U}/repo/setsettings.sh"; then
 3027      sed -n '/^#Autosave$/,/^done$/p' "${U}/repo/setsettings.sh" > "${U}/args.sh"
 3028      # sp <setsettings options...>: the four parsers over runemu's call; A= S= C= F= on four lines
 3029      sp() { bash -c '. "$0"; printf "%s\n" "A=${AUTOSAVE}" "S=${SNAPSHOT}" "C=${CONTROLLERS}" "F=${STATEFILE}"' "${U}/args.sh" gba "${UROM}" mgba "$@" 2>"${U}/sp.err"; }
 3030      got="$(sp --state_file="${USTATES}/${TENNIS}.state3" --controllers="${UPADS}" --autosave=1 --snapshot=3)"
 3031      [ "${got}" = "$(printf 'A=1\nS=3\nC=%s --autosave=1 --snapshot=3\nF=%s' "${UPADS}" "${USTATES}/${TENNIS}.state3")" ] && [ ! -s "${U}/sp.err" ]; check $? "setsettings reads --state_file= whole and, placed ahead of --controllers=, leaves AUTOSAVE, SNAPSHOT and CONTROLLERS exactly as today" "got: $(echo "${got}" | tr '\n' '|'); err: $(tr '\n' '|' < "${U}/sp.err")"
 3032      got="$(sp --state_file= --controllers="${UPADS}" --autosave= --snapshot=)"
 3033      [ "${got}" = "$(printf 'A=\nS=\nC=%s --autosave= --snapshot=\nF=' "${UPADS}")" ]; check $? "an empty --state_file= (no manager, or a tile without a file) reads as no state file, the other three as today" "got: $(echo "${got}" | tr '\n' '|')"
 3034      sed -n '/^function redact_credentials() {/,/^}/p' "${FN}" > "${U}/ss.sh"
 3035      sed -n '/^function log() {/,/^}/p; /^function game_setting() {/,/^}/p; /^function clear_setting() {/,/^}/p; /^function add_setting() {/,/^}/p; /^function set_autosave() {/,/^}/p' "${U}/repo/setsettings.sh" >> "${U}/ss.sh"
 3036      # sa <AUTO SAVE/LOAD setting> <AUTOSAVE> <SNAPSHOT> <STATEFILE>: set_autosave; the appendconfig in $U/append.cfg, its stdout in $U/sa.out
 3037      sa() {
 3038          : > "${U}/append.cfg"; rm -f "${U}/append.cfg.sed"; : > "${U}/log/exec.log"
 3039          SETTING_AUTOSAVE="$1" AUTOSAVE="$2" SNAPSHOT="$3" STATEFILE="$4" PLATFORM=gba ROM="${TENNIS}.zip" SNAPSHOTS="${U}/savestates" TMP_CONFIG="${U}/append.cfg" LOGGING=verbose LOG_DIR="${U}/log" LOG_FILE=exec.log \
 3040          PATH="${TMP}/bbin:${PATH}" bash -c '. "$0"; get_setting() { echo "${SETTING_AUTOSAVE}"; }; set_autosave' "${U}/ss.sh" > "${U}/sa.out" 2>"${U}/sa.err"
 3041      }
 3042      # is <expected appendconfig lines, |-joined> <expected stdout>
 3043      is() { [ "$(tr '\n' '|' < "${U}/append.cfg")" = "$1" ] && [ "$(cat "${U}/sa.out")" = "$2" ] && [ ! -s "${U}/sa.err" ]; }
 3044      got() { printf 'cfg: %s stdout: [%s] err: %s' "$(tr '\n' '|' < "${U}/append.cfg")" "$(cat "${U}/sa.out")" "$(tr '\n' '|' < "${U}/sa.err")"; }
 3045      DIR="savestate_directory = \"${U}/savestates/gba\"|"
 3046      sa 1 "" 3 "${USTATES}/${TENNIS}.state3"; is "${DIR}state_slot = \"3\"|savestate_auto_load = \"true\"|savestate_auto_save = \"true\"|" " -e 3"; check $? "a numbered slot with AUTO SAVE/LOAD on: state_slot 3, auto-load and the exit auto save on, and \" -e 3\" on stdout" "$(got)"
 3047      [ -d "${U}/savestates/gba" ]; check $? "and the savestates directory is made" "no ${U}/savestates/gba"
 3048      sa 0 "" 3 "${USTATES}/${TENNIS}.state3"; is "${DIR}state_slot = \"3\"|savestate_auto_load = \"false\"|savestate_auto_save = \"false\"|" " -e 3"; check $? "a numbered slot with AUTO SAVE/LOAD off: \" -e 3\" still, both auto settings off -- the slot loads, nothing is written at quit" "$(got)"
 3049      sa 1 1 "" "${USTATES}/${TENNIS}.state.auto"; is "${DIR}state_slot = \"-1\"|savestate_auto_load = \"true\"|savestate_auto_save = \"true\"|" ""; check $? "the AUTO SAVE tile (-autosave 1, the .auto file, no slot): auto-load and auto-save on, no state_slot, nothing on stdout" "$(got)"
 3050      sa 0 "" "" "${USTATES}/${TENNIS}.state.auto"; is "${DIR}state_slot = \"-1\"|savestate_auto_load = \"true\"|savestate_auto_save = \"false\"|" ""; check $? "a .auto file with AUTO SAVE/LOAD off: the file alone turns auto-load on (Batocera's rule), the exit auto save stays off" "$(got)"
 3051      sa 1 1 2 ""; is "${DIR}state_slot = \"2\"|savestate_auto_load = \"true\"|savestate_auto_save = \"true\"|" "" && sa 0 "" "" ""; is "${DIR}savestate_auto_load = \"false\"|savestate_auto_save = \"false\"|" "" && sa 1 0 2 ""; is "${DIR}state_slot = \"2\"|savestate_auto_load = \"false\"|savestate_auto_save = \"false\"|" ""; check $? "without a state file (the fallback's -autosave 1 -state_slot 2; nothing; -autosave 0 -state_slot 2): today's appendconfig lines byte for byte and nothing on stdout" "$(got)"
 3052      sa 1 0 "" ""; is "${DIR}savestate_auto_load = \"false\"|savestate_auto_save = \"false\"|" ""; check $? "START NEW GAME (-autosave 0 alone): both off, no state_slot, no -e" "$(got)"
 3053      sa 1 "" "" "${USTATES}/${TENNIS}.state3" && [ "$(cat "${U}/sa.out")" = "" ] && sa 1 "" -1 "${USTATES}/${TENNIS}.state3" && [ "$(cat "${U}/sa.out")" = "" ] && sa 1 "" "3; rm -rf x" "${USTATES}/${TENNIS}.state3" && [ "$(cat "${U}/sa.out")" = "" ]; check $? "a slot that is not a number (none, -1, \"3; rm -rf x\") gets no -e: the fragment is eval'd inside RetroArch's command line" "stdout: [$(cat "${U}/sa.out")]"
 3054      SPLICE='RUNTHIS=$(echo ${RUNTHIS} | sed "s|--config|${EXTRAOPTS} --config|")'
 3055      grep -qF "${SPLICE}" "${U}/repo/runemu.sh"; check $? "runemu still splices setsettings' stdout before --config (the line --host and --set-shader ride)" "the splice line changed: $(grep -n 'EXTRAOPTS' "${U}/repo/runemu.sh" | tr '\n' '|' | cut -c1-240)"
 3056      RUNTHIS='${EMUPERF} /usr/bin/${RABIN} -L /tmp/cores/${CORE}_libretro.so --config ${RETROARCH_TEMP_CONFIG} --appendconfig ${RETROARCH_APPEND_CONFIG} "${ROMNAME}"'
 3057      sa 1 "" 3 "${USTATES}/${TENNIS}.state3"; EXTRAOPTS=$(cat "${U}/sa.out"); eval "${SPLICE}"
 3058      # The fragment carries its leading space, like --host's, so the splice leaves two before it; eval collapses them.
 3059      [[ "$(printf '%s' "${RUNTHIS}" | tr -s ' ')" == *'_libretro.so -e 3 --config ${RETROARCH_TEMP_CONFIG}'* ]]; check $? "spliced, the RetroArch command reads ... _libretro.so -e 3 --config ..." "RUNTHIS: ${RUNTHIS}"
 3060      RUNTHIS='${EMUPERF} /usr/bin/${RABIN} -L /tmp/cores/${CORE}_libretro.so --config ${RETROARCH_TEMP_CONFIG} --appendconfig ${RETROARCH_APPEND_CONFIG} "${ROMNAME}"'
 3061      sa 1 1 2 ""; EXTRAOPTS=$(cat "${U}/sa.out"); eval "${SPLICE}"
 3062      [[ "${RUNTHIS}" != *" -e "* ]] && [[ "${RUNTHIS}" == *'_libretro.so'*'--config ${RETROARCH_TEMP_CONFIG}'* ]]; check $? "and without a state file no -e is spliced" "RUNTHIS: ${RUNTHIS}"
 3063  else
 3064      check 1 "" "setsettings.sh has no --state_file= parser and set_autosave knows no state file (#196)"
 3065  fi
 3066  
```

## Excerpt: x/F1.: the history helpers and the first F1 checks (`:3198-3330` at 8ebaf8daad)

```text
 3198  echo "  F1. GENERIC_X64, the developers' QA device (D-QA-053): the boot quirks write only what a guest keeps, the serial shell stays on a VM, the launcher's print verb touches nothing (#307 PL-019, PL-022, PL-023, PL-033, PL-034, PL-073; #308)"
 3199  F1="${TMP}/f1"; mkdir -p "${F1}"
 3200  F1_PREV=417dcd8610     # the tree before stream F1: what the earlier builds installed, and so wrote
 3201  F1_QEMU="QEMU Standard PC (Q35 + ICH9, 2009)"
 3202  F1_QREL=projects/ROCKNIX/packages/hardware/quirks
 3203  # A directory's files: the working tree's, or BASE_REF's under --old, or a
 3204  # named ref's (f1_tree_at) -- an absent directory copies nothing.
 3205  f1_tree_at() { # <ref|""> <repo-relative dir> <destination>
 3206      mkdir -p "${3}"
 3207      if [ -n "${1}" ]; then
 3208          git -C "${ROOT}" ls-tree --name-only "${1}:${2}" 2>/dev/null | while IFS= read -r f; do
 3209              git -C "${ROOT}" show "${1}:${2}/${f}" > "${3}/${f}" || { echo "cannot read ${2}/${f} at ${1}" >&2; exit 2; }
 3210          done
 3211      elif [ -d "${ROOT}/${2}" ]; then
 3212          cp -a "${ROOT}/${2}/." "${3}/"
 3213      fi
 3214      chmod +x "${3}"/* 2>/dev/null; true
 3215  }
 3216  f1_tree() { if [ "${OLD}" -eq 1 ]; then f1_tree_at "${BASE_REF}" "$@"; else f1_tree_at "" "$@"; fi; }
 3217  F1BB=(); F1PATH="/shim:/usr/bin:/bin"
 3218  if [ -n "${BB}" ]; then F1BB=(--ro-bind "${TMP}/bbin" /bbin --ro-bind "${BB_HOST}" "${BB}"); F1PATH="/shim:/bbin:/usr/bin:/bin"; fi
 3219  # /etc as the image has it: read-only, with the links the systemd and kmod
 3220  # recipes make into /storage (tmpfiles.d, sysctl.d, modules-load.d, the udev
 3221  # rules, the *.conf.d of logind and friends), and no /etc/systemd/system --
 3222  # the systemd recipe removes it and points systemd's own unit directory at
 3223  # /storage/.config/system.d instead (its patch 0001).
 3224  F1ETC="${F1}/etc"; mkdir -p "${F1ETC}/systemd/system.conf.d" "${F1ETC}/udev" "${F1ETC}/dbus-1/system.d"
 3225  : > "${F1ETC}/systemd/journald.conf"; : > "${F1ETC}/systemd/system.conf"
 3226  cat "${ROOT}/projects/ROCKNIX/packages/sysutils/systemd/package.mk" "${ROOT}/projects/ROCKNIX/packages/sysutils/kmod/package.mk" \
 3227      | sed -n 's#^ *ln -sf \(/storage/[^ ]*\) ${INSTALL}/etc/\([^ ]*\)$#\1 \2#p' > "${F1}/etc-links"
 3228  while read -r tgt rel; do mkdir -p "$(dirname "${F1ETC}/${rel}")"; ln -sfn "${tgt}" "${F1ETC}/${rel}"; done < "${F1}/etc-links"
 3229  [ -L "${F1ETC}/tmpfiles.d" ] && [ -L "${F1ETC}/sysctl.d" ] && [ -L "${F1ETC}/udev/rules.d" ] && [ -L "${F1ETC}/modules-load.d" ]
 3230  check $? "the fixture's /etc carries the recipes' links into /storage ($(wc -l < "${F1}/etc-links") of them)" "the recipes' /etc links were not found; the fixture is not the image's /etc: $(tr '\n' ' ' < "${F1}/etc-links")"
 3231  # The shims: systemctl as the patched systemd behaves -- mask and unmask
 3232  # write a /dev/null link in /storage/.config/system.d, its unit directory --
 3233  # and the tools a quirk may call that do nothing here.
 3234  mkdir -p "${F1}/shim"
 3235  cat > "${F1}/shim/systemctl" <<'EOS'
 3236  #!/bin/bash
 3237  case "$1" in
 3238      mask)   shift; for u in "$@"; do mkdir -p /storage/.config/system.d; ln -sfn /dev/null "/storage/.config/system.d/${u}"; done ;;
 3239      unmask) shift; for u in "$@"; do [ "$(readlink "/storage/.config/system.d/${u}")" = /dev/null ] && rm -f "/storage/.config/system.d/${u}"; done ;;
 3240  esac
 3241  exit 0
 3242  EOS
 3243  for t in systemd-detect-virt modprobe udevadm plymouth logger blockdev; do printf '#!/bin/sh\nexit 0\n' > "${F1}/shim/${t}"; done
 3244  chmod +x "${F1}/shim"/*
 3245  # /storage as a guest's first boot leaves it: the /usr/config directories the
 3246  # links point into (each with its README), the shipped retroarch.cfg.
 3247  f1_storage() { # <dir>: a fresh /storage
 3248      rm -rf "${1}"; mkdir -p "${1}/.config/profile.d" "${1}/.config/retroarch" "${1}/.cache"
 3249      for d in tmpfiles.d sysctl.d modules-load.d modprobe.d udev.rules.d hwdb.d system.d logind.conf.d resolved.conf.d sleep.conf.d timesyncd.conf.d; do
 3250          mkdir -p "${1}/.config/${d}"; echo "shipped" > "${1}/.config/${d}/README"
 3251      done
 3252      printf 'video_driver = "vulkan"\nvideo_fullscreen = "true"\nvideo_fullscreen_x = "640"\nvideo_fullscreen_y = "480"\n' > "${1}/.config/retroarch/retroarch.cfg"
 3253  }
 3254  # /sys: one connected virtio output at 1280x800 (QEMU's default), fw_cfg's
 3255  # SSH port, the DMI names.
 3256  f1_sys() { # <dir> [<connector>:<status>:<mode>[,<mode>...]]...
 3257      local d="${1}" c name st modes; shift
 3258      rm -rf "${d}"; mkdir -p "${d}/class/drm" "${d}/firmware/qemu_fw_cfg/by_name/opt/org.rocknix.cloud_ssh_port" "${d}/class/dmi/id"
 3259      printf '10022' > "${d}/firmware/qemu_fw_cfg/by_name/opt/org.rocknix.cloud_ssh_port/raw"
 3260      echo QEMU > "${d}/class/dmi/id/sys_vendor"; echo "Standard PC (Q35 + ICH9, 2009)" > "${d}/class/dmi/id/product_name"
 3261      [ $# -eq 0 ] && set -- "card0-Virtual-1:connected:1280x800,1024x768,640x480"
 3262      for c in "$@"; do
 3263          name="${c%%:*}"; c="${c#*:}"; st="${c%%:*}"; modes="${c#*:}"
 3264          mkdir -p "${d}/class/drm/${name}"
 3265          echo "${st}" > "${d}/class/drm/${name}/status"
 3266          if [ "${st}" = connected ]; then echo enabled; else echo disabled; fi > "${d}/class/drm/${name}/enabled"
 3267          echo "${modes}" | tr ',' '\n' > "${d}/class/drm/${name}/modes"
 3268      done
 3269  }
 3270  # One boot's quirk pass, as autostart runs it: the platform's scripts, then
 3271  # the device's, each "${script}" 2>&1 >>boot.log -- so what a script says on
 3272  # stderr is what the journal holds, and that is what lands in <journal>.
 3273  f1_pass() { # <storage> <sys> <quirks dir> <journal>
 3274      ( bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr "${F1BB[@]}" \
 3275          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin \
 3276          --ro-bind "${F1ETC}" /etc --bind "${1}" /storage --ro-bind "${2}" /sys --ro-bind "${3}" /quirks \
 3277          --ro-bind "${F1}/shim" /shim --tmpfs /run --tmpfs /tmp --tmpfs /var --dev /dev --proc /proc \
 3278          --setenv PATH "${F1PATH}" --setenv HOME /storage \
 3279          bash -c 'for s in /quirks/platforms/GENERIC_X64/* "/quirks/devices/QEMU Standard PC (Q35 + ICH9, 2009)"/*; do
 3280                       [ -f "${s}" ] && bash "${s}" 2>&1 >>/run/boot.log
 3281                   done; exit 0' ) > "${4}" 2>&1
 3282  }
 3283  f1_quirks() { # <ref|""> <destination>: the platform and QEMU device quirks a build installs
 3284      rm -rf "${2}"; mkdir -p "${2}/platforms" "${2}/devices"
 3285      f1_tree_at "${1}" "${F1_QREL}/platforms/GENERIC_X64" "${2}/platforms/GENERIC_X64"
 3286      f1_tree_at "${1}" "${F1_QREL}/devices/${F1_QEMU}" "${2}/devices/${F1_QEMU}"
 3287  }
 3288  f1_new_files() { # <storage> <reference listing> -> files and links under <storage> not in the listing
 3289      ( cd "${1}" && find . \( -type f -o -type l \) | LC_ALL=C sort ) | LC_ALL=C comm -13 "${2}" -
 3290  }
 3291  f1_storage "${F1}/fresh"; ( cd "${F1}/fresh" && find . \( -type f -o -type l \) | LC_ALL=C sort ) > "${F1}/fresh.list"
 3292  f1_sys "${F1}/sys"
 3293  F1_UNDER=""; [ "${OLD}" -eq 1 ] && F1_UNDER="${BASE_REF}"
 3294  
 3295  # F1a. #307 PL-019 (and #308 F-VM-07, both seats): one boot's quirk pass on a
 3296  #      guest writes nothing into the read-only image -- the acceptance's own
 3297  #      `journalctl -b | grep -c 'Read-only file system'` -- says nothing on
 3298  #      the journal at all, and leaves /storage no file that changes a later
 3299  #      boot: no tmpfiles.d, sysctl.d, modules-load.d or udev rule, no unit or
 3300  #      mask in system.d.
 3301  f1_quirks "${F1_UNDER}" "${F1}/quirks.now"
 3302  f1_storage "${F1}/a"; f1_pass "${F1}/a" "${F1}/sys" "${F1}/quirks.now" "${F1}/a.journal"
 3303  F1_RO=$(grep -c 'Read-only file system' "${F1}/a.journal")
 3304  [ "${F1_RO}" -eq 0 ]; check $? "the quirk pass writes nothing into the read-only image: 0 'Read-only file system' lines on the journal" "the quirk pass writes into the read-only image: ${F1_RO} 'Read-only file system' lines, e.g. $(grep -m2 'Read-only file system' "${F1}/a.journal" | tr '\n' '|' | cut -c1-240)"
 3305  [ ! -s "${F1}/a.journal" ]; check $? "and says nothing else on the journal" "the pass says $(wc -l < "${F1}/a.journal") line(s) on the journal: $(head -3 "${F1}/a.journal" | tr '\n' '|' | cut -c1-240)"
 3306  F1_BOOT=$(f1_new_files "${F1}/a" "${F1}/fresh.list" | grep -E '^\./\.config/(tmpfiles\.d|sysctl\.d|modules-load\.d|modprobe\.d|udev\.rules\.d|hwdb\.d|system\.d|systemd)/')
 3307  [ -z "${F1_BOOT}" ]; check $? "and leaves /storage no file that changes a later boot (tmpfiles, sysctl, modules, udev, units, masks)" "the pass leaves /storage files that change later boots: $(echo "${F1_BOOT}" | tr '\n' ' ' | cut -c1-300)"
 3308  
 3309  # F1b. #307 PL-019's Already written: a guest that ran the earlier builds'
 3310  #      quirks carries what they wrote into /storage. The fixture is exactly
 3311  #      that: the pass of the tree before this stream (F1_PREV), run on a
 3312  #      fresh /storage beside a file of the owner's own in each of those
 3313  #      directories. One boot of the tree under test takes back every file
 3314  #      the retired quirks wrote -- by name, so the owner's files stay -- and
 3315  #      a second boot changes nothing.
 3316  f1_quirks "${F1_PREV}" "${F1}/quirks.prev"
 3317  f1_storage "${F1}/b"
 3318  echo "mine" > "${F1}/b/.config/tmpfiles.d/50-mine.conf"; echo "mine" > "${F1}/b/.config/sysctl.d/99-mine.conf"
 3319  echo "mine" > "${F1}/b/.config/modules-load.d/mine.conf"; ln -s /dev/null "${F1}/b/.config/system.d/mine.service"
 3320  # and one under a drop-in directory the retired writers used, with a name
 3321  # none of them wrote (weston got 10-vm-config.conf, never 10-generic-x64.conf)
 3322  mkdir -p "${F1}/b/.config/systemd/system/weston.service.d"; echo "mine" > "${F1}/b/.config/systemd/system/weston.service.d/10-generic-x64.conf"
 3323  ( cd "${F1}/b" && find . \( -type f -o -type l \) | LC_ALL=C sort ) > "${F1}/b.before"
 3324  f1_pass "${F1}/b" "${F1}/sys" "${F1}/quirks.prev" "${F1}/b.prev.journal"
 3325  F1_WROTE=$(f1_new_files "${F1}/b" "${F1}/b.before" | grep -vE '^\./\.config/(profile\.d/(001-device_config|090-ui_service|091-ui_shader)|cloud_setup_ssh)$')
 3326  [ -n "${F1_WROTE}" ]; check $? "the earlier builds' pass wrote $(echo "${F1_WROTE}" | grep -c .) file(s) into /storage the fixture can take back (the fixture holds what a guest holds)" "the earlier builds' pass wrote nothing -- the fixture proves nothing"
 3327  f1_pass "${F1}/b" "${F1}/sys" "${F1}/quirks.now" "${F1}/b.now.journal"
 3328  F1_LEFT=""; while IFS= read -r f; do [ -e "${F1}/b/${f}" ] || [ -L "${F1}/b/${f}" ] && F1_LEFT="${F1_LEFT} ${f}"; done <<< "${F1_WROTE}"
 3329  [ -z "${F1_LEFT}" ]; check $? "one boot of the tree under test takes back every one of them" "still on /storage after a boot: $(echo "${F1_LEFT}" | cut -c1-300)"
 3330  F1_MINE=0
```

## Excerpt: x/F2: the mupen64plus repair read from 417dcd8610 (`:4255-4290` at 8ebaf8daad)

```text
 4255  F2_OUT="$(awk -F' *= *' '/^\[/{sec=$0; next} /^[A-Za-z]/{ if (sec=="[Input-SDL-Control1]") n[$1]++; if ($1=="X Axis" && !seen++) xsec=sec }
 4256      END { d=""; for (k in n) if (n[k]>1) d=d" "k"x"n[k]; print xsec "|" (("DPad R" in n) ? "dpad" : "no-dpad") "|" d }' "${M64}")"
 4257  [ "${F2_OUT}" = "[Input-SDL-Control1]|dpad|" ]; check $? "Control1's DPad and axis mappings are read under [Input-SDL-Control1], each key once" "Control1 read as '${F2_OUT}' (section of the first X Axis | DPad R present | keys seen twice) -- a section header is spliced into it"
 4258  
 4259  # F2-5b. The audit of the fixes, claude G-F2-08 and gpt G-F2-04: the seed
 4260  # is fixed, but start_mupen64plus.sh copies it only when the player has no
 4261  # mupen64plus.cfg, so a GENERIC_X64 guest that ran mupen64plus before keeps
 4262  # the splice. The launcher's repair block is taken out of the script and run
 4263  # under the image's awk and mv against the audited seed with two settings
 4264  # the player changed: the six pasted lines go, every other byte stays, a
 4265  # second run changes nothing, and another device's copy -- SM8250's seed
 4266  # carries the same splice, upstream's file -- is left alone.
 4267  echo "  F2-5b. a GENERIC_X64 guest's existing mupen64plus.cfg loses the splice at the next launch and keeps everything else (#307 follow-up: claude G-F2-08, gpt G-F2-04)"
 4268  MR="${F2}/m64repair"; mkdir -p "${MR}"
 4269  src_of "${F2P}/emulators/standalone/mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh" "${MR}/start_mupen64plus.sh"
 4270  awk '/# ROCKNIX: GENERIC_X64 repair begin/,/# ROCKNIX: GENERIC_X64 repair end/' "${MR}/start_mupen64plus.sh" > "${MR}/repair.sh"
 4271  git -C "${ROOT}" show "417dcd8610:${F2P}/emulators/standalone/mupen64plus-sa/mupen64plus-sa-core/config/GENERIC_X64/mupen64plus.cfg" > "${MR}/spliced.cfg" 2>/dev/null
 4272  sed -e '0,/^plugin = 2$/s//plugin = 5/' -e 's/^ScreenWidth = .*/ScreenWidth = 1280/' "${MR}/spliced.cfg" > "${MR}/player.cfg"
 4273  f2_m64() { # <HW_DEVICE> <cfg>: run the repair block as the launcher would
 4274      ( set +u; HW_DEVICE="$1"; M64PCONF="$2"; PATH="${TMP}/bbin:${PATH}"; . "${MR}/repair.sh" ) > /dev/null 2>&1
 4275  }
 4276  cp "${MR}/player.cfg" "${MR}/g.cfg"; f2_m64 GENERIC_X64 "${MR}/g.cfg"
 4277  F2_OUT="$(diff "${MR}/player.cfg" "${MR}/g.cfg" | grep '^[<>]' | tr '\n' '|')"
 4278  [ -s "${MR}/repair.sh" ] && [ "${F2_OUT}" = "< ; Retroid Pocket Gamepad - default.ini|< [Retroid Pocket Gamepad]|< plugged = True|< mouse = False|< AnalogDeadzone = 0,0|< AnalogPeak = 32768,32768|" ]
 4279  check $? "GENERIC_X64: exactly the six pasted lines leave the player's copy; plugin = 5 and ScreenWidth = 1280 stay" "the repair changed: '${F2_OUT:-nothing}' $([ -s "${MR}/repair.sh" ] || echo '(start_mupen64plus.sh has no repair block)')"
 4280  cp "${MR}/g.cfg" "${MR}/g1.cfg"; f2_m64 GENERIC_X64 "${MR}/g.cfg"
 4281  cmp -s "${MR}/g.cfg" "${MR}/g1.cfg" && grep -q '^plugin = 5$' "${MR}/g.cfg"; check $? "a second launch changes nothing" "a second run changed the repaired copy"
 4282  cp "${MR}/player.cfg" "${MR}/s.cfg"; f2_m64 SM8250 "${MR}/s.cfg"
 4283  cmp -s "${MR}/s.cfg" "${MR}/player.cfg"; check $? "another device's copy is left as it is" "the repair touched a copy on HW_DEVICE=SM8250"
 4284  
 4285  # F2-6. #308 9-emulators claude F-EM-02: ppsspp-lr's strip of the
 4286  # aarch64-only -mno-outline-atomics ran in post_unpack, before scripts/unpack
 4287  # applies the patches (005 adds the flag), so it never found it. The recipe's
 4288  # hooks and its patches are run in scripts/unpack's order over the pinned
 4289  # source's files: x86_64 comes out without the flag, aarch64 with it.
 4290  echo "  F2-6. ppsspp-lr: the x86_64 strip of -mno-outline-atomics runs after the patches that add it (#308 F-EM-02)"
```

## Excerpt: y4 (`:8684-8905` at 8ebaf8daad)

```text
 8684  # y4. chksysconfig's boot pass, factoryreset, rocknix-evidence,
 8685  # rocknix-corekeep, runemu.sh's argument parsers and automount's
 8686  # internal-disk test.
 8687  P7="${P7:-${TMP}/p7}"; P7M="${P7}/misc"; mkdir -p "${P7M}"
 8688  P7ETC=(--tmpfs /etc); for e in /etc/ld.so.cache /etc/alternatives /etc/passwd /etc/group /etc/localtime; do [ -e "${e}" ] && P7ETC+=(--ro-bind "${e}" "${e}"); done
 8689  P7USR=(); for u in bin sbin lib lib64 libexec share; do [ -e "/usr/${u}" ] && P7USR+=(--ro-bind "/usr/${u}" "/usr/${u}"); done
 8690  P7MBB=(); if [ -n "${BB}" ]; then P7MBB=(--ro-bind "${TMP}/bbin" /bbin --ro-bind "${BB_HOST}" "${BB}"); fi
 8691  # The applets the evidence collector and the core keeper call that ARE
 8692  # busybox applets on the device, the image's here (the audit of the fixes,
 8693  # gpt G-B-15: these two ran on the host's tools); grep, sort and gzip are the
 8694  # device's GNU ones, the host's.
 8695  mkdir -p "${P7M}/bb"
 8696  if [ -n "${BB}" ]; then
 8697      for a in find mktemp tar cp mv rm touch date cut tr sed head tail du ls awk flock ln cat mkdir basename dirname wc stat df uname chmod readlink; do
 8698          printf '#!/bin/sh\n[ -x %s ] && exec %s %s "$@"\nexec %s %s "$@"\n' "${BB}" "${BB}" "${a}" "${BB_HOST}" "${a}" > "${P7M}/bb/${a}"; chmod +x "${P7M}/bb/${a}"
 8699      done
 8700  fi
 8701  # chksysconfig's functions, lifted as a lifts them.
 8702  P7K="${P7M}/chk"; mkdir -p "${P7K}/cfg/system/configs" "${P7K}/def/system/configs"
 8703  src_of "${CHK_REL}" "${P7K}/chksysconfig"
 8704  { sed -n '/^function prepare_settings_temp() {/,/^}/p' "${FN}"
 8705    awk '/^[a-z_]+\(\) *\{/{p=1} p{print} p&&/^\}/{p=0}' "${P7K}/chksysconfig"
 8706    printf 'logger() { echo "logger $*" >&2; }\nCONFIG_ROOT=%q; DEFAULT_ROOT=%q\nCFG_PATH="${CONFIG_ROOT}/system/configs"; CFG="${CFG_PATH}/system.cfg"; BACKUP="${CFG}.backup"\nrsync() { :; }\n' "${P7K}/cfg" "${P7K}/def"
 8707  } > "${P7K}/fns.sh"
 8708  printf 'system.hostname=DEFAULT\n' > "${P7K}/def/system/configs/system.cfg"
 8709  # mountpoint is the image's too, so the --old run judges PL-045's first cut
 8710  # under the tool the device has (claude G-B-04 of the audit of the fixes:
 8711  # busybox mountpoint compares st_dev and cannot see a bind on the same
 8712  # filesystem); the fix reads the mount table with the image's awk (bbin).
 8713  mkdir -p "${P7K}/bin"
 8714  if [ -n "${BB_HOST}" ]; then printf '#!/bin/sh\nexec %s mountpoint "$@"\n' "${BB_HOST}" > "${P7K}/bin/mountpoint"; chmod +x "${P7K}/bin/mountpoint"; fi
 8715  p7chk() { EXTRACT_ROOT="${P7K}/root" ROMS_ROOT="${P7K}/roms" PATH="${P7K}/bin:${TMP}/bbin:${PATH}" bash -c ". '${P7K}/fns.sh'; verify" 2>"${P7K}/err"; }
 8716  
 8717  # == PL-045: a copy on a folder that is there but not mounted yet is not called missing
 8718  mkdir -p "${P7K}/roms/backup/archive" "${P7K}/root"
 8719  printf 'system.hostname=X\n' > "${P7K}/cfg/system/configs/system.cfg"; cp "${P7K}/cfg/system/configs/system.cfg" "${P7K}/cfg/system/configs/system.cfg.backup"
 8720  printf '%s\n' "${P7K}/roms/backup/archive/2026_01_01-000000-PRE_RESTORE-ROCKNIX_SETTINGS.tar.gz" > "${P7K}/cfg/.restore-in-progress"
 8721  rm -f "${P7K}/cfg/.restore-reverted"
 8722  p7chk
 8723  [ -e "${P7K}/cfg/.restore-in-progress" ] && [ ! -e "${P7K}/cfg/.restore-reverted" ] && grep -q 'not mounted yet' "${P7K}/err"; check $? "#307 PL-045 / #308 claude F-PB-11: a copy under the roms folder while that folder is not a mountpoint (its internal-card directory present) leaves the mark for the later check and says nothing" "#307 PL-045: mark: $([ -e "${P7K}/cfg/.restore-in-progress" ] && echo kept || echo removed); said: '$(cat "${P7K}/cfg/.restore-reverted" 2>/dev/null)' -- the directory test read an unmounted card as a missing copy"
 8724  
 8725  # == #308 (stream E1's reading, PL-064's upgrade half): a whole .tmp beside a cut file with no record is the last good copy
 8726  rm -f "${P7K}/cfg/.restore-in-progress" "${P7K}/cfg/.restore-reverted" "${P7K}/cfg/system/configs/system.cfg.backup"
 8727  printf 'system.hostn' > "${P7K}/cfg/system/configs/system.cfg"
 8728  printf 'system.hostname=MINE\na.b=1\n' > "${P7K}/cfg/system/configs/system.cfg.tmp"
 8729  p7chk
 8730  [ "$(tr '\n' '|' < "${P7K}/cfg/system/configs/system.cfg")" = "system.hostname=MINE|a.b=1|" ] && [ ! -e "${P7K}/cfg/system/configs/system.cfg.tmp" ] && grep -q 'system.cfg.tmp' "${P7K}/err"; check $? "#307 PL-064 (upgrade half, E1): a cut system.cfg with no .backup and a whole system.cfg.tmp beside it takes the .tmp at boot, and says so" "#307 PL-064: system.cfg '$(tr '\n' '|' < "${P7K}/cfg/system/configs/system.cfg")'; .tmp: $([ -e "${P7K}/cfg/system/configs/system.cfg.tmp" ] && echo left || echo gone) -- the whole copy was deleted and the defaults reseeded"
 8731  printf 'system.hostname=REC\n' > "${P7K}/cfg/system/configs/system.cfg.backup"; printf 'system.hostn' > "${P7K}/cfg/system/configs/system.cfg"
 8732  printf 'system.hostname=TMP\n' > "${P7K}/cfg/system/configs/system.cfg.tmp"
 8733  p7chk
 8734  [ "$(cat "${P7K}/cfg/system/configs/system.cfg")" = "system.hostname=REC" ] && [ ! -e "${P7K}/cfg/system/configs/system.cfg.tmp" ]; check $? "#307 PL-064 (upgrade half, E1): with a good .backup the record wins over a .tmp, which is swept" "#307 PL-064: system.cfg '$(cat "${P7K}/cfg/system/configs/system.cfg")'"
 8735  
 8736  # == PL-044: factoryreset stops when the old folder will not go
 8737  P7R="${P7M}/reset"; mkdir -p "${P7R}/repo" "${P7R}/shim" "${P7R}/usrconfig/retroarch" "${P7R}/storage/.config/retroarch/stuck"
 8738  src_of projects/ROCKNIX/packages/rocknix/sources/scripts/factoryreset "${P7R}/repo/factoryreset"
 8739  printf '#!/bin/sh\nexit 0\n' > "${P7R}/shim/logger"; chmod +x "${P7R}/shim/logger"
 8740  echo shipped > "${P7R}/usrconfig/retroarch/retroarch.cfg"; echo mine > "${P7R}/storage/.config/retroarch/retroarch.cfg"
 8741  echo held > "${P7R}/storage/.config/retroarch/stuck/file"; chmod 555 "${P7R}/storage/.config/retroarch/stuck"
 8742  RC=$( ( bwrap --die-with-parent --tmpfs / --tmpfs /usr "${P7USR[@]}" --ro-bind "${P7R}/usrconfig" /usr/config "${P7MBB[@]}" \
 8743      --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 "${P7ETC[@]}" \
 8744      --bind "${P7R}/storage" /storage --ro-bind "${P7R}/shim" /shim --ro-bind "${P7R}/repo" /repo \
 8745      --dev /dev --proc /proc --tmpfs /tmp --setenv PATH /shim:/bbin:/usr/bin:/bin \
 8746      bash /repo/factoryreset retroarch-full > "${P7R}/out" 2>&1; echo $? ) 2>/dev/null )
 8747  chmod 755 "${P7R}/storage/.config/retroarch/stuck"
 8748  [ "${RC}" -ne 0 ] && [ ! -e "${P7R}/storage/.config/retroarch/retroarch" ] && [ "$(tail -1 "${P7R}/out" | sed 's/\x1b\[[0-9;]*m//g')" = "THE DEFAULT SETTINGS COULDN'T BE PUT BACK." ]; check $? "#307 PL-044: a retroarch folder that cannot be removed ends the reset (rc ${RC}) with the sentence, and the defaults are not copied inside it" "#307 PL-044: rc ${RC}; nested copy: $([ -e "${P7R}/storage/.config/retroarch/retroarch" ] && echo yes || echo no); last line: '$(tail -1 "${P7R}/out")'"
 8749  
 8750  # == PL-046: a file the filter could not replace is not archived raw
 8751  P7E="${P7M}/ev"; P7ES="${P7E}/storage"; mkdir -p "${P7ES}/.cache/log" "${P7ES}/.cache/cloud_sync" "${P7E}/repo" "${P7E}/shim" "${P7E}/etc"
 8752  src_of projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-evidence "${P7E}/repo/rocknix-evidence"
 8753  sed -n '/^function redact_credentials() {/,/^}/p' "${FN}" > "${P7E}/etc/001-functions"
 8754  printf 'NAME="ROCKNIX"\nBUILD_ID=test\n' > "${P7E}/etc/os-release"
 8755  for t in journalctl dmesg sysctl top; do printf '#!/bin/sh\necho "%s output"\n' "${t}" > "${P7E}/shim/${t}"; done
 8756  printf '#!/bin/sh\nexit 0\n' > "${P7E}/shim/logger"
 8757  # mv and rm that fail for exec.log's files when /run/p7-mv-fails and /run/p7-rm-fails exist.
 8758  printf '#!/bin/bash\n[ -e /storage/.p7-mv-fails ] && case "$*" in *exec.log.redacting*) echo "mv: I/O error" >&2; exit 1 ;; esac\n[ -x /p7mbb/mv ] && exec /p7mbb/mv "$@"\nexec /usr/bin/mv "$@"\n' > "${P7E}/shim/mv"
 8759  printf '#!/bin/bash\n[ -e /storage/.p7-rm-fails ] && case "$*" in *"/logs/exec.log"*) echo "rm: I/O error" >&2; exit 1 ;; esac\n[ -x /p7mbb/rm ] && exec /p7mbb/rm "$@"\nexec /usr/bin/rm "$@"\n' > "${P7E}/shim/rm"
 8760  chmod +x "${P7E}/shim"/*
 8761  p7ev() { # <verb>: rocknix-evidence whole; output in $P7E/out, rc in $RC
 8762      RC=$( ( bwrap --die-with-parent --tmpfs / --tmpfs /usr "${P7USR[@]}" \
 8763          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 8764          "${P7ETC[@]}" --ro-bind "${P7E}/etc/os-release" /etc/os-release --ro-bind "${P7E}/etc/001-functions" /etc/profile.d/001-functions \
 8765          --bind "${P7ES}" /storage --bind "${P7ES}/.cache/log" /var/log --ro-bind "${P7E}/repo" /repo --ro-bind "${P7E}/shim" /shim \
 8766          --ro-bind "${P7M}/bb" /p7mbb "${P7MBB[@]}" \
 8767          --dev /dev --proc /proc --tmpfs /tmp --tmpfs /run --setenv PATH "/shim:/p7mbb:/usr/bin:/bin" \
 8768          bash "/repo/${P7EVSCRIPT:-rocknix-evidence}" "$@" > "${P7E}/out" 2>&1; echo $? ) 2>/dev/null )
 8769  }
 8770  p7evreset() {
 8771      rm -rf "${P7ES}/.cache/log/evidence"; rm -f "${P7ES}"/.p7-*
 8772      printf 'runemu.sh: Executing /usr/bin/gopher64 --ra-password QA-EV-PLANT game.z64\n' > "${P7ES}/.cache/log/exec.log"
 8773  }
 8774  p7evarcs() { ls "${P7ES}/.cache/log/evidence"/*-evidence.tar.gz 2>/dev/null; }
 8775  # The sandbox's find, tar, flock and date are the image's (gpt G-B-15).
 8776  if [ -n "${BB}" ]; then
 8777      printf 'for a in find tar flock date mktemp; do if "$a" --help 2>&1 | head -1 | grep -q BusyBox; then echo "IMG:$a"; else echo "HOST:$a"; fi; done\n' > "${P7E}/repo/p7probe"
 8778      P7EVSCRIPT=p7probe p7ev
 8779      [ "$(grep -c '^IMG:' "${P7E}/out")" -eq 5 ]; check $? "#307 audit G-B-15 (gpt): the evidence collector runs under the image's find, tar, flock, date, and mktemp" "#307 audit G-B-15: $(tr '\n' ' ' < "${P7E}/out")"
 8780  fi
 8781  p7evreset; touch "${P7ES}/.p7-mv-fails"
 8782  p7ev collect
 8783  p7a=$(p7evarcs | head -1)
 8784  [ -n "${p7a}" ] && ! tar -xzOf "${p7a}" 2>/dev/null | grep -q QA-EV-PLANT && tar -xzOf "${p7a}" --wildcards '*/summary.txt' 2>/dev/null | grep -q '1 left out'; check $? "#307 PL-046: exec.log, whose filtered copy could not be moved into place, is left out -- not archived raw -- and the summary counts it left out" "#307 PL-046: rc ${RC}; archive: ${p7a:-none}; plant in it: $(tar -xzOf "${p7a}" 2>/dev/null | grep -c QA-EV-PLANT); summary: $(tar -xzOf "${p7a}" --wildcards '*/summary.txt' 2>/dev/null | grep 'credential filter:' | tail -1)"
 8785  p7evreset; touch "${P7ES}/.p7-mv-fails" "${P7ES}/.p7-rm-fails"
 8786  p7ev collect
 8787  [ "${RC}" -ne 0 ] && [ -z "$(p7evarcs)" ]; check $? "#307 PL-046: when the raw file can be neither replaced nor removed, no archive is written (rc ${RC})" "#307 PL-046: rc ${RC}; archives: $(p7evarcs | wc -l)"
 8788  
 8789  # == PL-077 (evidence half): two collections in one second keep two archives
 8790  p7evreset
 8791  printf '#!/bin/bash\ncase "$*" in "+%%Y_%%m_%%d-%%H%%M%%S") echo 2026_09_21-140000 ;; *) [ -x /p7mbb/date ] && exec /p7mbb/date "$@"; exec /usr/bin/date "$@" ;; esac\n' > "${P7E}/shim/date"; chmod +x "${P7E}/shim/date"
 8792  p7ev collect; p7rc1=${RC}; p7ev collect
 8793  [ "${p7rc1}" -eq 0 ] && [ "${RC}" -eq 0 ] && [ "$(p7evarcs | wc -l)" -eq 2 ]; check $? "#307 PL-077 (evidence half): two collections in one second leave two archives" "#307 PL-077: rc ${p7rc1}/${RC}; archives: $(p7evarcs | xargs -rn1 basename | tr '\n' ' ')"
 8794  rm -f "${P7E}/shim/date"
 8795  
 8796  # == #308 10-packages-and-build claude F-PB-16: the core keeper, disarmed, reads nothing; a dump one byte over the cap is cut
 8797  P7C="${P7M}/core"; mkdir -p "${P7C}/storage/.config" "${P7C}/shim" "${P7C}/repo" "${P7C}/bb"
 8798  src_of projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-corekeep "${P7C}/repo/rocknix-corekeep"
 8799  printf '#!/bin/bash\nexit 0\n' > "${P7C}/shim/logger"; chmod +x "${P7C}/shim/logger"
 8800  if [ -n "${BB}" ]; then printf '#!/bin/sh\nexec %s head "$@"\n' "${BB}" > "${P7C}/bb/head"; chmod +x "${P7C}/bb/head"; fi
 8801  p7ck() { # <stdin producer> <exe> <epoch> [env...]: the keeper under the image's head; the note of <exe>.<epoch> in $P7NOTE
 8802      local prod="$1" exe="$2" when="$3"; shift 3
 8803      ( bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 8804          --ro-bind /etc /etc --bind "${P7C}/storage" /storage --ro-bind "${P7C}/shim" /shim --ro-bind "${P7C}/bb" /p7bb --ro-bind "${P7C}/repo" /repo "${P7MBB[@]}" \
 8805          --ro-bind "${P7M}/bb" /p7mbb --dev /dev --proc /proc --tmpfs /tmp --tmpfs /var --setenv PATH /shim:/p7bb:/p7mbb:/usr/bin:/bin "$@" \
 8806          bash -c "${prod} | bash /repo/rocknix-corekeep ${exe} 4242 ${when} 11 '!usr!bin!${P7EXEPATH:-${exe}}'" ) > "${P7C}/out" 2>&1
 8807      P7NOTE="$(cat "${P7C}"/storage/.cache/log/cores/core.*."${when}".4242.txt 2>/dev/null)"
 8808  }
 8809  if [ -n "${BB}" ]; then
 8810      p7ck 'for a in head flock find mkdir mv rm df date; do if "$a" --help 2>&1 | head -1 | grep -q BusyBox; then echo "IMG:$a" >&2; else echo "HOST:$a" >&2; fi; done' probe 1
 8811      [ "$(grep -c '^IMG:' "${P7C}/out")" -eq 8 ]; check $? "#307 audit G-B-15 (gpt): the core keeper runs under the image's head, flock, find, mkdir, mv, rm, df, and date" "#307 audit G-B-15: $(grep -E '^(IMG|HOST):' "${P7C}/out" | tr '\n' ' ')"
 8812  fi
 8813  rm -f "${P7C}/storage/.config/keep-core-dumps"
 8814  p7consumed=$(python3 - "${P7C}" "$(printf '%q ' bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 --ro-bind /etc /etc --bind "${P7C}/storage" /storage --ro-bind "${P7C}/shim" /shim --ro-bind "${P7C}/repo" /repo "${P7MBB[@]}" --ro-bind "${P7M}/bb" /p7mbb --dev /dev --proc /proc --tmpfs /tmp --tmpfs /var --setenv PATH /shim:/p7mbb:/usr/bin:/bin bash /repo/rocknix-corekeep retroarch 1 1 11 '!usr!bin!retroarch')" <<'EOS'
 8815  import subprocess, sys
 8816  p = subprocess.Popen(sys.argv[2], shell=True, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
 8817  chunk = b"\0" * 65536; sent = 0
 8818  try:
 8819      for _ in range(1024):              # 64 MiB offered
 8820          p.stdin.write(chunk); p.stdin.flush(); sent += len(chunk)
 8821  except (BrokenPipeError, OSError):
 8822      pass
 8823  try: p.stdin.close()
 8824  except Exception: pass
 8825  p.wait(); print(sent)
 8826  EOS
 8827  )
 8828  [ -n "${p7consumed}" ] && [ "${p7consumed}" -lt 16777216 ]; check $? "#308 10-packages-and-build claude F-PB-16: disarmed, the keeper exits without reading the dump (${p7consumed} of 67108864 bytes taken before the pipe closed)" "#308 F-PB-16: ${p7consumed} bytes were read and dropped -- the whole dump, while the crashed process waited"
 8829  date -u '+armed %Y-%m-%d' > "${P7C}/storage/.config/keep-core-dumps"
 8830  p7ck "head -c 3001 /dev/zero" retroarch 5000 --setenv CORE_MAX_BYTES 3000
 8831  printf '%s' "${P7NOTE}" | grep '^dump' | grep -qi 'cut' && ! printf '%s' "${P7NOTE}" | grep '^dump' | grep -q 'whole'; check $? "#308 10-packages-and-build claude F-PB-16: a dump one byte over a 3000-byte cap is noted CUT under the image's head (which reads ahead past the cap)" "#308 F-PB-16: note: $(printf '%s' "${P7NOTE}" | grep '^dump' | cut -c1-140)"
 8832  p7ck "head -c 3000 /dev/zero" retroarch 5001 --setenv CORE_MAX_BYTES 3000
 8833  printf '%s' "${P7NOTE}" | grep '^dump' | grep -q 'whole'; check $? "#308 10-packages-and-build claude F-PB-16: and one of exactly the cap is noted whole" "#308 F-PB-16: note: $(printf '%s' "${P7NOTE}" | grep '^dump' | cut -c1-140)"
 8834  
 8835  # == #308 10-packages-and-build gpt F-PB-15: the ring keeps the newest crashes, by time, notes included
 8836  rm -rf "${P7C}/storage/.cache"; mkdir -p "${P7C}/storage/.cache/log/cores"
 8837  for w in 1000 2000 3000; do echo x | gzip > "${P7C}/storage/.cache/log/cores/core.retroarch.${w}.1.gz"; echo note > "${P7C}/storage/.cache/log/cores/core.retroarch.${w}.1.txt"; done
 8838  p7ck "head -c 100 /dev/zero" emulationstation 4000 --setenv CORE_MAX_BYTES 1048576
 8839  [ -e "${P7C}/storage/.cache/log/cores/core.emulationstation.4000.4242.gz" ] && [ ! -e "${P7C}/storage/.cache/log/cores/core.retroarch.1000.1.gz" ] && [ -e "${P7C}/storage/.cache/log/cores/core.retroarch.3000.1.gz" ]; check $? "#308 10-packages-and-build gpt F-PB-15: the newest crash (the interface's, epoch 4000) is kept and the oldest (1000) goes, whatever the names sort to" "#308 F-PB-15: left: $(ls "${P7C}/storage/.cache/log/cores" | tr '\n' ' ') -- sorted by executable, the newest dump went first"
 8840  rm -rf "${P7C}/storage/.cache"; mkdir -p "${P7C}/storage/.cache/log"
 8841  P7FREE=$(df -k "${P7C}/storage" | awk 'NR==2{print $4}')
 8842  for w in 6001 6002 6003 6004 6005; do p7ck "head -c 100 /dev/zero" retroarch "${w}" --setenv CORE_MAX_BYTES 1048576 --setenv CORE_MIN_FREE_KB "${P7FREE}"; done
 8843  [ "$(ls "${P7C}/storage/.cache/log/cores"/*.txt 2>/dev/null | wc -l)" -le 3 ] && [ -e "${P7C}/storage/.cache/log/cores/core.retroarch.6005.4242.txt" ]; check $? "#308 10-packages-and-build gpt F-PB-15: five crashes refused for space leave at most three notes, the newest kept" "#308 F-PB-15: notes: $(ls "${P7C}/storage/.cache/log/cores" 2>/dev/null | tr '\n' ' ')"
 8844  
 8845  # == #308 10-packages-and-build gpt F-PB-20 (via stream F2): the interface's cap follows its path, not its truncated name
 8846  rm -rf "${P7C}/storage/.cache"; mkdir -p "${P7C}/storage/.cache/log"
 8847  P7FREE=$(df -k "${P7C}/storage" | awk 'NR==2{print $4}')
 8848  P7EXEPATH=emulationstation p7ck "head -c 100 /dev/zero" emulationstatio 7000 --setenv CORE_MIN_FREE_KB "$(( P7FREE - 400000 ))"
 8849  printf '%s' "${P7NOTE}" | grep '^dump' | grep -q 'plus the 1073741824 byte cap'; check $? "#308 10-packages-and-build gpt F-PB-20: a crash reported as 'emulationstatio' (the kernel's 15-character name) from /usr/bin/emulationstation gets the interface's 1 GiB cap" "#308 F-PB-20: note: $(printf '%s' "${P7NOTE}" | grep '^dump' | cut -c1-140) -- the 256 MiB cap was applied"
 8850  P7EXEPATH=""
 8851  
 8852  # == #308 10-packages-and-build gpt F-PB-21: one dump is written at a time
 8853  rm -rf "${P7C}/storage/.cache"; mkdir -p "${P7C}/storage/.cache/log"
 8854  p7ck "{ head -c 1000 /dev/zero; sleep 3; head -c 1000 /dev/zero; }" retroarch 8000 --setenv CORE_MAX_BYTES 1048576 &
 8855  P7A=$!; sleep 1
 8856  p7ck "head -c 100 /dev/zero" emulationstation 8001 --setenv CORE_MAX_BYTES 1048576 &
 8857  P7BK=$!; sleep 1
 8858  p7mid=$([ -e "${P7C}/storage/.cache/log/cores/core.emulationstation.8001.4242.txt" ] && echo yes || echo no)
 8859  wait "${P7A}" "${P7BK}" 2>/dev/null
 8860  [ "${p7mid}" = "no" ] && [ -e "${P7C}/storage/.cache/log/cores/core.emulationstation.8001.4242.gz" ] && [ -e "${P7C}/storage/.cache/log/cores/core.retroarch.8000.4242.gz" ]; check $? "#308 10-packages-and-build gpt F-PB-21: a second crash's handler waits while the first is still writing, then keeps its own" "#308 F-PB-21: the second note existed mid-way through the first dump: ${p7mid}; left: $(ls "${P7C}/storage/.cache/log/cores" | tr '\n' ' ')"
 8861  
 8862  # == #308 10-packages-and-build gpt F-PB-17: save-state arguments come from their own arguments, never a ROM's name
 8863  P7U2="${P7M}/runemu"; mkdir -p "${P7U2}"
 8864  src_of "${RE_REL:-projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh}" "${P7U2}/runemu.sh"
 8865  sed -n '/^function parse_savestate_arguments() {/,/^}/p' "${P7U2}/runemu.sh" > "${P7U2}/parse.sh"
 8866  P7ROM="/storage/roms/snes/Demo -state_slot 2 - Part.sfc"
 8867  p7pa=$(bash -c '. "$0"; ARGUMENTS="$*"; parse_savestate_arguments "$@"; printf "S=%s A=%s F=%s" "${SNAPSHOT}" "${AUTOSAVE}" "${STATEFILE}"' "${P7U2}/parse.sh" "${P7ROM}" -Psnes --core=snes9x --emulator=retroarch --controllers="-p1index 0" -state_slot 7 2>/dev/null)
 8868  p7pb=$(bash -c '. "$0"; ARGUMENTS="$*"; parse_savestate_arguments "$@"; printf "S=%s A=%s" "${SNAPSHOT}" "${AUTOSAVE}"' "${P7U2}/parse.sh" "/storage/roms/snes/Game -autosave 0 x.sfc" -Psnes --core=snes9x --emulator=retroarch --controllers="-p1index 0" -autosave 1 2>/dev/null)
 8869  [ "${p7pa}" = "S=7 A= F=" ] && [ "${p7pb}" = "S= A=1" ]; check $? "#308 10-packages-and-build gpt F-PB-17: a ROM named 'Demo -state_slot 2 - Part' launched with -state_slot 7 reads slot 7, and 'Game -autosave 0 x' with -autosave 1 reads 1" "#308 F-PB-17: got '${p7pa}' and '${p7pb}' -- the first match in the joined line was the ROM's name"
 8870  
 8871  # == #308 8-es-menus-and-core claude (stream E2, the launch command): the platform is the -P argument, not the last -P anywhere
 8872  sed -n '/^ARGUMENTS="\$@"$/,/^CORE=/p' "${P7U2}/runemu.sh" | sed '$d' > "${P7U2}/platform.sh"
 8873  p7pl=$(bash -c '. "$0"; printf "%s" "${PLATFORM}"' "${P7U2}/platform.sh" "/storage/roms/snes/Super Mario-Party.sfc" -Psnes --core=snes9x --emulator=retroarch --controllers="-p1index 0" --host --port 55435 --nick "My-Player" 2>/dev/null)
 8874  [ "${p7pl}" = "snes" ]; check $? "#308 8-es-menus-and-core (E2): a launch carrying -Psnes and a later --nick 'My-Player' reads the platform snes" "#308 E2: the platform read '${p7pl}' -- the last -P in the joined line was the nick's"
 8875  
 8876  # == #308 10-packages-and-build claude F-PB-13: the disk under /storage is never an external candidate
 8877  P7AM="${P7M}/automount"; rm -rf "${P7AM}"; mkdir -p "${P7AM}/sys/devices/block/sda/sda2" "${P7AM}/sys/class/block" "${P7AM}/sys/block"
 8878  src_of projects/ROCKNIX/packages/rocknix/sources/scripts/automount "${P7AM}/automount"
 8879  echo 41943040 > "${P7AM}/sys/devices/block/sda/size"; echo 2 > "${P7AM}/sys/devices/block/sda/sda2/partition"
 8880  ln -s ../../devices/block/sda/sda2 "${P7AM}/sys/class/block/sda2"; ln -s ../devices/block/sda "${P7AM}/sys/block/sda"
 8881  echo "/dev/sda2 /storage ext4 rw 0 0" > "${P7AM}/mounts"
 8882  sed -n '/^function external_node_present() {/,/^}/p' "${P7AM}/automount" | sed "s#/sys/#${P7AM}/sys/#g; s#/proc/mounts#${P7AM}/mounts#g" > "${P7AM}/fn.sh"
 8883  PATH="${TMP}/bbin:${PATH}" bash -c ". '${P7AM}/fn.sh'; external_node_present"; p7rc=$?
 8884  [ "${p7rc}" -eq 1 ]; check $? "#308 10-packages-and-build claude F-PB-13: /storage on /dev/sda2 and no other disk: no external card is present (rc 1)" "#308 F-PB-13: rc ${p7rc} -- sda2 was stripped to itself, and sda, the internal disk, counted as an external card"
 8885  mkdir -p "${P7AM}/sys/devices/block/mmcblk1"; echo 62333952 > "${P7AM}/sys/devices/block/mmcblk1/size"; ln -s ../devices/block/mmcblk1 "${P7AM}/sys/block/mmcblk1"
 8886  PATH="${TMP}/bbin:${PATH}" bash -c ". '${P7AM}/fn.sh'; external_node_present"; p7rc=$?
 8887  [ "${p7rc}" -eq 0 ]; check $? "#308 10-packages-and-build claude F-PB-13: and a 32 GB mmcblk1 beside it is one (rc 0)" "#308 F-PB-13: rc ${p7rc}"
 8888  rm -rf "${P7AM}/sys"; mkdir -p "${P7AM}/sys/devices/block/mmcblk0/mmcblk0p2" "${P7AM}/sys/class/block" "${P7AM}/sys/block"
 8889  echo 124735488 > "${P7AM}/sys/devices/block/mmcblk0/size"; echo 2 > "${P7AM}/sys/devices/block/mmcblk0/mmcblk0p2/partition"
 8890  ln -s ../../devices/block/mmcblk0/mmcblk0p2 "${P7AM}/sys/class/block/mmcblk0p2"; ln -s ../devices/block/mmcblk0 "${P7AM}/sys/block/mmcblk0"
 8891  echo "/dev/mmcblk0p2 /storage ext4 rw 0 0" > "${P7AM}/mounts"
 8892  PATH="${TMP}/bbin:${PATH}" bash -c ". '${P7AM}/fn.sh'; external_node_present"; p7rc=$?
 8893  [ "${p7rc}" -eq 1 ]; check $? "#308 10-packages-and-build claude F-PB-13: a handheld's /storage on mmcblk0p2 still reads mmcblk0 as internal (rc 1)" "#308 F-PB-13: rc ${p7rc}"
 8894  # ---- audit #307, stream A ----
 8895  # The cloud scripts against the real rclone the image ships (a copy, as the
 8896  # busybox above is a copy), over an alias remote whose "cloud" is a folder
 8897  # of the fixture's, inside bwrap -- so every filter, listing, --max-delete,
 8898  # check and delete is rclone's own, not a shim's idea of it. A shim in front
 8899  # of it records every argv to /ctl/argv and, for a line of /ctl/fail
 8900  # ("<ERE over the argv><tab><exit code>"), fails that call instead: the one
 8901  # listing a flaky link loses, the endpoint that answers nothing. The host's
 8902  # rclone stands in when no build root is here. The image's busybox serves
 8903  # the applets it serves on the device (find, stat, awk, sed, tr, flock, cmp,
 8904  # unzip, tar, ...), as in case n. Written before each fix and seen to FAIL
 8905  # on the scripts at 417dcd8610 (BASE_REF=417dcd8610 ... --old).
```

## Excerpt: y/A.: stream A's rclone, shims, nbin wrappers and the sandbox helpers (`:8895-9032` at 8ebaf8daad)

```text
 8895  # The cloud scripts against the real rclone the image ships (a copy, as the
 8896  # busybox above is a copy), over an alias remote whose "cloud" is a folder
 8897  # of the fixture's, inside bwrap -- so every filter, listing, --max-delete,
 8898  # check and delete is rclone's own, not a shim's idea of it. A shim in front
 8899  # of it records every argv to /ctl/argv and, for a line of /ctl/fail
 8900  # ("<ERE over the argv><tab><exit code>"), fails that call instead: the one
 8901  # listing a flaky link loses, the endpoint that answers nothing. The host's
 8902  # rclone stands in when no build root is here. The image's busybox serves
 8903  # the applets it serves on the device (find, stat, awk, sed, tr, flock, cmp,
 8904  # unzip, tar, ...), as in case n. Written before each fix and seen to FAIL
 8905  # on the scripts at 417dcd8610 (BASE_REF=417dcd8610 ... --old).
 8906  echo "  A. audit #307/#308, stream A: the cloud scripts against the image's rclone"
 8907  SA="${TMP}/sa"; mkdir -p "${SA}/shim" "${SA}/nbin"
 8908  SA_RCLONE_SRC=$(image_tool_source rclone version) || exit 2
 8909  if [ -z "${SA_RCLONE_SRC}" ] || ! cp "${SA_RCLONE_SRC}" "${SA}/rclone.real"; then
 8910      echo "    FAIL  no rclone to run the stream A cases against (none in a build root, none on the host)"; FAIL=$((FAIL + 1))
 8911      : > "${SA}/rclone.real"
 8912  fi
 8913  chmod +x "${SA}/rclone.real" 2>/dev/null
 8914  echo "    rclone: $("${SA}/rclone.real" version 2>/dev/null | head -1) -- a copy of ${SA_RCLONE_SRC:-nothing}"
 8915  cat > "${SA}/shim/rclone" <<'EOR'
 8916  #!/bin/bash
 8917  # The image's rclone, with the calls /ctl/fail names ("<ERE><tab><exit>")
 8918  # failed instead; /ctl/kill ("<ERE><tab><n>") kills the caller's whole
 8919  # process group at the n-th matching call, before it runs -- a kill, not a
 8920  # failure; /ctl/post ("<ERE><tab><command>") runs a command after a
 8921  # matching call -- another
 8922  # writer landing between two steps; /ctl/nohash makes `backend features`
 8923  # describe a remote with no hashes (WebDAV, SFTP, SMB, FTP).
 8924  printf '%s\n' "$*" >> /ctl/argv
 8925  # A successful provider-features fixture must contain a valid answer.
 8926  if [ "$1" = backend ] && [ "$2" = features ] && [ -s /ctl/provider-features ]; then
 8927      cat /ctl/provider-features; exit 0
 8928  fi
 8929  if [ -s /ctl/fail ]; then
 8930      while IFS=$'\t' read -r pat code; do
 8931          [ -n "${pat}" ] || continue
 8932          if printf '%s' "$*" | grep -qE -- "${pat}"; then
 8933              printf '%s\n' "$*" >> /ctl/fault-fired
 8934              echo "ERROR : injected failure ${code}" >&2
 8935              exit "${code}"
 8936          fi
 8937      done < /ctl/fail
 8938  fi
 8939  if [ -s /ctl/kill ]; then
 8940      while IFS=$'\t' read -r pat nth; do
 8941          [ -n "${pat}" ] || continue
 8942          printf '%s' "$*" | grep -qE -- "${pat}" || continue
 8943          n=$(( $(cat /ctl/kill.count 2>/dev/null || echo 0) + 1 )); echo "${n}" > /ctl/kill.count
 8944          [ "${n}" -eq "${nth}" ] && kill -9 -- "-$(cut -d' ' -f5 /proc/self/stat)"
 8945      done < /ctl/kill
 8946  fi
 8947  if [ -s /ctl/hang ]; then
 8948      # /ctl/hang ("<ERE><tab><seconds>"): a call that sits silent, as a cloud
 8949      # that accepts and never answers leaves it -- one process, so whatever
 8950      # bound ends the call ends it.
 8951      while IFS=$'\t' read -r pat secs; do
 8952          [ -n "${pat}" ] || continue
 8953          printf '%s' "$*" | grep -qE -- "${pat}" && exec sleep "${secs}"
 8954      done < /ctl/hang
 8955  fi
 8956  if [ -e /ctl/nohash ] && [ "$1" = backend ] && [ "$2" = features ]; then
 8957      printf '{\n\t"Name": "qa",\n\t"Hashes": [],\n\t"Features": {\n\t\t"BucketBased": false\n\t}\n}\n'
 8958      exit 0
 8959  fi
 8960  if [ -s /ctl/post ]; then
 8961      /sa/rclone.real "$@"; rc=$?
 8962      while IFS=$'\t' read -r pat cmd; do
 8963          [ -n "${pat}" ] || continue
 8964          printf '%s' "$*" | grep -qE -- "${pat}" && eval "${cmd}"
 8965      done < /ctl/post
 8966      exit "${rc}"
 8967  fi
 8968  exec /sa/rclone.real "$@"
 8969  EOR
 8970  printf '#!/bin/sh\ncase "$*" in *"route show default"*) [ -e /ctl/noroute ] || echo "default via 10.0.2.2 dev eth0" ;; esac\n' > "${SA}/shim/ip"
 8971  printf '#!/bin/sh\n[ -e /ctl/noping ] && exit 1\nexit 0\n' > "${SA}/shim/ping"
 8972  printf '#!/bin/sh\nexit 0\n' > "${SA}/shim/logger"
 8973  printf '#!/bin/sh\nexit 0\n' > "${SA}/shim/systemd-tmpfiles"
 8974  chmod +x "${SA}/shim"/*
 8975  printf 'export PATH=/shim:/nbin:/usr/bin:/bin\nexport HOME=/storage\n' > "${SA}/profile"
 8976  SA_BB=()
 8977  if [ -n "${BB}" ]; then
 8978      # Every applet the image's /usr/bin links to busybox that these scripts
 8979      # call -- cp, mv, rm and the rest joined the list after the audit of the
 8980      # fixes (gpt coverage note 3: the sandbox ran the host's cp and mv).
 8981      # grep, sort and timeout are real binaries on the image, and the host's
 8982      # stand in for them.
 8983      for a in sed tr head wc cut awk tail tee mkfifo sleep flock stat md5sum find cmp mktemp unzip tar \
 8984               cp mv rm mkdir cat date ls readlink uniq basename dirname touch chmod ln xargs; do
 8985          printf '#!/bin/sh\n[ -x %s ] && exec %s %s "$@"\nexec %s %s "$@"\n' "${BB}" "${BB}" "${a}" "${BB_HOST}" "${a}" > "${SA}/nbin/${a}"
 8986          chmod +x "${SA}/nbin/${a}"
 8987      done
 8988      SA_BB=(--ro-bind "${BB_HOST}" "${BB}")
 8989  fi
 8990  # /usr as a tmpfs of the host's directories, for a case that needs /usr/config
 8991  # to be the fixture's (the helper reads its defaults there).
 8992  SA_USR=(); for u in bin sbin lib lib64 libexec share; do [ -e "/usr/${u}" ] && SA_USR+=(--ro-bind "/usr/${u}" "/usr/${u}"); done
 8993  sa_new() { # <name>: a fresh fixture directory; its path on stdout
 8994      local d="${SA}/f-$1"
 8995      rm -rf "${d}"; mkdir -p "${d}"/storage/.config/rclone "${d}"/storage/.cache/cloud_sync "${d}"/storage/roms \
 8996          "${d}"/cloud "${d}"/ctl "${d}"/log "${d}"/varrun "${d}"/repo
 8997      printf '[qa]\ntype = alias\nremote = /cloud\n' > "${d}/storage/.config/rclone/rclone.conf"
 8998      : > "${d}/ctl/argv"; : > "${d}/ctl/fail"; : > "${d}/ctl/kill"; : > "${d}/ctl/post"; : > "${d}/ctl/hang"
 8999      printf '#!/bin/sh\ncase "$1" in --label) echo QA ;; --previous|--legacy) ;; *) echo QA-deadbeef01 ;; esac\n' > "${d}/repo/cloud_device_id"
 9000      chmod +x "${d}/repo/cloud_device_id"
 9001      printf '%s' "${d}"
 9002  }
 9003  sa_script() { # <fixture> <script...>: the scripts under test into its /repo (working tree, or BASE_REF under --old)
 9004      local d="$1" s; shift
 9005      for s in "$@"; do src_of "${RCLONE_REL}/${s}" "${d}/repo/${s}"; chmod +x "${d}/repo/${s}"; done
 9006  }
 9007  # SA_EXTRA: more bwrap arguments for the next runs, after /usr -- a file
 9008  # the image ships under /usr/bin, overlaid for a case (A47); empty otherwise.
 9009  SA_EXTRA=()
 9010  sa_run() { # <fixture> <script> [args...]: the script whole, in the sandbox; stdout+stderr to ${d}/out, rc in RC, seconds in DT
 9011      local d="$1" s="$2" t0; shift 2
 9012      t0=$(date +%s)
 9013      RC=$( ( cd "${d}/storage" && setsid -w timeout 180 bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr ${SA_EXTRA[@]+"${SA_EXTRA[@]}"} "${SA_BB[@]}" \
 9014          --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
 9015          --ro-bind /etc /etc --ro-bind "${SA}/profile" /etc/profile \
 9016          --bind "${d}/storage" /storage --bind "${d}/cloud" /cloud --bind "${d}/ctl" /ctl \
 9017          --ro-bind "${SA}/shim" /shim --ro-bind "${SA}/nbin" /nbin --ro-bind "${SA}/rclone.real" /sa/rclone.real \
 9018          --ro-bind "${d}/repo" /repo --bind "${d}/log" /var/log --bind "${d}/varrun" /var/run \
 9019          --dev /dev --proc /proc --tmpfs /tmp --chdir "${SA_CWD:-/storage}" \
 9020          --setenv PATH "/shim:/nbin:/usr/bin:/bin" --setenv HOME /storage \
 9021          bash "/repo/${s}" "$@" > "${d}/out" 2>&1; echo $? ) 2>/dev/null )
 9022      DT=$(( $(date +%s) - t0 ))
 9023  }
 9024  sa_tail() { sed 's/\x1b\[[0-9;]*m//g' "$1/out" | grep -v '^\s*$' | tail -${2:-4} | tr '\n' '|' | cut -c1-240; }
 9025  # The run's own outcome line, as case n reads it: colour off, no protocol
 9026  # marker, no rclone stats, no rule of dashes.
 9027  sa_outcome() {
 9028      sed 's/\x1b\[[0-9;]*[A-Za-z]//g' "$1/out" | tr '\r' '\n' | grep -vE '^>>> |^(Transferred:|Checks:|Elapsed time:|Errors:|Deleted:|Renamed:|Transferring:|Checking:)|^[[:space:]]*\*[[:space:]]|^[=-]{4,}$|^[[:space:]]*$' | tail -1
 9029  }
 9030  
 9031  # A1. PL-001 (#307, F-CS-01 both seats + F-CS-03 gpt): --match --apply acts
 9032  #     only on the plan the preview showed. A system whose listing fails is
```

## Excerpt: aa: the two-argument check (`:13818-13832` at 8ebaf8daad)

```text
13818  # made merges -- newer wins, what differs is shelved first, the old folder goes only once every name is present;
13819  # the same folder with no marker is somebody's own and is still refused.
13820  rm -f "${LY}"/rec/*; touch "${LY}/rec/rocknix-files" "${LY}/rec/cur-exists"
13821  ly_run "$(ly_conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)" --apply; [ "${LYRC}" = 4 ] && grep -q 'REFUSING: qa:/pixelelated/Saves already exists' "${LY}/out" && grep -q '^>>> why THE NEW FOLDER ALREADY HAS FILES IN IT' "${LY}/out" && ! grep -q '^copy ' "${LY}/rec/argv"; check $? "a current folder with no marker is somebody's own: the move is refused with its why and nothing is copied (rc ${LYRC})" "$(ly_out)"
13822  touch "${LY}/rec/marker"
13823  ly_run "$(ly_conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)" --check; grep -q 'Another device has already moved' "${LY}/out" && [ "${LYRC}" = 0 ] && ! grep -q '^copy ' "${LY}/rec/argv"; check $? "--check on the fleet's folder says the tiers merge and changes nothing (rc ${LYRC})" "$(ly_out)"
13824  rm -f "${LY}/rec/argv"
13825  ly_run "$(ly_conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)" --apply; [ "${LYRC}" = 0 ] && grep -qE '^copy qa:/ROCKNIX/Saves qa:/pixelelated/Saves .*--update --backup-dir qa:/pixelelated/Saves-replaced/[0-9_-]+-move' "${LY}/rec/argv" && grep -q '^delete qa:/ROCKNIX/Saves ' "${LY}/rec/argv" && grep -q '^rmdirs qa:/ROCKNIX/Saves' "${LY}/rec/argv" && grep -q '^SAVES_REMOTE="/pixelelated/Saves"$' "${LY}/storage/.config/cloud_sync.conf" && grep -q '^>>> unit SAVES|1|1$' "${LY}/out"; check $? "--apply onto the fleet's folder merges the saves: copy --update with the shelf as --backup-dir, the old folder removed after the presence check, the pointer moved, the item announced (rc ${LYRC})" "$(ly_out) $(grep -E '^(copy|delete|rmdirs)' "${LY}/rec/argv" | cut -c1-120 | tr '\n' '|')"
13826  ! grep -qE '^copy qa:/ROCKNIX/Saves qa:/pixelelated/Saves-replaced/' "${LY}/rec/argv"; check $? "with nothing differing, nothing is shelved from the old folder"
13827  rm -f "${LY}/rec/argv"; touch "${LY}/rec/differ"
13828  ly_run "$(ly_conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)" --apply; [ "${LYRC}" = 0 ] && grep -qE '^copy qa:/ROCKNIX/Saves qa:/pixelelated/Saves-replaced/[0-9_-]+-move --files-from-raw' "${LY}/rec/argv" && grep -q '1 saves file(s) differ' "${LY}/out"; check $? "a file that differs is shelved from the old folder before the update copy (rc ${LYRC})" "$(ly_out)"
13829  # The mixed-installation test's fresh device (D-CLOUD-158, #354): on the current default, no saves in
13830  # the current folder, the fork's earlier /ROCKNIX holding them. --join points the device there -- a
13831  # setting, nothing copied -- so it reads the player's saves at once and is offered the move as every
13832  # device on that folder is; without it the scan offered CREATE IT beside them.
```

## Excerpt: the call sites (ae, af, ag, ah) and the verdict (`:14177-14239` at 8ebaf8daad)

```text
14177  echo "  ae. cloud folder state table and archive writer/reader contracts (#365, #383)"
14178  # Keep nested host fixtures on the same selected build filesystem.
14179  layout_args=(--output "${TMP}/cloud-layout")
14180  if [ "${OLD}" -eq 1 ]; then layout_args+=(--ref "${BASE_REF}")
14181  else layout_args+=(--source-root "${ROOT}"); fi
14182  [ -n "${SA_RCLONE_SRC:-}" ] && layout_args+=(--rclone "${SA_RCLONE_SRC}")
14183  if [ "${MIGRATION_AVAILABLE}" -eq 0 ]; then
14184      # Archive selection/writer/reader coverage survives engine retirement.
14185      layout_args+=(--archives-only)
14186      echo "    ae. historical migration matrix NOT APPLICABLE; ordinary T24 archive contracts still run"
14187  fi
14188  "${HARNESS_ROOT}/tools/rasteratops-cloud-layout-test" "${layout_args[@]}"
14189  check $? "applicable cloud folder/archive contract regressions" "cloud folder/archive contract regressions failed"
14190  
14191  echo "  af. content inactivity across provider retries (#401)"
14192  # Run both complete scripts with the candidate tools. A silent copy lasts
14193  # twelve seconds unless the product ends it; only the configured idle time
14194  # is shortened, keeping the real six-second grace. The old unguarded calls
14195  # return success here. Existing A7/A11/A29 cases cover selection and stamps.
14196  for content_script in cloud_content_backup cloud_content_restore; do
14197      CG=$(sa_new "inactivity-${content_script}")
14198      sa_script "${CG}" "${content_script}"
14199      printf 'CONTENT_REMOTE="/Content"\nRCLONE_NET_OPTS="--timeout 1s --low-level-retries 10 --retries 1"\n' > "${CG}/storage/.config/cloud_sync.conf"
14200      mkdir -p "${CG}/storage/roms/nes" "${CG}/cloud/Content/ROMs/nes"
14201      echo game > "${CG}/storage/roms/nes/probe.nes"
14202      echo game > "${CG}/cloud/Content/ROMs/nes/probe.nes"
14203      printf '^copy \t12\n' > "${CG}/ctl/hang"
14204      sa_run "${CG}" "${content_script}" --with-media nes
14205      cg_stamp="${CG}/storage/.cache/cloud_sync/last-${content_script#cloud_}"
14206      cg_stamp="${cg_stamp%_*}-${cg_stamp##*_}"
14207      [ "${RC}" -eq 124 ] && [ "${DT}" -ge 6 ] && [ "${DT}" -lt 12 ] && grep -qx '>>> why YOUR CLOUD STOPPED ANSWERING' "${CG}/out"
14208      check $? "${content_script} ends inactivity and says why (rc ${RC}, ${DT}s)" "${content_script}: rc ${RC}, ${DT}s; $(sa_tail "${CG}")"
14209      [ "$(awk '{print $2}' "${cg_stamp}" 2>/dev/null)" = 124 ] && [ "$(grep -c '^copy ' "${CG}/ctl/argv")" -eq 1 ] && [ -z "$(find "${CG}/varrun" -name 'cloud-content.*' -print)" ]
14210      check $? "${content_script} stamps failure, starts no game-list copy and removes its guard" "${content_script}: stamp/second-copy/cleanup mismatch"
14211      : > "${CG}/ctl/hang"
14212      # A real local copy followed by steadily advancing stats exceeds the
14213      # same seven-second inactivity window without being a stalled call.
14214      printf '^copy \tfor n in 1 2 3 4 5; do printf "Transferred: %%s KiB / 5 KiB\\n" "$n"; sleep 2; done\n' > "${CG}/ctl/post"
14215      sa_run "${CG}" "${content_script}" nes
14216      [ "${RC}" -eq 0 ] && [ "${DT}" -ge 9 ] && [ "$(awk '{print $2}' "${cg_stamp}" 2>/dev/null)" = 0 ]
14217      check $? "${content_script} keeps a progressing transfer alive beyond the window" "${content_script}: progressing run rc ${RC}, ${DT}s; $(sa_tail "${CG}")"
14218  done
14219  
14220  # #421: exercise actual writer functions with the same candidate applets.
14221  echo "  ag. settings writers retain private file permissions"
14222  # These host helpers need the owned build-drive temporary directory; the
14223  # bubblewrap device fixtures above intentionally do not inherit host TMPDIR.
14224  TMPDIR="${TMP}" "${ROOT}/tools/settings-modes-test" --profile "${FN}" --chksysconfig "${CHK}" \
14225    --busybox "${BB_HOST}" --output "${TMP}/settings-modes.json"
14226  check $? "#421: private modes and refused publications" "#421: settings mode regression (details above)"
14227  
14228  # #526: optional melonDS defaults never erase an owner's configuration.
14229  echo "  ah. melonDS update preserves settings and adds missing hotkeys"
14230  src_of projects/ROCKNIX/packages/rocknix/sources/post-update "${TMP}/post-update"
14231  TMPDIR="${TMP}" python3 "${HARNESS_ROOT}/tools/melonds-upgrade-test" --post-update "${TMP}/post-update" \
14232    --busybox "${BB_HOST}" --output "${TMP}/melonds-upgrade.json"
14233  check $? "#526: preserved configuration and atomic hotkey additions" "#526: melonDS update regression (details above)"
14234  
14235  if [ "${NOT_APPLICABLE}" -ne 0 ]; then echo "${NOT_APPLICABLE} HISTORICAL FEATURE GROUP(S) NOT APPLICABLE -- no checks counted as PASS"; fi
14236  if [ "${FAIL}" -eq 0 ] && [ "${SKIPPED}" -eq 0 ]; then echo "PASSED"; exit 0
14237  elif [ "${FAIL}" -eq 0 ]; then echo "PASSED, ${SKIPPED} SKIPPED -- a check that did not run has not passed"; exit 3
14238  else echo "${FAIL} CHECK(S) FAILED, ${SKIPPED} SKIPPED"; exit 1; fi
14239  
```

## The first reader's 02-forward-audit.md (whole)

# Forward audit: M6.P2 T15, the last-good scripts test (#662)

Read at `8ebaf8daad` (the branch `HEAD` at stage A, `60d7f6a5b2`, does not differ on the file). The lens is brittleness. The bench is the host, with no guest: **Can this be done on the VM? Yes -- on the host, where the suite runs by design. The one thing the host lacks, a build root's busybox, is read from the M7 root `m7-signin-build-20261022-07` (BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`) through `QA_SYSTEM_ROOT`, a read of one file the suite copies.**

## Phase 2: #662's checklist

Each criterion's state at stage B, with the artifact that will tick it. The coordinator ticks at acceptance, from the artifacts.

| # | Criterion (§ 7, short) | State at stage B | Artifact |
| --- | --- | --- | --- |
| 1 | the folder holds 00 to 05 | 00, 01 and 02 written; 03 to 05 at stage B to D | this folder |
| 2 | the lint prints PASS (pre-issue before D, resolution at close) | not yet run | `tools/lint-audit-artifacts` |
| 3 | `review-plan.json` and the seat's provenance; the packet's scan | stage C | `second-opinions/` |
| 4 | the punch-list issue at its Phase 7 outcomes | stage D onward | the audit issue |
| 5 | `reviewed-at` / `fixed-at` | `reviewed-at: 60d7f6a5b2` recorded in `00` | #662's body at hand-back |
| 6 | `01` § Scope | written: the inventory row, 408 commits, the 34 sections | `01-research-notes.md` |
| 7 | 34 coverage rows | written below | § Coverage |
| 8 | both runs, and the busybox-dependent checks | written below | § The runs, § The checks that depend on the busybox |
| 9 | the twelve `--old` recipes | written below | § The runs |
| 10 | no handheld, provider, guest, build or forbidden edit; every run with `SIGINT ignored=0` | holds so far; one write under `/tmp` was made and removed, recorded in `00` | `00-running-log.md` |
| 11 | Q6's 34-row brittleness table and the split proposal | stage B | `04` § Q6 |
| 12 | Q3 by section; the `|| true` sites, `check $?`, `skip()`, NOT APPLICABLE, no-busybox; the ten sorted | the ten are sorted (the fixture's history dependency, `00`); the rest is stage B | `04` § Q3 |
| 13 | Q7 | stage B | `04` § Q7 |
| 14 | Q5's wall time by section | measured (the timed run, below) | `04` § Q5 |
| 15 | every proof carries a `proved:` cell | below | § Proofs |
| 16 | `question:`, `box-check`, no `tools/` change before a stream; the two call sites' flags | no `tools/` change; the call sites at stage E | the branch's diff |
| 17 | the fixed tip refuses or marks a host-busybox run; the image run is judged on the tree | stage E | § The runs at the fixed tip |
| 18 | the retro | stage G | `docs/retros/` |
| 19 | the checkers, and `vm-qa:148`'s exit rule stated | stage E onward | § The runs at the fixed tip |

## Coverage

One row per section, as the brief's criterion 7 asks: the section's letter, its first line, its claim, its weight in the image run, its flips under the host's busybox, its seconds in the timed run, the `--old` recipe that promises a FAIL in it (and whether that run reaches it before it stops), and its sandbox and git-history dependencies counted from its lines. The sub-groups of `x`, `y` and `z` are under `04` § Q6, per the coordinator's 00:27 and 00:33 rulings.

| Section | Lines | Its claim (the `echo` line, cut) | Header claim | Checks (image run) | Flip to FAIL under the host's busybox | Seconds | `--old` recipe that promises a FAIL (reached before the stop?) | sandboxes / git-history reads |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `a` | `:429` | chksysconfig keeps and restores the last good system.cfg | yes | 13 | 0 | 0.4 | `1d1503180d` (yes), `c15050c897` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `b` | `:518` | backuptool: a kill mid-tar leaves the previous archive; a failed restore puts the snapshot back | yes | 14 | 0 | 2.9 | `1d1503180d` (yes) | 3 bwrap, 0 `sa_run`; 0 history |
| `c` | `:607` | set_setting is one rename; sort_settings refuses an empty result | yes | 9 | 0 | 0.2 | `1d1503180d` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `d` | `:650` | cloud_sync_helper and the saves scripts keep the config's last good copy; stamps survive a kill | yes | 13 | 0 | 0.4 | `1d1503180d` (yes) | 1 bwrap, 0 `sa_run`; 0 history |
| `e` | `:723` | nothing a screen can show carries an exit code, a log path, a tool's name or a flag | yes | 1 | 0 | 0.1 | `1d1503180d` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `f` | `:766` | backuptool: rclone.conf never enters an archive, and the scanner knows rclone's key names (#52) | yes | 10 | 0 | 0.6 | `1d1503180d` (yes) | 3 bwrap, 0 `sa_run`; 0 history |
| `g` | `:839` | the in-script RCLONE_NET_OPTS fallback is the shipped value (#146) | yes | 6 | 0 | 0.0 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `h` | `:854` | the rclone wrapper: an automatic run's stalled call ends at the ceiling, a deliberate run's at the stall ceili… | yes | 11 | 0 | 6.3 | `8707919349` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `i` | `:893` | cloud_net_ready settles on a held default route however NetworkManager judges connectivity | yes | 6 | 0 | 14.3 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `j` | `:934` | cloud_sync_helper migrates the shipped retry bound once, and leaves a hand-tuned value alone (#107) | yes | 6 | 0 | 0.5 | `1d1503180d` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `k` | `:962` | backuptool: what the image ships does not travel, and an older archive's copy of it is not put back (#45); a R… | yes | 25 | 11 | 1.0 | `1d1503180d` (yes), `53f390b1e9` (yes), `34aca64afd` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `l` | `:1114` | a missing cloud folder reads as not there yet whatever the server's words (#142) | yes | 23 | 0 | 0.2 | `1d1503180d` (yes), `53f390b1e9` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `m` | `:1251` | the shipped device name becomes this unit's own, once; a player's name is never touched (#50) | yes | 23 | 0 | 0.6 | `1d1503180d` (yes), `53f390b1e9` (yes) | 3 bwrap, 0 `sa_run`; 0 history |
| `n` | `:1403` | a deliberate cloud_backup ends a transfer that stops making progress at the stall ceiling, and says it couldn'… | yes | 11 | 7 | 41.6 | `8707919349` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `o` | `:1534` | set_setting system.hostname default keeps the line chksysconfig's sentinel reads, empty (D-NET-009) | yes | 7 | 0 | 0.1 | `8707919349` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `p` | `:1565` | raofflineproxy-ctl: enable records hardcore and turns it off, disable puts it back; both harmless twice (#165,… | yes | 38 | 0 | 1.6 | `34aca64afd` (yes), `d79281066c` (no), `cee1656c33` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `q` | `:1752` | 099-networkservices: a daemon fragment that sets no CONF inherits none from the fragment before it (#166) | yes | 9 | 0 | 2.2 | `0f7785e6ed` (no) | 2 bwrap, 0 `sa_run`; 0 history |
| `r` | `:1860` | the launch log carries no credential value: setsettings' Added setting and Fetch lines, runemu's Executing lin… | yes | 18 | 0 | 0.1 | `cee1656c33` (yes), `28a80357ed` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `s` | `:1949` | rocknix-evidence: every file in the bundle has been through the credential filter, summary.txt says so, and wi… | yes | 13 | 0 | 1.3 | `28a80357ed` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `t` | `:2033` | raofflineproxy-ctl scan, topup and ready against the client the tree describes: the refusals, the index rule b… | yes | 80 | 42 | 33.6 | `cee1656c33` (yes), `3387cf5da0` (yes), `70b6c70ca7` (yes) | 6 bwrap, 0 `sa_run`; 1 history |
| `u` | `:2856` | wifictl current, saved, forget and join read NetworkManager, not the setting; forget says when it dropped the … | yes | 19 | 0 | 0.5 | `655f103cc5` (yes) | 2 bwrap, 0 `sa_run`; 0 history |
| `v` | `:2991` | the save state manager's arguments reach RetroArch as Batocera's launcher carries them (#196, D-UI-057): runem… | yes | 20 | 0 | 0.3 | `655f103cc5` (yes) | 0 bwrap, 0 `sa_run`; 0 history |
| `w` | `:3067` | cheevos_armsx2.sh writes one Token line to secrets.ini, however often it runs (#170) | yes | 5 | 0 | 0.2 | none | 1 bwrap, 0 `sa_run`; 0 history |
| `x` | `:3113` | the launcher's incremental-save modes, the password's handoff, and the keeper's cut/whole note (#209, #198, #2… | **no** | 350 | 33 | 82.1 | none | 24 bwrap, 0 `sa_run`; 19 history |
| `y` | `:7796` | audit #307 / #308, stream B: backuptool, wifictl, the settings writer and lock, factoryreset, chksysconfig, ro… | **no** | 448 | 180 | 248.3 | none | 24 bwrap, 145 `sa_run`; 3 history |
| `z` | `:13182` | the audit of the fix round, stream B: the conf read as text, a flag's password redacted, the restore's lists a… | **no** | 92 | 36 | 17.4 | none | 0 bwrap, 1 `sa_run`; 0 history |
| `aa` | `:13723` | cloud_migrate_layout --state, --keep and --follow (#353, D-CLOUD-160/161): the layout as facts, a kept folder,… | **no** | 0 | 0 | ? | none | 2 bwrap, 0 `sa_run`; 0 history |
| `ab` | `:13913` | cloud_scan (#350, D-CLOUD-156): the opening scan's three items, the content scan's one, the selected folder fa… | **no** | 24 | 0 | 1.4 | `1d1503180d` (no) | 2 bwrap, 0 `sa_run`; 0 history |
| `ac` | `:14121` | the Retroid Pocket Nova's ledcontrol (#332): LED BRIGHTNESS writes the LEDs, rgb with no colour set lights whi… | **no** | 6 | 0 | 0.1 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `ad` | `:14142` | a backup does not make a missing earlier-default saves folder (D-CLOUD-172, #363): the offer instead, nothing … | **no** | 4 | 4 | 2.7 | none | 0 bwrap, 4 `sa_run`; 0 history |
| `ae` | `:14177` | cloud folder state table and archive writer/reader contracts (#365, #383) | **no** | 1 | 0 | 19.8 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `af` | `:14191` | content inactivity across provider retries (#401) | **no** | 6 | 6 | 33.7 | none | 0 bwrap, 2 `sa_run`; 0 history |
| `ag` | `:14221` | settings writers retain private file permissions | **no** | 1 | 0 | 0.4 | none | 0 bwrap, 0 `sa_run`; 0 history |
| `ah` | `:14229` | melonDS update preserves settings and adds missing hotkeys | **no** | 1 | 0 | 0.1 | none | 0 bwrap, 0 `sa_run`; 0 history |

**The header claims sections `a` to `w` only** (`:7-148`): `x` to `ah`, 11 sections holding 933 of the 1,313 checks, have no claim there. **No `--old` recipe names a FAIL in `w` to `ah`,** and none of the twelve reaches past `s` or `x` (§ The runs). So **20 sections, `s` (or `x`) to `ah`, have no control that runs.**

## The runs

Every run is in this worktree, with `TMPDIR=/workspace/tmp/m6-t15/tmp`, started through `vm-qa:158`'s launcher (SIGINT and SIGPIPE to default). Each first line reads `signals: SigIgn=0000000001000004 SIGINT ignored=0 SIGPIPE ignored=0`. Outputs are in `.qa-scratch/t15/`.

| Run | Command | Exit | Wall | Banner (the busybox and its source) | PASS / FAIL / SKIP | A FAIL would mean |
| --- | --- | ---: | ---: | --- | --- | --- |
| 1, the image's busybox | `QA_SYSTEM_ROOT=<m7-signin-build-20261022-07>/build.pixelelated-GENERIC_X64.x86_64/image/system python3 -c "$SIGDFL" tools/last-good-scripts-test` | 0 | 517 s | `BusyBox v1.36.1 (2026-10-05 03:37:19 UTC) ... -- a copy of /workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/...`; rclone `v1.75.2` | 1,313 / 0 / 0, `PASSED` (after `1 HISTORICAL FEATURE GROUP(S) NOT APPLICABLE`) | a script under test no longer keeps its last good state, or prints what a screen must not, under the device's own applets: a `bug` for that script's lane. **The tree's baseline** (the coordinator, 00:36) |
| 2, the host's busybox | `python3 -c "$SIGDFL" tools/last-good-scripts-test` (`QA_SYSTEM_ROOT` unset) | 1 | 677 s | `BusyBox v1.37.0 (Ubuntu 1:1.37.0-7ubuntu1) ... -- a copy of /usr/bin/busybox`; rclone `v1.60.1-DEV`, a copy of `/usr/bin/rclone` | 994 / 319 / 0 | nothing about the tree: the run judges the host's applets (§ below). This is the run every M6 worktree makes by default |
| `bbhost` | run 2 with only the busybox swapped: `QA_SYSTEM_ROOT=/workspace/tmp/m6-t15/roots/bbhost/image/system` (the host's busybox, the image's rclone) | 1 | 678 s | `BusyBox v1.37.0 ...`; rclone `v1.75.2` | 994 / 319 / 0, every verdict equal to run 2's | the busybox alone makes the 319 |
| `rchost` | run 1 with only the rclone swapped (the image's busybox, the host's rclone 1.60.1-DEV) | 0 | 512 s | `BusyBox v1.36.1 ...`; rclone `v1.60.1-DEV` | 1,313 / 0 / 0, every verdict equal to run 1's | the rclone's version makes no verdict: stream A's cases do not tell 1.60.1 from 1.75.2 (a Q4 finding) |
| timed | run 1, each line stamped with its seconds (`tools/t15-attribution.sh`) | 0 | 515 s | as run 1 | 1,313 / 0 / 0 | the wall time by section, `04` § Q5 |
| `--help` / `--nosuch` | `tools/last-good-scripts-test --help`; `--nosuch` | 0 / 2 | — | — | — | — |

**The twelve `--old` recipes** (the header's `:167-226`), each once, under the image's busybox (`QA_SYSTEM_ROOT` on the same root):

| `BASE_REF` | rc | wall | PASS | FAIL | where it stopped |
| --- | ---: | ---: | ---: | ---: | --- |
| `1d1503180d` (default) | 2 | 211 s | 73 | 118 | `s`: `rocknix-evidence` is not at the ref |
| `53f390b1e9` | 2 | 156 s | 123 | 116 | `x`: `rocknix-corekeep` is not at the ref |
| `c15050c897` | 2 | 213 s | 88 | 103 | `s`: `rocknix-evidence` |
| `8707919349` | 2 | 156 s | 161 | 78 | `x`: `rocknix-corekeep` |
| `34aca64afd` | 2 | 70 s | 179 | 60 | `x`: `rocknix-corekeep` |
| `0f7785e6ed` | 2 | 0 s | 0 | 0 | at once: `fatal: invalid object name '0f7785e6ed'` |
| `d79281066c` | 2 | 0 s | 0 | 0 | at once: `fatal: invalid object name 'd79281066c'` |
| `cee1656c33` | 2 | 133 s | 256 | 90 | `x`: `rocknix-corekeep` |
| `28a80357ed` | 2 | 114 s | 218 | 122 | `x`: `rocknix-corekeep` |
| `3387cf5da0` | 2 | 118 s | 264 | 85 | `x`: `rocknix-corekeep` |
| `655f103cc5` | 2 | 121 s | 267 | 82 | `x`: `rocknix-corekeep` |
| `70b6c70ca7` | 2 | 119 s | 296 | 71 | `x`: `rocknix-corekeep` |

**A FAIL in an `--old` run would mean** that the guard the recipe names fires against the scripts from before its fix. **None of the twelve reaches a verdict.**
- **Two refs are dead:** `0f7785e6ed` (q's control) and `d79281066c` (p's pending and flushed control) exist nowhere in the repository.
- **The other ten** stop at `s` (`rocknix-evidence` absent at the ref) or `x` (`rocknix-corekeep`): `src_of` exits 2 for the whole run (`:320-325`). So from `s` or `x` to `ah`, **no section has a control that runs**.
- **Before each stop**, the promised sections fail, except one. `70b6c70ca7`'s `t` fails on patch application (*003 to 006 do not apply to the pinned client*), and its five `012` checks never run.

The detail is in `00`.

## The checks that depend on the busybox

Every check whose verdict differs between run 1 (the image's BusyBox 1.36.1) and run 2 (the host's 1.37.0): **319**, each PASS under the image's and FAIL under the host's.
- **The pairing:** the two runs count 1,313 checks in the same order, so pairs align by position, and every PASS/PASS pair's text matches. One more pair differs only because its text carries a literal tab (`--set-content-remote refuses '/tab<TAB>name' ...`, PASS in both), and is not counted.
- **The attribution:** `bbhost` reproduces all 319 with the image's rclone, and `rchost` none with the host's rclone. So the busybox makes each one.
- **The applet:**
  - **`flock` is named on 61 lines** (*applet not found*: the suite's `flock` shims exec a busybox that lacks it);
  - **127 lines show its consequence** (rc 75, *another sync is already running*, a held lock);
  - **131 lines name no applet and carry no applet error.** No other refusal appears in either run, so these are *likely* `flock`'s too, **not proven**: a 1.37 applet that behaved differently without erroring would read the same.
- **By section and group:** `y/A` 95, `y` (`y1`-`y4`) 59, `t` 42, `x/D` 33, `y/CF` 26, `z` 24, `z/S315` 12, `k` 11, `n` 7, `af` 6, `ad` 4.

| # | Section / group | The applet | The host run's FAIL text (cut) |
| ---: | --- | --- | --- |
| 1 | `k` | busybox 1.37.0, no applet named on the line | rc 1: >>> why THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS/[31mTHE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS. NOTHIN |
| 2 | `k` | busybox 1.37.0, no applet named on the line | archive lists:   |
| 3 | `k` | busybox 1.37.0, no applet named on the line | duckstation:  melonDS:  flycast:  aethersx2:  |
| 4 | `k` | busybox 1.37.0, no applet named on the line | log: held back 5 file(s) that hold only a RetroAchievements token; the emulator writes them again at its next start (#169) held back 5 file( |
| 5 | `k` | busybox 1.37.0, no applet named on the line | rc 1; scanner: silent; archives: 0 -- until #169 its anchor was lower-case only, and the emulators' keys are capitalised |
| 6 | `k` | busybox 1.37.0, no applet named on the line | rc 1: [32mKEEPING A COPY OF YOUR CURRENT SETTINGS...[0m/>>> why COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS/[31mCOULDN'T KEEP A COPY OF |
| 7 | `k` | busybox 1.37.0, no applet named on the line | ini='the player's ini' own='the player's own' |
| 8 | `k` | busybox 1.37.0, no applet named on the line | snapshot: none; .dat in it: absent |
| 9 | `k` | busybox 1.37.0, no applet named on the line | rc 1: [32mKEEPING A COPY OF YOUR CURRENT SETTINGS...[0m/>>> why COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS/[31mCOULDN'T KEEP A COPY OF |
| 10 | `k` | busybox 1.37.0, no applet named on the line | ini='the player's ini' own='the player's own' |
| 11 | `k` | busybox 1.37.0, no applet named on the line | link: symlink; screen: 2 KEEPING line(s) |
| 12 | `n` | busybox 1.37.0, no applet named on the line | no such why line; protocol lines:  |
| 13 | `n` | `flock` (its consequence: rc 75 or a held lock) | the outcome line is 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 14 | `n` | busybox 1.37.0, no applet named on the line | the script's next sentence is glued to rclone's last progress line, which had no newline: '' (#153, LINK5 on MinIO, 2026-09-13) |
| 15 | `n` | busybox 1.37.0, no applet named on the line | log:  |
| 16 | `n` | `flock` (named: *applet not found*) | rc 75; stamp ''; marker: no; tail: flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try again |
| 17 | `n` | `flock` (its consequence: rc 75 or a held lock) | the outcome line is 'Skipped: another cloud sync is already running. Try again when it's done.' -- tools/cloud-round-trip's ALLOWED_SCRIPT w |
| 18 | `n` | `flock` (its consequence: rc 75 or a held lock) | rc 75 after 1s; log:  -- a fixed ceiling ends the transfers a deliberate run exists for |
| 19 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out: ; stamp: none |
| 20 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 21 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp: none; log:  |
| 22 | `t` | busybox 1.37.0, no applet named on the line | state mtime 1789380000 vs 1789380000, content: {   "online": true } ; probes:  (#186 PL-03) |
| 23 | `t` | `flock` (named: *applet not found*) | rc 75; log: ; err: flock: applet not found/logger -t raofflineproxy-ctl scan: another scan or top-up is running/ (#186 PL-23/PL-02) |
| 24 | `t` | busybox 1.37.0, no applet named on the line | jobs:  (#186 PL-23) |
| 25 | `t` | busybox 1.37.0, no applet named on the line | out: ; stamp: ; export: 101 102 105  |
| 26 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 27 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out: ; stamp:  -- a failed game read as COMPLETED (#186 PL-24) |
| 28 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; jobs: ; out:  |
| 29 | `t` | `flock` (named: *applet not found*) | rc 75; out: ; stamp: ; err: flock: applet not found/logger -t raofflineproxy-ctl scan: another scan or top-up is running/ |
| 30 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; jobs: 0; out:  |
| 31 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 32 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out:  |
| 33 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; sleeps: ; mark: none; log:  (#186 PL-04) |
| 34 | `t` | busybox 1.37.0, no applet named on the line | log: ; stamp:  |
| 35 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; log:  |
| 36 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes:  |
| 37 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; log:  |
| 38 | `t` | busybox 1.37.0, no applet named on the line | probes:  |
| 39 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cached_game_ids.txt last-topup-attempt proxy.sqlite3  |
| 40 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log:  |
| 41 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log: 2026-10-25 00:32:35 index ran offline: the hash library did not come (index-pending); the library is listed once at the link's r |
| 42 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: ; log:  |
| 43 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log: ; stamp:  |
| 44 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes: 0; mark mtime 1792881156 vs 1792881156 -- a probe that reached nothing was counted as the half hour's attempt (#186 PL-04) |
| 45 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; mark mtime 1792881156 vs 1792881156 |
| 46 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes:  |
| 47 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; probes:  |
| 48 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; took 890s; stamp: ; smart: ; log:  -- the fifteen minutes were not one bound (#186 PL-28) |
| 49 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp: ; log:  |
| 50 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; out: ; stamp:  |
| 51 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; seen: ; left: cached_game_ids.txt last-topup-attempt proxy.sqlite3  |
| 52 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; seen: ; left: cached_game_ids.txt proxy.sqlite3  |
| 53 | `t` | `flock` (its consequence: rc 75 or a held lock) | disable rc 0; helper none gone: 1; disable said: logger -t raofflineproxy-ctl disable: a scan or top-up holds the lock and left no pid; wait |
| 54 | `t` | busybox 1.37.0, no applet named on the line | running: '' (was route=run at=<epoch>images before #258 PL-013) |
| 55 | `t` | busybox 1.37.0, no applet named on the line | disable rc 0; helper none gone: 1; running left: no; helper times: ; disable said:  (#258 PL-013) |
| 56 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; running left: route=scan at=1792884806 index=3 total=9 name=dead |
| 57 | `t` | busybox 1.37.0, no applet named on the line | running: '' |
| 58 | `t` | busybox 1.37.0, no applet named on the line | disable rc 0; helper none gone: 1; running left: no; helper times:  |
| 59 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; log:  (#186 PL-17) |
| 60 | `t` | `flock` (its consequence: rc 75 or a held lock) | rc 75; jobs: ; log:  -- the walk stopped at the same ten cached files (#186 PL-17) |
| 61 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-013 ctl: rc 75 after 0.02s; out: ; stamp: ; helper:  -- the INT trap waited for the foreground image pass |
| 62 | `x/D` | busybox 1.37.0, no applet named on the line | PL-013 ctl: the image pass started at ? and the run exited at 1792888479.713265914 -- 1792888479.71s |
| 63 | `x/D` | busybox 1.37.0, no applet named on the line | #308 gpt F-RA-11: disable rc 0 after 10.12s; helper none gone: 1; disable said: logger -t raofflineproxy-ctl disable: the running scan or to |
| 64 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055 / claude G-D-13: rc 75; stamp: ; marker: kept; log:  -- a listing that failed was stamped COMPLETED, or the marker went |
| 65 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; stamp: ; marker: kept |
| 66 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; probes: 0; log: ; marker: kept |
| 67 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; log: ; marker: kept |
| 68 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-055: rc 75; stamp: ; marker: kept |
| 69 | `x/D` | busybox 1.37.0, no applet named on the line | PL-055: the run exited 75; marker: kept |
| 70 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-059: rc 75; out: ; stamp:  -- the truncation was in the log alone |
| 71 | `x/D` | busybox 1.37.0, no applet named on the line | PL-059: second scan's jobs:  -- the same first ten files held the front of the walk |
| 72 | `x/D` | busybox 1.37.0, no applet named on the line | PL-059: 0 distinct files over two scans |
| 73 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-059: rc 75; out: ; stamp: ; cursor: none |
| 74 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; out: ; stamp:  -- the image pass's failure was dropped |
| 75 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; image pass run: 0 time(s); out:  -- the nothing-new branch exited before the pass |
| 76 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; image pass run: 0; stamp:  |
| 77 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; stamp:  |
| 78 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060: rc 75; stamp:  |
| 79 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp:  -- a crash read as the sweep working |
| 80 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 claude F-RA-06: rc 75; jobs:  -- the listing read the base file alone |
| 81 | `x/D` | busybox 1.37.0, no applet named on the line | #308 claude F-RA-06: jobs:  |
| 82 | `x/D` | busybox 1.37.0, no applet named on the line | #308 gpt F-RA-14: jobs:  -- a patch path alone read as a complete cache |
| 83 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 claude F-RA-10: rc 75; stamp:  -- the recently played pass's new game was not counted as added |
| 84 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-15: rc 75; jobs: ; stamp:  -- a cache operation was counted as a new game |
| 85 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-13: rc 75; probes: ; log:  -- PPSSPP's play was invisible to the question |
| 86 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-13: rc 75; probes:  |
| 87 | `x/D` | busybox 1.37.0, no applet named on the line | #308 gpt F-RA-10 ctl: the scan's image pass:  -- no bound but the helper's own |
| 88 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-10 ctl: images rc 75:  |
| 89 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | #308 gpt F-RA-10 ctl: refresh rc 75:  -- no bound but the helper's own |
| 90 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; out: ; stamp:  -- a badge the server does not have failed the scan |
| 91 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; requested:  -- an absent badge was asked for at every pass |
| 92 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; out:  |
| 93 | `x/D` | `flock` (its consequence: rc 75 or a held lock) | PL-060 follow-up: rc 75; requested:  |
| 94 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-004: rc 1; the archive lists:  -- a path with a space split into two that do not exist |
| 95 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-004: rc 1; archive:  |
| 96 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-004: rc 1; archives: 0; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- find's error went to /dev/null and a short archive |
| 97 | `y` | `flock` (named: *applet not found*) | #307 PL-036: rc 1; link: symlink; f1='file1'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR |
| 98 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-035: rc 1; archive: ; SECRET in:  |
| 99 | `y` | `flock` (named: *applet not found*) | #307 PL-035: rc 1; archive: ; screen: YOUR OWN BACKUP LIST IS EMPTY, SO THE STANDARD ONE WAS USED./flock: applet not found/[31mA SETTINGS B |
| 100 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-038: rc 1; archives: 0; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- it was staged and silently left out of the archive |
| 101 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-008: rc 1; members under the backup folder:  |
| 102 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-008: rc 1; members under it:  |
| 103 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-009: rc 1; f1='LIVE'; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- the failed copy read as an empty device and the rest |
| 104 | `y` | `flock` (named: *applet not found*) | #308 F-BR-17: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE |
| 105 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-19: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archive:  |
| 106 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-005: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: ; secret in an archive:  |
| 107 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: 0 -- the capital P passed |
| 108 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 109 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 110 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 111 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 112 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-006: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; log:  |
| 113 | `y` | `flock` (named: *applet not found*) | #307 PL-007: rc 1; x.cfg='ORIGINAL' f1='file1' new.cfg: gone; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY R |
| 114 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-007: the mark at extraction: '' |
| 115 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-039: rc 1; f1='LIVE'; why: 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- the extraction ran with no mark for the boot to fini |
| 116 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-010: rc 1; rclone.conf='MINE' id='this-device' |
| 117 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-010: rc 1; rclone.conf='MINE' id='this-device' |
| 118 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-010: rc 1; archive:  |
| 119 | `y` | busybox 1.37.0, no applet named on the line | #537: tar credential directory changed (rc 1) |
| 120 | `y` | busybox 1.37.0, no applet named on the line | #537: zip credential directory changed (rc 1) |
| 121 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-037: rc 1; es_settings.cfg after the restore: 'EDITED' |
| 122 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-077: rc 1/1; archives: 0 -- the second took the first one's name |
| 123 | `y` | `flock` (named: *applet not found*) | #308 F-BR-08: rc 1; f1='file1'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR IT TO FINISH, |
| 124 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-07: rc 1; root: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_00_00.zip ; archive/:  |
| 125 | `y` | `flock` (named: *applet not found*) | #308 F-BR-12: screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR IT TO FINISH, THEN TRY AGAIN.[ |
| 126 | `y` | `flock` (named: *applet not found*) | #308 F-BR-12: why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS AL |
| 127 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-13: rc 1; raofflineproxy/q: held; p7other/q: held |
| 128 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-13: rc 1; es_systems.cfg is a symlink |
| 129 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-14: why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1='LIVE'; snapshots: 0 |
| 130 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-16: rc 1; system.cfg in the archive: ''; directory entries: 0 |
| 131 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-09: rc 1; mktemp calls:  |
| 132 | `y` | busybox 1.37.0, no applet named on the line | #308 gpt F-BR-17: rc 1; left: /workspace/tmp/m6-t15/tmp/tmp.kEAvzHFy5G/p7/storage/.cache: . .. backuptool-staging.p7dead  /workspace/tmp/m6- |
| 133 | `y` | busybox 1.37.0, no applet named on the line | #308 F-BR-18: rc 1; archives at /storage/roms/backup: 0; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 134 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-01: rc 1; members: ; planted value in the archive: 0 |
| 135 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-01: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: 0 -- *.backup was not read |
| 136 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-03: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' -- the unanchored sk- refused a clean backup as a sign-in |
| 137 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-02: rc 1; f1='LIVE'; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 138 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-12: rc 1; members:  |
| 139 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-11: rc 1; kept: 0 of 4; root: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_00_00.zip ARCHIVED_ROCKNIX_BACKUP-20-01-02_00_00_00.zip ARC |
| 140 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-02: rc 1; mybackups: ; standard folder: 0 |
| 141 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-09: rc 1; test/seed='device copy' -- the seed list overwrote the archive's own file |
| 142 | `y` | busybox 1.37.0, no applet named on the line | #307 audit G-B-08: rc 1; f1='LIVE'; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; the folder holds:  |
| 143 | `y` | `flock` (its consequence: rc 75 or a held lock) | #307 audit G-B-15: IMG:find IMG:tar HOST:flock IMG:date IMG:mktemp  |
| 144 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-046: rc 1; archive: none; plant in it: 0; summary:  |
| 145 | `y` | busybox 1.37.0, no applet named on the line | #307 PL-077: rc 1/1; archives:  |
| 146 | `y` | `flock` (its consequence: rc 75 or a held lock) | #307 audit G-B-15: IMG:head HOST:flock IMG:find IMG:mkdir IMG:mv IMG:rm IMG:df IMG:date  |
| 147 | `y` | `flock` (its consequence: rc 75 or a held lock) | #308 F-PB-16: note: dump         NOT KEPT -- the cores folder could not be locked, and one dump at a time is what keeps the free-space floor |
| 148 | `y` | `flock` (its consequence: rc 75 or a held lock) | #308 F-PB-16: note: dump         NOT KEPT -- the cores folder could not be locked, and one dump at a time is what keeps the free-space floor |
| 149 | `y` | busybox 1.37.0, no applet named on the line | #308 F-PB-15: left: core.emulationstation.4000.4242.txt core.retroarch.1000.1.gz core.retroarch.1000.1.txt core.retroarch.2000.1.gz core.ret |
| 150 | `y` | busybox 1.37.0, no applet named on the line | #308 F-PB-15: notes: core.retroarch.6001.4242.txt core.retroarch.6002.4242.txt core.retroarch.6003.4242.txt core.retroarch.6004.4242.txt cor |
| 151 | `y` | `flock` (its consequence: rc 75 or a held lock) | #308 F-PB-20: note: dump         NOT KEPT -- the cores folder could not be locked, and one dump at a time is what keeps the free-space floor |
| 152 | `y` | busybox 1.37.0, no applet named on the line | #308 F-PB-21: the second note existed mid-way through the first dump: yes; left: core.emulationstation.8001.4242.txt core.retroarch.8000.424 |
| 153 | `y/A` | `flock` (named: *applet not found*) | N.nes: kept; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runn |
| 154 | `y/A` | `flock` (named: *applet not found*) | N.nes: kept; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runn |
| 155 | `y/A` | `flock` (named: *applet not found*) | rc 75; gb's sync: ; B.gb kept; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is a |
| 156 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | second apply rc 75; plan: still there |
| 157 | `y/A` | `flock` (named: *applet not found*) | bios on the device: (none?); out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alr |
| 158 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gb/A.gb missing, nes/N.nes missing; rc 75 |
| 159 | `y/A` | busybox 1.37.0, no applet named on the line | units:  |
| 160 | `y/A` | `flock` (named: *applet not found*) | A.gb in the cloud: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is al |
| 161 | `y/A` | `flock` (named: *applet not found*) | B.gb on the device: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is a |
| 162 | `y/A` | `flock` (named: *applet not found*) | A.srm missing, A.gb not sent; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud syn |
| 163 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; replaced root holds: ./2099_01_01-000000/gb/Z.srm ; the run's own folder was pruned because 2099_... sorts after it (F-CS-06 gpt, F-C |
| 164 | `y/A` | busybox 1.37.0, no applet named on the line | the 2099 folder is still there beside the run's own |
| 165 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; the folder holds: 2097_01_01-000000-QA-ROCKNIX_SETTINGS.tar.gz 2098_01_01-000000-QA-ROCKNIX_SETTINGS.tar.gz 2099_01_01-000000-QA-ROCK |
| 166 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; replaced holds: ./2099_01_01-000000/gb/Y.srm  (F-CS-06 gpt, prune_replaced_local) |
| 167 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | exit 75, stamp 'none', outcome 'Skipped: another cloud sync is already running. Try again when it's done.' -- [ overall -eq 0 ] skipped the  |
| 168 | `y/A` | busybox 1.37.0, no applet named on the line | the saves phase never reported 9; log:  |
| 169 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | exit 75, stamp 'none', outcome 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 170 | `y/A` | `flock` (named: *applet not found*) | units: ; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try ag |
| 171 | `y/A` | busybox 1.37.0, no applet named on the line | saves folder's state: removed; rc 1; retired:  |
| 172 | `y/A` | busybox 1.37.0, no applet named on the line | took 11s, rc 1, entry:  -- the commit ran beside another capture's (F-CS-14) |
| 173 | `y/A` | busybox 1.37.0, no applet named on the line | rc 1; the fresh seal was collected -- another capture's pending version (F-CS-14) -- or the capture ended before its GC |
| 174 | `y/A` | busybox 1.37.0, no applet named on the line | took 14s, rc 1 -- timedatectl ran unbounded on the synchronous game-exit path |
| 175 | `y/A` | busybox 1.37.0, no applet named on the line | manifest: missing; cache: capture-failures manifest-QA-deadbeef01.json.corrupt-1792888649 stage  |
| 176 | `y/A` | busybox 1.37.0, no applet named on the line | Game.state2's unit:  -- the source's entry was inherited wholesale because the bytes matched |
| 177 | `y/A` | `flock` (named: *applet not found*) | exit 75, stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already r |
| 178 | `y/A` | busybox 1.37.0, no applet named on the line | the ROM did not come down -- the case would pass for the wrong reason |
| 179 | `y/A` | `flock` (named: *applet not found*) | exit 75, stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already r |
| 180 | `y/A` | `flock` (named: *applet not found*) | rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try agai |
| 181 | `y/A` | `flock` (named: *applet not found*) | rc 75; bios.bin missing; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already |
| 182 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; units: ; argv:  |
| 183 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | took 1s (rc 75) -- sleep 2, sleep 2 and sleep 3 ran with nobody reading |
| 184 | `y/A` | busybox 1.37.0, no applet named on the line | summary:  |
| 185 | `y/A` | busybox 1.37.0, no applet named on the line | summary:  |
| 186 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | the planted partial is still there after a run with no record (rc 75) |
| 187 | `y/A` | busybox 1.37.0, no applet named on the line | the partial was swept -- the whole saves tree, the ROM library, was walked after a transfer that completed (F-CS-08) |
| 188 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | the partial survived a failed transfer's sweep (rc 75) |
| 189 | `y/A` | busybox 1.37.0, no applet named on the line | log:  -- the warning covered the settings folder only, and only under a condition that can no longer hold |
| 190 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | ran it: no; rc 75; why: ; outcome 'Skipped: another cloud sync is already running. Try again when it's done.' -- the conf was sourced with t |
| 191 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | ran it: no; rc 75; why: ; outcome 'Skipped: another cloud sync is already running. Try again when it's done.' -- the conf was sourced with t |
| 192 | `y/A` | busybox 1.37.0, no applet named on the line | size call: (none) |
| 193 | `y/A` | busybox 1.37.0, no applet named on the line | ls call: (none) |
| 194 | `y/A` | busybox 1.37.0, no applet named on the line | restored:  -- lexical order put the undated name last (F-CS-35) |
| 195 | `y/A` | busybox 1.37.0, no applet named on the line | restored:  |
| 196 | `y/A` | `flock` (named: *applet not found*) | rc 75; cloud A.srm: older; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alrea |
| 197 | `y/A` | busybox 1.37.0, no applet named on the line | saves-root:  |
| 198 | `y/A` | busybox 1.37.0, no applet named on the line | removed line ''; B.gb kept, sub/C.gb kept -- the totals were the plan's, counted before the delete ran (F-CS-26) |
| 199 | `y/A` | busybox 1.37.0, no applet named on the line | in the cloud:  -- .fla is missing from SAVE_EXCLUDES |
| 200 | `y/A` | busybox 1.37.0, no applet named on the line | plan 'n64/remove/1/4'; Game.fla kept -- a save the saves tier owns was removed as content (gpt F-CS-02) |
| 201 | `y/A` | busybox 1.37.0, no applet named on the line | scummvm README missing, bios/README.txt left, card.dat 'this device's own vmu' |
| 202 | `y/A` | busybox 1.37.0, no applet named on the line | scan disagrees (system:cloud-only/here-only): bios:1/0 dc:1/0 scummvm:2/0  -- the cloud-side count and the transfer describe different sets  |
| 203 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp 'none' -- a bare 69 reads SKIPPED, NO NETWORK on the row over a system that did arrive (F-CS-24) |
| 204 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; New.srm in the cloud: no; stamp 'none' |
| 205 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp 'none' |
| 206 | `y/A` | busybox 1.37.0, no applet named on the line | why:  |
| 207 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | G-D-01/02: rc 75; image pass run: 0 time(s); out:  -- COMPLETED over images nobody looked at |
| 208 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | G-D-01/02: rc 75; image pass run: 0 |
| 209 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-01: rc 75; stamp: ; image pass: 0 -- a pass that never ran read as done |
| 210 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | claude G-D-03: rc 75; the helper saw: ; 1792888735.26s; out:  |
| 211 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-06: rc 75; out:  -- a cursor write failure passed over |
| 212 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-06: rc 75; cursor before '', after '' |
| 213 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | gpt G-D-04: rc 75; jobs: ; stamp:  |
| 214 | `y/A` | busybox 1.37.0, no applet named on the line | claude G-D-08: jobs:  |
| 215 | `y/A` | busybox 1.37.0, no applet named on the line | gpt G-D-03: the run exited 75; marker: kept -- the older run acknowledged the newer notification |
| 216 | `y/A` | busybox 1.37.0, no applet named on the line | claude G-D-10: 2026-10-25 00:39:08 index ran offline: the hash library did not come (index-pending); the library is listed once at the link' |
| 217 | `y/A` | `flock` (named: *applet not found*) | ran it: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runni |
| 218 | `y/A` | `flock` (named: *applet not found*) | rc 75; game1.srm missing, victim home; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud s |
| 219 | `y/A` | `flock` (named: *applet not found*) | rc 75; game1.srm missing, victim left; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud s |
| 220 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; why: ; B.gb kept |
| 221 | `y/A` | `flock` (named: *applet not found*) | preview rc 0, apply rc 75; units: ; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync |
| 222 | `y/A` | `flock` (named: *applet not found*) | rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/flock: applet not found/flock: applet not found/Skipped: |
| 223 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | outcome line 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 224 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; outcome 'Skipped: another cloud sync is already running. Try again when it's done.' |
| 225 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cloud:  |
| 226 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cloud:  |
| 227 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; cloud:  |
| 228 | `y/A` | `flock` (named: *applet not found*) | rc 75; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try again whe |
| 229 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | restore rc 75; scan row 'scummvm/10/1/0/1/0/10/0' (name/cloud/sup/device/...) -- the list below title/ was counted as a ROM |
| 230 | `y/A` | busybox 1.37.0, no applet named on the line | list on the device: no; scan row 'scummvm/51/1/0/0/0/0/0' |
| 231 | `y/A` | busybox 1.37.0, no applet named on the line | rc 1; entries:  |
| 232 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; N.nes missing; stamp '' |
| 233 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; N.nes in the cloud no; stamp '' |
| 234 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; stamp '' -- a unit that moved nothing counted as progress |
| 235 | `y/A` | `flock` (named: *applet not found*) | rc 75; New.srm in the cloud: no; stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another |
| 236 | `y/A` | `flock` (named: *applet not found*) | rc 75; stamp 'none'; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already run |
| 237 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | 1s, rc 75; why:  |
| 238 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | 1s, rc 75; why:  |
| 239 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; screen: ; log:  |
| 240 | `y/A` | `flock` (named: *applet not found*) | ran it: no; conf restored; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync i |
| 241 | `y/A` | `flock` (named: *applet not found*) | ran it: no; conf restored; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync i |
| 242 | `y/A` | `flock` (named: *applet not found*) | rc 75; RCLONEOPTS lines 2; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alrea |
| 243 | `y/A` | busybox 1.37.0, no applet named on the line | the partial is still there: the tree was recorded clean across a content restore that was cut |
| 244 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; in the cloud:  |
| 245 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; the record is gone -- every saves restore after a content restore would walk the library |
| 246 | `y/A` | `flock` (its consequence: rc 75 or a held lock) | rc 75; the reader gave "Skipped: another cloud sync is already running. Try again when it's done." "Skipped: another cloud sync is already r |
| 247 | `y/A` | busybox 1.37.0, no applet named on the line | #307 audit G-B-15: rc 1; left: .collect.p7dead  |
| 248 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-01 / claude G2-D-08: the walk's gb jobs were '' (rc 75) -- expected h.gb and l.gb; a head's partial or nested GameId made the wrong |
| 249 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  -- a failed measurement replaced by the cache count |
| 250 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp: ; log:  |
| 251 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  |
| 252 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  |
| 253 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-02 / S-24: rc 75; stamp:  |
| 254 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | gpt G2-D-03: top-up rc 75; the writer never ran: the removal was not reached; marker: '1792888830 2760104 16439' (listed for '1792888830 276 |
| 255 | `y/CF` | busybox 1.37.0, no applet named on the line | gpt G2-D-03: 2026-10-25 00:40:35 index ran offline: the hash library did not come (index-pending); the library is listed once at the link's  |
| 256 | `y/CF` | `flock` (named: *applet not found*) | PL-002: cloud_backup: ran it: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud |
| 257 | `y/CF` | `flock` (named: *applet not found*) | PL-002: cloud_restore: ran it: no; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another clou |
| 258 | `y/CF` | `flock` (named: *applet not found*) | PL-015: cloud_backup: rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alr |
| 259 | `y/CF` | `flock` (named: *applet not found*) | PL-015: cloud_restore: rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is al |
| 260 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-015: rc 75; log:  |
| 261 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-015: rc 75; the copy's bound:  -- the escaped quote read as the value's end and the shipped bound stood in |
| 262 | `y/CF` | `flock` (named: *applet not found*) | G2-A-03 (gpt): rc 75; in the cloud: ; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sy |
| 263 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_backup, cp fails: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/flock: app |
| 264 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_backup, cp says it worked: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/f |
| 265 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_restore, cp fails: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/flock: ap |
| 266 | `y/CF` | `flock` (named: *applet not found*) | PL-004: cloud_restore, cp says it worked: conf intact; cleanup ran: no; left: ; rc 75; out: flock: applet not found/flock: applet not found/ |
| 267 | `y/CF` | `flock` (named: *applet not found*) | G2-A-04 (gpt): plan written: yes; B.gb kept; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: an |
| 268 | `y/CF` | `flock` (named: *applet not found*) | G2-A-04 (gpt): B.gb kept; plan left; rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cl |
| 269 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | G2-A-06 (claude): 16 stat calls with the stage small, 16 with 301 more seals, rc 1; the most frequent:  6 -c %s %Y /storage/roms/gb/Game.srm |
| 270 | `y/CF` | busybox 1.37.0, no applet named on the line | G2-A-06 (claude): old unclaimed KEPT; fresh kept; claimed none MISSING |
| 271 | `y/CF` | busybox 1.37.0, no applet named on the line | PL-034: read-only saves folder: rc 1; entries: ; out:  |
| 272 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-034: past the bound: rc 1 after 10s; manifest none; failures: 1792888930 lock-busy gb:Game |
| 273 | `y/CF` | `flock` (its consequence: rc 75 or a held lock) | PL-034: within the bound: rc 1 after 10s; manifest none; failures: 1792888941 lock-busy gb:Game |
| 274 | `z` | busybox 1.37.0, no applet named on the line | PL-003: rc 1; the conf's command ran: no; mybk: 0 archive(s) -- backuptool sourced the file |
| 275 | `z` | busybox 1.37.0, no applet named on the line | PL-003: rc 1; ran: no; standard folder: 0; mybk: none; log: 1 |
| 276 | `z` | busybox 1.37.0, no applet named on the line | PL-003: rc 1; first: 0; second: 0 -- the source took the last |
| 277 | `z` | busybox 1.37.0, no applet named on the line | PL-003: single-quoted rc 1, 0 archive(s); bare rc 1, 0 |
| 278 | `z` | `flock` (named: *applet not found*) | PL-006 (KEEP's mktemp): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not fo |
| 279 | `z` | `flock` (named: *applet not found*) | PL-006 (KEEP's appends): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not f |
| 280 | `z` | `flock` (named: *applet not found*) | PL-006 (NEWLIST): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[ |
| 281 | `z` | `flock` (named: *applet not found*) | PL-006 (the final list): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not f |
| 282 | `z` | `flock` (named: *applet not found*) | PL-006 (MEMBERS): rc 1; f1='LIVE'; new.cfg absent; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; screen: flock: applet not found/[ |
| 283 | `z` | `flock` (named: *applet not found*) | PL-006 (empty selection): rc 1; f1=''; screen: flock: applet not found/[31mA SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING. WAIT FOR IT TO  |
| 284 | `z` | busybox 1.37.0, no applet named on the line | PL-006 (held back): rc 1; archives 0; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 285 | `z` | `flock` (named: *applet not found*) | PL-007 (tar): rc 1; mark's first line after the extraction ''; copy's f1 ''; f1 now 'LIVE'; screen: flock: applet not found/[31mA SETTINGS  |
| 286 | `z` | `flock` (named: *applet not found*) | PL-007 (zip): rc 1; mark's first line after the extraction ''; copy's f1 ''; f1 now 'LIVE'; screen: flock: applet not found/[31mA SETTINGS  |
| 287 | `z` | busybox 1.37.0, no applet named on the line | PL-007 (backup): rc 1; archive holds:  |
| 288 | `z` | busybox 1.37.0, no applet named on the line | PL-008: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; archives: 0 -- the value class could not take the space after the quote |
| 289 | `z` | busybox 1.37.0, no applet named on the line | PL-008: rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING' |
| 290 | `z` | busybox 1.37.0, no applet named on the line | G2-B-02: the mark at extraction: '' |
| 291 | `z` | busybox 1.37.0, no applet named on the line | PL-017: rc 1; upstream-era: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_00_00.zip ; contents: ARCHIVE-A ; root: ARCHIVED_ROCKNIX_BACKUP-20-01-01_00_ |
| 292 | `z` | busybox 1.37.0, no applet named on the line | PL-022 (stored, damaged): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1 'LIVE'; d.cfg absent -- the corrupted bytes were r |
| 293 | `z` | busybox 1.37.0, no applet named on the line | PL-022 (deflated, damaged): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1 'LIVE' |
| 294 | `z` | busybox 1.37.0, no applet named on the line | PL-022 (healthy): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; f1 'LIVE'; brackets '' |
| 295 | `z` | busybox 1.37.0, no applet named on the line | PL-028 (tar): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; outside: ; f1 'LIVE'; copies: 0 |
| 296 | `z` | busybox 1.37.0, no applet named on the line | PL-028 (zip): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; outside: ; f1 'LIVE'; copies: 0 |
| 297 | `z` | busybox 1.37.0, no applet named on the line | PL-028 (..): rc 1; why 'A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING'; outside: ; f1 'LIVE'; copies: 0 |
| 298 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 299 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 300 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 301 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --update: no copy command was issued (rc 75); the assertions below are vacuous |
| 302 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_restore --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 303 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_restore --yes --method=copy --update --saves-only --automatic: no copy command was issued (rc 75); the assertions below are vacuous |
| 304 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 305 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 306 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_restore --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 307 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 308 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only --recent: no copy command was issued (rc 75); the assertions below are vacuous |
| 309 | `z/S315` | `flock` (its consequence: rc 75 or a held lock) | cloud_backup --yes --saves-only: no copy command was issued (rc 75); the assertions below are vacuous |
| 310 | `ad` | `flock` (named: *applet not found*) | rc 75; /GAMES in the cloud: no; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is  |
| 311 | `ad` | `flock` (named: *applet not found*) | rc 75; /GAMES: no; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already runni |
| 312 | `ad` | `flock` (named: *applet not found*) | rc 75; A.srm missing; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already ru |
| 313 | `ad` | `flock` (named: *applet not found*) | rc 75; out: flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is already running. Try agai |
| 314 | `af` | `flock` (named: *applet not found*) | cloud_content_backup: rc 75, 2s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alre |
| 315 | `af` | busybox 1.37.0, no applet named on the line | cloud_content_backup: stamp/second-copy/cleanup mismatch |
| 316 | `af` | `flock` (named: *applet not found*) | cloud_content_backup: progressing run rc 75, 1s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cl |
| 317 | `af` | `flock` (named: *applet not found*) | cloud_content_restore: rc 75, 1s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another cloud sync is alr |
| 318 | `af` | busybox 1.37.0, no applet named on the line | cloud_content_restore: stamp/second-copy/cleanup mismatch |
| 319 | `af` | `flock` (named: *applet not found*) | cloud_content_restore: progressing run rc 75, 1s; flock: applet not found/flock: applet not found/flock: applet not found/Skipped: another c |

## Proofs

| Proof | What it shows | Proved |
| --- | --- | --- |
| P1 | the image's busybox run is the tree's baseline: 1,313 / 0 / 0, rc 0, from the worktree | proved: tool-run |
| P2 | the coordinator's ten image-run FAILs are the fixture's git-history dependency (an export without `.git`), not the tree's: the same bytes from the worktree pass all ten | proved: tool-run |
| P3 | all 319 host-busybox flips are the busybox's: `bbhost` 319 with the image's rclone, `rchost` 0 with the host's | proved: tool-run |
| P4 | none of the twelve `--old` recipes reaches a verdict: two refs dead, ten stopped at `s` or `x` | proved: tool-run |
| P5 | `70b6c70ca7`'s promised `012` FAILs do not fire: its `t` stops at the patches, with 0 lines naming `012` | proved: tool-run |


## The first reader's 03-retrospective.md (whole)

# Retrospective: M6.P2 T15, the last-good scripts test (#662)

Read at `8ebaf8daad`; the runs are `02` § The runs. The lens is brittleness.

## 3.1 What the suite was for

It was written on 2026-09-10 (`52c4249759`) as *a device-less check that the scripts keep the last known good state when they are killed mid-write* (D-CLOUD-078, #105, the header `:5-6`). The same day, blindspot 34 gave it its second purpose: run every busybox applet a script calls through the image's busybox, because GNU `tr` had passed a check that busybox `tr` failed on every device (`:152-160`).

In 408 commits it grew from those two claims to 34 sections. Three audits' punch items became cases: #307/#308's streams in `x` and `y`, the fix round in `y` and `z`, and the audit of the fixes in `z`'s `S3F`. Section `y` alone is 5,386 lines, and `x` and `y` together hold 61 % of the 1,313 checks.

## 3.2 What drifted

- **The busybox it exists to run.** No M6 worktree has a build root that `image_tool_source`'s three globs reach (`:392-394`: `${ROOT}/../*`, `${ROOT}.worktrees/*`, `${ROOT}/build.*`). The M7 roots live under `/workspace/repos/rocknix.worktrees/`, which none of them names. So since M6's worktrees were cut, every run but those given `QA_SYSTEM_ROOT` has fallen to `:400`'s `command -v busybox || true`, the host's 1.37.0. It judged the host: 319 checks FAIL, and 61 of their lines say `flock: applet not found`. The banner at `:426` names the copy; nothing in the verdict does. The founding lesson was undone by its own fallback.
- **The rclone stream A claims.** *The cloud scripts against the image's rclone* (`:8906`) take the host's `/usr/bin/rclone` by the same fallback: v1.60.1-DEV against the recipe's 1.75.2. Measured: no verdict changes (`rchost`, 1,313 / 0). The version is printed (`:8914`) and never asserted.
- **The `--old` controls.**
  - Two of the header's twelve refs no longer exist (`0f7785e6ed`, `d79281066c`).
  - The other ten stop at `s` or `x`, because `src_of` exits 2 for the whole run at the first script a ref predates.
  - The newest sections, `x` to `ah`, were added after every ref the header names, so no recipe reaches them.
  - One recipe (`70b6c70ca7`) fires on patch application, not on the `012` checks it promises.
  - The header was not updated as sections were added; its claims stop at `w`.

## 3.3 What none of them noticed

- **The record's last PASS under the image's busybox is 2026-10-06** (qa-18). Every run since from an M6 worktree FAILed 319 checks. #1015 (T12) filed them as *the last-good scripts test fails 319 checks on this host wherever its scratch is (backuptool's staging first; host tools suspected)*, the suspicion right and unproven, until this slice's attribution runs settled it: the busybox, by `bbhost` (319) and `rchost` (0). Nothing in a run's own verdict could have said so.
- **The coordinator's ten FAILs at the hash** were an export's: no `.git`, so the fixtures that read `417dcd8610` from git came up empty. Each was caught only by a vacuity detector downstream of a read that fails open (`f1_tree_at` `:3205-3215`; `:4271`). The read itself says nothing.
- **A host without the sources cache** would turn section `D`'s 33 busybox FAILs into 21 SKIPs (exit 3, read as SKIP by `vm-qa:148`), because they sit behind section `t`'s client tarball (`DT_OK`, `:6649`).

## 3.4 What the record says about catches

- **The header and the comments name what each section caught:** #105 to #546, the streams' PL and G items, and blindspot 34.
- **The `--old` recipes are the positives.** Before each stops, the promised FAILs fire in `a` to `v`, with the exceptions in `02` § The runs.
- **The later groups carry their own positive refs in comments,** unnamed in the header: `417dcd8610` (`:8905`, `:3194`, `:6636`), `f3d19dc8fb` (`:11068`, `:12089`, `:12321`, `:12603`, `:13172`), `320d2b2bea` (`:13586`), `286759eb6d` (`:13663`) and `a06539d8ec` (`:8593`). None of them was run here. Each would stop where `src_of` meets a script it predates.

## 3.5 The seams

| Seam | What crosses it | What breaks it |
| --- | --- | --- |
| this file and `tools/vm-qa`'s `scripts` suite | the exit code: `vm-qa:148` reads 3 as SKIP and any other non-zero as FAIL | a `NOT APPLICABLE` group exits 0 and reads PASS. A run on the host's busybox reads `FAIL (1)` with nothing to say it judged the host. An `--old` run is never `vm-qa`'s |
| this file and T14's four tools | `--cloud-layout` and `ae` (`rasteratops-cloud-layout-test`), and `ag`/`ah` (`settings-modes-test`, `melonds-upgrade-test` with `--busybox "${BB_HOST}"`) | T14's S8 refuses a busybox that is not a build root's, and `BB_HOST` is the run's copy, so `ag` and `ah` FAIL on every host until #997's two flags land here (S1). The connections fixture's `--config` order was fixed by T14 for this file's shims (#999) |
| this file and the scripts it proves | `src_of`'s copy of each script, from the tree or `BASE_REF` | a script added after a ref ends every `--old` run at its section. A script moved to another path, or a function renamed, empties a lifted fixture, and some checks then pass on nothing (`04` § Q3) |
| this file and the busybox source | `image_tool_source`: `QA_SYSTEM_ROOT`, then three globs, then the host's | no glob reaches the M7 roots, and the host fallback is silent. No busybox at all means GNU tools, with no banner |
| this file and git history | the fixtures that read `417dcd8610` and `73b20caf86` (`F1.`, `F1r.`, `C.`) | an export or a shallow clone: the read fails open, and only a vacuity detector catches it |


## The first reader's 04-analysis.md (whole)

# Analysis: M6.P2 T15, the last-good scripts test (#662)

Read at `8ebaf8daad`; the branch `HEAD` at stage A, `60d7f6a5b2`, does not differ on the file. The lens is brittleness: what the suite depends on that is not the thing it proves, and what happens when each is absent. The runs are `02` § The runs. The section reads were made by three read-only agents and re-derived here: each lead marked *re-derived* was read from its lines by the lane, and the rest are cited by line for the seat and stage D.

## Executive summary

- **At the hash, the suite passes on the tree:** 1,313 PASS, 0 FAIL, 0 SKIP under the M7 image's BusyBox 1.36.1, given through `QA_SYSTEM_ROOT`. That is the tree's baseline (the coordinator, 00:36). The coordinator's ten FAILs at the hash were its export's missing `.git`.
- **From any M6 worktree without `QA_SYSTEM_ROOT`, it judges the host instead, and says so only in a banner.** It takes the host's BusyBox 1.37.0 and rclone 1.60.1-DEV. 319 checks FAIL, every one the busybox's (`bbhost` 319, `rchost` 0); `flock`, missing from the host's busybox, is the only refusal named. A host with no busybox at all would run on GNU tools with no banner, which is blindspot 34, silently. **F-01, High.**
- **Its failing controls do not run.** None of the header's twelve `--old` recipes reaches a verdict:
  - two refs are gone;
  - the other ten stop when `src_of` meets a script the ref predates (`s` or `x`);
  - one fires for a reason other than the one it names;
  - the twenty sections from `s` (or `x`) to `ah` have no control that runs (F-04 to F-06).
- **Many of its checks can pass without proving anything.** The common shape is *rc non-zero, and nothing written*, which a script that never ran satisfies (F-10). With it come a `;`-chained `check` (F-11), skips and silent omissions behind a missing download (F-09), and a fourth verdict word, `NOT APPLICABLE`, that exits 0 (F-08).
- **Its two calls into T14's writer tests are now refused** (F-07, #997's two flags, stream S1).

## Acceptance-criteria scorecard

#662's 19 criteria at the end of stage B. The final state is the hand-back's.

| # | Criterion (short) | State | Artifact |
| --- | --- | --- | --- |
| 1 | the folder holds 00 to 05 | 00 to 04 written; 05 at stage D | this folder |
| 2 | the lint prints PASS | pre-issue at stage C | `tools/lint-audit-artifacts` |
| 3 | the review plan, the seat's provenance and the packet's scan | stage C | `second-opinions/` |
| 4 | the punch-list issue at its outcomes | stage D onward | the audit issue |
| 5 | `reviewed-at` / `fixed-at` | `reviewed-at: 60d7f6a5b2` | #662's body at hand-back |
| 6 | `01` § Scope | done | `01` |
| 7 | 34 coverage rows | done (34) | `02` § Coverage |
| 8 | both runs; the busybox-dependent checks with their applet | done: 319, with `flock` named where shown | `02` |
| 9 | the twelve `--old` recipes | done: all exit 2, each stop named | `02` § The runs |
| 10 | no forbidden action; `SIGINT ignored=0` on every run | holds; one write under `/tmp` made and removed (`00`) | `00` |
| 11 | Q6's 34-row table and the split proposal | done below | § Q6 |
| 12 | Q3 by section; the eight `\|\| true`; `check $?`; `skip()`; NOT APPLICABLE; no-busybox; the ten | done below | § Q3 |
| 13 | Q7 | done below | § Q7 |
| 14 | Q5 by section | done below | § Q5 |
| 15 | `proved:` cells | P1 to P5 in `02` | `02` § Proofs |
| 16 | `question:`; `box-check`; no `tools/` change before a stream; the call sites' flags | no `tools/` change; the rest at D and E | the branch |
| 17 | the fixed tip refuses or marks a host-busybox run | stage E | — |
| 18 | the retro | stage G | — |
| 19 | the checkers; `vm-qa:148`'s rule stated | `vm-qa:148` stated in `01` and § Q2; the checkers at hand-back | `01` |

## Risk assessment

- **The suite's verdict is only as good as its busybox source, and that source is chosen silently.** A worktree with no build root is every M6 worktree today. There, `vm-qa`'s `scripts` row reads `FAIL (1)` over 319 FAILs about the host. Worse, a host whose own busybox happened to carry `flock` would pass the host's applets as the image's, under a `PASSED` verdict. Blindspot 34 is exactly a check passed under the wrong tools.
- **The failing controls are the suite's evidence that its guards fire, and they have decayed.** Sections `x` to `ah` (933 of 1,313 checks, including the three audits' streams) have no runnable positive at all.
- **Absence is often indistinguishable from success** where a check asserts *nothing was written*. A sandbox that cannot start, a script that is not lifted, or a fixture that never ran each passes such checks. The paired positive usually fails beside it, but not always (F-10's list).
- **What this does not risk:** no device, no cloud and no player data. The suite runs on the host against fixtures, and its sandboxes bind the fixture's directories only, but they **share the host's network and the caller's environment** (F-16).

## Coverage boundary

- **Read:** the one path at `8ebaf8daad` (14,238 lines): the harness `:1-430` whole; sections `a`, `b`, the sandbox helpers and the `F1.` history helpers by the lane; every section by the three agents; their leads re-derived where marked.
- **Run:**
  - the suite fourteen times at stage A (the image's busybox, the host's, and the twelve `--old` recipes);
  - three more (`bbhost`, `rchost`, and the timed run);
  - `--help` and `--nosuch`.
- **Not run:** the positive refs the later groups name in comments (`417dcd8610`, `f3d19dc8fb`, `320d2b2bea`, `286759eb6d`, `a06539d8ec`). Each would stop where `src_of` meets a script it predates. Not run either: `--payload-tests`-style host gaps such as a host without `jq` or `node`, read from the code only.
- **Not touched:** the scripts it proves, T14's four tools (read at `7c1d729b57` for the call sites) and `tools/vm-qa`.

## Findings (Phase 4)

| ID | Finding | Where | Severity | Q |
| --- | --- | --- | --- | --- |
| F-01 | `image_tool_source` falls back to the host's busybox silently (`command -v busybox \|\| true`), and to none at all: no copy, no wrappers, no banner, GNU tools. The verdict never says whose applets judged the scripts. From every M6 worktree it takes the host's 1.37.0, and 319 checks FAIL (`flock`). #1015's root cause | `:381-401`, `:400`, `:416-426` | High | Q2 |
| F-02 | The rclone stream A runs is chosen the same way (`:8908`): the host's 1.60.1-DEV silently. Its version is printed (`:8914`) and never asserted, and no case depends on it (`rchost`: 1,313 / 0 with 1.60.1) | `:8906-8914` | Medium | Q4 |
| F-03 | The history read fails open. `f1_tree_at`'s `git ls-tree ... 2>/dev/null \| while ...` with its `exit 2` inside the pipeline subshell, and `:4271`'s `git show 417dcd8610:... 2>/dev/null`, make an empty fixture without a word, caught only by a downstream vacuity detector (the coordinator's ten). Ruled a bug, 00:36 | `:3205-3215`, `:4271` | Medium | Q2 |
| F-04 | Two `--old` refs are dead: `0f7785e6ed` (q) and `d79281066c` (p's pending and flushed) exist nowhere in the repository. Likely meant: `717bc04449` (`1a5c066623^`) and `51e2acece6` (`67a89cb623^`) | `:185`, `:191` | Medium | Q3 |
| F-05 | Under `--old`, `src_of` exits 2 for the whole run at the first script a ref predates. No recipe reaches a verdict, and sections `s` (or `x`) to `ah` never run as controls | `:320-325` | Medium | Q3 |
| F-06 | `70b6c70ca7`'s control fires on patch application, not on its `012` checks. Section `t` takes the client pin from the working tree (`:2051`) and the patches from `BASE_REF`, which no longer apply | `:2051-2086`, `:219-225` | Medium | Q3 |
| F-07 | `ag` and `ah` call T14's writer tests with `--busybox "${BB_HOST}"`, the run's copy, which T14's S8 contract refuses (CANNOT, exit 2) without `--busybox-from` or `--unverified-busybox`. They FAIL on every host until S1 | `:14224`, `:14231` | High | Q3 |
| F-08 | A fourth verdict word, `NOT APPLICABLE` (the retired migration group, #508), is reported, and the run then exits 0 `PASSED`: a group that did not run passes, and `vm-qa:148` reads it as PASS | `:4558`, `:14235-14238` | Medium | Q3 |
| F-09 | **Missing downloads hide or drop checks, by three rules.** (1) One SKIP stands in for every webkit patch (`:6491`), where F2-4 (`:4008`) and F2-6 (`:4297`) count the same absence as a FAIL. (2) Section `D`'s 21 SKIPs and seven `if DT_OK` blocks with no `else` (A's D22-D31) depend on `t`'s client tarball, so on a host without the cache `D`'s 33 `flock` FAILs would read as SKIPs (exit 3). (3) `F1r-d` (no `qemu-img`) and the G-B-15 banner probes (no busybox) vanish with no SKIP | `:6491`, `:6649`, `:10128-10358`, `:11180`, `:8777-8811` | Medium | Q3 |
| F-10 | *rc non-zero, and nothing written* passes when the script never ran: a sandbox that cannot start (rc 1 from `bwrap`, or 127 hidden by `2>/dev/null`), a missing applet path, or an unlifted function. 30-odd sites (§ Q3) | § Q3 | Medium | Q3 |
| F-11 | `v`'s START NEW GAME check chains three runs with `;` and `&&`, so `check $?` reads only the last `is`, against output an earlier failure may have left | `:3051` | Medium | Q3 |
| F-12 | `check` called with two arguments: a FAIL aborts the run under `set -u` with no FAIL counted (historical refs only) | `:13826` | Low | Q2 |
| F-13 | `q`'s *the boot pass ran (rc 0)* reads `wait`'s status, and its *still there* checks test markers the fixture made | `:1803-1846` | Low | Q3 |
| F-14 | `t`'s PASS text says *each compiled*, while `py_compile`'s failure only changes that text | `:2086` | Low | Q7 |
| F-15 | `! tar ... \| grep -q` with no `pipefail` passes on a missing archive or member; each has a paired existence check | `:548`, `:803`, `:1036-1047` | Low | Q2 |
| F-16 | `sa_run`'s sandbox has no `--clearenv` and no `--unshare-net`: the caller's environment (`RCLONE_*`, `BASH_ENV`) and the host network reach every script it runs (150 calls). Four other invocations do unshare the network | `:9010-9022` | Medium | Q2 |
| F-17 | Some checks ignore `--old` and grade the working tree among the expected FAILs: `g` `:845-851` (re-derived), `h`'s fallback `:887-891`, `i` `:903-928`, `t` `:2427`, `C7` `:6506` | as named | Low | Q3 |
| F-18 | **The descriptions drift from the code.** `--help`: *"with the image's busybox"*. The header's claims stop at `w`, and its recipes at `v`. `:264` and `:266` advise `setsid -f`, which keeps an ignored SIGINT. The index row's Detail-in rule never describes the file | `:239-250`, `:7-226`, `:264-266` | Low | Q7 |
| F-19 | S3F's canaries write to the host's `/tmp/s3f-*` if the guard fails, and a stale one from another run FAILs the check | `:13672-13678` | Low | Q2 |
| F-20 | `y4`'s G-B-15 banner probes accept any `BusyBox` banner, so the host's 1.37.0 passes as *the image's*; and they are silently absent with no busybox | `:8777-8779`, `:8809-8811` | Medium | Q3 |
| F-21 | `z`'s PL-022 measures *the image's busybox unzip* with whatever busybox ran; its skip tests only `-n BB` | `:13400-13424` | Low | Q3 |

## Finding Verification (Phase 4.5)

Each Medium or above, by the artifact that decided it:

- **F-01:** run 2 and `bbhost` (319 FAIL, `diff` 0 against each other), `rchost` (0), and `:400` read. *Re-derived.*
- **F-02:** `rchost`'s 1,313 / 0 with `rclone v1.60.1-DEV` (its own `rclone:` banner line), and `:8914` read. *Re-derived.*
- **F-03:** the coordinator's export run (no `.git`; its `run-image.out` lines 428-431, 524-525 and 1150-1156) against this worktree's run (all ten pass), and `:3205-3215` and `:4271` read. *Re-derived.*
- **F-04:** `git cat-file -t` on both refs (*Not a valid object name*), `git branch -a --contains` empty, and `git log -S` naming the commits that wrote them. *Re-derived.*
- **F-05:** the twelve `--old` outputs, each ending `cannot read <script> at <ref>`, rc 2. *Re-derived.*
- **F-06:** `old-70b6c70ca7.out`'s `t`: 0 lines naming `012` against 5 PASS in the baseline, and four FAILs *patch does not apply to the pinned client*. *Re-derived.* The working-tree pin at `:2051` is the agent's reading, not re-derived (inference).
- **F-07:** T14's `settings-modes-test` at `7c1d729b57` refuses a path not under a build root's `image/system/`, and `:14224` and `:14231` pass `${BB_HOST}` (`${TMP}/busybox`). T14's own run on 2026-10-24 showed both refused. *Re-derived.*
- **F-08:** run 1's `1 HISTORICAL FEATURE GROUP(S) NOT APPLICABLE -- no checks counted as PASS` then `PASSED`, rc 0. *Re-derived.*
- **F-09:** `:6488-6492` read (re-derived); `:6649` and D's skips from the agent's table; `:4008` and `:4297` from the agent.
- **F-10:** the shape read at `:548` and `:8583` (re-derived); the other sites cited by line from the agents, for the seat.
- **F-11:** `:3051` read. *Re-derived.*
- **F-16:** `:9010-9022` read. *Re-derived.*
- **F-20:** from the agent's reading of `:8777-8811` (not re-derived; cited for the seat).

## Second opinion (Phase 4.6)

Not yet run: stage C. One GPT-6 Astra seat at `max` through the Facilitator: a probe, then one refutation over one packet of excerpts, scanned before it is sent. The plan is in `second-opinions/review-plan.json` when written.

## Renovation face

### Q1 Modernize

- **The busybox roots it searches** (`:392-394`) name three distro layouts under `${ROOT}/..`, `${ROOT}.worktrees` and `${ROOT}`. None reaches `/workspace/repos/rocknix.worktrees/`, where the M7 roots are. `rocknix.worktrees` and `/workspace/repos/rocknix` appear 0 times in the file.
- **`$HOME`** appears twice, both as string fixtures (`:4673`, `:11376`), never read.
- **Absolute host binaries:** `/usr/bin/grep` 4, `busybox` 4, `tar` 3, `mv` 3, `sleep` 2, `rm` 2, `python3` 2, `env` 2, `date` 2, `sed`, `rsync`, `find` 1 each. Only `bwrap` and `setsid` are checked up front (`:286-287`), and `rsync`, `python3`, `jq`, `node`, `gcc` and `qemu-img` are found by failure.
- **The `BASE_REF` default `1d1503180d` and the twelve recipes** predate every section from `s` on (F-04, F-05).
- **`flock` is not in the top-level wrapper list** (`:422`: `sed mv cp tr head wc cut awk stat chmod cat`). It is shimmed in `n` (`:1484`), `t` (`:2097`), `y1` (`:7811`) and stream A (`:8983`), and called on the host directly at `:2345` and `:6765`, where it is util-linux's.

### Q2 Standards

- **`set -u` only** (`:270`): no `-e`, no `pipefail`. The pipeline-first-stage failures that matter are F-03 (`ls-tree ... 2>/dev/null \| while`) and F-15 (`tar ... \| grep -q`).
- **The eight `|| true` sites:**
  - `:400`: the fallback, F-01, a finding.
  - `:1102`: a comment (#151 PL-14's history).
  - `:2086`: `py_compile ... || true` feeds only the PASS text, F-14.
  - `:4376`: a comment.
  - `:9633`: inside a FAIL message's text.
  - `:10409`: sound. `grep -c` prints 0, an error leaves `DLEFT` empty, `-eq` then errors, and the check FAILs.
  - `:13871` and `:13908`: sound against a missing file (`src_of` guarantees it); a call through a variable verb evades the regex (inference).
- **`check $?` after a compound test:** `[ ] && [ ] && grep` returns the first failing status, which is sound throughout. The exception is the `;`-joined chain at `:3051` (F-11).
- **The SIGINT refusal** (`:265-268`) fails closed, exit 2. Its advice (`setsid -f`) is wrong (F-18). `vm-qa:158`'s launcher is the right way in.
- **Exit codes:** 0 PASS (including after `NOT APPLICABLE`, F-08), 1 FAIL, 2 cannot run, 3 SKIP. `vm-qa:148` reads 3 as SKIP and any other non-zero as FAIL.
- **The sandboxes** share the host's network and the caller's environment (F-16).

### Q3 Bugs: the pass-without-proving hunt, section by section

Each line read, with a constructed input that would pass wrongly, or the statement that none was found:

- **`a`:** with no busybox, `bbin` is empty and the text checks run on GNU `tr`, blindspot 34's exact case (F-01). Constructed: a host with no busybox and a `chksysconfig` whose text test only GNU `tr` passes. The `[ ] && [ ]` chains are sound.
- **`b`:** `:548` `! tar -xzOf "${first}" ... 2>/dev/null | grep -q SECRET` passes on a missing archive; `:547` catches it (F-15). `:573` and `:594` pass when the run never started (F-10).
- **`c`:** `:621` counts exact spellings, so a `set_setting` that appends with `printf >>` passes. `:644` passes if `sort_settings` is not lifted; `:647` catches it.
- **`d`:** `:681`, `:687` and `:688` confirm files the fixture wrote, with the helper's rc unchecked: a helper that never runs passes. `:719` passes if `record_last_run` is missing; `:720` catches it.
- **`e`:** `:747-751` scans only `echo`, `log_message`, `fail`, `note` and `why` lines with a leading literal, so a `printf 'exit code 3\n'` passes.
- **`f`:** `:803` (F-15). `:800`: the #537 check runs only if a grep of `backuptool` matches, and is otherwise dropped with no SKIP.
- **`g`:** grades the working tree under `--old` (F-17). None found at default.
- **`h`:** `:887-891` ignore `--old` (F-17). None found at default.
- **`i`:** ignores `--old` (F-17). None found at default.
- **`j`:** `:947` and `:959`: the helper's rc is unchecked (as `d`).
- **`k`:** `:1036-1047` (F-15). The skip-less `LL_SCOPED` branches belong to `l` (`:1171`, `:1195`, `:1215`).
- **`l`:** checks are dropped by scope with no SKIP (`:1171`, `:1195`, `:1215`).
- **`m`:** `:1385` matches `hostnamectl` only at a line's start, and the shim at `:1273` exits 0, so `x && hostnamectl` passes.
- **`n`:** `:1510` and `:1523` pass when the run never started; `:1507`'s rc check also passes when `bwrap` or `timeout` itself fails (F-10).
- **`o`:** none found (it reuses `a`'s, `c`'s and `m`'s fixtures).
- **`p`:** `:1692` and `:1745`: a failed `pdb` (no `python3`) leaves no store, which reads as empty, and both PASS.
- **`q`:** `:1842` reads `wait`'s rc, and `:1843`/`:1845` test markers the fixture made at `:1840` (F-13, re-derived).
- **`r`:** `:1895`, `:1908` and `:1938` are absence checks that pass when the log was never written; their positive partners fail.
- **`s`:** `:2025` and `:2030`, the same shape as `r`.
- **`t`:**
  - `:2086` (F-14);
  - `:2847-2853` grade only the verdict lines printed, so a block that throws (`:2658`, `:2681`, `:2734`) suppresses later verdicts unseen;
  - `:2090`'s `unittest discover` on a missing file exits 0 on Python before 3.12 (inference);
  - `:2059` is the section's one skip (the client tarball).
- **`u`:** none found.
- **`v`:** `:3051` (F-11, re-derived). `:3053` and `:3062`: a `set_autosave` that errors prints nothing, and *no -e* PASSes.
- **`w`:** `:3096`: *no Token of its own* is never grepped; `:3095` checks only the second run's rc.
- **`x`:**
  - before `F1.`, none found;
  - `F1.`: `:3303-3307` pass on an empty journal if the quirk directory is missing; `:3329` passes on an empty `F1_WROTE` (F-03); `:3381`→`:3394` takes the `else check 0` branch when `git cat-file` fails;
  - `:3441`, `:3478`, `:3540` and `:3565` pass when the launcher dies at start; `:3535`'s `qemu-img create` is unchecked; `F1g` and `F1h`'s *left alone* checks pass if the quirk never runs;
  - `:3866` checks rc only; `:4121` passes on an empty result when `python3` is absent;
  - `:4283` is re-derived: a no-op repair leaves both copies equal;
  - `:4433-4434`'s `-le 1` accepts zero;
  - `C.`: about twenty negatives (`:4616`, `:4675`, `:4703` to `:4884`) pass when `cloud_setup` never runs, because the sandbox's 127 is hidden by `2>/dev/null` (`:4610`); `:5627-5631` reports `result(True)` with no `node`; `:6120`'s and `:6431`'s `END n` sentinels never compare n; `:6483` takes any line as a description; `:6491` (F-09);
  - `D.`: `:6765` (re-derived): `kill -0 1` fails as a non-root user, and `flock -n` creates a missing lock, so both halves PASS when the helper never started; `:7302`, `:7351` and `:7426` pass on one verdict line; the `DT_OK` omissions (F-09).
- **`y`:**
  - `y1` to `y4`, A, A-fix and z: the *rc non-zero, nothing written* list (F-10): `:7912`, `:7934`, `:8246`, `:8258`, `:8271`, `:8352`, `:8583` (`RC -eq 1`, which is `bwrap`'s own failure code; re-derived), `:8787`, `:9172`, `:9744`, `:9951`, `:9957`, `:10085`, `:10580`, `:10727`, `:11050`, `:13270`, `:13508`;
  - negatives over possibly-absent output: `:8065`, `:8215`, `:9407`, `:10883`, `:10965`, `:13333`, `:13555`;
  - empty producers: `:8672`, `:8828`, `:10245`, `:10346`, `:13122`, `:13539`;
  - `y4`'s banner probes (F-20);
  - stream A's argv checks (`:9159`, `:9466`, `:9477`, `:9905`, `:9909`, `:10667`) assert what the script asked for, not what rclone did (F-02);
  - `CF`: `:11902` accepts `END 0`, and `:12061` counts groups above 0 only.
- **`z`:**
  - `:13423` (F-21);
  - `:13672`: `cmp` of three empty extracts;
  - `:13690`: `sort_settings` absent;
  - `:13710`: `grep -q 'rc=1'` matches `rc=127`;
  - S315's `! sz_fn` checks (`:13652-13660`) pass when the function is absent (exit 127);
  - S3F (F-19).
- **`aa`:** does not run at the hash (`MIGRATION_AVAILABLE=0`) except the D-CLOUD-170 loop (`:13904-13910`). `:13826` (F-12).
- **`ab`:** `:14003` to `:14112`: `! sc_valid` passes if `--stamp-valid` cannot run.
- **`ac`:** none found.
- **`ad`:** none found. One FAIL at `:8910` without any rclone.
- **`ae`:** `--archives-only` only (`:14183`), with no SKIP for the matrix. The `NOT APPLICABLE` line at `:14186` is F-08's.
- **`af`:** none found; it FAILs on the host's busybox (`flock`).
- **`ag`, `ah`:** F-07.

**The `skip()` paths:** 30 calls. One SKIP never hides a FAIL by itself, but three rules let absence change the count (F-09).
- **The calls:** 22 in `x` (`:6491`, and 21 behind `DT_OK`); `t` `:2059`; `y`'s `:10174`, `:10350`, `:12158`, `:12221`, `:12265` and `:12312`; `z` `:13423`.
- **Where a FAIL is hidden:**
  - one SKIP stands for N patch checks at `:6491`;
  - D's `flock` FAILs become SKIPs on a host without the sources cache;
  - `:13423` runs with any busybox.

**`NOT APPLICABLE`:** printed at `:4558`, `:9486`, `:10461`, `:10670`, `:13899` and `:14186`; counted once at `:4558`; the run exits 0 (F-08).

**The no-busybox case:** `BB_SRC` empty (`:402`) → no copy (`:416`), no wrappers (`:421`), no banner (`:426`). Every wrapper list then falls to GNU tools, and sections `b`, `d`, `f`, `h`, `i`, `j`, `l`, `w`, `aa`, `ab` and `ac` use host tools even with a busybox (no wrapper at all). It was not run (this host has a busybox); it is read from the code. **The ten:** the fixture's (F-03), sorted at stage A.

### Q4 Currency

- **No package.** The rclone stream A binds (`/sa/rclone.real`) is whatever `image_tool_source` finds (F-02): v1.75.2 from the M7 root, 1.60.1-DEV from the host. The recipe pins 1.75.2, and no case would notice the difference.
- **The busybox:** 1.36.1 is the image's (the M7 roots), and 1.37.0 the host's.

### Q5 Efficiency

The timed image run, 515 s:

| Section | Seconds | Share |
| --- | ---: | ---: |
| `y` | 248.3 | 48 % |
| `x` | 82.1 | 16 % |
| `n` | 41.6 | 8 % |
| `af` | 33.7 | 7 % |
| `t` | 33.6 | 7 % |
| `ae` | 19.8 | 4 % |
| `z` | 17.4 | 3 % |
| `i` | 14.3 | 3 % |
| `h` | 6.3 | 1 % |
| the other 25 | 17.9 | 3 % |

- **By group:** `y/A` 137.2, `y/CF` 65.9, `y1`-`y4` 36.4, `x/C` 45.3, `x/D` 31.7, `z/S315` 9.1, `y/F1r` 8.8, `x/F1` 4.9, `z/S3F` 0.3.
- **What carries the time:** stream A's 143 `sa_run` calls (`y` makes 145) and CF's shimmed runs. `n`'s, `af`'s and `t`'s waits are mostly real timeouts by design: stall ceilings and inactivity windows.
- **`vm-qa`'s 13 minutes** (T12's Q5 table) is this suite's 8.6 minutes plus `vm-qa`'s own setup, not measured here.
- **The wrong busybox costs** 677 s, 162 s more, to a verdict that judged the host.
- **The sandboxed sections could run beside the guest suites** (T12's #987 lead): they share nothing with a guest but the host's CPU (inference).

### Q6 Dead ends and brittleness: the table

(a) What each section depends on that is not the thing it proves, and what its absence does. (b) Its last recorded catch. (c) Its caller. (d) Its positive. The caller is `vm-qa`'s `scripts` suite (`vm-qa:158`) for every section, plus `--cloud-layout` (`:252`) for `ae`'s tool. "BB" is the busybox copy, and "no wrapper" means the section never uses it.

| Section | (a) dependencies, and what each one's absence does | (b) last recorded catch | (c) caller | (d) positive |
| --- | --- | --- | --- | --- |
| `a` | BB (`:459`): absent → GNU tools, a silent pass of blindspot 34's case. `/usr/bin/rsync` (`:453`): absent → FAIL. Host `tar` (`:501`) | blindspot 34, busybox `tr` (2026-09-10, `:158-160`); KILL18 (`:497`) | `vm-qa` | `1d1503180d` and `c15050c897`: FAIL as promised |
| `b` | `bwrap`, `setsid`; host `/usr/bin/tar` (`:566`, `:586`); no wrapper | D-CLOUD-078, #105 | `vm-qa` | `1d1503180d` (FAIL 7); dying-`tar` shims (`:556`, `:583`) |
| `c` | BB (`:614`): absent → GNU, silent | `sed -i '$a'` lost a last-line key (`:618-620`); #106 | `vm-qa` | `1d1503180d` (FAIL 4) |
| `d` | `bwrap`; host `/usr`; no wrapper | nothing recorded | `vm-qa` | `1d1503180d` (FAIL 9); a killing `mv` (`:714`) |
| `e` | `python3` (`:735`): absent → FAIL | the FORBIDDEN regex (`:724`) | `vm-qa` | `1d1503180d` (FAIL 1) |
| `f` | `bwrap`; host `tar`; no wrapper | #52, #64, #274, #307 PL-005, #221, #537 | `vm-qa` | `1d1503180d` (FAIL 5); a planted `leaky.conf` (`:810`) |
| `g` | the working tree's files only | 2026-09-12 F-03, #146 | `vm-qa` | none: `--old` has no effect (F-17) |
| `h` | host `sleep`, `timeout`, `date`; no wrapper | #153 | `vm-qa` | `8707919349` (FAIL 3) |
| `i` | the working tree's `cloud_net_ready`; host shell | RG SP 2026-09-12; #192 | `vm-qa` | none: ignores `--old` (F-17) |
| `j` | `d`'s sandbox | #107, #282 | `vm-qa` | `1d1503180d` (FAIL 4) |
| `k` | `bwrap`; BB `tar`/`unzip` (`:1015`): absent → GNU tar and Info-ZIP, silent; `python3` (`:1087`) | #45, #169, #165; #151 PL-03, PL-10, PL-14 | `vm-qa` | `1d1503180d` (19), `53f390b1e9` (17), `34aca64afd` (8); a grep shim (`:1103`) |
| `l` | host `timeout` (`:1164`); `bwrap`; no wrapper | #142; #151 PL-14; #273's trace of #113 | `vm-qa` | `1d1503180d` (14), `53f390b1e9` (14) |
| `m` | `bwrap`; host `md5sum`; a build root's avahi unit (`:1393-1399`), else the source unit, said | #50; #151 PL-01/02/04/14 | `vm-qa` | `1d1503180d` (17), `53f390b1e9` (17) |
| `n` | `bwrap`, `setsid`, `timeout`; BB with `flock` (`:1484`): the host's lacks it → 7 FAIL | #153; LINK5 on MinIO (`4d7eb1f303`) | `vm-qa` | `8707919349` (FAIL 7) |
| `o` | the fixtures of `a`, `c` and `m` | #154, guest b | `vm-qa` | `8707919349` (FAIL 5) |
| `p` | `bwrap`; host `python3` for `pdb` (`:1670`), rc unchecked (§ Q3) | #165, #173, #180, #186 PL-16/26/32 | `vm-qa` | `34aca64afd` (1: no ctl); `d79281066c` **dead**; `cee1656c33` (5) |
| `q` | `bwrap`; the fragment list from the working tree (`:1789`) | #166; `smb.conf` at every ref (`:1762`) | `vm-qa` | `0f7785e6ed` **dead**; FAILs at the older refs (2 each) |
| `r` | BB `sed` (`:1893`) | #176; #186 PL-29 | `vm-qa` | `28a80357ed` (6), `cee1656c33` (2) |
| `s` | `bwrap`; `r`'s helper (`:1964`) | #176 | `vm-qa` | `28a80357ed` (7); an emptied helper (`:2023`) |
| `t` | the sources cache's client tarball (`:2053`): absent → SKIP, and every `D.` group behind `DT_OK` goes with it; `patch`; host `python3`; BB `flock` (`:2097`): the host's lacks it → 42 FAIL | #186's PLs, #188, #189, #190, #194, #199, #241, #258, #299, #306 | `vm-qa` | `cee1656c33` (44), `3387cf5da0` (46); `70b6c70ca7` fires on patches (F-06) |
| `u` | `bwrap`; BB (`:2926`) | #191; #308 F-WF-07/12 | `vm-qa` | `655f103cc5` (19 of 19) |
| `v` | BB `sed` (`:3040`) | #196 | `vm-qa` | `655f103cc5` (FAIL 2) |
| `w` | `bwrap`; host tools; no wrapper | #170; #273's trace | `vm-qa` | none |
| `x` | `bwrap`; BB with `flock` via `t`'s wrappers: the host's lacks it → 34 FAIL; host `python3`, `node`, `cc`/`gcc`, `qemu-img`, `jq`; the sources cache (retroarch, ppsspp-lr, webkitgtk, the client); git history (`417dcd8610` `:3316`, `:4271`): absent → an empty fixture, caught downstream (F-03). Groups: the sub-group table | #307/#308 streams C, D, F1 and F2; #209, #198, #247 | `vm-qa` | `417dcd8610 --old` named (`:3194`, `:4500`, `:6636`), not run; no header recipe reaches `x` |
| `y` | the sandbox (`sa_run`, F-16); BB `nbin` with `flock`: the host's lacks it → 180 FAIL; rclone (F-02); `jq`, `python3`, `node`; `t`'s client (`DT_OK`/`DF_OK`). Groups: the sub-group table | #307/#308 streams A and B; the fix round; #352, #467, #315 | `vm-qa` | named in comments: `417dcd8610` (`:8905`), `f3d19dc8fb` (`:11068`, `:12089`), `a06539d8ec` (`:8593`); none run, none in the header |
| `z` | `y`'s harness; host `python3`; the BB copy (`BB_HOST unzip`, `:13402`); the host's `/tmp` (S3F). Groups: the sub-group table | the fix round's stream B; #315; the audit of #313's fixes | `vm-qa` | `f3d19dc8fb` (`:13172`), `320d2b2bea` (`:13586`), `286759eb6d` (`:13663`), named, not run |
| `aa` | the retired `cloud_migrate_layout` (`:4547-4559`): absent at the hash → skipped except `:13904-13910` | #354 phase 5; blindspot 72 | `vm-qa` | none runnable |
| `ab` | `bwrap`, `setsid`; `cloud_scan` | #350, D-CLOUD-169, #508 | `vm-qa` | none: `cloud_scan` is absent at every header ref |
| `ac` | host `timeout`, `grep`, `cut` | #332 | `vm-qa` | none |
| `ad` | rclone (`:8908`); BB `flock`: the host's lacks it → 4 FAIL | run 100 case E | `vm-qa` | none |
| `ae` | `tools/rasteratops-cloud-layout-test` (`:14188`): absent → FAIL | #365, #383 | `vm-qa`; `--cloud-layout` | none here; that tool's own (T14) |
| `af` | rclone; BB `flock`: the host's lacks it → 6 FAIL | #401 | `vm-qa` | none |
| `ag` | `${ROOT}/tools/settings-modes-test` (the source checkout's); `--busybox "${BB_HOST}"`: refused by T14's S8 (F-07) | #421 | `vm-qa` | none here; that tool's own |
| `ah` | host `python3`; `tools/melonds-upgrade-test`; the same `--busybox` (F-07) | #526 | `vm-qa` | none here; that tool's own |

**The sub-groups** of `x`, `y` and `z` that carry verdicts (the coordinator, 00:27 and 00:33). The echoed groups are named in a run's output, and the comment-headed ones (`y1`-`y4`, D-fix, F2-20..24, A-fix) only by line range. The same four columns:

| Group | Lines | Checks (image) | (a) dependencies and absence | (b) catch | (d) positive |
| --- | --- | ---: | --- | --- | --- |
| `x/F1.` (with F2-1..13, F1i/j) | `:3198-4539` | — | `bwrap`; `python3`; `qemu-img`: absent → 1 FAIL for ~17 checks; `gcc`; the retroarch and ppsspp-lr tarballs: absent → FAIL (`:4008`, `:4297`); uid 0 → FAIL; git `417dcd8610`: absent → empty, caught downstream (F-03) | #307 PL-019 to PL-076; #308 F-VM, F-EM, F-PB; G-F1, G-F2 | `417dcd8610 --old` (`:3194-3196`); a planted `.partial`; vacuity detectors |
| `x/C.` | `:4540-6634` | — | `bwrap` (127 hidden by `2>/dev/null`, `:4610`); `python3`; `node`; `cc`; `timeout`; the webkit tarball → one SKIP (`:6491`); the git index (`:6506`) | PL-015 to PL-074; G-C; #308 F-RS; #508, #352, #330, #380 | `417dcd8610` (`:4500`: *54 FAIL and 25 PASS*); constructed (`:4723`, `:4879`, `:4951`) |
| `x/D.` | `:6635-7795` | — | `t`'s client (`DT_OK`): absent → 21 SKIPs and 4 silent omissions; BB `flock`: the host's lacks it → 33 FAIL; `python3` | PL-013, PL-055, PL-057 to PL-060; #308 F-RA | `417dcd8610` (`:6636`) |
| `y/y1` | `:7799-8396` | 65 (agent) | BB (`/p7bb`): absent → the `tar` shims exit 127, and `:7912` passes silently; `python3`; host `tar`; `/usr/bin/grep` | #307 PL-004 to PL-010, PL-035 to PL-039, PL-077; G-B; #537 | none named |
| `y/y2` | `:8397-8606` | 17 | BB; `bwrap`; an `nmcli` shim | #307 PL-003, PL-031; #308 F-WF; #318 | `a06539d8ec` (`:8593`), #318's two checks only |
| `y/y3` | `:8607-8683` | 10 | host-lifted functions; host `flock` (not in `bbin`); `timeout` | #307 PL-011, PL-040, PL-041; #308 F-PB | none |
| `y/y4` | `:8684-8905` | 21 | BB; host `mountpoint` without it; banner probes accept any busybox (F-20); `python3` | #307 PL-044 to PL-077, G-B-15 | none |
| `y/A.` | `:8906-11071` | 212 (agent) | rclone (F-02); BB `nbin` with `flock`: the host's lacks it → 95 FAIL; `jq`; `python3`; `t`'s client (`DT_OK` blocks with no `else`) | #307 PL-001 to PL-070; #308 F-CS; G-A; G-D | `417dcd8610` (`:8905`), not run |
| `y/F1r.` | `:11072-11223` | 15 | `python3` and `tools/vm-upgrade-readiness-test`; git `417dcd8610`, `73b20caf86`: absent → empty, `:11131` passes silently; `qemu-img`: absent → 4 checks dropped | #309 PL-024; #546; #551 | `f3d19dc8fb` (`:11068`), not run |
| `y/CF.` | `:11224-12093` | 32 | a shell rclone shim only; `cf_src` drops a missing file silently; CF4 `--unshare-net` unprobed; `node` | PL-009, PL-014, PL-021, PL-032; G2-C | named without a ref (`:11217`) |
| `y/D-fix` | `:12094-12343` | 12 | `t`'s client (`DF_OK`): absent → 4 SKIPs; the `--unshare-net` probe (`:12285`) | G2-D; S-24; S-26 | `f3d19dc8fb` (`:12089`) |
| `y/F2-20..24` | `:12344-12604` | 16 | `python3`; `gcc`; the RetroArch tarball: absent → FAIL | PL-020; G2-F2 | `f3d19dc8fb` (`:12321`) |
| `y/A-fix` | `:12605-13181` | 38 | as A | PL-001 to PL-034; G2-A | `f3d19dc8fb` (`:12603`) |
| `z/S315.` | `:13592-13664` | 25 | the sandbox; rclone never executed (`/ctl/fail` answers everything) | #315 | `320d2b2bea` (`:13586`) |
| `z/S3F.` | `:13665-13722` | 15 | the host shell, no sandbox; the host's `/tmp` (F-19) | the audit of #313's fixes | `286759eb6d` (`:13663`) |

**The split proposal (a lead for the coordinator).** A split by section would make 34 files, or about six by subject: the settings writers (`a`, `c`, `o`, `y3`), backuptool (`b`, `f`, `k`, `y1`, `z`), the cloud scripts (`d`, `g`, `h`, `i`, `j`, `l`, `n`, `ad`, `af`, stream A, CF, S315), the network (`m`, `q`, `u`, `y2`), the proxy (`p`, `t`, `D.`, D-fix), and the boot quirks (`F1.`, `F1r.`, F2), with the retired `aa` and `ae` apart.
- **What it would cost:** the harness (`:259-430`), `src_of`, the busybox copy and the sandbox helpers would have to become a sourced library, which is one place to fix F-01, F-05 and F-16, but one more file `vm-qa` must keep beside the suite. A section-local fixture reused later (`o` reuses `a`'s, `c`'s and `m`'s; `D.` and A depend on `t`'s `DT_OK`) would become an explicit dependency between files. And the 30 skips and `NOT APPLICABLE` would need a verdict carried across files.
- **What it would gain:** an `--old` run per file, so a ref that predates `x` would still prove `a` to `w` (F-05); a failure attributable by file in `vm-qa`'s report; files a reader can hold whole (the largest, stream A, is 2,166 lines); and a section's positive written beside it rather than in a header that stopped at `v`.
- **The cheaper half first:** F-05's fix, a script absent at `BASE_REF` making its section NOT APPLICABLE rather than ending the run, delivers the `--old` gain without a split.

### Q7 Clarity and structure

- **The header's claims** (`:7-148`) cover `a` to `w`; `x` to `ah` (933 of 1,313 checks) have none. Each section's `echo` line matches what its checks assert, except `t`'s *each compiled* (F-14) and `q`'s *the boot pass ran* (F-13).
- **`--help`** (`:239-250`): *Run the host script regression suite with the image's busybox* is false from every M6 worktree (F-01). It says an unusable **explicit** `QA_SYSTEM_ROOT` is an error, which is true, but not that an absent one falls back silently.
- **`vm-qa:22`:** *the scripts under busybox shims, on the host*: true, without saying whose.
- **`upgrade-and-install.md:216-221`:** *the test now runs every command that is a busybox applet on the device ... through the image's busybox from the build root*: true only where a build root is found (F-01). A rule: a lead, not edited here.
- **`instruction-files.md:175`:** the index row's Detail-in rule, `generic-x64-vm-testing.md`, names the file twice (`:1040`, `:1307`) and never describes it, T14's PL-12 shape. A lead for #1007's kind.
- **`:264` and `:266`** advise `setsid -f`, which does not reset an ignored SIGINT (F-18).
- **The split:** § Q6.

## Instruction File Recommendations

Leads for the coordinator; no rule is edited by this lane.
- `upgrade-and-install.md` § Verify on a device: add that a test which falls back to the host's tools must say so in its verdict (F-01's fix makes it true).
- `generic-x64-vm-testing.md`: describe this file under its index row, or move the row's Detail-in to a rule that does.
- `engineering-practices.md` § Guards must fail closed: the `2>/dev/null` on a read inside a pipeline (F-03) as a named shape, beside `ls A B`.

## Quality self-check

- Every finding cites a line at the hash, and every Medium or higher has its deciding artifact in § 4.5.
- The agents' leads not re-derived are marked as theirs or as inference.
- No count is given without its command: the 319 by `diff` of the verdict lines; the 1,313 by `grep -c`; the seconds by the timed run.
- **What reading cannot prove:**
  - whether `flock` causes all 131 flips that name no applet;
  - whether a host without `jq` or `node` behaves as read (not run);
  - the `--old` refs `717bc04449` and `51e2acece6` as the intended controls (not run).


## Context: engineering-practices.md § Guards must fail closed (next)

## Guards must fail closed

A check that cannot run has not passed. Three defects in one day's work shared
this shape, and all three were invisible because the failure mode was silence.
A fourth, later, had the same shape and the opposite outcome:

- A pipeline's status is its **last** command's. `if ! producer | consumer`
  tests the consumer, so a producer that exits 1 — an unreadable input, a full
  disk — is discarded and the guard never fires. `backuptool` wrote short
  archives and announced them as successes.
- An **unquoted** list expanded into a command's arguments. A member name with
  a space split into two names that did not exist, the tool errored into
  `2>/dev/null`, and those members went unscanned — a *credential* scan
  quietly checking less than it claimed.
- **`ls A B` exits non-zero when either glob is unmatched.** Gating on it meant
  that once only one archive format was present — the normal state after a
  format change — the whole verification block was skipped, disabling the guard
  added for a shipped data-loss bug.
- **A check that reads a fixed position in another tool's output.** Verifying
  a Dropbox merge with `rclone check ... | tail -1 | grep -q "0 differences
  found"` looked exact, and matched nothing: rclone prints `N matching files`
  last, and the differences line second to last. This one happened to fail in
  the safe direction — it kept every directory it could not confirm, so the
  cost was a re-run rather than 489 MiB — and that is the whole argument for
  the rule. Grep the output, not a line of it, and let the safe branch be the
  one a broken check falls into.

Each reads as a reasonable check. Each defaults to "proceed" when its own
machinery breaks, which in a subsystem whose signature failure is *reporting
success while doing nothing* is precisely backwards. (The fourth defaulted to
"stop", which is what the rule asks for and why it cost nothing.)

So:

- **Prefer a positive assertion over the absence of an error.** Collect what
  exists and check the count, rather than branching on a command's exit status
  that also means "one of your arguments was empty".
- **`set -o pipefail`** (a subshell keeps it local) wherever a pipeline's first
  stage can fail.
- **Quote every expansion** that becomes another command's arguments, or pass
  the list some other way.
- **`ssh -n` inside a `while read` loop** (or redirect `< /dev/null`). ssh
  reads the loop's stdin, so the loop processes one item and exits having
  reported success; the count is the only thing that shows it. The same is
  true of any command in the loop body that reads stdin.
- **Prove the guard fires.** Construct the violation it exists to catch and
  watch it fail, then fix it and watch it pass. A guard with no observed
  positive is a guard with no evidence — the same rule blindspot 14 states for
  hooks, applied to checks inside a script.

An assertion that cannot fail is not evidence. Ask what input would produce a
FAIL; if you cannot name one, the check proves nothing.

**A fixture for a secret scanner is built at run time, never written as a
literal (2026-09-28, #307).** `tools/last-good-scripts-test`'s cases for the
credential scan and the redaction feed values that look like a private key,
an OAuth token and a `devpassword=`; three were committed as literals by a
fix stream, the push guard read them in history, and the unpushed range had
to be rewritten by the maintainer before `next` could move. So a fixture is
assembled when the case runs -- `printf '%s' 'OPENSSH PRIVATE KEY'` into a
format string, a value passed through `$(printf ...)` -- and the file at rest
carries no line the guard would match. `.githooks/pre-commit` (both
repositories) now refuses such a line at commit time with the same patterns
the push guard uses (`.githooks/secret-patterns`, one definition); a
refusal there costs one edit, at push time it costs a rewrite.

**The positive is recorded where the guard is wired (audit #258, P-02).** A
hook line, a CI step, a suite line or a `check` in a script is committed
with a work-log line naming the constructed failure it was seen to catch,
the date, and the command -- five guards in the RC round had none (the
build's `--wrap-mode=nodownload`, the push guard's index warning, a red
`fork-checks.yml` run, `tools/retroarch-wrapper-test`, `tools/archaeology`'s
own constructed case), and each was proven in an afternoon once asked. A
guard whose positive nobody can point at is a guard whose first real firing
will be argued with. No tool audits this yet: `tools/ceremony-check` proves
blindspot entries name a guard that exists, not that the guard has fired;
extending it to the fork tools is #254's, and until then this paragraph is
the whole enforcement.

**Success reported over a no-op is the same defect with a friendlier face
(audit #258, P-04).** Four shapes from one round, each green:

- **A count echoed is not a floor.** `echo "USING: $(wc -l < table) games"`
  printed `0 games` and the build went on; assert the number, and fail under
  the floor.
- **An exit code named must be defined.** `exit ${EX_USAGE}` with no
  `EX_USAGE=` anywhere is `exit`, the last command's status -- the usage
  `echo`'s 0. `set -u` does not catch it in a script that never enables it.
  Define the constants in one block at the top and grep `exit \$\{` against
  it.
- **A success log line is written from the artifact, not the exit status.**
  `save state copy recorded` on rc 0 recorded nothing when the script had
  exited 0 with a WARN; the script now exits a distinct code and the caller
  says "recorded nothing".
- **A lint reads every copy of the claim it checks.** `lint-audit-artifacts`
  read the Phase 7 table and never the YAML index beside it, which said
  `open` for 32 resolved items; it compares them now.

**And a suite is not wired in until it has been seen to FAIL once, on the
runner's own guest.** "Prove the guard fires" applies to a whole check as
much as to a branch inside one. The time-to-play cell (#135) was written and
measured on a guest whose RetroArch had been set to GL by hand months
earlier; its first dispatch by `tools/vm-qa` on a guest running the image's
default Vulkan driver -- which a QEMU guest cannot draw with -- printed
`time-to-play: PASS in 581s` over a table in which every headline number was
`-`. The tool judged its run by whether it *ran*, not by whether it
*measured*. Three rules came out of it, and they generalise past that suite
(blindspot 39, D-QA-022):

- **A tool that reports numbers fails when the numbers are missing**, and
  says which (`headline_missing()` in `tools/time-to-play`; the report ends
  "Not a pass").
- **A tool that needs the guest in a state the image does not ship puts it
  there for the run and restores it** (`--vm`), rather than depending on a
  condition that happened to be true where it was written.
- **The first PASS of anything new is the one to distrust.** Construct the
  failure, watch the runner report it, then trust the green.

A fifth, of the same family (2026-09-10): the picker's scan named the one
failure it anticipated -- the network gone, exit 69 -- and let every other
failed listing fall through to the success path, so a cloud that refused the
connection was presented as an empty one. A branch for the failure you
expect is not a guard; the guard is that the success path is reached only by
success (`rc -eq 0`, or the one other code that genuinely means "nothing
there"), and every other value is a failure whether or not you have a name
for it.

Two more shapes, the fourth and fifth instances of blindspot 22 (a probe
that cannot report absence), promoted here on 2026-09-06:

- **A missing tool is a failing guard.** `comm … | wc -l` on the image's
  busybox — which has no `comm` — read 0, and 0 meant "nothing differs".
  A count built on a command that may not exist must fail loudly when it
  does not (`command -v` first), and any script that reaches for a
  coreutils name runs on the VM before the host's answer is believed
  (`generic-x64-vm-testing.md` § What the guest's busybox lacks).
- **A kill by pattern reaches the shell that runs it.** `pkill -f
  'vm76[.]qcow2'` killed its own shell because the same command text held
  the literal in an `rm` three lines down, and `bash -c` carries the whole
  script in its argv. Long-lived processes get a pidfile; a kill goes by
  PID; when a pattern is unavoidable, filter the hits by
  `/proc/<pid>/comm` before signalling.



## Context: upgrade-and-install.md § Verify on a device, not on the host (next)

## Verify on a device, not on the host

**And on the VM before the device** (`engineering-practices.md` § "If the VM
can test it, the VM tests it first"). The VM is a device for this purpose — the
same busybox, scripts and binary — and it is the one you can afford to break.

Host tools are not the tools on the device, and the difference hides real
failures. Info-ZIP on a desktop silently replaces a symlink and returns success;
busybox on the device refuses and aborts. The bug was invisible until it ran on
the target.

The cheap way to cover both paths, per
[`generic-x64-vm-testing`](generic-x64-vm-testing.md):

- **Clean install** — boot the built image in a fresh VM.
- **Upgrade** — boot a VM from the *previous* image, use it enough to create
  state (a backup, a config change, a save), then update it in place and confirm
  that state still works.

`tools/vm-upgrade-rehearsal <previous img.gz> <new tar> <new BUILD_ID>` runs the
upgrade half end to end and fails closed on any piece of state that did not
survive (first run 2026-09-20, build 15 to `77e7e97515`, 20 of 20). The clean
install is what `tools/vm-qa` boots from the image every run.

**And under the device's tools, not the host's.** `tr -d '[:print:][:space:]'`
deletes every printable byte under GNU tr and eight literal characters under
busybox tr, so a text check that passed in `tools/last-good-scripts-test`
rejected every real `system.cfg` on every device and the last-good record
was never written (2026-09-10, blindspot 34). The test now runs every
command that is a busybox applet on the device (`sed mv cp tr head wc cut
awk`) through the image's busybox from the build root, and its fixtures are
the image's own files, not three lines typed for the test. When a script
will run under busybox, ask of every external command it calls whether the
host's is the same program -- `readlink -f $(command -v tr)` on the device
answers it -- and shim the ones that are not, not only the ones already known
to differ.

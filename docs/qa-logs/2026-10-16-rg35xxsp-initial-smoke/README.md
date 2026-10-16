# Initial RG35XX SP smoke — October 16 (#344, #614)

Basic health, menu rendering, return to the frontend and protected-state preservation
pass on the private `0.0.1-dev+20261015T161744Z.g077197e6cd3e` image. The browser
subcase is **incomplete**, with its original watchdog exit1 retained. This is no
public RC designation, full authentication test or universal memory/speed claim.

## Authorization and scope

The owner's exact initial-test request and VM-first plan are retained in
`originals.tar.gz` (`test-plan.json`/response, #344 comment6206334111). Existing
VM proofs remain accepted. The physical H700 compositor, installed native stack,
actual retained storage and memory are the named non-VM facts. All screenshots
and synthetic inputs use `tools/device-act`, strict preexisting host identity and
exact build/boot guards. No personal game, cloud file operation, credentials
entry, saved setting change or reboot occurred. Temporary OAuth state and normal
logs are expected effects of entering and cancelling setup. Separate RG SP and
Nova transfers were not started.

## Observations

- Same boot `067a27f1-143d-4fe8-83cd-937560a5c87b`, ES PID2696/start5810 and active
  services before/after; zero service restarts, failed units, kernel-error entries
  or OOM matches. Panel compositor is 640x480. First black frame was idle; a
  non-activating Right key woke normal rendering. Compositor pixels do not prove
  physical buttons, panel glass or audio.
- Main menu, game settings, cloud hub, connected-provider management, separate
  connection form and on-screen-keyboard route render. The public Dropbox page
  loads through the **normal ES handoff**, without sign-in or account access.
  [Reviewed frame index](frame-index.json) binds every retained frame to 077197 /
  ES16dbac. Canonical flow remains [ES menu map](../../es-menu-map.md); this test
  changed no interface or IA.
- Immediately across browser startup, sampled ES PSS 105994→64447KiB. The full
 66-sample observation reached 222108KiB available RAM (216.9MiB), WebKitWebProcess
  peak 372755KiB PSS (364.0MiB), memory PSI avg10 peak4.59. Reclaim continued after
  initial rendering. These are observations, not a controlled attribution of all
  memory savings. The guard's process list omitted Python3.14; global memory/PSI
  and full before/after census still include its effects.
- The 90-second browser deadline fired, sending SIGTERM through a pidfd bound to
  PID31023/start429594. The low-memory threshold did **not** fire. Original
  `browser-guard.rc` is1, reason `browser_time_limit`. Installed normal close
  returned0 but overlapped that deadline; neither independent normal exit nor a
  browser crash is established. Correctly named synthetic Escape did not visibly
  close the page, but input delivery/focus was uninstrumented. #614 requires a
  deterministic VM case before another hardware reproduction; Select+Start is
  a separate stop_browser path and was not tested.
- ES returned, Back cancelled the unfinished OAuth attempt and navigation returned
  to the normal carousel. All 163 protected files/25,549,175bytes, three recovery
  entries and every selected configuration/credential/path/hash/mode remain equal.
  Automatic cloud sync stays off. Available RAM recovered to 582944KiB (569.3MiB).
  OAuth is idle; no test browser, WebKit child, rclone, guard or virtual keyboard
  remains. No firmware build/VM/provider audit job is running.

## Diagnostic failures and next work

Keep the original missing cloud_connections import-path error and unsupported
`esc` key error; both failed before sending input. The corrected import and
`escape` name did not rewrite those results. A combined up/up/select operation
was rejected by automatic safety review because a backup row was visible. The
safe alternative moved only the highlight, reviewed its frame, then selected the
confirmed management submenu; no cloud transfer ran.

#614 separates normal close and key-delivery evidence from the emergency guard.
It does not reopen #570's completed repairs or claim a new memory leak. #613's
unused fallback symlink and #607–610's affected-platform fixes remain queued;
Nova deployment still requires applicable fixes and qualified new bytes. #528
publication/source requirements and website work remain separate from private use.

The archive retains 58 selected originals byte-verified against their source files;
11 reviewed PNGs remain exact. Full private save/config manifests and the frame
showing a personal cloud path remain in the mode0700 local owner directory,
`/tmp/pix-m7-rg35xxsp-initial-smoke-20261016-01`, outside Git. Helpers are historical,
state-bound diagnostic sources, not a standing instruction to repeat device tests.

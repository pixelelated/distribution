# #614 — installed browser exit qualification

**PASS, focused VM scope.** Exact product077197 / ES16dbac, accepted GENERIC_X64
image SHA256 `c5de01b869c5bb28966ab5d654b95a8ed36581c38b380ed885a5946489009932`.
No product code, package pin, player copy, or physical device changed.

Can this be done on the VM? Yes: one fresh no-NIC Q35/UEFI guest, standard8GiB/
4CPU/640×480 profile and16GiB disk. The unchanged first-boot selected-state gate
passed with0 blocked/0 errors before fixture staging. A bind-mounted fake rclone
handles only `authorize` with a loopback redirect/page; all other commands use
the installed original. It never issues a token. The normal EmulationStation
menu opens installed cloud_oauth and cloud-signin-window. CLOUD_SIGNIN_DEBUG
exposes the actual key handler; non-grabbing input events and page events prove
consumption separately from transport. Compositor focus was natural in every
accepted case; no focus correction was used.

| Guarded repeat | Evidence/outcome |
| --- | --- |
| QEMU keyboard | `q` is a trusted DOM key/input event; Escape appears as key65307 in the actual browser log and exits. |
| Short-lived virtual keyboard | The same immediate-destroy diagnostic shape as the handheld succeeds. Invalid `esc` is refused; valid `escape` produces kernel key1 and browser key65307. |
| Installed normal close | Started against live PID9772/start68494, returns original0 in0.27249s; browser disappears and ES resumes. |
| Installed phone HTTP handler | Guest-loopback POSTs return204; `v` reaches the field and Escape reaches the browser handler. This is not a physical phone/browser or network test. |

Every repeat retains ES PID2387/start9057 and boot896817c5-077f-4e10-b36f-1762351f622d.
Each return removes browser/WebKit/wait/input devices. Each UI cancellation
removes OAuth and synthetic rclone; final remote list is empty and rclone's
original binary mount is restored. The observer had a fresh heartbeat and active
systemd state before/after each case; its separate90s pidfd deadline never fired.
Observer actual service result is success/0/inactive. Kernel log has no OOM,
segfault or panic. All seven host result channels are0, every owned process exited,
admission31a92b1b is consumed, and2,481,815,552 allocated bytes of disk/OVMF were
retired after compact export. There is no active VM/watcher left.

## Retained failures and limits

The first observer stopped after0.17s because this kernel has no
`/proc/pressure/memory`. Its own flawed finally block wrote rc0; original systemd
ExecMainStatus1 and cleanup assertion1 establish failure. Initial functional
cases are **excluded from guarded qualification**. No absence-of-guard-file pass
is inferred. The additive observer02 records exceptions, represents missing PSI
as null and requires live heartbeat/service assertions. Four complete cases were
then repeated; the first observer and every original response remain unchanged
in the archive and guest-evidence/qa614-run01. Earlier preparation refused a stale
verifier and an overbroad /tmp protection entry before VM launch; current qualified
verifier and narrow owner protection fixed those fixture errors.

The accepted repeat has162 memory samples, minimum MemAvailable7,160,900KiB.
PSI is unavailable; no memory-savings, H700 capacity, WebKit-speed or leak claim
follows from this8GiB synthetic page. The previous physical90s result remains
INCOMPLETE_TIME_LIMIT. Its unsuccessful synthetic Escape is not reproduced here
and its exact cause remains unknown; focus or page behavior is not assigned as
cause. Physical Select+Start, actual Dropbox authentication, phone UI/network,
large pages and gameplay remain separate observations. No product defect or
upstream patch was established by this check. Already written: no product bytes
or personal device/cloud state changed; no state remediation is required.

## Custody and readiness

[Reviewed frame index](frame-index.json) records the unchanged flow against exact
source. [Repeat result](repeat-result.json), [host exits](host-exits.json),
[consumption](admission-consumed.json) and [retirement](retirement.json) bind actual
results. `original-records.tar.gz` preserves761 source/command/frame/receipt files
(3,042,641 uncompressed bytes); `original-records.json` gives each digest.
`fixtures/` retains executed diagnostic code, including the failed first observer;
these allocation-specific fixtures require a fresh owner, not blind replay.
`verify.py` rechecks the immutable originals without starting runtime work.

This resolves the portable #614 proof gap and supports continued private H700
owner testing. #613 remains before the next candidate/public RC; #607–610 precede
affected Nova deployment. #528 public-release obligations and website work remain
separate. Earlier accepted build/audit/upgrade matrices are not relabelled or rerun.

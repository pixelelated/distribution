# Steam metadata bounds and remaining recovery — #582/#580

Completed 2026-10-15 00:57:28 UTC. The no-network GENERIC_X64 guest used the
frozen fac608ff firmware, installed curl/Bash, and the exact prepared sources.
Run `20261015T005126Z-af985198` and its launcher, command, monitor and wrapper
all exited 0. All 14 cases passed with their original expected exits and selected
state restored. The bounded stopped-media export also exited 0; admission
`9351cef4f30f44159d27ca691f1f1440` is consumed qualified. Five recorded host
owners were absent, QEMU stopped normally, and the output disk unmounted normally.
Media remains held for guarded retirement; nothing here claims deletion.

## Metadata controls

The exact candidate function from installer `cefb22a5…3264` ran with installed
curl/Bash. Only its URL is redirected to a private loopback fixture; the argv
recorder delegates curl unchanged. Both normal metadata variants succeeded.
An oversized response failed immediately with curl 63; a stalled response failed
with curl 28 after 30.006 seconds. Existing failure presentation adds its unchanged
10-second delay. Exactly four expected HTTP requests occurred, no extra probes;
all listener threads and process groups exited. Installed dependency and selected
state manifests stayed equal. This qualifies the new `-q`, connect/time/size
bounds, not a live provider or native Steam launch.

## Fourteen remaining transaction cases

Five fresh/existing/profile/client cases returned 0; four unsafe partial or
conflicting states refused with original 1; five injected failure/interruption
cases returned 1 then succeeded with original 0 on retry. Every expected status
is retained in `export/reviewed-case-exits.json`, with full guest stage originals,
archive manifests and raw caller traces under `export/guest/steam/`.
The existing nine accepted transaction cases were not repeated.

These 14 cases exercised the unchanged frozen whole caller `fab7cdb4…9229d`
in private source chroots with synthetic boundaries. Native client exec is
intentionally denied and separately observed. The metadata function above is a
separate exact candidate-source control; this does not pretend the entire new
installer was exercised natively. GENERIC_X64 does not package the ARM/FEX Steam
installer. Installed/native ARM qualification remains separate.

## Failure custody and scope

Owner01 failed before boot because its bound launcher lacked `--no-network`.
Its original qemu-args exit 2 and aggregate failure remain in `preboot-failure/`;
no case ran. The corrected packet binds the already-qualified no-network helper
and preserves captured subprocess diagnostics. Earlier host metadata controls
also remain failed in their own packet; strict request assertions were retained.

All 170 guest files (1,074,352 bytes), all 120 original host files, the admission
consumption and exporter watcher receipts are retained. `original-records.tar.gz`
contains lossless original host records, and each guest fixture archive has a
verified member manifest. The SHA256SUMS seal covers this compact evidence.
No production device, private credentials, real cloud operation or game library
was involved. Can this be done on the VM? Yes; this evidence came from that VM.

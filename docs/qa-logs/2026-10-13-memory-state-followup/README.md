# Browser heap reclamation and Nova provenance — October 13

Refs #570, #565. Source baseline distribution `1a026648442321609b2288c2c9c06803817f9df2`,
ES `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`. This is diagnostic evidence;
no ES source, package pin, owner configuration, game save or cloud data changed.

## Measured allocator opportunity

A fresh VM20 used four virtual CPUs, 1280 MiB assigned RAM (1067644 KiB visible),
640×480 software graphics, GTK3/WebKit2.54.1 and the current handset user agent.
Four 65-second trials in sham/trim/trim/sham order each restarted ES, followed
its normal cloud setup flow and opened actual unauthenticated Dropbox sign-in.
No phone client, proxy account, entered credentials or cookie consent was used.

The small target-built interposer calls `malloc_trim(0)` only at the exact
`system("/usr/bin/cloud_oauth wait")` boundary, after existing frontend deinit.
Its constructor removes its own preload before child creation; each trial
verifies that only ES maps it. Sham uses the same observer without trimming.
Memory reads fail closed. Each case kept its own ES PID on the shared boot, loaded the
provider page and returned to the expected frontend sign-in-waiting modal.

| Case | Anonymous returned | Trim duration | Minimum available | Settled ES anonymous median |
| --- | ---: | ---: | ---: | ---: |
| sham 1 | 0 KiB | not called | 166708 KiB | 113416 KiB |
| trim 1 | 79504 KiB (77.64 MiB) | 2.049 ms | 223408 KiB | 33752 KiB |
| trim 2 | 77548 KiB (75.73 MiB) | 2.018 ms | 226884 KiB | 33608 KiB |
| sham 2 | 0 KiB | not called | 164684 KiB | 113024 KiB |

The before/after allocator used-byte count is unchanged: this returns free
heap pages rather than discarding live frontend data. The lower anonymous
footprint persists in the 10–60-second observation windows. PSS differences
are separately reported and must not be confused with anonymous savings.
Direct reclaim and provider responsiveness generally improve, but two trials
per mode on one boot and an unfrozen live page do not establish a stable
latency effect or reproduce the original handheld slowdown. Browser peak PSS
is higher in the trim cases; this does not show a smaller browser.

`matrix-analysis.json` is reproduced by `python3 analyse-matrix.py` from the
included compressed numeric samples and selected page metrics. Observed CPU
deltas pair PID/start-time across adjacent samples while the browser is alive;
short-lived work is missed. Actual `CLK_TCK=100` is in the identity receipt.
Generic `python3.14` totals are not a precise sampler attribution. Observer
overhead is not independently measured. No per-script execution-cost claim.

## Evidence and lifecycle

- `trim-probe.c`, `matrix02.py`, `sampler02.py` and the two startup-script
  copies preserve the exact diagnostic mechanism. Matrix code references its
  original private owner; it is archival, not a command to replay.
- `actual-initial-identities.txt` and `installed.txt` bind actual binaries.
  Installed libc is2.41 despite a differently named source recipe. The probe
  was built against the accepted read-only frozen toolchain in the pinned
  build container, not a newly built OS image.
- Each `run02-*/` holds actual case/sampler results, numeric process/system
  samples and selected page observations. Resource paths and query strings
  are omitted from the public page-metric copies; raw logs remain private.
- `frames.json` binds all four individually reviewed 60-second provider pages
  and all four reviewed return frames. Provider pages are included. Return
  frames stay private because a temporary QA pairing QR is behind the modal.
  The cookie overlay is untouched; field geometry is not input-usability proof.
- `matrix02-result.json` and `retirement.json` bind watcher, launcher, wrapper
  and actual host PID exits. All valid cases and final matrix returned0.
  Optional PSI is unavailable on this image and explicitly recorded as such.
- `matrix-invalid.json` preserves the first interrupted143 attempt: missing
  PSI killed its sampler, and per-case success failed to propagate sampler
  failure. None of that attempt counts. Corrected sampler health is checked
  before browser launch, throughout, and at exit; the160MiB guard stayed clear.
- Exact guest stopped, original bind paths restored, disk/UEFI/key files
  removed, ports released:2,252,709,888allocated bytes recovered. No memory
  experiment remains active. Sandboxed `/proc` is not the host PID namespace;
  process retirement was verified through the host execution context.

## Product qualification next

`cloud-handoff-trim.patch.gz` and `product-proposal.json` bind a minimal,
UNCOMPILED ES proposal: guarded `<malloc.h>` and `malloc_trim(0)` after existing
cloud handoff deinit. It preserves browser-first ordering and command status.
The measured interposer is not a compiled proof of this proposal. Next qualify
the actual source/binary with package/syntax checks, native sign-in/input/
cancel/error/return flows and same-source frames, then physical RG35XX SP (H700, Tailnet100.74.205.40)
corroboration under its recorded bench authorization (D-QA-060). Initial overlap before
deinit remains; no automatic permission to reorder startup is inferred.

Hold the more aggressive WebKit cleanup-policy candidate until this narrower
change is qualified. Its source-only packet is worker7ebc601e32,38bound inputs;
no measured benefit. Existing lazy proxy import target saving is390KiB and
GTK4 remains an uncompiled dependency/native-keyboard investigation. Preserve
offline achievements, normal rclone setup and all current functionality.

## Nova state findings

`nova-provenance.md` and `nova-field-presence.json` document the source-bound
timeline without credential values or hashes. September30 empty restore and
zero-byte backup logs explain operation dates without proving data transfer
or an actor. The old positive playcounts explain Recent entries; timestamps
predate the first fork upgrade and do not prove local play on Nova. Its first
fork deployment was an in-place update that preserved storage.

The effective on-disk account combination was incomplete on September29 and
fields were populated before the October9 update. Exact authorship and arrival
remain unknown. Earlier selected accepted-SYSTEM checks found no populated
player fields; that was not a whole-image scan. A new explicit selected-state
gate is under VM qualification in the separate #565 packet. Do not turn a
synthetic retained-state allowance into proof of an actual upgrade.

# #616 normal browser handoff and account-free provider observations

**Qualified scope: bounded functional launch, page observations, cancel, and
return to the same EmulationStation process.** The local fixture, Google Drive,
and Dropbox each launched through the normal ES/broker route. This is not a
performance ranking, trusted-input qualification, successful account link, or
hardware memory result.

The additional Google Drive test follows the
[recorded request to try another provider](https://github.com/pixelelated/distribution/issues/616#issuecomment-6230028480).
It ran before Dropbox in the same disposable guest. Product sources were
unchanged; the exact diagnostic helper and temporary fixture bindings were
removed during cleanup.

## Observed behavior

* All three final main-document responses were HTTP200, with no recorded
  main-resource errors. Each case produced one DOM binding at640×457, DPR1.
* Both reviewed Google frames show the sign-in form and an empty email/phone
  field. The two Dropbox frames show the sign-in form and empty email field.
  These frames establish that the pages painted at those observations; they
  do not establish uninterrupted rendering or positive input readiness.
* All three cases used the same default UA, **event probes on, periodic observer
  off**. The extra event probes are diagnostic overhead; this was not an
  uninstrumented browser run. No periodic observer or UA comparison was made.
* The fixed local original request and302 redirect both matched the server's
  received-UA hash. Each case's request-signal hash matched its DOM-UA hash.
  Local calibration shows a populated request signal in this fixture. It does
  not guarantee the UA sent on a provider's network connection.
* ES retained PID1645/start1146, later returned HTTP200 for idle, and no browser
  processes remained. The guard exited0 with no interventions or survivors.
  Original browser bytes and the original missing rclone directory state were
  restored. `originals/functional-result.json` retains these original receipts.

Review the six account-free frames through [frame-index.json](frame-index.json).
Every included image was reviewed by the coordinator and packager. No PIN/QR,
authorization URL, credential, entered account value, or personal device screen
is included. All other frames, including `drive-return`, are excluded.

## Input remains unproven

There are **zero `QA616_INPUT` records**. The first native local-input helper
refused with `FileNotFoundError` before its POST. It required the browser's page
marker, but unchanged `page_worth_recording()` deliberately omits loopback
addresses. That is a fixture-precondition mistake; it does not show a product
input failure. Earlier navigation keys sent before the intended button had
focus were setup false starts and are excluded from product-failure claims.
The exact sanitized refusal output remains in
`originals/native-input-v1-refusal.txt.gz`.

A [v2 fixture correction](sources/v2-unrun/native-light-input-v2.md) prepares
strict local server/helper/guard ownership checks without relying on the absent
loopback page marker. Its code, diff, and source hashes are included, but **v2
was not executed** and does not retroactively qualify this case. A future fresh
allocation needs a new server-owner receipt and native trusted-input plus
untrusted-event negative controls. HTTP204 by itself would still prove only
broker acceptance, not DOM delivery or visible painting.

## Descriptive memory and timing records

These are **whole-guest MemAvailable samples**, not browser RSS/PSS. Guest
MemTotal was1,840,260KiB. Only one tracked browser case had `owned_live` processes
in a sample, but other guest services and memory remained part of every value.

| Case | Samples with tracked processes live | Observed live-sample span | Minimum guest MemAvailable |
| --- | ---: | ---: | ---: |
| Local fixture | 34 | 33.704s | 1,333,780KiB |
| Google Drive | 16 | 15.356s | 1,312,640KiB |
| Dropbox | 33 | 32.810s | 1,205,272KiB |

The span is between the first and last sampled tracked-live records; it is not
exact browser lifetime, page load time, or user task duration. Adjacent samples
with no tracked live owner occurred about1.02s earlier, at1,334,876KiB,
1,364,984KiB, and1,360,048KiB respectively. Discovery and one-second sampling may
lag a launch, so these are not guaranteed browser-free baselines. No causal
memory subtraction or provider memory attribution is justified.

`descriptive-observations.json` binds the exact sanitized case samples and the
lossless whole-guest guard log. It also retains finite diagnostic callback
values. For Dropbox, final response and DOM callbacks were409.844ms and
1130.818ms after diagnostic setup. These are **callback timestamps, not actual
paint latency**. Console snapshot output also is not paint latency.

The cases ran for different durations while the engine build ran elsewhere on
the same host. No matched uncontended baseline or trusted-input control was
established. Do not rank providers, infer a memory-pressure root cause, claim
browser memory savings, or extrapolate this guest to the1GiB H700 device. The
metrics are descriptive evidence for planning the next controlled experiment.

## Completion and original channels

The original VM, command, watcher, runner, and launcher exited0. Original host
lifecycle summaries report no forced cleanup, remaining children, surviving
host processes, or live QEMU. Admission
`41d3a0c1d9fb4d11963a2857027d35c3` was consumed2026-10-17 05:41:40 UTC. The
owned VM disk and OVMF copy were retired at 2026-10-17 05:42:26 UTC,
freeing 2,322,104,320 allocated bytes. The exact
[retirement receipt](originals/retirement.json) retains their paths and identities.
Accepted firmware, build trees, and compact evidence were retained. This packet
contains no disk.

Preserve the cleanup exception honestly: stopping `qa616-calibration.service`
returned **5** because that bounded service had already ended. Its original
server result records natural expiry after240.224602323s, two requests, and
`stop_requested:false`. The earlier unused server also naturally expired with
zero requests. These originals are retained; the5 was not rewritten to0 and is
not a browser crash or unexplained cleanup failure. Both fixture unmounts and
broker cancel returned0.

The safe originals are in `originals/`; full VM commands, request files, argv,
private window logs, and PIN screens are excluded. `host-lifecycle-summary.json`
is a selected-field derivative bound to the original VM-result hash, not a
replacement original wait receipt. Original runner/launcher and consumed
admission records are included separately.

## Source and evidence custody

* `sanitized/`: exact per-case exported proof, validated launch receipts,
  selected guard samples, snapshot metadata, and ES identity. The historical
  snapshots explicitly do not call themselves terminal results; later cleanup
  and lifecycle originals establish completion separately.
* `sources/executed/`: exact guest-inputs03, including the v1 local-input helper,
  guard, calibration fixture, and recovered exact cleanup source. Old source
  docstrings saying “UNRUN” describe preparation time, not current results.
* `sources/exporter/`: the exact reviewed sanitizer and analysis source.
* `sources/v2-unrun/`: the proposed fixture correction and evidence, still unrun.
* `source-reference.json`: exact candidate, helper, ES, and frozen source hashes.
  The candidate C and compile qualification are in the companion
  [instrumentation packet](../2026-10-17-provider-instrumentation-616/README.md).
* `provenance.json`: every copied file's original and stored hashes. Large
  numeric guard records, the inherited-whitespace source diff, and the
  CRLF-containing refusal are lossless gzip.

This packaging step only read files, validated fixed schemas, derived the stated
summaries, and reviewed existing frames. It launched no producer, provider,
service, VM, device, input, or network action. No ELF binary, raw private log,
full request/argv record, credential, OAuth/PIN/QR frame, or firmware was copied.

```sh
sha256sum -c SHA256SUMS
python3 -I -B verify.py
```

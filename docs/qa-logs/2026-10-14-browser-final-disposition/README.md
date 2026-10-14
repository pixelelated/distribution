# #570 exact-criterion reconciliation — proposed, not applied

Recommendation: the remaining software criterion is supported. Record the
explicit recurrence watch in `proposed-body.md`, mark only that one remaining
criterion complete, and close the software investigation as completed after
coordinator review. No tracker changes, product edits, shared-record edits,
runtime, old-owner replay, or physical-device actions were performed here.

The review uses the supplied exact current body, the canonical
`bugs-are-agent-first.md` rule (D-QA-051), and published record head
`0457ac18cd061e159d19aa46f53a57eed94e42c0`. Thirty-nine original evidence files
are copied unchanged and bound in `evidence-index.json`. Published file bytes
were compared to the exact Git objects, not inferred from README status alone.
Local final image readback/continuity originals have separate exact path/hash
bindings. Historical originals are retained; this review does not promote an
earlier failed fixture to PASS or claim a fresh measurement.

## The exact three criteria

| Existing criterion | Disposition | Exact evidence and limit |
| --- | --- | --- |
| Source-bound comparison identifies relevant changes and earliest supported good/bad evidence, retaining uncertain attribution. | Already checked; supported. | `evidence/triage.md` identifies equal WebKit/browser inputs on the accepted device/VM snapshots and the earlier-good baseline that could not be bound. No new attribution is inferred. |
| Sanitized load/log observations distinguish browser, input bridge and resource/network candidates without exposing authentication contents. | Already checked; supported. | `evidence/triage.md` and the preserved issue history distinguish pressure, bridge, rendering, engine and provider hypotheses. The retained journal has 243 pressure-flush messages without the specified recorded OOM/panic/storage events. This is scoped historical observation, not universal secret or fault absence. |
| Reproduce any confirmed software defect with a synthetic VM fixture, repair it and retain reviewed flow/frame and timing evidence; otherwise record a watch item with a concrete next observation. | Software evidence complete; ready for the proposed explicit watch disposition. | Synthetic startup failure reproduced stale opening feedback; repaired native/phone retry/cancel and completion/expiry/provider-failure/Back branches passed on the compiled candidate. The allocator improvement has bounded actual-binary memory/timing/frame evidence, including preserved original guard failures. Actual final installed browser/phone return and clean/retained loader checks pass. The unreproduced physical hang gets the concrete recurrence watch below, not a cure claim. |

The criterion does not require a new provider-speed benchmark, a final-image
repeat of the earlier memory comparison, a Cartesian replay of every accepted
locale/branch combination, or physical corroboration as an issue-closing test.
Whole-image standard/release qualification is separate and remains root-owned.

## Evidence chain and original outcomes

1. **Bounded allocator result.** `memory-analysis.json` preserves baseline 1,
   candidate 0, candidate 0, baseline 1. The guards stopped old-binary sessions
   after approximately 8–9 seconds; each candidate observed 60 seconds.
   The shared 2–6-second window yields 79,882 KiB (78.01 MiB) lower ES anonymous
   memory. `repeat-analysis.json` records three 25-second same-process cycles,
   original 0. These use an actual unauthenticated provider page, not a synthetic
   reproduction of the severe hang. One boot, software rendering, a window
   selected after the first guard stop, unequal lifetimes and provider variation
   limit the result. `memory-frames.json` retains accepted/rejected dispositions.
   No provider-speed, long-term-leak, final-image-memory, or physical-cure claim.

2. **Confirmed software failure and repair.** `setup-readme.md` and
   `startup-original-failure.json` preserve the observed stale opening message
   and original overall failure 1 caused later by fixture focus handling.
   `setup-functional.json` retains successful synthetic cancel/provider-failure/
   success cases. The eight `setup-browser-*.json` files cover both keyboard
   routes at EN/FR640/1280: original 0, matching frontend PID/start/boot before
   and after, retry still waiting, cancellation idle/browser absent. Original
   start/end and stable-frame timings remain present. `setup-branches.json`
   covers the six recovered/completed/expired/provider-failed/Back cases, all 0.
   The selected reviewed frames and source/ELF hashes are in `setup-frames.json`.
   Frame-settle timings are not a measured input-to-paint latency benchmark.

3. **Applicability to final source.** `source-continuity.json` proves tested
   f7b71/a7dc ancestry in ES3178 and byte-identical `es-app/src/ApiSystem.cpp`
   across all three. The a7dc→3178 `GuiMenu.cpp` diff contains only unrelated
   save-state help additions; the browser recovery helper is identical. The
   selected French messages and effective English messages are unchanged;
   absent en_GB entries for two buttons continue to use the same source text.
   Do not claim entire GuiMenu/catalog identity or reuse an old full ELF hash.

4. **Actual final installed continuation.** fac608ff/ES3178, SYSTEM
   `ddeca0768aa0ee74f5b1cf6557d8a3cb165a89cff542d646d1f16c136726f9fc`, actual ES
   `8ce916365c4cf98919c6357b8311d0820a36e2da676949fe67038a6edd745036`.
   Final UI run `20261014T230909Z-21fa45d0` has five original stage returns 0,
   all seven outer channels 0, consumed admission and reviewed compact frames.
   Actual installed phone input delivers first571 then second571 across WebKit
   navigation and returns to Cloud Folders on the same ES PID/start/boot.
   The cancelled browser's own expected exit 1 remains 1; broker completion is
   0/idle. Synthetic authorization/listing seams do not prove hosted sign-in.
   `final-ui-loader.json` retains three original 0/empty-stderr subprocesses and
   a fresh default registry. `final-ui-frames.json` carries the previous personal
   review of 19 originals; the nine phone-flow frames are relevant here. No new
   frame review or capture is claimed by this reconciliation.

5. **Retained composition.** Corrected retained update/loader run
   `20261014T231504Z-04208eaf` has original all-zero outer channels, 22 host
   commands 0, changed boot, preserved selected state and unchanged protected
   base. `retained-loader.json` is PASS, RTLD_NOW PASS, fresh default registry,
   three loader subprocesses 0 and no surviving loader children. Its admission
   is consumed. #572's installed dependency repair is therefore actual final
   composition evidence, not merely a staged component. This run did not repeat
   the whole browser interaction matrix or default backup.

## Remaining uncertainty and proposed watch

The original severe handheld slowdown/full hang still has no established causal
mechanism or reproduced physical cure. Provider/network variation, device
memory headroom and accelerated-renderer behavior are not established by this
VM evidence. Those facts do not become software failures solely because they
are unmeasured. The source comparison also cannot reconstruct the unknown
earlier-good owner build.

Keep an eye on a recurrence on the separately designated RG35XX SP/H700 bench.
On a future explicitly authorized occurrence, retain the exact BUILD_ID, page
and navigation phase without credentials, monotonic input issue/acknowledgement/
visible-update observations, browser/frontend identities, pressure/reclaim
aggregates and bounded kernel logs, plus whether closing the browser restores
the same frontend and boot. A repeatable input/handoff failure or a timestamped
crash/pressure record tied to those identities supplies a concrete next bug and
VM fixture. This is a future observation trigger, not a new release gate or
authorization to launch a device test, sign in, reboot, or access an account.

`proposed-body.diff` replaces only the stale opening status, adds this watch,
and changes the single exact remaining criterion to checked. The dated intake,
failure history and uncertainty are preserved verbatim below the new status.
The watch must actually be recorded by the coordinator before relying on that
disposition. No remaining per-criterion software runtime is requested here.

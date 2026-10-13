# #571 phone keyboard status — source packet

Prepared 2026-10-13. **SOURCE ONLY. Browser fixture, frames, VM broker flows,
assistive-technology behavior, and device/phone behavior are UNRUN.** This packet
does not close #571 or supply a reviewed frame baseline. Coordinator w4:p2 owns
runtime allocation, shared records, integration, and publication.

The candidate replaces the variable-height status ribbon with a 44 px header:
one-line service heading on the left, ellipsis when necessary, and a 44 × 44 px
status button on the right. Shape distinguishes connected (✓), disconnected (×),
and warning (!). The button exposes the full translated description to assistive
technology and through a details panel. Status transitions announce through a
polite live region; identical polls do not repeat the announcement. Automatic
failure details never focus a control or move the typing/pointer controls. A
player can hide details; repeated identical failures respect that dismissal.
Long error text scrolls inside the bounded panel. This is a fixed **layout slot**,
not a new sticky bar that covers the page while scrolling.

## Source and refresh strategy

Read the complete live [#571 issue](https://github.com/pixelelated/distribution/issues/571)
and its [diagnosis comment](https://github.com/pixelelated/distribution/issues/571#issuecomment-6132337947),
next's checkpoint/rules, and D-UI-126. Historical checkpoint owners were not run.
The fork-specific phone page has no corresponding source at the recorded
`upstream/next` ref. The applicable upstream for this UI is the fork's own current
source/history and #571 diagnosis; no WebKit fix, dependency, or pin is involved.

Worker parent `7ebc601e32344b09a4d04bb161a8d4ba3ef95e91` and coordinator/next
`0ea6eaf74ad47503c05955d1c0bd4bd00bdfb816` contain **byte-identical cloud_oauth**,
SHA256 `81d8e448624e57a8ac78d242116259dadfba873eddf313b8fdbd742e3a9db4c3`.
Consequently no merge, rebase, or source refresh was necessary: edit that matching
file, read rules directly from next, and integrate only the new scoped commit.
Do not merge this worker's historical memory/proxy branch ancestry. Prior #570
packets and the independent ES trim were not changed or rerun.

[source.json](source.json) binds the exact baseline/candidate and preserved input
block. The only product file is
[`cloud_oauth`](../../../projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth):
HTML escaping for the service label (now also used in a title attribute),
`phone_page` translations, header CSS, and the phone page's status presentation /
probe validation. Broker lifecycle, PIN checks, HTTP endpoints, provider-host
guards, native window/popup/input handling, and all other Python AST are unchanged.

## Lifecycle traced to source

`make_handler.do_GET` generates `waiting` when `holder.browser` is absent;
otherwise a field marker or sign-in completion marker yields `open <page>`, and
the existing browser with no ready field yields `loading <page>`. The page token
is a truncated SHA256 of the browser page-state file. The PIN gate runs before
the probe. Closing/completing the whole broker may instead stop responses; the
phone cannot distinguish that from losing the network and must not assert why.

| Input evidence | Glyph / detail | Input behavior |
| --- | --- | --- |
| Initial script load, no probe yet | Warning / Checking connection | Local typing available |
| `waiting`, no browser observed yet | Disconnected / choose CONTINUE | Existing pre-open text remains queued |
| `loading`, with same or new page token | **Connected** / opening, field not ready | Existing `ready=false` gate; new page clears old-page text |
| `open` | Connected / keyboard ready | Existing readiness transition delivers pending text |
| First through fourth failed probes | Warning / checking again | No synthetic `loading`/`waiting` event; no reset or retry of the input queue |
| Fifth consecutive failure | Disconnected / Wi-Fi, VPN, possible completed sign-in | Details shown; polling continues |
| Valid probe after failures | State from that probe | No recovery-specific resend/reset |
| `waiting` after observing a browser | Disconnected / sign-in page closed | Existing `winUp=false`, `ready=false` gates |
| Script error | Warning / reload and report browser error | Sticky diagnostic; a later healthy probe cannot conceal it |

Malformed probe bodies, including a PIN HTML page delivered with HTTP 200, now
count as failures. Only `waiting`, `open [token]`, or `loading [token]` validate.
Failure count resets **after** this validation. The cadence remains a two-second
delay after each completed probe; five failures are not an exact ten-second
deadline because request duration also counts. This change adds no request timeout.

The entire block from the input queue through the pointer event bindings is
byte-identical, as are the page-token clearing and ready-to-type transition.
This deliberately makes no new claim of acknowledged text delivery: existing
POST error handling does not retry or reconstruct lost input. A transport outage
can still lose input as before; the new status must not be described as an input
receipt. That broader delivery protocol is outside this status/layout change.

## Verification and acceptance mapping

[static-result.json](static-result.json) records Python AST checks, both EN/FR
JavaScript `node --check` exits, interpreter versions, and exact source hashes.
No target module or phone script was executed by those checks.

| #571 criterion | Available source/static evidence | Required evidence still UNRUN |
| --- | --- | --- |
| Truthful lifecycle and real failure feedback | Probe mapping above; recognized-body gate; sticky script failure; unchanged readiness gate | Browser fixture navigation, delayed response, five failures, invalid 200, recovery, closed window, script failure; VM lifecycle trace |
| Compact accessible header, truncation, no vertical jump | Fixed geometry, min-width/ellipsis, full title, button name, shape, live region, absolute details | 320/768 px EN/FR geometry assertions and reviewed frames; keyboard and screen-reader review |
| Navigation/failure/reconnect/end, canonical flow | Deterministic source-bound fixture and proposed flow/copy below | Executed result/frames and coordinator update of canonical references |
| Input/touch/pointer stay usable | Preserved input-block hash and other broker AST | Queued typing, movement/tap/key ordering, masking, Close/Keep; actual native keyboard and popup/input regression |

The existing C3 load stub in `tools/last-good-scripts-test` need not grow DOM APIs:
the new `setAttribute` calls occur only in callbacks, while that stub never
resolves its first probe. The C4 DOM already has `setAttribute`, IDs and handlers.
These are source inspections, **not suite passes**. The coordinator should run
those existing regressions in its separately allocated test window; this worker
did not edit or execute the suite.

## Next serialized experiment (coordinator only; UNRUN)

Can this be done on the VM? **Yes.** Deterministic companion-page presentation,
synthetic broker navigation/failure/end, and native-window input have no physical
device dependency. Keep provider/owner data out. The first step is a synthetic
browser fixture; it is not proof of the installed broker or phone OS keyboard.

1. Review/cherry-pick only this scoped commit onto coordinator integration; verify
   the baseline and candidate file hashes. Record one runtime plan/resource lease
   in #571, then use an already available browser environment. Do not install
   dependencies or download browsers as an implicit part of this packet.
2. In that environment, first run the static/hash command below. With installed
   Python Playwright and its existing Chromium, execute the prepared command in
   a fresh output directory. Use a network-isolated QA environment. The fixture
   imports only the exact `phone_page` function into a synthetic namespace; it
   does not import the broker. It intercepts the synthetic document, denies all
   other requests, blocks service workers, sets the context offline, and replaces
   fetch/poll timers with deterministic responses. It opens **no listener**.

   ```sh
   packet=docs/qa-logs/2026-10-13-phone-status-source
   (cd "$packet" && sha256sum --check SHA256SUMS)
   python3 "$packet/static_check.py"
   # UNRUN: needs coordinator runtime allocation and pre-existing browser deps.
   python3 "$packet/browser_fixture.py" --browser chromium \
     --output /workspace/tmp/pix-m7-investigation-20261013/phone-status-run-01
   ```

   Record process exit, `result.json`, browser/library versions, source hash, and
   eight frames per language/width. A result is not PASS merely because images
   exist. The fixture retains a failure result and produced frames; stop and
   return the first failure rather than silently rerun. Time/scratch bounds are
   for the coordinator's lease, not newly granted here.
3. Review all EN/FR 320/768 frames, then allocate a separate VM broker/native
   browser flow. Stage only the verified changed `cloud_oauth` source using the
   established QA overlay procedure. Use synthetic pages/credentials and the
   existing broker fixture, not an owner session. Trace first scan (`waiting`),
   continue (`loading`), actual field focus (`open`), reload/token change, delayed
   focus, controlled probe failure/recovery, Keep then Close, and sign-in completion
   / listener end. Observe native popup opener and keyboard/input unchanged.
   The deterministic fixture's mocked protocol cannot certify those signals.
4. Coordinator attaches exact-source frames/results to #571 and updates canonical
   flow and copy references. Only then can the UI criterion be considered for
   completion. No production pin/build/promotion follows automatically.

## Proposed canonical handoff, not edits to shared records

For `docs/es-menu-map.md` phone keyboard paragraph and
`docs/pixelelated/cloud-folder-flow-review.md` companion flow, replace the old
full-width status-ribbon description with: “The phone header retains the service
heading and a fixed connected/disconnected/warning status control. Loading a
handheld page keeps the connection indication; readiness controls when queued
text is sent. Tap the status control for details. Genuine failure details appear
without moving the keyboard or pointer. Close remains at the bottom and asks
Keep/Close once.” Bind that description to reviewed exact-source frames, not this
source packet alone. There is no new ES menu row or native screen copy.

[copy.md](copy.md) lists every new/changed EN/FR string and the remaining locale
review boundary. No broad phone-page translation, production changelog, shared
flow, issue status, or work-log edit is included here.

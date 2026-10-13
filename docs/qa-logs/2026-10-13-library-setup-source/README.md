# #567 / #578 / #570 — bounded source handoff, October 13, 2026

**Source candidate only. All prepared runtime fixtures are UNRUN.**

Final ES commit `6b1dd68246c89f4c1c0fa17c3d8941ffd3b3d420`, on
`feature/m7-library-setup-567` in
`/home/max/Development/emulationstation-next.worktrees/m7-library-setup-567`.
It adds the requested #570 failure response to parent
`44b0522ae39a664209af35f8503b933bee09a1db` (#567/#578), whose parent is the
accepted baseline `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`.
Exactly two files differ from that baseline:

| File | Git blob | Change |
| --- | --- | --- |
| `es-app/src/guis/GuiMenu.cpp` | `96c66f3384a6c044b31b4d0f65acfd2d1685e464` | Conditional Update Gamelists explanation; browser-window failure retry/cancel |
| `es-core/src/Settings.cpp` | `425358c056837cc6127b67f61939f07924543773` | Compiled default `favorites, recent` → `favorites,recent` |

No other ES source or translation catalog changed. Independent trim commit
`f7b71db0a70e1c48627f70847ecbc95bb1cb4a43` changes `ApiSystem.cpp`; it was
neither replayed nor included. No integration branch, distribution pin, shared
record, previous clean-state source, private owner record or GitHub item was
modified. Local ES worktree creation and commit succeeded without an approval
blocker. Coordinator w4:p2 owns subsequent integration and all runtime.

The added #570 proposal, lifetime reasoning, exact copy, fixture command and
actual failure-frame requirements are in [browser-window-failure.md](browser-window-failure.md).
No earlier #570 allocator/browser result is a test of these new source bytes.

## Source findings and implementation

Read complete live [#567](https://github.com/pixelelated/distribution/issues/567)
and [#578](https://github.com/pixelelated/distribution/issues/578), including
their comment arrays (both empty), and the current `next` checkpoint/rules.
After the scope extension, read complete #570 body and all 38 live comments,
the OAuth lifetime rules and both existing OAuth test sources.
Accepted-source observations are in
`docs/qa-logs/2026-10-12-owner-feedback/README.md` and
`docs/qa-logs/2026-10-13-library-wifi-baseline/README.md` on `next`. Their prior
results are baseline evidence; none was rerun or counted as fixed-source proof.
The distribution control-script inspection used coordinator publication
`0ea6eaf74a`; no firmware or cache was extracted/copied.

#567 now adds one translated paragraph before the original question, only under
`ROCKNIX` with `OfflineAchievements::available()`, `toggleOn()`, and
`Settings::CheevosCheckIndexesAtStart()` all true. The startup-index predicate
matters: players can turn that setting off independently after enabling offline
achievements. The source's index trigger does not additionally require the
global achievement switch or a signed-in account. Account/readiness checks
remain in the downstream backend; the notice describes the operation and its
connection requirement, not guaranteed completion.

The paragraph is:

> THIS ALSO CHECKS NEW GAMES FOR OFFLINE ACHIEVEMENTS. AN INTERNET CONNECTION IS
> NEEDED TO DOWNLOAD THEIR ACHIEVEMENT DATA.

It does not inspect connectivity or enumerate the library on the UI thread.
The existing YES callback, NO/Back action, scraper/hasher busy guards and
`confirm=false` API path are unchanged. It adds neither a second confirmation
nor a recurring background prompt. The description does not claim every refresh
downloads the whole library or that simply reconnecting always prepares every
game. `copy.fr.po` supplies the exact proposed French addition; integrate it
and the new English msgid into the catalogs before French runtime review.

Source trace (paths relative to the ES commit unless noted):

| Source | Evidence and consequence |
| --- | --- |
| `GuiMenu.cpp:5756,8491` | Game Settings entry and shared existing confirmation |
| `GuiCollectionSystemsOptions.cpp:368`, `GuiMenu.h:40` | Collection Settings uses the same default `confirm=true` function |
| `services/HttpServerThread.cpp:532` | `/reloadgames` explicitly bypasses confirmation |
| `views/ViewController.cpp:1415`, `SystemData.cpp:1098,1304` | Rescan reloads systems, then startup index; enabled by the startup-index setting |
| `ThreadedHasher.cpp:264` | Only eligible visible supported games; no work returns before fetching; hash-without-ID lookup may run once per day |
| `ThreadedHasher.cpp:32,125` | Missing hash library leaves unindexed work; completed non-cancelled identified work can trigger offline top-up |
| `OfflineAchievements.cpp:95,168,309` | Backend existence, offline toggle, then `topup --after-index` |
| `NetworkThread.cpp:248`, `SystemData.cpp:1103` | Link-return index retry only until a hash library came this session, throttled to ten minutes |
| distribution `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl:1163,2184` | Toggle/account readiness, reachability probe, full indexed-but-not-cached pass after index; ordinary reconnect is recently played except pending-index handling |
| `Settings.cpp:116,321,549` | Defaults loaded first, saved settings overlay afterwards; only the default literal changes |
| `Settings.cpp:473` | Existing save behavior omits values equal to the compiled default |
| `CollectionSystemManager.cpp:380,1042` | Comma split and exact names; Recent membership from positive playcount |

#578 deliberately leaves the parser and load/save paths alone. Explicit
`favorites`, empty, `recent`, `all`, reordered, canonical and even the inherited
spaced selection keep their existing semantics. A saved spaced choice therefore
continues to omit Recent. This is a default correction, not a migration.

## Criteria and remaining evidence

| Owning criterion | Delivered here | Still required from coordinator |
| --- | --- | --- |
| #567 entry/help/confirmation/progress inventory | Source trace, predicate reasoning, `flow-proposal.md` | Bind canonical reference and reviewed frames to integrated source |
| #567 advance conditional explanation | Actual compiled-source change; one msgid; no behavior change in callbacks | Compiler and installed UI proof |
| #567 enabled/disabled, online/offline, new/no-new, responsiveness | Exact branches below; synthetic XML/HTTPS response fixtures; cancel walk | Allocated isolated backend/VM runs; real input and end-to-end limits explicitly separated |
| #567 EN/FR and small/large flow proof | Exact French addition and frame requirements | Catalog integration, 640×480 and 1280×800 EN/FR review |
| #578 absent default and imported history | One-literal source fix; ROM-only/history inputs and HTTP/status probe | Compiled default yields Recent HTTP200 empty/populated as appropriate |
| #578 preserve explicit choices | Nine-case matrix, including explicit empty/spaced/Favorites-only controls | Same-source case receipts and actual retained-upgrade qualification |
| #578 canonical flow and same-source frames | Proposed map addition and required frame metadata | Canonical edit and reviewed clean/retained frames |

No runtime checkbox is closed by this packet. `static-review.json` records
diff/scope, Python AST, XML and JSON parsing, and translation/source matching.
No compiler, fixture import/launch, test suite, guest, browser, service, package
build, account, device or provider operation ran. Static parsing does not prove
C++ compilation, rendering, responsiveness or the behavior of a running image.

## Next executable experiment: Recent default, then the notice

Can this be done on the VM? **Yes.** Use one coordinator-allocated disposable
GENERIC_X64 guest, fresh synthetic storage, standard VM profile. No owner data,
game launch or authenticated provider is needed for collection/confirmation
proof. The existing live issues already record VM-first plans; coordinator
posts the final source-bound allocation and observes its lifecycle.

After coordinator admission, the pending compiler command is:

```sh
tools/es-syntax-check --root "$ALLOCATED_ES_BUILD_ROOT" \
  /home/max/Development/emulationstation-next.worktrees/m7-library-setup-567/es-app/src/guis/GuiMenu.cpp \
  /home/max/Development/emulationstation-next.worktrees/m7-library-setup-567/es-core/src/Settings.cpp
```

This is **not run** here. Then compile the integrated candidate with the two
blobs above and proposed locale addition, record its source parents and actual
binary/catalog hashes, and verify the running `/proc/PID/exe` identity. If
using an overlay binary, use the current mountinfo/private-bind workflow; do
not replay an old VM/owner or infer identity from the installed pathname.

Copy this packet's `fixtures/` into a new coordinator-owned guest `/tmp`
directory. With the owned frontend stopped and its settings present, the first
prepared guest command is:

```sh
python3 "$FIXTURES/prepare-collection-inputs.py" \
  --case default-rom-only \
  --settings /storage/.config/emulationstation/es_settings.cfg \
  --out /tmp/m7-library-setup-default-rom-only
```

It **only renders files in a fresh output directory**. Coordinator installs its
`es_settings.cfg` and the single synthetic `.gb` stub at
`/storage/roms/gb/pixelelated-library-setup.gb`, with no GB `gamelist.xml` for
the ROM-only case, then starts its frontend and waits for real readiness.
Require no preexisting GB games/gamelist/recovery metadata. For other cases,
install the rendered `gamelist.xml` alongside that same stub. Between cases,
stop the frontend and remove only owned synthetic metadata/recovery files, or
use fresh storage; an old ES-written gamelist would invalidate the ROM-only
control. Do not erase unrelated library data. Pace starts beyond the accepted
five-starts/ten-seconds limit; retain an unexpected service refusal instead of
silently resetting it. The fixture does not control services or clean storage.

Run the prepared read-only observation with source-to-binary mapping from the
coordinator build receipt, actual boot ID and current ES PID:

```sh
python3 "$FIXTURES/probe-collections.py" \
  --case default-rom-only --pid "$ES_PID" --boot-id "$GUEST_BOOT_ID" \
  --binary-sha256 "$CANDIDATE_ES_SHA256" \
  --out /tmp/m7-library-setup-default-rom-only-result.json
```

Repeat with each ID in `fixtures/collections.json`, using a fresh input/output
directory per case. The probe checks HTTP status **and** system membership,
selected preference semantics, exact synthetic playcount/lastplayed, and both
Favorites and Recent membership. A required collection's HTTP404 is failure,
never an empty-list substitute. It prints no raw settings or API responses.
The output's source label is the expected source; only the coordinator build
receipt binds the supplied binary hash to that source.

Prepared failure controls: wrong binary hash and wrong boot ID must fail before
API observation; `default-rom-only` against the accepted old binary must fail
Recent HTTP404; `default-history` with history omitted must fail; the new binary
with an explicit `favorites` override must fail if probed as `default-history`
and pass when probed as `retained-favorites`. An unknown case, duplicate setting,
malformed XML/JSON, missing game or unavailable API must not yield PASS. The
read-only probe creates a new result file; preflight refusals may terminate
before that file exists, so consume stderr and actual exit status too.

## Notice fixture branches and API boundary

Use the same source/binary/catalog receipt for the confirmation matrix. Stage
new-game inputs **after** frontend readiness so startup indexing cannot consume
the intended Update Gamelists stimulus. Keep Netplay indexing off and isolate
the guest from public endpoints. For no-new-work cases, use
`indexed.gamelist.xml` (both hash and ID); for a new raw game, use the stub with
no achievement metadata; for a lookup-only case, use `lookup.gamelist.xml`.
The synthetic hash/ID are public fixture constants, not a real ROM fingerprint.
Never launch the text stub as a game.

| Case | State and input | Required observation |
| --- | --- | --- |
| N1 | Offline toggle off, index on; online/offline × new/no-new | Original question; no offline-preparation explanation or offline top-up |
| N2 | Offline on, startup index off; online/offline × new/no-new | Original question; no achievement index caused by this update |
| N3 | Offline on, index on, backend present; no new work, online/offline | New paragraph; YES rescan works; no index library request or after-index top-up from this update |
| N4 | Same, newly added unindexed stub, no route/controlled failed hash-library response | Same advance paragraph; existing failed-index/offline card path; no preparation success claim |
| N5 | Same, newly added prehashed/no-ID game, controlled successful hash-library response | Same paragraph; ID lookup succeeds; downstream after-index attempt observed once; explicitly a lookup control, not raw ROM hashing |
| N6 | N5 with no synthetic account | Backend's existing no-account refusal; copy remains a capability explanation, not a success assertion |
| N7 | N5 with coordinator-owned synthetic account and isolated local preparation backend | Indexed uncached game prepared; repeat with cached game, no redundant full download; retain progress/outcome and backend request counts |
| N8 | Same toggle/index but backend unavailable | Original question; source capability branch. Only alter a disposable fixture backend path before ES starts, since availability is cached |
| N9 | Busy scraper, then busy hasher | Existing respective stop question only; no new notice stacked on it |
| N10 | Enabled confirmation, NO then Back on separate visits | No rescan event/index/network calls caused by either cancellation |
| N11 | Enabled and plain confirmations, YES | Exactly one existing rescan; existing destination and progress; no new second confirmation |
| N12 | `/reloadgames` API with confirm=false, no new work | No dialog; existing reload remains immediate |

The included `confirm-cancel.steps` starts from a **reviewed** Game Settings
frame with Update Gamelists focused. Verify actual `es_input.cfg` mappings
(standard accept `x`, cancel `z`) before use. It opens/cancels only; it does not
assert text recognition. Coordinator uses `tools/vm-visual-qa --monitor
"$OWNED_MONITOR" run "$FIXTURES/confirm-cancel.steps" --outdir "$FRESH_FRAMES"`
and reviews frames. `flow-proposal.md` names the complete frame matrix.

**Online-index fixture gap:** `RetroAchievements::getCheevosHashes()` requests
fixed HTTPS `retroachievements.org/dorequest.php?r=hashlibrary` and
`r=officialgameslist` through libcurl. Stubbing `raofflineproxy-ctl` alone does
not intercept these. `hash-library-responses.json` provides exact valid parser
inputs; coordinator must supply an isolated local TLS harness/guest-only CA
or separately identified test adapter before N5–N7. No such harness or real
provider was started here. Existing proxy installed/integration tools can
exercise their own client seams, but that is not proof of this ES entry path.
A raw-ROM hashing branch still needs a coordinator-selected legal test ROM
with a verified response mapping; the lookup fixture does not cover it.

The existing hash-library fetch is on the UI thread with connect/stall bounds;
this copy change does not fix that earlier responsiveness limitation. Measure
open/cancel latency separately from YES-to-ready under successful/failed
network fixtures, compare accepted and candidate with the same fixture, and
retain failures. The new message itself adds only existing local getters.
Nothing here establishes historical Nova account/metadata provenance or
changes the earlier clean-state evidence boundary.

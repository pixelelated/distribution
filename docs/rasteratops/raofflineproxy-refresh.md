# Current RAOfflineProxy integration for0.0.1

M7.P3, #361/#451, D-WORKFLOW-138. Selected main:
`3036478f2b2d22db451396a48f44feee94e8462f` (reviewed2026-10-05).
Archive SHA256: `8db22d572e963193031bb9e27bcbbe5d7767ab7a24e7b23b0efaedfda2f75e2e`.

The Linux Python source/test tree is identical to the actual replacement10
consumed7252fc tree (113files); all15 patches apply without fuzz. This parent
advances coupled libchdr to607694ca0812edfc9cc2030c64634fc2393668de for ANSI C
compatibility. rcheevos is unchanged. The rebuilt native library passes815
Linux tests without skips;11 fork integration checks pass with each actual7252fc
and historical865e21 predecessor. The fixed predecessor fixture retains both
APIs and its original failed run (#451). Both recipes pass pkgcheck.

Evidence: [proxy3036478](../qa-logs/2026-10-05-proxy-3036478/README.md).
Replacement12's affected installed preservation, native-format and HTTP checks
are complete:22 preservation assertions,18 native-format tests, four legacy
CHD cases and35 HTTP refusal/reconnection/idempotence assertions pass.
Receipts: [proxy13](../qa-logs/2026-10-05-pixelelated-replacement-12/proxy-13/README.md)
and [subset10](../qa-logs/2026-10-05-pixelelated-replacement-12/subset-10/README.md).
Ordinary account-backed new-award and P4 gates remain pending. No telemetry
or Linux UI behavior was changed by this source refresh.

## Previous7252fc source qualification

M7.P3, #361/#384/#426, D-WORKFLOW-138. Selected main:
`7252fc781392d45b22f50d1a92f9febc4d1fa172` (reviewed2026-10-05).
Archive SHA256: `c5c85da105782828c738539db048e62677c9da11d215c0dcc5dae8c3f79c5680`.

This update changes Linux runtime behavior: streaming response-body reads,
key/summary queries, an additive cached_game_meta table with delete/rename
triggers and one-time metadata backfill, and pending-award lookup limited to
needed achievement IDs. Existing cache and pending-award columns remain intact.
The fork's ctl listing, image repair and refresh helpers use those APIs;
whole-library preparation, pauses and base/subset award ownership remain required.

All15 patches apply with zero fuzz.003's import context and005's refresh wrapper
are rebased onto upstream's key-only lookup.008 adapts upstream's report tests
to the existing explicit-consent policy and tests non-consent values; production
consent behavior is unchanged. Both coupled native-library pins remain unchanged.
815 patched upstream tests, including native hashing, and11 downstream
integration tests pass. The full host script suite passes with no FAIL/SKIP
lines; actual5816 and all three recorded results are0. Source seals and actual
process exits verify. Receipts: `docs/qa-logs/2026-10-05-proxy-7252fc/`. Installed
replacement-image and ordinary new-award evidence remain outstanding.

Previous865e21 evidence is historical: its105 consumed Python/native files and
268 Linux/native/test files excluding two bundle scripts matched aec99c;
`docs/qa-logs/2026-10-04-proxy-865e21/`. That equivalence does not apply to7252fc.

Previous aec99c history: five Android files and one documentation file changed,
all270 Linux/native files matched ea9aba;15 zero-fuzz patches. Its completed
1e6a installed preservation and subset HTTP proof remain scoped to that image.
Receipt: `docs/qa-logs/2026-10-04-proxy-aec99c/`.

Previous ea9aba history follows.
This commit arrived during corrected-build preparation and changes11 Android
files only. All270 patched Linux/native files and both submodule pins are
byte-identical to ec60; all15 patches apply with zero fuzz. The new pin is
included before assembly, without changing Linux behavior. Evidence:
`docs/qa-logs/2026-10-04-proxy-ea9aba/`.
The preceding ec60 refresh remains historical evidence:
The four commits after5866cd9 change only the packaged service version string
(alpha2); remaining changes are Android/docs/bundle versions. All15 current
fork patches still apply with zero fuzz;199 upstream and8 fork tests pass.
Evidence: `docs/qa-logs/2026-10-04-proxy-preflight/`. The detailed earlier
refresh history below retains its original source counts and scope.
This is source integration; candidate build and VM qualification remain required.

## Patch disposition

| Prior patch | Current disposition / behavior retained |
| --- | --- |
|001|Rebased: truthful dorequest client errors;401/403 retain auth handling.|
|002|Retained: strip the synthetic casual-only warning from achievement sets.|
|003|Rebased: atomic flush notification stamp; preserve upstream usage accounting.|
|004|Replaced: the old total-library cap is gone upstream. An explicit `budgeted=False` API lets the OS's deliberate scan finish a whole library, retaining queue locks, pacing, batch bounds and server pauses. Default upstream callers keep their100-game window.|
|005|Rebased: refresh thread survives exceptions; auth refusal and consecutive failures stop a pass, alongside upstream background429 handling.|
|007|Retained: use only the configured account's cached sign-in.|
|008|Rebased: automatic corruption-log upload requires JSON true; new usage consent remains independently enforced upstream.|
|009|Rebased: distinct process/thread temporary image paths and atomic publication.|
|010|Retained: store-only requests never attempt the network.|
|011|Rebased: headers identify offline/cache responses.|
|012|Rebased: an offline/store-only image miss returns immediately.|
|013|Rebased: Content-Length and PNG chunk/CRC/IDAT validation before publication, through upstream's current image fetchers and sharded paths.|
|014|Retired: upstream `_fetch_image`/`_thread_connection` already reuse a connection per thread/host, replace closed connections and follow redirects. Existing transport assertions move to that API.|
|015|Rebased: bounded DNS and reuse of the lookup answer, preserving upstream request accounting.|
|016|Rebased: downloaded/cached, absent404/410 and transient outcomes remain visible to the image helper.|
|017|Retired: upstream subset-aware `_iter_achievementsets_achievements`/`build_achievement_game_ids` and award-parity tests already preserve each set's game ID.|
|018|Retained for the renamed project: recognize complete `OS_NAME="pixelelated"` records while preserving ROCKNIX account paths and configured overrides; focused platform-discovery tests travel with the patch.|

Fifteen patches, including the renamed platform-discovery follow-up, apply
without fuzz to selected parent3036478. Its coupled pins are
rcheevos1433173220a7eaede6a9ed7a18e94117be1821e0 and
libchdr607694ca0812edfc9cc2030c64634fc2393668de. Exact archives, patch
application and815 native-enabled Linux tests are retained in the current
evidence linked above. The older libchdr8e7b8bd belongs to earlier refreshes.
The whole upstream download/queue model remains available. The deliberate OS
helper explicitly opts out of its game-count window and checks `queued`; a
queued game produces FAIL/pending behavior, never OK/offline-ready. Indexed
work uses background request throttling and persists server pauses so restart
cannot defeat them. Image lookup retains older unsharded paths.

## Initial refresh evidence — 2026-10-03

`docs/qa-logs/2026-10-03-proxy-refresh/` records the initial125-game failure:
125 reported cached,100 actually cached. Five of eight strengthened integration
controls fail with the old helper; all eight pass with the integrating helper.
They cover indexed/unindexed125-game preparation, failure/retry, current queue
defaults, persisted pause,429 and reopen of an actual predecessor-written
SQLite store with login/cache/base/subset award rows and legacy image paths.
The reconstructed mapping remains base100/subset200 after two reopens.

On that initial refresh,180 upstream queue, award, consent, image, network
and refresh tests passed on its selected patched source. The first sandboxed attempt lacked socket/DNS access;
the host run passed. The broad fork harness now passes1,367 checks plus322 focused cloud cases
with0 FAIL/0 SKIP against this exact archive/series. Its initial four failures
were a stale schema annotation and old unsharded-path fixtures; after updating
the fixtures, timeout/503 retries and404/410 absence are exercised and pass.
Network/game boundaries in the whole-library tests are synthetic; no live
achievement account or personal cloud is used. Cold build, packaged service,
offline/online reconnect, image/UI/flush proof and upgrade remain P3.

The isolated concurrent-image-publication contribution under
`docs/upstream/raofflineproxy/image-publication/` remains prepared, not submitted.
General fixes remain owned by #168; upstream acceptance does not gate the
locally qualified candidate.


## Historical branded runtime discovery follow-up — #408

Replacement134e89 exposed upstream's exact OS_NAME=ROCKNIX detector missing
Rasteratops, so automatic account discovery could not find system.cfg. Patch018
adds the new complete identity while preserving the existing paths, configured
overrides and all queue behavior. Seven isolated controls,36 upstream platform/
config/auth tests and eight fork integration tests pass. The prepared upstream
patch includes focused tests. A rebuilt image must qualify this correction;
the original packaged failure remains in2026-10-03-proxy-identity.

The current patch018 uses lowercase pixelelated, superseding the historical
Rasteratops identity above. Its focused upstream draft is retained at
`docs/upstream/raofflineproxy/pixelelated-identity/`. Together with the concurrent
image-publication draft, it remains prepared, not submitted; #168 tracks outward
contributions and the remaining generally useful fixes. Replacement12 has now
built with parent3036478; its default/upgrade and scoped QA continuation, installed native/proxy
and HTTP reconnection proofs are retained under the replacement12 evidence.
Ordinary account-backed achievement earning remains pending. No old source-only result is relabeled as this
candidate's installed result.

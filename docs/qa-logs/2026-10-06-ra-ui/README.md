# Installed RetroAchievements reconnect cards — #465

This proof complements the [real softcore award and provider API proof](../2026-10-06-ra-award/README.md).
It uses a synthetic local account/award, the installed Storage writer, installed
flusher against an actual loopback HTTP server, installed ctl, and installed ES.
It does not earn another real achievement or contact the real provider with a
synthetic award. The earlier 33-assertion account proof remains unchanged.

Source `7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2`; immutable candidate bundle
`b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1`;
image SHA256 `c7df6a6f428086f79a377ca1b049f20694f34a868987cf12c493c78eab7b2254`.
No product bytes change. Owners verify frozen input custody and installed
identity/scripts before and after both display profiles.

## Contract and boundaries

The fixture enables the proxy UI setting before restarting ES, with no real
account configured and the background proxy service stopped. It clears only
its owned synthetic store between profiles. The installed flusher uses a local
HTTP endpoint; no function or installed bytecode is replaced. The 44 packaged
proxy files plus ES and ctl are hashed before and after every profile.

The host removes and restores the guest's real IPv4 address through serial
NetworkManager commands. This supplies the input NetworkStateWatcher observes;
QEMU link-off alone can retain the address. The source deliberately shows no
award card at game exit (D-RA-030). Previous exit-only carousel captures did
not establish a broken product card.

The matrix is English/French at 640×480 and 1280×960, on the complete software
rendered panel. Each profile starts with pending 0 and no send outcome, seeds
pending 1, reconnects, frames the sending card, invokes the actual flusher,
and matches the sent card to pending 0, the flush receipt, UI log and outcome
stamp. After dismissal, an empty reconnect must leave the outcome unchanged.
English 640 additionally refuses the award with HTTP 503: pending 1 survives,
the bounded card ends not-sent with retry text, and then dismisses.

The UI case does not cover real-provider authentication, actual award input,
background service scheduling, physical Wi-Fi or device rendering. RA33 and
the retained installed subset/retry proof supply their separately named
coverage. This is composed evidence, not one new uninterrupted provider run.

## Superseded owners

- Owner01/run20261006T063640Z-fa7faea7: 89 assertions, all four rc 0;
  terminal 06:44:23UTC, actual cleanup 06:44:42. Its source census selected .py
  and missed installed .pyc, so it cannot qualify proxy byte invariance.
- Owner02/run20261006T064452Z-f0f26182: 101 assertions, all four rc 0;
  terminal 06:52:34UTC, actual cleanup 06:52:57. It adds the compiled-module census and
  actual ES restart/lifetime controls. Direct review found its French 640
  baseline already showing a send card: the preceding refusal left pending 1
  across the language restart. Its runtime assertions cannot establish clean
  stimulus isolation. `visual-review-superseded-02.json` retains that finding.

Original receipts, sealed harnesses and frames are preserved. Their successful
exit codes do not override these qualification failures. Owner03 adds explicit
profile-store isolation and supplies the final qualified matrix below.

## Permanent harness changes

`tools/ra-ui-test` is the reusable local UI fixture. The ordinary
`tools/ra-offline-test` now reloads ES settings before launching, removes the
actual address while offline, captures reconnect as well as game exit, and
checks a current sent outcome. Unearned preflight, real award and provider API
checks are retained. Bash syntax passes; this matrix exercises the changed
settings/reconnect mechanics. The complete changed ordinary award runner has
not consumed another achievement and is not represented as rerun.

Owners use the standard durable 5-second watcher with 5-minute inactivity
detection and connected-session supervision. Terminal four-channel results
and actual process/port cleanup are separate checks. No disconnected alert
delivery is claimed (#395). No guest disk, QA private key, real credential or
raw account configuration is published here.

## Qualified owner03

**109 PASS, 0 FAIL, 0 SKIP; all23 original frames directly reviewed.**
English640 has34 assertions (including refusal); each other profile has25.
Every baseline is empty, every sending/sent card is readable without clipping,
and dismissal/empty-repeat frames show no notification. Installed ES/ctl and
all44 proxy files have identical hashes across all four profiles and before/
after each run. Each profile keeps the same restarted ES PID/start ticks.

Owner `/workspace/tmp/pixelelated-m7-ra-ui-03`, run20261006T065301Z-41c3ed1c.
All four result channels are0; `qualified-03/completion.json` records terminal
status and actual launcher/job/watcher/two-guest process absence, no QEMU and
unbound10026/5912. The local provider/flusher exits are checked inside every
profile. The source, candidate and sealed harness verify before/after.

`visual-review.json` binds every inspected frame to its SHA256; the unmodified
per-profile result files deliberately retain visual_review=pending because
visual inspection is a later separate gate. `qualification.json` combines
that gate with the assertions and actual cleanup. Prior attempts remain
superseded. This closes #465's UI proof; P4 is the next gate, not a completed
audit or RC/device-ready claim.

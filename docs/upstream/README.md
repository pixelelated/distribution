# Upstream contributions

The [running contribution queue (#585)](https://github.com/pixelelated/distribution/issues/585)
is the live status list across projects. It records the intended upstream, owning
issue, prepared patch/evidence, remaining proof and eventual submission or
non-submission disposition. Update it as each independently useful fix is found.

Under D-WORKFLOW-165, submissions wait until the initial build from the current M7
fix set is complete and the relevant fixes are qualified. Keep release work moving;
standalone upstream reproductions and PR preparation are follow-up work, not build
gates. Retain patches/evidence now and refresh upstream/duplicate checks before
submission. Nothing in this index indicates a PR was sent or accepted.

Detailed source/evidence stays with its owner:

- [RAOfflineProxy contribution map](raofflineproxy/contribution-map.md), owned by
  [#168](https://github.com/pixelelated/distribution/issues/168): ten existing
  standalone drafts, remaining API proposals and already-upstream dispositions.
  Its October2/6 qualification belongs to those bases; recheck before submitting.
- [RVZ/proxy/Dolphin component evidence](../qa-logs/2026-10-14-rvz-proxy-components/README.md)
  for #574/#583/#584; installed proxy hashing/service/startup proof now passes.
  Actual Dolphin lifecycle/request routing now has the candidate proof below;
  final installed-image/gameplay scope remains separate under#584.
- [MD5 one-file contribution and public reproducer](../qa-logs/2026-10-14-md5-upstream-source/README.md),
  owned by #574 and destined for libretro/libretro-common; upstream-only run UNRUN.
- [Steam repair upstream comparison](../qa-logs/2026-10-14-steam-client-repair-source/upstream.md),
  owned by #582 with #564/#579/#580; bootstrap repair is implemented and
  qualified in part. Remaining recovery and native integration are still separate.

The queue also tracks focused Recent-default and Dolphin save-preservation fixes,
and conditional browser/Wi-Fi/capability/dependency candidates. Fork-specific UI
and scanner policy are explicitly distinguished from reusable component fixes.
Historical broad-series and QA-toolkit proposals remain linked without becoming
new RC requirements. The [M7 milestone](https://github.com/pixelelated/distribution/milestone/7)
owns release order; [the dated working list](../releases/next-candidate-work.md)
explains what remains from testing the last device build.

Dolphin NoGUI startup lacks AchievementManager initialization in the pinned
source and current upstream. The [minimal lifecycle repair](../qa-logs/2026-10-15-dolphin-nogui-lifecycle/README.md)
is prepared locally for dolphin-emu/dolphin and a focused ROCKNIX backport;
the [one-object build and actual-process proof](../qa-logs/2026-10-15-dolphin-startup-result/README.md)
now reproduce the installed baseline omission and verify candidate enabled,
disabled and failed-boot lifecycle branches. Final installed-image smoke and
normal gameplay remain due. Refresh the upstream bug-tracker duplicate search
before submission. #585 owns the deferred contribution.

### October15 — Dolphin system-resource layout (#592)

Queue a focused ROCKNIX package change exposing existing immutable Data/Sys at
Dolphin's compiled /usr/share/dolphin-emu/sys path. Upstream Dolphin already has
the correct install destination; ROCKNIX's manual recipe omits it. Original failed
badge reads and absent staged path are preserved. Source/pkgcheck pass; final
installed resource/startup proof remains pending. Submit after the initial
qualified build alongside the existing #585 queue, not as a new Dolphin API fork.

### October15 — completed recognition, native-state and audit follow-ups

This dated reconciliation supersedes the earlier pending-proof wording above
for #574/#575/#584 and records #593/#594/#595. It updates the existing
[#585 queue](https://github.com/pixelelated/distribution/issues/585), without
adding duplicate candidates or changing milestone order. Accepted composition
is distribution `f8636de1d105275dbf9420bbabbbc26f79abb10f` / ES
`16dbac5211eea7e70db7394372033be2be7df829`. The [final artifact and clean/retained
records](../qa-logs/2026-10-15-final-engineering-result/README.md) preserve the
producer's separate #597 reporting failure and unknown launcher wait.

- #574 now has independent Dolphin format/native/installed hash proof and final
  composition. Keep three distinct owners: libretro-common's one-file MD5 patch;
  the ES RVZ adapter/build/notices and narrow failed-hash retry; and
  **RetroAchievements/rcheevos** `src/rhash/hash_disc.c` short-read, unsigned-size
  and caller-close corrections. The last is a destination clarification within
  the existing combined disc-reader item, not a duplicate candidate. The retained
  [October13 source comparison](../qa-logs/2026-10-13-rvz-source/README.md) supplies
  its dated upstream basis. The prepared MD5 upstream-only run remains UNRUN.
- #584's [installed NoGUI lifecycle](../qa-logs/2026-10-15-engineering-image-result/dolphin-installed/README.md)
  and final executable continuity close the old installed-startup gap. Keep
  Dolphin's conditional MainNoGUI init/shutdown patch separate from ROCKNIX's
  conditional offline routing, inactive-session correction and Sys packaging.
  Synthetic failed authentication establishes neither login nor awards.
- #575's [completed native-state readback](../audits/2026_10_14-milestone-m7-next-candidate/native-state02-readback.md)
  complements accepted ordinary saves and EN/FR capability frames. Contribute
  accurate guidance only where upstream has the same capability mismatch; native
  manual/automatic states do not add ES global auto-state or manager integration.
- #593's worker controls and actual Back/reopen/normal-exit flows, and #594's
  full-helper transitions plus localized refusal, now have accepted
  [clean](../qa-logs/2026-10-15-final-engineering-result/clean/README.md) and
  [retained](../qa-logs/2026-10-15-final-engineering-result/retained/README.md)
  installed evidence. Wi-Fi worker adoption stays conditional; the Dolphin
  inactive-session patch is a separable helper/two-caller correction.
- #595 stays a one-line isolated Python invocation patch under the existing
  Steam item, separate from transactions and metadata deadlines. Recorded
  negative/positive controls qualify that invocation. GENERIC_X64 omits the
  ARM installer; SM8550 payload readback remains #555's device criterion.

ES component ownership remains ROCKNIX/emulationstation-next; D-WORKFLOW-012
routes its contribution through a focused `ROCKNIX/distribution:next` ES
patch/package change. Refresh current upstream and duplicates before any
submission. These accepted local results do not claim current-base-ready patches,
authorize posting, change #168's ownership, or broaden physical/account/RC scope.

### October15 — reused ABL correction and separate incoming OpenABL review

[#600](https://github.com/pixelelated/distribution/issues/600) applies the existing
[ROCKNIX checksum correction](https://github.com/ROCKNIX/distribution/commit/15123b29517ad92be1f6cbcc3924a92705887d12)
as local `9aa7affee9d4ad5e69725cab20b6d7ad84d93dea`. Version1.2, URL and packaging
are unchanged. The [retained failure and archive evidence](../qa-logs/2026-10-15-device-refresh/abl-checksum-fix/README.md)
record matching official/current archive bytes and preserve the original failed
SM8550 result. Fresh SM build and acceptance remain required. This is reuse of
an existing fix, so no duplicate outgoing contribution is queued.

[#601](https://github.com/pixelelated/distribution/issues/601) separately tracks
the later OpenABL replacement and corresponding-source review under #559's
incoming integration policy. It does not widen this checksum repair or add a
new M7 build gate. Existing #528 source/notice/publication holds remain open;
no upstream submission is claimed or newly authorized.

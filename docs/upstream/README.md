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
  for #574/#583/#584; independent native qualification remains open.
- [MD5 one-file contribution and public reproducer](../qa-logs/2026-10-14-md5-upstream-source/README.md),
  owned by #574 and destined for libretro/libretro-common; upstream-only run UNRUN.
- [Steam repair upstream comparison](../qa-logs/2026-10-14-steam-client-repair-source/upstream.md),
  owned by #582 with #564/#579/#580; bootstrap repair remains unimplemented.

The queue also tracks focused Recent-default and Dolphin save-preservation fixes,
and conditional browser/Wi-Fi/capability/dependency candidates. Fork-specific UI
and scanner policy are explicitly distinguished from reusable component fixes.
Historical broad-series and QA-toolkit proposals remain linked without becoming
new RC requirements. The [M7 milestone](https://github.com/pixelelated/distribution/milestone/7)
owns release order; [the dated working list](../releases/next-candidate-work.md)
explains what remains from testing the last device build.

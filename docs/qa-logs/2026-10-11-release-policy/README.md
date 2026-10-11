# Thin RC/release policy — #532

D-WORKFLOW-159 and docs/releases/versioning.md define RC counters, rolling
patch targets, internal dev builds, public tag/title identity and RC-to-release
reassembly. No release, tag or allocation was created by this work.

`tools/build-identity-test` executes actual scripts/image naming, sidecar and
os-release blocks with actual config/build-identity in disposable Git trees.
Synthetic firmware embeds the emitted metadata; actual candidate-store verification
and fork-publish-release planning run against those tiny manifest-bound files.
Host02:57 assertions pass. RC1/RC2 same-day sets, release and next patch names,
metadata and draft/prerelease fields agree. Duplicate outputs retain old bytes;
engineering/unsupported stages, malformed overrides, relabelled RC identity,
wrong checksums, unbound firmware and tampered bytes are refused. Changing
embedded RC metadata yields different synthetic bytes and manifest identity.

Host01 retained an extra temporary etc directory inside the flat candidate
bundle; the actual verifier rejected it. Original21 passing/2 failed assertions
remain recorded. Host02 moves that metadata into its report before bundling;
no product guard or tested assertion was weakened. No VM, full image, physical
USB test, device/cloud operation, external audit or publication was performed.
The counter-allocation and existing-tag gate remains explicit release workflow,
not a claimed network check in the offline planner.

#532's first three policy/host criteria are qualified. The shared #530/#532
next-image metadata and INFORMATION-frame criterion remains open. The existing
#530 frames are historical proof, not new RC/release screenshots. Product UI,
ES source/pin and stored settings are unchanged by this host-policy delta.

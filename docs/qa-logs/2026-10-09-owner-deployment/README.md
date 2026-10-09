# Owner engineering-device deployment — 2026-10-09

#344 owns the approved hardware updates; #519 owns the one-time RG35XX SP
pre-upgrade alignment. This packet contains compact redacted evidence. Personal
filenames, credential/configuration contents and captured owner screens remain
private under `/tmp/pixelelated-device-deploy-20261009/`.

Can this be done on the VM? Software upgrade and cloud-preservation behavior was
already qualified there. These checks require the actual H700 DDR3/DDR4 boards,
Nova boot chain, owner storage mounts and Tailnet return. This is engineering
firmware deployment, not RC/publication clearance or a gameplay/audio test.

## Completed results

All three updates and single reboots are accepted. RG35XX SP finished installed
verification15:24UTC, RG SP15:54UTC, Nova16:01UTC; subsequent preservation and
frame reviews pass. Screens are640×480,720×480 and1280×960 respectively. Every
original stage/reboot result channel is0 and all owners exited. Both H700 units
retain163 protected files each; the Nova protected filter contained0 before
and after, not a claim about all storage. The owner may use all three devices.

`deployment-summary.json` and the per-device receipts bind the results.
`startup-observations.json` preserves inherited frontend/firmware/audio warnings
and the unclassified early Nova SMMU burst. Final boot/render success does not
assert a warning-free journal or physical audio/gameplay acceptance. No further
device mutations are planned; owned screenshots under /tmp expire at reboot.

## Authority and sequence

The owner explicitly approved RG35XX SP transfer, reboot and screenshots, then
approved the prepared #519 alignment/guarded rollback. Its final executor SHA
`4e286b7906d47ef752761442ed294960f6d7ef5b3417f8925f1249024ce676a1`
ran successfully before any update transfer. The independently read actual
acceptance and private seal are represented by
`alignment-acceptance-redacted.json`. All163 protected files, local recovery and
credentials were preserved; only approved path/settings alignment and archival
of stale experimental migration/scan records occurred. No cloud operation ran.

The owner subsequently said: "you have my approval for both devices to both
transfer the latest build and reboot the devices following the transfer" after
the concrete RG SP/Nova preparation proposal. These two devices received only
the approved startup/game-exit auto0 setting change and cached-frontend restart.
Their selected cloud paths and credentials stayed unchanged. The byte-identical
qualified operation core supplied gates, lock, archive and service restoration;
its one-time wrapper did not call #519's cloud-path/scan alignment. Exact old
69e603 settings-writer differences were reviewed against installed files; actual
0644 modes and contents were verified after preparation.

Every mutation used `tools/device-act`. Transfers wrote a new partial outside
the update queue, verified the complete device-side SHA256, repeated the full
accepted live-state binding, then queued the exact file. Each device received
one separately approved reboot with fresh identity, power, quiet-process,
state-binding and full queued-file checksum guards. No gameplay, input, cloud
sync or automation reenable is covered by this evidence.

## Firmware

All deployed images use distribution8b5113fa164ada7d002ab138b1e3a9bf795e9de5
and ES1d76b3da7da75794066df1c089931b890304da7a.
H70002 TAR SHA `b49cca4ca0b8996fa994181508c887d9df5afe155c9502919bab7bf7e153e39d`;
SM855003 TAR SHA `b3f1a8190e04abbf64d35486601ee19fce35d2d25bc7239b1be7cccd9fb43730`.
The accepted immutable bundles and detailed artifact checks are in
[device refresh](../2026-10-08-device-refresh/).

## Preservation interpretation

Protected payload/recovery and credential/cloud-path files retain exact
hashes. Main settings and its last-good copy may be reordered by the real
settings writer. Compare every parsed value, including duplicate-value order,
against the retained original, allowing only the approved auto0 choices. This
is semantic preservation, not byte equality.

All three pre-update rules files exactly matched old default SHA951a7d65…;
new generated rules match exact installed/source defaults SHAa5243acb…. The
post-update hook calls `cloud_sync_helper`; the rules merge is expected.
Preserve the failed overbroad equality observation rather than silently treating
changed bytes as equal. Each accepted device has its own comparison receipt.

## Monitoring and limitations

Each transfer/reboot uses `tools/watch-build-submit`, `tools/watch-build` and
`tools/watch-job`. Terminal receipts consume original inner/outer, wrapper,
runner and launcher results plus actual host process exits. Active session
supervision supplied completion delivery; no off-session alert is claimed.

Remote frames establish compositor output only. No game was launched and no
physical controls/audio/sleep/LED test is inferred. Startup/game-exit automatic
cloud sync remains disabled after update. #528's source/licence and off-host
custody obligations remain open independently of these personal tests.

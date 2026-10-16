# Private RG35XX SP engineering update — October 16 (#344)

The owner authorized the exact H700 transfer and one reboot. Both completed;
the RG35XX SP is ready for private testing on
`0.0.1-dev+20261015T161744Z.g077197e6cd3e`.
This is an engineering handoff under D-WORKFLOW-168, not public RC designation.

## Evidence and scope

- Accepted artifact bundle `a808df3dbffc6281b0bf698fbbbd97a526f16211d1195bcf13ebd5fccb7e3e5f`;
  update tar 1,321,697,280bytes, SHA256
  `e68f5c21b38b298e307fa1f00f87762a9aaeb2348aa91a9d43d940ce11da35dd`.
- Stage `20261016T005220Z-1e0080ba`: host and device hashes match, complete file
  moved from private partial staging to update queue only after state/power checks.
- Single reboot `20261016T005615Z-800bd9a5`: installed SYSTEM, KERNEL, selected DTB,
  DDR4 bootloader, EmulationStation and both RetroArch binaries match accepted bytes.
  Original command/monitor/runner/tool channels are0; recorded owners exited.
- Old boot `d351eba2-431e-4806-b75d-c9d94af476f5`; new boot `067a27f1-143d-4fe8-83cd-937560a5c87b`.
  Tailscale returned, queue empty, original storage mounts and active frontend.
- All 163 protected files/25,549,175bytes and three recovery entries retain their
  recorded hashes/modes. Credentials, selected paths, configuration semantics,
  hooks and service overrides are preserved; automatic cloud sync stays off.
  See [preservation result](preservation-summary.json).
- 126 retained/default systems; no custom GameCube/Wii/Steam mapping. The H700
  package/menu audit applicability remains accepted. No game, injected input,
  screenshot, cloud transfer or manual settings mutation occurred.

Can this be done on the VM? Existing VM/artifact qualification is accepted.
This step verifies the physical DDR4 H700 boot chain, its actual retained
storage and Tailnet return, which the VM cannot establish. No new UI/frame,
physical controls, audio or gameplay proof is inferred.

## Trust, original failures and incidental finding

An initial accept-new SSH attempt was rejected by automatic approval review.
No new host key was accepted: the Tailnet ed25519 key exactly matched an already
trusted 192.168.1.81 known-host entry. All successful reads and mutations used
StrictHostKeyChecking=yes with that existing HostKeyAlias. The earlier
`authorization.md` wording about a first key is superseded by this verified
comparison and the retained receipt. No future trust bypass is authorized.

The first extra read-only mapper stopped on a broken fallback symlink; its
original stderr is retained. The corrected reader explicitly records absent
or broken links. `/etc/emulationstation/es_systems.cfg` contains a build-host
prefix in old firmware and current image staging, while the active storage
link correctly resolves to `/usr/config/emulationstation/es_systems.cfg`.
[Issue 613](https://github.com/pixelelated/distribution/issues/613) tracks the
portable package correction, upstream check and VM proof before a public RC.
The exact deployed image was not changed to fix this inactive fallback.

The filtered boot journal repeats the same BFQ scheduler-path and PipeWire D-Bus
messages retained in the October 11 deployment. No new error class was observed
in the selected error-level readback; this is not a full service/audio test.

## Custody and next work

`originals.tar.gz` holds the selected original scripts, logs, results and watcher
receipts; `originals.json` identifies each source and hash. The compact archive
was independently compared with every selected source byte; `custody.json`
records the count. Full configs, credential values and personal save paths stay
in the mode0700 local owner directory, excluded from Git and public reports.
Private owner: `/tmp/pix-m7-h700-rg35xxsp-deploy-20261016-01`.

The transfer and one-reboot permission is consumed. No runtime remains.
RG SP and Nova retain their earlierbc9d deployment. #607–610 affect their named
platforms/public RC; #613 is next packaging cleanup and #611 remains guidance.
#528 public-source obligations and website #511/#605 remain separate.

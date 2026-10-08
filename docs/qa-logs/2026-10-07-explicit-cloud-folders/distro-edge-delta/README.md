# Folder availability and final-readback correction (#508)

This is a delta to `e484380a3426626d84afa0c5109abeff4512dd0c`. Its earlier source and
sealed evidence remain unchanged. Product-flow decisions and firmware integration
are on hold; this packet covers only the two confirmed setup defects.

An empty carried relative folder such as `GAMES` or `Saves` was incorrectly reported
missing: the availability helper split `qa:GAMES` as if the remote label were part
of a pathname. It now separates the remote prefix before resolving the parent,
retaining the distinction between `remote:Name` and `remote:/Name`.

Final seeding readback previously accepted a provider's partial stdout even when
that listing returned failure. Both direct and parent-fallback controls reproduced
`OK`/exit0 with provider exit3,4,5. Seeding now uses the same status-aware availability
helper; nonempty failed output cannot establish presence or absence. A read failure
returns nonzero and never prints a misleading `OK` or `MISSING` for that folder.
No copying, deleting, pointer selection, or migration algorithm changed.

## Verified scope

- `initial-observations.json`: 11 observations on frozen `67c6f9be…`, including
  successful ordinary backup using a carried `GAMES` setting. New setters reject
  single-level saves choices, but the stored config reader and transfer still
  support these existing values.
- `old-fixed-result.json`: 20 paired controls confirm the old behavior and the
  corrected result for relative/absolute empty directories and direct/parent
  partial listings with exit3,4,5. They use real rclone and injected failures in
  isolated synthetic filesystems.
- `host43-result.json`: all 43 durable regression cases passed with final
  `cloud_setup` SHA256 `a7eea3879848ec4879f279f3b7e2a2c08f3531c970ec4dd9858b09290975265c`.
  `host-new-cases/` retains the 12 new cases' command and data receipts. The rest
  repeat the earlier 31-case suite; their summary and hashes are retained here.
- The home-relative versus absolute namespace controls map two separate synthetic
  filesystem trees through real rclone. They verify argument semantics relevant
  to SFTP; they are not an authenticated SFTP-server proof.
- `package-install.json` records source-equal executable bytes from the real package
  install hook, with no migration engine installed. Syntax, package, rule inventory,
  and diff checks passed. All 12 distro-owned watch processes exited; host fixture
  and staging payloads were removed after receipts.
- The coordinated broad suite passed on the preceding source; its affected
  setup/scan extraction then passed 81 checks on `a7eea387…`. The added late-read
  assertion fails on the immutable predecessor and passes here. That separate
  suite's evidence belongs to the coordination packet.

`guest-check.sh` is the bounded same-guest delta fixture. It checks the exact source
hash and GENERIC_X64 identity, requires the interface stopped, and uses a fresh
synthetic local alias. It preserves/restores the configured sync file, leaves the
configured provider credentials untouched, checks four empty-directory cases and
six failed-listing cases, and removes its temporary profile and payloads on exit.
The UI owner completed that proof under watched owner `/tmp/pixelelated-508-ui12`
at 18:51:08 UTC, with launcher, inner command, and wrapper return codes all zero.
`final-edge-guards.log` records all ten checks and the installed `a7eea387…` hash.
`edge-provider-unchanged.log` retains the configuration and original synthetic
WebDAV-file hashes; the runner compared them before/after and asserted removal
of the temporary profile and fixture payload. `final-edge-ordinary-seed.log` then
records normal seeding with four `OK` paths and exit0. `guest-result.json` binds
those assertions to the coordinated runner. No personal device or cloud is involved.
The UI owner retains full watcher and later guest-retirement receipts separately.

These are source-overlay and package-staging checks. They do not establish final
firmware inclusion or authorize integration while the product-flow review is held.

## Held product-flow limits (#510)

The draft still has a player-visible `TIDY UP YOUR CLOUD FOLDERS` warning in
`cloud_backup:1454` when settings/content sit inside saves. Public ROCKNIX
`20261001` uses `/GAMES` and `/GAMES/backup`, so this can concern the actual
adoption baseline. This packet does not claim every TIDY reference is gone.
`backend-selection.md` records the independent content setter, the combined
saves setter, fixed child folders, and restore fallback outside the selected
root. These are design-review inputs; this narrow fix does not decide them.

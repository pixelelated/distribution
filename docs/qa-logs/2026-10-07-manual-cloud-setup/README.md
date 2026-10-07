# Manual cloud setup draft qualification (#508)

Final draft evidence sealed on 2026-10-07. All owned QA guests, endpoints and
large scratch files are retired. No test or build is running from this packet.
This is source/overlay proof of held drafts, not final validator qualification,
public ROCKNIX image-adoption proof, firmware inclusion or RC acceptance.

D-CLOUD-175/176 removes cloud-folder relocation from setup. D-CLOUD-177/178
makes #510's category-validator/action contract the current prerequisite for
#508 reconciliation/integration and #507 audit. The direction is chosen;
implementation gaps remain in `docs/pixelelated/cloud-folder-flow-review.md`.
New device builds remain held. #511 is separate parallel site planning.

## Evidence and exact scope

- Distribution draft3268015c185b04a17e756829ee116c664d679b4e, local and clean
  at `/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders`. Final setup
  SHA256a7eea3879848ec4879f279f3b7e2a2c08f3531c970ec4dd9858b09290975265c.
  Earlier e484/67c6 evidence remains labelled by its source. The separately
  retained distro packet is `docs/qa-logs/2026-10-07-explicit-cloud-folders/`
  in that feature tree: initial318 checksums/28 source entries and94 edge
  receipts were independently checked. See source-readback.json and
  edge-readback.json here; host43, paired20, guest10 edge checks + seed0 pass.
- `es-ui/` binds local clean commit300f97d28a072b916c54dcbf108f1440e7253761
  to compiler, catalog, screen, source and cleanup receipts. It records178
  cases/1886 assertions and the actual setup/chooser/startup checks. English
  intro truncation at1280×800 is explicitly unresolved, so visual acceptance
  is incomplete. Failed/stale-fixture frames are not approved final frames.
- `broad-harness/` records1303 main PASS, no FAIL/SKIP and13 ordinary archive
  cases against pre-edge e484/67c6, then81 affected checks against finala7ee.
  It does not claim the full broad run repeated on finala7ee.
- `qa-routing/` records9 host-only controls for retired-suite refusal, exact
  historical --ref recovery and the explicit13-case archive allowlist.
  `held-qa-tools.patch` preserves the source adaptations, which are not yet
  integrated on next. In particular cloud-round-trip uses the held product's
  new folder-state contract; do not run it against old installed source.
- `final-packet-readback.json` records root's1031 ES evidence checksum checks.
  Root also checked10 final ES source hashes and the distro/harness hashes.

Final guest1235151, endpoint863920, cleanup launcher1295516 and broad
controller/command/watcher1062185/1062214/1062186 are absent in host context.
The guest disk, QA keys and compilation scratch are retired. The earlier
PID860697 was superseded by the later resized guest and is not a live owner.
Accepted candidate16/H700/SM8550 firmware remains unchanged.

Root coordination publication contains documents and receipts only. The seven
QA-tool adaptations and draft cloud-sync-changelog remain held with the
unintegrated product source; the patch here preserves their exact state.

## Historical scope correction

Submitted ROCKNIX/distribution PR3404 head4c83ebede4 and ES PR40 sourceca300dd41
already contained an optional tidier, before the hard fork. It could move
content from derived paths, and a recovery branch used a /Content suffix as
an old-layout heuristic. Custom-layout guards did not establish user intent
universally. The original ES label emphasized saves/settings. Both PRs closed
without merging. #510 is now the current validator/action contract before #508 integration
and #507 audit. The owner selected D-CLOUD-178; website guides are separate #511.

#509 tracks eventual cleanup of active Rasteratops helper/document names.
Historical paths and receipts keep their identities. No personal Dropbox
credentials or data are included in this packet, and no owner-cloud migration
was retried by these tests.

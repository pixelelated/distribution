# Selected clean-state gate: runtime qualification

Refs #565. Source45d899bdf3371937dfd494bc0a43e50ea1c4871e, integrated
cc0f8b0aa743f7e83db07317e162fcdf9b7bbc93. No owner account, handheld, provider,
cloud folder, game save or metadata was changed. No release was published.

## Results and boundaries

1. Original63e candidate on a fresh VM20: first-boot gate returned2 with one
   parser error and one prohibited-state report. Readiness passed. Actual
   `/etc/retroarch.cfg` is comment-only, and cloud_log_scrub writes the exact
   two-family zero-work startup marker even on a clean install. Neither finding
   is evidence of copied owner data. Original68synthetic root controls passed,
   exposing missing real-default coverage in that initial fixture set.
2. Correctedab47: same fresh guest's selected roots remain unmodified; no account,
   SSH key or storage fixture was staged. Actual first-boot/--require-ready
   inspection PASS0; all selected account/remote/history checks clear, startup
   scrub marker accepted only with zero work in the inspected root's current
   boot interval. Expanded113synthetic-root controls PASS0 in5.90seconds,
   stderr empty; synthetic trees lived only in guest/tmp and were removed.
3. Additional host payload controls initially returned2: empty native ext4
   lost+found has exact `/0/000000/0/0//0/` unused directory slots, which the
   reader incorrectly refused. The separate synthetic32MiB filesystem receipt
   confirms debugfs1.47.2 output. Two diagnostic copies locate the assertion;
   their results are failures, never qualification passes. All channels and
   exits consumed, temporary files removed. Production error reports still
   suppress values and tracebacks.
4. Corrected final gate and fixture bytes were frozen by independently reviewed
   Git blob before the producer completed commit metadata. Final commit binding
   proves those exact bytes match. All142root/payload/release-preparation
   controls PASS0 in10.22seconds; maximum sampled scratch188178432bytes,
   scratch empty afterward, all watcher/launcher/wrapper and host PID exits
   consumed. Eleven reader-response controls explicitly use a synthetic
   debugfs shim; native clean/dirty ext4/image controls run separately.

The final source change after actual guest proof affects only `empty_ext4` in
the gate AST; the first-boot path is unchanged. This is composed source-bound
qualification, not a claim that a second guest ran the final file verbatim.

The release helper now reads actual final assets during `--prepare` and refuses
unsupported/unreadable/malformed inputs or prohibited selected state; it never
publishes. Tests exercise that integration using synthetic candidate bundles,
not today's accepted real firmware archive. A future candidate must still
pass its actual final-payload gate, ready clean boot and genuine retained-
storage upgrade. Synthetic retained-state allowances prove no mutation by the
checker; they are not an OS upgrade-preservation rehearsal. This policy is a
selected-surface check, not a general or whole-image secret scanner. Explicit
coverage and exclusions are in tool output and the source packet.

## What is checked

Selected system/ES/RetroArch and standalone account fields, recovery siblings,
known compiled service-identity patterns, rclone connection/selection state,
cloud device identity and activity cache, selected gamelists/Recent history,
RetroArch playlists, known QA/proxy residue and empty install-storage seeds.
Required malformed or unreadable input refuses. Service identity is separate
from player identity; successful parsing is not permission to reuse a provider
credential. Logs explain operation stamps without proving a transfer or actor.

Meaningful corrections include exact shipped locale links, Dolphin ApiToken,
melonDS's exact null defaults, literal SquashFS filenames, comment-only upstream
RetroArch defaults, strict first-boot scrub state and valid retained partial/
reordered scrub histories. A preseeded scrub marker always blocks clean-image
mode. Only the exact canonical unused ext4 slot is skipped; malformed/named
zero-inode entries, missing dots and real entries beside slots refuse or block.

## Evidence and lifecycle

The two `classification*.serial.gz` files preserve the exact serial bytes,
including CRLF line endings. `serial-storage.json` binds their original and
compressed hashes; decompression was checked byte-for-byte. Compression only
changes evidence storage, not the test or its result.

`source*.json` bind guest revisions; `first-boot*-report.json` retain original
failure and corrected pass. `controls*-result.json` bind guest controls.
`pix565-payload*/` retain original failure, diagnostic location, native listing,
final142-control pass and final commit binding. All fixtures use synthetic
values. No real credential value or credential-derived hash is emitted.
`run-*.py` and `retire-state.py` are archived coordinator harnesses with original
owner paths; do not replay them. A new experiment needs a fresh owner/allocation.

VM20 image hash was checked before expansion by the captured boot runner;
guest ES/libc hashes and kernel are in actual-identities.txt. The VM used4vCPU,
2048MiB,640×480 and a16GiB disposable disk, no owner image/storage seed. The
first untouched gate preceded every fixture; later synthetic tests used/tmp
only. Original guest script and serial runner emit actual gate result markers.
Retirement consumes all five original channels, stops exact QEMU2650452 and
removes disk/UEFI; ports10577/5962free,2,244,313,088allocated bytes recovered.
No SSH key was provisioned. No VM or payload-test job remains active.

Host-reader rationale and bounds are in payload-plan.md. Host had all required
utilities except mcopy; the accepted read-only frozen build toolchain supplies
mcopy4.0.49 (binary hash in final result). No dependency install, root mount,
network request, cache mutation or firmware build occurred. This host program
qualification supplements, rather than replaces, the guest runtime proof.

## Still open

Nova account/metadata original entry remains unproved; see the adjacent
memory-state-followup/nova-provenance.md. Real candidate image inspection,
retained-upgrade preservation and the broader #565 acceptance remain open.
Keep legitimate device state during upgrades. Do not reset or clean the owner's
Nova to manufacture a clean-install result.

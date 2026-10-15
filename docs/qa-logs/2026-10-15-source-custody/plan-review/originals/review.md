# Finite #528 proposal review

No actionable source defect or blocker was found in the three minimum collector changes or the proposal's historical/current provenance claims. This is a focused local source/evidence review, not an external audit, runtime qualification or publication clearance. The executable final binding/lifecycle derivative is outside this review except for confirming its two collector templates match the reviewed proposal bytes.

## Reviewed changes

1. `collectors/source-inventory.py:170–178` derives the rclone binary directory from the hash-checked recipe version and requires the unpacked root to agree. Frozen `source-f863/projects/ROCKNIX/packages/network/rclone/package.mk:7,36–58` declares1.75.2, selects arm64 for aarch64 and amd64 otherwise, unpacks that exact nested path and deletes its ZIP. The mapper preserves the missing-ZIP custody limitation and does not import old embedded-module or modified-binary claims. No defect found.
2. `collectors/source-inventory.py:52,74–80,103–113,125–135` includes idtech's explicit source name, validates declared version and normal checksum stamp, requires one cache member with the pinned ff35cde0 hash, and requires staged and installed archives to match that same hash. Frozen `source-f863/projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk:5–11,26–39` supplies the exact source name, immutable4cb65b68 URL and normal copy path. The existing Doom game-data publication hold remains. No defect found.
3. `collectors/component-map.py:62–64` changes only the no-install-stamp disposition. Such rows are retained and explicitly may represent build-only, static or vendored work; they no longer exclude shipped work merely by stamp absence. Recipe lookup, inherited recipe hashes, source classification, missing licence list and publication_bundle_complete=false remain intact. No defect found.

The proposal source helper is based on exact accepted attempt04 bytes (also identical to attempt03), and its component helper is based on exact attempt05 bytes. All existing function ASTs are unchanged; the inspected diff is limited to the three described changes. Candidate identities: source-inventory84b9d6dfaf61b31d554536f88ee60f186da5589ea4602b9f475b8e0d82124efe; component-map2ebab5ad2f042becb395297942ace63af2f781873d3ef878d754bd09ed5b4973.

## Schema and provenance boundary

`invocation-plan.md:28–48` correctly identifies the VM schema: six product hashes in build-inputs11c9cb3d, no source_cache field there, and artifact-inputs7c3f497b binding actual outputs. Full source maps must be explicitly derived from f863 and the source-cache location must come from original custody. The retained VM result/input closeout objects agree: qualificationfalse, original launcher returncode null and failed-investigated/reporting-failure. Independent artifact integrity does not supply a launcher zero.

`invocation-plan.md:77–85` correctly says the historical runner is a template with an old bundle-input equality assumption, not executable current binding proof. Author has separately identified the actual H700 reader-input/ARM-manifest shapes and supplied source-cache provenance for the new draft; those new lifecycle/binding checks require their own review. No finding is inferred merely from this explicitly UNRUN plan retaining historical interfaces.

`invocation-plan.md:125–157` preserves recursive source identity, raw symlinks, source/member manifests and separate ABL/rclone/notice holds. Historical2327 rows, prebuilt versions, Teakra non-use and old404 are not promoted to current results. The17 corrected notice rows plus separate Doom row all retain publication_clearance=false. No legal conclusion is drawn by this review.

Remaining dependencies, in order, are existing prerequisites rather than newly discovered defects: finish/consume SM8550 and bind all five actual inputs/output results; review the fresh runner/binding/member-index derivative and allocate the finite collector job; then retain exact additive source/notice members and qualify retrieval/off-host custody. Historical profile counts and proposed time ceilings remain non-results. The committed proposal is accurately labelled source-only.

## Evidence checked and limits

The committed archive719cc280 was read directly and all125 regular members matched the original sealed packetf345980a. All21 referenced originals matched their recorded hashes. Independent Git object reads confirmed both historical73-path deltas, all four changed PKG_VERSION declarations,30 current recipe records and135 selected package-directory blobs. The original2327-row member-map hash and VM schema/closeout were checked. `readback.json` records these observations.

No collector or preparer was imported or executed; no cache traversal, network, firmware, target, VM, container, registry or shared-file mutation occurred. This review does not establish current cache availability, current installed/profile membership, full corresponding-source completeness or source/licence clearance. The two historical collector outputs and notice evidence remain historical.

An initial reviewer-only readback script stopped with FileNotFoundError because it guessed the new draft helper subdirectory as collectors rather than templates. Correcting that reviewer locator allowed the same bounded source/record readback to complete0. This was not a collector failure; both observations are retained in execution-observation.json.

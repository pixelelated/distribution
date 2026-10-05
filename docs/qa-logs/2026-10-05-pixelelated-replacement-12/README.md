# Replacement12 preparation — not image qualification

Frozen distribution55d8ee8f75965a560f75d187e34c9beaa93133f1, manifest
bfdcf9b2655157b7e4d3a59f1c6fa803f68989b2cfb8b460eb0f2a666ee98192:
6549product/202QA/180symlinks. Only the two proxy/CHD recipes and reviewed
schema-pin comment differ from qualifiedreplacement10. ES/splash/container
and24/4 concurrency are unchanged. Pre-freeze schema guard passes (#452).

Full freshness03 actually completes22:26:40/allthreeproducedrc0; actual993074
22:27:12 observes allfourprocesses absent. No outer channel was produced.
All1608recipes and the exact freshness tool verify before/after. The earlier
freshness01rc1 and subsequent02rc0 retain their own inputs/results.

The independentreplacement11 cache copy is still in flight at this preparation
checkpoint. No build12 or VM owner has executed. The sealed adoption requires
that copy's terminal/cleanup/checksum/inode receipt before an atomic same-volume
rename of the unbuilt independent root; it then rechecks complete checksums.
The original frozen11 source and failed schema guard are preserved, unbuilt.

Prepared fresh owners: image13 → defaults/actualRC2 QA15 → installedproxy12
(includes upstream native-format tests against the actual installed library,
no skips) → subset09 HTTP reconnect. Exact guards/inputs/assertions are retained.
These are preparation artifacts, not PASS results. Account/P4/H700 gates remain.

The full inputs.json remains at the sealed build owner and will accompany the
immutable candidate bundle. Its digest/counts are in freeze-receipt.json here.
The normal credential hook rejected two upstream patch filenames in the full
mapping as credential-shaped; keep the original manifest intact outside Git
and publish its verifiable digest instead. No hook exemption or bypass used.

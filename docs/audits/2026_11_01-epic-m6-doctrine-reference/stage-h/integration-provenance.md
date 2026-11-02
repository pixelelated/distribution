# Stage-H integration provenance — 2026-11-02T19:15:01Z

The owner explicitly named coordinator 329011b9eae20922b4d0727e13bf1626b2e1c04f. E/F/G were ready at ad5516f6603509954d241e62585b22d32402b03c; merge 24a5e0e294607bc6fc99025873cb063d26c9a4da preserves both complete work-log append sequences and regenerates INDEX. The initial full harness passed 12/13: its untouched history scan attributed 113 imported coordinator paths to T39.

The audit-local checker now accepts optional --coordinator-tip for that exact hash only. It refuses a different tip or a commit that does not descend from it. The untouched step excludes only commits reachable from the authorized coordinator tip, and independently requires every non-owned final path to match that coordinator tree. This prevents a merge resolution from hiding an unrelated lane edit. Original default mode, the 13 steps, --since 86ebb6dffc and all original refusals remain. No production tool was changed.

provenance-controls.json records two new refusal cases (rc=2), an isolated post-merge lane edit and an isolated merge-resolution edit of docs/reviews/order.md (both rc=1, untouched FAIL), then the real merged artifact with findings withheld (rc=0, 13/13). Synthetic objects used an isolated Git index; no source checkout or branch was mutated by them. These controls exercise only the new integration behavior. Accepted A–D receipts are unchanged.

source-after-merge.json verifies all 48 owned source hashes against Stage F. host-census.json counts zero T39-authored host lines. Exact receipt whitespace is preserved in JSON companions where a readable .txt view is normalized. The exported source trees are retired after final verification; retained receipt paths and commit objects are sufficient to reproduce them.

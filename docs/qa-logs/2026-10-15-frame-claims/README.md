# Screenshot claims and comparator correction — #591

The original fac608ff VM report remains failed. A separately watched host
continuation, `20261015T002234Z-faf6a7c9`, passed the old-checker negative control,
all 20 candidate controls, and all 78 retained-frame comparisons. Original
child, command, watcher and runner results are retained. No new VM run, baseline
replacement or mask change occurred.

The comparator now attributes each actual changed pixel to its first matching
live claim before clustering unexplained differences. Adjacent claims therefore
work together without accepting the gaps between them. The controls retain
failures for uncovered foreground/gaps, stale or wrong-screen claims, missing
frames and size differences; original negative child statuses remain nonzero.

The 348 added claims name exact screens and exposed backdrop regions affected
by #578's corrected empty Last Played default. Source, theme identity, reviewed
frame pairs, per-frame hashes and diagnostic limits are in `review.txt` and
`pixel-inventory.json`. The Last Played carousel artwork shifts the surrounding
background; no modal text/control interior is newly covered. Existing claims
and masks retain their original scope. Root reviewed the source correction and
representative before/after frames. This is not a claim to have manually viewed
every frame pair or to qualify any previously masked behavior.

`continuation01.md` reports 389 claimed regions, zero unclaimed and zero missing.
The original failed report remains in the baseline02 evidence packet. Original
sources, controls, per-child outputs and watcher records are archived losslessly
in `original-packet.tar.gz`. Runtime images remain in their original baseline
export; frame hashes provide the exact-source index for these added claims.

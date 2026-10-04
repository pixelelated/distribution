# Exact candidate extraction — #344/#383/#418

The first same-tree parallel attempt (image-01) was refused by the watcher
before execution; its receipt lives under replacement-01/image-concurrency-refusal.
After qa-02 completed, image-02 failed on a missing ES_SRC before extraction.
Its original rc1/log remains in attempt-02. image-03 supplies the pinned ES
checkout explicitly. Its initial separate preflight from the feature cwd was
correctly refused; rerun from the actual frozen cwd passed before launch.

image-03 run20261004T171722Z-0c6a3fd1 finished17:17:32 UTC. All command, inner,
outer, watcher, wrapper and actual tool session44613 results0. Actual host
readback confirms its runner/watcher exited. Candidate custody and frozen
source checks pass before/after. The raw image GPT first partition starts at
sector8192; its SYSTEM matches the update tar SYSTEM exactly, SHA256
8f034d028da6c1afb404670e2aac27348aa785f23a21372022b048ff41fac841.
Non-root extraction created57034 files,2662 directories,1345 symlinks,258
hardlinks, no device nodes. No image binary was executed.

Analysis root: /workspace/tmp/pixelelated-m7-image-03/root. The extracted
usr/cache/shadow had mode000; only that owned analysis copy was made0400 so
a complete scan could read it. Original mode is retained in the receipt; no
contents were printed and the immutable image/runtime remain unchanged.

All1038 brand-bearing files exactly match the inspected staging bytes. This
confirms416/417's actual artifact scope; it is not yet a completed brand or
secret classification. Preliminary staging discovery files remain under /tmp;
use the canonical checkpoint for the remaining source/artifact checks.

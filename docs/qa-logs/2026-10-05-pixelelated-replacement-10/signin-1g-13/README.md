# Installed Pixman 1GiB sign-in qualification

Frozen source d6e8390c93, immutable bundle1c69bcf5. The example.org baseline page
loads and remains responsive for the original30second measurement in a guest
with actual QEMU1024MiB and firmware1GiB. Linux usable memory is recorded
separately (810372KiB). Installed service selection proves
Pixman, with no runtime renderer override. The actual loaded640x480frame was
directly reviewed and the kernel journal contains no OOM event.

Peak measured combined RSS: 271416KiB. This records the
observed workload; no arbitrary numerical RSS ceiling was added. Baseline
and provider workloads are different and do not establish like-for-like growth.
Public login is not authenticated Dropbox trust proof.

Durable completion 2026-10-05T20:57:32.868021+00:00; all four result channels0.
Actual cleanup verifies all5 owner/guest processes absent
and no QEMU. See completion.json, visual-review.json, artifacts/resource-budget.json,
actual-gl.json and guest-physical-memory.json. Refs #447, #362.

# H700 retained-output reader source custody

This compact archive retains the exact sealed source packet from `/tmp/pix-m7-h700-reader-review-20261015`, including the corrected SM8550 subtree, original source/failure evidence, diagnosis, static observations, proposed #555 criterion, and all source seals. The original top seal is `a21f13162120c1d856652fd5ff8a509f84f8a75a039c9ce7a9d17d4040933870`.

The archive has 173 regular files (172 sealed payload files plus their top SHA256SUMS) and 16 directories. `member-manifest.json` records exact membership, file bytes/SHA256, permission modes, UID/GID and nanosecond mtime. Every archived member was checked against the original with `stat.S_IMODE` permission comparison and decimal PAX timestamps; source bytes and metadata were rechecked unchanged afterward. No links or special files are included. Archive paths are relative to the source packet root.

The packet corrects explicit H700 versus SM8550 GStreamer package expectations and prepares fresh read-validation and independent firmware acceptance for already assembled H700 outputs. The original combined producer1 remains failed-investigated and consumed. The archived README preserves the exact scope and pending execution dependencies; the source review metadata predates root's final prepare/commands clearance, which was received before release. No source, preparer, admission, compiler, firmware, cache, VM or target runtime operation was executed or changed during this custody task. Active owner results belong to root's separate original runtime evidence and are not asserted here.

Outer SHA256SUMS binds this README, member manifest and archive. No disk image, full cache or private configuration is included.

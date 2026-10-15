# Upstream queue reconciliation — exact source and publication custody

Root applied the reviewed additive #585 body and canonical `docs/upstream/README.md`
append after checking the expected before hashes and issue updatedAt. The original
publication receipt records `2026-10-15T05:32:28.925550+00:00`; its before/edit/after
commands all returned0. This retention step performed no issue edit, upstream
submission, native test, build, cache operation, or change to the canonical doc.

`originals.tar.gz` contains exactly39 original regular files:

- `source/`: all29 original source-packet members, including its seal
  `d1cb66fda979b09bc5471318d2fffe6b8053411f8a6303a776610cdae87032f3`.
- `publication/`: all10 original before/edit/after stdout, stderr and exit files,
  plus the original publication receipt. No channel was synthesized.

Every archived member was read back without extraction and matched to its original
bytes, length, mode and uid/gid. `member-manifest.json` records the original paths,
hashes, modes and source timestamps. `publication-receipt.json` is a byte-exact
convenience copy. No native archive, image or mutable cache is included; originals
remain unchanged. The outer `SHA256SUMS` binds this compact retention packet.

Verified published issue body SHA256:
`7cb7afa3d159ebd697aeab7f49ff5c3bfae8e32560e7f8d9b7b73334dcf83070`.
Verified canonical-doc SHA256:
`a0a4cf53c9d97e566d69204e38f2f38d9c3c9d1dd29edd940d2bfa772d7fb25f`.
The retained before and after issue bodies equal the source packet's exact proposed
versions; the local canonical doc equals its exact prepared append. This proves
queue/doc publication, not an upstream contribution submission.

Scope is completed #574/#575/#584 and audit fixes #593/#594/#595. All six already
had queue coverage. The addition clarifies the separate RetroAchievements/rcheevos
owner for the disc-reader correction already included under #574, preserves focused
patch boundaries, and updates accepted local evidence without duplicate priorities.
The original #597 reporting failure, account/award limits, conditional upstream
adoption, and absent x64 ARM Steam payload remain explicit. Existing #168 ownership
and milestone order are unchanged. Current-upstream/duplicate checks and explicit
posting authority remain prerequisites for eventual submission under D-WORKFLOW-165.

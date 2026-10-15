# SM8550 source handoff custody

This compact archive preserves only the released source packet from `/tmp/pix-m7-h700-state-resume-20261015/sm8550`, sealed `fb8c6628e10c844ea8eda74d6965e89032da259bbc074e42c8426886b113c16f`. It includes the executable delta, exact H700 acceptance prerequisites, the separate host checker, original source references, historical source seals and source-only static observations. No firmware, cache or new runtime output is included.

The archive contains 127 regular files (126 sealed payloads plus their top SHA256SUMS) and 15 directories. `member-manifest.json` records exact membership, file bytes/SHA256, permission modes, UID/GID and nanosecond mtime. Every archived member was compared with its original, including permission bits through `stat.S_IMODE` and timestamps through exact decimal PAX values. Source bytes and metadata were checked unchanged afterward. There are no links or special files; archive paths are relative to the source packet root.

The handoff binds actual H700 acceptance `e8107b4bffac81fa72dd127a45ec1b6b7455518829f04c143690ec60687813db`, run `20261015T064734Z-8868082e`, normally consumed admission `4ebc249f9b7d4e9a8c61cff36cc23fea`. Earlier combined-producer1 and selected-state-acceptance1 remain failed-investigated. The SM8550 prerequisite requires the new original zero channels and consumed receipt, rather than merely its PASS summary.

Checker `65ab515ec2c0ccdf474f08128cabf1dea774846a8add3725cd05d334b2e1eba6` is copied and sealed separately for host artifact acceptance, with original 212-control host-suite provenance. It does not change frozen firmware/source `f8636de1d105275dbf9420bbabbbc26f79abb10f` or replace the checker in that checkout/image. The existing canonical cache/build/ordinary consumption, host gateway, GStreamer device profile, FEX and ABL checks remain unchanged as documented by the packet's source diff and static record.

The archived source record predates root's subsequent checkout/preparation activity. No preparer, admission, compiler, firmware reader, cache operation, VM, device or target executable ran during this custody task. This record makes no SM8550 compilation, firmware acceptance, physical boot, RC or publication-success claim; actual outcomes belong to root's separate original run evidence. `pre-actual-binding-draft/` and inherited prior records remain explicitly historical inside the archive.

Outer SHA256SUMS binds this README, member manifest and exact source archive. Root owns integration and publication.

# New final generator input controls — 2026-11-02T19:31:43.724913+00:00

Authority: D-WORKFLOW-228, full #688 comment 6586375296 and coordinator 10e055e3043b7bd41f9dcca3e04abce9d979817e, docs/qa-logs/2026-11-02-m6-resume/t41-generator-input-ruling.md.

Historical Stage-C negative input identities are unavailable; these are new controls only. No old fixture bytes were read or inferred. Accepted formal program, selected source modes/blobs and A–D receipts are unchanged. No application, extraction or whole-stage replay. Actual Codex / GPT-6-Astra / xhigh, T3 wN:p6; observed identity, not provider-attested.

Builder SHA256: c0a3559eb5d1f2b0149664b6f7462f114f0ec88ab6e4f9574e25ef6907436363. Producer command: python3 /workspace/tmp/m6-t41/tmp/run-final-control.py, cwd /workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688. The sealed copy is run.py. It refuses existing nonempty output. Validation consists of run.py deterministic input assertions, all 107 immutable mode/blob comparisons, complete single-file overlay membership and the four exact argv/rc/output assertions in manifest.json. Result: PASS. Negative exits 1/1/1 with the exact required final assertions; positive exit0, empty stderr and stdout byte-equal to retained stage-c/tables/stats.txt. No other generator mode or call ran.

Complete sealed file list (this README included):

- README.md
- fixtures/bytes/projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches/0001-Update-dram_sun50i_h616.c.patch
- fixtures/drop.json
- fixtures/reach.json
- manifest.json
- outputs/drop.stderr
- outputs/drop.stdout
- outputs/header.stderr
- outputs/header.stdout
- outputs/reach.stderr
- outputs/reach.stdout
- outputs/stats.stderr
- outputs/stats.stdout
- run.py
- source-identities.json

All manifest artifact paths are relative, with no symlink or parent traversal. Input modes are 100644. Git bytes, not extracted source, supply the single overlay. Future acceptance reconciles these records; it does not rerun this builder.

This is the corrected second four-control attempt. The first attempt passed generator assertions but failed filename-serialization publication hygiene. Its packet is preserved losslessly at ../generator-input-proof-attempt-1, with the original two row inputs explicitly base64 encoded and hashed. D228 permits this recorded implementation correction; each attempt ran only the four specified controls. Historical C inputs remain unavailable.

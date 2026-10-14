# Candidate proxy product integration — 2026-10-14

**Source integrated; runtime acceptance pending.** This change extends distribution composition `4eb90eb648c29066030d8d2e7ce9067f83ade85c` on `feature/m7-candidate-compose`. It changes exactly three product paths: the scanner and two new package patches. It does not close #583, #584 or #588, and it does not establish installed-image acceptance.

The existing 16 package patch files remain byte-identical. Their numbering ends at 019, so the new files are `020-rvz-padding-preserve-partial-word.patch` and `021-flush-reconnect-during-startup.patch`. Both are the exact uncompressed packet diffs, applied in normal filename order. No package recipe, source pin, native build function, dependency recipe or ES pin changes.

Selected immutable inputs:

- RVZ decoder and scanner: `22cfb2385acce6d9c20b20d2f7f40970808777b3`, `docs/qa-logs/2026-10-14-proxy-rvz-revision-source/candidates/`.
- Startup handoff: `77901d054ed062a6312d5b5efcc023088907fa48`, `docs/qa-logs/2026-10-14-proxy-startup-race-internal/startup-handoff.patch.gz`; checked equal to the coordinator copy.
- RAOfflineProxy archive pin `c7ebd1b6e777f3751ff0ecdf8aba54045844e00d`, SHA256 `88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b`.

The fresh small preparation at `/tmp/m7-proxy-product-source-20261014-01/tree` extracted only the 112 package/test Python files from that archive. SHA256 was streamed and extraction performed on the same open archive descriptor, with unchanged before/after fstat identity. All 18 package patches applied with `patch --batch --fuzz=0 -p1`; any original offsets matched the already accepted preparation transcript exactly. New patches applied without offsets. No direct candidate replacement was used in this preparation.

Every resulting Python file matches the manifest and actual bytes in `/workspace/tmp/pix588-candidate-prepared-20261014-01/tree`. Exact resulting SHA256 values:

| Source | SHA256 |
| --- | --- |
| `rvz_datasource.py` | `b0d28c147c24c0e6909e8e754915ab4323d766b7fbd711b16c2ce949bd8f3407` |
| `proxy_service.py` | `432bb07ac6b0abcdcb38800d7c75a92c768b2b6bea583a1bab6834bb7f7b0d00` |
| `raofflineproxy-ctl` | `47391a3bbcaa0f2262cdee12f09bd48d17f7fedf0237a1a661a21b085b2f71f7` |

`source.json` preserves all 18 original patch results, all 112 hashes, reference manifest identity, unchanged recipes and static-check results. Python 3.10 AST parsing passed for all 112 files and both scanner heredocs; scanner `bash -n` and `tools/pkgcheck raofflineproxy` passed. Full staged whitespace checking reports only standard single-space blank context lines in the two exact unified patches; the check excluding those two patches passed. No source module or fixture was imported or executed, and no bytecode was generated.

The coordinator owns the original #588 baseline/candidate service and component results and their acceptance. Packaging parity allows those exact candidate source results to be assessed without substituting a different repair. Final ES integration, actual image payload/native loader closure, clean/retained storage and combined runtime qualification remain separate. No build, compiler, VM, service, device, shared-record edit, push or external post occurred in this work.

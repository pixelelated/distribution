# Corrected Stage-B packet — complete source-application evidence

Recorded 2026-11-02 17:42:20 UTC. Source `02aab33bd9842610b0d466c9c186454dc14373ee`; method D-WORKFLOW-222 at coordinator `4c8a118cfb4efa8d13c1b41b72ef7a205da5f766`, #688 comment 6583428757. The original packet one directory above remains historical and unchanged.

- `apply-corrected.py`, `run-metadata.json`: source hash, actual GNU patch/tar versions, locale, exact start/end and fresh scratch root.
- `application-results.json`, `rows/`, `logs/`: all 120 rows / 106 patch paths, both command results and output digests, input/output tree digests, explicit promotion; 43 applies, 48 offsets, 29 fuzz; zero true failures or blocked production rows. H700 011 is the sole diagnostic disagreement.
- `failed-candidate-guard.json`: actual partial failure, unchanged prefix, no promotion, blocked successor; same engine as production.
- `tar-*.json/out`, `targets-*.txt`, `order-*.txt`, `archive-sha256.json`: exact extraction/order, every missing target accounted for as created, archive/sidecar/recipe equality.
- `source-readings.py/md`, `source-readings-commands.json`, `path-metadata.json`, `remaining-reads.py/json`, `0010-final-function.txt`: source/history commands and targeted analysis; no source helper executed.
- `t41-tables.py`: Stage-B draft derived from T40's asserted schema, with corrected applications and three FAIL-first mutations. `inventory-rows.json` derives from retained P1 TSV; table outputs and stats are checked here. Stage C promotes the formal tool and reader plan.
- `generator-fail-first.json`, three failing outputs: membership, reach and header positives before successful modes.
- `issue-688-body.txt`, `issue-states.json`, coordinator method/register excerpts: exact current contract and scope context, not implicit product acceptance.
- `verify-packet.py`, `validation.json`, `hygiene.out`: final Stage-B artifact checks and positive hygiene controls, including byte equality of all 329 earlier receipts, 107 source paths, every normal-output hash and all retained candidate tree digests.

`02-forward-audit.md`, `03-retrospective.md`, and `04-analysis.md` at the audit root are the complete Stage-B reports. No final slice closure, runtime/boot claim, bug filing or Stage-C/D completion is implied. Committed path text retains the literal `\u002d`; comparisons/source access alone decode it. Scratch remains under `/workspace/tmp/m6-t41/src/` for Stage H retirement.

Read-display formatting: `source-readings.md`, `0010-final-function.txt`, and the excerpt in 02 expand tabs to eight-column spaces and omit trailing whitespace. These are numbered presentation copies; immutable source blobs and raw-command stdout hashes in `source-readings-commands.json` remain authoritative. No application output or receipt from the original packet was transformed. The initial validation did not cover then-untracked files; staged diff found display whitespace, corrected before publication. `validation-initial.json` / `hygiene-initial.out` preserve that first check; `whitespace-correction.json` records the correction, and the final validation explicitly diffs the whole checkpoint against `3cd9ca140a`.

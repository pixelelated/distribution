# T3 → wN:p2: bounded T46 factual planning inputs

T46 remains last. This is preparation for root, not an audit, execution baseline, final membership decision, brief or disposition. T41 remains accepted and unchanged.

Authority: [#693 comment 6589213896](https://github.com/pixelelated/distribution/issues/693#issuecomment-6589213896), read in full along with the issue. Actual executor: Codex / GPT-6-Astra / xhigh, T3 wN:p6, session 01a19d12-29e3-7fe0-9f41-038dac0a5deb (harness label, not provider attestation). All shell commands and children were pinned to CPUs 8–23.

## Immutable inputs and reconciliation

- P1: 2174265e9cc1b248c0fbe27fa101875984d46d6b.
- Frozen coordinator: 92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1.
- The inventory hosted at both commits describes distribution eb4763e3cc9bcd729830cd85f1719bbd4f28db10, generated 2026-10-23T02:20:48Z. It is not a fresh census of either host commit.
- Inventory, areas, slices and generator are byte-identical between P1 and the coordinator. Exact blob IDs, SHA-256 values and sizes are in report.json.

| Population | Paths | Meaning |
| --- | ---: | --- |
| Stored records survey | 126,149 | All distribution / fork-own / reach n/a |
| P1 matching metadata paths | 126,150 | Survey plus docs/retros/2026-10-23-m6-p1-survey.md |
| Frozen coordinator matching metadata paths | 126,670 | P1 +522 additions −2 deletions; 3 changed paths |

All 126,149 survey paths match P1 literally without decoding. The coordinator retains 126,147 survey paths and has 523 paths outside that survey. This reconciles the count difference without replacing the survey or cutting final T46 membership.

The records area selects docs/{qa-logs,qa-frames,audits,work-logs,retros,retrospective,futros}/**, research/**, .github/sessions/** and docs/reviews/inventory.json. The records slice has an empty selector, meaning all rows of that area, with no additional tier, reach or glob filter.

The stored line total is exactly **22,984,582**. The generated issue's **15,392,661 read lines** are exactly the sum for languages in the generator's CODE set, excluding vendor-carried or unreached rows. Shell contributes 12,526,323 and Python 2,815,020 of that tally. The order explicitly uses a **table**, displaying a row count and “--” for reading size. This is not a 15-million-line code-review budget.

The generator's line_counts source uses Git numstat against the empty tree, with binary “-” stored as null. This preparation sums the existing column; it does not recount record bodies or rerun the generator. The inventory's own row stores 134,637 historical lines and a prior commit attribution, so treating that self-row as current output measurement would introduce a recursive denominator.

## Folder metadata

| Group | Survey rows / lines | P1 paths | Coordinator paths | A / D / M |
| --- | ---: | ---: | ---: | --- |
| .github/sessions | 353 / 84,435 | 353 | 356 | 3 / 0 / 1 |
| docs/audits | 59,688 / 16,262,198 | 59,688 | 59,693 | 5 / 0 / 0 |
| docs/futros | 6 / 520 | 6 | 17 | 11 / 0 / 0 |
| docs/qa-frames | 970 / 5,625 | 970 | 970 | 0 / 0 / 0 |
| docs/qa-logs | 64,327 / 6,195,761 | 64,327 | 64,815 | 488 / 0 / 0 |
| docs/retros | 5 / 415 | 6 | 8 | 2 / 0 / 0 |
| docs/retrospective | 1 / 17 | 1 | 1 | 0 / 0 / 0 |
| docs/reviews | 1 / 134,637 | 1 | 1 | 0 / 0 / 0 |
| docs/work-logs | 81 / 27,812 | 81 | 94 | 13 / 0 / 2 |
| research/council-runs | 660 / 270,364 | 660 | 658 | 0 / 2 / 0 |
| research/preliminary-reviews | 24 / 1,278 | 24 | 24 | 0 / 0 / 0 |
| research/seat-probes | 33 / 1,520 | 33 | 33 | 0 / 0 / 0 |

Each Git row binds path, mode, type, full blob ID and logical byte size. P1 modes are 96,707 regular 100644 and 29,443 executable 100755; coordinator modes are 97,225 and 29,445. No symlink or gitlink entries occur in either selected set. No source-link targets or broad Markdown links were traversed.

P1 logical bytes total **2,137,588,288**; coordinator **2,173,665,613**, a delta of **36,077,325**. Unique blobs number 37,343 / 37,761, with unique-blob logical totals 1,032,903,648 / 1,068,422,827 bytes. These are uncompressed object-content measures. They establish neither packed/disk use nor achievable savings, reader value or a case for deleting repeated evidence.

The frozen delta is **522 A / 2 D / 3 M / 126,145 unchanged** with rename detection disabled. Independent raw metadata diff and two-tree comparison agree. All three changed paths change blob identity; none changes mode:

- .github/sessions/saved-session-state-feature-m6-renovation-plan-346.md
- docs/work-logs/2026_10-work_logs/2026_10_23-work_log.md
- docs/work-logs/INDEX.md

Of 522 additions, 488 are under docs/qa-logs, including 455 under 2026-11-02-m6-resume (34,361,042 logical bytes). Other additions: 13 work logs, 11 futros, 5 audit artifacts, 3 archived session pointers and 2 retros. These are metadata group descriptions, not content-review claims.

The two existing deletions are under research/council-runs/verification and have credential-labelled filenames. Only Git path/mode/blob/size metadata was observed; their content was not read or recovered. The report retains group counts and a metadata digest rather than exporting those paths. No cleanup is proposed.

report.json also carries inventory language groups, suffix groups, per-folder bytes, added subgroups and exact changed-path object metadata. Filename extensions are labels, not proof of a file's semantic purpose.

## Candidate reader routes and ownership

| Named entrypoint | What it establishes | Boundary |
| --- | --- | --- |
| docs/reviews/README.md → plan/order/areas/slices/inventory | Program inputs, order and generated-ledger ownership | Root owns baseline, slicing, briefs and acceptance; no regeneration here |
| docs/audits/README.md | Dated scope directories and 00–05 artifact convention | No audit-body sweep or new audit |
| docs/retros/README.md and docs/futros/README.md | Dated placement and ceremony conventions | No new ceremony or execution |
| docs/work-logs/INDEX.md | Generated index, month → ISO week → day; day file remains the record | No day-body sweep or index regeneration |
| Coordinator session pointer at frozen coordinator | Accepted producer refs and coordinator integration ownership | Its pending-state prose is temporal, not live scheduling authority |
| T39 current-focus block at completion 7994f760fe1f4df6744844e80433bc49295cb94e | Accepted source 4eb5dfab8e745914a55e7de3e5a43c5b91ebc608; audit #1406 completed; stop pending ordered integration | Completed T39 corrections are not reopened |

The T39 pointer is not present in the frozen coordinator tree. It was read at the exact completion commit named by the coordinator, without changing or scanning another worktree. A historical archived T39 pointer was also encountered while resolving that entrypoint; its old commands and permission text were not executed or adopted.

D-WORKFLOW-223 keeps the menu-map journal in place for the completed T39 correction, labels its history and corrects obsolete pending headings. D-WORKFLOW-224 retains low-inbound references and dates/labels those liable to mislead. Neither authorizes bulk deletion.

[#1407](https://github.com/pixelelated/distribution/issues/1407) owns later monthly indexing and individual review of 33 documents / 2,770 lines: 32 T39 edit-scope files plus the table-only historical plan plans/conflict-resolution/vita-style-conflict-resolution.md. Low inbound link counts measure links, not readership. Its later work preserves dates, content provenance, headings and old-to-new path/anchor/line citations, and requires purpose/replacement evidence for each proposed outcome. T39's completed reference fixes remain completed.

The plan, reviews README, register and menu-map context are not silently added to the records slice. Source links, generated indexes and the records they describe remain distinct. The frozen coordinator is not the final ordered integration tree; accepted T39/T41 branch contents have not been unioned into this observation.

## Inputs root can use for a future bounded brief

1. Bind the stored survey by inventory/areas/slices blobs, its distribution source commit and its selected-path digest. Bind any separate frozen metadata observation by commit IDs and the canonical path/mode/type/blob/size digest. Root decides final membership after the prior slices.
2. Keep survey rows, later P1 records and post-P1 coordinator deltas separate. Select immutable inputs before producing outputs. Count generated indexes explicitly rather than silently dropping them; keep the new report outside the measured tree to avoid recursive self-counting.
3. Use the named reader routes as candidate bounded reading inputs. Root chooses exact links, paths, questions and acceptance evidence. This report does not establish that every link resolves or every record remains useful/current.
4. Metadata can measure counts, stored language/lines, modes, logical bytes, unique blobs and frozen deltas. Later authorized proof is needed for reader use/value, stale versus intentional history, path/anchor/line-citation resolution, final integrated membership, disk/pack costs or runtime costs.
5. State the interface with #1407 explicitly in a future brief. Do not repeat T39 corrections or preempt that backlog's monthly indexing and individual dispositions.

## Commands, hashes and limits

Core derivation: taskset -c 8-23 python3 /workspace/tmp/m6-t46-t3-20261102-planning/derive-metadata.py, run from the existing T41 tree. The private script reads only the frozen inventory/source-map inputs and Git metadata. It is not installed in the repository or kit. Exact Git argv is retained in report.json:

- git show PIN:docs/reviews/{inventory.json,areas.json,slices.json} and PIN:tools/renovation-inventory
- git ls-tree -r -l -z PIN -- the exact expanded records roots
- git diff-tree --no-commit-id -r --raw --no-abbrev -z --no-renames P1 COORDINATOR -- the same roots
- git ls-tree -l -z PIN -- named entrypoint; git rev-parse PIN^{commit} / PIN^{tree}

The generator was parsed only to read literal CODE metadata. No generator or accepted program/control was executed. Named prose reads used git show at the frozen coordinator, except the explicitly pinned T39 handoff. Their bounded sections and blob IDs, plus full GitHub issue/comment body hashes, are retained in report.json.

Path-set SHA-256 encodes sorted raw path bytes separated by NUL. Canonical metadata SHA-256 encodes sorted entries as path NUL mode NUL type NUL blob-ID NUL decimal-size NUL. Raw listing/diff hashes cover exact Git command output; no complete path list or full tree export is persisted.

- report.json SHA-256: 713f999d552cdacce9e59bd062ac7b410b11ce26bf427860412b09de185a0b98
- derive-metadata.py SHA-256: 1eea99da03a27a158fc987677618b4b0de0ee55e27356cca233792b6b0583d94
- P1 raw metadata SHA-256: e9116491df36a939e0cc1c50127c031ebeace88e362c0070deff9ca99600b6f2
- Coordinator raw metadata SHA-256: a5080d8cf9218a60e7885e5f2f3abd55c417f647350f9ad78a76bc0f11b4c0d3
- Raw metadata diff SHA-256: d5f951839720859ac4651a9740adde492e09f520a26fa763382af8a899a6a70f

Only this new private report directory was written. No repository/tracker/kit edits, commit/push/merge, live worktree scan, source export, final membership recut, audit-log body sweep, held/private or credential-content read, host/cache/process inspection, runtime/guest/build allocation, fetch/provider/device/cloud action, producer replay or permission answer occurred.

**Stop:** factual planning preparation is complete. Root retains baseline, brief, criteria, dispatch, dispositions and ordered integration.

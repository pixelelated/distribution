# Selected cloud folders: validator and harness evidence

The latest validator control run (`runs/final04.json`) passed all **30 cases** on combined source commit `6f89bc7cecee5972909828103689e2c7c0711c30`; `source04/` holds the six exact scripts delivered to the UI worker. This supersedes source03: flat files under the selected ROMs folder are now reported as misplaced, and the content parent walk preserves an explicitly selected relative root. The earlier 28-case run and six affected absolute-root controls remain as historical receipts. These are host fixture proofs, not final image or device qualification.

The controls use real pinned rclone 1.75.1 against owned local filesystems, with narrow metadata fault shims. They cover selected-root-only reads, no writes during validation, explicit category seeding, independent pointers, relative namespaces, missing versus unreadable results, partial failures, bounded depth/entries/bytes/time, actual progress/conflict exclusions, and exact public ROCKNIX `/GAMES` plus `/GAMES/backup` config conversion. Canonical public config comes from `c445081a59518f37d9776e5412dd7b14910696f7`. Missing new content selection receives the shipped default; explicit existing selection, including empty relative root, remains unchanged.

`runs/root-old01.json` preserves the failing control at `583c1b4d`: `--folder-state` reported `STATE=ready` for an unreadable explicitly selected absolute root because it probed the readable relative root instead. The final correction preserves `remote:/` separately from `remote:`. The control maps these namespaces to distinct real directories rather than using an alias that normalizes leading slashes.

The validator never proves payload integrity. `present` means recognized metadata was seen; bounded or failed reads remain incomplete/unreadable. A save named `Saves/foo.srm` is not assumed misplaced from that folder name alone. Unsupported layouts receive instructions; no general repair, relocation, provider-root search, or ROM movement is offered. Explicit folder creation also writes explanatory README notes when absent and preserves existing notes.

## Regression harness adaptation

`harness-incremental.patch` contains only this worker's changes after the earlier held #508 routing edits. The worker did not stage shared coordination files. Root later committed the combined qualified QA-tool changes as `5f21df775614bd22e56eb1d02e1b39e17069cd7b`. This earlier focused harness identity remains in `qualification-inputs.json`; the final full-run identity is in `../broad/run03/terminal-readback.json`.

| Affected cases | Current-source contract | Historical contract retained |
| --- | --- | --- |
| Source loader | Load executable `cloud_folder_validate` when selected setup requires it | Old source needs no new helper |
| C1 setters | Saves/settings/content choices change one pointer; relative namespaces preserved; explicit content root allowed | Coupled saves setter and absolute normalization assertions remain |
| C1/CF1 malformed config/path | Scoped seed calls actually reach config validation; canonical path suggestions reflect independent selection | Original sibling derivation and canonical suggestions remain |
| C2 seeding | Explicit categories; four selected README destinations; no unselected writes; no-argument seed refused before remote access | Original five README destinations and no-argument seed remain |
| C2 content location | Bounded metadata reads of selected content only | Earlier bounded `lsf` expectations remain |
| CF2 duplicate keys/readers | First-key and malformed-value assertions still execute through new helper | Original reader agreement checks retained |
| Scanner opening/content/folder | JSON result bound to run, config, mode, and result bytes; no account-root discovery; new request cannot consume stale results | Epoch stamps, root-dir listing, and old folder stamp behavior remain |
| Migration history | Existing #508 absence routing unchanged; explicitly inapplicable, never counted PASS | Historical engine routing remains when selected source contains it |

The focused scripts are extractions of the affected sections. `harness-focus01` passed 105 controls using host utilities. **Runtime correction:** the initially named `harness-image01` (105 PASS) and `harness-historical01` (99 PASS at ref `3268015c`) also used host utilities: their BusyBox setup slice incorrectly matched an earlier marker and was empty. Image binary hashes were verified, but that did not establish image runtime use. Their unchanged raw outputs and originally reported metadata are retained; corrected metadata is in `qualification-inputs.json`. The superseding `harness-actual-image02` and `harness-actual-historical02` checks print the copied BusyBox identity and pass 105 current-source and 99 historical-source controls, respectively; `actual-image02.json` records the copied binary hash. The corrected extraction is `focused-harness-actual-image.sh`. Each original run reports zero failures/skips and one explicitly inapplicable retired migration section. Independent validator controls use real pinned rclone. These extracts do not replace full broad qualification; the later broad attempt is recorded separately in `../broad/`.


## Earlier attempts and limits

Earlier raw failures remain under `runs/earlier-*`, without fabricated terminal result receipts. Proof01/02 exposed real missing-listing output (`[` plus rclone rc 3), which the initial parser treated as unreadable. Proof03 used the older host rclone, which could not seed with the already-required directory-marker flag; final controls use pinned 1.75.1 and the focused validator harness now refuses another version up front. Public01 failed to create `/usr/config` in a read-only fixture mount; later public-config controls correct that fixture. Proof08 contains no product result because host sandbox quota prevented fixture creation. Historical intermediate PASS summaries are in `intermediate-results.json`; they do not qualify final bytes.

Each `runs/*.json` preserves original relative paths, byte counts, SHA-256 hashes, raw UTF-8 output, fixture inputs, and final filesystem/config readback. Duplicate source trees are represented by source hashes or their existing `source-sha256.json`; committed product sources remain in Git. No personal cloud data or credentials are in these synthetic fixtures.

The earlier prepared full-run command is retained in `broad-run-command.sh`. The final complete run has now passed; see `../broad/run03/README.md` for its actual invocation, unchanged inputs and consumed terminal receipts. No launch is pending. The retained image binary hashes were reverified against the earlier receipt before the focused image run. Build-drive temporary files are used, not the root filesystem.

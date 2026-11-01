# T39 (#686) forward audit -- doctrine: the reference documents

Phase 2 over #686's checklist. **reviewed-at** `86ebb6dffc` (the dispatch
merge), the lane's tip at stage B `f60c2c08bf`. Every check below is a
`git show`/`git grep`/`git cat-file`/`git diff` at a hash or a
`gh --repo pixelelated/distribution` read -- no fetch, no guest, no build, no
keyed call (ruling (q)). Each lead's line is **FAIL-first**: it prints the
defect at the tip here, and must print nothing (or the corrected line) after
its disposition lands. The `L-NN` numbering is the brief's § 3.

Sections filled at this stage (B): § The table (the leads), § Binaries, § Art
bytes, § The identity words, § The retired names, § The runs, § Proofs, and the
inherited list. **§ Coverage** (the 254-row table) is generated at stage C by
`tools/t39-tables.py` from `block-2.txt`, the probes and the export; its inputs
are gathered and recorded under § The runs. **§ The streams** is filled at
stage E.

## Coverage

Generated at stage C by `tools/t39-tables.py` (§ 6 Outputs; the tool does not
exist at stage A/B). Its inputs are in hand and recorded in § The runs: the
carve TSV in `.qa-scratch/t39/block-2.txt`, the export of the 254 at the
dispatch tip, and the probes below. The carve classes at the tip (the brief's
§ 2 classifier run unmodified, matching `:1297` to the byte):

`art-bytes 18` · `edit-scope 68` · `edit-under-naming 1` · `ledger-binary 31` ·
`ledger-named 6` · `ledger-plan 1` · `ledger-reviews 12` · `read-only-528 1` ·
`read-only-585 27` · `read-only-upstream 88` · `tabled-generic-x64 1` ·
**total 254**. The edit scope the lane may touch at stage E is `edit-scope` 68
plus `edit-under-naming` 1 (`TRADEMARK.md`, where `NAMING.md` decides the word).

## The table

One row per misleading statement (the leads of § 3). `path:line` is at the
dispatch tip; *tip* is the FAIL-first check's result, run this stage. The
disposition set is § 6's: `fix`, `inherited:<owner>`, `ledger`, `#528`, `#585`
(a few leads resolve to a § Coverage `none` and are marked so).

| path:line | the sentence | the artifact it names | what a reader does | owner | lead | tip (FAIL-first) | disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/reviews/README.md:10-12` etc | the renovation README/plan name `order.md`, `inventory.json`, `status.md`, `slices.json`, `renovation-{inventory,status,drift}` | the renovation's own files/tools | looks for them, found absent at `e3fb3dfe00` | coordinator | L-01 | the 15-name loop prints **no `MISSING`** at the tip (present via the P1 stacking) | **ledger** (resolved at dispatch, ruling (p)) |
| `README.md:7-10` | *"Updates for this release are manual; use the instructions attached to the [release]"* | a pixelelated release that does not exist (`gh release list`: `rc1-20260929`, two dev builds) | opens the release, finds no 0.0.1 | -- | L-02 | `instructions attached` = **1** | **fix** (ruling (c)) |
| `docs/device-testing-policy.md:5` | *"**Open:** D-QA-016 ... (#131)"* | a decided row / a closed issue | treats a settled QA-handheld question as open | -- | L-03 | `Open:.*D-QA-016` = **1** | **fix** (ruling (l)); `vm-first.md`'s line is **inherited:coordinator** |
| `docs/rasteratops/cloud-layout.md:16`, `docs/releases/pr/08-saves.md:5` | *"`cloud_migrate_layout` derives the destination ..."*; *"... layout migration ... scripts"* | a script D-CLOUD-175 retired | expects a live migration script | -- | L-04 | both lines present; `D-CLOUD-175` in them = **0/0**; shipped OS (`projects`+`packages`+`scripts`) = **0** | **fix** (ruling (l)) |
| `docs/device-flashing-runbook.md:3,5,...` | the OS named *ROCKNIX* throughout (*"every fresh ROCKNIX card"*) | the flashing runbook `CLAUDE.md` names | flashes thinking the OS is ROCKNIX | -- | L-05 | `ROCKNIX`=**21**, `pixelelated`=**0** | **fix** where `NAMING.md` decides the word; the rest recorded (ruling (l)) |
| `docs/cloud-save-integrity.md:4` | *"M7 order remains #515 -> #508 -> #507 ..."* | closed issues as an order the milestone body owns | reads a stale order | -- | L-06 | `M7 order remains` = **1** | **fix** |
| `docs/backup-contents.md:3-5` | *"BACKUP CONFIGURATIONS"*, *"RESTORE EVERYTHING"* -- banned words, labels the pin doesn't ship | the ES labels (*"source of truth for ... rocknix.org"*) | expects labels/words that aren't shipped | -- | L-07 | at the pin: `BACKUP CONFIGURATIONS`=0, `RESTORE FROM BACKUP`=0, `RESTORE EVERYTHING`=0 | **fix** (labels re-derived from the pin) |
| `docs/es-menu-map.md:758,806,817` | *"### Pending ... (#570)"*, *"under qualification"* | closed work called pending | believes work is open | -- | L-08 | three headings print at the tip; `es-menu-map-check` still `0 missing` | **fix**: the headings only, no restructuring (ruling (b)) |
| `docs/releases/next-candidate-work.md:4` | *"the baseline is ... `0.0.1-dev+20261011...`"* | a superseded baseline (`device-facts`/`support-matrix` name `077197`) | plans against an old baseline | -- | L-09 | `baseline is` at `:4` | **fix** |
| `docs/pixelelated/cloud-folders.md:32-35` | *"Publish it with the qualified build ... earlier ... migration flow"* | internal release status in a player guide | reads internal status as guidance | -- | L-10 | `prepared release documentation` = **1** | **fix** |
| 10 files, `release-readiness.md` etc | words and numbers run together (*"all18"*, *"October14"*) | nothing; a legibility defect | mis-reads a number | -- | L-11 | `next-candidate-work`: `October1`=12, `and1`=7, ... | **fix** in the edit scope; `docs/upstream/README.md`'s 8 **#585**; `rc-accept.txt`'s `glslang16.6.0` **ledger** (L-26) |
| `docs/council-mistral-counter.md:3` | a counter note for the retired Mistral seat, no banner | `scripts/council-count-mistral.mjs` for a seat outside every run profile | thinks the seat is live | -- | L-12 | `sealed\|retired\|scaffold#915` = **0** | **fix**: a banner; retiring `council-limits.md` is § 4 Q2 |
| `docs/technical-appendix-...md`, `site-plan.md:70`, ... | rocknix.org drafts naming pages/branches this tree can't check | seven rocknix.org pages; `docs/cloud-saves-native-wizard` (a site branch) | looks for a page/branch in this tree | -- | L-13 | `docs/cloud-saves-native-wizard` **ABSENT** (external, X02) | **fix**: name the repository/branch beside each page |
| `docs/pixelelated/art/README.md:20-21` | *"generated by `pixelelated/splash` `tools/pixelelated-wordmark`"* | the splash repo's tool, named as such | -- (the README already says where it lives) | -- | L-14 | `tools/pixelelated-wordmark` **ABSENT**; the README names `pixelelated/splash` | **none** -> § Coverage row (X02) |
| `docs/releases/device-facts.md:7` + rows | *"The cuts themselves are [catalog.md]"* with none of their cuts in it; rows cited by number | a catalog with none of the four hashes | follows a pointer to a catalog that lacks the cuts | #270 / coordinator | L-15 | four hashes in `catalog.md` = **0/0/0/0** | **fix** the pointer without moving a cited row; **inherited:#270** (the tool/row-vs-rule); **inherited:coordinator** (catalog regen, #964) |
| `docs/device-testing-policy.md:94` | the mask's long form, short of the flag form | the read mask a reader copies | masks a command line and prints a credential | -- | L-16 | `--(token` = **0** at the tip | **fix** |
| `docs/conflict-wizard-ia.md` | the IA at Rev 6 vs #23's rev 5; text against decided rows | #134's revision list; D-CLOUD-024/027/032/041 | reads the IA against a stale #23 | the interface lanes | L-17 | `rev 6` at `:19`, `rev 5` at `:29` | **fix** where a sentence contradicts a decided row; else **inherited:the interface lanes** |
| the 17 low-inbound documents | dated records presenting as current | the lens's sharpest rows (2,135 lines) | reads a dated record as current state | -- | L-18 | `LOW-INBOUND` set confirmed by the digest; each dated | **fix**: a dated first line where a record presents itself as current; retirement is § 4 Q2 |
| `docs/rasteratops/art/README.md:8` | *"generated ... by `rasteratops/splash`'s `tools/rasteratops-wordmark`"* | the splash repo's tool, in a historical artifact | -- (the README says where it lives) | -- | L-19 | `tools/rasteratops-wordmark` **ABSENT**; line 8 names `rasteratops/splash` | **ledger** (a historical artifact; X02) -> § Coverage |
| `docs/rasteratops/p0-read.md`, `p0-sweep.md` | a short path `packages/rocknix` in dated P0 records | an in-tree path that is absent | looks for `packages/rocknix` | -- | L-20 | `packages/rocknix` **ABSENT** | **ledger** (a dated record) unless it presents as current -> § Coverage |
| `docs/rasteratops/raofflineproxy-refresh.md:180,188`, `cloud-folder-state-table.md:38` | *"Rasteratops, so ... could not find system.cfg"*, *"`N` is `/Rasteratops/Saves`"* | Rasteratops as the OS's identity | reads the retired name as current | -- | L-21 | the three lines print | **ledger** (dated) unless its tense presents the identity as current: then **fix** (name D-WORKFLOW-144) |
| `docs/pixelelated/site-plan.md:72` | *"Remotes still name `maxengel/rocknix.org`"*; a `Development/rocknix` line | a retired owner/path in a current plan | acts on a retired remote/path | #511 | L-22 | the two lines print | **fix** where it misstates the present; else **inherited:#511** |
| `docs/cloud-sync-changelog.md:706-735` | `maxengel/rocknix` links resolving only by redirect | four links in dated changelog entries | follows a redirecting link | -- | L-23 | `github.com/(rasteratops\|maxengel)` prints **`docs/cloud-sync-changelog.md:4`** alone | **ledger**; ruling (l)'s fix applies to any edit-scope instance the identity step finds |
| `plans/conflict-resolution/...:8-9,13` | *"Choices: KEEP CLOUD / KEEP DEVICE / MERGE"* -- superseded, unmarked | the July plan; the IA has no `MERGE` | reads a superseded plan as current | -- | L-24 | IA words: `KEEP BOTH`/`KEEP LEFT`/`KEEP RIGHT`, **no `MERGE`** | **ledger**: one historical-plan row naming the superseding row (ruling (d)) |
| `docs/releases/rc-accept.txt:13,15` | *"the first Rasteratops release"* | the RC ledger; `release-readiness.md` | reads the retired name in the RC record | coordinator | L-25 | `Rasteratops` at `:13` | **ledger**: **inherited:coordinator** (ruling (l)) |
| `docs/releases/rc-accept.txt` | two stale acceptances (`zip`, `spirv-headers`) kept as the record | the RC ledger (9 non-comment lines) | -- (the file says they stay as the record) | -- | L-26 | non-comment lines = **9** | **ledger** |
| `docs/pr-series/map.txt:112,174` | two deleted rclone paths named in the upstream-series map | `post-update`, `cloud_migrate_layout` (both deleted) | `pr-stack-check` would fail on them | coordinator | L-27 | both **GONE** | **ledger**: **inherited:coordinator** (ruling (e)); never run `pr-stack-check` here |
| `docs/reviews/plan-for-the-plan.md:...` | *"This file exists on `next` at `docs/reviews/...`"* while `next` has none | the renovation plan; `next`'s tree | believes `docs/reviews/` is on `next` | coordinator | L-28 | `next` (`8ebaf8daad`) `docs/reviews/` = **0** files | **ledger**: **inherited:coordinator** (ruling (a)) |
| `docs/reviews/order.md:792` | *"split in three (T4, T33, T39)"* -- a preliminary number | the renovation order; T33=today's T38 | reads an old slice number | coordinator | L-29 | the line prints at `2174265e9c` | **ledger**: **inherited:coordinator** |
| `docs/rasteratops/release-readiness.md`, `support-matrix.md` | *"# pixelelated 0.0.1 release readiness"* under the retired-name folder | current release records under `docs/rasteratops/` | -- | #509 | L-30 | the title prints | **inherited:#509** (a reviewed rename batch; moving changes a ledger row) |
| `documentation/.../GENERIC_X64/...md` | the fork's emulator table drifted, no generator | AMD64 vs GENERIC_X64 (`57+/66-`) | reads a stale emulator table | coordinator | L-31 | the `--stat` prints the drift | **inherited:coordinator**: a Backlog candidate (ruling (j)) |
| `docs/es-menu-map.md:134,405,595` | the most-cited map, cited by line by 26 issues | the map (a check that proves titles only) | an issue's line-cite drifts | the interface lanes | L-32 | the three lines print | **inherited:the interface lanes** (ruling (b)); `02` records which lines still say what the issues cite |
| #576 `:7`, #620 `:16` | *"governed by `docs/graphics-memory-testing.md`"* | a document the tree lacks | looks for a missing document | coordinator | L-33 | `docs/graphics-memory-testing.md` **MISSING** | **inherited:coordinator** (in no tree here) |
| `docs/decision-register.md` rows vs `:514`, `:797` | a submission series D-WORKFLOW-084 ended, described as live | the register rows / `documentation-accuracy.md`'s *"blocks it"* | reads an ended series as live | coordinator | L-34 | the three rows print | **inherited:coordinator** (rows + a rule); `map.txt` tabled (L-27) |
| `.claude/rules/handheld-evidence.md` glob | a `docs/**` glob loading the rule for any record | the rule's glob | -- | coordinator | L-35 | the glob line prints | **inherited:coordinator** (T4's file); `02` lists which reference documents it reaches |
| `CLAUDE.md:34`, `AGENTS.md:31`, `instruction-files.md:122` | *"Two ... documents"* vs *"three"* load nowhere | the three load-nowhere documents | counts two where three are meant | coordinator | L-36 | `:34`/`:122` print the two counts | **inherited:coordinator**; T39's half (does the policy carry interface law) is a § Coverage note |
| #807 body `:15` | *"its paths have no upstream (ROCKNIX carries none of them)"* | the area epic's framing vs `upstream-carried 90` | reads a slice-untrue area sentence | coordinator | L-37 | the sentence prints; **the Erratum IS present** on `:15` (case-insensitive; settled 06:43 UTC) | **inherited:coordinator** (erratum written at dispatch) |
| the 53 files outside `register-check`'s LIVE | decision IDs no tool checks | 53 reference files citing IDs | a cite could rot unguarded | #947 | L-38 | register **716**, cited distinct **442**, **UNRESOLVED: none** | **inherited:#947** (the guard); clean today, unguarded tomorrow |
| `docs/releases/versioning.md` | #1013's open criterion on the file | the versioning doc | -- | #1013 | L-39 | `emulationstation` in the file = **0** | **inherited:#1013** |
| `worktrees.md`, `CLAUDE.md` vs the machine | `../rocknix.worktrees/`, `/workspace/repos/rocknix` | rule paths the machine retired | reads a retired path word | coordinator | L-40 | `git worktree list` has `distribution.worktrees`; the rules say `rocknix.worktrees` | **inherited:coordinator** (T4's rules) |
| `documentation/.../SUPPORTED_EMULATORS_AND_CORES.md` (13 of 15) | upstream's generated tables, behind upstream | the per-device tables | reads a table behind upstream's | the next upstream base merge | L-41 | `--stat` vs `651150fc88` prints **15 files changed** | **inherited:the next upstream base merge** (ruling (a)) |
| #335 `:19` | *"the CC BY-NC-SA attribution ... per `LICENSE.md`"* | a licence attribution `LICENSE.md` lacks | expects BY-NC-SA in `LICENSE.md` | coordinator | L-42 | `BY-NC` in `LICENSE.md` = **0** | **inherited:coordinator** (a stale checkbox) |
| `TRADEMARK.md:5-6`; `LICENSE.md:3,13,18` | GPL v2 vs *"non-commercial use only"*; *"Copyright 2024 ROCKNIX"* | the fork's own licence terms (unstated) | can't tell the fork's own terms | #528 | L-43 | the statements print and disagree | **#528** (a legal reading; never a fix here) |
| `licenses/AETHERSX2.pdf` | a licence upstream dropped for a licensing concern, carried on | the PDF (21 `aethersx2` paths; 0 upstream) | -- | #528 | L-44 | `aethersx2` paths at HEAD = **21** | **#528** (the PDF row) -> § Coverage; the package is another slice's |
| #359 `:9,13,14` | a candidate's recorded licence bytes | `LICENSE.md`/`TRADEMARK.md` sha256 | -- | #528 | L-45 | hashes **equal** #359's (`1a277de2...`, `d46db25c...`) | **#528**; an edit to `TRADEMARK.md` is preceded by this line |
| `docs/upstream/**` (28) | the contribution queue's drafts, read-only | #585, D-WORKFLOW-165 | -- | #585 | L-46 | `#585`/`D-WORKFLOW-165` at `:3,8,45,...` | **#585** |

**Not leads (checked, pass), at the tip.** `rclonectl` 0, `.github/instructions`
0, `rubber-duck` 1 (in the dated `rules-sweep-2026-09-12.md` alone),
`Pixelelated`/`PIXELELATED` capitalised **0** (D-WORKFLOW-144 holds); **0 dead
relative Markdown links** over 511 scanned (resolved against the worktree).

## Binaries (ledger-binary, 31; ruling (o))

sha256 at the dispatch tip; the `fixed-at` column is filled at stage E (equal,
these are never edited). 28 png, 2 pdf, 1 gz.

| path | size | sha256 (16) at tip | sha256 at fixed-at |
| --- | ---: | --- | --- |
| `docs/pixelelated/art/proofs/backgrounds.png` | 25167 | `19e30291d51ffeab` | (E) |
| `docs/pixelelated/art/proofs/boot-shutdown-640x480.png` | 1393 | `a3211e6206231751` | (E) |
| `docs/pixelelated/art/proofs/small-sizes.png` | 10195 | `596f6de6772b4cfd` | (E) |
| `docs/pixelelated/art/raster/1x/dual.png` | 676 | `9fe50cf05c01a428` | (E) |
| `docs/pixelelated/art/raster/1x/monochrome-dark.png` | 542 | `4771c7673637a785` | (E) |
| `docs/pixelelated/art/raster/1x/monochrome-light.png` | 531 | `f59f0c9825691258` | (E) |
| `docs/pixelelated/art/raster/1x/neon.png` | 712 | `b1e993ec24beb292` | (E) |
| `docs/pixelelated/art/raster/1x/ocean.png` | 693 | `5fde4a652c49d024` | (E) |
| `docs/pixelelated/art/raster/1x/scanline.png` | 653 | `b85abe09b8ea1159` | (E) |
| `docs/pixelelated/art/raster/1x/spectrum.png` | 696 | `b43c4eeb8db061c4` | (E) |
| `docs/pixelelated/art/raster/1x/sunrise.png` | 710 | `86ceca6c48315efd` | (E) |
| `docs/pixelelated/art/raster/2x/dual.png` | 1589 | `7c39c02af9ed1fb1` | (E) |
| `docs/pixelelated/art/raster/2x/monochrome-dark.png` | 1293 | `c5ef49a820e21a05` | (E) |
| `docs/pixelelated/art/raster/2x/monochrome-light.png` | 1269 | `b0bea5b35c8a0d6f` | (E) |
| `docs/pixelelated/art/raster/2x/neon.png` | 1473 | `69345e13666ab714` | (E) |
| `docs/pixelelated/art/raster/2x/ocean.png` | 1467 | `411877033bb998ba` | (E) |
| `docs/pixelelated/art/raster/2x/scanline.png` | 1384 | `a38293cae2957b2c` | (E) |
| `docs/pixelelated/art/raster/2x/spectrum.png` | 1450 | `0379e2602a68a3f2` | (E) |
| `docs/pixelelated/art/raster/2x/sunrise.png` | 1472 | `b7a09bb72fcb2c21` | (E) |
| `docs/pixelelated/art/raster/4x/dual.png` | 4095 | `da6c65fe17397ca2` | (E) |
| `docs/pixelelated/art/raster/4x/monochrome-dark.png` | 3836 | `d14d7c953a42e71e` | (E) |
| `docs/pixelelated/art/raster/4x/monochrome-light.png` | 3814 | `0ccbe161b9d81541` | (E) |
| `docs/pixelelated/art/raster/4x/neon.png` | 4112 | `98d4df292b81a890` | (E) |
| `docs/pixelelated/art/raster/4x/ocean.png` | 4092 | `979ecb9d6c729e0b` | (E) |
| `docs/pixelelated/art/raster/4x/scanline.png` | 3944 | `48d8dbd4b043940a` | (E) |
| `docs/pixelelated/art/raster/4x/spectrum.png` | 4102 | `00a70a9a1943b8eb` | (E) |
| `docs/pixelelated/art/raster/4x/sunrise.png` | 4102 | `23745b792dc63cd3` | (E) |
| `docs/rasteratops/art/icon-interim-2026-10-01.png` | 718 | `1c7f06f8c28de2ac` | (E) |
| `docs/upstream/2026-10-15-queue-reconciliation/originals.tar.gz` | 57557 | `88e015409159c98e` | (E) |
| `licenses/AETHERSX2.pdf` | 1005740 | `25bca10c4ceaf24d` | (E) |
| `licenses/DRASTIC.pdf` | 239739 | `697815a8d51d416d` | (E) |

## Art bytes (art-bytes, 18; ruling (o), widened at version 2)

The 18 art text files, never edited; sha256 at the tip, `fixed-at` equal at E.

| path | size | sha256 (16) at tip | sha256 at fixed-at |
| --- | ---: | --- | --- |
| `docs/pixelelated/art/Tiny5-OFL.txt` | 4384 | `6e24408062bb54fd` | (E) |
| `docs/pixelelated/art/pixelelated-wordmark.svg` | 25092 | `f5fa983918169354` | (E) |
| `docs/pixelelated/art/proofs/artifact-checks.json` | 6822 | `1274ba1d67da2ec6` | (E) |
| `docs/pixelelated/art/source/font.json` | 359 | `cb3b043a4ce2bc2e` | (E) |
| `docs/pixelelated/art/source/generate.py` | 8802 | `0ccded4cb9693b81` | (E) |
| `docs/pixelelated/art/source/palettes.json` | 975 | `f0ef617d86144a19` | (E) |
| `docs/pixelelated/art/source/pixelelated-live-text.svg` | 979 | `3afb3bcd7a470e01` | (E) |
| `docs/pixelelated/art/source/wordmark.css` | 1524 | `fb5ee55b1321e9d1` | (E) |
| `docs/pixelelated/art/wordmark/dual.svg` | 12441 | `850c80cc8affc6c5` | (E) |
| `docs/pixelelated/art/wordmark/monochrome-dark.svg` | 12137 | `19fd14fbc2c905dc` | (E) |
| `docs/pixelelated/art/wordmark/monochrome-light.svg` | 12137 | `fbdbfa331d156f9c` | (E) |
| `docs/pixelelated/art/wordmark/neon.svg` | 12437 | `29929e3460498aed` | (E) |
| `docs/pixelelated/art/wordmark/ocean.svg` | 12437 | `aa6b69817d6a1df7` | (E) |
| `docs/pixelelated/art/wordmark/scanline.svg` | 12427 | `6fbc7dc7705df158` | (E) |
| `docs/pixelelated/art/wordmark/spectrum.svg` | 12437 | `3ccd73a324678be4` | (E) |
| `docs/pixelelated/art/wordmark/sunrise.svg` | 12437 | `3dd5ff8a2ad42d99` | (E) |
| `docs/rasteratops/art/Tiny5-OFL.txt` | 4384 | `6e24408062bb54fd` | (E) |
| `docs/rasteratops/art/rasteratops-wordmark.svg` | 6241 | `707f8d21d09bdcfd` | (E) |

## The ledgers (ruling (a), (d), (e))

"A ledger, not a reference" -- the renovation records, the running ledgers and
the named ledger rows. None is edited (the lane never runs a `--write`).

| path | class | misleading sentence (if any) | where it goes |
| --- | --- | --- | --- |
| `docs/reviews/*` (12) + `docs/reviews/briefs/p1-survey.md` (1) | ledger-reviews | L-01 (resolved at dispatch), L-28, L-29 | the coordinator's; the renovation's own records |
| `docs/releases/catalog.md` | ledger-named | (generated; L-15's catalog gap) | `tools/release-catalog --write`, coordinator |
| `docs/pr-series/map.txt` | ledger-named | L-27 (two deleted paths) | `tools/pr-stack-check` input, coordinator |
| `docs/releases/rc-accept.txt` | ledger-named | L-25, L-26 | `tools/rc-preflight` input, coordinator |
| `docs/vm-qa-log.md` | ledger-named | -- | the running VM QA ledger |
| `docs/cloud-sync-changelog.md` | ledger-named | L-23 (redirecting link at `:4`) | the running change log |
| `docs/rasteratops/p0-sweep-hits.txt` | ledger-named | -- (the sweep's hits as found, open item 25) | the P0 baseline (`NAMING.md:30`) |
| `plans/conflict-resolution/...md` | ledger-plan | L-24 (superseded, unmarked) | one historical-plan row (ruling (d)) |

## The identity words (over the 223 text rows, tip; case-sensitive, `-w`)

Generated; the `after stage E` column fills at E. Allowlists per `NAMING.md`
(retained ROCKNIX labels/paths/upstream credit; the character/handle; historical
`docs/rasteratops/` names and paths).

| term | lines | files | note |
| --- | ---: | ---: | --- |
| `Rasteratops` | 27 | 11 | the character/historical folders (allowed) |
| `rasteratops` | 31 | 20 | historical paths/handle (allowed) |
| `ROCKNIX` | 3271 | 56 | upstream project, retained labels/paths (allowed); L-05's runbook is the exception |
| `maxengel` | 28 | 6 | the account (allowed); L-22/L-23 the stale-remote cases |
| `pixelelated` | 241 | 51 | the OS name |
| `rocknix.worktrees` | 4 | 3 | L-40 (the retired path word; coordinator's rules) |
| `Pixelelated`/`PIXELELATED` | 0 | 0 | D-WORKFLOW-144 holds |

## The retired names (case-insensitive, tip)

| term | lines | files | note |
| --- | ---: | ---: | --- |
| `cloud_migrate_layout` | 21 | 7 | L-04 (docs, present tense); shipped OS (`projects`+`packages`+`scripts`) = 0; `tools/` (fork-only QA) = 127 |
| `rclonectl` | 0 | 0 | gone |
| `rubber-duck` | 1 | 1 | the dated `rules-sweep-2026-09-12.md` (allowed) |
| `.github/instructions` | 0 | 0 | gone |

## The runs (stage B; each with its figure and *a FAIL would mean ...*)

All `LC_ALL=C`, counts by `/usr/bin/grep`, at the lane's tip `f60c2c08bf`.

| run | result | a FAIL would mean |
| --- | --- | --- |
| export the 254 at the tip | 254 files | a path of the membership is absent at the tip (ruling (p)) |
| binaries name/size/sha256 | 31 (28 png, 2 pdf, 1 gz) | a binary moved or the carve miscounted |
| art-text name/size/sha256 | 18 | an art file moved or the carve miscounted |
| byte identity vs UP `651150fc88` (documentation+licenses) | 15 files changed | the fork drifted further from upstream than L-41 records |
| identity words (lines/files) | per § The identity words | a retired identity appears where `NAMING.md` forbids |
| retired names | per § The retired names | a retired script/name lives in the shipped product |
| dead relative Markdown links | 511 scanned, **0 dead** (resolved against the worktree) | a reference points nowhere |
| decision IDs cited vs register | register 716, cited 442, **0 unresolved** | a cite names no decided row (L-38) |
| the 46 lead FAIL-first checks | each prints its defect at the tip (see § The table) | a lead's premise no longer holds |

**Note (inherited:coordinator):** the brief's R3 C24 says *"product-tree hits
for `cloud_migrate_layout` (projects packages scripts tools): 0"*. At the lane's
tip the shipped OS (`projects`+`packages`+`scripts`) is **0**, but `tools/`
carries **127** (fork-only QA/test tooling: `cloud-pair-migration`,
`last-good-scripts-test`, `rasteratops-cloud-layout-test`, the VM-cloud tests, a
migration walk). L-04's premise (the shipped product has no `cloud_migrate_layout`)
holds; the brief's parenthetical that includes `tools` and reads 0 is inaccurate
at the tip -- a coordinator-owned brief-evidence erratum, flagged on #686.

## Proofs

| claim | proved |
| --- | --- |
| the membership is 254 at the tip | tree (export) |
| the carve classes sum to 254, v2 figures | tool-run (the § 2 classifier on `block-2.txt`) |
| each lead's defect prints at the tip | tree / tool-run / record (per § The table) |
| 0 dead links, 0 unresolved IDs, 0 capitalised brand | tree / tool-run |
| the binaries and art bytes are unchanged at the tip | tree (sha256) |

## The streams

Filled at stage E, under the coordinator's stream brief (`t39-streams.md`); one
row per fix with its check lines. Empty at stage B.

## What the coordinator and the next slices inherit

Named here, read at stage A/B, never edited by the lane:

- **coordinator:** L-01, L-03 (`vm-first.md`'s line), L-15 (catalog regen, #964),
  L-25, L-27, L-28, L-29, L-31, L-33, L-34, L-35, L-36, L-37 (erratum, present),
  L-40; the R3 C24 brief-evidence erratum above; L-38's resolution (D-WORKFLOW-188
  carried by the P1 merge).
- **the interface lanes (#700):** L-17 (where no decided row is contradicted),
  L-32 (the map's line-cites).
- **#270:** L-15 (the device-facts tool and the row-against-rule).
- **#509:** L-30 (the rename batch).
- **#511:** L-22 (the site remote).
- **#947:** L-38 (the citation guard).
- **#1013:** L-39 (the versioning criterion).
- **the next upstream base merge:** L-41 (the per-device tables behind upstream).
- **#528:** L-43, L-44, L-45 (licence/notice text).
- **#585:** L-46, and `docs/upstream/README.md`'s run-together hits (L-11's share).

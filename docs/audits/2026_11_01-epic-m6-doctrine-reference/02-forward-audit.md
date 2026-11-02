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

Generated at stage C by `tools/t39-tables.py coverage` from the checker's baseline probes
(`stage-c/probes/`, t39-checks.sh's `--out` of run (i)) and the export, each file checked
byte-identical to its blob at the tip first; one row per path of the 254, the path in
backticks first. *probes* are the checker's per-file counts (links, backticked paths, `tools/`
names, decision IDs, identity and retired-name lines), dead or unresolved in brackets; the
Q1-Q7 cell names each question a lead answers on the row and gives the reason for the rest;
the disposition is § 6's Coverage set, the strongest of the row's leads (fix, inherited,
#528, #585, ledger, none). L-18's rows come from the Q5 generator's LOW-INBOUND set: an undated
low-inbound reference document is `fix` (a dated first line), a dated one `none` (§ 4 question 2
decides its keeping). The generator's own line: `DISPOSITIONS #528 2 #585 3 fix 34 inherited 20 ledger 50 none 145 total 254`
(`stage-c/tables/coverage.err`).

| path | group | tier | lines | kind | class | probes | Q1-Q7 | disposition |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| `LICENSE.md` | LICENSE.md | fork-own | 18 | text | read-only-528 | links 1 · identity 1 | Q4 L-42; Q2 L-43; Q4 L-45; the rest n/a (no other lead) | inherited:coordinator |
| `README.md` | README.md | fork-own | 23 | text | edit-scope | links 4 | Q4 Q7 L-02; the rest n/a (no other lead) | fix |
| `TRADEMARK.md` | TRADEMARK.md | fork-own | 38 | text | edit-under-naming | paths 1 · identity 1 | Q2 L-43; Q4 L-45; the rest n/a (no other lead) | #528 |
| `docs/backup-contents.md` | docs/* | fork-own | 100 | text | edit-scope | IDs 1 | Q2 Q4 L-07; Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/cloud-save-integrity.md` | docs/* | fork-own | 100 | text | edit-scope | tools 4 · IDs 1 | Q4 L-06; the rest n/a (no other lead) | fix |
| `docs/cloud-sync-changelog.md` | docs/* | fork-own | 3581 | text | ledger-named | links 12 · paths 13 · tools 31 · IDs 244 · identity 14 · retired 4 | Q2 L-23; the rest n/a (no other lead) | ledger |
| `docs/cloud-vocabulary-audit.md` | docs/* | fork-own | 240 | text | edit-scope | paths 4 · IDs 5 · retired 2 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/conflict-wizard-ia.md` | docs/* | fork-own | 323 | text | edit-scope | links 4 · IDs 25 | Q4 L-17; the rest n/a (no other lead) | inherited:the interface lanes |
| `docs/council-limits.md` | docs/* | fork-own | 54 | text | edit-scope | paths 1 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/council-mistral-counter.md` | docs/* | fork-own | 127 | text | edit-scope | links 1 · paths 1 | Q5 Q6 L-12; the rest n/a (no other lead) | fix |
| `docs/council-staged-attempts.md` | docs/* | fork-own | 144 | text | edit-scope | links 4 · paths 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/council-staged-controller.md` | docs/* | fork-own | 279 | text | edit-scope | links 6 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/council-staged-derived-packages.md` | docs/* | fork-own | 101 | text | edit-scope | links 3 · paths 2 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/council-staged-derived-runtime.md` | docs/* | fork-own | 298 | text | edit-scope | links 1 · paths 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/council-staged-readings.md` | docs/* | fork-own | 180 | text | edit-scope | links 4 · paths 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/council-staged-rereads.md` | docs/* | fork-own | 129 | text | edit-scope | paths 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/council-staged-sources.md` | docs/* | fork-own | 151 | text | edit-scope | links 4 · paths 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/device-flashing-runbook.md` | docs/* | fork-own | 534 | text | edit-scope | paths 6 · tools 1 | Q2 Q4 L-05; the rest n/a (no other lead) | fix |
| `docs/device-testing-policy.md` | docs/* | fork-own | 122 | text | edit-scope | paths 2 · tools 2 · IDs 14 | Q4 L-03; Q3 L-16; Q7 L-36; the rest n/a (no other lead) | fix |
| `docs/es-menu-map.md` | docs/* | fork-own | 989 | text | edit-scope | links 76 · paths 1 · tools 5 · IDs 67 | Q4 Q7 L-08; Q7 L-11; Q4 L-32; the rest n/a (no other lead) | fix |
| `docs/pixelelated/art/README.md` | docs/pixelelated/ | fork-own | 26 | text | edit-scope | links 1 · paths 1 · tools 1 (1 absent) · IDs 2 | Q6 L-14; the rest n/a (no other lead) | none |
| `docs/pixelelated/art/Tiny5-OFL.txt` | docs/pixelelated/ | fork-own | 93 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/pixelelated-wordmark.svg` | docs/pixelelated/ | fork-own | 263 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/proofs/artifact-checks.json` | docs/pixelelated/ | fork-own | 326 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/proofs/backgrounds.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/proofs/boot-shutdown-640x480.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/proofs/small-sizes.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/dual.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/monochrome-dark.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/monochrome-light.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/neon.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/ocean.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/scanline.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/spectrum.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/1x/sunrise.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/dual.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/monochrome-dark.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/monochrome-light.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/neon.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/ocean.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/scanline.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/spectrum.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/2x/sunrise.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/dual.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/monochrome-dark.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/monochrome-light.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/neon.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/ocean.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/scanline.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/spectrum.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/raster/4x/sunrise.png` | docs/pixelelated/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/pixelelated/art/source/font.json` | docs/pixelelated/ | fork-own | 10 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/source/generate.py` | docs/pixelelated/ | fork-own | 180 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/source/palettes.json` | docs/pixelelated/ | fork-own | 10 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/source/pixelelated-live-text.svg` | docs/pixelelated/ | fork-own | 18 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/source/wordmark.css` | docs/pixelelated/ | fork-own | 10 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark-system.md` | docs/pixelelated/ | fork-own | 334 | text | edit-scope | links 5 · paths 1 · IDs 1 · identity 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/pixelelated/art/wordmark/dual.svg` | docs/pixelelated/ | fork-own | 167 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark/monochrome-dark.svg` | docs/pixelelated/ | fork-own | 163 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark/monochrome-light.svg` | docs/pixelelated/ | fork-own | 163 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark/neon.svg` | docs/pixelelated/ | fork-own | 167 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark/ocean.svg` | docs/pixelelated/ | fork-own | 167 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark/scanline.svg` | docs/pixelelated/ | fork-own | 167 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark/spectrum.svg` | docs/pixelelated/ | fork-own | 167 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/art/wordmark/sunrise.svg` | docs/pixelelated/ | fork-own | 167 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/pixelelated/cloud-folder-flow-review.md` | docs/pixelelated/ | fork-own | 632 | text | edit-scope | links 69 · paths 1 · IDs 5 | Q7 L-11; the rest n/a (no other lead) | fix |
| `docs/pixelelated/cloud-folders.md` | docs/pixelelated/ | fork-own | 35 | text | edit-scope | IDs 1 · identity 1 | Q7 L-10; the rest n/a (no other lead) | fix |
| `docs/pixelelated/rename-plan.md` | docs/pixelelated/ | fork-own | 77 | text | edit-scope | paths 4 · IDs 4 · identity 5 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/pixelelated/site-dns.md` | docs/pixelelated/ | fork-own | 62 | text | edit-scope | paths 1 · IDs 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/pixelelated/site-plan.md` | docs/pixelelated/ | fork-own | 147 | text | edit-scope | links 2 · paths 2 (1 dead) · IDs 2 · identity 1 | Q6 L-13; Q4 L-22; the rest n/a (no other lead) | fix |
| `docs/pr-series/es-review-guide.md` | docs/pr-series/ | fork-own | 124 | text | edit-scope | paths 1 · IDs 4 | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/pr-series/map.txt` | docs/pr-series/ | fork-own | 199 | text | ledger-named | tools 3 · IDs 2 · retired 2 | Q6 L-27; the rest n/a (no other lead) | inherited:coordinator |
| `docs/ra-offline/2026_09_13-phase-1-design-note.md` | docs/ra-offline/ | fork-own | 590 | text | edit-scope | paths 26 (21 dead) · tools 3 · IDs 8 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/ra-offline/rocknix-org-offline-achievements.md` | docs/ra-offline/ | fork-own | 59 | text | edit-scope | paths 3 (2 dead) | Q6 L-13; Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/rasteratops/art/README.md` | docs/rasteratops/ | fork-own | 16 | text | edit-scope | tools 1 (1 absent) · IDs 5 | Q6 L-19; the rest n/a (no other lead) | ledger |
| `docs/rasteratops/art/Tiny5-OFL.txt` | docs/rasteratops/ | fork-own | 93 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/rasteratops/art/icon-interim-2026-10-01.png` | docs/rasteratops/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/rasteratops/art/rasteratops-wordmark.svg` | docs/rasteratops/ | fork-own | 151 | text | art-bytes | -- | n/a: art bytes, tabled and never edited (ruling (o)) | none |
| `docs/rasteratops/candidate-source-plan.md` | docs/rasteratops/ | fork-own | 80 | text | edit-scope | links 2 · paths 4 · IDs 4 · identity 1 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/rasteratops/cloud-folder-state-table.md` | docs/rasteratops/ | fork-own | 334 | text | edit-scope | links 1 · paths 1 · tools 5 · IDs 13 · identity 2 · retired 4 | Q2 L-21; the rest n/a (no other lead) | ledger |
| `docs/rasteratops/cloud-layout.md` | docs/rasteratops/ | fork-own | 116 | text | edit-scope | links 1 · paths 1 · tools 1 · IDs 4 · retired 2 | Q1 Q3 L-04; Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/rasteratops/cloud-provider-2026-09-30.md` | docs/rasteratops/ | fork-own | 68 | text | edit-scope | IDs 3 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/rasteratops/p0-read.md` | docs/rasteratops/ | fork-own | 70 | text | edit-scope | paths 34 (1 dead) · IDs 10 | Q5 L-18; Q6 L-20; the rest n/a (no other lead) | ledger |
| `docs/rasteratops/p0-sweep-hits.txt` | docs/rasteratops/ | fork-own | 2419 | text | ledger-named | tools 1 · IDs 77 · identity 20 · retired 28 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/rasteratops/p0-sweep.md` | docs/rasteratops/ | fork-own | 142 | text | edit-scope | paths 79 (1 dead) · IDs 4 | Q5 L-18; Q6 L-20; the rest n/a (no other lead) | ledger |
| `docs/rasteratops/p0-updater.md` | docs/rasteratops/ | fork-own | 70 | text | edit-scope | paths 5 · IDs 1 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/rasteratops/raofflineproxy-refresh.md` | docs/rasteratops/ | fork-own | 195 | text | edit-scope | links 6 · paths 8 · IDs 3 · identity 2 | Q2 L-21; the rest n/a (no other lead) | ledger |
| `docs/rasteratops/release-readiness.md` | docs/rasteratops/ | fork-own | 990 | text | edit-scope | links 49 · paths 13 · IDs 22 · identity 4 · retired 2 | Q7 L-11; Q2 Q7 L-30; the rest n/a (no other lead) | fix |
| `docs/rasteratops/support-matrix.md` | docs/rasteratops/ | fork-own | 162 | text | edit-scope | links 22 · paths 7 · tools 3 · IDs 15 | Q7 L-11; Q2 Q7 L-30; the rest n/a (no other lead) | fix |
| `docs/releases/0.0.1-release-note-draft.md` | docs/releases/ | fork-own | 43 | text | edit-scope | links 3 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/releases/0.0.1-release-note-evidence.md` | docs/releases/ | fork-own | 40 | text | edit-scope | links 32 · paths 1 · IDs 3 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/releases/0.0.1-release-preparation.md` | docs/releases/ | fork-own | 115 | text | edit-scope | links 8 · IDs 10 | Q7 L-11; the rest n/a (no other lead) | fix |
| `docs/releases/catalog.md` | docs/releases/ | fork-own | 112 | text | ledger-named | links 1 · tools 8 · IDs 36 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/releases/device-facts.md` | docs/releases/ | fork-own | 31 | text | edit-scope | links 9 · paths 1 · tools 1 · IDs 8 | Q7 L-11; Q4 Q6 L-15; the rest n/a (no other lead) | fix |
| `docs/releases/next-candidate-scope.md` | docs/releases/ | fork-own | 233 | text | edit-scope | links 12 · paths 1 · tools 4 · IDs 12 | Q7 L-11; the rest n/a (no other lead) | fix |
| `docs/releases/next-candidate-work.md` | docs/releases/ | fork-own | 963 | text | edit-scope | links 104 · IDs 13 | Q4 L-09; Q7 L-11; the rest n/a (no other lead) | fix |
| `docs/releases/pr/01-build.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/02-generic-x64.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/03-evidence.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/04-settings.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/05-network.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/06-retroachievements.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/07-cloud-setup.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/08-saves.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q1 Q3 L-04; Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/09-retroarch.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/10-es-pin.md` | docs/releases/ | fork-own | 7 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/pr/11-interface.md` | docs/releases/ | fork-own | 13 | text | edit-scope | paths 1 · IDs 1 | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/rc-accept.txt` | docs/releases/ | fork-own | 17 | text | ledger-named | tools 1 · IDs 9 · identity 1 | Q2 L-25; Q4 L-26; the rest n/a (no other lead) | inherited:coordinator |
| `docs/releases/rc1-20260929-release-note.md` | docs/releases/ | fork-own | 38 | text | edit-scope | paths 1 · IDs 2 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/releases/rc2-20260929-release-note.md` | docs/releases/ | fork-own | 32 | text | edit-scope | paths 1 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md` | docs/releases/ | fork-own | 13 | text | edit-scope | paths 5 (5 dead) | Q6 L-13; Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/releases/versioning.md` | docs/releases/ | fork-own | 138 | text | edit-scope | paths 3 · tools 2 · IDs 3 | Q7 L-11; Q4 L-39; the rest n/a (no other lead) | fix |
| `docs/reviews/README.md` | docs/reviews/ | fork-own | 165 | text | ledger-reviews | paths 10 · tools 11 · IDs 7 | Q6 L-01; the rest n/a (no other lead) | ledger |
| `docs/reviews/areas.json` | docs/reviews/ | fork-own | 124 | text | ledger-reviews | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/reviews/assessment.md` | docs/reviews/ | fork-own | 108 | text | ledger-reviews | paths 32 · tools 8 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/reviews/briefs/p1-survey.md` | docs/reviews/briefs/ | fork-own | 386 | text | ledger-reviews | paths 81 (1 dead) · tools 30 · IDs 20 · retired 2 | Q6 L-01; the rest n/a (no other lead) | ledger |
| `docs/reviews/build-path-read.md` | docs/reviews/ | fork-own | 216 | text | ledger-reviews | paths 44 · tools 14 · IDs 26 | Q6 L-01; the rest n/a (no other lead) | ledger |
| `docs/reviews/cross-reference.md` | docs/reviews/ | fork-own | 113 | text | ledger-reviews | paths 1 · tools 1 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/reviews/inventory.md` | docs/reviews/ | fork-own | 1515 | text | ledger-reviews | paths 1434 · tools 25 · IDs 1 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/reviews/order.md` | docs/reviews/ | fork-own | 806 | text | ledger-reviews | paths 21 · tools 36 · IDs 51 | Q7 L-29; the rest n/a (no other lead) | inherited:coordinator |
| `docs/reviews/p1-tracking.md` | docs/reviews/ | fork-own | 449 | text | ledger-reviews | paths 27 · tools 19 · IDs 18 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/reviews/plan-for-the-plan.md` | docs/reviews/ | fork-own | 499 | text | ledger-reviews | paths 65 · tools 29 · IDs 53 | Q6 L-01; Q4 L-28; the rest n/a (no other lead) | inherited:coordinator |
| `docs/reviews/slices.json` | docs/reviews/ | fork-own | 1048 | text | ledger-reviews | paths 12 · tools 28 · IDs 24 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/reviews/status.md` | docs/reviews/ | fork-own | 58 | text | ledger-reviews | tools 1 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/rules-sweep-2026-09-12.md` | docs/* | fork-own | 277 | text | edit-scope | paths 38 (3 dead) · tools 25 · IDs 116 · identity 1 · retired 4 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/save-history-consensus-amendment.md` | docs/* | fork-own | 116 | text | edit-scope | paths 1 · IDs 20 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/save-history-gap-analysis.md` | docs/* | fork-own | 92 | text | edit-scope | paths 2 · IDs 2 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/save-history-plan-delta.md` | docs/* | fork-own | 40 | text | edit-scope | paths 3 · IDs 16 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/save-history-serial-model-addendum.md` | docs/* | fork-own | 111 | text | edit-scope | paths 1 · IDs 11 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/save-manifest-alignment-review.md` | docs/* | fork-own | 98 | text | edit-scope | paths 4 (1 dead) · tools 1 · IDs 33 | Q5 L-18; the rest n/a (no other lead) | none |
| `docs/save-manifest-schema.md` | docs/* | fork-own | 555 | text | edit-scope | links 2 · paths 4 · IDs 26 | n/a: no lead and no unexcused probe hit at the tip | none |
| `docs/savestate-compat-test.md` | docs/* | fork-own | 117 | text | edit-scope | -- | Q5 Q7 L-18; the rest n/a (no other lead) | fix |
| `docs/technical-appendix-cloud-sync-and-offline-achievements.md` | docs/* | fork-own | 3 | text | edit-scope | paths 3 (2 dead) · IDs 1 | Q6 L-13; Q5 L-18; the rest n/a (no other lead) | fix |
| `docs/upstream/2026-10-15-queue-reconciliation/README.md` | docs/upstream/ | fork-own | 37 | text | read-only-585 | paths 1 · IDs 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/2026-10-15-queue-reconciliation/SHA256SUMS` | docs/upstream/ | fork-own | 5 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/2026-10-15-queue-reconciliation/member-manifest.json` | docs/upstream/ | fork-own | 397 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/2026-10-15-queue-reconciliation/originals.tar.gz` | docs/upstream/ | fork-own | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `docs/upstream/2026-10-15-queue-reconciliation/publication-receipt.json` | docs/upstream/ | fork-own | 9 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/2026-10-15-queue-reconciliation/retention-verification.json` | docs/upstream/ | fork-own | 23 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/README.md` | docs/upstream/ | fork-own | 139 | text | read-only-585 | links 15 · IDs 2 | Q7 L-11; Q4 L-46; the rest n/a (no other lead) | #585 |
| `docs/upstream/raofflineproxy/bounded-dns/README.md` | docs/upstream/ | fork-own | 34 | text | read-only-585 | links 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/bounded-dns/fix.patch` | docs/upstream/ | fork-own | 274 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/client-errors/README.md` | docs/upstream/ | fork-own | 20 | text | read-only-585 | links 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/client-errors/fix.patch` | docs/upstream/ | fork-own | 83 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/configured-login/README.md` | docs/upstream/ | fork-own | 20 | text | read-only-585 | links 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/configured-login/fix.patch` | docs/upstream/ | fork-own | 144 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/contribution-map.md` | docs/upstream/ | fork-own | 109 | text | read-only-585 | links 11 · paths 1 (1 dead) · IDs 2 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/early-consent/README.md` | docs/upstream/ | fork-own | 33 | text | read-only-585 | links 2 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/early-consent/fix.patch` | docs/upstream/ | fork-own | 81 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/image-completeness/README.md` | docs/upstream/ | fork-own | 24 | text | read-only-585 | links 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/image-completeness/fix.patch` | docs/upstream/ | fork-own | 207 | text | read-only-585 | identity 1 | Q4 L-46; the rest n/a (no other lead) | #585 |
| `docs/upstream/raofflineproxy/image-publication/README.md` | docs/upstream/ | fork-own | 42 | text | read-only-585 | links 1 · paths 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/image-publication/fix.patch` | docs/upstream/ | fork-own | 86 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/log-consent/README.md` | docs/upstream/ | fork-own | 20 | text | read-only-585 | links 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/log-consent/fix.patch` | docs/upstream/ | fork-own | 121 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/pixelelated-identity/README.md` | docs/upstream/ | fork-own | 35 | text | read-only-585 | links 1 · paths 2 · identity 2 | Q4 L-46; the rest n/a (no other lead) | #585 |
| `docs/upstream/raofflineproxy/pixelelated-identity/fix.patch` | docs/upstream/ | fork-own | 58 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/refresh-resilience/README.md` | docs/upstream/ | fork-own | 23 | text | read-only-585 | links 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/refresh-resilience/fix.patch` | docs/upstream/ | fork-own | 192 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/warning-sets/README.md` | docs/upstream/ | fork-own | 20 | text | read-only-585 | links 1 | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/upstream/raofflineproxy/warning-sets/fix.patch` | docs/upstream/ | fork-own | 87 | text | read-only-585 | -- | n/a: #585's queue, read-only (ruling (n)); nothing misleads at the tip | none |
| `docs/vm-qa-log.md` | docs/* | fork-own | 361 | text | ledger-named | links 25 · paths 17 · tools 55 · IDs 172 · retired 1 | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `documentation/PER_DEVICE_DOCUMENTATION/AMD64/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 137 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | fork-own | 128 | text | tabled-generic-x64 | -- | Q5 Q6 L-31; the rest n/a (no other lead) | inherited:coordinator |
| `documentation/PER_DEVICE_DOCUMENTATION/H700/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 128 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/RK3326/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 128 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/RK3399/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 133 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/RK3566/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 134 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/RK3576/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 134 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/RK3588/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 135 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/S922X/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 134 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/SDM845/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 130 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `documentation/PER_DEVICE_DOCUMENTATION/SM4450/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 140 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/SM6115/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 135 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/SM8250/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 141 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/SM8550/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 141 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/SM8650/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 141 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `documentation/PER_DEVICE_DOCUMENTATION/SM8750/SUPPORTED_EMULATORS_AND_CORES.md` | documentation/ | upstream-carried | 141 | text | read-only-upstream | -- | Q4 L-41; the rest n/a (no other lead) | inherited:the next upstream base merge |
| `licenses/0BSD.txt` | licenses/ | upstream-carried | 5 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/AETHERSX2.pdf` | licenses/ | upstream-carried | -- | binary | ledger-binary | -- | Q1 L-44; the rest n/a (no other lead) | #528 |
| `licenses/AFL-2.1.txt` | licenses/ | upstream-carried | 45 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Apache-2.0.txt` | licenses/ | upstream-carried | 183 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Artistic-2.0.txt` | licenses/ | upstream-carried | 85 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Autoconf-exception-3.0.txt` | licenses/ | upstream-carried | 26 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/BSD-2-Clause.txt` | licenses/ | upstream-carried | 9 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/BSD-3-Clause.txt` | licenses/ | upstream-carried | 11 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/BSD-4-Clause.txt` | licenses/ | upstream-carried | 14 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/BSL-1.0.txt` | licenses/ | upstream-carried | 23 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/BigPEmu_ReadMe.txt` | licenses/ | upstream-carried | 356 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Bitstream-Charter.txt` | licenses/ | upstream-carried | 9 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/CC-BY-NC-SA-3.0.txt` | licenses/ | upstream-carried | 360 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/CC-BY-SA-4.0.txt` | licenses/ | upstream-carried | 171 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/CDDL-1.0.txt` | licenses/ | upstream-carried | 118 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/ClArtistic.txt` | licenses/ | upstream-carried | 61 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Classpath-exception-2.0.txt` | licenses/ | upstream-carried | 3 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/DRASTIC.pdf` | licenses/ | upstream-carried | -- | binary | ledger-binary | -- | n/a: a ledger, not a reference (ruling (a)) | ledger |
| `licenses/EPL-1.0.txt` | licenses/ | upstream-carried | 73 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/FTL.txt` | licenses/ | upstream-carried | 79 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/GPL-2.0-only.txt` | licenses/ | upstream-carried | 311 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/GPL-2.0-or-later.txt` | licenses/ | upstream-carried | 311 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/GPL-3.0-only.txt` | licenses/ | upstream-carried | 232 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/GPL-3.0-or-later.txt` | licenses/ | upstream-carried | 232 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/HPND-sell-variant.txt` | licenses/ | upstream-carried | 19 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/HPND.txt` | licenses/ | upstream-carried | 7 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/IJG.txt` | licenses/ | upstream-carried | 38 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/ISC.txt` | licenses/ | upstream-carried | 15 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/JasPer-2.0.txt` | licenses/ | upstream-carried | 17 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LGPL-2.0-only.txt` | licenses/ | upstream-carried | 444 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LGPL-2.0-or-later.txt` | licenses/ | upstream-carried | 444 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LGPL-2.1-only.txt` | licenses/ | upstream-carried | 462 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LGPL-2.1-or-later.txt` | licenses/ | upstream-carried | 462 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LGPL-3.0-only.txt` | licenses/ | upstream-carried | 304 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LGPL-3.0-or-later.txt` | licenses/ | upstream-carried | 304 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LLVM-exception.txt` | licenses/ | upstream-carried | 15 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-7-Zip.txt` | licenses/ | upstream-carried | 146 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-ARM-Mali-EULA.txt` | licenses/ | upstream-carried | 194 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-FLIRC.txt` | licenses/ | upstream-carried | 32 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-Free-to-use.txt` | licenses/ | upstream-carried | 5 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-FreeDO.txt` | licenses/ | upstream-carried | 27 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-HIDAPI-orig.txt` | licenses/ | upstream-carried | 9 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-MAME.txt` | licenses/ | upstream-carried | 35 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-NextPVR.txt` | licenses/ | upstream-carried | 17 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-Nmap.txt` | licenses/ | upstream-carried | 583 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-Non-commercial.txt` | licenses/ | upstream-carried | 53 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-PublicDomain.txt` | licenses/ | upstream-carried | 10 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-bk-emulator.txt` | licenses/ | upstream-carried | 5 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-fdk-aac.txt` | licenses/ | upstream-carried | 92 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-firmware-Broadcom.txt` | licenses/ | upstream-carried | 65 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-linux-firmware.txt` | licenses/ | upstream-carried | 6 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-ngrep.txt` | licenses/ | upstream-carried | 69 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/LicenseRef-nonfree.txt` | licenses/ | upstream-carried | 4 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/MIT-CMU.txt` | licenses/ | upstream-carried | 7 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/MIT-open-group.txt` | licenses/ | upstream-carried | 20 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/MIT.txt` | licenses/ | upstream-carried | 20 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/MPL-1.1.txt` | licenses/ | upstream-carried | 401 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/MPL-2.0.txt` | licenses/ | upstream-carried | 292 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/NCSA.txt` | licenses/ | upstream-carried | 15 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/OFL-1.1.txt` | licenses/ | upstream-carried | 84 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/PSF-2.0.txt` | licenses/ | upstream-carried | 47 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/SGI-B-2.0.txt` | licenses/ | upstream-carried | 12 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/UnRAR.txt` | licenses/ | upstream-carried | 41 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Unicode-3.0.txt` | licenses/ | upstream-carried | 39 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Unlicense.txt` | licenses/ | upstream-carried | 25 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Vim.txt` | licenses/ | upstream-carried | 76 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/X11.txt` | licenses/ | upstream-carried | 13 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/XFree86-1.1.txt` | licenses/ | upstream-carried | 16 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/Zlib.txt` | licenses/ | upstream-carried | 19 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/blessing.txt` | licenses/ | upstream-carried | 5 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/bzip2-1.0.6.txt` | licenses/ | upstream-carried | 15 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/curl.txt` | licenses/ | upstream-carried | 20 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/hdparm.txt` | licenses/ | upstream-carried | 9 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/libpng-2.0.txt` | licenses/ | upstream-carried | 33 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `licenses/libtiff.txt` | licenses/ | upstream-carried | 8 | text | read-only-upstream | -- | n/a: upstream-carried, byte-identical to the merge base, read-only (ruling (a)) | none |
| `plans/conflict-resolution/vita-style-conflict-resolution.md` | plans/ | fork-own | 223 | text | ledger-plan | paths 13 · tools 6 · IDs 25 | Q5 Q7 L-18; Q1 Q5 L-24; the rest n/a (no other lead) | ledger |

## The table

One row per misleading statement (the leads of § 3, L-01 to L-46). `path:line` is at the
dispatch tip; *tip* is the FAIL-first check's result, run this stage. The
disposition set is § 6's: `fix`, `inherited:<owner>`, `ledger`, `#528`, `#585`
(L-14 resolves to a § Coverage `none` and is marked so). By primary disposition
over the 46 rows (`COUNTS TABLE #528 3 #585 1 fix 16 inherited 16 ledger 9 none 1 total 46`):
16 `fix`, 16 `inherited:<owner>`, 9 `ledger`, 3 `#528`, 1 `#585`, 1 `none` (`L-14` -> § Coverage), total `46`.

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

Generated at stage C by `tools/t39-tables.py binaries` (`BINARIES 31`): size and
sha256 at the dispatch tip, read by `git show`, each also byte-identical in the export; the
`fixed-at` column is filled at stage E with `--fixed-at` (equal: these are never edited).
28 png, 2 pdf, 1 gz. Stage B's 16-character prefixes match these.

| path | size | sha256 at the dispatch tip | sha256 at fixed-at |
| --- | ---: | --- | --- |
| `docs/pixelelated/art/proofs/backgrounds.png` | 25167 | `19e30291d51ffeab673a1b344c4a402f0f97f83a2e53c73b6088ce77291d3672` | (stage E) |
| `docs/pixelelated/art/proofs/boot-shutdown-640x480.png` | 1393 | `a3211e6206231751725e3aaa0f4dbcdc9e9071529c45dc5f00a9f42b9fe7f504` | (stage E) |
| `docs/pixelelated/art/proofs/small-sizes.png` | 10195 | `596f6de6772b4cfdf8415cb7f25081135d40fa6a95ebde378d1cc14f6e457f2d` | (stage E) |
| `docs/pixelelated/art/raster/1x/dual.png` | 676 | `9fe50cf05c01a428c066d683075162aef291a02bd00e2f53f057f3c79399284e` | (stage E) |
| `docs/pixelelated/art/raster/1x/monochrome-dark.png` | 542 | `4771c7673637a78514ce78968cdb2e344f3a832dd77aa674c50a6c29729e1b7c` | (stage E) |
| `docs/pixelelated/art/raster/1x/monochrome-light.png` | 531 | `f59f0c98256912583298aa838cc86844873b04bca5fb455888482407c6d218e9` | (stage E) |
| `docs/pixelelated/art/raster/1x/neon.png` | 712 | `b1e993ec24beb2920694721f47c7a72d35e2e17524a2fa4b768076287853b160` | (stage E) |
| `docs/pixelelated/art/raster/1x/ocean.png` | 693 | `5fde4a652c49d024e944362c6236234b5812c7c66821ac1cc265376d2bdfe2fb` | (stage E) |
| `docs/pixelelated/art/raster/1x/scanline.png` | 653 | `b85abe09b8ea11593a8e3cf246de450be893fe1683a8fa375d4dda856d382aef` | (stage E) |
| `docs/pixelelated/art/raster/1x/spectrum.png` | 696 | `b43c4eeb8db061c4a75db7f7576e8ae403cb2c9a8b7c56d636b10456be0690ff` | (stage E) |
| `docs/pixelelated/art/raster/1x/sunrise.png` | 710 | `86ceca6c48315efd45ca32289ad9f2c4b4332046a88922770195f48efa005057` | (stage E) |
| `docs/pixelelated/art/raster/2x/dual.png` | 1589 | `7c39c02af9ed1fb11766181c47fabdae9c3e6b502102ca062e22093813f477df` | (stage E) |
| `docs/pixelelated/art/raster/2x/monochrome-dark.png` | 1293 | `c5ef49a820e21a055d58125e1e8371adeeacaac79934a93bcc71fb5d766ada37` | (stage E) |
| `docs/pixelelated/art/raster/2x/monochrome-light.png` | 1269 | `b0bea5b35c8a0d6ffb63402800e1cd0b814ad7a44bf73e136c66623533fe2a2c` | (stage E) |
| `docs/pixelelated/art/raster/2x/neon.png` | 1473 | `69345e13666ab714b2917506c1456b5ab4effa20f9f06b95475d2e53806bb418` | (stage E) |
| `docs/pixelelated/art/raster/2x/ocean.png` | 1467 | `411877033bb998babb5194018345cbb50155178fabcb0b936c6bb18777e0f414` | (stage E) |
| `docs/pixelelated/art/raster/2x/scanline.png` | 1384 | `a38293cae2957b2c74d45b475c61c869a9017be58fc5548df1e1235b030d896a` | (stage E) |
| `docs/pixelelated/art/raster/2x/spectrum.png` | 1450 | `0379e2602a68a3f289d9e7667fbf398e3716328fcf390f8737a589f135fb427d` | (stage E) |
| `docs/pixelelated/art/raster/2x/sunrise.png` | 1472 | `b7a09bb72fcb2c21a9c6d503fc0601536cbb2ce570b4ea47cba79e7c782c6bd9` | (stage E) |
| `docs/pixelelated/art/raster/4x/dual.png` | 4095 | `da6c65fe17397ca2c7183aac16044b53082e7adf9096f4192c6671668a6e977e` | (stage E) |
| `docs/pixelelated/art/raster/4x/monochrome-dark.png` | 3836 | `d14d7c953a42e71e759f7f200271fb0299ae9846d5f8995899787c8be1562761` | (stage E) |
| `docs/pixelelated/art/raster/4x/monochrome-light.png` | 3814 | `0ccbe161b9d815414615628a05d8639d94f58177c6f2ad5b280038549ecdb5c9` | (stage E) |
| `docs/pixelelated/art/raster/4x/neon.png` | 4112 | `98d4df292b81a8907b97e6d83546d367aab41fdfb2517b95b148591569946e82` | (stage E) |
| `docs/pixelelated/art/raster/4x/ocean.png` | 4092 | `979ecb9d6c729e0b56c2ea3c35e3067b86bd675ea679b719a7f25890e67c7de3` | (stage E) |
| `docs/pixelelated/art/raster/4x/scanline.png` | 3944 | `48d8dbd4b043940a662906a76a28549f9176054be3e3fb96cb32e61a0a830ace` | (stage E) |
| `docs/pixelelated/art/raster/4x/spectrum.png` | 4102 | `00a70a9a1943b8eb96237e5aba92bfeb6867ee90a73b30157c8ee536a42c6ef6` | (stage E) |
| `docs/pixelelated/art/raster/4x/sunrise.png` | 4102 | `23745b792dc63cd34feeaa74aa05d72f7a7bff095e508b7c076c09871b9e3ccb` | (stage E) |
| `docs/rasteratops/art/icon-interim-2026-10-01.png` | 718 | `1c7f06f8c28de2acb323940165bc1405e128139bcc34f5963e37521219398675` | (stage E) |
| `docs/upstream/2026-10-15-queue-reconciliation/originals.tar.gz` | 57557 | `88e015409159c98e6052252ee4bb429875d288e2907a7d3b785a1e6079c015d9` | (stage E) |
| `licenses/AETHERSX2.pdf` | 1005740 | `25bca10c4ceaf24d9bbf6148e8a5333afb4966550c4f002e0bc520c7dd0aab44` | (stage E) |
| `licenses/DRASTIC.pdf` | 239739 | `697815a8d51d416deb7e5e83ba763e8fb9dae0f7f6f74de12ca2a88a554f4e0a` | (stage E) |

## Art bytes (art-bytes, 18; ruling (o), widened at version 2)

Generated at stage C by `tools/t39-tables.py art` (`ART 18`); never edited.

| path | size | sha256 at the dispatch tip | sha256 at fixed-at |
| --- | ---: | --- | --- |
| `docs/pixelelated/art/Tiny5-OFL.txt` | 4384 | `6e24408062bb54fdc755e7701306f4e8bdc115d472c0e8b2f789e063038fa836` | (stage E) |
| `docs/pixelelated/art/pixelelated-wordmark.svg` | 25092 | `f5fa9839181693546ac97adb68e9af83e81e7e8fc0d55e11a10378636e2f0355` | (stage E) |
| `docs/pixelelated/art/proofs/artifact-checks.json` | 6822 | `1274ba1d67da2ec6c45f75e251615957fb70f2deb3e479f69af12d4c166c8d73` | (stage E) |
| `docs/pixelelated/art/source/font.json` | 359 | `cb3b043a4ce2bc2e3d400423ea0da21569131121e2cdbe50fe16809144747b3b` | (stage E) |
| `docs/pixelelated/art/source/generate.py` | 8802 | `0ccded4cb9693b81a3e203ca68080161c360d2b0fca67da5802ca8f6b540031e` | (stage E) |
| `docs/pixelelated/art/source/palettes.json` | 975 | `f0ef617d86144a19e2124e2c7a76741374d35ed25a893f41d701fe0c016d5c47` | (stage E) |
| `docs/pixelelated/art/source/pixelelated-live-text.svg` | 979 | `3afb3bcd7a470e01a15a3bc921e2efbe329d82c95cb06de25c59159642f1107c` | (stage E) |
| `docs/pixelelated/art/source/wordmark.css` | 1524 | `fb5ee55b1321e9d146599b248fbd1981cfe5653f860fe5ca64306d9a77622771` | (stage E) |
| `docs/pixelelated/art/wordmark/dual.svg` | 12441 | `850c80cc8affc6c527fee536681fcefb3e39726a4a62d7f03a345f9e94cfcd62` | (stage E) |
| `docs/pixelelated/art/wordmark/monochrome-dark.svg` | 12137 | `19fd14fbc2c905dc62aaa415bc358b3f399a7542747f0b4094e94838aadf4d56` | (stage E) |
| `docs/pixelelated/art/wordmark/monochrome-light.svg` | 12137 | `fbdbfa331d156f9c3605bc0989553d5e8c19ab285d645d63f3904358bbba795d` | (stage E) |
| `docs/pixelelated/art/wordmark/neon.svg` | 12437 | `29929e3460498aed68cad5ecf96bbc1a5fb5c905d6e9cf724c1d823e82b635ce` | (stage E) |
| `docs/pixelelated/art/wordmark/ocean.svg` | 12437 | `aa6b69817d6a1df715dc44da85d407721c11aec097bf563114ef4ef6d387e9d6` | (stage E) |
| `docs/pixelelated/art/wordmark/scanline.svg` | 12427 | `6fbc7dc7705df1580cc57a82b131ab3d4d68077e40df5c1635d1110675e14dfb` | (stage E) |
| `docs/pixelelated/art/wordmark/spectrum.svg` | 12437 | `3ccd73a324678be41ad5cabe3484523e8aa234e8afafc7bce4d739b8d6d9ba4d` | (stage E) |
| `docs/pixelelated/art/wordmark/sunrise.svg` | 12437 | `3dd5ff8a2ad42d996f325ef2bc30aec60231a3e69181f657e330ff3cc3be7d40` | (stage E) |
| `docs/rasteratops/art/Tiny5-OFL.txt` | 4384 | `6e24408062bb54fdc755e7701306f4e8bdc115d472c0e8b2f789e063038fa836` | (stage E) |
| `docs/rasteratops/art/rasteratops-wordmark.svg` | 6241 | `707f8d21d09bdcfd07b0871988fcf06d9ff9479e5b01907401839e7480c0bb03` | (stage E) |

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

Generated from `stage-c/checkers/identity-words.out` and `tools/t39-checks.sh`'s `identity`
step (`stage-c/probes/read-identity.tsv`); the `after stage E` column fills at E. Allowlists
per `NAMING.md` (retained ROCKNIX labels/paths/upstream credit; the character/handle;
historical `docs/rasteratops/` names and paths): `tools/allow-legit.txt` (58 entries),
`tools/allow-inherited.txt` (4 entries), `tools/allow-findings.txt` (17 entries).

| term | lines at tip | files at tip | after stage E | note |
| --- | ---: | ---: | --- | --- |
| `Rasteratops` | 27 | 11 | (stage E) | the character/historical folders (allowed; `rc-accept.txt:13` in `allow-inherited.txt`, L-25) |
| `rasteratops` | 31 | 20 | (stage E) | historical paths/handle (allowed; `cloud-sync-changelog.md:4` in `allow-legit.txt`, L-23) |
| `RASTERATOPS` | 4 | 4 | (stage E) | historical env/path references (allowed) |
| `ROCKNIX` | 3297 | 57 | (stage E) | upstream project, retained labels/paths (allowed); L-05's runbook (`21` lines) is the exception |
| `rocknix` | 1000 | 46 | (stage E) | upstream/path/user references (allowed; `site-plan.md:72` in `allow-findings.txt`, L-22) |
| `maxengel` | 28 | 6 | (stage E) | the account (allowed); `site-plan.md:72` (`allow-findings.txt`, L-22) and `cloud-sync-changelog.md:706-735` (`allow-legit.txt`, L-23) |
| `JELOS` | 7 | 7 | (stage E) | upstream lineage credits (allowed) |
| `pixelelated` | 243 | 51 | (stage E) | the OS name |
| `Pixelelated` | 0 | 0 | (stage E) | D-WORKFLOW-144 holds |
| `PIXELELATED` | 0 | 0 | (stage E) | D-WORKFLOW-144 holds |

## The retired names (case-insensitive, over the 223 text rows, tip)

Generated from `stage-c/checkers/retired-names.out` and `tools/t39-checks.sh`'s `retired`
step (`stage-c/probes/read-retired.tsv`, 51 hits across 9 files); the `after stage E`
column fills at E.

| term | lines at tip | files at tip | after stage E | note |
| --- | ---: | ---: | --- | --- |
| `cloud_migrate_layout` | 21 | 7 | (stage E) | 2 current-tense hits in `allow-findings.txt` (`docs/rasteratops/cloud-layout.md:16`, L-04); `docs/pr-series/map.txt:174` in `allow-inherited.txt` (L-27); 18 historical/dated in `allow-legit.txt`; shipped OS (`projects`+`packages`+`scripts`) = 0; `tools/` (fork-only QA) = 127 |
| `migrate.?layout` | 21 | 7 | (stage E) | same 21 lines as `cloud_migrate_layout` |
| `rebase --onto` | 2 | 2 | (stage E) | retired recipe cited as retired (`allow-legit.txt`) |
| `rclonectl` | 0 | 0 | (stage E) | gone |
| `\.github/instructions` | 0 | 0 | (stage E) | gone |
| `copilot` | 0 | 0 | (stage E) | gone |
| `rubber[- ]duck` | 1 | 1 | (stage E) | the dated `docs/reviews/rules-sweep-2026-09-12.md:62` (`allow-legit.txt`) |
| `\brclone config\b` | 2 | 2 | (stage E) | historical/upstream notes (`allow-legit.txt`) |
| `rocknix\.worktrees` | 4 | 3 | (stage E) | L-40 (retired path word in dated/review records; `allow-legit.txt` / `allow-inherited.txt`) |

## The runs (stages B and C; each with its figure and *a FAIL would mean ...*)

All `LC_ALL=C`, counts by `/usr/bin/grep`, re-run at `3f241300f0` (`stage-c/checkers.out` and `stage-c/checks-runs.out`).

### (a) The repository checkers and § 5 baseline runs (`stage-c/checkers.out`)

```text
== at 3f241300f0, 2026-11-02T05:29:37Z
rules-check                  rc=0  rules-check: 30 rule files, every one front-mattered and indexed (no evidence for the 254: rules-check reads .claude/rules/, CLAUDE.md and AGENTS.md, none of the 254)
register-check               rc=0  register-check: 716 IDs, each once; every citation in the live documents names a row
es-menu-map-check            rc=0  55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing
release-catalog              rc=0  release-catalog: current (99 cuts)
work-log-index               rc=0  work-log index: current
prose-check                  rc=0  self-test: PASS
ceremony-check               rc=0  nothing overdue.
hooks-test                   rc=0  PASS
box-check                    rc=0  box-check: 300 issue(s), 626 open checkbox(es), 0 fail, 13 issue(s) with rows to re-derive against
== the byte identity of the 254 against the merge base and upstream (R1 C12)
    162 vs c445081a59 absent
      2 vs c445081a59 differs
     90 vs c445081a59 identical
    163 vs 651150fc88 absent
     15 vs 651150fc88 differs
     76 vs 651150fc88 identical
== the secret scan in the hooks' form (compile rc at most 1, the runtime-built positive 1, then files with a hit)
secret regex compile rc=1
1
0
== non-ASCII files over the 223
86
== forbidden-terms over the 223, over empty input, and over a planted positive
forbidden-terms-check: 0 hits on stdin
over the 223 rc=0
forbidden-terms-check: 0 hits on stdin
over empty input rc=0
forbidden-terms-check: 1 line(s) on stdin carry a listed word
a planted positive rc=1
== the licence files against #359's recorded bytes (L-45)
LICENSE.md 1a277de267611abc4242e6a1e08ac2abac54316e7abcbf8ae7afd0a1dc98ec6c
TRADEMARK.md d46db25cb845b021cd7f1c13dabcd98d04e77d89a45968527e58abc9e3788761
== the releases a reader of README.md finds (L-02)
ROCKNIX RC1 (2026-09-29): cloud sync, offline achievements, Wi-Fi	Pre-release	rc1-20260929	2026-09-29T10:14:30Z
ROCKNIX dev build — 20260827	Latest	dev-20260827	2026-08-27T20:47:51Z
RK3326 build — 20260819	Pre-release	dev-rk3326-20260819	2026-08-21T05:52:15Z
== the removal check and the registers' removed lines, 86ebb6dffc to HEAD (expect no line, then 0)
0
== the host file: lines since the dispatch's 712, this lane's (the coordinator's own block excluded)
0
```

- **`tools/es-menu-map-check`:**
  - At the dispatch tip (`86ebb6dffc` / `3f241300f0`): `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (`rc=0`).
  - At `fixed-at`: filled at stage E, together with `git show <fixed-at>:docs/es-menu-map.md | /usr/bin/grep -c -E '^#+ Pending.*#570'` -> `0` (ruling (b)).

| run | result | a FAIL would mean |
| --- | --- | --- |
| `tools/rules-check` | `rc=0` (`30 rule files, every one front-mattered and indexed`; **no evidence for the 254**) | a rule file lost front matter or `AGENTS.md`/`CLAUDE.md` drifted |
| `tools/register-check` | `rc=0` (`716 IDs, each once; every citation in the live documents names a row`) | a duplicate ID in the register or a broken citation in the 4 reference docs `LIVE` covers |
| `tools/es-menu-map-check` | `rc=0` (`55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`) | an ES screen at the pin is missing from `docs/es-menu-map.md` |
| `tools/release-catalog --check` | `rc=0` (`release-catalog: current (99 cuts)`) | `docs/releases/catalog.md` drifted from the release `RECORD.txt` files |
| `tools/work-log-index --check` | `rc=0` (`work-log index: current`) | a work log was added or edited without `tools/work-log-index --write` |
| `tools/prose-check --self-test` | `rc=0` (`self-test: PASS`) | the prose checker's self-test regression suite broke |
| `tools/ceremony-check` | `rc=0` (`nothing overdue.`) | a ceremony or register/work-log obligation is overdue |
| `.githooks/hooks-test` | `rc=0` (`PASS`) | a git hook regression test failed |
| `tools/box-check` | `rc=0` (`300 issue(s), 626 open checkbox(es), 0 fail, 13 issue(s) with rows to re-derive against`) | an open issue checkbox violates D-QA-044/045 |
| export the 254 at the tip | 254 files (`rc=0`) | a path of the membership is absent at the tip (ruling (p)) |
| binaries name/size/sha256 | 31 (28 png, 2 pdf, 1 gz) | a binary moved or the carve miscounted |
| art-text name/size/sha256 | 18 | an art file moved or the carve miscounted |
| byte identity vs `c445081a59` / `651150fc88` | 90 identical vs MB; 76 identical, 15 differs vs UP | the fork drifted further from upstream than L-41 records |
| identity words (lines/files) | per § The identity words | a retired identity appears where `NAMING.md` forbids |
| retired names | per § The retired names | a retired script/name lives in the shipped product |
| dead relative Markdown links | 512 scanned (`t39-checks.sh` `links`), **0 dead** (resolved against the worktree) | a reference points nowhere |
| decision IDs cited vs register | register 716, cited distinct 442 (1272 citations), **0 `UNRESOLVED`** (D-WORKFLOW-188 carried by P1's merge, X03) | a cite names no decided or open row (L-38) |
| secret scan in hooks' form | compile `rc=1` (at most 1), runtime-built positive `1`, files with a hit `0` | a file of the 223 matches a secret pattern |
| non-ASCII files over the 223 | `86` files (informational; no positive required) | n/a (informational) |
| `tools/forbidden-terms-check` | over the 223 `rc=0`, over empty input `rc=0`, planted positive via `FORBIDDEN_PATTERNS` `rc=1` (`forbidden-terms-check: 1 line(s) on stdin carry a listed word`) | a file of the 223 carries a forbidden term |
| #359's two licence hashes | `LICENSE.md` `1a277de2...`, `TRADEMARK.md` `d46db25c...` (both equal #359's) | `LICENSE.md` or `TRADEMARK.md` changed since #359 |
| `gh release list` (L-02) | 3 releases (`rc1-20260929`, `dev-20260827`, `dev-rk3326-20260819`), 0 `pixelelated` | n/a (proves L-02's premise at the tip) |
| the 46 lead FAIL-first checks | each prints its defect at the tip (see § The table) | a lead's premise no longer holds |

### (b) `tools/t39-checks.sh` runs (`stage-c/checks-runs.out`)

Run (i) baseline (exit 0), run (ii) one mutation per step with its stub checked against the unfixed text first (each exit 1 naming its step), run (iii) the tip with `allow-findings.txt` withheld (exit 1 naming all 17 finding assertions across `identity`, `retired` and `leads`), and the 7 refusals (each exit 2, nothing checked). Run (iv) -- exit 0 at `fixed-at` with `allow-findings.txt` withheld -- runs at stage E.

```text
== (i) the baseline: the export at the dispatch tip, all three allowlists
i-baseline                         rc=0  TOTAL: 13 of 13 steps
== (ii) one mutation per step; each stub is first checked against the unfixed text (it must print 0 there)
ii-inventory                       rc=1  TOTAL: 12 of 13 steps
    FAIL  inventory  508 of 510 assertions; paths 254 text 222 binary 31
stub check: the python above asserted licenses/0BSD.txt's tier at HEAD is upstream-carried before the flip, rc=0
ii-scope                           rc=1  TOTAL: 12 of 13 steps
    FAIL  scope      9 of 11 assertions; CARVE art-bytes 18 edit-scope 69 edit-under-naming 1 ledger-binary 31 ledger-named 6 ledger-plan 1 ledger-reviews 12 read-only-528 1 read-only-585 27 read-only-upstream 87 tabled-generic-x64 1 total 254
stub check: README.md carries docs/no-such.md 0 times (expect 0)
ii-links                           rc=1  TOTAL: 12 of 13 steps
    FAIL  links      511 of 512 assertions; 512 relative links
stub check: docs/releases/versioning.md carries no-such-dir 0 times (expect 0)
ii-paths                           rc=1  TOTAL: 12 of 13 steps
    FAIL  paths      2060 of 2061 assertions; 39 allowlisted; 2061 backticked repository paths
stub check: docs/releases/versioning.md carries no-such-tool 0 times (expect 0)
ii-tools                           rc=1  TOTAL: 12 of 13 steps
    FAIL  tools      366 of 367 assertions; 2 allowlisted; 367 tools/ names
stub check: README.md carries Pixelelated 0 and Rasteratops OS 0 times (expect 0 and 0)
ii-identity                        rc=1  TOTAL: 12 of 13 steps
    FAIL  identity   58 of 60 assertions; 58 allowlisted
stub check: docs/pixelelated/cloud-folders.md carries rebase --onto 0 and cloud_migrate_layout 0 times (expect 0 and 0)
ii-retired                         rc=1  TOTAL: 12 of 13 steps
    FAIL  retired    51 of 54 assertions; 51 allowlisted
stub check: the register at HEAD has D-CLOUD-9999 0 times (expect 0)
ii-cites                           rc=1  TOTAL: 12 of 13 steps
    FAIL  cites      1272 of 1273 assertions; register IDs 716, citations 1273
ii-untouched-order                 rc=1  TOTAL: 12 of 13 steps
    FAIL  untouched  3 of 4 assertions; 1 non-merge commits since 3f241300f03d32c25283cb2c18c36d04baefa66d
ii-untouched-licence               rc=1  TOTAL: 12 of 13 steps
    FAIL  untouched  3 of 4 assertions; 1 non-merge commits since 3f241300f03d32c25283cb2c18c36d04baefa66d
ii-generated-commit                rc=1  TOTAL: 11 of 13 steps
    FAIL  untouched  3 of 4 assertions; 1 non-merge commits since 3f241300f03d32c25283cb2c18c36d04baefa66d
    FAIL  generated  2 of 3 assertions
ii-generated-tree                  rc=1  TOTAL: 12 of 13 steps
    FAIL  generated  2 of 3 assertions
ii-binaries                        rc=1  TOTAL: 12 of 13 steps
    FAIL  binaries   97 of 98 assertions; held 49 (ledger-binary 31, art-bytes 18)
ii-leads                           rc=1  TOTAL: 12 of 13 steps
    FAIL  leads      16 of 17 assertions; 16 allowlisted; 13 lead checks, 13 printing a defect
== (iii) the tip with allow-findings.txt withheld: exit 1, naming each of the slice's own findings
iii-tip-withheld                   rc=1  TOTAL: 10 of 13 steps
    FAIL  identity   57 of 58 assertions; 57 allowlisted
    FAIL  retired    49 of 51 assertions; 49 allowlisted
    FAIL  leads      0 of 16 assertions; 13 lead checks, 13 printing a defect
== refusals: exit 2, nothing checked
refuse-no-tree                     rc=2  t39-checks: refused: no --tree; nothing checked
refuse-checkout                    rc=2  t39-checks: refused: --tree /workspace/tmp/m6-t39/stage-c/mut/checkout is a checkout (it holds .git); nothing checked
refuse-no-paths                    rc=2  t39-checks: refused: --paths absent; nothing checked
refuse-paths-253                   rc=2  t39-checks: refused: --paths /workspace/tmp/m6-t39/stage-c/paths-253.txt has 253 lines, not 254; nothing checked
refuse-no-python3                  rc=2  t39-checks: refused: python3 missing; nothing checked
refuse-register                    rc=2  t39-checks: refused: the register is unreadable at 651150fc88; nothing checked
refuse-entry-no-reason             rc=2  t39-checks: refused: allow-legit.txt:67 is not `<path>:<line> <class> <reason>` (a class and a reason are required); nothing checked
```

### (c) `tools/t39-tables.py` counts and drift runs (`stage-c/tables/drift.out`)

```text
coverage             ok=0    COUNTS DISPOSITIONS #528 2 #585 3 fix 34 inherited 20 ledger 50 none 145 total 254
coverage             drift=1 FAIL  README.md in --export differs from its blob at 3f241300f0
binaries             ok=0    COUNTS BINARIES 31
binaries             drift=1 FAIL  licenses/AETHERSX2.pdf in --export differs from its blob at 3f241300f0
art                  ok=0    COUNTS ART 18
art                  drift=1 FAIL  docs/pixelelated/art/Tiny5-OFL.txt in --export differs from its blob at 3f241300f0
q4                   ok=0    COUNTS Q4 ids 442 (decided 435, open 7, unresolved 0); tools 69 (absent 2); issues 617; path references 2060
q4                   drift=1 FAIL  README.md in --export differs from its blob at 3f241300f0
q5                   ok=0    COUNTS Q5 rows 69; LOW-INBOUND files=33 lines=2770; population 70
q5                   drift=1 FAIL  README.md in --export differs from its blob at 3f241300f0
q6                   ok=0    COUNTS Q6 dead 41 (paths and tools) plus 3 inherited; rows 44
q6                   drift=1 FAIL  README.md in --export differs from its blob at 3f241300f0
missing-row          drift=1 FAIL  coverage rows 253, expected 254
```

**Note (inherited:coordinator):** the brief's R3 C24 says *"product-tree hits
for `cloud_migrate_layout` (projects packages scripts tools): 0"*. At the lane's
tip the shipped OS (`projects`+`packages`+`scripts`) is **0**, but `tools/`
carries **127** (fork-only QA/test tooling: `cloud-pair-migration`,
`last-good-scripts-test`, `rasteratops-cloud-layout-test`, the VM-cloud tests, a
migration walk). L-04's premise (the shipped product has no `cloud_migrate_layout`)
holds; the brief's parenthetical that includes `tools` and reads 0 is inaccurate
at the tip -- a coordinator-owned brief-evidence erratum, flagged on #686.

## Proofs

Every row corresponds 1-to-1 to a `^PROOF:` line in `00-running-log.md`, with its proof-class cell from `{tree, history, tool-run, fixture, design}` (§ 7 criterion 22).

| # | claim | evidence | proved |
| ---: | --- | --- | --- |
| 1 | the membership exports 254 files at the tip (`git archive HEAD`) | `/workspace/tmp/m6-t39/export/` (254 files) | `proved: tree` |
| 2 | the carve classifier on `block-2.txt` prints `edit-scope 68`, `edit-under-naming 1`, `CARVE total 254` | `stage-a/03-carve.out` | `proved: tool-run` |
| 3 | 0 dead relative Markdown links over 512 scanned, resolved against the worktree | `stage-c/runs/i-baseline/links.txt` | `proved: tree` |
| 4 | decision IDs: register 716, cited distinct 442, 0 unresolved (L-38; D-WORKFLOW-188 carried by P1's merge) | `stage-c/runs/i-baseline/cites.txt` | `proved: tool-run` |
| 5 | `Pixelelated`/`PIXELELATED` capitalised 0 (D-WORKFLOW-144 holds) | `stage-c/checkers/identity-words.out` | `proved: tree` |
| 6 | each of the 46 leads prints its defect at the tip | `02` § The table; `stage-b/leads-check.txt` | `proved: tool-run` |
| 7 | the 31 binaries and 18 art text files carry their recorded sha256 at the tip (ruling (o)) | `02` § Binaries, § Art bytes; `stage-c/runs/i-baseline/binaries.txt` | `proved: tree` |
| 8 | none of the 254 is modified in stages A-C; the removal check vs `86ebb6dffc` is empty | `stage-c/checkers.out` | `proved: tree` |
| 9 | each fix candidate's sentence predates, or was left untouched by, the change that made it untrue (`git log -S`) | `03` § 3.3 | `proved: history` |
| 10 | `t39-checks.sh` exits 0 on the baseline (`TOTAL: 13 of 13 steps`), 1 on each of the 14 step mutations, 1 on the tip with `allow-findings.txt` withheld (`TOTAL: 10 of 13 steps`), and 2 on all 7 refusals | `stage-c/checks-runs.out` | `proved: fixture` |
| 11 | `t39-tables.py` exits 0 on all 6 tables (`coverage`, `binaries`, `art`, `q4`, `q5`, `q6`) and exits 1 with `FAIL` on each constructed drift and missing-row mutation | `stage-c/tables/drift.out` | `proved: fixture` |
| 12 | `tools/lint-audit-artifacts docs/audits/2026_11_01-epic-m6-doctrine-reference --phase pre-issue` exits 0 (`PASS pre-issue artifacts (does not certify resolution)`) | `stage-c/lint-pre-issue.out` | `proved: tool-run` |

## The § 1 rulings ((a) to (q))

Each of the brief's § 1 rulings `(a)` to `(q)`, with its row and verification in this audit (§ 7 criterion 21):

| ruling | what it rules | where it is verified in this audit |
| --- | --- | --- |
| `ruling (a)` | the carve-out: 68 `edit-scope` + 1 `edit-under-naming` (`README.md`, `TRADEMARK.md`); ledgers, 90 upstream-carried, `LICENSE.md`, `docs/upstream/`, 31 binaries and 18 art text files untouched | `01` § Scope (`CARVE total 254`); `02` § Coverage, § The ledgers; `t39-checks.sh` `scope` and `untouched` |
| `ruling (b)` | `docs/es-menu-map.md` stale screen rows are the E700 interface lanes' (D-UI-039); T39 fixes only #570's `Pending` headings (L-08) and puts the journal's home as § 4 question 1 | `02` § The table (`L-08`, `L-32`); `04` § Maintainer questions (question 1) |
| `ruling (c)` | `README.md` has no build commands; `:7-10` (*"instructions attached to the [release]"*) is L-02 (`fix`) | `02` § The table (`L-02`); `stage-c/checkers/releases.out` |
| `ruling (d)` | `plans/` is one historical-plan ledger row (`ledger-plan`), never edited; names the superseding D-CLOUD-024/027/032/041 rows (L-24) | `02` § Coverage, § The table (`L-24`), § The ledgers |
| `ruling (e)` | `docs/pr-series/map.txt`'s two deleted paths (`post-update`, `cloud_migrate_layout`) are `inherited:coordinator` (L-27); never run `pr-stack-check` | `02` § The table (`L-27`), § The ledgers; `04` § Q6 |
| `ruling (f)` | session `m6-t1-os-launch` (freed from T36 #683), `cd`ing to `m6-doctrine-reference-686` | `00` header; `.github/sessions/saved-session-state-feature-m6-doctrine-reference-686.md` |
| `ruling (g)` | read tree is the dispatch tip (`86ebb6dffc`, stacked on P1 `2174265e9c` + coordinator `86ebb6dffc`), exported to `/workspace/tmp/m6-t39/export/` | `01` § Scope; `t39-checks.sh` `inventory` |
| `ruling (h)` | both line figures recorded side by side: 38,598 (inventory at `eb4763e3cc`) and 38,675 (`grep -c ''`) / 38,674 (`wc -l`) over the 223 text rows at `2174265e9c`, 31 binaries uncounted | `01` § Scope; `stage-a/01-block-membership.out` |
| `ruling (i)` | `#686`'s body rewritten at dispatch from § 7; `#807` `:15` carries the coordinator's `Erratum` for T39's 90 upstream-carried paths (L-37) | `00` § Stage A; `02` § The table (`L-37`) |
| `ruling (j)` | `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md` is tabled (`tabled-generic-x64`) with a Backlog candidate for the coordinator (L-31) | `02` § Coverage, § The table (`L-31`), § What the coordinator and the next slices inherit |
| `ruling (k)` | `LICENSE.md` is `read-only-528`: findings to #528 (L-43, L-45), never edited | `02` § Coverage, § The table (`L-42`, `L-43`, `L-45`) |
| `ruling (l)` | retired-name and identity hits fixed where a reader acts wrongly (`L-03`, `L-04`, `L-05` under `NAMING.md`, `L-22`); ledger/rule hits routed (`L-23`, `L-25`) | `02` § The table (`L-03`, `L-04`, `L-05`, `L-22`, `L-23`, `L-25`); `t39-checks.sh` `identity`, `retired`, `leads` |
| `ruling (m)` | `docs/futros/2026-10-24-m6-doctrine.md` carries the T39 kickoff addendum after T38's; predictions checked in `03` | `03-retrospective.md` § The doctrine futro's predictions checked |
| `ruling (n)` | `docs/upstream/**` (28 paths: 27 `read-only-585` text + 1 `ledger-binary` `.tar.gz`) is #585's, read-only, never sent (L-46) | `02` § Coverage, § The table (`L-11`, `L-46`), § What the coordinator and the next slices inherit |
| `ruling (o)` | 31 binaries (`ledger-binary`) and 18 art text files (`art-bytes`) tabled by name, size and sha256 and never edited; the 2 art READMEs are reference documents | `02` § Binaries (31), § Art bytes (18); `t39-checks.sh` `binaries` |
| `ruling (p)` | L-01 resolved at dispatch by stacking on P1 `2174265e9c`; verified by the 15-name loop printing no `MISSING` line and `of the 254 absent: 0` | `00` § Stage A; `01` § Scope; `stage-a/00-lint-and-l01.out` |
| `ruling (q)` | Local depth (`D-WORKFLOW-184`), no reviewer, no guest, no compile, no council/Facilitator/keyed call; lint Local PASS (`rc=0`) and FAIL-first (`rc=1`) proven first at stage A | `00` § Stage A; `second-opinions/review-plan.json`; `stage-c/lint-pre-issue.out` |

## The streams

Filled at stage E, under the coordinator's stream brief (`t39-streams.md`); one
row per fix with its check lines. Empty at stage C.

## What the coordinator and the next slices inherit

Named here at its `file:line`, read at stages A-C, never edited by the lane (§ 7 criterion 20 and § 8):

- **coordinator:**
  - `L-01` (`docs/reviews/README.md:10-12`, `docs/reviews/plan-for-the-plan.md:14`, `docs/reviews/briefs/p1-survey.md:19`, `docs/reviews/build-path-read.md:12` -- resolved at dispatch by the P1 stacking, ruling (p)).
  - `L-03` rule half (`.claude/rules/vm-first.md:21` -- names `D-QA-016` as open alongside `docs/device-testing-policy.md:5`).
  - `L-15` catalog regeneration (`docs/releases/catalog.md:1-60` via `tools/release-catalog --write`, and `#964`'s four release folders without a `RECORD.txt`).
  - `L-25` (`docs/releases/rc-accept.txt:13,15` -- *"the first Rasteratops release"* in the RC ledger).
  - `L-27` (`docs/pr-series/map.txt:112,174` -- deleted `projects/ROCKNIX/packages/network/rclone/sources/post-update` and `cloud_migrate_layout`, ruling (e)).
  - `L-28` (`docs/reviews/plan-for-the-plan.md:5,528` -- *"exists on `next` at `docs/reviews/...`"* and the plan's `:528` criterion; T4's boundary sentence and T38's hand-back plan leads).
  - `L-29` (`docs/reviews/order.md:792` -- preliminary slice number `T33` for `T38`).
  - `L-31` (`documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md:1-128` -- Backlog candidate: generate or drop the fork-own GENERIC_X64 emulator table, ruling (j)).
  - `L-33` (`#576 :7`, `#620 :16` -- cite `docs/graphics-memory-testing.md`, absent from the tree).
  - `L-34` (`docs/decision-register.md:239,250,368,486,490,497,502,514,797` and `.claude/rules/documentation-accuracy.md:48-52` -- upstream PR series ended by `D-WORKFLOW-084` still described as live).
  - `L-35` (`.claude/rules/handheld-evidence.md:3` -- `paths:` glob includes `docs/**`, loading the rule on every document under `docs/`).
  - `L-36` (`CLAUDE.md:34`, `AGENTS.md:31`, `.claude/rules/instruction-files.md:122` -- *"Two documents"* vs *"three"* that load by no rule).
  - `L-37` (`#807` body `:15` -- erratum present at dispatch, settled 06:43 UTC, ruling (i)).
  - `L-40` (`.claude/rules/worktrees.md:18,37`, `CLAUDE.md:166`, `AGENTS.md:148`, `docs/reviews/rules-sweep-2026-09-12.md:97,99` -- retired `rocknix.worktrees` / `/workspace/repos/rocknix` path words).
  - `L-42` (`#335 :19` and `LICENSE.md:1-25` -- stale checkbox citing a CC BY-NC-SA attribution in `LICENSE.md`).
  - **Backlog candidate (`tools/t39-checks.sh` -> `tools/docs-check`, § 8 item 3):** promote `docs/audits/2026_11_01-epic-m6-doctrine-reference/tools/t39-checks.sh` and its allowlists (`allow-legit.txt`, `allow-inherited.txt`, `allow-findings.txt`) to a repository tool `tools/docs-check`, updating `.githooks/pre-push`, `.claude/rules/fork-workflow.md` and `.claude/rules/instruction-files.md` in the same change.
  - **The R3 C24 lead (acceptance of 2026-11-02 00:12 UTC):** `cloud_migrate_layout` survives in 127 lines over six fork-only tools outside this slice -- `tools/cloud-pair-migration`, `tools/last-good-scripts-test`, `tools/pixelelated-vm-cloud-boundaries`, `tools/rasteratops-cloud-layout-test`, `tools/rasteratops-vm-cloud-epic` and `tools/vm-walks/cloud-epic/migration-protocol.sh` -- a lead for the tooling slices that own them (`cloud-harness`, `tooling-state-tests`, `tooling-last-good-test`, the VM tools slice); #508, which retired the automatic migration, is closed.
- **#528 (licences and notices):**
  - `L-43` (`TRADEMARK.md:5-6`, `LICENSE.md:3,13,18` -- GPL v2 vs *"non-commercial use only"* and *"Copyright 2024 ROCKNIX"*).
  - `L-44` (`licenses/AETHERSX2.pdf:1` -- PDF dropped upstream in `c4d353449e` for a licensing concern, still carried on the fork alongside 21 `aethersx2` package paths).
  - `L-45` (`LICENSE.md:1-25`, `TRADEMARK.md:1-20` vs `#359 :9,13,14` -- hashes match `#359`'s recorded bytes `1a277de2...` and `d46db25c...`).
- **#585 (the contribution queue, owed lines, never sent; D-WORKFLOW-164, -165):**
  - `L-46` (`docs/upstream/README.md:3,8,45`, `docs/upstream/raofflineproxy/pixelelated-identity/README.md:1-40`, `docs/upstream/raofflineproxy/image-completeness/fix.patch:64` -- `#585` queue drafts and `maxengel/rocknix` in `fix.patch:64`, read-only).
  - `L-11`'s share in `docs/upstream/README.md:12,14,19,22,25,28,31,34` (8 run-together word/number hits in `#585`'s read-only queue README).
- **the interface lanes (epic #700):**
  - `L-17` (`docs/conflict-wizard-ia.md:19,29` -- Rev 6 vs #23's rev 5 where a screen change owns the IA text; sentences contradicting decided rows D-CLOUD-024/027/032/041 are T39's `fix`).
  - `L-32` (`docs/es-menu-map.md:134,405,595` -- cited by `#682` at `:134`, `#1216` at `:405` where `#1216` quotes *"FINISH RESTORE PROCESS"* and `:405` reads `### FINISH RESTORE SETUP (the checklist after a settings restore)`, and `#667` at `:595`).
- **#509 (the reviewed rename batches):**
  - `L-30` (`docs/rasteratops/release-readiness.md:1`, `docs/rasteratops/support-matrix.md:1` -- current `pixelelated 0.0.1` release records living under `docs/rasteratops/`).
- **#511 (the website):**
  - `L-22` (`docs/pixelelated/site-plan.md:72,118` -- where the remote/checkout state is external to the doc's present-tense statement; the doc statement itself is a `fix` candidate).
- **#270 (the device-facts check):**
  - `L-15` tool half (`docs/releases/device-facts.md:7,17-19,31` and `.claude/rules/release-candidates.md:38-40` -- the tool `D-WORKFLOW-046` promises to check `device-facts.md` against `catalog.md`).
- **#947 (`register-check`'s `LIVE` list):**
  - `L-38` (`tools/register-check:15-22` -- the 53 reference documents outside `LIVE` that cite 442 distinct decision IDs, 0 unresolved today).
- **#1013 (versioning criterion):**
  - `L-39` (`docs/releases/versioning.md:1-95` -- `#1013`'s open criterion on `emulationstation` stamp/versioning).
- **the next upstream base merge:**
  - `L-41` (`documentation/PER_DEVICE_DOCUMENTATION/*/SUPPORTED_EMULATORS_AND_CORES.md`, 13 of 15 upstream-carried tables behind `upstream/next` `651150fc88`).


## Stage-D issue and question routing -- 2026-11-02

Audit: [#1406](https://github.com/pixelelated/distribution/issues/1406), real sub-issue of #686, M6. All 46 outcomes remain open; the six bugs remain reactive, milestone-less and without parents.

| Lead | Stage-D record |
| --- | --- |
| L-16 | Bug [#1405](https://github.com/pixelelated/distribution/issues/1405); accepted trace and criterion retained in stage-d/issues/bug-L-16.md |
| L-02 | Bug [#1400](https://github.com/pixelelated/distribution/issues/1400); accepted trace and criterion retained in stage-d/issues/bug-L-02.md |
| L-03 | Bug [#1401](https://github.com/pixelelated/distribution/issues/1401); accepted trace and criterion retained in stage-d/issues/bug-L-03.md |
| L-04 | Bug [#1402](https://github.com/pixelelated/distribution/issues/1402); accepted trace and criterion retained in stage-d/issues/bug-L-04.md |
| L-05 | Bug [#1403](https://github.com/pixelelated/distribution/issues/1403); accepted trace and criterion retained in stage-d/issues/bug-L-05.md |
| L-07 | Bug [#1404](https://github.com/pixelelated/distribution/issues/1404); accepted trace and criterion retained in stage-d/issues/bug-L-07.md |
| L-08 | Journal placement question [6582760931](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582760931); coordinator disposition awaited |
| L-12 | Low-inbound disposition question [6582762282](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582762282); accepted Q5: 33 files / 2,770 lines; coordinator disposition awaited |
| L-13 | Low-inbound disposition question [6582762282](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582762282); accepted Q5: 33 files / 2,770 lines; coordinator disposition awaited |
| L-18 | Low-inbound disposition question [6582762282](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582762282); accepted Q5: 33 files / 2,770 lines; coordinator disposition awaited |
| L-22 | #511 readback through comment 6129207059 describes private design planning, not current remotes; remains conditional for the stream brief / #511 owner |

Question IDs and exact posted bodies were read back through the GitHub comments API and retained in stage-d/question-readbacks.json. 06/07 and stage-d/ hold the filing/checkpoint records; they do not replace the 12 accepted A–C proofs or claim a fix. Stage D's checks validate the new records only.


## Owner dispositions and execution dispatch -- 2026-11-02T18:40:21Z

Both questions are settled: [6584515739](https://github.com/pixelelated/distribution/issues/686#issuecomment-6584515739). D-WORKFLOW-223/-224 at immutable coordinator b6332dbc13f5929f05ec5ba23c44285c5ee56b38 retain the journal in place with historical status/corrected headings and retain documents with dates/status. #1407 owns later indexed monthly storage and individual purpose/replacement review. Q5 remains 33 files / 2,770 lines: 32 editable, one ledger-plan table-only.

[Dispatch 6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759) authorizes S0-S6 and F/G/H under [stream brief v2](https://github.com/pixelelated/distribution/blob/7f25f9f78b3da3a6b2c893397b58a3ce5a04be75/docs/reviews/briefs/t39-streams.md). The original questions/readbacks above are preserved; these are answers and execution scope, not acceptance of corrections.

## Stage E/F — correction and resolution evidence

Observed 2026-11-02T19:02:55Z; checked source commit `de11515859d231a82a511c3867e12211190041a2`. Current executor: Codex / GPT-6-Astra / xhigh, session `01a19d12-0c07-7ba3-88b8-ab9d609f4d67`, T1 wN:p4. Historical identities, generated baseline tables and the 12 accepted proof pairs remain unchanged.

### The streams — S0 through S6

| Stream | Result / artifact | Commit |
| --- | --- | --- |
| S0 | Owner dispositions and complete route map; stage-e/00-opening.md and disposition-plan.json; original questions retained | 79866517db |
| S1 | Candidate and committed harness rc=0, 13/13; stage-e/S1/result.json and before/after artifacts | de40e931a469f6aa6889f08ec9d4d31266f4c6d4 |
| S2 | Candidate and committed harness rc=0, 13/13; stage-e/S2/result.json and before/after artifacts | 424eea28ecbfaa8fbbe49cdee6c99750becd13cf |
| S3 | Candidate and committed harness rc=0, 13/13; stage-e/S3/result.json and before/after artifacts | 895b90abcf44e62d3aa7339eba043cfe01e9b98e |
| S4 | Candidate and committed harness rc=0, 13/13; stage-e/S4/result.json and before/after artifacts | a2d4a33d4aa310d78c1b5c23b5bcdcd93f8ffe89 |
| S5 | Candidate and committed harness rc=0, 13/13; stage-e/S5/result.json and before/after artifacts | de11515859d231a82a511c3867e12211190041a2 |
| S6 | Final source normal + withheld-findings harness rc=0, 13/13; stage-f/outcomes.json; resolution/merge checks appended below when run | source de11515859d231a82a511c3867e12211190041a2; record commit named by final hand-back |

### Per-fix and recorded-route table

The precise source sentences/replacements are retained in each stream source-before-after.diff; these rows retain accepted lead locations, consumer impact and limits. Stage-F inherited issue excerpts confirm named owners remain open; they do not claim the downstream edits occurred.

| Item | Before | After / remaining action | Fix commit | Already written | Evidence / proof class |
| --- | --- | --- | --- | --- | --- |
| PL-01 | `docs/reviews/README.md:10-12`, `plan-for-the-plan.md`, at the dispatch tip `86ebb6dffc` — the renovation's README and plan name P1's files and tools | recorded design; accepted 15-name dispatch evidence  | record-only | nothing: resolved before any reader acted | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-02 | `README.md:9`, at the dispatch tip `86ebb6dffc` — the front page sends a player to instructions attached to a release that does not exist | README no longer promises attached instructions for an existing release; #344 remains the release-status authority.  | de40e931a469f6aa6889f08ec9d4d31266f4c6d4 | every session that opens the front page; #344 is open | stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-03 | `docs/device-testing-policy.md:5`, at the dispatch tip `86ebb6dffc` — the device-testing policy calls D-QA-016 open | D-QA-016 is described as decided on 2026-09-13. Existing per-action boundaries remain. Deferred rule counterpart: coordinator #346 must reconcile vm-first.md. | de40e931a469f6aa6889f08ec9d4d31266f4c6d4 | the five rule files that send testers to the policy | stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-04 | `docs/rasteratops/cloud-layout.md:16`, `docs/releases/pr/08-saves.md:5`, at the dispatch tip `86ebb6dffc` — the retired cloud-folder migration script described as current | Both old migration documents carry historical/retired notices, D-CLOUD-175 and current selected-folder policy; original record text preserved.  | 424eea28ecbfaa8fbbe49cdee6c99750becd13cf | the 08-saves PR description; the cloud-layout record | stage-e/S2/focused-checks.out; stage-e/S2/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-05 | `docs/device-flashing-runbook.md` (21 lines), at the dispatch tip `86ebb6dffc` — the flashing runbook names the OS ROCKNIX throughout | All 21 original ROCKNIX lines classified; current OS prose corrected and all fenced command bytes unchanged.  | de40e931a469f6aa6889f08ec9d4d31266f4c6d4 | `CLAUDE.md`, `AGENTS.md` and `device-builds.md:616` send every fresh-card flasher here | stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-06 | `docs/cloud-save-integrity.md:4`, at the dispatch tip `86ebb6dffc` — an M7 order of closed issues | The old order is dated 2026-10-08; the live M7 milestone supplies current order.  | 895b90abcf44e62d3aa7339eba043cfe01e9b98e | nothing traced | stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-07 | `docs/backup-contents.md:3-4`, at the dispatch tip `86ebb6dffc` — labels the pin does not ship, in banned words, in the public docs' stated source | Four labels mapped to exact ES source at 16dbac5211eea7e70db7394372033be2be7df829; backup semantics/stored archive names retained.  | 424eea28ecbfaa8fbbe49cdee6c99750becd13cf | the rocknix.org backup page drafts that copy it | stage-e/S2/focused-checks.out; stage-e/S2/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-08 | `docs/es-menu-map.md:758`, `:806`, `:817`, at the dispatch tip `86ebb6dffc` — the map's journal calls closed #570 work pending | Journal remains in place, three status headings corrected, historical anchor aliases retained; canonical menu prefix unchanged.  | 895b90abcf44e62d3aa7339eba043cfe01e9b98e | agents placing a row read it | stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-09 | `docs/releases/next-candidate-work.md:4`, at the dispatch tip `86ebb6dffc` — a superseded baseline build named as the baseline | The exact 20261011 build remains the baseline of the dated October reconciliation.  | 895b90abcf44e62d3aa7339eba043cfe01e9b98e | nothing traced | stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-10 | `docs/pixelelated/cloud-folders.md:32-35`, at the dispatch tip `86ebb6dffc` — the player's cloud-folder guide ends in internal release status | Guide ends with player guidance; removed internal publication note retained in S2 audit evidence.  | 424eea28ecbfaa8fbbe49cdee6c99750becd13cf | `README.md:22` sends players here | stage-e/S2/focused-checks.out; stage-e/S2/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-11 | ten files (`02` § The table), at the dispatch tip `86ebb6dffc` — words and numbers run together | 223 bounded hits classified, 189 ordinary prose hits corrected, identifiers retained; only whitespace plus old-heading aliases changed. Deferred upstream README prose: #585; rc-accept.txt remains a historical ledger. | a2d4a33d4aa310d78c1b5c23b5bcdcd93f8ffe89 | nothing traced | stage-e/S4/focused-checks.out; stage-e/S4/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-12 | `docs/council-mistral-counter.md:3`, at the dispatch tip `86ebb6dffc` — a counter note for a seat outside every run profile, no banner | Historical/retired-seat notice cites scaffold#915; original counter description and verified:false limits retained.  | 895b90abcf44e62d3aa7339eba043cfe01e9b98e | nothing traced | stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-13 | four files (`02` § The table), at the dispatch tip `86ebb6dffc` — rocknix.org drafts naming pages without their repository | External repository named in three paths; the fourth already names it and was unchanged in S4.  | a2d4a33d4aa310d78c1b5c23b5bcdcd93f8ffe89 | nothing traced | stage-e/S4/focused-checks.out; stage-e/S4/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-14 | `docs/pixelelated/art/README.md:20-21`, at the dispatch tip `86ebb6dffc` — the splash repository's wordmark tool, named with its repository | splash repository already named; accepted X02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-15 | `docs/releases/device-facts.md:7`, at the dispatch tip `86ebb6dffc` — the device facts point to a catalog with none of their cuts | Catalog generated scope stated; exact row Evidence links remain; S3 fact-table bytes unchanged, S4 spacing separately recorded. Deferred catalog/tool work: #964/#270; no catalog regeneration here. | 895b90abcf44e62d3aa7339eba043cfe01e9b98e | #1100, #1126 and #1094 cite its rows | stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out; tree |
| PL-16 | `docs/device-testing-policy.md:94`, at the dispatch tip `86ebb6dffc` — the read mask's long form lacks the flag form | Canonical literal mask hides 24 synthetic values; assignment-only control leaks eight space-separated flags; benign text preserved.  | de40e931a469f6aa6889f08ec9d4d31266f4c6d4 | readers who copy the policy's mask | stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out; stage-e/S1/mask-fixture.out; fixture |
| PL-17 | `docs/conflict-wizard-ia.md`, at the dispatch tip `86ebb6dffc` — the wizard's IA against its decided rows | #23 interface owners: unverified/conditional IA claim  | record-only | #23 still says rev 5 | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-18 | the Q5 table's LOW-INBOUND set, at the dispatch tip `86ebb6dffc` — low-inbound reference documents presenting themselves as current | Exactly 33/2770 accepted rows tabled: 29 additive notices, three S2 notices reused, one ledger-plan unchanged. #1407 owns later review. Later compact index, nested monthly storage and individual purpose/replacement review: #1407. | de11515859d231a82a511c3867e12211190041a2 | search results that look current | stage-e/S5/focused-checks.out; stage-e/S5/result.json; stage-f/withheld-findings/harness.out; stage-e/S5/dispositions.json; tree |
| PL-19 | `docs/rasteratops/art/README.md:8`, at the dispatch tip `86ebb6dffc` — the splash repository's tool in a historical artifact's README | recorded design: dated historical evidence; no current instructions claim  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-20 | `docs/rasteratops/p0-read.md:11`, `p0-sweep.md:39`, at the dispatch tip `86ebb6dffc` — `packages/rocknix` in dated P0 records | recorded design: dated historical evidence; no current instructions claim  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-21 | `docs/rasteratops/raofflineproxy-refresh.md:180,188`, `cloud-folder-state-table.md:38`, at the dispatch tip `86ebb6dffc` — Rasteratops as the OS's identity in dated records | recorded design: dated historical evidence; no current instructions claim  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-22 | `docs/pixelelated/site-plan.md:72`, at the dispatch tip `86ebb6dffc` — a current plan says the site remotes still name the retired owner | #511 current remote/checkout fact remains unestablished  | record-only | nothing traced | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-23 | `docs/cloud-sync-changelog.md:706-735`, at the dispatch tip `86ebb6dffc` — `maxengel/rocknix` links resolving only by redirect | recorded design: dated historical evidence; no current instructions claim  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-24 | `plans/conflict-resolution/vita-style-conflict-resolution.md:8-9`, at the dispatch tip `86ebb6dffc` — the one plan, superseded and unmarked | historical ledger-plan; table-only; later review #1407  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-25 | `docs/releases/rc-accept.txt:13`, at the dispatch tip `86ebb6dffc` — 0.0.1 called the first Rasteratops release in the RC ledger | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-26 | `docs/releases/rc-accept.txt`, at the dispatch tip `86ebb6dffc` — two stale acceptances kept as the record | recorded design: dated historical evidence; no current instructions claim  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-27 | `docs/pr-series/map.txt:112`, `:174`, at the dispatch tip `86ebb6dffc` — the upstream-series map names two deleted paths | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-28 | `docs/reviews/plan-for-the-plan.md`, at the dispatch tip `86ebb6dffc` — the plan says it exists on next; next has no docs/reviews/ | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-29 | `docs/reviews/order.md:792`, at the dispatch tip `86ebb6dffc` — a preliminary slice number in the order | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-30 | `docs/rasteratops/release-readiness.md`, `support-matrix.md`, at the dispatch tip `86ebb6dffc` — current release records under the retired name's folder | #509 reviewed rename batch  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-31 | `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`, at the dispatch tip `86ebb6dffc` — the fork's GENERIC_X64 emulator table has drifted and has no generator | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-32 | `docs/es-menu-map.md:134`, `:405`, `:595`, at the dispatch tip `86ebb6dffc` — the most-cited map, cited by line by open issues | #1216 interface owners; return line mapping  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-33 | #576 `:7`, #620 `:16`, at the dispatch tip `86ebb6dffc` — two open issues cite a document the tree lacks | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-34 | `docs/decision-register.md` rows; `documentation-accuracy.md:48-52`, at the dispatch tip `86ebb6dffc` — register rows describe a series D-WORKFLOW-084 ended | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-35 | `.claude/rules/handheld-evidence.md`, at the dispatch tip `86ebb6dffc` — a docs/** glob loads a device rule for any record | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-36 | `CLAUDE.md:34`, `AGENTS.md:31`, `instruction-files.md:122`, at the dispatch tip `86ebb6dffc` — two documents or three that load nowhere | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-37 | #807 `:15`, at the dispatch tip `86ebb6dffc` — an area sentence untrue of this slice | erratum already present at dispatch; accepted case-insensitive readback  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; design |
| PL-38 | the reference files outside `register-check`'s LIVE, at the dispatch tip `86ebb6dffc` — citations no tool checks | #947 citation-check coverage  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-39 | `docs/releases/versioning.md`, at the dispatch tip `86ebb6dffc` — an open criterion on the versioning document | #1013 versioning criterion  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-40 | `worktrees.md`, `CLAUDE.md`, at the dispatch tip `86ebb6dffc` — a path word the machine retired | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-41 | 13 of the 15 upstream-carried `documentation/` tables, at the dispatch tip `86ebb6dffc` — upstream's generated tables, behind upstream | #563/#559 next upstream base merge  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-42 | #335 `:19`, at the dispatch tip `86ebb6dffc` — an open checkbox against the licence file | #346 coordinator: preserve exact inherited action in 02  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-43 | `TRADEMARK.md:5-6`; `LICENSE.md:3,13,18`, at the dispatch tip `86ebb6dffc` — the licence statements disagree | #528 licensing/source publication; no legal interpretation or byte edit  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-44 | `licenses/AETHERSX2.pdf`, at the dispatch tip `86ebb6dffc` — a licence upstream dropped for a licensing concern | #528 licensing/source publication; no legal interpretation or byte edit  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-45 | #359 `:9`, `:13`, `:14`, at the dispatch tip `86ebb6dffc` — a qualified candidate's recorded licence bytes | #528 licensing/source publication; no legal interpretation or byte edit  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |
| PL-46 | `docs/upstream/**`, at the dispatch tip `86ebb6dffc` — the contribution queue's drafts, read-only | #585 contribution queue; drafts never sent  | record-only | -- | Accepted 02-forward-audit.md / 04-analysis.md; stage-e/inputs/t39-streams-v2.md; stage-f/inherited-issue-readback.json; tree |

### Current identity and retired-name counts beside the accepted baseline

Generated with LC_ALL=C /usr/bin/grep -E -c, identity -w and retired -i, over the same 223 text paths. These counts supplement the unchanged historical tables above. Current exact exceptions are stage-f/allowlist-locations.json.

| Class | Term | Current lines | Current files |
| --- | --- | ---: | ---: |
| identity | `Rasteratops` | 27 | 11 |
| identity | `rasteratops` | 31 | 20 |
| identity | `RASTERATOPS` | 4 | 4 |
| identity | `ROCKNIX` | 3264 | 57 |
| identity | `rocknix` | 947 | 43 |
| identity | `maxengel` | 28 | 6 |
| identity | `JELOS` | 7 | 7 |
| identity | `pixelelated` | 255 | 54 |
| identity | `Pixelelated` | 0 | 0 |
| identity | `PIXELELATED` | 0 | 0 |
| retired | `cloud_migrate_layout` | 21 | 7 |
| retired | `migrate.?layout` | 21 | 7 |
| retired | `rebase --onto` | 2 | 1 |
| retired | `rclonectl` | 0 | 0 |
| retired | `\.github/instructions` | 0 | 0 |
| retired | `copilot` | 0 | 0 |
| retired | `rubber[- ]duck` | 1 | 1 |
| retired | `\brclone config\b` | 2 | 1 |
| retired | `rocknix\.worktrees` | 4 | 3 |

### Current protected-byte comparison

The complete 31 binary and 18 art rows, each with size and original/current SHA256, are stage-f/binary-art-comparisons.json. All compare byte-identical to 86ebb6dffc. The final source-diff manifest is stage-f/source-diff-manifest.json.

### New proof pairs

| ID | Claim / command | Evidence | Proof |
| --- | --- | --- | --- |
| E01 | S1 candidate/commit harness; 21 runbook lines classified, fenced commands unchanged | `stage-e/S1/result.json; stage-e/S1/focused-checks.out` | `proved: tree` |
| E02 | Literal canonical mask synthetic control and corrected mask | `stage-e/S1/mask-fixture.out` | `proved: fixture` |
| E03 | S2 pinned labels and historical contract byte comparison | `stage-e/S2/result.json; stage-e/S2/pin-labels.json; stage-e/S2/focused-checks.out` | `proved: tree` |
| E04 | S3 dated headings, canonical prefix, historical aliases and seven cited targets | `stage-e/S3/result.json; stage-e/S3/citation-map.json; stage-e/S3/menu-map-check.out` | `proved: tree` |
| E05 | S4 bounded prose hit classification and external repository assertions | `stage-e/S4/prose-hit-table.json; stage-e/S4/result.json; stage-e/S4/citation-map.json` | `proved: tree` |
| E06 | S5 exact accepted 33/2770 membership and 29 body-preserving notices, three reused statuses, plan unchanged | `stage-e/S5/dispositions.json; stage-e/S5/result.json` | `proved: tree` |
| F01 | Final-source and --withhold findings harness both 13/13, rc=0 | `stage-f/final-source/harness.out; stage-f/withheld-findings/harness.out` | `proved: tool-run` |
| F02 | git show SHA256 comparison of original/current 31 binary and 18 art rows; source-diff manifest | `stage-f/binary-art-comparisons.json; stage-f/source-diff-manifest.json` | `proved: tree` |
| F03 | grep identity/retired counts and exact current allowlist locations; findings empty | `stage-f/term-counts.json; stage-f/allowlist-locations.json` | `proved: tool-run` |
| F04 | 46 dispositions under owner dispatch and open owner-issue readbacks; no downstream completion asserted | `stage-f/outcomes.json; stage-f/inherited-issue-readback.json; stage-e/inputs/t39-streams-v2.md` | `proved: design` |
| F05 | Resolution lint default/--issue 1406; rules/register/index/ceremony/forbidden/hooks/menu-map and eight issue checkbox checks all rc=0 | `stage-f/checks/; stage-f/audit-1406-body.md (exact live readback, open)` | `proved: tool-run` |
| F06 | New-record guard rejects five in-memory missing/drift controls before accepting the records | `stage-f/record-check.py; stage-f/checks/record-check.out` | `proved: fixture` |

| G01 | Stage-G four-answer retro, ten scoped checks and complete 46-item instruction coverage map | docs/retros/2026-11-02-m6-doctrine-reference.md; 04 Instruction File Recommendations | `proved: tree` |
| H01 | Exact authorized coordinator merge preserves complete log entries and all 48 corrected source hashes | `stage-h/merge-log-reconciliation.json; stage-h/source-after-merge.json` | `proved: tree` |
| H02 | New exact-tip provenance mode rejects wrong/unmerged tips and both post-merge and merge-resolution ownership violations; real merged withheld-findings run 13/13 | `stage-h/provenance-controls.json; stage-h/integrated-withheld-findings/harness.out` | `proved: fixture` |

### Counts after the authorized coordinator merge

The corrected-source counts above describe the pre-merge T39 source. The current 223-row counts below also include the authorized coordinator documentation changes; stage-h/source-after-merge.json confirms the 48 T39 source hashes did not change.

| Class | Term | Current lines | Current files |
| --- | --- | ---: | ---: |
| identity | `Rasteratops` | 27 | 11 |
| identity | `rasteratops` | 31 | 20 |
| identity | `RASTERATOPS` | 4 | 4 |
| identity | `ROCKNIX` | 3264 | 57 |
| identity | `rocknix` | 947 | 43 |
| identity | `maxengel` | 28 | 6 |
| identity | `JELOS` | 7 | 7 |
| identity | `pixelelated` | 255 | 54 |
| identity | `Pixelelated` | 0 | 0 |
| identity | `PIXELELATED` | 0 | 0 |
| retired | `cloud_migrate_layout` | 21 | 7 |
| retired | `migrate.?layout` | 21 | 7 |
| retired | `rebase --onto` | 2 | 1 |
| retired | `rclonectl` | 0 | 0 |
| retired | `\.github/instructions` | 0 | 0 |
| retired | `copilot` | 0 | 0 |
| retired | `rubber[- ]duck` | 1 | 1 |
| retired | `\brclone config\b` | 2 | 1 |
| retired | `rocknix\.worktrees` | 4 | 3 |

### Stage-H final record evidence

| ID | Claim / command | Evidence | Proof |
| --- | --- | --- | --- |
| H03 | Merged resolution/rules/register/index/ceremony/hooks/menu-map/new-record checks all rc=0; current counts generated; validated source exports retired | `stage-h/checks/results.json; stage-h/term-counts.json; stage-h/export-retirement.json` | `proved: tool-run` |

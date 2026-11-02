# T44 research — #691

Spec: docs/reviews/briefs/es-vendored-and-data.md v2 at817bb999f27a22c1ef33485b886663eb8b07a074; D-WORKFLOW-232. Primary ES 55158d2a64c69fe295fb4e67fd174424a71b1b4d. Distribution seed 48a335700d05a733703e1b58536877b91b921259. Local source provenance table, not installed verification.

## First source observations — 2026-11-02T22:49:49.413709+00:00

- ES root CMakeLists.txt:393–396 selects system pugixml when USE_SYSTEM_PUGIXML; external/CMakeLists.txt:5–7 excludes its gitlink then. Distribution recipe:24 sets that option. The mere gitlink is not an installed-source claim.
- Root CMakeLists.txt:610–612 adds es-app/tests/unit only with ES_BUILD_TESTS; the root tests directory is a distinct table/behavior-owner interface. No tests are executed.
- locale/CMakeLists.txt:9,14,25,31,33 creates/updates POT/PO/MO and installs compiled catalogues; root:614–616 gates the directory on gettext tools and Intl. These are source writers/conditions, not observed output. Never run this catalogue producer during the table audit.
- Distribution recipe:67–68 copies locale/lang, :81–85 copies resources then replaces DroidSansFallbackFull.ttf with the system Noto CJK symlink; source bytes and installed font identity are different questions. No image/render claim.
- Root:581–588 defines a Python resources checker POST_BUILD when Python exists and not MSVC. Read its source; do not execute it or treat membership as a successful build.

These observations are direct reads at the named objects. Later prior-evidence comparison will record agreement/limits separately; historical preparation knowledge is disclosed above.

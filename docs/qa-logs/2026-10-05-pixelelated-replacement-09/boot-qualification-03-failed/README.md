# Dependency guard failure before boot (#441)

Actual60221/allfourrc1; no guest started. Original valid seal pointed to failed
QA11 and its guard refused it. The agent launched despite the preceding failed
rebind preparation; this was an orchestration error, not a candidate boot
failure. Actual06:37:58 all owned processes absent, noQEMU. Replacementboot04
is a new sealed owner referring to successfulQA13's actual upgraded disk.

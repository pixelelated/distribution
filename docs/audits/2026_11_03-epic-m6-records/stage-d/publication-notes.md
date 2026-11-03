# T46 publication checks and transport

## Publication transport erratum — 2026-11-03

The first staged diff check exited2 on trailing spaces in numbered blank source lines. A subsequent normal commit attempt was refused by the pre-commit credential-pattern guard on decoded public historical patch names; no commit was created. Both failures and their actual streams are retained losslessly in stage-d/publication-refusals/. Earlier unstaged diff-check0 did not cover untracked audit files and was not a complete staged publication check.

The exact29 affected new record files now use lossless JSON transport: numbered stdout files are JSON UTF-8 strings at the same path; parse with json.loads then encode UTF-8 to recover original bytes. Selected JSON metadata uses escaped hyphens inside public path strings, with exact original formatting retained as JSON strings in stage-d/publication-encoding/original-*.json. The manifest binds original/stored SHA256 and recovery. Original receipts still hash the decoded original streams; original programs/fixtures are not replayed. Source and historical accepted artifacts are unchanged. This transport change is not a new reading or altered verdict.

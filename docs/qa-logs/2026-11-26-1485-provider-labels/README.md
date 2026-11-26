# #1485: the provider form's labels in French

OS coordinator, 2026-11-26.

- **`es-untranslated-before-french.txt`.** The labels marked `N_()` but with no French yet: 857 fork strings, 37 without French, all from `CloudText.cpp`, rc 1. Once the labels are marked, the check sees them and fails on a missing entry.
- **`es-untranslated-after.txt`.** With the French added (ES `9c75ebeb6`): 857 of 857.
- **Frames.** On build 15 (`90b95f7259`), `docs/qa-logs/2026-11-26-1111-1115-campaign/phase-d/build15-640x480/fr/s24/05-webdav-form.png` and `…/s30/05-s3-form.png`, `06-s3-form-lower.png`.
- **Also run:** `msgfmt --check` with the toolchain's msgfmt (clean), the ES unit tests (193 of 193), and es-syntax-check (PASS, 15 host tests).

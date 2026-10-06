Actual candidate15 VM proof coverage05 writes258048 of8391392bytes of a settings archive, records rclone PID5217/start8543/argv, then SIGKILLs that exact copy. The original four source files, all pointers and recovery record survive. The real UI offers TRY AGAIN but immediately fails with THE NEW FOLDER ALREADY HAS FILES IN IT. Primary reviewed the actual frames; allfourrc1/10seals and actual cleanup are retained23:00:41/45.

Source/history: resumable() at cloud_migrate_layout713-726 uses a reverse one-way full-file equality check. It admits a subset of completed files but cannot admit a truncated file. This guard dates to b9ea9f3fe8e (2026-09-04); D-CLOUD-026 still requires copy, content verification, then deletion. The valid recovery record must not become generic permission to merge somebody else's cloud.

Can this be done on the VM? Yes: same isolated local WebDAV fixture, actual installed script and UI. Existing tests inject errors before copies or after whole files; the new partial-byte case adds a missing boundary. No physical or personal cloud actions.

Acceptance criteria:
- [ ] Retain actual old-image SIGKILL/partial bytes, failed UI retry, original data/pointer preservation and lifecycle evidence as a failing control.
- [ ] Correct source regression covers partial files across all moved tiers, valid original binding, exact-prefix comparison and completed-file behavior. Missing/changed/extra/longer files, absent/wrong record binding and failed reads refuse without changing original cloud bytes or pointers. Old source fails the partial positives; new source passes and the full regression remains green.
- [ ] Rebuilt image repeats actual partial-copy interruption then UI TRY AGAIN, verifies all original bytes and new pointers, and proves the next backup's displaced save remains in the current shelf. Record clean/upgrade qualification, direct640/1280 frames and all result/seal/cleanup evidence before closure.

Tracked within open audit PL-003 (migration recovery), not an independent-review rerun or RC waiver. Refs #471, #478, #353; four original audit findings remain open. Fresh-root testing can proceed independently while this repair is prepared.

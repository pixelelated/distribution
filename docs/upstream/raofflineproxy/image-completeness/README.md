# Check downloaded image bytes before publication

Prepared for upstream under #168/#361; not submitted.
Base: `879b158995d412af434301ebdae581f66b8b6d57`.

Reject bodies shorter than a numeric Content-Length in both fetch paths. Before publishing a PNG, check its signature, chunk bounds and CRCs through IEND, and that IDAT inflates. A rejected download leaves no published image or temporary file and can be retried. Accept trailing bytes after a valid IEND and preserve existing cached files. This is not a full PNG decoder or a migration of previously cached corrupt files.

`fix.patch` contains the focused Linux change and regression tests.
6 targeted tests; 16 executions including the existing image-cache/shutdown suite. Before the fix, seven subcase assertions fail across the image-rejection and short-body tests. The distributed patch applies independently at fuzz0 to the
named pristine base. These are source tests; they do not replace installed
candidate or authenticated-account proofs.

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_image_completeness
```

[Before/after and distribution receipts](../../../qa-logs/2026-10-06-upstream-drafts/README.md).
The fixtures contain no real credentials and make no provider requests.
Keep the local product fix until upstream adoption and integration qualification.

The standalone context uses upstream's existing temporary-name/rename lines.
The concurrent-publication fix is a separate draft; this patch neither includes
nor supersedes it. Both would need a combined integration check if adopted together.

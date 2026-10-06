# Preserve upstream client-error responses

Prepared for upstream under #168/#361; not submitted.
Base: `879b158995d412af434301ebdae581f66b8b6d57`.

An understood request can return an upstream 400, 404 or 429 with a useful error body. The general online path replaces it with a misleading 503. Preserve status, reason, content type and body for non-authentication 4xx responses on dorequest.php; keep 401/403, server errors and non-API handling unchanged. Network failures still use the offline cache.

`fix.patch` contains the focused Linux change and regression tests.
3 targeted tests; 26 executions including the existing award-parity suite. The three client-status subcases fail before the fix. The distributed patch applies independently at fuzz0 to the
named pristine base. These are source tests; they do not replace installed
candidate or authenticated-account proofs.

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_client_errors
```

[Before/after and distribution receipts](../../../qa-logs/2026-10-06-upstream-drafts/README.md).
The fixtures contain no real credentials and make no provider requests.
Keep the local product fix until upstream adoption and integration qualification.

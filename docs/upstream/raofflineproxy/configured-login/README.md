# Select the configured account from cached sign-ins

Prepared for upstream under #168/#361; not submitted.
Base: `879b158995d412af434301ebdae581f66b8b6d57`.

When a password config selects a new account but has no token yet, the first cached login can belong to the previous account. Select the configured account's cache key, or attempt its login. A failed new login must not fall back to another account. Explicit token precedence and the unconfigured cached-login fallback are preserved. Uses real temporary SQLite rows and RetroArch config files; login transport is replaced with a local fixture.

`fix.patch` contains the focused Linux change and regression tests.
7 targeted tests pass. Five fail before the fix. The distributed patch applies independently at fuzz0 to the
named pristine base. These are source tests; they do not replace installed
candidate or authenticated-account proofs.

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_configured_login
```

[Before/after and distribution receipts](../../../qa-logs/2026-10-06-upstream-drafts/README.md).
The fixtures contain no real credentials and make no provider requests.
Keep the local product fix until upstream adoption and integration qualification.

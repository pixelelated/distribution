# Require explicit consent for automatic incident uploads

Prepared for upstream under #168/#361; not submitted.
Base: `879b158995d412af434301ebdae581f66b8b6d57`.

Automatic startup retry can upload an unreported storage-corruption incident without independent log-upload consent. Require the exact JSON boolean true in upload_logs. Default off; strings and numbers do not grant consent. Pass the loaded config to the startup retry. Existing reported/no-incident and upload success/failure behavior remain covered; manual menu upload and usage-statistics consent are separate, unchanged paths. The default choice should be described explicitly to upstream.

`fix.patch` contains the focused Linux change and regression tests.
6 tests pass, including invalid opt-in values as subcases. The no-argument default regression fails on pristine production code because the upload is attempted. Before testing the old implementation, select only this interface-compatible method; new config-argument tests would otherwise fail on the old signature. The distributed patch applies independently at fuzz0 to the
named pristine base. These are source tests; they do not replace installed
candidate or authenticated-account proofs.

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_storage_corruption_retry
```

[Before/after and distribution receipts](../../../qa-logs/2026-10-06-upstream-drafts/README.md).
The fixtures contain no real credentials and make no provider requests.
Keep the local product fix until upstream adoption and integration qualification.

# Filter the synthetic warning from achievement sets

Prepared for upstream under #168/#361; not submitted.
Base: `879b158995d412af434301ebdae581f66b8b6d57`.

The achievementsets filter retains the synthetic warning because its Flags value is core. Filter its ID as the other achievement APIs already do. Existing cache rows are filtered when served, without rewriting their stored history; newly fetched responses and cache entries omit the warning. Real core definitions, subset IDs and existing flag filtering are preserved.

`fix.patch` contains the focused Linux change and regression tests.
4 targeted tests; 27 executions including the existing award-parity suite. Three tests fail before the fix. The distributed patch applies independently at fuzz0 to the
named pristine base. These are source tests; they do not replace installed
candidate or authenticated-account proofs.

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_warning_sets
```

[Before/after and distribution receipts](../../../qa-logs/2026-10-06-upstream-drafts/README.md).
The fixtures contain no real credentials and make no provider requests.
Keep the local product fix until upstream adoption and integration qualification.

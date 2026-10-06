# Keep periodic refresh alive after a failed pass

Prepared for upstream under #168/#361; not submitted.
Base: `879b158995d412af434301ebdae581f66b8b6d57`.

An exception while resolving credentials or reading refresh inputs can end the refresh thread. Catch pass-level failures so the next interval still runs. End a game pass on authentication rejection or three consecutive fetch failures, resetting the streak on success. Preserve recent-played selection, activity deferral and rate-limit stopping. Current upstream already catches individual game failures; this draft does not claim that boundary is absent.

`fix.patch` contains the focused Linux change and regression tests.
6 targeted tests; 57 executions including the existing refresh-scope suite. Before the fix, two assertions fail and the injected pass-level exception escapes. The distributed patch applies independently at fuzz0 to the
named pristine base. These are source tests; they do not replace installed
candidate or authenticated-account proofs.

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_refresh_resilience
```

[Before/after and distribution receipts](../../../qa-logs/2026-10-06-upstream-drafts/README.md).
The fixtures contain no real credentials and make no provider requests.
Keep the local product fix until upstream adoption and integration qualification.

The packaged patch context mentioned patch001; this draft replaces that context
with the actual pristine blank line. Production changes are otherwise identical.

# Standalone proxy contribution qualification

Owners #168/#361. Seven new drafts are prepared, not submitted. The candidate
source and image are unchanged; no installed-image or account proof is inferred.

Exact upstream base: `879b158995d412af434301ebdae581f66b8b6d57`.
Archive SHA256: `984957322337d1325f1b0fc11502336a80241ec511fd041c969bb0103c231664`.
`verify-drafts.py` rejects any other archive and an existing output directory.
It applies test-only diffs first and hashes production files to confirm they
remain pristine, then applies each full draft independently at fuzz0 in a
fresh copy. Test processes exit before the next draft begins.

| Draft | Targeted tests passing | Fixed executions with related suites | Pristine result |
| --- | ---: | ---: | --- |
| HTTP client errors | 3 | 26 | 3 client-status subcase failures |
| Warning achievement sets | 4 | 27 | 3 failed tests |
| Configured cached sign-in | 7 | 7 | 5 failed tests |
| Refresh resilience | 6 | 57 | 2 assertions fail; injected pass exception escapes |
| Log-upload consent | 6 | 6 | default-no-consent upload is attempted |
| Image completeness | 6 | 16 | 7 negative subcase failures |
| Bounded DNS | 8 | 30 | connection is attempted after failed DNS |

Total:40 targeted tests,169 fixed executions including repeated award-parity
coverage, zero skips. The log-consent pristine control selects the existing
no-argument interface: calling its new config signature on old code would
only demonstrate a signature mismatch. All fixtures are local and synthetic;
no provider account is contacted. Upstream's award tests open local sockets.

`result.json` (six drafts) and `bounded-dns/result.json` bind the distributed patch hashes and outcomes. All before,
after and apply logs are retained alongside it. `targeted-result.json` records
the earlier isolated source tests and original packaged patch hashes.

Reproduce from the repository root with a new output directory:

```sh
python3 docs/qa-logs/2026-10-06-upstream-drafts/verify-drafts.py \
  --archive /path/to/raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57.tar.gz \
  --output /path/to/new-output-directory
```

Preparation failures remain in `preparation-failures/`: the first005 context
rewrite was rejected by GNU patch; the corrected draft uses pristine blank
context and applies at fuzz0. The first broader award-suite run hit three
sandbox socket PermissionErrors. The later unchanged tests run with local
socket access pass; this is an environment correction, not a product fix or
ignored failed assertion. No failed receipt was overwritten.

These source regressions are portable to a VM. The host ran them here; frozen
replacement14's full VM qualification is separately recorded. Ten upstream
drafts now exist in total. Interface/policy proposals in the contribution map
remain subject to upstream agreement; no submission has been made.


DNS preparation initially referenced urllib as a proxy_service module attribute;
the actual forwarder imports it locally. That fixture-only AttributeError is
retained in `preparation-failures/`; the corrected fixture patches urllib's
shared request module and the fresh02 run passes all30 tests. The bounded
worker test releases its stalled resolver and joins the captured thread;
answer reuse, expiration, other hosts, IPv4/IPv6 and fresh probes are covered.
No unbounded DNS or provider endpoint is contacted.

Live upstream at preparation completion still names879b158. Its two open PRs,
206 (SteamOS/EmuDeck) and84 (RetroDECK), concern platform packaging/discovery,
not these behavioral fixes. Their bodies and file lists are retained. They
share config.py with the existing identity/consent proposals, so recheck that
context before submission or rebasing. This check does not claim a merge is
conflict-free.

The fresh-context resume proof in `resume-proof.json` found no blocking mismatch.
It verified heads, frozen manifest identity, completed process absence, cleanup
state and draft result/hash records. One historical cleanup sentence was clarified
and independently reread. `publication.json` and `local-final-verification.json`
retain the original published-head/tracker and host checks; later handoff commits
do not change the candidate or these test results.

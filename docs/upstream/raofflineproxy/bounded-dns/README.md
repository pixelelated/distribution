# Bound DNS before probes and upstream forwarding

Prepared under #168/#361; not submitted. Base879b158995d412af434301ebdae581f66b8b6d57.

Connection timeouts do not bound the platform resolver. Give the lookup a
three-second deadline and use its remembered answer for the following
connection, so that connection does not incur a second unbounded lookup.
The request log reads the known reachability state instead of probing merely
to print a line. Failed DNS returns the existing network-error/offline path.

The draft retains the fork's process-wide socket.getaddrinfo wrapper and
30-second answer lifetime. This side effect should be explicit in upstream
review: other hosts/families fall back to the resolver, each bounded probe
still asks the platform anew, and a timed-out daemon worker may finish later.
It is not cancellation of the platform lookup or a bound on all process DNS.

Eight targeted tests plus22 existing network tests pass. The pristine
interface-compatible negative control attempts a connection after DNS failure;
the fixed probe refuses before urlopen. Additional controls cover deadline
return while the worker is still blocked, explicit worker release/join,
connection answer reuse, fresh probes, expiry, unrelated host/family fallback,
IPv6 flow/scope preservation and forwarder refusal. No real DNS/provider is used.

The standalone patch rebases request-log context from upstream's direct probe;
it does not depend on the fork's earlier image-only logging change. Production
network/forwarding behavior otherwise follows packaged015.

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_bounded_dns linux.tests.test_linux_network
```

[Reproducer, hashes, original fixture failure and passing receipts](../../../qa-logs/2026-10-06-upstream-drafts/README.md).
These source controls do not replace frozen candidate/account qualification.

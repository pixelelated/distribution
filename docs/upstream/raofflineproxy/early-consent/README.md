# Read consent on the first observation

Prepared for upstream; not submitted. Fork issues #457 and #168.
Base: `b09d604ecaba7c973028a659b69106b72d3c9514`.

`_Recorder` initializes `_consent_checked_at` to0.0, then reads consent only
when monotonic time exceeds that value by30 seconds. At early system uptime,
already-granted consent is therefore ignored and opted-in counters are missed.
The same sentinel fails to invalidate an observation immediately. This is not
an unsolicited upload. Persisted counters, consent and report timestamps keep
their existing formats; missed counters cannot be recovered.

`fix.patch` changes the sentinel to None and includes three regression methods:
zero/five-second granted consent, immediate grant/decline/regrant, and unanswered
consent. With tests alone, eight consent tests have three failing assertions;
with the fix, all eight pass. Source controls are retained under
[retained source controls](../../../qa-logs/2026-10-06-proxy-consent/README.md).

From a pristine upstream checkout at the named base:

```sh
patch --batch --fuzz=0 -p1 < /path/to/fix.patch
python3 -m unittest -v linux.tests.test_linux_usage_stats.ConsentTests
```

The regression uses simulated monotonic uptime and isolated configuration;
it makes no external request. Fork full-series qualification and installed
VM reporting proof are separate gates. The installed positive control first
found this on candidate12; that run remains failed. Replacement14 now passes
all30installed reporting/restart cases, with the first granted counter at
16.705487703seconds uptime. The draft is byte-identical to packaged patch019.
[Installed receipts](../../../qa-logs/2026-10-06-pixelelated-replacement-14/README.md)
are separate from this standalone upstream regression.

# #577: preserve Wi-Fi scan failures

Evidence level: **static source inspection only**. No compiler, fixture, test
suite, service, browser, VM, or radio operation was run for this extension.
The runtime controls below are **UNRUN**. This packet does not close #577 or
claim that the composed ES source builds or behaves correctly.

The preceding picker packet is immutable at distribution commit
`6cf8405bcc398af71ba081b6eb377da41b44ef0d`. Its ES source remains
`2e84879d488e22a312b5a3e179836f927c448738`, which the coordinator reports composed
at `a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20`. No ES file changed during this
backend extension. The old worker/process fixture remains UNRUN.

## Source and intent

Before editing, local `wifictl`, local `next` at
`0ea6eaf74ad47503c05955d1c0bd4bd00bdfb816`, and the coordinator's working file
were identical: SHA-256
`32d43774637fed12b6ed083ce3f9c0dcc63d97850f0d515fc670b620a36fe2d4`.
No refresh was needed. A final static comparison still found the original
bytes on `next` and in the coordinator checkout; the latter's HEAD was
`7c13b9c08bd419ce9e62e4af8f4e306d9bad0853`. Exact original/current hashes and
the 17 unchanged function hashes are in [source-review.json](source-review.json).

Local primary-source history explains the retained behavior:

- `f48cc1b0304a843ed4e04c7627a2fe08f733d4f9` introduced the iwd readiness
  loop and a `scanlist` pre-scan in the 2025-08-07 iwd conversion.
- `beb5d8a239` introduced NetworkManager scanning: wait for iwd, rescan,
  delay, then enumerate. `e88678fc0e7262136875c78f090f8c4df32d7131` later
  added connection readiness checks; it did not give scanning typed errors.
- Cached upstream `upstream/next` is
  `d59bdaa28908f7266e40172e088ec40813fd3f46`, dated 2026-10-12. Its script
  contains `b1f84642413f7723241a48d63cfdd601083f1103`'s larger saved-network
  refactor. Its `list_wifi` explicitly ignores rescan errors and still pipes
  enumeration through text filters. That source does not supply this fix.
  This is a local ref comparison, not a claim about the latest online head.
- Fork `ea5872b6a9ab73e1ec85c9d79edc767adee7ce83` restored scan SSID
  unescaping so exact names agree with current/saved names. Its `nm_unescape`
  and the order unescape → remove blank lines → deduplicate remain intact.
- `fbb999bf51da45827a457d57da932627965b6489` records D-UI-118's merged
  design: preserve fork saved-profile semantics and upstream's keyless
  saved-profile-first connection. `bc2dceb406969a401d987de168acfb3ae60b7e01`
  added the open/unknown-security boundary. Those function bodies are unchanged.
  D-UI-127 and #577 require failed scans to differ from successful empty ones.

The [official nmcli manual](https://networkmanager.dev/docs/api/latest/nmcli.html),
read 2026-10-13, documents success as rc 0, timeout as rc 3, unavailable
NetworkManager as rc 8, and missing connection/device/access point as rc 10.
It also documents terse escaping of colons and backslashes. Rescan requests
scanning; enumeration returns access points. The prepared cases use those
statuses without inventing a new product error taxonomy. Synthetic rc 124 is
an arbitrary wrapper-status propagation control, not nmcli's timeout code.

## Narrow correction

Only `projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl` changes:

- `list` and `scanlist` join the existing typed entry guard: unavailable
  adapter or nmcli is rc 2. Other entrypoints retain their existing guards.
- `wait_for_wifi` explicitly reports success when the adapter was seen,
  including with no country configured. Five completed unsuccessful checks
  return 1 when the final query succeeded but found no adapter, or the final
  failed iwctl query's status. A country-setting failure is also nonzero.
  Readiness still permits later successful checks to recover from earlier
  failures. Existing connection/AP callers ignore the helper's status and
  continue to judge their own operation, as before; only listing checks it.
- Listing checks readiness and rescan status, buffers enumeration before
  filtering, and returns its actual nonzero status without partial stdout.
  Successful zero networks still produce no stdout and rc 0. Rescan/readiness
  stdout cannot become a network row. Existing SSID spaces, tabs, colons,
  backslashes, deduplication, and sorting are preserved.
- `scanlist` retains its existing initial rescan, two-second delay, and
  `list_wifi` rescan. Its first rescan now checks status and uses explicit
  `-w 15`, matching the second. A failed first rescan exits immediately;
  a failed second rescan prevents enumeration. Removing the historical
  extra rescan is outside this prerequisite.
- `pipefail` is enabled only in the final formatting subshell. No global
  shell option changes. The other pipelines include intentional grep probes,
  `head -n 1`, and saved/profile readers; changing their status semantics
  globally would exceed this fix. The new enumeration capture checks nmcli
  directly, before any pipe can hide it.

The other 17 function bodies compare byte-for-byte with the baseline, including
`wifi_security`, `connect_open_wifi`, `connect_wifi`, `current_wifi`,
`saved_wifi`, `saved_with_ssids`, `forget_wifi`, `join_wifi`, and the escaping
helpers. Existing manual/protected/saved connection dispatch is unchanged.
No dependency or recipe change, new user-facing string, translation, pin,
shared record, or GitHub mutation accompanies this packet.

## Prepared controls and original expectations — UNRUN

[fixture.py](fixture.py) is the single executable fixture. It requires the
adjacent source binding and an explicitly supplied script. It refuses other
hashes, replaces exactly `. /etc/profile` with a synthetic shim, and executes
the remaining complete script bytes, including discovery, guards, functions,
and dispatch. It does not copy the implementation into the fixture.

The shim replaces settings, adapter discovery/directory checks, iwctl, iw,
nmcli, and sleeps. A private PATH exposes only grep, sed, sort, seq, and tr;
no networking executable is exposed. Each case gets private counters and
call logs. The runner imposes a five-second per-case deadline and kills the
shell process group even on failure, then reaps the direct shell. The
coordinator's outer runner owns escaped processes and overall resource limits.

There are 18 controls each for `list` and `scanlist`, plus a `scanlist`
second-rescan failure: **37 per source version, all UNRUN**. Expectations are
source-derived assertions, not observed results:

| Synthetic condition | Original expected rc/stdout | New expected rc/stdout |
| --- | --- | --- |
| Successful empty list | 0 / empty | 0 / empty |
| Escaped names, duplicates, whitespace | 0 / decoded, sorted exact names | Same |
| Missing adapter, disappeared adapter, missing nmcli | 0 / empty | 2 / empty |
| Five successful queries without the adapter | 0 / empty | 1 / empty |
| Five failed iwctl queries, including misleading partial output | 0 / empty | 9 / empty |
| Adapter appears on third query | 0 / empty | 0 / empty |
| Country succeeds / country command fails rc 6 | 0 / empty in both | 0 / empty; 6 / empty |
| First rescan fails / times out | 0 / empty | 8 / empty; 3 / empty |
| Second `scanlist` rescan fails | 0 / empty | 10 / empty |
| Enumeration fails / times out / returns synthetic wrapper status | 0 / empty | 8 / empty; 3 / empty; 124 / empty |
| Enumeration prints partial SSID then fails rc 8 | 0 / partial SSID | 8 / empty |
| Rescan prints a diagnostic to stdout | 0 / diagnostic(s) | 0 / empty |

New-source assertions also check readiness/rescan/enumeration call counts,
absence of enumeration after an earlier failure, enumeration as the final
external operation, and `-w 15` on every rescan. Original-source runs assert
the historical return/output contract, including the false-success behavior.
Neither version's expected output is an execution receipt.

The controls simulate timeout exit statuses immediately. They do not measure
wall-clock deadlines, real NetworkManager/iwd behavior, radio discovery, or
ES subprocess cleanup. The five readiness attempts do not bound a hung iwctl
call. `scanlist` still performs its first rescan before the readiness loop;
that operation can fail early. ES's 30/45-second worker deadlines and process
cleanup remain the outer bound to qualify in the coordinator's existing
UNRUN helper controls. Enumeration is buffered in shell memory before the ES
output cap sees it; this is not a backend memory-limit claim.

## Coordinator's next executable experiment

Can this be done on the VM? **Yes**: these synthetic control/status checks do
not need a radio. The coordinator must record the VM-first plan and allocate
the disposable environment before running anything below. No allocation or
fixture execution happened in this packet. Use a fresh private temporary
directory; do not replace guest or host `/usr/bin/wifictl`.

On the distribution checkout, the smallest new-source command is:

```sh
TMPDIR=/workspace/tmp/pix570-parallel-20261013/tmp python3 \
  docs/qa-logs/2026-10-13-wifi-backend-source/fixture.py \
  --version current \
  --source projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl \
  --tmp-root /workspace/tmp/pix570-parallel-20261013/tmp
```

This is a prepared command, **not authorization to run on the shared host**.
For the disposable VM, stage this fixture, adjacent `source-review.json`, and
the exact source under the allocated private directory; substitute those
paths and the VM's private temporary root. Capture stdout as a new JSONL
receipt plus stderr and outer-runner status. Every result binds both original
script bytes and adapted script bytes by SHA-256.

To prepare the historical control, export (read-only) the baseline with
`git show 6cf8405bcc398af71ba081b6eb377da41b44ef0d:projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl`
to the coordinator's private staging path, then use `--version original` and
that file. Keep old-source receipts separate. The expected rc 0 failures
are historical regression controls, not permission to ship that behavior.

Acceptance mapping for #577:

| Criterion | This packet's evidence | Remaining coordinator proof |
| --- | --- | --- |
| Empty differs from failure; retry keeps results | Checked source branches and 37 prepared controls | Execute both source versions; exercise ES initial-empty, initial-error, retained-results/error/retry with corrected backend |
| No duplicate UI jobs; back and late completion safe | No ES changes; scanlist's existing two nmcli rescans explicitly retained | Existing worker helper fixture and VM navigation/deadline controls, still UNRUN here |
| Saved/current/open/protected/unknown/manual/forget preserved | 17 function-byte equalities; guarded status extension only for list/scanlist | Existing routing/security controls against the composed binary and this exact script |
| Stable viewport, scrolling, focus, EN/FR copy | Prior immutable picker source packet | Exact-source frames at 640x480 and 1280x800, including retry, long list, and failure |
| Shared flow/docs and integration | Proposed text below only | Coordinator owns canonical flow/menu map, work log, issue status, changelog/public docs, build/VM admission, and pin/integration |

Suggested canonical backend contract addition: “Wi-Fi search reports an error
when adapter readiness, rescan, or network enumeration fails. Successful zero
networks is empty; a failed refresh keeps prior results. Saved and manual
connection behavior is unchanged.” Publish behavior claims only after the
coordinator's exact-source runtime evidence. No extra EN/FR strings are needed
beyond the preceding picker packet.

## Actual checks

`bash -n` passed on the modified source and the fixture's extracted shim;
Python AST parsing passed on the fixture. Static function comparison found
only `wait_for_wifi` and `list_wifi` changed, with the entry guard and scanlist
dispatch edits reviewed separately. `git diff --check` and manifest validation
passed before the local commit. These checks do not execute the fixture or
establish behavior. Source and packet hashes are in [SHA256SUMS](SHA256SUMS),
relative to the distribution checkout root. Prior packets and historical
receipts were not edited or rehashed.

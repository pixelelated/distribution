# #582 CRC retry event capture — fixture-only, UNRUN

This additive packet prepares only `crc-failure-retry` against unchanged installer
03e130e4b3c244337f2e6d782b392a2c444c28e7, SHA256
`fab7cdb4ad8adbcea147be54092bb7ce2005010447be4ab8192c94d8bbe9229d`.
No product, original packet, accepted case or original FAIL was changed. New
runtime is UNRUN; synthetic structure checks cannot establish native Steam success.

## Original failure and source intent

The coordinator's lossless attempt 10 archive is 44380 bytes, SHA256
`317d21f4c3a50ff24784340bf65a0c7b70fa8d188d49d87e0083eeb818044a60`.
`intake.json` binds every regular evidence member and selected byte-exact copies
under `evidence/`. Original caller/trace exits were **1,1**, with no remaining
tracees or outer descendants and successful outer quiescence. Attempt 1 explicitly
reports actual CRC validation refusal; both saved storage manifests have no owned
client stage left (the independent persistent lock remains). The first failure
is expected. Attempt 2 manifest child 67 returns 0, archive child 68 returns 1,
and the helper reports transfer failure. There is no second archive event.

The unchanged product `transfer` sets each curl child's RLIMIT_FSIZE to its
output bound: manifest 2,097,152 B, synthetic archive 10,676 B. The actual boundary
copies the exact archive to stdout and then appends an archive event and an exit
event. Before archive child 68, shared `/qa/events.ndjson` already has 10,806 B;
the complete old log is 11,027 B. A regular-file append above 10,676 B is incompatible
with that child's limit. `boundary.py` catches the first event failure, then its
finally-block attempts another append and can exit 1; the product drains child
stderr into a bounded internal buffer without emitting it. The originals do
**not** retain an EFBIG errno/traceback. This is a concrete source/evidence binding,
not a claim that the exact exception was directly captured.

The shared event writer originated in transaction packet
a057a2a7e94c372642fd66ff9795125487f1fa75 and was copied unchanged into 03e130.
Its purpose was complete synthetic-boundary observability, not transport output;
real curl does not append this fixture-wide file. The product's per-transfer file
bound remains appropriate and unchanged. The existing CRC corruption remains the
same local/central CRC change for `steamrtarm64/chromehtml.so`, offsets 231/6731,
3787868624→3787868625, with complete manifest/ZIP transport integrity maintained.

## Narrow correction and retained assertions

`boundary.py` imports a new event writer from `event_records.py`. Each boundary
process creates one exclusive private regular event file under
`qa/boundary-events/`, with PID and monotonic identity in its name, a 4 KiB hard
writer cap and a 512-file bound. Every write checks regular-file identity, link
count and length; failures remain fatal. No exception is ignored, no signal
handling changes and no resource limit is adjusted. The largest original event
stream for a single PID was 633 B, below 4 KiB and the 10,676 B synthetic archive limit.

The exact `python-boundary.py` helper writer still uses `qa/events.ndjson` outside
the transfer child's FSIZE restriction. Its live reader in `transfer-child.py`
is also byte-identical. Only transport/engine boundary writers move; this avoids
changing accepted detached-child/visibility semantics. The old shared filename
is now the helper stream, **not the complete event list**.

The fixture collects both original streams after the blocked trace control,
after attempt 1's original result/empty trace census, and during final assessment
after unchanged outer quiescence. It creates separate `events-controls.ndjson`,
`events-attempt-1.ndjson` and `events-collected.ndjson`, each with a JSON input-hash,
byte-count and ordering receipt. It never truncates or rewrites originals. Each
record's exact original bytes/PID/timestamp survive; merged order uses original
monotonic time, PID, path and source-line number for deterministic ties. This is
recorded event order, not a new guarantee of simultaneous processes' syscall order.
Missing/aliased/changed/partial/oversized files fail collection; combined events
remain capped at 2 MiB. A stopped fixture may lack a final collection, but original
per-process files, earlier snapshots and original result receipts remain available.

Only three event-read sites change in the complete caller. All remaining caller
AST, transport/TLS argv, exec-denial checks, route/namespace supervision, original
result assertions, CRC generation and preservation checks are unchanged. Expected
caller exits remain **1,0**, both trace receipts RETURNED, actual first CRC refusal,
retired failed stage, protected state unchanged, and final synthetic client exec
denied at its syscall. No cleanup/timeout rescue may become success.

`static-check.py` parses source, compares complete normalized caller AST and exact
source deltas, verifies old packet hashes and original evidence. It imports no
fixture and generates no payload. `static-result.json` records those actual checks.
Existing limits remain 90 s fixture / 80 s trace / 10 s cleanup, 64 MiB retained output,
2 MiB per log, and the separately admitted 3 GiB executable scratch filesystem with
2368 MiB minimum free. No timer/resource increase is proposed.

## Next failed-case command — coordinator allocation required

In a fresh admitted no-NIC GENERIC_X64 guest, with byte-exact source under
`/opt/pix582-source` and new private scratch output:

```sh
TMPDIR=/run/pix582-scratch python3 -I -S -B \
  /opt/pix582-source/docs/qa-logs/2026-10-14-steam-crc-event-source/fixture.py \
  --disposable-vm --case crc-failure-retry \
  --installer '/opt/pix582-source/projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh' \
  --output /run/pix582-scratch/crc-failure-retry-events-11
```

Consume the unchanged original caller sequence 1,0 and all existing guards plus
`events-collected.json`/`.ndjson` and their original inputs. The entrypoint accepts
only this case. Other accepted cases stay accepted on 03e130; no broad rerun plan.

If direct errno corroboration is desired, the smallest extra VM-only control is
a separately owned ≤5 s child setting FSIZE 10676, appending one byte to a private
pre-created 10806 B regular file (expect EFBIG 27), then writing a 633 B fresh private
file under the same limit (expect success). It must preserve both original
results and leave signal dispositions/limits on the installer untouched. This
optional control is proposed, UNRUN and not a prerequisite added to acceptance.

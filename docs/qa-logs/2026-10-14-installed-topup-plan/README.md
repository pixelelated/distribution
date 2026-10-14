# #567 installed top-up continuation

Source-only preparation, 2026-10-14. No VM, service, executable fixture,
provider, compiler or container was run. The engineering image can compile
independently. This packet is a bounded source plan, **not an installed top-up
adapter or preparation PASS**.

The remaining check is one successful native ES indexing request followed by
the **installed** `/usr/bin/raofflineproxy-ctl topup --after-index` and installed
Python preparation helpers. Reuse the accepted success fixture's API trigger.
Do not repeat its four indexing branches or the separately accepted confirmation
UI branches. This adds the backend boundary the previous proof explicitly
substituted; it does not add a new #567 release criterion.

## Accepted inputs and exact original result

`source.json` binds every input and relevant source read. The accepted native
success is the coordinator's:

```
docs/qa-logs/2026-10-14-offline-components/guest-archives/
  index-log-success01/pix567-log-success01/
```

Its `worker-result.json` says one hash-library request, one official-games
request, one simulated preparation, ES exit 0, listener exit 0 and output guard
PASS. Its outer `result.json` has original worker exit 0, no timeout, no killed
stragglers, no remaining namespace processes and unchanged parent census.
`index-success-api` is the original SIGXFSZ failure, not this successful result.
The accepted binary was ES `bb9e2785f88c2b9de979022a2a9ded2cbce2f954`, SHA256
`8752b5391ea8728c1a088d0a80e3776469692dda665e8f07f062fed3206263d2`.

The exact reusable runner is commit
`84faea63d9f83392ff9b6ec30bd98c3585024c9d`, SHA256
`10d3b0276ae780fac4f39f7af1b2791c9872bcb8e3e70acb6d139c1c919200a1`.
Keep its accepted `81d618` output guard byte-for-byte: 64 MiB ES file-size
ceiling for PulseAudio memfd, separate 8 MiB/64-inode ES log tmpfs, original
exits, GET `/quit`, namespace/pidfd cleanup and unchanged-parent check. Keep
the private INI `log=` setting and information-level logging. Do not restore
the unsupported `--log-path` option or an 8 MiB hard ES file limit.

This source-only command recovers nine exact small inputs (51,406 bytes) from
immutable git objects and verifies them against the accepted run's bindings:

```bash
python3 prepare-inputs.py \
  --repo /workspace/repos/rocknix \
  --output /tmp/pix567-installed-topup-source01
```

It does not execute or import those files. Output is deliberately under
`accepted/`, mode 0600, with `SOURCE-ONLY.json`; the contained runner still uses
the fake ctl and must not be presented as the installed continuation.

## Minimal additive adapter, before allocation

1. Derive only the success/API route from that runner. Remove the bind of
   `HERE/raofflineproxy-ctl` over the installed ctl and its executable-seam
   prerequisite. Do not wrap, relocate or edit the real ctl: sibling helper
   selection depends on its original installed path. Record hashes before and
   after of the ctl, cache-indexed, cache-images, ES, installed proxy `.pyc`
   files and native library. Resolve expected bytes and ES source pin from the
   final distribution/image manifest; the old accepted binary is not the new
   installed binding. ES `3178b832b8d134198b2b4eede4f725d4ed283f8c` is pending
   integration at this source read, not silently assumed installed.
2. Keep the no-NIC parent, private mount/network namespace, fixed private hosts,
   files-only resolver and loopback TLS peer. Add an observer-only bootstrap
   for the already accepted explicit substitution
   `network.has_active_network_interface = lambda: True`, with a visible receipt
   and installed `.pyc` import checks; allow real probes, HTTP, credentials,
   caching, timers and helpers to run. Import/guard errors must terminate with
   their original failure, not be swallowed by Python's `sitecustomize` loader.
   The complete #588 bootstrap cannot be copied unchanged: its audit policy
   allows ports 8080/18081 and forbids subprocesses/scratch outside its service
   state. Reuse only this one interface seam and the installed-import binding
   pattern. No source or native overlay is needed for an indexed metadata job.
3. Write only a named synthetic username/token to private `system.cfg`, retain
   `offlineproxy=1`, and create private proxy configuration/storage. Keep real
   history empty. Seed the already identified existing game 4242002 via the
   installed `Storage`, `cache_keys` and export functions: account-scoped patch,
   unlocks, achievementsets, local session and hash alias. Assert ready IDs are
   exactly `{4242002}` and no last-scan exists before arming. Do not seed a ready
   text file without the matching real account-scoped SQLite rows. New game
   4242001 must have no cache rows before the trigger. Keep both text-only
   metadata stubs and the `/bin/false` system command; do not launch a game.
4. Extend the existing strict TLS peer, without a forwarding client: retain
   the two exact indexing GETs; allow `HEAD /`; allow authenticated GET `patch`
   (`g,u,t`), `unlocks` (`g,h=0,u,t`) and `achievementsets` (`m,u,t`) only for
   the new synthetic game/account/hash. Reject extra, duplicate or unknown
   parameters, bodies, hosts, SNI names and methods. Do not log credential
   values or complete request URLs. Use valid synthetic success payloads,
   with root `GameId=4242001` in achievementsets and no image/badge URLs.
   Set `RAOFFLINEPROXY_CA_FILE` to the peer's generated certificate in the
   allowlisted environment; the real proxy verifies TLS. No global CA change.
   Preserve the existing refusal controls and atomic count receipts.
5. Account for the real ctl's fixed scratch and lock locations. Its scan lock
   is `/var/run/raofflineproxy-scan.lock`; the pending route can also write
   `/var/run/raofflineproxy-index-pending.lock`; probe/job/readiness scratch is
   under `/tmp`. A private `/storage` alone does not isolate these. Give the
   derivative private scratch/lock custody, or explicitly record and restore
   their original disposable-guest state after proving no concurrent proxy
   preparation. Keep the live Wayland socket visible if isolating `/run`.
   `logger` also reaches the guest journal: record this bounded, synthetic-only
   side effect rather than claim the old file census proves journal identity.
   Do not start the proxy service for this CLI path. Actual service/default-boot
   qualification is the separate #588 continuation.
6. Replace fake ctl-event/stamp assertions with the real evidence below. Allow
   the actual top-up to complete within the existing 240-second owner; the old
   fake-ctl 15-second wait is not an established timing claim for this route.
   Preserve the product's 900-second top-up budget, nine/10-second probes,
   throttle and all helper bodies. An outer timeout is a retained failure,
   never a successful shortened product run. The image/VM owner remains the
   coordinator's existing watched 8 GiB, four-vCPU, no-NIC allocation.

## Exact remaining trigger and required evidence

After source review, final installed binding, real frontend readiness and a
fresh synthetic-state baseline, the existing runner makes the sole request:

```python
api('/reloadgames')
```

Actual ES then starts this installed command; the fixture must not invoke it a
second time or replace its process:

```text
/usr/bin/raofflineproxy-ctl topup --after-index
```

Keep the existing actual library-rescan log barrier and recovery XML assertion
for `recovery/gb/new.xml` with ID 4242001. Require exactly one native ES log line
`OfflineAchievements: topup --after-index exited 0`. Retain the real `scan.log`:
one indexed game, hash reused, asked patch/unlocks/achievementsets; recently
played pass exits 0 with no work; the real image pass exits 0 with no URL work.
`cache_images=false` alone would not bypass the ctl's final image pass.

The peer's post-control delta for the happy route is one hashlibrary GET, one
officialgameslist GET, **two HEADs** (ctl probe and the separate recently-played
process's online check), one patch, one unlocks and one achievementsets GET.
No gameid/login/startsession/award request is expected. `cache_session` writes
the startsession cache locally. Record unknown/refused requests as failures,
not as an omitted count. No public RetroAchievements request occurs.

Open the real SQLite database read-only after the ES-observed command exit.
Require integrity `ok`, the five new target cache keys (gameid, patch, unlocks,
achievementsets, startsession), correct game/account/hash associations, patch
`sourceRomPath=/storage/roms/gb/new.gb`, and unchanged existing-game data. Check
actual cached IDs `{4242001,4242002}` and the real `last-scan` fields:
`rc=0`, `route=topup`, `cached=1`, `indexed=1`, `ready=2`, `added=1`, `errors=0`,
`limit=0`, with no failure reason. Preserve account values only inside synthetic
state; exported assertions report booleans/counts/key categories. Neither ctl
exit 0 nor a patch row alone proves unlocks and achievementsets were stored.

Retain hashes and original bytes of the installed binding, seed/pre-trigger
receipt, peer counts/guard receipts, real scan log and stamp, row assertions,
unchanged stubs, one extra library load, normal ES GET `/quit` exit 0, listener
exit 0, worker exit 0, outer watcher/monitor/result consumption and cleanup.
Any forced child kill, namespace survivor, wrong installed identity, missing
new rows or changed parent fixture boundary prevents PASS. Normal cleanup must
retire the fresh VM and scratch only after compact original evidence is kept.

The deterministic remaining blocker is fixture adaptation, not product source
or compilation: merely deleting the fake ctl bind cannot pass (loopback probe
refusal; unsupported authenticated TLS endpoints; no matching synthetic account
cache), and the current runner has no installed-backend assertions. No runnable
installed adapter or image result is claimed by this plan.

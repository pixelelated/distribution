# The lane's grades of Gemini 4 Argon's 39 items (T19, #666)

Each item is re-read at its lines before its grade. The new re-reads are `rereads/r36.out` (`usage_report.py:177-196` at the patched pin) and `rereads/r37.out` (the ctl's `take_lock` :1188-1192, the scan's EXIT trap :1979-1982 and `cancelled` :1811-1822 at `8ebaf8daad`). The rest rest on the stage-B reading and Astra's re-reads.

**Counts:** accepted 35, accepted in part 2, plausible 2, rejected 0 (39).

| Item | Grade | What the re-read showed, and what changes |
| --- | --- | --- |
| R-1 | accepted | F-01 as Astra's A-1; the conditions agree. |
| R-2 | accepted | F-02 narrowed (the peer check); a rebind read needs the upstream to fail in the same window. |
| R-3 | accepted | F-35 is wider: uppercase `T=`/`P=` pass too, and the quarantined store's regex needs well-formed JSON, on a file quarantined because its JSON was bad. |
| R-4 | accepted | As A-4. |
| R-5 | accepted | As A-5. |
| R-6 | plausible | **Against A-6:** with `Type=simple`, `ExecStartPost` runs right after the fork, and the unit's own comment says the port is bound "seconds" later (`raofflineproxy.service:34-36`). So a pre-existing foreign listener satisfies the first look, `enable` completes, and the service then dies on `EADDRINUSE`. This restores F-03's toggle-on path as plausible; not run (the guest showed `listening` only). F-03 stays Low. |
| R-7 | accepted | F-04: the service parses untrusted network bodies and ROM images in native code (`libraproxy_rchash.so`), so containment matters even on a root device. Info stands. |
| R-8 | accepted | As A-8. |
| R-9 | accepted | As A-9, plus `last-scan.tmp` left on a failed write. |
| R-10 | accepted in part | F-08 as written; the claim that `list_jobs` never closes its `Storage` is refuted: `storage.close()` at ctl :1564, after the indexed read. |
| R-11 | accepted | As A-11. |
| R-12 | accepted | As A-12. |
| R-13 | accepted | F-26 is wider: `int(body["Score"])` takes a JSON boolean (`bool` is an `int`), printing `score=1`. |
| R-14 | accepted | F-17 narrowed to selected paths; a loud failure, not a silent one. |
| R-15 | accepted | F-24 is wider: the skip pattern is tested first, so a filename with `Hash failed` turns real failures into skips and resets `IN_A_ROW`. |
| R-16 | accepted in part | The bounds rows as A-16 to A-20. The claim that `cache-indexed` waits on non-daemon threads after its join depends on `shutdown_image_downloads`, which was not read: plausible only. |
| R-17 | accepted | F-34 is wider: `run_jobs` removes `running` (ctl :1786) before the scan's image pass, so the interface sees no run for up to 300 s while one is going. |
| R-18 | accepted | F-14 is wider: `http_post` also skips the request throttle `http_get` waits on. |
| R-19 | accepted | F-01 Low; the fix compares a presented credential and the configured account; old accounts' rows are left on devices. |
| R-20 | accepted | F-02: reject a foreign `Host` and any `Origin`. |
| R-21 | plausible | F-03 Low, with R-6's path. |
| R-22 | accepted | F-04 Info; `UMask=0077` and the sandbox directives without a user migration. |
| R-23 | accepted | F-05: the environment at all five sites. |
| R-24 | accepted | F-06 Low; `/var/run` is tmpfs, so a lock path left a directory clears at reboot. |
| R-25 | accepted | F-07 Low. |
| R-26 | accepted | F-08 to F-10 Info. |
| R-27 | accepted | F-12 and F-15 proposed Low; F-13 an availability fix; F-14 Info. |
| R-28 | accepted | F-16 Low; F-17 Low (`errors="surrogateescape"` at both ends). |
| R-29 | accepted | F-18 is wider (the image helper's `argparse` 2); F-19's `b` has three meanings; F-20 to F-25 as written. |
| R-30 | accepted | F-27 as Astra's A-47. |
| R-31 | accepted | F-28 as A-48. |
| R-32 | accepted | F-29 is wider: `mapfile` in `run_jobs` desynchronises from `TOTAL` too (ctl :1707). |
| R-33 | accepted | F-30, and **new (F-36, Info):** on patch 013's `+` side, `_fetch_image` raises out of its retry loop on a short read over a reused connection instead of retrying or falling back to `_fetch_with_urllib`. |
| R-34 | accepted | F-31, and **new (F-37, Info):** a non-numeric `Content-Length`, a non-UTF-8 body and a non-integer `g=` each raise unhandled in the request path (`proxy_service.py:298`, `:303`, `:439`); the thread dies, the server stays up; loopback only. |
| R-35 | accepted | F-32 and F-33 as A-52 and A-53. |
| R-36 | accepted | **New (F-38, Info):** `usage_report._report` takes `storage.load_login_credentials()`, the first login row whoever's it is, which patch 007 replaced in `resolve_credentials` (`usage_report.py:185`); consent-gated, upstream's (a #585 line). |
| R-37 | accepted | **New (F-39, Info):** `take_lock` opens fd 9 without close-on-exec, so every helper inherits the locked file; the EXIT traps kill `CLIENT` without waiting, so a helper that outlives the ctl keeps the lock held under a pid that is gone, and `cancelled` reads the store while the helper still writes it (ctl :1190, :1811-1822, :1981). |
| R-38 | accepted | **New (F-40, Info):** `row_ages` reads three whole prefixes per game (quadratic over `--all`); the refresh never shuts its badge pool down (plausible: the pool's internals not read). No interface caller at the pin. |
| R-39 | accepted | **New (F-41, Info):** an `I` job with no id or hash falls through to the hashing path (`cache-indexed:182`, `:196`); only a malformed job file reaches it, since `list_jobs` writes `I` with both. |

**A correction to R-10, made here:** Argon says `list_jobs` never closes its `Storage`; the listing calls `storage.close()` after the indexed read (ctl :1564). The finding (F-08) is unchanged.

# Source trace and containment argument

Inspected ES `e87d0d1b4562adfb9e5b8b6882c0c655ed611afc`, the received #575
composition, read-only. Relevant #567 behavior comes from the previously
accepted `6b1dd68246c89f4c1c0fa17c3d8941ffd3b3d420` proposal. Distribution
evidence base is this worktree's `44d4553a8479a4df647ed785ee434782c93db983`.
Per-file Git blobs and SHA256 are recorded in `source-bindings.json`; the
fixture does not change either baseline or infer the next candidate's pin.

| Source / anchor | Consequence for this harness |
| --- | --- |
| `RetroAchievements.cpp`, `getCheevosHashes()` | Constructs both fixed `https://retroachievements.org/dorequest.php?r=hashlibrary` and `...?r=officialgameslist`. No ctl URL override reaches these calls. Official response must contain `Response` game IDs; only integer `MD5List` IDs present there survive. Both supplied synthetic response shapes match the parser. |
| Same file, `getHttpOptions()` | Starts default `HttpReqOptions`, optionally derives User-Agent from configured login. Synthetic system config has no login; no real credential is needed for these two global index endpoints. |
| `HttpReq.h`, default options | Connect 10 seconds, total timeout 0, cookies enabled. `getCheevosHashes()` adds a 30-second low-speed/stall bound. Moving bytes can extend a fetch, so the harness additionally bounds the entire owner. |
| `HttpReq.cpp`, `performRequest()` | Fixed URL passed to `CURLOPT_URL`; follows redirects, max 2, redirect protocols HTTP/HTTPS. Sets `CURLOPT_SSL_VERIFYPEER=0` unconditionally. Sets `SSL_VERIFYHOST=0` only in the client-cert branch, not used by these calls. Cookie jar resolves into synthetic ES storage. No Linux `CAINFO`, `CAPATH`, `RESOLVE` or explicit proxy override; Windows registry proxy code is excluded. |
| Distribution curl recipes | Target enables OpenSSL TLS, threaded resolver, proxies and IPv6; default CA bundle is changed from `/run/libreelec/cacert.pem` to `/run/rocknix/cacert.pem`, CA path is `none`. A curl-CLI environment variable alone is not a replacement for tracing ES's libcurl options. |
| `ThreadedHasher.cpp`, `start()` and constructor | Already hashed+identified game does no work. Prehashed/no-ID new game goes to `lookupOnly`, library fetched once, matching ID queued. Once-daily silent lookup stamp initially 0. Empty work returns before networking. |
| Same file, `run()` / destructor | Lookup-only skips CRC and ROM hashing, writes changed ID via `saveToGamelistRecovery()`. Completed, non-cancelled identified work calls `topUpAfterIndex`. Hash-library exception leaves no new ID or completed-work top-up. With lookup-only input the search queue is empty on fetch failure, so the existing offline-index card/marker is **not** promised by this fixture. |
| `OfflineAchievements.cpp`, `topUpAfterIndex()` / `runTopUp()` | Backend path existence and offline toggle gate `/usr/bin/raofflineproxy-ctl topup --after-index`; logs the actual returned exit. No frontend account check precedes this call. |
| ctl `refuse_unless_ready()` / `do_topup()` | Real top-up acquires lock, checks toggle/account, then probes before listing/caching. No-account exits `EX_NOPERM` (77); this packet simulates that boundary. A simulated success is not the real backend's authenticated result. |
| `ProxyCards.cpp`, `runTopUp` worker | Reads `running`/`last-scan`/ready IDs; quick completed work can produce its outcome from a current stamp. No-account/no-work with no stamp does not claim an added-game count. |
| `GuiMenu.cpp`, `updateGameLists()` | One conditional explanatory paragraph when backend exists, offline toggle on and startup index on. Existing YES/NO and busy guards remain. |
| `HttpServerThread.cpp`, `/reloadgames` / `/quit` | Local API posts `updateGameLists(w,false)`; bypasses question. `/quit` requests normal ES quit, not reboot/shutdown. API request acceptance is not completion. |
| `ViewController.cpp`, `reloadAllGames()` / `SystemData.cpp`, `loadConfig()` | Rescan invokes startup index exactly once through loadConfig's window; no second post-failure fetch. Its actual loading log is the zero-work barrier. |
| `Paths.cpp`, ROCKNIX branch / `Gamelist.cpp`, recovery | Runtime config is `/storage/.config/emulationstation`, system config under `/storage/.config/system/configs`, recovery `recovery/gb/new.xml`. `--home` alone would not isolate these paths. |
| `CustomFeatures.cpp` / `SystemData.cpp` | Minimal fixture `gb` system with libretro/gambatte `cheevos` feature is eligible, visible, not a collection. Command `/bin/false` never launches an emulator even if mis-selected. |
| ES packaging / `essway.service` / `start_es.sh` | Resources and locale can refer through runtime storage; fixture makes the necessary read-only-default symlinks. Launch binary directly; do not source `es_settings`. |

libcurl's official documentation confirms that hostname verification defaults
to 2 and is independent of certificate-chain verification. Disabling peer
verification skips loading CA certificates for that check. The generated SAN
therefore matters even though ES does not need a trusted CA for these calls.
[VERIFYHOST](https://curl.se/libcurl/c/CURLOPT_SSL_VERIFYHOST.html),
[VERIFYPEER](https://curl.se/libcurl/c/CURLOPT_SSL_VERIFYPEER.html), read 2026-10-13.
libcurl also reads proxy environment variables independently of the curl CLI;
the fixture passes an allowlisted environment and `NO_PROXY=*`.
[libcurl environment](https://curl.se/libcurl/c/libcurl-env.html), read 2026-10-13.
These are source/documentation findings, not a claim of runtime TLS proof.

Public RA and other endpoints are denied by construction, not by certificate
trust. The parent guest has no NIC; the worker unshares a new network namespace
and adds no interface except bringing up its existing loopback. Files-only name
resolution maps only the expected RA hostname to loopback. Thus DNS names not
listed fail resolution, and numeric non-loopback destinations have no route.
IPv6 has the same interface boundary. There is no external proxy in the
allowlisted environment. Redirects could be followed by production libcurl,
but could reach only those same isolated interfaces. The TLS fixture sends no
redirects and has no HTTP client, subprocess forwarding or provider code.

Within the namespace the server listens on `127.0.0.1:443`. Exact Host/SNI and
the two exact GET targets are required; unknown query parameters, targets,
hosts and upload methods receive refusal. `/dorequest.php?r=login` in a negative
control carries no account data and never leaves loopback. Request bodies,
arbitrary headers, unknown URLs and their hashes are not logged. Kernel/API
negative controls record categories and error numbers. The binding proof does
not purport to inventory every attempted outbound endpoint or make a general
security claim about production ES.

Reusable-source search covered TLS constructors/certificate commands in
`tools/` and Python/shell QA fixtures. Existing `tools/ra-ui-test` and
`tools/raofflineproxy-consent-test` use loopback HTTP for different installed
backend seams, not the fixed HTTPS ES fetches. Their separation of synthetic
data/provider boundaries informed this packet; neither is run, copied or
represented as TLS proof. Decision archaeology remains D-RA-035, D-UI-106/107;
the cached complete #567 body has zero comments, and the prior immutable packet
records its complete live intake. No tracker/shared-record mutation occurs.

# #603: five blind leads, independent source verification

Read-only review of G-04/G-05/G-11/G-12/G-13. Distribution source is exactly `cdd92f10605517e789e09d13b6f4ba68573c2617`; ES is exactly `16dbac5211eea7e70db7394372033be2be7df829`. Full source hashes, Git blob identities and retained-record locators are in `source-bindings.json`. No provider call, product/shared-record edit, runtime, device read, helper import/execution, fixture/test run or archive expansion occurred. Source and ordinary metadata were read only. This note makes no new runtime qualification claim.

## G-11: confirmed recurring automatic-retry defect; format support remains deliberately bounded

`es-app/src/GameCubeRvzHashRetry.h` (SHA256 `7eb61676391b8541e3fecda77138dbc9e6894c1cb2fa4c971619629ee5598b33`) is header-only, not a missing .cpp. Lines16–29 restrict repair to an enabled reader, an unambiguous GameCube system, RVZ extension and absent/zero ID. Lines31–43 return true for absent, malformed or all-zero hashes. They carry no attempt/version/file-identity marker or cooldown.

Exact causal chain:

- `SystemData.cpp:1098–1134` starts silent indexing when `CheevosCheckIndexesAtStart` is on. Its ten-minute limiter applies to the link-up retry, not startup/update-gamelists. This is conditional automatic indexing, not every boot regardless of settings.
- `ThreadedHasher.cpp:325–327` overrides the normal index decision to `Hash` for every matching failed RVZ; line227 forces `FileData::checkCheevosHash` past its existing stored-hash guard. The daily lookup-only throttle at361–381 does not apply because this entry is in `searchQueue`.
- `RetroAchievements.cpp:935–950` returns the all-zero sentinel on any hashing failure. `FileData.cpp:2175–2184` saves that sentinel to metadata/recovery. `ThreadedHasher.cpp:239–245` leaves/sets the no-ID state when the hash is not in the library. The same predicate is therefore true on the next eligible start.
- `cheevos.cpp:170–172` dispatches GameCube RVZ directly to `generateGameCubeRvzHash`. `rvz_hash.cpp:177–179` intentionally rejects non-GameCube/unsupported compression (supported modes are NONE/Zstandard). Unsupported, malformed and read failures collapse to false, then the same zero sentinel. A valid nonzero unmatched hash is correctly excluded by the retry helper and stays lookup-only.

Impact: repeated automatic hash attempts and hash-library acquisition instead of one repair of an old failure. `RetroAchievements.cpp:865–866` constructs hash-library and official-games HTTP requests; `ThreadedHasher.cpp:65–78,110–115` can show the existing offline-index notification when the library does not arrive. Offline library failure empties the queue before hashing, so do not claim ROM I/O on that path. Unsupported codec rejection occurs early; the 128MiB hash-read/512MiB decoded limits are ceilings, not observed per-boot costs. There is no tight infinite loop within one run.

Disposition: the supported NONE/Zstandard parser repair remains supported by its existing proofs; support for every RVZ compression was never established. The permanent-failure automatic requeue is a concrete separate availability/performance defect requiring root disposition. Existing source controls/format proof do not establish retry termination. The retained #574 body says explicit scanner retry preserves existing automatic policy; that wording does not describe the ThreadedHasher override. The record distinguishes absent sets, valid unmatched hashes and unreadable/unsupported/runtime categories, but this hashing API does not supply separate unreadable-versus-unsupported reason codes. Do not invent such UI/status evidence or automatically reinterpret AC-59 as requiring new UI categories.

## G-04: confirmed intentional refusal after kill; no new data-loss finding

Frozen `dolphin-save-paths` SHA256 `507ccc96245bfc7aaca5e154ef0567cacccd0cbc9d0f999761d2fdee1fc245e8`:

- Lines156–158 refuse either reserved stage when it already exists.
- Lines197–200 explicitly document killed-copy refusal until review;224–238 remove only the current invocation's still-owned, unactivated stage in `finally`. SIGKILL/power loss cannot run that finally.
- Lines254–261 copy from retained `/storage/.config/dolphin-emu/GC`, excluding managed cards/regions for the GC root. This is not a proven immutable-only shipped-resource source. Across restart there is no durable inode/owner receipt authorizing deletion of any object merely found at the reserved name.
- Lines101–106 and68–76 name the actual path in the localized instruction to back up and arrange data in the file manager; this does not specifically instruct unconditional deletion.

The already-transferred original `candidate-receipts/result.json` (SHA256 `9d4a90d4fc1d8dd577be2c4be9a76168a6f6c2b9d6d3038fa93dbf1057f13303`, packet lines325–331/741–747) records both GC/Wii kill-copy original -9, retry250, PASS under the preservation/refusal contract. I read that preserved packet text, not a newly expanded archive. AC-35/36 expressly allow refusal of ambiguous preparation while preserving data and preventing engine launch; they do not promise automatic interrupted-copy recovery.

Disposition: retain as a known safety/UX limitation, not a newly demonstrated loss or noncompliance with those interruption criteria. `docs/es-menu-map.md:379–400` documents generic retained-state refusal/action/return, but lacks a dedicated reserved-stage recovery example. A narrow guidance clarification is possible; the blind suggestion that unconditional discard is already proven safe is not established by this source.

## G-05: normal production route is covered; conservative fallback is intentional

Frozen `cheevos_dolphin.sh` SHA256 `01473794711dafd9607e1b6894ec482e34820807b81e1c45c352d5da9768c28a`, lines115–145, expressly requires offlineproxy1, raw hardcore0 and an IPv4-capable listener. Empty/unknown hardcore keeps customhost even though the existing INI Boolean conversion at93–99 yields False. This is the documented guarded policy, including synthetic missing/unknown controls, not an inferred normalization rule.

The producer contract is concrete: frozen `raofflineproxy-ctl:473–478` writes hardcore0 and verifies it before writing/reading offlineproxy1. ES `GuiRetroAchievementsSettings.cpp:479–501` invokes that producer and mirrors its result; the shipped system.cfg line80 also starts with hardcore0. It is unnecessary and too broad to claim every possible ES/external edit always serializes this key.

For IPv6 wildcard, `/proc/net/tcp6` alone does not establish whether the socket accepts IPv4. The exclusion is explicitly documented in `raofflineproxy-ctl:909–923`. G-12 below supplies the actual proxy source, which uses AF_INET. No supported default IPv4 proxy is excluded by this check. A manually changed/malformed configuration or future IPv6 transport remains outside that source proof; fallback preserves the configured host. No service-authentication/readiness claim follows from socket presence.

## G-12: supplied proxy bind source closes the packet-source omission

The existing `/tmp/m7-proxy-product-source-20261014-01/source.json` binds upstream `c7ebd1b6e777f3751ff0ecdf8aba54045844e00d`, archive `88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b` and recipe `e13f5bb22eae74c73ecb4141c3580f2627b9f8cfc317840656d90ed017e0f13d`. I independently matched all18 composition patch hashes to frozen cdd92f and the five named resulting Python files to the recorded composition hashes, without applying patches or opening an archive.

- `config.py:284,365–377`: non-Spruce default8080; host default127.0.0.1. SHA256 `3184e88b2eac7b5da3a5e0f5906ae193f1dcda7df7e0849d05cd5ec91fe5e3bb`.
- `proxy_service.py:268–270,338–354`: ThreadingTCPServer inherits TCPServer without overriding address_family; ProxyRuntimeServer binds `(host,port)`. `boot.py:32,58` explicitly creates/adopts AF_INET sockets. Proxy service SHA256 `432bb07ac6b0abcdcb38800d7c75a92c768b2b6bea583a1bab6834bb7f7b0d00`.
- `main.py:396–397` → `service.py:365–404` → `proxy_service.py:1442–1454` is the packaged run-service path. The exact frozen unit ExecStart invokes it and ExecStartPost uses the same IPv4 readiness predicate.

This satisfies the blind request's alternative “or the proxy bind source.” Existing installed startup analysis retains original0 and actual installed identity, but I did not reread its archived socket payload, execute a service or manufacture a fresh installed socket observation. Config overrides and unrelated listeners are not authenticated by these checks.

## G-13: resolved packet omission, exact launcher span and receipts

Frozen GC launcher SHA256 `b5e7afb8f3952f8082d4f39c70cffb9e5ccbd7a265cc6c28f1e96aefbb31c568`: lines426–433 call the helper, save its status, continue for0|1 and exit otherwise; actual engine invocation is478. Wii SHA256 `8843d7358f948add1c53851cef2cfb2da2cd93141ad14784c46252bffbada3d7`: same block395–402, engine442. The 237-byte snippets spanning GC426–434/Wii395–403 hash exactly `f365d6319de66f53bf7d9638b80a620d5fc5f0cfc5470a9abccca76f81400403` as the retained receipts claim.

Helper lines77–90 publish inactive state before returning1 for disabled/missing token; failed publication takes the error path instead. The already-extracted final-clean/final-retained `dolphin/result.json` hashes `a935b7bdc712a69a87300216d0cc915e5af3730c72e689219a3b4c592adbfad1` / `ef4183a7ff2178533075a891422d1581573734934a9f8c77c239617f4492aab0` match retained custody. Each records disabled and missing-token original0 at the launcher wrapper, engine marker present, inactive-session publication and23 protected files unchanged. They are full-helper/exact-block synthetic-marker proofs, not actual gameplay/authentication. No source defect remains in this lead.

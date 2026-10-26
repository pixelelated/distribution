# Retrospective audit — M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

Written by the first reader (Opus 5.5) after stages A and B and the first guest window, before any seat saw the packet. Line numbers are the pin's (`16dbac5211`) unless they name a script, which is `8ebaf8daad`'s.

## 3.1 Architectural coherence

- **Two stores, two contracts.** `SystemConf` (`system.cfg`) is the fork's rebuilt writer: `PidLock` around the read-modify-write, `AtomicFile::writeText`, the record published after a re-read under the lock (#320), and pending changes kept across a refused save. `Settings` (`es_settings.cfg`) shares only the primitive (`writeText`) and the ladder's shape: no lock, no mutex, and no test. D-CLOUD-079's sentence describes both as locked (L-13).
- **The primitive is sound and the store around it leaves litter.** `writeText` holds under a kill at every step (99 of 99). Since PL-063 gave each write its own temporary, the old sweeps no longer match, and a kill's temporary stays for good (L-09).
- **One network client with no thread of its own.** Every `HttpReq` is completed by whichever thread next calls `status()` under one static mutex. That is why #299's silence held the interface thread, why one page's wait completes another's request, and why `mStatus` is a data race (L-04). The option set is upstream's, with the fork's `stallTimeout` added; the peer is never verified (#1154).
- **The shell bridge has three quoting rules.** `shellQuote` where the fork wrote the call (13 `wifictl` sites); double quotes where upstream did (16 rows, the live ones `7z` and poppler over a player's file name, L-01); bare where a script's own output is joined (safe by shape). The argv executor (`WifiScanProcess`) exists and is used once.

## 3.2 Project conformance

- **`engineering-practices.md` § Guards must fail closed:** `executeEnumerationScript` discards the exit (L-17), eleven exit reads take a signal for exit 0 (L-18), and `wifictl` exits 0 with no device, which the page reads as CONNECTED (L-22).
- **§ The last known good state is a record:** the shell's seed is copied before the record is consulted, and the interface then records it (L-10). A download removes the file it replaces before the bytes arrive (L-03).
- **`upgrade-and-install.md`:** a device that upgraded keeps its `system.cfg`'s mode, and the seed ships 0645, so nothing narrows it (L-21).
- **`es-code-traps.md` § A pooled connection:** the scraper's probes have no stall bound (`ScreenScraper.cpp:1030-1032`, `:1067-1068`); the hash library's fetch is T20's.
- **`es-player-text.md`:** the one sentence a recovery shows (`main.cpp:1041-1042`) is plain and said once; it says "damaged" for a file that was missing too.

## 3.3 Spec fidelity

The brief's figures held at their hashes (`01` § Scope, `02` § The runs). Three of its comments were corrected by its own commands (`02` § Corrections to the brief), and the coordinator's ruling of 22:35 took both stage-A deltas.

## 3.4 Platform conformance

- **The image is M7's composition over the pin.** Five of the six OS files are `8ebaf8daad`'s bytes; the seed `system.cfg` differs in content and is 0645 against git's 0644.
- **`/storage` is ext4 `rw,noatime`,** so the shell writers' rename without `fsync` is covered by `auto_da_alloc` when it replaces an existing file. It is not covered for the seed's `cp` over a missing file.
- **`7zr`, `pdfinfo` and `pdftoppm` ship,** so L-01's rows are live code. curl lists `file` among its protocols; the status-0 path closes it.

## 3.5 Cross-system interaction audit

### Interaction: the shell's writers (T1) x the interface's recorder

`set_setting` seeds a missing `system.cfg` before its lock and without the record. The interface's next load takes any usable, whole live file as the record (`AtomicFileUtil.cpp:352-361`, `SystemConf.cpp:232-238`), so the seed replaces the player's record. Either side alone is reasonable; together the record is lost (`shell-writers.out` S1). How the live file comes to be absent while a `set_setting` runs after boot's `chksysconfig verify` is T22's boot order, not read here.

### Interaction: D-NET-009's empty line x the interface's parse

The shell writes `system.hostname=` on purpose so `chksysconfig`'s sentinel survives. The interface's parse drops an empty value, and `get` answers the table's `BATOCERA` (`state-units.out` U1; on the image, `frames/g05-network-settings.png`).

### Interaction: `wifictl` x the Wi-Fi page

`wifictl` exits 0 with no device; `enableWifi` reads `system() == 0`; the page saves the network and the key and says CONNECTED (L-22). The key is argv of three processes while `wifictl` lives, and of `nmcli` for up to 90 s on a device (L-08).

### Interaction: the scraper x `HttpReq` x the unverified peer

Every scraper request carries the developer pair and the player's account on its query, to a peer `HttpReq` never verifies (#1154). The server's answer then decides the media URLs and the saved files' extensions. `file://` and the extension-as-path were read and closed (`02` § The leads, closed); the download that removes its target first is not closed (L-03).

### Interaction: the settings archive (T17) x a kill's leftovers

The archive takes the stores by exact name (`backuptool:283-292`), so a writer's leftover temporary stays on the card and never reaches a cloud (L-09).

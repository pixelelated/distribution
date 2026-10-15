# Independent blind findings — M7 cadence #603 (Anthropic seat)

Basis: packet text only. I executed nothing, opened no repository, saw no pixels. Where a primary note is my only source I say so. Severities are mine.

---

## A. Confirmed source observations (code in packet)

### G-01 — Client journal pins raw mountinfo rows; uncommitted recovery becomes impossible after a mount-row change
**Severity:** Medium (predicted; no data loss; blocks install; manual filesystem recovery)
**Location:** `Install Steam.sh:1386-1395` (`mount_rows` keeps the whole split line incl. mount ID / parent ID / major:minor), `:1398-1416` (`available` returns `found[0]`), `:1678` (`metadata` persists `"mounts": available(physical)` into the journal header), `:1470-1474` (`journal_schema`: for *uncommitted* rows `need(available(physical) == meta["mounts"], "The previous support storage changed.")`), `:1581-1583` (`inspect_tree` → `load_journal` whenever `.steam-client-update` exists), `:2716` (`tree` mode runs first; failure → `die "Steam client files could not be checked. Nothing was changed."`). `check_probe` (`:1638-1646`) additionally requires equal `st_dev` per path component (`:1275-1280`).
**Trigger:** client transaction interrupted before `committed` (SIGKILL/power loss during the ≤180 s archive transfer or 90 s decode), followed by a reboot or any change to the `/storage` mountinfo row (mount ID / parent ID are kernel-assigned per boot and not guaranteed stable; major:minor can move with device enumeration).
**Consequence:** every later Install Steam run exits at `:2716` before FEX/runtime/client; the stage (≤128 MiB archive + ≤384 MiB payload) is retained indefinitely; no code path cleans or offers to; the bash message names no path. The AC-31 kill controls (cases 10-14, `[1,0]`) cannot observe this because mount rows are stable within one boot. FEX and runtime recoveries do *not* persist mount rows (they use `no_mounts` + identities), so this is specific to the client journal.
**Refutation:** in the VM, SIGKILL the client python during transfer, reboot, run `steam_client_state tree` → show exit 0 and journal recovery; or show `available(physical)` byte-identical across ≥3 reboots on GENERIC_X64 and SM8550.

### G-02 — `registry.vdf` unconditionally overwritten on every run, including the "existing client kept" path
**Severity:** Medium (state preservation) — **scope-edge**: not named in the 67 criteria; likely upstream-inherited
**Location:** `Install Steam.sh:2367-2370` (`cp -f /usr/share/steam/registry.vdf "${STEAM_DOT}"`), called at `:2747` after `install_steam_client_arm64` returns 0 for both fresh and existing (`:2292-2294`). Contrast the careful preservation of sibling entries `physical/steam`, `physical/sdkarm64`, `package/beta` (`:1671-1694`).
**Trigger:** player re-runs Install Steam (e.g., to pick up a new Proton) with an existing Steam setup.
**Consequence:** player-owned Steam registry state (AutoLoginUser/RememberPassword, CompatToolMapping, …) replaced by the packaged template.
**Refutation:** show the 18 protected roots include `${STEAM_DOT}/registry.vdf` seeded with non-template bytes and unchanged after the complete caller; or an ADR declaring the file installer-owned.

### G-03 — Exact 55-member archive shape and ~16% size headroom pinned against an unpinned "latest" manifest
**Severity:** Medium (availability/design risk; satisfies AC-32's letter; fail-closed)
**Location:** `:1954` (latest `steam_client_publicbeta_linuxarm64`), `:1193-1195` caps, `:1207-1261` EXPECTED, `:1981` `count == len(EXPECTED)`, `:2000/2003/2006` exact `made`/`attr` bytes, `:2023` `seen == set(EXPECTED)`. Measured from `steam-inspection.json:1634-1637,1457`: archive 110,373,661 B = 82% of MAX_ZIP; decoded 339,635,561 B = 84% of MAX_OUTPUT; largest member 97,036,984 B = 72% of MAX_MEMBER.
**Trigger:** any Valve ARM64 beta client with an added/removed/renamed file, different packer attributes, or >~16% growth.
**Consequence:** all players refused ("Unexpected or duplicate Steam ZIP path"/"Incomplete Steam ZIP inventory"/size errors) until a source release.
**Refutation:** documented monitoring/guidance policy or a version-pinned manifest.

### G-04 — Killed GC seed copy leaves a reserved stage that refuses every later launch
**Severity:** Low (documented limitation; safe; UX)
**Location:** `dolphin-save-paths:156-158,197-199,224-238`; receipts `candidate-receipts/result.json:325-331` (`gamecube-kill-copy` retry 250), `:741-747` (wii).
**Trigger:** SIGKILL/power loss during the first `/storage/roms/bios/GC` seed copy.
**Consequence:** persistent refusal until the player deletes `/storage/roms/bios/.GC.dolphin-new` by hand (path is named in the message via `reject`). The stage holds shipped resources, not player data, so identity-checked discard of the private unactivated copy would have been safe.
**Refutation:** es-menu-map limitation entry with the exact player instruction, or a retained-stage discard proof.

### G-05 — Routing predicate: dual-stack wildcard not recognised; hardcore gate requires literal `"0"`
**Severity:** Low (safe fallback, silent in one branch)
**Location:** `cheevos_dolphin.sh:123-137` (only `0100007F:1F90`, `00000000:1F90`, v4-mapped; `[::]:8080` with v6only=0 treated as absent), `:139` (`hardcore_raw = "0"` only; an absent setting blocks routing while Dolphin runs non-hardcore per `:97-98`).
**Consequence:** offline proxy never selected in those states; only the "nothing listening" case logs (`:143-144`). Pairs with gap G-12.
**Refutation:** show raofflineproxy binds IPv4 loopback and ES always writes `hardcore=0`.

### G-06 — Record-clarity: hardcoded archive hash in the reader
**Severity:** Low (not a product defect)
**Location:** `verify-additions.py:84` `'archive_sha256':'64034fb0…'` is a literal annotation, not a measurement; the archive→member binding actually rests on `archive-reader/result.json:4-5,31-35,94-96`. Also `:106` exempts `usr/bin/steam` (added at `:54`) from the ELF class/machine assertion with no stated reason.
**Refutation:** `products['usr/bin/steam']` header bytes showing a script; none needed for the annotation.

---

## B. Evidence gaps (claim may be true; packet cannot establish it)

### G-11 — Failed-RVZ retry termination and unsupported/unreadable/unmatched distinction
**Severity:** Medium
**Location:** `ThreadedHasher.cpp:35-47,227,326-327`; `cheevos.cpp:170-173`; `rvz_hash.cpp:177` (GameCube only), `:179` (compression 0/5 only — bzip2/LZMA/LZMA2 RVZ are valid upstream variants), `:246,:317` (128 MiB read / 512 MiB decode per file). `generateGameCubeRvzHash` returns `false` identically for unsupported, non-GC, and read failure. `GameCubeRvzHashRetry` and `FileData::checkCheevosHash` are **not in the packet**.
**Predicted consequence if uncapped:** a permanently unhashable RVZ re-enters the queue every start → `lookupsAlone` false (`:361`) → hash library fetched every boot, offline toast every boot (`:75-76,114-115`), up to 128 MiB read/512 MiB decode per file per boot; AC-59's "unmatched vs unreadable/unsupported" cannot be verified.
**Needed:** `GameCubeRvzHashRetry.cpp/.h`, `FileData::checkCheevosHash`, and the stored metadata value on failure.

### G-12 — Positive listener match against the *installed* proxy's real bind address
**Severity:** Low-Medium
**Location:** `dolphin/result.json:30-35` (cases run in private net namespaces; case 02 claim at `:177` is "routing bytes unchanged", not a live-listener match). AC-27's installed startup payload is not in the packet.
**Needed:** `/proc/net/tcp` (or `ss -ltn`) from the installed VM with `raofflineproxy.service` active showing `0100007F:1F90 … 0A`, or the proxy bind source.

### G-13 — Launcher RA block position and exit-1 tolerance
**Severity:** Low
**Location:** `start_dolphin_gc.sh:30,68` / `wii.sh:30,73` show check/prepare; lines 106-end (RA block, engine exec) are absent. `cheevos_dolphin.sh:83,:90` exit 1 after publishing disabled; tolerance inferred only from `dolphin/result.json:20,37`.
**Needed:** full launcher text or snippet f365d631 with its line span.

### G-14 — Unlisted source identity for the host test receipt
**Severity:** Low
**Location:** `qa20-final-result.json:7` source `1a026648…` is none of the declared frozen hashes; tool sha `ebd9a466` not bound to cdd92f10.
**Needed:** ancestry check and `tools/last-good-scripts-test` sha at cdd92f10.

### G-15 — "SOURCE-ONLY UNRUN" label on the executed owner
**Severity:** Low
**Location:** `run.py:2` docstring vs. its use as the baseline-continuation owner; `C['code']` map (asserted at `:149`) not in packet.
**Needed:** `config.json` `code` map binding run.py 5ed44531 to `result.json`.

### G-16 — GENERIC_X64 f863 image build has `qualification: false`
**Severity:** Low (records are honest; readiness wording unknown)
**Location:** `final-result.json:1093-1149` (`original_launcher_returncode: null`, reason `exclusive-wrapper-receipt-collision`, `runtime_qualified: false` at `:4`); the clean/retained VM proofs (AC-37, AC-49, AC-51 "final installed") run on this image. Artifact integrity passed (`:2-3,1072`).
**Needed:** the M7 readiness record's exact statement for GENERIC_X64 f863 (artifact-integrity vs build-submission qualification).

### G-17 — SM8550 image stamp vs producer run id
**Severity:** Low
**Location:** `acceptance.json:23` image `…20261015T075604Z…` vs `:51` producer run `20261015T081827Z-07dceee9` (22 min); the H700 analogue is 28 s (`final-result.json:1101,1143`; tar name 035337Z).
**Needed:** stamping source or the SM8550 submission record tying 07:56 to run 07dceee9.

### G-18 — Component receipts bind an older installer
**Severity:** Low
**Location:** `runtime/…/result.json:280`, `proton/…/result.json:4`, `root/…/result.json:4` all `source_sha256 9e1ce7b5…`; transfer to module 1694f7a9 depends on heredoc ("stdin") hashes I cannot recompute.
**Needed:** line spans + sha256 of the three heredocs in both 9e1ce7b5 and 1694f7a9.

### G-19 — Rectangle claims accept any change inside them; claim text not supplied
**Severity:** Low
**Location:** `tools/frame-diff:192-206` (first live rectangle owns the pixel; correct per AC-17). `claims.composed.txt` (7764b682) and the 348-rectangle diagnosis are hashes only; the "zero outside_carousel_change_support" mitigation and 2-of-78 visual sample rest on records/pixels I cannot see.
**Needed:** claims text + pixel-inventory rows, or one documented pair compared with claims removed.

### G-20 — AC-08 historical receipt
**Severity:** Low (largely closed)
**Location:** `checks/pkgcheck-current/invocation.json:9,13` exit 0 on recipe 6b07c262 (identical bytes to the retained fix, `package.mk:6` = `upstream-fix.patch:18`); stdout empty (`:15`), stderr progress line only. This independently supplies the mechanical check; only the historical `root_reported_status` remains unrecovered.

---

## C. Out-of-scope observations (not among the 67 criteria; stated to avoid silent omission)

- **G-21 (Low)** `Install Steam.sh:240-243` `eval` of GitHub-derived `tag_name`/`browser_download_url` (regexes `:217,:222` exclude only `"`). Injection surface in a root context if upstream metadata ever contains `'`/metacharacters. Upstream-inherited.
- **G-22 (Low)** `:2692-2710` unbounded native first launch; binfmt disabled `:2694-2696` with no trap before `:2709`. Hang / system-wide x86 binfmt left disabled if the script dies mid-window. AC-33 declares native limits unproved.
- **G-23 (Low)** Bound adequacy: client archive 180 s for ~110 MB (`:1962`) ⇒ ≥4.9 Mbit/s sustained; FEX 900 s fetch+extract (`:285`); runtime/Proton 900 s (`:1071,:2631`). Timeouts roll back fully with no resume → slow-link players loop. Refutation: shaped-link VM install at ~10 Mbit/s.
- **Not judged (scope expansion):** whether per-system AUTO SAVE/LOAD rows remain offered for standalone emulators other than dolphin/flycast (`GuiMenu.cpp:10866-10873` gates the dialog to those two; `:5802` global text does not enumerate). Needs `es_features.cfg` autosave flags.

---

## D. What I could independently confirm vs. what rests on primary notes

| Independently supported by packet records/source | Notes-only or not judgeable here |
|---|---|
| AC-01/03/04/06 runner results and timestamps; AC-02 diff/template/12 controls/3 payload readbacks; AC-07 archive-reader + upstream patch; AC-08 (see G-20); AC-12/13 source + 212 controls incl. 40 PPSSPP; AC-14 SM binding in acceptance.json; AC-17 20 controls + old-control stage; AC-18 11.75 s / rc 0; AC-21 `observe()`; AC-25 source; AC-27 partial (4 installed cases); AC-30-32 source + inspection; AC-34-36 104+6+13 receipts; AC-38-40 56 Proton cases + source; AC-49 clean/retained results (≈120-150 ms exit, joined/stopping 1); AC-51 syntax/link originals; AC-52/54 source; AC-53 native inventories (Wii .s01 3732… stable; Flycast 4666→376c only with native auto); AC-57 rvz source + format02; AC-61/62 39 cases + source; AC-65 source; AC-67 merge response + page text matches `GuiMenu.cpp:4905`. | All visual claims (AC-16, 37, 46-48, 50, 53, 54, 65, 66); AC-05/09/10/11/15/20/22/23/24/28/29/33/41-45/55/56/58-60/63/64/66 (receipts described, not included); `set_kill`/runemu kill semantics for the installer's frontend interaction; cloud_scan `MINE` selection source; RetroArch #196 (custody acknowledged missing). The native02 vs native03 Wii state hashes (3732… vs b946…, `state-inventory.json:5-13`) are different runs, not a contradiction. |

No quota was filled: items above are the only ones I could ground in the supplied bytes.
# Independent refutation — #553 (Anthropic reviewer)

Scope read: the 33-file delta, ES test-only diff, applied proxy modules supplied, issue bodies, checks/, and cited qa-log artifacts. I cannot execute anything; probes are named where needed. Frame pixels were not seen by me.

---

## Part 1 — My own findings (independent leads)

### A. Evidence/binding defects (confirmed from supplied bytes)

**F-1 — Stale evidence binding in the #528 citation: dispositions.json describes a pre-bump rclone recipe.**
Severity: Medium (evidence, not product). Not a new punch item for the #528 gates; a citation defect in the primary's AC-528-01..05 blocks.
- `docs/qa-logs/2026-10-11-component-inputs/dispositions.json:412` records `rclone/package.mk` = `9543732dead2…`; `audit/inputs/source-manifest.json:24` and the supplied file hash both say head is `030b2429b9c6…`. All other 12 recipe hashes match head; only rclone does not.
- `dispositions.json:3` base is `153bfa6b79…` (neither delta endpoint); `utc` 16:53Z precedes `fetch.json` 17:02Z, i.e. before the 1.75.1→1.75.2 bump. The rclone "verified_notice_evidence" points at the `m7-prebuilt-aeef83ae…` custody from 2026-10-08 (#528 comment: rclone `687d264b…`), which cannot be the 1.75.2 release (published 2026-10-09).
- Expected: the evidence cited for a head verdict binds to head bytes. Actual: the primary cites a disposition for a recipe/version no longer shipped, while the firmware installs 1.75.2 (`checks/installed-rclone-version.log`).
- Disproof: show a dispositions revision whose rclone entry hashes to `030b2429…` and names 1.75.2 source custody. Until then, the AC-528 evidence line is partially stale (verdict PARTIAL is unaffected).

**F-2 — The "actual 19→20 upgrade" was produced by a variant script, not the delivered tool as cited.**
Severity: Medium (source binding of a composed constituent).
- `upgrade/run.py:23` runs `bash rehearsal.sh …`. The raw transcript (`actual-rehearsal.raw.json:4`) ends with `=== 20:35:54 pair retained for installed verification; outer owner guarantees shutdown` — a line that does not exist in `tools/vm-upgrade-rehearsal` (which at :167 does `say "pair down"; ./tools/vm-pair down`).
- The primary binds AC-545-03/AC-546-03/AC-546-04 to `tools/vm-upgrade-rehearsal:39`. The two `PASS storage ready in boot … after 1 poll(s)` lines match the tool's format, so the function was very likely identical, but the packet contains neither `rehearsal.sh`, its hash, nor `prepared-manifest.json` (consumed at run.py:4).
- Disproof: `diff tools/vm-upgrade-rehearsal docs/…/upgrade/rehearsal.sh` showing only the teardown line replaced, plus the manifest hash.

**F-3 — Delivery/closure state for #548-AC4 and #549–#552 is contradicted by the supplied tracker snapshots and the head commit message.**
Severity: Low–Medium (process/evidence).
- `issue-549.md:13-15`, `issue-550.md:12-14`, `issue-551.md:12-14`, `issue-552.md:10-11`, `issue-548.md:16` are all `- [ ]` with no delivery comment; `history.txt:1-2` (top commit) says "Final portable-helper full regression and image qualification remain in progress; no closure or firmware change."
- `03-retrospective.md:34` claims "Ten completed issues closed from delivered evidence"; `02-forward-audit` grades 12 of those criteria PASS with "exact tracker readbacks are in …/tracker-reconciliation" — not supplied. The random-reverification population (32 entries) also excludes these, consistent with them being unchecked at draw time (20:54Z).
- Disproof: supply tracker-reconciliation and `git log -1 --stat b990d32c` showing the closure/evidence commit.

**F-4 — AC-549 composed acceptance does not consume the original build20 failure it claims to preserve.**
Severity: Low.
- `container-temporary-path/…/run.py:4-5` asserts `pixelelated-m7-build20b` wrapper rc 1 and inner/outer rc 1. The original build20 (rc 2, the actual TMPDIR failure) is never read; `result.json` records only `original_wrapper_returncode: 1`. The primary's text "original build20 remains2" is unevidenced in the packet.
- The three "refusal controls" (`run.py:17-21`) are in-memory mutations of the observation JSON, not pinned-image/nonroot container runs. AC-549-01's "demonstrate the host-only temporary path refusal … using the same pinned image and nonroot user" is therefore satisfied only by the original build20 failure itself, which this verifier does not bind.
- Disproof: the build20 `launcher-result.json`/inner.rc = 2 readback and any `pix549-container-tmp01` negative container run.

### B. Unproven product hypotheses (require probes; not confirmed defects)

**F-5 — First proxy start after upgrade may delay/refuse the listener while `cached_game_meta` is backfilled over an inherited large library.**
Severity: Medium if confirmed; currently hypothesis.
- `applied-proxy/…/proxy_service.py:1439-1444`: `storage = Storage()` runs before `ProxyRuntimeServer(...)` binds; `storage.py:92,285-315` `_index_missing_game_meta` parses every `patch:`/`achievementsets:` body on first open ("1000 games takes about half a minute, once", on SD). The `cached_game_meta` table/triggers are described as new in this pin (`raofflineproxy-ctl:244-245`). The fork's whole-library preparation makes multi-hundred-game caches the normal case.
- The ctl's `listening --wait N` is the unit's ExecStartPost (`ctl:903-955`); if N < indexing time, `enable`/boot start fails and rcheevos gives up achievements for the session. Supplied evidence reopens a **one-game** synthetic store (`guest-proof.py:14-21`, integration `Upgrade`); nothing exercises a large inherited store.
- Mitigating unknown: if the unit uses `raofflineproxy.boot` to pre-bind the socket, connections queue rather than refuse.
- Probes: read the unit's ExecStartPost bound; confirm absence of `cached_game_meta` in 879b158 `storage.py`; time `Storage()` on a VM store with ~500–1000 patch/achievementsets rows; confirm whether the unit binds via boot.py.

**F-6 — ctl ↔ upstream CLI contract at c7ebd1b6e7 is unverified: `probe-online`, `cached-games-count`, `run-smart-cache` are shimmed in the harness and not run in the installed proof.**
Severity: Medium if any verb changed; hypothesis.
- `raofflineproxy-ctl:1138` (`probe-online`), `:893` (`cached-games-count`), `:2354` (`run-smart-cache`). `last-good-scripts-test:2037-2039` states these verbs "are shims". `guest-proof.py` only runs `run-service`. A renamed verb would make every real `scan` refuse as offline (EX_UNAVAILABLE) or break top-up — a silent functionality loss the AC-541-01 wording excludes.
- Probe: on the image root, `python3 -m raofflineproxy.main --help` / grep `main.py` for the three verbs.

**F-7 — `wait_for_badges` depends on private `image_cache` attributes never executed against the new pin.**
Severity: Low–Medium; hypothesis.
- `raofflineproxy-cache-indexed:90-95` uses `image_cache._image_download_executor` and `image_cache.shutdown_image_downloads`; `raofflineproxy-integration-test:74` mocks `wait_for_badges`, and module import does not touch these attributes. An AttributeError would traceback after `DONE` on every real scan (tolerated by the ctl, but badge waiting/dropping would be lost).
- Probe: `grep -n '_image_download_executor\|def shutdown_image_downloads' linux/raofflineproxy/image_cache.py` in the pinned tree.

**F-8 — Patch 004's header overstates what the deliberate scan retains: upstream's inter-request pace cannot fire on the per-ROM drain path.**
Severity: Low (claim precision; not a regression vs. the prior fork pin).
- `rom_browser.py:817-831`: the pace wait requires `requested > 0`; `add_rom_to_cache` drains with `keys=[rom.key]`, so `requested == 0` at the check and the queue empties after one ROM. With `budgeted=False` the only remaining bounds are the 0.3 s `RequestThrottle` and the OS helper's 50/30 s cooldown. The 125-game test finishing within a 6.6 s run (`checks/proxy-fixed.log:15`) is consistent with no pace wait.
- `patches/004…:6-7` says deliberate calls "retain the queue locks, pacing, 429 stop". "Pacing" should read "request throttle"; the 18 s pace upstream added against 429 bursts does not apply. Disproof: a trace showing `wait_for_pace` entered from the helper's H path.

### C. Test/tool defects (confirmed, low)

**F-9** — `tools/raofflineproxy-integration-test:235` `loadTestsFromModule` also collects the imported `QueueTestCase` (:32). It currently contributes 0 tests (log shows 12), but any upstream `test_*` added to that base class would silently join the fork's count. Pin the suite to the fork's classes or assert the discovered set.

**F-10** — `tools/vm-pair:17-18` header still says sockets live at `/tmp/rocknix-qemu-*.sock` while only the pidfile is described under `$RUNTIME`; all three now move with `VM_QEMU_RUNTIME_DIR`. `down` locates guests only via the same env var with no persisted record — a mismatched environment leaves guests running silently. The primary's sibling search shape (`03-retrospective.md:70`) did not include the literal `/tmp/rocknix-qemu`; probe `grep -rn '/tmp/rocknix-qemu' tools/ projects/ROCKNIX/devices/GENERIC_X64/vm/` for unmigrated consumers (e.g. emulator-exit-test, cloud-pair-migration).

**F-11** — `tools/rocknix-info-test:33` gates the "original reproduces arithmetic error" control on `--baseline`; CI (`fork-checks.yml:49`) passes none, so CI runs 12 controls and never exercises the baseline/"presentation unchanged" comparisons. Informational: the audit's `optional-info.log` "13" is the host run with `--baseline`.

**F-12** — `tools/last-good-scripts-test:11078` under `--old`: `vm-upgrade-readiness-test:15` raises an uncaught `IndexError` when the historical rehearsal lacks `wait_for_storage`. The check still FAILs (correct direction) but by traceback rather than a graded message.

**F-13** — `checks/result.json` `recipe_count: 13` vs `checks/pkgcheck.log` showing 14 recipe files (`packages/addons/service/tailscale/package.mk` matched by name). Count is name-based, not file-based; harmless but imprecise.

Product-correctness review of `rocknix-info` (regex bounds, `10#`, quirk status propagation, ARM/x86 branches), `vm-pair` (`PIPESTATUS[0]` under pipefail, PID/argv/disk ownership, fail-closed `ready_one`), `wait_for_storage` ordering (pre-seed and post-reboot, before hash reads), and patches 001/004/005/011/012 against the applied source found **no new confirmed product defect**.

---

## Part 2 — Refutation of primary claims and regrading

| Primary claim | Status after independent read |
|---|---|
| 44 PASS / 5 PARTIAL arithmetic (49 = 5+5+4+4+4+4+4+4+4+3+3+3+2) | Correct. |
| AC-528-01..05 PARTIAL, evidence block | Verdict stands; **evidence citation partially stale** (F-1). Primary should rebind the rclone entry or state explicitly that dispositions predate the 1.75.2 bump. |
| AC-541-01/03 "no silent loss of whole-library preparation / queue behavior … searched queue/watcher consumers" | Default budget true, missing `watched_folders`→`[]`, persisted-pause refusal in both branches, `cached_game_meta` additive — all confirmed in supplied source. But the ctl's upstream-CLI dependencies (F-6) and `wait_for_badges` internals (F-7) were not executed; "pacing retained" is imprecise (F-8). PASS not disproven; coverage narrower than the prose implies. |
| AC-541-02 fresh rehash + installed 1.75.2 | `fetch.json` sums match recipe; version log present. No fresh rehash output is in the packet (only the original 17:02Z fetch). PASS stands. |
| AC-541-04 "final source freshness check exits 0" | Prose-only in the packet (`dependency-refresh/README.md`); no freshness output supplied. PASS rests on cited, unsupplied receipts. |
| AC-543-01..03 | Confirmed: fixed 12/0, negative 12/1 failing exactly the named assertion. Note only the duration half is mutated (F-9 fragility). PASS. |
| AC-544-01..04 | corrected.log 78/0 unclaimed; missing-claim control rc 1; the two replaced hub claims widen y to 640 (157k px) — large but reviewed per review.json. PASS stands; pixel review remains the primary's observation. |
| AC-545-01..04, AC-546-01..04 "actual 19→20 upgrade … two current-boot readiness lines … four save hashes" | Transcript confirms both waits precede seeding/hash reads and all retained checks pass, under `/workspace/tmp/…/runtime`. **Constituent binding gap (F-2)**: the running script is `rehearsal.sh`, not the cited tool. Under the brief's composed-acceptance rule, **AC-546-03 and AC-545-03 should be held PARTIAL pending the binding probe** (not FAIL; the behavior is not in doubt, the source identity is). AC-546-02 PASS on synthetic + transcript evidence. |
| AC-547-01..04 "unchanged upstream test bytes … installed modules" | Runner refuses non-installed paths, checks `/proc/self/maps` and digest, forbids skips; 18/0/0 + 4 CHD cases confirmed. "Unchanged upstream bytes" is asserted, not shown: `tests_sha256 500373b9…` is recorded but no digest of `linux/tests/test_rom_hashing.py` inside the c7ebd1b6e7 tarball is supplied. Evidence is image-19 bound; transfer to image 20 relies on the cited 61309-entry comparison. PASS stands with that caveat. |
| AC-548-01..04 | Script and 13 controls confirmed correct; frames hashed and reviewed by primary. PASS. |
| AC-549-01..03 "original build20 remains 2 … three altered-input refusals" | **Overstated** (F-4): the verifier binds build20b (rc 1), not build20 (rc 2); the "refusals" are JSON mutations, not container controls. PASS not disproven, but AC-549-01's "preserve the original failure" is unbound in the supplied composer. |
| AC-550/551/552 | final-result 1378/0/0, tool hashes = head manifest, final-controls and parser-controls consistent. PASS. |
| Retrospective "Ten completed issues closed from delivered evidence"; issue-tracking "verified closures read back" | **Not supported by the supplied tracker snapshots/head commit message** (F-3). Rows should be amended or the reconciliation supplied. |
| Retrospective "SAFE-AS-TESTED" sibling search | Shapes listed omit `/tmp/rocknix-qemu` literals (F-10) and the ctl's CLI-verb contract (F-6). |
| Research notes "Eighteen-digit unsigned frequencies fit signed 64-bit" | Correct (10¹⁸−1 < 2⁶³). |

No criterion is disproven to FAIL. Recommended regrades: AC-546-03 and AC-545-03 → PARTIAL pending F-2 binding; AC-528 verdicts unchanged with corrected evidence lines; AC-549-01 PASS only once the build20 rc 2 artifact is bound.

---

## Part 3 — Evidence gaps, coverage limits, required probes

**Evidence gaps (packet-level):**
1. `rehearsal.sh` / `prepared-manifest.json` hashes and diff vs `tools/vm-upgrade-rehearsal` (F-2).
2. tracker-reconciliation and `git log -1 --stat b990d32c`; whether the cited qa-log JSON/MD artifacts are committed in the frozen head or working-tree only (F-3).
3. Head-bound dispositions for rclone 1.75.2 (F-1).
4. build20 (rc 2) launcher/inner/outer readback (F-4).
5. `es-lifetime` fresh run: `git -C …/qa-integration rev-parse HEAD` at 20:57Z to bind to 0ee5b28a6/c8dc72cf9.
6. `proxy-fixed`/`proxy-negative` `--source …/final-patched` tree digests vs the supplied applied-proxy hashes (proxy_service.py `42fbdb00…`, rom_browser.py `9b8bbe81…`).
7. Digest of upstream `linux/tests/test_rom_hashing.py` at c7ebd1b6e7 vs `500373b9…`, and the 7z fixture hashes.
8. Freshness tool output (exit 0) for AC-541-04.
9. The 61309-entry image-19↔20 comparison used to carry AC-547 evidence onto 1a02664844.

**Product probes (hypotheses F-5…F-8):** unit ExecStartPost bound and boot.py pre-bind; `_index_missing_game_meta` timing on a large inherited store; presence of `probe-online`/`cached-games-count`/`run-smart-cache` in pinned `main.py`; `image_cache` attributes; narrow the patch 004 "pacing" wording.

**Tool probes:** `grep -rn '/tmp/rocknix-qemu'` across tools/ and the VM launcher (F-10); pin integration-test class set (F-9).

**Observation outside the delta (not a finding):** `clean-standard-report.md:63-65` shows the game-to-game exit-sync stamp as `-` with token `?`; cloud/ES source is unchanged here, but compare with the image-19/18 reports to confirm it is historical rather than new.

**Coverage limits honoured:** no inference about hosted-provider OAuth/award, handheld hardware, physical sensors, or #528 legal clearance; no new punch item raised for the source/licence/vendor/retrieval/off-host-custody gates — only the stale binding of the evidence the primary cites for them.
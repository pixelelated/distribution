# Refutation pass — M7 cadence #603 (Anthropic seat, second serial call)

Basis unchanged from the blind pass: packet text only. Nothing executed, no repository opened, no pixels seen. "Confirmed" below means the behaviour is visible in supplied source or original records; "predicted" means a consequence inferred from confirmed source without a record of its trigger. Line references are packet `file:line`.

---

## Part 1 — Additional findings (new since the blind response)

### G-24 — FEX staging bounds were never measured against the real fetched tree
**Class:** evidence gap (bound adequacy, not enforcement). **Severity:** Low-Medium.
**Location:** `Install Steam.sh:280-286` (RESERVE 256 MiB, MAX_FILE 2 GiB, MAX_TREE 16 GiB, MAX_CONFIG 64 MiB, MAX_ENTRIES 250 000, FETCH_SECONDS 900); `:323-335` (`tree_budget` counts dirs+files, charges 4096 B each, raises on any bound); `:498-501` (full budget walk of `work/data` roughly every second during fetch); `:686` (final walk). The client component has a real-archive measurement with computable headroom (`steam-inspection.json:1634-1637`); nothing analogous exists for the FEX RootFS or the runtime tarball — the AC-44 fresh/refresh successes are synthetic by the primary's own note.
**Trigger:** the real Arch RootFS (download plus `-x` extraction) exceeding 250 000 entries, or fetch+extract exceeding 900 s on a handheld link.
**Consequence:** every fresh install refuses with "FEX staging exceeds the bounded file/space budget" or "FEX fetch/extraction reached its time limit"; the existing environment is preserved (safe), the feature is unusable. Not a defect; an unverified adequacy assumption that AC-44's wording ("bounds … are verified") does not distinguish from enforcement.
**Would be false if:** a retained entry/byte count of the real RootFS and one fetch+extract timing on target or a shaped VM link. **Packet:** absent.

### G-25 — Runtime kill-case retries all exit 1; recovery success is invisible in the exit channel
**Class:** evidence gap (narrows AC-62). **Severity:** Low-Medium.
**Location:** `runtime/tmp/cases/result.json:187-228` — kill-staging/old-renamed/new-renamed/first-link/second-link/committed are all `first_exit -9, retry_exit 1`; `:243-256` recovery-failure and cleanup-failure are also `1/1`. Source `Install Steam.sh:1133-1141` prints "Steam runtime replacement failed" and "Runtime recovery needs attention" differently but returns 1 for both. Contrast Proton (`proton/tmp/cases/result.json:317-343`: kill-download/extracted/activated retry **0**) and Dolphin (`candidate-receipts/result.json:333-346`: kill-state-created/swapped retry **0**), which did demonstrate a successful post-interruption retry.
**Consequence:** because the fixture deliberately fails the retry's download (primary AC-62 note), a `recover()` raise and the intended download failure produce the same exit; the claim "rollback state remains correct" rests on manifest/stderr assertions not in the packet.
**Would be false if:** per-case before/after-recovery dictionaries or stderr captures for the six kill cases are supplied, or one kill case is rerun with a succeeding retry. **Packet:** exits only.

### G-26 — Clean-run Wi-Fi transcript records no exit for the two killed scan-group processes
**Class:** evidence gap (narrows AC-49 "all worker exits"). **Severity:** Low.
**Location:** final-clean `wifi-candidate/result.json:3-18` (blocked group 2510/2511), `:78` `reaped: []`, `:83-84` survivors empty; retained `wifi-candidate/result.json:78-84` records one `-9` reap (pid 2553). Exit request→driver exit: 121.5 ms clean (`:39,:29`), 153.1 ms retained; group stopped 30.7 ms / 42.1 ms after request.
**Consequence:** the leader's status is consumed inside ES (`WifiScanProcess.h:53`) and is unobservable to the fixture by design; the grandchild's exit is recorded in one run and not the other. Either the observer is not a subreaper (then "all worker exits" is not something the fixture can record) or there is a reap race. Not a product defect; the cleanup itself is shown.
**Would be false if:** `guest-wifi-observer.py` (sha f895b41e, named at `vm-result.json:584`) shows subreaper setup and the clean-run grandchild exit appears elsewhere. **Packet:** observer source absent.

### G-27 — The passing frame comparison used a /tmp-composed claims file; repository custody is not shown
**Class:** evidence/process gap. **Severity:** Low-Medium.
**Location:** `execution01/result.json:50-51` (`--claims /tmp/pix-m7-frame-diff-review-20261015/claims.composed.txt`); `tools/frame-diff:43-45` ("the claims file is in git"); `:284-285` (`*` heads are live against every baseline forever). AC-19 binds the composed claims by hash 7764b682 only.
**Consequence:** if the 389 claims were not committed to the path vm-qa passes to `frame-diff compare`, the next retained-baseline run reproduces the 65-unclaimed failure; if they were committed with `*` heads they silently outlive the next baseline move. Neither is a product defect; both bear on whether AC-18's pass is durable rather than a one-off.
**Would be false if:** sha of the vm-qa claims path at cdd92f10 equals 7764b682, plus the head column of those lines. **Packet:** absent.

### G-28 — A pre-existing incomplete Proton directory stops the entire installer chain until hand-deleted
**Class:** documented refusal; missing player route. **Severity:** Low.
**Location:** `Install Steam.sh:2609-2616` (existing target failing `validate` → "kept untouched … Resolve that version separately before retrying"), `:2670` (`die`), `:2749-2752` (GE and first launch unreachable when CachyOS refuses). Receipts `proton/tmp/cases/result.json:41-55` (partial-existing, bad-existing-elf exit 1).
**Trigger:** leftovers from the pre-fork installer (which extracted directly into `compatibilitytools.d`) or an older interrupted run.
**Consequence:** correct under "refuse ambiguous ownership", but the only recovery is manual deletion of `compatibilitytools.d/<name>`; whether es-menu-map or the public guide names that step is not in the packet. With G-04 (GC seed stage) and G-01 (uncommitted client journal) this is the third refusal state with no in-product route.
**Would be false if:** documentation naming the path and action. **Packet:** absent.

### G-29 — Scope expansion in the retrospective's preservation generalisation
**Class:** unsupported generalisation by the primary (not a product finding). **Severity:** Low.
**Location:** retrospective "Steam components … each component preserves unrelated prior state and retires only owned work" and "No new architectural defect survived source/original inspection", versus `Install Steam.sh:2367-2370,2747` (G-02) and `:1470-1474` (G-01). The 67 verdicts do not depend on these sentences; the sentences overreach them.

---

## Part 2 — Refutation of the first reader and revisit of blind findings

The primary reports no Medium-or-higher finding, so there is no finding to re-grade in the usual sense. I challenge its three load-bearing conclusions instead, then revisit each blind item.

### 2a. "No fresh confirmed product defect" — partly disagree

- **G-02 (registry.vdf overwrite) is a confirmed source behaviour, not a hypothesis.** `Install Steam.sh:2369` runs `cp -f /usr/share/steam/registry.vdf "${STEAM_DOT}"` unconditionally at `:2747`, after the client step returned 0 on the "Existing Steam client files were kept" path (`:2292-2294`). It is not reached by any of the 67 literal criteria, so no AC fails; but AC-30's own text ("preserve valid client/channel/aliases/custom files") and the project requirement "preserve existing and unrelated state" make it a defect under the project's invariant unless an ADR declares the file installer-owned. The 18 protected roots in the bridge receipts are not enumerated in the packet, so I cannot tell whether `registry.vdf` was ever seeded with non-template bytes. **Re-grade of the headline:** "no fresh confirmed defect *within the 67 literal criteria*" is supportable; "no new architectural defect survived source inspection" is not.
  *What would make it false:* a protected-roots list containing `${STEAM_DOT}/registry.vdf` with non-template seed bytes and unchanged hash after the complete caller, or an ADR. *Packet:* neither.
- **G-01 is a confirmed mechanism with an unconfirmed trigger.** `mount_rows` (`:1386-1395`) keeps the whole mountinfo row — mount ID, parent ID, major:minor and optional fields such as `shared:N` peer-group IDs, all kernel-assigned per boot — and `journal_schema` (`:1470-1474`) demands byte equality for any uncommitted journal before `tree` mode can succeed (`:1581-1583`, `:2716`). The sibling FEX/runtime transactions use `no_mounts` plus identities and have no such pin. I keep this as predicted, not confirmed: whether `/storage`'s row actually drifts across boots on H700/SM8550 depends on early-mount determinism I cannot see.
- Everything else in my list is an evidence gap or a design risk and I do not promote any of it.

### 2b. PASS verdicts I would narrow or re-grade (none to FAIL)

| AC | Primary | My position | Why / deciding artifact |
|---|---|---|---|
| AC-08 | PASS (amended) | **Agree** | `pkgcheck-current/invocation.json:9,13` exit 0 on recipe 6b07c262 whose `package.mk:6` equals `upstream-fix.patch:18`. Stdout empty, stderr a progress line; tool semantics unknown (G-20) but the mechanical check exists. |
| AC-10 | PASS | **Agree, narrow wording** | "Complete normal build" is evidenced by assembled artifacts (`acceptance.json:21-37`) while `producer_combined_run_returncode: 1` (`:50`); the failure was the producer's own ELF64 assertion (pre-diff `verify-additions.py.diff:7`). PASS should read "image assembled; producer exit 1 preserved". |
| AC-18/19 | PASS | **Narrow** | Comparison and identities are in the packet; durability of the fix (G-27) is not. |
| AC-27/56 | PASS | **Narrow** | Installed proof of the *positive* proxy route is absent: final-clean `dolphin/result.json:146-177` case 02 runs in a private netns (`:169-173`) and its claim is "enabled routing bytes unchanged" (`:177`) — i.e. the no-listener fallback, not the `127.0.0.1:8080` route (G-12). |
| AC-30/31/33 | PASS | **Narrow** | Preservation proven for the enumerated protected roots and the client/runtime/FEX/Proton trees; `registry.vdf` overwrite visible at `:2369` (G-02). |
| AC-37, AC-49, AC-51 ("final installed") | PASS | **Narrow** | The f863 GENERIC_X64 image these run on carries `runtime_qualified: false` and `build_closeout.qualification: false`, `original_launcher_returncode: null`, reason `exclusive-wrapper-receipt-collision` (`final-result.json:4,1093-1108`). Artifact integrity passed. The primary discloses this ("#597 launcher wait remains unknown"); the scorecard label "final installed" should carry the same caveat (G-16). |
| AC-49 | PASS | **Narrow** | G-26 — one run's killed-group exits unrecorded. Independently, the pixel-identical return frame (`vm-result.json:503` = `:785`, sha 1792ba79…, "restored in 57.258 ms" `:592`) is a non-visual witness I *can* confirm for "back during a pending scan does not corrupt the parent screen". |
| AC-59 | PASS | **Narrow to "source-level distinction present; retry termination unverified"** | `generateGameCubeRvzHash` (`rvz_hash.cpp:374-389`) returns false identically for unsupported compression (`:179`), non-GC (`:177`) and read failure; `GameCubeRvzHashRetry` and `FileData::checkCheevosHash` are not supplied (G-11). |
| AC-62 | PASS | **Narrow** | G-25 — exit-channel ambiguity for all six runtime kill cases. |
| AC-32 | PASS | **Agree** | Literal contract met; G-03 is a design fragility (82 %/84 %/72 % of caps used by the one inspected archive against an unpinned "latest" manifest `:1954`), not a defect. |
| AC-25/26 | PASS | **Agree** | Gate logic confirmed at `cheevos_dolphin.sh:139-146`; reachability question deferred to G-05 below. |
| AC-12/13 | PASS | **Agree** | I counted the 40 PPSSPP cases in `runs/03/owner/command.stdout:576-775` (14 shipped profiles + 26 syntax/account cases) against `pixelelated-state-check-test:390-454`; grammar isolation at `pixelelated-state-check:147-148,167`. |
| AC-02/07 | PASS | **Agree** | Diff lines 8-13 and `format-controls-result.json:71-75` ("other bootloader path has no ELF32 exemption" REJECT) confirm exact-identity exemption; `archive-reader/result.json:31-35,94-96` binds the member. |

Verification-depth labels: the scorecard applies "code + original execution/receipt readback" uniformly, including AC-05/09/11/14/15/20/22/23/24/28/29/41-45/55/58/60/63/64/66 whose receipts are not in this packet. I neither contest nor confirm those; that is a packet-selection boundary, not a finding.

### 2c. The historical #196 evidence-sufficiency boundary — disagree with the upgrade mechanics, not the honesty

The primary's AC-53 statement is candid: no new RetroArch replay, the raw manual-launch/stat transcript not located, before/after manager frames plus a dated ledger plus current launcher controls as the inherited boundary. Two objections:

1. By the project's own rule ("verify an artifact rather than a tracker/summary; independently bind source, image, process and frame"), the RetroArch leg of AC-53 lacks the process binding. Frames show tiles at 02:08→02:17 and a persisting 02:16; which RetroArch process produced them, how it exited, and that `.srm`/state bytes came from that exit are ledger claims. That is PARTIAL-grade evidence for one of the four observations the criterion enumerates ("exit auto-state").
2. The cross-check table says prior AC-064 PARTIAL → PASS because "later evidence resolves original gap". The later evidence (native02/03) is Dolphin/Flycast. If the prior PARTIAL named the RetroArch transcript, the upgrade is a re-judgement of unchanged evidence, not a resolution. I cannot see AC-064's text.

**Position:** AC-53 PASS for the Dolphin and Flycast legs (inventories `wii-saved-a`/`wii-loaded-a` keep `.s01` 3732… across a running engine; `dc-global-on-native-off-stopped` keeps 4666… while `dc-auto-saved-stopped` writes 376c… and `dc-auto-cold-restored-c` loads it with flycast live — all in packet). RetroArch exit-auto-state leg: PARTIAL, inherited and evidence-bounded, unless the prior PARTIAL was solely about native states. The project is VM-first and already owns the harness (`run.py` scripts row; vm-visual-qa); one bounded RetroArch run with manager frames and process/stat records would close this cheaply and is the artifact I would ask for rather than another search for the lost transcript.

### 2d. Blind findings revisited

- **G-01** — Re-grade **Medium → Low-Medium (predicted)**. Mechanism confirmed (`:1386-1395, 1470-1474, 1581-1583, 2716`); optional mountinfo fields (`shared:N`) make equality more fragile than I first stated; but `/storage` is an early, fixed mount and drift frequency is unknown. Restored to Medium by a captured mountinfo delta across two boots (with/without SD card) on either device. Packet does not show the trigger. Also note the kill controls (AC-31 cases 10-14) run within one boot and cannot observe it.
- **G-02** — **Keep Medium**; see 2a. Confirmed behaviour; defect classification contingent on Steam's semantics for `registry.vdf` (login/compat-tool state), which is player-owned by Steam's definition.
- **G-03** — **Keep Medium as design/availability risk, explicitly not a defect**; AC-32 PASS stands.
- **G-04** — **Keep Low**; `dolphin-save-paths:224-238` discards only its own unactivated stage and only within the same invocation; `:197-199` documents the refusal; receipts `:325-331,:741-747`. Fail-closed; stage contains shipped resources only.
- **G-05** — **Keep Low, sharpen the deciding question.** `cheevos_dolphin.sh:139` routes only when `hardcore_raw` is the literal `"0"`. GuiMenu writes `global.autosave` as `""` when off (`GuiMenu.cpp:5806`); if the RA settings page writes hardcore the same way, the offline route is unreachable from the UI (blindspot 29 shape). AC-26 covers "empty" → no routing, so the fixture agrees with the source; what it cannot tell me is what ES actually writes. Deciding artifact: the hardcore save line in `GuiRetroAchievementsSettings.cpp`, or a `system.cfg` from the installed VM after toggling hardcore off. Packet: absent.
- **G-06** — **Keep Low**; `verify-additions.py:84` is an annotation, `:106`'s `usr/bin/steam` exemption unexplained. Not product.
- **G-11** — **Keep Medium evidence gap**; see AC-59 row. Predicted boot-time cost (hash library fetched every boot via `ThreadedHasher.cpp:361`, offline toast at `:75-76`) if the retry sentinel is not capped.
- **G-12** — **Keep Low-Medium**; now supported by the final-clean case-02 claim (`dolphin/result.json:177`).
- **G-13** — **Keep Low**; launcher lines after 105 and snippet f365d631's span absent; exit-1 tolerance at `cheevos_dolphin.sh:83,90` inferred only from `dolphin/result.json:20,37`.
- **G-14** — **Keep Low**; `qa20-final-result.json:7` source 1a026648… unbound to cdd92f10.
- **G-15** — **Keep Low**; `run.py:2` label vs executed role; `C['code']` map at `:149` not supplied.
- **G-16** — **Keep Low**; see AC-37/49/51 row. Also `vm-result.json:879` records the retained affected export's own acceptance as "pending coordinator review" at run time — a status, not a contradiction.
- **G-17** — **Keep Low**; `acceptance.json:23` 07:56:04 stamp vs `:51` run id 08:18:27 (22 min) against the H700 analogue of 28 s (`final-result.json:1101,1143`).
- **G-18** — **Keep Low**; component receipts bind installer 9e1ce7b5 (`runtime…:280`, `proton…:4`, `root…:4`); transfer to module 1694f7a9 rests on heredoc hashes I cannot recompute.
- **G-19** — **Keep Low, add:** a rectangle claim owns every changed pixel inside it regardless of foreground/background (`frame-diff:192-206`), so "do frame claims hide foreground changes?" is answered only by rectangle tightness; the 348 rectangles and whether any of the 389 live claims use `*` heads are not in the packet (G-27).
- **G-20** — **Closed for current verification**; historical `root_reported_status` remains unrecovered, as the primary states.
- **G-21/22/23** — **Out of scope, unchanged.** On G-22 I add the cross-system angle the prompt asks about: `:2694-2696` disables x86 binfmt system-wide, `:2709` re-enables, and `:2739` registers `set_kill -9 steam FEX` with the frontend; whether a frontend exit kills the bash script itself (leaving binfmt disabled until reboot) depends on runemu semantics not supplied.
- The native02 vs supplemental `.s01` hashes (3732… vs b946…, `state-inventory.json:5-13`) remain different runs, not a contradiction.

---

## Part 3 — What I could not judge, and what would decide it

| Missing fact | Deciding artifact |
|---|---|
| Whether `/storage` (and any `/var/media/*`) mountinfo rows are byte-stable across reboots on H700 and SM8550 (G-01) | Two captured `/proc/self/mountinfo` rows per device across reboots, one with an SD card inserted; or a VM SIGKILL-during-transfer → reboot → `steam_client_state tree` exit code |
| Whether the bridge's 18 protected roots include `${STEAM_DOT}/registry.vdf` with non-template seed bytes (G-02) | The protected-roots list and before/after hashes from `fixture-records/result.json`; or an ADR declaring the file installer-owned |
| Real FEX RootFS entry count/bytes and fetch+extract duration on target or a shaped link (G-24, G-23) | One retained real-fetch record; a shaped-link VM install at ~10 Mbit/s |
| Runtime kill-case recovery correctness independent of exit 1 (G-25) | Per-case before/after-recovery manifests or stderr for the six kill cases; or one kill case with a succeeding retry |
| Observer subreaper status and the clean-run grandchild exit (G-26) | `guest-wifi-observer.py` (f895b41e) and `guest_helpers.py` (89a1c39a) |
| Repository custody and head column of the 389 composed claims (G-27, G-19) | `git ls-files`/sha at cdd92f10 for the vm-qa claims path; `claims.composed.txt`; `pixel-inventory.json` rows |
| Retry cap and stored failure metadata for unhashable RVZ (G-11) | `GameCubeRvzHashRetry.cpp/.h`, `FileData::checkCheevosHash`, the sentinel value written to `CheevosHash` on failure |
| What ES writes for hardcore-off, and the proxy's real bind address with the service active (G-05, G-12) | Hardcore save line in `GuiRetroAchievementsSettings.cpp`; installed `/proc/net/tcp` showing `0100007F:1F90 … 0A` with `raofflineproxy.service` active; or the proxy bind source |
| Launcher RA-block position and engine exec relative to `prepare` (G-13) | `start_dolphin_gc.sh`/`wii.sh` lines 106-end, or snippet f365d631 with line span |
| Whether runemu's exit path kills the Install Steam module's bash process (G-22; cross-system "installer × frontend") | `runemu.sh` (deb95aee in `final-result.json:198`) stop/kill section and `set_kill` definition in `001-functions` |
| Source and tool ancestry for `qa20-final-result.json` (G-14); `run.py` code map (G-15) | `git merge-base --is-ancestor 1a026648 cdd92f10`; `tools/last-good-scripts-test` sha at cdd92f10; `baseline-correction/config.json` |
| Readiness-record wording for GENERIC_X64 f863 given `qualification: false` (G-16) | The M7 readiness record / #597 entry |
| Stamping source for the SM8550 image timestamp vs producer run id (G-17) | The SM8550 submission/admission record tying 07:56:04 to 07dceee9 |
| Heredoc spans and hashes in installer 9e1ce7b5 vs 1694f7a9 (G-18) | Line spans + sha256 of the three embedded Python blocks in both versions |
| Prior AC-064's PARTIAL text, and a process-bound RetroArch exit-auto-state proof (#196 boundary) | The frozen #596 AC-064 entry; either the #196 raw launch/stat transcript or one bounded new VM RetroArch run with manager frames and process/stat records |
| Player-facing route for the three refusal states (G-01, G-04, G-28) | es-menu-map / public guide entries naming the exact path and action |
| All visual claims (AC-16, 37, 46-48, 50, 53, 54, 65, 66) | Pixels, or the per-frame hash pairs that stand in for them where identity is the claim (as `vm-result.json:503/:785` already does for one pair) |

Nothing above converts a prediction into a confirmed defect. The one confirmed behaviour that the project's own invariant would call a defect (G-02) sits outside the 67 literal criteria and inside the audited module; the primary's 67/67 within literal contracts survives, its two retrospective generalisations do not, and AC-53's RetroArch leg should be stated as inherited PARTIAL rather than PASS until a process-bound run exists.
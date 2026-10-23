# Retrospective — M6.P2 T2, EmulationStation's launch path

**Auditor:** Code Auditor skill, with the renovation face (plan § 4)
**Date:** 2026-10-23
**Subject:** #649, the twenty EmulationStation paths at the pin `16dbac5211`
**Spec:** `docs/reviews/briefs/es-launch-path.md` version 2

---

## Running Notes

Written after Phase 2's entries, from them and from the tree. The prior audits' verdicts (provenance in `01-research-notes.md` § 1.5) were not opened before Phase 2 was written. They are compared in `04-analysis.md` § Finding Verification.

### 3.1 Architectural coherence

The launch path is coherent in its order: the view's transition, then `FileData::launchGame`'s gates, the command, the hooks, the run, and the return. It carries two structural costs.

- **The gates sit after the transition (VC-1).** The question is asked once the screen has said the game is starting. The gates are `FileData`'s, and the transition is `ViewController`'s, which knows nothing of them. That is the seam that misplaced them.
- **`FileData.cpp` is five responsibilities in one unit (Q7).** It holds the node model, the art lookup, the command builder, the gates and their deferred launch, and the return path (capture, rotation, play time, exit sync). Of its 2,680 lines about a fifth are the fork's, and all the fork's are in the last three. `launchGame` alone is 400 lines (`:928-1328`). A reader meets the gates' 60-line rationale comment (`:941-989`) before the first gate.

No orphaned file. Five unreached functions (Q6) are upstream API kept for the merge, plus `renumberSlots`, which is retired.

### 3.2 Project conformance

**Instruction files** (read this session; equal to `next`'s except P1's two files, the council's `IMPORTED-FROM.md` and this lane's own `es-native-ui.md` sentence):

| Rule | Relevance | Finding |
| --- | --- | --- |
| `es-player-text.md` § Conventions, § Outcome vocabulary, § Every fork string in English and French | ✓ | ⚠ FD-10 (`UKNOWN ERROR`), MN-5 (three boxes outside `_()`), MN-6 (`DOWNLOAD ... GAMES`). The four gate questions follow D-CLOUD-130/D-UI-096 (statement, consequence, two verbs, safe last). The proxy cards follow D-UI-107. |
| `es-ui-style-guide.md` § Confirmations, § Glyphs | ✓ | ⚠ FD-12 (two spaces before a toast's glyph). The gate boxes have no `NO`/`OK` button, so the back button falls to the last one, `KEEP WAITING`, which is safe. |
| `es-native-ui.md` § Core patterns (`exists(path, false)`), § Spacing's tiers, D-UI-093/095 | ✓ | ✓ The stamps and markers are read uncached (`ProxyCards.cpp:97`, `main.cpp:960`, `:1051`, `SaveStateRepository.cpp:144`). FD-11's `/tmp/launch_error.log` is fresh by order (cache reset at `FileData.cpp:1113`), not by the rule; recorded. One floating surface at a time (`ProxyCards.cpp:499-513`). |
| `es-code-traps.md` § A rescan that deletes FileData drops the view first | ✓ | ✓ for the view and collections (SD-1); ⚠ FD-8 for a deferred launch's pointer (latent). |
| `es-code-traps.md` § Comments near a translatable string must be ASCII | ✓ | Not re-checked by `grep -nP '^\s*//.*[^\x00-\x7F]'` yet; owed before any ES commit (stage E). |
| `time-to-play.md` | ✓ | ⚠ VC-1, SR-2 to measure. **Doctrine drift (lead for the doctrine slice):** the rule says "what ships today still cancels an automatic sync at launch (D-CLOUD-076) ... D-CLOUD-109 replaces that". The code ships D-CLOUD-130: every sync a launch would interrupt asks STOP IT AND PLAY / KEEP WAITING, nothing is cancelled until the answer (`FileData.cpp:993-1008`, `:947-950`). |
| `least-surprise.md` | ✓ | ⚠ VC-1 (the screen says starting, then asks); FD-1 (a spectator joins as a player). |
| `upgrade-and-install.md` | ✓ | ⚠ SD-4 (a stored sort id from another build), MN-3 (a stored boot command), SS-2 (a `.bak` left by the fallback). Each finding's fix carries its `Already written:` line in the punch list. |
| `engineering-practices.md` § Guards must fail closed, § Fail gracefully, § A name is not a behaviour | ✓ | ⚠ SB-2 (fails closed, silently); FD-4 (`get...` writes `system.cfg`); SS-4 (a copy that reports success unchecked). |
| `decision-register.md` § A reversal sweeps its old words | ✓ | ⚠ MN-4 (three comments describe superseded behaviour). |
| `vm-first.md`, `bugs-are-agent-first.md` | ✓ | Every runtime claim is held as a lead until the guest proof runs (queued). Each defect's bug issue gets its VM line at stage D. |

**Blindspot register** (the entries brief § 3 names):

| Entry | Does this work repeat it? |
| --- | --- |
| 7 host tools are not the device's | Not repeated: no device verdict was made from a host tool. `git apply --check` is a host operation on host data (Q4). |
| 13 assumed done | Not repeated: no criterion was ticked from an artifact's existence. AC-07/10/11 cite commands. |
| 30 a resumed session built on its own summary | Guarded: every finding cites `file:line` read this session. Phase 4.5 re-reads each. |
| 35 a remedy built on an audit's claim about a default | Avoided: `CheckBiosesAtLaunch`'s default was read (`Settings.cpp:207`, false) before VC/308221458's Q5 claim was graded. |
| 44 proven at a fixture's size | **Applies to SR-2**: the exit's state refresh must be measured at hundreds of states, not a handful. The queued proof says N = 500. |
| 46 a name read as a behaviour | **Found in the code**: FD-4 (`getlaunchCommand` persists `system.cfg`). Avoided in this audit: FD-1 was corrected by the caller search, not by the field's name. |
| 49 an edit made blind to the compiler | No ES edit yet. #699's fix restores the tool that guards it (stage A). |
| 51 a checklist built from open boxes | Applies at stage D: each punch item is written from the reading, not from a prior audit's box. |
| 54, 63 a measurement on a guest whose renderer was not the device's | Applies to Q5: `time-to-play --vm` sets gl, and the renderer is read and recorded beside the numbers. |
| 59 a memory measurement on a page that never loaded | Applies to `es-launch-memory`: the frame of the loaded game is checked, not only the process. |
| 64 a wait lengthened for an event the code cannot produce | Read: `launchWhenGone`'s 20 s, `captureGate`'s 10 s, the proxy's 45/10/90/120 s each wait for an event their callers produce. No repeat found. |
| 65 a proof's substitute | Applies to the queued proofs: a fixture ROM with `$` in its name (SS-1) and a fixture `.m3u` (FD-14) are named substitutes. Each checkbox stays partial until the real input is seen. |
| 73 a monitor of completion, not activity | Applies to the queued tool runs (watched by their own output). |

**Project invariants:**
- Progress over recency: the `racommands` fallback's `.bak` dance can restore an older auto state over a newer one after a killed session (SS-2), on the fallback path only.
- No secrets in what is written: `global.bootgame.cmd` stores a launch command in `system.cfg`, including a netplay nick but no password (`netplayClientPassword` is never set, FD-1). The launch log goes through `maskSecrets` (`FileData.cpp:1090`).
- The allowlist invariant: not this slice's.
- Every change lands on a device with state: SD-4, MN-3, SS-2 above.

### 3.3 Spec fidelity

The code agrees with the decisions brief § 3 names, with three exceptions:

- **D-CLOUD-130 ships, not D-CLOUD-109's bounded wait.** `time-to-play.md` says otherwise (above). The code is right, and the rule's paragraph is stale.
- **D-UI-069** (no renumbering) holds in `SaveState::onGameEnded`. `FileData.cpp:1134` says the opposite (FD-13), and `renumberSlots` survives unreached (SR-1).
- **D-UI-031** reworded `SKIPPED - NO NETWORK CONNECTION`, and `main.cpp:595` keeps the old words (MN-4).

### 3.4 Platform architecture conformance

| Check | Relevance | Finding |
| --- | --- | --- |
| Reference Implementation | · | not this repository's model |
| Schema-Before-Code | · | not applicable |
| Dogfooding Gate | · | not applicable |
| API-First | · | the HTTP API's `POST /launch` reaches `ViewController::launch` (FD-8's context) |

### 3.5 Cross-system interaction audit

### Interaction: the command × `runemu.sh`'s parsing (T1, #648, #730)
**State shared:** the argument line: `-P<system>`, `--core=`, `--emulator=`, `--controllers="..."`, `-state_slot N -state_file "<file>"`, and the netplay words.
**Wipe risk:** a word in one reading that the other reads differently: a nick such as `'Bob -Pro'` (LaunchCommand.h's header), a state file path holding `--core=` (#730), a ROM name with `"`/`$` inside `-state_file "..."` (SS-1).
**Test coverage:** PARTIAL. `LaunchCommandTests.cpp` covers this side with a `runemu` stand-in; T1's #730 holds the launcher's side.
**Finding:** risky at SS-1 (this side), with #730 on the other side. The two halves are one fix series across lanes, which is the coordinator's to sequence.

### Interaction: the gates × the sync, the transfer and the proxy (T18, T20)
**State shared:** `ThreadedCloudSync::isRunning`, `CloudTransferJob::current`, `ProxyCards::sendRunning/topUpRunning`, and the capture generation.
**Wipe risk:** a gate answered while its job ends. The answer lambdas re-check (`cancelForLaunch(...) || !isRunning()`, `FileData.cpp:1001`).
**Test coverage:** PARTIAL. `tests/launch-capture-gate.py` and `tests/launch-deferred-state.py` (queued) compile `captureGate` and `launchNow`. The question boxes need a running sync on the guest, which is a lead for the integration run (brief § 5: the shared QA backend is not this lane's).
**Finding:** safe in logic. VC-1 is the placement cost.

### Interaction: `rescanIfFolderChanged` × the deferred launches
**State shared:** `FileData*` of the system's files.
**Wipe risk:** the merge's `vanished` deletes a file a pending launch holds (FD-8). No current trigger lands in a wait; the API's reload does.
**Test coverage:** UNTESTED (the guest proof is queued).
**Finding:** risky, latent.

### Interaction: the exit path × `cloud_capture` and the exit sync (T16, T18)
**State shared:** `sCaptureInFlight`, `sExitGeneration` and `sCaptureWaitedOn`; the capture manifest; the sync lock.
**Wipe risk:** a launch on the next frame under a running capture, which `captureGate` prevents. A second exit's capture: the generation check (`FileData.cpp:1281`, `:1295`).
**Test coverage:** PARTIAL (`launch-capture-gate.py`, queued).
**Finding:** safe.

### Interaction: the boot game × the startup sync (MN-3)
**State shared:** the saves the boot game writes; the capture.
**Wipe risk:** the boot game runs before the window and before the startup sync. The sync's `copy --update` then carries what it wrote; the capture records it (`main.cpp:551-570`).
**Test coverage:** UNTESTED.
**Finding:** safe for the saves. The stored command's staleness is MN-3.

### 3.6 What's missing?

Searches:
- `git -C $W grep -n -E 'formatCommandLineArgument|getContentFiles|deleteGameFiles|launchToken' $PIN -- es-app/tests` finds `launchToken` (LaunchCommandTests) and none of the other three. **No unit case** covers `formatCommandLineArgument` (FD-2) or `getContentFiles`/`deleteGameFiles` (FD-14). Both are pure enough to test (es-code-traps § Pure text has a home).
- `ls $W/es-app/tests/unit/` (queued with the unit build) was not read further here. The punch list's test-first items name the files.
- No flow or frame evidence is owed yet: no player-visible change has been made.
- `git -C $W log --oneline -5 $PIN -- es-app/tests` (proximate work) is run at stage E with the stream briefs.

### 3.6.5 Audit-prescription verification: the shapes, every site

Searches: `git -C $W grep -n -E <shape> $PIN -- es-app/src es-core/src` per row (`00-running-log.md` 17:5x).

| Shape | Site | Sibling (this slice) | Adjacent (another slice) | Verdict |
| --- | --- | --- | --- | --- |
| a path or name double-quoted into a shell line, unescaped (SS-1) | `SaveState.cpp:97` | `:77`, `:111` | `ApiSystem.cpp:1527`, `:1659` (7z on a ROM path, reached from `FileData::checkMd5`/the hasher), `:838`, `:2591-2593`, `:3502` (T21); `GuiMenu.cpp:1842` (`rocknix-keyboard`, the GuiMenu slice) | FIX-NOW in the slice; FILE-FOLLOWUP as leads for T21 and the GuiMenu slice |
| quoted only when it holds a space (FD-2, FD-9) | `FileData.cpp:530` | none | `Scripting.cpp:92`, `:109` (T33/T21); `ApiSystem.cpp:2076`, `:3471` (T21) | FIX-NOW (the site); leads for the others |
| a path filter by substring (SD-2) | `SystemData.cpp:627` | `:631` | none found | FIX-NOW |
| `> size()` before `.at()` (FD-15) | `FileData.cpp:1659` | none | `GuiGamelistOptions.cpp:148` (the game-list options slice) | FIX-NOW; lead |
| a list's entries deleted with no containment (FD-14) | `FileData.cpp:1505-1506` | `:1487-1495` (every `MD_PATH` metadata file removed, wherever it points, including art a second game's entry names) | none found | FIX-NOW |
| superseded words in a comment (MN-4) | `main.cpp:617` | `:595`, `:1110-1114` | `GuiMenu.cpp:6665`, `:8167` are current player strings (`NO NETWORK CONNECTION DETECTED ...`) on another surface, the GuiMenu slice's to judge against D-UI-031 | FIX-NOW (comments); lead |
| a player string outside `_()` (MN-5) | `main.cpp:929` | `:328-329`, `:336-339` | `GuiMenu.cpp:11714`, `:11727`, `:11738` (eject drive), `SystemView.cpp:234` (upstream) | FIX-NOW for the fork string; D-UI-079 for the upstream ones; leads |
| an unknown argument ignored silently (MN-1) | `main.cpp` `parseArgs` | `:98-106`, `:220-229` (MN-2, unbounded `argv[i+1]`) | none | FIX-NOW or BY-DESIGN, the stream brief's call |
| a plain static read across threads (FD-18) | `FileData.h:217` | `ViewController.cpp:39` `sConfigurationReplaced` (interface thread only: SAFE-AS-TESTED by reading) | `SaveStateConfigFile.cpp:271` `_cache` (interface thread only today, SC-1) | FIX-NOW (FD-18); recorded |

### 3.7 Retrospective Summary

#### Architectural Assessment
The order is right except for the gates' placement (VC-1). `FileData.cpp` carries five responsibilities, and the fork's part of it is the launch.

#### Cornerstone Alignment
The ES rules are met with the exceptions above. The doctrine has one stale paragraph (`time-to-play.md`, D-CLOUD-130).

#### Cross-System Interactions
The command × `runemu.sh` is the riskiest seam (SS-1 with #730). The rescan × deferred launches is latent (FD-8).

#### Spec Drift
Three comments and one rule describe superseded behaviour (MN-4, FD-13, `time-to-play.md`).

#### Missing Artifacts
Unit cases for `formatCommandLineArgument` and for `getContentFiles`/`deleteGameFiles`.

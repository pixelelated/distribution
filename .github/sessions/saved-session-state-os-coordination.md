# Saved session state for OS work coordination

## Start here

Saved 2026-11-25T06:27Z on `feature/conflict-resolution` in the pixelelated distribution repository. Resume this file for the **OS work coordinator**, the sole dispatcher for M7. Since November 24 that role runs in **Claude Code on the latest Opus** (`claude-opus-5-5`) in Herdr pane `w4:p2`; session `b19c3b8c-1c4f-4a57-8765-0b8fe1f11ae9` (D-WORKFLOW-200). The one-on-one steward runs Claude Code on the latest Fable in `w4:pF` (session `2032b6b6-3946-42d0-ab2c-cfb5469deeea`); worker lanes run Codex on `gpt-6.2-sol`. The daily operations worktree is `/workspace/repos/rocknix.worktrees/conflict-resolution`; the primary checkout `/workspace/repos/rocknix` carries local `next`. pixelelated builds an immutable Linux gaming OS. This worktree's rules lag `next`: read them with `git show next:<path>` (`AGENTS.md`, `.claude/rules/worktrees.md`, `.claude/rules/device-builds.md`, `.claude/skills/build-cleanup/SKILL.md`).

Read the [M7 milestone](https://github.com/pixelelated/distribution/milestone/7) (body updated 12:29Z), [#555](https://github.com/pixelelated/distribution/issues/555) (build qualification; 12:30Z comment), [#1441](https://github.com/pixelelated/distribution/issues/1441) (the H700 recipe failure) and [#1442](https://github.com/pixelelated/distribution/issues/1442) (the two-ABI admission refusal). Decisions made this session, all on local `next`: D-INFRA-035 to D-INFRA-043 and D-WORKFLOW-200. Also read [#1448](https://github.com/pixelelated/distribution/issues/1448) (the SM8550 fex-emu stop).

## Current focus

**000000000000000000000000000000. Newest (2026-11-28T00:25Z): the handheld builds are held for Max's #1477 answer (this release or next).**
- **Max** (00:20 UTC, a proposal): a forced wait, "Please wait, saves are syncing", with a time limit, in place of STOP IT AND PLAY / KEEP WAITING over a saves sync. His words and the outline are on #1477; the proposed limit is 15 s; the steward is asking him this release or next.
- **The carry-on chain (pid 2444801) was stopped at 00:23 UTC by its PID,** before it launched H700. `b24-carry/STOPPED` says why.
- **Standard run 18 is still running:** chain pid 2370499, waiter `batz8c478`. Read it and run `rc-preflight --only vm-qa` by hand.
- **On "next release":** launch H700 and then SM8550 from `428f4661b1` (`b24-carry.sh`'s commands, or a fresh carry-on chain from the H700 step).
- **On "this release":** the ES change in the saves-sync branch of `FileData::launchGame`, route 15, a warm PC build, the proofs, then the handhelds.

**00000000000000000000000000000. Newest (2026-11-28T00:12Z): Max's lessons are codified; the carry-on chain is waiting on run 18.**
- **Max's four messages** (2026-11-27, relayed 00:06 UTC) are filed: #1505 (siblings at filing, D-QA-069), #1506 (a failed check says why, D-QA-070), #1507 (chains carry the next routine step, D-WORKFLOW-254), #1508 (friction in every lane, D-WORKFLOW-253). The rules are in `bugs-are-agent-first.md`, `release-candidates.md`, `generic-x64-vm-testing.md`, `engineering-practices.md` and `ceremonies.md`.
- **The friction log:** the steward's six lines carry their issues. `tools/issue-file` reads only a body's first line now (a false positive on #1505's body).
- **Running:**
  - standard run 18, chain pid 2370499 (`b24-chain/`), waiter `batz8c478`;
  - **carry-on chain pid 2444801** (`b24-carry.sh`, step files in `b24-carry/`, `STOPPED` on a failure): run 18 PASS, then `rc-preflight --only vm-qa`, then H700 (cold, `--name m7-round-h700-20261128`), its reads, then SM8550 and its reads.
  - Acceptance (ACCEPTANCE json and admission consume) and the records stay with OS.
- **Owed:** #1506's and #1508's tooling in a later round; the inbox note on what was filed.

**0000000000000000000000000000. Newest (2026-11-28T00:05Z): #1501, #1502 and #1464 are closed. Round head `428f4661b1` (route 14 plus #1503's test change). Build 24 is accepted; standard run 18 is running.**
- **Build 23** (`5bd8ad6dc0`): `ra-refusal-outcomes` EN and FR PASSED, six of six. The top-up stamped SIGN_IN_REFUSED.
  - **Standard run 17: 15 of 16.** `lifecycle`'s last #1467 check failed once (submit rc 0) without naming its condition. Three direct runs passed. Filed as **#1503**. The check now names each condition and dumps state and journal on a FAIL (round `428f4661b1`; constructed failure shown; packet `docs/qa-logs/2026-11-27-1503-lifecycle/`).
  - **The top-up card's refused line cannot be framed:** a refused run with no work draws no card (`ProxyCards.cpp:320`). The harness for it is **#1504**. #1501's c3 is reworded to the unit case and the code.
- **`tools/issue-file`** (`bbe1bb8ee8`) files with `{{NOW}}` from the clock. It was the third typed found-time; #1464 was reopened, met (#1504 was filed through the tool) and closed.
- **Build 24** (`428f4661b1`): run `20261128T000014Z-27912c2f`, rc 0. The ES binary and ctl are byte-identical to build 23's. ACCEPTANCE-24 written; admission `7b1c9555…` consumed; records in `build24/`.
- **Running:** standard run 18, chain pid 2370499 (`b24-chain.sh`, rc in `b24-chain/`); waiter `batz8c478`.
- **Next:**
  1. Run 18 → #1465 c3, #1503 c2, and `rc-preflight --only vm-qa`.
  2. Then H700 cold from `428f4661b1` (set `m7-round-x64`), then SM8550 cold, unless #1477's answer moves ES.
  3. The two proposed strings (#1501) are for Max to see in the build.

**000000000000000000000000000. Newest (2026-11-27T18:17Z): #1497, #1498 and #1500 are closed on build 22. #1501 and #1502 are found and fixed in route 14 (round `5bd8ad6dc0`). Build 23 (PC, warm) is running.**
- **Build 22's proofs** (12:41 to 13:52Z; read at 17:41Z after a usage limit):
  - the pre-split `suite-1428` passed whole (#1498 c3);
  - standard run 16 passed 16 of 16, `frame-diff` 426 claimed and 0 unclaimed (#1500 c2), with the new walk's frame (#1497 c4);
  - `rc-preflight --only vm-qa` PASS.
  - The three issues are closed with their evidence; #1497 has a full trace. #1465 has run 16; its c3 waits for the final head.
- **#1501** (hunted from #1497): the offline achievements scan page offers TRY AGAIN for a refused sign-in, and the top-up card promises a retry.
- **#1502** (found framing #1501 on build 22, loopback stand-in at 401): the ctl tells a rejected token as RETROACHIEVEMENTS STOPPED ANSWERING, because the proxy's "rejected the login" is not in its matcher, and the top-up's recently played pass calls every failure the link's.
  - Packet: `docs/qa-logs/2026-11-27-1501-ra-refusal/`. #1470's table has the row.
- **Route 14:**
  - ES `57a2357d3` (`CloudText::scanFix`, 196 of 196 unit tests, es-syntax-check PASS; two proposed strings with French), `m7-20261127-9384b9c64e0a`, supplier `.build-runs/m7-rc-round-20261127-14-es/inputs/es`;
  - the ctl fix;
  - `tools/vm-walks/ra-refusal-outcomes` (it FAILED on build 22 at token-401, as it should).
  - The menu map is updated for #1497 and #1501; the missed #1497 map update is a friction line.
- **Running:** build 23, run `20261127T181632Z-9eb10240` (build.pid 81503, watcher 81504), owner `.build-runs/m7-round-x64-23-owner/submit-01`; harness waiter `brpcvd3dd` on `build.rc`.
- **Next:**
  1. Build 23's acceptance and image reads: the ES binary carries the two new strings, and the image's ctl has the "rejected the login" match.
  2. `ra-refusal-outcomes` EN and FR on build 23 (#1501 c2–c5, #1502 c2–c4).
  3. Standard run 17 for #1465 c3.
  4. Then H700 cold and SM8550 cold from `5bd8ad6dc0`, unless #1477's answer moves ES again.

**00000000000000000000000000. Newest (2026-11-27T07:56Z): route 12 is round `2479f6f2e8`. Build 21 (PC, warm) is accepted, and #1497 is fixed on its image. #1496 and #1495 are closed. Build 21's proof chain is running.**
- **Run 14 on build 20:** PASS, 16 of 16; `rc-preflight --only vm-qa` PASS (#1465).
- **s36 on build 20** found #1497 on the folder scan (CHECKING YOUR CLOUD): it offered CLOUD FOLDERS and clipped the why. ES `480efb93d1` fixes it. #1497 is rewritten; c1–c3 are ticked from build 21's s36 and s37. **c4 is open:** walks for the card (s34) and scan (s36) states join a standard suite with reference frames. That is a round `tools/vm-walks` change, made after the chain.
- **Route 12** (`m7-20261126-1004de647320`) contains:
  - ES `480efb93d1`;
  - `suite-1428` split into the main file plus four failure-branch files (#1498);
  - the round's register = next's, with 17 live citations swept (#1463 c2 ticked; c3, the guard, open).
- **Build 21:** run `20261127T073955Z-4dd7f52c`, rc 0, image `…g2479f6f2e8ac-from-ROCKNIX`, no `.dirty`; ACCEPTANCE-21 written and its admission (`4f4d23b9…`) consumed; records in `build21/`.
- **#1496 is closed:** dry-run proofs; build 21 is clean; `rc-preflight` refuses a dirty identity (constructed control).
- **Running:**
  - chain pid 778734 (`b21-chain.sh`, rc files in `b21-chain/`): phase D done (rc 0); then `suite-1428`, the four branch files, then standard run 15;
  - waiter `bzyymtb6b` on the branch files.
- **D-QA-068** (Max, 05:48Z relay): every VM finding updates its card's criteria. #1470 has a findings table, and #1499 is filed.
- **Next:**
  1. The suites' verdicts (#1498 c1 and c2).
  2. Run 15: `rc-preflight`, then #1465.
  3. #1497 c4, in the round after the chain.
  4. H700 cold from `2479f6f2e8` (set `m7-round-x64`), then SM8550, unless #1477's answer moves the head first.

**0000000000000000000000000. Newest (2026-11-27T04:56Z): build 20 (PC, cold, `1d3c0c735e`) is accepted; phase D on it passed; #1495 is closed; #1497 is filed and fixed on the ES branch but not routed. The proof chain runs: walks, then standard run 14.**
- **Build 20:** run `20261127T012429Z-dad9fcb9`, 01:24 to 04:30Z, rc 0; ACCEPTANCE-20 written and the admission consumed (`2e93b61a…`); records in `docs/qa-logs/2026-11-26-1445-device-build/build20/`.
  - Its version reads `.dirty`. The cause was an untracked `kept/` that `tools/device-build` wrote into the build worktree (#1496). The tool is fixed on next (`a41d72357c`): the keep goes under `.build-runs/kept/`, and step 2 refuses an unclean worktree. Build 19's leftover is removed.
  - Build 20 serves the VM proofs, not publication.
  - Still owed for #1496: a dry-run proof. Step 0 refuses even a dry run while guests are up.
- **Phase D on build 20** (`416aabe9d2`): s34 shows #1495's card naming where to act, in EN and FR. s31, s13 and s35 hold, and French settings rows read PARAMÈTRES. #1495 is closed with its trace.
- **#1497** (filed 04:46Z): the transfer page offers TRY AGAIN for a refusal only the player can fix. The fix is ES `4a93c079d3` (`CloudText::playerFix`, 195 of 195 unit tests, es-syntax-check PASS), **unrouted**.
- **Running:**
  - chain pid 3157684 (`/workspace/tmp/rocknix-session/b20-chain.sh`, rc files in `b20-chain/`): phase D (done, rc 0), walks-640, walks-1280, standard-14;
  - s36 runner pid 3350581 (`b20-s36.sh`, output in `b20-s36/`): waits for `chain.rc`, then runs phase D s36 on build 20 for #1497 c1, writing `phase-d/build20-640x480-s36`;
  - patch replay pid 3175280 (`patch-replay-round-1d3c0c735e/`), for SM8550 and H700, both ABIs, at nice 19;
  - a read-only agent classifying D-WORKFLOW-175..182's citations into `/workspace/tmp/rocknix-session/1463-c2-classification.md`.
- **#1463:** criterion 1 is 29 of 39 (D-INFRA-048, with the rekey recorded as D-INFRA-049; `5da31ec397`).
- **Traces posted:** #1448, #1459, and #1422's headphone half.
- **Next:**
  1. Read the walks' frames for #1478 criterion 2 at both sizes.
  2. Standard run 14, then `rc-preflight --only vm-qa`, then a note on #1465.
  3. The s36 frames for #1497 c1.
  4. The `device-build --dry-run` proof for #1496.
  5. **Route 12:** ES `4a93c079d3` (#1497), plus #1477's change if Max has answered. Then a warm PC build 21, s36's after-frames and standard run 15.
  6. H700, then SM8550, cold from route 12's head (D-INFRA-043). The handhelds wait for route 12, because #1497 is an M7 bug that moves the head.

**000000000000000000000000. Newest (2026-11-27T01:25Z): #1478 item 2 answered (PARAMÈTRES, D-UI-147). The H700 build of `fd8dadd564` was stopped on purpose. The PC image is building cold from route 11's head `1d3c0c735e`.**
- **Max's word** (via the steward, 01:16Z): "We're just using French for testing. Let's just see what the most common word is online. I really don't know."
  - The steward's search gave Paramètres.
  - ES `0b5e210c5` changes 25 fork French "settings" entries. Upstream's two and the two "setup" lines keep RÉGLAGES.
  - Recorded on #1478 and D-UI-147 (next `e5d2d896f4`, and in the round's register).
- **Route 11** (`m7-20261126-3edb5648453f`, ES `0b5e210c5`, which carries #1495's `a8107f028`) is round `1d3c0c735e`, the set's head.
- **H700 of `fd8dadd564` stopped at 01:21Z:** TERM to runner pid 3775796; rc 143; container `d2d283ac2934` gone; its roots removed by the next launch. Every target is now built from `1d3c0c735e`, handhelds last (D-INFRA-043).
- **Running:** cold GENERIC_X64 build `m7-round-x64-20`.
  - Run `20261127T012429Z-dad9fcb9`: build pid 2402467, command pid 2402566, watcher pid 2402468.
  - Owner `.build-runs/m7-round-x64-20-owner`; the waiter delivers `build.rc`.
- **When it ends:**
  1. image reads and ACCEPTANCE-20;
  2. phase D: s34 (#1495's card, EN/FR), s31, s13 and s35, plus the French pages;
  3. `tools/vm-walks/suite-1428.txt` at 640x480 and 1280x800, EN and FR, for #1478 criterion 2 and #1111 C24's French half;
  4. standard run 14;
  5. H700, then SM8550, each from `1d3c0c735e`.

**00000000000000000000000. Newest (2026-11-27T00:38Z): standard run 13 on build 19 passed 15 of 16 suites. The register fault is fixed in round `fd8dadd564`. H700 cold is building from `fd8dadd564`.**
- **Run 13:** report `/workspace/artifacts/rocknix-images/qa-a267c139b1-webdav-a-20261127-0000/report.md`.
  - The one failure was register: `MISSING D-CLOUD-194`, because the round's register copy predated the row.
  - Fixed by copying the row verbatim (`fd8dadd564`); `tools/register-check` on the round passes.
  - Recorded on #1465. The guests are down, and the run's guest disks in /tmp are removed.
- **H700:**
  - owner `.build-runs/m7-round-h700-fd8dadd5-owner`;
  - worktree `/workspace/repos/rocknix.worktrees/m7-round-h700-fd8dadd5`;
  - run `20261127T003711Z-eb7dd594`, build pid 3775796, command pid 3776113, watcher pid 3775797;
  - started 00:37Z, and the waiter delivers `build.rc`;
  - the x64 root is removed (+120.6 GiB), its ES binary kept under `m7-round-x64-20261125/kept/`.
- **When H700 ends:**
  - read every result channel; check the DDR3, DDR4 and update tar hashes; image reads (os-release BUILD_ID `fd8dadd564…`, the ES strings, the French catalog);
  - write ACCEPTANCE and consume the admission;
  - then SM8550 cold from the same head (`--device SM8550 --commit fd8dadd564 --set m7-round-x64 --name m7-round-sm8550-fd8dadd5`, ES supplier route 10).
- **SM8550's acceptance reads, beyond the usual:**
  - no `usr/share/aethersx2-sa/aethersx2` in `SYSTEM` (#1459 checkbox 2; then its trace and close);
  - the installed UCM file carrying ROCKNIX #3481's Nova headphone Class-AB quirk (#1422; its listening stays an open item to test, Max's disposition);
  - `fex-emu` unpacked and built (#1448's history).
- **Also done in this stretch:**
  - #1463 criterion 1: 28 of 39 rows landed on next (`38cbebf9a5`). D-WORKFLOW-175 to 182 carry two decisions each; their citation count, done in context, is next (the keyword pass was too weak).
  - The audit's scope, depth and cost plan is on #555, and the steward has the cost question for Max (inbox 00:39Z).
- **Pending into the next head:**
  - #1495's ES commit `a8107f028` (not in route 10);
  - Max's #1478 word.

  When they land: a new route, then all three images rebuilt cold from the final head, last (D-INFRA-043), and the standard run on the PC image.

**0000000000000000000000. Newest (2026-11-27T00:01Z): #1492, #1493 and #1494 closed; build 19 (`a267c139b1`) is the round's head and PC image; standard run 13 on it is running; H700 cold follows.**
- **Builds:**
  - 18: `4753d00e8e`, route 09, ES `4ef2a8dac`.
  - 19: `a267c139b1`, route 10, ES `77d7b2681` (#1494's French label). Accepted, owner `.build-runs/m7-round-x64-19-owner`.
- **Phase D:**
  - s32: the reboot's startup sync in #1489's state.
  - s33: an unreachable connection on the setup check.
  - s34: a 40-frame card burst over an ES restart; duplicates removed after hashing.
  - s35: both syncs on.

  Records are on next at `4461f6361c` and `95bf0ae6e5`.
- **Filed, open:** #1495, a refused sync's card names the cause but not where to fix it; it also applies to CHECK YOUR SIGN-IN, which `shortenWhy` cuts. A design task for daylight.
- **Running:** standard run 13, `tools/vm-qa` on build 19.
  - Directory: `/workspace/tmp/rocknix-session/vmqa-standard-13-20261126T2359Z/` (vm-qa pid 3371285).
  - The waiter delivers its rc.
  - When it ends: `tools/vm-pair down`; `tools/rc-preflight --only vm-qa --build-set /workspace/repos/rocknix.worktrees/m7-round-x64-20261125/target`; a note on #1465.
- **Then H700 cold:** `tools/device-build --device H700 --commit a267c139b1 --set m7-round-x64 --name m7-round-h700-19 --es-supplier /workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/m7-rc-round-20261126-10-es/inputs/es`.
  - Its one-build step removes the x64 root, as D-INFRA-033/036/040 intend.
  - SM8550 after it.
  - When Max answers #1478, the head moves and all three are rebuilt cold from the final head, last (D-INFRA-043).
- **Steward told** at 00:01Z (inbox). The M7 milestone body was updated at 23:26Z: the 0a3e979e50 handheld images are superseded, and the next steps are listed.

**000000000000000000000. Newest (2026-11-26T23:22Z): #1489 and #1490 closed on build 16; #1492 and #1493 filed and fixed; build 17 accepted; build 18 (`4753d00e8e`) running; H700 waits for its proof.**
- **D-CLOUD-194 is decided** (Max: today's behaviour for 0.0.1; #1491 holds the next-release proof). His last clause is the word to keep going toward the handheld build. It is not a yes to any copy, reboot or other action on a handheld or in its cloud.
- **Build 16** (`fc3e489f8a`, route 07): accepted. Phase D s31/s30/s24 plus a rerun (`-r2/`, the store dumped, s20) closed #1489 and #1490 with code traces (next `3445abddf5`).
- **#1492** (#1489's sibling): a transfer refused in that state said CHOOSE A CONNECTION. Fixed in round `a09786c37c` (`selection_reason`; host suite 54/54).
  - Found with it: the card's why table never matched a sentence ending in a full stop. Fixed in ES `992d36e98` (unit 193/193).
- **#1493:** three rows at three lines at 640x480. Proposed words in ES `4ef2a8dac`; the unreachable line reuses the dialog's sentence.
- **Build 17** (`7c2d063194`, route 08): accepted, owner `.build-runs/m7-round-x64-17-owner`.
- **Build 18** (`4753d00e8e`, route 09, ES `4ef2a8dac`) is running: run `20261126T231913Z-2a7b4ce1`, pid 2811954, waiter armed.
  - **Next:** image reads and ACCEPTANCE-18; then phase D `--only s31,s32,s33,s13 --lang en,fr` into `build18-640x480`. s32 is new (the reboot's startup sync in #1489's state, the hub's startup row) and so is s33 (unreachable on the setup check).
  - **Then:** review, close #1492/#1493, add build18 to index.py and the README.
- **Then H700 cold** from the same head: `tools/device-build --device H700 --commit <head> --set m7-round-x64 --name m7-round-h700-<N> --es-supplier <route dir>`.
  - Its one-build step removes the x64 root (D-INFRA-033/036/040: accepted, cold builds preferred). That is why #1492/#1493 go first.
  - SM8550 after H700.
- **Corrected to the steward** (inbox 22:59, 23:03): the candidate is level with ROCKNIX (`0f4806b59b` merged), and ES with ROCKNIX's master. The preflight's 300 cap is M6's #956.
- **Step 0 on the round** (`rc-preflight`, 22:50): base distribution PASS, packages PASS. ES and CI wait on publication; bugs wait on Max's scope question (M7 body); the code audit is owed.

**00000000000000000000. Newest (2026-11-26T22:13Z): build 15 (`90b95f7259`) built and accepted; #1445, #1485 and #1486 closed; standard run 12 on build 15 running; #1490's fix is on the ES round, awaiting build 16.**
- **Run 11 on build 14:** PASS; `rc-preflight --only vm-qa` PASS; recorded on #1465.
- **Build 15:**
  - route 06 (`m7-20261126-3817c3c0b12f`, ES `334ee42b8`);
  - owner `.build-runs/m7-round-x64-15-owner` (ACCEPTANCE-15, admission consumed);
  - run `20261126T214408Z-b2e64750`, the first run `device-build` named correctly (#1445 closed).
- **Closed today since the last item:** #1485 (the provider form's labels translated, N_ + `--keyword=N_`), #1486 (back from SIGN IN AGAIN), #1488, #1484, #1482, #1483.
- **Open bugs filed today, on the M7 candidate's path:**
  - #1489: a connection added outside the interface reads unreadable on the hub and review on the connections page; reconciliation (`import-connections`) is reached only through LINK FROM A COMPUTER's CONTINUE. Next to design and build.
  - #1490: two provider names. Fixed in ES `1006ab503`, needs build 16 and frames (s24, s30 in FR).
  - #1487 is keep-an-eye-on.
- **Running:** standard run 12, `tools/vm-qa` on build 15's image, vm-qa pid 1765028, `/workspace/tmp/rocknix-session/vmqa-standard-12-20261126T2211Z/`, waiter armed.
  - When it ends: `vm-pair down`; `rc-preflight --only vm-qa --build-set …/m7-round-x64-20261125/target`; a note on #1465.
  - Then route 07 for ES head plus #1489's fix, build 16, and phase D s24/s30 (FR) plus #1489's screens.
- **Phase D driver:** s01–s30 are defined. s29 is the OAuth renewal (`conn.py add-oauth`/`remove-oauth`); s30 is the S3 form. A failed arm skips its walk.

**0000000000000000000. Newest (2026-11-26T20:37Z): build 14's fixes are proven and closed; standard run 11 on build 14 is running.**
- **Closed this stretch:** #1482, #1483, #1484, #1488 (all with code traces and frames on `next`). #1111 has 23 of 25 ticked; C15 waits on D-CLOUD-194 and C24's French half on #1478.
- **Filed:**
  - #1485: the provider form's labels are English in French; es-untranslated cannot see them.
  - #1486: back from SIGN IN AGAIN skips the connection page; a VM route exists.
  - #1487: keep an eye on; adding qa-two failed twice on build 14 and did not reproduce.
- **ES round** `m7/rc-round-es-20261125` at `879ab6ce8`: route 05 (`6cdcb7a64`) plus the test fixes. The next route must include `879ab6ce8`.
- **Tools on `next`:**
  - `es-syntax-check` runs every ES `tests/*.py` of the checked tree (15 tests, about 26 s);
  - `device-build` names only a new run directory;
  - the register sweep reads reservations and open rows.
- **Phase D driver:**
  - a failed arm skips its walk;
  - a failed walk reboots the guest;
  - s25/s26 save and restore only the files that exist;
  - screens s01–s28 are defined.
- **Running:** standard run 11, `tools/vm-qa` on build 14's image from the round tree. vm-qa pid 908694; folder `/workspace/tmp/rocknix-session/vmqa-standard-11-20261126T2028Z/` (`rc` when done); harness waiter armed (3 h).
  - When it ends: `rc-preflight --only vm-qa --build-set m7-round-x64`, a note on #1465, `vm-pair down`.
- **Waiting on Max (through the steward):** #1477, #1478, D-CLOUD-194, publication, the bug dispositions, fast mode, the M6 reservation relay (refused by the harness at 19:38Z), and the two proposed sentences in build 14 (steward inbox 20:37Z).

**000000000000000000. Newest (2026-11-26T19:35Z): after the host restart (18:27Z), phase D on build 13 is done, build 14 (`ed61fe8e59`) is built and accepted with three fixes, and its phase D screens are running.**
- **The restart** wiped every guest, waiter and the QA WebDAV backend (`tools/cloud-test-backend up` from the round tree brings it back). No build was in flight.
- **Closed:** #1480 (with the amended root clause: saves can never be the cloud root) and #1115 (phases A, B and D, with the code trace).
- **Filed and fixed on the ES round:**
  - #1482, `7ff5f6b77`: no saved connection now asks to add one.
  - #1483, `274d3716b`: back on EDIT CONNECTION returns to the connection.
  - #1111 C10/C11/C20, `6cdcb7a64`: an unreadable setup is named.
  - #1484, `b80e59646`: the page-lifetime test compiles again. `tools/es-syntax-check` now runs it.
- **Build 14:**
  - route 05 (`m7-20261126-552f3815e4b4`, supplier `.build-runs/m7-rc-round-20261126-05-es/`);
  - owner `.build-runs/m7-round-x64-14-owner` (ACCEPTANCE-14, admission consumed);
  - run `m7-round-x64-20261125/.build-runs/20261126T192842Z-d162c1da`;
  - image `…20261126T192845Z.ged61fe8e5922…`.
- **Running:** phase D on build 14, s04, s05, s15, s19, s20, s22, s23 and s24 at 640x480 EN/FR. Runner `/workspace/tmp/rocknix-session/phase-d-b14.sh`, pid 558003; rc file `phase-d-b14.rc`; harness waiter armed.
  - When it ends: review, tick #1482, #1483 and #1111's C03/C08/C11, commit `build14-640x480/`, then run standard run 11 on build 14 and `rc-preflight --only vm-qa`.
- **#1111 next:** post the criteria comment (draft `/workspace/tmp/rocknix-session/issues/1111-ticks.md`). C15 waits on D-CLOUD-194, and C24's French half on #1478.
- **#1463:** the 2026-11-03 direction stands (M7 keeps its numbers, M6 rekeys). Fresh reservations are on `next` (`d53880bc00`), and the sweep reads reservations and open rows. M6's confirmation was asked through the steward (inbox 19:34Z). Still to do: land M7's off-`next` rows by content (criterion 1).
- **#1445:** build 14 printed the wrong run directory; it is fixed. Criterion 1 waits on the next launch.

**00000000000000000. Newest (2026-11-26T16:25Z): build 13 (`bc81894fa8`) launched and accepted through `tools/device-build`; standard run 10 running; #1481 closed; #1480 fixed and awaiting its frames.**
- **Build 13** carries ES `c0fd03e1b` (#1480's hub fix; route `m7-20261126-16a1ec4e624a`, supplier `.build-runs/m7-rc-round-20261126-04-es/`).
  - It was the first real launch of `tools/device-build`. Owner `.build-runs/m7-round-x64-13-owner`; run `20261126T161644Z-7f89045d`, rc 0, accepted (`ACCEPTANCE-13.json`), admission consumed. Set file `.build-runs/build-sets/m7-round-x64.json`.
  - The round head is now `6aefb77d60`: build 13 plus #1481's `scripts/get_git` fix, with no image change.
- **Standard run 10** on build 13 started at 16:24 (`/workspace/tmp/rocknix-session/vmqa-standard-10-20261126T1624Z/`, harness waiter on its `rc`).
  - When it reports: `rc-preflight --only vm-qa`, a note on #1465, `vm-pair down`.
- **Then phase D** on build 13, four batches, each `phase-d.sh --round <round> --image <build 13> --res 640x480|1280x800 --lang en,fr --outdir phase-d/<res>`. Tile the frames with `/workspace/tmp/rocknix-session/tile.py` for review.
  - #1480's ticks come from its screens s04 and s05.
  - #1111 C03/C08/C10–C14/C16–C20/C23/C24 and #1115 C04 come from the set.
- **Closed:** #1481. The re-clone came from `get_git`'s pipefail plus `grep -q`; fixed on the round and on `next`, and mapped into the upstream series.
- **#1445:** 7 of 8 ticked. Criterion 1 needs a launch that prints the run directory, which was added after build 13.
- **#1448:** criterion 4 ticked. Criterion 5 waits for `next` to take upstream's `fex-emu`.
- **`next` is 621 commits behind `upstream/next`.** `pr-stack-check` refuses until the base refresh, which is step 0 for the final set.
- **Waiting on Max:** #1477, #1478, publication, the 300 bugs, fast mode, and D-CLOUD-194 (it went to the steward at 15:19).

**0000000000000000. (2026-11-26T15:19Z): #1457, #1427 and #1479 closed; run 9 PASS on build 12; the #1111/#1115 campaign is under way.**
- **Build 12** (`a069abd236`, #1457's post-update fix): standard run 9 `VERDICT: PASS` (`qa-a069abd236-webdav-a-20261126-1416`), and `rc-preflight --only vm-qa` PASS. The round head is now `18169f5efe` (local): build 12 plus #1479's test fix, tools only.
- **Closed:**
  - #1457: control and fix rehearsals.
  - #1427: `docs/qa-logs/2026-11-26-1427-free-slot/`, an installed proof on build 12.
  - #1479: the validator test's stale seeding, fixed on the round.
- **The #1111/#1115 campaign:** `docs/qa-logs/2026-11-26-1111-1115-campaign/PLAN.md`.
  - Phase A is done (host suites with the image's rclone 1.76.0), and #1115 C01 is ticked.
  - **Next:** phase B, a driver porting the October installed-component checks to a plain `vm-pair` guest from build 12 (the cases are listed in the plan). Then C (upgrade from `43d0bc3b` onto build 12), then D (EN/FR 640/1280 frames).
  - D-CLOUD-194 (C15, a renewal keeping a folder check) is open and went to the steward's inbox (`20261126T1519Z-one-decision-and-1427.md`).
- **`tools/patch-replay` (#1448 c4, on `next`)** on the round head:
  - Every patch applies for x64, H700 aarch64, H700 arm and SM8550 aarch64.
  - SM8550 arm is running in the runner `/workspace/tmp/rocknix-session/patch-replay-round-20261126T1432Z/` (pid 2654557, harness waiter on its `rc`), slowed by `scripts/get`'s fetch lock while ppsspp-sa's `ffmpeg` submodule clones into the shared cache.
- **`tools/device-build` (#1445), not committed yet.** It sits in the primary checkout's working tree (`tools/device-build`, plus the pre-push, fork-workflow, instruction-files and device-builds edits).
  - The dry runs and refusals were seen: `/workspace/tmp/rocknix-session/device-build-dryruns/`.
  - The failing-step real run is in the background. Its owner is `.build-runs/m7-test-1445-refusal-owner`, and the test set file is `.build-runs/build-sets/test-1445-refusal.json`, removed once its result is recorded. It is held by the same fetch lock, and is expected to stop at the retention report.
  - Commit the tool once that run's result is read.
- **Waiting on Max:** unchanged: #1477, #1478, publication, the 300 bugs, and fast mode. D-CLOUD-194 is added to that list.

**000000000000000. (2026-11-26T14:04Z): #1428 closed; the M7 critical path is Max's answers.**
- **Closed today:** #1474, #1475, #1476, #1012, #1428 (packet `docs/qa-logs/2026-11-26-1428-cloud-setup/`, 33 frames). Round head `6dbc78398e` (local) = build 11 (`30e6ff3db9`, standard run 8 PASS) plus tools only.
- **Waiting on Max:**
  - #1477: the launch question outlives a finished sync; KEEP WAITING launches nothing.
  - #1478: three cloud-page wording questions.
  - Publication: the ES pin as a GitHub commit, the round to GitHub for `ci`.
  - The 300 undispositioned bugs, M6 and unplaced.
  - Codex fast mode, so lanes stay paused.
  - #1470's plan shaping.
- **Then (owner OS):** the final head's build set (x64, H700, SM8550 from one head, D-INFRA-043); rc-preflight in full; the two-lab audit (RC step 4).
- **Round tools not yet on `next`:** WALK_SUITE, VM_RES, `-unchanged-`/`-witnessed-`, `g2g-midsync`, `offline-toggle-outcomes`, `suite-1428.txt`, the PL-021 test change. They land with the round.
- No guests, no build. #1465 checkbox 3 waits for the final head.

**00000000000000. (2026-11-26T13:37Z): #1428 has 5 of 6 criteria ticked; criterion 5 (branch receipts) is next.**
- Packet `docs/qa-logs/2026-11-26-1428-cloud-setup/` (`beace1b194`, 28 reviewed frames, `criterion-2-witness.txt`). Round head `9bcd94fc08` (local): the WALK_SUITE check, the -unchanged-/-witnessed- witness, the folder-action legs, the two-connection fixture. Image unchanged: build 11, `30e6ff3db9`.
- **Next (owner OS), criterion 5:**
  - **no selection:** SAVES and SETTINGS off, then CHECK or CREATE;
  - **offline:** the guest's rclone.conf url port moved to a dead port in a walk pre-hook;
  - **authentication failure:** a wrong `pass` via `rclone obscure` on the guest;
  - **empty selection:** NO FILES FOUND, already in the frames;
  - **retained state:** checks after a creation.
  Each is a walk in suite-1428 with frames, plus the witness where it applies.
- For review on #1428 (not changed): GAME CONTENT shares the ROMS path; FR PARAMÈTRES and RÉGLAGES; after creation no "created" sentence.

**0000000000000. (2026-11-26T13:00Z): #1428 criteria 1 and 3 ticked with frames; the rest of #1428 is fixtures and receipts.**
- **#1428's walks:** `tools/vm-walks/suite-1428.txt` (round `b1938d2adf`) is run with `WALK_SUITE=tools/vm-walks/suite-1428.txt tools/vm-qa <img> --only walks`, with `VM_RES=640x480` for the small panel. It reaches CLOUD FOLDER ACTIONS, CHECK CLOUD SETUP and MANAGE CLOUD CONNECTIONS in EN and FR. Runs `qa-30e6ff3db9-webdav-a-20261126-1231` (1280) and `-1240` (640) both PASS.
- **Packet:** `docs/qa-logs/2026-11-26-1428-cloud-setup/` (`78bf131b67`, 11 reviewed frames); #1428 `issuecomment-7192562887`.
- **Left on #1428, owner OS:**
  - criterion 2: before and after manifests for toggle and cancel on CLOUD FOLDERS;
  - criterion 4: a fixture with two saved connections, two on one provider, then frames of MANAGE CLOUD CONNECTIONS and the change flow with cancel;
  - criterion 5: receipts for the branches (success, no selection, offline or authentication failure, empty selection, cancel, confirmed creation), clean and retained;
  - the last criterion: the hub's transfer entries in FR and at 640x480.
  - Seen for review: GAME CONTENT shares the ROMS folder path; the FR page mixes PARAMÈTRES and RÉGLAGES.
- No guests, no build.

**000000000000. (2026-11-26T12:30Z): round head `30e6ff3db9` (build 11) passes the standard run; step 0's packages PASS by D-RA-054; #1428's page title done.**
- **Build 11** (`ACCEPTANCE-11.json`, admission consumed; ES route `m7-20261126-bb3f0838f671` = ES `d87891f24`, supplier `.build-runs/m7-rc-round-20261126-03-es/`; launcher `/workspace/tmp/rocknix-session/round-build-11.sh`).
  - **Standard run 8** `qa-30e6ff3db9-webdav-a-20261126-1156`: VERDICT PASS, all 16, empty list; `rc-preflight --only vm-qa` PASS, with the tree head equal to the image's.
- **rc-preflight in full** (round `59c278448b`, #1462 `issuecomment-7191154307`):
  - PASS: base distribution, packages (raofflineproxy accepted by **D-RA-054**, `next` `06e5fd16a9`), vm-qa, checkboxes, catalog.
  - Max's: the ES base (a GitHub pin) and `ci` (publication); 300 undispositioned bugs.
  - Re-run `already written` (one tracker error, transient). H700 and SM8550 builds from the final head are still owed (D-INFRA-043).
- **#1428:** inventory `issuecomment-7191212924`. The hub copy, the single CHECK CLOUD SETUP and ACTIVE CONNECTION were already in source. The transfer page's title is fixed (ES `d87891f24`, frame in run 8). **Left:** the evidence criteria. They need walks that reach CLOUD FOLDER ACTIONS, CHECK CLOUD SETUP's results and the connection pages, EN/FR at 640x480 (`VM_RES`) and 1280x800, and a two-connection fixture. **Next (owner OS).**
- No guests, no build. Codex still paused (Max's fast-mode decision). #1477 waits on Max.

**00000000000. (2026-11-26T11:41Z): the round's image `59c278448b` (build 10) passes the standard vm-qa run, all 16, empty list; #1474, #1475, #1476, #1012 closed.**
- **Round** `/workspace/repos/rocknix.worktrees/m7-rc-round-20261125` (branch `build/m7-rc-round-20261125`, local) at head `59c278448b`.
  - Build 10: `ACCEPTANCE-10.json`, admission consumed, image in `m7-round-x64-20261125/target/`.
  - ES route `m7-20261126-d70f76225b96` = ES `95febae8e` on the local branch `m7/rc-round-es-20261125`. The supplier is `.build-runs/m7-rc-round-20261126-02-es/inputs/es`. The writer is `/workspace/tmp/rocknix-session/es-route-20261126.py`, and the launcher template is `/workspace/tmp/rocknix-session/round-build-10.sh`.
- **Standard run 7** `qa-59c278448b-webdav-a-20261126-1108`: VERDICT PASS; `rc-preflight --only vm-qa` PASS with the tree head equal to the image's (#1465 `issuecomment-7191014301`). Run 6 on build 9 had passed too. #1465 checkbox 3 waits for the round's final head.
- **Closed today:**
  - #1474 (the offline switch's sentences, 640x480 packet `docs/qa-logs/2026-11-26-1474-offline-toggle/`);
  - #1475 (es-syntax-check vs a copied build root; French duplicate);
  - #1476 (STOP IT AND PLAY over a stalled sync: `timeout` moved rclone out of the signalled group; the fix `Utils::ProcessSession::signalSession`; rule `es-code-traps.md` § A setsid group);
  - #1012 (time-to-play g2g; new `--only g2g-midsync` cell, round `70663ad96d`).
- **Filed for Max:** #1477 (the launch question outlives a finished sync; KEEP WAITING then launches nothing). The steward inbox has it in plain words (`20261126T1109Z-stop-it-and-play.md`).
- **Round-only tools not yet on `next`:** `vm-pair` VM_RES, `vm-walks/offline-toggle-outcomes`, time-to-play `g2g-midsync`, and the PL-021 scripts test change. They land with the round.
- **Next (owner OS):** #1428's copy and layout work (ES, large); the RC step 0 items in the M7 body. The remaining open M7 bugs sit under #1470's proposed plan, awaiting Max, or need Codex, which stays paused for Max's fast-mode decision. No guests, no build.

**0000000000. (2026-11-26T09:58Z): build 9 RUNNING (round `bfff87f94c`, #1474's ES change); standard run 5 was 15 of 16, its one failure my test assumption, now fixed.**
- **#1428's unchanged save is fixed at its source** (round `2ef63929b7`; run 8 accepted, `ACCEPTANCE-8.json`). The cloud-folder walks pass on run 8 and the known-failures list is **empty** (round `7ea797a710`). Standard run 5 on run 8 (`qa-2ef63929b7-webdav-a-20261126-0908`): 15 PASS. `scripts` FAILED 2 PL-021 checks: `aeb70574ad` published the profile with an unchanged save, which the fix now makes write nothing. Test adapted (round `bfff87f94c`), scripts suite PASSED on the round tree (`/workspace/tmp/rocknix-session/scripts-1428-0941Z/`). #1465 `issuecomment-7188357291`.
- **Build 9 RUNNING since 09:52Z**: run `/workspace/repos/rocknix.worktrees/m7-round-x64-20261125/.build-runs/20261126T095159Z-e89b6147`, owner `m7-round-x64-owner-20261125/submit-09`, admission `admission-9.json`. The harness waiter `btji17z60` watches `build.rc` (expires 12:52Z). Launcher `/workspace/tmp/rocknix-session/round-build-9.sh`; the owner dir must exist before submit.
- **#1474** (ES `2f6c01fd7`; round route `m7-20261126-42eb8b8664b6`, `742443200b`, written by `/workspace/tmp/rocknix-session/es-route-20261126.py`, which reproduces the Nov 25 tar byte for byte): the switch says once why a change did not take. **Next (owner OS), after build 9:**
  1. accept it (`ACCEPTANCE-9.json`, consume);
  2. on a guest from its image, `tools/vm-walks/offline-toggle-outcomes --port 10022 --identity <qa-key> --monitor <sock> --outdir <dir>` (round `d447c2192d`; busy, refused, restored, and the took control). Read the frames against #1474's sentences.
  3. then a standard `vm-qa` on build 9's image, the first that can read `VERDICT: PASS` with an empty list;
  4. then `rc-preflight --only vm-qa --build-set <target>`.
- **#1475 closed** (es-syntax-check vs a copied build root, `next` `718ec14a8a`; the French duplicate in ES source). Menu map `dbd0d45299`.
- **#1012:** its open item 2 (STOP IT AND PLAY over a visible exit sync) needs a time-to-play mode that relaunches once the sync holds its lock. Today's runs relaunch before the sync starts (PL-009 claims it), so no question appears. Harness work, after build 9.
- Codex dispatches still paused (Max's fast-mode decision). Steward inbox `20261126T0952Z-run5-and-build9.md`.

**000000000. (2026-11-26T08:55Z): standard run 4 is 15 of 16 PASS; #1465 checkbox 2 waits only on #1428's question.**
- Round head `96fe959434` (local), image run 7 `2fc3f2aad2`. Standard run `qa-2fc3f2aad2-webdav-a-20261126-0823`: the only failure is `walks` (known, #1428): `confirm-cloud-folder`'s witness refuses an unchanged SAVES FOLDER save's new `config_id` (#1428 `issuecomment-7186014027`). frame-diff PASSES with claims against the unmoved `d72084ccad` baseline. Known-failures list: one entry.
- **Next (owner OS):** #1428's design answer decides the last entry: the product stops reconfirming an unchanged save, or the walk's witness compares paths and files but not `config_id`. #1428 is a large ES change (copy, French, frames). Other M7 work by priority: #1474 (the ES sentence, proposed words on the issue); RC step 0 items in the M7 body (14 packages behind, ES pin vs ROCKNIX, device facts); the round's eventual landing on `next` (publication of the candidate is Max's). Codex dispatches still paused pending Max's fast-mode decision.
- No guests, no build, all lanes idle.

**00000000. Newest (2026-11-26T07:20Z): #1467 fixed and closed (patch 039, D-RA-053); the round's known failures are walks and frame-diff only.**
- Round head `0067ae0b05` (local); its newest image is run 7 `2fc3f2aad2` (`ACCEPTANCE-7.json`), which carries patch 039. Lifecycle suite 23 PASS; drop-in reproduction PASS. #1474 (bug, M7) filed for ES's silent toggle revert after busy, refused or restored, with proposed words.
- **07:58Z:** standard run 3 on run 7's image: 14 PASS, 2 known (walks, frame-diff). The walks now follow the shipped pages (round `60b5017efb`): `to-change-cloud-folder` passes. `confirm-cloud-folder`'s witness refuses an unchanged save's new `config_id`, which is #1428's design question (`issuecomment-7186014027`). **Correction (07:58Z): frame-diff HAS an accepted baseline** (`/workspace/artifacts/rocknix-images/walk-baseline`, build `d72084ccad`, accepted 2026-09-26); it fails on 45 unclaimed regions and missing screens, not for lack of a baseline (#1465 `issuecomment-7186044935`). **Do not accept a new baseline** (frame-diff: the baseline is 'the last cut the maintainer accepted'). **Next (owner OS):** a full walks run on run 7's image is RUNNING since 07:58Z (`/workspace/tmp/rocknix-session/walks-full-20261126T0758Z/`, `rc` and `vm-qa.log`; stop guests with `vm-pair down`). Then `tools/frame-diff compare /workspace/artifacts/rocknix-images/walk-baseline <run>/walks --masks tools/vm-walks/masks.txt --claims tools/vm-walks/claims.txt --report <f>`, and review each unclaimed region: claim it with its issue, or file a regression. Codex dispatches still paused pending Max's fast-mode decision.

**0000000. Newest (2026-11-26T07:05Z): Codex dispatches paused pending Max; #1467's fix designed, next to build.**
- **No Codex dispatch from this workspace until Max decides on fast mode** (steward's request 06:17Z; `steward-notes/for-os/20261126T0617Z-allowance-18-percent.md`). The fast-vs-default measurement (`codex-allowance/ab-20261126T0652Z/`) was inconclusive at about 1.2 M tokens per tier (account 20 to 21 to 21; #1471 `issuecomment-7185019477`). A decisive run is about 10 M tokens per tier, about 8 points; whether to spend that is Max's call via the steward (inbox `20261126T0701Z-tier-measurement-result.md`). Each dispatch's cost is on #1472 (`issuecomment-7184853558`). Account 21% at 07:00Z.
- **#1467's fix (owner OS, design on #1467 `issuecomment-7184881904`), in the fork's proxy patch series** (`projects/ROCKNIX/packages/network/raofflineproxy/patches/`, next number 039; source as built: `m7-round-x64-20261125/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-40201a2a5d…/linux/raofflineproxy/`):
  1. `lifecycle_owner.process_owner`: an `AdmissionError` from `adapter.armed()` (before `run_owner` touches anything; the original #1467 reproduction) records REFUSED with its reason, not FAILED. `observe()` already maps a clean REFUSED to terminal `refused`, and the ExecStopPost recovery returns for any terminal phase.
  2. `finish_stopped` for mode `disable` when `recovering=True` (the ExecStopPost retry): if `adapter.commit_disabled()` raises again, roll back with the existing `restore(adapter, lease)` (service restarted under the unchanged preference, phase RESTORED, provable by `observe()` as `restored`). **Before building, read how the ctl and ES treat a `restored` outcome for a disable request** (`raofflineproxy-ctl` `toggle`/`operation`, ES `GuiRetroAchievementsSettings.cpp` around 541/582): it must read as "the change didn't happen", not success.
  3. **The ES half** (#1467 `issuecomment-7185056976`): ES adopts the backend's flags on any terminal outcome and says only "The current setting is confirmed.", so `busy` (already shipping), `refused` and `restored` silently flip the toggle back. Add one sentence per outcome when it differs from the request, with the proposed words on the issue, plus French, menu-map/flow entries and 640x480 frames. Run `tools/es-syntax-check` before the ES pin moves.
  - Proof: `tools/raofflineproxy-lifecycle-test`'s three #1467 assertions PASS on a rebuilt round image, its other 19 still pass, and the unfixed proxy fails them (today's runs). Then the `lifecycle #1467` known entry leaves the list. The proxy has no unit tests for the owner; the guest test is the control.
- Round head `1df537e98f` (local); round image run 6 `26bc845d9f`. No guests, no build, all lanes idle.

**000000. Newest (2026-11-26T06:50Z): the scripts suite passes; the standard run is 13 PASS, 3 known; #1467 proven and next to fix.**
- The round (`1df537e98f`, local) passes its scripts suite (0). Standard run `qa-26bc845d9f-webdav-a-20261126-0617`: FAIL only on walks (#1428), frame-diff (no accepted baseline) and the `lifecycle` guest suite (#1467), none unlisted. `rc-preflight --only vm-qa --build-set` refuses it, correctly.
- **#1467 is proven on a guest** (`issuecomment-7184164892`): if the settings write and its retry both fail during a disable, the owner stays FAILED (never terminal), the preference stays on while the service is down, and a later disable answers 75 until a reboot. **Next (owner OS): its fix in the proxy's lifecycle** (proxy `40201a2a5d`, source in the build root's `build/raofflineproxy-*/linux/raofflineproxy/lifecycle*.py`; the fork's proxy patches under `projects/ROCKNIX/packages/network/raofflineproxy/patches/`). A FAILED owner that changed nothing ends REFUSED; one that stopped the service restores it under the verified preference before settling. The lifecycle suite's 3 FAILs must then pass.
- Lanes all idle (pH's worktree `m7-1465-scripts` at `1df537e98f`; pJ's `m7-1468-test-drives`). No guests, no build. Allowance 14% at 05:32Z.

**00000. Newest (2026-11-26T04:47Z): #1454, #1468 and #1473 closed; #1465 down to guest work; the Codex pace set.**
- **Closed today:** #1454 (game-exit QA clock fix, `tools/game-exit-qa/` on `next`); #1468 (D-QA-066, `tools/test-drive-check` gate on `next`); #1473 (bug: on-device cloud sign-in never saved its connection with the window open; fixed on the round in `df5d096261`, on the November 5 build too). #1469: all criteria ticked, open until the round's `vm-qa` reaches `next`.
- **The round** (`/workspace/repos/rocknix.worktrees/m7-rc-round-20261125`, branch `build/m7-rc-round-20261125`, local, head `26bc845d9f`) carries all of today's harness fixes and #1473's fix. **Run 6 rebuilt it at 04:51Z** (`20261126T045149Z-af35f62b`, 649/649, all channels 0, admission `1cd45b7d…` consumed; `ACCEPTANCE-6.json` in `m7-round-x64-owner-20261125/`; image `0.0.1-dev+20261126T045152Z.g26bc845d9ff2`, its `cloud_oauth` byte-identical to the fixed source). **Its full standard `vm-qa` run finished at 05:28Z: 12 PASS, 3 FAIL all known (scripts 11, walks, frame-diff), none unlisted** (`qa-26bc845d9f-webdav-a-20261126-0456`; `rc-preflight --only vm-qa` refuses it, correctly; guests stopped). It ran since 04:55:21Z (pid 1584302, detached; output `/workspace/tmp/rocknix-session/vmqa-standard-26bc845d9f-20261126T0455Z/` with `rc` and `vm-qa.log`; waiter `b0kv4b6yv`). It owns guests a and b: stop only with `vm-pair down`. Expected verdict FAIL on the three known entries (scripts' 11, walks, frame-diff); its report is the first standard-run report `rc-preflight --only vm-qa` can read.
- **05:52Z:** the scripts suite's last 11 checks are traced (pJ, `9add00cf3a`: 4 kept, 5 superseded by the lifecycle's busy refusal, 2 defect readings added to #1467) and `tools/raofflineproxy-lifecycle-test` passed 17/17 on guest a (on `next` `e7bb3b0c3d`, round `c23dad200d`). **pH is working** (turn from 05:52:31Z, waiter `bddumzdxk`, brief `dispatch/20261126T0552Z-pH-1465-lifecycle-suite.md`): reset its worktree to the round head, the persistent double-failure case (expected FAIL, #1467), a `lifecycle` guest suite in vm-qa with a `lifecycle #1467` known entry, and the 11 host cases replaced by pointers. OS then runs the full scripts suite and the lifecycle test on a guest.
- **#1465 left (all need a guest):** the 11 scripts checks (8 helper-disable now the lifecycle's, 3 needing a writable `/run/raofflineproxy-lifecycle`) want a guest test beside `tools/raofflineproxy-toggle-test`; the two cloud-folder walks rewritten for #1428's chooser; a walk baseline for frame-diff; then the rebuild and the standard run, read by `rc-preflight --only vm-qa --build-set`.
- **Lanes:** pB, pJ, pH idle (pH compacted 04:24; its worktree `m7-1465-scripts` has 15 commits all taken onto the round; pJ's `m7-1468-test-drives` delivered). p7/p8/p9/pA/pC/pD idle with reasons on #1472. **Pace:** account 8% at 04:10Z (window to 2026-12-03 03:18Z); one lane at a time, compact past about 250 k tokens a call (#1472 `issuecomment-7182364756`). Codex sandbox: no namespaces, no `gh`, no Herdr socket — OS runs suites and watches rollouts for `task_complete`.
- **Steward inbox notes today:** 0323Z (issues on GitHub), 0341Z (cost so far), 0356Z (first fast turn, #1454), 04xxZ (pace at 04:10), 0418Z (#1473). Nothing new in `for-os/` after 03:36Z.

**0000. Newest (2026-11-26T03:25Z): Codex lanes resume after the allowance reset (#1472, D-WORKFLOW-239).**
- **Max, about 03:15Z:** reset the Codex account and resume every lane using Codex; and put the plan on GitHub. The reset was already in effect (steward's read 03:16:39Z: 0%, no credit). #1470's body now holds the five proposed steps ("awaiting Max's shaping"); #1471 files the fast-mode instruction (D-WORKFLOW-238), #1472 the resume (D-WORKFLOW-239). The issue numbers are in `steward-inbox/20261126T0323Z-codex-resume-and-github.md`.
- **pB is working on #1454 criteria 2 to 4** on the fast tier: resumed through `tools/herdr-lane` at 03:19Z, `task_started` 03:20:18Z (turn `01a215de-…`), `thread_settings_applied` service_tier `priority`, gpt-6.2-sol, xhigh. Brief: `/workspace/tmp/rocknix-session/dispatch/20261126T0320Z-pB-1454.md`. **pB holds the VM slot until it reports; start no guest meanwhile.** It commits the fixed tool under `tools/game-exit-qa/` on its branch; OS integrates it onto `next` by content and registers it (pre-push, `fork-workflow.md`, `instruction-files.md`). Keep `/workspace/tmp/pix-m7-pc-20261125-backup-0{1,2,3}/` until then.
- **What watches pB:** harness waiter `br8f00bzb` on the rollout's `task_complete` for that turn (4 h expiry), plus pB's own `herdr agent prompt w4:p2` result. Both are silent after this session disconnects: a resumed session reads `herdr agent get w4:pB` and the rollout `~/.codex/sessions/2026/11/03/rollout-2026-11-03T16-18-48-01a1a234-c080-75d2-98d3-3be40c9a57bb.jsonl` first.
- **Allowance:** 0% at 03:18:46Z, 1% at 03:23:39Z (`/workspace/tmp/rocknix-session/codex-allowance/`: `read-allowance.py` via `codex app-server`, `turn-tokens.py` per turn, `readings.txt`). Waiter `brlmxkx02` reads again at 03:40Z. pB's old thread re-sends about 281,000 tokens a call; new work goes to fresh lanes (`tools/herdr-lane fresh`) in their own worktrees.
- **03:40Z: 3% used** (pB's turn 23.3 M tokens in 20 min, 98.6% cached; at most about 6%/hour for an old thread). Posted on #1471 and #1472; inbox `20261126T0341Z-fast-mode-cost-so-far.md`.
- **pH (new, `w4:pH`, lane `m7-1465-scripts`, thread `01a215f0-ec38-…`) is working on #1465's scripts suite**: about 42 cloud setup and sign-in checks, host only, judged test-behind / product-wrong / sandbox. Worktree `/workspace/repos/rocknix.worktrees/m7-1465-scripts`, branch `feature/m7-1465-scripts` from round `e0b494de79`. Started 03:40:47Z, tier `priority`. Brief `dispatch/20261126T0340Z-pH-1465-scripts.md`. Waiter `bp2tf58p6` on its `task_complete`; cost reading `bes3r4f5t` at 04:10Z. Its commits go onto the round by OS.
- **Idle lanes named on #1472** (p7, p8, p9, pA, pC, pD: closed issues, finished work, or #576 outside the current order). New work goes to fresh lanes.
- **#1469 done to its criteria** (all five ticked, `issuecomment-7181810822`): `rc-preflight --only vm-qa --build-set` on `next` (`0366353ab1`), `vm-qa`'s run-kind line and closed-issue refusal on the round (`e0b494de79`, local). Stays open until the round's `vm-qa` reaches `next`.
- **03:56Z state.** #1454 CLOSED as completed (pB's fix, offline and both VM proofs verified by hash; `tools/game-exit-qa/` on `next` in `5e71828fac`, registered; code trace with its Already-written line, `issuecomment-7182057852`; M7 body updated). pB's first fast turn: 26.6 min, 31.0 M tokens (98.9% cached); account 0% to 5% by 03:47Z (shared). pB is idle; its old thread is not reused.
- **pH (#1465 scripts):** its sandbox refuses `bwrap --unshare-user`, `gh` and `herdr agent prompt` (Codex workspace-write sandbox). It judged all 39 cloud failures (a) and committed C4, C2 and PL-021 fixes (`52d1f3cb56`, `dd4c337268`, `2a78ae1f71`). **OS runs the full suite in its worktree** (`/workspace/tmp/rocknix-session/scripts-suite-pH-1.log`, task `bih55a2gz`) and sends it the FAIL lines; pH waits idle meanwhile.
- **pJ (new, `w4:pJ`, lane `m7-1468-test-drives`, thread `01a215fa-c949-…`):** #1468's map (`docs/qa/test-drives.txt`) and check (`tools/test-drive-check`, wired into `ceremony-check --gate`). Worktree `m7-1468-test-drives` from `next` `5e71828fac`. Started 03:51:33Z, tier `priority`. Brief `dispatch/20261126T0351Z-lane-1468-test-drives.md`. Waiter `b1iq30sba`. OS writes the rule, its register row and the registrations at integration.
- **#1465 by OS:** the wrapper suite drives f726's mailbox (round `2f9573781c`; real 10/10 PASS, `--control` 3/3 FAIL); its known-failures entry removed. **The time-to-play g2g question is answered: PL-009, not a defect** (#1465 `issuecomment-7182118348`, which corrects the 00:29 comment: the rclone copy it cited was the previous cell's). `tools/time-to-play` (round, uncommitted) now tells the claimed-sync path from the running-sync path and proves the deferral at the next exit; judge proven offline. **Running now:** `tools/vm-qa <round 43d9013c4d img> --only time-to-play`, detached, output `/workspace/tmp/rocknix-session/ttp-g2g-20261126T0355Z/` (`rc`, `vm-qa.log`), waiter `b55097pcr`. It owns guest a; stop by `vm-pair down` only.
- **Next (owner OS), in order:** consume pB and pH as they return (pB: integrate `tools/game-exit-qa/` onto `next` by content and register it; pH: take its commits onto the round); the wrapper fixture's port to f726's mailbox (OS, in the round worktree; pH does not touch that file); then #1468 (a candidate for a third fresh lane once the 04:10Z cost is read). No guest while pB holds the VM slot. Read `steward-notes/for-os/` at each push and checkpoint.

**000. Newest (2026-11-25T08:47Z; supersedes the #1450, #1451 and allowance lines of item 00).**
- **14:22Z:** the M7 bug triage resumed after a stop at the 12:06Z turn end. Five moves were made with reasons (item 1 under "Next (owner OS)" below), and #1458 was filed. A third NEEDS MAX (mGBA Smart on updated handhelds) is queued behind the RG SP copy and the October images. Max had not written since about 06:13Z, per the steward's 14:06Z note.
- **11:17Z:** the step-0 items were read over the whole tracker after the steward's 11:03 note, and the Nova's bootloader claim was corrected. Both are under "The code audit" below. Max had not answered the RG SP copy as of 11:03Z.
- **11:29Z:** all 27 code traces are posted and checked, and #1455's build is at 636/642, waiter `brnquief0`.
- **11:40Z:** the futro is done, and its packages finding is corrected on #555. #1456 filed: `rc-preflight` hides BEHIND rows when the freshness tool exits 2.
- **11:50Z:** #1455's starting image is built, identified and kept, its build root is removed (111.6 GB recovered), and criterion 2 is ticked.
- **12:05Z:**
  - #1455 criterion 4 ticked: run 3, 40 PASS, 0 FAIL (`7161896592`); the tool's seeds are in `adaad9dc49`. Criterion 3 is open for its item-by-item argument; criteria 1 and 5 remain.
  - #1457 filed: upstream `post-update` resets an opt-in to `system.suspend.dpms`.
  - The RG SP note is restated in place on the steward's request: recommend copying now, with wait equally fine, and the reasons are the GCC 16 rebuild and games frozen during sleep. The steward has put it to Max again.
- **Still waiting on Max for the RG SP copy.** It was put to him at 06:27:52Z; he had not answered by the steward's 08:29Z note. Nothing has run on any device. On a relayed yes, the plan in item 00 stands.
- **The steward's 08:29Z note (D-WORKFLOW-195):** move what needs no device, no Max and no Codex allowance. The allowance read 88% used at 08:08Z (reset 2026-11-30T06:35:50Z), and another lane is still drawing on it, so this lane dispatched nobody and did the work itself:
  - **#1454 criterion 1 ticked** (comment `7157175665`). The cause:
    - the second review's 10 s window (`RECHECK_REVIEW`, `visible_quit.py:151`), against ordinary approvals of 5.9 to 14.2 s;
    - triggered by the menu clock's minute changing between preview and check;
    - made worse because `CLOCK_TEXT` knows only four renders from Nov 21, and the quit dialog masks nothing.
  - **#1454 criteria 2 to 4 wait.** That is the fix, two VM proofs (about 12 Codex points) and the tool into the tree. The tool's only copies are pB's `/workspace/tmp/pix-m7-pc-20261125-backup-0{1,2,3}/code/`. **Keep those folders** until criterion 4. Owner: pB, on the next affordable dispatch or after the reset. It must close before the next PC VM run or any RC call.
  - **#1451 criteria 2 and 4 ticked** (`cc89bb4453`, `acbfe010e8`). The escalation tool writes only to the inbox and refuses a pane config (35 tests; the old tool fails 24). The coordination rules (D-WORKFLOW-183/184/185/187/189/190/195) are on `next`. Five decided rows that had never been committed (D-WORKFLOW-191/192/193/195, D-LAUNCH-008) are appended. Record: `docs/qa-logs/2026-11-25-1451-rules-review/REVIEW.md`. Criterion 3, the agenda, stays held for the steward.
  - **#1450 criterion 4 reworded and held under D-WORKFLOW-203.** It is no longer blocked by #1451. A CI silence is "something broken", which goes to #1452's monitoring tool, and nothing is built before #1452's inputs.
  - **#1449 criterion 5** waits on #1445, the one-command build route: a multi-hour tool whose proof is a real build launch, and no build is planned before the device step and the code audit.
- **`/workspace/artifacts` pass: first batch prepared and refused (#493 `7157556001`).** It retires the 46 October candidate images (70,587,789,508 B, 19 store entries), keeping each entry's records plus a `RETIRED.json`.
  - Script: `conflict-resolution/docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/20261125-artifacts-candidates/retire-candidate-images.sh`, **sha256 `e076737b…`** (floor exactly 46). This is the batch Max's yes must name.
    - The revision refused at 08:50 was `4cd6b903…`; `4a7eab82…` was the floor fix.
    - `e076737b…` corrects its wording: the RG35XX SP runs H700 `43d0bc3bf4` of 2026-10-07 by the device action log. Its images left the store on 2026-10-12, entry `d89b067a…`, so none is in the batch.
    - #493 correction comment `7157700039`.
  - **#1455 filed:** rehearse the RC's upgrade from the RG35XX SP's October 7 build on the VM. Needs a PC image of `43d0bc3bf4`, the old state listed and seeded, and `release-candidates.md` step 3 naming the device's own build.
  - The harness review refused it at 08:50:20Z; nothing ran (`REFUSAL-artifacts-candidates.json`).
  - **NEEDS MAX** `steward-inbox/20261125T0851Z-old-test-builds.md`, marked for after the RG SP question. On the relayed yes, run the script once and report the measured recovery on #493.
  - Not in this batch: `pixelelated-release-sources` (32.4 GB: October M7 source archives and the `materialization05` git store, which borrows from the 13-04 keep item), `pixelelated-build-custody` (23.5 GB) and `m6-*` (M6's, not inspected). Inventory: `/workspace/tmp/rocknix-session/artifacts-pass-20261125/inventory.tsv`.
- **Checkbox reads against pB's 2026-11-25 originals: done (09:05Z).**
  - **#1433: criteria 4 and 5 ticked** (comment `7157831598`; 19 cited files check against manifest `92a3e316…`).
    - The changed save reached the server and the preseeded version survived with its mtime; 8 server objects, 7 local files and 4 protected configs are unchanged.
    - The one difference is the system config's `global.netplay.nickname` line, which the frontend writes at launch. Untick 4 if that is read as "configuration changed".
    - Criterion 1 (binding the original incident: `c9864eea`, `7581756f`, `27b5793a`; DETAIL_UNOBSERVED) stays open.
  - **#1427 and #1423: nothing tickable from the run;** notes `7157851519` and `7157852103` say what it covers.
    - #1427 needs an installed COPY TO FREE SLOT run on the candidate image, and the ES-pin check for criterion 1.
    - #1423 needs the Nova case on a per-action yes.
- **#1455: the starting image is built and accepted (11:50Z); criterion 2 is ticked** (`7161551945`). Cold GENERIC_X64 build of `43d0bc3bf4`, run `20261125T091159Z-3c44fe1c`, 09:11:59Z to 11:45:37Z. All three result channels were 0, and the processes had gone. `/etc/os-release` names `43d0bc3bf47fd858…` and builder `988c0ba5`.
  - **Keep items** until #1455's rehearsal passes:
    - `m7-pc-43d0bc3b-20261125/target/` img.gz `fdcfa903…` and tar `2a539a8b…`, 4,147,167,630 B together;
    - `owner/keep/emulationstation-72494bc72e.unstripped`.
  - **Removed:** the build root and the empty `sources/` stub. Recovered 111.6 GB, measured. Receipt: `owner/ACCEPTANCE.json`.
  - **Next:** criterion 3's save and save-state layouts; add the seeds to the rehearsal; then `tools/vm-upgrade-rehearsal` against the candidate's PC tar (criterion 4).
  - Historical (the run while it was live):
  - Worktree `m7-pc-43d0bc3b-20261125`, owner `conflict-resolution/.build-runs/m7-pc-43d0bc3b-owner-20261125/`.
  - Matched to the RG35XX SP's build: image `988c0ba5`, `CUSTOM_VERSION=0.0.1`, options `2cf98cb3`, ES `72494bc72e`.
  - Processes: job pid 2339622, `make` 2339651, `watch-job` 2339623. A harness waiter (task `brnquief0`) reports on `launcher-result.json` or job exit; it dies with the session.
  - Consume it from `submit-01/launcher-result.json`, `tool-wrapper.rc`, the run's `build.rc`, the identity file and the image hashes. Then remove the build root and keep the img.gz and tar as named keep items until #1455 passes.
  - Criterion 3: the list is complete after the third pass (`7161615211`: save layouts, and the widened cloud rules that `cloud_sync_helper` merges on every backup). It stays open until the items are seeded or argued absent in the rehearsal.
  - **Criterion 4, first run (owner OS, started 11:51:08Z):** `tools/vm-upgrade-rehearsal`, unchanged, with its own seeds (sha256 `894021ab…`), from `/workspace/tmp/rocknix-session/rehearsal-start-43d0bc3bf4/…img.gz` (a link to the keep item) to the candidate's PC tar, expecting `0a3e979e50`.
    - Detached: console and rc in `/workspace/tmp/rocknix-session/rehearsal-43d0bc3bf4-to-0a3e979e50-01/`. Harness waiter `bq57mt5gg`. Its records are under `/workspace/artifacts/rocknix-images/qa-0a3e979e50-upgrade-from-43d0bc3bf4-*`.
    - Then add criterion 3's seeds as a second run. Editing the tool waits for the first run's rc.
- **The code audit (RC step 4) is blocked, not started.** Exact blockers:
  - step 3 is incomplete: #1455's rehearsal (above), RECORD.txt and the catalog;
  - step 0 fails on `0a3e979e50`: `bugs FAIL` with 542 open bugs without a disposition (full read; the tool alone shows 300), `packages CANNOT` (corrected 14:38Z: the candidate's own run shows 7 BEHIND, 6 PINNED and 2 UNKNOWN, `FRESHNESS-candidate-20261125.txt`; the morning's `FRESHNESS-full-20261125.txt` was `next`'s list, #1460; the tool's message shows only its last line, #1456), and `base: emulationstation CANNOT` (the pin is a tarball tag).
  - **Full step 0 (09:25Z): `CANNOT ANSWER`, rc 2** (#555 `7158351275`; `m7-pc-0a3e979e-owner-20261124/RC-PREFLIGHT-full-20261125.txt`).
    - **Read over the whole tracker at 11:06-11:15Z** (#555 `7160824879`; the 09:25 comment corrected). `box-check` and `rc-preflight` cap their lists at 300 (#941, #956: M6 bugs, M6's fix). A harness runs their own code with the limit raised and refuses short lists: `m7-pc-0a3e979e-owner-20261124/STEP0-FULLREAD-20261125/fullread.py`. Re-run it, not the bare tool, wherever step 0 is quoted, until #941 and #956 land.
      - **checkboxes PASS:** 949 issues, 2,324 open checkboxes, 0 fail.
      - **bugs FAIL:** 542 open (320 M6, 205 no milestone, 17 M7). No register rule settles whether M6's findings count at an M7 call: a scope question to prepare.
      - **already-written FAIL, closed side only:** every open bug's trace has its line. #366 and #1154 were fixed at 09:29Z.
    - ci FAIL: `0a3e979e50` is not on GitHub. Pushing it is publication, separately governed: a decision to prepare.
    - CANNOT: rclone 1.76.0, the ES pin (tarball tag), device facts (#270).
  - **Next in the OS lane:**
    1. Record-keeping. #366 and #1154 are done (09:29Z): both traces had the line, but formatted so the pattern missed it (mid-line, and in backticks). Fixed with no words changed, and noted on each issue.
       - **Done 11:28Z: all 27 traces posted.** Checked by `rc-preflight`'s own patterns, 27/27 with the #1455 control false (#555 `7161110545`; `STEP0-FULLREAD-20261125/traced27-check.txt`). Step 0's already-written item is answered on both sides.
       - The candidate's own `pixelelated-state-check` passes on the H700 and SM8550 update tars (`m7-h700-0a3e979e-owner-20261125/STATE-CHECK-20261125/`).
       - **Step 0 left:**
         - bugs: 542, a scope question for Max;
         - ci: publication, Max's;
         - packages: **corrected 14:38Z.** The morning's "14 BEHIND and 8 UNKNOWN" were `next`'s rows (#1460). The candidate's own run (`FRESHNESS-candidate-20261125.txt`) reads 7 BEHIND, 6 PINNED and 2 UNKNOWN (#555 `7165597605`). Bump the six small ones in the source round; raofflineproxy needs a bump with `ra-offline-test`, or a pin with a row; spirv-headers needs only a `PKG_SITE`; AetherSX2 follows upstream (#1459);
         - ES base: the tarball tag;
         - device facts: by hand (#270).
       - **Futro done (11:40Z):** `docs/futros/2026-11-25-m7-rc-step0.md` (`325ec1e693`), summary on #555 `7161344224`. The milestone body now carries step 0 and the audit's blockers (read back 11:40Z). `0a3e979e50` is an engineering build qualified ahead of step 0; the release candidate is whatever head passes it.
       - **Next (owner OS), in order, from the futro's adjustments:**
         1. **In progress (owner OS; started 11:42Z, stopped at the 12:06Z turn end with no blocker, resumed 14:06Z on the steward's note): triage the open M7 bugs.**
            - **The five proposals are done (14:21Z, #555 `7165142510`):**
              - #1110 and #840 moved to keep an eye on and retitled "Monitor…";
              - #1113 closed as completed: trace and the 16 controls re-run on the candidate's bytes, open item on #277;
              - #1423 stays a bug: Smart does not reach upgraded handhelds, a fifth checkbox added, NEEDS MAX `20261125T1415Z-mgba-smart-on-updated-handhelds.md` queued;
              - #1422 stays a bug: ROCKNIX #3481 is not in the candidate or `next`.
            - **Open M7 bugs: 14.**
            - **14:28Z:** all 14 now have a closing path (#555 `7165324411`).
              - **Fix in the candidate, bound to its image bytes:** #607/#608/#610 (Steam installer `162e4272…`), #618 and #629. The binding notes are on each issue.
              - **Two guest sessions cover most of the rest:** a GENERIC guest with the Steam overlay (#607, #610), and the candidate's PC image (#618, #629, #609, #1427).
              - **#608's ticks wait for its records on `next` (#1458).**
            - **14:30Z: item 1 done.** #1115's fix is in the candidate. #1111's work is in it in a later form, with 25 criteria open and a plan needed (#555 `7165375768`).
         2. **Done 14:33Z: the unplaced bugs by origin** (#555 `7165449383`; `docs/qa-logs/2026-11-25-m7-bug-triage/origin-final.json`). 204 of 207 are M6 renovation findings. #1457, #1456 and #1012 were placed in M7.P5. Open bugs: 541, with **M7 17** and **M6 524** (320 under M6, 204 unplaced). #1012's accepted fix `af16f3391c` is unmerged on `origin/fix/m6-1012-ttp-runner`.
            - Note: `0a3e979e50` is not on `next`'s line (393 commits ahead), so the source round builds on the candidate's line.
            - **#1458 filed (14:16Z):** about 95,000 QA record files (2.1 GB) in ten worktrees are on no branch. Not started. Do not remove those worktrees before its inventory exists.
         3. **Done 14:38Z: the packages, one line each** (#555 `7165597605`). The morning's list was `next`'s (#1460, filed). On the candidate: 7 behind, 6 pinned with reasons, and 2 unknown read by hand. #1459 filed: the SM8550 image ships AetherSX2's proprietary binary, which ROCKNIX withdrew over licensing; upstream's October 18 deletion was undone by a delete/modify merge. **Open M7 bugs: 19** (17 plus #1459 and #1460).
         4. **Done 14:42Z: the ES pin's history** (#555 `7165685123`). The pin is a computed tree, nearest commit `16dbac5211` plus 73 fork sources and the pugixml bundle. Its base is 20 commits behind ROCKNIX's ES master, including SM8550 hardware suspend. Fix in the source round: commit the tree over `16dbac5211`, then merge ROCKNIX's 20.
         5. **Done 14:49Z: the device facts** (#555 `7165866109`).
            - The central device log misses all October lane updates (**#1461**). **The RG35XX SP was at `bcc866f1` on 2026-10-25**, not `43d0bc3bf4`, and Max's manual install that day is unrecorded.
            - #1455 criteria 2 and 4 are unticked. Do not run the step-5 plan or the rehearsal from `43d0bc3bf4` until criterion 1's read.
            - The October-images NEEDS MAX was corrected in place: the `bcc866f1` H700 entry `71ff97b8…` is in the batch, with a keep option.
            - `device-facts.md` boot rows updated. All three handhelds were offline at 14:43Z.
         6. **Done 14:53Z: the questions for Max are written as NEEDS MAX** (`20261125T1451Z-m6-bugs-at-the-m7-call.md`, `20261125T1451Z-publish-the-candidate-head.md`; mGBA `20261125T1415Z`). Queue: RG SP copy, October images, mGBA, M6 bugs, publishing. Each was written as:
            - whether M6's 524 findings count at the M7 call (#555 `7165449383` has the groups);
            - whether to publish the head (`0a3e979e50` is not on GitHub);
            - mGBA Smart on updated handhelds (already written, `20261125T1415Z`).
         7. **In progress (owner OS): the source round, #1462.** The plan is on the issue. The merge dry run is on #1462 `7165993025`: 15 conflicts, 2 unapplied upstream deletions, 24 older ones to decide. **Step 1 done: merge `f207c4ccd3`, local only,** on `build/m7-rc-round-20261125`, worktree `rocknix.worktrees/m7-rc-round-20261125` (#1462 `7166118617`). Unpushed until Max answers on publication. **Replay done (15:04Z):** batteryplus applies, and 8 fork RetroArch patches conflict with a heavily changed RetroArch `f726f0955a` (#1462 `7166232999`). Upstream's new `0012-cheevos.patch` reopens #825, so the fix must become `0012a-…`. The scratch tree is `/workspace/tmp/rocknix-session/ra-rebase-20261125` (`old-base`, `new-base`). **RetroArch port in progress (owner OS, started 15:04Z)** in the scratch tree's `new-base` branch: work tree `ra-rebase-20261125/new`, git dir `../.git`, always with `--work-tree=.`. Sizing is on #1462 `7166273422`: 20 of 44 hunks fail. Ported so far:
              - `0018`: the command.c guard is kept; the runtime_file.c hunks are dropped because f726 no longer restores the slot from the runtime log;
              - `0012a-cheevos-cmd-no-shell` (new): replaces upstream's `system()` block (#825).
              15:10Z: `0013` and `0014` are also ported, 4 of 8 (#1462 `7166419304`). f726 dropped the Ozone x1.5 widget factor, so `0016`, `0017` and `0019` get decided by 640x480 frames. **15:15Z: the RetroArch series is done, `8d0dc8f255` (local)** (#1462 `7166550579`). `0011` and `0015` are upstream's now, `0012a` is new, and the other five are ported. It replays for SM8550 and H700 under `LC_ALL=C`. Its proofs come after the build. **15:19Z: the kept deletions are decided, `c2a5f85c93` (local)** (#1462 `7166653323`). The fork's `post-update` had lost 4 upstream blocks; 3 are restored, and the PPSSPP InputPlumber controls block is an open design point (merge rather than overwrite, with a VM case). **15:24Z:** the other 18 packages' patches replay on SM8550 and H700; six packages are current and spirv-headers is readable (`27e7850bd6`, local). Round branch head: `27e7850bd6`. **15:37Z: #1460 and #1456 fixed and closed** (`7c73bad693`). `rc-preflight --only packages` on the round reads only raofflineproxy as behind. **#1442 fixed and closed** (`553e0f9850`). **15:47Z: ES is a commit and level with ROCKNIX.** The pin is `409704f3ba` (its tree equals the pin's `0d852e5d…`), and the merge is `ee098b0ad` on `m7/rc-round-es-20261125`, both local.
              - **The round's ES recipe change waits on Max's publication answer.** Yes: a GitHub pin. No: a new local archive plus five regenerated `SOURCE-ACTIVATION-*.json` receipts.
              - Posted at 15:55Z as #1462 `7167420431`, through REST; GraphQL kept failing for that issue.
              - **#1442 correction (15:56Z):** `bd5e72d18c` refuses only on the Docker route. CI guards are green again (run 45649252137); the records job is red only for the owed audit.
              - **Independent next work:**
                - **raofflineproxy: ported, `e9d4eb544c` (local, 16:15Z)** on the round branch, now the round head. 40201a2a5d; the 34 patches apply at fuzz 0 with no offsets and equal the port tree; libchdr 47d794151b, rcheevos unchanged; schema note re-read (`--only proxy-schema` PASS); source tests 966 pass with the lifecycle runtime redirected. 018 regained the near-miss and account-settings tests (mutation-checked); 023 fixes upstream's image-download test; 022 cites #629, not D-RA-049, because that ID means two things (below). Scratch: `/workspace/tmp/rocknix-session/rao-port-20261125/src` (master `6d54760`); regenerator `…/rao-port-20261125-regen.py`. Still owed after the build: `ra-offline-test`, the integration and consent tests, #629's controls, and the first-open re-index time on the guest.
                - **#1463 corrected (16:2xZ):** the "next free is D-WORKFLOW-209" line was wrong; the M6 branches use 209-237. Next free anywhere: WORKFLOW 238, CLOUD 194, UI 138, RA 53, QA 65, NET 19, ROADMAP 4, INFRA 47, SYS 14, LAUNCH 9. Re-run `docs/qa-logs/2026-11-25-m7-bug-triage/register-sweep.py` before taking any ID.
                - **16:29Z, the rest of the source items are done** (#1462 `7168063923`; round head `cbfc6d4d14`, local): PPSSPP's guide-combo step restored verbatim, `1a83caf7ae` (D-UI-079; the 15:19 merge lean dropped); the menu map, `cbfc6d4d14` (ROCKNIX's two pages declared; only #1428's three cloud pages stay missing, so `menumap` fails until #1428 lands, noted on #1428 `7167946217`); GENERIC_X64 on 7.2 checked by Kconfig symbols (8 dropped, none functional; no new dependency); all 24 older upstream deletions decided ("decide the 6 older" below is stale).
                - **16:36Z: the ES local route is done (`b458f6359a`, local) and the round's GENERIC_X64 engineering build is RUNNING** (#1462 `7168264529`). ES tar `emulationstation-m7-20261125-1f85c7d82085.tar` (sha256 `3bcd1f11…`; the writer `/workspace/tmp/rocknix-session/es-archive-20261125.py` rebuilds the candidate's `6ce58c98…` byte for byte) in `conflict-resolution/.build-runs/m7-rc-round-20261125-es/inputs/es/` (read-only, keep while the round builds); receipts by `/workspace/tmp/rocknix-session/es-receipts-20261125.py`.
                  - Run `20261125T163611Z-dadd5b66` in `rocknix.worktrees/m7-round-x64-20261125` (branch `build/m7-round-x64-20261125` at `b458f6359a`), owner `conflict-resolution/.build-runs/m7-round-x64-owner-20261125/` (admission `fff0f303d5ca…`, `submit-01/`). Launch environment as item 0 below, plus `-v …/m7-rc-round-20261125-es/inputs/es:/tmp/pix-m7-es-source-delivery-20261125-01:ro`.
                  - Recorder: watch-job pid 3881939 → `<wt>/.build-runs/20261125T163611Z-dadd5b66/build.status`. Delivery: harness waiter `b6br8cfs1` (ends on `build.rc` or `died`; silent after a disconnect). **A resumed session reads `build.rc`/`build.status` first**, then `submit-01/launcher-result.json` and `tool-wrapper.rc`.
                  - First compiler of the merged `GuiMenu.cpp`, the RetroArch port and the proxy glue (no ES build root survived for `es-syntax-check`). On a failure: archive `.threads/logs` before any resume, enumerate poisoned packages, fix on the round branch, re-freeze.
                  - On success: consume the run (rc, cleanup, identity), keep `target/`, then the VM proofs listed on #1462 (no guest beside a build). H700 and SM8550 wait for the final head.
                  - **18:29Z: run 1 FAILED at [502/649], RetroArch** (0014's `task_ptr` against f726; a 114-file syntax-only check with the root's gcc-16.2.0 then found 0013's header walk), fixed in `a8c909eecc` with the series' seven stray `.orig` files removed; consumed as `FAILED-INVESTIGATED-run1.json` (thread logs in `threads-logs-run1/`). Twelve in-flight packages cleared; the worktree fast-forwarded to `a8c909eecc`. **RESUMED: run `20261125T182838Z-c32e4d89`** (admission `a137b15f…`, `admission-plan-2.json`, owner `submit-02/`), watch-job pid 3595903, harness waiter `b0zn2qhsq`. A resumed session reads its `build.rc`/`build.status` first. #1462 `7170979877`.
                  - **19:53Z: the image is BUILT and accepted at build level** (#1462 `7172905773`): run 2 rc 0 at 19:51:57Z, 649/649, `ACCEPTANCE.json`, admission consumed, outputs held. Image `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261125T182840Z.ga8c909eecc7c-from-ROCKNIX` in `rocknix.worktrees/m7-round-x64-20261125/target/` (BUILD_ID `a8c909eecc`; ES FAKE SUSPEND and proxy pixelelated detection read from it). **Next (owner OS): the VM proofs on #1462.** Read `generic-x64-vm-testing.md` first (not read this session). `ra-offline-test` earns one real achievement on the QA account per run. No guest while a build runs. Keep `target/` until the proofs are recorded (D-INFRA-036/037).
                  - **19:55Z: `tools/vm-qa` on the image is RUNNING**: run `20261125T195456Z-cb47c86a` in `m7-round-x64-20261125`, owner `conflict-resolution/.build-runs/m7-round-x64-vmqa-owner-20261125/submit-01`, artifacts dir in `ARTIFACTS-DIR.txt` there, watch-job pid 785662, harness waiter `b6sfom3kw` (session-only). On completion: read `build.rc`, the report, every FAIL (menumap's three #1428 pages are expected). Stop owned guests through `vm-pair down`/`tools/vm-stop`, by pidfile. Then the targeted proofs (`--only ra-offline --guest d`, the proxy's integration and consent tests, RetroArch's).
                  - **20:20Z: vm-qa on the round image FAILED 7 suites** (rc 1 at 20:18Z; guests stopped by `vm-pair down`). Harness gaps, not the image: menumap (the local ES version has no commit), wrapper (looks only under retired build-root paths), time-to-play (the candidate line's reservation guard wants `host-reservation.json`). To judge against a baseline: scripts (host stubs lack `/usr/bin/raofflineproxy-lifecycle`), round-trip (refused: no chosen cloud connection), walks (two cloud-folder walks' preservation witness), **exit: RetroArch never started**. **Baseline RUNNING:** the same harness on the candidate image `0a3e979e50`, run `20261125T201946Z-08ee664d`, owner `m7-round-x64-vmqa-baseline-owner-20261125`, waiter on its build.rc. A suite failing on the round but passing on the baseline is a round regression.
                  - **20:45Z: the baseline fails the SAME seven suites with identical FAIL lines**, so there is no round regression, and the candidate line fails vm-qa itself: **#1465** (M7). Both pairs are stopped. **Next (owner OS): the exit cells on a guest from the round image** (`RetroArch never started`; read `/tmp/exit-launch.log`), then the two cloud-folder walks, then the harness gaps listed on #1465.
                  - **20:49Z: #1465 checkbox 1 ticked: all seven are harness gaps** (#1465 `7174238688`). The exit cells call `runemu.sh` directly, refused since #1430 (`verified managed launch ticket required`; tickets come only through ES's process tree), so they must launch through ES's `POST /launch`. The cloud-folder walks and round-trip need a chosen and reviewed connection. Guests stopped. **Next (owner OS): #1465 checkbox 2, the harness fixes**, then `vm-qa` again on the round image, then the targeted proofs (`--only ra-offline --guest d`, the proxy's tests, RetroArch's). The new RetroArch's own start is proven only once the exit cell launches through ES.
                  - **21:05Z, after the steward's 20:51 check:** 'no regression' holds for the in-guest suites only. A true baseline (each worktree's own `last-good-scripts-test`): candidate 194 FAIL lines, round 73. Five round-only items, read against the source (#1465 `7174596548`): the 0012a order is the harness's locale; the XMB scale and 0011 checks are stale (f726 removed the function; f726 has its own poster slot); the 0018 matrix is harness (f726 no longer restores the slot from the runtime log). **F2-7 was a real defect:** the merge made `yabasanshiro-pirry-sa` (aarch64-only) the GENERIC_X64 Saturn default. Fixed on the round, `1d89461d4e` (local; the next build of the round carries it).
                  - **21:16Z, #1465 checkbox 2 in progress (round branch, local):** the exit test launches through ES (`f3bf0e90c6`; all four cells PASS on the round image, the first proof the new RetroArch runs a game). **The XMB verdict was wrong:** f726 keeps the XMB branch inline in `gfx_widgets_scale_factor()`, and my 0014 port dropped F-RW-07's fallback. Restored in `0643e6d247` with the test fixes (C-locale patch order, the F-RW-07 check, 0011 as the poster slot). #1465 `7174855360`. **Still to do (owner OS):** the 0018 matrix's link list and its runtime_file.c expectation; F2-7 on `yabasanshiro-pirry-sa`; the scripts suite's lifecycle stub; menumap reading the ES commit from the receipt; the wrapper's build-root path; the time-to-play reservation; round-trip and walks choosing a connection. Then a GENERIC_X64 rebuild at the round head and `vm-qa` again.
                  - **21:18Z:** F2-7 done (`b0f58fb1a7`; it fails before `1d89461d4e`). Next: the scripts suite's ctl cases. `raofflineproxy-ctl` `enable|disable|stop|toggle|operation` now `exec /usr/bin/raofflineproxy-lifecycle` (candidate-line design, ctl lines 270-290), so those cases need a lifecycle stub that records argv and asserts the hand-off; the lifecycle itself is proven by the proxy's VM tests. Remaining after that: the 0018 matrix link list, menumap's ES commit from the receipt, the wrapper's build-root path, the time-to-play reservation, round-trip and walks choosing a connection. Round head `b0f58fb1a7` (local).
                  - **21:24Z: #1466 filed (M7 bug).** On GENERIC_X64 the offline proxy's toggle is refused: the lifecycle owner fails 'independent owner unit not exact' (AdmissionError). This holds on the round image (the interface's `toggle enable --operation --boot` path and `enable`) and on the candidate (`enable`). The proxy never turns on, and later calls answer 75 until a reboot. New `tools/raofflineproxy-toggle-test` (`b09958c1fd`, round, local) found it. **Next (owner OS): #1466's cause**: `lifecycle_systemd.py`'s exact-shape admission against the guest's `owners/*/events.jsonl` (unit-property-shape observed vs required). Guests are stopped.
                  - **21:28Z: #1466's cause found and fixed (round `9b6e200280`, local).** Upstream's `service.d/10-rocknix-thp.conf` (dc14669f69, every device) is in every unit's DropInPaths, and the three lifecycle admissions required none. Patch 038 allows exactly that file (helper cases PASS; the 35-patch series equals the port tree). #1466 `7175068489`, checkbox 1 ticked. **REBUILD RUNNING** at round head `9b6e200280` (Saturn, XMB and 038): run `20261125T212743Z-6dd1fb89`, admission `1b314985…` (`admission-plan-3.json`), owner `submit-03/`, harness waiter on its build.rc. **On success:** consume it as before, then on fresh guests run `raofflineproxy-toggle-test`, the interface's `toggle enable --operation --boot` path, `emulator-exit-test --vm`, and `vm-qa`.
                  - **21:47Z: the rebuild PASSED and #1466 is CLOSED.** Run `20261125T212743Z-6dd1fb89` rc 0, image `0.0.1-dev+20261125T212745Z.g9b6e20028014` (038, Saturn and XMB read from it), `ACCEPTANCE-3.json`, admission consumed. On guests from it: `raofflineproxy-toggle-test` PASSED (its own fixture had written an empty `hardcore_was=`, which the lifecycle refuses; fixed), the interface's toggle path ENABLED/DISABLED, `emulator-exit-test --vm` PASSED (four cells). A refused owner holds every toggle at 75 until a reboot (FAILED is never terminal; ES loops on CHECK SETTING STATUS): **#1467** (bug, M7.P5), undecided. **0018 lost its runtime-log guard in the f726 port** (f726 restores the slot in runloop.c): restored in round `7e330ba2bc` (local) with the scripts suite's 0018 checks (blindspot 77). **Next (owner OS):** guests down (`vm-pair down`); rebuild GENERIC_X64 at `7e330ba2bc`; the auto-slot proof on a guest; the full scripts suite in the round worktree; the remaining #1465 items (lifecycle stub, menumap's ES commit, the wrapper's path, the time-to-play reservation, round-trip and walks); then `vm-qa`.
                  - **22:30Z: run 5 RUNNING at round head `43d9013c4d`** (run `20261125T222739Z-5838b4d3` in `m7-round-x64-20261125`, admission `1e70751b…`, `admission-plan-5.json`, owner `submit-05/`; recorder watch-job in its `build.status`, harness waiter `bdcwxpdg2`, silent after a disconnect: a resumed session reads `build.rc` first). Since 21:52 (round, local): 0018's runloop.c guard (`7e330ba2bc`, run 4 accepted, `ACCEPTANCE-4.json`); menumap/wrapper/time-to-play repaired (`8ca8bba3b0`, `aea84994b1`); D-LAUNCH-009 built (`044312753c`, D-LAUNCH-010); scripts suite 196→109 FAIL (`43d9013c4d`), INCOMPLETE marker (`094673fd91`). **The 21:05 'candidate 194, round 73' line above is wrong**: the round's run had stopped at F2-7 (#1465 `7176409063`). **Next (owner OS):** accept run 5 as before; guests from it (`vm-pair up`): `tools/ra-auto-slot-test --port 10022 --identity /tmp/rocknix-vm-pair/qa-key --monitor /tmp/rocknix-qemu-monitor.sock --vm`, the fresh-install mGBA record (`/storage/.config/retroarch/config/mGBA/.pixelelated-interframe-smart`), then guests down and `tools/vm-upgrade-rehearsal <candidate img.gz in m7-pc-0a3e979e-20261124/target> <run 5 tar> <BUILD_ID>`; then the 109 remaining scripts FAILs (C, D, t, CF, A; all shared with the candidate), round-trip and walks, `vm-qa`.
                  - **23:21Z: run 5 ACCEPTED; 0018 and D-LAUNCH-009/010 proven on guests; the upgrade rehearsal PASSES** (candidate image → round tar, `RESULT PASS`). `tools/ra-auto-slot-test` PASS on guest b (#1465 `7176738657`). Scripts suite 58 FAIL / 1309 PASS (#1465 `7177452835`; round head `9bd1be7fd6`, local): C 41 and CF 9 (cloud setup/sign-in, read against D-CLOUD-175 and the candidate's APIs), t 4 and D 4 (disable while a helper runs: now the lifecycle's; prove on a guest). No guests and no build are running. **Next (owner OS):** the 58, round-trip and walks (need a chosen connection), the wrapper fixture's port, then `vm-qa` on the round image; #1467's decision (a refused owner holds the toggle until a reboot). H700 and SM8550 wait for the final head.
                  - **23:35Z: `tools/vm-qa` RUNNING on run 5's image with the round head's tools** (`m7-round-x64-20261125` fast-forwarded to `9bd1be7fd6`, tools only): run `20261125T232344Z-73132244`, owner `conflict-resolution/.build-runs/m7-round-x64-vmqa-owner-20261125/submit-02`, artifacts in `ARTIFACTS-DIR-2.txt` there; recorder watch-job in its `build.status`, harness waiters on `build.rc` (session-only). Expected: menumap's three #1428 pages, wrapper exit 2 (fixture not ported), round-trip refusals (the harness writes paths outside the folder-profile API). Uncommitted on the round worktree: `c1clean` in section C (the profile store reset with the conf). **On completion:** read `build.rc` and the report, compare every suite with the 20:18 run, stop owned guests by `vm-pair down`.
                  - **00:06Z (2026-11-26): vm-qa DONE, rc 1** (#1465 `7178196392`): PASS lifetime, vocabulary, french, quoting, pair-identity, fresh, exit; expected FAIL scripts, wrapper (2), menumap (#1428); register fixed since (round `3a6f7086df`); **round-trip, time-to-play's exit sync and the two cloud-folder walks share one harness gap**: paths written to `cloud_sync.conf` by `sed` while `folder-profiles.json` holds others, so `cloud_remote active` refuses ('Review this connection') and every cloud tool says 'CHOOSE A CONNECTION'. Scripts suite 50 FAIL (round `960b5b5216`). Guests stopped. **Next (owner OS):** route `tools/cloud-round-trip`'s path writes (about 30 `sed` sites and its cleanup) and the vm-qa/time-to-play cloud setup through the folder-profile API (`cloud_setup --set-*-remote`, or conf and profile written together); then the remaining 50 (C 33, CF 9, t 4, D 4); the wrapper fixture's port; `vm-qa` again; #1467's decision.
                  - **00:37Z (2026-11-26): round-trip PASSES; Max's test request is #1470; fast mode is D-WORKFLOW-238.** Round head `174ea851a7` (local): the cloud harnesses keep the profile store in step; time-to-play's exit sync stamps; the walks' witness passes, and the two cloud-folder walks wait for #1428. #1470 (M7.P5) quotes Max's three questions and owns the plan; #1468 and #1469 (no milestone) were filed; the M6 false-pass list (about 37) is on #1470 for Max's exception choice; the plan note is in the steward's inbox. `tools/herdr-lane` passes `service_tier="priority"` per lane (verified once by `codex exec`); the w4 lanes p7 to pD switch at next dispatch with a first-turn readback. Weekly Codex allowance 100% until 2026-11-30 06:35 UTC. **Relay route (agreed with the steward): read `/workspace/tmp/rocknix-session/steward-notes/for-os/` at each push and checkpoint.** Guests a and b are up from the walks run (`vm-pair down` when done). **Next (owner OS):** #1470 steps 1 to 3 (#1465's remaining items, #1469, #1468) unless Max reorders; step 4 waits on his choice of machine.
                  - **00:41Z: #1469's verdict built** (round `385c88fc82`, local): `vm-qa` ends PASS or FAIL, a suite that cannot run fails, and known failures annotate only (`docs/qa/vm-qa-known-failures.txt`, six round entries). D-QA-065 and its practice are in `engineering-practices.md`. The M6 false-pass list (about 37) is on #1470 for Max. No guests and no build are running. **Next (owner OS):** #1469's remaining checkboxes (`rc-preflight` reads the verdict and refuses a closed issue's entry); #1468 (the map of what each test drives, and its check); #1465's remaining items. Step 4 (automatic runs) waits on Max's choice of machine; step 5 on his exception.
                  - 16:43Z: 92/649; swap back to 7/8 GB seven minutes after the reclaim, 36 GB RAM available. Watch memory at webkitgtk (capped `-j4`).
                - **17:04Z: the four NEEDS MAX notes are restated after the steward's check** (`steward-notes/20261125-afternoon-notes-checked.md`). The steward verifies each again and puts them to Max one at a time.
                  - RG SP copy: timing restated; the round leaves H700's bootloader, kernel, compiler and sleep unchanged (one source URL, two Rust-version config lines).
                  - October images: the "installed by hand" line now quotes Max's own October 25 words with their source (#1110). New scripts: whole batch `3b9a350c…` and keep-RG35XX-SP `484c36f2…`, both proven on constructed stores (#493 `7168806636`). `e076737b…` is withdrawn.
                  - mGBA: no longer a question. D-LAUNCH-009 (`2e8ff5aa7e`, under D-WORKFLOW-050) turns it into an information note. A marker beside `mGBA.opt` covers the backup-restore path (#1423 `7168840801`). **Owed (owner OS): the switch in the round plus its rehearsal seed.**
                  - M6 bugs: the list was made first (38 = 14 High shipped + 14 exposures + 10 losses; 22 with an M6 fix recorded; `docs/qa-logs/2026-11-25-m7-bug-triage/m6-bugs-for-the-call.md`, #555 `7168913158`). The note now asks for an exception to D-WORKFLOW-185, in his words.
                  - Publication: rewritten. A push of the candidate uploads 8,441 unpublished file versions (157 MB), 8,226 of them test records. The recommendation is a source-only public head, brought back to Max with its exact commit before any push. The EmulationStation push is its own line.
                  - #1458 gained a read-before-push checkbox. Today's own pushes were scanned: 0 hits for every shape in 26 QA files and 4,816 added lines, with a positive control.
                  - **17:13Z, after the steward's verification:** the October images (next after the RG SP copy) and the M6 note (third; a method clause added) are ready. mGBA goes to Max as information. **The publication note is held out of his queue: no question now.** Preparing the source-only private copy is OS work (D-WORKFLOW-184). **Next (owner OS), when the source round allows:** rebuild our commits without the test records and with corrected identities, then bring ONE question: the exact commit and what each of the two pushes uploads. Times in notes, markers and comments come from `date -u` in the writing command (#1464).
                  - **When the Nova restart question comes, it must name the PPSSPP `controls.ini` replacement** (custom mappings lost once), beside the `abl_a`/`abl_b` rewrite (steward D3).
                - **Next independent item while the build runs (owner OS): #1463's 16 M6/M7 collisions** (map and plan, #1463 `7168613055`). M7 rows take new numbers (D-INFRA-038 keeps M6 untouched). First classify every round-tree and issue citation of the 16 by meaning; only M7 citations are rewritten, each listed. Ten M7 rows exist only uncommitted in `m7-player-setup`. Do it before the candidate line is published.
                - **16:48Z: #1459 checkboxes 1 and 3 ticked** (#1459 `7168547367`): the round's AetherSX2 equals upstream's; `tools/upstream-deletion-check` (`e004ebbb14`, fork-only, in the push guard and both rule lists) passes on the merge window and, with the round's `docs/releases/upstream-deletions-kept.txt` (`51790df72a`, local; round head now `51790df72a`), since June. Checkbox 2 waits for the rebuilt SM8550 image. Run it after every upstream merge.
                - **16:43Z: #1012's runner fix merged** (#1012 `7168429537`): `next` `560188d9d4` (a content fast-forward from `a4617bfd4a`; brings #967/#971/#976/#983's time-to-play parts) and the round `80b2fd4358` (three-way, keeps the reservation guard). D-QA-062 integrated on both (`88f29a30a9`; round `cd9d5ebe80`), and D-INFRA-025/030/031 on the round (`ae4a99e358`). Round head now `ae4a99e358`; the running build is frozen at `b458f6359a` (tools and the register are not in the image). #1012's fifth checkbox waits for a qualification run. Pointers posted on the M6 issues #967/#971/#976/#983.
                Then the build set. Done already: the six small bumps and spirv-headers' `PKG_SITE`; the tool fixes #1460, #1456 and #1442; the ES commit over `16dbac5211` plus ROCKNIX's 20. Then the build set. Then regenerate the patches in name order, replay, build RetroArch, and run the VM proofs. Also still to do: replay the other 18 bumped packages with patches; decide the 6 older kept upstream deletions; check GENERIC_X64's kernel config on 7.2; then the small bumps. Contents:
            - the upstream merge (246 commits; take upstream's AetherSX2, #1459; check for undone deletions);
            - the six small bumps; the raofflineproxy decision; spirv-headers `PKG_SITE`;
            - the ES commit plus ROCKNIX's 20; #1422's quirk arrives with the merge;
            - the tool fixes #1456, #1460 and #1442;
            - #1012's runner fix onto `next`.
       - **The restart questions must name the bootloader writes** (corrected #555 `7154797416` at 11:15Z):
         - RG SP (H700): the update rewrites the card's u-boot at 8 KiB, chosen by `vdd-dram`, plus the device trees and `dtb.img`.
         - Nova (SM8550): `updateabl` flashes OpenABL 1.2 to the internal `abl_a` and `abl_b` partitions whenever they differ, and keeps no backup.
    2. A plan for step 0, with a futro.
    3. The two decisions in plain terms, queued behind the RG SP question and the October images.
- **The largest unblocked M7 item is the owed code audit** (release-candidates step 4, D-WORKFLOW-062; `ceremony-check` keeps CI red for it and for the futro). It runs through the Facilitator on OpenRouter, not Codex. Plan it with the futro before starting.

**00. Newer (2026-11-25T06:27Z).**
- **The M7 build set is built and passes on one commit (D-INFRA-043).** `tools/rc-preflight --only build-set` PASS at 05:20:42Z: SM8550, GENERIC_X64 and H700 all `0a3e979e50`. Quoted on #555 (`issuecomment-7153693555`); #1449's "The M7 set passes" checkbox ticked.
  - **H700 accepted:** run `20261125T020406Z-f7a619db` (02:04:06Z to 05:18:02Z), all result channels 0, owners exited, DDR3 `b4ff5ad3…`, DDR4 `7ae4d351…`, tar `cb705521…`. Record `m7-h700-0a3e979e-owner-20261125/ACCEPTANCE.json` and `RC-PREFLIGHT-build-set.txt`.
  - H700 roots removed at 05:23Z (+147.10 GB, `REMOVAL-build-roots.json`). Kept: `m7-h700-0a3e979e-20261125/target/` and `kept/emulationstation-m7-20261110-0d852e5d1106/emulationstation` (`62b84880…`). Logs compacted to `.zst`, the PC console log included.
  - The `ee74f157` PC worktree is gone (+7.90 GB, 05:25Z); its records are in `conflict-resolution/.build-runs/m7-pc-ee74f157-records-20261124/`.
- **The PC image of `0a3e979e50` passes its VM checks** (pB, `RESULT.json` sha256 `06283f88…`, manifest of 2,018 members verified; #555 `issuecomment-7154478975`). Checks 1 (294/294), 2a (from `672a7c995f`), 2b (from `d7ca912480ea`, the WebDAV leg on its third case) and 3 (Smart mGBA) PASS.
  - The two upgrade-start images were released and removed at 06:06Z (+12.88 GB). `KEEP-named-items.json` now holds the 13-04 store and `root02` only.
  - Nine small November 5 receipts were lost to a `find -size -1M` filter: `released-upgrade-starts/nov5-672a7c995f/LOST-RECEIPTS.md`; the lesson is in `engineering-practices.md`.
  - Open checkboxes on #1423, #1427 and #1433 are to be read against pB's receipts before any tick.
- **H700 and SM8550 host readback: PASS** (#555 `issuecomment-7154797416`; `READBACK.json` in both owner folders). Both images carry 509 dead 32-bit systemd/udev copies, noted, not a gap.
- **Waiting on Max: the RG SP copy** (NEEDS MAX `steward-inbox/20261125T0626Z-rg-sp-first-copy.md`, also on #555). Max said at 06:13Z he will get a device ready when told which; that is not a yes.
  - On the steward's relayed yes: read the RG SP first (boot id, build, idle, the update queue, auto-sync, through the read filter).
  - Then copy the H700 tar (`cb705521…`) to a staging folder, verify the hash on the device, and move it into `/storage/.update`, all through `tools/device-act`.
  - Then put the restart as its own NEEDS MAX. The Nova follows.
- **#1454 (bug, M7):** the game-exit QA case's frame-review deadline. It must close before the next PC VM run and before any RC call.
- **The shared Codex weekly allowance is 85% used, reset 2026-11-30T06:35:50Z.** Every Codex lane on the account draws on it, another project's included. Overnight, 12 of 14 points went while only that project's lanes ran. Read it from `~/.codex/sessions/**/rollout-*.jsonl` (`rate_limits.primary.used_percent`).
  - Order: no other M7 Codex dispatch until pB reports. The H700/SM8550 qualification preparation runs in this lane.
  - The steward has the finding (sent into `w4:pF` at 05:33:43Z, before D-WORKFLOW-205 stopped pane delivery). Only Max can add allowance.
- **Never stage `docs/coordinator-one-on-one.md`** (the steward's agenda, with their uncommitted edits) on any branch until the steward says so. #1451 criterion 3 is held for that; criteria 2 and 4 are this lane's.
- **#1451 criterion 1 is committed locally as `4badc4e6c0`** (the five coordination tools, tests 31/21 OK). Push it with the next material batch, then tick it.
- **CI is back (#1446 closed).** Max re-enabled workflows at about 02:58Z. The first runs on `next` (`d5d8e07350`) were the wordlist check in 53 s, green (`45537101984`), and the record checks (`45537101977`), red only for the audit and futro owed. `tools/ci-silence-check` passes live.
  - #1441 is closed. #1450 waits only on criterion 4, the daily timer, which needs #1451.
  - Branches that have not merged `next` keep the old four-minute scan; the one-line fix is on #1446. The M6 lane is not messaged.
  - Owed: the code audit and the futro (`ceremony-check`). They keep `fork record checks` red by design.
- **The /tmp scratch removal is done (D-INFRA-046).** Max said yes at about 03:53Z. 267 entries were removed in two passes: the second for two read-only evidence folders, kept in `20261125-tmp-m7/kept-records/`. 4.85 GB of `/tmp` was freed. Outcome on #493.
- **Alerts (#1452, D-WORKFLOW-203/204): scoped, not built.** Build results go by email from the build account's Hostinger mailbox, sent by the finished build's watcher; breakage goes to SkyWalking or another open-source tool over OTLP; everything else waits for the watcher agent. It waits on a refreshed mailbox credential and a destination address from Max. The address goes in a private file only, never the tree, tracker or commits.
- **Push cadence:** each push of `next` is two workflow runs. Batch records into one push per material outcome, and mirror this checkpoint to the feature branch only at a handoff.
- **Nothing goes into the one-on-one pane `w4:pF` (D-WORKFLOW-205, #1453; Max, 05:34Z).** No `herdr agent prompt` to it, no messaging-tool message to the steward's session, and no escalation delivery aimed at it.
  - A notice for the steward is one file in `/workspace/tmp/rocknix-session/steward-inbox/` (mode 700), named `<UTC time>-<slug>.md`, with a first line of `NEEDS MAX`, `STOPPED WORK` or `INFORMATION`.
  - A `NEEDS MAX` or `STOPPED WORK` notice also goes on its issue: nothing wakes a closed steward session.
  - Max still answers only in the one-on-one, and the steward relays his words here (D-WORKFLOW-201). The earlier by-pane rule (#1447) is reversed.
- **Batch 6's ten leftovers are removed (D-INFRA-045)**, +26.26 GB. The 13-04 store and `root02` are named keep items.

**0. Latest (2026-11-24T23:05Z; supersedes the running/next parts of items 1, 2 and 4 below).**
- **SM8550 of `0a3e979e50` is accepted.** Run `20261124T184914Z-84d3f121`, rc 0; record `m7-sm8550-0a3e979e-owner-20261124/ACCEPTANCE.json`; #1448 criteria 1–3 ticked.
  - Its build roots were removed (+183.41 GB, `REMOVAL-build-roots.json`).
  - Kept: `m7-sm8550-0a3e979e-20261124/target/` and `kept/emulationstation-m7-20261110-0d852e5d1106/emulationstation` (sha256 `edcb8d26…`).
- **The PC cold build of `0a3e979e50` is running.** Started 22:54:54Z: run `20261124T225454Z-289bae16` in `/workspace/repos/rocknix.worktrees/m7-pc-0a3e979e-20261124` (branch `build/m7-pc-0a3e979e-20261124`), owner `conflict-resolution/.build-runs/m7-pc-0a3e979e-owner-20261124/`, watcher pid 1774390, job 1774384.
  - Consume it from `build.rc`, `runner-result.json`, `submit-01/launcher-result.json` and `tool-wrapper.rc`, then check process cleanup, the identity file and both hashes.
  - Then remove its build root, keeping `target/` and the unstripped ES binary.
  - Then H700 cold from the final head, last; then `tools/rc-preflight --only build-set` over the three `target/` folders.
- **Batch 6 is done** (D-INFRA-044): rc 0, +489.74 GB, outcome on #493.
  - 26.6 GB remains in `/workspace/tmp` outside the keep set: 11 git object stores and 2 held entries (`batch6-left-not-keep.txt`).
  - Removing those deletes more than batch 6 did, so it goes to the one-on-one first.
  - `KEEP-named-items.json` now names the set's final head in its release events.
- **CI (#1446, #1450).** Max set Actions budgets at about 22:37Z; a push at 22:38Z still got no check suite, so the budgets did not restore CI. Owner-only pages remain unread (Actions policy, audit log, payment).
  - #1450 (Max's *"why'd this go unnoticed?"*): on `next` and pushed in `4eb89d2e4c`, `f7f7755e8b` and `95e97bb50f`.
    - `tools/ci-silence-check`.
    - The push guard prints it for every push of `next` (criterion 2 ticked).
    - `rc-preflight --only ci` (D-WORKFLOW-202, criterion 3 ticked).
    - `fork-checks.yml` split into `guards` and `records` jobs.
    - Criteria 1 and 5 wait for a live run after Actions returns.
  - The daily timer (criterion 4) is blocked by #1451: `tools/coordinator-escalation`, `tools/m7-lane-watch` and `tools/priority-check` were never committed to any branch, and the rule text naming them is uncommitted in this worktree. Integrating them is coordinator work, and it comes next once the PC build is consumed.
  - Swap refilled to 7 of 8 GB within ten minutes of the 22:5xZ reclaim, with about 38 GB of RAM available. Watch the PC build for memory pressure.
  - Note: `0a3e979e50` is not on GitHub at all (`check-suites` answers 404), so the M7 head has never been checked by CI.

**1. The SM8550 cold build of `0a3e979e50` is running (#555, #1448).** `0a3e979e50` = `ace312b0d2` with `fex-emu`'s fork patch `0006` deleted. Upstream's `0003` in the November 18 tree already carries its change, so `0006` stopped the first SM8550 run at `[706/736]` unpack. Kept as `refs/m7/candidate-0a3e979e`. **Image heads (D-INFRA-043, #1449, reverses D-INFRA-042):** the whole M7 set comes from one commit with one build ID, now `0a3e979e50`. Max at about 19:21Z: *"make sure we institutionalize it and store that as our preference"*. SM8550 continues; the PC is rebuilt cold from `0a3e979e50`; H700 is rebuilt cold from the final head last. If a fix moves the head again, the not-yet-built targets take the new head and the built ones are rebuilt last. `ace312b0d2` stays `refs/m7/candidate-ace312b0`.

- **H700 of `ace312b0d2` is released (D-INFRA-043).** It was built and verified (run `20261124T122752Z-42bd4e9d`, 672/672, 32-bit yabadabadoo core shipped, #1441 criterion 2 ticked from it). Its build roots went at 16:00Z (+145.5 GB). Its `target/` worktree and the unstripped ES binary went at 19:26Z (+6.95 GB net, `REMOVAL-images.log`), because these images are no longer the ones to qualify. Its records, image hashes and `build.log.zst` are in `m7-h700-ace312b0-owner-20261124/` (`ACCEPTANCE.json`, `RELEASED.json`, `runs/`).
- **SM8550.** Worktree `/workspace/repos/rocknix.worktrees/m7-sm8550-0a3e979e-20261124` (branch `build/m7-sm8550-0a3e979e-20261124`).
  - Owner records: `conflict-resolution/.build-runs/m7-sm8550-0a3e979e-owner-20261124/` (plans, report, admission `9d93d899cd2b492c8568531841d0a0ec`, `submit-01/`).
  - Run `<worktree>/.build-runs/20261124T184914Z-84d3f121`, started 18:49:14Z after the guarded swap reclaim (8 GB used to 0). 258 ARM tasks, then about 736 aarch64.
  - The first run, `20261124T155230Z-1d5546ee` of `ace312b0d2`, is consumed as failed-investigated (`m7-sm8550-ace312b0-owner-20261124/FAILED-INVESTIGATED.json`; worktree removed, +148.44 GB). Its earlier refused launches are in `REFUSED-BEFORE-COMPILE.json` there.
  - Before the relaunch, the patches of the 15 unreached packages no build of the head had unpacked were replayed against pinned sources: 43 applications, 0 failures (`/workspace/tmp/rocknix-session/patch-replay-sm8550.sh`, seen to fail on the old `fex-emu`).
- **Delivery.** A harness waiter (`bvrffk3mf`) is on `build.rc` while this session is connected. Nothing alerts after a disconnect. A resumed session reads `build.rc`/`build.status` first. The container's processes show the alias path below as their cwd, not the real worktree.
- **Launch environment** (for the PC rebuild too):
  - `export PROJECT=ROCKNIX DEVICE=<D> ARCH=<last ABI>`. This is needed for two-ABI admissions (#1442).
  - `DOCKER_WORK_DIR=/workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/m7-candidate-build-20261118-01/checkout`. This is the EmulationStation recipe's fixed custody root.
  - `DOCKER_EXTRA_OPTS="-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v /workspace/cache/rocknix-sources:$DOCKER_WORK_DIR/sources -v <that root's parent>/inputs/es:/tmp/pix-m7-es-source-delivery-20261110-01:ro -e TMPDIR=/tmp"`.
  - The admission plan's `container_checkout` is the same alias.
- **Launch sequence:**
  1. `tools/fork-worktree add-build <name> <commit>`
  2. `mkdir -m 0755 <wt>/sources`
  3. the retention report (`tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report ...`); first check that every `protected` path still exists
  4. `build-admission prepare`
  5. `tools/build-preflight --reclaim-swap 2>&1 | tee <owner>/PREFLIGHT-reclaim-swap.txt` (the record lives in the owner folder, not only the terminal; #555, 23:08Z). Remove `/tmp` (tmpfs) leftovers first: tmpfs pages refill swap within minutes of a reclaim.
  6. `tools/watch-build-submit --owner <owner>/submit-NN -- --admission <admission> -- make docker-<D>`
- **Run the launch under `set -o pipefail`, with an explicit stop after each step.** Check for a running build with `ps -C make -o args=`, never `pgrep -f` (it matches the launching shell). SM8550's gated command is in this session's transcript at 15:52Z.
- The first H700 attempt from `d86c089eab` (run `20261124T100549Z-8b97f52f`) is consumed as failed-investigated (`m7-h700-d86c089e-owner-20261124/`).

**2. Then, in order (D-INFRA-043):** (a) the PC (GENERIC_X64) cold from `0a3e979e50`. Before launching it, remove the SM8550 build roots and generated caches after the use check, and keep SM8550 `target/` and its unstripped ES binary (`emulationstation-*` under `build.pixelelated-SM8550.aarch64/build/`) as named items. Its patches are proven: the `3258f06c09` cold build differs only in the ES custody binding, the yabadabadoo path and `fex-emu` (not built on x86). (b) H700 cold from the final head, last; before it, remove the PC build roots and keep the PC `target/`. (c) `tools/rc-preflight --tree <final-head worktree> --only build-set --build-set <SM8550 target> --build-set <PC target> --build-set <H700 target>` must PASS; quote it on #555. (d) The PC clean-install and upgrade checks on that PC image, dispatched to a worker lane (as pB ran them on `3258f06c09`), from `672a7c995f` with `d7ca912480ea` as a second start; no guest runs beside a cold build. (e) H700 and SM8550 qualification. Builds run one at a time. Before each: recheck free space and swap, and reclaim swap only while no guest or compiler runs. A fix that moves the head again: not-yet-built targets take the new head, built ones are rebuilt last, and their VM checks rerun.

**3. Evidence already in hand.** The PC image of `ee74f157` (build commit `3258f06c09`; `m7-pc-ee74f157-20261124/target/`, img.gz sha256 `91a364aa…`, tar `c6d753a8…`) passed pB's VM checks: 294/294 clean first boot, an upgrade from keeper `d7ca912480ea` with game-exit backup and slot restore, and the Smart mGBA default (`m7-source-delivery-20261103/docs/qa-logs/2026-11-24-integrated-pc-vm/RESULT.json`, sha256 `409ab8d7…`). It is early evidence only, because it is not the candidate head. Its run `20261124T050615Z-8fd0015c` is consumed as qualified (12:3xZ). That image is the kept warm base until the next build supersedes it (D-INFRA-037).

**4. Cleanup (#493, D-INFRA-035/036/037/038).** 2.250 TB free on `/workspace` at 12:40Z, after batch 5 (+251.16 GB: both GENERIC_X64 build roots, the earlier PC root and the November 21 keeper root, the two gtk4 worktrees, `rc-device-fixes` roots and the `/tmp` policy worktree; `20261124-post-h700-pass/batch5.log`). The keep set is now the running SM8550 build of `0a3e979e50` (the H700 images of `ace312b0d2` were released at 19:26Z under D-INFRA-043), plus `m7-pc-ee74f157-20261124/target` (pB-qualified images, released when the PC image of the final head exists) and `m7-generic-post-release-boot-owner-20261122-03/boot-output/` (the d7ca image and `reader.raw` the PC upgrade check reads, released when that check passes on the PC image of the set's final head). Batches 1–4 and two compactions are done; records in `docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/20261124-october-roots/`. **Deferred and now unblocked** (pB's VM qualification has ended): finished QA disks and extracted firmware, `/workspace/tmp` scratch and staging under `/workspace/artifacts`, largest first. Exclude the M6 directories (`/workspace/tmp/m6-coordinator`, `/workspace/repos/pixelelated/distribution.worktrees`, any `m6-*`), `/workspace/tmp/rocknix-session`, git object stores referenced as alternates (a `find` for `objects/info/alternates` under `/workspace/repos`, `/workspace/artifacts` and `/workspace/tmp` returned no paths, but it ran under a 300 s timeout and may have been cut short, so it is not conclusive; e.g. `/workspace/tmp/pix-m7-november-textual-merge-20261113-04` is a known store), files with more than one link, the running build's inputs (`m7-candidate-build-20261118-01/inputs/es`, the sources cache) and the keeper. Also the RAM-backed `/tmp` (tmpfs, 31 GB): about 12 GB of leftover session directories (`m7-493-*`, `pixelelated-policy-20261119`, `m6-assess-*` (M6-owned, leave), `pix-*`, `m7-es-handheld-activation.*`). The November 21 keeper's build root (`m7-ntfs-source-candidate-20261121-01/checkout/build.*`) is already gone (batch 5); its checkout's `.git` and update tar remain.

## Open items owned by OS

1. **No GitHub Actions workflow has run on the fork since 2026-10-29** ([#1446](https://github.com/pixelelated/distribution/issues/1446)). The November 18 and November 24 pushes started none, and the build host's token cannot read the Actions settings (HTTP 403). Every CI guard is silent, including the #1441 DISTRO step. Needs someone with org or repo Actions and billing access. The steward put it to Max in the one-on-one at about 14:47Z; wait for the relayed answer there (D-WORKFLOW-201).
2. **Batch 6 (`/workspace/tmp` compaction) awaits Max's yes.** Claude Code's auto-mode review refused the first version at 12:49Z and nothing ran (`20261124-post-h700-pass/REFUSAL-batch6.json`). After the steward's read-only preview (7,824 files, about 496 GB in 482 of 2,177 entries), the script was revised at about 12:56Z:
   - the November 5 PC image folder is a named keep (`KEEP-named-items.json`);
   - pictures are kept as frames;
   - `held.py` re-checks holders right before each entry's deletion.
   The new script sha256 starts `f06842247be9d0c0` and `held.py` starts `d4cfa4d580150a75`. The fixture run passed. The steward put it to Max in the one-on-one at about 14:47Z. Do not start it until the steward relays his exact yes (D-WORKFLOW-201, #1447). Then submit exactly that script. If the review refuses it again, send the refusal back to the one-on-one unchanged. /workspace/tmp will not be at the keep set afterwards: small generated output stays. The `/workspace/artifacts` pass (candidate stores, build custody, release sources) has not started and needs per-item review, because D-INFRA-033 holds a deliverable missing from GitHub.
2a. **The PC upgrade check on the PC image of the set's final head (D-INFRA-043; `0a3e979e50` unless a fix moves it) starts from `672a7c995f`** (November 5 PC image, the build on the RG SP and the Nova; the RG35XX SP still runs the October 7 build `43d0bc3bf4` by the device action log, #1455; `release-candidates.md` step 3), with `d7ca912480ea` as a second starting point (#555 comment).
3. `next` was pushed at 12:47Z (`9a51171c34..29bc9fd857`) and 12:51Z (`..6e30af8fac`); `ceremony-check --gate` prints no BLOCK line. The audit and futro ceremonies remain overdue (CI-red only). The retro is `docs/retros/2026-11-24-m7-cleanup-and-build-restart.md`.
4. **The lane observer is down** and its config pins the old Codex root session `01a0faa5-…`. The human-escalation config pins the old steward session `01a1e512-…`. Re-pin the observer before relying on it. The escalation tool must deliver to the steward's inbox or make no human delivery, never to `w4:pF` (D-WORKFLOW-205, #1451).
4a. **The P3 Tiny becomes the dedicated build machine, serval the development machine, once it is set up (D-INFRA-041, #1419).** Max is building its rack, and no date is set. The M7 build set stays here meanwhile. #1419 holds the first-build checklist. Copying `~/.ROCKNIX/options` there needs Max's yes, through the one-on-one.
5. Open issues from today: #1441 (criterion 3, waits on CI), #1442 (two-ABI admission), #1444 (criterion 3), #1445 (one command for the build route; a failing-step criterion added after the SM8550 launch), #1449 (one build set, one commit: criteria 1–3 done on `next` in `64986c543f`; 4 is the M7 set PASS; 5 is the #1445 criterion), #1448 (criteria 1–3 read from the running SM8550 run; criterion 4 is promoting the patch replay into a tree tool in the build route, #1445; criterion 5 is `next` dropping `0006` when it takes upstream's recipe). #1443 is closed. `tools/build-preflight`'s guest check is anchored on `next` (`6957ae9029`); build worktrees cut from `ace312b0d2`/`0a3e979e50` still carry the unanchored one, so keep the emulator's name out of a launch command line.
6. **#1447: Max speaks in one place (D-WORKFLOW-201).** Every question for Max goes to the one-on-one, never into this tab. The rule landed on `next` in `3aab3ee850` (pushed at 14:52Z). Still open: integrate or retire the rest of the uncommitted lane text in this worktree. That is the D-WORKFLOW-183/184/187/189/190/194/195 sections of `engineering-practices.md`, the 441-line `docs/coordination-continuity.md`, `docs/coordinator-one-on-one.md`, `tools/coordinator-escalation` and `tools/m7-lane-watch`.

## Files and ownership

| File or record | Purpose |
| --- | --- |
| `.github/sessions/saved-session-state-next.md` and the feature-branch selector | Link to this file and the steward's checkpoint. |
| `.claude/skills/build-cleanup/SKILL.md` (on `next`) | Cleanup procedure: delete is the default; keep one build, source, the download cache and compact records. |
| `docs/decision-register.md` (on `next`) | D-INFRA-035–040, D-WORKFLOW-200. |
| `docs/work-logs/2026_11-work_logs/2026_11_24-work_log.md` | 04:45Z cleanup entry; 12:33Z #1441 entry. Untracked here, committed to `next` by content in `1272656075`. |
| `.github/workflows/fork-checks.yml` (on `next`) | The DISTRO build-root guard (#1441). |
| `tools/herdr-lane` (on `next`) | Role selects harness and tier; refuses a Codex coordinator or steward. |

The worktree also holds unrelated modified instructions, package recipes, scripts, logs and untracked evidence from earlier sessions. Commit only the paths you own. Use the session-resume skill with the role **OS work coordinator**.

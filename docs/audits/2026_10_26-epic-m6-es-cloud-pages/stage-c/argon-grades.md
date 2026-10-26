### Gemini 4 Argon (`gemini-argon`, `google/gemini-4-argon`, `high`): 45 items, graded

**The calls:**

- Call 3, the probe: 10:49:58 to 10:50:05 UTC, PASS.
- Call 4, the refutation: 10:50:15 to 11:06:02 UTC, 36,980 bytes. **Its first attempt returned empty content** (`finish=error`, `retry(empty_content)`, after 396 s). The invoke's one allowed retry succeeded, `finish=stop`, still within the one keyed call.
- Both were served `google/gemini-4-argon` by Google (`stage-c/provenance-read.txt`).
- Argon's brief was the packet with `{PREFIX}` as R, plus the grades of Astra (357,825 bytes).

Each item was re-read at its lines before it was graded (`stage-c/rereads/`), in the same words as Astra's table.

| Item | Grade | The lane's re-read, and where it lands |
| --- | --- | --- |
| R-1 | accepted, narrowed | `case Doing:` does not clear `mCurrent`, `mChecksTotal` or `mListed`, which outrank `mDoing` on row 3 (`GuiCloudTransfer.cpp:946-1035`). A `doing` after rclone ran within the same unit shows stale rclone state; every producer at `8ebaf8daad` announces its `doing` after a fresh `>>> unit`, so it is latent. The empty `>>> why ` becomes `Unknown` after `cleanLine`'s trim, but both readers ignore an empty why anyway (`CloudTransferJob.cpp:284`), so it changes nothing: `:284` is unreachable. PL-13. |
| R-2 | accepted | As A-1. |
| R-3 | accepted | As A-3. |
| R-4 | accepted, extended | A second `>>> pid` that is junk or `0` overwrites a good pid with 0 and disarms a later stop (`CloudTransferJob.cpp:157`, `ThreadedCloudSync.cpp:816`). It is latent, since only the wrappers print the line (P14). PL-13. |
| R-5 | accepted, narrowed | The 1,024 cap drops characters and can hide a glued `Transferred:`. On A-35 the seat says "more than merely plausible": the code's own comment (`:645-647`) says the block ends without a newline, but says nothing of rclone's last block at exit. The grade stays plausible until the fixture (PL-19). |
| R-6 | accepted | `atol` in the count line can double-count a unit's files after a torn line (`CloudTransferJob.cpp:425-428`). Latent. PL-13. |
| R-7 | accepted | As A-7: `lock` and `job` dangle across `:328-343`, unused. No use after free. |
| R-8 | accepted, narrowed | Four parts. (1) and (3) are A-33 and A-34. (2): after `mInstance` is cleared (`:716-720`) a launch is allowed during the linger, and then `CloudOffer::present` (`:741`, completed runs only) and `ProxyCards::afterSync` (`:754-755`) run over a game that has started. `afterSync` (`ProxyCards.cpp:543-551`) has no running-game guard; whether `batch()` defers is the offline achievements slice's. (4): `mPid`, `mWaitingForNetwork` and `mCancelled` are `std::atomic` (`ThreadedCloudSync.h:149-151`, in the lane's read). The cached-pid SIGKILL is A-8. Mostly accepted; "refuted" is too strong for a design that holds where it is atomic. PL-18. |
| R-9 | accepted, extended | A stale `<stamp>.tmp` left by an earlier failed write is renamed over the stamp when the next `fopen` fails, a case the lane did not name. PL-01. |
| R-10 | accepted | As A-11, citing D-CLOUD-109 and D-CLOUD-129's visible wait. PL-15. |
| R-11 | accepted, **new** | The job's own window: `pclose` (`CloudTransferJob.cpp:679`) reaps before the lock at `:684`. A stop in that window marks a run that **failed** on its own (5, 69, 75) as stopped, because `:691` clears the stop flags only on 0 or 9, and the real outcome becomes `SKIPPED - YOU CANCELLED IT`. "Refuted" is right about the lane's "every race closed": the named races are closed and this one is not. PL-18. |
| R-12 | accepted | As A-13 and A-16. The 48-character scan candidate that fits beside the 36- and 43-character `NOTHING NEW` forms is an inference about one font, not a frame. PL-05 stays as written. |
| R-13 | accepted | As A-12. |
| R-14 | accepted | As A-14. |
| R-15 | accepted | As A-15. The sentinels `whyForCode` handles (69, 75, NoFolder) are in § The protocol's exit rows, not the fallback map's comparison. |
| R-16 | accepted, narrowed | The emitter table omits three rows that no test reaches through the protocol: `CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.`, `YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` and `YOUR CLOUD FOLDER COULDN'T BE READ` (`git grep -c` in `CloudTextTests.cpp`: 0 each). `YOU WENT OFFLINE PART-WAY THROUGH` is a stamp's why and has its own case (`:747`; 12 mentions). That is why A-36 passed the tests. PL-03. |
| R-17 | accepted | As A-17, with the omitted rows of R-16. |
| R-18 | accepted | The untested list grows: the page formatter's torn fields and its four-byte separator check, the unfitted rows, normalization round-trips, a glued `>>> `, and the card's three races. PL-14. |
| R-19 | accepted | As A-2 and R-4. |
| R-20 | accepted | As A-29. |
| R-21 | accepted | As A-1. |
| R-22 | accepted | As A-4. |
| R-23 | accepted | As A-18. |
| R-24 | accepted | As A-30, with R-9's stale temporary. |
| R-25 | accepted | As A-11 and A-42. |
| R-26 | accepted | As A-31: the preview's plan is spent too, so the next match must check again. |
| R-27 | accepted | As A-13. |
| R-28 | accepted | F-10 confirmed. |
| R-29 | accepted | As A-32 and A-36. |
| R-30 | accepted | F-12, with R-16's rows. |
| R-31 | accepted, narrowed | `ThreadedCloudSync.h:158-159` and `shortenWhy`'s body (`CloudText.cpp:371-386`) are in the lane's read: both hold. |
| R-32 | accepted | F-14, with codes 6 and 10. |
| R-33 | accepted | As A-16. |
| R-34 | accepted | F-16; the census is P13 and P14. |
| R-35 | accepted | As A-27; `nextTime` is P12. |
| R-36 | accepted | As A-28. |
| R-37 | accepted | F-19; `jobs-tests` ran here (6 PASS). |
| R-38 | accepted | F-20 confirmed at its lines. |
| R-39 | accepted | The details of R-8: (1) is A-33's window and the SIGTERM to a reaped group; (2) is the linger's launch and `afterSync`. PL-18. |
| R-40 | accepted, **new**, latent | Both readers decide COMPLETED from the last code (`ThreadedCloudSync.cpp:494`, `GuiCloudTransfer.cpp:435`) without asking whether a tier failed. The card's `badTiers` drops each tier's code (`:482-483`), so a failed tier with no why gets the last command's phrase. The composers propagate a failure unless a 9 follows it: `main.cpp`'s startup composer exits the restore's code first (`[ "$_r" != 0 ] && exit "$_r"`), so a restore's 9 hides the backup's failure. Latent with A-38 (no script passes `--error-on-no-transfer`). PL-21. |
| R-41 | accepted | As R-11. PL-18. |
| R-42 | accepted, **new**, confirmed | `cloud_content_backup` and `cloud_content_restore` exit 69 after progress with only a stamp and no `>>> why` (`:336-342`, `:391-397` at `8ebaf8daad`). The page reads COULDN'T FINISH (progress), but `run()` leaves 69 out of its fallback (`CloudTransferJob.cpp:721`) and never reads `offlinePartWayWhy` as the card does (`ThreadedCloudSync.cpp:509-511`). So line 4 is blank under COULDN'T FINISH: no why, against D-UI-028. `cloud_content_restore:372` says "the page reads a 69 after progress the same way"; it does not. PL-22. |
| R-43 | accepted, **new**, confirmed | `CloudTransferJob::mWhy` is written (`:286`) and never read (`git grep -w mWhy` in the job and the page: one write, one declaration), against its comments (`:244`, `.h:173`). The no-tier fallback copies pending whys without the tier arm's de-duplication and drops them when an earlier tier failed. Every composer echoes a tier after each part, so the second half is latent. PL-23. |
| R-44 | accepted | As R-16. |
| R-45 | accepted, narrowed | It confirms A-33 to A-42. On A-41 and A-42, which are about the first reader's own claims, the seat agrees. A-39: of `backuptool`'s rows (`CloudText.cpp:437`, `:448-453`, `:461-465`), those printed only by `backup` are unreachable from the backup chain. PL-17. |

**Counts:** 45 items, all accepted, 0 rejected. Of these, R-1, R-4, R-5, R-8, R-9, R-12, R-16, R-31 and R-45 are narrowed or extended. Five are new to the lane: R-1's stale row and R-4's pid zero (both latent), and R-11/R-41, R-42 and R-43, which are confirmed. R-8 and R-39 add the linger's launch to A-33. One grade stays with the lane: A-35/R-5 remains plausible until its fixture.

# The lane's grades of Gemini 4 Argon's 25 items (T20, #667)

Argon read the same packet plus the grades of Astra's 55 (`astra-grades.md`). Each item was re-read at its lines at the pin (`16dbac5211`) or the ctl (`8ebaf8daad`) before it was graded; the grades mean what they mean in `astra-grades.md`.

| Item | Grade | Re-read and consequence |
| --- | --- | --- |
| R-1 | accepted | Agrees with A-1, A-27 and A-49 (L-04). The stale comment at `RetroAchievements.cpp:173` ("Use empty UserAgent with doRequest.php calls") contradicts `getHttpOptions()` being used for `dorequest.php` calls; added to L-04. |
| R-2 | accepted | **L-01's fix:** `HttpReq` already carries `options.dataToPost` (`HttpReq.cpp:165-170`). Whether retroachievements.org's `dorequest.php?r=login` accepts the credentials in a POST body is outside this tree, and is the stream's first question (A-24's caution). |
| R-3 | accepted | L-02. |
| R-4 | accepted | L-03 as A-4. Also curl's message on the account page through `getLoginErrorMessage` (`RetroAchievements.cpp:165`, `:737`; `GuiRetroAchievements.cpp:44`). |
| R-5 | accepted | Agrees with A-5 and A-11. Adds that `mapfile -t` (`:1707`) splits only on `\n`, so a name with a CR survives into the `game` line. |
| R-6 | accepted | L-06 Low on the image. |
| R-7 | accepted | Agrees with A-9 (77 and 78 reach the page through TRY AGAIN) and A-54 (the top-up adopts a scan's progress and stamp: neither `route` nor `topup` is checked, `ProxyCards.cpp:274`, `:314-320`). |
| R-8 | accepted | L-07 narrowed and L-09 widened, as A-10 and A-8. |
| R-9 | accepted | L-21, with A-13. Adds the one-game normal queue whose ROM is not in the library (no recovery write) as a second short-queue case. |
| R-10 | accepted | L-22 and L-26, as A-45 and A-50. |
| R-11 | accepted | As A-14. |
| R-12 | accepted | L-13. The fix in `skipUtf8Bom` (`file.clear()` before `seekg(0)`) repairs `readAllText` and `readAllLines` alike. |
| R-13 | accepted | L-15 and L-16. |
| R-14 | accepted | L-14 as a state-coherence defect, as A-19. |
| R-15 | accepted | L-24. |
| R-16 | accepted | Agrees with A-21 and A-22. |
| R-17 | accepted | L-25, as A-23. |
| R-18 | accepted | L-01 to L-06 rulings. **L-04** is Low/Info. |
| R-19 | accepted | L-07 to L-11 rulings. **L-10's fix:** take `>>> pid` once, while `mPid == 0`, and require it above 1. |
| R-20 | accepted | L-12 to L-18 rulings. |
| R-21 | in part | L-19, L-21 to L-25 accepted. For L-20 the seat keeps Medium for the screen; the lane keeps **Low**, as A-43, because the dialog is reached only by a non-silent run with the library failing and the cause stays in the log. Recorded as a disagreement. |
| R-22 | accepted | **New, L-30.** When `getCheevosHashes()` returns an empty map without throwing (a 200 with a captive portal's HTML or bad JSON, `RetroAchievements.cpp:873-877`, `:898-902`), the constructor posts the offline card and sets `mTotal = 0`. `start()` then shows `NO GAMES FIT THAT CRITERIA.` on a non-silent run (`ThreadedHasher.cpp:383-390`), a sentence that is false there. Low. |
| R-23 | accepted | Joins **L-28**: `response` and `mdlist` are used as objects without `IsObject()` (`:879-880`, `:904-905`), and `Token` and `Error` without `IsString()` (`:1055`, `:1064`). |
| R-24 | accepted | **New, L-31.** `offlineScanStart` saves `SystemConf` (`GuiRetroAchievementsSettings.cpp:321`) while the parent page's save, which clears or replaces the token, has not run (`:743-807`). An edited username is written to `system.cfg` beside the previous account's token, and the scan runs with that pair. Low; the parent's close puts it right. |
| R-25 | accepted | Confirms **L-29** (INDEXING COMPLETED after a stop, `ThreadedHasher.cpp:146`). **New, L-32:** the game page prefixes a message already in the player's words with `AN ERROR OCCURRED` (`GuiGameAchievements.cpp:41-42` over `RetroAchievements.cpp:507`, `:513`). Low. |

**Totals:** 25 items. 24 accepted, 1 in part (R-21, on L-20's severity), 0 plausible, 0 rejected. New leads: L-30, L-31 and L-32; R-23 joins L-28.

**Where the two seats agree with each other and against the first reader:**
- L-03 narrowed (A-4, R-4);
- L-10 raised to Medium (A-11, R-5);
- L-09 widened to the pin (A-8, R-8);
- `scan`'s 77/78 reachable through TRY AGAIN (A-9, R-7);
- L-07 narrowed to `ready=unknown` beside a numeric `added` (A-10, R-8);
- L-21 widened to the constructor's own `push_back` (A-13, R-9).

**Where they disagree:** L-20's severity. Astra lowers it to Low, Argon keeps Medium for the screen; the lane keeps Low.

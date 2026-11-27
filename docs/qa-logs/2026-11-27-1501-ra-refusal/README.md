# #1501 and #1502: an offline achievements refusal on the scan page

Proof packet for [#1501](https://github.com/pixelelated/distribution/issues/1501) and [#1502](https://github.com/pixelelated/distribution/issues/1502), 2026-11-27. The canonical reference is `docs/es-menu-map.md` § RetroAchievements (our rows). The frame index is `evidence-index.json` (schema 1).

**Source:**
- the round `a2e853e14c` (build 22), with EmulationStation `480efb93d` (route 12, `m7-20261126-1004de647320`);
- the image `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261127T091044Z.ga2e853e14cb9-from-ROCKNIX`.

This is the state **before** the fixes. The fixes are ES `57a2357d3` (#1501) and the ctl change (#1502), which ride route 14.

**Guest:** a QA guest from that image at 640x480 (`VM_RES=640x480 tools/vm-pair up`, guest a), with ROMs from `tools/cloud-test-backend seed-device`.

**Can this be done on the VM?** Yes. No real account or service is used:
- `fixture/standin.py` is a loopback RetroAchievements stand-in on the guest. It answers every request with one status: 401, a refused sign-in, or 503, a server that cannot answer.
- `fixture/ra-refusal-guest.sh` points the proxy's `upstream_host` (its `config.json`) at the stand-in.
- It sets a synthetic account, `QA1501`, in one of two ways:
  - `token`: a local token, which is what EmulationStation's own sign-in leaves;
  - `password`: a password with no cached sign-in.
- It turns the proxy on.
- The ctl's own reachability probe still reaches `retroachievements.org` with a HEAD request; that sends no account.

**The run:** `scripts/ra-refusal.sh`, three cases in EN and FR, 17:55 to 18:04 UTC (`RESULT.txt`). Each case arms the account, reboots so EmulationStation reads it, starts the stand-in, then walks GAME SETTINGS > RETROACHIEVEMENTS SETTINGS > OFFLINE ACHIEVEMENTS (BETA) > SCAN GAMES FOR OFFLINE ACHIEVEMENTS > YES. `RESULT.txt` is its own record, with each case's `last-scan` stamp and the scan log's last lines. The frames are `frames/<lang>-<case>-{scan-row,confirm,result}.png`, and `evidence-index.json` indexes them. Each confirmation quotes the case before it as "last time".

| Case | The client's line | Stamp | The page |
| --- | --- | --- | --- |
| password-401 | `RetroAchievements login required` | `SIGN_IN_REFUSED` | COULDN'T FINISH / RETROACHIEVEMENTS DIDN'T ACCEPT YOUR SIGN-IN, help bar CLOSE · TRY AGAIN. That is #1501: a retry that is refused the same way. |
| token-401 | `RetroAchievements rejected the login` (×3) | `RETROACHIEVEMENTS_STOPPED_ANSWERING` | COULDN'T FINISH / RETROACHIEVEMENTS STOPPED ANSWERING, CLOSE · TRY AGAIN. That is #1502: a refused sign-in is told as the server not answering. |
| token-503 | `Game lookup failed: HTTP Error 503` (×3) | `RETROACHIEVEMENTS_STOPPED_ANSWERING` | The same page. This is the control: here the why and the retry are right. |

**Also seen:** after the reboot in the password case, the top-up at the link's return logged `RetroAchievements login required` from its recently played pass. It stamped `RETROACHIEVEMENTS_STOPPED_ANSWERING` (17:53:35, `raofflineproxy-ctl:2269-2272`). That is #1502's second half.

## The ctl change before the build (#1502)

`scripts/ctl-check.sh` binds the round's patched `raofflineproxy-ctl` over the image's on the guest (a bind mount, gone at the next reboot). It runs the states from the shell, first with the image's ctl as the control. `ctl-check-2.txt` is the run that counts.

| State | Image's ctl | Patched ctl |
| --- | --- | --- |
| scan, token-401 | RETROACHIEVEMENTS_STOPPED_ANSWERING | **SIGN_IN_REFUSED** |
| scan, token-503 (control) | RETROACHIEVEMENTS_STOPPED_ANSWERING | RETROACHIEVEMENTS_STOPPED_ANSWERING |
| scan, password-401 | SIGN_IN_REFUSED | SIGN_IN_REFUSED |
| top-up, password-401 | RETROACHIEVEMENTS_STOPPED_ANSWERING | **SIGN_IN_REFUSED** |
| top-up, token-401 | nothing to do (rc 0) | nothing to do (rc 0) |

- **`ctl-check-1.txt` was the first run, and its top-up token case is void.** The stand-in then answered every request with its status, the client's check that the site is up included. The client printed `Smart Cache requires an online connection`, which is not a sign-in at all. `scripts/standin.py` now answers only `/dorequest.php` with its status and 200 elsewhere. The scan cases are unaffected: the scan's helper does not make that check.
- **The top-up with a refused token is not exercised here.** The client's recently played pass contacted nothing and ended rc 0, even with one RetroArch history entry for a seeded ROM written by hand. The fix reads the client's `rejected the login` in that pass too, but no run has shown it there. It is named in #1502's trace.

The fixed image (route 14) is proved with `tools/vm-walks/ra-refusal-outcomes`, the promoted driver. It checks each case's stamp and fails on a wrong one.

## Build 23: the fixes (route 14, round `5bd8ad6dc0`)

**The check fails on the unfixed image.** `tools/vm-walks/ra-refusal-outcomes` on build 22, in EN, ended FAILED. It wanted SIGN_IN_REFUSED at token-401 and got RETROACHIEVEMENTS_STOPPED_ANSWERING; password-401 and the 503 control passed (`build22-driver-RESULT.txt`).

**On build 23 it passes.** The same driver, EN and FR, 18:22 to 18:31 UTC, ended **PASSED**: all six cases stamped their expected why (`build23/RESULT.txt`, with each case's scan-log lines).

| Case | The page on build 23 |
| --- | --- |
| password-401, token-401 (EN) | COULDN'T FINISH / RETROACHIEVEMENTS DIDN'T ACCEPT YOUR SIGN-IN / SIGN IN AGAIN: GAME SETTINGS > RETROACHIEVEMENTS SETTINGS, with **CLOSE alone** |
| password-401, token-401 (FR) | N'A PAS PU SE TERMINER / RETROACHIEVEMENTS N'A PAS ACCEPTÉ VOTRE CONNEXION / PARAMÈTRES DES JEUX > PARAMÈTRES RETROACHIEVEMENTS, with **FERMER alone**. The long line does not fit at 640x480, so the short form shows, unclipped. |
| token-503, the control (EN, FR) | RETROACHIEVEMENTS STOPPED ANSWERING / NE RÉPOND PLUS, with CLOSE · TRY AGAIN and FERMER · RÉESSAYER |

Frames: `build23/frames/`. They are indexed in `evidence-index.json` as `build23-*`.

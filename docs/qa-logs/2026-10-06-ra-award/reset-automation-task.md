# Reset automation task — GitHub readback

https://github.com/pixelelated/distribution/issues/464

Title: Backlog: Automate dedicated RetroAchievements QA progress resets

State: OPEN; no milestone. This snapshot records the requested task, not its implementation.

## Maintainer request — 2026-10-06

> We should add a task to use something like Browserbase or Kite Surf to automate the reset of the RetroAchievements when necessary, so it can be fully automated. https://developers.cloudflare.com/browser-run/kitesurf/

## Prior decision reopened

Archaeology found #240/D-QA-035 and the 2026-09-21 work log: reset automation was previously left manual after a headless authentication failure and Kitesurf limitations. D-QA-059 records the maintainer's new request to reopen this as an explicit automation task. Preserve those observations and recheck current compatibility; do not silently assume either a supported reset API or permanent browser incompatibility. #240 retains additional routed-fixture coverage and clear spent-fixture guidance; this issue owns automation.

## Existing behavior

`tools/ra-offline-test` queries RetroAchievements for an unearned routed achievement before launching, then consumes one ordinary/softcore unlock per successful run. Only Tobu Tobu Girl Deluxe game15738 / Potato-tan Secret achievement100359 currently has a proven route. The maintainer manually resets it between tests; #361's replacement14 proof completed33/33 checks after “Progress reset.”; that reset is now consumed. The award/queue/reconnect/API receipt and actual cleanup are retained at `docs/qa-logs/2026-10-06-ra-award/`. Dedicated credentials are in the existing protected QA-account file and never belong in chat, logs or source.

This is a backlog improvement to make future proof runs unattended, not a new gate for the first RC or a reason to repeat the current award.

## Approach to evaluate

Compare an official supported reset interface if one exists, local/self-hosted browser automation, Browserbase and Cloudflare Browser Run/Kitesurf. Preserve the maintainer's FOSS preference: record licenses, self-hosting options and hosted dependencies separately before choosing. Do not assume a hosted browser service is a fully FOSS stack or provision/buy one as part of filing this task.

Cloudflare's [Kitesurf documentation](https://developers.cloudflare.com/browser-run/kitesurf/) describes a stateless browser and currently excludes long-running authenticated sessions requiring persistent state. Verify whether the actual login/reset flow fits; otherwise evaluate Chromium-based browser automation. A page screenshot or successful click alone is not reset evidence.

Can this be done on the VM? Yes — the harness can coordinate a dedicated QA-account reset through browser automation on the build/agent host, then run the normal award/reconnect test in an isolated GENERIC_X64 guest. No physical device or personal account is needed.

## Acceptance criteria

- [ ] A recorded capability/license/deployment comparison selects a supported approach, with a working authenticated QA reset prototype and its exact execution environment.
- [ ] A tool validates the dedicated QA account, game15738, achievement100359 and softcore/normal scope before a reset; refuse mismatched account/game/mode. Already-unearned state is an observed no-op.
- [ ] The existing RA API preflight confirms the selected achievement is unearned after reset, with bounded polling and a sanitized result; unknown API state is never treated as unearned.
- [ ] Integrate reset-on-demand before `ra-offline-test`, with exclusive account ownership so two jobs cannot reset or consume the same fixture concurrently. Never reset during an in-flight award/flush proof or erase that proof's evidence.
- [ ] Demonstrate two consecutive reset → offline award → reconnect → provider receipt cycles without a manual progress reset. Retain exact build/ROM identities, terminal results and actual cleanup.
- [ ] Login expiry, reset refusal, unavailable provider and unexpected UI/account/mode fail visibly with bounded behavior and watcher completion/failure receipts; credentials, cookies and session artifacts stay protected and out of published logs.
- [ ] Update the QA runbook and session guidance with the supported automated path and the named manual fallback if unattended authentication cannot be completed. No bypass of provider authentication challenges.

Related: #166, #361, #462; D-QA-016, D-QA-058. The separate Dropbox/offsite cloud observation remains optional #463.

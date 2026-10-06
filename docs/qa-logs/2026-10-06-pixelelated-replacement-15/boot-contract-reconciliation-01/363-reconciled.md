## Completed on the current candidate — 2026-10-05

Frozen `57cbc9b981205328444d41f6c4237dc9f5736d7f`, bundle `d4007387afd5ac42104a53a3073b93fdadd33c51179bf9f3142101609f821ec9`. Published receipts: https://github.com/pixelelated/distribution/tree/cdb1b307e74ebb9b2cf36f2dffa451468c6fb358/docs/qa-logs/2026-10-04-pixelelated-57cbc-qualification. All named owners' actual tool/result channels and cleanup are recorded.

- qa07's installed scripts.log lines1461/1462 pass both no-networked-folder-preparation assertions. Sections aa/ab/ad cover the no-network needs-step decisions, folder-only scan, unchanged transfer-page scans and absent/unknown legacy-folder behavior. The implementation's local `--superseded` list is intentional under D-CLOUD-172; the old literal no-call criterion is corrected below.
- runtime07/tool29491 passes the unchanged30ms median gate at28ms with every save byte verified and no migration journal delta. #429/#430 retain all attempts and distinguish fixture correction from any unproved original host cause.
- guest06/tool67203 independently resets each case. I has11PASS, including NOT NOW asking next boot, MOVE preserving bytes/pointers, and a post-move boot with the exact `nothing to settle` journal predicate and no checking line (runner lines297–298). Selected actual640x480 frames I-boot1-0020/0027/0030/0031/0035 show startup card, outcome, clear carousel, CHECKING, then the move question. E's no-folder path also shows card clearance before CREATE IT; no old root is recreated.
- L has7PASS and actual wizard frames: L-setup-0137/0138 show step3 then CHECKING, followed by move question and CLOUD SETUP COMPLETE after NOT NOW. J's offline frame and K's explicitly seeded restore-marker sequence preserve offline choices and restore-first FINISH/LATER ordering.
- optins05/tool62343 passes42 mixed previous-RC2/fresh-pixelelated pair assertions: wizard seeding joins the existing folder, move/quiet follow preserve saves, a missed step refuses absent-old-root recreation, and the explicitly staged older-writer save merges into the fleet folder.

Code trace: distribution cloud_backup's `superseded_saves_setting` and `bucket_exists`, cloud_restore's transfer path, plus ES at `c75aa3fac967ba532fd9ba1c21fa10ca024e8bc1` boot readiness/notification wait. D-CLOUD-173 keeps boot preparation before startup transfers and defers the dialog until the actual notification list is empty. `tools/rasteratops-vm-cloud-epic` supplies the retained case predicates.

Already written: existing configured ROCKNIX/custom cloud paths and local saves remain authoritative. The candidate preserves them on upgrade, performs no automatic cloud move, waits for the player's setup choice, and prevents recreating an absent superseded saves folder. Tests use isolated synthetic clouds and an actual RC2 upgrade, not the owner's personal cloud. No deployed-state rewrite is claimed.

## Readiness review update — 2026-10-02 (#375)

Fresh corrected `tools/cloud-pair-migration` on RC2/run101 passed 42/0 at 2026-10-02 06:08 UTC, artifact `qa-b2378d9c33-pair-migration-from-69e6039f8f-20261002-0606`. Step 5m now proves refusal/follow after an absent old root; 5n proves staged old-writer merge. The boot-card criterion is reopened: `docs/qa-frames/2026-10-02/363/E-run101-skipped-card-over-the-step.png` shows SKIPPED over CHECKING YOUR CLOUD; `ThreadedCloudSync.cpp:719–735` clears the worker before the card's linger ends and `GuiMenu.cpp:5545–5603` waits on worker state. Repair visibility ordering without reversing the lock-order decision D-CLOUD-171. `docs/retros/2026-10-02-cloud-runs-95-101.md` feeds #365's whole-boot cases.

## The maintainer's words (2026-10-01, on the exit-sync cost measured on run 99)

> Why don't we just do this the first time? A handheld with a newer version of the OS boots and connects to the network. If we know the version and we know it's running Rasteratops, we'll know this is something we need to look for. It should only need to be checked the first time it checks the network. It shouldn't need to happen at every exit sync.
>
> We already have the ability to run the post-restore migration after our restore is complete. We could do something similar: the first time a Rasteratops-generated build loads, simply ask the person to connect to the network. Or, it's not a great idea. We could show it if they're connected to the network at boot, and then the next time they exit, or the next time any network connection is detected.
>
> My point is that there should be a way to simplify this and reduce it to something that happens every sync.

And, a minute later:

> Sorry, there was a typo. I mean that we should be able to reduce it so it does not happen on every sync.

## What existed when this was filed

- `cloud_backup` and `cloud_restore` run `follow_layout` before every sync, automatic or not (`48c2df30a9`, D-CLOUD-160's "your other devices will follow"). On a device whose conf names a folder this project once shipped as its default (`/ROCKNIX/Saves`, `/GAMES`) and that has not kept it, it starts `cloud_migrate_layout --follow`, which asks the cloud whether another device has made `/Rasteratops` and, if that device emptied the old folder, re-points this one. A device on the current folder pays only a string test.
- Why every sync: to catch another device's move before this one writes into the old folder again. Once written into, the old folder cannot be followed without stranding those saves, so the device is offered MOVE instead.
- The cost, on guest d with run 99's image (`041900bfa7`), the median of five exit syncs:

| Exit sync | ms |
| --- | --- |
| a device on the current folder | 147 |
| a device still on `/ROCKNIX`, the follow check as shipped | 419 |
| the same, the check trimmed to one listing (in the working tree, not built) | 242 |

A handheld pays more than the VM; the VM's latency is a lower bound.

## The first proposal (superseded by D-CLOUD-170 below)

- Check once per boot, at the first sync that reaches the network: the startup sync when the handheld boots online, otherwise the first exit sync after a connection appears. The mark lives in `/run`, cleared at every boot, and is written only after a check that reached the cloud, so a sync with no network does not use it up.
- The transfer pages' scan keeps checking every time it opens; it already talks to the cloud.
- No new prompt at boot: the folder question stays on the cloud setup step and the transfer pages (D-CLOUD-166).
- What it gives up: a device that is already on and has checked keeps syncing to `/ROCKNIX` if another device moves the folder meanwhile, until its next boot. By then it has written there, so instead of following silently it is offered MOVE, which merges (D-CLOUD-168) and loses nothing. This rests on D-CLOUD-168 staying as written.
- Once per update instead of once per boot would never catch a later move by another device on its own.

## Decided: the cloud folder step (D-CLOUD-170, 2026-10-01)

The maintainer replaced the proposal above with a setup step (their words are in the comments below): the folder is settled where the player first meets the cloud, and no sync checks it.

- **At the end of cloud setup**, right after a remote is linked and before the seeding and CLOUD SETUP COMPLETE: the scan of the folder alone (`cloud_scan --folder`) and, when an earlier `/ROCKNIX` or `/GAMES` holds saves, MOVE / KEEP USING / NOT NOW. Every way out goes on to the seeding and the last page.
- **At boot**, for a conf on a folder an earlier version made its default and not kept, with a remote set up (`cloud_migrate_layout --needs-step`, no network): the same step once the startup sync has ended and the screen is free, at every boot until the folder is moved, kept, followed or created. Offline: `FINISH CLOUD SETUP` / `YOU'RE NOT ONLINE. CONNECT TO FINISH SETTING UP YOUR CLOUD FOLDER.` with CONNECT TO WI-FI and NOT NOW.
- **One setup page at a time**: FINISH RESTORE PROCESS first; its FINISH arms the step, its LATER puts both off to the next boot.
- **The follow check before every sync is gone** from `cloud_backup` and `cloud_restore`. What that gives up, accepted with the step: a handheld already on that writes into the old folder after another device moved it is offered MOVE at its next step, which merges (D-CLOUD-168).

## Can this be done on the VM?

**Yes.** The scripts are the sandbox suite's (`tools/last-good-scripts-test`); two guests on one cloud, the move and the merge are `tools/cloud-pair-migration`'s; the step's pages are frames on guest d at 640x480, offline with the link cut on the QEMU monitor; the cost is the follow benchmark on guest d.

## Acceptance criteria

- [x] Ordinary backup/restore and exit-sync paths run no networked layout join/state/follow/migration preparation before transfer. The explicit boot-only exception is D-CLOUD-173: the startup worker prepares eligible legacy pointers with the existing join/state/follow scan before transfers, bounded to 30 seconds; failed preparation prevents transfer, and preparation moves no cloud files. The setup dialog still waits for the worker and the actual notification list, including linger/fade, to finish. The local `cloud_migrate_layout --superseded` string-list call and per-run legacy saves-folder existence probe required by D-CLOUD-172 remain permitted. `tools/last-good-scripts-test` reports both no-folder-check PASS lines; missing/unknown-root controls preserve D-CLOUD-172. This corrects the obsolete literal no-call wording against D-CLOUD-170/172/173, rather than removing the required absent-folder guard.
- [x] An exit sync on an existing earlier `/ROCKNIX` folder and the current folder meets the unchanged five-alternating-sample median difference limit of30ms. Current candidate runtime07:272/244ms medians,28ms difference, real transferred bytes and zero migration preparation. #429 preserves the original36ms failed attempt and justifies the new fixture-bound qualification.
- [x] `cloud_migrate_layout --needs-step` answers with no network: 0 for an earlier default, not kept, with a remote set up; 1 for the current folder, a folder of the player's own, a kept one, or no remote; 2 for a conf it cannot read; rclone never starts (`tools/last-good-scripts-test` section aa, its `--needs-step` lines).
- [x] `cloud_scan --folder` is the folder item alone -- the join, the state, the quiet follow -- with no archive or root listing, the opening scan's files left as they were, and a refused join ending with its why and no state (section ab, its `--folder` lines).
- [x] The transfer pages' scan still checks on every open (`tools/last-good-scripts-test` section ab).
- [x] At the end of cloud setup, for a fresh install whose cloud holds its saves under an earlier folder, the step reads the move before the seeding (`tools/cloud-pair-migration` step 2's lines), and the frames show CHECKING YOUR CLOUD, the MOVE question, then CLOUD SETUP COMPLETE after the answer (`tools/vm-visual-qa` frames at 640x480).
- [x] At boot, for a guest whose conf names an earlier folder it has not kept, with a remote set up, the step comes up after the startup sync's card: CHECKING YOUR CLOUD, then the question; NOT NOW brings it back at the next boot; after MOVE the next boot raises nothing and the journal reads `nothing to settle` (frames at 640x480 and the journal, guest d).
- [x] Offline at boot (the guest's link cut on the QEMU monitor), the step asks `FINISH CLOUD SETUP` / `YOU'RE NOT ONLINE. CONNECT TO FINISH SETTING UP YOUR CLOUD FOLDER.` with CONNECT TO WI-FI and NOT NOW (a frame at 640x480).
- [x] With a settings restore's marker and an earlier folder both set at boot (written on guest d, a named stand-in for a restore followed by an update), FINISH RESTORE PROCESS comes first with nothing over it; its FINISH brings the step once the screen is free; its LATER brings neither until the next boot (frames at 640x480).
- [x] `tools/cloud-pair-migration` covers both later cases: the other guest's step follows after the move (step 5), and a guest that missed its step and backed up into the earlier folder has those saves merged by MOVE with nothing left behind (step 5n; 5m checks absent-root refusal/follow) -- its PASS lines.

(2026-10-02, run 101 `b2378d9c33`: the end-of-setup checkbox ticked from `pair-101.log`'s five step-2 PASS lines and the frames `docs/qa-frames/2026-10-02/363/L-run101-checking-your-cloud-at-end-of-setup.png`, `L-1-move-question-after-step3.png` (run 100's, the same question) and `L-run101-setup-complete.png`; case L's four PASS lines in `epic-proof-101.log`.)

P4 audit contract reconciliation, 2026-10-06: the wording above now states the existing D-CLOUD-173 boot exception explicitly (audit B-04, narrowed to contract reconciliation). This changes no runtime requirement, completion state, historical title or checkbox. Source trace: EmulationStation `main.cpp` startup preparation before receive/send; the original runtime prohibition was withdrawn by the verified Fable refutation. Current candidate qualification remains tracked by #471.

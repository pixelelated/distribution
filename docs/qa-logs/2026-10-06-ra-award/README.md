# Ordinary offline RetroAchievements proof — replacement14

Refs #361/#383. After the maintainer confirmed “Progress reset.”, a fresh
isolated guest ran the existing `tools/ra-offline-test --game tobu` route on
Tobu Tobu Girl Deluxe (game15738), Potato-tan Secret (achievement100359),
in softcore/normal mode. **33 PASS, 0 FAIL, 0 SKIP.**

The provider API first confirmed the achievement was unearned. RetroArch
logged in through the installed proxy and activated28/28 achievements.
The QEMU link was cut and both guest eth0 and the proxy's offline state were
verified before game input. The real game awarded100359, the proxy queued
it, and one pending award remained after the game exited offline. On link
return the proxy flushed one award and pending became zero. The provider's
API reported it earned; relaunch activated27/28, recognizing the unlock.
No hardcore or synthetic award substituted for this proof.

Source `7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2`; immutable candidate bundle
`b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1`;
image SHA256 `c7df6a6f428086f79a377ca1b049f20694f34a868987cf12c493c78eab7b2254`.
Exact installed identity/scripts and frozen inputs/bundle pass before and after.
No product bytes changed or new image was built.

Owner `/workspace/tmp/pixelelated-m7-ra-01`, run20261006T060338Z-0420faa8.
The standard durable watcher sampled every5seconds with5minute inactivity
detection, actively supervised. Terminal result06:09:20UTC; all four rc0.
Actual cleanup06:10:11 verifies five recorded PIDs absent, no QEMU, SSH/VNC
ports unbound. The harness restored switches, disabled the proxy and cleared
QA credentials/cache; an independent final `qa-accounts clear` readback passed.
No disconnected alert-delivery claim (#395). Never replay this used owner.

`ra-offline.log` is the sanitized assertion record. `harness/` retains the
sealed owner and completion checker. It exports QA_KEY for the private pair,
uses the fixed external ROM directory, explicitly selects hardcore=0 and
independently clears accounts before stopping the guests. No secret file,
proxy database, ROM or raw guest configuration is included.

## Visual scope

Forty exit captures contain four unique PNG byte streams. All four were
directly reviewed and are retained under `frames/`; `frame-groups.json` maps
the original40 captures to their hashes. They show the complete ES carousel,
with the connection indicator absent offline and present online. No account
identity or credential is visible. **No send/queue card was captured**, so
this run makes no new card-layout/progress-UI claim. Previously retained UI
qualification remains separate; this receipt proves the actual award path.

## Follow-up

This PASS consumed the reset softcore achievement. A future repeat requires
another reset until #464 qualifies automated reset-on-demand. D-QA-059 reopens
the earlier D-QA-035 manual-only choice for evaluation of local/self-hosted,
Browserbase and Kitesurf options. No provider or hosted credential transfer
has been selected. Automation remains backlog and does not delay the RC.

Local WebDAV/SFTP/MinIO-S3 qualification is separately complete under #462.
Dropbox/offsite accounts remain optional under D-QA-058/#463. Continue the P3
criterion reconciliation and approved P4 fixes review before H700 arm/aarch64;
this is not a completed audit or an RC/device-ready claim.

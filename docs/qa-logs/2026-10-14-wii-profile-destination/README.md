# Wii retained profile destination — source correction, runtime UNRUN

Review target: distribution `7aab15fc9a1ceab18125ec096a8e6f7f03bdae95`.
Only `/tmp` packet files were written. No coordinator/product/shared checkout,
Git branch, owner, runtime, compiler, device, or provider was changed or launched.

## Confirmed adjacent defect

`projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/start_dolphin_wii.sh:57`
copies missing stock Wii profiles to `${CONF_DIR}/dolphin-emu/`, although line 24
already sets `CONF_DIR=/storage/.config/dolphin-emu`. When an existing retained
config lacks `WiiControllerProfiles`, the intended directory stays absent.
Line 62 cannot create the custom profile, and lines 256–264 cannot select a
stock or custom profile into `WiimoteNew.ini`. The script continues, potentially
using stale controls or leaving Dolphin without the requested profile.

Fresh whole-directory initialization at lines 39–41 masks this branch; this is
specifically a retained partial configuration. It predates the M7 integration:
`history-blame.txt` attributes the destination to `43eb79428d62f536a531419c96421437a860da20`
(2025-09-03, Dolphin SA updates). Offline archaeology found no register,
blindspot, work-log, or rule entry for `WiiControllerProfiles`; this does not
claim a complete live issue search. The coordinator tracks it under existing
#581/#585 work.

Upstream-first: live GitHub API read at 2026-10-14 19:03 UTC found
`ROCKNIX/distribution:next` at `50097e80c92f96cf301f8ae146fef41e39c37608`.
Its exact launcher still has the same error at line 52. The full fetched file,
URL, SHA256, and relevant lines are retained in `upstream-start_dolphin_wii.sh`
and `upstream-comparison.json`. The cached upstream ref was older and was not
used as a current-upstream claim.

## Minimal source correction

Apply `wii-profile-destination.patch` from a checkout whose complete launcher
matches `bindings.json`'s baseline SHA256. The only changed bytes replace the
destination `${CONF_DIR}/dolphin-emu/` with `${CONF_DIR}/` on line 57. Full
baseline/candidate launcher bytes are retained; helper, GC launcher, achievement
helper, runemu, Tools entry, recipe and all four canonical Wii profile files are
included unmodified under `source/`. The correction preserves the existing
conditional that leaves an already-present directory and custom profile alone.

```sh
git apply --check /tmp/m7-wii-profile-destination-20261014/wii-profile-destination.patch
git apply /tmp/m7-wii-profile-destination-20261014/wii-profile-destination.patch
```

These integration commands were not executed by this worker. Candidate launcher
SHA256 is `8b87c5779737918644655950f25547341f89eda59fee137b752790382dffb88b`;
patch SHA256 is `110a1bb4f0791b6efac795bdbcc30878b754e14965f58334321d26a780cb76ae`.
Static AST/shell syntax and exact one-line comparison are in `static-result.json`.
No script body or fixture was executed during preparation.

## Existing installed-image acceptance, with a focused component check

Can this be done on the VM? Yes. No physical fact is involved. Do not allocate a
separate prebuild VM for this packet: run alongside the coordinator's existing
new-image #581 native/retained-storage checks. An installed image must contain
the corrected full GENERIC_X64 launcher, unchanged preservation helper and exact
stock Wii profiles. `profile-fixture.py` verifies those bytes before any case.

The optional bounded fixture executes only the verbatim initialization block
from the complete bound launcher, with `CONF_DIR` set to fresh synthetic `/run`
storage. It reads actual `/usr/config` defaults. It never launches an emulator,
the full launcher, runemu or helper; it does not establish gameplay, native
controller discovery, full caller acceptance or save persistence. The new image's
already-required actual launch/native checks cover those paths.

Use a newly admitted, no-NIC disposable QEMU guest with a fresh output name.
Stage this complete packet read-only as `/tmp/pix-input/wii-profile-destination`
with source modes preserved. Python invokes the fixture, so input may be noexec.
The fixture requires `/sys/class/net` to contain only `lo`, a QEMU DMI name,
the explicit allocation marker below, and a new direct `/run/pix581-profile-*`
output directory. Its own wall bound is 45 seconds, each Bash child 10 seconds,
address-space cap 256 MiB, CPU cap 15/20 seconds and per-file cap 4 MiB. The
coordinator's normal admitted owner retains lifecycle and original exit channels.
No visual/QMP/VNC interaction or competing serial reader is required.

Run these sequentially through the coordinator's one serial owner. Each direct
command's original return status must be captured by that owner; do not append
an echo that replaces it. The first intentionally returns **1** when the exact
baseline failure is reproduced and records `causal_reproduced: true`, original
Bash exit and diagnostics. A fixture failure has no such assertion and is not a
reproduction. The second returns **0** only if all candidate cases pass.

```sh
PIX581_PROFILE_VM=allocated /usr/bin/python3 -I -S -B \
  /tmp/pix-input/wii-profile-destination/profile-fixture.py \
  --disposable-vm --variant baseline --output /run/pix581-profile-baseline01

PIX581_PROFILE_VM=allocated /usr/bin/python3 -I -S -B \
  /tmp/pix-input/wii-profile-destination/profile-fixture.py \
  --disposable-vm --variant candidate --output /run/pix581-profile-candidate01
```

Candidate cases: retained config missing profiles gets all four stock profiles
plus custom copied from vremote; an existing custom profile remains byte-exact;
existing stock profiles without custom receive only that missing custom file.
Every case proves all pre-existing synthetic files unchanged and no extra nested
`dolphin-emu` directory. Preserve `result.json`, exact executed block, each
original stdout/stderr and owner return status before removing only owned `/run`
outputs. Existing helper/refusal frame evidence retains its original scope;
there is no string or layout change here and no new frame claim.

## Other reviewed integration changes

No additional functional defect was found in the reviewed GENERIC_X64 package
selection, profile symlinks, OGL defaults, or generated-documentation redirect.
OGL is set in both stock Dolphin.ini and recipe-substituted automatic launcher
fallbacks; manual renderer selection remains explicit. The metapackage includes
the full existing Dolphin package and lists its two compiled GC/Wii frontends,
without listing the unbuilt libretro core. `cp -aL` resolves the repaired stock
profile links. Compilation, Qt plugin/ELF closure and actual renderer/controller
operation remain the existing assembled-image acceptance work, not source proof.

Packaged proxy patch 021 is byte-identical to the accepted startup-handoff patch
(SHA256 `6e8992555e7c6f6616be48ec7e3e2f5626718bb08d1ebc243e0f466ebc912d22`).
Independent static reconstruction from the exact prepared baseline produces
`proxy_service.py` SHA256 `432bb07ac6b0abcdcb38800d7c75a92c768b2b6bea583a1bab6834bb7f7b0d00`.
Startup assigns the initial result before starting the monitor; the extra flush
uses the existing server lock and stop check. Root's existing actual-service and
ten component results remain the runtime evidence; this review ran none.

The generated-doc candidate functions hash matches
`e574a017b83e0da4d9360017ed14d1edcab86eb979efcad1b15fd4bc76407baa`.
The redirect runs only after BUILD is established, all final doc writes use the
redirected SYSDOC, and the watched-build marker reaches native/Docker children.
Direct generation keeps the configured old destination. Its fixture01 setup
failure and delegated correction are unchanged; this review makes no fixture
PASS or full-image claim.

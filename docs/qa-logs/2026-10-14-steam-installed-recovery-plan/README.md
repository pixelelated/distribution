# Steam remaining recovery and selected-image qualification — #564 / #579 / #580 / #582

SOURCE ONLY, UNRUN. No product selection, running build, provider, guest or original
fixture was changed. Frozen engineering source is distribution
`d6a87f05c1935516115b2cca1af22151a0209224`. Its complete installer is 124320 bytes,
SHA256 `fab7cdb4ad8adbcea147be54092bb7ce2005010447be4ab8192c94d8bbe9229d`, byte-equal
to reviewed candidate `03e130e4b3c244337f2e6d782b392a2c444c28e7`.

Can this be done on the VM? The remaining synthetic recovery cases can run on the
existing no-NIC GENERIC_X64 QEMU topology using installed interpreter/tools and
private synthetic storage. They execute a **source copy in a chroot**, with
synthetic profile, transport, FEX/Proton/client payloads and native-client exec
denial. They cannot establish installed Steam or native ARM64 usability. The
selected SM8550 SYSTEM can be inspected on the host without executing its code;
actual native ARM64 execution needs a separately admitted compatible runtime.
No owner-device/provider operation is authorized or performed by this packet.

## Accepted evidence to retain, not repeat

`docs/qa-logs/2026-10-13-library-vm/results/steam-results/result.json` retains the
original combined FAIL: root35, runtime39 and Proton56 individual cases passed;
FEX's original fixture failed. The additive `steam-corrected-results/result.json`
records FEX43 PASS and preserves the original failure. All four embedded helper
hashes still match the current installer. The FEX enclosing success logger changed
from terminal to returning; `steam-routes-results/{result,caller-observation}.json`
proves the complete nine-step caller and 12 preservation roots on c6240ed3984a.
The current client implementation then received independent review and full-caller
proofs; no old whole-file digest is silently accepted as the current source.

`docs/qa-logs/2026-10-14-steam-client-first-caller/` contains nine accepted labels:
fresh-client-real-root, fresh-profile-parent-alias, existing-profile-parent-alias,
detached-transfer-child, proc-census-error, transport-timeout,
interrupt-published-retry, committed-self-update-retry and crc-failure-retry.
Attempts01 and10 remain failed; attempt06 was refused before execution. The real
180-second timeout and deliberate SIGKILL results remain negative original exits.
The public 55-member archive CRC/layout/ELF inspection is accepted separately;
no second download or decoder inspection is requested here.

## Small missing glue: corrected event capture for the remaining labels

`prepare-recovery.py` verifies the complete accepted CRC-event packet at manifest
SHA256 `6a6c3b255525f57c624dba32d55720e10d0e130c2ffeb564c4e2ae6881796c7d`
(commit `8f0eaf27ed539beeac4c117711601d78c9125d4a`). It copies its exact files to a
new private directory, changes **only `source.json.cases`** to the 14 labels below,
retains the original binding/manifest, writes a separate continuation receipt,
and seals the derivative. Every fixture/helper/event-writer/payload byte stays
unchanged. The nine accepted labels, including CRC, are refused by the new
allowlist. The original multi-case03e130 fixture still has the known shared-event
FSIZE collision; do not use it for the remaining retry cases. No new runner,
retry loop, timeout, failure interpretation or native-exec permission is added.
The copied original README/static results describe their historical CRC-only
packet; `continuation.json` explicitly distinguishes the new UNRUN scope.

On the host, source preparation only (fresh absolute output; no fixture imports):

```sh
python3 -I -S -B /path/to/this-packet/prepare-recovery.py \
  --accepted-packet /workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-14-steam-crc-event-source \
  --output /tmp/pix582-remaining-source01
```

Retain its stdout/seal and source-bind the installer from the **frozen build
checkout**, not an old fixture source. Stage both read-only through the existing
input-ext4 mechanism. Existing lifecycle and guest wrapper originals are
`/workspace/tmp/pix582-client-vm-20261014-11/{vm-lifecycle.py,run-guest.sh}`; they
are templates only, with spent owner/image paths. Root must prepare a fresh owner,
final-image/helper/input identities and the selected case before allocation.
Omit the already accepted5-second FSIZE control. Keep the lifecycle's original
result channels, serial ownership, output-media export, pidfile stop and retirement.
No existing owner or input disk is reused.

One case per newly admitted owner, serially; consume the original result before
choosing another. No shell loop or automatic retry. Example first remaining case:

```sh
# Guest-only inside the admitted 8GiB/4-vCPU no-NIC QEMU guest.
# The derivative is staged at /tmp/pix-input/docs/qa-logs/2026-10-14-steam-remaining-source.
# Keep this repository-relative depth: fixture ROOT=HERE.parents[2] must be /tmp/pix-input.
# Root supplies a fresh3GiB executable nosuid,nodev tmpfs at /run/pix582-scratch.
# /tmp/pix-output/steam is a fresh directory on the bounded output ext4.
set +e
TMPDIR=/run/pix582-scratch timeout --signal=TERM --kill-after=10s 120s \
  python3 -I -S -B /tmp/pix-input/docs/qa-logs/2026-10-14-steam-remaining-source/fixture.py \
  --disposable-vm --case fresh-profile-dot \
  --installer '/tmp/pix-input/projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh' \
  --output /run/pix582-scratch/fresh-profile-dot-01 \
  > /tmp/pix-output/steam/stdout 2> /tmp/pix-output/steam/stderr
TASK_STEAM_RC=$?
printf '%s\n' "$TASK_STEAM_RC" > /tmp/pix-output/steam/original.rc
set -e
```

Retain/export the original `result.json`, `namespace-result.json`, all
`exec-*.json`/`attempt-*.json`, installer stdout/stderr, before/after storage
manifests, first-failure journals, `events-collected.*` and every original event
stream. Reuse accepted wrapper tar exclusions for rootfs/storage/tmp/qa/payloads;
do not strip observation JSON or original event files. Then sync/unmount scratch,
flush/export output, stop by the actual QEMU pidfile, check all original
launcher/runner/monitor/namespace/trace exits and census, consume admission and
retire its disposable disk/media. A wrapper0 is insufficient without the expected
caller sequence and PASS assertions below; guards/rescue/survivors are failures.

| Remaining case, in proposed serial order | Required original caller exits |
| --- | --- |
| fresh-profile-dot | 0 |
| fresh-profile-dot-absent | 0 |
| valid-existing-alias | 0 |
| existing-profile-dot | 0 |
| self-updated-client | 0 |
| partial-before-profile | 1 |
| marker-missing-core | 1 |
| metadata-conflict-after-profile | 1 |
| unknown-stage-before-profile | 1 |
| download-failure-retry | 1,0 |
| validation-failure-retry | 1,0 |
| publication-failure-retry | 1,0 |
| metadata-failure-retry | 1,0 |
| interrupt-prepared-retry | 1,0; deliberate helper SIGKILL retained |

All fixture/namespace/trace final wrappers must0 for an accepted expected outcome.
Internal idle trace admission remains driver1/caller null, intentionally, and
its original record is retained. Limits remain90s fixture,80s trace,10s cleanup,
120s+10s guest wrapper,900s existing whole lifecycle;3GiB executable tmpfs with
2368MiB minimum free,64MiB retained data,2MiB/log and1MiB synthetic archives.
Original per-child event streams have4KiB/512-file bounds, merged2MiB. No240s
transport case is dispatched. Guest Python must support hashlib.file_digest
(accepted VM20 was3.14.7); namespace applets must still match BusyBox digest
`79e7b20ddbe5abb6d18690dacc9b31803eb72cea949fce0a52cd9c2888829346`.
A changed final-image applet digest is a deterministic admission stop requiring
source/tool review, never a blanket hash replacement or prior-image tool overlay.

## What the current GENERIC_X64 image can prove

`virtual/emulators/package.mk` selects Steam and installs its module/system only
for SM4450/SM8250/SM8550/SM8650/SM8750 (current lines754–768). GENERIC_X64 has no
Steam package/module/system declaration. Keep this production selection unchanged.
After normal image identity/untouched-clean verification, this read-only guest
command confirms the actual default image absence (use the same owner, no extra
VM). It prints no account/config values; outer command bound10s/1MiB output:

```sh
python3 -I -S -B - <<'PY'
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
paths=['/usr/config/modules/Install Steam.sh','/usr/config/modules/Uninstall Steam.sh',
       '/usr/bin/start_steam.sh','/usr/bin/start_steam_arm64.sh','/usr/bin/FEX']
absence={p:not Path(p).exists() and not Path(p).is_symlink() for p in paths}
raw=Path('/usr/config/emulationstation/es_systems.cfg').read_bytes()
assert len(raw)<=4*1024**2
names=[n.text for n in ET.fromstring(raw).findall('./system/name')]
assert all(absence.values()) and 'steam' not in names
print(json.dumps({'scope':'GENERIC_X64 selected packaging absence only','absent':absence,
                  'steam_system_absent':True,'es_systems_sha256':hashlib.sha256(raw).hexdigest()}))
PY
```

Expected original0 proves absence only. It neither passes nor fails the ARM64
installer's recovery behavior. Passing the exact source path to a fixture does
not convert its private chroot into an installed-image Steam proof.

## Selected SM8550 payload and native execution remain separate

When the existing SM8550 build lane produces the corresponding candidate, first
use its completed build/output/source custody to identify its actual SYSTEM.
Reuse the read-only SYSTEM reader from `tools/pixelelated-state-check`/the existing
image verifier; resolve absolute image symlinks inside that image. The minimum
installed-byte comparison is `/usr/config/modules/Install Steam.sh` against the
frozen source path above, SHA256 fab7cdb4…9229d,124320B, mode0755. Also compare
`Uninstall Steam.sh`, `/usr/bin/{start_steam.sh,start_steam_arm64.sh,start_steam_x86.sh}`,
`/usr/config/fex-emu/{Config.json,AppConfig/steamwebhelper.json}` and
`/usr/share/steam/registry.vdf` to their selected source/package inputs, and require
the Steam system in shipped es_systems.cfg. Preserve actual SYSTEM/file hashes,
modes, link resolution and source commit; original checker0 is package identity,
not execution. The existing prior FEX verifier is
`docs/qa-logs/2026-10-11-device-refresh/sm855005/prepared/verify-fex.py`; reuse its
**file/ELF checks** against the new package/SYSTEM, not its old hardcoded owner,
Nix-cache invocations or old receipt. Required native FEX ELF is machine183;
GuestThunks and GuestThunks_32 must remain machine62/class64 and machine3/class32.

The ordinary full caller fixture is x86_64 ptrace-specific and rejects ARM64;
its staged profile/transport/binary seams remain synthetic even if its input
comes from SM8550 SYSTEM. Do not remove its architecture guard to claim native
installed acceptance. No ready accepted native-Steam harness was found.

For an independently admitted ARM64 runtime with the real prepared support tree,
actual loader closure and a disposable account-free profile, the existing first
launch command is exactly:

```sh
LD_LIBRARY_PATH=/storage/.local/share/Steam/lib/aarch64-linux-gnu/ \
  /storage/.local/share/Steam/steamrtarm64/steam -deckard -exitsteam
```

Record its original process exit/stdout/stderr and descendants directly under
root's bounded owner; do not invoke it here or on x86_64. Actual real payload,
loader, graphics/session prerequisites and a finite native-launch allocation
remain unresolved, so this is a held command, not a runnable accepted plan or a
new release criterion. Installer line2703 deliberately tolerates native failure;
`start_steam.sh` also exits0 after its loop and removes its temporary child-exit
file. Neither outer0 is a native-success discriminator. Existing synthetic SIGKILL
and committed-update cases establish neither power-loss recovery nor real
Steam self-update/consumer quiescence. Those limits must remain explicit.

## Issue criterion readback

- #564 criterion4 asks **new-source installed VM proof**; component runtime39 and
  complete caller evidence satisfy only their declared synthetic scope. Generic
  absence cannot tick installed runtime preservation on the selected ARM64 image.
- #579 criterion4 asks **candidate-source installed VM proof and review**, with
  native execution limits explicit; synthetic FEX43 plus caller evidence do not
  validate actual installed FEX fetcher/overlay closure. Keep that distinction.
- #580 criterion4 uses the same installed-VM wording and separately identifies
  native Proton/Steam usability; Proton56 plus caller evidence are not native
  Wine/Proton runs and may not be relabelled installed by copying their source.
- #582 criterion5 requires reviewed full-caller fresh/retained/allowed-alias VM
  receipts and explicit installed-image/native ARM64/self-update/quiescence/
  power-loss limits. Nine targeted passes and the remaining14 source cases are
  separate from selected-image byte identity and native qualification.

This reconciles the current architecture selection with existing criteria; it
does not waive them, close an issue, add Steam to GENERIC_X64, authorize an owner
handheld action, or create a new user-feature gate.

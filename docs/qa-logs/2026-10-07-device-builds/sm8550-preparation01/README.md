# SM8550 preparation — #492

Prepared while H700 firmware compiles. No SM8550 checkout, compiler or firmware
artifact exists yet. `prepare.py` refuses to proceed until the H700 artifact
acceptance and its process/seal verification both pass. It creates a fresh named
build branch from published `next` only if product paths still equal H700's
accepted frozen source and measured capacity meets the 347,688,935,424-byte
stage budget. The actual invocation remains pending.

The prepared runner uses the canonical Docker target and pinned container. It
builds ARM compatibility output, records its bytes with a Python 3.10-compatible
helper, and then builds the aarch64 firmware. The recorder's three controls ran
inside the pinned container against disposable copies of three accepted H700
ARM binaries: exact hashes/classification, symlink preservation, and refusal
when RetroArch is missing without altering an existing manifest. All fixtures
were removed. These are tooling checks, not SM8550 qualification.

After preparation, run guarded host preflight before the standard build watcher.
Do not reclaim swap while any watcher/compiler/guest is active. Attach the
standard automatic acceptance follow-up with `verify-firmware.py` sealed before
submission. It checks independent artifact custody, installed identity and ARM
handoff, GPT system/storage layout, raw/update SYSTEM and kernel equality, and
actual ABL boot files. The acceptance template has been syntax checked; it has
not yet run on newly built SM8550 artifacts. Physical boot remains separate.

The sealed controller owner is
`/workspace/tmp/pixelelated-m7-sm8550-sequence-01`. Its `state.json` heartbeat,
`controller-result.json`, and each stage's standard watcher/result files are
the live state. A preparation receipt does not mean it was launched. The
controller waits in a standard watched stage, consumes H700 acceptance and
actual exits, then freezes SM8550 and runs host preflight between watched
stages. It submits the build and its separate acceptance watcher, records the
actual container/mounts, and updates #492 and M7 on start and acceptance.
Any artifact failure stops advancement and keeps the failed owner. A tracker
write failure is reported separately while the active build remains supervised.
It creates no physical-device action or release publication. Off-session chat
alerts are still #395; local state/heartbeat recording is not a chat alert.

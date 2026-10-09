# Frontend startup readiness — #529

The unmodified replacement18 guest reproduced the first-start failure on its
normal boot: Sway's service reported started at monotonic10.034s; ES started
at10.079s and failed SDL video initialization at10.890s with `wayland not
available`. Its automatic second start succeeded. An injected eight-second
compositor delay caused four SDL failures before the original frontend reached
idle at9.990s. This proves a common startup ordering defect on the VM. The
retained Nova excerpts omit SDL's second error line, so attribution of its
particular retry remains a hardware observation, not a proved VM equivalence.

## Fix and boundary

The Wayland frontend unit now runs `sway-ready` before ES. The helper uses the
same profile environment, performs an actual read-only Wayland round trip
with wlr-randr, then queries Sway for an active output with a valid mode. It
returns immediately when ready, waits approximately15seconds otherwise, bounds
each protocol probe, and logs a failure on timeout. The service imposes a
20second start deadline and retains its existing2second restart policy.
A stale socket inode is insufficient. Readiness does not guarantee a compositor
will remain healthy after the check; normal frontend restart recovery remains.

The helper belongs to the Sway package and declares bash, busybox, jq and
wlr-randr dependencies. Its actual install hook copied the exact executable
bytes in a temporary staging directory. `pkgcheck sway`, shell syntax and
whitespace checks pass. ES C++ and its pin, Sway's source version, settings
formats and cloud behavior are unchanged. Full custom systemd unit overrides
retain their existing precedence; the change does not rewrite owner settings.

## Observed controls

| Control | Result |
| --- | --- |
| Unmodified natural boot | One SDL/video failure, successful automatic restart; full multiline journal retained |
| Original +8s compositor delay | Four SDL failures; idle9.990s |
| Fixed default startup | No SDL failures/restarts; idle0.687s |
| Fixed +8s delay | No SDL failures/restarts; idle8.636s |
| Fixed +22s delay | One visible guard timeout, automatic recovery; idle22.738s, no premature SDL launch/failure |
| Already responsive compositor | Immediate success (9ms in this guest) |
| Missing Wayland socket | Bounded refusal |
| Stale socket inode | Bounded refusal despite healthy separate Sway IPC |
| Hung compositor | Bounded refusal; success after resuming it |
| No active output | Bounded refusal; success after restoring output |
| Absolute Wayland socket path | Success |
| Retained-storage VM reboot | New boot, zero restarts/SDL errors, unchanged synthetic save/helper/unit hashes; idle14.348s after request |
| Original/fixed1280×960 carousel | Reviewed PICO-8 carousel; pixels identical, zero masks |

The11 fixed controls are counted in `fixed-controls/evidence/summary.json`.
These short timings describe this VM, not Nova boot speed or a game launch
benchmark. No gameplay was exercised. All four watched owners have their
original five zero result channels and verified host exits in
`original-results.json`; the VM was then stopped and its disk and synthetic
keys retired. `retirement.json` records released allocated bytes. Existing
accepted firmware/source-custody bundles remain unchanged.

## Evidence and remaining work

- `source-bindings.json`: exact tested helper/unit/recipe hashes and base source.
- `installed-source.json`: VM startup source matched to the accepted device
  source8b511; ES source1d76b3d is common to both architectures.
- `baseline-journal.txt`: full natural first-boot failure, including the detail
  omitted by the old error-only collector. These are synthetic VM logs.
- `original-control/`, `fixed-controls/`, `retained-boot/`: frozen executable
  harnesses, original results, journals and timings. Temporary runtime helper
  paths are recorded; they are the only unit-path substitutions in the tests.
- `evidence-index.json`: source-bound unchanged-presentation proof for the
  canonical menu map. This does not replace the accepted image's visual baseline.

This is a local implementation review and target-runtime proof, not a new
assembled firmware qualification or independent release audit. #529 stays open
for inclusion/installed-byte checks in the next candidate and the applicable
release delta review. Nova's driver/panel timing remains explicitly unverified;
any future physical reboot/capture needs named authorization after owner use.
No handheld was contacted in this investigation.

Already written: the old startup path wrote no new data format read by this
helper. Existing storage, profile overrides and settings are retained. The
runtime reboot proves retained synthetic data; a new firmware's actual
upgrade/install qualification is still required before an RC claim.

Learning: capture complete bounded journal events, including multiline error
messages. Filtering only lines containing ERROR discarded SDL_GetError()'s
explanation in the earlier device excerpts; a generic renderer error is not
its underlying cause. Source reports it before SDL window creation.

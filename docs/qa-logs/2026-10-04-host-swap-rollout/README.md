# Actual host swap-helper rollout — #410

The owner installed the corrected immutable652ec25fed bundle and supplied
matching visudo, ownership, mode and digest output. This is the actual serval
host boundary; the earlier37-case simulated guard suite and independent
#411 review are separate evidence.

At16:15UTC the installed helper was root:root0755 with the expected SHA256;
the corrected zz policy was root:root0440 and the old policy was absent.
The policy digest in installed.json is attributed to the owner's installer
readback: the unprivileged agent cannot directly read a root0440 policy.

The noninteractive sudo probe uses -k to ignore cached authentication. The
exact permitted action reached the root helper and refused the owned live
watch-job PID before mutation. PYTHONPATH contained a failing sitecustomize;
isolated Python did not import it. Extra arguments and unrelated /usr/bin/true
both required authentication and never reached the helper. The owned job and
watcher exited normally. No broad sudo permission was introduced.

At16:17:24UTC tools/build-preflight --reclaim-swap returned0 after9.578seconds.
The real kernel swapfile remained active at priority-1, its size unchanged,
with8388604KiB free. Pre/post /proc/swaps and preflight output are retained.
Available RAM remained37252MB after recycling. A later exact invocation during cache copying refused the active watcher:
swap had refilled. No second recycle occurred while that job was active;
after preparation finished, the16:32:37UTC recycle and immediate repeat both
returned0. Swap was active with all8GiB free and original priority; the repeat
reported READY/no change. This second sequence took13.999seconds including
the no-op. Its pre/post counters and logs are retained separately. No guest or build was active
when reclamation ran; the busy probe had exited. No frozen build input changed.

This proves the normal actual-host grant/refusal/recycle/no-op paths. Failure
recovery, signals, lock conflicts and malformed observations remain covered
by isolated controls, not destructive host fault injection. SIGKILL and power
loss cannot execute cleanup. Future use is explicit tools/build-preflight
--reclaim-swap before a build watcher starts; default preflight stays read-only.

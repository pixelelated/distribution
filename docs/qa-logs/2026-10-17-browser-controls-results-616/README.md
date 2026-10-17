# Diagnostic browser controls — VM results, #616

This is a direct-launch functional check on the unchanged077197/ES16dbac image,
in a fresh1GiB,640x480,software-rendered VM with no external NIC. The clean-state
gate passed before staging. It does not qualify GTK4, Blink, hardware acceleration,
normal ES/broker handoff, provider usability, input latency or memory savings.

The first driver inherited a1MiB file-size limit into WebKit and exited with
SIGXFSZ(-25). Raising only that ceiling to128MiB allowed rendering; the explicit
log, memory and deadline guards remained. The backing file that hit the limit was
not identified. Attempts2/3 rendered the clean page, but lacked an accepted DOM
report. Attempt3 proved the POST arrived with matching Origin and was refused by
schema validation. Attempt4 adds an animation-frame/positive-viewport wait and
bounded rejection diagnostics. Earlier failing attempts remain intact.

Actual per-attempt outcomes are in analysis.json and originals/functional*/.
The latest attempt's result is **PASS**. Reviewed native frames and
their limits are in frame-review.json. Do not turn a server request or a visible
input into proof of typing, authentication or usable-provider latency.

All original browser outcomes, guard results and frontend restoration are kept.
The enclosing lifecycle completed and all host/QEMU identities exited; its
PASS means export and shutdown succeeded, independently of failed test cases.
The admission was consumed and only its owned VM disk and firmware were removed.
Tiny compiled helpers remain outside Git for the immediate #616 provider tests.

Executed drivers are retained in originals/ beside their results. The reusable
source companion remains ../2026-10-17-browser-controls-vm-616/. Build/parser
evidence is ../2026-10-17-browser-controls-build-616/. No product source, ES pin,
device, credentials, cloud or firmware changed. Loopback HTML reports only
synthetic fixed-schema measurements and UA hashes; no account information.

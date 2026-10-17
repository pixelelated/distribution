# #616 provider instrumentation — source and compile evidence

The diagnostic helper compiled successfully for **GENERIC_X64 and H700**.
All **14 actual x86 pre-GTK configuration cases passed**, including refusal of
both empty and nonempty `CLOUD_SIGNIN_DEBUG`. This packet does not contain a
browser, provider, normal-handoff, or device performance result.

The exact candidate C SHA256 is
`63b8cf5725652874f361aa5fe04abe2b5f326b1cb9ae113590d5c422f9e16b6d`.
It adds bounded main-document request-UA hash/status/error records, isolated-world
DOM-UA and numeric trusted-input probes, and a pre-GTK debug-logging refusal.
Native browser behavior, UA modes, and periodic observer controls remain intact.
The always-on event probes still add diagnostic overhead when the periodic
observer is off; this is not an uninstrumented browser.

## Results

| Evidence | Actual result |
| --- | --- |
| Two-target compile owner | PASS, 2.580 seconds |
| Actual pre-GTK parser cases | 14/14 PASS, 0.182 seconds |
| Original shell / inner wrapper / Docker CLI | All exit0 |
| Original command / watcher / runner / launcher | All exit0 |
| Container CPU and memory contract | CPU4, one CPU; 1 GiB memory; zero swap |
| Cgroup peak | 212,680,704 bytes / 202.83 MiB |
| Cgroup memory-limit and OOM event deltas | All0 |
| Cleanup receipts | Container absent; no surviving host command-group members; sampler threads exited |
| Admission | `f94742d08d05481790d8fb18484d217e`, consumed 2026-10-17 05:17:43 UTC |

The compile used the pinned builder image and accepted read-only GTK3/WebKitGTK
2.54.1 toolchains at their original canonical container paths. Container
inspection and a nonce handshake preceded the compiler. The original run was
`20261017T051712Z-dc9a7da8` in the frozen `m7-p5-build-20261015-03` checkout.
The canonical source commit remained
`077197e6cd3ea31f33b28aaf3882a694b3423b53`.

Host telemetry has **one memory sample and two allocation samples** because
this run was short. Its recorded host swap-counter delta0 does not establish
zero swap activity throughout the run. The cgroup peak is a kernel peak counter;
allocated disk maxima are sampled. No browser-memory savings can be inferred
from these compiler measurements.

| Diagnostic artifact, retained outside Git | Bytes | SHA256 |
| --- | ---: | --- |
| GENERIC_X64 | 66,576 | `8c3a9ba06dc78efffee68bb510b5f273f2fafc8d2ecbc8ee17227a3e4c1e3f0a` |
| H700 | 84,824 | `8da94f0cf89b4788c8e3186eb272e9a9d7d67163a5b3d120d99a4c85aff353be` |

Both ELF binaries remain in the compile owner's `out/` directory for immediately
queued qualification. They are deliberately absent from this Git-ready packet.
Their byte hashes were rechecked while packaging against the original acceptance
record. Readelf text and every other accepted evidence hash are retained.
Admission consumption releases the reservation, not those retained outputs.

## Later runtime evidence and remaining limits

At compilation time the signal callbacks and isolated-world script were unrun.
The subsequent [functional packet](../2026-10-17-provider-functional-616/README.md)
records this same GENERIC helper in a WebView: local original/redirect HTTP UA
calibration, request/DOM-UA hashes, normal ES/broker handoff, and real Google
Drive/Dropbox forms. Those later observations supersede the historical UNRUN
runtime status in this packet's preserved preparation/qualification records.
Native trusted-input remains unproved after the local fixture's pre-POST refusal;
matched performance, hardware memory and complete account linking remain unrun.
Compilation/parser checks alone are not browser runtime or privacy validation.

Missing or mismatched request UA evidence withholds UA-ranking claims; useful
fixed-UA page/input/error/memory observations remain independently interpretable.
Even successful loopback header calibration does not guarantee the UA on a
provider's network request. HTTP200 and a hittable input do not exclude a provider
error, unsupported-browser page, or challenge. Those require reviewed frames
and explicit classification; no credentials or consent submission are involved.

Every subsequent runtime allocation follows the coordinator's current VM
networking and normal-broker plan. The earlier source packet's no-NIC proposal
is historical preparation, not a granted allocation or proof of normal handoff.
This packet neither launches a new test nor establishes a new gate on other
memory investigations. GTK4/Blink work is separate.

## Contents and custody

* `instrumentation/`: the original source packet, fixtures, strict parser, API
  bindings, pure-source checks, and prepared C, **unchanged byte-for-byte**.
* `compile-preparation/`: original preparer/template, source checks, and README,
  **unchanged byte-for-byte**.
* `originals/owner/` and `originals/run/`: lossless gzip copies of the actual
  compiler, parser, cgroup/host telemetry, admission, source-owner, watcher,
  launcher, acceptance, and consumed-admission records. Gzip mtime is0 for
  deterministic storage. Readelf's inherited trailing whitespace is preserved.
* `qualification.json`: compact current findings derived from those originals.
* `provenance.json`: original path, raw size/hash, stored path/hash, and encoding
  for every copied original; both excluded ELF artifacts are named and hashed.

The two historical source READMEs still say their compilation/runtime was unrun
at preparation time. They were not rewritten after the fact. This outer README,
qualification record, and actual originals establish the later compile result.
The packager read and rehashed files only; it did not rerun compilation, inspect
Docker/process state again, or manufacture producer return-code files. Cleanup
claims cite the original owner and consumed lifecycle receipts plus the
coordinator's review, not a newly run test.

Verify this packet without executing any browser or compiler:

```sh
sha256sum -c SHA256SUMS
python3 -I -B verify.py
```

To inspect an individual original, decompress it to stdout or separate scratch;
for example, `gzip -dc originals/owner/stages/compile/inner-result.json.gz`.
Do not edit or normalize the stored originals. No ELF payload, credential,
authorization URL, provider response, cookie, or personal device data was added.

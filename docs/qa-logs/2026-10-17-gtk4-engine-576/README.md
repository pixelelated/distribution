# #576 WebKit6 engine compilation evidence

The original GENERIC_X64 WebKit2.54.1/GTK4/API6 engine build completed on frozen
source969354955741d6c0ca8ce816e1c59ad338b1605b. Original build/inner wrapper,
canonical Docker/make stage, watch command/monitor/runner and durable launcher
results are all0. Docker's exit propagates through the canonical make/watch
path; stage/host-result.json retains that original make result.

Owner elapsed time: **2155.316882s**. Recorded compilation cgroup peak:
**14,397,218,816bytes**, under its20GiB limit, with4CPUs0–3 and zero cgroup swap.
Cgroup OOM counters stayed0; host OOM count did not increase. Host swap activity
is retained separately in the resource evidence. These are build measurements;
they establish no browser runtime memory savings or performance comparison.

The owner and exact container were absent in the recorded terminal host census.
The original admission was consumed at2026-10-17T05:41:38.531808Z, with outputs
held. Engine artifacts remain in the isolated build checkout for further work.

`originals.json` maps45 unchanged source/result records to their stored paths,
raw lengths and SHA256 values. Four large text logs and the executed owner source (which contains inherited
trailing whitespace) are losslessly gzip-compressed
with deterministic timestamps. `source/` preserves the exact owner/sampler/
inner/source-verification/launcher code. `originals/` preserves original status,
resource, nonce/container identity, admission and terminal evidence. No ELF or
account/OAuth/private provider material is included. No original byte was edited.

`SHA256SUMS` covers every packet member except itself. The standalone verifier
checks stored hashes, exact membership, lossless originals, distinct return
channels, measurement bindings, nonce/container identity and recorded cleanup.
It performs only local reads, hashing, decompression and JSON checks:

```sh
python3 -I -B verify.py
# While indexed originals remain available, also compare every original byte:
python3 -I -B verify.py --check-originals
```

Closure findings, normalized package/sysroot identity and the separately scoped
compile-only qualification belong to the companion closure packet. The strict
closure result remains independent of this successful engine compile. Loader,
sandbox, input, rendering, provider login and production suitability require
their own evidence; this packet grants no runtime authority.

# #583 additive review correction — 2026-10-14

Supersedes only the **unrun candidates and next fixture command** from
`819d1c30ec6bc4d7354babecec1b84ceed960189`. That packet, its source readbacks,
and static receipts remain byte-for-byte unchanged. No production file or pin
changes in this revision. The concurrent #584 launcher change is separate.

**A — allocation statement corrected.** The original
`bytes(output[leading_bytes:])` first constructs a bytearray slice of the full
requested size. Its claim of at most three additional allocated bytes was false.
The revised candidate uses `bytes(memoryview(output)[leading_bytes:])`: the output
bytearray grows by at most three bytes, the final bytes result has the requested
size, and temporary memoryview objects add interpreter-dependent overhead. It
avoids the additional full-size bytearray slice. This is source analysis, not a
measured memory saving or target peak-memory claim.

**B — traversal restricted.** The original candidate's global nonempty failure
set allowed traversal of every indexed root. The revised condition admits only a
root containing a failed RVZ path, using the same lexical Path relationship as
the walk's membership test. This adds no filesystem resolution/read or custom
root to the allowed walk. The existing custom-path/D-RA-013 policy, automatic
top-up, exclusions, cap, cursor and valid unmatched hashes stay unchanged.

`fixtures/probe.py` is an additive adapted copy of the original full prepared
fixture. It reads original source from the adjacent immutable packet and revised
candidates here. All inputs are sealed in `fixture-inputs.json`. Its new
`unrelated` case places a zero-hash RVZ in GameCube and a valid unmatched ISO in
an indexed PSX root, includes both roots in the configured walk, records actual
`os.walk` roots, and requires that PSX is **not walked**. The wrapper delegates
calls unchanged to `os.walk`; it does not fake traversal results. Existing
preservation checks cover both roots. Cases run for baseline/candidate and
explicit/indexed modes; all prior controls are retained.

**UNRUN.** Static AST, identity, exact-diff and whitespace checks only. No fixture
or product import/execution, native library, compiler, VM, listener, account or
network-provider action. No memory measurements. The upstream contribution
routing and remaining native/offline qualification gates in the original README
continue to apply.

Coordinator next allocation: stage this packet **and the original packet as
adjacent directories**, verify both SHA256SUMS manifests. In the same disposable
no-NIC VM boundary described by819, from this new packet directory run once:

```sh
timeout --signal=TERM --kill-after=5s 45s python3 -I -S -B fixtures/probe.py --output /run/pix583-revision01
```

Do not run the old probe as well. This is one proposed allocation with old-source
controls retained, not a repeat of an executed run. Limits are unchanged:
512MiB address-space,30CPU seconds,40-second internal alarm,2MiB per file;
16MiB asserted aggregate scratch, optional32MiB coordinator-owned finite scratch
for a hard cap. Runtime results and original exits remain to be recorded by the
coordinator. Changes are source-review corrections, not runtime findings.

`bindings.json` retains old/reviewed/revised source hashes and uncompressed patch
hashes. Compressed patches apply to the same original baseline source as819,
not on top of its candidate. `static-result.json` contains inspection results.

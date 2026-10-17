# #576 GTK4 native-input fixture compilation — 2026-10-17

The fixture compiled successfully against GTK 4.24.1 and WebKitGTK 2.54.1 from
frozen checkout `969354955741d6c0ca8ce816e1c59ad338b1605b`. Original compiler,
compile wrapper, inner wrapper, Docker, command, monitor, runner, and launcher
returns are zero. Owner elapsed time was **1.8460479939822108 seconds**; the
compiler's own recorded interval was 0.27957473089918494 seconds. Compilation
cgroup peak was **118,661,120 bytes**, with no recorded cgroup OOM events.

The admitted owner used CPU 4, 2 GiB with no container swap, network disabled,
read-only source/toolchain/common Git mounts, 512 MiB output allowance, and a
90-second producer plus 30-second cleanup deadline. It finished without deadline
overrun. Exact container and host-owner absence is recorded in
`originals/owner/terminal-host-census.json`; admission
`9af04cefcbab47e6afaf83f15efd1039` was consumed at
`2026-10-17T05:51:31.164776+00:00`, retaining outputs.

This is compilation evidence only. The explicit qualification permitted this
compile despite six inherited search-path findings; the strict closure check
remained FAIL. Its original v4 inventory/receipt hashes remain unchanged here.
The closure companion packet owns that inventory and subsequent checks. No
target execution, trusted-input behavior, provider login, runtime qualification,
or memory savings are established by this packet.

`originals/owner/` preserves the original plans, qualification, resource samples,
source bindings, results, acceptance, and terminal census. `originals/run/`
preserves admission and watcher results. `source/` preserves the compile-input
source and complete preparer packet. Historical `SOURCE_ONLY`/`PREPARED_UNRUN`
labels describe preparation time; the later original run receipts establish
execution. `originals.json` maps every retained file to its original path, raw
byte count, and SHA-256. One whitespace-bearing original diff is stored as
deterministic gzip without changing its decompressed bytes.

No ELF is included. The original result binds the 27,056-byte output to SHA-256
`27908eb5badf203de53332c4e35ee96d8c7fbbb6afefd5d72d11c9d8068359f8`;
the packet verifier checks that receipt, not the excluded binary. No private
OAuth/provider material is included.

From this directory, run `python3 -I -B verify.py`; add `--check-originals` while
the indexed original paths remain available. Verification only reads files,
hashes, decompresses, and checks JSON receipts. It launches no recorded command.
`SHA256SUMS` covers every packet file except itself.

Publication destination: `docs/qa-logs/2026-10-17-gtk4-input-compile-576/`.

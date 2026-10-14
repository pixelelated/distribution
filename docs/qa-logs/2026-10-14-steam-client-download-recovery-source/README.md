# #582: preserve the failed public acquisition and recover its verified payload

Additive source packet after **6c27adda2326d4f5792051abdc738ad49e53ea8c**.
The original packet, download directory and owner remain unchanged. The new
corrected downloader, recovery helper and VM receipt adapter are **UNRUN**.
Only source/AST/bytes and small original receipts were inspected here; the
archive payload was not opened, hashed, decoded, copied or executed.

## Original result and one-field correction

[original-observation.json](original-observation.json) is a derived readback,
not a replacement result. [source.json](source.json) binds all ten download
receipts and six owner files, including the complete console, by original path,
size and SHA256. Original paths:

- `/workspace/tmp/pix-steam-public-download-20261014/download01`
- `/workspace/tmp/pix-steam-public-download-20261014/owner`

The original result and wrapper/launcher all remain **FAIL / 1**. Curl-version,
transport and full-file SHA256 children each returned **0**, no intervention,
no remaining process group or cleanup timeout. Transport completed HTTP200,
verified TLS, no redirect/retry/proxy, exact payload **110373661 bytes**; the
separate hash child reported full SHA256
`8b31d0b0aa844d906b690283da41403b601a9b36b1f80b7819d1f85bb27854fc`.
The wrapper failed after these checks at `KeyError('request_size')`, before its
PASS update. Its original total work/cleanup was 24.029309488949366 seconds.
This is original acquisition/hash evidence, not format or native-client proof.

The official [curl write-out documentation](https://curl.se/docs/manpage.html#-w)
was checked 2026-10-14: **`size_request`** is the HTTP-request byte counter;
`size_header` describes HTTP response headers. Neither measures aggregate wire
traffic. Original curl8.18.0 JSON has `size_request=221`, `size_header=555` and
no `request_size`. History locates the mistaken key in the initial 6c27 wrapper.
No upstream curl defect, update or transport workaround is implicated.

[download.diff](download.diff) changes exactly
`metadata['request_size']` to `metadata['size_request']`. All other bytes,
transport argv, checks and bounds remain identical. There is no missing-key
fallback or weakened predicate. This prospective correction is supplied for
source review; **do not redownload the completed object** for this recovery.
No source pin, installer or acquisition policy is changed.

## Separate honest recovery receipt

[recover.py](recover.py) is scoped to those exact original host directories.
It creates only a fresh independent output owner. It does not write, rename,
copy, truncate or delete the archive or any original receipt.

Before accepting the original evidence it verifies all pinned receipt hashes,
original FAIL reason/source/limits, original version/transport/hash argv and
child results, the original disk margin/deadline, TLS/HTTP/URL/redirect/encoding,
exact byte count and SHA receipt. The corrected request field remains mandatory.
Wrapper and launcher must still contain their original1. Missing, replaced,
aliased, oversized or changed receipts refuse; no generic failed run qualifies.

Then it launches **only the byte-identical `hash_archive.py`** against the retained
archive, read-only. That existing helper requires a single-link regular file of
the exact advertised length, checks all bytes against the selected manifest hash
and detects identity/time/size changes during the read. The parent also compares
archive identity around recovery and rechecks all original receipt bindings.
This new check establishes current integrity independently of the earlier hash;
it never parses ZIP/ELF or executes downloaded content. It was not run here.

The fresh result uses `phase=metadata-recovery`, schema1, `status=PASS` only after
all checks, and explicitly retains `original_status=FAIL`, `original_wrapper_exit=1`,
the original result/source hashes and every original receipt binding. It records
one **historical** acquisition attempt and **zero new download attempts**, plus
the new hash child and its raw stdout/stderr/result hashes. No old FAIL is
rewritten to PASS, and no new successful-download receipt is fabricated.
A failure produces its own FAIL and keeps its evidence and original payload.

The source-sealed runner and its process-group/pidfd/subreaper cleanup are
unchanged. The new hash-only recovery gets its own finite **180-second** work
budget plus at most **10 seconds** child cleanup, **384MiB address space**,
CORE0, original CPU/file limits and **64KiB per child log**. This is a distinct
new operation, not an extension or replay of the original acquisition deadline.
The conservative original ordinary free-space margin181676829 is retained;
recovery writes only small reports and does not allocate another archive.
No privilege, mount, service, package or network operation is requested.
Total wire bytes remain **UNMEASURED**.

## Offline verifier compatibility

[vm-verify.diff](vm-verify.diff) adds an explicit `--recovery` input. Without it,
the existing original-success predicate still applies. The original failed
`download01/result.json` alone remains inadmissible. With it, the adapter requires
the current packet's separate PASS recovery receipt and all original FAIL
bindings, checks the fresh hash child/receipt and identity/counters, and records
**both** original and recovery receipt hashes. The staged original result is
never rewritten or relocated to masquerade as recovery.

Stage the original download directory directly under the admitted VM scratch,
with its ten original receipts plus archive; stage the recovery directory as a
separate sibling. Absolute host paths in original argv are historical provenance,
not paths opened by the VM. The adapter opens only the explicitly staged archive.
Do not compare host inode/device numbers with a new guest copy.

`verify_archive.py`, `hash_archive.py`, `runner.py`, the eight bound metadata
files and VM admission schema are byte-identical to6c27. The decoder SHA remains
`84d8951b926651ac44929b1e642f57808d7d85fbe6940159e724887942725b51`.
Every original VM predicate, dedicated private scratch/mount/source/expiry gate,
90s verification +10s cleanup, 768MiB scratch maximum, 384MiB decoded total and
address-space cap, 128MiB/member, 128 entries and64KiB logs remains. The unchanged
decoder hashes the **entire staged file before decoding**, regardless of which
receipt path admitted it. CRC/layout/name/link/ELF checks and no payload execution
are unchanged. Native ARM64 readiness, manifest signatures, self-update safety,
existing-client classification and installed-image acceptance remain separate.

## Next coordinator command — UNRUN

Can this be done on the VM? Yes: archive decoding remains a separately allocated
offline guest operation. The approved ordinary-host intake contract permits
read-only full SHA256; this worker has only prepared its next command. No runtime
lease, redownload or new VM is granted by this packet.

From the assigned checkout, under a fresh coordinator-owned watched operation:

```sh
TMPDIR=/workspace/tmp/pix570-parallel-20261013/tmp \
python3 -I -S -B docs/qa-logs/2026-10-14-steam-client-download-recovery-source/recover.py \
  --download /workspace/tmp/pix-steam-public-download-20261014/download01 \
  --owner /workspace/tmp/pix-steam-public-download-20261014/owner \
  --output /workspace/tmp/pix-steam-public-download-20261014/recovery01
```

Require new wrapper/launcher0, recovery PASS and original FAIL1 unchanged; fresh
hash child0, no intervention/remaining group/cleanup timeout, exact size/hash,
original request counter221, no new transfer. Preserve the separate owner and
all original receipts. Do not reuse a failed recovery directory.

Only after the coordinator consumes that result and allocates an offline VM,
stage this whole sealed source packet, `download01/` and `recovery01/`. Bind the
VM admission to this packet's **new SHA256SUMS hash**, not6c27's. Existing source
seal will refuse any unmanifested file. Then, with real allocated scratch and
admission variables:

```sh
python3 -I -S -B docs/qa-logs/2026-10-14-steam-client-download-recovery-source/vm_verify.py \
  --scratch-root "$VM_INTAKE_SCRATCH" \
  --output "$VM_INTAKE_SCRATCH/verify01" \
  --archive "$VM_INTAKE_SCRATCH/download01/archive.zip" \
  --recovery "$VM_INTAKE_SCRATCH/recovery01/result.json" \
  --admission "$VM_INTAKE_ADMISSION"
```

Do not invoke the decoder on the host or turn a metadata-recovery result into
archive-format acceptance. VM full hash/CRC/layout/ELF evidence remains UNRUN.

[qualification-plan.json](qualification-plan.json) lists bounded positive and
negative controls, all UNRUN. They use fresh synthetic receipt copies or small
mutations in disposable VM input, never the original owner; no malformed input
stands in for the real positive archive. They are proposed qualification, not
new public RC criteria or authorization to run them now.

[verify_static.py](verify_static.py) ran AST/byte checks only; results are in
[static-result.json](static-result.json). It imports no runtime module and never
opens the archive. It checks all sealed originals, the exact single-key diff,
unchanged download/VM predicates, helper bytes and limits. No shared record or
GitHub write, runtime, VM or product operation occurred in this assignment.

Both documented runtime command blocks passed `bash -n` without execution.
The reproducible source-only check is:

```sh
python3 -I -S -B docs/qa-logs/2026-10-14-steam-client-download-recovery-source/verify_static.py
```

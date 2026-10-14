# #574 chdman static closure — prepared, UNRUN

This is one readelf-only step for the coordinator's existing admitted owner,
after a successful `chdman-build`. It creates no owner, container, admission,
clock, service or target process. No new build or compiler invocation. The
existing owner must retain control of its deadline, resources and cleanup;
this command does not extend a family clock or authorize execution after expiry.

The adaptation comes from successful
`2026-10-14-dolphin-loader-resolution/closure.py` at
`4d15c80dce0b91eb0adf40fd24f156c5e771238a`. Four ELF parsing/resolution functions,
eight common helpers and `loader_resolution.py` are reused verbatim. There is
no Docker/lifecycle code here. The Dolphin resource/notices copying is removed;
only actual recursive ELF dependencies are staged. This is a private QA payload,
not a release package or a redistribution/license audit. Retain the sealed source
plan and its attribution records alongside the evidence.

## Exact inputs and build receipt

The referenced runner is
`m7-steam-preservation-integration/docs/qa-logs/2026-10-14-chdman-build-runner`.
Its `inner.py` writes `target-artifact.json` **after** successful selected build
and generated-file checks. `bindings.json` records the exact inspected source
hashes; that checkout was read only. This packet does not freeze its evolving
lifecycle implementation or change any of its files.

Pass that original build stage's receipts read-only as `/build-receipts`.
The checker requires its original `container-result.json` PASS, identical
source-before/after inventory, healthy sampler, and exact original
`selected-stage.json` child exit 0/reaped/no forced group stop. The dynamically
read target path/size/SHA256 must match both the real ELF at
`/work/format-tools/mame-24cffe763621b164fc10be2ae3660f140be25182/chdman`
and its post-build generated inventory. No preset chdman hash, wrapper hash,
recovered-failure bypass or receipt rewriting is accepted. Host attach/container
termination, admission consumption and cleanup remain separate coordinator
acceptance; this inner receipt does not replace them.

`--plan` must be the **byte-identical** sealed `1c0e93` `input-bindings.json`,
SHA256 `d3841143585153f060f19144a7e3fb55e003b88dfdd8b4c752374845e61296a4`.
The upcoming CHD runner's unchanged `plan/` copy meets that contract. MAME pin
is `24cffe763621b164fc10be2ae3660f140be25182` (0.289); the existing private
shared-libstdc++ link-policy patch remains the build runner's responsibility.

Keep the existing read-only retained cache mapping:

```text
host: /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20
  -> /workspace/repos/rocknix.worktrees/m7-pixelelated (read-only)
```

The toolchain is `build.pixelelated-GENERIC_X64.x86_64/toolchain` beneath that
mapping. Readelf is pinned to SHA256
`831dfa5f667cdaab85df5e27d88107899b18bdfaa0b6d72bd4909d7832f3aa9b`.
Every selected library needs an exact byte/size binding from the sealed plan or
the retained C/C++ runtime recorded by the successful Dolphin closure. Those
additional core-runtime hashes were compared read-only with retained bytes here;
that historical receipt is provenance, never permission to replay owner04.
Compiler and unused cache-input integrity remains the build runner's contract.

The unchanged SDK resolver accepts only `/lib64/ld-linux-x86-64.so.2` and
`/usr/lib/ld-linux-x86-64.so.2`, both mapped to the exact retained
`sysroot/usr/lib/ld-linux-x86-64.so.2` (1,352,760 bytes, 0755, SHA256
`ce676fd2c523729f7660bfaf1e34f7c221cb70bb7c238feb8ffd46c9bc00ff29`).
Unlike Dolphin's specific interpreter assertion, either source-backed alias is
allowed for the new ELF; its actual string and resolution are recorded. Any
other path, conflicting SDK alias, escape, absent/mismatched library or differing
candidate bytes refuses. There is no host-library or basename fallback.

## One coordinator command, not an allocation

Use the existing owner's readelf-capable environment with the mappings above,
the successful private work tree read-only at `/work`, the sealed plan read-only
at `/plan`, this complete packet read-only at `/closure`, original build-stage
receipts read-only at `/build-receipts`, and a fresh owned receipt location at
`/receipts`. The output child must not already exist. No mounts are performed by
this packet. If the existing owner has no time or cannot supply these inputs,
stop for coordinator admission; do not replay a retired owner or silently reset
its deadline. Python 3.10+; no external Python dependencies.

```sh
python3 -I -S -B /closure/closure.py \
  --plan /plan/input-bindings.json \
  --work /work/format-tools \
  --build-records /build-receipts \
  --output /receipts/chdman-closure-01
```

The existing owner's child wrapper retains this command's original exit/stdout/
stderr. The only subprocesses it starts are the pinned readelf with
`--wide --file-header --program-headers --dynamic --version-info --notes`.
Each has the unchanged 30-second child bound, original PID/start identity,
stdout/stderr and exit/reap receipt. Existing limits remain 128 ELF objects,
256 MiB per object, 512 MiB closure/copy, 32 MiB stdout/1 MiB stderr per readelf
after exit. Diagnostic-size checks are not streaming quotas; the enclosing
owner enforces total wall/disk/resource bounds and whole-container cleanup.
This step supplies no independent watchdog or new time allowance.

Accept only original command 0, all `elf-N.json` readelf exits 0 with empty
stderr, unchanged build/input/library hashes, `elf-closure.json` status
`STATIC_CLOSURE_ONLY`, and `bundle-receipt.json` with `target_executed=false`.
Retain every raw readelf receipt/output, parsed version-provider check, alias
candidate map, original build-receipt hash and manifest. A failure keeps its
partial output and original exit; there is no retry/delete/overwrite path.

## Staged output and distinct VM gate

```text
chdman-closure-01/
  elf-N.{start.json,json,stdout,stderr}
  elf-closure.json
  bundle-receipt.json
  vm20-bundle/
    manifest.json
    chdman                        # actual receipt-bound ELF
    ld-linux-x86-64.so.2
    lib/<each needed SONAME>      # regular byte-verified copies
```

No Sys assets or other converter executable. Revalidate the manifest when
coordinator stages the fresh no-NIC VM. For accepted `76f44e` CHD execution
packet, the exact program maps to `/run/pix574-chd/chdman`, the staged libraries
to `/run/pix574-chd/chdman-lib/`, and the private loader can be kept at
`/run/pix574-chd/ld-linux-x86-64.so.2` for the separate comparison/load gate.
Do not pass a loader wrapper as `--chdman-sha256` input. The actual installed
and private loaders must be compared and exercised in the VM before conversion;
chdman help's actual exit/output also remains unmeasured. This packet performs
none of these actions. No native engine, ROM, account or network input.

The parser preserves RPATH/RUNPATH and checks version **names** against retained
providers; it does not emulate ld.so search/relocations or prove dynamic dlopen,
NSS, IFUNC, kernel/CPU compatibility, actual load/help, CHD correctness or ES
integration. Static success must not be relabelled as VM execution proof.

## Static checks and prepared refusal criteria

`static-validation.json` records AST parsing (Python 3.10 grammar), exact reused
function/file comparisons, sealed plan identity and source call-site inspection.
No module was imported, fixture launched, readelf run or target executed here.
`SHA256SUMS` seals this packet. Runtime adaptation is **UNRUN**.

For coordinator review/controlled checks, these expected outcomes remain UNRUN:

| Input/control | Required result |
| --- | --- |
| Successful build's untouched receipt-bound target | Stage only actual ELF closure; preserve raw readelf and provider checks |
| Target byte/size/path changed or wrapper substituted | Refuse before first readelf |
| Failed/forced original build child or changed generated inventory | Refuse before first readelf; original failure stays unchanged |
| Unpinned or unreadable required library/readelf | Refuse; no host fallback |
| Exact legacy loader alias with absent SDK `lib64` | Resolve the pinned canonical SDK loader |
| Escaped/conflicting alias, duplicate dependency, absent version provider | Refuse without executing target |
| Library, alias or build receipt changes during inspection/copy | Refuse final acceptance; keep partial receipts |
| Output already exists | Refuse; no replay or overwrite |

Shared decisions, work logs, issues, product source, original packets and
coordinator runner are unchanged. No push, allocation or runtime occurred.

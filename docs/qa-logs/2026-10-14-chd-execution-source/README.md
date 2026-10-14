# #574: remaining CHD/Saturn/CUE and cross-format execution map

Source-only **UNRUN** packet. Parent052b36080f. Complete live #574 body/comments
were read on2026-10-14; exact intake is retained here. This is a narrow selection
from the immutable `2026-10-13-rvz-regression-source/run-regressions.py`, not a new
build or lifecycle harness. Coordinator alone admits compilation and guest work.
Can this be done on the VM? Yes: all inputs are legal self-created bytes; no
owner ROM, account, provider, device, emulator or frontend service is required.

## Concrete prerequisite and existing artifacts

**Only chdman and its qualified target loader/library closure are still missing
for this selected run.** Coordinator is preparing MAME0.289 source
`24cffe763621b164fc10be2ae3660f140be25182` under the existing1c0e93 plan. This
packet neither starts nor changes that plan. Its final executable SHA256, ELF
interpreter/DT_NEEDED, exact closure identities, build/source receipts and actual
VM loading/help evidence must precede acceptance. No target hash is invented;
`--chdman-sha256` must come from that fresh accepted build/closure, not a hash of
an arbitrary substitute. The runner additionally requires an actual x86_64 ELF.

All nine retained artifacts under
`/workspace/tmp/pix574-md5-target-20261014/artifacts` still match their accepted
compile-result SHA256 values. `input-bindings.json` records every exact file,
length and hash. This run executes only the fixture writer and two wrappers;
the other four executables remain unexecuted. The two sanitizer libraries are
runtime dependencies.

| Input | Disposition |
|---|---|
| candidate/pix574-fixture-writer | Available469304bytes; makes new official GC/Saturn inputs. Its fixed writer also emits unused Wii-helper data; no Wii test is run. |
| candidate/pix574-regression-hash | Available7906968bytes, SHA2565e00ed65…; exact314da58d composition. |
| baseline-repaired/pix574-regression-hash | Available7245840bytes, SHA256e95d6423…; a7dcdbb plus only the identical MD5 repair. Never label it pristine baseline. |
| candidate and baseline-repaired pix574-md5-alignment / pix574-wii-partition-probe | Available, hash-bound, excluded from execution. |
| lib/libasan.so.8 and lib/libubsan.so.1 | Available; leak/alignment/undefined-behavior checks stay enabled. |
| pix574-rvz-reader-probe / pix574-padding-oracle | **Absent from these nine. Not required or proposed for compilation:** their separately accepted tests are excluded. |
| corrected generator1dd4eb12… | Available in052b36080f; raw ISO and expected hashes unchanged. |
| target libzstd.so.1 | Available8163ae3e… in the retained Dolphin bundle; used solely by the legal generator. No Dolphin binary is called. |
| target chdman / post-link closure | Pending coordinator build/qualification, sole selected native prerequisite. |

The old full runner cannot be pointed unchanged at these artifacts: it binds
candidatebb9e2785 and pristine baselinea7dcdbb source files, the old malformed
RVZ generator, and calls two missing executables plus completed suites.
`run-chd-regressions.py` explicitly replaces that obsolete source-input selection
with the accepted314da58d artifact/source-contract bindings and repaired-baseline
label. It reuses **byte-identical bounded.py** and the original selected command
vectors/expected answers. Old source bindings, generator and proofs stay immutable.
No rebuilt baseline, suppressed sanitizer or broad failed-build exception is used.

Original MD5 compile wrapper FAIL1 remains in provenance. The separate exact
cleanup recovery accepted all four compile stages0, nine artifacts and compiler
contracts; the subsequent actual MD5 guest proof passed. Those distinct receipts
are hash-bound in `completed_proof_records`, never rewritten or relabelled.

## Exact selected commands and acceptance

Paths below are relative to the new private work/output directories. Every
original stdout, stderr, PID/process group, exit, elapsed time and executable
hash is retained by the unchanged bounded helper. Any failure stops the sequence.

| Order / label | Command substance | Bound / expected result |
|---|---|---|
| 1 make | Actual retained candidate fixture writer → fresh fixtures/ |30s,0, empty stderr; preparation only. |
| 2 make-rvz | Corrected make-fixtures.py → fresh rvz-cases/, exact target libzstd |30s,0, empty stderr; generation only. Validate full manifest and exact synthetic.iso/mixed-zstd.rvz/ordinary.nes identities against attempt02. |
| 3 chd-create | Actual chdman `createcd -i saturn.cue -o saturn.chd -c none -np 1` |30s,0, output>124bytes; retain progress stderr as the original runner did. No stub or conversion fallback. |
| 4–5 baseline-repaired-formats/repeat | Actual repaired baseline: GC ISO → Saturn ISO → CUE → new CHD → GC ISO, once then16times |30s/60s,0, empty sanitizer stderr; exact5/80 ordered hashes. |
| 6–7 candidate-formats/repeat | Same new CHD-bearing sequence in actual candidate |30s/60s,0, empty sanitizer stderr; same5/80 hashes. |
| 8 rvz-cd-transition | Candidate: CHD → corrected mixed-zstd.rvz → ordinary NES → CUE,16times |60s,0, empty sanitizer stderr; exact64 hashes. |

That is **seven native child commands plus one Python generator**, five wrapper
invocations and234 ordered hash rows. GC/Saturn ISO/CUE participate only in the
new CHD-bearing state transitions. The already accepted standalone ISO/CUE
subset is not separately rerun. Official expected hashes stay:

- Official GC: `c7803b704fa43d22d8f6e55f4789cb45`.
- Saturn ISO/CUE/CHD: `4cd9c8e41cd8d137be15bbe6a93ae1d8`.
- Corrected RVZ: `118545082f24fc195a446d1ee7bbf816`.
- Ordinary NES: `6d2fc9abd70a8d230dc90b972aa9a00e`.

No `chdman verify` is added: this is an uncompressed/writable CD CHD, outside
that command's documented verification scope. Actual wrapper content hashes
are the acceptance here. No compressed-codec, multitrack/audio, whole Wii,
CHD/native-proxy parity, ARM/big-endian or gameplay acceptance follows.

## Completed proof exclusion and #574 criterion mapping

| Criterion or earlier suite | This packet's contribution / boundary |
|---|---|
| #574 source/runtime support and launcher gates | No new claim; current package/installed/frontend work remains coordinator-owned. |
| #574 recognition and offline-index trace | Cross-format wrapper/callback regression only; accepted Dolphin/native-proxy proof retained, not rerun. Main/systemd/current-native provenance remain separate. |
| #574 source-bound reproduction/repair | Adds the previously blocked real-CHD branch and CHD/RVZ/CD transitions to accepted repaired compositions. Must still pass actual runtime. |
| #574 disposition/flow/screens | No UI or player-copy change, no new screenshot claim, no issue closure. |
| 528 MD5 vectors, ISO/CUE-only subset, Wii-helper positives/short refusal | Accepted md5-result; excluded. Old alignment UB stays recorded. |
| Four-reader lifetime/concurrency and five padding vectors | Accepted separate original instrumented subset in #574 comment6159175863; excluded; no missing-probe rebuild requested. |
| Independent Dolphin 5decode/2encode/2roundtrip/2hash | Accepted attempt02 with corrected generator; excluded. |
| Native proxy ISO/RVZ parity and state/queue branches | Accepted proxy-native attempt01 within its recorded scope; excluded. |
| Malformed/unsupported RVZ full suite | Not silently repeated by this CHD selection; any remaining criterion needs its own coordinator mapping. |

## Fresh input tree, limits and next serialized command

Use the existing coordinator VM owner/lifecycle machinery. This file is a
**case runner, not an outer process owner**. The coordinator must enforce240s
for all guest work plus cleanup, track/retire the descendant groups (including
on parent/serial interruption), collect original exits, sample disk/RAM and
retire the guest after evidence export. This runner checks a235s shared work
clock at every child boundary and passes the lesser of the original per-command
bound and remaining time to bounded.py. There is no per-case extension. Its
result carries `outer_cleanup_required:true`; case PASS alone is insufficient.

Proposed existing envelope: no-NIC VM20, private executable tmpfs at most2GiB,
128MiB free after staging, guest work235s plus5s cleanup. No address-space cap
that breaks ASan; unchanged `detect_leaks=1:halt_on_error=1:abort_on_error=1` and
`halt_on_error=1:print_stacktrace=1`. Normal account/home variables are replaced
with fresh synthetic HOME/XDG/user labels. No mounts or services are created by
the runner. Python3.11+ is required by the immutable bounded helper.

Exact layout (coordinator assembles and verifies, UNRUN here):

```text
/tmp/pix-input/pix574-chd/                 public read-only
  packet/                                all flat files of this new packet
  original/make-fixtures.py               exact052b generator, descriptor in binding
  original/upstream/rvz-go-license        unchanged padding attribution/licence
/run/pix574-chd/                          coordinator exec tmpfs0700, max2GiB
  artifacts/                             all nine exact retained MD5 artifacts
    candidate/...
    baseline-repaired/...
    lib/libasan.so.8
    lib/libubsan.so.1
  chdman                                 actual accepted target ELF
  chdman-lib/                             coordinator-qualified target closure
  lib/libzstd.so.1                        exact retained generator dependency
  work/                                  MUST NOT exist before this run
/tmp/pix-output/                         writable evidence destination
```

Inspect/bind chdman's interpreter and closure before assembling that directory;
do not guess dependencies or install libraries in outer `/usr`. The selected
runner verifies the actual converter hash, nine artifacts, generator and libzstd;
it does **not replace the coordinator's loader-closure qualification**. Retain
that qualification's manifest/receipts with this new admission. The native paths
above must contain actual binaries, never loader wrappers substituted for hashes.

After fresh build/closure and VM admission, set `PIX574_CHDMAN_SHA256` from the
accepted executable receipt. The exact next selected command is:

```sh
python3 -I -S -B /tmp/pix-input/pix574-chd/packet/run-chd-regressions.py \
  --chdman-sha256 "$PIX574_CHDMAN_SHA256" \
  --output /tmp/pix-output/pix574-chd-01
```

The existing outer owner must wrap that command and retain its original exit.
Do not run it directly as an unsupervised serial command. Use a fresh output ID
for any later admission; never replay a consumed owner. Result/logs stay under
the output path; fixtures and CHD are in `/run/pix574-chd/work`. Export the CHD,
its CUE/BIN source identities and result manifest if immediately needed for
later native parity, then let coordinator retire the VM/scratch. Do not claim
native-proxy CHD parity from these frontend-wrapper results.

Static validation here only: complete issue/receipt/source reads, all nine
artifact hash checks, AST parsing without importing runners, exact bounded.py
identity, unchanged expected answers and selection/exclusion inspection. No
compiler/configure/export, generator, fixture, loader, container or VM ran.

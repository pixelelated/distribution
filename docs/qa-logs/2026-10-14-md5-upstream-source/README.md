# #574 MD5 upstream contribution candidate — source only

Disposition: a narrow correction belongs in **libretro/libretro-common**, whose
`utils/md5.c` implements the affected routine. This is not an rcheevos-owned fix.
The local clean patch and public reproducer are ready for review; submission is
held for a separately admitted upstream standalone before/after run and explicit
posting authorization. No upstream posting, branch, push, compiler, container,
VM, test execution, or shared-record edit occurred in preparing this packet.

Only `contribution/md5-alignment.patch` is the proposed product diff. Its sole
path is `utils/md5.c`:10 additions/1 removal, carrying the exact314da58d helper,
comment and macro with `MD5_u32plus` spelled `uint32_t`, as current upstream uses.
No public API typedef is reintroduced. Alexander Peslyak/Solar Designer's original
public-domain dedication and fallback permissive license remain byte-identical.
The generic architecture branch and every other upstream byte remain unchanged.
The patch applies to current upstream without needing the fork's commit history.

`contribution/` is the standalone public bundle. It contains the exact34-line
MIT-labelled alignment control from314da58d, six unmodified upstream source/header
files, the one-file patch, a source manifest, and prepared reproduction/comparison
helpers. The compile-only type-name define keeps the control byte-identical;
no sanitizer is disabled or aliasing warning hidden. Only the patch belongs in
a product PR; the bundle can accompany the report or be adapted into upstream's
preferred test location after review. Fork records, private paths and UI changes
are absent from that patch and public bundle. `DRAFT-PR.md` is local draft copy.

## Dated upstream source and history check

On2026-10-14, direct unauthenticated GitHub GETs resolved master to
[a3194c18ba65ef89734e1898a2f61403c255d368](https://github.com/libretro/libretro-common/commit/a3194c18ba65ef89734e1898a2f61403c255d368)
(committed2026-10-11). Current [MD5 source](https://github.com/libretro/libretro-common/blob/a3194c18ba65ef89734e1898a2f61403c255d368/utils/md5.c)
is byte-identical to its most recent file change,
[39eae6ac1c4e4dd809f27cec210ace8d62a5c0a5](https://github.com/libretro/libretro-common/commit/39eae6ac1c4e4dd809f27cec210ace8d62a5c0a5)
on2026-08-23. That change removed an Apple-only guard, leaving the cast/load intact.
The API returned no releases; this bundle targets a commit, not a claimed release.

All11 returned `utils/md5.c` history entries were inspected as source. The Solar
Designer cast-load path appears in the2015-10-21 snapshot and each later returned
revision; earlier snapshots use a different implementation and are not included
in that inference. By7040de62 (2026-04-19) the word type is `uint32_t`, compared
with the earlier/downstream `MD5_u32plus`. Current source also changes local
variable declarations relative to our vendored copy; those differences are left
alone. `upstream-review.json` retains exact commits, public URLs, response hashes,
source hashes, dates and bounded search coverage.

Six repository issue/PR searches, across both open and closed items, used `md5`,
`alignment`, `misaligned`, `"strict aliasing"`, `"undefined behavior"`, and
`"MD5_SET"`. None was incomplete or paginated. Four returned0. The two results
were read with their full bodies, comments and changed paths:

- [#175: CHD alignment lzma/zlib](https://github.com/libretro/libretro-common/pull/175),
  merged; four CHD codec/header paths, no MD5 change, empty body and no comments.
- [#155: generic mips libco](https://github.com/libretro/libretro-common/pull/155),
  merged; four libco/sample paths, no MD5 change, empty body and no comments.

No direct duplicate appeared within those searches. This does not prove absence
from other wording, repositories, unpublished work or unindexed discussions.
The complete upstream tree response was not truncated and had no repository
CONTRIBUTING file or PR template. No CLA/DCO/author claim is invented here.

Existing [test/utils/test_utils.c](https://github.com/libretro/libretro-common/blob/a3194c18ba65ef89734e1898a2f61403c255d368/test/utils/test_utils.c)
tests empty input and43-byte string updates (including repeated updates), not
arbitrary-offset direct full blocks. Makefile.test compiles MD5 into the utility
and crypto suites with ASan/UBSan; it also pulls broader dependencies and libcheck.
The standalone bundle needs neither suite nor libcheck. Upstream's
[tools convention](https://github.com/libretro/libretro-common/blob/a3194c18ba65ef89734e1898a2f61403c255d368/tools/README.md)
already permits manually compiled source probes; no test-framework rewrite is
proposed. No existing upstream test was run or changed here.

## Evidence boundary and next command

Coordinator's current `md5-host01/stdout` was read and bound in `evidence.json`:
43 recovery controls PASS and target result PASS with ten accepted commands,
264 digest comparisons per repaired composition (528 total), and serial marker0.
The runtime checker source rejects unexpected target exits or any sanitizer stderr.
Coordinator reports guest/serial/wrapper0 and all original commands consumed;
full per-target receipt export will follow guest retirement and was not reopened
or invented by this worker. Keep original compile outer/watcher/launcher FAIL1
and explicit8568 cleanup recovery intact. The older pristine-baseline UB remains
an independent failure finding. These are **ES-integrated target results**, not
a build or run of this upstream source snapshot.

The next new admitted compile/runtime command is solely the standalone before/after
probe, not a replay of the target VM or independent format-tool allocation:

```sh
bash /workspace/repos/rocknix.worktrees/m7-rvz-regressions-574/docs/qa-logs/2026-10-14-md5-upstream-source/contribution/reproduce.sh \
  /workspace/tmp/REPLACE_WITH_NEW_ADMITTED_MD5_UPSTREAM_OUTPUT /absolute/path/to/gcc
```

Coordinator selects the explicit host compiler, fresh owner, current capacity,
standard watched admission and result delivery. The script has two60s compile
bounds, two15s target bounds and10s patch bound, with5s kill grace per command;
it copies only two9.5KiB source files. Preserve compiler/target stdout/stderr and
command exits, result JSON, compiler identity, source/binary hashes and watcher
channels. After consuming them, coordinator retires this fresh scratch.

Required upstream acceptance: unpatched original1 with a matching misaligned-load
diagnostic; patched original0/empty sanitizer stderr and264 exact independent
rows. A timeout, missing reproduction, other sanitizer report, compiler failure,
changed source or output mismatch fails. No platform/performance/security claim
is added. The standalone script, oracle and upstream patch remain **UNRUN**;
static AST, shell syntax, patch reconstruction, source hashes, source-preservation
and314 identity checks are in `static-result.json`. Independent format plan1c0e93
remains separate and unchanged; shared records and product pins are coordinator-owned.

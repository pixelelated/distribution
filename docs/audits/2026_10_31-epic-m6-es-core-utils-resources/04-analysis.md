# Analysis: the second opinion — M6.P2 T36 (#683)

- **Depth:** Independent (one seat, OpenAI GPT-6 Astra at `max`, through the council Facilitator). `review-plan.json`; `second-opinions/`.
- **The two keyed invokes:** the probe (`gpt-probe.md`, served `openai/gpt-6-astra` by OpenAI at max, outcome success) and the refutation (`gpt-audit.md`, 18,169 bytes, 31,078 reasoning tokens, http 200, finish stop, outcome success, ~11.8 min, attempt 1 of 2; `gpt-audit.md.provenance.json`). Every other `tools/council/run` call used `COUNCIL_ENV_FILE=/nonexistent`.
- **The packet:** `t36-packet.md`, 352,038 bytes, 36 sources (15 fork-own whole, 20 cited ranges of the upstream-carried, `02`, the brief's § 4), sha256 `c3b14889`; scan clean (`packet-manifest.json`: 0 forbidden, 0 secret-pattern lines, 138 credential-shaped words all classed, 0 a value). The held implementations (`getEscapedPath`, `getCanonicalPath`) were not in the packet, by design (D-WORKFLOW-215); the seat was told so and graded them `CANNOT-TELL`.

## Executive summary

The forward audit's leads are sound and its new finding L-19 (removeFile leaves the deleted path cached as present) is confirmed on the VM by a unit case (3.26 FAILs `exists(p)==false`). The independent seat (GPT-6 Astra at max) corrected three positives in `02` and, more importantly, found a layer of memory-safety and data-loss defects the audit missed -- four of them confirmed at the pin by the lane: a dangling font-atlas pointer (G-1), a stack buffer overflow in date formatting (G-9), a copy that destroys its source onto the same inode (G-16), and a PDF loader that always reports failure (G-4). The slice is entirely upstream-carried, so every fix is a rule-6 contained change. Ten punch items (three High) are proposed for stage D.

## Second opinion

## The verdict

The seat: **"Usable as a starting punch list, not sound enough unchanged for sign-off. L-19 survives scrutiny... Correct the contradictory positives and add the omitted findings before prioritisation."** The audit is sound in its leads and wrong in three positives; it missed a layer of memory-safety and data-loss defects. All three corrections are taken, and the missed findings are verified at the pin and carried into `05`.

## The lead and floor grades

The seat graded every lead and every floor case against the packet's source. Summary (full table in `gpt-audit.md` §§ 1-2):

- **CONFIRMED (leads):** L-01, L-02, L-03, L-04, L-06, L-07, L-09, L-10, L-11, L-12, L-13, L-15, L-16, L-18, **L-19**. The floor's FAIL-at-pin candidates (3.1, 3.2, 3.3, 3.4, 3.26) and the positives/controls are confirmed.
- **NARROWER-THAN-STATED:** L-05 (the pipe defect is real; status 141 and the launch's signal disposition are not established by the packet — the guest's G-07 `SigIgn=0x1000` is the evidence, and it shows the launch gets EPIPE, not a signal); L-08 (height is stable after a *successful* ASCII preload; a glyph that failed first can grow it later); L-14 (the mask's gaps are real but production credential exposure is unproved; it is not "`=`-only" — it handles flags and commands too).
- **CANNOT-TELL:** L-17 (concurrent callers/GL-thread reachability not supplied); 3.14, 3.19, 3.20, 3.21, 3.25 (the implementations are held or absent from the packet, as intended).

## The three corrections to `02` (all taken)

1. **The `renameFile`/`copyFile` "erase after they write" positive is wrong.** Both `FileCache::remove` calls precede the rename (`FileSystemUtil.cpp:1457-1463`), and `copyFile`'s precede nothing it guards. `02` § Positives is corrected: only the *claim* that these erase after the write is withdrawn; the L-19 contrast (removeFile re-reads between its erase and its unlink) stands.
2. **"Only `fromStat64` refreshes an entry" is false.** `FileCache::add` overwrites an existing entry too (`:168-180`), and the WIN32 `fromStat64` uses `try_emplace` (no overwrite), not the POSIX overwrite. `02` § The file cache is corrected.
3. **"Until a reset" is too absolute for L-19.** `exists(p, false)` refreshes the entry, a writer can invalidate it, and a targeted reset exists; ordinary *cached* reads alone do not repair it. `02` § The file cache and the L-19 text are narrowed to "until a refresh, an invalidation or a reset — ordinary cached reads do not repair it." The functional priority of L-19 is retained (the seat: "retain its substantive functional priority; narrow only the persistence wording").

Minor: the writes table's `:1461` row names `MoveFileW` (WIN32), not `std::rename` — corrected.

## What `02` missed (G-1 to G-21), with the lane's verification at the pin

The seat raised 21 source-supported findings `02` did not carry. The lane verified the highest-severity ones at the pin (`/workspace/tmp/m6-t36/pin`, read, not run); each verified one is a punch item in `05`.

| # | Finding | Lines | Lane's check | → 05 |
| --- | --- | --- | --- | --- |
| **G-1** | font atlas: `tex` pushed to `mTextures` (`:268`) then `delete tex` (`:275`) on the fresh-atlas failure path → dangling pointer / double-delete | `Font.cpp:258-275` | **CONFIRMED at the pin** (push_back precedes delete) | PL, High |
| **G-4** | `loadFromPdf` never sets `retval` on success (`:441` calls `initImageFromMemory` without assigning), returns false after loading | `TextureData.cpp:425-444` | **CONFIRMED at the pin** | PL, Medium |
| **G-9** | `TimeUtil` date format: `char buf[256]`, `*s++ = ...` with no bound → a format over 256 bytes overruns the stack | `TimeUtil.cpp:415-508` | **CONFIRMED at the pin** (no bound on `s`) | PL, High |
| **G-16** | `copyFile` has no `src==dst`/inode guard; opens dest `"wb"` (truncates) before reading source → identical/hard-linked path destroys the source, returns true | `FileSystemUtil.cpp:1481-1509` | **CONFIRMED at the pin** | PL, High (data loss) |
| G-2 | glyph objects leaked (font teardown frees only textures) | `Font.cpp:405,423`; `Font.h:147-148` | source-supported; a leak case | PL, Low |
| G-3 | `rebuildTextures` may deref a null face / ignore `FT_Load_Char` failure | `Font.cpp:376-388,442-454` | source-supported | PL, Medium |
| G-5 | CBZ buffer and VLC argv not released; repeated extraction leaks | `TextureData.cpp:357-408,473-492` | source-supported | PL, Low |
| G-6 | `startsWithIgnoreCase("abc","abc")` advances past both terminators | `StringUtil.cpp:202-210,1032-1042` | source-supported | PL, Medium |
| G-7 | `proper` can split a 4-byte UTF-8 char → `length()-2` underflow into the 4-byte decoder | `StringUtil.cpp:213-218,1144-1149` | source-supported | PL, Medium |
| G-8 | more casing defects than L-01: `unicode_uppers` unsorted for `bsearch`; dotless `ı→I` | `StringUtil.cpp:30,105-108,184-188` | source-supported; widens L-01 | folded into L-01's item |
| G-10 | date parser: literals advance `s` not `parsedChars` → day read past the input | `TimeUtil.cpp:275-335,400-404` | source-supported | PL, Medium |
| G-11 | an in-flight stat inserts its stale result after a reset/invalidation | `FileSystemUtil.cpp:213-215,258-261,313-323` | source-supported; widens L-19/L-12 | folded, noted in L-19's item |
| G-12 | a directory's `/*` wildcard is published before its children are inserted → a concurrent lookup reports a child absent | `FileSystemUtil.cpp:364,370-372,479,277-281` | source-supported | PL, Low |
| G-13 | cached `isRegularFile` reports a FIFO/socket/device as a regular file | `FileSystemUtil.cpp:238-240,294-306` | source-supported | PL, Low |
| G-14 | `removeFile` of a broken symlink: the following `stat64` fails, returns true without unlinking | `FileSystemUtil.cpp:146,1063-1065` | source-supported | PL, Medium |
| G-15 | `createDirectory` returns true for an existing *file* | `FileSystemUtil.cpp:1093-1095` | source-supported | PL, Low |
| G-17 | a quoted credential flag `"--password"` evades `maskSecrets` | `StringUtil.cpp:725-795` | widens L-14 | folded into L-14's item |
| G-18 | `run()`'s log path interpolated unquoted; `2>` binds only the last simple command | `Platform.cpp:162` | widens L-05 | folded into L-05's item |
| G-19 | a signalled `system` child passed to `WEXITSTATUS`; interrupted `waitpid` not retried | `Platform.cpp:167-168,868,876` | widens L-13 | folded into L-13's item |
| G-20 | SVG parsed dimensions reach unchecked `w*h*4` allocation and narrowing to int | `TextureData.cpp:115-198,205-206` | source-supported | PL, Medium |
| G-21 | `getSystemDateFormat(true)` drops the time on Linux; cached formats bypass locale changes | `TimeUtil.cpp:19-111` | source-supported | PL, Low |

**The four CONFIRMED-at-the-pin findings (G-1, G-4, G-9, G-16) are the most consequential** — a dangling font-atlas pointer, a stack overflow, a PDF loader that always fails, and a copy that can destroy its source. None is in the fork's changed lanes (all upstream-carried), so each is a rule-6 contained fix (`bugs-are-agent-first.md`): a guard, a bound, a return value. The remaining G-items are carried into `05` with the seat's lines; the ones that widen an existing lead (G-8, G-11, G-17, G-18, G-19) are folded into that lead's punch item.

## Dissent / what the seat could not reach

The seat graded the held and absent implementations `CANNOT-TELL`, correctly — the packet withheld them (D-WORKFLOW-215) or they are other slices' (`InputManager` for 3.14). Those are not refutations; they are the boundary of what one packet can show. The held leads' public framing was judged "appropriate... does not require disclosure of held details."

## Renovation face

### Q1 Modernize

Raw owning pointers and manual `new`/`delete` are the pre-C++11 idioms here, and they are where the memory-safety bugs live: the font atlas (`Font.cpp:258-275`, PL-06), each glyph (`Font.cpp:405`, G-2), the quit event (`Platform.cpp:235`, L-18), the SDL/VLC argv (`TextureData.cpp`, G-5). RAII (a `unique_ptr`, a container of values) is the modern shape, held for a stream.

### Q2 Standards

The house rules this slice touches: the last known good state (broken — `copyFile` truncates before it reads, PL-08; `writeAllText` is not atomic, L-04), fail-closed (broken — `copyFile`/`renameFile` return true over an absent source, PL-02; `loadFromPdf` returns false over a success, PL-09), verify the artifact not the report (the cache answers a stale `exists`, PL-03/PL-05).

### Q3 Bugs

Three High (PL-06 dangling font atlas, PL-07 stack overflow, PL-08 data-loss copy — all CONFIRMED at the pin by the second opinion), six Medium and one Low in the punch list, plus eleven source-supported findings grouped in PL-10. Each is upstream-carried and a rule-6 contained fix; filed as `bug`s at stage D with traces and `Already written:` lines.

### Q4 Package currency

The slice has no package of its own; its 43 upstream-carried files are byte-identical to `rocknix/master` (`02` § Coverage). Batocera's 13 commits on 9 files are the reconciliation list in `02` § The merge debt.

### Q5 Efficiency

The texture cache reloads a re-sized shared texture synchronously on the caller's thread (`TextureResource.cpp:110-127`); the SVG path allocates `w*h*4` without a bound (G-20). Priced on the guest (G-05: RSS stable under a scroll).

### Q6 Dead ends

No image compiles `Renderer_GL21`/`GLES10`/`GLES20` (G-08, a structure fact); the WIN32 branches throughout are dead on the device. Recorded, not removed (upstream-carried; D-UI-079).

### Q7 Clarity and structure

The two rule errata (L-08 against `es-code-traps.md:118`, L-13 against `es-native-ui.md:103`), the `key`-as-identifier vs credential ambiguity the packet scan surfaced (classed, `tools/t36-packet-disp.json`), and the vendored headers `han.h` and `zip_file.hpp` (#256's PR bucket).

## Acceptance-criteria scorecard

The brief's § 7 acceptance is the checklist on #683. Stage C's part: the membership block, the § 5 runs, `02`'s generated tables (asserted, drift-tested), the unit cases (4 FAIL-at-pin incl. L-19 proved), 3.11's re-run (PASS at the amended tips), the packet (scan clean) and the seat's two keyed calls (probe + refutation, served `openai/gpt-6-astra`), the guest window (G-01..G-10, disk retired). Open: the stand-in's 4 T36 fakes + the renderers positive; the three held public bugs (stage D); the fixes (stage E). No criterion is ticked from memory; each cites its artifact.

## Risk assessment

The three High items are the risk: G-1 (use-after-free / double-delete on a font-atlas allocation failure), G-7/PL-07 (stack overflow from an over-long date format -- a format string is theme/locale data), and G-16/PL-08 (silent source destruction on a same-inode copy -- data loss). Each is upstream-carried and reachable only through specific inputs; none is in the fork's changed lanes, so each is a contained guard. The held trio (archive extraction, canonical-path fold, launch-shell escaping) are weighed under D-WORKFLOW-215 and filed as neutral public bugs at stage D.

## Coverage boundary

The host proved the pure and linkable seams (StringUtil, FileSystemUtil, the text-read extracts) and the file cache; it did not link Font/TextureData/TextureDataManager (the stand-in's 4 fakes are owed) or run the sanitizer programs (3.6/3.11/3.25 at stage E). The guest showed identity, the renderer path, the two font sizes and the pipe/launch disposition; it could not stage G-03/G-04's exact frames (no scraped media) or read VRAM counters. The held implementations were kept out of the packet, so the seat graded them CANNOT-TELL -- the boundary of one packet, not a gap in the review.

## Quality self-check

The generated tables are asserted against the pin and seen to exit 1 on ten drifts. Each FAIL-at-pin case was seen to FAIL against the unfixed code (harness self-coverage). The seat's grades were taken as input, not authority: the four High G-items were re-read at the pin before becoming punch items, and the three corrections to `02` were applied at their lines. One process miss is recorded honestly (a compile overlapped an M7 START; friction logged). The measurement is the lane's own cap-height reader value, named as such, not claimed to match T34's metric.

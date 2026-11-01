# Independent review

**L-19 is real with the file cache enabled.** The audit is useful, but its “until reset” wording, several positives, and some reachability claims need correction. It also misses substantial memory-safety and data-loss defects.

Grades below concern **source support**, not confirmation that the reported or planned tests ran. Filenames refer to the packet’s `es-core/src` paths.

## 1. Lead grades

| Lead | Grade | Reason and source |
|---|---|---|
| L-01 | **CONFIRMED** | Three-byte case conversion uses `+=` instead of assignment, corrupting the encoded bytes (`StringUtil.cpp:357-362,398-403`). |
| L-02 | **CONFIRMED** | A short BOM probe sets failure state; `seekg(0)` without clearing it does not restore the consumed one-/two-byte input (`FileSystemUtil.cpp:1374-1378,1408-1425`). |
| L-03 | **CONFIRMED** | Missing sources report success; copying ignores I/O failures; POSIX renaming does not enforce `overWrite=false` (`FileSystemUtil.cpp:1451-1463,1473-1474,1500-1509`). |
| L-04 | **CONFIRMED** | `writeAllText` truncates in place, returns `void`, and checks neither write nor close results (`FileSystemUtil.cpp:1429-1446`). |
| L-05 | **NARROWER-THAN-STATED** | Early pipe closure is real; status 141 and the actual launch’s signal disposition/reachability are not established by this source packet (`Platform.cpp:162-168`). |
| L-06 | **CONFIRMED** | `popen` failure is unchecked, and every `fgets` chunk loses its last byte whether or not that byte is a newline (`Platform.cpp:894-903`). |
| L-07 | **CONFIRMED** | When size is inherited, `orig->mSize` is already scaled and the new constructor scales it again; an explicit theme size takes a different path (`Font.cpp:99-101,1238-1255`). |
| L-08 | **NARROWER-THAN-STATED** | Height is stable after **successful** ASCII preload; an ASCII glyph that initially failed can be retried later and increase it (`Font.cpp:115-117,385-388,420-421`). |
| L-09 | **CONFIRMED** | Substitutes are measured as `lineHeight` but advance by less when drawn; newline measurement also falls through to glyph advance (`Font.cpp:728-745,1046-1078,1092-1097`). |
| L-10 | **CONFIRMED** | Locking SVG initialization does not synchronize its fields with unlocked `setMaxSize`/`rasterizeAt` accesses (`TextureData.cpp:95,124-143,615-645,670-705`). |
| L-11 | **CONFIRMED** | While `paused` remains true, the wait predicate rejects even `mExit`, so notification cannot release the joins; notifying without holding the mutex is not itself illegal (`TextureDataManager.cpp:225-235,252-255`). |
| L-12 | **CONFIRMED** | Explicit negative entries and parent wildcards suppress fresh filesystem queries until refresh/invalidation (`FileSystemUtil.cpp:213-215,277-281,313-323`). |
| L-13 | **CONFIRMED** | Normally waits through both children, discards their status, ignores `name`/`window`, and returns zero to the caller (`Platform.cpp:853-879`). |
| L-14 | **NARROWER-THAN-STATED** | JSON/colon/header shapes are not covered, but actual logged exposure is unproved here; the implementation is not simply “`=`-only”—it also handles flags and special commands (`StringUtil.cpp:742-795`; `Platform.cpp:855`). |
| L-15 | **CONFIRMED** | The detached lambda captures `trySaveStates` by reference; the static `preloaded` set is also unsynchronized (`FileSystemUtil.cpp:1766-1797`). |
| L-16 | **CONFIRMED** | A competing creator can make both `mkdir` attempts fail with an already-existing directory, yielding false (`FileSystemUtil.cpp:1093-1119`). |
| L-17 | **CANNOT-TELL** | Unlocked maps and glyph uploads are visible, but actual concurrent callers/off-context execution and renderer-wide checks are not supplied (`Font.cpp:161-178,415-417`; `TextureResource.cpp:100-146`). |
| L-18 | **CONFIRMED** | The allocated event is never deleted after `SDL_PushEvent` (`Platform.cpp:235-238`). |
| L-19 | **CONFIRMED** | Cache-on removal erases, repopulates through `isDirectory`, then deletes without invalidating again (`FileSystemUtil.cpp:1067-1084,1181-1184`). |

## 2. Floor-case grades

| Case | Grade | Reason and source |
|---|---|---|
| 3.1 | **CONFIRMED** | The three-byte fixtures exercise corrupting additions; the two-byte branch uses assignment (`StringUtil.cpp:352-362,393-403`). |
| 3.2 | **CONFIRMED** | Missing-source success and POSIX overwrite despite `false` follow directly from the branches (`FileSystemUtil.cpp:1451-1463,1473-1474`). |
| 3.3 | **CONFIRMED** | At this pin there is no returned status to assert; unchecked write/close calls are explicit (`FileSystemUtil.cpp:1429-1446`). |
| 3.4 | **CONFIRMED** | A two-byte file is consumed by the failed three-byte probe and is not successfully rewound (`FileSystemUtil.cpp:1374-1378,1408-1425`). |
| 3.5 | **NARROWER-THAN-STATED** | The wrapper permits producer failure, but exact exit codes depend on signal disposition and producer behavior; the host run is not independently evidenced (`Platform.cpp:162-168`). |
| 3.6 | **CONFIRMED** | A worker delayed until after return dereferences a dead parameter; enforce that interleaving rather than expect ASan to find it every run (`FileSystemUtil.cpp:1773-1797`). |
| 3.7 | **CONFIRMED** | Zero return, unused parameters, and both waits are directly inspectable (`Platform.cpp:853-879`). |
| 3.8 | **NARROWER-THAN-STATED** | Re-measuring successfully cached ASCII passes, but does not prove height immutability after initial glyph failures (`Font.cpp:115-117,385-388,420-421`). |
| 3.9 | **CONFIRMED** | The first 255-byte chunk loses a digit: 300 digits plus newline produce 299 digits (`Platform.cpp:894-901`). |
| 3.10 | **CONFIRMED** | A JSON key’s closing quote/colon bypasses the assignment and whitespace-followed flag tests (`StringUtil.cpp:742-795`). |
| 3.11 | **CONFIRMED** | The proposed overlapping calls access the same size fields without a common synchronization discipline (`TextureData.cpp:95,129-143,620-633`). |
| 3.12 | **CONFIRMED** | With `paused` still true, exit notification cannot satisfy the predicate (`TextureDataManager.cpp:231-235,252-255`). |
| 3.13 | **CONFIRMED** | On POSIX, forced stat overwrites the negative entry; ordinary wildcard hits avoid stat (`FileSystemUtil.cpp:161-162,277-281,1127-1145`). |
| 3.14 | **CANNOT-TELL** | The InputManager implementation and integration test are absent; the cache dependency alone cannot establish that test’s outcome (`FileSystemUtil.cpp:1127-1145`). |
| 3.15 | **CONFIRMED** | Force both initial probes before creation: the losing creator can return false after both `mkdir` failures (`FileSystemUtil.cpp:1093-1119`). |
| 3.16 | **CONFIRMED** | A non-unit scale exposes the inherited-size double scaling; this does not establish shipped-theme reachability (`Font.cpp:99-101,1238-1255`). |
| 3.17 | **CONFIRMED** | Both discrepancies exist; a vertex-based fixture must control bearings and image geometry rather than assume every last vertex equals advance (`Font.cpp:728-745,1046-1078,1133-1157`). |
| 3.18 | **CONFIRMED** | POSIX single-quote construction, embedded apostrophe escaping, and empty-string quoting are correct (`StringUtil.cpp:426-442`). |
| 3.19 | **CANNOT-TELL** | The escaper implementation is absent; seeing the shell sink does not establish escaping coverage (`Platform.cpp:162-168`). |
| 3.20 | **CANNOT-TELL** | The canonicalizer implementation is absent; its visible callers do not prove an array overrun (`Font.cpp:163`; `TextureResource.cpp:88`). |
| 3.21 | **CANNOT-TELL** | The relative/prefix implementations are absent; only a caller is shown, not the alleged `.//a.png` result (`TextureData.cpp:326-329`). |
| 3.22 | **NARROWER-THAN-STATED** | Duration formatting is covered by the cited range, but per-call 12-hour behavior belongs to `localClockText`, not `secondsToString` (`TimeUtil.cpp:207-215,514-580`). |
| 3.23 | **NARROWER-THAN-STATED** | Reverse eligible eviction is visible; MRU maintenance is not, and protected textures can prevent reaching the budget (`TextureDataManager.cpp:146-164`). |
| 3.24 | **CONFIRMED** | The event allocation has no matching deletion (`Platform.cpp:235-238`). |
| 3.25 | **CANNOT-TELL** | Cache locking is inspectable, but the complete pool, `StringListLock`, `ConcurrentVector`, and calling-thread evidence are absent (`FileSystemUtil.cpp:208-215`; `ThreadPool.cpp:22-34,81-99`). |
| 3.26 | **CONFIRMED** | It fails with `UseFileCache` enabled; the harness must set that condition explicitly (`FileSystemUtil.cpp:203-215,1067-1084`). |

## 3. File-cache reasoning

### L-19: the ordering really does leave a positive entry

For an existing ordinary file, with caching enabled:

1. `exists(path, false)` bypasses cache **reads**, but POSIX `fromStat64` still writes the result (`FileSystemUtil.cpp:1064,1142-1145,146-162`).
2. `remove` erases the path and ancestor wildcards (`FileSystemUtil.cpp:1067,183-197`).
3. `isDirectory(_path)` misses, stats the **still-existing** file, and inserts `_exists=true`, `_directory=false` (`FileSystemUtil.cpp:1080,1183-1184,213-215,294-306,323`).
4. It returns false for “directory,” **not** for existence. `unlink` then succeeds without another invalidation (`FileSystemUtil.cpp:1084`).
5. The subsequent cached `exists` returns true (`FileSystemUtil.cpp:1127-1131`).

This also explains why thumbnail expiry skips regeneration at `TextureData.cpp:336-340`.

**“Until a reset” is too absolute.** `exists(p, false)` can refresh it, a writer can invalidate it, and targeted reset is available; disabling cache reads also avoids the stale answer (`FileSystemUtil.cpp:161-162,183-190,203-204,348-351`). Ordinary cached reads alone do not repair it.

### #1271: yes, the entry is shared

`exists` and `isRegularFile` apply different predicates to the same lookup and stored entry (`FileSystemUtil.cpp:200-240`). An engaged `optional<bool>` containing false is still a cache hit. With caching enabled, a cold `isRegularFile` query itself populates the cache; its `fromStat64` fallback is not a general refresh path for cached callers (`FileSystemUtil.cpp:1164-1177`).

The audit’s stat-versus-listing symlink inconsistency is also supported (`FileSystemUtil.cpp:146-152,238-240,433,575`).

### Locks: map safety is not cache coherence

- The shared lookup and exclusive insertion discipline is sound for protecting the map and consuming entry pointers (`FileSystemUtil.cpp:208-215,313-323`).
- The double-check does **not** prevent an old, in-flight stat from being inserted after invalidation; see G-11.
- “Only `fromStat64` refreshes” is false: `add` overwrites existing entries too (`FileSystemUtil.cpp:168-180`). Also, its Windows counterpart uses `try_emplace`, not overwrite (`FileSystemUtil.cpp:141-144`).
- The hash key is `size_t`; the source does not establish the audit’s universal “64-bit collision” qualification (`FileSystemUtil.cpp:331-337`).
- `isCached` avoids filesystem I/O, but its `shared_lock` can block; “non-blocking” is not literally guaranteed (`FileSystemUtil.cpp:223-235`).

Moving L-19’s erase after deletion fixes the deterministic self-repopulation, **not every concurrent invalidation race**.

## 4. Processes, writes, and held paths

- **L-13:** the blocking/zero-status diagnosis is correct. “For the command’s whole run” needs an interruption caveat because neither `waitpid` is checked or retried (`Platform.cpp:868,876-879`).
- **L-05:** the pipe defect is real, but this packet cannot establish httplib’s signal setup, the running process’s `SigIgn`, or the distribution wrapper. Do not turn the conditional hazard into a proven handheld launch termination (`Platform.cpp:162-168`).
- **L-03/L-04:** the return-value diagnoses are sound. However, **refute the positive claiming `renameFile` erases after writing**: both erases precede the rename (`FileSystemUtil.cpp:1457-1463`). Likewise, the whole helper is not an atomic replacement when it first deletes the destination (`FileSystemUtil.cpp:1454-1455`). The Windows table also misnames `MoveFileW` as `std::rename` (`FileSystemUtil.cpp:1461`).
- **Held paths:** the neutral, non-certifying public framing is appropriate. The packet does not contain those implementations, so neither escaping coverage nor the canonicalizer overrun can be independently confirmed. This does not require disclosure of held details.

## 5. What `02` missed

These are additional source-supported findings, not claims of demonstrated exploitation.

- **G-1 — Dangling font atlas / double deletion:** a failed fresh-atlas allocation path deletes `tex` after pushing it into `mTextures`; the next glyph or font teardown dereferences/deletes that dangling pointer (`Font.cpp:244-250,258-275,122-130`).
- **G-2 — Glyph heap leak:** each glyph is allocated and stored through a raw pointer, but font destruction deletes only textures; font/theme churn leaks glyph objects (`Font.cpp:405,423,122-130`; `Font.h:147-148`).
- **G-3 — Unchecked font reload failure:** `rebuildTextures` dereferences a possibly null face and ignores `FT_Load_Char` failure; unavailable font data during reload can crash rather than follow `getGlyph`’s guarded failure path (`Font.cpp:376-388,442-454`).
- **G-4 — PDF loader always reports failure:** successful image initialization never changes `retval`, so `loadFromPdf` returns false even after loading pixels (`TextureData.cpp:425-444`).
- **G-5 — Extraction allocations leak:** the CBZ compressed-image buffer and VLC argument array have no release; repeated extractions accumulate allocations (`TextureData.cpp:357-408,473-492`).
- **G-6 — Equal-prefix comparison reads past the strings:** `startsWithIgnoreCase("abc","abc")` reaches two zero terminators but has no terminating branch, then advances beyond them (`StringUtil.cpp:202-210,1032-1042`).
- **G-7 — Valid UTF-8 can reach an overread through `proper`:** it splits the first byte from a four-byte character; the resulting one-byte input underflows `length()-2` and enters the four-byte decoder (`StringUtil.cpp:213-218,1144-1149`).
- **G-8 — More casing defects than L-01:** `unicode_uppers` is unsorted for `bsearch`, and dotless `ı→I` is still emitted through the two-byte encoder; fixing `+=` alone cannot make these conversions correct (`StringUtil.cpp:30,105-108,184-188,393-397`).
- **G-9 — Time formatter stack overflow:** a format producing 256 bytes overruns the fixed buffer at least with its terminator; no output bound is checked (`TimeUtil.cpp:415-424,501-507`).
- **G-10 — Date parser overread:** literals advance `s` but not `parsedChars`; parsing `2026-01-` with `%Y-%m-%d` consequently permits day reads beyond the input (`TimeUtil.cpp:275-295,313-335,400-404`).
- **G-11 — In-flight stat defeats reset/invalidation:** a reader can stat the old filesystem state, another thread deletes and resets, then the reader inserts its old result after reset (`FileSystemUtil.cpp:213-215,258-261,313-323`).
- **G-12 — “Directory enumerated” is published before enumeration:** a concurrent lookup between wildcard publication and the child’s insertion reports an existing child absent (`FileSystemUtil.cpp:364,370-372,479,277-281`).
- **G-13 — Cached regular-file classification is wrong for special files:** an existing FIFO/socket/device is neither directory nor symlink and therefore reports “regular file” with caching enabled (`FileSystemUtil.cpp:238-240,294-306`; contrast `:1177`).
- **G-14 — Broken symlink removal reports false success:** the initial following `stat64` fails on the target, so `removeFile` returns true without unlinking the symlink (`FileSystemUtil.cpp:146,1063-1065`).
- **G-15 — Existing file accepted as a directory:** `createDirectory` returns true for any existing path, including an ordinary file (`FileSystemUtil.cpp:1093-1095`).
- **G-16 — Copying onto the same inode destroys the source:** identical paths or hard-link aliases are opened first for reading and then with `"wb"`; truncation precedes the first read, and the function returns true (`FileSystemUtil.cpp:1481-1509`).
- **G-17 — Quoted credential flags evade masking:** quoting the flag itself, such as `"--password"`, prevents the whitespace-followed flag branch from masking its following value (`StringUtil.cpp:725-752,787-795`; logging sink `Platform.cpp:855`).
- **G-18 — Wrapper redirections change command semantics:** raw log paths containing spaces/metacharacters are interpolated unquoted; for a compound command, appended `2>` redirects only the final command rather than the whole group (`Platform.cpp:162`).
- **G-19 — Process wait-status handling is incomplete:** a signalled `system` child is passed straight to `WEXITSTATUS`, potentially appearing successful; interrupted `waitpid` calls can also end waiting prematurely (`Platform.cpp:167-168,868,876`).
- **G-20 — SVG dimensions lack safe arithmetic bounds:** oversized parsed dimensions reach unchecked conversions, `width * height * 4` allocation, and narrowing to rasterizer `int` dimensions (`TextureData.cpp:115-119,145-198,205-206`).
- **G-21 — Another date-formatting contract is broken:** on Linux, `getSystemDateFormat(true)` takes `D_FMT` without appending hours; cached formats also bypass later setting/locale changes (`TimeUtil.cpp:19-25,89-111`).

## 6. Verdict

**Usable as a starting punch list, not sound enough unchanged for sign-off.** L-19 survives scrutiny and should remain a concrete defect—not be dismissed as merely an outside-writer cache contract. Correct the contradictory positives and add the omitted findings before prioritisation.

Severity/confidence adjustments:

- **L-05:** conditional producer/output failure, not proven unconditional handheld launch termination.
- **L-14:** demonstrated masking limitations, not yet demonstrated production credential exposure.
- **L-17:** investigation/open item until actual concurrent callers and GL-thread reachability are established.
- **L-08:** conditional rule correction; do not claim the warm-ASCII test proves universal immutability.
- **L-19:** retain its substantive functional priority; narrow only the persistence wording.

The newly identified memory-safety and destructive-copy paths warrant attention before treating L-18’s small quit-path leak as representative of the remaining lifetime risk.
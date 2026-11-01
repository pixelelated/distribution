# Punch list (Phases 5 and 6) — M6.P2 T36, EmulationStation's utilities, resources and renderers (#683)

`question:` is the brief's § 4 numbering (Q1 the file cache, Q2 the texture/font caches, Q3 the paths, Q4 the processes, Q5 the writes, Q6 the device reads and words, Q7 structure/merge debt). Every item is upstream-carried (the 58 have 0 fork hunks beyond the 15 whole files; `02` § Coverage), so each contained fix is a **rule 6** bug (`bugs-are-agent-first.md`): a guard, a bound, a return, a quote. The four CONFIRMED-at-the-pin findings the second opinion added (G-1, G-4, G-9, G-16) are the most consequential. The items are **proposed dispositions**; the stage-D pause records the coordinator's rulings and any stream brief before a fix lands.

reviewed-at-es: 16dbac5211eea7e70db7394372033be2be7df829

fixed-at-es: (pending stage E)

**Second opinion:** independent, GPT-6 Astra at max (`04-analysis.md`, `second-opinions/gpt-audit.md`): verdict "usable as a starting punch list, not sound unchanged"; L-19 confirmed; three positives corrected in `02`; 21 missed findings (G-1..G-21), the four CONFIRMED-at-the-pin carried here as PL-06..PL-09.

## PL-01: toUpper/toLower fold a multi-byte codepoint byte-wise, and the casing tables are unsafe

- **Severity:** Medium; **category:** Words; **question:** Q6
- **Source finding:** L-01, 3.1 (FAIL at the pin), G-8
- **Lines at the pin:** `StringUtil.cpp:357-362`, `:398-403`; `:30`, `:105-108`, `:184-188`
- **Owner:** T36 (rule 6)
- **What is wrong:** `toUpper`/`toLower` build the result with `+=` on bytes, corrupting a 3-byte codepoint (3.1 FAILs: `toUpper("\xE1\xBA\xA1")` ≠ `"\xE1\xBA\xA0"`). G-8 widens it: `unicode_uppers` is unsorted for the `bsearch` it feeds, and dotless `ı→I` is emitted through the 2-byte encoder, so fixing `+=` alone does not make the conversion correct.
- **Proposed disposition:** a `bug`: decode a full codepoint, map it, re-encode; sort the table (or use an ordered map); 3.1 the covering case plus a sorted-table and dotless-i case; a #585 line.
- **proved:** fix-unit-test (3.1 FAIL at the pin, `stage-c/build-tests.out`)

## PL-02: copyFile returns true over an absent source and over a short write

- **Severity:** Medium; **category:** Writes; **question:** Q5
- **Source finding:** L-03, 3.2 (FAIL at the pin)
- **Lines at the pin:** `FileSystemUtil.cpp:1472-1474`, `:1500-1509`
- **Owner:** T36 (copyFile's half; `renameFile`'s absent-source half is T21's #1191, a collision)
- **What is wrong:** `copyFile` returns true when the source does not exist (`:1472-1474`), and ignores `fwrite`/`fclose` results so a short write (full disk) reports success. 3.2 FAILs both `CHECK_FALSE`.
- **Proposed disposition:** a `bug`: return false on an absent source, check the byte count and `fclose`; 3.2 the covering case; a #585 line.
- **proved:** fix-unit-test (3.2 FAIL at the pin)

## PL-03: removeFile leaves the deleted path cached as present

- **Severity:** Medium; **category:** File cache; **question:** Q1
- **Source finding:** L-19 (new), 3.26 (FAIL at the pin), G-11
- **Lines at the pin:** `FileSystemUtil.cpp:1067`, `:1080`, `:1084`; reaches `TextureData.cpp:336-340`
- **Owner:** T36 (rule 6)
- **What is wrong:** `removeFile` erases the entry (`:1067`), then `isDirectory(_path)` re-stats the still-present file and stores `_exists=true` (`:1080`), then unlinks (`:1084`). A cached `exists(p)` then answers true until a refresh/invalidation/reset. 3.26 FAILs `CHECK(exists(p)==false)` with `true == false`. It explains #1263's thumbnail-expiry skip (`TextureData.cpp:336-340`). G-11 notes a related in-flight-stat race the erase-ordering fix does not close.
- **Already written:** the code before any fix leaves stale `true` entries only in the live session's in-memory cache (never on disk); a reset clears it, and ES resets after a game exit (`FileData.cpp:1113`). Nothing inherited on disk. The fix changes only in-session behaviour.
- **Proposed disposition:** a `bug`: unlink first, then erase; #1263's reads use `exists(path, false)`; 3.26 the covering case; note G-11 as the remaining race. A #585 line.
- **proved:** fix-unit-test (3.26 FAIL at the pin, `exists(p)` reads true after removeFile)

## PL-04: createDirectory races to false, and accepts an existing file

- **Severity:** Low; **category:** File cache; **question:** Q1
- **Source finding:** L-16, 3.15 (passes at pin as written), G-15
- **Lines at the pin:** `FileSystemUtil.cpp:1089-1120`, `:1093-1095`
- **Owner:** T36 (rule 6)
- **What is wrong:** two threads creating one path can both have their `mkdir` fail with EEXIST → false (L-16). And `createDirectory` returns true for any existing path including an ordinary *file* (G-15: `exists(path,false)` does not check it is a directory).
- **Proposed disposition:** a `bug`: treat EEXIST-as-directory as success; return false when the existing path is not a directory; a case for each.
- **proved:** design (read at the pin; a race case and a file-collision case at stage E)

## PL-05: cache reads that an outside writer can stale are not forced uncached

- **Severity:** Medium; **category:** Texture/font cache; **question:** Q2
- **Source finding:** L-12, 3.13, #1263 (OPEN)
- **Lines at the pin:** `TextureData.cpp:331`, `:339`, `:410`; `FileSystemUtil.cpp:213-215`, `:277-281`
- **Owner:** T36 for the cache contract; #1263's picture checkbox stays open for this record (ruling (i))
- **What is wrong:** the video-thumbnail reads decide from the session cache; an outside writer (libvlc's snapshot) or L-19's stale entry makes a just-made file read absent (`:410` returns false) or an expired file read present (`:339`).
- **Proposed disposition:** `exists(path, false)` at `:339` and `:410` (and L-19's order fix serves `:339`); #1263's frame or the unit case cited.
- **proved:** fix-unit-test (3.13 passes; 3.26 shows the stale path)

## PL-06: a failed font atlas allocation leaves a dangling pointer in mTextures

- **Severity:** High; **category:** Lifetimes; **question:** Q2
- **Source finding:** G-1 (second opinion; CONFIRMED at the pin)
- **Lines at the pin:** `Font.cpp:258-275` (push_back `:268`, delete `:275`)
- **Owner:** T36 (rule 6)
- **What is wrong:** `getGlyph`'s fresh-atlas path does `mTextures.push_back(tex)` and then, on the sizing failure, `delete tex` — leaving a freed pointer in `mTextures` that the next glyph or font teardown dereferences/deletes.
- **Proposed disposition:** a `bug`: do not push until the atlas is known good, or pop before delete; an ASan case driving the failure path; a #585 line.
- **proved:** tree (push_back precedes delete at the pin); fix-unit-test at stage E (ASan)

## PL-07: a date format over 256 bytes overruns a stack buffer

- **Severity:** High; **category:** Words; **question:** Q6
- **Source finding:** G-9 (second opinion; CONFIRMED at the pin)
- **Lines at the pin:** `TimeUtil.cpp:415-508` (`char buf[256]`, `*s++` unbounded)
- **Owner:** T36 (rule 6)
- **What is wrong:** `formatDateTime` copies expanded fields into `buf[256]` via `*s++ = ...` with no bound against `buf+256`; a format string (theme or locale) expanding past 256 bytes overruns the stack.
- **Proposed disposition:** a `bug`: bound every write to the buffer (or use `std::string`); a case with an over-long format; a #585 line.
- **proved:** tree (no bound on `s` at the pin); fix-unit-test at stage E

## PL-08: copyFile onto the same inode destroys the source

- **Severity:** High (data loss); **category:** Writes; **question:** Q5
- **Source finding:** G-16 (second opinion; CONFIRMED at the pin)
- **Lines at the pin:** `FileSystemUtil.cpp:1481-1509`
- **Owner:** T36 (rule 6)
- **What is wrong:** `copyFile` has no `src==dst`/inode guard; it opens the source `"rb"` and the destination `"wb"` (which truncates) and copies — so an identical path or a hard-link alias truncates the source to empty, then reports true.
- **Already written:** the defect is in what the code *does* at copy time, not a format on disk; nothing inherited. A device that already ran a same-path copy has already lost that file — no migration can recover it, so the fix is forward-only and the guard prevents recurrence.
- **Proposed disposition:** a `bug`: refuse when `src` and `dst` resolve to the same file (canonical path or stat inode+dev); a case with a path and its hard link; a #585 line.
- **proved:** tree (no guard at the pin); fix-unit-test at stage E

## PL-09: loadFromPdf returns false after a successful load

- **Severity:** Medium; **category:** Texture/font cache; **question:** Q2
- **Source finding:** G-4 (second opinion; CONFIRMED at the pin)
- **Lines at the pin:** `TextureData.cpp:425-444` (`retval` never set on success)
- **Owner:** T36 (rule 6)
- **What is wrong:** `loadFromPdf` sets `bool retval = false`, calls `initImageFromMemory(...)` at `:441` without assigning its result, and returns `retval` — so a PDF page that loaded reports failure.
- **Proposed disposition:** a `bug`: `retval = initImageFromMemory(...)`; a case that loads a one-page fixture; a #585 line.
- **proved:** tree (retval unset on the success path)

## PL-10: more upstream correctness defects the second opinion found (grouped)

- **Severity:** Medium (the overreads) / Low (the leaks and the classifications); **category:** mixed; **question:** Q5/Q6/Q1/Q2
- **Source finding:** G-2, G-3, G-5, G-6, G-7, G-10, G-12, G-13, G-14, G-20, G-21 (second opinion; source-supported, each to be verified with a case at stage E)
- **Lines at the pin:** per `04` § What `02` missed
- **Owner:** T36 (rule 6), each a contained guard/bound/return
- **What is wrong:** the overreads (G-6 `startsWithIgnoreCase` past both terminators; G-7 `proper` splitting a 4-byte char into a `length()-2` underflow; G-10 the date parser reading past the input), the null/ignored-failure paths (G-3 font reload, G-14 broken-symlink removeFile returns true without unlinking), the leaks (G-2 glyph objects, G-5 CBZ/VLC argv), the mis-classifications (G-13 a FIFO/socket read as a regular file, G-12 the `/*` wildcard published before children), the unchecked arithmetic (G-20 SVG `w*h*4`), and the dropped time (G-21).
- **Proposed disposition:** one `bug` per finding at stage D, each with its case; the overreads and G-14 first (correctness/safety), the leaks and classifications after.
- **proved:** design (each read at the pin; a case per finding at stage E)

## Collisions (recorded, not re-fixed here)

| Finding | Lines | Fixed on | Disposition |
| --- | --- | --- | --- |
| L-02 (`readAllText` under 3 bytes) | `FileSystemUtil.cpp:1369-1379` | T20 `d9afa5c7c` (#1177) | collision; 3.4 the FAIL-at-pin control; a #585 line owed (T20 `02:337`) |
| L-03 rename half (`renameFile` absent source) | `FileSystemUtil.cpp:1451-1455` | T21 `f7c16144d` (#1191) | collision; a #585 line owed (#1191 `:21`) |
| L-06 (`GetShOutput` drops last byte) | `Platform.cpp:891-905` | T26 `a5d2d3756` (#1225) | collision; 3.9 the control; a #585 line owed (T26 `02:819`) |

## Pauses and errata

| Item | Lines | Disposition |
| --- | --- | --- |
| L-04 (`writeAllText` void) | `FileSystemUtil.cpp:1429-1446` | **pause**: the function's return or its supersession by `AtomicFile::writeText` is #1186's; call sites their owners' |
| L-08 (font height not fixed after the constructor) | `Font.cpp:107`, `:115-117`, `:420-421` | **rule erratum** against `es-code-traps.md:118`, with 3.8's positive; the seat narrowed it (height is stable only after a *successful* ASCII preload); for the coordinator's sweep, with T34 PL-17 |
| L-13 (`runSystemCommand` returns 0, blocks) | `Platform.cpp:853-880` | **rule erratum** against `es-native-ui.md:103`, with 3.7; G-19 widens it (a signalled child → `WEXITSTATUS`; interrupted `waitpid`); #1220 the callers' |
| L-14 (`maskSecrets` gaps) | `StringUtil.cpp:446-804` | the seat narrowed it (not "`=`-only"; G-17 a quoted `"--password"` evades it); a `bug` for the JSON/colon/header/quoted-flag shapes, severity pending whether a real logged sink is shown |
| L-05 (`run()` pipe wrap) | `Platform.cpp:162-168` | the seat narrowed it (conditional, not a proven launch kill); G-07's `SigIgn=0x1000` shows the launch gets EPIPE; G-18 widens it (unquoted log path, `2>` binds the last command); recorded, a `bug` for the quoting |

## The held, filed at stage D as neutral public bugs (one each)

| Hold | Public title (neutral) | Record |
| --- | --- | --- |
| h1 | ES: archive extraction does not confine members to the destination | `/workspace/tmp/m6-t36/held/h1-archive-extraction.md` (sha256 in `00`, `SHA256SUMS`) |
| h2 | ES: getCanonicalPath folds into fixed arrays without a bound | `.../h2-canonical-path.md` |
| h3 | ES: a ROM's path is not fully escaped for the launch shell | `.../h3-escaped-path.md` |

## Phase 7 resolution gate

Pending stage D (the pause records the coordinator's rulings and any stream brief) and stage E (the fixes). No fix has landed; every outcome is **Pending**.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | 3.1 FAIL at the pin (`stage-c/build-tests.out`); fix + sorted-table/dotless-i cases at stage E |
| PL-02 | Open | 3.2 FAIL at the pin; fix + cases at stage E |
| PL-03 | Open | 3.26 FAIL at the pin (`exists(p)` reads true); unlink-first fix at stage E |
| PL-04 | Open | read at the pin; race + file-collision cases at stage E |
| PL-05 | Open | 3.13 passes, 3.26 shows the stale path; `exists(path,false)` fix at stage E |
| PL-06 | Open | G-1 CONFIRMED at the pin (push_back precedes delete); ASan case at stage E |
| PL-07 | Open | G-9 CONFIRMED at the pin (no bound on `s`); over-long-format case at stage E |
| PL-08 | Open | G-16 CONFIRMED at the pin (no same-inode guard); hard-link case at stage E |
| PL-09 | Open | G-4 CONFIRMED at the pin (`retval` unset); one-page fixture at stage E |
| PL-10 | Open | G-2/3/5/6/7/10/12/13/14/20/21 read at the pin; one case per finding at stage E |

## punch_index

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Words
  question: Q6
  source_finding: "L-01, 3.1, G-8"
  outcome: "open"
- id: PL-02
  severity: "Medium"
  category: Writes
  question: Q5
  source_finding: "L-03, 3.2"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: "File cache"
  question: Q1
  source_finding: "L-19, 3.26, G-11"
  outcome: "open"
- id: PL-04
  severity: "Low"
  category: "File cache"
  question: Q1
  source_finding: "L-16, 3.15, G-15"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: "Texture/font cache"
  question: Q2
  source_finding: "L-12, 3.13, #1263"
  outcome: "open"
- id: PL-06
  severity: "High"
  category: Lifetimes
  question: Q2
  source_finding: "G-1"
  outcome: "open"
- id: PL-07
  severity: "High"
  category: Words
  question: Q6
  source_finding: "G-9"
  outcome: "open"
- id: PL-08
  severity: "High"
  category: Writes
  question: Q5
  source_finding: "G-16"
  outcome: "open"
- id: PL-09
  severity: "Medium"
  category: "Texture/font cache"
  question: Q2
  source_finding: "G-4"
  outcome: "open"
- id: PL-10
  severity: "Medium"
  category: mixed
  question: Q5
  source_finding: "G-2, G-3, G-5, G-6, G-7, G-10, G-12, G-13, G-14, G-20, G-21"
  outcome: "open"
```

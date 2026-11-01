**T36 (#683) stage-D pause, 00:12 UTC 2026-11-01.** Distribution at `2e5229eed7`; ES worktree at the pin, 0 changes. The audit issue, the ten bugs and the three held bugs are filed; the lane waits here for your dispositions and the stream brief.

**Filed:** audit **#1358** (sub-issue of #683); bugs **#1359-#1368**; held bugs **#1369-#1371** (neutral, symptom class only, details under D-WORKFLOW-215).

## Proposed disposition per punch item

| Item | Bug | Sev | Proposed | Why |
| --- | --- | --- | --- | --- |
| PL-01 | #1362 | Med | **Resolve (rule 6)** | `toUpper`/`toLower` byte-wise fold + unsorted table/dotless-i (G-8); decode/map/re-encode, sort. 3.1 FAIL-at-pin control. |
| PL-02 | #1363 | Med | **Resolve (rule 6)** | `copyFile` true over absent source / short write; return false, check counts. 3.2 control. |
| PL-03 | #1364 | Med | **Resolve (rule 6)** | L-19: unlink before erase; #1263's reads uncached. 3.26 control (L-19 proved on the VM). Note G-11's residual race. |
| PL-04 | #1365 | Low | **Resolve (rule 6)** | `createDirectory` EEXIST race + accepts a file; treat EEXIST-dir as success, reject a file. |
| PL-05 | #1366 | Med | **Resolve (rule 6)** | `exists(path,false)` at TextureData's thumbnail reads; relates #1263 (its checkbox stays open, ruling (i)). |
| PL-06 | #1359 | **High** | **Resolve (rule 6)** | dangling font-atlas pointer (G-1, confirmed at pin); push after the atlas is good, or pop before delete. ASan case. |
| PL-07 | #1360 | **High** | **Resolve (rule 6)** | date-format stack overflow (G-9, confirmed); bound the buffer. |
| PL-08 | #1361 | **High** | **Resolve (rule 6)** | same-inode `copyFile` destroys source (G-16, confirmed, data loss); refuse src==dst. |
| PL-09 | #1367 | Med | **Resolve (rule 6)** | `loadFromPdf` always false (G-4, confirmed); assign `retval`. |
| PL-10 | #1368 | Med/Low | **Resolve the safety/overreads; your call on the minor leaks** | G-6, G-7, G-10, G-14, G-20, G-3 (overreads / null-deref / unchecked arithmetic) -> Resolve; G-2, G-5, G-12, G-13, G-21 (leaks, races, classifications) -> Resolve or **Defer to Backlog** at your preference. |

All ten are **upstream-carried**, so each is a rule-6 contained fix (a guard, a bound, a return, a quote), proven twice at stage E with an `Already written:` line.

## Collisions (recorded, not re-fixed; #585 lines owed)

- L-02 `readAllText` under 3 bytes -> T20 `d9afa5c7c` (#1177); 3.4 the control.
- L-03 `renameFile` absent-source half -> T21 `f7c16144d` (#1191).
- L-06 `GetShOutput` last byte -> T26 `a5d2d3756` (#1225); 3.9 the control.

## Pauses and errata (your ruling)

- **L-04** (`writeAllText` void return): the function's return or its supersession by `AtomicFile::writeText` is **#1186's**; call sites their owners'. Hold for #1186.
- **L-08** rule erratum vs `es-code-traps.md:118` (font height not fixed after the constructor; the seat narrowed it to "stable only after a *successful* ASCII preload"), with T34 PL-17 -- **your sweep**.
- **L-13** rule erratum vs `es-native-ui.md:103` (`runSystemCommand` returns 0, blocks; G-19 widens it), #1220 the callers' -- **your sweep**.
- **L-05** / **L-14**: the seat narrowed both (L-05 conditional not a proven launch kill -- G-07's `SigIgn=0x1000` shows EPIPE; L-14 not "=-only", G-17 a quoted flag evades it). A `bug` for the quoting/mask gaps, severity pending whether a real logged sink is shown.

## Held (your call on routing to the maintainer)

#1369 (archive extraction confinement), #1370 (getCanonicalPath OOB write), #1371 (launch-shell escaping): records at `/workspace/tmp/m6-t36/held/` (sha256 in `00`). You tell the maintainer by path and severity on #346.

## Owed before the hand-back (carried)

- `es-unit-tests` retried against the build root's rapidjson (the host attempt's command, first error whole and reason are in `02` § The runs; no GENERIC_X64 build root here currently has rapidjson built, and M7 held a compile START at the attempt -- pending M7-clear + a built root).
- The stand-in's four T36 fakes (Font/FreeType, TextureData/vlc, the three renderers/GLES3) and the renderers positive under `-DUSE_OPENGLES_30` (bracketed compiles, no M7 START open).

The lane pauses here for your dispositions and the stage-E stream brief.

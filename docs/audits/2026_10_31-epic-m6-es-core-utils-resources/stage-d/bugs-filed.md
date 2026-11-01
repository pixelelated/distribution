# Stage D: the audit issue and the bugs filed (T36 #683)

Filed at the stage-D pause, 2026-11-01, as `issue-tracking.md` and `bugs-are-agent-first.md` require (every lead that FAILs at the pin is a `bug`; the three held findings are neutral public bugs under D-WORKFLOW-215).

## The audit issue
- **#1358** — audit issue, a sub-issue of #683; its checklist is the 10 punch items PL-01..PL-10.

## The bugs (public), by punch item
| Bug | Punch | Stream | File |
| --- | --- | --- | --- |
| #1359 | PL-06 (G-1) | S1 | resources/Font.cpp |
| #1360 | PL-07 (G-9) | S2 | utils/TimeUtil.cpp |
| #1361 | PL-08 (G-16) | S3 | utils/FileSystemUtil.cpp |
| #1362 | PL-01 (L-01, G-8) | S8 | utils/StringUtil.cpp |
| #1363 | PL-02 (L-03) | S3 | utils/FileSystemUtil.cpp |
| #1364 | PL-03 (L-19) | S4 | utils/FileSystemUtil.cpp |
| #1365 | PL-04 (L-16) | S3 | utils/FileSystemUtil.cpp |
| #1366 | PL-05 (L-12) | S4 | utils/FileSystemUtil.cpp, resources/TextureData.cpp |
| #1367 | PL-09 (G-4) | S9 | resources/TextureData.cpp |
| #1368 | PL-10 (six G-items) | S10 | StringUtil/TimeUtil/FileSystemUtil/TextureData/Font + Platform |

## The held findings (neutral public bugs, D-WORKFLOW-215 — file and symptom class only)
| Bug | Hold | Stream | File |
| --- | --- | --- | --- |
| #1369 | h1 (archive extraction) | S7 | utils/ZipFile.cpp |
| #1370 | h2 (canonical path) | S5 | utils/FileSystemUtil.cpp |
| #1371 | h3 (escaped path) | S6 | utils/FileSystemUtil.cpp |

## The ruling-10 bugs (filed at S0 start, D-WORKFLOW-189)
#1374 (L-07), #1375 (L-09), #1376 (L-10), #1377 (L-11 -> Backlog #1372), #1378 (L-15, fixed in S4), #1379 (L-18), #1380 (3.21). The not-yet-fixed six are Backlog candidates (hand-back); #1372 holds PL-10's five (G-2, G-5, G-12, G-13, G-21).

The stage-D pause post itself is `pause-post.md` in this folder.

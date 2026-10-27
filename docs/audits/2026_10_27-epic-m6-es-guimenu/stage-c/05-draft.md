# 05 draft (stage C, before the seat's grades)

The items below are the first reader's, from `02` § The leads, `04` § Risk assessment and the guest cycle. They become `05-punch-list.md` after the seat is graded; a seat item the grading keeps is added or folded in.

| Item | Severity | Category | Q | Family | Leads | Kind |
| --- | --- | --- | --- | --- | --- | --- |
| PL-01 | Medium | Correctness | Q5 | a word or a dialog | L-18 | bug (the fork's) |
| PL-02 | Medium | Correctness | Q2 | a row that writes the wrong place | L-09 | bug (upstream's row; rule 6) |
| PL-03 | Medium | Correctness | Q2 | a row that writes the wrong place | L-10 | bug (upstream's row; rule 6) |
| PL-04 | Medium | Security | Q2 | a row that writes the wrong place | L-08 | bug (the fork's #198 touch, ROCKNIX's page) |
| PL-05 | Medium | Reliability | Q3 | a page's lifetime or thread | L-04 | bug (the fork's cloud pages) |
| PL-06 | Low | Correctness | Q4 | a read that can be stale | L-01, L-02 | bug (the fork's) |
| PL-07 | Low | Correctness | Q4 | a read that can be stale | L-03 | bug (the fork's) |
| PL-08 | Low | UX | Q5 | a word or a dialog | L-19 | bug (the fork's) |
| PL-09 | Low | UX | Q5 | a word or a dialog | L-20 | bug (the fork's) |
| PL-10 | Low | Correctness | Q6 | a row that reads the wrong place | L-05, L-06 | bug (the fork's callers of `es-core`'s reader) |
| PL-11 | Low | UX | Q5 | a word or a dialog | L-21 | bug (the fork's) |
| PL-12 | Low | Docs | Q5 | a word or a dialog | L-23 | the map (D-UI-039, D-UI-046) |
| PL-13 | Low | UX | Q7 | a word or a dialog | L-26 | design, for the pause |
| PL-14 | Low | Maintainability | Q2 | a row that writes the wrong place | L-12 | `GuiSettings.cpp`'s (another slice) |
| PL-15 | Low | Correctness | Q2 | a row that writes the wrong place | L-11 | bug (writes at open) |
| PL-16 | Low | UX | Q5 | a word or a dialog | L-22 | style, for the pause |
| PL-17 | Low | UX | Q5 | a word or a dialog | L-25 | design, against T21's ruling |
| PL-18 | Low | Maintainability | Q6 | -- | L-27 | refactor |
| PL-19 | Low | Maintainability | Q7 | -- | L-28, L-29 | Backlog proposal (D-WORKFLOW-080 option (a)) |
| PL-20 | Low | Correctness | Q2 | a row that writes the wrong place | L-13 | recorded (upstream's rows) |
| PL-21 | Low | UX | Q5 | a word or a dialog | L-15, L-24 | recorded (upstream's, D-UI-079) |
| PL-22 | Low | Reliability | Q4 | a state write | Backlog #1186 (`:11587`) | the dispatch's: onto the atomic writer |
| PL-23 | Low | UX | Q1 | a page's lifetime | L-16 | larger panels only |
| PL-24 | Low | Maintainability | Q1 | a page's lifetime | L-17 | recorded |

Not items: L-07 (T21's S1), L-14 (never built on ROCKNIX), L-30 (the reads table, recorded).

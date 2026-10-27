# 05 draft (stage C, before the seat's grades)

The first reader's items, from `02` § Leads, `04` § Risk assessment and the guest cycle. They become `05-punch-list.md` after the seat is graded; a seat item the grading keeps is added or folded in.

| Item | Severity | Category | Q | Family | Leads | Kind |
| --- | --- | --- | --- | --- | --- | --- |
| PL-01 | Medium | Correctness | Q2 | a state write that can lose the record | L-01 | bug (upstream's base, reaching the fork's pages); its shape for the pause |
| PL-02 | Medium | Correctness | Q2 | a state write that can lose the record | L-02; T26's PL-17 (deferred here) | bug (the base's `save()` early return; the LED page ROCKNIX's) |
| PL-03 | Medium | Security | Q6 | a command built from a player's string | L-05 | bug (ROCKNIX's page; rule 6) |
| PL-04 | Medium | Correctness | Q4 | a check whose failure reads as success | L-06 | bug (ROCKNIX's page; rule 6) |
| PL-05 | Medium | UX | Q4 | a check whose failure reads as success | L-13 | bug (the fork's; with #782's message) |
| PL-06 | Low | Correctness | Q2 | a state write that can lose the record | L-03 | bug (upstream's; rule 6) |
| PL-07 | Low | Correctness | Q4 | a check whose failure reads as success | L-12 | bug (the fork's) |
| PL-08 | Low | UX | Q5 | a page with no help bar | L-26 | bug (the fork's) |
| PL-09 | Low | UX | Q5 | a player sentence outside the vocabulary | L-11, L-27 | bug (the fork's) |
| PL-10 | Low | UX | Q4 | a check whose failure reads as success | L-09, L-10 | bug (the fork's) |
| PL-11 | Low | UX | Q5 | a player sentence outside the vocabulary | L-08 | design, for the pause (a register row) |
| PL-12 | Low | UX | Q5 | a player sentence outside the vocabulary | L-07 | bug (ROCKNIX's page) |
| PL-13 | Low | Docs | Q7 | a page the map does not describe | L-24 | the map (D-UI-039), a stream's commit |
| PL-14 | Low | Reliability | Q3 | work on the interface thread | L-22 | bug (batocera's header; rule 6) |
| PL-15 | Low | Security | Q2 | a credential's sink | L-04 | bug (upstream's row) |
| PL-16 | Low | Correctness | Q2 | a row whose store is wrong | L-15, L-16 | bug (the fork's remembered filters) |
| PL-17 | Low | UX | Q1 | a dialog whose back lands on the acting choice | L-19, L-20, L-21 | recorded (D-UI-079), for the pause |
| PL-18 | Low | Maintainability | Q7 | -- | L-23 | the inventory (the coordinator's), and a removal proposal |
| PL-19 | Low | Reliability | Q3 | work on the interface thread | L-17, L-18 | recorded |
| PL-20 | Low | UX | Q4 | a check whose failure reads as success | L-14 | keep an eye on (ES is root) |

Not items: L-25 (a real seed, recorded).

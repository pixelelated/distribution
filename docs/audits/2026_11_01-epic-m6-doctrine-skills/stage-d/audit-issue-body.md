The T38 audit of the skills, agents and settings (#685, area epic #807, renovation #339). It covers the 52 paths of `.claude/**` less `.claude/rules/**`: the ten skills and the eight agent definitions, 12,783 lines at the dispatch tip `87c2ab0fed` (`reviewed-at`). Nothing was built, run against a provider, or edited under `.claude/` before this issue.

**Depth: Local** (plan § 6c, *a doctrine read*; D-WORKFLOW-184's tier exception in `second-opinions/review-plan.json`). There is no reviewer seat and no keyed call, and Phase 4.6 is recorded as not applicable at Local depth. The checks are the artifact lint and the slice's own checker, `tools/t38-checks.sh` under the folder, seen to fail first on a planted positive per probe.

**57 items:** 0 Critical, 0 High, 16 Medium, 41 Low.
- **`bug` issues:** the 5 sentences a reader acts on wrongly each have one: PL-01 #1389, PL-02 #1390, PL-03 #1391, PL-04 #1392, PL-05 #1393.
- **Questions put to the coordinator at the stage-D pause:** PL-47, PL-48, PL-49, PL-50, PL-51, PL-52.
- **Inherited:** PL-53, PL-54, PL-55, PL-56, PL-57: the export's refresh (#911), the coordinator's rule errata and Backlog leads, and `tools/skills-check`'s inputs (#1373).
- **The rest** are punch items for the fork-adapted skills (begin-delivery, code-auditor, futro, mini-retro, session-resume, session-stash, developer-relations, release-notes). They are fixed only at stage E, under the coordinator's stream brief `docs/reviews/briefs/t38-streams.md`, and never in the council family.

**Folder:** [`docs/audits/2026_11_01-epic-m6-doctrine-skills/`](https://github.com/pixelelated/distribution/tree/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills). The punch list is [`05-punch-list.md`](https://github.com/pixelelated/distribution/blob/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills/05-punch-list.md), with each item's where, acceptance and ladder, and the analysis is [`04-analysis.md`](https://github.com/pixelelated/distribution/blob/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills/04-analysis.md).

**Stage:** D, the pause. Every item is Open until the stream brief; each checkbox is ticked at Phase 7 from its artifact.

## Items

- [ ] **PL-01** (Medium, Q3, L-56, #1389): the acceptance check in `05-punch-list.md` § PL-01 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-02** (Medium, Q3, L-10, #1390): the acceptance check in `05-punch-list.md` § PL-02 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-03** (Medium, Q3, L-11, #1391): the acceptance check in `05-punch-list.md` § PL-03 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-04** (Low, Q3, L-52, #1392): the acceptance check in `05-punch-list.md` § PL-04 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-05** (Low, Q3, L-13, #1393): the acceptance check in `05-punch-list.md` § PL-05 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-06** (Medium, Q7, L-02): the acceptance check in `05-punch-list.md` § PL-06 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-07** (Medium, Q3, L-60): the acceptance check in `05-punch-list.md` § PL-07 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-08** (Medium, Q4, L-63): the acceptance check in `05-punch-list.md` § PL-08 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-09** (Medium, Q7, L-57): the acceptance check in `05-punch-list.md` § PL-09 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-10** (Medium, Q1, L-59): the acceptance check in `05-punch-list.md` § PL-10 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-11** (Medium, Q3, L-53): the acceptance check in `05-punch-list.md` § PL-11 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-12** (Medium, Q3, L-66): the acceptance check in `05-punch-list.md` § PL-12 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-13** (Medium, Q2, L-69): the acceptance check in `05-punch-list.md` § PL-13 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-14** (Medium, Q5, L-70): the acceptance check in `05-punch-list.md` § PL-14 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-15** (Medium, Q7, L-81): the acceptance check in `05-punch-list.md` § PL-15 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-16** (Medium, Q2, L-06, L-07): the acceptance check in `05-punch-list.md` § PL-16 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-17** (Medium, Q2, L-08, L-20): the acceptance check in `05-punch-list.md` § PL-17 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-18** (Low, Q4, L-03): the acceptance check in `05-punch-list.md` § PL-18 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-19** (Low, Q1, L-04): the acceptance check in `05-punch-list.md` § PL-19 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-20** (Low, Q2, L-05): the acceptance check in `05-punch-list.md` § PL-20 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-21** (Low, Q1, L-09): the acceptance check in `05-punch-list.md` § PL-21 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-22** (Low, Q1, L-12, L-73): the acceptance check in `05-punch-list.md` § PL-22 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-23** (Low, Q1, L-14, L-21): the acceptance check in `05-punch-list.md` § PL-23 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-24** (Low, Q1, L-15): the acceptance check in `05-punch-list.md` § PL-24 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-25** (Low, Q6, L-58): the acceptance check in `05-punch-list.md` § PL-25 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-26** (Low, Q5, L-16): the acceptance check in `05-punch-list.md` § PL-26 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-27** (Low, Q1, L-17): the acceptance check in `05-punch-list.md` § PL-27 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-28** (Low, Q2, L-19): the acceptance check in `05-punch-list.md` § PL-28 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-29** (Low, Q3, L-51): the acceptance check in `05-punch-list.md` § PL-29 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-30** (Low, Q1, L-54): the acceptance check in `05-punch-list.md` § PL-30 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-31** (Low, Q6, L-55): the acceptance check in `05-punch-list.md` § PL-31 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-32** (Low, Q7, L-61): the acceptance check in `05-punch-list.md` § PL-32 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-33** (Low, Q7, L-62): the acceptance check in `05-punch-list.md` § PL-33 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-34** (Low, Q4, L-64): the acceptance check in `05-punch-list.md` § PL-34 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-35** (Low, Q6, L-65): the acceptance check in `05-punch-list.md` § PL-35 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-36** (Low, Q4, L-67): the acceptance check in `05-punch-list.md` § PL-36 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-37** (Low, Q4, L-71): the acceptance check in `05-punch-list.md` § PL-37 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-38** (Low, Q4, L-72): the acceptance check in `05-punch-list.md` § PL-38 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-39** (Low, Q2, L-74): the acceptance check in `05-punch-list.md` § PL-39 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-40** (Low, Q6, L-75): the acceptance check in `05-punch-list.md` § PL-40 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-41** (Low, Q7, L-79): the acceptance check in `05-punch-list.md` § PL-41 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-42** (Low, Q4, L-80): the acceptance check in `05-punch-list.md` § PL-42 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-43** (Low, Q7, L-82): the acceptance check in `05-punch-list.md` § PL-43 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-44** (Low, Q7, L-83): the acceptance check in `05-punch-list.md` § PL-44 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-45** (Low, Q7, L-84): the acceptance check in `05-punch-list.md` § PL-45 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-46** (Low, Q7, L-85): the acceptance check in `05-punch-list.md` § PL-46 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-47** (Medium, Q6, L-22): the acceptance check in `05-punch-list.md` § PL-47 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-48** (Low, Q7, L-24): the acceptance check in `05-punch-list.md` § PL-48 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-49** (Low, Q4, L-28): the acceptance check in `05-punch-list.md` § PL-49 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-50** (Low, Q2, L-29): the acceptance check in `05-punch-list.md` § PL-50 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-51** (Low, Q7, L-68): the acceptance check in `05-punch-list.md` § PL-51 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-52** (Low, Q2, L-27): the acceptance check in `05-punch-list.md` § PL-52 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-53** (Low, Q6, L-30 to L-50, L-76 to L-78): the acceptance check in `05-punch-list.md` § PL-53 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-54** (Low, Q5, L-47): the acceptance check in `05-punch-list.md` § PL-54 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-55** (Low, Q1, L-22's rule half, L-23, L-50, D-QA-040, worktrees.md, the lost spaces): the acceptance check in `05-punch-list.md` § PL-55 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-56** (Low, Q2, the checker's steps; register-check's LIVE): the acceptance check in `05-punch-list.md` § PL-56 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.
- [ ] **PL-57** (Low, Q6, L-18, L-44): the acceptance check in `05-punch-list.md` § PL-57 passes, and the Phase 7 gate records its outcome with the commit or the issue that shows it.

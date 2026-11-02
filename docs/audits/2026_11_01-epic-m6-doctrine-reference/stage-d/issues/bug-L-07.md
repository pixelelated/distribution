T39 #686, PL-07 / L-07. **Severity: Medium.** Confirmed by the accepted A–C audit; filing at Stage D does not claim a fix.

## Trace

`docs/backup-contents.md:3-4` calls itself the source of truth for public documentation but names BACKUP CONFIGURATIONS, RESTORE FROM BACKUP and RESTORE EVERYTHING. The accepted L-07 source lookup at ES pin `16dbac5211` found zero instances of each literal; the configurations/everything vocabulary also conflicts with D-UI-022. A documentation writer copying the reference gives players menu labels the pin does not ship.

Evidence: [accepted finding verification](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/04-analysis.md#l-07-docsbackup-contentsmd3-4); [forward audit and retained receipts](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/02-forward-audit.md). Reviewed source: `86ebb6dffc`. [Stage-C acceptance](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582545265).

**Already written:** The repository backup reference and drafts sourced from it carry these labels. This audit does not establish that a public page was deployed with them.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it.

## Acceptance

- [ ] The committed reference uses labels and content tiers derived from the pinned ES source, with source path/line citations for each replacement. The receipt includes the obsolete-label before/after output and literal-to-source mapping; the three obsolete labels are absent from current instructions.

## Ownership

Reference wording only. Public documentation follow-through stays with its owner; no ES edit, pin change or guest test. Execution waits for the coordinator's `docs/reviews/briefs/t39-streams.md`. This reactive bug has no milestone or parent; the audit punch list will link it.

Stage-D filing identity: Codex / GPT-6-Astra / xhigh; session 01a19d12-0c07-7ba3-88b8-ab9d609f4d67; Herdr T1 wN:p4.
No A–C test was repeated for this filing.

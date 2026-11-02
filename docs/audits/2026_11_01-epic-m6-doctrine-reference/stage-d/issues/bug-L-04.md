T39 #686, PL-04 / L-04. **Severity: Medium.** Confirmed by the accepted A–C audit; filing at Stage D does not claim a fix.

## Trace

`docs/rasteratops/cloud-layout.md:16` and `docs/releases/pr/08-saves.md:5` describe automatic cloud-folder migration as current. The accepted L-04 evidence finds no D-CLOUD-175 citation in either document and no cloud_migrate_layout symbol in the shipped-OS projects/packages/scripts scope. D-CLOUD-175 retires automatic migration. The separately recorded 127 tool matches are historical/tool material, not shipped behavior. A reader or PR writer would promise a migration that the OS no longer performs.

Evidence: [accepted finding verification](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/04-analysis.md#l-04-docsrasteratopscloud-layoutmd16-docsreleasespr08-savesmd5); [forward audit and retained receipts](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/02-forward-audit.md). Reviewed source: `86ebb6dffc`. [Stage-C acceptance](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582545265).

**Already written:** The cloud-layout reference and the 08-saves PR description already carry the current-tense claim.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it.

## Acceptance

- [ ] Both committed documents state the retirement and cite D-CLOUD-175 without promising automatic migration. The receipt names the corrected passages and the retained-name classifications, with L-04 before/after output and the applicable retired-name check.

## Ownership

The two reference documents under ruling (l). No cloud operation, OS behavior or historical evidence deletion. Execution waits for the coordinator's `docs/reviews/briefs/t39-streams.md`. This reactive bug has no milestone or parent; the audit punch list will link it.

Stage-D filing identity: Codex / GPT-6-Astra / xhigh; session 01a19d12-0c07-7ba3-88b8-ab9d609f4d67; Herdr T1 wN:p4.
No A–C test was repeated for this filing.

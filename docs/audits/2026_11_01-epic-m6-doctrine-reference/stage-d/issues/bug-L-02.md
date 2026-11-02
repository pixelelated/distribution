T39 #686, PL-02 / L-02. **Severity: Medium.** Confirmed by the accepted A–C audit; filing at Stage D does not claim a fix.

## Trace

`README.md:9` tells a player to use instructions attached to release 0.0.1. The accepted L-02 trace records one such sentence, while the retained release listing contains rc1-20260929, dev-20260827 and dev-rk3326-20260819, with no 0.0.1; #344 was open at review. The sentence was introduced at `3d7c075f63` on 2026-10-02 for a release that was never cut. A player following the front page reaches no corresponding release instructions.

Evidence: [accepted finding verification](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/04-analysis.md#l-02-readmemd9); [forward audit and retained receipts](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/02-forward-audit.md). Reviewed source: `86ebb6dffc`. [Stage-C acceptance](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582545265).

**Already written:** The repository front page contains the misleading release pointer. This establishes exposure to readers, not a count of affected people.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it.

## Acceptance

- [ ] The committed README describes the actual publication state and points only to existing instructions. The fix receipt includes the corrected sentence, its destination artifact or a contemporaneous release listing, and L-02's before/after check output.

## Ownership

README wording under NAMING.md and brief ruling (c); no release publication. Execution waits for the coordinator's `docs/reviews/briefs/t39-streams.md`. This reactive bug has no milestone or parent; the audit punch list will link it.

Stage-D filing identity: Codex / GPT-6-Astra / xhigh; session 01a19d12-0c07-7ba3-88b8-ab9d609f4d67; Herdr T1 wN:p4.
No A–C test was repeated for this filing.

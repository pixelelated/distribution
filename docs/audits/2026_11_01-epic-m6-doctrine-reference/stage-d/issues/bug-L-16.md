T39 #686, PL-16 / L-16. **Severity: Medium.** Confirmed by the accepted A–C audit; filing at Stage D does not claim a fix.

## Trace

`docs/device-testing-policy.md:94` supplies a reusable read mask. The accepted L-16 trace shows that its expression lacks the command-line flag form added to engineering-practices.md on 2026-10-30. A reader copying the policy expression can leave a credential flag's value visible in command output. This is a documented mask mismatch; T39 did not observe or reproduce an actual credential disclosure.

Evidence: [accepted finding verification](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/04-analysis.md#l-16-docsdevice-testing-policymd94); [forward audit and retained receipts](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference/02-forward-audit.md). Reviewed source: `86ebb6dffc`. [Stage-C acceptance](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582545265).

**Already written:** The incomplete mask is already written in the device-testing policy for readers to copy.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it.

## Acceptance

- [ ] The committed policy mask includes the canonical rule's command-line flag coverage as well as assignment coverage. The fix receipt cites both expressions and the L-16 before/after check. Any later synthetic verification builds placeholders at runtime and records only redacted output; no real credential is read.

## Ownership

Policy text under ruling (l), with the canonical rule read-only. No device or credential read. Execution waits for the coordinator's `docs/reviews/briefs/t39-streams.md`. This reactive bug has no milestone or parent; the audit punch list will link it.

Stage-D filing identity: Codex / GPT-6-Astra / xhigh; session 01a19d12-0c07-7ba3-88b8-ab9d609f4d67; Herdr T1 wN:p4.
No A–C test was repeated for this filing.

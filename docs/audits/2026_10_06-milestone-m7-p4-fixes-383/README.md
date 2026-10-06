# M7 P4 fixes audit — independent review pending

The authorized primary audit is complete through Phase4.5. All261 forward
criteria are recorded:204PASS,36PARTIAL,3FAIL,18SKIP. Independent entries were
completed before prior answers were opened;123prior criteria are compared.
Phase3 covers30rules,74distinct blindspots and190supporting-history criteria.
The latter are historical trust review, not190new test executions.

Three product findings remain: #467 content recognition, #468 refusal reason
and #469 French sign-in text. Refutation03 repeats the seven actual14 cases,
3PASS/4FAIL expected, with no state changes and actual process/port cleanup.
No product patch, new image or RC clearance exists.

Phase4.6 awaits approval for the exact prepared source/spec/QA transfer through
OpenRouter to Fable5.1/xhigh, blind then refutation. Automatic review refused
the transfer before execution; authentication itself is restored. No external
call or background build/VM/reviewer process is active. After approval, use a
fresh sealed durable watcher and verify identity/effort/output provenance.

- [Running log](00-running-log.md): stage timestamps and failed attempts.
- [Research](01-research-notes.md): primary sources and exact frozen scope.
- [Forward audit](02-forward-audit.md):261entries and123prior comparisons.
- [Retrospective](03-retrospective.md): rules, blindspots and interactions.
- [Provisional analysis](04-analysis.md): findings, coverage and remaining gaps.
- `evidence/forward-verdicts.json`: authoritative independent scorecard.
- `inputs/scoped-criteria.json`:455exact criteria,261forward/190supporting/4later.
- `second-opinions/`: plan, prepared blind packet, input hashes and dispatch state.

Frozen distribution7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2;
ESf6f0c134212bc696f2f6a747c8d390a588f2f0ce;
bundleb77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1.
Qualified UI prerequisite:109assertions/23directly reviewed frames, allfour0.
Phase5 final punch list and Phase6 tracker follow verified independent review;
Phase7 fixes/requalification precede capacity#461 and device/P5 work.

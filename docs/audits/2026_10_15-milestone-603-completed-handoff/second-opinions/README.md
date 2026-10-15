# Phase 4.6 transfer preparation

Preparation checkpoint: neither external transfer was authorized or started when this packet was sealed. The owner subsequently directed completion of #603; `authorization.json` records the unchanged scope. Root started the blind call at21:14:18UTC under `/tmp/pix-m7-audit603-blind-20261015-01`; the running log/checkpoint owns its live status. Refutation remains gated on the verified first response. Both calls must use the installed Facilitator, member `claude`, provider `openrouter`, Fable 5.1 at xhigh, serially. No formal council genesis is required.

The blind prompt is concrete in `claude-blind-brief.md`. The refutation base is concrete in `claude-refutation-base.md`; the final prompt will append only the verified blind answer, at most 131,072 bytes, with its original digest and size. Its final digest cannot exist before that answer. Parent may request authorization for this explicit two-call scope; any additional data or base change requires a new manifest/authorization determination. No other files are implicitly transmitted.

`packet-manifest.json` gives exact sizes, SHA-256 hashes, included original source hashes, line ranges, and sanitization. The evidence packet includes all 67 literal criteria, labeled primary read notes, exact source excerpts and original command result excerpts. Primary verdicts/refutations/findings are absent from the blind prompt. The refutation base includes the whole primary forward audit and retrospective and analysis through Finding Verification. Images are not attached; pixel review remains a primary observation.

Commands after authorization, under a fresh monitored owner allocated by root:

```text
tools/council/run invoke --member claude --provider openrouter --prompt-file docs/audits/2026_10_15-milestone-603-completed-handoff/second-opinions/claude-blind-brief.md --output docs/audits/2026_10_15-milestone-603-completed-handoff/second-opinions/claude-blind.md
tools/council/run invoke --member claude --provider openrouter --prompt-file docs/audits/2026_10_15-milestone-603-completed-handoff/second-opinions/claude-brief.md --output docs/audits/2026_10_15-milestone-603-completed-handoff/second-opinions/claude-audit.md
```

After each call, inspect actual served identity, successful outcome, Facilitator provenance and output digest. An error or identity failure halts this phase; no provider substitution. Only then assemble/dispatch refutation. Verify each external lead against primary artifacts before Phase 5. No completion marker exists.

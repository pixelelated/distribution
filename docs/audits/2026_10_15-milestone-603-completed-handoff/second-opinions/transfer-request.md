# Exact transfer request — audit #603

Authorize two serial independent-review calls through the existing Council Facilitator to Anthropic Fable 5.1 at xhigh via OpenRouter:

1. Blind pass: `claude-blind-brief.md`, 790,371 bytes, SHA-256 `3da1c2290b787fc113a3bb5809ce11fd7acfe68b7bb717bc404d6203c9350345`.
2. Refutation pass: fixed `claude-refutation-base.md`, 922,168 bytes, SHA-256 `80450a6e6249f9b34e0a7cb6740dd268ea1b4bbbcc99b35077c0641e4d7ccdcc`, plus only the verified sanitized blind response (maximum 131,072 bytes) and its digest/size declaration. The exact combined digest will be recorded after that response exists and before dispatch. No extra repository data or user messages may be appended under this scope.

Both contain the frozen cdd92 audit's 67 literal criteria, bounded public source and original result excerpts. The blind prompt omits primary verdicts/findings; the second includes the primary analysis and the blind answer. Host home paths and opaque encoded command payloads were removed from transfer copies. No image pixels, provider configuration/credentials, owner game/save payloads, full issue comments or firmware images are included. The manifest records original and transfer hashes, selected line ranges and substitutions.

This is the two-call Independent audit already selected, not a formal council. No external call or transfer has started. Root must also allocate a fresh monitored owner before execution. A served-identity/provenance/output-digest failure halts the phase.

The exact approval requirement comes from `.claude/skills/code-auditor/references/phases.md`, Phase 4.6: “External provider permission is separate from reviewer selection.” Its fail-closed rule says: “if ... the external transfer is not authorized, record the blocker and keep this phase pending. Do not proceed to Phase 5”. The prior transfers were specific to older packets and do not cover these new bytes.
